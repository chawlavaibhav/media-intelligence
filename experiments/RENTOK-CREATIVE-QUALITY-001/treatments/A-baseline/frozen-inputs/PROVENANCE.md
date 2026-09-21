# Frozen inputs — provenance

Every file here is a byte-identical copy from the Lane A job directory
`agency/jobs/AGY-2026-09-20-RENTOK-GAME-LANE-A-001/` at job commit
`7dab37a70b004881a1ef9dea465b8aac41e6a979` (branch `work/agency-job-rentok-game-lane-a-001`),
checked out at `/Users/vaibhavchawla/Vaibhav_Personal_Projects/media-intelligence-rentok-lane-a/`.
Copied 2026-09-21 by the investigator session; `SHA256SUMS.txt` lists every file's sha256
(`shasum -a 256 -c SHA256SUMS.txt` verifies). Nothing here may be edited; treatments B/C/D read from
these copies, never from the job tree.

| Path (relative to the job dir) | Role in the baseline sequence (14.0–20.8 s) |
|---|---|
| `board.json` | beats F6 (12.6–15.0), F7 (15.0–18.0), F8 (18.0–19.6), F9.1 (19.6–20.8); `install_event_t` 17.4; `powered_from_t` 17.4 |
| `copy-deck.json` | strings rendered in the window: `OBST_5`, `HUD_HEALTH_0/1..5`, `GAMEOVER`, `CHEAT_HDR`, `CHEAT_1`, `CHEAT_2`, `POWERUP`, `OBST_1`, `CHIP_1`, `HUD_NAME` |
| `gen/ATTEMPTS.jsonl` | the eight paid calls with verbatim prompts |
| `gen/prompts/A1_owner_sheet.txt`, `A2_obst_wall.txt`, `A6_obst_swarm.txt`, `A7_plate.txt` | the prompt files as dispatched (identical text to ATTEMPTS.jsonl) |
| `gen/raw/A1_owner_sheet_att001.png` (sha256 `f1706052…`) | raw owner sheet, att-001 |
| `gen/raw/A6_obst_swarm_att-006.png` (`e9c5ef00…`) | raw swarm, att-006 (obstacle 5, on screen 14.0–15.0) |
| `gen/raw/A2_obst_wall_att-002.png` (`1e52476b…`) | raw document wall, att-002 (obstacle 1, on screen 19.6–20.8) |
| `gen/raw/A7_plate_att-007.png` (`04b0615f…`) | raw 9:16 plate, att-007 (identical bytes to `gen/assets/plate.png`) |
| `gen/assets/owner_idle.png`, `owner_runA.png`, `owner_runB.png`, `owner_jump.png`, `owner_runB_orig.png`, `owner_cutout.json` | keyed cut-outs used by the renderer (`runB` carries the D-5 book patch; `_orig` is the pre-patch pose) |
| `gen/assets/obst_5.png`, `obst_5_cutout.json`, `obst_1.png`, `obst_1_cutout.json` | keyed obstacle cut-outs |
| `gen/assets/plate.png` | the plate as loaded by `Sprites.plate()` |
| `rentok-new-logo.webp` (`1ff7dcf5…`) | the wordmark raster (HUD chip, phone screen) — from `source/rentok-brand/` |
| `tools/render_game.py` (`f9a819f0…`) | the renderer — the animation/compositing instructions |
| `tools/sfx.py` (`d2433705…`) | the SFX synthesis at board times |
| `tools/assemble.py` (`a7113f26…`) | music trim + SFX mix + loudnorm + mux |
| `tools/cutout.py` (`db4f2ae4…`) | the keying that produced `gen/assets/*.png` |
| `tools/pixfont.py` (`31b7a43c…`) | the bitmap font every string and the `✓` projectile glyph are drawn with |
| `tools/prompts.py` (`9aeea4e5…`) | the prompts as data + the prompt guard |

Not copied (not needed for the window, or too large): `gen/raw/A10_music_att-008.wav` (music bed; sha256 `8be3e70e…` in ATTEMPTS.jsonl), `gen/assets/obst_2/3/4.png`, the animatic/final intermediates, `qa/`.

Cross-check against the production-learning case `RENTOK-GAME-A-004` EVIDENCE-MAP (PR #104, not merged): `board.json` sha256 `9be5c767…` and `tools/render_game.py` `f9a819f0…` match the case's recorded values.
