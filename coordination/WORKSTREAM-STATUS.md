# Workstream Status

**Snapshot, updated at integration checkpoints.**  
**Updated:** 24 Aug 2026

| Stream | Status | Current approved work | Blocking item / next gate |
|---|---|---|---|
| Canon | **CANON-003 active. 13/18 usable books Controller-accepted.** Accepted: five pre-parallel books + Lane A Books 6–7 + Lane C Books 13–15 + original Lane D Books 16–18. | `CANON-003.md` + `CANON-003-PARALLEL-EXECUTION.md` + `CANON-003-REBALANCE-01.md` | Lane B latest checkpoint reports Books 9–10 complete and Book 12 in progress; Controller audit still pending. Rebalance worker owns Books 8+11. After all remaining books return and pass audit, run one fresh integration/synthesis session with independent mechanical revalidation. |
| Eval | **EVAL-004 stopped by Controller after a single-reader 54-item pilot.** EVAL-003 readiness remains closed/merged; the two-reader calibration was not completed. | none | Decide whether to redesign checker qualification around harder, controlled generated-Hindi failure cases. Do not qualify or rank checkers from the EVAL-004 pilot. |
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

EVAL-003 readiness is merged. The prepared pack is **173 eligible Hindi-labelled unique photographs → 54 selected → 54 distinct photograph hashes** under `--overlap-policy admit-once --language-filter hindi --target-n 54`.

Two related CVIT releases are treated as one source lineage. Their annotation disagreement (725 identical / 357 different across 1,082 one-to-one matched regions) is evidence that source labels cannot be promoted directly to ground truth; it is not human-performance evidence and yields no evaluator threshold.

Canonical crop files were materialised and the original EVAL-004 protocol required **two independent blind Hindi-competent readers**, with exact agreement forming the strict reference.

**Controller override, 24 Aug 2026:** EVAL-004 was stopped after one complete 54-item Reader-A pilot. A second person informally looked at the material but did not perform the frozen independent blind pass, so there is no protocol-compliant Reader B and no two-reader reference. The pilot is exploratory only. See `eval/decisions/EVAL-004-STOP-2026-08-24.md`.

Consequently, Reader A is not ground truth; no checker may be qualified, disqualified, ranked, or entered into the Capability Registry from EVAL-004; and no accuracy / false-pass / Hindi-reading qualification claim may be made from this run.

The pilot's design lesson is that basic photographed-signage words may be too weak a proxy for the downstream failure state of interest: a multimodal checker silently normalizing or autocorrecting subtly malformed **generated** Hindi text. If Eval resumes, the next gate is a Controller decision on a harder controlled-failure qualification design, not automatic completion of the old two-reader signage run.

No checker roster, API/model spend, generator work, BSTD use, Marathi stress subset, Registry entry or methodology change is currently authorized.

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
                         └──► EVAL-004 single-reader pilot STOPPED
                                  │
                                  └──► next Eval gate: decide whether to redesign a harder checker-qualification battery

Capability Registry / routing remain blocked until empirical measurements exist and Registry architecture is separately approved.
```

## Current Controller posture

- Keep accepted Canon branches untouched until final integration.
- Finish and audit remaining fixed Canon books before any schema revision or Canon-consumption experiment.
- Treat EVAL-004 as a stopped exploratory pilot, not a completed calibration.
- Do not promote Reader A to ground truth or qualify checkers from the pilot.
- Treat source labels as provenance/evidence, not truth.
- Keep BSTD untouched until a deliberate cross-lineage validation task.
- Do not authorize checker/API/model runs, Registry, Production IR or routing work implicitly.
