# Treatment D — production-method alternative (generative video with C's direction)

Experiment `RENTOK-CREATIVE-QUALITY-001`, Phase 2. Produced 2026-09-21. Labels: OBSERVED / INFERRED / UNKNOWN.

**This is a route comparison, not a prompt-only result.** D changes the production route (image-to-video on a video model) *and* carries C's direction in the prompt; it cannot separate the two, and the clip's tempo, effects and continuity are the model's, not the board's.

## 1. Deliverable

| Item | Value |
|---|---|
| Clip | `D-14.0-20.8.mp4` — sha256 `03439a521c3e432991ce6898f0baae0710db72765e81cd1d054e0be33a00c992` |
| Geometry | 1080×1920, h264 30 fps, **205 video frames = 6.833 s** (the generated 720×1280 24-fps clip upscaled LANCZOS, nearest source frame per output frame), aac 48 kHz stereo (the clip's **native audio**, 6.855 s), no edit lists |
| Deviation from the window | the route produced an 8.0-s clip; it is trimmed to 0–6.833 s to match the baseline window — the dropped 1.17 s show only running past the debris; the events themselves fall at the model's tempo (§5), not at the board's timecodes |
| Loudness | I = −13.8 LUFS on the delivered file (native audio; not ear-checked — §7) |
| Contact sheets | composite `CONTACT-SHEET-10fps.png` (sha256 `fed6bde3…`); raw takes `D1-microqual-CONTACT-SHEET-10fps.png` (`2d39d511…`), `D1-take2-…` (`999adeda…`), `D1-take3-…` (`143aefaf…`); frame pulls in `frames-microqual/`, `frames-take2/`, `frames-take3/` |
| Code | `composite_d.py` (sha256 `3209bcd5…`), event table `gen/take3-events.json` (`03e97847…`) |

## 2. Route, evidence status, settings (OBSERVED)

| Field | Value |
|---|---|
| Route | `veo-3.1-fast-i2v` — Vertex `veo-3.1-fast-generate-001`, `predictLongRunning` → `fetchPredictOperation`, inline bytes |
| Cell / status | VID-I2V · `clean_observed` · `production_use_allowed: true` · 5/8 (Lane A `stages/evidence/routing-table.txt`); directional notes: RR-8 "avoid Veo 3.1 fast i2v where the brief forbids camera moves", map "0/2 on the phone still: 'zooms in'", Cumin RO-02 "static camera obeyed 6/6" |
| Price | USD 0.10 per second (PriceBook, pin `vertex-generative-ai-pricing.html`) → 8 s = **USD 0.80 per draw**; credits (Vertex service account `~/.aight-litellm-keys/vertex-sa.json`, token via a throw-away gcloud config — `_common.gcloud_sa_token`) |
| Parameters (every draw) | `sampleCount 1`, `durationSeconds 8`, `aspectRatio 9:16`, `resolution 720p`, `generateAudio true`, `negativePrompt` (§3); no seed, no `personGeneration` (vendor defaults, as the harness adapter) |
| Probes not run | D2 `veo-3.1-fast-ref2v` (VID-REF 2/4) and D3 `gemini-omni-1.1-flash` t2v (VID-T2V 8/8) were conditional in 05 §3b on D1 failing identity or the world; D1 held both, so neither probe was spent. `veo-3.1-fast-extend` is `manual_only` and was never in the tool |

## 3. Reference package (OBSERVED, `refs/`)

| File | sha256 | What it is |
|---|---|---|
| `start-frame-14.000-world-1080x1920.png` | `83938d89…` | the baseline **world** at frame 420 (14.000 s) rebuilt from the frozen primitives with **no UI**: plate parallax at `camera_x(14.0)`, `draw_ground`, the complaints swarm at its baseline position (x 520, on the ground line), the owner in the run-A pose at (260, ground−260) |
| `start-frame-14.000-world-720x1280.png` | `8f8679b4…` | the same, LANCZOS-resized to the accepted Veo i2v geometry — **the image input of all three draws** (recorded per attempt as `image_sha256`) |
| `ingredient-owner-1024.png`, `-swarm-`, `-wall-` | `7e88b5f1…`, `464fbad5…`, `edb1e2db…` | cut-outs padded onto flat mid-grey 1024² for the D2 probe — **not used** |

Negative prompt (`prompts/D1-negative.txt`, sha256 `ee4bfe87…`), sent as `negativePrompt` on every draw: `text, lettering, captions, subtitles, HUD, health bar, logos, watermark, photorealistic, 3D render, camera zoom, camera pan, extra people, extra hands`

## 4. Every attempt — prompt verbatim, USD, result, inspection (OBSERVED, `treatments/ATTEMPTS.jsonl` att-007…009)

All three: `status ok`, 8.000 s, 720×1280, 24 fps, h264 + aac (native audio), latency 72–98 s, no refusal, no `raiMediaFilteredCount`. Prompt guard passed (no IP word, no copy-deck string, no-lettering clause).

### att-007 · D1-microqual · USD 0.80 · `gen/D1-microqual_att-007.mp4` sha256 `c7fb8cd0…`

Prompt (`prompts/D1-veo-i2v.txt`, sha256 `6c89c220…` — the 05 §3c prompt verbatim, 345 words):

> Side-scrolling 2-D platform game view: the camera is locked level at ground height and does not zoom, tilt or cut; the level scrolls slowly from right to left; vertical 9:16 frame. The player character from the start image: an ordinary Indian man of about forty, slightly stocky, short black hair, rectangular spectacles, a blue-and-white checked half-sleeve shirt, dark trousers, brown sandals, a big bunch of keys on a ring at his belt, a thick red account book under his left arm — he stays exactly this man throughout. Action, in order: he runs right toward a swarm of five angry red speech-bubble creatures; they dive at him; he is knocked back onto one knee, shocked, the book tumbling then caught; the whole scene dims to cold blue-grey while the red creatures hover over him; a small plain blue phone drops from above into his raised open hand and its screen lights up cyan; a burst of cyan-white light floods out from the phone and full warm colour returns; a pulsing cyan glow wraps his body and he stands tall, jaw set, holding the phone forward; he runs right and punches his fist forward, firing a bright cyan tick-shaped bolt with a short trail at a tall leaning wall of blank white paper sheets, which bursts outward into tumbling sheets as he runs on. Context: an Indian city lane in front of a tall cream-and-terracotta paying-guest building with stacked floors of small windows, water tanks on the roof, a packed-earth lane with a stone kerb. Style: flat 16-bit pixel-art game animation, crisp square pixels, matte colours, 2-pixel dark outlines, hard-edged sprite motion with clear key poses, daylight from the upper left. Audio: an upbeat 8-bit chiptune bed; a crunchy 8-bit hit when the creatures strike; a low hum while the scene is dim; a rising four-note chiptune arpeggio when the phone lights; a soft pew for the bolt; a crunchy burst for the wall. All walls, sheets and screens are plain and blank; no text, no letters, no numbers, no health bar, no logos, no watermark.

**Micro-qualification, per criterion (frames in `frames-microqual/`, sheet `D1-microqual-CONTACT-SHEET-10fps.png`):**

| Criterion | Verdict | Evidence |
|---|---|---|
| (i) identity held — the owner is the same character | **PASS** | `t0.9`, `t2.5`, `t3.4`, `t4.9`, `t7.5`: spectacles, short black hair, blue-white checked shirt, dark trousers, sandals, keys at the belt, red book — the same man from the start frame to the last frame |
| (ii) pixel-art / game aesthetic held | **PASS with a note** | the world, sprites and outlines stay flat and pixel-styled for the whole clip; OBSERVED softening: the glow, the burst and the flying sheets are painted (anti-aliased, painterly), and after the burst (≈ 5.5 s on) the character's outline is smoother — closer to cel-shaded cartoon than to crisp 16-bit pixels; no drift to 3-D or photoreal |
| (iii) spatial continuity | **PASS with a note** | the camera stays side-on and level with the ground line fixed; the level scrolls right-to-left throughout; **the street drifts**: after the burst the tall facade row is replaced by a different, lower building row with an awning and trees (`t6.5`, `t7.5`) — a scrolling level may change, but this is not the plate's world |
| (iv) the transformation visible | **PASS** | knock-down to one knee (`t0.9`), the world dims (`t1.5`–`t2.5`), the phone falls into his raised hand (`t2.5`), a cyan-white burst (`t3.4`), a cyan aura around his body while he stands and then runs (`t4.0`, `t4.9`) |
| (v) no stray lettering | **PASS with a note** | no letters or digits on any sampled frame; one small grey plaque on the drifted shop-front (`t6.5`, zoomed) carries a few illegible marks, not letters |
| (vi) no Nintendo drift | **PASS** | no cap, overalls, moustache, mushroom, pipe, coin or block anywhere |
| (vii) motion quality | OBSERVED (not pass/fail) | weight in the knock-down, the book drops and bounces, dust on landing, the beam and the wall burst with sheets — secondary motion the code treatments do not have |
| Event chain in order inside 8 s | **PASS** | faces the swarm (0–0.9) → hit (0.9) → dims (1.0) → phone (2.0–2.5) → burst (3.0–3.5) → aura + stands (3.6) → fires (4.0) → wall bursts (4.1–5.5) → runs on |

Defects (OBSERVED): a **duplicate book** — after the hit one book lies on the ground for the rest of the clip while another is under his arm (`t3.4`, `t4.9`); an unrequested **orange fire flash** inside the wall burst (`t4.9`); the paper wall is **visible from the first frame** beside the swarm rather than entering later; the street drift above. **Verdict: micro-qualification PASSED on identity + aesthetic (the gate for further spend) — proceed.**

### att-008 · D1-take2 · USD 0.80 · `gen/D1-take2_att-008.mp4` sha256 `8d09f704…`

The Media Factory practice applied (Controller step 4; 03 §2.6 P1/P5): **iterate on the same plate with one recorded change-set, compare takes.** Prompt `prompts/D1-veo-i2v-take2.txt` (sha256 `8cc89335…`, 397 words) = att-007's prompt with four edits, verbatim:
- "a thick red account book under his left arm — he stays exactly this man throughout." → "a thick red account book **that stays clamped under his left arm for the whole clip** — he stays exactly this man throughout."
- "he runs right and punches his fist forward, firing … at a tall leaning wall of blank white paper sheets, which bursts outward into tumbling sheets as he runs on." → "he runs right; **only now a tall leaning wall of blank white paper sheets slides into view from the right edge**; he punches his fist forward, firing a bright cyan tick-shaped bolt with a short trail at the wall, which bursts outward into tumbling blank sheets **and dust** as he runs on."
- Context sentence + "**; the same row of tall buildings continues behind him for the whole clip, with nothing else in the street at the start.**"
- "All walls, sheets and screens are plain and blank; no text …" → "All walls, sheets and screens are plain and blank, **with no signboards or plaques; no fire or flames**; no text …"

Result (sheet `D1-take2-CONTACT-SHEET-10fps.png`, frames `frames-take2/`): book stays under the arm — fixed; wall enters late (≈ 3.5–4.0 s) — fixed; no fire — fixed; the street still drifts after the burst (≈ 5.5 s) — not fixed. **New story defect:** the swarm **crumbles into red pieces on the ground right after the hit** (`t1.6`, `t2.4`) — the problem dies before the app arrives, which inverts the customer's mechanic. The phone screen shows a faint bolt-like glyph (`t2.4`) — a symbol, not lettering. Not selected.

### att-009 · D1-take3 · USD 0.80 · `gen/D1-take3_att-009.mp4` sha256 `abc74298…` — **selected**

One change on take 2's prompt (`prompts/D1-veo-i2v-take3.txt`, sha256 `e81cf6dc…`, 416 words), verbatim:
- "the whole scene dims to cold blue-grey while the red creatures hover over him;" → "… while the red creatures **stay whole, alive and angry, hovering over him the entire time**;"
- "a burst of cyan-white light floods out from the phone and full warm colour returns;" → "a burst of cyan-white light floods out from the phone, **the red creatures scatter away off the top of the frame**, and full warm colour returns;"

Result (sheet `D1-take3-CONTACT-SHEET-10fps.png`, frames `frames-take3/`, 0.1-s pulls): the swarm stays whole and angry over him through the grey beat (`t1.5`, `t2.3`) and scatters upward on the burst — the mechanic reads as asked; the wall enters at ≈ 5.0 s and bursts at 5.2–5.4 with cyan bolt, grey dust and sheets; the tall facade row holds until ≈ 6 s, after which a lower row appears (drift smaller than takes 1–2). Defects: the **duplicate book returns** (a book on the ground from 1.0 s while one stays under his arm, `t2.3`); **small orange sparks** in the burst (`t4.2` per the 4.2-s pull; fire was excluded in the prompt); the character **softens toward cel-shading** after the burst (`t6.0`, `t7.0`). No lettering on any sampled frame.

Why take 3 over take 2 (INFERRED): the customer's mechanic is "install → power → clear the obstacles"; take 2 clears the first obstacle before the install, take 3 keeps it alive until the power arrives. Take 3's duplicate book is a continuity slip; take 2's is a story inversion.

Treatment D spend: **USD 2.400 reserved of the 4.811 maximum** (3 draws, 3 ok, 0 failed, 0 refused). Two planned probes unspent.

## 5. How identity, continuity and the transformation were held — or not (OBSERVED → INFERRED)

- **Identity** was held by the start frame (the accepted world with the owner in it) plus the description repeated word for word (03 §2.5 practice). In all three draws the man is the same in every frame. INFERRED: the image input, not the prose, is doing most of the work — the model kept even the checked-shirt pattern and the key ring.
- **Spatial continuity** was held for the camera (side-on, level, no zoom in 3/3 — the negative prompt and the locked-camera clause worked where the map recorded "zooms in" on a phone still) and for the ground line; it was **not** held for the *place*: in all three draws the plate's facade row is replaced by other buildings after the burst, and the same-street instruction in takes 2–3 only delayed the drift. INFERRED: the model treats the scroll as a journey and invents new scenery once the start frame's content has left the screen.
- **The transformation** — dim → phone → burst → glow — arrived in all three draws in the right order, with the phone lighting up and a body glow the code treatments approximate with a halo. The world dimmed and re-brightened without being told which colour to use.
- **Aesthetic** was held as "flat game cartoon" but not as "crisp 16-bit pixels": effects are painted, and the character softens after the burst. INFERRED: a video model animates *the style it reads from the start frame* and relaxes it under heavy effects.
- **Things the model did that were not asked** (all three draws): a fire/spark flash in the burst (2 of 3), a duplicate book (2 of 3), the swarm self-destructing (1 of 3), a plaque with marks (1 of 3). INFERRED, consistent with the map's "one 'hand appeared'" note: the route adds one or two unrequested elements per 8 s.

## 6. Compositing (OBSERVED, `composite_d.py`)

The generated clip is the world layer; the UI layer is drawn by code with the frozen `put_text` at the baseline's positions and scales: `PG OWNER` + health (1 → 0 at the hit, refilling in cyan after the flash), the wordmark chip, `COMPLAINTS` / `TENANT VERIFICATION` labels, `GAME OVER?`, the cheat panel with `CHEAT CODE:` / `INSTALL` / `RENTOK APP` typed, `POWER UP!`, the HUD phone icon and the `✓ DIGITAL KYC` chip flight. **UI timing follows the clip**, from `gen/take3-events.json` (clip-relative): hit 0.95 · `GAME OVER?` 0.95–1.35 · panel 1.35 (slide 0.15) · typing 1.55–2.55 · install (screen lights) 2.6 · panel off 2.6 · refill 2.95 · `POWER UP!` 3.1–4.3 · wall label 4.9–5.3 · chip 5.35. The model compressed the "code" beat: the baseline gives typing 1.4 s and a 0.8-s GAME OVER? hold; here GAME OVER? holds 0.4 s and typing 1.0 s so the code finishes before the screen lights — the one manual timing pass 05 §3f predicted (≈ 15 min, two passes because the first misread the contact-sheet labels by one row and put the flash a second early).

Gates over the composite's layout log (`tools/gates_over_log.py`, runtime `check_text_bounds` / `check_disjoint` + exact-copy): 205 frames, 808 boxes, **0 outside the safe box, 0 frames with overlapping UI, 0 copy mismatches** (B: 4,028 boxes / 0 / 0 / 0; C: 851 / 0 / 0 / 0).

What this does to A1 ("an actual platform game, not a promotional video with gaming graphics placed over it"): the picture is a game-styled world with a code HUD — the same relationship as the baseline — and the checker's furniture (side-scroll, player, obstacle, HUD, labels) is all present. INFERRED risk, for the evaluator: the generated world moves like a cartoon (painted effects, drifting scenery, a soft character after the burst), so the HUD may read as "graphics placed over a film" to a viewer who knows games; the 06 rubric's R8 and Q6 exist for exactly this.

## 7. Open items (UNKNOWN / not verified)

- **Native audio not ear-checked.** `generateAudio true` produced a 48-kHz stereo track (−13.8 LUFS) that is kept as the D clip's audio because it is part of what the route delivers. This session cannot listen; whether it contains speech, a recognisable melody or anything outside the prompt's SFX list is UNKNOWN. The evaluator and the checker must listen with sound on; if speech or a claim is heard, the clip must not leave the packet.
- **A9 (no Nintendo asset) on generated frames:** human-eye pass on ~30 sampled frames per take; no Cloud Vision or paid detector run.
- **Extending D to the full 30-s film** (mixed method) is not addressed; the unit is one beat cluster.
