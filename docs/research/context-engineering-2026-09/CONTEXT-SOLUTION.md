# Context, memory and knowledge: why we lose to a direct prompt, and the fix

**Written:** 2026-09-25, from a research sweep of frontier-lab engineering posts, ~80 papers, generative-media companies,
coding-agent tooling and practitioner talks. The sweep is in five appendices in this folder (`01`–`05`), each with URLs.
**Status:** a proposal. Nothing here changes Canon, Registry, routing, runtime or CONTROL-STATE. Adoption is a Controller decision.
**Labels:** **[evidence]** = a published source (see the appendices). **[observed]** = measured in this repo today.
**[inference]** = our reasoning.

---

## 0. The answer on one page

**The problem is not that the Canon is too big for the models' memory. We are putting knowledge in the wrong place.**

The whole industry has converged on one rule: **knowledge does not travel to the generator as text.**

- **Runway:** every production video model hides "a complex prompt completion pipeline". Model-specific craft lives only there.
- **Higgsfield:** replaced prompting with 1,500+ tested presets.
- **HeyGen:** passes brand context as IDs and applies it in code.
- **Adobe, Typeface and Google's ABCD Detector:** turn guidelines into **pass/fail checks run after generation**.

The research says the same:

- **Constraints multiply failure.** Whole-prompt accuracy drops from **~58% with 3 constraints to ~4% with 10** (GenEval 2).
- **Long prompts lose.** Every tested image model degrades past ~250 tokens (DetailMaster).
- **LLM rewrites can lose to the raw prompt.** A text-only LLM rewrite scored **below the raw prompt** (FaithRewriter: 59.1 vs 62.1).
- **Expansion adds diversity, not fidelity.** Google's own prompt-expansion paper says expansion "can never be expected to increase the degree of alignment".

**What we do [observed]:**

- **Still prompts are ~260 words.** Our deterministic builder produces 252–266-word still prompts (about 340 tokens) for the Mokobara example board.
- **Each prompt carries 25+ constraints.** They include a full description of the protagonist, the bag, the island and the grade, **in every shot**. The first shot is a close-up of a hand scratching rock, and it still describes the bag down to its zip pulls. The prompt ends with five "no …" clauses.
- **Image-to-video prompts re-describe the still.** They run 82–136 words. Runway says re-describing the still "can lead to reduced motion or unexpected results".
- **The planner reads a large doctrine payload.** P1's chef is given the ten doctrine packs (~25k tokens) plus a tray.
- **Planning costs more than generation.** On the P1 v1 live poster, **USD 1.87 of 2.28 was reasoning**.
- **Our only knowledge-vs-no-knowledge test never looked at media.** It compared *plans* scored by an LLM, never finished media against a direct prompt. Its judge also said the winners won on **form, "and none of them is knowledge"** (`canon/validation/blind-comparison-2026-09-22/RESULT.md`).
- **The cause:** a customer's direct prompt has 2–4 constraints, is in the model's native caption style, and gets the vendor's own tuned rewriter. **That is why it wins.**

**The fix, in one sentence:** the Canon should shape the plan, drive the choice of tested recipes, and power the checks. The generator itself should get a short prompt (**4–6 must-haves, 30–80 words**) in its own dialect. We buy quality with **parallel candidates plus calibrated checks** instead of longer prompts. And every piece of knowledge has to **beat a permanent direct-prompt baseline in paired tests** before it may touch a generation prompt.

The same principle fixes the coding agents (Claude Code, Codex): a tiny always-loaded map, retrieval on demand, rules enforced by code, and learnings curated rather than accumulated. See §6.

---

## 1. Diagnosis: why the pipeline produces worse media than a direct prompt

Ranked by strength of evidence × fit to what we observe:

| # | Mechanism | Evidence | What we do today [observed] |
|---|---|---|---|
| 1 | **Constraint count multiplies failure.** Whole-prompt success ≈ product of per-constraint success. | GenEval 2 (58% → 4% from 3 → 10 atoms; best model 85% per atom but 36% per prompt). DetailMaster (all models decline past ~250 tokens; attributes ~50%). | 25+ atoms per still. Every anchor restated in every beat. Continuity + must-not + look + product paragraph. |
| 2 | **Off-distribution language.** Models were trained on short, literal visual captions; persuasion and craft vocabulary has no visual grounding. | DALL·E 3 recaptioning; Ideogram 4 "plain text will not work"; FaithRewriter (LLM rewrite < raw prompt); RePrompt ("stylistic or unrealistic content"). | "Direction: endurance — he has been here a very long time."; "the pull-back is the reveal of scale (the marks = years)". These are director's notes, not captions. |
| 3 | **Truncation and position.** CLIP sees 77 tokens (effective < 20); T5 truncates silently at 256/512; FLUX weights the first words. | diffusers docs; Long-CLIP; BFL FLUX.2 guide; OPT2I (the winning rewrites *move ignored elements to the front*). | The style line comes first; the thing that matters in the shot may sit behind 150+ words of identity anchors. |
| 4 | **Negatives prime the thing they forbid.** | BFL: "no negative prompts"; Google: use semantic negatives. | Each still ends with "No text, no lettering, no captions, no logos, no watermark…". The P1 builder adds a 13-item negative list. P1 v1 got a drawn "SUPPLIED" label (recorded in `product/prompts.py`). |
| 5 | **Double rewriting.** Vendors rewrite our already-expanded prompt again. | Veo 3/3.1 rewriter "can't be disabled"; OpenAI `revised_prompt`; Qwen/Wan expansion. | Veo 3.1 is our main video route. |
| 6 | **Over-specification overrides the model's taste and suppresses motion.** | Google Prompt Expansion (no gain on specific queries); Runway i2v guide; PromptEnhancer regresses on text layout. | Image-to-video prompts re-describe the still and fix the camera, the impact and the sound all at once. |
| 7 | **A plan that is too hard to execute.** Every shot generated independently with many actions leads to hands, drift and colour change. | Customer on the P1 v1 reel: "two random hands, too many AI slops, robotic; the yellow colour is changing". | The P1 v2 spec already addresses this (master plate, feasibility). Good. |
| 8 | **No ablation, so every fix breaks something else.** A global prompt or rule edit changes many atoms, their order and the length at once, and its sign differs by model and brief. | OPT2I, Promptist and RePrompt work only because a measured reward closes the loop. ETH's AGENTS.md study: context files often *reduce* success and add 20% cost unless evaluated. | No standing direct-prompt arm; no media-level A/B; rules promoted by argument, not by a paired win. |
| 9 | **Knowledge gets written twice**, once into the planner's context and again into the prompt. Tokens and cost go to the wrong stage. | Anthropic: "smallest possible set of high-signal tokens"; IFScale: rules get silently dropped as they multiply. | ~25k tokens of packs to the chef; reasoning cost > media cost on the accepted poster. |

**What we are *not* doing wrong:**

- Composing exact text in code (mechanism B).
- A deterministic prompt builder.
- Per-shot forms.
- A master plate and continuity owner (P1 v2).
- Binding checker verdicts.
- Human release.

Every source we read endorses all six. Keep them.

---

## 2. The principle: knowledge lives in five places, and "in the prompt" is last

Every Canon item gets exactly **one** job, and its job decides where it lives. This is what Typeface ("extract the rules,
categorize them, map them to the right channels"), Jasper (typed Brand/Marketing/Product layers) and HeyGen (IDs, not text) do.

| Canon item type | Example | Where it lives | Mechanism |
|---|---|---|---|
| **1. Deterministic spec** | aspect ratios, safe zones, logo rules, contrast minimum, copy ≤ N chars, fonts | Code | Compositor + gates. *Never prompted.* (We already do much of this.) |
| **2. Check** | "brand visible in first 5 s", "product is the largest object", "one action per clip", "no extra hands" | **Check registry** | DSG-style yes/no questions run after generation, each with a method (code / detector / VLM), evidence and a repair hint. Google ABCD Detector / Adobe per-rule pass/fail shape. |
| **3. Recipe ingredient** | "hero still on nano-banana then Veo i2v, camera orbit, product unchanged" | **Recipe library** (presets) | Tested model + params + slot template + references + checks + known failures. The planner picks a recipe ID and fills slots. Higgsfield pattern. |
| **4. Model prompt craft** | "Veo: motion-only for i2v", "FLUX: subject first, 30–80 words, no negatives" | **Per-model adapter** (one small versioned file per model) | Renders the IR into that model's dialect. Only the adapter knows it; the planner never sees it. Runway/Veo/DALL·E rewriter pattern. |
| **5. Strategic heuristic** | "one clear idea", "first frame already contains the gag", "declare deviations", "brand inside 10 s" | **Planner context**, retrieved per job class, **≤ ~15 items** | The only type an LLM reads before deciding. |
| **6. Fact** | product parts, claims, customer photos, prices | **Job dossier / customer shelf** | Retrieval by ID; never generic Canon. |

**Consequence:** the Canon stops being a *payload* and becomes a *compiler input*. From it we compile recipes, adapters,
checks and a short heuristic card for the planner. The 1,300-claim corpus stays as the source of truth and for provenance,
but runtime never reads the raw corpus.

Our blind comparison already hinted at this. The winning boards won on **form** (a `first_frame` containing the idea,
one job per clip, declared deviations). Those are type-5 heuristics that became form fields, which is exactly the right move. More of the Canon
should become form fields, checks and recipes, and less should be injected prose.

---

## 3. Target runtime architecture (customer → media)

```
customer words (verbatim, never edited)
   │
   ▼
[1] Intake / waiter (cheap LLM) ──► vagueness score + job class + facts + questions
   │
   ▼
[2] Planner / chef (strong LLM)   reads: intent + job-class heuristic card (≤15 items, ~1–3k tokens)
   │                               + RECIPE MENU (ids + one line each) + feasibility
   │                               writes: IR (structured, controlled vocabulary, atom budget)
   ▼
[3] Recipe binding (code)         IR → recipe id → model, params, refs, slot template, check list
   ▼
[4] Per-model adapter (code)      IR slots → prompt in that model's dialect, within its budget
   │                               (+ a DIRECT arm: customer words + refs, same model)
   ▼
[5] Generate N in parallel        seeds × {compiled, direct} × (optionally) 2 models; references and edits over text
   ▼
[6] Verify & select (code+VLM)    hard filter: check registry (atomic yes/no, per must-have)
   │                               rank: preference model (HPSv3/PickScore) + intent VQA
   │                               tiebreak: pairwise VLM; judges calibrated on OUR accept/reject labels
   ▼
[7] Compose (code)                exact text, logo, end card (mechanism B, unchanged)
   ▼
[8] Customer: accept / specific repair / reject
   ▼
[9] Learning (offline)            outcome → delta to a recipe / adapter / check / heuristic (never prose append)
```

### Rules that make it work

**R1. The IR has an atom budget.**
- Each shot carries **4–6 must-have atoms**, and **only for what is in frame** (an anchor is restated only if that object is visible in that shot).
- Everything else becomes `nice_to_have`, a check, or compositing.
- Keep `intent_verbatim` and pass it to every stage.
- Controlled vocabularies for framing, angle, lighting, style and camera move, each value mapped per model to tested phrasing.

**R2. Adapters enforce the vendors' own guides.** They are tested with golden prompts whenever the vendor ships an update.

| Model family | Budget and shape |
|---|---|
| FLUX.2 / Seedream / Imagen / nano-banana stills | 30–80 words, subject → action → setting → style, positive phrasing, state the use ("a product ad photo for…"), no negative sentences |
| Image-to-video (Veo i2v, Kling, Runway, Seedance) | **Motion and camera only**, 1–3 sentences; never re-describe the image; identity comes from the frame and the references |
| Veo t2v | Short and literal, because Google's rewriter will expand it again |
| Ideogram 4 | Its JSON schema |
| gpt-image / Gemini edits | "Change only X; keep everything else the same" |

**R3. "No X" becomes a positive state or a check.**
- "No text in image" → "clean, unmarked surfaces"; then an OCR check rejects any image with lettering.
- "No extra hands" → a hand-count check.

The model never reads the forbidden word.

**R4. Identity comes from pixels, not paragraphs.** Escalate in this order:
1. Product and character reference images, plus a master plate (already in P1 v2).
2. An edit model from the master plate.
3. **A small per-product/per-character LoRA** (minutes to train, 3–30 images; Higgsfield Soul ID, Krea, Firefly custom models) when the look keeps landing "almost right".

A 120-word description of the bag is a worse identity carrier than one reference image.

**R5. Spend on candidates, not words.**
- With per-sample acceptance p, the chance that at least one of N is acceptable is 1−(1−p)^N. At p = 0.3, **N = 4 gives 76%** (the arithmetic is sketched after these rules).
- Stills are cheap. Generating 4 stills plus scoring usually costs less than one LLM planning round plus a customer revision round, and it runs in parallel, which cuts TpAO.
- For video, generate N candidates **only for the risky shots**, and only after the still is selected.
- Google's inference-time-scaling paper: a smaller model with search beat a bigger model without it.

**R6. Judges are atomic and calibrated.**
- Holistic VLM "which is better?" matches humans only **49%** of the time (GenAI-Arena).
- Atomic yes/no questions (DSG, VQAScore) and learned preference models (PickScore 70.5% vs human experts 68%) are reliable.
- Calibrate each judge on our own accepted and rejected media, and re-qualify it on model changes. P1 v2's "judges qualified only by a recorded live run" is exactly right.

**R7. The direct arm is permanent.** Every job generates at least one candidate from the customer's own words (plus references) on the same model. If it wins selection, that is a free lesson about which of our constraints hurt.

**R8. Rewriting only when measured.**
- Concrete requests: pass them through unchanged.
- Vague requests: light expansion into caption style.
- Failed atoms: targeted delta edits (move the missing element to the front, or elaborate only it). OPT2I.
- Never stack our LLM rewrite on top of a vendor's rewriter without a measured win.

Here is the R5 arithmetic in full [inference]:

```
P(≥1 acceptable in N) = 1 − (1 − p)^N
p = 0.30:  N=1 → 30%   N=2 → 51%   N=4 → 76%   N=8 → 94%
p = 0.15:  N=4 → 48%   N=8 → 73%
CpAO ≈ (N·c_gen + c_judge·N + c_plan) / P(accept on round 1) + revision cost × P(revision)
```

The lever is p: short prompts on a tested recipe raise p. N and a good selector turn p into round-one acceptance.
Measure p per recipe; it goes into the router.

---

## 4. Reshaping the Canon (the migration)

1. **Tag every accepted claim and pack rule with one of the six types in §2**, using an LLM plus human review, once, offline.
   Expect most items to be type 2 (check) or type 5 (heuristic), and very few to belong in a prompt at all.
2. **Compile type 2 into `checks/registry.yaml`**, one row per check:
   - `id`, `applies_to` (job class, channel, time window);
   - `method` (code / detector / vlm_yesno);
   - `question`, `pass_if`, `repair_hint`;
   - `source_claims[]` (provenance back into the Canon).
   Model it on Google's open-source `abcds-detector/features_repository.py`.
3. **Compile type 3 into `recipes/*.yaml`**, starting with the 3–5 production classes we have actually shipped. Each recipe holds:
   - model and params;
   - slot template;
   - required references;
   - checks;
   - known failure modes;
   - measured p (acceptance), cost and time;
   - version.
4. **Compile type 4 into `adapters/<model>.yaml`**: budget, slot order, phrasing map, rewriter on/off, and golden tests.
5. **Compile type 5 into one heuristic card per job class** (≤15 items). This is what the planner reads instead of ~25k tokens of packs.
6. **Keep the corpus as it is** for provenance and search, behind a hybrid (BM25 + embedding) search tool that returns snippets with IDs. The planner may call it on demand, with every call logged, as Ruling 4 already requires.

The compiled-pack machinery (`canon/compilation/`) and the marker map are the right *engine* for this. Point their output at checks,
recipes, adapters and cards instead of at an injection payload.

---

## 5. The discipline that stops "every fix breaks something else"

This is the most important section. The research is unanimous that knowledge only helps when a **measured loop** decides where it goes.

### 5.1 The bake-off (run this first, before building anything)

- **Golden set:** 20–30 real briefs, drawn from the accepted and rejected cases plus marketplace briefs. Split by class: static ad and product film.
- **Arms**, per brief, same model, same references, same seeds where possible:

  | Arm | What is sent |
  |---|---|
  | **A — Direct** | the customer's words + references → model (vendor rewriter on) |
  | **B — Direct, clean** | A + the use statement ("an Instagram product ad") + aspect ratio |
  | **C — Short compiled** | IR through a per-model adapter (≤80 words stills, motion-only i2v, ≤6 atoms) |
  | **D — Current pipeline** | today's builder output |

- **Judging:**
  - The founder (and ideally 1–2 customers) rank blind, per brief.
  - Record accept / near-miss / reject.
  - Also log check pass rates and cost.
- **Cost:** stills only at first. 25 briefs × 4 arms × 2 samples ≈ 200 images, roughly USD 10–40 on nano-banana- or FLUX-class pricing. This needs a signed spend record under C-6a. **[inference; confirm prices from the price book]**
- **Decision rule:**
  - If A or B ≥ D, the enrichment is net harmful for stills, and §3 is the build plan.
  - If C > A, then compiling (not enriching) is where the value is.
  - Then repeat for image-to-video shots.

### 5.2 Ablation as a permanent gate
- **Promotion rule:** a knowledge item may enter a *generation prompt* only after it wins a paired comparison (with vs without it: same brief, model and seed) at a pre-registered margin over enough pairs. The target is ~100 pairs stratified by model and class. While data is thin, use a sign test and Bradley-Terry fits across jobs.
- **Where losers go:** until it wins, the item lives in checks or the planner card, not in the prompt.
- **Regression suite:** the golden set re-runs, as a paid, capped batch, on every change to an adapter, recipe or card. This is the direct cure for whack-a-mole.
- **Router:** a contextual bandit over (model × recipe × strategy), with reward = accept − λ·cost − μ·time. The direct arm keeps a **5–10% floor forever**, to catch vendor model and rewriter updates.

### 5.3 Learnings: a curated playbook, never a growing pile
The evidence is ACE, ExpeL, Letta, Every's compound engineering and the Claude Code auto-memory design.

- **Raw job records** stay append-only and are **never loaded wholesale**. Retrieve them only by ID or search.
- **Each lesson becomes a delta against a specific artifact:** a recipe, adapter, check or heuristic card. It carries:
  - `id`, scope, evidence (job ids, before/after), status and `supersedes`;
  - helpful/harmful counters.
- **Merge deltas by code, never by an LLM rewriting the whole file.** ACE measured a single rewrite collapsing an 18,282-token playbook to 122 tokens, with accuracy dropping below the no-memory baseline.
- **Promotion ladder:**
  1. raw record;
  2. candidate lesson;
  3. validated entry (wins a paired check or recurs ≥ N times);
  4. **check / recipe / adapter change**, after which the prose is deleted.
  Entries whose counters reach zero are retired. Entries are re-validated after model upgrades.
- **Consolidation runs offline in batch**, with PR review. `/media-agency-sync` already has this shape; aim its output at deltas.
- **Only promote on grounded feedback:** a customer verdict, a check result, or a baseline comparison. Memory that is not grounded propagates errors ("experience-following", arXiv 2505.16067).

---

## 6. The coding-agent side (Claude Code, Codex)

The same principle applies when agents build and operate this repo.

**[observed]**
- There is **no root `AGENTS.md` or `CLAUDE.md`**, so nothing loads automatically.
- The entry point is a 38 KB `PROJECT-MEMORY.md` that agents must be told to read.
- `canon/` holds ~2M tokens of Markdown and ~21 MB of YAML.

**[evidence]**
- Keep the root file to about 100 lines. That is OpenAI's Codex team figure, with Anthropic's limit under 200 lines and HumanLayer's under 60.
- Codex hard-caps all AGENTS.md at **32 KiB** and silently drops files past it.
- Claude Code: "Bloated CLAUDE.md files cause Claude to ignore your actual instructions".
- Models reliably follow ~150–200 instructions, and the harness uses ~50 of them.
- Vercel measured an **8 KB compressed docs index in AGENTS.md at 100%** pass rate, versus 79% for skills with explicit instructions and 53% for skills by default (unused in 56% of runs).
- Hooks are the only guarantee; prose is "a request, not a guarantee".
- Context quality starts to drop at roughly 40% window use (Horthy's "dumb zone").

**Do:**
1. **Add a root `AGENTS.md` (≤100 lines) and a `CLAUDE.md` containing `@AGENTS.md`.** It holds:
   - what the project is;
   - the five authorities (one line each);
   - the ~15 non-negotiables;
   - commands;
   - explicit skill triggers ("for any media job, invoke `media-agency` first");
   - a pointer to the index.

   A draft is in `proposed-AGENTS.md` in this folder.
2. **Add a generated `canon/INDEX.md`** (≤8 KB, pipe-delimited: `path | what | when to read`). Regenerate it in CI. Never `@import` Canon files.
3. **Hooks:**
   - A SessionStart hook (including after compaction) prints the index and the current CONTROL-STATE line, under 10k characters.
   - PreToolUse hooks **block** the known-bad actions: writes to `canon/**`, the Registry and `coordination/**` outside the sync skill, and paid dispatch without a cap record.
4. **A `canon-researcher` subagent** reads the corpus and returns 1–2k-token digests with claim IDs, so the main context stays clean.
5. **Research → Plan → Implement**, with written artifacts and a fresh context per phase. Humans review the plan.
6. **Mirror the skills to `.agents/skills`** for Codex. Keep SKILL.md under 500 lines with references one level deep.
7. **Evaluate every change to agent context** on 5–15 tasks that failed before. ETH found auto-generated context files *reduce* success, so write them by hand and keep them short.

---

## 7. Fine-tuning, LoRA and small models: where they fit

| Use | Verdict | Why |
|---|---|---|
| Fine-tune an LLM on the Canon ("teach it Ogilvy") | **No** | New knowledge learns slowly and *raises* hallucination (Gekhman). RAG beats unsupervised fine-tuning (Ovadia). It is impossible on Claude/GPT anyway. |
| **Per-product / per-character LoRA** on the image model | **Yes, when references aren't enough** | Industry standard for identity and style: minutes of training, 3–30 images (Soul ID, Krea, Firefly). fal hosts trainers. Directly targets "the bag changed between shots". |
| **Small models as judges and classifiers** (job class, lesson de-duplication, hand-count, OCR, preference) | **Yes** | 10–30× cheaper (NVIDIA SLM paper). Checks run on every candidate, so they must be cheap. |
| **A learned rewriter / fixed templates** | **Later, once there are logs** | RL-trained rewriters (Promptist, RePrompt, PromptEnhancer) beat hand rules. A learned 64-token template matched a per-request creative agent at 4.8× lower cost. Needs our accept/reject data first. |
| **Performance-trained copy / creative model** | **Later** | Meta's AdLlama: RL on CTR gave +6.7% CTR. Needs performance data. |

---

## 8. The 30-day plan

| Week | Do | Done when |
|---|---|---|
| 1 | **Bake-off §5.1 on stills** (A/B/C/D, 25 briefs). Write adapter v0 for the 2 still models we use. Add a prompt linter: word budget, atom count, negation sentences, image-to-video re-description. | A signed result: which arm wins, per class. A linter run over all past job prompts. |
| 2 | Per-shot anchors only for objects in frame. **Motion-only image-to-video prompts.** Positive phrasing plus checks instead of "no X". Best-of-4 stills with a hard filter (OCR, hand count, product-similarity) plus a preference rank. | Bake-off arm C re-run; image-to-video bake-off on 10 shots. |
| 3 | Tag the Canon into the six types (pilot: 2 packs). Build `checks/registry.yaml` v0 (~30 checks) and heuristic cards for the 2 shipped classes. Replace pack injection in the chef with the card plus the recipe menu. | The chef's context drops from ~25k to ≤5k tokens; plan quality unchanged or better on the blind board test. |
| 4 | Recipes v0 for the shipped classes, with measured p, cost and time. Direct arm wired in as a permanent candidate. Learnings as deltas with counters. Root AGENTS.md, index and hooks. | Golden-set regression runs on every change; the dashboard shows CpAO and TpAO per recipe against the direct arm. |

## 9. Stop doing

- Restating every identity anchor in every shot.
- Writing "no X" sentences to a generator.
- Re-describing the still in image-to-video prompts.
- Injecting doctrine packs into the planner by default.
- Judging plans in place of media.
- Holistic "is it good?" VLM verdicts as release gates.
- Promoting a rule by argument.
- Letting an LLM rewrite a whole learnings file.
- Growing always-loaded agent files.

## 10. Honest limits

- No paper compares "a rule in the prompt" head-to-head with "the same rule as a check" for ad creative. The recommendation rests on converging evidence plus vendor practice. The bake-off is how we find out for *our* briefs.
- Several numbers are vendor-reported (Pencil, Mem0, Zep, Higgsfield) or come from pages we could only see as search extracts. Each appendix labels them.
- The atom and word budgets are starting points taken from the vendor guides and GenEval 2. Tune them per model with the bake-off.
- Our observed prompt lengths come from the agency-skill builder on the Mokobara example board. P1's `product/prompts.py` has the same structure but was not measured on a live recipe here.

## Appendices (this folder)

- `01-FRONTIER-LABS.md`: Anthropic, OpenAI/Codex, Manus, Cognition, LangChain, Chroma, HumanLayer, Vercel, Cursor, Factory, Letta, ETH.
- `02-RESEARCH-PAPERS.md`: long-context failure, memory architectures, fine-tuning vs RAG, rule compliance.
- `03-GEN-MEDIA-COMPANIES.md`: Runway, HeyGen, Higgsfield, Adobe, Typeface, Jasper, Canva, Synthesia, Midjourney, Krea, Google, Meta, TikTok, Invideo, Luma.
- `04-TOOLING-AND-PRACTITIONERS.md`: Claude Code / Codex / Cursor / Gemini mechanisms and limits, search tools, talks, learnings pipelines.
- `05-ENRICHED-VS-DIRECT-MEDIA-PROMPTS.md`: model prompt guides, prompt-rewriting research, best-of-N and verifiers, ablation design.
- `proposed-AGENTS.md`: draft root agent file (not active).
