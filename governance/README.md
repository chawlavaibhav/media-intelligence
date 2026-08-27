# Governance

This directory contains the Repository Governor operating layer.

| File | Purpose |
|---|---|
| `GOVERNOR-CONTRACT.md` | The durable Governor operating contract — role, write boundaries, per-task review protocol, verdicts, audit cadence, routing rules. **Active.** |
| `audits/` | Dated repository-health audits. Permanent evidence of what was inspected, found, corrected and routed. |
| `reviews/` | Per-task integrity reviews. Each carries one verdict: `PASS`, `PASS WITH NON-BLOCKING NOTES` or `BLOCK`. |
| `status/` | Governor-owned status and supersession notes — records that a document or task is stale, without rewriting it. |
| `tasks/` | Controller-assigned Governor tasks. |
| `bootstrap/` | One-time migration input. **Historical — do not bootstrap from it.** |

The approved governance design is
`docs/superpowers/specs/2026-08-25-repository-governor-project-memory-design.md`.

**The canonical project entry point is the root `PROJECT-MEMORY.md`.** It is a map to the evidence,
not a source of truth: committed artifacts, deterministic validators and durable Controller decisions
establish project truth, and detailed domain artifacts remain authoritative for their own facts. The
Governor is downstream of all of them.

**A Governor verdict is a claim about repository coherence only.** `PASS` means no coherence defect
was found in that review's scope. It never certifies that domain work is scientifically or
technically correct — see `GOVERNOR-CONTRACT.md` §0.

## Current execution posture — read the Controller state, not this file

**This file no longer states the freeze.** The GOV-001 audit freeze has been re-scoped twice by the
Controller since it was written, so any freeze wording kept here would go stale again.

**`coordination/CONTROL-STATE.md` is authoritative for what is currently authorised**, and the
decision records under `coordination/decisions/` establish it.

**As of 28 Aug 2026 (GOV-005): paid empirical execution is authorised and has happened.** The user
approved a bounded EMP-001 tranche — USD 10 total consumed API spend, a USD 6 text-judge
qualification sub-cap, zero retries — and roughly USD 1.30 has been consumed. Five exact-text
checkers were measured and all five were disqualified, so there is **still no qualified evaluator
and the Capability Registry still holds zero rows**. Three lanes run in parallel: EVAL-028,
EVAL-024 and CANON-011.

**Any statement elsewhere that paid execution is unauthorised or has never occurred is stale.**

## Governor task history

| Task | What it did | Outcome |
|---|---|---|
| **GOV-001** | Established this layer: `PROJECT-MEMORY.md`, the Governor contract, the first repository audit and targeted control-plane corrections. | Complete — `audits/2026-08-25-initial-repository-hygiene-audit.md` |
| **GOV-002** | Assigned, **never executed**. Its premise — that EVAL-006 was open — was reversed when the Controller paused EVAL-006 on 26 Aug. | Superseded — `status/2026-08-26-GOV-002-SUPERSEDED.md` |
| **GOV-003** | Bounded integrity review of the three completed macro-research branches and the Controller's integration decision, plus a project-memory refresh. | `reviews/GOV-003-MACRO-RESEARCH-INTEGRATION-REVIEW.md` |
| **GOV-004** | Final pre-execution coherence review of the four freeze packages before merge, plus a project-memory refresh. | PASS WITH NON-BLOCKING NOTES — `reviews/GOV-004-FINAL-PRE-EXECUTION-REVIEW.md` |
| **GOV-005** | Post-EMP-001 coherence review and project-memory refresh, after the first paid tranche: qualification history, EVAL-022/023/025 integrations, active lanes, the marketplace-demand source, and every stale claim that paid execution had not been authorised. | PASS WITH NON-BLOCKING NOTES — `reviews/GOV-005-POST-EMP-001-COHERENCE-REVIEW.md`. One High finding routed and unresolved: the live tranche evidence is not committed to `main`. |

**No Governor task may be self-started.** Only the Controller opens tasks, Governor tasks included.
