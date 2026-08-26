# Pre-E7 Scope Rebase Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refreeze the pre-paid-run Eval architecture so customer outcomes, production conditions and multi-step workflows are represented before current-model benchmarking begins.

**Architecture:** Preserve the accepted V1 capability/evidence machinery, add a model-agnostic Production Requirement Profile and frozen condition taxonomy, extend Resources persistence to whole customer outcomes with graph lineage, then audit/refreeze the capability contract and benchmark. Work is isolated by stream and reconciled by Controller before E7 is re-authorised.

**Tech Stack:** Markdown/YAML/JSONL, Python validators, existing Eval harness and Resources validators, GitHub isolated branches.

**Spec:** `docs/superpowers/specs/2026-08-26-pre-e7-scope-rebase-design.md`

## Global Constraints

- E7 and E8 remain blocked until Controller integration.
- No paid generation/checker/evaluator calls.
- No empirical current-model Registry entries.
- Do not enumerate the full cartesian product of condition variables.
- Preserve one provider/API/transform call = one trial.
- Preserve repeat vs retry separation.
- Preserve Creative IR != Production IR.
- Production Requirement Profile is model/provider agnostic.
- Resources owns persistence; Eval owns measurement semantics; Canon owns customer/creative requirement interpretation.
- Existing 30 Canon briefs remain unchanged.
- Existing 100-item Eval bank is the baseline; rebuild only with concrete justification.
- Existing V2.1 empirical archives remain valid historical evidence and are not silently rewritten.

---

### Task 1: Canon customer-to-requirement audit

**Files:**
- Read: `canon/experiments/v1/brief-bank/briefs-source.yaml`
- Read: `canon/knowledge/SPEC-01-creative-ir.md`
- Read: `eval/v1/capability-contract.yaml`
- Create: `canon/experiments/pre-e7-scope-audit/requirement-ledger.jsonl`
- Create: `canon/experiments/pre-e7-scope-audit/AUDIT-REPORT.md`
- Create: `canon/experiments/pre-e7-scope-audit/validate_requirement_ledger.py`

**Interfaces:**
- Consumes: 30 authoritative customer briefs and existing Creative IR/capability vocabulary.
- Produces: one grounded requirement ledger consumed by Eval during capability-v2 refreeze.

- [ ] **Step 1: Write validator tests/negative fixtures first**

Create fixtures covering: missing brief id, missing evidence, duplicate classification, unsupported `genuine_gap`, Planner decision falsely marked customer-specified, and model/provider name appearing as requirement resolution.

- [ ] **Step 2: Run validator against failing/incomplete ledger**

Run: `python3 canon/experiments/pre-e7-scope-audit/validate_requirement_ledger.py`

Expected before ledger completion: non-zero exit with explicit missing-brief / missing-row errors.

- [ ] **Step 3: Build the requirement ledger from all 30 briefs**

Classify each meaningful requirement exactly once as:

`existing_capability | condition | planner_decision | acceptance_constraint | operational_variable | genuine_gap`

Include evidence, source operation, strength and scope as specified in `canon/tasks/CANON-PRE-E7-SCOPE-AUDIT.md`.

- [ ] **Step 4: Run validator to green**

Expected: all 30 brief ids represented, zero unsupported gaps, zero ungrounded rows.

- [ ] **Step 5: Write the Canon audit report**

Report total requirements, bucket counts, repeated condition concepts, commonly omitted production decisions and exact genuine gaps.

- [ ] **Step 6: Commit on isolated branch**

Suggested branch: `work/canon-pre-e7-scope-audit`.

Commit message: `canon: audit customer requirements before E7`

---

### Task 2: Eval Production Requirement Profile and Condition Contract

**Files:**
- Create: `eval/pre-e7/PRODUCTION-REQUIREMENT-PROFILE.md`
- Create: `eval/pre-e7/production-requirement-profile.schema.yaml`
- Create: `eval/pre-e7/CONDITION-ENVELOPE-CONTRACT.yaml`
- Create: `eval/pre-e7/validate_pre_e7_contracts.py`
- Modify/version: `eval/registry/SCHEMA-v1-draft.yaml` or create its explicit successor

**Interfaces:**
- Consumes: Pre-E7 spec and, when available, Canon requirement ledger.
- Produces: model-agnostic requirement query interface and frozen Registry condition vocabulary.

- [ ] **Step 1: Write failing validator fixtures**

Cover: provider/model embedded in Production Requirement Profile, unknown condition key, applicable condition silently missing, synthetic aggregate complexity score used in place of atomic conditions, invalid decision provenance.

- [ ] **Step 2: Run failing validation**

Run the new validator and record the expected failures before adding final schemas.

- [ ] **Step 3: Define Production Requirement Profile schema**

Required fields: requirement id/type, source operation/provenance, strength, value, scope, status, acceptance consequence.

Explicitly prohibit provider/model/routing score fields.

- [ ] **Step 4: Define Condition / Envelope Contract**

Freeze the 12 condition families from the approved design. For each field define: machine id, type/allowed values or numeric unit, applicability rule, allowed null state, and whether changing it requires a distinct Registry evidence row.

- [ ] **Step 5: Version Registry semantics**

Replace unconstrained free-form conditions for new evidence with the frozen contract reference and validated fields. Preserve historical rows through explicit legacy-state handling.

- [ ] **Step 6: Run validators green**

Expected: schema fixtures pass; every forbidden/unknown condition negative control fails closed.

- [ ] **Step 7: Commit on isolated branch**

Suggested branch: `work/eval-pre-e7-scope-rebase`.

Commit message: `eval: freeze production requirements and evidence conditions`

---

### Task 3: Resources Outcome / Production Topology Contract

**Files:**
- Read/modify or version: `resources/v1/EMPIRICAL-ARTIFACT-MANIFEST-SCHEMA.yaml`
- Create: `resources/pre-e7/OUTCOME-PRODUCTION-TOPOLOGY-CONTRACT.yaml`
- Create: `resources/pre-e7/validate_outcome_archive.py`
- Create: `resources/pre-e7/fixtures/` for positive/negative topology archives
- Create: `resources/pre-e7/PRE-E7-RESOURCES-CONTROLLER-BRIEF.md`

**Interfaces:**
- Consumes: existing V2.1 storage contract and approved topology semantics.
- Produces: backward-compatible job/outcome/sequence/unit/step lineage and whole-outcome CpAO recomputation.

- [ ] **Step 1: Write failing topology fixtures**

Include: unknown parent, graph cycle, duplicate ledger reference in outcome cost, child with invented trial, historical trial acceptance promoted to outcome acceptance, multi-parent composition missing config provenance.

- [ ] **Step 2: Run validator RED**

Expected: each negative fixture fails for the intended reason.

- [ ] **Step 3: Add hierarchy identities**

Represent `job -> outcome -> sequence_or_asset_set -> production_unit -> production_step -> attempt -> artifact` without changing one-call-one-trial semantics.

- [ ] **Step 4: Add graph lineage**

Represent ordered multi-parent composition/assembly edges and recoverable transform/config provenance.

- [ ] **Step 5: Add outcome acceptance and cost recomputation**

Ensure whole-outcome cost traverses contributing production history without counting one ledger entry twice.

- [ ] **Step 6: Add V2.1 compatibility mapping**

Existing archives remain valid with explicit `not_recorded_pre_rebase` state. Do not infer customer-outcome acceptance from historical trial acceptance.

- [ ] **Step 7: Run all Resources validators green**

Run both new topology tests and existing `bash resources/v1/validators/run_all.sh`.

- [ ] **Step 8: Commit on isolated branch**

Suggested branch: `work/resources-pre-e7-scope-rebase`.

Commit message: `resources: add outcome-level production lineage`

---

### Task 4: Eval capability-v2 refreeze and benchmark rebase

**Files:**
- Read: Canon requirement ledger from Task 1
- Read: `eval/v1/capability-contract.yaml`
- Read: `eval/v1/bank/master-bank-v1.jsonl`
- Create: `eval/pre-e7/CAPABILITY-AUDIT.md`
- Create/version: `eval/pre-e7/CAPABILITY-CONTRACT-v2.yaml`
- Modify/version benchmark builder/manifests only where justified
- Create: `eval/pre-e7/BENCHMARK-REBASE.md`

**Interfaces:**
- Consumes: Canon audit and Condition Contract.
- Produces: capability vocabulary refrozen against real briefs plus a sparse layered benchmark.

- [ ] **Step 1: Map every Canon `genuine_gap` candidate**

For each, document one of four resolutions: existing capability; capability+condition; non-capability requirement; new capability required.

- [ ] **Step 2: Add only proven missing capabilities**

No target count. Preserve existing ids unless definition change is unavoidable and explicitly versioned.

- [ ] **Step 3: Validate capability-v2 contract**

Every capability requires definition, exclusions, observation unit, result form, readiness axes, Registry conditions and routing use.

- [ ] **Step 4: Re-evaluate the 100-item bank**

Keep it intact where possible. Prefer metadata/condition enrichment or small reallocations. Any added/removed item requires a coverage and cost justification.

- [ ] **Step 5: Add sparse envelope sweeps**

Design controlled sweeps for only the highest-value variables surfaced by the 30-brief audit, seeking failure boundaries rather than cartesian completeness.

- [ ] **Step 6: Add workflow-topology comparison tranche**

Define a small set of equivalent-outcome comparisons such as native extension vs reference-conditioned multi-shot assembly. Do not implement Production Planner logic.

- [ ] **Step 7: Commit**

Commit message: `eval: refreeze capabilities and benchmark after scope audit`

---

### Task 5: E2 production-operation inventory and fresh cost forecast

**Files:**
- Modify/version: `eval/v1/model-workflow-inventory-2026-08-26.yaml`
- Modify/version: `eval/v1/MODEL-WORKFLOW-INVENTORY-2026-08-26.md`
- Modify: official price file produced from current sources
- Modify/version: benchmark cost forecast outputs

**Interfaces:**
- Consumes: capability-v2/condition/topology design.
- Produces: current official workflow candidates and a new paid-run forecast.

- [ ] **Step 1: Browse official current provider docs only for identity/access/pricing claims**

Record current exact model/API ids, availability, official billing units/prices and production-operation features required by the design.

- [ ] **Step 2: Record production-operation envelope per workflow**

Capture duration, t2v/i2v/edit/extension, frame/reference controls, native audio, aspect/resolution, camera controls, seed/version pinning and production-relevant access constraints where officially exposed.

- [ ] **Step 3: Recalculate generation/evaluator/human forecast**

The historical 204/520 counts remain labelled pre-rebase. New totals must come from the revised benchmark.

- [ ] **Step 4: Fail closed on unresolved prices**

No partial budget total may be presented as complete.

- [ ] **Step 5: Commit**

Commit message: `eval: refresh workflow roster and pre-E7 budget`

---

### Task 6: Resources pack-delta reconciliation

**Files:**
- Read: revised Eval contracts and benchmark requirements
- Modify/version: `resources/v1/resource-requirements.yaml`
- Regenerate derived requirements matrix
- Create: `resources/pre-e7/RESOURCE-PACK-DELTA.md`

**Interfaces:**
- Consumes: new Eval consumer requirements.
- Produces: minimal acquisition/capture delta; no speculative packs.

- [ ] **Step 1: Map every new/changed consumer requirement to an existing pack or explicit gap**

- [ ] **Step 2: Test whether existing four packs can absorb the rebase through metadata/coverage changes**

- [ ] **Step 3: Justify any quantity increase by exact consumer ids**

- [ ] **Step 4: Run requirements validators and negative controls**

- [ ] **Step 5: Commit**

Commit message: `resources: reconcile packs with Pre-E7 scope`

---

### Task 7: Controller integration gate

**Files:**
- Update: `coordination/CONTROL-STATE.md`
- Create: `coordination/decisions/CONTROLLER-PRE-E7-INTEGRATION-<date>.md`
- Update shared plan/task status only after evidence is reviewed

**Interfaces:**
- Consumes: Canon, Eval and Resources branch returns.
- Produces: explicit go/no-go for evaluator qualification and E7.

- [ ] **Step 1: Verify Canon audit has no unexplained requirement fall-through**

- [ ] **Step 2: Verify Eval contracts cover all audited requirements without provider choices in PRP**

- [ ] **Step 3: Verify Resources can persist a multi-step, multi-parent outcome and recompute CpAO**

- [ ] **Step 4: Verify capability-v2 and benchmark remain sparse rather than combinatorial**

- [ ] **Step 5: Verify current official E2 roster and complete budget forecast**

- [ ] **Step 6: Decide E7**

Only the Controller may change E7 from BLOCKED to AUTHORISED, with an explicit approved budget and exact workflow roster.

## Self-review

- Spec coverage: all four new interfaces, E2 amendment, benchmark layering, backward compatibility, stream boundaries and E7 gate are assigned above.
- Placeholder scan: no TBD/TODO placeholders; date placeholder exists only in a future Controller filename pattern and is intentionally resolved at execution date, not a design unknown.
- Type/name consistency: Production Requirement Profile, Condition / Envelope Contract, Outcome / Production Topology Contract and Capability Contract v2 use the same names as the design spec and stream task packets.
