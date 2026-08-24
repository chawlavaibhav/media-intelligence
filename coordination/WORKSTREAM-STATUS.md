# Workstream Status

**Snapshot, updated at integration checkpoints.**  
**Updated:** 24 Aug 2026

| Stream | Status | Current approved work | Blocking item / next gate |
|---|---|---|---|
| Canon | **CANON-003 active. 13/18 usable books Controller-accepted.** Accepted: five pre-parallel books + Lane A Books 6–7 + Lane C Books 13–15 + original Lane D Books 16–18. | `CANON-003.md` + `CANON-003-PARALLEL-EXECUTION.md` + `CANON-003-REBALANCE-01.md` | Lane B latest checkpoint reports Books 9–10 complete and Book 12 in progress; Controller audit still pending. Rebalance worker owns Books 8+11. After all remaining books return and pass audit, run one fresh integration/synthesis session with independent mechanical revalidation. |
| Eval | **EVAL-003 readiness complete and merged to `main` via PR #3.** Hindi-primary pack, two-reader protocol, crop pipeline and checker plumbing are ready; no calibration has been run. | No active Eval execution task. EVAL-001/002/003 readiness are closed/merged. | Next gate is explicit authorization of ≈3.5–4.5 hours across two Hindi-competent readers. Checker roster/API spend is a separate later decision. EVAL-004 and Registry remain unopened. |
| Resources | **RES-001/002 closed and merged.** | none | Pending optional Controller action on `eval/PROPOSED-INTEGRATION-CHANGE-EVAL-003-RESOURCES.md`; otherwise remain closed. |

## Canon

Lane A Books 6–7 and Lane C Books 13–15 are Controller-audited accepted and stopped. Original Lane D Books 16–18 remain accepted/frozen. Together with the five usable pre-parallel books, the confirmed usable count is **13**.

Book 7 identity correction is durable: the preselected Freeman artifact is *The Photographer's Eye: A Graphic Guide* (2013), not the 2007 *The Photographer's Eye*. Final synthesis must retain that corrected identity.

The fixed 18-book source set remains unchanged. Execution ownership:

- A: stopped; Book 8 moved out.
- B: Books 9, 10 and 12; latest worker checkpoint reports 9 and 10 complete, 12 in progress. Book 11 moved out.
- C: stopped.
- Rebalance worker: Books 8 and 11.
- Original D: stopped/frozen with Books 16–18 accepted.

No schema, granularity, visual-pass, ontology-vocabulary or Canon-consumption change is allowed until the batch-level synthesis.

## Eval

EVAL-003 readiness is merged. The active pack is **173 eligible Hindi-labelled unique photographs → 54 selected → 54 distinct photograph hashes** under `--overlap-policy admit-once --language-filter hindi --target-n 54`.

Two related CVIT releases are treated as one source lineage. Their annotation disagreement (725 identical / 357 different across 1,082 one-to-one matched regions) is evidence that source labels cannot be promoted directly to ground truth; it is not human-performance evidence and yields no evaluator threshold.

Canonical crop files are materialised and shared by human-review and future checker inputs. The protocol uses **two independent blind Hindi-competent readers**; exact agreement forms the strict reference. After both passes are frozen, either reader may perform the separate altered-target validity check without modifying the reference.

Before merge, the branch recorded: matcher adversarial self-test passing, crop geometry/identity and blinding checks passing, 27/27 historical checker cases re-scored with 0 judgement mismatches, local harness checks green, no absolute machine paths, and BSTD untouched. No human/API/model/generator work was performed.

The final stale operator-facing findings were removed by replacing the active findings file with an authoritative current-state summary; superseded zero-Hindi/single-reader/browser-crop states remain only in Git history.

## Cross-stream dependency chain

```text
CANON-003 remaining book work
        │
        └──► Controller audits
                 │
                 └──► one fresh CANON-003 integration/synthesis
                          │
                          └──► possible consolidated Canon-method revision task

RES-002 corpus ──► EVAL-003 readiness MERGED
                         │
                         ├──► two-reader Hindi calibration (not yet authorized)
                         └──► checker qualification/API runs (separately gated)

Capability Registry / routing remain blocked until empirical measurements exist and Registry architecture is separately approved.
```

## Current Controller posture

- Keep accepted Canon branches untouched until final integration.
- Finish and audit remaining fixed Canon books before any schema revision or Canon-consumption experiment.
- EVAL-003 needs no further readiness cleanup.
- Human calibration is the next Eval decision, not an automatic continuation.
- Treat source labels as provenance/evidence, not truth.
- Keep BSTD untouched until a deliberate cross-lineage validation task.
- Do not open EVAL-004, Registry, Production IR or routing work implicitly.
