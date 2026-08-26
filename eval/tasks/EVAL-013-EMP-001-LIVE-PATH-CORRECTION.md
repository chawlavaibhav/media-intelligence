# EVAL-013 — EMP-001 Positive Live-Path Correction

**AUTONOMY:** autonomous  
**ENVIRONMENT:** Claude Code/cloud repository workspace  
**EXTERNAL SPEND:** **USD 0 / INR 0**  
**PROVIDER / MODEL / EVALUATOR CALLS:** **0**  
**BRANCH:** `work/eval-013-emp-001-live-path-correction`

## Objective

Correct only the positive live-execution gaps identified by the Controller review of EVAL-012. Preserve all useful EVAL-012 zero-spend work.

This task must make the code mechanically ready for explicit EMP-001 spend approval **without making any real provider call**.

Read first:

1. `PROJECT-MEMORY.md`
2. `shared/COMMUNICATION-STANDARD.md`
3. `coordination/decisions/CONTROLLER-EVAL-012-REVIEW-2026-08-26.md` from current `main`
4. `eval/tasks/EVAL-012-EMP-001-ZERO-SPEND-IMPLEMENTATION.md`
5. `docs/superpowers/plans/2026-08-26-first-empirical-tranche.md`
6. all returned EVAL-012 files under `eval/empirical-tranche-1/`

## Fixed boundaries — do not reopen

- EMP-001 remains text-first; not the full 90-generation Stage A.
- Proposed later external ceiling remains **USD 10.00**; this task authorises USD 0.
- Retries remain **0**.
- Stage-Q model generations remain 0.
- Devanagari validated view remains 96 items, untouched.
- Latin qualification pack remains separate 96 items, 48 match + 48 mismatch.
- Qualification repeats remain 3 per shape.
- `transcribe` remains primary/blind; `verdict` remains diagnostic.
- A-TEXT strings remain exactly the four frozen strings.
- A-TEXT maximum remains 16 generations: 8 IMG-01 + 8 IMG-02.
- No customer CpAO.
- No full-slot promotion from A-TEXT.
- No scientific roster/model-selection change.
- No new research.

## Required corrections

### E13-A — positive live qualification orchestration

`qualify_text.py --live` currently unconditionally refuses even after opening a valid authorisation guard.

Implement the real orchestration path so it can consume real `TextJudge` instances behind injected transports.

Requirements:

- keep Devanagari-first progressive stop;
- Latin runs only for Devanagari survivors;
- real/non-dry-run records are `synthetic: false`;
- no Registry promotion merely because qualification ran;
- every provider call is one trial; refusal/error/timeout remains evidence and is never retried;
- cumulative spend guard is shared across candidates/scripts as frozen;
- exact alias + resolved version persists on every call;
- CLI still fails closed without valid explicit authorisation.

No real provider call may be made in this task. Exercise the path with fake transports only.

### E13-B — provider-correct judge transports

Split provider-specific request dispatch/auth rather than using one generic Bearer-key transport for all providers.

At minimum:

- OpenAI path: Bearer-token semantics appropriate to the chosen OpenAI API surface;
- Gemini API-key path: `x-goog-api-key` semantics, not generic Bearer of `GOOGLE_API_KEY`;
- secrets read only at dispatch time;
- no key in committed request/response artifacts;
- URL/model path is derived from the exact resolved version at execution, not silently from a floating alias.

Tests must inspect the generated URL/headers/body through an injected no-network HTTP recorder.

Do not make a real HTTP request.

### E13-C — fal IMG-01 / IMG-02 generation adapters

Implement route-specific generation adapters for exactly:

- IMG-01: fal `openai/gpt-image-2`, 1024x1024 medium;
- IMG-02: fal `fal-ai/ideogram/v3`, BALANCED.

Requirements:

- `FAL_KEY` read only at dispatch time;
- construction/import makes no network call;
- request route/config frozen exactly;
- provider request id/status/error/refusal/cost metadata can be persisted;
- exactly one dispatch per attempt;
- no retry path;
- artifact result can be handed to the qualified judge as image bytes through an injected artifact-fetch layer;
- fake transports/fake artifact fetchers only in EVAL-013 tests.

Do not contact fal.

### E13-D — real A-TEXT measurement path

Correct `run_atex.py` so non-dry-run execution does not use `_fake_transcribe` and is not hard-coded synthetic.

Requirements:

- dry run continues to use fake generator/judge and stays synthetic;
- non-dry-run uses the supplied qualified judge's blind `transcribe(image_bytes)` result;
- code-level exact comparison remains authoritative;
- `verdict` may remain omitted unless explicitly budgeted; it may never override transcription;
- `synthetic` must equal the actual execution mode, not a constant;
- real A-TEXT remains partial admission evidence and cannot by itself populate a complete slot Registry row;
- failed/refused/timed-out generation attempts persist even without artifact;
- if an artifact exists but judge evaluation fails/refuses, preserve both the generation trial and evaluator trial separately.

### E13-E — missing positive controls

Add tests that prove the inverse path, not only refusal:

1. valid authorisation + fake OpenAI live transport + budget -> exactly one evaluator dispatch and a non-synthetic persisted call record;
2. valid authorisation + fake Gemini live transport -> correct `x-goog-api-key` header and exactly one dispatch;
3. valid authorisation + qualified fake-live judge + green preflight + fake fal generator -> exactly the frozen A-TEXT call count, non-synthetic records, no retries;
4. invalid auth -> zero dispatch;
5. budget insufficient -> zero next dispatch;
6. real/non-dry-run evidence is never labeled synthetic;
7. A-TEXT real partial evidence still cannot promote a complete Registry row;
8. all refusal/error/timeout paths preserve one-call-one-trial and cost/absence semantics.

A positive-control test that would still pass if the live branch were unconditionally refused is invalid.

### E13-F — final zero-spend verification

Freshly run:

- all `eval/empirical-tranche-1/tests/`;
- V1 harness self-test;
- cross-branch validation;
- dry-run preflight / qualification / A-TEXT;
- positive fake-live qualification path;
- positive fake-live A-TEXT path;
- Registry zero/byte-identical check;
- protected baseline hash check.

Record exact commands, test counts and exits in a new or amended verification record.

## Human perceptibility boundary

The Latin `perceptibility-review.csv` may remain unfilled if no human reviewer is available. Do not fabricate it. State clearly that Latin paid qualification remains gated on this zero-spend human review.

This does not excuse missing live-path implementation.

## Return

Create/update a bounded readiness record and return exactly:

1. verdict: `READY_FOR_SPEND_APPROVAL | BLOCKED`;
2. commit SHA;
3. exact fresh tests/commands and results;
4. positive fake-live paths proved;
5. remaining prerequisites before first real call;
6. confirmation external calls = 0 and spend = 0;
7. whether a valid user approval + runtime secrets/version pins would now be sufficient to start EMP-001 without another code change.

Do not merge.
