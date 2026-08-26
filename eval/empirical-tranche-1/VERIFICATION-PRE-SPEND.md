# EMP-001 pre-spend verification record

**Date:** 27 Aug 2026
**Branch:** `work/eval-014-emp-001-budget-continuity`
**Supersedes:** the EVAL-013 record
**External calls made producing this record: 0. Spend: USD 0 / INR 0.**

Copied from fresh runs in this branch. Environment: macOS (Darwin 23.6.0), Python 3.14.6,
pytest 9.1.1, PyYAML 6.0.3 in a throwaway virtualenv outside the repository. No API key was used;
the rehearsal sets `OPENAI_API_KEY`/`GOOGLE_API_KEY`/`FAL_KEY` to the literal string
`REHEARSAL-NOT-A-REAL-KEY`.

---

## Step 1 — all EMP-001 tests

```
$ python3 -m pytest -q eval/empirical-tranche-1/tests
...........................                                              [100%]
315 passed in 24.96s
EXIT=0
```

Up from 247 at the EVAL-013 head; 68 new controls.

## Step 2 — inherited V1 harness verification

```
$ python3 eval/v1/harness/run_selftest.py
RESULT: 107/107 checks passed
Registry rows created: 0  (must be 0)
Paid API calls made:   0
==========================================================================
EXIT=0
```

```
$ bash eval/v1/harness/run_cross_branch_validation.sh

RESULT: PASS — Eval's emission satisfies the current Resources contract (exit 0)
EXIT=0
```

## Step 3 — dry-run preflight

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
written: /Users/vaibhavchawla/Vaibhav_Personal_Projects/media-intelligence-worktrees/eval-014/eval/empirical-tranche-1/preflight-result.json
EXIT=0
```

## Step 4 — positive fake-live qualification

```
$ python3 .../qualify_text.py --fake-live --authorisation <valid> --out <path>
fake-live: 2304 recorded dispatches, 0 network calls
  openai:FAKE-LIVE-openai-snapshot   devanagari= 576 latin= 576 scope=['devanagari', 'latin']
  google:FAKE-LIVE-google-snapshot   devanagari= 576 latin= 576 scope=['devanagari', 'latin']
external calls: 0   spend USD: 0
written: /tmp/w-qual.json
EXIT=0
```

## Step 5 — positive fake-live A-TEXT

```
$ python3 .../run_atex.py --fake-live --authorisation <valid> --out <path>
fake-live: 16 generations ({'IMG-01': 8, 'IMG-02': 8}), 16 evaluator dispatches, 0 network calls
exact matches: 16/16  (perfect reader — not evidence about any model)
synthetic: False   registry rows: 0
external calls: 0   spend USD: 0
written: /tmp/w-atex.json
EXIT=0
```

## Step 6 — cross-process budget / handoff rehearsal

The control this task exists for. Real `subprocess` interpreters: qualification runs and exits,
and A-TEXT is a fresh process that knows only what is on disk.

```
$ python3 eval/empirical-tranche-1/rehearse_cross_process.py
EMP-001 cross-process rehearsal — fake-live, zero network, zero spend

[1] create a valid fake authorisation
    /var/folders/1h/9tpkt7s175x90vf_38376zbr0000gn/T/tmpzbu06i7q/authorization.local.yaml

[2] initialise the persistent run and spend state
    run rehearsal-run  ledger runs/rehearsal-run/spend-ledger.jsonl

[3] PROCESS A — fake-live qualification (separate interpreter)
    fake-live: 2304 recorded dispatches, 0 network calls

[4] PROCESS A exits — reopen the budget from disk only
    qualification spend reconstructed from the ledger: USD 0.9763200
    tranche total so far:                              USD 0.9763200

[5] the persisted qualification handoff
    qualified candidates: ['openai:FAKE-LIVE-openai-snapshot', 'google:FAKE-LIVE-google-snapshot']
    fingerprint: b8cf6bcf60a2862563bda5fd310b4f92…

[6] PROCESS B — A-TEXT with the Latin perceptibility gate UNRESOLVED
    exit 2: REFUSED: GATE 2b CLOSED — the Latin human perceptibility review is unresolved. Two of the four froze

[7] PROCESS C — A-TEXT with a REHEARSAL-ONLY perceptibility fixture
    fake_live: 16 generations {'IMG-01': 8, 'IMG-02': 8}, 16 evaluator dispatches, retries 0
    tranche spent USD 1.8905680 (qualification 0.9763200, atex 0.9142480)
    synthetic: False   registry rows: 0
    written: /var/folders/1h/9tpkt7s175x90vf_38376zbr0000gn/T/tmpzbu06i7q/atex.json

[8] verify the invariants against the reconstructed ledger
    [PASS] cumulative_spend_did_not_reset
    [PASS] total_within_10
    [PASS] qualification_within_6
    [PASS] retries_zero
    [PASS] generations_sixteen
    [PASS] per_route_eight_each
    [PASS] cost_refs_unique
    [PASS] trial_ids_unique
    [PASS] generation_and_evaluator_costed_separately
    [PASS] atex_not_synthetic
    [PASS] registry_rows_written
    [PASS] not_promotable

    qualification USD 0.9763200  +  A-TEXT USD 0.9142480  =  USD 1.8905680 of 10.00
    spend records 2336, all cost refs unique: True

RESULT: PASS   external calls 0   spend USD 0
EXIT=0
```

Read the numbers rather than the PASS lines:

- qualification spent **USD 0.9763200** in process A and, after that process exited, process B
  reconstructed exactly that from the ledger — **not** a fresh USD 10;
- A-TEXT then spent **USD 0.9142480** against the remaining headroom;
- cumulative **USD 1.8905680** of 10.00, with qualification inside its 6.00 sub-cap;
- **2,336** spend records — 2,304 qualification dispatches + 16 generations + 16 evaluator calls
  — every cost reference and trial id unique;
- step 6 of the rehearsal ran A-TEXT against the **committed, unfilled** perceptibility sheet and
  was **refused**. The gate is demonstrated closed before it is demonstrated open.

## Step 7 — protected baselines, byte for byte

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

Zero empirical rows, before and after every run above including the full cross-process rehearsal.

### The committed perceptibility sheet is still unfilled

```
$ python3 -c "import csv; rows=list(csv.DictReader(open('.../perceptibility-review.csv'))); \
print(len(rows), sum(1 for r in rows if r['visible_difference'] or r['usable_surface']))"
96 rows; 0 filled verdicts
```

A test asserts this, so a rehearsal fixture can never leak back into the repository.

### No key material in committed code

```
$ grep -rInE "sk-[A-Za-z0-9]{12,}|AIza[A-Za-z0-9_-]{20,}" eval/empirical-tranche-1/
(no matches)
```

### Runtime spend state is not committed

```
$ git status --porcelain | grep -c 'eval/runs'
0
```

`eval/runs/` is gitignored: it is machine-local runtime state about money.

---

## What EVAL-014 changed

| Blocker | Correction |
|---|---|
| **B6** tranche spend not cumulative across processes | durable ledger keyed by RUN id, reconstructed from disk on every read |
| **B7** USD 6 evaluator sub-cap not enforced | stage caps enforced in one place; qualification refused at 6.00 even when the authorisation names 10.00 |
| **B8** A-TEXT paid CLI still refused | fingerprint-bound qualification handoff; `--live` and `--fake-live` share one code path |
| **B9** evaluator calls lacked durable trial/cost identity | deterministic trial id + ledger-resolvable cost_ref on every dispatch |
| **B10** A-TEXT blind check not target-aware | `blind_check_target` passed evaluator-side only; Devanagari and Latin leak controls |

## Deviations and honesty notes

- **The human perceptibility review is still NOT performed and NOT fabricated.** The rehearsal's
  filled sheet is written to a temporary directory, is labelled `REHEARSAL FIXTURE - NOT A HUMAN
  REVIEW`, and never enters the repository.
- **The fake-live reader is perfect.** `16/16 exact matches` is a property of the fake. It says
  nothing about IMG-01, IMG-02 or either judge candidate.
- **The live transports remain unproven against real providers.** Their URLs, headers and bodies
  are asserted against documented contracts, not observed responses.
- Carried forward: hyphenated package directory with `tests/conftest.py`; `shasum -a 256` in place
  of `sha256sum`; pytest/PyYAML in a throwaway virtualenv outside the repository.
- No provider, model or evaluator was contacted. No account was funded and no terms accepted.
