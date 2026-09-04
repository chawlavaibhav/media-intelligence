# AUD-TTS-01 — AUD lane, hi (whatsapp)

## The request, as the customer sent it

**Channel:** whatsapp · **Language:** hi · **Attachments named:** none

> एक voice-over line चाहिए हमारे 10 सेकंड वाले detergent video के लिए। पुरुष आवाज़, साफ़ हिंदी, घरेलू और भरोसेमंद, ज़्यादा नाटकीय नहीं। Line है: "एक धुलाई में दाग गायब"। बस यही, सिर्फ audio file (wav या mp3) भेज दीजिए।

**Source:** pool `brief_bank`, id `BR-F05-HI`

**Adaptations:**

- voiceover_script_extracted_as_a_tts_request (the source is a 10-s product video with this VO line; here the buyer asks for the VO alone)
- voice_gender_stated_male (the source names none; chosen so the same voice can drive the male-plate lipsync cases)
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
| language_topology | {on_screen_copy: none, spoken: hi, subtitles: none, viewer_locale: IN} | customer_stated |
| speaker_topology | {offscreen_voices: 1, script: एक धुलाई में दाग गायब, script_exactness: exact, turn_boundaries_required: false, visible_speakers: 0} | customer_stated |
| temporal_structure | — (absent) | absent |
| subject_motion | — (absent) | absent |
| camera_motion | — (absent) | absent |
| delivery | {aspect_ratios: [], platform: audio file for a video edit, resolution: 'wav or mp3, as the route returns', safe_areas: []} | customer_stated |
| ambiguity_markers | — (absent) | absent |
| acceptance_intent | {free_choices: ['which voice, within the stated gender and register'], hard_constraints: ['the script, word for word', one voice], soft_preferences: [], stated_rejection_criteria: [], stated_success_criteria: ['male voice, clear Hindi, homely and trustworthy, not theatrical']} | customer_stated |

`product_or_packshot_present`: False · primary capability `spoken_script_correctness`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if a first-language Hindi listener hears exactly "एक धुलाई में दाग गायब" — every word, in order, no extra word.
- ACCEPT only if it is one male voice speaking clear standard Hindi; REJECT if the accent makes any word ambiguous (e.g. धुलाई heard as another word).
- REJECT if any music, effect, second voice or English word is present.
- REJECT if the file is silent, truncated mid-word, or longer than 6 seconds.
- Deterministic pre-checks that count as rejects (E5): format probe (container/aspect/resolution/duration/audio-track); baked-text scan on no-text items; duration or aspect mismatch against `delivery`.

## Routes

Routes, arms, tranches and billing quantities are in `TEST-CASES.yaml` → this case's `routes[]` (route facts in `route_catalogue`): azure-neural-tts-hi-in, chirp-3-hd-hi-in, elevenlabs-v3, sarvam-bulbul-v3.

**Blueprint:** `BLUEPRINTS/AUD-TTS-01.blueprint.md` (sha256 `1e1cf42cf56f0472…`, author executor_agent)

## Why this shape is real demand

BR-F05-HI is an Indore detergent brand's ten-second demo whose voice-over line is 'एक धुलाई में दाग गायब'; here the buyer asks for that VO alone, as brands do when the video is cut in-house. A one-line Hindi efficacy VO is the commonest TTS job in regional FMCG.
