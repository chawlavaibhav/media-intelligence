#!/usr/bin/env python3
"""Dry run: render the exact request body and price for every Tranche-1 call. Sends nothing.

    python3 eval/harness-v2/dry_run.py --git-rev HEAD --out eval/harness-v2/DRY-RUN-MANIFEST-2026-09.yaml
    python3 eval/harness-v2/dry_run.py --test-cases ... --roster ... --cost-table ... --out ...

One row per (case, route row, repeat_index). The same `adapter.build_request()` that `dispatch()`
would send is used here, so the body bytes are the bytes a live call would carry. The manifest
header counts the rows, totals them by tranche and billing pool, and reconciles them against
COST-TABLE.yaml line by line. It is planning evidence, not a spend authorisation, and says so.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import yaml

import hv2_paths
import casebook as CB
import pricing as PR
import surfaces
from adapters import adapter_for

# Package totals after the 2026-09-09 rebuild (tools/build.py): Controller between-role note 6 (2026-09-05) carried 192 / 96 / 288 calls and
# USD 156.46; since then the package gained, by hand, the VID-TOPO3-01 arm A2 rows (commit 9adc403, +4 calls, +1.09), the ElevenLabs direct
# re-point (commit 0ba06b9: 10 calls moved from fal cash to plan credits, -2.43) and the 8-s ref2v rows (+0.80 credits) - the COST-TABLE was not
# regenerated for those - and now the Wan 2 contender rows (CONTROLLER-WAN2-CONTENDER-PREMIUM-DEFERRED-2026-09-09: wan-2.2-a14b on
# VID-T2V-01/02/03 and VID-2SPK-01, wan-2.2-a14b-i2v on VID-I2V-01..04; 16 calls, USD 8.00). The regenerated COST-TABLE carries all of it:
# 202 / 106 / 308 calls + 32 conditional, USD 163.93 nominal in cap (cash 121.98 + GCP credits 41.94 + Rs 0.80; ElevenLabs plan credits 0 USD).
# The task file's older 186 / 112 / 298 and 155.71 are superseded and kept only for the record.
TASK_FIXED = {"tranche_1a": 202, "tranche_1b": 106, "total": 308, "conditional": 32, "nominal_usd_in_cap": "163.93",
              "nominal_usd_cash": "121.98", "nominal_usd_credits": "41.94", "nominal_inr_sarvam": "0.80",
              "source": "COST-TABLE.yaml totals after the 2026-09-09 rebuild (Wan 2 contender rows + the hand-edited A2 / ElevenLabs-direct / ref2v-8s rows now generated); before them, Controller between-role note 6",
              "superseded_figures": {"between_role_note_6_2026_09_05": {"tranche_1a": 192, "tranche_1b": 96, "total": 288, "nominal_usd_in_cap": "156.46"},
                                     "task_file": {"tranche_1a": 186, "tranche_1b": 112, "total": 298, "nominal_usd_in_cap": "155.71"}}}
ROUNDING_TOLERANCE_PER_CALL = Decimal("0.0001")    # COST-TABLE rounds line_usd to 4 decimals


def _d2(x: Decimal | int | None) -> Decimal | None:
    # `sum()` over zero rows is the int 0 (a subset book with no INR row): coerce, never fail (EVAL-040 runner, additive fix)
    return None if x is None else Decimal(x).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _s(x):
    return None if x is None else str(x)


ROSTER_PRICE_ROUTES = ("flux-2-pro-edit",)      # the one route whose roster price disagrees with the COST-TABLE on multi-reference rows
PRICE_MISMATCH_OPTION = "Controller option: `run_live.py plan --accept-roster-price` dispatches this row at the ROSTER price (the higher one), price_basis roster_over_cost_table; the cap protects the money either way"


def _only_price_mismatch(reason: str | None) -> bool:
    parts = [x.strip() for x in (reason or "").split(";") if x.strip()]
    return bool(parts) and all(x.startswith("price_mismatch") for x in parts)


def price_mismatch_view(pricing: PR.Pricing, route_key: str, row: dict) -> dict:
    """EVAL-041 part 2: what the Controller needs to decide a price-mismatch row - both prices, side by side."""
    pc = pricing.evaluate(route_key, row)
    refs = (row.get("params") or {}).get("refs")
    try:
        refs = int(refs or 0)
    except (TypeError, ValueError):
        refs = 0
    roster = pc.unit_price
    cost_table = row.get("unit_price")
    eligible = (route_key in ROSTER_PRICE_ROUTES and refs >= 2 and _only_price_mismatch(pc.refusal_reason)
                and roster is not None and cost_table is not None and roster > Decimal(str(cost_table)))
    return {"roster_implied_usd": _s(roster), "cost_table_unit_price": _s(cost_table), "refs": refs, "pricing_ok": pc.ok,
            "refusal_reason": pc.refusal_reason, "roster_price_option_eligible": eligible}


def build_manifest(book: CB.CaseBook, registry: surfaces.SurfaceRegistry, pricing: PR.Pricing,
                   cost_table: PR.CostTable, seed_policy_path: Path | str = hv2_paths.SEED_POLICY,
                   git_commit: str | None = None, inputs_for=None, accept_roster_price: bool = False) -> dict:
    """One row per (case, route row, repeat). `inputs_for(row, entry)` (inputs.InputResolver.for_row) resolves the
    sealed inputs a row needs so the body - and its sha256 - are the ones a live dispatch sends; without it every
    input-taking row renders a placeholder and refuses `input_unresolved:<role>`. `accept_roster_price` dispatches a
    multi-reference FLUX edit row at the roster-implied price when that is the ONLY thing refusing it."""
    rows_out = []
    adapters_cache: dict[str, object] = {}
    # A registry entry may already run on a surface / pool the Controller decided but the freeze package has not been rebuilt for
    # (surfaces.GEMINI_API_REPOINT_PENDING_PACKAGE, 2026-09-09). The row keeps BOTH pools; the reconciliation below is against the
    # package's pool (the COST-TABLE basis), and the header lists every such re-point so nothing is hidden.
    pending_repoints = dict(getattr(surfaces, "GEMINI_API_REPOINT_PENDING_PACKAGE", None) or {})
    catalogue = dict(cost_table.route_catalogue or {})
    for row in book.rows():
        entry = registry.get(row["route_key"])
        package_pool = (catalogue.get(entry.route_key) or {}).get("billing_pool") or entry.billing_pool
        ad = adapters_cache.get(entry.route_key)
        if ad is None:
            ad = adapter_for(entry, pricing=pricing, seed_policy_path=seed_policy_path)
            adapters_cache[entry.route_key] = ad
        inputs, resolved, unresolved = inputs_for(row, entry) if inputs_for else ({}, [], [])
        d = ad.dry_run(row, inputs)
        price_basis = "cost_table"
        pm = price_mismatch_view(pricing, entry.route_key, row) if (d["refusal_reason"] and "price_mismatch" in d["refusal_reason"]) else None
        if pm:
            d["refusal_reason"] = (d["refusal_reason"] + f" [cost_table {pm['cost_table_unit_price']} vs roster {pm['roster_implied_usd']}; {PRICE_MISMATCH_OPTION}]")
            if accept_roster_price and pm["roster_price_option_eligible"]:
                priced_row = {**row, "unit_price": Decimal(pm["roster_implied_usd"])}
                d = ad.dry_run(priced_row, inputs)                # the same builder, priced at the roster's number
                price_basis = "roster_over_cost_table"
        price = d["price"]
        computed = Decimal(price["amount_native"]) if price.get("amount_native") is not None else None
        usd = Decimal(price["amount_usd_equiv"]) if price.get("amount_usd_equiv") is not None else None
        counted = (not row["conditional"]) and computed is not None
        rows_out.append({
            "case_id": row["case_id"], "item_id": row["item_id"], "route_key": row["route_key"], "arm": row["arm"],
            "repeat_index": row["repeat_index"], "tranche": row["tranche"], "surface": entry.surface,
            "adapter": entry.adapter, "method": d["method"], "url": d["url"], "headers": d["headers"],
            "body": d["body"], "body_sha256": d["body_sha256"], "api_calls_per_trial": entry.api_calls_per_trial,
            "followups": d["followups"] or None, "shape_status": entry.shape_status,
            "quantity": price.get("quantity"), "quantity_unit": price.get("quantity_unit"), "quantity_rule": price.get("quantity_rule"),
            "unit_price": price.get("unit_price"), "price_status": price.get("price_status"), "route_status": price.get("route_status"),
            "row_unit_price": _s(row.get("unit_price")), "computed_amount": _s(computed), "currency": price.get("currency"),
            "amount_usd_equiv": _s(usd), "fx_rate": price.get("fx_rate"), "price_pin_ref": price.get("pin_ref"),
            "billing_pool": entry.billing_pool, "package_billing_pool": package_pool,
            "pool_repoint_pending_package": bool(entry.route_key in pending_repoints and package_pool != entry.billing_pool),
            "conditional": row["conditional"], "counted_in_cap": counted,
            "would_dispatch": d["would_dispatch"], "refusal_reason": d["refusal_reason"], "request_notes": d["request_notes"] or None,
            "seed_policy": "unset", "key_name": entry.key_name, "credential_file_name": entry.credential_file_name,
            # EVAL-041 part 2: inputs resolved at plan time (summaries, never bytes) and the price basis the row was priced on
            "inputs": resolved or None, "unresolved_inputs": unresolved or None,
            "price_basis": price_basis, "cost_table_unit_price": _s(pm["cost_table_unit_price"]) if pm else _s(row.get("unit_price")),
            "roster_implied_usd": (pm["roster_implied_usd"] if pm else price.get("unit_price")),
        })

    # ---- counts and totals -------------------------------------------------------------------
    non_cond = [r for r in rows_out if not r["conditional"]]
    cond = [r for r in rows_out if r["conditional"]]
    counts = {
        "rows": len(rows_out), "calls_not_conditional": len(non_cond), "calls_conditional": len(cond),
        "tranche_1a": sum(1 for r in non_cond if r["tranche"] == "1a"), "tranche_1b": sum(1 for r in non_cond if r["tranche"] == "1b"),
        "would_dispatch_true": sum(1 for r in rows_out if r["would_dispatch"]),
        "would_dispatch_false": sum(1 for r in rows_out if not r["would_dispatch"]),
        "unpinned_calls": sum(1 for r in non_cond if r["computed_amount"] is None),
        "task_fixed": TASK_FIXED,
        "counts_match_task": (len(non_cond) == TASK_FIXED["total"] and len(cond) == TASK_FIXED["conditional"]),
    }

    def totals(rs, pool_field="billing_pool"):
        agg: dict[tuple, dict] = {}
        for r in rs:
            k = (r["tranche"], r[pool_field])
            a = agg.setdefault(k, {"tranche": k[0], "billing_pool": k[1], "calls": 0, "priced_calls": 0, "unpinned_calls": 0,
                                   "usd_nominal": Decimal("0"), "inr_nominal": Decimal("0"), "usd_equiv_nominal": Decimal("0"),
                                   "plan_credits_nominal": Decimal("0")})
            a["calls"] += 1
            if r["computed_amount"] is None:
                a["unpinned_calls"] += 1
                continue
            a["priced_calls"] += 1
            amt = Decimal(r["computed_amount"])
            if r["billing_pool"] == PR.CREDIT_POOL:
                # ElevenLabs direct (2026-09-09): computed_amount is the vendor's plan credits, 0 USD cash (amount_usd_equiv)
                a["plan_credits_nominal"] += amt
                a["usd_nominal"] += Decimal(r["amount_usd_equiv"])
            elif r["currency"] == "INR":
                a["inr_nominal"] += amt
            else:
                a["usd_nominal"] += amt
            a["usd_equiv_nominal"] += Decimal(r["amount_usd_equiv"])
        out = []
        for k in sorted(agg):
            a = agg[k]
            o = {**a, "usd_nominal": str(_d2(a["usd_nominal"])), "inr_nominal": str(_d2(a["inr_nominal"])),
                 "usd_equiv_nominal": str(_d2(a["usd_equiv_nominal"]))}
            if a["plan_credits_nominal"]:
                o["plan_credits_nominal"] = str(a["plan_credits_nominal"])
            else:
                o.pop("plan_credits_nominal")
            out.append(o)
        return out

    by_pool = totals(non_cond)                                   # by the REGISTRY pool: where the money would actually go
    cond_by_pool = totals(cond)
    recon_by_pool = totals(non_cond, "package_billing_pool")     # by the PACKAGE pool: the COST-TABLE basis the reconciliation is against
    recon_cond_by_pool = totals(cond, "package_billing_pool")
    repoints = {}
    for r in rows_out:
        if r["pool_repoint_pending_package"]:
            k = r["route_key"]
            e = repoints.setdefault(k, {"route_key": k, "registry_pool": r["billing_pool"], "package_pool": r["package_billing_pool"],
                                        "surface": r["surface"], "calls": 0, "usd_nominal": Decimal("0")})
            e["calls"] += 1
            if r["computed_amount"] is not None and r["currency"] == "USD":
                e["usd_nominal"] += Decimal(r["computed_amount"])
    pool_repoints = [{**e, "usd_nominal": str(_d2(e["usd_nominal"]))} for e in repoints.values()]
    in_cap_usd = sum(Decimal(r["amount_usd_equiv"]) for r in non_cond if r["counted_in_cap"] and r["currency"] == "USD")
    in_cap_inr = sum(Decimal(r["computed_amount"]) for r in non_cond if r["counted_in_cap"] and r["currency"] == "INR")
    in_cap_usd_equiv = sum(Decimal(r["amount_usd_equiv"]) for r in non_cond if r["counted_in_cap"])

    # ---- reconciliation against COST-TABLE -------------------------------------------------
    ct_tot = cost_table.totals
    ct_by = {(t["tranche"], t["billing_pool"]): t for t in ct_tot.get("by_tranche_and_pool", [])}
    ct_cond = {(t["tranche"], t["billing_pool"]): t for t in ct_tot.get("conditional_by_pool", [])}
    recon = []
    for t in recon_by_pool:
        c = ct_by.get((t["tranche"], t["billing_pool"]), {})
        delta = Decimal(t["usd_nominal"]) - Decimal(str(c.get("usd_nominal", 0)))
        recon.append({"tranche": t["tranche"], "billing_pool": t["billing_pool"], "manifest_calls": t["calls"], "cost_table_calls": c.get("calls"),
                      "manifest_usd": t["usd_nominal"], "cost_table_usd": _s(c.get("usd_nominal")), "delta_usd": str(_d2(delta)),
                      "within_0_01": abs(delta) <= Decimal("0.01"), "manifest_inr": t["inr_nominal"], "cost_table_inr": _s(c.get("inr_nominal"))})
    recon_cond = []
    for t in recon_cond_by_pool:
        c = ct_cond.get((t["tranche"], t["billing_pool"]), {})
        delta = Decimal(t["usd_nominal"]) - Decimal(str(c.get("usd_nominal", 0)))
        recon_cond.append({"tranche": t["tranche"], "billing_pool": t["billing_pool"], "manifest_calls": t["calls"], "cost_table_calls": c.get("calls"),
                           "manifest_usd": t["usd_nominal"], "cost_table_usd": _s(c.get("usd_nominal")), "delta_usd": str(_d2(delta)),
                           "within_0_01": abs(delta) <= Decimal("0.01")})
    # line-by-line: manifest per-call amount (native currency) vs COST-TABLE row line_usd|line_inr / calls
    ct_rows = {(r["case_id"], r["item_id"], r["route_key"], r["arm"]): r for r in cost_table.rows}
    explained = []
    seen = set()
    for r in rows_out:
        k = (r["case_id"], r["item_id"], r["route_key"], r["arm"])
        if k in seen:
            continue
        c = ct_rows.get(k)
        mine = Decimal(r["computed_amount"]) if r["computed_amount"] is not None else None
        if r["billing_pool"] == PR.CREDIT_POOL and r["amount_usd_equiv"] is not None:
            mine = Decimal(r["amount_usd_equiv"])          # plan credits are not USD; the COST-TABLE line for this pool is 0 USD
        theirs = None
        line_key = "line_inr" if r["currency"] == "INR" else "line_usd"
        if c and c.get(line_key) is not None and c.get("calls"):
            theirs = (Decimal(str(c[line_key])) / Decimal(c["calls"]))
        if mine is None and theirs is None:
            continue
        if mine is not None and theirs is not None and abs(mine - theirs) <= ROUNDING_TOLERANCE_PER_CALL:
            continue
        seen.add(k)
        explained.append({"case_id": r["case_id"], "item_id": r["item_id"], "route_key": r["route_key"], "arm": r["arm"],
                          "calls": c.get("calls") if c else r.get("repeats"), "currency": r["currency"],
                          "manifest_per_call": _s(mine), "cost_table_per_call": _s(theirs),
                          "delta_per_call": _s(None if (mine is None or theirs is None) else mine - theirs),
                          "delta_line_total": _s(None if (mine is None or theirs is None) else (mine - theirs) * Decimal(c.get("calls") if c else r.get("repeats") or 0)),
                          "explanation": r["refusal_reason"] or "; ".join(r["request_notes"] or []) or "see quantity_rule / price_pin_ref"})

    # closure: per pool, the explained line totals must account for the pool delta (mechanical, Tester check 4)
    pool_of = {(r["case_id"], r["item_id"], r["route_key"], r["arm"]): (r["tranche"], r["package_billing_pool"], r["conditional"]) for r in rows_out}
    explained_by_pool: dict[tuple, Decimal] = {}
    for e in explained:
        tp = pool_of[(e["case_id"], e["item_id"], e["route_key"], e["arm"])]
        if e["delta_line_total"] is not None and e["currency"] == "USD" and not tp[2]:
            explained_by_pool[tp[:2]] = explained_by_pool.get(tp[:2], Decimal("0")) + Decimal(e["delta_line_total"])
    for t in recon:
        ex = explained_by_pool.get((t["tranche"], t["billing_pool"]), Decimal("0"))
        residual = Decimal(t["delta_usd"]) - ex
        t["explained_delta_usd"] = str(_d2(ex))
        t["residual_after_explanation_usd"] = str(_d2(residual))
        t["closed"] = bool(t["within_0_01"] or abs(residual) <= Decimal("0.01"))
    nominal_in_cap = str(_d2(in_cap_usd))
    ct_in_cap = Decimal(str(ct_tot.get("nominal_usd_in_cap", 0)))
    header = {
        "manifest": "DRY-RUN-MANIFEST-2026-09",
        "task": "EVAL-039C",
        "status": "PLANNING_EVIDENCE_NOT_A_SPEND_AUTHORISATION",
        "statement": ("Every row is a request body rendered by the same builder a live dispatch would use, priced from the roster at the "
                      "recorded commit. Nothing was sent. This manifest authorises nothing; the Controller's spend record for EVAL-040 "
                      "is the only authority for a paid call, and it must name the roster sha256 below."),
        "generated_utc": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat().replace("+00:00", "Z"),
        "inputs": {
            "test_cases": book.source,
            "roster": {"path": str(pricing.roster.path), "sha256": pricing.roster.sha256,
                       "roster_last_commit_sha": _git_last_commit(hv2_paths.ROSTER),
                       "matches_cost_table_priced_against_roster": pricing.roster.sha256 == (cost_table.priced_against_roster or {}).get("sha256"),
                       "repo_commit_at_generation": git_commit},
            "cost_table": {"path": str(cost_table.path), "sha256": cost_table.sha256, "priced_against_roster": cost_table.priced_against_roster},
            "seed_policy": {"path": str(seed_policy_path), "sha256": hashlib.sha256(Path(seed_policy_path).read_bytes()).hexdigest()},
            "schemas": "eval/harness-v2/schemas/{fal,vertex,sarvam}/SCHEMA-INDEX.yaml",
        },
        "counts": counts,
        "totals_by_tranche_and_pool": by_pool,
        "conditional_by_tranche_and_pool": cond_by_pool,
        "pool_repoints_pending_package": {"routes": pool_repoints,
                                          "note": ("registry entries the Controller re-pointed (surface / pool) before the freeze package was rebuilt for it; "
                                                   "totals_by_tranche_and_pool follow the registry (where the money would go), the reconciliation follows "
                                                   "the package pool (the COST-TABLE basis); empty once the package is rebuilt")},
        "nominal_in_cap": {"usd": nominal_in_cap, "inr": str(_d2(in_cap_inr)), "usd_equiv_all_pools": str(_d2(in_cap_usd_equiv)),
                           "cost_table_nominal_usd_in_cap": str(ct_in_cap), "delta_usd": str(_d2(in_cap_usd - ct_in_cap)),
                           "within_0_01": abs(in_cap_usd - ct_in_cap) <= Decimal("0.01"),
                           "explained_delta_usd": str(_d2(sum(explained_by_pool.values(), Decimal("0")))),
                           "residual_after_explanation_usd": str(_d2(in_cap_usd - ct_in_cap - sum(explained_by_pool.values(), Decimal("0")))),
                           "closed": abs(in_cap_usd - ct_in_cap - sum(explained_by_pool.values(), Decimal("0"))) <= Decimal("0.01"),
                           "all_pools_closed": all(t["closed"] for t in recon)},
        "reconciliation": {"by_tranche_and_pool": recon, "conditional_by_tranche_and_pool": recon_cond,
                           "cost_table_rules_applied": cost_table.rules, "explained_deltas": explained,
                           "note": ("a pool delta above USD 0.01 is explained per (case, route, arm) in explained_deltas (per-call amounts in the row's own "
                                    "currency; a per-call difference within 0.0001 is COST-TABLE's 4-decimal rounding and is not listed); every explained "
                                    "line names the rule or refusal that produced it; the sum of delta_line_total per pool equals that pool's delta_usd")},
        "would_dispatch_rule": "true only when: an adapter exists, shape_status is verified, the row is not conditional, no dispatch precondition is pending, and the roster check pins route, price, quantity and no promo",
        "size_policy": {"SIZE_A": "long side 1024, exact aspect, multiples of 16 (<= 1,048,576 px)", "SIZE_SEEDREAM": "short side 1024 (schema minimum 1024x1024 total pixels; pinned tier <= 1536x1536)",
                        "controller_ref": "MD-C10"},
    }
    return {"header": header, "rows": rows_out}


def _git_last_commit(path: Path) -> str | None:
    try:
        import subprocess
        return subprocess.run(["git", "log", "-1", "--format=%H", "--", str(path)], cwd=hv2_paths.REPO_ROOT,
                              capture_output=True, text=True, check=True).stdout.strip() or None
    except Exception:  # noqa: BLE001
        return None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--git-rev", help="read TEST-CASES / blueprints / COST-TABLE from this git revision (recommended: HEAD)")
    ap.add_argument("--test-cases", default=str(hv2_paths.TEST_CASES))
    ap.add_argument("--roster", default=str(hv2_paths.ROSTER))
    ap.add_argument("--cost-table", default=str(hv2_paths.COST_TABLE))
    ap.add_argument("--seed-policy", default=str(hv2_paths.SEED_POLICY))
    ap.add_argument("--expected-roster-sha256", default=None)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)

    if a.git_rev:
        book = CB.CaseBook.from_git(a.git_rev)
        ct_bytes = CB.git_show(a.git_rev, f"{CB.FREEZE_REL}/COST-TABLE.yaml")
        ct_path = Path(a.out).with_suffix(".cost-table-at-rev.yaml")
        ct_path.write_bytes(ct_bytes)
        roster_bytes = CB.git_show(a.git_rev, "eval/empirical-planning/ROSTER-REFRESH-2026-09.yaml")
        roster_path = Path(a.out).with_suffix(".roster-at-rev.yaml")
        roster_path.write_bytes(roster_bytes)
        cost_table = PR.CostTable(ct_path)
        pricing = PR.Pricing(roster_path, expected_roster_sha256=a.expected_roster_sha256)
        commit = CB.git_sha(a.git_rev)
    else:
        book = CB.CaseBook.from_paths(a.test_cases, Path(a.test_cases).parent)
        cost_table = PR.CostTable(a.cost_table)
        pricing = PR.Pricing(a.roster, expected_roster_sha256=a.expected_roster_sha256)
        commit = None
    manifest = build_manifest(book, surfaces.REGISTRY, pricing, cost_table, a.seed_policy, git_commit=commit)
    if a.git_rev:
        manifest["header"]["inputs"]["cost_table"]["path"] = f"{CB.FREEZE_REL}/COST-TABLE.yaml@{a.git_rev}"
        manifest["header"]["inputs"]["roster"]["path"] = f"eval/empirical-planning/ROSTER-REFRESH-2026-09.yaml@{a.git_rev}"
        ct_path.unlink(missing_ok=True)
        roster_path.unlink(missing_ok=True)
    out = Path(a.out)
    out.write_text("# DRY-RUN MANIFEST - planning evidence, NOT a spend authorisation. Generated by eval/harness-v2/dry_run.py; nothing was sent.\n"
                   + yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True, width=160), encoding="utf-8")
    h = manifest["header"]
    print(json.dumps({"counts": h["counts"], "nominal_in_cap": h["nominal_in_cap"], "reconciliation": h["reconciliation"]["by_tranche_and_pool"],
                      "explained_deltas": len(h["reconciliation"]["explained_deltas"])}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
