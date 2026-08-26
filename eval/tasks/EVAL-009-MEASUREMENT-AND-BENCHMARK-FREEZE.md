# EVAL-009 — Measurement & Benchmark Freeze

**AUTONOMY:** autonomous  
**ENVIRONMENT:** Claude Web/cloud; GitHub + public web as needed  
**BUDGET:** ₹0 external spend  
**BRANCH:** `work/eval-009-measurement-freeze`

## Objective

Turn the accepted macro research into the exact **measurement-side package ready for Controller freeze** before any paid current-model testing.

This task chooses what the lab must measure and the scientific Wave-1 model/workflow roster. It does **not** choose access routes or providers based on credits/availability.

## Read first

1. `PROJECT-MEMORY.md`
2. `coordination/CONTROL-STATE.md`
3. `coordination/decisions/CONTROLLER-MACRO-RESEARCH-INTEGRATION-2026-08-26.md`
4. `coordination/decisions/CONTROLLER-FINAL-PRE-EXECUTION-FREEZE-2026-08-26.md`
5. `coordination/plans/2026-08-26-FINAL-PRE-EXECUTION-FREEZE-PROGRAM.md`
6. EVAL-007 research under `eval/research/pre-e7-macro/`
7. EVAL-008 candidate-universe research under `eval/model-access/2026-08-26/` if present on main; otherwise inspect PR/branch evidence without treating it as authoritative
8. current 36-capability contract, 100-item bank, evaluator-family specs and Registry schema
9. CANON-009 request-space research

## Work packages

### E9-A — Capability Contract v2 proposal

Audit the current 36 and implement the Controller-approved direction without chasing a target count.

Produce exact V1→V2 mapping for every existing id:
- unchanged;
- renamed/refined;
- split;
- retired/absorbed;
- dormant.

Resolve, with explicit reasoning:
- 2D spatial vs depth/3D relationship;
- script/word correctness vs pronunciation/intelligibility;
- reproducibility vs repairability;
- human anatomy integrity while preserving hand-specific diagnostics;
- person identity vs wardrobe/clothing invariants;
- camera/framing instruction fidelity;
- sequence/state continuity;
- technical visual integrity;
- voice identity/consistency;
- style-reference fidelity boundary;
- cross-asset identity boundary;
- campaign/variant-set consistency boundary.

A new capability is allowed only if existing capability + condition + observation scope cannot represent the failure cleanly.

### E9-B — Dependency-aware scoring contract

Define prerequisite graph semantics for compound requirements.

Freeze the distinction among:
- pass;
- fail;
- genuinely not applicable;
- not measured/instrument unavailable;
- `blocked_by_prerequisite_failure` or equivalent final machine id.

A required descendant blocked because an ancestor failed remains **unsatisfied at brief/outcome acceptance**.

Provide negative fixtures proving aggregation cannot forgive a failed ancestor.

### E9-C — Condition / envelope contract

Freeze explicit condition families sufficient to make evidence interpretable.

At minimum cover:
- delivery/duration/size/platform;
- content/entity load;
- reference type/count/quality;
- physical interaction/action load;
- camera/motion/framing load;
- constraint/exactness load;
- workflow mode;
- sequence/shot/set structure;
- language/script/speaker topology;
- input quality;
- decision provenance;
- output scale/set structure;
- requested operation as customer-side provenance, distinct from workflow mode.

No single complexity score.

### E9-D — Production Requirement Profile v1 proposal

Define the provider/model-agnostic compiled view between Creative IR/request representation and future Production IR.

Each requirement must expose at least:
- id/type;
- source operation/provenance;
- strength;
- resolved value or unresolved state;
- scope/observation unit;
- required capabilities;
- relevant conditions;
- acceptance consequence.

It must not contain provider/model/routing decisions.

### E9-E — Benchmark v2 Wave-1 design

Preserve the V1 100-item bank as a historical/baseline artifact. Do not silently rewrite it.

Design the runnable Wave-1 benchmark as four layers:
1. atomic probes;
2. compound scenarios with prerequisite graph;
3. sparse/adaptive condition sweeps;
4. end-to-end accepted outcomes.

Cross the benchmark with materially different requested operations. No cartesian product.

Produce exact:
- item counts;
- asset-generation counts;
- measurement fan-out;
- repeats/retries semantics;
- evaluator-call counts;
- human-review counts;
- stop/expansion rules for sparse sweeps.

If CANON-010 is not yet available, parameterise extension-bank slots against the Controller-approved operations and mark the exact reconciliation point rather than inventing Canon output.

### E9-F — Evaluator qualification map

For every active Wave-1 capability identify:
- evaluator family/instrument type;
- deterministic vs model-based vs human judgement;
- qualification material required;
- false-pass/false-fail risks;
- whether an existing instrument can be reused;
- whether the capability is measurable in Wave 1;
- fallback/adjudication path.

Do not declare an instrument qualified without an executed qualification.

### E9-G — Scientific Wave-1 model/workflow roster

Start from EVAL-008 as candidate-universe research but challenge every row.

Selection rule: each admitted row must answer a distinct, product-relevant empirical question that materially affects production design, acceptance, repair or CpAO.

Do **not** use availability on Frontier Clouds, fal, direct vendors, account status or user credits as an admission criterion.

Do not keep a model solely because:
- it leads a generic leaderboard;
- it is new/topical;
- it has a different national/vendor/training lineage without a concrete failure hypothesis;
- it has an unverified marketing claim.

Specifically, the reported ~99% Hindi/Bengali character-accuracy claim in EVAL-008 is not load-bearing unless primary evidence is found.

For every admitted row state:
- hypothesis;
- capability/condition coverage;
- nearest redundant candidate and why both are/are not needed;
- required workflow mode;
- whether it is core Wave 1 or reserve.

Produce a **scientific roster before sourcing**. Cost/access may be reported only as unresolved external inputs for later Controller trade-off.

### E9-H — Call-count and cost-input forecast

Produce deterministic generation/evaluator/human call counts from the Wave-1 design.

Where official prices are unavailable, leave price fields null. Do not total a partially resolved budget as though it were exact.

Output the formula/table that EVAL-010 pricing can populate later.

## Deliverables

Under `eval/pre-execution-freeze/` create at minimum:
- `CAPABILITY-CONTRACT-v2.yaml`
- `CAPABILITY-V1-V2-MAPPING.md`
- `DEPENDENCY-SCORING-CONTRACT.yaml`
- `CONDITION-ENVELOPE-CONTRACT.yaml`
- `PRODUCTION-REQUIREMENT-PROFILE-v1.yaml`
- `BENCHMARK-v2-WAVE1.md`
- `BENCHMARK-v2-WAVE1.yaml`
- `EVALUATOR-QUALIFICATION-MAP.yaml`
- `SCIENTIFIC-WAVE1-MODEL-ROSTER.md`
- `SCIENTIFIC-WAVE1-MODEL-ROSTER.yaml`
- `WAVE1-CALL-COUNT-FORECAST.yaml`
- validators/negative fixtures sufficient to enforce the contracts
- `EVAL-009-CONTROLLER-BRIEF.md`

## Mechanical gates

Fail if:
- V1 capabilities disappear without explicit mapping;
- a required descendant can pass/be ignored after prerequisite failure;
- requested operation is substituted for workflow mode;
- PRP contains provider/model/routing fields;
- benchmark performs a cartesian sweep;
- an unqualified evaluator is described as qualified;
- scientific roster uses access/credits as admission rationale;
- a price is guessed;
- a partially unresolved forecast is totalled as an exact budget;
- historical V1 36-capability or 100-item artifacts are silently modified.

## Restrictions

No generation/model calls. No evaluator API calls. No Registry rows. No provider account actions. No paid spend. No Production IR/Planner implementation. No merge.

Commit and push the branch. Return the Controller brief and commit SHA only after the whole program is complete.
