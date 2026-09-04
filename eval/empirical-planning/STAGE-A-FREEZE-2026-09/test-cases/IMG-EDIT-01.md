# IMG-EDIT-01 — IMG lane, en (email)

## The request, as the customer sent it

**Channel:** email · **Language:** en · **Attachments named:** showroom_sofa_01.jpg

> Hi, we shot this sofa in our showroom (attached: showroom_sofa_01.jpg) but one of our staff is standing in the background on the left. Can you take him out? Everything else should stay exactly as it is, same sofa, same room, same light. It goes on the product page tomorrow morning so we need it back today. Thanks, Meera

**Source:** pool `rx`, id `RX-01`

**Adaptations:**

- attachment_named
- register_rewritten_to_email (sign-off added)

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | edit | customer_stated |
| modality | static_image | customer_stated |
| supplied_assets | [{applies_to: sofa_photo, asset_id: showroom_sofa_01, description: showroom photograph containing the sofa and an unintended person at the left background, media_type: image, role: subject_of_operation}] | customer_stated |
| mutation_intents | {intents: [{detail: must not appear, intent: remove, target: staff member in left background}], preservation_default: implicit_everything_not_named} | customer_stated |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | [{allowed_variation: {}, entity_id: sofa, entity_type: product, identity_invariants: [shape, colour, position, lighting], role: hero}, {entity_id: staff_member, entity_type: person, role: absent}] | customer_stated |
| relationships | — (absent) | absent |
| text_requirements | — (absent) | absent |
| brand_requirements | — (absent) | absent |
| language_topology | {on_screen_copy: none, spoken: none, subtitles: none, viewer_locale: en-IN} | — |
| speaker_topology | — (absent) | absent |
| temporal_structure | — (absent) | absent |
| subject_motion | — (absent) | absent |
| camera_motion | — (absent) | absent |
| delivery | {aspect_ratios: [as supplied], platform: product page, resolution: as supplied, safe_areas: []} | customer_implied |
| ambiguity_markers | — (absent) | absent |
| acceptance_intent | {free_choices: [how the vacated area is filled], hard_constraints: [no person in the result, 'sofa unchanged in shape, colour, position', room and light unchanged], soft_preferences: [], stated_rejection_criteria: ['sofa, room or light changed'], stated_success_criteria: [the person is gone, everything else unchanged]} | customer_stated |

`product_or_packshot_present`: True · primary capability `edit_preservation`

## Acceptance contract (judged blind, from the artifact alone)

- REJECT if any person, or part of a person, remains anywhere in the image.
- ACCEPT only if the sofa is the same object — same outline, same colour, same position in frame — when the result is flicked against the supplied photo.
- REJECT if the vacated area shows a smudge, a repeated texture patch, a colour seam or an object that was not in the original.
- REJECT if the lighting direction or overall brightness of the room has changed.

### E5 pre-checks (code, not shown to the judge)

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

## Routes

See `TEST-CASES.yaml` → `routes[]`: flux-2-pro-edit, gpt-image-2-edit, nano-banana-pro-edit, seedream-5-pro-edit.

**Blueprint:** `BLUEPRINTS/IMG-EDIT-01.blueprint.md` (sha256 `f2d9536595fddb8e…`, author executor_agent)

## Why this shape is real demand

RX-01 is a Bengaluru furniture retailer asking to remove a staff member from a showroom photo before it goes on the product page tomorrow — the defining single-removal edit where the customer names nothing to keep because everything is implicitly preserved. Retailers send this to designers daily.
