#!/usr/bin/env python3
"""render_game.py — the film, rendered by code from board.json + copy-deck.json (Stage 4 A0 / A8 / A9 / A12).

Modes:  --mode animatic   grey placeholder sprites + code plate (USD 0; proves timing, safe zones, readability)
        --mode final      cut-out sprites from gen/assets/ (owner_idle/runA/runB/jump, obst_1..5, plate.png optional)

Writes: an H.264 MP4 (video only; audio is mixed by assemble.py), a layout log gen/<name>-layout.jsonl with every
text/logo box per frame (the input of qa_checks.py), sampled frames + contact sheet + keyframes under qa/<name>/.

One token source (DesignTokens below) for every geometry constant; every string comes from copy-deck.json and is
rendered by pixfont (byte-exact); the wordmark is the fetched raster placed by code. No model draws any letter.
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageOps

HERE = Path(__file__).resolve().parent
JOB = HERE.parent
sys.path.insert(0, str(HERE))
import pixfont as PF  # noqa: E402

FPS = 30
W, H = 1080, 1920


@dataclass(frozen=True)
class DesignTokens:
    safe: tuple = (65, 288, 888, 1248)       # Stage 2.2 intersection
    ground_y: int = 1180                     # R1 (animatic v1 look): 1130 → 1180, more play height; still inside the safe box (1248)
    hud_y: int = 300
    hud_scale: int = 6
    chip_box: tuple = (738, 300, 888, 377)   # wordmark chip in the HUD (150x77)
    label_y: int = 720
    label_scale: int = 7
    flash_y: int = 560
    flash_y_f10: int = 720
    flash_scale: int = 8
    cheat_scale: int = 10
    cta_scale: int = 10
    url_scale: int = 7
    checklist_x: int = 90
    checklist_y0: int = 400
    checklist_row: int = 54                  # R2a: 48 → 54 (chip backing is 50 px tall at scale 6 + pad 4); column bottom 666 < label zone 710
    checklist_scale: int = 6
    chip_pad: int = 4
    backing_pad: int = 10
    outline_px: int = 2
    owner_x: int = 260                       # left third of the safe box: room to run
    owner_h: int = 260                       # R4 (final-v2 look): 220 → 260, sprites read small at phone size; top at 920 stays clear of the label zone (≤ 779)
    scroll_problem: int = 400                # px/s
    scroll_clear: int = 480
    endcard_wordmark_w: int = 700
    # colours (Stage 3 palette; brand from source/rentok-brand)
    brand_blue: str = "#0038FF"
    cyan: str = "#03FFF1"
    yellow: str = "#FFF100"
    green: str = "#30B502"
    white: str = "#FFFFFF"
    ink: str = "#1E1E28"
    panel: str = "#0B0F1E"
    lane: str = "#A8926A"
    kerb: str = "#6E6455"
    sky_top: str = "#6FB7FF"
    sky_bot: str = "#CFEBFF"
    facade: str = "#F1E3C6"
    terracotta: str = "#C8683F"


T = DesignTokens()


def hx(h: str, a: int = 255) -> tuple:
    h = h.lstrip("#"); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def rgb(h: str) -> tuple:
    return hx(h)[:3]


# ── text with opaque backing (one primitive for every string) ────────────────
_cache: dict = {}


def text_img(text: str, scale: int, fg: str) -> Image.Image:
    k = (text, scale, fg)
    if k not in _cache:
        _cache[k] = PF.render(text, scale, fg=rgb(fg))
    return _cache[k]


def put_text(cv: Image.Image, log: list, key: str, text: str, scale: int, fg: str, *, cx=None, x=None, y: int,
             backing: str = T.ink, pad: int = T.backing_pad, kind: str = "text") -> tuple:
    im = text_img(text, scale, fg)
    if x is None:
        x = int(cx - im.width / 2)
    box = (x - pad, y - pad, x + im.width + pad, y + im.height + pad)
    if backing:
        ImageDraw.Draw(cv).rectangle(box, fill=hx(backing))
    cv.alpha_composite(im, (x, y))
    log.append({"id": key, "text": text, "kind": kind, "box": [x, y, x + im.width, y + im.height], "backing_box": list(box),
                "fg": fg, "backing": backing, "scale": scale})
    return box


# ── sprites ──────────────────────────────────────────────────────────────────
class Sprites:
    def __init__(self, mode: str, assets: Path):
        self.mode = mode; self.assets = assets; self._c = {}
        self.wordmark = Image.open(JOB / "source/rentok-brand/rentok-new-logo.webp").convert("RGBA")

    def _load(self, name: str, w: int, h: int) -> Image.Image:
        k = (name, w, h)
        if k in self._c:
            return self._c[k]
        p = self.assets / f"{name}.png"
        if self.mode == "final" and p.exists():
            im = Image.open(p).convert("RGBA")
            im = ImageOps.contain(im, (w, h), Image.NEAREST)
        else:
            im = self._placeholder(name, w, h)
        self._c[k] = im
        return im

    @staticmethod
    def _placeholder(name: str, w: int, h: int) -> Image.Image:
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        g = (120, 120, 130, 255); o = (40, 40, 50, 255)
        if name.startswith("owner"):
            d.rectangle((w * 0.25, h * 0.32, w * 0.75, h * 0.7), fill=g, outline=o, width=3)            # torso
            d.rectangle((w * 0.33, h * 0.05, w * 0.67, h * 0.32), fill=(150, 150, 160, 255), outline=o, width=3)  # head
            leg = 0.18 if name.endswith("runA") else 0.0
            d.rectangle((w * (0.28 + leg), h * 0.7, w * 0.46, h), fill=g, outline=o, width=3)
            d.rectangle((w * 0.54, h * 0.7, w * (0.72 - leg), h), fill=g, outline=o, width=3)
            d.ellipse((w * 0.7, h * 0.5, w * 0.86, h * 0.62), fill=(200, 180, 60, 255), outline=o, width=2)  # keys
            d.rectangle((w * 0.08, h * 0.45, w * 0.3, h * 0.62), fill=(200, 60, 60, 255), outline=o, width=2)  # register
        elif name == "obst_1":
            d.rectangle((0, h * 0.25, w, h), fill=(225, 225, 215, 255), outline=o, width=4)
            for i in range(4):
                d.line((10, h * (0.4 + i * 0.14), w - 10, h * (0.4 + i * 0.14)), fill=(160, 160, 150, 255), width=6)
            d.ellipse((w * 0.35, 0, w * 0.65, h * 0.28), fill=(80, 80, 90, 255))
        elif name == "obst_2":
            d.ellipse((0, h * 0.2, w, h), fill=(170, 130, 70, 255), outline=o, width=4)
            d.rectangle((w * 0.4, h * 0.45, w * 0.6, h * 0.7), fill=(90, 90, 100, 255), outline=o, width=3)
        elif name == "obst_3":
            d.rectangle((w * 0.3, 0, w * 0.7, h * 0.3), fill=(150, 150, 160, 255), outline=o, width=3)
            d.rectangle((w * 0.25, h * 0.3, w * 0.75, h * 0.72), fill=(90, 110, 160, 255), outline=o, width=3)
            d.rectangle((w * 0.28, h * 0.72, w * 0.72, h), fill=(60, 60, 80, 255), outline=o, width=3)
            d.rectangle((w * 0.72, h * 0.5, w, h * 0.8), fill=(120, 80, 50, 255), outline=o, width=3)  # suitcase
        elif name == "obst_4":
            for i in range(6):
                d.rectangle((w * 0.1 + (i % 2) * 14, h * (0.05 + i * 0.155), w * 0.9 - (i % 2) * 10, h * (0.05 + i * 0.155) + h * 0.14),
                            fill=(210, 205, 190, 255), outline=o, width=3)
        elif name == "obst_5":
            for (cx, cy) in [(0.3, 0.3), (0.7, 0.25), (0.5, 0.65), (0.2, 0.75), (0.8, 0.7)]:
                d.ellipse((w * cx - 40, h * cy - 32, w * cx + 40, h * cy + 32), fill=(200, 60, 60, 255), outline=o, width=3)
        elif name == "plate":
            return None
        return im

    def owner(self, pose: str, powered: bool) -> Image.Image:
        h = T.owner_h; w = int(h * 0.75)
        im = self._load(f"owner_{pose}", w, h)
        if not powered:
            return im
        k = ("powered", pose)
        if k not in self._c:
            base = im.copy()
            # aura: cyan halo built from the alpha mask, dilated by 6 px, then the sprite on top with a cyan-shifted outline
            mask = base.split()[3]
            halo = Image.new("RGBA", (w + 24, h + 24), (0, 0, 0, 0))
            for dx in range(-6, 7, 3):
                for dy in range(-6, 7, 3):
                    layer = Image.new("RGBA", halo.size, (0, 0, 0, 0))
                    layer.paste(hx(T.cyan, 110), (12 + dx, 12 + dy), mask)
                    halo = Image.alpha_composite(halo, layer)
            halo.alpha_composite(base, (12, 12))
            self._c[k] = halo
        return self._c[k]

    def obst(self, n: int) -> Image.Image:
        sizes = {1: (345, 368), 2: (276, 276), 3: (200, 300), 4: (300, 390), 5: (368, 300)}   # R4: x1.15
        return self._load(f"obst_{n}", *sizes[n])

    def plate(self) -> Image.Image | None:
        """The generated 9:16 plate, fitted to 1080x1920 and shifted up so its lane edge meets the engine's ground line
        (measured: the plate's lane starts at y 1602 after the fit; ground_y is 1180 → shift 422 px; the exposed top
        band is filled with the plate's own sky colour). Tiled 2x horizontally with a mirrored copy for the parallax."""
        p = self.assets / "plate.png"
        if not (self.mode == "final" and p.exists()):
            return None
        fit = ImageOps.fit(Image.open(p).convert("RGB"), (W, H), Image.LANCZOS)
        shift = 1602 - T.ground_y
        one = Image.new("RGB", (W, H), fit.getpixel((W // 2, 2)))
        one.paste(fit, (0, -shift))
        two = Image.new("RGB", (W * 2, H)); two.paste(one, (0, 0)); two.paste(ImageOps.mirror(one), (W, 0))
        return two


# ── repair-round-1 primitives ────────────────────────────────────────────────
def draw_tick(cv: Image.Image, x: int, y: int, scale: int = 4):
    """D-3: the projectile is the board's cyan tick mark (pixfont glyph), with a 1-scale dark shadow."""
    cv.alpha_composite(PF.render("✓", scale, fg=rgb(T.ink)), (x + scale, y + scale))
    cv.alpha_composite(PF.render("✓", scale, fg=rgb(T.cyan)), (x, y))


def debris(cv: Image.Image, sprite: Image.Image, ox: int, oy: int, k: float, seed: int, tiles: int = 6):
    """D-6: burst the sprite into tiles that fly outward with gravity and fade over k in [0,1]."""
    tw, th = max(1, sprite.width // tiles), max(1, sprite.height // tiles)
    rng = np.random.default_rng(seed)
    for j in range(tiles):
        for i in range(tiles):
            tile = sprite.crop((i * tw, j * th, (i + 1) * tw, (j + 1) * th))
            if tile.getbbox() is None:
                continue
            vx = (i - tiles / 2 + 0.5) * 90 + rng.uniform(-30, 30); vy = -260 + (j - tiles / 2) * 40 + rng.uniform(-40, 40)
            dx = int(vx * k * 1.1); dy = int(vy * k + 900 * k * k)
            a = tile.split()[3].point(lambda p: int(p * max(0.0, 1 - k)))
            tile.putalpha(a)
            cv.alpha_composite(tile, (ox + i * tw + dx, oy + j * th + dy))


def recolour_red_to_green(sprite: Image.Image, k: float) -> Image.Image:
    """D-6 (tickets): red bubbles turn brand green as k goes 0→1 (pixel test on the sprite, no model)."""
    a = np.asarray(sprite).astype(int)
    red = (a[:, :, 0] > 150) & (a[:, :, 1] < 110) & (a[:, :, 2] < 110) & (a[:, :, 3] > 0)
    g = np.array(rgb(T.green))
    out = a.copy()
    out[red, :3] = (a[red, :3] * (1 - k) + g * k).astype(int)
    return Image.fromarray(out.astype(np.uint8), "RGBA")


def neat_dashboard(w: int, h: int) -> Image.Image:
    """D-6 (ledger tower): after the hit the tower becomes one neat dashboard card — a brand-blue rounded panel with
    cyan bars and a green tick; no lettering."""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=18, fill=hx(T.brand_blue), outline=hx(T.ink), width=4)
    d.rounded_rectangle((14, 14, w - 15, 54), radius=8, fill=hx(T.white))
    for j, frac in enumerate([0.7, 0.45, 0.85, 0.55]):
        y0 = 74 + j * 40
        d.rectangle((16, y0, w - 16, y0 + 24), fill=hx(T.ink))
        d.rectangle((16, y0, 16 + int((w - 32) * frac), y0 + 24), fill=hx(T.cyan))
    im.alpha_composite(PF.render("✓", 6, fg=rgb(T.green)), (w - 60, 16))
    return im


def flash_sprite(cv: Image.Image, sprite: Image.Image, xy, alpha: int = 200):
    """D-9: hit flash on the character only (white silhouette from the alpha mask), never full-frame."""
    m = sprite.split()[3]
    white = Image.new("RGBA", sprite.size, (255, 255, 255, 0)); white.putalpha(m.point(lambda p: int(p * alpha / 255)))
    cv.alpha_composite(white, xy)


# ── world drawing ────────────────────────────────────────────────────────────
def code_plate() -> Image.Image:
    """The USD-0 fallback background (also the animatic background): sky gradient, a tall PG facade with stacked
    floors (the named vertical shape, CA-D6), rooftops. Deterministic; no lettering."""
    im = Image.new("RGB", (W * 2, H), rgb(T.sky_top)); d = ImageDraw.Draw(im)
    t0, t1 = rgb(T.sky_top), rgb(T.sky_bot)
    for y in range(0, T.ground_y):
        f = y / T.ground_y
        d.line((0, y, W * 2, y), fill=tuple(int(t0[i] + (t1[i] - t0[i]) * f) for i in range(3)))
    # far facade: tall block with stacked floors
    for bx in range(0, W * 2, 540):
        top = 330 + (bx // 540 % 3) * 60
        d.rectangle((bx + 40, top, bx + 420, T.ground_y), fill=rgb(T.facade), outline=rgb(T.terracotta), width=6)
        for fy in range(top + 40, T.ground_y - 40, 90):
            d.line((bx + 40, fy, bx + 420, fy), fill=rgb(T.terracotta), width=4)
            for wx in range(bx + 80, bx + 400, 80):
                d.rectangle((wx, fy + 22, wx + 34, fy + 62), fill=(110, 140, 170))
        d.rectangle((bx + 140, top - 70, bx + 220, top), fill=(60, 60, 70))  # water tank
        d.rectangle((bx + 440, T.ground_y - 260, bx + 530, T.ground_y), fill=(226, 205, 170), outline=rgb(T.terracotta), width=4)
    return im


def draw_ground(cv: Image.Image, camx: float):
    """The lane below the play line. D-7 (repair round 1, code only): the band is no longer a flat ochre field — a slab kerb
    (long stone slabs, not a brick bond), two darker wheel tracks, a drain grate, a manhole and a scooter silhouette scroll
    as a NEARER parallax layer (1.3x), and the bottom darkens with distance. Everything here is non-critical world art
    that platform UI may cover; the safe box is untouched."""
    d = ImageDraw.Draw(cv)
    g = T.ground_y
    d.rectangle((0, g, W, H), fill=hx(T.lane))
    # depth: darken toward the bottom of the frame
    for y in range(g + 240, H, 8):
        f = (y - g - 240) / (H - g - 240)
        d.rectangle((0, y, W, y + 8), fill=(int(0xA8 * (1 - 0.35 * f)), int(0x92 * (1 - 0.35 * f)), int(0x6A * (1 - 0.35 * f)), 255))
    # kerb: one row of long stone slabs with joints (no brick bond)
    d.rectangle((0, g, W, g + 26), fill=hx(T.kerb))
    d.rectangle((0, g + 26, W, g + 34), fill=(90, 82, 70, 255))
    off = int(camx) % 220
    for x in range(-off, W + 220, 220):
        d.rectangle((x, g + 2, x + 6, g + 26), fill=(78, 72, 62, 255))
    # nearer parallax layer (1.3x)
    fx = int(camx * 1.3)
    # two wheel tracks
    d.rectangle((0, g + 120, W, g + 150), fill=(150, 130, 92, 255))
    d.rectangle((0, g + 330, W, g + 366), fill=(150, 130, 92, 255))
    # painted kerb dashes (yellow, scrolling)
    off = fx % 160
    for x in range(-off, W + 160, 160):
        d.rectangle((x, g + 8, x + 70, g + 20), fill=(220, 190, 60, 255))
    # drain grate every 1400 px
    off = fx % 1400
    gx = 300 - off
    while gx < W + 200:
        d.rectangle((gx, g + 60, gx + 150, g + 96), fill=(70, 66, 60, 255), outline=hx(T.ink), width=3)
        for j in range(6):
            d.rectangle((gx + 12 + j * 22, g + 66, gx + 20 + j * 22, g + 90), fill=(120, 112, 100, 255))
        gx += 1400
    # manhole every 1400 px, offset
    off = (fx + 700) % 1400
    mx = 600 - off
    while mx < W + 200:
        d.ellipse((mx, g + 200, mx + 170, g + 260), fill=(120, 108, 84, 255), outline=hx(T.ink), width=3)
        d.ellipse((mx + 20, g + 208, mx + 150, g + 252), fill=(100, 90, 70, 255))
        mx += 1400
    # parked scooter silhouette every 2100 px (pixel primitives, no lettering)
    off = (fx + 300) % 2100
    sx = 800 - off
    while sx < W + 300:
        sy = g + 380
        d.rectangle((sx + 30, sy - 60, sx + 190, sy - 20), fill=(60, 64, 90, 255), outline=hx(T.ink), width=3)   # body
        d.rectangle((sx + 150, sy - 120, sx + 175, sy - 60), fill=(60, 64, 90, 255), outline=hx(T.ink), width=3)  # steering column
        d.rectangle((sx + 120, sy - 130, sx + 210, sy - 118), fill=hx(T.ink))                                       # handlebar
        d.rectangle((sx + 20, sy - 80, sx + 110, sy - 62), fill=(40, 40, 50, 255), outline=hx(T.ink), width=2)     # seat
        for wx in (sx + 10, sx + 170):
            d.ellipse((wx, sy - 30, wx + 50, sy + 20), fill=(30, 30, 36, 255), outline=hx(T.ink), width=3)
            d.ellipse((wx + 16, sy - 14, wx + 34, sy + 4), fill=(120, 120, 130, 255))
        d.ellipse((sx - 10, sy + 10, sx + 240, sy + 40), fill=(140, 122, 90, 255))                                   # ground shadow
        sx += 2100
    # small stones
    off = int(camx) % 140
    for x in range(-off, W, 140):
        d.rectangle((x + 30, g + 170, x + 42, g + 178), fill=hx(T.kerb))
        d.rectangle((x + 90, g + 290, x + 98, g + 296), fill=hx(T.kerb))


def desaturate(cv: Image.Image, amount: float) -> Image.Image:
    if amount <= 0:
        return cv
    g = ImageOps.grayscale(cv.convert("RGB")).convert("RGBA")
    return Image.blend(cv, g, min(1.0, amount))


# ── the timeline ─────────────────────────────────────────────────────────────
def load():
    board = json.load(open(JOB / "board.json")); deck = json.load(open(JOB / "copy-deck.json"))["strings"]
    frames = {f["n"]: f for f in board["frames"]}
    return board, deck, frames


def beat_at(board, t):
    for f in board["frames"]:
        if f["t0"] <= t < f["t1"]:
            return f
    return board["frames"][-1]


def camera_x(t: float) -> float:
    """World scroll in px: problem half 400 px/s; paused 15.0–18.0; 480 px/s from 18.0; stops at 26.6."""
    a = T.scroll_problem * min(t, 15.0)
    if t <= 15.0:
        return a
    if t <= 18.0:
        return a
    b = a + T.scroll_clear * (min(t, 26.6) - 18.0)
    return b


OBST_BEATS = {"F2": 1, "F3": 2, "F4": 3, "F5": 4, "F6": 5, "F9.1": 1, "F9.2": 2, "F9.3": 3, "F9.4": 4, "F9.5": 5}
CONTACT_X = T.owner_x + 200


def health_at(t: float) -> int:
    contacts = [3.3, 6.1, 8.6, 11.7, 14.1]   # t0 + 1.5 (obstacles 1,2,4,5) ; tenant pass at 8.6
    if t >= 17.6:
        return min(5, int((t - 17.6) / 0.08) + 1) if t < 18.0 else 5
    return 5 - sum(1 for c in contacts if t >= c)


def render_frame(i: int, board, deck, frames, S: Sprites, plate_img, log_all: list, events: list) -> Image.Image:
    t = i / FPS
    f = beat_at(board, t); n = f["n"]; tl = t - f["t0"]
    log: list = []
    cv = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    camx = camera_x(t)
    powered = t >= 17.4

    if n == "F11":
        # end card: freeze-dim to brand blue then the package
        k = min(1.0, tl / 0.3)
        card = S.wordmark.getpixel((100, 100))[:3]   # D-8: the logo file's own card blue (measured #0239FF) so no seam shows
        cv = Image.new("RGBA", (W, H), (*card, 255))
        wm = S.wordmark; ww = T.endcard_wordmark_w; wh = int(ww * wm.height / wm.width)
        wmi = wm.resize((ww, wh), Image.LANCZOS)
        cxs = (T.safe[0] + T.safe[2]) // 2
        wx = cxs - ww // 2; wy = 560
        cv.alpha_composite(wmi, (wx, wy))
        log.append({"id": "WORDMARK", "text": "RentOk (raster)", "kind": "logo", "box": [wx, wy, wx + ww, wy + wh], "fg": None, "backing": None})
        put_text(cv, log, "CTA_1", deck["CTA_1"], T.cta_scale, T.white, cx=cxs, y=960, backing=None)
        put_text(cv, log, "CTA_2", deck["CTA_2"], T.cta_scale, T.white, cx=cxs, y=1050, backing=None)
        put_text(cv, log, "URL", deck["URL"], T.url_scale, T.white, cx=cxs, y=1170, backing=None)
        if k < 1.0:
            # blend from the last game frame's blue dim: approximate by darkening the card in
            cv = Image.blend(Image.new("RGBA", (W, H), (*card, 255)), cv, k)
        log_all.append({"frame": i, "t": round(t, 3), "beat": n, "powered": True, "boxes": log}); return cv

    # background (parallax 0.25x)
    bg = plate_img if plate_img is not None else S._plate_cache if hasattr(S, "_plate_cache") else None
    if bg is None:
        bg = code_plate() if plate_img is None else plate_img
        S._plate_cache = bg
    px = int(camx * 0.25) % bg.width
    strip = Image.new("RGB", (W, H))
    strip.paste(bg.crop((px, 0, min(px + W, bg.width), H)), (0, 0))
    if px + W > bg.width:
        strip.paste(bg.crop((0, 0, px + W - bg.width, H)), (bg.width - px, 0))
    cv.paste(strip, (0, 0))
    draw_ground(cv, camx)

    # obstacles
    d = ImageDraw.Draw(cv)
    if n in OBST_BEATS:
        k = OBST_BEATS[n]; im = S.obst(k); clearing = n.startswith("F9")
        v = T.scroll_clear if clearing else T.scroll_problem
        if k == 3:   # the tenant: enters from behind (left), overtakes, exits right; never stopped
            ox = -200 + tl * (v * 1.9)
        else:
            ox = 1080 - tl * v
        oy = T.ground_y - im.height
        hit_t = 0.75 if clearing else 1.5
        alive = True
        if clearing and tl >= hit_t and k != 3:
            alive = False
            kk = min(1.0, (tl - hit_t) / 0.35)
            if k in (1, 2):                      # D-6: paper wall and money sack burst into flying debris
                debris(cv, im, int(ox), int(oy), kk, seed=k)
            elif k == 4:                         # D-6: the ledger tower becomes one neat dashboard card that shrinks toward the checklist
                card = neat_dashboard(220, 260)
                sc = max(0.25, 1 - kk * 0.75); cw, ch = int(220 * sc), int(260 * sc)
                cx0 = int(ox + im.width / 2 - cw / 2 + (T.checklist_x - ox) * kk * 0.5); cy0 = int(oy + im.height - ch - (oy + im.height - 700) * kk * 0.6)
                cv.alpha_composite(card.resize((cw, ch), Image.NEAREST), (cx0, cy0))
            elif k == 5:                         # D-6: the red ticket bubbles turn green, then fade
                green = recolour_red_to_green(im, min(1.0, kk * 2))
                if kk > 0.5:
                    al = green.split()[3].point(lambda p: int(p * (1 - (kk - 0.5) * 2))); green.putalpha(al)
                cv.alpha_composite(green, (int(ox), int(oy)))
        if alive:
            cv.alpha_composite(im, (int(ox), int(oy)))
        if clearing and k == 3 and tl >= hit_t:   # dues tag travels with him (3-A: tracked, not stopped)
            tx, ty = int(ox) + im.width // 2 - 22, int(oy) - 60
            d.rectangle((tx, ty, tx + 44, ty + 44), fill=hx(T.cyan), outline=hx(T.ink), width=3)
            for j in range(3):
                d.line((tx + 10, ty + 12 + j * 10, tx + 34, ty + 12 + j * 10), fill=hx(T.ink), width=3)
            if tl < hit_t + 0.04:
                events.append({"t": round(t, 3), "event": "tag", "obstacle": k})
        # burst / clear events + chip flight
        if clearing and hit_t <= tl < hit_t + 0.04:
            events.append({"t": round(t, 3), "event": "burst" if k != 3 else "tag", "obstacle": k})
        # label
        lab_key = f"OBST_{k}"
        show_label = (0.4 <= tl <= f["t1"] - f["t0"]) if not clearing else (tl < 0.4)
        if show_label:
            put_text(cv, log, lab_key, deck[lab_key], T.label_scale, T.yellow, cx=(T.safe[0] + T.safe[2]) // 2, y=T.label_y)
        # projectile in the clearing run (D-3: the board's tick mark)
        if clearing and 0.3 <= tl < hit_t:
            pxr = int(T.owner_x + 150 + (tl - 0.3) * 900)
            draw_tick(cv, pxr, T.ground_y - 160)
        hit_now = (not clearing) and hit_t <= tl < hit_t + 0.12 and k != 3   # D-9: flash the sprite, drawn after the owner below
    else:
        hit_now = False
    if n == "F8" and 0.4 <= tl < 0.9:  # test tick fired from the phone in his hand (D-4)
        pxr = int(T.owner_x + 150 + (tl - 0.4) * 900)
        draw_tick(cv, pxr, int(T.ground_y - 230 - (tl - 0.4) * 300))

    # owner
    jump = 0.0
    if n == "F1" and 0.6 <= tl < 1.1:
        jump = math.sin((tl - 0.6) / 0.5 * math.pi) * 170
    if n == "F3" and 1.0 <= tl < 1.5:
        jump = math.sin((tl - 1.0) / 0.5 * math.pi) * 150
    if n == "F10" and 0.6 <= tl < 1.0:
        jump = math.sin((tl - 0.6) / 0.4 * math.pi) * 200
    ox_owner = T.owner_x
    if n == "F10" and tl >= 0.6:
        ox_owner = int(T.owner_x + min(1.0, (tl - 0.6) / 0.4) * 280)
    pose = "idle"
    if n in ("F1", "F2", "F3", "F4", "F5", "F9.1", "F9.2", "F9.3", "F9.4", "F9.5", "F10"):
        pose = "runA" if int(t * 8) % 2 == 0 else "runB"
    if jump > 0:
        pose = "jump"
    if n == "F6" and tl >= 1.5:
        pose = "idle"
    if n == "F7":
        pose = "idle"
    knock = 0
    if n in ("F2", "F3", "F5") and 1.5 <= tl < 1.9:
        knock = int(60 * (1 - (tl - 1.5) / 0.4))
    if n == "F4" and 1.2 <= tl < 1.7:
        knock = int(40 * (1 - (tl - 1.2) / 0.5)); pose = "idle"
    if n == "F6" and tl >= 1.5:
        knock = 40
    if n == "F10" and tl >= 1.0:
        pose = "idle"                           # D-2 (cosmetic): he holds the pole instead of running on the spot
    if n == "F7" or (n == "F8" and tl < 1.6):
        pose = "idle"
    sp = S.owner(pose, powered)
    oy_owner = T.ground_y - sp.height + (12 if powered else 0) - int(jump)
    owner_xy = (ox_owner - knock - (12 if powered else 0), oy_owner)

    # flag pole is drawn BEFORE the owner so he stands in front of it (D-2 cosmetic)
    if n == "F10":
        polex = int(1080 - tl * T.scroll_clear) if tl < 1.0 else 600
        d.rectangle((polex, 520, polex + 14, T.ground_y), fill=(120, 120, 130, 255), outline=hx(T.ink), width=2)
    cv.alpha_composite(sp, owner_xy)
    if hit_now:
        flash_sprite(cv, sp, owner_xy)         # D-9
    # D-4: the phone stays in his raised hand from the drop (17.2) through the power-up beat (to 19.6): the install is him using the app
    if (n == "F7" and tl >= 2.6) or n == "F8":
        phx, phy = owner_xy[0] + sp.width - 30, owner_xy[1] + 60
        d.rectangle((phx, phy, phx + 60, phy + 104), fill=hx(T.brand_blue), outline=hx(T.ink), width=4)
        d.rectangle((phx + 6, phy + 8, phx + 54, phy + 96), fill=hx(T.cyan))
        sm = S.wordmark.resize((44, 23), Image.LANCZOS); cv.alpha_composite(sm, (phx + 8, phy + 40))

    # flag (F10) — the flag itself, in front
    if n == "F10":
        fy = T.ground_y - 120 - (min(1.0, max(0.0, (tl - 1.0) / 0.8))) * (T.ground_y - 120 - 540)
        d.rectangle((polex + 14, fy, polex + 150, fy + 90), fill=hx(T.brand_blue), outline=hx(T.ink), width=2)
        cv.alpha_composite(PF.render("✓", 8, fg=rgb(T.cyan)), (polex + 60, int(fy) + 15))
        if tl >= 1.0:
            for j in range(40):   # confetti (deterministic)
                cxp = (j * 97) % W; cyp = (int((tl - 1.0) * 400) + j * 53) % 700 + 300
                d.rectangle((cxp, cyp, cxp + 10, cyp + 10), fill=hx([T.yellow, T.cyan, T.green, T.white][j % 4]))
        if 1.0 <= tl:
            events.append({"t": round(t, 3), "event": "flag_reached"}) if abs(tl - 1.0) < 0.02 else None

    # desaturation around the low point / cheat panel
    if n == "F6" and tl >= 1.6:
        cv = desaturate(cv, (tl - 1.6) / 0.8)
    if n == "F7" and tl < 2.6:
        cv = desaturate(cv, 1.0 if tl < 2.2 else 1 - (tl - 2.2) / 0.4)
    d = ImageDraw.Draw(cv)

    # checklist (from F9.1; persists through F10)
    fade_chk = 1.0
    if n == "F10" and tl >= 1.0:
        fade_chk = max(0.0, 1 - (tl - 1.0) / 0.4)   # D-2: the checklist's proof is done; it fades so the raised flag is clearly seen
    if (n.startswith("F9") or n == "F10") and fade_chk > 0:
        done = {"F9.1": 0, "F9.2": 1, "F9.3": 2, "F9.4": 3, "F9.5": 4, "F10": 5}[n]
        rows = list(range(done))
        if n.startswith("F9") and tl >= 0.75:
            # chip in flight from the burst to its row over 0.35 s, then it sits
            rows.append(done)
        for r in rows:
            key = f"CHIP_{r + 1}"
            y = T.checklist_y0 + r * T.checklist_row
            x = T.checklist_x
            if n.startswith("F9") and r == done and tl < 1.1:
                k2 = (tl - 0.75) / 0.35
                cw = text_img(deck[key], T.checklist_scale, T.green).width
                x_start = max(T.safe[0] + T.chip_pad, min(T.safe[2] - cw - T.chip_pad, 700 - cw // 2))   # R2c: flight start clamped inside the safe box
                x = int(x_start + (T.checklist_x - x_start) * k2); y = int(880 + (y - 880) * k2)
            if fade_chk >= 1.0:
                put_text(cv, log, key, deck[key], T.checklist_scale, T.green, x=x, y=y, pad=T.chip_pad)
            else:   # fading: draw through an alpha layer, still logged as a box while any of it is visible
                layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                put_text(layer, log, key, deck[key], T.checklist_scale, T.green, x=x, y=y, pad=T.chip_pad)
                al = layer.split()[3].point(lambda p: int(p * fade_chk)); layer.putalpha(al); cv.alpha_composite(layer)
            if n.startswith("F9") and r == done and abs(tl - 1.1) < 0.02:
                events.append({"t": round(t, 3), "event": "chip", "chip": key})

    # HUD
    hp = health_at(t)
    hkey = f"HUD_HEALTH_{hp}"
    put_text(cv, log, "HUD_NAME", deck["HUD_NAME"], T.hud_scale, T.white, x=T.safe[0] + 12, y=T.hud_y + 6)
    hfg = T.cyan if powered else (T.white if hp > 1 else T.yellow)
    hx0 = T.safe[0] + 12 + text_img(deck["HUD_NAME"], T.hud_scale, T.white).width + 40
    put_text(cv, log, hkey, deck[hkey], T.hud_scale, hfg, x=hx0, y=T.hud_y + 6)
    if powered and t >= 18.0:   # phone icon beside the health bar
        pxx = hx0 + text_img(deck[hkey], T.hud_scale, hfg).width + 36
        d.rectangle((pxx, T.hud_y - 2, pxx + 30, T.hud_y + 52), fill=hx(T.brand_blue), outline=hx(T.ink), width=3)
        d.rectangle((pxx + 6, T.hud_y + 6, pxx + 24, T.hud_y + 40), fill=hx(T.cyan))
    chip = S.wordmark.resize((T.chip_box[2] - T.chip_box[0], T.chip_box[3] - T.chip_box[1]), Image.LANCZOS)
    cv.alpha_composite(chip, (T.chip_box[0], T.chip_box[1]))
    log.append({"id": "WORDMARK_CHIP", "text": "RentOk (raster)", "kind": "logo", "box": list(T.chip_box), "fg": None, "backing": None})

    # state flashes
    cxs = (T.safe[0] + T.safe[2]) // 2
    blink = int(t * 4) % 2 == 0
    if n == "F1" and tl < 1.2 and blink:
        put_text(cv, log, "LEVEL", deck["LEVEL"], T.flash_scale, T.white, cx=cxs, y=T.flash_y)
    if n == "F6" and tl >= 1.6 and blink:
        put_text(cv, log, "GAMEOVER", deck["GAMEOVER"], T.flash_scale, T.yellow, cx=cxs, y=T.flash_y)
    if n == "F8" and tl < 1.2 and blink:
        put_text(cv, log, "POWERUP", deck["POWERUP"], T.flash_scale, T.cyan, cx=cxs, y=T.flash_y)
    if n == "F10" and tl >= 1.0 and blink:
        put_text(cv, log, "CLEAR", deck["CLEAR"], T.flash_scale, T.yellow, cx=cxs, y=T.flash_y_f10)

    # cheat-code panel (F7)
    if n == "F7":
        slide = min(1.0, tl / 0.5)
        py = int(520 + (1 - slide) * 500)
        panel = (105, py, 848, py + 400)
        if tl < 2.6:
            d.rectangle(panel, fill=hx(T.panel), outline=hx(T.cyan), width=6)
        else:   # R2b: fade out in place (alpha), no text after 2.6 s
            fade = max(0.0, 1 - (tl - 2.6) / 0.4)
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ov).rectangle(panel, fill=hx(T.panel, int(255 * fade)), outline=hx(T.cyan, int(255 * fade)), width=6)
            cv.alpha_composite(ov); d = ImageDraw.Draw(cv)
        if slide >= 1.0 and tl < 2.6:
            put_text(cv, log, "CHEAT_HDR", deck["CHEAT_HDR"], 7, T.white, cx=cxs, y=py + 36, backing=T.panel)
            full1, full2 = deck["CHEAT_1"], deck["CHEAT_2"]
            nchars = int(max(0.0, (tl - 0.8)) / 1.4 * (len(full1) + len(full2)))
            s1 = full1[:min(nchars, len(full1))]; s2 = full2[:max(0, nchars - len(full1))]
            if s1:
                put_text(cv, log, "CHEAT_1" if s1 == full1 else "CHEAT_1_partial", s1, T.cheat_scale, T.cyan, cx=cxs, y=py + 130, backing=T.panel)
            if s2:
                put_text(cv, log, "CHEAT_2" if s2 == full2 else "CHEAT_2_partial", s2, T.cheat_scale, T.cyan, cx=cxs, y=py + 240, backing=T.panel)
        if 2.2 <= tl < 2.6:   # phone drops into his hand
            k2 = (tl - 2.2) / 0.4
            phx, phy = T.owner_x + 120, int(200 + (T.ground_y - 200 - 200) * k2)
            d.rectangle((phx, phy, phx + 70, phy + 120), fill=hx(T.brand_blue), outline=hx(T.ink), width=4)
            sm = S.wordmark.resize((56, 29), Image.LANCZOS); cv.alpha_composite(sm, (phx + 7, phy + 45))
            if abs(tl - 2.4) < 0.02:
                events.append({"t": round(t, 3), "event": "install", "note": "phone dropped into his raised hand at 17.4 and held through 19.6 (D-4); powered from 17.4"})
        if 2.6 <= tl < 2.7:
            d.rectangle((0, 0, W, H), fill=(255, 255, 255, 160))

    # aura pulse hint in F8 (POWER UP): brighten outline slightly — handled by sprite halo
    log_all.append({"frame": i, "t": round(t, 3), "beat": n, "powered": powered, "boxes": log})
    return cv


def contact_sheet(frames: list, out: Path, cols: int = 8, thumb_h: int = 320, labels=None):
    tw = int(thumb_h * W / H); rows = math.ceil(len(frames) / cols)
    sheet = Image.new("RGB", (cols * tw, rows * (thumb_h + 30)), (20, 20, 24))
    for j, im in enumerate(frames):
        th = im.convert("RGB").resize((tw, thumb_h), Image.LANCZOS)
        x, y = (j % cols) * tw, (j // cols) * (thumb_h + 30)
        sheet.paste(th, (x, y))
        if labels:
            sheet.alpha_composite if False else None
            lab = PF.render(labels[j], 2, fg=(255, 255, 255))
            sheet.paste(lab, (x + 6, y + thumb_h + 6), lab)
    sheet.save(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["animatic", "final"], required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--assets", default=str(JOB / "gen/assets"))
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    board, deck, frames = load()
    S = Sprites(a.mode, Path(a.assets)); plate_img = S.plate()
    total = int(round(board["frames"][-1]["t1"] * FPS))
    out = Path(a.out or (JOB / f"gen/{a.name}.mp4")); out.parent.mkdir(parents=True, exist_ok=True)
    qa = JOB / "qa" / a.name; (qa / "frames").mkdir(parents=True, exist_ok=True)
    log_all: list = []; events: list = []
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-b:v", "9M", "-maxrate", "12M", "-bufsize", "18M",
           "-g", str(FPS // 2), "-bf", "2", "-r", str(FPS), "-movflags", "+faststart", "-an", str(out)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    sample_every = FPS // 2   # 2 fps sampling
    beat_mid = {int(round((f["t0"] + f["t1"]) / 2 * FPS)): f["n"] for f in board["frames"]}
    if "F9.2" in frames:
        beat_mid[int(round(21.4 * FPS))] = "F9.2 HERO"
    samples, sample_labels, keys, key_labels = [], [], [], []
    for i in range(total):
        im = render_frame(i, board, deck, frames, S, plate_img, log_all, events)
        proc.stdin.write(im.convert("RGB").tobytes())
        if i % sample_every == 0 or i == total - 1:
            im.convert("RGB").save(qa / "frames" / f"f{i:04d}_t{i / FPS:05.2f}.png")
            samples.append(im); sample_labels.append(f"{i / FPS:05.2f}")
        if i in beat_mid:
            keys.append(im); key_labels.append(f"{beat_mid[i]} {i / FPS:05.2f}")
        if i % 150 == 0:
            print(f"  frame {i}/{total}", flush=True)
    proc.stdin.close(); proc.wait()
    with open(JOB / f"gen/{a.name}-layout.jsonl", "w") as fh:
        for row in log_all:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    json.dump(events, open(JOB / f"gen/{a.name}-events.json", "w"), indent=1)
    contact_sheet(samples, qa / "CONTACT-SHEET.png", labels=sample_labels)
    contact_sheet(keys, qa / "KEYFRAMES.png", cols=4, thumb_h=520, labels=key_labels)
    print("wrote", out, "| frames", total, "| samples", len(samples), "| keyframes", len(keys), "| events", len(events))


if __name__ == "__main__":
    main()
