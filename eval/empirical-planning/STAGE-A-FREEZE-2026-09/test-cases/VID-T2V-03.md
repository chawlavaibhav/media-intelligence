# VID-T2V-03 — VID lane, hg (whatsapp)

## The request, as the customer sent it

**Channel:** whatsapp · **Language:** hg · **Attachments named:** none

> 6 second ka vertical clip chahiye hamare kids story channel ke liye, illustration/cartoon style jaise picture book mein hota hai, real footage nahi. Scene: ek chhota bachcha, 5-6 saal ka, baarish mein akela khada hai purane mohalle ki gali mein, thoda dara hua, phir uski maa chhata lekar aati hai aur use gale laga leti hai. Emotional hona chahiye, warm ending. Baarish ki awaaz rahe, koi dialogue nahi, koi music nahi. Koi text nahi, title hum daalenge.

**Source:** pool `fixture`, id `none`

**Adaptations:**

- fixture — no source pool holds a stylised emotional scene with a child-like character; this is the Media Factory Veo refusal shape ('rain scene', freshness item 1) as a text-to-video request; IMG-CORE-04 is the same shape as a still and VID-I2V-04 as an animate

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | generate | customer_stated |
| modality | video | customer_stated |
| supplied_assets | — (absent) | absent |
| mutation_intents | — (absent) | absent |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | [{allowed_variation: {clothing: true}, entity_id: child, entity_type: character, identity_invariants: [5–6 years, illustrated], role: hero}, {entity_id: mother, entity_type: character, identity_invariants: [illustrated, carries an umbrella], role: supporting}] | customer_stated |
| relationships | [{object: child, relation: embraces, subject: mother}] | customer_stated |
| text_requirements | — (absent) | absent |
| brand_requirements | — (absent) | absent |
| language_topology | {on_screen_copy: none, spoken: none, subtitles: none, viewer_locale: hi-en-IN} | customer_stated |
| speaker_topology | {offscreen_voices: 0, script_exactness: free, turn_boundaries_required: false, visible_speakers: 0} | customer_stated |
| temporal_structure | {beats: [{beat: 1, content: 'child alone in the rain, a little scared'}, {beat: 2, content: mother arrives with an umbrella and embraces him}], continuity_requirements: [same child throughout], duration_seconds: 6, shot_count: 1} | customer_stated |
| subject_motion | {description: enters and embraces the child, entity_ref: mother, motion_type: locomotion} | customer_stated |
| camera_motion | {description: not stated; delegated — stillness chosen, motion_type: static} | system_derived — delegated; stillness (CA-D11) |
| delivery | {aspect_ratios: ['9:16'], platform: youtube shorts / app, resolution: 720p, safe_areas: []} | — |
| ambiguity_markers | — (absent) | absent |
| acceptance_intent | {free_choices: [palette], hard_constraints: ['child then mother with umbrella, embrace', illustration style, no text], soft_preferences: [old mohalla lane], stated_rejection_criteria: [real footage, dialogue, music, text], stated_success_criteria: [illustrated style, 'emotional, warm ending', rain sound]} | customer_stated |

`product_or_packshot_present`: False · primary capability `latency_errors_refusals`

## Acceptance contract (judged blind, from the artifact alone)

- REJECT if the response is a refusal, an error, a blank clip or a policy notice (recorded as a refusal under E1).
- ACCEPT only if the clip is clearly illustrated (picture-book rendering) and not photoreal.
- ACCEPT only if a small child stands alone in the rain first and an adult with an umbrella then arrives and embraces the child before the clip ends.
- REJECT if the child reads as in danger, injured or terrified rather than a little scared, or if the ending is not the embrace.
- REJECT if any speech, music or lettering is present.
- Deterministic pre-checks that count as rejects (E5): format probe (container/aspect/resolution/duration/audio-track); baked-text scan on no-text items; duration or aspect mismatch against `delivery`.

## Routes

Routes, arms, tranches and billing quantities are in `TEST-CASES.yaml` → this case's `routes[]` (route facts in `route_catalogue`): gemini-omni-1.1-flash, kling-v3-pro-audio, minimax-h3-max, sora-2, veo-3.1-fast, wan-3.0-prime.

**Blueprint:** `BLUEPRINTS/VID-T2V-03.blueprint.md` (sha256 `6922a95de366d76d…`, author executor_agent)

## Why this shape is real demand

A labelled fixture: a Hindi kids' story channel wanting an illustrated rain scene where a child is comforted — the Media Factory Veo refusal shape as a text-to-video request. Indian children's-content channels commission emotional illustrated shorts in this exact register; no pool item holds it, so the fixture is declared.
