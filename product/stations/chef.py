"""Station 4 — the chef (strongest AI), with the librarian's tray and the recipe checker's binding send-back (spec §3, §4.4,
§4.5, §6.2, §8).

    tray → Recipe → normalise (code) → Recipe check (AI + code rules)
      approve   → quote + sample picture → the customer's plan card (awaiting_approval)
                  (while the recipe checker is unqualified its approve = "the founder confirms" first — spec §6.4, §10)
      add_steps → the chef applies them → checked again            } counted as recipe rounds: 2, then the founder decides
      send_back → the chef, with the reasons                      }
The same station re-plans ONE shot when the small taster rejects it twice (head_cook → replan_shot) and re-plans the
recipe when the big taster says the recipe is wrong (earliest_stage plan).
"""
from __future__ import annotations

import json

from product import authority, cost, flow, library
from product.store import dec, money, utc_now


def _tray(k, job_id, u, f, recipe=None, worker="chef"):
    job = k.store.job(job_id)
    classes = sorted({a["action_class"] for a in f.get("actions_needed", [])} |
                     ({s["action_class"] for s in recipe.get("shots", [])} if recipe else set()))
    routes = sorted({v["route"] for v in f.get("route_verdicts", []) if v["verdict"] != "cannot"} |
                    ({s["route"] for s in recipe.get("shots", [])} if recipe else set()) - {"END-CARD"})
    slip = k.store.artifact(job_id, "order_slip")
    query = k.exact_words(job_id) + " " + u.get("objective", "")
    args = None
    if worker == "chef":
        args = {"media": u["deliverable"]["media"], "brief_text": k.exact_words(job_id), "market": u.get("market") or "IN",
                "language": u.get("language") or "en", "product": {"category": u["product"].get("category"), "brand": u.get("brand")},
                "exact_strings": slip.get("exact_strings", []), "has_product_photo": bool(slip.get("photos"))}
    return k.librarian.tray(job_id, worker, query=query, media=u["deliverable"]["media"], account_id=job["account_id"],
                            action_classes=classes, routes=routes, product_category=u["product"].get("category"), cookbook_args=args)


def _chef_call(k, job_id, u, f, extra: dict) -> dict:
    slip = k.store.artifact(job_id, "order_slip")
    job = k.store.job(job_id)
    tray = _tray(k, job_id, u, f)
    ctx = {"UNDERSTANDING": _public(u),
           "FEASIBILITY": {kk: f[kk] for kk in ("actions_needed", "route_verdicts", "alternatives", "reference_risks", "verdict")},
           "ORDER_SLIP": {kk: slip[kk] for kk in ("exact_strings", "formats", "duration_s", "brand_colours", "media")},
           "SHELF": k.shelf.summary(job["account_id"]), **extra}
    with k.store.timed(job_id, "creative_planning"):
        r = k.workers.call(job_id, "chef", "recipe", ctx, exact_words=k.exact_words(job_id), media=k.photo_media(job_id, 3), tray=tray)
    r["_normalisation_notes"] = normalise(r, u, slip)
    return r


def direct(k, job_id: str):
    u, f = k.store.artifact(job_id, "understanding"), k.store.artifact(job_id, "feasibility")
    extra = {}
    change = k.store.artifact(job_id, "plan_change")
    if change and not change.get("_used"):
        extra["CUSTOMER_CHANGE_REQUEST"] = change
    fail = k.store.artifact(job_id, "replan_request")
    if fail and not fail.get("_used"):
        extra["REPLAN"] = fail
    recipe = _chef_call(k, job_id, u, f, extra)
    while True:
        check_tray = _tray(k, job_id, u, f, recipe, worker="recipe_checker")
        from product.stations import recipe_check
        rc = recipe_check.check(k, job_id, recipe, check_tray)
        k.put_form(job_id, "recipe", recipe)
        k.put_form(job_id, "recipe_check", rc)
        verdict = rc["verdict_after_code"]
        if verdict == "approve":
            break
        why = "; ".join([x["finding"] for x in rc["code_findings"]] + [i["issue"] for i in rc["issues"]] + rc["add_steps"])[:600]
        flow.send_back(k.store, job_id, "SB-RECIPE", why=why or verdict)      # raises LimitReached → the founder decides
        recipe = _chef_call(k, job_id, u, f, {**extra, "RECIPE_CHECK": {kk: rc[kk] for kk in ("verdict_after_code", "issues", "add_steps",
                                                                                               "code_findings", "past_failures_matched")},
                                              "PREVIOUS_RECIPE": _public(recipe)})
    for kind in ("plan_change", "replan_request"):
        a = k.store.artifact(job_id, kind)
        if a and not a.get("_used"):
            k.store.put_artifact(job_id, kind, {**a, "_used": True}, "system")
    after_approved_recipe(k, job_id, recipe, founder=None)


def after_approved_recipe(k, job_id, recipe, founder=None):
    """A recipe the checker approved (or the founder overrode/confirmed) goes to the customer's plan card."""
    if not k.qualified("recipe_checker") and founder is None:
        k.to_founder(job_id, "directing", "the recipe checker approved, but it is not yet qualified: the founder confirms the recipe "
                                          "before the customer sees it (spec 6.4)", "confirm recipe")
        return
    q = cost.quote(k, job_id, recipe)
    k.store.put_artifact(job_id, "quote", q, "system")
    from product.stations import head_cook
    head_cook.sample_picture(k, job_id, recipe)
    frm = k.store.job(job_id)["state"]
    acct = k.store.account(k.store.job(job_id)["account_id"])
    cap = dec(k.brief(job_id).get("max_budget_usd") or 0)
    if acct["auto_approve"] and cap >= dec(q["recommended_budget_usd"]) and frm == "directing":
        approve(k, job_id, by="auto-approve (account setting)", budget_usd=cap)
        return
    k.store.transition(job_id, frm, "awaiting_approval", actor=founder.actor if founder else "system", founder=founder)
    k.store.timing_start(job_id, "customer_wait", "approval")


def founder_confirm(k, job_id, proof, reason):
    """The founder confirms an unqualified recipe checker's approve (spec §6.4: its yes = the founder confirms)."""
    rc = k.store.artifact(job_id, "recipe_check") or {}
    if rc.get("verdict_after_code") != "approve":
        raise ValueError("there is no approved recipe to confirm; use override_recipe to override a send-back")
    k.store.add_override(job_id, kind="confirm_recipe", target=f"recipe v{len(k.store.artifact_versions(job_id, 'recipe'))}",
                         founder=proof, reason=reason)
    k.store.transition(job_id, "paused_for_founder", "directing", actor=proof.actor, founder=proof, data={"reason": "recipe confirmed"},
                       pause_reason=None)
    after_approved_recipe(k, job_id, k.store.artifact(job_id, "recipe"), founder=proof)


def founder_override(k, job_id, proof, reason):
    """The founder overrides the recipe checker's send-back (after the 2-round limit) — named and reasoned."""
    rc = k.store.artifact(job_id, "recipe_check") or {}
    if rc.get("verdict_after_code") == "approve":
        raise ValueError("the recipe checker approved this recipe; nothing to override")
    k.store.add_override(job_id, kind="recipe_send_back", target=f"recipe v{len(k.store.artifact_versions(job_id, 'recipe'))}",
                         founder=proof, reason=reason, data={"findings": rc.get("code_findings"), "issues": rc.get("issues")})
    k.store.transition(job_id, "paused_for_founder", "directing", actor=proof.actor, founder=proof, data={"reason": "recipe override"},
                       pause_reason=None)
    after_approved_recipe(k, job_id, k.store.artifact(job_id, "recipe"), founder=proof)


def approve(k, job_id, *, by: str, budget_usd, note: str = ""):
    job = k.store.job(job_id)
    rc = k.store.artifact(job_id, "recipe_check") or {}
    ok = rc.get("verdict_after_code") == "approve" or k.store.overrides(job_id, "recipe_send_back")
    if not ok:
        raise PermissionError("the recipe checker sent this recipe back; it cannot be approved until it is fixed or the founder overrides")
    acct = k.store.account(job["account_id"])
    budget = dec(budget_usd)
    if budget > dec(acct["ceiling_usd"]):
        raise PermissionError(f"USD {budget} is above the account ceiling USD {acct['ceiling_usd']}")
    committed = k.store.committed_usd(job_id)
    k._end_wait(job_id, "approval")
    k.store.transition(job_id, ("awaiting_approval", "directing"), "planning", actor=by,
                       data={"budget_usd": money(budget), "note": note, "recipe_version": len(k.store.artifact_versions(job_id, "recipe"))},
                       budget_usd=money(max(budget, committed)), budget_authorised_by=by, budget_authorised_at=utc_now(),
                       approved_at=utc_now())


def replan_shot(k, job_id: str, shot_n: int, why: str) -> dict:
    """The small taster rejected a shot's output twice: the chef re-plans THAT shot (route/action change). 1 per shot."""
    flow.send_back(k.store, job_id, "SB-TASTER-REPLAN", key=f"shot{shot_n}", why=why)
    u, f = k.store.artifact(job_id, "understanding"), k.store.artifact(job_id, "feasibility")
    old = k.store.artifact(job_id, "recipe")
    recipe = _chef_call(k, job_id, u, f, {"REPLAN": {"shot": shot_n, "why": why, "instruction": "change this shot's route or action; "
                                                     "keep every other shot exactly as it is"}, "PREVIOUS_RECIPE": _public(old)})
    for s in recipe.get("shots", []):          # keep every other shot exactly as approved (the chef may only touch this one)
        if s["n"] != shot_n:
            prev = next((p for p in old["shots"] if p["n"] == s["n"]), None)
            if prev:
                s.update(prev)
    new = next((s for s in recipe["shots"] if s["n"] == shot_n), None)
    oldshot = next((s for s in old["shots"] if s["n"] == shot_n), None)
    if new and oldshot and (new["route"], new["action"]) == (oldshot["route"], oldshot["action"]):
        # the re-plan must change something (spec §6.2): fall back to the safest route, a still with code motion
        new.update(route="FILM-A", action_class="product_state_still", starts_from="master_plate",
                   action=f"held still of: {oldshot['end_state']}", feasibility_refs=[])
    tray = _tray(k, job_id, u, f, recipe, worker="recipe_checker")
    from product.stations import recipe_check
    rc = recipe_check.check(k, job_id, recipe, tray)
    k.put_form(job_id, "recipe", recipe)
    k.put_form(job_id, "recipe_check", rc)
    if rc["verdict_after_code"] != "approve":
        raise flow.LimitReached("SB-TASTER-REPLAN", f"shot{shot_n}", 1)
    return recipe


def normalise(r: dict, u: dict, slip: dict) -> list:
    """Deterministic corrections, each recorded: exact strings verbatim in the copy deck; films have an end card, shot
    lengths a clip can carry, and a total equal to the requested duration; stills have no shots."""
    notes = []
    deck = r.setdefault("copy_deck", [])
    for s in slip.get("exact_strings", []):
        if s and s not in [c["text"] for c in deck]:
            deck.append({"id": f"c{len(deck) + 1}", "text": s, "role": "line", "source": "customer_exact"})
            notes.append(f"added the customer's exact string {s!r} to the copy deck")
    if u["deliverable"]["media"] != "video":
        if r.get("shots"):
            notes.append("a still has no shots; removed")
        r["shots"] = []
        return notes
    shots = r.get("shots") or []
    if not any(s["route"] == "END-CARD" for s in shots):
        shots.append({"n": len(shots) + 1, "duration_s": 3.0, "purpose": "sign-off", "first_frame": "end card", "action": "none",
                      "end_state": "logo and line", "camera": "n/a", "route": "END-CARD", "action_class": "none", "starts_from": "still_only",
                      "feasibility_refs": [], "product_present": False, "product_state": "n/a", "continuity": [], "must_not": [],
                      "super_id": None, "mandatory_ids": []})
        notes.append("added a 3 s end card")
    for s in shots:
        if s["route"] != "END-CARD" and float(s["duration_s"]) > 7.5:
            notes.append(f"shot {s['n']} shortened from {s['duration_s']}s to 7.5s")
            s["duration_s"] = 7.5
        if float(s["duration_s"]) < 1.0:
            s["duration_s"] = 1.0
    target = min(float(u["deliverable"].get("duration_s") or sum(float(s["duration_s"]) for s in shots)), 30.0)
    total = sum(float(s["duration_s"]) for s in shots)
    if abs(total - target) > 0.25:
        body = [s for s in shots if s["route"] != "END-CARD"]
        card = sum(float(s["duration_s"]) for s in shots if s["route"] == "END-CARD")
        scale = (target - card) / max(0.1, sum(float(s["duration_s"]) for s in body))
        for s in body:
            s["duration_s"] = round(min(7.5, max(1.0, float(s["duration_s"]) * scale)), 2)
        notes.append(f"shot lengths scaled so the film runs {target:.1f}s (was {total:.1f}s)")
    shots.sort(key=lambda s: (s["route"] == "END-CARD", s["n"]))
    for i, s in enumerate(shots, 1):
        s["n"] = i
    r["shots"] = shots
    return notes


def _public(d: dict) -> dict:
    return {kk: v for kk, v in (d or {}).items() if not kk.startswith("_") and kk not in ("written_by", "llm_call_id", "input_sha256")}


def recipe_routes(recipe: dict) -> list:
    return sorted({s["route"] for s in recipe.get("shots", [])} - {"END-CARD"})


__all__ = ["direct", "approve", "replan_shot", "founder_confirm", "founder_override", "normalise", "library", "authority", "json"]
