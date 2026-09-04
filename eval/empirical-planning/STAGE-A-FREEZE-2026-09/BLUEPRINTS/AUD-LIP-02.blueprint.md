# Production blueprint — AUD-LIP-02

```yaml
case_id: AUD-LIP-02
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

### Coverage-gap notice for the audio half of this cell (verbatim, `canon/packs/pack-triggers-v0.yaml` → `coverage_gap_notice`)

> CANON COVERAGE GAP: no accepted Canon source covers audio production. Canon has no doctrine for this cell — no defaults, no checks. Proceed on the brief alone, state this gap in FAILURE_PREVENTION, and do not attribute audio decisions to Canon. Closing the gap requires new source ingestion only the Controller can authorise.

**Attribution:** the speech-to-mouth transform and every audio parameter below come from the brief alone and are not attributed to Canon. Only the three composition decisions in section 2, which concern the untouched video plate, cite compiled doctrine.

## 2. decisions (by id; DEFAULT = the pack's text; CASE VALUE = this case's filled value)

### CA-D11 — Does the camera move, and why?

- **DEFAULT (composition_and_attention):** Every move is motivated and stillness is chosen (ms_0002); an object in transit licenses a move across a location (0011); do the most with the least (murch_0015); shared success criterion: the technique goes unnoticed (ms_0018; ms_003).
- **CASE VALUE:** No camera move is added; the supplied clip's stillness is kept (ms_0002).

### CA-D1 — What reads first, second, third?

- **DEFAULT (composition_and_attention):** One dominant element by contrast — visual power is achieved by contrast, not 'impact' (vig_0009); eyes attract more strongly than probably any other subject (fre_0020); competing cues confuse rather than direct (repeated focus-shifting is the type case, ms_0019); complete control of attention is self-defeating (murch_0018); misdirection (murch_0033) is the scoped exception, only to set up a reveal.
- **CASE VALUE:** The 1st read must remain the face; the transform may not introduce a new cue (a mouth region that flickers or shifts tone competes with the eyes, ms_0019).

### CA-D3 — How does the frame hold the subject at its edges?

- **DEFAULT (composition_and_attention):** One edge treatment per shot (fre_002): tight fit with a slight deliberate gap (fre_0006); busy scene, edges stop mattering (0005); deliberate halving of a symmetrical subject (0007). Straight subject edges near frame edges read magnetic (0003); thin any bright framing element (0004).
- **CASE VALUE:** Framing unchanged; no re-crop of the plate.

### DOCTRINE_DEVIATIONS

- none — every applicable default is accepted as written.

### 2a. Production parameters from the brief alone (not Canon)

- plate: the Controller-accepted VID-I2V-02 clip (6 s, one man, static camera) — one plate held constant across all three lipsync cases so that the drive language is the only variable; for TOPO-01 the plate's subject (a young man in a lobby) differs from arm A's farmer in a field — the spoken line and the brief shape (one visible Hindi speaker, one line) are the same; the subject difference is recorded as the residual confound (Auditor AF-2)
- drive: drive = repeat 1 of ElevenLabs v3 for this script (frozen rule; the Controller may choose Sarvam in the morning — decision 9); the same drive file is held constant across both lipsync routes
- drive script ≤ 70 characters (≈ ≤ 5 s spoken) so the line ends inside the 6-s plate and the after-line silence is judgeable (AF-4); this script: 70 characters
- no speaker mask supplied (one face)
- output audio = the drive, unchanged; video = the plate with the mouth region re-synthesised only

## 3. text_handling

- mode: `none`

## 4. dispatch_parameters (identical for every route; route mapping only in `TEST-CASES.yaml` → `routes[].params`)

- aspect: as the clip
- duration_s: 6
- resolution: as the clip
- audio: the supplied drive, muxed unchanged
- reference_slots: 2 (clip + audio)

## 5. pre_dispatch_checks (the packs' CHECK lines, by id, run over the prompt before any call)

- `CA-D11-check`: Each camera move names its motivation; unmotivated moves are replaced by stillness or a cut.
- `CA-D1-check`: Name the 1st/2nd/3rd read; each carried by exactly one dominant cue; no two cues compete for one beat.
- `CA-D3-check`: The edge treatment is one of the three, named; no accidental near-tangency between a subject edge and a frame edge.
- `no-in-image-text`: the generation prompt includes an explicit no-lettering instruction and names no string; any lettering in the output is a reject (E5), never an exclusion.
- pack limit (`composition_and_attention`): Devanagari correctness criteria do not exist in Canon — never generate Devanagari glyphs; composite text deterministically.

## 6. generation_prompt (byte-identical across every route listed for this case)

```text
Lip-sync the supplied voice onto the supplied clip. The man's mouth must move with the words "Job chahiye? Skill upgrade karo. Aaj hi enroll karo, Kaushal Setu par." in time and shape; when the voice is silent his lips rest closed. Change nothing else: face, hair, background, framing and timing of the clip stay exactly as supplied.
```
