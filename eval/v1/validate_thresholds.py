#!/usr/bin/env python3
"""E-C9 — prove no judgement threshold has been promoted to empirical truth.

A threshold may be `approved` ONLY when approval_ref names a real Controller
decision record. Anything else must carry an explicitly provisional status and
an honest empirical_support value.

Run:  python3 eval/v1/validate_thresholds.py
      python3 eval/v1/validate_thresholds.py --selftest
"""
import argparse, copy, io, contextlib, pathlib, sys, yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
REG = ROOT / "eval/v1/THRESHOLD-REGISTER.yaml"

PROVISIONAL = {"proposed", "provisional", "deliberately_not_set", "not_a_threshold"}
VALID_STATUS = PROVISIONAL | {"approved"}
REQUIRED = ["id", "name", "value", "applies_to", "status", "approval_ref",
            "empirical_support", "rationale_kind"]


def validate(doc=None):
    errors = []
    d = doc if doc is not None else yaml.safe_load(REG.read_text())
    if not d:
        print("FAIL: register is empty - an empty check is not a passing check")
        return 1
    ths = d.get("thresholds") or []
    if not ths:
        print("FAIL: register lists zero thresholds")
        return 1

    ids = [t.get("id") for t in ths]
    if len(set(ids)) != len(ids):
        errors.append("duplicate threshold ids")

    approved = 0
    for t in ths:
        tid = t.get("id", "<no id>")
        for f in REQUIRED:
            if f not in t:
                errors.append(f"{tid}: missing required field '{f}'")
        st = t.get("status")
        if st not in VALID_STATUS:
            errors.append(f"{tid}: unknown status '{st}'")
        if st == "approved":
            approved += 1
            if not t.get("approval_ref"):
                errors.append(
                    f"{tid}: status 'approved' with NO approval_ref. A threshold "
                    f"is approved only when a Controller decision record says "
                    f"so; appearing in a specification is not approval.")
        else:
            if t.get("approval_ref"):
                errors.append(f"{tid}: carries an approval_ref but is not approved")
            # a provisional threshold must not claim empirical support
            es = str(t.get("empirical_support", "")).strip().lower()
            if es not in ("none", "") and "not establish" not in es \
                    and "under an assumption" not in es:
                errors.append(
                    f"{tid}: status '{st}' but empirical_support is '{es}'. "
                    f"An unapproved threshold may not claim empirical backing.")
        # a threshold with a real value must say what would support it
        if st in ("proposed", "provisional") and not t.get("what_would_support_it"):
            errors.append(f"{tid}: proposed threshold must state what evidence "
                          f"would support it")
        if st == "deliberately_not_set" and t.get("value") is not None:
            errors.append(f"{tid}: deliberately_not_set must have value null, "
                          f"got {t.get('value')!r}")

    declared = d.get("approved_count")
    if declared != approved:
        errors.append(f"register declares approved_count={declared} but "
                      f"{approved} row(s) are approved")

    print(f"thresholds registered : {len(ths)}")
    print(f"approved              : {approved}")
    print(f"proposed/provisional  : {sum(1 for t in ths if t.get('status') in ('proposed','provisional'))}")
    print(f"deliberately not set  : {sum(1 for t in ths if t.get('status')=='deliberately_not_set')}")
    if errors:
        print(f"\nFAIL - {len(errors)} error(s):")
        for e in errors:
            print("  -", e)
        return 1
    print("\nPASS - no threshold is promoted to empirical truth.")
    return 0


def _run(doc):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = validate(doc)
    return rc


def selftest():
    base = yaml.safe_load(REG.read_text())
    if _run(copy.deepcopy(base)) != 0:
        print("ABORT: real register does not validate.")
        return 1
    print("baseline: real register PASSES\n")
    controls, bad = [], []

    def ctl(n):
        def d(f):
            controls.append((n, f))
            return f
        return d

    @ctl("E-C9: approving a threshold with NO approval_ref must FAIL")
    def c1(d):
        d["thresholds"][0]["status"] = "approved"
        d["approved_count"] = 1
        return d

    @ctl("E-C9: a provisional threshold claiming empirical support must FAIL")
    def c2(d):
        d["thresholds"][0]["empirical_support"] = "validated in production"
        return d

    @ctl("E-C9: a proposed threshold with no supporting-evidence path must FAIL")
    def c3(d):
        del d["thresholds"][0]["what_would_support_it"]
        return d

    @ctl("E-C9: deliberately_not_set carrying a value must FAIL")
    def c4(d):
        d["thresholds"][3]["value"] = 120
        return d

    @ctl("E-C9: miscounting approved_count must FAIL")
    def c5(d):
        d["approved_count"] = 7
        return d

    @ctl("E-C9: unknown status must FAIL")
    def c6(d):
        d["thresholds"][1]["status"] = "basically_fine"
        return d

    @ctl("E-C9: empty register must FAIL")
    def c7(d):
        d["thresholds"] = []
        return d

    for name, fn in controls:
        rc = _run(fn(copy.deepcopy(base)))
        good = rc != 0
        print(f"  [{'ok' if good else 'DEFECT'}] {name} -> rc={rc}")
        if not good:
            bad.append(name)
    print()
    if bad:
        print(f"FAIL - {len(bad)} control(s) not rejected: {bad}")
        return 1
    print(f"PASS - all {len(controls)} negative controls correctly rejected.")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    sys.exit(selftest() if a.selftest else validate())
