# FINAL_PRODUCTION_PACKAGE

## DELIVERABLE

One textless plate deliverable, 9:16 aspect ratio, resolution class 1K-class.

## OBJECTIVE_INTERPRETATION

The plan's objective, verbatim: A spec film that makes Cumin Co.'s founders (ex-Meta / ex-Zomato growth) see that their own blog content converts into a warm, product-led launch film for the new Ramen Bowl in days — a launch-cadence capacity demonstration, never a quality critique (Controller hand-check 14 Sep: ~270 active premium ads).
Interpretation beyond the plan's words: none added by the operator.

## CORE_CREATIVE_IDEA

'Bottom stick, still.' Noodle night at a warm kitchen table: he fumbles a pair of chopsticks over a steaming Kairi bowl, she shows him with her hands over her Rosé bowl — three quiet macro beats that are the brand's own guide, verbatim — he fails anyway, and they eat happily regardless, her chopsticks resting in the bowl's rim notch. The lesson is the brand's blog; the warmth is the brand's register; the bowl demonstrates its own feature without a line of copy.

## MESSAGE_AND_INFORMATION_HIERARCHY

- Primary message: The bottom one doesn't move — and Cumin Co. is the bowl on a noodle night.
- Exact copy (composited by code onto the textless plate, never drawn by the model): The bottom stick stays still.; The top stick does all the work.; Pinch and release.; Ramen night at home.; Cumin Co.
- Read order: see the attention_order subfield below.

## VISUAL_SYSTEM

surface_finish_per_key_object: ceramic bowl glaze glossy (one large soft window reflection); ceramic body, noodles, wood, linen, skin and cloth matte; no other gloss.
implied_light_source: one soft window, camera-left, late afternoon; soft shadow edges; no second source.
placement_zone: bowl and hands in the lower two-thirds because the hands work above the bowl and the copy zone must stay clear; upper third empty wall; declared balanced (bowl mass low, hand mass centre, copy zone upper); no named ratio.
attention_order: 1st read the hand and chopsticks (motion / the only action), 2nd read the bowl (the only saturated colour), 3rd read the code-set line that lands after the action settles.

## PRODUCTION_RECIPE

- Exact-text mechanism: deterministic_text_composition (code sets every string onto the plate or the clip frames after the draw).
- Dispatched prompt: the prompt below; no other prompt is sent for this asset.

## GENERATION_PROMPTS

Dispatched prompt, the textless plate (the text mechanism is deterministic code composition, so this is the only prompt sent):
"Vertical photograph, close on a young Indian woman's right hand holding a pair of dark acacia wood chopsticks, the chopsticks from the second reference photograph, above a bowl of ramen; the camera is low and slightly to the thumb side of the hand so the web of the thumb and the curled ring finger under the lower chopstick are clearly visible. The bowl is the ceramic bowl from the first reference photograph, exactly the same shape and size, but in the soft rosé pink glaze of the second reference photograph: gently flared wall, thick rounded rim, a small moulded notch cut into the rim on the near side, glossy glaze over matte-looking ceramic. The bowl sits on warm oat-coloured linen on a light wood table, filled with amber broth, wheat noodles, a halved egg and spring onion, faint steam. The grip is shown precisely and calmly: the lower chopstick rests in the web between the thumb and index finger and lies along the base of the ring finger, which curls gently under it to support it; the upper chopstick is held like a pencil between the tips of the thumb, index and middle finger; the two tips are level and hover just above the noodles without touching. One hand only, five fingers, natural proportions, short clean nails, a plain oatmeal knit sleeve at the wrist. One soft window light from camera-left, late afternoon, soft shadow edges, one large soft window reflection on the glaze. The bowl and hand sit in the lower two-thirds of the frame; the upper third is plain soft-focus warm off-white wall, empty. Warm, calm, domestic, photographic, shallow depth of field. No text, no lettering, no logos, no printed matter anywhere in the image."

## DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

Code composes these exact strings after the draw; the model never renders this copy:
- string 1 (script latin, placement overlay, may_reflow false): The bottom stick stays still.
- string 2 (script latin, placement overlay, may_reflow false): The top stick does all the work.
- string 3 (script latin, placement overlay, may_reflow false): Pinch and release.
- string 4 (script latin, placement overlay, may_reflow false): Ramen night at home.
- string 5 (script latin, placement overlay, may_reflow false): Cumin Co.
Deterministic checks run by code: check_text_bounds, check_contrast, check_fit, check_geometry, check_disjoint, frame_hygiene.

## FAILURE_PREVENTION

Gate requirements the plan names:
- LIMIT-TEXT: no text-bearing surface and no rendered text requested in any prompt.
- delivered-vs-declared aspect 9:16.

## HARD_CONSTRAINT_CHECK

The plan's hard constraints, verbatim:
- the bowl is the brand's own bowl, geometry and glaze from the reference photographs
- no text, lettering, logos or printed matter in any generated image or frame
- no health, safety, patent, performance or financial claim anywhere
- the Kairi (Mint) and Rosé colourways only
