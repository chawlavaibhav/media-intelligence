# Stage 0 — Bootstrap record (USD 0)

Job `AGY-2026-09-20-RENTOK-GAME-LANE-A-001` · class `customer_work` · lane A of the two-lane RentOK experiment.
Worktree `media-intelligence-rentok-lane-a`, branch `work/agency-job-rentok-game-lane-a-001`.

## 1. HEAD and protected trees (OBSERVED)

```
git rev-parse --short HEAD      -> cee442a   (scaffold commits on top of origin/main @ 4d919c9)
production_base_sha             -> 4d919c9df6c9725a2f14c411771565bb09089876
git status --short              -> empty (clean before this job's files)
git status --short -- canon eval/registry eval/capability-map coordination -> empty
bootstrap started (date -u)     -> 2026-09-20T18:08:20Z
```

Tools observed: `/usr/bin/python3` = Python 3.9.6 (yaml, Pillow, numpy import OK — used for every runtime call in this job) · ffmpeg 8.1.2 · ffprobe · `hb-view` at `/opt/homebrew/bin/hb-view`.

## 2. What was read (OBSERVED, in this order)

- `shared/COMMUNICATION-STANDARD.md` (acknowledgement in the final report).
- `PROJECT-MEMORY.md` §1, §2, §5, §7 · `coordination/CONTROL-STATE.md` §2, §3, §6, §8.
- `.claude/skills/media-agency/SKILL.md`, `BOOTSTRAP.md`, `PRODUCTION-WORKFLOW.md`, `QA-CHECKLIST.md`, `JOB-TEMPLATE.yaml`.
- `canon/CANON-SHAPE-v1.md` §4–§5 · `canon/packs/pack-triggers-v0.yaml` · `runtime/ALPHA-1.md` §"What exists / does not exist".
- `production-learning/README.md`; cases `UPWORK-INTRO-001` and `UPWORK-PORTFOLIO-002`: `README.md`, `SYSTEM-DEFECTS.yaml`, `ROUTE-OBSERVATIONS.yaml`, `PROMOTION-QUEUE.yaml`; `UPWORK-INTRO-001/ACCEPTED-TEMPLATE.yaml` (pacing values, `evidence_scope: this_accepted_template`).
- `input/01-CUSTOMER-BRIEF-FROZEN.md`, `input/03-ACCEPTANCE-CONTRACT.md`, `input/04-QUESTION-TEMPLATE-v0.1-FROZEN.md`.
- `source/rentok-snapshot/README.md`, `fetched_utc.txt` (2026-09-20T18:00:45Z), `SHA256SUMS.txt`, and all four `.txt` extracts (home, tenant-verification, autopay, complaint-management).
- `tools/reference-kit/README.md`, `_common.py`, `dispatch.py` (fal routes present in the kit; to be removed in this job's copy).
- Upwork profile reads skipped: this job is `customer_work`, not portfolio (instruction from the Controller).

## 3. Bootstrap commands run (USD 0)

1. Pack decisions + check lines: both compiled packs print `status: PROPOSED — … CONTROL-STATE.md governs`. Decision ids available for rendering by id: `PA-D1..PA-D10`, `CA-D1..CA-D11` (21 check lines).
2. Routing table: 61 cells; summary `clean_observed 36 / directional_only 25`, `production_use_allowed True 29 / manual_only 15 / False 17`. Saved verbatim to `stages/evidence/routing-table.txt`.

Cells relevant to this job's constraint set (credits only, no fal), copied from that file:

| Cell | Status | Use | Accepts | Pinned price | Pool |
|---|---|---|---|---|---|
| IMG-CORE / nano-banana-2 | clean_observed | True | 7/8 | 0.067 per_image | credits |
| IMG-CORE / nano-banana-pro | clean_observed | True | 4/8 | 0.134 per_image | credits |
| IMG-TEXT / nano-banana-2+A_cheap_generated | clean_observed | True | 4/4 | 0.067 per_image | credits (model_draws_text) |
| IMG-TEXT / nano-banana-pro+B_premium_generated | clean_observed | True | 4/4 | 0.134 per_image | credits (model_draws_text) |
| VID-I2V / veo-3.1-fast-i2v | clean_observed | True | 5/8 | 0.1 per_second | credits |
| VID-T2V / veo-3.1-fast | clean_observed | True | 4/8 | 0.1 per_second | credits |
| VID-T2V / gemini-omni-1.1-flash | clean_observed | True | 8/8 | 0.10136 per_second | credits |
| VID-REF / veo-3.1-fast-ref2v+native | clean_observed | True | 2/4 | 0.1 per_second | credits |
| VID-MS / gemini-omni-1.1-flash-10s | directional_only | manual_only | 2/2 | 0.10136 per_second | credits |
| VID-MS / veo-3.1-fast-extend+chain | directional_only | manual_only | 2/2 | 0.1 per_second | credits |
| VID-TOPO3 / nano-banana-2+A2_nb_plate_9x16 | directional_only | manual_only | 1/2 | 0.067 per_image | credits |
| MUS / lyria+native | clean_observed | True | 4/4 | 0.06 per_clip | credits |
| AUD-TTS / sarvam-bulbul-v3+native | clean_observed | True | 6/6 | 3.0 per_1000_characters (pin; PriceBook quotes USD 0.003773 for 120 chars) | sarvam_credits |
| AUD-TTS / elevenlabs-v3-direct+native | clean_observed | True | 4/6 | 0 pinned in map; PriceBook quotes 0.1 per_1000_characters | elevenlabs_credits |

Gemini TTS has no Registry cell and no roster price (the reference kit carries a job-local pin from a Gemini pricing page fetched 2026-09-15; that pin's html is NOT in this job's `source/` — see Stage 4).

Observed discrepancy, recorded not resolved: the runtime PriceBook labels the Sarvam and ElevenLabs quotes `cash` while the taint register labels the pools `sarvam_credits` / `elevenlabs_credits`. The pools that exist for this job are the plan credits named by the Controller; the PriceBook label is treated as a display defect and noted for the sync PR.

## 4. Spend authority (OBSERVED)

Absent at bootstrap. The Controller is obtaining a written cap; a PROVISIONAL ceiling of USD 10.00 is used for planning only. `CAP_USD` in `tools/dispatch.py` stays `0.0` until the written cap arrives. No paid call of any kind before then.

## 5. READY block (written here, not printed to the user, per the Controller's instruction)

```
MEDIA AGENCY READY
main: 4d919c9 (production base; job HEAD cee442a)
Canon packs available: product_appearance (PA-D1..D10), composition_and_attention (CA-D1..D11) — both status PROPOSED; only these two are compiled
production-learning cases: 2 (UPWORK-INTRO-001, UPWORK-PORTFOLIO-002)
commercial profile: not read — job class customer_work (Controller instruction)
spend authority for this job: absent (provisional planning ceiling USD 10.00; CAP_USD = 0.0 until the written cap)
```
