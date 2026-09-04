# Production blueprint — AUD-TTS-02

```yaml
case_id: AUD-TTS-02
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
- `indian_indic_context` — uncompiled — language_topology_present_or_market_IN (R10; market IN for every case)
- `commercial_communication` — uncompiled — advertising_acceptance_intent (R18)

### Coverage-gap notice (verbatim, `canon/packs/pack-triggers-v0.yaml` → `coverage_gap_notice`, mandatory in every audio cell)

> CANON COVERAGE GAP: no accepted Canon source covers audio production. Canon has no doctrine for this cell — no defaults, no checks. Proceed on the brief alone, state this gap in FAILURE_PREVENTION, and do not attribute audio decisions to Canon. Closing the gap requires new source ingestion only the Controller can authorise.

**Attribution:** no decision in this blueprint is attributed to Canon. Section 2 is empty by design; section 2a lists the production parameters taken from the brief alone.

## 2. decisions (by id; DEFAULT = the pack's text; CASE VALUE = this case's filled value)

_No Canon decision applies to this cell (audio: zero packs, zero accepted sources — see the notice above)._

### DOCTRINE_DEVIATIONS

- none — every applicable default is accepted as written.

### 2a. Production parameters from the brief alone (not Canon)

- script (exact, 74 characters): Job chahiye? Toh skill upgrade karo. Aaj hi enroll करो — Kaushal Setu par.
- young male voice, energetic and motivational yet trustworthy; a little fast but every word clear
- one voice, no music bed, no effects
- pace: natural; a short pause at each sentence boundary
- fixture note: the brand name Kaushal Setu is a labelled fixture; no real business of that name is implied

## 3. text_handling

- mode: `none (audio)`

## 4. dispatch_parameters (identical for every route; route mapping only in `TEST-CASES.yaml` → `routes[].params`)

- format: wav preferred, mp3 accepted
- audio: the deliverable
- reference_slots: 0
- max_chars: 250

## 5. pre_dispatch_checks (the packs' CHECK lines, by id, run over the prompt before any call)

- no pack CHECK applies (audio cell — see the coverage-gap notice); brief-only pre-dispatch checks, attributed to nothing in Canon: the request payload's script is byte-identical to `speaker_topology.script`; ≤ 250 characters; one voice; no music bed.

## 6. generation_prompt (byte-identical across every route listed for this case)

```text
Job chahiye? Toh skill upgrade karo. Aaj hi enroll करो — Kaushal Setu par.
```
