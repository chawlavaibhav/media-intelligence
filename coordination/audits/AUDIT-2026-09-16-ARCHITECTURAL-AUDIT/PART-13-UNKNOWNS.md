# PART 13 — INFORMATION WE STILL DO NOT KNOW

What must be tested rather than argued, and the conflicts between sources that this audit reports without harmonising. Every item is UNKNOWN unless marked CONFLICT. Each names the experiment (Part 16) or the record action that would resolve it.

## 1. Unknowns that decide architecture (test, do not argue)

| # | Unknown | Why it matters | Resolves by |
|---|---|---|---|
| U1 | Is the single human judge a reliable instrument? No inter-rater agreement exists; the judge authored every brief; his stated beliefs shifted within one job ("voices are robotic" → "I don't agree voice is an issue") | Every production verdict, both Canon experiments' media arms and any future experiment rest on him | **E6** (three judges, blind, 15 artefacts; κ) |
| U2 | Would a fresh-context reviewer with the rejection checklist have flagged what the producer self-passed (PA-D7, CF2, D11, D14)? | Cause 1 (role collapse) is the top-ranked root cause on three councils' agreement, with n = 0 experiments | **E4** (replay 8 artefacts under three reviewers) |
| U3 | Were Cumin's rejections assembly problems? Would gated re-assembly of the same accepted components (VO schedule, obstruction, edge trim) have been accepted? | Separates J (assembly) from the structural causes at USD 0 media | **E5** |
| U4 | Does a strong model given the Cumin brief verbatim and *no* repo context propose a product end card and brand-from-frame-1 unprompted (≥ 4/5 samples)? | Decides whether the tutorial failure was the prior (needs only "proceed on the brief" deleted) or needs a required question | **E0** (USD < 1) |
| U5 | Does *what* is in context matter: nothing vs oracle compiled doctrine (≤ 2.5 k tokens) vs the same content as raw excerpts vs the union of ten packs? | Hypotheses A/C/F/H; whether Canon's form or volume is the lever | **E1** |
| U6 | Does a 40-line rejection-derived checklist match oracle Canon? And does the checklist built from human rejection transcripts differ from one built from Q&A/eval data? | Hypotheses L, M/N; whether to compile the advertising pack at all | **E3** |
| U7 | Does the trigger-table lookup lose what an oracle finds, with all ten packs compiled *for the experiment only*? | Hypothesis B in its proper form | **E2** |
| U8 | Does a strong reasoning model with oracle context beat a weak one with the same? | Hypothesis D; whether the Lab's reasoning half reopens | **E7** |
| U9 | Would the Cumin plates have been worse without the PA-D lighting/finish vocabulary and the no-text clause? | The only Canon chain that reached state 7 has no ablation | plate ablation (same prompts minus PA-D vocabulary; blind judge) |
| U10 | Would the human have accepted V3's structure with clean audio? ("not at all happy with it" is global) | Whether the applied ABCD fix was sufficient for acceptance | second reviewer on V3-with-clean-audio (E5 pair) |

## 2. Unknowns about the record (resolve by reading or asking, not testing)

| # | Unknown | Where it bites |
|---|---|---|
| R1 | Who the EVAL-037 "four independent blind judgment streams" were and where their verdicts are (nothing committed on any of 12 refs) | The "Canon helps" conclusion rests on them |
| R2 | Whether the Cumin operator ever opened the pack YAML and read PA-D7's DEFAULT text (the documented path prints Q + CHECK only) | Whether the compiled form or the operator's reading failed |
| R3 | Which of the three EVAL-038 spend figures (2.26 / 2.76 / 3.96) a vendor billed; vendor statements for every pool never reconciled | All USD figures are ledger reservations at pinned prices |
| R4 | LLM/session cost of Canon extraction, compilation, bindings, ontology, Q&A lanes, and of every production job (subscription-metered, unrecorded) | The dominant real cost; CpAO numerators are provider-only lower bounds |
| R5 | Owner minutes per job (inferred from gaps and chat timestamps; 001 "not measured") | The economics in council 11 §7 |
| R6 | Exact V1 verdict time in Cumin (chat-only "15:0xZ"); whether the 2 h to the V2 clips was idle | TTAO accounting |
| R7 | Whether the V1 file the human watched is the committed blob (`versions[]` hash `0fa7df99…` ≠ blob `097e428e…`) | Evidence integrity of the case |
| R8 | Whether the Cumin human saw the 4:5 / 1:1 files or judged only the 9:16 | Whether the CF2 flags were ever seen |
| R9 | Whether `grounding_audit.py` was ever run on the Q&A corpus | "Grounded" is asserted, not measured |
| R10 | Licence status of 13 of the 17 experimental Q&A sources | Any training or redistribution use |
| R11 | Commit order inside `7629894`: was 001's CANON-BRIEF written before the V1 concept? | Council 15's "001 is the natural control" inference |
| R12 | Whether any real production ever executed `run_loop(frame_sampler=…)` or `pools.py` outside the dry battery | The runtime's claim to have been used |
| R13 | Whether the Controller ever evaluated any `promotion_condition` outside sync PRs | Cause 4 |
| R14 | Whether "why are we not using veo models with voice?" is a standing direction (contradicts 002 RO-02) | No house voice default exists |
| R15 | Whether proposal 1 (Mumbai agency, USD 1,000) was viewed; whether the "USD 120 interior test shot due 18 Sep" can be produced (no interior i2v run exists) | Commercial exposure |
| R16 | The smallest value of Upwork's catalog delivery dropdown; enforceability of the express refund | The speed promise |
| R17 | Whether a supplied *real* product photo holds within the decision-7 tolerance through Seedream/NB2 (only 2/4 on a constructed stand-in; n = 6 on a brand JPEG) | The "your product photo in a new scene" claim |
| R18 | Whether >2-turn dialogue and frame-chaining behave on current models (MF law never retested; VID-2SPK used exactly two turns) | Any dialogue film |
| R19 | Whether an accepted Hindi / Indian-English voice route exists at production length (Leda "bubbly" accepted for five short English lines only) | VO sold as standard |
| R20 | Whether PR #103 merged unchanged (if so, `check_vo_schedule` enters main with no caller and WALL_OBSTRUCTION is a candidate for the second time) | Cause 5 |
| R21 | The "10 MB tool limit" single point of failure named in the commission: no trace in any job tree or case | Treat as unverified |
| R22 | Whether any post-28-Aug incident of a worker acting on stale state occurred (none recorded) | The Governor-refresh ritual's benefit is unmeasured, not zero |

## 3. Conflicts between sources (reported, not harmonised)

| # | Conflict | Sources |
|---|---|---|
| C1 | Cumin working span: "≈ 3 h (13:17–16:15Z)" and V2 elapsed "≈ 0:35" vs ledger (V2 clips 16:59–17:00Z; V3 requested 17:47:49Z) | `TIME-AND-COST.yaml`, `REVISION-TRACE.yaml` @ 1de2b37 vs `gen/LEDGER.jsonl`, commit times @ de1f978 |
| C2 | Cumin human cycles: 10 stated vs 11–12 enumerated (18 touches) | README/TIME-AND-COST vs HUMAN-VERDICTS + ATTEMPTS |
| C3 | Cumin V1 9:16 hash: `versions[]` `0fa7df99…` vs QA row and blob `097e428e…` | `JOB.yaml @ de1f978` |
| C4 | Cumin `compose.py` comments vs render: brand mark "top-left" (rendered top-right); beat-5 mouth "closes at ~1.2 s" (frames show ≈ 2.5 s) | `tools/compose.py` vs frames |
| C5 | Sarvam behaviour has four statuses: 001 SD-05 `pipeline_failure`; 001 REVISION-TRACE `model_audio`; 003 RO-04 "model observation, consistent with RO-05"; RR-12 clean default | the two cases vs `ROUTING-EVIDENCE-MAP-v0.yaml` |
| C6 | 001 "54 paid dispatches" vs V3 PRODUCT-LEARNING "37 calls" vs V3 ledger 36 lines | case README vs pilot doc vs ledger |
| C7 | 001 `media_model_failures_that_reached_the_controller: 0` vs REVISION-TRACE coding two defects `model_generation` / `model_audio`; 003 tally "5 pipeline failures reached the human" vs 6 rows with `reached_human: true` | SYSTEM-DEFECTS vs REVISION-TRACE in each case |
| C8 | `CONTROL-STATE.md:196-199` "deterministic gates promoted into the runtime" vs the call graph (library only; no production path calls them) | CONTROL-STATE vs `grep` over `runtime/` |
| C9 | Three diagnoses of one failure family: 001 "no new Canon need was proven"; 002 "not missing Canon knowledge"; 003 "Canon gap" | the three PROMOTION-QUEUEs |
| C10 | Q&A status: README 108/920 vs CANON-CORPUS-INDEX totals 796/232 vs index per-source entries (13 contradict themselves) vs validator 26 errors vs manifest 0 | `canon/qa/canon-014/*` vs `CANON-CORPUS-INDEX.yaml` |
| C11 | Two fingerprints for the same 23 Q&A files (`1313c0ba…` vs `25ac8bbc…`) | index vs manifest |
| C12 | EVAL-038 spend: 2.260122 (CONTROL-STATE) vs 2.7601 settled vs 3.9611 reserved (ledger recount) | CONTROL-STATE §6 vs `spend-ledger.jsonl` |
| C13 | EVAL-037 spend USD 3.229 (attempt ledgers) absent from CONTROL-STATE §6; lane floor 8.372931 recomputed | councils 08, 11, 14 |
| C14 | Registry-derived Lab cost (≈ 154 deduped) vs ledger consumed (119.09) | council 08 §2.4 (ledger authoritative) |
| C15 | `pack-triggers-v0.yaml` header cites `CANON-V1-LIVE24-COVERAGE.yaml`; the live map is LIVE37 | stale citation |
| C16 | CANON-BRIEF line refs cited by councils 05/06 (L174, L185-187) vs actual (L52, L20, L65) — content held | council 15 §0 #14 |
| C17 | Skill instruction conflicts at HEAD: WORKFLOW §7 PriceBook workaround vs PR #102 fix; SKILL.md "never a one-off gate" vs §9/§10 one-off dispatcher/compositor; QA-CHECKLIST D1 "PASS by eye" vs `frame_hygiene.py` "NOT-RUN, never PASS"; PROJECT-MEMORY §7 trap 8 "no mandatory HITL" vs `acceptance.py` C-8 | council 09 §Q7 |
| C18 | UP `PROFILE.md` l.89 "delivery note lists the models used" vs QA-CHECKLIST E3 "no tool or model name in customer-visible text" | council 03 |
| C19 | UP `PLAN-2026-09-09` "Sarvam 6/6 … Use Sarvam" vs 001/003 by-ear rejections; the profile still sells Hindi/Indian-English VO on that basis | council 03 |
| C20 | Intro-video script "no presenters, no lip-sync" vs the film as made | `UP/research/2026-09-14-intro-video-script.md` vs V4.1 |
| C21 | MF `CLAUDE.md` rule 5 "NEVER ask a model to render the logo or exact brand typography" (never changed) vs the spike and MI RR-2 (native text allowed on NB2/GPT Image 2) | MF repo vs MI evidence |
| C22 | Vendor memory benchmarks: A-MEM's own gains vs Mem0's re-run; ACE (long playbooks) vs context-rot (focused context) | Part 8 |
| C23 | The three MF priors superseded by MI evidence (Veo policy refusal; LatentSync; price tiers) still read `freshness_required: true` with no "checked" field | `PRIOR-INDEX.yaml` vs Lab results |

## 4. Method limits of this audit (stated so they are not mistaken for findings)

- Counterfactual "strong baseline" completions were written by a frontier model about frontier-model behaviour (INFERENCE).
- No council could *listen*; every voice judgement is inference from transcripts, measured timing and the human's recorded ear.
- Case-002 B1 files are not on disk; pre-fix defects are taken from HUMAN-VERDICTS.
- Commit-hour buckets over-count Canon effort where sessions interleaved.
- Councils 6/7 regex counts and council 13a/13b external claims were spot-checked, not fully re-run, by the adjudicating councils (marked OBSERVED-A<n> in their reports).
- The wave-two requirement-model agent was stopped; Part 9 was written by the lead from the councils' evidence and is less granular than the commissioned version would have been.
- Nothing Nadia read off Upwork pages was verifiable from the repo (proposal counts, client spend, catalog approval).
