#!/usr/bin/env python3
"""v5 showcase segments with ONE caption rule: every showcase piece carries the same small label (bottom-right,
format · size · language) for its whole duration, and each benefit group carries one tab (bottom-left, same style
as the speech captions). Nothing else on the frame. Reuses film.py primitives."""
from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

import adcomp as A
import film as F
from film import W, H, FPS, INK, GROUND, Writer, ease, ground, place_super, fit_h, shadowed, deck_text

DECK = F.DECK


def place_label(frame: Image.Image, s: str, alpha: float = 1.0):
    g = deck_text(s, "hn", 28, INK, alpha=int(200 * alpha))
    A.paste(frame, g, W - g.width - int(W * 0.05), H - g.height - int(H * 0.085))


def dress(f: Image.Image, t: float, tab: str, label: str, tab_in: float):
    """Apply the caption rule to a showcase frame."""
    a = ease((t - tab_in) / 0.3) if tab_in >= 0 else 1.0
    if a > 0:
        place_super(f, tab, a)
    place_label(f, label)


def card_frame(im: Image.Image, h_frac: float, push: float = 1.0) -> Image.Image:
    return shadowed(fit_h(im, int(H * h_frac * push)))


# --------------------------------------------------------------------------------- statics

def seg_build(plate, copy, brand, out: Path, dur: float, tab: str, label: str, tab_in: float = 0.3):
    w = Writer(out); n = int(dur * FPS)
    steps = F.BUILD_STEPS
    step_t = [0.25 + i * (dur - 1.0) / (len(steps) - 1) for i in range(len(steps))]
    cache = {}
    for i in range(n):
        t = i / FPS; f = ground(); cur = 0.0
        for st, b in zip(step_t, steps):
            if t >= st: cur = b
        if cur not in cache: cache[cur] = A.ledge(plate, copy, brand, "4x5", build=cur)
        card = card_frame(cache[cur], 0.84, 1.0 + 0.03 * t / dur)
        A.paste(f, card, (W - card.width) // 2, (H - card.height) // 2)
        dress(f, t, tab, label, tab_in); w.add(f)
    return w.close(), [round(s, 3) for s in step_t]


def seg_sizes(plate, copy, brand, out: Path, dur: float, tab: str, label: str, tab_in: float = -1):
    w = Writer(out); n = int(dur * FPS)
    ads = {fmt: A.ledge(plate, copy, brand, fmt) for fmt in ("4x5", "1x1", "9x16", "wa")}
    gap, row_h = 36, int(H * 0.62)
    while True:
        raw = [fit_h(ads[f], row_h if f != "9x16" else int(row_h * 1.15)) for f in ("9x16", "4x5", "1x1", "wa")]
        cards = [shadowed(r, blur=14, off=10, alpha=80) for r in raw]
        if sum(c.width for c in cards) + gap * 3 <= int(W * 0.92): break
        row_h -= 8
    total = sum(c.width for c in cards) + gap * 3; x0 = (W - total) // 2
    for i in range(n):
        t = i / FPS; f = ground(); x = x0
        for j, c in enumerate(cards):
            a = ease((t - 0.12 * j) / 0.45)
            if a > 0:
                cc = c.copy(); cc.putalpha(cc.getchannel("A").point(lambda v: int(v * a)))
                A.paste(f, cc, x, (H - c.height) // 2 - 30 + int((1 - a) * 40))
            x += c.width + gap
        dress(f, t, tab, label, tab_in); w.add(f)
    return w.close()


def seg_hooks(plate, brand, out: Path, dur: float, tab: str, label: str, tab_in: float = 0.2):
    w = Writer(out); n = int(dur * FPS)
    en = DECK["aarohi_en"]; hi = DECK["aarohi_hi"]
    tiles = []
    for hl in DECK["aarohi_hooks"]:
        c = A.Copy("en", hl, en["pill"], en["product"], en["price"], en["was"], en["code"], en["cta"], en["legal"])
        tiles.append(A.ledge(plate, c, brand, "4x5"))
        for s_ in hl: F.USED_STRINGS.add(s_)
    hi_copy = A.Copy("hi", hi["headline"], hi["pill"], hi["product"], hi["price"], hi["was"], hi["code"], hi["cta"], hi["legal"])
    hi_tile = A.ledge(plate, hi_copy, brand, "4x5")
    for s_ in [*hi["headline"], hi["pill"], hi["product"], hi["code"], hi["cta"], hi["legal"]]: F.USED_STRINGS.add(s_)
    th = int(H * 0.33)
    small = [shadowed(fit_h(tl, th), blur=12, off=8, alpha=70) for tl in tiles]
    small_hi = shadowed(fit_h(hi_tile, th), blur=12, off=8, alpha=70)
    gap = 22; cw, ch = small[0].width, small[0].height
    gx0 = (W - (3 * cw + 2 * gap)) // 2; gy0 = int(H * 0.04)
    flip_t = dur - 1.2
    for i in range(n):
        t = i / FPS; f = ground()
        for j in range(6):
            a = ease((t - 0.15 * j) / 0.4)
            if a <= 0: continue
            tile = small[j]
            if j == 5 and t >= flip_t:
                k = ease((t - flip_t) / 0.4); tile = Image.blend(small[j], small_hi, k) if k < 1 else small_hi
            tt = tile.copy(); tt.putalpha(tt.getchannel("A").point(lambda v: int(v * a)))
            A.paste(f, tt, gx0 + (j % 3) * (cw + gap), gy0 + (j // 3) * (ch + gap))
        dress(f, t, tab, label, tab_in); w.add(f)
    return w.close(), flip_t


def seg_check(brand, out: Path, dur: float, tab: str, label: str, tab_in: float = 0.2):
    w = Writer(out); n = int(dur * FPS)
    en = DECK["aarohi_en"]; cb = DECK["check_beat"]
    for s_ in (cb["wrong_price"], cb["right_price"], en["product"], en["was"], en["code"]): F.USED_STRINGS.add(s_)
    sub = 66; m = int(W * 0.09)
    prod = A.text(en["product"], "hn", sub, brand.cream)
    wrong = A.text(cb["wrong_price"], "hn_medium", sub, brand.accent); right = A.text(cb["right_price"], "hn_medium", sub, brand.accent)
    was = A.strike(A.text(en["was"], "hn", sub, brand.cream, alpha=170), brand.cream, 6)
    code = A.text(en["code"], "hn", sub, brand.cream, alpha=200)
    hl_lines = [A.text(l, "didot", 150, brand.cream) for l in en["headline"]]
    y1 = int(H * 0.14); y2 = y1 + int(150 * 1.12); y_sub = y2 + 150 + int(150 * 0.45)
    fix_t = dur * 0.55
    for i in range(n):
        t = i / FPS
        f = Image.new("RGBA", (W, H), A._hex_to_rgba(brand.primary))
        A.paste(f, hl_lines[0], m, y1); A.paste(f, hl_lines[1], m, y2)
        x = m; A.paste(f, prod, x, y_sub); x += prod.width + int(sub * 0.9)
        price = right if t >= fix_t else wrong; px = x
        A.paste(f, price, x, y_sub); x += price.width + int(sub * 0.7)
        A.paste(f, was, x, y_sub); x += was.width + int(sub * 0.9)
        A.paste(f, code, x, y_sub)
        d = ImageDraw.Draw(f); uy = y_sub + price.height + 12
        if 0.5 <= t < fix_t:
            a = ease((t - 0.5) / 0.3); d.rectangle([px, uy, px + int(price.width * a), uy + 8], fill=A._hex_to_rgba(brand.accent))
        if t >= fix_t:
            k = ease((t - fix_t) / 0.35); x0, y0 = x + code.width + int(sub * 0.6), y_sub + int(sub * 0.1); L = int(70 * k)
            d.line([(x0, y0 + 35), (x0 + min(L, 28), y0 + 35 + min(L, 28))], fill=A._hex_to_rgba(brand.accent), width=12)
            if L > 28: d.line([(x0 + 28, y0 + 63), (x0 + 28 + (L - 28) * 1.7, y0 + 63 - (L - 28) * 1.7)], fill=A._hex_to_rgba(brand.accent), width=12)
        # labels on the dark panel: cream ink
        a = ease((t - tab_in) / 0.3)
        if a > 0: place_super(f, tab, a)
        g = deck_text(label, "hn", 28, brand.cream, alpha=200); A.paste(f, g, W - g.width - int(W * 0.05), H - g.height - int(H * 0.085))
        w.add(f)
    return w.close(), fix_t


def seg_still(img: Image.Image, out: Path, dur: float, tab: str, label: str, tab_in: float = -1, h_frac: float = 0.84):
    """A still in a card with a slow push (Ken Burns), same caption rule."""
    w = Writer(out); n = int(dur * FPS)
    for i in range(n):
        t = i / FPS; f = ground()
        a = ease(t / 0.35)
        card = card_frame(img, h_frac, 1.0 + 0.035 * t / dur)
        if a < 1: card.putalpha(card.getchannel("A").point(lambda v: int(v * a)))
        A.paste(f, card, (W - card.width) // 2, (H - card.height) // 2)
        dress(f, t, tab, label, tab_in); w.add(f)
    return w.close()


def seg_clip_card(clip: Path, out: Path, start: float, dur: float, tab: str, label: str, tab_in: float = -1, aspect: float = 16 / 9, h_frac: float = 0.84):
    """A clip inside a rounded card (9:16 phone or 16:9 wide) on the cream ground, via ffmpeg; caption rule burned from a PNG."""
    inner_h = int(H * h_frac); inner_w = int(inner_h * aspect)
    if inner_w > int(W * 0.86): inner_w = int(W * 0.86); inner_h = int(inner_w / aspect)
    bezel = 22 if aspect < 1 else 0
    radius = 64 if aspect < 1 else 28
    fx, fy = (W - inner_w) // 2 - bezel, (H - inner_h) // 2 - bezel
    overlay = ground()
    if bezel:
        A.paste(overlay, F.phone_frame(inner_w, inner_h, bezel, radius), fx, fy)
    else:
        sh = shadowed(Image.new("RGBA", (inner_w, inner_h), (0, 0, 0, 255)), blur=24, off=16, alpha=80)
        A.paste(overlay, sh, fx - 72, fy - 72)
    mask = Image.new("L", (inner_w, inner_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, inner_w - 1, inner_h - 1], radius=radius if bezel else 20, fill=255)
    overlay.paste(Image.new("RGBA", (inner_w, inner_h), (0, 0, 0, 0)), (fx + bezel, fy + bezel), mask)
    dress(overlay, 9.0, tab, label, -1)      # tab shown steady for the whole clip (fade handled by tab_in<0)
    ov = out.with_suffix(".overlay.png"); overlay.save(ov)
    gp = out.with_suffix(".ground.png"); ground().convert("RGB").save(gp)
    vf = (f"[1:v]trim=start={start}:duration={dur},setpts=PTS-STARTPTS,scale={inner_w}:{inner_h}:force_original_aspect_ratio=increase,"
          f"crop={inner_w}:{inner_h},format=rgba[clip];[0:v][clip]overlay={fx + bezel}:{fy + bezel}[a];[a][2:v]overlay=0:0,format=yuv420p[v]")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-t", str(dur), "-i", str(gp),
                    "-i", str(clip), "-loop", "1", "-framerate", str(FPS), "-t", str(dur), "-i", str(ov),
                    "-filter_complex", vf, "-map", "[v]", "-an", "-r", str(FPS), "-c:v", "libx264", "-crf", "17", "-preset", "medium",
                    "-t", str(dur), str(out)], check=True)
    F.USED_STRINGS.update([tab, label])
