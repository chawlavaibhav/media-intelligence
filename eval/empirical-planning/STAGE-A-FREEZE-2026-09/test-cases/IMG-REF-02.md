# IMG-REF-02 — IMG lane, en (email)

## The request, as the customer sent it

**Channel:** email · **Language:** en · **Attachments named:** host_ref_1.jpg, host_ref_2.jpg, host_ref_3.jpg

> Hi, we run a social channel with a recurring host, she is a real person and has to look the same in every creative. Sharing 3 photos of her (host_ref_1.jpg, host_ref_2.jpg, host_ref_3.jpg). Need one new still: her at a cafe table, laptop open, smiling at the camera, morning light. Same face, same hair, same build, that is non-negotiable. A casual outfit is fine, it does not have to match the photos. No text on the image. 4:5 for Instagram. Thanks, Nikhil

**Source:** pool `marketplace`, id `MKT-009`

**Adaptations:**

- buyer_localised_to_India (a Bengaluru content studio; the source is a UK Upwork buyer — the demand shape, a recurring established character, is kept)
- deliverable_set_to_one_still (the source's video output is served by VID-REF-02; this case is the still)
- scene_stated_by_customer (cafe, laptop, morning) — the source names no scene; the fixture element is the scene, labelled
- identity_invariants_as_in_the_bank's fixture (face, hair, build)
- reference_count_set_to_3
- aspect_stated_4_5

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | generate | customer_stated |
| modality | static_image | customer_stated |
| supplied_assets | [{applies_to: host, asset_id: host_ref_1, description: reference photo 1 of the host, media_type: image, role: identity_reference}, {applies_to: host, asset_id: host_ref_2, description: reference photo 2 of the host, media_type: image, role: identity_reference}, {applies_to: host, asset_id: host_ref_3, description: reference photo 3 of the host, media_type: image, role: identity_reference}] | customer_stated |
| mutation_intents | — (absent) | absent |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | [{allowed_variation: {pose: true, wardrobe: true}, entity_id: host, entity_type: person, identity_invariants: [face, hair, build], role: hero}, {entity_id: laptop, entity_type: object, identity_invariants: ['open laptop, screen not readable'], role: supporting}] | customer_stated |
| relationships | [{object: laptop, relation: sits_at_table_with, subject: host}] | customer_stated |
| text_requirements | — (absent) | absent |
| brand_requirements | — (absent) | absent |
| language_topology | {on_screen_copy: none, spoken: none, subtitles: none, viewer_locale: en-IN} | customer_implied |
| speaker_topology | — (absent) | absent |
| temporal_structure | — (absent) | absent |
| subject_motion | — (absent) | absent |
| camera_motion | — (absent) | absent |
| delivery | {aspect_ratios: ['4:5'], platform: instagram, resolution: ~1 MP, safe_areas: []} | — |
| ambiguity_markers | — (absent) | absent |
| acceptance_intent | {free_choices: [outfit, cafe details], hard_constraints: [identity from references, no text], soft_preferences: [casual outfit], stated_rejection_criteria: [any text], stated_success_criteria: ['same face, hair, build', 'cafe, laptop, smiling, morning light']} | customer_stated |

`product_or_packshot_present`: False · primary capability `person_identity`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if, shown the result beside the three references and the two decoy sets, the judge identifies the referenced person as the match (same face, same hair, same build).
- ACCEPT only if she sits at a cafe table with an open laptop whose screen shows nothing readable, smiling toward the camera.
- REJECT if any lettering, logo or numeral appears (including cafe signage or the laptop lid).
- REJECT if hands or face show anatomical faults (extra fingers, doubled features).
- Deterministic pre-checks that count as rejects (E5): format probe (container/aspect/resolution/duration/audio-track); baked-text scan on no-text items; duration or aspect mismatch against `delivery`.

## Routes

Routes, arms, tranches and billing quantities are in `TEST-CASES.yaml` → this case's `routes[]` (route facts in `route_catalogue`): flux-2-pro-edit, gpt-image-2-edit, nano-banana-pro-edit, seedream-5-pro-edit.

**Blueprint:** `BLUEPRINTS/IMG-REF-02.blueprint.md` (sha256 `aef93422cdef6fa6…`, author executor_agent)

## Why this shape is real demand

MKT-009 is an Upwork buyer with a recurring female character who 'must be maintained across all output' — the posting drew 50+ proposals, the strongest demand signal in the marketplace bank. Localised to a Bengaluru content studio with a real recurring host, the still is the first asset such a studio orders.
