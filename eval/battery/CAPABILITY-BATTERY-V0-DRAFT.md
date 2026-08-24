# Capability Battery V0

**Task:** EVAL-001 (revision 3) · **Date:** 24 Aug 2026
**Status: CONTROLLER-APPROVED as the V0 battery specification.** EVAL-001 is closed.

The dimensions, difficulty levels, observation units, trial definitions, pass criteria and required
instruments below are approved as the V0 design. Changing any of them after results are seen is an
EXPERIMENT MUTATION stop under `shared/AUTONOMY-POLICY.md`.

**Still unapproved and out of scope of this approval:** the workflow/model roster, the human-time
budget, and the Registry's cross-stream field proposals. **No benchmark run is authorised by this
document** — a run requires a separate approved task, and the instrument calibrations in
`INSTRUMENT-CALIBRATION-PLAN-V0.md` must pass first.

**Zero generations were made in producing this document. No model was benchmarked. ₹0 spent.**

---

## 1 · What this document is

A specification for *how the Capability Lab measures*, so that a later approved run produces
numbers that can be defended, reproduced, and correctly interpreted a year from now.

It defines, per dimension: the property being measured, the unit that must be observed to see it,
what counts as one trial, what counts as a pass, which instrument produces the verdict, and what
that instrument's calibration status currently is.

**What it is not.** Not a Registry. Not a score. Not a model recommendation. Not a list of
approved vendors. Not an exhaustive account of what matters — see §4 for what is deliberately
absent.

---

## 2 · Scope decision: hard-fidelity and operational only

Per Controller clarification 2, V0 measures **Evaluation-A** properties (hard fidelity) plus
operational behaviour. Creative-fitness measurement (**Evaluation-B**) is out of scope for
EVAL-001 and will be designed separately once the relevant Canon work is ready.

This is a deliberate choice with three consequences that must be stated rather than discovered
later:

1. **V0 cannot bear on assumptions 6b or 15.** Whether explicit Canon improves creative
   evaluation, and whether Canon-derived requirements improve routing, are untouched by this
   battery. A passing V0 score means "the hard constraints held," never "the asset is good."
2. **A V0-complete asset can still be commercially worthless.** Every hard constraint can pass
   while the hierarchy fails, the proposition is unclear and the emotional target is missed.
3. **Absence here is not a judgement of importance.** §4 exists so this cannot be misread.

The justification for starting here: A-side properties have deterministic or empirically
testable instruments, they map to `strength: hard` and `exactness: exact` fields that SPEC-01's
acceptance contract *requires* to be verifiable, and two of them are where we already hold
observed failures.

---

## 3 · Evidence classes and provenance

Per Controller clarification 3, a dimension may enter this draft on **any one** approved evidence
class. No two-source rule is imposed. Every dimension records its provenance and the strength of
that justification.

| Class | Meaning |
|---|---|
| `PUB` | published benchmark methodology, cited with source and access date |
| `IR` | a current Creative IR requirement at an exact SPEC-01 path |
| `OBS` | an observed production failure already recorded in our material |

**Strength** is recorded as `direct` (the evidence names this property) or `adjacent` (the
evidence names a closely related property and the extension is ours, stated as such).

Sources are listed in full in `eval/findings/EVAL-001-battery-design-findings.md` §7.

---

## 4 · Deliberately deferred dimensions

Recorded so that absence is never mistaken for irrelevance (Controller clarification 2).

| Deferred dimension | Class | Why deferred from V0 |
|---|---|---|
| Creative hierarchy — does attention land in the intended order | B-side | needs Canon-informed evaluator; clarification 2 |
| Proposition clarity / objective fit | B-side | needs Canon + real advertising corpus (RES-001) |
| Emotional target achieved | B-side | `verification.mode: unresolved` in SPEC-01's own example |
| Composition quality — framing, depth, figure-ground | B-side | `StaticCreativeExtension.composition` is a craft judgement, not a hard constraint |
| Temporal hierarchy — does attention evolve correctly across beats | B-side | needs `VideoCreativeExtension.temporal_hierarchy` consumption |
| Logo & brand-mark fidelity | A-side | no calibratable instrument identified; COCO-class detectors do not cover brand marks. See §7.4 |
| Human-object interaction (holding, using, manipulating) | A-side | `relationships[]` is checkable in principle; no calibrated instrument found in the review |
| Speech, Hindi dialogue, lip sync | A-side | `VideoCreativeExtension.dialogue_intent`; distinct capability from on-screen script, distinct instruments, not affordable in V0 |
| Reference conditioning strategy (1 ref vs many vs ref+style) | A-side | this is a Production IR variable; Production IR does not exist |
| Identity across *shots* and across *sessions* | A-side | observation units `sequence` and `asset_set_over_time` at higher cost; V0 covers across-prompts only |
| Moderation / refusal behaviour by content class | operational | needs a deliberately provocative prompt set; policy question for Controller |

Two of these — logo fidelity and human-object interaction — are **observed failure areas**
(`nano_arms-crossed_t0` "logo floating mid-air", `nano_sign_t1` "board occludes body oddly",
`nano_server-room_t0` "bg logos mirrored", `seedream_poster_t2` "wordmark missing"). They are
deferred for lack of an instrument, **not** for lack of evidence that they matter. This is
exactly the case the Registry's proposed `required_but_no_calibrated_instrument` state exists to
record (see schema §`instrument_state`).

---

## 5 · Core measurement concepts

### 5.1 Property vs instrument

The **property** is what must be true of the asset. The **instrument** is the machinery that
produces a verdict about it. They are separate, they fail independently, and a Registry number is
a joint statement about the model *and* the instrument.

This is not theoretical. FINDINGS-01 records one VLM returning `exact_match: true,
edit_distance: 0` on six frames that a second VLM scored at edit distance 1–2 against the same
target string. I re-read the raw run files at
`eval/runs/finding-01-devanagari-check/` and confirm the pattern is as recorded.

**Rule:** no Registry entry without `instrument` and `instrument_calibration_ref`.

### 5.2 Gate accuracy vs diagnostic accuracy

An instrument has **two** accuracies and they are not interchangeable:

- **Gate accuracy** — does it correctly say pass/fail? Consumed by routing.
- **Diagnostic accuracy** — does it correctly say *what broke*? Consumed by repair and by
  Empirical Memory.

FINDINGS-01 is precise about this: Qwen3-VL is recorded as 14/14 on **verdicts**, while the same
finding records that it "caught सुबह→सुवह but silently corrected चाथ→चाय" — verdict right,
diagnosis incomplete. Any downstream citation that reduces this to a bare "14/14" reads as a
general accuracy claim and would be wrong. Both accuracies must be calibrated and stored
separately.

### 5.3 Observation unit

Some defects are **invisible** at the wrong unit — not hard to see, structurally undetectable.
`canon/knowledge/migration/AUDIT-grammar-of-the-shot.md` records `gos_005`
(`line_violation_is_invisible_until_assembly`) as the source case, and
`canon/knowledge/SPEC-04-operational-bindings.md` §`observation_unit` already defines the
vocabulary. **This battery adopts SPEC-04's vocabulary unchanged and invents nothing:**

```
frame | shot | shot_pair | sequence | whole_asset | asset_set_over_time
```

Our own data confirms the lesson independently. In `frame_wan_*`, the sign is misspelled in
every frame, but the *drift* — सुवह की in frames 1–4, सुवह के in frames 5–6 — exists only
*between* frames. FINDINGS-01 could record it only as an "incidental finding" because the
instrument was frame-level.

**Rule:** every dimension declares its observation unit. Declaring it too narrow does not degrade
accuracy — it makes a defect class undetectable while the report reads clean.

### 5.4 Trial unit — and the correlation rule

This was undefined in `CAPABILITY-LAB-V0-PLAN.md` ("20 trials" could mean 20 prompts, 20 seeds of
one prompt, or 20 frames — three different experiments). Proposed definitions:

- **Item** — one distinct prompt-instance with fixed conditions. Items are the unit of
  independence.
- **Trial** — one generation of one item. `trials = items × repeats`.
- **Repeat** — a re-generation of the *same* item under a different seed. Repeats measure
  **reproducibility**, not capability breadth.
- **Observation** — one application of the instrument. A `sequence`-unit trial yields one
  observation computed over many frames, **not** many observations.

**Correlation rule (binding):** frames drawn from one generated clip are **one trial**, never N.
Repeats of one item are **not** independent items. Any pass rate must report `n_items` alongside
`n_trials`, and confidence must be computed on `n_items`.

Why this is not pedantry: FINDINGS-01's 14 samples come from **4 independent sources**; 12 are
correlated frames from 4 clips. Treating them as 14 independent observations overstates
confidence roughly threefold. The finding says so itself under "Limits of this result."

### 5.5 Difficulty level — operational definition rule

`CAPABILITY-LAB-V0-PLAN.md` names ladder rungs but never defines what makes a level harder.
Proposed rule:

> **Level N+1 = level N plus exactly one named, independently observable stressor.**

One stressor per step, named in the level definition, so that (a) a sample can be audited into
the right level by someone who did not write it, and (b) when a model fails at level 3 but passes
at level 2, the *specific* thing it cannot do is already isolated.

V0 runs levels 1–3. Level 4 rungs are written where the ladder is known, and not run.

### 5.6 Pass criterion

Every dimension states its criterion as a decidable predicate over the instrument's output.
Where a criterion has a tolerance, the tolerance is part of `conditions` and moves the entry to a
different Registry row if changed. **A pass criterion may never be adjusted after seeing results**
— Autonomy Policy stop condition 8.

---

## 6 · Dimensions

Notation per dimension: `id`, provenance, observation unit, item design, ladder, pass criterion,
instrument, instrument state.

`approval_status` distinguishes dimensions traceable to the V0 scope already in
`CAPABILITY-LAB-V0-PLAN.md` from **proposed additions**, which require a Controller decision under
the task's HUMAN APPROVAL TRIGGERS. Cost is given both ways in §8.

---

### 6.1 · D1 — `exact_text_devanagari`

**approval_status:** `traced_to_plan_v0`

**Property.** On-screen copy in Devanagari script renders as the exact specified string.

**Provenance.**
- `IR` `direct` — `copy.headline.exactness = exact`; `copy.script_system = devanagari`;
  `audience.language.on_screen_copy`. All three are defined paths in SPEC-01 v0.1.
- `OBS` `direct` — `still_seedream_headline` (gibberish); `frame_wan_*` (character
  substitution); FINDINGS-01 throughout.
- `PUB` `adjacent` — MULTITEXTEDIT (2026) establishes the *method* for script-fidelity scoring
  across languages. It does **not** cover Devanagari. See §7.1 and findings §3.

**Observation unit:** `frame`.

**Item design.** Each item = one target string + one scene context. Strings drawn from a
proprietary Devanagari string set (see §9, media requirement M1) covering: simple CV syllables,
conjuncts (संयुक्ताक्षर), i-matra and u-matra vowel signs, nukta-bearing characters, and the
ब/व and य/थ pairs we have already observed being confused.

**Ladder.**

| Level | Added stressor | Example |
|---|---|---|
| 1 | none — baseline | single word, plain rendering, high contrast |
| 2 | +multi-word line | 3–5 word phrase, one line |
| 3 | +in-scene surface | same phrase painted on a signboard/packaging within the scene |
| 4 *(not run in V0)* | +perspective/occlusion | signboard at an angle or partly occluded |

**Pass criterion.** `normalize(transcription) == normalize(target)` under NFC normalisation with
whitespace and ZWJ/ZWNJ collapsed, as already implemented in `eval/scripts/check-vlm.mjs`.
Character edit distance is recorded alongside as the diagnostic, never as the gate.

**Instrument.** Two-stage `transcribe-then-compare`:
1. VLM transcribes what is drawn, explicitly instructed not to correct spelling. The existing
   prompt in `check-vlm.mjs` already does this, and MULTITEXTEDIT's LSF metric independently
   arrived at a two-stage trace-then-judge protocol — convergent design, recorded in findings §2.
2. Deterministic normalisation + comparison.

**Note the split:** step 2 is deterministic and needs no calibration. Step 1 is the entire
uncertainty. Only step 1 gets calibrated.

**instrument_state:** `provisional_uncalibrated`. Per Controller clarification 4, the existing
Devanagari checker result is treated as **preliminary**: native-speaker confirmation is
unresolved and the sample is correlated. Requirements to promote it are in
`INSTRUMENT-CALIBRATION-PLAN-V0.md` §3.1. **No V0 Registry entry may be written from this
instrument until that calibration passes.**

---

### 6.2 · D2 — `exact_text_latin` *(control)*

**approval_status:** `controller_approved_v0` — approved for V0 by Controller, 24 Aug 2026.

**Property.** Identical to D1, Latin script.

**Why propose it.** Without a same-model Latin baseline, a Devanagari failure rate is
uninterpretable: we cannot separate "this model is bad at rendering text" from "this model is bad
at *Devanagari*." MULTITEXTEDIT's entire design is a per-language delta against English for
exactly this reason, and it reports script-fidelity degradation (∆LSF) as the headline quantity
rather than absolute score. Routing needs the delta: if a model is uniformly bad at text we
composite; if it is specifically bad at Devanagari we can still use it for Latin copy.

**Provenance.** `PUB` `direct` (MULTITEXTEDIT delta-vs-English design); `IR` `direct`
(`copy.headline.exactness`, `audience.language.on_screen_copy` with Latin script);
`OBS` `adjacent` (`nano_sign_t0/t2/t3` recorded "headline exact" — Latin passes we hold).

**Observation unit:** `frame`. **Ladder, pass criterion:** as D1, Latin strings matched for word
count and character count.

**Instrument.** Same two-stage protocol. **instrument_state:** `requires_calibration` — cheaper
than D1's, because ground truth needs no specialist reader and deterministic OCR is a viable
second opinion for Latin (it is not for Devanagari — FINDINGS-01 records Tesseract failing
completely, though see findings §5 on that claim's evidence).

---

### 6.3 · D3 — `person_identity_across_prompts`

**approval_status:** `traced_to_plan_v0`

**Property.** A person entity's declared invariants hold across separately generated images
produced from one reference set.

**Provenance.**
- `IR` `direct` — `entities[].invariants` and `entities[].allowed_variation`, both defined in
  SPEC-01 v0.1.
- `OBS` `direct` — `nano_chai_t3` "face drift — younger, streak moved"; `nano_server-room_t2`
  "blazer color split"; `nano_server-room_t3` "outfit changed to pants".
- `PUB` `direct` — DreamBench++ (2024) for the evaluation protocol.

**Observation unit:** `asset_set_over_time` (SPEC-04 vocabulary). The defect does not exist in
any single image; it exists across the set. A per-image instrument cannot see it.

**Item design.** One item = one reference set + N distinct prompts + a declared invariant list
and allowed-variation list. **Both lists are mandatory.** The plan's ladder referenced only
invariants; without `allowed_variation`, "the blazer changed colour" and "the lighting changed
the apparent shade" are indistinguishable and the criterion is undecidable.

**Ladder.**

| Level | Added stressor |
|---|---|
| 1 | 2 prompts, same setting, same wardrobe intent |
| 2 | +setting change across prompts |
| 3 | +pose/action change across prompts |
| 4 *(not run in V0)* | +wardrobe change intended, identity must still hold |

**Pass criterion.** Every declared invariant holds across all images in the set. A change in a
field listed under `allowed_variation` is **not** a failure. One invariant violated = item fails;
the violated invariant is recorded by name, and **multiple invariants may be recorded as
violated on the same item** (Project Contract separation 13).

**Instrument.** VLM judge with a structured per-invariant rubric, scoring each invariant
separately rather than issuing a holistic similarity score.

**Why not DINO/CLIP-I embedding similarity** — the obvious cheap choice, rejected on published
evidence. DreamBench++ reports concept-preservation human alignment of **50.72% for DINO** versus
**83.31% for a structured GPT-4o evaluator**, and concludes DINO "prioritize[s] overall shape and
color over detailed features, making them suboptimal for evaluating personalized image
generation." Our invariants are precisely detailed features — a hair streak's position, a
colourway. An embedding metric would have scored `nano_chai_t3` as a pass.

**instrument_state:** `requires_calibration`. Highest human cost in V0; see calibration plan §3.3.

---

### 6.4 · D4 — `object_count`

**approval_status:** `traced_to_plan_v0` (split from the plan's merged dimension — see note below)

**Property.** The specified number of the specified object appears.

**Split rationale.** `CAPABILITY-LAB-V0-PLAN.md` merged counting and placement into one dimension.
Both published sources separate them — GenEval has distinct `counting` and `position` tasks;
T2I-CompBench++ separates generative numeracy from 2D/3D-spatial relationships — and they fail
independently: a model can place two objects correctly and produce three of them. They also need
**different detector settings**: GenEval uses confidence 0.9 for counting and 0.3 elsewhere, so a
single dimension could not carry one honest `conditions.detector_confidence`. Shared detector
infrastructure, **separate capability results**.

**Provenance.** `PUB` `direct` — GenEval `counting`, T2I-CompBench++ numeracy. `IR` `direct` —
`creative.hierarchy` `element_ref` resolution requires referenced entities to exist and be
countable. `OBS` `direct` — `nano_desk_t3` "two laptops".

**Observation unit:** `frame`.

**Ladder.**

| Level | Added stressor |
|---|---|
| 1 | exactly 2 of one object type |
| 2 | +count raised to 3 or 4 |
| 3 | +a second object type present at its own specified count |
| 4 *(not run in V0)* | +count under partial occlusion |

**Pass criterion.** Detector instance count equals the specified count for each named type, at
`conditions.detector_confidence = 0.9`.

**Instrument.** Mask2Former (Swin-S, COCO instance segmentation), counting configuration.

**instrument_state:** `published_calibration_available, local_confirmation_required`.

---

### 6.4b · D4b — `spatial_relationship`

**approval_status:** `traced_to_plan_v0` (split from the plan's merged dimension — see §6.4)

**Property.** Two specified objects stand in the specified spatial relation.

**Provenance.** `PUB` `direct` — GenEval `position`; T2I-CompBench++ 2D/3D-spatial. `IR` `direct` —
`relationships[]` (subject / relation / object). `OBS` `adjacent` — `nano_sign_t1` "board occludes
body oddly" is a contact/occlusion failure; V0's predicate vocabulary does not yet cover contact,
so this observation motivates the dimension without being scorable at V0 (see limits below).

**Observation unit:** `frame`.

**Ladder.**

| Level | Added stressor |
|---|---|
| 1 | 2 objects, one 2D relation (left of / right of / above / below) |
| 2 | +depth relation (in front of / behind) |
| 3 | +relation holding while both objects are also count-constrained |
| 4 *(not run in V0)* | +contact relations (holding, resting on) |

**Pass criterion.** Detector bounding-box geometry satisfies the rule-based predicate for the
specified relation, at `conditions.detector_confidence = 0.3`.

**Limits, stated rather than discovered later.** Bounding-box geometry expresses *relative
position* well and *contact* not at all. "Is the person actually holding it?" — the question
SPEC-01's `relationships[]` most wants answered — is **not** decidable from boxes, and no
calibrated instrument for it was found. Contact relations stay at level 4, unrun, and human-object
interaction remains in §4 as `required_but_no_calibrated_instrument`.

**instrument_state:** `published_calibration_available, local_confirmation_required` — GenEval
reports **83% agreement with annotators against 88% inter-annotator agreement**, rising to **91%
on images annotators unanimously agree on**, using Mask2Former (Swin-S, COCO) at confidence 0.3.

**Scope restriction shared by D4 and D4b — the honest limit.** GenEval's authors record that the
detector is confined to MS COCO's 80 classes, merges bounding boxes for overlapping same-class
objects, mis-segments objects with holes, and degrades on out-of-distribution imagery such as clip
art. Our real subjects are branded products and wordmarks, which are not COCO classes. **V0
therefore restricts both dimensions to COCO-representable generic objects.** Brand-mark counting
and placement is deferred (§4) with `required_but_no_calibrated_instrument`. Presenting a
COCO-class result as covering brand marks would be exactly the over-claim this battery exists to
prevent.

Note also that GenEval's 83% was measured on *their* material. A small local agreement check is
specified in calibration plan §3.4.

---

### 6.5 · D5 — `text_stability_across_frames`

**approval_status:** `controller_approved_v0` — approved for V0 by Controller, 24 Aug 2026.

**Property.** Rendered on-screen text remains *the same string* for the duration it is on screen.

**Why it is in V0.** This is the most distinctive measurement we have and the clearest
demonstration that observation unit is load-bearing. It is our own observed failure (`E-05` in
FINDINGS-11, the incidental finding in FINDINGS-01), it is the case that
`canon/knowledge/SPEC-04-operational-bindings.md` `observation_unit` was written for, and it has
independent published support: **T2VTextBench arXiv:2505.04946v1 (8 May 2025, only version)** is
dedicated to on-screen text fidelity **and temporal consistency** in text-to-video. v1 reports
*"the highest average score is reported for Sora, which is only 0.37"* across ten evaluated systems
on a 0/0.25/0.5/1 scale — every model below 0.4. Text instability in generated video is a real,
general, published failure, not an artefact of one clip we happened to make.

**Provenance.** `OBS` `direct`; `PUB` `direct` (T2VTextBench); `IR` `direct`
(`VideoCreativeExtension.continuity_requirements` — see §7.2 on the path).

**Observation unit:** `sequence`. Non-negotiable: at `frame` this defect does not exist.

**Item design.** One item = one target string + one scene + one clip. Frames sampled at a fixed
rate declared in `conditions`. **All frames from one clip are one trial.**

**Ladder.**

| Level | Added stressor |
|---|---|
| 1 | static camera, static sign, Latin string |
| 2 | +Devanagari string |
| 3 | +camera or subject motion |

**Pass criterion.** Two separate results, both recorded:
- `correctness` — the modal transcription equals the target (same predicate as D1).
- `stability` — all sampled frames yield the same normalised transcription.

These are independent. Our Wan clip **fails both**. A clip could pass stability while failing
correctness (consistently misspelled), which is a materially different defect with a different
repair, and collapsing them into one number would hide it.

**Instrument.** Per-frame transcription (D1's stage 1) plus deterministic cross-frame agreement.
The stability comparison is fully deterministic **given** the transcriptions; it inherits D1's
calibration and adds no new uncalibrated judgement.

**instrument_state:** inherits D1 / D2 state per script.

---

### 6.6 · D6 — `operational_behaviour`

**approval_status:** `traced_to_plan_v0`

**Property.** Cost, latency, failure and reproducibility behaviour of the workflow in use.

**Provenance.** `IR` `adjacent` (`delivery.*` constrains what must be produced, not how the
provider behaves); `OBS` `direct` (`E-19` provider API drift — Sarvam speaker names changing
between versions; `E-17`/`E-18` infrastructure failures); `PUB` `direct` (HYPE-EDIT-1's
effective-cost-per-success methodology, §7.3).

**Observation unit:** `whole_asset` per trial, aggregated per cell.

**Not a separate generation budget.** This is the correction to the plan's arithmetic: D6 is
measured as a **by-product** of the D1–D5 runs and costs **zero additional generations**. The
plan's `3 workflows × 4 dimensions × 3 levels × 20 trials ≈ 720` treats it as a fourth
generating dimension, which double-counts.

**Measured, all deterministic:** wall-clock latency p50/p95; API error rate by class
(4xx/5xx/timeout); moderation/refusal rate; per-call price at the exact posted rate on the run
date; **reproducibility** — repeat-rate agreement across `repeats` of the same item at fixed
seed where the provider supports seeds, and explicitly `seed_unsupported` where it does not.

**instrument_state:** `deterministic` — no calibration required.

---

## 7 · Instrument reference and known limits

### 7.1 The Devanagari gap — narrowed after Controller review

**⚠️ Narrowed 24 Aug 2026.** An earlier draft claimed "no benchmark covering Devanagari."
**That was too broad and is withdrawn.** Devanagari benchmarks exist — they measure a different
task.

**What exists: Devanagari *recognition*.** arXiv:2606.29213v1 (Jun 2026) stress-tests ten OCR/VLM
systems reading Devanagari; IIIT-ILST, IndicSTR12, the Bharat Scene Text Dataset, IndicVisionBench,
MLT-17/19 and DohaScript cover Indic scene text, documents and handwriting. Full table in
findings §1.1.

**The narrowed claim, re-checked and still supported:**

> **No public benchmark measures whether a generative image or video model correctly renders
> Devanagari text it was instructed to produce.**

Generative text-rendering benchmarks are English/Chinese (CVTG-2K, MARIO-Eval, AnyText,
TextAtlasEval, LongText-Bench, ChineseWord, OneIG-Bench EN/ZH). MULTITEXTEDIT covers 12 languages
including Bengali — not Devanagari. **Reading and drawing are different capabilities.** Our observed
failures are drawing failures, and nothing public scores them.

**OneIG-Bench: resolved, does not affect the claim.** Checked against the released dataset
(findings §1.2). Exactly two configs are published — English (1,120 rows, **no Multilingualism
category**) and Chinese (1,320 rows, including 200 `Multilingualism` rows). Sampled Multilingualism
rows are Simplified Chinese prompts about Chinese cultural subjects, consistent with the paper's own
description of the set as culture- and portrait-related and with its text-rendering score defining a
constant only for English and Chinese. **No Devanagari, no Indic script.** The structural evidence is
decisive; the content evidence is a 6-of-200 sample and is not extrapolated.

**Bengali as the nearest published generative proxy.** In MULTITEXTEDIT, Bengali — Brahmic, with
conjuncts and a headline stroke — is third-worst of twelve (∆Sem 0.697, ∆TA 0.960, ∆LSF 1.172),
behind only Hebrew and Arabic. Corroborating context for our own failures; it does **not** license
inferring a Devanagari number from a Bengali one.

**What the recognition benchmarks do give us.** They measure our *instrument* — an OCR-VLM reading
generated images — and they materially change the calibration design. The load-bearing point:
**clean synthetic renders do not discriminate between checkers** (all ten systems cluster at
chrF++ 91–98), so a calibration set built only from clean renders would be uninformative. Detail in
findings §1.3 and `INSTRUMENT-CALIBRATION-PLAN-V0.md` §3.1.

**Consequence.** The instrument must still be calibrated locally: nothing public scores Devanagari
*generation*, and whether reading-benchmark rankings transfer to generated-image text is NOT
VERIFIED. But the calibration material is **partly reusable** rather than wholly new — see §9.1.

### 7.2 SPEC-01 path corrections

Per Controller clarification 8, exact paths are used where defined, and mismatches in
`CAPABILITY-LAB-V0-PLAN.md` are flagged rather than papered over. No temporary naming convention
is invented.

| Plan writes | Status | Correct reference |
|---|---|---|
| `copy.headline.exactness` | ✅ defined | unchanged |
| `entities.invariants` | ✅ defined | `entities[].invariants` (array element) |
| `relationships` | ✅ defined | `relationships[]` |
| `audience.language` | ⚠️ **wrong field for D1** | SPEC-01 splits language four ways. On-screen Devanagari is `audience.language.on_screen_copy` + `copy.script_system`. `audience.language.spoken` is a *different capability* (speech/lip-sync), which the plan itself lists separately. |
| `static.composition` | ❌ not a SPEC-01 path | SPEC-01 §`StaticCreativeExtension` → `composition` |
| `video.continuity_requirements` | ❌ not a SPEC-01 path | SPEC-01 §`VideoCreativeExtension` → `continuity_requirements` |
| `video.temporal_structure` | ❌ not a SPEC-01 path | SPEC-01 §`VideoCreativeExtension` → `temporal_structure` |
| `video.dialogue_intent` | ❌ not a SPEC-01 path | SPEC-01 §`VideoCreativeExtension` → `dialogue_intent` |
| `brand.logo.exactness` | ⚠️ prose-defined only | SPEC-01 describes `brand.logo` as "(asset, placement, exactness)" in prose; no YAML block fixes the path |

**CROSS_STREAM.** SPEC-01's own open question 1 states that hierarchy element references "need a
naming scheme that survives compilation." Until Canon resolves it, the battery cannot cite IR
paths mechanically. Raised in the Controller Brief; not resolved here.

### 7.3 Cost methodology — published precedent

HYPE-EDIT-1 (Jan 2026), a 100-task reliability benchmark for image editing, independently
implements the economics this project already assumes. It generates **10 independent outputs per
task**, judges **binary pass/fail**, computes **pass@k**, estimates **expected attempts under a
retry cap**, and reports an **effective cost per success combining model price with human review
time**. Its stated conclusion: models with low per-image pricing are more expensive once retries
and human review are counted.

Two things follow for us. First, `usd_per_pass` has published precedent and is not an idiosyncratic
metric. Second — and this is the correction to our own schema — **their cost includes human
review time and ours did not.** ASSUMPTIONS §12 already warned that CpAO omits the intelligence
layer's own cost. Proposed schema fields in §`cost` address this.

Their **50 public / 50 private held-out** task split is also worth borrowing later, as protection
against the battery being optimised against. Not proposed for V0 (we have too few items to split),
recorded as a V1 candidate.

### 7.4 Instruments considered and not adopted in V0

| Instrument | Considered for | Not adopted because |
|---|---|---|
| CLIPScore | overall prompt adherence | holistic; GenEval's authors show it is unsuited to instance-level analysis, and it cannot express *which* constraint failed |
| DINO / CLIP-I similarity | identity preservation | 50.72% human alignment on concept preservation (DreamBench++); insensitive to exactly the detailed features our invariants name |
| Tesseract (Hindi) | Devanagari transcription | FINDINGS-01 records 0/14, unreadable output. See findings §5 — no supporting artifact for this claim exists in the repo, so it is carried as *unverified*, not as settled |
| TIFA question-generation | acceptance-contract checking | strong methodological fit for a later Production-IR-driven checker; the VQA answering step is an uncalibrated model judgement, so it is a V1 candidate, not a V0 instrument |
| LAION aesthetic predictor / MUSIQ (via VBench) | image quality | B-side, deferred per clarification 2 |
| AVA / Pick-a-Pic / HPDv2 preference models | creative fitness | B-side; and per corpus plan, contest and preference aesthetics are not commercial effectiveness |
| VBench `subject_consistency` (DINO across frames) | identity in video | same DINO limitation as above; and V0 does not cover in-clip identity |

---

## 8 · Costed run plan (parameterised)

Per Controller clarification 5, the cost model is parameterised first. Any model named below is a
**labelled budgeting example only** and is **not an approved benchmark roster**.

### 8.1 Parameters

```
N   items per (dimension, level)          # independent prompt-instances
R   repeats per item                       # seeds; measures reproducibility
U   generation units per trial             # 1 image, or S seconds of video
O   instrument observations per trial      # 1 for frame unit; F frames for sequence unit
V   human-verified fraction of trials
Cg  generation cost per unit
Ce  evaluator cost per observation
Ch  human cost per verified trial
```

### 8.2 Formulae

```
trials_per_cell     = N × R
generation_cost     = N × R × U × Cg
evaluation_cost     = N × R × O × Ce
human_cost          = N × R × V × Ch
cell_cost           = generation_cost + evaluation_cost + human_cost

pass_rate           = passes / trials            # reported with n_items, never n_trials alone
cost_per_pass       = cell_cost / passes         # see zero-pass rule
```

**Zero-pass rule.** When `passes == 0`, `cost_per_pass` is emitted as `null`, never as infinity
or a large sentinel, and the entry additionally carries
`cost_per_pass_lower_bound = cell_cost` with `passes_observed: 0`. "Never observed to pass in N
trials" and "expensive per pass" are different facts and must not collapse into one number.

**Total evaluator cost is not optional.** At the ~₹0.90 per VLM check recorded in FINDINGS-01,
`evaluation_cost` on a ₹2.50 image generation is over a third of the true cost of the observation.

### 8.3 Worked budgeting example — ILLUSTRATIVE ONLY

**Not an approved roster.** Workflows taken from `CAPABILITY-LAB-V0-PLAN.md` purely to make the
arithmetic concrete. Wan and Veo are kept as **separate** workflows per clarification 5 and are
never collapsed into one row.

Prices read from the fal.ai public pricing page, accessed 24 Aug 2026, normalised to 1MP:
Seedream V4 **$0.03/image**; Nano Banana **$0.0398/image**; Wan 2.5 **$0.05/second**; Veo 3
**$0.40/second**. ⚠️ The plan's own observed spike price of ~$0.15 per nano edit corresponds to
the **Nano Banana Pro** variant, which is priced separately and was **not** confirmed on the
vendor page during this task. Any approved run must re-read the exact model page on the run date.

Settings: `N = 12` items, `R = 2` repeats, `V = 0.20`, `Ce = $0.011` (≈₹0.90),
`Ch = $6.00` per verified trial (≈15 min at a nominal ₹2,000/hr; **not a budget approval**).

**Image cells** (D1, D2, D3, D4, D4b — levels 1–3), per workflow, `U = 1`, `O = 1`:

| Cell | trials | gen (Seedream $0.03) | eval | human | cell total |
|---|---:|---:|---:|---:|---:|
| one dimension × one level | 24 | $0.72 | $0.26 | $28.80 | **$29.78** |

**Video cells** (D5 — levels 1–3), per workflow, 5-second clips, 6 frames sampled, `O = 6`:

| Cell | trials | gen (Wan 2.5 @$0.05/s) | gen (Veo 3 @$0.40/s) | eval | human |
|---|---:|---:|---:|---:|---:|
| one dimension × one level | 24 | $6.00 | $48.00 | $1.58 | $28.80 |

**⚠️ Illustrative scenario, not a finding.** In the settings above, generation works out at ~2–4%
of an image cell. That ratio depends entirely on `V` and `Ch`, **neither of which is approved or
measured** — the 20% verification rate and the $6.00-per-verified-trial figure are placeholders
chosen to make the arithmetic concrete. Halve either and the ratio moves by a factor of four; set
human verification to zero and generation becomes the whole cost.

**What the scenario does support**, independent of the exact numbers: **human verification can
materially dominate total cost and must therefore be in the cost model rather than omitted.** That
was the term missing from our schema. It follows that `V` and `Ch` are the parameters worth
arguing about, and the calibration plan's human-hour estimates are what a budget decision actually
turns on.

### 8.4 Shape of a V0 run — and the correction to "720"

The plan's `3 × 4 × 3 × 20 ≈ 720` assumes full crossing. Two reasons it does not describe a real
design:

1. **D6 generates nothing.** It is a by-product. Counting it as a fourth generating dimension
   over-counts by roughly 180 generations.
2. **The cross is not physically meaningful.** An image-to-video workflow cannot be tested on
   `person_identity_across_prompts` the way an image model is, and an image model cannot exhibit
   `text_stability_across_frames`. The real design is **ragged**, not a cube.

Proposed shape — **image workflows** run D1, D2, D3, D4 and D4b (levels 1–3); **video workflows** run D5
(levels 1–3) plus D1 at frame level on extracted frames; **all** workflows accumulate D6 for free.

| Workflow type | Generating dimensions × levels | Cells | Trials at N=12, R=2 |
|---|---|---:|---:|
| Image | D1, D2, D3, D4, D4b × levels 1–3 | 15 | **360** per image workflow |
| Video | D5 × levels 1–3, plus D1 on extracted frames × 3 | 6 | **144** per video workflow |

**Updated 24 Aug 2026 for the D4 split.** Image workflows now run five generating dimensions, not
four: 15 cells rather than 12, and 360 trials rather than 288 at `N=12, R=2`. D6 still generates
nothing and is unchanged.

**D4 and D4b share generations only where the item genuinely satisfies both.** A count item and a
relation item are different prompts, so the default is separate items. Where one item is designed to
carry both a specified count *and* a specified relation — level 3 of each ladder — a single
generation may be scored twice, once per dimension, **producing two separate Registry entries**. The
table above assumes no sharing, so it is an upper bound; any sharing must be recorded in
`conditions` so a shared generation is never counted as two independent trials.

Seven dimensions are now defined for V0 (D2 and D5 Controller-approved 24 Aug 2026; D4/D4b split at
Controller direction). Exact totals depend on the approved roster, which remains a Controller
decision.

---

## 9 · Media and corpus requirements (for Resources)

Recorded as requirements, not requests. Nothing here is acquired by Eval.

| ID | Requirement | Why | Status |
|---|---|---|---|
| **M1a** | *Instrument*-calibration material: Devanagari images with existing ground-truth transcriptions from published recognition resources (arXiv:2606.29213 release, BSTD, IIIT-ILST, IndicSTR12), **including degraded and real-scan material, not only clean renders** | calibrating I1's reading accuracy | **candidate for reuse** — conditional on Resources clearing it for bounded internal evaluation under `resources/CHARTER.md` (§9.1) |
| **M1b** | *Capability* item set: prompt → target-string pairs covering conjuncts, matras, nukta and the observed ब/व and य/थ confusion pairs, with native-speaker-verified reference renderings | D1/D5 — feeding generators | the **item set** must be built; the **target strings themselves may be drawn from existing permissible Hindi text resources** (§9.1) |
| **M2** | Latin string set matched to M1 on word and character count | D2 delta-vs-Latin design | trivially constructible |
| **M3** | Reference image sets for person identity: ≥12 subjects, multiple views, with declared invariants and allowed-variation | D3 | needs rights clearance — Resources |
| **M4** | Generic-object prompt set restricted to MS COCO's 80 classes | D4 detector constraint (§6.4) | constructible from GenEval's public prompt list |
| **M5** | Access to the `media-factory` spike outputs (64 scored images) as regression cases | permanent regression layer | **BLOCKED** — see §10 |

### 9.1 M1 — reassessed after Controller review

An earlier draft stated M1 "cannot be acquired and must be built." **That rested on the over-broad
claim corrected in §7.1 and is withdrawn.** M1 splits in two:

- **M1a — candidate for reuse, pending a Resources clearance decision.** Published Devanagari
  recognition resources carry images with human ground-truth transcriptions, which is exactly what
  calibrating the *reading* instrument needs. arXiv:2606.29213 states its benchmark, code and models
  are released, and its arXiv page displays a CC BY 4.0 licence icon.

  **Updated 24 Aug 2026 to current Resources policy.** Reuse is conditional on **Resources clearing
  the material for bounded internal evaluation under `resources/CHARTER.md`** — not on a licence
  being found. Under that charter, **absence of a stated licence is no longer an automatic block**
  for public, ungated material used internally: what blocks is an explicit prohibiting term, a
  gate, or a use beyond internal evaluation. Our use is internal evaluation only. If Resources
  clears it, rights are recorded as `not_stated` / `not_verified` and the material **may not** be
  redistributed, used as training data, delivered to customers, or treated as production-cleared.
  **Eval performs no rights assessment of any kind** — that is Resources' work.

- **M1b — the item set must be built; the strings need not all be authored.** No public resource
  contains prompt → target-string pairs for Devanagari *generation*, so the pairing, the difficulty
  laddering and the reference renderings are ours to construct. **The target strings themselves may
  be drawn from existing permissible Hindi text resources** rather than written from scratch —
  ordinary Hindi words and phrases are not scarce, and sourcing them reduces authoring to selection
  plus native-speaker verification. What must be deliberately constructed is the *coverage*:
  conjuncts, i/u matras, nukta-bearing characters, and the ब/व and य/थ pairs we have observed being
  confused. Any external text source used is subject to the same Resources clearance as M1a.

**The two may not substitute for each other.** M1a calibrates whether the checker can *read*
Devanagari. M1b measures whether a generator can *draw* it. Using recognition material as capability
items would measure the wrong thing.

**Revised effort.** The original estimate assumed authoring everything. With M1a clearance and
string sourcing, native-reader time narrows to verifying M1b's reference renderings plus a local
agreement check — see `INSTRUMENT-CALIBRATION-PLAN-V0.md` §3.1 and §4.

---

## 10 · Regression cases — referenced, not imported

Per Controller clarification 6, the external `media-factory` 64-image set is **not copied** into
this repository during EVAL-001, and is **not re-scored**. Recorded as historical evidence and as
a dependency for a later Resources/integration task.

**What is verifiable today.** `media-factory/spike/out/scores.json` exists on the local machine
and contains 64 records with 10 failures (nano 7/32, seedream 3/32), matching the counts cited in
`CAPABILITY-LAB-V0-PLAN.md` and FINDINGS-11. I read it read-only to confirm the counts and
changed nothing.

**Two dependencies this creates.**

1. **The media is unreachable from this repository.** The 10 failure images are not in
   `media-intelligence`, so the regression cases the plan calls the layer that "gets more
   valuable with time" cannot currently be assembled where the battery that consumes them lives.
2. **The records are single-label and therefore a floor, not a count.** Every entry carries one
   free-text note. FINDINGS-11 §Co-occurrence establishes that `seedream_sign_t1`, scored only
   "rendered hex codes from prompt", *also* exhibits the head-collision defect — the human
   recorded the most salient failure and the second was lost. Project Contract separation 13
   requires multiple defects per output. **Re-annotation is prerequisite to regression use, is
   human work, and is explicitly out of EVAL-001's scope.**

Until both are resolved, the 10 failures function as *evidence that these dimensions matter*
(which is how §6 uses them) and **not** as runnable regression cases.

---

## 11 · What V0 must not do

Carried forward from `CAPABILITY-LAB-V0-PLAN.md`, unchanged, with two additions from this task.

- Benchmark live during a customer request.
- Trust a vendor claim.
- Report a capability without naming its instrument.
- Infer any capability from a book.
- Treat a published benchmark's score as our answer.
- **Report a pass rate without `n_items` alongside `n_trials`** (§5.4).
- **Write a Registry entry from an instrument whose `instrument_state` is
  `provisional_uncalibrated`** (§6.1).

---

## 12 · Open items requiring a Controller decision

1. ~~D2 and D5 as V0 dimensions~~ — **RESOLVED: both approved by Controller, 24 Aug 2026.**
2. **The approved workflow roster.** §8.3 is an illustrative example only.
3. **Human verification budget** — `V` and `Ch` in §8.2 dominate cost. Calibration alone needs
   **≈ 11–15.5 hours** (calibration plan §4), of which 2–4 must be a Hindi first-language reader;
   run-time verification is on top. Needs a budget decision before any run.
4. **M1 ownership, now split** (§9.1). **M1a** — can Resources verify licensing on the published
   Devanagari recognition resources so their material can calibrate our reading instrument?
   **M1b** — who builds the prompt/target-string set that must still be created from scratch?
5. **The SPEC-01 naming-scheme gap** (§7.2) — CROSS_STREAM to Canon.
6. **Registry schema field additions** — see the schema draft; several touch routing semantics
   and are raised as cross-stream rather than assumed.
