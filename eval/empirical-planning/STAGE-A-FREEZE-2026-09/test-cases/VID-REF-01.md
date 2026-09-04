# VID-REF-01 — VID lane, en (email)

## The request, as the customer sent it

**Channel:** email · **Language:** en · **Attachments named:** pack_front.jpg, pack_side.jpg, pack_angle.jpg

> Hi, we want a 6 second product video for Amazon and Instagram made from our product photos - attaching 3 pics of the pack (pack_front.jpg, pack_side.jpg, pack_angle.jpg). The pack in the video has to be exactly ours, same shape, same colours, same label, please don't reinvent it. Camera can move however looks good, product turning slowly on a plain surface is fine. No text, no voice-over. 9:16 please. Regards, Sameer

**Source:** pool `marketplace`, id `MKT-014`

**Adaptations:**

- buyer_localised_to_India (a Jaipur D2C brand; the source is a USD 10 fixed Upwork posting for 'an AI video ad, produced from images')
- operation_read_as_generate_with_identity_references rather than animate: the customer supplies three reference photos and asks for a new video of the product, not motion added to one photo (MKT-014's own reading is animate from one image; here three references and a free camera make it reference-conditioned generate — recorded)
- duration_set_to_6s
- reference_count_set_to_3
- text_and_vo_dropped (customer states)
- aspect_stated_9_16

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | generate | customer_stated |
| modality | video | customer_stated |
| supplied_assets | [{applies_to: pack, asset_id: pack_front, description: front view of the pack, media_type: image, role: identity_reference}, {applies_to: pack, asset_id: pack_side, description: side view, media_type: image, role: identity_reference}, {applies_to: pack, asset_id: pack_angle, description: three-quarter view, media_type: image, role: identity_reference}] | customer_stated |
| mutation_intents | — (absent) | absent |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | [{allowed_variation: {angle: true}, entity_id: pack, entity_type: product, identity_invariants: [shape, colours, label as on references], role: hero}] | customer_stated |
| relationships | — (absent) | absent |
| text_requirements | — (absent) | absent |
| brand_requirements | {assets: [pack_front, pack_side, pack_angle], mandatories: [], palette: {pack_colours: as references}, palette_tolerance: visually identical when flicked, prohibitions: [no reinvention]} | customer_stated |
| language_topology | {on_screen_copy: as printed on the references, spoken: none, subtitles: none, viewer_locale: en-IN} | customer_stated |
| speaker_topology | {offscreen_voices: 0, script_exactness: free, turn_boundaries_required: false, visible_speakers: 0} | — |
| temporal_structure | {beats: [{beat: 1, content: product turns slowly on a plain surface}], continuity_requirements: [pack identity constant], duration_seconds: 6, shot_count: 1} | customer_stated |
| subject_motion | {description: turns slowly, entity_ref: pack, motion_type: object_motion} | customer_stated |
| camera_motion | {description: customer delegated ('however looks good'); blueprint chooses a still camera and lets the product turn, motion_type: static} | system_derived — delegated; still camera (CA-D11) |
| delivery | {aspect_ratios: ['9:16'], platform: amazon + instagram, resolution: 720p, safe_areas: []} | customer_stated |
| ambiguity_markers | — (absent) | absent |
| acceptance_intent | {free_choices: [camera, lighting], hard_constraints: [identity from references, no text, no VO], soft_preferences: [plain surface], stated_rejection_criteria: [reinvented pack, text, VO], stated_success_criteria: [exactly our pack, turning slowly]} | customer_stated |

`product_or_packshot_present`: True · primary capability `product_identity`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if the pack in the clip is the referenced pack and not either decoy, judged on a paused mid-clip frame beside the references and decoys.
- ACCEPT only if the pack's label stays as printed on the references in every sampled frame (start, middle, end); REJECT if lettering morphs, blurs into new shapes or re-arranges.
- ACCEPT only if the pack visibly turns or the viewpoint visibly changes during the clip.
- REJECT if the pack's proportions or colours change during the clip, or if any added lettering, voice or music is present.
- Deterministic pre-checks that count as rejects (E5): format probe (container/aspect/resolution/duration/audio-track); baked-text scan on no-text items; duration or aspect mismatch against `delivery`.

## Routes

Routes, arms, tranches and billing quantities are in `TEST-CASES.yaml` → this case's `routes[]` (route facts in `route_catalogue`): kling-v3-elements, seedance-2.5-ref2v, veo-3.1-fast-ref2v.

**Blueprint:** `BLUEPRINTS/VID-REF-01.blueprint.md` (sha256 `fbee0f74bc6ca394…`, author executor_agent)

## Why this shape is real demand

MKT-014 is an Upwork buyer paying USD 10 fixed for 'an AI video ad, produced from images' — the marketplace's clearest statement that buyers expect product video to come from their own photos. Localised to a Jaipur D2C brand sending three photos of its pack, with the tin reference pack shared with IMG-REF-01.
