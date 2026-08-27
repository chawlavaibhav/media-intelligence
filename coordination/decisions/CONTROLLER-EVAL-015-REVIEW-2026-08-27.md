# Controller Review — EVAL-015 Ambiguous Dispatch Accounting

**Date:** 27 Aug 2026  
**Worker branch:** `work/eval-015-emp-001-ambiguous-dispatch`  
**Returned head:** `b98789673a90fac350609eed5730ff6483e7e6bf`  
**Integration PR:** #36  
**Integration merge commit:** `bf17fe2db3a3712753fbf5bdf8db28e682f1b1b1`

## Controller verdict

**ACCEPTED FOR INTEGRATION — NOT SPEND APPROVAL.**

EVAL-015 closes the bounded ambiguous-dispatch accounting defects identified in the EVAL-014 review. The accepted EVAL-012→015 execution implementation is now integrated into `main`.

No external provider/model/evaluator call was authorised or made by this Controller review.

## What was reviewed

The Controller inspected the pushed EVAL-015 diff and the live branch contents, with emphasis on the exact failure modes named in the assignment:

- evaluator timeout / socket timeout;
- connection reset / remote disconnect;
- TLS / network ambiguity;
- malformed provider response after send;
- fal generation ambiguity;
- persistence of failed evaluator and generation trials;
- conservative budget accounting after reopen;
- zero retries and fail-closed stop behaviour;
- preservation of EVAL-014 cumulative budget continuity.

The worker readiness record reports:
- 363 EMP-001 tests passing;
- V1 harness 107/107;
- Resources cross-branch validation PASS;
- fake-live qualification 2,304 dispatches;
- fake-live A-TEXT 16 generations + 16 evaluator calls;
- cross-process cumulative rehearsal USD 1.8905680;
- Registry rows 0;
- 13/13 protected baselines byte-identical;
- 0 external calls and USD 0 spend.

These test counts are worker evidence. The Controller independently reviewed the code/diff and integration shape; this review did not rerun provider calls.

## Accepted failure semantics

### 1. Provably pre-dispatch failures

A reservation may be released or avoided only when the code can prove that no provider request was sent.

Examples now represented explicitly include:
- missing runtime key before dispatch;
- blind/request refusal before dispatch;
- model/body refusal before dispatch.

### 2. Ambiguous post-dispatch failures

Once the dispatch boundary is entered, timeout/reset/disconnect/TLS/network failures are not treated as proof that the provider received nothing.

The accepted implementation:
- does not release the reservation;
- conservatively settles at the reserved estimate when actual billing is unavailable;
- marks `billing_state: unknown_provisional`;
- persists provider/model/route plus trial/attempt identity and `cost_ref`;
- records timeout/error status and explicit error class;
- retries 0 times;
- stops fail-closed.

Malformed/unparseable responses after send follow the same conservative rule.

## Evaluator path

`TextJudge._dispatch()` now distinguishes `PreDispatchRefusal` from `AmbiguousDispatch`.

For an ambiguous evaluator call, the judge returns a persistable failed response carrying:
- timeout/error status;
- explicit error class;
- unknown/provisional billing state;
- conservative reserved estimate;
- no fabricated provider request id;
- durable call/trial identity through the call record.

Qualification persists that record and stops immediately on the first ambiguous dispatch. The Latin leg is not entered after such a stop.

## Generation path

The fal route now has the same dispatch boundary.

For an ambiguous generation call, A-TEXT:
- keeps the generation spend counted;
- persists the generation Attempt/trial before stopping;
- preserves route/slot/provider-surface identity and `cost_ref`;
- marks timeout/error and unknown/provisional billing;
- performs no evaluator call because there is no usable artifact;
- performs no retry;
- stops the remaining paid screen.

An ambiguous evaluator call after a successful generation also stops the screen while preserving both trials.

## Budget continuity preserved

The persistent tranche ledger still counts outstanding reservations, settles them against the same cost reference, and survives process reopen.

The frozen controls remain:
- EMP-001 total ceiling: USD 10.00;
- qualification sub-cap: USD 6.00;
- retries: 0;
- no pre-funding above an approved ceiling.

## What this does not establish

Nothing empirical has yet been learned about real model quality.

Still true:
- 0 qualified models/workflows;
- 0 qualified subjective/perceptual evaluators;
- 0 empirical Capability Registry rows;
- 0 accepted evidence Canon improves outputs.

The live provider success paths remain unobserved until an authorised real call occurs.

## Remaining gates before any spend decision

1. Latin human perceptibility review is still unfilled and must not be fabricated.
2. Runtime secrets must exist only at execution.
3. Exact OpenAI/Google model versions must be pinned at execution.
4. Current route/model availability and planning prices must be re-verified before approval.
5. Gitignored generated image sets must be rebuilt before execution.
6. The user must explicitly approve the bounded EMP-001 ceiling before any paid call.

## Controller disposition

EVAL-015 is closed as an implementation correction and its code is integrated.

The project now moves to **zero-spend pre-execution prerequisites only**. Paid EMP-001 execution remains blocked.
