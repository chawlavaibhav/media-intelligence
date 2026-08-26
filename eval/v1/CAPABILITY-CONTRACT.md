# Eval V1 — Capability & Measurement Contract

> **GENERATED FILE — do not hand-edit.**  
> Source of truth: [`capability-contract.yaml`](capability-contract.yaml).  
> Regenerate with `python3 eval/v1/render_contract_docs.py`.  
> Validate with `python3 eval/v1/validate_capability_contract.py`.

**Task:** E1 · **Date:** 2026-08-26 · **Status:** `PROPOSED_FOR_CONTROLLER_REVIEW` · **Contract version:** `v1-draft`

## What this document is

This is the **measurement contract**: it says what each of the 36 frozen capabilities *means*, at what unit it must be observed, how it is tested, which instrument judges it, and what has to be held fixed for two measurements to be comparable.

**It contains no results.** No model has been measured, no instrument is qualified, and nothing here licenses a capability claim. Its purpose is that a later task cannot quietly redefine what a capability meant and report the rerun as the same experiment.

## The three rules that protect every number downstream

**1 · One generation is one trial.** Several evaluators may score that one trial. Those are several *measurements* of one trial, never several trials. Frames sampled from one clip carry the parent trial id and remain one trial. Confidence is computed on independent **base items** — never on trials, never on frames. The founding example: a prior study's 14 samples came from only 4 independent sources, so treating them as 14 overstates confidence roughly threefold.

**2 · The observation unit is load-bearing.** A misspelling that *changes* partway through a clip does not exist in any single frame — it exists only *between* frames. Choose the wrong unit and the defect is undetectable, not merely under-measured. The unit vocabulary is Canon's (`SPEC-04`), adopted unchanged: `frame`, `shot`, `shot_pair`, `sequence`, `whole_asset`, `asset_set_over_time`.

**3 · Generate once, measure everything valid.** A generated asset may feed every measurement for which it is a valid observation unit. Never regenerate because a second evaluator wants to look. Reuse never turns one asset into multiple independent trials.

## Summary

Readiness is **two independent questions**, not one score (correction E-C1).

**Can the mechanism be trusted?**

| `instrument_readiness` | Count |
|---|---:|
| blocked — not qualified | 30 |
| deterministic — ready | 6 |

**Do we hold the material to exercise it?**

| `benchmark_material_readiness` | Count |
|---|---:|
| missing | 17 |
| Eval constructs it | 10 |
| none needed | 5 |
| partial | 3 |
| held | 1 |

| | |
|---|---:|
| Capabilities defined | **36 / 36** |
| **Ready on BOTH axes** | **5** |
| Usable as a hard routing constraint | 27 |
| Descriptive evidence only | 9 |
| Empirical results contained | **0** |

**Why two axes.** A single score had to misreport one of them. `audio_video_synchronisation` and `edit_preservation` have mechanisms that need no calibration *and* no material to run on — a state the old scalar could only call "measurable now" (false: there is nothing to measure) or "blocked on instrument" (false: the instrument is fine). Each misreading sends the next decision the wrong way: one wastes qualification effort, the other buys material we may not need yet.

**Only 5 of 36 are ready on both axes**, and every one of them is operational or deterministic — none reports fidelity or creative quality.


---

## A · Constraint fidelity — did it do the specific checkable thing it was told to do?

### `object_count` — Right number of things

The output contains exactly the number of each named object the prompt asked for. Three bottles means three, not two and not four.

- **Covers:** Cardinality of prompt-named countable objects.
- **Does not cover:** Where the objects are (spatial_relationship), what they look like (attribute_binding), and whether they are the RIGHT specific product (product_identity).
- **Observation unit:** `frame` — Single image; for video, the declared hero frame plus 2 sampled frames.
- **Applies to:** image, video, editing
- **Atomic probe:** Prompt names N instances of one plainly countable object on a plain background, no other countable objects present. N is varied across items.
- **Reusable from:** `product_packshot`, `person_plus_product_static`, `product_handoff_action`, `multi_shot_branded_ad`
- **Instrument:** deterministic CV/geometry, corroborated by structured visual VLM
- **Human verifier:** Adjudicates only when the detector and the VLM disagree, or on partial occlusion.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `constructed_by_eval` — Eval constructs it
- **Result form:** `exact_pass_fail`
- **Routing use:** `hard_constraint`

  **Difficulty ladder**

  1. 1-3 instances of one object type, plain background, no occlusion
  2. 4-6 instances of one object type, plain background
  3. two object types counted simultaneously, e.g. 3 bottles and 2 boxes
  4. counted objects partially occluding one another
  5. counted objects in a cluttered commercial scene with distractor objects

  **Failure vocabulary:** Observer's own words retained, e.g. "one extra bottle", "shadow counted as object". Multiple defects per output permitted. Ontology mapping later.

  **Held fixed for comparability:** `resolution`, `aspect_ratio`, `object_class`, `target_count`, `background_complexity`, `detector_confidence`

  **Note:** Detector-based counting is implementable and its truth is constructed by us. NOTE the known trap - counting and locating need DIFFERENT detector confidence settings. High when counting, so shadows are not counted as extra objects; lower when locating. Shared software, separate results, separate Registry rows. UNBLOCK PATH IS CHEAP - a detector is a model, not an oracle, so this is blocked until family 2 is qualified. Qualification needs no human labels at all - E3's 100 synthetic known-answer fixtures supply the truth by construction.

### `attribute_binding` — Right property on the right thing

When the prompt says "the red bottle and the blue box", the red belongs to the bottle and the blue to the box. Models frequently produce both objects and both colours but swap which is which.

- **Covers:** Correct assignment of colour, material, size or state to the named object.
- **Does not cover:** Whether the colour matches a brand specification (packaging_brand_colour_fidelity) and whether the count is right (object_count).
- **Observation unit:** `frame` — Single image; for video, the declared hero frame.
- **Applies to:** image, video, editing
- **Atomic probe:** Two objects, two attributes, deliberately crossable. The swapped assignment is a distinct, observable failure and is recorded as such rather than as a generic miss.
- **Reusable from:** `product_packshot`, `typography_led_image`, `person_plus_product_static`, `multi_shot_branded_ad`
- **Instrument:** structured visual VLM, corroborated by deterministic CV/geometry
- **Human verifier:** Adjudicates ambiguous material/finish descriptions.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `constructed_by_eval` — Eval constructs it
- **Result form:** `structured_categorical`
- **Routing use:** `hard_constraint`

  **Difficulty ladder**

  1. one object, one attribute
  2. two objects, two distinct colours - swap is detectable
  3. two objects, colour plus material, e.g. matte red bottle and glossy blue box
  4. three objects, three attributes
  5. attribute assignment in a cluttered scene with same-class distractors

  **Failure vocabulary:** Distinguish `attribute_swapped`, `attribute_absent`, `attribute_on_extra_object`. Swap and absence are different failures with different repair paths.

  **Held fixed for comparability:** `resolution`, `aspect_ratio`, `n_objects`, `attribute_type`, `distractor_present`

  **Note:** Colour can be sampled deterministically inside a detected region, which makes part of this dimension instrument-cheap. Material and finish need a VLM and are the uncertain part; the split is recorded per the Registry `deterministic_component` field. UNBLOCK PATH - the colour half can be qualified deterministically; the material/finish half needs the VLM family qualified. Blocked until then, because the dimension reports one verdict and the weaker half governs it.

### `spatial_relationship` — Things in the right places relative to each other

The prompt's positional instruction holds - the cup is LEFT OF the laptop, the logo is in the LOWER RIGHT, the product is IN FRONT OF the model.

- **Covers:** Relative position between named entities, and absolute placement within the frame.
- **Does not cover:** How many objects there are (object_count) and continuity across shots (multi_shot_spatial_continuity).
- **Observation unit:** `frame` — Single image; for video, the declared hero frame.
- **Applies to:** image, video, editing
- **Atomic probe:** Two unambiguous objects with one stated relation, on a plain background, where the relation is decidable from bounding-box geometry alone.
- **Reusable from:** `product_packshot`, `typography_led_image`, `person_plus_product_static`, `product_hero_video`, `multi_shot_branded_ad`
- **Instrument:** deterministic CV/geometry, corroborated by structured visual VLM
- **Human verifier:** Adjudicates depth-ordering cases the detector cannot resolve.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `constructed_by_eval` — Eval constructs it
- **Result form:** `exact_pass_fail`
- **Routing use:** `hard_constraint`

  **Difficulty ladder**

  1. left/right of, two objects, plain background
  2. above/below, and in-frame quadrant placement
  3. in front of / behind - requires depth ordering, not just 2D boxes
  4. count and relation together, e.g. three cups to the left of one laptop
  5. relation preserved under camera movement across a clip

  **Failure vocabulary:** `relation_inverted`, `relation_absent`, `object_missing`, `depth_ambiguous`.

  **Held fixed for comparability:** `resolution`, `aspect_ratio`, `relation_type`, `n_objects`, `detector_confidence`

  **Note:** Left/right/above/below are decidable from bounding boxes and need no human label. Depth ordering is NOT decidable from 2D boxes and is escalated to a VLM plus human adjudication; it must not be silently scored by the geometric instrument. UNBLOCK PATH IS CHEAP - synthetic fixtures with known geometry qualify family 2 with no human label. Blocked only because no family is qualified yet, not because the material is hard to build.

### `action_adherence` — The thing actually does what it was told to do

The prompted action is the action depicted - pouring, opening, handing over, walking towards camera - rather than a static pose that merely resembles it.

- **Covers:** Presence and correctness of the prompted action or verb.
- **Does not cover:** Whether the motion looks physically plausible (motion_action_quality) and whether hands are anatomically correct (anatomy_hands).
- **Observation unit:** `sequence` — For video, whole clip - an action is a temporal object. For a still image, `frame`, and the item declares that the still can only test a depicted instant, not the action.
- **Applies to:** image, video, native_av, editing
- **Atomic probe:** One subject, one unambiguous prompted action, plain setting. For video the action must be one whose completion is observable within the clip length.
- **Reusable from:** `product_handoff_action`, `product_hero_video`, `actor_plus_product_vo`, `multi_shot_branded_ad`
- **Instrument:** temporal/video, corroborated by structured visual VLM
- **Human verifier:** Decides whether the depicted action is the prompted action when the VLM is uncertain.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `constructed_by_eval` — Eval constructs it
- **Result form:** `structured_categorical`
- **Routing use:** `hard_constraint`

  **Difficulty ladder**

  1. single-actor gross action, e.g. walking, plain background
  2. actor plus object action, e.g. picking up a bottle
  3. action with a required completion state, e.g. pouring until the glass is full
  4. two-participant action, e.g. handing an object from one person to another
  5. ordered two-step action, e.g. open the box then lift out the product

  **Failure vocabulary:** `action_absent`, `action_substituted`, `action_incomplete`, `action_out_of_order`.

  **Held fixed for comparability:** `resolution`, `aspect_ratio`, `clip_duration_s`, `fps`, `action_class`, `n_participants`, `sampled_frames`

  **Note:** Requires the temporal evaluator family, which is itself unqualified. A still image cannot establish an action; items must not silently score a still as if it had. Blocked on family 4, which has no qualification record. Deterministic perturbation of clean clips supplies known-answer material without human labels, so the unblock path does not depend on new human time.

### `delivery_format_compliance` — The file is the file we asked for

Duration, aspect ratio, resolution, frame rate, container, audio track presence and any stated output contract are exactly as requested.

- **Covers:** Machine-checkable properties of the delivered artifact itself.
- **Does not cover:** Anything about what the artifact depicts.
- **Observation unit:** `whole_asset` — The delivered file, probed once.
- **Applies to:** image, video, native_av, lipsync, tts, editing
- **Atomic probe:** Request an explicit output contract - e.g. 9:16, 1080x1920, 8.0s, 24fps, with audio - and probe the returned file.
- **Reusable from:** every compound scenario
- **Instrument:** deterministic CV/geometry
- **Human verifier:** *none*
- **Instrument readiness:** `deterministic_ready` — deterministic — ready
- **Benchmark material:** `no_external_stimulus_required` — none needed
- **Result form:** `exact_pass_fail`
- **Routing use:** `hard_constraint`

  **Difficulty ladder**

  1. provider default output accepted and probed
  2. one non-default constraint requested, e.g. 9:16
  3. resolution and aspect together
  4. exact duration to within a declared tolerance
  5. full contract - duration, aspect, resolution, fps and audio track together

  **Failure vocabulary:** `aspect_mismatch`, `duration_mismatch`, `resolution_mismatch`, `fps_mismatch`, `audio_track_absent`, `container_unexpected`.

  **Held fixed for comparability:** `requested_contract`, `provider_default_contract`

  **Note:** Fully deterministic - it reads file metadata and needs no calibration at all. Its Registry `calibration_status` is `deterministic`. This is the cheapest dimension in the whole contract and should be measured on EVERY generated asset as a free rider, never as its own generation. It must fail closed on an unparseable file rather than reporting a pass.

  **Production envelope:** Ready and needs no external stimulus. Should ride free on EVERY generated asset from the first paid call onward; not doing so is wasted money.


---

## B · Text & brand — the family the Indian-market scope makes unavoidable

### `exact_text_latin` — Latin-alphabet text drawn exactly right

A requested Latin string appears in the image character-for-character correct after a declared normalisation.

- **Covers:** Exact character-level correctness of a requested Latin string.
- **Does not cover:** Whether it is readable at size (typography_legibility) and whether it is the brand wordmark (logo_wordmark_fidelity).
- **Observation unit:** `frame` — Single image; for video see text_logo_stability_in_clip, which is a different dimension.
- **Applies to:** image, video, editing
- **Atomic probe:** Render-target pairs at increasing string length, plain layout, high contrast, one string per item.
- **Reusable from:** `typography_led_image`, `product_packshot`, `person_plus_product_static`, `multi_shot_branded_ad`
- **Instrument:** text/OCR, corroborated by structured visual VLM
- **Human verifier:** None for the comparison itself; a human confirms only that the reference string is what was requested.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `constructed_by_eval` — Eval constructs it
- **Result form:** `exact_pass_fail`
- **Routing use:** `hard_constraint`

  **Difficulty ladder**

  1. single word, <=8 characters
  2. two to four words on one line
  3. headline plus subline, two text blocks
  4. text on a product surface or signage within the scene
  5. text with mixed case, digits and punctuation, e.g. a price and a claim

  **Failure vocabulary:** `char_substitute`, `char_drop`, `char_insert`, `word_drop`, `gibberish`, `prompt_leakage`.

  **Held fixed for comparability:** `resolution`, `aspect_ratio`, `script`, `string_length_words`, `string_length_chars`, `normalisation_ref`, `surface_type`

  **Note:** Needs a Latin exact-text calibration pack that does NOT exist yet - E3 specifies it. It must be built separately and MUST NOT mutate the frozen Devanagari battery. Like the Devanagari case, the comparison step is deterministic; only the transcription step is uncertain. Blocked on family 1, which is unqualified, AND on a Latin pack that does not exist. The Devanagari battery cannot substitute - it is frozen, and reading Latin is a different judgement.

### `exact_text_devanagari` — Hindi/Devanagari text drawn exactly right

A requested Devanagari string appears character-for-character correct after NFC normalisation - including vowel signs, conjuncts, nukta, nasal marks and the two positional forms of the letter र.

- **Covers:** Exact character-level correctness of a requested Devanagari string.
- **Does not cover:** Reading real photographed Hindi signage - that is a checker-calibration question, not a generator capability. The two must never be conflated.
- **Observation unit:** `frame` — Single image; drift within a clip is text_logo_stability_in_clip.
- **Applies to:** image, video, editing
- **Atomic probe:** Render-target pairs from the frozen validated word pool, using the EVAL-005 failure taxonomy's 20 classes across 5 groups as the perturbation space for checker qualification, and as the defect vocabulary for generator scoring.
- **Reusable from:** `typography_led_image`, `product_packshot`, `person_plus_product_static`, `multi_shot_branded_ad`
- **Instrument:** text/OCR, corroborated by structured visual VLM
- **Human verifier:** A Hindi first-language reader confirms that a TARGET string is valid Hindi. The reader never decides whether an image matches its target - for the qualification battery that label is true by construction.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `available` — held
- **Result form:** `exact_pass_fail`
- **Routing use:** `hard_constraint`

  **Difficulty ladder**

  1. single word, no conjunct, no nukta
  2. single word containing a conjunct or a reph
  3. two to four words on one line
  4. headline plus subline, or text on an in-scene surface
  5. Devanagari and Latin together in one composition

  **Failure vocabulary:** The 20 frozen EVAL-005 failure classes in 5 groups - vowel_signs, letters, conjuncts, dots_marks, ra_forms - retained as the observer vocabulary.

  **Held fixed for comparability:** `resolution`, `aspect_ratio`, `script`, `string_length_words`, `normalisation_ref`, `font_or_surface`, `battery_version`

  **Note:** The checker-qualification battery EXISTS and is frozen - 96 items, 48 match / 48 mismatch, 48 accepted base words, 33 hard opportunities. What does NOT exist is a checker that has passed it. Until one has, no generator score on this dimension may be written to the Registry. Registry state for now - `required_but_no_calibrated_instrument`. The battery also cannot produce malformed GENERATED glyphs; it perturbs real characters. A generator can fail in a way this battery never shows - see the Class B generated-glyph layer, specified but not built.

  **Production envelope:** The frozen 96-item battery qualifies a checker against CORRECTLY-FORMED WRONG TEXT. It perturbs real characters and cannot produce malformed generated glyphs, so a checker qualified on it is NOT qualified against the failure mode where a generator emits shapes that are not characters at all.

### `typography_legibility` — The text can actually be read at delivery size

Correct characters are not enough. Text must survive the size, contrast and placement it will be viewed at - a headline correct at 100% zoom and unreadable in a feed is a commercial failure.

- **Covers:** Contrast, effective type size, crowding, overlap with busy background, cropping at frame edge.
- **Does not cover:** Whether the characters are correct (exact_text_*) and whether the typeface is the brand's.
- **Observation unit:** `frame` — Single image evaluated at the declared delivery size, not at native resolution.
- **Applies to:** image, video, editing
- **Atomic probe:** Same string rendered at declining relative type size and declining contrast against a controlled background, with the delivery size declared.
- **Reusable from:** `typography_led_image`, `product_packshot`, `multi_shot_branded_ad`
- **Instrument:** structured visual VLM, corroborated by deterministic CV/geometry
- **Human verifier:** Required. Legibility is a perceptual judgement; a contrast ratio alone does not settle it.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `constructed_by_eval` — Eval constructs it
- **Result form:** `human_hybrid_score`
- **Routing use:** `descriptive_only`

  **Difficulty ladder**

  1. large text, plain high-contrast background
  2. text over a photographic background
  3. small subline text at declared feed delivery size
  4. text over a busy or low-contrast region
  5. text near the frame edge where platform-safe-area cropping applies

  **Failure vocabulary:** `too_small_at_delivery`, `low_contrast`, `overlapped_by_subject`, `crops_at_safe_area`, `crowded`.

  **Held fixed for comparability:** `resolution`, `aspect_ratio`, `delivery_size_declared`, `background_class`, `type_size_ratio`

  **Note:** Deterministic components exist - measured contrast ratio and type height as a fraction of frame height are both computable. Whether that adds up to "legible" is a perceptual call and needs human calibration first. Do NOT invent a contrast threshold and present it as a finding; propose a calibration curve, per the same rule applied to audio tolerances.

### `logo_wordmark_fidelity` — The brand mark is the real mark, not a lookalike

A supplied logo or wordmark appears with its true geometry, proportions and letterforms, rather than a plausible re-drawing.

- **Covers:** Shape, proportion, letterform and structural correctness of a supplied mark.
- **Does not cover:** Brand colour accuracy (packaging_brand_colour_fidelity) and general text (exact_text_*).
- **Observation unit:** `frame` — Single image; drift within a clip is text_logo_stability_in_clip.
- **Applies to:** image, video, editing
- **Atomic probe:** Supply a controlled reference mark, request placement, compare the rendered mark against the reference under a declared alignment.
- **Reusable from:** `product_packshot`, `typography_led_image`, `person_plus_product_static`, `reference_campaign_edit`, `multi_shot_branded_ad`
- **Instrument:** structured visual VLM, corroborated by deterministic CV/geometry
- **Human verifier:** Required. Adjudicates whether a difference is a re-drawing or an acceptable projection.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `partial` — partial
- **Result form:** `human_hybrid_score`
- **Routing use:** `hard_constraint`

  **Difficulty ladder**

  1. flat placement on plain background, frontal
  2. placed on a flat product surface
  3. on a curved surface, e.g. a bottle
  4. in perspective at an angle
  5. in motion within a clip

  **Failure vocabulary:** `mark_redrawn`, `proportion_distorted`, `letterform_wrong`, `element_missing`, `mark_absent`, `mark_duplicated`.

  **Held fixed for comparability:** `resolution`, `aspect_ratio`, `surface_geometry`, `mark_ref_hash`, `placement_request`

  **Note:** Recorded in CAPABILITY-BATTERY-V0-DRAFT section 4 as `required_but_no_calibrated_instrument`, and that has not changed. Template matching handles flat frontal cases and fails under perspective and curvature, which is exactly where commercial work lives. Requires controlled brand-mark references from Resources. Keeping this dimension visible with an explicit blocked state is the point - a dimension with no instrument that quietly disappears later reads as "we decided this did not matter".

  **Production envelope:** Recorded in prior findings as required_but_no_calibrated_instrument. Template matching handles flat frontal marks and fails under perspective and curvature - which is where commercial work lives, so the easy envelope is the one we could qualify and the hard envelope is the one we need.

### `packaging_brand_colour_fidelity` — Brand colours are the actual brand colours

A specified brand or packaging colour is reproduced within a declared tolerance in a declared colour space, rather than merely being the right general hue.

- **Covers:** Measured colour of a specified region against a specified reference value.
- **Does not cover:** Whether the colour is on the right object (attribute_binding) and whether the logo shape is right (logo_wordmark_fidelity).
- **Observation unit:** `frame` — Single image; sampled within a detected or declared region.
- **Applies to:** image, video, editing
- **Atomic probe:** Supply a reference swatch and a target region, sample the rendered region and compute a colour difference in a declared space.
- **Reusable from:** `product_packshot`, `person_plus_product_static`, `reference_campaign_edit`, `multi_shot_branded_ad`
- **Instrument:** deterministic CV/geometry, corroborated by structured visual VLM
- **Human verifier:** Sets the acceptable tolerance once, with reference to commercial practice; does not judge per item.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `missing` — missing
- **Result form:** `structured_categorical`
- **Routing use:** `hard_constraint`

  **Difficulty ladder**

  1. flat colour field, even studio lighting
  2. colour on a flat packaging face
  3. colour on a curved surface with a specular highlight
  4. colour under a deliberately warm or cool lighting setup
  5. colour held across a clip under changing light

  **Failure vocabulary:** `hue_shift`, `saturation_loss`, `value_shift`, `colour_replaced`, `region_not_found`.

  **Held fixed for comparability:** `resolution`, `colour_space`, `tolerance_metric`, `tolerance_value`, `lighting_condition`, `region_definition`

  **Note:** Sampling is deterministic once the region is located, so the instrument cost is low. What is missing is the resource - controlled product references with declared brand colour values. The TOLERANCE is a judgement call and must be declared and Controller-approved before a run, not chosen after seeing results; changing it later is an EXPERIMENT MUTATION stop.


---

## C · Identity & references — “is this the same person / the same product?”

### `person_identity` — The same person stays the same person

A person generated from a reference, or across separate generations, is recognisably the SAME individual - face, hair, build and declared wardrobe invariants - rather than a different person of similar description.

- **Covers:** Match to a supplied person reference, and consistency of that person across separately generated assets.
- **Does not cover:** Drift WITHIN one clip (person_stability_in_clip) and anatomical correctness (anatomy_hands).
- **Observation unit:** `asset_set_over_time` — A set of separately generated assets compared pairwise against the reference and against each other. A single image cannot test this.
- **Applies to:** image, video, native_av, editing
- **Atomic probe:** One person reference, N separate generations under varied prompts. Include known-match and known-NON-match reference pairs so the instrument can be caught being permissive.
- **Reusable from:** `person_plus_product_static`, `actor_plus_product_vo`, `one_visible_speaker`, `two_person_dialogue`, `multi_shot_branded_ad`
- **Instrument:** structured visual VLM
- **Human verifier:** Required for adjudication. Identity similarity is not exact equality and must not be presented as if it were.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `missing` — missing
- **Result form:** `human_hybrid_score`
- **Routing use:** `hard_constraint`

  **Difficulty ladder**

  1. same person, same prompt, repeated generation
  2. same person across different prompts, same setting
  3. same person across different settings and lighting
  4. same person across separate shots intended to cut together
  5. same person across separate sessions, days apart, no shared context

  **Failure vocabulary:** `different_person`, `face_drift`, `wardrobe_change`, `age_shift`, `build_shift`, `hair_change`.

  **Held fixed for comparability:** `resolution`, `aspect_ratio`, `reference_count`, `reference_hashes`, `prompt_variation_class`, `session_separation`

  **Note:** Needs the planned >=32 person references, 8 identities x >=4 views. The frozen V0 rubric already encodes the essential rule and must be reused unchanged - each declared identity feature is judged on TWO questions, does it match the reference AND is it consistent across the set, and BOTH must hold. A consistently-produced WRONG person is a failure, not a pass. "Stability is not identity."

  **Production envelope:** Material target exists but WITHOUT same-category decoys the envelope is category recognition, not individual identity (cross-stream ask ADD-01).

### `product_identity` — The same product stays the same product

A specific product - its shape, proportions, label layout, closure and distinguishing features - is reproduced as that product rather than as a generic member of its category.

- **Covers:** Match to a supplied product reference across generations.
- **Does not cover:** Brand colour value (packaging_brand_colour_fidelity), mark geometry (logo_wordmark_fidelity), drift within a clip (product_stability_in_clip).
- **Observation unit:** `asset_set_over_time` — A set of separately generated assets compared against the product reference.
- **Applies to:** image, video, editing
- **Atomic probe:** One product reference, N generations at varying pose and context, with known-match and known-non-match pairs including same-category decoys.
- **Reusable from:** `product_packshot`, `person_plus_product_static`, `product_hero_video`, `product_handoff_action`, `reference_campaign_edit`, `multi_shot_branded_ad`
- **Instrument:** structured visual VLM, corroborated by deterministic CV/geometry
- **Human verifier:** Required for adjudication, especially against same-category decoys.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `missing` — missing
- **Result form:** `human_hybrid_score`
- **Routing use:** `hard_constraint`

  **Difficulty ladder**

  1. frontal, studio, static
  2. rotated to a three-quarter view
  3. held in a hand
  4. partially occluded or in a cluttered scene
  5. in motion within a clip

  **Failure vocabulary:** `different_product`, `label_redrawn`, `shape_drift`, `feature_missing`, `feature_invented`, `category_generic`.

  **Held fixed for comparability:** `resolution`, `aspect_ratio`, `reference_count`, `reference_hashes`, `pose_class`, `occlusion_class`

  **Note:** Needs the planned >=48 product references, 12 products x >=4 views. The same-category decoy is the important design element - without it, an instrument that says "yes, that is a shampoo bottle" scores as if it had verified identity.

  **Production envelope:** As person_identity: without same-category decoys the qualification envelope cannot separate recognising a product CATEGORY from recognising THE product.

### `reference_conditioning` — The model actually uses the reference images you give it

Measures how well a workflow honours supplied reference images at all - one reference, several references, and a reference combined with a requested style or context change. This is the mechanism by which any identity result is achieved.

- **Covers:** Whether and how strongly supplied references control the output.
- **Does not cover:** Whether the resulting identity is correct (person_identity, product_identity) - that is the outcome, this is the mechanism.
- **Observation unit:** `asset_set_over_time` — Generations compared across increasing reference counts and increasing requested divergence.
- **Applies to:** image, video, editing
- **Atomic probe:** Hold the prompt fixed and vary only the reference configuration - none, one, three - then measure how the output changes.
- **Reusable from:** `reference_campaign_edit`, `person_plus_product_static`, `product_packshot`, `multi_shot_branded_ad`
- **Instrument:** structured visual VLM, corroborated by deterministic CV/geometry
- **Human verifier:** Adjudicates the conflict case at level 5.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `missing` — missing
- **Result form:** `structured_categorical`
- **Routing use:** `hard_constraint`

  **Difficulty ladder**

  1. one reference, no requested change
  2. one reference plus a background change
  3. multiple references, e.g. person plus product
  4. reference plus a requested style change
  5. reference plus a change that conflicts with the reference, testing which wins

  **Failure vocabulary:** `reference_ignored`, `reference_overapplied`, `reference_blended`, `only_first_reference_used`, `reference_rejected_by_api`.

  **Held fixed for comparability:** `resolution`, `reference_count`, `reference_hashes`, `reference_slot_semantics`, `requested_divergence_class`

  **Note:** Shares the SAME reference packs as person_identity and product_identity - no separate acquisition is needed, and no separate generation either where the same asset serves both. `only_first_reference_used` is called out explicitly because it is a known provider-shaped failure that a generic "reference ignored" label would hide.

### `edit_preservation` — Editing one thing does not quietly change everything else

When a workflow is asked to change a specified region or attribute, the rest of the asset survives unchanged - the untouched area is genuinely untouched.

- **Covers:** Preservation of non-target content during an edit or inpaint operation.
- **Does not cover:** Whether the requested change itself is correct - that is scored by whichever dimension the change belongs to.
- **Observation unit:** `frame` — Edited output compared pixel-wise against its own input outside the declared edit region.
- **Applies to:** editing, image, video
- **Atomic probe:** Supply a source image and an edit instruction bounded to a declared region; measure change inside and outside that region separately.
- **Reusable from:** `reference_campaign_edit`, `product_packshot`, `person_plus_product_static`
- **Instrument:** deterministic CV/geometry, corroborated by structured visual VLM
- **Human verifier:** Adjudicates whether an out-of-region change is a genuine defect or a legitimate lighting consequence of the edit.
- **Instrument readiness:** `deterministic_ready` — deterministic — ready
- **Benchmark material:** `missing` — missing
- **Result form:** `structured_categorical`
- **Routing use:** `hard_constraint`

  **Difficulty ladder**

  1. background replaced, subject must be untouched
  2. one object's colour changed, all else untouched
  3. object removed and background plausibly filled
  4. text region edited while surrounding layout is preserved
  5. edit applied across frames of a clip with the rest preserved

  **Failure vocabulary:** `out_of_region_change`, `global_restyle`, `identity_lost_in_edit`, `text_corrupted_by_edit`, `edit_not_applied`.

  **Held fixed for comparability:** `resolution`, `edit_region_definition`, `edit_class`, `input_hash`, `diff_metric`, `diff_tolerance`

  **Note:** Largely deterministic - the input is ours, so a masked pixel difference outside the edit region is computable with no human label. The human is needed only for the legitimate-consequence question. A cheap and high-value dimension that is easy to overlook.

  **Production envelope:** Masked pixel difference against our own input needs no calibration, but no production-realistic edit material exists. Ready mechanism, absent material.


---

## D · Human & physical realism — the failures a customer notices instantly

### `anatomy_hands` — Hands, fingers and bodies are not broken

Human anatomy is structurally correct - finger count and articulation, limb count and joint direction, facial feature placement.

- **Covers:** Structural anatomical correctness of depicted humans.
- **Does not cover:** Whether it is the right person (person_identity) and whether the motion is plausible (motion_action_quality).
- **Observation unit:** `frame` — Per frame for images. For video, a declared frame sample - an anatomy defect may appear in only part of a clip, so the sample rate is recorded.
- **Applies to:** image, video, native_av, editing
- **Atomic probe:** Prompts that force hands into the frame at increasing difficulty - visible, holding, manipulating - with a plain background so the defect is unambiguous.
- **Reusable from:** `person_plus_product_static`, `actor_plus_product_vo`, `product_handoff_action`, `one_visible_speaker`, `two_person_dialogue`, `multi_shot_branded_ad`
- **Instrument:** structured visual VLM
- **Human verifier:** Required. This is a perceptual defect judgement and there is no deterministic oracle.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `constructed_by_eval` — Eval constructs it
- **Result form:** `structured_categorical`
- **Routing use:** `hard_constraint`

  **Difficulty ladder**

  1. person present, hands out of frame - control condition
  2. hands visible and relaxed
  3. hand holding an object
  4. hand manipulating an object, fingers articulated around it
  5. two people, four hands, at least one interaction

  **Failure vocabulary:** `extra_finger`, `missing_finger`, `fused_digits`, `extra_limb`, `joint_inversion`, `facial_feature_misplaced`, `merged_bodies`.

  **Held fixed for comparability:** `resolution`, `aspect_ratio`, `hand_visibility_class`, `n_people`, `sampled_frames`

  **Note:** No deterministic oracle exists. A VLM can be asked, but whether it RELIABLY detects a six-fingered hand is precisely what qualification must establish - and a false pass here is the dangerous direction. Human adjudication is required for the qualification set.

### `human_object_contact` — People hold and touch objects convincingly

Contact between a person and an object is physically coherent - the hand encloses the object, the object rests where it is held, there is no floating, interpenetration or impossible grip.

- **Covers:** Physical plausibility of the contact between person and object.
- **Does not cover:** Whether the object is the right product (product_identity) and whether the hand itself is anatomically correct (anatomy_hands).
- **Observation unit:** `frame` — Per frame for images; declared frame sample for video.
- **Applies to:** image, video, editing
- **Atomic probe:** One person, one object, one declared contact type, plain background.
- **Reusable from:** `person_plus_product_static`, `product_handoff_action`, `actor_plus_product_vo`, `multi_shot_branded_ad`
- **Instrument:** structured visual VLM
- **Human verifier:** Required.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `constructed_by_eval` — Eval constructs it
- **Result form:** `structured_categorical`
- **Routing use:** `hard_constraint`

  **Difficulty ladder**

  1. person and object in frame, no contact - control
  2. touching a static object
  3. holding an object with a full grip
  4. manipulating - opening, pouring, rotating
  5. passing an object between two people

  **Failure vocabulary:** `object_floating`, `hand_through_object`, `impossible_grip`, `contact_absent`, `object_merged_with_hand`.

  **Held fixed for comparability:** `resolution`, `aspect_ratio`, `contact_class`, `object_class`, `sampled_frames`

  **Note:** Recorded in CAPABILITY-BATTERY-V0-DRAFT section 4 as `required_but_no_calibrated_instrument`. Unchanged. Human adjudication required to build any qualification reference.

  **Production envelope:** Recorded in prior findings as required_but_no_calibrated_instrument. Unchanged.

### `human_human_interaction` — Two or more people occupy one scene coherently

Multiple people in one asset are separate, complete individuals with coherent relative scale, gaze and spatial relationship.

- **Covers:** Multi-person scene coherence - separation, scale, gaze, relative placement.
- **Does not cover:** Who the people are (person_identity) and who is speaking (two_speaker_turn_assignment_and_lip_sync).
- **Observation unit:** `frame` — Per frame for images; declared frame sample for video.
- **Applies to:** image, video, native_av
- **Atomic probe:** Two people, one declared relationship, plain setting.
- **Reusable from:** `two_person_dialogue`, `product_handoff_action`, `multi_shot_branded_ad`
- **Instrument:** structured visual VLM, corroborated by deterministic CV/geometry
- **Human verifier:** Required.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `constructed_by_eval` — Eval constructs it
- **Result form:** `structured_categorical`
- **Routing use:** `hard_constraint`

  **Difficulty ladder**

  1. two people, well separated, no interaction
  2. two people, mutual gaze
  3. two people at different depths, correct relative scale
  4. two people in physical contact, e.g. a handshake
  5. three or more people with a stated arrangement

  **Failure vocabulary:** `bodies_merged`, `limb_shared`, `scale_inconsistent`, `gaze_wrong`, `person_count_wrong`, `duplicate_face`.

  **Held fixed for comparability:** `resolution`, `aspect_ratio`, `n_people`, `interaction_class`, `depth_arrangement`

  **Note:** Person COUNT is deterministically checkable with a detector and overlaps object_count's instrument; the coherence judgement is not. Record the split rather than treating the whole dimension as equally uncertain.

### `motion_action_quality` — Movement looks like real movement

Motion within a clip is temporally coherent - gait, camera movement and object motion proceed plausibly rather than sliding, stuttering, teleporting or reversing.

- **Covers:** Plausibility and coherence of motion over time.
- **Does not cover:** Whether the prompted action happened at all (action_adherence) and whether materials look right (physics_material_appearance).
- **Observation unit:** `sequence` — Whole clip. Motion does not exist in a single frame and must never be scored from one.
- **Applies to:** video, native_av
- **Atomic probe:** One moving subject, one declared motion, static camera, plain background.
- **Reusable from:** `product_hero_video`, `actor_plus_product_vo`, `product_handoff_action`, `multi_shot_branded_ad`
- **Instrument:** temporal/video, corroborated by structured visual VLM
- **Human verifier:** Required.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `partial` — partial
- **Result form:** `human_hybrid_score`
- **Routing use:** `descriptive_only`

  **Difficulty ladder**

  1. static subject, camera push - camera motion only
  2. subject walks across frame, static camera
  3. subject and camera both moving
  4. object motion with a required trajectory, e.g. liquid pouring
  5. interaction motion between two entities

  **Failure vocabulary:** `foot_sliding`, `teleport`, `stutter`, `direction_reversal`, `morphing`, `frame_freeze`, `speed_implausible`.

  **Held fixed for comparability:** `resolution`, `aspect_ratio`, `clip_duration_s`, `fps`, `motion_class`, `camera_motion`, `sampled_frames`

  **Note:** Some components are deterministically measurable - optical-flow discontinuity and frame-freeze detection do not need a human. Whether the motion is PLAUSIBLE is a perceptual judgement. Deterministic perturbations of clean clips - injected freezes, reversals, jumps - give known-answer qualification material without any human label, and E3 designs exactly that.

### `physics_material_appearance` — Materials, light and shadow behave believably

Surfaces, reflections, shadows, liquids and cloth behave in a way that does not read as wrong - shadows fall consistently with the light, reflective surfaces reflect the scene, liquid has volume.

- **Covers:** Material and lighting plausibility, including shadow and reflection consistency.
- **Does not cover:** Exact brand colour (packaging_brand_colour_fidelity) and motion coherence (motion_action_quality).
- **Observation unit:** `frame` — Per frame for images; declared frame sample for video, since a lighting defect can appear intermittently.
- **Applies to:** image, video, native_av, editing
- **Atomic probe:** One object of a declared material under one declared lighting setup on a plain surface.
- **Reusable from:** `product_packshot`, `product_hero_video`, `person_plus_product_static`, `multi_shot_branded_ad`
- **Instrument:** structured visual VLM, corroborated by temporal/video
- **Human verifier:** Required.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `constructed_by_eval` — Eval constructs it
- **Result form:** `human_hybrid_score`
- **Routing use:** `descriptive_only`

  **Difficulty ladder**

  1. matte object, even lighting, visible contact shadow
  2. glossy object with a specular highlight
  3. transparent or liquid-containing object
  4. reflective surface that should reflect the scene
  5. multiple materials plus a directional key light with consistent shadows

  **Failure vocabulary:** `shadow_absent`, `shadow_direction_inconsistent`, `reflection_wrong`, `material_reads_wrong`, `liquid_volume_implausible`, `floating_object`.

  **Held fixed for comparability:** `resolution`, `aspect_ratio`, `material_class`, `lighting_setup`, `surface_class`

  **Note:** No deterministic oracle. Shadow-direction consistency across multiple objects is partially computable but was not attempted here and must not be claimed. Treat as descriptive evidence until an instrument is qualified.


---

## E · Temporal / continuity — defects that exist *between* frames

### `person_stability_in_clip` — The person does not morph during the clip

Within one generated clip, a person's face, hair, build and wardrobe remain the same person from first frame to last.

- **Covers:** Within-clip identity drift.
- **Does not cover:** Identity across SEPARATE generations (person_identity) and identity across cuts (multi_shot_spatial_continuity). Different units, different failures.
- **Observation unit:** `sequence` — Whole clip, with a declared frame sample rate. A drift that occurs between two sampled frames is invisible - the sample rate is therefore part of the measurement and is recorded in the Registry conditions.
- **Applies to:** video, native_av, lipsync
- **Atomic probe:** One person, static camera, plain background, clip at the declared maximum duration.
- **Reusable from:** `actor_plus_product_vo`, `one_visible_speaker`, `two_person_dialogue`, `product_handoff_action`, `multi_shot_branded_ad`
- **Instrument:** temporal/video, corroborated by structured visual VLM
- **Human verifier:** Adjudicates borderline drift.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `missing` — missing
- **Result form:** `structured_categorical`
- **Routing use:** `hard_constraint`

  **Difficulty ladder**

  1. short clip, static camera, minimal motion
  2. full-length clip, static camera
  3. subject turns or moves within the clip
  4. camera moves around the subject
  5. subject leaves frame and re-enters

  **Failure vocabulary:** `face_drift`, `wardrobe_change_mid_clip`, `hair_change_mid_clip`, `identity_swap`, `age_drift`.

  **Held fixed for comparability:** `resolution`, `aspect_ratio`, `clip_duration_s`, `fps`, `sampled_frames`, `camera_motion`, `subject_motion_class`

  **Note:** Qualification material can be built WITHOUT human labels by taking clean clips and injecting a known identity swap at a known frame - the answer is then true by construction, the same trick that made the Devanagari battery cheap. "Stability is not identity" - a clip that is perfectly stable on the WRONG person passes this dimension and fails person_identity. Both must be reported.

### `product_stability_in_clip` — The product does not change shape during the clip

Within one clip, a product's shape, label, proportions and colour remain constant.

- **Covers:** Within-clip product drift.
- **Does not cover:** Product identity across separate generations (product_identity) and brand colour accuracy at a point in time (packaging_brand_colour_fidelity).
- **Observation unit:** `sequence` — Whole clip at a declared frame sample rate.
- **Applies to:** video, native_av
- **Atomic probe:** One product, static camera, plain background, full-length clip.
- **Reusable from:** `product_hero_video`, `actor_plus_product_vo`, `product_handoff_action`, `multi_shot_branded_ad`
- **Instrument:** temporal/video, corroborated by structured visual VLM
- **Human verifier:** Adjudicates borderline drift.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `missing` — missing
- **Result form:** `structured_categorical`
- **Routing use:** `hard_constraint`

  **Difficulty ladder**

  1. static product, static camera
  2. product rotates
  3. camera orbits the product
  4. product is picked up and handled
  5. product passes behind an occluder and re-emerges

  **Failure vocabulary:** `shape_drift`, `label_drift`, `colour_drift_mid_clip`, `feature_appears`, `feature_disappears`, `product_swap`.

  **Held fixed for comparability:** `resolution`, `aspect_ratio`, `clip_duration_s`, `fps`, `sampled_frames`, `camera_motion`, `occlusion_present`

  **Note:** Same construction trick as person_stability_in_clip - inject a known product swap into a clean clip. Re-emergence after occlusion at level 5 is the commercially important case and the one most likely to fail.

### `text_logo_stability_in_clip` — On-screen text and logos stay the same through the clip

A string or mark rendered in a clip is identical in every frame it appears in - it does not mutate, flicker, re-spell itself or drift.

- **Covers:** Within-clip constancy of rendered text and marks.
- **Does not cover:** Whether the text was correct in the first place (exact_text_latin, exact_text_devanagari).
- **Observation unit:** `sequence` — Whole clip at a declared frame sample rate. THIS IS THE DIMENSION THAT PROVES WHY THE UNIT RULE EXISTS - a misspelling that changes partway through a clip does not exist in any single frame. Frame-level scoring cannot see it, however accurate the checker is.
- **Applies to:** video, native_av, editing
- **Atomic probe:** Request a fixed string on screen for the whole clip duration; transcribe every sampled frame; compare the sampled transcriptions to each other AND to the target.
- **Reusable from:** `product_hero_video`, `multi_shot_branded_ad`, `actor_plus_product_vo`
- **Instrument:** temporal/video, corroborated by text/OCR
- **Human verifier:** None for the comparison; the Devanagari target-validity question is inherited from exact_text_devanagari.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `missing` — missing
- **Result form:** `exact_pass_fail`
- **Routing use:** `hard_constraint`

  **Difficulty ladder**

  1. short Latin word, static, full duration
  2. Devanagari word, static, full duration
  3. text on a moving surface or with camera movement
  4. text plus logo present together
  5. text persisting across a shot change

  **Failure vocabulary:** `text_mutates_mid_clip`, `text_flickers`, `text_disappears`, `logo_drifts`, `text_wrong_from_first_frame`.

  **Held fixed for comparability:** `resolution`, `aspect_ratio`, `clip_duration_s`, `fps`, `sampled_frames`, `script`, `string_length_words`

  **Note:** Depends on the text/OCR family, which is unqualified, applied per sampled frame. IMPORTANT - two different failures share this dimension and must be recorded apart. Text wrong in EVERY frame is an exact-text failure. Text correct then changing is a STABILITY failure. Collapsing them would credit a model that got it right once and then destroyed it. This is a project-observed failure - Devanagari corruption drifting WITHIN a single clip is recorded in CAPABILITY-LAB-V0-PLAN as a prior observation, which makes it a permanent regression case.

### `multi_shot_spatial_continuity` — Separate shots cut together without contradicting each other

Across two or more shots intended to sit next to each other, the setting, lighting, wardrobe, product placement and screen direction remain consistent.

- **Covers:** Continuity BETWEEN shots.
- **Does not cover:** Continuity within a single shot (the *_stability_in_clip dimensions).
- **Observation unit:** `shot_pair` — Pairs of shots, evaluated as pairs. A single shot cannot exhibit this defect at all - the unit is the pair, and this is the second dimension whose defect is structurally invisible at any smaller unit.
- **Applies to:** video, native_av
- **Atomic probe:** Generate two shots of the same declared setting and subject intended to cut together, then evaluate the pair.
- **Reusable from:** `multi_shot_branded_ad`, `product_handoff_action`, `two_person_dialogue`
- **Instrument:** temporal/video, corroborated by structured visual VLM
- **Human verifier:** Required. Continuity is a craft judgement with established professional vocabulary.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `partial` — partial
- **Result form:** `human_hybrid_score`
- **Routing use:** `hard_constraint`

  **Difficulty ladder**

  1. two shots, same setting, no subject
  2. two shots with the same subject
  3. two shots with a required screen-direction match
  4. three or more shots forming a sequence
  5. sequence with a required continuity of product state, e.g. box open in shot 2 after being opened in shot 1

  **Failure vocabulary:** `setting_changed`, `lighting_mismatch`, `wardrobe_mismatch`, `screen_direction_flipped`, `product_state_inconsistent`, `subject_identity_changed_across_cut`.

  **Held fixed for comparability:** `resolution`, `aspect_ratio`, `n_shots`, `shot_generation_method`, `continuity_requirement_class`

  **Note:** Canon owns what good continuity MEANS; Eval measures whether a workflow achieves it. Eval must consume Canon's continuity vocabulary rather than invent its own. Deterministic perturbation is available for some sub-cases - flipping one shot horizontally creates a known screen-direction violation with no human label needed.


---

## F · Speech / audio

### `spoken_language_correctness` — The voice says the right words in the right language

Generated speech says the requested script, in the requested language, with correct pronunciation - including Hindi and Hinglish code-mixing, where an English word inside a Hindi sentence must still be pronounced correctly.

- **Covers:** Word-level correctness of the spoken script, language identity and pronunciation.
- **Does not cover:** Whether the mouth matches (single_speaker_lip_sync) and whether the emotion fits (emotional_prosodic_fit).
- **Observation unit:** `whole_asset` — Audio track of the whole asset, transcribed and compared against the requested script.
- **Applies to:** tts, native_av, lipsync
- **Atomic probe:** Supply an exact script, generate audio, transcribe with a qualified ASR instrument, compare against the script under a declared normalisation.
- **Reusable from:** `one_visible_speaker`, `two_person_dialogue`, `actor_plus_product_vo`, `product_hero_video`, `multi_shot_branded_ad`
- **Instrument:** speech/audio/AV
- **Human verifier:** A first-language listener confirms pronunciation acceptability. Word correctness is machine-comparable; PRONUNCIATION is not, and must not be inferred from a matching transcript.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `missing` — missing
- **Result form:** `exact_pass_fail`
- **Routing use:** `hard_constraint`

  **Difficulty ladder**

  1. short English sentence
  2. short Hindi sentence
  3. Hinglish code-mixed sentence
  4. script containing a brand name and a number or price
  5. full 15-20 second voiceover with mixed script and a required emphasis

  **Failure vocabulary:** `word_substituted`, `word_dropped`, `wrong_language`, `mispronounced`, `brand_name_mispronounced`, `number_misread`, `code_switch_failed`.

  **Held fixed for comparability:** `language`, `script_system`, `script_length_words`, `sample_rate`, `normalisation_ref`, `asr_instrument_ref`

  **Note:** A TRAP that mirrors the founding Devanagari lesson - a transcript matching the script proves the WORDS were right, not that they were pronounced acceptably. An ASR system trained to be robust will happily normalise a mispronunciation into the correct word, exactly as the vision checker silently corrected a misspelling. Word correctness and pronunciation acceptability are therefore recorded as SEPARATE results with separate instruments, never as one number.

### `single_speaker_lip_sync` — The mouth matches the words, one speaker

For one visible speaker, mouth movement corresponds to the audio being spoken, in time and in shape.

- **Covers:** Audio-visual correspondence of mouth movement for a single speaker.
- **Does not cover:** Whether the words are right (spoken_language_correctness) and global A/V offset (audio_video_synchronisation).
- **Observation unit:** `sequence` — Whole clip; the audio track and the video track evaluated jointly.
- **Applies to:** lipsync, native_av
- **Atomic probe:** One visible speaker, frontal, static camera, known script, clip at declared duration.
- **Reusable from:** `one_visible_speaker`, `two_person_dialogue`, `multi_shot_branded_ad`
- **Instrument:** speech/audio/AV, corroborated by temporal/video
- **Human verifier:** Required for the acceptability judgement; deterministic offset is machine-measurable.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `missing` — missing
- **Result form:** `human_hybrid_score`
- **Routing use:** `hard_constraint`

  **Difficulty ladder**

  1. frontal, short English utterance
  2. frontal, Hindi utterance
  3. three-quarter angle
  4. speaker moving or camera moving during speech
  5. full-length utterance with pauses and emphasis

  **Failure vocabulary:** `mouth_static`, `sync_drift`, `viseme_mismatch`, `mouth_moves_without_audio`, `audio_without_mouth_movement`.

  **Held fixed for comparability:** `resolution`, `fps`, `clip_duration_s`, `language`, `speaker_angle`, `audio_sample_rate`

  **Note:** Needs the planned 24 single-speaker clean AV clips with transcripts. DO NOT invent a millisecond tolerance for "acceptable sync". Propose a calibration curve from known injected offsets first and let the data say where acceptability breaks down. Inventing a threshold now would encode a guess as a finding - the same error the project already paid for with statistical bounds.

### `two_speaker_turn_assignment_and_lip_sync` — With two people, the right person's mouth moves

In a two-speaker asset, each line of dialogue is delivered by the correct visible speaker, and only that speaker's mouth moves during their turn.

- **Covers:** Turn-to-speaker assignment plus per-speaker lip sync.
- **Does not cover:** Single-speaker sync (single_speaker_lip_sync) and whether the people are distinct individuals (person_identity, human_human_interaction).
- **Observation unit:** `sequence` — Whole clip, segmented by declared turn boundaries.
- **Applies to:** lipsync, native_av
- **Atomic probe:** Two visible speakers, a script with explicit turn boundaries, both speakers in frame throughout so a wrong assignment is observable.
- **Reusable from:** `two_person_dialogue`, `multi_shot_branded_ad`
- **Instrument:** speech/audio/AV, corroborated by temporal/video
- **Human verifier:** Required.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `missing` — missing
- **Result form:** `structured_categorical`
- **Routing use:** `hard_constraint`

  **Difficulty ladder**

  1. two turns, one each, both speakers in frame
  2. four alternating turns
  3. turns with a short overlap or interruption
  4. turns across a shot change
  5. turns in Hinglish with differing speaker genders or ages

  **Failure vocabulary:** `turn_assigned_to_wrong_speaker`, `both_mouths_move`, `neither_mouth_moves`, `turn_order_wrong`, `turn_merged`, `speaker_voice_swapped`.

  **Held fixed for comparability:** `resolution`, `fps`, `clip_duration_s`, `language`, `n_turns`, `both_speakers_in_frame`, `turn_boundary_ref`

  **Note:** Needs the planned 12 two-speaker clean AV clips WITH turn boundaries - the boundaries are what make wrong assignment machine-detectable. Qualification material can be built deterministically by swapping the speaker channels in a clean clip - a known-wrong answer with no human label. A recorded provider-shaped failure already exists in this area - a provider changed valid speaker names between versions - so `error_classes` must be recorded, not treated as noise.

  **Production envelope:** Turn boundaries are what make a wrong speaker assignment machine-detectable. Without them the envelope collapses to single-speaker sync.

### `emotional_prosodic_fit` — The delivery sounds right for the ad

Tone, pace, emphasis and energy of the delivery suit the requested register - warm and reassuring, urgent and promotional, calm and premium.

- **Covers:** Suitability of prosodic delivery to the requested register.
- **Does not cover:** Word correctness (spoken_language_correctness) and sync (single_speaker_lip_sync).
- **Observation unit:** `whole_asset` — Audio track of the whole asset.
- **Applies to:** tts, native_av, lipsync
- **Atomic probe:** One script delivered under several requested registers; the measurable question is whether the registers are DISTINGUISHABLE and correctly identified, not whether one is 'good'.
- **Reusable from:** `one_visible_speaker`, `actor_plus_product_vo`, `product_hero_video`, `two_person_dialogue`
- **Instrument:** speech/audio/AV, corroborated by creative/commercial
- **Human verifier:** Required. This is a preference-shaped judgement, not a right answer.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `missing` — missing
- **Result form:** `pairwise_preference`
- **Routing use:** `descriptive_only`

  **Difficulty ladder**

  1. neutral read
  2. two clearly contrasting registers on the same script
  3. register with a required emphasis on a named word
  4. register sustained across a full 20-second read
  5. register shift partway through, e.g. calm then urgent call-to-action

  **Failure vocabulary:** `register_absent`, `register_wrong`, `flat_delivery`, `emphasis_misplaced`, `pace_wrong`, `register_not_sustained`.

  **Held fixed for comparability:** `language`, `script_length_words`, `requested_register`, `sample_rate`

  **Note:** There is no right answer here, so this is deliberately DESCRIPTIVE ONLY and may never be a hard routing constraint. The honest measurable form is discrimination - can listeners or a qualified instrument tell the requested registers apart, and does the requested one get identified? That is testable; "is this delivery good" is not.

### `audio_video_synchronisation` — Sound and picture line up

Global alignment between the audio track and the video track - the sound of a bottle being placed happens when the bottle lands.

- **Covers:** Global A/V offset and drift over the clip.
- **Does not cover:** Mouth-shape correspondence (single_speaker_lip_sync), which is a finer judgement than global offset.
- **Observation unit:** `whole_asset` — Both tracks of the whole asset; offset measured at start, middle and end to detect drift.
- **Applies to:** native_av, lipsync, video
- **Atomic probe:** A clip with a sharp, unambiguous audio-visual event - a clap or an impact - whose visual and audio onsets can both be located precisely.
- **Reusable from:** `one_visible_speaker`, `two_person_dialogue`, `product_handoff_action`, `multi_shot_branded_ad`
- **Instrument:** speech/audio/AV
- **Human verifier:** Sets the acceptability threshold once from a calibration curve; does not judge per item.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `missing` — missing
- **Result form:** `operational_metric`
- **Routing use:** `hard_constraint`

  **Difficulty ladder**

  1. single sharp event, short clip
  2. single event in a full-length clip
  3. several events across the clip - detects drift, not just offset
  4. continuous speech rather than discrete events
  5. sync maintained across a shot change

  **Failure vocabulary:** `constant_offset`, `progressive_drift`, `audio_absent`, `audio_truncated`, `video_truncated`, `offset_after_cut`.

  **Held fixed for comparability:** `fps`, `audio_sample_rate`, `clip_duration_s`, `event_class`, `measurement_points`

  **Note:** The most deterministic dimension in family F. Onset detection on both tracks gives a measured offset in milliseconds with no human label, and known offsets can be INJECTED into clean clips to qualify the instrument exactly. What still needs a human decision is the ACCEPTABILITY threshold - report the measured offset as the primary result and treat any pass/fail line as a separately declared, Controller-approved parameter.

  **Production envelope:** SPLIT ENVELOPE, and the reason this is not `deterministic_ready`. Computing the OFFSET between two located onsets is deterministic arithmetic. LOCATING the visual onset is not: on a constructed fixture with a sharp clap it is trivial, but in arbitrary production content "the moment the bottle lands" needs an event detector, which is a model. So the mechanism is deterministic only inside the fixture envelope, and the qualification must establish event localisation before any production claim. Reported primary result stays the MEASURED OFFSET in milliseconds; any pass/fail line is a separately declared, Controller-approved parameter. Material is additionally missing - the project holds no audio at all.


---

## G · Commercial / creative fitness — descriptive only, never a hard gate

### `proposition_objective_fit` — The ad actually communicates what it was supposed to

A viewer takes away the intended proposition and the intended action from the asset - the objective stated in the brief is the objective a viewer perceives.

- **Covers:** Whether the intended message and objective are conveyed.
- **Does not cover:** Whether the copy is spelled right (exact_text_*) and whether the product is the right product (product_identity).
- **Observation unit:** `whole_asset` — The finished asset as a customer would see it, at delivery size.
- **Applies to:** image, video, native_av
- **Atomic probe:** NOT atomic. This dimension is only meaningful on a complete commercial asset generated against a real brief, and is therefore compound-only.
- **Reusable from:** `typography_led_image`, `person_plus_product_static`, `product_hero_video`, `multi_shot_branded_ad`, `actor_plus_product_vo`
- **Instrument:** creative/commercial
- **Human verifier:** Required, and it must be FRESH INDEPENDENT human review. Public or source preference labels are one party's observations and are never our creative truth.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `missing` — missing
- **Result form:** `pairwise_preference`
- **Routing use:** `descriptive_only`

  **Difficulty ladder**

  1. single explicit proposition, product plus claim
  2. proposition plus a specific call to action
  3. proposition requiring an implied benefit rather than a stated one
  4. proposition plus audience-appropriate register
  5. proposition carried across a multi-shot narrative

  **Failure vocabulary:** `proposition_absent`, `proposition_wrong`, `cta_absent`, `benefit_unclear`, `audience_mismatch`, `message_contradicted_by_image`.

  **Held fixed for comparability:** `brief_ref`, `delivery_size_declared`, `asset_modality`, `reviewer_pool_ref`

  **Note:** Depends on Canon's 30-brief bank, which Eval must NOT independently author, and on Resources' 60 active commercial assets. Measure by pairwise comparison or structured issue-detection, not by an absolute score - "is this ad any good" has no right answer, but "which of these two better conveys the stated proposition" is answerable and repeatable. FALSE CRITICISM must be measured alongside detection - an instrument that flags problems in flawless work is as useless as one that misses them.

### `hierarchy_product_as_hero` — The product is the thing you look at first

Visual hierarchy places the intended subject - usually the product or the key message - as the dominant element, rather than burying it behind a model, a background or decoration.

- **Covers:** Whether the intended hero element dominates attention.
- **Does not cover:** Whether the product is correctly rendered (product_identity) and whether text is legible (typography_legibility).
- **Observation unit:** `whole_asset` — The finished asset at delivery size.
- **Applies to:** image, video, native_av
- **Atomic probe:** NOT atomic in the commercial sense. A controlled probe CAN vary the hero element's size, placement and contrast systematically to test whether an instrument detects the intended hierarchy at all.
- **Reusable from:** `product_packshot`, `person_plus_product_static`, `typography_led_image`, `product_hero_video`, `multi_shot_branded_ad`
- **Instrument:** creative/commercial, corroborated by deterministic CV/geometry
- **Human verifier:** Required.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `missing` — missing
- **Result form:** `pairwise_preference`
- **Routing use:** `descriptive_only`

  **Difficulty ladder**

  1. product isolated, plain background
  2. product with a supporting element
  3. product plus person, product must still dominate
  4. product plus person plus text block
  5. hero maintained across a multi-shot sequence

  **Failure vocabulary:** `hero_subordinate`, `model_dominates`, `background_dominates`, `text_dominates_product`, `hero_cropped`, `attention_split`.

  **Held fixed for comparability:** `brief_ref`, `delivery_size_declared`, `asset_modality`, `hero_element_declared`, `reviewer_pool_ref`

  **Note:** Canon owns what hierarchy MEANS - Eval consumes that definition and must not re-derive it. Partially instrumentable - relative area, centrality and contrast of the declared hero region are computable. Whether that constitutes hierarchy is a craft judgement. Record the computable components separately from the judgement so the two are never confused.

### `composition_brand_register` — It looks like it belongs to this brand, at this quality level

Composition, styling, colour treatment and production values sit in the register the brand requires - premium, mass-market, playful, clinical - rather than merely being technically correct.

- **Covers:** Compositional quality and register appropriateness.
- **Does not cover:** Exact brand colour values (packaging_brand_colour_fidelity) and mark geometry (logo_wordmark_fidelity), which are hard-fidelity questions.
- **Observation unit:** `whole_asset` — The finished asset at delivery size.
- **Applies to:** image, video, native_av
- **Atomic probe:** NOT atomic. Compound-only.
- **Reusable from:** `typography_led_image`, `product_packshot`, `person_plus_product_static`, `product_hero_video`, `multi_shot_branded_ad`
- **Instrument:** creative/commercial
- **Human verifier:** Required, fresh and independent.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `missing` — missing
- **Result form:** `pairwise_preference`
- **Routing use:** `descriptive_only`

  **Difficulty ladder**

  1. single declared register, simple composition
  2. register plus a stated compositional constraint
  3. register maintained with a person in frame
  4. two contrasting registers on the same product - tests discrimination
  5. register sustained across a multi-shot sequence

  **Failure vocabulary:** `register_mismatch`, `composition_unbalanced`, `styling_generic`, `production_value_low`, `visual_cliche`, `crop_awkward`.

  **Held fixed for comparability:** `brief_ref`, `delivery_size_declared`, `asset_modality`, `declared_register`, `reviewer_pool_ref`

  **Note:** The most subjective dimension in the contract and the one most at risk of producing a confident-looking number that means nothing. Discrimination framing at level 4 is the honest test - can the register be told apart and correctly identified. HARD-FIDELITY AND CREATIVE-QUALITY CHECKS ARE SEPARATE INSTRUMENTS AND MUST NOT BE MERGED - one evaluator cannot honestly answer both "is this spelled correctly" and "is this any good".

### `hook_pacing_temporal_hierarchy` — The video grabs attention early and holds it

A short video establishes its hook in the opening seconds and paces its information so the proposition and call to action land within the duration.

- **Covers:** Temporal structure of attention and information delivery in a short video.
- **Does not cover:** Motion plausibility (motion_action_quality) and shot-to-shot continuity (multi_shot_spatial_continuity).
- **Observation unit:** `sequence` — Whole clip, with the opening window evaluated separately from the remainder.
- **Applies to:** video, native_av
- **Atomic probe:** NOT atomic. Compound-only, and only on video.
- **Reusable from:** `product_hero_video`, `actor_plus_product_vo`, `one_visible_speaker`, `multi_shot_branded_ad`
- **Instrument:** creative/commercial, corroborated by temporal/video
- **Human verifier:** Required, fresh and independent.
- **Instrument readiness:** `blocked_pending_qualification` — blocked — not qualified
- **Benchmark material:** `missing` — missing
- **Result form:** `pairwise_preference`
- **Routing use:** `descriptive_only`

  **Difficulty ladder**

  1. single-shot 6-second clip with one message
  2. single-shot clip with hook plus call to action
  3. two-shot 10-15 second clip
  4. multi-shot 15-20 second clip with a required beat structure
  5. multi-shot clip with hook, demonstration, proposition and call to action all landing within duration

  **Failure vocabulary:** `hook_absent`, `hook_late`, `pacing_flat`, `cta_missing`, `cta_too_late`, `information_overloaded`, `dead_opening`.

  **Held fixed for comparability:** `brief_ref`, `clip_duration_s`, `n_shots`, `asset_modality`, `reviewer_pool_ref`

  **Note:** Canon owns temporal hierarchy as a craft concept. Some structure is computable - shot-boundary timings, when the product first appears, when on-screen text first appears - and those measurements are worth recording independently of the judgement, because they are reproducible and the judgement is not.


---

## H · Operational / workflow behaviour — derived, never generates its own trials

### `reliability_pass_at_k` — How often it works, and how many tries it takes

For a given capability and difficulty level, the proportion of attempts that pass, and the probability of at least one pass within k attempts.

- **Covers:** Pass rate per independent base item, and pass-at-k derived from repeats.
- **Does not cover:** What the failures were (each capability's own failure vocabulary) and what they cost (cost_and_cpao).
- **Observation unit:** `asset_set_over_time` — Computed across the repeats of each base item. THE COUNTING RULE IS THE DIMENSION - confidence is computed on independent BASE ITEMS, never on trials and never on frames.
- **Applies to:** image, video, native_av, lipsync, tts, editing
- **Atomic probe:** None of its own. Derived entirely from the trials that other dimensions already generated.
- **Reusable from:** every compound scenario
- **Instrument:** operational logging (no instrument)
- **Human verifier:** *none*
- **Instrument readiness:** `deterministic_ready` — deterministic — ready
- **Benchmark material:** `no_external_stimulus_required` — none needed
- **Result form:** `operational_metric`
- **Routing use:** `hard_constraint`

  **Difficulty ladder**

  1. pass rate at 1 attempt
  2. pass-at-2
  3. pass-at-4
  4. pass rate reported per difficulty level of the parent capability
  5. pass rate under a full production recipe rather than a single call

  **Failure vocabulary:** Inherited from the parent capability. This dimension adds no vocabulary of its own.

  **Held fixed for comparability:** `parent_dimension`, `difficulty_level`, `n_items`, `repeats_per_item`, `seed_policy`

  **Note:** Zero marginal generation cost - it is arithmetic over trials that already exist. THE TRAP - repeats are not independent items. A 96% pass rate over 2 repeats of 3 items is not a 96% pass rate. n_items and repeats_per_item are BOTH mandatory in every Registry row so this can never be silently misread. Reporting a pass rate without n_items is a defect, not a style choice.

  **Production envelope:** Mechanism ready, but it is DERIVED - it has no value until real trials exist. Zero generations have been run, so the envelope is empty rather than blocked.

### `cost_and_cpao` — What an ACCEPTED result actually costs

Total cost to reach an output that passes its acceptance requirements - including failed attempts, evaluator calls and human review time, not just the price of one generation.

- **Covers:** Generation cost, transform cost, evaluator cost, human verification cost, retry cost, and cost per accepted outcome.
- **Does not cover:** Whether the output was any good - that is every other dimension.
- **Observation unit:** `asset_set_over_time` — Aggregated across all attempts required to reach an accepted outcome.
- **Applies to:** image, video, native_av, lipsync, tts, editing
- **Atomic probe:** None of its own. Derived from logged costs on trials other dimensions generated.
- **Reusable from:** every compound scenario
- **Instrument:** operational logging (no instrument)
- **Human verifier:** Supplies the human-time rate; does not judge per item.
- **Instrument readiness:** `deterministic_ready` — deterministic — ready
- **Benchmark material:** `no_external_stimulus_required` — none needed
- **Result form:** `operational_metric`
- **Routing use:** `hard_constraint`

  **Difficulty ladder**

  1. cost per successful call
  2. cost per accepted outcome including retries
  3. including evaluator cost
  4. including human verification time
  5. cost per accepted outcome for a complete production recipe end to end

  **Failure vocabulary:** Not applicable - this dimension records cost, not defects.

  **Held fixed for comparability:** `currency`, `price_source`, `price_read_date`, `component_breakdown`, `human_rate_assumption`

  **Note:** THIS IS THE PROJECT'S PRIMARY LONG-TERM METRIC and the most commonly mis-stated. Three rules carried from prior evidence - (1) HUMAN CHECKING, NOT API SPEND, IS LIKELY TO DOMINATE. The original cost model left it out entirely. Any ratio quoted before we have measured it is an ILLUSTRATIVE SCENARIO, not a finding. (2) EVALUATOR COST IS NOT HIDDEN INSIDE GENERATION COST. At roughly one rupee per VLM check, evaluation can exceed a third of the true cost of observing a cheap generation. (3) THE ZERO-PASS RULE. When passes == 0, cost per pass is null - never infinity, never a large sentinel - and the cell cost goes in a lower-bound field. "Never observed to pass in N trials" and "expensive per pass" are different facts about the world.

  **Production envelope:** Mechanism ready and derived. Note the envelope gap that matters: human verification cost is expected to dominate and has no approved rate, so CpAO cannot be completed from generation and evaluator costs alone.

### `latency_errors_refusals` — How slow it is, how often it breaks, how often it says no

Wall-clock latency distribution, API error rate by class, and content refusal or moderation-block rate.

- **Covers:** Latency p50 and p95, error classes and counts, refusal and moderation rates.
- **Does not cover:** Whether the returned output was correct.
- **Observation unit:** `asset_set_over_time` — Logged on every API interaction, including ones that returned nothing usable.
- **Applies to:** image, video, native_av, lipsync, tts, editing
- **Atomic probe:** None of its own. Logged as a free rider on every call any dimension makes.
- **Reusable from:** every compound scenario
- **Instrument:** operational logging (no instrument)
- **Human verifier:** *none*
- **Instrument readiness:** `deterministic_ready` — deterministic — ready
- **Benchmark material:** `no_external_stimulus_required` — none needed
- **Result form:** `operational_metric`
- **Routing use:** `hard_constraint`

  **Difficulty ladder**

  1. latency p50 on the default configuration
  2. p50 and p95 together
  3. error rate broken down by error class
  4. refusal rate on commercially ordinary content
  5. behaviour under sustained load or rate limiting

  **Failure vocabulary:** `4xx`, `5xx`, `timeout`, `rate_limited`, `moderation_block`, `content_refusal`, `malformed_response`, `truncated_output`.

  **Held fixed for comparability:** `region`, `concurrency`, `time_of_day_window`, `retry_policy`, `request_size`

  **Note:** Costs nothing extra - every call already produces this data, and a call that FAILS still produces it. A p50 alone hides the timeout tail that decides whether a workflow is usable interactively, so p95 is mandatory. Refusals must be reported separately and never folded into a pass or fail verdict - "the model refused" and "the model tried and got it wrong" are different facts with different routing consequences. A recorded prior failure - a provider changed valid speaker names between versions - shows error classes are schema-shaped information, not noise.

  **Production envelope:** Mechanism ready and derived; every call produces this data, including calls that fail. Empty until real calls are made.

### `reproducibility_repairability` — Does it do the same thing twice, and can a failure be fixed

Whether repeated identical requests produce equivalent results, whether seeds are supported and honoured, and whether a failed output can be repaired by a further call rather than discarded.

- **Covers:** Repeat agreement, seed support and honouring, and repair success rate and cost.
- **Does not cover:** First-attempt pass rate (reliability_pass_at_k).
- **Observation unit:** `asset_set_over_time` — Repeats of one item compared with each other; repair attempts linked to their parent failed attempt.
- **Applies to:** image, video, native_av, lipsync, tts, editing
- **Atomic probe:** None of its own. Derived from repeats and from repair attempts on already-generated failures.
- **Reusable from:** every compound scenario
- **Instrument:** operational logging (no instrument)
- **Human verifier:** *none*
- **Instrument readiness:** `deterministic_ready` — deterministic — ready
- **Benchmark material:** `no_external_stimulus_required` — none needed
- **Result form:** `operational_metric`
- **Routing use:** `descriptive_only`

  **Difficulty ladder**

  1. seed supported yes or no, as documented and as observed
  2. repeat agreement with a fixed seed
  3. repeat agreement with no seed control
  4. repair success rate on a failed output
  5. repair success rate by failure class - which defects are cheaply fixable

  **Failure vocabulary:** `seed_unsupported`, `seed_ignored`, `repeat_divergent`, `repair_failed`, `repair_introduced_new_defect`.

  **Held fixed for comparability:** `seed_policy`, `repeats_per_item`, `repair_strategy_ref`, `parent_failure_class`

  **Note:** Repeat agreement is cheap and depends only on repeats already budgeted. REPAIR IS DIFFERENT - measuring repair requires a repair loop that DOES NOT EXIST YET, and repair attempts are additional generations that must be budgeted explicitly rather than smuggled in under the generate-once rule. The generate-once rule says do not regenerate to satisfy another EVALUATOR; a repair attempt is a genuinely new trial and is recorded as a new attempt id linked to its parent. Repair matters commercially because a cheaply-repairable failure and a total loss are not equivalent, and routing should be able to prefer the former - but that field stays null until a repair loop exists to measure.

  **Production envelope:** SPLIT ENVELOPE. Repeat agreement is deterministic arithmetic over repeats we already budget, and is ready. REPAIR is not: measuring it requires a repair loop that DOES NOT EXIST, and repair attempts are additional generations that must be budgeted explicitly rather than smuggled in under generate-once. The repair fields stay null until that loop exists.


---

## Proposed changes — raised, not applied

The 36 capability ids remain exactly as the Controller froze them. These are proposals for review.

**PC-01 · `CROSS_STREAM` → Canon — Observation-unit vocabulary has no audio term**

SPEC-04's list - frame, shot, shot_pair, sequence, whole_asset, asset_set_over_time - is visual. Family F dimensions use `whole_asset` with an Eval-local `observation_span_detail` naming the audio track. That works but is a workaround. Canon may wish to add an audio-track or time-span unit. Eval has NOT added one and will not.

**PC-02 · `LOCAL` — Two distinct failures share text_logo_stability_in_clip**

Text wrong in every frame is an exact-text failure; text correct and then changing is a stability failure. The contract records them apart in the failure vocabulary. If the Controller prefers, this could be split into two dimensions - that WOULD change the frozen 36 and is therefore raised rather than done.

**PC-03 · `LOCAL` — Thresholds and tolerances that must be approved before any run**

Several dimensions need a declared tolerance that has no empirical basis yet - colour difference tolerance, A/V sync acceptability in milliseconds, legibility contrast, edit out-of-region diff tolerance. Each is a judgement call. They must be declared and approved BEFORE a run. Changing one after seeing results is an EXPERIMENT MUTATION stop.

**PC-04 · `CROSS_STREAM` → Controller — Registry needs an explicit unmeasurable state, already drafted**

11 of 36 dimensions are blocked pending an instrument and 9 pending a resource. The V0 Registry draft already proposes `calibration_status: required_but_no_calibrated_instrument` for exactly this. It remains UNAPPROVED. Without it, a dimension with no instrument silently disappears and later reads as "we decided this did not matter".

**PC-05 · `LOCAL` — Family G may never be a hard routing constraint**

All four commercial/creative dimensions are marked descriptive_only. Recorded explicitly so a later Planner cannot treat a preference score as a hard gate.

