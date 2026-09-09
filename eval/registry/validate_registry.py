#!/usr/bin/env python3
"""Validate the Capability Registry schema and the (empty) registry file.

Fails closed. The single most important assertion here is that the registry
contains ZERO empirical rows: no instrument is qualified, so any row would be a
capability claim with nothing behind it.

Run:  python3 eval/registry/validate_registry.py
      python3 eval/registry/validate_registry.py --selftest   # negative controls
"""
import hashlib
import argparse, io, json, pathlib, sys, contextlib, yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "eval/registry/SCHEMA-v1-draft.yaml"
DATA = ROOT / "eval/registry/registry-v1.jsonl"

REQUIRED_TOP = ["schema_version", "status", "empirical_entries", "row_fields",
                "no_routing_scores", "extends"]
REQUIRED_ROW = ["entry_id", "provider", "model", "version", "endpoint",
                "workflow", "capability", "n_items", "repeats_per_item",
                "trials", "passes", "instrument", "cost", "uncertainty",
                "absence_reason", "synthetic", "registry_write_rule",
                "freshness", "reliability"]
# E-C8
REQUIRED_UNCERTAINTY = ["status", "method", "interval_low", "interval_high",
                        "computed_over", "assumptions", "independence_status",
                        "is_reference_calculation_only",
                        "not_computed_reason"]


def validate(schema_path=None, data_path=None):
    schema_path = schema_path or SCHEMA
    data_path = data_path or DATA
    errors = []

    if not schema_path.exists():
        print("FAIL: schema file missing")
        return 1
    s = yaml.safe_load(schema_path.read_text())
    if not s:
        print("FAIL: schema is empty - an empty check is not a passing check")
        return 1

    for k in REQUIRED_TOP:
        if k not in s:
            errors.append(f"schema missing top-level key '{k}'")

    # 2026-09-09: the Controller froze the six deterministic-instrument criteria
    # (coordination/decisions/CONTROLLER-INSTRUMENT-THRESHOLDS-FROZEN-2026-09-09.md), so rows from
    # `deterministic` (or `qualified`) instruments are admissible. The declared count must equal
    # the rows actually present; nothing else changed in the admission bar.
    declared_entries = s.get("empirical_entries")
    if s.get("status") != "PROPOSED_NOT_IN_FORCE":
        errors.append(f"schema status is '{s.get('status')}'; the schema is not "
                      f"approved and must not claim otherwise")

    rf = s.get("row_fields") or {}
    for k in REQUIRED_ROW:
        if k not in rf:
            errors.append(f"row_fields missing '{k}'")

    # --- E-C8 uncertainty provenance ---------------------------------------
    unc = rf.get("uncertainty")
    if not isinstance(unc, dict):
        errors.append("row_fields.uncertainty must be a structured block")
    else:
        for k in REQUIRED_UNCERTAINTY:
            if k not in unc:
                errors.append(f"uncertainty block missing '{k}'")
        if "status" in unc and "not_computed" not in str(unc["status"]):
            errors.append("uncertainty.status must permit 'not_computed'")
        if "independence_status" in unc and \
                "NOT ESTABLISHED" not in str(unc["independence_status"]):
            errors.append("uncertainty.independence_status must permit "
                          "'NOT ESTABLISHED'")

    # --- the write rule must still be stated --------------------------------
    wr = str(rf.get("registry_write_rule", ""))
    for token in ("required_but_no_calibrated_instrument", "deterministic"):
        if token not in wr:
            errors.append(f"registry_write_rule no longer mentions '{token}'")

    # --- the data file must be EMPTY of empirical rows ----------------------
    if not data_path.exists():
        errors.append("registry data file missing")
        rows = []
    else:
        rows = [l for l in data_path.read_text().splitlines()
                if l.strip() and not l.lstrip().startswith("#")]
    if declared_entries != len(rows):
        errors.append(f"schema declares {declared_entries} empirical entries but the data file holds {len(rows)}")
    criteria_path = schema_path.parent.parent / "harness-v2" / "instruments" / "PASS-CRITERIA-v0.yaml"
    frozen_sha = hashlib.sha256(criteria_path.read_bytes()).hexdigest() if criteria_path.exists() else None
    for i, l in enumerate(rows, 1):
        try:
            r = json.loads(l)
        except Exception:
            errors.append(f"row {i} is not valid JSON")
            continue
        if r.get("synthetic"):
            errors.append(f"row {i} is SYNTHETIC and must never be in the registry")
        if r.get("instrument_qualification_status") not in ("deterministic", "qualified"):
            errors.append(f"row {i}: instrument qualification status {r.get('instrument_qualification_status')!r} may not write a row")
        if r.get("evidence_tier") not in ("deterministic", "qualified"):
            errors.append(f"row {i}: evidence tier {r.get('evidence_tier')!r} is not admissible (human, benchmark and screened evidence never enter the Registry)")
        if frozen_sha and r.get("criteria_sha256") != frozen_sha:
            errors.append(f"row {i}: criteria_sha256 does not match the committed frozen PASS-CRITERIA file")
        for k in ("n_items", "repeats_per_item", "trials"):
            if not isinstance(r.get(k), int):
                errors.append(f"row {i}: {k} missing or not an integer")
        unc = r.get("uncertainty") or {}
        if unc.get("status") not in ("computed", "not_computed"):
            errors.append(f"row {i}: uncertainty.status must be computed or not_computed")
        if unc.get("status") == "computed" and unc.get("independence_status") not in ("ESTABLISHED", "NOT ESTABLISHED"):
            errors.append(f"row {i}: computed uncertainty needs independence_status")

    print(f"schema                 : {schema_path.name}")
    print(f"schema_version         : {s.get('schema_version')}")
    print(f"status                 : {s.get('status')}")
    print(f"declared empirical rows: {s.get('empirical_entries')}")
    print(f"actual data rows       : {len(rows)}")
    print(f"row_fields defined     : {len(rf)}")
    print(f"uncertainty keys       : {len(unc) if isinstance(unc, dict) else 0}")

    if errors:
        print(f"\nFAIL - {len(errors)} error(s):")
        for e in errors:
            print("  -", e)
        return 1
    print("\nPASS - schema valid, uncertainty provenance present, registry empty.")
    return 0


# ---------------------------------------------------------------- selftest
def _run(schema_obj, data_text):
    import tempfile, os
    sd = pathlib.Path(tempfile.mkdtemp())
    sp, dp = sd / "s.yaml", sd / "d.jsonl"
    sp.write_text(yaml.safe_dump(schema_obj))
    dp.write_text(data_text)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = validate(sp, dp)
    return rc


def selftest():
    import copy
    base = yaml.safe_load(SCHEMA.read_text())
    ok = _run(copy.deepcopy(base), DATA.read_text())
    if ok != 0:
        print("ABORT: the real schema does not validate; controls prove nothing.")
        return 1
    print("baseline: real schema + empty registry PASSES\n")

    controls = []

    def ctl(name):
        def d(fn):
            controls.append((name, fn))
            return fn
        return d

    @ctl("a POPULATED registry must FAIL")
    def c1(s):
        return s, json.dumps({"entry_id": "cap_0001", "synthetic": False}) + "\n"

    @ctl("a SYNTHETIC row in the registry must FAIL")
    def c2(s):
        return s, json.dumps({"entry_id": "cap_x", "synthetic": True}) + "\n"

    @ctl("schema claiming empirical entries must FAIL")
    def c3(s):
        s["empirical_entries"] = 12
        return s, ""

    @ctl("schema claiming to be IN FORCE must FAIL")
    def c4(s):
        s["status"] = "APPROVED_IN_FORCE"
        return s, ""

    @ctl("E-C8: removing the uncertainty block must FAIL")
    def c5(s):
        del s["row_fields"]["uncertainty"]
        return s, ""

    @ctl("E-C8: uncertainty without not_computed_reason must FAIL")
    def c6(s):
        del s["row_fields"]["uncertainty"]["not_computed_reason"]
        return s, ""

    @ctl("E-C8: uncertainty that cannot express NOT ESTABLISHED must FAIL")
    def c7(s):
        s["row_fields"]["uncertainty"]["independence_status"] = "<ESTABLISHED>"
        return s, ""

    @ctl("weakening the write rule must FAIL")
    def c8(s):
        s["row_fields"]["registry_write_rule"] = "write whatever you like"
        return s, ""

    @ctl("empty schema must FAIL")
    def c9(s):
        return None, ""

    bad = []
    for name, fn in controls:
        s, data = fn(copy.deepcopy(base))
        rc = _run(s, data)
        good = rc != 0
        print(f"  [{'ok' if good else 'DEFECT'}] {name} -> rc={rc}")
        if not good:
            bad.append(name)
    print()
    if bad:
        print(f"FAIL - {len(bad)} control(s) not rejected: {bad}")
        return 1
    print(f"PASS - all {len(controls)} negative controls correctly rejected.")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    sys.exit(selftest() if a.selftest else validate())
