# P1 — independent review entry point

Start here. This page is enough to begin an independent review of Media Intelligence P1 without the previous builder's
conversation or anyone's laptop. It was written on 2026-09-23 as a preservation handover, not as a review: nothing in it is a
verdict on P1, and where it quotes the previous builder's explanations they are labelled as **hypotheses**.

The standard you are reviewing against is the founder's **P1 mission addendum** (supplied to you with this assignment). It
takes precedence over every design document in this repository. The existing architecture is evidence of what was intended; it
is not the definition of success.

---

## A. Exact source version

| | |
|---|---|
| Repository | https://github.com/chawlavaibhav/media-intelligence (public) |
| Branch | `claude/confident-franklin-s1v8ln` |
| Commit | the branch head that contains this file. It is recorded in the evidence repository's `SOURCE-VERSION.md`, and `git log -1 -- coordination/p1/P1-REVIEW-ENTRY.md` prints it. |
| Pull request | https://github.com/chawlavaibhav/media-intelligence/pull/108 — **draft, open, not merged** |
| Code that ran the two live jobs | commits `2693d3b`…`bcfb3fc`. The code **changed during the live jobs**: `f30b636` (10:20 IST) and `15ab0a7` (11:56 IST) landed while the film job (04:31–06:48 UTC = 10:01–12:18 IST) was running, and `bcfb3fc` right after it. No single commit produced either job end to end. |

## B. Evidence access

| | |
|---|---|
| Private evidence repository | https://github.com/chawlavaibhav/mi-p1-evidence (private). Access: ask the founder (GitHub `chawlavaibhav`) to add your GitHub account as a collaborator with read access. No credentials are needed or stored anywhere in it. |
| Revision | recorded in `SOURCE-VERSION.md` at the head of `main`. Every file's hash is in its `MANIFEST.json`. |
| Start with | `README.md` (map, integrity, what was removed and why, known gaps) |
| Manifest | `MANIFEST.json` / `MANIFEST.csv` — path, type, job, SHA-256, size, timestamps, database asset row |
| Accepted posters (as delivered) | `review-exports/DELIVERED-ast_e05db60251c4ab8d.png` (1:1), `review-exports/DELIVERED-ast_8008723f7cc0cdc4.png` (4:5) |
| Rejected film (exactly the file the founder rejected) | `review-exports/mokobara-reel-30s.mp4` = `livebeta/media/job_20260923_7d36a5b6/out/cut2-9x16.mp4`, asset `ast_96ccb4b092b8f40b`, SHA-256 `957f00c7…9313e` |
| Original job records | `JOBS.md` (brief verbatim, spend by route, full attempt ledger, graph, timings, checks, deliveries) |
| Customer verdicts, verbatim | `VERDICTS.md` |
| Sanitized ledger and all tables | `db/mi-sanitized.sqlite3` and `db/export/*.jsonl` (attempts, llm_calls, artifacts, checks, events, timings, nodes, assets, deliveries, waivers) |
| Every generated still/clip/music take | `livebeta/media/<job>/gen/` |
| Integrity check | `python3 tools/verify_evidence.py` (no network, read-only) |

The raw database, the web app's signing key and the test-customer passwords were deliberately left out; the evidence README
explains exactly what was removed. The original folder stays untouched on the founder's Mac.

## C. Product shape

P1 is meant to be an invite-only web product in which a business submits a brief with product photos, logo and exact copy,
and receives a finished **static product ad (P1-IMG)** or a **15–30-s product story film without speech (P1-FILM)**. Code holds
the job state; LLMs are components: strategist (intent + questions) → creative director (concept, storyboard, copy deck,
product anchor, with Canon injected) → pre-spend direction reviewer → customer approves direction, preview and quote →
orchestrated production (stills → clips → music → code-composed text/logo → assembly) → deterministic checks + isolated model
reviewer → presentation gateway → customer preview, targeted changes, accept, download → learning case.

Authoritative definition (do not rely on this summary): `coordination/assessments/P1-PRODUCTIZATION-2026-09-22/P1-PRODUCTIZATION-ASSESSMENT.md`,
§D (supported media classes, customer journey, customer-vs-autonomous decisions, interfaces) and §G (beta-release gate).
Code map: `product/README.md`.

## D. What actually happened (live validation, 2026-09-23)

Both jobs ran locally on the founder's Mac (not deployed) through the web app and worker, with GPT-5.6 (`gpt-5.6-sol`, Azure
getaight) for reasoning, Gemini 3.1 Pro as reviewer/inspector, nano-banana-2 stills, Veo 3.1 Fast i2v clips, Lyria music.
The "customer" was a test account; the founder judged the outputs.

### Image job `job_20260923_6720871c` — launch poster, 1:1 + 4:5 — **ACCEPTED**

- Timeline (UTC): submitted 02:56 → direction approved 03:15 → first cut 04:07 → recomposed 04:23 → released 04:30 →
  accepted and downloaded 04:30. Ledger **USD 2.275137** (23 attempts).
- The founder picked the plate takes and asked for a colour, clearance and logo-size change before accepting (events at 04:07
  and 04:23 are recorded as `operator:vaibhav@getaight.ai`).
- The model reviewer returned **fail** on both reviews. Gateway reports v1 and v2 were `ready: false`. Gateway v3 (04:30,
  `released_by: operator:vaibhav@getaight.ai`) is `ready: true` with no waivers recorded. **How the blocking FAIL was cleared
  at v3 is unverified**; the reviewer should establish it from `product/verify.py` and the `checks` table.
- The job failed twice and was restarted by the builder (03:09 `failed → directing`; 03:22 `failed → paused_operator`, "offer the paid draws to a person").
- Accepted: this proves one acceptable result for this assignment. It does not prove reliability across the image family.

### Film job `job_20260923_7d36a5b6` — 30-s 9:16 Reel, hands-only packing — **REJECTED**

- Timeline (UTC): submitted 04:31 → direction approved 04:48 → first cut 06:35 (**1 h 47 min after approval**) → second cut
  06:41 → founder rejected 06:48. Ledger **USD 13.591638** (81 attempts: 42 provider, 39 reasoning; 7 failed).
- Founder's verdict, verbatim (also in the evidence repo's `VERDICTS.md`):
  > "the video is fucked up. two random hands, too many AI slops. video is robotic." / "the yellow colour is also changing in
  > the bag. it was blue and then turned yellow."
- **The model reviewer did not pass this film.** Both final reviews returned `fail` (6 defects, 5 blocker/major on cut 2),
  including product fidelity, product across shots, character continuity, M03/M04/M06/M12/M13. Both gateway reports were
  `ready: false`. The job was never presented through the product (`presented_at` is empty); the founder saw the film as an
  exported file (`review-exports/`). An earlier handover line saying the reviewer's PASS "counts as a person confirms" describes
  the design, not what happened on this film.
- Veo produced 16 clip takes; the per-clip inspector recorded a rejection for 15 of them (`take_rejected`, 05:02–06:37; the
  16th, `clip_b1__att-0080`, has no inspection result). **All five Veo clips in the rejected film (b1, b2, b5, b7, b8) are takes
  the inspector had rejected.** They were selected by `operator:claude (builder, P1 validation; founder judges the film)`; under
  commit `15ab0a7` an unqualified inspector cannot remove a take on its own.
- The pre-spend direction reviewer returned `revise` with a major issue (a 180-degree laptop compartment "fully unzipped" on an
  upright bag for six beats). It was overridden by `operator:claude (builder, P1 validation)` at 04:44 with the recorded reason
  that the only blocker was the wording "reverse-coated".
- Stills: the inspector rejected 12 of the 13 beat stills generated. The builder selected six of the rejected ones, including `still_b7`
  (inspector: brand misspelt "mokebara" on the plaque) and `still_b6` (inspector: wrong handle, legible plaque text).
- Beats 3, 4, 6 became code push-ins on stills: b3 and b4 were refused twice by Veo's safety filter ("celebrity likeness";
  "an issue with the audio"); b6 morphed the bag in both takes.
- An automatic internal repair was queued and then reverted by the builder ("unqualified reviewer; person judges"). The test
  customer's budget was raised to USD 14 at 06:40.
- The builder changed code and restarted the job repeatedly during the run (`failed → producing` at 05:01, 06:27, 06:31, 06:35).
- No learning case was written for the film (it was never closed); only the image job has `livebeta/cases/`.

### Not verified at all

Deployment (nothing is deployed; no VM exists), email notifications, a customer operating the product without a developer,
a second image job, any film acceptance, reviewer qualification (1/6 on MOKO7 v1, see `product/qualification/RESULT-2026-09-23.md`),
the 10–15-min first-cut target, and vendor bills (the ledger has not been reconciled against Google/Azure invoices).

## E. How to reproduce

Every command below is **no-spend** unless marked. Paid calls happen only when `MI_PROVIDER_MODE=live` and/or
`MI_REASONING_MODE=live` are set, or when a command is given `--live`; the defaults are `simulated`.

```bash
# 1. Source (public)
git clone https://github.com/chawlavaibhav/media-intelligence && cd media-intelligence
git checkout claude/confident-franklin-s1v8ln
python3 -m venv .venv && .venv/bin/pip install -r deploy/requirements.txt
#    also needs ffmpeg and Pillow built with raqm (macOS: brew install ffmpeg libraqm; Debian: see deploy/install.sh)

# 2. No-spend test suite (real ffmpeg, simulated providers; ~4-6 min)
PYTHONPATH=. .venv/bin/python -m unittest discover -s product/tests -t .

# 3. Media-engine + dry end-to-end smoke (no-spend)
PYTHONPATH=. .venv/bin/python -m product.smoke

# 4. Local app in simulated mode (no-spend): two terminals
PYTHONPATH=. MI_DATA_DIR=/tmp/mi-dry .venv/bin/python -m product.web.app --port 8766
PYTHONPATH=. MI_DATA_DIR=/tmp/mi-dry .venv/bin/python -m product.worker
#    black-box journey against it (no-spend): PYTHONPATH=. .venv/bin/python -m product.journey --dry --help

# 5. Evidence (private; needs collaborator access)
git clone https://github.com/chawlavaibhav/mi-p1-evidence && cd mi-p1-evidence
python3 tools/verify_evidence.py
```

**Recorded result on 2026-09-23 (founder's Mac, Python 3.14.7, ffmpeg 8.1.2, clean environment with no provider keys):**
`unittest` — `Ran 54 tests in 245.409s … OK`; `product.smoke` — PASS media engine on this host, PASS dry image + film jobs
through the product, PASS backup and restore. `runtime/tests` (the older runtime package) was not run for this handover; the PR
notes it already had failures on `main` before this branch.

To inspect the live jobs **in the product's own operator view** without any spend: point the simulated app at a *copy* of the
evidence (never the clone itself): `mkdir /tmp/mi-replay && cp -R mi-p1-evidence/livebeta/media mi-p1-evidence/livebeta/cases /tmp/mi-replay/ && cp mi-p1-evidence/db/mi-sanitized.sqlite3 /tmp/mi-replay/mi.sqlite3`,
then start only the web app (step 4, `MI_DATA_DIR=/tmp/mi-replay`, **do not start the worker**). The sanitized database has no
passwords, so create an operator account with `PYTHONPATH=. MI_DATA_DIR=/tmp/mi-replay .venv/bin/python -m product.admin init-operator --help`; the two jobs then open in
the operator view. Starting a worker against this copy could resume a paused job; in simulated mode that costs nothing, but it
would change the copy.

**Paid (need explicit founder authorisation; do not run):** `run-live.sh` in the evidence `scripts/` folder, any command with
`MI_PROVIDER_MODE=live` or `MI_REASONING_MODE=live`, `python -m product.qualification.qualify_reviewer --live`.

## F. Known problems (observed, with evidence)

| Problem | Evidence |
|---|---|
| Film rejected: hands in two different wardrobes (white cuff vs grey jacket), robotic/jerky motion, morphing zips and flaps, bag construction changing between shots, yellow lining visible where the plan has the bag closed | `review-exports/mokobara-reel-30s.mp4`, `review-exports/mokobara-reel-frames.png`, reviews in `artifacts` (kind `review`) |
| The inspector and final reviewer flagged most of these defects, but the takes still went into the film and the file still reached the founder | `events` (`take_rejected`, `take_selected_by_person`), `checks`, gateway v1/v2 `ready: false` |
| Pre-spend direction review said `revise`; overridden by the builder | artifacts `direction_review` v1, `direction_override` v1 |
| Veo safety-filter refusals on b3/b4 (4 refusals) and request-shape errors on b1 (2) | `attempts` seq 42, 43, 49, 54, 56, 70, 74 |
| Three of eight beats shipped as code push-ins on stills | `gen/clip_b3__still-motion.mp4`, `clip_b4__…`, `clip_b6__…`; events `still_motion_fallback` |
| Creative latency: director calls of 225 s and 246 s; approval → first cut 1 h 47 min | `attempts` seq 2 and 4; `JOBS.md` timings |
| Model reviewer not qualified (1/6) | `product/qualification/RESULT-2026-09-23.md` |
| Output files overwritten in place: the image job's first-cut posters were lost when the recomposition wrote to the same path | evidence `README.md` "Known gaps"; assets `ast_9c4715ffcd8aa1c3`, `ast_15a65b55e1b4818b` |
| No learning case for the rejected film | evidence `livebeta/cases/` holds only the image job |
| Not deployed; no email; typography is a system sans; no per-customer product dossier | `HANDOVER-2026-09-23.md` §5 |

**Hypotheses from the previous builder (not verified)** — `HANDOVER-2026-09-23.md` §4: (1) the plan asked Veo for fine hand
choreography it cannot do; (2) beat stills were generated independently, so the world and product drift; (3) static fallbacks
add to the robotic feel; (4) director latency is the main obstacle to 10–15 min. Test them against the evidence; do not adopt them.

## G. Review scope

Evaluate independently, against the founder's P1 mission addendum: the implementation, the creative intelligence (does the
direction serve the assignment?), production intelligence (does it choose methods the models can execute?), actual media
quality (watch the film at phone size), reliability (which protections operated, which were bypassed, and by whom),
operational learning (does the atlas prevent repeats in practice?), customer experience (could a customer do this without a
developer?), economics (time, cost, failed attempts, cost per accepted outcome), and readiness for a beta customer. You are not
asked to agree with the previous builder, and the fact that code or a control exists is not evidence that it worked.

Where things are: failure atlas (verbatim) `production-learning/atlas/2026-09-22/` (`FAILURE-ANALYSIS.md`,
`FAILURE-ATLAS-RAW.yaml`, `FAILURE-ATLAS-CLASSIFIED.yaml`); P1 control register and reconciliation
`product/data/FAILURE-CONTROLS-v1.yaml` (key `atlas_reconciliation`); historical regression tests `product/tests/test_verify.py`
and `product/tests/test_e2e.py`; reviewer qualification `product/qualification/`; engineering record
`coordination/p1/P1-BUILD-STATUS.md`; spend authority `coordination/p1/SPEND-RECORD-P1-VALIDATION-2026-09-23.md`.

## H. Review boundaries

Read-only by default. Without the founder's explicit authorisation: no paid generation or reasoning calls, no cloud-resource
creation, no merge of PR #108, no pushes to `main`, and no change to anything in the evidence repository. Cloud: only the
getaight Azure subscription `b832f4a1` resource group `aight-mi-p1` belongs to P1; never touch resource group `project-1` or
the Wherehouse subscription. Spend so far: USD 15.97 of the USD 20 validation authority; the remaining USD 4.03 is not a
standing authorisation for you.
