# VID-KNEE-01 — VID lane, en (whatsapp)

## The request, as the customer sent it

**Channel:** whatsapp · **Language:** en · **Attachments named:** none

> Following up on the bottle shot - now we want a 6 sec cinematic product ad for the same 250ml cold pressed orange juice bottle, vertical for Reels. Think: bottle standing on a wet dark slate surface, condensation on the glass, morning light coming in from one side, slow reveal, a couple of orange slices next to it. Product only, no people, no hands. Ambient sound is fine, no VO, no music. No text anywhere - leave the label blank like the still, we add label and copy in post.

**Source:** pool `marketplace`, id `MKT-012`; secondary `brief_bank:BR-F02-EN`

**Adaptations:**

- identical_request_to_VID-T2V-04 (the cost knee runs the same request on the Veo lite / Veo full / H3 Max 480p tiers; Veo fast and H3 Max 768p come from the core)

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

`product_or_packshot_present`: True · primary capability `cost_and_cpao`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if one glass bottle of orange juice with a blank label is the subject for the whole clip and no hand, person or second bottle appears.
- ACCEPT only if the camera moves slowly (a reveal or drift) while the bottle itself stays still and keeps its shape; REJECT if the bottle warps, changes size or shifts on the surface.
- ACCEPT only if condensation droplets are visible on the glass at some point.
- REJECT if any voice, music or lettering is present.

### E5 pre-checks (code, not shown to the judge)

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- duration or aspect mismatch vs `delivery`
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

## Routes

See `TEST-CASES.yaml` → `routes[]`: minimax-h3-max-480p, veo-3.1-full, veo-3.1-lite.

**Blueprint:** `BLUEPRINTS/VID-KNEE-01.blueprint.md` (sha256 `f6e8774ae8603379…`, author executor_agent)

## Why this shape is real demand

The same request as VID-T2V-04, run on the cheap and premium tiers so the Controller can see the price ladder on one real buyer's brief rather than on a benchmark prompt.
