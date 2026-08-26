#!/usr/bin/env bash
# R4-D controls: three known-answer computations that MUST compute, ten broken archives that MUST
# refuse. Control 00-02 exist because an engine that refuses everything would pass all ten negatives.
set -u
V=resources/pre-execution-freeze/validators/recompute_cpao_v3.py
L=resources/pre-execution-freeze/fixtures/lineage
F=resources/pre-execution-freeze/fixtures/cpao
fail=0
echo "== R4-D whole-outcome CpAO v3 controls =="
pos () {
  if python3 "$V" "$1" >/dev/null 2>&1; then echo "[PASS] $2"; else echo "[FAIL] $2 did not compute or match"; fail=1; fi
}
pos "$L/v3-valid-outcome.yaml"                  "v3-valid-outcome            API/tool 50.00 · fully-loaded 71.50"
pos "$F/revision-journey-included.yaml"         "revision-journey-included   API/tool 20.00 · fully-loaded 30.00"
pos "$F/scope-change-cuts-journey.yaml"         "scope-change-cuts-journey   API/tool 10.00 · fully-loaded 15.00"
for f in "$F"/nc-*.yaml; do
  n=$(basename "$f" .yaml)
  python3 "$V" "$f" --expect-refusal >/dev/null 2>&1
  if [ $? -eq 3 ]; then echo "[PASS] $n  refused as required"; else echo "[FAIL] $n did NOT refuse"; fail=1; fi
done
echo
[ "$fail" -eq 0 ] && echo "13/13 CpAO v3 controls behaved as declared" || echo "CPAO V3 CONTROLS FAILED"
exit "$fail"
