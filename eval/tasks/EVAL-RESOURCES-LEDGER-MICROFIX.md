# EVAL–RESOURCES LEDGER MICROFIX

**Status:** AUTHORIZED final micro-fix on `work/eval-v1-overnight` only.  
**Purpose:** close the last remaining Eval→Resources wire-format failure discovered by Resources after Eval had already validated against an older Resources commit.  
**Spend:** ₹0. No paid calls, no new benchmark execution, no instrument qualification, no Registry population, no merge to `main`.

## Root cause

This is a branch-order race, not a new architecture defect.

Eval commit `adac747` validated successfully against Resources commit `e974c813...` (schema v2). Resources then tightened the canonical cost-ledger contract in commit `db54e972...` (schema v2.1) and revalidated Eval `adac747`.

At `adac747`, attempts/artifacts/measurements/acceptances all validate cleanly against Resources v2.1. The only remaining failures are in the synthetic cost ledger:

- 19/19 missing `unit`
- 19/19 missing `recorded_at`
- 19/19 missing `basis`
- 19/19 missing `immutable`
- consequent invalid `basis`
- consequent `immutable != true`

Total: 19 × 6 = 114 violations.

Authoritative evidence:
- Resources branch: `work/resources-v1-overnight`
- Resources head to validate against: `db54e972a8a0d593e3c3455f630641906e7a58f6`
- `resources/v1/EVAL-ARCHIVE-INTERFACE-DELTA.md`
- `resources/v1/validators/check_empirical_archive.py`

## Required change — TDD, minimal only

### RED

Before production code, extend the existing Eval harness self-test so the emitted synthetic ledger is asserted to satisfy the current Resources v2.1 minimum ledger contract. At minimum every emitted ledger row must contain:

- an entry id (`ledger_entry_id`, or the Resources-accepted `cost_ref` alias)
- `amount`
- `currency`
- `unit`
- `recorded_at`
- `basis`
- `immutable`

For synthetic self-tests additionally require:
- `basis == "synthetic_test"`
- `synthetic is true`
- `immutable is true`

Run the test before changing `_ledger_line()` and record that it fails for the expected missing fields.

### GREEN

Make the smallest source change in `eval/v1/harness/harness.py` so `_ledger_line()` emits the required v2.1 fields.

Controller-approved mapping for current synthetic self-tests:

- existing `cost_ref` may remain the ledger entry id alias;
- `unit: "call"`;
- `recorded_at`: a deterministic timestamp/value produced by the harness clock (or another deterministic ISO-8601 UTC test timestamp if the self-test clock is intentionally synthetic); do not introduce nondeterministic byte drift;
- `basis: "synthetic_test"`;
- `immutable: true`;
- `synthetic: true`.

Keep the existing explicit disclaimer that the amount is fabricated test data and not a provider price. Do **not** invent a real-provider cost source.

`currency: "USD"` is not a merge blocker under Resources v2.1. You may switch synthetic rows to `XTS` only if doing so is already supported by the self-test and does not broaden this task; otherwise leave currency unchanged. Do not spend time redesigning test currency semantics.

### VERIFY GREEN

Run:

1. `python3 eval/v1/harness/run_selftest.py`
2. all existing Eval verification suites used by the previous integration pass
3. **the real cross-branch gate against the latest Resources head**:

`bash eval/v1/harness/run_cross_branch_validation.sh`

Before the final gate, refresh `origin/work/resources-v1-overnight` and record the exact Resources SHA. It must be at least `db54e972a8a0d593e3c3455f630641906e7a58f6`; if the branch moved, validate against the newer head.

## Completion gate

This task is complete only if:

> Eval dummy archive → current Resources `check_empirical_archive.py` → **exit 0**

and the output explicitly shows:
- zero attempt violations;
- zero artifact violations;
- zero measurement violations;
- zero acceptance violations;
- zero cost-ledger violations.

Do not weaken or copy the Resources validator into Eval. Use the Resources branch validator directly through the existing cross-branch runner/worktree pattern.

## Documentation

Append a short final section to `eval/findings/EVAL-RESOURCES-STORAGE-INTEGRATION-CONTROLLER-BRIEF.md` titled `Final v2.1 ledger closure` recording:
- previous Eval SHA `adac747...`;
- Resources SHA used;
- RED test failure evidence;
- minimal code change;
- self-test result;
- cross-branch validator exit code;
- final Eval commit SHA.

Commit and push to `work/eval-v1-overnight`. Do not merge.