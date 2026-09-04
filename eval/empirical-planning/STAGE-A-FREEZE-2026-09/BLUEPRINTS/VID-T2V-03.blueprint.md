# Production blueprint — VID-T2V-03

```yaml
case_id: VID-T2V-03
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

## 2. decisions (by id; DEFAULT = the pack's text; CASE VALUE = this case's filled value)

### CA-D1 — What reads first, second, third?

- **DEFAULT (composition_and_attention):** One dominant element by contrast — visual power is achieved by contrast, not 'impact' (vig_0009); eyes attract more strongly than probably any other subject (fre_0020); competing cues confuse rather than direct (repeated focus-shifting is the type case, ms_0019); complete control of attention is self-defeating (murch_0018); misdirection (murch_0033) is the scoped exception, only to set up a reveal.
- **CASE VALUE:** 1st read: the child's face (fre_0020); 2nd: the mother entering with the umbrella (a new contrast at the beat change); 3rd: the rain-filled lane. One cue per beat.

### CA-D2 — Where does the subject sit in frame?

- **DEFAULT (composition_and_attention):** Off-centre within one of three approximate zones (fre_001; fre_0017, 0018); centre only when the scene points inward (0019); extreme placement needs a visible reason (0021). The source rejects coordinate rules (0016, vs its nod to classical proportion, 0028): zones are regions, never grids or named ratios.
- **CASE VALUE:** Child centred-low at the start (the lane points inward, fre_0019); the mother enters from the left and the pair end slightly left of centre.

### CA-D3 — How does the frame hold the subject at its edges?

- **DEFAULT (composition_and_attention):** One edge treatment per shot (fre_002): tight fit with a slight deliberate gap (fre_0006); busy scene, edges stop mattering (0005); deliberate halving of a symmetrical subject (0007). Straight subject edges near frame edges read magnetic (0003); thin any bright framing element (0004).
- **CASE VALUE:** Busy scene (rain, lane): edges stop mattering (fre_0005).

### CA-D5 — Balance the frame, or refuse the eye rest?

- **DEFAULT (composition_and_attention):** Classical balance is the default; it weighs size AND tone together (fre_0028, 0029; fre_005); refusing the eye a resting place (0032) is the declared energetic exception. Symmetry imposes order on a subject that has none (0030); diagonals need strict horizontals and verticals to divide against (0033, 0034 per CF-07).
- **CASE VALUE:** Balanced by the end; the umbrella's dark mass over the pair weighs against the bright wet lane.

### CA-D6 — Which orientation and aspect?

- **DEFAULT (composition_and_attention):** Choose by the scene's shapes (fre_003): a vertical frame is not itself tallness (fre_0008); a square reads strict and draws the eye inward (0009, 0010); a wide frame needs shapes that call for it (0011).
- **LIMIT (pack text):** No accepted source treats fixed 9:16 feed frames (A01/G2): every aspect and orientation claim here predates vertical-feed formats; transfer is untested.
- **CASE VALUE:** 9:16 justified by the tall lane walls and the falling rain.

### CA-D7 — How does attention travel across cuts (video)?

- **DEFAULT (composition_and_attention):** Every new shot carries new information (gote_0004) and every departure is motivated (0006); drive eye-trace by alternating frame placement (0010), keeping difficulty near the optimum (0011); composition must differ at the cut (0026) — the wipe waives it (0035). Alternatives: move attention inside one continuous shot (ms_0010; ms_002), or block with a static wide (0017). One device per beat.
- **CASE VALUE:** One continuous shot; device: blocking (the mother's entrance moves attention). No cut.

### CA-D8 — When cut criteria conflict, what is sacrificed first?

- **DEFAULT (composition_and_attention):** Murch's Rule of Six (murch_001; murch_0019): emotion 51 (0020) > story 23 (0021) > rhythm 10 (0022) > eye-trace 7 (0023) > planarity 5 (0024) > 3D space 4 (0025). Aim to satisfy all six (0031); else sacrifice upward from the bottom (0027) — higher criteria obscure failures of lower ones, never the reverse (0028). Weights hedged, intervals the point (0029); top three bind tightly (0030); 'bad' is film-relative (0011); the list serves occupying the audience's position (0032).
- **CASE VALUE:** Single shot, no cut to rank; noted that emotion (murch_0020) governs if any route inserts a cut.

### CA-D9 — Screen direction and the line?

- **DEFAULT (composition_and_attention):** Frame edges are the audience's directional reference (gos_0005); keep setups within one 180-degree arc (0010; gos_001); movement and position persist across cuts (gote_0017, 0018; gos_0011); reciprocal coverage obeys the line (gote_0056). A far-side setup is good in itself — the reversal shows only at the cut (gos_0012, contradicting 0007/0010); crossing needs a declared creative reason (0013).
- **CASE VALUE:** The mother enters from frame-left and stays left of the child; sight lines consistent.

### CA-D10 — How long may a shot hold?

- **DEFAULT (composition_and_attention):** Set length by silently describing the shot's contents; the description's time is the shot's (gote_0053). The fast-cutting norm — which the source calls alarming — is the ambient pace (0052).
- **CASE VALUE:** 6 s: 'a child alone in the rain; a woman with an umbrella rushes in and holds him' (gote_0053).

### CA-D11 — Does the camera move, and why?

- **DEFAULT (composition_and_attention):** Every move is motivated and stillness is chosen (ms_0002); an object in transit licenses a move across a location (0011); do the most with the least (murch_0015); shared success criterion: the technique goes unnoticed (ms_0018; ms_003).
- **CASE VALUE:** Camera still (ms_0002); the mother in transit supplies the motion (0011).

### DOCTRINE_DEVIATIONS

- none — every applicable default is accepted as written.

### 2a. Production parameters outside the triggered packs (brief-only; not Canon)

The `product_appearance` pack is not triggered for this Normalized Request (no product or packshot entity), so its lighting doctrine is not injected. The parameters below are the Executor's production choices on the brief alone and are attributed to nothing in Canon.

- light/mood: (scene light) Fictional source: warm street lamp upper-right; rain catches it; key agrees.
- light/mood: (scene mood) Low key, warm-on-cool; mood from light character.

## 3. text_handling

- mode: `none`

## 4. dispatch_parameters (identical for every route; route mapping only in `TEST-CASES.yaml` → `routes[].params`)

- aspect: 9:16
- duration_s: 6
- resolution: 720p
- audio: on (rain ambience only)
- reference_slots: 0

## 5. pre_dispatch_checks (the packs' CHECK lines, by id, run over the prompt before any call)

- `CA-D1-check`: Name the 1st/2nd/3rd read; each carried by exactly one dominant cue; no two cues compete for one beat.
- `CA-D2-check`: Placement is stated as a zone plus the reason for it; no placement is justified by a named ratio or grid line.
- `CA-D3-check`: The edge treatment is one of the three, named; no accidental near-tangency between a subject edge and a frame edge.
- `CA-D5-check`: Declared balanced or deliberately restless; if balanced, a grayscale check shows tonal weight agreeing with size weight.
- `CA-D6-check`: The stated aspect is justified by a named shape in the scene, not by the platform alone.
- `CA-D7-check`: Per cut, name the new information and motivation; per beat, state the one device: cut, camera move, or blocking.
- `CA-D8-check`: An imperfect cut names the bottom criteria sacrificed; never sacrifice emotion for eye-trace, planarity or 3D continuity.
- `CA-D9-check`: Screen direction and side-of-frame persist across consecutive shots, or something on screen shows the change (gos_0007), or the crossing is declared in DOCTRINE_DEVIATIONS.
- `CA-D10-check`: No shot outlasts its describable content; the stated pace names the prevailing norm it assumes.
- `CA-D11-check`: Each camera move names its motivation; unmotivated moves are replaced by stillness or a cut.
- `no-in-image-text`: the generation prompt includes an explicit no-lettering instruction and names no string; any lettering in the output is a reject (E5), never an exclusion.
- pack limit (`composition_and_attention`): Devanagari correctness criteria do not exist in Canon — never generate Devanagari glyphs; composite text deterministically.

## 6. generation_prompt (byte-identical across every route listed for this case)

```text
Vertical animated clip in a children's picture-book illustration style, painterly and flat, not photoreal, one continuous static shot, 6 seconds. A narrow old-neighbourhood lane in India at dusk in steady rain, a warm street lamp upper-right lighting the wet ground. A small boy of five or six stands alone at the centre holding his schoolbag, looking around a little worried. From the left his mother rushes in under an umbrella, kneels, and wraps him in a hug under the umbrella; he relaxes into her. Warm, gentle ending. Only the sound of rain; no speech, no music. No text, title, captions or lettering anywhere in any frame.
```
