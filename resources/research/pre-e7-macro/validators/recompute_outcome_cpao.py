#!/usr/bin/env python3
"""Fail-closed whole-outcome CpAO recomputation over the R3-D topology.

    python3 recompute_outcome_cpao.py <fixture.yaml> [--expect-refusal]

CpAO = (total cost of every DISTINCT cost entry in the accepted outcome's provenance closure)
       / (number of accepted outcomes)

THE DOUBLE-COUNTING PROBLEM AND HOW THIS SOLVES IT
Production provenance is a DAG, not a tree: one generated logo can be composited into three shots.
A recursive walk visits that logo once per path and counts its cost three times. So the engine
collects the SET of distinct ledger_entry_ids reachable from the outcome and sums each entry EXACTLY
ONCE. Cost attaches to the step/attempt that incurred it, never to the edge that consumed it.

FAIL-CLOSED. This tool REFUSES to emit a number rather than emit a wrong one. Any of the following
produces a refusal, not a best-effort total:
  * a cost_ref that does not resolve to a ledger entry;
  * a ledger entry missing an amount, currency or immutability guarantee;
  * mixed currencies (no exchange rates are invented, ever);
  * an accepted outcome whose delivered artifact is not in its own provenance;
  * a provider_call step with no attempt, or a local_transform with no transform_ref;
  * zero accepted outcomes (CpAO is undefined, not infinite, and not zero).

EXIT CODES
  0  a total was computed and matches the fixture's expected values
  1  computed, but disagrees with expectation
  2  could not compute (refusal) OR the input could not be read
  3  refusal was expected and correctly produced (used by negative controls)
"""
import os, sys

try:
    import yaml
except ImportError:
    print("[FAIL] PyYAML not available", file=sys.stderr); sys.exit(2)


class Refusal(Exception):
    pass


def load(path):
    if not os.path.isfile(path):
        print(f"[FAIL] fixture not found: {path}", file=sys.stderr); sys.exit(2)
    d = yaml.safe_load(open(path))
    if not d:
        print("[FAIL] fixture parsed to nothing", file=sys.stderr); sys.exit(2)
    return d


def index(rows, key):
    return {r[key]: r for r in (rows or []) if key in r}


def resolve_cost(cid, ledger, why):
    """Return (amount, currency) or raise Refusal. Never guesses, never defaults to zero."""
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
    return float(e["amount"]), e["currency"]


def compute(d):
    ledger = index(d.get("cost_ledger"), "ledger_entry_id")
    attempts = index(d.get("attempts"), "attempt_id")
    artifacts = index(d.get("artifacts"), "artifact_id")
    steps = d.get("steps") or []
    units = index(d.get("units"), "unit_id")
    sets = index(d.get("sets"), "set_id")
    accs = [a for a in (d.get("outcome_acceptance") or []) if a.get("accepted")]

    if not accs:
        raise Refusal("no accepted outcome: CpAO is UNDEFINED, not zero and not infinite")

    # Structural integrity of steps, before any arithmetic.
    for s in steps:
        if s.get("step_kind") == "provider_call" and not s.get("attempt_id"):
            raise Refusal(f"step {s.get('step_id')}: provider_call with no attempt_id")
        if s.get("step_kind") == "local_transform" and not s.get("transform_ref"):
            raise Refusal(f"step {s.get('step_id')}: local_transform with no transform_ref "
                          f"(the operation would be unreproducible)")
        if s.get("step_kind") == "human_edit" and not s.get("operator_ref"):
            raise Refusal(f"step {s.get('step_id')}: human_edit with no operator_ref")

    # DISTINCT cost entries -> the double-counting fix. A set, not a running sum.
    charged = {}          # ledger_entry_id -> (amount, currency, why)
    def charge(cid, why):
        if cid is None:
            return
        amt_cur = resolve_cost(cid, ledger, why)
        if amt_cur is None:
            return
        amt, cur = amt_cur
        if cid in charged:
            return        # already counted once; this is the shared-intermediate case
        charged[cid] = (amt, cur, why)

    total_outcomes = 0
    per_outcome = {}
    for acc in accs:
        oid = acc["outcome_id"]
        total_outcomes += 1
        # Provenance closure: every step of every unit of every set of this outcome.
        unit_ids = {u["unit_id"] for u in (d.get("units") or [])
                    if sets.get(u.get("set_id"), {}).get("outcome_id") == oid}
        if not unit_ids:
            raise Refusal(f"outcome {oid}: no production units resolve to it")
        o_steps = [s for s in steps if s.get("unit_id") in unit_ids]
        if not o_steps:
            raise Refusal(f"outcome {oid}: no production steps resolve to it")

        before = set(charged)
        for s in o_steps:
            if s.get("attempt_id"):
                a = attempts.get(s["attempt_id"])
                if a is None:
                    raise Refusal(f"step {s.get('step_id')}: attempt {s['attempt_id']} not found")
                # A failed or refused attempt still cost money and is still charged.
                charge(a.get("cost_ref"), f"attempt {a['attempt_id']} (status {a.get('status')})")
            charge(s.get("cost_ref"), f"step {s.get('step_id')} ({s.get('step_kind')})")

        # Evaluator costs on measurements of artifacts belonging to this outcome's steps.
        step_ids = {s.get("step_id") for s in o_steps}
        att_ids = {s.get("attempt_id") for s in o_steps if s.get("attempt_id")}
        o_arts = {aid for aid, r in artifacts.items()
                  if r.get("attempt_id") in att_ids or r.get("step_id") in step_ids}
        for m in (d.get("measurements") or []):
            if m.get("artifact_id") in o_arts:
                charge(m.get("evaluator_cost_ref"), f"measurement {m.get('measurement_id')}")

        # The delivered artifact must actually be part of what we costed.
        da = acc.get("delivered_artifact_id")
        if da and da not in o_arts:
            raise Refusal(f"outcome {oid}: delivered artifact {da} is not in its own provenance; "
                          f"the cost total would not describe what was delivered")
        per_outcome[oid] = sorted(set(charged) - before)

    currencies = {c for (_, c, _) in charged.values()}
    if len(currencies) > 1:
        raise Refusal(f"mixed currencies {sorted(currencies)}: no exchange rate may be invented")

    total = round(sum(a for (a, _, _) in charged.values()), 10)
    return {
        "total_cost": total,
        "accepted_outcomes": total_outcomes,
        "cpao": round(total / total_outcomes, 10),
        "currency": currencies.pop() if currencies else None,
        "distinct_cost_entries_counted": len(charged),
        "charged": charged,
        "per_outcome": per_outcome,
    }


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    expect_refusal = "--expect-refusal" in sys.argv
    if len(args) != 1:
        print("[FAIL] usage: recompute_outcome_cpao.py <fixture.yaml> [--expect-refusal]",
              file=sys.stderr)
        sys.exit(2)
    d = load(args[0])

    try:
        res = compute(d)
    except Refusal as r:
        print(f"[REFUSED] {r}")
        print("No cost total was produced. A refusal is the correct output when the evidence "
              "cannot support a number.")
        sys.exit(3 if expect_refusal else 2)

    if expect_refusal:
        print(f"[FAIL] expected a refusal but a total was computed: {res['total_cost']}")
        sys.exit(1)

    print(f"distinct cost entries counted: {res['distinct_cost_entries_counted']}")
    for cid, (amt, cur, why) in sorted(res["charged"].items()):
        print(f"   {cid:22s} {amt:>8.2f} {cur}   {why}")
    print(f"\ntotal cost:        {res['total_cost']} {res['currency']}")
    print(f"accepted outcomes: {res['accepted_outcomes']}")
    print(f"CpAO:              {res['cpao']} {res['currency']}")

    exp = d.get("expected") or {}
    if not exp:
        print("\n[FAIL] fixture declares no expected values; refusing to call this a pass")
        sys.exit(2)
    bad = []
    for k in ("total_cost", "accepted_outcomes", "cpao", "currency", "distinct_cost_entries_counted"):
        if k in exp and exp[k] != res[k]:
            bad.append(f"{k}: expected {exp[k]!r}, got {res[k]!r}")
    shared = exp.get("shared_intermediate_counted_once")
    if shared:
        arts = index(d.get("artifacts"), "artifact_id")
        att = arts.get(shared, {}).get("attempt_id")
        cref = (index(d.get("attempts"), "attempt_id").get(att) or {}).get("cost_ref")
        consumers = sum(1 for r in (d.get("artifacts") or [])
                        for p in (r.get("parents") or []) if p.get("parent_artifact_id") == shared)
        if cref not in res["charged"]:
            bad.append(f"shared intermediate {shared}: its cost entry was not counted at all")
        else:
            print(f"\n[PASS] shared intermediate {shared} is consumed by {consumers} downstream "
                  f"artifacts and its cost entry {cref} is counted ONCE")
    print()
    if bad:
        for b in bad:
            print(f"[FAIL] {b}")
        sys.exit(1)
    print("[PASS] recomputed total matches the fixture's hand-computed expectation")
    print("[PASS] failed and refused attempts are included in the cost of the accepted outcome")
    print("[PASS] local, evaluator and human costs are included where recorded")
    print("[PASS] no cost entry counted more than once")
    sys.exit(0)


if __name__ == "__main__":
    main()
