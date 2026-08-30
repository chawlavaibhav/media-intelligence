#!/usr/bin/env python3
"""EVAL-037 — supplemental gates for the CONTROLLED_CANON retrieval treatment.

    python3 validators/validate_controlled_retrieval.py \\
        --lane lanes/sonnet-controlled-canon.yaml --run runs/sonnet-controlled-canon

Runs IN ADDITION to validators/validate_lane_run.py, which is untouched and still owns
every frozen gate (order, retries, repair discipline, usage, cost, Canon transcript,
website, substrate identity). This file only asks the questions the supplemental
treatment adds:

  * did each trial stay inside the retrieval allowance,
  * was the allowance MEASURED rather than enforced,
  * do the recorded numbers actually match the raw tool transcript, and
  * was a violation recorded as `failed_controlled_retrieval` instead of quietly
    repaired, rescued or re-run.

It never re-runs anything and never judges creative quality.
"""
import argparse
import json
import pathlib
import sys

import yaml

HERE = pathlib.Path(__file__).resolve().parent
PKG = HERE.parent
sys.path.insert(0, str(PKG / "tools"))
import controlled_retrieval as CR              # noqa: E402

FAILURES = []
GATES = {"n": 0}
# Statuses that mean the trial produced a package under the treatment and is therefore
# subject to the mechanical compliance check.
SUCCESSFUL = ("complete", "format_repaired")


def gate(name, ok, detail=""):
    GATES["n"] += 1
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))
    if not ok:
        FAILURES.append(name.split()[0])
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--run", required=True)
    a = ap.parse_args()
    lane = yaml.safe_load(pathlib.Path(a.lane).read_text(encoding="utf-8"))
    run = pathlib.Path(a.run)
    result = json.loads((run / "result.json").read_text())
    ledger = json.loads((run / "attempt-ledger.json").read_text())
    print(f"EVAL-037 controlled-retrieval validation — {lane['lane_id']}\n")

    L = CR.LIMITS
    trials = result["trials"]
    lane_allow = lane["retrieval_treatment"]["allowance"]

    # ---- the treatment is declared as a treatment, not a guard -------------
    gate("C0  condition is CONTROLLED_CANON and the lane allowance matches the code",
         result["condition"] == "CONTROLLED_CANON"
         and lane_allow["max_canon_search_calls"] == L["max_canon_search_calls"]
         and lane_allow["max_results_per_search"] == L["max_results_per_search"]
         and lane_allow["max_search_results_total"] == L["max_search_results_total"]
         and lane_allow["max_canon_read_objects"] == L["max_canon_read_objects"]
         and lane["retrieval_treatment"]["enforced_by_harness"] is False)

    gate("C1  every trial carries a controlled_retrieval record, none enforced by the "
         "harness",
         all(isinstance(t.get("controlled_retrieval"), dict)
             and t["controlled_retrieval"]["enforced_by_harness"] is False
             for t in trials))

    # ---- the recorded numbers must come from the raw transcript ------------
    by_trial = {}
    for at in ledger["attempts"]:
        by_trial.setdefault(at["trial_id"], []).extend(at.get("tool_calls") or [])
    recount_ok = True
    for t in trials:
        raw = [tc for tc in by_trial.get(t["trial_id"], [])
               if tc.get("tool_family") == "canon"]
        c = t["controlled_retrieval"]
        recount_ok &= (
            c["canon_search_calls"] == sum(1 for tc in raw if tc["name"] == "canon_search")
            and c["canon_read_calls"] == sum(1 for tc in raw if tc["name"] == "canon_read")
            and c["canon_catalog_calls"] == sum(1 for tc in raw if tc["name"] == "canon_catalog")
            and c["search_results_total"] == sum(tc.get("result_item_count", 0)
                                                 for tc in raw if tc["name"] == "canon_search"))
    gate("C2  recorded retrieval counts recompute from the raw tool transcript",
         recount_ok)

    # ---- MECHANICAL COMPLIANCE, on every successful trial ------------------
    succ = [t for t in trials if t["status"] in SUCCESSFUL]
    c = lambda t: t["controlled_retrieval"]                       # noqa: E731
    gate(f"C3  <= {L['max_canon_search_calls']} canon_search calls per successful trial",
         all(c(t)["canon_search_calls"] <= L["max_canon_search_calls"] for t in succ),
         f"max={max([c(t)['canon_search_calls'] for t in succ], default=0)}")
    gate(f"C4  <= {L['max_results_per_search']} results returned per canon_search",
         all(s["results_returned"] <= L["max_results_per_search"]
             for t in succ for s in c(t)["searches"]),
         f"max={max([s['results_returned'] for t in succ for s in c(t)['searches']], default=0)}")
    gate(f"C5  <= {L['max_search_results_total']} search results exposed per trial",
         all(c(t)["search_results_total"] <= L["max_search_results_total"] for t in succ),
         f"max={max([c(t)['search_results_total'] for t in succ], default=0)}")
    gate(f"C6  <= {L['max_canon_read_objects']} canon_read objects per trial",
         all(c(t)["canon_read_calls"] <= L["max_canon_read_objects"] for t in succ),
         f"max={max([c(t)['canon_read_calls'] for t in succ], default=0)}")

    # ---- a violation is a RESULT, never a repair --------------------------
    viol = [t for t in trials if c(t)["violations"]]
    gate("C7  every trial with a violation is failed_controlled_retrieval and not "
         "eligible",
         all(t["status"] == CR.VIOLATION_STATUS
             and t["eligible_for_media_generation"] is False for t in viol),
         f"{len(viol)} violating trial(s)")
    gate("C8  no successful trial carries a violation (compliance and status agree)",
         all(c(t)["compliant"] for t in succ))
    gate("C9  no trial was re-run for a retrieval violation",
         all(len([at for at in ledger["attempts"]
                  if at["trial_id"] == t["trial_id"] and at["phase"] == "creative"
                  and at["attempt_kind"] == "initial"]) == 1 for t in trials))

    # ---- the harness really did not clamp anything ------------------------
    #  `limit_applied` in the tool's own result must equal what the model asked for.
    clamp_ok, unbounded = True, 0
    for tpath in sorted(run.glob("transcripts/*.jsonl")):
        for line in tpath.read_text().splitlines():
            row = json.loads(line)
            call, full = row.get("call") or {}, row.get("full_result") or {}
            if call.get("name") != "canon_search":
                continue
            asked = (call.get("arguments") or {}).get("limit")
            clamp_ok &= full.get("limit_applied") == asked
            if asked is None:
                unbounded += 1
    gate("C10 the harness applied exactly the model's own `limit` and clamped nothing",
         clamp_ok, f"{unbounded} unbounded search(es) let through unmodified")

    # ---- the model was actually given the controlled addendum -------------
    cond = yaml.safe_load((PKG / lane["condition_detail"]["addendum_path"])
                          .read_text(encoding="utf-8"))
    add = cond["addendum"]
    reqs = sorted(run.glob("requests/*.request.json"))
    gate("C11 every request carried the CONTROLLED_CANON addendum verbatim",
         bool(reqs) and all(add.rstrip("\n") in json.loads(p.read_text()).get("system", "")
                            for p in reqs), f"{len(reqs)} requests")

    # ---- declared needs ---------------------------------------------------
    declared = [t for t in trials if c(t)["declared_knowledge_needs_count"] > 0]
    gate("C12 no trial declared more than three knowledge needs",
         all(c(t)["declared_knowledge_needs_count"] <= lane_allow["max_knowledge_needs"]
             for t in trials),
         f"{len(declared)}/{len(trials)} trials declared needs")

    print()
    if FAILURES:
        print(f"CONTROLLED-RETRIEVAL VALIDATION FAILED — {len(FAILURES)} gate(s): "
              f"{', '.join(FAILURES)}")
        return 1
    print(f"CONTROLLED-RETRIEVAL VALIDATION PASSED — all {GATES['n']} gates green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
