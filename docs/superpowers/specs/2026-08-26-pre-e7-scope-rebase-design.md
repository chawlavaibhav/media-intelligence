# Pre-E7 Scope Rebase — Design

**Date:** 26 Aug 2026  
**Owner:** Controller  
**Status:** APPROVED FOR IMPLEMENTATION  
**Purpose:** correct Eval's pre-paid-run scope so empirical evidence remains interpretable when customer outcomes span multiple shots, multiple model calls, transforms, repairs and omitted production decisions.

## 1. Problem discovered

The accepted V1 architecture correctly defines 36 capability dimensions and a generate-once / measure-many benchmark. However, discussion of customer video duration exposed a broader gap: the capability vocabulary says **what can fail**, while the Registry has not frozen the **conditions under which that capability was measured**.

A score such as `product_stability_in_clip = 0.9` is unsafe without context such as duration, shot count, workflow mode, reference quality, motion complexity and constraint load.

A second gap is that the current empirical persistence model centres on attempts/artifacts, while the customer buys an **accepted outcome**. A 45-second ad can be one customer outcome assembled from multiple shots, API calls, transforms, deterministic overlays and repairs.

This rebase fixes those interfaces before any paid current-model benchmark. It does not discard the accepted V1 work.

## 2. Product scope after rebase

The product is an API-native **commercial media production intelligence layer** for Indian businesses, optimising **Cost per Accepted Outcome**.

Initial empirical emphasis remains:

- static commercial creatives and product/brand imagery;
- commercial video outcomes, including multi-shot/composed outcomes;
- English, Hindi and Hinglish;
- Latin and Devanagari;
- products, people and reference-conditioned identity;
- edits, VO, one visible speaker and two visible speakers;
- single assets and small campaign sets;
- multi-stage and multi-model production workflows.

A model's native duration is a production constraint, **not** a customer-product limit. V1 should gather strong evidence for native/short-form units and a bounded sample of approximately 30–60 second composed outcomes. Longer outcomes remain architecturally representable but are outside the first empirical claim envelope until tested.

## 3. Four interfaces to freeze before E7

### 3.1 Production Requirement Profile

A derived, model-agnostic view compiled from Normalized Request + Creative IR.

It records only what the production system must satisfy, not how it will be made.

Each requirement records:

- requirement id;
- requirement type: capability | acceptance constraint | delivery condition | planner decision;
- source operation: preserve | derive | decide | delegate | ask | flag;
- strength: hard | soft | free;
- resolved value;
- applicable entity/asset/sequence scope;
- acceptance consequence if violated.

It must remain separate from Production IR. It is the query interface between Creative IR and Eval evidence.

### 3.2 Condition / Envelope Contract

Registry evidence must carry a frozen set of condition families. Do not collapse them into one synthetic complexity score.

Required condition families:

1. **delivery** — modality, duration, aspect ratio, resolution, platform;
2. **content load** — people count, product/object count, text load, speaker count;
3. **identity/reference load** — reference type, count, quality class, identity count;
4. **physical complexity** — action complexity, human-object/human-human interaction, clutter;
5. **cinematic complexity** — camera motion, framing requirement, shot count;
6. **constraint load** — hard-constraint count, modality-crossing constraints, exactness requirements;
7. **workflow mode** — t2i/t2v/i2v/edit/extension/ref-conditioned/native-av/lipsync/tts/composite;
8. **sequence structure** — single asset, single shot, extended clip, multi-shot sequence, campaign/asset set;
9. **language/audio** — spoken language, on-screen language/script, exact spoken script required, speaker topology;
10. **input quality** — clean/controlled vs degraded/noisy/low-resolution customer references;
11. **decision provenance** — customer-specified, derived, brand/legal policy, planner-decided, delegated;
12. **scale** — one output, variant set, campaign set.

Every empirical Registry row must state applicable condition values or explicit `not_applicable` / `not_recorded_pre_rebase` where historical evidence cannot supply them. New paid evidence may not silently omit applicable required conditions.

### 3.3 Outcome / Production Topology Contract

The persistence and later Production IR must support:

`job -> outcome -> sequence_or_asset_set -> production_unit -> production_step -> attempt -> artifact`

Where:

- **job** = customer request / production engagement;
- **outcome** = one accept/reject-able deliverable from the customer's point of view;
- **sequence_or_asset_set** = ordered video sequence or related campaign set;
- **production_unit** = shot, layer, end-card, audio segment, static asset, or other independently producible unit;
- **production_step** = generation, transform, deterministic compose/edit, assembly, repair;
- **attempt** = one provider/API/transform call, preserving the accepted one-call-one-trial rule;
- **artifact** = bytes produced by a step.

A final artifact may have **multiple parents**. Composition lineage must therefore be a graph, not a single-parent chain.

CpAO is computed at **outcome level**: total cost of all attempts/transforms/repairs that contributed to the accepted outcome, divided by accepted outcomes. Trial-level cost remains available for diagnosis.

### 3.4 Capability Contract v2 Audit

The current 36 are a strong starting point, not to be casually replaced. Audit them against all 30 Canon customer briefs and the new condition/outcome model.

For every meaningful customer requirement, classify it as:

- existing capability;
- condition;
- planner decision;
- acceptance constraint;
- operational variable;
- genuine missing capability.

Candidate missing-capability questions to test rather than assume:

- exact spoken-content/script fidelity;
- camera/framing instruction fidelity;
- cross-shot / cross-asset identity consistency;
- sequence/state continuity beyond screen-direction continuity;
- technical visual integrity (flicker, transient corruption, warping, sudden softness);
- pronunciation/intelligibility/voice consistency where not already fully covered;
- style-reference fidelity where current `reference_conditioning` is insufficient.

No new capability count is frozen in advance. Add only gaps that cannot be represented honestly by an existing capability + condition.

## 4. Benchmark architecture after rebase

Do **not** enumerate the full combinatorial space.

Use five layers:

1. **Evaluator qualification** — can the checker be trusted?
2. **Primitive capability baseline** — current atomic/compound bank, minimally revised only where v2 capability definitions require it.
3. **Production-envelope sweeps** — vary one important condition at a time to find failure boundaries (for example duration or reference quality).
4. **Workflow-topology comparisons** — compare materially different ways to make the same outcome, e.g. extension vs independent shots + references + edit.
5. **Customer-outcome benchmark** — selected Canon briefs produced end-to-end, including Planner-selected values where the customer omitted production decisions.

The existing E7=204 and E8=520 generation counts are no longer authoritative budgets. They remain historical calculations for the pre-rebase design and must be recalculated after the interfaces above are frozen.

## 5. What survives unchanged unless the audit finds a concrete conflict

- 30-brief Canon bank;
- generate-once / measure-many principle;
- one call = one trial;
- repeat vs retry separation;
- six evaluator-family architecture;
- atomic + compound benchmark strategy;
- existing 100-item bank as the baseline starting point;
- Resources rights/integrity/lineage principles;
- immutable attempt/artifact/measurement/cost preservation;
- Registry principle: evidence, never routing scores;
- separation of Creative IR from Production IR.

## 6. E2 amendment

E2 must inventory **production operations**, not only model identity and price.

For each admitted endpoint/workflow capture, where officially exposed:

- exact model/API/version and access path;
- billing unit and price;
- native duration range;
- t2v/i2v/edit/extension capabilities;
- first/last-frame controls;
- reference asset support, count and type;
- mask/edit controls;
- character/product/reference conditioning;
- native audio availability;
- aspect ratio and resolution support;
- camera controls;
- seed/reproducibility support;
- version pinning;
- concurrency/rate constraints relevant to production;
- aggregator vs direct-access distinction.

One model used through materially different production modes creates different workflow evidence.

## 7. Stream responsibilities

### Canon

Audit the 30 customer briefs from customer intent outward. Do not invent production methods or model capabilities. Produce a requirement-classification ledger showing whether every meaningful requirement maps to capability / condition / planner decision / acceptance constraint / operational variable / gap.

### Eval

Own the Condition/Envelope Contract, Production Requirement Profile interface, capability-v2 audit/refreeze, E2 production-operation amendment, Registry semantic changes and revised benchmark design/budget.

### Resources

Own persistence changes required for outcome-level lineage and cost: job/outcome/production-unit/step identities, multi-parent artifact lineage, whole-outcome cost provenance, and any resource-pack delta caused by the rebase. Do not define measurement semantics.

## 8. Hard gates

Until the Pre-E7 rebase is integrated:

- **E7 is BLOCKED**;
- **E8 is BLOCKED**;
- no paid current-model generation/checker benchmarking;
- no empirical current-model Registry population;
- no implementation of a Production Planner;
- no expansion into speculative long-form/movie/VFX domains.

Evaluator qualification work that does not depend on the changed interfaces may continue only if the Controller explicitly assigns it.

## 9. Completion criteria

The rebase is complete only when:

1. all 30 Canon briefs have a complete requirement classification with no unexplained fall-through;
2. Eval freezes the condition taxonomy and Capability Contract v2;
3. Production Requirement Profile can represent every audited brief without choosing a provider/model;
4. Resources can represent a multi-step, multi-parent accepted outcome and recompute whole-outcome cost;
5. E2 workflow records expose the production-operation fields needed by the new topology;
6. the benchmark is revised without combinatorial explosion and has a fresh generation/evaluator/human-cost forecast;
7. Controller reconciles the three streams and explicitly re-authorises E7.
