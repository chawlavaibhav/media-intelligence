# Controller — Spend Authorisation, Capability Lab Image Round 1 — 2026-09-08

**Status:** APPROVED CONTROLLER DECISION. First paid tranche of the Capability Lab.
**Role:** Writer Controller, recording the human Controller's approval verbatim before any paid call
(EVAL-038 / DN-07 pattern).
**Parent:** `CONTROLLER-CAPABILITY-LAB-DIRECTION-2026-09-05.md` (ratified the same moment, §8).
**Task executed under it:** EVAL-040, scope limited to this record.

## 1. Authority — the Controller's words, verbatim (2026-09-08, ~12:00 IST)

Put to the Controller: *"Ratify the direction, sign an image-round cap of ₹1,200 for the first half,
and I run it today with a single smoke-test image before the lane."*

Controller:

> **"Go for it. Approved now"**

Preceded in the same exchange by: *"We go for images one."* and, on round two, *"250 USD is nearly
25k inr. fairly high"* — hence the smaller first step.

## 2. Scope

**Image lane, half one:** cases `IMG-CORE-01`, `IMG-CORE-02`, `IMG-CORE-03`, `IMG-CORE-04`,
`IMG-TEXT-01`, `IMG-TEXT-02` from the frozen package
`eval/empirical-planning/STAGE-A-FREEZE-2026-09/` (item basis commit `0596aa2`, carried unchanged
on `main` by the PR #87 merge). Two repeats per item. Routes and nominal cost, from
`COST-TABLE.yaml` priced against roster sha256
`99cde63c8c668e57457915ee1aae69e7ba7f09ed9c8b2d26bc5a3a0537aa2b46`:

| Route | Surface | Pool | Calls | Nominal USD |
|---|---|---|---:|---:|
| gpt-image-2 | fal | cash | 12 | 0.636 |
| nano-banana-2 (`gemini-3.1-flash-image`) | Google | credits | 12 | 0.804 |
| nano-banana-pro (`gemini-3-pro-image`) | Google | credits | 12 | 1.608 |
| seedream-5-pro | fal | cash | 12 | 0.810 |
| flux-2-pro (core + textless composite base) | fal | cash | 12 | 0.360 |
| qwen-image-3 | fal | cash | 12 | 0.480 |
| recraft-v4 (text cases, premium arm) | fal | cash | 4 | 0.160 |
| **Total** | | | **76** | **4.858 ≈ ₹464** |

Plus one **smoke-test image** on the cheapest Google route before the lane (≈ USD 0.07), and
Cloud Vision text detection on the text-case artifacts (≈ USD 0.05). Conditional routes (SD3.5,
MAI-Image-2.6) and all edit / reference / extend / compose cases are **outside** this record.

## 3. Hard limits

- **Cap: ₹1,200 = USD 12.58 USD-equivalent** at the 26-Aug reference rate 95.4211 (display-only
  rate; provider invoices stay in source currency), enforced across cash and credits together.
- 0 retries. A failed, refused or timed-out call is a trial and is recorded.
- Reservation before send; execution-time price check against the roster pin; refuse on mismatch;
  stop at the cap without exception.
- Credentials: the Google service account and fal key already on this machine, read by name at
  dispatch, never persisted. No new cloud resource is created for this round (direction §8 item 2).
- Media role: product evidence (blind Controller acceptance) plus deterministic-instrument
  evidence; Registry rows only from `deterministic` instruments; the post-draw gate runs on every
  artifact as an observation and yields no verdict on Canon.
- Every artifact sealed as committed bytes with sha256 (EVAL-024 pattern), plus the ledger.

## 4. Machine block (materialised verbatim into `eval/harness-v2/authorization.local.yaml`, gitignored)

```yaml
machine_authorisation:
  tranche_id: EVAL-040-TRANCHE-1
  authorised: true
  item_basis_commit: "0596aa2"
  price_basis_roster_sha256: "99cde63c8c668e57457915ee1aae69e7ba7f09ed9c8b2d26bc5a3a0537aa2b46"
  max_consumed_usd_equivalent: 12.58
  cap_1a_usd: 12.58
  cap_1b_usd: 0.00
  sarvam_cap_inr: 0.00
  retries_authorised: 0
  execution_time_route_price_verification: required_before_every_paid_call
  images_before_video: true
  approved_by: "Vaibhav Chawla (Controller) — \"Go for it. Approved now\""
  approved_at: "2026-09-08T12:00:00+05:30"
```

`cap_1b_usd: 0.00` and `sarvam_cap_inr: 0.00` mean: no 1b call and no Sarvam call can be
dispatched under this record. A later record raises them.

## 5. Not authorised by this record

Any video, audio, music or lip-sync call; any edit / reference / extend / compose case; any
conditional route; any call after the cap; any Registry row from a non-deterministic instrument;
any conclusion about whether Canon works; any change to the frozen package or the roster (a change
means a rebuild and a new record).

## 6. Addendum — composite arm re-run (Controller, 2026-09-08 ~15:45 IST: "do it")

Image Round 1 dispatched the composite arm (arm C, FLUX.2 Pro textless plate) of IMG-TEXT-01/02 with the main
text-bearing prompt, because the harness selected one prompt per case. The blueprints already carried a textless
plate prompt (`### generation_prompt_textless_plate (arm C only)`); the harness now selects it for `C_composite*`
arms (`casebook.py`, test `test_casebook_arms.py`). The frozen package and the item basis commit are unchanged.

Authorised under this record's existing scope and cap: run `img-r1-composite` — the same four arm-C rows
(IMG-TEXT-01 ×2, IMG-TEXT-02 ×2) on FLUX.2 Pro with the textless prompt, ≈ USD 0.12 — plus the deterministic overlay
step at USD 0 (exact strings rendered with a pinned system font and composited by code onto each plate). The
composited pictures are judged by the Controller against the same contracts; they cannot be blind as to arm
(code-set type is visibly code-set), so only the plate order is shuffled. The original arm-C trials in `img-r1`
stay on the record as what they were: FLUX generating text from the main prompt.
