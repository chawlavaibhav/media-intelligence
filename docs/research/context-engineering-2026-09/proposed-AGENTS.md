<!-- DRAFT, not active. Proposed root AGENTS.md (with CLAUDE.md = "@AGENTS.md"). See CONTEXT-SOLUTION.md §6.
     Budget: ≤100 lines, ≤8 KB. Every line must answer "would removing this cause a mistake?" Nothing inferable from code. -->
# Media Intelligence — agent entry point

An API-native media production layer: customer brief → plan → tested recipe → generation → checks → accepted media.
Primary metrics: **CpAO** (cost per accepted outcome) and **TpAO** (time to accepted outcome), against a direct-prompt baseline.

## Authorities (never substitute one for another)
- What is authorised, incl. money → `coordination/CONTROL-STATE.md` + `coordination/decisions/` (newest durable decision wins)
- What happened → committed evidence + `verify/VALIDATOR-INDEX.yaml`
- What a good outcome must achieve → Canon (`canon/INDEX.md` → the file it points to)
- What models can do today → `eval/capability-map/ROUTING-EVIDENCE-MAP-v0.yaml` + `TAINT-REGISTER-v1.yaml`
- What happened on real jobs (directional, n small) → `production-learning/cases/`
- Project map (not authority) → `PROJECT-MEMORY.md` — read the section you need, not the whole file

## Non-negotiables
1. No paid call without a job-specific spend cap stated in this session; every attempt is ledgered; no hidden retry.
2. Exact text, prices, logos, CTAs are composed by code onto textless plates — never generated.
3. Only a human accepts or releases. Gates passing, a judge liking it, or you liking it is not acceptance.
4. Do not modify `canon/**`, `eval/registry/**`, `eval/capability-map/**`, sealed evidence or `coordination/**`
   except through the owning workflow (e.g. `/media-agency-sync`). Record gaps; propose, never apply.
5. A checker's "no" is binding; only the founder overrides, in writing.
6. Generation prompts: ≤6 must-have atoms, only objects in frame, positive phrasing (no "no X" sentences),
   image-to-video = motion + camera only. Knowledge goes to plan, recipe, adapter or check — not into the prompt.
7. Every change to a prompt adapter, recipe or heuristic card is judged against the direct-prompt arm on the golden set.
8. Video is judged on sampled frames, never the source still.

## Skills — invoke explicitly
- Any request to make/edit/repair/plan commercial media → invoke `media-agency` first, before reading anything else.
- Integrating finished jobs' learning → invoke `media-agency-sync`.

## Finding knowledge (do not bulk-read)
- Start at `canon/INDEX.md` (generated: path | what | when). Open only the files it points to.
- Prefer retrieval from the repo over prior knowledge for anything about models, prices, routes or doctrine.
- For broad Canon questions, delegate to a research subagent and ask for a ≤2k-token digest with claim ids.
- Never load `production-learning/` or `canon/knowledge/` wholesale; search by id or keyword.

## Commands
- Runtime tests: `python3 -m unittest discover -s runtime/tests -p 'test_*.py'`
- Gate regression: `python3 -m tests.test_gate_regression_battery --table`
- Dry chain: `python3 -m runtime.alpha.cli` (see `runtime/ALPHA-1.md`)
- Stage completeness for an agency job: `python3 .claude/skills/media-agency/tools/check_stage.py <job_dir> --through <N>`

## Working style
- Research → plan → implement; write the plan to a file; start implementation from the plan, not the chat.
- Keep a progress file for long work; keep the list of changed files in it (summaries lose it).
- When compacting, preserve: the goal, decisions made, files changed, spend so far, open checker verdicts.
