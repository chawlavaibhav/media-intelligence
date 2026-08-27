# Controller EVAL-025 Disposition — Close Tesseract; Prepare Human-Confirmed Exact-Text Gate — 2026-08-27

## Status

**EVAL-025 ACCEPTED AND INTEGRATED. TESSERACT CONFIGURATION SEARCH IS CLOSED. NEXT EXACT-TEXT DIRECTION: FAIL-CLOSED HUMAN-CONFIRMED COMPOSITE, PREPARATION ONLY.**

Integration:
- PR #47
- merge commit `711aa8ceb12231610212236a19ab21578fb028c0`

Tested EVAL-025 head:
- `b6c6ba663fc8217bc70bb6ac12c81c60281c90b8`

## Scientific disposition

Script-specific Tesseract legs:
- Devanagari `hin`: 3 false passes / 1 unique; false-fail rate 0.6042; consistency 1.0.
- Latin `eng`: 12 false passes / 4 unique; false-fail rate 0.5000; consistency 1.0.

Both fail:
- mismatch false-pass max 0;
- match false-fail rate max 0.10.

Script routing removed wrong-script errors but did not reduce false-pass counts.

Therefore:
- **Tesseract literal line is scientifically disqualified and CLOSED**;
- no more PSM/OEM/language/preprocessing/DAWG sweeps are authorised without a new mechanism-level rationale.

## Mechanism finding

Across the exact-text programme:

1. lexical/language priors are a major cause of silent word repair;
2. removing lexical aids sharply reduces that failure;
3. after lexical repair is removed, a classifier/sequence-model floor remains:
   - Devanagari glyph confusion;
   - Latin homoglyph/repetition confusion;
4. script routing can remove wrong-script errors but does not remove the residual false-pass floor.

This means the project has reached diminishing returns for single OCR configuration search.

## Why a pure machine ensemble is not enough yet

At least one residual Tesseract false-pass item (`dx-0013`) also appears among false-pass items from
stronger OCR/VLM candidates.

Therefore a simple rule such as:
- "pass only if Cloud Vision and Tesseract both say exact"

cannot be assumed to satisfy the zero-false-pass gate.

Any machine-only ensemble must itself qualify empirically; none is authorised by this decision.

## Next architecture to prepare

Prepare a **human-confirmed exact-text composite**:

1. automated OCR acts as a first-stage rejector;
2. any item the automated layer would PASS is shown to **two independent blind human readers**;
3. neither human sees the target, source transcription, OCR output, or the other reader's response;
4. both transcribe exactly what is visible;
5. code compares each transcription to the requested target;
6. composite MATCH only if the human confirmation rule is satisfied;
7. any disagreement / cannot-read / ambiguity fails closed.

Preferred automated first-stage candidate for design:
- Cloud Vision TEXT_DETECTION, because it had the best operational stability and a low match false-fail rate;
- this does NOT make Cloud Vision independently qualified.

Do not include Tesseract in the production composite merely because it is more literal; its false-fail
rate is too high.

## Human protocol basis

Reuse the already-approved principles in:
- `eval/calibration/devanagari-v0/HUMAN-REVIEW-GUIDE.md`;
- `eval/calibration/devanagari-v0/CALIBRATION-RUN-PLAN-V0.md`;
- `eval/tasks/EVAL-004-HUMAN-REFERENCE.md`.

Core principles:
- two distinct independent readers;
- blind transcription, never target-visible verdict;
- transcribe what is drawn, do not correct;
- exact character comparison in code;
- cannot-read / ambiguous is an allowed fail-closed response;
- freeze both reader response files before comparison;
- do not expose one reader to the other's response.

## Preparation boundary

Authorise zero-spend EVAL-028 preparation only:
- design/freeze composite contract;
- build blinded review pack over existing frozen Devanagari + Latin qualification materials;
- build deterministic response ingest/comparison;
- build synthetic/fake-reader tests;
- build later A-TEXT review mode that consumes the sealed EVAL-024 artifact hashes;
- no human review is started by this decision;
- no Cloud Vision/API call is made by this decision;
- no A-TEXT scoring yet;
- Registry unchanged.

The Controller will separately approve/coordinate actual human time after reviewing the prepared pack.

## Parallel work unaffected

- EVAL-024 A-TEXT generation-only remains authorised and may finish independently.
- CANON-011 marketplace-derived brief preparation remains authorised.
- Any other separately authorised zero-spend lanes remain unaffected.

Current paid qualification spend remains USD 1.3037905.
