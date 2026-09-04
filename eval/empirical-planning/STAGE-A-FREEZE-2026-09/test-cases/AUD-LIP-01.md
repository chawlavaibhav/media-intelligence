# AUD-LIP-01 — AUD lane, hi (whatsapp)

## The request, as the customer sent it

**Channel:** whatsapp · **Language:** hi · **Attachments named:** model_clip.mp4, vo_line.wav

> हमारे model की एक clip है (model_clip.mp4, 6 सेकंड) और VO की audio है (vo_line.wav) — "एक धुलाई में दाग गायब"। इस आवाज़ को clip में lip-sync कर दीजिए, जो बोला जा रहा है वही होंठों से निकलता दिखे और सही समय पर। चेहरा, background, बाकी सब वैसा ही रहे, सिर्फ होंठ बदलें। जब line खत्म हो जाए तब होंठ बंद रहें।

**Source:** pool `fixture`, id `none`

**Adaptations:**

- fixture — no source pool holds a 'lip-sync this voice onto this clip' request; the shape is the Media Factory LatentSync route (freshness item 5) and TOPO-01 arm B; the drive is the AUD-TTS-01 output and the plate is the VID-I2V-02 accepted clip, so the case consumes two real-demand items

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | compose | customer_stated |
| modality | video | customer_stated |
| supplied_assets | [{applies_to: presenter, asset_id: model_clip, description: '6-s clip of one man, static camera (the VID-I2V-02 accepted clip)', media_type: video, role: subject_of_operation}, {applies_to: voice, asset_id: vo_line, description: 'the VO file: "एक धुलाई में दाग गायब"', media_type: audio, role: subject_of_operation}] | customer_stated |
| mutation_intents | {intents: [{detail: must match the supplied voice in time and shape, intent: change, target: mouth movement}, {detail: 'customer named this: face, background, rest of the clip unchanged', intent: preserve, target: everything else in the clip}, {detail: closed / at rest during silence — customer named this, intent: preserve, target: lips when no speech}], preservation_default: implicit_everything_not_named} | customer_stated |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | [{entity_id: presenter, entity_type: person, identity_invariants: [face as in the clip], role: hero}] | customer_stated |
| relationships | [{object: voice, relation: speaks, subject: presenter}] | customer_stated |
| text_requirements | — (absent) | absent |
| brand_requirements | — (absent) | absent |
| language_topology | {on_screen_copy: none, spoken: hi, subtitles: none, viewer_locale: IN} | customer_stated |
| speaker_topology | {offscreen_voices: 0, script: एक धुलाई में दाग गायब, script_exactness: exact, turn_boundaries_required: false, visible_speakers: 1} | customer_stated |
| temporal_structure | {beats: [{beat: 1, content: the line is spoken; silence after}], continuity_requirements: [identity unchanged], duration_seconds: 6, shot_count: 1} | customer_implied |
| subject_motion | {description: mouth moves with the voice, entity_ref: presenter, motion_type: gesture} | customer_stated |
| camera_motion | {description: as the supplied clip, motion_type: static} | customer_implied |
| delivery | {aspect_ratios: ['as the clip (4:5)'], platform: social, resolution: as the clip, safe_areas: []} | customer_implied |
| ambiguity_markers | — (absent) | absent |
| acceptance_intent | {free_choices: [], hard_constraints: [mouth matches the voice, face and background unchanged, lips at rest when no speech], soft_preferences: [], stated_rejection_criteria: [anything else changed], stated_success_criteria: [lips match the words and timing, lips closed in silence]} | customer_stated |

`product_or_packshot_present`: False · primary capability `single_speaker_lip_sync`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if the man's mouth opens and closes with the syllables of "एक धुलाई में दाग गायब" — a first-language Hindi judge sees the words being spoken; REJECT if the mouth moves out of time by a visible beat.
- ACCEPT only if his lips are closed or at rest during the silence after the line.
- REJECT if the face changes identity, the mouth region shows a visible patch, blur, colour seam or flicker, or the background changes.
- REJECT if the audio in the output is not the supplied voice (re-synthesised, clipped or shifted).
- Deterministic pre-checks that count as rejects (E5): format probe (container/aspect/resolution/duration/audio-track); baked-text scan on no-text items; duration or aspect mismatch against `delivery`.

## Routes

Routes, arms, tranches and billing quantities are in `TEST-CASES.yaml` → this case's `routes[]` (route facts in `route_catalogue`): kling-lipsync-a2v, sync-lipsync-v3.

**Blueprint:** `BLUEPRINTS/AUD-LIP-01.blueprint.md` (sha256 `0785cf24e2077768…`, author executor_agent)

## Why this shape is real demand

A labelled fixture consuming two real-demand items: the detergent brand (BR-F05-HI) supplies its VO and a 6-second clip of its presenter (the VID-I2V-02 accepted clip) and asks for the voice to be lip-synced — the Media Factory LatentSync route, which the prior calls the 'best ₹20 shot', and TOPO-01's arm B.
