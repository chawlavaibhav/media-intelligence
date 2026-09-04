# Cost Summary — recovered historical spend

All figures USD unless marked ₹. Two independent records exist and **disagree**; both are reported.

## 1. On-disk ledger (`spike/out/costs.jsonl`, 129 entries) — total **$35.28**

| Model / endpoint | Ledger USD | Unit price used | Notes |
|---|---|---|---|
| fal-ai/nano-banana-pro/edit | $5.10 | $0.15/img | 2 sheets + 32 stills |
| fal-ai/bytedance/seedream/v4.5/edit | $1.28 | $0.04/img | 32 stills |
| fal-ai/veo3.1/fast/image-to-video | $13.20 | $1.20/8s clip ($0.15/s) | **over-counted**: duplicate entries for retried takes (e.g. vid_veo_t0 logged 3×) |
| fal-ai/wan-25-preview/image-to-video | $6.00 | $0.50/10s clip ($0.05/s) | over-counted same way |
| fal-ai/bytedance/seedance/v1/lite (i2v) | $0.80 | ~$0.40/5s clip (est., token-priced) | incl. one ghost clip (billed, file missing: vid_seedance_t0) |
| lipsync experiment (seedance-idle / sadtalker / latentsync) | $0.50 | $0.12 / $0.10 / $0.07 per shot | |
| "film" (guddu v1: 12 plates + 12 motion) | $4.80 | plates $0.15, motion $0.25 | |
| "scene7" (2 Wan beats + Lyria music) | $1.10 | Wan $0.50, Lyria $0.10 | Veo beats refused → $0 |
| "film2" (5 performed Wan beats) | $2.50 | $0.50/beat | batch2 never ran (no ledger entries, no files) |

**Known ledger gaps:** Sarvam TTS, ElevenLabs, the s7 dub/hindi retakes, `s_music_*`, `film_audio*` generations, and the gallery run (2026-07-24) were never logged. Failed attempts are double-counted; ghost-billed clips appear once.

## 2. Dashboard-verified (fal billing UI, checked 2026-07-19; recorded in project memory — Tier C)

- Spike bill to that date: **$22.38 (≈ ₹1,960)**, including ~₹500 of ghost clips "billed but never downloaded" (14 Wan clips billed vs 5 kept, queue-polling bug).
- guddu film dress-rehearsal (2026-07-20): **~₹1,050 (≈ $12.2)** "burnt across 3 failed builds".

## 3. Production-era verified unit costs (live-verified, memory/commits — Tier C)

- V0 static campaign: **$0.025** (3 on-brand ads, FLUX-era).
- V1 full campaign (3 statics + 6 videos + 6 WhatsApp renditions): **$0.228**, ~90s.
- GPT Image 2 hero: **$0.04/img** (Render env `FAL_IMAGE_PRICE=0.04`).
- Production totals (Render + fal over the live period): **unknown** — not recoverable from the repo.

## 4. Derived economics (computed now from Tier-A data; not recorded historically)

- **Cost per accepted still:** Seedream 4.5 edit $1.28/29 = **$0.044**; Nano Banana Pro $4.80/25 = **$0.192** (4.4×).
- **Talking-shot ladder (per ~10s shot, as published on videos.html):** SadTalker ₹10 (rejected) · LatentSync+Sarvam ₹16–20 · LatentSync+ElevenLabs ~₹25 · Seedance b-roll+VO ~₹35 · Wan native ₹42 · Veo ₹105.
- **Benchmark video estimate (RentOk-class, ~10 talking shots):** ₹850–1,150 mixed-tier vs ₹1,800–2,300 all-Veo (memory, Tier C; user-approved quality at the cheap tier).
- Film COGS estimate if LatentSync passes ear-check: ~₹60–80; else ~₹120 (memory, Tier C).

## Bottom line

**Total recovered historical experiment spend ≈ $35 (ledger view) / ≈ $34.6 (dashboard view: $22.38 spike + ~$12.2 guddu), plus unquantified production-era spend.** Use the dashboard view as the closer estimate of real money; use the ledger for per-artifact attribution only, with the caveats above. All prices are July-2026 prices; the Aug-2026 landscape check already moved Veo and Seedance materially.
