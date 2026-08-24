# Workstream Status

**Snapshot, updated at integration checkpoints. Detail lives in each stream's task brief / handoff.**  
**Updated:** 24 Aug 2026

| Stream | Status | Current approved work | Blocking item / next gate |
|---|---|---|---|
| Canon | **CANON-003 active, parallel extraction.** Five usable books complete at the pre-parallel checkpoint. Lanes A/B/C remain at the common base. Lane D has one Book 16 extraction commit, currently **provisional under Controller audit** rather than counted as a completed usable book. | `CANON-003.md` + `CANON-003-PARALLEL-EXECUTION.md` | Lane D must preserve/reconcile the required fresh-before-historical checkpoint and add its lane issue/checkpoint record; subsequent lane returns remain under the frozen method. After all usable assignments, one fresh integration/synthesis session. No schema changes or Canon-consumption experiments during the batch. |
| Eval | **EVAL-003 correction return audited; final bounded pass active.** Major validity corrections are accepted provisionally, but the branch is not merge-ready and no calibration is approved. | `EVAL-003.md` + `EVAL-003-CORRECTION-PASS.md` + `EVAL-003-FINALIZATION-PASS.md` | Sync `work/eval` with main; add adversarial one-to-one matcher regression; rebuild primary V0 as **54 Hindi-labelled unique photographs** if available; fix the two-reader altered-target rule; remove stale contradictory prose; complete the three-point Resources proposal; re-run bounded verification. No human/API work yet. |
| Resources | **RES-001/002 closed and merged. No active task.** | none | Stay closed unless a Controller-approved cross-stream correction or new sourcing requirement warrants a new task. |

## Canon live-review note

Lane D Book 16 (*Creativity, Inc.*, chapter 5) currently looks structurally strong: source provenance limitations are explicit, the visual pass records that the chapter has no evidentiary figure rather than inventing one, SourceConceptSystem synthesis is marked as extractor synthesis, no Creative IR binding is forced, and Production IR implications are parked.

However, GitHub currently shows only one post-base commit and no required Lane D issue/checkpoint files, while the provenance file says historical material was searched “after this checkpoint.” Until that history is reconciled, the book is a **provisional checkpoint**, not the sixth accepted usable book. Do not trigger a cleanup/re-extraction loop solely for this; if the sealed fresh checkpoint was amended or squashed, record that method deviation and enforce the frozen checkpoint rule on subsequent books.

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

- Keep Canon lanes isolated until fresh extraction checkpoints are committed.
- Treat source annotations as provenance/evidence, not truth; reference construction remains two-reader and blind.
- Spend the first I1 calibration budget on the Hindi-facing capability actually needed, not a zero-Hindi proxy pack.
- Do not reopen Resources for ordinary cleanup; use the cross-stream proposal path.
- Do not allow worker-recommended next steps to become automatic tasks.
- Canon-consumption/planning experiments remain paused.
