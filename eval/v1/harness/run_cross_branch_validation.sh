#!/usr/bin/env bash
# EI-C8 — validate Eval's emitted archive with RESOURCES' OWN validator.
#
# This is the completion gate for the storage integration:
#
#   Eval dummy generation -> canonical JSONL handoff
#     -> Resources check_empirical_archive.py -> exit 0
#
# The validator is INVOKED from a worktree of the Resources branch. It is never
# copied into Eval: a second copy would drift, and then Eval would be proving
# compliance against its own stale snapshot of somebody else's contract.
#
# Usage: bash eval/v1/harness/run_cross_branch_validation.sh [resources_ref]
set -uo pipefail

REPO="$(git rev-parse --show-toplevel)"
REF="${1:-origin/work/resources-v1-overnight}"
WT="$(mktemp -d)/res-wt"

cd "$REPO"
echo "== EI-C8 cross-branch storage validation =="
git fetch -q origin "${REF#origin/}" 2>/dev/null || true
SHA="$(git rev-parse "$REF")"
echo "Resources ref   : $REF"
echo "Resources SHA   : $SHA"

git worktree add -q --detach "$WT" "$SHA" || { echo "FAIL: worktree"; exit 2; }
trap 'git worktree remove --force "$WT" >/dev/null 2>&1 || true' EXIT

VALIDATOR="$WT/resources/v1/validators/check_empirical_archive.py"
SCHEMA="$WT/resources/v1/EMPIRICAL-ARTIFACT-MANIFEST-SCHEMA.yaml"
[ -f "$VALIDATOR" ] || { echo "FAIL: validator not found at $VALIDATOR"; exit 2; }
echo "Schema version  : $(grep -m1 -E '^\s*version: v' "$SCHEMA" | tr -d ' ')"
echo "Validator sha256: $(sha256sum "$VALIDATOR" | cut -c1-16)…"
echo

echo "-- regenerating the Eval archive from dummy fixtures --"
python3 "$REPO/eval/v1/harness/run_selftest.py" >/dev/null 2>&1 || {
  echo "FAIL: Eval harness self-test did not pass; not validating a broken archive"; exit 2; }

ARCHIVE="$REPO/eval/v1/harness/out-selftest"
echo "-- running Resources' validator against $ARCHIVE --"
python3 "$VALIDATOR" "$ARCHIVE"
RC=$?
echo
case $RC in
  0) echo "RESULT: PASS — Eval's emission satisfies the current Resources contract (exit 0)";;
  1) echo "RESULT: FAIL — schema violation (exit 1)";;
  2) echo "RESULT: COULD NOT CHECK (exit 2) — this is NOT a pass";;
  *) echo "RESULT: unexpected exit $RC";;
esac
exit $RC
