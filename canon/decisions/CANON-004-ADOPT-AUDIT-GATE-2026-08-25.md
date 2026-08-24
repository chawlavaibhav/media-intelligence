# CANON-004 Controller decision — adopt Post-Extraction Audit Gate v0.2

**Date:** 25 Aug 2026  
**Decision:** **ADOPT** the CANON-004 Post-Extraction Audit Gate v0.2, including the Controller correction pass merged via PR #6.

## Basis

CANON-004 tested one post-extraction audit layer across the frozen 16-book CANON-003 corpus. The design preserved the core architecture:

**SourceKnowledge → source systems / ontology → OperationalBindings → post-extraction Audit Gate**

The gate earned its place on five questions:

1. representation/source integrity;
2. evidence and claim origin;
3. application/product fit, with `no_current_binding` as a valid result;
4. pairwise source lineage / independence;
5. technology contingency for older technical material.

The Controller correction pass closed the only blocking design hole found in review: stale audits could previously continue to validate after their source representation changed. The adopted design now fingerprints the exact source artifacts the audit depends on and fails mechanically if any of them changes.

The correction pass also:

- retains `deterministic_composition` as an audit consumer; frequency in the 16-book corpus is not evidence of product irrelevance;
- keeps `human_workflow` as an audit consumer without creating a SPEC-04 target type;
- makes `recorded_at_commit` informational only and `source_snapshot` the sole enforced version mechanism;
- makes lineage promotion fail closed on unrecognised verdicts;
- keeps CANON-004 historically fixed to the original 16-book method-test corpus;
- leaves SPEC-01/03/04/05 unchanged pending this decision.

Final CANON-004 verification reported:

- integrated Canon validator: 0 errors; 16 books, 505 SourceKnowledge objects, 54 systems, 417 terms, 53 concepts, 111 bindings;
- Audit Gate validator: 0 errors; 16 records;
- test suite: 46 passed plus 5 subtests;
- no auto-running GitHub Actions workflow.

## Authorised authoritative changes

This decision authorises **only** the minimum changes CANON-004 requested.

### 1. SPEC-05 governance rule 5

Amend the existing rule so that independence for a `cross_source_concept` is established from Audit Gate lineage records, not from a count of distinct source identifiers.

Two origins may count as independent only when neither source's audit declares the other with a dependence relation:

- `shared_author`;
- `same_series`;
- `companion_volume`;
- `derivative_of`.

`independence_not_established` blocks promotion. A shared publisher or a citation alone does not defeat independence.

### 2. Canon extraction procedure

After source knowledge, source systems/ontology and operational bindings are stable and the fresh checkpoint is committed, the Audit Gate must run and validate before:

- cross-source promotion;
- downstream product/application use;
- Canon-consumption/retrieval work that treats that source as accepted knowledge.

An unaudited or stale source may remain in the repository as source evidence, but may not pass those downstream gates.

### 3. Make the adopted Audit Gate authoritative

Promote the tested v0.2 audit schema, records and validator out of experimental-only status into a stable Canon method location. Preserve the experiment history, but ensure there is exactly one active authoritative audit record per accepted source and exactly one normative procedure/schema for v0.2.

The existing 16 validated records are the initial backfill; do not reinterpret their source claims during promotion.

## Explicitly not authorised

- no SPEC-01 change;
- no SPEC-03 evidence-field migration;
- no new SPEC-04 target type or executor;
- no automatic cross-source concept creation;
- no numeric author/source quality or credibility score;
- no mandatory Creative IR binding;
- no new books or videos in the adoption task;
- no ingestion of deferred *Master Shots* or *The Conversations* as part of CANON-004/005;
- no RAG/Canon-lift experiment in the adoption task;
- no auto-running GitHub Actions workflow.

`deterministic_composition` and `human_workflow` remain **audit application-fit vocabulary only** unless a later task separately establishes an executable product target.

## Deferred reserve sources

*Master Shots* and *The Conversations* remain reserve sources outside the frozen 16-book CANON-004 evidence set. If their workers have completed usable extractions, they may be integrated later under the newly adopted method, including a fresh Audit Gate record. They are not part of this adoption implementation.

## Next gate

Open **CANON-005** as a small implementation task: apply the authorised SPEC-05 rule and extraction-procedure change, promote the tested Audit Gate representation to its authoritative home, update validation/tests/handoff, rerun all relevant checks, and stop for Controller review.
