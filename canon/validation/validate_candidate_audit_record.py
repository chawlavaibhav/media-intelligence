#!/usr/bin/env python3
"""Run the adopted Audit Gate v0.2 per-record checks against a CANDIDATE-dir record.

STATUS: PROPOSED — REP-07 executor tooling; no Controller decision adopts it.

Why this exists. REP-07 authors Audit Gate v0.2 records for HOLD sources while they still live
under canon/candidates/canon-014/. The repository validator (validate_audit_gate_v02.py) reads
only canon/audit/records/*.audit.yaml — deliberately, because that directory holds accepted
sources and REP-07's acceptance forbids a candidate dir gaining a record there before admission.
This harness proves a candidate-dir record would pass the adopted per-record rules by calling the
SAME validate_record() the repository validator uses, against the same root. Zero rules are
redefined here.

Record-set rules (duplicate ids, dependence symmetry) are reported informationally against the
union of accepted + given candidate records: a candidate may declare a dependence on an accepted
source whose record cannot declare it back until admission updates it, and that asymmetry is an
admission-time task, not an inspection-time failure.

Usage: python3 canon/validation/validate_candidate_audit_record.py <record.yaml> [...] [--root .]
Exit 0 iff every given record passes the per-record rules.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import yaml  # noqa: E402

from validate_audit_gate_v02 import (  # noqa: E402
    RECORDS_SUBPATH,
    _load_yaml,
    validate_record,
    validate_record_set,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("records", nargs="+", type=Path)
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()
    root = args.root.resolve()

    errors: list[str] = []
    union: dict[str, dict] = {}
    for path in sorted((root / RECORDS_SUBPATH).glob("*.audit.yaml")):
        doc = _load_yaml(path)
        if isinstance(doc, dict):
            union[path.name] = doc

    for path in args.records:
        try:
            doc = _load_yaml(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not isinstance(doc, dict):
            errors.append(f"{path}: record is not a mapping")
            continue
        union[str(path)] = doc
        for err in validate_record(doc, root):
            errors.append(f"{path}: {err}")

    for line in errors:
        print(f"ERROR {line}")

    informational = validate_record_set(union)
    for line in informational:
        print(f"INFO (admission-time, not failing) {line}")

    print(f"checked {len(args.records)} candidate record(s); {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
