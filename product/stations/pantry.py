"""Station 3 — the pantry and oven checker (spec §3, §4.3, §5, §6.2). NEW in v2.

AI + code. One cheap vision call lists what the order needs from the product (`product_truth`) and from the kitchen
(`actions_needed`). Code then decides everything binding:
  - each action is held to the most restrictive class its words match (a model cannot talk an action out of `cannot`);
  - each action is looked up in the equipment sheet for every route of this media: reliable | risky | cannot;
  - a part/state no photo shows and the customer never stated → `need_input` (the job pauses, USD 0 spent);
  - an action no route can make → `cannot_make`, always with an alternative, back to the customer via the waiter;
  - an infographic photo used as a product reference is flagged with its equipment row;
  - an alternative the customer accepted sticks for every later round, matched by the action CLASS it replaces (the
    model rewords its actions every round, so exact wording can never be relied on);
  - loop guard: the same ask is never sent to the customer twice for one job. A `cannot` action whose alternative was
    already offered gets that alternative applied by the system (amendment 1 §3: nobody waits); a part/state already
    requested is carried as a stated limit instead of being asked again.
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
    # the customer's own accepted alternatives (as clicked, with the class they replace) count alongside the waiter's copy,
    # which a model may have reworded
    cinput = k.store.artifact(job_id, "customer_input") or {}
    ud = {**u, "accepted_alternatives": list(u.get("accepted_alternatives") or []) + list(cinput.get("accepted_alternatives") or [])}
    decide(k, form, ud, routes, already_asked=asked_before(k, job_id))
    k.put_form(job_id, "feasibility", form)
    if form.get("loop_guard"):
        k.store.event(job_id, "system", "pantry_loop_guard", {"applied": form["loop_guard"]})
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


def _truth_key(part_state: str) -> str:
    return "truth:" + " ".join(sorted(set(library.words(part_state))))


def _alt_class(x: dict) -> str:
    """The action class an alternative stands in for: carried on the alternative, else re-derived from its words."""
    return x.get("action_class") or library.floor_class(x.get("instead_of") or x.get("for_action") or "", None)


def asked_before(k, job_id: str) -> set:
    """Every ask already sent to the customer on this job: `class:<action class>` for each cannot-alternative offered,
    `truth:<words>` for each part/state requested, and the exact ask sentences. Read from the earlier feasibility forms
    whose verdict paused the job for the customer (those asks were shown to them)."""
    out = set()
    for row in k.store.artifact_versions(job_id, "feasibility"):
        f = k.store.artifact(job_id, "feasibility", row["version"]) or {}
        if f.get("verdict") not in ("need_input", "cannot_make"):
            continue
        out.update(f.get("ask_customer") or [])
        out.update("class:" + _alt_class(x) for x in f.get("alternatives") or [])
        out.update(_truth_key(t["part_state"]) for t in f.get("product_truth") or [] if t.get("source") == "none")
    return out


def decide(k, form: dict, u: dict, routes: tuple, already_asked: set | frozenset = frozenset()):
    """The code half: route verdicts from the equipment sheet, the binding verdict, requests and alternatives."""
    eq = k.equipment
    verdicts, alternatives, asks, guard, limits = [], [], [], [], []
    accepted_alts = u.get("accepted_alternatives") or []
    accepted = {x["use"].strip().lower() for x in accepted_alts}
    by_text = {(x.get("instead_of") or "").strip().lower(): x["use"] for x in accepted_alts if x.get("instead_of")}
    by_class = {}
    for x in accepted_alts:
        by_class.setdefault(_alt_class(x), x["use"])

    def best_of(cls):
        best, rows = None, []
        for r in routes:
            v = eq.verdict(cls, r)
            rows.append((r, v))
            if best is None or library.RANK[v["verdict"]] < library.RANK[best["verdict"]]:
                best = v
        return best, rows

    for a in form["actions_needed"]:
        if a["action"].strip().lower() in accepted:
            # an alternative the customer accepted is a STILL of a state (FILM-A / IMG), never an action — decided by code
            a["action_class"], a["from_alternative"] = "product_state_still", True
        floor = "product_state_still" if a.get("from_alternative") else library.floor_class(a["action"], a.get("action_class"))
        if floor != a.get("action_class"):
            a["model_class"], a["action_class"] = a.get("action_class"), floor
        best, rows = best_of(a["action_class"])
        if best["verdict"] == "cannot":
            key = a["action"].strip().lower()
            use = by_text.get(key) or by_class.get(a["action_class"])
            how = "customer_accepted"
            if use is None and "class:" + a["action_class"] in already_asked:
                # loop guard: this alternative was already offered once; the system applies it rather than ask again
                use = eq.alternative(a["action_class"]) or "show the result as a still instead of the action"
                how = "system_applied_after_asking_once"
            if use is not None:
                a.update({"instead_of": a["action"], "replaced_class": a["action_class"], "action": use,
                          "action_class": "product_state_still", "from_alternative": True, "alternative_by": how})
                if how != "customer_accepted":
                    guard.append({"action_id": a["id"], "instead_of": a["instead_of"], "use": use, "class": a["replaced_class"]})
                best, rows = best_of("product_state_still")
        for r, v in rows:
            verdicts.append({"action_id": a["id"], "action_class": a["action_class"], "route": r, "verdict": v["verdict"],
                             "equipment_row": v["row"]})
        a["best_verdict"] = best["verdict"]
        if best["verdict"] == "cannot":
            alt = eq.alternative(a["action_class"]) or "show the result as a still instead of the action"
            alternatives.append({"for_action": a["action"], "alternative": alt, "action_class": a["action_class"]})
            asks.append(f"We can't film \"{a['action']}\" reliably yet. We suggest: {alt} Is that all right?")
    missing = []
    for t in form["product_truth"]:
        if t["source"] != "none":
            continue
        if _truth_key(t["part_state"]) in already_asked:
            # loop guard: already requested once and the customer has answered — carry it as a limit, never ask again
            limits.append(f"no photo or fact shows the {t['part_state']}; it will not be shown as a product detail")
            guard.append({"truth": t["part_state"], "limit": limits[-1]})
            continue
        missing.append(t)
    for t in missing:
        asks.insert(0, f"Please send a photo that shows the {t['part_state']} (or tell us exactly how it looks).")
    asks = [x for x in dict.fromkeys(asks) if x not in already_asked]
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
    form["limits"] = limits
    form["loop_guard"] = guard
    if missing and asks:
        form["verdict"] = "need_input"
    elif alternatives and asks:
        form["verdict"] = "cannot_make"
    elif any(a["best_verdict"] in ("risky", "cannot") for a in form["actions_needed"]) or risks or limits:
        form["verdict"] = "go_with_limits"
    else:
        form["verdict"] = "go"
    return form
