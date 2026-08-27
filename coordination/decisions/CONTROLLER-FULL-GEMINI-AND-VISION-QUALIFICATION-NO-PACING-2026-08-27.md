# Controller Override — Full Gemini + Cloud Vision Qualification, No Gemini Pacing — 2026-08-27

## Status

**USER OVERRIDE ACCEPTED. RUN BOTH FULL QUALIFICATION PATHS: GEMINI 3.5 FLASH-LITE AND GOOGLE CLOUD VISION OCR. REMOVE THE 7-SECOND GEMINI PACING REQUIREMENT. NO SEPARATE SMOKE CALLS.**

This decision supersedes:
- the prior 7-second Gemini pacing requirement;
- the prior "Gemini connectivity smoke only" limitation in
  `CONTROLLER-DUAL-API-SMOKE-NO-GEMINI-PACING-2026-08-27.md`;
- the prior general freeze on additional Gemini qualification, for this one explicitly user-requested repeat only.

It does not reopen Sonnet or Haiku.

## Why no smoke calls

A complete qualification attempt already exercises:
- auth;
- network path;
- provider API;
- billing;
- parsing;
- persistence.

Separate smoke calls would add spend and create evidence that cannot answer the qualification question.
Therefore this override authorises the scientific runs directly after zero-spend readiness passes.

## Shared safety controls

Both provider runs:
- retries 0;
- preserve all prior evidence;
- append only to the persistent EMP-001 spend ledger;
- use exact frozen batteries/materials;
- no threshold, prompt, normalization or provider-config changes during execution;
- A-TEXT remains blocked;
- fal is not called;
- Registry remains unchanged.

An infrastructure failure in one provider stops **that provider's run only**.
The other provider may still run if:
- the failure is persisted;
- any ambiguous cost remains conservatively reserved;
- the persistent qualification budget remains mechanically below its ceiling.

This lets the user test both APIs without allowing one provider's outage to erase the other experiment.

## Run A — Gemini 3.5 Flash-Lite repeat qualification

Exact candidate:
- `gemini-3.5-flash-lite`;
- existing `GOOGLE_API_KEY`;
- explicit `thinkingLevel: minimal`;
- minimum mandatory dispatch interval: **0 seconds**;
- serial execution remains acceptable;
- retries 0.

Contract:
- VLM qualification contract v2;
- blind `transcribe` decides qualification;
- target-aware `verdict` remains diagnostic only;
- mismatch false-pass max 0;
- match false-fail rate max 0.10;
- refusal rate max 0.05;
- repeat consistency min 0.95.

Protocol:
- fresh Devanagari from call 1;
- 96 items × 2 shapes × 3 repeats = 576 total Devanagari dispatches;
- Latin only if Devanagari primary gate passes;
- maximum both scripts = 1,152 dispatches;
- no artificial sleep.

Evidence:
- write a new human-readable result, distinct from prior Gemini evidence;
- canonical VLM qualification evidence may be rewritten for the current run, but prior human-readable
  Gemini artifacts must remain byte-identical;
- use the same persistent ledger.

Scientific interpretation:
- Gemini already has one valid contract-v2 Devanagari failure.
- This new run is an independent repeat requested by the user.
- If it fails again: prior disqualification is reinforced.
- If it is infrastructure-incomplete: prior scientific disqualification remains unchanged.
- If it unexpectedly passes Devanagari and Latin: record that run-level contract pass, but do NOT
  silently promote Gemini to globally "qualified". The candidate then has conflicting complete-run
  evidence and must return to Controller for a drift/reproducibility disposition.
- In all cases A-TEXT remains blocked from Gemini by this override.

Gemini conservative maximum reservation:
- USD 0.000760/call × 1,152 = **USD 0.875520**.

## Run B — Google Cloud Vision OCR qualification

Precondition:
- first finish the already-recorded OCR live-runner wiring correction;
- zero-network tests/preflight must be fully green;
- exact tested branch head must be pushed before live execution.

Candidate:
- Google Cloud Vision API;
- `TEXT_DETECTION`;
- dedicated `GOOGLE_CLOUD_VISION_API_KEY`;
- no `languageHints`;
- target never sent;
- retries 0.

OCR contract:
- family `ocr`, contract `ocr-1`;
- transcription only;
- local NFC + surrounding-whitespace exactness;
- mismatch false-pass max 0;
- match false-fail rate max 0.10;
- empty-transcription rate max 0.05;
- repeat consistency min 0.95.

Protocol:
- fresh Devanagari from call 1;
- 96 items × 3 repeats = 288 calls;
- Latin only if Devanagari scientifically passes;
- maximum both scripts = 576 calls.

Scientific/infrastructure taxonomy remains:
- successful-but-empty OCR response = scientific `empty_transcription`;
- provider/API/quota/backend/transport/malformed failure = infrastructure;
- infrastructure failure stops that OCR run incomplete, persists billing evidence, and does not alter
  scientific gate metrics;
- missing key is pre-dispatch, zero calls, zero spend.

OCR conservative maximum reservation:
- USD 0.0015/call × 576 = **USD 0.864000**.

If OCR passes both scripts:
- record it as OCR-family qualification evidence;
- A-TEXT still remains blocked pending separate family-handoff review.

## Budget

Current cumulative EMP-001 qualification spend:
- **USD 0.6712415**.

Maximum new Gemini reservation:
- **USD 0.875520**.

Maximum new OCR reservation:
- **USD 0.864000**.

Maximum combined new reservation:
- **USD 1.739520**.

Prospective cumulative qualification spend:
- **USD 2.4107615**.

This exceeds the earlier temporary USD 1.00 OCR-step cap, but the user has now explicitly requested
both full qualification runs. The already-approved EMP-001 qualification ceiling remains **USD 6.00**,
so this combined full-qualification plan is mechanically within the standing authorised ceiling.

No account prefunding is authorised.

## Zero-spend readiness before live calls

Before either live run:
1. finish OCR `--live` persistent-ledger wiring;
2. bring current `origin/main` into the OCR branch;
3. all OCR and affected existing tests pass;
4. preflight green;
5. injected live-orchestration test proves 576 clean OCR calls without network;
6. live OCR canonical evidence persists and fingerprints correctly;
7. historical evidence is byte-identical;
8. pushed tested HEAD == local tested HEAD.

If zero-spend readiness fails:
- do not run either provider live.

## Execution order

Preferred:
1. Gemini full qualification, pacing 0;
2. Cloud Vision full OCR qualification.

Reason:
- Gemini live path is already mature and the user explicitly asked to retest it;
- OCR live path is newly added and separately verified before execution.

The order is operational only and does not change scientific interpretation.

## Stop boundaries

Gemini:
- provider/API/429/transport/malformed ambiguity => persist, no retry, stop Gemini run;
- still proceed to OCR if ledger/budget state is healthy.

OCR:
- infrastructure failure => persist, no retry, scientific disposition null for incomplete script;
- if Devanagari fails scientifically, stop before Latin;
- if Devanagari passes, run Latin automatically.

No A-TEXT.
No fal.
No Registry population.
