# Controller State

**Updated:** 27 Aug 2026 — User authorised a combined EVAL-022 pass: apply the OCR failure-taxonomy correction, verify at zero spend, then—only if fully green—run live Google Cloud Vision TEXT_DETECTION. Incremental OCR cap USD 1.00; frozen 576-call protocol reserves at most USD 0.864. A-TEXT remains blocked.

**Read `PROJECT-MEMORY.md` first.** Where older task/handoff wording conflicts with this file and the latest durable Controller decisions, the latest Controller decision governs.

## Global posture

Broad research/design and the final pre-execution freeze are closed.

The accepted EVAL-012→016 execution implementation for the first empirical tranche is now integrated. Fresh macOS verification of the reproducible execution materials was green before live spend. The first real qualification run has now occurred and is preserved as empirical evidence.

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

The execution machinery is now live. Contract-v2 Sonnet 5 and Gemini 3.5 Flash-Lite are both scientifically disqualified for Devanagari exact-text judging. Both exhibit stable silent auto-correction of corrupted Hindi text on the blind transcription shape. The later Gemini 429 occurred only after all 288 primary calls were complete and affects diagnostic completeness, not qualification. Historical Haiku evidence remains preserved.

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

General-purpose multimodal LLMs are now **frozen as the primary exact-text judge family for EMP-001**. No further Haiku/Sonnet/Gemini qualification call is authorised. EVAL-022 prepares a purpose-built OCR evaluator family at zero spend.

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
- any additional paid text-judge call while EVAL-022 readiness is open;
- any Cloud Vision live OCR call;
- any further Haiku, Sonnet or Gemini qualification attempt;
- account funding above the approved ceiling;
- A-TEXT until a qualified evaluator covers all required scripts;
- full 90-generation Stage A;
- Stage B / Stage C;
- EVAL-006;
- Registry population from unqualified instruments;
- broad controlled-pack acquisition;
- Production IR/Planner implementation.

Customer-outcome CpAO remains Stage C only.

## Next gate

Execute the combined EVAL-022 correction + conditional live OCR pass recorded in
`coordination/decisions/CONTROLLER-EVAL-022-COMBINED-CORRECTION-LIVE-OCR-AUTH-2026-08-27.md`.

Sequence:
1. apply the OCR scientific-vs-infrastructure failure taxonomy correction;
2. run full zero-spend focused verification and preflight;
3. if ANY verification fails, stop before external spend;
4. if fully green, push the corrected branch and confirm pushed HEAD == tested HEAD;
5. confirm `GOOGLE_CLOUD_VISION_API_KEY` exists locally without printing it;
6. run Google Cloud Vision `TEXT_DETECTION` qualification from that exact pushed/tested HEAD;
7. no language hints, retries 0, target never sent;
8. Devanagari: 96 × 3 = 288 OCR calls;
9. Latin only if Devanagari scientifically passes; max total 576 calls;
10. incremental OCR spend cap USD 1.00;
11. frozen max OCR reservation USD 0.864;
12. prior qualification spend USD 0.6712415;
13. prospective cumulative USD 1.5352415 <= USD 6;
14. provider/API/quota/transport failures stop incomplete and are not scientific gate evidence;
15. successful-but-empty OCR responses count toward `empty_transcription_rate_max: 0.05`;
16. if both scripts qualify, stop before A-TEXT;
17. no fal calls; Registry unchanged;
18. preserve all historical EMP-001 evidence byte-identically.












