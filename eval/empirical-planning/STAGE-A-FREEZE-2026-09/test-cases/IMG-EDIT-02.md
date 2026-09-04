# IMG-EDIT-02 — IMG lane, hi (whatsapp)

## The request, as the customer sent it

**Channel:** whatsapp · **Language:** hi · **Attachments named:** masala_pack_raw.jpg

> इस पैक की फोटो (masala_pack_raw.jpg) का background बदल कर एकदम सफेद कर दीजिए, Amazon listing के लिए चाहिए। पैक पर जो लिखा है "शुद्ध मसाले" और "५०० ग्राम" वो बिल्कुल वैसा ही रहना चाहिए, एक भी अक्षर इधर-उधर नहीं। पैक का रंग भी वही रहे। नीचे हल्की छाया रख सकते हैं, आपकी मर्ज़ी।

**Source:** pool `rx`, id `RX-02`

**Adaptations:**

- attachment_named
- platform_named_amazon (source: e-commerce listing)

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | edit | customer_stated |
| modality | static_image | customer_stated |
| supplied_assets | [{applies_to: spice_pack, asset_id: masala_pack_raw, description: spice pack photographed against a cluttered background; printed Devanagari on the pack, media_type: image, role: subject_of_operation}] | customer_stated |
| mutation_intents | {intents: [{detail: plain white for marketplace listing, intent: change, target: background}, {detail: 'customer named this explicitly: "पैक पर जो लिखा है"', intent: preserve, target: pack label text}, {detail: customer named this explicitly, intent: preserve, target: pack colour}], preservation_default: implicit_everything_not_named} | customer_stated |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | [{allowed_variation: {shadow: true}, entity_id: spice_pack, entity_type: product, identity_invariants: [printed strings "शुद्ध मसाले" and "५०० ग्राम" byte-exact, pack colour], role: hero}] | customer_stated |
| relationships | — (absent) | absent |
| text_requirements | [{content: शुद्ध मसाले, exactness: exact, note: 'already printed on the supplied pack; must survive, not be generated', role: brand_name, script: devanagari, text_id: p1}, {content: ५०० ग्राम, exactness: exact, note: Devanagari digits; must survive, role: incidental, script: devanagari, text_id: p2}] | customer_stated (supplied strings to preserve) |
| brand_requirements | — (absent) | absent |
| language_topology | {on_screen_copy: 'hi (Devanagari, supplied)', spoken: none, subtitles: none, viewer_locale: hi-IN} | customer_stated |
| speaker_topology | — (absent) | absent |
| temporal_structure | — (absent) | absent |
| subject_motion | — (absent) | absent |
| camera_motion | — (absent) | absent |
| delivery | {aspect_ratios: [as supplied], platform: amazon listing, resolution: as supplied, safe_areas: []} | — |
| ambiguity_markers | — (absent) | absent |
| acceptance_intent | {free_choices: [shadow treatment], hard_constraints: [white background, both strings survive exactly, pack colour unchanged], soft_preferences: [], stated_rejection_criteria: [any character changed], stated_success_criteria: [background pure white, strings byte-exact, pack colour unchanged]} | customer_stated |

`product_or_packshot_present`: True · primary capability `edit_preservation`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if the background is uniformly white with no leftover clutter, edge halo or colour cast.
- ACCEPT only if the pack still reads exactly "शुद्ध मसाले" and "५०० ग्राम" — the conjunct द्ध and the Devanagari digits ५०० unchanged; REJECT if any character is altered, blurred into a different form or re-rendered in a different typeface.
- ACCEPT only if the pack's colour matches the supplied photo when flicked side by side.
- REJECT if the pack's outline, size or position has changed, or if any part of the pack is cut off.

### E5 pre-checks (code, not shown to the judge)

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

## Routes

See `TEST-CASES.yaml` → `routes[]`: flux-2-pro-edit, gpt-image-2-edit, nano-banana-pro-edit, seedream-5-pro-edit.

**Blueprint:** `BLUEPRINTS/IMG-EDIT-02.blueprint.md` (sha256 `1bd82f5a6dab5046…`, author executor_agent)

## Why this shape is real demand

RX-02 is an Indore spice brand asking for a white background for an Amazon listing while the printed Devanagari on the pack stays byte-exact. Marketplace listings require white backgrounds, and a damaged matra on a food pack is a real compliance and trust failure — the extension file explains why an English version would not test the same thing.
