# VID-REF-02 — VID lane, en (email)

## The request, as the customer sent it

**Channel:** email · **Language:** en · **Attachments named:** host_ref_1.jpg, host_ref_2.jpg, host_ref_3.jpg

> Following on from the host stills - we need a 6 second vertical clip with the same host (refs attached again: host_ref_1.jpg, host_ref_2.jpg, host_ref_3.jpg). She walks into frame in a cafe, sits down at a table and looks at the camera. Same face, same hair, that is the whole point, it has to be her. Camera is free, whatever looks natural. No dialogue needed, ambient sound is fine, no text. Thanks, Nikhil

**Source:** pool `marketplace`, id `MKT-009`

**Adaptations:**

- buyer_localised_to_India (same Bengaluru studio as IMG-REF-02)
- scene_stated_by_customer (walk in, sit, look — the bank's fixture element is the scene, labelled)
- duration_set_to_6s
- reference_count_set_to_3
- aspect_stated_9_16

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | generate | customer_stated |
| modality | video | customer_stated |
| supplied_assets | [{applies_to: host, asset_id: host_ref_1, description: reference photo 1, media_type: image, role: identity_reference}, {applies_to: host, asset_id: host_ref_2, description: reference photo 2, media_type: image, role: identity_reference}, {applies_to: host, asset_id: host_ref_3, description: reference photo 3, media_type: image, role: identity_reference}] | customer_stated |
| mutation_intents | — (absent) | absent |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | [{allowed_variation: {wardrobe: true}, entity_id: host, entity_type: person, identity_invariants: [face, hair], role: hero}] | customer_stated |
| relationships | — (absent) | absent |
| text_requirements | — (absent) | absent |
| brand_requirements | — (absent) | absent |
| language_topology | {on_screen_copy: none, spoken: none, subtitles: none, viewer_locale: en-IN} | customer_stated |
| speaker_topology | {offscreen_voices: 0, script_exactness: free, turn_boundaries_required: false, visible_speakers: 0} | — |
| temporal_structure | {beats: [{beat: 1, content: walks in}, {beat: 2, content: 'sits, looks at camera'}], continuity_requirements: [identity constant], duration_seconds: 6, shot_count: 1} | customer_stated |
| subject_motion | {description: walks into frame and sits, entity_ref: host, motion_type: locomotion} | customer_stated |
| camera_motion | {description: delegated ('camera is free'); blueprint chooses a still camera, motion_type: static} | system_derived — delegated; still camera (CA-D11) |
| delivery | {aspect_ratios: ['9:16'], platform: instagram reels, resolution: 720p, safe_areas: []} | — |
| ambiguity_markers | — (absent) | absent |
| acceptance_intent | {free_choices: [camera, wardrobe], hard_constraints: [identity from references, 'walk in, sit, look at camera', no text], soft_preferences: [ambient sound], stated_rejection_criteria: [text], stated_success_criteria: [it has to be her, natural]} | customer_stated |

`product_or_packshot_present`: False · primary capability `person_identity`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if, on a paused frame where she faces the camera, the judge picks the referenced person as the match against the two decoy sets.
- ACCEPT only if she enters the frame walking, sits at a table and looks at the camera before the clip ends.
- REJECT if her face or hair changes between the walking frames and the seated frames.
- REJECT if any lettering or speech is present.
- Deterministic pre-checks that count as rejects (E5): format probe (container/aspect/resolution/duration/audio-track); baked-text scan on no-text items; duration or aspect mismatch against `delivery`.

## Routes

Routes, arms, tranches and billing quantities are in `TEST-CASES.yaml` → this case's `routes[]` (route facts in `route_catalogue`): kling-v3-elements, seedance-2.5-ref2v, veo-3.1-fast-ref2v.

**Blueprint:** `BLUEPRINTS/VID-REF-02.blueprint.md` (sha256 `e860908af55a16c7…`, author executor_agent)

## Why this shape is real demand

MKT-009 again: the recurring host must be her in every video, 50+ proposals' worth of demand. The Bengaluru studio asks for its host walking into a cafe, camera free — identity from references without a starting frame, which is what distinguishes reference-to-video from i2v.
