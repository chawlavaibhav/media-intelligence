# Production blueprint — IMG-EDIT-01

```yaml
case_id: IMG-EDIT-01
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

### PA-D10 — When may any of the above be overridden?

- **DEFAULT (product_appearance):** Technique serves a creative decision it does not make (sk_lsm_c003_0020): any default in this pack yields to an explicit creative decision recorded in DOCTRINE_DEVIATIONS with the brief clause that forces it.
- **CASE VALUE:** The supplied photograph is the creative decision (sk_lsm_c003_0020): PA-D1–PA-D9 are not re-decided on an edit; the only production decision is the removal. Recorded deviation: no lighting, finish or angle choice is made because the customer's clause 'same sofa, same room, same light' forces preservation.

### PA-D4 — What is the fictional light source, and does everything agree with it?

- **DEFAULT (product_appearance):** Name the fictional source first, then place the key to agree with it (sk_alt_c003_0011); build in the working order of scs_alt_c003_002 — one source photographs flat, added lights restore roundness (sk_alt_c003_0009), interiors imitate daylight's structure (0008); keep one consistent direction because audiences read light without being taught (0026).
- **CASE VALUE:** Preserved as supplied: the existing single light direction must survive in the filled area (no shadow in the vacated region may contradict the room's direction).

### CA-D1 — What reads first, second, third?

- **DEFAULT (composition_and_attention):** One dominant element by contrast — visual power is achieved by contrast, not 'impact' (vig_0009); eyes attract more strongly than probably any other subject (fre_0020); competing cues confuse rather than direct (repeated focus-shifting is the type case, ms_0019); complete control of attention is self-defeating (murch_0018); misdirection (murch_0033) is the scoped exception, only to set up a reveal.
- **CASE VALUE:** 1st read stays the sofa; the filled background must not introduce a new attention cue (ms_0019).

### CA-D3 — How does the frame hold the subject at its edges?

- **DEFAULT (composition_and_attention):** One edge treatment per shot (fre_002): tight fit with a slight deliberate gap (fre_0006); busy scene, edges stop mattering (0005); deliberate halving of a symmetrical subject (0007). Straight subject edges near frame edges read magnetic (0003); thin any bright framing element (0004).
- **CASE VALUE:** Edge treatment preserved as supplied; no re-crop.

### DOCTRINE_DEVIATIONS

- PA-D10: The supplied photograph is the creative decision (sk_lsm_c003_0020): PA-D1–PA-D9 are not re-decided on an edit; the only production decision is the removal. Recorded deviation: no lighting, finish or angle choice is made because the customer's clause 'same sofa, same room, same light' forces preservation.

## 3. text_handling

- mode: `none`

## 4. dispatch_parameters (identical for every route; route mapping only in `TEST-CASES.yaml` → `routes[].params`)

- aspect: as supplied
- resolution: as supplied
- audio: not_applicable
- reference_slots: 1

## 5. pre_dispatch_checks (the packs' CHECK lines, by id, run over the prompt before any call)

- `PA-D10-check`: Every deviation from PA-D1..PA-D9 is listed in DOCTRINE_DEVIATIONS with its forcing brief clause; none is silent.
- `PA-D4-check`: One nameable fictional source; key direction agrees with it; no shadow in frame contradicts the declared direction.
- `CA-D1-check`: Name the 1st/2nd/3rd read; each carried by exactly one dominant cue; no two cues compete for one beat.
- `CA-D3-check`: The edge treatment is one of the three, named; no accidental near-tangency between a subject edge and a frame edge.
- `no-in-image-text`: the generation prompt includes an explicit no-lettering instruction and names no string; any lettering in the output is a reject (E5), never an exclusion.
- pack limit (`composition_and_attention`): Devanagari correctness criteria do not exist in Canon — never generate Devanagari glyphs; composite text deterministically.
- pack limit (`product_appearance`): Devanagari correctness criteria do not exist in Canon — never generate Devanagari glyphs; composite text deterministically.

## 6. generation_prompt (byte-identical across every route listed for this case)

```text
Remove the person standing in the left background of this showroom photograph. Fill the vacated area with the same wall, floor and lighting that surround it, matching the existing light direction and shadows. Change nothing else: the sofa, its colour, its position, the room and the lighting stay exactly as they are. No text, no lettering, no logos added.
```
