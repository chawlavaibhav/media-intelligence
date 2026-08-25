# Governor Reset Cleanup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reconstruct authoritative project state from GitHub, establish the Repository Governor control layer, and eliminate or clearly mark all operational-state contradictions accumulated through 2026-08-25 without changing domain methodology or evidence.

**Architecture:** Preserve Canon/Eval/Resources as the evidence/data plane. Add a governance layer consisting of a curated root `PROJECT-MEMORY.md`, `governance/GOVERNOR-CONTRACT.md`, a dated audit report, and targeted status/supersession corrections to stale coordination documents. Domain-owned artifacts are read-only evidence during this task; any domain defect is routed rather than silently repaired.

**Tech Stack:** Markdown, Git/GitHub, existing repository validators/tests/grep/search tools.

**Spec:** `docs/superpowers/specs/2026-08-25-repository-governor-project-memory-design.md`

## Global Constraints

- GitHub is project memory; chat is execution context only.
- Audit against the current merged `main` before making cleanup edits.
- This first audit is exhaustive across operational/state documents, not a routine spot check.
- Preserve historical baselines and domain artifacts.
- Do not change Canon/Eval/Resources methodology, schemas, source knowledge, benchmark contents, thresholds, datasets, or product architecture.
- Prefer targeted corrections/status markers over large file moves, deletions, or cosmetic restructuring.
- Any claim that cannot be proven from committed GitHub evidence must be qualified as unresolved, external research snapshot, human-reviewed, Controller-inspected, or agent-reported as appropriate.
- No new Canon/Eval/Resources task may be authorized by this cleanup.

---

### Task 1: Build the authoritative-state inventory

**Files:**
- Read: `coordination/**`
- Read: `canon/**` operational/task/audit state
- Read: `eval/**` operational/task/battery state
- Read: `resources/**` operational/task/manifests
- Read: repository root and current branches/PR metadata
- Produce working notes only until evidence is reconciled

**Interfaces:**
- Consumes: current merged `main`, approved governance design.
- Produces: evidence-backed current-state facts and a classification of every operational/state document.

- [ ] **Step 1: Record the exact `main` commit being audited.**

Use Git/GitHub to record the current `main` SHA in the audit working notes. All later state claims must be traceable to this baseline plus commits made by GOV-001 itself.

- [ ] **Step 2: Enumerate operational/state documents exhaustively.**

At minimum inspect every file whose purpose is project state, handoff, task status, decision history, runbook, roadmap, charter, contract, resource request, audit summary, or current-state coordination. Do not infer completeness from filenames alone; search for phrases such as `current`, `active`, `next`, `status`, `accepted`, `complete`, `pending`, `deferred`, `stopped`, and `merged`.

- [ ] **Step 3: Classify each operational/state document.**

Use exactly one primary classification:

```text
CURRENT_AUTHORITY
SUPPORTING_CURRENT
HISTORICAL
SUPERSEDED
REQUIRES_CORRECTION
```

Record the evidence for each classification.

- [ ] **Step 4: Reconstruct current stream state from underlying evidence.**

For Canon, Eval, Resources, coordination, and external-acquisition references present in GitHub, reconcile current counts/statuses against committed artifacts, task outcomes, accepted decision records, and merged PR history. Treat historical baselines as separate facts rather than replacing them with live counts.

- [ ] **Step 5: Identify contradictions and missing durable decisions.**

For each issue record: affected files, conflicting claims, which evidence is stronger, whether the issue can be fixed within governance write boundaries, and owner if it must be routed.

### Task 2: Establish the Governor control layer

**Files:**
- Create: `PROJECT-MEMORY.md`
- Create: `governance/GOVERNOR-CONTRACT.md`

**Interfaces:**
- Consumes: Task 1 authoritative-state inventory and approved design.
- Produces: the canonical project bootstrap and durable Governor operating contract.

- [ ] **Step 1: Write `governance/GOVERNOR-CONTRACT.md`.**

Encode the fifth-agent role, authority boundaries, review cadence, verdict vocabulary, write boundaries, evidence/provenance discipline, and prohibition against using integrity review to redesign methodology.

- [ ] **Step 2: Write the first `PROJECT-MEMORY.md`.**

It must be concise enough for a fresh zero-context agent while covering: project thesis/success metric, architecture and separations, frozen decisions, exact current state by stream, important established lessons/results, limitations/unresolved issues, current freeze/next gates, concise milestones, authority map, and material verification qualifiers.

- [ ] **Step 3: Link every material current-state claim to deeper repository evidence by path.**

Do not duplicate large tables, raw task histories, or manually maintained hashes/counts where the detailed artifact itself is the authority.

- [ ] **Step 4: Run a zero-chat bootstrap self-test.**

Pretend no conversation exists. From only `PROJECT-MEMORY.md` and its linked files, answer internally: what is the product, what has been built, what is live versus historical, what is frozen, what is unresolved, and what may happen next. Revise the memory if any answer depends on remembered chat.

### Task 3: Repair the operational documentation layer

**Files:**
- Modify only operational/control documents proven stale or ambiguous by Task 1.
- Do not modify domain evidence/artifacts outside the governance write boundary.

**Interfaces:**
- Consumes: contradiction inventory and `PROJECT-MEMORY.md`.
- Produces: operational docs that cannot reasonably be mistaken for a different current state.

- [ ] **Step 1: Add explicit status/supersession markers to historical documents that still read as live.**

A marker must state whether the file is historical/superseded, where current state now lives, and whether the underlying historical content remains evidentially valid.

- [ ] **Step 2: Correct central coordination files that are intended to remain current.**

Update only factual/current-state portions necessary to align them with repository evidence. Avoid rewriting historical findings into current prose or deleting useful forensic history.

- [ ] **Step 3: Route domain-owned inconsistencies instead of silently fixing them.**

If an Eval/Canon/Resources artifact itself is wrong and the correction would change domain-owned content, list it as a routed issue in the audit report with exact path/evidence/owner.

- [ ] **Step 4: Search for stale operational claims after edits.**

Search the repo for old live-state numbers/status phrases discovered in Task 1. Distinguish legitimate historical references from misleading current-state references; do not mechanically replace historical numbers.

### Task 4: Produce the first governance audit and verify the reset

**Files:**
- Create: `governance/audits/2026-08-25-initial-repository-hygiene-audit.md`
- Update: `PROJECT-MEMORY.md` only if verification exposes a gap

**Interfaces:**
- Consumes: Tasks 1-3.
- Produces: permanent evidence of what GOV-001 inspected, found, changed, and routed.

- [ ] **Step 1: Write the dated audit report.**

For every material inconsistency include: evidence, severity, resolution (`corrected`, `marked historical/superseded`, `routed`, or `unresolved`), and affected paths. Include the exhaustive operational-document classification inventory.

- [ ] **Step 2: Run existing validators/tests relevant to files touched and repository integrity.**

Run the existing Canon/Eval/Resources validators/tests without modifying their inputs merely to make them pass. Record exact commands and results. If environment limitations prevent a test, record that explicitly rather than reporting it as passed.

- [ ] **Step 3: Run repository-level hygiene searches.**

Verify there are no unqualified current-state contradictions for the material facts established by the audit, no broken links introduced by GOV-001, and no files outside the approved write boundary changed unintentionally.

- [ ] **Step 4: Inspect the final diff against the audit baseline.**

Confirm all changes are governance/control-plane changes, historical baselines remain intact, and no Canon/Eval/Resources methodology or evidence was silently modified.

- [ ] **Step 5: Open one PR to `main` and stop.**

PR description must contain: audited baseline SHA, files changed, high-severity inconsistencies corrected, issues routed but not fixed, verification commands/results, and a final Governor verdict. Do not merge. Do not authorize GOV-002 or any domain work.
