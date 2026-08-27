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

**As of 28 Aug 2026, `main` at `8990a7a`: paid empirical execution is authorised and has happened.**
The user approved a bounded EMP-001 tranche — USD 10 total consumed API spend, a USD 6 text-judge
qualification sub-cap, zero retries — and roughly USD 1.30 has been consumed. Five exact-text
checkers were measured and all five failed the strict zero-false-pass standard, so there is **still
no qualified evaluator and the Capability Registry still holds zero rows**.

**Exact text is no longer a programme-wide gate.** Certifying text as exact and benchmarking which
model handles text better are now separate jobs with separate standards. **EVAL-028 and its
two-human architecture are cancelled and must not run**; **no mandatory human-in-the-loop step
exists in the production API architecture.** Three lanes run in parallel: **EVAL-029** (benchmark-grade
text OCR), **EVAL-024** (A-TEXT generation-only, returned at USD 0 and behind a cleanup gate) and
**CANON-011**.

**Any statement elsewhere that paid execution is unauthorised, that exact text blocks the programme,
or that EVAL-028 is the next direction, is stale.**

## Governor task history

| Task | What it did | Outcome |
|---|---|---|
| **GOV-001** | Established this layer: `PROJECT-MEMORY.md`, the Governor contract, the first repository audit and targeted control-plane corrections. | Complete — `audits/2026-08-25-initial-repository-hygiene-audit.md` |
| **GOV-002** | Assigned, **never executed**. Its premise — that EVAL-006 was open — was reversed when the Controller paused EVAL-006 on 26 Aug. | Superseded — `status/2026-08-26-GOV-002-SUPERSEDED.md` |
| **GOV-003** | Bounded integrity review of the three completed macro-research branches and the Controller's integration decision, plus a project-memory refresh. | `reviews/GOV-003-MACRO-RESEARCH-INTEGRATION-REVIEW.md` |
| **GOV-004** | Final pre-execution coherence review of the four freeze packages before merge, plus a project-memory refresh. | PASS WITH NON-BLOCKING NOTES — `reviews/GOV-004-FINAL-PRE-EXECUTION-REVIEW.md` |
| **GOV-005** | Post-EMP-001 coherence review and project-memory refresh, after the first paid tranche: qualification history, EVAL-022/023/025 integrations, active lanes, the marketplace-demand source, and every stale claim that paid execution had not been authorised. Audited `0e24d6a`, then resynced to `8990a7a` after the Controller's disposition. | PASS WITH NON-BLOCKING NOTES — `reviews/GOV-005-POST-EMP-001-COHERENCE-REVIEW.md` (§§1–9 audit `0e24d6a`; **§10 is the current-state update and governs**). Disposition: `coordination/decisions/CONTROLLER-GOV-005-REVIEW-AND-CORRECTIONS-2026-08-28.md`. F-4, F-5, F-9 and F-10 closed; **F-1 remains High and unresolved** — completed live evidence is not yet sealed into GitHub; F-2, F-6, F-7 and F-8 routed to Eval. |

**No Governor task may be self-started.** Only the Controller opens tasks, Governor tasks included.
