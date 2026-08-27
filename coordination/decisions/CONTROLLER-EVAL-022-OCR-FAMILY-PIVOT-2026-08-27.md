# Controller EVAL-022 — OCR-Family Pivot After VLM Auto-Correction — 2026-08-27

## Status

**OPEN A BOUNDED ZERO-SPEND OCR-FAMILY READINESS PASS. NO NEW PAID PROVIDER CALLS ARE AUTHORISED YET. A-TEXT REMAINS BLOCKED.**

## Accepted Gemini disposition

Google `gemini-3.5-flash-lite` completed the full contract-v2 PRIMARY Devanagari transcribe screen before a later diagnostic 429.

Primary blind transcribe:
- 288/288 calls complete;
- 144 match / 144 mismatch opportunities;
- false passes: **18** across **7 unique items**;
- false-pass rate: 0.125;
- false fails: 16;
- match false-fail rate: 0.1111;
- repeat consistency: 0.9375;
- refusals: 0;
- failed gates: `mismatch_false_pass`, `match_false_fail_rate`, `repeat_consistency`.

A later diagnostic verdict call stopped on HTTP 429 at total dispatch 486/576. The diagnostic shape was incomplete (198/288).

Controller disposition:
- **Gemini 3.5 Flash-Lite is DISQUALIFIED for EMP-001 exact-text qualification.**
- This is a scientific disqualification because every qualifying primary observation was already complete and the primary gate had irreversibly failed.
- The incomplete diagnostic weakens only the transcribe-vs-verdict analysis. It cannot rescue qualification and is not worth completing.
- Do not spend more calls finishing Gemini diagnostic coverage.

Incremental Gemini qualification spend: USD 0.1696397.
Cumulative EMP-001 qualification spend: **USD 0.6712415**.

## Family-level empirical finding

General-purpose multimodal language models show the wrong failure mode for this judge role.

Observed under the current programme:
- Haiku 4.5: pooled-v1 failure;
- Sonnet 5 contract-v2: 20 blind false passes across 7 unique items;
- Gemini 3.5 Flash-Lite contract-v2: 18 blind false passes across 7 unique items.

Sonnet and Gemini both repeatedly returned the intended/correct Hindi word instead of the corrupted
word actually rendered. Several false-pass items overlap across the two models.

Controller interpretation:
- this is stable **semantic auto-correction / normalization**;
- it is exactly the dangerous behavior the zero-false-pass gate is designed to catch;
- do **not** relax the gate;
- do **not** keep cycling through general-purpose VLMs without new evidence that a different family
  addresses the failure mechanism.

For EMP-001, general-purpose multimodal LLMs are now **frozen as the primary exact-text judge family**.
A new LLM candidate requires a separate Controller decision.

## Next family: purpose-built OCR

Open EVAL-022 as a zero-spend readiness pass for a purpose-built OCR evaluator.

First external candidate to prepare:
- **Google Cloud Vision API — TEXT_DETECTION**.

Why this is a legitimate next family:
- Cloud Vision exposes dedicated OCR rather than a generative language-model response;
- Google documents Hindi (`hi`) / Devanagari support;
- `TEXT_DETECTION` is optimized for sparse text in images, matching the current single-word /
  short-line battery better than dense-document OCR;
- Cloud Vision supports API-key authentication;
- current public pricing: first 1,000 Text Detection units/month free, then USD 1.50 / 1,000 units.
  Do not assume the free tier is unused; any later live authorisation must budget against paid price.

Verified 27 Aug 2026:
- https://docs.cloud.google.com/vision/docs/languages
- https://docs.cloud.google.com/vision/docs/features-list
- https://docs.cloud.google.com/vision/docs/request
- https://docs.cloud.google.com/vision/product-search/docs/auth
- https://cloud.google.com/vision/pricing

## OCR qualification semantics

Do **not** force the LLM `verdict` shape onto an OCR engine.

EVAL-022 must prepare a separate OCR-family qualification contract rather than mutating or
reinterpreting `qualification-contract-v2.yaml`.

Proposed OCR contract principles:
1. primary measurement is OCR transcription only;
2. target is never sent to the OCR provider;
3. exactness is decided locally in code using the existing NFC + surrounding-whitespace rule;
4. zero mismatch false passes remains the safety gate;
5. match false-fail max remains 0.10 unless a future Controller decision changes it;
6. refusal/error rate max remains 0.05;
7. 3 repeats remain for initial qualification so service variability is measurable rather than assumed absent;
8. Devanagari first; Latin only for survivors;
9. no target-aware diagnostic shape is fabricated for a service that does not have one;
10. outcomes, provider request identity where available, image hash, response text, cost, and exact
    provider configuration are persisted and fingerprint-bound;
11. a missing/empty OCR transcription on a known-visible text image is an evaluator failure, not a
    silent match;
12. no OCR evidence may open A-TEXT unless the A-TEXT handoff explicitly accepts the new OCR-family
    contract and the candidate qualified for every required script.

This is a family-specific instrument, not a relaxation of the LLM contract.

## Exact Cloud Vision configuration to prepare

- endpoint: `POST https://vision.googleapis.com/v1/images:annotate`;
- feature: `TEXT_DETECTION`;
- one rendered PNG per trial;
- base64 image content;
- **no `languageHints` in the initial candidate**. Google documents that omitting hints usually
  yields the best general OCR behavior and allows automatic detection; adding a Hindi hint would be
  a separate candidate configuration, not a silent runtime tweak;
- API auth from a dedicated local env var, proposed:
  `GOOGLE_CLOUD_VISION_API_KEY`;
- do not reuse or print credential values;
- retries 0.

## EVAL-022 zero-spend implementation/readiness scope

Prepare, test and report only. Make zero external provider calls.

Required:
1. create a new OCR-family qualification contract; do not edit v1 or v2 historical contracts;
2. add a Cloud Vision TEXT_DETECTION adapter behind an injected HTTP seam;
3. keep target out of the provider request and add a mechanical blindness test;
4. parse OCR transcription deterministically;
5. persist enough per-trial evidence to analyse false-pass items by failure class;
6. bind OCR contract/config/outcomes/call records into the qualification fingerprint;
7. prepare a progressive Devanagari -> Latin runner for OCR candidates;
8. A-TEXT must reject OCR evidence until its handoff explicitly understands and accepts the OCR-family contract;
9. add current pricing/reservation logic using USD 1.50 / 1,000 images as the conservative paid basis;
10. prove the prospective maximum paid cost without relying on the free tier:
    - 96 items × 3 repeats × 2 scripts = 576 OCR image calls;
    - 576 × USD 0.0015 = **USD 0.864**;
    - current cumulative qualification spend USD 0.6712415;
    - prospective cumulative = **USD 1.5352415 <= USD 6**;
11. zero-spend fake-live must exercise all 576 calls for a clean two-script candidate;
12. preserve all current empirical evidence and Registry state;
13. no Cloud Vision, Gemini, Anthropic, fal or other external call in EVAL-022 readiness.

## Paid execution boundary

EVAL-022 readiness does **not** authorise a live Cloud Vision run.

After the zero-spend implementation returns, Controller will review:
- contract semantics;
- exact provider configuration;
- test evidence;
- credential/setup requirements;
- whether Cloud Vision live qualification is authorised.

A-TEXT remains blocked.
Registry remains unchanged.
