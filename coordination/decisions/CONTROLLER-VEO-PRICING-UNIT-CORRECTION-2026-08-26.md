# Controller Decision — Correct Veo execution billing unit

**Date:** 26 Aug 2026  
**Scope:** pricing/evidence correction only  
**Spend authorised:** ₹0 / $0

## Decision

Withdraw the repository shorthand that could be read as **Veo 3.1 / Veo 3.1 Lite prices being per generated video count** for execution budgeting.

For current empirical planning, the relevant Veo hosted/API prices are to be treated as **per generated second**, pinned to the exact route and audio/resolution mode.

This corrects a supply/pricing evidence interpretation. It does **not** reopen the scientific roster, benchmark design, capability contract, or Stage A/B/C counts.

## Why the correction is required

The earlier EVAL-010 evidence captured a Google Cloud pricing surface whose English rendering used `/ 1 count`. That wording was carried into Controller shorthand as though a complete generated video were one billable count.

Fresh pre-execution verification on 26 Aug 2026 found current provider-authorised execution surfaces that are unambiguous about a **per-second** unit:

- fal Veo 3.1: https://fal.ai/models/fal-ai/veo3.1 — current route lists USD 0.40/sec with audio and USD 0.20/sec silent for the relevant quality tiers.
- fal Veo 3.1 Lite: https://fal.ai/models/fal-ai/veo3.1/lite — current route lists 720p with audio at USD 0.05/sec and silent at USD 0.03/sec.
- Google Veo documentation: https://ai.google.dev/gemini-api/docs/video — current API documentation exposes discrete generated durations; cost planning must therefore preserve duration explicitly.

The safe execution rule is to use the **route's explicit billing unit**, never extrapolate from a sibling pricing page, and never generalise one route's rate to another wrapper.

## Consequence for Stage A planning

The Controller freezes a **6-second common video duration** for the admission screen unless an exact slot cannot support it. This gives a common temporal observation length across the planned routes while avoiding delivery-length spend during admission.

At 6 seconds:

- VID-01 Veo 3.1 with audio on the planned fal route: `8 calls × 6 sec × $0.40/sec = $19.20`.
- VID-05 Veo 3.1 Lite 720p with audio on the planned fal route: `8 calls × 6 sec × $0.05/sec = $2.40`.

These are planning figures, not authorised spend.

## Historical handling

Do not rewrite EVAL-010's historical evidence artifact. It records what that worker saw and how it read the source at the time.

From this decision forward:

- the old `per count` / `per generated video` Controller implication is superseded for execution budgeting;
- exact source route, duration, audio mode and resolution must be recorded with every Veo trial;
- cost ledgers must store the provider's actual billed basis rather than a normalized invented unit.

## What remains unchanged

- VID-01 and VID-05 remain the same scientific questions.
- VID-05's accepted-outcome cost-knee / CpAO conclusion remains Stage C only.
- Stage A remains 90 generations in the full design and is not authorised by this decision.
- No model or evaluator is qualified by this correction.
