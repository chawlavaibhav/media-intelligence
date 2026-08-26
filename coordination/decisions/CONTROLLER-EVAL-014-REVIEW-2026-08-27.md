# Controller Review — EVAL-014 EMP-001 budget continuity and paid handoff

**Date:** 27 Aug 2026  
**Returned branch:** `work/eval-014-emp-001-budget-continuity`  
**Returned head:** `094c24a77737b17067a3e98834c00e3bf2e1fa53`  
**Worker verdict:** `READY_FOR_SPEND_APPROVAL`  
**Controller verdict:** **BLOCKED — one bounded ambiguous-dispatch accounting correction only**

## Accepted EVAL-014 work

The Controller accepts the EVAL-014 implementation and worker evidence for the task's intended B6–B10 corrections:

1. **Persistent cumulative budget:** spend is now reconstructed from a durable run ledger across separate processes instead of resetting with a new in-memory guard.
2. **Frozen caps:** the USD 10 EMP-001 total ceiling and USD 6 qualification sub-cap are mechanically enforced.
3. **Paid handoff:** persisted qualification evidence is fingerprint-bound to its call records and the A-TEXT handoff reconstructs the same provider / alias / resolved version.
4. **Durable call identity:** evaluator dispatches carry deterministic trial/attempt identity and ledger cost references.
5. **Blindness parity:** A-TEXT uses the target only as evaluator-side `blind_check_target` and the Latin gate is explicit.
6. **Cross-process rehearsal:** worker-reported fresh evidence shows qualification spend surviving process exit and A-TEXT consuming the remaining tranche headroom.
7. **Latin prerequisite:** the unfilled human perceptibility review correctly gates the whole four-item A-TEXT screen because two frozen items are Latin.

Worker-reported fresh verification, accepted as worker evidence rather than an independent Controller rerun:
- 315 EMP-001 tests passed;
- V1 harness 107/107 passed;
- Resources cross-branch validation passed;
- positive fake-live qualification traversed 2,304 dispatches;
- positive fake-live A-TEXT traversed 16 generations + 16 evaluator calls;
- cross-process rehearsal passed at zero network / zero spend;
- Registry remained empty;
- protected baselines remained byte-identical;
- no real provider/model/evaluator call was made.

The Controller directly inspected `spend_ledger.py`, `providers.py`, `qualify_text.py`, `run_atex.py`, the readiness record and the verification record.

## Why READY_FOR_SPEND_APPROVAL is still rejected

### B11 — an ambiguous evaluator transport exception can manufacture headroom

`TextJudge._dispatch()` currently reserves budget, calls the transport, and on **any** exception executes `guard.release()` before re-raising.

That logic assumes every transport exception proves the provider call never happened. It does not.

A missing key, local request-build refusal, or other provably pre-dispatch failure can safely release a reservation. But a socket timeout, connection reset, TLS/read failure, or similar network exception can occur **after the provider received the request**. The provider may bill that attempt even though no response reached us.

Releasing the reservation in that ambiguous case causes two contract violations:
- the persistent ledger may say the call cost USD 0 even though the provider may have billed it, weakening the user-approved USD 10 hard ceiling;
- the attempted call disappears from empirical evidence instead of persisting as a timeout/error with one-call-one-trial identity.

This conflicts with the already-frozen rule that failures/refusals/timeouts persist and with the purpose of EVAL-014's cumulative spend control.

### B12 — generation transport exceptions also need an explicit ambiguous-dispatch record

A-TEXT reserves generation spend and then calls the fal route. If the route raises, the current runner exits before creating the Attempt/cost evidence. The reservation remains pending, which is fail-closed for budget, but the provider attempt itself is not persisted as a timeout/error trial.

The safe behavior for an ambiguous post-dispatch failure is conservative:
- do not manufacture headroom;
- persist the trial as timeout/error/unknown-billing-state;
- keep a conservative cost reservation/charge until provider billing can be reconciled;
- stop the tranche rather than retry automatically;
- retries remain 0.

A reservation may be released only when the code can prove no provider request was dispatched.

## Controller disposition

Do **not** merge EVAL-014 as spend-ready and do **not** request user spend approval yet.

Preserve all EVAL-014 work and open exactly one correction lane, **EVAL-015**, based on returned head `094c24a77737b17067a3e98834c00e3bf2e1fa53`.

EVAL-015 may only correct provider-dispatch exception accounting for evaluator and generation calls and prove it with injected transports. No model, prompt, route, threshold, item, repeat count, budget, qualification rule, Latin gate or scientific decision may change.

## Spend posture

Still **not authorised**:
- any provider/model/evaluator call;
- any account funding;
- EMP-001 USD 10 spend;
- full Stage A or later stages.

External spend authorised for EVAL-015: **USD 0 / INR 0**.
