# AUD-TTS-02 — AUD lane, hg (whatsapp)

## The request, as the customer sent it

**Channel:** whatsapp · **Language:** hg · **Attachments named:** none

> Ek VO chahiye 15 sec video ke liye, young male voice, energetic aur motivational but trustworthy bhi, education hai. Thoda fast bole but clearly samajh aaye. Line: "Job chahiye? Toh skill upgrade karo. Aaj hi enroll करो — Kaushal Setu par." Hindi-English mix hai, waise hi bolna hai jaise hum bolte hain. "Kaushal Setu" hamara naam hai, sahi bolna. Sirf audio chahiye.

**Source:** pool `brief_bank`, id `BR-F07-HG`

**Adaptations:**

- spoken_script_extracted_as_a_tts_request (the source is a 15-s single-speaker video; here the VO alone)
- brand_name_line_added_as_fixture ('— Kaushal Setu par.' appended: the task requires Indian brand names in the Hinglish script and the source's business is unnamed; the name is a labelled fixture, not customer text from the bank)
- end_card_dropped ("Batch starts Monday")
- both source contradictions kept (energetic vs calm; fast vs clear)

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
| language_topology | {on_screen_copy: none, spoken: hi-en (Hinglish), subtitles: none, viewer_locale: IN} | customer_stated |
| speaker_topology | {offscreen_voices: 1, script: 'Job chahiye? Toh skill upgrade karo. Aaj hi enroll करो — Kaushal Setu par.', script_exactness: exact, turn_boundaries_required: false, visible_speakers: 0} | customer_stated |
| temporal_structure | — (absent) | absent |
| subject_motion | — (absent) | absent |
| camera_motion | — (absent) | absent |
| delivery | {aspect_ratios: [], platform: audio file for a video edit, resolution: 'wav or mp3, as the route returns', safe_areas: []} | customer_stated |
| ambiguity_markers | [{affected_fields: [R18], detail: 'energetic vs calm/trustworthy; fast vs clearly understood (source c1, c2) — recorded; the request''s own words are the resolution (''thoda fast but clearly'')', marker_type: contradiction}] | — |
| acceptance_intent | {free_choices: ['which voice, within the stated gender and register'], hard_constraints: ['the script, word for word', one voice], soft_preferences: [], stated_rejection_criteria: [], stated_success_criteria: ['young male voice, energetic and motivational yet trustworthy; a little fast but every word clear']} | customer_stated |

`product_or_packshot_present`: False · primary capability `spoken_script_correctness`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if the listener hears exactly "Job chahiye? Toh skill upgrade karo. Aaj hi enroll करो — Kaushal Setu par." — every word, in order.
- ACCEPT only if "Kaushal Setu" is pronounced as a Hindi name (कौशल सेतु), not anglicised; REJECT if either word is mangled.
- ACCEPT only if the English words (job, skill, upgrade, enroll) sound as an Indian speaker says them inside a Hindi sentence, not as a separate English accent.
- REJECT if any music, effect or second voice is present, or if the file is longer than 8 seconds.
- REJECT if the delivery is so fast that a word is lost, or so slow that it reads as a lullaby (the customer asked for fast but clear).
- Deterministic pre-checks that count as rejects (E5): format probe (container/aspect/resolution/duration/audio-track); baked-text scan on no-text items; duration or aspect mismatch against `delivery`.

## Routes

Routes, arms, tranches and billing quantities are in `TEST-CASES.yaml` → this case's `routes[]` (route facts in `route_catalogue`): elevenlabs-v3, sarvam-bulbul-v3.

**Blueprint:** `BLUEPRINTS/AUD-TTS-02.blueprint.md` (sha256 `6e06cf0b25e69985…`, author executor_agent)

## Why this shape is real demand

BR-F07-HG is a Noida upskilling platform's Hinglish instructor line with a Devanagari verb inside a Latin sentence — 'Aaj hi enroll करो' — and the bank's energetic-yet-calm tension. Code-mixed VO with a brand name is what edtech brands send to voice studios; the brand name is a labelled fixture.
