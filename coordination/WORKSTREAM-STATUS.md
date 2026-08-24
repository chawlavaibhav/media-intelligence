# Workstream Status

**Snapshot, updated at integration checkpoints. Detail lives in each stream's task brief / handoff.**  
**Updated:** 24 Aug 2026

| Stream | Status | Current approved work | Blocking item / next gate |
|---|---|---|---|
| Canon | **CANON-003 active, parallel extraction.** Five usable books complete at the pre-parallel checkpoint. Lane D is now **Controller-audited complete with Books 16–18 accepted as usable**, bringing the currently confirmed count to 8. Lanes A/B/C remain separately reviewable as they return. | `CANON-003.md` + `CANON-003-PARALLEL-EXECUTION.md` | Keep Lane D isolated and unmerged. Audit remaining lane returns against the frozen method. After all usable assignments, one fresh integration/synthesis session merges/reconciles lanes, revalidates all per-book outputs, counts recurrence and synthesizes. No schema changes or Canon-consumption experiments during the batch. |
| Eval | **EVAL-003 correction return audited; final bounded pass active.** Major validity corrections are accepted provisionally, but the branch is not merge-ready and no calibration is approved. | `EVAL-003.md` + `EVAL-003-CORRECTION-PASS.md` + `EVAL-003-FINALIZATION-PASS.md` | Sync `work/eval` with main; add adversarial one-to-one matcher regression; rebuild primary V0 as **54 Hindi-labelled unique photographs** if available; fix the two-reader altered-target rule; remove stale contradictory prose; complete the three-point Resources proposal; re-run bounded verification. No human/API work yet. |
| Resources | **RES-001/002 closed and merged. No active task.** | none | Stay closed unless a Controller-approved cross-stream correction or new sourcing requirement warrants a new task. |

## Canon live-review note

Lane D is accepted. Git history now supplies the missing checkpoint evidence rather than relying on the worker's retrospective claim. The common base → Book 16 checkpoint `b7f0d47` is exactly one commit and contains only Book 16 source-representation files. Book 16 findings/history are committed before the Book 17 fresh checkpoint `75e4da1`; Book 17 findings/history are committed before the Book 18 fresh checkpoint `f0127e4`; Book 18 findings/history land only after that checkpoint. This satisfies the frozen fresh-before-historical rule for all three books, so the earlier provisional status is lifted with **no method deviation**.

Compare-to-base also shows the lane stayed in bounds: only source-specific Book 16–18 directories plus Lane D findings/checkpoint/issues files changed. Locked shared synthesis/Controller files were untouched. The return preserves important distinctions rather than smoothing them away: process knowledge is not forced into Creative IR, source-system synthesis is marked as extractor synthesis, visual evidence is inspected explicitly, evidence weaknesses remain visible, and schema implications are proposed but not applied.

Lane D should now **stop and remain untouched** until the fresh final Canon integration session. It should not merge itself to main or synthesize across lanes.

## Eval live-review note

The correction return successfully withdrew the unsupported human-performance ceiling, made region matching one-to-one, separated the mechanical Unicode diagnostic from linguistic interpretation, corrected candidate arithmetic, moved to two-reader reference construction, materialised canonical hashed crops, and removed absolute paths.

It also revealed the decisive composition issue: the original overlap-exclusion policy leaves **0 Hindi** in the 54-item pack. Controller decision for primary V0 is now a **Hindi-focused 54-item pack of unique photographs**, admitting shared CVIT photographs once rather than counting dataset copies independently. Marathi stress coverage is deferred rather than mixed into the first qualification result.

Human/API calibration is still blocked until the finalization pass returns cleanly.

## Cross-stream dependency chain

```text
CANON-003 parallel book extractions
        │
        └──► fresh CANON-003 integration/synthesis
                 │
                 └──► evidence for a later consolidated Canon-method decision

RES-002 closed corpus ──► EVAL-003 finalised Hindi-primary calibration readiness
                               │
                               └──► Controller review
                                      │
                                      ├──► later two-reader human calibration (not yet approved)
                                      └──► later API checker qualification (not yet approved)

Capability Registry / routing remain blocked until empirical measurements exist and the Registry architecture is separately approved.
```

## Current Controller posture

- Keep Canon lanes isolated until fresh extraction checkpoints are committed; accepted lanes remain untouched until integration.
- Treat source annotations as provenance/evidence, not truth; reference construction remains two-reader and blind.
- Spend the first I1 calibration budget on the Hindi-facing capability actually needed, not a zero-Hindi proxy pack.
- Do not reopen Resources for ordinary cleanup; use the cross-stream proposal path.
- Do not allow worker-recommended next steps to become automatic tasks.
- Canon-consumption/planning experiments remain paused.
