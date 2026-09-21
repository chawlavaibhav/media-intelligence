# 05 — Treatments B, C, D on the frozen unit: plan and costs (USD 0 spent; nothing dispatched)

Experiment `RENTOK-CREATIVE-QUALITY-001`, Phase 1. Written 2026-09-21. **This file is a plan. No paid call has been made.** Every price below is a live PriceBook quote taken by this session (`runtime.route.cli.build_router()[0].prices.quote(route_key, {"params": {"duration_s": N}})` for per-second routes; `quote(route_key, {})` for per-image routes), all on the **credits** pool; no fal, no cash route.

The unit: the frozen Treatment A window (04), events 14.0→20.8 s — *owner faces the complaints swarm → hit → GAME OVER? → cheat panel → install → power-up → first clear (document wall) → chip*. B, C and D each produce one ≈ 5–8 s clip covering that event list, for the blind evaluation in 06.

Labels: OBSERVED (a quoted price, a cell status, a file) · INFERRED · PROPOSED · UNKNOWN.

---

## 0. Prices and cells used (OBSERVED)

| route_key | Cell (Lane A `stages/evidence/routing-table.txt`) | evidence status · use · accepts | Surface · pool | PriceBook quote |
|---|---|---|---|---|
| `nano-banana-2` | IMG-CORE | clean_observed · True · 7/8 | gemini_api (`gemini-3.1-flash-image`) · credits | **USD 0.067 per image** (pin: `price-pins-2026-09/gemini-api-judge/gemini-api-pricing.html`) |
| `nano-banana-pro` | IMG-CORE (declared fallback) | clean_observed · True · 4/8 | gemini_api · credits | USD 0.134 per image |
| `veo-3.1-fast-i2v` | VID-I2V | clean_observed · True · **5/8** | vertex (`veo-3.1-fast-generate-001`) · credits | **USD 0.10 per second** → 4 s 0.40 · 6 s 0.60 · 8 s 0.80 (pin: `price-pins-2026-09/vertex-shared/vertex-generative-ai-pricing.html`) |
| `veo-3.1-fast-ref2v` | VID-REF (`+native`) | clean_observed · True · **2/4** | vertex · credits | USD 0.10 per second → 0.40 / 0.60 / 0.80 |
| `gemini-omni-1.1-flash` (t2v) | VID-T2V | clean_observed · True · **8/8** | gemini_api · credits | **USD 0.10136 per second** → 4 s 0.405 · 6 s 0.608 · 8 s 0.811 |
| `veo-3.1-fast-extend` | VID-MS (`+chain`) | directional_only · **manual_only** · 2/2 | vertex · credits | USD 1.50 per call (quantity rule `veo_extend_15s`: 15 s billed) |
| `lyria` | MUS | clean_observed · True · 4/4 | vertex · credits | USD 0.06 per clip — **not used**: every treatment re-uses the baseline bed |

Directional notes attached to these cells (OBSERVED in the map/routing table, `routing_authority: none`): RR-8 "avoid Veo 3.1 fast i2v where the brief forbids camera moves"; map evidence "veo-3.1-fast-i2v 5/8 (0/2 on the phone still: 'zooms in'; one 'hand appeared')"; Cumin case RO-02 "veo-3.1-fast-i2v … all 7 technically clean (no lettering, static camera obeyed 6/6)"; RR-11 "Veo 3.1 fast ref2v carries a referenced PRODUCT into motion (2/2) but invents lettering in people scenes (0/2)"; RR-9 "Veo 3.1 fast extend chain works but reads visually weaker"; RR-15 "Gemini Omni 1.1 Flash on GCP credits is the default … do not rely on Veo 3.1 fast or Kling v3 Pro audio where the brief names physical detail". **UNKNOWN:** no trial in the map or in any case animates *pixel-art* stills; the D micro-qualification exists to answer that.

---

## 1. Treatment B — asset-prompt improvement only

**Held fixed (OBSERVED constraints of the renderer):** `tools/render_game.py` @ `f9a819f0…` unchanged; `board.json`, `copy-deck.json`, `sfx.py`, `assemble.py` unchanged; model `nano-banana-2`; aspects 21:9 (sheet) / 9:16 (plate) / 1:1 (obstacles); cut-out by `cutout.py`; the renderer loads exactly four owner bitmaps by name (`owner_idle/runA/runB/jump`), five obstacles and one plate. **Consequence (INFERRED):** B cannot add a pose, an expression *state*, a camera or an effect — it can only change what those fixed bitmaps look like. B therefore tests the customer's hypothesis in its purest form: *if the plan's intent had been carried into the prompts better, would the same renderer have produced a better film?*

### 1a. Which assets are most consequential for this sequence (INFERRED, from 04 §3a screen time)

| Rank | Asset | Screen time in the unit | Why it matters most |
|---|---|---|---|
| 1 | **Owner sheet** (idle 5.5 s of 6.8; run 1.3 s) | every frame | the only face in the film; idle is the pose held through the low point *and* the power-up |
| 2 | **Plate** | every frame | the whole world; depth and mood live here |
| 3 | Swarm (obstacle 5) | 1.0 s | the threat he faces at the in-point |
| 4 | Document wall (obstacle 1) | 1.2 s | the first payoff |

The idle pose is the crux and the constraint: in the baseline it serves as *cornered* (14.1–17.4) and as *powered* (17.4–19.6). One bitmap must read acceptably in both. PROPOSED resolution: draw idle as **braced and determined** (feet planted, weight slightly back, fists, jaw set, brows down, eyes on the threat) — a stance that reads as "refusing to fall" before the install and "ready" after it. An *alarmed* idle would sell 14.1–17.4 better and break 17.4–19.6; a *triumphant* idle the reverse. This is B's ceiling, stated.

### 1b. The proposed prompts (PROPOSED; vendor-guidance style: fixed order — subject, poses/layout, costume, style block verbatim from A, exclusions; concrete nouns; no negatives in the body except the closing exclusion block)

**B-A1 owner sheet (21:9, replaces att-001):**
> A sprite sheet of ONE character in four poses side by side, evenly spaced, same size and same design in every pose: (1) standing braced and determined — feet planted wide, weight slightly back, both fists clenched at hip height, shoulders squared, jaw set, brows lowered, eyes fixed ahead; (2) running hard with the left leg forward — torso leaning forward about fifteen degrees, right arm punched forward, left arm swung back, mouth set in a grim line; (3) running hard with the right leg forward — the same forward lean, arms in the opposite swing; (4) jumping with knees pulled up and both arms raised, a broad open-mouthed grin. The character: an ordinary Indian man of about forty, slightly stocky, short black hair, rectangular spectacles, thick expressive eyebrows, a blue-and-white checked half-sleeve shirt, dark trousers, brown sandals; a big bunch of keys on a ring hangs from his belt and swings with his motion; he carries a thick red bound account book under his left arm in every pose, its cover blank. Full body, facing right, feet on the bottom edge, the head about one fifth of the body height so the face reads at small sizes. Flat 16-bit pixel-art game sprite, crisp square pixels, matte colours with no gloss, every shape closed by a 2-pixel dark outline, daylight from the upper left with one hard pixel shadow, on a solid uniform bright green background (#00FF00) with nothing else in frame. No text, no lettering, no numbers, no logos, no watermark anywhere. Original design, not based on any existing video game character.

What changed vs att-001 and why (INFERRED from 02 rows 1, 4): each pose now carries a *body attitude* and a *facial expression*; the run has lean and arm swing (two-frame cycles read as running when the extremes are exaggerated — classic-animation reasoning, not Canon); the book is fixed to the left arm in all four (removes the D-5 patch); head proportion is stated so the face survives at 260 px.

**B-A7 plate (9:16, replaces att-007):**
> A vertical 9:16 pixel-art background for a side-scrolling game, an Indian city lane at late afternoon: in the far distance a tall cream-and-terracotta paying-guest building with many stacked floors of small windows and iron balconies filling the upper two thirds, black water tanks and a TV antenna on the roof, a lower cream building beside it, one rooftop with drying laundry, a pale blue sky with two simple clouds; in the middle distance a row of low shop-house fronts with closed shutters, a leaning electricity pole with looped wires, a small neem tree and a parked yellow auto-rickshaw seen from the side; the bottom fifth is an empty flat packed-earth lane in muted ochre with a low stone kerb, no ground pattern. All building faces, shutters and walls are plain and blank — no shop fronts with writing, no boards, no hoardings, no writing of any kind. Flat 16-bit pixel art, crisp square pixels, matte colours, 2-pixel dark outlines, daylight from the upper left with long soft-edged afternoon shadows. No text, no lettering, no numbers, no logos, no watermark anywhere. Original design, not based on any existing video game.

What changed: a middle-distance row (depth without a second layer), specific life (laundry, pole, tree, auto), a time of day. Risk (OBSERVED, RO-04 in cases 001/002): shop-house fronts invite signage; the exclusion block is kept verbatim and "closed shutters" is used so there is no surface to write on.

**B-A6 swarm (1:1, replaces att-006):**
> A single game obstacle: a swarm of five angry red speech-bubble creatures diving down and to the left in a tight wedge, the lead bubble largest and closest, each with cartoon furrowed eyes and bared teeth, each bubble empty except one bold exclamation-mark symbol, trailing short motion lines. No letters or words inside the bubbles. Flat 16-bit pixel-art game sprite, crisp square pixels, matte colours with no gloss, every shape closed by a 2-pixel dark outline, daylight from the upper left with one hard pixel shadow, on a solid uniform bright green background (#00FF00) with nothing else in frame. No text, no lettering, no numbers, no logos, no watermark anywhere. Original design, not based on any existing video game character.

What changed: a *diving wedge* with a lead bubble — the still carries the threat the code will not animate (02 row 7b).

**B-A2 document wall (1:1, replaces att-002):**
> A single game obstacle: a tall wall built from stacked blank white paper sheets and blank folders, leaning toward the viewer's left and bulging as if about to burst, a few loose sheets already lifting off the top, with a faceless grey human silhouette peeking out from behind it and a large bold question-mark symbol floating above. The sheets are blank with no writing. Flat 16-bit pixel-art game sprite, crisp square pixels, matte colours with no gloss, every shape closed by a 2-pixel dark outline, daylight from the upper left with one hard pixel shadow, on a solid uniform bright green background (#00FF00) with nothing else in frame. No text, no lettering, no numbers, no logos, no watermark anywhere. Original design, not based on any existing video game character.

### 1c. Draws and price (PROPOSED)

| Asset | Draws (max) | Unit | Max USD | Expected |
|---|---|---|---|---|
| B-A1 owner sheet | 2 (1 + 1 repair; the sheet is micro-qualified on the same five criteria as Lane A plus "expression reads at 260 px") | 0.067 | 0.134 | 0.067 |
| B-A7 plate | 2 | 0.067 | 0.134 | 0.067 |
| B-A6 swarm | 1 | 0.067 | 0.067 | 0.067 |
| B-A2 wall | 1 | 0.067 | 0.067 | 0.067 |
| Render + assemble | code | 0 | 0 | 0 |
| **Treatment B** | **≤ 6 draws** | | **0.402** | **0.268** |

Order of work: sheet → cut-out → 30-frame test render of 14.0–15.0 and 18.0–19.6 → checker look → plate → obstacles → full re-render of the unit with the unchanged board → `qa_checks.py` gates (C1/C5/C2/C6) → cut 14.0–20.8 by the same `-c copy` recipe as 04.

---

## 2. Treatment C — creative-direction improvement, same renderer where feasible

### 2a. The stronger visual-quality objective for the scene

**Derived from the brief:** "feel like an actual platform game" · "a gun sort of power/immunity" · "runs and kills all the obstacles" · "central turning point". The customer wrote a power fantasy: a beaten man is handed a power and *uses* it. The baseline shows the events; the objective is that the viewer *feels* the beating, the gift and the use.

**Canon claims actually retrieved for this objective (OBSERVED ids, text re-read in `canon/knowledge/current/**`):**

| id | Claim (as Canon holds it) | Executable consequence for the unit |
|---|---|---|
| `sk_murch_c003_0020` | "Emotion is the first criterion, weighted … at 51 percent … preserved at all costs" | every beat gets a stated feeling; where a feeling and a tidy layout conflict, the feeling wins (the safe box stays) |
| `sk_alt_c003_0014` | "the camera is the audience's eye, so when it moves closer the audience moves with it and when it concentrates on one item the audience's attention goes th[ere]" | a camera push-in on the owner at the hit and at the install |
| `sk_alt_c003_0022` | in drama "the lighting fluctuates across the film … gay sequences are lit brightly, sad scenes lower, and tragedy is served by strong contrast" | the low point is *dark and cold*, not grey; the power-up is *bright and warm-cyan* |
| `sk_alt_c003_0015` | "The illusion of depth is produced by separating foreground from background in tone" | the owner is lit/outlined brighter than the world at the power-up; the world is dimmed behind him at the low point |
| `sk_conv_c003_0019` | "dialogue and sound effects compete, and withdrawing dialogue causes the audience to search the remaining sound for meaning" | a 0.3-s near-silence before the flash so the power-up sound lands |
| `sk_hop_sa_0026` | a picture must "earn the space it occupies, with its size gauged by its importance to the sale" | the owner and the phone get more of the frame at the install than anywhere else in the film |
| `sk_whip_0015` | "the figure who … grants a power before the hero returns transformed" | the transformation must be *visible on the hero's body*, not only in a HUD colour |
| `sk_abcd_0006` | "'Jump in' … pacing that keeps the viewer engaged, and tight framing" | tighter framing on the action beats |
| `sk_gote_c003_0004` | "Each shot cut to must give the viewer information it did not already have" | the push-in/snap-back are treated as "shots" and each reveals something (his face; the phone; the glow) |

**GAP (OBSERVED):** Canon holds nothing on animation principles or game feel (01 §3). The motion instructions below therefore rest on **explicit reasoning with named external references, not Canon**: the twelve principles of animation as set out by Frank Thomas and Ollie Johnston in *The Illusion of Life* (1981) — *anticipation* (a small counter-movement before an action so the eye is ready), *squash and stretch* (deformation that reads as weight and speed), *follow-through and overlapping action* (parts keep moving after the main action stops), *timing* and *exaggeration*; and the "game feel"/"juice" vocabulary of action games — *hit-stop* (a 2–5-frame freeze at impact), *screen shake*, *impact frames* (a one-frame flash or silhouette at contact), *particle bursts* — as described in Steve Swink's *Game Feel* (2008) and popularised in the talk "Juice it or lose it" (Jonasson & Purho, 2012). These are cited as reasoning; they are not Canon and must not be recorded as such.

### 2b. The objective, as executable instructions per beat (PROPOSED)

Time base = the baseline window; C keeps the board's beat boundaries and every string, so the DET gates still apply.

**Beat 1 · 14.0–14.1 · "He sees it coming."** Feeling: dread. Character: run pose (lean) → at 14.05 a 2-frame *anticipation* (weight back, arms up — the braced idle from the new sheet). Environment: the swarm dives on a curve from upper-right toward his head (`oy` follows a quadratic), lead bubble first. Camera: begin a push-in 1.00→1.30 centred on the owner over 14.05–14.30. Audio: the bed ducks 6 dB; a short riser (noise sweep 0.2 s).

**Beat 2 · 14.1–14.5 · "It lands."** Feeling: pain. Impact: **hit-stop** — hold frame 14.10 for 3 frames (0.1 s) with a one-frame white silhouette of *both* owner and swarm; then **screen shake** 10 px decaying over 0.25 s; owner swaps to the *hurt* pose (new sheet: knocked back, book flying up 40 px and landing at 14.5 — follow-through); knock-back 90 px with ease-out (not linear); a 6-point yellow impact star at the contact point for 2 frames; 8 dust puffs at his feet. The swarm *recoils* 30 px right and bobs. Audio: hit (existing) + a 60-Hz thump 0.3 s; the bed cuts for the hit-stop and returns low-passed (800 Hz) — dread.

**Beat 3 · 14.5–15.0 · "Down."** Feeling: defeat. Character: *cornered* pose (on one knee, one hand on the ground, face up, alarmed — new sheet). Environment: instead of `desaturate`, a **colour grade**: sky and facade to slate blue-grey (multiply by (0.55, 0.6, 0.75)), a vignette darkening the corners 35 %, the swarm hovering over him and still red (the one warm thing in frame — tonal separation). `GAME OVER?` as now. Camera: hold at 1.30. Audio: `cue_low` as now; bed low-passed and −9 dB.

**Beat 4 · 15.0–17.2 · "The code."** Feeling: a held breath. The swarm does **not** vanish: it drifts up and out over 15.0–15.6 (the world pausing pushes it off). Panel and typing exactly as now (all strings unchanged; disjointness gates re-run against the *transformed* layout log, see 2c). Character: cornered pose; at 16.8 he looks up (head-up variant of cornered — one more drawn frame). Camera: hold 1.30. Audio: key clicks as now over the low-passed bed.

**Beat 5 · 17.2–17.7 · "The gift."** Feeling: awe. The phone falls with a 3-px trail and a soft cyan glow; the owner's *catch* pose (arm up, hand open — new sheet) at 17.35; the phone lands in the hand at 17.4 (`install_event_t` unchanged); the screen lights cyan from the centre outward (a code radial); **0.3 s of near-silence** (bed −24 dB, no SFX) from 17.3; at 17.6 the flash — but *from the phone*: a cyan-white radial burst 0→1400 px radius over 4 frames with a 1-frame full white; camera **snaps back** to 1.00 on the flash with a 6-px shake. Audio: at 17.6 the arpeggio + a bright impact + a bass drop; the bed returns full-band and one semitone up (ffmpeg `asetrate`/`atempo` on the bed from 17.6 — "level 2").

**Beat 6 · 17.7–19.6 · "The power."** Feeling: rising confidence. Character: *powered stand* (new sheet: chest out, phone held forward, jaw set, brows up — the same man, brighter eyes); the **aura pulses** (halo alpha 60↔140 at 3 Hz) and the shirt's blue takes a cyan tint (palette shift, code); 6 cyan sparks orbit him for 0.6 s. Environment: colour grade to *brighter* than the opening (sky +10 % luminance, a cyan cast in the highlights) — the world after is not the world before. The test tick at 18.4 leaves from the phone with a 60-px trail and a 2-frame muzzle flash; he *fires* it (firing pose from the new sheet, 0.2 s wind-up: arm back, then out). HUD as now.

**Beat 7 · 19.6–20.8 · "The first kill."** Feeling: release. Character: run pose with lean and a 3-px bob; at 19.8 the 0.2-s wind-up, at 19.9 the *firing* pose and the tick with trail + muzzle flash; recoil 8 px. The wall re-enters *taller* (drawn at ×1.3 relative to him — it is a wall) and leaning. Impact at 20.35: 2-frame hit-stop; a **shockwave ring** (expanding white ring 20→260 px over 6 frames); the wall's tiles fly outward (existing `debris`) plus 14 white paper-sheet sparks that flutter (rotate as they fall); 8-px shake; the silhouette peeks out and drops. Camera: quick push 1.00→1.15 on the impact and back over 0.3 s. Chip flight with ease-out and a landing "pop" (scale 1.3→1.0 over 3 frames). Audio: pew with a lower body (add a 200-Hz layer), burst + 60-Hz thump + a short whoosh (band-passed noise sweep down), ding as now.

**Text, HUD, safe box:** unchanged strings, scales and positions. The UI layer is drawn **after** the camera transform, so every text box stays where the DET gates measured it.

### 2c. What `render_game.py` would need (PROPOSED) — and what is feasible at USD 0

| New primitive | Purpose | Feasible at USD 0? | Needs new assets? |
|---|---|---|---|
| World/UI layer split | camera moves must not move the HUD, labels, panel or chips | yes — refactor `render_frame` into `world()` then `ui()`; the layout log is written from `ui()` so the gates are untouched | no |
| `camera(scale, cx, cy, shake)` — crop-and-scale of the world layer | push-in at the hit and install; snap-back on the flash; small pushes on impacts | yes (Pillow crop + `resize(NEAREST)`; 1080×1920 at ×1.3 = crop 831×1477) | no |
| hit-stop (frame hold) | impact weight | yes — a table of `(t, frames)` holds; the frame loop repeats the last composed world frame while the UI keeps time | no |
| screen shake (decaying offset) | impact | yes — `shake = A·(1−k)·sin(ωt)` on the camera centre | no |
| easing helper (`ease_out`, `ease_in_out`) | knock-back, chip landing, phone fall, camera | yes | no |
| pose table by beat (`POSES[beat][t-range] → asset name`) | hurt / cornered / catch / powered / firing / head-up | yes for the code — **the bitmaps do not exist** | **yes**: one 2×4 sheet (8 poses) or two 1×4 sheets |
| expression on the existing four poses | see B-A1 | — | **yes** (B-A1) |
| `colour_grade(cv, mul, vignette)` | cold low point, bright power state | yes (numpy multiply + radial mask) | no |
| aura pulse + palette shift | powered form visible on the body | yes (`alpha(t)`; per-pixel hue map on the shirt's blue) | no |
| particle emitter (sparks, dust, paper sheets with rotation) | impact, aura, burst | yes (a small list of `(x, y, vx, vy, rot, life)` per frame; Pillow `rotate` for sheets) | no |
| shockwave ring; impact star; muzzle flash; projectile trail | impact and firing | yes (ellipse outlines, polygons, alpha-faded copies) | no |
| obstacle motion curves (dive, recoil, drift-off, lean) | 02 row 7b | yes (`oy(t)`, `rotate`) | no |
| phone glow radial + flash-from-source | the gift | yes | no |
| bed processing (duck, low-pass, semitone lift, silence window) in `assemble.py` | audio progression | yes (ffmpeg `volume`/`lowpass`/`asetrate`+`atempo` with `aeval`-style envelopes or split-and-concat) | no |
| extra SFX layers (thump, riser, whoosh, bass drop) in `sfx.py` | weight | yes (synthesis) | no |

**Assets priced for C (PROPOSED):** one owner **expression/pose sheet** — 8 poses in a 2×4 grid (hurt · cornered · cornered-head-up · catch · powered stand · firing wind-up · firing · determined idle) at 21:9 or 1:1 — `nano-banana-2` **USD 0.067**, +1 repair **0.067** (identity risk vs the four-pose base sheet is real — a second sheet from a text prompt may drift; mitigation: micro-qualify it against the accepted base sheet on identity before any dependent work; if it drifts twice, fall back to the B-A1 four-pose sheet and drop the pose swaps, keeping every code primitive). Optional: a **second plate** for a true mid-ground parallax layer (a 9:16 strip of shop-house fronts/tree/pole on transparent-keyable green) **USD 0.067**. Optional: `nano-banana-pro` for the sheet if `nano-banana-2` drifts twice — USD 0.134, only on the Controller's OK (the declared Lane A fallback).

**Sheet prompt (PROPOSED, same style block, layout convention 2×4):**
> A sprite sheet of ONE character in eight poses arranged in two rows of four, evenly spaced, same size and same design in every pose. Row one: (1) knocked backwards mid-stumble, arms flung up, mouth open in shock, the red account book flying loose above his hand; (2) down on one knee with one hand flat on the ground, head lowered, shoulders sagging, eyes wide with alarm; (3) the same kneeling pose with the head lifted, looking up and to the right, hopeful; (4) standing with the right arm raised high and the hand open, palm up, catching something, eyes on the hand. Row two: (5) standing tall, chest out, feet planted, holding a small plain blue rectangle phone forward in the right hand at chest height, jaw set, brows raised, a confident half-smile; (6) standing with the right arm drawn back at shoulder height in a wind-up, left foot forward, eyes narrowed at a target to the right; (7) the same stance with the right arm punched straight out to the right, fist closed, mouth in a fierce grin, motion lines behind the fist; (8) standing braced and determined, feet wide, fists at hip height, jaw set. The character: an ordinary Indian man of about forty, slightly stocky, short black hair, rectangular spectacles, thick expressive eyebrows, a blue-and-white checked half-sleeve shirt, dark trousers, brown sandals; a big bunch of keys on a ring hangs from his belt; a thick red bound account book with a blank cover is under his left arm in every pose except pose one. Full body, facing right, feet on the bottom edge of each cell, the head about one fifth of the body height so the face reads at small sizes. Flat 16-bit pixel-art game sprite, crisp square pixels, matte colours with no gloss, every shape closed by a 2-pixel dark outline, daylight from the upper left with one hard pixel shadow, on a solid uniform bright green background (#00FF00) with nothing else in frame. No text, no lettering, no numbers, no logos, no watermark anywhere. Original design, not based on any existing video game character.

(The "plain blue rectangle phone" is textless by construction; the code overlays the wordmark as now.)

**Objectives the renderer cannot realise (stated, not weakened):**

1. **Secondary motion of cloth, hair and keys** (keys jingling on impact, shirt lag) — rigid bitmaps cannot do it; a drawn 2–3-frame overlay per event would approximate it (more sheet cells, ≈ USD 0.067 per sheet) but not match what a video model does for free. Left as an objective, met only in D.
2. **Physical contact between owner and obstacle** (the swarm *on* him, papers *over* him) — needs drawn contact frames or a video model; the C plan uses overlap + hit-stop + shake as a proxy.
3. **A face that moves between drawn states** (a grimace tightening, eyes narrowing over 0.3 s) — pose swaps are discrete; C accepts 2–3 discrete states per beat.
4. **Continuous camera with parallax depth change** — a crop-and-scale zoom does not change parallax; true depth needs separate world layers scaled by their depth (feasible only with the optional second plate).
5. **Squash-and-stretch of the character** — a non-uniform scale of a pixel-art bitmap breaks the pixel grid at 260 px; C uses anticipation and follow-through poses instead and states the omission.

**Price (PROPOSED):** sheet 0.067 (+ 0.067 repair) = **0.134 expected / 0.134 max**; optional second plate 0.067; optional Pro fallback 0.134 (Controller OK). **Treatment C max USD 0.335; expected USD 0.134.** All motion, camera, grade, particles, audio: USD 0 (code). Effort (INFERRED, not a cost the ledger sees): the renderer changes are ≈ 300–400 lines; the animatic-first rule applies — render C with placeholder poses first at USD 0 and judge *feel* on the animatic with the 06 rubric before drawing the sheet.

---

## 3. Treatment D — production-method alternative (generative video) with C's direction

### 3a. Route options for the unit (OBSERVED cells; PROPOSED use)

| Option | Route · cell · status | Price for 4 / 6 / 8 s | Fit to the unit (INFERRED) | Role in D |
|---|---|---|---|---|
| **D1** image-to-video from a composed start frame | `veo-3.1-fast-i2v` · VID-I2V · clean_observed · use=True · 5/8 | 0.40 / 0.60 / **0.80** | the strongest identity anchor (the accepted world frame at 14.0 with the owner and swarm in place); known risks: unmotivated zoom (map 0/2 on a phone still "zooms in"), extra hands; Cumin: static camera obeyed 6/6 | **primary** |
| **D2** reference-to-video (ingredients) | `veo-3.1-fast-ref2v` · VID-REF · clean_observed · use=True · 2/4 | 0.40 / 0.60 / 0.80 | carries a referenced *product* 2/2 but "invents lettering in people scenes (0/2)" (RR-11) — the owner is a person; a pixel-art person is untested | **probe only**, 1 draw, after D1's micro-qualification |
| **D3** text-to-video, no image | `gemini-omni-1.1-flash` t2v · VID-T2V · clean_observed · use=True · 8/8 | 0.405 / 0.608 / **0.811** | best acceptance rate in the map, native audio, but no visual anchor — identity with Lane A's owner would rest on the prose alone (03 §2.5 practice: description repeated word for word) | **probe only**, 1 draw |
| **D4** extend | `veo-3.1-fast-extend` · VID-MS · directional_only · **manual_only** | 1.50 per extend (15 s billed) | not needed: the unit fits in 8 s | **not used** (would require the human's explicit OK) |

Duration: **8 s** for every D draw — the unit's event list needs ≈ 6.8 s at the baseline's tempo; a generated clip will set its own tempo, and 8 s gives room to trim to the best 5–7 s. (4-s and 6-s prices are quoted for completeness; a 6-s draw is acceptable if the micro-qualification shows the model compresses the events well.)

### 3b. Order of work (PROPOSED)

1. **Micro-qualification, one draw (D1, 8 s, USD 0.80).** Judge on: (i) the owner is the same man as Lane A's (spectacles, checked shirt, keys, book); (ii) the world stays flat pixel art (no drift to 3-D/photoreal); (iii) no lettering, no HUD invented by the model; (iv) the camera stays side-on and level; (v) the *install → glow → fire → burst* chain happens inside the clip in that order; (vi) frame-hygiene scan on sampled frames (`runtime/loop/frame_hygiene`). Verdict by the independent checker, recorded before any further draw. **If (i)–(iv) fail twice, D stops** and is reported as a method failure for this look (a finding, not a defect).
2. **Up to N = 3 further D1 attempts** (USD 2.40 max), each a counted attempt with its prompt delta recorded (the MF same-plate iteration practice, 03 §2.6 P1/P5, applied deliberately: one change per attempt).
3. **One D2 probe** (USD 0.80) with the ingredient package below — only if D1 holds identity but loses the world, or vice versa.
4. **One D3 probe** (USD 0.811) — only if D1 fails on camera/zoom twice.
5. Composite (3e), cut, contact sheet, DET gates on the UI layer, hand to the evaluator.

### 3c. The model-specific prompt (PROPOSED; five-part Veo formula: cinematography → subject → action → context → style/ambience; positive phrasing; SFX lines; exclusions last and short)

**D1 prompt (image-to-video; the start frame is the 14.0-s world frame — see 3d):**
> Side-scrolling 2-D platform game view: the camera is locked level at ground height and does not zoom, tilt or cut; the level scrolls slowly from right to left; vertical 9:16 frame. The player character from the start image: an ordinary Indian man of about forty, slightly stocky, short black hair, rectangular spectacles, a blue-and-white checked half-sleeve shirt, dark trousers, brown sandals, a big bunch of keys on a ring at his belt, a thick red account book under his left arm — he stays exactly this man throughout. Action, in order: he runs right toward a swarm of five angry red speech-bubble creatures; they dive at him; he is knocked back onto one knee, shocked, the book tumbling then caught; the whole scene dims to cold blue-grey while the red creatures hover over him; a small plain blue phone drops from above into his raised open hand and its screen lights up cyan; a burst of cyan-white light floods out from the phone and full warm colour returns; a pulsing cyan glow wraps his body and he stands tall, jaw set, holding the phone forward; he runs right and punches his fist forward, firing a bright cyan tick-shaped bolt with a short trail at a tall leaning wall of blank white paper sheets, which bursts outward into tumbling sheets as he runs on. Context: an Indian city lane in front of a tall cream-and-terracotta paying-guest building with stacked floors of small windows, water tanks on the roof, a packed-earth lane with a stone kerb. Style: flat 16-bit pixel-art game animation, crisp square pixels, matte colours, 2-pixel dark outlines, hard-edged sprite motion with clear key poses, daylight from the upper left. Audio: an upbeat 8-bit chiptune bed; a crunchy 8-bit hit when the creatures strike; a low hum while the scene is dim; a rising four-note chiptune arpeggio when the phone lights; a soft pew for the bolt; a crunchy burst for the wall. All walls, sheets and screens are plain and blank; no text, no letters, no numbers, no health bar, no logos, no watermark.

`negativePrompt` (the Veo field, as Cumin used it): `text, lettering, captions, subtitles, HUD, health bar, logos, watermark, photorealistic, 3D render, camera zoom, camera pan, extra people, extra hands`. Params: `aspectRatio 9:16`, `resolution 720p` (as every accepted Veo i2v draw in the record), `durationSeconds 8`, `generateAudio true` (native audio is a D advantage; the composite keeps the baseline bed if the native bed is weak), `sampleCount 1`.

**D2 (reference-to-video) prompt:** the same text with the opening clause replaced by "Using the reference images — image one is the player character, image two the red speech-bubble creatures, image three the paper wall — …" and the world described in words (no plate reference if the surface caps references at three).

**D3 (Omni t2v) prompt:** the same text; the subject sentence is the identity anchor (03 §2.5: identity by word-for-word repetition), plus "the start of the clip shows him mid-run".

### 3d. The reference / ingredient package (PROPOSED)

| Item | Source (frozen) | Prepared as | For |
|---|---|---|---|
| Start frame | a **world-only** render of frame 420 (14.000 s): `render_game.py` with the UI pass disabled (a one-flag change: no HUD, no label, no chip) — the owner running, the swarm at x ≈ 520, plate and lane in place | 1080×1920 PNG → 720×1280 (9:16, the accepted Veo i2v geometry) | D1 image input |
| Owner ingredient | `frozen-inputs/gen/assets/owner_idle.png` (250×561) | padded onto a 1024×1024 flat mid-grey square (not green: chroma green in a reference could be reproduced) | D2 ref 1 |
| Swarm ingredient | `gen/assets/obst_5.png` | same padding | D2 ref 2 |
| Wall ingredient | `gen/assets/obst_1.png` | same padding | D2 ref 3 |
| Plate | `gen/assets/plate.png` | not sent to D2 if the surface allows only three references (UNKNOWN cap on the Vertex ref2v surface at dispatch time — read the surface doc then; the roster records the cell, not the cap) | D2 optional |

### 3e. How identity, spatial continuity and the transformation are held (PROPOSED)

- **Identity:** D1 — the start frame *is* the accepted world (the strongest anchor the record has: MF B3 and Cumin RO-02 both animate an accepted still); plus the full description in the prompt (03 §2.5). D2 — the cut-outs as ingredients. D3 — prose only (weakest; a probe).
- **Spatial continuity:** the locked side-on camera clause + `camera zoom, camera pan` in the negative prompt; the start frame fixes the horizon and ground line; the scroll direction is stated.
- **The power-up transformation:** stated as a *visible bodily change* ("a pulsing cyan glow wraps his body and he stands tall") plus a *world change* ("full warm colour returns") — the C objective, worded positively.
- **Text:** none asked of the model; every string by code (RR-1/RR-6 kept).

### 3f. Compositing and the "actual game" requirement (PROPOSED; consequences INFERRED)

The generated 8-s clip is the **world layer**; the code draws the **UI layer** over it: `PG OWNER` + health glyphs (draining 1→0 at the hit, refilling in cyan after the flash), the wordmark chip, `COMPLAINTS` and `TENANT VERIFICATION` labels, `GAME OVER?`, the cheat panel with the typed `INSTALL` / `RENTOK APP` (the panel can sit over the dimmed world exactly as now), `POWER UP!`, and the `✓ DIGITAL KYC` chip flight — all with `put_text` and the existing panel code, so the DET gates (bounds, disjoint, contrast, exact copy, forbidden claims) run unchanged on the layout log.

What changes: **the UI's timing must follow the clip**, not the board. The generated clip decides when the hit, the dim, the phone, the flash and the burst occur; a human reads those times off the frames (a 10-fps contact sheet) and writes them into a small per-clip event table the UI pass reads. This is one manual timing pass per attempt (≈ 10 minutes) and the main reason D is not deterministic.

What it does to A1 ("an actual platform game, not … gaming graphics placed over it"): the picture is still a game world with a code HUD — the same relationship as the baseline (world by stills + code, HUD by code) — so A1's furniture holds. The risk runs the other way: if the model drifts the look toward a cartoon film, the HUD becomes "gaming graphics placed over" a film, which is exactly what the customer excluded; the micro-qualification criterion (ii) exists for that. A9 (no Nintendo assets) becomes a *generation-time* risk the checker must inspect on frames. A11 holds (all strings by code). If D wins the evaluation, the consequence for a full 30-s film is a further question — mixed method (generated action beats, code-rendered connective tissue) — not answered here.

---

## 4. Budget (PROPOSED; all credits; prices OBSERVED above)

| Treatment | Paid items | Max draws | Max USD | Expected USD |
|---|---|---|---|---|
| A (baseline) | none — frozen | 0 | 0 | 0 |
| B (prompts only) | 4 nano-banana-2 stills, 2 with a repair | 6 | 0.402 | 0.268 |
| C (direction, same renderer) | 1 pose sheet + 1 repair; optional 2nd plate 0.067; optional Pro fallback 0.134 on Controller OK | 4 | 0.335 (0.134 without options) | 0.134 |
| D (generative video) | D1 micro-qual 0.80 + up to 3 × 0.80; D2 probe 0.80; D3 probe 0.811 | 6 | 4.811 | 2.40 (micro-qual + 2 attempts) |
| Evaluation packet | code only (labels, randomisation, contact sheets) | 0 | 0 | 0 |
| **Total** | | **16 calls** | **5.548** | **2.802** |

**Recommended cap: USD 6.00** for Phase 2, credits only, 0 hidden retries, hard stop — USD 0.45 (8 %) of headroom above the summed maxima, enough for one unforeseen infrastructure re-send at the most expensive unit (0.811) but not for an extra attempt on any treatment. Every failed or refused call counts. If the Controller wants D's ceiling lower: cap D at the micro-qualification + 1 attempt (USD 1.60) → total max USD 2.34, recommended cap USD 2.60.

Pool: Google credits (Gemini API key for nano-banana-2 and Omni; Vertex service account for Veo) — the same two-credential assumption Lane A recorded (Stage 4 §4.8); a balance reading or a human attestation is required before dispatch, as in Lane A.

---

## 5. The Media Factory technique adapted (PROPOSED; source in 03)

**Applied to D — "accepted hero still → image-to-video with a style/identity-lock sentence, then judge the clip on frame strips" (`media-factory/spike/film.mjs` `motion` and `run.mjs video`, git `706ee9c5…` / `dc729db5…`; finding B3).** D1's start frame is the accepted world frame; the prompt ends the subject sentence with "he stays exactly this man throughout" and the style sentence locks the pixel-art look — the same shape as MF's "Keep the exact soft watercolor storybook illustration style of the input image. No style change, no new elements, no text." Judged on a 10-fps strip (MF's `_veo0_strip.jpg` practice; our `CONTACT-SHEET-10fps.png`).

**Applied to C — "state the emotional target per beat before writing the instruction" (`rentok-ad/assets/brief.md`, sha256 `fb6bf460…`: "Specify the intended feeling PER BEAT, not once for the film").** Section 2b writes a feeling on every beat before its motion, camera and sound; this is the discipline that produced the `rentok-ad` prompts and that the board schema lacks (03 §4 row 3). If C wins, the candidate change to the skill is a `feeling` line per board frame — a Controller decision, not made here.

---

## 6. What this plan does not decide (UNKNOWN / for the Controller)

- Whether Veo/Omni can animate flat pixel art without drifting the look: no trial in the map or any case; D1's micro-qualification is the test.
- The reference-image cap on the Vertex ref2v surface at dispatch time.
- Whether the four clips are judged on *the 6.8-s window* or on *the event list*: 06 says the event list; the Controller may prefer equal lengths (trim all to the shortest).
- Whether a C or D win generalises to the full 30-s film (the unit is one beat cluster).
