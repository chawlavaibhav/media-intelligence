"""Stations 9 and 10 — the big taster (strong AI from another company) and the door guard (code) (spec §3, §4.8, §4.10,
§5, §6.2, §6.4).

    finished cut → measuring tools (deterministic checks on the exact file) → big taster (Final review form)
      pass → door guard: every required check PASS (or waived by the founder) → the customer's preview
              (while `hold_before_preview` is on, or anything blocks, the cut waits in operator_hold for the founder)
      fix  → the head cook redoes ONLY the named shots (2 rounds)
      fail with earliest_stage plan → the chef re-plans (1 round) → recipe check → the plan goes back to the customer
      2 failed rounds → the founder decides
While the big taster is unqualified its "pass" counts only as "the founder confirms" (its rows are NOT_VERIFIED until the
founder records a confirmation); its "no" still blocks.
"""
from __future__ import annotations

import json
from pathlib import Path

from product import flow, media, verify
from product.store import utc_now


def required(k, job_id) -> dict:
    u = k.store.artifact(job_id, "understanding")
    recipe = k.store.artifact(job_id, "recipe")
    media_kind = u["deliverable"]["media"]
    supers = [f"s{s['n']}" for s in recipe.get("shots", []) if s.get("super_id") and k.store.node(job_id, f"super_{s['n']}")
              and k.store.node(job_id, f"super_{s['n']}")["status"] == "done"]
    req = verify.required_checks(media_kind, mandatory_ids=[m["id"] for m in u.get("mandatory", [])], has_copy=bool(recipe.get("copy_deck")),
                                 has_logo=bool(k.logo(job_id)), super_ids=supers,
                                 has_character=bool((recipe.get("character") or {}).get("present")))
    if not k.qualified("small_taster"):
        req["small_taster_confirmed"] = "QA_COVERAGE_ENFORCEMENT"
    return req


def check_cut(k, job_id: str):
    u = k.store.artifact(job_id, "understanding")
    recipe = k.store.artifact(job_id, "recipe")
    media_kind = u["deliverable"]["media"]
    finals = k.final_assets(job_id)
    logo = k.logo(job_id)
    with k.store.timed(job_id, "deterministic_verification"):
        for aid in finals:
            a = k.store.asset(aid)
            meta = json.loads(a["meta_json"])
            rows = [verify.ledger_integrity(k.store, job_id),
                    verify.exact_copy_match(exact_strings(k, job_id), recipe, _rendered_text(k, meta, media_kind), logo_present=bool(logo)),
                    verify.not_previously_rejected(k.store, job_id, aid), verify.ad_structure(_as_direction(recipe), media_kind, bool(logo))]
            if media_kind == "video" and not meta.get("placeholder"):
                srcs = []
                for sg in meta["segments"]:
                    try:
                        p = media.probe(sg["clip"]); srcs.append([p["width"], p["height"]])
                    except media.MediaError:
                        pass
                rep = meta["assembly"]
                rows += verify.film_checks(Path(a["path"]), cuts=rep["cuts_s"], source_sizes=srcs,
                                           delivered=media.FORMAT_PX[json.loads(k.store.node(job_id, "film")["spec_json"])["aspect"]],
                                           planned_s=rep.get("duration_s"), card_in_s=rep.get("card_in_s"))
            if media_kind == "image" and not meta.get("placeholder"):
                rows.append(verify.format_revalidated(k.store, aid, meta.get("format")))
            rows += verify.process_controls(k.store, job_id, media_kind, clip_asset_ids=[sg["asset"] for sg in meta.get("segments", [])])
            verify.record_rows(k.store, job_id, aid, rows, runner="measuring_tools")
    review = big_taste(k, job_id, finals, media_kind)
    k.put_form(job_id, "final_review", review)
    req = required(k, job_id)
    mids = [m["id"] for m in u.get("mandatory", [])]
    for aid in finals:
        verify.record_rows(k.store, job_id, aid, verify.review_rows(_as_v1_review(review), mandatory_ids=mids, media_kind=media_kind,
                                                                    asset_sha256=k.store.asset(aid)["sha256"],
                                                                    qualified=k.qualified("big_taster")),
                           runner=f"big_taster:{review['written_by']['model']}")
    results = [verify.gateway(k.store, job_id, aid, req) for aid in finals]
    k.put_form(job_id, "gateway_report", {"results": results, "required": req, "overrides": results[0]["founder_overrides"] if results else []},
               by="door_guard")
    verdict = review["verdict"]
    if verdict != "pass":
        return _send_back(k, job_id, review)
    ready = all(r["ready"] for r in results)
    if ready and not k.s.hold_before_preview:
        k.store.transition(job_id, "checking", "ready_for_review", actor="door_guard", presented_at=utc_now())
        k.store.timing_start(job_id, "customer_wait", "review")
    else:
        k.store.transition(job_id, "checking", "operator_hold", actor="door_guard",
                           data={"ready": ready, "blocking": [b["check_id"] for r in results for b in r["blocking"]][:40]})


def _send_back(k, job_id, review):
    """The big taster said no. Where it goes is decided here by code, from the defects' earliest stage (spec §6.2)."""
    defects = [d for d in review.get("defects", []) if d.get("severity") in ("blocker", "major")] or review.get("defects", [])
    plan = [d for d in defects if d.get("earliest_stage") == "plan"]
    shots = sorted({int(d["shot"]) for d in defects if d.get("shot")})
    why = "; ".join(f"{d.get('id')}: {d.get('description', '')[:120]}" for d in defects)[:600]
    if review["verdict"] == "fail" and plan or (review["verdict"] == "fail" and not shots):
        flow.send_back(k.store, job_id, "SB-BIG-FAIL", why=why)             # 1 round; a second fail → the founder
        k.store.put_artifact(job_id, "replan_request", {"from": "big_taster", "defects": defects, "why": why}, "big_taster")
        k.store.transition(job_id, "checking", "directing", actor="big_taster", data={"reason": "the recipe itself is wrong", "why": why})
        return
    flow.send_back(k.store, job_id, "SB-BIG-FIX", why=why)                  # 2 rounds, then the founder
    from product.stations.head_cook import _reset_downstream
    reset = []
    for n in shots:
        if k.store.node(job_id, f"shot_{n}"):
            note = "; ".join(d.get("repair", "") for d in defects if d.get("shot") == n)[:300]
            reset += _reset_downstream(k, job_id, f"frame_{n}" if _stage(defects, n) in ("reference",) else f"shot_{n}", note)
    if not reset:
        for x in ("film",) if k.store.node(job_id, "film") else [n["node_id"] for n in k.store.nodes(job_id) if n["kind"] == "compose_still"]:
            reset += _reset_downstream(k, job_id, x, why[:300])
    k.store.put_artifact(job_id, "internal_repair", {"defects": defects, "nodes": sorted(set(reset))}, "big_taster")
    k.store.transition(job_id, "checking", "producing", actor="big_taster", data={"fix": sorted(set(reset))})


def _stage(defects, n):
    return next((d.get("earliest_stage") for d in defects if d.get("shot") == n), "generation")


def big_taste(k, job_id, finals, media_kind) -> dict:
    u = k.store.artifact(job_id, "understanding")
    items, note, shas = [], "", []
    for aid in finals:
        a = k.store.asset(aid)
        if json.loads(a["meta_json"]).get("placeholder"):
            note += f"{aid}: stand-in file (no media engine on this host). "
            continue
        shas.append(a["sha256"])
        if media_kind == "image":
            items.append(("image/png", Path(a["path"]).read_bytes()))
            note += f"image {len(items)}: {json.loads(a['meta_json']).get('format')} at delivery size. "
        elif k.s.models.get("big_taster", "").startswith("gemini"):
            small = k.store.new_output_path(Path(a["path"]).parent, Path(a["path"]).stem + "-review", "mp4")
            media.reencode_small(a["path"], small)
            items.append(("video/mp4", small.read_bytes()))
            note += "The attached MP4 is the complete assembled film with its sound (720p review copy). "
        else:
            sheet = k.store.new_output_path(Path(a["path"]).parent, "contact", "png")
            media.contact_sheet(a["path"], sheet)
            items.append(("image/png", sheet.read_bytes()))
            note += "Contact sheet at 2 fps; the audio could not be sent. "
    from product.stations.head_cook import product_refs
    refs = product_refs(k, job_id, 3)
    checks = [{"check": r["check_id"], "status": r["status"]} for aid in finals for r in k.store.checks(aid)]
    ctx = {"UNDERSTANDING": {kk: u[kk] for kk in ("objective", "audience", "audience_response", "forbidden", "deliverable")},
           "MANDATORY": u.get("mandatory", []), "MEASUREMENTS": checks,
           "MEDIA_NOTE": ("The first image(s) are the customer's own product photos (reference, not the work); the rest is the finished "
                          "work. " if refs else "") + (note or "no media")}
    total = sum(float(s["duration_s"]) for s in (k.store.artifact(job_id, "recipe") or {}).get("shots", [])) or 8.0
    with k.store.timed(job_id, "independent_review", "big taster"):
        review = k.workers.call(job_id, "big_taster", "final_review", ctx, exact_words=k.exact_words(job_id), media=refs + items,
                                video_seconds=total, sim_args={"cut": len(k.store.artifact_versions(job_id, "final_review")) + 1})
    review["_reviewed_sha256"] = shas
    return review


def _as_v1_review(r: dict) -> dict:
    """verify.review_rows speaks the v1 review shape (pass/repair/fail, beat); map the Final review form onto it."""
    out = dict(r)
    out["verdict"] = {"pass": "pass", "fix": "repair", "fail": "fail"}[r["verdict"]]
    out["defects"] = [{**d, "beat": d.get("shot")} for d in r.get("defects", [])]
    out["_simulated"] = bool((r.get("written_by") or {}).get("simulated"))
    out["_call"] = {"isolated": True, "model": (r.get("written_by") or {}).get("model")}
    return out


def _as_direction(recipe):
    return {**recipe, "beats": [{**s, "beat": s["n"]} for s in recipe.get("shots", [])]}


def exact_strings(k, job_id) -> list:
    over = k.store.artifact(job_id, "copy_overrides") or {}
    return [over.get(s, s) for s in k.brief(job_id).get("exact_strings", [])]


def _rendered_text(k, meta: dict, media_kind: str):
    if meta.get("placeholder"):
        return None
    if media_kind == "image":
        return (meta.get("layout") or {}).get("rendered_text")
    card = json.loads(k.store.asset(meta["end_card"])["meta_json"]).get("layout", {}).get("rendered_text")
    if card is None:
        return None
    out = list(card)
    for sp in meta.get("supers", []):
        out += json.loads(k.store.asset(sp["asset"])["meta_json"]).get("rendered_text") or []
    return out


# ── founder and customer decisions at the door ───────────────────────────────────────────────────────────────────
def founder_override(k, job_id, proof, reason):
    """The founder overrides the big taster's fix/fail (spec §6.4): the cut goes to the door guard's hold, where every
    FAILED or unverified check still needs the founder's own waiver or confirmation before release."""
    fr = k.store.artifact(job_id, "final_review") or {}
    if fr.get("verdict") == "pass":
        raise ValueError("the big taster passed this cut; nothing to override")
    k.store.add_override(job_id, kind="big_taster", target=f"final_review v{len(k.store.artifact_versions(job_id, 'final_review'))}",
                         founder=proof, reason=reason, data={"verdict": fr.get("verdict"), "defects": fr.get("defects")})
    if k.store.job(job_id)["state"] == "paused_for_founder":
        k.store.transition(job_id, "paused_for_founder", "operator_hold", actor=proof.actor, founder=proof, data={"reason": reason},
                           pause_reason=None)


def release(k, job_id, proof):
    rep = k.store.artifact(job_id, "gateway_report") or {"results": []}
    req = required(k, job_id)
    fresh = [verify.gateway(k.store, job_id, r["asset_id"], req) for r in rep["results"]]
    if not fresh or not all(r["ready"] for r in fresh):
        raise PermissionError("the door guard still blocks: " + ", ".join(b["check_id"] for r in fresh for b in r["blocking"])
                              + " — confirm or waive each (founder), or fix them")
    fr = k.store.artifact(job_id, "final_review") or {}
    if fr.get("verdict") != "pass" and not k.store.overrides(job_id, "big_taster"):
        raise PermissionError("the big taster did not pass this cut and the founder has not overridden it")
    k.put_form(job_id, "gateway_report", {"results": fresh, "required": req, "overrides": fresh[0]["founder_overrides"],
                                          "released_by": proof.actor}, by="door_guard")
    k.store.transition(job_id, "operator_hold", "ready_for_review", actor=proof.actor, founder=proof, presented_at=utc_now())
    k.store.timing_start(job_id, "customer_wait", "review")


def accept(k, job_id, by: str):
    from product.stations import diary
    req = required(k, job_id)
    finals = k.final_assets(job_id)
    for aid in finals:
        g = verify.gateway(k.store, job_id, aid, req)
        if not g["ready"]:
            raise PermissionError(f"{aid} is not presentable: {[b['check_id'] for b in g['blocking']]}")
    for aid in finals:
        k.store.deliver(job_id, aid, by)
    k._end_wait(job_id, "review")
    k.store.transition(job_id, "ready_for_review", "accepted", actor=by, data={"delivered": finals}, closed_at=utc_now(), outcome="accepted")
    propose_shelf(k, job_id)
    from product import learning
    learning.write_case(k.store, job_id)
    diary.write(k, job_id)


def propose_shelf(k, job_id):
    """An accepted job puts what it established on the customer's shelf as PROPOSALS (logo, colours, product photos with
    roles, the character); the customer approves each once. The master plate was approved in the job itself."""
    job = k.store.job(job_id)
    acct, sh = job["account_id"], k.shelf
    brief = k.brief(job_id)
    for c in brief.get("brand_colours") or []:
        sh.propose(acct, kind="brand_colour", key=c.lower(), data={"hex": c}, source_job_id=job_id)
    for a in k.uploads(job_id, "logo")[-1:]:
        sh.propose(acct, kind="logo", key="primary", data={"filename": json.loads(a["meta_json"]).get("filename")}, file=Path(a["path"]),
                   source_job_id=job_id)
    u = k.store.artifact(job_id, "understanding") or {}
    product = (brief.get("product") or {}).get("name") or "product"
    for r in u.get("photo_roles", []):
        if r["role"] in ("product_view", "product_detail", "infographic"):
            a = k.store.asset(r["asset_id"])
            sh.propose(acct, kind="product_photo", key=f"{product}/{json.loads(a['meta_json']).get('filename')}",
                       data={"product": product, "role": r["role"], "shows": r["shows"]}, file=Path(a["path"]), source_job_id=job_id)
    recipe = k.store.artifact(job_id, "recipe") or {}
    ch = k.store.node(job_id, "character")
    if (recipe.get("character") or {}).get("present") and ch and ch["selected_asset_id"] and not json.loads(ch["spec_json"]).get("shelf_item"):
        a = k.store.asset(ch["selected_asset_id"])
        sh.propose(acct, kind="character", key=recipe["character"]["description"][:60],
                   data={"description": recipe["character"]["description"]}, file=Path(a["path"]), source_job_id=job_id)
