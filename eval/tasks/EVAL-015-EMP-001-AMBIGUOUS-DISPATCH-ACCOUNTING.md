# EVAL-015 — EMP-001 Ambiguous Dispatch Accounting Correction

**AUTONOMY:** autonomous  
**EXTERNAL SPEND:** **USD 0 / INR 0**  
**PROVIDER / MODEL / EVALUATOR CALLS:** **0**  
**BRANCH:** `work/eval-015-emp-001-ambiguous-dispatch`

## Objective

Close only the remaining paid-execution defect identified in:

`coordination/decisions/CONTROLLER-EVAL-014-REVIEW-2026-08-27.md`

Preserve all valid EVAL-012/EVAL-013/EVAL-014 implementation. This is not a research, architecture, pricing or experiment-design task.

The required end state is:

> a provider call that is definitely not dispatched may release its reservation; a call whose dispatch/billing state is ambiguous must remain conservatively counted and persist as one failed/timeout trial, so no transport exception can manufacture spend headroom or erase an attempted call.

## Fixed Controller decisions — do not reopen

- EMP-001 total consumed-API ceiling: **USD 10.00**.
- qualification sub-cap: **USD 6.00**.
- retries: **0**.
- no account pre-funding above approved ceiling.
- scientific roster, candidates, thresholds, prompts, routes and A-TEXT items unchanged.
- A-TEXT remains 16 image generations maximum.
- Latin human perceptibility review remains an outstanding human prerequisite.
- Registry remains empirical-only.
- no external call is authorised by this task.

## Required corrections

### E15-A — distinguish proven pre-dispatch failure from ambiguous post-dispatch failure

Do not catch every transport exception and call `release()`.

Implement explicit failure semantics so that:

1. **Provably pre-dispatch failures** may release the reservation. Examples:
   - missing API key discovered before any socket/request send;
   - request validation / blindness refusal before network dispatch;
   - route/body construction refusal before network dispatch.

2. **Ambiguous dispatch failures** must NOT release the reservation. Examples:
   - connect/read timeout once the HTTP dispatch path was entered;
   - connection reset / remote disconnect;
   - TLS/network error where it cannot be proven the provider received nothing;
   - malformed/unparseable provider response after a request was sent.

For ambiguous failures:
- persist one trial with `api_status` = `timeout` or `error` and an explicit error class;
- persist provider/model/route identity and trial/attempt identity;
- retries remain 0;
- preserve a conservative cost reference in the persistent tranche ledger;
- mark billing state as unknown/provisional when actual provider billing is unavailable;
- do not manufacture headroom;
- stop execution rather than retry automatically.

### E15-B — evaluator path

Correct `TextJudge._dispatch()` / transports so an ambiguous evaluator failure cannot disappear or free budget.

Required controls:
- missing key / explicit pre-dispatch refusal => 0 network dispatch, reservation safely released or never created;
- injected timeout after dispatch boundary => reservation remains conservatively counted/settled, one trial persisted, 0 retries;
- injected connection-reset / malformed-response case => same conservative behavior;
- reopening the run sees the ambiguous call cost/history and cannot reclaim the headroom;
- provider request id may be null when unavailable, but trial/cost identity must still exist.

### E15-C — fal generation path

Correct A-TEXT generation so an ambiguous fal transport failure:
- creates/persists the generation Attempt/trial;
- carries `api_status` timeout/error and an explicit error class;
- carries a cost_ref resolving to the persistent ledger;
- keeps conservative spend counted;
- causes no evaluator call because no usable artifact exists;
- causes no automatic retry;
- stops/fails closed after the ambiguous call rather than continuing as if nothing happened.

A provably pre-dispatch fal refusal may release/avoid the reservation.

### E15-D — no-regression controls

Freshly prove:
- EVAL-014 cumulative USD 10 / USD 6 controls still pass;
- full positive fake-live qualification still passes;
- full positive fake-live A-TEXT still passes;
- cross-process rehearsal still passes;
- Latin perceptibility gate remains closed in the committed repo;
- Registry remains unchanged;
- protected baselines remain byte-identical;
- zero real network/provider/model/evaluator calls and zero spend.

## Verification before return

Run and record:
- all `eval/empirical-tranche-1/tests/`;
- V1 harness self-test;
- Resources cross-branch validation;
- dry-run preflight;
- full positive fake-live qualification;
- positive fake-live A-TEXT;
- cross-process budget/handoff rehearsal;
- new evaluator ambiguous-dispatch controls;
- new generation ambiguous-dispatch controls;
- Registry zero check;
- protected baseline SHA check.

## Required return

Create:

`eval/empirical-tranche-1/EVAL-015-AMBIGUOUS-DISPATCH-READINESS.md`

Return exactly:
1. verdict: `READY_FOR_SPEND_APPROVAL | BLOCKED`;
2. final pushed commit SHA;
3. exact tests/commands and results;
4. evaluator ambiguous-dispatch accounting evidence;
5. generation ambiguous-dispatch accounting evidence;
6. remaining non-code prerequisites, including Latin human perceptibility review, secrets and exact version pins;
7. confirmation external calls = 0 and spend = 0.

Commit and push to the assigned branch. Do not merge.
