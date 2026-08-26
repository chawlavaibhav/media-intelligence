#!/usr/bin/env python3
"""Run every committed negative control against the empirical-archive validator.

Each case in fixtures/empirical-archive-negative-controls/CASES.yaml breaks exactly ONE rule of the
canonical storage contract. This runner materialises each case into a temporary directory, runs the
validator, and asserts BOTH the expected outcome and, where declared, that the failure message names
the right rule. A case that fails for the wrong reason is not a passing negative control.

Exit 0 if every case behaved as declared; exit 1 otherwise; exit 2 if the runner could not run.
"""
import json, os, subprocess, sys, tempfile

try:
    import yaml
except ImportError:
    print("[FAIL] PyYAML not available", file=sys.stderr); sys.exit(2)

HERE = os.path.dirname(os.path.abspath(__file__))
CASES = os.path.join(os.path.dirname(HERE), "fixtures", "empirical-archive-negative-controls", "CASES.yaml")
VALIDATOR = os.path.join(HERE, "check_empirical_archive.py")
LISTS = ["attempts", "artifacts", "measurements", "acceptances"]


def fatal(m):
    print(f"[FAIL] {m}", file=sys.stderr); sys.exit(2)


def main():
    if not os.path.isfile(CASES):
        fatal(f"cases file not found: {CASES}")
    doc = yaml.safe_load(open(CASES))
    if not doc or not doc.get("cases"):
        fatal("cases file parsed to nothing or declares no cases")
    baseline, cases = doc["baseline"], doc["cases"]
    if len(cases) < 5:
        fatal(f"only {len(cases)} cases declared; refusing to report a negative-control suite this thin")

    bad = 0
    for c in cases:
        override = c.get("override") or {}
        with tempfile.TemporaryDirectory() as d:
            for name in LISTS:
                rows = override.get(name, baseline.get(name, []))
                with open(os.path.join(d, name + ".jsonl"), "w") as fh:
                    for r in rows:
                        fh.write(json.dumps(r, sort_keys=True) + "\n")
            for fn, content in (c.get("extra_files") or {}).items():
                with open(os.path.join(d, fn), "w") as fh:
                    fh.write(content)
            p = subprocess.run([sys.executable, VALIDATOR, d], capture_output=True, text=True)
            out = p.stdout + p.stderr

        expect = c["expect"]
        got = "pass" if p.returncode == 0 else ("fail" if p.returncode == 1 else f"error(exit {p.returncode})")
        ok = (got == expect)
        detail = ""
        if ok and expect == "fail" and c.get("expect_contains"):
            if c["expect_contains"] not in out:
                ok = False
                detail = f" — failed, but not for the declared reason (no {c['expect_contains']!r} in output)"
        status = "PASS" if ok else "FAIL"
        if not ok:
            bad += 1
        print(f"[{status}] {c['name']:48s} expected {expect:4s} got {got}{detail}")

    print()
    print(f"{len(cases)-bad}/{len(cases)} negative controls behaved as declared")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
