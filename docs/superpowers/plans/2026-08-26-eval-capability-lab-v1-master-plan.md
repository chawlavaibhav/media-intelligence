# Eval Capability Lab V1 — End-to-End Master Plan

> **STATUS: PROPOSED FOR CONTROLLER REVIEW. NOT APPROVED FOR EXECUTION.**
>
> No Eval task, API call, model generation, human review or spend is authorised by this document. The Controller must approve the programme before task files are created. Paid execution has an additional explicit spend gate after current API access and live prices are known.

**Date:** 26 Aug 2026

**Goal:** turn Eval from a collection of narrowly scoped battery-design tasks into the complete empirical capability system needed to support production routing, runtime verification, repair and continuous model refresh for the first product: **short-form commercial media for Indian businesses — static ads and 6–20 second product videos.**

**Architecture:** Eval has two jobs. Offline, the Capability Lab measures current **workflows** under frozen conditions and maintains the Capability Registry. Online, calibrated Eval instruments verify whether a generated asset satisfies the job's acceptance requirements and diagnose failures. Eval supplies evidence; the future Production Planner performs routing using Creative IR requirements plus Registry evidence.

**Primary optimization:** **generate once, measure many valid properties.** A frozen generated asset may be scored by several independent instruments and may later be re-scored by a newly calibrated evaluator. It is still one generation and one trial; reuse never turns one asset into multiple independent trials.

---

## 1. What Eval is supposed to be when finished

A production-ready Eval system answers five questions reliably:

1. **What capabilities does this job require?** Eval does not invent this from scratch. It consumes the Creative IR / acceptance contract and Canon-derived requirements.
2. **Which current model or workflow has demonstrated those capabilities under comparable conditions?** This is the Capability Registry.
3. **Did this particular generated asset satisfy the required properties?** Runtime evaluators answer this after generation.
4. **If it failed, what failed and what repair is plausible?** Diagnostic outputs and Empirical Memory support repair.
5. **Is our knowledge still current?** Version changes, production failures and scheduled regression trigger re-measurement.

The production flow is therefore:

```text
Creative IR + acceptance contract
        ↓
required capability set
        ↓
Production Planner (future) ← Capability Registry (Eval offline)
        ↓
chosen workflow
        ↓
generated asset
        ↓
Eval runtime instruments
        ↓
pass → accepted outcome
fail → defects → repair / alternate workflow
        ↓
Empirical Memory → future regression cases
```

**Boundary:** Eval does **not** choose the production workflow at runtime. It makes that choice possible by maintaining trustworthy evidence and trustworthy checkers.

---

## 2. What "100% complete" means for this programme

This is not "all media capabilities forever." It is **V1 production readiness for the first product scope**. Models will continue changing, so the Lab becomes a recurring operating system after V1.

### Weighted readiness model

| Component | Weight | Current state | Current credit |
|---|---:|---|---:|
| Product-relative capability map | 10 | V0 exists but is deliberately narrow; broader original plan is not frozen | **4** |
| Measurement definitions / observation units / pass rules | 15 | strong work on text, identity, count, spatial and temporal text; many production capabilities unresolved | **8** |
| Instrument calibration / qualification | 15 | Devanagari calibration battery human-validated; no checker qualified; other instruments mostly uncalibrated | **2** |
| Reusable probe resources / manifests | 15 | strong Devanagari reading corpus; some video/image evaluation corpora; no unified production probes | **5** |
| Harness, run integrity, telemetry discipline | 10 | substantial plumbing and negative-control lessons exist | **7** |
| Current model/workflow admission and access snapshot | 5 | no frozen current roster | **0** |
| Empirical model/workflow benchmark results | 15 | no current generator benchmark | **0** |
| Capability Registry implementation and population | 10 | schema work exists; no empirical rows | **1** |
| Refresh / production feedback / regression loop | 5 | conceptual only | **0** |
| **Total** | **100** | | **27 / 100** |

**Interpretation:** Eval is approximately **27% system-ready**, but **0% complete on the part customers ultimately depend on: current empirical model/workflow capability knowledge.** Most completed work is foundational measurement discipline. That work is valuable and should be reused, not repeated.

### V1 production-readiness gate

Eval is "ready enough for first production routing" only when all of these are true:

- ≥90% of **critical hard-fidelity capabilities** are either measurable by a qualified instrument or explicitly marked `unresolved` with a safe production fallback; nothing critical silently disappears.
- the common production scenarios in §7 have empirical workflow evidence, not vendor claims;
- every active Registry measurement names exact provider/model/version/workflow, conditions, instrument, sample counts, cost and date;
- no Registry score uses an unqualified instrument;
- every active workflow has fresh admission/regression evidence;
- runtime evaluation can compile the Creative IR acceptance requirements into available checkers or explicitly return `unverifiable`;
- the frozen regression set contains our own recurring production failures as they accumulate.

---

## 3. Complete V1 capability map

The Registry must **not** collapse these into one "model score." A workflow can be excellent at motion and unusable for logos; averaging destroys routing value. The unit of knowledge is **workflow × capability × condition**.

### A. Static / frame-level hard fidelity

1. Instruction / mandatory element presence
2. Prohibited element absence
3. Exact Latin text
4. Exact Devanagari text
5. Logo / wordmark fidelity
6. Brand colour fidelity where a tolerance is specified
7. Product-reference fidelity — silhouette / packaging geometry / label / colourway
8. Product material appearance — e.g. glass, metal, liquid, fabric where commercially relevant
9. Person / character reference fidelity
10. Attribute binding — the right property attached to the right entity
11. Object count
12. 2D / depth spatial relationships
13. Human-object contact / holding / using / manipulating
14. Occlusion / contact plausibility
15. Edit locality — requested region changed while protected regions remain stable
16. Delivery constraints — aspect ratio, resolution, safe area, duration where deterministic

### B. Cross-output and video hard fidelity

17. Person identity across prompts / shots / sessions
18. Product identity across views / shots
19. Logo and text stability across frames
20. Background / wardrobe / lighting invariants when declared
21. Action / object-state continuity
22. Camera instruction adherence
23. Shot-to-shot spatial continuity / screen direction where specified
24. Motion quality and physical plausibility
25. Anatomy / deformation stability during motion
26. Temporal duration and beat-boundary adherence where exact timing is required

### C. Audio / speech / audiovisual production capability

27. Voiceover-only workflow — video quality when **no visible speaker must sync**
28. Speech intelligibility and exact transcript / language
29. Single visible speaker — native audiovisual generation
30. Single visible speaker — external lip-sync workflow
31. Hindi single-speaker lip-sync
32. Two-speaker dialogue — correct speaker turn assignment
33. Two-speaker lip-sync / mouth assignment
34. Audio-video synchronization
35. Voice identity / stability when a voice reference is supplied
36. Subtitle / spoken-copy agreement when subtitles are required

These are deliberately separated because the user's earlier production experience shows why: **voiceover-only, one visible speaker, external lip-sync and two-speaker dialogue are different workflows and must never inherit one another's capability score.**

### D. Creative fitness — Evaluation-B, Canon-informed and separately calibrated

37. Visual hierarchy / attention order
38. Product-as-hero / commercial subject priority
39. Proposition clarity
40. Composition / framing / depth / figure-ground
41. Lighting and material presentation as creative craft
42. Objective fit
43. Audience fit / register
44. Emotional target / brand feel
45. Hook / opening effectiveness
46. Pacing / temporal hierarchy
47. Feed-native / platform fitness, including sound-off and thumbnail legibility
48. Indian cultural / market appropriateness where the Canon/empirical source is sufficient

Evaluation-B must remain separate from deterministic hard fidelity. A beautifully composed ad with the wrong logo fails a hard requirement; a technically perfect asset may still be commercially poor.

### E. Operational and workflow economics — measured as telemetry, not separate generations

49. Posted generation / edit / audio cost on run date
50. Evaluation cost
51. Human-review cost where used
52. Latency p50 / p95
53. API error rate and error class
54. Moderation / refusal rate
55. Repeatability / seed behaviour
56. Pass@1 and, when repeats justify it, pass@k / expected attempts
57. Repair success rate and repair cost
58. **Cost per Accepted Outcome** for the workflow, including evaluator and repair cost that the experiment actually incurred
59. Freshness / version drift

---

## 4. Measurement architecture: atomic probes + reusable production probes

### Rule 1 — use atomic probes only when isolation matters

Examples: a plain one-word Devanagari render isolates script ability; a controlled two-object count isolates numeracy; a known-audio lip-sync clip isolates synchronization. These are diagnostic instruments, not miniature advertisements.

Atomic probes answer **why** a workflow failed. They stay small.

### Rule 2 — production probes carry several legitimate measurements at once

A single product-and-person image may legitimately be scored for product identity, person identity, logo fidelity, text fidelity, count, holding/contact, colour, composition and hierarchy. A single video may be scored for those plus temporal identity, text stability, motion, camera instruction, continuity, pacing and audio-video behaviour.

**The generation is stored once. Each measurement is a separate record pointing to the same `asset_id`.** The asset does not become independent evidence twice.

### Rule 3 — do not combine properties that confound the question

Keep separate baseline probes for:

- plain text vs in-scene text;
- product reference fidelity before product handling;
- single speaker vs two speakers;
- voiceover-only vs visible speech;
- native audiovisual generation vs post-generation lip-sync;
- hard fidelity vs creative fitness;
- instrument calibration vs generator benchmarking.

### Rule 4 — re-score before re-generate

A new evaluator version does **not** automatically require new model generations. Freeze the old outputs and re-score them. A new **generation model version** does require fresh generations. This distinction saves the largest amount of repeated work over time.

---

## 5. Frozen reusable probe packs

The following are V1 **planning quantities**. Final manifests are created before any paid model run and then frozen.

### Pack S — Static Commercial Pack: 24 briefs

Four strata × six briefs:

- product / packshot + logo + copy + material;
- person + product reference + interaction;
- multi-object count / relation / attribute binding;
- typography-led / commercial-layout assets with hierarchy and mandatories.

Every brief declares hard requirements, soft creative requirements, observation units and which capability records it is allowed to produce.

**Deep run per image workflow:** 24 distinct items × 2 repeats = **48 images**.

**Admission subset:** 8 of the same 24 items. Their outputs are retained and count as the first run for those exact items if all conditions remain unchanged.

### Pack V — Video Commercial Pack: 24 briefs

Six strata × four briefs:

- voiceover-only / no visible speech;
- one visible speaker with native generated speech;
- two-speaker native dialogue;
- product handling / demonstration;
- on-screen text / logo under motion;
- multi-shot / continuity / camera-instruction cases.

Default duration: one fixed V1 test duration within the first-product 6–20 second range, chosen before roster execution based on common endpoint support. If an endpoint cannot produce that duration directly, its workflow graph must state how it composes the duration; that is a different workflow condition.

**Deep run per foundation-video workflow:** 24 items × 2 repeats = **48 clips**.

**Admission subset:** 8 of the same 24.

### Pack L — Controlled Lip-Sync Pack: 16 source cases

Four strata × four cases:

- single speaker, English;
- single speaker, Hindi;
- two speakers, English alternating turns;
- two speakers, Hindi alternating turns.

The source video, exact audio, speaker-turn timing and expected active speaker are frozen. This pack tests **external lip-sync workflows**, not video generation quality.

**Deep run per lip-sync workflow:** 16 × 2 repeats = **32 outputs**.

**Admission subset:** 8 of the same 16.

### Pack E — Edit / Repair Pack: 12 source assets

Four strata × three cases:

- exact text / logo correction;
- product-reference correction;
- local object/layout correction;
- background/style change while protected identity/content stays fixed.

**Deep run per edit workflow:** 12 × 2 = **24 edits**.

**Admission subset:** 6 of the same 12.

### Atomic diagnostic packs

Keep existing EVAL-005 96-case Devanagari **checker-qualification** battery exactly as a checker test. Build only the minimum additional atomic packs required to isolate text, count/spatial, identity and audiovisual judge failure. These do not become a second parallel production benchmark.

---

## 6. Resource plan: use what exists, ask only for exact gaps

### Existing Resources that should be reused

- Devanagari scene/crop corpus → calibrating Devanagari reading instruments, with the existing lineage caveats.
- EVAL-005 validated constructed battery → Devanagari checker qualification.
- ImageRewardDB → candidate material for creative-evaluator calibration, not generator ground truth.
- VideoFeedback / VideoGen RewardBench → candidate multi-dimensional video-judge calibration material.
- KoNViD → technical video-quality calibration only, not creative merit.
- existing media-factory failures → permanent regression candidates once the actual media is made accessible and multi-defect re-annotation is performed.

### Exact new Resources requests likely required

**R1 — product references:** 12 products, ideally with front / side / back or equivalent identity views, known colourway, packaging geometry and logo. Internal-evaluation rights sufficient.

**R2 — person/character references:** 12 identities with 2–4 reference views and predeclared invariants. Prefer rights-cleared / consented or synthetic identities to avoid unnecessary personal-data burden.

**R3 — interaction source set:** 20–24 images/clips containing clear holding, contact, using and occlusion states for instrument calibration; include negative near-misses.

**R4 — controlled speech material:** 16 Pack-L source videos plus exact Hindi/English audio/transcripts and speaker-turn timestamps. Synthetic speech is acceptable for synchronization testing; voice-naturalness is a separate property.

**R5 — commercial creative calibration:** enough static/video material to calibrate Evaluation-B on the dimensions Canon actually supports. First target: **60 assets** split roughly 30 static / 30 video, reviewed dimension-by-dimension rather than with one holistic "good/bad" label.

**R6 — old empirical failures:** bring the previous `media-factory` failure media into a legitimately accessible evaluation surface and re-annotate every item for **all visible defects**, not one salient label.

Resources must not collect beyond a request like R1–R6. If an existing corpus satisfies the requirement, reuse wins over acquisition.

---

## 7. Five production scenario families the Registry must ultimately answer

Atomic capability rows are necessary but insufficient. The product must know whether a **workflow graph** succeeds on actual job shapes.

### Scenario P1 — static commercial asset with exact copy / logo

Compare native generation against generation + deterministic text/logo compositing when applicable. Measure visual quality **and** the cost of reaching acceptance, not just whether a model can spell.

### Scenario P2 — product video with voiceover, nobody visibly speaking

This is a separate capability family. Lip-sync is irrelevant and must not penalize a workflow. Compare foundation-video workflows plus external TTS/mux where appropriate.

### Scenario P3 — one visible speaker

Compare native audiovisual generation against silent/video generation + speech + external lip-sync where both are feasible. Measure identity under speech, synchronization, language and CpAO.

### Scenario P4 — two visible speakers in dialogue

Measure correct turn assignment, which mouth speaks, identity stability, synchronization, temporal interaction and refusal/error behaviour. A workflow that works for P3 does not inherit a P4 pass.

### Scenario P5 — product-reference demo / interaction

Compare direct reference-to-video and decomposed keyframe / image-to-video workflows where available. Measure product identity, holding/contact, motion, multi-shot continuity, logo/text preservation and CpAO.

These five scenario families become the bridge from "model benchmark" to useful routing evidence.

---

## 8. Model/workflow roster: freeze by rule, not by today's marketing list

Model names change too quickly to hard-code the architecture around them. Before each major benchmark wave, Eval performs a **zero-generation admission snapshot** from official API documentation and configured credentials.

### V1 maximum roster slots

- **4 image-generation workflows**
- **5 foundation-video workflows**
- **3 external audiovisual / lip-sync workflows**
- **2 edit / repair workflows**

Maximum: **14 workflow paths**. One foundation model may occupy more than one path when modes such as text-to-video, image-to-video or reference-to-video are materially different; the Registry stores them separately.

### Admission eligibility

A workflow is eligible only if the exact API model/version can be pinned, legitimate API access exists in the execution environment, current pricing is discoverable, required media/input modes are documented, and its terms permit the intended internal evaluation. Missing credentials produce `unavailable`; they do not trigger a workaround.

### Deep-test advancement

There is **no universal overall score**. After the admission sweep, a workflow advances when it is one of the top two observed options for at least one critical family, provides a unique production capability, or is materially cheaper at comparable hard-gate success. Maximum deep roster: **3 image + 3 foundation video + 2 lip-sync + 2 edit workflows**.

The exact advancement rule and any cost-difference threshold are frozen in the task **before** results are read.

---

## 9. First-wave quantity model — how much generation this programme actually implies

### Admission sweep

| Type | workflows | admission items | outputs |
|---|---:|---:|---:|
| Image | 4 | 8 | 32 |
| Foundation video | 5 | 8 | 40 |
| Lip-sync | 3 | 8 | 24 |
| Edit / repair | 2 | 6 | 12 |
| **Total** | **14 max** | | **108 outputs** |

One output per item at admission. This is a screen, not a final capability estimate.

### Deep profile — maximum additional outputs after reuse

Admission cases are subsets of the deep packs and are **not regenerated for repeat 1** when conditions are identical.

| Type | deep workflows | full deep target | already held from admission | additional per workflow | max additional |
|---|---:|---:|---:|---:|---:|
| Image | 3 | 24×2 = 48 | 8 | 40 | 120 |
| Foundation video | 3 | 24×2 = 48 | 8 | 40 | 120 |
| Lip-sync | 2 | 16×2 = 32 | 8 | 24 | 48 |
| Edit / repair | 2 | 12×2 = 24 | 6 | 18 | 36 |
| **Total additional** | | | | | **324** |

Therefore the **maximum planned first-wave output count is 108 + 324 = 432** before technical retries.

Technical API failures may receive at most one retry per failed call and the total retry allowance is capped at **10% of the planned run**, giving a hard ceiling of **475 external production calls** for this wave. A quality failure is **not** an API-error retry; it is evidence and remains in the dataset.

This is a run-size ceiling, **not a spend approval**. Before paid execution the agent must price every cell at current rates and produce expected / high-bound INR totals for Controller approval.

---

## 10. Instrument strategy — calibrate families, not one checker per task

A major cause of duplication would be creating a separate human-calibration exercise for every capability. Instead, build a few **multi-label calibration surfaces**, while keeping results separate by dimension.

### Instrument family I-A — exact text / transcript

- Devanagari: reuse the validated EVAL-005 checker battery.
- Latin: matched deterministic / OCR + VLM calibration.
- video text stability: reuse the qualified transcription instrument per sampled frame; stability comparison itself is deterministic.
- spoken transcript: ASR / transcript comparison calibrated separately by language.

### I-B — reference / identity / brand / interaction visual judge

Use a common calibration media set where humans independently label **separate fields**: person fidelity, product fidelity, logo fidelity, protected attributes, holding/contact/occlusion. One media item can therefore calibrate several predicates, but agreement is reported per predicate.

### I-C — count / spatial detector

Reuse one ~20-item hand-labelled local set for both count and relation, as the existing plan already recommends. Different detector thresholds and separate qualification results remain.

### I-D — temporal / motion / continuity judge

Calibrate on existing generated-video / real-video material plus controlled positive/negative cases. Measure camera adherence, temporal identity, motion/anatomy, object state and continuity separately.

### I-E — audiovisual judge

Use Pack L and controlled references for active-speaker correctness, AV offset / synchronization, transcript correctness and identity under speech. Deterministic signal methods may provide diagnostics; human judgement remains the reference where the predicate is perceptual.

### I-F — creative fitness judge

Separately calibrated against human dimension-level reviews using Canon-derived rubrics. It may later score **the same S/V outputs already generated**. Default new-generation count for evaluator calibration is **zero**; generate extra stress cases only if an important creative dimension is absent from the frozen packs.

### Human effort planning envelope

For the complete V1, target approximately:

- hard / temporal / audiovisual instrument reference and calibration: **12–18 human-hours** total;
- Evaluation-B creative reference/calibration: **12–20 human-hours**;
- Hindi-specific linguistic review beyond what is already completed: **~2–3 hours** if new phrases/scripts require it.

Planning envelope: **26–41 one-time human-hours**. This is deliberately a time envelope, not an invented rupee value. Each task must report the actual human surface before approval.

---

## 11. Registry V1 — what gets stored

Every measurement row represents **one property under one workflow condition**, not a claim about a model in general.

Required fields:

```yaml
identity:
  provider
  model
  exact_version
  endpoint
  workflow_graph_id
capability:
  dimension_id
  difficulty_or_scenario
  observation_unit
conditions:
  prompt_manifest_version
  references
  duration
  resolution
  aspect_ratio
  language
  script
  seed_policy
result:
  n_items
  n_trials
  passes
  pass_rate
  indeterminate
  failed_trials: [multiple defects allowed]
instrument:
  exact_id_and_version
  calibration_ref
  gate_or_diagnosis
cost:
  generation
  evaluation
  human_review
  repair
  cost_per_pass_or_lower_bound
operations:
  latency_p50
  latency_p95
  api_errors
  refusals
  repeat_agreement
provenance:
  run_ref
  asset_ids
  tested_date
  sample_source
freshness:
  status
  retest_triggers
```

Also maintain a **scenario/workflow result** for P1–P5 that can combine component costs and acceptance outcomes across a workflow graph. This is the level most useful to a future Production Planner.

No row may be interpreted outside its stated conditions. No single scalar "best model" field exists.

---

## 12. Proposed execution programme — finite tasks with boundaries

These are **proposed task boundaries, not approved task files**. After Controller approval they should receive new Eval task IDs; the withdrawn EVAL-006 ID must not be silently reused for a materially different method.

### Proposed Task A — Freeze V1 capability contract and coverage matrix

**Cost:** ₹0 API; 0 generations.

**Work:** convert §3 into a machine-readable capability map linked to Creative IR paths, acceptance requirements, observation unit, evaluator family, resource need and scenario family. Reconcile the existing V0 dimensions rather than deleting them.

**Quantitative finish line:** every one of the 59 V1 capability/operational rows above is classified `measurable_now`, `instrument_needs_calibration`, `resource_missing`, `canon/rubric_missing`, or `deferred`, with an owner and next gate. Every hard/exact Creative IR family maps to at least one capability or an explicit unresolved state.

**Outcome:** one authoritative coverage map; no more task-by-task drift in scope.

### Proposed Task B — Current access, roster and live-cost snapshot

**Cost:** ₹0 generation/API benchmark spend.

**Work:** inspect only official provider docs plus the execution environment's configured credential availability. Select up to the 14 roster slots in §8 and pin exact endpoints/versions/modes. Never expose secrets; record only `configured / absent / unusable`.

**Quantitative finish line:** 100% of selected workflow paths have exact version, endpoint, supported inputs, duration/resolution constraints, official price source/date and access state. Produce admission and deep-run expected/high-bound cost forecasts.

**Stop:** paid work cannot start here.

### Proposed Task C — Build and freeze the reusable probe packs

**Cost:** ₹0 model generation. Human/source work only if the Controller separately authorises the concrete Resources/human requests.

**Work:** materialize S=24, V=24, L=16 and E=12 manifests; admission subsets 8/8/8/6; integrate existing atomic batteries; obtain only missing R1–R6 resources.

**Quantitative finish line:** **76 production probes** total, every item hashed/versioned, with capability tags, hard requirements, permitted measurements and observation units. Every critical V1 capability must have a stated opportunity count; any capability below the predeclared minimum is flagged before generation.

### Proposed Task D — Qualify the evaluator families

**Cost:** evaluator API + approved human time; **0 generator benchmarking**.

**Work:** qualify I-A through I-E; prepare I-F only when Canon-derived creative rubric is ready. Reuse multi-label reference material where valid. Preserve the EVAL-005 zero-false-pass principle for Devanagari qualification without pretending the small sample establishes a real-world error rate.

**Quantitative finish line:** every instrument has `qualified`, `diagnosis_only`, `failed`, or `unavailable` status with exact version and evidence. If a critical capability lacks a gate-qualified instrument, its Registry state remains explicitly unmeasurable; do not benchmark it with guesswork.

**Gate:** paid generator benchmarking cannot begin until the required instrument for that capability is qualified.

### Proposed Task E — Admission sweep

**Maximum outputs:** **108**; + ≤10% technical retry allowance shared with the total wave.

**Work:** run the frozen admission subsets across the frozen roster in round-robin order. Score every valid capability carried by each output and collect operational telemetry automatically.

**Quantitative finish line:** one comparable admission record for every accessible workflow and every applicable admission item; no missing cost/latency/error fields. Freeze results before deciding deep-test advancement.

**Outcome:** prune weak/redundant models cheaply; do not spend full deep-benchmark money on every vendor variant.

### Proposed Task F — Deep capability profile

**Maximum additional outputs:** **324**. Combined first-wave ceiling E+F: **432 planned / 475 including technical retry cap**.

**Work:** deep-run max 3 image, 3 foundation-video, 2 lip-sync, 2 edit workflows. Reuse admission outputs. Score all valid hard capabilities on each asset. Log co-occurring failures, not one failure label.

**Quantitative finish line:** each deep workflow has 2 trials for every item in its applicable frozen production pack, with Registry cells populated only for dimensions whose instruments qualified.

### Proposed Task G — Creative fitness calibration and re-score

**Default new generations:** **0**.

**Work:** use Canon-derived Evaluation-B rubrics and human reference reviews to qualify the creative judge. Then score the existing S/V output corpus for hierarchy, proposition, composition, objective/audience fit, tone, hook, pacing and platform fitness where supported.

**Quantitative finish line:** creative measurements are attached to existing assets without changing hard-fidelity scores. Any unmeasurable creative dimension stays explicit rather than being inferred from a generic aesthetic score.

### Proposed Task H — Workflow composition, repair and scenario evidence

**Work:** convert model-level evidence into workflow-level evidence for P1–P5. Compare the two most plausible workflow shapes per scenario where two exist: e.g. native text vs composited text; native speech vs external lip-sync; direct reference-video vs decomposed keyframe chain.

**Planned scenario surface:** **5 scenario families × 4 briefs × up to 2 workflows × 2 repeats = 80 workflow outcomes maximum**, but reuse components/outputs from Tasks E/F wherever conditions are identical. New generation/edit calls are separately counted and priced before execution.

Additionally, sample up to **20 failed deep-run outputs** and try at most **2 predeclared repair strategies** each → maximum **40 repair attempts**. Do not repair only the failures that look easy.

**Quantitative finish line:** Registry contains current workflow-level evidence and CpAO components for all five production scenario families, or an explicit `no_qualified_workflow` state.

### Proposed Task I — Registry productionization and continuous operating loop

**Cost:** no new generation required to implement.

**Work:** validate Registry schema, requirement→capability lookup interface, freshness states, version triggers, frozen run references, and production-failure ingestion. Create admission/regression schedules.

**Quantitative finish line:** 100% of Registry rows validate mechanically; every row traces to frozen assets + run + instrument; every active workflow has a next retest trigger; no stale row can silently be treated as current.

**Cadence after V1:**

- new serious model/version → admission subset;
- promising/unique → targeted deep profile, not automatic full battery;
- active workflows → monthly admission regression;
- major provider/model version change → relevant full profile;
- quarterly → full profile for production-active workflows only;
- production failure spike → targeted regression case immediately;
- evaluator version change → re-score stored outputs first; regenerate only when the generator changed.

---

## 13. Task dependencies and what can run in parallel

```text
A Capability contract
        ↓
B roster/access/cost  ──────────────┐
C probe packs/resources ────────────┼→ D evaluator qualification
                                     ↓
                                 E admission
                                     ↓
                                 F deep profile
                                  ↙        ↘
                   G creative re-score    H workflows/repair
                                  ↘        ↙
                                   I Registry productionization
```

B and C can proceed in parallel after A. Parts of D can proceed as soon as their reference material exists. **E and F are the expensive gates and must wait for both frozen probes and qualified instruments.** G intentionally follows generation so it reuses the same outputs rather than creating a second media corpus.

---

## 14. Spend / credential governance

Approval of this master plan is **not automatically approval to spend money**.

Before the first external paid call, Task B must have produced:

- exact configured providers (without exposing keys);
- exact model IDs and endpoints;
- current official pricing;
- admission-call forecast;
- deep-call forecast;
- evaluator-call forecast;
- expected and high-bound INR totals;
- the precise API account/environment that will be charged.

The Controller then records a rupee cap. The worker cannot infer a payment authorization merely because credentials happen to exist.

If an API credential is missing, the workflow is recorded `unavailable`. No new account, purchase, plugin, credential or provider substitution is authorised automatically.

---

## 15. Data reuse / anti-duplication rules — binding if this plan is approved

1. Every generated output receives a stable `asset_id` before scoring.
2. A later instrument points to the existing asset; it does not regenerate it for convenience.
3. Admission items are literal subsets of deep packs, not separately authored lookalikes.
4. Admission output counts as deep repeat 1 only when model version, workflow graph, prompt, reference inputs and generation parameters are identical.
5. Operational metrics are captured on every paid call and never create a separate generation task.
6. A single asset may produce many measurement records; it remains one trial.
7. Repeats measure reliability, not independent breadth.
8. Frames from one clip are one sequence trial.
9. A model update creates a new capability run; an evaluator update triggers re-scoring first.
10. Production failures become regression cases only after their requirements, media, outcome and all visible defects are frozen.

---

## 16. What this plan deliberately does not build yet

- Production IR implementation;
- Production Planner / routing algorithm;
- a universal model leaderboard;
- a single weighted score across capabilities;
- automatic creative-quality truth from Canon;
- campaign-effectiveness prediction;
- a giant speculative Resources corpus;
- exhaustive audio/music generation benchmarking outside first-product needs;
- training/fine-tuning/RAG infrastructure.

These are downstream or separate product questions. V1 Eval's job is to make the **evidence layer trustworthy and useful enough that routing can be built on top of it.**

---

## 17. Controller approval package

When this proposal is reviewed, the Controller should approve/reject these decisions explicitly:

1. first-product Eval scope = static commercial ads + 6–20 second commercial/product videos for Indian businesses;
2. the complete V1 capability families in §3;
3. atomic + reusable production-probe architecture;
4. pack sizes S24 / V24 / L16 / E12 and admission subsets;
5. maximum roster slots 4 image / 5 video / 3 lip-sync / 2 edit;
6. maximum deep roster 3 / 3 / 2 / 2;
7. first-wave planned output ceiling 432, technical retry ceiling 475, **without yet approving spend**;
8. the proposed Task A–I sequence;
9. separate paid-spend gate after live access/pricing forecast;
10. V1 readiness criteria in §2 and continuous refresh cadence in Task I.

Only after those are approved should Controller-authored Eval task files be created.

---

## 18. Self-review against the project architecture

- **Canon/Eval boundary preserved:** creative principles come from Canon; model capability is empirical only.
- **Resources boundary preserved:** Eval specifies exact material; Resources owns discovery/rights/integrity.
- **Planner boundary preserved:** Registry provides evidence; Eval does not silently become router.
- **Existing Eval work preserved:** EVAL-005 remains the checker battery, identity rubric remains calibration input, V0 observation-unit and correlation rules carry forward.
- **Duplication reduced:** production packs are shared, admission is a subset of deep, creative evaluation reuses generated outputs, operational measurement is telemetry, evaluator changes trigger re-scoring.
- **Quantities exist before execution:** pack sizes, roster ceilings, admission/deep call counts, retry ceiling, human-hour envelope and task finish lines are stated.
- **Unknown costs remain honestly unknown:** rupee spend is not invented before access and live provider pricing are known.
- **Early production lessons are structurally represented:** voiceover-only, native one-speaker, external lip-sync and two-speaker dialogue are distinct scenario/capability families rather than anecdotes.
