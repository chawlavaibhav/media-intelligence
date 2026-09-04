# AUD-TTS-03 — AUD lane, en (whatsapp)

## The request, as the customer sent it

**Channel:** whatsapp · **Language:** en · **Attachments named:** none

> Need the VO for our scooter film. Calm male voice, Indian English accent, not American or British. Script exactly: "Zero petrol. Zero noise. All city." Three short sentences with a small pause between each. Just the audio file please, wav if possible.

**Source:** pool `brief_bank`, id `BR-F05-EN`

**Adaptations:**

- voiceover_script_extracted_as_a_tts_request (the source is a 15-s scooter film with this VO)
- accent_stated_indian_english (the source says 'calm male voice'; the Indian-English condition is the lane's stated shape)
- end_text_dropped ("Book now at velo.in")

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
| language_topology | {on_screen_copy: none, spoken: en-IN, subtitles: none, viewer_locale: IN} | customer_stated |
| speaker_topology | {offscreen_voices: 1, script: Zero petrol. Zero noise. All city., script_exactness: exact, turn_boundaries_required: false, visible_speakers: 0} | customer_stated |
| temporal_structure | — (absent) | absent |
| subject_motion | — (absent) | absent |
| camera_motion | — (absent) | absent |
| delivery | {aspect_ratios: [], platform: audio file for a video edit, resolution: 'wav or mp3, as the route returns', safe_areas: []} | customer_stated |
| ambiguity_markers | — (absent) | absent |
| acceptance_intent | {free_choices: ['which voice, within the stated gender and register'], hard_constraints: ['the script, word for word', one voice], soft_preferences: [], stated_rejection_criteria: [], stated_success_criteria: ['calm male voice, Indian English accent']} | customer_stated |

`product_or_packshot_present`: False · primary capability `spoken_script_correctness`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if the listener hears exactly "Zero petrol. Zero noise. All city." — three sentences, no added or missing word.
- ACCEPT only if there is an audible pause between each sentence.
- ACCEPT only if the accent is recognisably Indian English; REJECT if it is American or British.
- REJECT if any music, effect or second voice is present, or if the file is longer than 6 seconds.

### E5 pre-checks (code, not shown to the judge)

- audio probe (container, sample rate, duration: TTS ≤ 6 s / music 28–32 s)
- refusal / error / empty artifact → reject

## Routes

See `TEST-CASES.yaml` → `routes[]`: elevenlabs-v3, sarvam-bulbul-v3.

**Blueprint:** `BLUEPRINTS/AUD-TTS-03.blueprint.md` (sha256 `94c11ec223134b69…`, author executor_agent)

## Why this shape is real demand

BR-F05-EN is a Chennai electric-scooter brand's three-sentence VO 'Zero petrol. Zero noise. All city.' in a calm male voice; asking for an Indian-English accent is how such brands reject the default Western voice.
