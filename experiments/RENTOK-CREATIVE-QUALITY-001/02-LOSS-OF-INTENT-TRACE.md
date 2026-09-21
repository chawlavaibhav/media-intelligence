# 02 — Loss-of-intent trace (Lane A, with Lane B as a cross-check)

Experiment `RENTOK-CREATIVE-QUALITY-001`, Phase 1 (USD 0). Written 2026-09-21.
Every judgement in the classification column is **INFERRED** by this session from the OBSERVED sources named in `01-PRODUCTION-CHAIN-RECONSTRUCTION.md`. Quotes are verbatim from the named file. Frames are this session's extractions under `evidence/frames-A/`.

**The question:** the customer's hypothesis (verbatim, `00-EXPERIMENT-CONTRACT.md` §1) is "that creative intelligence may be lost between planning and the final model-facing prompt". This trace follows each consequential creative decision through four hand-offs — plan → asset prompt → animation code → media — and names the hand-off where the intent stopped.

**Classification key** (one per row; where two apply, the earliest loss wins and the other is noted):

| Label | Meaning |
|---|---|
| PRESERVED | what the plan asked for is what the film shows |
| SIMPLIFIED | reached the film in a reduced form; the reduction happened at the hand-off named in the row |
| LOST-IN-PROMPT | the plan held it; the asset prompt did not ask the image model for it; nothing downstream could recover it |
| LOST-IN-ANIMATION | the plan held it (and the assets could support it); the renderer did not implement it |
| METHOD-LIMITED | the chosen method (AI stills + code) could not realise it at any reasonable effort |
| NEVER-SPECIFIED | the plan never held it; no downstream step could lose what was never there |

---

## 1. The trace

Column key: **Intended** (plan quote) · **Basis** (Canon id / customer words / reasoning) · **Plan carrier** (frame/field where it lived) · **Asset prompt?** · **Animation code?** · **Method could?** · **Media** (frame) · **Class**.

### Row 1 — Character expression (the owner's face and inner state)

- **Intended:** nothing. Stage 3 describes the owner as "an ordinary Indian man of about forty, slightly stocky, ordinary (a specific person, `sk_hop_sa_0014`)"; tone "the joke is on the problems, never on the owner". OBSERVED: the words *face, expression, worried, angry, triumphant, smile, grimace* do not occur in `03-CREATIVE.md` Part B or D.
- **Basis available and unused:** customer — "the problems that owner faces", "gets … immunity"; Canon `sk_murch_c003_0020` "Emotion is the first criterion … preserved at all costs" (Lane A cited it only for the length of the GAME OVER hold); `sk_hop_sa_0014` "one imagined typical buyer".
- **Plan carrier:** none (no pose or expression field on the board).
- **Asset prompt?** No. att-001 asks for four locomotion poses and costume; no emotional word. The enemies got faces ("a mean squinting face", "cartoon frowning eyes"); the hero did not.
- **Animation code?** No swap exists; `Sprites.owner()` serves one face in all states (idle/runA/runB/jump, powered or not).
- **Method could?** Yes — a second 4-pose sheet or a 2×4 sheet with hurt/cornered/determined/triumphant faces (one draw, USD 0.067), swapped by code at USD 0.
- **Media:** `t00.90`, `t14.50`, `t18.55`, `t21.40` — the same neutral closed-mouth face at the cold open, at GAME OVER?, at POWER UP! and in the hero frame.
- **Class: NEVER-SPECIFIED.** The prompt could not lose what the plan never held.
- Cross-check, Lane B: the prompt *did* ask for "hurt pose recoiling backwards with a pained face" and "cornered pose"; the checker still found "Facial expression does not change while losing hearts … the owner smiles all the way through". INFERRED: specifying one hurt cell is not the same as directing the character's emotional arc; the arc was never a plan object in either lane.

### Row 2 — Game-world richness (environment, depth, life)

- **Intended:** "a tall PG building facade with stacked floors and small windows filling the upper third … rooftops/water tanks in the middle distance, a lane in front"; "Parallax: background plate scrolls at 0.25× the ground speed; foreground props at 1×"; CA-D6 "the PG building facade with stacked floors behind the level".
- **Basis:** customer delegated the visual treatment; `sk_abcd_0006` "tight framing" (cited for F1 only).
- **Plan carrier:** Stage 3 "World / level design"; board `layout.ground`.
- **Asset prompt?** Yes, faithfully: att-007 asks for the facade, tanks, antenna, "a lower cream building beside it", clouds, "an empty flat packed-earth lane … no ground pattern". One plate.
- **Animation code?** Partly: one plate, tiled ×2 with its mirror, at 0.25×; the "foreground props at 1×" line was not built until repair D-7 added a kerb/tracks/drain/manhole/scooter layer at 1.3×. No mid-ground layer; no life (no windows lighting, no birds, no passers-by); the facade repeats every 1080 px.
- **Method could?** Yes — two or three plates at different depths (USD 0.067 each) and code-drawn props; or a plate drawn at 2× width.
- **Media:** every gameplay frame — one facade pattern repeating; the lane 38.5 % of frame height (checker: "an empty brown band"; producer recorded it before delivery).
- **Class: SIMPLIFIED** (at the animation hand-off: one layer where the plan named three; the lower band by a composition decision at Stage 2/3 — "the world was composed only inside the safe box", case A-004 D-7).

### Row 3 — Scale and framing (how close the viewer is to the action)

- **Intended:** only readability: "props on the sprite readable at ≈ 220 px height"; "Gameplay must still read at phone size". No objective for *presence* or *impact*.
- **Basis available and unused:** `sk_abcd_0006` "tight framing"; `sk_alt_c003_0014` "when [the camera] moves closer the audience moves with it and when it concentrates on one item the audience's attention goes th[ere]"; `sk_hop_sa_0026` a picture must "earn the space it occupies … its size gauged by its importance to the sale".
- **Plan carrier:** Stage 3 3.9; `DesignTokens.owner_h`.
- **Asset prompt?** n/a (scale is a compositing decision).
- **Animation code?** `owner_h = 260` (raised from 220 at repair R4 because "sprites read small at phone size"); no push-in, no zoom, one fixed framing for 27.6 s.
- **Method could?** Yes — a code camera (crop-and-scale of the composed frame) costs USD 0.
- **Media:** owner = 13.5 % of frame height; `t21.40` hero frame: the owner is a 260-px figure in a 1920-px frame with the sack 400 px away.
- **Class: NEVER-SPECIFIED** (framing for impact was not a plan objective; the checker named it: "a game viewed from too far away").

### Row 4 — Player movement / run cycle

- **Intended:** "the owner runs"; jump "0.5 s, code"; clearing run "runs faster".
- **Basis:** customer "It runs".
- **Plan carrier:** Stage 3 mechanics line; Stage 4 A1 "(idle, run A, run B, jump)".
- **Asset prompt?** Yes, as planned: "(2) running with the left leg forward, (3) running with the right leg forward" — a **two-frame** cycle by request.
- **Animation code?** `pose = runA if int(t*8) % 2 == 0 else runB` — 8 swaps/s, no vertical bob, no lean, no arm swing beyond the two drawings; the body is a rigid rectangle sliding at 0 px/s relative to the frame while the world moves.
- **Method could?** Yes — 6–8 run frames on one sheet (USD 0.067) and a 2–4 px bob with a 12–15 Hz cycle at USD 0 (Lane B has a 3-px bob).
- **Media:** `t19.90`, `t21.40` — legs alternate; torso and head do not move. (Classic-animation reasoning, not Canon: a run reads as weight through up-down bob, lean and contact/passing poses; two poses give a "shuffle".)
- **Class: SIMPLIFIED** (at the plan→prompt hand-off: two poses were *asked for*; the renderer added nothing).

### Row 5 — Jump and anticipation

- **Intended:** F1 "the PG owner … runs right and jumps a gap between two rooftop blocks"; F3 "he jumps, clips it, knock-back"; F10 "The owner jumps, grabs the pole".
- **Basis:** customer "a Mario game"; checker Gate 3: "only three jumps in 30 s".
- **Plan carrier:** board F1/F3/F10 prose; Stage 3 "jump arc 0.5 s".
- **Asset prompt?** Yes: "(4) jumping with knees up".
- **Animation code?** `jump = sin(...) * 170/150/200 px`; pose swaps to `jump` for the arc; **there is no gap and there are no rooftop blocks** — the level geometry the board describes for F1 was never drawn (`draw_ground` is a continuous lane); no crouch before take-off, no landing frame, no dust.
- **Method could?** Yes — a gap in `draw_ground` and two extra poses (crouch, land) at USD 0.067; anticipation/landing timing at USD 0.
- **Media:** `t00.90` — the owner airborne over an unbroken lane.
- **Class: LOST-IN-ANIMATION** (the board's gap and the "clips it" contact were not rendered; anticipation was NEVER-SPECIFIED).

### Row 6 — Hit reaction and impact (problem half)

- **Intended:** "each contact costs one health segment (5 → 0) with a white hit-flash and a knock-back of 60 px"; per beat: F2 "runs into it, bounces back", F4 "reaches out, trips", F5 "topples onto him; he is half-buried", F6 "dives at him; he sits down".
- **Basis:** customer "the problems that owner faces"; `sk_whip_0011` "a brand story requires an opposing force"; Canon has nothing on impact (GAP).
- **Plan carrier:** Stage 3 mechanics line + board Part D prose.
- **Asset prompt?** No hurt, tripped, buried or seated pose was requested (att-001 has four locomotion poses only).
- **Animation code?** `flash_sprite()` 0.12 s white silhouette; `knock` 60 px decaying over 0.4 s (F4/F6: 40 px + idle pose); SFX `cue_hit` 0.22 s. No hit-stop, no shake, no obstacle reaction, no pose change beyond idle.
- **Method could?** Yes — hurt/seated poses (USD 0.067); hit-stop (freeze 2–4 frames), 6–10 px screen shake, impact star and dust at USD 0.
- **Media:** `t03.35` — white silhouette next to an unchanged wall; `t14.50` — the owner in the idle pose beside the swarm.
- **Class: LOST-IN-ANIMATION** for the four per-beat pictures ("buried", "sits down", "trips", "bounces"); note that the mechanics line itself (flash + 60 px) was PRESERVED — the plan set a low ceiling and the code met it exactly.

### Row 7a — Obstacle design (what each problem looks like)

- **Intended:** the five pictures in Stage 3's obstacle table ("a wall of paper documents with a faceless silhouette … a big question mark"; "a heavy cloth money sack with a padlock and chain"; tenant "with a suitcase and a coin bag"; "a toppling tower of ledgers … calculator"; "a swarm of angry red speech-bubble tickets").
- **Basis:** customer's five problems; G3 "an obstacle whose picture says the problem before the label does".
- **Asset prompt?** Yes, each faithfully (att-002…006), with the style block.
- **Animation code?** Placed at ×1.15 sizes; recognisable.
- **Media:** `t03.00`, `t06.00`, `t08.80`, `t11.70`, `t13.80`; checker A3 PASS on all five "the picture reads before its label".
- **Class: PRESERVED.**

### Row 7b — Obstacle behaviour (how each problem moves and threatens)

- **Intended:** sack "hopping away from the owner"; tenant "sprinting ahead and out of frame right"; tower "topples onto him"; swarm "dives at him"; wall "the owner runs into it, bounces back".
- **Basis:** plan prose; customer "obstacles".
- **Asset prompt?** The stills were asked for motion states ("mid-hop", "about to fall to the left; a few sheets fluttering", "flying in a loose cluster with small motion lines").
- **Animation code?** `ox = 1080 − tl·v`, `oy = ground − height` — every obstacle is a rigid bitmap sliding left at constant speed on a fixed baseline; no hop, no topple, no dive; after hurting the owner it keeps sliding unchanged; the swarm **disappears at 15.0 s** because F7 is not in `OBST_BEATS`.
- **Method could?** Yes — a hop is a sine on `oy`; a topple is a rotation (`Image.rotate`) over 0.3 s; a dive is a curve on `oy`; all USD 0.
- **Media:** `t06.00` (sack level with the ground, not hopping); frames 14.9 → 15.0 on the 10-fps sheet (swarm present, then gone).
- **Class: LOST-IN-ANIMATION.**

### Row 8 — The low point (GAME OVER?)

- **Intended:** "At health 0 the world desaturates and `GAME OVER?` flashes (0.8 s)"; Murch: emotion "preserve at all costs" → "the GAME OVER? low point is held 0.8 s before the panel".
- **Basis:** `sk_murch_c003_0019/0020`.
- **Animation code?** `desaturate` ramp 14.2–15.0; `GAMEOVER` blink at 4 Hz; `cue_low` 70 Hz 0.8 s; owner idle + 40 px.
- **Media:** `t14.50` — grey world, yellow `GAME OVER?`, owner unchanged.
- **Class: PRESERVED** as specified. (The owner's face at this moment is Row 1.)

### Row 9 — The install / cheat-code moment

- **Intended:** "A dark arcade panel with a cyan border slides up … the two lines type in letter by letter with key-click SFX (1.4 s) … a RentOk-blue phone item drops into the owner's hand (0.4 s), the screen shows the wordmark, a white flash, colour returns, health refills to five in cyan."
- **Basis:** customer "cheat code — install RentOK app", "central turning point"; `sk_abcd_0019` "the ask … a scene from the story itself".
- **Asset prompt?** None by plan (all code) — correct under RR-1/RR-6 (exact text by code).
- **Animation code?** All events present: panel slide 0.5 s, typing 15.8–17.2 (17 key clicks), phone rectangle 70×120 falling 0.4 s, full-frame white 0.1 s, colour back 0.4 s, refill 17.6–18.0, phone held 17.6–19.6 (D-4). The owner does not look up, reach, catch or react; the phone is an unlit rectangle with a 56-px wordmark; no build-up (no riser, no silence, no camera move) before the flash.
- **Method could?** Yes — a "catch" pose (USD 0.067), a screen glow, a 0.3-s silence + riser, a push-in, at USD 0.
- **Media:** `t16.50`, `t17.47`, `t17.80`. Checker: "the app itself is a blue rectangle on screen for a third of a second — the transformation is told by words more than shown by picture".
- **Class: SIMPLIFIED** (the events are all there; the *moment* is carried by typed text, as the checker said).

### Row 10 — The power-up transformation and its effects

- **Intended:** "(a) a pulsing cyan aura (code: 2-px outline + 40 % alpha halo) — the visible change (M5) … Rendered by code from the base sprite (palette shift + aura)"; F8 "cyan aura pulses around him". Stage 1 G5 had proposed "a second character sheet (powered)"; Stage 4 A1p replaced it with code "so identity cannot drift".
- **Basis:** customer "gets a gun sort of power/immunity", "visibly enhanced ability"; `sk_whip_0015` the guide "grants a power".
- **Asset prompt?** No powered pose or powered form was requested — by plan (a recorded decision, not an omission at the prompt step).
- **Animation code?** `Sprites.owner(pose, powered=True)`: a static halo (alpha 110, ±6 px) — **no pulse** (the cached halo does not vary with t) and **no palette shift** (not implemented); the sprite shifts 12 px. HUD colour turns cyan; a phone icon appears.
- **Method could?** Yes — a pulsing halo is one `sin(t)` on alpha (USD 0); a palette shift is a per-pixel map (USD 0); a powered sheet is USD 0.067 with a small identity risk.
- **Media:** `t18.55`, `t21.40` — a thin cyan outline around the same sprite; at 360-px preview a 1–2 px line.
- **Class: SIMPLIFIED** (at the animation hand-off: "pulsing" and "palette shift" not built; the powered *form* was consciously reduced to a recolour at Stage 4 — a direction/method decision, recorded).

### Row 11 — The powered attack

- **Intended:** "fires cyan tick projectiles (one per 0.4 s, 26 px, 900 px/s) that burst each obstacle"; F8 "he fires one test tick upward-right"; hero frame F9.2 "the app-powered owner blasting the rent problem".
- **Basis:** customer "a gun sort of power … runs and kills all the obstacles"; Stage 1 F3 "a projectile/immunity power-up that is not a firearm".
- **Asset prompt?** **No firing, aiming or attack pose was requested.** The four poses are idle/run/run/jump. Nothing downstream can make a running sprite *fire* — the projectile is spawned from empty space 150 px ahead of him.
- **Animation code?** `draw_tick()` — a pixfont `✓` at scale 4 (≈ 20×28 px), one per obstacle (not "one per 0.4 s"), 900 px/s over 0.45 s; SFX `cue_pew` 0.12 s. No arm, no recoil, no muzzle flash, no trail.
- **Method could?** Yes — an aiming/firing pose (USD 0.067) and a trail + muzzle flash + recoil (USD 0).
- **Media:** `t19.90` — a small cyan mark between the owner and the wall; `t21.40` HERO — no projectile in frame at all (the tick has already hit; the sack is intact; the burst is at 21.55). The board's hero frame, "the app-powered owner blasting the rent problem", does not exist as a single frame.
- **Class: LOST-IN-PROMPT** (the only row where the prompt step is the earliest loss: the plan said "fires", the sheet request omitted the pose). Also SIMPLIFIED by the plan's own 26-px projectile and by the code's one-shot-per-obstacle.

### Row 12 — Obstacle-clear payoff and environmental transformation

- **Intended:** "burst each obstacle into pixel debris; the burst spawns the green chip which flies to the checklist"; F9.4 "blasted into one neat stack/screen"; F9.5 "ticks turn each red bubble green"; environment: colour returns at 17.6 s (no further world change specified in Lane A).
- **Basis:** customer "kills all the obstacles"; `sk_hea_mts_0018` rehearsal; Stage 2 permitted claims → chips.
- **Asset prompt?** n/a (code by plan; the obstacle stills are single-state).
- **Animation code?** First render: one generic scale-and-fade for all four (checker D-6). After repair: `debris()` 6×6 tiles with gravity over 0.35 s (wall, sack), `neat_dashboard()` card (tower), `recolour_red_to_green()` (tickets); chip flight 0.35 s. No world change on clearing (the facade, sky and lane are identical before and after the power-up; only the health bar colour and a HUD icon differ).
- **Method could?** Yes; Lane B tinted the whole plate to brand blue after the install (`tinted_plate(after=True)`).
- **Media:** `t20.45`, `t21.65`, `t24.05`, `t25.25`.
- **Class: PRESERVED** (after the USD-0 repair; the first render was LOST-IN-ANIMATION — case A-004 F-08 "the renderer simplified four board-specified clears into one generic routine"). Environmental transformation: NEVER-SPECIFIED in Lane A.

### Row 13 — Camera / scroll

- **Intended:** CA-D11 "the only camera move is the side-scroll follow at the player's run speed; it stops when the game 'pauses' (F7) — both motivated."
- **Basis:** `sk_gote_c003_0006` motivation for transitions; G1 "camera moves a game would never make" would break the game feel.
- **Animation code?** `camera_x(t)`: 400 → pause → 480 px/s → stop. Nothing else.
- **Method could?** A push-in on the install and on each hit is a code crop (USD 0); platform games do use camera zoom/shake at events (reasoning, not Canon).
- **Media:** constant framing 0–27.6 s.
- **Class: PRESERVED** as specified (the plan chose no camera language; a stronger objective would be NEVER-SPECIFIED).

### Row 14 — Audio-visual sync and weight

- **Intended:** SFX "at the board's timestamps"; bed 140 bpm chiptune; power-up arpeggio at 17.4; fanfare at 26.6; loudness −14 LUFS.
- **Animation code / sfx.py?** Cues at `t0 + 0.3 / 0.75 / 1.1` per clear, hits at 3.3/6.1/8.6/11.7/14.1; checker measured "Every board event has a sound at its frame".
- **Media:** sync confirmed by the checker's energy profile (`CHECK-STAGE-5.md` §1).
- **Class: PRESERVED** for sync. Weight (INFERRED, reasoning): all cues are short square-wave blips (0.12–0.28 s), no low-end on impacts, no riser or silence before the flash — the mix is *correct* and *light*; the plan never asked for weight (NEVER-SPECIFIED for impact sound).

### Row 15 — The flag / victory

- **Intended:** "The owner jumps, grabs the pole, the flag rises to the top; `LEVEL CLEAR!` flashes; pixel confetti in brand colours."
- **Basis:** customer "gets the flag"; `sk_ogx_0039` close on the package.
- **Animation code?** Pole enters, owner advances 280 px and jumps 200 px, flag rises 0.8 s, 40 confetti squares, checklist fades (D-2), owner idle at the pole.
- **Media:** `t26.80`, `t27.40`.
- **Class: PRESERVED** (after the D-2 repair; the first render hid the flag behind the checklist).

---

## 2. Counts

| Class | Rows | Count |
|---|---|---|
| PRESERVED | 7a obstacle design · 8 low point · 12 clear payoff (after repair) · 13 camera (as specified) · 14 AV sync · 15 flag | **6** |
| SIMPLIFIED | 2 world · 4 run cycle · 9 install moment · 10 power-up | **4** |
| LOST-IN-ANIMATION | 5 jump/gap · 6 hit reaction · 7b obstacle behaviour | **3** |
| LOST-IN-PROMPT | 11 powered attack (firing pose) | **1** |
| NEVER-SPECIFIED | 1 expression · 3 scale/framing | **2** |
| METHOD-LIMITED | — | **0** |

Sixteen rows. Secondary notes add: anticipation, impact weight, environmental transformation and impact sound as further NEVER-SPECIFIED items; the first render's D-6 and D-2 as LOST-IN-ANIMATION items that the checker caught and the repair round closed.

---

## 3. Synthesis (INFERRED)

### Where the losses cluster

1. **At the direction layer, by omission (NEVER-SPECIFIED + the ceiling-setting lines of SIMPLIFIED rows).** The plan is precise about *events, timing, strings and safe zones* and silent about *how anything should feel*: no expression arc, no framing objective, no impact language, no motion vocabulary beyond "jump arc 0.5 s" and "knock-back 60 px". Where the plan did write a feeling ("the low point is held"), the code delivered it. Where it wrote a picture ("half-buried", "hops"), the code often did not. Where it wrote nothing (the owner's face), nothing arrived. This is cause (A) in the experiment's terms — but *under-specified for feel*, not *mis-specified*: the ad structure is sound and Canon-backed.

2. **At the animation renderer (LOST-IN-ANIMATION 3 + the animation-side SIMPLIFIED rows).** The renderer is a *timeline compositor*: it places rigid bitmaps at positions that are functions of time. Its primitive set (01 §7a) has no anticipation, hit-stop, shake, squash, bob, easing, expression swap or attack pose (01 §7b). Every board motion that needed one of these was reduced to "slide, flash 0.12 s, offset 60 px". The independent checker caught the loudest of these (D-6: four clears rendered as one routine; D-3: a square instead of a tick; D-4: a phone that vanished) and the repair round fixed them at USD 0 — which shows the renderer *can* be made to honour the board when someone names the gap.

3. **At the prompt-translation step: one row.** The firing pose. Otherwise the seven prompts carry the plan's nouns, props, style and poses faithfully (01 §6). The step the customer suspected is the *least* lossy of the four hand-offs in this record.

4. **Method: zero rows.** Nothing the plan asked for is beyond AI stills + code; the method's real cost is that *every* quality item is hand-built (a pose is a draw, a shake is code), so under a plan that does not name them, none gets built. A video model supplies secondary motion, expression and lighting change whether or not the plan names them — which is why Treatment D (05) is worth running as a *method* test, not because the method was proven limiting here.

### What the checkers and the customer said — corroboration and contradiction

- **Corroborates the cluster.** Lane A's Gate-3 checker, before any spend: "the first half is an auto-runner … more scripted than played … Whether it *feels* like a game is exactly what the USD-0 animatic exists to test" — and the animatic test that followed checked timing, safe zones and readability, not feel (05-EXECUTION §5: R1 ground line, R2 collisions). Lane A's Stage-5 checker: "the transformation is told by words more than shown by picture, and the customer asked for it to be shown"; "a game viewed from too far away". Lane B's checker: "the owner smiles all the way through … calm and friendly rather than dramatic"; "runner with labels". Four independent readings, two lanes, the same two gaps: **presence/impact** and **the character's felt state**.

- **Contradicts the customer's hypothesis as the *main* cause.** Lane B put expression ("with a pained face") and before/after states *into the prompts* and *implemented* a hurt pose, a cornered pose, a world tint and a beam — more creative information reached its prompts and its code than Lane A's — and Lane B was **not** the preferred film (customer: "video 2 is better", Y = Lane A; the one reason given was Lane B's voice). n = 1, confounded by the voice; but it is the only paired evidence in the record, and it does not point at the prompt step.

- **Contradicts "lost" as the right verb.** The customer's own words carried no creative-quality target beyond "feel like an actual platform game"; the acceptance contract graded presence (A1–A11) and left quality to one sentence (§B). Both lanes optimised what was graded. The intelligence was not *lost in transit*; most of it was *never loaded* — and the part that was loaded was under-served by a renderer with a small vocabulary.

- **Customer acceptance.** Both films were ACCEPTED blind; the later verdict (`00-EXPERIMENT-CONTRACT.md` §1: Lane A "Better overall and accepted, but still below the desired creative standard"; "the question-answering process has improved the result. However, the final creative quality remains insufficient") is consistent with this trace: every required event is present (PRESERVED 6 of 16 on the rows that carry compliance) and the rows that carry *feel* (1, 3, 4, 5, 6, 7b, 9, 10, 11) are SIMPLIFIED, LOST or NEVER-SPECIFIED.

### Consequence for the three candidate causes

| Cause | Evidence in this trace | Reading (INFERRED) |
|---|---|---|
| (A) direction under-ambitious / mis-specified | 2 NEVER-SPECIFIED rows + the plan's own low ceilings ("knock-back 60 px", 26-px projectile, four locomotion poses, no camera language, no expression) | **Supported, as under-specification for feel** — the largest contributor |
| (B) loss in translation to prompts / animation instructions | prompt step: 1 row; animation step: 3 LOST + 3 SIMPLIFIED | **Supported for the animation step, refuted for the prompt step** — the customer's suspected location is the wrong one |
| (C) method limits | 0 rows METHOD-LIMITED; every gap is buildable at USD 0–0.07 | **Not supported on this evidence**; untested whether a video model would deliver the unbuilt qualities more cheaply than writing them — that is Treatment D's question |

### What would have caught it earlier (INFERRED, for the Controller)

The USD-0 animatic was the right instrument aimed at the wrong target: it was inspected for timing, safe zones and readability and passed; nobody was asked to judge *feel* on it, and Canon gave the checker nothing to judge feel against. A feel rubric (06) applied to the animatic — anticipation present? impact lands? character reacts? — would have surfaced rows 1, 4, 5, 6, 7b, 9, 10, 11 before any draw.

---

## 4. Evidence index for this file

- Plan quotes: `A/stages/03-CREATIVE.md` @ 7dab37a (sha256 `9c68ad65…` per case A-004 EVIDENCE-MAP); `A/stages/01-INTENT.md`.
- Prompts: `A/gen/ATTEMPTS.jsonl` (sha256 `406e38c9…`), frozen copy in `treatments/A-baseline/frozen-inputs/`.
- Code: `A/tools/render_game.py` (sha256 `f9a819f0…`), `A/tools/sfx.py` (`d2433705…`), frozen copies as above.
- Checker quotes: `A/stages/CHECK-GATES-1-4.md`, `A/stages/CHECK-STAGE-5.md`, `B/stages/CHECK-STAGE-5.md`.
- Verdict: `…-ctrl/experiments/RENTOK-TWO-LANE-2026-09-20/05-BLIND-PACKET/VERDICTS.md`.
- Canon ids re-read in `canon/knowledge/current/**` of this worktree (see 01 §3).
- Frames: `evidence/frames-A/*.png`, `evidence/CONTACT-SHEET-A-2fps.png`, `treatments/A-baseline/CONTACT-SHEET-10fps.png`.
