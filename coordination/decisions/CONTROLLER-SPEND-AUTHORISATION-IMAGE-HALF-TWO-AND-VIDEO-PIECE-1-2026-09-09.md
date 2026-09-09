# Controller — Spend Authorisation: Image Half Two (constructed stand-ins) and Video Piece 1 (text into motion) — 2026-09-09

**Status:** APPROVED CONTROLLER DECISION.
**Role:** Writer Controller, recording the human Controller's words before any paid call.
**Parent:** `CONTROLLER-CAPABILITY-LAB-DIRECTION-2026-09-05.md` §8; previous record
`CONTROLLER-SPEND-AUTHORISATION-IMAGE-ROUND-1-2026-09-08.md` (closed: ≈ USD 5.36 of ₹1,200 spent).

## 1. Authority — the Controller's words (2026-09-09)

Put to the Controller: (1) freeze thresholds, (2) *"Photos for image half two … Or approve constructed
stand-ins"*, (3) *"Authorise the first video round, starting with the text-into-motion case, which now has
its plate. I will size it and write the spend record when you say go."*

> **"freeze as proposed, constructed stand in, go ahead"**

The caps below are the Writer Controller's sizing under that approval; each is small and stops mechanically.

## 2. Scope A — Image half two on constructed stand-ins (cap ₹700 = USD 7.34)

Cases `IMG-EDIT-01`, `IMG-EDIT-02`, `IMG-EXT-01`, `IMG-COMP-01`, `IMG-REF-01`, `IMG-REF-02` from the frozen
package (item basis commit `0596aa2`), on the four edit/reference routes (FLUX.2 Pro edit, Nano Banana Pro edit,
Seedream 5 Pro edit, GPT Image 2 edit — the last priced on fal's token meter and therefore run only if its price
pins; otherwise excluded), two repeats: ≤ 48 calls, nominal ≈ USD 3.5. Plus **constructed stand-in inputs**
generated once on the cheapest Google route (Nano Banana 2, credits) from prompts written from each case's
`reference_assets` specification — the showroom sofa with a staff member, the masala pack raw shot, the
mustard-oil tin (three views) with two same-category decoy tins, the recurring host (a synthetic person) with two
decoy portraits, the backwaters banner, the model portrait and the lipstick packshot: ≤ 16 calls, ≈ USD 1.1.
Stand-ins are sealed as fixtures with their prompts and are labelled `constructed_synthetic` on every row that
uses them; they are never presented as customer photos.

## 3. Scope B — Video piece 1: text into motion, `VID-TOPO3-01` (cap ₹900 = USD 9.43)

The three arms of the frozen case, at 9:16, 6 s, 720p, two repeats: arm A — the Diwali still WITH cheap-generated
text (two 9:16 draws of IMG-TEXT-01 on Nano Banana 2) animated by MiniMax H3 Max, Wan 3.0 Prime and Veo 3.1 Lite
(Veo Lite image input runs only if its price pins); arm B — Veo 3.1 (full) and Kling v3 Pro generating the text
natively from the text prompt; arm C — a 9:16 textless plate (FLUX.2 Pro) animated by the cheapest pinned
image-to-video route, then the exact strings composited by code on every frame (static overlay). ≈ 4 image calls
+ ≈ 12–14 video calls, nominal ≈ USD 8. This is the first live use of the video adapters; the first call is a
single 6-second smoke test.

## 4. Hard limits (both scopes)

0 retries; reservation before send; execution-time price check; stop at cap; keys by name; sealed bytes; product
evidence plus deterministic-instrument rows (thresholds now frozen); blind Controller judging where the arm can be
hidden. Each scope has its own authorisation file (`eval/harness-v2/authorization.half2.local.yaml`,
`authorization.video1.local.yaml`, both gitignored) and its own ledger.

```yaml
machine_authorisation_half2:
  tranche_id: EVAL-040-TRANCHE-1
  authorised: true
  item_basis_commit: "0596aa2"
  price_basis_roster_sha256: "99cde63c8c668e57457915ee1aae69e7ba7f09ed9c8b2d26bc5a3a0537aa2b46"
  max_consumed_usd_equivalent: 7.34
  cap_1a_usd: 7.34
  cap_1b_usd: 0.00
  sarvam_cap_inr: 0.00
  retries_authorised: 0
  execution_time_route_price_verification: required_before_every_paid_call
  images_before_video: true
  approved_by: "Vaibhav Chawla (Controller) — \"freeze as proposed, constructed stand in, go ahead\""
  approved_at: "2026-09-09T10:30:00+05:30"
machine_authorisation_video1:
  tranche_id: EVAL-040-TRANCHE-1
  authorised: true
  item_basis_commit: "0596aa2"
  price_basis_roster_sha256: "99cde63c8c668e57457915ee1aae69e7ba7f09ed9c8b2d26bc5a3a0537aa2b46"
  max_consumed_usd_equivalent: 9.43
  cap_1a_usd: 9.43
  cap_1b_usd: 0.00
  sarvam_cap_inr: 0.00
  retries_authorised: 0
  execution_time_route_price_verification: required_before_every_paid_call
  images_before_video: true
  approved_by: "Vaibhav Chawla (Controller) — \"freeze as proposed, constructed stand in, go ahead\""
  approved_at: "2026-09-09T10:30:00+05:30"
```

## 5. Not authorised

Any other video case; any audio, music or lip-sync; conditional routes; any Registry row from a non-deterministic
instrument; any conclusion about Canon; any spend beyond the two caps.
