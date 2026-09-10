# Controller — Spend Authorisation (DRAFT awaiting "go"): Wan 2 contender round — 2026-09-10

**Status:** PREPARED by the Writer Controller under `CONTROLLER-WAN2-CONTENDER-PREMIUM-DEFERRED-2026-09-09.md`
("where wan 3 is passing, we will keep wan 2 as contender"). **Becomes an authorisation only on the Controller's "go".**

## 1. Scope — `wan-2.2-a14b` (fal, USD 0.08 per video second at 720p, pinned) on exactly the rows Wan 3.0 Prime passed

| Rows | Workflow | Clips | Seconds | Cost |
|---|---|---|---|---|
| VID-T2V-01, 02, 03 | text-to-video, 6 s | 6 | 36 | USD 2.88 |
| VID-I2V-01..04 (the same accepted Nano Banana stills) | image-to-video, 6 s | 8 | 48 | USD 3.84 |
| VID-2SPK-01 | text-to-video, 8 s | 2 | 16 | USD 1.28 |
| | | **16 + 1 smoke** | | **USD 8.00 (+ smoke 0.48) ≈ USD 8.5** |

Wan 2.2 A14B has no audio field: on the two briefs with speech it is judged visually only (recorded on the rows). fal
bills video seconds at 16 fps and the model takes 4n+1 frames, so each call may carry 1/16 s extra (worst case +USD 0.08).
Why this tier: the cheaper Wan rungs (2.5 preview at USD 0.05/s, turbo, 5B) make only fixed 5/10-s clips and cannot
render the frozen 6-s and 8-s rows.

## 2. Cap and hard limits

Cap **₹800 = USD 8.39** (`max_consumed_usd_equivalent`; `cap_1a_usd` = `cap_1b_usd` = 8.39). Package commit
d8399d84b8b4, roster sha 311f6631…; retries 0; price verified before every paid call; sealed evidence write-once; blind
judging by the Controller; Registry rows only from the deterministic instruments. Run ids `vid-wan2(-smoke)`;
authorisation file `eval/harness-v2/authorization.wan2.local.yaml` (gitignored, materialised on "go").

## 3. Not authorised

Anything else on Wan 2; Seedance / Wan premium (deferred to a real brief); round two of stills (later).
