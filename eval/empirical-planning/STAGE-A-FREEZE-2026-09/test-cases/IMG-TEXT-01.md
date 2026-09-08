# IMG-TEXT-01 — IMG lane, hi (whatsapp)

## The request, as the customer sent it

**Channel:** whatsapp · **Language:** hi · **Attachments named:** none

> दीपावली के लिए एक poster चाहिए, दुकान के बाहर print और Instagram दोनों के लिए, square बनाइए। ऊपर लिखा हो "दीपावली की शुभकामनाएं", offer लिखा हो "सभी मिठाइयों पर 20% छूट", और दुकान का नाम "श्री गणेश मिष्ठान भंडार" सबसे बड़ा दिखे। Traditional feel हो लेकिन modern भी लगे। सबसे ज़रूरी चीज़ offer है, लेकिन नाम सबसे बड़ा होना चाहिए। मिठाई का डिब्बा या दीये वगैरह रख सकते हैं। Spelling एकदम सही हो, मात्रा गलत नहीं होनी चाहिए।

**Source:** pool `brief_bank`, id `BR-F01-HI`

**Adaptations:**

- register_rewritten_to_devanagari_whatsapp (source was Hinglish with Devanagari strings; the buyer is Hindi-first)
- aspect_stated_1_1
- spelling_clause_added_from_the_source's hard constraint (matras and the conjunct in मिष्ठान must render exactly)
- both planted contradictions kept (offer most important vs name largest; traditional vs modern)

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | generate | customer_stated |
| modality | static_image | customer_stated |
| supplied_assets | — (absent) | absent |
| mutation_intents | — (absent) | absent |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | [{allowed_variation: {kind_of_sweets: true}, entity_id: sweet_box_and_diyas, entity_type: product, identity_invariants: [box of Indian sweets, lit diyas], role: supporting}, {entity_id: t1, entity_type: text_element, role: hero}, {entity_id: t2, entity_type: text_element, role: hero}, {entity_id: t3, entity_type: text_element, role: hero}] | customer_stated |
| relationships | [{object: 't1,t2', relation: largest_lettering_of, subject: t3}] | customer_stated |
| text_requirements | [{content: दीपावली की शुभकामनाएं, exactness: exact, role: headline, script: devanagari, text_id: t1}, {content: सभी मिठाइयों पर 20% छूट, exactness: exact, role: body, script: devanagari, text_id: t2}, {content: श्री गणेश मिष्ठान भंडार, exactness: exact, role: brand_name, script: devanagari, text_id: t3}] | customer_stated |
| brand_requirements | — (absent) | absent |
| language_topology | {on_screen_copy: hi (Devanagari), spoken: none, subtitles: none, viewer_locale: hi-IN} | customer_stated |
| speaker_topology | — (absent) | absent |
| temporal_structure | — (absent) | absent |
| subject_motion | — (absent) | absent |
| camera_motion | — (absent) | absent |
| delivery | {aspect_ratios: ['1:1'], platform: print + instagram, resolution: ~1 MP, safe_areas: []} | — |
| ambiguity_markers | [{affected_fields: [R07, R18], detail: 'offer is ''most important'' but the shop name must be ''largest'' (source c1) — resolved in the blueprint as: name largest by size, offer first read by contrast (CA-D1: dominance by contrast, not size)', marker_type: contradiction}, {affected_fields: [R18], detail: '''traditional but modern'' (source c2) — a register choice; the blueprint declares: traditional motifs (diyas, marigold), modern layout (clean negative space, one typeface family)', marker_type: underspecification}] | system_derived (flagged) |
| acceptance_intent | {free_choices: [palette, typeface], hard_constraints: [three exact Devanagari strings, shop name largest lettering, square], soft_preferences: [sweet box or diyas], stated_rejection_criteria: [wrong matra or spelling], stated_success_criteria: [three strings exactly, shop name largest, offer most important, traditional yet modern]} | customer_stated |

`product_or_packshot_present`: True · primary capability `exact_text_devanagari`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if the lettering reads exactly "दीपावली की शुभकामनाएं", "सभी मिठाइयों पर 20% छूट" and "श्री गणेश मिष्ठान भंडार" — every matra and the conjunct ष्ठ in मिष्ठान correct, the figure 20 present as either 20 or २०; REJECT on any wrong, missing, doubled or invented character.
- ACCEPT only if "श्री गणेश मिष्ठान भंडार" is the largest lettering on the poster.
- REJECT if any other lettering or pseudo-lettering (scribbled or half-formed letters) appears anywhere.
- ACCEPT only if at least one of a sweet box or lit diyas is recognisable.
- REJECT if any string is cut by the frame edge or overlaps another string.

### E5 pre-checks (code, not shown to the judge)

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- required string absent (Cloud Vision, T-BENCH) → reject before judging
- refusal / error / empty artifact → reject

## Routes

See `TEST-CASES.yaml` → `routes[]`: flux-2-pro, gpt-image-2, nano-banana-2, nano-banana-pro, qwen-image-3, recraft-v4, seedream-5-pro.

**Blueprint:** `BLUEPRINTS/IMG-TEXT-01.blueprint.md` (sha256 `72de774d6dcaed7e…`, author executor_agent)

## Why this shape is real demand

BR-F01-HI is a Jaipur sweet shop's Diwali poster with three exact Devanagari strings, including the conjunct in मिष्ठान, and two real contradictions (offer most important but name biggest; traditional but modern). Festival offer posters are the single most common request small Indian retailers make, and they write them exactly like this.
