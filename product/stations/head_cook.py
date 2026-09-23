"""Station 7 — the head cook (code, no AI) with the small taster on every generated output (spec §3, §4.6, §4.7, §5, §6).

"One dish, one memory":
  - FILMS: ONE master plate first (the sample picture the customer saw, re-checked by the small taster), approved by the
    customer (or the founder) before any shot is paid for. Every shot starts from the master plate or from the previous
    shot's END FRAME (extracted by code, USD 0); shot first frames are generated WITH the master plate (and the previous
    end frame) as references. Risky shots are produced and checked first; every other shot waits on them.
  - IMAGES: the first format's plate is the master; the other formats are generated with it as a reference.
  - Small taster on each generated picture/clip. "No" is binding: retry once with a changed request (its notes as a
    correction), then the chef re-plans that shot (1 per shot), then the founder decides. Never a third identical request.
  - Every output is written to a new, unique path (write-once). The Production log form records source images, links,
    routes, attempts and choices.
"""
from __future__ import annotations

import json
import shutil
import time
from pathlib import Path

from product import compose, cost, flow, media, prompts, verify
from product.dispatch import DispatchFailed, GuardRefused, IdenticalRequestRefused
from product.reasoning import ProviderUnavailable
from product.store import BudgetExhausted, utc_now

TRANSIENT_RETRIES = 3


class NeedsFounder(Exception):
    def __init__(self, node_id, candidates, why):
        super().__init__(f"{node_id}: {why}")
        self.node_id, self.candidates, self.why = node_id, candidates, why


class ShotReplan(Exception):
    def __init__(self, node_id, shot, why):
        super().__init__(f"{node_id}: shot {shot} rejected twice — {why}")
        self.node_id, self.shot, self.why = node_id, shot, why


def fid(fmt: str) -> str:
    return fmt.replace(":", "x")


def _aspect(k, job_id):
    u = k.store.artifact(job_id, "understanding")
    fmts = u["deliverable"].get("formats") or (["9:16"] if u["deliverable"]["media"] == "video" else ["1:1"])
    if u["deliverable"]["media"] == "video":
        return fmts[0] if fmts[0] in ("9:16", "16:9") else "9:16"
    return fmts[0]


def guard(k, job_id, recipe):
    u = k.store.artifact(job_id, "understanding")
    return prompts.guard_for({"brand": u.get("brand")}, recipe, k.brief(job_id))


def product_refs(k, job_id, limit=2) -> list:
    """Reference photos for the generator: product views first, then details; never lifestyle/people or logo photos.
    Infographic photos go last (EQ-006: annotated references are risky)."""
    u = k.store.artifact(job_id, "understanding") or {}
    order = {"product_view": 0, "product_detail": 1, "infographic": 2}
    roles = sorted([r for r in u.get("photo_roles", []) if r["role"] in order], key=lambda r: order[r["role"]])
    out = []
    for r in roles[:limit]:
        a = k.store.asset(r["asset_id"])
        if a:
            out.append((a["content_type"], Path(a["path"]).read_bytes()))
    return out


# ── the sample picture (before approval) ───────────────────────────────────────────────────────────────────────────
def sample_picture(k, job_id: str, recipe: dict):
    """What the customer sees on the plan card: the film's master plate (or the first format's picture). Paid from the
    planning allowance authorised at submission; production reuses it once the small taster has checked it."""
    job = k.store.job(job_id)
    aspect = _aspect(k, job_id)
    shelf_master = _shelf_master(k, job_id, recipe)
    if shelf_master:
        p = k.store.new_output_path(k.job_dir(job_id) / "gen", "master__shelf", Path(shelf_master["path"]).suffix.lstrip(".") or "png")
        shutil.copyfile(shelf_master["path"], p)
        aid = k.store.add_asset(job_id, path=p, kind="image", source="shelf", content_type="image/png", node_id="preview", role="preview",
                                meta={"shelf_item": shelf_master["id"], "shelf_version": shelf_master["version"], "master": True, "format": aspect})
        k.shelf.record_use(job_id, job["account_id"], shelf_master["id"], "master_plate")
        return aid
    refs = product_refs(k, job_id)
    g = guard(k, job_id, recipe)
    if job["media"] == "image":
        prompt = prompts.still_prompt(recipe, g, aspect=aspect, with_product_ref=bool(refs), with_character_ref=False)
    else:
        prompt = prompts.master_plate_prompt(recipe, g, aspect=aspect, with_product_ref=bool(refs))
    with k.store.timed(job_id, "asset_preparation", "sample picture"):
        aid = k.dispatch.image(job_id, "preview", prompt=prompt, aspect=aspect, refs=refs, guard=g,
                               meta={"format": aspect, "preview": True, "master": job["media"] == "video"})
    k.store.set_asset(aid, role="preview")
    return aid


def _shelf_master(k, job_id, recipe):
    job = k.store.job(job_id)
    for it in k.shelf.approved(job["account_id"], "master_plate"):
        if it["id"] in (recipe.get("reuse_shelf_items") or []) and it["path"]:
            return it
    return None


def _shelf_character(k, job_id, recipe):
    job = k.store.job(job_id)
    for it in k.shelf.approved(job["account_id"], "character"):
        if it["id"] in (recipe.get("reuse_shelf_items") or []):
            return it
    return None


# ── plan: the production graph ─────────────────────────────────────────────────────────────────────────────────────
def plan(k, job_id: str):
    recipe = k.store.artifact(job_id, "recipe")
    job = k.store.job(job_id)
    aspect = _aspect(k, job_id)
    preview = next(iter(k.store.assets(job_id, role="preview")[-1:]), None)
    existing = {n["node_id"]: n for n in k.store.nodes(job_id)}
    want = []
    with k.store.timed(job_id, "asset_preparation", "plan"):
        if job["media"] == "image":
            fmts = k.store.artifact(job_id, "understanding")["deliverable"].get("formats") or ["1:1"]
            master = f"plate_{fid(fmts[0])}"
            for i, f in enumerate(fmts):
                want.append((f"plate_{fid(f)}", "plate", [] if i == 0 else [master],
                             {"aspect": f, "route": "IMG", "reuse": preview["id"] if (preview and i == 0) else None, "master": i == 0}))
                want.append((f"ad_{fid(f)}", "compose_still", [f"plate_{fid(f)}"], {"aspect": f}))
        else:
            eq = k.equipment
            shots = [s for s in recipe["shots"] if s["route"] != "END-CARD"]
            card = next((s for s in recipe["shots"] if s["route"] == "END-CARD"), {"duration_s": 3})
            risky = [s["n"] for s in shots if s["route"] in ("FILM-B", "FILM-C") and eq.verdict(s["action_class"], s["route"])["verdict"] == "risky"]
            shelf_master = _shelf_master(k, job_id, recipe)
            want.append(("master", "master", [], {"aspect": aspect, "route": "IMG", "reuse": preview["id"] if preview else None,
                                                  "shelf_item": shelf_master["id"] if shelf_master else None}))
            char = (recipe.get("character") or {}).get("present")
            if char:
                sc = _shelf_character(k, job_id, recipe)
                want.append(("character", "character", ["master"], {"aspect": aspect, "route": "IMG", "shelf_item": sc["id"] if sc else None}))
            prev = None
            for s in shots:
                deps = ["master"] + (["character"] if char else [])
                if s["starts_from"] == "previous_shot_end" and prev:
                    deps.append(f"shot_{prev}")
                elif prev and s["n"] not in risky:
                    deps.append(f"shot_{prev}")
                deps += [f"shot_{r}" for r in risky if r != s["n"] and s["n"] not in risky]
                spec = {"shot": s["n"], "aspect": aspect, "route": s["route"], "starts_from": s["starts_from"],
                        "previous": f"shot_{prev}" if prev else None, "risky": s["n"] in risky, "fp": _shot_fp(s)}
                want.append((f"frame_{s['n']}", "frame", list(dict.fromkeys(deps)), spec))
                want.append((f"shot_{s['n']}", "shot", [f"frame_{s['n']}"], dict(spec)))
                if s.get("super_id") and not _logo_copy(k, job_id, recipe, s["super_id"]):
                    want.append((f"super_{s['n']}", "super", [f"shot_{s['n']}"], {"shot": s["n"], "copy_id": s["super_id"], "aspect": aspect}))
                prev = s["n"]
            want.append(("music", "music", [], {}))
            want.append(("end_card", "end_card", [], {"aspect": aspect, "duration_s": card["duration_s"]}))
            fin = [f"shot_{s['n']}" for s in shots] + [w[0] for w in want if w[1] == "super"] + ["music", "end_card"]
            want.append(("film", "assemble", fin, {"aspect": aspect, "card_s": card["duration_s"]}))
    keep = []
    for node_id, kind, deps, spec in want:
        old = existing.get(node_id)
        if old and old["status"] == "done" and json.loads(old["spec_json"]).get("fp") == spec.get("fp") and kind not in ("assemble",):
            keep.append(node_id)                 # unchanged work is preserved (a re-plan redoes only what changed)
            k.store.set_node(job_id, node_id, deps_json=json.dumps(deps))
            continue
        k.store.put_node(job_id, node_id, kind=kind, deps=deps, spec=spec, max_draws=2 if kind not in ("assemble",) else 1)
    for node_id in existing:
        if node_id not in [w[0] for w in want]:
            k.store.set_node(job_id, node_id, status="retired", note="not in the current recipe")
    # anything downstream of a changed node is redone
    changed = [w[0] for w in want if w[0] not in keep]
    for c in changed:
        _reset_downstream(k, job_id, c)
    k.store.event(job_id, "system", "plan", {"nodes": [w[0] for w in want], "kept": keep})
    write_log(k, job_id)
    k.store.transition(job_id, "planning", "producing", actor="system")


def _shot_fp(s: dict) -> str:
    from product.store import sha256_json
    return sha256_json({kk: s.get(kk) for kk in ("route", "action", "action_class", "first_frame", "end_state", "starts_from",
                                                 "duration_s", "camera", "product_state", "continuity", "must_not")})[:16]


def _reset_downstream(k, job_id, node_id, note=None):
    nodes = {n["node_id"]: n for n in k.store.nodes(job_id) if n["status"] != "retired"}
    todo, seen = [node_id], []
    while todo:
        x = todo.pop()
        if x in seen or x not in nodes:
            continue
        seen.append(x)
        todo += [m for m, n in nodes.items() if x in json.loads(n["deps_json"])]
    for x in seen:
        spec = json.loads(nodes[x]["spec_json"])
        if x == node_id and note:
            spec["revision_note"] = note
            spec.pop("reuse", None)
        k.store.set_node(job_id, x, status="pending", draws=0, spec_json=json.dumps(spec), selected_asset_id=None,
                         note=f"reset by change to {node_id}")
    return seen


def _logo_copy(k, job_id, recipe, copy_id) -> bool:
    c = next((c for c in recipe.get("copy_deck", []) if c["id"] == copy_id), None)
    return bool(c and k.logo(job_id) and compose.is_logo_line(c))


# ── produce ─────────────────────────────────────────────────────────────────────────────────────────────────────────
def produce(k, job_id: str):
    for n in k.store.nodes(job_id):
        if n["status"] == "running":
            k.store.set_node(job_id, n["node_id"], status="pending", note="restarted after interruption")
    ctx = _ctx(k, job_id)
    while True:
        nodes = {n["node_id"]: n for n in k.store.nodes(job_id) if n["status"] != "retired"}
        if all(n["status"] == "done" for n in nodes.values()):
            break
        waiting = [x for x, n in nodes.items() if n["status"] == "needs_founder"]
        ready = [x for x, n in nodes.items() if n["status"] == "pending"
                 and all(nodes[d]["status"] == "done" for d in json.loads(n["deps_json"]) if d in nodes)]
        if not ready and waiting:
            notes = {x: json.loads(nodes[x]["note"] or "{}").get("why", "") for x in waiting}
            k.to_founder(job_id, "producing", "the small taster rejected every take of " + ", ".join(waiting)
                         + ": the founder picks a take, or closes the job — " + "; ".join(f"{x}: {w}" for x, w in notes.items())[:400],
                         "pick a take")
            return
        if not ready:
            raise _node_failed("no runnable node; states: " + json.dumps({x: n["status"] for x, n in nodes.items()}))
        order = sorted(ready, key=lambda x: (not json.loads(nodes[x]["spec_json"]).get("risky"), x))
        x = order[0]
        if not k.store.take_node(job_id, x):
            continue
        try:
            _run(k, job_id, x, ctx)
        except (BudgetExhausted, ProviderUnavailable):
            k.store.set_node(job_id, x, status="pending")
            raise
        except NeedsFounder as e:
            k.store.set_node(job_id, x, status="needs_founder", note=json.dumps({"candidates": e.candidates, "why": e.why}))
        except IdenticalRequestRefused as e:
            k.store.set_node(job_id, x, status="needs_founder", note=json.dumps({"candidates": _takes(k, job_id, x), "why": str(e)}))
        except ShotReplan as e:
            from product.stations import chef
            k.store.set_node(job_id, x, status="pending")
            try:
                recipe = chef.replan_shot(k, job_id, e.shot, e.why)
            except flow.LimitReached as lim:
                k.store.set_node(job_id, x, status="needs_founder", note=json.dumps({"candidates": _takes(k, job_id, x), "why": str(lim)}))
                continue
            ctx = _ctx(k, job_id)
            _replace_shot_nodes(k, job_id, e.shot, recipe)
        if x == "master" and _master_needs_approval(k, job_id):
            write_log(k, job_id)
            k.store.transition(job_id, "producing", "awaiting_master_approval", actor="system",
                               data={"master": k.store.node(job_id, "master")["selected_asset_id"]})
            k.store.timing_start(job_id, "customer_wait", "master")
            return
    write_log(k, job_id)
    finals = k.final_assets(job_id)
    if not k.store.job(job_id)["first_cut_at"]:
        k.store.set_job(job_id, first_cut_at=utc_now())
    k.store.event(job_id, "system", "cut_ready", {"assets": finals})
    k.store.transition(job_id, "producing", "checking", actor="system")


def _node_failed(msg):
    from product.orchestrator import NodeFailed
    return NodeFailed(msg)


def _replace_shot_nodes(k, job_id, shot_n, recipe):
    s = next(s for s in recipe["shots"] if s["n"] == shot_n)
    for x in (f"frame_{shot_n}", f"shot_{shot_n}"):
        n = k.store.node(job_id, x)
        spec = json.loads(n["spec_json"])
        spec.update(route=s["route"], starts_from=s["starts_from"], fp=_shot_fp(s), replanned=True)
        k.store.set_node(job_id, x, spec_json=json.dumps(spec))
    _reset_downstream(k, job_id, f"frame_{shot_n}")


def _master_needs_approval(k, job_id) -> bool:
    if k.store.job(job_id)["media"] != "video":
        return False
    n = k.store.node(job_id, "master")
    if n["status"] != "done":
        return False
    if json.loads(n["spec_json"]).get("shelf_item"):
        return False                               # already approved by the customer on their shelf
    return not k.store.events(job_id, ("master_approved",))


def approve_master(k, job_id, *, by: str, founder_session: str | None = None):
    """The customer approves the look of the film (the master plate) — or the founder does, on their behalf (spec §6.1)."""
    job = k.store.job(job_id)
    if job["state"] != "awaiting_master_approval":
        raise ValueError("there is no master plate waiting for approval")
    proof = None
    if founder_session:
        proof = k.founder(founder_session, job_id, "approve the master plate")
        by = proof.actor
    aid = k.store.node(job_id, "master")["selected_asset_id"]
    k.store.event(job_id, by, "master_approved", {"asset": aid})
    if not proof:        # the customer approved it once — it goes on their shelf as an approved master plate
        a = k.store.asset(aid)
        sid = k.shelf.propose(job["account_id"], kind="master_plate", key=(k.brief(job_id).get("product") or {}).get("name") or "product",
                              data={"description": (k.store.artifact(job_id, "recipe").get("master_plate") or {}).get("description", ""),
                                    "asset": aid}, source_job_id=job_id, file=Path(a["path"]))
        if k.shelf.item(job["account_id"], sid)["status"] == "proposed":
            k.shelf.decide(job["account_id"], sid, approve=True, by=by)
    k._end_wait(job_id, "master")
    k.store.transition(job_id, "awaiting_master_approval", "producing", actor=by, data={"master_approved": aid})
    write_log(k, job_id)


def founder_select_take(k, job_id, proof, asset_id, reason):
    """The founder overrides the small taster's "no" by picking one of the paid takes (spec §6.4). Nothing is re-bought."""
    a = k.store.asset(asset_id)
    n = k.store.node(job_id, a["node_id"]) if a and a["job_id"] == job_id else None
    if n is None or n["status"] != "needs_founder":
        raise ValueError("that take does not belong to an output waiting for the founder")
    k.store.add_override(job_id, kind="take", target=f"{n['node_id']}:{asset_id}", founder=proof, reason=reason,
                         data={"taster": json.loads(a["meta_json"]).get("inspection")})
    k.store.set_asset(asset_id, status="candidate")
    _done(k, job_id, n["node_id"], asset_id)
    k.store.event(job_id, proof.actor, "take_selected_by_founder", {"node": n["node_id"], "asset": asset_id, "reason": reason})
    if not [x for x in k.store.nodes(job_id) if x["status"] == "needs_founder"] and k.store.job(job_id)["state"] == "paused_for_founder":
        k.store.transition(job_id, "paused_for_founder", "producing", actor=proof.actor, founder=proof, data={"take_selected": asset_id},
                           pause_reason=None)


# ── nodes ───────────────────────────────────────────────────────────────────────────────────────────────────────────
def _ctx(k, job_id):
    recipe = k.store.artifact(job_id, "recipe")
    return {"recipe": recipe, "guard": guard(k, job_id, recipe), "refs": product_refs(k, job_id), "logo": k.logo(job_id),
            "shots": {s["n"]: s for s in recipe.get("shots", [])}, "workdir": k.job_dir(job_id) / "work",
            "cut": 1 + len(k.store.events(job_id, ("cut_ready",)))}


def _run(k, job_id, node_id, ctx):
    n = k.store.node(job_id, node_id)
    spec = json.loads(n["spec_json"])
    ctx["workdir"].mkdir(parents=True, exist_ok=True)
    kind = n["kind"]
    if kind in ("master", "plate", "character", "frame"):
        return _node_image(k, job_id, n, spec, ctx)
    if kind == "shot":
        return _node_shot(k, job_id, n, spec, ctx)
    if kind == "music":
        p, neg = prompts.music_prompt(ctx["recipe"], ctx["guard"])
        aid = _draw(k, job_id, node_id, lambda: k.dispatch.music(job_id, node_id, prompt=p, negative=neg, guard=ctx["guard"]))
        return _done(k, job_id, node_id, aid)
    with k.store.timed(job_id, "composition", node_id):
        from product.stations import assembly
        return getattr(assembly, kind)(k, job_id, n, spec, ctx)


def _done(k, job_id, node_id, asset_id):
    if asset_id:
        k.store.set_asset(asset_id, status="selected")
    k.store.set_node(job_id, node_id, status="done", selected_asset_id=asset_id)


def _draw(k, job_id, node_id, fn):
    """One paid draw. Quality draws are capped by the node's max_draws (2 attempts per output); transient provider failures
    do not use them up (they pause the job as paused_provider after TRANSIENT_RETRIES)."""
    transient = 0
    while True:
        cur = k.store.node(job_id, node_id)
        if cur["draws"] >= cur["max_draws"]:
            raise _node_failed(f"{node_id}: attempt allowance ({cur['max_draws']}) used")
        k.store.set_node(job_id, node_id, draws=cur["draws"] + 1)
        try:
            return fn()
        except (BudgetExhausted, GuardRefused):
            k.store.set_node(job_id, node_id, draws=cur["draws"])
            raise
        except DispatchFailed as e:
            k.store.event(job_id, "system", "provider_failure", {"node": node_id, "class": e.failure_class, "error": str(e)[:300]})
            if not e.retryable:
                raise _node_failed(f"{node_id}: {e}")
            k.store.set_node(job_id, node_id, draws=cur["draws"])
            transient += 1
            if transient >= TRANSIENT_RETRIES:
                raise ProviderUnavailable(f"{node_id}: {e}")
            time.sleep(0 if k.s.provider_mode == "simulated" else 5 * transient)


def _takes(k, job_id, node_id):
    return [x["id"] for x in k.store.assets(job_id, node_id=node_id) if x["status"] in ("rejected", "candidate")]


def _image_request(k, job_id, n, spec, ctx, correction=""):
    """(prompt, refs, instruction, source description) for a generated picture."""
    recipe, g, refs = ctx["recipe"], ctx["guard"], ctx["refs"]
    aspect = spec["aspect"]
    kind = n["kind"]
    if kind == "master":
        p = prompts.master_plate_prompt(recipe, g, aspect=aspect, with_product_ref=bool(refs))
        return p, refs, {"asset": "master plate — the film's one world", "prompt": p}, "product photos"
    if kind == "plate":
        p = prompts.still_prompt(recipe, g, aspect=aspect, with_product_ref=bool(refs), with_character_ref=False)
        use = list(refs)
        src = "product photos"
        if not spec.get("master"):
            m = k.store.asset(k.store.node(job_id, n["deps_json"] and json.loads(n["deps_json"])[0])["selected_asset_id"])
            use = [("image/png", Path(m["path"]).read_bytes())] + use[:1]
            p = p.replace(prompts.NO_LETTERING, "The product and set are exactly as in the first reference image (the master picture), "
                                                "recomposed for this format. " + prompts.NO_LETTERING)
            src = f"master picture {m['id']}"
        if spec.get("revision_note"):
            p = p.replace(prompts.NO_LETTERING, f"Change requested: {spec['revision_note']}. {prompts.NO_LETTERING}")
        if correction:
            p = p.replace(prompts.NO_LETTERING, f"Correct this from the last attempt: {correction}. {prompts.NO_LETTERING}")
        return p, use, {"asset": "hero product picture (text is added later by code)", "prompt": p}, src
    if kind == "character":
        p = prompts.character_prompt(recipe, g, aspect)
        m = _selected_bytes(k, job_id, "master")
        return p, [m], {"asset": "character reference (same world as the master plate)", "prompt": p}, "master plate"
    # a shot's first frame
    s = ctx["shots"][spec["shot"]]
    m = _selected_bytes(k, job_id, "master")
    prev_end = _end_frame(k, job_id, spec.get("previous")) if spec.get("previous") and spec["starts_from"] != "master_plate" else None
    if prev_end is None and spec.get("previous") and not spec.get("risky"):
        prev_end = _end_frame(k, job_id, spec["previous"])
    ch = k.store.node(job_id, "character")
    use = [m] + ([prev_end] if prev_end else []) + (refs[:1] if s.get("product_present") else [])
    if ch and ch["selected_asset_id"]:
        use.append(_selected_bytes(k, job_id, "character"))
    note = (spec.get("revision_note") or "") + (("; " if spec.get("revision_note") and correction else "") + correction if correction else "")
    p = prompts.shot_frame_prompt(recipe, g, s, aspect=aspect, has_previous=bool(prev_end), correction=note)
    return p, use, {"asset": f"first frame of shot {s['n']}", "prompt": p, "first_frame": s["first_frame"],
                    "product_present": s.get("product_present"), "must_not": s.get("must_not", [])}, \
        "master plate" + (f" + end frame of {spec['previous']}" if prev_end else "")


def _node_image(k, job_id, n, spec, ctx):
    node_id = n["node_id"]
    job = k.store.job(job_id)
    # a shot that starts from the previous shot's end frame needs no picture at all: code extracts it (USD 0)
    if n["kind"] == "frame" and spec["starts_from"] == "previous_shot_end" and spec.get("previous"):
        p = _extract_end_frame(k, job_id, spec["previous"], node_id)
        aid = k.store.add_asset(job_id, path=p, kind="image", source="composed", content_type="image/png", node_id=node_id,
                                meta={"source_kind": "previous_shot_end", "from": spec["previous"],
                                      "from_asset": k.store.node(job_id, spec["previous"])["selected_asset_id"]})
        return _done(k, job_id, node_id, aid)
    if spec.get("shelf_item"):
        it = k.shelf.item(job["account_id"], spec["shelf_item"])
        if it["path"]:
            p = k.store.new_output_path(k.job_dir(job_id) / "gen", f"{node_id}__shelf", "png")
            shutil.copyfile(it["path"], p)
            aid = k.store.add_asset(job_id, path=p, kind="image", source="shelf", content_type="image/png", node_id=node_id,
                                    meta={"shelf_item": it["id"], "shelf_version": it["version"], "source_kind": "customer shelf"})
            k.shelf.record_use(job_id, job["account_id"], it["id"], n["kind"])
            k.store.event(job_id, "system", "shelf_reuse", {"node": node_id, "item": it["id"], "version": it["version"]})
            return _done(k, job_id, node_id, aid)
    aid = spec.get("reuse") if spec.get("reuse") and not spec.get("revision_note") and k.store.asset(spec["reuse"]) else None
    if aid:
        k.store.event(job_id, "system", "reuse", {"node": node_id, "asset": aid})
    correction = ""
    while True:
        prompt, refs, instruction, source = _image_request(k, job_id, n, spec, ctx, correction)
        if aid is None:
            aid = _draw(k, job_id, node_id, lambda: k.dispatch.image(job_id, node_id, prompt=prompt, aspect=spec["aspect"], refs=refs,
                                                                   guard=ctx["guard"], meta={"format": spec["aspect"], "shot": spec.get("shot"),
                                                                                             "source_kind": source, "correction": correction}))
        a = k.store.asset(aid)
        verdict = taste(k, job_id, node_id, instruction, a, prev=_prev_bytes(k, job_id, spec))
        if _usable(verdict):
            return _done(k, job_id, node_id, aid)
        correction = _rejected(k, job_id, node_id, aid, verdict)
        aid = None


def _node_shot(k, job_id, n, spec, ctx):
    node_id = n["node_id"]
    s = ctx["shots"][spec["shot"]]
    frame = k.store.asset(k.store.node(job_id, f"frame_{spec['shot']}")["selected_asset_id"])
    use = float(s["duration_s"])
    if spec["route"] == "FILM-A":
        out = k.store.new_output_path(k.job_dir(job_id) / "gen", f"{node_id}__code-motion", "mp4")
        if media.have_ffmpeg():
            media.still_motion(Path(frame["path"]), out, duration_s=use + 0.5)
        else:
            out.write_bytes(Path(frame["path"]).read_bytes())
        aid = k.store.add_asset(job_id, path=out, kind="video", source="composed", content_type="video/mp4", node_id=node_id,
                                meta={"code_motion": True, "from_frame": frame["id"], "in_s": 0.0, "use_s": use, "route": "FILM-A",
                                      "det": {"check_id": "no_in_model_cut", "status": "PASS", "detail": "code motion on one approved still"}})
        return _done(k, job_id, node_id, aid)
    dur = cost.clip_len(use)
    correction = ""
    while True:
        prompt = prompts.clip_prompt(ctx["recipe"], ctx["guard"], s) + (f" Correct: {correction}." if correction else "") + \
            (f" Change requested: {spec['revision_note']}." if spec.get("revision_note") else "")
        negative = prompts.clip_negative(ctx["recipe"], ctx["guard"], s, [])
        aid = _draw(k, job_id, node_id, lambda: k.dispatch.video(job_id, node_id, prompt=prompt, image=(frame["content_type"] or "image/png",
                                                                                                       Path(frame["path"]).read_bytes()),
                                                                 duration_s=dur, aspect=spec["aspect"], negative=negative, guard=ctx["guard"],
                                                                 meta={"shot": s["n"], "route": spec["route"], "from_frame": frame["id"]}))
        a = k.store.asset(aid)
        det = _clip_det(a, use)
        instruction = {"asset": f"clip for shot {s['n']} ({dur}s; {use}s used)", "action": s["action"], "end_state": s["end_state"],
                       "must_not": s.get("must_not", []), "product_present": s.get("product_present")}
        verdict = taste(k, job_id, node_id, instruction, a, prev=[("image/png", Path(frame["path"]).read_bytes())], video_seconds=dur)
        seg = verdict.get("best_segment") or {}
        t_in = min(float(seg.get("in_s") or 0.0), max(0.0, dur - use))
        meta = {**json.loads(a["meta_json"]), "det": det, "in_s": t_in, "use_s": use}
        k.store.set_asset(aid, meta_json=json.dumps(meta, default=str))
        if _usable(verdict) and det["status"] != "FAIL":
            return _done(k, job_id, node_id, aid)
        if det["status"] == "FAIL":
            verdict = {**verdict, "usable": False, "notes": f"{det['detail']}; {verdict.get('notes', '')}"}
        correction = _rejected(k, job_id, node_id, aid, verdict)


def _usable(v) -> bool:
    return bool(v.get("usable")) and v.get("lettering_present") != "yes" and v.get("product_identity_ok") != "no" \
        and v.get("matches_master_plate") != "no" and v.get("matches_previous_plate") != "no" \
        and v.get("required_action_occurred") != "no" and v.get("end_state_reached") != "no" and not v.get("prohibited_present")


def _rejected(k, job_id, node_id, aid, verdict) -> str:
    """A binding "no": record it; retry once with the taster's notes as a correction; after 2 rejected attempts the shot
    goes back to the chef (films) or to the founder (a master plate, plate or character has no shot to re-plan)."""
    k.store.set_asset(aid, status="rejected")
    why = (verdict.get("notes") or "") + ("; differences: " + "; ".join(verdict.get("differences") or []) if verdict.get("differences") else "")
    k.store.event(job_id, "system", "take_rejected", {"node": node_id, "asset": aid, "why": why[:400]})
    cur = k.store.node(job_id, node_id)
    if cur["draws"] < cur["max_draws"]:
        flow.send_back(k.store, job_id, "SB-TASTER-RETRY", key=node_id, why=why)
        return why[:300] or "the previous attempt was rejected by the small taster"
    spec = json.loads(cur["spec_json"])
    if cur["kind"] in ("frame", "shot") and not spec.get("replanned"):
        raise ShotReplan(node_id, spec["shot"], why[:400])
    raise NeedsFounder(node_id, _takes(k, job_id, node_id), f"rejected {cur['draws']} times: {why[:300]}")


def taste(k, job_id, node_id, instruction, a, *, prev=None, video_seconds=8.0) -> dict:
    """The small taster on one output: the customer's words, the instruction, the master plate and the previous plate.
    Unsure → the strong model looks again once. The Ingredient check form is stored on the asset and in the job file."""
    ctx = {"INSTRUCTION": instruction,
           "MEDIA_NOTE": "Images in order: the MASTER plate (if any), the PREVIOUS plate (if any), the customer's product photo, "
                         "then the output to inspect (last)."}
    master = _selected_bytes(k, job_id, "master") if k.store.node(job_id, "master") and k.store.node(job_id, "master")["selected_asset_id"] \
        and node_id != "master" else None
    items = ([master] if master else []) + list(prev or [])[:1] + product_refs(k, job_id, 1) + _media_of(k, a)
    with k.store.timed(job_id, "independent_review", f"small taster {node_id}"):
        v = k.workers.call(job_id, "small_taster", "ingredient_check", ctx, exact_words=k.exact_words(job_id), media=items,
                           video_seconds=video_seconds, sim_args={"node_id": node_id})
        if v.get("unsure"):
            v2 = k.workers.call(job_id, "small_taster", "ingredient_check", ctx, exact_words=k.exact_words(job_id), media=items,
                                model_key="small_taster_escalation", video_seconds=video_seconds, sim_args={"node_id": node_id, "escalated": True})
            v2["escalated_from"] = v.get("llm_call_id")
            v = v2
    k.put_form(job_id, "ingredient_check", v)
    meta = {**json.loads(k.store.asset(a["id"])["meta_json"]), "inspection": {kk: v.get(kk) for kk in (
        "usable", "unsure", "required_action_occurred", "end_state_reached", "product_identity_ok", "matches_master_plate",
        "matches_previous_plate", "differences", "lettering_present", "notes")}, "taster_form_version": len(k.store.artifact_versions(job_id, "ingredient_check")),
            "taster_model": v["written_by"]["model"], "taster_simulated": v["written_by"]["simulated"]}
    k.store.set_asset(a["id"], meta_json=json.dumps(meta, default=str))
    return v


def _media_of(k, a) -> list:
    if (a["content_type"] or "").startswith("image/"):
        return [(a["content_type"], Path(a["path"]).read_bytes())]
    if k.s.models.get("small_taster", "").startswith("gemini") and media.have_ffmpeg():
        return [("video/mp4", Path(a["path"]).read_bytes())]
    if not media.have_ffmpeg():
        return []
    d = _duration(a["path"])
    base = Path(a["path"]).with_suffix("")
    return [("image/png", media.frame_png(a["path"], d * i / 4 + 0.1, Path(f"{base}-f{i}.png")).read_bytes()) for i in range(4)]


def _duration(path) -> float:
    try:
        return media.probe(path)["duration_s"] or 4.0
    except media.MediaError:
        return 4.0


def _selected_bytes(k, job_id, node_id):
    a = k.store.asset(k.store.node(job_id, node_id)["selected_asset_id"])
    return (a["content_type"] or "image/png", Path(a["path"]).read_bytes())


def _prev_bytes(k, job_id, spec):
    if spec.get("previous") and not spec.get("risky") and k.store.node(job_id, spec["previous"]) and \
            k.store.node(job_id, spec["previous"])["selected_asset_id"]:
        e = _end_frame(k, job_id, spec["previous"])
        return [e] if e else []
    return []


def _extract_end_frame(k, job_id, shot_node, for_node) -> Path:
    src = k.store.asset(k.store.node(job_id, shot_node)["selected_asset_id"])
    out = k.store.new_output_path(k.job_dir(job_id) / "gen", f"{for_node}__from-{shot_node}-end", "png")
    meta = json.loads(src["meta_json"])
    t = float(meta.get("in_s", 0.0)) + float(meta.get("use_s", _duration(src["path"]))) - 0.05
    if media.have_ffmpeg() and (src["content_type"] or "").startswith("video/"):
        media.frame_png(src["path"], max(0.0, t), out)
    else:
        out.write_bytes(Path(src["path"]).read_bytes())
    return out


def _end_frame(k, job_id, shot_node):
    n = k.store.node(job_id, shot_node)
    if not n or not n["selected_asset_id"]:
        return None
    tmp = k.job_dir(job_id) / "work"
    tmp.mkdir(parents=True, exist_ok=True)
    p = tmp / f"endframe-{shot_node}-{n['selected_asset_id']}.png"
    if not p.exists():
        src = k.store.asset(n["selected_asset_id"])
        meta = json.loads(src["meta_json"])
        t = float(meta.get("in_s", 0.0)) + float(meta.get("use_s", _duration(src["path"]))) - 0.05
        if media.have_ffmpeg() and (src["content_type"] or "").startswith("video/"):
            media.frame_png(src["path"], max(0.0, t), p)
        else:
            p.write_bytes(Path(src["path"]).read_bytes())
    return ("image/png", p.read_bytes())


def _clip_det(a, use) -> dict:
    if not media.have_ffmpeg():
        return {"check_id": "no_in_model_cut", "status": "NOT_VERIFIED", "detail": "ffmpeg not installed"}
    cuts = [t for t in media.scene_cuts(a["path"]) if 0.15 < t < use]
    return {"check_id": "no_in_model_cut", "status": "FAIL" if cuts else "PASS",
            "detail": f"in-model cut(s) at {cuts} inside the used {use}s" if cuts else f"no cut inside the used {use}s"}


# ── the production log (spec §4.6) ─────────────────────────────────────────────────────────────────────────────────
def write_log(k, job_id):
    nodes = {n["node_id"]: n for n in k.store.nodes(job_id)}
    master = nodes.get("master") or next((n for n in nodes.values() if n["kind"] == "plate" and json.loads(n["spec_json"]).get("master")), None)
    appr = next(iter(k.store.events(job_id, ("master_approved",))[-1:]), None)
    mspec = json.loads(master["spec_json"]) if master else {}
    entries = []
    atts = k.store.attempts(job_id)
    for x, n in nodes.items():
        if n["kind"] not in ("master", "plate", "character", "frame", "shot") or n["status"] == "retired":
            continue
        spec = json.loads(n["spec_json"])
        sel = k.store.asset(n["selected_asset_id"]) if n["selected_asset_id"] else None
        meta = json.loads(sel["meta_json"]) if sel else {}
        if n["kind"] == "shot":
            src_kind, src = "frame", meta.get("from_frame")
        elif n["kind"] == "frame":
            src_kind = spec.get("starts_from") if spec.get("starts_from") == "previous_shot_end" else "master_plate"
            src = meta.get("from_asset") or (nodes["master"]["selected_asset_id"] if "master" in nodes else None)
        else:
            src_kind, src = meta.get("source_kind") or "product photos", None
        entries.append({"node": x, "shot": spec.get("shot"), "route": spec.get("route") or "IMG", "source_image": src, "source_kind": src_kind,
                        "previous_shot": spec.get("previous"),
                        "attempts": [{"attempt": a["id"].split(":")[-1], "status": a["status"]} for a in atts if a["node_id"] == x],
                        "selected": n["selected_asset_id"], "reason": n["note"] or ("taster yes" if n["status"] == "done" else n["status"])})
    log = {"master_plate": {"node": master["node_id"] if master else None, "asset_id": master["selected_asset_id"] if master else None,
                            "approved_by": appr["actor"] if appr else None, "approved_utc": appr["utc"] if appr else None,
                            "reused_from_shelf": mspec.get("shelf_item")}, "entries": entries}
    prev = k.store.artifact(job_id, "production_log")
    if prev is None or {kk: prev.get(kk) for kk in ("master_plate", "entries")} != log:
        k.put_form(job_id, "production_log", log, by="head_cook")
    return log


__all__ = ["plan", "produce", "sample_picture", "approve_master", "founder_select_take", "write_log", "taste", "verify",
           "IdenticalRequestRefused"]
