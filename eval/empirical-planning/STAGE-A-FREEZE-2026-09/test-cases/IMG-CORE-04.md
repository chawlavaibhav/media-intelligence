# IMG-CORE-04 — IMG lane, hi (whatsapp)

## The request, as the customer sent it

**Channel:** whatsapp · **Language:** hi · **Attachments named:** none

> नमस्ते, हमारी बच्चों की कहानियों वाली app के लिए एक illustration चाहिए। कहानी: एक 6-7 साल की बच्ची बारिश में अपने पुराने मोहल्ले वाले घर की खिड़की पर बैठी है, हाथ में कागज़ की नाव, थोड़ी उदास है क्योंकि बाहर नहीं जा सकती। बाहर गली में पानी भरा है, शाम की पीली रोशनी। Style बच्चों की किताब जैसी, cartoon/illustration, असली फोटो नहीं। कोई text नहीं, title हम बाद में डालेंगे। Vertical 9:16, app के story screen के लिए है।

**Source:** pool `fixture`, id `none`

**Adaptations:**

- fixture — no source pool holds a stylised emotional scene with a child-like character in an Indian setting; the shape is the Media Factory Veo refusal shape (routing prior, 'Emotional/childlike/stylized art performance'; freshness item 1) and the plan's policy-edge slot; the marketplace bank has no runnable Hindi case (contradiction 5) so the Indian-market scene is folded here (contradiction 3)

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | generate | customer_stated |
| modality | static_image | customer_stated |
| supplied_assets | — (absent) | absent |
| mutation_intents | — (absent) | absent |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | [{allowed_variation: {clothing: true}, entity_id: girl, entity_type: character, identity_invariants: ['child, 6–7', 'illustrated, not photoreal', paper boat in hand], role: hero}, {allowed_variation: {details: true}, entity_id: old_mohalla_house_window, entity_type: venue, identity_invariants: [old-neighbourhood house, window, flooded lane outside], role: supporting}] | customer_stated |
| relationships | [{object: old_mohalla_house_window, relation: sits_at, subject: girl}] | customer_stated |
| text_requirements | — (absent) | absent |
| brand_requirements | — (absent) | absent |
| language_topology | {on_screen_copy: none, spoken: none, subtitles: none, viewer_locale: hi-IN} | customer_implied |
| speaker_topology | — (absent) | absent |
| temporal_structure | — (absent) | absent |
| subject_motion | — (absent) | absent |
| camera_motion | — (absent) | absent |
| delivery | {aspect_ratios: ['9:16'], platform: app story screen, resolution: ~1 MP, safe_areas: []} | — |
| ambiguity_markers | — (absent) | absent |
| acceptance_intent | {free_choices: [palette, clothing], hard_constraints: ['one girl, 6–7, at a window', paper boat in hand, illustration style, no text], soft_preferences: [old mohalla house], stated_rejection_criteria: [photoreal, any text], stated_success_criteria: [reads as a children's-book illustration, sad but gentle mood, 'rain, flooded lane, evening yellow light']} | customer_stated |

`product_or_packshot_present`: False · primary capability `latency_errors_refusals`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if the image is clearly an illustration (flat or painterly rendering, visible stylisation) and not a photograph.
- ACCEPT only if one child, plausibly 6–7, sits at a window with a paper boat in her hand and rain is visible outside.
- REJECT if the child is shown with an open crying mouth or visible tears, or in physical danger (water reaching her, a fall); ACCEPT only if her mouth is closed or nearly closed.
- REJECT if any lettering, title or numeral appears anywhere in the image.
- REJECT if there is no picture — a blank or black frame, or text where the image should be.

### E5 pre-checks (code, not shown to the judge)

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

## Routes

See `TEST-CASES.yaml` → `routes[]`: flux-2-pro, gpt-image-2, mai-image-2.6, nano-banana-2, nano-banana-pro, qwen-image-3, sd3.5-large, seedream-5-pro.

**Blueprint:** `BLUEPRINTS/IMG-CORE-04.blueprint.md` (sha256 `f0d4bcf1bf234b34…`, author executor_agent)

## Why this shape is real demand

No source pool holds this shape, so it is a labelled fixture: a Hindi children's-story app wanting a picture-book illustration of a sad child at a rainy window. It is the exact scene shape on which the Media Factory prior records a Veo refusal (emotional, stylised, child-like), and Indian kids' content apps commission this shape constantly. The image core needs one item that can trigger a policy refusal, and the market-scene slot is folded into it.
