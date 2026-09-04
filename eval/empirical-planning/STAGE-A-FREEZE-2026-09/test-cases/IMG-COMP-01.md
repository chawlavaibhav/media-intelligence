# IMG-COMP-01 — IMG lane, hg (whatsapp)

## The request, as the customer sent it

**Channel:** whatsapp · **Language:** hg · **Attachments named:** model_portrait.jpg, shade_ruby_pack.jpg

> Do photos bhej raha hoon - ek model ka portrait (model_portrait.jpg) aur doosra hamare lipstick ka packshot (shade_ruby_pack.jpg). Dono ko ek creative mein combine karna hai, model haath mein product pakde hue dikhe. Model ka face bilkul same rehna chahiye aur pack ka shade bhi exactly same, wo hamara signature colour hai. Upar likha ho "नया शेड, वही भरोसा". Instagram post, 4:5.

**Source:** pool `rx`, id `RX-08`

**Adaptations:**

- attachments_named
- aspect_stated_4_5

## Normalized Request (CANON-010 grammar)

| field | value | provenance |
|---|---|---|
| requested_operation | compose | customer_stated |
| modality | static_image | customer_stated |
| supplied_assets | [{applies_to: model, asset_id: model_portrait, description: portrait of a model, media_type: image, role: identity_reference}, {applies_to: lipstick_pack, asset_id: shade_ruby_pack, description: packshot of a lipstick in the signature shade, media_type: image, role: identity_reference}] | customer_stated |
| mutation_intents | {intents: [{detail: 'customer named this: ''face bilkul same''', intent: preserve, target: model facial identity}, {detail: 'signature colour, customer named this', intent: preserve, target: product shade}, {detail: model holds the product, intent: add, target: holding relationship}], preservation_default: implicit_everything_not_named} | customer_stated |
| deliverable_set | {acceptance_basis: per_deliverable, cardinality: 1, variation_axis: none} | — |
| entities | [{allowed_variation: {background: true, pose: true}, entity_id: model, entity_type: person, identity_invariants: [face identical to the supplied portrait], role: hero}, {allowed_variation: {}, entity_id: lipstick_pack, entity_type: product, identity_invariants: [shade exactly as supplied, pack form], role: hero}] | customer_stated |
| relationships | [{object: lipstick_pack, relation: holds, subject: model}] | customer_stated |
| text_requirements | [{content: 'नया शेड, वही भरोसा', exactness: exact, role: headline, script: devanagari, text_id: h1}] | customer_stated |
| brand_requirements | {assets: [shade_ruby_pack], mandatories: [], palette: {signature_shade: as supplied packshot}, palette_tolerance: visually identical when flicked against the packshot, prohibitions: []} | customer_stated |
| language_topology | {on_screen_copy: hi (Devanagari), spoken: none, subtitles: none, viewer_locale: hi-en-IN} | customer_stated |
| speaker_topology | — (absent) | absent |
| temporal_structure | — (absent) | absent |
| subject_motion | — (absent) | absent |
| camera_motion | — (absent) | absent |
| delivery | {aspect_ratios: ['4:5'], platform: instagram, resolution: ~1 MP, safe_areas: []} | — |
| ambiguity_markers | — (absent) | absent |
| acceptance_intent | {free_choices: [background, pose beyond holding], hard_constraints: [face identical, shade identical, holding relationship, exact Devanagari headline], soft_preferences: [natural hand contact], stated_rejection_criteria: [], stated_success_criteria: [same face, same shade, holding the product, headline exact]} | customer_stated |

`product_or_packshot_present`: True · primary capability `person_identity`

## Acceptance contract (judged blind, from the artifact alone)

- ACCEPT only if the face in the result is the same person as in the supplied portrait when the two are shown side by side with two decoy portraits (the judge must pick the supplied portrait as the match).
- ACCEPT only if the lipstick's shade matches the supplied packshot and not either decoy shade.
- ACCEPT only if the model's hand visibly holds the pack — fingers wrap it, the pack does not float or pass through the hand.
- ACCEPT only if the headline reads exactly "नया शेड, वही भरोसा" with every matra correct (composited at USD 0 on the accepted draw; judged on the final).
- REJECT if a second person, a second product or any other lettering appears.
- Deterministic pre-checks that count as rejects (E5): format probe (container/aspect/resolution/duration/audio-track); baked-text scan on no-text items; duration or aspect mismatch against `delivery`.

## Routes

Routes, arms, tranches and billing quantities are in `TEST-CASES.yaml` → this case's `routes[]` (route facts in `route_catalogue`): flux-2-pro-edit, gpt-image-2-edit, nano-banana-pro-edit, seedream-5-pro-edit.

**Blueprint:** `BLUEPRINTS/IMG-COMP-01.blueprint.md` (sha256 `43973582de2e94fa…`, author executor_agent)

## Why this shape is real demand

RX-08 is a Delhi cosmetics brand sending a model portrait and a lipstick packshot to be combined, with the face and the signature shade held exactly and a Devanagari headline on top — two identity references and a new relationship in one creative, written in Hinglish with Devanagari copy, which is how such brands actually write.
