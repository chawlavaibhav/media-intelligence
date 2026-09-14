# ROUTE-ANALYSIS — Upwork intro film (~60 s, 16:9, 1080p, fully AI-made)

**Role:** production-capability analyst. **Date:** 14 Sep 2026. **Spend by this analysis:** USD 0 (free reads only: fal
balance, Gemini model list, Sarvam key probe with an empty body, ElevenLabs subscription, local fonts/ffmpeg). **Repo
state read:** `main` = `fcc99ce` (PR #97 Governor refresh after #95/#96). **Recipes:** `preprod/recipes/` (8 files,
none has made a paid call; the two USD-0 tools were exercised on synthetic media).

## 0. Read this first

1. **Nothing in this film is authorised to spend yet.** `coordination/CONTROL-STATE.md` §6 and §8: every paid dispatch
   needs a signed record in writing before the first call; the 14-Sep rulings authorise none. The recipes refuse to send
   without `--confirm-spend --ledger`. This document prices; it does not authorise.
2. **This film sits outside Alpha 1 by ruling.** C-7 excludes "talking heads; lip-sync; native speech; multi-shot
   stories" from the product family (`runtime/ALPHA-1.md`). That is a product-scope ruling, not a capability verdict;
   the Lab's evidence for native speech and multi-shot exists and is used below. The film is a one-off pilot, priced as
   such.
3. **Brief-consistency flag for the Creative Director (not a routing decision):** `preprod/COMMERCIAL-BRIEF.md` line 70
   quotes the live profile: "Not on the menu: on-camera presenters, lip-synced people, the same character across several
   clips, and 30-60 second commercials", and line 178/187 describe the film as "no presenter, no lip-synced person, no
   recurring character; the voice is Indian English" versus "two short pieces of Vaibhav to camera; his real voice over the
   rest". A fully AI presenter (U1) would demonstrate on the profile the exact thing the profile says is not on the menu.
   Routing below covers U1 fully, and also gives a U1-alt (silent presenter b-roll + voice-over) that needs no untested
   capability and matches the "no lip-synced person" reading.
4. **Delivery target confirmed from the commercial brief** (lines 238-247): Upwork's player is 16:9 landscape; one 2026
   source says direct upload "under 200 MB, MP4, less than 60 seconds"; older guidance is a YouTube link. Plan a 16:9
   1080p24 H.264 master **under 60.0 s** (aim 57-59 s), AAC 48 kHz, plus a YouTube-ready copy of the same file.

### Evidence labels used below (every number carries one)

| Label | Meaning | Where it comes from |
|---|---|---|
| **CLEAN** | `clean_observed` cell in `eval/capability-map/TAINT-REGISTER-v1.yaml`: the frozen rule reproduces the number from sealed files, ≥ 4 settled draws, one human judge. Honest evidence, never a statistic or a clearance. `prod=True` means the runtime's policy would auto-route it; `manual_only` / `False` as stated | routing map cells + taint register (both regenerated 14 Sep under C-3/C-4/C-6b/C-6c/C-6d) |
| **DIRECTIONAL** | `directional_only`: reproduces, but < 4 settled draws (2/2 "may simply be a coin that landed twice") | same |
| **ELIMINATED** | frozen rule E1/E2 applied literally; `production_use_allowed: false`; `replacement_needed` where the failures were infrastructure (C-15, not authorised) | same |
| **REGISTRY (deterministic)** | one of the 575 `eval/registry/registry-v1.jsonl` rows: format, latency p50/p95, cost per settled trial. Reference calculations, `independence NOT ESTABLISHED` | `python3 eval/registry/validate_registry.py` PASS |
| **PINNED** | a price or request field present verbatim in fetched bytes under `eval/empirical-planning/price-pins-2026-09/` (81 pins, `verify_price_pins.py`: 81 verified, 0 failed, 2 warnings) or a pinned OpenAPI under `eval/harness-v2/schemas/` | pins |
| **UNTESTED** | the field/route/surface exists in pinned bytes but the Lab never dispatched it. Priced from pins, acceptance unknown | this document |
| **HISTORICAL-PRIOR** | Media Factory Jul-Aug 2026 observations (`eval/historical-priors/media-factory-v1/`) — **none is relied on below** | — |

Nothing below is Registry evidence about quality: the Registry never holds a human verdict (`CONTROL-STATE.md` §5).

---

## 1. Access reality check (free calls, 14 Sep 2026, this Mac)

| Surface | Check made | Result | Dispatchable now? |
|---|---|---|---|
| **fal** (cash) | `GET https://rest.alpha.fal.ai/billing/user_balance` with `Authorization: Key` | HTTP 200 → **USD 3.3515175** remaining. (The Lab spent USD 77.52 cash on fal 8-10 Sep; the balance ran out twice on 9 Sep — `DAY-2-SUMMARY` and `aud-lip/RESULTS.yaml`: "User is locked. Reason: Exhausted balance.") | **Yes, but only ~3 clips of Kling silent 6 s.** Any fal-heavy plan needs a top-up first; a fal balance lock mid-run counts as a failure under C-3. |
| **Gemini Developer API** (GCP credits via `GOOGLE_API_KEY`) | `GET /v1beta/models` | HTTP 200, 56 models, incl. `gemini-omni-1.1-flash`, `gemini-3.1-flash-image` (Nano Banana 2), `gemini-3-pro-image`, `veo-3.1-fast-generate-preview`, `veo-3.1-generate-preview`, `veo-3.1-lite-generate-preview`, `lyria-3.5`, `lyria-3-clip-preview`, `gemini-3.1-flash-tts-preview` | **Yes** for stills (surface live-proven by EVAL-038 for image generation). **Omni video on this surface has never carried a paid call** (C-13 "Gemini API smoke", ~USD 1, not authorised; `PIN-INDEX.yaml` header CAUTION). Veo/Lyria via this key: models listed, no harness adapter, UNTESTED. |
| **Vertex AI** (GCP credits, project `vertexaiproject-507518`) | SA file `~/.aight-litellm-keys/vertex-sa.json` present (`aight-gateway-sa@vertexaiproject-507518`, mode 0600). `~/.mi-battery-keys/` does **not** exist. Token exchange **not re-run today** (the session's permission classifier blocked activating the SA); last proven live 9-10 Sep 2026 by USD 41.55 of Vertex credits spend across Veo / Omni / Lyria / Nano Banana runs | Default `gcloud` account is `vaibhav@wherehouse.io` / project `supe-ask-staging` — the harness never touches it (throw-away `CLOUDSDK_CONFIG`; recipe `_common.gcloud_sa_token`). **GCP credit balance: unknown** (MD-1; no billing read exists). | **Yes** (Veo 3.1 fast/full/lite, Omni preview, Lyria 2, Nano Banana on Vertex), pending a token exchange that worked five days ago. |
| **Sarvam** (INR) | `POST /text-to-speech` with body `{}` | HTTP 400 `invalid_request_error` "Either 'text' or 'inputs' must be provided" — the key was accepted, nothing generated (a bad key returns 401/403) | **Yes**. Lab spend so far ₹0.894. |
| **ElevenLabs** (plan credits) | `GET /v1/user/subscription`, `GET /v1/voices` | tier **free**, 0 of 10,000 characters used this cycle (resets 2026-10-10 00:24 UTC); 21 premade voices, accents american/british/australian, **no Indian voice**; Eleven Music is paid-plan only (HTTP 402 on 9 Sep) | **Yes for TTS** (10k chars ≈ 1,600 words). Accent gap unchanged since RR-12. |
| **Local** | `which`, `fc-query`, `ffmpeg -filters` | ffmpeg 8.1.2 with libx264/aac/xfade/acrossfade/loudnorm/overlay/drawbox, **no drawtext, no libass**; hb-view/hb-shape 14.2.1; gcloud; python3 3.14 **without** `requests`/`PIL` (PIL only under `/usr/bin/python3` 3.9.6); Kohinoor Devanagari (5 faces), Helvetica Neue (14 faces), Avenir/Avenir Next, Gill Sans, Futura, Mukta Mahee, ITF Devanagari, Devanagari Sangam MN, Shree 714, `~/Library/Fonts/D-DIN.ttf` | **Yes** — all USD-0 units (U4, U9, U10) can run today. |

**Pools, in the Lab's vocabulary:** `credits` (Vertex + Gemini API; balance unknown), `cash` (fal; USD 3.35),
`sarvam_credits` (INR), `elevenlabs_credits` (10,000 chars/month). The Controller's standing preference is credits
first, fal last (`CONTROLLER-FAL-LAST-CHOICE-CREDITS-FIRST-2026-09-09`).

**FX convention:** the repo prices INR at the display-only rate **95.4211 INR/USD** (`COST-TABLE.rules`,
`eval/harness-v2/pricing.py`), not ₹90. INR 3,000 = **USD 31.44** at the repo rate (USD 33.33 at ₹90). This document
uses 95.4211; provider invoices stay in source currency.

---

## 2. What each route actually delivers (measured on the Lab's sealed clips, `ffprobe`, read-only)

| Route | Frame | fps | Audio | Duration behaviour | Native 16:9 1080p? |
|---|---|---|---|---|---|
| Kling v3 Pro (t2v, i2v) | **1080p** (1080×1920 at 9:16; i2v follows the plate, e.g. 1292×1604 for 4:5) | 24 | AAC 44.1 k when `generate_audio` | exact (+0.04 s) | **Yes** (no resolution parameter; 1080p is what it ships) |
| Veo 3.1 fast / full | 720p (1280×720 at 16:9); **1080p available** at USD 0.12/s fast (pinned) | 24 | AAC 48 k when `generateAudio` | exact | Yes at 1080p price |
| Gemini Omni 1.1 Flash | 720p default; 360p/720p/1080p/4k in the schema | 24 | AAC 48 k, native | exact | 1080p exists but **its token rate is not pinned** — price unknown; use 720p + lanczos upscale, or accept unpinned |
| Wan 3.0 Prime | 720p (pinned 0.14/s); 1080p at 0.28/s | **30** | AAC 44.1 k when `audio` | +0.03 s | Yes at double price |
| MiniMax H3 Max | 768p (768×1344 at 9:16) | 24 | has an AAC track (ambient) | **over-delivers**: 6.59 s for a 6 s ask | No — upscale 1.4× |
| Lyria 2 | — | — | WAV 48 k stereo | **32.768 s** per track | — |
| Sarvam bulbul:v3 | — | — | WAV **22.05 k mono** | as spoken | resample to 48 k |

Everything is conformed to 1920×1080 / 24 fps / 48 kHz before the cut (`recipes/assemble.sh conform`). Mixed 30-fps Wan
clips are frame-rate converted, which slightly softens motion; prefer Kling/Veo/Omni for shots with fast movement.

---

## 3. Unit-by-unit routing

Prices are USD per clip at the pinned per-second rate (table in §5). Latency = Registry p50 / p95 over the Lab's trials
(`latency_errors_refusals` rows). "Cell" names are `question/route` in `ROUTING-EVIDENCE-MAP-v0.yaml`.

### U1 — Speaking presenter to camera, native audio, 6-8 s takes, 2-4 takes, ONE identity

**Must accomplish:** the same person, same clothes, same room and light, speaking scripted Indian-English lines with
lips that match, across 2-4 separate clips, no lettering anywhere in frame, 16:9.

**What the Lab proved and did not prove (read the reject notes, not the headlines):**

| Fact | Evidence | Label |
|---|---|---|
| Native two-speaker Hindi dialogue, right lips on the right line, 8 s: Veo 3.1 fast 2/2, Gemini Omni 1.1 Flash 2/2, Wan 3.0 Prime 2/2 ("all 6 approved"); Kling v3 Pro audio 0/2 ("characters cut off, language bad", "language off") | RR-14; `vid-2spk/RESULTS.yaml`; cells `VID-2SPK/*` | DIRECTIONAL (2 draws each, `manual_only`); Kling ELIMINATED E1+E2, `replacement_needed` |
| Kling's audio is documented as English/Chinese only: "Supports Chinese and English voice output. Other languages are automatically translated to English. For English speech, use lowercase letters; for acronyms or proper nouns, use uppercase" | pinned OpenAPI `schemas/fal/fal-ai_kling-video_v3_pro_image-to-video.json` `generate_audio.description` | PINNED — explains the Hindi failure; **English speech on Kling is UNTESTED, not refuted** |
| Plate + lipsync chain: Kling lipsync a2v 0/5 "looking very odd" (+1 refusal on balance) | RR-14 note; `aud-lip/RESULTS.yaml`; cell `AUD-LIP/kling-lipsync-a2v+chain` | CLEAN, ELIMINATED E2 — **do not route through lipsync** |
| Image-to-video from an accepted still, silent: Kling v3 Pro 8/8, Wan 3.0 Prime 8/8, H3 Max 7/8, Veo 3.1 fast 5/8. Notes on the man-with-phone still (VID-I2V-02): "expression change to angry" on Kling ×2, Wan ×1, H3 ×1 (accepted under contract); Veo 0/2 "zooms in" | RR-8; `vid-i2v/RESULTS.yaml`; cells `VID-I2V/*` | CLEAN (`prod=True` on all four) — **every one of the 32 i2v draws was sent with audio OFF** (`generateAudio:false`, `generate_audio:false` in the sealed `.request.json`). i2v **with** speech is UNTESTED on every route |
| Reference-to-video, person: Veo 3.1 fast ref2v 0/2 — both notes read "some different language (lettering appeared; contract: no lettering, signage or logos)". The run's own reading: "Reference fidelity of the person was not the failure the Controller named; text hygiene was" | RR-11; `vid-ref/RESULTS.yaml` `reading[1]`; cell `VID-REF/veo-3.1-fast-ref2v+native` 2/4 | CLEAN as a 4-draw cell (`prod=True` on the question); the **person** item is 0/2 on lettering, identity was not judged as failed. Sent with `generateAudio:true`, 3 asset references, 8 s (6 s refused on Vertex) |
| Veo extend chain (8 s + fixed 7 s = 15 s, one continuous clip): 2/2, one "a little visually bad but technically correct" | RR-9; `vid-ms/RESULTS.yaml`; cell `VID-MS/veo-3.1-fast-extend+chain` | DIRECTIONAL |
| Kling v3 Pro 15 s single clip 2/2 clean (silent); 10 s 2/2 "visually not amazing" | RR-9; cells `VID-MS/kling-v3-pro-15s`, `-10s` | DIRECTIONAL |
| Kling i2v `elements` field: "Elements (characters/objects) to include in the video. Each example can either be an image set (frontal + reference images) or a video. Reference in prompt as @Element1" — present in the pinned i2v schema; the separate `kling-v3-elements` endpoint 404s and is unpinned | `schemas/fal/fal-ai_kling-video_v3_pro_image-to-video.json` `KlingV3ComboElementInput`; roster `kling-v3-elements: unpinned` | PINNED field, UNTESTED |
| Veo's recurring weakness is text hygiene, not identity: fabricated Devanagari (piece 1), stray script in the cafe (ref2v), "hand appeared" (i2v) | `DAY-2-SUMMARY` §"What the day says" 3 | DIRECTIONAL synthesis |

**The four options, evaluated:**

| Option | Mechanism for identity | Speech | Evidence for the pieces | What is UNTESTED | Cost per 8 s take (1080p where possible) |
|---|---|---|---|---|---|
| **(a) One accepted portrait still → i2v WITH native audio, same still for every take** | Frame 0 of every take is the same pixels: face, clothes, room, light fixed by construction. Drift can only happen within a take (8 s). | Veo 3.1 fast: `generateAudio:true` on the i2v instance (params pinned: `VideoGenerationModelParams.generateAudio`). Kling v3 Pro i2v: `generate_audio:true` (English documented). Omni: `image_to_video` task with the same Interactions body (adapter supports `image_bytes`). Wan 3.0 Prime i2v: `audio:true` | i2v silent CLEAN 5/8-8/8; native speech DIRECTIONAL 2/2 on Veo/Omni/Wan; Kling English speech nothing | **i2v + speech together on any route**; Kling English speech; Omni i2v at all | Veo fast 1080p **0.96**; Kling audio **1.34**; Omni 720p **0.81**; Wan 720p **1.12** |
| (b) Veo extend chain from take 1 | Continuous clip, so identity is continuous by construction (8 + 7 s = one 15 s take covering two lines) | `generateAudio` on both calls; speech across the join is the risk (audio continuity at the extend boundary) | 2/2 DIRECTIONAL, quality note "a little visually bad" | speech across an extend boundary | 15 s ≈ **1.50** at 720p (RR-9 recorded USD 2.00 in the ledger for the item) |
| (c) One long Kling 15 s take with audio, covering all the speech | One clip = one identity, no cross-take problem at all | English documented; **Hindi failed 0/2** | 15 s silent 2/2 clean DIRECTIONAL | English speech on Kling; a 15 s monologue's lip sync | **2.52** (0.168 × 15), 1080p native |
| (d) Reference-image conditioning: Veo ref2v with 3 stills of the presenter, `generateAudio:true` | Model keeps the referenced face across takes; no shared first frame | already sent with audio on in the Lab (silent brief) | 0/2 on the person item **for lettering**, 2/2 on the product item; identity not the named failure | identity **across** takes (never measured); speech from a reference | **0.80** at 720p (8 s only on Vertex) |

**Recommendation for U1 (in this order):**

1. **Primary: (a) on Veo 3.1 fast, Vertex, 16:9, 1080p, 8 s, `generateAudio:true`, from ONE accepted Nano Banana 2
   portrait still.** Reasons: identity anchoring by shared first frame is the only mechanism whose two halves are both
   observed (i2v CLEAN; Veo native speech DIRECTIONAL 2/2 with correct lip assignment); it is on credits, not fal cash;
   1080p is pinned at 0.12/s; latency p50 41-56 s. Prompt discipline from the Lab: static camera, "no text, captions,
   subtitles, logos or lettering anywhere in any frame", spoken line in quotes, "lips matching the words", Indian-English
   accent named. Known failure modes to plan for: Veo i2v 0/2 on one still for "zooms in" (write "camera completely
   static" and accept a slow push-in at judging), "hand appeared", stray lettering (post-check every frame by eye; the
   Cloud Vision detector is wired in the gate but invoking it is not authorised); expression drift late in the take
   (seen on 3 routes) — keep takes at 6 s where the line allows.
2. **Fallback A: (a) on Kling v3 Pro i2v, `generate_audio:true`, English lowercase per the schema note, same still.**
   1080p native, i2v 8/8 CLEAN, but English speech untested and the route is on fal cash (balance USD 3.35 ≈ two 8 s audio
   takes). Latency p50 ~95-105 s, p95 344 s.
3. **Fallback B: (a) on Gemini Omni 1.1 Flash `image_to_video`, Vertex surface, 720p** (t2v 8/8 CLEAN, 2-speaker 2/2;
   i2v untested; latency ~30-45 s; cheapest at 0.81).
4. **Do not** route through lipsync (0/5) or Wan 2.2 (silent family). Use (b) only if a single 15 s continuous take is
   creatively wanted; use (d) only as an experiment after (a) is proven — it adds the lettering risk (0/2) without
   removing any.
5. **Pre-flight smoke, before the shot list is locked (USD ≈ 3.1):** one 8 s take on each of Veo-i2v-audio, Kling-i2v-audio
   and Omni-i2v from the same still, judged by the Creative Director for lip sync, accent, identity hold and lettering.
   This is the single most important unknown in the film; everything else in it rests on CLEAN or DIRECTIONAL evidence.

**U1-alt (no untested capability):** silent presenter b-roll by i2v from the same still on Kling v3 Pro (CLEAN 8/8) with
the presenter *not* speaking on camera (listening, nodding, working), and the lines carried as voice-over (U7: Sarvam
bulbul:v3 6/6, or Vaibhav's own recorded voice). Zero lip-sync risk, and it matches the brief's own "no lip-synced person"
wording. Cost per 6 s clip 0.67 (fal) or Veo fast silent 0.72 at 1080p (credits).

### U2 — Presenter b-roll without speech (same identity), optional

Same still → Kling v3 Pro i2v silent (**CLEAN 8/8**, `prod=True`, 1080p, 0.112/s) or Wan 3.0 Prime i2v (**CLEAN 8/8**,
720p/30 fps, 0.14/s); H3 Max cheapest (7/8, one "label appeared out of thin air"); Veo fast i2v 5/8 (avoid where the
camera must not move — RR-8). fal: `start_image_url` (data URI), `duration "6"`, `generate_audio:false`. Failure modes:
expression drift to "angry" late in the clip (3 routes, one still); an invented object/label (H3 Max, Veo). Cost 6 s:
0.67 / 0.84 / 0.48 / 0.72 (Veo 1080p).

### U3 — Product/ad b-roll: an ad "building itself" (textless plate → i2v → exact text by code per frame)

**Must accomplish:** a clean, textless commercial plate in motion (product, light, hands, surface), onto which the
exact offer/price/brand strings are composed by code on every frame, English and Devanagari.

| Step | Route | Evidence | Label | Price |
|---|---|---|---|---|
| Plate | **FLUX.2 Pro** textless plate (fal `fal-ai/flux-2-pro`, `image_size {1280,720}` keeps the first-megapixel price) | RR-1: 4/4 accepted as plates for code overlay (cell `IMG-TEXT/flux-2-pro+code_overlay`); the same plates judged bare 1/4 (eliminated) — the *plate* passed, the model's *text* did not | CLEAN (`prod=True`) | 0.03 |
| Plate alt | **Nano Banana 2** (Gemini API `gemini-3.1-flash-image`, `imageConfig.aspectRatio "16:9"`) | IMG-CORE 7/8 CLEAN; as a *text* plate 1/2 DIRECTIONAL ("two shri") — irrelevant when the plate is textless | CLEAN / DIRECTIONAL | 0.067 |
| Animate | **Kling v3 Pro i2v** (1080p) or **Wan 3.0 Prime i2v**; **H3 Max i2v** cheapest | RR-8 8/8, 8/8, 7/8 CLEAN; RR-6/RR-7: H3 Max carried both a wrong plate faithfully (0/4) and a right plate faithfully (2/2 + 2/2) — "the animators preserved the lettering", so they will also preserve a textless plate | CLEAN | 6 s: 0.67 / 0.84 / 0.48 |
| Text | **code**, per frame, after the fact (`recipes/overlay_text_video.py`; Lab tool `eval/harness-v2/composite.py --video`) | RR-6 arm C 2/2 (cell `VID-TOPO3/minimax-h3-max-i2v+C_textless_plate_i2v_composite`), RR-1 4/4; exact by construction | DIRECTIONAL in motion, CLEAN on stills; mechanism B (deterministic composition) | 0 |

**Never** ask the video model to draw the text: arm B native text on Veo 3.1 full 0/2 and Kling v3 Pro 0/2 ("different
text altogether"), both ELIMINATED (RR-6). For "building itself", generate the plate with the product on a planned
negative-space region (wall, sky, marble, per `adwisely-order-mode/docs/2026-09-14-ad-design-direction.md` §3 Archetype B)
so the animated text has room; keep the camera static or a slow drift so a static overlay stays registered (the Lab's
overlay is static; `overlay_text_video.py animate` adds fades/slides of the text itself, not tracking).

### U4 — Text-in-motion: exact English + Devanagari offer text animating (code-drawn)

Fully USD 0 and deterministic. Fonts on this Mac (verified `fc-query`): `/System/Library/Fonts/Kohinoor.ttc` faces 0
Regular / 1 Medium / 2 Semibold / **3 Bold** (the Lab's arm C face) / 4 Light; `/System/Library/Fonts/HelveticaNeue.ttc`
faces 0 Regular / 1 Bold / 2 Italic / 4 Condensed Bold / 5 UltraLight / 7 Light / 9 Condensed Black / 10 Medium / 12 Thin;
also Avenir, Avenir Next, Gill Sans, Futura, Mukta Mahee, ITF Devanagari, Devanagari Sangam MN, Shree Devanagari 714,
`~/Library/Fonts/D-DIN.ttf`. Renderer: hb-view with font FILE + face INDEX + `--unicodes` (the exactness battery's
renderer; no fontconfig fallback possible). Motion: ffmpeg `overlay` with `fade`/`enable`/expression positions
(`recipes/overlay_text_video.py animate`, tested on a synthetic 1080p clip 14 Sep: Devanagari shaped correctly, panel +
fade + slide-up rendered). Limits: this ffmpeg has **no drawtext/libass**, so all text is PNG layers; tracking text to a
moving object is not provided (static camera plates only). Failure mode: none generative; the only risk is a typo in the
copy deck — proof the strings with `hb-shape` for a dotted-circle glyph (malformed cluster) before rendering.

### U5 — Multi-shot product story, 10-15 s

| Route | Evidence | Label | Price | Latency |
|---|---|---|---|---|
| **Gemini Omni 1.1 Flash 10 s** (Vertex, 720p, `duration "10s"`) | RR-9: 2/2 "clean" three-shot story | DIRECTIONAL (`manual_only`) | **1.01** | p50 33 s |
| **Kling v3 Pro 15 s** (fal, `duration "15"`, `generate_audio:false`, optional `multi_prompt` with per-shot durations) | RR-9: 2/2 clean; 1080p native | DIRECTIONAL (`manual_only`) | **1.68** (silent) / 2.52 (audio) | p50 203 s |
| Kling v3 Pro 10 s | 2/2 "technically correct but visually not amazing" | DIRECTIONAL | 1.12 | p50 136 s |
| Veo 3.1 fast extend (8 + 7) | 2/2, one "a little visually bad" | DIRECTIONAL | 1.50 (ledger 2.00) | p50 151 s |
| Seedance 2.5 | not run ("not needed on this evidence") | UNTESTED | 4.73-7.09 | — |

Recommendation: **Omni 10 s on credits** as primary (cheapest, cleanest, fastest, native ambience); **Kling 15 s** where
the story needs 15 s or 1080p without upscale. Omni is capped at 10 s (the 15 s row was refused by the planner). Multi-shot
clips are the place native ambience helps; keep the film's spoken lines off these clips.

### U6 — "Impossible"/ambitious world shots (text-to-video)

| Route | Evidence (RR-15, 4 briefs × 2) | Label | Price 6 s / 8 s | Latency |
|---|---|---|---|---|
| **Gemini Omni 1.1 Flash** (Vertex, 720p) | **8/8**; plus VID-MS 2/2 and VID-2SPK 2/2 = 12/12 across questions | CLEAN (`prod=True`) | 0.61 / 0.81 | p50 28-44 s |
| MiniMax H3 Max 768p (fal) | 5/8 incl. one fal-403 balance refusal counted; 0/2 on the bottle brief | CLEAN (`prod=True`) | 0.48 / 0.64 | p50 < 10 s |
| Wan 2.2 A14B (fal, silent, 16 fps) | 4/6 | CLEAN (`prod=True`) | 0.48 / 0.64 | p50 60-90 s |
| Veo 3.1 fast (Vertex) | 4/8; 0/2 umbrella "rain doesn't appear, looks fake" | CLEAN (`prod=True`) | 0.60 / 0.80 (720p); 0.72 / 0.96 (1080p) | p50 47-68 s |
| Wan 3.0 Prime (fal) | 4/8 incl. one 403 | CLEAN (`prod=True`) | 0.84 / 1.12 | p50 72-117 s |
| Kling v3 Pro audio (fal) | 2/8 | ELIMINATED E2 (`replacement_needed`) | — | — |
| Veo 3.1 full (product hero with physical detail, RR-10) | 1/2; cheap tier 0/4 | DIRECTIONAL | 2.40 / 3.20 | p50 47-53 s |

Recommendation: **Omni on GCP credits (RR-15 default)**; H3 Max as the cash fallback for everyday shots (not for product
detail: RR-10). Refusal/failure modes: Veo `raiMediaFilteredCount` safety filtering (adapter classifies as refusal); Omni
"Prompts that violate usage policies are blocked" (no block shape documented); fal HTTP 403 on exhausted balance (counted
as a failure under C-3); Wan 2.2 i2v HTTP 422 when `aspect_ratio` is left at `auto` (send the aspect explicitly — the
recipe does). Where a shot names physical detail (condensation, rain, slow motion, blank label), plan 2 draws or go
premium (RR-10: Veo full 1/2).

### U7 — Voice-over lines

| Route | Evidence | Label | Price | Notes |
|---|---|---|---|---|
| **Sarvam bulbul:v3**, `language_code en-IN`, speaker `aditya` | RR-12: 6/6 (Hindi, Hinglish, English scripts) | CLEAN (`prod=True`) | ₹3.00 / 1,000 chars → **100 words ≈ 600 chars ≈ ₹1.80 ≈ USD 0.019**; the film's 108 words ≈ ₹2 | WAV 22.05 k mono; ≤ 2,500 chars per call; latency 1-2 s; other speakers pinned in `SPEAKERS-PIN.yaml` |
| ElevenLabs `eleven_v3` direct, premade voice | RR-12: Hindi 2/2, English 2/2, **Hinglish 0/2 "rejected for accent"** | CLEAN (`prod=True`) | 0 cash; 1 plan credit/char; free tier 10,000/month, 0 used | no Indian voice on the account (checked today); ~2-3 s latency |
| ElevenLabs via fal | — | UNTESTED | USD 0.10 / 1,000 chars | cash |
| Gemini TTS (`gemini-3.1-flash-tts-preview`) | listed on the key | UNTESTED | on the pinned Gemini pricing page | no adapter |

Recommendation: Sarvam for Indian-English VO (default per RR-12). ElevenLabs only if the Creative Director wants a
non-Indian narrator voice. The brief's "his real voice" option costs nothing and removes the accent question entirely.

### U8 — Music bed, 60 s

**Lyria 2 (`lyria-002`, Vertex us-central1):** RR-13 4/4 accepted, judged raw and stacked under the accepted clips —
cell `MUS/lyria+native`, **CLEAN** (`clean_observed`, `prod=True`, 4 settled draws; it is one of the three audio cells the
runtime's router leaves out only because it cannot price them by duration). **USD 0.06 per track**, each **32.768 s**
WAV 48 k stereo, p50 28-30 s. `seed` cannot be combined with `sample_count`, so two calls are two different
pieces. To reach 60 s:

1. **Loop one accepted track with a 4 s `acrossfade`** (32.8 + 32.8 − 4 = 61.6 s; same key and tempo by construction) —
   `assemble.sh music60_loop`. Try first; audition the seam.
2. **Two generations, A then B, joined at a scene change** with a 3 s crossfade — `music60_two`. Different pieces; needs a
   listening pass.
3. Generate a spare (USD 0.06) so the edit has a choice; the whole music line is ≤ USD 0.18.

Alternatives: Lyria 3.5 on the Gemini API (`lyria-3.5`, "$0.08 per song", full songs — listed on the key, pinned price
page, **no adapter, UNTESTED**); ElevenLabs Music direct is paid-plan only (HTTP 402); fal ElevenLabs Music USD 0.60 per
output minute (UNTESTED, cash). Failure modes: vocals or a build the brief did not ask for (write "instrumental, no
vocals" and use `negative_prompt`), tempo mismatch with the cut (pick the track first, then cut to it).

### U9 — Exact-text end card / title cards / lower thirds (code)

USD 0. Same renderer and fonts as U4; still frames via hb-view PNG layers over a solid `color` or the accepted still
(`assemble.sh end_card`, `overlay_text_video.py static`). The separate composer `adwisely-order-mode/ordermode/`
(`layout.py`, `textrender.py`, `compose.py`) renders the same two font files (`fonts.py`: Helvetica Neue faces 0/1,
Kohinoor faces 1/3), wraps and fits blocks, measures legibility and draws **a translucent scrim panel** — and its own
design direction (§4) says that scrim must be replaced by a solid panel and that **pill, circle badge, button,
strikethrough, rule, product anchor and logo lockup primitives are missing** (§4 items 3-6). So today `ordermode` can set
exact copy in a column with a panel behind it; it cannot draw the offer pill, CTA button or struck price. A sibling agent
has since started `pilots/.../tools/adcomp.py` (Pillow-based "Ledge" archetype with pill/button/seam) — note it imports
PIL, which only `/usr/bin/python3` (3.9) has. For the film's cards: headline Helvetica Neue Bold (face 1) or Didot for a
serif, Devanagari Kohinoor Bold (face 3), legal Helvetica Neue Light (face 7); left-align inside a solid panel that
touches two frame edges; no floating scrim (design direction §3).

### U10 — Assembly

ffmpeg 8.1.2: conform (lanczos to 1920×1080, `fps=24`, 48 k stereo), trim, `concat` demuxer for straight cuts, `xfade` +
`acrossfade` for dissolves, PNG-layer text, music loop, mix with `sidechaincompress` ducking under speech, `loudnorm`
I=−14 LUFS TP=−1 (web/social), master libx264 High 4.1 crf 18 yuv420p `+faststart`. Captions: no libass, so either timed
PNG layers or a sidecar `.srt` muxed as `mov_text`. All functions in `recipes/assemble.sh` were exercised on synthetic
media (a 5.5 s master probed at 1920×1080 h264 / aac 48 k). Keep the master **under 60.0 s**.

---

## 4. Provider surfaces and exact request shapes (the ones this film would send)

| Unit | Surface | Endpoint | Body (pinned shape) | Auth |
|---|---|---|---|---|
| U1 primary | Vertex | `POST https://us-central1-aiplatform.googleapis.com/v1/projects/vertexaiproject-507518/locations/us-central1/publishers/google/models/veo-3.1-fast-generate-001:predictLongRunning` then `:fetchPredictOperation {"operationName"}` | `{"instances":[{"prompt":"...","image":{"bytesBase64Encoded":"...","mimeType":"image/png"}}],"parameters":{"sampleCount":1,"aspectRatio":"16:9","resolution":"1080p","durationSeconds":8,"generateAudio":true}}` — inline mp4 back | Bearer token from SA file via gcloud (throw-away config) |
| U1 fallback A / U2 / U3 / U5 | fal queue | `POST https://queue.fal.run/fal-ai/kling-video/v3/pro/image-to-video` → poll `status_url` (200/202) → `response_url` → `video.url` on `*.fal.media` | `{"prompt":"...","start_image_url":"data:image/png;base64,...","duration":"8","generate_audio":true|false}`; optional `elements:[{frontal_image_url, reference_image_urls[]}]` (UNTESTED); t2v adds `"aspect_ratio":"16:9"`, `duration` up to `"15"`, `multi_prompt` | `Authorization: Key <FAL_KEY>` |
| U1 fallback B / U5 / U6 | Vertex (proven) | `POST https://aiplatform.googleapis.com/v1beta1/projects/vertexaiproject-507518/locations/global/interactions` | `{"model":"gemini-omni-1.1-flash-preview","input":[{"type":"text","text":"..."},{"type":"image","data":"...","mime_type":"image/png"}],"response_format":[{"type":"video","aspect_ratio":"16:9","resolution":"720p","duration":"8s"}],"generation_config":{"video_config":{"task":"text_to_video"|"image_to_video"}}}` — synchronous, inline mp4 | Bearer (SA) |
| same, Gemini API (UNTESTED surface for video) | Gemini API | `POST https://generativelanguage.googleapis.com/v1beta/interactions` | same body with `"model":"gemini-omni-1.1-flash"` and `response_format` as a **dict**, not a list | `x-goog-api-key` header, never in the URL |
| U3 plate | fal | `POST https://queue.fal.run/fal-ai/flux-2-pro` | `{"prompt":"...","image_size":{"width":1280,"height":720}}` | Key |
| U1 still / U3 alt plate | Gemini API | `POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image:generateContent` | `{"contents":[{"role":"user","parts":[{"text":"..."},{"inlineData":{...}}?]}],"generationConfig":{"responseModalities":["IMAGE"],"candidateCount":1,"imageConfig":{"aspectRatio":"16:9"}}}` — 1K default | `x-goog-api-key` |
| U6 alt | fal | `POST https://queue.fal.run/minimax/h3-max/text-to-video` | `{"prompt","prompt_expansion_mode":"balanced","aspect_ratio":"16:9","resolution":"768P","duration":6}` | Key |
| U7 | Sarvam | `POST https://api.sarvam.ai/text-to-speech` | `{"text","language_code":"en-IN","speaker":"aditya","model":"bulbul:v3"}` → `audios[0]` base64 WAV | `api-subscription-key` |
| U8 | Vertex | `POST .../us-central1/publishers/google/models/lyria-002:predict` | `{"instances":[{"prompt":"...","negative_prompt":"..."}],"parameters":{"sample_count":1}}` → `predictions[0].bytesBase64Encoded` | Bearer (SA) |

Harness conventions carried into the recipes: key read by name at dispatch, never in a URL/log; one submit = one trial,
bounded poll (120 × 5 s), never resubmit; reservation line written to the ledger before the first byte leaves; downloads
only from fal hosts; `generateAudio`/`generate_audio` sent explicitly; `sampleCount`/`num_images` pinned to 1; `seed`
never sent. Sealing: the Lab writes `media/<trial>.<ext>` + `.request.json` (before dispatch) + `.record.json` +
`.attempt.json` + an append-only manifest (`eval/harness-v2/store.py`); the pilot should at least keep the request JSON,
the returned bytes and the ledger line per clip under `gen/`.

---

## 5. Cost table (pinned prices; USD; INR at 95.4211)

### 5.1 Video, per second and per clip

| Route (resolution priced) | USD/s | 6 s | 8 s | 10 s | 15 s | 8 s in ₹ | Pool | Duration limits |
|---|---|---|---|---|---|---|---|---|
| Veo 3.1 fast 720p | 0.10 | 0.60 | 0.80 | — | 1.50 (extend 8+7) | 76 | credits | 4 / 6 / 8 s; extend +7 |
| Veo 3.1 fast **1080p** | 0.12 | 0.72 | 0.96 | — | 1.80 (extend) | 92 | credits | same |
| Veo 3.1 full 720/1080p | 0.40 | 2.40 | 3.20 | — | 6.00 | 305 | credits | 4 / 6 / 8 |
| Veo 3.1 lite 720p (1080p 0.08) | 0.05 | 0.30 | 0.40 | — | — | 38 | credits | RR-10: failed physical detail 0/2 |
| Gemini Omni 1.1 Flash 720p | 0.10136 | 0.61 | 0.81 | 1.01 | — | 77 | credits | 3-10 s; 1080p rate **unpinned** |
| Kling v3 Pro silent (1080p native) | 0.112 | 0.67 | 0.90 | 1.12 | 1.68 | 85 | **cash** | 3-15 s |
| Kling v3 Pro audio on | 0.168 | 1.01 | 1.34 | 1.68 | 2.52 | 128 | cash | voice control 0.196 |
| Wan 3.0 Prime 720p (480p 0.068) | 0.14 | 0.84 | 1.12 | 1.40 | 2.10 | 107 | cash | 2-30 s |
| Wan 3.0 Prime 1080p | 0.28 | 1.68 | 2.24 | 2.80 | 4.20 | 214 | cash | |
| MiniMax H3 Max 768p (480p 0.05) | 0.08 | 0.48 | 0.64 | 0.80 | 1.20 | 61 | cash | 5-15 s; over-delivers ~0.6 s |
| Wan 2.2 A14B 720p silent | 0.08 | 0.48 | 0.64 | 0.80 | — | 61 | cash | ≤ 10 s (161 frames @16 fps) |
| Seedance 2.5 720p | 0.473 | 2.84 | 3.78 | 4.73 | 7.09 | 361 | cash | up to 30 s |
| Kling lipsync a2v (eliminated) | 0.014/input s, 5 s steps | 0.07 | 0.14 | — | — | — | cash | 0/5 |

### 5.2 Stills, speech, music

| Item | Price | Pool | Evidence |
|---|---|---|---|
| Nano Banana 2 (1K) | 0.067 (+0.0011 per input reference image) | credits (Gemini API) | IMG-CORE 7/8 CLEAN; IMG-TEXT 4/4 |
| Nano Banana Pro (1K/2K) | 0.134 | credits | IMG-CORE 4/8; IMG-TEXT 4/4 |
| FLUX.2 Pro (first MP) | 0.03 | cash | textless plate for code overlay 4/4 |
| Seedream 5 Pro / edit | 0.0675 | cash | edit/ref default (RR-4) 10/12 |
| GPT Image 2 (medium) | 0.053 | cash | IMG-CORE 6/8; IMG-TEXT 4/4 |
| Qwen Image 3 | 0.04 | cash | avoid for Devanagari (RR-3) |
| Sarvam bulbul:v3 | ₹3.00 / 1,000 chars → **100 words ≈ ₹1.80 ≈ USD 0.019** | INR | 6/6 |
| ElevenLabs v3 direct | 1 credit/char; free 10,000/month (0 used) | plan credits | 4/6 |
| ElevenLabs v3 on fal | USD 0.10 / 1,000 chars | cash | untested |
| Lyria 2 track (32.8 s) | **0.06** | credits | 4/4 |
| Lyria 3.5 (Gemini API, "per song") | 0.08 | credits | untested, no adapter |
| fal ElevenLabs Music | 0.60 / output minute (rounded up) | cash | untested |

### 5.3 Redraw rule of thumb, by unit type (from the Lab's accept counts; plan draws = 1 / observed accept rate, rounded up)

| Unit type | Observed | Planned draws per accepted clip | Note |
|---|---|---|---|
| Silent i2v from an accepted still (Kling / Wan 3.0 Prime) | 16/16 | **1.1** (one spare per 8 shots) | expression drift late in clip is the residual risk |
| Silent i2v on H3 Max / Veo fast | 7/8, 5/8 | 1.2 / 1.6 | Veo adds camera moves |
| Plain t2v on Omni | 8/8 (+4/4 elsewhere) | **1.1** | |
| Plain t2v on H3 Max / Veo fast / Wan 3.0 Prime | 5/8, 4/8, 4/8 | **2** | Wan 2.2 4/6 → 1.5 |
| Product hero with named physical detail | Veo full 1/2, cheap 0/4 | 2 on premium, or switch to plate + i2v + code | RR-10 |
| Multi-shot 10-15 s (Omni 10 s, Kling 15 s) | 2/2, 2/2 | 1.5 (small n) | |
| Native speech, two speakers (Veo / Omni / Wan) | 6/6 | 1.5 (small n) | Hindi; English untested |
| **Presenter i2v + speech (U1)** | **untested** | **2** until the smoke says otherwise | the film's one real unknown |
| Text by code (U4, U9, overlay in U3) | 4/4 + 2/2, deterministic | **1** | redraw only the plate, never the text |
| Textless plate (FLUX.2 Pro / NB2) | 4/4 as plates; NB2 core 7/8 | 1.25 | cheap: over-generate 2-3 plates and pick |
| Sarvam VO | 6/6 | 1 | regenerate per script change, ₹-scale |
| Lyria | 4/4 | 1.5 (taste, not failure) | 0.06 each |

### 5.4 A 12-shot film at first pass, plus one redraw on the two riskiest shots

Shot list shaped on the commercial brief's structure (brief arrives → presenter → ad builds → QA → tiles → presenter →
end card). Prices at §5.1/5.2; 1080p where pinned.

| Shot | Route | USD | Pool |
|---|---|---|---|
| S1 open: the brief arrives | Omni t2v 6 s (Vertex) | 0.610 | credits |
| S2 presenter take 1 | NB2 portrait still 16:9 | 0.067 | credits |
| S2 presenter take 1 | Veo 3.1 fast i2v + audio, 8 s, 1080p | 0.960 | credits |
| S3 the ad builds itself | FLUX.2 Pro textless plate | 0.030 | cash |
| S3 | Kling v3 Pro i2v 6 s silent (1080p) + text by code | 0.672 | cash |
| S4 text in motion (offer, EN + Devanagari) | FLUX.2 Pro plate | 0.030 | cash |
| S4 | H3 Max i2v 6 s + code text | 0.480 | cash |
| S5 QA moment (a stray character caught) | Omni t2v 6 s | 0.610 | credits |
| S6 product hero | NB2 still | 0.067 | credits |
| S6 | Kling v3 Pro i2v 6 s silent | 0.672 | cash |
| S7 three-shot story | Omni 10 s | 1.010 | credits |
| S8 four tiles flash | 3 × NB2 stills + code animation | 0.201 | credits |
| S9 presenter take 2 (same still) | Veo 3.1 fast i2v + audio, 8 s, 1080p | 0.960 | credits |
| S10 ambitious world shot | Omni t2v 8 s | 0.810 | credits |
| S11 b-roll | FLUX plate + Wan 3.0 Prime i2v 6 s | 0.870 | cash |
| S12 end card, lower thirds, captions | code | 0.000 | — |
| VO | Sarvam ≈ 650 chars (108 words) | 0.020 (₹1.95) | INR |
| Music | Lyria 2 ×2 (one used, one spare) | 0.120 | credits |
| **First pass** | | **8.19** (cash 2.75 / credits 5.42 / ₹1.95) | **₹781** |
| + one redraw on the two riskiest shots (S2, S9 presenter takes) | 2 × 0.96 | 1.92 | credits |
| **First pass + 2 redraws** | | **10.11** | **₹965** |
| + U1 pre-flight smoke (Veo-i2v-audio 0.96, Kling-i2v-audio 1.34, Omni-i2v 0.81) | | 3.11 | mixed |
| **Grand total incl. smoke** | | **13.22** | **₹1,262** |
| Hard cap | INR 3,000 | **31.44** | headroom ≈ USD 18 (≈ 30 % general redraw allowance on the rest is USD 1.9; the remainder covers a second identity attempt on Kling or a full route switch) |

Pool reality: the cash lines above (USD 2.75 + Kling smoke 1.34 = 4.09) **exceed today's fal balance of USD 3.35**;
either top up fal by ~USD 10 or move S3/S6 to Veo fast i2v silent 1080p (0.72 each, credits; 5/8 evidence instead of
8/8). Every credit line depends on an unknown GCP credit balance (MD-1).

---

## 6. Known failure modes and refusals, consolidated

| Where | What happened in the Lab | Mitigation in this film |
|---|---|---|
| fal balance | two exhaustions on 9 Sep; HTTP 403 "User is locked. Reason: Exhausted balance." counted as failures under C-3 | check `fal_queue.py balance` before each fal batch; top up before the presenter smoke |
| fal Wan 2.2 i2v | HTTP 422 "Use aspect_ratio='16:9', '9:16', or '1:1' instead of 'auto'" when the plate resolved to an odd size | always send `aspect_ratio` (recipes do; Wan 2.2 is not used here) |
| Veo (Vertex) | `raiMediaFilteredCount` safety filtering; ref2v accepts only 8 s; extend adds a fixed 7 s; i2v "zooms in", "hand appeared"; ref2v invented foreign lettering in a people scene twice; t2v missed weather physics ("rain doesn't appear") | static-camera wording; "no lettering" wording + eye check of every frame; people scenes only via i2v from a still, never ref2v, until proven |
| Kling v3 Pro audio | Hindi dialogue 0/2 ("language bad"); schema says English/Chinese only | English lowercase per the schema; smoke before use |
| Kling / Wan / H3 i2v | expression drift to "angry" on one still late in the clip | 6 s takes where possible; pick a neutral-smile still |
| H3 Max | invents a label/product ("label appeared out of thin air"); over-delivers duration; 768p | trim; upscale; not for product detail (RR-10) |
| Omni (Vertex) | none observed in 16 draws; clip cap 10 s; policy block shape undocumented | keep prompts commercial and lettering-free |
| Gemini API surface (video) | never carried a paid Omni call; prices pinned but "untested in execution" (audit F-9) | use Vertex for Omni unless the Controller wants the C-13 smoke folded in |
| Lyria | returns `bytesBase64Encoded` (page says `audioContent`); 32.8 s not 30 | recipe accepts both keys; loop/crossfade plan |
| ElevenLabs | Hinglish accent 0/2; music 402 on free plan; no Indian voice | Sarvam default |
| Lipsync chain | 0/5 "looking very odd" | not used |
| Text in video by the model | 0/4 across Veo full and Kling ("different text altogether"), 0/4 from a misspelled cheap plate | code overlay only; textless plates only |
| Vision judge | 66 % agreement, 22 % false-accept — not qualified | every clip judged by a person (C-8 spirit) |

---

## 7. Recommendations, in one screen

1. **Lock the presenter mechanism first** with the USD ≈ 3.1 smoke (one 8 s take each on Veo-i2v-audio 1080p, Kling-i2v-audio,
   Omni-i2v, all from one NB2 portrait still). If none holds identity + lips + no lettering, switch the film to **U1-alt**
   (silent presenter b-roll on Kling i2v, CLEAN 8/8, plus Sarvam or Vaibhav's own voice), which also removes the
   brief-consistency risk in §0.3.
2. **Credits first:** Omni (Vertex) for every plain and ambitious t2v shot and the 10 s story; Veo 3.1 fast 1080p for the
   presenter; NB2 for stills; Lyria for music. **fal only** for Kling i2v (1080p, 8/8) and FLUX plates, and only after a
   top-up.
3. **Every piece of text is code** (U3 overlay, U4, U9): FLUX.2 Pro or NB2 textless plate → Kling/Wan/H3 i2v → hb-view
   layers via ffmpeg. No model is ever asked to spell.
4. **Budget:** first pass ≈ USD 8.2 (₹781); with the two presenter redraws and the smoke ≈ USD 13.2 (₹1,262) against a
   USD 31.44 (₹3,000) cap — comfortable, provided GCP credits exist and fal is topped up by ~USD 10.
5. **Before any `--confirm-spend`:** a signed spend record naming the pilot, the ceiling, the routes, 0 retries and the
   approver (`CONTROL-STATE.md` §6/§9). This document and the recipes are USD-0 preparation only.

---

## 8. Files read (authority for the claims above)

`PROJECT-MEMORY.md`; `coordination/CONTROL-STATE.md`; `runtime/ALPHA-1.md`; `eval/capability-map/ROUTING-EVIDENCE-MAP-v0.yaml`
(RR-1…RR-16, 61 cells); `eval/capability-map/TAINT-REGISTER-v1.yaml` (36 clean / 25 directional / 17 eliminated / 3
replacement_needed); `eval/registry/registry-v1.jsonl` + `SCHEMA-v1-draft.yaml` (575 rows: 120 latency, 120 cost, 117
format, 117 reliability, 101 reproducibility; lanes image 262 / general_video 150 / native_av 119 / tts 32 / lipsync 12);
`eval/empirical-planning/price-pins-2026-09/PIN-INDEX.yaml` + `gemini-api/`, `elevenlabs-direct/`, `sarvam-bulbul-v3/`,
`wan-2.2-a14b/` sub-indexes (81 pins verified by `coordination/audits/tools/verify_price_pins.py`);
`eval/empirical-planning/ROSTER-REFRESH-2026-09.yaml`; `ACCESS-STATUS-2026-09.yaml`; `eval/experiments/EVAL-040/DAY-2-SUMMARY-2026-09-09.md`
and `runs/{vid-i2v,vid-ref,vid-2spk,vid-ms,aud-lip}/RESULTS.yaml` (verdict notes read trial by trial), sealed
`.request.json` bodies for vid-i2v / vid-ref / vid-2spk, `runs/topo3-video/VIDEO-COMPOSITE-SPEC.yaml`;
`eval/empirical-planning/STAGE-A-FREEZE-2026-09/{ACCEPTANCE-CONTRACTS.md,ELIMINATION-RULES.md,TEST-CASES.yaml,BLUEPRINTS/VID-2SPK-01.blueprint.md}`;
`eval/harness-v2/{README.md,surfaces.py,transports.py,composite.py,stack_audio.py,pricing.py}` and
`adapters/{fal_queue,vertex_veo,vertex_omni,gemini_api_omni,gemini_api_image,vertex_gemini_image,vertex_lyria,sarvam_tts,elevenlabs_direct}.py`;
pinned fal OpenAPI under `eval/harness-v2/schemas/fal/`; Vertex extracts under `schemas/vertex/`;
`eval/battery/devanagari-exactness/devtext.py`; `adwisely-order-mode/ordermode/{textrender,fonts,layout,compose,imageio,pricing.yaml}`,
`providers/real.py`, `docs/2026-09-14-ad-design-direction.md`; `preprod/COMMERCIAL-BRIEF.md` (format facts only).
