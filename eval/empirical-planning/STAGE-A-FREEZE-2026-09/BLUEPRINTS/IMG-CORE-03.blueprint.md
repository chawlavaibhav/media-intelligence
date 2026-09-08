# Production blueprint — IMG-CORE-03

```yaml
case_id: IMG-CORE-03
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
- `product_appearance` — compiled — product_or_packshot_entity_present (R06)
- `indian_indic_context` — uncompiled — language_topology_present_or_market_IN (R10; market IN for every case)
- `commercial_communication` — uncompiled — advertising_acceptance_intent (R18)

## 2. decisions (by id; DEFAULT = the pack's text; CASE VALUE = this case's filled value)

### PA-D1 — What reflection type dominates each key product surface — diffuse (matte), direct (glossy), or glare?

- **DEFAULT (product_appearance):** Declare a finish per named object before any prompt is written and light for the declared finish; the three reflection types are a contrast set (scs_lsm_c003_001) — finish is a property of the surface, not of the light.
- **CASE VALUE:** biryani rice: diffuse (matte) with glossy ghee sheen on the meat pieces (direct); handi: brass/copper — polished metal, CF-09 material rule: lit by embracing direct reflection; raita: diffuse with a soft sheen; lemon skin: semi-gloss; table surface: diffuse dark wood.

### PA-D2 — Where may the highlight sit on each glossy surface?

- **DEFAULT (product_appearance):** One highlight per surface, consistent with one implied source placed inside or outside the family of angles by intent (scs_lsm_c003_002); the reflection reports the source's size.
- **CASE VALUE:** One soft window reflection on the handi rim from a single large source top-left; no second highlight on the metal.

### PA-D3 — Hard or soft source?

- **DEFAULT (product_appearance):** Large/soft relative to subject for product surfaces unless the brief forces drama; choose the instrument for the shadow edge it must produce (sk_alt_c003_0006); for direct reflection the source's size sets the highlight's size (sk_lsm_c003_0014).
- **CASE VALUE:** Large soft source; soft shadow edges under bowls; highlight on the handi large and soft.

### PA-D4 — What is the fictional light source, and does everything agree with it?

- **DEFAULT (product_appearance):** Name the fictional source first, then place the key to agree with it (sk_alt_c003_0011); build in the working order of scs_alt_c003_002 — one source photographs flat, added lights restore roundness (sk_alt_c003_0009), interiors imitate daylight's structure (0008); keep one consistent direction because audiences read light without being taught (0026).
- **CASE VALUE:** Fictional source: daylight window top-left of the table; every shadow falls bottom-right.

### PA-D5 — How does the product separate from its ground?

- **DEFAULT (product_appearance):** By tonal separation, either direction (sk_alt_c003_0015). Scope rule: 0015 governs subject-against-ground; the dark-to-light progression (0017) governs only staged depth planes. Cold, plain grounds separate warm subjects (0003); a deliberately shiny prop (0004) trades off against a quiet ground — decide per object, never both on one surface.
- **CASE VALUE:** Warm dishes against a cool, dark, plain wood ground (sk_alt_c003_0003); no staged depth planes in a flat-lay.

### PA-D6 — What key level does the mood require?

- **DEFAULT (product_appearance):** Set the key by genre and mood before lighting anything (sk_alt_c003_0018); let level follow the dramatic line (0022); make mood with the character of the light, not exposure (0025); the fictional source still governs (0011).
- **CASE VALUE:** Medium key, generous and clean — mood from soft side light, not from a bright exposure.

### PA-D7 — Does the imagery earn its space commercially?

- **DEFAULT (product_appearance):** Treat the picture as a salesman that must earn its space (sk_hop_sa_0026); assume the viewer decides from a glance at headline or picture (0035); size imagery by importance to the sale, never decoration.
- **CASE VALUE:** Sells at a glance: 'a full, generous biryani meal for one price' (price added later by the customer).

### PA-D8 — Glass, dark or mirror-glossy object in frame — special handling?

- **DEFAULT (product_appearance):** Dark subjects reveal direct reflection because they produce less diffuse reflection (sk_lsm_c003_0017); on black-on-black, capitalize on it — light black as if it were metal, find and fill the family (sk_lsmx_0057). Use the diagnostic guidelines to identify polarized reflection (0018). Polarizing the source makes a reflection manageable (0019), but it sits late in the remedy ladder on cost grounds: try a darker background, the source toward the camera, and camera height first (sk_lsmx_0023); cross-polarizing source and lens buys freedom from geometry only at a large cost (sk_lsmx_0009). Polarized direct reflection is dimmer than ordinary direct reflection (0015).
- **CASE VALUE:** Polished handi: the rim highlight is wanted; any hot mirror-spot on the brass body is removed by the source's size, not by a polarizer (CF-11: never cross-polarize metal).

### PA-D9 — Which angle is the hero angle?

- **DEFAULT (product_appearance):** The angle showing the most surfaces of the product (sk_alt_c003_0010) — Canon's only committed angle-choice criterion.
- **LIMIT (pack text):** Packshot convention absent from Canon (A13 application_unbound): hero-angle, label-legibility and scale-cue conventions are not in the corpus; this default is one 1949 cinema-era claim — do not overgeneralize.
- **CASE VALUE:** Top-down shows the handi's opening and rim; the most surfaces of a round pot from above is the full opening plus the rim ring.

### PA-D10 — When may any of the above be overridden?

- **DEFAULT (product_appearance):** Technique serves a creative decision it does not make (sk_lsm_c003_0020): any default in this pack yields to an explicit creative decision recorded in DOCTRINE_DEVIATIONS with the brief clause that forces it.
- **CASE VALUE:** Deviation from PA-D9's 'most surfaces' preference: the customer's clause 'upar se, top view' forces the top-down angle; recorded.

### CA-D1 — What reads first, second, third?

- **DEFAULT (composition_and_attention):** One dominant element by contrast — visual power is achieved by contrast, not 'impact' (vig_0009); eyes attract more strongly than probably any other subject (fre_0020); competing cues confuse rather than direct (repeated focus-shifting is the type case, ms_0019); complete control of attention is self-defeating (murch_0018); misdirection (murch_0033) is the scoped exception, only to set up a reveal.
- **CASE VALUE:** 1st read: the handi (largest warm mass at centre); 2nd: the white raita bowl (tonal contrast); 3rd: lemon and onion colour notes.

### CA-D2 — Where does the subject sit in frame?

- **DEFAULT (composition_and_attention):** Off-centre within one of three approximate zones (fre_001; fre_0017, 0018); centre only when the scene points inward (0019); extreme placement needs a visible reason (0021). The source rejects coordinate rules (0016, vs its nod to classical proportion, 0028): zones are regions, never grids or named ratios.
- **CASE VALUE:** Centred, because a flat-lay spread points inward to the handi (fre_0019).

### CA-D3 — How does the frame hold the subject at its edges?

- **DEFAULT (composition_and_attention):** One edge treatment per shot (fre_002): tight fit with a slight deliberate gap (fre_0006); busy scene, edges stop mattering (0005); deliberate halving of a symmetrical subject (0007). Straight subject edges near frame edges read magnetic (0003); thin any bright framing element (0004).
- **CASE VALUE:** Busy scene: edges stop mattering (fre_0005); sides may run off-frame; the handi does not touch the frame.

### CA-D4 — Use a frame within the frame?

- **DEFAULT (composition_and_attention):** No compulsion (fre_0022); when a subject passes behind an opening, the near-universal reaction is to shoot the moment it sits cleanly inside, breaking no edges; thin a bright framing element or it takes over (0004).
- **CASE VALUE:** None used.

### CA-D5 — Balance the frame, or refuse the eye rest?

- **DEFAULT (composition_and_attention):** Classical balance is the default; it weighs size AND tone together (fre_0028, 0029; fre_005); refusing the eye a resting place (0032) is the declared energetic exception. Symmetry imposes order on a subject that has none (0030); diagonals need strict horizontals and verticals to divide against (0033, 0034 per CF-07).
- **CASE VALUE:** Balanced by tone: the bright raita bowl top-right against the dark onion/lemon cluster bottom-left.

### CA-D6 — Which orientation and aspect?

- **DEFAULT (composition_and_attention):** Choose by the scene's shapes (fre_003): a vertical frame is not itself tallness (fre_0008); a square reads strict and draws the eye inward (0009, 0010); a wide frame needs shapes that call for it (0011).
- **LIMIT (pack text):** No accepted source treats fixed 9:16 feed frames (A01/G2): every aspect and orientation claim here predates vertical-feed formats; transfer is untested.
- **CASE VALUE:** 1:1 justified by the round handi and the radial spread (fre_0009/0010: square draws the eye inward).

### DOCTRINE_DEVIATIONS

- PA-D10: Deviation from PA-D9's 'most surfaces' preference: the customer's clause 'upar se, top view' forces the top-down angle; recorded.

## 3. text_handling

- mode: `none`

## 4. dispatch_parameters (identical for every route; route mapping only in `TEST-CASES.yaml` → `routes[].params`)

- aspect: 1:1
- resolution: ~1 MP
- audio: not_applicable
- reference_slots: 0

## 5. pre_dispatch_checks (the packs' CHECK lines, by id, run over the prompt before any call)

- `PA-D1-check`: Every key object has exactly one declared finish; two surfaces of the same tone still read differently by finish; no surface reads as both matte and mirror-glossy in one shot.
- `PA-D2-check`: Highlight positions agree with the single implied source; highlight brightness does not fall off with implied source distance; a large soft source reads as a large reflection, never a hard point.
- `PA-D3-check`: Shadow edge quality and highlight size agree — a soft shadow with a pinpoint specular, or the reverse, is a lighting contradiction.
- `PA-D4-check`: One nameable fictional source; key direction agrees with it; no shadow in frame contradicts the declared direction.
- `PA-D5-check`: Product-to-ground tonal contrast survives a grayscale check; where depth planes are staged, nearer planes are darker than farther ones.
- `PA-D6-check`: Mood is attributable to light character — direction, hardness, contrast — not to a brightness slider; the key level is declared and consistent across shots.
- `PA-D7-check`: State in one line what the hero image sells at a glance; if that line needs the body copy, the image fails.
- `PA-D8-check`: Every specular on glass, dark or glossy surfaces is declared wanted or removed; none is accidental.
- `PA-D9-check`: Count visible faces of the product; if a candidate angle shows more surfaces without breaking PA-D2 or PA-D5, prefer it.
- `PA-D10-check`: Every deviation from PA-D1..PA-D9 is listed in DOCTRINE_DEVIATIONS with its forcing brief clause; none is silent.
- `CA-D1-check`: Name the 1st/2nd/3rd read; each carried by exactly one dominant cue; no two cues compete for one beat.
- `CA-D2-check`: Placement is stated as a zone plus the reason for it; no placement is justified by a named ratio or grid line.
- `CA-D3-check`: The edge treatment is one of the three, named; no accidental near-tangency between a subject edge and a frame edge.
- `CA-D4-check`: A framing element used is darker or thinner than the subject it frames.
- `CA-D5-check`: Declared balanced or deliberately restless; if balanced, a grayscale check shows tonal weight agreeing with size weight.
- `CA-D6-check`: The stated aspect is justified by a named shape in the scene, not by the platform alone.
- `no-in-image-text`: the generation prompt includes an explicit no-lettering instruction and names no string; any lettering in the output is a reject (E5), never an exclusion.
- pack limit (`composition_and_attention`): Devanagari correctness criteria do not exist in Canon — never generate Devanagari glyphs; composite text deterministically.
- pack limit (`product_appearance`): Devanagari correctness criteria do not exist in Canon — never generate Devanagari glyphs; composite text deterministically.

## 6. generation_prompt (byte-identical across every route listed for this case)

```text
Top-down food photograph, camera looking straight down. A round brass handi of dum biryani at the exact centre — saffron rice, a few pieces of meat with a glossy ghee sheen, fried onion and mint on top. Around it on a dark plain wooden table: a small white bowl of raita top-right, a plate of onion rings and green chilli bottom-left, lemon halves, a small salad. Single soft daylight from the top-left, soft shadows falling bottom-right, one soft reflection on the brass rim. Clean, generous, everyday-premium; no gold cutlery, no candles, no glassware. No text, no menu card, no price, no logo, no numerals anywhere in the image.
```
