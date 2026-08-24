# Workstream Status

**Snapshot, updated at integration checkpoints. Detail lives in each stream's task brief / handoff.**  
**Updated:** 24 Aug 2026

| Stream | Status | Current approved work | Blocking item / next gate |
|---|---|---|---|
| Canon | **CANON-003 active, parallel extraction with one execution rebalance.** Five usable books complete at the pre-parallel checkpoint. Lane D Books 16–18, Lane A Books 6–7, and Lane C Books 13–15 are now Controller-audited accepted, bringing the currently confirmed usable count to **13**. Lane B Book 9 is worker-complete but not yet Controller-audited. | `CANON-003.md` + `CANON-003-PARALLEL-EXECUTION.md` + `CANON-003-REBALANCE-01.md` | Lane A and C stop and remain untouched. Remaining execution: B→Books 10+12 (plus Controller audit of completed Book 9); fresh rebalance branch→Books 8+11. After all 18 are reviewed, run one fresh integration/synthesis session with mechanical revalidation of every per-book output. No schema changes or Canon-consumption experiments during the batch. |
| Eval | **EVAL-003 substantive finalization passed Controller audit; documentation consistency cleanup active.** The Hindi-primary pack and protocol are mechanically in place, but operator-facing files still contain stale pre-finalization instructions, so the branch is not yet merge-ready and no calibration is approved. | `EVAL-003.md` + `EVAL-003-CORRECTION-PASS.md` + `EVAL-003-FINALIZATION-PASS.md` + `EVAL-003-DOC-CONSISTENCY-CLEANUP.md` | Preserve the 173-eligible / 54-Hindi pack, matcher, crop pipeline, two-reader protocol and Resources proposal unchanged. Remove stale 202-item/0-Hindi/browser-crop/pending-composition instructions, fix V0 reproduction commands, sweep current docs, then return. No human/API/model work yet. |
| Resources | **RES-001/002 closed and merged. No active task.** | none | Stay closed unless a Controller-approved cross-stream correction or new sourcing requirement warrants a new task. |

## Canon live-review note

**Lane A is accepted for Books 6–7 and now stops.** Git history verifies Book 6 fresh checkpoint `c8cb9d4` and Book 7 fresh checkpoint `5f95755` precede their historical searches/findings. Compare-to-base shows only source-specific Book 6/7 knowledge plus Lane A findings/checkpoint files. Book 8 has no committed extraction on A and remains assigned to `work/canon-003-rebalance-d`.

A's most important provenance correction is that its preselected Freeman artifact was misidentified in the inventory: the local file is **Michael Freeman, _The Photographer's Eye: A Graphic Guide_ (2013)**, not the 2007 _The Photographer's Eye_. This is retained as an inventory identity correction, not treated as a post-result source substitution: the same local artifact had been preselected and still fits the intended photography/composition coverage. Freeman also exposed a distinct visual-provenance trap: a Calibre-reflowed PDF can render pages while still not preserve the authored printed page, so "PDF" alone cannot justify page-level visual completeness.

**Lane C is accepted for Books 13–15 and now stops.** Git history shows the required alternating fresh/post-history pattern: `1222919` (Hopkins fresh) → findings; `a699a49` (Heath fresh) → findings; `f992d69` (Sutherland fresh) → findings. Shared ledger/synthesis/Controller/Handoff files were untouched.

Lane C's strongest recurring finding is an evidence-vocabulary gap across all three persuasion books: `empirical_within_source` only represents a source's own reported measurement, while the lane encountered claimed-but-unreported measurement, cited third-party research, and a source mixing its own experiment with external studies. Each case was kept faithful through caveats rather than changing the frozen schema. Final cross-lane synthesis, not the lane, decides whether that warrants one consolidated revision.

The durable Controller audit is `coordination/CANON-003-LANE-A-C-AUDIT.md`. The workers report SPEC-03/04/05 mechanical validation passes, but their validators were scratchpad tools and were not committed; therefore the final integration session must independently revalidate every per-book output before closing CANON-003.

Lane D remains accepted and frozen. The remaining live work is Lane B Books 10 and 12 plus Book 9 Controller audit, and the rebalance worker Books 8 and 11. The fixed 18-book source set is unchanged.

## Eval live-review note

The finalization return fixed the substantive gates. `work/eval` contains the Controller finalization task; the Hindi-primary selection summary reports **173 eligible Hindi-labelled photographs and 54 selected, all 54 with distinct hashes**; the one-to-one matcher has a committed adversarial self-test where two A regions contend for one B; the run plan and reader guide use **two independent Hindi-competent readers** and allow either reader to perform the later altered-target validity check only after the reference is frozen; the review/checker artifacts reference the same materialised crop hashes; and the Eval→Resources proposal now records the full-scene correction, **375 + 176 locally paired records**, and the denominator-specific **173/176** overlap result.

The branch is still not merge-ready because the Controller Brief's claim that stale contradictions were removed is not true across the active documents. `EVAL-003-calibration-readiness-findings.md` still presents the old **202-item overlap-excluded / 0-Hindi** pool as current, says browser-only crops/no transformed images, and calls crop materialisation unresolved. The README also contains followable old-state instructions, including reproduction without the approved Hindi-primary arguments and stale pool/source-composition prose; `annotator-disagreement.json` still says the shared files are excluded; the retained composition note still contains a later recommendation saying the decision is open. These are documentation/operational consistency defects, not a reason to reopen the method.

Controller therefore opened `eval/tasks/EVAL-003-DOC-CONSISTENCY-CLEANUP.md`. No new research, sample redesign, human review, API/model work, EVAL-004 or Registry work is authorized. After the cleanup returns cleanly, the next Controller decision is whether to merge EVAL-003 readiness and separately authorize the two-reader human pass.

## Cross-stream dependency chain

```text
CANON-003 parallel/rebalanced book extractions
        │
        └──► fresh CANON-003 integration/synthesis
                 │
                 └──► evidence for a later consolidated Canon-method decision

RES-002 closed corpus ──► EVAL-003 Hindi-primary readiness cleanup
                               │
                               └──► Controller merge review
                                      │
                                      ├──► later two-reader human calibration (not yet approved)
                                      └──► later API checker qualification (not yet approved)

Capability Registry / routing remain blocked until empirical measurements exist and the Registry architecture is separately approved.
```

## Current Controller posture

- Preserve the fixed 18-book source set; rebalance only explicitly not-started work under written Controller amendment.
- Keep accepted Lane A, Lane C and Lane D branches untouched until integration.
- Treat source annotations as provenance/evidence, not truth; reference construction remains two-reader and blind.
- Spend the first I1 calibration budget on the Hindi-facing capability actually needed, not a zero-Hindi proxy pack.
- Do not reopen EVAL-003 methodology for documentation cleanup; make current operator instructions match the already-approved Hindi-primary artifacts.
- Do not reopen Resources for ordinary cleanup; use the cross-stream proposal path.
- Do not allow worker-recommended next steps to become automatic tasks.
- Canon-consumption/planning experiments remain paused.
