# IMG-CORE-01 — IMG lane, en (whatsapp)

## The request, as the customer sent it

**Channel:** whatsapp · **Language:** en · **Attachments named:** none

> Hi, need a clean product shot of our 250ml cold pressed orange juice bottle for the launch page. Just the bottle, nothing else in frame, light background, premium feel. Bottle is glass so it should actually look like glass, not plastic. Keep the label area blank pls - our label artwork goes on in post, so no text or logo anywhere on the image. Don't have a photo yet, standard 250ml round-shoulder glass bottle with a metal cap is fine. 4:5 for the site and Insta.

**Source:** pool `brief_bank`, id `BR-F02-EN`

**Adaptations:**

- text_requirement_dropped_for_core ("Cold-pressed. Nothing else." removed; customer states copy goes on in post)
- label_lettering_dropped_for_core (blank label area so no lettering appears; customer states label artwork goes on in post)
- aspect_stated_4_5 (customer names site + Instagram)
- register_rewritten_to_whatsapp

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | generate | customer_stated |
| modality | static_image | customer_stated |
| supplied_assets | — (absent) | absent |
| mutation_intents | — (absent) | absent |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | [{allowed_variation: {angle: true, background: true}, entity_id: juice_bottle, entity_type: product, identity_invariants: [250 ml round-shoulder glass bottle, metal cap, orange juice inside, blank label area], role: hero}] | customer_stated |
| relationships | — (absent) | absent |
| text_requirements | — (absent) | absent |
| brand_requirements | — (absent) | absent |
| language_topology | {on_screen_copy: none, spoken: none, subtitles: none, viewer_locale: en-IN} | customer_implied |
| speaker_topology | — (absent) | absent |
| temporal_structure | — (absent) | absent |
| subject_motion | — (absent) | absent |
| camera_motion | — (absent) | absent |
| delivery | {aspect_ratios: ['4:5'], platform: website + Instagram, resolution: ~1 MP, safe_areas: []} | — |
| ambiguity_markers | — (absent) | absent |
| acceptance_intent | {free_choices: [angle, exact background tone], hard_constraints: ['single product, nothing else in frame', blank label area, no text or logo], soft_preferences: [premium feel], stated_rejection_criteria: [plastic look, anything else in frame, any text or logo], stated_success_criteria: [reads as glass, premium feel, light background]} | customer_stated |

`product_or_packshot_present`: True · primary capability `hierarchy_product_as_hero`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if exactly one bottle is in frame and no other object, hand or prop appears.
- ACCEPT only if the bottle reads as clear glass with liquid inside — a visible refracted edge or a light-through-liquid glow — not as an opaque or plastic body.
- ACCEPT only if the label area is blank: no lettering, logo, numeral or symbol anywhere on the bottle or the image.
- REJECT if the cap, neck or base is deformed, doubled or cut off by the frame edge.
- REJECT if the background is dark or cluttered (the customer asked for a light background).

### E5 pre-checks (code, not shown to the judge)

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

## Routes

See `TEST-CASES.yaml` → `routes[]`: flux-2-pro, gpt-image-2, mai-image-2.6, nano-banana-2, nano-banana-pro, qwen-image-3, sd3.5-large, seedream-5-pro.

**Blueprint:** `BLUEPRINTS/IMG-CORE-01.blueprint.md` (sha256 `dba8636060372bc5…`, author executor_agent)

## Why this shape is real demand

BR-F02-EN is the brief bank's purest packshot: a Mumbai cold-pressed juice brand asking for one clean bottle shot on a light ground for a launch. Its notes say it directly exercises the reflection physics that make glass read as glass — the shape every D2C beverage brand asks for first. The only change is that the label copy goes on in post, which is how launch shots are actually briefed when the label artwork is still with the designer.
