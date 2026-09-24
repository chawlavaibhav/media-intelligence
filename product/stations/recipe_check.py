"""Station 5 — the recipe checker (spec §3, §4.5, §5). Strong AI from another company + binding code rules.

The model judges the recipe against the customer's exact words and predicts acceptance. Code then applies rules the
model cannot talk its way past; any code finding of blocker/major weight forces `send_back`:
  R1  a shot's action (held to its most restrictive class) is `cannot` on its route in the equipment sheet   → blocker
  R2  a shot cites a Feasibility action the pantry marked `cannot` (and the customer did not accept an alternative) → blocker
  R3  a risky shot is not listed in `risks`, or does not start from the master plate (it must be produced first) → major
  R4  film continuity: the first shot must start from the master plate; no shot on a still-only route claims motion → major
  R5  a customer must-have is placed in no shot (films) / the exact copy is missing from the copy deck               → major
  R6  the model's own verdict is send_back, or it predicts `unlikely` acceptance                                      → send_back
"""
from __future__ import annotations

from product import library


def check(k, job_id: str, recipe: dict, tray: dict) -> dict:
    u = k.store.artifact(job_id, "understanding")
    f = k.store.artifact(job_id, "feasibility")
    words = k.exact_words(job_id)
    ctx = {"UNDERSTANDING": _public(u), "FEASIBILITY": {kk: f[kk] for kk in ("actions_needed", "route_verdicts", "alternatives",
                                                                             "reference_risks", "verdict")},
           "RECIPE": _public(recipe)}
    with k.store.timed(job_id, "recipe_check"):
        form = k.workers.call(job_id, "recipe_checker", "recipe_check", ctx, exact_words=words, media=k.photo_media(job_id, 3), tray=tray)
    findings = code_rules(k, recipe, u, f)
    form["code_findings"] = findings
    weighty = [x for x in findings if x["rule"].split(":")[0] in ("R1", "R2", "R3", "R4", "R5")]
    if weighty or form["verdict"] == "send_back" or form["predicted_acceptance"] == "unlikely" \
            or any(i["severity"] in ("blocker", "major") for i in form["issues"]):
        form["verdict_after_code"] = "send_back"
    else:
        form["verdict_after_code"] = form["verdict"]
    return form


def code_rules(k, recipe: dict, u: dict, f: dict) -> list:
    out = []
    eq = k.equipment
    media = u["deliverable"]["media"]
    cannot_actions = {a["id"] for a in f.get("actions_needed", []) if a.get("best_verdict") == "cannot"}
    risk_shots = {r.get("shot") for r in recipe.get("risks", [])}
    shots = [s for s in recipe.get("shots", []) if s.get("route") != "END-CARD"]
    for s in shots:
        cls = library.floor_class(s.get("action", ""), s.get("action_class"))
        if s["route"] == "FILM-A" and s.get("action_class") in ("product_state_still", "camera_move_static_product", "none"):
            cls = s["action_class"]                 # a still with code motion performs no action; its words describe a state
        v = eq.verdict(cls, s["route"])
        where = f"shot {s['n']} ({s['route']}): {s.get('action', '')[:90]}"
        if v["verdict"] == "cannot":
            out.append({"rule": "R1:cannot_on_route", "where": where,
                        "finding": f"{cls} is CANNOT on {s['route']} ({v['row'] or v['why']}); use: {eq.alternative(cls) or 'a still of the state'}"})
        bad_refs = [r for r in s.get("feasibility_refs", []) if r in cannot_actions]
        if bad_refs:
            out.append({"rule": "R2:uses_cannot_action", "where": where, "finding": f"cites Feasibility action(s) {bad_refs} marked cannot"})
        if v["verdict"] == "risky" and media == "video":
            if s["n"] not in risk_shots:
                out.append({"rule": "R3:risky_not_limited", "where": where, "finding": f"{cls} is risky on {s['route']} and is not in risks"})
            if s.get("starts_from") != "master_plate":
                out.append({"rule": "R3:risky_not_first", "where": where,
                            "finding": "a risky shot is produced first, so it must start from the master plate"})
        if s.get("action_class") == "legible_text_on_product":
            out.append({"rule": "R1:lettering_in_picture", "where": where, "finding": "lettering is set by code, never generated"})
    if media == "video" and shots:
        if shots[0].get("starts_from") != "master_plate":
            out.append({"rule": "R4:continuity", "where": f"shot {shots[0]['n']}", "finding": "the first shot must start from the master plate"})
        placed = {m for s in recipe.get("shots", []) for m in s.get("mandatory_ids", [])}
        for m in u.get("mandatory", []):
            if m["id"] not in placed and not m["requirement"].startswith("the exact text"):
                out.append({"rule": "R5:must_have_unplaced", "where": m["id"], "finding": f"'{m['requirement'][:90]}' is placed in no shot"})
    deck = {c["text"] for c in recipe.get("copy_deck", [])}
    order = k.store.artifact(u["job_id"], "order_slip") if u.get("job_id") else None
    for s in (order or {}).get("exact_strings", []):
        if s not in deck:
            out.append({"rule": "R5:exact_copy_missing", "where": "copy deck", "finding": f"the exact string {s!r} is missing"})
    return out


def _public(d: dict) -> dict:
    return {kk: v for kk, v in d.items() if not kk.startswith("_") and kk not in ("written_by", "llm_call_id", "input_sha256")}
