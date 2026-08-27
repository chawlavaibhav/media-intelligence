# Task EVAL-033: Temporal checker candidate and precommit package

**TASK ID:** EVAL-033  
**AUTONOMY MODE:** autonomous  
**RESOURCE BUDGET:** USD 0 / INR 0. Public web research permitted. No paid/model/evaluator API calls on qualification material.

## Objective

Reduce temporal qualification to a single Controller decision by identifying the best current checker candidate(s), exact executable routes and a precommittable qualification gate before any EVAL-032 qualification observations are seen.

## Read first

- eval/v1/instruments/FAMILY-4-TEMPORAL-VIDEO.md
- eval/v1/instruments/QUALIFICATION-MASTER-SPEC.md
- eval/pre-execution-freeze/CAPABILITY-CONTRACT-v2.yaml
- eval/v1/instruments/temporal-perturbation/**
- coordination/decisions/CONTROLLER-EVAL-026-INTEGRATION-2026-08-28.md
- coordination/decisions/CONTROLLER-RES-005-INTEGRATION-AND-TEMPORAL-MATERIAL-RESOLUTION-2026-08-28.md

## Work

Research current official/primary sources for viable temporal checker approaches, including local/open-source and API/VLM/video-understanding routes where appropriate.

For each serious candidate record:
- exact model/software/version;
- route/API availability;
- input limits and video handling;
- whether it can detect and localise each of the 13 perturbation classes;
- deterministic sampling/configuration;
- price/billing unit if paid;
- expected latency and operational constraints;
- privacy/data-retention constraints if relevant;
- reproducibility/version pinning;
- known blind spots.

Implement adapters or local wrappers **only enough for dry-run/interface verification on toy/non-qualification material**.

Produce:
- a preferred candidate and one fallback;
- exact configuration hashes;
- proposed repeat count;
- **proposed pass marks per perturbation type**, false-positive gate on clean controls, and localisation gate;
- explicit treatment of the two negative-direction-only capabilities;
- which capabilities still require human adjudication under the frozen map.

## Critical precommit rule

Do **not** run any candidate on the protected 12-clip qualification observations, and do not inspect any such results if they exist elsewhere.

The pass-mark package must be proposed before those observations.

Controller must separately approve/freeze candidate + numeric pass marks before a real qualification run.

## Deliverables

- `eval/research/EVAL-033-TEMPORAL-CHECKER-CANDIDATES.md`
- machine-readable candidate/precommit proposal under `eval/v1/instruments/temporal-perturbation/`
- narrow adapter/dry-run code/tests if useful.

Commit and push to `work/eval-033-temporal-checker-precommit`. Do not merge.