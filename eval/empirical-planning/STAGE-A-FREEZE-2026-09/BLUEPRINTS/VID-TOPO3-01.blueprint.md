# Production blueprint — VID-TOPO3-01

```yaml
case_id: VID-TOPO3-01
author: executor_agent
blueprint_author: executor_agent
held_constant_across_routes: true
frozen: 2026-09-05
gate_pre: not_available_on_base — canon/gate/run_gate.py is absent from base cb92f1e (CANON-GATE-001 unmerged); run `pre` on this file when it lands
packs_source: canon/compilation/PACK-*-v0.yaml (corpus 3f7e3fadb3fb); triggers canon/packs/pack-triggers-v0.yaml; DEFAULT/CHECK text rendered by id, never paraphrased; no HOLD material
```

## 1. packs_selected (deterministic lookup from the Normalized Request; `compiled` = injected by id, `uncompiled` = listed only, no doctrine drawn)

- `concept_and_distinctiveness` — uncompiled — universal
- `critique_and_effectiveness` — uncompiled — universal
- `composition_and_attention` — compiled — base:video (R05)
- `colour_and_visual_register` — uncompiled — base:video (R05)
- `camera_and_spatial_grammar` — uncompiled — base:video (R05)
- `editing_pacing_and_short_form` — uncompiled — base:video (R05)
- `typography_and_copy` — uncompiled — text_requirements_nonempty (R08)
- `product_appearance` — compiled — product_or_packshot_entity_present (R06)
- `indian_indic_context` — uncompiled — language_topology_present_or_market_IN (R10; market IN for every case)
- `commercial_communication` — uncompiled — advertising_acceptance_intent (R18)

## 2. decisions (by id; DEFAULT = the pack's text; CASE VALUE = this case's filled value)

### PA-D1 — What reflection type dominates each key product surface — diffuse (matte), direct (glossy), or glare?

- **DEFAULT (product_appearance):** Declare a finish per named object before any prompt is written and light for the declared finish; the three reflection types are a contrast set (scs_lsm_c003_001) — finish is a property of the surface, not of the light.
- **CASE VALUE:** As IMG-TEXT-01: sweet box matte card with a glossy foil band; diyas matte clay; flames the only hard sources.

### PA-D4 — What is the fictional light source, and does everything agree with it?

- **DEFAULT (product_appearance):** Name the fictional source first, then place the key to agree with it (sk_alt_c003_0011); build in the working order of scs_alt_c003_002 — one source photographs flat, added lights restore roundness (sk_alt_c003_0009), interiors imitate daylight's structure (0008); keep one consistent direction because audiences read light without being taught (0026).
- **CASE VALUE:** Fictional source: the diya flames, low and warm; consistent through the clip.

### PA-D6 — What key level does the mood require?

- **DEFAULT (product_appearance):** Set the key by genre and mood before lighting anything (sk_alt_c003_0018); let level follow the dramatic line (0022); make mood with the character of the light, not exposure (0025); the fictional source still governs (0011).
- **CASE VALUE:** Low key, festive warmth.

### PA-D8 — Glass, dark or mirror-glossy object in frame — special handling?

- **DEFAULT (product_appearance):** Dark subjects reveal direct reflection because they produce less diffuse reflection (sk_lsm_c003_0017); on black-on-black, capitalize on it — light black as if it were metal, find and fill the family (sk_lsmx_0057). Use the diagnostic guidelines to identify polarized reflection (0018). Polarizing the source makes a reflection manageable (0019), but it sits late in the remedy ladder on cost grounds: try a darker background, the source toward the camera, and camera height first (sk_lsmx_0023); cross-polarizing source and lens buys freedom from geometry only at a large cost (sk_lsmx_0009). Polarized direct reflection is dimmer than ordinary direct reflection (0015).
- **CASE VALUE:** Flame reflections on the oil are wanted and may flicker; no other specular may appear during the move.

### PA-D10 — When may any of the above be overridden?

- **DEFAULT (product_appearance):** Technique serves a creative decision it does not make (sk_lsm_c003_0020): any default in this pack yields to an explicit creative decision recorded in DOCTRINE_DEVIATIONS with the brief clause that forces it.
- **CASE VALUE:** No deviation.

### CA-D1 — What reads first, second, third?

- **DEFAULT (composition_and_attention):** One dominant element by contrast — visual power is achieved by contrast, not 'impact' (vig_0009); eyes attract more strongly than probably any other subject (fre_0020); competing cues confuse rather than direct (repeated focus-shifting is the type case, ms_0019); complete control of attention is self-defeating (murch_0018); misdirection (murch_0033) is the scoped exception, only to set up a reveal.
- **CASE VALUE:** 1st read: the offer line by contrast; 2nd: the name by size; 3rd: the flickering flames — the only moving element, kept small so it does not compete (ms_0019).

### CA-D2 — Where does the subject sit in frame?

- **DEFAULT (composition_and_attention):** Off-centre within one of three approximate zones (fre_001; fre_0017, 0018); centre only when the scene points inward (0019); extreme placement needs a visible reason (0021). The source rejects coordinate rules (0016, vs its nod to classical proportion, 0028): zones are regions, never grids or named ratios.
- **CASE VALUE:** Text block upper zone, props lower zone, as in the still.

### CA-D3 — How does the frame hold the subject at its edges?

- **DEFAULT (composition_and_attention):** One edge treatment per shot (fre_002): tight fit with a slight deliberate gap (fre_0006); busy scene, edges stop mattering (0005); deliberate halving of a symmetrical subject (0007). Straight subject edges near frame edges read magnetic (0003); thin any bright framing element (0004).
- **CASE VALUE:** Deliberate margin around every string in every frame.

### CA-D5 — Balance the frame, or refuse the eye rest?

- **DEFAULT (composition_and_attention):** Classical balance is the default; it weighs size AND tone together (fre_0028, 0029; fre_005); refusing the eye a resting place (0032) is the declared energetic exception. Symmetry imposes order on a subject that has none (0030); diagonals need strict horizontals and verticals to divide against (0033, 0034 per CF-07).
- **CASE VALUE:** Balanced.

### CA-D6 — Which orientation and aspect?

- **DEFAULT (composition_and_attention):** Choose by the scene's shapes (fre_003): a vertical frame is not itself tallness (fre_0008); a square reads strict and draws the eye inward (0009, 0010); a wide frame needs shapes that call for it (0011).
- **LIMIT (pack text):** No accepted source treats fixed 9:16 feed frames (A01/G2): every aspect and orientation claim here predates vertical-feed formats; transfer is untested.
- **CASE VALUE:** 9:16 justified by the stacked vertical text block and the tall diya flames; CA-D6 LIMIT noted.

### CA-D7 — How does attention travel across cuts (video)?

- **DEFAULT (composition_and_attention):** Every new shot carries new information (gote_0004) and every departure is motivated (0006); drive eye-trace by alternating frame placement (0010), keeping difficulty near the optimum (0011); composition must differ at the cut (0026) — the wipe waives it (0035). Alternatives: move attention inside one continuous shot (ms_0010; ms_002), or block with a static wide (0017). One device per beat.
- **CASE VALUE:** One continuous shot; device: none needed — attention stays on the text; the flames are ambient.

### CA-D10 — How long may a shot hold?

- **DEFAULT (composition_and_attention):** Set length by silently describing the shot's contents; the description's time is the shot's (gote_0053). The fast-cutting norm — which the source calls alarming — is the ambient pace (0052).
- **CASE VALUE:** 6 s: 'three lines over a box of sweets while the diyas flicker' (gote_0053).

### CA-D11 — Does the camera move, and why?

- **DEFAULT (composition_and_attention):** Every move is motivated and stillness is chosen (ms_0002); an object in transit licenses a move across a location (0011); do the most with the least (murch_0015); shared success criterion: the technique goes unnoticed (ms_0018; ms_003).
- **CASE VALUE:** Camera does not move; stillness chosen (ms_0002) — the customer's 'हिलें-डुलें नहीं' forces it; the flames are the only motion.

### DOCTRINE_DEVIATIONS

- PA-D10: No deviation.

## 3. text_handling

- mode: generated (arm B native; arm A inherits the still's generated text) and composite (arm C)
- string `t1` (devanagari, headline, exact): **दीपावली की शुभकामनाएं**
- string `t2` (devanagari, body, exact): **सभी मिठाइयों पर 20% छूट**
- string `t3` (devanagari, brand_name, exact): **श्री गणेश मिष्ठान भंडार**
- composite arm: font Noto Serif Devanagari (bundled); positions: as IMG-TEXT-01 arm C; colour: as IMG-TEXT-01 arm C; rule: overlay by code at USD 0 on every frame of the arm-C clip; static overlay if the plate region is still, tracked (per-frame homography from the plate) if it moves; identical on both draws

## 4. dispatch_parameters (identical for every route; route mapping only in `TEST-CASES.yaml` → `routes[].params`)

- aspect: 9:16
- duration_s: 6
- resolution: 720p
- audio: off
- reference_slots: 1 (arms A and C) / 0 (arm B)

## 5. pre_dispatch_checks (the packs' CHECK lines, by id, run over the prompt before any call)

- `PA-D1-check`: Every key object has exactly one declared finish; two surfaces of the same tone still read differently by finish; no surface reads as both matte and mirror-glossy in one shot.
- `PA-D4-check`: One nameable fictional source; key direction agrees with it; no shadow in frame contradicts the declared direction.
- `PA-D6-check`: Mood is attributable to light character — direction, hardness, contrast — not to a brightness slider; the key level is declared and consistent across shots.
- `PA-D8-check`: Every specular on glass, dark or glossy surfaces is declared wanted or removed; none is accidental.
- `PA-D10-check`: Every deviation from PA-D1..PA-D9 is listed in DOCTRINE_DEVIATIONS with its forcing brief clause; none is silent.
- `CA-D1-check`: Name the 1st/2nd/3rd read; each carried by exactly one dominant cue; no two cues compete for one beat.
- `CA-D2-check`: Placement is stated as a zone plus the reason for it; no placement is justified by a named ratio or grid line.
- `CA-D3-check`: The edge treatment is one of the three, named; no accidental near-tangency between a subject edge and a frame edge.
- `CA-D5-check`: Declared balanced or deliberately restless; if balanced, a grayscale check shows tonal weight agreeing with size weight.
- `CA-D6-check`: The stated aspect is justified by a named shape in the scene, not by the platform alone.
- `CA-D7-check`: Per cut, name the new information and motivation; per beat, state the one device: cut, camera move, or blocking.
- `CA-D10-check`: No shot outlasts its describable content; the stated pace names the prevailing norm it assumes.
- `CA-D11-check`: Each camera move names its motivation; unmotivated moves are replaced by stillness or a cut.
- `no-in-image-text (composite arm / plate)`: the textless-plate prompt includes an explicit no-lettering instruction; lettering on a plate is a reject; the overlay step is code at USD 0.
- `exact-string-carry (generated arms)`: every required string appears in the generation prompt byte-identical to `text_requirements[].content` (checked by substring).
- pack limit (`composition_and_attention`): Devanagari correctness criteria do not exist in Canon — never generate Devanagari glyphs; composite text deterministically.
- pack limit (`product_appearance`): Devanagari correctness criteria do not exist in Canon — never generate Devanagari glyphs; composite text deterministically.

## 6. generation_prompt (byte-identical across every route listed for this case)

```text
Vertical video, one continuous static shot, 6 seconds, silent. A Diwali festive poster scene: on a deep maroon matte ground, an open box of Indian sweets with one gold foil band beside three lit clay diyas whose flames flicker gently and light the scene from below; the only movement is the flames and their warm light on the box. Devanagari text stays perfectly still and sharp in every frame, all spellings exact: at the top "दीपावली की शुभकामनाएं"; below it, larger and in bright gold, "सभी मिठाइयों पर 20% छूट"; across the lower third, the largest lettering of all, in cream, "श्री गणेश मिष्ठान भंडार". No other words, letters or numerals anywhere; no camera movement.
```

### i2v_motion_prompt (arms A and C, identical)

```text
Static camera, 6 seconds, silent. Keep everything in the image exactly where it is. Only the diya flames flicker gently and their warm light plays softly on the sweet box; nothing else moves; any lettering stays perfectly still and unchanged in every frame.
```
