# Controller State

**Updated:** 27 Aug 2026 — EVAL-013 reviewed BLOCKED; bounded EVAL-014 budget-continuity / paid-handoff correction active. Paid calls remain blocked.

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

## EVAL-013 review

Returned branch:
- `work/eval-013-emp-001-live-path-correction` @ `2b83efd15c1f0fb26d6e7ca8bfbe542071abf577`

Worker verdict:
- `READY_FOR_SPEND_APPROVAL`

Controller verdict:
- **BLOCKED — preserve EVAL-013; correct only cumulative budget continuity and the paid stage handoff.**

Authoritative review:
- `coordination/decisions/CONTROLLER-EVAL-013-REVIEW-2026-08-27.md`

Accepted EVAL-013 work:
- real qualification orchestration behind injectable transports;
- provider-correct OpenAI/Gemini auth paths;
- frozen fal IMG-01 / IMG-02 route adapters;
- non-dry-run A-TEXT now uses a supplied qualified judge rather than `_fake_transcribe`;
- positive fake-live controls;
- live blind-check enforcement and UTF-8 payload inspection;
- worker-reported 247 EMP-001 tests green, V1 107/107 green, Resources validation PASS, Registry zero, protected baselines intact, zero external calls/spend.

Controller independently checked current official fal documentation and confirmed the implemented `FAL_KEY` / `Authorization: Key <key>` convention.

Blocking defects remaining:
1. **Budget reset across processes:** `BudgetGuard.spent_usd` is process-local, so qualification and A-TEXT could each reopen the USD 10 authorisation from zero.
2. **USD 6 qualification sub-cap not enforced:** live qualification currently uses the general USD 10 authorisation ceiling.
3. **Paid A-TEXT CLI handoff still refuses:** `run_atex.py --live` has no executable handoff from the real qualification result to the same pinned judge + frozen fal routes.
4. **Evaluator call identity:** live qualification needs durable unique trial ids and cost references, not only `one_call_one_trial: true` assertions.
5. **A-TEXT blind defense:** primary live transcription should pass the target only to the evaluator-side `blind_check_target` check, including Latin targets.

These are implementation/spend-control defects only. Scientific scope is not reopened.

## Active assignment — EVAL-014

Task:
- `eval/tasks/EVAL-014-EMP-001-BUDGET-CONTINUITY-HANDOFF.md`

Branch:
- `work/eval-014-emp-001-budget-continuity`

Base:
- EVAL-013 returned head `2b83efd15c1f0fb26d6e7ca8bfbe542071abf577`

External spend/calls:
- **USD 0 / INR 0**;
- **0 provider/model/evaluator calls**.

EVAL-014 may only:
- persist cumulative EMP-001 spend across separate processes/stages;
- enforce both USD 10 total and USD 6 qualification sub-cap;
- implement the real qualification → A-TEXT CLI/orchestrator handoff;
- give every evaluator call durable unique trial/cost identity;
- apply target-aware blind pre-dispatch checking in A-TEXT;
- prove the lifecycle with injected fake transports and zero network.

No model, prompt, threshold, route, repeat, retry, A-TEXT item or budget may change.

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

The Latin human perceptibility review remains unfilled and is a zero-spend prerequisite for the Latin qualification leg. It must not be fabricated.

## Still blocked / not authorised

Not authorised:
- any paid EMP-001 call;
- EMP-001 USD 10 tranche until EVAL-014 returns clean and the user explicitly approves;
- any account funding;
- full 90-generation Stage A;
- Stage B / Stage C;
- EVAL-006;
- Registry population from unqualified instruments;
- broad controlled-pack acquisition;
- Production IR/Planner implementation.

Customer-outcome CpAO remains Stage C only.

## Next gate

EVAL-014 returns first.

If it is genuinely `READY_FOR_SPEND_APPROVAL`, Controller will re-review cumulative budget persistence, the USD 6 sub-cap, and the real qualification → A-TEXT handoff before asking the user for any spend approval.
