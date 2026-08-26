#!/usr/bin/env bash
# R-C4 negative controls: prove the three lineage outcomes are distinguishable.
#
#   independent registered lineages -> exit 0  (clean)
#   one shared registered lineage   -> exit 1  (leak)
#   unregistered lineage            -> exit 3  (INDETERMINATE, and NOT clean)
#
# If NC-03 or NC-04 ever returns 0, an unregistered source is being silently certified as an
# independent holdout, which is the defect R-C4 exists to prevent.
set -u
V=resources/v1/validators/check_allocation_leakage.py
F=resources/v1/fixtures/allocations
fail=0

check () {  # name, file, expected exit
  python3 "$V" "$F/$2" >/tmp/lnc.out 2>&1
  got=$?
  if [ "$got" -eq "$3" ]; then
    echo "[PASS] $1: exit $got as expected"
  else
    echo "[FAIL] $1: expected exit $3, got $got"; sed 's/^/         /' /tmp/lnc.out | tail -4; fail=1
  fi
}

echo "== R-C4 lineage negative controls =="
check "NC-01 two independent registered lineages -> clean        " LINEAGE-NC-01-independent-lineages.yaml 0
check "NC-02 one shared registered lineage       -> leak         " LINEAGE-NC-02-dependent-lineage.yaml    1
check "NC-03 unregistered source in a protected role -> indeterminate" LINEAGE-NC-03-unknown-lineage.yaml  3
check "NC-04 two DIFFERENT unknown lineages      -> indeterminate" LINEAGE-NC-04-unknown-vs-unknown.yaml   3
echo
[ "$fail" -eq 0 ] && echo "4/4 lineage negative controls behaved as declared" || echo "LINEAGE NEGATIVE CONTROLS FAILED"
exit "$fail"
