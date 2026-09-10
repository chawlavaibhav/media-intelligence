"""`--plan` a route decision for a spec, offline. `--execute` exists only to refuse, today.

    python3 -m runtime.route.cli --plan runtime/route/fixtures/SPEC-static-ad-devanagari.yaml \
        --profile alpha_human_release

    python3 -m runtime.route.cli --cells --profile alpha_human_release
        how many of the 61 evidence cells this router would auto-route under a given profile

`--plan` reads five files and opens no socket: the spec, the policy profile, the taint register, the
routing evidence map and the roster (plus the price pin indexes). There is no provider client in this
package to call even by accident, and a test replaces `socket.socket` with an exploding stub and runs
every fixture plan through it.
"""
from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal
from pathlib import Path

from .attempt_id import load_identities
from .decision import CostEnvelopeExceeded, ExecuteRefused, Router
from .evidence import EvidenceBase, repo_root_from
from .price import PriceBook
from .profile import load_profile
from .spec import load_spec


def build_router(root: Path | None = None) -> tuple[Router, EvidenceBase, Path]:
    ev = EvidenceBase(root=root)
    src = ev.binding.sources
    prices = PriceBook(root=ev.root,
                       roster_path=ev.root / src["roster"],
                       pin_root=ev.root / src["price_pin_root"])
    return Router(ev, prices, load_identities()), ev, ev.root


def _profile(ev: EvidenceBase, name: str):
    return load_profile(name, ev.root / ev.binding.sources["policy_profiles"])


def render(decision: dict) -> str:
    """A plan a person can read, then the decision object itself."""
    out = []
    d = decision
    out.append("=" * 100)
    out.append(f"ROUTE-DECISION  {d['decision_id']}   spec {d['spec_id']}   {d['decided_utc']}")
    out.append(f"profile: {d['provenance']['policy_profile']} "
               f"(status {d['provenance']['policy_profile_status']}, "
               f"adopted {d['provenance']['policy_profile_adopted']})")
    out.append("=" * 100)
    sb = d["selection_basis"]
    out.append(f"required capabilities : {sb['required_capabilities']}")
    out.append(f"selection order       : {sb['rule']}")
    for p in sb.get("preflight") or []:
        out.append(f"  ! {p}")
    out.append("")
    out.append("CANDIDATES (in the order the stages ran)")
    for c in sb["candidates_considered"]:
        mark = "KEPT " if c["kept"] else f"drop@{c['dropped_at']}"
        cost = (c.get("price") or {}).get("expected_cost_usd")
        out.append(f"  [{mark:>22}] {c['route_key']:<24} {('USD ' + cost) if cost else ''}")
        for w in c["why"]:
            out.append(f"        - {w}")
    for row in sb.get("self_composed_requirements") or []:
        out.append("")
        out.append(f"REQUIREMENT SATISFIED BY THE RUNTIME'S OWN CODE: {row['capability']} "
                   f"(level {row['level']}, question {row['question']}) — no provider call")
        for w in row["why"]:
            out.append(f"        - {w}")
        out.append(f"        => cell selected: {row['cell_selected']}")
    if d["exclusions_applied"]:
        out.append("")
        out.append("EXCLUSIONS APPLIED (neither primary nor fallback)")
        for e in d["exclusions_applied"]:
            out.append(f"  - {e['route_key']:<24} {e['reason']}  [{e['basis']}] "
                       f"would have supplied {e['would_have_supplied']}")
    if sb.get("register_notes_applied"):
        out.append("")
        out.append("TAINT-REGISTER NOTES TOUCHING THIS DECISION")
        for n in sb["register_notes_applied"]:
            out.append(f"  - {n['id']} (ruling {n['blocking_ruling']}): {(n['text'] or '')[:220]}…")
    out.append("")
    if d["primary"]:
        p = d["primary"]
        out.append(f"PRIMARY   {p['route_key']}  on {p['surface']}  ({p['evidence_status']})")
        out.append(f"          cells        {p['evidence_cells']}")
        out.append(f"          price        {p['unit_price']} {p['unit']} x {p['quantity']} "
                   f"{p['quantity_unit']}  =  USD {p['expected_cost_usd']}   pool {p['billing_pool']}")
        out.append(f"          pin          {p['price_pin_ref']}")
        out.append(f"          credential   {p['credential_name']} (name only)   adapter {p['adapter_family']}")
        out.append(f"          attempt ids  {p['attempt_ids_if_dispatched']}")
    else:
        out.append("PRIMARY   none — no route survived every stage")
    if d["fallback"]:
        f = d["fallback"]
        out.append(f"FALLBACK  {f['route_key']}  USD {f['expected_cost_usd']}  triggers {f['trigger']}")
    else:
        out.append("FALLBACK  none declared")
    ce = d["cost_envelope"]
    out.append(f"ENVELOPE  committed {ce['already_committed_usd']} + this decision max "
               f"{ce['this_decision_max_usd']} vs ceiling {ce['job_ceiling_usd']}  -> "
               f"{'WITHIN' if ce['within_ceiling'] else 'REFUSE (checked before dispatch)'}")
    if d["unsupported_requirements"]:
        out.append("")
        out.append("UNSUPPORTED REQUIREMENTS")
        for u in d["unsupported_requirements"]:
            out.append(f"  - {u['capability']} (level {u.get('level')}): {u['reason']}"
                       + (f"  blocking: {u.get('blocking')}" if u.get("blocking") else ""))
    out.append("")
    out.append(f"MANUAL ROUTE REQUIRED: {d['manual_route_required']}")
    if d["manual_route_reason"]:
        out.append(f"  {d['manual_route_reason']}")
    out.append("")
    out.append("WHY: " + d["why_selected"])
    return "\n".join(out)


def cells_audit(router: Router, ev: EvidenceBase, profile_name: str) -> str:
    """How many of the map's cells this router would auto-route today, and why not the rest."""
    prof = _profile(ev, profile_name)
    auto = prof.auto_routable_evidence_status
    rows, counters = [], {}
    for key in sorted(ev.cells):
        cell = ev.cells[key]
        g = ev.gate(cell, auto)
        priced = router.prices.quote(cell.route_key, {"params": {"duration_s": 6}})
        ok = g.allowed and priced.priced
        bucket = ("auto_routable" if ok else
                  ("blocked_on_price" if g.allowed else f"blocked_on_evidence:{cell.evidence_status}"))
        counters[bucket] = counters.get(bucket, 0) + 1
        rows.append(f"  {'AUTO' if ok else '----'}  {key:<58} {cell.evidence_status:<26} "
                    f"use={str(cell.production_use_allowed):<11} "
                    f"{'pin ok' if priced.priced else 'no live price'}"
                    f"{('  blocking ' + str(cell.blocking_ruling or cell.blocking_open_question)) if not g.allowed and cell.evidence_status == 'awaiting_controller_ruling' else ''}")
    head = [f"CELL AUDIT under profile {profile_name!r} (auto_routable_evidence_status={auto})",
            f"register vocabulary: {ev.status_vocabulary}",
            f"cells: {len(ev.cells)}"]
    tail = ["", "TOTALS: " + ", ".join(f"{k}={v}" for k, v in sorted(counters.items()))]
    return "\n".join(head + [""] + rows + tail)


def main(argv: list | None = None) -> int:
    ap = argparse.ArgumentParser(prog="runtime.route.cli", description=__doc__)
    ap.add_argument("--plan", metavar="SPEC", help="path to a PRODUCTION-SPEC-v1 yaml")
    ap.add_argument("--execute", metavar="SPEC", help="attempt to execute (refuses without a "
                                                      "request ceiling and an adopted profile)")
    ap.add_argument("--cells", action="store_true", help="audit all evidence cells under a profile")
    ap.add_argument("--profile", required=True, help="the policy profile row the job names")
    ap.add_argument("--already-committed-usd", default="0")
    ap.add_argument("--request-ceiling-usd", default=None)
    ap.add_argument("--customer-ref", default="acct-fixture")
    ap.add_argument("--json", action="store_true", help="print the decision object as JSON")
    args = ap.parse_args(argv)

    router, ev, root = build_router()
    prof = _profile(ev, args.profile)

    if args.cells:
        print(cells_audit(router, ev, args.profile))
        return 0
    if args.plan:
        spec = load_spec(args.plan)
        decision = router.plan(spec, prof, already_committed_usd=Decimal(args.already_committed_usd),
                               customer_ref=args.customer_ref)
        print(json.dumps(decision, indent=2, default=str) if args.json else render(decision))
        return 0
    if args.execute:
        spec = load_spec(args.execute)
        try:
            router.execute(spec, prof,
                           request_cost_ceiling_usd=(Decimal(args.request_ceiling_usd)
                                                     if args.request_ceiling_usd is not None else None),
                           already_committed_usd=Decimal(args.already_committed_usd),
                           customer_ref=args.customer_ref)
        except (ExecuteRefused, CostEnvelopeExceeded) as exc:
            print("EXECUTE REFUSED")
            for r in getattr(exc, "reasons", [str(exc)]):
                print(f"  - {r}")
            return 2
        return 0
    ap.error("one of --plan, --execute or --cells is required")
    return 1


if __name__ == "__main__":
    sys.exit(main())
