#!/usr/bin/env bash
# RI-C5 cross-branch gate: does the CORRECTED Eval harness archive validate against the Resources
# v2.1 persistence contract?
#
#   bash resources/v1/validators/validate_eval_archive.sh [ref] [archive_path_within_repo]
#
# Defaults to origin/work/eval-v1-overnight and eval/v1/harness/out-selftest.
#
# Read-only with respect to Eval: it checks the branch out into a DETACHED throwaway worktree and
# never writes to any eval/ path. Resources does not edit Eval-owned files.
#
# Exit 0 = the gate is met. Exit 1 = the archive does not yet validate (the exact failing fields are
# printed). Exit 2 = could not check.
set -u
REF="${1:-origin/work/eval-v1-overnight}"
SUB="${2:-eval/v1/harness/out-selftest}"
WT="$(mktemp -d)/evalwt"

cleanup () { git worktree remove --force "$WT" >/dev/null 2>&1 || true; rm -rf "$(dirname "$WT")"; }
trap cleanup EXIT

git fetch -q origin "${REF#origin/}" 2>/dev/null || true
if ! git rev-parse --verify -q "$REF" >/dev/null; then
  echo "[FAIL] cannot resolve ref $REF"; exit 2
fi
git worktree add -q --detach "$WT" "$REF" || { echo "[FAIL] could not create worktree for $REF"; exit 2; }

echo "Eval ref:      $REF @ $(git -C "$WT" rev-parse --short HEAD)"
echo "Eval archive:  $SUB"
echo "Last Eval commit touching that archive:"
git log --oneline -1 "$REF" -- "$SUB" | sed 's/^/  /'
echo

if [ ! -d "$WT/$SUB" ]; then
  echo "[FAIL] $SUB does not exist on $REF"; exit 2
fi

python3 resources/v1/validators/check_empirical_archive.py "$WT/$SUB"
rc=$?
echo
if [ "$rc" -eq 0 ]; then
  echo "GATE MET: the Eval archive validates against the Resources v2.1 contract."
else
  echo "GATE NOT MET (validator exit $rc): status BLOCKED_WAITING_FOR_EVAL_INTERFACE."
  echo "The failing fields are listed above. The validator was NOT weakened to accommodate them."
fi
exit "$rc"
