#!/usr/bin/env bash
# R3-E controls: one known-answer fixture that must COMPUTE, eight that must REFUSE.
# A refusal engine that refuses everything would be useless, which is why control 00 exists.
set -u
V=resources/research/pre-e7-macro/validators/recompute_outcome_cpao.py
F=resources/research/pre-e7-macro/fixtures/cpao
fail=0

echo "== R3-E whole-outcome CpAO controls =="
if python3 "$V" "$F/outcome-happy.yaml" >/dev/null 2>&1; then
  echo "[PASS] 00-outcome-happy                              computed and matched (45.25 XTS, CpAO 45.25)"
else
  echo "[FAIL] 00-outcome-happy did not compute or did not match"; fail=1
fi

for f in "$F"/nc-*.yaml; do
  n=$(basename "$f" .yaml)
  python3 "$V" "$f" --expect-refusal >/dev/null 2>&1
  if [ $? -eq 3 ]; then
    echo "[PASS] $n  refused as required"
  else
    echo "[FAIL] $n did NOT refuse"; fail=1
  fi
done
echo
[ "$fail" -eq 0 ] && echo "9/9 CpAO controls behaved as declared" || echo "CPAO CONTROLS FAILED"
exit "$fail"
