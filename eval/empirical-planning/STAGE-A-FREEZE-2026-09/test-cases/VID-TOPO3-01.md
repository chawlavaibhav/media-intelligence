# VID-TOPO3-01 — VID lane, hi (whatsapp)

## The request, as the customer sent it

**Channel:** whatsapp · **Language:** hi · **Attachments named:** none

> जो दीपावली वाला poster बन रहा है, उसी का एक 6 सेकंड का vertical video भी चाहिए WhatsApp status के लिए। वही तीनों लाइनें — "दीपावली की शुभकामनाएं", "सभी मिठाइयों पर 20% छूट", और "श्री गणेश मिष्ठान भंडार" सबसे बड़ा — पूरे वीडियो में साफ़ पढ़ने लायक रहें, हिलें-डुलें नहीं, एक भी अक्षर बदले नहीं। पीछे दीये जलते हुए, हल्की सी movement, मिठाई का डिब्बा वहीं रहे। कोई आवाज़ ज़रूरी नहीं।

**Source:** pool `brief_bank`, id `BR-F01-HI`

**Adaptations:**

- converted_to_video_6s (same brief as IMG-TEXT-01, asked as a moving status)
- aspect_set_to_9_16 (WhatsApp status)
- text_stability_stated ('हिलें-डुलें नहीं') — the customer's own words for text stability under motion
- audio_not_required (customer states)

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | generate | customer_stated |
| modality | video | customer_stated |
| supplied_assets | — (absent) | absent |
| mutation_intents | — (absent) | absent |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | [{entity_id: sweet_box_and_diyas, entity_type: product, identity_invariants: [sweet box, lit diyas], role: supporting}, {entity_id: t1, entity_type: text_element, role: hero}, {entity_id: t2, entity_type: text_element, role: hero}, {entity_id: t3, entity_type: text_element, role: hero}] | customer_stated |
| relationships | [{object: 't1,t2', relation: largest_lettering_of, subject: t3}] | customer_stated |
| text_requirements | [{content: दीपावली की शुभकामनाएं, exactness: exact, role: headline, script: devanagari, stability: stable and legible in every frame, text_id: t1}, {content: सभी मिठाइयों पर 20% छूट, exactness: exact, role: body, script: devanagari, stability: stable and legible in every frame, text_id: t2}, {content: श्री गणेश मिष्ठान भंडार, exactness: exact, role: brand_name, script: devanagari, stability: stable and legible in every frame, text_id: t3}] | customer_stated |
| brand_requirements | — (absent) | absent |
| language_topology | {on_screen_copy: hi (Devanagari), spoken: none, subtitles: none, viewer_locale: hi-IN} | customer_stated |
| speaker_topology | {offscreen_voices: 0, script_exactness: free, turn_boundaries_required: false, visible_speakers: 0} | customer_stated (none) |
| temporal_structure | {beats: [{beat: 1, content: 'diyas flicker, gentle movement; text static'}], continuity_requirements: [text identical in every frame], duration_seconds: 6, shot_count: 1} | customer_stated |
| subject_motion | {description: flames flicker; light movement, entity_ref: diyas, motion_type: object_motion} | customer_stated |
| camera_motion | {description: customer-implied by 'हिलें-डुलें नहीं', motion_type: static} | customer_implied |
| delivery | {aspect_ratios: ['9:16'], platform: whatsapp status, resolution: 720p, safe_areas: []} | customer_stated |
| ambiguity_markers | [{affected_fields: [R07, R18], detail: 'as IMG-TEXT-01: offer most important vs name largest — same resolution (dominance by contrast, size by request)', marker_type: contradiction}] | — |
| acceptance_intent | {free_choices: [palette, audio (none required)], hard_constraints: ['three exact Devanagari strings, stable', name largest, '9:16'], soft_preferences: ['diyas, sweet box'], stated_rejection_criteria: [any character changing, text moving], stated_success_criteria: [three strings legible and unchanged in every frame, name largest, gentle diya movement]} | customer_stated |

`product_or_packshot_present`: True · primary capability `text_logo_stability_in_clip`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if, in the first, middle and last frame, the lettering reads exactly "दीपावली की शुभकामनाएं", "सभी मिठाइयों पर 20% छूट" and "श्री गणेश मिष्ठान भंडार"; REJECT if any character differs between frames or from the strings.
- REJECT if any string drifts, wobbles, smears or flickers across the clip.
- ACCEPT only if "श्री गणेश मिष्ठान भंडार" is the largest lettering in every frame.
- ACCEPT only if some movement is visible (diya flames or light) — a still image held for 6 s is a reject.
- REJECT if any other lettering or pseudo-lettering appears in any frame.
- Deterministic pre-checks that count as rejects (E5): format probe (container/aspect/resolution/duration/audio-track); baked-text scan on no-text items; duration or aspect mismatch against `delivery`.

## Routes

Routes, arms, tranches and billing quantities are in `TEST-CASES.yaml` → this case's `routes[]` (route facts in `route_catalogue`): kling-v3-pro, minimax-h3-max-i2v, veo-3.1-full, veo-3.1-lite-i2v, wan-3.0-prime-i2v.

**Blueprint:** `BLUEPRINTS/VID-TOPO3-01.blueprint.md` (sha256 `2f8d5591bfa7da5a…`, author executor_agent)

## Why this shape is real demand

The same Jaipur sweet shop (BR-F01-HI) asking for its Diwali poster as a 6-second WhatsApp status with the three Devanagari lines held perfectly still and readable — the request that turns a poster into a moving status is asked of every small designer each festival season, and it is the Controller's headline cheap-text topology.
