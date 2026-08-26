# Controller decision — V1 overnight integration

**Date:** 26 Aug 2026  
**Status:** ACCEPTED AND MERGED

## Decision

The Controller reviewed the Canon, Eval and Resources V1 overnight branches, assigned bounded correction passes, reviewed the corrections, and then ran one final Eval↔Resources storage-integration micro-fix. The three streams are accepted as coherent V1 architecture/design work and merged to `main`.

Merge order and merge commits:

1. Resources — PR #19 → `4bfb4fe2ec103ea11e246fb930e6e0c5eda9ef91`
2. Eval — PR #17 → `f17e2587989232bea47b8f86acdc76e3ba499794`
3. Canon — PR #18 → `ae540c6bf5855e6cc4c09e8d2c28ff53666c2377`

Final verified `main` at integration: `ae540c6bf5855e6cc4c09e8d2c28ff53666c2377`.

## Accepted cross-stream ownership

- **Canon owns** durable creative/production knowledge, the 30-commercial-brief bank and the Canon value-gate design.
- **Eval owns** the 36-capability measurement contract, evaluator semantics, the 100-item generate-once bank, qualification design, and Capability Registry semantics.
- **Resources owns** independent evidence supply, rights/integrity/lineage, protected-set allocation, and the persistent empirical attempt/artifact/measurement/acceptance contract.
- **Production Planner/routing remains unbuilt.** No current-model routing claim exists.

## Accepted shared interfaces

### Canon

- Live Canon remains 19 accepted sources.
- The first-product coverage rebaseline and 30-brief bank are accepted.
- The early value gate is design-ready but **not executed**.
- Two independent reviewers are required.
- Only 7 `coverage_probe` briefs vote on continuation; 5 `gap_probe` briefs are diagnostic only.
- Any Canon intent regression blocks automatic continuation.
- Real generic-control authoring must come from a fresh Canon-naive session; the Canon-reading worker must not author the control used in the real gate.
- Candidate source portfolio is research only; no candidate is automatically approved for ingestion/acquisition.

### Eval

- 36-capability contract and 100-base-item bank are accepted.
- Critical capability opportunity floor is satisfied after correction.
- Generate-once / measure-many architecture is accepted.
- Experimental repeat and production retry are distinct records and costs.
- Registry writes fail closed on mixed cells, synthetic measurements, unqualified instruments, invalid repeat structure and production retries.
- Capability Registry still contains **zero empirical current-model entries**.
- No subjective/perceptual evaluator family is qualified yet.
- E2 current official model/API/access/pricing inventory remains incomplete and must be finished from official current provider sources before paid qualification/benchmark execution.

### Resources

- Resources remains a requirement-driven evidence supply chain, not a dataset-collection target.
- Existing corpus remains 34,786 items / 5.70 GB across 8 acquired sources with 4 blocked, based on previously committed evidence; the cloud workers did not re-open the raw corpus.
- Three independence levels are authoritative for protected-set work: byte identity, content lineage and source lineage.
- Unknown lineage is indeterminate, never silently independent.
- Resources persistent empirical-storage contract v2.1 is authoritative.
- One provider/API/transform call = one trial.
- Persistent entities are: attempt → optional artifact → many measurements, plus optional acceptance.
- Provider failures/refusals are preserved on attempts, not duplicated as fake measurement absences.
- Cost values resolve through immutable cost-ledger records.
- Controlled product, person, AV and commercial-creative packs remain missing; no new acquisition was authorised during the overnight tranche.

## Eval ↔ Resources final integration gate

The final Eval ledger micro-fix was validated against Resources branch head `db54e972a8a0d593e3c3455f630641906e7a58f6`, schema v2.1.

Accepted verification evidence:

- Eval harness self-test: 107/107.
- Eval verification suites: 11 suites, 0 failing.
- Eval dummy archive → Resources `check_empirical_archive.py`: exit 0.
- Cross-stream violations after the micro-fix: attempts 0; artifacts 0; measurements 0; acceptances 0; cost ledger 0.
- No paid calls, no empirical Registry rows and no instrument qualification occurred in these tests.

## Explicit remaining gates

The overnight program is merged, but the following are **not authorised merely by this merge**:

1. Paid model/checker/evaluator/generation runs.
2. Empirical Capability Registry population.
3. Canon value-gate execution until independent generic controls and two reviewers are arranged.
4. New Canon source ingestion/acquisition.
5. Materially new Resources acquisition/capture without explicit approval of the route and rights posture.
6. Production IR / Production Planner / routing implementation.

`EVAL-006` remains paused historical work and must not be resurrected implicitly.

## Next Controller sequence

Before material paid benchmarking:

1. finish Eval E2 using current official provider documentation;
2. resolve/approve the controlled Resources packs and collect only the required material;
3. arrange independent Canon generic-control authoring and run the small Canon value gate;
4. qualify evaluator families against protected calibration/qualification material;
5. approve the exact generation/measurement budget;
6. only then begin current-model empirical qualification and populate the Capability Registry.

This integration is an architecture/design milestone, not evidence that Canon improves outcomes or that any current model/workflow meets production quality.
