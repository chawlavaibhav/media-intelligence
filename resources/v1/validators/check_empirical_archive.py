#!/usr/bin/env python3
"""Validate an empirical archive against EMPIRICAL-ARTIFACT-MANIFEST-SCHEMA.yaml (v2).

Four persistent entities, one file each in the archive directory:
    attempts.jsonl  artifacts.jsonl  measurements.jsonl  acceptances.jsonl

WHAT THIS PROVES
  * every failed/refused attempt survives INDIVIDUALLY (aggregate counters are rejected);
  * status 'ok' <=> exactly one artifact; any other status <=> none;
  * repeats and retries are distinct, and only retries appear in an accepted-outcome retry chain;
  * observation units use the CANONICAL vocabulary verbatim, not Resources-local synonyms;
  * derived artifacts inherit their parent's trial/attempt and never become independent trials;
  * one artifact fans out to many measurements, and no output is stored twice.

EXIT CODES
  0  archive is valid
  1  schema violation found
  2  could not check (missing/empty/unparseable input)

"I found no problem" and "I could not look" must never share an exit code.

Usage: check_empirical_archive.py <archive_dir>
"""
import json, os, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Canonical vocabulary, stored verbatim from Canon/Eval. Resources validates membership only.
CANONICAL_OBSERVATION_UNITS = {"frame", "shot", "shot_pair", "sequence", "whole_asset",
                               "asset_set_over_time"}
# v1 Resources-local coinage. Explicitly rejected so it cannot creep back in.
FORBIDDEN_OBSERVATION_UNITS = {"image", "sampled_clip", "whole_clip", "asset_set", "clip", "video"}

VALID_STATUS = {"ok", "error", "refusal", "timeout", "cancelled"}
NON_OK = VALID_STATUS - {"ok"}

REQ_ATTEMPT = ["attempt_id", "trial_id", "eval_item_id", "provider", "model_id", "model_version",
               "endpoint", "workflow", "lane", "prompt_hash", "config_hash", "config_location",
               "reference_asset_hashes", "requested_at", "completed_at", "status", "cost_ref",
               "storage_class", "repeat_index"]
REQ_ARTIFACT = ["artifact_id", "attempt_id", "trial_id", "output_hash", "output_bytes",
                "output_location", "media_kind", "storage_class"]
REQ_MEASUREMENT = ["measurement_id", "trial_id", "capability_id", "instrument_ref",
                   "instrument_version", "instrument_config_hash", "instrument_qualification_ref",
                   "observation_unit", "measured_at"]
REQ_ACCEPTANCE = ["acceptance_id", "trial_id", "accepted", "decided_by", "decided_at", "brief_ref"]

FILES = ["attempts", "artifacts", "measurements", "acceptances"]


def fatal(msg):
    print(f"[FAIL] {msg}", file=sys.stderr)
    sys.exit(2)


def load(d, name, allow_empty=False):
    path = os.path.join(d, name + ".jsonl")
    if not os.path.isfile(path):
        fatal(f"{name}.jsonl not found in {d}")
    rows = []
    with open(path) as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                fatal(f"{name}.jsonl line {n} unparseable: {e}")
    if not rows and not allow_empty:
        fatal(f"{name}.jsonl holds 0 rows; refusing to validate an empty archive")
    return rows


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if len(args) != 1:
        fatal("usage: check_empirical_archive.py <archive_dir>")
    d = args[0]
    if not os.path.isdir(d):
        fatal(f"archive directory not found: {d}")

    attempts = load(d, "attempts")
    artifacts = load(d, "artifacts")
    measurements = load(d, "measurements")
    acceptances = load(d, "acceptances", allow_empty=True)

    errors = []

    # ---------------- attempts ----------------
    a_ids, trial_of_attempt = set(), {}
    for a in attempts:
        for f in REQ_ATTEMPT:
            if f not in a:
                errors.append(f"attempt {a.get('attempt_id','<no id>')}: missing field '{f}'")
        aid = a.get("attempt_id")
        if aid in a_ids:
            errors.append(f"duplicate attempt_id {aid}")
        a_ids.add(aid)
        trial_of_attempt[aid] = a.get("trial_id")
        if a.get("status") not in VALID_STATUS:
            errors.append(f"attempt {aid}: invalid status {a.get('status')!r}")
        if not a.get("cost_ref"):
            errors.append(f"attempt {aid}: no cost_ref; cost must never be invented later")
        if a.get("storage_class") != "C_irreproducible_empirical":
            errors.append(f"attempt {aid}: storage_class must be C_irreproducible_empirical")
        if a.get("repeat_index") is None:
            errors.append(f"attempt {aid}: repeat_index is required (reliability repeats must be countable)")
        # Repeat vs retry must not be conflated.
        if a.get("retry_of_attempt_id"):
            if not a.get("retry_reason"):
                errors.append(f"attempt {aid}: retry_of_attempt_id set but no retry_reason")
            if a["retry_of_attempt_id"] == aid:
                errors.append(f"attempt {aid}: retry_of_attempt_id points at itself")
        if a.get("status") in NON_OK and not a.get("error_detail"):
            errors.append(f"attempt {aid}: status {a['status']!r} but no error_detail; "
                          f"a failure with no recorded reason is not preserved evidence")

    # Aggregate reliability counters may NEVER stand in for the individual rows.
    summary_path = os.path.join(d, "reliability_summary.json")
    if os.path.isfile(summary_path):
        try:
            summ = json.load(open(summary_path))
        except json.JSONDecodeError as e:
            fatal(f"reliability_summary.json unparseable: {e}")
        actual = collections.Counter(a.get("status") for a in attempts)
        for status, claimed in (summ.get("status_counts") or {}).items():
            if claimed != actual.get(status, 0):
                errors.append(
                    f"reliability_summary claims {claimed} attempt(s) with status '{status}' but "
                    f"{actual.get(status,0)} row(s) exist. Aggregate counters may not replace "
                    f"individually preserved attempts.")

    # ---------------- artifacts ----------------
    art_ids = set()
    by_attempt = collections.defaultdict(list)
    for r in artifacts:
        for f in REQ_ARTIFACT:
            if f not in r:
                errors.append(f"artifact {r.get('artifact_id','<no id>')}: missing field '{f}'")
        rid = r.get("artifact_id")
        if rid in art_ids:
            errors.append(f"duplicate artifact_id {rid}")
        art_ids.add(rid)
        if not r.get("output_hash"):
            errors.append(f"artifact {rid}: output_hash is null; an artifact IS its bytes")
        if r.get("attempt_id") not in a_ids:
            errors.append(f"artifact {rid}: references unknown attempt {r.get('attempt_id')}")
        else:
            if r.get("derived_from_artifact_id") is None:
                by_attempt[r["attempt_id"]].append(rid)
            if r.get("trial_id") != trial_of_attempt.get(r.get("attempt_id")):
                errors.append(f"artifact {rid}: trial_id does not match its attempt's trial_id")

    # Derived media inherits; it never becomes an independent trial.
    art_by_id = {r.get("artifact_id"): r for r in artifacts}
    for r in artifacts:
        p = r.get("derived_from_artifact_id")
        if p is None:
            continue
        if p not in art_by_id:
            errors.append(f"artifact {r.get('artifact_id')}: derived_from unknown artifact {p}")
            continue
        if not r.get("derivation_type"):
            errors.append(f"artifact {r.get('artifact_id')}: derived but no derivation_type")
        par = art_by_id[p]
        if r.get("trial_id") != par.get("trial_id") or r.get("attempt_id") != par.get("attempt_id"):
            errors.append(f"artifact {r.get('artifact_id')}: derived artifact must inherit its "
                          f"parent's trial_id and attempt_id, never its own")

    # status <-> artifact existence
    for a in attempts:
        n = len(by_attempt.get(a.get("attempt_id"), []))
        if a.get("status") == "ok" and n != 1:
            errors.append(f"attempt {a.get('attempt_id')}: status 'ok' but {n} direct artifact(s); expected exactly 1")
        if a.get("status") in NON_OK and n != 0:
            errors.append(f"attempt {a.get('attempt_id')}: status {a.get('status')!r} but {n} artifact(s); "
                          f"a call that produced nothing must have no artifact row")

    # No output stored twice.
    loc_by_hash = collections.defaultdict(set)
    for r in artifacts:
        if r.get("output_hash"):
            loc_by_hash[r["output_hash"]].add(r.get("output_location"))
    for h, v in loc_by_hash.items():
        if len(v) > 1:
            errors.append(f"output_hash {h[:12]}… stored at {len(v)} distinct locations: duplicate media copy")

    # ---------------- measurements ----------------
    m_ids = set()
    for m in measurements:
        for f in REQ_MEASUREMENT:
            if f not in m:
                errors.append(f"measurement {m.get('measurement_id','<no id>')}: missing field '{f}'")
        mid = m.get("measurement_id")
        if mid in m_ids:
            errors.append(f"duplicate measurement_id {mid}")
        m_ids.add(mid)
        if m.get("artifact_id") is not None and m["artifact_id"] not in art_ids:
            errors.append(f"measurement {mid}: references unknown artifact {m['artifact_id']}")
        u = m.get("observation_unit")
        if u in FORBIDDEN_OBSERVATION_UNITS:
            errors.append(f"measurement {mid}: observation_unit {u!r} is Resources-local coinage. "
                          f"Use the canonical vocabulary verbatim: {sorted(CANONICAL_OBSERVATION_UNITS)}")
        elif u not in CANONICAL_OBSERVATION_UNITS:
            errors.append(f"measurement {mid}: observation_unit {u!r} is not in the canonical vocabulary")
        has_r = m.get("result") is not None
        has_a = m.get("absence_reason") is not None
        if has_r == has_a:
            errors.append(f"measurement {mid}: exactly one of result and absence_reason must be set "
                          f"(result={'set' if has_r else 'null'}, absence_reason={'set' if has_a else 'null'})")

    # ---------------- acceptances ----------------
    attempt_by_id = {a.get("attempt_id"): a for a in attempts}
    for c in acceptances:
        for f in REQ_ACCEPTANCE:
            if f not in c:
                errors.append(f"acceptance {c.get('acceptance_id','<no id>')}: missing field '{f}'")
        if c.get("artifact_id") is not None and c["artifact_id"] not in art_ids:
            errors.append(f"acceptance {c.get('acceptance_id')}: references unknown artifact")
        if str(c.get("decided_by", "")).lower().startswith("resources"):
            errors.append(f"acceptance {c.get('acceptance_id')}: decided_by must never be Resources")
        # Only retries belong in a retry chain.
        chain = c.get("retry_chain") or []
        for idx, aid in enumerate(chain):
            if aid not in a_ids:
                errors.append(f"acceptance {c.get('acceptance_id')}: retry_chain references unknown attempt {aid}")
                continue
            if idx == 0:
                continue
            at = attempt_by_id[aid]
            if not at.get("retry_of_attempt_id"):
                errors.append(
                    f"acceptance {c.get('acceptance_id')}: retry_chain includes {aid}, which is a "
                    f"deliberate reliability repeat (repeat_index={at.get('repeat_index')}), not a "
                    f"retry. Repeats must never enter an accepted-outcome retry chain - it inflates CpAO.")

    # ---------------- fan-out ----------------
    per = collections.Counter(m["artifact_id"] for m in measurements if m.get("artifact_id") in art_ids)
    fan = (sum(per.values()) / len(per)) if per else 0.0
    ok_attempts = [a for a in attempts if a.get("status") == "ok"]
    failed = [a for a in attempts if a.get("status") in NON_OK]
    if per and fan <= 1.0:
        errors.append(f"fan-out is {fan:.2f}: the archive is not reusing artifacts across measurements")

    # ---------------- report ----------------
    print(f"attempts:              {len(attempts):,}")
    print(f"  ok:                  {len(ok_attempts):,}")
    print(f"  failed/refused:      {len(failed):,}  (each preserved individually with its reason)")
    print(f"artifacts:             {len(artifacts):,}")
    print(f"  derived:             {sum(1 for r in artifacts if r.get('derived_from_artifact_id')):,}"
          f"  (inherit parent trial/attempt; never independent trials)")
    print(f"measurements:          {len(measurements):,}")
    print(f"acceptances:           {len(acceptances):,}")
    print(f"distinct output hashes: {len(loc_by_hash):,}")
    print(f"duplicate media copies: {sum(1 for v in loc_by_hash.values() if len(v) > 1)}")
    print(f"MEAN MEASUREMENTS PER ARTIFACT: {fan:.2f}" + (f"  (min {min(per.values())} / max {max(per.values())})" if per else ""))
    print(f"capability ids covered: {len({m.get('capability_id') for m in measurements})}")
    print(f"observation units used: {sorted({m.get('observation_unit') for m in measurements})}")

    print()
    if errors:
        for e in errors[:25]:
            print(f"[FAIL] {e}")
        if len(errors) > 25:
            print(f"[FAIL] … and {len(errors)-25} more")
        print(f"\nRESULT: {len(errors)} schema violation(s).")
        sys.exit(1)
    print("[PASS] every failed/refused attempt is preserved individually with its reason")
    print("[PASS] status 'ok' <=> exactly one artifact; any other status <=> none")
    print("[PASS] repeats and retries are distinct; no repeat appears in a retry chain")
    print("[PASS] observation units use the canonical vocabulary verbatim")
    print("[PASS] derived artifacts inherit their parent's trial and attempt")
    print("[PASS] no output is stored more than once")
    print("[PASS] every attempt carries a cost reference")
    print(f"[PASS] fan-out {fan:.2f} measurements per artifact — one generation, many measurements")
    sys.exit(0)


if __name__ == "__main__":
    main()
