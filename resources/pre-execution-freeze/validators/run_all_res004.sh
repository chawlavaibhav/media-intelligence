#!/usr/bin/env bash
# Re-verify every mechanically checkable RES-004 claim, plus the inherited contracts.
#   bash resources/pre-execution-freeze/validators/run_all_res004.sh
# Exit 0 = all passed. Nothing here opens raw media, calls any API, or spends anything.
set -u
fail=0
step () { echo; echo "=============================================================="; echo "== $1"; echo "=============================================================="; }

step "1/5  R4-A/C  v3 topology + lineage: 1 valid archive, 17 gate violations"
bash resources/pre-execution-freeze/validators/run_lineage_controls.sh || fail=1

step "2/5  R4-D    whole-outcome CpAO v3: 3 known answers, 10 required refusals"
bash resources/pre-execution-freeze/validators/run_cpao_controls_v3.sh || fail=1

step "3/5  R4-E    controlled-pack requirements: four packs, labelled counts, no invented precision"
python3 resources/pre-execution-freeze/validators/check_pack_requirements.py || fail=1

step "4/5  inherited v2.1 contract still green (historical evidence preserved)"
rm -rf resources/v1/build
bash resources/v1/validators/run_all.sh >/tmp/res004-v1.out 2>&1
rc=$?; tail -3 /tmp/res004-v1.out | sed 's/^/   /'; [ "$rc" -eq 0 ] || fail=1

step "5/5  inherited RES-003 research suite still green"
bash resources/research/pre-e7-macro/validators/run_all_res003.sh >/tmp/res004-r3.out 2>&1
rc=$?; tail -3 /tmp/res004-r3.out | sed 's/^/   /'; [ "$rc" -eq 0 ] || fail=1

echo
echo "=============================================================="
if [ "$fail" -eq 0 ]; then echo "ALL RES-004 CHECKS PASSED"; else echo "SOME CHECKS FAILED"; fi
echo "=============================================================="
exit "$fail"
