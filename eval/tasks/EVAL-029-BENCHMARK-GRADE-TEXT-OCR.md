# EVAL-029 — Benchmark-Grade Text OCR Qualification and A-TEXT Scoring Handoff

**Owner:** Eval worker  
**Authority:** `coordination/decisions/CONTROLLER-EXACT-TEXT-NONBLOCKING-BENCHMARK-THRESHOLD-2026-08-28.md`  
**Purpose:** benchmark utility, NOT strict exactness certification

## Objective

Create and execute a separate benchmark-grade text-evaluator contract that is sufficient to compare
media-generation routes without pretending the evaluator is a perfect production certifier.

Do not mutate or reinterpret historical strict contracts/results.

## Contract

Create `benchmark_text_ocr_v1` with:

- mismatch false-pass rate <= 0.15;
- match false-fail rate <= 0.10;
- repeat consistency >= 0.95;
- empty/refusal/infrastructure failure rate <= 0.05;
- 3 repeats;
- blind transcription only for qualification/scoring;
- exact local comparison with existing NFC + outer-whitespace semantics;
- retries 0.

Semantics:
- `benchmark_qualified` is distinct from `strict_exactness_qualified`;
- preserve both statuses explicitly;
- no human review is part of this evaluator contract.

## Existing Cloud Vision Devanagari evidence

Recompute, do not rerun, the existing Cloud Vision TEXT_DETECTION/no-language-hints Devanagari result
against the benchmark contract.

Expected historical metrics from accepted evidence:
- false-pass rate 0.125;
- match false-fail rate 0.0208;
- repeat consistency 1.0;
- empty 0;
- infrastructure failures 0.

Mechanically verify from stored observations rather than copying prose.

If recomputation differs, stop and return to Controller before any paid call.

## Live Latin-only screen

If Devanagari recomputation passes:
- run Cloud Vision TEXT_DETECTION on Latin only;
- no languageHints;
- 96 items × 3 repeats = 288 calls;
- retries 0;
- conservative reservation USD 0.432;
- use existing persistent EMP-001 qualification ledger;
- no Devanagari rerun;
- no Gemini/Anthropic/Tesseract/fal calls in this phase.

Persist a new benchmark-contract-specific result and evidence fingerprint.
Do not overwrite historical Cloud Vision strict-contract evidence.

If Latin passes:
- status = benchmark-qualified for [devanagari, latin];
- strict exactness status remains failed.

If Latin fails:
- record partial benchmark coverage;
- do not block unrelated model benchmark work.

## A-TEXT handoff

If EVAL-024 sealed generation-only artifacts are already available on a pushed/merged branch visible
to this worker:
- consume only those exact artifact hashes;
- score A-TEXT using the benchmark-qualified Cloud Vision evaluator;
- no human review;
- do not regenerate any image;
- report evaluator uncertainty alongside generator results;
- explicitly label results as benchmark-grade, not strict-certification.

If EVAL-024 artifacts are not yet available:
- prepare the scoring handoff and stop after qualification;
- do not wait or invent artifacts.

## Reporting

For every generator result later scored by this evaluator, carry:
- evaluator contract id/version;
- qualification false-pass rate;
- qualification false-fail rate;
- repeat consistency;
- script coverage;
- strict_exactness_qualified: false;
- benchmark_qualified: true/false.

This makes downstream consumers aware that the measurement itself has bounded error.

## Boundaries

- no human-in-loop requirement;
- no threshold changes after seeing Latin;
- no new OCR candidate search;
- no Registry population unless separately authorised after A-TEXT review;
- exact-text imperfection does not block unrelated Stage-A capabilities;
- no account prefunding.

Push branch; do not merge.
Return exact tested/live HEAD and results.
