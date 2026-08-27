# Controller EMP-001 Gemini Qualification Continuation — 2026-08-27

## Status

**AUTHORISED — GEMINI-ONLY PACED QUALIFICATION CONTINUATION UNDER EXISTING EMP-001 SPEND APPROVAL.**

This is not a new scientific candidate and does not alter any qualification threshold, item, prompt, repeat count, shape, or script order.

## Evidence accepted from first live run

Anthropic `claude-haiku-4-5-20251001` completed the full Devanagari qualification screen:
- 576 calls;
- 0 refusals;
- 0 errors;
- match false-fail rate 0.4097;
- 43 mismatch false passes;
- repeat consistency 0.9271;
- 118 false fails.

Verdict: **DISQUALIFIED for EMP-001 text judging.**
Latin was correctly not run.

Google `gemini-3.5-flash-lite` stopped after 17 calls on an HTTP 429 ambiguous post-dispatch failure. That partial screen is **not a scientific qualification verdict**.

A-TEXT did not run and fal generation count remained 0.

First-run counted qualification spend:
- reported: USD 0.0846618;
- unknown provisional: USD 0.0007600;
- total counted: **USD 0.0854218**.

## Continuation decision

Run **Gemini only** against the same frozen qualification protocol:
1. Devanagari first.
2. Latin only if Gemini passes Devanagari.
3. Same 96 items per script.
4. Same two shapes.
5. Same 3 repeats per shape.
6. Same prompts, scoring, thresholds, exact model ID and human-reviewed materials.

Operational pacing is permitted and does not change the scientific instrument:
- minimum interval between Gemini dispatches: **7 seconds**;
- no concurrency;
- retries remain **0**.

The first failed 17-call attempt remains persisted and must not be deleted or rewritten. The paced run is a new qualification attempt, not a retry of the ambiguous trial.

If any new ambiguous post-dispatch failure occurs, including another 429:
- count the reservation conservatively;
- persist it;
- do not retry;
- stop the paced run.

## Spend bounds

Original user approval remains controlling:
- USD 10 total EMP-001 consumed API spend;
- USD 6 qualification sub-cap;
- retries 0;
- no prefunding above USD 10.

Already-counted qualification spend: USD 0.0854218.

Therefore remaining qualification headroom before this continuation is **USD 5.9145782**.

No billing-tier upgrade, prepaid-credit purchase, or other account funding is authorised by this continuation decision.

## A-TEXT

Do not run A-TEXT unless the paced Gemini qualification completes and qualifies on both Devanagari and Latin.

If Gemini qualifies, return the qualification evidence to the Controller before any image generation if the current runner cannot safely bind the continuation evidence into the existing EMP-001 handoff without rewriting history.
