# Task CANON-005: Apply adopted Audit Gate v0.2

**TASK ID:** CANON-005  
**STATUS:** Controller-opened 25 Aug 2026. Implementation task for the already-approved CANON-004 decision.

## OBJECTIVE

Apply the Controller-adopted CANON-004 Post-Extraction Audit Gate v0.2 as the authoritative Canon method, with the smallest possible change surface.

This is an implementation/promotion task, not another design experiment.

## AUTHORITATIVE INPUTS

Read first:

- `canon/decisions/CANON-004-ADOPT-AUDIT-GATE-2026-08-25.md`
- `canon/findings/CANON-004-CONTROLLER-BRIEF.md`
- `canon/findings/CANON-004-audit-gate-design.md`
- `canon/experiments/audit-gate-v0.2/SCHEMA-audit-record-v0.2.md`
- `canon/validation/validate_audit_gate_v02.py`
- `tests/test_validate_audit_gate_v02.py`
- current `canon/knowledge/SPEC-05-knowledge-ontology.md`
- `canon/HANDOFF.md`
- `shared/COMMUNICATION-STANDARD.md`

Do not reinterpret CANON-004. The Controller decision is final for this task.

## REQUIRED CHANGES

### 1. Apply the authorised SPEC-05 governance amendment

Modify Governance rule 5 in `canon/knowledge/SPEC-05-knowledge-ontology.md` so that a `cross_source_concept` cannot establish independence merely by listing distinct source ids.

The authoritative rule must state, consistently with CANON-004:

- independence is established from the active Audit Gate lineage records;
- `shared_author`, `same_series`, `companion_volume`, and `derivative_of` defeat independence for that source pair;
- `independence_not_established` blocks promotion;
- a shared publisher or `cites_source` alone does not defeat independence;
- independence is pairwise, not a permanent global property of a source.

Do not add unrelated ontology relation types or change concept semantics.

### 2. Promote Audit Gate v0.2 out of experimental-only status

Create one stable authoritative home for the adopted Audit Gate method and its active records.

Preferred shape unless repository constraints justify a smaller equivalent:

- `canon/audit/AUDIT-GATE-v0.2.md` — normative adopted procedure/schema;
- `canon/audit/records/*.audit.yaml` — exactly one active audit record per accepted source.

The experiment history under `canon/experiments/audit-gate-v0.2/` must remain understandable as historical design/test evidence, but downstream tooling must have **one unambiguous active source of truth**. Do not leave two independently editable active copies of the same 16 records.

A clean move plus a historical README/pointer is preferable to duplicate active records.

Do not create `SPEC-06`; CANON-004 explicitly concluded that a new authoritative spec was not required. This is a Canon method/procedure layer plus the one SPEC-05 governance change.

### 3. Make the extraction gate explicit

Authoritatively document the accepted order:

1. source extraction stabilises;
2. source systems/ontology stabilise;
3. OperationalBindings stabilise;
4. fresh checkpoint is committed;
5. Audit Gate record is written against those exact bytes;
6. Audit Gate validator passes;
7. only then may cross-source promotion, downstream product/application use, or Canon-consumption/retrieval treat that source as accepted downstream knowledge.

An unaudited or stale source may remain as source evidence but may not pass those downstream gates.

Do not reintroduce mandatory bindings.

### 4. Preserve the adopted audit vocabulary

Retain all seven application-fit consumers in v0.2, including:

- `deterministic_composition`;
- `human_workflow`.

These remain audit vocabulary only. Do not add a SPEC-04 target type or executor for either.

Retain the adopted `source_snapshot` behaviour:

- deterministic content fingerprint;
- exact covered artifact set from CANON-004 unless a mechanical move requires path-only updates;
- fail stale on byte change;
- fail on missing covered artifact;
- `recorded_at_commit` informational only;
- no snapshot-refresh shortcut that can rubber-stamp a changed source without rerunning the audit.

### 5. Update validator and tests to the authoritative paths

Update `canon/validation/validate_audit_gate_v02.py` and its tests so they read the active authoritative audit records, not the experimental directory.

Preserve all existing protection, including:

- reference resolution;
- controlled vocabularies;
- anti-score rule;
- evidence-origin consistency;
- complete application-fit coverage;
- pairwise lineage checks;
- fail-closed independence verdict handling;
- stale-audit snapshot checks;
- 16-source coverage check.

Do not weaken tests merely to make the move pass.

### 6. Preserve the 16-book evidence set

CANON-005 must not ingest new sources.

Specifically do **not** integrate:

- *Master Shots*;
- *The Conversations*;
- any new books, courses or videos discovered by Work/Resources.

Those will be handled after the adopted method is fully authoritative and revalidated.

### 7. Update handoff/status

Update `canon/HANDOFF.md` to state:

- CANON-004 was Controller-adopted on 25 Aug 2026;
- Audit Gate v0.2 is now authoritative after CANON-005 completes;
- the exact active method/record paths;
- unaudited/stale sources are blocked from downstream promotion/use;
- the 16 current accepted books have active audits;
- deferred reserve sources remain outside the 16-book method-test set;
- next work is Controller-assigned only.

If a coordination/status file outside Canon needs a change, propose it rather than silently editing another workstream's ownership area unless repo governance explicitly authorises Controller-owned coordination edits.

## VERIFICATION

Before returning, run **fresh from the final branch head**:

1. `python canon/validation/validate_canon003_integrated.py --root .`
2. `python canon/validation/validate_audit_gate_v02.py --root .`
3. `python -m pytest tests/ -q`

Also mechanically confirm:

- exactly 16 active audit records;
- no active duplicate copy of those records remains under an experimental path;
- all 16 snapshots validate against current source bytes;
- the only authoritative spec changed is SPEC-05;
- SPEC-01, SPEC-03 and SPEC-04 are byte-identical to task-base `main`;
- no source-knowledge/system/binding meaning was changed as part of promotion;
- no GitHub Actions workflow was added.

Report actual commands, exit codes, test counts, corpus counts, and changed authoritative files.

## STOP / ESCALATION CONDITIONS

Stop and return to Controller rather than expanding scope if:

- promoting the Audit Gate requires changing SourceKnowledge semantics;
- a second authoritative spec appears necessary;
- the move makes stale-audit validation impossible without weakening the content fingerprint;
- an existing 16-book audit no longer validates for a substantive reason rather than a path-only promotion issue;
- SPEC-01/03/04 would need modification;
- a deferred/new source becomes necessary to complete adoption.

## NON-GOALS

CANON-005 does not:

- design a new Audit Gate version;
- run a Canon-vs-vanilla lift experiment;
- build RAG/retrieval;
- build Production IR;
- create cross-source concepts;
- add new sources;
- add model/API spend;
- change evaluation resources;
- create auto-running CI.

## DELIVERABLE

Open one PR from a dedicated branch, preferably `work/canon-005`, containing only the authoritative adoption changes. Return a concise Controller Brief with:

- exact files promoted/moved;
- exact SPEC-05 text changed;
- verification evidence;
- any migration/path consequence;
- confirmation that the 16-source content is otherwise unchanged.

Stop after the PR. Do not self-assign the reserve-book integration or Canon expansion task.
