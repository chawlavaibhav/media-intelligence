# Stage 4 — Production selection · AGY-2026-09-20-RENTOK-GAME-LANE-B-001 (lane B)

Author: lane-B producer session. Date: 2026-09-21 (UTC). Cost: USD 0 — no paid call has been made; `tools/dispatch.py` has `CAP_USD = 0.0` and refuses every reserve until the Controller's written cap is recorded.
Gate rule: riskiest element tested first; every route has evidence or a test; pool balances read before dispatch.

Live PriceBook quotes (USD 0, `stages/evidence/pricebook-quotes.txt`, re-run by `tools/dispatch.py quotes`): nano-banana-2 **0.067/image** (credits) · nano-banana-pro 0.134/image (credits) · lyria **0.06/clip** (credits) · sarvam-bulbul-v3 **0.002264 per 72 chars** (₹3 per 1,000 characters converted; the PriceBook labels the pool `cash`, the routing table says `sarvam_credits`) · elevenlabs-v3-direct 0.0072 per 72 chars (PriceBook `cash`; routing table `elevenlabs_credits`, plan credits) · veo-3.1-fast-i2v 0.80 per 8 s · gemini-omni-1.1-flash 1.0136 per 10 s (the last two are quoted for the record; not used).

---

## The production method — decided on this plan's requirements

| Requirement from the board | What it demands | Generative video (Veo 3.1 Fast t2v/i2v, Omni) | AI still → code animation | Decision |
|---|---|---|---|---|
| One character identical across 17 beats / 30 s | identity held across every frame | RO-02 (case 001): identity drifted across chained Veo pieces; RO-02 (case 002): two independent Veo generations gave two different narrators; no route holds a sprite's identity across 8–10 separate clips | one sprite sheet drawn in one call → identity is fixed by construction; code reuses the same pixels for 30 s | **still → code** |
| Exact in-game text (labels, cards, cheat code, CTA) | byte-exact strings | RR-6 "never ask the premium video model to write the text"; RR-10/RR-11 video routes invent lettering | text set by code on textless plates (RR-1, 4/4) | **code** |
| Physical contact with obstacles at set times (hit at 2.6 s, beam at 16.9 s …) | deterministic timing, five + five contact events | a video model cannot be told "hit at 2.6 s"; a 30-s film would be 4 clips × 8 s with joins | timeline in code; contact is a coordinate test | **code** |
| Two world states from one world (dusty → clean) | same geometry, new palette | would need a second generation, different geometry | one plate + a code recolour | **code** |
| 30.0 s ± 0.5, 30 fps, 1080×1920 | exact container | Veo outputs 4/6/8 s at 720p/1080p; assembly needed anyway | rendered to spec directly | **code** |
| Budget (provisional USD 10) | | ≈ 30 s × 0.10 = USD 3.0 per attempt with no identity control | ≈ USD 0.81 expected, all in | **still → code** |

**Method: original AI stills (Nano Banana 2) for the character sheet, the five obstacle pairs and the world plate; everything else — HUD, labels, cards, beam, phone, flag, end card, camera scroll, hits, palette change, SFX, mix, encode — by code (Pillow + numpy + hb-view + ffmpeg).** This coincides with what the supplied direction suggested; it is adopted because the four requirements above have no generative-video answer in the evidence, not because it was suggested (Stage 3 change #16). No video model is used; none is wired in `tools/dispatch.py`.

Retro look: generated assets are flat cel-shaded at high resolution; a code pixelation pass (downscale ÷k, nearest-neighbour ×k, default k = 3, tunable at Stage 5 after the first sheet) unifies assets from separate draws into one texture. Text is NOT pixelated (readability: sk_wcag_0022 familiar letterforms).

## 4.2 — Asset list with dependencies, routes, evidence, price

| id | asset | method | route (cell) | evidence status / use | unit price | planned draws (+repair) | depends on | exact-text mechanism |
|---|---|---|---|---|---|---|---|---|
| A1 | **Character sprite sheet** — 9 poses in a 3×3 grid on flat magenta: run 1–4, jump, hurt, cornered, powered-run A, powered-run B | AI still | IMG-CORE/nano-banana-2 | clean_observed 7/8, use=True | 0.067 | 1 (+1) | — (FIRST: micro-qualification) | none — prompt forbids lettering; post-draw text scan |
| A2a–e | **Obstacle pairs** ×5 — each one 1:1 image, two panels (creature ‖ cleared state) on magenta | AI still | IMG-CORE/nano-banana-2 | as above | 0.067 | 5 (+2) | A1 frozen (style anchor described in the prompt, no reference image) | none |
| A3 | **World plate** — 16:9 PG street facade, sky, pavement, no people, no signage | AI still | IMG-CORE/nano-banana-2 | as above | 0.067 | 1 (+1) | A1 frozen | none; signage forbidden; paint-out by code if a small mark slips through |
| A3b | world "after" palette | code recolour of A3 | code | — | 0 | — | A3 | — |
| A4 | HUD (hearts, `LEVEL 1`, score, power-up slot), labels, cards, cheat bar, `CONTINUE?`, `LEVEL COMPLETE`, end card | code (hb-view + Pillow) | code | — | 0 | — | copy deck | code_set_on_textless_plate |
| A5 | phone + app icon, OK-glyph beam, shield glow, flag (wordmark composited on a code-drawn flag), fireworks | code | code | — | 0 | — | S-LOGO | — |
| A6 | Music bed 30 s | AI music | MUS/lyria+native | clean_observed 4/4, use=True | 0.06 | 1 (+1) | — | n-a |
| A6b | Chiptune fallback | code (numpy square/triangle waves) | code | — | 0 | — | — | n-a |
| A7 | SFX ×10 | code | code | — | 0 | — | — | n-a |
| A8 | Voice: 3 announcer lines, candidate A | AUD-TTS/sarvam-bulbul-v3+native | clean_observed 6/6, use=True | 0.0023 per ~72 chars (≈ 0.002 for the 3 lines, 61 chars) | 3 calls (one per line) | — (FIRST in work order) | on-screen = spoken |
| A8b | Voice candidate B | AUD-TTS/elevenlabs-v3-direct+native | clean_observed 4/6, use=True | plan credits (PriceBook shows 0.0072/72 chars cash-equivalent) | 3 calls | — | on-screen = spoken |
| A9 | Assembly: frame renderer → ffmpeg H.264/AAC 1080×1920 30 fps | code | code | — | 0 | — | A1–A8 | — |
| D1 | Deliverable `deliverables/rentok-lane-b-30s-9x16.mp4` (9:16, 1080×1920) | — | — | — | — | — | A9 | one `qa.final_geometry` row |

Fallback cells (declared): A1–A3 → IMG-CORE/nano-banana-pro (clean 4/8, use=True, 0.134) only after two nb2 failures on the same asset; A6 → A6b code; A8 → A8b (or the reverse, by the audition). No `manual_only` or `False` cell is used anywhere. No fal.

Reuse provenance (QA G1): nothing is reused from earlier work. The hb-view text renderer is adapted from `tools/reference-kit/overlay_text_video.py` (a tool, not a design treatment). The wordmark is the customer's brand asset (S-LOGO), not prior creative.

## 4.1 / 4.3 — Risk order and known failures (with ids)

| rank | capability | why it is the riskiest | known failures (source id) | test |
|---|---|---|---|---|
| **1** | A1 character sheet: one identity across 9 poses, no lettering, no Nintendo drift, clean keying | every later asset and the whole animation depend on it; nb2 with a reference image is not a registered cell, so consistency must come from one draw | RO-04 (case 001): nb2 drew paper-like text despite "no text"; RO-04 (case 002): clean when paper/notes/posters were explicitly forbidden · EVAL-038 videos failed on baked-in text (PROJECT-MEMORY §5) · IMG-CORE nb2 1/8 rejected in the Lab (routing table) | **micro-qualification: one draw (USD 0.067)**, checker-inspected against a 6-point card (identity across cells · no cap/moustache/overalls · no lettering · flat magenta background · side view · pose set complete); then FROZEN; nothing dependent is drawn before |
| 2 | A2 obstacle pairs: distinct silhouettes; cleared state readable at ~250 px | five draws; A3 mapping (LJ) rides on silhouettes | same lettering risk (RO-04); calendar digits and receipts invite text — prompts say "no digits, no writing" | drawn after A1 freeze; each pair judged on a 270-px thumbnail contact sheet before use |
| 3 | A3 world plate: shop signage / lettering; a "PG" nameplate that is legible but wrong | RO-06 (case 001): Kling sharpened blurred signage into letters (a video risk we avoid by not animating the plate generatively); RO-04 lettering | prompt forbids signs/boards/text; post-draw scan; small marks painted out by code (recorded as a repair at the `text` layer) |
| 4 | A6 Lyria chiptune | n = 0 for chiptune on Lyria; RO-09 (case 001): three provider errors on advertising-flavoured wording | neutral prompt; one draw; code fallback at USD 0 |
| 5 | A8 voice as an arcade announcer | RO-05 (case 001): Sarvam cadence judged robotic on long narration (~1,000 chars) — lines here are ≤ 28 chars, where the Lab's evidence (≤ 70-char lines, 6/6) applies; SD-HD-13b (case 002): two clips two voices — avoided by one source | audition A vs B by ear on the assembly of the three lines |
| 6 | Keying / pixelation artefacts | halo fringes on magenta edges | erode 1 px + matte; inspect on the contact sheet |

Not generative but real: the animation code itself (contact timing, label holds, safe-zone placement) — covered by the DET checks below, not by draws.

## 4.4 — Text, logo, UI generated? No.

Every string in the copy deck is composed by code (`tools/text_render.py`, hb-view + Pillow, Helvetica Neue Bold / Condensed Bold from the fonts listed in the reference kit). The wordmark is the customer's file, composited. The app icon, phone, HUD and cards are drawn by code. No generation prompt contains any string from the deck (DET: `tools/qa_checks.py prompts` greps every prompt for every deck string and for the Nintendo list; `dispatch.guard_prompt` refuses the latter before reserving).

## 4.5 / 4.6 — Voice: one source; durations measured before the timeline is frozen

`plan.voice.source_count = 1` (the audition winner supplies all three lines; the audition takes ARE the takes — no regeneration). `tools/render_film.py` reads the measured durations of V1–V3 (ffprobe) and asserts, through `tools/vo_schedule_gate.check_vo_schedule`, that no two lines overlap and V3 ends ≤ 29.6 s; the board's slots (F8 1.8 s, F9 1.6 s, F16+F17 3.4 s) are the maxima; if a measured line is longer than its slot the slot grows and the adjacent hold shrinks by code, never the label hold below 1.2 s (CA-D8 rule).

## 4.7 — References

No reference images are sent to any route (consistency is inside one draw). Identity anchors for the CODE stage: the frozen A1 sheet (sha256 recorded on freeze) is the only source of character pixels; A2/A3 prompts describe the same style in words (flat cel-shade, thick outlines, palette hexes).

## 4.8 — Pool balances

**Not yet read.** No reading exists for any pool this plan touches (Google Gemini-API/Vertex credits, Sarvam credits, ElevenLabs plan credits). A7 is a hard stop, so before the first dispatch at Stage 5 each pool gets a `{pool, balance, read_utc, source}` line in `JOB.yaml spend.pool_readings`: Google credits via the Cloud Billing console or `runtime/execute/pools.py` shape (the Controller reads; there is no free API for credit balance known to this session — UNKNOWN); Sarvam via its dashboard/API; ElevenLabs via `GET /v1/user/subscription`. A balance read is a non-paid call but is deferred until the cap arrives so that nothing touches the providers before authorisation.

Open discrepancy for the checker: the roster row for `elevenlabs-v3-direct` carries `surface_model_id: fal-ai/elevenlabs/tts/eleven-v3` (a fal path) while the routing map's surface is `elevenlabs_direct` and the tool calls `api.elevenlabs.io` directly (as the reference kit did). The direct endpoint is what is used; no fal.

## 4.9 — Expected spend vs cap

| item | draws × price | USD |
|---|---|---|
| A1 character sheet | 1 × 0.067 | 0.067 |
| A2 obstacle pairs | 5 × 0.067 | 0.335 |
| A3 world plate | 1 × 0.067 | 0.067 |
| A6 music (Lyria) | 1 × 0.06 | 0.060 |
| A8 voice audition A (Sarvam, 3 lines ≈ 61 chars) | ≈ 3 × 0.0007 | 0.002 |
| A8b voice audition B (ElevenLabs, plan credits; cash-equivalent shown) | ≈ 3 × 0.002 | 0.006 |
| **Expected (no repairs)** | | **≈ 0.54** |
| Repair round (one each: A1 +1, A2 +2, A3 +1, A6 +1) | 4 × 0.067 + 0.06 | 0.328 |
| **Expected with one repair round** | | **≈ 0.86** |
| Worst case inside the hard stop (pro fallback for A1 + A3, 2 more obstacle repairs) | + 2 × 0.134 + 2 × 0.067 | ≈ 1.27 |
| Provisional ceiling (UNCONFIRMED) | | 10.00 |

If the confirmed cap is lower than USD 10: nothing changes down to USD 1.30. Below that, cut in this order: (1) drop candidate B of the audition (−0.006), (2) drop Lyria, use the code chiptune (−0.06 / −0.12 with its repair), (3) drop the obstacle repair allowance (−0.134), (4) draw the five obstacles as two sheets (3+2) instead of five (−0.20) — accepting a higher risk of one weak creature spoiling a sheet. The minimum plan that can still deliver is ≈ USD 0.47 (A1 + 2 obstacle sheets + A3 + Sarvam) with no repair; a cap below USD 0.50 cannot fund a single repair and this is stated to the Controller before the first call.

## 4.10 — Order of work

1. Pool balances read and recorded; cap recorded in `JOB.yaml` and `CAP_USD` (Controller's written cap only).
2. Voice audition (A8 × 3 lines, A8b × 3 lines) → durations measured → winner frozen (human ear; checker-inspected).
3. **A1 character sheet — the riskiest — one draw → checker inspection → freeze (sha256).** Repair once if needed; pro fallback after two failures.
4. A2a–e obstacle pairs → thumbnail contact sheet → freeze.
5. A3 world plate → text scan → freeze; A3b recolour by code.
6. A6 Lyria → listen; else A6b.
7. Code: keying → pixelation → timeline with measured VO → render 900 frames → mix → encode.
8. QA bundle (below) → contact sheet → checker LJ → human release.

## Text-rendering approach

`tools/text_render.py` (adapted from the reference kit's `render` subcommand): hb-view shapes each deck string with the font file + face index → transparent PNG at the declared cap height → Pillow composites onto an opaque dark plate (`#101528` at 92 % or brand blue for cards) with a 24-px inset (READABILITY_MARGIN candidate) → contrast measured by `runtime.compositor.gates.check_contrast` on the actual pixels behind the text → bounds by `check_text_bounds` against the canvas AND the safe box (x 65–1015, y 269–1248) → `check_disjoint` across HUD / label / card / cheat-bar regions on every frame where two coexist. A two-line wrap keeps the cap height (STACK_LEVEL_FIT candidate); it never shrinks the string.

## Audio approach

- Music: Lyria (MUS clean 4/4, USD 0.06); prompt: "upbeat 8-bit chiptune, bright square-wave lead, driving bass, 140 bpm, playful, instrumental, no vocals" — no brand or advertising words (RO-09). Trim 32.8 → 30.0 s with a 0.3-s fade; the F7 drop-out and F9 return are code-side gain automation on the same track. Fallback: `tools/chiptune_fallback.py` (USD 0).
- SFX: `tools/sfx_synth.py` (numpy): step, hurt, thud, ring-buzz, key blip, chime, beam, stamp, flag zip, fanfare.
- Voice: Sarvam bulbul:v3 (candidate A) vs ElevenLabs v3 (candidate B), three lines each, one winner.
- Mix: `tools/mix_audio.py` → ffmpeg `amix` + sidechain-free manual ducking (−6 dB under V1–V3) → `loudnorm` to I = −14 LUFS, TP = −1 dBTP (Stage 2 §2.6 target, our own) → AAC-LC 48 kHz stereo 192 kbps.

## Assembly method — the tools this job writes (all under `tools/`, all USD 0)

| tool | does |
|---|---|
| `dispatch.py` (written, adapted) | paid calls with cap/ledger/attempt records; no fal; `CAP_USD = 0.0` until the cap arrives; `guard_prompt` refuses Nintendo words |
| `_common.py` (adapted) | key-by-name, scrubbing, HTTP, bounded polling, gcloud SA token |
| `vo_schedule_gate.py` (copied) | VO lines from measured durations: no overlap, no overrun |
| `text_render.py` | hb-view + Pillow string → plate PNG; bounds/contrast/disjoint via `runtime.compositor.gates` |
| `keying.py` | magenta chroma-key of A1/A2 sheets → per-pose RGBA sprites; 1-px erode; slice the 3×3 / 2-panel grids |
| `pixelate.py` | ÷k nearest-neighbour ×k pass over A1–A3 (k default 3) |
| `render_film.py` | the timeline (F1–F17 from a table), side-scroll camera, sprites, HUD, labels, cards, beam, hits, palette flip, flag, end card; streams raw frames to ffmpeg (no 900-PNG spill — 8 GB machine) |
| `sfx_synth.py`, `chiptune_fallback.py`, `mix_audio.py` | audio as above |
| `qa_checks.py` | `container` (ffprobe: 1080×1920, h264 High, yuv420p, 30/1, aac 48 kHz 2 ch, 29.5–30.5 s, moov-before-mdat) · `safezone` (every text placement from the layout table inside the box; right-edge rule) · `copy` (rendered strings == deck byte-exact; forbidden-list scan over deck + VO transcript) · `prompts` (no deck string, no Nintendo word in any prompt) · `frames` (sample first, last, every 1.0 s and ±0.2 s around the three cuts → contact sheet under `qa/`) · `loudness` (ffmpeg ebur128) |
| `contact_sheet.py` | 6-column sheet of the sampled frames with the 14/35/6 safe box drawn |

## QA plan — every acceptance item → a named check

| item | check | kind | tool / judge |
|---|---|---|---|
| A1 platform game, not graphics over an ad | five-item LJ checklist (side-scroll · player · obstacles · HUD · flag) on the contact sheet + a full viewing; DET support: game frame ≥ 24 s from the timeline table | LJ + HJ | checker session; customer |
| A2 PG owner recognisable | checker names the identifiers seen in F1–F2 at phone scale (a 375-px-wide render of the frame is supplied) | LJ + HJ | checker; customer |
| A3 five obstacles identifiable | DET: C04–C08 rendered byte-exact on F2–F6 (`qa_checks.py copy`); LJ: per-obstacle mapping to the customer's five | DET + LJ | code; checker |
| A4 cheat code = install RentOk, central | DET: C10 on F8 at 12.6–14.4 s (timeline table + frame sample at 13.5 s); LJ: reads as the turning point | DET + LJ + HJ | code; checker; customer |
| A5 visible enhanced ability | LJ on F9–F10 frames (phone, glow, slot ON, hearts refilled) | LJ + HJ | checker; customer |
| A6 all obstacles overcome, flag reached | LJ: five clears + flag on frames 16–26 s; DET support: five beam-contact events logged by `render_film.py` | LJ + HJ | checker; customer |
| A7 duration | `qa_checks.py container` — ffprobe 29.5–30.5 s | DET | code |
| A8 platform fit + safe zones | `qa_checks.py container` + `safezone`; LJ on the contact sheet with the box drawn | DET + LJ | code; checker |
| A9 original | DET: `qa_checks.py prompts` (no Nintendo word; `guard_prompt` at dispatch); LJ: Stage 2 §2.5 do/don't list against A1–A3 and the film | DET + LJ | code; checker |
| A10 relevance | HJ (customer); LJ proxy: the checker's one-sentence muted-viewing statement | HJ | customer; checker |
| A11 no unverified claim | DET: forbidden-list scan over deck + VO transcripts (`qa_checks.py copy`); LJ: implied-claim pass on F12 (dues visible ≠ recovered) | DET + LJ | code; checker |
| D factual accuracy | every C13–C17 string ↔ Stage 2 citation table (checker re-reads the cited lines) | LJ | checker |
| C production quality | QA-CHECKLIST B (stills), C (composition gates), D (video frames D1–D13; D14 voice continuity on the three lines), E (delivery) | DET + LJ + HJ | code; checker; human |
| Frame text hygiene (D1) | human-eye pass on the sampled frames + `runtime.loop.frame_hygiene.assess` over the human verdicts; the paid Cloud Vision detector is not authorised (CONTROL-STATE §8) → recorded as NOT_RUN for the detector, PASS/FAIL by the human-eye pass | LJ | checker |

## Pre-dispatch (QA-CHECKLIST A) status now

A1 Canon gate: to run at Stage 5 over the three generation prompts + this plan (`python3 canon/gate/run_gate.py pre …`) · A2 check lines rendered (Stage 3 §3.11) · A3 no critical string in any prompt (guarded) · A4 route evidence: every route clean_observed + use=True · A5 prices pinned live (above) · A6 **cap: absent → BLOCKS** · A7 **pool readings: none → BLOCKS** · A8 consent: no identifiable person in any asset · A9 micro-qualification: A1 planned first · A10 TTAO: `job_start_utc` stamped; `planning_complete_utc` stamped at the end of this stage.

## Stage 4 exit criteria — self-assessment (the checker issues the verdict)

| Criterion | Self-assessment | Evidence |
|---|---|---|
| Riskiest element identified from evidence (not the author's label) and tested first | met | rank 1 = A1 sheet, cited to RO-04 ×2, EVAL-038, IMG-CORE 1/8; work order step 3 |
| Every route has evidence or a test | met | asset table: every cell clean_observed + use=True; Lyria chiptune n=0 → one draw + USD 0 fallback |
| Prices quoted live | met | PriceBook quotes saved; `dispatch.py quotes` |
| Pool balances read | **not met — deliberately deferred** until the cap arrives; recorded as blocking A7 | 4.8 |
| Spend vs cap with a repair round; cuts named | met | 4.9 |
| Text/logo/UI never generated | met | 4.4 |
| Tools adapted; no fal; no paid call | met | `tools/dispatch.py` (refuses at CAP 0.0 — verified), `_common.py`, `vo_schedule_gate.py` |
| QA plan maps A1–A11 | met | table above |
