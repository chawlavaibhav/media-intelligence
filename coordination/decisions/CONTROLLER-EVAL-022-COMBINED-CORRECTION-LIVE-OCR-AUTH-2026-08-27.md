# Controller EVAL-022 Combined Correction + Live OCR Authorisation — 2026-08-27

## Status

**CONDITIONALLY AUTHORISED AS ONE PASS: ZERO-SPEND OCR TAXONOMY CORRECTION + VERIFICATION, THEN LIVE GOOGLE CLOUD VISION QUALIFICATION IF AND ONLY IF ALL GATES ARE GREEN.**

The user explicitly approved spending up to **USD 1.00** on this combined OCR step.

This does not increase the existing EMP-001 global ceilings:
- total consumed API ceiling remains USD 10.00;
- qualification sub-cap remains USD 6.00;
- retries remain 0;
- no account prefunding above the existing approved ceiling.

This decision supersedes the earlier EVAL-022 instruction that required another Controller round-trip before any live Cloud Vision call.

## Combined-pass sequence

### Phase 1 — zero-spend correction

Apply exactly:
`coordination/decisions/CONTROLLER-EVAL-022-OCR-FAILURE-TAXONOMY-CORRECTION-2026-08-27.md`

Required scientific semantics:
- successful provider execution + no usable OCR transcription on a validated visible-text image
  = scientific evaluator failure;
- count it only toward `empty_transcription_rate`;
- `empty_transcription_rate_max: 0.05`;
- provider/API/backend/quota/transport/malformed execution failures are infrastructure failures;
- infrastructure failure stops fail-closed, leaves current script scientifically incomplete, and
  does not increment false-pass, false-fail, or empty-transcription scientific metrics;
- no infrastructure failure may yield scientific `passed: true` or `passed: false`;
- retries 0.

### Phase 2 — mandatory zero-spend verification

Before any live dispatch:
1. all focused OCR tests pass;
2. all affected existing qualification/handoff tests pass;
3. preflight green;
4. all provider keys except the local Cloud Vision key may remain unset;
5. external calls during verification = 0;
6. spend during verification = USD 0;
7. clean fake-live completes 576 OCR calls and qualifies both scripts;
8. infrastructure-stop negative controls pass;
9. empty-transcription scientific-failure control passes;
10. all historical EMP-001 evidence and Registry remain byte-identical.

If ANY required verification fails:
- stop;
- do not make a live Cloud Vision call;
- return evidence to Controller.

### Phase 3 — push and live execution

If and only if Phase 2 is fully green:
1. push the corrected branch to origin so the exact live code is durable and inspectable;
2. do not merge;
3. confirm pushed HEAD equals local tested HEAD;
4. confirm local `GOOGLE_CLOUD_VISION_API_KEY` exists without printing it;
5. run the live OCR qualification from that exact pushed/tested HEAD.

The live run is authorised even though the branch is not yet merged, because the user explicitly
requested collapsing correction + verification + bounded execution into one pass. Merge remains a
Controller action after the evidence returns.

## Live OCR candidate

Provider:
- Google Cloud Vision API.

Configuration:
- endpoint `POST https://vision.googleapis.com/v1/images:annotate`;
- feature `TEXT_DETECTION`;
- no `languageHints`;
- one rendered PNG per trial;
- target never sent to provider;
- dedicated env var `GOOGLE_CLOUD_VISION_API_KEY`;
- retries 0.

OCR qualification contract:
- transcription only;
- local exact comparison after NFC + surrounding-whitespace trim;
- mismatch false-pass max 0;
- match false-fail rate max 0.10;
- empty-transcription rate max 0.05;
- repeat consistency min 0.95;
- Devanagari first;
- Latin only if Devanagari scientifically qualifies.

## Spend

Current cumulative EMP-001 qualification spend:
- **USD 0.6712415**.

Conservative OCR price basis:
- USD 0.0015 per image;
- do not rely on free tier.

Maximum authorised OCR protocol:
- Devanagari: 96 items × 3 repeats = 288 calls;
- Latin if Devanagari passes: 288 additional;
- total maximum = 576 calls;
- maximum OCR reservation = **USD 0.864**.

User's new per-step cap:
- **USD 1.00**.

Therefore the frozen protocol itself is below the user-approved incremental cap.

Prospective cumulative qualification spend if all 576 OCR calls reserve at paid basis:
- **USD 1.5352415**.

This remains below the existing USD 6 qualification sub-cap and USD 10 total ceiling.

Do not add retries or any extra diagnostic calls.
Do not silently switch to a hinted OCR configuration.
Do not add another OCR provider in this pass.
Do not fund an account to enable the call.

## Live stop conditions

Stop immediately, persist evidence, and do not retry if:
- missing local key before dispatch;
- provider/API/backend/quota error;
- HTTP 429;
- transport timeout/reset;
- malformed post-dispatch response;
- budget refusal;
- any true infrastructure ambiguity.

Such a stop leaves the current script scientifically incomplete unless every required scientific
observation for that script had already completed before the infrastructure failure.

If Devanagari scientifically fails:
- stop before Latin.

If Devanagari scientifically passes:
- run Latin automatically.

If both scripts scientifically pass:
- stop before A-TEXT;
- do not call fal;
- return to Controller.

## Evidence requirements

Preserve all prior EMP-001 artifacts byte-identically.

Write a new OCR-family live result and canonical fingerprint-bound OCR qualification evidence with:
- contract family/version/hash;
- exact Cloud Vision config hash;
- item/repeat coordinates;
- target/rendered string;
- raw OCR transcription;
- expected/observed labels;
- failure class/group/edit detail;
- image SHA;
- provider/config identity;
- provider request id if exposed;
- status/error;
- actual/provisional cost;
- scientific completeness;
- gate metrics;
- call records;
- recomputable evidence fingerprint.

A-TEXT remains blocked even if OCR qualifies on both scripts. OCR-family handoff acceptance requires a later Controller decision after reviewing this live evidence.

Registry remains unchanged.
