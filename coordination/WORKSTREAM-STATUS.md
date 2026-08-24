# Workstream Status

**Snapshot, updated at integration checkpoints.**  
**Updated:** 24 Aug 2026

| Stream | Status | Current approved work | Blocking item / next gate |
|---|---|---|---|
| Canon | **CANON-003 extraction closed at 16 Controller-accepted usable books.** The task minimum was 15; the 18-book target is intentionally not pursued further. | Final CANON-003 integration, independent mechanical revalidation and 16-book synthesis. | Run one fresh integration session over the accepted 16-book evidence set. Books 11–12 are deferred reserve sources, not failures and not part of the synthesis set unless separately re-authorized. |
| Eval | **EVAL-004 stopped by Controller after a single-reader 54-item pilot.** EVAL-003 readiness remains closed/merged; the two-reader calibration was not completed. | none | Decide whether to redesign checker qualification around harder, controlled generated-Hindi failure cases. Do not qualify or rank checkers from the EVAL-004 pilot. |
| Resources | **RES-001/002 closed and merged.** | none | Pending optional Controller action on `eval/PROPOSED-INTEGRATION-CHANGE-EVAL-003-RESOURCES.md`; otherwise remain closed. |

## Canon

Controller-accepted usable books total **16**. This exceeds CANON-003's minimum success threshold of 15. On 24 Aug 2026 the Controller chose to stop extraction above the minimum but below the 18-book target rather than spend additional time on diminishing-return sources. See `canon/decisions/CANON-003-STOP-AT-16-2026-08-24.md`.

Accepted parallel work:

- Lane A: Books 6–7 accepted and stopped.
- Rebalance lane: Book 8 accepted.
- Lane B: Books 9–10 accepted.
- Lane C: Books 13–15 accepted and stopped.
- Original Lane D: Books 16–18 accepted/frozen.
- Together with the five usable pre-parallel books, the confirmed usable synthesis set is **16 books**.

The Controller audit for Books 8–10 is recorded at `coordination/CANON-003-BOOKS-08-10-AUDIT.md`. It verifies branch isolation against common base `4cbe25783cb2bccf1584c792d44ca54adf71bf3b`, book-specific fresh checkpoints before historical comparison, representative-section/provenance/visual procedure, and frozen-method discipline. The worker validators were ephemeral and are therefore not treated as independently rerun evidence; final integration must mechanically revalidate every accepted book before completion is claimed.

Book 7 identity correction remains durable: the preselected Freeman artifact is *The Photographer's Eye: A Graphic Guide* (2013), not the 2007 *The Photographer's Eye*. Final synthesis must retain that corrected identity.

Deferred reserve sources:

- Book 11 — Christopher Kenworthy, *Master Shots* — `work/canon-003-rebalance-d`.
- Book 12 — Michael Ondaatje, *The Conversations* — `work/canon-003-b`.

These are **deferred, not failed or blocked**. Any later worker output for them is outside the frozen 16-book evidence set unless the Controller separately decides to expand the batch.

No accepted worker branch is merged individually. Keep accepted branches untouched until one fresh final integration/synthesis session reconciles all reviewed lanes and reruns mechanical validation.

No schema, granularity, visual-pass, ontology-vocabulary or Canon-consumption change is allowed until the batch-level synthesis is complete.

## Eval

EVAL-003 readiness is merged. The prepared pack is **173 eligible Hindi-labelled unique photographs → 54 selected → 54 distinct photograph hashes** under `--overlap-policy admit-once --language-filter hindi --target-n 54`.

Two related CVIT releases are treated as one source lineage. Their annotation disagreement (725 identical / 357 different across 1,082 one-to-one matched regions) is evidence that source labels cannot be promoted directly to ground truth; it is not human-performance evidence and yields no evaluator threshold.

Canonical crop files were materialised and the original EVAL-004 protocol required **two independent blind Hindi-competent readers**, with exact agreement forming the strict reference.

**Controller override, 24 Aug 2026:** EVAL-004 was stopped after one complete 54-item Reader-A pilot. A second person informally looked at the material but did not perform the frozen independent blind pass, so there is no protocol-compliant Reader B and no two-reader reference. The pilot is exploratory only. See `eval/decisions/EVAL-004-STOP-2026-08-24.md`.

Consequently, Reader A is not ground truth; no checker may be qualified, disqualified, ranked, or entered into the Capability Registry from EVAL-004; and no accuracy / false-pass / Hindi-reading qualification claim may be made from this run.

The pilot's design lesson is that basic photographed-signage words may be too weak a proxy for the downstream failure state of interest: a multimodal checker silently normalizing or autocorrecting subtly malformed **generated** Hindi text. If Eval resumes, the next gate is a Controller decision on a harder controlled-failure qualification design, not automatic completion of the old two-reader signage run.

No checker roster, API/model spend, generator work, BSTD use, Marathi stress subset, Registry entry or methodology change is currently authorized.

## Cross-stream dependency chain

```text
CANON-003 extraction CLOSED at 16 accepted books
        │
        └──► one fresh CANON-003 integration/synthesis
                 │
                 ├──► independent mechanical revalidation of all 16 accepted books
                 ├──► 16-book multi-source synthesis
                 └──► possible consolidated Canon-method revision task

Books 11–12 ──► deferred reserve evidence only; not required for current synthesis

RES-002 corpus ──► EVAL-003 readiness MERGED
                         │
                         └──► EVAL-004 single-reader pilot STOPPED
                                  │
                                  └──► next Eval gate: decide whether to redesign a harder checker-qualification battery

Capability Registry / routing remain blocked until empirical measurements exist and Registry architecture is separately approved.
```

## Current Controller posture

- Treat the accepted **16 books** as the frozen CANON-003 synthesis set.
- Keep accepted Canon branches untouched until final integration.
- Do not wait for Books 11–12; they are deferred reserve sources.
- Start one fresh CANON-003 integration/synthesis session with independent mechanical revalidation.
- Do not revise Canon schemas/method until that synthesis is complete.
- Treat EVAL-004 as a stopped exploratory pilot, not a completed calibration.
- Do not promote Reader A to ground truth or qualify checkers from the pilot.
- Treat source labels as provenance/evidence, not truth.
- Keep BSTD untouched until a deliberate cross-lineage validation task.
- Do not authorize checker/API/model runs, Registry, Production IR or routing work implicitly.
