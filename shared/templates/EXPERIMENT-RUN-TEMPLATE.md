# Experiment Run — <experiment ID> v<N>

**task_id:**
**hypothesis:** (reference coordination/ASSUMPTIONS.md entry)
**predefined_interpretation:** what result would mean what, decided BEFORE running

**versions:**
- canon_version:
- creative_ir_version:
- source_knowledge_schema_version:
- eval_battery_version:
- evaluator_version:
- corpus_version:
- capability_registry_version:
- models: (exact vendor/model/version strings)

**settings:** (temperature, retrieval config, etc — whatever is specific to this run)
**sample_counts:**
**random_seeds:**
**retry_policy:**
**cost:**
**timestamp:**
**result_location:**

---
**Rule:** if the protocol/evaluator needs to change after seeing a result, this run is FROZEN as
evidence. A new experiment run file, `v<N+1>`, is created after Controller approval. Never edit
this file post-hoc to reflect a changed method and call it the same run.
