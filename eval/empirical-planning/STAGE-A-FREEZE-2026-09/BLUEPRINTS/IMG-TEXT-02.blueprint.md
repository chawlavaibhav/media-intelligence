# Production blueprint — IMG-TEXT-02

```yaml
case_id: IMG-TEXT-02
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
- `composition_and_attention` — compiled — base:static_image (R05)
- `colour_and_visual_register` — uncompiled — base:static_image (R05)
- `typography_and_copy` — uncompiled — text_requirements_nonempty (R08)
- `indian_indic_context` — uncompiled — language_topology_present_or_market_IN (R10; market IN for every case)
- `commercial_communication` — uncompiled — advertising_acceptance_intent (R18)

## 2. decisions (by id; DEFAULT = the pack's text; CASE VALUE = this case's filled value)

### CA-D1 — What reads first, second, third?

- **DEFAULT (composition_and_attention):** One dominant element by contrast — visual power is achieved by contrast, not 'impact' (vig_0009); eyes attract more strongly than probably any other subject (fre_0020); competing cues confuse rather than direct (repeated focus-shifting is the type case, ms_0019); complete control of attention is self-defeating (murch_0018); misdirection (murch_0033) is the scoped exception, only to set up a reveal.
- **CASE VALUE:** 1st read: "FLAT 40% OFF" (largest, neon yellow on black — contrast); 2nd: "First 100 members only"; 3rd: "AlphaFit" and the date. One cue per read.

### CA-D2 — Where does the subject sit in frame?

- **DEFAULT (composition_and_attention):** Off-centre within one of three approximate zones (fre_001; fre_0017, 0018); centre only when the scene points inward (0019); extreme placement needs a visible reason (0021). The source rejects coordinate rules (0016, vs its nod to classical proportion, 0028): zones are regions, never grids or named ratios.
- **CASE VALUE:** Headline block off-centre, upper-left zone; the lower-right corner is left clean for the customer's logo (a visible reason for the asymmetry, fre_0021).

### CA-D3 — How does the frame hold the subject at its edges?

- **DEFAULT (composition_and_attention):** One edge treatment per shot (fre_002): tight fit with a slight deliberate gap (fre_0006); busy scene, edges stop mattering (0005); deliberate halving of a symmetrical subject (0007). Straight subject edges near frame edges read magnetic (0003); thin any bright framing element (0004).
- **CASE VALUE:** Sparse frame: tight fit with a deliberate margin around the headline (fre_0006); no letter touches the frame edge.

### CA-D4 — Use a frame within the frame?

- **DEFAULT (composition_and_attention):** No compulsion (fre_0022); when a subject passes behind an opening, the near-universal reaction is to shoot the moment it sits cleanly inside, breaking no edges; thin a bright framing element or it takes over (0004).
- **CASE VALUE:** None used.

### CA-D5 — Balance the frame, or refuse the eye rest?

- **DEFAULT (composition_and_attention):** Classical balance is the default; it weighs size AND tone together (fre_0028, 0029; fre_005); refusing the eye a resting place (0032) is the declared energetic exception. Symmetry imposes order on a subject that has none (0030); diagonals need strict horizontals and verticals to divide against (0033, 0034 per CF-07).
- **CASE VALUE:** Deliberately restless (fre_0032) — the brief says bold and energetic; declared as the energetic exception per CF-06.

### CA-D6 — Which orientation and aspect?

- **DEFAULT (composition_and_attention):** Choose by the scene's shapes (fre_003): a vertical frame is not itself tallness (fre_0008); a square reads strict and draws the eye inward (0009, 0010); a wide frame needs shapes that call for it (0011).
- **LIMIT (pack text):** No accepted source treats fixed 9:16 feed frames (A01/G2): every aspect and orientation claim here predates vertical-feed formats; transfer is untested.
- **CASE VALUE:** 1:1 justified by the stacked block of three lines forming a near-square shape.

### DOCTRINE_DEVIATIONS

- CA-D5: Deliberately restless (fre_0032) — the brief says bold and energetic; declared as the energetic exception per CF-06.

### 2a. Production parameters outside the triggered packs (brief-only; not Canon)

The `product_appearance` pack is not triggered for this Normalized Request (no product or packshot entity), so its lighting doctrine is not injected. The parameters below are the Executor's production choices on the brief alone and are attributed to nothing in Canon.

- light/mood: (scene mood) Key set by genre: high-contrast, hard-edged; mood from contrast, not from brightness.

## 3. text_handling

- mode: generated (arms A/B) and composite (arm C)
- string `t1` (latin, headline, exact): **FLAT 40% OFF**
- string `t2` (latin, body, exact): **First 100 members only**
- string `t3` (latin, brand_name, exact): **AlphaFit**
- string `t4` (latin, body, approximate): **Offer ends 15 January**
- composite arm: font Inter Black / Inter Bold (bundled, deterministic); positions: t1 upper-left, largest, neon yellow #E6FF00 on black; t2 below it, white; t3 lower-left, yellow; t4 small, white, under t2; lower-right corner empty; colour: neon yellow #E6FF00, white, on black #000000; rule: overlay by code at USD 0 on the textless plate; identical overlay on both base draws

## 4. dispatch_parameters (identical for every route; route mapping only in `TEST-CASES.yaml` → `routes[].params`)

- aspect: 1:1
- resolution: ~1 MP
- audio: not_applicable
- reference_slots: 0

## 5. pre_dispatch_checks (the packs' CHECK lines, by id, run over the prompt before any call)

- `CA-D1-check`: Name the 1st/2nd/3rd read; each carried by exactly one dominant cue; no two cues compete for one beat.
- `CA-D2-check`: Placement is stated as a zone plus the reason for it; no placement is justified by a named ratio or grid line.
- `CA-D3-check`: The edge treatment is one of the three, named; no accidental near-tangency between a subject edge and a frame edge.
- `CA-D4-check`: A framing element used is darker or thinner than the subject it frames.
- `CA-D5-check`: Declared balanced or deliberately restless; if balanced, a grayscale check shows tonal weight agreeing with size weight.
- `CA-D6-check`: The stated aspect is justified by a named shape in the scene, not by the platform alone.
- `no-in-image-text (composite arm / plate)`: the textless-plate prompt includes an explicit no-lettering instruction; lettering on a plate is a reject; the overlay step is code at USD 0.
- `exact-string-carry (generated arms)`: every required string appears in the generation prompt byte-identical to `text_requirements[].content` (checked by substring).
- pack limit (`composition_and_attention`): Devanagari correctness criteria do not exist in Canon — never generate Devanagari glyphs; composite text deterministically.

## 6. generation_prompt (byte-identical across every route listed for this case)

```text
Bold square social-media poster for a gym offer. Solid black background with a single wide diagonal neon-yellow stripe running from lower-left to upper-right; no people, no photographs, no objects. Text set in a heavy grotesque typeface: the headline "FLAT 40% OFF" in large neon yellow letters at the upper left; beneath it in white "First 100 members only"; beneath that in smaller white "Offer ends 15 January"; the gym name "AlphaFit" in neon yellow at the lower left. The lower-right corner stays completely empty. High contrast, energetic. No other words, letters, numerals or symbols anywhere.
```

### generation_prompt_textless_plate (arm C only)

```text
Bold square social-media poster background. Solid black background with a single wide diagonal neon-yellow stripe running from lower-left to upper-right; no people, no photographs, no objects. The upper-left two-thirds and the lower-left are plain black space; the lower-right corner stays completely empty. High contrast, energetic. No text, no letters, no numerals, no symbols anywhere in the image.
```
