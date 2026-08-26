# Controller State

**Updated:** 26 Aug 2026 — four pre-execution programs reviewed; one bounded Eval integration correction active.

**Read `PROJECT-MEMORY.md` first.** Where older task/handoff wording conflicts with current Controller decisions and this file, the latest Controller decision governs until the next Repository Governor refresh.

## Global posture

Broad discovery/research is closed for now.

Merged research/state already on `main`:
- CANON-009 request-space research;
- EVAL-007 capability/workflow research;
- RES-003 evidence/topology research;
- GOV-003 repository-coherence review.

Four final pre-execution programs returned unmerged:
- CANON-010 @ `3cf29790dfc0ae34a9ded2a42ad5b8774fb36d58`;
- EVAL-009 @ `718ba01927d11632c4957096f2d0144d8095c488`;
- RES-004 @ `2dc4796ff0916172855e29d0fc02a17a9d9a4201`;
- EVAL-010 @ `8a8fc0915bbf8acfe193cef854e9e0fbe64239dc`.

Authoritative joint disposition:
- `coordination/decisions/CONTROLLER-PRE-EXECUTION-INTEGRATION-2026-08-26.md`

The architecture is accepted far enough to stop broad design work. One bounded Eval reconciliation is required before Governor review.

## Accepted request-side freeze target

- requested operation vocabulary: `generate | edit | animate | restore | extend | compose | variants`;
- requested operation is customer intent and is distinct from workflow mode;
- supplied asset does not imply edit;
- `restore` remains distinct from edit;
- deliverable-set/cardinality/acceptance-basis semantics live on Normalized Request;
- camera motion and subject motion remain separate;
- customer-attributed requirements require explicit provenance/evidence;
- CANON-010's 11-item request extension is accepted as structural coverage; original 30 remain byte-identical authored probes, not demand evidence;
- multi-turn remains representation-only/deferred.

## Accepted measurement-side freeze target

Capability Contract v2 target:
- **44 total = 43 active + 1 dormant repairability**;
- V1 36-capability contract and V1 100-item bank remain immutable historical baselines.

Accepted v2 semantics include:
- 2D vs depth spatial relation split;
- spoken script correctness vs pronunciation/intelligibility;
- person identity vs wardrobe invariant;
- reproducibility vs repairability;
- camera/framing fidelity;
- sequence/state continuity;
- technical visual integrity;
- voice identity consistency;
- dependency state `blocked_by_prerequisite_failure` remains unsatisfied at outcome level;
- style-reference fidelity remains reference-conditioning + condition;
- cross-asset identity remains observation scope of identity;
- campaign/set consistency is outcome-level, not another per-asset capability.

Production Requirement Profile remains provider/model/routing free.

Condition architecture has **13 families**. No synthetic complexity score. Requested operation and workflow mode are separate condition/provenance axes.

Scientific hypothesis roster target:
- **12 core question slots + 2 reserve slots**;
- slots are scientific questions, not provider commitments;
- sourcing cannot silently add/delete questions.

## Accepted Resources freeze target

Forward topology:

`job -> outcome -> sequence_or_asset_set -> production_unit -> production_step -> attempt -> artifact`

- one provider/API/transform call = one trial;
- local deterministic steps do not invent provider attempts;
- artifacts may have ordered multi-parent lineage;
- historical v2.1 is never backfilled with invented v3 context;
- failed/refused/timed-out attempts remain evidence.

CpAO:
- API/tool CpAO is diagnostic;
- fully-loaded whole-outcome CpAO is primary;
- include outcome-specific required production/repair/review/acceptance labour;
- exclude one-time R&D, benchmark construction, pack acquisition and evaluator qualification from per-customer CpAO unless a later accounting policy explicitly amortises them;
- rejected revisions in the same journey count; a material customer scope change cuts the journey;
- shared upstream costs count once.

Four controlled-pack families survive. Structural requirements are accepted, but provisional entity totals and RES-004's 173-hour full-pack estimate are **not** first-run prerequisites or approved budgets.

CC-BY-NC remains unauthorised for commercial empirical material absent explicit disposition. Request-corpus/UGC identity images require positive rights/consent before protected benchmark use.

## EVAL-010 supply state

EVAL-010 is accepted as **partial supply evidence**:
- 2/26 candidate rows currently have fully verified identity + route + billing unit + price under its strict evidence rule;
- that does NOT mean only two models are accessible;
- 19 further rows have substantial provider-authorised route/identity evidence but incomplete verified pricing;
- fal/direct wrapper equivalence cannot be assumed;
- the reported ~99% Hindi/Bengali OpenAI accuracy claim remains unverified and non-load-bearing;
- seeded and unseeded routes require different reproducibility interpretation;
- `Frontier Clouds` service identity remains unresolved in repository evidence.

Controller independently clarified the Google shorthand: `$0.067 per 1K image` means approximately $0.067 per **generated 1K-resolution image**, not per thousand images. Route-specific billing units must remain route-specific.

## Active assignment — EVAL-011 only

Task:
- `eval/tasks/EVAL-011-PRE-EXECUTION-INTEGRATION-CORRECTION.md`

Branch:
- `work/eval-011-pre-execution-integration`

Purpose:
- reconcile EVAL-009's 13-vs-12 condition count inconsistency;
- consume CANON-010's exact request vocabulary;
- stage the `VID-05` CpAO question to the end-to-end outcome layer;
- reconcile seeded/unseeded reproducibility semantics;
- map scientific slots to EVAL-010 supply evidence without changing admission;
- replace one monolithic first-run interpretation with staged Q/A/B/C execution counts;
- separate minimum stage materials from RES-004's full-pack acquisition plan;
- produce a price-ready staged forecast without guessing missing prices.

This is a bounded correction, not another research round.

## Paid execution remains blocked

Not authorised:
- historical E7/E8;
- EVAL-006 (PAUSED — DO NOT EXECUTE);
- 494 generations as a paid run;
- 5,515 evaluator calls as a paid run;
- 188 human review units as a paid run;
- 173 pack-acquisition hours as a required budget;
- any provider/evaluator/model call;
- Registry population;
- acquisition/account funding/terms acceptance;
- Production IR/Planner implementation.

## Next gate

After EVAL-011 returns, one Repository Governor review must inspect CANON-010, corrected Eval, RES-004, EVAL-010 and the Controller integration decision jointly.

Only after a coherence-safe review may the Controller merge the accepted branches and propose an explicitly priced paid tranche for user approval.
