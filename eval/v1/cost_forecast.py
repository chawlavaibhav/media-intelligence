#!/usr/bin/env python3
"""E2 cost forecast calculator for the later paid Eval waves.

WHY THIS IS A PROGRAM AND NOT A TABLE
-------------------------------------
The call counts are frozen by the runbook and are pure arithmetic - they can be
computed today with certainty. The PRICES could not be obtained in this cloud
session (see MODEL-WORKFLOW-INVENTORY for the blocker evidence). Rather than
guess prices, this calculator computes the full forecast structure with every
price cell marked unresolved, and produces real totals the moment a prices file
is supplied.

Fails closed: an unresolved price yields `null`, never 0 and never a guess.
A forecast with unresolved cells is reported AS incomplete - it never silently
totals only the cells it happens to know.

Usage:
  python3 eval/v1/cost_forecast.py                 # unresolved forecast
  python3 eval/v1/cost_forecast.py --prices p.yaml # resolved forecast
  python3 eval/v1/cost_forecast.py --selftest      # arithmetic self-check
"""
import argparse, json, sys, pathlib, yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]

# --------------------------------------------------------------------------
# FROZEN BY THE RUNBOOK. These are Controller-set caps, not Eval's choice.
# eval/tasks/EVAL-V1-OVERNIGHT-PROGRAM.md section 4.
# --------------------------------------------------------------------------
LANES = {
    "image":     {"label": "image generation/editing",      "max_endpoints": 4},
    "video":     {"label": "general text/image-to-video",   "max_endpoints": 5},
    "native_av": {"label": "native audio-video",            "max_endpoints": 4},
    "lipsync":   {"label": "lip-sync/digital-human",        "max_endpoints": 3},
    "tts":       {"label": "TTS/external VO",               "max_endpoints": 3},
}

# E7 admission screen: endpoints x items per endpoint.
ADMISSION = {
    "image":     {"items_per_endpoint": 12},
    "video":     {"items_per_endpoint": 12},
    "native_av": {"items_per_endpoint": 12},
    "lipsync":   {"items_per_endpoint": 8},
    "tts":       {"items_per_endpoint": 8},
}
ADMISSION_HARD_MAX = 204

# E8 deep qualification: top <=2 per lane x items x repeats.
DEEP = {
    "image":     {"top_n": 2, "items": 40, "repeats": 2},
    "video":     {"top_n": 2, "items": 30, "repeats": 2},
    "native_av": {"top_n": 2, "items": 36, "repeats": 2},
    "lipsync":   {"top_n": 2, "items": 12, "repeats": 2},
    "tts":       {"top_n": 2, "items": 12, "repeats": 2},
}
DEEP_HARD_MAX = 520

# --------------------------------------------------------------------------
# EVALUATOR FAN-OUT — Eval's own design estimate, NOT a frozen Controller cap.
# This is how many evaluator calls one generated asset triggers under the
# generate-once rule. It is an ESTIMATE and is labelled as one.
# Video is higher because per-sampled-frame OCR is one call per sampled frame.
# --------------------------------------------------------------------------
EVALUATOR_CALLS_PER_ASSET = {
    "image":     {"vlm": 3, "ocr": 1, "deterministic": 3},
    "video":     {"vlm": 3, "ocr": 6, "deterministic": 4},
    "native_av": {"vlm": 3, "ocr": 6, "deterministic": 5},
    "lipsync":   {"vlm": 1, "ocr": 0, "deterministic": 4},
    "tts":       {"vlm": 0, "ocr": 0, "deterministic": 3, "asr": 1},
}
EVALUATOR_ESTIMATE_STATUS = "ESTIMATE_NOT_MEASURED"

UNRESOLVED = None


def counts():
    """Frozen call counts. Pure arithmetic, computable with certainty today."""
    out = {"admission": {}, "deep": {}}
    a_total = d_total = 0
    for lane, cfg in LANES.items():
        n = cfg["max_endpoints"] * ADMISSION[lane]["items_per_endpoint"]
        out["admission"][lane] = {
            "endpoints_max": cfg["max_endpoints"],
            "items_per_endpoint": ADMISSION[lane]["items_per_endpoint"],
            "outputs": n,
        }
        a_total += n
        dd = DEEP[lane]
        m = dd["top_n"] * dd["items"] * dd["repeats"]
        out["deep"][lane] = {**dd, "outputs": m}
        d_total += m
    out["admission_total"] = a_total
    out["deep_total"] = d_total
    return out


def evaluator_counts(c):
    """Evaluator calls implied by the generate-once fan-out."""
    out = {}
    for phase, key in (("admission", "admission"), ("deep", "deep")):
        tot = {}
        for lane, row in c[key].items():
            for instr, per in EVALUATOR_CALLS_PER_ASSET[lane].items():
                tot[instr] = tot.get(instr, 0) + per * row["outputs"]
        out[phase] = tot
    return out


def money(units, price):
    """Fails closed: unresolved price never becomes 0."""
    if price is UNRESOLVED:
        return UNRESOLVED
    return round(units * price, 2)


def build(prices=None):
    prices = prices or {}
    c = counts()
    ev = evaluator_counts(c)

    report = {
        "status": "PRE_RUN_FORECAST",
        "authorises_spend": False,
        "counts": c,
        "evaluator_calls": ev,
        "evaluator_fanout_status": EVALUATOR_ESTIMATE_STATUS,
        "generation_cost": {},
        "evaluator_cost": {},
        "unresolved_price_cells": [],
        "hard_max_checks": {},
    }

    for phase, key in (("admission", "admission"), ("deep", "deep")):
        gen = {}
        for lane, row in c[key].items():
            p = prices.get("generation", {}).get(lane, UNRESOLVED)
            gen[lane] = {
                "outputs": row["outputs"],
                "unit_price": p,
                "cost": money(row["outputs"], p),
            }
            if p is UNRESOLVED:
                report["unresolved_price_cells"].append(f"generation.{lane}")
        report["generation_cost"][phase] = gen

        evc = {}
        for instr, n in ev[phase].items():
            p = prices.get("evaluator", {}).get(instr, UNRESOLVED)
            evc[instr] = {"calls": n, "unit_price": p, "cost": money(n, p)}
            if p is UNRESOLVED:
                report["unresolved_price_cells"].append(f"evaluator.{instr}")
        report["evaluator_cost"][phase] = evc

    report["unresolved_price_cells"] = sorted(set(report["unresolved_price_cells"]))

    # Totals only when EVERY contributing cell is resolved. Never partial.
    for phase in ("admission", "deep"):
        g = [v["cost"] for v in report["generation_cost"][phase].values()]
        e = [v["cost"] for v in report["evaluator_cost"][phase].values()]
        report.setdefault("totals", {})[phase] = {
            "generation": None if any(x is None for x in g) else round(sum(g), 2),
            "evaluator": None if any(x is None for x in e) else round(sum(e), 2),
        }
    report["totals"]["human_verification"] = prices.get("human_verification_total", UNRESOLVED)
    report["totals"]["note"] = (
        "Human verification is a SEPARATE line and is expected to dominate. "
        "The project's original cost model omitted it entirely. Any ratio quoted "
        "before it is measured is an illustrative scenario, not a finding."
    )

    # Guard: our arithmetic must agree with the runbook's stated hard maxima.
    report["hard_max_checks"] = {
        "admission_computed": c["admission_total"],
        "admission_runbook_max": ADMISSION_HARD_MAX,
        "admission_ok": c["admission_total"] == ADMISSION_HARD_MAX,
        "deep_computed": c["deep_total"],
        "deep_runbook_max": DEEP_HARD_MAX,
        "deep_ok": c["deep_total"] == DEEP_HARD_MAX,
    }
    return report


def selftest():
    r = build()
    ok = True
    hm = r["hard_max_checks"]
    print(f"admission computed {hm['admission_computed']} vs runbook {hm['admission_runbook_max']}: "
          f"{'OK' if hm['admission_ok'] else 'MISMATCH'}")
    print(f"deep      computed {hm['deep_computed']} vs runbook {hm['deep_runbook_max']}: "
          f"{'OK' if hm['deep_ok'] else 'MISMATCH'}")
    ok &= hm["admission_ok"] and hm["deep_ok"]

    # Unresolved prices must NEVER produce a total.
    tot = r["totals"]
    if tot["admission"]["generation"] is not None:
        print("DEFECT: produced a generation total from unresolved prices")
        ok = False
    else:
        print("unresolved prices produce null totals, not 0: OK")

    # A partially-resolved price set must STILL refuse to total.
    partial = build({"generation": {"image": 0.04}})
    if partial["totals"]["admission"]["generation"] is not None:
        print("DEFECT: totalled a partially-resolved forecast")
        ok = False
    else:
        print("partially-resolved forecast refuses to total: OK")

    # A fully-resolved set must total correctly.
    full = build({
        "generation": {"image": 0.10, "video": 1.00, "native_av": 2.00,
                       "lipsync": 0.50, "tts": 0.05},
        "evaluator": {"vlm": 0.01, "ocr": 0.001, "deterministic": 0.0, "asr": 0.006},
    })
    expect = 48*0.10 + 60*1.00 + 48*2.00 + 24*0.50 + 24*0.05
    got = full["totals"]["admission"]["generation"]
    print(f"fully-resolved admission generation total {got} vs expected {round(expect,2)}: "
          f"{'OK' if abs(got-expect) < 0.01 else 'MISMATCH'}")
    ok &= abs(got - expect) < 0.01
    print("\n" + ("SELFTEST PASS" if ok else "SELFTEST FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--prices")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    pr = yaml.safe_load(pathlib.Path(a.prices).read_text()) if a.prices else None
    rep = build(pr)
    print(json.dumps(rep, indent=2))
