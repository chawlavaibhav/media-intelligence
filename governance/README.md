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

**As of 28 Aug 2026, `main` at `91984f5`: paid empirical execution is authorised, has happened, and
the five parallel lanes that followed GOV-005 have all settled and merged.** CANON-011, EVAL-024,
EVAL-029, EVAL-026, EVAL-030 and RES-005 are accepted and merged; **no domain lane is currently
open**.

**What the paid work produced.** Cloud Vision `TEXT_DETECTION` is **`benchmark_qualified`** for
Devanagari and Latin and remains **`strict_exactness_qualified: false`**. Sixteen A-TEXT images were
generated, sealed as committed bytes and scored — **7/16 exact** (GPT Image 2 6/8, Ideogram v3 1/8).
**The Capability Registry still holds zero rows**, deliberately: `benchmark_qualified` is weaker than
the Registry's admission bar, and admission was not weakened to create a first row.

**Exact text is not a programme-wide gate.** Certifying text as exact and benchmarking which model
handles text better are separate jobs with separate standards. **EVAL-028 and its two-human
architecture are cancelled and must not run**; **no mandatory human-in-the-loop step exists in the
production API architecture.**

**Any statement elsewhere that paid execution is unauthorised, that no image has been generated, that
exact text blocks the programme, or that EVAL-028 is the next direction, is stale.**

## Governor task history

| Task | What it did | Outcome |
|---|---|---|
| **GOV-001** | Established this layer: `PROJECT-MEMORY.md`, the Governor contract, the first repository audit and targeted control-plane corrections. | Complete — `audits/2026-08-25-initial-repository-hygiene-audit.md` |
| **GOV-002** | Assigned, **never executed**. Its premise — that EVAL-006 was open — was reversed when the Controller paused EVAL-006 on 26 Aug. | Superseded — `status/2026-08-26-GOV-002-SUPERSEDED.md` |
| **GOV-003** | Bounded integrity review of the three completed macro-research branches and the Controller's integration decision, plus a project-memory refresh. | `reviews/GOV-003-MACRO-RESEARCH-INTEGRATION-REVIEW.md` |
| **GOV-004** | Final pre-execution coherence review of the four freeze packages before merge, plus a project-memory refresh. | PASS WITH NON-BLOCKING NOTES — `reviews/GOV-004-FINAL-PRE-EXECUTION-REVIEW.md` |
| **GOV-005** | Post-EMP-001 coherence review and project-memory refresh, after the first paid tranche: qualification history, EVAL-022/023/025 integrations, active lanes, the marketplace-demand source, and every stale claim that paid execution had not been authorised. Audited `0e24d6a`, then resynced to `8990a7a` after the Controller's disposition. | PASS WITH NON-BLOCKING NOTES — `reviews/GOV-005-POST-EMP-001-COHERENCE-REVIEW.md`. Disposition: `coordination/decisions/CONTROLLER-GOV-005-REVIEW-AND-CORRECTIONS-2026-08-28.md`. F-4, F-5, F-9 and F-10 closed. **Closed and merged** (PR #48, `c794694`) — **do not reopen it for parallel-lane drift.** **Its §10 no longer governs current state; GOV-006 supersedes it**, and its High finding **F-1 is now resolved** for the text-OCR, A-TEXT generation and A-TEXT scoring lanes. F-2 remains open and was re-routed and escalated by GOV-006 as G6-05; F-6, F-7 and F-8 remain with Eval. |

| **GOV-006** | Post-parallel reconciliation after the five settled lanes: verified the sealed A-TEXT artifacts and their fingerprint, that EVAL-030 scored those exact bytes without regenerating, the 6/8 · 1/8 · 7/16 arithmetic, both EVAL-029 benchmark screens recomputed from committed evidence, EVAL-026's 13 perturbation types over 9 capabilities, RES-005's 12 clips and coverage counts, and that the Registry is still empty. Reconciled the current-state documents to the settled tree. Audited `91984f5`. | PASS WITH NON-BLOCKING NOTES — `reviews/GOV-006-POST-PARALLEL-RECONCILIATION.md`. **GOV-005's High finding F-1 is resolved** for the text-OCR lane. Seven findings (G6-01…G6-07) routed to Eval, Canon and Resources; none blocking. |

**No Governor task may be self-started.** Only the Controller opens tasks, Governor tasks included.
