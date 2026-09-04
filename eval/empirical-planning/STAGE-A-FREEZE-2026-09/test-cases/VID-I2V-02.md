# VID-I2V-02 — VID lane, hi (whatsapp)

## The request, as the customer sent it

**Channel:** whatsapp · **Language:** hi · **Attachments named:** phone_creative_final.png

> जो young professional वाली फोटो बनी थी (phone_creative_final.png), उसको 6 सेकंड का वीडियो बना दीजिए हमारे Hindi page के लिए। वो फ़ोन की तरफ़ देखे और हल्का सा मुस्कुराए, बस इतना ही — कैमरा एकदम स्थिर रहे। चेहरा वही रहे जो फोटो में है, बदले नहीं। कोई text नहीं, headline हम बाद में डालेंगे। आवाज़ की ज़रूरत नहीं।

**Source:** pool `rx`, id `RX-06`

**Adaptations:**

- subject_changed_to_the_accepted_IMG-CORE-02_still (source: a man with tea; here the customer's own accepted still — the plate rule)
- steam_motion_dropped (no tea in the plate; the micro-expression beat kept)
- text_requirement_dropped_customer_adds_in_post (source's "स्वाद चाय" removed)
- duration_set_to_6s (source 8 s)
- buyer_is_the_plate_owner (the fintech's Hindi page)

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | animate | customer_stated |
| modality | video | customer_stated |
| supplied_assets | [{applies_to: young_professional, asset_id: phone_creative_final, description: the Controller-accepted IMG-CORE-02 draw, media_type: image, role: subject_of_operation}] | customer_stated |
| mutation_intents | {intents: [{detail: 'customer named this: ''चेहरा वही रहे''', intent: preserve, target: facial identity}], preservation_default: implicit_everything_not_named} | customer_stated |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | [{entity_id: young_professional, entity_type: person, identity_invariants: [face as in the still], role: hero}] | customer_stated |
| relationships | — (absent) | absent |
| text_requirements | — (absent) | absent |
| brand_requirements | — (absent) | absent |
| language_topology | {on_screen_copy: none, spoken: none, subtitles: none, viewer_locale: hi-IN} | customer_stated |
| speaker_topology | {offscreen_voices: 0, script_exactness: free, turn_boundaries_required: false, visible_speakers: 0} | — |
| temporal_structure | {beats: [{beat: 1, content: 'glances at the phone, slight smile'}], continuity_requirements: [face identical throughout], duration_seconds: 6, shot_count: 1} | customer_stated |
| subject_motion | {description: looks toward the phone and smiles slightly, entity_ref: young_professional, motion_type: micro_expression} | customer_stated |
| camera_motion | {description: 'customer-stated: camera must not move', motion_type: static} | customer_stated |
| delivery | {aspect_ratios: ['4:5 (as the still)'], platform: instagram (Hindi page), resolution: 720p-class, safe_areas: []} | — |
| ambiguity_markers | — (absent) | absent |
| acceptance_intent | {free_choices: [timing of the smile], hard_constraints: [camera static, identity preserved, no text, no audio required], soft_preferences: [], stated_rejection_criteria: [camera movement, face changes, text], stated_success_criteria: [glance and slight smile, camera static, same face]} | customer_stated |

`product_or_packshot_present`: False · primary capability `person_stability_in_clip`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if the frame edges and background stay fixed for the whole clip (no pan, zoom or drift).
- ACCEPT only if the man's face is recognisably the same person in the first and last frame, with no change of hairline, jaw or eye spacing.
- ACCEPT only if he visibly glances toward the phone and his expression changes to a slight smile within the clip.
- REJECT if his hand, the phone or his features distort, or if any lettering appears.
- Deterministic pre-checks that count as rejects (E5): format probe (container/aspect/resolution/duration/audio-track); baked-text scan on no-text items; duration or aspect mismatch against `delivery`.

## Routes

Routes, arms, tranches and billing quantities are in `TEST-CASES.yaml` → this case's `routes[]` (route facts in `route_catalogue`): kling-v3-pro-i2v, minimax-h3-max-i2v, seedance-2.5-i2v, veo-3.1-fast-i2v, wan-3.0-prime-i2v.

**Blueprint:** `BLUEPRINTS/VID-I2V-02.blueprint.md` (sha256 `08fb8cbd2803a34b…`, author executor_agent)

## Why this shape is real demand

RX-06 is a Lucknow tea brand asking for a still to become a short clip with a static camera and a slight smile, written in Devanagari. Transposed to the fintech's Hindi page animating its own accepted still, it is the near-static talking-shot plate that every lip-sync job starts from.
