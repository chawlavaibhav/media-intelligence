# Controller EMP-001 Spend Authorisation — 2026-08-27

## Status

**AUTHORISED FOR BOUNDED LIVE EXECUTION.**

The user explicitly approved:

> EMP-001 up to USD 10 total consumed API spend, with a USD 6 text-judge qualification sub-cap, retries 0, and no prefunding above USD 10.

## Authorised scope

This authorisation applies only to EMP-001 with the currently integrated roster and frozen execution shape:

- Anthropic judge: `claude-haiku-4-5-20251001`
- Google judge: `gemini-3.5-flash-lite`
- fal IMG-01: `openai/gpt-image-2`
- fal IMG-02: `fal-ai/ideogram/v3`

Qualification remains progressive:
1. Devanagari first.
2. Latin only for judge candidates that survive Devanagari.
3. A-TEXT only if at least one judge qualifies on both scripts.

Frozen A-TEXT maximum:
- 4 strings × 2 repeats × 2 routes = 16 image generations.

## Hard limits

- Total consumed API spend ceiling: USD 10.
- Text-judge qualification sub-cap: USD 6.
- Retries authorised: 0.
- No prefunding above USD 10.
- Ambiguous post-dispatch failures remain conservatively reserved/counted and are not retried.
- No secrets may be committed or written to GitHub.
- Runtime secrets remain local only.
- Local `authorization.local.yaml` must remain gitignored.

## Execution keys expected locally

- `ANTHROPIC_API_KEY`
- `GOOGLE_API_KEY`
- `FAL_KEY`

This record contains no credential values.

## Registry / promotion

Qualification evidence may open A-TEXT only under the frozen gates. No Registry row is automatically authorised by this spend approval. Existing Registry promotion rules remain in force.
