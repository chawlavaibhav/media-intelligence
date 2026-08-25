#!/usr/bin/env bash
# Re-verify every R1-R8 claim that is mechanically checkable. Run from the repository root.
#
#   bash resources/v1/validators/run_all.sh
#
# Exit 0 means every check passed. Any non-zero exit means a claim in resources/v1/ no longer holds.
# NOTE: none of this opens a media file. The raw corpus is git-ignored and absent from a clone.
set -u
fail=0
step () { echo; echo "=============================================================="; echo "== $1"; echo "=============================================================="; }

step "1/6  Requirements matrix matches its YAML source of truth (R1)"
python3 resources/v1/validators/build_requirements_matrix.py --check || fail=1

step "2/6  Corpus rebaseline from the committed manifest (R2)"
python3 resources/v1/validators/rebaseline_from_manifest.py || fail=1

step "3/6  Views rebuild deterministically from the manifest (R5)"
# Hash the views BEFORE rebuilding and compare afterwards. Deliberately not `git diff`: on an
# untracked directory git reports no difference and the check would pass vacuously without ever
# comparing anything. An empty check is not a passing check.
VIEW_DIR=resources/v1/views
if ! ls "$VIEW_DIR"/*.jsonl >/dev/null 2>&1; then
  echo "[FAIL] no existing views to compare against; cannot verify determinism"; fail=1
else
  before=$(sha256sum "$VIEW_DIR"/*.jsonl | sha256sum | cut -d" " -f1)
  n_before=$(ls "$VIEW_DIR"/*.jsonl | wc -l)
  python3 resources/v1/validators/build_views.py || fail=1
  after=$(sha256sum "$VIEW_DIR"/*.jsonl | sha256sum | cut -d" " -f1)
  n_after=$(ls "$VIEW_DIR"/*.jsonl | wc -l)
  if [ "$before" = "$after" ] && [ "$n_before" = "$n_after" ]; then
    echo "[PASS] $n_after views rebuilt byte-identically (combined sha256 ${after:0:16}…)"
  else
    echo "[FAIL] rebuilt views differ from the previous views"; fail=1
  fi
fi

step "4/6  Allocation leakage: clean split passes (R3)"
python3 resources/v1/validators/check_allocation_leakage.py \
  resources/v1/fixtures/allocations/DUMMY-01-clean-cross-lineage.yaml || fail=1

step "5/6  NEGATIVE CONTROL: the content-leak split MUST fail (R3)"
if python3 resources/v1/validators/check_allocation_leakage.py \
     resources/v1/fixtures/allocations/DUMMY-02-NEGATIVE-CONTROL-content-leak.yaml >/dev/null 2>&1; then
  echo "[FAIL] DUMMY-02 passed. The content-lineage check has stopped working."; fail=1
else
  echo "[PASS] DUMMY-02 correctly rejected (content leak detected)"
fi

step "6/6  Empirical archive schema at 1,000 artifacts (R8)"
python3 resources/v1/validators/check_empirical_archive.py \
  resources/v1/fixtures/empirical-archive-dummy/artifacts.jsonl \
  resources/v1/fixtures/empirical-archive-dummy/measurements.jsonl \
  resources/v1/fixtures/empirical-archive-dummy/acceptances.jsonl || fail=1

echo
echo "=============================================================="
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASSED"; else echo "SOME CHECKS FAILED"; fi
echo "=============================================================="
exit "$fail"
