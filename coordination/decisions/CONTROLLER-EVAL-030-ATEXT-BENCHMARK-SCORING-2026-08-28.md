# Controller — EVAL-030 A-TEXT Benchmark Scoring — 2026-08-28

## Status

**AUTHORISED: SCORE THE 16 MERGED EVAL-024 A-TEXT ARTIFACTS WITH THE MERGED EVAL-029 BENCHMARK-GRADE CLOUD VISION EVALUATOR.**

Do not regenerate any image.

## Inputs

### Generator evidence
Merged EVAL-024:
- manifest: `eval/empirical-tranche-1/atex/sealed-generation-v1/atex-generation-only-manifest.json`
- 16 sealed artifacts;
- 8 GPT Image 2;
- 8 Ideogram v3;
- retries 0;
- generation spend USD 0.904.

### Evaluator evidence
Merged EVAL-029:
- contract: `benchmark_text_ocr_v1`;
- Cloud Vision `TEXT_DETECTION`, no language hints;
- benchmark-qualified for Devanagari + Latin;
- strict-exactness qualified: false;
- Devanagari qualification FP 0.1250, FF 0.0208, consistency 1.0;
- Latin qualification FP 0.1042, FF 0.0000, consistency 1.0.

## Scoring shape

Score each of the 16 sealed artifacts exactly once.

Evaluator:
- Google Cloud Vision `TEXT_DETECTION`;
- no `languageHints`;
- target string never sent;
- retries 0.

Comparison:
- frozen NFC + outer-whitespace trim;
- exact code equality.

Before every evaluator dispatch:
- verify artifact SHA-256 against the merged EVAL-024 manifest;
- refuse any missing or mismatched artifact;
- never substitute or regenerate.

## Spend

16 evaluator calls x USD 0.0015 = **USD 0.024 maximum**.

Use the existing persistent EMP-001 ledger.
This remains within:
- USD 6 qualification/evaluator sub-cap;
- USD 10 total consumed API ceiling.

No account prefunding above the standing ceiling.

## Required output

For every artifact persist:
- slot;
- item id;
- target string;
- script;
- repeat index;
- generator route/config;
- artifact SHA;
- evaluator identity;
- evaluator contract id/hash;
- OCR transcription;
- exact-match boolean;
- evaluator cost ref;
- evaluator qualification error rates for that script;
- benchmark_qualified: true;
- strict_exactness_qualified: false;
- measurement_has_known_error: true.

Aggregate by route and by script:
- exact matches / attempts;
- observed exact-match rate;
- repeat-level consistency;
- total evaluator spend;
- combined generation + evaluator spend attributable to A-TEXT.

Do NOT mathematically “correct” the generator rate for evaluator error unless a separately justified method exists.
Report the raw observed benchmark result plus evaluator uncertainty.

## Boundaries

- no human review;
- no regeneration;
- no prompt changes;
- no route substitution;
- no retries;
- no additional OCR qualification;
- no Registry row yet;
- no full Stage-A expansion automatically;
- return to Controller for interpretation and Registry decision.

## Persistence

Commit the scoring result and bounded evaluator evidence/cost trace so a fresh clone can reproduce:
- artifact-hash verification;
- OCR transcription;
- exact-match computation;
- aggregate route metrics.

No secrets.
