# PART 8 — EXTERNAL RESEARCH

Two councils performed the external research after the repository evidence was gathered (not before): 13A (context engineering, RAG, agent memory, fine-tuning/SLM/judges, role separation, checklists) and 13B (agency brief practice, platform structural guidance, pre-production review, ad QA, multimodal pipelines, TTS). Full tables with URLs are in `council-reports/13a-…` and `13b-…`. This Part keeps the load-bearing claims, each cited as source + date + one-sentence direct claim, labelled OBSERVED (stated in the cited source), OBSERVED-SECONDARY (via a third party), SEARCH-ONLY, or INFERENCE (synthesis). External research speaks to chain states 3–5 (in context → understood → changed a decision) and 8 (QA detection); it cannot prove anything about states 1–2 or 6–7 in this repository.

---

## A. Context engineering

| # | Source (date) | Direct claim | Bearing on MI |
|---|---|---|---|
| A1 | Liu et al., *Lost in the Middle*, arXiv:2307.03172 (Jul 2023; TACL 2024) | OBSERVED: performance "significantly degrades when models must access relevant information in the middle of long contexts." | The 21 CHECK lines sit ~4.6 KB inside a ~218 KB bootstrap block; the §5 blueprint table is at stage 5 of 14 (council 09 §Q7) |
| A2 | Levy, Jacoby, Goldberg, *Same Task, More Tokens*, ACL 2024, arXiv:2402.14848 | OBSERVED: reasoning drops with input length "well before reaching the models' maximum input-length capacity", with only irrelevant padding varied. | 60–80 k tokens of process/authority text precede the brief |
| A3 | Du et al., *Context Length Alone Hurts…*, arXiv:2510.05381 (Oct 2025) | OBSERVED: even with perfect retrieval "performance still degrades substantially" and persists when models attend only to relevant tokens. | Loading whole packs or more cases is not free |
| A4 | Jaroslawicz et al., *IFScale*, arXiv:2507.11538 (Jul 2025) | OBSERVED: with 500 simultaneous instructions "even the best frontier models only achieve 68% accuracy"; "bias towards earlier instructions". | 21 imperative check lines + 28 conflict rules + ~50 QA rows is the shape predicted to be ticked, not obeyed |
| A5 | Martin & Roger, *Classifier Context Rot*, arXiv:2605.12366 (May 2026) | OBSERVED: frontier monitors "miss these actions 2× to 30× more often when they occur after 800K tokens of benign activity"; partial mitigation with "periodic reminders". | A self-QA pass at the end of a long production transcript is the worst placement for detection |
| A6 | Hong, Troynikov, Huber (Chroma), *Context Rot* (14 Jul 2025) | OBSERVED: "even a single distractor reduces performance"; "significantly higher performance on focused prompts compared to full prompts." | Selection beats volume |
| A7 | Jang, Ye, Seo, *Negated Prompts*, arXiv:2209.12711 (2023) | OBSERVED: "all LM types perform worse on negated prompts as they scale" and tend to act as if given the original prompt. | "Do not make it a tutorial", "no text over faces" are the worst-handled form |
| A8 | Mu et al., *RuLES*, arXiv:2311.04235 (Nov 2023) | OBSERVED: "almost all current models struggle to follow scenario rules, even on straightforward test cases." | Prefix rules are fragile even when short |
| A9 | Anthropic, *Effective context engineering for AI agents* (29 Sep 2025) | OBSERVED: context is a "finite resource"; prompts at the "right altitude"; "just in time" loading via "lightweight identifiers"; "structured note-taking"; "specialized sub-agents … with clean context windows". | Supports metadata-first loading and clean-context reviewers |
| A10 | Anthropic, *Agent Skills* (16 Oct 2025) | OBSERVED: three-level progressive disclosure — name/description preloaded, SKILL.md on demand, linked files "only as needed"; "When the SKILL.md file becomes unwieldy, split its content." | The `/media-agency` bundle loads ~318 KB unconditionally at bootstrap |
| A11 | Anthropic, *Prompt caching* docs (accessed 16 Sep 2026) | OBSERVED: cache prefixes in order tools → system → messages; "Changes at each level invalidate that level and all subsequent levels"; cache reads 0.1× (0.025× newest). | Per-job material must sit after a stable prefix; growing JOB.yaml re-reads defeat caching |
| A12 | Manus, *Context Engineering for AI Agents* (18 Jul 2025) | OBSERVED: "KV-cache hit rate is the single most important metric"; recite objectives "into the end of the context"; "The more uniform your context, the more brittle your agent becomes." | Late recitation of the live checklist |
| A13 | Zhang et al., *ACE*, arXiv:2510.04618 (Oct 2025; ICLR 2026) | OBSERVED: summarisation causes "brevity bias" and iterative rewriting "context collapse"; itemised playbooks updated incrementally give "+10.6% on agents". | Conflict with A6: reconciled by selectivity per task, not volume |

INFERENCE (A): degradation is monotone in length, worst for lexically dissimilar needles, worst in the middle, and caused by length itself. Vendor guidance converges on a stable cacheable prefix, metadata-first loading, task material late or recited, and externalised notes.

## B. Retrieval

| # | Source (date) | Direct claim | Bearing |
|---|---|---|---|
| B1 | Anthropic, *Contextual Retrieval* (19 Sep 2024) | OBSERVED: contextual embeddings + BM25 + reranking cut top-20 retrieval failure "by 67%"; "If your knowledge base is smaller than 200,000 tokens … you can just include the entire knowledge base in the prompt." | The ~30 ABCD claims that matter fit in context; the 7 MB corpus does not |
| B2 | Cuconasu et al., *The Power of Noise*, SIGIR 2024, arXiv:2401.14887 | OBSERVED: highest-scoring but not-directly-relevant documents "negatively impact the effectiveness"; random documents can improve accuracy "by up to 35%". | Near-miss doctrine chunks are actively harmful; EVAL-037's 53 % HOLD diet |
| B3 | Chhikara et al., *Mem0*, arXiv:2504.19413 (Apr 2025; verified from PDF) | OBSERVED: on LOCOMO a full-context method "still achieves the highest J score (approximately 73%)"; strongest RAG ≈ 61 %. | Chunked retrieval loses to whole-document context when the corpus fits |
| B4 | Hajimiri et al., *Budget-Constrained Study of Web Agents*, arXiv:2606.15017 (Jun 2026) | OBSERVED: a token-matched vanilla baseline "matches or surpasses all three augmentation methods". | Memory/skill modules can be net-negative once their tokens are charged |
| B5 | Edge et al., *GraphRAG*, arXiv:2404.16130; *GraphRAG-Bench*, arXiv:2506.05690 (ICLR 2026) | OBSERVED: GraphRAG "underperforms vanilla RAG on single-hop … 13.4% lower accuracy", excels on multi-hop; LLM-built graphs incur "significant token costs". | The 0/422 cross-source ontology would need this to pay off; no evidence it would |
| B6 | Min et al., *Rethinking Demonstrations*, EMNLP 2022 | OBSERVED: "randomly replacing labels in the demonstrations barely hurts"; format and distribution matter. | Examples act through form, not lesson |
| B7 | Hu et al., *Case-Based or Rule-Based*, ICML 2024, arXiv:2402.17709 | OBSERVED: "transformers are performing case-based reasoning"; rule-following fine-tuning (recite and follow) generalises ">95%". | Rules change behaviour when recited stepwise |
| B8 | Zhang et al., *LEAP*, ICML 2024, arXiv:2402.05403; Sun et al., *RICP*, EMNLP 2024, arXiv:2407.05682 | OBSERVED: principles induced from mistakes and retrieved with similar mistakes improve GPT-4 "+7.5%" (DROP); "+22.6% relative on AQuA". | Mistake-anchored principles (e.g. `qa_abcd_0010` next to the Cumin plan) are the form that changes decisions |
| B9 | Dhuliawala et al., *Chain-of-Verification*, arXiv:2309.11495 (Sep 2023) | OBSERVED: strongest is "fully factored execution" — verification questions answered "independently so the answers are not biased". | The reviewer should not see the author's rationale |
| B10 | Cook et al., *TICK*, arXiv:2410.03608 (Oct 2024) | OBSERVED: instruction-specific yes/no checklists raise judge–human agreement "46.4% → 52.2%" and self-refinement "+7.8%". | Binary instance-level questions move both judging and generation |

INFERENCE (B): the published mechanism by which a principle changes a decision is not "read it in a prefix"; it is a question the model must answer about its draft (B9, B10), a principle attached to a retrieved similar mistake (B8), or a rule recited and applied stepwise (B7). No source shows a static abstract-principle prefix reliably changing downstream generation on unlike tasks.

## C. Long-term agent memory

| # | Source (date) | Direct claim | Bearing |
|---|---|---|---|
| C1 | Sumers et al., *CoALA*, arXiv:2309.02427 (2023) | OBSERVED: episodic / semantic / procedural long-term memories plus working memory. | MI has all three stores (Part 4); none is keyed for retrieval at job time |
| C2 | Shinn et al., *Reflexion*, NeurIPS 2023 | OBSERVED: self-critique in an episodic buffer; "91% pass@1 on HumanEval versus 80%". | Recurrence prevention *within* a task, not across jobs |
| C3 | Dixit, Kamal, Oates, *Honest Lying: Memory Confabulation in Reflexive Agents*, arXiv:2605.29463 (28 May 2026) | OBSERVED: Reflexion-style agents "store confident but incorrect interpretations … and continue acting on them"; "0 of 121 reflections mention the correct target object"; programmatic extraction of failure signals raises it "from 0% to 86%" and cuts repetition "from 0.64 to 0.10". | The LEARNING-PACKET / case free-text lessons are this form; V3 PRODUCT-LEARNING §G "zero text defects" seeded 002's defects |
| C4 | Zhao et al., *ExpeL*, AAAI 2024; Google, *ReasoningBank*, arXiv:2509.25140 (Sep 2025) | OBSERVED: insights distilled by contrasting successful and failed trajectories on the same task. | One-sided post-mortems are the weaker form |
| C5 | Wang et al., *Voyager* (2023); *Agent Workflow Memory*, arXiv:2409.07429 (Sep 2024); Fang et al., *Memp*, arXiv:2508.06433 (Aug 2025); Suzgun et al., *Dynamic Cheatsheet*, arXiv:2504.07952 | OBSERVED: executable/procedural artefacts retrieved by similarity give the large gains ("+51.1% relative" AWM; "10% to 99%" Game of 24); Memp: procedural memory "migrating … to a weaker model can also yield substantial performance gains"; explicit update/deprecate step. | Gates with callers and reusable templates are the memory form that works; prose candidates are not |
| C6 | Chroma (A6) on LongMemEval | OBSERVED: "focused" (relevant-only) history beats "full" history. | Memory *selection* helps, not volume |

INFERENCE (C): every positive cross-task result stores executable or procedural artefacts, distils contrastively, and has an update/deprecate step; the two 2026 negatives (C3, B4) are the most relevant to a system that writes "lessons" files. No study measures cross-job recurrence prevention for creative-quality failures (UNKNOWN).

## D. Fine-tuning, distillation, small models, judges

| # | Source (date) | Direct claim | Bearing |
|---|---|---|---|
| D1 | Ovadia et al., *Fine-Tuning or Retrieval?*, arXiv:2312.05934 (Dec 2023) | OBSERVED: "RAG consistently outperforms [unsupervised fine-tuning]"; LLMs "struggle to learn new factual information". | Do not fine-tune facts |
| D2 | Gekhman et al., *Does Fine-Tuning on New Knowledge Encourage Hallucinations?*, EMNLP 2024 | OBSERVED: new-knowledge examples "increase the model's tendency to hallucinate". | Same |
| D3 | Zhou et al., *LIMA*, NeurIPS 2023 | OBSERVED: "only 1,000 carefully curated prompts and responses" suffice for behaviour/format. | Procedure can be taught with ~10³ curated examples |
| D4 | Cobbe et al., *Training Verifiers*, arXiv:2110.14168 (2021; verified from PDF) | OBSERVED: verifiers give "approximately the same performance boost as a 30x model size increase" with 7.5 K problems. | A separate trained verifier beats a bigger generator |
| D5 | McAleese et al., *CriticGPT*, arXiv:2407.00215 (Jun 2024) | OBSERVED: trained critics preferred over human critiques "in 63% of cases"; critics "hallucinate bugs"; human–critic teams hallucinate less. | Trained critics add value; prompted self-critique does not (E) |
| D6 | Panickssery, Bowman, Feng, *LLM Evaluators Recognize and Favor Their Own Generations*, NeurIPS 2024 | OBSERVED: "linear correlation between self-recognition capability and the strength of self-preference bias." | The author-as-QA pattern in all three cases |
| D7 | Li et al., *Preference Leakage*, arXiv:2502.01534 (ICLR 2026) | OBSERVED: judges biased "towards their related student models" when same model/family. | A Claude persona reviewing a Claude blueprint inherits this |
| D8 | Chen et al., *MLLM-as-a-Judge*, ICML 2024 | OBSERVED: multimodal judges show "significant divergence from human preferences in Scoring Evaluation and Batch Ranking". | Vision judge κ 0.33 in MI (council 08 §2.5) is consistent |
| D9 | Gunjal et al., *Rubrics as Rewards*, arXiv:2507.17746; Viswanathan et al., *RLCF*, arXiv:2507.18624 (Jul 2025) | OBSERVED: checklist rubrics beat Likert judges "up to 31%"; "RLCF is the only method to help on every benchmark tested." | Representation (checklist vs scalar) moves judge reliability more than judge size |
| D10 | *RocketEval*, ICLR 2025, arXiv:2503.05142; Lee et al., *CheckEval*, arXiv:2403.18771 | OBSERVED: "Gemma-2-2B as the judge" reaches "0.965" correlation with humans given instance checklists; binary questions raise cross-evaluator agreement "by 0.45". | A small checklist-driven judge is precedented |
| D11 | Tunstall et al., *SetFit*, arXiv:2209.11055 | OBSERVED: competitive "with only 8 labeled examples per class". | A narrow "is this a tutorial?" classifier is cheap to build once labels exist |
| D12 | Shumailov et al., *AI models collapse…*, Nature 631 (Jul 2024) | OBSERVED: "Indiscriminate use of model-generated content in training causes irreversible defects." | The Q&A corpus is model-generated |

INFERENCE (D): fine-tuning carries procedure/format well with ~10³ curated examples and facts poorly; a narrow checklist-formatted, separately-trained detector is well precedented; a fine-tuned general operator is not.

## E. Role separation

| # | Source (date) | Direct claim |
|---|---|---|
| E1 | Huang et al., *LLMs Cannot Self-Correct Reasoning Yet*, ICLR 2024, arXiv:2310.01798 | OBSERVED: under intrinsic self-correction "performance even degrades after attempting to do so." |
| E2 | Stechly, Marquez, Kambhampati, arXiv:2310.12397 / 2402.08115 (ICLR 2025) | OBSERVED: "iterative frameworks with LLMs self-critiquing perform even worse"; helps "when there is an external provably correct verifier in the loop." |
| E3 | Kamoi et al., *When Can LLMs Actually Correct Their Own Mistakes?*, TACL 2024, arXiv:2406.01297 | OBSERVED: "no prior work demonstrates successful self-correction with feedback from prompted LLMs, except … tasks exceptionally suited"; works with "reliable external feedback"; "large-scale fine-tuning enables self-correction." |
| E4 | Khan et al., *Debating with More Persuasive LLMs*, ICML 2024 best paper | OBSERVED: adversarial expert debate with a weaker judge lifts human accuracy "88% (naive 60%)". |
| E5 | Smit et al., *Should we be going MAD?*, ICML 2024 | OBSERVED: multi-agent debate "do[es] not reliably outperform … self-consistency and ensembling". |
| E6 | Cemri et al., *MAST — Why Do Multi-Agent LLM Systems Fail?*, arXiv:2503.13657 (NeurIPS 2025 D&B) | OBSERVED: 14 failure modes in three classes — "system design issues, inter-agent misalignment, task verification"; failures "often stem from system design issues". |
| E7 | Anthropic, *How we built our multi-agent research system* (13 Jun 2025) | OBSERVED: orchestrator + subagents "+90.2%" on research; "about 15× more tokens"; dependency-heavy domains "are not a good fit". |
| E8 | Cognition, *Don't Build Multi-Agents* (Jun 2025) and 2026 follow-up | OBSERVED: default single-threaded; "multi-agent systems work best today when writes stay single-threaded and the additional agents contribute intelligence rather than actions." |

INFERENCE (E): the literature does not support "add a critic agent" as such. Separation helps when the critic has *different information or a different objective* (external verifier, adversarial debate, trained critic, programmatic gate); it does not help — sometimes hurts — when the critic is the same model re-prompted with the same context. The Anthropic/Cognition disagreement resolves on task structure: a compositing/render pipeline is write-heavy and dependency-heavy; the reconciled 2026 position is that extra agents contribute judgment while writes stay single-threaded.

## F. Checklists vs principles

| # | Source (date) | Direct claim |
|---|---|---|
| F1 | Haynes et al., NEJM 360:491 (Jan 2009) | OBSERVED: surgical checklist, 8 hospitals: major complications "fell from 11 percent … to 7 percent"; deaths "1.5 percent to 0.8 percent". |
| F2 | Pronovost et al., NEJM 355:2725 (Dec 2006) | OBSERVED: five-step checklist + culture intervention: CRBSI "66%" reduction at 16–18 months. |
| F3 | Urbach et al., NEJM 370:1029 (Mar 2014) | OBSERVED: mandated Ontario checklists "not associated with significant reductions in operative mortality or complications." |
| F4 | Degani & Wiener, *Cockpit Checklists*, Human Factors 35(2) (1993) | OBSERVED: "improper use, or nonuse, of the normal checklist … often cited as a major contributing factor to aircraft accidents"; format, length and production pressure determine use. |
| F5 | Gawande, *The Checklist Manifesto* (2009) | OBSERVED: errors of "ineptitude" (not using what is known) dominate; effective checklists carry "5–9 items — only the 'killer items'", DO-CONFIRM or READ-DO, at defined "pause points". |
| F6 | Reward hacking in rubric RL, arXiv:2605.12474 (May 2026) | OBSERVED (abstract-level): rubric rewards can be gamed by satisfying the letter of items. |

INFERENCE (F): the only intervention with positive evidence from *both* human-factors and LLM studies is a short, instance-specific, binary confirmation checklist run at a defined pause point by something other than the author, with the answer gating the next step. Mandated-but-unenforced checklists show null effects (F3, F4) — the exact analogue of "the rule exists in the repository" vs "the confirmation ran before render". Caveats: checklists decay with length (A4) and can be gamed (F6).

---

## G. Agency practice: incomplete brief → complete brief

| # | Source (date) | Direct claim |
|---|---|---|
| G1 | Julian Cole, *GET/WHO/TO/BY* (May 2021) — OBSERVED-PRIMARY | GET = target; WHO = current belief/behaviour; TO = desired response; BY = "one message/action"; "creative briefs have to be simple or wonderful". |
| G2 | Wikipedia *Creative brief* (citing Burtenshaw et al. 2011; O'Guinn 2011; Butterfield 1999) — OBSERVED-PRIMARY | fields: background, audience, insight, objectives, single message, desired behaviour, tone, mandatories, deliverables, timeline, budget, approvals. |
| G3 | Ogilvy brief template (Scribd reproduction) — OBSERVED-SECONDARY | single-minded proposition, reason to believe, tone with examples, current vs desired belief, mandatories, measurement. |
| G4 | Binet & Field, *The Long and the Short of It* (IPA, 2013) — OBSERVED-PRIMARY (IPA page) | brand-building vs activation on "two different clocks"; ~60:40 split. The brief must declare which clock. |
| G5 | Romaniuk / Sharp (Ehrenberg-Bass); *Int. J. Advertising* 2026, DOI 10.1080/02650487.2026.2637295 — OBSERVED | 1,162 distinctive assets, 21 categories: shape-based assets (logos, packaging) strongest (40 % Fame / 71 % Uniqueness). The brief must enumerate the brand's *existing* distinctive assets. |
| G6 | Mercer Island Group, *tissue session* (19 Mar 2024) — OBSERVED-PRIMARY | a midpoint session presenting "early strategies", "early solution ideas" — rough territories, before finishing. |
| G7 | Dalim, *Why creative projects get stuck…* (23 Jun 2026) — OBSERVED-SECONDARY | "internal review happens before client presentation"; a named approver per stage; "Involve key stakeholders at the brief stage, not the review stage." |
| G8 | Agency role explainers — OBSERVED-SECONDARY | planner owns the brief; CD owns creative quality vs brief; producer owns feasibility, schedule, budget, casting, delivery specs. |

INFERENCE (G): the twelve decisions a strategist extracts before a brief exists — objective/clock, who, to-what, single proposition, proof, product role, distinctive assets, tone, mandatories, deliverables/formats, budget/timeline, approver — are stable across sources. The Cumin failures (proposition, product role, proof, CTA, casting) are *all* standard brief fields: the gap is intake, not generation.

## H. Structural knowledge for short video ads (universal vs platform-specific)

| # | Source (date) | Direct claim |
|---|---|---|
| H1 | Google, *ABCD playbook* (Ipsos/Nielsen Neuro/Kantar; 2018 data) — OBSERVED-PRIMARY | "Use tight framing"; "two or more shots in the first five seconds"; "Introduce your product or brand in the first five seconds"; on-screen people mentioning the brand beat VO for recall; logo on product for recall, super/watermark for consideration; specific CTA verbs; "present CTAs after establishing context" (Action objective). n = 5,000 / 6,000 / 15,000 ads. Effectiveness: "30% lift in short-term sales likelihood" (Kantar Link AI, 2021 — a predicted metric). |
| H2 | Meta Ads Guide, Instagram Reels (current) — OBSERVED-PRIMARY | 9:16 safe zone: keep text/logos out of "at least 14%" top, "35%" bottom, "6%" each side (≈ 269 / 672 / 65 px on 1080×1920). **No official 4:5 or 1:1 margins.** |
| H3 | Meta Help Center, Advantage+ creative — OBSERVED-PRIMARY | 31 enhancements incl. generative text/backgrounds/CTA stickers; "may be enabled by default"; QA must record enhancement state. |
| H4 | TikTok *Creative Codes* one-pager (May 2023) — OBSERVED-PRIMARY | "90% of ad recall impact is captured within 6 seconds"; "Branding in the first few seconds should be subtle"; "Go lo-fi"; "Close: Use strong CTA". TikTok safe zone is template-based, not a fixed percentage. |
| H5 | System1 × TikTok (887 ads, 92 k viewers; 23 Jun 2025) — OBSERVED-PRIMARY | highest early brand recognition → "88% higher Memory lift, 92% higher Brand Awareness lift"; "logos in context … outperform standalone logo placement"; sonic asset in first 2 s +191 %; **logo overlays reduced brand awareness**; creator ads +39 % attention but brand identified at "roughly half the rate". |
| H6 | Kantar, *Role of attention* (21 Nov 2023) — OBSERVED-PRIMARY | passive attention "diminishes more quickly in short formats"; viewers "often stopped watching by the time the brand was introduced". |
| H7 | Digiday (2016) — OBSERVED-SECONDARY | "85% of Facebook video is watched without sound." |
| H8 | Google Ads Help, video specs / Shorts — OBSERVED-PRIMARY | safe-area PNG templates, no percentages; Shorts CTA button at 3 s or 10 s by campaign type. |

INFERENCE (H): universal across Google, Meta, TikTok, System1, Kantar: hook in 2–6 s; brand/product recognisable early, preferably *in context* (in hand/in scene, spoken by an on-screen person) rather than as an overlay; legible when muted (except YouTube, ~95 % sound-on); explicit CTA/offer at the close; keep text out of UI-occluded bands. Platform-specific and **not to be hard-coded**: safe-zone geometry (changed Mar 2026 per third parties), "3 s" (Meta) vs "5 s" (YouTube) vs "subtle in hook" (TikTok), lo-fi vs polished register, social loudness targets, "UGC outperforms" (attention yes, branding no), any single TTS "best".

## I. Pre-production review, locks and audio

| # | Source (date) | Direct claim |
|---|---|---|
| I1 | Wikipedia *Animatic* (citing Brine, OUP 2020) — OBSERVED-PRIMARY | animatic = storyboard stills "in sync with rough dialogue (i.e., scratch vocals)"; "avoid wasting time and resources on the animation of scenes that would otherwise be edited out." |
| I2 | A. Williams, *Animation Apprentice* (19 May 2020) — OBSERVED-PRIMARY | "Record your dialogue first, then do the animation"; post-syncing "almost always a mistake". |
| I3 | Frame.io *Editing stages* — OBSERVED-PRIMARY | assembly → rough cut → fine cut → picture lock "so that the color, sound, and finishing teams can begin work." |
| I4 | AICP Standard Commercial Production Agreement — OBSERVED-PRIMARY (PDF) | "Agency/Client shall supply scripts, storyboards…"; changes "from the script(s) or storyboard(s)" priced before incurred; payment "Due upon approval of photography". Script + storyboard are contractual inputs locked before money is binding. |
| I5 | Yamdu, *PPM* — OBSERVED-PRIMARY | pre-production meeting checks storyboard, AV script, shot list, cast/styling, deliverables and cut-downs. |
| I6 | Kantar (5 Apr 2022; Marketplace page) — OBSERVED-PRIMARY | "Testing an ad at two stages … (for example animatic and finished film) can increase advertising impact by 38%"; early testing "up to 12%" — unmethodised marketing claims. |
| I7 | EBU R 128 v5 (Nov 2023) and R 128 s1 v3 (Aug 2020) — OBSERVED-PRIMARY (PDFs) | −23.0 LUFS programme loudness; short-form "shall not exceed −18.0 LUFS" short-term; max true peak −1 dBTP. |
| I8 | Netflix spec via Production Expert (13 May 2022) — OBSERVED-SECONDARY | "−27 LKFS within a 2 LU window" dialogue-gated; true peak −2 dBFS. |
| I9 | WCAG 2.1 SC 1.4.7 — OBSERVED-PRIMARY | background "at least 20 decibels lower than the foreground speech". |
| I10 | T. Ricketts, *briefing voice auditions* (2 Apr 2024) — OBSERVED-PRIMARY | specify accent, tone, emotional quality, age/gender, and "a custom read of the actual script excerpt rather than a reel". |

INFERENCE (I): three review points are supported in this order — brief-complete gate (the twelve decisions), animatic gate (script locked, VO recorded and *measured*, boards from approved stills with safe-zone overlays, shot durations derived from the VO), picture-lock/QA gate (automated safe-zone, legibility, loudness, duration, enhancement flags; human only on flagged items plus on-screen text and identity). Never fix shot durations before the VO exists.

## J. Multimodal AI pipelines and vendor controls

| # | Source (date) | Direct claim |
|---|---|---|
| J1 | Lin et al., *VideoDirectorGPT*, arXiv:2309.15091; Li et al., *Anim-Director*, arXiv:2408.09787 (SIGGRAPH Asia 2024); Hu et al., *StoryAgent*, arXiv:2411.04925; Xu et al., *FilmAgent*, arXiv:2501.12909; Wu et al., *MovieAgent*, arXiv:2503.07314; *MM-StoryAgent*, arXiv:2503.05242; Huang et al., *ViMax*, arXiv:2606.07649 (Jun 2026) — OBSERVED | Common order: story/script → per-shot plan with entity registry → still keyframes/storyboard → I2V per shot → audio → assembly; FilmAgent uses "Critique-Correct-Verify" and "Debate-Judge"; only MovieAgent takes a character bank as input; **none takes a product bank; audio is last** (opposite of animation practice I2). |
| J2 | Google Veo 3.1 API docs — OBSERVED-PRIMARY | "Up to three reference images" with `reference_type: "asset"` to "Preserve subject appearance (person, character, or product)"; "English (EN) is fully supported, but other languages have not been evaluated"; 8 s only at 1080p or with references. |
| J3 | Kling Element Library guide — OBSERVED-PRIMARY | an element = 2–4 reference images; Video 3.0 binds up to 3 elements. |
| J4 | Runway Gen-4 / References — OBSERVED-PRIMARY | consistency "with a single reference image"; third-party: up to 3 references (SEARCH-ONLY). |
| J5 | Higgsfield (9 Aug 2026); Morphic troubleshooting — OBSERVED-PRIMARY | root cause of failed generations: "the model had to guess at something … the person generating already knew and simply didn't specify"; hands: "reduce how much the hands are asked to do"; text: never generate on-screen copy, composite it. |
| J6 | Artificial Analysis Speech Arena (Aug 2026 snapshot) — OBSERVED-PRIMARY | Elo leaders within ~80 points (Cartesia Sonic 3.6 1277 … Gemini 3.1 Flash TTS 1204 … ElevenLabs v3 1197); ranking churns monthly; no Indian-language arena. |
| J7 | Sarvam *Bulbul V3* (5 Feb 2026, vendor-commissioned) — OBSERVED-PRIMARY; Menta, *PSP benchmark*, arXiv:2604.25476 (Apr 2026) — OBSERVED-PRIMARY | ElevenLabs v3 alpha leads full-band audio quality; Bulbul V3 leads at 8 kHz; "no single system is Pareto-optimal"; retroflex collapse grows Hindi < Telugu < Tamil. |
| J8 | ElevenLabs v3 / Voice Design docs; Gemini TTS docs; Sarvam Bulbul docs — OBSERVED-PRIMARY | ElevenLabs: audio tags, "The most important parameter … is the voice you choose", seed-reproducible voice design; Gemini: natural-language "style, accent, pace, and tone", Hindi at GA, prompt structure "Audio Profile, Scene, Director's Notes…"; Bulbul: speaker + `pace` only, "does not support SSML tags" — emotion must be written into the script. |
| J9 | Google Ads asset generation help — OBSERVED-PRIMARY | generator "automatically limit[s] … Branded items and logos not provided as input"; advertisers must review generated assets. |
| J10 | Bachar et al., *LLM Performance Predictors: Learning When to Escalate*, arXiv:2601.07006 (AAMAS 2026) — OBSERVED-PRIMARY | uncertainty meta-models give "significant improvements … in accuracy-cost trade-offs"; distinguishes ambiguous-content from ambiguous-policy failures. |

INFERENCE (J): vendor identity controls converge (≤ 3–4 references; i2v from an approved still; never generate copy); TTS must be cast by audition on the actual script at final pace, not by leaderboard; HITL literature supports uncertainty-triggered review for *final QA* but offers no confidence estimator for *concept* correctness — concept sign-off must be unconditionally human.

---

## K. What the research implies for the hypotheses (no winner chosen here; see Part 12)

| Hypothesis | Supported mechanisms | Against |
|---|---|---|
| B retrieval weak | contextual retrieval + reranking cuts misses (B1); mistake-anchored retrieval changes decisions (B8) | a ~30-claim need fits in context without retrieval (B1, B3); near-miss chunks hurt (B2, A6); retrieval only helps states 2–3 |
| C context overloaded | A1–A6, A4 (instruction count), A7 (negation), A5 (late judge) | whether the two packs cross a threshold is an empirical question for the repo councils (they do: 60–80 k tokens before the brief, 21 + 28 + ~50 instructions) |
| E role collapse | E1–E3, D6, D7, E6 "task verification" | separation helps only with different information/objective or a programmatic gate; a prompted persona of the same model does not (E1, E4) |
| F/H representation wrong / too abstract | B6, B7, F (checklists), B8 | compatible with all others, not exclusive |
| D/I model insufficient | D4 (verifiers), D10 (small checklist judges) | 43/46 defects were not model failures (Part 6) |
| K over-engineered | B4, C3, A13's warning, Anthropic "simplest solution" | memory helps when procedural/executable (C5) |
| L strong LLM + short checklist | F1–F5, B10, D9, D10 | checklists decay (A4) and can be gamed (F6); no controlled "doctrine-in-prefix vs same content as checklist" ablation exists (UNKNOWN) |
| M/N Q&A as substrate / as eval data | B8 (mistake-anchored examples) for M; D12, D1 against training use; benchmark use precedented | see Part 7 |

Cross-cutting: the one intervention with positive evidence from both human-factors and LLM research is a short, binary, instance-level confirmation at a defined pause point, answered by something other than the author, gating the next step. That is not a verdict; it is the mechanism most of the hypotheses would need to instantiate.

## Unknowns from the research
- No published study measures cross-job recurrence prevention for creative-quality failures.
- No study isolates "doctrine in prefix vs the same doctrine as a checklist" with content held constant.
- No peer-reviewed cost-of-late-rejection data for advertising creative; Kantar's 38 % / 12 % are unmethodised.
- No AI creative platform (Pencil, Omneky, AdCreative.ai) publishes its brief schema or QA rules.
- No independent benchmark of *product* (vs character) identity retention across shots.
- Indian-market-specific evidence on early branding and sound-on: not found; all H evidence is global/Western.
- Vendor conflicts: A-MEM vs Mem0 numbers are not mutually reproducible; ACE vs context-rot on playbook length.
