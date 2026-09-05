"""30-line checker: does a qualification record carry every field of qualification-result-schema.yaml?

    python3 eval/harness-v2/q1/check_record.py <record.yaml>      exit 0 when nothing is missing
The schema's `fields` block is the shape; nested mappings are followed; `status_rules`, descriptions
and example lists are documentation, not fields, and are skipped.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

DOC_KEYS = {"description", "example_fields", "status_rules", "note", "caveat"}


def _walk(node, prefix=""):
    if not isinstance(node, dict):
        return [prefix.rstrip(".")]
    if all(k in DOC_KEYS for k in node):
        return [prefix.rstrip(".")]
    out = []
    for k, v in node.items():
        if k in DOC_KEYS:
            continue
        out += _walk(v, f"{prefix}{k}.")
    return out


def required_fields(schema_path) -> list:
    return _walk(yaml.safe_load(Path(schema_path).read_text(encoding="utf-8"))["fields"])


def _has(record, dotted) -> bool:
    cur = record
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return False
        cur = cur[part]
    return True


def missing_fields(record: dict, schema_path) -> list:
    return [f for f in required_fields(schema_path) if not _has(record, f)]


def skeleton(schema_path) -> dict:
    out: dict = {}
    for f in required_fields(schema_path):
        cur = out
        parts = f.split(".")
        for p in parts[:-1]:
            cur = cur.setdefault(p, {})
        cur[parts[-1]] = None
    return out


if __name__ == "__main__":
    rec, schema = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else Path(__file__).resolve().parents[2] / "v1/instruments/qualification-result-schema.yaml")
    docs = yaml.safe_load(Path(rec).read_text(encoding="utf-8"))
    records = docs if isinstance(docs, list) else docs.get("records", [docs]) if isinstance(docs, dict) else [docs]
    bad = {r.get("record_id", i): missing_fields(r, schema) for i, r in enumerate(records)}
    bad = {k: v for k, v in bad.items() if v}
    print("PASS - every schema field present in every record" if not bad else f"FAIL - missing: {bad}")
    sys.exit(1 if bad else 0)
