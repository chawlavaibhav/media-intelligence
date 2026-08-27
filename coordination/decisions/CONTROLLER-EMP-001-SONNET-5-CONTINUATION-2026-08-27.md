# Controller EMP-001 Sonnet 5 Continuation — 2026-08-27

## Status

**AUTHORISED — SONNET-ONLY QUALIFICATION CONTINUATION UNDER EXISTING EMP-001 SPEND APPROVAL.**

User direction: use Sonnet at least.

This supersedes the pending Gemini-only continuation decision. Do not start the paced Gemini continuation at this time.

## Candidate

Run Anthropic:
- model ID: `claude-sonnet-5`
- current Anthropic price: USD 2 / 1M input tokens, USD 10 / 1M output tokens
- vision input supported
- Anthropic documents the model ID itself as pinned/stable for its lifetime.

The previous Haiku 4.5 result remains valid historical evidence and is not rerun.

## Scientific protocol

Sonnet uses the exact frozen qualification protocol:
1. Devanagari first.
2. 96 items.
3. two shapes: `transcribe`, `verdict`.
4. 3 repeats per shape.
5. Latin only if Devanagari passes.
6. same prompts, images, human-reviewed materials, scoring, thresholds and blindness checks.
7. retries 0.

No Gemini calls are part of this continuation.

## Spend

Already-counted qualification spend from the first live attempt:
- USD 0.0854218.

Existing conservative reservation rule for Sonnet:
- 2,000 input tokens + 64 output tokens per call;
- USD 2/M input + USD 10/M output;
- reservation per call = USD 0.004640.

Maximum if Sonnet survives both scripts:
- 1,152 calls;
- Sonnet reservation = USD 5.345280;
- cumulative qualification worst case including first run = **USD 5.4307018**.

This remains below the existing user-approved USD 6 qualification sub-cap and USD 10 EMP-001 total cap.

A full Sonnet + Gemini rerun would not fit the USD 6 sub-cap under conservative reservation, so this decision explicitly authorises Sonnet only.

## Operational requirements

- Use the existing EMP-001 persistent spend ledger so prior counted spend remains included.
- Preserve the first live run and all existing evidence byte-for-byte.
- Write the Sonnet qualification result to a new output artifact; do not overwrite prior qualification evidence.
- No concurrency requirement is added beyond existing runner semantics.
- On any ambiguous post-dispatch failure: count reservation, persist, no retry, stop.
- No account funding or billing-tier change is authorised.
- No secrets may be committed or printed.

## A-TEXT

If Sonnet qualifies on both Devanagari and Latin, stop and return the qualification evidence to the Controller before A-TEXT generation.

Do not run fal image generation as part of this continuation.
