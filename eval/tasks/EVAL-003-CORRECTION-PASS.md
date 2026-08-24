# EVAL-003 — Controller correction pass

**Status:** Controller-approved bounded correction pass · 24 Aug 2026  
**Task identity:** remains **EVAL-003**; this does not open EVAL-004  
**Autonomy mode:** autonomous implementation inside the corrections below only  
**Spend:** ₹0 / $0 API · 0 human specialist hours · 0 generations · 0 new acquisition

## Why this pass is required

The first EVAL-003 return contains useful work: deterministic CVIT candidate selection, hash-based deduplication, an untouched BSTD reserve, a blinded review interface, per-item checker targets, and a 27-case historical regression showing the checker judgement path did not change.

It is **not yet approved for merge or for human/API calibration**. Several claims and protocol details would make the later calibration harder to interpret than the evidence supports. Correct those issues without redesigning the approved EVAL-001/002 battery or expanding scope.

Before editing, fetch `origin/main` and merge current `origin/main` into `work/eval` normally. Do not rewrite history. Main has received Controller control commits since the worker started, including this correction contract, so the worker branch must be current before the next review.

## Preserve these parts unless a correction below requires a local change

- per-item target support in `eval/scripts/check-vlm.mjs`;
- the existing 27 historical transcription regression and malformed-input rejection tests;
- deterministic candidate construction from the CVIT lineage;
- exact-hash exclusion of cross-source duplicates and collapse of within-source duplicate copies;
- BSTD as an untouched unseen source-lineage reserve;
- first-pass blinding from source transcription and checker output;
- no human review, external model/API call, generator run, Registry entry, battery change, or EVAL-004 work.

## Required corrections

### 1. Reframe the cross-dataset disagreement result

The current artifacts describe the observed 67% exact agreement, and a derived ~73% figure, as a human-performance ceiling. That is not supported.

What is actually observed is **agreement between two dataset annotation sets on a subset of byte-identical images under our region-matching procedure**. We have not established from repository evidence that the annotators were independent, equally qualified, blind, or representative of the humans we will use. The overlap set may also be selected/non-representative.

Correct every current EVAL-003 artifact so that:

- the result is described as **cross-dataset annotation disagreement**, not a human-performance ceiling;
- it is evidence that source labels are not interchangeable with project ground truth;
- it is not used to say what accuracy a machine can or cannot sensibly exceed;
- the EVAL-001 policy about measured inter-annotator agreement remains a design rule, but no qualifying human inter-reader number is claimed until our own controlled reader protocol actually measures one.

Keep evidence and inference explicitly separate.

### 2. Make region matching one-to-one before quoting any disagreement rate

The current code chooses the best IIIT-ILST region independently for each IndicSTR12 region. That permits one region on one side to be reused for more than one match on the other side.

Replace this with a **deterministic one-to-one matching rule** within each shared photograph: once a region is matched, it cannot be reused. Preserve an explicit geometry threshold and record the matching method.

Add a fabricated regression case in which two regions on side A both prefer one region on side B. The test must prove only one of them can claim that B region.

Regenerate `annotator-disagreement.json` and every number derived from it. Do not preserve the old 1,082 / 67% figures merely for narrative continuity if the corrected matcher changes them.

### 3. Remove the unsupported “convention only” interpretation

The current builder labels two strings as `convention_only` when they become equal after deleting selected Devanagari marks. That is a mechanical Unicode transformation, not a linguistic judgement. Removing virama, nukta, anusvara or chandrabindu can change the reading.

Remove the linguistic label and the ~73% “forgiving conventions” agreement claim.

If the mechanical diagnostic is retained because it is useful for debugging, name it literally, for example `equal_after_selected_mark_removal`, define exactly which code points are removed, and **never count it as agreement or as a validated spelling/convention category**.

### 4. Fix the candidate-count explanation

The current prose shows `551 - 173 - 3 = 202`, which is arithmetically misleading.

Explain the units correctly. There are 173 **unique shared hashes**, but each shared hash appears once in each source and the builder excludes both source records from the candidate pool. Therefore distinguish at minimum:

- labelled source records found per source;
- unique cross-source shared hashes;
- source records removed because of those shared hashes;
- within-source duplicate records collapsed;
- final eligible unique photographs.

Regenerate the summary fields so a reader can reproduce the arithmetic without reverse-engineering the code.

### 5. Measure Hindi / Marathi composition instead of assuming “Hindi”

Resources deliberately acquired both `hindi/` and `marathi/` material from IndicSTR12. The candidate filenames preserve that source provenance.

Report the **source-provided language-label composition** of:

1. the eligible candidate pool; and
2. the selected 54-item readiness pool,

using only provenance already present in the acquired source/file naming or source metadata. Include `unknown` if a source record cannot be classified deterministically. Do **not** infer language from the Devanagari string itself.

Explain the practical consequence for reviewer qualification. If the pack contains Marathi material, do not describe “Hindi first-language reader” as automatically sufficient for every item. The future readers must have language competence appropriate to the material they are asked to adjudicate, or those items must be treated as outside their competence.

Do not rebalance the sample merely to make the composition look cleaner unless a separate validity reason requires it; report first.

### 6. Redesign the future human protocol around two independent blind readers

The next calibration stage must no longer depend on one person's transcription becoming the reference.

Design the pack/run plan so **two independent readers** each perform the first pass on the same canonical crops:

- both are blind to source-provided transcription, checker output, intact/broken assignment, and the other reader's response;
- each response is frozen separately before reconciliation;
- `cannot_read` and `ambiguous` remain valid outcomes;
- an item may enter the primary V0 reference set automatically only when both readers mark it readable and their exact transcriptions agree under the already-declared Unicode normalization policy;
- disagreements, ambiguity, or language-competence problems are reported and excluded from the primary gate set unless a later, separately specified adjudication step resolves them;
- never silently choose one reader as truth.

The two-reader agreement generated by this controlled protocol is the first number that may be discussed as **our measured inter-reader agreement for this pack**. Even then, describe it as reference/reviewer reliability under this protocol, not a universal human-performance ceiling.

Revise the operator guide, response schema/templates, run plan, and human-time estimate accordingly. Estimate per-reader and total time separately; do not reuse the current one-reader total.

### 7. Solve crop materialisation before asking for human time

Crop materialisation is a prerequisite to calibration validity, not work to defer until after human approval.

Create a deterministic local crop-materialisation path now, at zero human/API spend, so the **same canonical crop pixels** can later be shown to both human readers and sent to candidate checkers.

Requirements:

- use explicit, verifiable crop-box semantics;
- verify generated crop width/height against the recorded box geometry;
- record a hash for each materialised crop so later stages can prove they used the same pixels;
- have the review pack and future checker-item manifest reference the same canonical crop artifact;
- keep crop media out of git. Source rights are internal research/evaluation only and the repository must not become a redistribution surface;
- commit only the materialisation code, manifests/hashes/metadata needed for reproducibility, and ignore rules;
- do not depend on an unverified `sips` offset interpretation. Use a local image implementation whose crop semantics can be tested. If this cannot be done without an external service or a material architecture change, STOP and report.

Add at least one fabricated image/crop test where expected output dimensions and pixel placement are mechanically known.

### 8. Remove machine-specific absolute paths from committed evidence

`selection-summary.json` currently records `/Users/...` worktree paths. Committed artifacts must not depend on one machine's directory layout.

Replace them with repository-relative logical paths, source IDs, or explicit CLI provenance that remains portable. Add a final scan of current EVAL-003 committed artifacts for machine-specific absolute paths such as `/Users/`, local worktree roots, or equivalent Windows home paths.

The scripts may accept an explicit local `--corpus-root`; the **committed evidence** must not preserve the operator's private absolute path.

### 9. File the Resources cross-stream correction; do not edit Resources directly

Create an Eval-owned proposed integration note, for example:

`eval/PROPOSED-INTEGRATION-CHANGE-EVAL-003-RESOURCES.md`

At minimum it should ask Resources to reconcile these evidence-backed points:

1. `resources/sources/src_indicstr12_devanagari.md` describes the acquired material as “cropped word images,” while EVAL-003 observed full scene photographs with multiple region boxes in the locally acquired material. State the observed evidence and ask Resources to correct/clarify its own record.
2. EVAL-003 could locally pair usable annotations with 375 IndicSTR12 and 176 IIIT-ILST images. Ask Resources to distinguish **media acquired** from **locally paired image+annotation records** where its summaries currently risk implying every acquired image has a locally usable transcription. Do not claim Resources is wrong about publisher-level annotation availability without evidence.
3. On the locally paired IIIT-ILST subset, 173 of 176 records are byte-identical to an IndicSTR12 file, leaving 3 unique labelled images. Make clear that this is a different denominator from Resources' full-source duplicate percentage, not a contradiction of it.

Follow the project boundary: Eval proposes; Resources owns any Resources-file correction; Controller decides integration.

## Files expected to change

At minimum inspect and update as applicable:

- `eval/calibration/devanagari-v0/build-candidate-pool.py`
- `eval/calibration/devanagari-v0/build-review-pack.py`
- new deterministic crop-materialisation code and its synthetic fixture/test
- `eval/calibration/devanagari-v0/selection-summary.json`
- `eval/calibration/devanagari-v0/annotator-disagreement.json`
- candidate/review manifests if new composition/crop provenance fields are required
- `eval/calibration/devanagari-v0/README.md`
- `eval/calibration/devanagari-v0/HUMAN-REVIEW-GUIDE.md`
- `eval/calibration/devanagari-v0/CALIBRATION-RUN-PLAN-V0.md`
- human response schema/templates
- `eval/findings/EVAL-003-calibration-readiness-findings.md`
- `eval/tasks/EVAL-003-CONTROLLER-BRIEF.md`
- `eval/HANDOFF.md`
- `eval/PROPOSED-INTEGRATION-CHANGE-EVAL-003-RESOURCES.md`

Do not perform unrelated cleanup or redesign.

## Acceptance checks

The correction pass is ready for Controller review only when all are true:

1. Corrected disagreement matching is deterministic, one-to-one, and covered by an adversarial synthetic test.
2. All disagreement statistics and derived prose are regenerated from the corrected matcher.
3. No current EVAL-003 artifact calls the cross-dataset rate a human-performance ceiling or treats mark-stripping as validated “convention-only” agreement.
4. Candidate-count arithmetic explicitly reconciles unique shared hashes with the number of source records removed.
5. Hindi/Marathi/unknown source-label composition is reported for both eligible and selected pools.
6. The human protocol uses two independent blind readers and specifies conservative handling of disagreement/ambiguity/language competence.
7. Canonical crops can be materialised locally and reproducibly; dimensions and hashes are verified; crop bytes remain git-ignored; both human and future checker paths use the same crop identity.
8. Current EVAL-003 committed artifacts contain no machine-specific absolute paths.
9. Existing per-item target behaviour still reproduces all 27 historical stored cases with 0 mismatches, and malformed-input tests still pass.
10. The Eval→Resources proposed integration note exists and does not directly edit Resources files.
11. BSTD remains untouched except for the already permitted deterministic directory/integrity metadata operations.
12. No human review, external model/API/network checker call, generation, Registry result, new acquisition, battery change, or EVAL-004 work occurs.

## Return to Controller

Update `eval/tasks/EVAL-003-CONTROLLER-BRIEF.md` so it clearly separates:

- what was wrong in the first return;
- what was mechanically corrected;
- the new measured counts/statistics;
- what still requires human judgement;
- the revised human protocol and estimated human effort;
- whether crop identity is now reproducibly solved;
- any remaining blocker before human/API calibration.

Commit and push `work/eval`, then STOP for Controller review. **Do not start the readers, select a checker roster, spend API money, or start EVAL-004.**
