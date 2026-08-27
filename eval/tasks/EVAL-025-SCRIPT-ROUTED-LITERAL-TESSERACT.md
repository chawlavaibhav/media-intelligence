# EVAL-025 — Script-Routed Literal Tesseract Probe

**Owner:** Eval worker  
**Authority:** `coordination/decisions/CONTROLLER-EVAL-023-DISPOSITION-AND-SCRIPT-ROUTED-OCR-2026-08-27.md`  
**API spend:** USD 0

## Objective

Measure whether selecting a script-specific literal OCR model removes the large wrong-script error
surface seen in the mixed `hin+eng` EVAL-023 candidate.

Run both legs independently:
- Devanagari with `hin` only;
- Latin with `eng` only.

This is the last authorised Tesseract configuration probe in this line unless Controller later
opens a new mechanistic experiment.

## Base

Use current `origin/main` including merged EVAL-023.

Reuse:
- Tesseract 5.5.3 if unchanged;
- pinned tessdata_best tag 4.1.0 / commit `e2aad9b983032bb1beff9133104a67cdbb87ca4d`;
- existing EVAL-023 local adapter and evidence semantics.

Do not redownload or change traineddata if the existing hashes still match.

## Frozen configurations

Freeze both candidate identities in git BEFORE scientific execution.

### Candidate A — Devanagari
- alias: `tesseract5-hin-literal-psm13-v1`
- language: `hin`
- OEM 1
- PSM 13
- no preprocessing
- fresh process per trial
- no user words
- retries 0
- all six DAWG flags = 0

### Candidate B — Latin
- alias: `tesseract5-eng-literal-psm13-v1`
- language: `eng`
- OEM 1
- PSM 13
- no preprocessing
- fresh process per trial
- no user words
- retries 0
- all six DAWG flags = 0

Target/ground truth must not enter subprocess command/stdin/temp path/environment.

## Scientific runs

Run both legs regardless of the other's outcome.

Devanagari:
- authoritative validated 96-item view;
- 3 repeats;
- 288 local executions.

Latin:
- authoritative reviewed 96-item pack;
- 3 repeats;
- 288 local executions.

No progressive stop between these two because they are separate script-specific candidate legs,
not one mixed candidate progressing through scripts.

## Gates per leg

Use OCR contract scientific thresholds unchanged:
- mismatch false-pass max 0;
- match false-fail rate max 0.10;
- empty-transcription rate max 0.05;
- repeat consistency min 0.95.

Do not change normalization.

## Required comparison

For each leg report:
- executions/completeness;
- false passes + unique false-pass items/classes;
- false fails + unique false-fail items;
- empty transcriptions;
- repeat consistency;
- failed gates;
- wrong-script reads;
- trailing punctuation-only differences;
- ZWJ/ZWNJ-only differences;
- direct comparison to the same-script EVAL-023 mixed-language result.

Also explicitly answer:
1. Did script restriction reduce wrong-script false fails?
2. Did it change false-pass count?
3. Did it clear every qualification gate?
4. If not, what mechanism remains?

## Evidence

Persist provider-specific human-readable results for both legs and fingerprint-bound config/evidence.
Do not overwrite prior EVAL-023 human-readable evidence.

The two legs are NOT yet a composite evaluator identity and may not open A-TEXT.

## Verification / boundaries

Before scientific execution:
- focused tests green;
- preflight green;
- exact candidate identities fingerprint-bound;
- no paid provider constructed;
- API spend 0.

After:
- historical evidence byte-identical;
- Registry 0;
- A-TEXT not evaluated;
- fal not called.

Push exact tested/scientific HEAD.
Do not merge.
Return to Controller.
