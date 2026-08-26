#!/usr/bin/env python3
"""Fail-closed whole-outcome CpAO recomputation for topology v3.

    recompute_cpao_v3.py <archive.yaml> [--expect-refusal]

TWO REQUIRED VIEWS (Controller integration decision §4.2):
    API/tool CpAO   = api_tool costs only.                DIAGNOSTIC.
    fully-loaded    = api_tool + local_compute + human_required.  PRIMARY BUSINESS METRIC.

WHAT IS COUNTED, per the decision:
  successful, failed, refused and retried provider attempts; paid transforms and evaluator calls;
  repair attempts; material local/deterministic compute where recorded; REQUIRED human review or
  production time; and rejected revisions belonging to the same production journey.

ATTRIBUTION RULE (explicit, and the reason no double counting occurs):
  A cost attaches to the STEP OR ATTEMPT THAT INCURRED IT, never to the edge that consumed it. The
  engine collects the SET of distinct ledger_entry_ids reachable from the accepted outcome and sums
  each EXACTLY ONCE. Production provenance is a DAG - one logo composited into three shots is visited
  three times by a recursive walk - so set semantics, not traversal, is what makes reuse safe.

REVISION JOURNEY:
  If an accepted outcome supersedes earlier rejected outcomes, those belong to the same production
  journey and their costs are included. THE CHAIN IS CUT at any outcome carrying
  scope_change_boundary: true - a customer materially changing the brief opens a new journey rather
  than retroactively charging unrelated earlier work.

EXIT CODES
  0  computed and matched the archive's declared expectation
  1  computed but disagreed with expectation
  2  could not read the input
  3  REFUSED - the evidence cannot support a number (negative controls expect this)
"""
import os, sys, collections

try:
    import yaml
except ImportError:
    print("[FAIL] PyYAML not available", file=sys.stderr); sys.exit(2)

VALID_COST_CLASS = {"api_tool", "local_compute", "human_required", "human_optional"}
FULLY_LOADED = {"api_tool", "local_compute", "human_required"}
API_ONLY = {"api_tool"}


class Refusal(Exception):
    pass


def idx(rows, key):
    return {r[key]: r for r in (rows or []) if isinstance(r, dict) and key in r}


def resolve(cid, ledger, why):
    if cid is None:
        return None
    e = ledger.get(cid)
    if e is None:
        raise Refusal(f"cost_ref {cid!r} ({why}) does not resolve to a ledger entry")
    if e.get("amount") is None:
        raise Refusal(f"ledger entry {cid}: no amount; a missing cost is not a zero cost")
    if not e.get("currency"):
        raise Refusal(f"ledger entry {cid}: no currency")
    if e.get("immutable") is not True:
        raise Refusal(f"ledger entry {cid}: immutable is not true; a mutable cost is not evidence")
    cc = e.get("cost_class")
    if cc not in VALID_COST_CLASS:
        raise Refusal(f"ledger entry {cid}: cost_class {cc!r} not in {sorted(VALID_COST_CLASS)}; "
                      f"an unclassified cost cannot be placed in either CpAO view")
    return float(e["amount"]), e["currency"], cc


def compute(d):
    ledger = idx(d.get("cost_ledger"), "ledger_entry_id")
    attempts = idx(d.get("attempts"), "attempt_id")
    artifacts = idx(d.get("artifacts"), "artifact_id")
    steps = idx(d.get("steps"), "step_id")
    units = idx(d.get("units"), "unit_id")
    sets_ = idx(d.get("sets"), "set_id")
    outcomes = idx(d.get("outcomes"), "outcome_id")
    accs = [a for a in (d.get("outcome_acceptance") or []) if a.get("accepted")]

    if not accs:
        raise Refusal("no accepted outcome: CpAO is UNDEFINED, not zero and not infinity")

    charged = {}                       # ledger_entry_id -> (amount, currency, cost_class, why)

    def charge(cid, why):
        r = resolve(cid, ledger, why)
        if r is None or cid in charged:
            return                     # already counted once: the shared-intermediate case
        amt, cur, cc = r
        charged[cid] = (amt, cur, cc, why)

    def journey(oid, seen=None):
        """The accepted outcome plus every superseded outcome in the same journey."""
        seen = seen or []
        if oid in seen:
            raise Refusal(f"revision chain contains a cycle at {oid!r}")
        seen = seen + [oid]
        o = outcomes.get(oid)
        if o is None:
            raise Refusal(f"outcome {oid!r} does not exist")
        chain = [oid]
        prev = o.get("supersedes_outcome_id")
        if prev:
            p = outcomes.get(prev)
            if p is None:
                raise Refusal(f"outcome {oid}: supersedes unknown outcome {prev!r}")
            if p.get("scope_change_boundary"):
                # Journey stops here: the customer materially changed the brief.
                pass
            else:
                chain += journey(prev, seen)
        return chain

    def charge_outcome(oid):
        uids = {u["unit_id"] for u in units.values()
                if sets_.get(u.get("set_id"), {}).get("outcome_id") == oid}
        if not uids:
            raise Refusal(f"outcome {oid}: no production units resolve to it")
        o_steps = [s for s in steps.values() if s.get("unit_id") in uids]
        if not o_steps:
            raise Refusal(f"outcome {oid}: no production steps resolve to it")
        for s in o_steps:
            mode = s.get("execution_mode")
            for aid in (s.get("attempt_ids") or []):
                a = attempts.get(aid)
                if a is None:
                    raise Refusal(f"step {s.get('step_id')}: attempt {aid!r} does not exist")
                charge(a.get("cost_ref"), f"attempt {aid} (status {a.get('status')})")
            if mode != "provider_call" and (s.get("attempt_ids") or []):
                raise Refusal(f"step {s.get('step_id')}: {mode} step carries provider attempts")
            charge(s.get("cost_ref"), f"step {s.get('step_id')} ({s.get('step_kind')}/{mode})")
        step_ids = {s.get("step_id") for s in o_steps}
        o_arts = {aid for aid, r in artifacts.items() if r.get("producing_step_id") in step_ids}
        for m in (d.get("measurements") or []):
            if m.get("artifact_id") in o_arts:
                charge(m.get("evaluator_cost_ref"), f"measurement {m.get('measurement_id')}")
        return o_arts

    accepted = 0
    for acc in accs:
        oid = acc["outcome_id"]
        accepted += 1
        chain = journey(oid)
        arts = set()
        for o in chain:
            arts |= charge_outcome(o)
        fa = outcomes[oid].get("final_artifact_id")
        if not fa:
            raise Refusal(f"outcome {oid}: ACCEPTED but has no final_artifact_id")
        if fa not in arts:
            raise Refusal(f"outcome {oid}: final artifact {fa!r} is not in its own provenance; "
                          f"the cost total would not describe what was delivered")

    currencies = {c for (_, c, _, _) in charged.values()}
    if len(currencies) > 1:
        raise Refusal(f"mixed currencies {sorted(currencies)}: no exchange rate may be invented")
    cur = currencies.pop() if currencies else None

    by_class = collections.defaultdict(float)
    for amt, _, cc, _ in charged.values():
        by_class[cc] += amt
    api = round(sum(v for k, v in by_class.items() if k in API_ONLY), 10)
    full = round(sum(v for k, v in by_class.items() if k in FULLY_LOADED), 10)
    return {
        "api_tool_cost": api,
        "local_compute_cost": round(by_class.get("local_compute", 0.0), 10),
        "human_required_cost": round(by_class.get("human_required", 0.0), 10),
        "human_optional_excluded": round(by_class.get("human_optional", 0.0), 10),
        "fully_loaded_cost": full,
        "accepted_outcomes": accepted,
        "api_tool_cpao": round(api / accepted, 10),
        "fully_loaded_cpao": round(full / accepted, 10),
        "currency": cur,
        "distinct_cost_entries_counted": len(charged),
        "charged": charged,
    }


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    expect_refusal = "--expect-refusal" in sys.argv
    if len(args) != 1:
        print("[FAIL] usage: recompute_cpao_v3.py <archive.yaml> [--expect-refusal]", file=sys.stderr)
        sys.exit(2)
    if not os.path.isfile(args[0]):
        print(f"[FAIL] archive not found: {args[0]}", file=sys.stderr); sys.exit(2)
    d = yaml.safe_load(open(args[0]))
    if not d:
        print("[FAIL] archive parsed to nothing", file=sys.stderr); sys.exit(2)

    try:
        r = compute(d)
    except Refusal as x:
        print(f"[REFUSED] {x}")
        print("No cost total was produced. Refusing is correct when the evidence cannot support a number.")
        sys.exit(3 if expect_refusal else 2)
    if expect_refusal:
        print(f"[FAIL] expected a refusal but computed {r['fully_loaded_cost']}")
        sys.exit(1)

    print(f"distinct cost entries counted: {r['distinct_cost_entries_counted']}")
    for cid, (amt, cur, cc, why) in sorted(r["charged"].items(), key=lambda x: (x[1][2], x[0])):
        print(f"   [{cc:14s}] {cid:20s} {amt:>8.2f} {cur}   {why}")
    print()
    print(f"  api_tool            {r['api_tool_cost']:>10.2f} {r['currency']}")
    print(f"  local_compute       {r['local_compute_cost']:>10.2f} {r['currency']}")
    print(f"  human_required      {r['human_required_cost']:>10.2f} {r['currency']}")
    if r["human_optional_excluded"]:
        print(f"  human_optional      {r['human_optional_excluded']:>10.2f} {r['currency']}   (EXCLUDED from both views)")
    print(f"  {'-'*44}")
    print(f"  fully-loaded        {r['fully_loaded_cost']:>10.2f} {r['currency']}")
    print(f"  accepted outcomes   {r['accepted_outcomes']:>10d}")
    print()
    print(f"  API/tool CpAO       {r['api_tool_cpao']:>10.2f} {r['currency']}   (diagnostic)")
    print(f"  FULLY-LOADED CpAO   {r['fully_loaded_cpao']:>10.2f} {r['currency']}   (PRIMARY BUSINESS METRIC)")
    print()

    exp = d.get("expected_cpao") or {}
    if not exp:
        print("[FAIL] archive declares no expected_cpao; refusing to call this a pass")
        sys.exit(2)
    bad = [f"{k}: expected {exp[k]!r}, got {r[k]!r}" for k in exp if k in r and exp[k] != r[k]]
    if bad:
        for b in bad:
            print(f"[FAIL] {b}")
        sys.exit(1)
    print("[PASS] recomputed totals match the archive's hand-computed expectation")
    print("[PASS] both required views reported: API/tool (diagnostic) and fully-loaded (primary)")
    print("[PASS] failed, refused and retried attempts are included")
    print("[PASS] local compute and required human time are included")
    print("[PASS] every ledger entry counted exactly once despite downstream reuse")
    sys.exit(0)


if __name__ == "__main__":
    main()
