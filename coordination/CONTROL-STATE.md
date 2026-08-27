# Controller State

**Updated:** 27 Aug 2026 — EVAL-015 accepted and integrated into `main`; paid EMP-001 execution remains blocked pending zero-spend prerequisites and explicit user approval.

**Read `PROJECT-MEMORY.md` first.** Where older task/handoff wording conflicts with this file and the latest durable Controller decisions, the latest Controller decision governs.

## Global posture

Broad research/design and the final pre-execution freeze are closed.

The accepted EVAL-012→015 execution implementation for the first empirical tranche is now integrated. The project is at **zero-spend pre-execution prerequisites** before any real provider call.

Frozen foundations remain:
- CANON-010 request contract;
- Capability Contract v2: **44 = 43 active + 1 dormant**;
- 13 condition families;
- 12 core + 2 reserve scientific question slots;
- Resources topology v3 / CpAO v3 / four controlled-pack families;
- EVAL-011 staged design: Q=0 model generations, A=90, B≤404 additional, C=32 outcome attempts;
- GOV-004 **PASS WITH NON-BLOCKING NOTES**.

There is no active broad research task.

## Current empirical floor

Still true:
- **0 qualified models/workflows**;
- **0 qualified subjective/perceptual evaluator families**;
- **0 current empirical Capability Registry rows**;
- **0 accepted evidence that Canon improves model outcomes**;
- no Production IR/Planner exists.

The EVAL-012→015 work makes the execution machinery safer. It does **not** establish any model-quality result.

## EMP-001 — prepared, NOT authorised

Frozen paid shape remains:

1. qualify text judges progressively: Devanagari first, Latin only for survivors;
2. only if one judge qualifies for every script required by A-TEXT, run image generation;
3. A-TEXT: 4 strings × 2 repeats × 2 routes = **16 image generations maximum**.

Frozen A-TEXT strings:
- `शुभ दीपावली`
- `आज की डील`
- `Aaj ki Deal`
- `SAVE 20% • ₹999`

Frozen image routes:
- IMG-01: fal `openai/gpt-image-2`
  - 1024×1024
  - medium
  - 8 unseeded generations
- IMG-02: fal `fal-ai/ideogram/v3`
  - BALANCED
  - 8 unseeded generations

Primary measurement remains:
- blind transcription;
- code-level exact equality.

A-TEXT remains only a partial admission screen. It may eliminate deeper text spend; it cannot promote a complete Stage-A model slot.

Proposed spend remains:
- total consumed-API ceiling **USD 10.00**;
- planning reference ≈ ₹954 before tax;
- text-judge qualification sub-cap **USD 6.00**;
- retries **0**;
- no account pre-funding above the approved ceiling.

**No part of that spend is approved yet.**

## Text-judge qualification freeze

Candidates remain:
- OpenAI `gpt-5.4-mini`;
- Google `gemini-3.5-flash-lite`.

Exact resolved model versions must be pinned at execution. Aliases alone are insufficient.

Materials remain:
- Devanagari validated view: 96 items;
- Latin pack: 96 items = 48 match + 48 controlled mismatch;
- 3 repeats per shape;
- shapes: `transcribe`, `verdict`.

Maximum evaluator calls if both candidates survive both scripts:
- **2,304**.

Devanagari failure stops that candidate before Latin.

## EVAL-015 — ACCEPTED AND INTEGRATED

Authoritative Controller review:
- `coordination/decisions/CONTROLLER-EVAL-015-REVIEW-2026-08-27.md`

Worker branch:
- `work/eval-015-emp-001-ambiguous-dispatch`
- returned head `b98789673a90fac350609eed5730ff6483e7e6bf`

Conflict-free Controller integration:
- PR #36;
- merge commit `bf17fe2db3a3712753fbf5bdf8db28e682f1b1b1`.

Controller verdict:
- **ACCEPTED FOR INTEGRATION — NOT SPEND APPROVAL.**

Accepted semantics:

### Provably pre-dispatch failure

Examples:
- missing API key before dispatch;
- blindness/request validation refusal;
- model/body refusal before dispatch.

May release or avoid a reservation because no provider call occurred.

### Ambiguous post-dispatch failure

Examples:
- read/socket timeout after dispatch path entered;
- connection reset;
- remote disconnect;
- TLS/network ambiguity;
- malformed/unparseable provider response after send.

Must:
- **NOT** release spend headroom;
- persist one timeout/error trial;
- preserve provider/model/route identity;
- preserve trial/attempt identity;
- preserve `cost_ref`;
- mark billing state unknown/provisional;
- conservatively count the reserved estimate when actual billing is unavailable;
- retry 0 times;
- stop fail-closed.

Generation ambiguity also persists the generation Attempt and invokes no evaluator because there is no usable artifact.

An ambiguous evaluator call after a successful generation preserves both trials and stops the run.

## Accepted EVAL-014 controls preserved

Still accepted:
- persistent cumulative spend ledger across separate processes;
- mechanical USD 10 total ceiling;
- mechanical USD 6 qualification sub-cap;
- outstanding reservations count against available headroom;
- fingerprint-bound qualification → A-TEXT handoff;
- real A-TEXT handoff reconstructs the same provider + model alias + exact resolved version;
- deterministic evaluator trial/attempt identity;
- ledger-resolvable cost refs;
- target-aware blind pre-dispatch checking;
- Latin perceptibility gate blocks complete A-TEXT;
- Registry remains empty unless qualified empirical evidence exists.

Worker-reported EVAL-015 verification:
- EMP-001 tests: **363 passed**;
- V1 harness: **107/107**;
- Resources cross-branch validation: **PASS**;
- fake-live qualification: **2,304 evaluator dispatches**;
- fake-live A-TEXT: **16 generations + 16 evaluator calls**;
- cross-process rehearsal:
  - qualification USD 0.9763200
  - + A-TEXT USD 0.9142480
  - = USD 1.8905680 cumulative;
- Registry rows: 0;
- 13/13 protected baselines byte-identical;
- 0 external calls;
- USD 0 spend.

Treat the test counts as worker execution evidence. The Controller independently reviewed the pushed code/diff and integration shape.

## Remaining zero-spend prerequisites

### 1. Latin human perceptibility review — STILL UNFILLED

This is the main outstanding non-code gate.

It must not be fabricated.

Mechanical validation exists, but a person has not yet confirmed that the rendered Latin match/mismatch differences are perceptible and usable.

This gates the Latin qualification leg and therefore the complete four-item A-TEXT screen.

### 2. Runtime secrets

Needed only at execution:
- `OPENAI_API_KEY`;
- `GOOGLE_API_KEY`;
- `FAL_KEY`.

No secret belongs in GitHub.

If any provider requires account funding above an approved ceiling, execution must stop and return.

### 3. Exact execution-time model/version pins

The live path mechanically refuses floating aliases without exact version pins.

Current exact available versions must be verified immediately before execution.

### 4. Current route availability and planning prices

The frozen scientific routes remain unchanged, but current provider availability and planning prices must be checked before approval so the USD 10 ceiling is still credible.

### 5. Rebuild gitignored generated image sets

Required before execution. This is zero spend.

## Still blocked / not authorised

Not authorised:
- any paid EMP-001 call;
- any account funding;
- full 90-generation Stage A;
- Stage B / Stage C;
- EVAL-006;
- Registry population from unqualified instruments;
- broad controlled-pack acquisition;
- Production IR/Planner implementation.

Customer-outcome CpAO remains Stage C only.

## Next gate

1. Complete the Latin human perceptibility review with a real person.
2. Verify current exact model/version availability plus frozen route availability/prices.
3. Rebuild the generated zero-spend image sets.
4. Confirm execution secrets can be supplied without pre-funding beyond the proposed ceiling.
5. Only then present the user the explicit bounded EMP-001 spend decision.

**No paid provider/model/evaluator call may occur until the user explicitly approves the bounded EMP-001 USD 10 ceiling.**
