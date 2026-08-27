# EMP-001 pre-spend verification record

**Date:** 27 Aug 2026
**Branch:** `work/eval-015-emp-001-ambiguous-dispatch`
**Supersedes:** the EVAL-014 record
**External calls made producing this record: 0. Spend: USD 0 / INR 0.**

Copied from fresh runs in this branch. Environment: macOS (Darwin 23.6.0), Python 3.14.6,
pytest 9.1.1, PyYAML 6.0.3 in a throwaway virtualenv outside the repository. No API key was used;
every key in every run is the literal string `REHEARSAL-NOT-A-REAL-KEY`.

---

## Step 1 — all EMP-001 tests

```
$ python3 -m pytest -q eval/empirical-tranche-1/tests
...                                                                      [100%]
363 passed in 24.61s
EXIT=0
```

Up from 315 at the EVAL-014 head; 48 new ambiguous-dispatch controls.

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
written: /Users/vaibhavchawla/Vaibhav_Personal_Projects/media-intelligence-worktrees/eval-015/eval/empirical-tranche-1/preflight-result.json
EXIT=0
```

## Step 4 — no-regression: positive fake-live paths

```
$ python3 .../qualify_text.py --fake-live --authorisation <valid> --out <path>
fake-live: 2304 recorded dispatches, 0 network calls
  openai:FAKE-LIVE-openai-snapshot   devanagari= 576 latin= 576 scope=['devanagari', 'latin']
  google:FAKE-LIVE-google-snapshot   devanagari= 576 latin= 576 scope=['devanagari', 'latin']
external calls: 0   spend USD: 0
written: /tmp/x-qual.json
EXIT=0
```

```
$ python3 .../run_atex.py --fake-live --authorisation <valid> --out <path>
fake-live: 16 generations ({'IMG-01': 8, 'IMG-02': 8}), 16 evaluator dispatches, 0 network calls
exact matches: 16/16  (perfect reader — not evidence about any model)
synthetic: False   registry rows: 0
external calls: 0   spend USD: 0
written: /tmp/x-atex.json
EXIT=0
```

## Step 5 — no-regression: cross-process budget / handoff rehearsal

```
$ python3 eval/empirical-tranche-1/rehearse_cross_process.py
    tranche spent USD 1.8905680 (qualification 0.9763200, atex 0.9142480)
    synthetic: False   registry rows: 0
    written: /var/folders/1h/9tpkt7s175x90vf_38376zbr0000gn/T/tmpick3zo92/atex.json

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

Unchanged from EVAL-014: qualification spend survives a process exit, both ceilings hold, 2,336
spend records all uniquely referenced.

## Step 6 — new ambiguous-dispatch controls

```
$ python3 -m pytest -q .../test_ambiguous_dispatch.py .../test_ambiguous_generation.py
................................................                         [100%]
48 passed in 0.19s
EXIT=0
```

Six ambiguous failure modes are injected on both paths — read timeout, socket timeout, connection
reset, remote disconnect, TLS failure, connection abort — plus a malformed post-send response.

## Step 7 — EVAL-014 budget and handoff regressions

```
$ python3 -m pytest -q .../test_spend_ledger.py .../test_trial_identity.py \
      .../test_cross_process_rehearsal.py .../test_atex_handoff.py
....................................................................     [100%]
68 passed in 24.28s
EXIT=0
```

## Step 8 — protected baselines, Registry, Latin gate

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

```
$ grep -v '^#' eval/registry/registry-v1.jsonl | grep -c '[^[:space:]]'
0
```

```
$ python3 -c "import run_atex as R; print(R.latin_perceptibility_resolved())"
False
```

The Latin human perceptibility gate remains **closed** in the committed repository, as it must.

### No key material in committed code

```
$ grep -rInE "sk-[A-Za-z0-9]{12,}|AIza[A-Za-z0-9_-]{20,}" eval/empirical-tranche-1/
(no matches)
```

---

## What EVAL-015 changed

One rule, applied to both provider paths:

> **Release only when it is PROVABLE nothing was sent. Otherwise keep the money counted and keep
> the trial.**

`PreDispatchRefusal` marks the provable cases — missing key, refused body construction, blindness
violation — and releases. Every failure after the send boundary raises `AmbiguousDispatch`, which
settles at the reserved estimate, marks `billing_state: unknown_provisional`, persists one trial
with full identity and a resolvable ledger `cost_ref`, and stops the run. Retries remain 0.

An unparseable response after the send is ambiguous too: the request was sent, and a gibberish
reply does not make the call free.

## Honesty notes, carried forward

- The **Latin human perceptibility review is still not performed and not fabricated.** It gates
  the whole A-TEXT screen, because two of the four frozen items are Latin.
- The **fake-live readers are perfect.** `16/16 exact matches` is a property of the fake and says
  nothing about IMG-01, IMG-02 or either judge candidate.
- The **live transports remain unproven against real providers.** EVAL-015 makes their *failure*
  accounting correct; it does not make their success path observed. The first authorised call is
  still their first real test.
- No provider, model or evaluator was contacted. No account funded, no terms accepted.
