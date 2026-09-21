#!/usr/bin/env python3
"""render_v2.py — the full 30-s film "the Video-4 way" (Treatment C's method over every beat), rendered by code from
board.json (BOARD-v2: feeling / framing / impact per beat) + copy-deck.json.

PROVENANCE: imports Lane A's frozen render_game.py (tools/render_game.py, byte-identical to 7dab37a) for the design tokens,
the text primitive + layout log, the base sprites, ground, plate fitting, debris, dashboard card, red->green recolour and
the tick glyph. The Treatment C primitives (source/treatment-c/render_c.py @ 41d97c6: world/UI split, camera crop-and-scale,
hit-stop with catch-up, screen shake, easing, colour grade + vignette, aura pulse + palette shift, particles, impact star,
shockwave ring, muzzle flash, tick trail, phone glow, flash-from-source, obstacle motion curves, chip landing pop) are
re-implemented here so that they cover ALL FIFTEEN beats and are DRIVEN BY THE BOARD: camera keyframes, hit-stops, shakes,
the pose table and the audio cue list are read from board.json `framing.camera` / `impact[]`, not hard-coded.

Two token changes vs Lane A (recorded in board.json layout): ground_y 1180 -> 1220 and owner_h 260 -> 300 (framing target);
obstacle sizes from board.json layout.obstacle_sizes. Every string, scale, backing and UI position is Lane A's.

Modes: --poses placeholder   USD-0 animatic: poses that no accepted sheet carries are stand-ins built from accepted bitmaps
                              (magenta corner dot marks each stand-in)
       --poses sheet          the accepted C sheet (gen/assets/c_*.png) + this job's new sheet (gen/assets/v2_*.png)
Writes gen/<name>.mp4 (video only), gen/<name>-layout.jsonl (UI text/logo boxes + screen-space sprite boxes + camera per
frame), gen/<name>-events.json, and qa/<name>/{frames at 2 fps, CONTACT-SHEET.png, KEYFRAMES.png}.
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

HERE = Path(__file__).resolve().parent
JOB = HERE.parent
sys.path.insert(0, str(HERE))
import render_game as G  # noqa: E402  (frozen Lane A module)
import pixfont as PF  # noqa: E402

BOARD = json.load(open(JOB / "board.json"))
DECK = json.load(open(JOB / "copy-deck.json"))["strings"]
LAY = BOARD["layout"]
# token changes for v2 (the board is the source; render_game's functions read G.T at call time)
G.T = dataclasses.replace(G.T, ground_y=BOARD["ground_y"], owner_h=BOARD["owner_h"])
T = G.T; W, H = G.W, G.H; FPS = G.FPS
hx, rgb = G.hx, G.rgb
INSTALL_T = BOARD["install_event_t"]; FLASH_T = BOARD["flash_t"]; FLAG_T = BOARD["flag_reached_t"]
CATCHUP_RATE = 1.25
POLE_TOP = 792   # world y: the raised flag stops below the LEVEL CLEAR! backing (710-779) at every zoom (camera_cy_rule)
OBST_SIZES = {int(k): tuple(v) for k, v in LAY["obstacle_sizes"].items()}
FRAMES = BOARD["frames"]
BEAT_BY_N = {f["n"]: f for f in FRAMES}


def beat_at(t):
    for f in FRAMES:
        if f["t0"] <= t < f["t1"]:
            return f
    return FRAMES[-1]


# ── the board's direction, indexed ───────────────────────────────────────────
def _collect(prim):
    out = []
    for f in FRAMES:
        for e in f["impact"]:
            if e["primitive"] == prim:
                out.append(e)
    return out


HOLDS = sorted([(e["t"], e["frames"] / FPS) for e in _collect("hit_stop")])
SHAKES = sorted([(e["t"], e["amp_px"], e["decay_s"]) for e in _collect("shake")])
POSES = sorted([e for e in _collect("pose")], key=lambda e: e["t0"])
CAMS = sorted([k for f in FRAMES for k in f["framing"]["camera"]], key=lambda k: k["t"])
ANTIC = sorted([e for e in _collect("anticipation")], key=lambda e: e["t"])
RUN_BEATS = {"F1", "F2", "F3", "F4", "F5", "F6", "F9.1", "F9.2", "F9.3", "F9.4", "F9.5", "F10"}


def ease_out(k):   return 1 - (1 - min(1.0, max(0.0, k))) ** 3
def ease_in(k):    return min(1.0, max(0.0, k)) ** 3
def ease_in_out(k):
    k = min(1.0, max(0.0, k)); return 3 * k * k - 2 * k * k * k


def world_time(t: float) -> float:
    """Hit-stop: the world freezes for d at each hold, then runs at CATCHUP_RATE until caught up (4d later)."""
    wt = t
    for h0, d in HOLDS:
        if t < h0:
            continue
        if t < h0 + d:
            wt -= (t - h0)
        elif t < h0 + d + 4 * d:
            wt -= d - (t - h0 - d) * (CATCHUP_RATE - 1)
    return wt


def shake_offset(t: float):
    dx = dy = 0.0
    for s0, amp, dec in SHAKES:
        if s0 <= t < s0 + dec:
            k = 1 - (t - s0) / dec
            dx += amp * k * math.sin((t - s0) * 95); dy += amp * k * 0.6 * math.cos((t - s0) * 70)
    return dx, dy


SCROLL_PAUSES = [(11.7, 12.35), (14.1, 18.0)]   # buried under the tower; down after the swarm through the cheat panel (Lane A paused 15.0-18.0)


def scroll_dist(t: float) -> float:
    """World scroll distance in px at time t: 400 px/s before 18.0, 480 px/s after, 0 inside SCROLL_PAUSES and after the flag (26.6)."""
    d = 0.0; step = 0.01; x = 0.0
    # closed form piecewise: integrate in segments
    segs = []
    marks = sorted({0.0, 18.0, 26.6, t} | {a for a, b in SCROLL_PAUSES} | {b for a, b in SCROLL_PAUSES})
    for a, b in zip(marks, marks[1:]):
        if a >= t:
            break
        b = min(b, t)
        paused = any(pa <= a < pb for pa, pb in SCROLL_PAUSES)
        if paused or a >= 26.6:
            continue
        v = T.scroll_problem if a < 18.0 else T.scroll_clear
        d += v * (b - a)
    return d


def cam_cy(s: float) -> float:
    """board layout.camera_cy_rule: the world row y=750 maps to screen 790 at every zoom (play band under the label zone)."""
    return 960.0 if s <= 1.0001 else 750 + 170 / s


def camera(t: float):
    """(scale, cx, cy) from the board's camera keyframes: each keyframe eases from the previous VALUE over ease_s."""
    s, cx = 1.0, W / 2
    prev_s, prev_cx = 1.0, W / 2
    for k in CAMS:
        if t < k["t"]:
            break
        prev_s, prev_cx = s, cx
        kk = ease_out((t - k["t"]) / k["ease_s"]) if k["ease_s"] > 0 else 1.0
        s = prev_s + (k["scale"] - prev_s) * kk; cx = prev_cx + (k["cx"] - prev_cx) * kk
        # for the next keyframe, the "previous value" is this keyframe's target once it has completed
        if t >= k["t"] + k["ease_s"]:
            s, cx = k["scale"], k["cx"]
    return s, cx, cam_cy(s)


def apply_camera(world, scale, cx, cy, dx, dy):
    if scale <= 1.001 and abs(dx) < 0.5 and abs(dy) < 0.5:
        return world, (0.0, 0.0, 1.0)
    cw, ch = W / scale, H / scale
    x0 = min(max(0.0, cx - cw / 2 + dx), W - cw); y0 = min(max(0.0, cy - ch / 2 + dy), H - ch)
    crop = world.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch)))
    return crop.resize((W, H), Image.NEAREST), (x0, y0, scale)


def to_screen(box, view):
    x0, y0, s = view
    return [int((box[0] - x0) * s), int((box[1] - y0) * s), int((box[2] - x0) * s), int((box[3] - y0) * s)]


# ── colour grade ─────────────────────────────────────────────────────────────
_VIG = None


def vignette_mask():
    global _VIG
    if _VIG is None:
        yy, xx = np.mgrid[0:H, 0:W]
        r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / math.sqrt(2)
        _VIG = np.clip(r, 0, 1) ** 1.6
    return _VIG


def grade(world, mul, vig, lift=0.0, cyan=0.0):
    a = np.asarray(world.convert("RGB")).astype(np.float32) / 255.0
    a = a * np.array(mul, dtype=np.float32)
    if vig > 0:
        a *= (1 - vignette_mask() * vig)[:, :, None]
    if lift > 0:
        a = a + lift * (1 - a) * 0.6
    if cyan > 0:
        lum = a.mean(axis=2, keepdims=True)
        a = a + cyan * np.clip(lum - 0.55, 0, 1) * np.array([0.0, 0.35, 0.45], dtype=np.float32)
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).convert("RGBA")


def grade_for(t):
    """(mul, vig, lift, cyan): cold from the swarm hit to the flash (board F6 grade 'cold', 0.9 s ease), bright after the flash
    through the flag (F7/F10 grade 'bright'); none before 14.1."""
    if t < 14.1:
        return (1, 1, 1), 0.0, 0.0, 0.0
    if t < 15.0:
        k = ease_in_out((t - 14.1) / 0.9)
        return (1 - 0.45 * k, 1 - 0.40 * k, 1 - 0.25 * k), 0.35 * k, 0.0, 0.0
    if t < 17.2:
        return (0.55, 0.60, 0.75), 0.35, 0.0, 0.0
    if t < FLASH_T:
        k = (t - 17.2) / 0.4
        return (0.55 + 0.45 * k, 0.60 + 0.40 * k, 0.75 + 0.25 * k), 0.35 * (1 - k), 0.0, 0.0
    if t < 27.6:
        return (1.0, 1.0, 1.0), 0.0, 0.10, 0.18
    return (1, 1, 1), 0.0, 0.0, 0.0


# ── sprites ──────────────────────────────────────────────────────────────────
C_POSES = ["hurt", "cornered", "cornered_up", "catch", "powered", "windup", "fire", "brace"]
V2_POSES = ["lookback", "reach", "trip", "cover", "runfire", "cheer", "dazed", "land"]


class V2Sprites(G.Sprites):
    def __init__(self, assets: Path, poses: str):
        super().__init__("final", assets); self.poses_mode = poses
        self.v2_scale = None
        cj = assets / "v2_cutout.json"
        if cj.exists():
            j = json.load(open(cj)); self.v2_scale = T.owner_h / float(j.get("standing_cell_h", 344))

    def obst(self, n: int):
        return self._load(f"obst_{n}", *OBST_SIZES[n])

    def cpose(self, name: str):
        k = ("pose", name, self.poses_mode)
        if k in self._c:
            return self._c[k]
        h = T.owner_h
        if name in C_POSES and self.poses_mode == "sheet" and (self.assets / f"c_{name}.png").exists():
            im = Image.open(self.assets / f"c_{name}.png").convert("RGBA")
            f = h / 344.0   # C sheet: the standing 'brace' cell is 344 px (c_cutout.json); one common scale for all eight cells
            im = im.resize((max(1, int(im.width * f)), max(1, int(im.height * f))), Image.NEAREST)
        elif name in V2_POSES and self.poses_mode == "sheet" and (self.assets / f"v2_{name}.png").exists() and self.v2_scale:
            im = Image.open(self.assets / f"v2_{name}.png").convert("RGBA")
            im = im.resize((max(1, int(im.width * self.v2_scale)), max(1, int(im.height * self.v2_scale))), Image.NEAREST)
        else:
            im = self._standin(name)
        self._c[k] = im
        return im

    def _standin(self, name: str):
        """USD-0 stand-ins from ACCEPTED bitmaps (base four + C eight when present); magenta dot = stand-in."""
        h = T.owner_h
        base = {"hurt": "jump", "cornered": "idle", "cornered_up": "idle", "catch": "jump", "powered": "idle", "windup": "runB", "fire": "runA", "brace": "idle",
                "lookback": "idle", "reach": "runA", "trip": "runA", "cover": "idle", "runfire": "runB", "cheer": "jump", "dazed": "idle", "land": "idle"}[name]
        # prefer an accepted C cell as the stand-in where it is closer to the pose
        cbase = {"reach": "catch", "runfire": "fire", "cover": "cornered", "dazed": "brace", "cheer": "catch"}.get(name)
        cbase_used = bool(cbase and (self.assets / f"c_{cbase}.png").exists() and self.poses_mode == "sheet")
        if cbase_used:
            im = self.cpose(cbase).copy()
        else:
            im = self._load(f"owner_{base}", int(h * 0.75), h).copy()
        if name == "hurt":
            im = im.rotate(-18, Image.NEAREST, expand=True)
        elif name in ("cornered", "cornered_up") or (name == "cover" and not cbase_used):
            im = im.resize((im.width, int(im.height * 0.72)), Image.NEAREST)
        elif name == "windup":
            im = im.rotate(6, Image.NEAREST, expand=True)
        elif name in ("fire", "runfire"):
            im = im.rotate(-6, Image.NEAREST, expand=True)
        elif name == "trip":
            im = im.rotate(-80, Image.NEAREST, expand=True)
        elif name == "land":
            im = im.resize((int(im.width * 1.06), int(im.height * 0.92)), Image.NEAREST)
        elif name == "dazed":
            im = im.rotate(5, Image.NEAREST, expand=True)
        elif name == "lookback":
            im = ImageOps.mirror(im)
        ImageDraw.Draw(im).rectangle((0, 0, 10, 10), fill=(255, 0, 255, 255))
        return im

    def powered_sprite(self, im, t):
        """Pulsing aura (alpha 60<->140 at 3 Hz) + shirt palette shift (blue toward cyan). Cached per (image id, alpha bucket)."""
        alpha = int(100 + 40 * math.sin(t * 2 * math.pi * 3)); bucket = alpha // 12
        k = ("pow", id(im), bucket)
        if k in self._c:
            return self._c[k]
        a = np.asarray(im).astype(np.int16)
        blue = (a[:, :, 2] > 150) & (a[:, :, 0] < 120) & (a[:, :, 3] > 0)
        out = a.copy(); out[blue, 0] = np.minimum(255, a[blue, 0] + 10); out[blue, 1] = np.minimum(255, a[blue, 1] + 70); out[blue, 2] = 255
        sp = Image.fromarray(out.astype(np.uint8))
        mask = sp.split()[3]
        halo = Image.new("RGBA", (sp.width + 24, sp.height + 24), (0, 0, 0, 0))
        for dx in range(-6, 7, 3):
            for dy in range(-6, 7, 3):
                layer = Image.new("RGBA", halo.size, (0, 0, 0, 0)); layer.paste(hx(T.cyan, bucket * 12), (12 + dx, 12 + dy), mask)
                halo = Image.alpha_composite(halo, layer)
        halo.alpha_composite(sp, (12, 12))
        self._c[k] = halo
        return halo


def run_pose(t):
    return "runA" if int(t * 8) % 2 == 0 else "runB"


def pose_at(t):
    """(pose name, entry) from the board's pose table; anticipation entries override for their frames; default run/idle."""
    for a in ANTIC:
        n = a.get("frames", 3)
        if a["t"] <= t < a["t"] + n / FPS:
            return a["pose"], {"pose": a["pose"]}
    for e in POSES:
        if e["t0"] <= t < e["t1"]:
            name = e["pose"]
            return (run_pose(t) if name == "run" else name), e
    n = beat_at(t)["n"]
    return (run_pose(t) if n in RUN_BEATS else "idle"), {"pose": "run" if n in RUN_BEATS else "idle"}


def health_at(t):
    contacts = [f["contact_t"] for f in FRAMES if "contact_t" in f and f["n"].startswith("F") and not f["n"].startswith("F9")]
    if t >= FLASH_T:
        return min(5, int((t - FLASH_T) / 0.08) + 1) if t < 18.0 else 5
    return 5 - sum(1 for c in contacts if t >= c)


# ── particles and effect primitives ──────────────────────────────────────────
class Particles:
    def __init__(self):
        self.ps = []; self.rng = np.random.default_rng(3)

    def emit(self, n, x, y, spread, vy0, life, color, size=8, kind="dot", gravity=900, up_only=True):
        for _ in range(n):
            ang = self.rng.uniform(-math.pi, 0) if (up_only and kind != "spark") else self.rng.uniform(0, 2 * math.pi)
            sp = self.rng.uniform(*spread)
            self.ps.append({"x": x, "y": y, "vx": math.cos(ang) * sp, "vy": math.sin(ang) * sp + vy0, "life": life, "age": 0.0,
                            "c": color, "s": size, "kind": kind, "rot": self.rng.uniform(0, 360), "g": gravity})

    def step(self, dt):
        for p in self.ps:
            p["age"] += dt; p["x"] += p["vx"] * dt; p["y"] += p["vy"] * dt; p["vy"] += p["g"] * dt
            if p["kind"] == "sheet":
                p["vx"] *= 0.97; p["vy"] = min(p["vy"], 260); p["rot"] += 240 * dt
            if p["kind"] == "confetti":
                p["vx"] *= 0.985; p["vy"] = min(p["vy"], 320); p["rot"] += 400 * dt
        self.ps = [p for p in self.ps if p["age"] < p["life"]]

    def draw(self, cv):
        d = ImageDraw.Draw(cv)
        for p in self.ps:
            k = 1 - p["age"] / p["life"]; a = int(255 * min(1.0, k * 1.5))
            if p["kind"] == "sheet":
                sh = Image.new("RGBA", (int(p["s"] * 1.4), p["s"]), (250, 250, 245, a)); ImageDraw.Draw(sh).rectangle((0, 0, sh.width - 1, sh.height - 1), outline=(30, 30, 40, a), width=2)
                sh = sh.rotate(p["rot"], Image.NEAREST, expand=True); cv.alpha_composite(sh, (int(p["x"]), int(p["y"])))
            elif p["kind"] == "confetti":
                sh = Image.new("RGBA", (p["s"], int(p["s"] * 0.6)), (*p["c"], a)); sh = sh.rotate(p["rot"], Image.NEAREST, expand=True)
                cv.alpha_composite(sh, (int(p["x"]), int(p["y"])))
            elif p["kind"] == "coin":
                s = p["s"]; d.ellipse((int(p["x"]), int(p["y"]), int(p["x"]) + s, int(p["y"]) + s), fill=(255, 220, 60, a), outline=(60, 40, 10, a), width=2)
            else:
                s = max(2, int(p["s"] * (0.5 + 0.5 * k)))
                d.rectangle((int(p["x"]), int(p["y"]), int(p["x"]) + s, int(p["y"]) + s), fill=(*p["c"], a))


def impact_star(cv, x, y, r=52, color=(255, 241, 0, 255)):
    d = ImageDraw.Draw(cv); pts = []
    for i in range(12):
        rr = r if i % 2 == 0 else r * 0.42; ang = i * math.pi / 6
        pts.append((x + rr * math.cos(ang), y + rr * math.sin(ang)))
    d.polygon(pts, fill=color); d.polygon(pts, outline=hx(T.ink), width=3)


def ring(cv, x, y, r, width, alpha, color=(255, 255, 255)):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ov).ellipse((x - r, y - r, x + r, y + r), outline=(*color, alpha), width=width)
    cv.alpha_composite(ov)


def muzzle_flash(cv, x, y, k):
    r = int(26 * (1 - k) + 8); d = ImageDraw.Draw(cv)
    d.polygon([(x, y - r), (x + r * 0.35, y - r * 0.35), (x + r, y), (x + r * 0.35, y + r * 0.35), (x, y + r), (x - r * 0.35, y + r * 0.35), (x - r, y), (x - r * 0.35, y - r * 0.35)], fill=(255, 255, 255, 230))
    d.ellipse((x - r * 0.4, y - r * 0.4, x + r * 0.4, y + r * 0.4), fill=hx(T.cyan))


TICK_SCALE = 6   # Lane A D-3 used 4 (28 px); 6 = 42 px so the projectile reads at phone size


def tick_with_trail(cv, x, y):
    for i in range(1, 6):
        g = PF.render("✓", TICK_SCALE, fg=rgb(T.cyan)); a = g.split()[3].point(lambda p, i=i: int(p * (0.55 - i * 0.1)))
        g.putalpha(a); cv.alpha_composite(g, (int(x - i * 20), y))
    G.draw_tick(cv, int(x), y, TICK_SCALE)


def phone_item(cv, x, y, w, h, glow, S):
    if glow > 0:
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ov).ellipse((x - 40, y - 40, x + w + 40, y + h + 40), fill=hx(T.cyan, int(120 * glow)))
        cv.alpha_composite(ov.filter(ImageFilter.GaussianBlur(18)))
    d = ImageDraw.Draw(cv)
    d.rectangle((x, y, x + w, y + h), fill=hx(T.brand_blue), outline=hx(T.ink), width=4)
    d.rectangle((x + 6, y + 8, x + w - 6, y + h - 8), fill=hx(T.cyan) if glow > 0 else (12, 20, 60, 255))
    if glow > 0.5:
        sm = S.wordmark.resize((w - 16, int((w - 16) * S.wordmark.height / S.wordmark.width)), Image.LANCZOS); cv.alpha_composite(sm, (x + 8, y + h // 2 - sm.height // 2))


def silhouette(cv, sp, xy, alpha=0.85):
    white = Image.new("RGBA", sp.size, (255, 255, 255, 0)); white.putalpha(sp.split()[3].point(lambda p: int(p * alpha))); cv.alpha_composite(white, xy)


def rotate_about(im, angle_deg, pivot_rel):
    """Rotate `im` (expand) and return (rotated, offset) such that pasting at (px - off_x, py - off_y) keeps the pivot
    (given relative to the image's top-left) at world (px, py). Pillow's positive angle = counter-clockwise on screen."""
    rot = im.rotate(angle_deg, Image.NEAREST, expand=True)
    th = math.radians(angle_deg)
    dx, dy = pivot_rel[0] - im.width / 2, pivot_rel[1] - im.height / 2
    ddx = dx * math.cos(th) + dy * math.sin(th); ddy = -dx * math.sin(th) + dy * math.cos(th)
    return rot, (rot.width / 2 + ddx, rot.height / 2 + ddy)


def speed_lines(cv, x, y, n=3, length=90):
    d = ImageDraw.Draw(cv)
    for i in range(n):
        yy = y + i * 26
        d.line((x - length, yy, x, yy), fill=(255, 255, 255, 170), width=4)


def dazed_stars(cv, cx, cy, t):
    d = ImageDraw.Draw(cv)
    for i in range(3):
        ang = t * 7 + i * 2 * math.pi / 3; sx = cx + 46 * math.cos(ang); sy = cy + 12 * math.sin(ang)
        pts = [(sx + 9 * math.cos(a), sy + 9 * math.sin(a)) if j % 2 == 0 else (sx + 4 * math.cos(a), sy + 4 * math.sin(a)) for j, a in enumerate(np.linspace(0, 2 * math.pi, 11)[:-1])]
        d.polygon(pts, fill=hx(T.yellow), outline=hx(T.ink))


# ── the world (one frame) ────────────────────────────────────────────────────
class State:
    def __init__(self):
        self.P = Particles(); self.fired = {}; self.ev = []; self.last_hop = {}; self.last_sheet = 0.0; self.last_coin = 0.0
        self.hand_world = None; self.view = None


def obstacle_pose(f, k, wt, t, S, st, cv, boxes, draw_after):
    """Draw obstacle k for beat f at world time wt. Returns (drawn_after_owner_callable or None)."""
    n = f["n"]; t0 = f["t0"]; tl = wt - t0; clearing = n.startswith("F9"); ct = f["contact_t"]
    v = T.scroll_clear if clearing else T.scroll_problem
    im = S.obst(k); w, h = im.size; g = T.ground_y
    motion = f["motion"]; d = ImageDraw.Draw(cv)
    hit = wt >= ct
    ox_scroll = 1080 - (scroll_dist(wt) - scroll_dist(t0))   # the obstacle rides the world scroll (pauses included)
    if motion not in ("sprint_past", "sprint_ahead") and (ox_scroll + w * 1.4 < 0 or ox_scroll > 1080):
        return None

    if motion == "lean_in":
        lean = 6.0 * (ease_in_out((tl - 0.8) / 0.7) if not clearing else 1.0)
        ox = ox_scroll
        rot, off = rotate_about(im, lean, (0, h)) if lean > 0.05 else (im, (0, h))
        px, py = int(ox - off[0]), int(g - off[1])
        if not clearing and 0.8 <= tl < ct - t0 and t - st.last_sheet > 0.16:
            st.last_sheet = t; st.P.emit(1, ox + w * 0.5, g - h + 10, (40, 120), -60, 0.7, (250, 250, 245), size=26, kind="sheet", gravity=400)
        if clearing and hit:
            kk = min(1.0, (wt - ct) / 0.35)
            G.debris(cv, im, int(ox), int(g - h), kk, seed=1)
            if wt < ct + 2 / FPS:
                silhouette(cv, rot, (px, py), 0.9)
            if not st.fired.get(("payoff", n)):
                st.fired[("payoff", n)] = True
                st.P.emit(14, ox + w / 2, g - h * 0.66, (150, 420), -300, 0.9, (250, 250, 245), size=34, kind="sheet", gravity=500)
                st.P.emit(10, ox + 40, g - 10, (80, 260), -120, 0.5, (200, 190, 160), size=10, gravity=700)
                st.ev.append({"t": round(t, 3), "event": "burst", "obstacle": k})
            boxes.append({"id": f"OBST_{k}", "box": [int(ox), int(g - h), int(ox + w), g], "state": "burst"})
        else:
            cv.alpha_composite(rot, (px, py)); boxes.append({"id": f"OBST_{k}", "box": [px, py, px + rot.width, py + rot.height], "state": "alive"})
            if clearing and ct <= wt < ct + 2 / FPS:
                silhouette(cv, rot, (px, py), 0.9)
        return None

    if motion == "hop":
        ox = ox_scroll
        period = 0.45; ph = (tl / period) % 1.0; hop = 110 * math.sin(math.pi * ph)
        cyc = int(tl / period)
        squash = ph < 0.08 and tl > 0.05
        sp = im.resize((int(w * 1.06), int(h * 0.94)), Image.NEAREST) if squash else im
        oy = g - sp.height - int(hop)
        if st.last_hop.get(n) != cyc and tl > 0.05:
            st.last_hop[n] = cyc
            if not (clearing and hit):
                st.P.emit(5, ox + w / 2, g - 6, (40, 160), -100, 0.4, (168, 146, 106), size=10, gravity=700)
        if clearing and hit:
            kk = min(1.0, (wt - ct) / 0.35)
            G.debris(cv, im, int(ox), int(g - h), kk, seed=2)
            if wt < ct + 2 / FPS:
                silhouette(cv, im, (int(ox), int(g - h)), 0.9)
            if not st.fired.get(("payoff", n)):
                st.fired[("payoff", n)] = True
                st.P.emit(14, ox + w / 2, g - h * 0.5, (160, 420), -420, 1.0, (255, 220, 60), size=16, kind="coin", gravity=900)
                st.P.emit(8, ox + 40, g - 10, (80, 260), -120, 0.5, (200, 190, 160), size=10, gravity=700)
                st.ev.append({"t": round(t, 3), "event": "burst", "obstacle": k})
            boxes.append({"id": f"OBST_{k}", "box": [int(ox), int(g - h), int(ox + w), g], "state": "burst"})
        else:
            cv.alpha_composite(sp, (int(ox), oy)); boxes.append({"id": f"OBST_{k}", "box": [int(ox), oy, int(ox + sp.width), oy + sp.height], "state": "alive"})
            if clearing and ct <= wt < ct + 2 / FPS:
                silhouette(cv, sp, (int(ox), oy), 0.9)
        return None

    if motion in ("sprint_past", "sprint_ahead"):
        if motion == "sprint_past":
            ox = -230 + (tl - 0.35) * (v * 1.9)   # appears at t0+0.35; passes the owner exactly at contact_t (t0+1.2)
        else:
            ox = 560 + tl * 250 + 600 * max(0.0, tl - (ct - t0))
        bob = int(8 * abs(math.sin(tl * 2 * math.pi * 6)))
        oy = g - h - bob
        cv.alpha_composite(im, (int(ox), oy)); boxes.append({"id": f"OBST_{k}", "box": [int(ox), oy, int(ox + w), oy + h], "state": "alive"})
        speed_lines(cv, int(ox) - 6, oy + int(h * 0.3))
        if t - st.last_coin > 0.1 and (0.2 < tl < 2.4):
            st.last_coin = t; st.P.emit(1, ox + w * 0.8, oy + h * 0.35, (30, 90), -80, 0.6, (255, 220, 60), size=12, kind="coin", gravity=900)
        if clearing and hit:
            tx, ty = int(ox) + w // 2 - 22, oy - 64
            d.rectangle((tx, ty, tx + 44, ty + 44), fill=hx(T.cyan), outline=hx(T.ink), width=3)
            for j in range(3):
                d.line((tx + 10, ty + 12 + j * 10, tx + 34, ty + 12 + j * 10), fill=hx(T.ink), width=3)
            rk = (wt - ct) / 0.25
            if rk < 1:
                ring(cv, tx + 22, ty + 22, int(10 + 120 * ease_out(rk)), max(2, int(8 * (1 - rk))), int(255 * (1 - rk)), rgb(T.green))
                cv.alpha_composite(PF.render("✓", 5, fg=rgb(T.green)), (tx + 50, ty - 20))
            if not st.fired.get(("payoff", n)):
                st.fired[("payoff", n)] = True; st.ev.append({"t": round(t, 3), "event": "tag", "obstacle": k})
        return None

    if motion in ("topple", "topple_wobble"):
        ox = ox_scroll
        wob = 3.0 * math.sin(2 * math.pi * 2 * tl) * min(1.0, tl / 0.8)
        ang = wob
        fall_start = (ct - t0) - 0.35
        if motion == "topple" and tl >= fall_start:
            ang = 85.0 * ease_in((tl - fall_start) / 0.35)
        if clearing and hit:
            kk = min(1.0, (wt - ct) / 0.35)
            if not st.fired.get(("payoff", n)):
                st.fired[("payoff", n)] = True
                st.P.emit(12, ox + w / 2, g - h * 0.7, (150, 400), -300, 0.9, (250, 250, 245), size=30, kind="sheet", gravity=500)
                st.ev.append({"t": round(t, 3), "event": "burst", "obstacle": k})
            card = G.neat_dashboard(220, 260)
            sc = max(0.25, 1 - kk * 0.75); cw, ch = int(220 * sc), int(260 * sc)
            cx0 = int(ox + w / 2 - cw / 2 + (T.checklist_x - ox) * kk * 0.5); cy0 = int(g - ch - (g - 700) * kk * 0.6)
            cv.alpha_composite(card.resize((cw, ch), Image.NEAREST), (cx0, cy0))
            if wt < ct + 2 / FPS:
                silhouette(cv, im, (int(ox), g - h), 0.9)
            boxes.append({"id": f"OBST_{k}", "box": [cx0, cy0, cx0 + cw, cy0 + ch], "state": "burst"})
            return None
        rot, off = rotate_about(im, ang, (w / 2, h))   # pivot = base centre: the far corner rises at most sqrt((w/2)^2+h^2)-h = 28 px
        px, py = int(ox + w / 2 - off[0]), int(g - off[1])
        if motion == "topple" and hit and t < SCROLL_PAUSES[0][1]:
            # fallen: drawn AFTER the owner (half-buried) while the scroll is paused — returned as a deferred draw
            def later(cv2):
                cv2.alpha_composite(rot, (px, py))
                if ct <= t < ct + 2 / FPS:
                    silhouette(cv2, rot, (px, py), 0.9)
            boxes.append({"id": f"OBST_{k}", "box": [px, py, px + rot.width, py + rot.height], "state": "fallen"})
            return later
        cv.alpha_composite(rot, (px, py)); boxes.append({"id": f"OBST_{k}", "box": [px, py, px + rot.width, py + rot.height], "state": "alive"})
        return None

    if motion == "swoop":
        base_y = g - h
        if clearing:
            ox = ox_scroll; k0 = max(0.0, min(1.0, tl / (ct - t0)))
            oy = base_y - 120 * (1 - k0) ** 1.5
            if hit:
                kk = min(1.0, (wt - ct) / 0.4)
                green = G.recolour_red_to_green(im, min(1.0, kk * 2))
                if kk > 0.5:
                    al = green.split()[3].point(lambda p: int(p * (1 - (kk - 0.5) * 2))); green.putalpha(al)
                cv.alpha_composite(green, (int(ox), int(oy)))
                rng = np.random.default_rng(5)
                for j in range(5):
                    tj = ct + j * 0.05
                    if tj <= wt < tj + 0.2:
                        rk = (wt - tj) / 0.2; px_ = ox + rng.uniform(0.15, 0.85) * w; py_ = oy + rng.uniform(0.2, 0.8) * h
                        ring(cv, px_, py_, int(8 + 60 * ease_out(rk)), 4, int(255 * (1 - rk)), rgb(T.green))
                    else:
                        rng.uniform(0.15, 0.85); rng.uniform(0.2, 0.8)
                if not st.fired.get(("payoff", n)):
                    st.fired[("payoff", n)] = True; st.ev.append({"t": round(t, 3), "event": "burst", "obstacle": k})
                boxes.append({"id": f"OBST_{k}", "box": [int(ox), int(oy), int(ox + w), int(oy + h)], "state": "burst"})
            else:
                cv.alpha_composite(im, (int(ox), int(oy))); boxes.append({"id": f"OBST_{k}", "box": [int(ox), int(oy), int(ox + w), int(oy + h)], "state": "alive"})
            return None
        # problem half (F6 + drift-off in F7)
        base_x = ox_scroll
        if wt < 13.9:
            ox = base_x; oy = base_y + 10 * math.sin(wt * 9)
        elif wt < ct:
            ox = base_x - 300 * (wt - 13.9); oy = base_y + 10 * math.sin(wt * 9) + 30 * (wt - 13.9) / 0.2
        elif wt < 15.0:
            kx = ease_out((wt - ct) / 0.4); ox = base_x - 60 + 30 * kx; oy = base_y - 20 * kx + 10 * math.sin(wt * 9)
        else:
            kx = ease_in((wt - 15.0) / 0.6); ox = base_x - 30 + 80 * kx; oy = base_y - 40 - 900 * kx
        if wt < 15.0:
            cv.alpha_composite(im, (int(ox), int(oy))); boxes.append({"id": f"OBST_{k}", "box": [int(ox), int(oy), int(ox + w), int(oy + h)], "state": "alive"})
        elif wt < 15.45:   # drift-off: fades out as it rises so it is gone before it reaches the HUD row (state 'leaving')
            fade = max(0.0, 1 - (wt - 15.0) / 0.45); ghost = im.copy(); ghost.putalpha(ghost.split()[3].point(lambda p: int(p * fade)))
            cv.alpha_composite(ghost, (int(ox), int(oy))); boxes.append({"id": f"OBST_{k}", "box": [int(ox), int(oy), int(ox + w), int(oy + h)], "state": "leaving"})
        return None
    return None


def draw_world(t, wt, S, plate_img, st, boxes):
    cv = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    camx = scroll_dist(wt)
    bg = plate_img if plate_img is not None else G.code_plate()
    px = int(camx * 0.25) % bg.width
    strip = Image.new("RGB", (W, H)); strip.paste(bg.crop((px, 0, min(px + W, bg.width), H)), (0, 0))
    if px + W > bg.width:
        strip.paste(bg.crop((0, 0, px + W - bg.width, H)), (bg.width - px, 0))
    cv.paste(strip, (0, 0)); G.draw_ground(cv, camx)
    d = ImageDraw.Draw(cv)
    f = beat_at(wt); n = f["n"]; tl = t - f["t0"]
    deferred = None

    # obstacles (the swarm persists into F7 for its drift-off)
    order = ["F2", "F3", "F4", "F5", "F6"]
    todo = []
    if n in order and order.index(n) > 0:
        todo.append(BEAT_BY_N[order[order.index(n) - 1]])      # the previous obstacle is still leaving the screen
    if "obstacle" in f:
        todo.append(f)
    if n == "F7" and wt < 15.7:
        todo.append(BEAT_BY_N["F6"])
    for fo in todo:
        dfr = obstacle_pose(fo, fo["obstacle"], wt, t, S, st, cv, boxes, None)
        deferred = dfr or deferred
        if "contact_t" in fo and not n.startswith("F9"):
            ct = fo["contact_t"]
            if ct <= t < ct + 2 / FPS and not st.fired.get(("hit", fo["n"])):
                st.fired[("hit", fo["n"])] = True; st.ev.append({"t": round(t, 3), "event": "hit", "obstacle": fo["obstacle"]})

    # flag pole (F10) before the owner
    polex = None
    if n == "F10":
        polex = int(1080 - tl * T.scroll_clear) if tl < 1.0 else 600
        d.rectangle((polex, POLE_TOP, polex + 14, T.ground_y), fill=(120, 120, 130, 255), outline=hx(T.ink), width=2)

    # owner
    name, e = pose_at(t)
    is_c = name in C_POSES or name in V2_POSES
    sp = S.cpose(name) if is_c else S.owner(name, False)
    powered = t >= INSTALL_T
    if name.startswith("run"):
        sp = sp.rotate(-8, Image.NEAREST, expand=True)
    bob = -int(3 * abs(math.sin(t * 2 * math.pi * 4))) if name.startswith("run") else 0
    knock = 0
    if "knock_px" in e:
        if e.get("hold"):
            knock = e["knock_px"]
        else:
            knock = int(e["knock_px"] * (1 - ease_out((t - e["t0"]) / e.get("knock_s", 0.4))))
    if e.get("pose") in ("cornered", "cornered_up", "catch") and 9.6 <= t and e.get("hold") and "knock_px" not in e:
        knock = 0
    if is_c and "knock_px" not in e and 14.5 <= t < FLASH_T:
        knock = 20
    jump = 0.0; forward = 0
    if "arc_px" in e:
        kj = (t - e["t0"]) / (e["t1"] - e["t0"]); jump = math.sin(math.pi * min(1.0, kj)) * e["arc_px"]
        if "forward_px" in e:
            forward = int(e["forward_px"] * min(1.0, kj))
    elif "forward_px" in e:
        forward = e["forward_px"]
        if "hop_t" in e and e["hop_t"] <= t < e["hop_t"] + 0.3:
            jump = math.sin(math.pi * (t - e["hop_t"]) / 0.3) * 60
    if "fall_from_px" in e:
        jump = e["fall_from_px"] * (1 - ease_in((t - e["t0"]) / e["fall_s"]))
    ox_owner = T.owner_x - knock + forward
    oy_owner = T.ground_y - sp.height + bob - int(jump)
    if powered:
        sp = S.powered_sprite(sp, t); ox_owner -= 12; oy_owner = T.ground_y - sp.height + 12 + bob - int(jump)
    rec = 0
    if name in ("fire", "runfire"):
        rec = int(8 * (1 - ease_out((t - e["t0"]) / 0.15))); ox_owner -= rec
    cv.alpha_composite(sp, (ox_owner, oy_owner))
    boxes.append({"id": "OWNER", "box": [ox_owner, oy_owner, ox_owner + sp.width, oy_owner + sp.height], "pose": name})
    if name == "dazed":
        dazed_stars(cv, ox_owner + sp.width * 0.45, oy_owner + 10, t)
    # impact frames on the owner (problem half hits)
    for fb in FRAMES:
        if "contact_t" in fb and not fb["n"].startswith("F9"):
            ct = fb["contact_t"]
            if ct <= t < ct + 2 / FPS:
                if any(x["primitive"] == "impact_frame" and x.get("target") == "owner" for x in fb["impact"]):
                    silhouette(cv, sp, (ox_owner, oy_owner))
                if not st.fired.get(("dust", fb["n"])):
                    st.fired[("dust", fb["n"])] = True
                    for x in fb["impact"]:
                        if x["primitive"] == "particles" and abs(x["t"] - ct) < 1e-6:
                            if x["kind"] == "dust":
                                st.P.emit(x["n"], ox_owner + sp.width / 2, T.ground_y - 6, (60, 240), -160, 0.45, (168, 146, 106), size=12, gravity=600)
                            elif x["kind"] == "sheet":
                                st.P.emit(x["n"], ox_owner + sp.width + 120, T.ground_y - 300, (120, 360), -220, 0.9, (250, 250, 245), size=30, kind="sheet", gravity=450)
    if deferred is not None:
        deferred(cv)
    # impact star at the contact (problem half): between him and the obstacle, at chest height
    for fb in FRAMES:
        if "contact_t" in fb and not fb["n"].startswith("F9") and any(x["primitive"] == "impact_star" for x in fb["impact"]):
            ct = fb["contact_t"]
            if ct <= t < ct + 2 / FPS:
                impact_star(cv, ox_owner + sp.width + 30, oy_owner + int(sp.height * 0.35))
    # rings on the clearing hits
    for fb in FRAMES:
        if fb["n"].startswith("F9") and fb["obstacle"] != 3:
            ct = fb["contact_t"]; rk = (wt - ct) / 0.2
            if 0 <= rk < 1:
                ob = next((b for b in boxes if b["id"] == f"OBST_{fb['obstacle']}"), None)
                if ob:
                    bx = ob["box"]; ring(cv, (bx[0] + bx[2]) / 2, (bx[1] + bx[3]) / 2, int(20 + 240 * ease_out(rk)), max(2, int(12 * (1 - rk))), int(255 * (1 - rk)))

    # phone: fall, land, glow, flash; held through F8
    HAND = {"catch": (0.86, 0.02), "powered": (0.84, 0.22), "windup": (0.5, 0.1), "fire": (0.9, 0.3)}
    hf = HAND.get(name, (0.85, 0.15)); hand = (ox_owner + int(sp.width * hf[0]) - 30, oy_owner + int(sp.height * hf[1]))
    st.hand_world = hand   # for the UI-layer phone drop (17.2-17.4): the target is the hand in world space
    if INSTALL_T <= t < 19.6:
        pw, ph = 70, 120
        if True:
            glow = min(1.0, (t - INSTALL_T) / 0.2) if t < FLASH_T else 0.6 + 0.3 * math.sin(t * 6)
            phone_item(cv, hand[0], hand[1], pw, ph, glow, S); boxes.append({"id": "PHONE", "box": [hand[0], hand[1], hand[0] + pw, hand[1] + ph]})
            if abs(t - INSTALL_T) < 1 / FPS and not st.fired.get("install"):
                st.fired["install"] = True; st.ev.append({"t": round(t, 3), "event": "install", "note": "phone lands in the raised hand (catch pose) at install_event_t; powered from here"})
    if FLASH_T <= t < FLASH_T + 5 / FPS:
        k = (t - FLASH_T) / (5 / FPS); r = int(60 + 1500 * ease_out(k))
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ov).ellipse((hand[0] + 35 - r, hand[1] + 60 - r, hand[0] + 35 + r, hand[1] + 60 + r), fill=(240, 255, 255, int(235 * (1 - k))))
        cv.alpha_composite(ov)
    if powered and t < 18.2 and not st.fired.get("sparks"):
        st.fired["sparks"] = True; st.P.emit(10, ox_owner + sp.width / 2, oy_owner + sp.height / 2, (120, 320), -80, 0.6, (3, 255, 241), size=9, kind="spark", gravity=0, up_only=False)

    # projectiles: the F8 test tick and one per clearing beat (board 'projectile' at t0+0.3)
    shots = [(18.4, -300, None)] + [(fb["t0"] + 0.3, 0, fb) for fb in FRAMES if fb["n"].startswith("F9")]
    for t_fire, rise, fb in shots:
        if t_fire <= t < t_fire + 0.55:
            k = t - t_fire; fx = ox_owner + sp.width + 6; fy = oy_owner + int(sp.height * 0.3)
            if k < 0.08:
                muzzle_flash(cv, fx, fy, k / 0.08)
            x = fx + k * 900; y = int(fy + rise * k)
            if fb is None or wt < fb["contact_t"]:
                tick_with_trail(cv, x, y); boxes.append({"id": "TICK", "box": [int(x), y, int(x) + 7 * TICK_SCALE, y + 7 * TICK_SCALE]})
            if abs(k) < 1 / FPS and not st.fired.get(("fire", t_fire)):
                st.fired[("fire", t_fire)] = True; st.ev.append({"t": round(t, 3), "event": "fire"})

    # flag (F10), in front
    if n == "F10" and polex is not None:
        fy = T.ground_y - 120 - (min(1.0, max(0.0, (tl - 1.0) / 0.8))) * (T.ground_y - 120 - (POLE_TOP + 10))
        d.rectangle((polex + 14, fy, polex + 150, fy + 90), fill=hx(T.brand_blue), outline=hx(T.ink), width=2)
        cv.alpha_composite(PF.render("✓", 8, fg=rgb(T.cyan)), (polex + 60, int(fy) + 15))
        boxes.append({"id": "FLAG", "box": [polex, int(fy), polex + 150, int(fy) + 90]})
        if abs(tl - 1.0) < 1 / FPS and not st.fired.get("flag"):
            st.fired["flag"] = True; st.ev.append({"t": round(t, 3), "event": "flag_reached"})
        for tb in (26.6, 26.9):
            if abs(t - tb) < 1 / FPS and not st.fired.get(("conf", tb)):
                st.fired[("conf", tb)] = True
                for c in ((255, 241, 0), (3, 255, 241), (48, 181, 2), (255, 255, 255)):
                    st.P.emit(10, polex + 60, T.ground_y - 400, (300, 700), -500, 1.6, c, size=16, kind="confetti", gravity=700)

    st.P.step(1 / FPS); st.P.draw(cv)
    return cv


# ── the UI layer (Lane A strings, scales, positions; drawn after the camera) ─
def draw_ui(cv, t, log, S, st):
    f = beat_at(t); n = f["n"]; tl = t - f["t0"]
    d = ImageDraw.Draw(cv); cxs = (T.safe[0] + T.safe[2]) // 2; put = G.put_text
    # obstacle labels: problem half from 0.4 s to the beat end; clearing half a 0.4-s recall flash
    if "obstacle" in f:
        k = f["obstacle"]; clearing = n.startswith("F9")
        show = (tl >= 0.4) if not clearing else (tl < 0.4)
        if show:
            put(cv, log, f"OBST_{k}", DECK[f"OBST_{k}"], T.label_scale, T.yellow, cx=cxs, y=T.label_y)
    # checklist (from F9.1; persists through F10, fades 26.6-27.0)
    fade_chk = 1.0
    if n == "F10" and tl >= 1.0:
        fade_chk = max(0.0, 1 - (tl - 1.0) / 0.4)
    if (n.startswith("F9") or n == "F10") and fade_chk > 0:
        done = {"F9.1": 0, "F9.2": 1, "F9.3": 2, "F9.4": 3, "F9.5": 4, "F10": 5}[n]
        rows = list(range(done))
        if n.startswith("F9") and tl >= 0.75:
            rows.append(done)
        for r in rows:
            key = f"CHIP_{r + 1}"; y = T.checklist_y0 + r * T.checklist_row; x = T.checklist_x
            if n.startswith("F9") and r == done and tl < 1.1:
                k2 = ease_out((tl - 0.75) / 0.35); cw = G.text_img(DECK[key], T.checklist_scale, T.green).width
                x_start = max(T.safe[0] + T.chip_pad, min(T.safe[2] - cw - T.chip_pad, 700 - cw // 2))
                x = int(x_start + (T.checklist_x - x_start) * k2); y = int(880 + (y - 880) * k2)
            if fade_chk >= 1.0:
                put(cv, log, key, DECK[key], T.checklist_scale, T.green, x=x, y=y, pad=T.chip_pad)
                if n.startswith("F9") and r == done and 1.1 <= tl < 1.2:
                    b = log[-1]["backing_box"]; d.rectangle(b, outline=hx(T.white, int(255 * (1 - (tl - 1.1) / 0.1))), width=3)
            else:
                layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                put(layer, log, key, DECK[key], T.checklist_scale, T.green, x=x, y=y, pad=T.chip_pad)
                al = layer.split()[3].point(lambda p: int(p * fade_chk)); layer.putalpha(al); cv.alpha_composite(layer)
            if n.startswith("F9") and r == done and abs(tl - 1.1) < 1 / FPS and not st.fired.get(("chip", key)):
                st.fired[("chip", key)] = True; st.ev.append({"t": round(t, 3), "event": "chip", "chip": key})
    # HUD
    hp = health_at(t); hkey = f"HUD_HEALTH_{hp}"; powered = t >= INSTALL_T
    put(cv, log, "HUD_NAME", DECK["HUD_NAME"], T.hud_scale, T.white, x=T.safe[0] + 12, y=T.hud_y + 6)
    hfg = T.cyan if powered else (T.white if hp > 1 else T.yellow)
    for fb in FRAMES:   # hud_flash: the lost segment row blinks white/yellow for 0.4 s after each hit
        if "contact_t" in fb and not fb["n"].startswith("F9") and any(x["primitive"] == "hud_flash" for x in fb["impact"]):
            if fb["contact_t"] <= t < fb["contact_t"] + 0.4 and int(t * 12) % 2 == 0:
                hfg = T.yellow if hfg == T.white else T.white
    hx0 = T.safe[0] + 12 + G.text_img(DECK["HUD_NAME"], T.hud_scale, T.white).width + 40
    put(cv, log, hkey, DECK[hkey], T.hud_scale, hfg, x=hx0, y=T.hud_y + 6)
    if powered and t >= 18.0:
        pxx = hx0 + G.text_img(DECK[hkey], T.hud_scale, hfg).width + 36
        d.rectangle((pxx, T.hud_y - 2, pxx + 30, T.hud_y + 52), fill=hx(T.brand_blue), outline=hx(T.ink), width=3)
        d.rectangle((pxx + 6, T.hud_y + 6, pxx + 24, T.hud_y + 40), fill=hx(T.cyan))
    chip = S.wordmark.resize((T.chip_box[2] - T.chip_box[0], T.chip_box[3] - T.chip_box[1]), Image.LANCZOS)
    cv.alpha_composite(chip, (T.chip_box[0], T.chip_box[1]))
    log.append({"id": "WORDMARK_CHIP", "text": "RentOk (raster)", "kind": "logo", "box": list(T.chip_box), "fg": None, "backing": None})
    # state flashes
    blink = int(t * 4) % 2 == 0
    if n == "F1" and tl < 1.2 and blink:
        put(cv, log, "LEVEL", DECK["LEVEL"], T.flash_scale, T.white, cx=cxs, y=T.flash_y)
    if n == "F6" and tl >= 1.6 and blink:
        put(cv, log, "GAMEOVER", DECK["GAMEOVER"], T.flash_scale, T.yellow, cx=cxs, y=T.flash_y)
    if n == "F8" and tl < 1.2 and blink:
        put(cv, log, "POWERUP", DECK["POWERUP"], T.flash_scale, T.cyan, cx=cxs, y=T.flash_y)
    if n == "F10" and tl >= 1.0 and blink:
        put(cv, log, "CLEAR", DECK["CLEAR"], T.flash_scale, T.yellow, cx=cxs, y=T.flash_y_f10)
    # cheat panel (F7): geometry and typing exactly Lane A's
    if n == "F7":
        slide = min(1.0, tl / 0.5); py = int(520 + (1 - slide) * 500); panel = (105, py, 848, py + 400)
        if tl < 2.4:   # v2: the panel fades from 17.4 (the code is complete at 17.2; the gift takes the frame) — Lane A faded from 17.6
            d.rectangle(panel, fill=hx(T.panel), outline=hx(T.cyan), width=6)
        else:
            fade = max(0.0, 1 - (tl - 2.4) / 0.3)
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ov).rectangle(panel, fill=hx(T.panel, int(255 * fade)), outline=hx(T.cyan, int(255 * fade)), width=6)
            cv.alpha_composite(ov)
        if slide >= 1.0 and tl < 2.4:
            put(cv, log, "CHEAT_HDR", DECK["CHEAT_HDR"], 7, T.white, cx=cxs, y=py + 36, backing=T.panel)
            full1, full2 = DECK["CHEAT_1"], DECK["CHEAT_2"]
            nchars = int(max(0.0, (tl - 0.8)) / 1.4 * (len(full1) + len(full2)))
            s1 = full1[:min(nchars, len(full1))]; s2 = full2[:max(0, nchars - len(full1))]
            if s1:
                put(cv, log, "CHEAT_1" if s1 == full1 else "CHEAT_1_partial", s1, T.cheat_scale, T.cyan, cx=cxs, y=py + 130, backing=T.panel)
            if s2:
                put(cv, log, "CHEAT_2" if s2 == full2 else "CHEAT_2_partial", s2, T.cheat_scale, T.cyan, cx=cxs, y=py + 240, backing=T.panel)
    if 17.2 <= t < INSTALL_T and st.hand_world is not None and st.view is not None:
        # the gift: the phone drops OUT of the cheat panel (its centre, screen space) into the hand, in front of the panel
        pw, ph = 70, 120
        hx_, hy_ = to_screen([st.hand_world[0], st.hand_world[1], st.hand_world[0] + pw, st.hand_world[1] + ph], st.view)[:2]
        sx0, sy0 = cxs - pw // 2, 860   # emerges from the panel's bottom edge (920), clear of the RENTOK APP line's backing (750-840)
        k = ease_in((t - 17.2) / 0.2); px_ = int(sx0 + (hx_ - sx0) * k); py_ = int(sy0 + (hy_ - sy0) * k)
        for i in range(1, 4):
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ov).rectangle((px_, py_ - i * 26, px_ + pw, py_ - i * 26 + ph), fill=hx(T.cyan, 60 - i * 15)); cv.alpha_composite(ov)
        phone_item(cv, px_, py_, pw, ph, 0.4, S)
        log.append({"id": "PHONE_DROP", "text": "phone item (graphic)", "kind": "graphic", "box": [px_, py_, px_ + pw, py_ + ph], "fg": None, "backing": None})
    if FLASH_T <= t < FLASH_T + 1 / FPS:
        d.rectangle((0, 0, W, H), fill=(255, 255, 255, 200))


def end_card(t, S, log):
    f = BEAT_BY_N["F11"]; tl = t - f["t0"]; k = min(1.0, tl / 0.3)
    card = (2, 57, 255)   # Lane A D-11: the logo card blue, hard-coded from the Stage 2 measurement
    cv = Image.new("RGBA", (W, H), (*card, 255))
    wm = S.wordmark; ww = T.endcard_wordmark_w; wh = int(ww * wm.height / wm.width)
    wmi = wm.resize((ww, wh), Image.LANCZOS); cxs = (T.safe[0] + T.safe[2]) // 2
    wx = cxs - ww // 2; wy = 560
    cv.alpha_composite(wmi, (wx, wy))
    log.append({"id": "WORDMARK", "text": "RentOk (raster)", "kind": "logo", "box": [wx, wy, wx + ww, wy + wh], "fg": None, "backing": None})
    G.put_text(cv, log, "CTA_1", DECK["CTA_1"], T.cta_scale, T.white, cx=cxs, y=960, backing=None)
    G.put_text(cv, log, "CTA_2", DECK["CTA_2"], T.cta_scale, T.white, cx=cxs, y=1050, backing=None)
    G.put_text(cv, log, "URL", DECK["URL"], T.url_scale, T.white, cx=cxs, y=1170, backing=None)
    if k < 1.0:
        cv = Image.blend(Image.new("RGBA", (W, H), (*card, 255)), cv, k)
    return cv


# ── the render loop ──────────────────────────────────────────────────────────
def render(name, poses, out, i0=0, i1=None, encode=True):
    S = V2Sprites(JOB / "gen/assets", poses); plate_img = S.plate()
    st = State(); log_all = []
    total = int(round(FRAMES[-1]["t1"] * FPS)); i1 = total if i1 is None else min(i1, total)
    out.parent.mkdir(parents=True, exist_ok=True)
    qa = JOB / "qa" / name; (qa / "frames").mkdir(parents=True, exist_ok=True)
    proc = None
    if encode:
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
               "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-b:v", "9M", "-maxrate", "12M", "-bufsize", "18M",
               "-g", str(FPS // 2), "-bf", "2", "-r", str(FPS), "-movflags", "+faststart+negative_cts_offsets", "-use_editlist", "0", "-an", str(out)]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    last_world = None; last_wt = None; last_boxes = []
    beat_mid = {int(round((f["t0"] + f["t1"]) / 2 * FPS)): f["n"] for f in FRAMES}
    beat_mid[BOARD["hero_frame"]] = "F9.2 HERO"
    samples, sample_labels, keys, key_labels = [], [], [], []
    for i in range(i0, i1):
        t = i / FPS; f = beat_at(t); n = f["n"]
        log = []
        if n == "F11":
            cv = end_card(t, S, log); view = (0.0, 0.0, 1.0); sboxes = []
        else:
            wt = world_time(t)
            if last_world is not None and abs(wt - last_wt) < 1e-6:
                world = last_world; boxes = last_boxes          # hit-stop: the world frame is held
            else:
                boxes = []
                world = draw_world(t, wt, S, plate_img, st, boxes)
                mul, vig, lift, cyan = grade_for(t)
                if mul != (1, 1, 1) or vig or lift or cyan:
                    world = grade(world, mul, vig, lift, cyan)
                last_world, last_wt, last_boxes = world, wt, boxes
            s, cx, cy = camera(t); dx, dy = shake_offset(t)
            cv, view = apply_camera(world, s, cx, cy, dx, dy); cv = cv.copy()
            sboxes = [{**b, "screen_box": to_screen(b["box"], view)} for b in boxes]
            st.view = view
            draw_ui(cv, t, log, S, st)
        own = next((b for b in sboxes if b["id"] == "OWNER"), None)
        log_all.append({"frame": i, "t": round(t, 3), "world_t": round(world_time(t), 3) if n != "F11" else None, "beat": n, "powered": t >= INSTALL_T,
                        "camera": [round(view[2], 3), int(view[0]), int(view[1])], "owner_frac": round((own["screen_box"][3] - own["screen_box"][1]) / H, 3) if own else None,
                        "boxes": log, "sprites": sboxes})
        rgb_im = cv.convert("RGB")
        if proc is not None:
            proc.stdin.write(rgb_im.tobytes())
        if i % (FPS // 2) == 0 or i == total - 1:
            rgb_im.save(qa / "frames" / f"f{i:04d}_t{i / FPS:05.2f}.png"); samples.append(rgb_im); sample_labels.append(f"{i / FPS:05.2f}")
        if i in beat_mid:
            keys.append(rgb_im); key_labels.append(f"{beat_mid[i]} {i / FPS:05.2f}")
        if i % 150 == 0:
            print(f"  frame {i}/{total}", flush=True)
    if proc is not None:
        proc.stdin.close(); proc.wait()
    with open(JOB / f"gen/{name}-layout.jsonl", "w") as fh:
        for row in log_all:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    json.dump(st.ev, open(JOB / f"gen/{name}-events.json", "w"), indent=1)
    if samples:
        G.contact_sheet(samples, qa / "CONTACT-SHEET.png", labels=sample_labels)
    if keys:
        G.contact_sheet(keys, qa / "KEYFRAMES.png", cols=4, thumb_h=520, labels=key_labels)
    print("wrote", out if encode else "(frames only)", "| frames", i1 - i0, "| samples", len(samples), "| keyframes", len(keys), "| events", len(st.ev))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True); ap.add_argument("--poses", choices=["placeholder", "sheet"], required=True)
    ap.add_argument("--out", default=None); ap.add_argument("--t0", type=float, default=0.0); ap.add_argument("--t1", type=float, default=None)
    ap.add_argument("--no-encode", action="store_true")
    a = ap.parse_args()
    render(a.name, a.poses, Path(a.out or (JOB / f"gen/{a.name}.mp4")), int(round(a.t0 * FPS)), None if a.t1 is None else int(round(a.t1 * FPS)), encode=not a.no_encode)
