# Controller EMP-001 Judge Roster Switch — 2026-08-27

## Status

**BOUNDED ZERO-SPEND CORRECTION PREPARED — VERIFICATION REQUIRED BEFORE INTEGRATION.**

User direction: replace the unavailable OpenAI judge candidate rather than create/fund an OpenAI API account.

No provider/model/evaluator call is authorised by this decision.

## Roster change

Superseded active judge candidate:
- OpenAI `gpt-5.4-mini`

New active judge candidate:
- Anthropic `claude-haiku-4-5-20251001`

Unchanged second candidate:
- Google `gemini-3.5-flash-lite`

The original scientific requirement remains unchanged: qualify two independent multimodal judge families so one model's language prior is not silently treated as measurement truth.

## Why Haiku 4.5, not Sonnet 5

Current Anthropic first-party list pricing verified on 27 Aug 2026:
- Claude Haiku 4.5: USD 1 / 1M input tokens, USD 5 / 1M output tokens.
- Claude Sonnet 5: USD 2 / 1M input tokens, USD 10 / 1M output tokens.

Canonical Haiku model ID:
- `claude-haiku-4-5-20251001`

Anthropic documents this dated ID as a pinned model version.

Under the existing conservative reservation rule (2,000 input + 64 output tokens per call):
- Anthropic Haiku 4.5 reserve/call = USD 0.002320;
- Google Gemini 3.5 Flash-Lite reserve/call = USD 0.000760;
- each candidate maximum = 1,152 calls if it survives both scripts;
- Anthropic maximum reservation = USD 2.672640;
- Google maximum reservation = USD 0.875520;
- combined worst-case qualification reservation = **USD 3.548160**.

This fits the frozen USD 6 qualification sub-cap.

Claude Sonnet 5 was considered and rejected for this tranche because its conservative combined Anthropic+Google full-survival reservation would be USD 6.220800, above the existing USD 6 sub-cap. The user did not authorise changing the cap.

## Anthropic transport contract

Active key:
- `ANTHROPIC_API_KEY`

Endpoint:
- `POST https://api.anthropic.com/v1/messages`

Headers:
- `x-api-key`
- `anthropic-version: 2023-06-01`

Image input:
- base64 image content block, `image/png`.

The exact target remains absent from blind `transcribe` requests and present only in the diagnostic `verdict` prompt.

## What does not change

Unchanged:
- EMP-001 total consumed API ceiling: USD 10;
- qualification sub-cap: USD 6;
- retries: 0;
- no prefunding above the approved ceiling;
- Devanagari-first progression;
- Latin only for survivors;
- 96 Devanagari + 96 Latin qualification items;
- 3 repeats per shape;
- shapes: `transcribe`, `verdict`;
- qualification gates/thresholds;
- A-TEXT strings;
- fal image routes;
- 16 maximum A-TEXT generations;
- exact-string comparison in code;
- Registry promotion boundaries.

The dormant OpenAI adapter may remain as compatibility code, but OpenAI is no longer on the active EMP-001 judge roster and `OPENAI_API_KEY` is not an execution prerequisite.

## Additional handoff correction

A-TEXT now checks a qualification candidate against the current configured judge roster before accepting it.

Therefore an older, fingerprint-valid OpenAI qualification record cannot open A-TEXT after this roster switch.

## Public sources re-verified

Anthropic:
- model IDs/versioning: https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions
- Haiku 4.5 migration/model ID: https://platform.claude.com/docs/en/models/haiku-4-5/migration-guide
- pricing: https://platform.claude.com/docs/en/about-claude/pricing
- Messages/image API: https://platform.claude.com/docs/en/api/http/messages
- stop reasons/refusals: https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons

## Next gate

Fresh zero-spend macOS verification must prove:
- full EMP-001 tests green;
- fake-live qualification uses Anthropic + Gemini;
- cross-process rehearsal remains green;
- preflight green;
- generated material identities unchanged;
- zero provider/model/evaluator calls;
- zero API spend.

Do not merge this correction and do not request paid execution until that verification returns green.
