# EVAL-V1-CORRECTION-PASS

**Status:** AUTHORIZED correction pass on `work/eval-v1-overnight` only.  
**Purpose:** close the Controller review loop on E1–E5 before merge.  
**Spend:** ₹0. No paid generation, checker, evaluator, model qualification, or empirical Registry population is authorized.

## Zoom-out

Eval / Capability Lab is the empirical truth layer about what current workflows can do under specific conditions. It owns capability definitions, evaluator qualification, benchmark design, current workflow measurement, failure-state evidence, cost/latency/reliability measurement and the Capability Registry. It does **not** own Canon truth, persistent resource rights/lineage policy, Production Planner scoring, or routing weights.

The overnight architecture is substantively accepted. Do **not** restart E1–E5. This is a bounded hardening pass on issues found by Controller code review and cross-stream integration.

## Controller decisions you must implement

### E-C1 — Separate instrument readiness from material readiness

`measurability_status` currently conflates at least two questions:
1. can the measurement mechanism/instrument be trusted for this property?
2. do we possess the benchmark/reference material needed to exercise the property under the intended conditions?

Refactor the 36-capability contract to expose at minimum:
- `instrument_readiness`: e.g. `deterministic_ready | qualified | provisional | blocked_pending_qualification | unmeasurable`;
- `benchmark_material_readiness`: e.g. `available | constructed_by_eval | partial | missing | no_external_stimulus_required`.

If useful, add a clearly named production-envelope note, but do not invent a third scalar score.

The contract must be able to say, for example, "deterministic mechanism exists, but realistic production reference material is still missing" without contradiction.

Update generated documentation and validators. Preserve the frozen 36 capability ids.

### E-C2 — Complete E2 only from current official provider evidence

Fill the model/workflow roster and prices only where exact current official documentation can be reached. Preserve the five-lane cap:
- image ≤4
- general video ≤5
- native AV ≤4
- lip-sync/digital-human ≤3
- TTS/external VO ≤3
- total ≤19 endpoint/workflow rows.

For each admitted row require exact model/API id, provider, endpoint/workflow, version-pinning state, region/access condition, billing unit, current official price, source URL and read date.

If the cloud environment still cannot reach an official provider page, leave that row unresolved; do not use memory, reseller blogs or search snippets as evidence. A partially filled roster is preferable to invented certainty.

Re-run the cost calculator only when the required price cells are supported. Human verification cost remains a separate unresolved/explicit line if no rate has been approved.

### E-C3 — Repair the 100-item bank without increasing generation count

The frozen design target is ≥10 distinct base-item opportunities for every critical capability. Current `two_speaker_turn_assignment_and_lip_sync` has 7.

Controller decision: **do not change `multi_shot_branded_ad` modality merely to repair the denominator and do not increase the bank beyond 100.**

Rebalance exactly three atomic items from capabilities that remain comfortably above their breadth target into three additional scientifically valid two-speaker atomic probes.

Invariants after correction:
- exactly 100 base items;
- exactly 40 atomic + 60 compound;
- same 10 compound scenario families ×6;
- all 20 critical capabilities ≥10 distinct base-item opportunities;
- no fake opportunity where two visible speakers/turns cannot exhibit the failure;
- measurement fan-out remains contract-authorised.

Re-run all bank validators and negative controls.

### E-C4 — Separate experimental repeat from production retry

The harness currently uses retry metadata for deliberate reliability repeats. Correct the data model and generation API so these are independent concepts:

- **repeat** = deliberate experimental repeat of a benchmark item/config to estimate reproducibility/reliability. Use `repeat_index` and/or `repeat_of_attempt_id` (or an equivalent explicit representation).
- **retry** = a later attempt caused by a previous failed/rejected attempt in an accepted-outcome/repair chain. Keep separate `retry_of_attempt_id` + `retry_reason`.

Operational metrics must report repeat count and retry count separately. CpAO/acceptance retry chains must include retries, not experimental repeats.

Add negative controls proving a repeat is not counted as retry and a retry is not counted as a repeat.

### E-C5 — Harden Registry row homogeneity fail-closed

`write_registry_row()` must refuse any measurement list that is not one coherent cell.

Before aggregating, validate all scoreable measurements agree on at least:
- capability = requested capability;
- instrument id/version/config hash/qualification state = requested instrument;
- provider;
- model;
- exact version;
- endpoint;
- workflow;
- lane;
- observation unit/compatible declared conditions;
- contract/battery context as applicable.

Also validate the base-item/repeat structure is compatible with `repeats_per_item`; do not trust a caller-supplied repeat count if the underlying attempts disagree.

Add negative controls that deliberately mix two models, two capabilities, two instruments/configs and incompatible conditions and prove every mixed cell is refused.

### E-C6 — Remove any synthetic Registry escape hatch

There must be no `allow_synthetic` or equivalent override that can promote dummy/synthetic measurements into empirical Registry evidence.

Synthetic/dummy measurements may exercise code paths and schemas. They may **never** become empirical Registry rows under any call option.

Delete the override and add a regression test proving there is no writable bypass.

### E-C7 — Emit the canonical Resources storage handoff

Controller integration decision: **Resources owns the persistent attempt/artifact/measurement/acceptance storage contract; Eval owns measurement semantics.**

Adapt the harness to emit a durable handoff compatible with the Resources correction contract. The conceptual records must be:

1. **Attempt** — every provider/transform call, including error/refusal/timeout; individual records must survive even when there is no output artifact.
2. **Artifact** — bytes produced by an attempt; derived frames/assets point to parent and add no independent trial.
3. **Measurement** — many per artifact/trial, using Eval's capability ids, instrument provenance, canonical observation units and absence reasons.
4. **Acceptance** — not decided by Eval in the benchmark harness unless explicitly supplied by a later production experiment; do not invent acceptance.

Canonical observation-unit vocabulary remains:
`frame | shot | shot_pair | sequence | whole_asset | asset_set_over_time`.

Do not invent a second Eval-specific persistent manifest. If Resources' correction branch is not visible in this session, implement against the exact contract above and record any field-name adapter that still needs reconciliation; do not silently choose a competing schema.

### E-C8 — Add explicit uncertainty representation to Registry schema

A Registry cell must be able to state either:
- an uncertainty/confidence interval with method and assumptions, or
- `not_computed` with the reason (e.g. independence not established, sample too small, descriptive-only result).

Do not invent confidence intervals or statistical thresholds. The purpose is to preserve provenance of uncertainty, not manufacture precision.

### E-C9 — Keep thresholds provisional

Do not promote 0.95 repeat consistency, ≤10% false fail, ≤5% refusal, sync/colour/legibility tolerances or any other judgement threshold into empirical truth merely because they are in a spec. Keep each explicitly proposed/provisional unless already supported by accepted evidence.

## Required verification

Freshly run:
- capability-contract validator + negative controls;
- bank build/validate + negative controls;
- harness full self-test after adding the new repeat/retry, mixed-cell and synthetic-bypass regressions;
- Registry schema parse/validation;
- cost calculator self-test;
- any E2 official-evidence checks that the environment can actually perform.

Do not claim a runtime PASS for anything you could not execute.

## Completion criteria

This correction pass is complete only when:

1. 36/36 capabilities separate instrument readiness from material readiness;
2. E2 is either officially evidenced or explicitly unresolved row by row — no remembered identities/prices;
3. bank remains 100 = 40 atomic + 60 compound and all critical capabilities reach ≥10 real opportunities;
4. repeats and retries are structurally separate and tested;
5. Registry aggregation rejects mixed cells;
6. synthetic measurements have no promotion bypass;
7. every failed/refused provider call survives in the persistent handoff as an attempt record;
8. Eval emits/targets the canonical Resources storage contract, not a competing persistent schema;
9. Registry schema carries explicit uncertainty method/status;
10. all applicable validators/negative controls are freshly run;
11. a correction brief is written at `eval/findings/EVAL-V1-CORRECTION-CONTROLLER-BRIEF.md`, clearly separating verified, unresolved and later-gated work.

No paid calls. No empirical Registry entries. No instrument qualification. Do not merge to `main`. Commit and push the correction pass on the existing Eval branch.