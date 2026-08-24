# Task CANON-002: Williams proximity — second current-schema extraction

**TASK ID:** CANON-002
**OBJECTIVE:** Produce a fresh current-schema extraction of Robin Williams' proximity chapter and use it to test whether the CANON-001 extraction method, V0 granularity rule, independent visual-evidence pass, and current ontology work on a materially different kind of source without changing the schemas.

**WHY WE ARE DOING THIS:** CANON-001 showed the current source-knowledge / bindings split can work on Molly Bang, but one source is not enough. Williams is a useful second case because the chapter is short, concrete, design-focused, and explicitly authors its own problem/remedy guidance. This task tests whether the method travels rather than beginning broad ingestion.

**COMMUNICATION STANDARD:** inherits `shared/COMMUNICATION-STANDARD.md`; plain English without reducing substance, minimum sufficient wording, no invention, evidence separated from inference. Important findings/questions must be explained in chat and also written to the Controller Brief/checkpoint and pushed to GitHub.

**INPUTS:**
- `coordination/PROJECT-CONTRACT.md`
- `coordination/RUNBOOK.md`
- `shared/COMMUNICATION-STANDARD.md`
- `canon/CHARTER.md`
- `canon/HANDOFF.md`
- `canon/knowledge/SPEC-03-source-knowledge.md`
- `canon/knowledge/SPEC-04-operational-bindings.md`
- `canon/knowledge/SPEC-05-knowledge-ontology.md`
- `canon/sources/williams-proximity-p15-32.txt`
- `canon/tasks/CANON-001-CONTROLLER-BRIEF.md` only for the approved CANON-001 method decisions, especially the V0 granularity rule
- `canon/knowledge/SPEC-01-creative-ir.md` **binding-stage only**; do not use it while deciding what source knowledge exists
- any already-available local page images/PDF matching this exact Williams source may be used read-only for the visual pass after provenance is verified; do not acquire a new source and do not commit copyrighted page renders

**SEALED UNTIL THE FRESH CHECKPOINT EXISTS:**
- `canon/findings/FINDINGS-04-williams-proximity-pass1.md`
- `canon/knowledge/migration/AUDIT-williams.md`
- `canon/knowledge/atoms-v1-superseded/williams-proximity-atoms.yaml`
- any other historical Williams extraction/summary derived from these files

Do not open, grep, search, quote, or use the sealed material before the fresh checkpoint commit. After the checkpoint, comparison is allowed and disagreement is evidence; do not converge to the historical version.

## Method

### Phase 0 — provenance and visual-source gate

Before extraction, verify that `williams-proximity-p15-32.txt` is readable and that any local visual source you plan to inspect actually matches the same chapter/page content. Edition or page-number mismatch is a provenance problem, not something to guess through.

A **true independent visual pass is part of this task**. If no matching visual source is already available locally, or its provenance cannot be verified, STOP and report the blocker rather than silently downgrading the method. Rendering matching pages ephemerally from an already-available local source is permitted; committing those page images is not.

### Phase 1 — independent visual-evidence pass

Before creating SourceKnowledge objects and without consulting sealed historical work, inspect the chapter visually and create a visual-evidence ledger.

The purpose is not to confirm text-derived claims. Ask independently:
- what relationship/change is directly visible in each example or before/after pair?
- what can the visual itself support?
- what would require the author's prose to interpret?
- does a figure teach or demonstrate something that would be lost in plain-text extraction?

Do not turn a visual observation into a source claim unless the evidence supports that strength. Record uncertainty explicitly.

### Phase 2 — fresh source representation

Extract the source under SPEC-03 using the CANON-001 V0 granularity rule:

> Create a separate SourceKnowledge object when a claim can meaningfully be retrieved, supported, contradicted, or qualified independently. Do not split merely because there is another example, explanation, or restatement. Do not target an object count.

Use task-scoped fresh IDs; do not reuse historical IDs:
- SourceKnowledge: `sk_rw_c002_0001...`
- SourceConceptSystem: `scs_rw_c002_001...`
- ontology term: `t_rw_c002_0001...`
- binding: `bnd_rw_c002_0001...`

Preserve source-authored problem/remedy language as source evidence rather than translating it prematurely into product vocabulary. Keep `source_explicit` versus extractor inference visible at every level.

Where a granularity decision is genuinely ambiguous, make the least assumptive defensible choice and record the case in the findings. Do not invent a new granularity rule mid-task.

### Phase 3 — systems, ontology, then bindings

Create SourceConceptSystems where the source teaches an interacting set, procedure, dependency, priority, trade-off, or other system supported by SPEC-03.

Use only existing SPEC-05 relation types. `distinct_from` is permitted only in the SPEC-05 ontology layer, not inside SPEC-03 `intra_source_relations`.

Only after the source representation is stable may you open/use SPEC-01 to draft SPEC-04 operational bindings. Zero bindings is acceptable. Canon knowledge must not be admitted, rejected, split, or rewritten merely to make a product binding easier.

### Phase 4 — freeze, then historical comparison

Validate all fresh files mechanically where possible. Commit a **fresh pre-history checkpoint** containing the visual ledger and fresh current-schema representation before opening any sealed historical Williams material.

After that checkpoint, compare against the old finding/audit/atoms. Record:
- knowledge found by both;
- knowledge found only by the fresh method;
- knowledge found only historically;
- whether differences come from granularity, visual evidence, schema separation, or genuine omission;
- whether the V0 granularity rule was usable without inventing exceptions;
- whether Williams produces materially richer source-stated problem/remedy ontology than Bang, without treating one source as proof of a general rule.

Do not silently back-fill the fresh extraction after seeing history. If historical comparison reveals an objective fresh error, correct it only when the source independently proves the correction, and record the post-comparison change explicitly.

## IN SCOPE

- one fresh source-faithful Williams extraction
- independent visual-evidence ledger before text-derived SourceKnowledge is finalised
- SourceKnowledge and SourceConceptSystem objects
- source-local ontology terms/relations using the existing vocabulary only
- operational bindings where supported
- explicit application of the V0 granularity rule
- mechanical validation
- pre-history checkpoint commit
- post-checkpoint comparison against the sealed historical work
- finding whether the current method appears to travel from a principles-heavy source (Bang) to a source with explicit design problems/remedies (Williams)

## OUT OF SCOPE

- no schema changes
- no new ontology relation types or term kinds
- no cross-source canonical concepts
- no broad curriculum ingestion
- no third source
- no Canon-consumption/RAG experiment
- no model selection/provider claims
- no Eval battery changes
- no new copyrighted-source acquisition
- no committing full copyrighted pages/renders
- no rewriting/deleting historical Williams files
- no retroactive re-audit of CANON-001

## DELIVERABLES

- `canon/knowledge/current/robin-williams-proximity/visual-evidence-ledger.yaml`
- `canon/knowledge/current/robin-williams-proximity/source-knowledge.yaml`
- `canon/knowledge/current/robin-williams-proximity/source-concept-systems.yaml`
- `canon/knowledge/current/robin-williams-proximity/operational-bindings.yaml`
- `canon/knowledge/current/robin-williams-proximity/ontology-mappings.yaml`
- `canon/findings/CANON-002-williams-current-schema-extraction-findings.md`
- `canon/tasks/CANON-002-CONTROLLER-BRIEF.md`

**AUTONOMY MODE:** autonomous, after Phase-0 provenance/visual-source gate passes. Stop at the Controller Brief; do not start CANON-003.

## RESOURCE BUDGET

- sources/items: one named Williams chapter only
- storage: negligible; text/YAML/Markdown plus ephemeral local page rendering only
- API spend: ₹0 / $0 paid APIs
- generations/retries: none
- acquisition: none; use only source material already available locally/repo

**APPROVED DEPENDENCIES:** CANON-001 is substantively approved. Its V0 granularity rule and the decision to treat visual evidence as an independent completeness problem are binding for this task. Canon-consumption experiments remain paused.

**IMPORTANT SPEC-03 NOTE:** CANON-001 established that the Molly Bang worked example in SPEC-03 incorrectly says the source never states the principles-in-conjunction claim. The Controller has approved correcting that factual example. Until the correction is visible in the branch, do not use that example as evidence for deciding `source_explicit` versus `extractor_synthesis`; use the actual schema rule and source evidence.

**STOP CONDITIONS:**
- no matching/provenance-verified Williams visual source is available for the independent visual pass
- edition/page/source mismatch that cannot be resolved from evidence
- existing schemas cannot represent source evidence honestly
- a new ontology relation type/term kind appears necessary
- the V0 granularity rule cannot be applied without inventing a new policy
- any temptation to alter schema or task method after seeing the historical comparison
- cross-stream implication requiring architecture/policy change
- source/data integrity uncertainty that could contaminate the extraction

**HUMAN APPROVAL TRIGGERS:** schema/ontology expansion; changing the granularity rule; changing the visual-pass method; adding/acquiring another source; declaring a cross-source canonical concept; changing Canon scope; any paid/resource expansion.

**RESULT LOCATION:** `canon/tasks/CANON-002-CONTROLLER-BRIEF.md` plus the deliverables above.
