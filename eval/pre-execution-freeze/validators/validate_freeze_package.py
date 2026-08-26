#!/usr/bin/env python3
"""EVAL-009 — enforce every mechanical gate in the task. Fails closed.

Gates (from EVAL-009 "Mechanical gates"):
  1  V1 capabilities may not disappear without explicit mapping
  2  a required descendant may not pass or be ignored after prerequisite failure
  3  requested_operation may not be substituted for workflow_mode
  4  PRP may not contain provider/model/routing fields
  5  benchmark may not perform a cartesian sweep
  6  an unqualified evaluator may not be described as qualified
  7  scientific roster may not use access/credits as admission rationale
  8  a price may not be guessed
  9  a partially unresolved forecast may not be totalled as an exact budget
 10  historical V1 artifacts may not be silently modified
"""
import hashlib, json, pathlib, re, subprocess, sys, yaml

HERE = pathlib.Path(__file__).resolve().parent
PKG = HERE.parent
ROOT = HERE.parents[2]

ACCESS_WORDS = ["credit", "credits", "frontier cloud", "fal availability", "account access",
                "we have access", "already available to us", "on our account"]
QUALIFIED_ASSERTIONS = ["is now qualified", "has been qualified", "is hereby qualified",
                        "instrument qualified:", "qualified: true"]


def load(name):
    p = PKG / name
    return yaml.safe_load(p.read_text()) if p.exists() else None


def main():
    e, w = [], []

    # ---- gate 1: every V1 id mapped ---------------------------------------
    v1 = yaml.safe_load((ROOT / "eval/v1/capability-contract.yaml").read_text())
    v1_ids = {d["id"] for d in v1["dimensions"]}
    v2 = load("CAPABILITY-CONTRACT-v2.yaml")
    if not v2:
        e.append("CAPABILITY-CONTRACT-v2.yaml missing")
    else:
        mapped = {m["v1_id"] for m in v2["v1_to_v2_mapping"]}
        missing = sorted(v1_ids - mapped)
        if missing:
            e.append(f"GATE1: {len(missing)} V1 id(s) with no disposition: {missing[:5]}")
        if len(v2["v1_to_v2_mapping"]) != len(v1_ids):
            e.append(f"GATE1: mapping has {len(v2['v1_to_v2_mapping'])} rows for {len(v1_ids)} V1 ids")
        for d in v2["dimensions"]:
            if d.get("v2_disposition") != "added" and not d.get("v1_origin"):
                e.append(f"GATE1: v2 capability {d['id']} has no v1_origin and is not 'added'")
        for d in v2["dimensions"]:
            if d.get("v2_disposition") == "added" and not d.get("admission_justification"):
                e.append(f"GATE1: added capability {d['id']} has no admission justification")

    # ---- gate 2: blocked descendants stay unsatisfied ----------------------
    dep = load("DEPENDENCY-SCORING-CONTRACT.yaml")
    if not dep:
        e.append("DEPENDENCY-SCORING-CONTRACT.yaml missing")
    else:
        st = {s["id"]: s for s in dep["measurement_states"]}
        if "blocked_by_prerequisite_failure" not in st:
            e.append("GATE2: no blocked_by_prerequisite_failure state defined")
        else:
            b = st["blocked_by_prerequisite_failure"]
            if b["outcome_acceptance"] != "unsatisfied":
                e.append(f"GATE2: blocked state resolves to '{b['outcome_acceptance']}' at outcome "
                         f"level; it MUST be 'unsatisfied'")
            if b.get("countable_in_pass_rate"):
                e.append("GATE2: blocked state is counted in the diagnostic pass-rate denominator")
        rules = " ".join(dep["prerequisite_graph"]["rules"]).lower()
        if "may never be `pass`" not in rules and "may never be pass" not in rules:
            e.append("GATE2: graph rules do not forbid a descendant passing under a failed ancestor")
        forb = " ".join(dep["aggregation"]["forbidden"]).lower()
        if "not_applicable" not in forb:
            e.append("GATE2: aggregation does not forbid treating blocked as not_applicable")

    # ---- gate 3: operation != workflow mode --------------------------------
    cond = load("CONDITION-ENVELOPE-CONTRACT.yaml")
    if not cond:
        e.append("CONDITION-ENVELOPE-CONTRACT.yaml missing")
    else:
        ids = {c["id"]: c for c in cond["condition_families"]}
        if "COND-OPERATION" not in ids or "COND-WORKFLOW" not in ids:
            e.append("GATE3: requested_operation and workflow_mode are not both condition families")
        else:
            if ids["COND-OPERATION"].get("provenance") != "customer_side":
                e.append("GATE3: requested_operation is not marked customer_side")
            if ids["COND-WORKFLOW"].get("provenance") != "planner_side":
                e.append("GATE3: workflow_mode is not marked planner_side")
            if "MUST NOT" not in str(ids["COND-WORKFLOW"].get("hard_rule", "")):
                e.append("GATE3: no hard rule preventing workflow_mode being filled from operation")
        if cond.get("single_complexity_score") != "FORBIDDEN":
            e.append("GATE3/5: single complexity score is not forbidden")

    # ---- gate 4: PRP is provider-agnostic ---------------------------------
    prp = load("PRODUCTION-REQUIREMENT-PROFILE-v1.yaml")
    if not prp:
        e.append("PRODUCTION-REQUIREMENT-PROFILE-v1.yaml missing")
    else:
        if prp.get("contains_provider_or_routing_decisions") is not False:
            e.append("GATE4: PRP does not declare itself provider/routing free")
        forbidden = set(prp.get("forbidden_keys", []))
        for need in ("provider", "model", "endpoint", "price", "route"):
            if need not in forbidden:
                e.append(f"GATE4: '{need}' is not in the PRP forbidden-key list")
        # scan the worked example for forbidden keys
        def scan(node, path=""):
            if isinstance(node, dict):
                for k, v in node.items():
                    if k in forbidden and k != "workflow_mode":
                        e.append(f"GATE4: PRP example contains forbidden key '{k}' at {path}")
                    scan(v, path + "/" + str(k))
            elif isinstance(node, list):
                for i, v in enumerate(node):
                    scan(v, f"{path}[{i}]")
        scan(prp.get("example", {}), "example")

    # ---- gate 5: no cartesian sweep ---------------------------------------
    bench = load("BENCHMARK-v2-WAVE1.yaml")
    if not bench:
        e.append("BENCHMARK-v2-WAVE1.yaml missing")
    else:
        if bench.get("cartesian_sweep") is not False:
            e.append("GATE5: benchmark does not declare cartesian_sweep false")
        l3 = bench["layers"]["layer3_sweeps"]
        if l3.get("cartesian") is not False:
            e.append("GATE5: layer 3 does not declare cartesian false")
        swept = len(l3["swept"])
        total_fams = len(cond["condition_families"]) if cond else 0
        if total_fams and swept >= total_fams:
            e.append(f"GATE5: {swept}/{total_fams} condition families swept - that is a full sweep")
        if not l3.get("stop_rule") or not l3.get("expansion_rule"):
            e.append("GATE5: sparse sweeps lack stop/expansion rules")

    # ---- gate 6: nothing described as qualified ---------------------------
    evm = load("EVALUATOR-QUALIFICATION-MAP.yaml")
    if not evm:
        e.append("EVALUATOR-QUALIFICATION-MAP.yaml missing")
    else:
        if evm.get("instruments_qualified") != 0:
            e.append("GATE6: evaluator map claims qualified instruments")
        for c in evm["capabilities"]:
            if c.get("qualified") is not False:
                e.append(f"GATE6: {c['capability']} is marked qualified")
    for f in PKG.glob("*.md"):
        for sent in re.split(r"(?<=[.!?])\s+", f.read_text()):
            s = sent.lower()
            for a in QUALIFIED_ASSERTIONS:
                if a in s and not any(n in s for n in ("no ", "not ", "never", "must be", "none")):
                    e.append(f"GATE6: {f.name} asserts qualification: '{sent.strip()[:80]}'")

    # ---- gate 7: roster admission is science, not access -------------------
    ros = load("SCIENTIFIC-WAVE1-MODEL-ROSTER.yaml")
    if not ros:
        e.append("SCIENTIFIC-WAVE1-MODEL-ROSTER.yaml missing")
    else:
        if ros.get("admission_used_access_or_credits") is not False:
            e.append("GATE7: roster does not declare admission independent of access")
        for s in ros["slots"]:
            blob = " ".join(str(s.get(k, "")) for k in
                            ("question", "why_it_changes_production", "admission_basis",
                             "tier_rationale")).lower()
            for wd in ACCESS_WORDS:
                if wd in blob:
                    e.append(f"GATE7: slot {s['slot_id']} rationale references access/credits ('{wd}')")
            if not s.get("question") or not s.get("why_it_changes_production"):
                e.append(f"GATE7: slot {s['slot_id']} lacks a question or production consequence")
            if not s.get("nearest_redundant"):
                e.append(f"GATE7: slot {s['slot_id']} does not name a nearest redundant candidate")
            if not s.get("workflow_mode"):
                e.append(f"GATE7: slot {s['slot_id']} does not state a workflow mode")
            if s.get("tier") not in ("core", "reserve"):
                e.append(f"GATE7: slot {s['slot_id']} has no core/reserve tier")

    # ---- gates 8 + 9: no guessed price, no partial total -------------------
    fc = load("WAVE1-CALL-COUNT-FORECAST.yaml")
    if not fc:
        e.append("WAVE1-CALL-COUNT-FORECAST.yaml missing")
    else:
        pr = fc["prices"]
        for k, v in (pr.get("generation_unit_price_by_slot") or {}).items():
            if v is not None:
                e.append(f"GATE8: a generation price is populated for {k} - no official price exists")
        for k, v in (pr.get("evaluator_unit_price_by_instrument") or {}).items():
            if v is not None:
                e.append(f"GATE8: an evaluator price is populated for {k}")
        if pr.get("human_rate") is not None:
            e.append("GATE8: a human rate is populated; none is approved")
        unresolved = any(v is None for v in
                         (pr.get("generation_unit_price_by_slot") or {}).values())
        for k, v in fc["totals"].items():
            if k == "why_null":
                continue
            if unresolved and v is not None:
                e.append(f"GATE9: total '{k}' is populated while prices are unresolved")
        if fc.get("authorises_spend") is not False:
            e.append("GATE9: forecast does not declare that it authorises no spend")

    # ---- gate 10: V1 artifacts untouched ----------------------------------
    dirty = subprocess.run(["git", "status", "--porcelain", "eval/v1/"],
                           capture_output=True, text=True, cwd=ROOT).stdout.strip()
    if dirty:
        e.append(f"GATE10: V1 artifacts modified:\n{dirty}")
    bank = ROOT / "eval/v1/bank/master-bank-v1.jsonl"
    if bank.exists():
        n = len([l for l in bank.read_text().splitlines() if l.strip()])
        if n != 100:
            e.append(f"GATE10: V1 bank has {n} items, expected 100")

    # ---- report ------------------------------------------------------------
    if v2:
        c = v2["counts"]
        print(f"capability v1->v2        : {c['v1_capabilities']} -> {c['v2_capabilities_total']} "
              f"({c['v2_active']} active, {c['v2_dormant']} dormant)")
    if ros:
        print(f"roster slots             : {ros['summary']['core_slots']} core / "
              f"{ros['summary']['reserve_slots']} reserve")
    if bench:
        print(f"benchmark base items     : {bench['totals']['base_items']}")
    if fc:
        print(f"generations / evaluator  : {fc['generations_total_core']} / "
              f"{fc['evaluator_calls_total']:.0f}")
    if evm:
        print(f"instruments qualified    : {evm['instruments_qualified']}")
    print(f"V1 artifacts modified    : {'YES' if dirty else 'no'}")
    for x in w:
        print("WARN ", x)
    if e:
        print(f"\nFAIL - {len(e)} gate violation(s):")
        for x in e:
            print("  -", x)
        return 1
    print("\nPASS - all 10 mechanical gates hold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
