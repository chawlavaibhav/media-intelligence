#!/usr/bin/env python3
"""Negative controls for validate_capability_contract.py.

EVAL-002's lesson, paid for once already: negative-control fixtures exposed
three real defects that were NOT visible from reading the code, including a run
that raised integrity errors and still exited successfully.

Each control deliberately breaks the contract in one way and asserts the
validator REJECTS it. A validator that passes everything is not a validator.

Run:  python3 eval/v1/test_validator_negative_controls.py
"""
import copy, io, sys, yaml, pathlib, contextlib, tempfile, os

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "eval/v1"))
CONTRACT = ROOT / "eval/v1/capability-contract.yaml"

import validate_capability_contract as V


def run_against(doc):
    """Run the validator against a mutated document; return (rc, output)."""
    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as fh:
        yaml.safe_dump(doc, fh)
        tmp = fh.name
    orig = V.CONTRACT
    V.CONTRACT = pathlib.Path(tmp)
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            rc = V.main()
    finally:
        V.CONTRACT = orig
        os.unlink(tmp)
    return rc, buf.getvalue()


BASE = yaml.safe_load(CONTRACT.read_text())

CONTROLS = []

def control(name):
    def deco(fn):
        CONTROLS.append((name, fn))
        return fn
    return deco


@control("empty contract must FAIL (an empty check is not a passing check)")
def c_empty(d):
    d["dimensions"] = []
    return d

@control("dropping a frozen capability must FAIL")
def c_missing(d):
    d["dimensions"] = [x for x in d["dimensions"] if x["id"] != "object_count"]
    return d

@control("adding a capability outside the frozen 36 must FAIL (silent scope change)")
def c_extra(d):
    new = copy.deepcopy(d["dimensions"][0])
    new["id"] = "vibes_alignment"
    d["dimensions"].append(new)
    return d

@control("duplicated capability id must FAIL")
def c_dupe(d):
    d["dimensions"].append(copy.deepcopy(d["dimensions"][0]))
    return d

@control("missing mandatory field must FAIL")
def c_missing_field(d):
    del d["dimensions"][3]["registry_conditions"]
    return d

@control("empty mandatory field must FAIL")
def c_empty_field(d):
    d["dimensions"][4]["definition"] = ""
    return d

@control("observation_unit outside Canon's vocabulary must FAIL")
def c_bad_unit(d):
    d["dimensions"][2]["observation_unit"] = "clip_ish"
    return d

@control("two-level difficulty ladder must FAIL")
def c_short_ladder(d):
    d["dimensions"][5]["difficulty_ladder"] = d["dimensions"][5]["difficulty_ladder"][:2]
    return d

@control("out-of-order ladder level must FAIL")
def c_ladder_order(d):
    d["dimensions"][6]["difficulty_ladder"][1]["level"] = 7
    return d

@control("family G promoted to a hard routing constraint must FAIL")
def c_g_hard(d):
    for x in d["dimensions"]:
        if x["id"] == "proposition_objective_fit":
            x["routing_use"] = "hard_constraint"
    return d

@control("unknown result_form must FAIL")
def c_bad_result(d):
    d["dimensions"][7]["result_form"] = "looks_good_to_me"
    return d

@control("unknown modality must FAIL")
def c_bad_modality(d):
    d["dimensions"][8]["modalities"] = ["hologram"]
    return d


def main():
    print("Negative controls for validate_capability_contract.py\n")
    # Sanity: the real contract must PASS, or the controls prove nothing.
    rc, _ = run_against(copy.deepcopy(BASE))
    if rc != 0:
        print("ABORT: the real contract does not pass; controls are meaningless.")
        return 1
    print("  baseline: real contract PASSES (rc=0)\n")

    failures = []
    for name, fn in CONTROLS:
        rc, out = run_against(fn(copy.deepcopy(BASE)))
        # Each control must be REJECTED individually.
        ok = rc != 0
        print(f"  [{'ok' if ok else 'DEFECT'}] {name}  -> rc={rc}")
        if not ok:
            failures.append(name)

    print()
    if failures:
        print(f"FAIL — {len(failures)} control(s) were NOT rejected:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"PASS — all {len(CONTROLS)} negative controls correctly rejected, "
          f"and the real contract passes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
