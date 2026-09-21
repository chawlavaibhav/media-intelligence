# 01 — Production chain reconstruction (Lane A in full, Lane B in brief)

Experiment `RENTOK-CREATIVE-QUALITY-001`, Phase 1 (USD 0). Written 2026-09-21 by the investigator session.
Labels: **OBSERVED** = read from the named file or measured on the named frame · **INFERRED** = this session's reading · **UNKNOWN** = not in the record.

Purpose of this file: lay the actual chain out end to end — what the customer said, what the plan decided, what was sent to the image model, what the animation code does with it, and what the film shows — so that `02-LOSS-OF-INTENT-TRACE.md` can say, decision by decision, where creative intent was kept, simplified or lost.

Three kinds of "prompt" are kept strictly apart throughout:

| Kind | What it is in this job | Where it lives |
|---|---|---|
| **Asset-generation prompt** | text sent to Nano Banana 2 (7 stills) and Lyria (1 music bed) | `gen/ATTEMPTS.jsonl` (verbatim in §6) |
| **Animation / compositing instruction** | the Python that places, moves, hits, bursts and composites those stills, plus its constants | `tools/render_game.py`, `tools/sfx.py`, `tools/assemble.py` (§7) |
| **Video-model prompt** | none — no generative video route was called in either lane | — (OBSERVED: no `veo`/`omni`/`kling` row in either ATTEMPTS.jsonl) |

Sources (read-only): Lane A job `AGY-2026-09-20-RENTOK-GAME-LANE-A-001` at commit `7dab37a70b004881a1ef9dea465b8aac41e6a979` in `/Users/vaibhavchawla/Vaibhav_Personal_Projects/media-intelligence-rentok-lane-a/agency/jobs/AGY-2026-09-20-RENTOK-GAME-LANE-A-001/` (hereafter `A/`); Lane B job `AGY-2026-09-20-RENTOK-GAME-LANE-B-001` in `…/media-intelligence-rentok-lane-b/agency/jobs/AGY-2026-09-20-RENTOK-GAME-LANE-B-001/` (hereafter `B/`). Final files verified by sha256: Lane A `9d50c4c5729f32d198fbaafc642fd78eccc0ee11dee2131cb637270584b5e24a` (30.000 s video / 30.021 s container, 1080×1920, h264+aac); Lane B `40cf2f40bf50c88d04afebb98ea91f6896a83aac8ad4fbdc010b0e289eb42c78`.

---

## 1. The customer's words (OBSERVED, `A/input/01-CUSTOMER-BRIEF-FROZEN.md`)

Original request, verbatim:

> "I want to make a video for RentOK. The video has a Mario game. The player is basically a PG owner. The obstacles in the game are basically the problems that owner faces — tenant verification, collecting rent, tenants leaving without paying rent, no place to do reconciliation, solving complaints and so on. The game also introduces a cheat code — install RentOK app. Once it is done, Mario gets a gun sort of power/immunity. It runs and kills all the obstacles and gets the flag."

Confirmed answers: Reels/Facebook/Shorts · 30 s · "An original Mario-inspired game, rather than an exact reproduction" · visual treatment **delegated** · power-up design **delegated** "while preserving the requested game-style power/immunity mechanic" · source = rentok.com.

Intent block (binding): "should feel like an actual platform game, not a conventional promotional video with gaming graphics placed over it" · owner recognisable · obstacles = genuine problems · install = central turning point · "visibly enhanced ability, use it to overcome the obstacles, and reach the finishing flag" · no guarantee claims.

Every creative-quality word the customer used: **"Mario game"**, **"cheat code"**, **"gun sort of power/immunity"**, **"runs and kills all the obstacles"**, **"gets the flag"**, **"feel like an actual platform game"**. INFERRED: the brief carries the *mechanics* of the fantasy (power, immunity, killing, flag) and one *feel* word ("actual platform game"); it carries no words about art quality, expression, drama or spectacle — those were delegated.

The later judgement this experiment is testing — "technically correct, not exceptional" — comes from the Controller's brief to this experiment (customer words relayed in chat); it is not in any committed file. UNKNOWN: the customer's exact wording beyond that phrase.

---

## 2. Stage 1 — how the words became requirements (OBSERVED, `A/stages/01-INTENT.md`)

| Stage-1 item | What it fixed | Creative content carried forward |
|---|---|---|
| M1 (A1) platform game | "side-scrolling level, a player character, obstacles, HUD elements and a finishing flag, and that the game is the film rather than an overlay" | the *furniture* of a game; nothing about how the game should feel to watch |
| M2 (A2) PG owner | cues: "a keyring, a 'PG' cap/badge, a rent register" at the hero frame | identity props |
| M3 (A3) obstacles | "five obstacle labels present … each of the five identifiable by picture + label" | picture-says-the-problem test |
| M4 (A4) install | "the film's state changes visibly at that frame"; string "INSTALL RENTOK" byte-present | a state change |
| M5 (A5) power | "a visible change of the character (glow/aura/projectile) and that the change is used, not decorative" | glow/aura/projectile named here for the first time |
| M6 (A6) clears + flag | "counts obstacles cleared … sees the flag reached" | count and presence |
| 1.6 tone | "retro-arcade playful; the joke is on the problems, never on the owner; the close is calm and clear" | tone in one line; example given = the request itself |
| G1 (generated question) | "broken by: cutting to non-game footage, camera moves a game would never make, photoreal rendering" → "code/procedural (Pillow + ffmpeg) with generative stills only for sprites/backgrounds" | **the production method is chosen inside Stage 1** (INFERRED: before any creative package existed) |
| G5 | powered state = "sprite change (aura/colour) + projectile + obstacles no longer hurt … a second character sheet (powered)" | later replaced by a code recolour (Stage 4 A1p) |
| D3 (assumption) | "Retro-arcade playful tone; original pixel-art look … creative-direction repair … the most expensive kind" | look chosen; mitigated by drawing the character first |

INFERRED: Stage 1 translated every customer sentence into a *presence* check (is there a flag? is there an aura?) and none into a *quality* target (how hard does the hit land? how does the owner feel at GAME OVER?). That is what the acceptance contract asked for (A1–A11 are presence/compliance items; §B "creative quality" is one sentence judged by the customer).

---

## 3. Canon claims retrieved (OBSERVED, `A/stages/03-CREATIVE.md` Part A2; ids re-verified in `canon/knowledge/current/**` of this worktree)

Lane A retrieved 33 accepted claims and 21 compiled check lines. The ones that shaped creative decisions, with the claim text as Canon holds it (re-read by this session; abridged only by cutting sentences):

| id | Claim (Canon text) | Lane A used it for |
|---|---|---|
| `sk_abcd_0006` | "'Jump in' asks the ad to reach the heart of its story sooner … pacing that keeps the viewer engaged, and tight framing" | F1 opens mid-run |
| `sk_abcd_0007` | "beginning in the middle of the action, and opening on a close-up … not as a required opening" | F1 |
| `sk_whip_0011` | "a brand story requires an opposing force, and that most briefs remove it" | five problems unsoftened before the solution |
| `sk_sb_c003_0008` | "The customer occupies the hero role and the brand occupies the guide role" | owner = player; RentOk = power granted |
| `sk_whip_0015` | "the brand is the archetype the hero meets — the figure who teaches a lesson or grants a power before the hero returns transformed" | same |
| `sk_hea_mts_0009` | "mastery of exclusion and relentless prioritisation" | one mechanic, one power |
| `sk_hea_mts_0018` | stories as "a kind of mental flight simulator" | the clearing run rehearses problem→app→cleared five times |
| `sk_hop_sa_0026` | "A picture in an advertisement must be a salesman in itself and earn the space it occupies" | the hero frame F9.2 |
| `sk_hop_sa_0014` | "planned and written to one imagined typical buyer" | the owner is a specific man |
| `sk_ms_c003_0019` | "repeatedly shifting focus … does not guide attention, it confuses" | one moving cue per beat (CA-D1) |
| `sk_gote_c003_0004` | "Each shot cut to must give the viewer information it did not already have" | one new element per beat |
| `sk_murch_c003_0019` / `_0020` | six ranked cut criteria; "Emotion is the first criterion, weighted … at 51 percent … preserved at all costs" | the GAME OVER? low point held 0.8 s |
| `sk_wcag_0001/0002`, `sk_sam_c003_0021` | contrast ≥ 4.5:1; text over image needs contrast | label backing bands |
| `sk_vig_c003_0013` | identity is "an overall system approach, not just a logo" | wordmark placed as raster |
| `sk_ogl_c003_0014` | "make the product itself the hero" | product = the power-up |

Gaps Lane A recorded honestly (OBSERVED, Part A2): "**no accepted Canon on** game/arcade grammar, pixel-art readability, or chiptune sound"; audio has zero accepted Canon. This session re-searched `canon/knowledge/current/**` for *squash, anticipation, follow-through, hit-stop, game feel, screen shake, platformer, pixel art, arcade*: the only hits are "anticipation" in the photographic decisive-moment sense (`carroll-read-this-photographs`) and "animation" in unrelated senses. **The gap is confirmed: Canon holds nothing on animation principles or game feel.**

INFERRED: every Canon claim above governs *advertising structure* (open fast, brand early, hero/guide, one idea, ask at the end). None governs *how motion should feel*. Lane A's creative package is therefore well-founded as an ad and unfounded — by Canon — as an animation. Lane A said as much.

---

## 4. Stage 3 — the creative decisions (OBSERVED, `A/stages/03-CREATIVE.md` Part B)

**Proposition (3.1):** "Running a PG is a platform game where every level is the same five problems — and installing the RentOk app is the cheat code that turns the owner into the one who clears them."

**Player:** HUD name `PG OWNER`; props "a bunch of keys on a ring at the belt and a rent register / ledger book under the arm"; "an adult Indian man of ~40, slightly stocky, ordinary"; checked half-sleeve shirt, dark trousers, rectangular spectacles, chappals. **No expression is specified anywhere in the package** (OBSERVED: the words *face, expression, worried, angry, triumphant, smile* do not occur in Part B).

**World:** "sky gradient … a tall PG building facade with stacked floors … rooftops/water tanks … a lane"; ground at y 1130 (later 1180); parallax 0.25×; scroll 320→480 px/s (later 400→480); palette fixed; brand colours "reserved for the app/power/labels/chips so the brand colours mean 'the solution'".

**Obstacles (five):** document wall + silhouette + "?"; "a heavy cloth money sack with a padlock and chain, **hopping** away"; fleeing tenant with suitcase and coin bag; "a **toppling** tower of ledgers"; "a **swarm** of angry red speech-bubble tickets".

**Gameplay mechanics (verbatim):** "Problem half: the owner runs and jumps (jump arc 0.5 s, code); each obstacle either blocks (1, 4), hits (2, 5) or escapes (3); each contact costs one health segment (5 → 0) with a white hit-flash and a knock-back of 60 px. Clearing half: the owner runs faster, is immune … and fires cyan tick projectiles (one per 0.4 s, 26 px, 900 px/s) that burst each obstacle into pixel debris; the burst spawns the green chip which flies to the checklist. Flag: a jump at the pole, the flag rises 0.8 s."

**Turning point (F7):** "At health 0 the world desaturates and `GAME OVER?` flashes (0.8 s). A dark arcade panel … the two lines type in letter by letter with key-click SFX (1.4 s) … a RentOk-blue phone item drops into the owner's hand (0.4 s), the screen shows the wordmark, a white flash, colour returns, health refills to five in cyan."

**Power-up:** "(a) a pulsing cyan aura (code: 2-px outline + 40 % alpha halo) — the visible change (M5); (b) projectile — cyan tick marks …; (c) immunity … Rendered by code from the base sprite (palette shift + aura), so the character cannot drift between 'before' and 'after'."

**Per-beat pictures (board Part D, the beats that matter for the trace):** F2 "the owner runs into it, bounces back, white hit-flash"; F3 "he jumps, clips it, knock-back"; F4 "the owner reaches out, trips"; F5 "topples onto him; he is half-buried"; F6 "dives at him; he sits down; the world desaturates"; F8 "The owner stands, cyan aura pulses around him, he fires one test tick upward-right"; F9.1 "a tick projectile bursts the document wall into pixels; a green chip flies"; F9.2 HERO at 21.40 s "the app-powered owner blasting the rent problem"; F9.4 "blasted into one neat stack/screen"; F9.5 "ticks turn each red bubble green"; F10 "the owner jumps, grabs the pole … pixel confetti".

**Hold logic (3.12):** 2.8 s per obstacle (enter 0.6, contact 0.4, label ≥ 1.2, exit 0.6); 1.2 s per clear; 3.0 s turning point.

**Audio:** chiptune bed (Lyria) + nine code-synthesised cues; no voice.

**Checker at Gate 3 (OBSERVED, `A/stages/CHECK-GATES-1-4.md` Q13):** "the first half is an auto-runner where the owner loses to every obstacle on cue — closer to an 'endless runner' than to a jump-over-enemies platformer; only three jumps in 30 s … Whether it *feels* like a game is exactly what the USD-0 animatic exists to test."

### 4a. The board, F1–F15 (OBSERVED, `A/board.json` @ 7dab37a, sha256 `9be5c767…`)

| Frame | t0–t1 | Beat (board `beat` field) | Mandatory |
|---|---|---|---|
| F1 | 0.00–1.80 | cold_open_mid_action | M1, M2 |
| F2 | 1.80–4.60 | obstacle_1_tenant_verification | M3 |
| F3 | 4.60–7.40 | obstacle_2_collecting_rent | M3 |
| F4 | 7.40–10.20 | obstacle_3_left_without_paying | M3 |
| F5 | 10.20–12.60 | obstacle_4_no_reconciliation | M3 |
| F6 | 12.60–15.00 | obstacle_5_complaints_game_over | M3 |
| F7 | 15.00–18.00 | cheat_code_install_rentok_turning_point (install_event_t 17.4) | M4 |
| F8 | 18.00–19.60 | power_up (powered_from_t 17.4) | M5 |
| F9.1 | 19.60–20.80 | clear_1_verification | M6, M10 |
| F9.2 | 20.80–22.00 | clear_2_rent (HERO FRAME at 21.4 s) | M6, M10 |
| F9.3 | 22.00–23.20 | clear_3 … TAGGED_not_stopped | M6, M10 |
| F9.4 | 23.20–24.40 | clear_4_reconciliation | M6, M10 |
| F9.5 | 24.40–25.60 | clear_5_complaints | M6, M10 |
| F10 | 25.60–27.60 | flag_level_clear (flag_reached_t 26.6; checklist fades 26.6–27.0) | M6 |
| F11 | 27.60–30.00 | end_card_brand_cta | M10 |

The board is a *timeline of beats and strings*. OBSERVED: it carries no field for pose, expression, motion curve, impact or effect — those exist only as prose in `03-CREATIVE.md` Part B/D and then as code.

---

## 5. Stage 4 — production choices (OBSERVED, `A/stages/04-PRODUCTION-PLAN.md`)

Approach in the plan's own three lines: (1) "a 2-D side-scroller **rendered by code** (Pillow frames → ffmpeg)"; (2) generative models supply "only **textless stills**: one PG-owner sprite sheet, five obstacle sprites, one background plate (Nano Banana 2)"; (3) Lyria bed + code SFX, no voice.

Why not generative video (verbatim): "(a) one character identical across 30 s, (b) readable in-game text on every frame, (c) obstacles physically hit by projectiles at exact times, (d) 30.0 s exactly. Every video route in the table is 4–15 s per clip, identity across clips is a directional risk … and in-motion text is the defect the packs guard against."

Riskiest element (4.1): the sprite sheet, tested first for USD 0.067. Take strategy: **one draw per asset** (1 + 5 + 1 + 1 = 8 calls; repair round budgeted but unused). References: **none** ("A1 (sprite sheet): no reference image — text prompt only"; obstacles text-only "sharing the palette and outline words"). Route: IMG-CORE/nano-banana-2 (clean_observed, use=True, 7/8) via the Gemini API endpoint `gemini-3.1-flash-image`.

Spend (OBSERVED, `gen/LEDGER.jsonl`/`ATTEMPTS.jsonl`): 8 calls, 8 ok, USD 0.529 reserved, 0 repairs, 0 rejected draws.

INFERRED: Stage 4 optimised the four things code guarantees (identity, exact text, exact timing, exact duration). It did not list — and the acceptance contract did not ask it to list — the things code *cannot* supply without being written: expressive poses, secondary motion, impact. The method was chosen for its guarantees, and its ceiling was never stated as a cost.

---

## 6. The eight asset-generation prompts — verbatim (OBSERVED, `A/gen/ATTEMPTS.jsonl`, sha256 `406e38c9…`)

Every image call: `route_cell: nano-banana-2`, `endpoint: gemini-3.1-flash-image`, `surface: gemini_api`, `pool: credits`, `unit_price_usd: 0.067`, `reference_images: []`, `verdict: accepted`, `is_repair: false`.

**att-001 · A1_owner_sheet · aspect 21:9 · artifact `gen/raw/A1_owner_sheet_att001.png` sha256 `f1706052…`**
> A sprite sheet of ONE character in four poses side by side, evenly spaced, same size and same design in every pose: (1) standing idle, (2) running with the left leg forward, (3) running with the right leg forward, (4) jumping with knees up. The character: an ordinary Indian man of about forty, slightly stocky, short black hair, rectangular spectacles, a blue-and-white checked half-sleeve shirt, dark trousers, brown sandals; a big bunch of keys on a ring hangs from his belt; he carries a thick red bound account book under one arm, its cover blank. Full body, facing right, feet on the bottom edge. Flat 16-bit pixel-art game sprite, crisp square pixels, matte colours with no gloss, every shape closed by a 2-pixel dark outline, daylight from the upper left with one hard pixel shadow, on a solid uniform bright green background (#00FF00) with nothing else in frame. No text, no lettering, no numbers, no logos, no watermark anywhere. Original design, not based on any existing video game character.

**att-002 · A2_obst_wall · 1:1 · `A2_obst_wall_att-002.png` `1e52476b…`**
> A single game obstacle: a tall wall built from stacked blank white paper sheets and blank folders, slightly leaning, with a faceless grey human silhouette peeking out from behind it and a large bold question-mark symbol floating above. The sheets are blank with no writing. Flat 16-bit pixel-art game sprite, crisp square pixels, matte colours with no gloss, every shape closed by a 2-pixel dark outline, daylight from the upper left with one hard pixel shadow, on a solid uniform bright green background (#00FF00) with nothing else in frame. No text, no lettering, no numbers, no logos, no watermark anywhere. Original design, not based on any existing video game character.

**att-003 · A3_obst_sack · 1:1 · `A3_obst_sack_att-003.png` `7d56cfdc…`**
> A single game obstacle: a heavy brown cloth money sack tied at the neck, wrapped in a thick grey chain with a big padlock in front, a mean squinting face on the sack, mid-hop with a small pixel shadow beneath. No symbols or writing on the sack. Flat 16-bit pixel-art game sprite, crisp square pixels, matte colours with no gloss, every shape closed by a 2-pixel dark outline, daylight from the upper left with one hard pixel shadow, on a solid uniform bright green background (#00FF00) with nothing else in frame. No text, no lettering, no numbers, no logos, no watermark anywhere. Original design, not based on any existing video game character.

**att-004 · A4_obst_tenant · 1:1 · `A4_obst_tenant_att-004.png` `5165b2d6…`**
> A single game character: a young man in a hoodie and jeans sprinting to the right in a running pose, dragging a rolling suitcase behind him with one hand and clutching a bulging cloth coin bag to his chest with the other, looking back over his shoulder. Full body, feet on the bottom edge. Flat 16-bit pixel-art game sprite, crisp square pixels, matte colours with no gloss, every shape closed by a 2-pixel dark outline, daylight from the upper left with one hard pixel shadow, on a solid uniform bright green background (#00FF00) with nothing else in frame. No text, no lettering, no numbers, no logos, no watermark anywhere. Original design, not based on any existing video game character.

**att-005 · A5_obst_tower · 1:1 · `A5_obst_tower_att-005.png` `19550e25…`**
> A single game obstacle: a precarious toppling tower of thick bound account books, loose blank paper sheets and a chunky pocket calculator with a blank display, stacked crookedly and about to fall to the left; a few sheets fluttering. All pages blank, no writing. Flat 16-bit pixel-art game sprite, crisp square pixels, matte colours with no gloss, every shape closed by a 2-pixel dark outline, daylight from the upper left with one hard pixel shadow, on a solid uniform bright green background (#00FF00) with nothing else in frame. No text, no lettering, no numbers, no logos, no watermark anywhere. Original design, not based on any existing video game character.

**att-006 · A6_obst_swarm · 1:1 · `A6_obst_swarm_att-006.png` `e9c5ef00…`**
> A single game obstacle: a swarm of five angry red speech-bubble shapes with cartoon frowning eyes, each bubble empty except one bold exclamation-mark symbol, flying in a loose cluster with small motion lines. No letters or words inside the bubbles. Flat 16-bit pixel-art game sprite, crisp square pixels, matte colours with no gloss, every shape closed by a 2-pixel dark outline, daylight from the upper left with one hard pixel shadow, on a solid uniform bright green background (#00FF00) with nothing else in frame. No text, no lettering, no numbers, no logos, no watermark anywhere. Original design, not based on any existing video game character.

**att-007 · A7_plate · 9:16 · `A7_plate_att-007.png` `04b0615f…`**
> A vertical 9:16 pixel-art background for a side-scrolling game, Indian city lane: a tall cream-and-terracotta paying-guest building with many stacked floors of small windows and balconies filling the upper two thirds, black water tanks and a TV antenna on the roof, a lower cream building beside it, a pale blue sky with two simple clouds. The bottom fifth is an empty flat packed-earth lane in muted ochre with a low stone kerb, no ground pattern. All building faces and walls are plain and blank — no shop fronts, no boards, no hoardings, no writing of any kind. Flat 16-bit pixel art, crisp square pixels, matte colours, 2-pixel dark outlines, daylight from the upper left. No text, no lettering, no numbers, no logos, no watermark anywhere. Original design, not based on any existing video game.

**att-008 · A10_music · lyria-002 (vertex) · USD 0.06 · `A10_music_att-008.wav` `8be3e70e…`**
> Upbeat 8-bit chiptune instrumental, bright square-wave lead melody, driving bass line, punchy electronic drums, 140 bpm, playful and energetic, loop-friendly, no vocals

What the prompts carry and do not carry (OBSERVED by reading them):

- The owner prompt specifies costume, props, four *locomotion* poses and a style block. It specifies **no facial expression, no emotional state, no hurt/cornered/triumphant pose, no powered pose, no attack pose**. The four poses are idle, run-L, run-R, jump.
- Two obstacles are given an expression ("a mean squinting face", "cartoon frowning eyes") — the enemies have faces; the hero does not.
- The sack is asked for "mid-hop"; the tower "about to fall"; the swarm "flying … with small motion lines" — **motion is asked of the still**, then (§7) the code moves those stills as rigid rectangles.
- Nothing in any prompt describes the *powered* state, the projectile, the phone, the flag or any effect; those were, by plan, code.
- The style block is identical across seven prompts (consistent order, concrete nouns, exclusions) — INFERRED: as prompt craft for *what was asked*, these are competent; the loss is in what was not asked.

The raw sheet (OBSERVED at 1:1, `gen/raw/A1_owner_sheet_att001.png`, 1584×672): four poses, one man, **the same neutral, closed-mouth face in all four**; keys and book present; no lettering. The five obstacle stills read as designed; the sack squints, the tickets frown.

---

## 7. The animation / compositing instructions (OBSERVED, `A/tools/render_game.py` @ 7dab37a, sha256 `f9a819f0…`, 36,972 bytes; `tools/sfx.py` `d2433705…`)

This is the film's "director": every movement, contact and effect is a line of Python evaluated per frame (900 frames at 30 fps, 1080×1920). There is no physics, no collision detection, no animation curves library — positions are functions of time.

### 7a. Every effect primitive the renderer has

| Primitive (function / block) | What it does | Constants |
|---|---|---|
| `camera_x(t)` — scroll | world moves left at a constant rate; **pauses** 15.0–18.0; stops at 26.6 | 400 px/s (0–15 s), 480 px/s (18–26.6 s) |
| `Sprites.plate()` + parallax | the generated 9:16 plate fitted to 1080×1920, shifted up 422 px, tiled ×2 with a mirrored copy; scrolls at 0.25× camera | 0.25× |
| `draw_ground(cv, camx)` — lower band (repair D-7) | lane fill; depth darkening; kerb slabs; yellow dashes; two wheel tracks; drain grate; manhole; parked-scooter silhouette; small stones — a nearer layer at 1.3× | slab joint 220 px; dashes 160 px; grate/manhole 1400 px; scooter 2100 px |
| `desaturate(cv, k)` — world tint | blend the whole frame to grayscale | F6 ramp 14.2→15.0 (0.8 s); F7 full to 17.2, back over 0.4 s |
| `Sprites.owner(pose, powered)` — character | one of **four** bitmaps (idle / runA / runB / jump), `ImageOps.contain` to 260 px tall, NEAREST; powered = the same bitmap with a **cyan halo** (25 offset pastes of the alpha mask at alpha 110, ±6 px in steps of 3) and a 12-px offset | `owner_h = 260`, `owner_x = 260`, halo alpha 110 |
| run cycle | pose = runA if `int(t*8) % 2 == 0` else runB | **2-frame cycle at 8 swaps/s** (4 Hz) |
| jump | `sin` arc, pose = jump while airborne | F1 0.6–1.1 s ×170 px; F3 1.0–1.5 s ×150 px; F10 0.6–1.0 s ×200 px — **three jumps in 30 s** |
| knock-back | horizontal offset decaying linearly | F2/F3/F5 60 px over 0.4 s (tl 1.5–1.9); F4 40 px over 0.5 s + idle pose; F6 40 px held + idle pose |
| `flash_sprite()` — hit flash (repair D-9) | white silhouette from the alpha mask, alpha 200 | 0.12 s at contact (obstacles 1, 2, 4, 5; none for 3) |
| obstacle entry | rigid bitmap enters from x=1080 at scroll speed; `oy` fixed at ground; **no hop, no topple, no dive** — every obstacle travels in a straight line at constant speed; the tenant enters from the left at 1.9× speed | contact at `tl = 1.5` (problem) / `0.75` (clearing) — **timed, not detected**; sizes ×1.15 (R4): 345×368, 276×276, 200×300, 300×390, 368×300 |
| obstacle exit at F6→F7 | F7 is not in `OBST_BEATS`, so the swarm **is not drawn from 15.0 s** — it vanishes at the beat boundary (OBSERVED on frames 14.9 vs 15.0) | — |
| `draw_tick()` — projectile (repair D-3) | pixfont `✓` glyph at scale 4 with a 1-scale dark shadow | flies from `owner_x+150` at 900 px/s from tl 0.3 to 0.75 (≈ 405 px), y = ground−160 |
| F8 test tick | same glyph rising | 0.4–0.9 s, +900 px/s x, −300 px/s y |
| `debris()` — burst (repair D-6) | sprite cut into 6×6 tiles flying outward with gravity, alpha fading 1−k | obstacles 1, 2; vx (i−2.5)·90 ± 30, vy −260 + (j−3)·40 ± 40, gravity 900·k², over **0.35 s** |
| `neat_dashboard()` (D-6) | a 220×260 brand-blue card with cyan bars and a green tick replaces the tower, shrinking to 25 % and drifting toward the checklist | 0.35 s |
| `recolour_red_to_green()` (D-6) | pixel test turns red pixels green, then fades | recolour over 0.175 s, fade over 0.175 s |
| dues tag (F9.3) | 44×44 cyan square with three lines travels with the tenant | from tl 0.75 |
| chip flight | the chip string flies from ~(700, 880) to its checklist row | tl 0.75–1.10 (0.35 s) |
| label recall flash | obstacle label at y 720 | 0.4 s in the clearing run |
| cheat panel (F7) | slides up 500 px over 0.5 s; header; **typing** `INSTALL` / `RENTOK APP` by character count over 1.4 s (15.8–17.2); fades over 0.4 s from 17.6 | panel (105, 520)–(848, 920) |
| phone drop (F7) | a 70×120 blue rectangle with the wordmark falls from y 200 to ground−200 at x `owner_x+120` | 17.2–17.6 (0.4 s) |
| full-frame white overlay | `rectangle((0,0,W,H), alpha 160)` | 17.6–17.7 (0.1 s) — OBSERVED still full-frame (D-9 changed only the *hit* flashes) |
| phone in hand (D-4) | 60×104 blue rectangle composited at `owner_xy + (width−30, 60)` | 17.6–19.6 |
| health refill | one segment per 0.08 s, cyan | 17.6–18.0 |
| HUD | `PG OWNER`, health glyphs, phone icon (from 18.0), wordmark chip 150×77 | y 300, scale 6 |
| state flashes | `LEVEL 1`, `GAME OVER?`, `POWER UP!`, `LEVEL CLEAR!` blink | `int(t*4) % 2` → 4 Hz |
| flag (F10) | pole enters at 480 px/s to x 600; flag 136×90 rises ground−120 → 540 over 0.8 s; 40 deterministic 10-px confetti squares fall at 400 px/s; checklist fades 26.6–27.0; owner advances 280 px over 0.4 s then idle | jump 200 px 0.6–1.0 |
| end card (F11) | 0.3-s blend to #0239FF; wordmark 700 px; CTA; URL | — |

### 7b. What the renderer does **not** have (OBSERVED by absence in the file)

No anticipation (crouch before a jump, wind-up before a shot), no squash-and-stretch, no follow-through or overshoot, no hit-stop (frame freeze on impact), no screen shake, no impact frame, no particle burst on contact in the problem half, no expression swap (one face), no attack pose (the projectile leaves from a point 150 px in front of a running/idle sprite; the arm never moves), no recoil on firing, no vertical bob in the run, no easing on any move (every motion is linear or a single sine), no collision detection (contacts are at fixed `tl`), no camera push-in or zoom at any beat, no sprite-scale change except the ×1.15 global repair, no shadow under the character, no obstacle *reaction* on hit in the problem half (the obstacle keeps scrolling unchanged after hurting the owner).

### 7c. Sound (OBSERVED, `tools/sfx.py`)

Fourteen cue types, all square/noise synthesis with attack-decay envelopes: jump (300 Hz sweep up, 0.18 s), hit (220 Hz sweep down + noise, 0.22 s), trip, key click ×17 (1600 Hz, 45 ms), low tone (70 Hz, 0.8 s at 14.2), pew (900 Hz sweep down, 0.12 s), burst (noise + 110 Hz, 0.28 s), ding, tag, power-up (C-E-G-C-E at 90 ms/note), fanfare (G-G-A-C-E-C at 130 ms), end hit. Cue times come from the board (`t0+0.3` pew, `t0+0.75` burst, `t0+1.1` ding per clear). INFERRED: the sound design is correct to the events and thin in weight — no low-frequency impact on the hits, no riser into the power-up, no bass drop or silence before the flash.

### 7d. Board vs code drift (OBSERVED)

| Board says | Code does |
|---|---|
| F3 "sack hops toward him" (prompt: "mid-hop") | sack slides in a straight line (`oy` fixed) |
| F5 "topples onto him; he is half-buried" | tower slides past; owner knocked 60 px |
| F6 "swarm dives at him; he sits down" | swarm slides; owner idle pose + 40 px offset |
| F4 "reaches out, trips" | idle pose + 40 px offset |
| F7 "a white flash" (D-9 fixed hit flashes on the character) | install flash still full-frame alpha 160 |
| F1 jump blip at 0.9 s | code jumps at 0.6 s (checker noted; picture and sound agree with each other) |
| `board.json` `checklist_row_h: 48` | `T.checklist_row = 54` (R2a) |
| swarm present through F6 | swarm disappears at 15.0 (not drawn in F7) |

None of these drifts was a defect under the acceptance contract; all of them are places where the prose promised a *motion* and the code delivered a *translation*.

---

## 8. The final media (OBSERVED on frames extracted by this session)

Contact sheet at 2 fps: `evidence/CONTACT-SHEET-A-2fps.png` (60 frames). Key-beat frames in `evidence/frames-A/` (25 frames named `tSS.SS.png`, extracted from the sha-verified final with `ffmpeg -ss`).

| Frame | What the picture shows (OBSERVED) |
|---|---|
| `t00.90` | owner mid-jump at the cold open; `LEVEL 1`; HUD full; facade fills the top half; lane the bottom 40 % |
| `t03.00` / `t03.35` | document wall next to the owner; white silhouette flash at 3.35 |
| `t06.00` | sack beside the owner, both on the ground line, the same size relationship as every other obstacle |
| `t13.80` / `t14.50` | swarm beside the seated owner; `GAME OVER?`; world greying — the owner's face is the same neutral face as at 0.9 s |
| `t15.50`–`t16.50` | panel up; typing; owner idle in grey, no obstacle on screen |
| `t17.47` | the blue phone rectangle level with the owner's head, mid-drop |
| `t17.80` / `t18.55` | colour back; cyan halo (a thin outline at phone size); phone in hand; test tick a small cyan mark |
| `t19.90` | tick in flight toward the re-entering wall |
| `t20.45` | wall bursting into tiles (debris) |
| `t21.40` (HERO) | owner running with halo, sack intact to his right, checklist with one chip, `PG OWNER` HUD — **no projectile and no impact visible in the hero frame itself** |
| `t21.65` | sack in debris |
| `t22.90` | tenant with dues tag exiting right |
| `t24.05` | dashboard card where the tower was |
| `t25.25` | tickets olive (mid red→green) |
| `t26.80` / `t27.40` | owner at the pole; flag rising / at the top; confetti |
| `t29.90` | end card |

Scale (measured on the frame): the owner is 260 px tall in a 1920-px frame — **13.5 % of frame height**; the largest obstacle 390 px (20 %). The facade occupies y ≈ 0–1180; the lane y 1180–1920 (38.5 %). At Reels size (≈ 360 px wide preview) the owner is ≈ 87 px tall.

The independent checker's creative-quality observations (OBSERVED, `A/stages/CHECK-STAGE-5.md` §5 and closing summary) corroborate what the frames show: "the 'gun sort of power' reads as a small cyan dot and the app itself is a blue rectangle on screen for a third of a second — the transformation is told by words more than shown by picture, and the customer asked for it to be shown"; "the sprites are small in the middle of a tall phone screen, which at Reels size can feel like a game viewed from too far away"; "the 'game' is more scripted than played".

---

## 9. Lane B — the same chain, in brief (OBSERVED, `B/`)

**Direction input:** the ChatGPT direction (`…-ctrl/experiments/RENTOK-TWO-LANE-2026-09-20/02-CHATGPT-DIRECTION-LANE-B-ONLY.md`) — notable creative lines: "The player initially struggles, loses health, and becomes trapped"; "The player is cornered with one heart remaining. The game freezes"; "the world transitions from chaotic to controlled gameplay"; "**The character should physically interact with the game obstacles, rather than merely running past labels that disappear automatically.**"

**Method:** the same — code-rendered 2-D scroller, seven Nano Banana 2 stills + Lyria, plus a three-line announcer (Sarvam bulbul:v3, the element the customer called "robotic"). 25 paid calls, USD 0.587 (17 of them voice auditions and transcription checks).

**Asset prompts (verbatim in `B/gen/ATTEMPTS.jsonl`, att-018…att-025):** the character sheet asks for **nine** poses in a 3×3 grid on magenta, including "hurt pose recoiling backwards **with a pained face**", "cornered pose standing with arms up defensively", and two "running while holding a smartphone up high" poses; "Round friendly face". The five obstacle prompts each ask for **two panels — a before state and an after state** ("the same card creature now calm and friendly … a big green check-mark sticker"). The plate is 16:9 ("a wide horizontal strip"), later found to leave the lower third of the 9:16 frame empty (checker D-5).

**Renderer (`B/tools/render_film.py`, 29,792 bytes):** renders at 360×640 and upscales ×3 NEAREST; character 92 px low-res (≈ 276 px on screen, "1/7 frame"); 9 poses; a 3-px run bob (`3·|sin 20t|`); jump 180 px triangular; hurt knock −60; cornered −40; world plate **tinted** before/after (sky mask to brand blue); obstacle **before→after sprite swap** at `hit_t = 0.7` with the after-state rising 120 px over 0.6 s; O3/O5 idle bob (`sin 6t·10`, `sin 9t·14`); a cyan **beam** line (4 px + 1 px white core, an "OK" glyph at the tip) 0.45–0.75 s; an expanding white ring 20→80 px over 0.15 s on hit; 50 % white blend hit flash 0.10–0.15 s; shield glow = Gaussian-blurred ellipse pulsing at 7 rad/s; fireworks (3 bursts × 8 particles) at the flag; 70 %/50 % greying during the freeze; a 60 % white flash at `RENTOK MODE: ON`.

**Differences from Lane A that matter for the trace (INFERRED):** Lane B *asked the image model for expression and for before/after states* and *implemented a hurt pose, a cornered pose and a world tint*; it therefore had more creative information reach the assets and the code. Its checker still wrote (OBSERVED, `B/stages/CHECK-STAGE-5.md`): "Facial expression does not change while losing hearts. The four run cells and the jump cell smile; only the brief hurt pose grimaces"; "the owner smiles all the way through, so the customer's 'problems → cheat code → blast them all' story arrives as calm and friendly rather than dramatic"; "no platforms, no pit, no stomp"; "runner with labels". Lane B's character is drawn at 92 px and upscaled ×3, so it reads *softer and smaller* than Lane A's (contact sheet `evidence/CONTACT-SHEET-B-2fps.png`; frames in `evidence/frames-B/`).

Both lanes converged on the same method from the same evidence base (Controller comparison §2). Both checkers, independently, named the same two customer-rejection risks: the game is viewed from too far away / letterboxed, and the transformation is told rather than shown.

---

## 10. What this reconstruction establishes (INFERRED, carried into 02)

1. The customer's creative words are few and mechanical; the plan expanded them into a sound ad structure (Canon-backed) and a *described* set of game motions (not Canon-backed — Canon has nothing on animation).
2. The asset prompts faithfully carry costume, props, style and the four locomotion poses — and nothing about the owner's inner state, powered form or attack. They carry motion words for the obstacles ("hopping", "toppling", "diving") that the renderer then ignores.
3. The renderer has a small primitive set (§7a) and lacks the primitives (§7b) that would make a hit land or a power-up feel powerful. Several board motions were reduced to "slide and knock 60 px".
4. The film shows exactly what the code says: correct events, small sprites, one face, straight-line motion, brief effects. The checkers saw it; the customer accepted it and later called it not exceptional.
