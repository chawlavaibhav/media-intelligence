# Controller Course Correction — Exact Text Becomes Non-Blocking Benchmark Capability — 2026-08-28

## Status

**USER COURSE CORRECTION ACCEPTED. HUMAN-CONFIRMED PRODUCTION GATE IS WITHDRAWN. ZERO-FALSE-PASS OCR IS NO LONGER A PROGRAMME-WIDE BLOCKER.**

This supersedes:
- `coordination/decisions/CONTROLLER-EVAL-025-DISPOSITION-HUMAN-CONFIRMED-TEXT-GATE-2026-08-27.md`
  only in its proposed next architecture;
- `eval/tasks/EVAL-028-HUMAN-CONFIRMED-EXACT-TEXT-PREP.md`, which is now cancelled/superseded and
  must not be executed.

Historical scientific results remain valid and preserved.

## Product principle

This project is building an API-native production system.

A benchmark evaluator should be judged by whether it is useful enough to compare/rank workflows and
estimate commercial reliability. It does NOT need to be a perfect production certifier for every
capability before the rest of the programme can move.

Therefore:

- exact Hindi text is one capability among many;
- imperfect exact-text checking must not freeze image/video capability benchmarking;
- human review is not inserted into the production API architecture merely to make the benchmark
  mathematically perfect;
- if a customer later requires near-zero exact-text risk, that is a product/workflow requirement to
  solve separately (e.g. deterministic text rendering/overlay, specialized verification, or
  customer-side review), not a prerequisite for learning which media models are useful.

## Preserve the strict research result

The old strict exactness screen remains meaningful:

- mismatch false-pass max 0.

Under that standard:
- Sonnet failed;
- Gemini failed;
- Cloud Vision failed;
- Tesseract variants failed.

Do NOT rewrite those results.

That strict screen is now classified as:
- `strict_exactness_certification`;
- useful for diagnosing whether an evaluator can make a zero-false-pass claim;
- **not required to proceed with benchmark/model capability work**.

## New benchmark-grade evaluator class

Create a separate evaluator contract for **benchmark use**, not strict certification.

Name:
- `benchmark_text_ocr_v1`

Purpose:
- compare/rank media-generation routes on text performance;
- estimate text reliability with known evaluator error;
- not certify customer-facing text as guaranteed exact.

Qualification thresholds:

### Primary
- mismatch false-pass rate <= **0.15**
  - equivalently: catches at least 85% of adversarial mismatches in the qualification battery;
- match false-fail rate <= **0.10**;
- repeat consistency >= **0.95**;
- empty/refusal/infrastructure failure rate <= **0.05** for a complete screen.

### Interpretation
- a candidate that passes this contract is `benchmark_qualified`;
- it is NOT `strict_exactness_qualified`;
- Registry/evidence must preserve that distinction;
- metrics scored by this evaluator must carry its measured qualification error rates and contract id.

## Cloud Vision disposition under benchmark contract

Existing Devanagari evidence for Cloud Vision TEXT_DETECTION, no language hints:

- false-pass rate: 0.125;
- match false-fail rate: 0.0208;
- repeat consistency: 1.0;
- empty transcriptions: 0;
- infrastructure failures: 0.

Therefore it **meets the proposed benchmark-grade Devanagari thresholds**.

However Latin was not run under this candidate because the old strict progressive gate stopped after
Devanagari.

Next bounded action:
- run Cloud Vision Latin qualification only under the new benchmark contract;
- 96 items × 3 repeats = 288 calls;
- retries 0;
- conservative reservation USD 0.432;
- use existing persistent ledger;
- no language hints;
- preserve all prior evidence;
- if Latin passes benchmark thresholds, Cloud Vision becomes benchmark-qualified for both scripts.

## A-TEXT

A-TEXT generation-only remains authorised independently.

Once EVAL-024 sealed artifacts exist:
- score them using the benchmark-qualified text evaluator if Cloud Vision covers both scripts;
- do not require a human reviewer;
- preserve evaluator uncertainty in reported metrics;
- no claim of perfect exactness certification.

If Cloud Vision fails Latin benchmark qualification:
- do not block the rest of Stage A;
- report A-TEXT Latin/Hindi scoring coverage as partial/unavailable where appropriate;
- continue other capability lanes.

## Stage-A / programme rule

Exact-text qualification is no longer a global gate.

A Stage-A slot/capability may proceed whenever the instruments required for THAT measurement are
ready.

No unrelated image/video/audio capability is blocked merely because exact Hindi text remains imperfect.

The project should continue in parallel on:
- temporal/video evaluator qualification;
- operational logging/deterministic instruments;
- marketplace-derived Stage-C brief preparation;
- A-TEXT generation;
- other independently ready capability families.

## Production interpretation

For future product architecture:

- benchmark-grade OCR may be used as a confidence/quality signal;
- it must not be marketed internally as a guaranteed exact-text certifier;
- if a workflow/customer needs stronger text guarantees, solve that at the production-recipe level
  (for example deterministic text compositing rather than asking a generative model to paint text)
  or with a separate stricter verifier.

No mandatory two-human loop is part of the production API design from this decision.

## Spend

Existing paid qualification spend remains USD 1.3037905.

New bounded Latin Cloud Vision reservation:
- USD 0.432 max.

This remains inside the existing EMP-001 qualification and total ceilings.

No account prefunding.
