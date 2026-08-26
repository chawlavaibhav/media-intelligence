# Controller Decision — Pre-Execution Freeze Integration

**Date:** 26 Aug 2026  
**Status:** APPROVED WITH ONE BOUNDED EVAL CORRECTION REQUIRED BEFORE GOVERNOR REVIEW  
**Inputs:**
- `work/canon-010-request-freeze` @ `3cf29790dfc0ae34a9ded2a42ad5b8774fb36d58`
- `work/eval-009-measurement-freeze` @ `718ba01927d11632c4957096f2d0144d8095c488`
- `work/res-004-production-readiness` @ `2dc4796ff0916172855e29d0fc02a17a9d9a4201`
- `work/eval-010-route-verification` @ `8a8fc0915bbf8acfe193cef854e9e0fbe64239dc`

No paid model/evaluator work is authorised by this decision.

## 1. Controller conclusion

The final pre-execution tranche succeeded at the architecture level. The project now has a defensible request contract, capability contract direction, production-requirement profile, dependency/condition model, outcome topology, CpAO accounting contract, scientific model-question roster and supply-verification method.

The remaining issue is not another broad research gap. It is one bounded Eval reconciliation before the Repository Governor reviews the package.

The Controller explicitly separates three concepts that workers sometimes collapsed:

1. **the full scientific design** — what we ultimately want to learn;
2. **the first paid execution tranche** — the smallest useful experiment we actually authorise;
3. **the full evidence-pack build** — material needed to exercise every planned evaluator/capability.

A complete design is not automatically a sensible first bill.

## 2. CANON-010 disposition — ACCEPT

### 2.1 Freeze the Media Request Grammar / Normalized Request direction

Adopt the seven-value customer-request operation vocabulary:

`generate | edit | animate | restore | extend | compose | variants`

Rules:
- this is customer intent, upstream of Creative IR;
- it must never be populated from production workflow mode;
- a supplied asset does not imply `edit`;
- `restore` remains distinct from `edit` because its acceptance target is materially different even if later production techniques overlap;
- future operation values require a genuinely unrepresentable request class, not a new production technique.

Adopt the proposed request-side additions, including:
- `subject_of_operation` semantics for the supplied asset being acted on;
- mutation intent;
- `deliverable_set` cardinality / variation / acceptance-basis semantics;
- separate camera motion and subject motion;
- explicit specification provenance with evidence for customer-attributed requirements.

`deliverable_set` belongs on the Normalized Request. `best_n_of_m` remains a valid acceptance-basis vocabulary value even though Wave 1 need not exercise it yet.

### 2.2 Request coverage

Accept the separate 11-item request-coverage extension as structural coverage evidence:
- 10 items may be runnable after downstream measurement prerequisites are met;
- the multi-turn probe remains representation-only;
- the original 30 authored briefs remain byte-identical and remain generation-core/value-gate probes, not demand evidence.

Combined 30+11 coverage is an authored test surface, not market prevalence.

### 2.3 Multi-turn

Keep multi-turn deferred. Preserve append-only/addressable request history and do not assume the first request is complete, but do not freeze a conversation-history schema in this tranche.

## 3. EVAL-009 disposition — ACCEPT THE CORE DESIGN, CORRECT BEFORE GOVERNOR

### 3.1 Capability Contract v2

Approve the proposed **44-capability contract** as the v2 freeze target:
- 43 active;
- 1 dormant (`repairability`) until an actual repair loop exists.

The four splits are accepted:
- 2D spatial relationship vs depth/3D relationship;
- spoken script correctness vs pronunciation/intelligibility;
- person identity vs wardrobe-invariant fidelity;
- reproducibility vs repairability.

The four additions are accepted:
- camera/framing instruction fidelity;
- sequence/state continuity;
- technical visual integrity;
- voice identity/consistency.

Also accept the three non-additions:
- style-reference fidelity stays `reference_conditioning` under a style-reference condition;
- cross-asset person/product identity is an observation-scope extension of existing identity capabilities;
- campaign/variant-set consistency is an outcome/set-level acceptance concept, not another per-asset capability.

V1 36-capability and 100-item artifacts remain historical baselines and must stay byte-identical.

### 3.2 Dependency scoring

Adopt `blocked_by_prerequisite_failure` semantics.

If a required ancestor fails, a dependent requirement may become diagnostically uninspectable, but it remains **unsatisfied** at outcome acceptance. It must never be promoted to ordinary `not_applicable` or pass.

### 3.3 PRP and conditions

Approve the Production Requirement Profile direction: provider/model/routing free.

Approve explicit production-condition recording and the prohibition on a synthetic single complexity score.

CANON-010 now owns the exact seven-value requested-operation vocabulary and EVAL must consume it unchanged.

### 3.4 Blocking internal inconsistency to correct

EVAL-009 currently contains a mechanical contradiction:
- the condition contract actually declares **13 condition families**;
- parts of the same package still say **12**;
- a two-level full product is therefore **8,192** cells, not 4,096.

This must be made consistent in every machine-readable and prose artifact, validator, benchmark note and forecast before Governor review.

### 3.5 Scientific roster

Approve the **12 core scientific question slots + 2 reserve slots** as the hypothesis roster. These are questions, not a commitment to 12 specific providers.

Sourcing may choose an equivalent implementation for a slot only when it answers the same question and the route/version differences are recorded. Access convenience cannot delete a scientific question silently.

### 3.6 CpAO/cost-knee correction

EVAL-009 also contains a semantic contradiction:
- `VID-05` asks whether premium vs fast tiers improve **accepted outcomes / CpAO**;
- the same benchmark states that Layer 4 end-to-end outcomes are not instantiated and therefore CpAO is not computable in Layers 1–3.

Controller disposition:
- keep the cost-knee question in the core scientific program;
- do **not** claim that Layers 1–3 answer CpAO;
- stage `VID-05`'s CpAO conclusion to the end-to-end/outcome stage;
- Layers 1–3 may report trial cost, reliability, latency/errors/refusals and cost per benchmark pass, but must not relabel those as customer-outcome CpAO;
- once CANON-010 request items are mapped to Layer 4 and accepted-outcome semantics are available, the premium-vs-fast question may produce real CpAO evidence.

Any call-count forecast must be recomputed or relabelled so this staging is explicit.

### 3.7 494 generations are not authorised

The proposed `494 generations / 5,515 evaluator calls / 188 human review units` is accepted only as a **full Layers-1–3 design forecast/ceiling subject to the correction above**. It is not the first paid tranche and not a budget.

Paid execution must later be staged:
1. evaluator/material qualification;
2. small scientific admission/discrimination screen;
3. deeper atomic/compound/sparse-envelope testing on surviving routes;
4. end-to-end customer outcomes and CpAO.

Do not halve repeats merely to save money if doing so destroys reliability evidence. Reduce scope by deferring whole questions or later stages instead.

### 3.8 Reproducibility semantics

EVAL-010 found that some routes expose seeds and others do not. Therefore no universal threshold may silently pretend seeded and unseeded repetition are the same experiment.

The corrected Eval package must record seed availability as a condition and define repeat evidence accordingly. Existing provisional evaluator thresholds remain unqualified; this decision does not validate a universal `0.95` repeat-consistency threshold across unlike routes.

## 4. RES-004 disposition — ACCEPT ARCHITECTURE; STAGE PACK BUILD

### 4.1 Topology v3

Adopt the forward topology:

`job -> outcome -> sequence_or_asset_set -> production_unit -> production_step -> attempt -> artifact`

Adopt:
- ordered multi-parent artifact lineage;
- deterministic local steps without fake provider attempts;
- one provider/API/transform call = one trial;
- explicit preservation of failed/refused/timed-out attempts;
- v2.1 compatibility without invented historical job/outcome context.

Historical v2.1 stays historical truth and is never silently backfilled.

### 4.2 CpAO v3

Adopt two views:
- API/tool CpAO — diagnostic;
- fully-loaded CpAO — primary business metric.

Fully-loaded CpAO includes outcome-specific labour that is actually required to produce, repair, review or accept the deliverable under the production policy.

It does **not** include one-time R&D/benchmark design, pack acquisition, evaluator qualification or general research as if those were per-customer production cost. Those remain separate program costs unless a later accounting policy explicitly amortises them.

Rejected revisions that belong to the same production journey count. A material customer scope change cuts the journey boundary. Shared upstream cost is counted once.

### 4.3 Controlled packs

Keep exactly four pack families:
- product reference;
- person reference;
- AV clean;
- commercial/campaign.

Accept the structural requirements such as multi-view identity evidence, framing diversity, same-category decoys where evaluator permissiveness must be tested, longer clean AV material, speech/language metadata and grouped campaign structure.

Do **not** freeze the provisional entity totals or `173 person-hours` as a prerequisite to the first paid model call. That figure is a full provisional acquisition plan under one sizing assumption, not a minimal execution gate.

Protected qualification and empirical holdout material must be disjoint at the meaningful identity/speaker/campaign level whenever an evaluator could overfit. Do not mechanically apply a blanket multiplier when staged acquisition can satisfy the same independence requirement more cheaply.

Prefer known-by-construction scripted/captured truth where appropriate; for example, first-party scripted AV can preserve the intended transcript without paying to rediscover it through transcription.

### 4.4 Rights

Carry forward:
- CC-BY-NC is not authorised as commercial empirical material absent explicit legal/Controller disposition;
- request-corpus/user-uploaded identity/reference images are not usable as protected benchmark material unless rights/consent are positively established;
- consent for likeness/voice must be explicit before person/AV protected packs are acquired.

No Pitt Ads outreach or full-pack acquisition is authorised by this decision.

## 5. EVAL-010 disposition — ACCEPT AS PARTIAL SUPPLY EVIDENCE

EVAL-010 is accepted as a disciplined partial verification table, not as proof that only two useful models are accessible.

The `2/26 execution-ready` result means only two candidate rows currently have identity + route + billing unit + price verified to the task's strict evidence standard. Nineteen more have substantial provider-authorised identity/route evidence but lack verified prices. Network restrictions are an evidence blocker, not evidence of model unavailability.

Carry forward its corrections to EVAL-008, including:
- no verified ~99% Hindi/Bengali accuracy claim;
- no silent fal family/version substitution;
- direct and aggregator wrappers may expose materially different controls;
- Runway Aleph should not be called enterprise-only merely from the earlier research;
- seed/reproducibility controls differ materially by route.

### 5.1 Controller price clarification

Independent Controller verification on current official Google documentation confirms that the Nano Banana 2 shorthand `$0.067 per 1K image` means **approximately $0.067 per generated 1K-resolution image**, not $0.067 per one thousand images.

The cited Google `Veo 3.1 Lite` `$0.05` value is a **route-specific 720p video+audio count price on the cited Google Cloud pricing surface**. It must not be assumed to be the universal price/billing unit for every Google/Veo API route.

All budget calculations must preserve exact route and source billing units.

### 5.2 Frontier Clouds

`Frontier Clouds` service identity remains unresolved in the repository. Do not guess. Nominal scientific scope can be frozen without it; actual cash outlay after credits cannot.

## 6. What is frozen now vs not frozen

### Approved freeze targets, pending bounded correction + Governor coherence review
- Media Request Grammar v1 direction and seven operation values;
- Normalized Request delta and request-coverage extension;
- Capability Contract v2 at 44 (43 active + 1 dormant);
- dependency-aware scoring;
- Production Requirement Profile;
- explicit condition/envelope architecture, with 13-family count to be corrected consistently;
- 12 core + 2 reserve scientific question slots;
- outcome topology v3 and CpAO v3;
- four-pack architecture and structural evidence requirements;
- supply-verification evidence standard.

### Explicitly not frozen / not authorised
- 494 generations as a paid run;
- 5,515 evaluator calls as a paid run;
- 188 human review units as a paid run;
- 173 pack-acquisition hours as a prerequisite/budget;
- provisional controlled-pack entity totals;
- unverified prices or aliases;
- cash outlay after cloud credits;
- any provider account funding or terms acceptance;
- any model/evaluator call;
- any Registry population;
- Production IR/Planner implementation.

## 7. Required next step — one bounded Eval correction only

Before Repository Governor review, run one bounded Eval integration correction. It must:
1. reconcile the condition contract and every derived count to **13 families / 8,192 two-level cells**;
2. consume CANON-010's exact requested-operation vocabulary;
3. resolve the `VID-05`/CpAO staging contradiction and update/recompute the forecast accordingly;
4. incorporate EVAL-010's seeded-vs-unseeded reproducibility finding without inventing a universal threshold;
5. map the 12 core + 2 reserve scientific slots to EVAL-010's verified/unresolved supply evidence without letting sourcing change admission;
6. produce staged execution counts for qualification -> admission screen -> deeper benchmark -> end-to-end CpAO;
7. preserve all V1 historical artifacts byte-identical;
8. perform no paid calls, acquisitions or Registry writes.

After that correction returns, one Repository Governor review should cover CANON-010, corrected Eval, RES-004, EVAL-010 and this Controller decision jointly.

Paid empirical execution remains BLOCKED until that review passes and the Controller separately approves a priced execution tranche.
