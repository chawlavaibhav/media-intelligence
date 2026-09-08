# VID-T2V-01 — VID lane, hi (whatsapp)

## The request, as the customer sent it

**Channel:** whatsapp · **Language:** hi · **Attachments named:** none

> एक 6 सेकंड का वीडियो चाहिए, Reels के लिए vertical। एक किसान खेत में खड़ा होकर camera के सामने बोल रहा है — "इस दवाई से मेरी फसल दोगुनी हुई"। बोलते हुए उसका चेहरा साफ़ दिखे, हाथ में product की बोतल हो। वो खुद बोलता दिखे, dubbing जैसा न लगे। Simple और भरोसेमंद लगे, ज़्यादा चमक-दमक नहीं। कोई text नहीं, "किसान भरोसा" वाला end card हम बाद में लगाएंगे।

**Source:** pool `brief_bank`, id `BR-F07-HI`

**Adaptations:**

- duration_set_to_6s (source ≈ 20 s)
- end_card_dropped_customer_adds_in_post ("किसान भरोसा" removed from the generated clip)
- register_rewrite_after_audit (the native-audio clause 'आवाज़ वीडियो में ही होनी चाहिए, अलग से voice-over नहीं' replaced by the buyer's own words 'वो खुद बोलता दिखे, dubbing जैसा न लगे'; the contract carries the test)
- aspect_stated_9_16 (Reels)
- register_rewritten_to_devanagari_whatsapp
- source flag carried: the spoken line is an efficacy claim presented as testimony; recorded as the customer wrote it, never to be used as real advertising without substantiation

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | generate | customer_stated |
| modality | video | customer_stated |
| supplied_assets | — (absent) | absent |
| mutation_intents | — (absent) | absent |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | [{allowed_variation: {age: true, clothing: true}, entity_id: farmer, entity_type: person, identity_invariants: [adult Indian farmer, face visible while speaking], role: hero}, {allowed_variation: {form: true}, entity_id: product_bottle, entity_type: product, identity_invariants: ['a bottle of agricultural input, held in hand', no readable label], role: supporting}] | customer_stated |
| relationships | [{object: product_bottle, relation: holds, subject: farmer}] | customer_stated |
| text_requirements | — (absent) | absent |
| brand_requirements | — (absent) | absent |
| language_topology | {on_screen_copy: none, spoken: hi, subtitles: none, viewer_locale: hi-IN} | customer_stated |
| speaker_topology | {offscreen_voices: 0, script: इस दवाई से मेरी फसल दोगुनी हुई, script_exactness: exact, turn_boundaries_required: false, visible_speakers: 1} | customer_stated |
| temporal_structure | {beats: [{beat: 1, content: farmer looks at camera and speaks the line}], continuity_requirements: [], duration_seconds: 6, shot_count: 1} | customer_stated |
| subject_motion | {description: speaks to camera; lips move with the words, entity_ref: farmer, motion_type: gesture} | customer_implied |
| camera_motion | {description: not stated by the customer; delegated — the blueprint chooses stillness, motion_type: static} | system_derived — camera delegated; stillness chosen (CA-D11) |
| delivery | {aspect_ratios: ['9:16'], platform: instagram reels, resolution: 720p, safe_areas: []} | — |
| ambiguity_markers | [{affected_fields: [R11], detail: '''इस दवाई से मेरी फसल दोगुनी हुई'' is an efficacy claim; recorded, not softened (source flag)', marker_type: unverifiable_claim}] | — |
| acceptance_intent | {free_choices: ['field, crop, time of day'], hard_constraints: ['one visible speaker, Hindi', the exact line, bottle in hand, no lettering], soft_preferences: [not flashy], stated_rejection_criteria: [looks dubbed, any text], stated_success_criteria: [face clearly visible while speaking, voice in the video, simple and trustworthy]} | customer_stated |

`product_or_packshot_present`: True · primary capability `single_speaker_lip_sync`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if one man is visible speaking to camera and the audio track carries a Hindi voice saying "इस दवाई से मेरी फसल दोगुनी हुई" — every word present and in order; REJECT if a word is missing, garbled, or spoken in another language.
- ACCEPT only if his mouth opens and closes in time with the spoken words (a first-language judge hears and sees the same syllables).
- REJECT if the clip is silent or the voice is a separate narration over a closed mouth.
- ACCEPT only if a bottle is held in his hand for the whole clip and stays the same object.
- REJECT if any lettering appears anywhere in any frame.

### E5 pre-checks (code, not shown to the judge)

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- duration or aspect mismatch vs `delivery`
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

## Routes

See `TEST-CASES.yaml` → `routes[]`: gemini-omni-1.1-flash, kling-v3-pro-audio, minimax-h3-max, seedance-2.5, sora-2, veo-3.1-fast, wan-3.0-prime.

**Blueprint:** `BLUEPRINTS/VID-T2V-01.blueprint.md` (sha256 `22a6b861659cc8f8…`, author executor_agent)

## Why this shape is real demand

BR-F07-HI is a Nashik agri-inputs dealer wanting a farmer speaking one Hindi line to camera with the product in hand — 'simple aur bharosemand'. Testimonial-style talking clips in Hindi are the dominant rural-marketing format; the source flags the efficacy claim and so does this case.
