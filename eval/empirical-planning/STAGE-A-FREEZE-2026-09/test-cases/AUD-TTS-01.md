# AUD-TTS-01 — AUD lane, hi (whatsapp)

## The request, as the customer sent it

**Channel:** whatsapp · **Language:** hi · **Attachments named:** none

> एक voice-over line चाहिए हमारे किसान वाले video के लिए, video अलग से बन रहा है। पुरुष आवाज़, किसान जैसी सादी हिंदी, भरोसेमंद, ज़्यादा नाटकीय नहीं। Line है: "इस दवाई से मेरी फसल दोगुनी हुई"। बस यही, सिर्फ audio file (wav या mp3) भेज दीजिए।

**Source:** pool `brief_bank`, id `BR-F07-HI`

**Adaptations:**

- spoken_line_extracted_as_a_tts_request (the source is the 20-s farmer testimonial video; the same Nashik dealer asks for the line as a VO for a separate edit)
- line_shared_with_VID-T2V-01_after_audit (AF-2: TOPO-01 arm A and arm B now carry the same brief and the same spoken line; the first draft used BR-F05-HI's detergent line, which is no longer in the package)
- voice_gender_stated_male (the source's speaker is a farmer, male by the source's own pronoun; chosen so the same voice can drive the male-plate lipsync cases)
- register_rewritten_to_devanagari_whatsapp
- source flag carried: the line is an efficacy claim presented as testimony

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
| speaker_topology | {offscreen_voices: 1, script: इस दवाई से मेरी फसल दोगुनी हुई, script_exactness: exact, turn_boundaries_required: false, visible_speakers: 0} | customer_stated |
| temporal_structure | — (absent) | absent |
| subject_motion | — (absent) | absent |
| camera_motion | — (absent) | absent |
| delivery | {aspect_ratios: [], platform: audio file for a video edit, resolution: 'wav or mp3, as the route returns', safe_areas: []} | customer_stated |
| ambiguity_markers | — (absent) | absent |
| acceptance_intent | {free_choices: ['which voice, within the stated gender and register'], hard_constraints: ['the script, word for word', one voice], soft_preferences: [], stated_rejection_criteria: [], stated_success_criteria: ['male voice, plain farmer-like Hindi, trustworthy, not theatrical']} | customer_stated |

`product_or_packshot_present`: False · primary capability `spoken_script_correctness`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if a first-language Hindi listener hears exactly "इस दवाई से मेरी फसल दोगुनी हुई" — every word, in order, no extra word.
- ACCEPT only if it is one male voice speaking clear Hindi; REJECT if any word is heard as a different word (e.g. दवाई or दोगुनी mispronounced into another word).
- REJECT if any music, effect, second voice or English word is present.
- REJECT if the file is silent, truncated mid-word, or longer than 6 seconds.

### E5 pre-checks (code, not shown to the judge)

- audio probe (container, sample rate, duration: TTS ≤ 6 s / music 28–32 s)
- refusal / error / empty artifact → reject

## Routes

See `TEST-CASES.yaml` → `routes[]`: azure-neural-tts-hi-in, chirp-3-hd-hi-in, elevenlabs-v3, sarvam-bulbul-v3.

**Blueprint:** `BLUEPRINTS/AUD-TTS-01.blueprint.md` (sha256 `3c10c117788072ed…`, author executor_agent)

## Why this shape is real demand

BR-F05-HI is an Indore detergent brand's ten-second demo whose voice-over line is 'एक धुलाई में दाग गायब'; here the buyer asks for that VO alone, as brands do when the video is cut in-house. A one-line Hindi efficacy VO is the commonest TTS job in regional FMCG.
