"""Station 3 — the pantry and oven checker (spec §3, §4.3, §5, §6.2). NEW in v2.

AI + code. One cheap vision call lists what the order needs from the product (`product_truth`) and from the kitchen
(`actions_needed`). Code then decides everything binding:
  - each action is held to the most restrictive class its words match (a model cannot talk an action out of `cannot`);
  - each action is looked up in the equipment sheet for every route of this media: reliable | risky | cannot;
  - a part/state no photo shows and the customer never stated → `need_input` (the job pauses, USD 0 spent);
  - an action no route can make → `cannot_make`, always with an alternative, back to the customer via the waiter;
  - an infographic photo used as a product reference is flagged with its equipment row.
"""
from __future__ import annotations

from product import flow, library

FILM_ROUTES = ("FILM-A", "FILM-B", "FILM-C")


def check(k, job_id: str):
    u = k.store.artifact(job_id, "understanding")
    job = k.store.job(job_id)
    media = u["deliverable"]["media"]
    routes = FILM_ROUTES if media == "video" else ("IMG",)
    words = k.exact_words(job_id)
    tray = k.librarian.tray(job_id, "pantry_checker", query=words, media=media, account_id=job["account_id"],
                            action_classes=library.classify(words) + ["product_still_from_clean_photo", "product_still_from_infographic_photo"],
                            routes=routes)
    ctx = {"UNDERSTANDING": {kk: u[kk] for kk in ("deliverable", "mandatory", "product", "photo_roles", "accepted_alternatives", "mismatches")},
           "ACTION_CLASSES": [{"id": c["id"], "description": c["description"]} for c in library.yaml.safe_load(
               (library.HERE / "action_classes.yaml").read_text())["classes"]]}
    with k.store.timed(job_id, "feasibility"):
        form = k.workers.call(job_id, "pantry_checker", "feasibility", ctx, exact_words=words, media=k.photo_media(job_id), tray=tray)
    decide(k, form, u, routes)
    k.put_form(job_id, "feasibility", form)
    v = form["verdict"]
    if v in ("need_input", "cannot_make"):
        rule = "SB-PANTRY-NEED-INPUT" if v == "need_input" else "SB-PANTRY-CANNOT"
        flow.send_back(k.store, job_id, rule, why="; ".join(form["ask_customer"])[:500])
        k.store.transition(job_id, "feasibility", "awaiting_customer_input", actor="system",
                           data={"verdict": v, "ask": form["ask_customer"], "alternatives": form["alternatives"]},
                           pause_reason="; ".join(form["ask_customer"])[:300])
        k.store.timing_start(job_id, "customer_wait", "customer_input")
        return
    k.store.transition(job_id, "feasibility", "directing", actor="system", data={"verdict": v})


def decide(k, form: dict, u: dict, routes: tuple):
    """The code half: route verdicts from the equipment sheet, the binding verdict, requests and alternatives."""
    eq = k.equipment
    verdicts, alternatives, asks = [], [], []
    accepted = {x["use"].strip().lower() for x in u.get("accepted_alternatives") or []}
    for a in form["actions_needed"]:
        if a["action"].strip().lower() in accepted:
            # an alternative the customer accepted is a STILL of a state (FILM-A / IMG), never an action — decided by code
            a["action_class"], a["from_alternative"] = "product_state_still", True
        floor = "product_state_still" if a.get("from_alternative") else library.floor_class(a["action"], a.get("action_class"))
        if floor != a.get("action_class"):
            a["model_class"], a["action_class"] = a.get("action_class"), floor
        best = None
        for r in routes:
            v = eq.verdict(a["action_class"], r)
            verdicts.append({"action_id": a["id"], "action_class": a["action_class"], "route": r, "verdict": v["verdict"],
                             "equipment_row": v["row"]})
            if best is None or library.RANK[v["verdict"]] < library.RANK[best["verdict"]]:
                best = v
        a["best_verdict"] = best["verdict"]
        if best["verdict"] == "cannot":
            alt = eq.alternative(a["action_class"]) or "show the result as a still instead of the action"
            alternatives.append({"for_action": a["action"], "alternative": alt})
            asks.append(f"We can't film \"{a['action']}\" reliably yet. We suggest: {alt} Is that all right?")
    missing = [t for t in form["product_truth"] if t["source"] == "none"]
    for t in missing:
        asks.insert(0, f"Please send a photo that shows the {t['part_state']} (or tell us exactly how it looks).")
    risks = []
    for r in u.get("photo_roles", []):
        if r["role"] == "infographic":
            v = eq.verdict("product_still_from_infographic_photo", routes[0] if routes[0] != "FILM-C" else "FILM-A")
            risks.append({"photo": r["photo"], "risk": f"photo {r['photo']} is an annotated infographic ({r['shows'][:80]}); as a "
                                                       f"generator reference it is {v['verdict']}", "equipment_row": v["row"]})
    form["route_verdicts"] = verdicts
    form["alternatives"] = alternatives
    form["ask_customer"] = asks
    form["reference_risks"] = risks
    if missing:
        form["verdict"] = "need_input"
    elif alternatives:
        form["verdict"] = "cannot_make"
    elif any(a["best_verdict"] == "risky" for a in form["actions_needed"]) or risks:
        form["verdict"] = "go_with_limits"
    else:
        form["verdict"] = "go"
    return form
