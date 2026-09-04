# IMG-REF-01 — IMG lane, hi (whatsapp)

## The request, as the customer sent it

**Channel:** whatsapp · **Language:** hi · **Attachments named:** tin_front.jpg, tin_side.jpg, tin_top.jpg

> हमारे सरसों तेल के 1 लीटर टिन की 3 फोटो भेज रहा हूँ (tin_front.jpg, tin_side.jpg, tin_top.jpg)। इसी टिन का एक अच्छा photo चाहिए listing और pamphlet के लिए। टिन एकदम यही दिखे — पीला रंग वही, ऊपर जो छपा है वही, कुछ बदले नहीं, नया design मत बनाइए। Product traditional है लेकिन packaging साफ़ दिखनी चाहिए, ऐसा लगे कि घर में रोज़ इस्तेमाल होने वाला भरोसेमंद सामान है। Background साधारण रखिए, रसोई जैसा। Square।

**Source:** pool `brief_bank`, id `BR-F02-HI`

**Adaptations:**

- converted_from_generate_with_stated_strings_to_generate_with_identity_references (the source names the printed strings "शुद्ध सरसों तेल" / "कच्ची घानी"; here the printed lettering is whatever the reference tin carries and is preserved as product identity, not generated — the pack limit forbids generating Devanagari glyphs)
- reference_count_set_to_3 (three views named)
- aspect_stated_1_1
- register_rewritten_to_devanagari_whatsapp

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | generate | customer_stated |
| modality | static_image | customer_stated |
| supplied_assets | [{applies_to: oil_tin, asset_id: tin_front, description: front view of the 1 L yellow tin, media_type: image, role: identity_reference}, {applies_to: oil_tin, asset_id: tin_side, description: side view, media_type: image, role: identity_reference}, {applies_to: oil_tin, asset_id: tin_top, description: top view, media_type: image, role: identity_reference}] | customer_stated |
| mutation_intents | — (absent) | absent |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | [{allowed_variation: {angle: true, background: true}, entity_id: oil_tin, entity_type: product, identity_invariants: [1 L tin form, yellow colour, printed label exactly as on the references], role: hero}] | customer_stated |
| relationships | — (absent) | absent |
| text_requirements | — (absent) | absent |
| brand_requirements | {assets: [tin_front, tin_side, tin_top], mandatories: [], palette: {tin_yellow: as on references}, palette_tolerance: visually identical when flicked, prohibitions: [no new design]} | customer_stated |
| language_topology | {on_screen_copy: hi (as printed on the references), spoken: none, subtitles: none, viewer_locale: hi-IN} | customer_implied |
| speaker_topology | — (absent) | absent |
| temporal_structure | — (absent) | absent |
| subject_motion | — (absent) | absent |
| camera_motion | — (absent) | absent |
| delivery | {aspect_ratios: ['1:1'], platform: listing + pamphlet, resolution: ~1 MP, safe_areas: []} | — |
| ambiguity_markers | — (absent) | absent |
| acceptance_intent | {free_choices: [angle, props], hard_constraints: [identity from references, no redesign, kitchen-like plain background], soft_preferences: ['traditional product, clean packaging'], stated_rejection_criteria: [a new design], stated_success_criteria: [exactly this tin, yellow correct, printing unchanged, trustworthy household feel]} | customer_stated |

`product_or_packshot_present`: True · primary capability `product_identity`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if the tin in the result is the referenced tin and not either decoy when the judge sees the result beside the three references and the two decoys.
- ACCEPT only if the printed label reads as on the references — same words, same arrangement, same colours; REJECT if lettering is re-drawn, garbled or re-arranged.
- ACCEPT only if the tin's yellow matches the references when flicked side by side.
- REJECT if the tin's proportions, cap or handle differ from the references, or if a second tin appears.
- REJECT if any lettering appears outside the tin itself.

### E5 pre-checks (code, not shown to the judge)

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

## Routes

See `TEST-CASES.yaml` → `routes[]`: flux-2-pro-edit, gpt-image-2-edit, nano-banana-pro-edit, seedream-5-pro-edit.

**Blueprint:** `BLUEPRINTS/IMG-REF-01.blueprint.md` (sha256 `83f1d962e9cfe7d9…`, author executor_agent)

## Why this shape is real demand

BR-F02-HI is a Kanpur mustard-oil brand that wants a clean, trustworthy photo of its yellow 1-litre tin; here the customer sends three phone photos of the tin, which is how a regional FMCG owner actually briefs — 'यही टिन दिखे, कुछ बदले नहीं'. Product identity from the owner's own photographs is the bulk of Indian e-commerce imagery work.
