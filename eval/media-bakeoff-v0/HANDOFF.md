# HANDOFF: run the media bake-off v0, phase 1, overnight on the laptop (where the API keys are)

**Written 2026-09-25** by a cloud Claude Code session with no media-API access. **For** a Claude Code session on the
founder's laptop that has the fal / Google / Azure keys. The founder is asleep during the run. Judging happens when he
wakes up.

**Start:**
1. `git fetch origin claude/magical-volta-q45jee && git checkout claude/magical-volta-q45jee`
2. Read this file, `BRIEFS.yaml` and `PROMPTS.md`.

**Background, if needed:**
- `docs/research/context-engineering-2026-09/MASTER-PLAN.md` (§4 the pipeline, §5 the exam);
- the reviews in `docs/research/context-engineering-2026-09/personas/`.

## Phase 1 (tonight): three arms, no Canon

- **B0, direct:** the customer's words sent straight to the media model.
- **B1, smart writer:** one fresh writer session writes the prompts. No pipeline.
- **P, the pipeline:** Author + Finish + Choose, as in `PROMPTS.md`, **without** the P+Canon section.

**P+Canon (the Canon test) is phase 2, later.** Do not run it tonight.

The questions tonight's run answers:
1. Does P beat B0 by a lot?
2. Does P beat B1?
3. Does a smart writer (B1) alone beat raw direct (B0)?

## Pre-authorised by the founder in the kick-off message (no need to wake him)

- **Spend cap:** as stated in the kick-off message (proposed US$55). Release it in the per-step caps below. Stop the whole run the moment a step would exceed its cap, and write why in `RUN-LOG.md`.
- **Writer model:** as stated in the kick-off message. Use the same model for B1 and for P's writer step. Use GPT-5.6 Luna (or Claude Haiku) for P's understand step.
- **Briefs:**
  - Fill each `verbatim: TODO` in `BRIEFS.yaml` from the named source: the studio DB under `studio-jobs/`, the job branches, or the prospect and CANON-011 files.
  - If a source can't be found, swap in the closest real brief of the same class and note it.
  - Write the must-haves, deal-breakers and price anchors for any brief missing them **before** generating anything.
  - Hash the file into `BRIEFS.sha256`. The founder reviews this in the morning, and a brief he rejects is dropped from scoring.

## Rules

- **Freeze.** No code, prompt or model change once exam generation starts. Log problems in `RUN-LOG.md`; do not fix them mid-run. Practice briefs (T1–T4) are the only tuning, and tuning ends before step 3.
- **Ledger.** Reserve before every call and record every attempt, failures included. No hidden retries.
- **Blind.** Arms are never named in anything the founder sees before he exports his verdicts. Do not open `mapping.json`.
- **No verdicts by Claude.** Do not judge, accept or rank outputs as the customer. The founder judges in the morning. P's own internal take pick (from its contact sheet) is part of the pipeline and is allowed.
- **Blocking is by measurement only.** Only the code checks in `PROMPTS.md` step 5 may block or trigger a retake. No model judge decides anything.
- **Reuse, don't rebuild.** Use the existing P1/studio providers, compositor, Typeset, ledger and job store. Use **no kitchen stations** (waiter, chef, gatekeeper, tasters) in any arm.

## Steps

| # | Step | Done when | Cap US$ |
|---|---|---|---|
| 0 | Fill and hash `BRIEFS.yaml` (above) | `BRIEFS.sha256` committed; the swaps are listed in `RUN-LOG.md` | 0 |
| 1 | Wire the runner for B0, B1 and P exactly as in `PROMPTS.md` | Dry run with simulated providers passes on T1–T4 | 0 |
| 2 | Practice: T1–T4 through P, live (tuning allowed here only) | End to end works; the notes are in `RUN-LOG.md` | 6 |
| 3 | Exam, stills-type (E01–E07): B0, B1, P | 21 outputs sealed with cost and time | 9 |
| 4 | Exam, films (E08–E12): B0, P, and B1 for E08, E11 and E12 (E09 and E10 reuse the existing direct-Veo films as B1) | Outputs sealed | 40 |
| 5 | `outputs.json` → `python3 make_pairs.py <run_dir>` (phase 1 is the default) | `pairs.json` is ready and `viewer.html` loads it | 0 |
| 6 | Morning handover: a one-page `MORNING.md` covering what ran, spend, failures, brief swaps, and how to judge | Committed and pushed | 0 |

The founder then judges in `viewer.html`: 3 pairs × 12 briefs + ~4 repeats, about 35 minutes. He exports `verdicts.json`, and the session runs `python3 score.py <run_dir>` → `SCORECARD.md`.

## Decision rules (fixed before any output exists)

- **P vs B0:** P wins ≥80% of non-tie pairs **and** gets ≥2× B0's "would pay" rate. This is the golden benchmark's "much better than a direct prompt".
- **P vs B1, per class:** P wins ≥2/3 → ship P for that class. Otherwise ship "B1 + finishing" for that class.
- **B1 vs B0:** report only. It tells us how much a good writer alone adds.
- **Cost and time:** record CpAO and TpAO per arm. P's cost per round should be ≤1.5× B1's.
- **Honesty:** report ties, the agreement rate on the swapped repeats, and every failed call.

## Commit

- **Where:** everything goes to `eval/media-bakeoff-v0/run-<date>/` on this branch. Media is stored outside git (the laptop or a bucket), with a hash manifest in git.
- **Push when done.** Open no new PRs; the existing draft PR #113 covers this branch.
