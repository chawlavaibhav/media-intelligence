# RESOURCES — Pre-E7 Outcome/Lineage Scope Rebase

**Owner:** Resources  
**Controller decision:** `coordination/decisions/CONTROLLER-PRE-E7-SCOPE-REBASE-2026-08-26.md`  
**Design:** `docs/superpowers/specs/2026-08-26-pre-e7-scope-rebase-design.md`

## Goal

Extend the accepted empirical persistence model so one customer outcome may be composed from many production units, provider calls, deterministic transforms, repairs and intermediate artifacts while preserving the accepted one-call-one-trial rule.

## Read first

- `resources/v1/EMPIRICAL-ARTIFACT-MANIFEST-SCHEMA.yaml`
- `resources/v1/EVAL-STORAGE-HANDOFF.md`
- `eval/registry/SCHEMA-v1-draft.yaml`
- Pre-E7 design above

## Preserve unchanged

- one provider/API/transform call = one trial;
- every failed/refused attempt persists individually;
- attempt and artifact remain separate;
- measurement semantics remain Eval-owned;
- immutable cost ledger provenance;
- repeat vs retry distinction;
- derived frames/crops do not create trials;
- Resources does not decide acceptance or creative quality.

## Deliverables

Create/update under `resources/pre-e7/` or the authoritative V1 schema path:

1. `OUTCOME-PRODUCTION-TOPOLOGY-CONTRACT.yaml`.
2. empirical archive schema revision supporting job/outcome/sequence-or-asset-set/production-unit/production-step identities.
3. multi-parent artifact lineage representation.
4. whole-outcome cost recomputation contract and validator fixtures.
5. compatibility mapping from existing V2.1 attempt/artifact/measurement/acceptance archives.
6. resource-requirements delta showing whether the new sequence/campaign envelope changes the four existing pack requirements.
7. `PRE-E7-RESOURCES-CONTROLLER-BRIEF.md`.

## Required topology

The persistence layer must be able to represent:

`job -> outcome -> sequence_or_asset_set -> production_unit -> production_step -> attempt -> artifact`

Definitions:

- `job`: customer request/engagement;
- `outcome`: one deliverable independently accepted/rejected from the customer's point of view;
- `sequence_or_asset_set`: ordered video sequence or related campaign set;
- `production_unit`: independently producible shot/layer/end-card/audio segment/static asset/etc.;
- `production_step`: generation/transform/deterministic compose/edit/assembly/repair;
- `attempt`: one provider/API/transform call;
- `artifact`: bytes produced by a step.

A valid outcome may have one production unit or many.

## Multi-parent lineage

Current single-parent derivation is insufficient for assembly. Add a relation/edge representation that can express a final artifact assembled from multiple video shots, an audio track and deterministic graphics.

Requirements:

- parent artifact ids are explicit and ordered where order matters;
- relation type is explicit (`derive`, `compose`, `assemble`, `overlay`, `mix`, `repair`, or another frozen machine id justified in the schema);
- exact transformation/assembly parameters or recoverable config location are recorded;
- no parent relationship manufactures a new provider trial unless an actual provider/API/transform call occurred;
- deterministic local processing may create a production step/artifact without a provider attempt, but its compute/cost provenance must be recordable if material.

## Outcome-level acceptance and CpAO

Acceptance must be representable at customer-outcome level separately from any diagnostic trial-level/production-unit acceptance.

Whole-outcome CpAO must be mechanically recomputable from:

- every paid attempt contributing to the outcome, including failed/retried attempts within its production history;
- paid transforms/evaluators where included by the project cost definition;
- deterministic/local production costs when material and recorded;
- repair attempts;
- final outcome acceptance.

Do not double count one cost ledger entry when the same intermediate artifact feeds multiple downstream steps.

## Backward compatibility

Existing V2.1 archives remain valid historical evidence. Do not rewrite them to pretend job/outcome metadata existed.

Provide explicit legacy states such as `not_recorded_pre_rebase` where required. Historical trial-level acceptance must not be silently re-labelled as customer-outcome acceptance.

## Resource-pack delta

Re-run the requirements logic against the re-scoped Eval needs. Prefer extending metadata/usage of the existing four packs rather than creating speculative new packs.

Explicitly check whether sequence/campaign testing changes requirements for:

- number of views per product/person identity;
- cross-shot/cross-asset identity material;
- AV duration/turn coverage;
- commercial video duration/sequence examples;
- protected reserve design.

Any increase must be justified by a concrete Eval/Canon consumer row.

## Validators / negative controls

Must reject at least:

- outcome whose final artifact has an unknown parent;
- composition cycle;
- duplicate cost entry counted twice in whole-outcome CpAO;
- accepted outcome with no final deliverable artifact unless explicitly representing a non-media deliverable allowed by schema;
- child artifact claiming a new trial without an attempt;
- historical trial acceptance silently promoted to outcome acceptance;
- multi-parent composition with no transformation/config provenance.

No acquisition. No creative labels. No Eval thresholds. No merge. Commit and push isolated branch for Controller review.
