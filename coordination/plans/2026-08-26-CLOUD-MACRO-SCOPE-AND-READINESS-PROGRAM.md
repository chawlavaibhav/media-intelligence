# Cloud Macro Scope & Readiness Program

**Date:** 26 Aug 2026  
**Status:** CONTROLLER-APPROVED FOR THREE PARALLEL CLOUD SESSIONS  
**Decision:** `coordination/decisions/CONTROLLER-CLOUD-MACRO-RECALIBRATION-2026-08-26.md`

## 1. Purpose

Run one substantial cloud-only research/design tranche across Canon, Eval and Resources before any paid model benchmark.

The goal is not to finish the product tonight. It is to leave the Controller with enough independent evidence to freeze the next empirical program without building scope from synthetic prompts or stale benchmark assumptions.

## 2. Product end-state

The product remains an API-native media production intelligence layer that turns customer intent into the cheapest reliable production route to an accepted commercial-media outcome.

The future router needs four kinds of knowledge:

1. **what customers/creators ask to make and what requirements recur;**
2. **what technical capabilities/failures matter and under which conditions;**
3. **what current production operations/workflows exist;**
4. **what independent evidence/material and persistence are required to measure the above honestly.**

This program gathers those four ingredients. It does not implement routing.

## 3. Why this is the right macro reset

The first overnight program successfully built useful infrastructure: Canon coverage/value-gate design, Eval's 36-capability/100-item measurement architecture, and Resources' requirement/persistence layer.

The gap surfaced afterwards: the benchmark was starting to define the product scope instead of observed request patterns and production workflows defining the benchmark.

The correction is not to collect random individual briefs. Research should identify **recurring request structures and co-occurrences**, then use authored benchmark prompts to cover that discovered space.

## 4. Three evidence axes

### Axis A — Request / use-case reality

Use large real-user prompt/request corpora and public commercial-use evidence to discover recurring structures. Treat every source's distribution as biased by its interface/community. Do not claim one corpus equals market demand.

Seed sources include DiffusionDB, VidProM, TIP-I2V, Arena Image, Arena-T2I-Hard and Artificial Analysis methodology. Workers may add stronger sources with clear provenance.

### Axis B — Capability / failure / workflow reality

Use current evaluation literature and official provider documentation to understand what can fail, what conditions change behaviour, how benchmarks become stale, and what production operations APIs actually expose.

Seed benchmark families include GenEval/GenEval 2, T2I-CompBench, VBench and later human-aligned video evaluation work. Exact current provider facts/prices require official provider documentation.

### Axis C — Evidence / independence / persistence reality

Determine what controlled reference/evaluator material and archival structure the empirical program needs, while keeping request-discovery data, benchmark construction data, calibration material and final holdouts appropriately separated.

## 5. Stream programs

### Canon — request space and requirement intelligence

Task: `canon/tasks/CANON-009-CLOUD-SCOPE-PROGRAM.md`

Canon's cloud worker researches the recurring grammar of media-generation requests and commercial use cases; compares that evidence with Creative IR, the current 30 synthetic briefs and live Canon coverage; and proposes gaps/rebalancing. The 30 briefs are probes to compare against the discovered space, not evidence about demand.

### Eval — capability, evaluator and workflow intelligence

Task: `eval/tasks/EVAL-007-CLOUD-EVAL-RESEARCH-PROGRAM.md`

Eval's cloud worker independently audits modern benchmark dimensions/failure modes, completes the current official workflow/API/pricing inventory where possible, audits evaluator families, and proposes the capability/condition/benchmark architecture needed after integration. It must not finalize new benchmark dimensions by itself.

### Resources — evidence, access, lineage and outcome persistence

Task: `resources/tasks/RES-003-CLOUD-EVIDENCE-PROGRAM.md`

Resources' cloud worker verifies access/rights/provenance of relevant request and evaluation data sources; rebaselines existing resource fit from committed evidence only; designs/proposes outcome-level multi-parent lineage/CpAO persistence; and researches legitimate supply routes for controlled missing packs without acquiring them.

## 6. Parallelism rule

The three streams deliberately work independently during this tranche.

Do not wait for another stream's branch to finish. Where another stream's output would eventually be needed, produce a provisional interface/mapping and list exactly what must be reconciled at integration.

This independence is useful: Canon should not define customer request patterns to match Eval's existing 36; Eval should not define capabilities to match Canon's 30 briefs; Resources should not select evidence because it makes either framework look complete.

## 7. Cloud environment

Assume fresh Claude Web sessions with GitHub + public web, but no laptop.

Workers may not assume access to:

- raw 5.70GB git-ignored Resources corpus;
- local books/PDFs/Downloads;
- proprietary font files not committed;
- laptop API keys or provider accounts;
- prior chat context.

Unavailable local material is recorded as `not_available_in_cloud_session`; it does not stop independent web/repository research.

## 8. Global prohibitions

- ₹0 spend.
- No paid/free provider generation calls, including "just one test".
- No checker/evaluator API calls.
- No empirical Capability Registry rows.
- No new Canon ingestion.
- No materially new media/dataset acquisition.
- No login, account creation, click-through terms, payment or bypass.
- No Production IR or Planner implementation.
- No worker merge to main.
- No architecture decision promoted from recommendation to fact.

## 9. Expected outputs at the Controller gate

### From Canon

- evidence-backed Media Request Grammar proposal;
- source-bias and confidence notes;
- recurring co-occurrence patterns;
- customer-specified vs commonly omitted production choices;
- comparison of the 30 synthetic bank against observed request space;
- Creative IR / Canon coverage gap proposals.

### From Eval

- modern benchmark/capability landscape and drift lessons;
- current official production-workflow/API roster with prices/features where verifiable;
- mapping of current 36 capabilities to external evidence, candidate gaps and condition variables;
- evaluator-family readiness/qualification proposal;
- proposed sparse/adaptive benchmark structure and provisional cost model.

### From Resources

- source/access/rights map for request/evaluation corpora;
- protected-set/leakage proposal separating discovery, calibration, benchmark and holdout roles;
- existing resource fit/gap map from committed evidence;
- outcome/multi-parent lineage and whole-outcome CpAO persistence proposal;
- justified controlled-pack supply routes/deltas, with no acquisition.

## 10. Controller integration gate

Only after all three return does the Controller decide:

1. first-product request/use-case taxonomy;
2. Media Request Grammar v1;
3. Production Requirement Profile shape;
4. capability contract v2;
5. condition/envelope taxonomy;
6. outcome/production topology contract;
7. whether/how to rebalance the 30-brief bank;
8. whether/how to revise the 100-item Eval bank;
9. exact evaluator qualification program;
10. exact resource acquisition program;
11. current model/workflow admission roster;
12. paid benchmark budget and wave design.

The gate must explicitly separate **market/request evidence**, **technical capability evidence** and **benchmark design**.

## 11. What comes after — NOT authorised yet

If integration succeeds, the likely next macro tranche is:

- targeted Resources acquisition/controlled-pack construction;
- evaluator qualification;
- Canon value-gate execution on the accepted/rebalanced request bank;
- then a paid admission benchmark and deeper workflow qualification.

That later tranche depends on Controller judgement over this program's findings, so it is not pre-approved.

## 12. Startup message for each Claude Web session

Each worker must read, in order:

`PROJECT-MEMORY.md` -> `coordination/PROJECT-CONTRACT.md` -> `shared/COMMUNICATION-STANDARD.md` -> `shared/AUTONOMY-POLICY.md` -> `coordination/CONTROL-STATE.md` -> this program -> its CHARTER/HANDOFF -> its assigned macro task.

It must state in chat that it is cloud-only, has no laptop/API-key assumptions, will spend ₹0, will not run generation/evaluator APIs, and will commit/push its branch without merging.
