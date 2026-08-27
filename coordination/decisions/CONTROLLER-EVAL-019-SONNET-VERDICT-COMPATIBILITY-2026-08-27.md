# Controller EVAL-019 — Sonnet 5 Verdict Compatibility Correction — 2026-08-27

## Status

**ZERO-SPEND HARNESS CORRECTION PREPARED; CORRECTED SONNET-ONLY RERUN AUTHORISED UNDER EXISTING EMP-001 SPEND APPROVAL AFTER INTEGRATION.**

## Evidence motivating this correction

The first Sonnet 5 continuation produced:
- 96/96 Devanagari `transcribe` calls successfully;
- the first `verdict` call stopped as `malformed_response` / `ambiguous_dispatch`;
- Sonnet continuation counted spend: USD 0.035202;
- cumulative qualification spend after that stop: **USD 0.1206238**;
- Latin not run;
- A-TEXT not run.

This partial Sonnet screen is **not a scientific qualification verdict**.

## Root-cause diagnosis

The Anthropic adapter was written against Haiku-era behavior:
- `transcribe` used `max_tokens: 128`;
- `verdict` used `max_tokens: 16`;
- neither request specified a thinking mode.

Anthropic's current Sonnet 5 documentation states:
- adaptive thinking is ON by default when the `thinking` field is omitted;
- `max_tokens` is a hard limit across thinking plus final response text;
- thinking can be turned off with `thinking: {"type": "disabled"}`.

Therefore the old 16-token verdict request was not equivalent to the intended terse no-thinking judge configuration and was capable of consuming its output budget before a final text block.

Separately, the parser treated any successful Anthropic response with no text/refusal as malformed transport ambiguity. That is too broad: a documented `stop_reason` such as `max_tokens` is a well-formed provider response whose request ID, usage and cost are known.

Sources verified 27 Aug 2026:
- https://platform.claude.com/docs/en/models/sonnet-5/whats-new-sonnet-5
- https://platform.claude.com/docs/en/models/sonnet-5/migration-guide
- https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons

## Correction

1. Anthropic text-judge requests explicitly set:
   `thinking: {"type": "disabled"}`
   for both `transcribe` and `verdict`.

2. The existing max-token limits remain unchanged:
   - transcribe: 128;
   - verdict: 16.

3. A successful Anthropic response with no text but a documented `stop_reason` is no longer classified as ambiguous transport failure:
   - `stop_reason=max_tokens` -> `api_status=error`, `error_class=max_tokens_no_text`;
   - other documented no-text stop reasons -> explicit `empty_response_<stop_reason>` error.
   The response keeps its provider request ID, token usage and reported/provisional cost and is not retried.

4. Only a response lacking text/refusal **and** lacking a documented stop reason remains a malformed-response ambiguity.

5. The fake-live path now honors `--only-provider`, matching the live continuation path.

## Scientific consequence

The prior 97-call Sonnet attempt remains historical execution evidence but cannot qualify or disqualify Sonnet.

The corrected Sonnet qualification must restart from the beginning. It may not resume at verdict because the judge configuration changed.

Frozen scientific protocol otherwise remains unchanged:
- Devanagari first;
- 96 items;
- transcribe + verdict;
- 3 repeats;
- Latin only after Devanagari passes;
- same images, prompts, scoring, thresholds and human-reviewed materials;
- retries 0.

## Spend

Already-counted qualification spend: **USD 0.1206238**.

Conservative Sonnet reservation remains USD 0.004640 per call.

Maximum corrected Sonnet run if it survives both scripts:
- 1,152 calls;
- USD 5.345280 reservation.

Cumulative worst case:
- **USD 5.4659038**, below the user-approved USD 6 qualification sub-cap.

No additional user spend approval is required.

No Gemini continuation is authorised during this corrected Sonnet run.

## Execution gate

After this correction is integrated:
1. run focused zero-spend tests for the changed adapter/continuation path and preflight;
2. preserve all prior run evidence;
3. execute a fresh Sonnet 5-only qualification attempt from Devanagari call 1 using the same persistent spend ledger;
4. write a new evidence artifact; do not overwrite previous Haiku/Gemini/Sonnet evidence;
5. stop on true ambiguous dispatch with retries 0;
6. if Sonnet qualifies on both scripts, stop before A-TEXT and return to Controller.
