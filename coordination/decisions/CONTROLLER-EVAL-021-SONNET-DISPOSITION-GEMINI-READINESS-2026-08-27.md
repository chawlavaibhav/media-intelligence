# Controller EVAL-021 — Sonnet v3 Disposition and Gemini Contract-v2 Readiness — 2026-08-27

## Status

**SONNET 5 IS DISQUALIFIED UNDER CONTRACT V2. GEMINI 3.5 FLASH-LITE IS THE NEXT CANDIDATE, PENDING ZERO-SPEND EVAL-021 VERIFICATION. A-TEXT REMAINS BLOCKED.**

## Accepted Sonnet v3 empirical result

Worker-reported live evidence for Anthropic `claude-sonnet-5`, qualification contract v2:
- complete Devanagari screen: 576/576 total dispatches;
- primary blind `transcribe`: 288 calls;
- match / mismatch opportunities: 144 / 144;
- false passes: **20** across **7 unique mismatch items**;
- false-pass rate: 0.1389;
- false fails: 4;
- match false-fail rate: 0.0278;
- refusals: 0;
- repeat consistency: 0.9792;
- failed gate: `mismatch_false_pass` only;
- zero errors;
- zero ambiguous dispatches;
- retries 0;
- Latin not run;
- A-TEXT not run.

Diagnostic target-aware verdict:
- 288 calls;
- 9 false passes across 3 unique items;
- false-pass rate 0.0625;
- 3 false fails;
- repeat consistency 1.0.

Incremental Sonnet v3 spend: USD 0.190334.
Cumulative EMP-001 qualification spend after Sonnet v3: **USD 0.5016018**.

## Controller disposition: Sonnet 5

**DISQUALIFIED as an EMP-001 exact-text judge for Devanagari under contract v2.**

This is a scientific model result, not infrastructure failure and not a contract artifact.

The decisive failure mode is stable silent auto-correction: on corrupted rendered words the blind
transcription sometimes returns the intended/correct word rather than the text actually drawn.
Six of seven unique false-pass items repeated that behavior in all three repeats.

The zero-tolerance blind false-pass gate remains unchanged. This result is not a reason to relax it.

The diagnostic verdict shape happened to perform better than blind transcription in this run.
That contradicts any directional assumption that target exposure must make false passing worse, but
it does not invalidate the v2 instrument: verdict is diagnostic and the primary blind transcription
is correctly measuring whether the checker silently repairs wrong text.

## EVAL-021 zero-spend corrections before Gemini

1. Reporting schema:
   - top-level `calls` now means primary-shape calls;
   - `total_dispatches` reports all transcribe + verdict dispatches.
   This removes the v3 reporting ambiguity without changing any gate or historical result.

2. Gemini 3.5 Flash-Lite request reproducibility:
   - explicitly pin `thinkingLevel: minimal` in both qualification shapes.

3. Gemini billing correctness:
   - include `thoughtsTokenCount` in billed/provisional output-token accounting.

4. Gemini response taxonomy:
   - a documented empty response with `finishReason` is a well-formed evaluator/model error,
     not transport ambiguity;
   - a response with neither text nor a documented finish reason remains malformed/ambiguous.

5. Operational pacing:
   - add an optional minimum interval between evaluator dispatch starts;
   - no retries are introduced;
   - pacing does not change items, prompts, scoring, repeats, thresholds or trial identity.

## Why Gemini is next

The earlier Gemini attempt stopped after 17 calls on HTTP 429. It did not produce a scientific
qualification result.

Google's current documentation confirms:
- `gemini-3.5-flash-lite` is a stable multimodal model optimized for cost-efficient high-volume
  tasks and simple data processing;
- paid standard pricing is USD 0.30/M input tokens and USD 2.50/M output tokens;
- Gemini 3.5 Flash-Lite uses thinking at the `minimal` level by default;
- thinking tokens are billed as output;
- rate limits are project-level and a 429 is returned when a limit is exceeded; active limits vary
  by project/tier.

Public sources verified 27 Aug 2026:
- https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite
- https://ai.google.dev/gemini-api/docs/pricing
- https://ai.google.dev/gemini-api/docs/thinking
- https://ai.google.dev/gemini-api/docs/rate-limits

## Budget

Already-counted qualification spend: USD 0.5016018.

Conservative Gemini reservation remains USD 0.000760 per call.

Maximum if Gemini survives both scripts:
- 1,152 calls;
- USD 0.875520 reservation.

Cumulative worst case:
- **USD 1.3771218**, below the existing USD 6 qualification sub-cap.

No new user spend approval is required.

## Planned Gemini contract-v2 run after verification

Candidate:
- Google `gemini-3.5-flash-lite` only.

Protocol:
- Devanagari from call 1;
- 96 items;
- transcribe + verdict;
- 3 repeats;
- contract v2: blind transcribe decides qualification; verdict diagnostic only;
- same numerical thresholds;
- Latin only if primary Devanagari passes;
- retries 0;
- same persistent EMP-001 ledger;
- preserve all prior evidence;
- write a new result artifact plus canonical `qualification-result.json`.

Operational rate control:
- **minimum 7 seconds between Gemini dispatch starts**;
- serial execution;
- if any new 429 or other ambiguous post-dispatch failure occurs: count/persist it, no retry, stop.

No Haiku, Sonnet or fal calls during this run.

## Verification gate before merge/live execution

Zero-spend only:
- provider-adapter tests;
- provider-transport tests;
- text-qualification tests;
- live/fake-live qualification tests;
- A-TEXT handoff tests;
- preflight;
- keys unset;
- external calls 0;
- spend USD 0;
- prior live evidence byte-identical.

Only after green verification may EVAL-021 merge and the Gemini contract-v2 run begin.
