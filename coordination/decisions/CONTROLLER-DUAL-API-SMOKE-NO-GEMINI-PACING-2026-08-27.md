# Controller Override — Dual API Smoke + No Mandatory Gemini Pacing — 2026-08-27

## Status

**USER OVERRIDE ACCEPTED. TEST BOTH GEMINI API AND GOOGLE CLOUD VISION API LIVE. REMOVE THE 7-SECOND GEMINI PACING REQUIREMENT. KEEP THE EXISTING USD 1.00 INCREMENTAL CAP.**

This decision supersedes any prior Controller instruction requiring a minimum 7-second interval for Gemini dispatches.

It also extends the already-authorised combined EVAL-022 pass to include one bounded live Gemini API smoke call and one bounded live Cloud Vision API smoke call before the full OCR qualification.

## Scientific state does not change

Anthropic Sonnet 5 and Google Gemini 3.5 Flash-Lite remain scientifically disqualified as EMP-001 Devanagari exact-text judges based on their completed primary screens.

The Gemini smoke call below is **connectivity/infrastructure evidence only**. It must not:
- reopen Gemini qualification;
- alter its prior gate metrics;
- enter the Capability Registry;
- open A-TEXT;
- be described as a scientific rerun.

## Mandatory pacing override

For the Gemini smoke:
- minimum dispatch interval requirement = **0 seconds**;
- no artificial sleep is required;
- retries remain 0.

The optional pacing capability may remain in code, but no Controller rule requires 7 seconds anymore.

## Sequence

### Phase A — finish live OCR runner wiring at zero spend

First complete the already-recorded correction:
`coordination/decisions/CONTROLLER-EVAL-022-LIVE-RUNNER-WIRING-CORRECTION-2026-08-27.md`

All required zero-network tests and preflight must pass before any external call.

If verification fails: stop with spend USD 0.

### Phase B — live Gemini API smoke

If zero-spend verification is fully green:
- use existing `GOOGLE_API_KEY`;
- use exact model `gemini-3.5-flash-lite`;
- one request only;
- use the existing blind-transcription adapter on one frozen Devanagari battery image;
- `thinkingLevel: minimal`;
- no target in provider payload;
- minimum dispatch interval 0;
- retries 0.

Persist separately as **connectivity_smoke_only** with:
- provider/model/config;
- item/image SHA;
- request identity;
- response status;
- transcription if returned;
- billing;
- ambiguity status.

This smoke call does not contribute to scientific qualification metrics.

Conservative reserve:
- USD 0.000760 max for the single Gemini smoke call.

On provider/API/429/transport/malformed failure:
- persist one smoke result;
- no retry;
- continue to Cloud Vision smoke only if the failure is a clean provider response and doing so does not compromise budget/state;
- if dispatch/billing state is ambiguous, stop the combined pass fail-closed.

### Phase C — live Cloud Vision API smoke

Run exactly one connectivity smoke call:
- Google Cloud Vision;
- `TEXT_DETECTION`;
- no `languageHints`;
- one frozen Devanagari battery PNG;
- target never sent;
- retries 0;
- dedicated `GOOGLE_CLOUD_VISION_API_KEY`.

Persist separately as **connectivity_smoke_only**.

Conservative reserve:
- USD 0.0015.

If the Cloud Vision smoke returns a clean successful provider execution, proceed to Phase D.

If it returns provider/API/quota/backend/transport/malformed failure:
- persist;
- retries 0;
- stop before scientific OCR qualification.

The smoke result must not be reused as a scientific qualification observation. The qualification starts fresh from Devanagari call 1.

### Phase D — live Cloud Vision qualification

If Phases A-C are green:
- run the full already-authorised OCR contract-v1 qualification;
- Devanagari: 96 items × 3 repeats = 288 scientific calls;
- Latin only if Devanagari scientifically passes;
- max scientific OCR qualification calls = 576;
- retries 0;
- same frozen images/materials/normalization;
- no language hints;
- A-TEXT remains blocked even if both scripts qualify.

## Spend

Current cumulative EMP-001 qualification spend:
- USD 0.6712415.

New incremental per-step user cap:
- **USD 1.00 total across BOTH smoke calls + OCR qualification**.

Conservative maximum incremental reservation:
- Gemini smoke: USD 0.000760;
- Cloud Vision smoke: USD 0.001500;
- full OCR qualification: USD 0.864000;
- total maximum incremental: **USD 0.866260**.

This is below the user's USD 1.00 cap.

Prospective cumulative EMP-001 qualification-related spend:
- USD 0.6712415 + USD 0.866260 = **USD 1.5375015**.

This remains below the existing USD 6 qualification sub-cap and USD 10 total EMP-001 ceiling.

No free-tier assumption.

## Evidence / ledger rules

Both smoke calls:
- one call = one trial;
- persist separately from scientific qualification;
- append to the same durable EMP-001 spend ledger;
- never mutate previous evidence;
- clearly mark `evidence_class: connectivity_smoke_only`;
- `may_populate_registry: false`;
- `may_open_atext: false`.

Scientific OCR qualification remains governed only by OCR contract-v1.

## Branch / execution requirement

The OCR branch must first include the final live-runner wiring correction and current `origin/main`, pass all zero-network tests, and be pushed at the exact tested HEAD.

After that, the worker may immediately execute Phases B-D from that exact pushed/tested HEAD without another Controller round-trip.

Do not merge.
Do not call fal.
A-TEXT remains blocked.
Registry remains unchanged.
