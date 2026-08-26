# Controller — Macro Research Integration

**Date:** 26 Aug 2026  
**Status:** APPROVED INTEGRATION DISPOSITION; WORKER BRANCHES STILL REQUIRE GOVERNOR REVIEW BEFORE MERGE  
**Inputs:** `work/canon-009-request-space`, `work/eval-007-capability-workflow`, `work/res-003-evidence-topology`

## 1. Controller conclusion

The three-stream macro reset succeeded. The project now has enough convergent evidence to stop treating the original 30 authored briefs and 36-capability contract as the discovery universe.

The next empirical program will be built around three separate axes:

1. **request operation / customer requirement reality**;
2. **technical capability + production-condition reality**;
3. **evidence independence + whole-outcome production reality**.

No paid benchmark is authorised yet. EVAL-008 model-selection/sourcing research remains a required input to the paid-run roster.

## 2. Canon disposition — ACCEPT WITH SCOPING CAVEAT

CANON-009 is accepted as request-space research, not as a market-share study. Public prompt/edit corpora are interface/population biased and no corpus reviewed represents a full commercial brief population.

### Adopted architectural consequences

1. **Requested operation becomes an explicit customer-intent field upstream of Creative IR.** The Normalized Request must preserve whether the customer asked to `generate`, `edit`, `animate`, `restore`, `extend`, `compose`, or create `variants` (exact machine vocabulary to be frozen in the implementation spec). This must remain distinct from the Planner's chosen workflow mode.
2. **Output cardinality / deliverable-set semantics are required.** The system must represent one deliverable versus a variant/campaign set and the acceptance basis for the set, because this materially changes CpAO.
3. **Camera motion must be separable from subject motion** in video creative requirements.
4. **Multi-turn requests are recognised as a real request shape but are NOT solved in this integration.** The architecture must not preclude append-only request history, but no multi-turn schema is frozen and it does not block the first paid benchmark.
5. Style/prompt folklore is not promoted into durable Creative IR.

### Brief-bank disposition

- Keep the original 30 briefs byte-identical as the frozen **generation-core/value-gate bank**.
- Authorise a separate **request-coverage extension** before end-to-end paid benchmarking, covering at minimum edit, animate-from-supplied-image and variant/campaign-set requests.
- A multi-turn example may be authored for representation testing, but must not be treated as a runnable end-to-end benchmark until request-history semantics are frozen.
- The extended bank is still a controlled probe bank, not demand evidence.

## 3. Eval disposition — ACCEPT WITH CONTROLLER CORRECTIONS

### 3.1 Dependency-aware compound scoring — ADOPT THE GRAPH, CHANGE THE FAILURE STATE

Compound requirements need prerequisite edges. This is accepted.

However, a dependent requirement whose prerequisite failed must **not** be stored as ordinary `not_applicable`, because the requirement still existed in the brief. Example: if the requested product is absent, logo fidelity cannot be inspected, but the logo requirement was not waived.

Freeze a distinct measurement state such as `blocked_by_prerequisite_failure` (exact machine id to be specified). At diagnostic measurement level it means "not directly inspectable because an ancestor requirement failed". At outcome/brief acceptance level it propagates as **unsatisfied**, never as a pass and never as genuinely not applicable.

### 3.2 Capability Contract v2 direction

The current 36 remain the baseline. Controller authorises the following v2 changes for specification work:

**Split/refine existing capabilities**
- separate 2D spatial relationship from depth/3D relationship;
- split spoken word/script correctness from pronunciation/intelligibility;
- split reproducibility from repairability (repair remains dormant until a repair loop exists);
- rename/broaden `anatomy_hands` to human-anatomy integrity while preserving explicit hand failure coverage;
- refine person identity so declared wardrobe/clothing invariants are visible rather than silently mixed with face identity;
- make typography legibility explicitly conditioned on delivery size;
- keep brand-colour tolerance as a declared measurement condition/threshold, not generic categorical-colour evidence.

**Add to v2**
- camera/framing instruction fidelity;
- sequence/state continuity beyond spatial screen direction;
- technical visual integrity (flicker/transient corruption/warping/sudden softness);
- voice identity/consistency across relevant audio assets.

**Require explicit integration treatment, but do not yet add as independent capability**
- style-reference fidelity: resolve boundary with `reference_conditioning` first;
- cross-asset person/product identity: prefer extending existing identity capabilities to asset-set scope unless a distinct failure cannot be represented;
- campaign/variant-set consistency: keep as a required outcome-level/set-level evaluation concept; instrument and final capability boundary to be frozen with the request-coverage extension.

### 3.3 Condition/envelope model

Accept the no-single-complexity-score rule.

Every empirical row must record applicable values for: delivery/duration/size, content/entity load, reference type/count/quality, sequence/shot structure, motion/camera load, constraint/exactness load, language/script/speaker topology, workflow mode, input quality, decision provenance and output scale/set structure.

**Requested operation and workflow mode are distinct:** requested operation comes from the customer; workflow mode is the production route actually used. Both may affect evidence, but provenance must prevent one being substituted for the other.

### 3.4 Benchmark v2 structure

Adopt four evidence layers, now crossed by request-operation coverage:

1. atomic probes;
2. compound scenarios with prerequisite graph;
3. sparse/adaptive condition sweeps;
4. end-to-end accepted outcomes.

The benchmark must cover materially different request operations rather than treating everything as generate-from-nothing. Initial active sweeps remain sparse: duration, entity/load, constraint load, and language/script are good first candidates. Other conditions are recorded even when not actively swept.

No cartesian product is authorised.

## 4. Resources disposition — ACCEPT WITH METRIC DECISIONS

### 4.1 Outcome/production topology

Approve the v3 direction:

`job -> outcome -> sequence_or_asset_set -> production_unit -> production_step`

Production steps may have zero or more provider attempts as appropriate, produce artifacts, and artifacts may have ordered multi-parent lineage. Local deterministic transforms may create artifacts without manufacturing provider trials. One provider/API/transform call = one trial remains unchanged.

Legacy v2.1 archives are not backfilled with invented outcome context.

### 4.2 Whole-outcome CpAO

Primary production CpAO includes all material costs attributable to reaching the accepted outcome:

- successful, failed, refused and retried provider attempts;
- paid transforms and evaluator calls;
- repair attempts;
- material deterministic/local compute costs when recorded;
- **human review/production time when it is required in the operational path**;
- rejected revisions that belong to the same production journey toward the accepted deliverable.

If the customer materially changes the brief, that creates a new outcome/revision boundary rather than charging unrelated future work backward.

For transparency, report at least two views when human/internal costs are available: **API/tool CpAO** and **fully-loaded CpAO**. The primary business metric is fully-loaded CpAO; API/tool-only is diagnostic.

Costs attach to the step/attempt that incurred them and each immutable ledger entry is counted once, even when an artifact is reused downstream.

### 4.3 Protected-set / request-lineage rule

Adopt `request_discovery` as a distinct evidence role and adopt strict request-lineage tracking.

A discovery source and a benchmark descended from the same request pool cannot be presented as independent generalisation evidence. Rephrasing or deriving a taxonomy does not erase lineage.

**Controller choice for the arena lineage:** preserve Arena-T2I-Hard for Eval methodology/benchmark use. Do not use raw LMArena prompt data as a load-bearing request-discovery source for the integrated request grammar. Canon has independent edit/T2I/I2V/T2V sources for discovery.

Unknown request lineage is INDETERMINATE, not independent.

### 4.4 Resource packs

Retain the four-pack architecture; do not create a fifth speculative family. Adopt the direction of the proposed deltas:

- product pack records reference-to-production-step lineage;
- person pack gains sufficient framing/view diversity for cross-asset tests;
- AV pack includes longer continuous speech and commercially relevant Hinglish/brand-name material;
- commercial pack is grouped into campaign families and spans short plus ~20–30s examples.

Exact pack sizes are not reauthorised by this decision; they will be frozen against the integrated Capability Contract v2 and benchmark.

## 5. Rights and source-use posture

- Do not acquire/use CC-BY-NC request or benchmark datasets as project empirical material for the commercial product without explicit legal/Controller disposition.
- Published aggregate findings may be cited as external research evidence with their source and limitations; that is not the same as ingesting the dataset.
- Verify load-bearing licences on the actual distribution page before acquisition.
- User-uploaded reference images from request datasets are not assumed cleared for person/reference benchmarking.

## 6. Independent Controller verification performed

Before this disposition, the Controller independently verified several load-bearing external claims on primary/high-quality surfaces:

- PSR/WACV 2026: 82,976 final real-world PhotoshopRequest posts and 305,806 human-edited images;
- TIP-I2V/ICCV 2025: >1.70M unique user-provided text+image prompts;
- Arena-T2I-Hard: 310 real arena prompts with dependency-aware DAG checklists;
- GenEval2: 800 prompts, `atom_count`, and explicit benchmark-drift motivation;
- VBench-2.0: separate dimensions including Camera Motion, Motion Order Understanding, Human Identity, Human Clothes and Multi-View Consistency.

This verification supports the architectural direction. It does not establish market prevalence for commercial briefs.

## 7. What remains open before paid empirical work

1. EVAL-008: model list first, then sourcing via Frontier Clouds -> fal -> other/direct access.
2. Formal implementation specs for the Normalized Request additions, Capability Contract v2, condition contract and outcome topology v3.
3. Request-coverage brief extension.
4. Evaluator qualification designs/instruments for the newly accepted capability boundaries.
5. Final controlled-pack sizes and legitimate acquisition routes.
6. Fresh paid-run cost forecast after model roster and evaluator fan-out are known.
7. Explicit Controller budget approval.

E7/E8 historical paid programs remain blocked.

## 8. Merge posture

The three worker branches contain valuable research evidence and are recommended for merge **after one bounded Repository Governor integrity review**. Their proposal labels must remain proposals; this Controller record is the authoritative disposition that says which parts are adopted.
