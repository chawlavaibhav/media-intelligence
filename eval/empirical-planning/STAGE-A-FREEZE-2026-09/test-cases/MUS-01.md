# MUS-01 — MUS lane, hi (whatsapp)

## The request, as the customer sent it

**Channel:** whatsapp · **Language:** hi · **Attachments named:** none

> हमारे 15 सेकंड के kitchen वाले video के लिए background music चाहिए, 30 सेकंड का clip बना दीजिए, हम काट लेंगे। घर की रसोई वाला feel — हल्का, warm, थोड़ा Indian touch (बांसुरी या तबला हल्का सा), ज़्यादा filmy नहीं। कोई गाना या बोल नहीं, सिर्फ music। Loop हो सके तो अच्छा। wav भेज दीजिए।

**Source:** pool `brief_bank`, id `BR-F06-HI`

**Adaptations:**

- music_bed_extracted_from_the_video_brief (source: 'sirf background music aur kitchen ki awaaz' for a 15-s cooker demo; here the buyer asks for the bed alone)
- duration_set_to_30s (a bed to cut from)
- instrument_hint_stated (flute or light tabla) — the customer's own words for 'Indian touch'
- register_rewritten_to_devanagari_whatsapp

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | generate | customer_stated |
| modality | audio | customer_stated |
| supplied_assets | — (absent) | absent |
| mutation_intents | — (absent) | absent |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | — (absent) | absent |
| relationships | — (absent) | absent |
| text_requirements | — (absent) | absent |
| brand_requirements | — (absent) | absent |
| language_topology | {on_screen_copy: none, spoken: none, subtitles: none, viewer_locale: IN} | customer_stated |
| speaker_topology | {offscreen_voices: 0, script_exactness: free, turn_boundaries_required: false, visible_speakers: 0} | — |
| temporal_structure | {beats: [], continuity_requirements: [loopable if possible], duration_seconds: 30, shot_count: null} | customer_stated |
| subject_motion | — (absent) | absent |
| camera_motion | — (absent) | absent |
| delivery | {aspect_ratios: [], platform: music bed for a video edit, resolution: wav preferred, safe_areas: []} | customer_stated |
| ambiguity_markers | — (absent) | absent |
| acceptance_intent | {free_choices: ['key, tempo'], hard_constraints: [30 s, no vocals], soft_preferences: [not filmy, loopable], stated_rejection_criteria: [vocals, big cinematic swell / filmy], stated_success_criteria: ['warm, light, home-kitchen feel', 'a light Indian touch: flute or soft tabla']} | customer_stated |

`product_or_packshot_present`: False · primary capability `emotional_prosodic_fit`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if the track is 28–32 s long and has no sung or spoken words.
- REJECT if drums or heavy percussion dominate the mix, or if an orchestral string or brass swell is present.
- ACCEPT only if at least one recognisably Indian instrument colour (flute/bansuri or tabla-like percussion) is audible.
- REJECT if the file is silent, clipped or ends with an abrupt cut mid-phrase.

### E5 pre-checks (code, not shown to the judge)

- audio probe (container, sample rate, duration: TTS ≤ 6 s / music 28–32 s)
- refusal / error / empty artifact → reject

## Routes

See `TEST-CASES.yaml` → `routes[]`: elevenlabs-music, lyria.

**Blueprint:** `BLUEPRINTS/MUS-01.blueprint.md` (sha256 `4d03a82e214c4c54…`, author executor_agent)

## Why this shape is real demand

BR-F06-HI is an Ahmedabad pressure-cooker brand's demo that wants 'sirf background music aur kitchen ki awaaz'; here the buyer asks for the 30-second bed alone with a light Indian touch, as brands do when the edit is in-house. Music beds for kitchen and home demos are a routine regional ask.
