# Production blueprint — VID-2SPK-01

```yaml
case_id: VID-2SPK-01
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
- `product_appearance` — compiled — product_or_packshot_entity_present (R06)
- `indian_indic_context` — uncompiled — language_topology_present_or_market_IN (R10; market IN for every case)
- `commercial_communication` — uncompiled — advertising_acceptance_intent (R18)

## 2. decisions (by id; DEFAULT = the pack's text; CASE VALUE = this case's filled value)

### PA-D1 — What reflection type dominates each key product surface — diffuse (matte), direct (glossy), or glare?

- **DEFAULT (product_appearance):** Declare a finish per named object before any prompt is written and light for the declared finish; the three reflection types are a contrast set (scs_lsm_c003_001) — finish is a property of the surface, not of the light.
- **CASE VALUE:** paint_can: semi-gloss metal (direct, soft); wall: matte fresh paint; skin: diffuse with natural speculars kept (sk_lsmx_0051).

### PA-D4 — What is the fictional light source, and does everything agree with it?

- **DEFAULT (product_appearance):** Name the fictional source first, then place the key to agree with it (sk_alt_c003_0011); build in the working order of scs_alt_c003_002 — one source photographs flat, added lights restore roundness (sk_alt_c003_0009), interiors imitate daylight's structure (0008); keep one consistent direction because audiences read light without being taught (0026).
- **CASE VALUE:** Fictional source: a large window camera-right in an empty new room; key on both faces agrees; one direction.

### PA-D6 — What key level does the mood require?

- **DEFAULT (product_appearance):** Set the key by genre and mood before lighting anything (sk_alt_c003_0018); let level follow the dramatic line (0022); make mood with the character of the light, not exposure (0025); the fictional source still governs (0011).
- **CASE VALUE:** High key, warm afternoon; mood from soft window light.

### PA-D10 — When may any of the above be overridden?

- **DEFAULT (product_appearance):** Technique serves a creative decision it does not make (sk_lsm_c003_0020): any default in this pack yields to an explicit creative decision recorded in DOCTRINE_DEVIATIONS with the brief clause that forces it.
- **CASE VALUE:** No deviation.

### CA-D1 — What reads first, second, third?

- **DEFAULT (composition_and_attention):** One dominant element by contrast — visual power is achieved by contrast, not 'impact' (vig_0009); eyes attract more strongly than probably any other subject (fre_0020); competing cues confuse rather than direct (repeated focus-shifting is the type case, ms_0019); complete control of attention is self-defeating (murch_0018); misdirection (murch_0033) is the scoped exception, only to set up a reveal.
- **CASE VALUE:** Beat 1: 1st read the wife's face as she speaks (fre_0020); beat 2: the husband's face as he answers — attention moves by the turn itself, not by a competing cue (ms_0019). 3rd read: the paint can in his hand.

### CA-D2 — Where does the subject sit in frame?

- **DEFAULT (composition_and_attention):** Off-centre within one of three approximate zones (fre_001; fre_0017, 0018); centre only when the scene points inward (0019); extreme placement needs a visible reason (0021). The source rejects coordinate rules (0016, vs its nod to classical proportion, 0028): zones are regions, never grids or named ratios.
- **CASE VALUE:** Two-shot: wife left zone, husband right zone, facing each other; the wall behind.

### CA-D3 — How does the frame hold the subject at its edges?

- **DEFAULT (composition_and_attention):** One edge treatment per shot (fre_002): tight fit with a slight deliberate gap (fre_0006); busy scene, edges stop mattering (0005); deliberate halving of a symmetrical subject (0007). Straight subject edges near frame edges read magnetic (0003); thin any bright framing element (0004).
- **CASE VALUE:** Tight fit with a deliberate gap above both heads (fre_0006).

### CA-D5 — Balance the frame, or refuse the eye rest?

- **DEFAULT (composition_and_attention):** Classical balance is the default; it weighs size AND tone together (fre_0028, 0029; fre_005); refusing the eye a resting place (0032) is the declared energetic exception. Symmetry imposes order on a subject that has none (0030); diagonals need strict horizontals and verticals to divide against (0033, 0034 per CF-07).
- **CASE VALUE:** Balanced: two figures of similar tonal weight.

### CA-D6 — Which orientation and aspect?

- **DEFAULT (composition_and_attention):** Choose by the scene's shapes (fre_003): a vertical frame is not itself tallness (fre_0008); a square reads strict and draws the eye inward (0009, 0010); a wide frame needs shapes that call for it (0011).
- **LIMIT (pack text):** No accepted source treats fixed 9:16 feed frames (A01/G2): every aspect and orientation claim here predates vertical-feed formats; transfer is untested.
- **CASE VALUE:** 9:16 justified by two standing figures close together; CA-D6 LIMIT noted.

### CA-D7 — How does attention travel across cuts (video)?

- **DEFAULT (composition_and_attention):** Every new shot carries new information (gote_0004) and every departure is motivated (0006); drive eye-trace by alternating frame placement (0010), keeping difficulty near the optimum (0011); composition must differ at the cut (0026) — the wipe waives it (0035). Alternatives: move attention inside one continuous shot (ms_0010; ms_002), or block with a static wide (0017). One device per beat.
- **CASE VALUE:** One continuous two-shot; device per beat: blocking (she turns to him; he lifts the can). No cut, so no line is crossed.

### CA-D9 — Screen direction and the line?

- **DEFAULT (composition_and_attention):** Frame edges are the audience's directional reference (gos_0005); keep setups within one 180-degree arc (0010; gos_001); movement and position persist across cuts (gote_0017, 0018; gos_0011); reciprocal coverage obeys the line (gote_0056). A far-side setup is good in itself — the reversal shows only at the cut (gos_0012, contradicting 0007/0010); crossing needs a declared creative reason (0013).
- **CASE VALUE:** Wife stays frame-left, husband frame-right; the sight line between them is the action line (gos_001) and the camera stays on one side of it.

### CA-D10 — How long may a shot hold?

- **DEFAULT (composition_and_attention):** Set length by silently describing the shot's contents; the description's time is the shot's (gote_0053). The fast-cutting norm — which the source calls alarming — is the ambient pace (0052).
- **CASE VALUE:** 8 s: 'a woman turns to a man and asks; a pause; he answers and lifts the can' (gote_0053) — two turns and a pause need eight seconds.

### CA-D11 — Does the camera move, and why?

- **DEFAULT (composition_and_attention):** Every move is motivated and stillness is chosen (ms_0002); an object in transit licenses a move across a location (0011); do the most with the least (murch_0015); shared success criterion: the technique goes unnoticed (ms_0018; ms_003).
- **CASE VALUE:** Camera still (ms_0002); the dialogue supplies the movement.

### DOCTRINE_DEVIATIONS

- PA-D10: No deviation.

## 3. text_handling

- mode: `none`

## 4. dispatch_parameters (identical for every route; route mapping only in `TEST-CASES.yaml` → `routes[].params`)

- aspect: 9:16
- duration_s: 8
- resolution: 720p
- audio: on (native speech, arm A) / off on the chain plate and i2v, speech added by lipsync (arm B)
- reference_slots: 0

## 5. pre_dispatch_checks (the packs' CHECK lines, by id, run over the prompt before any call)

- `PA-D1-check`: Every key object has exactly one declared finish; two surfaces of the same tone still read differently by finish; no surface reads as both matte and mirror-glossy in one shot.
- `PA-D4-check`: One nameable fictional source; key direction agrees with it; no shadow in frame contradicts the declared direction.
- `PA-D6-check`: Mood is attributable to light character — direction, hardness, contrast — not to a brightness slider; the key level is declared and consistent across shots.
- `PA-D10-check`: Every deviation from PA-D1..PA-D9 is listed in DOCTRINE_DEVIATIONS with its forcing brief clause; none is silent.
- `CA-D1-check`: Name the 1st/2nd/3rd read; each carried by exactly one dominant cue; no two cues compete for one beat.
- `CA-D2-check`: Placement is stated as a zone plus the reason for it; no placement is justified by a named ratio or grid line.
- `CA-D3-check`: The edge treatment is one of the three, named; no accidental near-tangency between a subject edge and a frame edge.
- `CA-D5-check`: Declared balanced or deliberately restless; if balanced, a grayscale check shows tonal weight agreeing with size weight.
- `CA-D6-check`: The stated aspect is justified by a named shape in the scene, not by the platform alone.
- `CA-D7-check`: Per cut, name the new information and motivation; per beat, state the one device: cut, camera move, or blocking.
- `CA-D9-check`: Screen direction and side-of-frame persist across consecutive shots, or something on screen shows the change (gos_0007), or the crossing is declared in DOCTRINE_DEVIATIONS.
- `CA-D10-check`: No shot outlasts its describable content; the stated pace names the prevailing norm it assumes.
- `CA-D11-check`: Each camera move names its motivation; unmotivated moves are replaced by stillness or a cut.
- `no-in-image-text`: the generation prompt includes an explicit no-lettering instruction and names no string; any lettering in the output is a reject (E5), never an exclusion.
- pack limit (`composition_and_attention`): Devanagari correctness criteria do not exist in Canon — never generate Devanagari glyphs; composite text deterministically.
- pack limit (`product_appearance`): Devanagari correctness criteria do not exist in Canon — never generate Devanagari glyphs; composite text deterministically.

## 6. generation_prompt (byte-identical across every route listed for this case)

```text
Vertical video, one continuous static two-shot, 8 seconds. An empty, newly painted room in an Indian home, soft afternoon window light from the right. A woman and a man in their early thirties stand close together facing each other, she on the left, he on the right holding an unlabelled paint can; the freshly painted wall behind them. She turns to him and asks in Hindi, lips matching the words: "यह रंग कैसा लगेगा?". A short pause. He smiles and answers in Hindi, lips matching: "घर जैसा", lifting the can slightly. Only the speaking person's mouth moves during each line. Warm, natural, unhurried. Room ambience only under the voices; no music. No text, captions, subtitles, logos or lettering anywhere in any frame.
```

### chain_plate_prompt (arm B step 1, still image)

```text
Vertical photograph. An empty, newly painted room in an Indian home, soft afternoon window light from the right. A woman and a man in their early thirties stand close together facing each other, she on the left, he on the right holding an unlabelled paint can; the freshly painted wall behind them; both faces fully visible, mouths closed, mid-shot with a small gap above their heads. No text, logos or lettering anywhere.
```

### chain_i2v_motion_prompt (arm B step 2, from the accepted plate)

```text
Static camera, 8 seconds. The woman turns her head slightly toward the man as if about to speak, then the man smiles and lifts the paint can a little. Both keep their faces and positions; mouths stay closed; no other motion. No sound.
```

### chain_tts_lines (arm B step 3)

```text
L1 (female voice, warm, questioning): यह रंग कैसा लगेगा?
L2 (male voice, warm, gentle smile): घर जैसा
```

### chain_lipsync (arm B step 4)

```text
Drive = L1, 0.6 s silence, L2 (ElevenLabs v3 repeat 1 by the frozen rule). Apply to the accepted i2v clip. The route must assign L1 to the woman and L2 to the man; no speaker masks are supplied — turn assignment is the capability under test.
```
