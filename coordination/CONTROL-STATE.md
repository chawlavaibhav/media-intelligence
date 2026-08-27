# Controller State

**Updated:** 28 Aug 2026 — **the five parallel domain lanes have all settled and merged**, and GOV-006 has reconciled this file to them against `main` at `91984f50b294f11aefc7065f5ad11f9e0d3e2b9a`. CANON-011, EVAL-024, EVAL-029, EVAL-026, EVAL-030 and RES-005 are all accepted and merged; GOV-005 is closed. Cloud Vision `TEXT_DETECTION`/no-language-hints is benchmark-qualified for Devanagari and Latin and remains strict-exactness disqualified; its evidence is now **sealed into Git and recomputable from a fresh clone**. The 16 A-TEXT images are generated, sealed and scored: **7/16 exact**. **The Capability Registry still holds 0 rows.**

> **The previous version of this line is superseded, not corrected away.** It said EVAL-029 was not merge-ready and that EVAL-024 had no live artifacts. Both were true when written and are now false. Governor reconciliation: `governance/reviews/GOV-006-POST-PARALLEL-RECONCILIATION.md`.

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

New:
- Cloud Vision `TEXT_DETECTION`, no language hints, is **benchmark-qualified for text OCR on both Devanagari and Latin** under the separate `benchmark_text_ocr_v1` contract;
- it remains **strict_exactness_qualified: false**;
- benchmark qualification does not certify any individual output as exact;
- accepted EVAL-029 metrics:
  - Devanagari false-pass 0.1250, false-fail 0.0208, consistency 1.0;
  - Latin false-pass 0.1042, false-fail 0.0000, consistency 1.0;
- **EVAL-029 evidence is now sealed and merged.** `eval/empirical-tranche-1/evidence/EMP-001/text-ocr/` holds the exact source observations, the completed result and a bounded cost excerpt, all hash-fingerprinted. Both scripts' metrics recompute from committed bytes alone, with no machine-local path. GOV-005 finding **F-1 is resolved for this lane**;
- **A-TEXT is generated, sealed and scored.** 16 images exist as committed bytes; observed exact-text result **7/16** (GPT Image 2 6/8, Ideogram v3 1/8).

**The Registry is still empty, deliberately.** `benchmark_qualified` is weaker than the Registry's `qualified` / `deterministic` admission bar, and admission was **not** weakened to manufacture a first row. `coordination/decisions/CONTROLLER-EVAL-030-INTEGRATION-AND-REGISTRY-DISPOSITION-2026-08-28.md`.

Tesseract configuration search remains closed. Exact text is not a programme-wide blocker.

## Settled lanes — all merged, none active

Every lane below is **closed**. Do not restart, re-run or re-generate any of them.

| Lane | Result | Authority |
|---|---|---|
| **CANON-011** | 18 marketplace-derived buyer cases, **16 runnable** without contacting the buyer. Upwork buyer jobs only; Fiverr remains seller-convention evidence. Now the preferred real-demand pool for Stage-C and compound sourcing. GG-01…GG-04 are **observed representation gaps, not grammar changes** — do not reopen the Media Request Grammar because they exist. USD 0. | `CONTROLLER-CANON-011-INTEGRATION-2026-08-28.md` |
| **EVAL-024** | **16/16 frozen A-TEXT coordinates generated and sealed** — 8 fal `openai/gpt-image-2`, 8 fal `fal-ai/ideogram/v3`. Generation spend **USD 0.904**. Manifest fingerprint `1e124343…`. **These exact bytes are durable evidence and must not be regenerated.** | `CONTROLLER-EVAL-024-INTEGRATION-2026-08-28.md` |
| **EVAL-029** | Cloud Vision benchmark-qualified on both scripts, strict-disqualified, evidence sealed and portable. Incremental spend USD 0.4320. | `CONTROLLER-EVAL-029-REVIEW-SEAL-EVIDENCE-BEFORE-MERGE-2026-08-28.md` |
| **EVAL-030** | The exact 16 sealed images scored **without regeneration**: GPT Image 2 **6/8**, Ideogram v3 **1/8**, overall **7/16**. Evaluator spend **USD 0.024**; A-TEXT generation + evaluation **USD 0.928**. Registry stays 0. Directional benchmark signal, **not** a production certification or a population rate. | `CONTROLLER-EVAL-030-INTEGRATION-AND-REGISTRY-DISPOSITION-2026-08-28.md` |
| **EVAL-026** | Temporal qualification **machinery only**: 13 deterministic perturbation types covering all 9 frozen `temporal_video` capabilities — 7 with full injected-truth coverage, 2 (`action_adherence`, `camera_framing_fidelity`) negative-direction-only. **No temporal evaluator is qualified and no pass mark exists.** USD 0. | `CONTROLLER-EVAL-026-INTEGRATION-2026-08-28.md` |
| **RES-005** | 12 clips from 12 distinct source works, **12/12 passing the Resources cleanliness screen**, rights limited to CC BY / CC BY-SA / CC0 / US-Government public domain. USD 0. | `CONTROLLER-RES-005-INTEGRATION-AND-TEMPORAL-MATERIAL-RESOLUTION-2026-08-28.md` |
| **GOV-005** | Closed and merged (PR #48, `c794694`). **Do not reopen it for parallel-lane drift** — GOV-006 exists for that. | `CONTROLLER-GOV-005-CLOSURE-AND-GOV-006-TRIGGER-2026-08-28.md` |

**A-TEXT manual review is not project evidence.** Any human re-reading of the 16 images that happened
outside GitHub is **not** durable truth, must not be recorded, and must not produce a Registry row
unless a later explicit Controller decision authorises it. The accepted result is the OCR-observed
7/16 above.

## Temporal material contract — resolved at pack level

The family-4 content requirement is **pack-level**. It is **not** a requirement that every clip
contain a person, a product and on-screen text simultaneously. An individual clip needs only the
feature the perturbation applied to it requires.

**Current measured opportunity counts** — these are *coverage* counts, never claims of statistical
precision, and the family-4 gate remains per perturbation type:

| Population | Clips |
|---|---:|
| General freeze / reversal base | 12 |
| Multi-shot | 6 |
| On-screen text | 6 |
| Product region | 5 |
| Rendered-character identity | 4 |
| Photographed-face identity | 3 |

**Rendered-character and photographed-face identity are separate populations and must not be
pooled.**

**RES-005 material is not `PACK-AV-CLEAN`** and does not satisfy any speech/audio pack obligation.
`PACK-AV-CLEAN`'s own requirements — consent, verified transcripts, turn boundaries, language balance
— are unchanged. Use the semantic role name **`MAT-TEMPORAL-BASE`**; existing paths containing
`MAT-AV-MIN` remain historical artifact names and need no migration.

**Ingest scope, stated exactly:** only a **representative 3/3** clips passed EVAL-026 real-clip
ingest. The full 12-clip ingest was **not** completed — per-frame materialisation exhausted local
disk. **Do not report this as 12/12.**

**Before any real temporal checker qualification observation, all four remain required:**

1. select the actual candidate checker/instrument;
2. complete the full 12-clip ingest under a recorded execution condition;
3. freeze Controller-approved numeric pass marks **before** observations are run or inspected;
4. preserve human adjudication wherever the frozen capability map says `model_based_plus_human`.

**No temporal qualification run is authorised.**

## EMP-001 — AUTHORISED; QUALIFICATION AND A-TEXT COMPLETE

**The paid shape below has now been executed end to end.** Text-judge qualification ran, the A-TEXT
generations ran, and the images were scored. The frozen shape is kept here because it is the contract
those results were produced under — it is **not** an authorisation to run any of it again.

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

### Spend consumed so far

| Stage | Recorded figure | Where it is recorded |
|---|---|---|
| Qualification stage, cumulative through EVAL-029 | USD 1.7357905 | sealed cost excerpt + EVAL-029 decision |
| EVAL-024 A-TEXT generation | USD 0.904 | sealed generation manifest + EVAL-024 decision |
| **Cumulative through EVAL-024** | **USD 2.6397905** | sealed generation manifest + EVAL-024 decision |
| EVAL-030 A-TEXT evaluator | USD 0.024 | sealed scoring evidence + EVAL-030 decision |

> **A gap worth knowing about.** The last *committed cumulative* figure is **USD 2.6397905**, through
> EVAL-024. EVAL-030's USD 0.024 is recorded only as a stage figure, so **no single committed artifact
> states the total consumed to date including it.** The arithmetic is trivial, but the Governor does
> not write an authoritative spend total it did not find recorded. Routed as GOV-006 finding **G6-02**.
> The mechanical USD 10 ceiling and USD 6 qualification sub-cap are enforced by the live ledger, which
> stays local by design.

## Text-judge qualification freeze

Configured candidates are now:
- Anthropic `claude-sonnet-5`;
- Google `gemini-3.5-flash-lite`.

General-purpose multimodal LLMs remain **frozen as the primary exact-text judge family for EMP-001**. Cloud Vision's first OCR configuration also fails the same literalness gate. EVAL-023 moves to a local Tesseract candidate with dictionary/lexical aids disabled; API spend USD 0.

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
- mandatory human-in-the-loop exact-text review as part of the production API architecture;
- further Tesseract/OCR configuration sweeps without a new mechanism-level rationale;
- treating benchmark-grade OCR as a perfect exactness certifier;
- Registry population from text metrics until the benchmark-grade handoff is reviewed;
- broad Stage-B/C execution without their own instrument readiness;
- Production IR/Planner implementation before sufficient empirical capability evidence exists.

Authorised / active:
- **nothing.** EVAL-029, EVAL-024, EVAL-030, EVAL-026, CANON-011 and RES-005 have all returned, been
  accepted and been merged — see "Settled lanes" above. **No domain lane is currently open**, and a
  worker may not infer authorisation from any of those task files;
- the standing posture is unchanged: unrelated evaluator/capability lanes **may** proceed
  independently of exact Hindi text once the Controller opens them.

Customer-outcome CpAO remains Stage C only.

## Next gate

**Both bounded Eval closures that stood here are complete.** The EVAL-029 persistence closure and the
EVAL-024 generation closure were executed, returned, accepted and merged — see "Settled lanes" above.
Their requirement lists are preserved in their own decision records as history; they are no longer
open work.

**There is currently no active domain lane.** Nothing in this file authorises a worker to start
anything. The next tranche of work is the Controller's to open.

**What the settled state leaves genuinely open:**

1. **Registry text rows remain blocked.** The Controller has now reviewed both the sealed EVAL-029
   evidence and the actual A-TEXT scoring result, and ruled the Registry stays at 0 — because
   `benchmark_qualified` is intentionally weaker than the Registry's admission bar. **Registry
   admission must not be weakened to create a first row.**
2. **Temporal qualification is not authorised** and needs all four prerequisites above first.
3. **Prices remain incomplete.** 0 of 4 stages is price-complete and `Frontier Clouds` is still
   unidentified.
4. **HED-1 is still undecided** — which human review time counts as required cost in fully-loaded
   CpAO.
5. **Any tranche beyond EMP-001 needs explicit user approval.** The USD 10 approval covers EMP-001
   only.

**Three stream-owned documents are stale and were left for their owners to fix** (GOV-006 findings,
`governance/reviews/GOV-006-POST-PARALLEL-RECONCILIATION.md`): `eval/HANDOFF.md` still claims ₹0 API
spend and that no checker run has occurred (**G6-05**, escalated); `resources/HANDOFF.md` still calls
RES-005 unmerged (**G6-04**); `canon/HANDOFF.md` does not mention CANON-011 (**G6-06**). **This file
governs where any of them disagrees with it.**
