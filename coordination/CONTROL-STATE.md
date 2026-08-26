# Controller State

**Updated:** 26 Aug 2026 — EMP-001 first empirical tranche prepared; explicit spend approval is the next gate.

**Read `PROJECT-MEMORY.md` first.** Where older task/handoff wording or the GOV-004 snapshot conflicts with this file and the latest durable Controller decisions, the latest Controller decision governs.

## Global posture

**Broad research/design and the final pre-execution freeze are closed.** The repository is now in empirical execution preparation.

Merged/frozen foundations remain:
- CANON-010 request contract / coverage freeze;
- Capability Contract v2: **44 = 43 active + 1 dormant**;
- 13 condition families;
- 12 core + 2 reserve scientific question slots;
- Resources topology v3 / CpAO v3 / four controlled-pack families;
- EVAL-011 staged design: Q=0 model generations, A=90, B≤404 additional, C=32 outcome attempts;
- GOV-004 **PASS WITH NON-BLOCKING NOTES**.

Historical V1 36-capability contract, V1 100-item bank and the frozen Devanagari battery remain protected baselines.

There is **no active broad research task**.

## Current empirical floor

Still true at this state:
- **0 qualified models/workflows**;
- **0 qualified subjective/perceptual evaluator families**;
- **0 current empirical Capability Registry rows**;
- **0 accepted evidence that Canon improves model outcomes**;
- no Production IR/Planner exists.

The next work is designed to change the first three facts with bounded evidence, not more architecture.

## EMP-001 — prepared, NOT authorised

Authoritative zero-spend preparation decision:
- `coordination/decisions/CONTROLLER-FIRST-EMPIRICAL-TRANCHE-PREPARATION-2026-08-26.md`

Proposal:
- `coordination/plans/2026-08-26-FIRST-EMPIRICAL-TRANCHE-PROPOSAL.md`

Execution implementation plan:
- `docs/superpowers/plans/2026-08-26-first-empirical-tranche.md`

Current route/price refresh:
- `eval/empirical-planning/STAGE-A-ROUTE-PRICE-REFRESH-2026-08-26.yaml`

EMP-001 scope:
1. zero-spend deterministic/persistence preflight;
2. build a separate 96-item Latin exact-text qualification pack;
3. qualify two text-judge candidates progressively — Devanagari first, Latin only for survivors;
4. only if at least one text judge qualifies, run an **A-TEXT partial admission screen** on IMG-01 and IMG-02: 4 frozen items × 2 repeats × 2 routes = **16 image generations maximum**.

This is deliberately not the full 90-generation Stage A.

## EMP-001 measurement freeze

Text qualification:
- existing Devanagari validated view: 96 items, unchanged;
- new Latin pack: 96 items = 48 match + 48 controlled mismatch;
- repeats per input shape: **3**;
- shapes: `transcribe` and `verdict`, kept separate;
- judge candidates:
  - OpenAI `gpt-5.4-mini`, exact snapshot pinned at execution;
  - Google `gemini-3.5-flash-lite`, exact version pinned at execution;
- maximum if both candidates reach both scripts: **2,304 evaluator calls**;
- Devanagari failure stops that candidate before Latin;
- proposed evaluator API consumption guard: **USD 6.00**.

Provisional first-run instrument gate:
- mismatch false passes: 0 allowed;
- clean-match false-fail rate ≤10%;
- refusal ≤5%, separate;
- repeat consistency ≥0.95 across three full passes in both shapes.

These are bounded first-run gates, not empirically validated universal thresholds. Generated malformed-glyph recognition remains outside qualified scope.

A-TEXT frozen targets:
- `शुभ दीपावली`
- `आज की डील`
- `Aaj ki Deal`
- `SAVE 20% • ₹999`

Routes:
- IMG-01: `gpt-image-2` via fal `openai/gpt-image-2`, 8 unseeded generations;
- IMG-02: Ideogram V3 via fal `fal-ai/ideogram/v3`, BALANCED, 8 unseeded generations.

Primary exactness measurement is blind transcription followed by code-level comparison. A target-visible verdict may be diagnostic but cannot override a primary mismatch.

A-TEXT is **partial evidence only**. It may stop deeper text-specific spend for a route that records zero exact matches across the frozen Devanagari/Hinglish opportunities, but no route can become a complete Stage-A survivor from this tranche alone.

## Proposed EMP-001 spend boundary

**Not yet approved:** maximum **USD 10.00 consumed API spend**, approximately **₹954** at the planning reference rate of 95.4211 INR/USD, excluding taxes.

Known allocation if every gate reaches image generation:
- text-judge qualification: hard cap USD 6.00;
- IMG-01 generation nominal: about USD 0.424;
- IMG-02 generation nominal: USD 0.480;
- allocated API maximum before contingency: about USD 6.904.

The remaining headroom is metering contingency, **not a retry pool**. Retries authorised: 0.

No account pre-funding above the approved consumption ceiling is implicit. A provider minimum deposit above that amount requires separate approval.

## Supply / pricing refresh

Current provider-authorised verification has improved the old EVAL-010 snapshot without changing scientific admission:
- exact Seedream 5 Pro route is now visible on fal; `IMG-04` is no longer an exact-version identity gap for planning;
- exact Sync-3 / v3 lip-sync route is now visible; `AUD-03` is no longer an exact-version identity gap for planning;
- Runway publishes current Hailuo 3 / Aleph 2 credit economics;
- Google/current hosted surfaces expose current Veo 3.1 identifiers and duration semantics.

Durable pricing correction:
- `coordination/decisions/CONTROLLER-VEO-PRICING-UNIT-CORRECTION-2026-08-26.md`

**Veo execution budgeting is per generated second on the currently planned routes.** The earlier Controller implication that `$0.40` / `$0.05` could be treated as per complete generated video count is withdrawn for execution budgeting.

Under the current frozen planning assumptions, the full 90-generation Stage-A **generation-side only** nominal consumption is approximately:
- USD 52.01 in USD-billed lines;
- plus up to ₹4.50 on the Sarvam TTS line;
- approximately ₹4,967 combined at the planning FX reference.

This excludes evaluator usage, human review, taxes, controlled-pack work, retries and account funding differences. The full 90-generation Stage A is **not authorised**.

## Still blocked / not authorised

Not authorised:
- **any paid EMP-001 call until explicit user approval**;
- full 90-generation Stage A;
- Stage B / Stage C execution;
- historical E7/E8;
- EVAL-006 — **PAUSED, DO NOT EXECUTE**;
- Registry population from unqualified instruments;
- broad controlled-pack acquisition;
- provider account funding above an explicitly approved ceiling;
- Production IR/Planner implementation.

No CpAO may be reported from EMP-001. Customer-outcome CpAO remains Stage C only.

## Next gate

The next decision is no longer “what should we research?”

It is explicit user approval or rejection of:

> **EMP-001: maximum USD 10 / approximately ₹954 consumed API spend, excluding taxes, no retries, no account pre-funding above the ceiling.**

Before the first external call, the zero-spend implementation/preflight tasks in the EMP-001 execution plan must be complete and freshly verified.
