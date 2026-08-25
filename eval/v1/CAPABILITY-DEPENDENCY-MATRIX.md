# Eval V1 — Capability Dependency Matrix

> **GENERATED FILE — do not hand-edit.** Source: `capability-contract.yaml`.

This is the answer to one question: **what has to exist before each capability can actually be measured?** It is the shopping list behind the whole programme.


## Full matrix

| Capability | Unit | Instrument | Resource | Routing | Status |
|---|---|---|---|---|---|
| `object_count` | `frame` | deterministic CV/geometry | `constructed_by_eval` | `hard_constraint` | blocked — no qualified instrument |
| `attribute_binding` | `frame` | structured visual VLM | `constructed_by_eval` | `hard_constraint` | blocked — no qualified instrument |
| `spatial_relationship` | `frame` | deterministic CV/geometry | `constructed_by_eval` | `hard_constraint` | blocked — no qualified instrument |
| `action_adherence` | `sequence` | temporal/video | `constructed_by_eval` | `hard_constraint` | blocked — no qualified instrument |
| `delivery_format_compliance` | `whole_asset` | deterministic CV/geometry | `no_external_resource` | `hard_constraint` | measurable now |
| `exact_text_latin` | `frame` | text/OCR | `constructed_by_eval` | `hard_constraint` | blocked — no qualified instrument |
| `exact_text_devanagari` | `frame` | text/OCR | `required` | `hard_constraint` | blocked — no qualified instrument |
| `typography_legibility` | `frame` | structured visual VLM | `constructed_by_eval` | `descriptive_only` | blocked — no qualified instrument |
| `logo_wordmark_fidelity` | `frame` | structured visual VLM | `required` | `hard_constraint` | blocked — no qualified instrument |
| `packaging_brand_colour_fidelity` | `frame` | deterministic CV/geometry | `required` | `hard_constraint` | blocked — resource missing |
| `person_identity` | `asset_set_over_time` | structured visual VLM | `required` | `hard_constraint` | blocked — resource missing |
| `product_identity` | `asset_set_over_time` | structured visual VLM | `required` | `hard_constraint` | blocked — resource missing |
| `reference_conditioning` | `asset_set_over_time` | structured visual VLM | `required` | `hard_constraint` | blocked — resource missing |
| `edit_preservation` | `frame` | deterministic CV/geometry | `constructed_by_eval` | `hard_constraint` | measurable now |
| `anatomy_hands` | `frame` | structured visual VLM | `constructed_by_eval` | `hard_constraint` | blocked — no qualified instrument |
| `human_object_contact` | `frame` | structured visual VLM | `constructed_by_eval` | `hard_constraint` | blocked — no qualified instrument |
| `human_human_interaction` | `frame` | structured visual VLM | `constructed_by_eval` | `hard_constraint` | blocked — no qualified instrument |
| `motion_action_quality` | `sequence` | temporal/video | `constructed_by_eval` | `descriptive_only` | blocked — no qualified instrument |
| `physics_material_appearance` | `frame` | structured visual VLM | `constructed_by_eval` | `descriptive_only` | blocked — no qualified instrument |
| `person_stability_in_clip` | `sequence` | temporal/video | `constructed_by_eval` | `hard_constraint` | blocked — no qualified instrument |
| `product_stability_in_clip` | `sequence` | temporal/video | `constructed_by_eval` | `hard_constraint` | blocked — no qualified instrument |
| `text_logo_stability_in_clip` | `sequence` | temporal/video | `constructed_by_eval` | `hard_constraint` | blocked — no qualified instrument |
| `multi_shot_spatial_continuity` | `shot_pair` | temporal/video | `constructed_by_eval` | `hard_constraint` | blocked — no qualified instrument |
| `spoken_language_correctness` | `whole_asset` | speech/audio/AV | `required` | `hard_constraint` | blocked — no qualified instrument |
| `single_speaker_lip_sync` | `sequence` | speech/audio/AV | `required` | `hard_constraint` | blocked — resource missing |
| `two_speaker_turn_assignment_and_lip_sync` | `sequence` | speech/audio/AV | `required` | `hard_constraint` | blocked — resource missing |
| `emotional_prosodic_fit` | `whole_asset` | speech/audio/AV | `required` | `descriptive_only` | blocked — no qualified instrument |
| `audio_video_synchronisation` | `whole_asset` | speech/audio/AV | `constructed_by_eval` | `hard_constraint` | measurable now |
| `proposition_objective_fit` | `whole_asset` | creative/commercial | `required` | `descriptive_only` | blocked — resource missing |
| `hierarchy_product_as_hero` | `whole_asset` | creative/commercial | `required` | `descriptive_only` | blocked — resource missing |
| `composition_brand_register` | `whole_asset` | creative/commercial | `required` | `descriptive_only` | blocked — resource missing |
| `hook_pacing_temporal_hierarchy` | `sequence` | creative/commercial | `required` | `descriptive_only` | blocked — resource missing |
| `reliability_pass_at_k` | `asset_set_over_time` | operational logging (no instrument) | `no_external_resource` | `hard_constraint` | measurable now |
| `cost_and_cpao` | `asset_set_over_time` | operational logging (no instrument) | `no_external_resource` | `hard_constraint` | measurable now |
| `latency_errors_refusals` | `asset_set_over_time` | operational logging (no instrument) | `no_external_resource` | `hard_constraint` | measurable now |
| `reproducibility_repairability` | `asset_set_over_time` | operational logging (no instrument) | `no_external_resource` | `descriptive_only` | blocked — no qualified instrument |

## Blockers, grouped by what would unblock them

### Waiting on an instrument nobody has qualified yet

| Instrument family | Capabilities it unblocks | Count |
|---|---|---:|
| structured visual VLM | `attribute_binding`, `typography_legibility`, `logo_wordmark_fidelity`, `anatomy_hands`, `human_object_contact`, `human_human_interaction`, `physics_material_appearance` | 7 |
| temporal/video | `action_adherence`, `motion_action_quality`, `person_stability_in_clip`, `product_stability_in_clip`, `text_logo_stability_in_clip`, `multi_shot_spatial_continuity` | 6 |
| deterministic CV/geometry | `object_count`, `spatial_relationship` | 2 |
| text/OCR | `exact_text_latin`, `exact_text_devanagari` | 2 |
| speech/audio/AV | `spoken_language_correctness`, `emotional_prosodic_fit` | 2 |
| operational logging (no instrument) | `reproducibility_repairability` | 1 |

**Why this table is the priority list:** qualifying one instrument family unblocks every capability in its row at once. That is the cheapest possible ordering of the work.

### Waiting on test material we do not hold

10 capabilities: `packaging_brand_colour_fidelity`, `person_identity`, `product_identity`, `reference_conditioning`, `single_speaker_lip_sync`, `two_speaker_turn_assignment_and_lip_sync`, `proposition_objective_fit`, `hierarchy_product_as_hero`, `composition_brand_register`, `hook_pacing_temporal_hierarchy`


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

