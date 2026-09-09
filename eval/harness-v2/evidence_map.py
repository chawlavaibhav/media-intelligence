#!/usr/bin/env python3
"""evidence_map: ROUTING-EVIDENCE-MAP-v0.yaml - the TIERED product asset for every (question, route, arm) cell of EVAL-040.

    python3 eval/harness-v2/evidence_map.py --registry eval/registry/registry-v1.jsonl \\
        --results eval/experiments/EVAL-040/runs/img-r1/RESULTS.yaml \\
        --results eval/experiments/EVAL-040/runs/half2/RESULTS.yaml \\
        --results eval/experiments/EVAL-040/runs/topo3-video/RESULTS.yaml \\
        --composite-results eval/experiments/EVAL-040/runs/img-r1-composite/RESULTS.yaml \\
        --out eval/capability-map/ROUTING-EVIDENCE-MAP-v0.yaml

`--results` repeats: the runs' trials and elimination lists are concatenated and every trial remembers the run it came
from. A cell is (question, route_key, arm); the arms None / "core" / "edit" name the cell by the route alone, the
composite plate (prompt_basis blueprint_textless_plate) is route + "+code_overlay", every other arm is route + "+" + arm.

Four tiers per cell, never mixed:
    deterministic            facts read back from the Registry rows (registry: true): refusal / error rate, format
                             compliance, settled trial cost, latency, unseeded repeat variance
    human_blind_acceptance   the Controller's blind accept / reject counts from RESULTS.yaml (registry: false -
                             product evidence, never a Registry row), with n and the Controller's own notes
    screened_not_qualified   VLM screening - none yet (registry: false)
    historical_prior         a pointer into eval/historical-priors/media-factory-v1/ where a row exists for the same
                             route family (registry: false, freshness_required: true)
plus `fallback` (the next-best route by acceptance within the question, ties by settled trial cost), `price_pin_ref`,
`evidence_date`, and the routing rules the Controller has already drawn. The map stores evidence and the Controller's
rules; it computes no score and no weight (SCHEMA-v1 no_routing_scores).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import yaml

import hv2_paths
from instruments import metrics as MX

MAP_PATH = hv2_paths.EVAL_ROOT / "capability-map" / "ROUTING-EVIDENCE-MAP-v0.yaml"
PRIOR_DIR = "eval/historical-priors/media-factory-v1"
PRIOR_FILE = f"{PRIOR_DIR}/MEDIA-FACTORY-ROUTING-PRIOR.md"
SUMMARY_REF = "eval/experiments/EVAL-040/runs/img-r1/IMAGE-ROUND-1-SUMMARY.md"
SUMMARY_HALF2 = "eval/experiments/EVAL-040/runs/half2/IMAGE-HALF-TWO-SUMMARY.md"
SUMMARY_VIDEO1 = "eval/experiments/EVAL-040/runs/topo3-video/VIDEO-PIECE-1-SUMMARY.md"
COMPOSITE_SUFFIX = "+code_overlay"
TRIVIAL_ARMS = (None, "core", "edit")      # arms that do not distinguish a cell: the route name stands alone
ROUND = "EVAL-040 Image Round 1 + image half two + video piece 1 (img-r1, img-r1-redo, img-r1-composite, half2, topo3-video, topo3-nb-video)"

TIERS = {
    "deterministic": {"registry": True, "meaning": "re-evaluated by a frozen deterministic instrument over sealed bytes; the Registry rows named are the evidence"},
    "human_blind_acceptance": {"registry": False, "meaning": "the Controller's blind accept / reject against the case's acceptance contract; product evidence, never a Registry row"},
    "screened_not_qualified": {"registry": False, "meaning": "VLM failure-mode screening by an unqualified instrument; never a Registry input"},
    "historical_prior": {"registry": False, "meaning": "Media Factory's July-August 2026 observations on earlier model versions; needs a fresh dated check before reuse"},
}

# route family -> rows of MEDIA-FACTORY-ROUTING-PRIOR.md that speak about the same family (pointers, never claims)
HISTORICAL_PRIORS = {
    "flux-2-pro": [{"row": "Production one-shot ads (V2 era)", "said": "FLUX.2 avoided for Indian-product world knowledge: 'FLUX invented wrong products'",
                    "confidence_then": "Low-Medium (Tier C; no scored corpus survives)", "freshness_risk": "High"}],
    "gpt-image-2": [{"row": "Production one-shot ads (V2 era)", "said": "GPT Image 2 hero ($0.04) + deterministic composite; 'payable' (live-verified)",
                     "confidence_then": "Low-Medium (Tier C; no scored corpus survives)", "freshness_risk": "High"}],
    "nano-banana-pro": [{"row": "Stills where exact in-scene text/craft matters", "said": "Nano Banana Pro edit ($0.15) preferred; its fails were identity, not text",
                         "confidence_then": "Medium-High (Tier A, n=16 text scenes)", "freshness_risk": "High"}],
    "seedream-5-pro": [{"row": "On-brand character stills at volume", "said": "Seedream 4.5 edit: 90.6% pass, $0.044/accepted (an earlier version)",
                        "confidence_then": "High (Tier A, n=64)", "freshness_risk": "High - seedream version superseded"},
                       {"row": "Stills where exact in-scene text/craft matters", "said": "Seedream avoided for text-critical stills: rendered hex codes / dropped wordmarks",
                        "confidence_then": "Medium-High (Tier A)", "freshness_risk": "High"}],
    "flux-2-pro" + COMPOSITE_SUFFIX: [{"row": "Guaranteed-exact text/logo (contracts, prices, Devanagari)",
                                       "said": "textless base + deterministic composite overlay is exact by construction",
                                       "confidence_then": "Medium (Tier B)", "freshness_risk": "Medium"}],
}

ROUTING_RULES = [
    {"id": "RR-1", "scope": "text on stills", "rule": "Code-set text on a cheap textless plate is the DEFAULT where exactness is contractual (prices, legal lines, brand names) or where a re-render must be free.",
     "evidence": "img-r1-composite: 4/4 accepted, exact by construction, ~USD 0.03 per accepted picture (plates USD 0.12 + overlay USD 0)",
     "tier": "human_blind_acceptance", "registry": False, "caveat": "could not be blind as to arm", "source": SUMMARY_REF + " (addendum 2026-09-09)"},
    {"id": "RR-2", "scope": "in-scene text on stills", "rule": "Generated text where the type must sit inside the scene (on a pack, a sign, a surface): Nano Banana 2 or GPT Image 2.",
     "evidence": "img-r1 IMG-TEXT: nano-banana-2 4/4 and gpt-image-2 4/4 (Devanagari 2/2, English 2/2 each) at USD 0.053-0.067 a picture; nano-banana-pro 4/4 at 3x the price",
     "tier": "human_blind_acceptance", "registry": False, "source": SUMMARY_REF},
    {"id": "RR-3", "scope": "Devanagari text on stills", "rule": "Avoid Seedream 5 Pro, Recraft V4 and FLUX.2 Pro for Devanagari text.",
     "evidence": "img-r1 IMG-TEXT-01 (Hindi): seedream-5-pro 0/2, recraft-v4 0/2, flux-2-pro 0/2 - every rejection 'wrong spelling'; qwen-image-3 1/2",
     "tier": "human_blind_acceptance", "registry": False, "source": SUMMARY_REF},
    {"id": "RR-4", "scope": "edit / extend / compose / reference on a supplied photo",
     "rule": "Seedream 5 Pro edit is the DEFAULT for work on a supplied photo (remove an object, extend a banner, compose a supplied face and pack, reproduce a referenced product or person).",
     "evidence": "half2: seedream-5-pro-edit 10/12 (IMG-EDIT 2/4, IMG-EXT 2/2, IMG-COMP 2/2, IMG-REF 4/4) at USD 0.0675 a call; flux-2-pro-edit 4/12; nano-banana-pro-edit 3/12 at USD 0.15 a call",
     "tier": "human_blind_acceptance", "registry": False,
     "caveat": "n = 2 per (case, route); two Controller rejects on IMG-REF-02 ('clothes changed') read the contract more strictly than it is written", "source": SUMMARY_HALF2},
    {"id": "RR-5", "scope": "extend a banner (outpaint to 9:16)",
     "rule": "Only Seedream 5 Pro edit extended the banner without resizing or cutting it; avoid FLUX.2 Pro edit and Nano Banana Pro edit for extension.",
     "evidence": "half2 IMG-EXT-01: seedream-5-pro-edit 2/2; flux-2-pro-edit 0/2 'changed size'; nano-banana-pro-edit 0/2 'slight cutoff, not consistent'",
     "tier": "human_blind_acceptance", "registry": False, "source": SUMMARY_HALF2},
    {"id": "RR-6", "scope": "exact Devanagari text in motion (video)",
     "rule": "Never ask the premium video model to write the text. Set the type by code on an animated textless plate (cheap image-to-video), or carry a CORRECT still into a cheap animator.",
     "evidence": "topo3-video VID-TOPO3-01: arm C (FLUX.2 Pro textless plate -> MiniMax H3 Max i2v -> exact strings by code on every frame) 2/2; arm B native text on veo-3.1-full 0/2 and kling-v3-pro 0/2 ('different text altogether'); arm A (qwen-image-3 plate -> H3 Max / Wan 3.0 Prime i2v) 0/4, every reject the plate's own misspelling carried faithfully - the animators preserved the lettering",
     "tier": "human_blind_acceptance", "registry": False, "caveat": "video packet was blind as to route and arm but had no off-repo reveal key", "source": SUMMARY_VIDEO1},
    {"id": "RR-7", "scope": "the still that feeds a cheap animator",
     "rule": "A text plate that goes into image-to-video must come from a text-capable still route (RR-2: Nano Banana 2 or GPT Image 2), never from the cheapest still model.",
     "evidence": "topo3-video arm A: both qwen-image-3 9:16 plates misspelled Hindi (0/4 in motion); topo3-nb-video arm A2: nano-banana-2 plate (draw 2 accepted, draw 1 'two shri') -> H3 Max 2/2 - the same animator passes once the plate is right",
     "tier": "human_blind_acceptance", "registry": False, "status": "tested_in_motion_2026-09-09", "source": SUMMARY_VIDEO1},
]


def _sha256_file(p: Path | str) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load_registry(path: Path | str) -> list:
    out = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.lstrip().startswith("#"):
            out.append(json.loads(line))
    return out


def _rate(num, den):
    return (num / den) if den else None


ANY_ARM = object()      # default: do not filter by arm at all


def _arm_matches(row: dict, arm) -> bool:
    """ANY_ARM: no filter. A trivial arm (None / core / edit) matches any trivial arm on the row; a named arm must match exactly."""
    if arm is ANY_ARM:
        return True
    if arm in TRIVIAL_ARMS:
        return row.get("arm") in TRIVIAL_ARMS
    return row.get("arm") == arm


def merge_results(results_list: list) -> dict:
    """Concatenate several RESULTS.yaml documents. Every trial and elimination entry remembers its run (`results_run_id`);
    `revealed_utc` is the latest reveal; `commitment_verified_by_run` keeps each run's own flag."""
    docs = [r for r in results_list if r]
    trials, elim = [], []
    for r in docs:
        rid = r.get("run_id")
        trials += [{**t, "results_run_id": rid} for t in r.get("trials", [])]
        elim += [{**e, "results_run_id": rid} for e in r.get("elimination", [])]
    revealed = [str(r["revealed_utc"]) for r in docs if r.get("revealed_utc")]
    rules = [r.get("rules_ref") for r in docs if r.get("rules_ref")]
    return {"run_ids": [r.get("run_id") for r in docs], "revealed_utc": max(revealed) if revealed else None,
            "commitment_verified_by_run": {r.get("run_id"): bool(r.get("commitment_verified")) for r in docs},
            "rules_ref": rules[0] if len(set(rules)) == 1 else (sorted(set(rules)) or None), "trials": trials, "elimination": elim}


def deterministic_facts(records: list, question: str, route_key: str, prompt_basis: str | None = None, arm=ANY_ARM) -> dict:
    rows = [r for r in records if r.get("question") == question and r.get("route_key") == route_key and r.get("evidence_tier") == "deterministic"
            and (prompt_basis is None or r.get("prompt_basis") == prompt_basis) and _arm_matches(r, arm)]
    if not rows:
        return {"tier": "deterministic", "registry": False, "status": "no_rows", "rows": []}
    by_cap: dict = defaultdict(list)
    for r in rows:
        by_cap[r["capability"]].append(r)
    fmt = by_cap.get("delivery_format_compliance", [])
    lat = by_cap.get("latency_errors_refusals", [])
    cost = by_cap.get("cost_and_cpao", [])
    rep = by_cap.get("reproducibility", [])
    status = Counter()
    for r in lat:
        status.update((r.get("reliability") or {}).get("status_counts") or {})
    n_counted = sum(status.values())
    lats = [v for r in lat for v in ((r.get("latency_s") or {}).get("by_trial") or {}).values() if v is not None]
    cost_rows = cost or lat            # every row carries the cell's settled total; the cost rows are the canonical carrier
    settled = [Decimal(r["cost"]["settled_total_usd_equiv_all_counted_trials"]) for r in cost_rows if (r.get("cost") or {}).get("settled_total_usd_equiv_all_counted_trials")]
    n_settled = sum(int((r.get("cost") or {}).get("n_settled") or 0) for r in cost_rows)
    pairs = [p for r in rep for p in ((r.get("repeat_variance") or {}).get("pairs") or [])]
    ham = [p["dhash_hamming_max"] for p in pairs if p.get("dhash_hamming_max") is not None]
    ssim = [p["ssim_min"] for p in pairs if p.get("ssim_min") is not None]
    refusals = status.get("refusal", 0)
    errors = status.get("error", 0) + status.get("timeout", 0)
    return {
        "tier": "deterministic", "registry": True, "rows": sorted(r["entry_id"] for r in rows),
        "n_items": sorted({i for r in rows for i in r.get("bank_item_ids", [])}),
        "counted_trials": n_counted, "status_counts": dict(status),
        "refusal_rate": _rate(refusals, n_counted), "error_rate": _rate(errors, n_counted),
        "format_compliance": {"passes": sum(r["passes"] for r in fmt), "trials": sum(r["trials"] for r in fmt), "n_items": sum(r["n_items"] for r in fmt),
                              "items_excluded": [x for r in fmt for x in r.get("items_excluded", [])]},
        "trial_cost_usd": {"settled_total": str(sum(settled, Decimal("0")).quantize(Decimal("0.000001"))) if settled else None,
                           "per_trial_mean": str((sum(settled, Decimal("0")) / n_settled).quantize(Decimal("0.000001"))) if settled and n_settled else None,
                           "n_settled": n_settled, "cost_within_reserved": {"passes": sum(r["passes"] for r in cost), "trials": sum(r["trials"] for r in cost)}},
        "latency_s": {"p50": MX.percentile_nearest_rank(lats, 0.5) if lats else None, "p95": MX.percentile_nearest_rank(lats, 0.95) if lats else None, "n": len(lats)},
        "repeat_variance_unseeded": {"pairs": len(pairs), "dhash_hamming_mean": (sum(ham) / len(ham)) if ham else None, "dhash_hamming_max": max(ham) if ham else None,
                                     "ssim_mean": (sum(ssim) / len(ssim)) if ssim else None, "ssim_min": min(ssim) if ssim else None,
                                     "structural_passes": sum(r["passes"] for r in rep), "structural_trials": sum(r["trials"] for r in rep)},
        "uncertainty": "Clopper-Pearson 95 % over base items on every row; independence NOT ESTABLISHED; reference calculation only",
    }


def human_facts(results: dict, question: str, route_key: str, arm=ANY_ARM) -> dict:
    """`results` is one RESULTS.yaml document or the output of merge_results. An elimination entry that carries an `arm` key
    (the video runs do) must match the cell's arm; entries without one (the image runs) match on question and route."""
    trials = [t for t in results.get("trials", []) if t.get("question") == question and t.get("route_key") == route_key and _arm_matches(t, arm)]
    if not trials:
        return {"tier": "human_blind_acceptance", "registry": False, "status": "no_verdicts"}
    accepts = sum(1 for t in trials if t.get("verdict") == "accept")
    elim = next((e for e in results.get("elimination", []) if e.get("question") == question and e.get("route_key") == route_key
                 and ("arm" not in e or _arm_matches(e, arm))), None)
    runs = sorted({t.get("results_run_id") or results.get("run_id") for t in trials if t.get("results_run_id") or results.get("run_id")})
    by_run = results.get("commitment_verified_by_run") or {results.get("run_id"): bool(results.get("commitment_verified"))}
    verified = bool(runs) and all(by_run.get(r, False) for r in runs)
    return {
        "tier": "human_blind_acceptance", "registry": False, "judge": "Controller (blind, commitment verified)" if verified else "Controller",
        "accepts": accepts, "trials": len(trials), "rejects": sum(1 for t in trials if t.get("verdict") == "reject"),
        "n_items": len({t.get("case_id") for t in trials}), "arms": sorted({t.get("arm") for t in trials if t.get("arm")}),
        "no_artifact_rejects": sum(1 for t in trials if str(t.get("verdict_basis", "")).startswith("no_artifact")),
        "per_item": {c: {"accepts": sum(1 for t in trials if t.get("case_id") == c and t.get("verdict") == "accept"),
                         "trials": sum(1 for t in trials if t.get("case_id") == c)} for c in sorted({t.get("case_id") for t in trials})},
        "controller_notes": [{"trial_id": t["trial_id"], "verdict": t.get("verdict"), "note": t["note"]} for t in trials if t.get("note")],
        "elimination": elim, "rules_ref": results.get("rules_ref"), "runs": runs,
        "source": f"RESULTS.yaml of run{'s' if len(runs) > 1 else ''} {', '.join(runs) if runs else results.get('run_id')}",
        "note": "acceptance is a per-artifact accept/reject against the case contract; never pooled with any deterministic number",
    }


def composite_human_facts(comp: dict) -> dict:
    per_case = comp.get("per_case") or {}
    accepts = sum(int(v.get("accepted", 0)) for v in per_case.values())
    trials = sum(int(v.get("trials", 0)) for v in per_case.values())
    return {"tier": "human_blind_acceptance", "registry": False, "judge": "Controller", "blind_as_to_arm": bool(comp.get("blind_as_to_arm", False)),
            "accepts": accepts, "trials": trials, "rejects": trials - accepts, "n_items": len(per_case), "arms": [str(comp.get("arm"))],
            "per_item": {c: {"accepts": int(v.get("accepted", 0)), "trials": int(v.get("trials", 0))} for c, v in sorted(per_case.items())},
            "controller_notes": [{"trial_id": t.get("trial_id"), "verdict": t.get("verdict"), "note": t.get("note")} for t in comp.get("trials", []) if t.get("note")],
            "cost": comp.get("cost"), "note": comp.get("note"), "source": f"RESULTS.yaml of run {comp.get('run_id')}"}


def _price_pins(records: list, question: str, route_key: str, arm=ANY_ARM) -> dict:
    rows = [r for r in records if r.get("question") == question and r.get("route_key") == route_key and _arm_matches(r, arm)]
    pins = sorted({p for r in rows for p in ((r.get("cost") or {}).get("price_source") or [])})
    prices = sorted({p for r in rows for p in ((r.get("cost") or {}).get("unit_price_pinned") or [])})
    pools = sorted({p for r in rows for p in ((r.get("cost") or {}).get("billing_pool") or [])})
    return {"price_pin_ref": pins, "unit_price_usd_pinned": prices, "billing_pool": pools, "surface": sorted({r.get("surface") for r in rows if r.get("surface")})}


def _evidence_date(records: list, results: dict, question: str, route_key: str, arm=ANY_ARM) -> str | None:
    dates = [str(r.get("tested_date"))[:10] for r in records if r.get("question") == question and r.get("route_key") == route_key and r.get("tested_date")
             and _arm_matches(r, arm)]
    if not dates and results.get("revealed_utc"):
        dates = [str(results["revealed_utc"])[:10]]
    return max(dates) if dates else None


def assign_fallbacks(cells: dict) -> None:
    """Within a question: rank by acceptance rate (desc), then settled cost per trial (asc); fallback = the next route down; the last falls back to the first."""
    def key(c):
        h = c["human_blind_acceptance"]
        acc = _rate(h.get("accepts", 0), h.get("trials", 0)) if h.get("trials") else -1.0
        cost = (c["deterministic"].get("trial_cost_usd") or {}).get("per_trial_mean") if c["deterministic"].get("registry") else None
        return (-(acc if acc is not None else -1.0), Decimal(cost) if cost else Decimal("999"))
    ranked = sorted(cells.items(), key=lambda kv: key(kv[1]))
    for i, (name, c) in enumerate(ranked):
        c["rank_in_question"] = i + 1
        nxt = ranked[i + 1][0] if i + 1 < len(ranked) else (ranked[0][0] if len(ranked) > 1 and ranked[0][0] != name else None)
        c["fallback"] = {"route": nxt, "basis": "next-best route by human acceptance within the question, ties by settled cost per trial; the last-ranked falls back to the first",
                         "registry": False}


def cell_name(route_key: str, arm: str | None, prompt_basis: str | None = None) -> str:
    """The composite plate is route+code_overlay; a trivial arm (None / core / edit) is the bare route; any other arm is route+arm."""
    if prompt_basis == "blueprint_textless_plate":
        return route_key + COMPOSITE_SUFFIX
    return route_key if arm in TRIVIAL_ARMS else f"{route_key}+{arm}"


def build_map(records: list, results: dict | list, composite_results: dict | None = None, registry_path: str | None = None,
              results_paths: list | None = None, criteria_sha256: str | None = None) -> dict:
    """`results` is one RESULTS.yaml document or a list of them (merged by merge_results)."""
    results = merge_results(results if isinstance(results, list) else [results])
    questions: dict = defaultdict(dict)
    def key_arm(a):            # the trivial arms are one cell: keyed as None, named by the route alone
        return None if a in TRIVIAL_ARMS else a
    keys = {(r["question"], r["route_key"], key_arm(r.get("arm")), r.get("prompt_basis")) for r in records if r.get("evidence_tier") == "deterministic"}
    for t in results.get("trials", []):
        keys.add((t.get("question"), t.get("route_key"), key_arm(t.get("arm")), "blueprint_main"))
    for question, route, arm, basis in sorted(keys, key=lambda k: tuple(str(x) for x in k)):
        name = cell_name(route, arm, basis)
        if basis == "blueprint_textless_plate":
            det = deterministic_facts(records, question, route, basis)
            hum = composite_human_facts(composite_results) if composite_results else {"tier": "human_blind_acceptance", "registry": False, "status": "no_verdicts"}
            arm_note = "textless plate (FLUX.2 Pro) + exact strings set by code (composite-v2 layout); deterministic facts describe the PLATE calls"
        else:
            det = deterministic_facts(records, question, route, basis if basis in ("blueprint_main",) else None, arm)
            hum = human_facts(results, question, route, arm)
            arm_note = None
        prior_rows = HISTORICAL_PRIORS.get(name) or HISTORICAL_PRIORS.get(route)
        arms_seen = sorted({str(r.get("arm")) for r in records if r.get("question") == question and r.get("route_key") == route and _arm_matches(r, arm) and r.get("arm")}
                           | {str(t.get("arm")) for t in results.get("trials", []) if t.get("question") == question and t.get("route_key") == route and _arm_matches(t, arm) and t.get("arm")})
        cell = {
            "route_key": route, "arm": arm if arm is not None else (arms_seen[0] if len(arms_seen) == 1 else None), "arm_note": arm_note, **_price_pins(records, question, route, arm),
            "evidence_date": _evidence_date(records, results, question, route, arm) or (str(composite_results.get("judged_utc"))[:10] if composite_results else None),
            "deterministic": det, "human_blind_acceptance": hum,
            "screened_not_qualified": {"tier": "screened_not_qualified", "registry": False, "status": "none_yet"},
            "historical_prior": {"tier": "historical_prior", "registry": False, "pointer": PRIOR_FILE, "freshness_required": True,
                                 "rows": prior_rows or [], "status": "row_exists" if prior_rows else "no_row_for_this_route_family"},
        }
        questions[question][name] = cell
    for q, cells in questions.items():
        assign_fallbacks(cells)
    n_cells = sum(len(c) for c in questions.values())
    return {
        "schema": "ROUTING-EVIDENCE-MAP-v0", "status": "product_asset; tiers never mixed; human tiers are never Registry rows",
        "generated_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "round": ROUND,
        "sources": {"registry": registry_path, "registry_sha256": (_sha256_file(registry_path) if registry_path and Path(registry_path).exists() else None),
                    "results": results_paths or [], "results_run_ids": results.get("run_ids"), "criteria_sha256": criteria_sha256,
                    "summary": SUMMARY_REF, "summaries": [SUMMARY_REF, SUMMARY_HALF2, SUMMARY_VIDEO1], "historical_prior_index": f"{PRIOR_DIR}/PRIOR-INDEX.yaml"},
        "tiers": TIERS, "routing_rules": ROUTING_RULES, "cell_count": n_cells,
        "reading_guide": ["deterministic numbers come from Registry rows re-evaluated under the frozen PASS-CRITERIA-v0.yaml; every row's interval is a reference calculation (independence NOT ESTABLISHED)",
                          "human acceptance is the Controller's blind verdict against the acceptance contract; n is small (2-8 trials over 1-4 items); never a Registry row",
                          "fallback is a ranking by acceptance within the question, not a score; the Production Planner decides routing"],
        "questions": {q: {"cells": cells} for q, cells in questions.items()},
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--registry", default=str(hv2_paths.EVAL_ROOT / "registry" / "registry-v1.jsonl"))
    ap.add_argument("--results", action="append", required=True, help="RESULTS.yaml of a blind-judged run (repeat for several runs)")
    ap.add_argument("--composite-results", default=None)
    ap.add_argument("--criteria-sha256", default=None)
    ap.add_argument("--out", default=str(MAP_PATH))
    a = ap.parse_args(argv)
    records = load_registry(a.registry)
    results = [yaml.safe_load(Path(p).read_text(encoding="utf-8")) for p in a.results]
    comp = yaml.safe_load(Path(a.composite_results).read_text(encoding="utf-8")) if a.composite_results else None
    m = build_map(records, results, comp, registry_path=a.registry, results_paths=list(a.results) + ([a.composite_results] if a.composite_results else []),
                  criteria_sha256=a.criteria_sha256)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    header = ("# ROUTING-EVIDENCE-MAP-v0 - generated by eval/harness-v2/evidence_map.py from the Registry rows and the Controller's verdicts.\n"
              "# Tiered product asset: deterministic (registry: true) | human_blind_acceptance | screened_not_qualified | historical_prior (all registry: false).\n"
              "# No score, no weight, no ranking beyond the stated fallback rule. Regenerate rather than edit.\n")
    out.write_text(header + yaml.safe_dump(m, allow_unicode=True, sort_keys=False, width=140), encoding="utf-8")
    print(f"wrote {out} ({m['cell_count']} cells)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
