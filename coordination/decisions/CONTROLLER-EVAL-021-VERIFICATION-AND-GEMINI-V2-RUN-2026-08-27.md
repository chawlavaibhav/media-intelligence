# Controller EVAL-021 Verification Acceptance and Gemini Contract-v2 Run — 2026-08-27

## Status

**EVAL-021 ACCEPTED AND INTEGRATED. GEMINI 3.5 FLASH-LITE CONTRACT-V2 QUALIFICATION IS AUTHORISED UNDER THE EXISTING EMP-001 SPEND CEILING.**

Integration:
- PR #44
- merge commit `045ccef9fd1a0629257ac6f3885320b1a3d6a7ff`

## Zero-spend verification accepted

Worker verification at branch head `ae31a2df9bf3c07361dc841fd35e594e67686f2c`:
- required five test files: 143 passed, 0 failed;
- targeted Gemini/schema/budget tests: 31 passed, 0 failed;
- malformed/A-TEXT/ambiguity filter tests: 73 passed, 0 failed;
- preflight: PREFLIGHT_GREEN, 8/8;
- all provider keys explicitly unset;
- external calls: 0;
- spend: USD 0;
- frozen Devanagari and Latin identities reproduced and verified;
- all prior EMP-001 evidence and ledger byte-identical.

Verification established:
1. top-level script `calls` = 288 primary transcribe calls;
2. `total_dispatches` = 576;
3. gates use blind transcribe only;
4. verdict remains diagnostic;
5. Gemini requests pin `thinkingLevel: minimal`;
6. Gemini billing counts `candidatesTokenCount + thoughtsTokenCount`;
7. documented empty `finishReason=MAX_TOKENS` is a well-formed model/evaluator error, not transport ambiguity;
8. truly malformed no-text/no-finishReason responses still fail closed;
9. dispatch pacing works without retries;
10. cumulative conservative Gemini budget fits the existing qualification cap;
11. A-TEXT remains blocked without both scripts;
12. historical evidence remains unchanged.

## Sonnet disposition

Anthropic `claude-sonnet-5` remains **DISQUALIFIED** under contract v2 for Devanagari exact-text judging:
- 20 blind false passes / 144 mismatch opportunities;
- 7 unique false-pass items;
- stable silent auto-correction behavior;
- clean complete screen;
- not an infrastructure failure.

Do not rerun Sonnet in EMP-001 unless separately authorised.

## Authorised Gemini run

Candidate:
- Google `gemini-3.5-flash-lite` only.

Contract:
- qualification contract v2;
- blind `transcribe` decides qualification;
- target-aware `verdict` is diagnostic only;
- numerical thresholds unchanged:
  - mismatch false pass max 0;
  - match false-fail rate max 0.10;
  - refusal rate max 0.05;
  - repeat consistency min 0.95.

Protocol:
- Devanagari from call 1;
- 96 items;
- transcribe + verdict;
- 3 repeats;
- 576 total Devanagari dispatches;
- Latin only if primary Devanagari transcribe gate passes;
- retries 0;
- same frozen prompts, images, scoring and reviewed materials;
- use same persistent EMP-001 ledger;
- preserve all prior evidence;
- write a new human-readable Gemini result and canonical fingerprint-bound `qualification-result.json`.

Operational pacing:
- serial execution;
- minimum **7 seconds between Gemini dispatch starts**;
- no retries;
- on HTTP 429 or any other true ambiguous post-dispatch failure: count/persist, do not retry, stop.

## Spend

Already-counted qualification spend: **USD 0.5016018**.

Conservative Gemini reservation:
- USD 0.000760 per call;
- max 1,152 calls if both scripts complete;
- max Gemini reservation: **USD 0.875520**.

Cumulative worst case:
- **USD 1.3771218**, below the existing USD 6 qualification sub-cap.

This is within the user's existing bounded EMP-001 approval. No additional spend approval is required.

## Stop boundary

- If Devanagari primary gate fails: stop before Latin.
- If Devanagari primary gate passes: run Latin automatically.
- If both scripts pass: stop before A-TEXT and return to Controller.
- No Haiku, Sonnet or fal calls in this run.
- A-TEXT remains blocked pending a judge qualified on both scripts.
