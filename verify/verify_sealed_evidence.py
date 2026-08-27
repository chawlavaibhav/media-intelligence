#!/usr/bin/env python3
"""Deterministic hash verification of the sealed EMP-001 evidence.

Checks, from committed bytes alone (no network, no secrets, no spend):

  1. the 16 sealed A-TEXT generation artifacts against the generation manifest
     (`atex-generation-only-manifest.json`): per-file SHA-256 and byte length,
     16/16 present, all hashes distinct;
  2. every file listed in the two evidence manifests
     (`evidence/EMP-001/text-ocr/EVIDENCE-MANIFEST.json`,
      `evidence/EMP-001/atex-scoring/EVIDENCE-MANIFEST.json`)
     against its recorded SHA-256 and byte length;
  3. the headline A-TEXT scoring counts recomputed from the 16 row-level
     records (expected 6/8 GPT Image 2, 1/8 Ideogram v3, 7/16 overall).

This script verifies linkage only. The manifests and evidence files are the
authority; a matching recomputation is a check that they still say what they
said when sealed, not a certification of the underlying science.

Exit code 0 = all checks pass; 1 = any mismatch (each mismatch is printed).
Run from the repository root: python3 verify/verify_sealed_evidence.py
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

ATEX_GEN_MANIFEST = ROOT / "eval/empirical-tranche-1/atex/sealed-generation-v1/atex-generation-only-manifest.json"
EVIDENCE_MANIFESTS = [
    ROOT / "eval/empirical-tranche-1/evidence/EMP-001/text-ocr/EVIDENCE-MANIFEST.json",
    ROOT / "eval/empirical-tranche-1/evidence/EMP-001/atex-scoring/EVIDENCE-MANIFEST.json",
]
ATEX_SCORING = ROOT / "eval/empirical-tranche-1/evidence/EMP-001/atex-scoring/atex-benchmark-scoring-v1.json"

EXPECTED_ATEX = {"IMG-01": (6, 8), "IMG-02": (1, 8), "overall": (7, 16)}


def sha256_of(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_file(path: pathlib.Path, want_sha: str, want_bytes: int, errors: list, label: str) -> None:
    if not path.is_file():
        errors.append(f"{label}: MISSING {path}")
        return
    size = path.stat().st_size
    if size != want_bytes:
        errors.append(f"{label}: BYTES {path} recorded {want_bytes} actual {size}")
    got = sha256_of(path)
    if got != want_sha:
        errors.append(f"{label}: SHA256 {path} recorded {want_sha} actual {got}")


def main() -> int:
    errors: list[str] = []

    # 1. Sealed A-TEXT generation artifacts.
    gen = json.loads(ATEX_GEN_MANIFEST.read_text())
    artifacts = gen["artifacts"]
    if len(artifacts) != 16:
        errors.append(f"atex-generation: expected 16 artifacts, manifest lists {len(artifacts)}")
    hashes = [a["sha256"] for a in artifacts]
    if len(set(hashes)) != len(hashes):
        errors.append("atex-generation: artifact hashes are not all distinct")
    root = ROOT / gen["artifact_root"]
    for a in artifacts:
        check_file(root / a["relative_path"], a["sha256"], a["bytes"], errors, "atex-generation")
    print(f"atex-generation: {len(artifacts)} artifacts checked against {ATEX_GEN_MANIFEST.relative_to(ROOT)}")

    # 2. Evidence manifests.
    for manifest_path in EVIDENCE_MANIFESTS:
        manifest = json.loads(manifest_path.read_text())
        for f in manifest["files"]:
            check_file(ROOT / f["path"], f["sha256"], f["bytes"], errors, manifest["evidence_package_id"])
        print(f"{manifest['evidence_package_id']}: {len(manifest['files'])} files checked against {manifest_path.relative_to(ROOT)}")

    # 3. Recompute the headline A-TEXT counts from row-level records.
    scoring = json.loads(ATEX_SCORING.read_text())
    rows = scoring["rows"] if isinstance(scoring, dict) and "rows" in scoring else scoring
    if isinstance(rows, dict):
        # fall back: find the list-valued key holding 16 records
        candidates = [v for v in rows.values() if isinstance(v, list) and len(v) == 16]
        rows = candidates[0] if candidates else []
    counts: dict[str, list[int]] = {"IMG-01": [0, 0], "IMG-02": [0, 0], "overall": [0, 0]}
    for r in rows:
        slot = r.get("slot") or (r.get("coordinate_id", "").split(":", 1)[0])
        exact = bool(r.get("exact_match"))
        for key in (slot, "overall"):
            if key in counts:
                counts[key][0] += 1 if exact else 0
                counts[key][1] += 1
    for key, (want_exact, want_total) in EXPECTED_ATEX.items():
        got_exact, got_total = counts.get(key, (None, None))
        if (got_exact, got_total) != (want_exact, want_total):
            errors.append(
                f"atex-scoring: {key} recomputed {got_exact}/{got_total}, sealed result says {want_exact}/{want_total}"
            )
    print(f"atex-scoring: recomputed exact counts {counts}")

    if errors:
        print("\nRESULT: FAIL")
        for e in errors:
            print("  -", e)
        return 1
    print("\nRESULT: PASS - sealed evidence hashes, byte lengths and headline A-TEXT counts all verify.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
