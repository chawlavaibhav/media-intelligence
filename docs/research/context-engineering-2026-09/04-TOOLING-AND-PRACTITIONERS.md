# Tooling and practitioner talks: giving coding agents a huge knowledge base

Research appendix 04 of `CONTEXT-SOLUTION.md`. Compiled 2026-09-25 from official docs (Claude Code, Anthropic, Codex, Cursor,
Gemini CLI), GitHub READMEs, and primary posts and talks. Star counts are from GitHub pages as fetched on that date.
**[UNVERIFIED]** marks claims not confirmed at a primary source.

Repo snapshot at the time:
- about 7.8 MB of Markdown under `canon/` (828 files, roughly 2M tokens);
- 118 KB under `production-learning/`;
- a 38 KB `PROJECT-MEMORY.md`;
- two skills;
- **no root `CLAUDE.md` or `AGENTS.md`**.

---

## 1. Built-in mechanisms and their limits

### Claude Code

**CLAUDE.md** (https://code.claude.com/docs/en/memory)
- Files load from broadest to most specific scope and are concatenated, not overridden.
- Subdirectory files load lazily.
- **Target under 200 lines**: "Longer files consume more context and reduce adherence."
- HTML comments are stripped before loading.
- `/doctor` proposes cuts; `/context` shows what actually loaded.

**`@imports`**
- Nested at most 4 hops deep.
- Imported files **still load at launch**: imports organise content but save no tokens.

**AGENTS.md**
- Claude Code v2.1.277+ reads `AGENTS.md` when no CLAUDE.md exists, or via `@AGENTS.md` inside CLAUDE.md.

**`.claude/rules/*.md`**
- Rules with `paths:` globs load lazily.
- Caveat: "Path-scoped rules and nested CLAUDE.md files load into message history when their trigger file is read, so
  compaction summarizes them away" (https://code.claude.com/docs/en/context-window). Anything that must survive compaction belongs in the root file.

**Skills** (https://code.claude.com/docs/en/skills)
- Metadata costs about 100 tokens per skill; the body should stay under 5k tokens (keep SKILL.md under 500 lines).
- The listing truncates each description at 1,536 characters.
- Useful frontmatter: `paths:`, `disable-model-invocation`, `context: fork`, and `` !`cmd` `` for injecting command output.
- With many skills, "some skills lose their descriptions entirely".
- After compaction, invoked skills are re-attached: 5k tokens each, 25k in total.

**Subagents**
- Each starts with a fresh context and can have its own `memory:` (the first 200 lines or 25 KB).
- They return summaries of 1–2k tokens.

**Hooks** (https://code.claude.com/docs/en/hooks)
- `additionalContext` injects context on SessionStart (including the `compact` matcher), UserPromptSubmit,
  PreToolUse, PostToolUse, PreCompact and SubagentStart.
- **Hard cap: 10,000 characters.**
- "Put guardrails in hooks… an instruction… is a request, not a guarantee."

**Auto memory**
- The MEMORY.md index loads its first 200 lines or 25 KB; topic files load on demand.
- It is machine-local.

**MCP**
- Tool search loads schemas on demand.
- Output is capped at 25k tokens by default.

**Large-codebase guide** (https://code.claude.com/docs/en/large-codebases)
- Per-directory files and Read deny rules.
- Expose an existing search or RAG index as an MCP tool.

### OpenAI Codex
- AGENTS.md files are read from the git root down to the working directory, and the closest file wins.
- **`project_doc_max_bytes` = 32 KiB**; once the total reaches it, further files are silently dropped.
- Skills live in `.agents/skills`.
- The initial skill list is capped at **2% of the context window or 8,000 characters**, whichever is smaller.

### Cursor
- `.mdc` rules have four modes: Always, Intelligent, Globs, Manual.
- Nested AGENTS.md is supported; rules should stay under 500 lines.

### Gemini CLI
- GEMINI.md files are discovered just in time.
- `context.fileName: ["AGENTS.md","GEMINI.md"]` lets one file serve all tools.

**Cross-tool takeaway:** use one lean root `AGENTS.md`, with `CLAUDE.md` importing it, under 32 KiB and about 150 lines. Push everything else into skills,
path-scoped rules and on-demand files.

## 2. Search tools for a large corpus

| Tool | What | Signal |
|---|---|---|
| **qmd** (github.com/tobi/qmd) | Local BM25 (FTS5) + embeddings + query expansion + reranker; CLI + MCP | About 30k stars. **Best fit for a Markdown canon** |
| Basic Memory | Markdown + SQLite, read/write MCP | About 4k stars; AGPL |
| claude-mem | Session-history memory plugin | Session history, not curated canon; star count unverified |
| Serena | Symbol-level retrieval through language servers | Code, not prose |
| Context7 | Public library docs | Not for private canon |
| MCP reference memory server | JSONL knowledge graph | Doesn't scale |
| Mem0 / Graphiti / Letta | Chat memory / temporal knowledge graph / agent platform | Heavy for a small team; chat-oriented |
| Beads | Issue-tracker memory for tasks and plans | Optional, for plans |
| Aider repo map | PageRank-ranked index within a 1k-token budget | The pattern matters: a token-budgeted, ranked index |
| llms.txt | An index of links an agent fetches | The index-then-fetch pattern |

On search style:
- Grep and agentic search beat embeddings for **code**; embeddings still pay off for large unstructured **prose** (Jason Liu / Augment, https://jxnl.co/writing/2025/09/11/why-grep-beat-embeddings-in-our-swe-bench-agent-lessons-from-augment/).
- Recommendation: hybrid BM25 + embeddings exposed as a CLI or MCP tool, with grep still available.

## 3. Practitioners

- **Dex Horthy, "No Vibes Allowed"** (AI Engineer 2025, https://www.youtube.com/watch?v=rmvDxxNubIg)
  - A "dumb zone" begins at roughly 40% context use.
  - Research → plan → implement.
  - "Incorrect information is the most damaging, followed by missing information and excessive noise."
- **HumanLayer, "Writing a good CLAUDE.md"**
  - Models reliably follow about 150–200 instructions, and the harness already uses about 50.
  - Keep the file under 300 lines (theirs is under 60).
  - Don't use the model as a linter.
- **Vercel** (https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
  - An 8 KB compressed index in AGENTS.md scored **100%**, vs 79% for skills with explicit instructions and 53% for skills by default (unused 56% of the time).
  - Added instruction: "Prefer retrieval-led reasoning over pre-training-led reasoning."
- **Gloaguen et al., "Evaluating AGENTS.md"** (arXiv 2602.11988)
  - LLM-generated context files lowered success by about 3%; human-written ones raised it by about 4%.
  - Both raised cost by 14–20%.
- **Anthropic**
  - Context engineering post; context editing + memory tool (+39%, −84% tokens).
  - Cal Rueb, "Claude Code best practices" (https://www.youtube.com/watch?v=gv0WHhKelSE).
  - "Don't Build Agents, Build Skills Instead" (https://www.youtube.com/watch?v=CEvIs9y1uog).
  - The Claude Code team adds every preventable PR mistake to a shared CLAUDE.md (Boris Cherny interviews).
- **Jesse Vincent, Superpowers** (https://blog.fsck.com/2025/10/09/superpowers/)
  - A SessionStart hook enforces "you must use skills"; skills are pressure-tested with subagents; lessons are mined into skills.
- **Armin Ronacher** (https://lucumr.pocoo.org/2025/12/13/skills-vs-mcp/)
  - MCP descriptions are "too long to load… too short to guide"; prefer tools packaged as skills.
- **Mitchell Hashimoto** (https://mitchellh.com/writing/my-ai-adoption-journey)
  - "Engineer the harness": every agent mistake becomes an AGENTS.md line **or a programmed tool**.
- **Geoffrey Huntley, "Ralph"** (https://ghuntley.com/ralph/)
  - The same loaded specs on every loop; one item per loop; a brief agent file.
- **Hamel Husain & Shreya Shankar** (https://hamel.dev/blog/posts/evals-skills/)
  - **Error analysis on traces first**, before adding knowledge.
- **Addy Osmani, "Audit your agent files"** (https://addyosmani.com/blog/audit-your-agent-files/)
  - Across 100 repos: 62% had linter-type rules in agent files, 42% had context bloat.

## 4. Keeping learnings from bloating

- **Compound engineering (Every / Kieran Klaassen)** (https://every.to/guides/compound-engineering)
  - The loop is plan → work → review → compound.
  - A prevention strategist is part of the compound step.
  - Learnings go into searchable `docs/solutions/*.md` files; only durable rules reach the root file.
- **ACE**
  - Itemised bullets with IDs and helpful/harmful counters, changed only by delta edits.
  - **Never let an LLM rewrite the whole learnings file** (context collapse: 18,282 → 122 tokens, below baseline).
- **Claude Code auto-memory shape:** a one-line-per-entry index with a hard cap, and detail in topic files.
- **Promotion ladder:**
  1. Append-only log.
  2. Curated, searchable entry.
  3. Root-file line, only if it applies universally.
  4. **Lint rule, test, hook or permission**, and the prose version is deleted.
  5. Expiry based on retrieval hit counts; re-evaluate after model upgrades.

## 5. Recommended stack for a small team

1. **Diagnose before adding context:** label 20–30 failed transcripts by failure mode.
2. **A lean root AGENTS.md** (about 150 lines or fewer, under 32 KiB) with invariants, commands and a compressed canon index
   (or inject the index from a SessionStart hook, under 10k characters).
3. **Path-scoped rules** for each area.
4. **One skill per workflow**, under 500 lines, with explicit triggers; mirror them to `.agents/skills` for Codex.
5. **Hybrid search CLI** (qmd or SQLite FTS5) over the canon and learnings, returning snippets plus paths.
6. **Hooks:** SessionStart injects the index; UserPromptSubmit injects the top 3–5 learnings; PreToolUse **blocks** known-bad actions.
7. **A canon-researcher subagent** returning 1–2k-token digests; keep main context use under 40–60%.
8. **An ACE-style learnings pipeline** with delta edits, a hard cap on the index, and CI failing when the cap is exceeded.
9. **Governance:** one owner for agent config, a monthly audit, re-tests after model releases.

Skip for now: Graphiti/Zep, Mem0/Letta, the reference memory server, Context7.
