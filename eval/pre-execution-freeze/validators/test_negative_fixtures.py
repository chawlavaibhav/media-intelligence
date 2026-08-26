#!/usr/bin/env python3
"""Negative fixtures for the EVAL-009 gates.

A validator that passes everything is not a validator. Each fixture breaks
exactly one gate and asserts rejection. The aggregation fixtures additionally
prove the E9-B requirement directly: aggregation CANNOT forgive a failed
ancestor.
"""
import copy, io, contextlib, pathlib, shutil, sys, tempfile, yaml

HERE = pathlib.Path(__file__).resolve().parent
PKG = HERE.parent
sys.path.insert(0, str(HERE))
import validate_freeze_package as V

FILES = ["CAPABILITY-CONTRACT-v2.yaml", "DEPENDENCY-SCORING-CONTRACT.yaml",
         "CONDITION-ENVELOPE-CONTRACT.yaml", "PRODUCTION-REQUIREMENT-PROFILE-v1.yaml",
         "BENCHMARK-v2-WAVE1.yaml", "EVALUATOR-QUALIFICATION-MAP.yaml",
         "SCIENTIFIC-WAVE1-MODEL-ROSTER.yaml", "WAVE1-CALL-COUNT-FORECAST.yaml"]


def run_with(mutations):
    """Copy the package to a temp dir, apply mutations, run the validator there."""
    tmp = pathlib.Path(tempfile.mkdtemp())
    for f in FILES:
        shutil.copy(PKG / f, tmp / f)
    for f in (PKG).glob("*.md"):
        shutil.copy(f, tmp / f.name)
    for fname, fn in mutations.items():
        d = yaml.safe_load((tmp / fname).read_text())
        d = fn(d)
        (tmp / fname).write_text(yaml.safe_dump(d, sort_keys=False))
    orig = V.PKG
    V.PKG = tmp
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            rc = V.main()
    finally:
        V.PKG = orig
        shutil.rmtree(tmp, ignore_errors=True)
    return rc, buf.getvalue()


CASES = []


def case(gate, name):
    def deco(fn):
        CASES.append((gate, name, fn))
        return fn
    return deco


@case(1, "a V1 capability dropped from the mapping must FAIL")
def c1(_):
    def m(d):
        d["v1_to_v2_mapping"] = d["v1_to_v2_mapping"][:-1]
        return d
    return {"CAPABILITY-CONTRACT-v2.yaml": m}


@case(1, "an added capability with no admission justification must FAIL")
def c1b(_):
    def m(d):
        for x in d["dimensions"]:
            if x.get("v2_disposition") == "added":
                x.pop("admission_justification", None)
                break
        return d
    return {"CAPABILITY-CONTRACT-v2.yaml": m}


@case(2, "blocked_by_prerequisite_failure resolving to 'pass' must FAIL")
def c2(_):
    def m(d):
        for s in d["measurement_states"]:
            if s["id"] == "blocked_by_prerequisite_failure":
                s["outcome_acceptance"] = "satisfied"
        return d
    return {"DEPENDENCY-SCORING-CONTRACT.yaml": m}


@case(2, "blocked treated as not_applicable at outcome level must FAIL")
def c2b(_):
    def m(d):
        for s in d["measurement_states"]:
            if s["id"] == "blocked_by_prerequisite_failure":
                s["outcome_acceptance"] = "not_required"
        return d
    return {"DEPENDENCY-SCORING-CONTRACT.yaml": m}


@case(2, "removing the rule that forbids a descendant passing must FAIL")
def c2c(_):
    def m(d):
        d["prerequisite_graph"]["rules"] = [
            r for r in d["prerequisite_graph"]["rules"] if "may NEVER be `pass`" not in r]
        return d
    return {"DEPENDENCY-SCORING-CONTRACT.yaml": m}


@case(3, "workflow_mode marked customer_side must FAIL")
def c3(_):
    def m(d):
        for c in d["condition_families"]:
            if c["id"] == "COND-WORKFLOW":
                c["provenance"] = "customer_side"
        return d
    return {"CONDITION-ENVELOPE-CONTRACT.yaml": m}


@case(3, "dropping requested_operation as a condition must FAIL")
def c3b(_):
    def m(d):
        d["condition_families"] = [c for c in d["condition_families"] if c["id"] != "COND-OPERATION"]
        return d
    return {"CONDITION-ENVELOPE-CONTRACT.yaml": m}


@case(4, "a PRP requirement carrying a model field must FAIL")
def c4(_):
    def m(d):
        d["example"]["requirements"][0]["model"] = "some-model-v2"
        return d
    return {"PRODUCTION-REQUIREMENT-PROFILE-v1.yaml": m}


@case(4, "a PRP requirement carrying a provider/price must FAIL")
def c4b(_):
    def m(d):
        d["example"]["requirements"][1]["provider"] = "SomeVendor"
        d["example"]["requirements"][1]["price"] = 0.04
        return d
    return {"PRODUCTION-REQUIREMENT-PROFILE-v1.yaml": m}


@case(5, "sweeping every condition family (cartesian) must FAIL")
def c5(_):
    cond = yaml.safe_load((PKG / "CONDITION-ENVELOPE-CONTRACT.yaml").read_text())
    allf = [c["id"] for c in cond["condition_families"]]

    def m(d):
        d["layers"]["layer3_sweeps"]["swept"] = {f: {"items_swept": 4, "extra_levels": 1} for f in allf}
        return d
    return {"BENCHMARK-v2-WAVE1.yaml": m}


@case(5, "removing sweep stop/expansion rules must FAIL")
def c5b(_):
    def m(d):
        d["layers"]["layer3_sweeps"].pop("stop_rule", None)
        return d
    return {"BENCHMARK-v2-WAVE1.yaml": m}


@case(6, "marking an instrument qualified must FAIL")
def c6(_):
    def m(d):
        d["capabilities"][0]["qualified"] = True
        d["instruments_qualified"] = 1
        return d
    return {"EVALUATOR-QUALIFICATION-MAP.yaml": m}


@case(7, "a roster slot justified by credits/access must FAIL")
def c7(_):
    def m(d):
        d["slots"][0]["why_it_changes_production"] = (
            "We already have credits for it and it is available on our account.")
        return d
    return {"SCIENTIFIC-WAVE1-MODEL-ROSTER.yaml": m}


@case(7, "a roster slot with no nearest-redundant candidate must FAIL")
def c7b(_):
    def m(d):
        d["slots"][2].pop("nearest_redundant", None)
        return d
    return {"SCIENTIFIC-WAVE1-MODEL-ROSTER.yaml": m}


@case(8, "a guessed generation price must FAIL")
def c8(_):
    def m(d):
        k = list(d["prices"]["generation_unit_price_by_slot"])[0]
        d["prices"]["generation_unit_price_by_slot"][k] = 0.05
        return d
    return {"WAVE1-CALL-COUNT-FORECAST.yaml": m}


@case(8, "a guessed human rate must FAIL")
def c8b(_):
    def m(d):
        d["prices"]["human_rate"] = 500
        return d
    return {"WAVE1-CALL-COUNT-FORECAST.yaml": m}


@case(9, "totalling a partially-unresolved forecast must FAIL")
def c9(_):
    def m(d):
        d["totals"]["generation_cost"] = 1234.0
        d["totals"]["fully_loaded"] = 5678.0
        return d
    return {"WAVE1-CALL-COUNT-FORECAST.yaml": m}


# ---------------------------------------------------------------------------
# E9-B DIRECT PROOF: aggregation cannot forgive a failed ancestor.
# These exercise the SEMANTICS, not just the document.
# ---------------------------------------------------------------------------
def aggregate(states, required):
    """Reference implementation of the E9-B aggregation rules."""
    COUNTABLE = {"pass", "fail"}
    SATISFIED = {"pass"}
    diag_den = [s for s in states.values() if s in COUNTABLE]
    diag = (sum(1 for s in diag_den if s == "pass") / len(diag_den)) if diag_den else None
    outcome_satisfied = all(states[r] in SATISFIED for r in required)
    return diag, outcome_satisfied


def semantic_cases():
    out = []
    # the motivating case: product absent, dependents blocked
    states = {"product_identity": "fail",
              "logo_wordmark_fidelity": "blocked_by_prerequisite_failure",
              "packaging_brand_colour_fidelity": "blocked_by_prerequisite_failure"}
    req = list(states)
    diag, ok = aggregate(states, req)
    out.append(("blocked descendants do not make the outcome acceptable", ok is False))
    out.append(("blocked descendants are excluded from the diagnostic denominator",
                abs(diag - 0.0) < 1e-9))
    # the V1 flat-fanout bug, reproduced to show it WOULD have passed
    flat = {"product_identity": "fail", "logo_wordmark_fidelity": "pass",
            "packaging_brand_colour_fidelity": "pass"}
    fdiag, fok = aggregate(flat, list(flat))
    out.append(("the old flat fan-out would have scored 0.67 on a totally failed asset",
                abs(fdiag - 2 / 3) < 1e-6))
    out.append(("...and even then the outcome is correctly unsatisfied because the ancestor failed",
                fok is False))
    # not_measured is not satisfied
    nm = {"a": "pass", "b": "not_measured"}
    _, ok2 = aggregate(nm, ["a", "b"])
    out.append(("not_measured does not satisfy an outcome", ok2 is False))
    # genuinely not applicable is not required
    na = {"a": "pass", "b": "not_applicable"}
    _, ok3 = aggregate(na, ["a"])
    out.append(("genuinely not_applicable requirements are simply not required", ok3 is True))
    return out


def main():
    rc, _ = run_with({})
    if rc != 0:
        print("ABORT: the real package does not validate; fixtures prove nothing.")
        return 1
    print("baseline: real package PASSES\n")
    bad = []
    for gate, name, fn in CASES:
        rc, _ = run_with(fn(None))
        ok = rc != 0
        print(f"  [{'ok' if ok else 'DEFECT'}] gate {gate}: {name} -> rc={rc}")
        if not ok:
            bad.append(name)
    print("\n  -- E9-B aggregation semantics --")
    for name, ok in semantic_cases():
        print(f"  [{'ok' if ok else 'DEFECT'}] {name}")
        if not ok:
            bad.append(name)
    print()
    if bad:
        print(f"FAIL - {len(bad)} fixture(s) not rejected: {bad}")
        return 1
    print(f"PASS - all {len(CASES)} gate fixtures rejected and "
          f"{len(semantic_cases())} aggregation semantics hold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
