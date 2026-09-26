# Persona 5: The Operator — an operating model and a repo plan

*One of six persona reviews run on 2026-09-25 over `MEDIA-HISTORY.md` ([00]–[08]) and `../CONTEXT-SOLUTION.md`. Model
output, preserved in substance. Synthesis: `../MASTER-PLAN.md`.*

## 1. Diagnosis: five root causes

**RC1. There is no single thing called "the product", and no single place where the truth lives.** Three production systems exist side by side:

- `runtime/` on `main`: Alpha-1, with 403–467 tests. It "has never called a provider".
- The `/media-agency` skill path: it made every asset the founder accepted.
- `product/`: P1, then the kitchen. It is live at studio.getaight.ai but exists only on a five-level stack of unmerged branches (PRs #108–#112). `main` has no `product/` folder [08 §3.9].

The live server runs `11bfc5f`, a version the founder had already moved past. v12 and v12b exist only on the Mac, uncommitted [05 §23]. Other key material is also off `main`:

- The failure atlas, the best diagnostic the project owns, is only on the unmerged P1 branch.
- The overnight films, the databases, the director reviews and the media research sit in `studio-jobs/`, outside git.
- The Mokobara v3 job folder was never committed [04 §4.5][05 §20].

Rulings live in five places: 119 decision files, 31 machine-local memory notes, "ruling lines" inside card YAML, PR bodies and chat. `PROJECT-MEMORY.md` (38 KB) and `CONTROL-STATE.md` (30 KB) are the files every session is told to read first. Both were last refreshed on 15 Sep, before every event that matters. Six parallel sessions worked from that and contradicted each other.

**RC2. Heavy process with no enforcement behind it.**

- By day 5 there were 612,000 words and 483 commits, and zero end-to-end outcomes [02 §10.2]. By 16 Sep: 1.11 M words and 120 decision files.
- Today's checkout has about 2.0 M words of Markdown.
- There are 146 remote branches and 18 open PRs, 13 of them dead.
- The git pack is 4.18 GiB. That includes 2.1 GB of Lab media in `eval/experiments/EVAL-040` (335 mp4 files), on an 8 GB Mac that fell to 120 MB free.

None of this stopped the failures that mattered:

- 27 of 39 repeating failures had no machine behind their fix.
- The P1 builder overrode its own reviewer and shipped five clips its inspector had rejected.
- Two sessions both took attempt id `att-020`.
- A duplicate session wrote a phantom US$0.50 into the spend ledger.

Words were used where hooks and tests were needed.

**RC3. Building before proving, and changing the thing while it was being tested.** "make me a workflow that is supposed to work. only then it will make sense to automate" (22 Sep, 15:23 UTC). A cloud session built P1 v1 four hours later. The same pattern continued:

- P1 v2 was specified and built the same afternoon as the P1 handover.
- The P1 film job was restarted four times with new code while it ran.
- The kitchen took "nine separate fixes mid-order".
- The chef card went from v1 to v13 in 26 hours; there were 30 rulings in 36 hours.

No version was ever evaluated. The proven assets were not wired in either: the Lab produced 575 Registry rows, while the kitchen's equipment sheet had about 15.

**RC4. Decisions were reactions to one output, with no gate between "rejected" and "redesigned".**

- At least 25 decisions were reversed, most after a single rejected output. The logo rule lasted 14 minutes, Astra 36 minutes, and the ChatGPT points an hour.
- The only experiments whose conclusions held were blind, sealed and multi-arm: the RentOK two-lane test and CQ-001.
- The blind planning rounds judged boards, not films. The Mokobara v3 root-cause analysis says they "optimised for the wrong thing".

**RC5. The founder is the only judge, customer, integrator and relay, and communication with him is breaking down.**

- He said "couldn't understand a thing" or the equivalent seven times.
- He relayed prompts between ChatGPT and Claude, and ran production deploys himself.
- He lost three days of quota to an audit's agent fan-out.

Two rules combined to leave the automated loop with no qualified judge at all: "the founder is never inside a running job", and Claude accepting films while acting as the customer.

**The pattern in one line.** Media Factory shipped fast but had no scoreboard. MI in Aug–Sep measured things but shipped nothing. The kitchen shipped, but nothing measured it. None of the three had a fixed benchmark that every change had to pass.

## 2. Keep / kill

**Keep:**
- Writing to the ledger before every call, per-job caps, and C-6a.
- Blind judging with sealed mappings, and the founder as the only trusted judge.
- One author holding the whole job (Mokobara v2, RentOK V2, Upwork intro).
- The deterministic wins: text set by code (4/4 against 0/4), image first then animate, a free animatic before spend, buying the riskiest shot first, and the voice-overlap check.
- Media Factory's rhythm: plan-sized PRs merged to `main` within hours.
- P1 infrastructure: the SQLite job store with atomic attempt ids, the chat front end, and the deploy script with backup and rollback.
- As data, not reading matter: the Registry (575 rows), the 7 cases, the atlas, and the 76 judged items.

**Kill or archive:**
- The Controller/Governor apparatus as the place where state is held (CONTROL-STATE, PROJECT-MEMORY, DECISION-LOG, 119 decision files, `governance/`, `history/`).
- `runtime/` Alpha-1, which never ran live and has been superseded twice.
- Improving the product by rewriting cards, fixing things mid-order, and overnight build-and-deploy.
- Claude acting as the customer and accepting work. Never again.
- Wide agent fan-out as the default.
- Media stored in git, Canon expansion, and Canon injected into prompts by default.
- The 13 dead PRs, about 135 dead branches, and stacked PRs.

## 3. The solution: the benchmark runs like CI, one repo, one writer

### 3.1 The product floor is "direct+"
Live studio v1 is what beat the kitchen twice: the customer's words sent straight to the best model for that media class (taken from the Registry). On top of that it adds only the deterministic layers that have already won:
- code composition for exact text, logo and end card;
- loudness and voice-timing checks;
- 2–4 candidates for the customer to pick from.

The direct arm stays in production for good. Every "intelligence" stage (intake questions, one-author treatment, short native prompts through adapters, Canon packs, selection models) is an increment that ships only if it beats the current version on the bench. That makes "beat one direct prompt" true by construction.

What each stage sees, when it is added:
- **Intake:** the verbatim words and uploads. It outputs the class, the format and at most 2 questions.
- **Author:** one model in one context. It sees the verbatim words, a product-facts dossier, the Registry menu for that class and at most 15 heuristics.
- **Adapter (code):** only the plan's slots. It writes a native prompt of 80 words or fewer; image-to-video prompts describe motion only.
- **Composer (code):** exact copy, logo and timing.
- **Customer:** the candidates.

Measured on every job: CpAO fully loaded, TpAO, and whether the customer picked the direct candidate or the pipeline's.

### 3.2 The bench (`bench/`)

**Briefs.** 24 frozen briefs that cover the whole product:
- 8 stills or static ads;
- 6 short films (15 s or less);
- 4 "edit my photo" or "animate my image" jobs (the real demand CANON-009 found, never tested);
- 6 holdout briefs that nobody sees during development.

The briefs use customers' verbatim words from the 7 cases, iPhone Duo, Ascend, ramen, Rama, Aight Studio and the CANON-011 marketplace briefs. Each carries one line from the founder, "what would make me pay", written before anything is generated.

**Arms and judging.**
- Arms: DIRECT against CANDIDATE, with the same model and references where possible.
- The founder judges blind: preference, "would I pay? y/n" and a one-line reason for each pair.
- One judging page, one sitting a week of 90 minutes or less.
- Verdicts are stored as data in `bench/verdicts/`. They never become rules.

**Promotion rule, fixed before any run.** On the 18 development briefs, a candidate ships only if all of these hold:
- it wins at least 13 of 18 pairs against the current version (ties count as losses; sign test p ≈ 0.05);
- its would-pay rate is at least the current version's;
- it does not lose more briefs than it wins in any class;
- its CpAO is at most 1.5× the current version's, unless it adds at least 3 more "would pay" answers.

It must then be no worse on the 6 holdout briefs. A change to one class is tested on that class's briefs (at least 6) and needs 5 of 6 wins; that result is directional until the next full run confirms it.

**What a rejected production output may do.** On the same day it becomes exactly one of two things: a bug ticket (a crash, a spend problem, a wrong file) or a new bench brief. It never changes a card or rule directly.

### 3.3 Weekly cadence
- **Monday:** the founder picks at most 3 hypotheses from a one-page menu (change, why, which briefs, cap).
- **Tuesday to Thursday:** one builder implements them behind a version flag. PRs merge daily; nothing touches live.
- **Friday:** the capped bench run. The founder judges in one sitting, the scoreboard regenerates, and each candidate is promoted or reverted. Only then is anything deployed.

He also gets a printable one-page Friday sheet: the scoreboard, what changed, and at most 3 yes/no decisions, each with a recommendation.

### 3.4 How decisions are made so they hold
- **Only two kinds of decision.** A verdict is the founder's taste on one output, stored as data. A rule is a `DECISIONS.md` line with an id, one line, a date, its evidence (a bench run id or incident id) and a review date.
- **At most 30 active rules.** Adding a 31st means retiring one in the same PR.
- **Where rules may come from:** a bench result, a money or safety incident, or a founder product call. Never a single output.
- **24-hour cooling-off:** no design rule within 24 hours of a rejected output, except fixes for bugs and money.
- **Founder overrides are allowed.** They are written as a line tagged `override` and reviewed at the next Friday run.

### 3.5 How Claude Code and Codex sessions are organised
- **One writer.**
  - At most two sessions write at the same time: Builder (code in `studio/`) and Operator (runs the bench; owns the scoreboard, spend and deploy gate).
  - At most 3 read-only subagents, each writing a digest of 2k tokens or less to a file.
  - At most 2 worktrees. No stacked PRs; no PR open longer than 48 hours.
- **Handoff by task file, not chat.**
  - Each piece of work has one `tasks/NNN.md`: goal, hypothesis, done-when, cap, files, progress log.
  - Every session starts the same way: git pull → `AGENTS.md` loads automatically → a SessionStart hook prints `STATE.md` and `DECISIONS.md` (under 6k characters) → open the task file → smoke test.
  - Every session ends by updating the task file and pushing.
- **`STATE.md` is generated, never hand-written.** It shows the live version, the scoreboard, spend against cap, open tasks and pending decisions, and is regenerated by the bench and deploy scripts.
- **Hooks are the rules.** PreToolUse hooks block:
  1. a paid dispatch with no cap file for that run;
  2. a deploy unless the scoreboard says PROMOTE for that version;
  3. writes to `bench/briefs/**`, `bench/verdicts/**` and `knowledge/**`;
  4. direct pushes to `main`.

  One dispatcher with a file lock handles every paid call, so there is one ledger.
- **Memory.** Machine-local memory notes stop being a source of truth. Triage the 31 notes: rules go to `DECISIONS.md`, preferences go to `AGENTS.md`, the rest are deleted. Codex reads the same `AGENTS.md`; skills are mirrored to `.agents/skills`.
- **Explain-back test before any building.** A fresh Claude Code session and a fresh Codex session, given only the repo, must answer: what the product is, what is live, what the next task is, and what they may spend. The founder confirms he understood the answers.

**`AGENTS.md` (80 lines or fewer):**
- the product in 3 lines, including the golden benchmark verbatim;
- the loop: bench → promote → deploy;
- 8 paths;
- 10 non-negotiables;
- 4 commands: run a job, run the bench, build the scoreboard, deploy;
- the session protocol.

### 3.6 Consolidating the repo
Start a new repo (`aight-studio`) with fresh history, and set `media-intelligence` to read-only (archive).

| Item | Action |
|---|---|
| `product/` + `deploy/` at `11bfc5f` (live) | Import as `studio/`, so `main` equals production; close #108–#112 as superseded, pointing to archive tags |
| Kitchen v12/v12b, `studio-jobs/`, `mi-p1-live-data`, the Mokobara v3 folder (local only) | **Capture on day 1** |
| 7 cases + atlas + 76 judged items | `learning/`; the judged items become the bench's calibration set |
| Registry (575 rows) | `data/registry/`, read-only |
| Canon | Only the ten packs and the claims index go into `knowledge/` (frozen); the raw corpus stays in the archive |
| `/media-agency` skill | Keep as the "hand" arm, pointed at the studio dispatcher and ledger; archive the forms and `build_prompts.py` |
| `runtime/`, `coordination/`, `governance/`, `history/`, `resources/`, eval media (2.1 GB) | Archive; move media to a bucket, with a hash manifest in git |
| 13 dead PRs, ~135 branches | Tag each tip as `archive/*`, then close or delete |

**Target:** a clone smaller than 150 MB, 10 or fewer branches, 0–2 open PRs.

## 4. The first 14 days (caps proposed; the founder states the real ones)

| Day | Step | Done when | US$ |
|---|---|---|---|
| 1 | Freeze: stop all building, pin live at `11bfc5f`, pause invites, capture everything that exists only on the Mac | Everything committed or uploaded; the founder has written the 14-day cap | 0 |
| 1–2 | Consolidate into the new repo | Clone under 150 MB; studio tests pass; 0 open PRs in the old repo | 0 |
| 2 | `AGENTS.md`, `DECISIONS.md` (≤30 rules), the generated `STATE.md`, hooks | Explain-back passes for Claude Code and Codex, and the founder understood it | 0 |
| 3–4 | Build the bench: 24 briefs, the judging page, the scoreboard script | The founder approves the brief list; the scoreboard runs on dummy verdicts | 0 |
| 5–6 | Baseline run: DIRECT on all 18 development briefs; current studio on 12 stills/edits and 3 films, with no fixes during the run | About 33 outputs judged in one 90-minute sitting; scoreboard v0 | ~80 (cap 90) |
| 7 | Deploy v1 = direct+ for every class where direct won or tied | Live serves v1; Friday sheet sent | 0 |
| 8–12 | **H-still:** one author + short native prompts + best-of-4. **H-film:** prose treatment → whole 8-second Veo scenes with native sound; code handles only the joins, the timed voice-over and the end card | Both built behind flags | 0 |
| 13 | Bench run on the development set | Each hypothesis marked PROMOTE or REVERT | ~60 (cap 60) |
| 14 | Holdout check of the winner against DIRECT; Friday sheet; pick the next ≤3 hypotheses | Scoreboard v2; `DECISIONS.md` PR citing run ids | ~25 (cap 30) |

- **Total:** about US$165 (caps US$180).
- **Founder time:** about 4.5 hours.

## 5. The bet and the risk
**The bet:** make the bench the only way a change reaches the customer, with the direct arm as the permanent floor, covering every media class each week.

**The risk:** the founder going back to redesigning after a single output: rulings outside the bench, mid-job changes, "approved to bypass". Hooks can block a deploy, but not a habit.

## 6. Where I disagree with CONTEXT-SOLUTION.md
1. **Its 30-day plan is still build-first:** four parallel workstreams. Build the bench first and let each component earn its place. Defer:
   - the bandit router (it needs hundreds of labels; we have about 90);
   - the HPSv3/PickScore ranking models, until calibrated on our labels;
   - Canon migration.
2. **About 100 pairs per knowledge item cannot be run with one judge.** Promote versions or bundles on the 24-brief bench instead.
3. **Its proposed `AGENTS.md` keeps the old apparatus** (CONTROL-STATE, `coordination/decisions/`, `runtime.alpha.cli`). The real source-of-truth problem is branch sprawl and state held outside git.
4. **A Canon-researcher subagent and qmd search are premature.** Canon's value on media is unproven, and retrieval found 0 of the 22 claims used on Mokobara. Freeze it, and test the ten packs once as a bench arm.
5. **It puts too much weight on prompt mechanics.** 43 of 46 defects were not model failures; 5 of 6 Mokobara v3 defects were in the board before any spend; CQ-001 found direction, not prompts, was the bottleneck.
6. **"Stills only at first" repeats the old habit of optimising the easy class.** Both losses to direct Veo were films, so films belong in week 1.

I agree with its central principle (knowledge becomes code, checks or recipes rather than prompt text; the direct arm is permanent). My disagreement is only with the build order.
