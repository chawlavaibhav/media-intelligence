#!/usr/bin/env python3
"""CANON-V1 / C-C4 — prepare a REAL value-gate run with a genuinely sealed blinding key.

WHAT WAS WRONG BEFORE. The dry-run builder derived its A/B mapping from a seed committed in the
repository. Anyone who could read the branch could recompute which arm was "A" for every pair — and
the key itself was committed as plain JSON. That is not blinding; it is blinding-shaped. It was
harmless for a synthetic dry run and unusable for a real one.

WHAT HAPPENS NOW.

1. Fresh randomness at preparation time, from `secrets` (OS entropy). Nothing in the repository
   determines the mapping, so nothing in the repository can reveal it.
2. The mapping is written OUTSIDE the repository, to a path the operator supplies. This script
   refuses to write it anywhere inside the working tree.
3. Only a COMMITMENT goes into the repo: SHA-256 over a random salt plus the canonical mapping. The
   salt is stored with the key, not with the commitment, so the commitment cannot be brute-forced
   from the 2**12 possible mappings.
4. After verdicts are frozen, `--verify-key` re-derives the commitment from the revealed key and
   proves the mapping was not altered mid-review.

It also refuses to prepare a run against contaminated controls (C-C3).

    python3 prepare_real_run.py --key-out /secure/path/key.json
    python3 prepare_real_run.py --verify-key /secure/path/key.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import secrets
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
MANIFEST = HERE / "early-12-manifest.json"
BRIEFS = ROOT / "canon/experiments/v1/brief-bank/briefs.jsonl"
ORACLE = HERE / "oracle-contexts"
REAL_CONTROLS = HERE / "generic-contexts-real"
CONTAMINATED = HERE / "generic-contexts-DRYRUN-CONTAMINATED"
PROMPT = HERE / "prompts/planning-prompt.md"
OUT_MANIFEST = HERE / "real-run-manifest.json"
OUT_PACKET = HERE / "real-reviewer-packet.json"

RUN_ID = "CANON-V1-GATE-REAL-001"
TOLERANCE = 0.15
REVIEWERS_REQUIRED = 2


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


def canonical(mapping: list[dict]) -> str:
    return json.dumps(sorted(mapping, key=lambda m: m["pair_id"]), sort_keys=True,
                      separators=(",", ":"))


def commitment(salt: str, mapping: list[dict]) -> str:
    return hashlib.sha256((salt + canonical(mapping)).encode()).hexdigest()


def verify(key_path: pathlib.Path) -> int:
    key = json.loads(key_path.read_text())
    if not OUT_MANIFEST.exists():
        print(json.dumps({"status": "NO_REAL_RUN", "message": "No real run has been prepared."},
                         indent=2))
        return 1
    manifest = json.loads(OUT_MANIFEST.read_text())
    recomputed = commitment(key["salt"], key["mapping"])
    ok = recomputed == manifest["blinding"]["commitment_sha256"]
    print(json.dumps({
        "status": "KEY_VERIFIED" if ok else "KEY_MISMATCH",
        "run_id": manifest["run_id"],
        "commitment_in_manifest": manifest["blinding"]["commitment_sha256"][:16] + "...",
        "recomputed_from_key": recomputed[:16] + "...",
        "message": "The revealed key matches the commitment frozen before review; the mapping was "
                   "not altered mid-review."
                   if ok else
                   "MISMATCH. The revealed key is not the one committed to before review. Treat the "
                   "run as compromised and do not report a result from it.",
    }, indent=2))
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--key-out", help="path OUTSIDE the repository to write the sealed key to")
    ap.add_argument("--verify-key", help="path to a revealed key, to check against the commitment")
    args = ap.parse_args()

    if args.verify_key:
        return verify(pathlib.Path(args.verify_key))
    if not args.key_out:
        ap.error("--key-out is required to prepare a run")

    errors = []

    # C-C3: the contaminated controls may never be used in a real run.
    if not REAL_CONTROLS.is_dir():
        errors.append(
            f"{REAL_CONTROLS.name}/ does not exist. The real gate needs generic controls authored "
            "by a fresh session with no Canon access — see GENERIC-CONTROL-AUTHORING-PACKET.md. "
            "The contaminated dry-run controls may not be substituted.")
    elif CONTAMINATED.resolve() == REAL_CONTROLS.resolve():
        errors.append("real controls resolve to the contaminated dry-run directory; refusing")

    key_out = pathlib.Path(args.key_out).resolve()
    try:
        key_out.relative_to(ROOT)
        errors.append(
            f"--key-out {key_out} is inside the repository. The blinding key must be stored outside "
            "the working tree while reviews are open; committing it is what broke the dry run.")
    except ValueError:
        pass  # outside the repo: correct

    manifest = json.loads(MANIFEST.read_text())
    ids = [b["brief_id"] for b in manifest["briefs"]]
    roles = {b["brief_id"]: b["gate_role"] for b in manifest["briefs"]}

    if not errors and REAL_CONTROLS.is_dir():
        for bid in ids:
            cf = REAL_CONTROLS / f"{bid}.md"
            if not cf.exists():
                errors.append(f"{bid}: no real control context at {cf.name}")
                continue
            gw = len(cf.read_text().split())
            ow = len((ORACLE / f"{bid}.md").read_text().split())
            drift = abs(gw - ow) / ow
            if drift > TOLERANCE:
                errors.append(f"{bid}: control {gw} words vs oracle {ow}, drift {drift:.1%} "
                              f"exceeds {TOLERANCE:.0%}")

    if errors:
        print(json.dumps({"status": "REFUSED", "error_count": len(errors), "errors": errors},
                         indent=2))
        return 1

    briefs = {json.loads(l)["brief_id"]: json.loads(l) for l in BRIEFS.read_text().splitlines()}

    # Fresh entropy, and STRATIFIED balance: only coverage probes vote, so the arm shown first
    # must be balanced within that stratum and not merely across all 12 pairs.
    order = list(ids)
    rng = secrets.SystemRandom()
    rng.shuffle(order)
    by_role: dict[str, list[str]] = {}
    for bid in order:
        by_role.setdefault(roles[bid], []).append(bid)
    a_side_by_brief = stratified_a_side(by_role, rng)

    mapping, pairs, packet = [], [], []
    for i, bid in enumerate(order, 1):
        pair_id = f"PAIR-{i:02d}"
        a_arm = a_side_by_brief[bid]
        b_arm = "oracle_canon" if a_arm == "generic" else "generic"
        mapping.append({"pair_id": pair_id, "brief_id": bid, "A": a_arm, "B": b_arm})
        # The committed manifest records WHICH FILES exist, never which side each is presented on.
        pairs.append({"pair_id": pair_id, "brief_id": bid, "gate_role": roles[bid],
                      "oracle_context": f"oracle-contexts/{bid}.md",
                      "control_context": f"generic-contexts-real/{bid}.md"})
        packet.append({
            "pair_id": pair_id,
            "customer_brief": briefs[bid]["customer_brief"],
            "plan_A": "<<PLAN TEXT>>",
            "plan_B": "<<PLAN TEXT>>",
            "reviewers_required": REVIEWERS_REQUIRED,
        })

    salt = secrets.token_hex(32)
    commit_hash = commitment(salt, mapping)

    key_out.parent.mkdir(parents=True, exist_ok=True)
    key_out.write_text(json.dumps({
        "run_id": RUN_ID, "salt": salt, "mapping": mapping,
        "warning": "SEALED BLINDING KEY. Do not place this file in the repository and do not show "
                   "it to a reviewer. Reveal only after every verdict is frozen.",
    }, indent=2) + "\n")

    out = {
        "run_id": RUN_ID,
        "status": "PREPARED_NOT_EXECUTED",
        "generated_outputs": 0,
        "expected_outputs": 24,
        "prompt_sha256": hashlib.sha256(PROMPT.read_bytes()).hexdigest(),
        "controls": "generic-contexts-real (authored by an independent session)",
        "blinding": {
            "sealed": True,
            "source_of_randomness": "secrets.SystemRandom (OS entropy) at preparation time",
            "commitment_sha256": commit_hash,
            "commitment_scheme": "sha256(salt || canonical_json(mapping)); the salt lives with the "
                                 "key, so the commitment cannot be brute-forced over the possible "
                                 "mappings",
            "key_location": "outside the repository; path known only to the operator",
            "balanced": True,
            "stratified_by": "gate_role",
            "note": "Balanced within each probe stratum, not merely overall, so a reviewer position "
                    "effect cannot carry the voting coverage probes. The mapping itself is NOT "
                    "recorded here and is not derivable from anything committed.",
        },
        "reviewers_required_per_pair": REVIEWERS_REQUIRED,
        "pairs": pairs,
    }
    OUT_MANIFEST.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    OUT_PACKET.write_text(json.dumps(
        {"run_id": RUN_ID, "reviewers_required": REVIEWERS_REQUIRED, "pairs": packet},
        indent=2, ensure_ascii=False) + "\n")

    print(json.dumps({"status": "PREPARED", "run_id": RUN_ID, "pairs": len(pairs),
                      "key_written_outside_repo": str(key_out),
                      "commitment_sha256": commit_hash[:16] + "...",
                      "mapping_in_committed_files": False}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
