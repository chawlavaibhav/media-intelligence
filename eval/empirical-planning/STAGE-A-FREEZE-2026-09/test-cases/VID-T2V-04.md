# VID-T2V-04 — VID lane, en (whatsapp)

## The request, as the customer sent it

**Channel:** whatsapp · **Language:** en · **Attachments named:** none

> Following up on the bottle shot - now we want a 6 sec cinematic product ad for the same 250ml cold pressed orange juice bottle, vertical for Reels. Think: bottle standing on a wet dark slate surface, condensation on the glass, morning light coming in from one side, slow reveal, a couple of orange slices next to it. Product only, no people, no hands. Ambient sound is fine, no VO, no music. No text anywhere - leave the label blank like the still, we add label and copy in post.

**Source:** pool `marketplace`, id `MKT-012`; secondary `brief_bank:BR-F02-EN`

**Adaptations:**

- product_taken_from_BR-F02-EN (MKT-012 names no product; the juice bottle of IMG-CORE-01 is used so the customer is the same buyer — cited as a second source)
- duration_set_to_6s (source 10–20 s)
- buyer_localised_to_India (Mumbai juice brand)
- text_and_label_dropped_for_the_no-lettering_video_core
- aspect_stated_9_16

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | generate | customer_stated |
| modality | video | customer_stated |
| supplied_assets | — (absent) | absent |
| mutation_intents | — (absent) | absent |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | [{allowed_variation: {angle: true}, entity_id: juice_bottle, entity_type: product, identity_invariants: [250 ml glass bottle, blank label, orange juice], role: hero}, {entity_id: orange_slices, entity_type: object, identity_invariants: [a couple of slices], role: supporting}] | customer_stated |
| relationships | [{object: juice_bottle, relation: beside, subject: orange_slices}] | customer_stated |
| text_requirements | — (absent) | absent |
| brand_requirements | — (absent) | absent |
| language_topology | {on_screen_copy: none, spoken: none, subtitles: none, viewer_locale: en-IN} | customer_stated |
| speaker_topology | {offscreen_voices: 0, script_exactness: free, turn_boundaries_required: false, visible_speakers: 0} | customer_stated |
| temporal_structure | {beats: [{beat: 1, content: slow reveal of the bottle}], continuity_requirements: [same bottle throughout], duration_seconds: 6, shot_count: 1} | customer_stated |
| subject_motion | — (absent) | absent |
| camera_motion | {description: '''slow reveal'' — customer-implied slow camera move', motion_type: dolly} | customer_implied ('slow reveal') |
| delivery | {aspect_ratios: ['9:16'], platform: instagram reels, resolution: 720p, safe_areas: []} | — |
| ambiguity_markers | — (absent) | absent |
| acceptance_intent | {free_choices: [reveal mechanics], hard_constraints: [product only, blank label, no text], soft_preferences: ['wet slate, orange slices'], stated_rejection_criteria: [people or hands, VO or music, text], stated_success_criteria: [cinematic, condensation, side light, slow reveal]} | customer_stated |

`product_or_packshot_present`: True · primary capability `product_stability_in_clip`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if one glass bottle of orange juice with a blank label is the subject for the whole clip and no hand, person or second bottle appears.
- ACCEPT only if the camera moves slowly (a reveal or drift) while the bottle itself stays still and keeps its shape; REJECT if the bottle warps, changes size or shifts on the surface.
- ACCEPT only if condensation droplets are visible on the glass at some point.
- REJECT if any voice, music or lettering is present.
- Deterministic pre-checks that count as rejects (E5): format probe (container/aspect/resolution/duration/audio-track); baked-text scan on no-text items; duration or aspect mismatch against `delivery`.

## Routes

Routes, arms, tranches and billing quantities are in `TEST-CASES.yaml` → this case's `routes[]` (route facts in `route_catalogue`): gemini-omni-1.1-flash, kling-v3-pro-audio, minimax-h3-max, sora-2, veo-3.1-fast, wan-3.0-prime.

**Blueprint:** `BLUEPRINTS/VID-T2V-04.blueprint.md` (sha256 `a837b8d563c4dc59…`, author executor_agent)

## Why this shape is real demand

MKT-012 is an Upwork buyer paying USD 80 fixed for a short cinematic product ad; the product is the same juice bottle as IMG-CORE-01 (BR-F02-EN), so the buyer is the same Mumbai brand following up its still with a 6-second Reels ad. 'Cinematic product ad' is the most-posted paid video shape in the marketplace research.
