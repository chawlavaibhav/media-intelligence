# VID-I2V-03 — VID lane, hg (whatsapp)

## The request, as the customer sent it

**Channel:** whatsapp · **Language:** hg · **Attachments named:** phone_creative_final.png

> Same photo (phone_creative_final.png) se ek 6 second ka fast wala clip chahiye Reels ke liye. Wo phone pe kuch dekhta hai, ekdum excited ho jaata hai, jhatke se seedha khada hota hai aur dono haath upar karke celebrate karta hai, thoda uchhalta bhi hai. Camera thoda handheld, energetic. Fast aur snappy chahiye, boring nahi. Face same rahe jo photo mein hai. Koi text nahi, koi awaaz nahi chahiye.

**Source:** pool `brief_bank`, id `BR-F06-HG`

**Adaptations:**

- converted_to_animate_on_supplied_still (source is a 10-s three-beat text-to-video; here one high-motion beat on the customer's accepted IMG-CORE-02 still — the plate rule)
- narrative_compressed_to_one_high_motion_beat (need → order → arrival becomes 'sees, jumps up, celebrates')
- duration_set_to_6s
- end_card_dropped ('10 minute mein delivery' / 'Order करो अभी' removed)
- buyer_changed_to_the_plate_owner (fintech, Hinglish — the source's register)

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | animate | customer_stated |
| modality | video | customer_stated |
| supplied_assets | [{applies_to: young_professional, asset_id: phone_creative_final, description: the Controller-accepted IMG-CORE-02 draw, media_type: image, role: subject_of_operation}] | customer_stated |
| mutation_intents | {intents: [{detail: 'customer named this: ''face same rahe''', intent: preserve, target: facial identity}], preservation_default: implicit_everything_not_named} | customer_stated |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | [{entity_id: young_professional, entity_type: person, identity_invariants: [face as in the still], role: hero}] | customer_stated |
| relationships | — (absent) | absent |
| text_requirements | — (absent) | absent |
| brand_requirements | — (absent) | absent |
| language_topology | {on_screen_copy: none, spoken: none, subtitles: none, viewer_locale: hi-en-IN} | customer_stated |
| speaker_topology | {offscreen_voices: 0, script_exactness: free, turn_boundaries_required: false, visible_speakers: 0} | — |
| temporal_structure | {beats: [{beat: 1, content: sees something on the phone}, {beat: 2, content: 'jumps up, arms raised, celebrates'}], continuity_requirements: [face identical throughout], duration_seconds: 6, shot_count: 1} | customer_stated |
| subject_motion | {description: 'stands up sharply, raises both arms, small jump', entity_ref: young_professional, motion_type: locomotion} | customer_stated |
| camera_motion | {description: 'customer-stated: a little handheld, energetic', motion_type: handheld} | customer_stated |
| delivery | {aspect_ratios: ['4:5 (as the still)'], platform: instagram reels, resolution: 720p-class, safe_areas: []} | — |
| ambiguity_markers | — (absent) | absent |
| acceptance_intent | {free_choices: [exact timing], hard_constraints: [identity preserved, stands up and raises both arms, 'no text, no audio'], soft_preferences: [handheld], stated_rejection_criteria: [boring, face changes, text, audio], stated_success_criteria: ['fast, snappy', jumps up and celebrates, handheld feel]} | customer_stated |

`product_or_packshot_present`: False · primary capability `motion_action_quality`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if the man goes from his starting pose to standing tall with both arms raised within the clip.
- ACCEPT only if the face in the last second is recognisably the same person as in the first frame.
- REJECT if arms, hands or the phone multiply, stretch, pass through the body or vanish during the movement.
- REJECT if the clip is nearly static (a slight sway is not the requested celebration), or if any lettering or audio is present.

### E5 pre-checks (code, not shown to the judge)

- format probe vs `delivery` (container, aspect, resolution, duration, audio track)
- duration or aspect mismatch vs `delivery`
- baked-text scan (Cloud Vision, T-BENCH instrument as the E5 trigger): any lettering → reject
- refusal / error / empty artifact → reject

## Routes

See `TEST-CASES.yaml` → `routes[]`: kling-v3-pro-i2v, minimax-h3-max-i2v, seedance-2.5-i2v, veo-3.1-fast-i2v, wan-3.0-prime-i2v.

**Blueprint:** `BLUEPRINTS/VID-I2V-03.blueprint.md` (sha256 `84c9da1027b04d2a…`, author executor_agent)

## Why this shape is real demand

BR-F06-HG is a Mumbai quick-commerce app wanting a fast, snappy clip of a young man reacting and moving — three beats in ten seconds, the tightest compression in the bank. Compressed to one celebration beat on the customer's own accepted still, it is the 'make my photo move, but energetically' request Hinglish-speaking growth teams send.
