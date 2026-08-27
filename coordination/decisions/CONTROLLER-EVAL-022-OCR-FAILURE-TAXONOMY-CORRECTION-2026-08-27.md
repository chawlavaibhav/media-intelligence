# Controller EVAL-022 Correction — Separate OCR Scientific Failure from Infrastructure Failure — 2026-08-27

## Status

**REQUIRED ZERO-SPEND CORRECTION BEFORE EVAL-022 CAN BE REVIEWED FOR MERGE OR LIVE AUTHORISATION.**

The worker-reported EVAL-022 implementation is substantially on target, but one contract semantic must be corrected before any live OCR run.

## Problem

The current local OCR implementation reportedly mixes:
- successful provider execution that returns no usable transcription on a validated visible-text image; and
- provider/API/backend/quota failures

inside one refusal/error-rate gate.

These are not the same evidence.

## Correct semantics

### Scientific OCR evaluator failure

A successful OCR provider response that contains **no usable transcription** for an image already validated as containing visible text is a scientific evaluator failure.

Persist it distinctly, e.g.:
- `api_status: error`
- `error_class: empty_transcription`
- `ambiguous_dispatch: false`

It must count against a dedicated OCR scientific availability/failure gate.

For OCR contract v1 use:
- `empty_transcription_rate_max: 0.05`

This replaces any combined `refusal/error_rate_max` concept for scientific qualification.

Do not silently turn an empty transcription into MATCH or MISMATCH.

### Infrastructure / execution failure

Provider/API/backend/quota failures are not evidence about OCR recognition quality.

Examples:
- HTTP 429 / quota / rate limit;
- provider `UNAVAILABLE` / backend error;
- transport reset / timeout;
- malformed response after dispatch;
- authentication/configuration error after dispatch.

They must:
- be persisted separately with provider/config/trial identity;
- preserve known billing or conservative provisional reservation as applicable;
- use retries 0;
- stop the run fail-closed;
- leave the current script scientifically **incomplete**;
- NOT increment `empty_transcription_rate`;
- NOT increment false-pass / false-fail counts;
- NOT produce a scientific pass/fail disposition for an incomplete script.

Provably pre-dispatch failures such as a missing local key dispatch nothing and cost nothing.

## Gate metrics

For a complete OCR script, qualification metrics should be:

- mismatch false passes: max 0;
- match false-fail rate: max 0.10;
- empty-transcription rate: max 0.05;
- repeat consistency: min 0.95.

All are computed only from provider executions that reached a scientifically interpretable OCR outcome, except the explicit empty-transcription metric which counts successful-but-empty OCR responses.

Infrastructure failures are execution state, not a gate metric.

## Tests required

Add or update zero-network tests proving:

1. an empty successful OCR response counts toward `empty_transcription_rate` and can fail that gate;
2. a provider-reported backend/quota error stops the run and leaves it incomplete without incrementing scientific gate metrics;
3. an ambiguous transport/malformed response stops the run and leaves it incomplete, with conservative billing semantics;
4. missing key is pre-dispatch and costs zero;
5. no infrastructure error can accidentally produce `passed: true` or `passed: false` for an incomplete script;
6. the clean 576-call fake-live control still qualifies both scripts;
7. retries remain 0.

## Other worker design calls

Accepted:
- OCR repeat consistency keyed by item only is correct for a single-shape family.
- Separate OCR contract is correct.
- No fabricated verdict shape is correct.
- `TEXT_DETECTION` with no language hints is the correct first candidate configuration.
- A-TEXT family gate remaining closed is correct.
- Conservative USD 0.0015/image reservation is correct.

## Source branch handling

The worker reported local branch:
- `eval/eval-022-ocr-family-readiness`
- local HEAD `3be9c1d3bcaafc612621fe99698d47fce1b7f554`

That branch is not on GitHub, so the Controller cannot inspect or merge it yet.

After applying this correction and rerunning zero-spend verification:
- push the branch to origin;
- do not merge;
- return the pushed exact HEAD and report to Controller.

No live Cloud Vision call is authorised.
A-TEXT remains blocked.
