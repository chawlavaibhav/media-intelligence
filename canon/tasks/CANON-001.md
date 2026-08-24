# Task CANON-001: First current-schema Canon extraction

**TASK ID:** CANON-001
**OBJECTIVE:** Produce the first fresh Canon source representation created directly under SPEC-03 / SPEC-04 / SPEC-05, using an already-available source, without changing any schema or running a Canon-consumption experiment.
**WHY WE ARE DOING THIS:** The six original sources were probes created before the current schema and later re-audited. We need one clean end-to-end current-schema extraction before scaling ingestion.

**INPUTS:**
- `coordination/PROJECT-CONTRACT.md`
- `canon/CHARTER.md`
- `canon/HANDOFF.md`
- `canon/knowledge/SPEC-03-source-knowledge.md`
- `canon/knowledge/SPEC-04-operational-bindings.md`
- `canon/knowledge/SPEC-05-knowledge-ontology.md`
- `canon/sources/molly-bang-principles-p42-91.txt`
- relevant rendered figures under `canon/sources/figures/`
- `canon/knowledge/migration/AUDIT-molly-bang.md` only as historical comparison after the fresh extraction is complete

**IN SCOPE:**
- fresh source-faithful extraction from the named source
- SourceKnowledge objects and SourceConceptSystem objects supported by the source
- precise provenance and source-stated vs extractor-inferred distinctions
- operational bindings only where genuinely supported; zero bindings is acceptable
- ontology mappings using existing relation types only
- validation against frozen schemas
- comparison against the prior audit only after extraction, to identify differences without forcing agreement

**OUT OF SCOPE:**
- no schema changes
- no new ontology relation types
- no cross-source canonical concepts
- no curriculum expansion
- no RAG/vector database work
- no Canon planning/evaluation experiment
- no model-selection or provider claims
- do not rewrite/delete historical atom or audit files

**DELIVERABLES:**
- `canon/knowledge/current/molly-bang/source-knowledge.yaml`
- `canon/knowledge/current/molly-bang/source-concept-systems.yaml`
- `canon/knowledge/current/molly-bang/operational-bindings.yaml`
- `canon/knowledge/current/molly-bang/ontology-mappings.yaml`
- `canon/findings/CANON-001-current-schema-extraction-findings.md`
- `canon/tasks/CANON-001-CONTROLLER-BRIEF.md`

**AUTONOMY MODE:** autonomous

**RESOURCE BUDGET:**
- sources/items: one named source only
- storage: negligible; text/YAML/Markdown only
- API spend: ₹0 / $0 paid APIs
- generations/retries: none
- other: use local/source files already present; do not acquire new copyrighted material

**APPROVED DEPENDENCIES:** SPEC-03 / SPEC-04 / SPEC-05 as currently frozen; existing source text and rendered figures.
**STOP CONDITIONS:** architecture inadequacy; source/figure provenance uncertainty that would contaminate extraction; need for a new ontology relation type; any temptation to change schema to fit the source; cross-stream implications that require policy change.
**HUMAN APPROVAL TRIGGERS:** any schema/ontology expansion, declaring a cross-source concept, adding a new source, or changing Canon scope.
**RESULT LOCATION:** `canon/tasks/CANON-001-CONTROLLER-BRIEF.md` plus the deliverables above.
