# Controller EVAL-030 Integration and Registry Disposition — 2026-08-28

## Status

**EVAL-030 ACCEPTED AND MERGED. REGISTRY REMAINS EMPTY.**

Integration:
- PR #53
- merge commit `13fe76fa99d0dda1c9459cafe9972fe2ec93c3ba`

## Accepted benchmark result

A-TEXT exact-text slice:
- GPT Image 2: 6/8 observed exact matches = 0.750
- Ideogram v3: 1/8 observed exact matches = 0.125
- overall: 7/16 = 0.4375
- Devanagari: 5/8 = 0.625
- Latin/Hinglish: 2/4 = 0.500
- commercial claim with rupee sign: 0/4

Evaluator:
- Cloud Vision TEXT_DETECTION
- no language hints
- benchmark_qualified for Devanagari and Latin
- strict_exactness_qualified: false
- known false-pass rates carried with the evidence

Spend:
- evaluator: USD 0.024
- A-TEXT generation + evaluation: USD 0.928

## Interpretation

This is real empirical routing evidence:
- on this small exact-text benchmark slice, GPT Image 2 materially outperformed Ideogram v3;
- sample size is small;
- evaluator error is non-zero;
- the ₹ failures cannot be cleanly attributed to the generator versus OCR from this evidence alone.

Use this as a directional benchmark signal, not a production certification or precise population rate.

## Registry decision

Do **not** populate the Capability Registry from EVAL-030.

Reason:
- current Registry v1 explicitly permits rows only from instruments with status `qualified` or `deterministic`;
- EVAL-029 is `benchmark_qualified`, intentionally distinct from strict qualification;
- weakening Registry admission semantics merely to create a first row would destroy the meaning of the Registry.

Registry remains 0 rows.

This does not erase the evidence. EVAL-030 is durable empirical benchmark evidence and may inform bounded routing experiments where its uncertainty is carried explicitly.
