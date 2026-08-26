#!/usr/bin/env python3
"""E7-F provisional call/cost forecast for a benchmark-v2 wave.

WHY THIS IS A PROGRAM. The CALL COUNTS follow from the proposed structure and are
computable with certainty. The PRICES could not be obtained: E7-B probed 22
official provider documentation domains and evidenced zero. Rather than guess,
this computes the full structure with every price cell unresolved.

FAILS CLOSED. An unresolved price yields None, never 0, and a partially-resolved
forecast REFUSES to total rather than silently under-reporting a budget.

Usage:
  python3 provisional_forecast.py            # unresolved forecast
  python3 provisional_forecast.py --selftest # arithmetic + fail-closed checks
"""
import argparse, json, sys

# ---- proposed benchmark-v2 shape (PROPOSED, not frozen) --------------------
TIERS = {
    "tier1_atomic":   {"items": 40, "repeats": 2, "note": "unchanged from current bank"},
    "tier2_compound": {"items": 60, "repeats": 2, "note": "unchanged count; prerequisite edges added"},
    "tier3_sweeps":   {"items": 0,  "repeats": 2, "note": "derived below - reuses tier2 items"},
}
# Tier 3 sweeps 4 conditions on a SUBSET of tier-2 items, adaptively.
SWEEP = {
    "conditions_swept": 4,
    "extra_levels_per_condition": 1,   # one ADDITIONAL level beyond the base item
    "tier2_items_swept": 20,           # subset, not all 60
    "adaptive_saving_assumed": 0.0,    # claimed as ZERO; see note
}
LANES = ["image", "general_video", "native_av", "lipsync", "tts"]

# Evaluator fan-out per asset. ESTIMATE, unchanged in status from E2.
EVAL_CALLS_PER_ASSET = {"vlm": 3, "ocr": 3, "asr": 1, "deterministic": 4}
FANOUT_STATUS = "ESTIMATE_NOT_MEASURED"


def counts():
    t1 = TIERS["tier1_atomic"]["items"] * TIERS["tier1_atomic"]["repeats"]
    t2 = TIERS["tier2_compound"]["items"] * TIERS["tier2_compound"]["repeats"]
    sweep_items = SWEEP["tier2_items_swept"] * SWEEP["conditions_swept"] * \
        SWEEP["extra_levels_per_condition"]
    t3 = sweep_items * TIERS["tier3_sweeps"]["repeats"]
    total = t1 + t2 + t3
    return {"tier1_trials": t1, "tier2_trials": t2, "tier3_trials": t3,
            "tier3_extra_items": sweep_items, "total_generations": total}


def evaluator_calls(total_generations):
    return {k: v * total_generations for k, v in EVAL_CALLS_PER_ASSET.items()}


def money(units, price):
    """Fails closed: an unresolved price never becomes 0."""
    return None if price is None else round(units * price, 2)


def build(prices=None):
    prices = prices or {}
    c = counts()
    ev = evaluator_calls(c["total_generations"])
    gen_prices = prices.get("generation", {})
    ev_prices = prices.get("evaluator", {})

    unresolved = []
    gen = {}
    per_lane = c["total_generations"] // len(LANES)
    for lane in LANES:
        p = gen_prices.get(lane)
        gen[lane] = {"generations_if_evenly_split": per_lane,
                     "unit_price": p, "cost": money(per_lane, p)}
        if p is None:
            unresolved.append(f"generation.{lane}")
    evc = {}
    for k, n in ev.items():
        p = ev_prices.get(k)
        evc[k] = {"calls": n, "unit_price": p, "cost": money(n, p)}
        if p is None:
            unresolved.append(f"evaluator.{k}")

    g = [v["cost"] for v in gen.values()]
    e = [v["cost"] for v in evc.values()]
    return {
        "status": "PROVISIONAL_PRE_RUN_FORECAST",
        "authorises_spend": False,
        "structure_source": "BENCHMARK-v2-PROPOSAL.md (PROPOSED, not frozen)",
        "counts": c,
        "evaluator_calls": ev,
        "evaluator_fanout_status": FANOUT_STATUS,
        "generation_cost": gen,
        "evaluator_cost": evc,
        "unresolved_price_cells": sorted(set(unresolved)),
        "totals": {
            "generation": None if any(x is None for x in g) else round(sum(g), 2),
            "evaluator": None if any(x is None for x in e) else round(sum(e), 2),
            "human_verification": prices.get("human_verification_total"),
            "note": ("Human verification is a SEPARATE line and is expected to dominate. "
                     "External corroboration: DreamBench++ reports ~20,000 judge calls and "
                     ">$400 per model evaluated for its MLLM-judge upgrade (INDICATIVE, "
                     "needs re-verification)."),
        },
        "blocked_by": "E7B-BLOCK-01 - zero official provider prices obtainable",
    }


def selftest():
    ok = True
    r = build()
    c = r["counts"]
    exp_t1, exp_t2 = 80, 120
    exp_sweep_items = 20 * 4 * 1
    exp_t3 = exp_sweep_items * 2
    print(f"tier1 {c['tier1_trials']} (expect {exp_t1}): {'OK' if c['tier1_trials']==exp_t1 else 'MISMATCH'}")
    print(f"tier2 {c['tier2_trials']} (expect {exp_t2}): {'OK' if c['tier2_trials']==exp_t2 else 'MISMATCH'}")
    print(f"tier3 {c['tier3_trials']} (expect {exp_t3}): {'OK' if c['tier3_trials']==exp_t3 else 'MISMATCH'}")
    ok &= c["tier1_trials"] == exp_t1 and c["tier2_trials"] == exp_t2 and c["tier3_trials"] == exp_t3
    tot = exp_t1 + exp_t2 + exp_t3
    print(f"total {c['total_generations']} (expect {tot}): {'OK' if c['total_generations']==tot else 'MISMATCH'}")
    ok &= c["total_generations"] == tot

    if r["totals"]["generation"] is not None:
        print("DEFECT: totalled an unresolved forecast"); ok = False
    else:
        print("unresolved prices produce null totals, not 0: OK")

    partial = build({"generation": {"image": 0.10}})
    if partial["totals"]["generation"] is not None:
        print("DEFECT: totalled a PARTIALLY resolved forecast"); ok = False
    else:
        print("partially-resolved forecast refuses to total: OK")

    full = build({"generation": {l: 1.00 for l in LANES},
                  "evaluator": {k: 0.0 for k in EVAL_CALLS_PER_ASSET}})
    per_lane = tot // len(LANES)
    exp_cost = per_lane * 1.00 * len(LANES)
    got = full["totals"]["generation"]
    print(f"fully-resolved total {got} (expect {exp_cost}): {'OK' if abs(got-exp_cost)<0.01 else 'MISMATCH'}")
    ok &= abs(got - exp_cost) < 0.01
    print("\n" + ("SELFTEST PASS" if ok else "SELFTEST FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    print(json.dumps(build(), indent=2))
