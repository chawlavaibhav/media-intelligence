# Eval V1 overnight program

**Date:** 26 Aug 2026  
**Status:** CONTROLLER-PREPARED FOR USER ASSIGNMENT  
**Supersedes for future planning:** the execution approach in paused `EVAL-006`; **do not execute EVAL-006**. Preserve it as historical evidence.  
**Read first:** `coordination/plans/2026-08-26-THREE-STREAM-OVERNIGHT-PROGRAM.md`, Eval Charter/Handoff, EVAL-001..005 findings/tasks, Capability Lab V0 plan, current Devanagari battery/human-validation material, Registry schema draft, Resources cross-stream notes.

## 0. Zoom-out: what Eval must become

Eval / Capability Lab is the empirical truth layer for current models/workflows. Canon says **what a job requires**; Eval measures **which current workflow can satisfy it, under what conditions, at what reliability/cost/failure profile, using which calibrated instrument**.

Eval V1 is production-usable when:

1. the first-product capability map is complete enough to express routing-relevant requirements;
2. each measurable capability has a defined observation unit, test design and instrument family;
3. evaluators are qualified/calibrated before their outputs become model capability claims;
4. benchmark generation is reusable across all valid measurements rather than one generation per metric;
5. current model/workflow versions are empirically measured, with cost/latency/reliability/failures and freshness;
6. complete production recipes are compared on pass rate, retry burden and Cost per Accepted Outcome;
7. new model versions and real production failures enter a maintained regression/retest system.

### Current starting state

- EVAL-001/002/003 closed; EVAL-004 exploratory/stopped; EVAL-005 validated Devanagari checker battery complete;
- authoritative Devanagari checker battery: **96 items = 48 match / 48 mismatch**, 48 accepted base words, 33 hard opportunities, 20 failure classes / 5 groups;
- reusable harness/plumbing exists but is not the complete production benchmark system;
- **0 qualified checker/instrument**;
- **0 benchmarked current generator/workflow**;
- **0 empirical Capability Registry entries**;
- `EVAL-006` paused and its prior spend authority withdrawn;
- no paid calls are authorised in this overnight program.

## 1. Frozen V1 capability map for tonight

The worker may refine definitions/conditions but may not silently add/remove capabilities. Proposed changes go in the Controller Brief.

### A. Constraint fidelity — 5

1. `object_count`
2. `attribute_binding`
3. `spatial_relationship`
4. `action_adherence`
5. `delivery_format_compliance` — duration/aspect/resolution/output contract

### B. Text & brand — 5

6. `exact_text_latin`
7. `exact_text_devanagari`
8. `typography_legibility`
9. `logo_wordmark_fidelity`
10. `packaging_brand_colour_fidelity`

### C. Identity & references — 4

11. `person_identity`
12. `product_identity`
13. `reference_conditioning`
14. `edit_preservation`

### D. Human & physical realism — 5

15. `anatomy_hands`
16. `human_object_contact`
17. `human_human_interaction`
18. `motion_action_quality`
19. `physics_material_appearance`

### E. Temporal / continuity — 4

20. `person_stability_in_clip`
21. `product_stability_in_clip`
22. `text_logo_stability_in_clip`
23. `multi_shot_spatial_continuity`

### F. Speech / audio — 5

24. `spoken_language_correctness`
25. `single_speaker_lip_sync`
26. `two_speaker_turn_assignment_and_lip_sync`
27. `emotional_prosodic_fit`
28. `audio_video_synchronisation`

### G. Commercial / creative fitness — 4

29. `proposition_objective_fit`
30. `hierarchy_product_as_hero`
31. `composition_brand_register`
32. `hook_pacing_temporal_hierarchy`

### H. Operational / workflow behaviour — 4

33. `reliability_pass_at_k`
34. `cost_and_cpao`
35. `latency_errors_refusals`
36. `reproducibility_repairability`

## 2. Full Eval V1 task queue

| ID | Task | Overnight? | Start | End / quantitative done condition |
|---|---|---|---|---|
| **E1** | Capability & measurement contract | **RUN TONIGHT** | existing Eval evidence + frozen 36 map | 36/36 dimensions defined with observation unit, modality/workflow applicability, atomic/compound test route, difficulty ladder, instrument family, resource need, pass-output type and Registry representation |
| **E2** | Current workflow/API/access/pricing inventory | **RUN TONIGHT** | public official docs + local environment access visibility | <=19 frozen candidate endpoints across five lanes; exact model/version/endpoint/access state/current official price source/date; credential presence boolean only; exact later call-count and cost forecast; **0 API generations/evaluations** |
| **E3** | Evaluator-stack qualification specification | **RUN TONIGHT — DESIGN/PACKAGE** | E1 + current EVAL-005 evidence + shared resource contract | 6/6 evaluator families end with qualification protocol, calibration material requirement, gate metrics and explicit blocked dependencies; existing Devanagari battery integrated correctly; no instrument claimed qualified |
| **E4** | Reusable master benchmark bank design | **RUN TONIGHT** | E1; shared first-product scope | exactly 100 base-item definitions = 40 atomic + 60 compound; every critical capability exercised by >=10 distinct base items across the whole design where semantically applicable; each item declares every valid measurement it supports; later 12 production briefs reserved for Canon bank, not independently authored |
| **E5** | Generate-once evaluation harness + Registry/storage interface | **RUN TONIGHT** | E1/E4 schemas; existing harness may be reused | dummy/synthetic test run proves one generated asset fans out to all eligible metrics; provenance complete; duplicate-regeneration guard; negative controls; Registry schema instantiated empty; **0 empirical rows** |
| **E6** | Evaluator qualification run | LATER | E3 + Resources packs + approved model access/budget/human needs | each of 6 families ends `qualified / provisional / unmeasurable`; no model capability score uses an unqualified instrument |
| **E7** | Current-model admission screen | LATER PAID | E2/E5/E6 + cost approval | maximum **204 generated/processed outputs** at full 19-endpoint roster under lane-specific screen counts; every endpoint `screened` or `unavailable`; no endpoint called qualified |
| **E8** | Deep workflow qualification | LATER PAID | E7 | top <=2 per lane; maximum **520 generated/processed outputs** under frozen counts; reusable multi-metric scoring; evidence-backed Registry cells |
| **E9** | Production workflow benchmark | LATER PAID | Canon 30-bank + select 12 briefs + E8 + Resources | **12 briefs × <=4 complete recipes × 2 attempts = <=96 end-to-end trials**; hard fidelity, creative acceptance, retry/manual intervention, cost and CpAO reported |
| **E10** | Production interface & maintenance | LATER | E9 | Registry consumption contract; new-model admission, monthly active regression, quarterly broader qualification and event-driven production-failure retest frozen |

## 3. E1 — Capability and measurement contract

### Objective

Turn the 36-name map into a machine-readable contract so later tasks do not rediscover what a capability means.

### For every dimension define

- id + plain-English definition;
- what is **inside** and **outside** the dimension;
- modality/workflow applicability: image, video, native AV, lip-sync, TTS, editing/compositing;
- minimum observation unit: frame / image / shot / sampled-clip / whole clip / shot-pair / sequence / asset set;
- atomic probe design;
- compound-scenario measurements that can validly reuse the same asset;
- difficulty ladder, preferably 3–5 ordered levels with observable changes rather than adjectives;
- primary instrument family and any secondary/human verifier;
- external resource requirement: `required / constructed_by_eval / no_external_resource`;
- result form: exact pass/fail, structured categorical, pairwise preference, human/hybrid score, operational metric;
- failure-recording vocabulary policy: observer terms retained; ontology mapping later;
- Registry conditions required to make two measurements comparable;
- whether the dimension can be used as a hard routing constraint later or only as descriptive creative evidence.

### Observation-unit rule

Frames sampled from one video clip are **one trial**, not many independent trials. If several dimensions inspect the same clip, they are several measurements of one trial, not several generations.

### Deliverables

- `eval/v1/CAPABILITY-CONTRACT.md`
- `eval/v1/capability-contract.yaml`
- `eval/v1/CAPABILITY-DEPENDENCY-MATRIX.md`

### Done when

36/36 dimensions have no missing mandatory field and every dimension maps to at least one measurement path or explicit `currently_unmeasurable` state.

## 4. E2 — Current workflow/API/access/pricing inventory

### Purpose

Separate the permanent benchmark architecture from current model churn. The permanent capability contract contains no provider names. E2 creates the time-stamped roster for the next empirical wave.

### Five lanes and hard roster caps

1. image generation/editing: **<=4 endpoints**;
2. general text/image-to-video: **<=5**;
3. native audio-video: **<=4**;
4. dedicated lip-sync/digital-human: **<=3**;
5. TTS/external VO: **<=3**.

Maximum endpoint/workflow combinations: **19**. One model may occupy more than one lane only if the workflow/endpoint conditions are materially different and recorded separately.

### Admission research rules

Use official provider documentation/pricing only for identity, current availability and price. Secondary sources may be used as leads but not as final evidence.

Record:

- vendor;
- exact current model/API id and marketed name;
- exact endpoint/workflow;
- version pinning mechanism or explicit inability to pin;
- modalities and reference/audio capabilities;
- max duration/resolution/aspect constraints relevant to our benchmark;
- official price and billing unit;
- price source URL + date;
- API availability region/account restrictions where stated;
- local execution environment: credential/config **present / absent / unknown** only. Never print or commit secret values;
- why the endpoint merits a Wave-1 slot;
- `admit / reserve / unavailable / reject`.

### Frozen future screen counts

If every lane fills to its maximum, the admission screen may later use at most:

- image: 4 × 12 = **48** outputs;
- general video: 5 × 12 = **60**;
- native AV: 4 × 12 = **48**;
- lip-sync: 3 × 8 = **24** transformations;
- TTS: 3 × 8 = **24** audio outputs;
- **hard maximum = 204 outputs** before retries; retries must be budgeted separately and predeclared.

### Frozen future deep-qualification caps

Top <=2 workflows per lane:

- image: 2 × 40 items × 2 repeats = **160**;
- general video: 2 × 30 × 2 = **120**;
- native AV: 2 × 36 × 2 = **144**;
- lip-sync: 2 × 12 × 2 = **48**;
- TTS: 2 × 12 × 2 = **48**;
- **hard maximum = 520 generated/processed outputs**.

### Cost forecast

Produce two forecasts from exact current prices:

1. admission screen max under roster actually available;
2. deep qualification max under top-two-per-lane assumption.

Also estimate evaluator-call cost separately; do not hide evaluator cost inside generation cost.

No external generation/evaluation calls tonight.

### Deliverables

- `eval/v1/MODEL-WORKFLOW-INVENTORY-2026-08-26.md`
- `eval/v1/model-workflow-inventory-2026-08-26.yaml`
- `eval/v1/COST-FORECAST-PRE-RUN.md`

## 5. E3 — Six evaluator-family qualification specifications

### Families

1. text/OCR;
2. deterministic/CV geometry;
3. structured visual VLM;
4. temporal/video evaluator;
5. speech/audio/AV evaluator;
6. creative/commercial evaluator.

### General qualification rule

A model/workflow score may name an instrument only when that exact instrument configuration has a qualification record for the relevant judgement family and conditions. `required_but_no_calibrated_instrument` is a valid Registry state.

Do not apply one family's thresholds to another merely for uniformity.

### Family-specific material targets to design around

#### 1. Text/OCR

- integrate existing authoritative **96-item Devanagari battery** as already frozen;
- preserve current zero-false-pass principle for exactness checking where applicable;
- define a separate Latin exact-text calibration pack, preferably deterministic and human-auditable, without mutating the Devanagari pack;
- explicitly separate ability to **read real text** from ability to judge **generated text defects**.

#### 2. Deterministic/CV geometry

- construct at least **100 synthetic known-answer fixtures** spanning count, bounding/relative position, aspect/duration and simple attribute/relationship checks;
- no human label needed where truth is generated deterministically;
- fail closed on unsupported file/parse states.

#### 3. Structured visual VLM

Design qualification around the shared product/person controlled reference packs:

- >=48 product refs;
- >=32 person refs;
- include known-match, known-nonmatch and controlled-preservation/edit cases;
- define what requires human adjudication rather than pretending identity similarity is exact.

#### 4. Temporal/video

Use clean clips plus deterministic perturbations where possible. Qualification pack should include known temporal discontinuity, identity swap/drift, text/logo instability and continuity perturbations. Define clip-level observation rules.

#### 5. Speech/audio/AV

Use the planned **24 single-speaker + 12 two-speaker clean AV clips** with transcripts/turns. Define deterministic perturbations such as known audio shifts, speaker-channel/turn swaps, transcript mismatch and controlled prosody variants where feasible. Never invent a millisecond tolerance without evidence; propose calibration curves first.

#### 6. Creative/commercial

Use Resources' planned **60 active commercial assets** with **fresh independent human review later**. Do not treat public/source preference labels as our creative truth. Specify pairwise or issue-detection protocol and false-criticism measurement.

### Tonight deliverables

- `eval/v1/instruments/QUALIFICATION-MASTER-SPEC.md`
- one family spec per instrument family;
- `eval/v1/instruments/RESOURCE-REQUESTS.yaml` exactly matching or explicitly proposing changes to the shared Resources contract;
- qualification-result schema and dummy records;
- no qualified status tonight.

## 6. E4 — 100-base-item reusable benchmark bank design

### Exact bank size

**40 atomic + 60 compound = 100 distinct base items.**

Repeats are never base items.

### Atomic 40

Use exactly these family counts unless E1 proves a material invalidity and the Controller Brief records it:

- exact text, Latin + Devanagari: **10**;
- count / attribute / spatial: **6**;
- identity / reference / preservation: **6**;
- anatomy / human-object interaction: **6**;
- motion / camera / physics: **6**;
- speech / lip-sync / speaker assignment: **6**.

### Compound 60

**10 scenario families × 6 benchmark items**:

1. typography-led commercial image;
2. product packshot;
3. person + product static ad;
4. reference-based campaign edit;
5. product-hero video + external VO/no visible speech;
6. actor + product, no visible dialogue, external VO;
7. one visible speaker;
8. two-person dialogue;
9. product handoff/action sequence;
10. multi-shot branded 6–20 sec ad.

These are capability benchmark scenarios, not the Canon 30 customer briefs. They may use controlled synthetic/reference conditions. Later E9's 12 end-to-end commercial briefs must come from Canon's bank.

### Measurement economy requirement

Every compound item must declare a **measurement fan-out list**: all dimensions that can validly score the same generated asset. The harness must never regenerate merely because another listed dimension is evaluated.

### Coverage target

For every **critical capability that is semantically testable in this bank**, provide >=10 distinct base-item opportunities across atomic + compound items. If a capability cannot reach 10 because it applies only to a narrower lane, record the exact denominator and reason instead of padding with fake items.

### Deliverables

- `eval/v1/bank/master-bank-v1.jsonl` or fully specified manifest template with frozen ids;
- `eval/v1/bank/MEASUREMENT-FANOUT.csv`;
- `eval/v1/bank/COVERAGE-REPORT.md`;
- no media generation tonight.

## 7. E5 — Generate-once harness + empty Registry/storage interface

### Required pipeline

```text
frozen item manifest
    -> one generation/transform call
    -> immutable output artifact + provenance
    -> evaluator fan-out by eligible dimension
    -> dimension results
    -> failure co-occurrence
    -> operational metrics
    -> Registry measurement rows
```

### Required invariants

- one trial asset id has exactly one generation provenance record;
- several evaluator results may point to that same trial asset;
- rerun/retry is a new attempt id, never silent replacement;
- frames extracted from one clip preserve parent-trial id;
- all Registry rows point to exact instrument configuration/calibration ref;
- result absence distinguishes `not_applicable`, `not_measured`, `instrument_unqualified`, `generation_failed`, `refused`;
- costs separate generation/transform/evaluator components;
- no routing score/weight is computed;
- Registry starts empty of empirical model results.

### Storage handoff

Expose an artifact manifest Resources can later archive. Required fields include:

- trial/attempt id;
- item id;
- provider/model/version/endpoint/workflow;
- input/ref hashes;
- prompt/config hash and recoverable config path;
- seed/settings if available;
- timestamps;
- output hash/path;
- cost components;
- API status/error/refusal;
- evaluator-result refs.

### Verification tonight

Use dummy/synthetic local fixtures only. Demonstrate:

1. one dummy video scored by >=3 fake/deterministic evaluator adapters without regeneration;
2. retry creates new attempt rather than replacing output;
3. parent-child frame provenance holds;
4. duplicate-regeneration guard fires;
5. an unqualified instrument cannot produce a trusted Registry row;
6. empty Registry schema validates.

### Deliverables

- implementation under `eval/v1/harness/` or integration with existing harness without breaking old evidence;
- `eval/registry/SCHEMA-v1-draft.yaml` or a clearly versioned compatible extension of the approved V0 storage basis;
- empty `eval/registry/registry-v1.jsonl` is permitted only if repository convention benefits; do not populate it with fake results;
- tests and verification log.

## 8. Later empirical tasks

### E6 instrument qualification

Requires Resources packs and, where specified, human reference judgements. No generator capability benchmarking until the necessary instrument is qualified.

### E7 admission screen

Vendor claim gives admission to testing, never a score. Run lane items round-robin. If budget truncates, truncation must be predeclared/uniform rather than quality-driven.

### E8 deep qualification

Top <=2 per lane based on predeclared screen rule. Two repeats per item. Reuse every asset across all eligible dimensions. Write evidence-backed Registry measurements.

### E9 production workflow benchmark

Select 12 briefs from Canon's accepted 30-bank after integration. Compare <=4 **complete recipes**, not just base models. 12 × 4 × 2 <=96 trials. Measure hard pass, creative acceptance, retries, manual intervention, latency, total cost and CpAO.

### E10 maintenance

New serious model -> admission suite. Provider/version change -> affected retest. Monthly -> active workflow regression. Quarterly -> broader qualification. Production failure -> permanent regression case where rights/provenance allow.

## 9. Autonomous decisions tonight

Eval may decide:

- exact capability definitions/levels within the frozen 36;
- which official current endpoints fill roster slots under the lane caps;
- exact measurement fan-out of benchmark items;
- deterministic fixture design;
- harness implementation details;
- proposed family-specific qualification gates, provided evidence/rationale is explicit and no gate is misrepresented as empirically established.

Eval may **not**:

- call paid generation/checker APIs;
- spend money;
- qualify an instrument without running its approved protocol;
- write empirical Registry model scores;
- create independent competing commercial briefs for E9;
- alter Canon/Resources files;
- implement routing/Planner;
- merge to main.

## 10. Stop conditions

Stop the affected package and document rather than ask the user overnight if:

- a capability cannot be defined without crossing Canon/Planner scope;
- official model version/access/pricing cannot be pinned;
- credential visibility would require exposing a secret;
- a measurement requires a resource or human reference that does not exist;
- the current harness must be destructively changed to proceed;
- another stream's file must be edited;
- an external call would incur cost or create empirical evidence.

Continue independent packages when safe.

## 11. Morning Controller brief

Create `eval/findings/EVAL-V1-OVERNIGHT-CONTROLLER-BRIEF.md` containing:

1. E1–E5 attempted/completed status;
2. 36-capability contract summary;
3. current model/workflow roster with availability/access gaps;
4. exact later admission/deep-qualification call counts and live cost forecast;
5. six instrument families and what is qualified vs still only specified;
6. 100-item bank coverage summary;
7. harness verification evidence;
8. Resources requests/cross-stream dependencies;
9. files/commits;
10. explicit confirmation of **₹0 paid API spend and 0 empirical Registry entries**.
