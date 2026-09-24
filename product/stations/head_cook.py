"""Station — the head cook (kitchen v3, founder-approved 2026-09-25): one cook doing the entire cooking, with three skills.

  - Cooking: the look of the film first (the chef's own look prompt), then every shot with the tool the chef chose — a
    designed still animated by the video model (`video`), a designed still with a slow code move (`still`), the
    customer's real product photo placed in the film's world by code (`photo`), the end card by code — each sent with
    the CHEF'S OWN prompt, as written. The voice-over, when the customer asked for one, is cast and configured by the head
    cook from the chef's voice direction.
  - Tasting: every take is tasted on a model from a different company than the chef's (pictures: head_cook; clips and
    voices, watched and heard: head_cook_av).
  - Repairing: a weak take is retaken with a sharper prompt, re-staged as the same moment another way, or made from the
    real product photo — never frozen into a still to make a problem go away. Takes are bounded by the customer's budget
    and MI_MAX_TAKES per shot (money protection); when they are used up, the best take is kept and the customer is told.
Kept stills are posted to the customer's page as they are made (founder 2026-09-25). The customer approves the recipe
and receives the dish; nothing waits for them in between (the older look / first-shot approvals are off unless
MI_CUSTOMER_TASTES=1).
Every output is written to a new, unique path (write-once); the Production log records sources, attempts and choices.
"""
from __future__ import annotations

import json
import re
import shutil
import time
from pathlib import Path

from product import compose, cost, flow, media, prompts, verify
from product.dispatch import DispatchFailed, GuardRefused, IdenticalRequestRefused
from product.reasoning import ProviderUnavailable
from product.store import BudgetExhausted, utc_now

TRANSIENT_RETRIES = 3
import os
MAX_TAKES = int(os.environ.get("MI_MAX_TAKES", "4"))           # per output: money protection, not a creative rule
CUSTOMER_TASTES = os.environ.get("MI_CUSTOMER_TASTES", "0") == "1"


class Reframed(Exception):
    """The head cook sent a clip back to its first frame: the frame is redrawn and the clip remade from it."""


class KeepFlagged(Exception):
    """Amendment 1 §3: an output the small taster rejected on every allowed attempt, on the safest route there is. The
    latest take is kept, flagged, and noted on the customer's preview — the customer's look is the final check."""
    def __init__(self, node_id, asset_id, why):
        super().__init__(f"{node_id}: kept flagged — {why}")
        self.node_id, self.asset_id, self.why = node_id, asset_id, why


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


def look_has_product(recipe: dict) -> bool:
    """The chef says whether the product is in the look of the film (recipe v3 `look.product_present`; older recipes: yes)."""
    return bool((recipe.get("look") or {}).get("product_present", True))


def product_refs(k, job_id, limit=3) -> list:
    """Reference photos for the generator and the head cook: the ones the chef chose (`reference_photos`, best first);
    otherwise product views first, then details, never lifestyle/people or logo photos, infographics last (EQ-006)."""
    u = k.store.artifact(job_id, "understanding") or {}
    chosen = (k.store.artifact(job_id, "recipe") or {}).get("reference_photos") or []
    by_n = {r.get("photo"): r for r in u.get("photo_roles", [])}
    order = {"product_view": 0, "product_detail": 1, "infographic": 2}
    roles = [by_n[n] for n in chosen if n in by_n] or \
        sorted([r for r in u.get("photo_roles", []) if r["role"] in order], key=lambda r: order[r["role"]])
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
                                meta={"shelf_item": shelf_master["id"], "shelf_version": shelf_master["version"], "master": True, "format": aspect,
                                      "master_plate": recipe.get("master_plate")})
        k.shelf.record_use(job_id, job["account_id"], shelf_master["id"], "master_plate")
        return aid
    refs = product_refs(k, job_id) if (job["media"] == "image" or look_has_product(recipe)) else []
    g = guard(k, job_id, recipe)
    if job["media"] == "image":
        prompt = prompts.still_prompt(recipe, g, aspect=aspect, with_product_ref=bool(refs), with_character_ref=False)
    else:
        prompt = prompts.master_plate_prompt(recipe, g, aspect=aspect, with_product_ref=bool(refs))
    with k.store.timed(job_id, "asset_preparation", "sample picture"):
        aid = k.dispatch.image(job_id, "preview", prompt=prompt, aspect=aspect, refs=refs, guard=g,
                               meta={"format": aspect, "preview": True, "master": job["media"] == "video",
                                     "master_plate": recipe.get("master_plate"), "look": (recipe.get("look") or {}).get("picture_prompt")})
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
            shots = [s for s in recipe["shots"] if s["route"] != "END-CARD"]
            card = next((s for s in recipe["shots"] if s["route"] == "END-CARD"), {"duration_s": 3})
            shelf_master = _shelf_master(k, job_id, recipe)
            want.append(("master", "master", [], {"aspect": aspect, "route": "IMG", "reuse": preview["id"] if preview else None,
                                                  "shelf_item": shelf_master["id"] if shelf_master else None}))
            prev = None
            for s in shots:
                tool = s.get("tool") or ("video" if s["route"] in ("FILM-B", "FILM-C") else "still")
                deps = ["master"] + ([f"shot_{prev}"] if prev else [])
                spec = {"shot": s["n"], "aspect": aspect, "route": s["route"], "tool": tool, "starts_from": "master_plate",
                        "previous": f"shot_{prev}" if prev else None, "fp": _shot_fp(s), "gates": [],
                        "photo_index": s.get("photo_index"), "photo_crop": s.get("photo_crop"), "photo_fill": s.get("photo_fill")}
                want.append((f"frame_{s['n']}", "photo" if tool == "photo" else "frame", list(dict.fromkeys(deps)), spec))
                want.append((f"shot_{s['n']}", "shot", [f"frame_{s['n']}"], dict(spec)))
                if s.get("super_id") and not _logo_copy(k, job_id, recipe, s["super_id"]):
                    want.append((f"super_{s['n']}", "super", [f"shot_{s['n']}"], {"shot": s["n"], "copy_id": s["super_id"], "aspect": aspect}))
                prev = s["n"]
            want.append(("music", "music", [], {}))
            vo = recipe.get("voice_over") or {}
            if vo.get("wanted") and vo.get("lines"):
                want.append(("voice", "voice", [], {"fp": json.dumps(vo, sort_keys=True)[:4000]}))
            want.append(("end_card", "end_card", [], {"aspect": aspect, "duration_s": card["duration_s"]}))
            fin = [f"shot_{s['n']}" for s in shots] + [w[0] for w in want if w[1] == "super"] + ["music", "end_card"] + \
                (["voice"] if any(w[0] == "voice" for w in want) else [])
            want.append(("film", "assemble", fin, {"aspect": aspect, "card_s": card["duration_s"]}))
    keep = []
    for node_id, kind, deps, spec in want:
        old = existing.get(node_id)
        if old and old["status"] == "done" and json.loads(old["spec_json"]).get("fp") == spec.get("fp") and kind not in ("assemble",):
            keep.append(node_id)                 # unchanged work is preserved (a re-plan redoes only what changed)
            k.store.set_node(job_id, node_id, deps_json=json.dumps(deps))
            continue
        k.store.put_node(job_id, node_id, kind=kind, deps=deps, spec=spec, max_draws=MAX_TAKES if kind not in ("assemble",) else 1)
    for node_id in existing:
        if node_id not in [w[0] for w in want]:
            k.store.set_node(job_id, node_id, status="retired", note="not in the current recipe")
    # anything downstream of a changed node is redone
    changed = [w[0] for w in want if w[0] not in keep and w[0] in existing]
    for c in changed:
        _reset_downstream(k, job_id, c)
    k.store.event(job_id, "system", "plan", {"nodes": [w[0] for w in want], "kept": keep})
    write_log(k, job_id)
    k.store.transition(job_id, "planning", "producing", actor="system")


def _shot_fp(s: dict) -> str:
    from product.store import sha256_json
    return sha256_json({kk: s.get(kk) for kk in ("tool", "picture_prompt", "motion_prompt", "photo_index", "photo_crop", "photo_fill", "duration_s", "route",
                                                 "action", "first_frame")})[:16]


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
        spec["repair_round"] = int(spec.get("repair_round") or 0) + 1      # redraws after a reset are repairs, not retakes
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
        ready = [x for x, n in nodes.items() if n["status"] == "pending"
                 and all(nodes[d]["status"] == "done" for d in json.loads(n["deps_json"]) + json.loads(n["spec_json"]).get("gates", [])
                         if d in nodes)]
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
        except Reframed:
            continue
        except KeepFlagged as e:
            _keep_flagged(k, job_id, x, e.asset_id, e.why)
        except IdenticalRequestRefused as e:
            takes = _takes(k, job_id, x)
            answered = [a["id"] for a in k.store.assets(job_id, node_id=x) if a["status"] == "selected"]
            if not takes and answered:
                # a node reset by a repair upstream sends a request already answered (its inputs did not change): the
                # earlier answer, which the head cook already kept, is used again — never a failed step
                k.store.event(job_id, "head_cook", "identical_answer_reused", {"node": x, "asset": answered[-1]})
                _done(k, job_id, x, answered[-1])
            elif not takes:
                raise _node_failed(f"{x}: {e}")
            else:
                # the customer is told what the head cook found wrong, never the dispatcher's refusal (it names our models)
                last = [json.loads(v["data_json"]) for v in k.store.events(job_id, ("take_rejected",))]
                last = [d for d in last if d.get("node") == x]
                _keep_flagged(k, job_id, x, takes[-1], f"rejected {len(last)} times: "
                              + ((last[-1].get("why") if last else "") or "our last takes were not right"))
        if x == "master" and _master_needs_approval(k, job_id):
            write_log(k, job_id)
            k.store.transition(job_id, "producing", "awaiting_master_approval", actor="system",
                               data={"master": k.store.node(job_id, "master")["selected_asset_id"]})
            k.store.timing_start(job_id, "customer_wait", "master")
            return
        if _taste_ready(k, job_id):
            write_log(k, job_id)
            k.store.transition(job_id, "producing", "awaiting_taste", actor="system", data={"taste": taste_nodes(k, job_id)})
            k.store.timing_start(job_id, "customer_wait", "taste")
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


def _keep_flagged(k, job_id, node_id, asset_id, why):
    k.store.set_asset(asset_id, status="candidate")
    _done(k, job_id, node_id, asset_id)
    spec = json.loads(k.store.node(job_id, node_id)["spec_json"])
    k.store.set_node(job_id, node_id, spec_json=json.dumps({**spec, "flagged": why[:300]}))
    k.store.event(job_id, "system", "take_kept_flagged", {"node": node_id, "asset": asset_id, "why": why[:300]})
    from product.stations.chef import add_customer_note
    what = f"shot {spec['shot']}" if spec.get("shot") else {"master": "the look of the film (master plate)", "character": "the character"}.get(
        node_id, node_id.replace("_", " "))
    reason = re.sub(r"^rejected \d+ times:\s*", "", why).split("; differences:")[0].strip()
    add_customer_note(k, job_id, f"Please look closely at {what}: we weren't fully happy with it"
                                 + (f" ({reason[:160]})" if reason else "") + ", so we kept our best version for you to judge.")


def _replace_shot_nodes(k, job_id, shot_n, recipe):
    s = next(s for s in recipe["shots"] if s["n"] == shot_n)
    for x in (f"frame_{shot_n}", f"shot_{shot_n}"):
        n = k.store.node(job_id, x)
        spec = json.loads(n["spec_json"])
        spec.update(route=s["route"], starts_from=s["starts_from"], fp=_shot_fp(s), replanned=True)
        k.store.set_node(job_id, x, spec_json=json.dumps(spec))
    _reset_downstream(k, job_id, f"frame_{shot_n}")


def _master_needs_approval(k, job_id) -> bool:
    if not CUSTOMER_TASTES:
        return False                    # kitchen v3: the customer approved the recipe and its look; they receive the dish
    if k.store.job(job_id)["media"] != "video":
        return False
    n = k.store.node(job_id, "master")
    if n["status"] != "done":
        return False
    if json.loads(n["spec_json"]).get("shelf_item"):
        return False                               # already approved by the customer on their shelf
    return not k.store.events(job_id, ("master_approved",))


# ── the taste (founder 2026-09-23): the hardest shot is made first and shown to the customer before the rest ────────
def taste_nodes(k, job_id) -> list:
    """The shots the customer tastes: the risky ones (made first anyway), else the first moving shot. Stills-only films
    have no taste — the approved look already shows what they will get."""
    if k.store.job(job_id)["media"] != "video":
        return []
    shots = [n for n in k.store.nodes(job_id) if n["kind"] == "shot" and n["status"] != "retired"]
    risky = [n["node_id"] for n in shots if json.loads(n["spec_json"]).get("risky")]
    if risky:
        return sorted(risky)
    moving = sorted((json.loads(n["spec_json"]).get("shot") or 0, n["node_id"]) for n in shots
                    if json.loads(n["spec_json"]).get("route") in ("FILM-B", "FILM-C"))
    return [moving[0][1]] if moving else []


def _taste_ready(k, job_id) -> bool:
    if not CUSTOMER_TASTES:
        return False
    if k.store.events(job_id, ("taste_approved",)):
        return False
    nodes = taste_nodes(k, job_id)
    return bool(nodes) and all(k.store.node(job_id, x)["status"] == "done" for x in nodes)


def approve_taste(k, job_id, *, by: str):
    if k.store.job(job_id)["state"] != "awaiting_taste":
        raise ValueError("there is no shot waiting for your taste")
    k.store.event(job_id, by, "taste_approved", {"shots": taste_nodes(k, job_id)})
    k._end_wait(job_id, "taste")
    k.store.transition(job_id, "awaiting_taste", "producing", actor=by, data={"taste_approved": True})


def change_taste(k, job_id, *, by: str, text: str):
    """The customer asks for a change to the tasted shot(s): only those are redone (within the approved budget), then
    they taste again."""
    if k.store.job(job_id)["state"] != "awaiting_taste":
        raise ValueError("there is no shot waiting for your taste")
    text = (text or "").strip()
    if len(text) < 3:
        raise ValueError("tell us what to change")
    k.store.add_feedback(job_id, asset_id=None, target="taste", text=text[:2000], kind="taste", by_user=by)
    for x in taste_nodes(k, job_id):
        _reset_downstream(k, job_id, x, f"the customer asked: {text[:300]}")
    k.store.event(job_id, by, "taste_change", {"text": text[:300]})
    k._end_wait(job_id, "taste")
    k.store.transition(job_id, "awaiting_taste", "producing", actor=by, data={"taste_change": text[:300]})


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
    if kind == "photo":
        return _node_photo(k, job_id, n, spec, ctx)
    if kind == "voice":
        return _node_voice(k, job_id, n, spec, ctx)
    if kind == "shot":
        return _node_shot(k, job_id, n, spec, ctx)
    if kind == "music":
        p, neg = prompts.music_prompt(ctx["recipe"], ctx["guard"])
        if (ctx["recipe"].get("sound") or {}).get("music_prompt"):          # kitchen v3: the chef's own music brief
            p = prompts._strip(ctx["recipe"]["sound"]["music_prompt"], ctx["guard"]["forbidden_words"]) + \
                " Instrumental only, no vocals, no singing, no spoken words."
        aid = _draw(k, job_id, node_id, lambda: k.dispatch.music(job_id, node_id, prompt=p, negative=neg, guard=ctx["guard"]))
        return _done(k, job_id, node_id, aid)
    with k.store.timed(job_id, "composition", node_id):
        from product.stations import assembly
        return getattr(assembly, kind)(k, job_id, n, spec, ctx)


def _done(k, job_id, node_id, asset_id):
    if asset_id:
        k.store.set_asset(asset_id, status="selected")
    k.store.set_node(job_id, node_id, status="done", selected_asset_id=asset_id)
    n = k.store.node(job_id, node_id)
    if n:                                   # the customer's progress line (customer.py): what was finished, in plain words
        from product import customer
        shots = len([s for s in (k.store.artifact(job_id, "recipe") or {}).get("shots", []) if s.get("route") != "END-CARD"])
        spec = json.loads(n["spec_json"])
        words = customer.node_words(n["kind"], spec, shots)
        a = k.store.asset(asset_id) if asset_id else None
        still = a and (a["content_type"] or "").startswith("image/") and n["kind"] in ("master", "frame", "photo") \
            and not spec.get("flagged") and k.store.job(job_id)["media"] == "video"
        if still:                           # founder 2026-09-25: show the customer the stills as they are made
            words = words or ("The look of your film" if n["kind"] == "master" else f"Shot {spec.get('shot')}: how it is looking")
        if words:
            customer.tell(k.store, job_id, words, asset=asset_id if still else None)


def _draw(k, job_id, node_id, fn):
    """One paid draw. Quality draws are capped by the node's max_draws (2 attempts per output); transient provider failures
    do not use them up (they pause the job as paused_provider after TRANSIENT_RETRIES)."""
    transient = 0
    while True:
        cur = k.store.node(job_id, node_id)
        if cur["draws"] >= cur["max_draws"]:
            takes = _takes(k, job_id, node_id)
            if takes:                   # takes exist (rejected ones): the best is kept, flagged, and the customer is told
                last = [json.loads(v["data_json"]) for v in k.store.events(job_id, ("take_rejected",))]
                last = [d for d in last if d.get("node") == node_id]
                raise KeepFlagged(node_id, takes[-1], f"rejected {len(last)} times: "
                                  + ((last[-1].get("why") if last else "") or "our takes were not right"))
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
    if spec.get("edit_from") and k.store.asset(spec["edit_from"]):
        # the head cook's `edit` repair: most of the take is right, so the picture model edits it instead of redrawing it
        take = k.store.asset(spec["edit_from"])
        if (kind == "master" and not look_has_product(recipe)) or (kind == "frame" and not ctx["shots"][spec["shot"]].get("product_present")):
            refs = []
        text = ("Edit the first image. Keep everything in it exactly as it is (the person, face, age, clothes, pose, room, "
                "light, colours and framing) and change only this: " + spec.get("edit_instruction", "") +
                (" The product must match the product reference photos (the images after the first) exactly." if refs else ""))
        p = prompts.chef_picture_prompt(text, g, aspect=aspect)
        return p, [(take["content_type"] or "image/png", Path(take["path"]).read_bytes())] + list(refs), \
            {"asset": f"{n['node_id']} — an edit of the previous take", "prompt": p, "edit_instruction": spec.get("edit_instruction")}, \
            f"edit of {take['id']}"
    if kind == "master":
        has = look_has_product(recipe)
        refs = refs if has else []
        p = prompts.master_plate_prompt(recipe, g, aspect=aspect, with_product_ref=bool(refs))
        if spec.get("prompt_override"):
            p = prompts.chef_picture_prompt(spec["prompt_override"], g, aspect=aspect,
                                            refs_note="The product must match the product reference photos exactly." if refs else "")
        return p, refs, {"asset": "master plate — the film's one world", "prompt": p, "product_present": has}, \
            "product photos" if refs else "the chef's look prompt"
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
    # a shot's first frame: the chef's own picture prompt (or the head cook's sharper one after a weak take), as written
    s = ctx["shots"][spec["shot"]]
    m = _selected_bytes(k, job_id, "master")
    prev_end = _end_frame(k, job_id, spec["previous"]) if spec.get("previous") else None
    use = [m] + ([prev_end] if prev_end else []) + (list(refs) if s.get("product_present") else [])
    text = spec.get("prompt_override") or s.get("picture_prompt") or s.get("first_frame", "")
    if spec.get("revision_note"):
        text += f" Change requested: {spec['revision_note']}."
    p = prompts.chef_picture_prompt(text, g, aspect=aspect, refs_note=prompts.REFS_NOTE)
    return p, use, {"asset": f"first frame of shot {s['n']} — {s.get('title', '')}", "prompt": p,
                    "chef_description": s.get("description"), "feeling": s.get("feeling"),
                    "product_present": s.get("product_present")}, \
        "look of the film" + (f" + end frame of {spec['previous']}" if prev_end else "")


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
        n = k.store.node(job_id, node_id)
        spec = json.loads(n["spec_json"])                 # a repair may have sharpened the prompt
        if n["kind"] == "photo":                          # ... or switched the shot to the real product photo
            return _node_photo(k, job_id, n, spec, ctx)
        prompt, refs, instruction, source = _image_request(k, job_id, n, spec, ctx, correction)
        if aid is None:
            aid = _draw(k, job_id, node_id, lambda: k.dispatch.image(job_id, node_id, prompt=prompt, aspect=spec["aspect"], refs=refs,
                                                                   guard=ctx["guard"], is_repair=bool(spec.get("repair_round")), meta={"format": spec["aspect"], "shot": spec.get("shot"),
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
    # a clip paid for before a worker died and recovered by a resumed poll (dispatch.recover) is tasted and used — never re-bought
    recovered = [x["id"] for x in k.store.assets(job_id, node_id=node_id, status="candidate") if json.loads(x["meta_json"]).get("recovered")]
    while True:
        spec = json.loads(k.store.node(job_id, node_id)["spec_json"])
        motion = spec.get("motion_override") or s.get("motion_prompt") or s.get("action", "")
        prompt = prompts.chef_motion_prompt(motion, ctx["guard"]) + \
            (f" Change requested: {spec['revision_note']}." if spec.get("revision_note") else "")
        negative = prompts.clip_negative(ctx["recipe"], ctx["guard"], s, [])
        if recovered:
            aid = recovered.pop(0)
            k.store.event(job_id, "system", "recovered_take_used", {"node": node_id, "asset": aid})
        else:
            aid = None
        try:
            aid = aid or _draw(k, job_id, node_id, lambda: k.dispatch.video(job_id, node_id, prompt=prompt, image=(frame["content_type"] or "image/png",
                                                                                                           Path(frame["path"]).read_bytes()),
                                                                     duration_s=dur, aspect=spec["aspect"], negative=negative, guard=ctx["guard"],
                                                                     is_repair=bool(spec.get("repair_round")), meta={"shot": s["n"], "route": spec["route"], "from_frame": frame["id"]}))
        except DispatchFailed as e:
            # live 2026-09-25: the video model's AUDIO safety filter refused the clip even with its sound switched off. The
            # sounds the prompt describes are what it objects to; the film's sound comes from the music bed and ambience
            # anyway, so the next attempt keeps every picture instruction and leaves out the sentences about sound.
            if e.failure_class == "provider_refusal" and "audio" in str(e).lower() and not spec.get("sound_left_out"):
                quiet = _without_sound(motion)
                k.store.set_node(job_id, node_id, spec_json=json.dumps({**spec, "motion_override": quiet, "sound_left_out": True}))
                k.store.event(job_id, "head_cook", "head_cook_repair", {"node": node_id, "repair": "sound_left_out", "better_prompt": quiet[:1500]})
                continue
            raise
        a = k.store.asset(aid)
        det = _clip_det(a, use)
        instruction = {"asset": f"clip for shot {s['n']} — {s.get('title', '')} ({dur}s; {use}s used)", "motion_prompt": motion,
                       "chef_description": s.get("description"), "feeling": s.get("feeling"), "product_present": s.get("product_present")}
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


_SOUND = re.compile(r"\b(sound\w*|chime\w*|click\w*|music\w*|audio|hum\w*|ring\w*|tap\w*|clink\w*|whisper\w*|voice\w*|"
                    r"noise\w*|song|sing\w*|speak\w*|talk\w*|say\w*|laugh\w*|mouths?)\b", re.I)


def _without_sound(text: str) -> str:
    """The motion prompt with its sentences about sound left out (the picture instructions stay)."""
    keep = [x for x in re.split(r"(?<=[.;!?])\s+", text or "") if x and not _SOUND.search(x)]
    return " ".join(keep) or text


def _usable(v) -> bool:
    return bool(v.get("usable")) and v.get("lettering_present") != "yes" and v.get("product_identity_ok") != "no" \
        and v.get("matches_master_plate") != "no" and v.get("matches_previous_plate") != "no" \
        and v.get("required_action_occurred") != "no" and v.get("end_state_reached") != "no" and not v.get("prohibited_present")


def _rejected(k, job_id, node_id, aid, verdict) -> str:
    """The head cook's repair skill (kitchen v3). The take is not served; what happens next is the head cook's decision,
    written on its tasting form: retake with a sharper prompt, re-stage the same moment another way, or use the real
    product photo. Never a still in place of a moving moment. When MI_MAX_TAKES is used (money protection) or the moment
    truly cannot be made, the best take is kept and the customer is told."""
    k.store.set_asset(aid, status="rejected")
    why = (verdict.get("notes") or "") + ("; differences: " + "; ".join(verdict.get("differences") or []) if verdict.get("differences") else "")
    cur = k.store.node(job_id, node_id)
    cspec = json.loads(cur["spec_json"])
    repair = verdict.get("repair") or "retake"
    better = (verdict.get("better_prompt") or "").strip()
    # the shot's action class at the time of the rejection: the diary writer turns repeated rejections into equipment lessons
    shot = next((s for s in (k.store.artifact(job_id, "recipe") or {}).get("shots", []) if s["n"] == cspec.get("shot")), None)
    k.store.event(job_id, "head_cook", "take_rejected", {"node": node_id, "asset": aid, "why": why[:400], "repair": repair,
                                                         "tool": cspec.get("tool"), "route": cspec.get("route"),
                                                         "action_class": shot.get("action_class") if shot else None})
    image_kind = cur["kind"] in ("master", "frame", "plate", "character")
    if image_kind and (repair == "edit" or (repair == "use_photo" and cur["kind"] != "frame")) and better:
        # most of the picture is right: edit this take (the person and the room stay; only what was wrong changes)
        k.store.set_node(job_id, node_id, spec_json=json.dumps({**cspec, "edit_from": aid, "edit_instruction": better}))
        k.store.event(job_id, "head_cook", "head_cook_repair", {"node": node_id, "repair": "edit", "better_prompt": better[:1500]})
        if cur["draws"] >= cur["max_draws"]:
            raise KeepFlagged(node_id, aid, f"rejected {cur['draws']} times: {why[:300]}")
        return why[:300]
    cspec.pop("edit_from", None)
    reframe = (verdict.get("better_picture_prompt") or "").strip()
    if cur["kind"] == "shot" and reframe and int(cspec.get("reframes") or 0) < 1 and k.store.node(job_id, f"frame_{cspec['shot']}"):
        # the clip failed because of its first frame: redraw the frame (once per shot — money protection), then remake the clip
        shot = cspec["shot"]
        fx = f"frame_{shot}"
        fspec = json.loads(k.store.node(job_id, fx)["spec_json"])
        for kk in ("edit_from", "edit_instruction", "flagged", "reuse"):
            fspec.pop(kk, None)
        k.store.set_node(job_id, fx, spec_json=json.dumps({**fspec, "prompt_override": reframe}))
        k.store.set_node(job_id, node_id, spec_json=json.dumps({**cspec, "reframes": int(cspec.get("reframes") or 0) + 1,
                                                                **({"motion_override": better} if better else {})}))
        _reset_downstream(k, job_id, fx)
        k.store.event(job_id, "head_cook", "head_cook_repair", {"node": node_id, "repair": "reframe", "better_prompt": reframe[:1500]})
        raise Reframed(node_id)
    if repair == "use_photo" and cur["kind"] in ("frame", "shot") and product_refs(k, job_id, 1):
        shot = cspec["shot"]
        for x in (f"frame_{shot}", f"shot_{shot}"):
            sp = json.loads(k.store.node(job_id, x)["spec_json"])
            # the first frame becomes the real photo; the shot keeps the chef's tool and route, so a moving moment still
            # moves (the video model animates the real photo) — never a still in its place
            sp.update(switched_to_photo=why[:200], **({"tool": "photo"} if x.startswith("frame_") else {}))
            k.store.set_node(job_id, x, spec_json=json.dumps(sp), **({"kind": "photo"} if x.startswith("frame_") else {}))
        if cur["kind"] == "shot":
            _reset_downstream(k, job_id, f"frame_{shot}", "the real product photo is used for this shot")
        from product.stations.chef import add_customer_note
        add_customer_note(k, job_id, f"Shot {shot}: our picture model could not draw your product exactly, so we used your "
                                     f"real product photo for it.")
        k.store.event(job_id, "head_cook", "switched_to_photo", {"shot": shot, "why": why[:300]})
        return why[:300]
    if repair == "tell_customer" or cur["draws"] >= cur["max_draws"]:
        raise KeepFlagged(node_id, aid, f"rejected {cur['draws']} times: {why[:300]}")
    if better:
        key = "motion_override" if cur["kind"] == "shot" else "prompt_override"
        k.store.set_node(job_id, node_id, spec_json=json.dumps({**cspec, key: better}))
    k.store.event(job_id, "head_cook", "head_cook_repair", {"node": node_id, "repair": repair, "better_prompt": better[:1500]})
    return why[:300] or "the previous take was not the shot"


def taste(k, job_id, node_id, instruction, a, *, prev=None, video_seconds=8.0) -> dict:
    """The head cook tastes one take (kitchen v3) on a model from a different company than the chef's: pictures on
    `head_cook`, clips (watched with their sound) on `head_cook_av`."""
    recipe = k.store.artifact(job_id, "recipe") or {}
    here = instruction.get("product_present", True) is not False
    product = (recipe.get("identity_anchors") or {}).get("product") if here else None
    ctx = {"INSTRUCTION": {**instruction, **({"product_description": product} if product else {})},
           "MEDIA_NOTE": "Images in order: the look of the film (if any), the previous shot's frame (if any), the customer's "
                         "product photos, then the take to taste (last)."}
    master = _selected_bytes(k, job_id, "master") if k.store.node(job_id, "master") and k.store.node(job_id, "master")["selected_asset_id"] \
        and node_id != "master" else None
    refs = ([master] if master else []) + list(prev or [])[:1] + (product_refs(k, job_id) if here else [])
    is_clip = not (a["content_type"] or "").startswith("image/")
    key = "head_cook_av" if is_clip else "head_cook"
    items = refs + _media_of(k, a, key)
    with k.store.timed(job_id, "independent_review", f"head cook tastes {node_id}"):
        v = k.workers.call(job_id, "head_cook", "ingredient_check", ctx, exact_words=k.exact_words(job_id), media=items,
                           model_key=key, video_seconds=video_seconds, sim_args={"node_id": node_id})
    k.put_form(job_id, "ingredient_check", v)
    meta = {**json.loads(k.store.asset(a["id"])["meta_json"]), "inspection": {kk: v.get(kk) for kk in (
        "usable", "unsure", "required_action_occurred", "end_state_reached", "product_identity_ok", "matches_master_plate",
        "matches_previous_plate", "differences", "lettering_present", "notes")}, "taster_form_version": len(k.store.artifact_versions(job_id, "ingredient_check")),
            "taster_model": v["written_by"]["model"], "taster_simulated": v["written_by"]["simulated"]}
    k.store.set_asset(a["id"], meta_json=json.dumps(meta, default=str))
    return v


def _media_of(k, a, key: str = "head_cook") -> list:
    if (a["content_type"] or "").startswith("image/"):
        return [(a["content_type"], Path(a["path"]).read_bytes())]
    if k.s.models.get(key, "").startswith("gemini") and media.have_ffmpeg():
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


__all__ = ["plan", "produce", "sample_picture", "approve_master", "write_log", "taste", "verify",
           "IdenticalRequestRefused"]


# ── kitchen v3: the real product photo, placed by code in the film's world ────────────────────────────────────────────
def _photo_asset(k, job_id, index):
    u = k.store.artifact(job_id, "understanding") or {}
    roles = u.get("photo_roles") or []
    if index and 1 <= int(index) <= len(roles):
        a = k.store.asset(roles[int(index) - 1]["asset_id"])
        if a:
            return a
    order = {"product_view": 0, "product_detail": 1}
    best = sorted([r for r in roles if r["role"] in order], key=lambda r: order[r["role"]])
    return k.store.asset(best[0]["asset_id"]) if best else None


def _fit_full_frame(ph, W, H):
    """The photo fills the frame: scaled to cover, centred; where the photo is too short or narrow for the frame's shape,
    the rest is filled with the photo's own edge colour (a screen's page colour), never stretched."""
    from PIL import Image
    s = min(W / ph.width, H / ph.height)
    if ph.width * s < W * 0.8 or ph.height * s < H * 0.8:        # far from the frame's shape: keep it whole on its own colour
        edge = ph.crop((0, 0, ph.width, 2)).resize((1, 1), Image.BOX).getpixel((0, 0))
        canvas = Image.new("RGB", (W, H), edge)
        s = min(W * 0.9 / ph.width, H * 0.9 / ph.height)
        p2 = ph.resize((round(ph.width * s), round(ph.height * s)), Image.LANCZOS)
        canvas.paste(p2, ((W - p2.width) // 2, (H - p2.height) // 2))
        return canvas
    s = max(W / ph.width, H / ph.height)
    p2 = ph.resize((round(ph.width * s), round(ph.height * s)), Image.LANCZOS)
    x, y = (p2.width - W) // 2, (p2.height - H) // 2
    return p2.crop((x, y, x + W, y + H))


def _node_photo(k, job_id, n, spec, ctx):
    """The customer's own product photo, cut out from its studio background and placed over the film's world (the look of
    the film, softened), with a soft shadow. Code only; the product is exactly the real product."""
    from PIL import Image, ImageChops, ImageDraw, ImageFilter
    node_id = n["node_id"]
    src = _photo_asset(k, job_id, spec.get("photo_index"))
    if src is None:
        raise _node_failed(f"{node_id}: the chef chose the real product photo but no product photo was supplied")
    W, H = media.FORMAT_PX.get(spec["aspect"], (1080, 1920))
    master = k.store.node(job_id, "master")
    if master and master["selected_asset_id"]:
        bg = Image.open(k.store.asset(master["selected_asset_id"])["path"]).convert("RGB")
    else:
        bg = Image.new("RGB", (W, H), (236, 229, 218))
    s = max(W / bg.width, H / bg.height)
    bg = bg.resize((round(bg.width * s), round(bg.height * s))).crop((0, 0, W, H))
    bg = bg.resize((W // 10, H // 10)).filter(ImageFilter.GaussianBlur(5)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(20))
    bg = Image.blend(bg, Image.new("RGB", (W, H), (38, 26, 16)), 0.25)
    ph = Image.open(src["path"]).convert("RGB")
    crop = spec.get("photo_crop")
    if crop and len(crop) == 4:
        l, t_, r, b = [min(1.0, max(0.0, float(v))) for v in crop]
        if r - l > 0.05 and b - t_ > 0.05:
            ph = ph.crop((round(l * ph.width), round(t_ * ph.height), round(r * ph.width), round(b * ph.height)))
    how = spec.get("photo_fill")
    if how == "full_frame":
        out = k.store.new_output_path(k.job_dir(job_id) / "gen", f"{node_id}__product-photo", "png")
        _fit_full_frame(ph, W, H).save(out)
        aid = k.store.add_asset(job_id, path=out, kind="image", source="composed", content_type="image/png", node_id=node_id,
                                meta={"source_kind": "customer product photo", "from": src["id"], "fill": "full_frame",
                                      "crop": crop, "shot": spec.get("shot")})
        return _done(k, job_id, node_id, aid)
    fill = ph.convert("L").point(lambda v: 255 if v > 244 else 0)
    for c in [(0, 0), (ph.width - 1, 0), (0, ph.height - 1), (ph.width - 1, ph.height - 1)]:
        if fill.getpixel(c) == 255:
            ImageDraw.floodfill(fill, c, 128)
    bgmask = fill.point(lambda v: 255 if v == 128 else 0)
    cut_out = how != "card" and sum(bgmask.histogram()[255:]) > 0.05 * ph.width * ph.height
    alpha = ImageChops.invert(bgmask).filter(ImageFilter.GaussianBlur(1.2)) if cut_out else Image.new("L", ph.size, 255)
    if cut_out and alpha.getbbox():
        bb = alpha.getbbox(); ph, alpha = ph.crop(bb), alpha.crop(bb)
    zone = ((ctx["recipe"].get("look") or {}).get("text_zone") or "top")
    th = int(H * (0.56 if cut_out else 0.72)); tw = int(ph.width * th / ph.height)
    if tw > W * 0.86:
        tw = int(W * 0.86); th = int(ph.height * tw / ph.width)
    if not cut_out:                                   # a whole photo or screen sits in the middle of the frame
        zone = "none"
    ph, alpha = ph.resize((tw, th), Image.LANCZOS), alpha.resize((tw, th), Image.LANCZOS)
    x = (W - tw) // 2
    y = int(H * 0.34) if zone == "top" else (int(H * 0.10) if zone == "bottom" else (H - th) // 2)
    sh = Image.new("L", (W, H), 0)
    ImageDraw.Draw(sh).rounded_rectangle([x + 14, y + 26, x + tw + 14, y + th + 26], 50 if cut_out else 18, fill=150)
    if not cut_out:                                   # a card: rounded corners, the photo whole
        alpha = Image.new("L", (tw, th), 0)
        ImageDraw.Draw(alpha).rounded_rectangle([0, 0, tw - 1, th - 1], max(6, tw // 90), fill=255)
    bg = Image.composite(Image.new("RGB", (W, H), (15, 10, 6)), bg, sh.filter(ImageFilter.GaussianBlur(30)))
    bg.paste(ph, (x, y), alpha)
    out = k.store.new_output_path(k.job_dir(job_id) / "gen", f"{node_id}__product-photo", "png")
    bg.save(out)
    aid = k.store.add_asset(job_id, path=out, kind="image", source="composed", content_type="image/png", node_id=node_id,
                            meta={"source_kind": "customer product photo", "from": src["id"], "cut_out": cut_out, "shot": spec.get("shot")})
    return _done(k, job_id, node_id, aid)


# ── kitchen v3: the voice-over, cast and configured by the head cook, tasted by ear ───────────────────────────────────
def _node_voice(k, job_id, n, spec, ctx):
    node_id = n["node_id"]
    recipe = ctx["recipe"]
    vo = recipe.get("voice_over") or {}
    starts, t = {}, 0.0
    for s in recipe["shots"]:
        starts[s["n"]] = t
        t += float(s["duration_s"])
    total = t
    notes, last_vid = "", None
    while True:
        cur = k.store.node(job_id, node_id)
        if cur["draws"] >= cur["max_draws"]:
            if last_vid:            # like a picture: the last voice take is kept, flagged, and the customer is told
                raise KeepFlagged(node_id, last_vid, f"voice rejected {cur['draws']} times: {notes[:300]}")
            raise _node_failed(f"{node_id}: {cur['max_draws']} voice takes used; last note: {notes[:200]}")
        board = [{"shot": s["n"], "title": s.get("title"), "starts_s": round(starts[s["n"]], 2), "duration_s": s["duration_s"]}
                 for s in recipe["shots"]]
        with k.store.timed(job_id, "voice_cast", node_id):
            cast = k.workers.call(job_id, "head_cook", "voice_cast", {"VOICE_OVER": {**vo, "board": board, "last_take_note": notes or None}},
                                  exact_words=k.exact_words(job_id), sim_args={"node_id": node_id})
        k.put_form(job_id, "voice_cast", cast)
        parts = []
        for ln in cast["lines"]:
            text = ln["text"]
            aid = _draw(k, job_id, node_id, lambda: k.dispatch.speech(job_id, node_id, provider=cast["provider"], text=text, voice=cast["voice"],
                                                                       language_code=cast["language_code"], settings=cast["settings"],
                                                                       ssml=ln.get("ssml") or ""))
            k.store.set_node(job_id, node_id, draws=k.store.node(job_id, node_id)["draws"] - 1)   # a take is the whole voice, not a line
            parts.append((starts.get(int(ln["shot"]), 0.0) + 0.25, k.store.asset(aid)["path"]))
        k.store.set_node(job_id, node_id, draws=k.store.node(job_id, node_id)["draws"] + 1)
        out = k.store.new_output_path(k.job_dir(job_id) / "gen", f"{node_id}__voice-track", "wav")
        _voice_track(parts, total, out)
        vid = k.store.add_asset(job_id, path=out, kind="audio", source="composed", content_type="audio/wav", node_id=node_id,
                                meta={"provider": cast["provider"], "voice": cast["voice"], "settings": cast["settings"], "why": cast.get("why")})
        a = k.store.asset(vid)
        instruction = {"asset": "the voice-over track for the whole film", "direction": vo.get("direction"), "language": vo.get("language"),
                       "lines": [ln["text"] for ln in cast["lines"]],
                       "listen_for": "does it sound like the direction — a real person, warm, natural pace, right accent — or flat and robotic?"}
        v = k.workers.call(job_id, "head_cook", "ingredient_check", {"INSTRUCTION": instruction, "MEDIA_NOTE": "The voice-over track."},
                           exact_words=k.exact_words(job_id), media=[("audio/wav", Path(a["path"]).read_bytes())] if media.have_ffmpeg() else [],
                           model_key="head_cook_av", video_seconds=total, sim_args={"node_id": node_id})
        k.put_form(job_id, "ingredient_check", v)
        if v.get("usable"):
            return _done(k, job_id, node_id, vid)
        notes = (v.get("notes") or "") + (f" Try: {v['better_prompt']}" if v.get("better_prompt") else "")
        k.store.set_asset(vid, status="rejected")
        last_vid = vid
        k.store.event(job_id, "head_cook", "take_rejected", {"node": node_id, "asset": vid, "why": notes[:400], "repair": v.get("repair")})


def _voice_track(parts, total, out):
    """Place each recorded line at its start time on one track the length of the film."""
    if not media.have_ffmpeg():
        shutil.copyfile(parts[0][1], out)
        return out
    inputs, f = [], []
    for i, (t0, p) in enumerate(parts):
        inputs += ["-i", str(p)]
        ms = int(t0 * 1000)
        f.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=mono,adelay={ms}|{ms}[l{i}]")
    f.append("".join(f"[l{i}]" for i in range(len(parts))) + f"amix=inputs={len(parts)}:duration=longest:normalize=0,"
             f"apad=whole_dur={total:.3f},atrim=0:{total:.3f}[v]")
    media.run(["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-filter_complex", ";".join(f), "-map", "[v]", "-ar", "48000",
               "-ac", "1", "-c:a", "pcm_s16le", str(out)])
    return out
