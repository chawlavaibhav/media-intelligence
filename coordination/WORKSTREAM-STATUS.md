# Workstream Status

**Snapshot, updated at integration checkpoints. Detail lives in each stream's task brief / handoff.**  
**Updated:** 24 Aug 2026

| Stream | Status | Current approved work | Blocking item / next gate |
|---|---|---|---|
| Canon | **CANON-003 active, parallel extraction.** Five usable books complete at the pre-parallel checkpoint. Lanes A/B/C remain at the common base. Lane D has one Book 16 extraction commit, currently **provisional under Controller audit** rather than counted as a completed usable book. | `CANON-003.md` + `CANON-003-PARALLEL-EXECUTION.md` | Lane D must preserve/reconcile the required fresh-before-historical checkpoint and add its lane issue/checkpoint record; subsequent lane returns remain under the frozen method. After all usable assignments, one fresh integration/synthesis session. No schema changes or Canon-consumption experiments during the batch. |
| Eval | **EVAL-001/002 closed and merged. EVAL-003 first return reviewed but not approved.** | `EVAL-003.md` + `EVAL-003-CORRECTION-PASS.md` | Bounded correction pass: repair disagreement methodology/claims, candidate accounting, language composition, two-reader protocol, canonical crop materialisation, portability, and Resources cross-stream note. No human/API calibration yet. |
| Resources | **RES-001/002 closed and merged. No active task.** | none | Stay closed unless a Controller-approved cross-stream correction or new sourcing requirement warrants a new task. |

## Canon live-review note

Lane D Book 16 (*Creativity, Inc.*, chapter 5) currently looks structurally strong: source provenance limitations are explicit, the visual pass records that the chapter has no evidentiary figure rather than inventing one, SourceConceptSystem synthesis is marked as extractor synthesis, no Creative IR binding is forced, and Production IR implications are parked.

However, GitHub currently shows only one post-base commit and no required Lane D issue/checkpoint files, while the provenance file says historical material was searched “after this checkpoint.” Until that history is reconciled, the book is a **provisional checkpoint**, not the sixth accepted usable book. Do not trigger a cleanup/re-extraction loop solely for this; if the sealed fresh checkpoint was amended or squashed, record that method deviation and enforce the frozen checkpoint rule on Books 17–18.

## Cross-stream dependency chain

```text
CANON-003 parallel book extractions
        │
        └──► fresh CANON-003 integration/synthesis
                 │
                 └──► evidence for a later consolidated Canon-method decision

RES-002 closed corpus ──► EVAL-003 corrected calibration readiness
                               │
                               └──► Controller review
                                      │
                                      ├──► later human checker calibration (not yet approved)
                                      └──► later API checker qualification (not yet approved)

Capability Registry / routing remain blocked until empirical measurements exist and the Registry architecture is separately approved.
```

## Current Controller posture

- Keep Canon lanes isolated until fresh extraction checkpoints are committed.
- Treat EVAL-003 source annotations as evidence, not truth; require controlled two-reader reference construction before calibration.
- Do not reopen Resources for ordinary cleanup.
- Do not allow worker-recommended next steps to become automatic tasks.
- Canon-consumption/planning experiments remain paused.
