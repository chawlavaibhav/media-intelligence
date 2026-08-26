# EMP-001 pre-spend verification record

**Date:** 26 Aug 2026
**Branch:** `work/eval-012-emp-001-zero-spend`
**External calls made producing this record: 0. Spend: USD 0 / INR 0.**

Every block below is **copied from a fresh run in this branch**, not written from expectation.
Environment: macOS (Darwin 23.6.0), Python 3.14.6, pytest 9.1.1, PyYAML 6.0.3 in a throwaway
virtualenv outside the repository. `hb-view` and `fc-list` are local rendering tools; nothing here
reaches a network.

---

## Step 1 — all EMP-001 tests

```
$ python3 -m pytest -q eval/empirical-tranche-1/tests
........................................................................ [ 88%]
..................                                                       [100%]
162 passed in 0.43s
EXIT=0
```

## Step 2 — inherited V1 harness verification

```
$ python3 eval/v1/harness/run_selftest.py
==========================================================================
RESULT: 107/107 checks passed
Registry rows created: 0  (must be 0)
Paid API calls made:   0
==========================================================================
EXIT=0
```

```
$ bash eval/v1/harness/run_cross_branch_validation.sh

cost-ledger entries:   19
trials:                5  (one call = one trial)

[PASS] one call = one trial: every attempt_id maps to a unique trial_id
[PASS] lane and status use the frozen machine vocabularies
[PASS] every cost_ref resolves to an immutable cost-ledger entry
[PASS] no provider failure is laundered into a measurement absence
[PASS] every failed/refused attempt is preserved individually with its reason
[PASS] status 'ok' <=> exactly one artifact; any other status <=> none
[PASS] repeats and retries are distinct; no repeat appears in a retry chain
[PASS] observation units use the canonical vocabulary verbatim
[PASS] derived artifacts inherit their parent's trial and attempt
[PASS] no output is stored more than once
[PASS] every attempt carries a cost reference
[PASS] fan-out 7.00 measurements per artifact — one generation, many measurements

RESULT: PASS — Eval's emission satisfies the current Resources contract (exit 0)
EXIT=0
```

## Step 3 — dry runs, network disabled

The no-network property is not asserted here in prose; it is a **test**. `test_preflight.py::
test_dry_run_needs_no_network_at_all` poisons `socket.socket.connect`, `connect_ex` and
`socket.create_connection`, then runs the whole preflight — including the V1 harness self-test,
which is invoked **in-process** precisely so the poison covers it. A subprocess would escape the
patch and the control would be theatre. Equivalent controls exist for the pack builder
(`test_latin_pack.py`), the qualification runner and the A-TEXT runner.

```
$ python3 eval/empirical-tranche-1/preflight.py --dry-run
verdict: PREFLIGHT_GREEN
  [PASS] adapter_path_blocked
  [PASS] authorisation_blocked
  [PASS] geometry_fixtures
  [PASS] harness_selftest
  [PASS] one_call_one_trial
  [PASS] protected_baselines
  [PASS] registry_empirical_rows
  [PASS] synthetic_cannot_reach_registry
external calls: 0   spend USD: 0
written: /Users/vaibhavchawla/Vaibhav_Personal_Projects/media-intelligence-worktrees/eval-012/eval/empirical-tranche-1/preflight-result.json
EXIT=0
```

```
$ python3 eval/empirical-tranche-1/text_qualification/qualify_text.py --dry-run
dry run: 2 synthetic candidates
  fake-openai-candidate      devanagari= 576 latin= 576 scope=['devanagari', 'latin']
  fake-google-candidate      devanagari= 576 latin=   0 scope=none
external calls: 0   spend USD: 0
written: /Users/vaibhavchawla/Vaibhav_Personal_Projects/media-intelligence-worktrees/eval-012/eval/empirical-tranche-1/text_qualification/qualification-dryrun.json
EXIT=0
```

```
$ python3 eval/empirical-tranche-1/atex/run_atex.py --dry-run
generations: 16  per route: {'IMG-01': 8, 'IMG-02': 8}  retries: 0
registry rows written: 0  boundary refused synthetic evidence: True
external calls: 0   spend USD: 0
written: /Users/vaibhavchawla/Vaibhav_Personal_Projects/media-intelligence-worktrees/eval-012/eval/empirical-tranche-1/atex/atex-dryrun.json
EXIT=0
```

### The refusal paths, exercised

```
$ python3 eval/empirical-tranche-1/preflight.py          # no --dry-run, no authorisation
REFUSED: EMP-001 paid execution is not authorised, so there is no non-dry-run preflight to perform. Reasons:
  - no authorisation file exists at that path
Re-run with --dry-run.
EXIT=2
```

```
$ python3 eval/empirical-tranche-1/atex/run_atex.py --live
REFUSED: EMP-001 paid A-TEXT generation is not authorised.
  - no authorisation file exists at that path
EXIT=2
```

## Step 4 — protected baselines, byte for byte

```
$ shasum -a 256 -c <(grep -v '^#' eval/empirical-tranche-1/protected-baselines.sha256)
eval/v1/capability-contract.yaml: OK
eval/v1/bank/master-bank-v1.jsonl: OK
eval/v1/instruments/fixtures/cv-geometry/manifest.json: OK
eval/battery/devanagari-exactness/human-validation/human-validation-v1.json: OK
eval/battery/devanagari-exactness/CHECKER-CONTRACT.md: OK
eval/battery/devanagari-exactness/build_items.py: OK
eval/battery/devanagari-exactness/devtext.py: OK
eval/battery/devanagari-exactness/checker_input.py: OK
eval/battery/devanagari-exactness/perturb.py: OK
eval/registry/registry-v1.jsonl: OK
eval/v1/harness/harness.py: OK
eval/v1/harness/models.py: OK
eval/v1/harness/adapters.py: OK
EXIT=0
```

### Capability Registry

```
$ grep -v '^#' eval/registry/registry-v1.jsonl | grep -c '[^[:space:]]'
0
```

Zero empirical rows. Unchanged since before this branch, and its SHA-256 is one of the thirteen
verified above.

### Nothing outside the tranche package was touched

```
$ git diff --name-only origin/main...HEAD | grep -v '^eval/empirical-tranche-1/' | grep -v '^.gitignore$'
(no output — only the tranche package and .gitignore changed)
```

The only change outside `eval/empirical-tranche-1/` is `.gitignore`, which adds three entries:
the runtime authorisation file (so a real approval can never be committed) and the two
reproducible build directories.

---

## Deviations from the implementation plan, and why

1. **Import path.** Plan Task 1 Step 1 shows `from eval.empirical_tranche_1.budget_guard import`.
   The authoritative file structure in the same plan — and EVAL-012, and CONTROL-STATE — names the
   directory `eval/empirical-tranche-1/`. A hyphen is not a legal Python identifier, so that
   dotted import cannot address the frozen directory name. The **directory name is authoritative**;
   the modules are imported by name via `tests/conftest.py`, exactly as the Devanagari battery
   already does. No behaviour differs.

2. **`sha256sum` is not present on macOS.** `shasum -a 256` is used instead; it is the same
   algorithm and the same digests. `run_cross_branch_validation.sh` calls `sha256sum` for a
   cosmetic banner line only and still exits 0.

3. **The human perceptibility review was NOT performed and NOT fabricated.** Plan Task 2 Step 5
   would have every mismatch marked `visible_difference=yes`. EVAL-012 overrides this where the
   review cannot be honestly performed, and it cannot be: this worker is not a person reading a
   surface. What WAS done is the mechanical half — all 48 mismatches differ after NFC **and** in
   their decoded RGBA8 raster, gated with the battery's existing pixel comparison. The review
   sheet is emitted **unfilled** and the record marks it outstanding.

4. **Development tooling.** `pytest` and `PyYAML` were installed into a throwaway virtualenv
   outside the repository. They are free, standard Python dev tooling from PyPI; no provider,
   model or evaluator was involved and no money was spent.

5. **Task 9 was not executed.** It is paid execution and remains blocked on explicit user
   approval, exactly as the plan states.
