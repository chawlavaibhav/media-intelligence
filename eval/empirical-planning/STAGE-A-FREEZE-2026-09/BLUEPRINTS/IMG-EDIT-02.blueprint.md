# Production blueprint — IMG-EDIT-02

```yaml
case_id: IMG-EDIT-02
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
- `product_appearance` — compiled — product_or_packshot_entity_present (R06)
- `indian_indic_context` — uncompiled — language_topology_present_or_market_IN (R10; market IN for every case)
- `commercial_communication` — uncompiled — advertising_acceptance_intent (R18)

## 2. decisions (by id; DEFAULT = the pack's text; CASE VALUE = this case's filled value)

### PA-D10 — When may any of the above be overridden?

- **DEFAULT (product_appearance):** Technique serves a creative decision it does not make (sk_lsm_c003_0020): any default in this pack yields to an explicit creative decision recorded in DOCTRINE_DEVIATIONS with the brief clause that forces it.
- **CASE VALUE:** The supplied photograph is the creative decision (sk_lsm_c003_0020); PA-D1–PA-D9 are not re-decided. Recorded deviation forced by 'बिल्कुल वैसा ही रहना चाहिए': finish, light and angle are preserved as supplied.

### PA-D5 — How does the product separate from its ground?

- **DEFAULT (product_appearance):** By tonal separation, either direction (sk_alt_c003_0015). Scope rule: 0015 governs subject-against-ground; the dark-to-light progression (0017) governs only staged depth planes. Cold, plain grounds separate warm subjects (0003); a deliberately shiny prop (0004) trades off against a quiet ground — decide per object, never both on one surface.
- **CASE VALUE:** Product-to-ground separation after the edit: the pack against pure white must survive a grayscale check (a pale pack needs its own edge, carried by the optional soft shadow, not by a dark outline).

### PA-D8 — Glass, dark or mirror-glossy object in frame — special handling?

- **DEFAULT (product_appearance):** Dark subjects reveal direct reflection because they produce less diffuse reflection (sk_lsm_c003_0017); on black-on-black, capitalize on it — light black as if it were metal, find and fill the family (sk_lsmx_0057). Use the diagnostic guidelines to identify polarized reflection (0018). Polarizing the source makes a reflection manageable (0019), but it sits late in the remedy ladder on cost grounds: try a darker background, the source toward the camera, and camera height first (sk_lsmx_0023); cross-polarizing source and lens buys freedom from geometry only at a large cost (sk_lsmx_0009). Polarized direct reflection is dimmer than ordinary direct reflection (0015).
- **CASE VALUE:** Any specular already on the pack is kept as supplied; none is added or removed.

### CA-D2 — Where does the subject sit in frame?

- **DEFAULT (composition_and_attention):** Off-centre within one of three approximate zones (fre_001; fre_0017, 0018); centre only when the scene points inward (0019); extreme placement needs a visible reason (0021). The source rejects coordinate rules (0016, vs its nod to classical proportion, 0028): zones are regions, never grids or named ratios.
- **CASE VALUE:** Placement unchanged from the supplied frame.

### CA-D3 — How does the frame hold the subject at its edges?

- **DEFAULT (composition_and_attention):** One edge treatment per shot (fre_002): tight fit with a slight deliberate gap (fre_0006); busy scene, edges stop mattering (0005); deliberate halving of a symmetrical subject (0007). Straight subject edges near frame edges read magnetic (0003); thin any bright framing element (0004).
- **CASE VALUE:** Edge treatment unchanged; no re-crop.

### DOCTRINE_DEVIATIONS

- PA-D10: The supplied photograph is the creative decision (sk_lsm_c003_0020); PA-D1–PA-D9 are not re-decided. Recorded deviation forced by 'बिल्कुल वैसा ही रहना चाहिए': finish, light and angle are preserved as supplied.

## 3. text_handling

- mode: `none (no new lettering; the two supplied Devanagari strings are preserved under mutation_intents — they are not generated)`

## 4. dispatch_parameters (identical for every route; route mapping only in `TEST-CASES.yaml` → `routes[].params`)

- aspect: as supplied
- resolution: as supplied
- audio: not_applicable
- reference_slots: 1

## 5. pre_dispatch_checks (the packs' CHECK lines, by id, run over the prompt before any call)

- `PA-D10-check`: Every deviation from PA-D1..PA-D9 is listed in DOCTRINE_DEVIATIONS with its forcing brief clause; none is silent.
- `PA-D5-check`: Product-to-ground tonal contrast survives a grayscale check; where depth planes are staged, nearer planes are darker than farther ones.
- `PA-D8-check`: Every specular on glass, dark or glossy surfaces is declared wanted or removed; none is accidental.
- `CA-D2-check`: Placement is stated as a zone plus the reason for it; no placement is justified by a named ratio or grid line.
- `CA-D3-check`: The edge treatment is one of the three, named; no accidental near-tangency between a subject edge and a frame edge.
- `no-in-image-text`: the generation prompt includes an explicit no-lettering instruction and names no string; any lettering in the output is a reject (E5), never an exclusion.
- pack limit (`composition_and_attention`): Devanagari correctness criteria do not exist in Canon — never generate Devanagari glyphs; composite text deterministically.
- pack limit (`product_appearance`): Devanagari correctness criteria do not exist in Canon — never generate Devanagari glyphs; composite text deterministically.

## 6. generation_prompt (byte-identical across every route listed for this case)

```text
Replace the background of this product photograph with a plain, uniform pure white, as for an online marketplace listing. Keep the pack itself exactly as photographed: same size, same position, same colours, and every printed character on the pack unchanged, including the words "शुद्ध मसाले" and "५०० ग्राम". A soft, light shadow directly under the pack is allowed. Do not add any text, lettering, logo or object.
```
