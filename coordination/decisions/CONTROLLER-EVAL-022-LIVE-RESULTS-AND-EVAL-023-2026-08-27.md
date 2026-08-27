# Controller EVAL-022 Live Results — Gemini Repeat, Cloud Vision, and Literal-OCR Next Step — 2026-08-27

## Status

**EVAL-022 ACCEPTED AND INTEGRATED. GEMINI 3.5 FLASH-LITE REMAINS DISQUALIFIED. GOOGLE CLOUD VISION TEXT_DETECTION IS DISQUALIFIED IN ITS UNHINTED CONFIGURATION. NEXT: ZERO-API-COST LITERAL OCR WITH LEXICAL AIDS DISABLED.**

Integration:
- PR #45
- merge commit `afe866cea4adc7625e1ee306ed93f396432a9212`

Worker live/tested head:
- `427d30eecd8bd444babb141cf2118cae7729c701`

## Accepted verification

Before live execution:
- 436 tests passed, 0 failed;
- OCR-focused suite: 47 tests;
- preflight: PREFLIGHT_GREEN 8/8;
- zero-network OCR proof passed with socket / create_connection / getaddrinfo blocked;
- historical EMP-001 evidence byte-identical;
- OCR live runner used the persistent EMP-001 qualification stage budget;
- retries 0.

## Gemini 3.5 Flash-Lite repeat qualification

Configuration:
- exact model `gemini-3.5-flash-lite`;
- `thinkingLevel: minimal`;
- mandatory pacing: **0 seconds**;
- contract v2;
- retries 0.

Devanagari:
- 576/576 total dispatches;
- zero errors;
- zero 429s;
- zero ambiguous dispatches.

Primary blind transcribe:
- 288 calls;
- false passes: **16** across **8 unique items**;
- false-pass rate: 0.1111;
- false fails: 13;
- match false-fail rate: 0.0903;
- refusals: 0;
- repeat consistency: **0.9167**;
- failed gates:
  - `mismatch_false_pass`;
  - `repeat_consistency`.

Latin correctly not run.

Controller disposition:
- **Gemini 3.5 Flash-Lite remains DISQUALIFIED.**
- This is now reinforced by a second independent complete contract-v2 Devanagari screen.
- The earlier 7-second pacing requirement is permanently withdrawn for this experiment family; the clean no-pacing run demonstrates that the prior 429 was not a reproducible scientific requirement for qualification.
- Do not rerun Gemini again in EMP-001 absent a new model/version or new Controller decision.

## Google Cloud Vision TEXT_DETECTION

Exact configuration:
- provider: Google Cloud Vision;
- feature: `TEXT_DETECTION`;
- no `languageHints`;
- target never sent;
- OCR contract `ocr-1`;
- retries 0.

Devanagari:
- 288/288 calls complete;
- scientific executions: 288;
- infrastructure failures: 0;
- false passes: **18** across **6 unique items**;
- false-pass rate: 0.125;
- false fails: 3 across 1 item;
- match false-fail rate: 0.0208;
- empty transcriptions: 0;
- repeat consistency: **1.0**;
- failed gate: `mismatch_false_pass` only.

All six false-pass items false-passed in all three repeats. The observed behavior is stable normalization / correction toward a plausible intended Hindi word.

Controller disposition:
- **Cloud Vision TEXT_DETECTION, no-language-hints configuration is DISQUALIFIED** for EMP-001 exact-text judging.
- It is the strongest candidate tested so far on consistency, false-fail cost, and infrastructure stability, but it still fails the safety-critical zero-false-pass gate decisively.
- Do not relax the gate.

## Why NOT test `languageHints: ["hi"]` next

The only observed Vision failure plausibly attributable to script/language detection is one correct Devanagari item (`dx-0072`, target `भाऊ`) read as Gurmukhi. That creates a false fail.

Vision already passes the false-fail gate comfortably (0.0208 <= 0.10).

The decisive failure is instead:
- 18 mismatch false passes;
- 6 unique corrupted Hindi items;
- every one repeated 3/3.

A Hindi language hint is designed to bias language/script interpretation. There is no current evidence that it addresses the decisive literalness/normalization failure, and making the recognizer more Hindi-aware could plausibly strengthen rather than weaken lexical normalization.

Therefore:
- **do not spend USD 0.432 on a hinted Cloud Vision rerun now**;
- a hinted configuration remains a legitimate future candidate only if evidence specifically suggests it can reduce false passes.

## Family-level finding

Across complete primary screens:
- Sonnet 5: silent auto-correction;
- Gemini 3.5 Flash-Lite: silent auto-correction, twice independently;
- Cloud Vision TEXT_DETECTION: silent auto-correction/normalization.

The problem is no longer "generative LLMs are too smart." It is broader:
**modern OCR/VLM systems commonly use lexical/language priors that can repair corrupted words.**

For this product, recognition accuracy on ordinary valid text is not enough. The evaluator must be intentionally optimized for **literal glyph fidelity under adversarial misspelling**.

## Next experiment: local Tesseract literal configuration

Open EVAL-023 as a **zero API spend** candidate using Tesseract with lexical/dictionary aids disabled.

Rationale:
- the repository's historical Tesseract `hin` 0/14 result is explicitly unverified because no supporting artifact exists;
- the accepted calibration plan already says deterministic Devanagari OCR should be re-tested rather than assumed absent;
- official Tesseract documentation says dictionary use can be disabled and that doing so can improve recognition for non-dictionary text;
- official Tesseract page segmentation supports raw/single-line modes suitable for the frozen word/short-line battery.

Primary candidate configuration to freeze before seeing results:
- Tesseract 5.x;
- official `hin` + `eng` traineddata;
- one fresh process per image/trial;
- OCR engine mode LSTM where supported;
- page segmentation: `--psm 13` (raw line, bypassing Tesseract-specific line hacks);
- languages: `hin+eng`;
- disable lexical DAWGs:
  - `load_system_dawg=0`;
  - `load_freq_dawg=0`;
  - `load_unambig_dawg=0`;
  - `load_bigram_dawg=0`;
  - `load_punc_dawg=0`;
  - `load_number_dawg=0`;
- no user word list;
- no target in OCR invocation;
- retries 0.

This candidate is chosen mechanistically to attack the observed failure mode, not because it has been tried on the qualification battery.

Public basis verified 27 Aug 2026:
- Tesseract tessdoc: page segmentation mode 13 is raw line, and dictionaries can be disabled;
- Tesseract control parameters expose DAWG-loading controls.

## EVAL-023 boundaries

- API spend: USD 0;
- do not call Gemini, Cloud Vision, Anthropic or fal;
- may use local CPU only;
- preserve current OCR contract and historical evidence;
- candidate configuration must be fingerprinted, including Tesseract version, traineddata hashes, languages, PSM, OEM and every lexical-control flag;
- use the existing OCR-family qualification semantics;
- Devanagari first, Latin only for survivors;
- 3 repeats;
- if Tesseract qualifies both scripts, stop before A-TEXT and return to Controller;
- no Registry population.

Current cumulative paid qualification spend remains:
- **USD 1.3037905**.

A-TEXT remains blocked.
