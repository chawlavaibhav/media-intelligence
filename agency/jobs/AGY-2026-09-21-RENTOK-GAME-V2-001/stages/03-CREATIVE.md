# Stage 3 — Creative, rewritten "the Video-4 way" (gate: a board exists with feeling / framing / impact on every beat)

Job `AGY-2026-09-21-RENTOK-GAME-V2-001`. Companion files: `board.json` (BOARD-v2, serialised by `tools/make_board.py` — the board is authored there as data), `copy-deck.json` (carried over byte-for-byte from Lane A; no string changed), `tools/render_v2.py` (the renderer that executes the board), `gen/animatic-v2.mp4` + `qa/animatic-v2/` (the USD-0 proof).

## What changed vs the accepted Lane A film, in one paragraph

Same story spine, same timings, same 27 strings, same brand decisions. What changed is the **direction**: every one of the fifteen beats now states what the viewer should feel, how big the owner is in the frame at the beat's focus and where the eye goes, and which impact primitives fire when — and the renderer executes those fields instead of a slide/flash vocabulary. Treatment C's method (CQ-001 clip 4, 14.0–20.8 s) is applied to **all five obstacle beats**, the turning point, the power-up, all five clears and the flag. The Lane A board carried the events; this board carries the feeling of them.

## Part A — Canon and reasoning, honestly

Canon ids used (retrieved by Lane A at Stage 3 Part A2 and by Treatment C at CQ-001 05 §2a; texts re-read there, not reworded here):
- `sk_murch_c003_0020` — emotion first, "preserved at all costs" → a stated feeling per beat, and where a feeling and a tidy layout conflict, the feeling wins (the safe box stays).
- `sk_alt_c003_0014` — the camera is the audience's eye; closer = attention → push-in at every hit, the install and the flag.
- `sk_alt_c003_0022` — lighting fluctuates with mood → cold grade + vignette at the low point; bright lift + cyan highlights after the flash.
- `sk_alt_c003_0015` — tonal separation → the swarm stays red in the cold world; the powered owner is the brightest thing in frame.
- `sk_conv_c003_0019` — withdrawing sound makes the audience listen → 0.3 s near-silence before the flash.
- `sk_hop_sa_0026` — size by importance → the owner is ≥ 0.25 of the frame height at the hits, the gift and the power; ≈ 0.15 during the clearing run, where the world changing is the picture.
- `sk_whip_0015` — a power granted, visible on the body → aura, palette shift, phone in hand, fire poses.
- `sk_abcd_0006`, `sk_gote_c003_0004` — tight framing; each new view reveals something → every push-in shows the face or the object that matters.
- Lane A's structural ids stand unchanged (`sk_abcd_0007/0010/0011`, `sk_whip_0011`, `sk_sb_c003_0008/0014`, `sk_hea_mts_0018/0009`, `sk_ms_c003_0019`, `sk_gote_c003_0006`, `sk_murch_c003_0013`, `sk_gos_c003_0007`, `sk_wcag_0001/0002`, `sk_sam_c003_0021`, `sk_vig_c003_0013`, `sk_ogl_c003_0014`).

**GAP (unchanged from CQ-001):** Canon holds nothing on animation principles or game feel. The motion below rests on named references used as reasoning, not Canon: the twelve principles of animation (Thomas & Johnston, *The Illusion of Life*, 1981 — anticipation, follow-through, timing, exaggeration, staging, easing/slow-in-slow-out) and the game-feel vocabulary (Swink, *Game Feel*, 2008; Jonasson & Purho, "Juice it or lose it", 2012 — hit-stop, screen shake, impact frames, particles). Recorded in `board.json principles_note`.

## Part B — The board schema change (the candidate pattern)

BOARD-v2 = BOARD-v1 + three fields per beat, filled for all fifteen:

| Field | What it holds | Who consumes it |
|---|---|---|
| `feeling` | what the viewer should feel (one or two words + one line) | the producer, when judging the animatic; the checker |
| `framing` | `owner_frac_target` (owner height ÷ 1920 at `focus_t`), `camera` keyframes (t, scale, cx, ease), `eye` (1st/2nd/3rd read), `target_note` where a pose is inherently short | `render_v2.py` reads the camera keyframes; `qa_checks.py` asserts `owner_frac ≥ target` at `focus_t` from the layout log |
| `impact` | the primitives that fire, named with timings: `anticipation`, `hit_stop` (frames), `shake` (amp, decay), `impact_star`, `impact_frame`, `particles` (kind, n), `grade`, `pose` (t0, t1, pose, knock/arc params), `audio` (cue), `obstacle_motion` (named curve), `hud_flash`, `ring`, `muzzle_flash`, `chip_flight`, `payoff` | `render_v2.py` reads hit-stops, shakes, poses and camera from the board; `sfx_v2.py` reads the audio cues; obstacle motion curves are code keyed by the `motion` name and `contact_t` |

The camera has one placement rule (`layout.camera_cy_rule`): `cy(s) = 750 + 170/s`, so the world row y = 750 always maps to screen y = 790 — the play band sits below the label zone at every zoom and the UI (drawn after the camera transform) never lands on him. Two token changes: ground line 1180 → 1220 and owner 260 → 300 px (so the 1.6× push gives 480 px = 0.25 of the frame).

## Part C — The per-beat feeling table (the direction, in short)

| Beat | t (s) | Feeling | Framing (owner ÷ frame at focus; camera; eye) | Impact (what fires) |
|---|---|---|---|---|
| F1 cold open | 0.0–1.8 | bustle | 0.15 @ 0.9; ×1.0; running owner → HUD name → LEVEL 1 | run lean + bob; 2-frame brace before the jump; landing dust + `land` pose |
| F2 wall | 1.8–4.6 | dread → bonk | 0.25 @ 3.5; push ×1.6 at 3.25, hold, back by 4.4; wall leaning in → his brace → star + HUD blink | wall leans 0→6° from 2.6 with sheets fluttering off its top; brace 3.2; **hit 3.3**: hit-stop 3 f, white silhouette, impact star, shake 10 px, dust 8 + sheets 6, `hurt` knock-back 90 px eased, HUD segment blinks; `dazed` with stars 3.75–4.25 |
| F3 sack | 4.6–7.4 | menace with a grin | 0.25 @ 6.3; push ×1.6 at 6.05, back by 7.1; hopping sack → crouch-and-jump → mid-air star | hop every 0.45 s (110 px, 1-frame squash, dust per landing); brace 5.5; jump 5.6–6.1; **hit 6.1** mid-air: hit-stop 2 f, star, silhouette, shake 8, `hurt` falls 125 px, `land` gets up |
| F4 tenant | 7.4–10.2 | surprise → helplessness | 0.21 @ 8.55 (reach pose); push ×1.4 at 8.4 centred right; runner overtaking → look-back and reach → trip | tenant sprints past from BEHIND at 1.9× scroll with speed lines, bouncing suitcase, coins spilling; `lookback` 8.2, `reach` 8.45; **contact 8.6**: hit-stop 2 f, shake 6, dust 10, `trip` sprawled, `cornered` getting up |
| F5 tower | 10.2–12.6 | dread (wobble) → crash → buried | 0.16 @ 11.9 (crouched `cover`; standing-equivalent 0.23); push ×1.5; wobbling tower → cover pose → the crash | wobble ±3° growing; topples about its base centre 0→85° over 0.35 s (ease-in); `cover` from 11.45; **crash 11.7**: hit-stop 3 f, shake 14 px (the biggest), star, white tower, dust 16 + sheets 12; the tower lands ON him and is drawn in front (half-buried); the scroll pauses 11.7–12.35; `cornered` crawls out |
| F6 swarm | 12.6–15.0 | panic → pain → defeat | 0.25 @ 14.35; push ×1.6 at 14.05, held; swarm lunging → hit → him on one knee under GAME OVER? in a cold frame | wobble; lunge from 13.9; brace 14.0; **hit 14.1**: hit-stop 3 f, silhouette, star, shake 10, dust; swarm recoils and hovers over him, still red; cold grade eased in over 0.9 s + 35 % vignette; the scroll pauses from 14.1 |
| F7 code → gift | 15.0–18.0 | a held breath → awe | 0.22 @ 17.4 (catch); ×1.45 during the panel (so the kneeling owner and the raised hand sit below the panel — closes C's limitation 5), snap to ×1.6 on the flash; panel → him looking up at 16.8 → the phone | swarm drifts up and out 15.0–15.45 fading; typing 15.8–17.2 unchanged; `cornered_up` 16.8; the phone drops OUT of the panel (its bottom edge) into his hand 17.2–17.4 with trail + glow; **install 17.4**; near-silence 17.3–17.6; **flash from the phone 17.6** + one white frame, 6-px shake; grade to bright; health refills in cyan one segment per 0.08 s; panel fades from 17.4 |
| F8 power | 18.0–19.6 | power, rising confidence | 0.24 @ 18.4; ×1.6 held, pull-out to ×1.0 over 19.3–19.7 (the world opens); the glowing owner → POWER UP! → the tick leaving the phone | `powered` (aura pulse 3 Hz, shirt to cyan, phone forward), 10 sparks; `windup` 18.2; `fire` 18.4 with muzzle flash, recoil, tick + trail rising; HUD phone icon |
| F9.1–9.5 clears | 19.6–25.6 (1.2 each) | glee · release · control · order · relief | 0.15; ×1.15 pulse on each hit centred toward the obstacle; obstacle entering → the fire → the payoff + chip pop | run with aura; `runfire` at +0.25; muzzle flash + tick (42 px) + trail at +0.3; **hit +0.75**: hit-stop 2 f, white obstacle 2 f, shockwave ring, shake 8; payoffs — wall: debris + 14 fluttering sheets; sack: debris + 12-coin fountain; tenant: cyan ledger tag with a green tick pop, he keeps running (tracked, not stopped); tower: 12 sheets + the dashboard card shrinking to the checklist; swarm: red → green sweep with 5 pop rings, then fade; chip flight ease-out + 3-frame landing pop; label 0.4-s recall flash |
| F10 flag | 25.6–27.6 | triumph | 0.19 @ 26.9 (cheer); push ×1.3 centred on him + the pole from 26.55; pole entering → jump and cheer → flag rising with LEVEL CLEAR! and confetti | brace 26.1; jump 26.2–26.6 (200 px, 280 px forward); **flag reached 26.6**; `cheer` with a hop at 26.9; two confetti fountains; checklist fades 26.6–27.0 (Lane A D-2); the flag stops just under the label zone (pole top 792) |
| F11 end card | 27.6–30.0 | calm, clear close | — | 0.3-s dim to the card blue; wordmark, CTA, URL; nothing moves for the last 1.0 s |

Hero frame: **frame 651 (t = 21.70 s)** — F9.2, the padlocked sack bursting into a coin fountain inside the shockwave, the owner powered mid-run with the aura, the first chip on the checklist and the second in flight. Without any copy it shows the app-powered owner blasting the rent problem (Lane A's hero frame was 21.40, before the burst).

Copy deck: no string needed a change; the panel fade moves from 17.6 to 17.4 (recorded reason: the gift needs the frame; the code is complete at 17.2 and readable until 17.4).

## Part D — The muted test, readability, IP

- Muted: yes — every beat carries its meaning in picture + on-screen label; sound adds weight only.
- Readability: the UI is Lane A's (every string, scale, backing, position), drawn after the camera transform, so the Lane A audition and contrast measurements hold; the animatic's DET run: C1 bounds 0 failures over 4,000+ boxes, C2 min contrast 6.08, C5 text-text disjoint 0, **C5b graphic-vs-text disjoint 0** (new gate: the owner, obstacles, phone, flag and tick never sit under a text backing).
- IP: the generic "?" on the document wall is the unknown tenant (a Lane A accepted still), not a block; the health bar is ▮▯ segments; the star, ring, muzzle flash, sparks, confetti and coins are plain code shapes; no Nintendo cue was added.

## Part E — Judgement on the USD-0 animatic (`gen/animatic-v2.mp4`, 900 frames; judged by the producer on `qa/animatic-v2/CONTACT-SHEET.png` and beat strips)

OBSERVED on the frames: every hit now has a build (lean / hop / overtaking / wobble / lunge), a stop (the freeze, the silhouette, the star), and an aftermath (knock-back, dazed, sprawled, buried, cornered). The world stops moving when he is buried and when he is down — the tower stays on him, the swarm hangs over him — which the first animatic did not do (fixed at USD 0). The gift now visibly comes out of the cheat panel. The clearing run's five payoffs are distinct. The flag beat has a jump, a cheer and confetti. What is NOT judgeable on the animatic: the eight new poses (look-back, reach, trip, cover, running-fire, cheer, dazed, land) are stand-ins built from accepted bitmaps (magenta dot) — that is what the one paid sheet is for (Stage 4). Decision: timing stands; proceed to the paid draw.

## 3.7 Every mandatory event on a numbered frame (unchanged from Lane A, re-verified on this board)

M1 F1–F10 · M2 F1 (HUD name + props) and every gameplay frame · M3 F2–F6 and F9.1–F9.5 · M4 F7 (17.4 s) · M5 F8 · M6 F9.1–F9.5 + F10 (26.6 s) · M7 30.0 s · M8 every string inside (65,288)–(888,1248) (DET C1) · M9 Stage 2c table · M10 F9.x chips + F11 · M11 copy deck only, `claims_source_map` unchanged.

Not a verdict. Written by the producer session.
