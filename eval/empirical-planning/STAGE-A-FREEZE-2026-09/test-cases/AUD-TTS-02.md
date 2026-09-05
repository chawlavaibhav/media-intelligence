# AUD-TTS-02 — AUD lane, hg (whatsapp)

## The request, as the customer sent it

**Channel:** whatsapp · **Language:** hg · **Attachments named:** none

> Ek VO chahiye 15 sec ke video ke liye, young male voice, energetic aur motivational, but bharosa bhi lage, padhai ka matter hai. Thoda fast bole but clear. Line: "Job chahiye? Skill upgrade karo. Aaj hi enroll karo, Kaushal Setu par." Hindi-English mix hai, waise hi bolna hai jaise hum bolte hain. Kaushal Setu hamara naam hai, sahi bolna. Sirf audio chahiye.

**Source:** pool `brief_bank`, id `BR-F07-HG`

**Adaptations:**

- spoken_script_extracted_as_a_tts_request (the source is a 15-s single-speaker video; here the VO alone)
- brand_name_line_added_as_fixture ('Kaushal Setu par' appended: the task requires Indian brand names in the Hinglish script and the source's business is unnamed; the name is a labelled fixture, not customer text from the bank)
- script_shortened_to_drive_cap (AF-4: 'Toh' dropped and the clauses tightened so the line is ≤ 70 characters, ≈ ≤ 5 s, and ends inside the 6-s lipsync plate)
- register_rewrite_after_audit (the source's mid-sentence Devanagari 'enroll करो' typed in Latin as a Hinglish buyer types; 'education hai' → 'padhai ka matter hai')
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
| speaker_topology | {offscreen_voices: 1, script: 'Job chahiye? Skill upgrade karo. Aaj hi enroll karo, Kaushal Setu par.', script_exactness: exact, turn_boundaries_required: false, visible_speakers: 0} | customer_stated |
| temporal_structure | — (absent) | absent |
| subject_motion | — (absent) | absent |
| camera_motion | — (absent) | absent |
| delivery | {aspect_ratios: [], platform: audio file for a video edit, resolution: 'wav or mp3, as the route returns', safe_areas: []} | customer_stated |
| ambiguity_markers | [{affected_fields: [R18], detail: 'energetic vs calm/trustworthy; fast vs clearly understood (source c1, c2) — recorded; the request''s own words are the resolution (''thoda fast but clearly'')', marker_type: contradiction}] | — |
| acceptance_intent | {free_choices: ['which voice, within the stated gender and register'], hard_constraints: ['the script, word for word', one voice], soft_preferences: [], stated_rejection_criteria: [], stated_success_criteria: ['young male voice, energetic and motivational yet trustworthy; a little fast but every word clear']} | customer_stated |

`product_or_packshot_present`: False · primary capability `spoken_script_correctness`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if the listener hears exactly "Job chahiye? Skill upgrade karo. Aaj hi enroll karo, Kaushal Setu par." — every word, in order.
- ACCEPT only if "Kaushal Setu" is heard as the Hindi words कौशल सेतु; REJECT if either word is heard as something else.
- ACCEPT only if every word, English and Hindi, is understood on a single listen by a Hindi-English speaker; REJECT if any word has to be replayed to be made out.
- REJECT if any music, effect or second voice is present, or if the file is longer than 6 seconds.

### E5 pre-checks (code, not shown to the judge)

- audio probe (container, sample rate, duration: TTS ≤ 6 s / music 28–32 s)
- refusal / error / empty artifact → reject

## Routes

See `TEST-CASES.yaml` → `routes[]`: elevenlabs-v3, sarvam-bulbul-v3.

**Blueprint:** `BLUEPRINTS/AUD-TTS-02.blueprint.md` (sha256 `87944aca072597cd…`, author executor_agent)

## Why this shape is real demand

BR-F07-HG is a Noida upskilling platform's Hinglish instructor line with a Devanagari verb inside a Latin sentence — 'Aaj hi enroll करो' — and the bank's energetic-yet-calm tension. Code-mixed VO with a brand name is what edtech brands send to voice studios; the brand name is a labelled fixture.
