# IMG-TEXT-02 — IMG lane, en (email)

## The request, as the customer sent it

**Channel:** email · **Language:** en · **Attachments named:** none

> Hi team, we need an Instagram post for our New Year offer. It has to say "FLAT 40% OFF" and "First 100 members only" and our gym name AlphaFit. Offer ends 15 January, that should come through as well. Make it bold and energetic, something people notice while scrolling. Use our brand colours, black and neon yellow. No pictures of people, we do not have good photos of the gym yet. We will drop our logo on ourselves, just leave a clean corner for it. Square post. Thanks, Rohan

**Source:** pool `brief_bank`, id `BR-F01-EN`

**Adaptations:**

- logo_asset_deferred_to_customer_overlay (the source's logo brand asset cannot be given to a text-to-image route; the customer keeps a clean corner)
- aspect_stated_1_1
- register_rewritten_to_email (sign-off added)

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | generate | customer_stated |
| modality | static_image | customer_stated |
| supplied_assets | — (absent) | absent |
| mutation_intents | — (absent) | absent |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | [{entity_id: t1, entity_type: text_element, role: hero}, {entity_id: t2, entity_type: text_element, role: supporting}, {entity_id: t3, entity_type: text_element, role: supporting}] | customer_stated |
| relationships | — (absent) | absent |
| text_requirements | [{content: FLAT 40% OFF, exactness: exact, role: headline, script: latin, text_id: t1}, {content: First 100 members only, exactness: exact, role: body, script: latin, text_id: t2}, {content: AlphaFit, exactness: exact, role: brand_name, script: latin, text_id: t3}, {content: Offer ends 15 January, exactness: approximate, role: body, script: latin, text_id: t4}] | customer_stated |
| brand_requirements | {assets: [], mandatories: [clean empty corner for the logo], palette: {accent: neon yellow, primary: black}, palette_tolerance: as the customer states — black and neon yellow dominate, prohibitions: [no human figures]} | customer_stated |
| language_topology | {on_screen_copy: en, spoken: none, subtitles: none, viewer_locale: en-IN} | customer_stated |
| speaker_topology | — (absent) | absent |
| temporal_structure | — (absent) | absent |
| subject_motion | — (absent) | absent |
| camera_motion | — (absent) | absent |
| delivery | {aspect_ratios: ['1:1'], platform: instagram, resolution: ~1 MP, safe_areas: [one clean corner]} | — |
| ambiguity_markers | — (absent) | absent |
| acceptance_intent | {free_choices: [typeface, graphic device], hard_constraints: [three exact strings, date communicated, no human figures, brand colours, clean corner], soft_preferences: [], stated_rejection_criteria: [people in the image], stated_success_criteria: ['bold, energetic, scroll-stopping', black and neon yellow]} | customer_stated |

`product_or_packshot_present`: False · primary capability `exact_text_latin`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if the lettering reads exactly "FLAT 40% OFF", "First 100 members only" and "AlphaFit" — same letters, same case, the numerals 40 and 100 correct; REJECT on any missing, extra, swapped or malformed character.
- ACCEPT only if the 15 January end date is readable in some wording.
- REJECT if any person, silhouette or body part appears.
- ACCEPT only if black and neon yellow are the two dominant colours and one corner is empty of lettering and graphics.
- REJECT if any other lettering or pseudo-lettering appears anywhere.
- Deterministic pre-checks that count as rejects (E5): format probe (container/aspect/resolution/duration/audio-track); baked-text scan on no-text items; duration or aspect mismatch against `delivery`.

## Routes

Routes, arms, tranches and billing quantities are in `TEST-CASES.yaml` → this case's `routes[]` (route facts in `route_catalogue`): flux-2-pro, gpt-image-2, nano-banana-2, nano-banana-pro, qwen-image-3, recraft-v4, seedream-5-pro.

**Blueprint:** `BLUEPRINTS/IMG-TEXT-02.blueprint.md` (sha256 `335be8f8dd06c951…`, author executor_agent)

## Why this shape is real demand

BR-F01-EN is an Indiranagar gym's New Year offer with three exact Latin strings and brand colours, no people because there are no good photos — the bank's clean baseline for typography-led creatives. Leaving a corner for the logo is how gyms and cafes brief when the logo file lives with someone else.
