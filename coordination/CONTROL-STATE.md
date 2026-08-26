# Controller State

**Updated:** 26 Aug 2026 by Controller after Pre-E7 scope rebase.

**Read `PROJECT-MEMORY.md` first.** Where older freeze/task wording conflicts with this newer Controller state, this file and the underlying decision/task artifacts govern until the Governor refreshes memory.

## Global posture — Pre-E7 rebase in force

The Canon / Eval / Resources V1 overnight architecture was accepted and merged. A subsequent Controller zoom-out identified a pre-paid-run scope gap: Eval defined **what capabilities can fail**, but had not frozen the **production conditions under which capability evidence is valid**, and the persistence model did not yet represent one customer outcome assembled from many production units/calls/transforms/repairs.

Authoritative rebase artifacts:

- `coordination/decisions/CONTROLLER-PRE-E7-SCOPE-REBASE-2026-08-26.md`
- `docs/superpowers/specs/2026-08-26-pre-e7-scope-rebase-design.md`
- `docs/superpowers/plans/2026-08-26-pre-e7-scope-rebase.md`
- `canon/tasks/CANON-PRE-E7-SCOPE-AUDIT.md`
- `eval/tasks/EVAL-PRE-E7-SCOPE-REBASE.md`
- `resources/tasks/RESOURCES-PRE-E7-SCOPE-REBASE.md`

## Immediate gates

- **E7 paid admission benchmark: BLOCKED.**
- **E8 deep qualification: BLOCKED.**
- Historical E7=204 and E8=520 generation counts remain pre-rebase calculations only; they are not authorised budgets.
- No paid current-model generation/checker/evaluator calls are authorised.
- No empirical current-model Capability Registry entries may be written.
- `EVAL-006` remains **PAUSED — DO NOT EXECUTE**.
- Production Planner / Production IR implementation remains out of scope during this rebase.

## Product / architecture state

The product is an API-native commercial-media production intelligence layer optimising **Cost per Accepted Outcome**.

Stable separation remains:

`Normalized Request -> Creative IR -> Production Requirement Profile -> future Production IR -> execution/evaluation/repair`

- Creative IR says what should exist and preserves/derives/decides/asks/flags customer intent.
- **Production Requirement Profile** will be a model-agnostic compiled view of what production must satisfy.
- Eval Registry stores empirical workflow evidence; it does not route.
- Production IR / Planner will later choose how to make the outcome using Canon + Registry evidence.

A model's native duration is a production constraint, not a customer-product limit. Customer outcomes may be multi-shot, multi-step and multi-model.

## Four interfaces being refrozen

Before E7, the project must freeze:

1. **Production Requirement Profile** — capability/acceptance/delivery/planner requirements derived from customer intent without provider choices.
2. **Condition / Envelope Contract** — delivery, content load, reference load, physical/cinematic complexity, constraint load, workflow mode, sequence structure, language/audio, input quality, decision provenance and scale.
3. **Outcome / Production Topology Contract** — `job -> outcome -> sequence_or_asset_set -> production_unit -> production_step -> attempt -> artifact`, including multi-parent composition lineage and outcome-level CpAO.
4. **Capability Contract v2** — current 36 audited against all 30 Canon customer briefs; add a capability only where existing capability + condition is genuinely insufficient.

## What remains accepted from V1

- live accepted Canon: 19 sources;
- Canon 30-commercial-brief bank;
- corrected Canon value-gate package;
- 36-capability V1 contract as the audit baseline;
- six evaluator-family architecture;
- 100-base-item atomic/compound bank as the benchmark baseline;
- generate-once / measure-many;
- one provider/API/transform call = one trial;
- repeat vs retry separation;
- Resources V2.1 attempt/artifact/measurement/acceptance/cost persistence;
- immutable failed/refused-attempt evidence;
- Registry stores evidence, not routing scores.

The 36 capabilities are temporarily open only for the bounded Pre-E7 audit. They are not discarded. The 100-item bank is not to be wholesale rebuilt without a concrete capability-v2 or envelope reason.

## Stream assignments

### Canon

Execute `canon/tasks/CANON-PRE-E7-SCOPE-AUDIT.md`.

Audit all 30 unchanged customer briefs and classify every meaningful requirement as:

`existing_capability | condition | planner_decision | acceptance_constraint | operational_variable | genuine_gap`.

Canon must not choose models/workflows or author Production IR.

### Eval

Execute `eval/tasks/EVAL-PRE-E7-SCOPE-REBASE.md`.

Own Production Requirement Profile semantics, Condition/Envelope Contract, capability-v2 refreeze, Registry condition semantics, E2 production-operation fields, revised sparse benchmark and fresh cost forecast.

### Resources

Execute `resources/tasks/RESOURCES-PRE-E7-SCOPE-REBASE.md`.

Own whole-outcome persistence/lineage/CpAO, multi-parent artifact composition and any justified resource-pack delta. Preserve one-call-one-trial and do not define Eval measurement semantics.

## Benchmark posture after rebase

Do not test the cartesian product of all conditions.

Target evidence layers:

1. evaluator qualification;
2. primitive atomic/compound baseline;
3. sparse production-envelope sweeps to locate failure boundaries;
4. workflow-topology comparisons for equivalent outcomes;
5. end-to-end customer-outcome benchmark using Canon briefs.

## Existing blockers still true

- no subjective/perceptual evaluator family is yet qualified;
- no current generator/workflow is benchmarked;
- Capability Registry has 0 empirical current-model entries;
- E2 current official model/API/access/pricing inventory is incomplete;
- controlled product/person/AV/commercial packs are not yet acquired;
- Canon's real value gate remains unrun and needs fresh Canon-naive controls + two independent reviewers;
- raw 5.70 GB Resources corpus was not revalidated in the cloud; BSTD 351-vs-364 discrepancy and GOV-001 R3 remain open.

## Controller integration gate

E7 may be re-authorised only after Controller verifies:

1. all 30 Canon briefs have no unexplained requirement fall-through;
2. Eval freezes the Production Requirement Profile, condition taxonomy and Capability Contract v2;
3. Resources can persist a multi-step, multi-parent accepted outcome and recompute whole-outcome CpAO;
4. the revised benchmark remains sparse/adaptive rather than combinatorial;
5. E2 contains a current official workflow roster with production-operation features and complete prices for the proposed run;
6. a fresh generation/evaluator/human-cost forecast is reviewed and explicitly approved.

This is a scope-correction milestone before empirical spend, not evidence about any current model's quality.
