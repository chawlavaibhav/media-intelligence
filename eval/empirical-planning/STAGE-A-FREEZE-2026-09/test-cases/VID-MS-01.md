# VID-MS-01 — VID lane, hg (whatsapp)

## The request, as the customer sent it

**Channel:** whatsapp · **Language:** hg · **Attachments named:** none

> 15 second ka multi-shot video chahiye, Reels ke liye vertical. Do friends (20s mein, ek ladka ek ladki) ghar pe phone pe trip plan kar rahe hain, phir airport pe bag lekar bhaagte hue, phir beach pe pahunch gaye. 3-4 shots, dono log har shot mein same dikhne chahiye. Young aur fun vibe. Aircraft agar dikhe toh generic rakhna, koi logo ya livery nahi. VO aur end card hum khud daalenge, sirf visuals aur ambient sound. Koi text nahi.

**Source:** pool `brief_bank`, id `BR-F10-HG`

**Adaptations:**

- vo_and_end_card_dropped_customer_adds_in_post ("Plan kam, travel zyada" VO and "फ्लाइट्स ₹1,499 से" end card removed)
- livery_dropped_no_brand_asset (source: 'livery hamari exact honi chahiye' — no livery asset can be supplied; customer asks for a generic aircraft)
- shot_count_stated_3_4 (source underspecified)
- genders_stated (one man, one woman) so identity continuity is judgeable
- aspect_stated_9_16

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | generate | customer_stated |
| modality | video | customer_stated |
| supplied_assets | — (absent) | absent |
| mutation_intents | — (absent) | absent |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | [{entity_id: friend_m, entity_type: person, identity_invariants: ['man, 20s', same in every shot], role: hero}, {entity_id: friend_f, entity_type: person, identity_invariants: ['woman, 20s', same in every shot], role: hero}, {entity_id: aircraft, entity_type: object, identity_invariants: ['generic, no livery'], role: background}] | customer_stated |
| relationships | [{object: friend_f, relation: travels_with, subject: friend_m}] | customer_stated |
| text_requirements | — (absent) | absent |
| brand_requirements | {assets: [], mandatories: [], palette: {}, palette_tolerance: '', prohibitions: [no logo or livery]} | customer_stated |
| language_topology | {on_screen_copy: none, spoken: none, subtitles: none, viewer_locale: hi-en-IN} | customer_stated |
| speaker_topology | {offscreen_voices: 0, script_exactness: free, turn_boundaries_required: false, visible_speakers: 0} | — |
| temporal_structure | {beats: [{beat: 1, content: planning at home on a phone}, {beat: 2, content: running through the airport with bags}, {beat: 3, content: arriving at the beach}], continuity_requirements: [both identities constant across shots], duration_seconds: 15, shot_count: 3–4} | customer_stated |
| subject_motion | {description: run through the airport; walk onto the beach, entity_ref: 'friend_m, friend_f', motion_type: locomotion} | customer_stated |
| camera_motion | {description: delegated; blueprint chooses one motivated move at the beach and stillness elsewhere, motion_type: static} | system_derived — delegated (CA-D11) |
| delivery | {aspect_ratios: ['9:16'], platform: instagram reels, resolution: 720p, safe_areas: []} | — |
| ambiguity_markers | [{affected_fields: [R06], detail: destination beach unnamed (source); free choice, marker_type: underspecification}] | — |
| acceptance_intent | {free_choices: [beach, wardrobe], hard_constraints: [15 s, 'multi-shot: home → airport → beach', identity continuity, 'no text, no VO'], soft_preferences: [fun vibe], stated_rejection_criteria: [logo or livery, text], stated_success_criteria: [3–4 shots, same two people in every shot, 'young, fun']} | customer_stated |

`product_or_packshot_present`: False · primary capability `multi_shot_spatial_continuity`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if the clip contains at least three distinct shots (visible cuts) showing, in order, a home scene with a phone, an airport with the pair running with bags, and a beach.
- ACCEPT only if the same man and the same woman appear in every shot — same faces, same hair — when paused on one frame per shot.
- REJECT if any logo, airline livery or lettering appears (aircraft must be plain).
- REJECT if a shot is shorter than one second or the total runs under 13 s or over 17 s.
- REJECT if any speech or music is present.
- Deterministic pre-checks that count as rejects (E5): format probe (container/aspect/resolution/duration/audio-track); baked-text scan on no-text items; duration or aspect mismatch against `delivery`.

## Routes

Routes, arms, tranches and billing quantities are in `TEST-CASES.yaml` → this case's `routes[]` (route facts in `route_catalogue`): gemini-omni-1.1-flash-long, kling-v3-pro-15s, seedance-2.5-15s, veo-3.1-fast-extend.

**Blueprint:** `BLUEPRINTS/VID-MS-01.blueprint.md` (sha256 `a731d6c6f16cfa8e…`, author executor_agent)

## Why this shape is real demand

BR-F10-HG is a Mumbai budget airline's 15-second multi-shot Reel — two friends planning, running through the airport, arriving — written in Hinglish. With VO and end card handled by the customer's editor and the livery constraint dropped (no asset), it is the §C.3d 15-second item on a real buyer's brief.
