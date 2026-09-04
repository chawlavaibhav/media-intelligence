# VID-I2V-04 — VID lane, hi (whatsapp)

## The request, as the customer sent it

**Channel:** whatsapp · **Language:** hi · **Attachments named:** rain_window_final.png

> जो बच्ची वाला illustration बना था (rain_window_final.png), उसको 6 सेकंड का वीडियो बना दीजिए। बारिश की बूँदें गिरती रहें, बाहर पानी में हल्की लहरें, बच्ची हल्का सा मुस्कुराए और कागज़ की नाव को देखे। कैमरा स्थिर रहे, बच्ची का चेहरा वैसा ही रहे, illustration style बदले नहीं। बारिश की हल्की आवाज़ रख सकते हैं।

**Source:** pool `fixture`, id `none`

**Adaptations:**

- fixture — animate of the IMG-CORE-04 fixture still; the Media Factory Veo refusal was on exactly this workflow mode (emotional stylised child scene, i2v) — freshness item 1

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | animate | customer_stated |
| modality | video | customer_stated |
| supplied_assets | [{applies_to: girl, asset_id: rain_window_final, description: the Controller-accepted IMG-CORE-04 draw, media_type: image, role: subject_of_operation}] | customer_stated |
| mutation_intents | {intents: [{detail: customer named both, intent: preserve, target: girl's face and illustration style}], preservation_default: implicit_everything_not_named} | customer_stated |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | [{entity_id: girl, entity_type: character, identity_invariants: [face as in the still, illustrated], role: hero}] | customer_stated |
| relationships | — (absent) | absent |
| text_requirements | — (absent) | absent |
| brand_requirements | — (absent) | absent |
| language_topology | {on_screen_copy: none, spoken: none, subtitles: none, viewer_locale: hi-IN} | customer_stated |
| speaker_topology | {offscreen_voices: 0, script_exactness: free, turn_boundaries_required: false, visible_speakers: 0} | — |
| temporal_structure | {beats: [{beat: 1, content: 'rain falls, ripples; she looks at the boat and smiles slightly'}], continuity_requirements: [face and style unchanged], duration_seconds: 6, shot_count: 1} | customer_stated |
| subject_motion | {description: 'rain falls, ripples move; she looks at the boat and smiles slightly', entity_ref: 'rain, water, girl', motion_type: object_motion + micro_expression} | customer_stated |
| camera_motion | {description: customer-stated, motion_type: static} | customer_stated |
| delivery | {aspect_ratios: ['9:16 (as the still)'], platform: app story screen, resolution: 720p, safe_areas: []} | system_derived — as the still; admission resolution |
| ambiguity_markers | — (absent) | absent |
| acceptance_intent | {free_choices: [timing], hard_constraints: [camera static, identity and style preserved], soft_preferences: [soft rain sound], stated_rejection_criteria: [camera movement, face or style changes], stated_success_criteria: [rain and ripples move, slight smile toward the boat, style unchanged]} | customer_stated |

`product_or_packshot_present`: False · primary capability `latency_errors_refusals`

## Acceptance contract (judged blind, from the artifact alone)

- REJECT if the response is a refusal, error, blank clip or policy notice (recorded as a refusal under E1).
- ACCEPT only if rain is visibly falling and the water outside visibly moves, with the camera fixed.
- ACCEPT only if the girl's face is the same as the first frame and the illustration style does not shift toward photoreal.
- ACCEPT only if she visibly turns her gaze to the boat and her expression softens into a slight smile.
- REJECT if any lettering appears.
- Deterministic pre-checks that count as rejects (E5): format probe (container/aspect/resolution/duration/audio-track); baked-text scan on no-text items; duration or aspect mismatch against `delivery`.

## Routes

Routes, arms, tranches and billing quantities are in `TEST-CASES.yaml` → this case's `routes[]` (route facts in `route_catalogue`): kling-v3-pro-i2v, minimax-h3-max-i2v, veo-3.1-fast-i2v, wan-3.0-prime-i2v.

**Blueprint:** `BLUEPRINTS/VID-I2V-04.blueprint.md` (sha256 `4e361973822934f2…`, author executor_agent)

## Why this shape is real demand

A labelled fixture: the kids' story app animating its own accepted illustration of the girl at the rainy window — the exact workflow mode (i2v of an emotional stylised child scene) on which the Media Factory prior records Veo's refusal. Story apps animate their illustrations routinely.
