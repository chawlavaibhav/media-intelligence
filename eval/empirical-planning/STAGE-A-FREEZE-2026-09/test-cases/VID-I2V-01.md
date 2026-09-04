# VID-I2V-01 — VID lane, en (whatsapp)

## The request, as the customer sent it

**Channel:** whatsapp · **Language:** en · **Attachments named:** juice_hero_final.png

> Take the bottle still you made (juice_hero_final.png) and give me a 6 second clip for the website hero. Camera moves slowly around the bottle, nothing else. The bottle shouldn't move or change - same bottle, same blank label, reflections behaving properly. No text, no music, no sound needed.

**Source:** pool `rx`, id `RX-05`

**Adaptations:**

- subject_changed_to_the_accepted_IMG-CORE-01_still (source: a brushed-steel bottle packshot; here the customer's own accepted glass-bottle still — the plate rule)
- attachment_named

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | animate | customer_stated |
| modality | video | customer_stated |
| supplied_assets | [{applies_to: juice_bottle, asset_id: juice_hero_final, description: the Controller-accepted IMG-CORE-01 draw, media_type: image, role: subject_of_operation}] | customer_stated |
| mutation_intents | {intents: [{detail: 'customer named this: ''shouldn''t move or change''', intent: preserve, target: bottle geometry and blank label}], preservation_default: implicit_everything_not_named} | customer_stated |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | [{entity_id: juice_bottle, entity_type: product, identity_invariants: [as in the still], role: hero}] | customer_stated |
| relationships | — (absent) | absent |
| text_requirements | — (absent) | absent |
| brand_requirements | — (absent) | absent |
| language_topology | {on_screen_copy: none, spoken: none, subtitles: none, viewer_locale: en-IN} | customer_stated |
| speaker_topology | {offscreen_voices: 0, script_exactness: free, turn_boundaries_required: false, visible_speakers: 0} | — |
| temporal_structure | {beats: [{beat: 1, content: slow orbit}], continuity_requirements: [bottle unchanged], duration_seconds: 6, shot_count: 1} | customer_stated |
| subject_motion | — (absent) | absent |
| camera_motion | {description: slow move around the object, motion_type: orbit} | customer_stated |
| delivery | {aspect_ratios: ['4:5 (as the still)'], platform: website hero, resolution: 720p-class, safe_areas: []} | — |
| ambiguity_markers | — (absent) | absent |
| acceptance_intent | {free_choices: [orbit speed and arc], hard_constraints: [bottle does not move or deform, label stays blank, 'no text, no audio'], soft_preferences: [reflections behave properly], stated_rejection_criteria: [bottle moves or changes, text, sound], stated_success_criteria: [camera orbits, bottle unchanged, reflections plausible]} | customer_stated |

`product_or_packshot_present`: True · primary capability `product_stability_in_clip`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if the viewpoint visibly travels around the bottle (a different side of the bottle is seen at the end than at the start).
- ACCEPT only if the bottle keeps the shape, size, cap and blank label of the first frame throughout; REJECT if it warps, drifts on the surface, or grows lettering.
- REJECT if the highlight on the glass flickers, or sits at the same spot on the bottle in the first and last frame while the viewpoint has changed.
- REJECT if speech or music is present, or any lettering.

### E5 pre-checks (code, not shown to the judge)

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- duration or aspect mismatch vs `delivery`
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

## Routes

See `TEST-CASES.yaml` → `routes[]`: kling-v3-pro-i2v, minimax-h3-max-i2v, veo-3.1-fast-i2v, wan-3.0-prime-i2v.

**Blueprint:** `BLUEPRINTS/VID-I2V-01.blueprint.md` (sha256 `0ab9692b55eb6c3c…`, author executor_agent)

## Why this shape is real demand

RX-05 is a premium bottle brand asking for a slow camera move around its packshot with the bottle itself untouched — the cleanest camera-versus-subject separation in the extension. Here it is the juice brand animating its own accepted still for the website hero, which is how the Media Factory plate topology was actually used.
