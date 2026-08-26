# RES-004 — Production Evidence & Persistence Readiness

**AUTONOMY:** autonomous  
**ENVIRONMENT:** Claude Web/cloud; GitHub + public web as needed  
**BUDGET:** ₹0 external spend  
**BRANCH:** `work/res-004-production-readiness`

## Objective

Turn RES-003 research plus the Controller integration decision into an **implementation-ready evidence/persistence package** that can safely receive the first paid model runs later.

This task owns production lineage, archive/persistence semantics, controlled-pack requirements, rights/access gates and whole-outcome cost accounting. It does not own creative truth, evaluator thresholds or model selection.

## Read first

1. `PROJECT-MEMORY.md`
2. `coordination/CONTROL-STATE.md`
3. `coordination/decisions/CONTROLLER-MACRO-RESEARCH-INTEGRATION-2026-08-26.md`
4. `coordination/decisions/CONTROLLER-FINAL-PRE-EXECUTION-FREEZE-2026-08-26.md`
5. `coordination/plans/2026-08-26-FINAL-PRE-EXECUTION-FREEZE-PROGRAM.md`
6. RES-003 research under `resources/research/pre-e7-macro/`
7. authoritative v2.1 persistence/archive artifacts and validators
8. current four controlled-pack designs/requirements

## Work packages

### R4-A — Outcome / production topology v3

Produce an implementation-ready schema for:

`job -> outcome -> sequence_or_asset_set -> production_unit -> production_step -> attempt -> artifact`

Required semantics:
- one customer request may produce multiple independently acceptable outcomes;
- sequence_or_asset_set may be ordered video sequence or grouped campaign/variant set;
- production units include shot/layer/end-card/audio/static/etc.;
- production steps include provider generation, transform, deterministic composition/edit/assembly and repair;
- one provider/API/transform call = one trial/attempt;
- deterministic local steps may produce artifacts without inventing provider attempts;
- artifacts may have ordered multi-parent lineage;
- relation/config needed to reconstruct a derived/composed artifact must be recoverable.

### R4-B — v2.1 compatibility

Historical v2.1 archives remain historical truth.

Define exact compatibility/migration semantics:
- no invented outcome/job context;
- no historical trial acceptance promoted to customer-outcome acceptance;
- explicit `not_recorded_pre_v3`/equivalent null state where information did not exist;
- new readers can ingest v2.1 without mutating source records;
- new v3 records preserve trial-level evidence.

### R4-C — Lineage and validator suite

Create fail-closed validators/fixtures for at minimum:
- unknown parent;
- cycle;
- duplicate/ambiguous parent ordering where ordering matters;
- child claiming a provider trial that never existed;
- deterministic local child manufacturing an attempt;
- accepted outcome without final artifact;
- composition/assembly with missing transform configuration;
- historical backfill that invents v3 context.

### R4-D — Whole-outcome CpAO

Implement the accounting contract for:
- successful attempts;
- failed/refused/timed-out attempts;
- retries and repair attempts;
- paid evaluator calls;
- paid transforms;
- material local compute;
- required human review/production time;
- rejected revisions belonging to the same production journey.

Report separately:
- API/tool CpAO;
- fully-loaded CpAO.

Fully-loaded CpAO is primary business metric.

Shared upstream artifacts/costs must be counted once according to an explicit attribution rule. Customer material scope change must open a new outcome/revision boundary rather than retroactively charging unrelated work.

Provide positive and negative recomputation fixtures.

### R4-E — Controlled-pack readiness

Keep the existing four-pack architecture unless a concrete active consumer makes it impossible.

For each pack, produce the **minimum evidence requirements** needed by the accepted architecture direction:
- product reference pack;
- person reference pack;
- AV clean pack;
- commercial/campaign pack.

Specify:
- required entities/identities/categories;
- views/framing/reference quality diversity;
- same-category decoys where needed;
- sequence/campaign grouping;
- duration/speech/language coverage including relevant Hindi/Hinglish/brand-name material;
- request-lineage and media-lineage metadata;
- protected qualification/holdout roles;
- minimum viable quantity and what assumption the number rests on.

If an exact count genuinely depends on EVAL-009 final capability/benchmark choices, provide a deterministic sizing rule plus the smallest safe provisional count. Do not invent statistical precision.

### R4-F — Rights / acquisition / human-effort plan

Research legitimate acquisition/capture routes but do not acquire.

For every required material class state:
- preferred route;
- rights/consent basis that must be established;
- whether user-generated/request-corpus images are disallowed or unresolved;
- protected-set/leakage implications;
- estimated human capture/review/annotation effort as a budget input.

CC-BY-NC material is not authorised as commercial-project empirical material without explicit Controller/legal disposition.

### R4-G — Execution-readiness brief

Return exactly what must exist before the first paid attempt can be persisted without schema debt or evidence leakage.

## Deliverables

Under `resources/pre-execution-freeze/` create at minimum:
- `OUTCOME-PRODUCTION-TOPOLOGY-v3.yaml`
- `V21-V3-COMPATIBILITY.md`
- `LINEAGE-CONTRACT-v3.md`
- `CPAO-CONTRACT-v3.md`
- `CONTROLLED-PACK-REQUIREMENTS-v2.yaml`
- `CONTROLLED-PACK-REQUIREMENTS-v2.md`
- `RIGHTS-ACQUISITION-PLAN.md`
- `HUMAN-EFFORT-BUDGET-INPUTS.yaml`
- validators + positive/negative fixtures
- `RES-004-CONTROLLER-BRIEF.md`

## Mechanical gates

Fail if:
- one provider/API/transform call no longer maps to one trial;
- a local deterministic step invents a provider attempt;
- historical v2.1 evidence is silently promoted/backfilled;
- lineage permits unknown parents or cycles;
- cost can be double-counted through reuse;
- accepted outcome can exist with no final artifact;
- request-lineage is confused with byte/media lineage;
- a fifth pack is created without a concrete active consumer;
- pack counts claim statistical confidence not established by the design;
- acquisition, login, payment or terms acceptance occurs.

## Restrictions

No acquisition/download program beyond ordinary public-document research. No paid calls. No creative labels. No Eval thresholds. No provider/model selection. No merge.

Commit and push the branch. Return the Controller brief and commit SHA only after the whole program is complete.
