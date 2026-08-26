# Controller State

**Updated:** 27 Aug 2026 — EVAL-014 reviewed BLOCKED on one ambiguous-dispatch accounting defect; bounded EVAL-015 active. Paid calls remain blocked.

**Read `PROJECT-MEMORY.md` first.** Where older task/handoff wording conflicts with this file and the latest durable Controller decisions, the latest Controller decision governs.

## Global posture

Broad research/design and the final pre-execution freeze are closed. The project remains in first empirical tranche implementation.

Frozen foundations remain:
- CANON-010 request contract;
- Capability Contract v2: **44 = 43 active + 1 dormant**;
- 13 condition families;
- 12 core + 2 reserve scientific question slots;
- Resources topology v3 / CpAO v3 / four controlled-pack families;
- EVAL-011 staged design: Q=0 model generations, A=90, B≤404 additional, C=32 outcome attempts;
- GOV-004 **PASS WITH NON-BLOCKING NOTES**.

There is no active broad research task.

## Current empirical floor

Still true:
- **0 qualified models/workflows**;
- **0 qualified subjective/perceptual evaluator families**;
- **0 current empirical Capability Registry rows**;
- **0 accepted evidence that Canon improves model outcomes**;
- no Production IR/Planner exists.

## EMP-001 — prepared, NOT authorised

Frozen paid shape remains:
1. qualify text judges progressively: Devanagari first, Latin only for survivors;
2. only with a judge qualified on all required scripts, run A-TEXT;
3. four frozen items × two repeats × two routes = **16 image generations maximum**.

Proposed spend remains:
- total consumed-API ceiling **USD 10.00** / approximately ₹954 planning reference, excluding taxes;
- qualification sub-cap **USD 6.00** inside that total;
- retries **0**;
- no account pre-funding above the approved ceiling.

No part of that spend is approved yet.

## EVAL-014 review

Returned branch:
- `work/eval-014-emp-001-budget-continuity` @ `094c24a77737b17067a3e98834c00e3bf2e1fa53`

Worker verdict:
- `READY_FOR_SPEND_APPROVAL`

Controller verdict:
- **BLOCKED — preserve EVAL-014; correct only ambiguous provider-dispatch exception accounting.**

Authoritative review:
- `coordination/decisions/CONTROLLER-EVAL-014-REVIEW-2026-08-27.md`

Accepted EVAL-014 work:
- durable run ledger carrying spend across separate processes;
- USD 10 total ceiling and USD 6 qualification sub-cap mechanically enforced;
- fingerprint-bound qualification → A-TEXT handoff;
- deterministic evaluator trial/attempt ids and ledger-resolvable cost refs;
- target-aware blind check parity in A-TEXT;
- Latin perceptibility review correctly gates the whole four-item A-TEXT screen;
- worker-reported 315 EMP-001 tests green, V1 107/107 green, Resources validation PASS, Registry zero, protected baselines intact, zero external calls/spend;
- worker-reported full cross-process rehearsal: qualification USD 0.9763200 persisted across process exit, then A-TEXT USD 0.9142480, cumulative USD 1.8905680 of USD 10.

Blocking defect remaining:
1. **Ambiguous evaluator transport exception:** after reserving budget, `TextJudge._dispatch()` releases the reservation on any transport exception. A timeout/reset can happen after the provider received the request, so releasing can manufacture headroom and erase a potentially billed trial.
2. **Ambiguous generation transport exception:** A-TEXT currently exits on a fal transport exception before persisting the generation Attempt/trial. The pending reservation is conservative for spend but the failure/timeout attempt is not durable evidence.

Frozen policy: a reservation may be released only when no provider dispatch can be proven. Ambiguous post-dispatch failures must persist as timeout/error/unknown-billing trials, remain conservatively costed, and receive no automatic retry.

## Active assignment — EVAL-015

Task:
- `eval/tasks/EVAL-015-EMP-001-AMBIGUOUS-DISPATCH-ACCOUNTING.md`

Branch:
- `work/eval-015-emp-001-ambiguous-dispatch`

Base:
- EVAL-014 returned head `094c24a77737b17067a3e98834c00e3bf2e1fa53`

External spend/calls:
- **USD 0 / INR 0**;
- **0 provider/model/evaluator calls**.

EVAL-015 may only:
- distinguish provably pre-dispatch failures from ambiguous post-dispatch failures;
- prevent ambiguous evaluator failures from releasing spend headroom;
- persist ambiguous evaluator and generation failures as one-call-one-trial evidence with cost refs;
- keep retries at 0 and stop fail-closed;
- prove the correction with injected fake transports and rerun EVAL-014 regressions.

No model, prompt, threshold, route, repeat, retry, A-TEXT item, budget, Latin prerequisite or scientific decision may change.

## Measurement freeze unchanged

Text qualification:
- Devanagari validated view: 96 items;
- Latin pack: 96 items = 48 match + 48 controlled mismatch;
- 3 repeats per shape;
- shapes: `transcribe`, `verdict`;
- candidates: OpenAI `gpt-5.4-mini` and Google `gemini-3.5-flash-lite`, exact versions pinned at execution;
- maximum 2,304 evaluator calls if both reach both scripts;
- Devanagari failure stops that candidate before Latin.

A-TEXT strings remain exactly:
- `शुभ दीपावली`
- `आज की डील`
- `Aaj ki Deal`
- `SAVE 20% • ₹999`

Routes remain:
- IMG-01: fal `openai/gpt-image-2`, 8 unseeded generations;
- IMG-02: fal `fal-ai/ideogram/v3`, BALANCED, 8 unseeded generations.

Primary exactness remains blind transcription followed by code-level comparison. A-TEXT remains partial evidence only.

The Latin human perceptibility review remains unfilled and is a zero-spend prerequisite for the Latin qualification leg and therefore for the complete four-item A-TEXT screen. It must not be fabricated.

## Still blocked / not authorised

Not authorised:
- any paid EMP-001 call;
- EMP-001 USD 10 tranche until EVAL-015 returns clean and the user explicitly approves;
- any account funding;
- full 90-generation Stage A;
- Stage B / Stage C;
- EVAL-006;
- Registry population from unqualified instruments;
- broad controlled-pack acquisition;
- Production IR/Planner implementation.

Customer-outcome CpAO remains Stage C only.

## Next gate

EVAL-015 returns first.

If it is genuinely `READY_FOR_SPEND_APPROVAL`, Controller will re-review ambiguous failure accounting plus the already-accepted EVAL-014 budget/handoff controls before asking the user for any spend approval.
