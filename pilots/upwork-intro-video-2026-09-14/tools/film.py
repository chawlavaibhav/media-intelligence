#!/usr/bin/env python3
"""Segment renderer for the Upwork intro film. Deterministic; no model calls.

Renders the 'work' segments and cards as 1920x1080 24 fps MP4s from the copy deck + a plate + sealed
library clips, and burns word-identical supers onto presenter takes. Assembly (concat + audio) is in
assemble.py. All text goes through adcomp.text (hb-view) from COPY-DECK.yaml.
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).parent))
import adcomp as A  # noqa: E402

W, H, FPS = 1920, 1080, 24
INK, GROUND, GOLD = "#17201C", "#F5F1EA", "#B88A2E"
HERE = Path(__file__).resolve().parent.parent
DECK = yaml.safe_load((HERE / "plan" / "COPY-DECK.yaml").read_text())
USED_STRINGS: set[str] = set()          # every string rendered, for the D3 deck check


def deck_text(s: str, font: str, size: int, colour: str, alpha: int = 255) -> Image.Image:
    USED_STRINGS.add(s)
    return A.text(s, font, size, colour, alpha)


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def ground() -> Image.Image:
    return Image.new("RGBA", (W, H), A._hex_to_rgba(GROUND))


class Writer:
    """Pipe RGB frames into ffmpeg -> H.264 MP4 (silent)."""

    def __init__(self, out: Path, fps: int = FPS):
        out.parent.mkdir(parents=True, exist_ok=True)
        self.p = subprocess.Popen(
            ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
             "-r", str(fps), "-i", "-", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
             "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
        self.n = 0

    def add(self, im: Image.Image):
        self.p.stdin.write(im.convert("RGB").tobytes()); self.n += 1

    def close(self):
        self.p.stdin.close(); self.p.wait()
        return self.n


def super_strip(s: str, size: int = 40) -> Image.Image:
    """Super on a solid cream tab (never reverse type over picture, sk_ogx_0028)."""
    g = deck_text(s, "hn_medium", size, INK)
    pad_x, pad_y = int(size * 0.9), int(size * 0.55)
    im = Image.new("RGBA", (g.width + 2 * pad_x, g.height + 2 * pad_y), A._hex_to_rgba(GROUND, 242))
    A.paste(im, g, pad_x, pad_y)
    return im


def place_super(frame: Image.Image, s: str, alpha: float = 1.0, size: int = 40):
    strip = super_strip(s, size)
    if alpha < 1.0:
        a = strip.getchannel("A").point(lambda v: int(v * alpha)); strip.putalpha(a)
    A.paste(frame, strip, int(W * 0.05), H - strip.height - int(H * 0.07))


def place_demo(frame: Image.Image, colour: str = INK):
    """Small truth label, top-right, on every work frame (E1: demonstrations, invented brands)."""
    g = deck_text(DECK["work_supers"]["demo"], "hn", 26, colour, alpha=170)
    A.paste(frame, g, W - g.width - int(W * 0.05), int(H * 0.06))


def fit_h(im: Image.Image, h: int) -> Image.Image:
    return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)


def shadowed(im: Image.Image, blur: int = 28, off: int = 18, alpha: int = 90) -> Image.Image:
    """Drop a soft shadow behind an ad card so it sits on the ground."""
    pad = blur * 3
    canvas = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, alpha))
    canvas.alpha_composite(sh, (pad, pad + off))
    canvas = canvas.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(im, (pad, pad))
    return canvas


# --------------------------------------------------------------------------------- segments

def seg_brief(plate: Image.Image, out: Path, dur: float = 3.0):
    """Card: 'Your brief.' + product photo + the typed offer line."""
    w = Writer(out); n = int(dur * FPS)
    title = deck_text(DECK["cards"]["brief_title"], "didot", 150, INK)
    sub = deck_text(DECK["cards"]["brief_sub"], "hn", 44, INK, alpha=170)
    line = DECK["cards"]["brief_line"]
    photo = shadowed(A.fit_plate(plate, 420, 420, 0.35), blur=20, off=12, alpha=70)
    m = int(W * 0.09)
    for i in range(n):
        t = i / FPS
        f = ground()
        a = ease(t / 0.5)
        ttl = title.copy(); ttl.putalpha(ttl.getchannel("A").point(lambda v: int(v * a)))
        A.paste(f, ttl, m, int(H * 0.18))
        A.paste(f, sub, m, int(H * 0.18) + title.height + 24)
        pa = ease((t - 0.5) / 0.6)
        if pa > 0:
            ph = photo.copy(); ph.putalpha(ph.getchannel("A").point(lambda v: int(v * pa)))
            A.paste(f, ph, m - 60, int(H * 0.50))
        # typed line: reveal by character count
        k = int(len(line) * ease((t - 1.0) / 1.4))
        if k > 0:
            g = deck_text(line[:k], "hn_medium", 44, INK)
            ly = int(H * 0.50) + 170
            A.paste(f, g, m + 440, ly)
            if k < len(line) and int(t * 3) % 2 == 0:
                d = ImageDraw.Draw(f); x = m + 440 + g.width + 6
                d.rectangle([x, ly, x + 3, ly + g.height], fill=A._hex_to_rgba(GOLD))
        place_demo(f)
        w.add(f)
    USED_STRINGS.add(line)
    return w.close()


BUILD_STEPS = [0.15, 0.30, 0.45, 0.60, 0.75, 0.90, 1.0]


def seg_build(plate: Image.Image, copy: A.Copy, brand: A.Brand, out: Path, dur: float = 6.0):
    """The ad assembles in hierarchy order on a slow push; each element snaps in at a step time."""
    w = Writer(out); n = int(dur * FPS)
    step_t = [0.3 + i * (dur - 1.4) / (len(BUILD_STEPS) - 1) for i in range(len(BUILD_STEPS))]
    ad_h = int(H * 0.86)
    cache = {}
    for i in range(n):
        t = i / FPS
        f = ground()
        cur = 0.0
        for st, b in zip(step_t, BUILD_STEPS):
            if t >= st:
                cur = b
        if cur not in cache:
            cache[cur] = A.ledge(plate, copy, brand, "4x5", build=cur)
        ad = cache[cur]
        scale = 1.0 + 0.03 * (t / dur)                      # slow push
        card = fit_h(ad, int(ad_h * scale))
        card = shadowed(card)
        A.paste(f, card, (W - card.width) // 2, (H - card.height) // 2)
        place_demo(f)
        w.add(f)
    snaps = [round(s, 3) for s in step_t]
    return w.close(), snaps


def seg_sizes(plate, copy, brand, out: Path, dur: float = 3.0):
    """4:5 -> 4:5 / 1:1 / 9:16 / WhatsApp in a row; super 'One layout. Four sizes.'"""
    w = Writer(out); n = int(dur * FPS)
    ads = {fmt: A.ledge(plate, copy, brand, fmt) for fmt in ("4x5", "1x1", "9x16", "wa")}
    gap = 36
    row_h = int(H * 0.56)
    while True:
        raw = [fit_h(ads[f], row_h if f != "9x16" else int(row_h * 1.15)) for f in ("9x16", "4x5", "1x1", "wa")]
        cards = [shadowed(r, blur=22, off=14, alpha=80) for r in raw]
        if sum(c.width for c in cards) + gap * 3 <= int(W * 0.94):
            break
        row_h -= 8
    total = sum(c.width for c in cards) + gap * (len(cards) - 1)
    x0 = (W - total) // 2
    for i in range(n):
        t = i / FPS
        f = ground()
        x = x0
        for j, c in enumerate(cards):
            a = ease((t - 0.15 * j) / 0.5)
            if a > 0:
                cc = c.copy(); cc.putalpha(cc.getchannel("A").point(lambda v: int(v * a)))
                dy = int((1 - a) * 40)
                A.paste(f, cc, x, (H - c.height) // 2 - 30 + dy)
            x += c.width + gap
        if t > 0.9:
            place_super(f, DECK["work_supers"]["sizes"], ease((t - 0.9) / 0.3))
        place_demo(f)
        w.add(f)
    return w.close()


def seg_hooks(plate, brand, out: Path, dur: float = 4.0):
    """2x3 grid of six headline variants; the last tile flips to Hindi. Super 'Six hooks. Then Hindi.'"""
    w = Writer(out); n = int(dur * FPS)
    en = DECK["aarohi_en"]; hi = DECK["aarohi_hi"]
    tiles = []
    for hl in DECK["aarohi_hooks"]:
        c = A.Copy("en", hl, en["pill"], en["product"], en["price"], en["was"], en["code"], en["cta"], en["legal"])
        tiles.append(A.ledge(plate, c, brand, "4x5"))
        for s in hl: USED_STRINGS.add(s)
    hi_copy = A.Copy("hi", hi["headline"], hi["pill"], hi["product"], hi["price"], hi["was"], hi["code"], hi["cta"], hi["legal"])
    hi_tile = A.ledge(plate, hi_copy, brand, "4x5")
    for s in [*hi["headline"], hi["pill"], hi["product"], hi["code"], hi["cta"], hi["legal"], en["pill"], en["product"], en["code"], en["cta"], en["legal"]]:
        USED_STRINGS.add(s)
    th = int(H * 0.31)
    small = [shadowed(fit_h(tl, th), blur=16, off=10, alpha=70) for tl in tiles]
    small_hi = shadowed(fit_h(hi_tile, th), blur=16, off=10, alpha=70)
    gap = 22
    cw, ch = small[0].width, small[0].height
    gx0 = (W - (3 * cw + 2 * gap)) // 2
    gy0 = int(H * 0.03)
    flip_t = dur - 1.4
    for i in range(n):
        t = i / FPS
        f = ground()
        for j in range(6):
            a = ease((t - 0.18 * j) / 0.45)
            if a <= 0:
                continue
            tile = small[j]
            if j == 5 and t >= flip_t:
                k = ease((t - flip_t) / 0.45)
                tile = Image.blend(small[j], small_hi, k) if k < 1 else small_hi
            tt = tile.copy(); tt.putalpha(tt.getchannel("A").point(lambda v: int(v * a)))
            A.paste(f, tt, gx0 + (j % 3) * (cw + gap), gy0 + (j // 3) * (ch + gap))
        if t > 1.3:
            place_super(f, DECK["work_supers"]["hooks"], ease((t - 1.3) / 0.3))
        place_demo(f)
        w.add(f)
    return w.close(), flip_t


def seg_check(plate, brand, out: Path, dur: float = 3.0):
    """Close on the price line, composed large on the brand panel: the wrong digit is underlined in gold, corrected,
    then a tick. Super 'Exactly as you wrote it.' (the close-up is the proof of care, sk_sut_alc_0020)"""
    w = Writer(out); n = int(dur * FPS)
    en = DECK["aarohi_en"]; cb = DECK["check_beat"]
    for s_ in (cb["wrong_price"], cb["right_price"], en["product"], en["was"], en["code"]): USED_STRINGS.add(s_)
    sub = 66
    m = int(W * 0.09)
    prod = A.text(en["product"], "hn", sub, brand.cream)
    wrong = A.text(cb["wrong_price"], "hn_medium", sub, brand.accent)
    right = A.text(cb["right_price"], "hn_medium", sub, brand.accent)
    was = A.strike(A.text(en["was"], "hn", sub, brand.cream, alpha=170), brand.cream, 6)
    code = A.text(en["code"], "hn", sub, brand.cream, alpha=200)
    hl_lines = [A.text(l, "didot", 150, brand.cream) for l in en["headline"]]
    y1 = int(H * 0.16); y2 = y1 + int(150 * 1.12)
    y_sub = y2 + 150 + int(150 * 0.45)
    fix_t = dur * 0.55
    for i in range(n):
        t = i / FPS
        f = Image.new("RGBA", (W, H), A._hex_to_rgba(brand.primary))
        A.paste(f, hl_lines[0], m, y1); A.paste(f, hl_lines[1], m, y2)
        x = m
        A.paste(f, prod, x, y_sub); x += prod.width + int(sub * 0.9)
        price = right if t >= fix_t else wrong
        px = x
        A.paste(f, price, x, y_sub); x += price.width + int(sub * 0.7)
        A.paste(f, was, x, y_sub); x += was.width + int(sub * 0.9)
        A.paste(f, code, x, y_sub)
        d = ImageDraw.Draw(f)
        uy = y_sub + price.height + 12
        if 0.5 <= t < fix_t:
            a = ease((t - 0.5) / 0.3)
            d.rectangle([px, uy, px + int(price.width * a), uy + 8], fill=A._hex_to_rgba(brand.accent))
        if t >= fix_t:
            k = ease((t - fix_t) / 0.35)
            x0, y0 = x + code.width + int(sub * 0.6), y_sub + int(sub * 0.1)
            L = int(70 * k)
            d.line([(x0, y0 + 35), (x0 + min(L, 28), y0 + 35 + min(L, 28))], fill=A._hex_to_rgba(brand.accent), width=12)
            if L > 28:
                d.line([(x0 + 28, y0 + 63), (x0 + 28 + (L - 28) * 1.7, y0 + 63 - (L - 28) * 1.7)], fill=A._hex_to_rgba(brand.accent), width=12)
        if t > 0.2:
            place_super(f, DECK["work_supers"]["check"], ease((t - 0.2) / 0.3))
        place_demo(f, brand.cream)
        w.add(f)
    return w.close(), fix_t


def phone_frame(inner_w: int, inner_h: int, bezel: int = 22, radius: int = 64) -> Image.Image:
    im = Image.new("RGBA", (inner_w + 2 * bezel, inner_h + 2 * bezel), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=radius, fill=A._hex_to_rgba("#14181A"))
    return im


def seg_phone(clip: Path, out: Path, start: float, dur: float, super_text: str | None, super_in: float = 0.0, super_out: float | None = None):
    """A sealed vertical clip inside a phone frame on the cream ground, via ffmpeg (no Python frame loop).
    The clip is cover-scaled into the phone's inner 9:16 area; text-bearing clips are 9:16 already so nothing is cut."""
    inner_h = int(H * 0.86); inner_w = int(inner_h * 9 / 16)
    frame = phone_frame(inner_w, inner_h)
    bezel = 22
    fx, fy = (W - frame.width) // 2, (H - frame.height) // 2
    overlay = ground()
    A.paste(overlay, frame, fx, fy)
    # cut a transparent window where the clip goes
    win = Image.new("RGBA", (inner_w, inner_h), (0, 0, 0, 0))
    mask = Image.new("L", (inner_w, inner_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, inner_w - 1, inner_h - 1], radius=44, fill=255)
    overlay.paste(win, (fx + bezel, fy + bezel), mask)
    if super_text:
        place_super(overlay, super_text)
    place_demo(overlay)
    ov = out.with_suffix(".overlay.png"); overlay.save(ov)
    ground_png = out.with_suffix(".ground.png"); ground().convert("RGB").save(ground_png)
    vf = (f"[1:v]trim=start={start}:duration={dur},setpts=PTS-STARTPTS,scale={inner_w}:{inner_h}:force_original_aspect_ratio=increase,"
          f"crop={inner_w}:{inner_h},format=rgba[clip];"
          f"[0:v][clip]overlay={fx + bezel}:{fy + bezel}[a];[a][2:v]overlay=0:0,format=yuv420p[v]")
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-t", str(dur), "-i", str(ground_png),
           "-i", str(clip), "-loop", "1", "-framerate", str(FPS), "-t", str(dur), "-i", str(ov),
           "-filter_complex", vf, "-map", "[v]", "-an", "-r", str(FPS), "-c:v", "libx264", "-crf", "17", "-preset", "medium",
           "-t", str(dur), str(out)]
    subprocess.run(cmd, check=True)
    if super_text: USED_STRINGS.add(super_text)


def seg_endcard(out: Path, dur: float = 5.5):
    """End on the package: CTA is the boss (Karl §7), then the standard line, the wordmark once, the window in small print."""
    w = Writer(out); n = int(dur * FPS)
    e = DECK["end_card"]
    cta = deck_text(e["cta"], "didot", 132, INK)
    std = deck_text(e["standard_line"], "hn_medium", 48, INK)
    mark = deck_text(e["wordmark"], "didot", 64, INK, alpha=210)
    small = deck_text(e["small"], "hn", 30, INK, alpha=160)
    m = int(W * 0.09)
    fade_start = dur - 0.6
    items = [(cta, int(H * 0.20)), (std, int(H * 0.20) + cta.height + 40), (mark, int(H * 0.20) + cta.height + 40 + std.height + 90), (small, H - int(H * 0.11))]
    for i in range(n):
        t = i / FPS
        f = ground()
        for j, (g, y) in enumerate(items):
            a = ease((t - 0.2 * j) / 0.5)
            if a > 0:
                gg = g.copy(); gg.putalpha(gg.getchannel("A").point(lambda v: int(v * a)))
                A.paste(f, gg, m, y)
        if t > fade_start:
            k = (t - fade_start) / (dur - fade_start)
            f = Image.blend(f, ground(), k)
        w.add(f)
    return w.close()


def burn_supers(take: Path, out: Path, cues: list, insert: tuple | None = None, trim_s: float | None = None):
    """Burn word-identical supers onto a presenter take. cues = [(t_in, t_out, text) | (t_in, t_out, text, qualifier)].
    insert=(png_path, until_s) shows a still card instead of the picture until `until_s` while the take's audio leads
    (J-cut). trim_s cuts the take. Keeps the take's audio."""
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(take)], capture_output=True, text=True)
    dur = float(probe.stdout.strip())
    if trim_s:
        dur = min(dur, trim_s)
    n = int(round(dur * FPS))
    dec = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", str(take), "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
                            "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    tmp = out.with_suffix(".video.mp4")
    w = Writer(tmp)
    card = Image.open(insert[0]).convert("RGBA").resize((W, H)) if insert else None
    cues = sorted(cues, key=lambda c: c[0])
    cues = [(c[0], min(c[1], cues[k + 1][0] - 0.08) if k + 1 < len(cues) else c[1], *c[2:]) for k, c in enumerate(cues)]
    i = 0
    while i < n:
        buf = dec.stdout.read(W * H * 3)
        if len(buf) < W * H * 3:
            break
        t = i / FPS
        if card is not None and t < insert[1]:
            f = card.copy()
        else:
            f = Image.frombytes("RGB", (W, H), buf).convert("RGBA")
        for c in cues:
            ti, to, s_ = c[0], c[1], c[2]
            if ti <= t < to:
                a = min(ease((t - ti) / 0.2), ease((to - t) / 0.2))
                if len(c) > 3:
                    place_super_2(f, s_, c[3], a)
                else:
                    place_super(f, s_, a)
        w.add(f); i += 1
    w.close(); dec.stdout.close(); dec.kill(); dec.wait()
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(tmp), "-i", str(take), "-map", "0:v", "-map", "1:a?", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-t", f"{dur:.3f}", str(out)], check=True)
    tmp.unlink(missing_ok=True)
    return dur


def place_super_2(frame: Image.Image, s: str, qualifier: str, alpha: float = 1.0):
    """Two-line strip: the word-identical super plus a smaller qualifier line on the same frame (A2 rule)."""
    g1 = deck_text(s, "hn_medium", 40, INK); g2 = deck_text(qualifier, "hn", 30, INK, alpha=200)
    pad_x, pad_y = 36, 22
    wdt = max(g1.width, g2.width) + 2 * pad_x
    strip = Image.new("RGBA", (wdt, g1.height + g2.height + 2 * pad_y + 12), A._hex_to_rgba(GROUND, 242))
    A.paste(strip, g1, pad_x, pad_y); A.paste(strip, g2, pad_x, pad_y + g1.height + 12)
    if alpha < 1.0:
        strip.putalpha(strip.getchannel("A").point(lambda v: int(v * alpha)))
    A.paste(frame, strip, int(W * 0.05), H - strip.height - int(H * 0.07))


def deck_strings() -> set[str]:
    out = set()
    def walk(o):
        if isinstance(o, str): out.add(o)
        elif isinstance(o, list): [walk(x) for x in o]
        elif isinstance(o, dict): [walk(v) for v in o.values()]
    walk(DECK)
    return out


def d3_check() -> list[str]:
    """Every rendered string must be in the deck (or a prefix of a deck string, for the typed line)."""
    deck = deck_strings()
    bad = []
    for s in USED_STRINGS:
        if s in deck or any(d.startswith(s) for d in deck):
            continue
        bad.append(s)
    return bad
