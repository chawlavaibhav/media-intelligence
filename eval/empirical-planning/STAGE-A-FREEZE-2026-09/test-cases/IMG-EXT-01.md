# IMG-EXT-01 — IMG lane, en (email)

## The request, as the customer sent it

**Channel:** email · **Language:** en · **Attachments named:** backwaters_banner_16x9.jpg

> Hi, we have this landscape banner (backwaters_banner_16x9.jpg) but we need a vertical version for Stories. Can you extend the image top and bottom so it works at 9:16? Please don't crop the boat or the headline, both need to stay fully visible and in the same position relative to each other. The new area should just continue the scene, sky above and water below. Regards, Anitha

**Source:** pool `rx`, id `RX-07`

**Adaptations:**

- attachment_named
- fill_direction_stated (sky above, water below) — the customer's own free choice made explicit
- register_rewritten_to_email

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | extend | customer_stated |
| modality | static_image | customer_stated |
| supplied_assets | [{applies_to: banner, asset_id: backwaters_banner_16x9, description: '16:9 banner: a boat on backwaters with a typeset Latin headline', media_type: image, role: subject_of_operation}] | customer_stated |
| mutation_intents | {intents: [{detail: 'fully visible, same relationship', intent: preserve, target: boat and headline}, {detail: 'extend vertically to 9:16', intent: transform, target: canvas bounds}, {detail: 'sky above, water below, continuing the scene', intent: add, target: new area}], preservation_default: implicit_everything_not_named} | customer_stated |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | [{entity_id: boat, entity_type: object, identity_invariants: [fully visible, unchanged], role: hero}, {entity_id: headline, entity_type: text_element, identity_invariants: [fully visible, unchanged glyphs], role: hero}] | customer_stated |
| relationships | [{object: headline, relation: same_spatial_relationship_as_supplied, subject: boat}] | customer_stated |
| text_requirements | [{content: (the headline as typeset on the supplied banner — fixture string recorded at asset specification), exactness: exact, note: 'supplied lettering to preserve, not to generate', role: headline, script: latin, text_id: h1}] | customer_stated (supplied) |
| brand_requirements | — (absent) | absent |
| language_topology | {on_screen_copy: en (supplied), spoken: none, subtitles: none, viewer_locale: en-IN} | — |
| speaker_topology | — (absent) | absent |
| temporal_structure | — (absent) | absent |
| subject_motion | — (absent) | absent |
| camera_motion | — (absent) | absent |
| delivery | {aspect_ratios: ['9:16'], platform: instagram stories, resolution: as supplied width, safe_areas: []} | — |
| ambiguity_markers | — (absent) | absent |
| acceptance_intent | {free_choices: [what appears in the new area beyond sky/water], hard_constraints: ['final aspect 9:16', boat not cropped, headline not cropped, relationship preserved], soft_preferences: [extended area consistent with the scene], stated_rejection_criteria: [cropping], stated_success_criteria: ['9:16 by extension', boat and headline fully visible, scene continues]} | customer_stated |

`product_or_packshot_present`: False · primary capability `edit_preservation`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if the result is 9:16 and contains the whole supplied banner uncropped — the boat and every letter of the headline fully visible.
- ACCEPT only if the boat and the headline sit in the same relationship to each other as in the supplied banner.
- REJECT if the headline's letters have changed shape, spacing or spelling.
- REJECT if the added sky or water shows a visible seam, a repeated tile, a horizon that does not line up, or a second boat.
- Deterministic pre-checks that count as rejects (E5): format probe (container/aspect/resolution/duration/audio-track); baked-text scan on no-text items; duration or aspect mismatch against `delivery`.

## Routes

Routes, arms, tranches and billing quantities are in `TEST-CASES.yaml` → this case's `routes[]` (route facts in `route_catalogue`): flux-2-pro-edit, gpt-image-2-edit, nano-banana-pro-edit, seedream-5-pro-edit.

**Blueprint:** `BLUEPRINTS/IMG-EXT-01.blueprint.md` (sha256 `0eb6ca1595e63510…`, author executor_agent)

## Why this shape is real demand

RX-07 is a Kochi travel agency that needs its landscape banner as a 9:16 Story without cropping the boat or the headline. Reformatting one asset for every placement is the most common 'small job' Indian agencies receive, and the customer asked to extend, not to crop.
