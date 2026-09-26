# How AI labs and coding-agent builders manage large context and long-term memory

Research appendix 01 of `CONTEXT-SOLUTION.md`. Compiled 2026-09-25. All sources were fetched and read, except where marked
**[mirror]** (the primary page blocked us, so we read a verbatim copy) or **[search-only]** (URL and summary seen in search results only).

---

## Part 1. Primary sources

### Anthropic
1. **Effective context engineering for AI agents** (Rajasekaran, Dixon, Ryan, Hadfield; Sep 29 2025).
   https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
   - Write the system prompt at the right "altitude": heuristics, not brittle if/else rules.
   - Just-in-time retrieval: the agent holds identifiers (file paths, queries, links) and loads content at runtime.
   - Compaction: summarise history, keep decisions, drop redundant tool output.
   - Structured notes (NOTES.md, to-do files) kept outside the context window.
   - Sub-agents return condensed summaries of **1–2k tokens**.
   - Minimal, non-overlapping tools.
2. **Equipping agents with Agent Skills** (Oct 16 2025).
   https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
   - Three-level progressive disclosure: frontmatter (always loaded) → SKILL.md (when relevant) → linked files (as needed).
   - Build skills from gaps observed on representative tasks.
3. **Skill authoring best practices.** https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
   - SKILL.md under **500 lines**; references one level deep (nested references get only partially read).
   - A table of contents on any reference file over 100 lines; organise by domain.
   - **Build evals first:** at least 3 scenarios, measured against a no-skill baseline.
   - Put deterministic steps in scripts.
4. **Claude Code skills docs.** https://code.claude.com/docs/en/skills
   - Listing cap of 1,536 characters for description plus `when_to_use`.
   - After compaction, invoked skills are re-attached: the first 5k tokens each, within a 25k budget.
   - `paths:` auto-load.
5. **Claude Code memory docs.** https://code.claude.com/docs/en/memory
   - **CLAUDE.md under 200 lines.** "Longer files consume more context and reduce adherence."
   - `@imports` expand at launch (up to 4 hops), so they save no tokens.
   - `.claude/rules/*.md` with `paths:` load lazily.
   - "No guarantee of strict compliance": use **hooks** for anything that must always happen.
   - Contradictory rules mean Claude "may pick one arbitrarily".
6. **Claude Code best practices.** https://code.claude.com/docs/en/best-practices
   - "Would removing this cause Claude to make mistakes? If not, cut it. Bloated CLAUDE.md files cause Claude to ignore your actual instructions!"
   - Explore → plan → code; `/clear` between tasks; clear after two failed corrections.
7. **Building effective agents** (Schluntz, Zhang; Dec 2024). https://www.anthropic.com/engineering/building-effective-agents
   - Use the simplest solution that works; add complexity only when evals show it is needed.
8. **Multi-agent research system** (Jun 2025). https://www.anthropic.com/engineering/multi-agent-research-system
   - +90.2% over a single agent, at about 15× the tokens.
   - Token usage explains 80% of the variance in results.
   - Subagents write their outputs to the filesystem.
9. **Writing effective tools for agents** (Sep 2025). https://www.anthropic.com/engineering/writing-tools-for-agents
   - Pagination and filtering; concise vs detailed response formats (about ⅔ fewer tokens); a 25k-token tool-response cap.
10. **Effective harnesses for long-running agents** (Nov 2025). https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
    - A JSON feature list is the source of truth for "done".
    - One feature at a time.
    - Every session starts the same way: git log → progress file → smoke test.
11. **Context editing + memory tool** (Sep 29 2025). https://claude.com/blog/context-management
    - Memory plus context editing: **+39%**; context editing alone: +29%.
    - **−84% tokens** on a 100-turn eval.
12. **Server-side compaction docs.** https://platform.claude.com/docs/en/build-with-claude/compaction
    - Default trigger at 150k tokens.
    - "Keep the active context small, because response quality degrades as a conversation grows."
13. **Scaling Managed Agents** (Apr 2026). https://anthropic.com/engineering/managed-agents
    - The session is a durable, append-only event log outside the context window; the harness slices and re-feeds it.

### OpenAI
14. **Harness engineering** (Lopopolo; Feb 11 2026). https://openai.com/index/harness-engineering/ [mirror: https://jaytaylor.com/notes/node/1770842156000.html]
    - **AGENTS.md is about 100 lines, "the table of contents", not an encyclopedia.** "A giant instruction file crowds out the task,
      the code, and the relevant docs." Their one-big-file attempt made the agent miss key constraints.
    - `docs/` is the system of record.
    - Linters and CI validate the knowledge base; a **doc-gardening agent** removes staleness.
    - "Anything it can't access in-context while running effectively doesn't exist."
15. **Codex AGENTS.md docs.** https://learn.chatgpt.com/docs/agent-configuration/agents-md
    - Files are concatenated root → current directory, and the closest file wins.
    - **Hard cap of `project_doc_max_bytes` = 32 KiB.** After that, nested guidance is silently dropped.
16. **AGENTS.md spec.** https://agents.md/
    - The closest file wins; used by 60k+ projects.
17. **Agents SDK memory cookbooks.** https://developers.openai.com/cookbook/examples/agents_sdk/session_memory ,
    …/context_personalization
    - Memory lifecycle: inject a structured profile, distil during the session, consolidate afterwards.
    - Precedence: latest message > session memory > global memory. Memory is "advisory, not authoritative".
18. **GPT-4.1 prompting guide.** https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide
    - Put instructions at both the start and the end of a long context.
    - XML beats JSON for document collections.
19. **Unrolling the Codex agent loop** [search-only].
    - Keep the stable prefix unchanged so prefix caching works.

### Builders and practitioners
20. **Manus, "Context Engineering for AI Agents: Lessons from Building Manus"** (Jul 2025). https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
    - **KV-cache hit rate is the key metric** (cached tokens cost about 10× less).
    - Mask tools rather than removing them.
    - The filesystem is unlimited context; compression should be restorable.
    - Recite goals in `todo.md`.
    - Keep errors in context; vary serialisation.
21. **Cognition, "Don't Build Multi-Agents"** (Jun 2025). https://cognition.com/blog/dont-build-multi-agents
    - "Actions carry implicit decisions, and conflicting decisions carry bad results."
    - Default to a single-threaded agent.
22. **LangChain, "Context Engineering for Agents"** (Jul 2025). https://www.langchain.com/blog/context-engineering-for-agents
    - Four strategies: write / select / compress / isolate.
23. **Chroma, "Context Rot"** (Jul 2025). https://www.trychroma.com/research/context-rot
    - 18 models degrade with length; one distractor hurts.
    - A focused ~300-token prompt beat the full ~113k-token one.
24. **Drew Breunig, "How Long Contexts Fail" / "How to Fix Your Context"** (Jun 2025). https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html
    - Four failure modes: poisoning, distraction, confusion (46 tools failed where 19 worked), and clash (−39%).
    - Six fixes, including tool loadout, quarantine, pruning and offloading.
25. **Dex Horthy (HumanLayer), "Advanced Context Engineering for Coding Agents"** + AI Engineer talk "No Vibes Allowed".
    https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md ,
    https://www.youtube.com/watch?v=rmvDxxNubIg
    - Keep context utilisation at **40–60%** (a "dumb zone" begins around 40%).
    - **Research → Plan → Implement**, with written artifacts and a fresh context per phase.
    - Humans review the plans.
26. **HumanLayer, "Writing a good CLAUDE.md"** (Nov 2025). https://www.humanlayer.dev/blog/writing-a-good-claude-md
    - Frontier models reliably follow about **150–200 instructions**, and the harness already uses about 50 of them.
    - Keep the root file under 300 lines (HumanLayer's own is under 60).
    - Don't use the LLM as a linter.
27. **HumanLayer, "Getting Claude to Actually Read Your CLAUDE.md"** (Mar 2026). https://www.humanlayer.dev/blog/stop-claude-from-ignoring-your-claude-md
    - `<important if="…">` conditional blocks.
28. **Vercel, "AGENTS.md outperforms skills in our agent evals"** (Jan 2026). https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals
    - Pass rates: no docs **53%**; skills **53%**; skills with explicit instructions **79%**; **compressed docs index in AGENTS.md 100%**.
    - Skills were never invoked in 56% of runs.
    - The index was an 8KB pipe-delimited pointer index (compressed from 40KB).
29. **Cursor, "Dynamic context discovery"** (Jan 2026). https://cursor.com/blog/dynamic-context-discovery
    - Files are the primitive: long outputs go to files, and MCP tool descriptions are loaded selectively (−46.9% tokens).
30. **Aider repo map.** https://aider.chat/docs/repomap.html
    - A PageRank-ranked symbol map with a 1k-token budget.
31. **Factory.ai, compression eval** (Dec 2025). https://factory.com/news/evaluating-compression
    - Anchored structured summaries scored 3.70, vs 3.44 (Anthropic-style) and 3.35 (OpenAI).
    - **Artifact tracking was the weakest dimension (2.2–2.5 / 5)**, so keep the list of changed files outside the summary.
32. **Letta, "Context Repositories"** (Feb 2026). https://www.letta.com/blog/context-repositories/
    - Memory = files in git; the `system/` folder is always loaded, everything else is disclosed progressively.
    - Reflection and defragmentation passes.
33. **ACE** (arXiv 2510.04618).
    - An itemised playbook updated by delta merges; avoids brevity bias and context collapse.
34. **Gloaguen et al. (ETH), "Evaluating AGENTS.md"** (Feb 2026). https://arxiv.org/abs/2602.11988
    - Context files "do not generally improve task success rates" and add **>20% cost**.
    - LLM-generated files reduced success; **repository overviews are "not helpful"**.
    - Instructions are followed literally, even when that is counterproductive.
    - Useful only for non-standard practices; evaluate changes before shipping them.
35. **Sourcegraph, "Context Engineering: A Practical Guide"** (2026). https://sourcegraph.com/blog/context-engineering
    - Stale indexes act as a poisoning source.
36. **Others.**
    - Karpathy on context engineering [search-only]: https://x.com/karpathy/status/1937902205765607626
    - Simon Willison, "Context engineering" (Jun 2025): https://simonwillison.net/2025/Jun/27/context-engineering/
    - AI Engineer World's Fair 2026 had Context Engineering and Memory tracks; recap: https://getunblocked.com/blog/context-grew-up-at-the-worlds-fair/

## Part 2. The consensus playbook, ranked by impact

**Nobody puts a large corpus in context.** Every source converges on the same set of moves:
- a **tiny always-loaded map**;
- **just-in-time retrieval** from an **agent-legible filesystem**;
- **mechanical enforcement** of the rules that must not be missed;
- a **curation loop** for learnings;
- utilisation kept well below the full window.

1. **Split rules from knowledge, and enforce rules mechanically** (hooks, validators, CI, Stop hooks). A rule an agent cannot violate
   does not need to be in context.
2. **Keep a small root file (about 100 lines), plus a generated, compressed index of the knowledge base** (Vercel: 8KB, 100% pass rate).
   Never `@import` the Canon; regenerate the index in CI.
3. **Restructure the knowledge base for just-in-time retrieval:**
   - focused files with frontmatter (`description`, `applies_to`, `status`, `last_verified`);
   - an INDEX.md per directory, with references one level deep;
   - stable rule IDs;
   - a search script that returns concise, paginated results.
4. **Scope instructions:** path-scoped rules, nested AGENTS.md, skills triggered explicitly.
5. **Subagents for read-only research** (returning 1–2k-token digests); Research → Plan → Implement, with human review of the plan.
   Keep decisions in one thread.
6. **Run learnings as a curated pipeline:**
   - raw logs are append-only and never auto-loaded;
   - a scheduled curator writes ID'd delta updates;
   - a defragmentation pass cleans up;
   - a tiny top-lessons file (200 lines or less).
7. **Session hygiene:** stay within 40–60% utilisation; `/clear`; keep the changed-file list in a file; recite in `todo.md`; keep the prefix
   stable for caching.
8. **Evaluate every context change** on 5–15 representative tasks: pass rate and cost, before and after.

## Part 3. Where sources disagree

| Tension | Reconciliation |
|---|---|
| Always-present index vs on-demand skills (Vercel vs Anthropic/Cursor) | Always load a compressed pointer index; load content on demand; trigger critical skills explicitly |
| Root files useful? (labs yes; ETH: no average gain, +20% cost) | Keep only non-standard, non-inferable rules and pointers; never auto-generate the file |
| How short? | 60 / 100 / 200 / 300 lines; 32 KiB — every answer is orders of magnitude below "the whole Canon" |
| Multi-agent (Anthropic +90%) vs single thread (Cognition) | Subagents read and review; a single writer decides |
| Static docs (OpenAI) vs fresh research (Horthy) | The knowledge base is the system of record, kept fresh by CI; per-task research artifacts are generated from it |
| Concise (Anthropic) vs detailed playbooks (ACE) | The always-loaded layer is concise; the retrievable layer is detailed but itemised |
