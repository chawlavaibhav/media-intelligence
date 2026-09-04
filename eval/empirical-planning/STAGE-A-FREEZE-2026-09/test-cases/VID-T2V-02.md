# VID-T2V-02 — VID lane, en (email)

## The request, as the customer sent it

**Channel:** email · **Language:** en · **Attachments named:** none

> Hi, need a 6 second vertical clip for Reels. One runner, a woman, early morning, empty city street in India. She sprints straight towards the camera and past it, shoes clearly visible as she goes by. Fast and real, not a fashion film. Natural street sound only, no dialogue, no music (we will add our track). No text on the video, the end card is ours to add. Same runner throughout, obviously. Thanks, Kabir

**Source:** pool `brief_bank`, id `BR-F06-EN`

**Adaptations:**

- duration_set_to_6s (source 15 s)
- single_shot_high_motion (the lacing-up beat dropped; the sprint kept as the one beat)
- text_requirement_dropped_customer_adds_in_post ("Made for the long road." removed)
- music_deferred_to_customer (source: music + ambient; here ambient only)
- aspect_stated_9_16
- register_rewritten_to_email

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | generate | customer_stated |
| modality | video | customer_stated |
| supplied_assets | — (absent) | absent |
| mutation_intents | — (absent) | absent |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | [{allowed_variation: {kit: true}, entity_id: runner, entity_type: person, identity_invariants: [one woman, same identity throughout], role: hero}, {allowed_variation: {colour: true}, entity_id: running_shoes, entity_type: product, identity_invariants: [clearly visible as she passes], role: supporting}] | customer_stated |
| relationships | [{object: running_shoes, relation: wears, subject: runner}] | customer_stated |
| text_requirements | — (absent) | absent |
| brand_requirements | — (absent) | absent |
| language_topology | {on_screen_copy: none, spoken: none, subtitles: none, viewer_locale: en-IN} | customer_stated |
| speaker_topology | {offscreen_voices: 0, script_exactness: free, turn_boundaries_required: false, visible_speakers: 0} | customer_stated |
| temporal_structure | {beats: [{beat: 1, content: she sprints toward and past the camera}], continuity_requirements: [same runner throughout], duration_seconds: 6, shot_count: 1} | customer_stated |
| subject_motion | {description: full sprint toward and past camera, entity_ref: runner, motion_type: locomotion} | customer_stated |
| camera_motion | {description: not stated; delegated — blueprint chooses a low static camera so the shoes pass close, motion_type: static} | system_derived — delegated; static low camera (CA-D11) |
| delivery | {aspect_ratios: ['9:16'], platform: instagram reels, resolution: 720p, safe_areas: []} | customer_stated (aspect, platform) |
| ambiguity_markers | — (absent) | absent |
| acceptance_intent | {free_choices: ['street, kit colours'], hard_constraints: [one woman, sprint toward and past camera, no dialogue/music/text], soft_preferences: ['early morning, empty street'], stated_rejection_criteria: [fashion-film look, dialogue, music, text], stated_success_criteria: ['fast, real', shoes clearly visible, same runner]} | customer_stated |

`product_or_packshot_present`: True · primary capability `motion_action_quality`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if one woman runs toward the camera and passes it within the clip, at a visible sprint (arms pumping, feet leaving the ground).
- ACCEPT only if her running shoes are clearly seen at least once as she passes.
- REJECT if her body, legs or feet visibly warp, multiply, slide without steps, or change identity between the first and last second.
- REJECT if any speech, music or lettering is present.
- REJECT if she never reaches or passes the camera (a jog in place or a distant figure does not satisfy the request).
- Deterministic pre-checks that count as rejects (E5): format probe (container/aspect/resolution/duration/audio-track); baked-text scan on no-text items; duration or aspect mismatch against `delivery`.

## Routes

Routes, arms, tranches and billing quantities are in `TEST-CASES.yaml` → this case's `routes[]` (route facts in `route_catalogue`): gemini-omni-1.1-flash, kling-v3-pro-audio, minimax-h3-max, seedance-2.5, sora-2, veo-3.1-fast, wan-3.0-prime.

**Blueprint:** `BLUEPRINTS/VID-T2V-02.blueprint.md` (sha256 `8b56537372dc0880…`, author executor_agent)

## Why this shape is real demand

BR-F06-EN is a Delhi running-shoe brand wanting a real, non-glossy runner with the shoes visible and no dialogue. Compressed to the single sprint beat, it is the high-motion clip every sportswear D2C brand asks for, with the end card and music added by their own editor.
