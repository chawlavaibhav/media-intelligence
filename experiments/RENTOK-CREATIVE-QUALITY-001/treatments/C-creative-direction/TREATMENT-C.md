# Treatment C — creative-direction improvement, same renderer topology (AI stills + code)

Experiment `RENTOK-CREATIVE-QUALITY-001`, Phase 2. Produced 2026-09-21. Labels: OBSERVED / INFERRED / PROPOSED.

## 1. Deliverable

| Item | Value |
|---|---|
| Clip | `C-14.0-20.8.mp4` — sha256 `cb91148aa9ccb9e24b2f187dbfa6328dc5e8ad1604f0a9575caccd82ef8d900a` |
| Geometry | 1080×1920, h264 30 fps, **205 video frames = 6.833 s** (frames 420–624, exactly the baseline's), aac 48 kHz stereo 6.845 s; no edit lists (`-use_editlist 0`) |
| Loudness (delivered) | I = −15.1 LUFS, true peak −2.5 dBTP (`job/gen/audio-c-mix.json`) |
| Contact sheets | `CONTACT-SHEET-10fps.png` (sha256 `f524543d…`); the USD-0 animatic `ANIMATIC-CONTACT-SHEET-10fps.png` (`3219be5f…`, from `job/gen/C-animatic.mp4` `e2666b64…`) |
| Assets | baseline four poses, obstacles and plate from `A-baseline/frozen-inputs/` (unchanged) + **one new pose sheet** (§4) |
| Code | `job/tools/render_c.py` (509 lines, sha256 `303dbf3f…`), `job/tools/sfx_c.py`, `job/tools/assemble_c.py`; the frozen `render_game.py` is imported unchanged |

Spend: **USD 0.067** (one draw; the planned repair was not needed). Treatment C reserved 0.067 of the 0.335 maximum.

## 2. The visual-quality objective (from 05 §2a — restated, with its basis)

The customer wrote a power fantasy: a beaten man is handed a power and uses it. The baseline shows the events; the objective is that the viewer **feels** the beating, the gift and the use.

Canon claims used (OBSERVED ids; text re-read in `canon/knowledge/current/**`): `sk_murch_c003_0020` (emotion first, "preserved at all costs" → a stated feeling per beat) · `sk_alt_c003_0014` (camera closer → attention → push-in at the hit and the install) · `sk_alt_c003_0022` (lighting fluctuates with mood → cold low point, bright power state) · `sk_alt_c003_0015` (tonal separation → the swarm stays red in a cold world; the powered owner is the brightest thing in frame) · `sk_conv_c003_0019` (withdrawing sound makes the audience listen → 0.3 s near-silence before the flash) · `sk_hop_sa_0026` (size by importance → the owner is ×1.3 during the low point and the gift) · `sk_whip_0015` (a power granted → visible on the body) · `sk_abcd_0006` (tight framing) · `sk_gote_c003_0004` (each new view reveals something).

GAP (OBSERVED): Canon has nothing on animation principles or game feel. The motion below rests on **named external references used as reasoning, not Canon**: the twelve principles of animation (Thomas & Johnston, *The Illusion of Life*, 1981 — anticipation, follow-through, timing, exaggeration, staging) and the game-feel vocabulary (Swink, *Game Feel*, 2008; Jonasson & Purho, "Juice it or lose it", 2012 — hit-stop, screen shake, impact frames, particles).

**Media Factory / rentok-ad technique applied here (Controller step 4):** "state the intended feeling per beat before writing the instruction" (`rentok-ad/assets/brief.md`, sha256 `fb6bf460…`). Each beat in §3 opens with its feeling; the code was written to that line.

## 3. Executable instructions as built (per beat; feeling first) — OBSERVED in `render_c.py`

| Beat | Feeling | What the code does (function · constants) |
|---|---|---|
| 14.00–14.10 · he sees it coming | dread | run poses with an 8° forward lean (`rotate(-8)`) and a 3-px bob at 4 Hz; at 14.05 the **brace** pose (anticipation); the swarm **dives** on a curve from 260 px above its baseline (`oy = base − 260·(1−k)^1.5`); camera push-in 1.00→1.30 over 0.25 s (`camera()`, ease-out) centred at (owner_x+100, 940); audio: bed ducks, 0.22-s riser |
| 14.10–14.50 · it lands | pain | **hit-stop** 3 frames (`HOLDS`, `world_time()` — the world freezes, the UI keeps time, then the world catches up at 1.25×); one impact frame (85 % white silhouette of the owner) + a 12-point **impact star** at the contact; **screen shake** 10 px decaying over 0.25 s (`SHAKES`); **hurt** pose with knock-back 90 px eased out; 8 dust puffs (`Particles.emit`, gravity 600); the swarm recoils 30 px and bobs; audio: hit + 60-Hz thump, bed cut for 0.1 s then low-passed 800 Hz at −7 dB |
| 14.50–15.00 · down | defeat | **cornered** pose (on one knee); **colour grade** replaces the baseline desaturation: RGB × (0.55, 0.60, 0.75) + 35 % vignette, eased in over 0.9 s (`grade()`, `grade_for()`); the swarm hovers over him, still red (tonal separation); `GAME OVER?` unchanged; camera holds 1.30 |
| 15.00–17.20 · the code | a held breath | the swarm **drifts up and out** 15.0–15.6 (ease-in) instead of vanishing; cornered pose; at 16.8 **cornered_up** (head lifted); panel and typing exactly the baseline's (UI layer); cold grade constant; bed low-passed |
| 17.20–17.60 · the gift | awe | phone falls from y 160 to the hand over 0.2 s (ease-in) with a 3-copy cyan trail and a Gaussian glow (`phone_item`, blur 18); **catch** pose from 17.35; phone lands in the hand at **17.4** (`install_event_t` unchanged), screen lights cyan over 0.2 s; bed at −24 dB from 17.3 (near-silence); at **17.6** a cyan-white **radial flash from the phone** 60→1560 px over 5 frames + one full-white impact frame; camera snaps to 1.00 with a 6-px shake; audio: impact + bass drop + the arpeggio; the bed returns full-band **one semitone up** (`asetrate·1.05946` + `atempo 0.9439`) |
| 17.60–19.60 · the power | rising confidence | **powered** pose (phone forward, half-smile); **aura pulses** alpha 100 ± 40 at 3 Hz and the shirt's blue is shifted toward cyan (`powered_sprite`); 10 cyan sparks orbit for 0.6 s; grade: +10 % lift, cyan cast in highlights — the world after is brighter than the world before; at 18.2 **wind-up**, at 18.4 **fire** with a muzzle flash (0.08 s), recoil 8 px, and the test tick with a 5-copy trail rising at 300 px/s; HUD refill, phone icon, `POWER UP!` unchanged |
| 19.60–20.80 · the first kill | release | run (lean + bob); wind-up 19.8, **fire** 19.9 with muzzle flash and the tick + trail; the wall re-enters at **×1.3** leaning 6° (`rotate(6)`); at **20.35** hit-stop 2 frames, a 2-frame white impact on the wall, **shockwave ring** 20→260 px over 0.2 s, the baseline `debris()` on the larger wall + **14 paper sheets** that rotate and flutter (`kind="sheet"`, gravity 500, drag) + 10 dust puffs, shake 8 px, camera push 1.15 and back over 0.3 s; the chip flies with ease-out and gets a 3-frame **landing pop** (white outline); audio: pew with a 200-Hz body, burst + thump + whoosh, ding |

Everything on the UI layer — every string, scale, backing and position, the panel geometry, the typing rate, the blink rate — is the baseline's, drawn **after** the camera transform, so the layout-log gates measure the same boxes.

## 4. The one paid draw (OBSERVED, `treatments/ATTEMPTS.jsonl` att-006)

| Attempt | Asset | Prompt | USD | Result |
|---|---|---|---|---|
| att-006 | C-A1 pose sheet, 2×4, **16:9** | `job/prompts/C-A1_pose_sheet.txt` — the 05 §2c prompt verbatim (352 words; the only choice made at dispatch was the aspect: 16:9 for a two-row grid, where 05 said "21:9 or 1:1") | 0.067 | ok, 11.8 s, `job/gen/raw/C-A1_pose_sheet_att-006.png` sha256 `0abda641…`, 1376×768 |

Inspection: eight poses in two rows, all present and in the requested order — (1) knocked back, arms up, mouth open, book flying; (2) on one knee, hand on the ground, alarmed; (3) kneeling, head lifted, hopeful; (4) standing, right arm raised, open hand; (5) chest out, plain blue phone forward, confident half-smile; (6) arm drawn back, eyes narrowed; (7) arm punched out, fist, fierce grin, motion lines; (8) braced, jaw set. **Identity vs the baseline sheet: PASS** (same face, spectacles, hair, shirt pattern, trousers, sandals, keys). Book: present in 6 of 8 (flying in 1 by design; absent in 2 — the cornered pose — by omission). No lettering (the phone screen is plain blue). Not a Nintendo cue. Keyable 100 %. The repair draw was **not** used.

Cut-out (USD 0): the frozen `key_out` + a 2×4 grid split by empty rows/columns (`job/gen/assets/c_cutout.json`); one common scale for all eight cells (standing cell 344 px → 260 px), so the kneeling poses stay shorter than the standing ones. Observed difference: the sheet's cells are drawn at ≈ 60 % of the baseline sheet's pixel density, so the C poses have slightly coarser pixels than the baseline run/jump poses at 260 px — visible on a large screen as a small change of "pixel size" when he switches from a run pose to a C pose; not visible at phone size (INFERRED).

## 5. The renderer changes (diff summary; OBSERVED)

`render_c.py` is a new 509-line module that **imports the frozen `render_game.py`** for `DesignTokens`, `Sprites` (plate, obstacle and owner loading), `draw_ground`, `camera_x`, `health_at`, `beat_at`, `put_text`, `text_img`, `debris`, `draw_tick`, `load`, and `pixfont`. Nothing in the frozen file is modified. New functions/classes and their constants:

| Added | Purpose |
|---|---|
| `world_time(t)`, `HOLDS = [(14.1, 3/30), (20.35, 2/30)]`, `CATCHUP_RATE = 1.25` | hit-stop with catch-up (the clip stays 205 frames) |
| `shake_offset(t)`, `SHAKES = [(14.1, 10 px, 0.25 s), (17.6, 6, 0.15), (20.35, 8, 0.2)]` | screen shake |
| `camera(t)`, `apply_camera()` | crop-and-scale of the world layer (NEAREST); push 1.30 at 14.05–14.30, hold to 17.6, snap back, 1.15 pulse at 20.35 |
| `ease_out/ease_in/ease_in_out` | easing |
| `grade()`, `grade_for()`, `vignette_mask()` | per-beat colour grade (cold multiply + vignette; bright lift + cyan highlights) |
| `CSprites.cpose()` (placeholder / sheet), `pose_at(t)` | pose table by time; eight new poses |
| `CSprites.powered_sprite()` | pulsing aura + shirt palette shift |
| `Particles` (dust, sparks, rotating paper sheets) | impact and burst secondary motion |
| `impact_star()`, `ring()`, `muzzle_flash()`, `tick_with_trail()`, `phone_item()` | effect primitives |
| `draw_world()` / `draw_ui()` split; `render()` window loop (frames 420–624) | world/UI layer split; UI boxes logged per frame as the baseline does |
| `sfx_c.py`: `cue_thump`, `cue_riser`, `cue_whoosh`, `cue_bassdrop`, `cue_impact`, `cue_sparks`; the pew gains a 200-Hz layer | audio weight |
| `assemble_c.py`: bed cut 0.1 s at the hit-stop, low-pass 800 Hz at −7 dB to the flash, −24 dB for 0.3 s before it, +1 semitone after; the frozen two-pass loudnorm and mux flags | audio progression |

Board (`board.json`), copy deck, obstacle motion timings (`hit_t` at F6+1.5 and F9.1+0.75), install time and chip time are unchanged.

## 6. The USD-0 animatic and my own feel judgement (before the draw; OBSERVED on `ANIMATIC-CONTACT-SHEET-10fps.png`)

Rendered with placeholder poses (baseline bitmaps rotated/squashed, marked with a magenta dot). Against the 06 rubric, judged by the producer (not an evaluator's score):
- Q4 motion: the hit now *lands* — the freeze, the star, the silhouette, the shake and the dust all read on the strip; the burst has a ring and flying sheets; the chip pops. Anticipation was not judgeable (the brace stand-in is the idle bitmap) — that is what the sheet was for.
- Q5 world: the low point is visibly darker and colder and the power state brighter; the swarm no longer vanishes.
- Q3 expression: not judgeable on stand-ins (by design of the animatic).
- Q6 readability: the ×1.30 push keeps every string inside its box (UI drawn after the transform); the play band is larger on screen.
Decision: proceed to the one paid draw. After the draw, one framing correction (USD 0): the camera centre moved from y 1050 to y 940 so the raised catching hand and the phone sit just below the panel's bottom edge instead of behind it.

## 7. What the renderer could NOT realise (documented, not weakened; OBSERVED on the final frames)

1. **Secondary motion on the body** — keys, shirt, hair do not move on impact; the drawn hurt pose is one frame. Only a video model or more drawn frames would give this.
2. **Physical contact** — the swarm hovers *over* him and the papers fly *from* the wall; there is no frame where the creatures are *on* him or the sheets *over* him. Overlap + hit-stop + shake stand in for contact.
3. **Continuous facial change** — the face moves between discrete drawn states (alarmed → hopeful → confident → fierce); there is no in-between.
4. **Depth on the camera push** — the crop-and-scale zoom enlarges the plate and the sprite alike; no parallax change (no second plate was drawn; the optional USD 0.067 was not spent).
5. **The raised catching arm is still partly behind the cheat panel** for 0.25 s (the panel's geometry is UI, held fixed; the camera fix exposes the hand and the phone, not the whole arm).
6. **Squash-and-stretch** — not attempted on pixel art at 260 px (it breaks the pixel grid); anticipation and follow-through poses are used instead.
7. **Pixel-density mismatch** between the baseline poses and the new sheet's cells (§4).

## 8. Honest statement

Treatment C changes two things at once — the direction (a feeling per beat, framing, light, impact, effects, sound) and the renderer that carries it — on top of the same assets, plus one drawn sheet. It therefore cannot separate "better direction" from "better renderer"; it tests whether the *same production topology* (AI stills + code) can reach the objective when both are supplied. The prompt step is the same as the baseline's for every reused asset. Whether the result is better is for the blind evaluation.

## 9. Files

`job/tools/render_c.py`, `sfx_c.py`, `assemble_c.py` (+ frozen copies of `render_game.py`, `pixfont.py`, `cutout.py`) · `job/prompts/C-A1_pose_sheet.txt` · `job/gen/raw/C-A1_pose_sheet_att-006.png` · `job/gen/assets/c_*.png`, `c_cutout.json` · `job/gen/C-animatic.mp4` (USD-0 animatic, video only) · `job/gen/C-sheet-v1.mp4` (first render, camera at y 1050), `C-sheet-v2.mp4` (final video) · `job/gen/*-layout.jsonl`, `*-events.json` · `job/gen/sfx-c-stem.wav`, `audio-c-raw.wav`, `audio-c-mix.wav`, `audio-c-mix.json` · `C-14.0-20.8.mp4` · `CONTACT-SHEET-10fps.png` · `ANIMATIC-CONTACT-SHEET-10fps.png`.
