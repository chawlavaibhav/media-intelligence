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

# Controller between-role note 6 (2026-09-05): the committed HEAD after the EVAL-039A Auditor fixes carries
# 192 / 96 / 288 calls + 32 conditional and USD 156.46 nominal in cap (cash 115.45 + GCP credits 41.01 + Rs 0.80).
# The task file's older 186 / 112 / 298 and 155.71 are superseded and kept only for the record.
TASK_FIXED = {"tranche_1a": 192, "tranche_1b": 96, "total": 288, "conditional": 32, "nominal_usd_in_cap": "156.46",
              "nominal_usd_cash": "115.45", "nominal_usd_credits": "41.01", "nominal_inr_sarvam": "0.80",
              "source": "COST-TABLE.yaml totals at the committed HEAD (Controller between-role note 6)",
              "superseded_task_file_figures": {"tranche_1a": 186, "tranche_1b": 112, "total": 298, "nominal_usd_in_cap": "155.71"}}
ROUNDING_TOLERANCE_PER_CALL = Decimal("0.0001")    # COST-TABLE rounds line_usd to 4 decimals


def _d2(x: Decimal | None) -> Decimal | None:
    return None if x is None else x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _s(x):
    return None if x is None else str(x)


def build_manifest(book: CB.CaseBook, registry: surfaces.SurfaceRegistry, pricing: PR.Pricing,
                   cost_table: PR.CostTable, seed_policy_path: Path | str = hv2_paths.SEED_POLICY,
                   git_commit: str | None = None) -> dict:
    rows_out = []
    adapters_cache: dict[str, object] = {}
    for row in book.rows():
        entry = registry.get(row["route_key"])
        ad = adapters_cache.get(entry.route_key)
        if ad is None:
            ad = adapter_for(entry, pricing=pricing, seed_policy_path=seed_policy_path)
            adapters_cache[entry.route_key] = ad
        d = ad.dry_run(row)
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
            "billing_pool": entry.billing_pool, "conditional": row["conditional"], "counted_in_cap": counted,
            "would_dispatch": d["would_dispatch"], "refusal_reason": d["refusal_reason"], "request_notes": d["request_notes"] or None,
            "seed_policy": "unset", "key_name": entry.key_name, "credential_file_name": entry.credential_file_name,
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

    def totals(rs):
        agg: dict[tuple, dict] = {}
        for r in rs:
            k = (r["tranche"], r["billing_pool"])
            a = agg.setdefault(k, {"tranche": k[0], "billing_pool": k[1], "calls": 0, "priced_calls": 0, "unpinned_calls": 0,
                                   "usd_nominal": Decimal("0"), "inr_nominal": Decimal("0"), "usd_equiv_nominal": Decimal("0")})
            a["calls"] += 1
            if r["computed_amount"] is None:
                a["unpinned_calls"] += 1
                continue
            a["priced_calls"] += 1
            amt = Decimal(r["computed_amount"])
            if r["currency"] == "INR":
                a["inr_nominal"] += amt
            else:
                a["usd_nominal"] += amt
            a["usd_equiv_nominal"] += Decimal(r["amount_usd_equiv"])
        out = []
        for k in sorted(agg):
            a = agg[k]
            out.append({**a, "usd_nominal": str(_d2(a["usd_nominal"])), "inr_nominal": str(_d2(a["inr_nominal"])),
                        "usd_equiv_nominal": str(_d2(a["usd_equiv_nominal"]))})
        return out

    by_pool = totals(non_cond)
    cond_by_pool = totals(cond)
    in_cap_usd = sum(Decimal(r["amount_usd_equiv"]) for r in non_cond if r["counted_in_cap"] and r["currency"] == "USD")
    in_cap_inr = sum(Decimal(r["computed_amount"]) for r in non_cond if r["counted_in_cap"] and r["currency"] == "INR")
    in_cap_usd_equiv = sum(Decimal(r["amount_usd_equiv"]) for r in non_cond if r["counted_in_cap"])

    # ---- reconciliation against COST-TABLE -------------------------------------------------
    ct_tot = cost_table.totals
    ct_by = {(t["tranche"], t["billing_pool"]): t for t in ct_tot.get("by_tranche_and_pool", [])}
    ct_cond = {(t["tranche"], t["billing_pool"]): t for t in ct_tot.get("conditional_by_pool", [])}
    recon = []
    for t in by_pool:
        c = ct_by.get((t["tranche"], t["billing_pool"]), {})
        delta = Decimal(t["usd_nominal"]) - Decimal(str(c.get("usd_nominal", 0)))
        recon.append({"tranche": t["tranche"], "billing_pool": t["billing_pool"], "manifest_calls": t["calls"], "cost_table_calls": c.get("calls"),
                      "manifest_usd": t["usd_nominal"], "cost_table_usd": _s(c.get("usd_nominal")), "delta_usd": str(_d2(delta)),
                      "within_0_01": abs(delta) <= Decimal("0.01"), "manifest_inr": t["inr_nominal"], "cost_table_inr": _s(c.get("inr_nominal"))})
    recon_cond = []
    for t in cond_by_pool:
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
    pool_of = {(r["case_id"], r["item_id"], r["route_key"], r["arm"]): (r["tranche"], r["billing_pool"], r["conditional"]) for r in rows_out}
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
