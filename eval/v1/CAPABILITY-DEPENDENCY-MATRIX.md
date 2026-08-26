# Eval V1 — Capability Dependency Matrix

> **GENERATED FILE — do not hand-edit.** Source: `capability-contract.yaml`.

This is the answer to one question: **what has to exist before each capability can actually be measured?** It is the shopping list behind the whole programme.


## Full matrix

| Capability | Unit | Instrument family | Instrument readiness | Benchmark material | Routing |
|---|---|---|---|---|---|
| `object_count` | `frame` | deterministic CV/geometry | `blocked_pending_qualification` | `constructed_by_eval` | `hard_constraint` |
| `attribute_binding` | `frame` | structured visual VLM | `blocked_pending_qualification` | `constructed_by_eval` | `hard_constraint` |
| `spatial_relationship` | `frame` | deterministic CV/geometry | `blocked_pending_qualification` | `constructed_by_eval` | `hard_constraint` |
| `action_adherence` | `sequence` | temporal/video | `blocked_pending_qualification` | `constructed_by_eval` | `hard_constraint` |
| `delivery_format_compliance` | `whole_asset` | deterministic CV/geometry | `deterministic_ready` | `no_external_stimulus_required` | `hard_constraint` |
| `exact_text_latin` | `frame` | text/OCR | `blocked_pending_qualification` | `constructed_by_eval` | `hard_constraint` |
| `exact_text_devanagari` | `frame` | text/OCR | `blocked_pending_qualification` | `available` | `hard_constraint` |
| `typography_legibility` | `frame` | structured visual VLM | `blocked_pending_qualification` | `constructed_by_eval` | `descriptive_only` |
| `logo_wordmark_fidelity` | `frame` | structured visual VLM | `blocked_pending_qualification` | `partial` | `hard_constraint` |
| `packaging_brand_colour_fidelity` | `frame` | deterministic CV/geometry | `blocked_pending_qualification` | `missing` | `hard_constraint` |
| `person_identity` | `asset_set_over_time` | structured visual VLM | `blocked_pending_qualification` | `missing` | `hard_constraint` |
| `product_identity` | `asset_set_over_time` | structured visual VLM | `blocked_pending_qualification` | `missing` | `hard_constraint` |
| `reference_conditioning` | `asset_set_over_time` | structured visual VLM | `blocked_pending_qualification` | `missing` | `hard_constraint` |
| `edit_preservation` | `frame` | deterministic CV/geometry | `deterministic_ready` | `missing` | `hard_constraint` |
| `anatomy_hands` | `frame` | structured visual VLM | `blocked_pending_qualification` | `constructed_by_eval` | `hard_constraint` |
| `human_object_contact` | `frame` | structured visual VLM | `blocked_pending_qualification` | `constructed_by_eval` | `hard_constraint` |
| `human_human_interaction` | `frame` | structured visual VLM | `blocked_pending_qualification` | `constructed_by_eval` | `hard_constraint` |
| `motion_action_quality` | `sequence` | temporal/video | `blocked_pending_qualification` | `partial` | `descriptive_only` |
| `physics_material_appearance` | `frame` | structured visual VLM | `blocked_pending_qualification` | `constructed_by_eval` | `descriptive_only` |
| `person_stability_in_clip` | `sequence` | temporal/video | `blocked_pending_qualification` | `missing` | `hard_constraint` |
| `product_stability_in_clip` | `sequence` | temporal/video | `blocked_pending_qualification` | `missing` | `hard_constraint` |
| `text_logo_stability_in_clip` | `sequence` | temporal/video | `blocked_pending_qualification` | `missing` | `hard_constraint` |
| `multi_shot_spatial_continuity` | `shot_pair` | temporal/video | `blocked_pending_qualification` | `partial` | `hard_constraint` |
| `spoken_language_correctness` | `whole_asset` | speech/audio/AV | `blocked_pending_qualification` | `missing` | `hard_constraint` |
| `single_speaker_lip_sync` | `sequence` | speech/audio/AV | `blocked_pending_qualification` | `missing` | `hard_constraint` |
| `two_speaker_turn_assignment_and_lip_sync` | `sequence` | speech/audio/AV | `blocked_pending_qualification` | `missing` | `hard_constraint` |
| `emotional_prosodic_fit` | `whole_asset` | speech/audio/AV | `blocked_pending_qualification` | `missing` | `descriptive_only` |
| `audio_video_synchronisation` | `whole_asset` | speech/audio/AV | `blocked_pending_qualification` | `missing` | `hard_constraint` |
| `proposition_objective_fit` | `whole_asset` | creative/commercial | `blocked_pending_qualification` | `missing` | `descriptive_only` |
| `hierarchy_product_as_hero` | `whole_asset` | creative/commercial | `blocked_pending_qualification` | `missing` | `descriptive_only` |
| `composition_brand_register` | `whole_asset` | creative/commercial | `blocked_pending_qualification` | `missing` | `descriptive_only` |
| `hook_pacing_temporal_hierarchy` | `sequence` | creative/commercial | `blocked_pending_qualification` | `missing` | `descriptive_only` |
| `reliability_pass_at_k` | `asset_set_over_time` | operational logging (no instrument) | `deterministic_ready` | `no_external_stimulus_required` | `hard_constraint` |
| `cost_and_cpao` | `asset_set_over_time` | operational logging (no instrument) | `deterministic_ready` | `no_external_stimulus_required` | `hard_constraint` |
| `latency_errors_refusals` | `asset_set_over_time` | operational logging (no instrument) | `deterministic_ready` | `no_external_stimulus_required` | `hard_constraint` |
| `reproducibility_repairability` | `asset_set_over_time` | operational logging (no instrument) | `deterministic_ready` | `no_external_stimulus_required` | `descriptive_only` |

## Blockers, grouped by what would unblock them

### Waiting on an instrument nobody has qualified yet

| Instrument family | Capabilities it unblocks | Count |
|---|---|---:|
| structured visual VLM | `attribute_binding`, `typography_legibility`, `logo_wordmark_fidelity`, `person_identity`, `product_identity`, `reference_conditioning`, `anatomy_hands`, `human_object_contact`, `human_human_interaction`, `physics_material_appearance` | 10 |
| temporal/video | `action_adherence`, `motion_action_quality`, `person_stability_in_clip`, `product_stability_in_clip`, `text_logo_stability_in_clip`, `multi_shot_spatial_continuity` | 6 |
| speech/audio/AV | `spoken_language_correctness`, `single_speaker_lip_sync`, `two_speaker_turn_assignment_and_lip_sync`, `emotional_prosodic_fit`, `audio_video_synchronisation` | 5 |
| creative/commercial | `proposition_objective_fit`, `hierarchy_product_as_hero`, `composition_brand_register`, `hook_pacing_temporal_hierarchy` | 4 |
| deterministic CV/geometry | `object_count`, `spatial_relationship`, `packaging_brand_colour_fidelity` | 3 |
| text/OCR | `exact_text_latin`, `exact_text_devanagari` | 2 |

**Why this table is the priority list:** qualifying one instrument family unblocks every capability in its row at once. That is the cheapest possible ordering of the work.

### Waiting on test material we do not hold

20 capabilities have `missing` or `partial` material: `logo_wordmark_fidelity`, `packaging_brand_colour_fidelity`, `person_identity`, `product_identity`, `reference_conditioning`, `edit_preservation`, `motion_action_quality`, `person_stability_in_clip`, `product_stability_in_clip`, `text_logo_stability_in_clip`, `multi_shot_spatial_continuity`, `spoken_language_correctness`, `single_speaker_lip_sync`, `two_speaker_turn_assignment_and_lip_sync`, `emotional_prosodic_fit`, `audio_video_synchronisation`, `proposition_objective_fit`, `hierarchy_product_as_hero`, `composition_brand_register`, `hook_pacing_temporal_hierarchy`

**These two lists overlap, and that is the point.** A capability can appear in both, in one, or in neither. Fixing an instrument does not deliver material, and buying material does not qualify an instrument.

### Mechanism ready, material absent

The state the single scalar could not express: `edit_preservation`. Qualification effort here buys nothing until material exists.


## Free riders — measurable on assets other dimensions already generate

These cost **no additional generation at all**. They should be attached to every eligible asset by default; not doing so is wasted money.

- `cost_and_cpao`
- `delivery_format_compliance`
- `latency_errors_refusals`
- `reliability_pass_at_k`
- `reproducibility_repairability`

## Unit distribution

| Observation unit | Capabilities |
|---|---:|
| `frame` | 13 |
| `sequence` | 8 |
| `whole_asset` | 7 |
| `asset_set_over_time` | 7 |
| `shot_pair` | 1 |

A capability measured at `sequence`, `shot_pair` or `asset_set_over_time` **cannot** be scored from a single still image. Any item claiming to do so is a design defect, not a cheaper test.

