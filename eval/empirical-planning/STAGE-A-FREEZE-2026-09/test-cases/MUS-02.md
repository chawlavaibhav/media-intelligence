# MUS-02 — MUS lane, en (whatsapp)

## The request, as the customer sent it

**Channel:** whatsapp · **Language:** en · **Attachments named:** none

> Need a music track for our runner film - 30 seconds, we will cut it down. Early morning, empty street, building momentum, real not glossy - think a minimal beat that picks up, no vocals, no big cinematic swell. It should sit under ambient street sound, so not too busy. wav please.

**Source:** pool `brief_bank`, id `BR-F06-EN`

**Adaptations:**

- music_bed_extracted_from_the_video_brief (source: 'just music and ambient sound' for a 15-s runner film)
- duration_set_to_30s
- register_kept_email_style_whatsapp

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
| acceptance_intent | {free_choices: ['key, tempo'], hard_constraints: [30 s, no vocals], soft_preferences: [no big cinematic swell, not too busy], stated_rejection_criteria: [vocals, big cinematic swell / filmy], stated_success_criteria: [minimal beat that builds momentum, 'real, not glossy; sits under ambient street sound']} | customer_stated |

`product_or_packshot_present`: False · primary capability `emotional_prosodic_fit`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if the track is 28–32 s long and has no sung or spoken words.
- ACCEPT only if the energy audibly builds from the start to the end (more elements or a stronger pulse by the last third).
- REJECT if there is a large orchestral or 'trailer' swell, or if the arrangement is so dense it would mask street ambience.
- REJECT if the file is silent, clipped or ends abruptly mid-phrase.

### E5 pre-checks (code, not shown to the judge)

- audio probe (container, sample rate, duration: TTS ≤ 6 s / music 28–32 s)
- refusal / error / empty artifact → reject

## Routes

See `TEST-CASES.yaml` → `routes[]`: elevenlabs-music, lyria.

**Blueprint:** `BLUEPRINTS/MUS-02.blueprint.md` (sha256 `dbf2301833123c51…`, author executor_agent)

## Why this shape is real demand

BR-F06-EN's runner film wants 'just music and ambient sound', real not glossy; here the brand asks for the 30-second bed alone — a minimal building beat that sits under street sound.
