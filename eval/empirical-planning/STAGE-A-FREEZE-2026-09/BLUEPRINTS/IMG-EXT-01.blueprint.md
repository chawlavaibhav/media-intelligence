# Production blueprint — IMG-EXT-01

```yaml
case_id: IMG-EXT-01
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

### CA-D6 — Which orientation and aspect?

- **DEFAULT (composition_and_attention):** Choose by the scene's shapes (fre_003): a vertical frame is not itself tallness (fre_0008); a square reads strict and draws the eye inward (0009, 0010); a wide frame needs shapes that call for it (0011).
- **LIMIT (pack text):** No accepted source treats fixed 9:16 feed frames (A01/G2): every aspect and orientation claim here predates vertical-feed formats; transfer is untested.
- **CASE VALUE:** 9:16 is forced by the platform (Stories); CA-D6's check wants a scene shape — the extension makes it true: tall sky above and open water below give the vertical frame a named shape (fre_0008: a vertical frame is not itself tallness). CA-D6 LIMIT on feed frames applies.

### CA-D2 — Where does the subject sit in frame?

- **DEFAULT (composition_and_attention):** Off-centre within one of three approximate zones (fre_001; fre_0017, 0018); centre only when the scene points inward (0019); extreme placement needs a visible reason (0021). The source rejects coordinate rules (0016, vs its nod to classical proportion, 0028): zones are regions, never grids or named ratios.
- **CASE VALUE:** The supplied composition (boat + headline) sits in the middle band; the new bands are quiet so placement stays as the customer set it.

### CA-D3 — How does the frame hold the subject at its edges?

- **DEFAULT (composition_and_attention):** One edge treatment per shot (fre_002): tight fit with a slight deliberate gap (fre_0006); busy scene, edges stop mattering (0005); deliberate halving of a symmetrical subject (0007). Straight subject edges near frame edges read magnetic (0003); thin any bright framing element (0004).
- **CASE VALUE:** Edge treatment: the boat and headline keep a deliberate gap from the new top and bottom edges (fre_0006).

### CA-D1 — What reads first, second, third?

- **DEFAULT (composition_and_attention):** One dominant element by contrast — visual power is achieved by contrast, not 'impact' (vig_0009); eyes attract more strongly than probably any other subject (fre_0020); competing cues confuse rather than direct (repeated focus-shifting is the type case, ms_0019); complete control of attention is self-defeating (murch_0018); misdirection (murch_0033) is the scoped exception, only to set up a reveal.
- **CASE VALUE:** The added sky and water carry no new attention cue; 1st read remains the headline, 2nd the boat (ms_0019).

### DOCTRINE_DEVIATIONS

- none — every applicable default is accepted as written.

### 2a. Production parameters outside the triggered packs (brief-only; not Canon)

The `product_appearance` pack is not triggered for this Normalized Request (no product or packshot entity), so its lighting doctrine is not injected. The parameters below are the Executor's production choices on the brief alone and are attributed to nothing in Canon.

- light/mood: The supplied banner is the creative decision; PA-D1–PA-D9 not re-decided. Recorded deviation forced by 'don't crop … same relationship'.

## 3. text_handling

- mode: `none (no new lettering; the supplied headline is preserved under mutation_intents)`

## 4. dispatch_parameters (identical for every route; route mapping only in `TEST-CASES.yaml` → `routes[].params`)

- aspect: 9:16
- resolution: supplied width
- audio: not_applicable
- reference_slots: 1

## 5. pre_dispatch_checks (the packs' CHECK lines, by id, run over the prompt before any call)

- `CA-D6-check`: The stated aspect is justified by a named shape in the scene, not by the platform alone.
- `CA-D2-check`: Placement is stated as a zone plus the reason for it; no placement is justified by a named ratio or grid line.
- `CA-D3-check`: The edge treatment is one of the three, named; no accidental near-tangency between a subject edge and a frame edge.
- `CA-D1-check`: Name the 1st/2nd/3rd read; each carried by exactly one dominant cue; no two cues compete for one beat.
- `no-in-image-text`: the generation prompt includes an explicit no-lettering instruction and names no string; any lettering in the output is a reject (E5), never an exclusion.
- pack limit (`composition_and_attention`): Devanagari correctness criteria do not exist in Canon — never generate Devanagari glyphs; composite text deterministically.

## 6. generation_prompt (byte-identical across every route listed for this case)

```text
Extend this landscape banner upward and downward to a vertical 9:16 frame without cropping or moving anything already in it. Above, continue the same sky; below, continue the same water, matching the existing horizon, light and colour so no seam shows. The boat and the headline stay exactly as they are and in the same position relative to each other. Do not add any new object, text or lettering.
```
