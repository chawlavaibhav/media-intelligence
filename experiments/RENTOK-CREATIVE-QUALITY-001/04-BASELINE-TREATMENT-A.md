# 04 — Treatment A (baseline): the accepted Lane A power-up + first-clear sequence, frozen

Experiment `RENTOK-CREATIVE-QUALITY-001`, Phase 1 (USD 0). Written 2026-09-21. All values OBSERVED unless marked.

## 1. The clip

| Item | Value |
|---|---|
| File | `treatments/A-baseline/A-baseline-14.0-20.8.mp4` |
| sha256 | `b1810188053cc13eb63a397f6e1beeeaf93b8a0a218783d3defd1c16f62bfb33` |
| Source | Lane A final `gen/final/rentok-game-lane-a-9x16-30s.mp4` @ job commit `7dab37a`, sha256 `9d50c4c5729f32d198fbaafc642fd78eccc0ee11dee2131cb637270584b5e24a` (verified before cutting) |
| Cut | `ffmpeg -ss 14.0 -to 20.8 -i <final> -c copy -movflags +faststart` — **stream copy, no re-encode** |
| Why copy was possible | the final's GOP is 15 frames (`-g 15`, 0.5 s); 14.000 s (frame 420) is a keyframe (ffprobe: keyframes at 13.5, 14.0, 14.5) |
| Verification | first clip frame vs source frame at 14.000 s: mean absolute pixel difference **0.0** (Pillow/numpy); video pts starts at 0.000 |
| Geometry / codecs | 1080×1920, h264, 30/1 fps, 205 video frames (source frames 420–624 = 14.000–20.833 s); aac 48 kHz stereo, 321 frames |
| Duration | 6.833 s video (container 6.833 s); 8,050,116 bytes |
| Loudness (ebur128 on the clip) | I = −13.3 LUFS, LRA 3.0 LU (the full film measured −14.6 LUFS; this window contains the fanfare-free, key-click-dense middle) |
| Contact sheet | `treatments/A-baseline/CONTACT-SHEET-10fps.png` (69 frames at 10 fps, labelled 14.00–20.80 s), sha256 `982a7728…` |

## 2. The in/out points and why

The task asked for "the moment the owner faces the obstacle before the install beat through the first clear payoff", ≈ 5 s. The board's own beat structure (`board.json`) makes the smallest window that contains every required event **6.8 s**, not 5:

| Event | Board / code time | Included because |
|---|---|---|
| Obstacle 5 (complaints swarm) on screen with the owner, before contact | F6 12.6–15.0; contact at `t0+1.5` = **14.1 s** (`health_at` contacts list; `hit_t = 1.5`) | in = **14.0 s** — the last 0.1 s in which the owner is still running *toward* the obstacle (swarm at x ≈ 520, owner at 260); this is "faces the obstacle" |
| Hit, health 1→0, hit flash, `GAME OVER?`, desaturation | 14.1 · 14.2–15.0 | the low point |
| Panel slide, header, typing `INSTALL` / `RENTOK APP` | 15.0–15.5 · 15.8–17.2 | the install beat |
| Phone drop, white flash, colour return, health refill | 17.2–17.6 · 17.6 · 17.6–18.0 (`install_event_t` 17.4) | the transformation |
| `POWER UP!`, aura, test tick, phone in hand | 18.0–19.2 · 18.4–18.9 | the visibly enhanced ability |
| Obstacle 1 re-enters; tick fired; burst; chip flight; chip lands | 19.6 · 19.9 · 20.35 · 20.35–20.7 · **20.7** | the first clear payoff |
| out | **20.8 s** (end of F9.1) | the chip has sat for 0.1 s; F9.2 (the sack) begins at 20.8 |

A 5.0-s cut (15.8→20.8) would start at the typing and drop the obstacle-facing moment and the low point — the two beats Treatment C most needs to re-direct. A 5.0-s cut (14.0→19.0) would drop the first clear. The 6.8-s window is kept; for Treatment D the longest single Veo/Omni clip is 8 s, so the unit still fits one generation. Treatments B, C and D are judged on **the same event list** above, not on matching 6.8 s to the frame.

## 3. Exactly what produced these frames

### 3a. Assets on screen in the window (from `frozen-inputs/`)

| Asset | File (sha256) | On screen | Produced by |
|---|---|---|---|
| Owner — run poses | `gen/assets/owner_runA.png` (`cecde375…`), `owner_runB.png` (`f81439cb…`, D-5 book patch) | 14.0–14.1 (F6 run), 19.6–20.8 (F9.1 run) | att-001, cut by `tools/cutout.py --sheet 4` |
| Owner — idle pose | `gen/assets/owner_idle.png` (`aea606d4…`) | 14.1–19.6 (knocked, panel, power-up) | att-001 |
| Owner — powered (halo) | code: `Sprites.owner(pose, powered=True)` over the same bitmaps | 17.4–20.8 | `render_game.py` |
| Obstacle 5 — complaints swarm | `gen/assets/obst_5.png` (`c6c0a59b…`), drawn at 368×300 | 14.0–15.0 (vanishes at F7) | att-006 |
| Obstacle 1 — document wall | `gen/assets/obst_1.png` (`61d96a8a…`), 345×368 | 19.6–20.35 intact; 20.35–20.7 as debris | att-002 |
| Plate | `gen/assets/plate.png` (`04b0615f…`), fitted, shifted 422 px, tiled ×2 mirrored | whole window (grey 14.2–17.6) | att-007 |
| Wordmark | `rentok-new-logo.webp` (`1ff7dcf5…`) | HUD chip 150×77 throughout; phone screen 56×29 (17.2–17.6) and 44×23 (17.6–19.6) | fetched raster |
| Music bed | `gen/raw/A10_music_att-008.wav` (`8be3e70e…`, not copied) trimmed by `assemble.py` | throughout | att-008 |
| SFX | `gen/sfx-stem.wav` from `tools/sfx.py` | hit 14.1; low 14.2; keys 15.8–17.2 (17 clicks); power-up 17.4; pew 18.4; pew 19.9; burst 20.35; ding 20.7 | code |

### 3b. The prompts behind those assets (verbatim; also in `frozen-inputs/gen/ATTEMPTS.jsonl`)

**att-001 (owner sheet, 21:9):** "A sprite sheet of ONE character in four poses side by side, evenly spaced, same size and same design in every pose: (1) standing idle, (2) running with the left leg forward, (3) running with the right leg forward, (4) jumping with knees up. The character: an ordinary Indian man of about forty, slightly stocky, short black hair, rectangular spectacles, a blue-and-white checked half-sleeve shirt, dark trousers, brown sandals; a big bunch of keys on a ring hangs from his belt; he carries a thick red bound account book under one arm, its cover blank. Full body, facing right, feet on the bottom edge. Flat 16-bit pixel-art game sprite, crisp square pixels, matte colours with no gloss, every shape closed by a 2-pixel dark outline, daylight from the upper left with one hard pixel shadow, on a solid uniform bright green background (#00FF00) with nothing else in frame. No text, no lettering, no numbers, no logos, no watermark anywhere. Original design, not based on any existing video game character."

**att-006 (swarm, 1:1):** "A single game obstacle: a swarm of five angry red speech-bubble shapes with cartoon frowning eyes, each bubble empty except one bold exclamation-mark symbol, flying in a loose cluster with small motion lines. No letters or words inside the bubbles. Flat 16-bit pixel-art game sprite, crisp square pixels, matte colours with no gloss, every shape closed by a 2-pixel dark outline, daylight from the upper left with one hard pixel shadow, on a solid uniform bright green background (#00FF00) with nothing else in frame. No text, no lettering, no numbers, no logos, no watermark anywhere. Original design, not based on any existing video game character."

**att-002 (document wall, 1:1):** "A single game obstacle: a tall wall built from stacked blank white paper sheets and blank folders, slightly leaning, with a faceless grey human silhouette peeking out from behind it and a large bold question-mark symbol floating above. The sheets are blank with no writing. Flat 16-bit pixel-art game sprite, crisp square pixels, matte colours with no gloss, every shape closed by a 2-pixel dark outline, daylight from the upper left with one hard pixel shadow, on a solid uniform bright green background (#00FF00) with nothing else in frame. No text, no lettering, no numbers, no logos, no watermark anywhere. Original design, not based on any existing video game character."

**att-007 (plate, 9:16):** "A vertical 9:16 pixel-art background for a side-scrolling game, Indian city lane: a tall cream-and-terracotta paying-guest building with many stacked floors of small windows and balconies filling the upper two thirds, black water tanks and a TV antenna on the roof, a lower cream building beside it, a pale blue sky with two simple clouds. The bottom fifth is an empty flat packed-earth lane in muted ochre with a low stone kerb, no ground pattern. All building faces and walls are plain and blank — no shop fronts, no boards, no hoardings, no writing of any kind. Flat 16-bit pixel art, crisp square pixels, matte colours, 2-pixel dark outlines, daylight from the upper left. No text, no lettering, no numbers, no logos, no watermark anywhere. Original design, not based on any existing video game."

**att-008 (music):** "Upbeat 8-bit chiptune instrumental, bright square-wave lead melody, driving bass line, punchy electronic drums, 140 bpm, playful and energetic, loop-friendly, no vocals"

### 3c. The render functions and constants that act in the window (`frozen-inputs/tools/render_game.py`)

| t (s) | Function / block | Constants that set what you see |
|---|---|---|
| 14.0–15.0 | obstacle block (`n in OBST_BEATS`, k=5) | `ox = 1080 − tl·400`; `oy = ground_y − 300`; size (368, 300); `hit_t = 1.5` → contact at 14.1; `flash_sprite(alpha=200)` 14.10–14.22 |
| 14.1– | `health_at(t)` | contacts `[3.3, 6.1, 8.6, 11.7, 14.1]` → 0 segments; HUD health in yellow (`hp ≤ 1`) |
| 14.1–15.0 | owner | pose `idle` (`n == "F6" and tl ≥ 1.5`); `knock = 40`; `owner_x = 260`, `owner_h = 260` |
| 14.2–15.0 | `desaturate(cv, (tl − 1.6)/0.8)`; `GAMEOVER` flash | grayscale ramp 0→1 over 0.8 s; blink `int(t·4) % 2` (4 Hz); text scale 8 yellow at y 560 |
| 15.0 | F6→F7 boundary | obstacle no longer drawn (F7 not in `OBST_BEATS`); `camera_x` pauses at 6000 px |
| 15.0–15.5 | cheat panel slide | `py = 520 + (1 − tl/0.5)·500`; panel (105, py)–(848, py+400), fill `#0B0F1E`, cyan border 6 px |
| 15.5–17.2 | header + typing | `CHEAT_HDR` scale 7 white at `py+36`; `nchars = (tl − 0.8)/1.4 · 17` over `CHEAT_1`+`CHEAT_2` (scale 10 cyan at `py+130` / `py+240`) |
| 15.0–17.2 | world | `desaturate(cv, 1.0)`; owner `idle`, no knock |
| 17.2–17.6 | phone drop | `phx = owner_x + 120`; `phy = 200 + (ground_y − 400)·k2`; rect 70×120 brand blue, wordmark 56×29 |
| 17.4 | `powered = t ≥ 17.4` | halo on (`Sprites.owner(..., powered=True)`: 25 pastes of the alpha mask at alpha 110, offsets −6…+6 step 3); sprite offset (−12, +12) |
| 17.2–17.6 | colour return | `desaturate(cv, 1 − (tl − 2.2)/0.4)` |
| 17.6–17.7 | full-frame flash | `rectangle((0,0,W,H), fill=(255,255,255,160))` |
| 17.6–18.0 | panel fade; health refill; phone in hand | `fade = 1 − (tl − 2.6)/0.4`; `min(5, int((t − 17.6)/0.08) + 1)` segments, cyan; phone rect 60×104 at `owner_xy + (sp.width − 30, 60)`, wordmark 44×23 |
| 18.0–19.2 | `POWERUP` flash | scale 8 cyan at y 560, 4 Hz blink |
| 18.0– | HUD phone icon | 30×54 at `hx0 + width + 36` |
| 18.4–18.9 | F8 test tick | `draw_tick(x = owner_x + 150 + (tl − 0.4)·900, y = ground_y − 230 − (tl − 0.4)·300)`; glyph `✓` scale 4 + 1-scale shadow |
| 18.0– | scroll resumes | `camera_x`: 480 px/s from 18.0 |
| 19.6–20.8 | F9.1 obstacle 1 | `ox = 1080 − tl·480`; size (345, 368); `hit_t = 0.75` → 20.35 |
| 19.6–20.0 | label recall | `OBST_1` for `tl < 0.4`, scale 7 yellow at y 720 |
| 19.9–20.35 | projectile | `draw_tick(owner_x + 150 + (tl − 0.3)·900, ground_y − 160)` |
| 20.35–20.7 | `debris(cv, im, ox, oy, kk, seed=1, tiles=6)` | `kk = (tl − 0.75)/0.35`; vx `(i − 2.5)·90 ± 30`, vy `−260 + (j − 3)·40 ± 40`, gravity `900·kk²`, alpha `1 − kk` |
| 20.35–20.7 | chip flight | `CHIP_1` from (clamped ≈ 700 − w/2, 880) to (90, 400) over 0.35 s; scale 6 green, pad 4 |
| 20.7–20.8 | chip seated; `events: chip` | row 0 at (90, 400) |
| 19.6–20.8 | owner | run cycle `runA/runB` at `int(t·8) % 2`; powered halo |
| whole | `draw_ground(cv, camx)` | lane below y 1180; kerb/dashes/tracks/grate/manhole/scooter at 1.3× |
| whole | HUD | `PG OWNER` scale 6 white at (77, 306); health glyphs; wordmark chip (738, 300)–(888, 377) |

SFX in the window (`tools/sfx.py`): `cue_hit` 14.1; `cue_low` 14.2; `cue_key` ×17 at `15.8 + i·(1.4/17)`; `cue_powerup` 17.4 (C5 E5 G5 C6 E6, 90 ms/note); `cue_pew` 18.4 and 19.9; `cue_burst` 20.35; `cue_ding` 20.7. Bed: the Lyria track, −14 LUFS target via `assemble.py` two-pass `loudnorm`, pre-encode true-peak −4 dBTP.

## 4. What the baseline shows (OBSERVED on the 10-fps sheet) — the reference the other treatments are judged against

- 14.0–14.1: owner running, swarm ahead at the same ground line, both ≈ 13–16 % of frame height.
- 14.1–15.0: white silhouette 0.12 s; owner drops to the idle pose offset 40 px; swarm continues sliding left over him; world greys; `GAME OVER?` blinks. The owner's face is unchanged.
- 15.0: swarm gone; panel rising; owner idle in a grey world for 2.2 s while text types.
- 17.2–17.6: a blue rectangle falls past the owner's head; 17.6 the frame whites out 0.1 s; colour returns; halo appears as a thin cyan edge.
- 18.0–19.6: `POWER UP!` blinks; owner stands idle with a blue rectangle at his hand; one small cyan mark rises at 18.4.
- 19.6–20.8: owner runs (two-pose cycle); the wall slides in; a small cyan mark travels to it; the wall becomes 36 falling tiles for 0.35 s; a green string flies to the top-left; done.

This is the frozen Treatment A. Nothing in `treatments/A-baseline/` is to be modified; B, C and D write to their own folders.
