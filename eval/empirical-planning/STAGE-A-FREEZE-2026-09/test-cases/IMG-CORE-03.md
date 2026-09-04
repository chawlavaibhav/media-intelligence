# IMG-CORE-03 — IMG lane, hg (whatsapp)

## The request, as the customer sent it

**Channel:** whatsapp · **Language:** hg · **Attachments named:** none

> Zomato pe jo top brands ke creatives hote hain waise ek biryani ka photo chahiye. Hamare paas abhi dhang ke photos nahi hain toh bana do - upar se, top view, biryani ki handi beech mein, side mein raita, salad, pyaaz, nimbu, thoda spread type. Premium lagna chahiye but hum budget brand hain toh over the top nahi, cheap bhi nahi. Unke jaisa quality but copy mat karna, apna alag lage. Koi text ya price mat likhna, ₹199 waala part aur logo hum khud daalenge. Square, Zomato aur Insta dono pe jaayega.

**Source:** pool `brief_bank`, id `BR-F04-HG`

**Adaptations:**

- text_requirement_dropped_for_core ("Biryani starting ₹199" removed; customer states price and logo go on later)
- supplied_food_photo_replaced_by_generate (customer states they have no usable photos — the BR-F01-EN condition)
- competitor_reference_dropped (no competitor asset attached; the quality-bar-vs-copy tension kept in words)
- shape_set_to_flat_lay (top view, several dishes — the core's flat-lay slot)
- aspect_stated_1_1

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | generate | customer_stated |
| modality | static_image | customer_stated |
| supplied_assets | — (absent) | absent |
| mutation_intents | — (absent) | absent |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | [{allowed_variation: {garnish: true}, entity_id: biryani_handi, entity_type: product, identity_invariants: [biryani in a handi (round pot), centre of frame], role: hero}, {allowed_variation: {arrangement: true}, entity_id: sides, entity_type: object, identity_invariants: [raita, salad, onion, lemon], role: supporting}] | customer_stated |
| relationships | [{object: biryani_handi, relation: arranged_around, subject: sides}] | customer_stated |
| text_requirements | — (absent) | absent |
| brand_requirements | — (absent) | absent |
| language_topology | {on_screen_copy: none, spoken: none, subtitles: none, viewer_locale: hi-en-IN} | customer_implied |
| speaker_topology | — (absent) | absent |
| temporal_structure | — (absent) | absent |
| subject_motion | — (absent) | absent |
| camera_motion | — (absent) | absent |
| delivery | {aspect_ratios: ['1:1'], platform: zomato + instagram, resolution: ~1 MP, safe_areas: []} | — |
| ambiguity_markers | [{affected_fields: [R18], detail: '''like the top brands'' and ''do not copy them'' (source c1); ''premium but budget, not cheap'' (source c2). Recorded; the blueprint treats the first as a quality bar and the second as a register choice (clean, generous, no luxury props).', marker_type: contradiction}] | — |
| acceptance_intent | {free_choices: [surface, props beyond the named sides], hard_constraints: [top view, biryani handi centred, 'raita, salad, onion, lemon present', no text], soft_preferences: [premium but not lavish], stated_rejection_criteria: [looks cheap, over the top, any text or price], stated_success_criteria: [premium quality bar, looks distinct, top view spread]} | customer_stated |

`product_or_packshot_present`: True · primary capability `hierarchy_product_as_hero`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if the camera looks straight down (top view) and a round pot of biryani sits at the centre.
- ACCEPT only if all four named sides are identifiable: a bowl of raita, salad, sliced onion, and lemon.
- REJECT if any lettering, price, logo or numeral appears anywhere (including on crockery or napkins).
- REJECT if rice grains, meat pieces or garnish are visibly melted, fused or duplicated in a repeating pattern.
- REJECT if the spread includes luxury props (gold cutlery, wine glass, candles) — the customer asked for premium but not over the top.
- Deterministic pre-checks that count as rejects (E5): format probe (container/aspect/resolution/duration/audio-track); baked-text scan on no-text items; duration or aspect mismatch against `delivery`.

## Routes

Routes, arms, tranches and billing quantities are in `TEST-CASES.yaml` → this case's `routes[]` (route facts in `route_catalogue`): flux-2-pro, gpt-image-2, mai-image-2.6, nano-banana-2, nano-banana-pro, qwen-image-3, sd3.5-large, seedream-5-pro.

**Blueprint:** `BLUEPRINTS/IMG-CORE-03.blueprint.md` (sha256 `ed23ebc78411341d…`, author executor_agent)

## Why this shape is real demand

BR-F04-HG is a Hyderabad cloud kitchen that wants to look like the top Zomato brands without copying them, at a budget price point, and — like most small Indian food businesses — has no usable photography (the honest condition the bank records under BR-F01-EN). A generated top-view biryani spread with the price and logo added later is exactly what such a kitchen sends its designer.
