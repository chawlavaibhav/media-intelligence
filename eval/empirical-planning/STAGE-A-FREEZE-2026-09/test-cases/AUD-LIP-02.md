# AUD-LIP-02 — AUD lane, hg (whatsapp)

## The request, as the customer sent it

**Channel:** whatsapp · **Language:** hg · **Attachments named:** instructor_clip.mp4, vo_kaushal.wav

> Ek clip hai instructor ki (instructor_clip.mp4, 6 sec) aur VO file (vo_kaushal.wav) — "Job chahiye? Toh skill upgrade karo. Aaj hi enroll करो — Kaushal Setu par." VO ko clip pe lip-sync kar do, lips exactly awaaz ke saath chalein, Hindi-English mix line hai toh mouth shapes sahi lagni chahiye. Baaki clip mein kuch change nahi, face same. Jab awaaz nahi hai tab lips band.

**Source:** pool `fixture`, id `none`

**Adaptations:**

- fixture — no source pool holds a 'lip-sync this voice onto this clip' request; the shape is the Media Factory LatentSync route (freshness item 5) and TOPO-01 arm B; the drive is the AUD-TTS-02 output and the plate is the VID-I2V-02 accepted clip, so the case consumes two real-demand items

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | compose | customer_stated |
| modality | video | customer_stated |
| supplied_assets | [{applies_to: presenter, asset_id: instructor_clip, description: '6-s clip of one man, static camera (the VID-I2V-02 accepted clip)', media_type: video, role: subject_of_operation}, {applies_to: voice, asset_id: vo_kaushal, description: 'the VO file: "Job chahiye? Toh skill upgrade karo. Aaj hi enroll करो — Kaushal Setu par."', media_type: audio, role: subject_of_operation}] | customer_stated |
| mutation_intents | {intents: [{detail: must match the supplied voice in time and shape, intent: change, target: mouth movement}, {detail: 'customer named this: face, background, rest of the clip unchanged', intent: preserve, target: everything else in the clip}, {detail: closed / at rest during silence — customer named this, intent: preserve, target: lips when no speech}], preservation_default: implicit_everything_not_named} | customer_stated |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | [{entity_id: presenter, entity_type: person, identity_invariants: [face as in the clip], role: hero}] | customer_stated |
| relationships | [{object: voice, relation: speaks, subject: presenter}] | customer_stated |
| text_requirements | — (absent) | absent |
| brand_requirements | — (absent) | absent |
| language_topology | {on_screen_copy: none, spoken: hi-en (Hinglish), subtitles: none, viewer_locale: IN} | customer_stated |
| speaker_topology | {offscreen_voices: 0, script: 'Job chahiye? Toh skill upgrade karo. Aaj hi enroll करो — Kaushal Setu par.', script_exactness: exact, turn_boundaries_required: false, visible_speakers: 1} | customer_stated |
| temporal_structure | {beats: [{beat: 1, content: the line is spoken; silence after}], continuity_requirements: [identity unchanged], duration_seconds: 6, shot_count: 1} | customer_implied |
| subject_motion | {description: mouth moves with the voice, entity_ref: presenter, motion_type: gesture} | customer_stated |
| camera_motion | {description: as the supplied clip, motion_type: static} | customer_implied |
| delivery | {aspect_ratios: ['as the clip (4:5)'], platform: social, resolution: as the clip, safe_areas: []} | customer_implied |
| ambiguity_markers | — (absent) | absent |
| acceptance_intent | {free_choices: [], hard_constraints: [mouth matches the voice, face and background unchanged, lips at rest when no speech], soft_preferences: [], stated_rejection_criteria: [anything else changed], stated_success_criteria: [lips match the words and timing, lips closed in silence]} | customer_stated |

`product_or_packshot_present`: False · primary capability `single_speaker_lip_sync`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if the mouth follows the whole line "Job chahiye? Toh skill upgrade karo. Aaj hi enroll करो — Kaushal Setu par." in time — including the English words — with no visible lag or lead.
- ACCEPT only if the lips rest closed during the pauses and after the line.
- REJECT if the face changes identity, or the mouth region shows a patch, blur, seam or flicker.
- REJECT if the output audio is not the supplied voice.
- Deterministic pre-checks that count as rejects (E5): format probe (container/aspect/resolution/duration/audio-track); baked-text scan on no-text items; duration or aspect mismatch against `delivery`.

## Routes

Routes, arms, tranches and billing quantities are in `TEST-CASES.yaml` → this case's `routes[]` (route facts in `route_catalogue`): kling-lipsync-a2v, sync-lipsync-v3.

**Blueprint:** `BLUEPRINTS/AUD-LIP-02.blueprint.md` (sha256 `faefd08ef8317562…`, author executor_agent)

## Why this shape is real demand

A labelled fixture: the Noida platform (BR-F07-HG) sends its instructor clip and Hinglish VO for lip-sync, asking that 'mouth shapes sahi lagni chahiye' on a code-mixed line — the request an edtech brand makes when it has a presenter clip but records the voice separately.
