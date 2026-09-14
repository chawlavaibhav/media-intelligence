# SPEND AMENDMENT V4 — UPWORK INTRO VIDEO V4 (continuation of pilot `upwork-intro-video-2026-09-14`)

**Written 2026-09-14 ~19:40 IST, BEFORE any V4 paid call.** Authority: Controller package "UPWORK INTRO VIDEO V4" (this
session) §3: "This is a CONTINUATION of the same Upwork showcase pilot. The previous hard ceiling was INR 2,000 cumulative.
IT DOES NOT RESET." Run class: commercial showcase pilot / product-learning. Not Alpha-1, Registry, Lab or Stage evidence.

| Item | Figure |
|---|---|
| Prior cumulative cap (V3 record `../v3/plan/SPEND-RECORD-V3.md`) | **INR 2,000 = USD 20.96** at the repo display rate 95.4211 |
| Prior consumed, conservative = every `reserved` line in `../v3/gen/LEDGER.jsonl` (36 lines, failed calls included) | **USD 3.2836 = INR 313.3** |
| Remaining under the cap before V4 | **USD 17.68 = INR 1,686.7** |
| **V4 does not reset the cap.** V4 lines append to a NEW ledger `gen/LEDGER.jsonl` whose opening cumulative is 3.2836 (carried) | |

**Billing pools now.** fal cash **USD 0.2589** (read 19:05 IST; Wan 3.0 Prime 8 s native = USD 1.12 → **Wan fallback is NOT
callable** without a top-up). Vertex credits (Veo 3.1 Fast, Gemini Omni 1.1 Flash on Vertex, Lyria): balance not readable
by API without the console; the pool carried V2's Veo calls at 17:00 IST today. Gemini API credits (Nano Banana 2 still):
carried V3's checks today. Sarvam: not used in V4.

**Planned calls (all Vertex/Gemini credits).**

| # | Call | Route (surface) | Pinned unit | Est. USD |
|---|---|---|---|---|
| 1 | Speaker anchor still, 16:9 (1 draw; 1 redraw only if the still fails §7) | Nano Banana 2 `gemini-3.1-flash-image` (Gemini API) | 0.067 / image | 0.067 (max 0.134) |
| 2 | Speaker candidate A: i2v + native speech, 10 s, 720p (1080p token rate is not pinned) | Gemini Omni 1.1 Flash `gemini-omni-1.1-flash-preview` (Vertex interactions) | 0.10136 / s | 1.014 |
| 3 | Speaker candidate B: i2v + native speech, 8 s, 1080p | Veo 3.1 Fast `veo-3.1-fast-generate-001` (Vertex predictLongRunning) | 0.12 / s | 0.96 |
| — | Wan 3.0 Prime native (third fallback) | fal — **not callable** (balance) | 0.14 / s | 0 |
| — | New showcase media | none planned; V3 accepted media reused | — | 0 |
| | **Planned first pass** | | | **≈ USD 2.04 = INR 195** |
| | **Maximum incremental V4 spend** (planned + one still redraw + one repeat of ONE speaker candidate if a provider error, not a quality fail, voids a draw) | | | **USD 3.20 = INR 305** |
| | Cumulative if the maximum is spent | | | USD 6.48 = INR 619 of INR 2,000 |

**Rules.** Reservation line before every request; cumulative check against USD 20.96 at every dispatch (`tools/gen4.py`,
which carries the V3 total forward). One draw per candidate; a quality fail is never re-drawn on the same route. If the
still fails §7 on the first draw, exactly one redraw. No new showcase media unless a V4 slot cannot meet its acceptance
contract with existing accepted V3 media, and the reason is written to `gen/ASSETS.jsonl` before the dispatch.
If the accounting above cannot be reconciled at dispatch time, stop before the call.

## Addendum 1 (19:58 IST) — Veo provider outage
`v4-speaker-veo-r1` and `-r2` both ended with gRPC 14 UNAVAILABLE (no media; reserved USD 0.96 each, conservative). The
Controller's order is to run the Veo candidate; the route worked at 17:00 IST today (V2). One further attempt after a wait
is authorised by this addendum: maximum incremental V4 spend raised from USD 3.20 to **USD 4.20**. If it fails again the
run stops before any further paid call.

## V4.1 (assembly repair, Controller verdict SPECIFIC REPAIR) — USD 0
No paid call. `gen/LEDGER.jsonl` unchanged (cumulative reserved USD 7.3112 = INR 697.6). All changes are compositor/edit changes over
existing accepted assets (`v4/tools/film4.py`, `mix4.py`); the Kora full-screen beat uses V3's deterministic `kora-hook-1-16x9.png`.
