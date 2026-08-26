# Controller State

**Updated:** 26 Aug 2026 — EVAL-012 reviewed BLOCKED; bounded EVAL-013 live-path correction active. Paid calls remain blocked.

**Read `PROJECT-MEMORY.md` first.** Where older task/handoff wording or the GOV-004 snapshot conflicts with this file and the latest durable Controller decisions, the latest Controller decision governs.

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

## EMP-001 — prepared, NOT authorised for paid execution

Authoritative preparation:
- `coordination/decisions/CONTROLLER-FIRST-EMPIRICAL-TRANCHE-PREPARATION-2026-08-26.md`
- `coordination/plans/2026-08-26-FIRST-EMPIRICAL-TRANCHE-PROPOSAL.md`
- `docs/superpowers/plans/2026-08-26-first-empirical-tranche.md`

Frozen later paid shape remains:
1. qualify the text measurement path;
2. only if a judge qualifies on required scripts, run A-TEXT;
3. four frozen items × two repeats × two routes = **16 image generations maximum**.

Proposed ceiling remains **USD 10.00 / approximately ₹954 consumed API spend**, excluding taxes, no retries, no account pre-funding above the ceiling. It is **not approved**.

## EVAL-012 review

Returned branch:
- `work/eval-012-emp-001-zero-spend` @ `d092be097cbc143cb1a5ad51ea5dc819a9a57486`

Worker verdict:
- `READY_FOR_SPEND_APPROVAL`

Controller verdict:
- **BLOCKED — preserve the dry-run work, correct only the positive live path.**

Authoritative review:
- `coordination/decisions/CONTROLLER-EVAL-012-REVIEW-2026-08-26.md`

Accepted worker evidence includes:
- 162 EMP-001 tests reported green;
- V1 self-test 107/107 reported green;
- cross-branch Resources validation reported PASS;
- zero provider/model/evaluator calls and zero spend;
- Registry remained empty;
- 96-item Latin pack built separately;
- protected baselines reported byte-identical;
- dry-run paths and 16-generation ceiling exercised.

The Controller could not independently rerun the suite because the local Controller runtime cannot resolve GitHub. The Controller did inspect the returned code directly.

Blocking implementation defects:
1. `qualify_text.py --live` is not implemented; it unconditionally refuses after authorisation.
2. `run_atex.py --live` is not implemented and no route-specific fal generator adapter exists.
3. A-TEXT always uses the fake transcription helper and hard-codes real/dry-run results as synthetic.
4. No positive fake-live control proves valid authorisation can actually dispatch one call and persist non-synthetic evidence.
5. Gemini API-key transport semantics must use provider-correct authentication rather than the generic Bearer-key transport.

These are implementation defects only. Scientific scope, prices, candidate questions, thresholds and budgets are not reopened.

## Active assignment — EVAL-013

Task on the correction branch:
- `eval/tasks/EVAL-013-EMP-001-LIVE-PATH-CORRECTION.md`

Branch:
- `work/eval-013-emp-001-live-path-correction`

Base:
- EVAL-012 returned head `d092be097cbc143cb1a5ad51ea5dc819a9a57486`

External spend/calls:
- **USD 0 / INR 0**;
- **0 provider/model/evaluator calls**.

EVAL-013 must only:
- wire real qualification orchestration behind injected fake transports;
- make OpenAI/Gemini transport/auth provider-correct;
- implement frozen fal IMG-01/IMG-02 generation adapters behind fake transports;
- make non-dry-run A-TEXT use the qualified blind transcription judge and non-synthetic labeling;
- add positive fake-live controls;
- rerun the full zero-spend verification suite.

No real provider call is allowed in EVAL-013.

## Measurement freeze unchanged

Text qualification:
- Devanagari validated view: 96 items;
- Latin pack: 96 items = 48 match + 48 controlled mismatch;
- 3 repeats per shape;
- shapes: `transcribe`, `verdict`;
- proposed candidates: OpenAI `gpt-5.4-mini` and Google `gemini-3.5-flash-lite`, exact versions pinned at execution;
- max 2,304 evaluator calls if both reach both scripts;
- Devanagari failure stops that candidate before Latin;
- evaluator API consumption guard: USD 6.00 within the proposed tranche.

A-TEXT strings remain exactly:
- `शुभ दीपावली`
- `आज की डील`
- `Aaj ki Deal`
- `SAVE 20% • ₹999`

Future image routes remain:
- IMG-01: fal `openai/gpt-image-2`, 8 unseeded generations;
- IMG-02: fal `fal-ai/ideogram/v3`, BALANCED, 8 unseeded generations.

The Latin human perceptibility review remains unfilled and is a zero-spend prerequisite for the Latin qualification leg. It must not be fabricated.

## Still blocked / not authorised

Not authorised:
- any paid EMP-001 call;
- the USD 10 tranche until EVAL-013 returns clean and the user explicitly approves it;
- full 90-generation Stage A;
- Stage B / Stage C;
- EVAL-006;
- Registry population from unqualified instruments;
- broad controlled-pack acquisition;
- provider account funding above an explicitly approved ceiling;
- Production IR/Planner implementation.

Customer-outcome CpAO remains Stage C only.

## Next gate

EVAL-013 returns first.

- If `BLOCKED`, route only the exact defect.
- If genuinely `READY_FOR_SPEND_APPROVAL`, the Controller re-reviews the positive fake-live path and only then asks the user to approve or reject the bounded USD 10 EMP-001 spend.
