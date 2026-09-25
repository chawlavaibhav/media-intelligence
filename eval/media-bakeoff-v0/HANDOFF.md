# HANDOFF: run the media bake-off v0 on the laptop (where the API keys are)

**Written 2026-09-25** by a cloud Claude Code session that has no media-API access. **Who this is for:** a Claude Code
session on the founder's laptop (or the studio server) that has the fal / Google / Azure keys.

**Start with:**
1. `git fetch origin claude/magical-volta-q45jee && git checkout claude/magical-volta-q45jee`
2. Read this file, `BRIEFS.yaml` and `PROMPTS.md`.

**Background (read if needed, not before starting):**
- `docs/research/context-engineering-2026-09/MASTER-PLAN.md` (§4 the pipeline, §5 the exam);
- `canon/shape-v1/` (the reshaped Canon);
- `eval/retrieval-canon-2026-09-25/RESULT.md` and `eval/canon-qa-knowledge-2026-09-25/RESULT.md`.

## What this test answers

On the same 12 exam briefs, judged blind:
1. Does **P** (one writer + finishing + choice) beat **B0** (the customer's words sent straight to the model) by a lot?
2. Does P beat **B1** (a smart writer with no pipeline, the thing that beat the kitchen twice)?
3. Does **P+Canon** (P with Canon shape v1 in the writer's context) beat P? This is the first clean Canon test: the
   pipeline has no gatekeepers, no failure-note tray, no still fallbacks and no code-rewritten prompts.

## Rules (non-negotiable; these are the founder's)

- **Spend cap.** US$75 total model spend for this run, released per step (below). The founder must confirm the cap in
  writing in the session before the first paid call. Reserve before each call; ledger every attempt, failures included.
- **Freeze.** No code, card or prompt change once exam generation starts. A problem becomes a note in `RUN-LOG.md`,
  not a fix. Practice briefs (T1–T4) are the only place to tune, and tuning ends before the exam.
- **One writer model for every arm** (B1, P, P+Canon). The founder picks it at the start: Claude Sonnet 5 / Opus 5.5
  or GPT-5.6 Sol. Luna (or Haiku) handles the understand step.
- **Blind.** The judge never sees arm names. The pipeline never sees `must_haves`, `deal_breakers` or `price_anchor`.
- **No Claude-as-customer verdicts.** Only the founder (and any outside judges) judge.
- **No model judge in the release path.** The code checks in `PROMPTS.md` step 5 are the only blockers.

## Steps

| # | Step | Done when | Cap US$ |
|---|---|---|---|
| 0 | The founder approves `BRIEFS.yaml`: fill every `verbatim: TODO` from the named source, swap any brief, set anchors. Hash the file into `BRIEFS.sha256` | Signed in `RUN-LOG.md` | 0 |
| 1 | Wire the runner, reusing the P1/studio provider, compositor, ledger and job store. There is **no kitchen code in any arm**. Implement the arms exactly as in `PROMPTS.md` | Dry run with simulated providers passes on T1–T4 | 0 |
| 2 | Practice: T1–T4 through P and P+Canon, live | The runs work end to end; the founder glances at them (not judged) | 8 |
| 3 | Exam, **stills-type classes** (E01–E07): B0, B1, P, P+Canon | 28 outputs sealed with cost and time | 12 |
| 4 | Exam, **films** (E08–E12): B0, P, P+Canon, plus B1 for E08, E11 and E12 (E09 and E10 reuse the existing direct-Veo films) | Outputs sealed | 50 |
| 5 | Build `pairs.json` with `make_pairs.py` and judge in `viewer.html` (blind, randomised sides, 10% swapped repeats) | The founder's verdicts are exported as `verdicts.json` | 0 |
| 6 | `score.py` → `SCORECARD.md`, applying the rules below | Scorecard committed; the founder signs the decisions | 0 |

Stop at any step whose cap would be exceeded, and ask the founder.

## Pairs judged (per exam brief)

P vs B0 · P vs B1 · P+Canon vs P · P+Canon vs B1. That is 4 pairs × 12 briefs = 48 pairs, plus about 5 swapped repeats.
At about 20 s per still pair and about 90 s per film pair, that is about 45 minutes.

## Decision rules (fixed now, before any output exists)

- **P vs B0:** P should win at least 80% of non-tie pairs and get at least 2× B0's "would pay" rate. This is the golden benchmark's "much better than a direct prompt".
- **P vs B1:** a class ships P only if P wins at least 2/3 of that class's pairs. Otherwise that class ships "B1 + finishing".
- **P+Canon vs P:** the Canon stays in the writer's context only if P+Canon wins more pairs than it loses **and** at least 7 of the 12. With n = 12 this is directional; a clear win earns a 30-brief confirmation run.
- **Cost and time:** record CpAO and TpAO per arm. P's cost per round should be ≤1.5× B1's.
- **Honest reporting:** report ties, the swapped-repeat agreement rate (the founder's own consistency), and every failed call.

## Commit

- **Where:** everything goes to `eval/media-bakeoff-v0/run-<date>/` on this branch. Media is stored outside git (a bucket or the laptop), with a hash manifest in git.
- **Deliverables:** `SCORECARD.md` and a one-page printable summary for the founder.
