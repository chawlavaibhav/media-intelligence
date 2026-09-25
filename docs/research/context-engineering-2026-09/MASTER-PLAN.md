# The plan: how to reach the golden benchmark

**Written 2026-09-25.** A synthesis of five sources:
- the complete project history (`MEDIA-HISTORY.md`, 6 Jul–25 Sep; cited [00]–[08]);
- an external research sweep (`CONTEXT-SOLUTION.md` + appendices `01`–`05`);
- six independent persona reviews (`personas/P1`–`P6`): product strategist, ML systems architect, creative director, evaluation scientist, operator, red-team skeptic.

**Status:** a proposal for the founder. It changes no code, Canon, routing or control state.

---

## 0. The golden benchmark (the founder's words, fixed)

> A pipeline on a web address. A customer comes in, chats, types the media they want. The pipeline understands the
> meaning, writes a recipe/script, sends it to media model(s), and returns the media. We optimise **CpAO** (cost per
> acceptable outcome) and **TpAO** (time to acceptable outcome), and the outcome must be **much, much better than a single
> prompt sent directly to a media model**.

The founder's own test for any design (25 Sep): **beats one direct prompt** and passes **"would I pay for this?"** on a
**fixed set of briefs**. This plan makes that test the machine everything runs through.

## 1. What 80 days actually proved (one screen)

- **About US$340 spent.** It produced 8 founder-accepted deliverables (≈US$34) and **0 accepted outputs from the automated product** [00 §4].
- **Every accepted piece was hand-authored by one session:** Mokobara v2, RentOK V2, the Upwork intro. Every automated or split-author film was rejected [00 §5.2].
- **Twice, one Claude session writing Veo prompts directly beat the whole kitchen.** On Ascend: about 6 minutes and about US$5, against 1 h 06 m and US$9.44 [05 §15].
- **What reliably worked was deterministic and visible:**
  - code-set text (4/4 against 0/4);
  - real product photos (a new product drawn from scratch: 0/6);
  - still first, then animate;
  - blind judging;
  - free animatics before spend [00 §5.10].
- **What reliably failed:**
  - voice (9 jobs);
  - continuity between shots (7);
  - slideshow instead of film (6);
  - asking a model for the impossible (6);
  - no automatic judge ever qualified [07].
- **Fixes and decisions did not stick.**
  - 27 of 39 repeating failure types were "fixed" only by a note.
  - At least 25 decisions were reversed, most after a single rejected output.
  - The chef card went through 13 versions in 26 hours [04][05].
- **Demand went unused.** Real demand ("edit my photo", "animate my image") was measured on 26 Aug and never became the product [02].
- **No outside judge.** There has been no paying customer, and no outside judge has ever scored the work [00 §5.9].

## 2. What all six reviewers agree on

The six personas were each given the full history and a different lens. They converged on these points. This is the
strongest signal in this document.

| # | Consensus finding | Consequence |
|---|---|---|
| 1 | **The real bar is "one strong author writing directly for the model" (B1), not raw words (B0).** That is what beat us, and any buyer can do it with ChatGPT or Gemini | Every test has three arms: B0, B1, and our pipeline P |
| 2 | **The creative layer as built (Canon injection, the kitchen of roles, prose cards) is falsified;** a finishing layer is not | Kill the kitchen; keep and extend deterministic finishing |
| 3 | **Authorship must not be split.** One strong model, in one context, holds the brief, the photos and the idea when it writes | One author call, not stations or forms |
| 4 | **Films were killed by chopping** (still → 2–4 s muted clip → words by code) and by fallbacks that swap motion for stills | Whole scenes in the model's own unit (e.g. 8-s Veo with native sound); a scene is never replaced by a still |
| 5 | **Unqualified judges must never veto.** Only measurable faults may block | Hard checks are code or narrow detectors; taste is decided by a human pick |
| 6 | **No change without a fixed benchmark.** A rejected output becomes a ticket or a new brief, never a design change | Frozen brief set, pre-registered rules, weekly cadence |
| 7 | **Point at real demand** (product stills, photo edits, animate-my-image, short product films), and test films in week 1 as well | A format menu with a refusal list; a class ships only when it passes |
| 8 | **The value a buyer can see** is real product pixels, exact Indian-language copy, every format, timed voice, cheap revisions, brand memory, and a choice of candidates | The product is "Author + Finish + Choose" |
| 9 | **The Canon is frozen.** At most it becomes a ≤15-question critique card and a copy reviewer, and it must win an ablation on finished media before it goes anywhere else | No Canon work for 30 days, beyond one ablation |
| 10 | **Operate with one writer, a generated state file and a short AGENTS.md;** no mid-order changes, no fan-out swarms | Consolidate the repo; the bench is the only road to production |

## 3. The corrected diagnosis: why we lose to a direct prompt

1. **We competed with the author instead of amplifying it.** The pipeline split the author across stations, forms and code-built prompts. The winners kept one author with everything in view [04 §4.5][05 §15.4].
2. **We chopped films into pieces that fail multiplicatively.** Eight independent beats at a 50–70% keep rate almost never all work. The winners used 3–4 whole scenes [05 §7.6].
3. **We gave vetoes to judges who had never qualified**, and wrote yesterday's model limits in as rules. The result was films that were "correct and lifeless" [00 §5.5].
4. **We had no baseline and no regression set.** Each fix was fitted to one output and broke something else [00 §5.8].
5. **We built for the hardest class, with no customer.** The founder was the only judge, on his own briefs, while measured real demand was ignored [00 §5.9][02].

*Correction to our own research (`CONTEXT-SOLUTION.md`):*
- **Prompt hygiene is a secondary cause.** Long, constraint-heavy prompts, negatives and re-described stills do hurt, but they are not the main problem. CQ-001 lost only 1 of 16 creative decisions at the prompt step [04 §4.2].
- **Our own wins break the rule.** The accepted Mokobara v2 and the winning direct-Veo prompts repeated anchor blocks and used a negative line.
- **Its code-compiled prompt adapters are withdrawn.** Code-built prompts caused F10, F15 and F27 and the Mokobara v3 prompts. The author LLM writes the prompts, reading a one-page style guide per model; code only lints them and returns them once.
- **Its stills-first bake-off becomes films-in-week-1.**
- **Its preference-model auto-selection and bandit router are deferred** until labels exist.
- **What stands:** knowledge out of generator prompts; identity carried by references, not paragraphs; a permanent direct arm; lessons stored as evidence-backed deltas; nothing promoted by argument.

## 4. The product: "Author + Finish + Choose"

**Principle.** Don't try to make the pipeline smarter than the model. Use the **same strong author** a direct user would
use, then add only what a direct prompt cannot do, and let a human choose. The B1 output is always one of the candidates,
so, under a trusted pick, **the pipeline cannot deliver worse than direct**; it can only cost more, and that cost is what
we optimise.

### 4.1 Stages and what each one sees (context budgets)

| Stage | Who | Sees, and nothing else | Produces | Budget |
|---|---|---|---|---|
| 1 Intake | cheap LLM | the customer's exact words (stored once, never edited); uploads; brand-shelf summary | operation (make / edit / animate / film), format from the menu, exact copy, language, ≤2 questions (facts only the customer knows), scope change stated before spend | ≤3k tokens, ≤US$0.01 |
| 2 Brand shelf | code | — | logos, fonts, colours, product photos, facts from the site (with sources), past approvals and rejections; passed **by ID and as reference images**, never as prose | US$0 |
| 3 Ideas (films and hero stills) | strongest writing LLM, the "author" | the exact words, facts, photos, the format card (≤1 page), a one-page style guide per target model, the last 8 pieces made (to avoid repeats), 2 example films | **3 ideas** differing in premise, each a human truth + a moment + a key frame rendered as a cheap still | ≤8k tokens in; ≤US$0.50 including key frames |
| 4 Pick the idea | customer | the 3 key frames | the chosen idea; on "you choose" or silence, the author picks | US$0 |
| 5 Treatment + prompts | the same author, same context | the pick | a ≤150-word treatment, then per scene: a prompt in the model's own style, duration, references, at most one spoken line, on-screen copy, facts used with sources (strict JSON) | ≤US$0.30 |
| 6 Lint | code | the author's JSON | flags only: word budgets, positive phrasing, no copy or brand strings in prompts, motion-only for animate-a-still, voice-line fit (≤ shot − 0.4 s at ~2.5 words/s), nothing on the refusal list. Returned to the author **once**; **code never edits a prompt** | US$0 |
| 7 Generate | media models | only prompts + reference images | stills: 4 candidates (one is the B1 prompt); clips: whole scenes in the model's unit with native sound, 2 takes of the riskiest scene; a scene failing twice is rewritten or cut, **never swapped for a still** | per format |
| 8 Hard checks | code + narrow detectors | the rendered files | block only on measurements: exact copy, text bounds and contrast, stray lettering (OCR), aspect and duration, black frames, audio overlap, loudness (−14 LUFS, ≤ −1 dBTP), **motion present (optical flow; ≥70% of a film's runtime generated motion)**, product similarity to the reference | US$0–0.01 |
| 9 Finish | code | the chosen media + copy + logo + audio | exact text, logo, end card, every format recomposed (not cropped), timed voice if chosen, music | US$0 |
| 10 Choose | customer (founder during the exam) | 2–4 candidates, or raw and finished cuts | accept / "change only X" / reject with a one-tap reason. **The pick is the quality label** | — |
| 11 Revise | author + code | the one change | re-assemble or regenerate only that element | cheap |
| 12 Learn (offline) | batch job + PR | verdicts, picks, costs | per-class acceptance rate, CpAO and TpAO; examples library (accepted and rejected, with the customer's words); a format card, style guide or check changes **only after winning on the bench** | — |

**Never in any context:** Canon packs, failure-note trays, raw job logs, other jobs' plans.
**Ledger:** every call's inputs, seed, model version and cost are stored append-only, so any job can be replayed. The ledger is never loaded into a model's context.

### 4.2 The format menu (the class decides the unit, not the idea)

| Offer now (subject to the exam) | Evidence | Unit |
|---|---|---|
| S1 Product ad still / poster from the real photo, exact copy, 4 formats | NB2 / GPT Image 2 11/12; code text 4/4; P1 poster accepted | 4 stills → pick → compose |
| S2 Edit my photo ("change only X") | Seedream edit 10/12; top real demand | 2–4 edits → pick |
| S3 Offer/festive banner set with exact Hindi | code text 4/4 | stills + code text |
| M1 Animate my image (5–8 s) | Kling 8/8, Wan 8/8, Veo Fast 5/8 | motion-only prompt, 2 takes |
| M2 Product film, no people (15 s) | Mokobara v2 path; condensation-bottle test | approved stills → 2–3 whole scenes |
| F1 One-moment story film (15–20 s) | both direct-Veo wins; Mokobara v2 | 2–3 whole 8-s scenes with native sound + a real-product insert + end card |
| F2 Drawn explainer by code | RentOK, US$0.07–0.53 | code render |
| F3 One presenter to camera | Upwork V4.1; Veo speech 53/60 | whole scenes, native speech |

- **Rescope before spend:** hands working a product becomes a before/after; a new product uses real photos only; narration becomes on-screen words plus one in-scene line.
- **Refuse for now:** back-and-forth dialogue drama, lip-sync onto footage (0/5), films over 30 s that depend on shots matching, real or celebrity likenesses, and claim-heavy categories without a claim sheet.
- **Voice:** the default is **no narration**; keep native scene sound, one music bed or silence, and at most one short line per scene in the model's own voice. Narration returns only as a cast brand voice, auditioned on the full real script and chosen by ear.
- **Continuity:** one approved master picture per character and product; each scene starts from an edit of it, plus one fixed description sentence; at most 4 joins and no frame-chaining. Per-customer LoRA only for repeat customers with ≥3 jobs.

### 4.3 Where each kind of knowledge lives

| Knowledge | Lives in | Reaches a model? |
|---|---|---|
| Brand identity (logo, fonts, colours, product look) | brand shelf, as files and references | Only as reference images |
| Product facts and claims | brand shelf, with sources | The author, as ≤1k tokens of facts |
| Model craft ("how Veo wants to be prompted") | one-page style guide per model (versioned, bench-tested) | The author, ≤600 tokens per model |
| Format craft | one-page format card | The author |
| Creative doctrine (the Canon) | frozen; optional ≤15-question critique card + copy reviewer | Only after winning CANON-ABL-1 on finished media. Retrieval test (`eval/retrieval-canon-2026-09-25/RESULT.md`): classic RAG is near random on this corpus; a fixed core list + LLM lookup over a label index works best — no vector DB |
| What models can and can't do | equipment sheet (Registry rows + live stats, Clopper–Pearson) | The intake (for the menu and refusals) and the lint |
| Lessons | deltas to a card, guide or check, with evidence and counters | Only through those artefacts |
| Taste | founder and customer picks (labels) | Never as rules; later via qualified judges |

## 5. The exam (the benchmark every change must pass)

**Briefs: 30, frozen and hashed.** Weighted to real demand, in customers' own words, with real assets.

| Class | Tuning (dev only) | Exam |
|---|---|---|
| S1 product ad still (exact copy) | 1 | 5 |
| S2 edit my photo | 1 | 4 |
| M1 animate my image | 1 | 4 |
| M2 product film, no people | 1 | 4 |
| F1 story film with people (the lost ones: iPhone Duo, Ascend, Mokobara, ramen, tea seller) | 1 | 5 |
| F3 presenter / voiced | 1 | 2 |

Each exam brief carries:
- a price anchor ("would I pay ₹X");
- 4–6 yes/no must-haves;
- a hard-fail list, written before anything is generated.

The pipeline never sees the must-haves. At least 8 briefs come from real outside people (Rama, prospects, CANON-011).
Rotate 6 a month for real requests.

**Arms per brief** (same models and references where possible):
- **B0:** the customer's words straight to the class's best model (vendor rewriter on).
- **B1:** a fresh strong-LLM session with no repo, ≤15 minutes, writes the prompts; stills N=4, clips N=2.
- **P:** the product (§4).

B0 and B1 are generated once per vendor model version and reused.

**Judges and protocol:**
- The founder plus at least 3 paid outside buyers of marketing (about US$40).
- Blind pairwise, at phone size, with sound, sides randomised, mapping sealed.
- Per pair: which would you rather pay for (5-point scale); would-pay per item (yes / yes after one small fix / no); a one-tap reason from 8.
- 10% of pairs are silent swapped repeats, to measure the founder's own consistency: the ceiling for any automatic judge.

**Pre-registered ship rules.** A class ships the pipeline only if all of these hold:
1. **P beats B1:** P is preferred on ≥2/3 of that class's exam briefs, and on ≥17 of 24 across all classes (sign test p ≈ 0.03). Outsiders' majority agrees on ≥2/3.
2. **P beats B0 by a lot ("much, much better"):** it wins ≥80% of pairs, and its would-pay rate is at least 2× B0's.
3. **Would-pay ≥60%,** from both the founder and the outsiders' majority.
4. **CpAO ≤1.5× B1** (or within the class cap), and **TpAO within the class cap.** Starting caps: S1 ≤US$0.60 / 10 min; S2 ≤US$0.30; M1 ≤US$2 / 15 min; M2 ≤US$8 / 45 min; F1 ≤US$15 / 45 min.

**Otherwise:**
- **If P does not beat B1:** that class ships **B1 + finishing** (brand shelf, code text, formats, checks, choice) with the extra stages removed. That is still a product.
- **If nothing reaches would-pay on ≥50% of a class:** refuse or rescope that class.

**Kill criteria** (from P6, adopted):
- **K1:** the non-film classes fail twice (the exam, then fresh briefs). Stop building pipeline for them.
- **K2:** films win ≤3 of 6. No automated films; re-test when a new video model ships, starting with B1.
- **K3:** B0 reaches would-pay on ≥50% of a class. That class is a commodity; don't build for it.
- **K4:** outsiders disagree with the founder on >40% of briefs. Freeze design until ≥10 outside judges have rated.
- **K5 (day 45):** no paid order ≥US$50, and no 3 written "I would pay" from non-friends. Stop product work.

**Change control (the cure for "every fix breaks something"):**
- Versions are hashed and frozen while any job runs.
- One change, or one pre-declared bundle, per candidate, with a hypothesis naming the brief or class it targets.
- **Gate 1:** unit tests, plus checks replayed on stored media (US$0).
- **Gate 2:** smoke-6, one brief per class (about US$15).
- **Gate 3:** the full exam, **weekly** (about US$110, 60–90 founder minutes).
- **Auto-revert** if the new version wins <40% of pairs against the previous one.
- **A rejected production output becomes a bug ticket or a new brief the same day, and never a design change.**
- There is a 24-hour cooling-off before any design ruling after a rejection.

**Judges earn authority later, by tier** (P4):
- **Screen** (rank inside a job): ≥70% agreement with the founder on ≥80 held-out pairs.
- **Gate** (one yes/no check forces a retake): founder agreement ≥90% on ≥30 defects.
- **Proxy** (stands in for the founder on regression runs): within 5 points of his own consistency, on ≥150 pairs.

Until then, a human picks.

**The Canon verdict (CANON-ABL-1)**, run in week 3:
- **Arms:** P with the critique card, P without it, and P with 25 random claims (a volume control).
- **Test:** 30 still briefs × 2 seeds, judged pairwise on finished media.
- **Rule:** keep it only if it wins ≥37/60 and beats the random-claims arm. Films follow only if stills show a win rate ≥0.55.

This gives the founder the data for the verdict he reserved on 1 Sep.

## 6. Operating model

- **One product, one truth.**
  - `main` equals production.
  - Import the live studio (`product/` + `deploy/` at the live commit) as the product.
  - Capture the Mac-only material on day 1: kitchen v12/v12b, `studio-jobs/`, live data, the Mokobara v3 folder, the atlas.
  - Close the stacked PRs #108–#112 as superseded, with archive tags.
- **Consider a fresh repo** (`aight-studio`) with `media-intelligence` archived read-only. The current clone is 4.18 GiB (including 2.1 GB of Lab media), with 146 branches and 18 open PRs, on an 8 GB Mac. The target is a clone under 150 MB, ≤10 branches and 0–2 open PRs. Registry rows, the cases, the atlas and the 76 judged items move as **data**; the Canon moves as a frozen folder.
- **Agents' context** (from the research):
  - an `AGENTS.md` of ≤80–100 lines: the golden benchmark verbatim, the loop (bench → promote → deploy), ~10 non-negotiables, 4 commands, and the session protocol;
  - `CLAUDE.md` = `@AGENTS.md`;
  - a **generated** `STATE.md` (live version, scoreboard, spend against cap, open tasks);
  - `DECISIONS.md` capped at 30 active rules, each citing a bench run or incident;
  - a SessionStart hook prints STATE and DECISIONS (under 6k characters);
  - PreToolUse hooks block a paid call without a cap file, a deploy without PROMOTE, writes to `bench/briefs`, `bench/verdicts` and the frozen knowledge, and pushes to `main`;
  - handoff by `tasks/NNN.md`, not chat;
  - the explain-back test: a fresh Claude Code session and a fresh Codex session must explain the product, what is live, the next task and the spend limit, and the founder must understand their answers.

  This supersedes `proposed-AGENTS.md`, which pointed at the old apparatus.
- **At most two writing sessions** (builder and operator), ≤3 read-only subagents, ≤2 worktrees, no stacked PRs, and PRs open ≤48 hours. Heavy runs happen on the Azure VM or in cloud sessions, not on the 8 GB Mac.
- **Weekly cadence:**
  - **Monday:** the founder picks ≤3 hypotheses from a one-page menu.
  - **Tuesday–Thursday:** build behind flags.
  - **Friday:** the exam run, one blind judging sitting of ≤90 minutes, and a **printable one-page Friday sheet** (scoreboard, what changed, ≤3 yes/no decisions with recommendations).
- **Two kinds of decision only:** a *verdict* (taste on one output, stored as data) and a *rule* (a DECISIONS.md line with evidence and a review date). Founder overrides are allowed, logged as `override`, and reviewed on Friday.

## 7. The first 14 days

Every paid step needs a founder-stated cap first. The figures below are proposals.

| Day | Step | Done when | Cap US$ |
|---|---|---|---|
| 1 | **Freeze and sign.** Stop kitchen deploys and kitchen film orders. Capture Mac-only material. The founder signs a one-page ruling: the golden test with arms B0/B1/P, the ship and kill rules (§5), change control, the 14-day cap, and **the pass definition** (§8, decision 1) | Signed; nothing is being built on the old kitchen | 0 |
| 1–3 | **Build the exam:** 30 briefs, anchors and must-haves; the blind pair viewer (static HTML); the scoreboard script; recruit 3 outside judges and book days 7 and 11 | The founder approves the brief list (30 min); the viewer works on 10 historical pairs | 0 (+~40 judge fees) |
| 2–3 | **Relabel history (US$0):** 60 pairs from the 14 judged films and 62 images, including swapped repeats; qualify the measurement checks (motion, VO fit, OCR, loudness) on stored media | The founder's test–retest estimate; a precision/recall table per check | 0 |
| 3–5 | **Baselines:** B0 and B1 on all 24 exam briefs, via API scripts on the VM | Outputs sealed with cost and time | 100 |
| 3–8 | **Build P v0 (Author + Finish + Choose)** on the P1 job store, compositor/Typeset, ledger and chat; the author call, 3-idea key frames, lint, whole-scene generation, hard checks, format recomposition, "change only X". No kitchen code; about 1,500 new lines | The 6 tuning briefs run end to end with no human touch; reasoning ≤10–20% of job cost | 10 |
| 7 | **Judging session 1** (founder ~70 min; outsiders): B1 vs B0 on 24; the live kitchen vs B1 on the still and animate briefs only | Signed. **If B1 beats the kitchen on ≥12/16 non-ties, the kitchen leaves the live path** | 20 |
| 9–10 | **Run P** on the 24 exam briefs; keep the raw and finished cuts | 24 sealed jobs with CpAO and TpAO | 100 |
| 11 | **Judging session 2:** P vs B1 and P vs B0 | Verdicts recorded | 0 |
| 12 | **Scorecard** against the §5 rules, per class: ship P / ship B1 + finish / refuse | A one-page Friday sheet | 0 |
| 13 | **Switch the live studio** to the winning path per class; the kitchen is off the live path; the golden briefs are dry-run through the studio | Live equals the scoreboard | 0 |
| 14 | **Real buyers:** offer passed classes to 5–10 prospects (free S1 packs from their own photos plus a paid offer) and to Rama + 2 users who own their budgets | Each has paid, declined with a reason, or not replied within 72 h | 25 |

**Totals:** model spend cap about US$255 (expected about US$200), plus about US$40 in judge fees. Founder time is about 5 hours.
**Week 3:** CANON-ABL-1 (about US$20); a voice-casting test (3 real scripts × 4 routes, by ear, about US$5); the brand-shelf second-job test.

## 8. Decisions only the founder can make

1. **The pass definition.** Does "an equal or better idea, a better-finished deliverable, chosen from candidates, that outside buyers would pay for" count as beating the direct prompt? If only raw creative superiority judged by one person counts, the red-team review argues no plan can pass (the same frontier LLM is available directly). This must be settled first.
2. **The 14-day spend cap** (proposed ≤US$255 model + ~US$40 judges), and per-step caps.
3. **Outside judges:** agree to pay 3 buyers of marketing to judge blind, and to K4 (freeze design if they disagree with you on >40% of briefs).
4. **Freeze:** no kitchen changes and no design rulings outside the Friday bench for 14 days. Overrides are logged.
5. **Repo:** consolidate into a fresh repo with the old one archived, or consolidate in place.
6. **Who picks in production:** the customer picks from candidates until an automatic judge earns the "screen" tier.

## 9. Where the reviewers disagreed, and how this plan resolves it

| Question | Positions | Resolution |
|---|---|---|
| Who writes the model prompt? | Research: code adapters. P2/P3/P6: the author LLM writes, code only checks | **The author writes, using per-model style guides; code lints and returns once; code never edits** |
| Who selects? | Research: preference model + VLM. P1/P2/P6: the customer picks. P4: judges earn tiers | **Human pick now; judges earn authority by tier** |
| Stills or films first? | Research: stills. All personas: films in week 1 | **Both in week 1**; films have their own stop rules |
| How many briefs? | 12 / 24 / 30 / 40 | **30 (6 tuning + 24 exam)**; rotate monthly; a vault later |
| Three ideas as key frames? | P3 yes; others silent | **Adopted for films and hero stills.** It is the cheapest taste decision, and the idea is where B1 can't give a choice |
| Canon? | Research: compile into checks, recipes, cards. Personas: freeze | **Freeze;** one critique-card ablation in week 3 |
| Router / bandit? | Research: yes. Personas: needs volume | **Deferred** until ≥30 judged jobs per option; fixed menu until then |
| New repo? | P5 yes; others silent | **Founder decision** (§8.5) |

## 10. The bet, and the risk

**The bet.** Stop trying to make the pipeline more intelligent than the model. Use the same strong author a direct user would use, give the customer a real choice of ideas and takes, and finish deterministically: real product pixels, exact Indian-language copy, every format, timed voice, fact checks, cheap revisions and brand memory across jobs. Then let a fixed exam, not the latest output, decide every change. Where the pipeline cannot beat B1, ship B1 plus finishing. Where nothing passes, refuse the class honestly.

**The risk.** It is behavioural, not technical: a redesign after the next single bad output. Over 80 days that has been the dominant pattern (30 rulings in 36 hours). Hooks can block a deploy but not a habit. The signed freeze and the Friday-only rule are the whole defence.

---

**Files in this folder**
- `MASTER-PLAN.md`: this document.
- `personas/P1`–`P6`: the six independent reviews, each with its own diagnosis, keep/kill list, solution, 14-day plan and critique of the research.
- `CONTEXT-SOLUTION.md` + `01`–`05`: the external research on context, memory and prompting (amended in §3 above).
- `proposed-AGENTS.md`: superseded by §6.
