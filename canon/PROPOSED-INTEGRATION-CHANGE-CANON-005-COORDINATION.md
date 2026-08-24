# Proposed coordination update — CANON-005

**From:** Canon worker, CANON-005 · **To:** Controller · **Date:** 25 Aug 2026
**Severity:** `LOCAL` (stale status records, no cross-stream logic affected)
**Status:** proposal only — nothing under `coordination/` was edited.

`coordination/` is Controller-owned and the runbook forbids a stream editing it directly, so this
records what is now out of date rather than fixing it.

## What is stale

Both files still describe CANON-003 as an in-flight extraction batch. It closed at 16 accepted books
on 24 Aug, was integrated and merged, and has since been followed by CANON-004 (Audit Gate designed,
tested, adopted) and CANON-005 (Audit Gate made authoritative).

### `coordination/CONTROL-STATE.md`

| Line | Says | Now |
|---|---|---|
| 16 | heading `## Canon status — CANON-003 active` | CANON-003 closed and merged (PR #4) |
| 18 | "CANON-003 remains a frozen-method 18-usable-book stress batch" | closed at 16 by Controller decision `canon/decisions/CANON-003-STOP-AT-16-2026-08-24.md` |
| 30, 32 | lane/branch assignments for Books 8–12 | lanes merged; Books 11–12 remain deferred reserves outside the method-test set |
| 36 | "No schema … change is permitted during the batch" | superseded: SPEC-05 Governance rule 5 was amended under the adopted CANON-004 decision |
| 73 | next step "finish and audit B plus the rebalance worker, then run one fresh CANON-003 integration/synthesis session" | done; CANON-004 and CANON-005 have since completed |

### `coordination/WORKSTREAM-STATUS.md`

| Line | Says | Now |
|---|---|---|
| 8 | Canon next step is "Run one fresh integration session over the accepted 16-book evidence set" | completed; the Audit Gate is now the active method |
| 38 | "No schema … change is allowed until the batch-level synthesis is complete" | synthesis complete; the one authorised change is applied |
| 59–65 | the flow diagram ending at "possible consolidated Canon-method revision task" | that revision happened: CANON-004 designed it, the Controller adopted it, CANON-005 applied it |

## Proposed replacement facts

If the Controller updates these files, the current Canon position is:

- **CANON-003:** closed at 16 Controller-accepted books, integrated, merged via PR #4.
- **CANON-004:** Post-Extraction Audit Gate v0.2 designed and tested against those 16 books;
  Controller-adopted 25 Aug (`canon/decisions/CANON-004-ADOPT-AUDIT-GATE-2026-08-25.md`, PR #6).
- **CANON-005:** the adopted gate is authoritative. SPEC-05 Governance rule 5 amended; the schema and
  the 16 records promoted to `canon/audit/`; the gate order documented; validator and tests
  repointed. SPEC-01/02/03/04 unchanged.
- **The gate now blocks downstream consumption:** an unaudited or stale source stays in the
  repository as source evidence but may not pass cross-source promotion, downstream product use, or
  Canon-consumption/retrieval.
- **Deferred reserves:** *Master Shots* and *The Conversations* remain outside the frozen 16-book
  method-test set. Integrating either is a separate Controller-assigned task and would require its
  own fresh Audit Gate record.
- **Still unapproved / not implemented:** Capability Registry, Production IR, routing, and
  Canon-consumption/training experiments. CANON-005 changed nothing here.

`canon/HANDOFF.md` has been updated with the same facts and is authoritative for the Canon stream in
the meantime.
