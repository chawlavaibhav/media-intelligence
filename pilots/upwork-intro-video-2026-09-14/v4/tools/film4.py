#!/usr/bin/env python3
"""V4 renderer — the Controller's second-by-second edit (§11) drawn only through design4 (tokens, measured text, contrast,
contain-fit). usage: film4.py <assembly_dir>"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import design4 as D  # noqa: E402
from design4 import A, T, W, H, SAFE, place_text, tab, card, contain, native, declared_cover, LayoutError  # noqa: E402

V4 = D.V4; V3G = V4.parent / "v3" / "gen"; FPS = T["fps"]
BG = T["wrapper_bg"]; FG = T["wrapper_fg"]; MUTED = T["muted_fg"]; ACC = T["accent"]
SX, SY = T["safe_x"], T["safe_y"]; XS, SM, MD, LG = T["spacing_xs"], T["spacing_sm"], T["spacing_md"], T["spacing_lg"]
FH, FM, FR = T["font_h"], T["font_m"], T["font_r"]
AAROHI = dict(primary="#1F4B3F", accent="#D9A441", cream="#F4EFE6")
DISCLOSURE = "DEMONSTRATION · INVENTED BRANDS"


def ease(t):
    t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3


def ease_io(t):
    t = max(0.0, min(1.0, t)); return 0.5 - 0.5 * math.cos(math.pi * t)


def ground():
    return Image.new("RGBA", (W, H), A._hex_to_rgba(BG))


def alpha_mul(im, a):
    if a >= 1:
        return im
    o = im.copy(); o.putalpha(o.getchannel("A").point(lambda v: int(v * max(0.0, a)))); return o


class Writer:
    def __init__(self, out: Path):
        out.parent.mkdir(parents=True, exist_ok=True)
        self.p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                                   "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "15", "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
        self.n = 0; self.keyframes = {}

    def add(self, im, key=None):
        if key and key not in self.keyframes:
            self.keyframes[key] = im.convert("RGB").copy()
        self.p.stdin.write(im.convert("RGB").tobytes()); self.n += 1

    def close(self):
        self.p.stdin.close(); self.p.wait(); return self.n / FPS


class Clip:
    """Stream a clip at 30 fps at its native 1920x1080 (no crop) — one frame in memory at a time."""

    def __init__(self, src: Path, start=0.0):
        self.p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-ss", f"{start:.3f}", "-i", str(src), "-vf", f"fps={FPS},scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                                  stdout=subprocess.PIPE, stderr=subprocess.DEVNULL); self.last = None

    def read(self):
        buf = self.p.stdout.read(W * H * 3)
        if len(buf) < W * H * 3:
            return self.last
        self.last = Image.frombytes("RGB", (W, H), buf).convert("RGBA"); return self.last

    def close(self):
        self.p.stdout.close(); self.p.kill(); self.p.wait()


# ------------------------------------------------------------------ assets (all accepted V3 media; nothing regenerated)
def load(p): return Image.open(p).convert("RGBA")
DL = V4 / "gen/deliverables"
MASTER = {f: load(DL / f"aarohi-master-{f}.png") for f in ("4x5", "1x1", "9x16", "wa")}
HOOKS = [load(DL / f"aarohi-hook-{i}-4x5.png") for i in range(1, 7)]
HINDI = load(DL / "aarohi-hindi-4x5.png")
A2 = load(V3G / "stills/a2-accepted.png"); B0 = load(V3G / "stills/brewa0-accepted.png"); B1 = load(V3G / "stills/b1-accepted.png")
SPEAKER = V4 / "gen/speaker/speaker-accepted.mp4"; BUBBLE_SRC = load(V4 / "gen/speaker/speaker-bubble-frame.png")
FACE_BOX = (692, 152, 1252, 712)   # 560-px square around the speaker's face in the 1920x1080 frame (declared cover for the bubble)


# ------------------------------------------------------------------ Loom bubble
VAIBHAV = load(V4 / "gen/speaker/vaibhav-cutout.png")   # background removed (rembg isnet), 398 px source
BUBBLE_TONE = "#E9E3D8"


def portrait_tile(size: int) -> Image.Image:
    """Vaibhav's cutout on a quiet tone, head sized to the tile, shoulders bleeding off the bottom edge."""
    tile = Image.new("RGBA", (size, size), A._hex_to_rgba(BUBBLE_TONE))
    s = size / VAIBHAV.width * 1.06; im = VAIBHAV.resize((int(VAIBHAV.width * s), int(VAIBHAV.height * s)), Image.LANCZOS)
    tile.alpha_composite(im, ((size - im.width) // 2, size - im.height + int(size * 0.02))); return tile


def bubble_image():
    face = declared_cover(BUBBLE_SRC, FACE_BOX, "bubble-face", "all", "speaker-bubble-frame.png", "the AI speaker's face during the 0.65-s reduction only")
    D.REPORT["crop"].append({"id": "bubble-vaibhav", "beat": "all", "source": "vaibhav-cutout.png", "fit": "contain(cutout)", "fraction_shown": 1.0})
    im, pad = card(portrait_tile(T["bubble_size"]), "bubble", "all", radius=T["bubble_radius"]); return im, pad


BUBBLE, BPAD = bubble_image()
BUBBLE_POS_L = (SX, H - SY - T["bubble_size"])
BUBBLE_POS_R = (W - SX - T["bubble_size"], H - SY - T["bubble_size"])


def draw_bubble(f, a=1.0, pos=BUBBLE_POS_L):
    if a > 0:
        f.alpha_composite(alpha_mul(BUBBLE, a), (pos[0] - BPAD, pos[1] - BPAD))


# ------------------------------------------------------------------ the craft ad (Proof 2): deterministic Ledge with a CTA button
def craft_ad(plate: Image.Image):
    """1080x1350: plate top, brand panel, hook headline, offer pill on the seam, code, SHOP NOW button, legal, mark.
    Returns (image, boxes) with boxes for hook / offer / cta in image coordinates."""
    Wc, Hc = 1080, 1350; seam = int(Hc * 0.53); m = 76; B = AAROHI
    canvas = Image.new("RGBA", (Wc, Hc), A._hex_to_rgba(B["primary"]))
    # plate: contain-fit is impossible for a 4:5 plate in a 1080x756 region; the plate is cover-cropped by DESIGN (it is the
    # ad's own art direction, not portfolio evidence) — recorded as declared cover
    s = max(Wc / plate.width, seam / plate.height); pw, ph = int(plate.width * s + .5), int(plate.height * s + .5)
    pl = plate.resize((pw, ph), Image.LANCZOS); x0 = (pw - Wc) // 2; y0 = int((ph - seam) * 0.42)
    D.REPORT["crop"].append({"id": "craft-plate", "beat": "proof2", "source": "a2-accepted.png", "fit": "cover(declared)", "reason": "ad-internal plate crop (Ledge layout), not portfolio evidence", "fraction_shown": round((Wc * seam) / (pw * ph), 3)})
    canvas.alpha_composite(pl.crop((x0, y0, x0 + Wc, y0 + seam)), (0, 0))
    boxes = {}
    y = seam + 44
    lines = ["YOUR NIGHT", "ROUTINE, SIMPLIFIED."]; hl = 80
    while max(A.text_width(l, "didot", hl) for l in lines) > Wc - 2 * m - int(Wc * 0.05):
        hl -= 2
    hy0 = y
    for l in lines:
        g = A.text(l, "didot", hl, B["cream"]); canvas.alpha_composite(g, (m, y)); y += int(hl * 1.05)
    boxes["hook"] = (m - 20, hy0 - 16, Wc - m + 20, y + 4)
    y += 30
    pill = A.pill("15% OFF FIRST ORDER", "hn_medium", 36, "#2C5E4F", B["accent"])   # offer: quiet tint, gold type; the gold button stays the only action
    canvas.alpha_composite(pill, (m, y)); boxes["offer"] = (m - 20, y - 14, m + pill.width + 20, y + pill.height + 14)
    y += pill.height + 30
    btn = A.button("SHOP NOW", "hn_medium", 36, B["accent"], B["primary"], min_w=340); canvas.alpha_composite(btn, (m, y))
    boxes["cta"] = (m - 20, y - 16, m + btn.width + 20, y + btn.height + 16)
    y += btn.height + 30
    code = A.text("CODE AAROHI15", "hn_medium", 30, B["cream"], alpha=230); canvas.alpha_composite(code, (m, y))
    boxes["code"] = (m, y, m + code.width, y + code.height)
    y += code.height
    leg = A.text("T&Cs apply", "hn", 26, B["cream"], alpha=170); mark = A.text("AAROHI SKIN", "didot", 44, B["cream"])
    ly = Hc - 64; canvas.alpha_composite(leg, (m, ly - leg.height)); canvas.alpha_composite(mark, (Wc - m - mark.width, ly - mark.height))
    boxes["legal"] = (m, ly - leg.height, m + leg.width, ly); boxes["mark"] = (Wc - m - mark.width, ly - mark.height, Wc - m, ly)
    # nothing may touch or overlap: every pair of element boxes must be disjoint (with the spotlight padding removed)
    inner = {k: (b[0] + (20 if k in ("hook", "offer", "cta") else 0), b[1] + (16 if k in ("hook", "offer", "cta") else 0),
                 b[2] - (20 if k in ("hook", "offer", "cta") else 0), b[3] - (16 if k in ("hook", "offer", "cta") else 0)) for k, b in boxes.items()}
    ks = list(inner)
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            a, b = inner[ks[i]], inner[ks[j]]
            assert a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1], f"craft ad: {ks[i]} overlaps {ks[j]}"
    assert boxes["code"][3] + 24 <= boxes["legal"][1], "craft ad: code touches the legal line"
    D.REPORT["cards"].append({"id": "craft-ad-elements", "beat": "proof2", "kind": "ad-internal", "boxes": inner, "disjoint": True})
    return canvas, boxes


# ------------------------------------------------------------------ beats
def beat_speaker(w: Writer, dur=8.5):
    """00:00 speaker full screen. Clip 0–7.75 s then the 7.7-s frame held. No supers."""
    n = int(dur * FPS); c = Clip(SPEAKER); last = None
    native(Image.new("RGBA", (W, H)), "speaker", "speaker", "speaker-accepted.mp4")
    for i in range(n):
        t = i / FPS
        fr = c.read() if t < 7.75 else BUBBLE_SRC
        if t >= 7.75:
            fr = BUBBLE_SRC
        last = fr; w.add(fr, key="01-speaker" if i == int(3 * FPS) else None)
    c.close(); return last


def beat_handoff(w: Writer, dur=4.3):
    """00:08.5 speaker reduces into the bubble (0.65 s); AND IT CAN'T SUCK. held 1.3 s with weight; then the statement."""
    n = int(dur * FPS); red = 0.65; punch_end = red + 1.3
    lines = ["MORE CREATIVE.", "FASTER.", "WITHOUT LOWERING THE BAR."]
    size = D.fit_size(lines, FH, [T["h1_size"], 104, 96, 88, 80, 72], W - 2 * SX - T["bubble_size"] - LG, 64)
    gl = [A.text(l, FH, size, FG) for l in lines]; gap = int(size * 0.28)
    total = sum(g.height for g in gl) + gap * 2; y0 = (H - total) // 2 - 20
    psize = D.fit_size(["AND IT CAN'T SUCK."], FH, [T["giant_size"], 152, 136, 120, 112], W - 2 * SX - T["bubble_size"] - LG, 96)
    pw, ph = D.measure("AND IT CAN'T SUCK.", FH, psize)
    bx, by = BUBBLE_POS_L; bs = T["bubble_size"]
    for i in range(n):
        t = i / FPS; f = ground()
        k = ease_io(t / red)
        if k < 1:
            src = tuple(int(a + (b - a) * k) for a, b in zip((0, 0, W, H), FACE_BOX))
            dst = tuple(int(a + (b - a) * k) for a, b in zip((0, 0, W, H), (bx, by, bx + bs, by + bs)))
            im = BUBBLE_SRC.crop(src).resize((dst[2] - dst[0], dst[3] - dst[1]), Image.LANCZOS)
            im = D.mask_rounded(im, int(T["bubble_radius"] * k)); f.alpha_composite(im, (dst[0], dst[1]))
        else:   # the AI speaker hands over to the person who directs the work
            sw = ease((t - red) / 0.35)
            if sw < 1:
                spk = D.mask_rounded(BUBBLE_SRC.crop(FACE_BOX).resize((bs, bs), Image.LANCZOS), T["bubble_radius"]); f.alpha_composite(alpha_mul(spk, 1 - sw), (bx, by))
            draw_bubble(f, sw)
        if t < punch_end:
            a = ease((t - red + 0.05) / 0.22)
            if a > 0:
                place_text(f, "punch", "AND IT CAN'T SUCK.", FH, psize, FG, SX, (H - ph) // 2 - 20 + int((1 - a) * 12), "handoff", alpha=a, check=a >= 1, role="display")
                rule = Image.new("RGBA", (int(pw * 0.18), 10), A._hex_to_rgba(ACC, int(255 * a))); f.alpha_composite(rule, (SX, (H - ph) // 2 - 20 + ph + SM))
        else:
            y = y0
            for j, (l, g) in enumerate(zip(lines, gl)):
                a = ease((t - punch_end - j * 0.22) / 0.3)
                if a > 0:
                    place_text(f, f"statement-{j}", l, FH, size, FG, SX, y + int((1 - a) * 18), "handoff", alpha=a, check=a >= 1, role="display")
                y += g.height + gap
        w.add(f, key="02a-punch" if abs(t - 1.5) < 0.02 else ("02b-handoff" if abs(t - 3.8) < 0.02 else None))


def beat_proof1(w: Writer, dur=5.0):
    """00:12 the strongest finished static, contain-fit, most of the frame; wrapper copy small at left."""
    n = int(dur * FPS); beat = "proof1"
    ad = contain(MASTER["4x5"], W, H - 2 * SY, "master-4x5", beat, "aarohi-master-4x5.png")
    cardim, pad = card(ad, "master-card", beat)
    ax = W - SX - ad.width; ay = SY
    copy = [("GREAT IMAGES AREN'T ENOUGH.", FM, 44), ("THEY HAVE TO WORK AS ADS.", FM, 44)]
    for i in range(n):
        t = i / FPS; f = ground(); a = ease(t / 0.35)
        f.alpha_composite(alpha_mul(cardim, a), (ax - pad, ay - pad + int((1 - a) * 16)))
        place_text(f, "disclosure", DISCLOSURE, FR, T["small_size"], MUTED, SX, SY, beat, check=True)
        y = int(H * 0.36)
        for j, (s, fnt, sz) in enumerate(copy):
            aa = ease((t - 0.5 - j * 0.25) / 0.4)
            if aa > 0:
                place_text(f, f"p1-copy-{j}", s, fnt, sz, FG, SX, y, beat, alpha=aa, check=aa >= 1, role="body"); y += sz + SM
        draw_bubble(f)
        w.add(f, key="03-proof1" if abs(t - 3.0) < 0.02 else None)


def beat_proof2(w: Writer, dur=6.5):
    """00:18 ad craft: finished ad first, then HOOK → OFFER → CTA sequential spotlight."""
    n = int(dur * FPS); beat = "proof2"
    adfull, boxes = craft_ad(A2)
    (V4 / "gen/deliverables").mkdir(exist_ok=True); adfull.convert("RGB").save(V4 / "gen/deliverables/aarohi-craft-4x5.png")
    ad = contain(adfull, W, H - 2 * SY, "craft-ad", beat, "aarohi-craft-4x5.png (deterministic)")
    sc = ad.width / adfull.width; cardim, pad = card(ad, "craft-card", beat)
    ax = W - SX - ad.width; ay = SY
    steps = [("HOOK", "hook", 1.5), ("OFFER", "offer", 3.1), ("CTA", "cta", 4.7)]
    for i in range(n):
        t = i / FPS; f = ground(); a = ease(t / 0.35)
        f.alpha_composite(alpha_mul(cardim, a), (ax - pad, ay - pad + int((1 - a) * 16)))
        cur = None
        for lab, key, t0 in steps:
            if t >= t0:
                cur = (lab, key, t0)
        if cur:
            lab, key, t0 = cur; k = ease((t - t0) / 0.35)
            bx = tuple(int(v * sc) for v in boxes[key]); hole = (ax + bx[0], ay + bx[1], ax + bx[2], ay + bx[3])
            dim = Image.new("RGBA", (W, H), (17, 17, 17, 255))
            m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rounded_rectangle((ax, ay, ax + ad.width, ay + ad.height), radius=T["card_radius"], fill=int(120 * k))
            ImageDraw.Draw(m).rounded_rectangle(hole, radius=T["card_radius"], fill=0)
            dim.putalpha(m.filter(ImageFilter.GaussianBlur(4))); f.alpha_composite(dim)
            ring = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ring).rounded_rectangle(hole, radius=T["card_radius"], outline=A._hex_to_rgba(ACC, int(255 * k)), width=4)
            f.alpha_composite(ring)
            place_text(f, f"p2-{key}", lab, FH, T["h2_size"], FG, SX, int(H * 0.40), beat, alpha=k, check=k >= 1, role="display")
            rule = Image.new("RGBA", (int(LG * 0.8), 6), A._hex_to_rgba(ACC, int(255 * k))); f.alpha_composite(rule, (SX, int(H * 0.40) + T["h2_size"] + SM))
        draw_bubble(f, 1 - ease((t - (dur - 0.6)) / 0.5))
        w.add(f, key="04-proof2" if abs(t - 3.6) < 0.02 else None)


def beat_proof3(w: Writer, dur=5.5):
    """00:24 SAME PRODUCT (packshot, contain, 2.5 s) → NEW SCENE (B1 native 16:9, no crop)."""
    n = int(dur * FPS); beat = "proof3"; cut = 2.2
    ps = contain(B0, int(W * 0.42), H - 2 * SY, "brewa-packshot", beat, "brewa0-accepted.png"); pcard, pad = card(ps, "packshot-card", beat)
    px = SX; py = SY + (H - 2 * SY - ps.height) // 2
    scene = native(B1, "brewa-scene", beat, "b1-accepted.png")
    for i in range(n):
        t = i / FPS
        if t < cut:
            f = ground(); a = ease(t / 0.35)
            f.alpha_composite(alpha_mul(pcard, a), (px - pad, py - pad))
            place_text(f, "disclosure", DISCLOSURE, FR, T["small_size"], MUTED, W - SX - D.measure(DISCLOSURE, FR, T["small_size"])[0], SY, beat)
            x = px + ps.width + LG; y = int(H * 0.40)
            aa = ease((t - 0.3) / 0.35)
            place_text(f, "p3-same", "SAME PRODUCT.", FH, T["h2_size"], FG, x, y, beat, alpha=aa, check=aa >= 1, role="display")
        else:
            k = ease((t - cut) / 0.4); f = scene.copy()
            if k < 1:
                f = Image.blend(ground(), scene, k)
            aa = ease((t - cut - 0.3) / 0.35)
            if aa > 0:
                tab(f, "p3-tab", [("NEW SCENE.", FH, T["h2_size"], FG), ("Shape. Colour. Details held.", FM, T["body_size"], MUTED)], SX, SY, beat, alpha=aa)
        w.add(f, key="05-proof3a" if abs(t - 1.5) < 0.02 else ("05-proof3b" if abs(t - 4.5) < 0.02 else None))


def beat_proof4(w: Writer, dur=8.0):
    """00:30 the video, full screen, native: A1 hero 5.0 s + A3 3.0 s. Tab label for the first 2.5 s only."""
    n = int(dur * FPS); beat = "proof4"
    native(Image.new("RGBA", (W, H)), "a1-clip", beat, "a1-accepted.mp4"); native(Image.new("RGBA", (W, H)), "a3-clip", beat, "a3-accepted.mp4")
    c1 = Clip(V3G / "video/a1-accepted.mp4"); c2 = Clip(V3G / "video/a3-accepted.mp4"); c = c1
    for i in range(n):
        t = i / FPS
        if t >= 5.0 and c is c1:
            c = c2
        f = c.read().copy()
        a = min(ease(t / 0.3), 1 - ease((t - 2.2) / 0.3))
        if a > 0:
            tab(f, "p4-tab", [("AND THEN IT MOVES.", FH, T["h2_size"], FG)], SX, SY, beat, alpha=a)
        w.add(f, key="06-proof4" if abs(t - 3.0) < 0.02 else None)
    c1.close(); c2.close()


KORA = load(V4 / "gen/deliverables/kora-hook-1-16x9.png")


def beat_kora(w: Writer, dur=2.8):
    """Creative range: the accepted Kora Threads finished creative, full screen, native 1920x1080, no wrapper copy."""
    n = int(dur * FPS); im = native(KORA, "kora-16x9", "kora", "kora-hook-1-16x9.png (deterministic on kora-accepted.png)")
    for i in range(n):
        t = i / FPS; f = im.copy()
        if i < 8:
            f = Image.blend(ground(), im, ease(i / 8))
        w.add(f, key="06b-kora" if abs(t - 1.5) < 0.02 else None)


def beat_proof5(w: Writer, dur=5.0):
    """00:38 ONE DIRECTION. MORE TO TEST. — approved layout, then 4 FORMATS, 6 HOOKS, ENGLISH + HINDI revealed in turn."""
    n = int(dur * FPS); beat = "proof5"
    colw = max(376, D.measure("ONE DIRECTION.", FH, T["h2_size"])[0], D.measure("MORE TO TEST.", FH, T["h2_size"])[0])
    master = contain(MASTER["4x5"], 376, 470, "p5-master", beat, "aarohi-master-4x5.png"); mcard, mpad = card(master, "p5-master-card", beat)
    rx = SX + colw + LG; rw = W - SX - rx
    fh = 300
    while True:  # formats row: shrink the row height until the four whole renditions fit the column (never crop)
        fmts = [contain(MASTER[k], 400, fh, f"p5-fmt-{k}", beat, f"aarohi-master-{k}.png") for k in ("1x1", "4x5", "9x16", "wa")]
        if sum(im.width for im in fmts) + 3 * SM <= rw or fh <= 200:
            break
        fh -= 10
    assert sum(im.width for im in fmts) + 3 * SM <= rw, "proof5 formats row does not fit"
    fcards = [card(im, f"p5-fmt-card-{k}", beat, shadow=False) for im, k in zip(fmts, ("1x1", "4x5", "9x16", "wa"))]
    hh = 190; hw = int(hh * 0.8)
    hooks = [contain(h, hw, hh, f"p5-hook-{j}", beat, f"aarohi-hook-{j}-4x5.png") for j, h in enumerate(HOOKS, 1)]
    hcards = [card(im, f"p5-hook-card-{j}", beat, shadow=False) for j, im in enumerate(hooks, 1)]
    grid_w = 3 * hw + 2 * SM; hindi_w = rw - grid_w - MD
    hindi = contain(HINDI, hindi_w, 2 * hh + SM, "p5-hindi", beat, "aarohi-hindi-4x5.png"); hcard, hpad = card(hindi, "p5-hindi-card", beat, shadow=False)
    assert grid_w + MD + hindi.width <= rw, "proof5 hooks/hindi row does not fit"
    lab_h = T["small_size"] + XS
    y_fmt = SY + lab_h + XS; y_hooks = y_fmt + fh + MD + lab_h + XS
    t_fmt, t_hooks, t_hindi = 0.9, 2.1, 3.3
    for i in range(n):
        t = i / FPS; f = ground()
        place_text(f, "p5-l1", "ONE DIRECTION.", FH, T["h2_size"], FG, SX, SY, beat, role="display")
        place_text(f, "p5-l2", "MORE TO TEST.", FH, T["h2_size"], FG, SX, SY + T["h2_size"] + XS, beat, role="display")
        my = SY + 2 * (T["h2_size"] + XS) + MD
        f.alpha_composite(alpha_mul(mcard, ease(t / 0.35)), (SX - mpad, my - mpad))
        a = ease((t - t_fmt) / 0.4)
        if a > 0:
            place_text(f, "p5-fmt-label", "4 FORMATS", FM, T["small_size"], MUTED, rx, SY, beat, alpha=a, check=a >= 1)
            x = rx
            for (cim, cp), im in zip(fcards, fmts):
                f.alpha_composite(alpha_mul(cim, a), (x - cp, y_fmt + (fh - im.height) - cp)); x += im.width + SM
        a = ease((t - t_hooks) / 0.4)
        if a > 0:
            place_text(f, "p5-hooks-label", "6 HOOKS", FM, T["small_size"], MUTED, rx, y_fmt + fh + MD, beat, alpha=a, check=a >= 1)
            for j, ((cim, cp), im) in enumerate(zip(hcards, hooks)):
                gx = rx + (j % 3) * (hw + SM); gy = y_hooks + (j // 3) * (hh + SM)
                f.alpha_composite(alpha_mul(cim, a), (gx - cp, gy - cp))
        a = ease((t - t_hindi) / 0.4)
        if a > 0:
            hx = rx + grid_w + MD
            place_text(f, "p5-hindi-label", "ENGLISH + HINDI", FM, T["small_size"], MUTED, hx, y_fmt + fh + MD, beat, alpha=a, check=a >= 1)
            f.alpha_composite(alpha_mul(hcard, a), (hx - hpad, y_hooks - hpad))
        w.add(f, key="07-proof5" if abs(t - 4.6) < 0.02 else None)


def beat_speed(w: Writer, dur=4.5):
    """00:44.8 STANDARD / 24 HOURS (2.6 s) → 4-HOUR EXPRESS + small line (2.4 s). Standard first, always."""
    n = int(dur * FPS); beat = "speed"; cut = 2.6
    for i in range(n):
        t = i / FPS; f = ground()
        if t < cut:
            a = ease(t / 0.35); y = int(H * 0.30)
            place_text(f, "std", "STANDARD", FM, T["body_size"], MUTED, SX, y, beat, alpha=a, check=a >= 1)
            place_text(f, "24h", "24 HOURS", FH, T["giant_size"], FG, SX, y + T["body_size"] + SM, beat, alpha=a, check=a >= 1, role="display")
        else:
            a = ease((t - cut) / 0.35); y = int(H * 0.33)
            xs = D.fit_size(["4-HOUR EXPRESS"], FH, [144, 136, 128, 120, 112], W - 2 * SX, 96); xw, xh = D.measure("4-HOUR EXPRESS", FH, xs)
            place_text(f, "4h", "4-HOUR EXPRESS", FH, xs, FG, SX, y, beat, alpha=a, check=a >= 1, role="display")
            rule = Image.new("RGBA", (int(xw * 0.22), 10), A._hex_to_rgba(ACC, int(255 * a))); f.alpha_composite(rule, (SX, y + xh + SM))
            place_text(f, "4h-sub", "eligible smaller packs · paid add-on", FR, T["body_size"], MUTED, SX, y + xh + SM + 10 + MD, beat, alpha=a, check=a >= 1)
        w.add(f, key="08-speed-a" if abs(t - 1.5) < 0.02 else ("08-speed-b" if abs(t - 4.0) < 0.02 else None))


def beat_human(w: Writer, dur=2.6):
    """The person behind the work: Vaibhav's photo, HUMAN-DIRECTED., one line. Between speed and the CTA."""
    n = int(dur * FPS); beat = "human"; size = 400
    tile, tpad = card(portrait_tile(size), "human-portrait", beat)
    D.REPORT["crop"].append({"id": "human-portrait", "beat": beat, "source": "vaibhav-cutout.png", "fit": "contain(cutout)", "fraction_shown": 1.0})
    px, py = SX, (H - size) // 2; tx = px + size + LG
    for i in range(n):
        t = i / FPS; f = ground(); a = ease(t / 0.35)
        f.alpha_composite(alpha_mul(tile, a), (px - tpad, py - tpad))
        aa = ease((t - 0.25) / 0.35); y = int(H * 0.36)
        place_text(f, "human-h", "HUMAN-DIRECTED.", FH, T["h2_size"], FG, tx, y, beat, alpha=aa, check=aa >= 1, role="display"); y += T["h2_size"] + SM
        for j, l in enumerate(D.wrap("Vaibhav checks every file before it reaches you.", FM, T["body_size"], W - SX - tx, 2)):
            place_text(f, f"human-l{j}", l, FM, T["body_size"], FG, tx, y, beat, alpha=aa, check=aa >= 1); y += T["body_size"] + XS
        y += SM
        place_text(f, "human-name", "Vaibhav Chawla", FR, T["small_size"], MUTED, tx, y, beat, alpha=aa, check=aa >= 1)
        w.add(f, key="08b-human" if abs(t - 1.5) < 0.02 else None)


def beat_cta(w: Writer, dur=5.0):
    """00:49.8 CTA with the master static as a restrained anchor and the speaker bubble; Adwisely once."""
    n = int(dur * FPS); beat = "cta"
    anchor = contain(MASTER["4x5"], 500, 560, "cta-anchor", beat, "aarohi-master-4x5.png"); acard, apad = card(anchor, "cta-anchor-card", beat)
    ax = W - SX - anchor.width; ay = SY
    l1 = ["SEND YOUR PRODUCT", "LINK + OFFER."]
    assert all(D.measure(l, FH, T["cta_size"])[0] <= ax - LG - SX for l in l1)
    l2 = D.wrap("GET A STRAIGHT PRICE FOR THE FIRST TEST PACK.", FM, T["body_size"], ax - LG - SX, 2)
    for i in range(n):
        t = i / FPS; f = ground(); a = ease(t / 0.35)
        f.alpha_composite(alpha_mul(acard, a), (ax - apad, ay - apad))
        y = int(H * 0.22)
        for j, l in enumerate(l1):
            aa = ease((t - 0.2 - j * 0.15) / 0.35); place_text(f, f"cta-{j}", l, FH, T["cta_size"], FG, SX, y, beat, alpha=aa, check=aa >= 1, role="display"); y += T["cta_size"] + XS
        y += SM
        for j, l in enumerate(l2):
            aa = ease((t - 0.7 - j * 0.15) / 0.35); place_text(f, f"cta2-{j}", l, FM, T["body_size"], FG, SX, y, beat, alpha=aa, check=aa >= 1); y += T["body_size"] + XS
        aa = ease((t - 1.3) / 0.4)
        fw, fhh = D.measure("AI-GENERATED · HUMAN-DIRECTED · CUSTOM PER ORDER", FR, T["small_size"]); fy = H - SY - fhh
        place_text(f, "footer", "AI-GENERATED · HUMAN-DIRECTED · CUSTOM PER ORDER", FR, T["small_size"], MUTED, SX, fy, beat, alpha=aa, check=aa >= 1)
        mw, mh = D.measure("Adwisely", T["font_mark"], 44)
        place_text(f, "adwisely", "Adwisely", T["font_mark"], 44, FG, BUBBLE_POS_R[0] - MD - mw, H - SY - mh, beat, alpha=aa, check=aa >= 1)
        draw_bubble(f, ease((t - 0.4) / 0.4), BUBBLE_POS_R)
        if t > dur - 0.7:
            f = Image.blend(f, ground(), ease((t - (dur - 0.7)) / 0.7))
        w.add(f, key="09-cta" if abs(t - 3.0) < 0.02 else None)


def main(out_dir: str):
    out = Path(out_dir); seg = out / "seg"; seg.mkdir(parents=True, exist_ok=True)
    order = []; keys = {}

    def run(name, fn, **kw):
        w = Writer(seg / f"{name}.mp4"); fn(w, **kw); d = w.close(); order.append((name, seg / f"{name}.mp4", d)); keys.update(w.keyframes); print(f"{name:12s} {d:5.2f} s")

    run("b1-speaker", beat_speaker); run("b2-handoff", beat_handoff); run("b3-proof1", beat_proof1); run("b4-proof2", beat_proof2)
    run("b5-proof3", beat_proof3); run("b6-proof4", beat_proof4); run("b6b-kora", beat_kora); run("b7-proof5", beat_proof5); run("b8-speed", beat_speed); run("b8b-human", beat_human); run("b9-cta", beat_cta)
    lst = out / "concat.txt"; lst.write_text("".join(f"file '{p.resolve()}'\n" for _, p, _ in order))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-an", "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", str(FPS), str(out / "video.mp4")], check=True)
    starts = {}; t = 0.0
    for name, _, d in order:
        starts[name] = round(t, 3); t += d
    (out / "timeline.json").write_text(json.dumps({"starts": starts, "total_s": round(t, 3), "fps": FPS}, indent=1))
    qa = V4 / "qa"; D.write_reports(qa)
    ks = sorted(keys.items()); cols = 3; th = 360; rows = (len(ks) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 640, rows * th), "white")
    for i, (k, im) in enumerate(ks):
        sheet.paste(im.resize((640, th)), ((i % cols) * 640, (i // cols) * th))
    sheet.save(qa / "contact-sheet-key-beats.jpg", quality=88)
    print("total", round(t, 2), "s")


if __name__ == "__main__":
    main(sys.argv[1])
