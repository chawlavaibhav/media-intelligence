# Capability V1 → V2 mapping

> **GENERATED** from `CAPABILITY-CONTRACT-v2.yaml`. **V1 is not modified.**

**Task:** EVAL-009 / E9-A · **Date:** 26 Aug 2026 · **Status:** `PROPOSED_FOR_CONTROLLER_FREEZE_NOT_IN_FORCE`

## The count is an output, not a target

| | |
|---|---:|
| V1 capabilities | **36** |
| V2 capabilities | **44** |
| — active | 43 |
| — dormant | 1 |

Arithmetic: **36 + 4 (splits) + 4 (added) = 44**. 22 unchanged, 9 refined in place, 1 renamed.

**No target count was aimed at.** Every change traces to a Controller-approved direction or to the admission bar below. Nothing was added to reach a number.

## The admission bar for a new capability

> A new capability is admitted **only** where existing capability + condition + observation scope cannot represent the failure cleanly.

**Three candidate concepts were rejected under this bar** — see the last section. That is the bar doing its job: it is only credible if it sometimes says no.


---

## Every V1 id, with its disposition

| V1 id | Disposition | V2 id(s) |
|---|---|---|
| `object_count` | **unchanged** | `object_count` |
| `attribute_binding` | **unchanged** | `attribute_binding` |
| `spatial_relationship` | **split** | `spatial_relationship_2d`, `spatial_relationship_depth` |
| `action_adherence` | **unchanged** | `action_adherence` |
| `delivery_format_compliance` | **refined** | `delivery_format_compliance` |
| `exact_text_latin` | **unchanged** | `exact_text_latin` |
| `exact_text_devanagari` | **unchanged** | `exact_text_devanagari` |
| `typography_legibility` | **refined** | `typography_legibility` |
| `logo_wordmark_fidelity` | **unchanged** | `logo_wordmark_fidelity` |
| `packaging_brand_colour_fidelity` | **refined** | `packaging_brand_colour_fidelity` |
| `person_identity` | **split** | `person_identity`, `wardrobe_invariant_fidelity` |
| `product_identity` | **unchanged** | `product_identity` |
| `reference_conditioning` | **refined** | `reference_conditioning` |
| `edit_preservation` | **unchanged** | `edit_preservation` |
| `anatomy_hands` | **renamed** | `human_anatomy_integrity` |
| `human_object_contact` | **unchanged** | `human_object_contact` |
| `human_human_interaction` | **unchanged** | `human_human_interaction` |
| `motion_action_quality` | **refined** | `motion_action_quality` |
| `physics_material_appearance` | **refined** | `physics_material_appearance` |
| `person_stability_in_clip` | **unchanged** | `person_stability_in_clip` |
| `product_stability_in_clip` | **unchanged** | `product_stability_in_clip` |
| `text_logo_stability_in_clip` | **unchanged** | `text_logo_stability_in_clip` |
| `multi_shot_spatial_continuity` | **refined** | `multi_shot_spatial_continuity` |
| `spoken_language_correctness` | **split** | `spoken_script_correctness`, `pronunciation_intelligibility` |
| `single_speaker_lip_sync` | **unchanged** | `single_speaker_lip_sync` |
| `two_speaker_turn_assignment_and_lip_sync` | **unchanged** | `two_speaker_turn_assignment_and_lip_sync` |
| `emotional_prosodic_fit` | **refined** | `emotional_prosodic_fit` |
| `audio_video_synchronisation` | **unchanged** | `audio_video_synchronisation` |
| `proposition_objective_fit` | **unchanged** | `proposition_objective_fit` |
| `hierarchy_product_as_hero` | **unchanged** | `hierarchy_product_as_hero` |
| `composition_brand_register` | **unchanged** | `composition_brand_register` |
| `hook_pacing_temporal_hierarchy` | **unchanged** | `hook_pacing_temporal_hierarchy` |
| `reliability_pass_at_k` | **unchanged** | `reliability_pass_at_k` |
| `cost_and_cpao` | **refined** | `cost_and_cpao` |
| `latency_errors_refusals` | **unchanged** | `latency_errors_refusals` |
| `reproducibility_repairability` | **split** | `reproducibility`, `repairability` |

**36 / 36 V1 ids mapped.** The build aborts if any lacks a disposition, so this is guaranteed by construction rather than by review.


---

## The changes that carry reasoning

### `spatial_relationship` → `spatial_relationship_2d`, `spatial_relationship_depth` *(split)*

T2I-CompBench evaluates 2D and 3D spatial relations SEPARATELY and with different judges. V1's own contract already stated depth ordering 'is NOT decidable from 2D boxes' - the split was documented and then not made. A 2D relation is deterministic given boxes; a depth relation is not. Different instrument, different qualification, different gate.

### `delivery_format_compliance` → `delivery_format_compliance` *(refined)*

Unchanged in meaning. Refined only to state its DUAL ROLE explicitly: the requested format is a CONDITION of every other measurement and simultaneously the subject of this capability.

### `typography_legibility` → `typography_legibility` *(refined)*

Controller-directed: legibility is now EXPLICITLY conditioned on delivery size. Previously the delivery size lived inside the prose definition, which made two legibility results silently incomparable. delivery_size becomes a REQUIRED condition.

### `packaging_brand_colour_fidelity` → `packaging_brand_colour_fidelity` *(refined)*

Controller-directed: brand-colour tolerance is a DECLARED measurement condition and threshold, not generic categorical-colour evidence. External colour benchmarks test 'is it red', which is a different and easier judgement than matching a declared brand value within tolerance.

### `person_identity` → `person_identity`, `wardrobe_invariant_fidelity` *(split)*

Controller-directed: declared wardrobe/clothing invariants must be VISIBLE rather than silently mixed with face identity. VBench-2.0 independently separates Human Identity from Human Clothes. The production consequence differs: a right face in wrong wardrobe is often repairable by re-prompting; a wrong face needs a different reference. One verdict cannot carry both.

### `reference_conditioning` → `reference_conditioning` *(refined)*

STYLE-REFERENCE BOUNDARY RESOLVED HERE. Style reference is NOT a new capability: it is this capability measured with reference_type=style. The failure - 'the supplied reference did not control the output' - is identical in kind; only the reference type differs, and a condition represents that cleanly. Adding a capability would duplicate the mechanism.

### `anatomy_hands` → `human_anatomy_integrity` *(renamed)*

Controller-directed rename/broaden. V1's own failure vocabulary already covered extra_limb, joint_inversion and facial_feature_misplaced - the NAME was narrower than the capability and invited under-testing of everything that is not a hand. Hand-specific diagnostics are PRESERVED as a required defect sub-vocabulary, not lost in the broadening.

### `motion_action_quality` → `motion_action_quality` *(refined)*

Refined to REQUIRE motion load as a recorded condition. VBench separates dynamic_degree from motion_smoothness because a near-static clip scores perfectly on smoothness - without motion load recorded, a model that produces almost no motion looks like one that produces excellent motion.

### `physics_material_appearance` → `physics_material_appearance` *(refined)*

Scope deliberately bounded DOWNWARD. VBench-2.0's physics group (mechanics, thermotics) is a research frontier; this product needs commercial plausibility for 6-20s media, not physical correctness. Multi-view consistency is extracted into sequence_state_continuity instead.

### `multi_shot_spatial_continuity` → `multi_shot_spatial_continuity` *(refined)*

Kept as SPATIAL continuity only, deliberately narrowed. Its V1 level-5 ladder example smuggled in product STATE continuity, which its name excludes. That case now belongs to the new sequence_state_continuity capability, so this id becomes honest rather than overloaded.

### `spoken_language_correctness` → `spoken_script_correctness`, `pronunciation_intelligibility` *(split)*

Controller-directed. This is the founding Devanagari trap in a different medium: a robust ASR NORMALISES a mispronunciation into the correct word, exactly as the vision checker silently corrected a misspelling. Word correctness is machine-comparable; pronunciation acceptability needs a first-language listener. One instrument cannot answer both, so one capability must not claim to.

### `emotional_prosodic_fit` → `emotional_prosodic_fit` *(refined)*

Refined toward DISCRIMINATION - can the requested register be told apart and correctly identified. TTSDS shows prosody has measurable correlates, so this need not stay purely preference-shaped.

### `cost_and_cpao` → `cost_and_cpao` *(refined)*

Refined to carry the Controller's TWO CpAO views: api_tool_cpao (diagnostic) and fully_loaded_cpao (primary business metric, including human review time in the operational path). V1 had a single cost view.

### `reproducibility_repairability` → `reproducibility`, `repairability` *(split)*

Controller-directed. Repeat agreement is measurable now from repeats we already budget. REPAIR requires a repair loop that DOES NOT EXIST, and repair attempts are additional generations. V1 flagged the split in an envelope note; v2 makes it structural. repairability is DORMANT.


---

## Added in V2

### `camera_framing_fidelity`

- **Family:** A_constraint_fidelity · **Unit:** `sequence` · **Routing:** `hard_constraint`
- **Why no existing capability + condition can represent it:** action_adherence asks whether the SUBJECT did what was asked. A camera instruction is about the OBSERVER, not the subject: a push-in can be absent while the subject action is perfect, and no existing capability's verdict changes. No condition can express it either, because a condition records circumstances, not whether an instruction was honoured.
- **External evidence:** VBench-2.0 names Camera Motion as its own controllable dimension; providers expose camera/motion controls as first-class API parameters.

### `sequence_state_continuity`

- **Family:** E_temporal_continuity · **Unit:** `shot_pair` · **Routing:** `hard_constraint`
- **Why no existing capability + condition can represent it:** multi_shot_spatial_continuity covers geometry and screen direction. State continuity is ORDERED and causal - the box is open in shot 2 BECAUSE it was opened in shot 1 - and a spatially perfect pair can be state-inconsistent. V1 already asked its spatial capability to carry a state example at level 5, which is the clearest possible evidence that one id was doing two jobs.
- **External evidence:** VBench-2.0 Motion Order Understanding and Multi-View Consistency.

### `technical_visual_integrity`

- **Family:** D_human_physical_realism · **Unit:** `sequence` · **Routing:** `hard_constraint`
- **Why no existing capability + condition can represent it:** Flicker, transient corruption, warping and sudden softness are not identity drift (the subject is still the same person), not motion quality (the motion may be smooth) and not anatomy (the body is correct). Every existing capability can pass on an asset a customer would reject on sight. Nothing in V1's 36 has a home for it.
- **External evidence:** VBench dedicates temporal_flickering, motion_smoothness and imaging_quality to this space - 3 of its 16 dimensions.

### `voice_identity_consistency`

- **Family:** F_speech_audio · **Unit:** `asset_set_over_time` · **Routing:** `hard_constraint`
- **Why no existing capability + condition can represent it:** The audio analogue of person_identity, and genuinely absent. spoken_script_correctness checks WHAT was said; pronunciation_intelligibility checks HOW clearly; emotional_prosodic_fit checks register. None asks whether it is the SAME VOICE across a campaign - a brand voice that changes between assets is a commercial failure every one of those three would pass.
- **External evidence:** TTS evaluation measures speaker similarity via automatic speaker verification (ASV) as an instrument distinct from intelligibility (ASR-WER).


---

## Rejected under the admission bar — deliberately NOT capabilities

**`style_reference_fidelity`**

RESOLVED INTO reference_conditioning with reference_type=style. The failure is identical in kind - the supplied reference did not control the output - and only the reference type differs. A condition represents that cleanly, so the admission bar is not met.

**`cross_asset_person_or_product_identity`**

RESOLVED BY OBSERVATION SCOPE. person_identity and product_identity already use asset_set_over_time. Cross-asset is a SCOPE of the same capability, not a different failure. Controller preferred extending existing identity capabilities and no distinct failure was found that scope cannot represent.

**`campaign_variant_set_consistency`**

DEFERRED AS AN OUTCOME-LEVEL CONCEPT, not a capability. It is a property of a DELIVERABLE SET against an acceptance basis, which lives at outcome acceptance rather than per-asset measurement. Controller directed that its instrument and final boundary be frozen WITH the request-coverage extension. Recorded here so it is not mistaken for solved or forgotten; reconciliation point is CANON-010.


---

## Backward compatibility

- **V1 remains authoritative until the Controller freezes v2.** This is a proposal.

- **No V1 artifact is modified.** `eval/v1/capability-contract.yaml` and the 100-item bank are byte-identical.

- **Historical Registry rows** (there are none) would remain readable: every V1 id resolves forward through this table, and split ids name their siblings so a historical result can be attributed to the correct successor or explicitly marked ambiguous.

- **A split is not a silent re-measure.** A V1 result under `spatial_relationship` cannot be presented as a `spatial_relationship_2d` result: the predicate changed. Such rows would be marked superseded, never migrated.

