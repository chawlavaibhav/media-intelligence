# CANON-003 16-Book Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reconcile the 16 Controller-accepted CANON-003 books into one integration branch, independently revalidate the integrated Canon artifacts, synthesize cross-book evidence, and recommend one consolidated post-batch method revision without changing the frozen method inside CANON-003.

**Architecture:** Start from current `main`; copy only accepted lane outputs from their frozen branches, excluding Books 11–12 and lane-local/shared files that were not approved for integration. Validate the integrated representation structurally and against the frozen SPEC-03/04/05 constraints that can be reproduced from committed data. Then write the 16-book synthesis, consolidate issues with source-lineage-aware counts, update the Controller/Handoff state, and prepare one reviewable PR.

**Tech Stack:** Git/GitHub repository artifacts, YAML/Markdown, Python for deterministic validation where needed.

**Spec:** `canon/tasks/CANON-003.md`; stop-at-16 decision: `canon/decisions/CANON-003-STOP-AT-16-2026-08-24.md`.

## Global Constraints

- Synthesis set is exactly the 16 Controller-accepted usable books; Books 11–12 are deferred reserve sources and excluded.
- Do not alter SPEC-01, SPEC-03, SPEC-04, SPEC-05, granularity, visual-pass method, ontology vocabulary, or extraction method inside CANON-003.
- Do not merge accepted worker branches wholesale; integrate only approved book artifacts and findings needed for synthesis.
- Preserve fresh-checkpoint provenance; do not rewrite historical evidence.
- Do not claim worker ephemeral validators were independently rerun. The integration validator must produce fresh, reproducible evidence from committed artifacts.
- Cross-source counts must treat same-author/companion-source lineage as non-independent where relevant.
- No Canon-consumption/RAG experiment, evaluator/model benchmark, Registry work, Production IR, or routing work in this integration.

---

### Task 1: Reconcile accepted branch outputs

**Files:**
- Add accepted book directories/findings from `work/canon-003-a`, `work/canon-003-b`, `work/canon-003-c`, `work/canon-003-d`, `work/canon-003-rebalance-d`.
- Exclude Book 11 and Book 12 artifacts.
- Preserve current `main` coordination/decision files.

- [ ] Verify each worker branch against common base and identify accepted book-only paths.
- [ ] Copy accepted files into `work/canon-003-integration-16` using original blobs where possible.
- [ ] Compare integration branch against `main` and verify no deferred-book or locked worker-shared files were imported.

### Task 2: Fresh integration validation

**Files:**
- Create: `canon/validation/validate_canon003_integrated.py`
- Create: `canon/findings/CANON-003-INTEGRATION-VALIDATION.md`

- [ ] Parse every integrated accepted-book YAML artifact.
- [ ] Verify required per-book files are present where the current method expects them.
- [ ] Verify IDs are unique within and across the 16-book set where global uniqueness is required by prefix convention.
- [ ] Verify source-layer records do not contain known product-layer vocabulary fields.
- [ ] Verify ontology `executable_by`, term kinds, relation types, and binding target namespaces stay within committed frozen vocabularies/spec constraints.
- [ ] Verify references used by systems, ontology mappings, and bindings resolve to committed IDs where the schema defines such references.
- [ ] Run the validator and record exact counts/failures. Fix only integration/serialization errors; do not revise the frozen method or source interpretation.

### Task 3: Consolidate the batch issue evidence

**Files:**
- Create: `canon/findings/CANON-003-integrated-issue-ledger.md`

- [ ] Read accepted lane-local issue files and pre-parallel batch issues.
- [ ] Consolidate by issue mechanism, not wording.
- [ ] Count distinct books and, separately where material, independent source lineages.
- [ ] Mark recurrence, counterevidence, source-specific cases, and product-schema-vs-Canon distinctions.
- [ ] Keep proposed fixes as proposals only.

### Task 4: Write the 16-book synthesis

**Files:**
- Create/replace: `canon/findings/CANON-003-multi-source-synthesis.md`

- [ ] Answer all 14 synthesis questions in `CANON-003.md` against the 16-book evidence set.
- [ ] Separate robust recurring findings from one-book/two-book signals.
- [ ] Explicitly evaluate granularity, SourceKnowledge/SourceConceptSystem/ontology/binding separation, visual-loss modes, source-shape effects, and unbound useful knowledge.
- [ ] Recommend one consolidated post-CANON-003 revision task and explicitly list what should remain unchanged.

### Task 5: Close CANON-003 integration state

**Files:**
- Update: `canon/tasks/CANON-003-CONTROLLER-BRIEF.md`
- Update: `canon/HANDOFF.md`
- Update: `coordination/WORKSTREAM-STATUS.md`

- [ ] Record 16-book completed synthesis set and Books 11–12 deferred status.
- [ ] Record fresh integration validation evidence and any residual limitations.
- [ ] Point the next gate to the consolidated Canon-method revision decision, not additional ingestion.
- [ ] Verify branch diff contains only integration artifacts, accepted book outputs, validation, synthesis, and status updates.

### Task 6: Final verification and review handoff

- [ ] Re-run integration validator from the final branch state and require zero structural validation failures or clearly documented non-fixable limitations.
- [ ] Re-read synthesis against all 14 required questions.
- [ ] Compare `main...work/canon-003-integration-16` for scope contamination.
- [ ] Prepare a PR only after verification evidence is fresh.