#!/usr/bin/env python3
"""CANON-V1 — score the value gate from HUMAN verdicts. Corrected per C-C5, C-C6, C-C7.

THIS SCRIPT CONTAINS NO VERDICTS AND CANNOT PRODUCE ONE. It reads a verdicts file written by human
reviewers and aggregates it. No default, no fallback, no imputation. A missing verdict is an error,
never a neutral value. If nobody has reviewed, it says nobody has reviewed.

THREE RULES THE CORRECTION PASS ADDED.

1. TWO INDEPENDENT REVIEWERS PER PAIR (C-C5). Exactly two distinct reviewer ids, or the pair is not
   scored. A pair counts as a clear Canon win only when BOTH reviewers independently satisfy the
   per-reviewer clear-win rule. One clear win plus one non-win is not a win; it is disagreement, and
   it is reported as such. Reviewer judgements are NEVER averaged into a pseudo-continuous number —
   averaging two people's preferences invents a precision neither of them expressed.

2. ONLY COVERAGE PROBES VOTE ON CONTINUATION (C-C6). The early-12 splits into 7 coverage probes and
   5 gap probes, and they answer different questions. A coverage probe asks whether explicit Canon
   beats an independent control WHERE THE CANON ACTUALLY HAS THE KNOWLEDGE. A gap probe asks how far
   general Canon knowledge carries into a known hole. Letting a gap probe vote to stop expansion
   would be perverse: it would use the absence of a source as an argument against acquiring one.
   Gap probes are reported as diagnostics and never move the band.

3. INTENT SAFETY IS GLOBAL. A Canon intent regression on ANY pair — coverage or gap — blocks
   automatic continuation. It is surfaced at the top of the result, not buried in the split.

"5 of 7" is an engineering continuation threshold, not a statistical claim. Seven briefs support a
decision about whether to keep going; they support no rate, no confidence interval and no statement
about briefs outside this set. This script refuses to emit one.

Run: python3 score_value_gate.py [verdicts.json] [--manifest run-manifest.json] [--key key.json]
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent

CLEAR_WIN_MIN_DIMENSIONS = 5   # a majority of the nine creative dimensions
REVIEWERS_REQUIRED = 2

# Frozen before any real output exists (C-C6). Coverage probes only.
COVERAGE_BANDS = [(5, "continue"), (4, "mixed"), (0, "stop")]
DIMENSIONS = [
    "concept_quality", "hierarchy_reasoning", "proposition_clarity", "objective_fit",
    "audience_fit", "visual_temporal_strategy", "trade_off_awareness",
    "contradiction_handling", "appropriate_specificity",
]


def band_for(wins: int, total: int) -> str:
    """Coverage-probe continuation band. Thresholds are absolute counts over 7 coverage probes."""
    if total != 7:
        # The bands were frozen for exactly 7 coverage probes. Do not silently rescale them.
        return "undefined_probe_count"
    for threshold, name in COVERAGE_BANDS:
        if wins >= threshold:
            return name
    return "stop"


def per_reviewer_clear_win(v: dict, mapping: dict) -> tuple[bool, dict]:
    """Does THIS reviewer's judgement satisfy the clear-win rule for the Canon arm?"""
    wins = collections.Counter()
    for d in DIMENSIONS:
        letter = v["dimensions"][d]
        if letter in ("neither", "cannot_tell"):
            continue
        wins[mapping[letter]] += 1
    overall = v["overall"]
    overall_arm = None if overall in ("neither", "cannot_tell") else mapping[overall]
    clear = (wins["oracle_canon"] >= CLEAR_WIN_MIN_DIMENSIONS
             and wins["oracle_canon"] > wins["generic"]
             and overall_arm == "oracle_canon")
    return clear, {"dimension_wins": dict(wins), "overall": overall_arm}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("verdicts", nargs="?", default=str(HERE / "verdicts.json"))
    ap.add_argument("--manifest", default=str(HERE / "run-manifest.json"))
    ap.add_argument("--key", default=str(HERE / "blinding-key.json"))
    args = ap.parse_args()

    path = pathlib.Path(args.verdicts)
    manifest = json.loads(pathlib.Path(args.manifest).read_text())
    early = json.loads((HERE / "early-12-manifest.json").read_text())
    roles = {b["brief_id"]: b["gate_role"] for b in early["briefs"]}

    if not path.exists():
        print(json.dumps({
            "status": "NO_VERDICTS",
            "verdicts_file": str(path),
            "message": "No human verdicts exist. The value gate has not been reviewed. This script "
                       "will not infer, estimate or default a result.",
            "reviewers_required_per_pair": REVIEWERS_REQUIRED,
            "generated_outputs": manifest.get("generated_outputs", 0),
            "expected_outputs": manifest.get("expected_outputs", 24),
        }, indent=2))
        return 0

    key = {k["pair_id"]: k for k in json.loads(pathlib.Path(args.key).read_text())["mapping"]}
    doc = json.loads(path.read_text())
    rows = doc["verdicts"]
    is_dummy = bool(doc.get("dummy"))

    expected = {p["pair_id"] for p in manifest["pairs"]}
    brief_of = {p["pair_id"]: p["brief_id"] for p in manifest["pairs"]}

    errors = []
    by_pair: dict[str, list[dict]] = collections.defaultdict(list)
    for v in rows:
        by_pair[v["pair_id"]].append(v)

    if doc.get("reviewers_required") != REVIEWERS_REQUIRED:
        errors.append(f"verdicts file declares reviewers_required="
                      f"{doc.get('reviewers_required')!r}; this gate requires {REVIEWERS_REQUIRED}")

    for pid in sorted(expected):
        vs = by_pair.get(pid, [])
        if not vs:
            errors.append(f"{pid}: no verdict recorded — a missing verdict is not a tie")
            continue
        ids = [v["reviewer_id"] for v in vs]
        if len(vs) != REVIEWERS_REQUIRED:
            errors.append(f"{pid}: {len(vs)} reviewer verdict(s); exactly "
                          f"{REVIEWERS_REQUIRED} independent reviewers are required")
        if len(set(ids)) != len(ids):
            errors.append(f"{pid}: duplicate reviewer_id {ids} — two verdicts from one reviewer are "
                          f"not two independent reviewers")
        for v in vs:
            for d in DIMENSIONS:
                if d not in v.get("dimensions", {}):
                    errors.append(f"{pid}/{v['reviewer_id']}: dimension {d} not judged")
            ip = v.get("explicit_intent_preservation")
            if not ip or "A" not in ip or "B" not in ip:
                errors.append(f"{pid}/{v['reviewer_id']}: explicit intent preservation not judged "
                              f"for both plans")
    for pid in sorted(set(by_pair) - expected):
        errors.append(f"{pid}: verdict for a pair that is not in the run")

    if errors:
        print(json.dumps({"status": "INCOMPLETE", "error_count": len(errors), "errors": errors},
                         indent=2))
        return 1

    per_pair, disagreements, intent_regressions, intent_violations = [], [], [], []
    intent_tally = collections.Counter()

    for pid in sorted(expected):
        mapping = {"A": key[pid]["A"], "B": key[pid]["B"]}
        vs = sorted(by_pair[pid], key=lambda v: v["reviewer_id"])
        judgements = {}
        clears = []
        for v in vs:
            clear, detail = per_reviewer_clear_win(v, mapping)
            clears.append(clear)
            judgements[v["reviewer_id"]] = {**detail, "canon_clear_win": clear}

        unanimous_win = all(clears)
        disagreed = len(set(clears)) > 1
        if disagreed:
            disagreements.append(pid)

        # Intent is a gate, per plan, per reviewer. Any reviewer seeing Canon degrade or violate
        # where generic preserved is enough to raise it — this is a safety signal, not a vote.
        pair_intent = collections.defaultdict(set)
        regressed = False
        for v in vs:
            for letter in ("A", "B"):
                arm = mapping[letter]
                node = v["explicit_intent_preservation"][letter]
                pair_intent[arm].add(node["verdict"])
                intent_tally[(arm, node["verdict"])] += 1
                for viol in node.get("violations", []):
                    intent_violations.append({"pair_id": pid, "reviewer_id": v["reviewer_id"],
                                              "arm": arm, **viol})
            canon = v["explicit_intent_preservation"]["A" if mapping["A"] == "oracle_canon" else "B"]
            gen = v["explicit_intent_preservation"]["A" if mapping["A"] == "generic" else "B"]
            if canon["verdict"] in ("degraded", "violated") and gen["verdict"] == "preserved":
                regressed = True
        if regressed:
            intent_regressions.append(pid)

        per_pair.append({
            "pair_id": pid, "brief_id": brief_of[pid], "gate_role": roles[brief_of[pid]],
            "reviewers": judgements,
            "unanimous_canon_clear_win": unanimous_win,
            "reviewer_disagreement": disagreed,
            "intent": {arm: sorted(v) for arm, v in pair_intent.items()},
            "canon_intent_regression": regressed,
        })

    coverage = [p for p in per_pair if p["gate_role"] == "coverage_probe"]
    gaps = [p for p in per_pair if p["gate_role"] == "gap_probe"]
    cov_wins = sum(1 for p in coverage if p["unanimous_canon_clear_win"])
    gap_wins = sum(1 for p in gaps if p["unanimous_canon_clear_win"])

    band = band_for(cov_wins, len(coverage))
    if intent_regressions:
        decision = ("BLOCKED PENDING CONTROLLER DIAGNOSIS. The Canon arm degraded or violated "
                    f"explicit customer intent on {len(intent_regressions)} pair(s) where the "
                    "generic arm preserved it. This overrides the coverage band: a Canon that "
                    "overwrites what the customer asked for is not an improvement, however strong "
                    "its creative reasoning. Automatic continuation is blocked.")
        headline = "intent_regression"
    else:
        headline = band
        decision = {
            "continue": "Threshold met on coverage probes. Canon expansion may proceed to "
                        "Controller review.",
            "mixed": "Diagnose before any source expansion.",
            "stop": "Stop source expansion. Diagnose Canon noise, redundancy or over-prescription "
                    "first — adding sources would make an unsynthesised corpus larger, not better.",
            "undefined_probe_count": "The frozen bands assume exactly 7 coverage probes. The probe "
                                     "count differs, so no band is emitted rather than rescaling "
                                     "thresholds after the fact.",
        }[band]

    result = {
        "status": "DUMMY_DRY_RUN_NOT_A_RESULT" if is_dummy else "SCORED",
        "run_id": manifest["run_id"],
        "headline": headline,
        "decision": decision,
        "intent_safety": {
            "canon_intent_regression_pairs": intent_regressions,
            "blocks_automatic_continuation": bool(intent_regressions),
            "note": "Global. Applies to coverage and gap probes alike and is never traded against "
                    "creative quality.",
        },
        "coverage_probes": {
            "counted_toward_continuation": True,
            "total": len(coverage),
            "unanimous_canon_clear_wins": cov_wins,
            "band": band,
            "bands_frozen": {"continue": "5-7 of 7", "mixed": "4 of 7", "stop": "0-3 of 7"},
            "question": "Where the live Canon actually holds relevant accepted knowledge, does "
                        "explicit Canon improve planning beyond an independent generic control?",
        },
        "gap_probes": {
            "counted_toward_continuation": False,
            "total": len(gaps),
            "unanimous_canon_clear_wins": gap_wins,
            "question": "How far does existing general Canon knowledge transfer into a known hole, "
                        "and what failure remains attributable to missing knowledge?",
            "note": "Diagnostic only. A gap probe never votes to stop source acquisition merely "
                    "because the necessary knowledge is absent — that would use the absence of a "
                    "source as an argument against acquiring one.",
        },
        "clear_win_rule": {
            "per_reviewer": f">= {CLEAR_WIN_MIN_DIMENSIONS} of {len(DIMENSIONS)} creative "
                            "dimensions AND more than the other arm AND the overall preference",
            "per_pair": "BOTH reviewers must independently satisfy the per-reviewer rule. "
                        "Disagreement, cannot_tell, or one clear win plus one non-win is not a "
                        "pair win.",
            "no_averaging": "Reviewer judgements are not averaged. Averaging two preferences "
                            "invents a precision neither reviewer expressed.",
        },
        "reviewer_disagreement_pairs": disagreements,
        "explicit_intent_tally": {f"{a}:{v}": c for (a, v), c in sorted(intent_tally.items())},
        "intent_violations": intent_violations,
        "per_pair": per_pair,
        "statistical_note": "Engineering continuation gate over 7 coverage probes. NOT a population "
                            "estimate. No rate, proportion or confidence interval derived from "
                            "these describes any wider set of briefs, and none is emitted here. "
                            "Independence across briefs is not established.",
    }
    if is_dummy:
        result["warning"] = ("Input was flagged dummy. These numbers are a pipeline check on "
                            "synthetic labels and are not evidence about Canon.")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
