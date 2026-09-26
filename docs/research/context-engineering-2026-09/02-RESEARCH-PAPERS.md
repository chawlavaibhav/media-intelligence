# Research literature: large knowledge and long-term memory for LLM agents

Research appendix 02 of `CONTEXT-SOLUTION.md`. Compiled 2026-09-25. Every source's abstract or official page was read
in this session, mostly on arxiv.org/abs; a few numbers come from the HTML full text and are marked "(body)". **[unverified]** marks
claims we could not check.

---

## 1. Long-context failure: a bigger context window is not the same as usable knowledge

| Work | URL / year | Takeaway |
|---|---|---|
| **Lost in the Middle** (Liu et al.) | arxiv.org/abs/2307.03172 (2023) | U-shaped accuracy: GPT-3.5-Turbo with 20 docs scored 75.8% with the answer first, 53.8% in the middle and 63.2% last. The middle score is **below its closed-book 56.1%**, so adding context made it worse than none. |
| **RULER** (NVIDIA) | arxiv.org/abs/2404.06654 (2024) | Near-perfect at needle-in-a-haystack, yet large drops as length grows. Only half of the models claiming 32K+ hold up at 32K. |
| **NoLiMa** (Adobe) | arxiv.org/abs/2502.05167 (2025) | When question and needle share few words, **11 of 13 models fall below 50% of baseline at 32K**; GPT-4o drops from 99.3% to 69.7%. *Most relevant for a Canon: a task is rarely phrased with the same words as the rule it needs.* |
| **Context Rot** (Chroma) | trychroma.com/research/context-rot (Jul 2025) | 18 models degrade with length even on trivial tasks. One distractor hurts, and coherent haystacks were worse than shuffled ones. On LongMemEval a focused ~300-token prompt clearly beat the full ~113K. |
| **LongMemEval** | arxiv.org/abs/2410.10813 (2024) | 30% accuracy drop across sustained interactions. Finer-grained session units, fact-augmented keys and time-aware query expansion help. |
| **Context Length Alone Hurts…** (Du et al.) | arxiv.org/abs/2510.05381 (2025) | Even with *perfect* retrieval, accuracy fell 13.9–85% as length grew, even with whitespace or masked filler. Fix: **recite the relevant evidence first**. |
| **IFScale** (Distyl) | arxiv.org/abs/2507.11538 (2025) | Best model reaches 68% at 500 instructions (o3 97.8% and gemini-2.5-pro 84.8% at 250). Earlier instructions are favoured, and failures are **silent omissions**. |
| **ATLAS** | arxiv.org/abs/2605.28079 (May 2026) | 26 models across 8K–1M tokens; rankings reshuffle between 128K and 1M. Measure by capability × length. |
| **1M multi-hop** | arxiv.org/abs/2605.02173 (May 2026) | Single-needle retrieval at 1M is solved (100%), but three-hop reasoning still decays. Nominal window size is a poor proxy for usable context. |
| **LOCA-bench** | arxiv.org/abs/2602.07962 (Feb 2026) | Agents in growing contexts degrade; context-management scaffolding substantially improves success. |
| **Anthropic, Effective context engineering** | anthropic.com/engineering/effective-context-engineering-for-ai-agents (Sep 2025) | Aim for the "smallest possible set of high-signal tokens"; load just-in-time via identifiers; compaction, notes, sub-agents. |

**RAG vs long context:**
- *Retrieval meets Long Context* (2310.03025): a 4K model with retrieval ≈ a 16K long-context model.
- *Self-Route* (2407.16833): route each query between RAG and long context by self-reflection, for near long-context quality at much lower cost.
- *Long-Context LLMs Meet RAG* (2410.05983): quality rises and then **falls** as more passages are retrieved, because of hard negatives.

**Bottom line:** loading hundreds of Canon docs degrades both recall and rule-following. It is worst when the task wording differs from the rule,
when rules number in the hundreds, and when similar-but-wrong distractors are present.

## 2. Memory architectures

| Work | URL / year | Takeaway |
|---|---|---|
| MemGPT / Letta | 2310.08560 (2023) | Tiers the context like an OS pages RAM; the agent moves data between tiers with tools. |
| Sleep-time Compute | 2504.13171 (2025) | Offline "thinking" about a context before queries arrive: about 5x less test-time compute, +13/18% accuracy, 2.5x lower cost per query. |
| Generative Agents | 2304.03442 (2023) | A memory stream plus periodic **reflections**; retrieval by recency, importance and relevance. |
| Reflexion | 2303.11366 (2023) | Verbal reflections in a buffer; 91% vs 80% pass@1 on HumanEval. |
| Voyager | 2305.16291 (2023) | **A skill library of executable code** plus self-verification. Procedural knowledge is stored as code. |
| ExpeL | 2308.10144 (2023) | Insights managed with ADD/EDIT/UPVOTE/DOWNVOTE; **removed when the count reaches 0**. HotpotQA 39% vs 28%, ALFWorld 59% vs 40%. |
| Agent Workflow Memory | 2409.07429 (2024) | Reusable workflows from past runs: +24.6% Mind2Web and +51.1% WebArena relative success. |
| Memp | 2508.06433 (2025) | Procedural memory with update, correct and **deprecate** operations. |
| ReasoningBank (Google) | 2509.25140 (2025) | Distils strategies from successes **and failures**; beats success-only memory. |
| Dynamic Cheatsheet | 2504.07952 (2025) | A self-curated set of concise snippets: Game of 24 went from 10% to 99%, and AIME more than doubled. |
| **ACE** (Stanford/SambaNova) | 2510.04618 (2025) | An evolving playbook of **itemised bullets with IDs and helpful/harmful counters**. **Delta updates are merged by deterministic code**; de-duplication by embedding. It names **brevity bias** and **context collapse**: a Dynamic Cheatsheet context went from 18,282 tokens to 122 in one rewrite, and accuracy fell from 66.7% to 57.1%, below the no-memory 63.7% (body). Results: +10.6% on agents, +8.6% on finance. Without a reliable feedback signal, the context becomes noisy. |
| A-MEM | 2502.12110 (2025) | Zettelkasten notes; new memories update old ones. |
| Mem0 | 2504.19413 (2025) | LoCoMo: +26% vs OpenAI memory, 91% lower p95 latency, 90%+ token savings. *Vendor-authored.* |
| Zep / Graphiti | 2501.13956 (2025) | Temporal knowledge graph with validity windows; up to +18.5% on LongMemEval. *Vendor-authored.* |
| HippoRAG | 2405.14831 (2024) | Knowledge graph plus PageRank; up to +20% on multi-hop, 10–30x cheaper than iterative retrieval. |
| GraphRAG (Microsoft) | 2404.16130 (2024) | Community summaries for global "themes" questions; expensive to index. |
| RAPTOR | 2401.18059 (2024) | A tree of recursive summaries; +20% absolute on QuALITY. |
| **Anthropic Contextual Retrieval** | anthropic.com/news/contextual-retrieval (2024) | Contextualised chunks + BM25 + rerank cut top-20 retrieval failure by 67% (5.7% → 1.9%). Under 200K tokens, "just include the entire knowledge base" with caching; the 2025–26 results suggest this is optimistic for rule-dense material. |
| **Anthropic Agent Skills** | anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills (Oct 2025) | Three-level progressive disclosure. Deterministic operations belong in scripts. |
| Memory management study | 2505.16067 (2025) | **Experience-following**: agents copy similar past memories, so bad memories propagate errors. Control the quality of what gets added or deleted. |
| SSGM (2026) | 2603.11768 | Consistency checks, temporal decay and access control before consolidation; "semantic drift" through iterative summarisation. |
| Surveys | 2512.13564, 2603.07670, 2602.06052, 2512.16301 | Memory as a write–manage–read loop. Open problems: consolidation, learned forgetting, contradictions. The field is shifting toward portable **skills**. |

## 3. Fine-tuning vs RAG vs small models

| Work | URL / year | Takeaway |
|---|---|---|
| Ovadia et al. (Microsoft) | 2312.05934 (2023) | **RAG beats unsupervised fine-tuning** for knowledge injection. |
| Gekhman et al. (Google) | 2405.05904 (2024) | New knowledge is learned slowly by fine-tuning and **linearly increases hallucination**. |
| LIMA | 2305.11206 (2023) | 1,000 examples teach format and style; knowledge comes from pretraining. *Fine-tune for behaviour, retrieve for facts.* |
| RAFT | 2403.10131 (2024) | Fine-tune the model to *use* retrieved docs and ignore distractors. |
| LoRA Learns Less and Forgets Less | 2405.09673 (2024) | LoRA learns less than full fine-tuning but preserves more general ability. |
| Prompt distillation | 2412.14964 (2024) | Self-distillation can beat fine-tuning and sometimes RAG. |
| Cartridges (Stanford) | 2506.06266 (2025) | An offline-trained KV cache per corpus: 38.6x less memory, 26.4x higher throughput. Needs open weights. |
| Test-time training | 2512.13898, 2512.23675 (2025) | Updating weights on the context beats piling on more thinking tokens at long context. |
| NVIDIA SLM position | 2506.02153 (2025) | 7B SLMs are 10–30x cheaper; 40–70% of agent calls are replaceable. A position paper, not an empirical result. |
| Distilling Step-by-Step | 2305.02301 (2023) | A 770M T5 beats 540B PaLM few-shot when trained on LLM rationales. |

**Bottom line:** fine-tuning is wrong for changing facts and rules (it learns them slowly, raises hallucination, cannot be audited, and is not
available for Claude or Codex). It is right for stable behaviour and format, and for cheap narrow classifiers, taggers and judges.

## 4. Instruction and rule compliance

| Work | URL / year | Takeaway |
|---|---|---|
| τ-bench (Sierra) | 2406.12045 (2024) | Agents following prose policy documents: GPT-4o succeeds on under 50% of tasks, and pass^8 is under 25%. |
| IFEval | 2311.07911 (2023) | "Verifiable instructions" that can be checked in code. |
| AgentSpec | 2503.18666 (2025) | Runtime rule DSL: over 90% of unsafe code-agent executions prevented and 100% AV compliance, at millisecond overhead. |
| Huang et al. (DeepMind) | 2310.01798 (2023) | Self-correction without external feedback fails. |
| CRITIC | 2305.11738 (2023) | Self-correction works when it is **grounded in tool feedback**. |
| TICK / STICK | 2410.03608 (2024) | Yes/no checklists: judge–human agreement 46.4% → 52.2%; +7.8% from self-refinement and +6.3% from Best-of-N. |
| RLCF: Checklists > Reward Models | 2507.18624 (2025) | Checklists scored by judges plus verifier programs improve all 5 instruction-following benchmarks. |
| LLM-as-a-Judge (Zheng) | 2306.05685 (2023) | Over 80% agreement with humans, but position, verbosity and self-enhancement biases. |
| Constitutional AI | 2212.08073 (2022) | Principles work when used to generate a feedback signal, not merely placed in context. |
| Instruction Hierarchy | 2404.13208 (2024) | Quoted logs can dilute or override rules. |

**Bottom line:** no paper compares a "prose rule" head-to-head with a "code check" in creative production. Even so, the evidence converges:
prose rules degrade as their number grows, and checks grounded in verifiers are what work.

## 5. Synthesis: where each piece of knowledge lives

- **A. Always in context (a few K tokens):** fewer than ~20–30 invariants plus a one-line-per-item map; critical rules first, and recite them before acting.
- **B. Retrieved on demand:** atomic, scoped, dated, status-tagged items. Hybrid BM25 + embeddings + rerank; retrieve few items.
- **C. Tools and verifiers:** everything checkable. Every recurring failure becomes a check where possible; prose only when not.
- **D. Weights and small models:** behaviour and style; high-volume narrow classifiers and judges. Never changing facts.

Routing test: can code check it → C. Needed on every task and short → A. Task- or model-specific → B. Stable, high-volume behaviour → D.

### The evolving playbook of learnings
Two failure modes: **bloat** (distractors, experience-following of bad precedents) and **collapse/drift** (LLM rewrites of the whole playbook).
Supported practices:
1. Raw logs are append-only and retrievable, never loaded wholesale.
2. The playbook holds itemised, ID-addressed entries; **deltas are merged by deterministic code**. Each entry carries scope, evidence,
   helpful/harmful counters, dates, status and a `supersedes` link.
3. Separate generator, reflector and curator roles; retire entries whose counts reach zero.
4. Promote only on grounded feedback: customer verdict, a validator, or a comparison against a baseline.
5. Promotion ladder: raw log → candidate → validated entry → **executable check / recipe** (leaves prose entirely).
6. Consolidate offline, as a batch with PR review.
7. Retrieve by scope at task time; never inject the whole playbook.
8. Keep an eval set of past jobs and re-run it on every playbook change.

### Honest gaps
- No head-to-head of prose vs verifier for creative work.
- Memory-system gains come from conversational QA benchmarks, several of them vendor-authored.
- The point where bloat starts to hurt depends on model and task, so it must be measured on our own eval.
