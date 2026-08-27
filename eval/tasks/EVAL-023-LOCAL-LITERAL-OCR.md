# EVAL-023 — Local Literal OCR Qualification

**Owner:** Eval worker  
**Authority:** `coordination/decisions/CONTROLLER-EVAL-022-LIVE-RESULTS-AND-EVAL-023-2026-08-27.md`  
**API spend:** USD 0  
**Paid provider calls:** 0

## Objective

Test whether a deliberately literal OCR configuration can avoid the stable auto-correction failure
seen in Sonnet, Gemini and Cloud Vision.

Candidate:
- local Tesseract 5.x;
- official Hindi + English traineddata;
- lexical/dictionary aids disabled;
- raw-line segmentation;
- same OCR-family qualification contract.

This is a scientific qualification run, not merely readiness. If implementation verification is green,
run the full local qualification in the same pass.

## First: environment + provenance

1. Read current `origin/main` and the authoritative decision.
2. Use the merged EVAL-022 OCR-family runner/contract as the base.
3. Check `tesseract --version`.
4. Require Tesseract 5.x.
5. Use project-local official `tessdata_best` `hin.traineddata` and `eng.traineddata`.
6. Pin and persist:
   - Tesseract exact version/build;
   - tessdata source repository + exact resolved commit/tag;
   - SHA-256 of `hin.traineddata`;
   - SHA-256 of `eng.traineddata`.
7. Do not commit traineddata binaries.
8. If Tesseract is absent and Homebrew is available, installing the current stable `tesseract`
   package is authorised as a zero-API-cost development dependency. Do not install unrelated packages.
9. If official traineddata must be downloaded, fetch only those two files into a gitignored local cache.
10. No Gemini, Cloud Vision, Anthropic, fal or other paid API call.

## Frozen candidate configuration

Freeze this before looking at qualification results:

- family: `ocr`;
- provider: `local_tesseract`;
- candidate alias: `tesseract5-hin-eng-literal-psm13-v1`;
- languages: `hin+eng`;
- `--oem 1`;
- `--psm 13`;
- one fresh Tesseract process per image/trial;
- original frozen rendered PNG as input; no adaptive preprocessing added;
- no target/ground-truth in invocation, environment, temp filename or config;
- no user words;
- retries 0;
- lexical DAWG controls:
  - `load_system_dawg=0`
  - `load_freq_dawg=0`
  - `load_unambig_dawg=0`
  - `load_bigram_dawg=0`
  - `load_punc_dawg=0`
  - `load_number_dawg=0`

Use `--tessdata-dir` pointed at the pinned project-local traineddata cache.

Do not silently change PSM, OEM, languages, traineddata, preprocessing or DAWG flags after seeing results.

## Why this configuration

The experiment targets the observed mechanism, not generic OCR accuracy.

Official Tesseract documentation states:
- PSM 13 treats input as a raw single text line while bypassing Tesseract-specific hacks;
- dictionaries can be disabled, and disabling dictionary support can improve recognition when the
  desired text is not ordinary dictionary text.

The controlled mismatches are intentionally often non-words, so dictionary correction is exactly
the prior we want to remove.

## Adapter / evidence

Add a local Tesseract OCR adapter behind an injected subprocess seam.

Per trial persist:
- item id;
- script;
- pass/repeat;
- expected label;
- observed label;
- target;
- rendered string;
- raw Tesseract stdout transcription;
- stderr/exit status;
- failure class/group/edit detail;
- image SHA;
- Tesseract version;
- traineddata hashes;
- PSM/OEM/languages;
- every DAWG flag;
- provider/config identity;
- elapsed time if convenient;
- cost USD 0;
- retries 0.

Target must not enter the subprocess command or file path. Add a mechanical blindness test.

A subprocess execution error is infrastructure failure and follows the accepted OCR taxonomy:
- persist;
- stop fail-closed;
- script scientifically incomplete;
- no scientific gate effect;
- retries 0.

A successful Tesseract invocation with empty stdout is scientific `empty_transcription`.

## Qualification

Use existing OCR contract `ocr-1` without threshold changes:

- mismatch false passes max 0;
- match false-fail rate max 0.10;
- empty-transcription rate max 0.05;
- repeat consistency min 0.95;
- 3 repeats;
- Devanagari first;
- Latin only if Devanagari passes.

Expected maximum:
- Devanagari 288 local executions;
- Latin +288 only for a survivor;
- total 576 local executions;
- API spend USD 0.

Write:
- provider-specific human-readable result, e.g.
  `qualification-live-tesseract5-literal-v1.json`;
- canonical OCR-family evidence `ocr-qualification-result.json`.

Preserve all prior human-readable empirical artifacts byte-identically.
Ledger should record no paid-provider spend for this local candidate.

## Required zero-spend controls before scientific run

Prove:
1. exact Tesseract version and traineddata hashes are bound into config fingerprint;
2. target cannot enter command, stdin, temp path or environment supplied by adapter;
3. fresh subprocess per trial;
4. all six lexical DAWG flags are set to 0;
5. PSM 13 and OEM 1 are pinned;
6. clean fake subprocess can complete 576 calls and qualify;
7. empty stdout is scientific `empty_transcription`;
8. nonzero exit/timeout/malformed local execution is infrastructure and yields incomplete/null;
9. retries remain 0;
10. fingerprint tampering is detected;
11. A-TEXT remains blocked for OCR family;
12. Registry remains 0;
13. existing tests/preflight remain green;
14. external paid API calls 0 / API spend USD 0.

If any required verification fails, do not run the scientific Tesseract battery.

## Final report

Return:
- branch/head;
- Tesseract version;
- traineddata source commit/tag and hashes;
- exact frozen command/config;
- tests/preflight;
- Devanagari metrics;
- Latin metrics if reached;
- false-pass items and classes;
- false-fail items;
- empty-transcription items;
- repeat consistency;
- infrastructure failures;
- comparison against Cloud Vision and Gemini;
- execution time;
- API spend USD 0;
- evidence paths/fingerprints;
- historical evidence SHA comparison;
- Registry/A-TEXT confirmation.

Do not merge. Return to Controller.
