# EVAL-011 — Pre-Execution Integration Correction

**AUTONOMY:** autonomous  
**ENVIRONMENT:** Claude Web/cloud; GitHub only plus public web if needed to inspect cited primary documentation  
**BUDGET:** ₹0 external spend  
**BRANCH:** `work/eval-011-pre-execution-integration`

## Objective

Perform the **one bounded correction/reconciliation pass** required by:

`coordination/decisions/CONTROLLER-PRE-EXECUTION-INTEGRATION-2026-08-26.md`

This is not another research round. The request architecture, Capability-v2 direction, topology-v3 direction and scientific question roster have already received Controller disposition.

Your job is to make the Eval execution package internally consistent and stageable before the Repository Governor reviews it.

## Read first

1. `PROJECT-MEMORY.md`
2. `shared/COMMUNICATION-STANDARD.md`
3. `coordination/CONTROL-STATE.md`
4. `coordination/decisions/CONTROLLER-PRE-EXECUTION-INTEGRATION-2026-08-26.md`
5. CANON-010 branch `work/canon-010-request-freeze`, especially:
   - `canon/experiments/pre-execution-freeze/MEDIA-REQUEST-GRAMMAR-v1.yaml`
   - `canon/experiments/pre-execution-freeze/REQUEST-COVERAGE-EXTENSION.jsonl`
   - `canon/experiments/pre-execution-freeze/CANON-010-CONTROLLER-BRIEF.md`
6. EVAL-009 branch `work/eval-009-measurement-freeze`, all files under `eval/pre-execution-freeze/`
7. RES-004 branch `work/res-004-production-readiness`, especially controlled-pack and CpAO requirements
8. EVAL-010 branch `work/eval-010-route-verification`, especially verified model universe, controls, price table and Controller brief

## Fixed Controller decisions — do not reopen

- Requested operation vocabulary is exactly:
  `generate | edit | animate | restore | extend | compose | variants`.
- Requested operation is customer intent; workflow mode is Planner/production choice.
- Capability Contract v2 freeze target is **44 total = 43 active + 1 dormant repairability**.
- Dependency state `blocked_by_prerequisite_failure` remains unsatisfied at outcome level.
- Scientific roster remains **12 core question slots + 2 reserve slots**; sourcing cannot add/delete scientific questions.
- Outcome topology v3 and whole-outcome CpAO direction are accepted.
- V1 36-capability contract and V1 100-item bank remain byte-identical historical baselines.
- No universal complexity score.
- No paid execution is authorised.

## Correction package

### E11-A — Condition-contract consistency

The EVAL-009 contract declares 13 condition families but parts of its own package still say 12.

Correct **all** machine-readable/prose/validator/forecast references so they agree on the actual intended architecture.

If each family had two levels, the naive full product is **8,192**, not 4,096.

Do not remove a condition family merely to recover the old count.

Consume CANON-010's exact requested-operation vocabulary unchanged.

Add/strengthen validator coverage so a future count mismatch fails mechanically.

### E11-B — CpAO / VID-05 staging correction

The scientific question `VID-05` is retained, but Layers 1–3 cannot claim customer-outcome CpAO when Layer 4 has no accepted customer outcomes.

Make the distinction explicit:
- Layers 1–3 may measure trial/API cost, reliability, latency/errors/refusals and cost per benchmark pass where defined;
- they do not produce customer-outcome CpAO;
- the premium-vs-fast **CpAO conclusion** executes only in the end-to-end outcome stage.

Use CANON-010's accepted request pool as the source from which end-to-end Layer-4 slots may later be instantiated. Eval must not invent customer briefs.

Do not silently fill Layer 4 with arbitrary prompts. If exact Layer-4 selection requires Controller choice, produce a deterministic candidate-selection rule and leave the final ids for Controller integration.

Update/recompute every affected call count and forecast.

### E11-C — Reproducibility semantics

Consume EVAL-010's route evidence:
- some routes expose a seed;
- some routes do not;
- wrapper/direct controls can differ.

Therefore:
- record seed availability/seed policy as a production condition;
- distinguish held-seed repeatability from unseeded inherent-variance measurement;
- do not apply one universal repeat-consistency threshold across unlike route semantics;
- keep repeats distinct from retries.

Existing provisional thresholds remain unqualified unless independently justified by already-approved evidence. Do not invent a new threshold in this task.

### E11-D — Scientific-slot supply reconciliation

For each 12 core + 2 reserve scientific slot:
- preserve the scientific question and admission rationale;
- map the EVAL-009 named candidate to EVAL-010 evidence status;
- record exact verified identity/version/route where EVAL-010 actually supports it;
- record unresolved where not supported;
- list evidence-backed equivalent candidate(s) only if they genuinely answer the same slot question;
- never silently substitute a sibling/family version;
- never remove a slot because sourcing is hard.

This is a reconciliation table, not a new model-selection exercise.

### E11-E — Staged execution design

Replace the misleading idea that the entire 494-generation design is automatically the first paid run.

Produce a staged program with exact call-count mechanics where currently knowable:

**Stage Q — evaluator/material qualification**
- what instruments/material must be qualified before each scientific slot can be scored credibly;
- no model-generation spend merely to qualify an evaluator unless the qualification design genuinely requires generated material.

**Stage A — scientific admission/discrimination screen**
- smallest defensible set of probes needed to answer whether a route deserves deeper spend;
- preserve repeat design where reliability matters;
- whole questions may be deferred; do not weaken all questions by halving repeats.

**Stage B — deeper capability + sparse-envelope benchmark**
- atomic + compound + adaptive condition work on survivors;
- show maximum and adaptive expected structure separately; do not invent a pass-rate saving.

**Stage C — end-to-end outcomes / CpAO**
- Canon-authored customer request items only;
- outcome topology v3;
- actual acceptance journey and fully-loaded CpAO;
- `VID-05` cost-knee conclusion lives here.

For every stage state:
- purpose;
- eligible scientific slots;
- required evaluator/material prerequisites;
- generation/transform attempt count formula and exact count if resolvable now;
- evaluator-call count formula/count;
- human-review units;
- what result promotes/stops/deepens a slot;
- what remains unpriced.

The output must make clear which counts are:
- design ceilings;
- first-tranche candidate counts;
- adaptive/conditional future counts.

### E11-F — Resources reconciliation

Do not edit Resources-owned files.

Produce an Eval-facing material requirement delta against RES-004:
- which pack structures are needed in Stage Q/A/B/C;
- which full-pack provisional counts can wait;
- where same-category decoys are mandatory;
- where protected qualification vs empirical holdout needs disjoint identities/speakers/campaign groups;
- which deterministic/known-by-construction materials Eval can build without a fifth Resources pack.

Do not turn RES-004's 173-hour full acquisition estimate into a first-run prerequisite.

### E11-G — Budget readiness output

Produce a price-ready forecast that can consume EVAL-010 verified price records without guessing missing prices.

Rules:
- preserve source billing units;
- distinguish nominal benchmark cost from cash outlay after credits;
- missing price remains null and blocks a total for the affected stage/slot;
- do not infer `Frontier Clouds` identity;
- Google Nano Banana 2 wording must mean per **1K-resolution image**, not per thousand images;
- a route-specific price must not be generalized across sibling APIs/routes.

No budget is approved in this task.

## Deliverables

Create under `eval/pre-execution-integration/`:
- `CONDITION-CONTRACT-CORRECTION.md`
- `SCIENTIFIC-SLOT-SUPPLY-RECONCILIATION.yaml`
- `SCIENTIFIC-SLOT-SUPPLY-RECONCILIATION.md`
- `STAGED-EXECUTION-PLAN.yaml`
- `STAGED-EXECUTION-PLAN.md`
- `EVALUATOR-AND-MATERIAL-STAGE-MAP.yaml`
- `PRICE-READY-STAGED-FORECAST.yaml`
- validators + negative fixtures
- `EVAL-011-CONTROLLER-BRIEF.md`

Also make the minimum necessary corrections to the EVAL-009 proposal files **on this EVAL-011 branch** so the corrected package is internally consistent. Preserve the original EVAL-009 branch as historical worker output; do not rewrite its git history.

## Mechanical gates

At minimum fail if:
- any live corrected file says 12 condition families while the schema declares 13;
- 13 binary families are described as 4,096 rather than 8,192;
- requested-operation vocabulary differs from CANON-010;
- workflow mode is populated from requested operation or vice versa;
- Layers 1–3 claim customer-outcome CpAO;
- `VID-05` claims CpAO before end-to-end outcomes;
- seeded and unseeded repeat semantics are silently pooled as identical;
- sourcing changes scientific-slot admission;
- a sibling/family model is silently substituted;
- missing prices are guessed or a partial stage is totalled;
- RES-004 provisional full-pack hours are treated as mandatory first-tranche spend;
- V1 historical artifacts change;
- any API/model/evaluator call, acquisition, account, payment or Registry write occurs.

## Restrictions

₹0 spend. No model/API/evaluator calls. No acquisition. No accounts or terms acceptance. No Registry population. No Production IR/Planner implementation. No broad new research. No merge.

Commit and push to `work/eval-011-pre-execution-integration`.

Return only after the whole correction package is complete, with:
- status;
- commit SHA;
- corrected condition-family count;
- staged Q/A/B/C counts;
- scientific slots resolved/unresolved by supply evidence;
- evaluator/material blockers by stage;
- price-complete vs price-blocked stages;
- any remaining Controller decision that prevents Governor review.
