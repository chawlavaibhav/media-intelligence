# First Empirical Tranche Proposal

**Date:** 26 Aug 2026  
**Status:** PROPOSED — EXPLICIT USER SPEND APPROVAL REQUIRED  
**External calls made by this proposal:** 0  
**Spend to date:** ₹0 / $0

## Controller recommendation

Do **not** authorise the full 90-generation Stage A yet.

Authorise one deliberately narrow first empirical tranche:

> **Tranche 1 = qualify the minimum text/geometry/logging measurement path, then run an A-TEXT partial admission screen on IMG-01 and IMG-02 only if those instruments qualify.**

This is the fastest route from architecture to trustworthy evidence without waiting for the AV, product/person-reference and commercial-review packs.

### Requested external-spend ceiling

**USD 10 maximum consumed API spend** (approximately **₹954 at the 26 Aug 2026 reference FX rate of 95.4211 INR/USD**), excluding taxes.

This is a **consumption ceiling**, not permission to pre-fund an account with a larger minimum deposit. If any provider requires account funding/top-up above this ceiling, stop and return to the Controller/user before funding.

No retries are included. A failed/refused/timed-out paid call still consumes its trial and its cost.

## Why this tranche, not the whole 90 generations

The merged Stage-Q contract explicitly permits Stage A to start slot-by-slot once the instruments needed by that slot are qualified.

IMG-01 asks the highest-leverage production question in the current roster: whether exact Devanagari/Hinglish text is viable from a frontier general image model. IMG-02 asks the directly adjacent question: whether a typography specialist materially outperforms that generalist.

A negative answer can change production topology immediately: generated type may need to become composited/repaired type. That is valuable information even before the rest of the benchmark is runnable.

The remaining Stage-A questions depend on currently missing qualification material: clean AV clips, person/product identity packs with decoys, speech material and an independent commercial-review panel. Waiting for all of those before learning anything from images would recreate the research-first bottleneck this project is trying to leave behind.

## Tranche 1 sequence

### Gate 0 — deterministic preflight, $0 external spend

Run locally:

- Q1 `deterministic_cv_geometry` against the existing 102-fixture pack;
- Q7 operational logging/persistence checks;
- verify that every future paid evaluator call and every generated image can be persisted under the one-call-one-trial contract;
- materialise the four A-TEXT comparability-core items for IMG-01/IMG-02 before any provider call.

If persistence or deterministic checks fail, stop. Spend remains $0.

### Gate 1 — build the Latin exact-text qualification pack, $0 API spend

Freeze `N_latin = 96`, in a **new separate artifact**. Do not mutate the frozen Devanagari battery.

Shape:

- 48 exact-match items;
- 48 controlled-mismatch items;
- one mismatch opportunity per base string;
- controlled mismatch classes covering confusable substitution, omission, insertion, transposition, case/diacritic, and punctuation/digit/spacing errors where visibly perceptible;
- truth known by construction;
- a quick human perceptibility sanity pass, not a new statistical ground-truth study.

The Latin pack exists only to qualify the text judge for the A-TEXT screen. It is not evidence about generator quality.

### Gate 2 — qualify text/OCR judges progressively

Test two independent current multimodal judge candidates so one model's language prior is not silently treated as measurement truth:

1. OpenAI `gpt-5.4-mini` (pin snapshot at execution time);
2. Google `gemini-3.5-flash-lite` (pin exact GA model/version at execution time).

Current official pricing evidence at planning time:

- OpenAI GPT-5.4 mini: $0.75 / 1M input tokens, $4.50 / 1M output tokens; image input supported. Source: https://developers.openai.com/api/docs/models/gpt-5.4-mini
- Gemini 3.5 Flash-Lite: $0.30 / 1M input tokens and $2.50 / 1M output tokens on paid standard Gemini API; image input supported. Source: https://ai.google.dev/gemini-api/docs/pricing

#### Freeze for this tranche

`R_q = 3` full passes per shape.

Two shapes remain separate:

- `transcribe`: judge never sees the requested target; code performs exact comparison;
- `verdict`: judge sees the requested target.

The blind-input verification in the existing contract remains mandatory.

#### Progressive stop

**Q2a first: Devanagari.**

Per candidate: `96 items × 2 shapes × 3 passes = 576 calls`.

Both candidates together: maximum **1,152 Devanagari evaluator calls**.

A candidate that fails the Devanagari qualification gate does **not** advance to Latin. This prevents paying another 576 calls to demonstrate that an already-disqualified checker also fails English.

**Q2b second: Latin, survivors only.**

Per survivor: another `96 × 2 × 3 = 576 calls`.

Maximum if both survive: another **1,152 calls**.

Absolute maximum across both candidates and both scripts: **2,304 evaluator calls**.

#### Provisional qualification gates for Tranche 1

Carry the existing FAMILY-1 proposal forward as a bounded first-run rule:

- zero false passes across the mismatch set — disqualifying;
- false-fail rate ≤10% on clean matches;
- refusal ≤5%, reported separately;
- repeat consistency ≥0.95 across the three full passes in both shapes.

These thresholds are **provisional instrument gates, not empirically established universal truths**. Record their performance and revisit after the first two candidate results. Do not convert them into a general benchmark claim.

A checker passing here is qualified only against correctly formed but wrong text in these constructed batteries. The unbuilt generated-glyph stress layer means malformed glyph recognition remains outside the qualified scope.

#### Evaluator spend guard

Hard combined Q2 API-consumption ceiling: **$6.00**.

Before every paid call, the harness must confirm cumulative recorded evaluator cost remains below the ceiling. If the next call could breach it, stop and return an incomplete qualification result rather than silently raising the budget.

### Gate 3 — A-TEXT partial admission screen, only after Gate 2 passes

This is **not** the full scientific admission verdict for IMG-01 or IMG-02.

It is a deliberately narrower question:

> On the frozen shared text comparability items, does this route fail badly enough on exact Devanagari/Latin text that deeper spend is already unjustified?

Run:

- IMG-01: `gpt-image-2`, 4 comparability items × 2 repeats = 8 generations;
- IMG-02: `ideogram-v3`, 4 comparability items × 2 repeats = 8 generations.

Planned routes/prices:

- IMG-01 via fal `openai/gpt-image-2`, 1024×1024 medium projection ≈ $0.053/image → **$0.424 nominal for 8**;
- IMG-02 via fal `fal-ai/ideogram/v3`, BALANCED = $0.06/request → **$0.480 for 8**.

Maximum nominal generation consumption: **$0.904**.

If no text judge qualifies, **run zero image generations**.

If a route fails the A-TEXT exactness screen, it may be eliminated from deeper text-focused spend. If it passes, that is **partial evidence only**: it may not be promoted as a complete Stage-A survivor until every instrument required by its full scientific slot is qualified.

## Tranche 1 budget envelope

| Line | Maximum / planning amount |
|---|---:|
| Q1/Q7 deterministic work | $0 external |
| Latin pack build | $0 API; human perceptibility time only |
| Text-judge qualification | **hard cap $6.00** |
| IMG-01 8 generations | ~$0.424 |
| IMG-02 8 generations | $0.480 |
| Known API subtotal if everything reaches Gate 3 | **≤$6.904** |
| Controller contingency inside requested ceiling | ~$3.096 |
| **Requested consumed-API ceiling** | **$10.00 (~₹954), excluding taxes** |

The contingency is not a retry pool. It covers token-meter variation and measurement overhead that cannot be known exactly before the first real evaluator payloads are metered.

## What this spend buys

If successful, Tranche 1 produces the project's first trustworthy empirical evidence on:

- whether either proposed text judge is safe enough to measure constructed Devanagari/Latin exactness;
- whether showing a judge the target materially changes false-pass behaviour (`transcribe` vs `verdict`);
- whether the generalist IMG-01 route or specialist IMG-02 route is obviously non-viable on exact text before deeper benchmark spend;
- actual evaluator token/call economics, replacing forecast guesses with measured costs;
- first empirical trial records suitable for the Registry **only where the instrument qualification contract permits it**.

## What this spend does NOT buy

It does not establish:

- full IMG-01 or IMG-02 capability quality;
- product/person identity, commercial composition or subjective creative quality;
- video/audio performance;
- customer acceptance;
- Canon uplift;
- Planner/routing uplift;
- Cost per Accepted Outcome.

Customer CpAO remains Stage C only.

## Full Stage A — price refresh, not authorisation

The full 12-slot / 90-generation Stage A is now substantially more price-resolved than EVAL-010's original snapshot. The current planning table lives at:

`eval/empirical-planning/STAGE-A-ROUTE-PRICE-REFRESH-2026-08-26.yaml`

Under the frozen planning assumptions (including 6-second video probes), generation-side nominal consumption is approximately:

- **$52.01** across USD-billed lines; plus
- **≤₹4.50** for the Sarvam TTS line;
- approximately **₹4,967 combined at the reference FX rate**, before evaluators, human review, taxes, pack acquisition or account-prefunding differences.

This is **not** a request to authorise the full Stage A. Four evaluator families still require qualification material before their associated slots can produce interpretable results.

## Next authorization boundary

This proposal itself authorises **nothing external**.

The next external action requires the user's explicit approval of:

> **Tranche 1: maximum $10 / approximately ₹954 consumed API spend, with no account pre-funding above that ceiling and no retries.**

After approval, execution must proceed gate-by-gate. A failed gate stops downstream spend automatically.
