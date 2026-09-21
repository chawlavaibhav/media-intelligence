#!/usr/bin/env python3
"""render_c.py — Treatment C renderer for the 14.0–20.8 s window (RENTOK-CREATIVE-QUALITY-001).

Same topology as Lane A (AI stills + code): this module IMPORTS the frozen render_game.py (byte-identical copy in this
folder) for its tokens, sprites, ground, plate, text primitive, debris and font, and re-implements the window's frames
with the direction in 05-TREATMENT-PLAN-AND-COSTS.md §2b. Board beats, every string and every UI position are unchanged,
so the layout-log gates of the baseline apply unchanged.

New primitives (05 §2c), all code, USD 0:
  world/UI layer split · camera(scale, cx, cy, shake) crop-and-scale of the WORLD only · hit-stop with catch-up
  (world time remap) · screen shake · easing · pose table by time · colour grade (cold low point / bright power state,
  vignette) · aura pulse + shirt palette shift · particles (dust, sparks, paper sheets with rotation) · shockwave ring,
  impact star, muzzle flash, projectile trail · obstacle motion curves (dive, recoil, drift-off, lean) · phone glow and
  flash-from-source · run bob + lean.

Modes: --poses placeholder  (USD-0 animatic: the eight new poses are stand-ins built from the four baseline bitmaps)
       --poses sheet        (the drawn 2x4 expression/pose sheet keyed into gen/assets/c_*.png)
Writes gen/<name>.mp4 (video only), gen/<name>-layout.jsonl (UI boxes per frame), gen/<name>-events.json.
"""
from __future__ import annotations

import argparse
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
import render_game as G  # noqa: E402  (frozen copy)
import pixfont as PF  # noqa: E402

T = G.T; W, H = G.W, G.H; FPS = G.FPS
hx, rgb = G.hx, G.rgb
T0, T1 = 14.0, 20.8333   # frames 420..624 inclusive = 205 frames, as the baseline clip

# ── timing constants of the direction (05 §2b) ───────────────────────────────
HIT_T = 14.1            # swarm contact (board: F6 t0 + 1.5)
INSTALL_T = 17.4        # board install_event_t (unchanged)
FLASH_T = 17.6
CLEAR_HIT_T = 20.35     # board: F9.1 t0 + 0.75
HOLDS = [(HIT_T, 3 / FPS), (CLEAR_HIT_T, 2 / FPS)]         # hit-stop: (start, duration); world catches up at 1.25x
CATCHUP_RATE = 1.25
SHAKES = [(HIT_T, 10, 0.25), (FLASH_T, 6, 0.15), (CLEAR_HIT_T, 8, 0.2)]   # (start, amplitude px, decay s)


def ease_out(k):   return 1 - (1 - min(1.0, max(0.0, k))) ** 3
def ease_in(k):    return min(1.0, max(0.0, k)) ** 3
def ease_in_out(k):
    k = min(1.0, max(0.0, k)); return 3 * k * k - 2 * k * k * k


def world_time(t: float) -> float:
    """Hit-stop: the world freezes for `d` at each hold, then runs at CATCHUP_RATE until it has caught up (4d)."""
    wt = t
    for h0, d in HOLDS:
        if t < h0:
            continue
        if t < h0 + d:
            wt -= (t - h0)                     # frozen
        elif t < h0 + d + 4 * d:
            wt -= d - (t - h0 - d) * (CATCHUP_RATE - 1)   # catching up
        # else fully caught up
    return wt


def shake_offset(t: float) -> tuple:
    dx = dy = 0.0
    for s0, amp, dec in SHAKES:
        if s0 <= t < s0 + dec:
            k = 1 - (t - s0) / dec
            dx += amp * k * math.sin((t - s0) * 95); dy += amp * k * 0.6 * math.cos((t - s0) * 70)
    return dx, dy


def camera(t: float) -> tuple:
    """(scale, cx, cy) of the world view. Push-in at the hit, hold through the panel, snap back on the flash, small push on the burst."""
    ocx, ocy = T.owner_x + 100, 940     # cy 940: at x1.30 the owner's head (world y 920) maps to screen y >= 933, below the cheat panel's bottom edge (920)
    if t < 14.05:
        return 1.0, W / 2, H / 2
    if t < 14.30:
        k = ease_out((t - 14.05) / 0.25); s = 1 + 0.30 * k
        return s, W / 2 + (ocx - W / 2) * k, H / 2 + (ocy - H / 2) * k
    if t < FLASH_T:
        return 1.30, ocx, ocy
    if t < CLEAR_HIT_T:
        return 1.0, W / 2, H / 2
    if t < CLEAR_HIT_T + 0.3:
        k = (t - CLEAR_HIT_T) / 0.3; s = 1 + 0.15 * math.sin(math.pi * k)
        return s, W / 2 + 200 * math.sin(math.pi * k), H / 2 - 60 * math.sin(math.pi * k)
    return 1.0, W / 2, H / 2


def apply_camera(world: Image.Image, scale: float, cx: float, cy: float, dx: float, dy: float) -> Image.Image:
    if scale <= 1.001 and abs(dx) < 0.5 and abs(dy) < 0.5:
        return world
    cw, ch = W / scale, H / scale
    x0 = min(max(0.0, cx - cw / 2 + dx), W - cw); y0 = min(max(0.0, cy - ch / 2 + dy), H - ch)
    crop = world.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch)))
    return crop.resize((W, H), Image.NEAREST)


# ── colour grade ─────────────────────────────────────────────────────────────
_VIG = None


def vignette_mask(strength: float) -> Image.Image:
    global _VIG
    if _VIG is None:
        yy, xx = np.mgrid[0:H, 0:W]
        r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / math.sqrt(2)
        _VIG = np.clip(r, 0, 1) ** 1.6
    return _VIG * strength


def grade(world: Image.Image, mul: tuple, vig: float, lift: float = 0.0, cyan: float = 0.0) -> Image.Image:
    """Multiply RGB by `mul`, darken corners by `vig`, lift luminance by `lift` (0..1), add a cyan cast to highlights."""
    a = np.asarray(world.convert("RGB")).astype(np.float32) / 255.0
    a = a * np.array(mul, dtype=np.float32)
    if vig > 0:
        a *= (1 - vignette_mask(vig))[:, :, None]
    if lift > 0:
        a = a + lift * (1 - a) * 0.6
    if cyan > 0:
        lum = a.mean(axis=2, keepdims=True)
        a = a + cyan * np.clip(lum - 0.55, 0, 1) * np.array([0.0, 0.35, 0.45], dtype=np.float32)
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).convert("RGBA")


def grade_for(t: float):
    """(mul, vig, lift, cyan) per beat: cold from the hit to the flash, bright-cyan after."""
    if t < HIT_T:
        return (1, 1, 1), 0.0, 0.0, 0.0
    if t < 15.0:
        k = ease_in_out((t - HIT_T) / 0.9)
        return (1 - 0.45 * k, 1 - 0.40 * k, 1 - 0.25 * k), 0.35 * k, 0.0, 0.0
    if t < 17.2:
        return (0.55, 0.60, 0.75), 0.35, 0.0, 0.0
    if t < FLASH_T:
        k = (t - 17.2) / 0.4
        return (0.55 + 0.45 * k, 0.60 + 0.40 * k, 0.75 + 0.25 * k), 0.35 * (1 - k), 0.0, 0.0
    return (1.0, 1.0, 1.0), 0.0, 0.10, 0.18


# ── poses ────────────────────────────────────────────────────────────────────
class CSprites(G.Sprites):
    """Baseline four poses + eight C poses. `placeholder` builds stand-ins from the baseline bitmaps so the animatic
    can be judged at USD 0; `sheet` loads gen/assets/c_<pose>.png keyed from the drawn 2x4 sheet."""
    C_POSES = ["hurt", "cornered", "cornered_up", "catch", "powered", "windup", "fire", "brace"]

    def __init__(self, assets: Path, poses: str):
        super().__init__("final", assets); self.poses_mode = poses

    def cpose(self, name: str) -> Image.Image:
        k = ("c", name, self.poses_mode)
        if k in self._c:
            return self._c[k]
        h = T.owner_h
        if self.poses_mode == "sheet" and (self.assets / f"c_{name}.png").exists():
            im = Image.open(self.assets / f"c_{name}.png").convert("RGBA")
            # one common scale for all eight cells: the standing 'brace' cell (344 px in the sheet) -> owner_h, so a
            # kneeling pose stays shorter than a standing one instead of being stretched to the same height
            f = h / 344.0
            im = im.resize((max(1, int(im.width * f)), max(1, int(im.height * f))), Image.NEAREST)
        else:
            base = {"hurt": "jump", "cornered": "idle", "cornered_up": "idle", "catch": "jump", "powered": "idle",
                    "windup": "runB", "fire": "runA", "brace": "idle"}[name]
            im = self._load(f"owner_{base}", int(h * 0.75), h).copy()
            if name == "hurt":
                im = im.rotate(-18, Image.NEAREST, expand=True)
            elif name in ("cornered", "cornered_up"):
                im = im.resize((im.width, int(im.height * 0.72)), Image.NEAREST)
            elif name == "windup":
                im = im.rotate(6, Image.NEAREST, expand=True)
            elif name == "fire":
                im = im.rotate(-6, Image.NEAREST, expand=True)
            # placeholder marker: a small magenta dot so the animatic reader knows the pose is a stand-in
            ImageDraw.Draw(im).rectangle((0, 0, 10, 10), fill=(255, 0, 255, 255))
        self._c[k] = im
        return im

    def powered_sprite(self, im: Image.Image, t: float) -> Image.Image:
        """Pulsing aura (alpha 60<->140 at 3 Hz) + shirt palette shift (the checked-shirt blue toward cyan)."""
        a = np.asarray(im).astype(np.int16)
        blue = (a[:, :, 2] > 150) & (a[:, :, 0] < 120) & (a[:, :, 3] > 0)
        out = a.copy(); out[blue, 0] = np.minimum(255, a[blue, 0] + 10); out[blue, 1] = np.minimum(255, a[blue, 1] + 70); out[blue, 2] = 255
        sp = Image.fromarray(out.astype(np.uint8))
        alpha = int(100 + 40 * math.sin(t * 2 * math.pi * 3))
        mask = sp.split()[3]
        halo = Image.new("RGBA", (sp.width + 24, sp.height + 24), (0, 0, 0, 0))
        for dx in range(-6, 7, 3):
            for dy in range(-6, 7, 3):
                layer = Image.new("RGBA", halo.size, (0, 0, 0, 0)); layer.paste(hx(T.cyan, alpha), (12 + dx, 12 + dy), mask)
                halo = Image.alpha_composite(halo, layer)
        halo.alpha_composite(sp, (12, 12))
        return halo


def pose_at(t: float) -> tuple:
    """(pose name, is_c_pose). The direction's pose table for the window."""
    if t < 14.05:
        return ("runA" if int(t * 8) % 2 == 0 else "runB"), False
    if t < HIT_T:
        return "brace", True
    if t < 14.5:
        return "hurt", True
    if t < 16.8:
        return "cornered", True
    if t < 17.35:
        return "cornered_up", True
    if t < FLASH_T:
        return "catch", True
    if t < 18.2:
        return "powered", True
    if t < 18.4:
        return "windup", True
    if t < 18.75:
        return "fire", True
    if t < 19.6:
        return "powered", True
    if t < 19.8:
        return ("runA" if int(t * 8) % 2 == 0 else "runB"), False
    if t < 19.9:
        return "windup", True
    if t < 20.15:
        return "fire", True
    return ("runA" if int(t * 8) % 2 == 0 else "runB"), False


# ── particles ────────────────────────────────────────────────────────────────
class Particles:
    def __init__(self):
        self.ps = []; self.rng = np.random.default_rng(3)

    def emit(self, n, x, y, spread, vy0, life, color, size=8, kind="dot", gravity=900):
        for _ in range(n):
            ang = self.rng.uniform(-math.pi, 0) if kind != "spark" else self.rng.uniform(0, 2 * math.pi)
            sp = self.rng.uniform(*spread)
            self.ps.append({"x": x, "y": y, "vx": math.cos(ang) * sp, "vy": math.sin(ang) * sp + vy0, "life": life, "age": 0.0,
                            "c": color, "s": size, "kind": kind, "rot": self.rng.uniform(0, 360), "g": gravity})

    def step(self, dt):
        for p in self.ps:
            p["age"] += dt; p["x"] += p["vx"] * dt; p["y"] += p["vy"] * dt; p["vy"] += p["g"] * dt
            if p["kind"] == "sheet":
                p["vx"] *= 0.97; p["vy"] = min(p["vy"], 260); p["rot"] += 240 * dt
        self.ps = [p for p in self.ps if p["age"] < p["life"]]

    def draw(self, cv: Image.Image):
        d = ImageDraw.Draw(cv)
        for p in self.ps:
            k = 1 - p["age"] / p["life"]; a = int(255 * k)
            if p["kind"] == "sheet":
                sh = Image.new("RGBA", (int(p["s"] * 1.4), p["s"]), (250, 250, 245, a)); ImageDraw.Draw(sh).rectangle((0, 0, sh.width - 1, sh.height - 1), outline=(30, 30, 40, a), width=2)
                sh = sh.rotate(p["rot"], Image.NEAREST, expand=True); cv.alpha_composite(sh, (int(p["x"]), int(p["y"])))
            else:
                s = max(2, int(p["s"] * (0.5 + 0.5 * k)))
                d.rectangle((int(p["x"]), int(p["y"]), int(p["x"]) + s, int(p["y"]) + s), fill=(*p["c"], a))


def impact_star(cv, x, y, r=46, color=(255, 241, 0, 255)):
    d = ImageDraw.Draw(cv); pts = []
    for i in range(12):
        rr = r if i % 2 == 0 else r * 0.42; ang = i * math.pi / 6
        pts.append((x + rr * math.cos(ang), y + rr * math.sin(ang)))
    d.polygon(pts, fill=color, outline=hx(T.ink)); d.polygon(pts, outline=hx(T.ink), width=3)


def ring(cv, x, y, r, width, alpha):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ov).ellipse((x - r, y - r, x + r, y + r), outline=(255, 255, 255, alpha), width=width)
    cv.alpha_composite(ov)


def muzzle_flash(cv, x, y, k):
    r = int(26 * (1 - k) + 8); d = ImageDraw.Draw(cv)
    d.polygon([(x, y - r), (x + r * 0.35, y - r * 0.35), (x + r, y), (x + r * 0.35, y + r * 0.35), (x, y + r), (x - r * 0.35, y + r * 0.35), (x - r, y), (x - r * 0.35, y - r * 0.35)], fill=(255, 255, 255, 230))
    d.ellipse((x - r * 0.4, y - r * 0.4, x + r * 0.4, y + r * 0.4), fill=hx(T.cyan))


def tick_with_trail(cv, x, y, k_dir=1):
    for i in range(1, 6):
        g = PF.render("✓", 4, fg=rgb(T.cyan)); a = g.split()[3].point(lambda p, i=i: int(p * (0.55 - i * 0.1)))
        g.putalpha(a); cv.alpha_composite(g, (int(x - i * 14 * k_dir), y))
    G.draw_tick(cv, int(x), y)


def phone_item(cv, x, y, w, h, glow: float, S):
    if glow > 0:
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ov).ellipse((x - 40, y - 40, x + w + 40, y + h + 40), fill=hx(T.cyan, int(120 * glow)))
        cv.alpha_composite(ov.filter(ImageFilter.GaussianBlur(18)))
    d = ImageDraw.Draw(cv)
    d.rectangle((x, y, x + w, y + h), fill=hx(T.brand_blue), outline=hx(T.ink), width=4)
    d.rectangle((x + 6, y + 8, x + w - 6, y + h - 8), fill=hx(T.cyan) if glow > 0 else (12, 20, 60, 255))
    if glow > 0.5:
        sm = S.wordmark.resize((w - 16, int((w - 16) * S.wordmark.height / S.wordmark.width)), Image.LANCZOS); cv.alpha_composite(sm, (x + 8, y + h // 2 - sm.height // 2))


# ── the world ────────────────────────────────────────────────────────────────
def draw_world(t: float, wt: float, S: CSprites, plate_img, P: Particles, ev: list, fired: dict) -> Image.Image:
    cv = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    camx = G.camera_x(wt)
    bg = plate_img
    px = int(camx * 0.25) % bg.width
    strip = Image.new("RGB", (W, H)); strip.paste(bg.crop((px, 0, min(px + W, bg.width), H)), (0, 0))
    if px + W > bg.width:
        strip.paste(bg.crop((0, 0, px + W - bg.width, H)), (bg.width - px, 0))
    cv.paste(strip, (0, 0)); G.draw_ground(cv, camx)
    d = ImageDraw.Draw(cv)

    # ── obstacle 5 (swarm): dives on a curve, recoils on the hit, hovers over him, drifts off during the panel
    if wt < 15.6:
        im = S.obst(5); tl = wt - 12.6
        base_x = 1080 - tl * T.scroll_problem
        if wt < HIT_T:
            k = max(0.0, min(1.0, tl / 1.5)); oy = T.ground_y - 300 - 260 * (1 - k) ** 1.5; ox = base_x
        elif wt < 15.0:
            k = ease_out((wt - HIT_T) / 0.4); ox = base_x + 30 * k; oy = T.ground_y - 300 - 40 * k + 10 * math.sin(wt * 9)
        else:
            k = ease_in((wt - 15.0) / 0.6); ox = base_x + 30 + 80 * k; oy = T.ground_y - 340 - 900 * k
        cv.alpha_composite(im, (int(ox), int(oy)))
        if HIT_T <= t < HIT_T + 2 / FPS and t >= HIT_T:
            impact_star(cv, int(ox) + 40, int(oy) + 150)
    # ── obstacle 1 (wall): re-enters taller and leaning; bursts with debris + paper sheets + shockwave
    if wt >= 19.6:
        tl = wt - 19.6; im = S.obst(1); big = im.resize((int(im.width * 1.3), int(im.height * 1.3)), Image.NEAREST)
        lean = big.rotate(6, Image.NEAREST, expand=True)
        ox = 1080 - tl * T.scroll_clear; oy = T.ground_y - lean.height + 8
        if wt < CLEAR_HIT_T:
            cv.alpha_composite(lean, (int(ox), int(oy)))
        else:
            kk = min(1.0, (wt - CLEAR_HIT_T) / 0.35)
            G.debris(cv, big, int(ox), int(oy), kk, seed=1)
            if not fired.get("sheets"):
                fired["sheets"] = True
                P.emit(14, ox + big.width / 2, oy + big.height / 3, (150, 420), -300, 0.9, (250, 250, 245), size=34, kind="sheet", gravity=500)
                P.emit(10, ox + 40, T.ground_y - 10, (80, 260), -120, 0.5, (200, 190, 160), size=10, gravity=700)
                ev.append({"t": round(t, 3), "event": "burst", "obstacle": 1})
            rk = (wt - CLEAR_HIT_T) / 0.2
            if rk < 1:
                ring(cv, ox + big.width / 2, oy + big.height / 2, int(20 + 240 * ease_out(rk)), max(2, int(12 * (1 - rk))), int(255 * (1 - rk)))
            if wt < CLEAR_HIT_T + 2 / FPS:
                white = Image.new("RGBA", big.size, (255, 255, 255, 0)); white.putalpha(big.split()[3].point(lambda p: int(p * 0.9)))
                cv.alpha_composite(white, (int(ox), int(oy)))

    # ── owner
    name, is_c = pose_at(t)
    powered = t >= INSTALL_T
    sp = S.cpose(name) if is_c else S.owner(name, False)
    bob = -int(3 * abs(math.sin(t * 2 * math.pi * 4))) if name.startswith("run") else 0
    if name.startswith("run"):
        sp = sp.rotate(-8, Image.NEAREST, expand=True)
    knock = 0
    if HIT_T <= t < 14.5:
        knock = int(90 * (1 - ease_out((t - HIT_T) / 0.4)))
    elif 14.5 <= t < FLASH_T:
        knock = 20
    ox_owner = T.owner_x - knock
    oy_owner = T.ground_y - sp.height + bob
    if powered:
        sp = S.powered_sprite(sp, t); ox_owner -= 12; oy_owner = T.ground_y - sp.height + 12 + bob
    if name == "fire":
        rec = int(8 * (1 - ease_out((t - (18.4 if t < 19 else 19.9)) / 0.15))) if t >= 18.4 else 0
        ox_owner -= rec
    cv.alpha_composite(sp, (ox_owner, oy_owner))
    HAND = {"catch": (0.86, 0.02), "powered": (0.84, 0.22)}      # hand anchor per pose (fraction of sprite w, h)
    hf = HAND.get(name, (0.85, 0.15)); hand = (ox_owner + int(sp.width * hf[0]) - 30, oy_owner + int(sp.height * hf[1]))
    if HIT_T <= t < HIT_T + 2 / FPS:                                # impact frame: white silhouette
        white = Image.new("RGBA", sp.size, (255, 255, 255, 0)); white.putalpha(sp.split()[3].point(lambda p: int(p * 0.85))); cv.alpha_composite(white, (ox_owner, oy_owner))
        if not fired.get("dust"):
            fired["dust"] = True; P.emit(8, ox_owner + sp.width / 2, T.ground_y - 6, (60, 220), -160, 0.45, (168, 146, 106), size=12, gravity=600)
            ev.append({"t": round(t, 3), "event": "hit", "obstacle": 5})

    # ── the phone: falls with a glow and a trail, lands in the hand at INSTALL_T, lights up, flashes at FLASH_T
    if 17.2 <= t < 19.6:
        pw, ph = 70, 120
        if t < INSTALL_T:
            k = ease_in((t - 17.2) / 0.2); py = int(160 + (hand[1] - 160) * k); pxx = hand[0]
            for i in range(1, 4):
                ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ov).rectangle((pxx, py - i * 26, pxx + pw, py - i * 26 + ph), fill=hx(T.cyan, 60 - i * 15)); cv.alpha_composite(ov)
            phone_item(cv, pxx, py, pw, ph, 0.4, S)
        else:
            glow = min(1.0, (t - INSTALL_T) / 0.2) if t < FLASH_T else 0.6 + 0.3 * math.sin(t * 6)
            phone_item(cv, hand[0], hand[1], pw, ph, glow, S)
            if abs(t - INSTALL_T) < 1 / FPS and not fired.get("install"):
                fired["install"] = True; ev.append({"t": round(t, 3), "event": "install", "note": "phone lands in the raised hand (catch pose)"})
    if FLASH_T <= t < FLASH_T + 5 / FPS:                            # flash from the phone
        k = (t - FLASH_T) / (5 / FPS); r = int(60 + 1500 * ease_out(k))
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ov).ellipse((hand[0] + 35 - r, hand[1] + 60 - r, hand[0] + 35 + r, hand[1] + 60 + r), fill=(240, 255, 255, int(235 * (1 - k))))
        cv.alpha_composite(ov)
    if powered and t < 18.2 and not fired.get("sparks"):
        fired["sparks"] = True; P.emit(10, ox_owner + sp.width / 2, oy_owner + sp.height / 2, (120, 320), -80, 0.6, (3, 255, 241), size=9, kind="spark", gravity=0)

    # ── projectiles: wind-up then fire; muzzle flash; trail
    for t_fire, rise in ((18.4, -300), (19.9, 0)):
        if t_fire <= t < t_fire + 0.5:
            k = t - t_fire; fx = ox_owner + sp.width + 10; fy = oy_owner + 70
            if k < 0.08:
                muzzle_flash(cv, fx, fy, k / 0.08)
            x = fx + k * 900; y = int(fy + rise * k)
            if not (t_fire == 19.9 and wt >= CLEAR_HIT_T):
                tick_with_trail(cv, x, y)
    P.step(1 / FPS); P.draw(cv)
    return cv


def draw_ui(cv: Image.Image, t: float, log: list, deck: dict, S: CSprites, board) -> None:
    """The UI layer — every string at the baseline's positions and scales (the gates measure these boxes)."""
    f = G.beat_at(board, t); n = f["n"]; tl = t - f["t0"]
    d = ImageDraw.Draw(cv); cxs = (T.safe[0] + T.safe[2]) // 2
    put = G.put_text
    # obstacle labels (board timing)
    if n == "F6" and tl >= 0.4:
        put(cv, log, "OBST_5", deck["OBST_5"], T.label_scale, T.yellow, cx=cxs, y=T.label_y)
    if n == "F9.1" and tl < 0.4:
        put(cv, log, "OBST_1", deck["OBST_1"], T.label_scale, T.yellow, cx=cxs, y=T.label_y)
    # chip flight (ease-out + landing pop)
    if n == "F9.1" and tl >= 0.75:
        k2 = ease_out((tl - 0.75) / 0.35); cw = G.text_img(deck["CHIP_1"], T.checklist_scale, T.green).width
        x_start = max(T.safe[0] + T.chip_pad, min(T.safe[2] - cw - T.chip_pad, 700 - cw // 2))
        x = int(x_start + (T.checklist_x - x_start) * k2); y = int(880 + (T.checklist_y0 - 880) * k2)
        put(cv, log, "CHIP_1", deck["CHIP_1"], T.checklist_scale, T.green, x=x, y=y, pad=T.chip_pad)
        if 1.1 <= tl < 1.2:   # landing pop: a bright outline around the chip for 3 frames
            b = log[-1]["backing_box"]; d.rectangle(b, outline=hx(T.white, int(255 * (1 - (tl - 1.1) / 0.1))), width=3)
    # HUD
    hp = G.health_at(t); hkey = f"HUD_HEALTH_{hp}"; powered = t >= INSTALL_T
    put(cv, log, "HUD_NAME", deck["HUD_NAME"], T.hud_scale, T.white, x=T.safe[0] + 12, y=T.hud_y + 6)
    hfg = T.cyan if powered else (T.white if hp > 1 else T.yellow)
    hx0 = T.safe[0] + 12 + G.text_img(deck["HUD_NAME"], T.hud_scale, T.white).width + 40
    put(cv, log, hkey, deck[hkey], T.hud_scale, hfg, x=hx0, y=T.hud_y + 6)
    if powered and t >= 18.0:
        pxx = hx0 + G.text_img(deck[hkey], T.hud_scale, hfg).width + 36
        d.rectangle((pxx, T.hud_y - 2, pxx + 30, T.hud_y + 52), fill=hx(T.brand_blue), outline=hx(T.ink), width=3)
        d.rectangle((pxx + 6, T.hud_y + 6, pxx + 24, T.hud_y + 40), fill=hx(T.cyan))
    chip = S.wordmark.resize((T.chip_box[2] - T.chip_box[0], T.chip_box[3] - T.chip_box[1]), Image.LANCZOS)
    cv.alpha_composite(chip, (T.chip_box[0], T.chip_box[1]))
    log.append({"id": "WORDMARK_CHIP", "text": "RentOk (raster)", "kind": "logo", "box": list(T.chip_box), "fg": None, "backing": None})
    blink = int(t * 4) % 2 == 0
    if n == "F6" and tl >= 1.6 and blink:
        put(cv, log, "GAMEOVER", deck["GAMEOVER"], T.flash_scale, T.yellow, cx=cxs, y=T.flash_y)
    if n == "F8" and tl < 1.2 and blink:
        put(cv, log, "POWERUP", deck["POWERUP"], T.flash_scale, T.cyan, cx=cxs, y=T.flash_y)
    # cheat panel (unchanged geometry and typing)
    if n == "F7":
        slide = min(1.0, tl / 0.5); py = int(520 + (1 - slide) * 500); panel = (105, py, 848, py + 400)
        if tl < 2.6:
            d.rectangle(panel, fill=hx(T.panel), outline=hx(T.cyan), width=6)
        else:
            fade = max(0.0, 1 - (tl - 2.6) / 0.4)
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ov).rectangle(panel, fill=hx(T.panel, int(255 * fade)), outline=hx(T.cyan, int(255 * fade)), width=6)
            cv.alpha_composite(ov)
        if slide >= 1.0 and tl < 2.6:
            put(cv, log, "CHEAT_HDR", deck["CHEAT_HDR"], 7, T.white, cx=cxs, y=py + 36, backing=T.panel)
            full1, full2 = deck["CHEAT_1"], deck["CHEAT_2"]
            nchars = int(max(0.0, (tl - 0.8)) / 1.4 * (len(full1) + len(full2)))
            s1 = full1[:min(nchars, len(full1))]; s2 = full2[:max(0, nchars - len(full1))]
            if s1:
                put(cv, log, "CHEAT_1" if s1 == full1 else "CHEAT_1_partial", s1, T.cheat_scale, T.cyan, cx=cxs, y=py + 130, backing=T.panel)
            if s2:
                put(cv, log, "CHEAT_2" if s2 == full2 else "CHEAT_2_partial", s2, T.cheat_scale, T.cyan, cx=cxs, y=py + 240, backing=T.panel)
    if FLASH_T <= t < FLASH_T + 1 / FPS:   # one full-white impact frame on the flash
        d.rectangle((0, 0, W, H), fill=(255, 255, 255, 200))


def render(name: str, poses: str, out: Path):
    board, deck, frames = G.load()
    S = CSprites(JOB / "gen/assets", poses); plate_img = S.plate()
    P = Particles(); ev: list = []; fired: dict = {}; log_all: list = []
    i0, i1 = int(round(T0 * FPS)), int(round(T1 * FPS))
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-b:v", "9M", "-maxrate", "12M", "-bufsize", "18M",
           "-g", str(FPS // 2), "-bf", "2", "-r", str(FPS), "-movflags", "+faststart", "-an", str(out)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    last_world = None; last_wt = None
    for i in range(i0, i1):
        t = i / FPS; wt = world_time(t)
        if last_world is not None and abs(wt - last_wt) < 1e-6:
            world = last_world                       # hit-stop: the world frame is held
        else:
            world = draw_world(t, wt, S, plate_img, P, ev, fired)
            mul, vig, lift, cyan = grade_for(t)
            if mul != (1, 1, 1) or vig or lift or cyan:
                world = grade(world, mul, vig, lift, cyan)
            last_world, last_wt = world, wt
        s, cx, cy = camera(t); dx, dy = shake_offset(t)
        cv = apply_camera(world, s, cx, cy, dx, dy).copy()
        log: list = []
        draw_ui(cv, t, log, deck, S, board)
        log_all.append({"frame": i, "t": round(t, 3), "world_t": round(wt, 3), "beat": G.beat_at(board, t)["n"], "powered": t >= INSTALL_T,
                        "camera": [round(s, 3), int(cx), int(cy)], "boxes": log})
        proc.stdin.write(cv.convert("RGB").tobytes())
    proc.stdin.close(); proc.wait()
    with open(JOB / f"gen/{name}-layout.jsonl", "w") as fh:
        for row in log_all:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    json.dump(ev, open(JOB / f"gen/{name}-events.json", "w"), indent=1)
    print("wrote", out, "| frames", i1 - i0, "| events", ev)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True); ap.add_argument("--poses", choices=["placeholder", "sheet"], required=True)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    render(a.name, a.poses, Path(a.out or (JOB / f"gen/{a.name}.mp4")))
