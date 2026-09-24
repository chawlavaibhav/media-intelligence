"""The gatekeeper (kitchen v3, founder-approved 2026-09-25): the one final check, from another AI company than the chef,
watching the finished film with its sound, against what the customer ordered — plus the measuring tools (deterministic
checks on the exact file: exact words, sizes, cuts, the money ledger).

    pass → the customer receives the dish
    fix  → the head cook repairs ONLY the named shots, within the approved budget (2 rounds), then the gatekeeper looks again
    fail (not the dish that was ordered) → the chef rewrites the recipe (1 round) and the customer approves it again
    still failing / repairs used up → the customer sees the dish with the plain report and decides
The gatekeeper never judges taste (the customer's) and never asks for a safer or different idea.
"""
from __future__ import annotations

import json
from pathlib import Path

from product import customer, flow, media, verify
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
    if not k.qualified("head_cook"):
        req["head_cook_confirmed"] = "QA_COVERAGE_ENFORCEMENT"
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
                    verify.not_previously_rejected(k.store, job_id, aid)]
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
                                                                    qualified=k.qualified("gatekeeper", review["written_by"]["model"]),
                                                                    voice_over=bool(((k.store.artifact(job_id, "recipe") or {}).get("voice_over") or {}).get("wanted"))),
                           runner=f"gatekeeper:{review['written_by']['model']}")
    results = [verify.gateway(k.store, job_id, aid, req) for aid in finals]
    k.put_form(job_id, "gateway_report", {"results": results, "required": req, "overrides": results[0]["founder_overrides"] if results else []},
               by="door_guard")
    if review["verdict"] != "pass":
        return _send_back(k, job_id, review, results)
    if any(r["measured_failed"] for r in results):
        return measured_repair(k, job_id, results)
    present(k, job_id, results)


def present(k, job_id, results):
    """The door guard lets the cut through to the customer unless a MEASURED check blocks it. Judgement rows an unqualified
    judge could not settle are the customer's to settle by looking; the preview says so."""
    if not all(r["presentable"] for r in results):
        return customer_decision(k, job_id, results)          # a measured check could not run / failed: never shown
    if any(r["judgement_open"] for r in results):
        from product.stations.chef import add_customer_note
        add_customer_note(k, job_id, "Our automatic reviewers are still in training, so your look at this preview is the final "
                                     "check: accept it only if it is right.")
    if k.s.hold_before_preview:        # the founder chose to look first (MI_HOLD_BEFORE_PREVIEW=1)
        k.store.transition(job_id, "checking", "operator_hold", actor="door_guard",
                           data={"hold_before_preview": True, "open": [b["check_id"] for r in results for b in r["blocking"]][:40]})
        return
    k.store.transition(job_id, "checking", "ready_for_review", actor="door_guard", presented_at=utc_now())
    k.store.timing_start(job_id, "customer_wait", "review")


def plain_report(review) -> str:
    defects = review.get("defects") or []
    parts = [f"{d.get('where') or 'the cut'}: {d.get('description', '')}" for d in defects]
    return ((review.get("summary_for_customer") or "").strip() + (" Problems our reviewer found: " + "; ".join(parts) + "." if parts else "")).strip()


def _to_customer(k, job_id, review, results):
    """Repairs used up, or the plan failed twice: the customer sees the cut with the plain report and decides (accept as is,
    changes — priced — or reject). A measured FAIL still never ships."""
    from product.stations.chef import add_customer_note
    report = plain_report(review)
    k.store.put_artifact(job_id, "review_report", {"verdict": review["verdict"], "plain": report, "defects": review.get("defects", [])},
                         "gatekeeper")
    add_customer_note(k, job_id, f"We tried to improve this ourselves and our reviewer still has comments: {report} "
                                 "You decide: accept it as it is, ask for changes, or turn it down.")
    k.store.event(job_id, "system", "to_customer_with_report", {"verdict": review["verdict"]})
    if any(r["measured_failed"] for r in results):
        return customer_decision(k, job_id, results)
    present(k, job_id, results)


def measured_repair(k, job_id, results):
    """A measured check FAILED on the exact file: it never ships. The system repairs it automatically (SB-BIG-FIX, 2 rounds,
    within the approved budget); still failing → the customer decides (stop or a paid rework)."""
    failed = [{"asset_id": r["asset_id"], "check_id": b["check_id"], "detail": b["detail"]} for r in results for b in r["measured_failed"]]
    why = "; ".join(f"{x['check_id']}: {str(x['detail'])[:100]}" for x in failed)[:600]
    try:
        flow.send_back(k.store, job_id, "SB-BIG-FIX", why=why)
    except flow.LimitReached:
        return customer_decision(k, job_id, results)
    from product.stations.head_cook import _reset_downstream
    reset = []
    for x in {f["asset_id"] for f in failed}:
        node = k.store.asset(x)["node_id"]
        if node:
            reset += _reset_downstream(k, job_id, node, f"measured check failed: {why[:250]}")
    k.store.put_artifact(job_id, "internal_repair", {"measured": failed, "defects": [], "nodes": sorted(set(reset))}, "door_guard")
    k.store.transition(job_id, "checking", "producing", actor="door_guard", data={"repair": sorted(set(reset)), "measured_failed": why})


def rework_price(k, job_id, asset_ids) -> str:
    from decimal import Decimal
    from product.dispatch import quote as provider_quote
    if k.store.job(job_id)["media"] == "image":
        return str((Decimal(2 * len(asset_ids)) * provider_quote("nano-banana-2")).quantize(Decimal("0.01")))
    q = k.store.artifact(job_id, "quote") or {}
    return str(Decimal(q.get("media_ceiling_usd") or "1.00"))


def customer_decision(k, job_id, results):
    """A measured check blocks and the automatic repairs are used up: the customer is told, in plain words, what failed and
    chooses stop (nothing more is spent) or a paid rework (one more attempt at the failing files, priced)."""
    blocked = [{"asset_id": r["asset_id"], "check_id": b["check_id"], "status": b["status"], "detail": str(b["detail"])[:300]}
               for r in results for b in r["measured_blocking"]]
    assets = sorted({b["asset_id"] for b in blocked})
    k.store.put_artifact(job_id, "customer_decision", {
        "what_failed": blocked, "options": ["stop", "rework"], "rework_price_usd": rework_price(k, job_id, assets),
        "plain": "We checked the finished work and something isn't right yet, so we won't send it to you like this. "
                 + " ".join(dict.fromkeys(customer.problem_words(b["check_id"]) for b in blocked))
                 + " We tried to fix it ourselves. You can stop here (nothing more is spent), or ask us to make it again "
                   "(about USD " + rework_price(k, job_id, assets) + ")."}, "door_guard")
    k.store.transition(job_id, "checking", "needs_customer_decision", actor="door_guard", data={"blocked": [b["check_id"] for b in blocked]})
    k.store.timing_start(job_id, "customer_wait", "decision")


def decide(k, job_id, *, by: str, choice: str, note: str = "", budget_usd=None):
    """The customer's answer to needs_customer_decision: stop, or a paid rework (the customer's money decision; within the
    account ceiling only when MI_ENFORCE_ACCOUNT_CEILING is on — off in beta, 2026-09-24)."""
    from decimal import Decimal
    from product.store import dec, money
    job = k.store.job(job_id)
    if job["state"] != "needs_customer_decision":
        raise ValueError("there is no decision waiting on this job")
    d = k.store.artifact(job_id, "customer_decision")
    k._end_wait(job_id, "decision")
    if choice == "stop":
        from product.stations import diary
        k.store.transition(job_id, "needs_customer_decision", "abandoned", actor=by, data={"reason": note[:300] or "customer stopped"},
                           closed_at=utc_now(), outcome="abandoned")
        diary.write(k, job_id)
        return
    if choice != "rework":
        raise ValueError(choice)
    price = Decimal(d["rework_price_usd"])
    budget = max(dec(budget_usd) if budget_usd else Decimal(0), k.store.committed_usd(job_id) + price, dec(job["budget_usd"]))
    if k.s.account_ceiling_enforced and budget > dec(k.store.account(job["account_id"])["ceiling_usd"]):   # off in beta
        raise PermissionError(f"USD {money(budget)} is above the account ceiling")
    from product.stations.head_cook import _reset_downstream
    reset = []
    for aid in {b["asset_id"] for b in d["what_failed"]}:
        node = k.store.asset(aid)["node_id"]
        root = node.replace("ad_", "plate_") if node and node.startswith("ad_") and k.store.node(job_id, node.replace("ad_", "plate_")) else node
        if root:
            reset += _reset_downstream(k, job_id, root, f"paid rework: {note[:200]}")
    k.store.event(job_id, by, "customer_rework", {"price_usd": str(price), "budget_usd": money(budget), "nodes": sorted(set(reset))})
    k.store.transition(job_id, "needs_customer_decision", "producing", actor=by, data={"rework": sorted(set(reset))},
                       budget_usd=money(budget), budget_authorised_by=by, budget_authorised_at=utc_now())


def _send_back(k, job_id, review, results):
    """The big taster said no. Where it goes is decided here by code, from the defects' earliest stage (spec §6.2)."""
    defects = [d for d in review.get("defects", []) if d.get("severity") in ("blocker", "major")] or review.get("defects", [])
    plan = [d for d in defects if d.get("earliest_stage") == "plan"]
    shots = sorted({int(d["shot"]) for d in defects if d.get("shot")})
    why = "; ".join(f"{d.get('id')}: {d.get('description', '')[:120]}" for d in defects)[:600]
    if review["verdict"] == "fail" and plan or (review["verdict"] == "fail" and not shots):
        try:
            flow.send_back(k.store, job_id, "SB-BIG-FAIL", why=why)         # 1 round; a second fail → the customer decides
        except flow.LimitReached:
            return _to_customer(k, job_id, review, results)
        k.store.put_artifact(job_id, "replan_request", {"from": "gatekeeper", "defects": defects, "why": why}, "gatekeeper")
        k.store.transition(job_id, "checking", "directing", actor="gatekeeper", data={"reason": "the recipe itself is wrong", "why": why})
        return
    try:
        flow.send_back(k.store, job_id, "SB-BIG-FIX", why=why)              # 2 automatic rounds, then the customer decides
    except flow.LimitReached:
        return _to_customer(k, job_id, review, results)
    from product.stations.head_cook import _reset_downstream
    reset = []
    for n in shots:
        if k.store.node(job_id, f"shot_{n}"):
            note = "; ".join(d.get("repair", "") for d in defects if d.get("shot") == n)[:300]
            # the first frame is redrawn too: a clip remade from the same wrong frame copies the fault
            reset += _reset_downstream(k, job_id, f"frame_{n}", note)
    if not reset:
        for x in ("film",) if k.store.node(job_id, "film") else [n["node_id"] for n in k.store.nodes(job_id) if n["kind"] == "compose_still"]:
            reset += _reset_downstream(k, job_id, x, why[:300])
    k.store.put_artifact(job_id, "internal_repair", {"defects": defects, "nodes": sorted(set(reset))}, "gatekeeper")
    k.store.transition(job_id, "checking", "producing", actor="gatekeeper", data={"fix": sorted(set(reset))})


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
        elif k.s.models.get("gatekeeper", "").startswith("gemini"):
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
    recipe = k.store.artifact(job_id, "recipe") or {}
    t0, board = 0.0, []
    deck = {c["id"]: c["text"] for c in recipe.get("copy_deck", [])}
    for s in recipe.get("shots", []):
        board.append({"shot": s["n"], "title": s.get("title"), "starts_s": round(t0, 2), "duration_s": s.get("duration_s"),
                      "what_we_see": s.get("description"), "tool": s.get("tool"), "words_on_screen": deck.get(s.get("super_id"))})
        t0 += float(s.get("duration_s") or 0)
    vo = recipe.get("voice_over") or {}
    ctx = {"UNDERSTANDING": {kk: u[kk] for kk in ("objective", "audience", "audience_response", "forbidden", "deliverable")},
           "MANDATORY": u.get("mandatory", []), "MEASUREMENTS": checks,
           # the board the customer approved is part of the order (kitchen v3): the gatekeeper checks the dish against it
           "APPROVED_BOARD": {"shots": board, "copy_deck": list(deck.values()), "product": u.get("product"),
                              "end_card": [deck.get(i) for i in (recipe.get("end_card") or {}).get("copy_ids", [])],
                              "voice_over": {"wanted": bool(vo.get("wanted")), "language": vo.get("language"),
                                             "lines": [ln.get("text") for ln in vo.get("lines", [])]}},
           "MEDIA_NOTE": ("The first image(s) are the customer's own product photos (reference, not the work); the rest is the finished "
                          "work. " if refs else "") + (note or "no media")}
    total = sum(float(s["duration_s"]) for s in (k.store.artifact(job_id, "recipe") or {}).get("shots", [])) or 8.0
    with k.store.timed(job_id, "independent_review", "big taster"):
        review = k.workers.call(job_id, "gatekeeper", "final_review", ctx, exact_words=k.exact_words(job_id), media=refs + items,
                                model_key="gatekeeper_image" if media_kind == "image" and "gatekeeper_image" in k.s.models else None,
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
    k.store.add_override(job_id, kind="gatekeeper", target=f"final_review v{len(k.store.artifact_versions(job_id, 'final_review'))}",
                         founder=proof, reason=reason, data={"verdict": fr.get("verdict"), "defects": fr.get("defects")})
    if k.store.job(job_id)["state"] == "paused_for_founder":
        k.store.transition(job_id, "paused_for_founder", "operator_hold", actor=proof.actor, founder=proof, data={"reason": reason},
                           pause_reason=None)


def release(k, job_id, proof):
    """The founder, who chose to hold cuts before the preview, lets one through. Measured checks must still pass (or be
    waived by the founder); judgement rows are the customer's to settle at the preview."""
    rep = k.store.artifact(job_id, "gateway_report") or {"results": []}
    req = required(k, job_id)
    fresh = [verify.gateway(k.store, job_id, r["asset_id"], req) for r in rep["results"]]
    if not fresh or not all(r["presentable"] for r in fresh):
        raise PermissionError("the door guard still blocks: " + ", ".join(b["check_id"] for r in fresh for b in r["measured_blocking"])
                              + " — waive each (founder), or fix them")
    k.put_form(job_id, "gateway_report", {"results": fresh, "required": req, "overrides": fresh[0]["founder_overrides"],
                                          "released_by": proof.actor}, by="door_guard")
    k.store.transition(job_id, "operator_hold", "ready_for_review", actor=proof.actor, founder=proof, presented_at=utc_now())
    k.store.timing_start(job_id, "customer_wait", "review")


def accept(k, job_id, by: str):
    from product.stations import diary
    req = required(k, job_id)
    finals = k.final_assets(job_id)
    if k.store.job(job_id)["state"] != "ready_for_review":
        raise PermissionError("there is no preview waiting for your acceptance")
    for aid in finals:
        g = verify.gateway(k.store, job_id, aid, req)
        if not g["presentable"]:
            raise PermissionError(f"{aid} is not presentable: {[b['check_id'] for b in g['measured_blocking']]}")
        objected = (k.store.artifact(job_id, "final_review") or {}).get("verdict") not in (None, "pass")
        for b in g["judgement_open"]:        # the customer's preview is the final check on every judgement row (amendment 1 §3)
            k.store.record_check(job_id, aid, check_id=b["check_id"], status="PASS", blocking=True, runner=f"customer:{by}",
                                 detail="the customer looked at the preview and accepted it"
                                        + (" as is, over our reviewer's objection" if b["status"] == "FAIL" or objected else "")
                                        + f" (was {b['status']}: {str(b['detail'])[:160]})")
        g = verify.gateway(k.store, job_id, aid, req)
        if not g["ready"]:
            raise PermissionError(f"{aid} is not deliverable: {[b['check_id'] for b in g['blocking']]}")
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
    m = k.store.node(job_id, "master")
    if m and m["selected_asset_id"] and not json.loads(m["spec_json"]).get("shelf_item") and not k.store.events(job_id, ("master_approved",)):
        # kitchen v3: the look of the film is no longer approved mid-job, so an accepted job offers it for the shelf
        a = k.store.asset(m["selected_asset_id"])
        sh.propose(acct, kind="master_plate", key=product,
                   data={"description": (recipe.get("look") or {}).get("picture_prompt") or (recipe.get("master_plate") or {}).get("description", ""),
                         "asset": a["id"]}, file=Path(a["path"]), source_job_id=job_id)
    ch = k.store.node(job_id, "character")
    if (recipe.get("character") or {}).get("present") and ch and ch["selected_asset_id"] and not json.loads(ch["spec_json"]).get("shelf_item"):
        a = k.store.asset(ch["selected_asset_id"])
        sh.propose(acct, kind="character", key=recipe["character"]["description"][:60],
                   data={"description": recipe["character"]["description"]}, file=Path(a["path"]), source_job_id=job_id)
