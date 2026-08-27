# EVAL-022 — OCR-Family Qualification Readiness

**Owner:** Eval worker  
**Authority:** Controller decision `coordination/decisions/CONTROLLER-EVAL-022-OCR-FAMILY-PIVOT-2026-08-27.md`  
**Spend:** USD 0 only  
**External provider/model calls:** 0

## Objective

Prepare a purpose-built OCR evaluator family for EMP-001 after general-purpose multimodal LLMs
showed stable semantic auto-correction of corrupted Devanagari.

First candidate configuration to prepare:
- Google Cloud Vision API
- feature `TEXT_DETECTION`
- no language hints
- dedicated local env var `GOOGLE_CLOUD_VISION_API_KEY`
- retries 0

Do not call Google Cloud Vision during this task.

## Required implementation

1. Add a new OCR-family qualification contract without editing the historical LLM contracts v1/v2.
2. OCR qualification is transcription-only; do not invent a target-aware verdict shape.
3. Use the same code-level exactness normalization currently frozen: NFC + surrounding whitespace trim.
4. Keep zero mismatch false passes as the safety gate.
5. Keep match false-fail max 0.10, evaluator refusal/error max 0.05, and 3 repeats for the first OCR qualification contract unless the Controller later changes them.
6. Run Devanagari first; Latin only for survivors.
7. Build a Cloud Vision REST adapter with an injected HTTP seam:
   - `POST https://vision.googleapis.com/v1/images:annotate`
   - `TEXT_DETECTION`
   - base64 PNG
   - no target or ground-truth string in request body
   - no `languageHints`
8. Add mechanical blindness tests proving target text cannot reach the request.
9. Parse OCR text deterministically and preserve the provider's response/request identity where exposed.
10. Treat no usable text on a known-visible text image as evaluator failure; never coerce it to match.
11. Persist per-trial:
    - item id
    - repeat
    - expected label
    - observed label
    - target
    - rendered string
    - OCR response text
    - failure class/group/edit detail
    - image SHA
    - provider/API identity/config
    - provider request id if available
    - status/error
    - cost basis
12. Fingerprint-bind the OCR-family contract/config, outcomes and call records.
13. Prepare the A-TEXT handoff to recognize OCR-family evidence only after a future Controller authorises it; in this task it must remain blocked.
14. Add conservative pricing:
    - USD 1.50 / 1,000 Text Detection images
    - reserve USD 0.0015/image
    - do not rely on first-1,000-free pricing for safety
15. Prove:
    - complete Devanagari = 96 × 3 = 288 OCR calls
    - complete Latin = 288 additional
    - maximum = 576 calls
    - max planned OCR reservation = USD 0.864
    - current prior qualification spend = USD 0.6712415
    - prospective cumulative = USD 1.5352415 <= USD 6
16. Fake-live positive control must complete both scripts at zero network/spend.
17. Negative controls must cover:
    - target leakage
    - missing API key before dispatch
    - malformed response
    - provider error
    - budget exhaustion
    - evidence tampering
    - old/wrong contract at A-TEXT boundary
    - retries remain 0
18. Preserve all current empirical evidence byte-identically and Registry at 0.

## Verification

Run focused OCR-family tests plus the existing qualification/handoff tests touched by the change.
Run preflight with all provider keys unset.

Report:
- exact branch/head
- changed files
- contract summary
- fake-live call counts
- false-pass/false-fail synthetic controls
- fingerprint/tamper controls
- max-cost arithmetic
- external calls 0
- spend USD 0
- previous evidence fingerprints unchanged
- git status

## Stop

Do not merge.
Do not make a live Cloud Vision call.
Do not alter LLM qualification history.
Return to Controller.
