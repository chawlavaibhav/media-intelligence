#!/usr/bin/env bash
# R4-C controls: one valid v3 archive that MUST pass, seventeen broken ones that MUST fail.
# A validator that rejects everything would pass all seventeen negatives and be useless, which is why
# the positive fixture exists.
set -u
V=resources/pre-execution-freeze/validators/validate_topology_v3.py
F=resources/pre-execution-freeze/fixtures/lineage
fail=0

echo "== R4-C v3 topology / lineage controls =="
if python3 "$V" "$F/v3-valid-outcome.yaml" >/dev/null 2>&1; then
  echo "[PASS] v3-valid-outcome                             validated cleanly (all 11 gates)"
else
  echo "[FAIL] v3-valid-outcome did not validate"; fail=1
fi

for f in "$F"/nc-*.yaml; do
  n=$(basename "$f" .yaml)
  out=$(python3 "$V" "$f" 2>&1)
  if echo "$out" | grep -q "^\[FAIL:"; then
    gate=$(echo "$out" | grep -m1 "^\[FAIL:" | sed 's/^\[FAIL:\([^]]*\)\].*/\1/')
    expect=$(echo "$n" | sed 's/^nc-\(G[0-9]*\).*/\1/')
    if [ "$gate" = "$expect" ]; then
      echo "[PASS] $n  rejected by $gate as declared"
    else
      echo "[FAIL] $n  rejected by $gate but declares $expect"; fail=1
    fi
  else
    echo "[FAIL] $n  was NOT rejected"; fail=1
  fi
done
echo
[ "$fail" -eq 0 ] && echo "18/18 lineage controls behaved as declared" || echo "LINEAGE CONTROLS FAILED"
exit "$fail"
