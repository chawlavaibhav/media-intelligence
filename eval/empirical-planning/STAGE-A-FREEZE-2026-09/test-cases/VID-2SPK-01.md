# VID-2SPK-01 — VID lane, hi (whatsapp)

## The request, as the customer sent it

**Channel:** whatsapp · **Language:** hi · **Attachments named:** none

> 8 सेकंड का वीडियो चाहिए, Reels और Status के लिए vertical। दो लोग — पति-पत्नी, 30-35 साल — नए घर में दीवार का रंग चुन रहे हैं, हाथ में paint का डिब्बा। पत्नी कहती है "यह रंग कैसा लगेगा?" और पति कहता है "घर जैसा"। दोनों की आवाज़ वीडियो में ही हो, असली बातचीत जैसी लगे। Emotional और warm लगे। पति का जवाब "घर जैसा" बदलना नहीं, वो हमारी tagline से जुड़ा है। कोई text नहीं, "रंग जो घर बनाए" वाला end card हम लगाएंगे।

**Source:** pool `brief_bank`, id `BR-F08-HI`

**Adaptations:**

- duration_set_to_8s (source ≈ 20 s; two turns with a pause need 8 s — system_derived, recorded)
- end_card_dropped_customer_adds_in_post ("रंग जो घर बनाए")
- ages_stated (30–35) so the chain arm's TTS voices can be chosen
- register_rewrite_after_audit (the turn-assignment clause 'जो बोल रहा है उसी के होंठ हिलें, दूसरे के नहीं' removed; the buyer now says 'असली बातचीत जैसी लगे' and the contract carries the turn test)
- aspect_stated_9_16
- register_rewritten_to_devanagari_whatsapp

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | generate | customer_stated |
| modality | video | customer_stated |
| supplied_assets | — (absent) | absent |
| mutation_intents | — (absent) | absent |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | [{entity_id: wife, entity_type: person, identity_invariants: ['woman, 30–35', consistent identity], role: hero}, {entity_id: husband, entity_type: person, identity_invariants: ['man, 30–35', consistent identity], role: hero}, {entity_id: paint_can, entity_type: product, identity_invariants: ['a paint can, visible', no readable label], role: supporting}] | customer_stated (ages 30–35 by adaptation, listed) |
| relationships | [{object: husband, relation: speaks_to, subject: wife}, {object: wife, relation: replies_to, subject: husband}, {object: paint_can, relation: holds, subject: husband}] | system_derived — 'speaks_to / replies_to' are customer_stated; 'husband holds paint_can' is the Executor's staging — the source says only 'paint can dikhe' |
| text_requirements | — (absent) | absent |
| brand_requirements | — (absent) | absent |
| language_topology | {on_screen_copy: none, spoken: hi, subtitles: none, viewer_locale: hi-IN} | customer_stated |
| speaker_topology | {offscreen_voices: 0, script_exactness: exact, turn_boundaries_required: true, turns: [{line: 'यह रंग कैसा लगेगा?', speaker: wife}, {line: घर जैसा, speaker: husband}], visible_speakers: 2} | customer_stated |
| temporal_structure | {beats: [{beat: 1, content: wife asks}, {beat: 2, content: husband answers}], continuity_requirements: [both identities constant], duration_seconds: 8, shot_count: 1} | system_derived — 8 s chosen on the freeze for two turns plus a pause; the source says ≈ 20 s; the request text states 8 s by adaptation |
| subject_motion | {description: each speaks in turn; the wife gestures at the wall, entity_ref: 'wife, husband', motion_type: gesture} | customer_implied |
| camera_motion | {description: delegated; stillness chosen, motion_type: static} | system_derived — delegated; stillness (CA-D11) |
| delivery | {aspect_ratios: ['9:16'], platform: reels + whatsapp status, resolution: 720p, safe_areas: []} | — |
| ambiguity_markers | — (absent) | absent |
| acceptance_intent | {free_choices: ['room, colour on the wall'], hard_constraints: [two people, two Hindi turns in order, paint can visible, turn-correct lip movement, no lettering], soft_preferences: [new home], stated_rejection_criteria: [the reply paraphrased, any text], stated_success_criteria: [both voices in the video, only the speaker's lips move, 'warm, emotional']} | customer_stated |

`product_or_packshot_present`: True · primary capability `two_speaker_turn_assignment_and_lip_sync`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if two adults are visible and the audio carries, in Hindi and in this order, "यह रंग कैसा लगेगा?" then "घर जैसा" — every word present; REJECT if either line is missing, changed or paraphrased.
- ACCEPT only if the woman's lips move while the first line is spoken and the man's lips move while the second is spoken.
- REJECT if the second speaker's lips move while the first line is spoken, or the first speaker's while the second is spoken.
- ACCEPT only if a paint can is visible at some point in the clip.
- REJECT if either person changes identity within the clip, or if any lettering appears.

### E5 pre-checks (code, not shown to the judge)

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- duration or aspect mismatch vs `delivery`
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

## Routes

See `TEST-CASES.yaml` → `routes[]`: elevenlabs-v3, flux-2-pro, gemini-omni-1.1-flash, kling-lipsync-a2v, kling-v3-pro-audio, minimax-h3-max-i2v, sarvam-bulbul-v3, seedance-2.5, sync-lipsync-v3, veo-3.1-fast, wan-3.0-prime.

**Blueprint:** `BLUEPRINTS/VID-2SPK-01.blueprint.md` (sha256 `3450eb2363323b49…`, author executor_agent)

## Why this shape is real demand

BR-F08-HI is a Jaipur paint brand's husband-and-wife exchange — 'यह रंग कैसा लगेगा?' / 'घर जैसा' — with the pun preserved and the paint can visible. Two-person emotional dialogue is the Indian TV-ad idiom carried into Reels; the customer's own words ('जो बोल रहा है उसी के होंठ हिलें') name the turn-assignment requirement.
