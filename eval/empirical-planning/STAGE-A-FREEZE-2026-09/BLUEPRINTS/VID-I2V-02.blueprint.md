# Production blueprint — VID-I2V-02

```yaml
case_id: VID-I2V-02
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
- `indian_indic_context` — uncompiled — language_topology_present_or_market_IN (R10; market IN for every case)
- `commercial_communication` — uncompiled — advertising_acceptance_intent (R18)

## 2. decisions (by id; DEFAULT = the pack's text; CASE VALUE = this case's filled value)

### CA-D1 — What reads first, second, third?

- **DEFAULT (composition_and_attention):** One dominant element by contrast — visual power is achieved by contrast, not 'impact' (vig_0009); eyes attract more strongly than probably any other subject (fre_0020); competing cues confuse rather than direct (repeated focus-shifting is the type case, ms_0019); complete control of attention is self-defeating (murch_0018); misdirection (murch_0033) is the scoped exception, only to set up a reveal.
- **CASE VALUE:** 1st read stays his eyes and the smile (fre_0020); the glance toward the phone is the one attention event.

### CA-D3 — How does the frame hold the subject at its edges?

- **DEFAULT (composition_and_attention):** One edge treatment per shot (fre_002): tight fit with a slight deliberate gap (fre_0006); busy scene, edges stop mattering (0005); deliberate halving of a symmetrical subject (0007). Straight subject edges near frame edges read magnetic (0003); thin any bright framing element (0004).
- **CASE VALUE:** Framing unchanged from the still; no drift.

### CA-D6 — Which orientation and aspect?

- **DEFAULT (composition_and_attention):** Choose by the scene's shapes (fre_003): a vertical frame is not itself tallness (fre_0008); a square reads strict and draws the eye inward (0009, 0010); a wide frame needs shapes that call for it (0011).
- **LIMIT (pack text):** No accepted source treats fixed 9:16 feed frames (A01/G2): every aspect and orientation claim here predates vertical-feed formats; transfer is untested.
- **CASE VALUE:** 4:5 as the still.

### CA-D7 — How does attention travel across cuts (video)?

- **DEFAULT (composition_and_attention):** Every new shot carries new information (gote_0004) and every departure is motivated (0006); drive eye-trace by alternating frame placement (0010), keeping difficulty near the optimum (0011); composition must differ at the cut (0026) — the wipe waives it (0035). Alternatives: move attention inside one continuous shot (ms_0010; ms_002), or block with a static wide (0017). One device per beat.
- **CASE VALUE:** One continuous shot; device: blocking (his glance). No cut, no move.

### CA-D10 — How long may a shot hold?

- **DEFAULT (composition_and_attention):** Set length by silently describing the shot's contents; the description's time is the shot's (gote_0053). The fast-cutting norm — which the source calls alarming — is the ambient pace (0052).
- **CASE VALUE:** 6 s: 'a man looks down at his phone and smiles' (gote_0053).

### CA-D11 — Does the camera move, and why?

- **DEFAULT (composition_and_attention):** Every move is motivated and stillness is chosen (ms_0002); an object in transit licenses a move across a location (0011); do the most with the least (murch_0015); shared success criterion: the technique goes unnoticed (ms_0018; ms_003).
- **CASE VALUE:** Stillness chosen (ms_0002) — the customer's 'कैमरा एकदम स्थिर रहे' forces it.

### DOCTRINE_DEVIATIONS

- none — every applicable default is accepted as written.

### 2a. Production parameters outside the triggered packs (brief-only; not Canon)

The `product_appearance` pack is not triggered for this Normalized Request (no product or packshot entity), so its lighting doctrine is not injected. The parameters below are the Executor's production choices on the brief alone and are attributed to nothing in Canon.

- light/mood: (scene light) The still's window light camera-right is preserved; no flicker.
- light/mood: The accepted still is the creative decision; nothing re-decided.

## 3. text_handling

- mode: `none`

## 4. dispatch_parameters (identical for every route; route mapping only in `TEST-CASES.yaml` → `routes[].params`)

- aspect: 4:5
- duration_s: 6
- resolution: 720p-class
- audio: off
- reference_slots: 1

## 5. pre_dispatch_checks (the packs' CHECK lines, by id, run over the prompt before any call)

- `CA-D1-check`: Name the 1st/2nd/3rd read; each carried by exactly one dominant cue; no two cues compete for one beat.
- `CA-D3-check`: The edge treatment is one of the three, named; no accidental near-tangency between a subject edge and a frame edge.
- `CA-D6-check`: The stated aspect is justified by a named shape in the scene, not by the platform alone.
- `CA-D7-check`: Per cut, name the new information and motivation; per beat, state the one device: cut, camera move, or blocking.
- `CA-D10-check`: No shot outlasts its describable content; the stated pace names the prevailing norm it assumes.
- `CA-D11-check`: Each camera move names its motivation; unmotivated moves are replaced by stillness or a cut.
- `no-in-image-text`: the generation prompt includes an explicit no-lettering instruction and names no string; any lettering in the output is a reject (E5), never an exclusion.
- pack limit (`composition_and_attention`): Devanagari correctness criteria do not exist in Canon — never generate Devanagari glyphs; composite text deterministically.

## 6. generation_prompt (byte-identical across every route listed for this case)

```text
Animate this still, 6 seconds, silent, camera completely static. The man glances down toward the phone in his hand and his expression eases into a slight, natural smile; a small breath of movement in his shoulders, nothing more. His face, hair, clothes, the phone and the background stay exactly as in the image. No text or lettering.
```
