"""Station — the chef (kitchen v3, founder-approved 2026-09-25).

    tray (Canon, past recipes, repeated failures, the tools' track record, the customer's shelf) → Recipe (the chef writes
    the story, the board and every prompt in full) → normalise (code: exact words, an end card, the ordered length, and
    the older production fields derived from the chef's own — never a rewrite of the chef's prompts) → quote + the look of
    the film → the CUSTOMER approves or asks for changes.

There is no recipe checker: the customer checks the recipe. The chef is called again only when the customer asks for a
change, or when the gatekeeper finds the finished dish is not the dish that was ordered (earliest_stage plan).
"""
from __future__ import annotations

import json

from product import cost, library
from product.store import dec, money, utc_now

FILM_ROUTE = {"video": "FILM-C", "still": "FILM-A", "photo": "FILM-A", "end_card": "END-CARD"}


def _tray(k, job_id, u, recipe=None, worker="chef"):
    job = k.store.job(job_id)
    words = k.exact_words(job_id)
    classes = sorted(set(library.classify(words)) | {"person_performance", "simple_hand_gesture", "product_state_still",
                                                      "product_still_from_clean_photo", "camera_move_static_product"})
    routes = ["IMG"] if u["deliverable"]["media"] == "image" else ["FILM-A", "FILM-B", "FILM-C"]
    slip = k.store.artifact(job_id, "order_slip")
    args = {"media": u["deliverable"]["media"], "brief_text": words, "market": u.get("market") or "IN",
            "language": u.get("language") or "en", "product": {"category": u["product"].get("category"), "brand": u.get("brand")},
            "exact_strings": slip.get("exact_strings", []), "has_product_photo": bool(slip.get("photos"))}
    return k.librarian.tray(job_id, worker, query=words + " " + u.get("objective", ""), media=u["deliverable"]["media"],
                            account_id=job["account_id"], action_classes=classes, routes=routes,
                            product_category=u["product"].get("category"), cookbook_args=args)


def _chef_call(k, job_id, u, extra: dict) -> dict:
    slip = k.store.artifact(job_id, "order_slip")
    job = k.store.job(job_id)
    tray = _tray(k, job_id, u)
    photos = [{"photo_index": i + 1, "shows": r.get("shows"), "customer_label": r.get("customer_label")}
              for i, r in enumerate(u.get("photo_roles") or [])]
    ctx = {"UNDERSTANDING": _public(u),
           "ORDER_SLIP": {kk: slip[kk] for kk in ("exact_strings", "formats", "duration_s", "brand_colours", "media")},
           "PHOTOS": photos or "no photos supplied",
           "SHELF": k.shelf.summary(job["account_id"]), **extra}
    with k.store.timed(job_id, "creative_planning"):
        r = k.workers.call(job_id, "chef", "recipe", ctx, exact_words=k.exact_words(job_id), media=k.photo_media(job_id, 6), tray=tray,
                           model_key="chef_image" if u["deliverable"]["media"] == "image" else None)
    r["_normalisation_notes"] = normalise(r, u, slip)
    return r


def direct(k, job_id: str):
    u = k.store.artifact(job_id, "understanding")
    extra = {}
    change = k.store.artifact(job_id, "plan_change")
    if change and not change.get("_used"):
        prev = k.store.artifact(job_id, "recipe")
        extra["CUSTOMER_CHANGE_REQUEST"] = change
        if prev:
            extra["PREVIOUS_RECIPE"] = _public(prev)
    fail = k.store.artifact(job_id, "replan_request")
    if fail and not fail.get("_used"):
        extra["GATEKEEPER_FOUND"] = fail
    recipe = _chef_call(k, job_id, u, extra)
    k.put_form(job_id, "recipe", recipe)
    _mark_used(k, job_id)
    to_customer(k, job_id, recipe)


def _mark_used(k, job_id):
    for kind in ("plan_change", "replan_request"):
        a = k.store.artifact(job_id, kind)
        if a and not a.get("_used"):
            k.store.put_artifact(job_id, kind, {**a, "_used": True}, "system")


def to_customer(k, job_id, recipe):
    """The recipe goes to the customer with the price and the look of the film (a still picture they can see)."""
    q = cost.quote(k, job_id, recipe)
    k.store.put_artifact(job_id, "quote", q, "system")
    k.store.put_artifact(job_id, "plan_note", {"text": "Here is the recipe for your dish. Read it, then say go ahead or tell us what "
                                                       "to change.", "objections": False}, "system")
    from product.stations import head_cook
    prev = [a for a in k.store.assets(job_id, role="preview")]
    look = (recipe.get("look") or {}).get("picture_prompt")
    same_look = prev and json.loads(prev[-1]["meta_json"]).get("look") == look
    if not same_look:                       # a change that keeps the look does not buy a new picture
        head_cook.sample_picture(k, job_id, recipe)
    frm = k.store.job(job_id)["state"]
    acct = k.store.account(k.store.job(job_id)["account_id"])
    cap = dec(k.brief(job_id).get("max_budget_usd") or 0)
    if acct["auto_approve"] and cap >= dec(q["recommended_budget_usd"]) and frm == "directing":
        approve(k, job_id, by="auto-approve (account setting)", budget_usd=cap)
        return
    k.store.transition(job_id, frm, "awaiting_approval", actor="system")
    k.store.timing_start(job_id, "customer_wait", "approval")


after_approved_recipe = to_customer          # older callers


def approve(k, job_id, *, by: str, budget_usd, note: str = "", accept_objections: bool = False):
    """The customer's go-ahead: the recipe is theirs, and so is the budget."""
    job = k.store.job(job_id)
    acct = k.store.account(job["account_id"])
    budget = dec(budget_usd)
    if k.s.account_ceiling_enforced and budget > dec(acct["ceiling_usd"]):      # off in beta (founder 2026-09-24)
        raise PermissionError(f"USD {budget} is above the account ceiling USD {acct['ceiling_usd']}")
    committed = k.store.committed_usd(job_id)
    k._end_wait(job_id, "approval")
    k.store.transition(job_id, ("awaiting_approval", "directing"), "planning", actor=by,
                       data={"budget_usd": money(budget), "note": note, "recipe_version": len(k.store.artifact_versions(job_id, "recipe"))},
                       budget_usd=money(max(budget, committed)), budget_authorised_by=by, budget_authorised_at=utc_now(),
                       approved_at=job["approved_at"] or utc_now())


def add_customer_note(k, job_id, text: str):
    """Notes shown with the customer's preview (what the kitchen changed or could not do as planned)."""
    cur = k.store.artifact(job_id, "customer_notes") or {"notes": []}
    if text not in cur["notes"]:
        k.store.put_artifact(job_id, "customer_notes", {"notes": cur["notes"] + [text]}, "system")


def normalise(r: dict, u: dict, slip: dict) -> list:
    """Code's only corrections, each recorded: the customer's exact words in the copy deck; films end on an end card and
    run the ordered length. Then the older production fields are DERIVED from the chef's own (route from tool, first
    frame from the chef's picture prompt, action from the chef's motion prompt, ...). The chef's prompts are never
    rewritten."""
    notes = []
    deck = r.setdefault("copy_deck", [])
    for s in slip.get("exact_strings", []):
        if s and s not in [c["text"] for c in deck]:
            deck.append({"id": f"c{len(deck) + 1}", "text": s, "role": "line", "source": "customer_exact"})
            notes.append(f"added the customer's exact string {s!r} to the copy deck")
    anchors = r.get("identity_anchors") or {}
    look = r.get("look") or {}
    person = (anchors.get("person") or "").strip()
    has_person = bool(person) and not person.lower().startswith(("none", "no person", "n/a"))
    r.setdefault("proposition", r.get("selected_concept", ""))
    r.setdefault("concepts", [{"name": r.get("selected_concept", "")[:80], "idea": r.get("story", "")[:400],
                               "why_it_works": r.get("remember", "")}])
    r.setdefault("rationale", r.get("story", "")[:600])
    r.setdefault("audience_experience", r.get("audience_person", ""))
    r.setdefault("hook", (r.get("shots") or [{}])[0].get("impact", "") if r.get("shots") else "")
    r["product_anchor"] = anchors.get("product", "")
    r["master_plate"] = {"description": look.get("picture_prompt", ""), "product_state": ""}
    r["character"] = {"present": has_person, "description": person if has_person else ""}
    r["visual_language"] = {"look": anchors.get("grade", ""), "light": anchors.get("grade", ""), "palette": [], "camera": ""}
    r["composition"] = {"hero": "", "text_zone": look.get("text_zone", "top"), "background": anchors.get("world", ""),
                        "product_treatment": ""}
    r.setdefault("risks", [])
    r.setdefault("reuse_shelf_items", [])
    if u["deliverable"]["media"] != "video":
        if r.get("shots"):
            notes.append("a still picture has no shots; removed")
        r["shots"] = []
        return notes
    shots = r.get("shots") or []
    if not any(s.get("tool") == "end_card" for s in shots):
        shots.append({"n": len(shots) + 1, "duration_s": 3.0, "title": "End card", "feeling": "the idea, remembered",
                      "framing": "the end card", "impact": "the product name and the last line",
                      "description": "The end card, set by code from the end card copy.", "tool": "end_card",
                      "picture_prompt": "", "motion_prompt": "", "photo_index": None, "product_present": False, "super_id": None})
        notes.append("added a 3 s end card")
    for s in shots:
        if s.get("tool") != "end_card" and float(s["duration_s"]) > 8.0:
            notes.append(f"shot {s['n']} shortened from {s['duration_s']}s to 8s (the longest clip the video model makes)")
            s["duration_s"] = 8.0
        s["duration_s"] = max(1.0, float(s["duration_s"]))
    target = min(float(u["deliverable"].get("duration_s") or sum(float(s["duration_s"]) for s in shots)), 30.0)
    total = sum(float(s["duration_s"]) for s in shots)
    if abs(total - target) > 0.25:
        body = [s for s in shots if s.get("tool") != "end_card"]
        card = sum(float(s["duration_s"]) for s in shots if s.get("tool") == "end_card")
        scale = (target - card) / max(0.1, sum(float(s["duration_s"]) for s in body))
        for s in body:
            s["duration_s"] = round(min(8.0, max(1.0, float(s["duration_s"]) * scale)), 2)
        notes.append(f"shot lengths scaled so the film runs {target:.1f}s (was {total:.1f}s)")
    shots.sort(key=lambda s: (s.get("tool") == "end_card", s["n"]))
    for i, s in enumerate(shots, 1):
        s["n"] = i
        tool = s.get("tool") or "still"
        s["route"] = FILM_ROUTE.get(tool, "FILM-A")
        s["action_class"] = {"video": "person_performance" if has_person else "camera_move_static_product",
                             "photo": "product_still_from_clean_photo", "end_card": "none"}.get(tool, "product_state_still")
        s["starts_from"] = "still_only" if tool == "end_card" else "master_plate"
        s["first_frame"] = s.get("picture_prompt", "")
        s["action"] = s.get("motion_prompt", "")
        s.setdefault("purpose", s.get("title", ""))
        for kk, v in (("end_state", ""), ("camera", ""), ("product_state", ""), ("continuity", []), ("must_not", []),
                      ("mandatory_ids", []), ("feasibility_refs", [])):
            s.setdefault(kk, v)
    r["shots"] = shots
    return notes


def _public(d: dict) -> dict:
    return {kk: v for kk, v in (d or {}).items() if not kk.startswith("_") and kk not in ("written_by", "llm_call_id", "input_sha256")}


def recipe_routes(recipe: dict) -> list:
    return sorted({s["route"] for s in recipe.get("shots", [])} - {"END-CARD"})


__all__ = ["direct", "approve", "to_customer", "normalise", "add_customer_note"]
