#!/usr/bin/env python3
"""CANON-V1 / C3 — score the value gate from HUMAN verdicts.

THIS SCRIPT CONTAINS NO VERDICTS AND CANNOT PRODUCE ONE. It reads a verdicts file written by human
reviewers and aggregates it. There is no default, no fallback, no imputation and no "unknown means
tie" rule. A missing verdict is an error, not a neutral value. If nobody has reviewed, this script
reports that nobody has reviewed.

That is not caution for its own sake. The project has already recorded what happens when a
convenient default fills a gap: a validator that returned early on a parse error under-reported, and
the shortfall was invisible in its own output.

TWO RULES ABOUT THE NUMBERS.

1. Explicit-intent preservation is a GATE, not a score. It is judged per plan and never averaged
   into creative quality. A plan that drops a client's stated requirement has failed at the thing the
   client actually asked for, however good its concept is.

2. "9 of 12" is an engineering continuation threshold, not a statistical claim. Twelve briefs
   support a decision about whether to keep going. They support no rate, no confidence interval and
   no statement about briefs outside this set. This script refuses to emit one.

Run: python3 canon/experiments/v1/value-gate/score_value_gate.py [verdicts.json]
"""
from __future__ import annotations

import collections
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
MANIFEST = HERE / "run-manifest.json"
KEY = HERE / "blinding-key.json"

CLEAR_WIN_MIN_DIMENSIONS = 5  # a "clear win" needs a majority of the 9 creative dimensions


def unblind(verdict_letter: str, mapping: dict) -> str | None:
    """Turn a blinded A/B letter into an arm name. Returns None for non-preferences."""
    if verdict_letter in ("neither", "cannot_tell"):
        return None
    return mapping[verdict_letter]


def main() -> int:
    path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "verdicts.json"
    manifest = json.loads(MANIFEST.read_text())
    dims = manifest["review_dimensions"]

    if not path.exists():
        print(json.dumps({
            "status": "NO_VERDICTS",
            "verdicts_file": str(path),
            "message": "No human verdicts exist. The value gate has not been reviewed. "
                       "This script will not infer, estimate or default a result.",
            "generated_outputs": manifest["generated_outputs"],
            "expected_outputs": manifest["expected_outputs"],
        }, indent=2))
        return 0

    key = {k["pair_id"]: k for k in json.loads(KEY.read_text())["mapping"]}
    verdicts = json.loads(path.read_text())
    rows = verdicts["verdicts"]
    is_dummy = bool(verdicts.get("dummy"))

    errors = []
    seen = {v["pair_id"] for v in rows}
    expected = {p["pair_id"] for p in manifest["pairs"]}
    for missing in sorted(expected - seen):
        errors.append(f"{missing}: no verdict recorded — a missing verdict is not a tie")
    for extra in sorted(seen - expected):
        errors.append(f"{extra}: verdict for a pair that is not in the run")
    for v in rows:
        for d in dims:
            if d not in v.get("dimensions", {}):
                errors.append(f"{v['pair_id']}: dimension {d} not judged")
        ip = v.get("explicit_intent_preservation")
        if not ip or "A" not in ip or "B" not in ip:
            errors.append(f"{v['pair_id']}: explicit intent preservation not judged for both plans")
    if errors:
        print(json.dumps({"status": "INCOMPLETE", "error_count": len(errors),
                          "errors": errors}, indent=2))
        return 1

    per_pair, dim_tally = [], {d: collections.Counter() for d in dims}
    intent = collections.Counter()
    intent_violations = []
    for v in rows:
        pid = v["pair_id"]
        mapping = {"A": key[pid]["A"], "B": key[pid]["B"]}
        wins = collections.Counter()
        for d in dims:
            arm = unblind(v["dimensions"][d], mapping)
            dim_tally[d][arm or "no_preference"] += 1
            if arm:
                wins[arm] += 1
        overall = unblind(v["overall"], mapping)
        canon_clear = wins["oracle_canon"] >= CLEAR_WIN_MIN_DIMENSIONS and \
            wins["oracle_canon"] > wins["generic"] and overall == "oracle_canon"
        pair_intent = {}
        for letter in ("A", "B"):
            arm = mapping[letter]
            node = v["explicit_intent_preservation"][letter]
            pair_intent[arm] = node["verdict"]
            intent[(arm, node["verdict"])] += 1
            for viol in node.get("violations", []):
                intent_violations.append({"pair_id": pid, "arm": arm, **viol})
        per_pair.append({
            "pair_id": pid, "brief_id": key[pid]["brief_id"],
            "dimension_wins": dict(wins), "overall": overall,
            "canon_clear_win": canon_clear, "intent": pair_intent,
        })

    canon_wins = sum(1 for p in per_pair if p["canon_clear_win"])
    n = len(per_pair)
    regressions = [p for p in per_pair
                   if p["intent"].get("oracle_canon") in ("degraded", "violated")
                   and p["intent"].get("generic") == "preserved"]

    if regressions:
        band, decision = "intent_regression", (
            f"Canon degraded or violated explicit client intent on {len(regressions)} pair(s) where "
            "the generic arm preserved it. This overrides the win count: a Canon that overwrites what "
            "the customer asked for is not an improvement, however strong its creative reasoning.")
    elif canon_wins >= 9:
        band, decision = "continue", "Threshold met. Canon expansion may proceed to Controller review."
    elif canon_wins >= 7:
        band, decision = "mixed", "Diagnose before any source expansion."
    else:
        band, decision = "stop", (
            "Stop source expansion. Diagnose Canon noise, redundancy or over-prescription first — "
            "adding sources would make an unsynthesised corpus larger, not better.")

    result = {
        "status": "DUMMY_DRY_RUN_NOT_A_RESULT" if is_dummy else "SCORED",
        "run_id": manifest["run_id"],
        "pairs_reviewed": n,
        "canon_clear_wins": canon_wins,
        "clear_win_rule": f">= {CLEAR_WIN_MIN_DIMENSIONS} of {len(dims)} creative dimensions AND "
                          "more than the other arm AND the overall preference",
        "gate_band": band,
        "decision": decision,
        "explicit_intent": {f"{a}:{v}": c for (a, v), c in sorted(intent.items())},
        "intent_regressions_vs_generic": [p["pair_id"] for p in regressions],
        "intent_violations": intent_violations,
        "dimension_tally": {d: dict(c) for d, c in dim_tally.items()},
        "per_pair": per_pair,
        "statistical_note": "This is an engineering continuation gate over 12 briefs. It is NOT a "
                            "population estimate. No rate, proportion or confidence interval derived "
                            "from these 12 describes any wider set of briefs, and none is emitted "
                            "here. Independence across briefs is not established.",
    }
    if is_dummy:
        result["warning"] = ("Input was flagged dummy. These numbers are a pipeline check on "
                            "synthetic labels and are not evidence about Canon.")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
