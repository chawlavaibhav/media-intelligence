#!/usr/bin/env python3
"""CANON-V1 / C3 — build the generic contexts, the blinded run manifest and the reviewer packet.

THREE JOBS, ALL ABOUT NOT FOOLING OURSELVES.

1. LENGTH MATCHING. It renders the generic contexts and refuses to continue if any generic context
   differs from its paired oracle context by more than the tolerance. Giving the Canon arm more words
   is the easiest way to manufacture a win, and it would be invisible in the results.

2. BLINDING. It assigns each pair a randomised A/B presentation order from a FIXED seed, writes the
   reviewer packet with arms stripped, and writes the arm mapping to a separate sealed key file that
   the reviewer never receives.

3. FROZEN BEFORE GENERATION. Prompts are hashed here, so a prompt edited after generation is
   detectable rather than merely regrettable.

The randomisation seed is fixed and committed. That is deliberate: a reproducible shuffle can be
re-derived and audited later, where an unseeded one cannot. It is not secret and does not need to be
— the reviewer never sees this file, and knowing the seed without the key reveals nothing.

Run: python3 canon/experiments/v1/value-gate/build_run_manifest.py
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import random
import sys

import yaml

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
GEN_SRC = HERE / "generic-source.yaml"
GEN_DIR = HERE / "generic-contexts"
ORA_DIR = HERE / "oracle-contexts"
MANIFEST = HERE / "early-12-manifest.json"
PROMPT = HERE / "prompts/planning-prompt.md"
BRIEFS = ROOT / "canon/experiments/v1/brief-bank/briefs.jsonl"

RUN_ID = "CANON-V1-GATE-001"
SEED = 20260826
TOLERANCE = 0.15

DIMENSIONS = [
    "concept_quality", "hierarchy_reasoning", "proposition_clarity", "objective_fit",
    "audience_fit", "visual_temporal_strategy", "trade_off_awareness",
    "contradiction_handling", "appropriate_specificity",
]
GATING_DIMENSION = "explicit_intent_preservation"


def words(t: str) -> int:
    return len(t.split())


def main() -> int:
    gen = {c["brief_id"]: c["body"] for c in yaml.safe_load(GEN_SRC.read_text())["contexts"]}
    manifest = json.loads(MANIFEST.read_text())
    briefs = {json.loads(l)["brief_id"]: json.loads(l) for l in BRIEFS.read_text().splitlines()}
    ids = [b["brief_id"] for b in manifest["briefs"]]

    errors = []
    if sorted(gen) != sorted(ids):
        errors.append(f"generic contexts {sorted(gen)} do not match the early-12 {sorted(ids)}")

    GEN_DIR.mkdir(parents=True, exist_ok=True)
    pairs_len = []
    for bid in ids:
        if bid not in gen:
            continue
        body = gen[bid]
        (GEN_DIR / f"{bid}.md").write_text(body)
        gw = words(body)
        ow = words((ORA_DIR / f"{bid}.md").read_text())
        drift = abs(gw - ow) / ow
        pairs_len.append({"brief_id": bid, "generic_words": gw, "oracle_words": ow,
                          "drift": round(drift, 4)})
        if drift > TOLERANCE:
            errors.append(
                f"{bid}: generic {gw} words vs oracle {ow} words, drift {drift:.1%} exceeds "
                f"{TOLERANCE:.0%} — the arms are not length-matched")

    if errors:
        print(json.dumps({"error_count": len(errors), "errors": errors,
                          "length_pairs": pairs_len}, indent=2))
        return 1

    prompt_hash = hashlib.sha256(PROMPT.read_bytes()).hexdigest()
    rng = random.Random(SEED)
    order = list(ids)
    rng.shuffle(order)

    # BALANCED A/B assignment, not per-pair coin flips. An unconstrained shuffle put the Canon arm
    # in position A for 9 of 12 pairs on this seed. Reviewers show real order effects, so that would
    # have been a systematic advantage to one arm, invisible in the results. Exactly half the pairs
    # present each arm first.
    a_side = ["generic"] * (len(order) // 2) + ["oracle_canon"] * (len(order) - len(order) // 2)
    rng.shuffle(a_side)

    run, key, packet = [], [], []
    for i, bid in enumerate(order, 1):
        pair_id = f"PAIR-{i:02d}"
        a_arm = a_side[i - 1]
        b_arm = "oracle_canon" if a_arm == "generic" else "generic"
        run.append({
            "pair_id": pair_id, "brief_id": bid,
            "outputs": [
                {"output_id": f"OUT-{2*i-1:03d}", "arm": "generic",
                 "context_file": f"generic-contexts/{bid}.md"},
                {"output_id": f"OUT-{2*i:03d}", "arm": "oracle_canon",
                 "context_file": f"oracle-contexts/{bid}.md"},
            ],
        })
        key.append({"pair_id": pair_id, "brief_id": bid, "A": a_arm, "B": b_arm})
        packet.append({
            "pair_id": pair_id,
            "customer_brief": briefs[bid]["customer_brief"],
            "plan_A": "<<PLAN TEXT — not generated>>",
            "plan_B": "<<PLAN TEXT — not generated>>",
            "instructions": (
                "Read the client brief, then both plans. For each dimension choose the plan that "
                "does it better, or 'neither' if they are equivalent, or 'cannot_tell'. Then judge "
                "explicit intent preservation for EACH plan separately: did it keep every "
                "requirement the client actually stated, including copy that must appear exactly? "
                "That question is not about quality and must not be traded against it."
            ),
            "dimensions": DIMENSIONS,
            "gating_dimension": GATING_DIMENSION,
        })

    out = {
        "run_id": RUN_ID,
        "status": "PACKAGE_ONLY_NOT_EXECUTED",
        "generated_outputs": 0,
        "expected_outputs": 24,
        "frozen_at": "2026-08-26",
        "prompt_file": str(PROMPT.relative_to(ROOT)),
        "prompt_sha256": prompt_hash,
        "randomisation": {"seed": SEED, "library": "python random.Random", "reproducible": True},
        "length_match": {"tolerance": TOLERANCE, "pairs": pairs_len,
                         "max_drift": max(p["drift"] for p in pairs_len)},
        "blinding": {
            "balanced": True,
            "a_side_generic": a_side.count("generic"),
            "a_side_oracle_canon": a_side.count("oracle_canon"),
            "note": "Exactly half the pairs present each arm first, so a reviewer order effect "
                    "cannot favour either arm systematically.",
        },
        "review_dimensions": DIMENSIONS,
        "gating_dimension": GATING_DIMENSION,
        "gate_thresholds": {
            "continue": ">=9 of 12 clear Canon wins AND no meaningful explicit-intent regression",
            "mixed": "7-8 of 12 — diagnose before any source expansion",
            "stop": "<=6 of 12 — stop source expansion, diagnose Canon noise/redundancy/"
                    "over-prescription first",
            "note": "This is an engineering continuation gate on 12 briefs. It is NOT a population "
                    "confidence claim and no rate derived from it describes any wider set of briefs.",
        },
        "pairs": run,
    }
    (HERE / "run-manifest.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    (HERE / "blinding-key.json").write_text(json.dumps(
        {"run_id": RUN_ID, "seed": SEED,
         "warning": "SEALED. Do not open before all verdicts are recorded. Reviewers must never "
                    "receive this file.",
         "mapping": key}, indent=2) + "\n")
    (HERE / "reviewer-packet-template.json").write_text(json.dumps(
        {"run_id": RUN_ID,
         "status": "TEMPLATE — plan text is placeholder because nothing has been generated",
         "pairs": packet}, indent=2, ensure_ascii=False) + "\n")

    print(json.dumps({
        "pairs": len(run), "expected_outputs": 24, "generated_outputs": 0,
        "max_length_drift": out["length_match"]["max_drift"],
        "tolerance": TOLERANCE, "prompt_sha256": prompt_hash[:16] + "...",
        "arm_A_is_generic_in_pairs": sum(1 for k in key if k["A"] == "generic"),
        "arm_A_is_oracle_in_pairs": sum(1 for k in key if k["A"] == "oracle_canon"),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
