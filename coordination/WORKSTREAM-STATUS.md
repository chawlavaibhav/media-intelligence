# Workstream Status

**Snapshot, updated at integration checkpoints. Detail lives in each stream's task brief / handoff.**  
**Updated:** 24 Aug 2026

| Stream | Status | Current approved work | Blocking item / next gate |
|---|---|---|---|
| Canon | **CANON-003 active, parallel extraction with one execution rebalance.** Five usable books complete at the pre-parallel checkpoint. Lane D is Controller-audited complete with Books 16–18 accepted, bringing the currently confirmed count to 8. A has Book 6 worker-complete; B has Book 9 worker-complete; C has Books 13–14 worker-complete. | `CANON-003.md` + `CANON-003-PARALLEL-EXECUTION.md` + `CANON-003-REBALANCE-01.md` | New ownership: A→Book 7; B→Books 10+12; C→Book 15; fresh rebalance branch→Books 8+11. Audit returned books before final integration. Accepted Lane D stays untouched. No schema changes or Canon-consumption experiments during the batch. |
| Eval | **EVAL-003 correction return audited; final bounded pass active.** Major validity corrections are accepted provisionally, but the branch is not merge-ready and no calibration is approved. | `EVAL-003.md` + `EVAL-003-CORRECTION-PASS.md` + `EVAL-003-FINALIZATION-PASS.md` | Sync `work/eval` with main; add adversarial one-to-one matcher regression; rebuild primary V0 as **54 Hindi-labelled unique photographs** if available; fix the two-reader altered-target rule; remove stale contradictory prose; complete the three-point Resources proposal; re-run bounded verification. No human/API work yet. |
| Resources | **RES-001/002 closed and merged. No active task.** | none | Stay closed unless a Controller-approved cross-stream correction or new sourcing requirement warrants a new task. |

## Canon live-review note

Lane D is accepted and its original branch remains frozen. To reduce idle time without changing the preselected 18-book experiment, Controller approved `CANON-003-REBALANCE-01.md`. At the audit point Books 8 and 11 were explicitly not started, so they were reassigned to a fresh branch `work/canon-003-rebalance-d` created from the original common parallel base. No book was added or dropped and no method/schema rule changed.

The remaining load is now balanced as follows: Lane A finishes Book 7; Lane B finishes Books 10 and 12; Lane C finishes Book 15; the rebalance worker handles Books 8 and 11. Book 12 deliberately remains with B because Lane D had already predicted that an interview-shaped source such as *The Conversations* might expose its claim-attribution issue; moving that source to the same worker after the prediction would weaken freshness.

The rebalance worker must not continue from Lane D's accepted branch and must not read A/B/C fresh findings or use D's issue file as an extraction checklist. It follows the same frozen per-book process and stops after Books 8 and 11.

## Eval live-review note

The correction return successfully withdrew the unsupported human-performance ceiling, made region matching one-to-one, separated the mechanical Unicode diagnostic from linguistic interpretation, corrected candidate arithmetic, moved to two-reader reference construction, materialised canonical hashed crops, and removed absolute paths.

It also revealed the decisive composition issue: the original overlap-exclusion policy leaves **0 Hindi** in the 54-item pack. Controller decision for primary V0 is now a **Hindi-focused 54-item pack of unique photographs**, admitting shared CVIT photographs once rather than counting dataset copies independently. Marathi stress coverage is deferred rather than mixed into the first qualification result.

Human/API calibration is still blocked until the finalization pass returns cleanly.

## Cross-stream dependency chain

```text
CANON-003 parallel/rebalanced book extractions
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

- Preserve the fixed 18-book source set; rebalance only explicitly not-started work under written Controller amendment.
- Keep accepted Lane D untouched until integration.
- Treat source annotations as provenance/evidence, not truth; reference construction remains two-reader and blind.
- Spend the first I1 calibration budget on the Hindi-facing capability actually needed, not a zero-Hindi proxy pack.
- Do not reopen Resources for ordinary cleanup; use the cross-stream proposal path.
- Do not allow worker-recommended next steps to become automatic tasks.
- Canon-consumption/planning experiments remain paused.