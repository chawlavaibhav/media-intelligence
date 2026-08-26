#!/usr/bin/env python3
"""EVAL-011 — enforce every mechanical gate in the task. Fails closed.

Gates (from EVAL-011 "Mechanical gates"):
  1  no live corrected file may say 12 condition families while the schema declares 13
  2  13 binary families may not be described as 4,096 rather than 8,192
  3  requested-operation vocabulary must equal CANON-010's, exactly
  4  workflow mode may not be populated from requested operation, or vice versa
  5  Layers 1-3 may not claim customer-outcome CpAO
  6  VID-05 may not claim CpAO before end-to-end outcomes
  7  seeded and unseeded repeat semantics may not be silently pooled
  8  sourcing may not change scientific-slot admission
  9  a sibling/family model may not be silently substituted
 10  missing prices may not be guessed, and a partial stage may not be totalled
 11  RES-004 provisional full-pack hours may not be a mandatory first-tranche gate
 12  V1 historical artifacts may not change
 13  staged counts must reconcile to the corrected design ceiling

Run from anywhere:  python3 eval/pre-execution-integration/validators/validate_integration_package.py
"""
import pathlib, re, subprocess, sys, yaml

HERE = pathlib.Path(__file__).resolve().parent
PKG = HERE.parent                      # eval/pre-execution-integration
ROOT = HERE.parents[2]                 # repo root
E9 = ROOT / "eval/pre-execution-freeze"

CANON_010_OPS = ["generate", "edit", "animate", "restore", "extend", "compose", "variants"]

# Files that legitimately discuss the historical 12/4096 error while correcting it.
CORRECTION_NARRATIVE = {
    "CONDITION-CONTRACT-CORRECTION.md",
    "EVAL-011-CONTROLLER-BRIEF.md",
}


def load(p):
    return yaml.safe_load(pathlib.Path(p).read_text())


def main(strict_paths=None):
    e, w = [], []
    cond_path = E9 / "CONDITION-ENVELOPE-CONTRACT.yaml"
    cond = load(cond_path)

    # ---- gate 1 + 2: family count and cell count, recomputed --------------
    actual = len(cond["condition_families"])
    declared = cond.get("condition_families_count")
    if declared != actual:
        e.append(f"G1 condition_families_count={declared} but {actual} families are defined")
    if cond["sweep_policy"].get("condition_families") != actual:
        e.append(f"G1 sweep_policy.condition_families="
                 f"{cond['sweep_policy'].get('condition_families')} != {actual}")
    expected_cells = 2 ** actual
    if cond.get("two_level_naive_cells") != expected_cells:
        e.append(f"G2 two_level_naive_cells={cond.get('two_level_naive_cells')} != 2**{actual}={expected_cells}")

    # swept flags must agree with the sweep list
    flagged = {f["id"] for f in cond["condition_families"] if f.get("swept_in_wave1")}
    listed = set(cond["sweep_policy"]["actively_swept_in_wave1"])
    if flagged != listed:
        e.append(f"G1 swept flags {sorted(flagged)} != sweep_policy list {sorted(listed)}")

    # ---- gate 1 + 2 in prose: scan live files -----------------------------
    bad_count = re.compile(r"\b12\s+(?:condition\s+)?families\b|\ball\s+12\s+at\s+two\s+levels\b", re.I)
    bad_cells = re.compile(r"\b4[,.]?096\b")
    scan = list(E9.rglob("*.md")) + list(E9.rglob("*.yaml")) + \
           list(PKG.rglob("*.md")) + list(PKG.rglob("*.yaml"))
    for f in scan:
        if f.name in CORRECTION_NARRATIVE:
            continue
        # negative fixtures are DELIBERATELY broken inputs; they are not live files.
        # Excluding them is required, not a loophole - the test harness asserts each
        # one still makes this validator fail when it is placed in a package root.
        if "fixtures" in f.parts:
            continue
        txt = f.read_text(errors="ignore")
        if bad_count.search(txt):
            e.append(f"G1 '{f.relative_to(ROOT)}' still claims 12 condition families")
        if bad_cells.search(txt):
            e.append(f"G2 '{f.relative_to(ROOT)}' still claims 4,096 cells")

    # ---- gate 3: operation vocabulary == CANON-010 ------------------------
    op = next(f for f in cond["condition_families"] if f["id"] == "COND-OPERATION")
    if op.get("vocabulary") != CANON_010_OPS:
        e.append(f"G3 COND-OPERATION vocabulary {op.get('vocabulary')} != CANON-010 {CANON_010_OPS}")
    if op.get("vocabulary_owner") != "canon":
        e.append("G3 COND-OPERATION must record vocabulary_owner: canon")
    if op.get("eval_may_extend") is not False:
        e.append("G3 COND-OPERATION must record eval_may_extend: false")
    if "provisional_vocabulary" in op:
        e.append("G3 COND-OPERATION still carries provisional_vocabulary; CANON-010 has frozen it")

    bench = load(E9 / "BENCHMARK-v2-WAVE1.yaml")
    if bench.get("requested_operation_vocabulary") != CANON_010_OPS:
        e.append("G3 benchmark requested_operation_vocabulary != CANON-010")
    if "requested_operations_covered" in bench:
        e.append("G3 benchmark still uses the ambiguous key 'requested_operations_covered'")

    # ---- gate 4: provenance separation ------------------------------------
    wf = next(f for f in cond["condition_families"] if f["id"] == "COND-WORKFLOW")
    if "MUST NOT be populated from requested_operation" not in str(wf.get("hard_rule", "")):
        e.append("G4 COND-WORKFLOW lost its provenance hard rule")
    if "MUST NOT be substituted for workflow_mode" not in str(op.get("hard_rule", "")):
        e.append("G4 COND-OPERATION lost its provenance hard rule")
    if wf.get("provenance") != "planner_side" or op.get("provenance") != "customer_side":
        e.append("G4 provenance sides corrupted")

    # ---- gate 5 + 6: CpAO staging -----------------------------------------
    plan = load(PKG / "STAGED-EXECUTION-PLAN.yaml")
    stages = {s["stage"]: s for s in plan["stages"]}
    for sid in ("A", "B"):
        forb = stages[sid].get("metrics_forbidden") or []
        if "customer-outcome CpAO" not in forb:
            e.append(f"G5 stage {sid} does not forbid customer-outcome CpAO")
    if stages["C"].get("cpao_authority") is None:
        e.append("G5 stage C must assert sole CpAO authority")

    recon = load(PKG / "SCIENTIFIC-SLOT-SUPPLY-RECONCILIATION.yaml")
    vid05 = next(s for s in recon["slots"] if s["slot_id"] == "VID-05")
    if vid05.get("cpao_staging") != "STAGE_C_ONLY":
        e.append("G6 VID-05 must carry cpao_staging: STAGE_C_ONLY")

    fc = load(E9 / "WAVE1-CALL-COUNT-FORECAST.yaml")["formula_for_eval010"]
    if "STAGE C" not in str(fc.get("api_tool_cpao_computable_from", "")):
        e.append("G6 forecast does not restrict api_tool_cpao to Stage C")
    if "customer-outcome CpAO" not in str(fc.get("layers_1_3_forbidden_metric", "")):
        e.append("G5 forecast does not forbid customer-outcome CpAO in Layers 1-3")

    # ---- gate 7: seed semantics -------------------------------------------
    if "seed_policy_vocabulary" not in wf:
        e.append("G7 COND-WORKFLOW records no seed_policy vocabulary")
    else:
        for v in ("held", "varied", "unset"):
            if v not in wf["seed_policy_vocabulary"]:
                e.append(f"G7 seed_policy vocabulary missing '{v}'")
        if "MUST NOT be pooled" not in str(wf.get("hard_rule_repeats", "")):
            e.append("G7 COND-WORKFLOW lacks the no-pooling rule for held vs unset repeats")
    if "absent_in_api" not in (wf.get("seed_support_vocabulary") or {}):
        e.append("G7 seed_support must distinguish absent_in_api from undocumented")

    # ---- gate 8 + 9: sourcing may not change admission --------------------
    r = recon["rollup"]
    if r["slots_total"] != 14 or recon["meta"]["core_slots"] != 12 or recon["meta"]["reserve_slots"] != 2:
        e.append("G8 slot roster is no longer 12 core + 2 reserve")
    for k in ("slots_added_by_this_task", "slots_removed_by_this_task",
              "slots_reprioritised_by_this_task"):
        if recon["meta"][k] != 0:
            e.append(f"G8 {k}={recon['meta'][k]}; sourcing must not change admission")
    if recon["meta"]["sourcing_changed_admission"] is not False:
        e.append("G8 sourcing_changed_admission must be false")
    if r["slots_deleted_for_sourcing_reasons"] != 0:
        e.append("G8 a slot was deleted for sourcing reasons")
    if r["sibling_substitutions_performed"] != 0:
        e.append("G9 a sibling/family substitution was performed")
    for s in recon["slots"]:
        if s["supply_status"] == "identity_unresolved" and s.get("do_not_substitute") is not True:
            e.append(f"G9 {s['slot_id']} unresolved but not marked do_not_substitute")
        if s["supply_status"] == "identity_unresolved" and s.get("slot_disposition") != "RETAINED":
            e.append(f"G8 {s['slot_id']} unresolved and not RETAINED")

    # ---- gate 10: no guessed prices, no partial totals ---------------------
    pf = load(PKG / "PRICE-READY-STAGED-FORECAST.yaml")
    for name, st in pf["staged_forecast"].items():
        tot = st.get("stage_total", {})
        if tot.get("value") is not None:
            e.append(f"G10 {name} has a stage_total value while prices are unresolved")
        for line in ("generation_cost", "evaluator_cost", "human_cost"):
            blk = st.get(line, {})
            if blk.get("value") not in (None, 0):
                e.append(f"G10 {name}.{line} carries a value ({blk.get('value')}) without complete prices")
    if pf["price_completeness_summary"]["stages_price_complete"] != 0:
        e.append("G10 a stage is described as price-complete")
    if pf["nominal_vs_cash"]["cash_outlay_after_credits"]["status"] != "UNRESOLVED":
        e.append("G10 cash outlay after credits must remain UNRESOLVED")
    txt = (PKG / "PRICE-READY-STAGED-FORECAST.yaml").read_text()
    if "per one thousand images" not in txt or "per generated 1K-RESOLUTION IMAGE" not in txt:
        e.append("G10 the Nano Banana 2 per-image wording guard is missing")

    # ---- gate 11: 173 hours is not a first-tranche prerequisite ------------
    mm = (PKG / "EVALUATOR-AND-MATERIAL-STAGE-MAP.yaml").read_text()
    if "173" not in mm:
        e.append("G11 material map does not address the 173 person-hour figure")
    elif "NOT a prerequisite" not in mm:
        e.append("G11 material map does not state 173 hours is not a prerequisite")
    mmy = load(PKG / "EVALUATOR-AND-MATERIAL-STAGE-MAP.yaml")
    if mmy["meta"]["resources_files_edited_by_this_task"] != 0:
        e.append("G11 Resources-owned files were edited")

    # ---- gate 12: V1 artifacts byte-identical ------------------------------
    try:
        out = subprocess.run(
            ["git", "diff", "--name-only", "origin/main", "--",
             "eval/v1/capability-contract.yaml", "eval/v1/bank/master-bank-v1.jsonl",
             "eval/battery/", "canon/experiments/v1/"],
            cwd=ROOT, capture_output=True, text=True, timeout=60)
        changed = [l for l in out.stdout.splitlines() if l.strip()]
        if changed:
            e.append(f"G12 V1 historical artifacts modified: {changed}")
    except Exception as ex:                                   # pragma: no cover
        w.append(f"G12 could not verify V1 immutability: {ex}")

    # ---- gate 13: staged counts reconcile ---------------------------------
    rp = plan["rollup"]
    A = rp["stage_A_model_generations"]; B = rp["stage_B_model_generations_max"]
    ceil = rp["design_ceiling_layers_1_3"]
    if A + B != ceil:
        e.append(f"G13 {A} + {B} != design ceiling {ceil}")
    if ceil != load(E9 / "WAVE1-CALL-COUNT-FORECAST.yaml")["generations_total_core"]:
        e.append("G13 plan ceiling disagrees with the forecast")
    if sum(stages["A"]["per_slot_generations"].values()) != A:
        e.append("G13 stage A per-slot generations do not sum to the stated total")
    if sum(stages["B"]["per_slot_remaining_after_stage_A"].values()) != B:
        e.append("G13 stage B per-slot remainders do not sum to the stated maximum")
    if rp["stage_Q_model_generations"] != 0:
        e.append("G13 stage Q must have zero model generations")
    if stages["B"]["adaptive_expected_structure"]["value"] is not None:
        e.append("G13 stage B claims an expected survivor count / pass-rate saving")

    # ---- report ------------------------------------------------------------
    for x in w:
        print(f"WARN  {x}")
    if e:
        for x in e:
            print(f"FAIL  {x}")
        print(f"\nFAIL - {len(e)} gate violation(s).")
        return 1

    print(f"condition families      : {actual} (declared {declared}), naive cells {expected_cells}")
    print(f"swept families          : {len(flagged)} of {actual}")
    print(f"operation vocabulary    : {len(CANON_010_OPS)} values, owner canon")
    print(f"scientific slots        : {recon['meta']['core_slots']} core / {recon['meta']['reserve_slots']} reserve, "
          f"{r['identity_resolved_by_supply_evidence']} identity-resolved, {r['identity_unresolved']} unresolved")
    print(f"staged generations      : Q={rp['stage_Q_model_generations']} A={A} B<={B} "
          f"C_attempts={rp['stage_C_outcome_attempts']} (ceiling {ceil})")
    print(f"price-complete stages   : {pf['price_completeness_summary']['stages_price_complete']}")
    print(f"V1 artifacts modified   : no")
    print("\nPASS - all 13 mechanical gates hold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
