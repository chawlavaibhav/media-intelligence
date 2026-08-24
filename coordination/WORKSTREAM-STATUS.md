# Workstream Status

**Snapshot, updated at integration checkpoints. Detail lives in each stream's task brief / handoff.**  
**Updated:** 24 Aug 2026

| Stream | Status | Current approved work | Blocking item / next gate |
|---|---|---|---|
| Canon | **CANON-003 active, parallel extraction.** Five usable books complete at the pre-parallel checkpoint; four isolated lanes are created from one common base; no post-split lane return yet. | `CANON-003.md` + `CANON-003-PARALLEL-EXECUTION.md` | Review lane returns under frozen method; after all usable assignments, one fresh integration/synthesis session. No schema changes or Canon-consumption experiments during the batch. |
| Eval | **EVAL-001/002 closed and merged. EVAL-003 first return reviewed but not approved.** | `EVAL-003.md` + `EVAL-003-CORRECTION-PASS.md` | Bounded correction pass: repair disagreement methodology/claims, candidate accounting, language composition, two-reader protocol, canonical crop materialisation, portability, and Resources cross-stream note. No human/API calibration yet. |
| Resources | **RES-001/002 closed and merged. No active task.** | none | Stay closed unless a Controller-approved cross-stream correction or new sourcing requirement warrants a new task. |

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
