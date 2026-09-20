# 00 — Bootstrap record (USD 0) — lane B

Written by the lane-B producer session, 2026-09-20. Everything here is OBSERVED from the worktree unless marked otherwise.

## Communication check

**Communication check:** I will explain technical ideas in plain English, including what they mean, why they matter, and their practical consequence; use minimum sufficient wording without sacrificing understandability; separate evidence from inference; and never invent facts. I have read `shared/COMMUNICATION-STANDARD.md`.

## HEAD and tree

- Worktree branch: `work/agency-job-rentok-game-lane-b-001`
- HEAD at bootstrap: `60813e3` (two scaffold commits on top of `origin/main @ 4d919c9` = `4d919c9df6c9725a2f14c411771565bb09089876`, the production base).
- `git status --short` at bootstrap: empty (clean). Protected trees (`canon`, `eval/registry`, `eval/capability-map`, `coordination`): no uncommitted change.
- Skill file sha (git blob of `.claude/skills/media-agency/SKILL.md`): `7e324b0f75658498b62802332504519b9d542996`.
- Local tools present: `/usr/bin/python3` (yaml, Pillow 11.3.0, numpy 2.0.2), ffmpeg 8.1.2, ffprobe, hb-view.

## Read (per BOOTSTRAP.md §2 and the task brief)

PROJECT-MEMORY.md §1, §2, §5, §7 · CONTROL-STATE.md §2, §3, §6, §8 · media-agency SKILL.md, BOOTSTRAP.md, PRODUCTION-WORKFLOW.md, QA-CHECKLIST.md, JOB-TEMPLATE.yaml · CANON-SHAPE-v1.md §4–§5 · pack-triggers-v0.yaml · ALPHA-1.md ("What exists" / "Does not exist") · production-learning/README.md, cases UPWORK-INTRO-001 and UPWORK-PORTFOLIO-002 (README, SYSTEM-DEFECTS, ROUTE-OBSERVATIONS, PROMOTION-QUEUE) · all four `input/*` files · `source/rentok-snapshot/README.md` + the four `.txt` extracts · `tools/reference-kit/*`.

Upwork profile reads skipped (class `customer_work`, per the task brief).

## Pack decisions and check lines

Both compiled packs read: `product_appearance` (PA-D1..D10) and `composition_and_attention` (CA-D1..D11); both carry status `PROPOSED — Canon-stream worker output; no Controller decision adopts it`. The 21 check lines are the ones rendered by id in Stage 3.

## Routing table

Saved verbatim to `stages/evidence/routing-table.txt` (61 cells; summary `clean_observed 36 / directional_only 25`; `production_use_allowed True 29 / manual_only 15 / False 17`). Cells this job may touch (credit pools only, no fal, per the Controller):

| cell | status | use | accepts | pinned price | pool |
|---|---|---|---|---|---|
| IMG-CORE/nano-banana-2 | clean_observed | True | 7/8 | 0.067 per_image | credits |
| IMG-CORE/nano-banana-pro | clean_observed | True | 4/8 | 0.134 per_image | credits |
| IMG-TEXT/nano-banana-2+A_cheap_generated | clean_observed | True | 4/4 | 0.067 per_image | credits |
| IMG-TEXT/nano-banana-pro+B_premium_generated | clean_observed | True | 4/4 | 0.134 per_image | credits |
| VID-I2V/veo-3.1-fast-i2v | clean_observed | True | 5/8 | 0.1 per_second | credits |
| VID-T2V/veo-3.1-fast | clean_observed | True | 4/8 | 0.1 per_second | credits |
| VID-T2V/gemini-omni-1.1-flash | clean_observed | True | 8/8 | 0.10136 per_second | credits |
| VID-REF/veo-3.1-fast-ref2v+native | clean_observed | True | 2/4 | 0.1 per_second | credits |
| VID-MS/veo-3.1-fast-extend+chain | directional_only | manual_only | 2/2 | 0.1 per_second | credits |
| VID-MS/gemini-omni-1.1-flash-10s | directional_only | manual_only | 2/2 | 0.10136 per_second | credits |
| VID-TOPO3/nano-banana-2+A2_nb_plate_9x16 | directional_only | manual_only | 1/2 | 0.067 per_image | credits |
| VID-KNEE/veo-3.1-full+knee_premium | directional_only | manual_only | 1/2 | 0.4 per_second | credits |
| VID-KNEE/veo-3.1-lite+knee_cheap | directional_only | **False** | 0/2 | — | credits |
| VID-TOPO3/veo-3.1-full+B_premium_native_t2v | directional_only | **False** | 0/2 | — | credits |
| MUS/lyria+native | clean_observed | True | 4/4 | 0.06 per_clip | credits |
| AUD-TTS/sarvam-bulbul-v3+native | clean_observed | True | 6/6 | 3.0 per_1000_characters (PriceBook defect: see PRODUCTION-WORKFLOW §7; harness figure ≈ USD 0.003/1000 chars) | sarvam_credits |
| AUD-TTS/elevenlabs-v3-direct+native | clean_observed | True | 4/6 | 0 (plan credits) | elevenlabs_credits |
| Gemini TTS | **no Registry cell** (reference-kit job-local pin only) | — | — | — | credits |

## Production-learning count

2 cases: UPWORK-INTRO-001, UPWORK-PORTFOLIO-002.

## Spend authority

**absent** at bootstrap. The task brief gives a PROVISIONAL planning ceiling of USD 10.00 (credits only, 0 hidden retries, hard stop) and states it is unconfirmed. `CAP_USD` in `tools/dispatch.py` stays `0.0` until a Controller message carries the confirmed cap. No paid call of any kind before that.

## MEDIA AGENCY READY (written here, not printed, per the task brief)

```
MEDIA AGENCY READY
main: 4d919c9 (production base; worktree HEAD 60813e3)
Canon packs available: product_appearance, composition_and_attention (both PROPOSED status; the only compiled packs)
production-learning cases: 2 (UPWORK-INTRO-001, UPWORK-PORTFOLIO-002)
commercial profile: not read (customer_work; Upwork reads skipped per task brief)
spend authority for this job: absent (provisional planning ceiling USD 10.00, unconfirmed; CAP_USD = 0.0)
```
