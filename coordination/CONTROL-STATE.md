# Controller State

**Updated:** 27 Aug 2026 — First EMP-001 live run disqualified Haiku 4.5; Gemini was unresolved after a 17-call 429 halt. User directed Sonnet; Sonnet 5-only qualification continuation is now the active next gate.

**Read `PROJECT-MEMORY.md` first.** Where older task/handoff wording conflicts with this file and the latest durable Controller decisions, the latest Controller decision governs.

## Global posture

Broad research/design and the final pre-execution freeze are closed.

The accepted EVAL-012→016 execution implementation for the first empirical tranche is now integrated. Fresh macOS verification of the reproducible execution materials is green. No real provider call has occurred.

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

The EVAL-012→016 work makes the execution machinery safer and closes the zero-spend material gates. It does **not** establish any model-quality result.

## EMP-001 — AUTHORISED, LIVE QUALIFICATION IN PROGRESS

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

Approved spend remains:
- total consumed-API ceiling **USD 10.00**;
- planning reference ≈ ₹954 before tax;
- text-judge qualification sub-cap **USD 6.00**;
- retries **0**;
- no account pre-funding above the approved ceiling.

**The bounded EMP-001 spend was explicitly approved by the user and is recorded in `coordination/decisions/CONTROLLER-EMP-001-SPEND-AUTHORISATION-2026-08-27.md`.**

## Text-judge qualification freeze

Configured candidates are now:
- Anthropic `claude-sonnet-5`;
- Google `gemini-3.5-flash-lite`.

For the active continuation, **Sonnet 5 only** is authorised. The pending Gemini continuation is superseded for now.

The prior OpenAI `gpt-5.4-mini` candidate is superseded for EMP-001. The OpenAI adapter may remain dormant compatibility code, but no OpenAI key is required for this tranche.

Exact execution model IDs must be pinned. Anthropic `claude-sonnet-5` is a pinned model ID under Anthropic's current model-ID policy; Google uses the documented stable exact ID `gemini-3.5-flash-lite`.

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

## EVAL-016 — ACCEPTED AND INTEGRATED

Authoritative Controller review:
- `coordination/decisions/CONTROLLER-EVAL-016-REVIEW-2026-08-27.md`

Integration:
- PR #39;
- merge commit `ff0e4bb379acd69a23909a57a2da50bf5ceaace3`.

Fresh macOS verification:
- EMP-001 tests: **366 passed**;
- preflight: **PREFLIGHT_GREEN**, 8/8 checks PASS;
- Latin exact pinned Arial render reproduced;
- completed human review survived rebuild byte-identically;
- human review: **96/96 usable, 48/48 mismatch-visible, 0 rejected**;
- Latin pack SHA: `320323ff84dd9c0d3ea3e9110eead1a3b789516de43c5f31c4f414fa022f1fcb`;
- Devanagari rebuilt identity matches frozen human-validation SHA exactly;
- validated Devanagari view: **96 = 48 match + 48 mismatch**;
- provider/model/evaluator calls: **0**;
- consumed API spend: **USD 0**.

EVAL-016 also fixes the post-review lifecycle:
- routine Latin rendering preserves completed human evidence;
- match rows do not require a fabricated visible-difference answer;
- human review is fingerprint-bound to the frozen pack;
- unresolved/stale review blocks Latin qualification before any Latin call;
- A-TEXT uses the same canonical gate.

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

### 1. Latin human perceptibility review — COMPLETE

Authoritative record:
- `coordination/decisions/CONTROLLER-EMP-001-LATIN-HUMAN-REVIEW-2026-08-27.md`

Human review result:
- usable surface: **96/96 yes**;
- controlled mismatches visibly different: **48/48 yes**;
- frozen pack SHA-256 verified against the supplied review bundle.

This prerequisite no longer blocks the Latin qualification leg.

### 2. Runtime secrets

Needed only at execution:
- `ANTHROPIC_API_KEY`;
- `GOOGLE_API_KEY`;
- `FAL_KEY`.

No secret belongs in GitHub.

If any provider requires account funding above an approved ceiling, execution must stop and return.

### 3. Exact execution-time model/version pins — PUBLIC METADATA VERIFIED

Authoritative verification:
- `coordination/decisions/CONTROLLER-EMP-001-PRE-SPEND-VERIFICATION-2026-08-27.md`

Current execution identifiers:
- Anthropic: `claude-sonnet-5` pinned model ID;
- Google: `gemini-3.5-flash-lite` current documented stable exact model ID.

Do not use the synthetic test fixture `gemini-3.5-flash-lite-001` as though it were a published provider version. Do not use a `*-latest` alias or silently substitute a sibling model.

### 4. Current route availability and planning prices — VERIFIED

Verified on 27 Aug 2026:
- fal `openai/gpt-image-2`, 1024×1024 medium: USD 0.053/image;
- fal `fal-ai/ideogram/v3`, BALANCED: USD 0.060/image;
- Anthropic Claude Sonnet 5: USD 2.00/M input, USD 10.00/M output;
- Gemini 3.5 Flash-Lite: USD 0.30/M input, USD 2.50/M output.

These match the current committed EMP-001 price book after the Sonnet 5 switch.

### 5. Rebuild gitignored generated image sets — VERIFIED

Fresh macOS rebuild completed under EVAL-016 verification:
- Latin images reproduced with the exact pinned Arial font;
- completed human review survived the rebuild;
- Devanagari materialised build matches the frozen battery identity;
- validated Devanagari execution view is 96 items.

These are reproducible gitignored build products. The live execution worker may recreate them in its execution worktree, but there is no remaining scientific/material uncertainty to resolve.

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

Run the authorised **Sonnet 5-only** qualification continuation recorded in `coordination/decisions/CONTROLLER-EMP-001-SONNET-5-CONTINUATION-2026-08-27.md`.

Constraints:
1. Anthropic `claude-sonnet-5` only; do not rerun Haiku and do not run Gemini in this continuation.
2. Devanagari first; Latin only if Devanagari passes.
3. Same 96-item batteries, 2 shapes, 3 repeats, prompts, thresholds and reviewed materials.
4. Preserve the first live run and its ledger/evidence.
5. Already-counted qualification spend: USD 0.0854218.
6. Sonnet worst-case reservation if both scripts run: USD 5.345280.
7. Cumulative worst-case qualification amount: USD 5.4307018 <= USD 6.
8. Retries 0. Any ambiguous dispatch failure is counted and stops the continuation.
9. No billing-tier change or prefunding is authorised.
10. Stop after qualification and report to Controller before A-TEXT.



