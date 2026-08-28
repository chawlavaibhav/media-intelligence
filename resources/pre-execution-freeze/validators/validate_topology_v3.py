#!/usr/bin/env python3
"""Fail-closed validator for the v3 outcome/production topology.

    validate_topology_v3.py <archive.yaml> [--expect-fail]

Enforces the twelve mechanical gates in OUTCOME-PRODUCTION-TOPOLOGY-v3.yaml:

  G1  one provider call = one trial; no two attempts share a trial_id
  G2  a local/human step must not carry provider attempts
  G3  no unknown artifact parent
  G4  no cycle in the artifact parent graph
  G5  parent positions unique and contiguous from 0 where ordering applies
  G6  no artifact claiming a trial/attempt that does not exist
  G7  an accepted outcome must have a final artifact, present in its own provenance
  G8  a local deterministic step must carry a complete, resolvable transform recipe
  G9  no historical backfill: a pre-v3 record must not assert v3 outcome/job context
  G10 failed/refused attempts persist individually with a reason
  G11 request lineage must never be populated from a media lineage id
  G12 v3 attempts carry the full inherited v2.1 call provenance; eval_item_id is
      required for benchmark/eval attempts and must not be fabricated on
      production-job attempts (Controller-approved conditional override,
      coordination/decisions/CONTROLLER-PREPILOT-RETURN-REVIEW-1-2026-08-28.md)

EXIT CODES
  0  archive is valid
  1  gate violation found
  2  could not check (missing/empty/unparseable input)

"I found no problem" and "I could not look" never share an exit code.
"""
import os, sys, collections

try:
    import yaml
except ImportError:
    print("[FAIL] PyYAML not available", file=sys.stderr); sys.exit(2)

VALID_STATUS = {"ok", "error", "refusal", "timeout", "cancelled"}
NON_OK = VALID_STATUS - {"ok"}
VALID_MODE = {"provider_call", "local_deterministic", "human"}
VALID_ORDERING = {"ordered", "unordered"}
ORDERED_ROLES = {"source", "overlay", "grade_source"}     # roles where sequence carries meaning
REQ_RECIPE = ["transform_ref", "tool", "tool_version", "operation", "params_hash", "params_location"]
# Any id in this namespace is a MEDIA lineage id and must never appear as a request lineage id.
MEDIA_LINEAGE_PREFIXES = ("lin_cvit", "lin_bhashini", "lin_diffusiondb", "lin_konstanz",
                          "lin_tigerlab", "lin_kwaivgi", "lin_google", "lin_abo", "content::",
                          "sha256:")
# ---- G12: inherited v2.1 attempt provenance, mechanically enforced for v3 attempts ----
VALID_ATTEMPT_KIND = {"production", "benchmark_eval"}
# Must be present AND non-null on every v3 attempt.
G12_REQUIRED_NON_NULL = ("provider", "model_id", "model_version", "endpoint", "workflow",
                         "prompt_hash", "config_hash", "config_location", "requested_at",
                         "cost_ref", "storage_class")
# Key must be PRESENT; null is a legitimate recorded value (a call that never completed;
# a first attempt with no prior repeat/retry). An absent key is not the same fact as null.
G12_REQUIRED_KEYS_NULLABLE = ("completed_at", "repeat_of_attempt_id", "retry_of_attempt_id")


def fatal(m):
    print(f"[FAIL] {m}", file=sys.stderr); sys.exit(2)


def idx(rows, key):
    return {r[key]: r for r in (rows or []) if isinstance(r, dict) and key in r}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    expect_fail = "--expect-fail" in sys.argv
    if len(args) != 1:
        fatal("usage: validate_topology_v3.py <archive.yaml> [--expect-fail]")
    if not os.path.isfile(args[0]):
        fatal(f"archive not found: {args[0]}")
    d = yaml.safe_load(open(args[0]))
    if not d:
        fatal("archive parsed to nothing")
    for req in ("jobs", "outcomes", "sets", "units", "steps", "artifacts"):
        if req not in d:
            fatal(f"archive is missing the '{req}' section; refusing to validate a partial archive")

    jobs = idx(d.get("jobs"), "job_id")
    outcomes = idx(d.get("outcomes"), "outcome_id")
    sets_ = idx(d.get("sets"), "set_id")
    units = idx(d.get("units"), "unit_id")
    steps = idx(d.get("steps"), "step_id")
    attempts = idx(d.get("attempts"), "attempt_id")
    artifacts = idx(d.get("artifacts"), "artifact_id")
    recipes = idx(d.get("transform_recipes"), "transform_ref")
    accs = d.get("outcome_acceptance") or []
    schema_era = d.get("schema_era", "v3")

    e = []          # (gate, message)
    def bad(g, m):
        e.append((g, m))

    # ---- G9: historical backfill -------------------------------------------------
    if schema_era in ("v2.1", "pre_v3"):
        for name, rows in (("jobs", d.get("jobs")), ("outcomes", d.get("outcomes")),
                           ("sets", d.get("sets")), ("units", d.get("units"))):
            if rows:
                bad("G9", f"archive declares schema_era {schema_era!r} but asserts {len(rows)} "
                          f"{name} record(s). Pre-v3 archives had no outcome/job context and must "
                          f"not be backfilled with invented context; use not_recorded_pre_v3.")
        for a in (d.get("artifacts") or []):
            if a.get("producing_step_id"):
                bad("G9", f"artifact {a.get('artifact_id')}: pre-v3 archive asserts a producing_step_id")

    # ---- G11: request lineage vs media lineage -----------------------------------
    for j in jobs.values():
        rl = j.get("request_lineage_id")
        if rl is None:
            bad("G11", f"job {j.get('job_id')}: no request_lineage_id (unknown is INDETERMINATE, "
                       f"and must be recorded as such rather than omitted)")
        elif any(str(rl).startswith(p) for p in MEDIA_LINEAGE_PREFIXES):
            bad("G11", f"job {j.get('job_id')}: request_lineage_id {rl!r} is a MEDIA lineage id. "
                       f"A brief's provenance and a photograph's provenance are different facts and "
                       f"must never share a namespace.")

    # ---- G1: one call = one trial -------------------------------------------------
    trial_owner = {}
    for a in attempts.values():
        aid, tid = a.get("attempt_id"), a.get("trial_id")
        if tid is None:
            bad("G1", f"attempt {aid}: no trial_id")
        elif tid in trial_owner:
            bad("G1", f"attempt {aid}: trial_id {tid!r} already used by attempt {trial_owner[tid]!r}. "
                      f"ONE CALL = ONE TRIAL: a repeat or retry is a NEW trial linked backward.")
        else:
            trial_owner[tid] = aid
        if a.get("status") not in VALID_STATUS:
            bad("G1", f"attempt {aid}: status {a.get('status')!r} not in the frozen vocabulary")
        # ---- G10: failures persist individually with a reason
        if a.get("status") in NON_OK and not a.get("error_detail"):
            bad("G10", f"attempt {aid}: status {a.get('status')!r} with no error_detail; a failure "
                       f"with no recorded reason is a row, not preserved evidence")
        # ---- G12: inherited v2.1 call provenance, fail-closed (v3 attempts only;
        # historical pre-v3 archives keep v2.1 semantics unchanged and are validated
        # by the v2.1 validator, never reinterpreted here)
        if schema_era not in ("v2.1", "pre_v3"):
            kind = a.get("attempt_kind")
            if kind not in VALID_ATTEMPT_KIND:
                bad("G12", f"attempt {aid}: attempt_kind {kind!r} is not one of "
                           f"{sorted(VALID_ATTEMPT_KIND)}. Without a declared kind the "
                           f"eval_item_id rule cannot be applied, so the row is refused "
                           f"rather than guessed at (fail-closed).")
            for f in G12_REQUIRED_NON_NULL:
                if a.get(f) in (None, ""):
                    bad("G12", f"attempt {aid}: required inherited field '{f}' is missing "
                               f"or null. v3 inherits the v2.1 attempt contract; an "
                               f"attempt without its call identity/provenance is not "
                               f"verifiable evidence.")
            for f in G12_REQUIRED_KEYS_NULLABLE:
                if f not in a:
                    bad("G12", f"attempt {aid}: key '{f}' is absent. Null is a recorded "
                               f"value ('never completed' / 'no prior attempt'); an "
                               f"absent key is an unrecorded fact and is refused.")
            rah = a.get("reference_asset_hashes", None)
            if not isinstance(rah, list):
                bad("G12", f"attempt {aid}: reference_asset_hashes must be a list "
                           f"(empty list if none), got {type(rah).__name__}")
            if "repeat_index" not in a or a.get("repeat_index") is None:
                bad("G12", f"attempt {aid}: repeat_index is required on every attempt")
            if a.get("retry_of_attempt_id") is not None and not a.get("retry_reason"):
                bad("G12", f"attempt {aid}: retry_of_attempt_id set without retry_reason; "
                           f"repeat and retry must stay distinguishable")
            if kind == "benchmark_eval" and not a.get("eval_item_id"):
                bad("G12", f"attempt {aid}: benchmark/eval attempt with no eval_item_id; "
                           f"v2.1 requires it exactly as written for benchmark attempts")
            if kind == "production" and a.get("eval_item_id") is not None:
                bad("G12", f"attempt {aid}: production-job attempt carries eval_item_id "
                           f"{a.get('eval_item_id')!r}. A production attempt serves a "
                           f"brief (via step -> unit -> set -> outcome -> job -> "
                           f"brief_ref); linking it to a benchmark item would fabricate "
                           f"provenance and must not happen.")

    # ---- G2 / G8: step execution mode ---------------------------------------------
    for s in steps.values():
        sid, mode = s.get("step_id"), s.get("execution_mode")
        if mode not in VALID_MODE:
            bad("G2", f"step {sid}: execution_mode {mode!r} invalid")
            continue
        att = s.get("attempt_ids") or []
        if mode == "provider_call":
            if not att:
                bad("G2", f"step {sid}: provider_call with no attempt_ids")
            for a in att:
                if a not in attempts:
                    bad("G6", f"step {sid}: references attempt {a!r} that does not exist")
        else:
            if att:
                bad("G2", f"step {sid}: execution_mode {mode!r} carries {len(att)} provider "
                          f"attempt(s). A local or human step MUST NOT manufacture a provider "
                          f"attempt - it would create a trial that never happened and corrupt every "
                          f"per-trial count.")
        if mode == "local_deterministic":
            tr = s.get("transform_ref")
            if not tr:
                bad("G8", f"step {sid}: local_deterministic with no transform_ref; the operation "
                          f"would be unreconstructible")
            elif tr not in recipes:
                bad("G8", f"step {sid}: transform_ref {tr!r} does not resolve to a recipe")
            else:
                for f in REQ_RECIPE:
                    if not recipes[tr].get(f):
                        bad("G8", f"transform recipe {tr}: missing '{f}'")
        if mode == "human" and not s.get("operator_ref"):
            bad("G2", f"step {sid}: human step with no operator_ref")
        if s.get("unit_id") not in units:
            bad("G3", f"step {sid}: references unknown unit {s.get('unit_id')!r}")

    # ---- ordering integrity of sets/units ----------------------------------------
    for st in sets_.values():
        if st.get("ordering") not in VALID_ORDERING:
            bad("G5", f"set {st.get('set_id')}: ordering {st.get('ordering')!r} invalid")
        if st.get("outcome_id") not in outcomes:
            bad("G3", f"set {st.get('set_id')}: references unknown outcome")
    by_set = collections.defaultdict(list)
    for u in units.values():
        by_set[u.get("set_id")].append(u)
        if u.get("set_id") not in sets_:
            bad("G3", f"unit {u.get('unit_id')}: references unknown set {u.get('set_id')!r}")
    for sid, us in by_set.items():
        st = sets_.get(sid)
        if not st:
            continue
        if st.get("ordering") == "ordered":
            pos = [u.get("position") for u in us]
            if any(p is None for p in pos):
                bad("G5", f"set {sid}: ordered set has a unit with no position")
            elif len(set(pos)) != len(pos):
                dupes = sorted({p for p in pos if pos.count(p) > 1})
                bad("G5", f"set {sid}: duplicate unit positions {dupes}; the order is ambiguous")
        else:
            if any(u.get("position") is not None for u in us):
                bad("G5", f"set {sid}: unordered set has units carrying positions; order must not be "
                          f"inferable where it has no meaning")

    # ---- G3 / G5 / G6: artifacts --------------------------------------------------
    for a in artifacts.values():
        aid = a.get("artifact_id")
        if not a.get("output_hash"):
            bad("G6", f"artifact {aid}: output_hash is null; an artifact IS its bytes")
        st_id = a.get("producing_step_id")
        if st_id not in steps:
            bad("G3", f"artifact {aid}: producing_step_id {st_id!r} does not exist")
            continue
        mode = steps[st_id].get("execution_mode")
        att = a.get("attempt_id")
        if mode == "provider_call":
            if att is None:
                bad("G6", f"artifact {aid}: produced by a provider_call step but claims no attempt")
            elif att not in attempts:
                bad("G6", f"artifact {aid}: claims attempt {att!r} that does not exist")
            elif a.get("trial_id") != attempts[att].get("trial_id"):
                bad("G6", f"artifact {aid}: trial_id does not match its attempt's trial_id")
        else:
            if att is not None:
                bad("G2", f"artifact {aid}: produced by a {mode} step but claims attempt {att!r}. "
                          f"A local or human step produces no trial.")
            if a.get("trial_id") is not None:
                bad("G6", f"artifact {aid}: produced by a {mode} step but claims a trial_id")
        # parents
        parents = a.get("parents") or []
        seen = set()
        ordered_positions = []
        for p in parents:
            pid = p.get("parent_artifact_id")
            if pid not in artifacts:
                bad("G3", f"artifact {aid}: parent {pid!r} does not exist")
            if pid in seen:
                bad("G5", f"artifact {aid}: parent {pid!r} listed more than once")
            seen.add(pid)
            if p.get("role") in ORDERED_ROLES:
                ordered_positions.append(p.get("position"))
        if ordered_positions:
            if any(x is None for x in ordered_positions):
                bad("G5", f"artifact {aid}: an order-bearing parent has no position")
            else:
                if len(set(ordered_positions)) != len(ordered_positions):
                    bad("G5", f"artifact {aid}: duplicate parent positions {sorted(ordered_positions)}; "
                              f"the composition order is ambiguous")
                elif sorted(ordered_positions) != list(range(len(ordered_positions))):
                    bad("G5", f"artifact {aid}: parent positions {sorted(ordered_positions)} are not "
                              f"contiguous from 0; a gap makes the intended order unknowable")

    # ---- G4: acyclicity -----------------------------------------------------------
    colour = {}
    def visit(n, stack):
        if colour.get(n) == "done":
            return
        if colour.get(n) == "open":
            bad("G4", f"cycle in artifact parent graph: {' -> '.join(stack + [n])}")
            return
        colour[n] = "open"
        for p in (artifacts.get(n, {}).get("parents") or []):
            pid = p.get("parent_artifact_id")
            if pid in artifacts:
                visit(pid, stack + [n])
        colour[n] = "done"
    for n in artifacts:
        visit(n, [])

    # ---- G7: accepted outcome must have a final artifact in its own provenance -----
    def outcome_artifacts(oid):
        uids = {u["unit_id"] for u in units.values()
                if sets_.get(u.get("set_id"), {}).get("outcome_id") == oid}
        sids = {s["step_id"] for s in steps.values() if s.get("unit_id") in uids}
        return {aid for aid, r in artifacts.items() if r.get("producing_step_id") in sids}

    for c in accs:
        oid = c.get("outcome_id")
        if oid not in outcomes:
            bad("G3", f"acceptance {c.get('acceptance_id')}: unknown outcome {oid!r}")
            continue
        if str(c.get("decided_by", "")).lower().startswith("resources"):
            bad("G7", f"acceptance {c.get('acceptance_id')}: decided_by must never be Resources")
        if not c.get("accepted"):
            continue
        fa = outcomes[oid].get("final_artifact_id")
        if not fa:
            bad("G7", f"outcome {oid}: ACCEPTED but final_artifact_id is null. You cannot accept nothing.")
        elif fa not in artifacts:
            bad("G7", f"outcome {oid}: final_artifact_id {fa!r} does not exist")
        elif fa not in outcome_artifacts(oid):
            bad("G7", f"outcome {oid}: final artifact {fa!r} is not in its own provenance")

    # ---- report -------------------------------------------------------------------
    print(f"schema_era:        {schema_era}")
    print(f"jobs {len(jobs)} · outcomes {len(outcomes)} · sets {len(sets_)} · units {len(units)} · "
          f"steps {len(steps)} · attempts {len(attempts)} · artifacts {len(artifacts)}")
    mode_counts = collections.Counter(s.get("execution_mode") for s in steps.values())
    print(f"step modes:        {dict(mode_counts)}")
    print(f"trials:            {len(trial_owner)}  (one call = one trial)")
    nonok = [a for a in attempts.values() if a.get("status") in NON_OK]
    print(f"failed/refused:    {len(nonok)}  (each preserved individually with its reason)")
    kind_counts = collections.Counter(a.get("attempt_kind") for a in attempts.values())
    print(f"attempt kinds:     {dict(kind_counts)}")
    multi = [a for a in artifacts.values() if len(a.get('parents') or []) > 1]
    print(f"multi-parent artifacts: {len(multi)}")
    local_arts = [a for a in artifacts.values()
                  if steps.get(a.get("producing_step_id"), {}).get("execution_mode") != "provider_call"]
    print(f"artifacts from local/human steps (no attempt): {len(local_arts)}")
    print()

    if e:
        by_gate = collections.Counter(g for g, _ in e)
        for g, m in e[:30]:
            print(f"[FAIL:{g}] {m}")
        if len(e) > 30:
            print(f"[FAIL] … and {len(e)-30} more")
        print(f"\nRESULT: {len(e)} gate violation(s): {dict(sorted(by_gate.items()))}")
        sys.exit(0 if expect_fail else 1)
    if expect_fail:
        print("[FAIL] expected a gate violation but the archive validated cleanly")
        sys.exit(1)
    print("[PASS] G1  one provider call = one trial")
    print("[PASS] G2  local/human steps carry no provider attempts")
    print("[PASS] G3  every parent, unit, set and step reference resolves")
    print("[PASS] G4  artifact parent graph is acyclic")
    print("[PASS] G5  parent and unit ordering is unambiguous")
    print("[PASS] G6  no artifact claims a trial that does not exist")
    print("[PASS] G7  accepted outcomes have a final artifact in their own provenance")
    print("[PASS] G8  local deterministic steps carry complete transform recipes")
    print("[PASS] G9  no historical backfill of v3 context")
    print("[PASS] G10 failed/refused attempts persist individually with reasons")
    print("[PASS] G11 request lineage is not populated from media lineage")
    print("[PASS] G12 attempts carry full inherited call provenance; eval_item_id "
          "required for benchmark_eval, absent/null for production")
    sys.exit(0)


if __name__ == "__main__":
    main()
