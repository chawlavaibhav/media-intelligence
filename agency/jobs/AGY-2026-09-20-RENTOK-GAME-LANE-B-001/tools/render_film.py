#!/usr/bin/env python3
"""The film, by code. USD 0. AGY-2026-09-20-RENTOK-GAME-LANE-B-001 lane B.

World composed at 360x640 (sprites + plate + fx), nearest-neighbour x3 -> 1080x1920 (the retro pixel look, k=3, Stage 4);
HUD, labels, cards, cheat bar, banner and end card drawn CRISP at full resolution by tools/text_render.py (hb-view, gates).
Frames stream to ffmpeg (rawvideo rgb24 stdin) -> H.264 High yuv420p 30 fps, faststart, silent; audio is muxed by mix_audio.py.
Writes gen/render/TIMELINE.json (beats, from the measured VO durations), LAYOUT.json (every text placement per frame
range, for qa_checks.py), CONTACT_EVENTS.json (the ten contact events with their frame times).
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
JOB = HERE.parent
sys.path.insert(0, str(HERE))
import text_render as T  # noqa: E402

W, H, FPS = 1080, 1920, 30
LW, LH, K = 360, 640, 3
GROUND = 1150                     # screen y of the ground line (feet)
CHAR_X = 300                      # screen x of the character's centre
SCROLL = 420.0                    # px/s, world moves left
OUT = JOB / "gen" / "render"; OUT.mkdir(parents=True, exist_ok=True)

# ── measured VO (ffprobe, Stage 5; candidate A Sarvam) ────────────────────────
VO = {"V1": 2.645, "V2": 2.219, "V3": 2.731}

# ── timeline (F1..F17), derived from the frozen board + the measured VO rule (Stage 4 §4.5/4.6) ──
BEATS = [("F1", 1.2), ("F2", 1.84), ("F3", 1.84), ("F4", 1.84), ("F5", 1.84), ("F6", 1.84), ("F7", 1.4), ("F8", 2.8), ("F9", 2.4),
         ("F10", 1.6), ("F11", 1.6), ("F12", 1.6), ("F13", 1.6), ("F14", 1.6), ("F15", 1.6), ("F16", 1.2), ("F17", 2.2)]
TL = {}; t = 0.0
for name, d in BEATS:
    TL[name] = (round(t, 3), round(t + d, 3)); t += d
assert abs(t - 30.0) < 1e-6, t
VO_START = {"V1": TL["F8"][0] + 0.1, "V2": TL["F9"][0] + 1.3, "V3": TL["F16"][0] + 0.1}   # repair round 1, D-3: V2 starts when RENTOK MODE: ON appears (15.9 s)

# ── copy deck (Stage 3), exact strings ──────────────────────────────────────
DECK = {"C01": "PG OWNER", "C02": "LEVEL 1", "C03": "RENTOK MODE: OFF", "C04": "UNVERIFIED TENANT", "C05": "RENT NOT PAID",
        "C06": "LEFT WITHOUT PAYING", "C07": "ACCOUNTS MESS", "C08": "COMPLAINT CALLS", "C09": "CONTINUE?",
        "C10": "CHEAT CODE: INSTALL RENTOK", "C11": "INSTALLING...", "C12": "RENTOK MODE: ON", "C13": "TENANT: VERIFIED",
        "C14": "AUTOPAY: ON", "C15": "DUES VISIBLE", "C16": "REPORTS: DONE", "C17": "TICKETS RESOLVED", "C18": "LEVEL COMPLETE",
        "C19": "PG OWNER? LEVEL UP.", "C20": "Get the app"}
OBST = [("O1", "C04", "C13"), ("O2", "C05", "C14"), ("O3", "C06", "C15"), ("O4", "C07", "C16"), ("O5", "C08", "C17")]
CAP = lambda cap_px: int(round(cap_px / 0.72))     # hb-view font-size that yields ~cap_px cap height (Helvetica Neue caps ≈ 0.72 em)

BRAND_BLUE = (2, 57, 255); CYAN = (3, 255, 241); WHITE = (255, 255, 255); OCHRE = (227, 155, 43)

# ── assets ────────────────────────────────────────────────────────────────────
def load_sprite(path, height=None, width=None):
    im = Image.open(JOB / path).convert("RGBA")
    if height:
        im = im.resize((max(1, int(im.width * height / im.height)), height), Image.LANCZOS)
    elif width:
        im = im.resize((width, max(1, int(im.height * width / im.width))), Image.LANCZOS)
    return im


SL = json.load(open(JOB / "gen/sprites/SLICES.json"))
CH = {k: load_sprite(v["file"], height=92) for k, v in SL["A1"].items()}           # ≈ 276 px on screen (1/7 frame)
for _k in ("jump", "hurt", "cornered"):                                             # repair round 1, D-4: code-drawn register on the three cells that lacked it
    CH[_k] = load_sprite(f"gen/sprites/A1_{_k}_reg.png", height=92)
OB = {}
for oid, _, _ in OBST:
    b, a = SL[oid]["before"], SL[oid]["after"]
    if oid == "O5":
        OB[oid] = {"before": load_sprite(b["file"], width=118), "after": load_sprite(a["file"], width=132)}
    else:
        OB[oid] = {"before": load_sprite(b["file"], height=98), "after": load_sprite(a["file"], height=98)}
OB["O3"]["after"] = load_sprite("gen/sprites/O3_after_tracked.png", height=98)   # repair round 1, checker note: tick -> neutral tracked marker

# world plate -> low-res strip; sky detection for recolour
_plate = Image.open(JOB / "gen/stills/A3_world_plate_v1.png").convert("RGB")
PLATE_H = int(round((GROUND - 240) / 0.911 / K))         # plate scaled so its pavement (0.911 of height) sits on GROUND
PLATE_H = 333                                            # (1150-240)/0.911 = 999 px screen -> 333 low-res
_ps = _plate.resize((int(_plate.width * PLATE_H / _plate.height), PLATE_H), Image.LANCZOS)
_pa = np.asarray(_ps).astype(np.int16)
_sky_ref = np.array([176, 209, 216], np.int16)
SKY_MASK = (np.abs(_pa - _sky_ref).sum(axis=2) < 40)


def tinted_plate(after: bool) -> Image.Image:
    a = _pa.astype(np.float32).copy()
    h = a.shape[0]
    if after:
        a[..., 0] *= 0.82; a[..., 1] *= 0.92; a[..., 2] *= 1.08
        grad = np.linspace(0, 1, h)[:, None]
        sky = np.array(BRAND_BLUE, np.float32)[None, None, :] * (1 - grad[..., None] * 0.35) + np.array([94, 124, 255], np.float32) * grad[..., None] * 0.35
    else:
        a = a * 0.96 + np.array([232, 201, 160], np.float32) * 0.08
        sky = np.full((h, 1, 3), [242, 217, 180], np.float32)
    a[SKY_MASK] = np.broadcast_to(sky, (h, a.shape[1], 3))[SKY_MASK]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


PLATE = {False: tinted_plate(False), True: tinted_plate(True)}
# repair round 1, D-5: a near-parallax foreground pavement with objects cut from the same plate (scooter, tree) + code bollards/drains
def _fg_objects():
    objs = []
    for box, h in (((895, 636, 1040, 728), 46),):          # the scooter only (the tree crop carried wall pixels behind it — dropped)
        crop = _plate.crop(box).convert("RGBA")
        arr = np.asarray(crop).astype(np.int16)
        # key out the plate's flat pavement/road/sky colours around the object (distance from each of three refs)
        keep = np.ones(arr.shape[:2], bool)
        for ref in ((156, 136, 111), (107, 93, 80), (176, 209, 216), (191, 174, 144), (217, 193, 149), (220, 193, 150)):
            keep &= np.abs(arr[..., :3] - np.array(ref, np.int16)).sum(axis=2) > 36
        a = np.asarray(crop).copy(); a[..., 3] = np.where(keep, 255, 0).astype(np.uint8)
        im = Image.fromarray(a).resize((int(crop.width * h / crop.height), h), Image.LANCZOS)
        objs.append(im)
    return objs
FG_OBJS = _fg_objects()
FG_TOP = int((GROUND + 90) / K)          # low-res y where the foreground pavement starts (just under the plate's road edge)
FG_ROAD = int(1560 / K)
PLATE_TOP = 240 // K                                     # low-res y of the plate top


def world_bg(t: float, after: bool, mix: float = 0.0) -> Image.Image:
    """Sky + scrolling plate (mirrored tiles) + ground band, low-res. mix>0 blends before->after."""
    bg = Image.new("RGB", (LW, LH))
    d = ImageDraw.Draw(bg)
    sky = (242, 217, 180) if not after else BRAND_BLUE
    d.rectangle([0, 0, LW, PLATE_TOP + 2], fill=sky)
    # below the plate (repair round 1, D-5): a foreground pavement at 1.4x parallax with objects, then the road
    yb = PLATE_TOP + PLATE_H - 1
    pav = (168, 150, 122) if not after else (74, 92, 160)
    d.rectangle([0, yb, LW, FG_ROAD], fill=pav)
    d.rectangle([0, yb, LW, yb + 5], fill=(214, 200, 176) if not after else (150, 170, 230))            # kerb top
    d.rectangle([0, FG_ROAD - 6, LW, FG_ROAD], fill=(120, 106, 88) if not after else (40, 54, 120))     # kerb to the road
    d.rectangle([0, FG_ROAD, LW, LH], fill=(96, 92, 88) if not after else (44, 56, 110))
    off = int((t * SCROLL / K) % 60)
    for x in range(-off, LW + 60, 60):
        d.rectangle([x, FG_ROAD + 40, x + 28, FG_ROAD + 44], fill=(220, 210, 150) if not after else (150, 190, 255))
    # slab joints
    off2 = int((t * SCROLL * 1.4 / K) % 44)
    for x in range(-off2, LW + 44, 44):
        d.line([(x, yb + 5), (x, FG_ROAD - 6)], fill=(150, 132, 106) if not after else (60, 76, 140), width=1)
    # objects: scooter, tree, bollard, drain — repeating every 330 low-res px at 1.4x scroll
    fgs = int(t * SCROLL * 1.4 / K)
    period = 330
    k0 = fgs // period
    for i in range(k0 - 1, k0 + 3):
        x = i * period - fgs + 40
        kind = i % 4
        if kind == 0:
            ob = FG_OBJS[0]; bg.paste(ob, (x, FG_ROAD - ob.height - 4), ob)
        elif kind == 1:
            # code-drawn planter with a bush
            bx = x + 60
            d.rectangle([bx, FG_ROAD - 30, bx + 70, FG_ROAD - 6], fill=(150, 90, 60) if not after else (50, 60, 130), outline=(60, 40, 30) if not after else (24, 32, 70), width=2)
            for j, (ox, oy, r) in enumerate(((14, -34, 16), (36, -42, 20), (58, -34, 16))):
                d.ellipse([bx + ox - r, FG_ROAD + oy - r, bx + ox + r, FG_ROAD + oy + r], fill=(86, 140, 60) if not after else (60, 120, 110), outline=(40, 70, 30) if not after else (30, 60, 70), width=2)
        elif kind == 2:
            for j in range(3):
                d.rectangle([x + j * 40, FG_ROAD - 34, x + j * 40 + 8, FG_ROAD - 6], fill=(60, 60, 66) if not after else (24, 32, 70))
                d.rectangle([x + j * 40 - 2, FG_ROAD - 38, x + j * 40 + 10, FG_ROAD - 32], fill=(240, 220, 60) if not after else (3, 255, 241))
        else:
            d.rectangle([x, FG_ROAD - 22, x + 70, FG_ROAD - 8], fill=(70, 64, 58) if not after else (24, 32, 70))
            for j in range(6):
                d.line([(x + 6 + j * 11, FG_ROAD - 20), (x + 6 + j * 11, FG_ROAD - 10)], fill=pav, width=3)
    pl = PLATE[after]
    pw = pl.width
    scroll = int(t * SCROLL / K)
    x = -(scroll % (2 * pw))
    i = (scroll // (2 * pw)) * 2
    while x < LW:
        tile = pl if (i % 2 == 0) else pl.transpose(Image.FLIP_LEFT_RIGHT)
        bg.paste(tile, (x, PLATE_TOP)); x += pw; i += 1
    if 0 < mix < 1:
        other = world_bg(t, not after)
        bg = Image.blend(bg, other, 1 - mix) if after else Image.blend(other, bg, mix)
    return bg


# ── code-drawn graphics ───────────────────────────────────────────────────────
def heart(size=44, full=True) -> Image.Image:
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    col = (232, 52, 78, 255) if full else (60, 60, 70, 255)
    s = size / 16
    for (x, y) in [(2, 3), (3, 2), (4, 2), (5, 3), (6, 3), (7, 2), (8, 2), (9, 3)]:
        d.rectangle([x * s, y * s, (x + 1) * s, (y + 1) * s], fill=col)
    pts = [(1, 4), (10, 4), (10, 7), (9, 8), (8, 9), (7, 10), (6, 11), (5, 10), (4, 9), (3, 8), (2, 7), (1, 6)]
    d.polygon([(x * s + s / 2, y * s + s / 2) for x, y in pts], fill=col)
    d.polygon([(x * s, y * s) for x, y in [(1, 3), (11, 3), (11, 7), (6, 12), (1, 7)]], fill=col)
    if not full:
        d.rectangle([2 * s, 4 * s, 9 * s, 6 * s], fill=(30, 30, 38, 255))
    return im


def phone(width=60, glow=0.0, icon=True) -> Image.Image:
    h = int(width * 2)
    pad = 20
    im = Image.new("RGBA", (width + 2 * pad, h + 2 * pad), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if glow > 0:
        g = Image.new("RGBA", im.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        gd.rounded_rectangle([pad - 8, pad - 8, pad + width + 8, pad + h + 8], radius=14, fill=CYAN + (int(160 * glow),))
        im.alpha_composite(g.filter(ImageFilter.GaussianBlur(8)))
    d.rounded_rectangle([pad, pad, pad + width, pad + h], radius=8, fill=(20, 22, 30, 255), outline=(240, 240, 240, 255), width=2)
    d.rounded_rectangle([pad + 4, pad + 8, pad + width - 4, pad + h - 8], radius=4, fill=BRAND_BLUE + (255,))
    if icon:
        cx, cy = pad + width // 2, pad + h // 2; r = width // 4
        d.rounded_rectangle([cx - r, cy - r, cx + r, cy + r], radius=r // 3, fill=WHITE + (255,))
        d.polygon([(cx, cy - r * 0.6), (cx - r * 0.6, cy), (cx + r * 0.6, cy)], fill=BRAND_BLUE + (255,))
        d.rectangle([cx - r * 0.4, cy, cx + r * 0.4, cy + r * 0.55], fill=BRAND_BLUE + (255,))
    return im


def app_icon(size=120) -> Image.Image:
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=size // 4, fill=BRAND_BLUE + (255,))
    cx, cy, r = size // 2, size // 2, size // 3
    d.polygon([(cx, cy - r * 0.8), (cx - r * 0.8, cy - r * 0.1), (cx + r * 0.8, cy - r * 0.1)], fill=WHITE + (255,))
    d.rectangle([cx - r * 0.55, cy - r * 0.1, cx + r * 0.55, cy + r * 0.7], fill=WHITE + (255,))
    d.rectangle([cx - r * 0.15, cy + r * 0.2, cx + r * 0.15, cy + r * 0.7], fill=CYAN + (255,))
    return im


def flag_sprite() -> Image.Image:
    wm = T.wordmark(70)
    im = Image.new("RGBA", (wm.width + 10, 90), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, wm.width + 9, 89], fill=BRAND_BLUE + (255,), outline=(255, 255, 255, 255), width=3)
    im.alpha_composite(wm, (5, 10))
    return im


FLAG = flag_sprite()
ICON = app_icon(150)
PHONE_BIG = {g: phone(70, glow=g) for g in (0.0, 0.5, 1.0)}
HEART_F, HEART_E = heart(46, True), heart(46, False)
_plates: dict = {}
_layout: list = []
_contacts: list = []


def plate_for(cid: str, **kw) -> Image.Image:
    lines = kw.pop("lines", None)
    key = (cid, tuple(sorted(kw.items())), tuple(lines) if lines else None)
    if key not in _plates:
        im, rep = T.plate(lines or [DECK[cid]], id_=cid, **kw)
        _plates[key] = (im, rep)
    return _plates[key][0]


def put(canvas: Image.Image, im: Image.Image, cx: int, cy: int, cid: str, t: float, record=True):
    x0, y0 = int(cx - im.width / 2), int(cy - im.height / 2)
    canvas.alpha_composite(im, (x0, y0))
    if record:
        _layout.append({"id": cid, "box": [x0, y0, x0 + im.width, y0 + im.height], "t": round(t, 3)})
    return (x0, y0, x0 + im.width, y0 + im.height)


# ── per-frame state ───────────────────────────────────────────────────────────
def beat_at(t):
    for name, (a, b) in TL.items():
        if a <= t < b:
            return name, t - a, b - a
    return "F17", t - TL["F17"][0], 2.2


def lowres(x): return int(round(x / K))


def char_pose(beat, lt, t):
    if beat in ("F1", "F2", "F3", "F4", "F5", "F6"):
        idx = int(t * 10) % 4
        pose = ["run1", "run2", "run3", "run4"][idx]
        if beat == "F2" and 0.9 < lt < 1.25: pose = "jump"
        if beat in ("F2", "F4") and 1.3 <= lt < 1.75: pose = "hurt"
        if beat == "F3" and 1.3 <= lt < 1.6: pose = "hurt"
        if beat == "F5" and 1.25 <= lt < 1.7: pose = "jump"
        if beat == "F6" and lt >= 1.2: pose = "cornered"
        return pose
    if beat in ("F7", "F8"): return "cornered"
    if beat == "F9": return "cornered" if lt < 0.9 else ("powerA" if int(t * 8) % 2 == 0 else "powerB")
    if beat in ("F10", "F11", "F12", "F13", "F14"): return "powerA" if int(t * 8) % 2 == 0 else "powerB"
    if beat == "F15": return "jump" if lt > 0.5 else "powerA"
    if beat == "F16": return "jump"
    return "cornered"


def render_frame(t: float) -> Image.Image:
    beat, lt, bd = beat_at(t)
    after = beat in ("F10", "F11", "F12", "F13", "F14", "F15", "F16") or (beat == "F9" and lt >= 1.3)
    if beat == "F17":
        # end card
        f = Image.new("RGBA", (W, H), BRAND_BLUE + (255,))
        fade = min(1.0, lt / 0.3)
        line = plate_for("C19", size=CAP(64), backing="0239FF", alpha=255, border="0239FF", face="cond-bold")   # deck said 84 cap: reduced to 64 condensed so the whole line fits the 950-px safe width (compositor, recorded)
        put(f, line, W // 2, 640, "C19", t)
        wm = T.wordmark(300); put(f, wm, W // 2, 900, "C21", t)
        cta = plate_for("C20", size=CAP(64), backing="FFFFFF", alpha=255, border="03FFF1", colour="0239FF", face="bold", inset=36)
        put(f, cta, W // 2, 1165, "C20", t)   # repair R1: plate bottom was 1249 > 1248 (safe-zone gate)
        if fade < 1:
            f = Image.blend(Image.new("RGBA", (W, H), (10, 12, 30, 255)), f, fade)
        return f.convert("RGB")

    # ---- world (low-res) ----
    scroll_t = t if beat not in ("F7", "F8", "F9") else TL["F7"][0]          # world holds still during freeze/install
    mix = 0.0
    if beat == "F9" and 1.3 <= lt < 1.6: mix = (lt - 1.3) / 0.3
    bg = world_bg(scroll_t, after, mix).convert("RGBA")
    # character
    pose = char_pose(beat, lt, t)
    sp = CH[pose]
    cx, feet = CHAR_X, GROUND
    bob = 0
    if pose.startswith("run") or pose.startswith("power"): bob = -int(3 * abs(math.sin(t * 20)))
    if pose == "jump":
        if beat == "F15":
            u = (lt - 0.5) / 1.1; feet = GROUND - int(380 * math.sin(math.pi * min(u, 1)) * (1 - 0.5 * u))
        else:
            u = 1 - abs((lt - 1.075) / 0.175) if beat == "F2" else 1 - abs((lt - 1.475) / 0.225)
            feet = GROUND - int(180 * max(0, u))
    knock = 0
    if pose == "hurt": knock = -60
    if beat == "F6" and lt >= 1.2: knock = -40
    if beat == "F15" and lt > 0.5: cx = CHAR_X + int(140 * min(1, (lt - 0.5) / 1.1))   # repair round 1, D-2: stops 160 px short of the pole
    if beat == "F16":
        cx = CHAR_X + 140
        feet = GROUND - int(40 * abs(math.sin(lt * 9)))                                  # D-6 note: a celebration hop (jump cell), not the cornered pose
    # obstacle for this beat
    ob_box = None
    struggle = beat in ("F2", "F3", "F4", "F5", "F6")
    power = beat in ("F10", "F11", "F12", "F13", "F14")
    if struggle or power:
        oi = ("F2", "F3", "F4", "F5", "F6").index(beat) if struggle else ("F10", "F11", "F12", "F13", "F14").index(beat)
        oid, lab_id, card_id = OBST[oi]
        rel = SCROLL + 100
        ox = 1100 + 140 - rel * lt if struggle else 1100 + 120 - rel * lt   # obstacle centre x (screen)
        state = "before"
        hit_t = 0.7 if power else None
        if power and lt >= hit_t:
            state = "after"; ox = (1100 + 120 - rel * hit_t) - SCROLL * (lt - hit_t)
        spr = OB[oid][state]
        oy_feet = GROUND if oid in ("O1", "O2", "O4") else (GROUND - 60 if oid == "O3" else GROUND - 100)   # repair round 1: swarm 30 px lower so the beam clears the name tag
        if state == "after" and power:
            oy_feet -= int(120 * min(1, (lt - hit_t) / 0.6))
        if oid == "O3": oy_feet -= int(10 * math.sin(t * 6))
        if oid == "O5": oy_feet -= int(14 * math.sin(t * 9))
        if struggle and lt >= 1.3 and oid != "O5":
            ox -= 40 * (lt - 1.3)          # keeps moving past the player
        lx, ly = lowres(ox - spr.width * K / 2), lowres(oy_feet - spr.height * K)
        sp_l = spr
        bg.alpha_composite(sp_l, (lx, ly))
        ob_box = (ox, oy_feet - spr.height * K, spr.width * K, spr.height * K)
    # flag (F15/F16)
    if beat in ("F15", "F16"):
        fx = 1100 - SCROLL * (lt if beat == "F15" else 1.6) if beat == "F15" else 1100 - SCROLL * 1.6
        fx = max(fx, CHAR_X + 300)   # repair round 1, D-2: the pole stops 300 px right of the player's start
        pole_x = lowres(fx)
        d = ImageDraw.Draw(bg)
        d.rectangle([pole_x - 2, lowres(GROUND - 520), pole_x + 2, lowres(GROUND)], fill=(230, 230, 230, 255))
        d.ellipse([pole_x - 6, lowres(GROUND - 532), pole_x + 6, lowres(GROUND - 520)], fill=CYAN + (255,))
        fy = GROUND - 500 + (int(360 * min(1, max(0, (lt - 0.9) / 0.6))) if beat == "F15" else 360)
        fl = FLAG.resize((FLAG.width // K, FLAG.height // K), Image.LANCZOS)
        bg.alpha_composite(fl, (pole_x + 3, lowres(fy)))
        _layout.append({"id": "G-flag", "box": [(pole_x + 3) * K, int(fy), (pole_x + 3 + fl.width) * K, int(fy) + fl.height * K], "t": round(t, 3)})
    # shield glow
    if after and beat != "F16":
        g = Image.new("RGBA", (LW, LH), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        pulse = 0.5 + 0.5 * math.sin(t * 7)
        r = 46 + int(4 * pulse)
        gd.ellipse([lowres(cx) - r, lowres(feet) - 100 - 4, lowres(cx) + r, lowres(feet) + 6], fill=CYAN + (int(70 + 40 * pulse),))
        bg.alpha_composite(g.filter(ImageFilter.GaussianBlur(3)))
    # character composite
    bg.alpha_composite(sp, (lowres(cx + knock) - sp.width // 2, lowres(feet + bob) - sp.height))
    # beam (power run)
    if power and 0.45 <= lt < 0.75 and ob_box:
        d = ImageDraw.Draw(bg)
        px, py = lowres(cx + 60), lowres(feet - 232)   # repair round 1: beam origin 18 px lower (gap to the tag)
        tx, ty = lowres(ob_box[0]), lowres(ob_box[1] + ob_box[3] / 2)
        u = min(1, (lt - 0.45) / 0.25)
        ex, ey = px + (tx - px) * u, py + (ty - py) * u
        d.line([(px, py), (ex, ey)], fill=CYAN + (255,), width=4)
        d.line([(px, py), (ex, ey)], fill=(255, 255, 255, 255), width=1)
        ok = T.glyphs("OK", "bold", 30, "03FFF1").resize((14, 10), Image.LANCZOS)
        bg.alpha_composite(ok, (int(ex) - 7, int(ey) - 5))
        _layout.append({"id": "G-beam", "box": [min(px, ex) * K, (min(py, ey) - 3) * K, max(px, ex) * K, (max(py, ey) + 3) * K], "t": round(t, 3)})
    # hit flash / stamp
    if power and 0.7 <= lt < 0.85 and ob_box:
        d = ImageDraw.Draw(bg)
        r = int(20 + 60 * (lt - 0.7) / 0.15)
        cxx, cyy = lowres(ob_box[0]), lowres(ob_box[1] + ob_box[3] / 2)
        d.ellipse([cxx - r, cyy - r, cxx + r, cyy + r], outline=(255, 255, 255, 255), width=3)
    if struggle and ((beat in ("F2", "F4") and 1.3 <= lt < 1.45) or (beat == "F3" and 1.3 <= lt < 1.4)):
        bg = Image.blend(bg, Image.new("RGBA", bg.size, (255, 255, 255, 255)), 0.5)
    # fireworks
    if beat in ("F15", "F16") and (beat == "F16" or lt > 1.2):
        d = ImageDraw.Draw(bg)
        ft = (t - (TL["F15"][0] + 1.2))
        for i, (fxp, fyp, col) in enumerate([(120, 120, CYAN), (250, 90, (255, 240, 0)), (190, 160, WHITE)]):
            ph = (ft * 1.6 - i * 0.3) % 1.0
            rr = int(6 + 40 * ph); a = int(255 * (1 - ph))
            for k in range(8):
                ang = k * math.pi / 4
                d.rectangle([fxp + rr * math.cos(ang) - 2, fyp + rr * math.sin(ang) - 2, fxp + rr * math.cos(ang) + 2, fyp + rr * math.sin(ang) + 2], fill=col + (a,))
    if beat == "F7" or (beat == "F8"):
        grey = bg.convert("L").convert("RGBA")
        bg = Image.blend(bg, grey, 0.7 if beat == "F7" else 0.5)
    if beat == "F9" and 1.3 <= lt < 1.45:
        bg = Image.blend(bg, Image.new("RGBA", bg.size, (255, 255, 255, 255)), 0.6)
    # ---- upscale ----
    f = bg.convert("RGB").resize((W, H), Image.NEAREST).convert("RGBA")

    # ---- HUD (crisp) ----
    hearts = 3
    if t >= TL["F2"][0] + 1.3: hearts = 2
    if t >= TL["F4"][0] + 1.3: hearts = 1
    if t >= TL["F9"][0] + 1.5: hearts = 3
    blink = beat == "F7" and int(t * 4) % 2 == 0
    for i in range(3):
        hm = HEART_F if i < hearts else HEART_E
        if blink and i >= hearts: continue
        put(f, hm, 100 + i * 56, 318, "HUD-heart", t, record=(i == 0))
    lvl = plate_for("C02", size=CAP(44), backing="101528", alpha=255, border="101528", inset=12)
    put(f, lvl, 330, 318, "C02", t)
    slot_id = "C12" if t >= TL["F9"][0] + 1.2 else "C03"
    slot = plate_for(slot_id, size=CAP(40), backing="0239FF" if slot_id == "C12" else "3A3F55", alpha=255,
                     border="03FFF1" if slot_id == "C12" else "3A3F55", colour="FFFFFF", inset=12)
    put(f, slot, 1015 - slot.width // 2, 318, slot_id, t)
    score = 120 + int(t * 37) if t < TL["F16"][0] else 1240 + int(min(1, (t - TL["F16"][0]) / 0.8) * 8760)
    sc = plate_for("C22", lines=[f"{score:06d}"], size=CAP(36), backing="101528", alpha=255, border="101528", inset=10, face="bold")
    put(f, sc, 160, 396, "C22", t)   # repair R1: 3-px overlap with LEVEL 1 (disjoint gate)
    # name tag
    if beat != "F16":
        tag = plate_for("C01", size=CAP(40), backing="E39B2B", alpha=255, border="E39B2B", colour="101528", inset=10)
        put(f, tag, cx + knock, 835, "C01", t)   # repair R3: the tag no longer rides up with the jump (it collided with the label plate; disjoint gate)
    # obstacle label / card
    if struggle and lt >= 0.3:
        oid, lab_id, _ = OBST[("F2", "F3", "F4", "F5", "F6").index(beat)]
        s = DECK[lab_id]; lines = [s] if len(s) <= 15 else [s.rsplit(" ", 1)[0], s.rsplit(" ", 1)[1]]
        lab = plate_for(lab_id, lines=lines, size=CAP(60), backing="101528", alpha=255, border="E8334E", colour="FFFFFF")
        put(f, lab, 540, 688, lab_id, t)   # repair R1: 12-px gap to the name tag (disjoint gate)
    if beat == "F7":
        put(f, plate_for("C09", size=CAP(84), backing="101528", alpha=255, border="FFFFFF", face="bold"), 540, 700, "C09", t)
    if beat == "F8":
        full = DECK["C10"]; n = len(full)
        shown = full[:max(0, min(n, int((lt - 0.15) / 1.1 * n)))] if lt < 1.25 else full
        l1, l2 = "CHEAT CODE:", shown[12:] if len(shown) > 12 else ""
        lines = [l1, l2 + ("_" if (int(t * 6) % 2 == 0 and lt < 1.3) else "")] if l2 or lt >= 0.15 else [l1]
        lines = [x for x in lines if x]
        cid = "C10" if shown == full else "C10-typing"
        bar = plate_for(cid, lines=lines, size=CAP(72), backing="0239FF", alpha=255, border="03FFF1", face="bold")
        put(f, bar, 540, 665, cid, t)   # repair R4: the two-line cheat bar's bottom edge sat 8 px above the name tag (disjoint gate)
    if beat == "F9":
        # phone rises into hand
        u = min(1, lt / 0.9)
        ph = PHONE_BIG[0.0 if lt < 0.9 else (0.5 if lt < 1.3 else 1.0)]
        py = int(feet - 120 - 180 * u)
        if lt < 0.9:
            put(f, ph, cx + 200, py, "G-phone", t)          # repair round 1, D-1: 110 px further right (clear of the PG OWNER tag); box recorded for the disjoint check
        # icon burst on install
        if 0.9 <= lt:
            s = int(150 * min(1, (lt - 0.9) / 0.3))
            if s > 2: put(f, ICON.resize((s, s)), 540, 540, "G-icon", t)
        cid = "C11" if lt < 1.3 else "C12"
        pl = plate_for(cid, size=CAP(56) if cid == "C11" else CAP(64), backing="0239FF", alpha=255, border="03FFF1", face="bold")
        put(f, pl, 540, 700, cid, t)
    if power and lt >= 0.7:
        oid, _, card_id = OBST[("F10", "F11", "F12", "F13", "F14").index(beat)]
        card = plate_for(card_id, size=CAP(72), backing="0239FF", alpha=255, border="03FFF1", face="cond-bold")   # repair R1: bold C17 was 1031 px wide (safe-zone gate); all five cards condensed for one look
        put(f, card, 540, 640, card_id, t)
    if power and beat != "F10" and lt < 0.3:
        # previous card persists into this beat (>= 1.2 s hold)
        pid = OBST[("F10", "F11", "F12", "F13", "F14").index(beat) - 1][2]
        put(f, plate_for(pid, size=CAP(72), backing="0239FF", alpha=255, border="03FFF1", face="cond-bold"), 540, 640, pid, t)
    if beat == "F15" and lt < 0.3:
        put(f, plate_for("C17", size=CAP(72), backing="0239FF", alpha=255, border="03FFF1", face="cond-bold"), 540, 640, "C17", t)
    if beat == "F16":
        put(f, plate_for("C18", size=CAP(76), backing="0239FF", alpha=255, border="FFFFFF", face="cond-bold", inset=36), 540, 700, "C18", t)   # deck 96 cap -> 76 condensed to fit the safe width (recorded)
    return f.convert("RGB")


def contacts():
    ev = []
    for i, b in enumerate(("F2", "F3", "F4", "F5", "F6")):
        ev.append({"beat": b, "obstacle": OBST[i][0], "kind": "struggle_contact", "t": round(TL[b][0] + 1.3, 3)})
    for i, b in enumerate(("F10", "F11", "F12", "F13", "F14")):
        ev.append({"beat": b, "obstacle": OBST[i][0], "kind": "beam_hit_transform", "t": round(TL[b][0] + 0.7, 3), "card": OBST[i][2]})
    ev.append({"beat": "F15", "kind": "flag_capture", "t": round(TL["F15"][0] + 0.9, 3)})
    return ev


def main(out: Path, preview_only: bool = False):
    n = int(30.0 * FPS)
    json.dump({"beats": TL, "vo_start": VO_START, "vo_dur": VO, "fps": FPS, "frames": n}, open(OUT / "TIMELINE.json", "w"), indent=1)
    if preview_only:
        for fr in [0, 30, 60, 100, 200, 320, 350, 400, 470, 530, 560, 640, 700, 760, 790, 820, 860, 899]:
            render_frame(fr / FPS).save(OUT / f"preview_{fr:03d}.png")
        json.dump(_layout, open(OUT / "LAYOUT.preview.json", "w"))
        return
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-an", "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18", "-g", "15", "-bf", "2",
           "-r", str(FPS), "-movflags", "+faststart", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fr in range(n):
        p.stdin.write(render_frame(fr / FPS).tobytes())
        if fr % 150 == 0: print("frame", fr, flush=True)
    p.stdin.close(); p.wait()
    json.dump(_layout, open(OUT / "LAYOUT.json", "w"))
    json.dump(contacts(), open(OUT / "CONTACT_EVENTS.json", "w"), indent=1)
    reps = {k[0] + "|" + str(k[2] or "") + "|" + str(k[1]): v[1] for k, v in _plates.items()}
    json.dump(reps, open(OUT / "PLATE_GATES.json", "w"), indent=1, default=str)
    print("done", out, p.returncode)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument("--preview", action="store_true"); ap.add_argument("--out", default=str(OUT / "video_silent.mp4"))
    a = ap.parse_args(); main(Path(a.out), a.preview)
