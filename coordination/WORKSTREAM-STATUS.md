# Workstream Status

**Snapshot, updated at integration checkpoints.**  
**Updated:** 24 Aug 2026

| Stream | Status | Current approved work | Blocking item / next gate |
|---|---|---|---|
| Canon | **CANON-003 active. 13/18 usable books Controller-accepted.** Accepted: five pre-parallel books + Lane A Books 6–7 + Lane C Books 13–15 + original Lane D Books 16–18. | `CANON-003.md` + `CANON-003-PARALLEL-EXECUTION.md` + `CANON-003-REBALANCE-01.md` | Lane B latest checkpoint reports Books 9–10 complete and Book 12 in progress; Controller audit still pending. Rebalance worker owns Books 8+11. After all remaining books return and pass audit, run one fresh integration/synthesis session with independent mechanical revalidation. |
| Eval | **EVAL-004 human-reference construction authorized.** EVAL-003 readiness is closed/merged; the existing 54-item Hindi-primary pack and protocol are frozen. | `eval/tasks/EVAL-004-HUMAN-REFERENCE.md` | Consume ≈3.5–4.5 total human hours across two independent Hindi-competent readers, freeze both passes, use exact agreement as the strict reference, exclude disagreements rather than adjudicating in V0, then stop before any checker/API/model run. Reader identities must be resolved privately before execution. |
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

Canonical crop files are materialised and shared by human-review and future checker inputs. The frozen protocol uses **two independent blind Hindi-competent readers**; exact agreement forms the strict reference. After both passes are frozen, either reader may perform the separate altered-target validity check without modifying the reference.

**EVAL-004 is now explicitly authorized.** Human-time budget is approximately **3.5–4.5 hours total** across the two readers. Before human time is consumed, the runner must re-run the existing matching/crop/blinding preflight. Reader identities stay private; repository records use `reader_a` / `reader_b` and only attest that they are distinct Hindi-competent humans.

V0 disagreements and unreadable items are **excluded from the strict gate rather than adjudicated**. This keeps EVAL-004 within the approved human budget and avoids silently turning a third opinion into a new reference rule. If fewer than roughly 20 strict-reference items survive, the task stops for Controller review.

No checker roster, API/model spend, generator work, BSTD use, Marathi stress subset, Registry entry or methodology change is authorized in EVAL-004. If deterministic altered-target tooling is not already present under the frozen rules, the human reference is still frozen and preserved; implementation becomes a later bounded task without rerunning the readers.

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
                         └──► EVAL-004 two-reader Hindi reference AUTHORIZED
                                  │
                                  └──► later checker roster/API qualification (separately gated)

Capability Registry / routing remain blocked until empirical measurements exist and Registry architecture is separately approved.
```

## Current Controller posture

- Keep accepted Canon branches untouched until final integration.
- Finish and audit remaining fixed Canon books before any schema revision or Canon-consumption experiment.
- Execute EVAL-004 only under the frozen EVAL-003 pack/protocol; no method redesign during human reference construction.
- Treat source labels as provenance/evidence, not truth.
- Keep BSTD untouched until a deliberate cross-lineage validation task.
- Do not authorize checker/API/model runs, Registry, Production IR or routing work implicitly.
