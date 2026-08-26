# Controller Decision — Freeze EMP-001 preparation shape

**Date:** 26 Aug 2026  
**Decision type:** zero-spend empirical-execution preparation  
**External spend authorised:** **none**

## Decision

Freeze the first empirical tranche candidate as **EMP-001**, a gated text-first experiment rather than the entire 90-generation Stage A.

EMP-001 is prepared in two layers:

1. qualify the minimum measurement path required to trust exact-text evidence;
2. only if that qualification succeeds, run a 16-generation A-TEXT partial admission screen across IMG-01 and IMG-02.

The proposed external consumed-API ceiling is **USD 10.00**. This decision does **not** authorise that spend. The user must explicitly approve it before any paid evaluator or generation call.

## Why the full 90-generation Stage A is not the first tranche

The merged execution contract permits partial Stage A as each slot's instruments qualify. Four evaluator families remain blocked on resource material or human reference. Waiting for every pack before making any model observation would delay the highest-value text question without improving its measurement.

IMG-01 and IMG-02 are the first useful comparison because the project already holds the validated Devanagari construction battery and can build the corresponding Latin pack without a new Resources pack.

## Frozen zero-spend preparation parameters

### Text qualification

- Devanagari battery: existing authoritative 96-item validated view, unchanged.
- Latin battery: new separate 96-item pack; 48 exact-match + 48 controlled-mismatch.
- Qualification repeats: `R_q = 3` full passes per input shape.
- Shapes: `transcribe` and `verdict`, kept separate.
- Judge candidates for the first qualification attempt:
  - OpenAI `gpt-5.4-mini`, exact snapshot pinned at execution;
  - Google `gemini-3.5-flash-lite`, exact current version pinned at execution.
- Progression: Devanagari first. A candidate that fails Devanagari does not consume Latin qualification calls.
- Maximum evaluator calls if both candidates reach both scripts: 2,304.
- Proposed evaluator API consumption guard inside EMP-001: USD 6.00.

### Provisional first-run qualification gate

Carry the existing FAMILY-1 thresholds only as a bounded first-run instrument gate:

- mismatch false passes: 0 allowed;
- clean-match false-fail rate: ≤10%;
- refusal rate: ≤5%, separately reported;
- repeat consistency: ≥0.95 across all three passes in both shapes.

These are not declared empirical universal thresholds. Their own usefulness is to be revisited after the first two candidate results.

Qualification scope explicitly excludes malformed generated glyphs because the generated-glyph stress layer is not built.

### A-TEXT partial screen

Freeze exactly four comparability targets:

1. `शुभ दीपावली`
2. `आज की डील`
3. `Aaj ki Deal`
4. `SAVE 20% • ₹999`

Each item asks for a plain 1:1 poster containing the target as the only text. This screen intentionally isolates text exactness and does not pretend to evaluate overall creative quality.

Routes:

- IMG-01: `gpt-image-2` via fal `openai/gpt-image-2`, 8 unseeded generations;
- IMG-02: Ideogram V3 via fal `fal-ai/ideogram/v3`, BALANCED, 8 unseeded generations.

Both routes use unseeded repeats for this first comparison. The resulting evidence must never later be pooled with held-seed reproducibility evidence.

Primary generated-output measurement is blind `transcribe` followed by code-level exact string comparison. A target-visible `verdict` may be recorded as diagnostic evidence but cannot override a primary mismatch.

### A-TEXT interpretation boundary

EMP-001 may stop deeper **text-specific** spend for a route if it records zero exact matches across all scoreable Devanagari/Hinglish opportunities in this frozen screen.

Any non-zero result is not full promotion. IMG-01/IMG-02 cannot become complete Stage-A survivors until the other instrument families required by those scientific slots are qualified.

## Budget posture

Planning figures under current provider-authorised prices:

- text-judge qualification: hard proposed cap USD 6.00;
- IMG-01 8-generation nominal line: approximately USD 0.424;
- IMG-02 8-generation nominal line: USD 0.480;
- known maximum allocated API usage if all gates reach generation: approximately USD 6.904;
- proposed EMP-001 consumed-API ceiling: **USD 10.00**, leaving metering contingency but **no retry pool**.

At the planning reference rate of 95.4211 INR/USD, USD 10 is approximately ₹954 before taxes.

No account pre-funding above the approved consumption ceiling is implicit. If a provider requires a larger minimum deposit, execution must stop for separate approval.

## Full Stage A remains only a forecast

A current route/price refresh now places the 90-generation Stage-A generation-side nominal consumption around USD 52.01 plus up to ₹4.50 of Sarvam TTS input under the frozen assumptions. Evaluator, human-review, taxes, pack work and account prefunding are separate.

That 90-generation run is **not authorised**.

## Execution authority

Tasks that only implement/dry-run the EMP-001 harness and build deterministic local material may proceed at ₹0.

The first external evaluator/model call requires a new explicit user approval of the USD 10 / approximately ₹954 consumed-API ceiling.
