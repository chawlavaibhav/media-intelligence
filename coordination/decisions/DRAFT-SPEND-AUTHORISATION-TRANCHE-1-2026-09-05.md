# DRAFT — Spend Authorisation, Capability Lab Tranche 1 (Stage A route admission screen)

**Status:** UNSIGNED DRAFT prepared overnight by the Writer Controller session, 2026-09-05 ~03:50 IST.
**Nothing is authorised until the human Controller signs §6 in their own words.** Until then no paid
call may be made under EVAL-040.
**Parent decision:** `CONTROLLER-CAPABILITY-LAB-DIRECTION-2026-09-05.md` (itself DRAFT, pending ratification).
**Pattern:** EVAL-038 / DN-07 — verbatim authorisation recorded before the first paid call; hard cap;
0 retries; execution-time route/price verification; keys from this machine.

## 1. Item basis (what is generated)

`eval/empirical-planning/STAGE-A-FREEZE-2026-09/` at commit `0596aa2` — 35 customer-shaped cases,
35 frozen Canon blueprints, acceptance contracts, elimination rules E1–E5 with proportional
denominators, seed policy, evaluator plan. Approver verdict: PASS WITH NOTES
(`eval/tasks/EVAL-039A-APPROVER-VERDICT.md`). Rebuild is byte-identical from `tools/build.py`.

## 2. Price basis (what it costs)

`eval/empirical-planning/ROSTER-REFRESH-2026-09.yaml`, sha256
`99cde63c8c668e57457915ee1aae69e7ba7f09ed9c8b2d26bc5a3a0537aa2b46` (commit `3434b37`); 36 vendor
pages pinned as bytes under `price-pins-2026-09/`. Approver verdict: PASS WITH NOTES
(`eval/tasks/EVAL-039B-APPROVER-VERDICT.md`). Regular prices only; the MiniMax promotion is recorded
and never used. If the roster changes, the package is rebuilt, never hand-edited.

## 3. Calls and nominal cost (from `COST-TABLE.yaml`, recomputed independently by the Approver)

| Tranche | Calls | Cash (fal) | GCP credits (Vertex) | Sarvam credits | Nominal |
|---|---:|---:|---:|---:|---:|
| **1a** — image core, exact text (TOPO-02), edit/reference, text-to-video core, native dialogue, TOPO-03, cost knee | 192 | USD 50.15 | USD 25.50 | — | **USD 75.65** |
| **1b** — image-to-video, reference-to-video, multi-shot (incl. 15 s), TTS, lip-sync, music | 96 | USD 65.30 | USD 15.51 | ₹0.80 | **USD 80.81** |
| **Tranche 1** | **288** | **USD 115.45** | **USD 41.01** | ₹0.80 | **USD 156.46** |
| Conditional (only if the Controller enables Azure / Bedrock routes) | +32 | — | ≈ USD 5.44 | — | outside cap |
| Unpinned, excluded from cap (gpt-image-2 edit 12, sync-lipsync v3 6, Veo Lite i2v 2) | 20 | — | — | — | outside cap |
| Evaluator calls (Cloud Vision, VLM triage; ASR unpriced) | — | ≈ USD 3.71 | — | — | inside cap |

Credits are "billed to the cloud account"; balances are unverified (MD-1). Caps are USD-equivalent
ceilings across both pools. 1b's plates and drives exist only after the Controller's blind
acceptance of 1a, so 1b is dispatched second.

## 4. Proposed caps and execution rules

- **Hard cap Tranche 1a: USD 85.00** (nominal 75.65 + ≈12 % headroom). Alternative: keep the plan's
  USD 60 and apply the cut order in `IRREDUCIBILITY.md`.
- **Hard cap Tranche 1b: USD 115.00** (nominal 80.81).
- **Tranche 1 total ceiling: USD 200.00 USD-equivalent** across cash and credits, plus ₹5 Sarvam.
- 0 retries; a failed, refused or timed-out call is a trial. Reservation before send; execution-time
  price check against the roster pin; refuse dispatch on mismatch; stop at cap without exception.
- Images first: the image lane runs and is judged blind before any video call.
- Media generated here is **product evidence and deterministic-instrument evidence only**; Registry
  rows come solely from `deterministic` instruments per the Registry writer.

## 5. Decisions folded into this authorisation (tick or amend)

| # | Decision | Default if the Controller says "approve with defaults" |
|---|---|---|
| A1 | Ratify counts 192 / 96 / 288 (+32 conditional) — deviation from the task's 186 / 112 / 298 explained in the package README | ratified |
| A2 | 1a cap: raise to USD 85 or cut per `IRREDUCIBILITY.md` | raise to 85 |
| A3 | The 20 unpinned calls: drop for Tranche 1 or pin and add | drop; revisit in Stage B |
| A4 | Two-speaker chain arm not run (no lip-sync route can assign faces); prior 4 tested on native routes only | accepted |
| A5 | TOPO-01 residual confound (arm B's on-screen person differs) — accept or fund +4 calls | accept |
| A6 | gpt-image-2 at quality=medium (fal default is high, +≈ USD 4) | medium |
| A7 | Lyria: `lyria-002` at the Lyria 2 rate; music lane 8 calls | as stated |
| A8 | Veo billed per second by assumption ("/ 1 count" on the page); first metered bill verifies | accepted |
| B1 | MD-1 credit balances on AWS / GCP / Azure — state them | unknown; proceed as USD-equivalent |
| B2 | MD-2 Azure deployments (gpt-image-2, FLUX.2-pro, Sora 2) in the getaight subscription | none tonight; fal cash |
| B3 | MD-3 new GCP project | no — dedicated service account only |
| B4 | MD-4 Bedrock offers pay-per-use, EULA unread | accept nothing; SD3.5 conditional |
| B5 | MD-5 Runway account | defer to Stage B |
| B6 | MD-8 Polly permission on the new AWS identity | yes (free until called) |
| B7 | MD-9 fresh isolated cloud resources and keys — Controller's own session, commands and undo in `MORNING-DECISIONS.md` | not created until the Controller runs them |
| C1 | Controller-supplied photos for the edit / reference / compose cases, or accept constructed / Resources items under the stated rights rule | constructed / Resources |
| C2 | Lip-sync drive route: ElevenLabs repeat 1 (default) or Sarvam | ElevenLabs |
| C3 | Fourth image-core slot = the Hindi emotional child-scene (policy edge) | as stated |

## 6. Authorisation (to be written by the human Controller, verbatim)

> _(empty until signed)_

```yaml
machine_authorisation:
  tranche_id: EVAL-040-TRANCHE-1
  authorised: false            # flips to true only with the Controller's words above
  item_basis_commit: "0596aa2"
  price_basis_roster_sha256: "99cde63c8c668e57457915ee1aae69e7ba7f09ed9c8b2d26bc5a3a0537aa2b46"
  max_consumed_usd_equivalent: null   # proposed 200.00
  cap_1a_usd: null                    # proposed 85.00
  cap_1b_usd: null                    # proposed 115.00
  sarvam_cap_inr: null                # proposed 5.00
  retries_authorised: 0
  execution_time_route_price_verification: required_before_every_paid_call
  images_before_video: true
  media_role: product evidence + deterministic-instrument evidence; Registry rows only from deterministic instruments
  approved_by: null
  approved_at: null
```
