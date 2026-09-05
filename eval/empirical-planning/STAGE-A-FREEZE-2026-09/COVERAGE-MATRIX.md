# Coverage matrix — Stage A freeze

35 cases, 288 calls (1a 192 / 1b 96) + 32 conditional. **4K recorded as a Stage B COND-DELIVERY level only; round one runs 720p.**

## 1. Plan §C.1 routing questions → cases

| routing question (plan §C.1) | cases |
|---|---|
| best commercial still without text | IMG-CORE-01, IMG-CORE-02, IMG-CORE-03, IMG-CORE-04 |
| best product-reference still / best person-reference still | IMG-COMP-01, IMG-REF-01, IMG-REF-02 |
| best supplied-image edit / preservation route | IMG-EDIT-01, IMG-EDIT-02, IMG-EXT-01, IMG-COMP-01 |
| best exact-text route; when text should be deterministic | IMG-TEXT-01, IMG-TEXT-02, VID-TOPO3-01 |
| best image-to-video route | VID-TOPO3-01, VID-I2V-01, VID-I2V-02, VID-I2V-03, VID-I2V-04 |
| best text-to-video route | VID-T2V-01, VID-T2V-02, VID-T2V-03, VID-T2V-04 |
| best reference-conditioned video route | VID-REF-01, VID-REF-02 |
| best multi-shot route | VID-MS-01, VID-MS-02 |
| best high-motion / action route | VID-T2V-02, VID-I2V-03 |
| best native dialogue / audio route | VID-T2V-01, VID-2SPK-01 |
| best Hindi / Hinglish route (COND-LANGUAGE) | IMG-CORE-02, IMG-CORE-04, IMG-EDIT-02, VID-T2V-01, VID-T2V-03, VID-2SPK-01, VID-I2V-02, VID-I2V-04, AUD-TTS-01, AUD-TTS-02, AUD-LIP-01, AUD-LIP-02 |
| best TTS route | AUD-TTS-01, AUD-TTS-02, AUD-TTS-03 |
| best lip-sync route | VID-2SPK-01, AUD-LIP-01, AUD-LIP-02, AUD-LIP-03 |
| cheapest acceptable production plate; premium when cheap fails | VID-T2V-04, VID-KNEE-01 |
| model-policy / refusal fallback | IMG-CORE-04, VID-T2V-03, VID-I2V-04 |
| behaviour under reference / constraint / language / motion / delivery load | Stage B sweeps (survivors only); Stage A records every family on every row |
| VID-04 edit existing footage (Runway Aleph) | deferred_no_account — Controller decision 5 |

## 2. Roster questions (SCIENTIFIC-WAVE1-MODEL-ROSTER) → cases

| question | cases |
|---|---|
| IMG-01 | IMG-CORE-01, IMG-CORE-02, IMG-CORE-03, IMG-CORE-04, IMG-TEXT-01, IMG-TEXT-02, VID-TOPO3-01 |
| IMG-02 | IMG-CORE-01, IMG-CORE-02, IMG-CORE-03, IMG-CORE-04, IMG-TEXT-01, IMG-TEXT-02, VID-TOPO3-01 |
| IMG-03 | IMG-CORE-01, IMG-CORE-02, IMG-CORE-03, IMG-CORE-04, IMG-EDIT-01, IMG-EDIT-02, IMG-EXT-01, IMG-COMP-01 |
| IMG-04 | IMG-CORE-01, IMG-CORE-02, IMG-CORE-03, IMG-CORE-04, IMG-COMP-01, IMG-REF-01, IMG-REF-02 |
| VID-01 | VID-T2V-01, VID-T2V-02, VID-T2V-03, VID-T2V-04, VID-2SPK-01 |
| VID-02 | VID-MS-01, VID-MS-02 |
| VID-03 | VID-TOPO3-01, VID-I2V-01, VID-I2V-02, VID-I2V-03, VID-I2V-04, VID-REF-01, VID-REF-02 |
| VID-04 | deferred_no_account (Runway) |
| VID-05 | VID-T2V-04, VID-KNEE-01 |
| AUD-01 | VID-2SPK-01, AUD-TTS-01, AUD-TTS-02, AUD-TTS-03 |
| AUD-02 | AUD-TTS-01, AUD-TTS-02, AUD-TTS-03 |
| AUD-03 | AUD-LIP-01, AUD-LIP-02, AUD-LIP-03 |

## 3. §C.3d additions

- one 15-second item: **VID-MS-01** (Kling v3 15 s, Seedance 2.5 15 s, Omni Flash 1.1 longest ≤ 15 s, Veo 3.1 fast + extend; 4 routes × 2 = 8 calls)
- one two-speaker Hindi dialogue item: **VID-2SPK-01** — native arm (Veo 3.1 fast, Kling v3 audio-on, Omni Flash 1.1, Seedance 2.5, Wan 3.0 Prime — Wan added after audit so freshness item 4's preferred route is present; 5 × 2 = 10 calls) and the chain arm (plate → i2v → TTS → lipsync) **recorded, not screened, 0 calls** (single-face lipsync routes document no speaker assignment — Auditor AF-3)
- music lane: **MUS-01**, **MUS-02** × 2 routes (Lyria on Vertex, ElevenLabs music on fal) × 2 repeats = 8 calls
- 4K: **not a case.** 4K recorded as a Stage B COND-DELIVERY level only; round one runs 720p.

## 4. Core counts and per-core requirements

| core | count | cases | Hindi/Hinglish | policy-edge | high-motion |
|---|---|---|---|---|---|
| image | 4 | IMG-CORE-01..04 | IMG-CORE-02 (hg), IMG-CORE-04 (hi) | IMG-CORE-04 | n/a |
| text-to-video | 4 | VID-T2V-01..04 | VID-T2V-01 (hi), VID-T2V-03 (hg) | VID-T2V-03 | VID-T2V-02 |
| image-to-video | 4 | VID-I2V-01..04 | VID-I2V-02 (hi), VID-I2V-04 (hi), VID-I2V-03 (hg) | VID-I2V-04 | VID-I2V-03 |
| TTS | 3 | AUD-TTS-01..03 | AUD-TTS-01 (hi), AUD-TTS-02 (hg) | waived — a TTS policy-edge has no source shape and no prior; stated | n/a |
| lipsync | 3 | AUD-LIP-01..03 | AUD-LIP-01 (hi), AUD-LIP-02 (hg) | waived — as TTS; stated | n/a |

## 5. TOPO-02 / TOPO-03 arms (generated from each case's `routes[]`)

| case | arm | routes (× repeats, tranche) |
|---|---|---|
| IMG-TEXT-01 | A_cheap_generated | `gemini-3.1-flash-image` ×2 (1a); `alibaba/qwen-image-3` ×2 (1a); `openai/gpt-image-2` ×2 (1a) |
| IMG-TEXT-01 | B_premium_generated | `gemini-3-pro-image` ×2 (1a); `bytedance/seedream/v5/pro/text-to-image` ×2 (1a); `fal-ai/recraft/v4 (text-to-image)` ×2 (1a) |
| IMG-TEXT-01 | C_composite_textless_base | `fal-ai/flux-2-pro` ×2 (1a) |
| IMG-TEXT-02 | A_cheap_generated | `gemini-3.1-flash-image` ×2 (1a); `alibaba/qwen-image-3` ×2 (1a); `openai/gpt-image-2` ×2 (1a) |
| IMG-TEXT-02 | B_premium_generated | `gemini-3-pro-image` ×2 (1a); `bytedance/seedream/v5/pro/text-to-image` ×2 (1a); `fal-ai/recraft/v4 (text-to-image)` ×2 (1a) |
| IMG-TEXT-02 | C_composite_textless_base | `fal-ai/flux-2-pro` ×2 (1a) |
| VID-TOPO3-01 | A_plate_9x16 | `alibaba/qwen-image-3` ×2 (1a) |
| VID-TOPO3-01 | C_plate_9x16 | `fal-ai/flux-2-pro` ×2 (1a) |
| VID-TOPO3-01 | A_cheap_still_to_cheap_i2v | `minimax/h3-max/image-to-video (768p)` ×2 (1b); `alibaba/wan-3.0-prime/image-to-video` ×2 (1b); `veo-3.1-lite-generate-001 (image input)` ×2 (1b) |
| VID-TOPO3-01 | B_premium_native_t2v | `veo-3.1-generate-001` ×2 (1a); `fal-ai/kling-video/v3/pro/text-to-video (silent)` ×2 (1a) |
| VID-TOPO3-01 | C_textless_plate_i2v_composite | `minimax/h3-max/image-to-video (768p)` ×2 (1b) |

Every TOPO-03 arm runs at 9:16: arms A and C use 9:16 plates drawn under VID-TOPO3-01 (Qwen Image 3 with text; FLUX.2 Pro textless), arm B draws natively at 9:16 (Auditor AF-1). Arm C's overlay is code at USD 0.

## 6. Media Factory freshness items → cases

| prior item | cases |
|---|---|
| 1 Veo policy behaviour on the emotional stylised child scene | VID-I2V-04, VID-T2V-03 (and IMG-CORE-04 as the still) |
| 2 Seedance 2.x cost/quality position | every Seedance 2.5 line: VID-T2V-01/02, VID-I2V-02/03, VID-REF-01/02, VID-MS-01 |
| 3 in-scene text through motion (composite-always for video) | VID-TOPO3-01 |
| 4 multi-turn dialogue and voice consistency | VID-2SPK-01 |
| 5 LatentSync-class mouth repaint vs native lip-sync | AUD-LIP-01/02/03 — tested with sync-lipsync v3 and Kling lipsync audio-to-video as the LatentSync-class substitutes (`fal-ai/latentsync` exists but is unpinned); the VID-2SPK-01 chain arm is recorded, not screened |

## 7. `requested_operation` coverage

| operation | cases | note |
|---|---|---|
| generate | IMG-CORE-*, IMG-TEXT-*, IMG-REF-*, VID-T2V-*, VID-2SPK-01, VID-KNEE-01, VID-TOPO3-01, VID-REF-*, VID-MS-*, AUD-TTS-*, MUS-* | |
| edit | IMG-EDIT-01, IMG-EDIT-02 | |
| animate | VID-I2V-01..04 | |
| extend | IMG-EXT-01 | |
| compose | IMG-COMP-01, AUD-LIP-01..03 | |
| restore | — | **omitted with reason:** no restore route in the plan §C.3 slate (RX-04's 1961 photograph shape has no screened route) |
| variants | — | **omitted with reason:** variant-set acceptance is outcome-level (COND-SCALE note) → Stage C; RX-09's Tamil/Bengali scripts have no benchmark-grade instrument |

## 8. Language mix (counts by lane)

| lane | en | hi | hg | total |
|---|---|---|---|---|
| IMG | 5 | 4 | 3 | 12 |
| VID | 7 | 5 | 3 | 15 |
| AUD | 2 | 2 | 2 | 6 |
| MUS | 1 | 1 | 0 | 2 |
| **all** | 15 | 12 | 8 | 35 |

Hindi + Hinglish = 20/35 = 57 % (target ≥ 40 %).

## 9. Benchmark vocabulary

No `customer_request.text` contains `probe`, `capability`, `benchmark`, `isolated`, `level 1` or `condition` (checked by grep in the Executor's self-check; the Tester re-runs it).
