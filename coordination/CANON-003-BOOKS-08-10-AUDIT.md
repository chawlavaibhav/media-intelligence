# CANON-003 Controller audit — Books 8–10

> **HISTORICAL — Controller audit record, not current state.** Classified `HISTORICAL` by GOV-001 on
> 25 Aug 2026. The findings below remain **evidentially valid** for the CANON-003 batch and were not
> altered. They describe a batch that has since closed at 16 accepted books and been superseded by
> the Audit Gate v0.2 method; live Canon is now 19 sources. Any lane, branch or in-progress status
> named below is finished. Current state: `PROJECT-MEMORY.md` and `coordination/CONTROL-STATE.md`.


**Date:** 24 Aug 2026  
**Decision:** Books 8, 9 and 10 are **Controller-accepted usable CANON-003 books**, subject to the batch-wide final integration requirement that all accepted outputs be independently mechanically revalidated before merge/reconciliation.

This audit is read-only with respect to the active worker branches. `work/canon-003-b` and `work/canon-003-rebalance-d` remain untouched.

## Scope audited

- **Book 8:** John Alton, *Painting With Light*, chapter 2, "Motion Picture Illumination" — branch `work/canon-003-rebalance-d`.
- **Book 9:** Roy Thompson & Christopher J. Bowen, *Grammar of the Edit*, 2nd ed., chapters 3–5, printed pp.55–109 — branch `work/canon-003-b`.
- **Book 10:** Walter Murch, *In the Blink of an Eye*, revised 2nd ed., printed pp.1–25 — branch `work/canon-003-b`.

## Procedure checks

### 1. Branch isolation / changed-file scope

Compared each worker branch against the common parallel base `4cbe25783cb2bccf1584c792d44ca54adf71bf3b`.

**Lane B:** only lane-local findings/issues/checkpoint plus Book 9 and Book 10 knowledge directories are changed. No locked shared batch ledger, synthesis, Controller Brief, or `canon/HANDOFF.md` change exists relative to the common base. No Book 11 artifact exists; no Book 12 knowledge artifact exists yet.

**Rebalance lane:** only lane-local findings/issues/checkpoint plus Book 8 knowledge directory are changed. No locked shared batch file is changed relative to the common base.

Result: **PASS** for isolation/scope.

### 2. Book-specific fresh checkpoint before historical comparison

Verified repository ordering:

- Book 8 fresh checkpoint: `ab2a833a3a3318192fe01e5a38c76bc88b34dbde`.
  - Comparing this checkpoint to the rebalance branch head shows exactly one later commit containing only the Book 8 findings, rebalance checkpoint and rebalance issue file; the frozen knowledge directory is not modified post-checkpoint.
- Book 9 fresh checkpoint: `ddef98d3104ab5056ed21e2fd0931e5b4c86666f`.
  - Book 9 findings are added only after this checkpoint. The next book's fresh extraction begins later.
- Book 10 fresh checkpoint: `72a6b31c2c19bc648c71b0613644c7f0766b2c72`.
  - Comparing this checkpoint to current Lane B head shows only Book 10 findings and lane checkpoint updates; Book 10 knowledge is not modified after the checkpoint.

Result: **PASS** for the sealed-history/freshness rule.

### 3. Representative section / provenance / visual handling

**Book 8:** coherent complete chapter 2; provenance identifies the UC Press reprint and records EPUB integrity limits. Visual pass recovered section headings stored as SVG outlines, inspected diagrammatic evidence, and records `verified_figure_level`. Ambiguous visual evidence is preserved as uncertainty rather than guessed.

**Book 9:** coherent tightly connected chapters 3–5; printed pp.55–109. Visual pass is page-level and materially changes the extraction: shot-relation diagrams and in-artwork labels are not recoverable from plain text. Source/publisher/edition and page span are explicit.

**Book 10:** coherent contiguous pp.1–25 containing the Rule of Six in full. The source is a scanned two-page-spread PDF; the extraction records and remedies line interleaving by respecting page geometry. Page-level visual verification found zero figures in the selected span rather than assuming a visual pass was unnecessary.

Result: **PASS** for representative-section/provenance/visual procedure.

### 4. Frozen method discipline

Across the audited outputs:

- no SPEC-01/03/04/05 change was made;
- no ontology relation/type was added;
- schema insufficiencies were logged instead of repaired;
- zero or partial product binding was allowed rather than forcing all source knowledge into Creative IR;
- post-history findings are recorded as findings/proposals rather than back-filled into the frozen source objects.

Result: **PASS** for frozen-instrument discipline.

## Book-level output summary

| Book | SourceKnowledge | Systems | Ontology terms | Relations | Concepts | Bindings | Visual |
|---|---:|---:|---:|---:|---:|---:|---|
| 8 — *Painting With Light* | 27 | 3 | 22 | 9 | 3 | 6 | verified figure-level |
| 9 — *Grammar of the Edit* | 60 | 5 | 48 | 15 | 6 | 11 | verified page-level |
| 10 — *In the Blink of an Eye* | 39 | 4 | 23 | 9 | 3 | 8 | verified page-level, zero figures |

These counts are taken from the frozen worker outputs/findings and checkpoint commit records.

## Substantive findings retained for final synthesis

### Book 8

- EPUB hierarchy can fail silently when major headings are image glyphs while deeper text headings survive; a text-only hierarchy can therefore appear coherent while being inverted.
- Figure-only evidence can be sufficient for diagram-argued books even when page layout is irrelevant.
- One source can interleave durable geometry/perception knowledge, obsolete technology, and historically bounded studio convention under the same claim types; shelf life is not mechanically inferable from claim type.
- A visual demonstration can remain genuinely under-determined even after the figure is inspected.

### Book 9

- Same-author companion books are not independent origins for cross-source convergence even when they have distinct source IDs.
- Shared concepts can be systematically transformed by production role: shooting-side camera actions become editing-side selection constraints.
- SPEC-03's source-local relation vocabulary loses some non-hierarchical/sibling/orthogonal structure; this is evidence to synthesize later, not a batch-time schema change.
- Visual information inside artwork can disappear silently from text extraction.

### Book 10

- `priority_order` carries rank but not interval/weight; Murch's 51/23/10/7/5/4 ordering is materially distorted if reduced to rank alone.
- Practitioner remedies can act on the decision-maker/working conditions rather than on media material, stressing `executable_by` without justifying a batch-time vocabulary change.
- Interleaving can be an extraction-geometry failure rather than source corruption; source-integrity blocking should distinguish those cases in synthesis.
- Visual dependence follows mode of argument, not domain: Book 9 is figure-dependent while Book 10 has zero figures despite the same broad subject.
- Long-form lecture/interview material can defer answers far beyond a normal extraction window; local completeness is a source-shape risk for Book 12.

## Mechanical-validation caveat

Worker checkpoints report their ephemeral scratchpad validators passed SPEC-03 rules 1–7, SPEC-04 rules 1–9 and SPEC-05 layer constraints. Those exact validator scripts were not committed, so the Controller cannot honestly claim an independent exact validator rerun from repository state alone.

Therefore:

- this audit accepts Books 8–10 as **usable / Controller-accepted** for CANON-003;
- it does **not** waive final mechanical validation;
- the fresh final integration session must independently revalidate every accepted book's YAML and cross-file references before any merged CANON-003 completion claim.

## Controller decision

**ACCEPT Books 8, 9 and 10.**

CANON-003 accepted usable count advances from **13/18 to 16/18**.

Remaining fixed books:

- Book 11 — Christopher Kenworthy, *Master Shots* — owned by `work/canon-003-rebalance-d`.
- Book 12 — Michael Ondaatje, *The Conversations* — owned by `work/canon-003-b`.

Do not merge the accepted worker branches individually. Keep them untouched until one fresh final CANON-003 integration/synthesis session reconciles all accepted lanes and reruns mechanical validation.