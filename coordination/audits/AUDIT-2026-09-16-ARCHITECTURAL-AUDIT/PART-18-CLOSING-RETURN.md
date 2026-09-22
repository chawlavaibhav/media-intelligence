# PART 18 — CLOSING RETURN

Per the commission's stop condition. The audit is complete as a read-only artefact; nothing was implemented, no PR was opened, no provider was called, no money was spent, no Controller state was modified. The folder is uncommitted in the `main` working tree; committing it (and where) is the Controller's decision. Completion date: 2026-09-20 (commissioned 2026-09-16; the folder keeps its original name).

## 1. Audit location

`coordination/audits/AUDIT-2026-09-16-ARCHITECTURAL-AUDIT/` in `/Users/vaibhavchawla/Vaibhav_Personal_Projects/media-intelligence` (untracked). Contents: `README.md`, `PART-01` … `PART-18`, and `council-reports/` (17 files: the agent-rules preamble, 15 council reports, the raw marketplace-case extract). Warning repeated from the README: the `/media-agency` workflow §0 refuses to start on a dirty tree — commit or move this directory before the next job.

## 2. Agents and personas used

Sixteen subagent councils were commissioned; thirteen wave-one councils and two wave-two councils (Canon Prosecutor, Canon Defender) completed their reports. The sixteenth (requirement-model builder, personas 6/13/36/38/39/40/61) was stopped by the Controller before writing; Part 9 was written by the lead from the councils' evidence. Parts 6–18 were written by the lead alone, without further agents, at the Controller's instruction.

| Council | Personas (commission numbering) | Report |
|---|---|---|
| 1 Project Archaeologist (MI) | — | `01-archaeology-mi.md` |
| 2 Media Factory Archaeologist | — | `02-media-factory-priors.md` |
| 3 Customer / Commercial | 1–6, 70 | `03-commercial-council.md` |
| 4 Case 003 forensic | 73, 74 | `04-case-003-cumin.md` |
| 5 Cases 001/002 + Recurrence | 73, 74 | `05-cases-001-002-recurrence.md` |
| 6 Canon / Retrieval / Ontology | 47–50, 55, 57 | `06-canon-retrieval.md` |
| 7 Q&A corpus (+ 53/54 consulted) | 56 | `07-qa-corpus.md` |
| 8 Model / Capability / Routing + Lab scientist | 41–46, 58 | `08-capability-routing.md` |
| 9 Runtime / Operator / Context-window | 36–40, 51, 57, 28, 35 | `09-runtime-operator-context.md` |
| 10 Evaluation / Production-learning / Memory | 52, 58–63 | `10-learning-evaluation.md` |
| 11 Adversarial Simplicity + Economics | 64–72, 75 | `11-adversarial-economics.md` |
| 12 Craft Jury (on the media) | 7–35 | `12-craft-jury.md` |
| 13A External research: context, RAG, memory, SLM, roles, checklists | 49, 51–54 | `13a-external-research-context-memory.md` |
| 13B External research: agency practice, platforms, pipelines, TTS | 12–20, 36–40 | `13b-external-research-agency-pipelines.md` |
| 14 Canon Prosecutor | 76 | `14-canon-prosecutor.md` |
| 15 Canon Defender / failure-to-consume | 77 | `15-canon-defender.md` |
| 16 Requirement-model builder | 6, 13, 36, 38–40, 61 | stopped; see Part 9 |
| Lead | — | Parts 1–18; adjudication in Part 12 |

## 3. Major evidence inspected (all read-only; refs verified by `git rev-parse` / `git show`)

- **MI** `main @ 3bb9a3c3da484e43d4d54ae20543d1d246769ac6` (899 commits, 5,288 files, 1.11 M markdown words): `coordination/` (CONTROL-STATE, 117 decisions, audits), `canon/` (37 sources, 1,300 SK, 291 bindings, ontology, 2 packs, trigger table, gate, 1,028 Q&A, context spec), `runtime/` (97 py, loop, compositor gates, route, canon lookup, contracts, dry battery), `eval/` (Registry 575 rows, routing map 61 cells, taint register, EVAL-037/038/040–043 ledgers and results, historical priors), `.claude/skills/media-agency*` (all files), `production-learning/cases/*` (001, 002 on main; 003 on PR #103), `UP`-facing docs.
- **PR #103** `work/agency-sync-2026-09-16 @ 1de2b37` (OPEN): case 003 files, `check_vo_schedule` + tests.
- **Cumin job** `work/agency-job-cuminco-chopsticks-001 @ de1f978` (1,403 files): JOB.yaml, brief.job.json, LEARNING-PACKET, LEDGER/ATTEMPTS jsonl, prompts and gate reports, plates/clips/VO/finals (V1/V2/V3, 9:16/4:5/1:1) — frames sampled and looked at; audio re-measured.
- **Case-001 branch** `work/pilot-upwork-intro-video-v4` (`7629894` V1 … `f6ca66f` head): CANON-BRIEF, COMMERCIAL-BRIEF, ROUTE-ANALYSIS, per-version tools and films (V1–V4.1), V3/V4 frames.
- **Case-002 branch** `work/upwork-portfolio-samples-2026-09-15 @ b4b77fa`: batch tools; exported tiles (UPM on disk; UPT `@ f236c54`).
- **EVAL-037 lane branches** (12 refs): `result.json` per lane; 36 Sonnet packages extracted and counted.
- **Media Factory** `@ 57b2cca` (spike) / `7279ec5` (main) / unmerged `fix/legible-ad-composite`; **MFH** bundle (five files, byte-identical to MI's import); MF `.env` present and **not read**.
- **upwork-project** `@ ff06dab`: PROFILE, LOG, ACCOUNTABILITY, BENCHMARKS, research, all proposals.
- **Local priors declared, not silently included**: 28-Aug OS and project-head reviews; `rentok-ad`; Aight gallery; the MF Claude memory file (Tier C only). `voice-workshop-agent` excluded as unrelated.
- Media cited by sha256 in Part 6 §0 and council 12 §0.

## 4. External research sources (primary unless marked)

Context/RAG/memory/roles/checklists (council 13A): Liu et al. 2023 (Lost in the Middle); Levy et al. ACL 2024; Hsieh et al. RULER 2024; Modarressi NoLiMa ICML 2025; Chroma Context Rot 2025; Du et al. 2025; Jaroslawicz IFScale 2025; Martin & Roger Classifier Context Rot 2026; Wallace et al. Instruction Hierarchy 2024; Mu et al. RuLES 2023; Jang et al. negated prompts 2023; Anthropic engineering posts (context engineering Sep 2025; Agent Skills Oct 2025; contextual retrieval Sep 2024; building effective agents Dec 2024; multi-agent research system Jun 2025; prompt-caching and long-context docs); Manus 2025; Zhang et al. ACE 2025; Cuconasu et al. SIGIR 2024; Mem0 2025 (PDF-verified); Hajimiri et al. 2026; GraphRAG 2024 / GraphRAG-Bench 2026; Min et al. 2022; Hu et al. ICML 2024; LEAP 2024; RICP 2024; Chain-of-Verification 2023; Constitutional AI 2022; TICK 2024; CoALA 2023; Reflexion 2023; Voyager 2023; ExpeL 2024; AWM 2024; Dynamic Cheatsheet 2025; Memp 2025; ReasoningBank 2025; Dixit et al. Honest Lying 2026; Ovadia et al. 2023; Gekhman et al. 2024; LIMA 2023; Cobbe et al. 2021 (PDF-verified); CriticGPT 2024; Panickssery et al. 2024; Preference Leakage 2025; MLLM-as-a-Judge 2024; Rubrics as Rewards 2025; RLCF 2025; RocketEval 2025; CheckEval 2024; SetFit 2022; Shumailov et al. Nature 2024; Huang et al. ICLR 2024; Stechly/Kambhampati 2023–25; Kamoi et al. TACL 2024; Khan et al. ICML 2024; Smit et al. ICML 2024; MAST 2025; Cognition 2025/26; Haynes NEJM 2009; Pronovost NEJM 2006; Urbach NEJM 2014; Degani & Wiener 1993; Gawande 2009.

Agency practice / platforms / pipelines / TTS (council 13B): Julian Cole GET/WHO/TO/BY 2021; textbook brief syntheses (Burtenshaw 2011, O'Guinn 2011, Butterfield 1999 via Wikipedia); Ogilvy brief template (secondary); Binet & Field IPA 2013; Ehrenberg-Bass / *Int. J. Advertising* 2026; Mercer Island Group tissue session 2024; Dalim 2026 (secondary); Google ABCD playbook (Ipsos/Nielsen/Kantar) and Think with Google 2022; Meta Ads Guide (Reels safe zone) and Advantage+ help; TikTok Creative Codes 2023 PDF and video specs; System1 × TikTok 2025; Kantar attention 2023 and pre-testing 2022; Digiday 2016 (secondary); Google Ads Help specs/Shorts; Wikipedia Animatic (Brine 2020); Williams Animation Apprentice 2020; Frame.io editing stages; AICP Standard Commercial Production Agreement; Yamdu PPM; EBU R 128 v5 and s1 v3 (PDFs); Netflix spec via Production Expert 2022 (secondary); WCAG 2.1 SC 1.4.7; Ricketts 2024; MagicBrief QA checklist 2025; Pencil / Omneky / AdCreative.ai (marketing pages only); Google Ads asset generation help; VideoDirectorGPT 2023; Anim-Director 2024; StoryAgent 2024; FilmAgent 2025; MovieAgent 2025; MM-StoryAgent 2025; ViMax 2026; Veo 3.1 API docs; Kling Element Library; Runway Gen-4; fal Workflows; Higgsfield 2026; Morphic; Artificial Analysis Speech Arena Aug 2026; Sarvam Bulbul V3 2026 (vendor); Menta PSP benchmark 2026; ElevenLabs / Gemini TTS / Sarvam docs; Bachar et al. AAMAS 2026; learning-to-defer surveys (search-only).

## 5. Five strongest findings

1. **Nothing converts knowledge into a challenged decision before money moves.** One session played 15 roles and rendered 21 Canon check lines "pass" including PA-D7 on a film with no product hero; `reviews: []`; the personas the workflow names do not exist; 46 of 46 defects across three cases were found by the human, 3 by gates. OBSERVED (`de1f978:…/JOB.yaml` L157, L173, L326; grep; three SYSTEM-DEFECTS files). Confidence HIGH.
2. **Approval was taken at the wrong altitude in every case.** Cumin: five strings and a cap at 13:28Z; plates and clips bought during voice rounds; timeline fixed before VO existed; proposition first challenged at V2 after USD 5.08 of 5.09. 001: decisive corrections after USD 8.08 and 3.28. No storyboard in any job; 8 of 12 Cumin defects were visible on accepted plates, contact sheets, a prompt string or timeline arithmetic before any clip was bought. OBSERVED (ATTEMPTS.jsonl; council 12 §1.5). HIGH.
3. **Knowledge is routed by compile policy, not by need — and the policy is self-sealing.** `commercial_communication` fired on the Cumin NR and was excluded by five separate blocks (C-10, `packs.py` continue-on-gap, `doctrine.py` and the compiler hard-coding two packs, WORKFLOW §4 "proceed on the brief… record the gap only after the production fails"); 0.63 % of Canon bytes reachable; the two compiled packs are Canon's own two lowest-demand; MF priors imported byte-identical and read by nothing on the production path. Once the human named it, the operator applied ABCD correctly in one pass at USD 0. OBSERVED. HIGH on mechanism.
4. **The learning loop is bookkeeping.** `check_case.py` ≈ 30 schema / 0 substance checks; eight case-001 gates exist as code with no mandatory caller; case-002 learnings are prose; case-003's promoted gate has 0 callers; candidates re-derived under new names (SPEAKER_MICROQUALIFICATION → VOICE_BY_EAR_FIRST); ten recurring defect classes, one prevented; every class had a Media Factory analogue from July. OBSERVED. HIGH.
5. **The evaluation programme measured what is easy and the commercial promise runs ahead of it.** 575 Registry rows = five deterministic properties; 31/36 capabilities 0 rows; 0/3 acceptance-turning routes Lab-covered; "Canon helps" has no committed judging artefact; EVAL-038 is the one decision-grade number (0/6). Upwork sells 24 h / 4 h with no clock in the runtime, VO as standard with no accepted route, product-photo-in-scene never done with a customer photo; revenue USD 0; break-even needs ≤ 1.7 owner-hours/job against 1–8 observed. OBSERVED. HIGH on facts, LOW on the dollar economics.

## 6. Five strongest disconfirming findings

1. **Knowledge is genuinely absent for two of the six Cumin failure classes** (text-over-subject obstruction; voice casting/register): 0 hits across 1,300 SK and 1,191 terms; audio has zero sources. No consumption fix touches these; they are gates and empirical notes. OBSERVED.
2. **Knowledge in context did not bind either.** 001's CANON-BRIEF carried "open tight", "seller mark in the opening beat and the last frame", "end on the package", 4.5:1 contrast — by id, before V1 — and the opening was rejected twice and V3 drew "HUMAN-CHECKED" over the dal photo. Retrieval fixes without a challenge step reproduce this. OBSERVED.
3. **The models are not the bottleneck and Sonnet without Canon was competitive or leading** in both experiments (EVAL-037 per-brief 2/2/2; EVAL-038 18/18 top-3); 3/46 defects were model failures. OBSERVED.
4. **The bypassed job had the best numbers.** Case 002 (workflow skipped, no bookkeeping) reached 1 h 07 m and USD 0.52/tile; conformant case 003 failed three times. Adding process to fix process is not supported at n = 3. OBSERVED.
5. **The single judge is unmeasured and moved within one job** ("all three are robotic" → "I don't agree on voice being an issue"; "why not Veo with voice" against 002 RO-02). No inter-rater reliability exists; every production verdict and both Canon experiments' media arms rest on him. OBSERVED; consequence UNKNOWN until E6.

## 7. Unresolved disagreements between agents

| # | Disagreement | Positions |
|---|---|---|
| 1 | K-coding of the Cumin tutorial failure | Council 04: K6/K7/K14, "not K0/K2" · Council 06: compile-policy (rung 2) · Council 10: K2/K3 mis-diagnosed as K0 · Council 15: rung 2 by policy with rung 5 waiting behind it · Council 14: the prior had it; retrieval moot. **All agree it is not K0.** Lead's ruling (Part 12 §2): K2-by-policy *and* K7/K14, both necessary. |
| 2 | Would a compiled `commercial_communication` pack have changed V1? | Councils 04, 06, 14: a 22nd self-pass · Council 15: least likely of five remedies but not certain (CONTROLLED_CANON B01 adopted "early and throughout" when the source was in context). HYPOTHESIS both ways. |
| 3 | Does a strong LLM supply ad structure unaided? | Council 14 (and 11, 04): yes on the coarse spine · Council 15: coarse yes, brand-early no (0/3 B01), and the Cumin operator (same family) did not. Lead: 15's narrower claim is the observed one. |
| 4 | Is EVAL-037 evidence for Canon? | Council 08/14: inconclusive, uncommitted judging, treatment self-disclosed · Council 15: per-brief 4/6 ≥, provenance gap not disproof. |
| 5 | What Canon contributed to the accepted Cumin plates | Council 14: co-owned with the Lab's mechanism B and baseline craft, no ablation · Council 15: "injected → fine, uncompiled → rejected" is consistent with "compile". |
| 6 | Whether the 001 CANON-BRIEF informed V1 (the "natural control") | Council 15 leans yes; commit order inside `7629894` unchecked (Part 13 R11). |
| 7 | Cost of Canon | Council 14: 18 % of commits and decision prose, 1.29 M words · Council 15: the cheap parts are cheap, extraction is sunk. Both OBSERVED; different frames. |
| 8 | The economics | Council 11's −USD 440/month at 10 jobs rests on USD 35/h owner time and 3 h/job (inferred); owner minutes are not recorded in any case. |
| 9 | Media Factory duplication in Lab dollars | Council 02: USD 15–25 of 119 (HYPOTHESIS on the "settled half" of i2v); council 08 treats the Lab's i2v ranking as new information. |
| 10 | Whether Q&A is a better substrate | Council 07: reading-comprehension corpus, 1.5 % production-shaped · Council 15: the ~15 items are the most transferable form in Canon. Lead: both, at different scales (Part 7 §7). |

## 8. What evidence would resolve them

| Disagreement | Resolving evidence (Part 16 id) |
|---|---|
| 1, 2 | **E4** (fresh-context reviewer replay: does a non-author with the checklist catch PA-D7/CF2/D11/D14?) and **E1/E3** (does compiled doctrine in checklist form beat a rejection checklist?). If E4 ≥ 50 %, K7 dominates; if E3 g > f, the pack had value beyond the prior. |
| 3 | **E0** (Cumin brief verbatim, strong model, no repo context, ≥ 5 samples): ≥ 4/5 with end card + brand from frame 1 → the prior suffices and "proceed on the brief" was the cause; ≤ 2/5 → a required question is necessary. |
| 4 | A record action: locate or reconstruct the EVAL-037 judging streams (Part 13 R1); failing that, **E1** with committed, blinded judging supersedes it. |
| 5 | **E8** plate ablation (same prompts minus PA-D vocabulary and the no-text clause; blind pairwise). |
| 6 | Read the commit order inside `7629894` (R11). |
| 7 | Record LLM/session cost per job and per Canon lane going forward (R4); the past is unrecoverable. |
| 8 | Record owner minutes on the next job (Part 17, day 8–10). |
| 9 | Not worth resolving; both councils agree the costlier duplication was production money, not Lab dollars. |
| 10 | **E3** f_m vs f_n (checklist from human rejections vs from Q&A/eval data). |

Prerequisite for all of the above: **E6** (judge reliability). If κ < 0.4, none of the verdict-based resolutions is interpretable and the rejection checklist must be written with the judges first.

---

**STOP.** This audit ends here for Controller review. Nothing has been implemented; no implementation PR exists; Controller state is unchanged. The recommended next action is the Controller's decision D1 in Part 17, day 1.
