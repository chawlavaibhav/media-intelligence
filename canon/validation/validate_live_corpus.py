#!/usr/bin/env python3
"""Live-corpus validator for the Canon as it stands today.

Introduced by CANON-006. It answers a question neither existing validator asks:

  validate_canon003_integrated.py  is a HISTORICAL instrument. It validates the frozen 16-book
                                   CANON-003 set and its meaning must never change.
  validate_audit_gate_v02.py       validates audit records against the sources they describe.
  this file                        validates the CURRENT live corpus: that every source present is
                                   declared, that `accepted` really did pass the gate, that
                                   `source_evidence_only` really is held back, and that ids are
                                   unique across everything now in the repository.

Read-only. It never writes to a source artifact or an audit record.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

# Importable as `canon.validation.validate_live_corpus` and runnable as a script from the repo root.
# The sibling validators need no bootstrap because they import nothing from this package; this one
# reuses their logic rather than duplicating it, which is worth one line of path handling.
if __package__ in (None, ""):  # pragma: no cover - only taken when run directly
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from canon.validation import validate_audit_gate_v02 as audit  # noqa: E402
from canon.validation import validate_canon003_integrated as integrated  # noqa: E402

REGISTER_PATH = Path("canon/audit/LIVE-CORPUS.yaml")
KNOWLEDGE_SUBPATH = Path("canon/knowledge/current")

GATE_STATUSES = {"accepted", "source_evidence_only"}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def validate_live_corpus(root: Path) -> dict[str, Any]:
    errors: list[str] = []
    register_file = root / REGISTER_PATH
    knowledge_root = root / KNOWLEDGE_SUBPATH

    if not register_file.is_file():
        return {"error_count": 1, "errors": [f"live-corpus register missing: {REGISTER_PATH}"]}

    register = yaml.safe_load(register_file.read_text(encoding="utf-8")) or {}
    entries = _list(register.get("sources"))

    declared: dict[str, str] = {}
    for i, entry in enumerate(entries, 1):
        if not isinstance(entry, dict):
            errors.append(f"register: sources[{i}] is not a mapping")
            continue
        name, status = entry.get("dir"), entry.get("gate_status")
        if not name:
            errors.append(f"register: sources[{i}] has no dir")
            continue
        if name in declared:
            errors.append(f"register: {name} declared more than once")
        if status not in GATE_STATUSES:
            errors.append(f"register: {name} has invalid gate_status {status!r}")
            continue
        declared[name] = status
        # A blocked source must say why. Silence would be indistinguishable from an oversight.
        if status == "source_evidence_only" and not str(entry.get("blocked_reason") or "").strip():
            errors.append(f"register: {name} is source_evidence_only with no blocked_reason")

    on_disk = sorted(p.name for p in knowledge_root.iterdir() if p.is_dir()) if knowledge_root.is_dir() else []
    for name in on_disk:
        if name not in declared:
            errors.append(
                f"undeclared source: {name} is present but not in {REGISTER_PATH}; every live source "
                f"must state whether it passed the gate"
            )
    for name in sorted(declared):
        if name not in on_disk:
            errors.append(f"register: {name} is declared but no such directory exists")

    # Which sources hold an active audit record.
    audited: dict[str, str] = {}
    records_dir = root / audit.RECORDS_SUBPATH
    if records_dir.is_dir():
        for path in sorted(records_dir.glob("*.audit.yaml")):
            doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            kd = str(doc.get("knowledge_dir") or "")
            if kd:
                audited[Path(kd).name] = path.name

    for name, status in sorted(declared.items()):
        if status == "accepted" and name not in audited:
            errors.append(
                f"{name}: declared accepted but has no active Audit Gate record; an unaudited source "
                f"cannot be accepted downstream knowledge"
            )
        if status == "source_evidence_only" and name in audited:
            errors.append(
                f"{name}: declared source_evidence_only but carries an audit record "
                f"({audited[name]}); a blocked source must not hold one"
            )

    # Every source in the repository must be mechanically valid, accepted or not. Being held back
    # from downstream use is not a licence to hold a malformed record.
    for name in on_disk:
        errors.extend(integrated.validate_book_dir(knowledge_root / name))

    # Ids must be unique across everything now present, not only within the historical 16.
    seen: dict[str, dict[str, str]] = {k: {} for k in ("sk", "scs", "term", "concept", "binding")}
    counts = {k: 0 for k in seen}
    for name in on_disk:
        try:
            ids = integrated._ids(knowledge_root / name)
        except ValueError as exc:
            errors.append(f"{name}: {exc}")
            continue
        for kind, values in ids.items():
            for value in values:
                counts[kind] += 1
                if value in seen[kind]:
                    errors.append(
                        f"id collision: {kind} {value} in {seen[kind][value]} and {name}"
                    )
                else:
                    seen[kind][value] = name

    accepted = sorted(n for n, s in declared.items() if s == "accepted")
    evidence_only = sorted(n for n, s in declared.items() if s == "source_evidence_only")

    return {
        "register_version": register.get("register_version"),
        "historical_method_test_corpus": register.get("historical_method_test_corpus"),
        "sources_on_disk": len(on_disk),
        "accepted_count": len(accepted),
        "accepted": accepted,
        "source_evidence_only_count": len(evidence_only),
        "source_evidence_only": evidence_only,
        "totals_across_live_corpus": counts,
        "error_count": len(errors),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--json-report", type=Path)
    args = parser.parse_args()
    report = validate_live_corpus(args.root.resolve())
    text = json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True)
    if args.json_report:
        args.json_report.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 1 if report["error_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
