"""The diary writer (spec §3, §4.11, §5, §7.5): cheap AI, run after the job closes — accepted, rejected or abandoned.
It reads the whole job file and the customer's verdict and PROPOSES lessons per worker; each proposal waits in the lesson
queue until the founder approves, edits or rejects it. Nothing is changed here."""
from __future__ import annotations

import json


def job_file(k, job_id: str) -> dict:
    job = k.store.job(job_id)
    recipe = k.store.artifact(job_id, "recipe") or {}
    rej, classes_at, routes_at = {}, {}, {}
    for e in k.store.events(job_id, ("take_rejected",)):
        d = json.loads(e["data_json"])
        key = f"{d.get('node')}|{d.get('action_class')}"          # the class and route AT THE TIME of the rejection
        rej[key] = rej.get(key, 0) + 1
        classes_at[key], routes_at[key] = d.get("action_class"), d.get("route")
    classes, routes = dict(classes_at), dict(routes_at)
    words = [f["text"] for f in k.store.feedback(job_id) if f["kind"] in ("reject", "revision")]
    fr = k.store.artifact(job_id, "final_review") or {}
    return {"job_id": job_id, "title": job["title"], "media": job["media"], "outcome": job["outcome"] or "abandoned",
            "verdict_words": " | ".join(words)[:1000], "product_category": ((k.brief(job_id).get("product") or {}).get("category")),
            "recipe": {kk: recipe.get(kk) for kk in ("proposition", "selected_concept", "customer_summary", "shots")} if recipe else {},
            "recipe_version": len(k.store.artifact_versions(job_id, "recipe")), "taster_rejections": rej, "node_classes": classes,
            "node_routes": routes, "defects": fr.get("defects", []),
            "send_backs": [json.loads(e["data_json"]) for e in k.store.events(job_id, ("send_back",))],
            "overrides": [dict(o) for o in k.store.overrides(job_id)],
            "feasibility_verdict": (k.store.artifact(job_id, "feasibility") or {}).get("verdict"),
            "ledger": k.store.ledger_summary(job_id)}


def write(k, job_id: str) -> list:
    jf = job_file(k, job_id)
    outcome = jf["outcome"] if jf["outcome"] in ("accepted", "rejected") else "abandoned"
    jf["outcome"] = outcome
    with k.store.timed(job_id, "learning", "diary writer"):
        form = k.workers.call(job_id, "diary_writer", "lessons", {"JOB_FILE": jf}, exact_words=k.exact_words(job_id))
    form["outcome"] = outcome                     # the store's outcome, not the model's reading of it
    k.put_form(job_id, "lessons", form)
    ids = k.lessons.enqueue(job_id, form)
    k.store.event(job_id, "diary_writer", "lessons_proposed", {"lessons": ids})
    return ids
