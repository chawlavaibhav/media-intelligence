#!/usr/bin/env python3
"""Validate an empirical archive against EMPIRICAL-ARTIFACT-MANIFEST-SCHEMA.yaml, and prove fan-out.

WHAT "PROVE FAN-OUT" MEANS
The design claim is: one generated asset is stored ONCE and scored by MANY capabilities. This tool
checks that claim mechanically -
  * every measurement points at an artifact that exists;
  * no artifact's output bytes are stored twice (a duplicate output_hash with a different
    output_location is a duplicate copy and is an error);
  * measurements per artifact is well above 1, i.e. the archive really is reusing generations.

FAIL-CLOSED. Missing/empty/unparseable input is exit 2, never a cheerful "0 problems found".

Usage: check_empirical_archive.py <artifacts.jsonl> <measurements.jsonl> [acceptances.jsonl]
"""
import json, os, sys, collections

VALID_STATUS = {"ok", "error", "refusal", "timeout", "cancelled"}
REQUIRED_ARTIFACT = ["artifact_id", "trial_id", "attempt_index", "eval_item_id", "provider",
                     "model_id", "model_version", "endpoint", "workflow", "prompt_hash",
                     "config_hash", "config_location", "reference_asset_hashes", "requested_at",
                     "completed_at", "api_status", "output_hash", "output_bytes",
                     "output_location", "cost_ref", "storage_class"]
REQUIRED_MEASUREMENT = ["measurement_id", "artifact_id", "capability_id", "instrument_ref",
                        "instrument_qualification_ref", "observation_unit", "result", "measured_at"]


def fatal(msg):
    print(f"[FAIL] {msg}", file=sys.stderr); sys.exit(2)


def load(path, label, minimum=1):
    if not os.path.isfile(path):
        fatal(f"{label} file not found: {path}")
    rows = []
    with open(path) as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                fatal(f"{label} line {n} unparseable: {e}")
    if len(rows) < minimum:
        fatal(f"{label} holds {len(rows)} rows; refusing to validate an empty archive")
    return rows


def main():
    if len(sys.argv) < 3:
        fatal("usage: check_empirical_archive.py <artifacts.jsonl> <measurements.jsonl> [acceptances.jsonl]")
    arts = load(sys.argv[1], "artifacts")
    meas = load(sys.argv[2], "measurements")
    accs = load(sys.argv[3], "acceptances") if len(sys.argv) > 3 else []

    errors = []
    ids = set()
    for a in arts:
        for f in REQUIRED_ARTIFACT:
            if f not in a:
                errors.append(f"artifact {a.get('artifact_id','<no id>')}: missing field '{f}'")
        aid = a.get("artifact_id")
        if aid in ids:
            errors.append(f"duplicate artifact_id {aid}")
        ids.add(aid)
        st = a.get("api_status")
        if st not in VALID_STATUS:
            errors.append(f"artifact {aid}: invalid api_status {st!r}")
        # The rule that keeps refusals in the record.
        if st == "ok" and not a.get("output_hash"):
            errors.append(f"artifact {aid}: api_status 'ok' but output_hash is null")
        if st != "ok" and a.get("output_hash"):
            errors.append(f"artifact {aid}: api_status {st!r} but output_hash is populated")
        if a.get("storage_class") != "C_irreproducible_empirical":
            errors.append(f"artifact {aid}: storage_class must be C_irreproducible_empirical")
        if not a.get("cost_ref"):
            errors.append(f"artifact {aid}: no cost_ref; cost must never be invented later")

    # No media stored twice.
    loc_by_hash = collections.defaultdict(set)
    for a in arts:
        if a.get("output_hash"):
            loc_by_hash[a["output_hash"]].add(a.get("output_location"))
    dupe_copies = {h: v for h, v in loc_by_hash.items() if len(v) > 1}
    for h, v in dupe_copies.items():
        errors.append(f"output_hash {h[:12]}… stored at {len(v)} distinct locations: duplicate media copy")

    seen_m = set()
    for m in meas:
        for f in REQUIRED_MEASUREMENT:
            if f not in m:
                errors.append(f"measurement {m.get('measurement_id','<no id>')}: missing field '{f}'")
        mid = m.get("measurement_id")
        if mid in seen_m:
            errors.append(f"duplicate measurement_id {mid}")
        seen_m.add(mid)
        if m.get("artifact_id") not in ids:
            errors.append(f"measurement {mid}: references unknown artifact {m.get('artifact_id')}")

    for c in accs:
        if c.get("artifact_id") not in ids:
            errors.append(f"acceptance {c.get('acceptance_id')}: references unknown artifact")

    # --- fan-out ---
    per = collections.Counter(m["artifact_id"] for m in meas if m.get("artifact_id") in ids)
    scored = [a for a in arts if a.get("api_status") == "ok"]
    unmeasured = [a["artifact_id"] for a in scored if per.get(a["artifact_id"], 0) == 0]
    fan = (sum(per.values()) / len(per)) if per else 0.0

    print(f"artifacts:            {len(arts):,}")
    print(f"  ok:                 {len(scored):,}")
    print(f"  refusal/error/etc:  {len(arts)-len(scored):,}  (retained: cost and latency were still spent)")
    print(f"measurements:         {len(meas):,}")
    print(f"acceptance records:   {len(accs):,}")
    print(f"distinct output hashes stored: {len(loc_by_hash):,}")
    print(f"duplicate media copies:        {len(dupe_copies)}")
    print(f"MEAN MEASUREMENTS PER SCORED ARTIFACT: {fan:.2f}")
    if per:
        print(f"  min {min(per.values())} / max {max(per.values())}")
    print(f"capability coverage:  {len({m['capability_id'] for m in meas})} distinct capability ids")
    if unmeasured:
        print(f"[WARN] {len(unmeasured)} successful artifact(s) carry no measurement — a paid generation nobody scored")

    if fan <= 1.0 and per:
        errors.append(f"fan-out is {fan:.2f}: the archive is not reusing generations across measurements")

    print()
    if errors:
        for e in errors[:25]:
            print(f"[FAIL] {e}")
        if len(errors) > 25:
            print(f"[FAIL] … and {len(errors)-25} more")
        print(f"\nRESULT: {len(errors)} schema violation(s).")
        sys.exit(1)
    print("[PASS] every measurement resolves to a stored artifact")
    print("[PASS] no output is stored more than once")
    print("[PASS] refusals and errors are retained with null output hashes")
    print("[PASS] every artifact carries a cost reference")
    print(f"[PASS] fan-out {fan:.2f} measurements per scored artifact — one generation, many measurements")
    sys.exit(0)


if __name__ == "__main__":
    main()
