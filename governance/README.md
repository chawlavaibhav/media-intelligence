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
decision records under `coordination/decisions/` establish it. As of 26 Aug 2026: research tasks
have been assigned and are running, and **paid empirical execution remains blocked** — no qualified
evaluator, no empirical Registry entry, no approved paid benchmark budget.

## Governor task history

| Task | What it did | Outcome |
|---|---|---|
| **GOV-001** | Established this layer: `PROJECT-MEMORY.md`, the Governor contract, the first repository audit and targeted control-plane corrections. | Complete — `audits/2026-08-25-initial-repository-hygiene-audit.md` |
| **GOV-002** | Assigned, **never executed**. Its premise — that EVAL-006 was open — was reversed when the Controller paused EVAL-006 on 26 Aug. | Superseded — `status/2026-08-26-GOV-002-SUPERSEDED.md` |
| **GOV-003** | Bounded integrity review of the three completed macro-research branches and the Controller's integration decision, plus a project-memory refresh. | `reviews/GOV-003-MACRO-RESEARCH-INTEGRATION-REVIEW.md` |

**No Governor task may be self-started.** Only the Controller opens tasks, Governor tasks included.
