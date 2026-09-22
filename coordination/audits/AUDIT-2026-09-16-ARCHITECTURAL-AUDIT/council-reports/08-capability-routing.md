# AGENT 8 — Model / Capability / Routing council + Capability-Lab Evaluation Scientist

Read-only audit. MI main verified at `3bb9a3c3da484e43d4d54ae20543d1d246769ac6` (`git rev-parse HEAD`). MF checked-out at `57b2cca`. Cumin evidence commit `de1f978`; PR #103 head `1de2b37`. Every count below was computed by the command shown or a script whose output is quoted; prose counts from PROJECT-MEMORY / CONTROL-STATE were not used as evidence.

Labels: OBSERVED = read from committed bytes; INFERENCE = my reading of observed facts; HYPOTHESIS = plausible, not provable from the repo; UNKNOWN = could not be established.

---

## 0. Findings ranked

1. **EVAL-037's "Canon helps" half has no committed judging evidence; only the "retrieval is immature" half is provable.** OBSERVED: no file matching `judging|verdict|blinding` exists under `EVAL-037/` on any of the 12 local/remote `eval-037-*` refs (scan command in §1.3); Canon-condition packages self-disclose treatment at package line 98 ("Canon knowledge used…"); the Sol lanes (36/144 trials) were never dispatched; the winning lane consumed 227/425 = 53.4 % HOLD (uncertified) objects. The Controller nevertheless recorded "Canon helps, but the current retrieval / consumption system is not mature" as an APPROVED conclusion (`coordination/decisions/CONTROLLER-EVAL-037-CONCLUSION-2026-08-31.md`). Honest verdict on the evidence: **inconclusive on value, conclusive on retrieval immaturity**. The outcome measure (a blind rank of *reasoning packages*, not media, not buyer acceptance) is not something a buyer cares about.
2. **EVAL-038 is a clean negative result, and its media arm (n = 2 pairs) is the only place in either Canon experiment where a human judged pixels.** OBSERVED: 0/6 briefs where weak+packs ≥ strong-alone; 18/18 top-3 slots to Sonnet NO_CANON; single reviewer (Controller abstained); B06 image pair inverted after reveal (haiku-packs won); replay of identical prompts produced worse artifacts (draw-to-draw variance flips acceptability). Controller reserved the Canon verdict to himself.
3. **The Capability Registry's 575 rows measure exactly five things, none of which a buyer accepts or rejects on.** COMPUTED (§2.3): `latency_errors_refusals` 120, `cost_and_cpao` 120, `delivery_format_compliance` 117, `reliability_pass_at_k` 117, `reproducibility` 101 — all from three deterministic instruments (`ledger_metrics` 240, `format_probe` 234, `repeat_consistency` 101). 524/575 rows rest on **one** base item; 441/575 on two trials. Of the 36 frozen capabilities in `eval/v1/capability-contract.yaml`, **31 have zero Registry rows**, including three that the freeze package itself declared deterministic-eligible (`edit_preservation`, `packaging_brand_colour_fidelity`, `audio_video_synchronisation`).
4. **Voice naturalness — the defect that rejected or delayed all three productions — was never a measured or contracted dimension anywhere in MI.** OBSERVED: `grep -c -iE 'natural|robotic' ACCEPTANCE-CONTRACTS.md` = 1 (and that hit is "natural mouth"); the three AUD-TTS contracts test transcript exactness, accent, no music, ≤ 6 s on scripts of 31–66 characters. `emotional_prosodic_fit` is a frozen capability id (contract line 1367) that appears in EVALUATOR-PLAN only as `non_registry`. MF had already recorded "raw TTS sounds robotic without speech-rhythm rewrite + mix" and "voice was the named weak link" (MFH ROUTING-PRIOR row 11; EMPIRICAL-FINDINGS B2) — and the routing map's historical tier for `sarvam-bulbul-v3` reads `no_row_for_this_route_family` (§3.2). K-codes: K1, K3, K5, K11, K13, K14 (§3.5).
5. **The runtime router reads only the Lab; MF evidence is structurally unreachable.** OBSERVED: `grep -rn historical runtime/` → 0 hits; `runtime/route/evidence.py:12-15` names TAINT-REGISTER-v1 as sole authority; the map's `historical_prior` tier is populated for 9/61 cells and the router never reads that key. The pilot's own ROUTE-ANALYSIS (case 001) says "HISTORICAL-PRIOR … none is relied on below".
6. **Production route choices cite Lab evidence when the workflow is followed (cases 001, 003) and nothing when it is bypassed (case 002); but the routes that *decided* acceptance (speech, narrated i2v, Gemini TTS) sit in cells that do not exist.** COMPUTED (§4.4): 14/24 route decisions explicitly cited a Lab cell; 6/24 used a route configuration that had no cell at all; the three routes on which each job's verdict actually turned (Sarvam long narration, Veo native narration across clips, Gemini TTS Leda) were 0/3 Lab-backed for the configuration used.
7. **Provider liquidity failed in every case and the Lab, and the only machine check that exists (fal `user_balance`) covers one of four pools.** OBSERVED: fal 403 balance lock ×7 draws in the Lab; fal USD 3.23 → 0.26 in case 001 (two slots dropped, Wan fallback dead — SD-11); fal USD 0.147 in case 003 (fal excluded); ElevenLabs `quota_exceeded` at 54 credits (att-038) after the user had *attested* the pool covered the cap; ElevenLabs Music HTTP 402; Lyria 503/500/500; Veo gRPC UNAVAILABLE ×2; Wan 2.2 HTTP 422 ×6. `runtime/execute/pools.py` takes readings and "never reads a balance itself"; the Lab harness enforces ledger caps, not balances.
8. **The Lab's Stage-A grammar produced honest, reproducible evidence and then two audits and the Controller correctly stopped widening it; the gap is not more Lab, it is that nothing the Lab measures predicts the human's verdict.** Vision judge: agreement 65.6 %, κ 0.33, false-accept 21.6 % — not qualified (QUALIFICATION-REPORT). Case 003 SYSTEM-DEFECTS tally: media-model failures reaching the human 1, pipeline failures 5, "third case in a row with the same shape: models delivered, assembly/QA/direction lost the job".

---

## 1. EVAL-037 and EVAL-038 — the Canon experiments

### 1.1 EVAL-037 — question and design (OBSERVED)

`eval/experiments/EVAL-037/experiment.yaml @ 3bb9a3c`:

- Question: "Does exposing a reasoning model to the merged status-aware Canon corpus change the production-ready creative package it returns, across four models of differing capability? EVAL-037 produces the packages and the evidence. It does not score them."
- Design: 6 briefs × 3 repetitions × 4 models (sol = gpt-5.6-sol, sonnet = claude-sonnet-5, haiku = claude-haiku-4-5-20251001, gemma = gemma-4-31b-it) × 2 conditions (NO_CANON / FULL_CANON) = 8 lanes × 18 = **144 trials**. FULL_CANON exposes `canon_catalog / canon_search / canon_read` over a 193-file corpus (accepted + HOLD + Q&A) via BM25. Explicitly out of scope: creative-quality judging, media generation, model selection.
- Supplemental (not in the freeze): `sonnet-controlled-canon`, `gemma-controlled-canon`, `gemma-required-canon`, `sonnet-full-canon-repair`.

### 1.2 What actually ran — recomputed from each lane's `result.json` (COMPUTED)

Command: for each lane `git show origin/work/eval-037-<lane>:eval/experiments/EVAL-037/runs/<lane>/result.json` → `Counter(status)`.

| lane | trials | status | lane_calculated_cost_usd |
|---|---|---|---|
| sonnet-no-canon | 18 | complete 18 | 1.138812 |
| sonnet-controlled-canon | 18 | complete 18 | 2.861148 |
| sonnet-full-canon (original) | 18 | 16 context-overflow (per REPAIR-RUN.md) | 0.412806 (floor; overflow turns unrecorded) |
| sonnet-full-canon-repair-001 (in-tree) | 18 | failed_execution 16, complete 2 | 3.228778 |
| haiku-no-canon | 18 | complete 18 | 0.331358 |
| haiku-full-canon | 18 | complete 18 | 0.400029 |
| gemma-no-canon | 18 | complete 16, format_repaired 2 | None (unpriced) |
| gemma-full-canon | 18 | complete 15, format_repaired 3 | None |
| gemma-controlled-canon | 18 | failed_required_canon_use 13, failed_technical 4, complete 1 | None |
| gemma-required-canon | 18 | failed_technical 18 | None |
| sol-no-canon / sol-full-canon | 0 | **never dispatched** (`git ls-tree origin/work/eval-037-sol-no-canon | grep EVAL-037/runs` → empty) | — |

Canon actually consumed: gemma-full-canon `canon_used` **0/18**; haiku-full-canon **3/18**; sonnet-controlled-canon returned 198 accepted + 227 HOLD objects = **53.41 % HOLD**. Recorded spend floor USD 8.372931 (A5 recompute reproduces exactly); Gemma unpriced; no committed spend authorisation for EVAL-037 (`grep -rl EVAL-037 coordination/decisions/` → only the conclusion record).

### 1.3 Judging — what exists (OBSERVED)

`CONCLUSION.md:45` states "Judging was blind to model/treatment identity and was performed independently in four streams over the production packages only." Scan run by me:

```
for b in $(git for-each-ref --format='%(refname:short)' 'refs/remotes/origin/work/eval-037-*' 'refs/heads/work/eval-037-*'); do
  git ls-tree -r --name-only "$b" | grep -iE 'EVAL-037/.*(judging|verdict|blinding)'; done   # → no output
```

No verdicts, rankings, judge identities or blinding key are committed anywhere. Package line 98 of `E037SCC-sonnet-B01-R1.txt` begins "- Canon knowledge used, all treated as directional craft guidance only (HOLD sources…" — treatment blindness was not structurally possible at package level. `canon/findings/PROPOSED-EVAL-037-EVIDENCE-ANNOTATIONS.md` (A1–A6) says the same and proposes annotations; those annotations were never applied to `CONCLUSION.md` (grep for "ANNOTATION" in CONCLUSION.md → 0).

The "results" table in CONCLUSION.md is qualitative ("Sonnet CONTROLLED_CANON leads B01/B06; NO_CANON leads B03/B04; ties on B02/B05") with no numbers.

### 1.4 What the Controller concluded (OBSERVED)

`CONTROLLER-EVAL-037-CONCLUSION-2026-08-31.md`: "Canon helps, but the current Canon retrieval / consumption system is not mature" — "sufficient to stop broad Canon-value discovery"; "does not populate the Capability Registry"; no further EVAL-037 execution.

### 1.5 EVAL-038 — question, design, results (OBSERVED, numbers from `RESULTS.md`, `CONTROLLER-EVAL-038-AUTHORISATION-AND-DISPOSITION-2026-09-01.md`)

- Question: weak model + the two compiled packs (unconditional injection) vs strong model alone.
- Design: 6 briefs × 2 reps Haiku+packs, × 2 reps Gemma+packs (USD 0.00 pinned), vs the committed 18 Sonnet NO_CANON packages (reused at USD 0). Decision rule fixed before execution: weak+packs supported on a brief only if it wins or ties strong-alone; programme support requires ≥ 3/6.
- Result: **0/6**; Sonnet NO_CANON took **18/18 top-3 slots**. Single reviewer (Controller abstained — deviation recorded). Structural compliance 24/24 (the gap is creative substance). Cheap arm cost more per package (USD 0.072 vs 0.063).
- Media (product learning only, n = 2 pairs): B06 image — after reveal both reviewers hold **M01 (haiku-packs) wins**; B01 video — V02 (sonnet) > V01, "neither is production grade", both failed on baked-in text. Replay of frozen prompts: both replays judged worse than all four originals; the replay image baked "ASTER MERIDIAN 38" into the pixels.
- Spend USD 2.260122 of a 10.00 cap.
- Controller disposition: configuration closed; "**it's my call eventually to decide whether it works or not**" — verdict on Canon reserved; no worker may draw a further conclusion.

### 1.6 Verdict for the lead

| claim | supported? | basis |
|---|---|---|
| Canon improves media outcomes | **No evidence either way.** EVAL-037 judged reasoning packages, not media; EVAL-038's media arm is n = 2 pairs, 1 reviewer, and split 1–1. | §1.3, §1.5 |
| Canon improves reasoning packages | **Inconclusive.** Uncommitted judging; Sonnet-only comparison; HOLD-majority diet; sol never ran. EVAL-038 (a different question) is a clean negative for weak+2-packs. | §1.2–1.5 |
| Retrieval interface is immature | **Supported.** Gemma 0/18 canon use; unbounded lane 16/18 overflow; required-canon 18/18 technical failures. | §1.2 |
| Buyer-relevant outcome measure? | **No.** The endpoint was a blind rank of text packages by unnamed judges. Neither experiment measured acceptance of a delivered asset. | §1.3, §1.5 |

INFERENCE: the programme has spent ≈ USD 10.6 (8.37 + 2.26, floor) on two Canon experiments and has one committed, decision-grade number about Canon: 0/6 for the weak+packs substitution. The "Canon helps" sentence in `CONTROLLER-EVAL-037-CONCLUSION` is a Controller preference recorded as a conclusion; it should be cited as such.

---

## 2. Capability Lab — EVAL-040..043

### 2.1 What the four ids are (OBSERVED, `AUDIT-2026-09-10-REPORT-A.md` §4 + `git log`)

- **EVAL-040** — the sealed run namespace (`eval/experiments/EVAL-040/runs/*`: 42 run dirs incl. smokes). The task file (`eval/tasks/EVAL-040-STAGE-A-ROUTE-ADMISSION-SCREEN.md`) is still headed "DRAFT — PENDING SPEND AUTHORISATION"; the spend records are the per-piece `CONTROLLER-SPEND-AUTHORISATION-*-2026-09-0{8,9,10}.md` files.
- **EVAL-041** — PR #91 (`b0f15f1`): Registry v1 (459 rows), image half two, video pieces 1–5, speech, music, lipsync; map RR-1..13.
- **EVAL-042** — PR #92: two-speaker/lipsync tail, RR-14 (Registry 475/480 — PR title and body disagree).
- **EVAL-043** — PR #93 (`dcfa6af`): text-to-video core RR-15, Wan 2 contender RR-16, vision-judge qualification run, Gemini routes re-pointed to the Gemini key; Registry 575.

### 2.2 Capabilities measured, n per cell, human verdicts (OBSERVED from the regenerated map, `ROUTING-EVIDENCE-MAP-v0.yaml @ 3bb9a3c`, generated 2026-09-14T03:23Z under rulings C-3/C-4/C-6b/C-6c/C-6d)

61 cells across 15 questions. Human accepts / planned trials (literal frozen rule), computed by script over the YAML:

| question | cells (route+arm → accepts/trials) |
|---|---|
| IMG-CORE | nano-banana-2 7/8 · gpt-image-2 6/8 · qwen-image-3 6/8 · seedream-5-pro 6/8 · flux-2-pro 4/8 · nano-banana-pro 4/8 |
| IMG-TEXT | flux-2-pro+code_overlay 4/4 (mechanism B, code composed the text) · gpt-image-2 4/4 · nano-banana-2 4/4 · nano-banana-pro 4/4 · qwen 2/4 · recraft 2/4 · seedream 2/4 · flux-2-pro bare plate 1/4 ELIM |
| IMG-EDIT / EXT / COMP / REF | seedream-5-pro-edit 2/4 · 2/2 · 2/2 · 4/4; flux-2-pro-edit 3/4 · 0/2 ELIM · 1/2 · 0/4 ELIM; nano-banana-pro-edit 1/4 ELIM · 0/2 ELIM · 1/2 · 1/4 ELIM |
| VID-I2V | kling-v3-pro-i2v 8/8 · wan-3.0-prime-i2v 8/8 · minimax-h3-max-i2v 7/8 · veo-3.1-fast-i2v 5/8 · wan-2.2-a14b-i2v 2/8 (6 HTTP-422 failures) ELIM |
| VID-T2V | gemini-omni-1.1-flash 8/8 · minimax-h3-max 5/8 · veo-3.1-fast 4/8 · wan-3.0-prime 4/8 · wan-2.2-a14b 4/6 · kling-v3-pro-audio 2/8 ELIM |
| VID-2SPK | veo-3.1-fast 2/2 · gemini-omni 2/2 · wan-3.0-prime 2/2 · wan-2.2-a14b 0/2 ELIM · kling-v3-pro-audio 0/2 ELIM |
| VID-MS | kling-15s 2/2 · kling-10s 2/2 · gemini-omni-10s 2/2 · veo-fast-extend 2/2 |
| VID-KNEE | veo-3.1-full 1/2 · veo-3.1-lite 0/2 ELIM · minimax-h3-max-480p 0/2 ELIM |
| VID-REF | veo-3.1-fast-ref2v 2/4 (tin 2/2, person 0/2) |
| VID-TOPO3 | H3Max i2v + C textless plate composite 2/2 · A2 NB2 plate 2/2 · A cheap plate 0/2 ELIM (×2 routes) · B native text veo-full 0/2 ELIM, kling 0/2 ELIM |
| AUD-TTS | sarvam-bulbul-v3 6/6 · elevenlabs-v3-direct 4/6 (Hinglish 0/2 accent) |
| AUD-LIP | kling-lipsync-a2v 0/6 ELIM |
| MUS | lyria 4/4 |

Taint register summary (`TAINT-REGISTER-v1.yaml` lines 293–323): clean_observed 36, directional_only 25; production_use_allowed True 29 / manual_only 15 / False 17; eliminated 17; replacement_needed 3; problems: smoke_shared_identity 13, infra_refusal_excluded 10, duplicate_dispatched_identity 6, denominator_convention_differs 3, contradictory_verdicts 2, judged_stricter_than_contract 2, redo_undeclared 2.

### 2.3 What the 575 Registry rows really are (COMPUTED over `eval/registry/registry-v1.jsonl`; 581 lines, 6 comment lines, 575 JSON rows)

```
capability:  latency_errors_refusals 120 | cost_and_cpao 120 | delivery_format_compliance 117 | reliability_pass_at_k 117 | reproducibility 101
instrument:  ledger_metrics 240 | format_probe 234 | repeat_consistency 101      qualification: deterministic 575/575
lane:        image 262 | general_video 150 | native_av 119 | tts 32 | lipsync 12
workflow:    t2i 172 | t2v 147 | i2v 108 | edit 90 | tts 24 | lipsync 12 | ref2v 10 | music 8 | extend 4
n_items:     1 → 524 rows | 2 → 51 rows        trials: 2 → 441 | 1 → 92 | 4 → 42        repeats_per_item: 2 → 474 | 1 → 101
pass_rate:   1.0 → 479 | 0.0 → 82 | 0.5 → 12 | 0.75 → 2
routing_use: hard_constraint 474 | descriptive_only 101 (the repeat-consistency rows)
surface:     fal 394 | vertex 157 | elevenlabs_direct 12 | sarvam_direct 12
34 route_keys; 20 run_ids; question ids: IMG-CORE 90, VID-I2V 88, VID-T2V 81, IMG-TEXT 77, VID-TOPO3 35, IMG-EDIT 30, IMG-REF 30, VID-2SPK 26, AUD-TTS 24, VID-MS 19, IMG-COMP 15, IMG-EXT 15, VID-KNEE 15, AUD-LIP 12, VID-REF 10, MUS 8
```

Reading: a "row" is (route × item × one of five deterministic properties). The 82 `pass_rate 0.0` rows are format probes and error-rate rows (e.g. all Lyria `delivery_format_compliance` rows fail on 32.77 s vs declared 30 s; `minimax-h3-max-i2v` reliability 0/14 is a resolution-class mismatch, not a creative failure). **No row encodes a human verdict; no row encodes any of the 31 other contract capabilities.** The `reliability_pass_at_k` column is a deterministic format/decode criterion (`PASS-CRITERIA-v0.yaml`), not "accepted k times".

Deterministic-eligible capabilities with 0 rows despite being declared eligible in EVALUATOR-PLAN: `edit_preservation` (masked diff planned on IMG-EDIT), `packaging_brand_colour_fidelity`, `audio_video_synchronisation`. UNKNOWN why — no record explains the omission.

### 2.4 USD spent (OBSERVED, `AUDIT-2026-09-10-SPEND-RECONCILIATION.md`, rebuilt from sealed ledgers)

Ledger consumed **USD 119.085109** across 39 run ledgers (+ USD 3.156153 vision-judge run, no ledger) = **USD 122.241262 counted against caps**; USD 108.970609 produced a sealed artifact; USD 10.114500 produced nothing (≥ USD 2.88 never billed — six Wan 2 HTTP-422). Pools: cash 77.5235; GCP credits 41.55224; ElevenLabs 1,198 plan credits (USD 0 equiv.); Sarvam INR 0.894. Two caps crossed (video1 10.364 vs 9.96; wan2 11.840 vs 11.53) — accepted as recorded on 14 Sep. Vendor statements **never reconciled** ("not in this repository"). By lane (registry rows, deduped by trial ids): image ≈ 12.6, general video ≈ 56.8, native AV ≈ 83.3, TTS 0.25, lipsync 1.12 — note the Registry-derived sum (≈ 154) exceeds the ledger (119); UNKNOWN whether from smoke-row overlap or my dedupe key; the ledger figure is authoritative.

Per-cell cost of the human tier: 261 verdicts / USD 122 ≈ USD 0.47 per judged artifact; 174 accepts → ≈ USD 0.70 per accepted artifact (REPORT-B Part 6).

### 2.5 Vision judge (OBSERVED, `QUALIFICATION-REPORT-2026-09-09.yaml`)

gemini-3.5-flash, 154 compared: agreement 0.6558, Cohen's κ 0.3265, false-accept 0.2157, false-reject 0.4078; IMG-CORE κ −0.07 with false-accept 0.92. Not qualified; judge v2 (C-14) unauthorised.

### 2.6 Red-team Q10 — did the Lab optimise what is easy to measure?

**Yes, by construction, and the freeze package says so itself.** Evidence:

1. The Registry admission rule is "only the 8 yes_deterministic capabilities … may write Registry rows" (`EVALUATOR-PLAN.yaml` line 5). Five of those eight actually wrote rows; all five are format/latency/cost/repeat properties (§2.3).
2. Every Stage-A case lists its creative capabilities as `non_registry_capabilities` — e.g. IMG-CORE-01: `[composition_brand_register, hierarchy_product_as_hero, physics_material_appearance]`; these were folded into a single blind accept/reject per artifact and never scored per capability.
3. The acceptance contracts themselves are written around measurable surface properties: `ACCEPTANCE-CONTRACTS.md` contains "natural" once ("natural mouth") and "robotic" 0 times; AUD-TTS-01..03 test transcript exactness, accent, absence of music, ≤ 6 s (§3.3). No contract line asks whether a voice is pleasant, a product is the hero, or a clip reads as an ad.
4. Text mechanism dominates the evidence base: IMG-TEXT 77 + VID-TOPO3 35 = 112/575 = 19.5 % of rows and 4 of 16 routing rules (RR-1, 2, 3, 6, 7) are about exact text; earlier programmes EVAL-022..030 were OCR/exact-text families and EVAL-026/032/033 temporal-perturbation instruments.
5. What rejected the three productions (§3–4): voice naturalness (001 V3, 003 rounds 1–4), voice identity across clips (002), ad structure / product hero / end card (003 V2), text over subject (001 V3, 003 V1), lips moving under VO (003 V1), pacing (001, 003). Zero Registry rows and zero contract lines cover any of these.

**Acceptance-critical capabilities with ZERO Lab evidence of any tier** (from the 36 frozen ids; "any tier" = no Registry row, no acceptance-contract line, no map question):

| capability id (contract) | Registry rows | human-tier question covering it | note |
|---|---|---|---|
| emotional_prosodic_fit | 0 | none (AUD-TTS contracts are transcript/accent) | the voice-naturalness gap |
| hierarchy_product_as_hero | 0 | none | 003 V2 "closing shot should have cumin product" |
| composition_brand_register | 0 | none | listed non_registry on every IMG case |
| hook_pacing_temporal_hierarchy | 0 | none | 001/003 pacing rejects |
| proposition_objective_fit | 0 | none | 003 "does not look like an ad at all" |
| single_speaker_lip_sync | 0 | none (only two-speaker VID-2SPK and lipsync-chain AUD-LIP) | 001 SD-08: "no Registry cell for single-speaker English native speech from an anchored still" |
| audio_video_synchronisation | 0 (deterministic-eligible!) | none | 003 DF-08 VO overlap |
| edit_preservation | 0 (deterministic-eligible!) | IMG-EDIT human only | planned masked-diff never written |
| packaging_brand_colour_fidelity | 0 (deterministic-eligible!) | IMG-EDIT-02 human only | |
| product_identity / person_identity / logo_wordmark_fidelity / typography_legibility | 0 | partly via IMG-REF / VID-REF / IMG-TEXT contract lines | human one-bit only |
| anatomy_hands / human_object_contact | 0 | "count fingers" contract lines only | 003 chopstick grip had to be micro-qualified |

INFERENCE: the Lab answered "which route returns a well-formed, cheap, repeatable file that a human accepted twice on a benchmark-shaped brief". It did not — and was never designed to — answer "which route produces something a buyer accepts as an ad". The audits (REPORT-B Part 4 items 1–2) and the Controller's C-9 stop are consistent with this.

---

## 3. Voice / TTS

### 3.1 Evidence BEFORE case 001 (OBSERVED)

**MF (July 2026), MFH `MEDIA-FACTORY-ROUTING-PRIOR.md` and `EMPIRICAL-FINDINGS.md`:**
- Row "Indic VO, cheap": Sarvam bulbul:v3 speaker "chosen by human ear … **raw TTS sounds robotic without speech-rhythm rewrite + mix**; ear beat RMS metric (ishita > kavya)"; confidence Medium (Tier B).
- Row "Directed/acted VO": ElevenLabs v3 acting tags work; "**western accent rejected by ear even in English**" (C6).
- B2: "Voiceover route was serviceable … **voice was the named weak link**"; Sarvam "not very good but not bad".
- Contradiction 4: "voice choice must be a human/brand decision, never auto-picked."
- Lip-sync ladder: LatentSync accepted as cheap talking shot, SadTalker rejected (256 px), Wan `audio_url` not a lipsync driver (C2); multi-turn dialogue → per-clip voice drift, chaining banned (C1).
- These five files were imported byte-for-byte into `eval/historical-priors/media-factory-v1/` (EVAL-039B, 2026-09-04) with `freshness_required: true` and `registry_rows_created: 0`.

**MI Lab (9 Sep 2026):** AUD-TTS-01..03 — scripts of ~31 / ~66 / ~34 characters (Hindi / Hinglish / English; computed from the contract strings); contracts test exact words, accent, no music, ≤ 6 s. Sarvam 6/6 (blind notes all empty); ElevenLabs 4/6, both rejects "rejected for accent" (premade male 'Eric'; no Indian voice on the account). RR-12: "Sarvam bulbul:v3 is the default voice route for all three". No naturalness criterion, no long-read item, no register/affect item. Lipsync chain 0/5 "looking very odd". Native two-speaker Hindi 2/2 on three routes.

**Map join:** `questions.AUD-TTS.cells['sarvam-bulbul-v3+native'].historical_prior.status = no_row_for_this_route_family` — the MF Sarvam row was not attached (52/61 cells carry no MF row at all; computed).

### 3.2 What case 001 recorded (OBSERVED, `production-learning/cases/UPWORK-INTRO-001/`)

- V3 (14 Sep): Sarvam bulbul:v3 speaker aditya, 16 calls, ≈ 1,000 characters, ~48 s of narration in a 60-s film; **16/16 verbatim on transcript**; Controller: "**voice horribly robotic**" (HUMAN-VERDICTS.yaml:46). RO-05: "long continuous narration exposes cadence that the Lab's ≤ 70-character lines did not; output not deterministic across calls".
- SD-05 root cause: "Sarvam bulbul:v3 chosen for ~48 s of continuous narration on the strength of Lab evidence gathered on ≤ 70-character lines; no long-read qualification before dependent assembly" → promoted as **SPEAKER_MICROQUALIFICATION (candidate pattern)**; Controller: "KEEP AS CANDIDATE for now" (PROMOTION-QUEUE.yaml:47–54).
- V4: speaker micro-qualified — Gemini Omni i2v+speech rejected ("timbre judged synthetic/robotic by the triage model and the executor", RO-03), Veo 3.1 fast i2v+speech accepted (RO-01), USD 4.03 before dependent spend. SD-08: "no Registry cell for single-speaker English native speech from an anchored still".
- The pilot's ROUTE-ANALYSIS.md (branch `work/pilot-upwork-intro-video-v4`) had recommended "Sarvam for Indian-English VO (default per RR-12)" and recorded the ElevenLabs account has "no Indian voice"; it named Gemini TTS as "listed on the key, UNTESTED, no adapter".
- Case 002 (15 Sep) added: Veo native narration across two independent i2v clips → two different narrator voices (RO-02); promoted CROSS_CLIP_VOICE_CONTINUITY and candidate SINGLE_VOICE_SOURCE_FOR_NARRATED_MULTI_CLIP with the note "no proven single-voice route exists today (Sarvam narration rejected in case 001 V3; ElevenLabs premade voice not Indian; native per-clip narration not identity-stable)".

### 3.3 What case 003 did (OBSERVED, `de1f978:agency/jobs/AGY-2026-09-15-CUMINCO-CHOPSTICKS-001/JOB.yaml`, `gen/ATTEMPTS.jsonl`; `1de2b37:production-learning/cases/CUMINCO-CHOPSTICKS-003/*`)

Plan: VO route "AUD-TTS/sarvam-bulbul-v3 (6/6) or AUD-TTS/elevenlabs-v3-direct (4/6) — human ear decides at micro-qualification"; `micro_qualifications[1]` = "calm, empathetic Indian-English narrator by ear … one line each, cost_usd 0.02". Pools attested by the user ("I attest all pools cover the cap").

Attempts (computed from ATTEMPTS.jsonl, 51 records): sarvam-bulbul-v3 8 ok; elevenlabs-v3-direct 7 ok + 1 http_401 (`quota_exceeded`: "54 credits remaining, 159 required", att-038); gemini-tts 17 ok + 1 `PROHIBITED_CONTENT` refusal (att-045, innocuous line); lyria 1.

Rounds (HUMAN-VERDICTS.yaml lines 18–31):
1. Sarvam priya/shreya + ElevenLabs Sarah → "we could use hidi comfoting voice. all three are robotic".
2–3. Hindi Sarvam ×4, ElevenLabs tagged ×2, Gemini TTS ×4 (Aoede/Leda/Kore/Sulafat) → "stick to english. but voices are not good. at all. why ae we not using veo models with voice? … i also dont agree on voice being an issue. eleven labs speically have vocies that feel human and so does sarvam … clam + cheerful is what we want".
4. Gemini Aoede/Leda/Zephyr/Despina + ElevenLabs Jessica/Bella (Lily = quota fail) → "leda is good. a little slower though. the shrillness and excitement is still miissing."
5. Leda v1/v2/full → "**bubbly**" → accept Leda 'bubbly'.

Totals: **26 voice takes, 5 rounds, USD 0.2947**, 4 of the job's 10 human review cycles; voice was qualified *after* plates H1/A/B were already drawn (REVISION-TRACE line 13; PROMOTION-QUEUE `VOICE_BY_EAR_FIRST`: "this job spent 5 rounds / 26 takes on it after plates were already drawn"). Final route `gemini-3.1-flash-tts-preview` has **no Registry cell, no roster row** (`grep -i tts ROSTER-REFRESH-2026-09.yaml` → only sarvam-bulbul-v3 and the fal elevenlabs rows), a job-pinned price; the job then failed on VO scheduling (DF-08 overlap 0.92 s / overrun 0.94 s) — "the voices are overlapping … reject completely".

### 3.4 Why voice consumed multiple iterations despite prior evidence (INFERENCE from the above)

1. The only structured voice evidence in MI (AUD-TTS 6/6, 4/6) measured transcript + accent on ≤ 66-character lines; the prior that said "raw Sarvam sounds robotic" and "western accent rejected by ear" lived in MF prose the router and the map never joined (`no_row_for_this_route_family`).
2. The operator in case 003 *did* read case 001 (JOB.yaml line 98 cites RO-05) and *did* micro-qualify by ear — but the micro-qualification was designed as "one line each on two routes" and the human rejected both routes outright, turning a gate into a search across a third, un-rostered provider.
3. The Controller's direction changed inside the search ("why are we not using veo models with voice" contradicts case 002's own finding; "i also dont agree on voice being an issue") — no written decision owner for "which voice route is the house default for calm-cheerful English".
4. ElevenLabs was drawn 8 times although the pilot's ROUTE-ANALYSIS (line 52) already recorded the account had no Indian voice, and the pool was attested rather than read, so the quota fault surfaced on the 8th draw.
5. No naturalness/prosody instrument exists at any tier, so every round required the human's ear — the scaling bottleneck REPORT-B named.

### 3.5 Was there a "voice micro-qualification" rule and was it followed?

- Rule status: **candidate pattern only** — `SPEAKER_MICROQUALIFICATION` (case 001, "KEEP AS CANDIDATE", promotion needs ≥ 2 more successes). The operator skill nonetheless encodes it as a non-negotiable: SKILL.md:71 "A high-risk speaker/presenter is micro-qualified before any dependent asset is built"; PRODUCTION-WORKFLOW.md §7 "Required capability with no clean cell … → micro-qualify before any dependent spend"; QA-CHECKLIST A9.
- Followed? **Case 001 V4: yes** (Omni vs Veo, one draw each, human gate, freeze). **Case 002: no** (workflow bypassed; SYSTEM-DEFECTS.yaml:16 "no … route plan existed before the first paid call"). **Case 003: partly** — planned (`micro_qualifications[1]`), run, but *after* plates and *as a five-round search*; A9 in the job's QA table stayed `NOT_RUN` at the time dependents were dispatched (JOB.yaml line 289 records A9 NOT_RUN with "micro-qualification … run next").

### 3.6 K-codes for the voice thread

| K | applies | evidence |
|---|---|---|
| K0 knowledge absent | partial | no instrument or contract for naturalness/prosody anywhere (contract id exists, never measured); Gemini TTS never evaluated |
| K1 unstructured | yes | MF "robotic without rhythm rewrite", "voice weak link", "ear beats metric" — Tier B/C prose, never a row |
| K2 retrieval failed | no | the files were on disk and indexed (PRIOR-INDEX.yaml) |
| K3 not in useful context | yes | map join `no_row_for_this_route_family` for sarvam; pilot ROUTE-ANALYSIS: "HISTORICAL-PRIOR … none is relied on below" |
| K4 ignored/diluted | partial | case 003 cited RO-05 but scoped the ear test to one line per route |
| K5 wrong reasoning | yes | SD-05 verbatim: Lab 6/6 on ≤ 70-char lines generalised to 48 s narration |
| K6 no decision owner | yes | Controller's mid-search reversal ("not using veo models with voice?", "don't agree voice is an issue") vs case 002 RO-02; no house default recorded |
| K7 self-review | no | the human judged every round |
| K8 wrong route | yes | Sarvam for calm-cheerful English; ElevenLabs with no Indian voice ×8; final route un-rostered |
| K9 model failed | yes | Sarvam cadence on long reads (RO-05, RO-04 003); Eleven accent; Gemini PROHIBITED_CONTENT false positive |
| K10 assembly failed | yes | 003 DF-08 VO overlap/overrun; 001/002 mix defects |
| K11 QA missed | yes | pilot gate transcript-only (16/16 verbatim yet robotic); no overlap gate until PR #103 |
| K12 workflow bypass | yes (002) | README:15 |
| K13 learning failed to propagate | yes | 001 SPEAKER_MICROQUALIFICATION → 003 VOICE_BY_EAR_FIRST is the same lesson re-derived, both still "candidate" |
| K14 human approval wrong level/time | yes | voice gate after plates; 5 rounds of Controller ear time on a 5-line VO |
| K15 unnecessary process | yes | 26 takes / 3 providers for ≈ 160 characters; 8 draws on a provider known to lack the required voice |

---

## 4. Did the productions use Registry / routing evidence?

### 4.1 Case 001 — Upwork intro (OBSERVED: ROUTE-OBSERVATIONS RO-01..10; pilot branch `work/pilot-upwork-intro-video-v4:pilots/upwork-intro-video-2026-09-14/preprod/ROUTE-ANALYSIS.md`, `v4/plan/ROUTE-PLAN-V4.yaml`)

The pilot wrote a full ROUTE-ANALYSIS keyed to the map: it defines CLEAN / DIRECTIONAL / REGISTRY / HISTORICAL-PRIOR tiers, cites RR-8, RR-9, RR-12, RR-14 and cells by name, uses Registry p50/p95 latency, and states historical priors are "none relied on below". ROUTE-PLAN-V4 line 7: "IMG-CORE/nano-banana-2 7/8 clean_observed (production_use_allowed: true)".

| decision | route | evidence source | cell matches configuration? |
|---|---|---|---|
| V1 stills | NB2 | Registry/map IMG-CORE 7/8 clean | yes |
| V1 presenter takes | Veo 3.1 fast i2v **+ native speech** | map VID-I2V veo 5/8 (silent) | **no** — speech-on i2v has no cell (SD-08) |
| V1 phone plate | H3 Max i2v + code text | VID-TOPO3 C 2/2 directional | yes |
| V2 presenter chain | Veo extend ×2 | VID-MS extend 2/2 directional | yes (RO-02: chain degraded) |
| V2 voice isolation | ElevenLabs free tool | none | n/a |
| V3 packshots | GPT Image 2 | IMG-CORE 6/8 clean | yes |
| V3 scene edits | Seedream 5 Pro edit | IMG-REF 4/4 clean (RR-4) | yes |
| V3 flat-lay | FLUX.2 Pro | IMG-CORE 4/8 | yes (0/1 accepted) |
| V3 motion | Kling v3 Pro i2v | VID-I2V 8/8 clean | yes |
| V3 music | Lyria | MUS 4/4 (RR-13) | yes |
| V3 narration | Sarvam bulbul:v3 | AUD-TTS 6/6 (RR-12) | **no** — ≤ 66-char items vs 48 s read |
| V4 speaker cand. A | Gemini Omni i2v+speech | none (VID-2SPK omni is two-speaker Hindi t2v) | **no** |
| V4 speaker cand. B | Veo fast i2v+speech | none | **no** |

Explicitly cited: 11/13 (the two speaker candidates were declared "no cell → micro-qualify", which is itself the correct use of the evidence). Configuration matched by a cell: 9/13.

### 4.2 Case 002 — portfolio batch (OBSERVED: ROUTE-OBSERVATIONS RO-01..06; README:15–16; SYSTEM-DEFECTS:16)

"no normalized request, blueprint, acceptance contract or route plan existed before the first paid call". Routes: GPT Image 2 (IMG-CORE cell exists), NB2 textless plate (IMG-CORE/IMG-TEXT cells exist), Gemini Omni i2v 10 s (no i2v cell for Omni), Veo t2v 8 s + extend 7 s with narration (VID-T2V veo 4/8 + extend directional; narration not covered), Veo i2v with `generateAudio` narration ×2 (no narrated-i2v cell), deterministic composition. Explicitly cited: **0/5**. Configuration matched: 2/5.

### 4.3 Case 003 — Cumin (OBSERVED: JOB.yaml `plan.assets[].route`)

Every asset carries `{cell, evidence_status, production_use_allowed, surface, pool, unit_price, fallback_cell, why, directional_notes_used}`:

| asset | route | cited cell | note |
|---|---|---|---|
| plates ×5 | NB2 + inline reference images (Gemini API) | IMG-CORE/nano-banana-2 7/8 clean; "NO registered cell for the reference-image variant — directional only (case 001 RO-04 n=2, case 002 RO-04 n=1) → micro-qualified" | configuration not covered; correctly flagged |
| clips ×5 | veo-3.1-fast-i2v 720p 6 s silent | VID-I2V/veo-3.1-fast-i2v 5/8 clean — "the only clean VID-I2V cell on credits; fal routes (Kling 8/8, Wan 8/8, H3 Max 7/8) excluded by the user" | **availability-driven**: the three better-evidenced routes were unreachable (fal USD 0.147) |
| VO | Sarvam 6/6 or ElevenLabs 4/6, ear decides | AUD-TTS cells | both rejected by ear → **gemini-tts, no cell, no roster row** |
| music | lyria | MUS 4/4 (RR-13) | yes |
| assembly | code | n/a | |

Explicitly cited: 5/5 generative decisions at plan time; the route that actually shipped VO (Gemini TTS) 0/1 Lab-backed; the i2v choice was the fourth-ranked VID-I2V route, forced by pool liquidity.

### 4.4 Fraction (COMPUTED from §4.1–4.3)

- Route decisions in the three cases: 13 + 5 + 6 = **24** (excluding code composition).
- Explicitly cited a Lab cell / RR at decision time: 11 + 0 + 5 = **16/24 = 67 %**.
- Route configuration actually covered by a Lab cell (any tier): 9 + 2 + 3 = **14/24 = 58 %**.
- Of the decisions on which each job's human verdict turned (001 V3 Sarvam narration; 002 Veo narrated clips; 003 VO route and VO scheduling), Lab-covered: **0/3**.
- Evidence sources by count: Registry/map 14; operator judgment / prior-case observation 6; availability/credits-forced 3 (003 Veo i2v, 003 Gemini TTS after Eleven quota, 001 V3 slots dropped); MF prior **0** (explicitly disclaimed in the pilot's ROUTE-ANALYSIS).

INFERENCE: the operator discipline of citing evidence is real and improving (001 → 003), but the map covers the *easy* choices (stills, silent i2v, music) and is silent exactly where the jobs failed (narration, narrated motion, voice identity, ad structure).

---

## 5. Does routing use MF + MI evidence, or only the Lab?

**Only the Lab.** OBSERVED:

- `runtime/route/CAPABILITY-EVIDENCE-BINDING-v0.yaml` `sources:` lists the routing map, taint register, policy profiles, deliverable kinds, roster, price pins, harness — no historical-prior file.
- `runtime/route/evidence.py:12-15`: "TAINT-REGISTER-v1 is the authority … The register's own reading, `production_use_allowed`: `manual_only` and `false` both stop"; `_load_cells` reads only `human_blind_acceptance` and the register entry (lines 179–190); `gate()` (237–265) checks `evidence_status`, `production_use_allowed`, and the profile's `auto_routable_evidence_status`.
- `grep -rn historical runtime --include='*.py' --include='*.yaml'` → **0 hits**; `grep -rln 'media-factory|historical-priors' runtime .claude/skills` → **0 hits**.
- The map carries a `historical_prior` tier per cell, but 52/61 cells say `no_row_for_this_route_family` and the 9 that have a row (`row_exists`, 1–2 rows) point at a markdown file, not a structured claim.
- `runtime/route/price.py` deliberately refuses the map's cost figures and prices from the roster + pins (correct); the roster has no Gemini TTS row and its `elevenlabs-v3` row still says fal (later decision re-pointed to direct).
- Policy profiles (`runtime/contracts/POLICY-PROFILES.yaml`): the release profile auto-routes `[clean_observed]` only with `fallback_required: true`; a permissive test profile lists all five statuses. Alpha-1 auto-routes 26 cells (PRODUCTION-WORKFLOW.md §7 note).
- The operator skill (`PRODUCTION-WORKFLOW.md` §7) orders: routing evidence → job requirements → surface availability → price → pool liquidity → "directional production notes as tie-breakers only". MF priors are not in the order.

INFERENCE: the strongest evidence on voice (MF, Tier B) and on single-turn talking shots (MF Wan 2.5 ear-approved) never had a path into a decision. The 5 Sep direction decision preserved "the seven settled priors are not re-proven from zero" — but no mechanism carries a prior into a cell.

---

## 6. Routing-persona answers per acceptance-critical modality (evidence from the three cases + MF)

| modality | freeze before the model runs | what the model often mutates | micro-qualify | expensive downstream failure | when one accepted draw is insufficient |
|---|---|---|---|---|---|
| **Stills with a supplied product** | packshot with embossed/moulded marks turned away or masked; copy zone declared; no legible-world surfaces in scene | embossed marks garbled ("cumin ca.", 003 DF-01); extra objects (FLUX rice bowl, 001 RO-08); paper-like text (NB2, 001 RO-04); logo floating (MF A2); Seedream leaks prompt hex codes (MF A2) | one plate per new product reference (003 MQ1 did this: r2 accepted) | every dependent clip inherits the plate; a text-clean still still yields lettered video (001 SD-06) | whenever the product has moulded lettering, hands, or a count constraint; MF takes-per-keeper 1.1–1.3 says one draw usually works *for a known character sheet*, not for a new packshot |
| **Image-to-video (silent)** | an accepted still; camera instruction ("static camera"); mouths-closed clause when faces present under VO | mouths open/speak (003 DF-03 ×2), expression drifts to angry (Lab i2v ×3 routes), signage sharpened into letters (001 RO-06), hands enter frame (001 RO-01), labels appear (H3 Max), framing widens | first clip from the frozen plate, frame-sampled (D1), before the remaining clips | clip rejected after VO/music/text are timed to it; re-draw shifts the whole timeline | any clip with a visible face under VO, any clip with background text surfaces; the Lab's 8/8 were on Controller-accepted stills only (input bias, ALPHA-1.md) |
| **Native speech in video (presenter / narrated clip)** | one voice source; script frozen; single clip per line OR one continuous take | inserted/changed words (Omni "make", 001 RO-03), voice identity differs across generations (002 RO-02, MF C1), timbre synthetic (001 RO-03), quality decays across extends (001 RO-02) | mandatory — no cell exists (001 SD-08); one line, one still, human ear + transcript | building 2+ clips on a voice that later fails identity or naturalness (002 tile 7 skipped; 001 V1/V2 USD 8.08 wasted) | always when >1 clip shares a narrator; always for extend chains |
| **TTS voice-over** | script and register frozen; speaker/style locked by ear on a full-length read at final pace; pool balance *read*, not attested | cadence on long reads (Sarvam RO-05), accent (Eleven), false-positive refusals (Gemini), silent tails/PCM format (003 RO-03), non-determinism across calls (RO-05) | ear test on the longest line at final tempo across the credited providers BEFORE plates (003 `VOICE_BY_EAR_FIRST`) | assembling around a voice the client rejects (001 V3 rejected; 003 5 rounds after plates) | one line ≠ one read: 001 passed 16/16 transcripts and failed by ear; a passing short line says nothing about a 48-s read |
| **Two-speaker / lipsync** | do not chain; ≤ 2 turns per clip (MF C1); native route, never plate+lipsync (RR-14, AUD-LIP 0/6) | wrong lips on wrong line, line bleed, per-clip voice change (MF C1), "looking very odd" (Kling lipsync) | one 8-s native beat with both lines | a dialogue film whose second clip cannot match the first | any multi-beat dialogue; Lab cells are 2/2 directional |
| **Text in motion / exact copy** | strings byte-frozen; mechanism B (code on textless plate) declared; per-frame gate | native text wrong "altogether" (Veo full, Kling 0/2), plate misspellings carried faithfully (qwen), Devanagari fabricated (Veo) | none needed for mechanism B beyond the plate; mechanism A needs the RR-2 route and a Cloud-Vision or human check | a whole spot with misspelt brand copy | never rely on one native-text draw (RR-6) |
| **Ad structure / composition** (product hero, end card, brand early, copy off subject) | blueprint check lines rendered honestly (PA-D7 was rendered "pass on a thin line", 003 SD-07); end card built by code from the brand's own photo; subject-obstruction gate per frame | not a model property — a planning/compositor property; the model will not add a product hero that the plan did not ask for | a 3-frame storyboard check by the human before any generation | the entire job (003 V2 "does not look like an ad at all") | n/a — this is not a draw question; it is a plan question, and no Lab evidence exists |
| **Music bed** | neutral prompt wording (RO-09), length trimmed by code, ducking/limiter chain | none observed on content; provider errors on wording (503/500/500), 32.8 s vs 30 s | none beyond a listen under the cut (stacked judging, RR-13) | low | one draw is fine on this evidence (Lyria 4/4 + 003 1/1) |

---

## 7. Provider reliability — every liquidity / credit / availability failure and what mechanism existed

| where | failure (OBSERVED) | mechanism that existed | used? |
|---|---|---|---|
| Lab vid-t2v | 4 fal draws refused HTTP 403 (balance lock) — counted as failures under C-3 | ledger cap only; no balance read in harness (`grep balance eval/harness-v2/adapters/*.py` → 0) | no |
| Lab aud-lip, vid-2spk | 1 lipsync draw + 2 Kling draws refused, fal balance exhausted; Controller topped up mid-round | manual top-up | human |
| Lab vid-wan2 | 6 Wan 2.2 i2v HTTP 422 (harness aspect fault), re-sent undeclared in vid-wan2-i2v; "nothing charged" yet USD 2.88 ledgered | none — re-send by hand; RR-16 later withdrawn (C-6b) | no |
| Lab img-r1 | network outage on first sendings of flux/gpt/qwen → img-r1-redo | manual redo | human |
| Lab aud-music-eleven | ElevenLabs Music HTTP 402 (free plan) — route skipped | none | — |
| Lab vid-ref / vid-ms | Vertex ref2v refuses 6 s (8 s only); Omni caps 10 s (15-s row refused by planner) | planner refusal (good) | yes |
| Lab lyria | response key `bytesBase64Encoded` ≠ pinned `audioContent` | adapter tolerance added same day | patched |
| Case 001 V3 | fal cash USD 3.23 → 0.26: B3 and Kora motion slots dropped, Wan fallback "structurally dead"; cap INR 2,000 was 6× the real constraint (SD-11) | none at the time → `runtime/execute/pools.py` PoolLiquidity written afterwards ("never reads a balance itself") | no (post-hoc fix) |
| Case 001 V3 | Lyria 503/500/500 on the frozen prompt; neutral rewrite succeeded | none; counted conservatively as spend | manual |
| Case 001 V4 | 2× Veo gRPC 14 UNAVAILABLE before the accepted take | classified infrastructure_transient (`runtime/execute/provider_errors.py`) | yes (classification only) |
| Case 002 | "no infrastructure error occurred" | none needed | — |
| Case 003 plan | fal cash USD 0.1470175 read via `GET rest.alpha.fal.ai/billing/user_balance` (`tools/dispatch.py balance`, line 442) → fal excluded, Seedream/Kling/Wan plan superseded | job-local balance command (fal only) | **yes — the one working example** |
| Case 003 VO | ElevenLabs `quota_exceeded` at att-038 ("54 credits remaining, 159 required") after user attestation "all pools cover the cap" | attestation accepted as A7 PASS; no ElevenLabs balance read (`GET /v1/user/subscription` exists — the pilot ROUTE-ANALYSIS used it on 14 Sep) | no |
| Case 003 VO | Gemini TTS `PROHIBITED_CONTENT` false positive on an innocuous line (att-045) → regenerated att-048 | provider_refusal classified, not retried; regenerated as new attempt | yes |
| Case 003 dispatch | duplicate attempt id att-019 (two concurrent processes, line-count ids) | none → alias line; candidate ATTEMPT_ID_LOCK | no |
| Runtime | `decision.py` declares a fallback with named triggers `[provider_refusal, timeout, gate_fail, capability_unsupported]`; `PoolLiquidity` marks attempts funded/not/unknown | exists in dry-run only; "live dispatch is not wired" (ALPHA-1.md) | never exercised live |

INFERENCE: across three jobs and the Lab, liquidity was read by machine exactly once (fal, case 003) and that reading changed the plan. Three of four pools (Vertex, Sarvam, ElevenLabs) have never been machine-read before dispatch; ElevenLabs failed on attestation within 45 minutes of it. The Lab's `spend authority ≠ provider liquidity` lesson (SD-11) was encoded as a class that requires a reading it cannot take.

---

## 8. Open questions / unknowns

1. UNKNOWN: who the "four independent blind judgment streams" of EVAL-037 were and where their verdicts are — nothing is committed; the Controller decision rests on them.
2. UNKNOWN: why `edit_preservation`, `packaging_brand_colour_fidelity`, `audio_video_synchronisation` — declared deterministic-eligible — wrote 0 Registry rows.
3. UNKNOWN: the Registry-derived generation cost (≈ 154 deduped by trial id) vs ledger consumed (119.09) — the cause of the gap (smoke rows, my dedupe key, or double-counted trials) was not resolved; the ledger figure is authoritative.
4. UNKNOWN: vendor-billed totals for the Lab and all three productions — no statement filed anywhere.
5. UNKNOWN: whether the Controller's "why are we not using veo models with voice?" (003 round 2–3) is a standing direction; it contradicts case 002 RO-02 and no decision record resolves it.
6. UNKNOWN: whether Gemini TTS (the only voice the human accepted) will be rostered/pinned; today it is a job-local price and no cell.
7. HYPOTHESIS: the OPEN-3 question (same bytes judged twice in img-r1 / img-r1-composite) remains factually unresolved per the 14 Sep record.

---

## 9. Commands used (reproducible, read-only)

- Registry counts: python over `eval/registry/registry-v1.jsonl` (lines starting `{`), Counters on capability / lane / route_key / instrument_id / n_items / trials / pass_rate / question; dedupe on (run_ref, cell_item_ids, route_key, arm, trial_ids).
- Map cells: `yaml.safe_load('eval/capability-map/ROUTING-EVIDENCE-MAP-v0.yaml')` → `questions[*].cells[*].human_blind_acceptance.{accepts,trials,refusals_or_errors,eliminated}`, `historical_prior.status`.
- Taint summary: `sed -n '293,324p' eval/capability-map/TAINT-REGISTER-v1.yaml` + yaml Counters.
- EVAL-037 lanes: `git show origin/work/eval-037-<lane>:eval/experiments/EVAL-037/runs/<lane>/result.json`; judging scan as in §1.3.
- Cumin attempts: `git show de1f978:agency/jobs/AGY-2026-09-15-CUMINCO-CHOPSTICKS-001/gen/ATTEMPTS.jsonl` → Counter((route_cell,status,verdict)).
- Runtime: `grep -rn historical runtime`; `grep -n -E 'auto_routable|fallback_required' runtime/contracts/POLICY-PROFILES.yaml`.
- Contracts: `grep -c -iE 'natural|robotic' eval/empirical-planning/STAGE-A-FREEZE-2026-09/ACCEPTANCE-CONTRACTS.md`; `grep -n -E '^\s*- id:' eval/v1/capability-contract.yaml`.
