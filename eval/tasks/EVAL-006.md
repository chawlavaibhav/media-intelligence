# Task EVAL-006: Checker qualification and Capability Registry bootstrap

**TASK ID:** EVAL-006
**OBJECTIVE:** Qualify at least one trustworthy Devanagari checker, instantiate the first empirical Capability Registry, and write the first current generator/workflow capability entries under a bounded frozen run.

**WHY WE ARE DOING THIS:** Eval has built measurement infrastructure but has never benchmarked a generator and the Capability Registry does not yet exist. This task converts the validated EVAL-005 instrument work into the project's first current empirical routing evidence while preserving the broader production-capability mission.

**COMMUNICATION STANDARD:** inherits `shared/COMMUNICATION-STANDARD.md`; explain technical ideas in plain English, including what they mean, why they matter and their practical consequence; use minimum sufficient wording without sacrificing understandability; do not invent; separate evidence from inference.

## INPUTS

Read only what is needed from:

- `PROJECT-MEMORY.md`
- `coordination/PROJECT-CONTRACT.md`
- `coordination/decisions/CONTROLLER-POST-AUDIT-UNBLOCK-2026-08-25.md`
- `eval/CHARTER.md`
- `eval/HANDOFF.md`
- `eval/battery/CAPABILITY-BATTERY-V0-DRAFT.md`
- `eval/battery/CAPABILITY-LAB-V0-PLAN.md`
- `eval/battery/CAPABILITY-REGISTRY-SCHEMA-V0-DRAFT.yaml`
- `eval/battery/devanagari-exactness/METRICS-AND-QUALIFICATION.md`
- `eval/battery/devanagari-exactness/human-validation/HUMAN-VALIDATION-RECORD.md`
- the authoritative 96-item validated battery artifacts named by that record
- official provider API/model/pricing documentation checked on the run date

## IN SCOPE

### Phase A — qualify the judge before trusting model scores

Approved checker candidates:

1. OpenAI **GPT-5.6 Luna**
2. Google **Gemini 3.7 Flash**
3. Anthropic **Claude Sonnet 5**
4. Alibaba **Qwen3-VL-32B-Instruct**

Before any paid call, record the exact API model identifier/version, availability and current price from the provider's official documentation. Do not use marketing summaries or old repository prices as the rate source.

Run the authoritative **96-item** EVAL-005 battery in **both checker shapes**.

Qualification gates are Controller-approved for this first run:

- zero false passes;
- false-fail rate <= 10%;
- refusal rate <= 5%;
- repeat consistency >= 0.95 across at least 3 full passes in both shapes.

A screening pass may count as pass 1 only if model version, prompts, parameters, scoring code and input bytes remain exactly unchanged. Any mutation creates a new run and cannot be pooled with the old one.

If a checker is unavailable, record `unavailable` and continue with the remaining approved candidates. Do not substitute another checker without Controller approval.

If **no checker qualifies**, STOP after freezing the evidence. Do not benchmark generators with an unqualified judge.

### Phase B — instantiate Registry V0

Proceed only if at least one checker qualifies.

Create an Eval-owned Registry implementation based on `CAPABILITY-REGISTRY-SCHEMA-V0-DRAFT.yaml`.

Approved boundary:

- measurement, provenance, instrument, cost, reliability, failure co-occurrence and freshness fields may be stored;
- proposed cross-stream fields may be retained as evidence-bearing metadata;
- they carry **no approved Production Planner/routing weighting semantics yet**;
- no scored entry may use an instrument whose calibration status is unqualified.

The first Registry must visibly distinguish measured capability from `required_but_no_calibrated_instrument` rather than silently omitting unmeasurable properties.

### Phase C — first current generator/workflow measurements

This is a **bootstrap**, not an exhaustive model ranking and not yet a production-routing licence.

Approved model/workflow roster for this task:

**Image generation, Runway API route**
- `seedream5_pro`
- `gpt_image_2`
- `gemini_image3_pro`

**Video generation**
- Runway `veo3.1`
- Runway `seedance2`
- Runway `gen4.5`
- Alibaba Model Studio `wan2.7` using an official current text/image-to-video endpoint as appropriate

Use only legitimately available configured credentials. Missing access to one approved workflow does not block the others; record the cell as unavailable. Do not silently replace a model version. In particular, **Seedance 2.5 and Wan 3.0 are not authorised substitutions inside this frozen run**; newer versions require a new admission/retest task once their API route is verified.

#### C1 — image: `exact_text_devanagari`

Run Levels 1–3 from the approved D1 ladder.

Freeze a deterministic item manifest before the first generation:

- **Level 1:** 8 distinct human-accepted base words from the authoritative 48-word pool, selected deterministically and spread across the available script/failure groups as evenly as possible.
- **Level 2:** 8 controlled three-word Devanagari lines constructed deterministically from distinct accepted base words. These are controlled exact-copy stimuli; do not claim they measure natural-language quality.
- **Level 3:** the same 8 Level-2 strings placed into one fixed in-scene signboard/packaging template, so the only added stressor is in-scene rendering.
- **Repeats:** 2 generations per item per model. Repeats measure reproducibility, not independent breadth.

Use the same semantic prompt and conditions across models except syntax changes strictly required by the provider API. A provider-specific prompt optimisation is a different workflow and is out of scope.

#### C2 — video: `text_stability_across_frames`

Run only the currently measurable Devanagari levels:

- **Level 2:** 4 fixed Devanagari target lines from C1, static camera/static sign.
- **Level 3:** the same 4 targets with the approved added camera-or-subject-motion stressor.
- **Repeats:** 2 clips per item per workflow.

All sampled frames from one clip are **one trial**. Record correctness and cross-frame stability separately, as required by D5.

Do **not** run the Latin Level 1 until its checker is separately calibrated.

#### C3 — operational behaviour

For every generation/evaluation call, record the approved D6 information: exact provider/model/version, price source and date, cost, latency, API errors, refusals/moderation blocks and repeat behaviour.

### Phase D — preserve the broader production mission

Create a short capability-readiness matrix from the original `CAPABILITY-LAB-V0-PLAN.md` showing each planned capability family as one of:

- measured in Registry now;
- instrument exists but needs calibration;
- required but no calibrated instrument;
- deferred/not yet designed.

The matrix must explicitly retain: product identity, person identity across shots/sessions, reference conditioning, human-object interaction, motion/physics, logo fidelity, **speech/lip-sync (English, Hindi, emotional, two-speaker)**, and operational behaviour. This is a coverage control, not permission to test those dimensions in EVAL-006.

## OUT OF SCOPE

- changing any approved battery dimension, difficulty ladder or pass criterion after seeing results;
- creative-fitness / Evaluation-B scoring;
- Production Planner or routing implementation;
- adding any unapproved checker, generator, vendor or model version;
- Seedance 2.5 or Wan 3.0 substitution inside this run;
- speech/lip-sync, multi-speaker, product-identity, logo-fidelity or human-object-interaction benchmarking;
- new Resources acquisition;
- using published benchmark scores or vendor claims as our capability result;
- claiming a small bootstrap cell is production-qualified or exhaustive.

## DELIVERABLES

- `eval/runs/EVAL-006-CHECKER-QUALIFICATION.md` plus frozen raw run artifacts
- `eval/registry/SCHEMA-v0.yaml`
- `eval/registry/registry-v0.jsonl` — first evidence-backed entries only
- `eval/registry/PRODUCTION-CAPABILITY-READINESS.md`
- frozen generation item manifest(s) under `eval/battery/` or `eval/runs/`, clearly versioned
- `eval/tasks/EVAL-006-CONTROLLER-BRIEF.md`

Every Registry row must point to its frozen run evidence and exact instrument calibration reference.

## AUTONOMY MODE

**autonomous**, only within the frozen roster, item-construction rules, gates and budgets above.

## RESOURCE BUDGET

- **sources/items:** no new external dataset acquisition; use existing approved battery/resources only
- **storage:** keep generated/evaluation artifacts bounded; do not commit large media if existing repository policy places them outside Git
- **checker API spend:** maximum **₹4,000**
- **generator + evaluation spend after checker qualification:** maximum **₹12,000**
- **total external API spend:** maximum **₹16,000**
- **generation cap:** maximum **260 generated images/clips total**, including retries; do not exceed the lower of the generation cap or spend cap
- **human specialist time:** ₹0 / 0 new specialist hours authorised in this task

Before Phase C, calculate the full run's live-price forecast. Execute model cells in round-robin order rather than finishing one vendor first, so an unexpected budget stop does not leave a cherry-picked comparison. If forecast exceeds the cap, reduce **repeats/items by one predeclared uniform rule across all comparable cells before starting**, record the rule, and never trim cells after seeing quality results.

## APPROVED DEPENDENCIES

- EVAL-005 validated 96-item view and frozen human-validation record
- Controller decision `coordination/decisions/CONTROLLER-POST-AUDIT-UNBLOCK-2026-08-25.md`
- Capability Battery V0 approved measurement design
- Resources corpus and lineage findings already merged on `main`

## STOP CONDITIONS

Stop and return to Controller if any of the following occurs:

- no checker qualifies;
- a checker/model version cannot be pinned or changes during the run;
- live-price forecast cannot fit the approved cap under one uniform pre-run reduction rule;
- an evaluator prompt, pass criterion, item definition or model-specific prompt would need changing after seeing results;
- a required input is unavailable in a way that changes the experiment rather than simply marking one approved cell unavailable;
- integrity/hash checks fail;
- a result would require treating an uncalibrated instrument as trusted;
- any cross-stream architecture change becomes necessary.

## HUMAN APPROVAL TRIGGERS

Controller approval is required for any new model/vendor, any spend increase, any new battery dimension, any threshold change, any change to the generation-item design after results are visible, or any proposal to make Registry data operationally control routing.

## RESULT LOCATION

Primary review surface: `eval/tasks/EVAL-006-CONTROLLER-BRIEF.md` on the EVAL-006 work branch, with exact commit SHA and links to frozen run/Registry artifacts.
