# IMG-CORE-02 — IMG lane, hg (whatsapp)

## The request, as the customer sent it

**Channel:** whatsapp · **Language:** hg · **Attachments named:** none

> Bhai ek creative chahiye Instagram ke liye. Young professional, ladka, 25-28 type, phone haath mein, metro ya office lobby type setting, smart casual. Trustworthy lagna chahiye bank jaisa serious but boring nahi, Gen Z audience hai, thoda fun bhi. Phone ki screen pe kuch mat dikhana, hum apna app screenshot khud lagayenge. Aur koi text mat daalna, headline aur CTA design team baad mein add karegi. Portrait 4:5.

**Source:** pool `brief_bank`, id `BR-F03-HG`

**Adaptations:**

- text_requirement_dropped_for_core ("Ab investing हुआ आसान" and "Download karo" removed; customer states design team adds copy later)
- app_screenshot_deferred_to_customer_overlay (screen left blank; the source's supplied UI asset is not used so no lettering appears)
- gender_and_age_stated (ladka, 25–28) so the same still can serve VID-I2V-02/03 and the male-voice lipsync drives
- register_kept_whatsapp

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | generate | customer_stated |
| modality | static_image | customer_stated |
| supplied_assets | — (absent) | absent |
| mutation_intents | — (absent) | absent |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | [{allowed_variation: {face: true, wardrobe_within_smart_casual: true}, entity_id: young_professional, entity_type: person, identity_invariants: [male, 25–28, smart casual], role: hero}, {allowed_variation: {model: true}, entity_id: phone, entity_type: object, identity_invariants: [screen blank / not readable], role: supporting}] | customer_stated |
| relationships | [{object: phone, relation: holds, subject: young_professional}] | customer_stated |
| text_requirements | — (absent) | absent |
| brand_requirements | — (absent) | absent |
| language_topology | {on_screen_copy: none, spoken: none, subtitles: none, viewer_locale: hi-en-IN} | customer_implied |
| speaker_topology | — (absent) | absent |
| temporal_structure | — (absent) | absent |
| subject_motion | — (absent) | absent |
| camera_motion | — (absent) | absent |
| delivery | {aspect_ratios: ['4:5'], platform: instagram, resolution: ~1 MP, safe_areas: []} | — |
| ambiguity_markers | [{affected_fields: [R18], detail: '''bank jaisa serious'' and ''Gen Z, thoda fun'' are opposed register instructions (source c1); recorded, resolved in the blueprint by keeping trust in light and posture and ''fun'' in expression only', marker_type: contradiction}] | system_derived (flagged, not resolved silently) |
| acceptance_intent | {free_choices: [exact location, wardrobe colours], hard_constraints: [one young man holding a phone, phone screen blank, no text], soft_preferences: [metro or office-lobby setting, smart casual], stated_rejection_criteria: [anything on the phone screen, any text], stated_success_criteria: ['trustworthy, bank-like', 'not boring, fun for Gen Z']} | customer_stated |

`product_or_packshot_present`: False · primary capability `composition_brand_register`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if exactly one adult man, plausibly 25–28, is in frame holding a phone with a visible hand.
- ACCEPT only if the phone screen shows no readable content — blank, dark or plain glow.
- REJECT if any lettering, logo or numeral appears anywhere in the image (including signage in the background).
- REJECT if the hand holding the phone has the wrong number of fingers, a bent-through joint, or fingers passing through the phone.
- ACCEPT only if the face is fully formed (two eyes, natural mouth, no doubled features) and the expression reads as a relaxed smile rather than a blank stare.
- Deterministic pre-checks that count as rejects (E5): format probe (container/aspect/resolution/duration/audio-track); baked-text scan on no-text items; duration or aspect mismatch against `delivery`.

## Routes

Routes, arms, tranches and billing quantities are in `TEST-CASES.yaml` → this case's `routes[]` (route facts in `route_catalogue`): flux-2-pro, gpt-image-2, mai-image-2.6, nano-banana-2, nano-banana-pro, qwen-image-3, sd3.5-large, seedream-5-pro.

**Blueprint:** `BLUEPRINTS/IMG-CORE-02.blueprint.md` (sha256 `9846d024ac29a6cd…`, author executor_agent)

## Why this shape is real demand

BR-F03-HG is a Gurugram fintech asking for a young professional with a phone, trustworthy 'like a bank' yet fun for Gen Z — the register tension the bank planted deliberately. Dropping the headline and the app screenshot ('design team baad mein add karegi') is the ordinary way an Indian marketing team briefs a base creative before copy is signed off.
