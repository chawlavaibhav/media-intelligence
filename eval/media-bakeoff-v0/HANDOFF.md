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

## PRE-FLIGHT: before any spend, confirm three things, then wait for the founder's "GO"

1. **Keys.** Run `python3 eval/media-bakeoff-v0/preflight.py`. It prints key **names** and yes/no only, plus the tools
   and git access. If any required key shows NO, stop: the session was not started with `source ~/.mi-keys && claude`.
   Tell the founder to restart it that way. Do not read `~/.mi-keys` yourself.
2. **Understanding.** Write back to the founder, in **≤10 plain lines**:
   - the three arms;
   - what tonight answers;
   - the media model per class;
   - the spend cap and per-step caps;
   - the freeze rule;
   - that you won't judge;
   - what `MORNING.md` will contain.
3. **Uninterrupted.** Do a zero-cost dry run of the runner on T1–T4 with simulated providers. Then do **one** tiny live
   smoke call per provider (≤US$0.50 total, counted in step 2's cap): one fal image, one Gemini image, a Veo *status*
   call or the cheapest clip, and one writer call. This proves no step will stop at a permission prompt or a network
   block overnight.
   - Report any command that needed approval.
   - The founder can pre-approve those commands in `.claude/settings.local.json` (`permissions.allow`), or you
     restructure them so the run needs no further approvals.

Then **stop and wait for the founder to reply "GO"**. After GO, run to the end without asking anything. Anything
unexpected goes into `RUN-LOG.md`, and the run carries on or stops at a cap. It never waits for input.

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

## API keys: use the MI keys on this laptop (authorised by the founder)

The keys live outside the repo, as the Capability Lab harness used them (EVAL-039C):

| File | Holds (names only) | How to load |
|---|---|---|
| `~/.mi-keys` | `FAL_KEY`, `GOOGLE_API_KEY`, `ANTHROPIC_API_KEY`, `SARVAM_API_KEY`, `GOOGLE_CLOUD_VISION_API_KEY` (every line starts with `export`) | `source ~/.mi-keys` in the same shell command that runs the runner |
| `~/.aight-litellm-keys/vertex-sa.json` | the Vertex service account (Veo on Vertex, Lyria) | pass the **path** to the adapter; never read the file into a prompt or a log |
| `/etc/mi/mi.env` (studio server only) | the studio's own keys, including the Azure OpenAI ones for Luna/Sol | only if running on the server: `set -a; . /etc/mi/mi.env; set +a` |

Rules for keys:
- **Read by name only.** Never print, echo, `cat`, log or commit a value, and never paste one into chat. Check presence with `grep -c '^export FAL_KEY=' ~/.mi-keys`, not by printing.
- **Load keys inside the command that runs the job:** `bash -c 'source ~/.mi-keys && python3 run.py …'`. Environment variables do not carry between tool calls.
- **If the Azure (Luna) key is not on this laptop,** run P's understand step on Claude Haiku 4.5 with `ANTHROPIC_API_KEY`, and log the substitution in `RUN-LOG.md`.
- **If Claude Code blocks reading `~/.mi-keys`** (a permission prompt the founder can't answer while asleep), the founder instead starts the session from a terminal that already ran `source ~/.mi-keys` (`source ~/.mi-keys && claude`). The keys are then inherited by every command.

## If something outside the repo can't be found

- **`studio-jobs/` or the job DB can't be found** (they sit outside git on the Mac): do not search the home folder.
  Use the briefs that are already verbatim (E09–E12), fill the rest from in-repo sources (`production-learning/cases/`,
  `canon/research/marketplace-demand-v1/`, the job branches), and list every swap in `RUN-LOG.md`.
- **The existing direct-Veo films for E09 and E10 can't be found:** generate B1 for them as well (about US$10 more,
  still within the film cap), and log it.

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
