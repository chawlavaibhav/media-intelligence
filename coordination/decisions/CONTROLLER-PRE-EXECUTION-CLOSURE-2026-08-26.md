# Controller Decision — Pre-Execution Freeze Closed

**Date:** 26 Aug 2026  
**Status:** APPROVED / CLOSED  
**Effect:** the final pre-execution design package is integrated on `main`; broad research/design is closed. No paid empirical execution is authorised by this decision.

## 1. Controller disposition

The Controller accepts GOV-004's verdict **PASS WITH NON-BLOCKING NOTES** and closes the final pre-execution coherence gate.

The project has completed the request/measurement/evidence architecture required to begin empirical planning. The next useful information must come from qualification and model/workflow observations, not another broad research round.

This decision does **not** claim that the science is proven, that any model is good, that any evaluator is qualified, that Canon improves outcomes, that the Planner exists, or that any paid run is authorised.

## 2. Integrated packages

The following reviewed packages are now integrated on `main`:

- **CANON-010** reviewed head `3cf29790dfc0ae34a9ded2a42ad5b8774fb36d58` via PR #27; merge commit `bcba5bd0130150ada1797c1fea9b1d898a06a111`.
- **RES-004** reviewed head `2dc4796ff0916172855e29d0fc02a17a9d9a4201` via PR #28; merge commit `87c582b5bfebd44c1e60de098d1392260d86089f`.
- **EVAL-010** reviewed head `8a8fc0915bbf8acfe193cef854e9e0fbe64239dc` via PR #29; merge commit `81b7e3fe91d4c7f32d4b1696aa8039918bb550de`.
- **EVAL-011** reviewed worker head `e300999b6e02c58e1d9bfd48a3963b3e5293ff51` via Controller-resolved PR #31; merge commit `afa647b7a2c7ce8f3dbcc2cf754a96099284d85a`.
- **GOV-004** reviewed head `bd6dbd75e6319f74bde0f25c5dc9c4872cb16a51` via PR #26; merge commit `35391e2fd57a83bf9fd8f9a86c4768976b6b9dfb`.

EVAL-009 remains historical worker output. EVAL-011 is the corrected live freeze package.

## 3. EVAL-011 merge resolution

GOV-004 N-1 identified one real merge hazard: the EVAL-011 branch carried an older Controller-authored `coordination/CONTROL-STATE.md`.

The Controller resolved the integration by preserving current `main` state and carrying the reviewed EVAL-011 domain package forward. During integration verification, an initial subtree construction was found to remove the already-merged EVAL-010 `model-supply` subtree. That candidate tree was **not merged**. The final integration overlay preserved EVAL-010 supply evidence and added EVAL-011 content only.

The final net EVAL-011 integration diff versus then-current `main` was additive-only under:
- `eval/pre-execution-freeze/` while preserving `model-supply/`; and
- `eval/pre-execution-integration/`.

No Eval methodology was changed during resolution.

## 4. Freeze now in force for empirical planning

### Request contract

Requested operation vocabulary is frozen for this experiment layer as:

`generate | edit | animate | restore | extend | compose | variants`

Requested operation remains customer intent and remains distinct from production workflow mode. The original 30 authored briefs remain historical probes; the 11-item extension is structural coverage, not demand evidence.

### Measurement contract

Capability Contract v2 is the accepted forward contract:
- **44 total = 43 active + 1 dormant `repairability`**;
- V1 36-capability contract and V1 100-item bank remain immutable historical baselines;
- condition architecture is **13 families**; 8,192 is only the naive two-level Cartesian size, not an authorised sweep;
- scientific roster is **12 core + 2 reserve question slots**;
- `blocked_by_prerequisite_failure` remains unsatisfied at outcome acceptance;
- seeded and unseeded repeat evidence must not be silently pooled.

Staged execution design remains:
- **Q:** evaluator/material qualification — 0 model generations;
- **A:** admission/discrimination screen — 90 model generations;
- **B:** deeper benchmark — up to 404 additional generations for survivors;
- **A+B design ceiling:** 494 generations;
- **C:** 32 end-to-end outcome attempts; generation count depends on the production topology used.

494 generations / 5,515 evaluator calls / 188 human-review units are design ceilings/forecast inputs, **not an approved paid tranche**.

### Evidence and CpAO contract

Forward topology is:

`job -> outcome -> sequence_or_asset_set -> production_unit -> production_step -> attempt -> artifact`

One provider/API/transform call = one trial. Failed/refused/timed-out attempts remain evidence. Historical v2.1 evidence is not backfilled with invented v3 context.

Fully-loaded whole-outcome CpAO remains the primary business metric; API/tool CpAO is diagnostic. One-time R&D, benchmark construction, pack acquisition and evaluator qualification are not charged as per-customer CpAO unless a later accounting policy explicitly amortises them.

Exactly four controlled-pack families remain in scope. Provisional entity counts and the 173-hour full-pack estimate are not first-run prerequisites or approved budgets.

## 5. Supply state remains partial

EVAL-010/EVAL-011 supply evidence remains intentionally incomplete:
- 12 of 14 scientific slot identities are resolved/provider-authorised;
- `IMG-04` and `AUD-03` remain unresolved/version-mismatched and must not be silently substituted;
- no scientific slot was deleted for sourcing convenience;
- price completeness is insufficient for a paid tranche;
- `Frontier Clouds` service identity remains unresolved;
- direct and aggregator wrappers may expose materially different controls.

Controller price clarification remains:
- Nano Banana 2 `$0.067` means approximately per **generated 1K-resolution image**, not per thousand images;
- Veo 3.1 Lite `$0.05` remains route-specific.

## 6. Empirical floor remains zero

At closure:
- **0 qualified models/workflows**;
- **0 qualified subjective/perceptual evaluator families**;
- **0 empirical Capability Registry rows**;
- **0 accepted evidence that Canon improves model outcomes**;
- **0 approved Production IR/Planner implementation**.

The design package makes those questions testable; it does not answer them.

## 7. What remains blocked / unauthorised

This closure does not authorise:
- any provider/model generation call;
- any paid evaluator/checker call;
- Capability Registry population;
- controlled-pack acquisition or capture;
- provider account funding or terms acceptance;
- historical E7/E8 execution;
- EVAL-006, which remains **PAUSED — DO NOT EXECUTE**;
- the 494-generation ceiling as a paid run;
- Production IR/Planner implementation.

## 8. Next Controller gate

There is **no further broad research round scheduled**.

The next Controller work is to prepare the smallest empirical tranche that can produce decision-useful evidence:
1. define/qualify the Stage-Q evaluators and only the materials they require;
2. verify exact execution routes and prices needed for the Stage-A scientific slots;
3. produce a separately priced Stage-A admission screen for explicit user approval;
4. only after approval, execute empirical model/workflow testing and begin Registry population.

No spend or empirical call is implicitly authorised by this sequence.
