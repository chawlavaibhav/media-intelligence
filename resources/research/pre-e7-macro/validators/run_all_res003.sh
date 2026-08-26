#!/usr/bin/env bash
# Re-verify every mechanically checkable RES-003 claim. Run from the repository root.
#   bash resources/research/pre-e7-macro/validators/run_all_res003.sh
# Exit 0 = all passed. Nothing here opens a media file or calls any API.
set -u
fail=0
step () { echo; echo "=============================================================="; echo "== $1"; echo "=============================================================="; }

step "1/4  R3-A source register completeness and lineage integrity"
python3 resources/research/pre-e7-macro/validators/check_source_register.py || fail=1

step "2/4  R3-B corpus rebaseline from committed metadata (no media opened)"
python3 resources/v1/validators/rebaseline_from_manifest.py || fail=1

step "3/4  R3-E whole-outcome CpAO: known answer + 8 required refusals"
bash resources/research/pre-e7-macro/validators/run_cpao_controls.sh || fail=1

step "4/4  Inherited V1/V2.1 contract still green (nothing regressed)"
rm -rf resources/v1/build
bash resources/v1/validators/run_all.sh >/tmp/res003-v1.out 2>&1
rc=$?
tail -3 /tmp/res003-v1.out | sed 's/^/   /'
[ "$rc" -eq 0 ] || fail=1

echo
echo "=============================================================="
if [ "$fail" -eq 0 ]; then echo "ALL RES-003 CHECKS PASSED"; else echo "SOME CHECKS FAILED"; fi
echo "=============================================================="
exit "$fail"
