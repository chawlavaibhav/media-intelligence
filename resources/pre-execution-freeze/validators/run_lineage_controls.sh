#!/usr/bin/env bash
# R4-C controls, extended 2026-08-28 by the RES-007 correction (gate G12 per
# CONTROLLER-PREPILOT-RETURN-REVIEW-1-2026-08-28.md): every v3-valid-*.yaml fixture MUST pass,
# every nc-*.yaml fixture MUST fail for its own declared gate. A validator that rejects
# everything would pass every negative and be useless, which is why the positive fixtures exist.
set -u
V=resources/pre-execution-freeze/validators/validate_topology_v3.py
F=resources/pre-execution-freeze/fixtures/lineage
fail=0
total=0
passed=0

echo "== R4-C v3 topology / lineage controls =="
for f in "$F"/v3-valid-*.yaml; do
  n=$(basename "$f" .yaml)
  total=$((total+1))
  if python3 "$V" "$f" >/dev/null 2>&1; then
    echo "[PASS] $n  validated cleanly (all 12 gates)"; passed=$((passed+1))
  else
    echo "[FAIL] $n did not validate"; fail=1
  fi
done

for f in "$F"/nc-*.yaml; do
  n=$(basename "$f" .yaml)
  total=$((total+1))
  out=$(python3 "$V" "$f" 2>&1)
  if echo "$out" | grep -q "^\[FAIL:"; then
    firstfail=$(echo "$out" | grep -m1 "^\[FAIL:")
    gate=$(echo "$firstfail" | sed 's/^\[FAIL:\([^]]*\)\].*/\1/')
    expect=$(echo "$n" | sed 's/^nc-\(G[0-9]*\).*/\1/')
    # A fixture may declare the exact invariant it must trip (not just the gate), so a
    # control cannot pass by accidentally breaking some unrelated field.
    expect_sub=$(grep -m1 '^# EXPECT-SUBSTRING: ' "$f" | sed 's/^# EXPECT-SUBSTRING: //')
    if [ "$gate" != "$expect" ]; then
      echo "[FAIL] $n  rejected by $gate but declares $expect"; fail=1
    elif [ -n "$expect_sub" ] && ! echo "$firstfail" | grep -qF "$expect_sub"; then
      echo "[FAIL] $n  rejected by $gate but not for '$expect_sub': $firstfail"; fail=1
    else
      echo "[PASS] $n  rejected by $gate as declared${expect_sub:+ (invariant: $expect_sub)}"
      passed=$((passed+1))
    fi
  else
    echo "[FAIL] $n  was NOT rejected"; fail=1
  fi
done
echo
[ "$fail" -eq 0 ] && echo "$passed/$total lineage controls behaved as declared" || echo "LINEAGE CONTROLS FAILED ($passed/$total)"
exit "$fail"
