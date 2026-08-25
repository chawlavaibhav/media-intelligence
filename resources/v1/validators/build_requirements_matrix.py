#!/usr/bin/env python3
"""Derive RESOURCE-REQUIREMENTS-MATRIX.csv from resource-requirements.yaml, and prove it complete.

WHY THIS EXISTS
The YAML is the single source of truth. The CSV is a convenience view of it. Deriving one from the
other means they cannot drift apart the way two hand-maintained files always do.

FAIL-CLOSED BY DESIGN
GOV-001 finding F1/R3 recorded a Resources script that produced a degraded artifact and still
exited 0 when its inputs were missing. That defect is domain-owned and is NOT fixed here (it needs
a Controller-assigned task). But the lesson is applied to every new tool in resources/v1/:

  * missing or unreadable input  -> exit 2, write nothing
  * an empty or short row set    -> exit 2, write nothing
  * completeness assertion fails -> exit 2, write nothing

An empty check is not a passing check. This script writes the CSV only after every assertion holds.

Usage:  python3 resources/v1/validators/build_requirements_matrix.py [--check]
        --check verifies the committed CSV matches the YAML without rewriting it.
"""
import csv, os, sys, io

try:
    import yaml
except ImportError:
    print("[FAIL] PyYAML not available", file=sys.stderr); sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "v1", "resource-requirements.yaml")
OUT = os.path.join(ROOT, "v1", "RESOURCE-REQUIREMENTS-MATRIX.csv")

# Frozen expectations from eval/tasks/EVAL-V1-OVERNIGHT-PROGRAM.md. If Eval's map changes, this
# script must fail until the matrix is updated deliberately.
EXPECT_CAPABILITIES = 36
EXPECT_INSTRUMENTS = 6
VALID_STATES = {"available", "partial", "missing", "blocked",
                "constructed_by_eval", "no_external_resource"}
VALID_STORAGE = {"A", "B", "C", "none"}

COLUMNS = ["id", "group", "consumer", "media", "target_quantity", "required_metadata",
           "label_trust", "independence", "geo_language", "rights_minimum", "storage_class",
           "candidate_sources", "state", "blocked_reason", "resources_note", "why"]


def fail(msg):
    print(f"[FAIL] {msg}", file=sys.stderr)
    sys.exit(2)


def load():
    if not os.path.isfile(SRC):
        fail(f"source of truth missing: {SRC}")
    with open(SRC) as fh:
        doc = yaml.safe_load(fh)
    if not doc:
        fail("source of truth parsed to nothing")
    rows = doc.get("requirements") or []
    if len(rows) < 40:
        fail(f"only {len(rows)} requirement rows parsed; refusing to emit a truncated matrix")
    return doc, rows


def check_completeness(rows):
    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        fail(f"duplicate requirement ids: {dupes}")

    caps = [r for r in rows if r["id"].startswith("REQ-CAP-")]
    if len(caps) != EXPECT_CAPABILITIES:
        fail(f"expected {EXPECT_CAPABILITIES} capability rows, found {len(caps)}")
    expected_cap_ids = {f"REQ-CAP-{n:02d}" for n in range(1, EXPECT_CAPABILITIES + 1)}
    missing = expected_cap_ids - set(ids)
    if missing:
        fail(f"missing capability rows: {sorted(missing)}")

    ins = [r for r in rows if r["id"].startswith("REQ-INS-")]
    if len(ins) != EXPECT_INSTRUMENTS:
        fail(f"expected {EXPECT_INSTRUMENTS} evaluator-family rows, found {len(ins)}")

    for r in rows:
        for field in ("consumer", "state", "storage_class", "why"):
            if not r.get(field):
                fail(f"{r['id']}: mandatory field '{field}' is empty")
        if r["state"] not in VALID_STATES:
            fail(f"{r['id']}: unknown state {r['state']!r}")
        if str(r["storage_class"]) not in VALID_STORAGE:
            fail(f"{r['id']}: unknown storage_class {r['storage_class']!r}")
        if r["state"] == "blocked" and not r.get("blocked_reason"):
            fail(f"{r['id']}: state is 'blocked' but no blocked_reason given")
    return caps, ins


def check_pack_refs(doc, rows):
    pack_ids = {p["pack_id"] for p in doc.get("packs", [])}
    # Legacy pool ids are resolved by the legacy reconciliation, not by the pack list.
    legacy_ids = {"LEGACY-MF-SCORES", "LEGACY-MF-REFS"}
    known = pack_ids | legacy_ids
    row_ids = {r["id"] for r in rows}
    for r in rows:
        for s in (r.get("candidate_sources") or []):
            if s.startswith(("PACK-", "LEGACY-")) and s not in known:
                fail(f"{r['id']}: candidate source {s} is not a declared pack or legacy pool")
    for p in doc.get("packs", []):
        for s in (p.get("serves") or []):
            if s not in row_ids:
                fail(f"pack {p['pack_id']}: serves unknown requirement {s}")


def render(rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=COLUMNS, lineterminator="\n")
    w.writeheader()
    for r in rows:
        out = {}
        for c in COLUMNS:
            v = r.get(c, "")
            if isinstance(v, list):
                v = "; ".join(str(x) for x in v)
            out[c] = "" if v is None else str(v)
        w.writerow(out)
    return buf.getvalue()


def main():
    check_only = "--check" in sys.argv
    doc, rows = load()
    caps, ins = check_completeness(rows)
    check_pack_refs(doc, rows)
    text = render(rows)

    if check_only:
        if not os.path.isfile(OUT):
            fail("--check requested but the CSV does not exist")
        with open(OUT) as fh:
            if fh.read() != text:
                fail("committed CSV does not match the YAML source of truth")
        print("[PASS] committed CSV matches the YAML source of truth")
    else:
        with open(OUT, "w") as fh:
            fh.write(text)
        print(f"[OK] wrote {OUT}")

    from collections import Counter
    print(f"[PASS] {len(caps)}/{EXPECT_CAPABILITIES} capability rows present")
    print(f"[PASS] {len(ins)}/{EXPECT_INSTRUMENTS} evaluator-family rows present")
    print(f"[PASS] {len(rows)} total requirement rows, all with a state and a reason")
    print("state distribution:")
    for k, v in sorted(Counter(r["state"] for r in rows).items()):
        print(f"   {k:22s} {v}")
    print("capability-only state distribution:")
    for k, v in sorted(Counter(r["state"] for r in caps).items()):
        print(f"   {k:22s} {v}")


if __name__ == "__main__":
    main()
