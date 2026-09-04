# VID-MS-02 — VID lane, en (email)

## The request, as the customer sent it

**Channel:** email · **Language:** en · **Attachments named:** none

> Hi, 10 seconds, 3 shots. Shot 1: someone tossing and turning at night, cannot sleep, dark room. Shot 2: the mattress itself, clean, morning light. Shot 3: the same person sleeping peacefully, bright and calm. A dark to light progression across the three. Same person in shots 1 and 3, that matters. No VO, no text - we add "100 nights. Risk free." and the logo ourselves. 9:16. Thanks, Divya

**Source:** pool `brief_bank`, id `BR-F10-EN`

**Adaptations:**

- duration_set_to_10s (source 20 s)
- shot_count_set_to_3 (source 4–5; the logo shot is dropped with the end card)
- vo_and_end_card_dropped_customer_adds_in_post ("Some nights are long. They do not have to be." and "100 nights. Risk free.")
- register_kept_email

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | generate | customer_stated |
| modality | video | customer_stated |
| supplied_assets | — (absent) | absent |
| mutation_intents | — (absent) | absent |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | [{entity_id: sleeper, entity_type: person, identity_invariants: [same person in shots 1 and 3], role: hero}, {entity_id: mattress, entity_type: product, identity_invariants: ['a mattress, no readable label'], role: hero}] | customer_stated |
| relationships | [{object: mattress, relation: lies_on, subject: sleeper}] | customer_stated |
| text_requirements | — (absent) | absent |
| brand_requirements | — (absent) | absent |
| language_topology | {on_screen_copy: none, spoken: none, subtitles: none, viewer_locale: en-IN} | customer_stated |
| speaker_topology | {offscreen_voices: 0, script_exactness: free, turn_boundaries_required: false, visible_speakers: 0} | — |
| temporal_structure | {beats: [{beat: 1, content: 'restless at night, dark'}, {beat: 2, content: 'the mattress, morning'}, {beat: 3, content: 'sleeping peacefully, bright'}], continuity_requirements: [same person in shots 1 and 3, dark-to-light progression], duration_seconds: 10, shot_count: 3} | customer_stated |
| subject_motion | {description: tosses and turns; then lies still, entity_ref: sleeper, motion_type: gesture} | customer_stated |
| camera_motion | {description: delegated; stillness chosen, motion_type: static} | system_derived — delegated (CA-D11) |
| delivery | {aspect_ratios: ['9:16'], platform: instagram reels, resolution: 720p, safe_areas: []} | — |
| ambiguity_markers | — (absent) | absent |
| acceptance_intent | {free_choices: [room, person], hard_constraints: [10 s, 3 shots in the stated order, identity continuity, dark-to-light], soft_preferences: [calm], stated_rejection_criteria: [VO, text], stated_success_criteria: [three shots, dark to light, same person 1 and 3]} | customer_stated |

`product_or_packshot_present`: True · primary capability `multi_shot_spatial_continuity`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if there are exactly three shots in this order: a person restless in a dark bedroom; a bare mattress in morning light; the same person asleep in a bright room.
- ACCEPT only if the person in shot 3 is recognisably the person in shot 1.
- ACCEPT only if shot 1 is visibly darker than shot 2 and shot 3 is the brightest.
- REJECT if any lettering, voice or music is present, or if the clip runs under 9 s or over 11 s.
- Deterministic pre-checks that count as rejects (E5): format probe (container/aspect/resolution/duration/audio-track); baked-text scan on no-text items; duration or aspect mismatch against `delivery`.

## Routes

Routes, arms, tranches and billing quantities are in `TEST-CASES.yaml` → this case's `routes[]` (route facts in `route_catalogue`): gemini-omni-1.1-flash-10s, kling-v3-pro-10s.

**Blueprint:** `BLUEPRINTS/VID-MS-02.blueprint.md` (sha256 `50dac11feef4693d…`, author executor_agent)

## Why this shape is real demand

BR-F10-EN is a Bengaluru mattress brand's problem-then-relief sequence with a dark-to-light lighting arc and the same person in shots one and three. Cut to 10 seconds and three shots, it is the one-person multi-shot control that the 15-second item needs.
