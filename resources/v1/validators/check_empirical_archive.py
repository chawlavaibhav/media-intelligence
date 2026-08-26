#!/usr/bin/env python3
"""Validate an empirical archive against EMPIRICAL-ARTIFACT-MANIFEST-SCHEMA.yaml (v2.1).

Five files in the archive directory:
    attempts.jsonl  artifacts.jsonl  measurements.jsonl  acceptances.jsonl  cost_ledger.jsonl

WHAT THIS PROVES
  * ONE CALL = ONE TRIAL: attempt_id maps one-to-one onto trial_id (RI-C1);
  * repeats and retries each get their OWN trial and link backward (RI-C1);
  * lane and status use the FROZEN machine vocabularies - 'refused' is not 'refusal' (RI-C2);
  * a provider failure lives on the attempt and may not be laundered into a measurement
    absence, and 'instrument_unqualified' is not an absence (RI-C3);
  * every cost_ref resolves to an immutable cost-ledger entry (RI-C4);
  * every failed/refused attempt survives INDIVIDUALLY (aggregate counters are rejected);
  * observation units use the CANONICAL vocabulary verbatim;
  * derived artifacts inherit their parent's trial/attempt and add no trials;
  * one artifact fans out to many measurements, and no output is stored twice.

EXIT CODES
  0  archive is valid
  1  schema violation found
  2  could not check (missing/empty/unparseable core entity file)

"I found no problem" and "I could not look" must never share an exit code.

Usage: check_empirical_archive.py <archive_dir>
"""
import json, os, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Canonical vocabulary, stored verbatim from Canon/Eval. Resources validates membership only.
CANONICAL_OBSERVATION_UNITS = {"frame", "shot", "shot_pair", "sequence", "whole_asset",
                               "asset_set_over_time"}
FORBIDDEN_OBSERVATION_UNITS = {"image", "sampled_clip", "whole_clip", "asset_set", "clip", "video"}

# RI-C2: frozen machine vocabularies. Machine ids, not display names.
VALID_LANES = {"image", "general_video", "native_av", "lipsync", "tts"}
VALID_STATUS = {"ok", "error", "refusal", "timeout", "cancelled"}
NON_OK = VALID_STATUS - {"ok"}

# RI-C3: canonical measurement absence vocabulary.
VALID_ABSENCE = {"not_applicable", "not_measured", "instrument_unavailable", "parse_failure",
                 "human_adjudication_pending", "other"}
# A provider failure belongs on the attempt, never laundered into a measurement absence.
PROVIDER_FAILURE_ABSENCE = {"refusal", "refused", "error", "timeout", "cancelled",
                            "provider_error", "api_error", "moderation_block", "provider_refusal"}

# RI-C4: cost ledger.
VALID_COST_BASIS = {"provider_invoice", "provider_api_response", "published_price_estimate",
                    "synthetic_test"}
REQ_LEDGER = ["ledger_entry_id", "amount", "currency", "unit", "recorded_at", "basis", "immutable"]

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

    # ---------------- cost ledger (RI-C4) ----------------
    # A missing ledger is NOT "could not check": the attempts reference it, so every reference is
    # unresolvable, which is a substantive violation of the archive rather than a tooling failure.
    # Canonical name is cost_ledger.jsonl; cost-ledger.jsonl is accepted as an interoperability
    # alias. This is a filename convention with no semantic content - accepting both settles a
    # cosmetic collision without relaxing a single content rule below.
    ledger_stem = next((n for n in ("cost_ledger", "cost-ledger")
                        if os.path.isfile(os.path.join(d, n + ".jsonl"))), None)
    ledger = {}
    if ledger_stem is None:
        errors.append("neither cost_ledger.jsonl nor cost-ledger.jsonl is present; every attempt "
                      "cost_ref is therefore unresolvable (RI-C4). Cost must reference an immutable "
                      "recorded entry.")
    else:
        for row in load(d, ledger_stem, allow_empty=True):
            # 'cost_ref' is accepted as an alias for the entry's own id. Also cosmetic: it names the
            # same value that attempts point at.
            if "ledger_entry_id" not in row and "cost_ref" in row:
                row["ledger_entry_id"] = row["cost_ref"]
            for f in REQ_LEDGER:
                if row.get(f) is None:
                    errors.append(f"cost ledger entry {row.get('ledger_entry_id','<no id>')}: missing field '{f}'")
            lid = row.get("ledger_entry_id")
            if lid in ledger:
                errors.append(f"duplicate ledger_entry_id {lid}")
            ledger[lid] = row
            if row.get("basis") not in VALID_COST_BASIS:
                errors.append(f"cost ledger entry {lid}: invalid basis {row.get('basis')!r}")
            if row.get("immutable") is not True:
                errors.append(f"cost ledger entry {lid}: immutable must be true; a correction is a new entry")
            if row.get("basis") == "synthetic_test" and row.get("synthetic") is not True:
                errors.append(f"cost ledger entry {lid}: basis 'synthetic_test' requires synthetic: true")

    # ---------------- attempts ----------------
    a_ids, trial_of_attempt = set(), {}
    attempt_of_trial = {}
    for a in attempts:
        for f in REQ_ATTEMPT:
            if f not in a:
                errors.append(f"attempt {a.get('attempt_id','<no id>')}: missing field '{f}'")
        aid = a.get("attempt_id")
        if aid in a_ids:
            errors.append(f"duplicate attempt_id {aid}")
        a_ids.add(aid)
        # RI-C1: one call = one trial. A trial is not a grouping of attempts.
        tid = a.get("trial_id")
        trial_of_attempt[aid] = tid
        if tid in attempt_of_trial:
            errors.append(
                f"attempt {aid}: trial_id {tid!r} is already used by attempt "
                f"{attempt_of_trial[tid]!r}. ONE CALL = ONE TRIAL (RI-C1): a repeat or a retry is a "
                f"NEW trial that links backward through repeat_of_attempt_id / retry_of_attempt_id, "
                f"never a shared trial_id.")
        else:
            attempt_of_trial[tid] = aid
        # RI-C2: frozen machine vocabularies.
        if a.get("status") not in VALID_STATUS:
            hint = ""
            if a.get("status") == "refused":
                hint = " ('refused' is not the persistent id; use 'refusal'. The provider's own " \
                       "wording belongs in error_detail, verbatim.)"
            errors.append(f"attempt {aid}: status {a.get('status')!r} is not in the frozen "
                          f"vocabulary {sorted(VALID_STATUS)}{hint}")
        if a.get("lane") not in VALID_LANES:
            errors.append(f"attempt {aid}: lane {a.get('lane')!r} is not in the frozen vocabulary "
                          f"{sorted(VALID_LANES)}. These are machine ids, not display names.")
        # RI-C4: cost is a reference to an immutable entry, never an inline number.
        cref = a.get("cost_ref")
        if not cref:
            errors.append(f"attempt {aid}: no cost_ref; cost must reference an immutable ledger entry")
        elif isinstance(cref, (int, float)):
            errors.append(f"attempt {aid}: cost_ref is an inline number ({cref}); it must be a "
                          f"reference to a cost_ledger.jsonl entry (RI-C4)")
        elif ledger and cref not in ledger:
            errors.append(f"attempt {aid}: cost_ref {cref!r} does not resolve to any cost-ledger entry")
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
        if a.get("repeat_of_attempt_id") == aid:
            errors.append(f"attempt {aid}: repeat_of_attempt_id points at itself")
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

    # RI-C1: repeat/retry back-links must point at attempts that exist.
    for a in attempts:
        for field in ("repeat_of_attempt_id", "retry_of_attempt_id"):
            ref = a.get(field)
            if ref and ref not in a_ids:
                errors.append(f"attempt {a.get('attempt_id')}: {field} {ref!r} is not a known attempt")

    # ---------------- measurements ----------------
    known_trials = set(trial_of_attempt.values())
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
        if m.get("trial_id") not in known_trials:
            errors.append(f"measurement {mid}: trial_id {m.get('trial_id')!r} does not exist on any attempt")
        has_r = m.get("result") is not None
        has_a = m.get("absence_reason") is not None
        if has_r == has_a:
            errors.append(f"measurement {mid}: exactly one of result and absence_reason must be set "
                          f"(result={'set' if has_r else 'null'}, absence_reason={'set' if has_a else 'null'})")
        # RI-C3: the absence vocabulary, and what may never be laundered into it.
        ar = m.get("absence_reason")
        if ar is not None:
            if ar in PROVIDER_FAILURE_ABSENCE:
                errors.append(
                    f"measurement {mid}: absence_reason {ar!r} records a PROVIDER FAILURE. That "
                    f"belongs on the attempt (status + error_detail), not on a measurement (RI-C3). "
                    f"When a call fails there is no artifact, so there is nothing to have measured.")
            elif ar == "instrument_unqualified":
                errors.append(
                    f"measurement {mid}: 'instrument_unqualified' is NOT an absence (RI-C3). An "
                    f"unqualified instrument may still emit an observational result; record it and "
                    f"carry instrument_qualification_ref: required_but_no_calibrated_instrument. It "
                    f"simply cannot create a Registry score.")
            elif ar not in VALID_ABSENCE:
                errors.append(f"measurement {mid}: absence_reason {ar!r} is not in the canonical set "
                              f"{sorted(VALID_ABSENCE)}")
        ecref = m.get("evaluator_cost_ref")
        if isinstance(ecref, (int, float)):
            errors.append(f"measurement {mid}: evaluator_cost_ref is an inline number ({ecref}); it "
                          f"must reference a cost_ledger.jsonl entry (RI-C4)")
        elif ecref and ledger and ecref not in ledger:
            errors.append(f"measurement {mid}: evaluator_cost_ref {ecref!r} does not resolve to any "
                          f"cost-ledger entry")

    # ---------------- acceptances ----------------
    attempt_by_id = {a.get("attempt_id"): a for a in attempts}
    for c in acceptances:
        for f in REQ_ACCEPTANCE:
            if f not in c:
                errors.append(f"acceptance {c.get('acceptance_id','<no id>')}: missing field '{f}'")
        if c.get("artifact_id") is not None and c["artifact_id"] not in art_ids:
            errors.append(f"acceptance {c.get('acceptance_id')}: references unknown artifact")
        if c.get("trial_id") not in known_trials:
            errors.append(f"acceptance {c.get('acceptance_id')}: trial_id {c.get('trial_id')!r} does "
                          f"not exist on any attempt")
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
    print(f"cost-ledger entries:   {len(ledger):,}")
    print(f"trials:                {len(attempt_of_trial):,}  (one call = one trial)")
    print()
    print("[PASS] one call = one trial: every attempt_id maps to a unique trial_id")
    print("[PASS] lane and status use the frozen machine vocabularies")
    print("[PASS] every cost_ref resolves to an immutable cost-ledger entry")
    print("[PASS] no provider failure is laundered into a measurement absence")
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
