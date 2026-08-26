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
# The dry-run controls are contaminated for a real gate (C-C3): they were authored by a
# session that had already read the Oracle Canon. They stay usable as synthetic fixtures
# and the directory name says what they are, so nothing can pick them up by accident.
GEN_DIR = HERE / "generic-contexts-DRYRUN-CONTAMINATED"
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


CONTAMINATION_BANNER = """<!-- ============================================================================
  DRY-RUN ONLY - CONTAMINATED FOR THE REAL GATE. DO NOT USE IN A REAL RUN.

  This control context was authored by the same worker session that had already
  read the Oracle Canon material for this brief. Even authored carefully, that
  is a contamination risk: the control cannot be shown to be independent of the
  Canon it is meant to be compared against, so a Canon win measured against it
  would not be interpretable.

  Retained ONLY as a dry-run fixture and as evidence of what was done. The
  real-run builder (prepare_real_run.py) refuses to start if this directory is
  used.

  Replacement controls must be authored per
  GENERIC-CONTROL-AUTHORING-PACKET.md by a fresh session with no Canon access,
  and written to generic-contexts-real/.
============================================================================= -->

"""


def words(t: str) -> int:
    return len(t.split())

def stratified_a_side(pairs_by_role: dict, rng) -> dict:
    """Balance which arm is shown first WITHIN each probe stratum, not just overall.

    WHY THIS IS NOT MERELY OVERALL BALANCE. Only the 7 coverage probes vote on continuation. An
    assignment that is a tidy 6/6 across all 12 pairs can still show Canon first on 5 of the 7
    coverage probes — and it did, on the first corrected build. A reviewer with a pure position
    effect would then have scored 5/7 and reached `continue` without reading anything. Overall
    balance is the wrong invariant; balance inside the stratum that votes is the right one.

    With an odd stratum a perfect split is impossible. 7 coverage probes give at best 4/3, so a pure
    position effect reaches 4/7 -> `mixed`, never `continue`. That is the floor, and it is stated
    rather than glossed.
    """
    a_side = {}
    for role, pids in sorted(pairs_by_role.items()):
        n = len(pids)
        # Canon-first on floor(n/2) of them; the leftover always goes to the control arm, so the
        # residual position advantage can never favour Canon.
        sides = ["oracle_canon"] * (n // 2) + ["generic"] * (n - n // 2)
        rng.shuffle(sides)
        order = list(pids)
        rng.shuffle(order)
        for pid, side in zip(order, sides):
            a_side[pid] = side
    return a_side



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
        # Re-stamp the banner on every write so a regeneration can never quietly produce a file
        # that looks like a usable control.
        (GEN_DIR / f"{bid}.md").write_text(CONTAMINATION_BANNER + body)
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

    # STRATIFIED balanced A/B assignment (see stratified_a_side). Balancing overall is not enough:
    # only coverage probes vote, and a 6/6 overall split once left Canon shown first on 5 of the 7
    # coverage probes, which a pure position effect would have turned into `continue`.
    early = json.loads((HERE / "early-12-manifest.json").read_text())
    roles = {b["brief_id"]: b["gate_role"] for b in early["briefs"]}
    by_role: dict[str, list[str]] = {}
    for bid in order:
        by_role.setdefault(roles[bid], []).append(bid)
    a_side_by_brief = stratified_a_side(by_role, rng)

    run, key, packet = [], [], []
    for i, bid in enumerate(order, 1):
        pair_id = f"PAIR-{i:02d}"
        a_arm = a_side_by_brief[bid]
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
            "stratified_by": "gate_role",
            "a_side_generic": sum(1 for v in a_side_by_brief.values() if v == "generic"),
            "a_side_oracle_canon": sum(1 for v in a_side_by_brief.values()
                                       if v == "oracle_canon"),
            "canon_first_by_role": {
                role: sum(1 for b in bids if a_side_by_brief[b] == "oracle_canon")
                for role, bids in sorted(by_role.items())
            },
            "note": "Balanced WITHIN each probe stratum, not merely overall. Only coverage probes "
                    "vote, so an overall 6/6 split is not sufficient: it once left Canon shown "
                    "first on 5 of 7 coverage probes, which a pure position effect would have "
                    "turned into `continue`. With 7 coverage probes a perfect split is impossible; "
                    "4/3 is the floor and any leftover goes to the control arm.",
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
    # This key is DERIVED FROM A COMMITTED SEED and is itself committed, so it provides no blinding
    # whatsoever: anyone who can read the branch can recompute it. That is fine for scoring
    # synthetic fixtures and unusable for a real run, so the file says so about itself. A real run
    # uses prepare_real_run.py, which draws fresh OS entropy and keeps the key outside the repo.
    (HERE / "blinding-key.json").write_text(json.dumps(
        {"status": "DRY_RUN_ONLY_INVALIDATED_FOR_REAL_USE",
         "invalidated_on": "2026-08-26",
         "invalidated_by": "Controller decision C-C4",
         "why": "Derived from a seed committed in the repository and committed as plain JSON, so "
                "the arm mapping is recomputable by anyone who can read the branch. This is not "
                "blinding.",
         "replacement": "prepare_real_run.py — fresh OS entropy at preparation time, key stored "
                        "outside the repository, only a salted SHA-256 commitment committed.",
         "retained_because": "the synthetic dry-run fixtures are scored against this mapping.",
         "run_id": RUN_ID, "seed": SEED, "mapping": key}, indent=2) + "\n")
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
        "canon_first_by_role": out["blinding"]["canon_first_by_role"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
