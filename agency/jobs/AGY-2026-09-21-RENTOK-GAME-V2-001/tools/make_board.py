#!/usr/bin/env python3
"""make_board.py — serialises the Stage 3 board (BOARD-v2) to board.json. The board is authored HERE as data; this
script only writes it out (one source, no hand-typed JSON). Run: /usr/bin/python3 tools/make_board.py

BOARD-v2 = Lane A's BOARD-v1 (n, t0, t1, beat, strings, mandatory) + THREE NEW FIELDS PER BEAT (the CQ-001 §6 change):
  feeling  — what the viewer should feel during the beat (one or two words + one line)
  framing  — owner height as a fraction of the 1920-px frame at the beat's focus (target >= 0.25 where the beat is about him),
             the camera keyframes that achieve it, and where the eye goes (first, second, third read)
  impact   — the primitives that fire, NAMED with their timings: anticipation, hit_stop, shake, impact_star, impact_frame,
             particles, grade, camera, pose, hud_flash, audio, ring, muzzle_flash, chip_pop, obstacle motion
The renderer (tools/render_v2.py) READS camera, hit_stop, shake, pose and audio entries from these lists — they are not
hard-coded constants — so the board is the single source of the direction. Obstacle motion curves are code keyed by the
`motion` name and `contact_t` given here.
"""
import json
from pathlib import Path

JOB = Path(__file__).resolve().parent.parent
FPS = 30
CLEAR_V = 480; PROB_V = 400

def cam(t, scale, cx=540, ease=0.25):
    return {"t": t, "scale": scale, "cx": cx, "ease_s": ease}

def hit(t, frames): return {"t": t, "primitive": "hit_stop", "frames": frames}
def shake(t, amp, decay): return {"t": t, "primitive": "shake", "amp_px": amp, "decay_s": decay}
def pose(t0, t1, name, note="", **kw):
    d = {"t0": t0, "t1": t1, "primitive": "pose", "pose": name, "note": note}; d.update(kw); return d
def audio(t, cue, note=""): return {"t": t, "primitive": "audio", "cue": cue, "note": note}
def prim(t, name, **kw): d = {"t": t, "primitive": name}; d.update(kw); return d

frames = []

# ── F1 cold open ─────────────────────────────────────────────────────────────
frames.append({
 "n": "F1", "t0": 0.0, "t1": 1.8, "beat": "cold_open_mid_action", "strings": ["HUD_NAME", "HUD_HEALTH_5", "LEVEL"], "mandatory": ["M1", "M2"],
 "feeling": "bustle — a game already running; a man with too much to carry, moving fast",
 "framing": {"owner_frac_target": 0.15, "focus_t": 0.9, "camera": [cam(0.0, 1.0)], "eye": "1st the running owner (lean + bob), 2nd the HUD name PG OWNER, 3rd the LEVEL 1 flash"},
 "impact": [pose(0.0, 0.55, "run", "lean 8 deg, 3-px bob at 4 Hz"), prim(0.55, "anticipation", pose="brace", frames=2, note="weight back before the jump"),
            pose(0.6, 1.1, "jump", "arc 170 px", arc_px=170), prim(1.1, "particles", kind="dust", n=6, note="landing puff"), pose(1.1, 1.2, "land", "knees bent, 3 frames follow-through"),
            audio(0.6, "jump"), audio(1.1, "land")]})

# ── the five obstacle beats (problem half) ───────────────────────────────────
OB = [
 (2, 1.8, 4.6, 1, "obstacle_1_tenant_verification", "OBST_1", "HUD_HEALTH_4", 3.3, "lean_in",
  "dread, then a bonk — the paperwork looms and he runs straight into it",
  "1st the wall leaning in from the right (sheets fluttering off its top), 2nd his brace, 3rd the star + HUD segment blink",
  [prim(2.6, "obstacle_motion", motion="lean_in", note="lean grows 0->6 deg 2.6-3.3 s about its base; 6 paper sheets flutter off the top from 2.8 s"),
   prim(3.2, "anticipation", pose="brace", note="0.1 s before contact"), hit(3.3, 3), prim(3.3, "impact_frame", target="owner", note="85 % white silhouette 2 frames"),
   prim(3.3, "impact_star", at="contact"), shake(3.3, 10, 0.25), prim(3.3, "particles", kind="dust", n=8), prim(3.3, "particles", kind="sheet", n=6, note="off the wall top"),
   pose(3.3, 3.75, "hurt", "knock-back 90 px ease-out 0.4 s", knock_px=90, knock_s=0.4), pose(3.75, 4.25, "dazed", "stars orbit the head (code)", knock_px=90, hold=True), prim(3.3, "hud_flash", note="lost segment blinks 0.4 s"),
   audio(3.1, "riser"), audio(3.3, "thump+hit"), audio(3.3, "bed_duck", note="bed cut 0.1 s then -6 dB to 3.8")],
  [cam(3.25, 1.6, 540, 0.2), cam(3.9, 1.6), cam(4.4, 1.0, 540, 0.5)], 3.5),
 (3, 4.6, 7.4, 2, "obstacle_2_collecting_rent", "OBST_2", "HUD_HEALTH_3", 6.1, "hop",
  "menace with a grin — the padlocked sack hops at him; he jumps and still gets clipped",
  "1st the hopping sack (dust on each landing), 2nd his crouch-and-jump, 3rd the mid-air star",
  [prim(4.6, "obstacle_motion", motion="hop", note="hop every 0.45 s, 110 px, 1-frame 6 % squash on landing, dust puff per landing; chain rattle per hop"),
   prim(5.5, "anticipation", pose="brace", note="crouch 3 frames before the jump"), pose(5.6, 6.1, "jump", "arc 130 px", arc_px=130), hit(6.1, 2), prim(6.1, "impact_star", at="contact"),
   prim(6.1, "impact_frame", target="owner"), shake(6.1, 8, 0.2), pose(6.1, 6.6, "hurt", "falls back to the ground by 6.5, knock 70 px", knock_px=70, knock_s=0.4, fall_from_px=125, fall_s=0.4), pose(6.6, 7.0, "land", "gets up", knock_px=70, hold=True),
   prim(6.1, "hud_flash"), audio(4.9, "hop"), audio(5.35, "hop"), audio(5.8, "hop"), audio(6.1, "thump+hit"), audio(6.1, "bed_duck")],
  [cam(6.05, 1.6, 540, 0.2), cam(6.6, 1.6), cam(7.1, 1.0, 540, 0.5)], 6.3),
 (4, 7.4, 10.2, 3, "obstacle_3_left_without_paying", "OBST_3", "HUD_HEALTH_2", 8.6, "sprint_past",
  "surprise, then helplessness — the tenant sprints past from behind dragging the suitcase; he grabs at air and trips",
  "1st the tenant overtaking (speed lines, bouncing suitcase, coins spilling), 2nd his look-back and reach, 3rd the trip and dust",
  [prim(7.4, "obstacle_motion", motion="sprint_past", note="enters from the LEFT at 1.9x scroll speed; suitcase bobs 8 px at 6 Hz; 3 speed lines; coins spill every 0.1 s"),
   pose(8.2, 8.45, "lookback", "hears him coming"), pose(8.45, 8.6, "reach", "arm out — anticipation of the grab"), hit(8.6, 2), shake(8.6, 6, 0.2),
   prim(8.6, "particles", kind="dust", n=10), pose(8.6, 9.2, "trip", "sprawled, book skids 40 px", knock_px=-30, knock_s=0.3), pose(9.2, 9.6, "cornered", "on one knee, getting up", knock_px=-30, hold=True),
   prim(8.6, "hud_flash"), audio(7.6, "steps", note="rapid steps to 9.2"), audio(8.55, "whoosh"), audio(8.6, "trip"), audio(8.65, "coins"), audio(8.6, "bed_duck")],
  [cam(8.4, 1.5, 600, 0.2), cam(9.1, 1.5, 600), cam(9.6, 1.0, 540, 0.5)], 8.55),   # R-1: 1.4 -> 1.5 (drawn reach pose is 6 % shorter than its stand-in; 1.45 measured 0.209 by rounding)
 (5, 10.2, 12.6, 4, "obstacle_4_no_reconciliation", "OBST_4", "HUD_HEALTH_1", 11.7, "topple",
  "dread (it wobbles) then a crash — the ledger tower topples onto him and he is half-buried",
  "1st the wobbling tower, 2nd his cover pose (arms over the head), 3rd the crash: biggest shake, dust cloud, papers",
  [prim(10.2, "obstacle_motion", motion="topple", note="wobble +/-3 deg at 2 Hz growing; from 11.35 rotates about its base toward him 0->-85 deg over 0.35 s (ease-in); lands ON him at 11.7 and is drawn in front of him (half-buried)"),
   pose(11.45, 11.7, "cover", "sees it coming — anticipation"), hit(11.7, 3), shake(11.7, 14, 0.3), prim(11.7, "impact_star", at="contact"), prim(11.7, "impact_frame", target="obstacle"),
   prim(11.7, "particles", kind="dust", n=16), prim(11.7, "particles", kind="sheet", n=12), pose(11.7, 12.3, "cover", "under the tower", knock_px=30, knock_s=0.2), pose(12.3, 12.6, "cornered", "crawls out as the world scrolls it away", knock_px=30, hold=True),
   prim(11.7, "hud_flash"), audio(11.3, "creak"), audio(11.7, "crash+thump"), audio(11.75, "papers"), audio(11.7, "bed_duck")],
  [cam(11.65, 1.5, 540, 0.2), cam(12.2, 1.5), cam(12.6, 1.0, 540, 0.4)], 11.9),
 (6, 12.6, 15.0, 5, "obstacle_5_complaints_game_over", "OBST_5", "HUD_HEALTH_0", 14.1, "swoop",
  "panic, pain, defeat — the swarm swoops, lands, and the world goes cold",
  "1st the swarm accelerating at him (buzz), 2nd the hit (star, silhouette, shake), 3rd him on one knee under GAME OVER? in a cold frame",
  [prim(12.6, "obstacle_motion", motion="swoop", note="enters with a 10-px wobble; at 13.9 lunges (extra 300 px/s for 0.2 s); recoils 30 px after the hit; hovers over him, still red; drifts up and out 15.0-15.6"),
   prim(14.0, "anticipation", pose="brace"), hit(14.1, 3), prim(14.1, "impact_frame", target="owner"), prim(14.1, "impact_star", at="contact"), shake(14.1, 10, 0.25),
   prim(14.1, "particles", kind="dust", n=8), pose(14.1, 14.5, "hurt", "knock 90 px ease-out", knock_px=90, knock_s=0.4), pose(14.5, 16.8, "cornered", "on one knee through the panel", knock_px=20, hold=True),
   prim(14.1, "grade", to="cold", ease_s=0.9, note="RGB x (0.55,0.60,0.75) + 35 % vignette; the swarm stays red (tonal separation)"), prim(14.1, "hud_flash"),
   audio(12.8, "buzz", note="swarm buzz to 15.6"), audio(13.9, "riser"), audio(14.1, "thump+hit"), audio(14.2, "low"), audio(14.1, "bed_cold", note="bed cut 0.1 s, then low-pass 800 Hz at -7 dB until 17.6")],
  [cam(14.05, 1.6, 540, 0.25), cam(15.0, 1.6)], 14.35),
]
TARGET = {2: (0.25, "hurt pose (standing height) at x1.6"), 3: (0.25, "hurt pose mid-air at x1.6"), 4: (0.21, "reach pose at x1.5 (R-1) — the beat is about him AND the runner; both must be in frame"),
          5: (0.16, "cover pose is crouched (~0.72 of standing) at x1.5 = the standing-equivalent 0.23; the tower on him is the picture"), 6: (0.25, "hurt pose at x1.6")}
for (fn, t0, t1, k, beat, s, hs, ct, motion, feeling, eye, impact, cams, focus) in OB:
    frames.append({"n": f"F{fn}", "t0": t0, "t1": t1, "beat": beat, "strings": [s, hs] + (["GAMEOVER"] if fn == 6 else []), "mandatory": ["M3"],
                   "obstacle": k, "contact_t": ct, "motion": motion, "feeling": feeling,
                   "framing": {"owner_frac_target": TARGET[fn][0], "target_note": TARGET[fn][1], "focus_t": focus, "camera": cams, "eye": eye}, "impact": impact})

# ── F7 the code / the gift ───────────────────────────────────────────────────
frames.append({
 "n": "F7", "t0": 15.0, "t1": 18.0, "beat": "cheat_code_install_rentok_turning_point", "strings": ["CHEAT_HDR", "CHEAT_1", "CHEAT_2", "HUD_HEALTH_5"], "mandatory": ["M4"],
 "feeling": "a held breath (the code types while he kneels in a cold world) → awe (the phone falls into his hand and lights the frame)",
 "framing": {"owner_frac_target": 0.22, "target_note": "catch pose at x1.45 (kneeling 0.16 during the panel)", "focus_t": 17.4, "camera": [cam(15.0, 1.6), cam(15.4, 1.45, 540, 0.4), cam(17.6, 1.6, 540, 0.05)],
             "eye": "1st the panel and the typing, 2nd him looking up at 16.8, 3rd the falling phone and its glow; at 17.6 the flash from the phone owns the frame",
             "note": "camera 1.45 during the panel so the kneeling owner and the raised catching hand sit BELOW the panel's bottom edge (920) — closes Treatment C limitation #5"},
 "impact": [prim(15.0, "obstacle_motion", motion="drift_off", note="swarm drifts up and out 15.0-15.6 (ease-in)"), pose(16.8, 17.35, "cornered_up", "head lifted, hopeful", knock_px=20, hold=True),
            prim(17.2, "phone_fall", note="from y 160 to the hand over 0.2 s ease-in, 3-copy cyan trail, Gaussian glow"), pose(17.35, 17.6, "catch", "arm raised, hand open", knock_px=20, hold=True),
            prim(17.4, "install", note="phone lands in the hand = install_event_t; screen lights cyan over 0.2 s"), prim(17.3, "audio_withdraw", note="bed -24 dB, no SFX 17.3-17.6 (sk_conv_c003_0019)"),
            prim(17.6, "flash_from_source", note="cyan-white radial 60->1560 px over 5 frames from the phone + one full-white impact frame"), shake(17.6, 6, 0.15),
            prim(17.6, "grade", to="bright", note="+10 % lift, cyan cast in highlights — the world after is brighter than the world before"), prim(17.6, "hud_refill", note="five segments refill in cyan one per 0.08 s with a tick each"),
            audio(15.8, "keys", note="17 key clicks 15.8-17.2"), audio(17.6, "impact+bassdrop"), audio(17.62, "powerup"), audio(17.6, "bed_level2", note="bed returns full-band one semitone up")]})

# ── F8 power ─────────────────────────────────────────────────────────────────
frames.append({
 "n": "F8", "t0": 18.0, "t1": 19.6, "beat": "power_up", "strings": ["POWERUP"], "mandatory": ["M5"],
 "feeling": "power, rising confidence — chest out, aura pulsing, the first tick fired; then the world opens up as he sets off",
 "framing": {"owner_frac_target": 0.24, "target_note": "fire pose at x1.6 (300 px x 1.6 / 1920 = 0.25, rounded)", "focus_t": 18.4, "camera": [cam(18.0, 1.6), cam(19.3, 1.6), cam(19.7, 1.0, 540, 0.4)],
             "eye": "1st the glowing owner (the brightest thing in frame), 2nd the POWER UP! flash, 3rd the tick leaving the phone with its trail"},
 "impact": [pose(17.6, 18.2, "powered", "phone forward, half-smile; aura alpha 100 +/- 40 at 3 Hz; shirt blue shifted to cyan"), prim(17.65, "particles", kind="spark", n=10, note="orbit 0.6 s"),
            pose(18.2, 18.4, "windup", "arm back — anticipation"), pose(18.4, 18.75, "fire", "muzzle flash 0.08 s, recoil 8 px, tick + 5-copy trail rising"), pose(18.75, 19.6, "powered"),
            prim(18.0, "hud_phone_icon"), audio(18.4, "pew"), audio(17.7, "sparks", note="6 sparks 17.7-18.05")]})

# ── F9.x five clears ─────────────────────────────────────────────────────────
CL = [
 ("F9.1", 19.6, 1, "clear_1_verification", "CHIP_1", "glee — the wall that stopped him bursts into paper", "burst_sheets",
  "the wall re-enters leaning; on the hit: debris tiles + 14 paper sheets that flutter + dust; the silhouette drops", "wall re-enters at x1.15 leaning 6 deg"),
 ("F9.2", 20.8, 2, "clear_2_rent (HERO FRAME at 21.70 s = frame 651)", "CHIP_2", "release — the sack bursts into a fountain of coins", "burst_coins",
  "debris + 12 coins fountain up and fall with gravity; padlock flies off", "sack re-enters hopping"),
 ("F9.3", 22.0, 3, "clear_3_left_without_paying_TAGGED_not_stopped", "CHIP_3", "control — he is not chasing; the tick TAGS the runner and the tag follows him", "tag_follow",
  "cyan ledger tag attaches above the tenant's head with a green tick pop; he keeps running and exits — tracked, never stopped", "tenant re-enters ahead, sprinting"),
 ("F9.4", 23.2, 4, "clear_4_reconciliation", "CHIP_4", "order — the wobbling tower becomes one neat card", "burst_dashboard",
  "12 sheets scatter, the tower flashes white and becomes the dashboard card that shrinks toward the checklist", "tower re-enters wobbling"),
 ("F9.5", 24.4, 5, "clear_5_complaints", "CHIP_5", "relief — every red ticket flips green with a pop", "flip_green",
  "bubbles turn green in a sweep with 5 small pop rings, then fade", "swarm re-enters diving"),
]
for (n, t0, k, beat, chip, feeling, payoff, payoff_note, entry) in CL:
    fr = {"n": n, "t0": t0, "t1": round(t0 + 1.2, 2), "beat": beat, "strings": [f"OBST_{k}", chip], "mandatory": ["M6", "M10"], "obstacle": k, "contact_t": round(t0 + 0.75, 2),
          "motion": {1: "lean_in", 2: "hop", 3: "sprint_ahead", 4: "topple_wobble", 5: "swoop"}[k], "payoff": payoff,
          "feeling": feeling,
          "framing": {"owner_frac_target": 0.15, "focus_t": round(t0 + 0.75, 2), "camera": [cam(t0, 1.0), cam(round(t0 + 0.75, 2), 1.15, 600, 0.15), cam(round(t0 + 1.05, 2), 1.0, 540, 0.15)],
                      "eye": "1st the obstacle entering (" + entry + "), 2nd the fire (running-fire pose, muzzle flash, tick + trail), 3rd the payoff and the chip popping onto the checklist",
                      "note": "the clearing run is about the WORLD changing, not his face — he stays at 0.16 with a 1.15 camera pulse on each hit"},
          "impact": [prim(t0, "obstacle_motion", motion={1: "lean_in", 2: "hop", 3: "sprint_ahead", 4: "topple_wobble", 5: "swoop"}[k]),
                     pose(t0, round(t0 + 0.25, 2), "run", "powered: aura + palette shift on the run poses; lean + bob"), pose(round(t0 + 0.25, 2), round(t0 + 0.5, 2), "runfire", "arm punched out mid-stride"),
                     prim(round(t0 + 0.3, 2), "muzzle_flash"), prim(round(t0 + 0.3, 2), "projectile", note="tick + 5-copy trail at 900 px/s"), pose(round(t0 + 0.5, 2), round(t0 + 1.2, 2), "run"),
                     hit(round(t0 + 0.75, 2), 2), prim(round(t0 + 0.75, 2), "impact_frame", target="obstacle", note="2 frames white"), prim(round(t0 + 0.75, 2), "ring", note="shockwave 20->260 px over 0.2 s"),
                     shake(round(t0 + 0.75, 2), 8, 0.2), prim(round(t0 + 0.75, 2), "payoff", kind=payoff, note=payoff_note), prim(round(t0 + 0.75, 2), "chip_flight", note="ease-out 0.35 s then a 3-frame landing pop"),
                     audio(round(t0 + 0.3, 2), "pew"), audio(round(t0 + 0.75, 2), {3: "tag", 2: "burst+coins", 5: "pops", 1: "burst+thump+whoosh", 4: "burst+papers"}[k]), audio(round(t0 + 1.1, 2), "ding")]}
    if n == "F9.2":
        fr["hero"] = True; fr["hero_t"] = 21.7; fr["hero_frame"] = 651
    frames.append(fr)

# ── F10 flag ─────────────────────────────────────────────────────────────────
frames.append({
 "n": "F10", "t0": 25.6, "t1": 27.6, "beat": "flag_level_clear", "strings": ["CLEAR"], "mandatory": ["M6"],
 "feeling": "triumph — he leaps for the pole, the flag runs up, confetti erupts, the checklist gives way to the flag",
 "framing": {"owner_frac_target": 0.19, "target_note": "cheer pose at x1.3", "focus_t": 26.9, "camera": [cam(25.6, 1.0), cam(26.55, 1.3, 600, 0.25), cam(27.6, 1.3, 600)],
             "eye": "1st the pole entering, 2nd his jump and cheer at the pole, 3rd the flag rising with LEVEL CLEAR! and the confetti"},
 "impact": [pose(25.6, 26.1, "run"), prim(26.1, "anticipation", pose="brace", frames=3), pose(26.2, 26.6, "jump", "arc 200 px, 280 px forward to the pole", arc_px=200, forward_px=280), prim(26.6, "flag_reached"),
            pose(26.6, 27.6, "cheer", "both arms up at the pole, small hop at 26.9", forward_px=280, hold=True, hop_t=26.9), prim(26.6, "particles", kind="confetti", n=40, note="fountain upward with gravity; second burst at 26.9"),
            prim(26.6, "grade", to="bright"), prim(26.6, "checklist_fade", note="26.6-27.0 (Lane A D-2)"), audio(26.2, "jump"), audio(26.6, "fanfare"), audio(26.6, "confetti")],
 "repair_of": "carried from Lane A D-2 (checklist fades so the raised flag is visible)"})

# ── F11 end card ─────────────────────────────────────────────────────────────
frames.append({
 "n": "F11", "t0": 27.6, "t1": 30.0, "beat": "end_card_brand_cta", "strings": ["CTA_1", "CTA_2", "URL"], "raster": ["WORDMARK"], "mandatory": ["M10"],
 "feeling": "calm, clear close — the game freezes into brand blue; the same ask, said plainly",
 "framing": {"owner_frac_target": 0.0, "focus_t": 29.0, "camera": [], "eye": "1st the wordmark, 2nd INSTALL / RENTOK APP, 3rd the URL; nothing moves for the last 1.0 s"},
 "impact": [prim(27.6, "freeze_dim", note="0.3 s dim to the card blue"), audio(27.6, "end")]})

board = {
 "schema": "BOARD-v2 (job-local): BOARD-v1 + feeling / framing / impact per beat",
 "job_id": "AGY-2026-09-21-RENTOK-GAME-V2-001", "supersedes_board": "source/lane-a/board.lane-a.json (AGY-2026-09-20-RENTOK-GAME-LANE-A-001 @ 7dab37a)",
 "fps": FPS, "canvas": [1080, 1920], "safe_box": [65, 288, 888, 1248],
 "ground_y": 1220, "owner_h": 300,
 "frames": frames,
 "brand_timeline": [{"t": 0.0, "what": "WORDMARK chip in HUD top-right, persistent to 27.6"}, {"t": 15.8, "what": "RENTOK APP typed in the cheat panel"},
                    {"t": 17.4, "what": "phone item with WORDMARK lands in the owner's hand; phone icon in the HUD from 18.0"}, {"t": 27.6, "what": "end card: WORDMARK large + CTA + URL"}],
 "install_event_t": 17.4, "flash_t": 17.6, "flag_reached_t": 26.6, "powered_from_t": 17.4, "hero_frame": 651, "hero_t": 21.7,
 "layout": {
  "hud_y": 300, "hud_scale": 6, "wordmark_chip": [738, 300, 888, 377], "checklist_x": 90, "checklist_y0": 400, "checklist_row_h": 54, "checklist_scale": 6,
  "label_y": 720, "label_scale": 7, "flash_y_default": 560, "flash_y_F10": 720, "flash_scale": 8, "cheat_scale": 10, "cta_scale": 10, "endcard_wordmark_w": 700, "endcard_centre_x": 476,
  "owner_x": 260, "scroll_problem_px_s": PROB_V, "scroll_clear_px_s": CLEAR_V,
  "obstacle_sizes": {"1": [373, 397], "2": [317, 317], "3": [230, 345], "4": [300, 390], "5": [423, 345]},
  "obstacle_size_rule": "resting top edge >= 790 (below the label backing 710-779) at ground 1220, including the wall's 6-deg lean (bbox +41 px) and the sack's 110-px hop; the tower stays at Lane A size and topples about its base CENTRE so its far corner never rises above 802",
  "camera_cy_rule": "cy(s) = 750 + 170/s for s > 1 (960 at s = 1): the world row y = 750 maps to screen y = 790 at every zoom, so the play band always sits BELOW the label zone and the HUD; the UI layer is drawn after the camera transform",
  "world_fills_frame": "the plate + code lane fill 1080x1920 at every zoom; only text/logo boxes are bound to the safe box (CQ-001 lesson)",
  "ground_y_note": "1180 -> 1220 (+40): room for 300-px sprites under the label zone; feet inside the safe box bottom (1248)",
  "checklist_fade_out": {"t0": 26.6, "t1": 27.0, "repair_of": "Lane A D-2"}
 },
 "principles_note": "hit-stop, screen shake, impact frames, particles, anticipation, follow-through, easing, staging are used as REASONING from named references (Thomas & Johnston 1981; Swink 2008; Jonasson & Purho 2012) — Canon holds nothing on animation principles (CQ-001 GAP); not recorded as Canon"
}
# checks
tot = sum(f["t1"] - f["t0"] for f in frames); assert abs(tot - 30.0) < 1e-6, tot
for a, b in zip(frames, frames[1:]): assert abs(a["t1"] - b["t0"]) < 1e-6, (a["n"], b["n"])
for f in frames:
    for k in ("feeling", "framing", "impact"): assert f.get(k) not in (None, "", []) or f["n"] == "F11", (f["n"], k)
json.dump(board, open(JOB / "board.json", "w"), indent=1, ensure_ascii=False)
print("board.json:", len(frames), "beats,", f"{tot:.1f} s; hero frame", board["hero_frame"])
