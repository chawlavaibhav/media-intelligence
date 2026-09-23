"""Station 4 — the chef (strongest AI), with the librarian's tray and the recipe checker's binding send-back (spec §3, §4.4,
§4.5, §6.2, §8).

    tray → Recipe → normalise (code) → Recipe check (AI + code rules)
      approve   → quote + sample picture → the customer's plan card (awaiting_approval); while the recipe checker is
                  unqualified its approve is shown as "our reviewer found no problems" (amendment 1 §3)
      add_steps → the chef applies them → checked again            } counted as recipe rounds: 2 per plan cycle, then
      send_back → the chef, with the reasons                      } the SYSTEM applies the pantry checker's safest
                  alternative for the problem shots and checks once more (SB-RECIPE-SAFE); still sent back → the
                  CUSTOMER sees the objections in plain words and chooses go ahead / change the brief / stop (USD 0 spent)
The same station re-plans ONE shot when the small taster rejects it twice (head_cook → replan_shot) and re-plans the
recipe when the big taster says the recipe is wrong (earliest_stage plan).
"""
from __future__ import annotations

import json

import copy
import re

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
        r = k.workers.call(job_id, "chef", "recipe", ctx, exact_words=k.exact_words(job_id), media=k.photo_media(job_id, 3), tray=tray,
                           model_key="chef_image" if u["deliverable"]["media"] == "image" else None)   # amendment 1 §1
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
    cycle = f"cycle{_cycle(k, job_id)}"
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
        try:
            flow.send_back(k.store, job_id, "SB-RECIPE", key=cycle, why=why or verdict)
        except flow.LimitReached:
            return safe_replan(k, job_id, recipe, rc, cycle)          # the system, then the customer — never the founder
        recipe = _chef_call(k, job_id, u, f, {**extra, "RECIPE_CHECK": {kk: rc[kk] for kk in ("verdict_after_code", "issues", "add_steps",
                                                                                               "code_findings", "past_failures_matched")},
                                              "PREVIOUS_RECIPE": _public(recipe)})
    _mark_used(k, job_id)
    after_approved_recipe(k, job_id, recipe, founder=None)


def _cycle(k, job_id) -> int:
    """Each entry into `directing` is a plan cycle with its own two recipe rounds (a customer's change of brief, or the big
    taster's re-plan, starts a new one)."""
    return sum(1 for e in k.store.events(job_id, ("state",)) if json.loads(e["data_json"]).get("to") == "directing")


def _mark_used(k, job_id):
    for kind in ("plan_change", "replan_request"):
        a = k.store.artifact(job_id, kind)
        if a and not a.get("_used"):
            k.store.put_artifact(job_id, kind, {**a, "_used": True}, "system")


def problem_shots(k, recipe: dict, rc: dict) -> list:
    """The shots the recipe checker (model or code) objected to; if it named none, every shot whose action is risky or
    cannot on its route."""
    named = set()
    for x in rc.get("code_findings", []) + rc.get("issues", []):
        for m in re.finditer(r"\bshot (\d+)", str(x.get("where", "")), re.I):
            named.add(int(m.group(1)))
    shots = [s for s in recipe.get("shots", []) if s.get("route") != "END-CARD"]
    if not named:
        for s in shots:
            cls = library.floor_class(s.get("action", ""), s.get("action_class"))
            if k.equipment.verdict(cls, s["route"])["verdict"] in ("risky", "cannot"):
                named.add(s["n"])
    return sorted(n for n in named if any(s["n"] == n for s in shots))


def _safest(k, f: dict, shot: dict) -> str:
    alts = {a["for_action"]: a["alternative"] for a in f.get("alternatives", [])}
    for ref in shot.get("feasibility_refs", []):
        if alts.get(ref):
            return alts[ref]
    cls = library.floor_class(shot.get("action", ""), shot.get("action_class"))
    return k.equipment.alternative(cls) or f"a held still of the moment after: {shot.get('end_state') or shot.get('action', '')}"


def safe_replan(k, job_id, recipe: dict, rc: dict, cycle: str):
    """SB-RECIPE-SAFE (amendment 1 §3): the recipe checker sent the recipe back twice. The system (code, no AI) swaps each
    problem shot for the pantry checker's safest alternative — a still with code motion (FILM-A) — and checks once more.
    Approved → the customer's plan card. Still sent back → the customer sees the objections in plain words and decides."""
    flow.send_back(k.store, job_id, "SB-RECIPE-SAFE", key=cycle, why="two recipe send-backs: the safest alternative for the problem shots")
    u, f = k.store.artifact(job_id, "understanding"), k.store.artifact(job_id, "feasibility")
    problems = problem_shots(k, recipe, rc)
    note = {"from_recipe_version": len(k.store.artifact_versions(job_id, "recipe")), "shots": [], "why": "the recipe checker sent the "
            "recipe back twice; the problem shots now use the safest alternative (a still with code motion)"}
    if problems:
        safe = copy.deepcopy({kk: v for kk, v in recipe.items() if kk not in ("job_id", "form", "form_version", "written_by",
                                                                             "rulebook_card_version", "created_utc", "llm_call_id")})
        for s in safe["shots"]:
            if s["n"] in problems:
                alt = _safest(k, f, s)
                note["shots"].append({"shot": s["n"], "was": {"route": s["route"], "action": s["action"]}, "now": alt})
                s.update(route="FILM-A", action_class="product_state_still", starts_from="master_plate", feasibility_refs=[],
                         action=f"held still: {alt}", end_state=alt)
        safe["risks"] = [r for r in safe.get("risks", []) if r.get("shot") not in problems]
        from product.stations import recipe_check
        rc = recipe_check.check(k, job_id, safe, _tray(k, job_id, u, f, safe, worker="recipe_checker"))
        k.put_form(job_id, "recipe", safe)
        k.put_form(job_id, "recipe_check", rc)
        recipe = safe
    k.store.put_artifact(job_id, "system_replan", {**note, "rechecked": bool(problems), "verdict": rc["verdict_after_code"]}, "system")
    k.store.event(job_id, "system", "system_replan", {"shots": [x["shot"] for x in note["shots"]], "verdict": rc["verdict_after_code"]})
    _mark_used(k, job_id)
    if rc["verdict_after_code"] == "approve":
        return after_approved_recipe(k, job_id, recipe, founder=None)
    objections_to_customer(k, job_id, recipe, rc)


def plain_objections(rc: dict) -> list:
    out = []
    for i in rc.get("issues", []):
        out.append(f"{i.get('where') or 'The plan'}: {i['issue']}" + (f" (suggested: {i['fix']})" if i.get("fix") else ""))
    for x in rc.get("code_findings", []):
        words = re.sub(r"\s*\((?:EQ-|seed|row)[^)]*\)", "", x["finding"]).replace("_", " ").replace("CANNOT", "not something our "
                                                                                                       "video tools can do reliably")
        out.append(f"{x['where'].split(':')[0].capitalize()}: {words}")
    out += [f"Missing step: {a}" for a in rc.get("add_steps", [])]
    return out or ["Our reviewer does not expect this plan to meet your brief."]


def objections_to_customer(k, job_id, recipe, rc):
    """The customer sees the plan with our reviewer's objections in plain words and chooses: go ahead (approve with
    accept_objections), change the brief (request_plan_change), or stop (reject — nothing has been spent on production)."""
    q = cost.quote(k, job_id, recipe)
    k.store.put_artifact(job_id, "quote", q, "system")
    k.store.put_artifact(job_id, "plan_objections", {"recipe_version": len(k.store.artifact_versions(job_id, "recipe")),
                                                     "plain_words": plain_objections(rc), "options": ["go_ahead", "change_brief", "stop"],
                                                     "spent_so_far_usd": money(k.store.committed_usd(job_id))}, "system")
    k.store.put_artifact(job_id, "plan_note", {"text": "Our reviewer still has objections to this plan. Read them below, then go ahead, "
                                                       "change your brief, or stop — nothing has been spent on production.",
                                               "objections": True}, "system")
    k.store.transition(job_id, "directing", "awaiting_approval", actor="system", data={"objections": True})
    k.store.timing_start(job_id, "customer_wait", "approval")


def after_approved_recipe(k, job_id, recipe, founder=None):
    """A recipe the checker approved (or the founder overrode) goes to the customer's plan card. An unqualified checker's
    approve is shown to the customer as "our reviewer found no problems" (amendment 1 §3) — the customer decides."""
    k.store.put_artifact(job_id, "plan_note", {"text": "Our reviewer checked this plan and found no problems." if k.qualified("recipe_checker")
                                               or founder is not None else "Our reviewer found no problems with this plan.",
                                               "objections": False, "reviewer_qualified": k.qualified("recipe_checker")}, "system")
    q = cost.quote(k, job_id, recipe)
    k.store.put_artifact(job_id, "quote", q, "system")
    from product.stations import head_cook
    prev = [a for a in k.store.assets(job_id, role="preview")]
    same_master = prev and json.loads(prev[-1]["meta_json"]).get("master_plate") == recipe.get("master_plate")
    if not same_master:                     # a re-plan that keeps the master plate does not buy a new sample picture
        head_cook.sample_picture(k, job_id, recipe)
    frm = k.store.job(job_id)["state"]
    acct = k.store.account(k.store.job(job_id)["account_id"])
    cap = dec(k.brief(job_id).get("max_budget_usd") or 0)
    if acct["auto_approve"] and cap >= dec(q["recommended_budget_usd"]) and frm == "directing":
        approve(k, job_id, by="auto-approve (account setting)", budget_usd=cap)
        return
    k.store.transition(job_id, frm, "awaiting_approval", actor=founder.actor if founder else "system", founder=founder)
    k.store.timing_start(job_id, "customer_wait", "approval")


def founder_override(k, job_id, proof, reason):
    """Optional founder intervention (never required): override the recipe checker's objections — named and reasoned.
    On a plan card with objections the customer then approves without having to accept them."""
    rc = k.store.artifact(job_id, "recipe_check") or {}
    if rc.get("verdict_after_code") == "approve":
        raise ValueError("the recipe checker approved this recipe; nothing to override")
    k.store.add_override(job_id, kind="recipe_send_back", target=f"recipe v{len(k.store.artifact_versions(job_id, 'recipe'))}",
                         founder=proof, reason=reason, data={"findings": rc.get("code_findings"), "issues": rc.get("issues")})
    if k.store.job(job_id)["state"] == "paused_for_founder":
        k.store.transition(job_id, "paused_for_founder", "directing", actor=proof.actor, founder=proof, data={"reason": "recipe override"},
                           pause_reason=None)
        after_approved_recipe(k, job_id, k.store.artifact(job_id, "recipe"), founder=proof)


def approve(k, job_id, *, by: str, budget_usd, note: str = "", accept_objections: bool = False):
    job = k.store.job(job_id)
    rc = k.store.artifact(job_id, "recipe_check") or {}
    ok = rc.get("verdict_after_code") == "approve" or k.store.overrides(job_id, "recipe_send_back")
    obj = k.store.artifact(job_id, "plan_objections")
    current = bool(obj) and obj["recipe_version"] == len(k.store.artifact_versions(job_id, "recipe"))
    if not ok and current and accept_objections:
        k.store.event(job_id, by, "customer_accepted_objections", {"recipe_version": obj["recipe_version"], "objections": obj["plain_words"]})
    elif not ok and current:
        raise PermissionError("our reviewer has objections to this plan: read them, then go ahead (accepting them), change the brief, or stop")
    elif not ok:
        raise PermissionError("the recipe checker sent this recipe back; it cannot be approved until it is fixed")
    acct = k.store.account(job["account_id"])
    budget = dec(budget_usd)
    if budget > dec(acct["ceiling_usd"]):
        raise PermissionError(f"USD {budget} is above the account ceiling USD {acct['ceiling_usd']}")
    committed = k.store.committed_usd(job_id)
    k._end_wait(job_id, "approval")
    k.store.transition(job_id, ("awaiting_approval", "directing"), "planning", actor=by,
                       data={"budget_usd": money(budget), "note": note, "recipe_version": len(k.store.artifact_versions(job_id, "recipe"))},
                       budget_usd=money(max(budget, committed)), budget_authorised_by=by, budget_authorised_at=utc_now(),
                       approved_at=job["approved_at"] or utc_now())    # the FIRST approval authorised production spend


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
        raise flow.LimitReached("SB-TASTER-REPLAN", f"shot{shot_n}", 1)      # the head cook then switches the shot to FILM-A
    return recipe


def force_still(k, job_id: str, shot_n: int, why: str) -> dict:
    """Amendment 1 §3: the riskiest shot failed after its re-plan — the SYSTEM switches it to FILM-A (a still with code
    motion). A new recipe version records it; the customer's preview notes it; the job continues."""
    old = k.store.artifact(job_id, "recipe")
    recipe = copy.deepcopy({kk: v for kk, v in old.items() if kk not in ("job_id", "form", "form_version", "written_by",
                                                                     "rulebook_card_version", "created_utc", "llm_call_id")})
    s = next(s for s in recipe["shots"] if s["n"] == shot_n)
    was = s["route"]
    s.update(route="FILM-A", action_class="product_state_still", starts_from="master_plate", feasibility_refs=[],
             action=f"held still of: {s['end_state']}")
    recipe["risks"] = [r for r in recipe.get("risks", []) if r.get("shot") != shot_n]
    k.put_form(job_id, "recipe", recipe)
    k.store.event(job_id, "system", "shot_switched_to_still", {"shot": shot_n, "was": was, "why": why[:300]})
    add_customer_note(k, job_id, f"Shot {shot_n}: the moving version did not pass our checks, so this shot is a still picture "
                                 f"with gentle camera motion instead.")
    return recipe


def add_customer_note(k, job_id, text: str):
    """Notes shown with the customer's preview (what the kitchen changed or could not verify on its own)."""
    cur = k.store.artifact(job_id, "customer_notes") or {"notes": []}
    if text not in cur["notes"]:
        k.store.put_artifact(job_id, "customer_notes", {"notes": cur["notes"] + [text]}, "system")


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


__all__ = ["direct", "approve", "replan_shot", "force_still", "safe_replan", "founder_override", "normalise", "library", "authority", "json"]
