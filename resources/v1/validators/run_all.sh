#!/usr/bin/env bash
# Re-verify every mechanically checkable claim in resources/v1/. Run from the repository root.
#
#   bash resources/v1/validators/run_all.sh
#
# Exit 0 means every check passed. Non-zero means a claim in resources/v1/ no longer holds.
#
# NOTE: nothing here opens a media file. The raw corpus is git-ignored and absent from a clone.
# Large views and the 1,000-attempt synthetic archive are DETERMINISTIC BUILD PRODUCTS: they are
# regenerated into resources/v1/build/ (git-ignored) and verified against committed fingerprints
# rather than being carried in git (R-C3).
set -u
fail=0
step () { echo; echo "=============================================================="; echo "== $1"; echo "=============================================================="; }

step "1/8  Requirements matrix matches its YAML source of truth (R1)"
python3 resources/v1/validators/build_requirements_matrix.py --check || fail=1

step "2/8  Corpus rebaseline from the committed manifest (R2)"
python3 resources/v1/validators/rebaseline_from_manifest.py || fail=1

step "3/8  Views rebuild byte-identically from the manifest (R5, R-C3)"
# Rebuilds into build/ and compares counts + per-view sha256 + a combined fingerprint against the
# committed views/view-fingerprints.json. Deliberately NOT `git diff`: on an untracked or
# git-ignored directory git reports no difference and the check would pass without comparing
# anything. An empty check is not a passing check.
python3 resources/v1/validators/build_views.py || fail=1

step "4/8  Allocation leakage: clean cross-lineage split passes (R3)"
python3 resources/v1/validators/check_allocation_leakage.py \
  resources/v1/fixtures/allocations/DUMMY-01-clean-cross-lineage.yaml || fail=1

step "5/8  NEGATIVE CONTROL: the content-leak split MUST fail (R3)"
python3 resources/v1/validators/check_allocation_leakage.py \
  resources/v1/fixtures/allocations/DUMMY-02-NEGATIVE-CONTROL-content-leak.yaml >/dev/null 2>&1
if [ $? -eq 1 ]; then
  echo "[PASS] DUMMY-02 correctly rejected (content leak detected)"
else
  echo "[FAIL] DUMMY-02 did not report a leak. The content-lineage check has stopped working."; fail=1
fi
# Same membership, byte level only: must PASS, demonstrating the blind spot it does not endorse.
python3 resources/v1/validators/check_allocation_leakage.py \
  resources/v1/fixtures/allocations/DUMMY-03-same-split-byte-level-only.yaml >/dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "[PASS] DUMMY-03 passes at byte level — the same split a hash check would certify"
else
  echo "[FAIL] DUMMY-03 no longer passes at byte level; the contrast case is broken"; fail=1
fi

step "6/8  R-C4 lineage negative controls: unknown lineage cannot be certified"
bash resources/v1/validators/run_lineage_negative_controls.sh || fail=1

step "7/8  Empirical storage contract at 1,000 attempts + 22 negative controls (R8, R-C2, RI-C1..C4)"
python3 resources/v1/validators/make_dummy_archive.py || fail=1
python3 resources/v1/validators/check_empirical_archive.py resources/v1/build/empirical-archive-dummy || fail=1
python3 resources/v1/validators/run_archive_negative_controls.py || fail=1

step "8/8  RI-C5 cross-branch gate: does the Eval archive validate?"
# Reported, NOT counted into `fail`. The Resources contract is what this suite verifies; whether Eval
# has yet emitted it is Eval's work, and folding their state into our exit code would make our own
# suite unreadable. The gate's own exit code is what the integration brief records.
if bash resources/v1/validators/validate_eval_archive.sh >/tmp/eval-gate.out 2>&1; then
  echo "[PASS] GATE MET — the Eval archive validates against the Resources v2.1 contract"
else
  echo "[INFO] GATE NOT MET — status BLOCKED_WAITING_FOR_EVAL_INTERFACE"
  echo "       exact failing fields: resources/v1/EVAL-ARCHIVE-INTERFACE-DELTA.md"
  tail -4 /tmp/eval-gate.out | sed 's/^/       /'
fi

echo
echo "=============================================================="
if [ "$fail" -eq 0 ]; then echo "ALL RESOURCES CHECKS PASSED"; else echo "SOME CHECKS FAILED"; fi
echo "=============================================================="
exit "$fail"
