# EVAL-003 — Devanagari checker calibration pack readiness

**OWNER:** Eval / Capability Lab  
**STATUS:** Controller-approved task  
**AUTONOMY MODE:** autonomous implementation within this task only  
**DATE:** 24 Aug 2026

## Why this task exists

EVAL-001 defined how a checker must earn trust before its scores can be used. EVAL-002 made the evaluation plumbing runnable. Resources has now supplied **29,722 real photographed Devanagari images with source-provided transcriptions**, but with an important independence caveat: BSTD is one lineage, while IndicSTR12 and IIIT-ILST are related CVIT / IIIT Hyderabad releases and share 173 byte-identical files.

The next step is deliberately narrow: **prepare the smallest real calibration package that can later test whether our Devanagari-reading checker is trustworthy, while stopping before any human time or external checker/API spend occurs.**

This task does not benchmark any image/video generator and does not claim any checker is accurate.

## Objective

Produce a reproducible, reviewable calibration pack for the existing Devanagari transcription instrument (I1) so that a later approved task can:

1. have a Hindi first-language reader establish/verify what the selected images actually say;
2. run candidate checkers blind to those answers;
3. measure gate accuracy and transcription/diagnostic accuracy without leakage;
4. preserve a genuinely independent cross-source check.

**Stop before step 1 consumes human time and before step 2 makes any external model/API call.**

## Inputs now available

Use only material already merged to `main`:

- `src_indicstr12_devanagari` — CVIT / IIIT Hyderabad lineage
- `src_iiit_ilst_devanagari` — same lineage; 173 exact overlaps with IndicSTR12
- `src_bstd_devanagari` — Bhashini / IIT Jodhpur; independent of the two CVIT sources
- `resources/reports/RES-001-integrity-report.md`
- `resources/PROPOSED-INTEGRATION-CHANGE-RES-002-EVAL.md`
- approved EVAL-001 battery and calibration specification
- EVAL-002 harness and portable `check-vlm.mjs`

Treat all source transcriptions as **source observations, not project ground truth**, until human verification occurs.

## Required design decision for this task

### Preserve BSTD as the unseen lineage

For V0 readiness:

- **Development / calibration-pack construction:** use the CVIT lineage (`IndicSTR12` + `IIIT-ILST`) after removing exact cross-source overlap from any candidate pool.
- **Unseen cross-source reserve:** preserve BSTD for later checking of transfer to a genuinely different source lineage.

Do not inspect or select BSTD examples for their visual/content suitability during this task beyond deterministic integrity/metadata checks needed to preserve the reserve. Do not use the publisher's BSTD train/test split as an independence guarantee; Resources found two duplicate pairs crossing that split.

This does **not** permanently establish the final benchmark split. It is the V0 calibration-readiness structure and must be reported as such.

## Work package A — build a reproducible candidate sampling pipeline

Create a deterministic script/config that can produce the calibration candidate set from the CVIT lineage.

It must:

1. exclude every exact file hash that appears in both IndicSTR12 and IIIT-ILST from the candidate pool, so the same photograph cannot enter twice under different dataset names;
2. treat duplicate copies within one source as one candidate item for independence counting;
3. identify Devanagari by **script in the transcription**, not only by language labels;
4. sample independent images rather than several crops/records that are demonstrably the same file;
5. preserve source ID and source-provided transcription for provenance, but keep the transcription hidden from the later checker and human-review interfaces where required;
6. use a fixed seed / stable sorting rule so the same repository state recreates the same candidate set;
7. produce a machine-readable manifest and a plain-English summary of exactly how the sample was selected.

### Candidate-set size

Prepare **more candidates than the eventual V0 calibration needs**, not a giant benchmark. Target roughly **45–60 candidate images** so a Hindi reader can reject unreadable/ambiguous examples while still leaving around 30 independent usable items.

This is a readiness pool, not a statistical claim and not the final calibrated set.

## Work package B — represent visual difficulty without inventing truth

The approved calibration plan says clean text alone is insufficient. The candidate pool should therefore contain visibly varied real-world difficulty.

Use only **deterministic or source/metadata-derived features** that do not require an AI judgement or a Hindi-language judgement. Examples may include image dimensions, crop size, contrast/blur estimates if already available or cheaply deterministic, source lineage, and simple geometry/quality proxies.

If an intended difficulty property cannot be measured without subjective judgement, mark it `unknown` rather than inventing a label.

Do **not** create Canon-derived strata and do not claim these proxies are a validated difficulty scale.

The purpose is only to avoid accidentally choosing 50 near-identical easy crops.

## Work package C — make the checker support per-item targets

EVAL-002 left one known implementation limit: `check-vlm.mjs` currently assumes one target string for an entire run. Real calibration items each have their own source/human-established transcription.

Extend the local input format so each item can carry its own target/reference transcription.

Requirements:

- preserve the existing one-target mode for backwards compatibility unless doing so would create ambiguity;
- no change to transcription judgement semantics;
- all 27 stored historical transcriptions must still reproduce exactly under an offline regression check;
- new per-item-target behaviour must be tested with fabricated local fixtures only;
- no external checker/API call;
- if supporting per-item targets would require changing the approved property or pass criterion, STOP instead of implementing.

## Work package D — prepare the blinded Hindi-reader pack

Create a human-review package, but **do not ask anyone to complete it yet**.

The reviewer must be able to establish what is visibly written without being pulled toward an expected answer.

The pack must therefore:

- show the image/crop and stable item ID;
- hide the source-provided transcription during the first-pass transcription task;
- hide any checker output;
- hide any intended "correct/incorrect" target;
- ask the reviewer to transcribe what is visibly drawn, not what they think was intended;
- allow `cannot_read` / `ambiguous` rather than forcing a guess;
- have a separate reconciliation view that can later compare human transcription with the source-provided label after the blind pass;
- preserve original Unicode exactly;
- explain what human decisions will and will not become project ground truth.

Produce a short operator guide and a machine-readable response template.

## Work package E — design the later intact/broken gate test without fabricating Hindi evidence

The final checker calibration needs both examples where the requested target matches the image and examples where it does not, because the dangerous error is a **false pass** on a mismatch.

In EVAL-003, design the transformation only. Do not create or approve final Hindi mismatch strings by intuition.

The design should show how, **after human transcription establishes the visible text**, the later calibration run can create:

- `intact` items: target exactly equals the human-established visible transcription;
- `broken` items: target deliberately differs from the visible transcription using a reproducible rule whose linguistic validity is not relied upon for ground truth.

The human establishing visible text must remain blind to which items will later be used as intact or broken targets.

If constructing the broken target requires a Hindi-language judgement rather than a deterministic transformation, leave that step pending native-reader review rather than inventing it.

## Work package F — package the future calibration run

Create the exact run plan that would execute **after** Controller approves human/API spend.

It must state:

- number of independent items and why they are independent;
- how many are expected to become false-pass opportunities;
- which source lineage is development material and which is unseen reserve;
- how human verification happens before checker scoring;
- what is blinded at each stage;
- candidate instrument identity/version fields;
- repeat-run mechanics for the leading checker;
- gate metrics versus diagnostic metrics;
- how `cannot_read` / ambiguous human cases are handled;
- opportunity count and the practical meaning of the V0 statistical upper bound;
- exactly which later actions would incur API cost or human time.

Do not select or add a model/vendor roster in this task.

## Deliverables

At minimum:

- `eval/calibration/devanagari-v0/README.md`
- `eval/calibration/devanagari-v0/build-candidate-pool.*`
- `eval/calibration/devanagari-v0/candidate-manifest.*`
- `eval/calibration/devanagari-v0/HUMAN-REVIEW-GUIDE.md`
- `eval/calibration/devanagari-v0/human-response-template.*`
- `eval/calibration/devanagari-v0/CALIBRATION-RUN-PLAN-V0.md`
- updated `eval/scripts/check-vlm.mjs` with per-item target support
- regression/synthetic fixtures for the new input mode
- `eval/findings/EVAL-003-calibration-readiness-findings.md`
- `eval/tasks/EVAL-003-CONTROLLER-BRIEF.md`
- updated `eval/HANDOFF.md`

Exact filenames may vary slightly if the implementation requires it, but the information above must exist and be easy to find.

## Acceptance checks

EVAL-003 is complete only if all are true:

1. Candidate pool is reproducible from repository-local Resources material.
2. Exact overlap between the two CVIT datasets cannot enter as two independent items.
3. BSTD remains untouched as the unseen source-lineage reserve except for deterministic integrity/metadata operations.
4. Candidate set is approximately 45–60 independent items, or the worker explains with evidence why that range cannot be achieved.
5. No source transcription is silently promoted to project ground truth.
6. Human-review pack is blind to expected/source/checker answers on first pass.
7. `check-vlm.mjs` supports per-item targets without changing judgement semantics, and all 27 historical stored cases still reproduce exactly offline.
8. Synthetic tests cover per-item target loading and at least one deliberately malformed input.
9. No external model/API/network checker call is made.
10. No human review time is consumed.
11. No real generator is run and no capability result is written.
12. No Registry entry is created from uncalibrated evidence.

## Explicitly out of scope

- no actual Hindi-reader work;
- no checker calibration run;
- no external VLM/OCR/API calls;
- no image/video generation;
- no model/vendor roster selection;
- no Capability Registry result;
- no new battery dimension;
- no battery ladder/pass-criterion/observation-unit change;
- no creative-quality evaluator work;
- no identity-rubric calibration;
- no new dataset acquisition;
- no rights reinterpretation;
- no EVAL-004.

## Budget

- API/model spend: **₹0 / $0**
- human specialist time: **0 hours**
- new media acquisition: **0**
- use existing repo/local corpus only
- storage increase should be negligible beyond small manifests/review thumbnails if needed; do not duplicate the source corpus

## Stop conditions

STOP and report rather than improvising if:

- the CVIT material cannot produce a reasonably varied independent candidate pool;
- duplicate/lineage structure is more complicated than Resources reported;
- source transcriptions cannot be reliably joined to images without a new interpretation rule;
- per-item target support would change checker judgement semantics;
- preparing the pack requires native-Hindi judgement;
- a new evaluator/instrument is needed;
- the approved calibration plan is internally contradictory once real Resources material is represented;
- any external call, paid step or human work becomes necessary;
- normal project autonomy stop conditions fire.

## Controller questions to answer at the end

The Controller Brief must answer, in plain English:

1. What exactly will the Hindi reader see and do if we approve the next step?
2. How many independent items do we actually have after deduplication and exclusions?
3. Why is the sample varied enough to be a useful first qualification screen, and what does it still fail to represent?
4. Is BSTD still genuinely untouched as an unseen lineage reserve?
5. Did per-item target support change any checker judgement? What regression evidence proves the answer?
6. What exact human hours and API actions would the next task require?
7. What can a clean V0 calibration result legitimately let us say — and what can it still not let us say?

## Completion rule

Explain important findings in chat as they occur, write durable evidence to GitHub, commit and push, then STOP for Controller review. **Do not perform the calibration and do not start EVAL-004.**
