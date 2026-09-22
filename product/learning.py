"""Production memory: metrics from the store and the production-learning case skeleton.

Metrics are mechanical (store timestamps), never estimated. Elapsed time is the UNION of intervals, so
concurrent work is not double-counted; accumulated time is the SUM. Customer waiting is its own phase.

The case skeleton follows PRODUCTION-LEARNING-CASE-v0 (production-learning/tools/check_case.py) and is
written under <data>/cases/<job>/ — customer material never enters the repository. Nothing here promotes
anything: ROUTE-OBSERVATIONS carry routing_authority none, and the PROMOTION-QUEUE is left for /media-agency-sync
and the Controller.
"""
from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import yaml

from product.store import Store, dec, money


def _union(intervals) -> float:
    iv = sorted((a, b) for a, b in intervals if b is not None and b >= a)
    total, cur = 0.0, None
    for a, b in iv:
        if cur is None or a > cur[1]:
            if cur:
                total += cur[1] - cur[0]
            cur = [a, b]
        else:
            cur[1] = max(cur[1], b)
    if cur:
        total += cur[1] - cur[0]
    return total


def _t(utc: str | None) -> float | None:
    if not utc:
        return None
    return datetime.strptime(utc, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc).timestamp()


def metrics(store: Store, job_id: str) -> dict:
    job = store.job(job_id)
    by_phase = defaultdict(list)
    for t in store.timings(job_id):
        by_phase[t["phase"]].append((t["started"], t["ended"]))
    phases = {p: {"elapsed_s": round(_union(iv), 2), "accumulated_s": round(sum((b or a) - a for a, b in iv), 2), "spans": len(iv)}
              for p, iv in by_phase.items()}
    active = [iv for p, ivs in by_phase.items() if p != "customer_wait" for iv in ivs]
    created, approved, first_cut = _t(job["created"]), _t(job["approved_at"]), _t(job["first_cut_at"])
    closed = _t(job["closed_at"])
    led = store.ledger_summary(job_id)
    provider = [a for a in store.attempts(job_id) if a["category"] == "provider"]
    out = {
        "job_id": job_id, "state": job["state"], "outcome": job["outcome"],
        "phases": phases,
        "active_elapsed_s": round(_union(active), 2),
        "active_accumulated_s": round(sum((b or a) - a for a, b in active), 2),
        "customer_wait_s": phases.get("customer_wait", {}).get("elapsed_s", 0.0),
        "provider_elapsed_s": phases.get("provider", {}).get("elapsed_s", 0.0),
        "first_cut_latency_s": round(first_cut - approved, 2) if (first_cut and approved) else None,
        "first_cut_latency_basis": "approved_at → first assembled/composed cut (store stamps)",
        "time_to_outcome_s": round(closed - created, 2) if (closed and created) else None,
        "cost": {**led, "provider_attempts": len(provider), "failed_attempts": sum(a["status"] == "failed" for a in provider)},
        "cuts_presented": len([e for e in store.events(job_id, ("state",)) if json.loads(e["data_json"]).get("to") == "ready_for_review"]),
    }
    delivered = store.deliveries(job_id)
    out["cost_per_accepted_outcome_usd"] = (money(dec(led["committed_usd"]) / len(delivered)) if (delivered and job["outcome"] == "accepted") else None)
    return out


def write_case(store: Store, job_id: str, root: Path | None = None) -> Path:
    job = store.job(job_id)
    from product import config
    root = root or (Path(store.db_path).parent / "cases")
    d = root / job_id
    d.mkdir(parents=True, exist_ok=True)
    m = metrics(store, job_id)
    delivered = store.deliveries(job_id)
    final = store.asset(delivered[-1]["asset_id"]) if delivered else None
    cuts = _cuts(store, job_id)
    versions = [c["version"] for c in cuts]
    accepted_by = next((c["decided_by"] for c in cuts if c["verdict"] == "accept"), None)
    outcome = {"case_id": job_id, "class": f"P1-{'VIDEO' if job['media'] == 'video' else 'IMG'} product job",
               "final_outcome": job["outcome"] if job["outcome"] in ("accepted", "rejected") else "abandoned",
               "not_evidence_for": ["routing authority (directional only)", "any other brand, product or brief"],
               "versions_produced": [{"version": c["version"], "asset_sha256": c["sha256"]} for c in cuts],
               "two_conclusions": {"final_quality": "PENDING REVIEW — stated by the case reviewer, not by the product",
                                   "pipeline_efficiency_time_to_accepted_outcome": f"mechanical: {m['time_to_outcome_s']} s; "
                                   f"first-cut latency {m['first_cut_latency_s']} s"}}
    if job["outcome"] == "accepted" and final:
        outcome.update(final_asset={"path": final["path"], "commit": "0000000", "sha256": final["sha256"],
                                    "note": "customer data store, not git (commit field is a placeholder required by the schema)"},
                       accepted_version=f"cut{final['cut']}", accepted_by=accepted_by, template_status="none")
    else:
        outcome["final_outcome_reason"] = job["pause_reason"] or job["outcome"] or "not accepted"
    provider = float(dec(m["cost"]["by_category"].get("provider", 0)))
    files = {
        "OUTCOME.yaml": outcome,
        "TIME-AND-COST.yaml": {
            "case_id": job_id,
            "time": {("time_to_accepted_outcome_mechanical" if job["outcome"] == "accepted" else "time_to_outcome_mechanical"):
                     ({"value_s": m["time_to_outcome_s"], "source": "product store: jobs.created -> jobs.closed_at"}
                      if m["time_to_outcome_s"] is not None else {"value": None, "reason": "job not closed"}),
                     "first_cut_latency_s": m["first_cut_latency_s"], "active_elapsed_s": m["active_elapsed_s"],
                     "active_accumulated_s": m["active_accumulated_s"], "customer_wait_s": m["customer_wait_s"], "phases": m["phases"]},
            "cost": {"total_known_provider_cost_usd": provider,
                     "reasoning_cost_usd": float(dec(m["cost"]["by_category"].get("reasoning", 0))),
                     "repair_cost_usd": float(dec(m["cost"]["repair_usd"])),
                     **({"cost_per_accepted_outcome": {"value": float(dec(m["cost"]["committed_usd"])), "numerator_complete": False,
                                                       "missing_components": ["human time"]}} if job["outcome"] == "accepted" else {})},
            "counts": {"paid_generation_attempts": m["cost"]["provider_attempts"], "human_review_cycles": len(cuts)},
            "product_conclusion": {"final_quality": "PENDING REVIEW", "pipeline_efficiency": "PENDING REVIEW"},
        },
        "HUMAN-VERDICTS.yaml": {"case_id": job_id, "evidence_class": "file_backed_human_evidence",
                                "verdicts": [{"version": c["version"], "verdict": c["verdict"], "by": c["decided_by"], "utc": c["decided_utc"],
                                              "feedback_verbatim": c["feedback"]} for c in cuts]},
        "REVISION-TRACE.yaml": {"case_id": job_id, "versions": [
            {"version": c["version"], "input_source": "product store", "generation_status": "complete", "assembly_status": "complete",
             "human_verdict": c["verdict"], "defects": [], "repair_succeeded": c["verdict"] == "accept" if c["version"] != "cut1" else "n-a",
             "cost_usd": c["cost_usd"], "elapsed": {"value_s": c["elapsed_s"], "source": "product store timings"}} for c in cuts],
            "note": "root_cause_class per defect is assigned by the case reviewer (the eleven classes), not by the product"},
        "ROUTE-OBSERVATIONS.yaml": {"case_id": job_id, "observations": [
            {"id": f"RO-{i + 1}", "route": r, "n": n, "evidence_class": "directional_production_observation", "routing_authority": "none",
             "context": f"{job_id} ({job['media']})"} for i, (r, n) in enumerate(_route_counts(store, job_id).items())]},
        "SYSTEM-DEFECTS.yaml": {"case_id": job_id, "classes": {
            "media_model_failure": "the generation model produced something that does not meet the brief",
            "pipeline_failure": "the system around the model let a defect through or created one",
            "infrastructure_transient": "provider unavailable / refusal / quota"},
            "defects": _defects(store, job_id)},
        "PROMOTION-QUEUE.yaml": {"case_id": job_id, "promoted_now": [], "candidate_patterns": [], "directional_only": [], "not_promoted": []},
    }
    for name, data in files.items():
        (d / name).write_text(f"# GENERATED from the product store for {job_id}; nothing here is promoted automatically.\n"
                              + yaml.safe_dump(data, sort_keys=False, allow_unicode=True))
    rows = [f"| `{a['path']}` | not-in-git | `{a['sha256']}` | {a['source']} {a['kind']} |" for a in store.assets(job_id)]
    (d / "EVIDENCE-MAP.md").write_text("# EVIDENCE MAP (generated)\n\n| path | commit | sha256 | what |\n|---|---|---|---|\n" + "\n".join(rows) + "\n")
    (d / "README.md").write_text(f"# Case {job_id}\n\nGenerated by product/learning.py from the P1 store. Review, then run /media-agency-sync.\n")
    (d / "metrics.json").write_text(json.dumps(m, indent=1, default=str))
    return d


def _cuts(store, job_id) -> list:
    """One entry per cut shown to the customer, with the customer's decision on it."""
    evs = store.events(job_id, ("state",))
    out, cur = [], None
    for e in evs:
        d = json.loads(e["data_json"])
        if d.get("to") == "ready_for_review":
            finals = [n["selected_asset_id"] for n in store.nodes(job_id) if n["kind"] in ("compose_still", "assemble")]
            cur = {"version": f"cut{len(out) + 1}", "presented_utc": e["utc"], "verdict": None, "decided_by": None, "decided_utc": None,
                   "feedback": [], "sha256": None, "cost_usd": 0.0, "elapsed_s": None}
            out.append(cur)
        elif cur and d.get("from") == "ready_for_review":
            cur["verdict"] = {"accepted": "accept", "revising": "specific_repair", "directing": "rebuild_direction",
                              "rejected": "reject"}.get(d.get("to"), "reject")
            cur["decided_by"], cur["decided_utc"] = e["actor"], e["utc"]
            cur["elapsed_s"] = round(_t(e["utc"]) - _t(cur["presented_utc"]), 2)
    fb = store.feedback(job_id)
    deliverables = [a for a in store.assets(job_id) if a["role"] == "deliverable"]
    for i, c in enumerate(out):
        mine = [a for a in deliverables if a["cut"] == i + 1]
        c["sha256"] = mine[-1]["sha256"] if mine else None
        c["feedback"] = [{"target": f["target"], "text": f["text"], "kind": f["kind"]} for f in fb
                         if c["decided_utc"] and f["created"] <= c["decided_utc"] and (i == 0 or f["created"] > out[i - 1]["decided_utc"])]
        c["verdict"] = c["verdict"] or "reject"
    return out


def _defects(store, job_id) -> list:
    out = []
    for a in store.attempts(job_id):
        if a["status"] in ("failed", "uncertain"):
            out.append({"id": f"ATT-{a['seq']}", "class": "infrastructure_transient" if a["failure_class"] in
                        ("infrastructure_transient", "provider_refusal", "interrupted_uncertain") else "pipeline_failure",
                        "subsystem": f"provider ({a['route']})", "observed": (a["detail"] or "")[:300], "found_by": "dispatcher",
                        "root_cause": a["failure_class"] or "unclassified", "repaired": "n-a", "promoted_as": None})
    for e in store.events(job_id, ("asset_rejected", "take_rejected")):
        d = json.loads(e["data_json"])
        out.append({"id": f"INSP-{e['id']}", "class": "media_model_failure", "subsystem": f"generation ({d.get('node')})",
                    "observed": (d.get("why") or d.get("det") or "")[:300], "found_by": "independent inspector / deterministic check",
                    "root_cause": "to be assigned by the case reviewer", "repaired": True, "promoted_as": None})
    for v, r in enumerate([store.artifact(job_id, "review", x["version"]) for x in store.artifact_versions(job_id, "review")], 1):
        for d in (r or {}).get("defects", []):
            out.append({"id": f"REV{v}-{d.get('id')}", "class": "media_model_failure" if d.get("earliest_stage") in ("generation", "reference")
                        else "pipeline_failure", "subsystem": f"{d.get('earliest_stage')} ({d.get('where')})",
                        "observed": d.get("description", "")[:300], "found_by": "independent reviewer",
                        "root_cause": d.get("earliest_stage") or "unknown", "repaired": "see REVISION-TRACE",
                        "promoted_as": None})
    return out


def _route_counts(store, job_id):
    out = defaultdict(int)
    for a in store.attempts(job_id):
        out[a["route"]] += 1
    return dict(out)
