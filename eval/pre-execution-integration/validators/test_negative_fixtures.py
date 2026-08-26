#!/usr/bin/env python3
"""EVAL-011 — negative fixtures.

A validator that has only ever seen correct input is not evidence. Each fixture
below breaks exactly ONE gate in a temporary copy of the repository package and
asserts the validator FAILS on it. A fixture that does not trigger a failure is
itself a failure: it means the gate is decorative.

This is the lesson the project already paid for - negative-control fixtures
immediately exposed three real defects in the V1 harness, none of which was
visible from reading the code.

Run:  python3 eval/pre-execution-integration/validators/test_negative_fixtures.py
"""
import copy, pathlib, shutil, subprocess, sys, tempfile, yaml

HERE = pathlib.Path(__file__).resolve().parent
PKG = HERE.parent
ROOT = HERE.parents[2]

E9_REL = "eval/pre-execution-freeze"
PKG_REL = "eval/pre-execution-integration"


def _write(p, obj):
    p.write_text(yaml.safe_dump(obj, sort_keys=False, allow_unicode=True))


# --------------------------------------------------------------------------
# each mutator receives the temp repo root and breaks exactly one gate
# --------------------------------------------------------------------------

def nc_family_count_12(root):
    """G1 — declare 12 families while 13 are defined."""
    p = root / E9_REL / "CONDITION-ENVELOPE-CONTRACT.yaml"
    d = yaml.safe_load(p.read_text()); d["condition_families_count"] = 12; _write(p, d)


def nc_cells_4096(root):
    """G2 — restore the 2**12 cell count."""
    p = root / E9_REL / "CONDITION-ENVELOPE-CONTRACT.yaml"
    d = yaml.safe_load(p.read_text()); d["two_level_naive_cells"] = 4096; _write(p, d)


def nc_drop_a_family(root):
    """G1 — remove a family to 'recover' the old count, the exact forbidden fix."""
    p = root / E9_REL / "CONDITION-ENVELOPE-CONTRACT.yaml"
    d = yaml.safe_load(p.read_text())
    d["condition_families"] = [f for f in d["condition_families"] if f["id"] != "COND-SCALE"]
    _write(p, d)


def nc_operation_vocab_drift(root):
    """G3 — Eval invents an operation value CANON-010 does not have."""
    p = root / E9_REL / "CONDITION-ENVELOPE-CONTRACT.yaml"
    d = yaml.safe_load(p.read_text())
    for f in d["condition_families"]:
        if f["id"] == "COND-OPERATION":
            f["vocabulary"] = f["vocabulary"] + ["upscale"]
    _write(p, d)


def nc_provenance_collapse(root):
    """G4 — drop the rule that keeps customer intent and workflow mode apart."""
    p = root / E9_REL / "CONDITION-ENVELOPE-CONTRACT.yaml"
    d = yaml.safe_load(p.read_text())
    for f in d["condition_families"]:
        if f["id"] == "COND-WORKFLOW":
            f["hard_rule"] = "populate from requested_operation when convenient"
    _write(p, d)


def nc_layer13_claims_cpao(root):
    """G5 — Stage A stops forbidding customer-outcome CpAO."""
    p = root / PKG_REL / "STAGED-EXECUTION-PLAN.yaml"
    d = yaml.safe_load(p.read_text())
    for s in d["stages"]:
        if s["stage"] == "A":
            s["metrics_forbidden"] = []
    _write(p, d)


def nc_vid05_early_cpao(root):
    """G6 — VID-05 claims its cost-knee CpAO conclusion before Stage C."""
    p = root / PKG_REL / "SCIENTIFIC-SLOT-SUPPLY-RECONCILIATION.yaml"
    d = yaml.safe_load(p.read_text())
    for s in d["slots"]:
        if s["slot_id"] == "VID-05":
            s["cpao_staging"] = "STAGE_A"
    _write(p, d)


def nc_seed_pooling(root):
    """G7 — remove the rule separating held-seed from unseeded repeats."""
    p = root / E9_REL / "CONDITION-ENVELOPE-CONTRACT.yaml"
    d = yaml.safe_load(p.read_text())
    for f in d["condition_families"]:
        if f["id"] == "COND-WORKFLOW":
            f["hard_rule_repeats"] = "held and unset repeats may be averaged together"
    _write(p, d)


def nc_sourcing_deletes_a_slot(root):
    """G8 — drop the unresolved slot because sourcing is hard."""
    p = root / PKG_REL / "SCIENTIFIC-SLOT-SUPPLY-RECONCILIATION.yaml"
    d = yaml.safe_load(p.read_text())
    d["slots"] = [s for s in d["slots"] if s["slot_id"] != "AUD-03"]
    d["rollup"]["slots_total"] = 13
    _write(p, d)


def nc_silent_sibling_substitution(root):
    """G9 — quietly promote a family sibling into an unresolved slot."""
    p = root / PKG_REL / "SCIENTIFIC-SLOT-SUPPLY-RECONCILIATION.yaml"
    d = yaml.safe_load(p.read_text())
    for s in d["slots"]:
        if s["slot_id"] == "IMG-04":
            s["do_not_substitute"] = False
            s["verified_identity"] = {"fal_endpoint": "fal-ai/bytedance/seedream/v5/lite/text-to-image"}
    _write(p, d)


def nc_partial_stage_totalled(root):
    """G10 — total a stage while eleven of twelve slots have no price."""
    p = root / PKG_REL / "PRICE-READY-STAGED-FORECAST.yaml"
    d = yaml.safe_load(p.read_text())
    d["staged_forecast"]["stage_A"]["stage_total"] = {"value": 4.5, "currency": "USD", "status": "COMPLETE"}
    _write(p, d)


def nc_cash_outlay_guessed(root):
    """G10 — infer Frontier Clouds and resolve cash outlay."""
    p = root / PKG_REL / "PRICE-READY-STAGED-FORECAST.yaml"
    d = yaml.safe_load(p.read_text())
    d["nominal_vs_cash"]["cash_outlay_after_credits"]["status"] = "RESOLVED_ASSUMED_GCP"
    _write(p, d)


def nc_173_hours_mandatory(root):
    """G11 — turn the full acquisition estimate into a first-run prerequisite."""
    p = root / PKG_REL / "EVALUATOR-AND-MATERIAL-STAGE-MAP.yaml"
    t = p.read_text().replace("is NOT a prerequisite", "is a mandatory prerequisite")
    p.write_text(t)


def nc_stage_counts_do_not_reconcile(root):
    """G13 — staged counts stop summing to the design ceiling."""
    p = root / PKG_REL / "STAGED-EXECUTION-PLAN.yaml"
    d = yaml.safe_load(p.read_text())
    d["rollup"]["stage_A_model_generations"] = 45
    _write(p, d)


def nc_stage_q_spends_generations(root):
    """G13 — Stage Q starts burning model generations to qualify an evaluator."""
    p = root / PKG_REL / "STAGED-EXECUTION-PLAN.yaml"
    d = yaml.safe_load(p.read_text())
    d["rollup"]["stage_Q_model_generations"] = 40
    _write(p, d)


def nc_pass_rate_saving_invented(root):
    """G13 — claim an expected Stage B saving that depends on results we lack."""
    p = root / PKG_REL / "STAGED-EXECUTION-PLAN.yaml"
    d = yaml.safe_load(p.read_text())
    for s in d["stages"]:
        if s["stage"] == "B":
            s["adaptive_expected_structure"]["value"] = 202
    _write(p, d)


FIXTURES = [
    ("nc-family-count-12", nc_family_count_12),
    ("nc-cells-4096", nc_cells_4096),
    ("nc-drop-a-family", nc_drop_a_family),
    ("nc-operation-vocab-drift", nc_operation_vocab_drift),
    ("nc-provenance-collapse", nc_provenance_collapse),
    ("nc-layer13-claims-cpao", nc_layer13_claims_cpao),
    ("nc-vid05-early-cpao", nc_vid05_early_cpao),
    ("nc-seed-pooling", nc_seed_pooling),
    ("nc-sourcing-deletes-a-slot", nc_sourcing_deletes_a_slot),
    ("nc-silent-sibling-substitution", nc_silent_sibling_substitution),
    ("nc-partial-stage-totalled", nc_partial_stage_totalled),
    ("nc-cash-outlay-guessed", nc_cash_outlay_guessed),
    ("nc-173-hours-mandatory", nc_173_hours_mandatory),
    ("nc-stage-counts-do-not-reconcile", nc_stage_counts_do_not_reconcile),
    ("nc-stage-q-spends-generations", nc_stage_q_spends_generations),
    ("nc-pass-rate-saving-invented", nc_pass_rate_saving_invented),
]


def run_validator(root):
    r = subprocess.run([sys.executable, str(root / PKG_REL / "validators" /
                                            "validate_integration_package.py")],
                       capture_output=True, text=True, timeout=180)
    return r.returncode, r.stdout + r.stderr


def main():
    # sanity: the real package must PASS before any fixture is meaningful
    rc, out = run_validator(ROOT)
    if rc != 0:
        print("ABORT - the real package does not pass; fixtures would be meaningless.")
        print(out)
        return 1
    print("baseline: real package PASSES\n")

    failures = []
    for name, mutate in FIXTURES:
        with tempfile.TemporaryDirectory() as td:
            tmp = pathlib.Path(td) / "repo"
            # copy only what the validator reads, plus git metadata for gate 12
            tmp.mkdir()
            for rel in (E9_REL, PKG_REL, "eval/v1", "eval/battery", "canon/experiments/v1"):
                src = ROOT / rel
                if src.exists():
                    shutil.copytree(src, tmp / rel, dirs_exist_ok=True)
            mutate(tmp)
            rc, out = run_validator(tmp)
            if rc == 0:
                failures.append(name)
                print(f"NOT CAUGHT  {name}  <-- gate is decorative")
            else:
                first = next((l for l in out.splitlines() if l.startswith("FAIL  ")), "")
                print(f"caught      {name:34} {first[6:96]}")

    print()
    if failures:
        print(f"FAIL - {len(failures)} fixture(s) not caught: {failures}")
        return 1
    print(f"PASS - all {len(FIXTURES)} negative fixtures were caught.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
