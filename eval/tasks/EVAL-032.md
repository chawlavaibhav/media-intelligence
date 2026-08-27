# Task EVAL-032: Complete real temporal ingest and perturbation materialisation

**TASK ID:** EVAL-032  
**AUTONOMY MODE:** autonomous  
**RESOURCE BUDGET:** USD 0 / INR 0 external spend. Network retrieval of already-approved RES-005 sources is permitted. No checker/model/provider API calls.

## Objective

Turn the accepted RES-005 acquisition record into a fully ingestible real temporal qualification pack for EVAL-026, without running any candidate checker.

## Authority

- coordination/decisions/CONTROLLER-EVAL-026-INTEGRATION-2026-08-28.md
- coordination/decisions/CONTROLLER-RES-005-INTEGRATION-AND-TEMPORAL-MATERIAL-RESOLUTION-2026-08-28.md
- eval/v1/instruments/temporal-perturbation/**

## Required work

1. Rehydrate the exact 12 RES-005 source clips from the committed retrieval/provenance records.
2. Verify source and clip hashes before ingest.
3. Complete EVAL-026 ingest for **all 12**, using batching/streaming first so the prior PNG disk-expansion failure does not recur.
4. If normalisation/downscale is technically necessary:
   - preserve original-source hashes;
   - make the transform deterministic;
   - record the exact condition;
   - treat qualification as valid only under that recorded condition;
   - never silently replace the original material.
5. Materialise and verify the deterministic perturbation set against the real clips.
6. Preserve per-perturbation opportunity counts and the Controller-resolved pack-level coverage semantics.
7. Verify that rendered-character identity and photographed-face identity remain separate populations.
8. Produce a fresh-clone/rebuild check where feasible.

## Success condition

Durable evidence establishes:
- 12/12 real clips successfully ingested under an explicit execution condition;
- perturbation material can be deterministically built for every supported opportunity;
- the 13 perturbation types remain intact;
- the 9 temporal capabilities retain the accepted 7 full + 2 negative-direction-only coverage shape;
- no checker observations have occurred.

## Restrictions

Do not select or run a temporal checker. Do not set qualification pass marks. Do not claim any evaluator is qualified. Do not create Registry rows. Do not modify Resources-owned historical acquisition evidence.

Commit and push to `work/eval-032-temporal-material-completion`. Do not merge.