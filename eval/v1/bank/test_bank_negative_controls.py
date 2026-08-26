#!/usr/bin/env python3
"""Negative controls for the E4 bank validator.

A validator that passes everything is not a validator. Each control breaks the
bank in one way and asserts rejection.
"""
import io, json, sys, pathlib, contextlib, shutil, tempfile
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_bank as B

SRC = HERE / "master-bank-v1.jsonl"
BASE = [json.loads(l) for l in SRC.read_text().splitlines() if l.strip()]


def run(items):
    tmp = pathlib.Path(tempfile.mkdtemp())
    orig = B.OUT
    B.OUT = tmp
    try:
        (tmp / "master-bank-v1.jsonl").write_text(
            "\n".join(json.dumps(i, sort_keys=True) for i in items) + "\n")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = B.validate(verbose=False)
        return rc
    finally:
        B.OUT = orig
        shutil.rmtree(tmp, ignore_errors=True)


CONTROLS = []
def ctl(name):
    def d(fn):
        CONTROLS.append((name, fn)); return fn
    return d

@ctl("empty bank must FAIL")
def c1(x): return []

@ctl("99 items must FAIL")
def c2(x): return x[:-1]

@ctl("duplicate item id must FAIL")
def c3(x): return x[:-1] + [dict(x[0])]

@ctl("wrong atomic/compound split must FAIL")
def c4(x):
    y = [dict(i) for i in x]
    for i in y:
        if i["class"] == "compound":
            i["class"] = "atomic"; i["atomic_group"] = "exact_text"; break
    return y

@ctl("compound item with empty fan-out must FAIL")
def c5(x):
    y = [dict(i) for i in x]
    for i in y:
        if i["class"] == "compound":
            i["measurement_fanout"] = []; break
    return y

@ctl("fan-out claiming a capability the contract forbids must FAIL")
def c6(x):
    y = [dict(i) for i in x]
    for i in y:
        if i["class"] == "compound" and i["scenario_family"] == "product_packshot":
            i["measurement_fanout"] = i["measurement_fanout"] + ["single_speaker_lip_sync"]
            break
    return y

@ctl("still image claiming a temporal measurement must FAIL")
def c7(x):
    y = [dict(i) for i in x]
    for i in y:
        if i["class"] == "compound" and i["modality"] == "image":
            i["measurement_fanout"] = i["measurement_fanout"] + ["person_stability_in_clip"]
            break
    return y

@ctl("unknown capability id in fan-out must FAIL")
def c8(x):
    y = [dict(i) for i in x]
    y[-1] = dict(y[-1])
    y[-1]["measurement_fanout"] = y[-1]["measurement_fanout"] + ["vibes_score"]
    return y

@ctl("E-C3: bank grown beyond 100 must FAIL")
def c10(x):
    return x + [dict(x[0], item_id="atomic-999")]

@ctl("E-C3: a two-speaker capability faked onto a scenario without two visible speakers must FAIL")
def c11(x):
    y = [dict(i) for i in x]
    for i in y:
        # typography_led_image has no speakers at all; claiming the two-speaker
        # capability there would inflate the denominator with an opportunity
        # that cannot possibly exhibit a wrong turn assignment.
        if i["class"] == "compound" and i["scenario_family"] == "typography_led_image":
            i["measurement_fanout"] = sorted(
                i["measurement_fanout"] + ["two_speaker_turn_assignment_and_lip_sync"])
            break
    return y

@ctl("E-C3: a two-speaker ATOMIC probe on a non-speaker modality must FAIL")
def c12(x):
    y = [dict(i) for i in x]
    for i in y:
        if i.get("primary_capability") == "two_speaker_turn_assignment_and_lip_sync":
            i["modality"] = "image"          # cannot show two speakers taking turns
            break
    return y

@ctl("scenario family with 5 items must FAIL")
def c9(x):
    for idx, i in enumerate(x):
        if i.get("scenario_family") == "product_packshot":
            return x[:idx] + x[idx+1:] + [dict(x[0], item_id="filler-999")]
    return x


def main():
    if run(BASE) != 0:
        print("ABORT: the real bank does not validate; controls prove nothing.")
        return 1
    print("baseline: real bank PASSES\n")
    bad = []
    for name, fn in CONTROLS:
        rc = run(fn([dict(i) for i in BASE]))
        ok = rc != 0
        print(f"  [{'ok' if ok else 'DEFECT'}] {name} -> rc={rc}")
        if not ok:
            bad.append(name)
    print()
    if bad:
        print(f"FAIL — {len(bad)} control(s) not rejected: {bad}")
        return 1
    print(f"PASS — all {len(CONTROLS)} negative controls correctly rejected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
