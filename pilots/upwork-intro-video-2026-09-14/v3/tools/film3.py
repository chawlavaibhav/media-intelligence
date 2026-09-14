#!/usr/bin/env python3
"""UPWORK-INTRO-V3 renderer: the frozen timeline (§16) as deterministic 1920x1080 30 fps segments. No model calls.
Every string comes from plan/COPY-DECK-v3.yaml (deck check), timestamps from gen/CLOCK.json (mechanical).
usage: film3.py <out_dir>"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).parent))
import compose as Cp  # noqa: E402
from compose import A, DECK, T, tracked, cover, alpha_mul  # noqa: E402

W, H, FPS = 1920, 1080, 30
V3 = Cp.V3
GEN = V3 / "gen"
GROUND, INK, ACCENT = Cp.GROUND, Cp.INK, Cp.ACCENT
WR = DECK["wrapper"]
DYN: set[str] = set()          # dynamic strings (timestamps, counters) — allowed by the deck check by construction


def ease(t):
    t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3


def ease_io(t):
    t = max(0.0, min(1.0, t)); return 0.5 - 0.5 * math.cos(math.pi * t)


def ground():
    return Image.new("RGBA", (W, H), A._hex_to_rgba(GROUND))


class Writer:
    def __init__(self, out: Path):
        out.parent.mkdir(parents=True, exist_ok=True)
        self.p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                                   "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
        self.n = 0

    def add(self, im):
        self.p.stdin.write(im.convert("RGB").tobytes()); self.n += 1

    def close(self):
        self.p.stdin.close(); self.p.wait(); return self.n / FPS


class Clip:
    """Stream a source clip at 30 fps, cover-fitted to (w,h) with anchor (ax,ay) — one frame in memory at a time."""

    def __init__(self, src: Path, w: int, h: int, ax=0.5, ay=0.5, start=0.0):
        self.w, self.h = w, h
        vf = f"fps={FPS},scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}:(iw-{w})*{ax}:(ih-{h})*{ay}"
        self.p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-ss", f"{start:.3f}", "-i", str(src), "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                                  stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        self.last = None

    def read(self):
        buf = self.p.stdout.read(self.w * self.h * 3)
        if len(buf) < self.w * self.h * 3:
            return self.last
        self.last = Image.frombytes("RGB", (self.w, self.h), buf).convert("RGBA"); return self.last

    def close(self):
        self.p.stdout.close(); self.p.kill(); self.p.wait()


def shadowed(im, blur=26, off=16, alpha=80):
    pad = blur * 3
    c = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    c.alpha_composite(Image.new("RGBA", im.size, (0, 0, 0, alpha)), (pad, pad + off))
    c = c.filter(ImageFilter.GaussianBlur(blur)); c.alpha_composite(im, (pad, pad)); return c, pad


def arrow(size: int, colour=INK, alpha=255) -> Image.Image:
    """A drawn arrow (Helvetica Neue has no U+2192 glyph via hb-view)."""
    w, h = int(size * 1.3), int(size * 0.9); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    y = h // 2; lw = max(2, size // 12); col = A._hex_to_rgba(colour, alpha)
    d.line([(2, y), (w - 3, y)], fill=col, width=lw); d.line([(w - int(size * 0.42), y - int(size * 0.36)), (w - 3, y), (w - int(size * 0.42), y + int(size * 0.36))], fill=col, width=lw)
    return im


def label(s: str, size=28, colour=INK, alpha=255):
    Cp.USED.add(s)
    parts = s.split("→")
    if len(parts) == 1:
        return tracked(s, "hn_medium", size, colour, 0.22, alpha)
    glyphs = []
    for i, part in enumerate(parts):
        if i:
            glyphs.append(arrow(size, colour, alpha))
        glyphs.append(tracked(part.strip(), "hn_medium", size, colour, 0.22, alpha))
    gap = int(size * 0.5); w = sum(g.width for g in glyphs) + gap * (len(glyphs) - 1); h = max(g.height for g in glyphs)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); x = 0
    for g in glyphs:
        A.paste(im, g, x, (h - g.height) // 2); x += g.width + gap
    return im


def place_label(f, s, x=None, y=None, a=1.0, size=28):
    g = label(s, size); g = alpha_mul(g, a)
    A.paste(f, g, int(W * 0.05) if x is None else x, H - g.height - int(H * 0.075) if y is None else y)


def place_disclosure(f, s, a=1.0):
    g = label(s, 22, INK, 150); g = alpha_mul(g, a)
    A.paste(f, g, W - g.width - int(W * 0.05), int(H * 0.06))


def fit_h(im, h):
    return im.resize((int(im.width * h / im.height + 0.5), h), Image.LANCZOS)


def ist(s: str) -> datetime:
    return datetime.fromisoformat(s)


def dyn(s: str):
    DYN.add(s); return s


# ------------------------------------------------------------------------------------------------- assets
CLOCK = json.loads((GEN / "CLOCK.json").read_text())
ST = GEN / "stills"; STAT = GEN / "statics"; VID = GEN / "video"
A0 = Image.open(ST / "a0-accepted.png").convert("RGBA")
A1 = Image.open(ST / "a1-accepted.png").convert("RGBA")
A2 = Image.open(ST / "a2-accepted.png").convert("RGBA")
A3 = Image.open(ST / "a3-accepted.png").convert("RGBA")
B0 = Image.open(ST / "brewa0-accepted.png").convert("RGBA")
B2 = Image.open(ST / "b2-accepted.png").convert("RGBA")
B3 = Image.open(ST / "b3-accepted.png").convert("RGBA")
KORA = Image.open(ST / "kora-accepted.png").convert("RGBA")
DH_REJ = Image.open(ST / "dhaba-r1.png").convert("RGBA")
DH = Image.open(ST / "dhaba-accepted.png").convert("RGBA")
HOOKS = DECK["aarohi"]["hooks"]; KHOOKS = DECK["kora"]["hooks"]

A1_ANCHOR = (0.62, 0.5)   # bottle sits right of centre in the hero still
A2_ANCHOR = (0.5, 0.45)
A3_ANCHOR = (0.5, 0.5)


def statics():
    """Render every deliverable static once (deterministic), return a dict of PIL images."""
    out = {}
    out["master"] = {fmt: Cp.aarohi(A1, fmt, anchor=A1_ANCHOR) for fmt in ("4x5", "1x1", "9x16", "wa")}
    out["hooks"] = [Cp.aarohi(A1, "4x5", variant=h, anchor=A1_ANCHOR) for h in HOOKS]
    out["hindi"] = Cp.aarohi(A1, "4x5", hindi=True, anchor=A1_ANCHOR)
    out["a2_hook"] = Cp.aarohi(A2, "4x5", variant=HOOKS[0], anchor=A2_ANCHOR)
    out["a3_hook"] = Cp.aarohi(A3, "4x5", variant=HOOKS[2], anchor=A3_ANCHOR)
    out["kora_4x5"] = Cp.kora(KORA, "4x5", KHOOKS[0], anchor=(0.42, 0.5))
    out["kora_16x9"] = [Cp.kora(KORA, "16x9", h) for h in KHOOKS]
    out["dhaba_4x5"] = Cp.dhaba(DH, "4x5")
    out["dhaba_wa"] = Cp.dhaba(DH, "wa", anchor=(0.5, 0.45))
    return out


# ------------------------------------------------------------------------------------------------- segments

def seg_brief(w: Writer, dur=1.2):
    n = int(dur * FPS); m = int(W * 0.08)
    photo, pad = shadowed(fit_h(A0, int(H * 0.70)), blur=22, off=14, alpha=70)
    t_brief = ist(CLOCK["brief_complete_ist"]).strftime(DECK["intake"]["brief_ts_fmt"])
    title = label(WR["brief_title"], 30)
    l1 = label(WR["brief_photo_label"], 26, INK, 170); l2 = label(WR["brief_offer_label"], 26, INK, 170)
    offer = T(WR["brief_offer_line"], "hn_medium", 46, INK)
    ts = T(dyn(f'{WR["brief_ts_label"]} · {t_brief}'), "hn", 30, INK, 170)
    for i in range(n):
        t = i / FPS; f = ground()
        A.paste(f, alpha_mul(photo, ease(t / 0.35)), m - pad, int(H * 0.15) - pad)
        x = int(W * 0.47); y = int(H * 0.22)
        A.paste(f, title, x, y); y += title.height + int(H * 0.06)
        a = ease((t - 0.15) / 0.35)
        A.paste(f, alpha_mul(l1, a), x, y); y += l1.height + 14
        A.paste(f, alpha_mul(l2, a), x, y); y += l2.height + 26
        A.paste(f, alpha_mul(offer, ease((t - 0.3) / 0.4)), x, y + int((1 - ease((t - 0.3) / 0.4)) * 20)); y += offer.height + int(H * 0.06)
        A.paste(f, alpha_mul(ts, ease((t - 0.5) / 0.4)), x, y)
        place_disclosure(f, WR["disclosure_one"])
        w.add(f)


def seg_hero(w: Writer, dur=2.8):
    n = int(dur * FPS); c = Clip(VID / "a1-accepted.mp4", W, H)
    last = None
    for i in range(n):
        fr = c.read(); last = fr
        if i < 8:  # 8-frame fade from the brief card's ground
            g = ground(); g.alpha_composite(alpha_mul(fr, ease(i / 8))); fr = g
        w.add(fr)
    c.close(); return last


def seg_freeze_static(w: Writer, hero_last: Image.Image, master4x5: Image.Image, dur=2.0):
    """Freeze on the hero frame, pull it into the 4:5 static's plate region, panel + exact typography animate on."""
    n = int(dur * FPS)
    cw, ch = 864, 1080; cx = (W - cw) // 2; plate_h = int(ch * 0.60)
    s = max(cw / W, plate_h / H); sw, sh = int(W * s), int(H * s)
    sx0 = int((sw - cw) * A1_ANCHOR[0] / s); sy0 = int((sh - plate_h) * A1_ANCHOR[1] / s)
    src_final = (sx0, sy0, sx0 + int(cw / s), sy0 + int(plate_h / s))
    dst_final = (cx, 0, cx + cw, plate_h)
    hold, pull = 0.40, 0.75
    lab = label(WR["label_static"], 30)
    for i in range(n):
        t = i / FPS; f = ground()
        if t < hold:
            fr = hero_last.copy()
            if i < 2:  # soft shutter: one bright frame
                fr = Image.blend(fr, Image.new("RGBA", fr.size, (255, 255, 255, 255)), 0.35)
            f.alpha_composite(fr)
        else:
            k = ease_io((t - hold) / pull)
            src = tuple(int(a + (b - a) * k) for a, b in zip((0, 0, W, H), src_final))
            dst = tuple(int(a + (b - a) * k) for a, b in zip((0, 0, W, H), dst_final))
            crop = hero_last.crop(src).resize((dst[2] - dst[0], dst[3] - dst[1]), Image.LANCZOS)
            f.alpha_composite(crop, (dst[0], dst[1]))
            b = ease((t - hold - pull * 0.55) / 0.7)
            if b > 0:
                card = Cp.aarohi(A1, "4x5", build=0.15 + 0.85 * b, anchor=A1_ANCHOR).resize((cw, ch), Image.LANCZOS)
                panel = card.crop((0, plate_h, cw, ch))
                f.alpha_composite(panel, (cx, plate_h))
            place_label(f, WR["label_static"], a=ease((t - hold - 0.3) / 0.4))
        w.add(f)


def seg_cards(w: Writer, cards: list[Image.Image], per: float, lab: str, counter=True, disclosure=False, list_lines=None, list_active=None):
    """Full-height cards owning the frame, one after another, with a small label (and optional side list)."""
    n_per = int(per * FPS)
    for ci, card in enumerate(cards):
        c = fit_h(card, H - int(H * 0.06))
        sh, pad = shadowed(c, blur=30, off=18, alpha=70)
        x = (W - c.width) // 2 if list_lines is None else int(W * 0.10)
        for i in range(n_per):
            t = i / FPS; f = ground()
            k = ease(t / 0.22)
            A.paste(f, alpha_mul(sh, k), x - pad, int(H * 0.03) - pad + int((1 - k) * 24))
            s = lab + (f" · {dyn(str(ci + 1))} / {dyn(str(len(cards)))}" if counter else "")
            place_label(f, s if not counter else lab)
            if counter:
                g = T(dyn(f"{ci + 1} / {len(cards)}"), "hn", 30, INK, 150)
                A.paste(f, g, int(W * 0.05), H - g.height - int(H * 0.075) - 44)
            if disclosure:
                place_disclosure(f, WR["disclosure"])
            if list_lines:
                lx = x + c.width + int(W * 0.06); ly = int(H * 0.22)
                for li, line in enumerate(list_lines):
                    active = (list_active(ci) == li)
                    g = T(line, "hn_medium" if active else "hn", 34, ACCENT if active else INK, 255 if active else 120)
                    A.paste(f, g, lx, ly); ly += g.height + 26
            w.add(f)


def seg_sizes(w: Writer, master: dict, dur=2.5):
    n = int(dur * FPS); hh = 520; gap = 44
    items = [(master["1x1"], WR["sizes"][0]), (master["4x5"], WR["sizes"][1]), (master["9x16"], WR["sizes"][2]), (master["wa"], WR["sizes"][3])]
    ims = [fit_h(im, hh) for im, _ in items]
    total = sum(i.width for i in ims) + gap * 3; x0 = (W - total) // 2; y0 = int(H * 0.20)
    shs = [shadowed(im, blur=22, off=12, alpha=60) for im in ims]
    for i in range(n):
        t = i / FPS; f = ground(); x = x0
        for j, ((sh, pad), (_, cap)) in enumerate(zip(shs, items)):
            k = ease((t - 0.15 - j * 0.32) / 0.3)
            A.paste(f, alpha_mul(sh, k), x - pad, y0 - pad + int((1 - k) * 30))
            g = label(cap, 26, INK, int(200 * k)); A.paste(f, g, x + (ims[j].width - g.width) // 2, y0 + hh + 30)
            x += ims[j].width + gap
        place_label(f, WR["label_sizes"])
        w.add(f)


def seg_master(w: Writer, hooks: list[Image.Image], dur=2.0):
    n = int(dur * FPS)
    mark = T(WR["wordmark"], "didot", 150, INK); sub = T(WR["master_sub"], "hn", 40, INK, 190)
    thumbs = [fit_h(h, 430) for h in hooks[:3]]
    for i in range(n):
        t = i / FPS; f = ground(); m = int(W * 0.08)
        A.paste(f, alpha_mul(mark, ease(t / 0.35)), m, int(H * 0.36))
        A.paste(f, alpha_mul(sub, ease((t - 0.2) / 0.4)), m, int(H * 0.36) + mark.height + 30)
        x = int(W * 0.58)
        for j, th in enumerate(thumbs):
            sh, pad = shadowed(th, blur=20, off=10, alpha=60)
            k = ease((t - 0.1 - j * 0.12) / 0.35)
            A.paste(f, alpha_mul(sh, k), x + j * 190 - pad, int(H * 0.30) + j * 40 - pad + int((1 - k) * 20))
        w.add(f)


def seg_static_motion(w: Writer, a2_static: Image.Image, dur=3.0):
    """The A2 static (full height) sheds its chrome; the plate region grows to the whole card and starts moving."""
    n = int(dur * FPS); cw, ch = 864, 1080; cx = (W - cw) // 2; plate_h = int(ch * 0.60)
    card = fit_h(a2_static, ch)
    plate_still = cover(A2, cw, ch, *A2_ANCHOR)
    c = Clip(VID / "a2-accepted.mp4", cw, ch, *A2_ANCHOR)
    hold, morph = 0.5, 0.7
    for i in range(n):
        t = i / FPS; f = ground()
        if t < hold:
            f.alpha_composite(card, (cx, 0))
        else:
            k = ease_io((t - hold) / morph)
            fr = c.read() if t >= hold + morph * 0.5 else plate_still
            f.alpha_composite(fr, (cx, 0))
            # chrome (the panel + type) dissolves while the plate takes the whole card
            panel = card.crop((0, plate_h, cw, ch))
            if k < 1:
                f.alpha_composite(alpha_mul(panel, 1 - k), (cx, plate_h + int(k * (ch - plate_h))))
        place_label(f, WR["label_static_motion"], a=ease((t - hold) / 0.4))
        w.add(f)
    c.close()


def seg_clip_full(w: Writer, src: Path, dur: float, lab: str | None = None, ax=0.5, ay=0.5, inset: Image.Image | None = None, inset_until=0.0, start=0.0):
    n = int(dur * FPS); c = Clip(src, W, H, ax, ay, start)
    ins = None
    if inset is not None:
        ins, ipad = shadowed(fit_h(inset, 300), blur=18, off=10, alpha=70)
    for i in range(n):
        t = i / FPS; fr = c.read(); f = fr.copy()
        if ins is not None:
            a = min(ease(t / 0.3), 1 - ease((t - inset_until) / 0.3))
            if a > 0:
                A.paste(f, alpha_mul(ins, a), int(W * 0.05) - ipad, int(H * 0.08) - ipad)
        if lab:
            place_label(f, lab, size=28)
        w.add(f)
    c.close()


def seg_still_full(w: Writer, im: Image.Image, dur: float, lab: str | None = None, push=0.04, anchor=(0.5, 0.5)):
    """Ken-Burns-free: a still owns the frame with a slow push (deterministic scale ramp)."""
    n = int(dur * FPS)
    base = cover(im, int(W * (1 + push)), int(H * (1 + push)), *anchor)
    for i in range(n):
        t = i / FPS; s = 1 + push * (1 - t / dur)
        cw, ch = int(W * (1 + push) / s), int(H * (1 + push) / s)
        x0 = (base.width - cw) // 2; y0 = (base.height - ch) // 2
        f = base.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.LANCZOS)
        if lab:
            place_label(f, lab, size=28)
        w.add(f)


def seg_card_full(w: Writer, card: Image.Image, dur: float, lab: str | None = None):
    n = int(dur * FPS); c = fit_h(card, H - int(H * 0.06)); sh, pad = shadowed(c, blur=30, off=18, alpha=70); x = (W - c.width) // 2
    for i in range(n):
        t = i / FPS; f = ground(); k = ease(t / 0.22)
        A.paste(f, alpha_mul(sh, k), x - pad, int(H * 0.03) - pad + int((1 - k) * 24))
        if lab:
            place_label(f, lab)
        w.add(f)


def seg_exact(w: Writer, master4x5: Image.Image, dhaba4x5: Image.Image, dur=3.5):
    n = int(dur * FPS); m = int(W * 0.07)
    head = T(WR["exact"], "hn_bold", 84, INK); sub = label(WR["exact_sub"], 26, INK, 170)
    Da = DECK["aarohi"]; Dd = DECK["dhaba"]
    brief_lines = [(Da["brand"], "hn"), (Da["eyebrow"], "hn"), (Da["headline"], "hn"), (Da["code"], "hn"), (Da["legal"], "hn"),
                   (Dd["l1"], "dev_regular"), (Dd["l2"], "dev_regular"), (Dd["l3"], "dev_regular"), (Dd["l4"], "dev_regular")]
    glyphs = [T(s, fnt, 34, INK) for s, fnt in brief_lines]
    crop_a = master4x5.crop((0, int(1350 * 0.60), 1080, 1350)); crop_a = crop_a.resize((int(crop_a.width * 0.62), int(crop_a.height * 0.62)), Image.LANCZOS)
    crop_d = dhaba4x5.crop((0, 0, 1080, 560)); crop_d = crop_d.resize((int(crop_d.width * 0.62), int(crop_d.height * 0.62)), Image.LANCZOS)
    tick = Image.new("RGBA", (30, 30), (0, 0, 0, 0)); ImageDraw.Draw(tick).line([(4, 16), (12, 24), (26, 6)], fill=A._hex_to_rgba(ACCENT), width=4)
    for i in range(n):
        t = i / FPS; f = ground()
        A.paste(f, head, m, int(H * 0.10)); A.paste(f, sub, m, int(H * 0.10) + head.height + 16)
        y = int(H * 0.32)
        for j, g in enumerate(glyphs):
            k = ease((t - 0.3 - j * 0.12) / 0.25)
            A.paste(f, alpha_mul(g, k), m, y)
            if t > 0.9 + j * 0.12:
                A.paste(f, tick, m + 520, y + (g.height - 30) // 2)
            y += g.height + 14
        x = int(W * 0.50)
        for j, cr in enumerate((crop_a, crop_d)):
            sh, pad = shadowed(cr, blur=20, off=10, alpha=60); k = ease((t - 0.5 - j * 0.5) / 0.4)
            A.paste(f, alpha_mul(sh, k), x - pad, int(H * 0.30) + j * (crop_a.height + 40) - pad + int((1 - k) * 20))
        w.add(f)


def seg_qa(w: Writer, dhaba_accepted: Image.Image, dur=3.0):
    """A REAL rejected output from this run (dhaba-r1: second rice bowl, no copy space) marked for <= 0.5 s, then the accepted replacement."""
    n = int(dur * FPS); show_rej = 0.5
    rej = fit_h(DH_REJ, H - int(H * 0.06)); acc = fit_h(dhaba_accepted, H - int(H * 0.06)); x = (W - rej.width) // 2
    head = T(WR["qa"], "hn_bold", 66, INK); sub = label(WR["qa_sub"], 26, INK, 170); rejl = label(DECK["intake"]["qa_reject"], 26, ACCENT)
    ring = Image.new("RGBA", (rej.width, rej.height), (0, 0, 0, 0)); d = ImageDraw.Draw(ring)
    sc = rej.height / DH_REJ.height
    for (cx, cy, r) in ((700 * sc, 265 * sc, 140 * sc), (780 * sc, 585 * sc, 165 * sc)):   # the two rice bowls in dhaba-r1 (1024x1280 space)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=A._hex_to_rgba(ACCENT), width=14)
    for i in range(n):
        t = i / FPS; f = ground()
        if t < show_rej:
            f.alpha_composite(rej, (x, int(H * 0.03)))
            f.alpha_composite(alpha_mul(ring, ease(t / 0.15)), (x, int(H * 0.03)))
        else:
            f.alpha_composite(acc, (x, int(H * 0.03)))
        hx = min(x + rej.width + int(W * 0.05), W - int(W * 0.05) - head.width)
        if t < show_rej:
            A.paste(f, rejl, x + rej.width + int(W * 0.05), int(H * 0.42))
        A.paste(f, alpha_mul(head, ease((t - show_rej) / 0.3)), hx, int(H * 0.40))
        A.paste(f, alpha_mul(sub, ease((t - show_rej - 0.1) / 0.3)), hx, int(H * 0.40) + head.height + 16)
        w.add(f)


def seg_bundle(w: Writer, files: list[Image.Image], files_complete_ist: str, dur=3.0):
    n = int(dur * FPS); m = int(W * 0.06)
    th = 200; thumbs = [fit_h(im, th) for im in files]
    t0, t1 = ist(CLOCK["brief_complete_ist"]), ist(files_complete_ist)
    el = t1 - t0; el_s = int(el.total_seconds()); el_txt = f"{el_s // 3600}h {(el_s % 3600) // 60:02d}m {el_s % 60:02d}s"
    head = T(WR["bundle"], "hn_bold", 84, INK)
    rows = [(WR["brief_ts_label"], dyn(t0.strftime("%H:%M:%S IST"))), (WR["files_ts_label"], dyn(t1.strftime("%H:%M:%S IST"))), (WR["elapsed_label"], dyn(el_txt))]
    rg = [(label(a, 24, INK, 160), T(b, "hn_medium", 44, INK)) for a, b in rows]
    cols = 5; gap = 22; colw = int(th * 0.8) + gap
    pos = []; x = m; y = int(H * 0.10); rowmax = 0
    for j, im in enumerate(thumbs):
        if x + im.width > int(W * 0.62):
            x = m; y += th + gap
        pos.append((x, y)); x += im.width + gap
    for i in range(n):
        t = i / FPS; f = ground()
        for j, im in enumerate(thumbs):
            k = ease((t - 0.1 - j * 0.07) / 0.3); x, y = pos[j]
            A.paste(f, alpha_mul(im, k), int(x), int(y) + int((1 - k) * 30))
        hx = int(W * 0.66); A.paste(f, head, hx, int(H * 0.12)); y = int(H * 0.12) + head.height + 40
        for j, (la, va) in enumerate(rg):
            k = ease((t - 0.6 - j * 0.35) / 0.3)
            A.paste(f, alpha_mul(la, k), hx, y); y += la.height + 6
            A.paste(f, alpha_mul(va, k), hx, y); y += va.height + 26
        w.add(f)


def seg_type(w: Writer, lines: list[tuple[str, str, int]], dur: float, sub: str | None = None, align="left"):
    n = int(dur * FPS); m = int(W * 0.08)
    gl = [T(s, fnt, sz, INK) for s, fnt, sz in lines]
    sg = label(sub, 26, INK, 170) if sub else None
    total = sum(g.height for g in gl) + 20 * (len(gl) - 1) + (sg.height + 40 if sg else 0)
    for i in range(n):
        t = i / FPS; f = ground(); y = (H - total) // 2
        for j, g in enumerate(gl):
            k = ease((t - j * 0.12) / 0.35); x = m if align == "left" else (W - g.width) // 2
            A.paste(f, alpha_mul(g, k), x, y + int((1 - k) * 24)); y += g.height + 20
        if sg:
            k = ease((t - 0.4) / 0.35); x = m if align == "left" else (W - sg.width) // 2
            A.paste(f, alpha_mul(sg, k), x, y + 20)
        w.add(f)


def seg_intake(w: Writer, files: list[Image.Image], dur=7.5):
    """Campaign assets collapse into a clean intake card; CTA lines follow."""
    n = int(dur * FPS); cw, ch = 1100, 520; cx, cy = (W - cw) // 2, (H - ch) // 2
    card = Image.new("RGBA", (cw, ch), (255, 255, 255, 255))
    d = ImageDraw.Draw(card); d.rounded_rectangle([0, 0, cw - 1, ch - 1], radius=28, fill=(255, 255, 255, 255), outline=(17, 17, 17, 40), width=2)
    Di = DECK["intake"]
    for j, lab_ in enumerate((Di["field_link"], Di["field_offer"])):
        y = 70 + j * 170
        d.rounded_rectangle([60, y + 44, cw - 60, y + 130], radius=14, fill=(243, 239, 231, 255))
        A.paste(card, label(lab_, 24, INK, 160), 60, y)
    card, pad = shadowed(card, blur=30, off=18, alpha=60)
    thumbs = [fit_h(im, 220) for im in files]
    cta1 = T(WR["cta"], "hn_bold", 66, INK); cta2 = T(WR["cta2"], "hn_medium", 48, INK)
    collapse = 0.9
    for i in range(n):
        t = i / FPS; f = ground(); k = ease_io(t / collapse)
        for j, im in enumerate(thumbs):
            ang = j / len(thumbs) * 2 * math.pi
            sx, sy = W / 2 + math.cos(ang) * 760 - im.width / 2, H / 2 + math.sin(ang) * 380 - im.height / 2
            x = sx + (W / 2 - im.width / 2 - sx) * k; y = sy + (H / 2 - im.height / 2 - sy) * k
            A.paste(f, alpha_mul(im, 1 - k), int(x), int(y))
        if t > collapse * 0.7:
            a = ease((t - collapse * 0.7) / 0.35)
            A.paste(f, alpha_mul(card, a), cx - pad, cy - 60 - pad)
        y = cy + ch - 60 + 40
        A.paste(f, alpha_mul(cta1, ease((t - 1.3) / 0.4)), (W - cta1.width) // 2, y)
        if t > 3.6:
            a = ease((t - 3.6) / 0.4)
            A.paste(f, alpha_mul(cta2, a), (W - cta2.width) // 2, y + cta1.height + 24)
        w.add(f)


def seg_final(w: Writer, dur=3.5):
    n = int(dur * FPS)
    gl = [tracked(s, "hn_bold", 72, INK, 0.12) for s in WR["final"]]
    for s in WR["final"]:
        Cp.USED.add(s)
    mark = T(WR["wordmark"], "didot", 56, INK, 200)
    total = sum(g.height for g in gl) + 34 * 2
    for i in range(n):
        t = i / FPS; f = ground(); y = (H - total) // 2 - 40
        for j, g in enumerate(gl):
            k = ease((t - 0.1 - j * 0.25) / 0.4); A.paste(f, alpha_mul(g, k), (W - g.width) // 2, y + int((1 - k) * 20)); y += g.height + 34
        A.paste(f, alpha_mul(mark, ease((t - 1.0) / 0.5)), (W - mark.width) // 2, H - int(H * 0.14))
        if t > dur - 0.6:  # single fade to ground at the very end
            f = Image.blend(f, ground(), ease((t - (dur - 0.6)) / 0.6))
        w.add(f)


# ------------------------------------------------------------------------------------------------- the 9:16 Aarohi video ad

def aarohi_ad_9x16(out: Path, files_dir: Path):
    """10–12 s 9:16 ad: the Ledge 9:16 layout whose plate is the moving A2 → A1 → A3 clips; offer text composed in post."""
    Wv, Hv = 1080, 1920; plate_h = int(Hv * 0.58)
    seq = [("a2-accepted.mp4", A2_ANCHOR, 4.0), ("a1-accepted.mp4", A1_ANCHOR, 4.0), ("a3-accepted.mp4", A3_ANCHOR, 3.5)]
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{Wv}x{Hv}", "-r", str(FPS), "-i", "-",
                          "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
    chrome_full = Cp.aarohi(A2, "9x16", anchor=A2_ANCHOR)
    panel = chrome_full.crop((0, plate_h, Wv, Hv))
    tglob = 0.0
    for src, anc, d in seq:
        c = Clip(VID / src, Wv, plate_h, *anc); n = int(d * FPS); prev = None
        for i in range(n):
            fr = c.read(); f = Image.new("RGBA", (Wv, Hv), A._hex_to_rgba(Cp.AAROHI["primary"]))
            if i < 10 and prev is not None:
                fr = Image.blend(prev, fr, ease(i / 10))
            f.alpha_composite(fr, (0, 0))
            b = ease((tglob - 0.4) / 1.0)
            card = Cp.aarohi(A2, "9x16", build=0.15 + 0.85 * b, anchor=A2_ANCHOR) if b < 1 else chrome_full
            f.alpha_composite(card.crop((0, plate_h, Wv, Hv)), (0, plate_h))
            p.stdin.write(f.convert("RGB").tobytes()); tglob += 1 / FPS
        prev = c.last; c.close()
    p.stdin.close(); p.wait()


# ------------------------------------------------------------------------------------------------- main

def main(out_dir: str):
    out = Path(out_dir); seg = out / "seg"; seg.mkdir(parents=True, exist_ok=True)
    S = statics()
    files_dir = GEN / "deliverables"; files_dir.mkdir(exist_ok=True)
    for fmt, im in S["master"].items():
        im.convert("RGB").save(files_dir / f"aarohi-master-{fmt}.png")
    for j, im in enumerate(S["hooks"], 1):
        im.convert("RGB").save(files_dir / f"aarohi-hook-{j}-4x5.png")
    S["hindi"].convert("RGB").save(files_dir / "aarohi-hindi-4x5.png")
    S["a2_hook"].convert("RGB").save(files_dir / "aarohi-scene-vanity-4x5.png"); S["a3_hook"].convert("RGB").save(files_dir / "aarohi-scene-festive-4x5.png")
    S["kora_4x5"].convert("RGB").save(files_dir / "kora-hook-1-4x5.png")
    for j, im in enumerate(S["kora_16x9"], 1):
        im.convert("RGB").save(files_dir / f"kora-hook-{j}-16x9.png")
    S["dhaba_4x5"].convert("RGB").save(files_dir / "dhaba47-hindi-4x5.png"); S["dhaba_wa"].convert("RGB").save(files_dir / "dhaba47-hindi-wa-800.png")
    ad = files_dir / "aarohi-video-ad-9x16.mp4"
    if not ad.exists():
        aarohi_ad_9x16(ad, files_dir)
    # files-complete = the moment the Aarohi bundle (4 sizes, 6 hooks, Hindi, 9:16 video) exists on disk — recorded mechanically
    clock_path = GEN / "CLOCK.json"; clk = json.loads(clock_path.read_text())
    if "files_complete_ist" not in clk:
        from datetime import timezone, timedelta
        now = datetime.now(timezone(timedelta(hours=5, minutes=30)))
        clk["files_complete_ist"] = now.isoformat(); clk["files_complete_utc"] = now.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        clk["elapsed_s"] = int((now - ist(clk["brief_complete_ist"])).total_seconds())
        clk["bundle"] = sorted(p.name for p in files_dir.iterdir() if p.name.startswith("aarohi"))
        clock_path.write_text(json.dumps(clk, indent=1))
    ad_first = Image.open(subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", "3.0", "-i", str(ad), "-frames:v", "1", str(seg / "ad-frame.png")]) and seg / "ad-frame.png").convert("RGBA")
    bundle_files = [S["master"]["4x5"], S["master"]["1x1"], S["master"]["9x16"], S["master"]["wa"], ad_first, *S["hooks"], S["hindi"], S["dhaba_4x5"], S["dhaba_wa"], S["kora_4x5"]]

    order = []
    def run(name, fn, *a, **k):
        w = Writer(seg / f"{name}.mp4"); r = fn(w, *a, **k); d = w.close(); order.append((name, seg / f"{name}.mp4", d)); print(f"{name:14s} {d:5.2f} s"); return r

    run("s01-brief", seg_brief)
    hero_last = run("s02-hero", seg_hero)
    run("s03-freeze", seg_freeze_static, hero_last, S["master"]["4x5"])
    run("s04-dirs", seg_cards, [S["master"]["4x5"], S["a2_hook"], S["a3_hook"], S["kora_4x5"]], 0.75, WR["label_scenes"], counter=True, disclosure=True)
    run("s05-sizes", seg_sizes, S["master"])
    run("s06-hooks", seg_cards, S["hooks"], 0.37, WR["label_hooks"], counter=False, list_lines=HOOKS, list_active=lambda ci: ci)
    run("s06b-hindi", seg_card_full, S["hindi"], 1.3, WR["label_hindi"])
    run("s07-master", seg_master, S["hooks"])
    run("s08-stmo", seg_static_motion, S["a2_hook"])
    run("s09a-a3", seg_clip_full, VID / "a3-accepted.mp4", 2.5, WR["label_video_16"])
    run("s09b-ad", seg_clip_card, ad, 2.5, WR["label_video"])
    run("s10a-b1", seg_clip_full, VID / "b1-accepted.mp4", 3.0, WR["label_new_scenes"], inset=B0, inset_until=1.4)
    run("s10b-b2", seg_still_full, B2, 0.75)
    run("s10c-b3", seg_still_full, B3, 0.75)
    run("s11a-kora", seg_still_full, S["kora_16x9"][0], 1.75, WR["label_range"], push=0.03)
    run("s11b-kora", seg_still_full, S["kora_16x9"][3], 1.75, WR["label_range"], push=0.03)
    run("s12-exact", seg_exact, S["master"]["4x5"], S["dhaba_4x5"])
    run("s13-qa", seg_qa, S["dhaba_4x5"])
    run("s14-bundle", seg_bundle, bundle_files, clk["files_complete_ist"])
    run("s15-24h", seg_type, [(WR["standard"], "hn_medium", 48), (WR["standard_big"], "hn_bold", 210)], 3.5)
    run("s16-4h", seg_type, [(WR["express_big"], "hn_bold", 150)], 3.0, sub=WR["express_sub"])
    run("s17-intake", seg_intake, bundle_files[:10])
    run("s18-final", seg_final)

    lst = out / "concat.txt"; lst.write_text("".join(f"file '{p.resolve()}'\n" for _, p, _ in order))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-an", "-c:v", "libx264", "-crf", "16", "-preset", "medium",
                    "-pix_fmt", "yuv420p", "-r", str(FPS), str(out / "video.mp4")], check=True)
    starts = {}; t = 0.0
    for name, _, d in order:
        starts[name] = round(t, 3); t += d
    (out / "timeline.json").write_text(json.dumps({"starts": starts, "total_s": round(t, 3)}, indent=1))
    off = Cp.deck_check(DYN)
    print("total", round(t, 2), "s; off-deck strings:", off)


def seg_clip_card(w: Writer, src: Path, dur: float, lab: str):
    """A 9:16 clip owning its full height in the frame (the finished vertical ad)."""
    n = int(dur * FPS); ch = H - int(H * 0.06); cw = int(ch * 9 / 16); x = (W - cw) // 2
    c = Clip(src, cw, ch, start=2.0)
    for i in range(n):
        t = i / FPS; fr = c.read(); f = ground(); sh, pad = shadowed(fr, blur=30, off=18, alpha=70)
        A.paste(f, alpha_mul(sh, ease(t / 0.22)), x - pad, int(H * 0.03) - pad)
        place_label(f, lab); w.add(f)
    c.close()


if __name__ == "__main__":
    main(sys.argv[1])
