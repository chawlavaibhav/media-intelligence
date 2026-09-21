# Treatment B — asset-prompt improvement only (everything else frozen)

Experiment `RENTOK-CREATIVE-QUALITY-001`, Phase 2. Produced 2026-09-21. Labels: OBSERVED / INFERRED.

## 1. What was held fixed (OBSERVED)

`job/` is a job-shaped directory built only from the frozen inputs: `tools/render_game.py` (sha256 `f9a819f0…`, byte-identical to Lane A @ 7dab37a), `tools/pixfont.py`, `tools/cutout.py`, `board.json`, `copy-deck.json`, the wordmark raster; the baseline assets `obst_2/3/4.png` (unchanged, used only outside the window). Model `nano-banana-2` (gemini_api, USD 0.067), aspects 21:9 / 9:16 / 1:1 as the baseline, one draw per asset (+ the one planned repair for the sheet), the same `key_out` keying, the same 900-frame render command, the same `-c copy` cut at the 14.0-s keyframe, and **the baseline's audio track muxed unchanged** (`-map 1:a -c copy` from `A-baseline-14.0-20.8.mp4`). No constant, timing or compositing line was changed.

## 2. Deliverable

| Item | Value |
|---|---|
| Clip | `B-14.0-20.8.mp4` — sha256 `31a1266aaf6d95ac0781ec339edca6bf4af6b22ec2be332e4b457308cfc55054` |
| Geometry | 1080×1920, h264 30 fps, 206 video frames (6.867 s — one frame more than A's 205 because the fresh encode's last packet boundary fell one frame later; audio 6.800 s identical bytes to A) |
| Contact sheet | `CONTACT-SHEET-10fps.png` (sha256 `0dd705e8…`); comparison `A-vs-B-frames.png` (A top row, B bottom row at +0.05 / 0.5 / 3.5 / 4.5 / 6.0 / 6.45 s) |
| Full render kept | `job/gen/B-full.mp4` (30 s, video only; the source of the cut) |

## 3. Draws (OBSERVED, `treatments/ATTEMPTS.jsonl` / `LEDGER.jsonl`)

| Attempt | Asset | Prompt file | USD | Result | Inspection against the plan's criteria |
|---|---|---|---|---|---|
| att-001 | B-A1 owner sheet (21:9) | `job/prompts/B-A1_owner_sheet.txt` — the 05 §1b prompt verbatim | 0.067 | ok, 12.6 s, `job/gen/raw/B-A1_owner_sheet_att-001.png` sha256 `699d3313…` | (1) four poses read as one man — same face, spectacles, shirt, keys, sandals: PASS; (2) keys on the belt in all four and the red book under the left arm in all four: PASS (the baseline hid the book in run-B); (3) no lettering: PASS; (4) border keyable 99.96 %: PASS; (5) no Nintendo cue: PASS; (6) expression reads at 260 px — lowered brows and a set mouth in idle/run, an open grin in the jump: PASS. Two shortfalls: the two run poses differ **less** than the baseline's (legs differ over 22 % of their union pixels vs 34 % for the baseline pair — the model repeated the leg phase), and the poses sit 15–19 px apart so the frozen `split_sheet` (which merges gaps < 2 % of width) found 2 poses, not 4. **Selected.** |
| att-002 | B-A1 owner sheet — repair | `job/prompts/B-A1_owner_sheet_repair.txt` — two recorded edits: "evenly spaced **with a wide gap of empty green at least half a character wide between neighbouring poses**", and the run poses re-worded "the left leg stretched far forward and the right leg trailing far behind, both feet off the ground" / mirror for pose 3 | 0.067 | ok, 11.5 s, `…att-002.png` sha256 `6d859164…` | Identity/props/lettering/keyable (100 %)/IP: PASS. Run distinctness **worse** (legs 14.8 %); gaps still merged by the splitter; the idle lost the wide braced stance. **Not selected** (recorded as `not_selected`, a counted attempt). Directional model observation, n = 2 here + Lane B's "run ×4 near-identical": Nano Banana 2 does not reliably produce two distinct leg phases from a text description; `routing_authority: none`. |
| att-003 | B-A7 plate (9:16) | `job/prompts/B-A7_plate.txt` verbatim | 0.067 | ok, `…att-003.png` sha256 `acf39dfa…` | Facade, water tanks, antenna, laundry line, pole with wires, neem tree, parked auto, closed shutters, late-afternoon light: all present; **no lettering** on shutters, walls, laundry or the auto (checked at 1:1); lane at the bottom. PASS. Used as `plate.png` directly (as the baseline did). |
| att-004 | B-A6 swarm (1:1) | `job/prompts/B-A6_swarm.txt` verbatim | 0.067 | ok, `…att-004.png` sha256 `36771616…` | five red bubbles in a diving wedge, lead bubble largest, bared teeth, motion lines; symbols `!` only. PASS; keyable 100 %. |
| att-005 | B-A2 wall (1:1) | `job/prompts/B-A2_wall.txt` verbatim | 0.067 | ok, `…att-005.png` sha256 `20d4f2a8…` | leaning, bulging stack with sheets lifting off, silhouette behind, `?` above; no writing. PASS; keyable 100 %. |

**Treatment B spend: USD 0.335 reserved of the 0.402 maximum (5 draws, 5 ok, 0 failed, 1 repair).** Prompt-guard passes on all five (no IP word, no copy-deck string, no-lettering clause present).

Cut-out (recorded deviation at the cut-out layer, USD 0): `job/gen/assets-B/owner_*.png` were split from att-001 at the four measured empty-column gaps (31–361, 396–800, 815–1202, 1221–1554) with the frozen `key_out`, because the frozen splitter's gap threshold merged them — the same kind of cut-out-layer fix Lane A recorded as R3. `obst_1` and `obst_5` were keyed by the frozen `cutout.py` unchanged.

## 4. The prompt diff, old → new (OBSERVED; full texts in `job/prompts/` and `treatments/ATTEMPTS.jsonl`)

**Owner sheet.** Baseline: "(1) standing idle, (2) running with the left leg forward, (3) running with the right leg forward, (4) jumping with knees up. The character: an ordinary Indian man of about forty, slightly stocky, short black hair, rectangular spectacles, a blue-and-white checked half-sleeve shirt, dark trousers, brown sandals; a big bunch of keys on a ring hangs from his belt; he carries a thick red bound account book under one arm, its cover blank. Full body, facing right, feet on the bottom edge." → B: "(1) standing braced and determined — feet planted wide, weight slightly back, both fists clenched at hip height, shoulders squared, jaw set, brows lowered, eyes fixed ahead; (2) running hard with the left leg forward — torso leaning forward about fifteen degrees, right arm punched forward, left arm swung back, mouth set in a grim line; (3) … the same forward lean, arms in the opposite swing; (4) jumping with knees pulled up and both arms raised, a broad open-mouthed grin. The character: … thick expressive eyebrows … keys … swings with his motion; he carries a thick red bound account book under his left arm in every pose … the head about one fifth of the body height so the face reads at small sizes." Style block and exclusions: identical.

**Plate.** Baseline: facade + "a lower cream building beside it" + clouds + "an empty flat packed-earth lane". → B adds "late afternoon", "iron balconies", "one rooftop with drying laundry", "in the middle distance a row of low shop-house fronts with closed shutters, a leaning electricity pole with looped wires, a small neem tree and a parked yellow auto-rickshaw seen from the side", "long soft-edged afternoon shadows". Exclusions: identical plus "no shop fronts with writing".

**Swarm.** "flying in a loose cluster with small motion lines" → "diving down and to the left in a tight wedge, the lead bubble largest and closest, each with cartoon furrowed eyes and bared teeth … trailing short motion lines".

**Wall.** "slightly leaning" → "leaning toward the viewer's left and bulging as if about to burst, a few loose sheets already lifting off the top".

## 5. What changed in the frames, and what did not (OBSERVED on `A-vs-B-frames.png` and the 10-fps sheet)

Changed:
- **The owner's face.** Lowered brows and a set mouth in every frame of the window (14.0–20.8); the baseline's face is neutral throughout. At 360-px preview the frown is visible on the idle pose (3.5 s, 4.5 s frames) and on the run.
- **The world.** A middle-distance row of shuttered shop fronts, an electricity pole with wires, a neem tree, a laundry line and a parked auto now scroll at the plate's 0.25× rate; the light is warmer (late afternoon). The frame reads as a place rather than one repeating facade.
- **The swarm** enters as a diving wedge with a large lead bubble (frame +0.05 s) — the still carries the dive the code does not animate.
- **The wall** is a leaning, bulging stack with sheets already lifting (frame +6.0 s).
- **The book** no longer flickers (present in all four poses by prompt, so the D-5 patch is moot).

Did not change (and could not, by design):
- **Every motion, timing and effect**: the swarm still slides in a straight line and vanishes at 15.0 s; the hit is still a 0.12-s silhouette and a 60-px offset; the two-frame run cycle now alternates two *less different* drawings; the projectile, burst, chip flight, halo and flash are byte-for-byte the same code. The B owner's brows are lowered at GAME OVER? and equally lowered at POWER UP! — one expression serves both, exactly the ceiling stated in 05 §1a.
- **Framing/scale**: owner 260 px, same camera.
- **A frozen-code side effect**: `Sprites.plate()` shifts the plate up by a hard-coded 422 px measured on the *baseline* plate (lane edge at y 1602 after fitting); the B plate's lane edge is at ≈ 1500, so ≈ 100 px of the plate's own pavement and road show as a strip between the shop fronts and the code ground line at y 1180 (visible in every gameplay frame as a beige/grey band with the yellow kerb dashes below it). INFERRED: it reads as a pavement, not as an error, but it is a mismatch the frozen constant cannot fix; a one-number change (`shift = 1500 − 1180`) would align it, and B does not allow that change.
- **Text, HUD, safe box**: unchanged strings and boxes (the renderer's layout log is asset-independent), so the DET gates of the baseline apply unchanged.

## 6. Honest statement

Treatment B cannot show any animation improvement: the renderer, its constants, the board and the audio are frozen, so everything that moves in B moves exactly as in A. B tests only whether the *pictures* the same code moves can carry more of the plan's intent when the prompts ask for it. What it shows (INFERRED): a stronger face, a richer world and more threatening obstacle stills do reach the film through the prompt step; the one thing the prompt cannot buy is a second expression state (the idle serves both defeat and power) or any change of motion. Whether the picture gain matters to a viewer is for the blind evaluation (06), not for this file.

## 7. Files

`job/prompts/*.txt` (the five prompts as sent) · `job/gen/raw/*.png` (five draws) · `job/gen/assets-B/` (keyed cut-outs + `owner_cutout.json`) · `job/gen/B-full.mp4` · `job/gen/B-full-layout.jsonl`, `B-full-events.json` (renderer logs) · `B-14.0-20.8.mp4` · `CONTACT-SHEET-10fps.png` · `A-vs-B-frames.png`.
