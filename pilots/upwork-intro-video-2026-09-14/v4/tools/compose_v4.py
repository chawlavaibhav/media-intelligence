#!/usr/bin/env python3
"""Deterministic composition for V3: every glyph via hb-view from an explicit font file (Helvetica Neue / Didot /
Kohinoor Devanagari), every string from plan/COPY-DECK-v3.yaml. No model writes a word."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
V3 = HERE.parent
sys.path.insert(0, str(V3.parent / "tools"))
import adcomp as A  # noqa: E402  (V2's hb-view text rasteriser + primitives, reused as a library)

DECK = yaml.safe_load((V3.parent / "v3" / "plan/COPY-DECK-v3.yaml").read_text())
USED: set[str] = set()
FORMATS = {"4x5": (1080, 1350), "1x1": (1080, 1080), "9x16": (1080, 1920), "wa": (800, 800), "16x9": (1920, 1080)}

# wrapper palette (frozen)
GROUND, INK, ACCENT = "#F3EFE7", "#111111", "#FF5A3C"
# invented-brand palettes (the ads are NOT forced into the wrapper palette)
AAROHI = dict(primary="#1F4B3F", accent="#D9A441", cream="#F4EFE6")
KORA = dict(ink="#F6E7D3", accent="#E8A33D", deep="#4A1421")
DHABA = dict(cream="#F7EFE2", accent="#E9B44C")


def T(s: str, font: str, size: int, colour: str, alpha: int = 255) -> Image.Image:
    USED.add(s)
    return A.text(s, font, size, colour, alpha)


def tracked(s: str, font: str, size: int, colour: str, track: float = 0.08, alpha: int = 255) -> Image.Image:
    """Letter-spaced caps (poster register). Rendered per glyph via hb-view, then laid out with extra tracking."""
    glyphs = [A.text(ch, font, size, colour, alpha) if ch != " " else None for ch in s]
    space = int(size * 0.32); gap = int(size * track)
    w = sum((g.width + gap) if g else space for g in glyphs)
    h = max(g.height for g in glyphs if g)
    im = Image.new("RGBA", (max(1, w), h), (0, 0, 0, 0)); x = 0
    for g in glyphs:
        if g is None:
            x += space; continue
        A.paste(im, g, x, h - g.height); x += g.width + gap
    return im


def wrap2(s: str, font: str, size: int, max_w: int) -> list[str]:
    """Break a headline into at most two balanced lines that fit max_w (never orphan a single word)."""
    if A.text_width(s, font, size) <= max_w:
        return [s]
    words = s.split(); best = None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        wa, wb = A.text_width(a, font, size), A.text_width(b, font, size)
        if wa <= max_w and wb <= max_w:
            score = abs(wa - wb)
            if best is None or score < best[0]:
                best = (score, [a, b])
    return best[1] if best else [s]


def cover(plate: Image.Image, W: int, H: int, ax: float = 0.5, ay: float = 0.5) -> Image.Image:
    pw, ph = plate.size; s = max(W / pw, H / ph)
    nw, nh = int(pw * s + 0.5), int(ph * s + 0.5)
    p = plate.resize((nw, nh), Image.LANCZOS)
    x0 = int((nw - W) * ax); y0 = int((nh - H) * ay)
    return p.crop((x0, y0, x0 + W, y0 + H))


def alpha_mul(im: Image.Image, a: float) -> Image.Image:
    if a >= 1:
        return im
    im2 = im.copy(); im2.putalpha(im2.getchannel("A").point(lambda v: int(v * max(0.0, a)))); return im2


# --------------------------------------------------------------------------- AAROHI: The Ledge (approved layout)

def aarohi(plate: Image.Image, fmt: str = "4x5", variant: str | None = None, hindi: bool = False,
           build: float = 1.0, anchor=(0.5, 0.5), cta: str | None = None, _shrink: float = 1.0) -> Image.Image:
    """Compose; if the stack (pill, headline, code, button) does not clear the legal line, retry with a smaller headline."""
    for k in range(12):
        im, ok = _aarohi(plate, fmt, variant, hindi, build, anchor, cta, 1.0 - 0.07 * k)
        if ok:
            return im
    raise RuntimeError(f"aarohi {fmt}: stack does not fit even at the smallest headline")


def _aarohi(plate, fmt, variant, hindi, build, anchor, cta, shrink):
    """One approved layout; every other rendition is a code-only copy/format change.
    build in [0,1] reveals elements in hierarchy order (plate, panel, pill, headline, code, legal+mark)."""
    W, H = FORMATS[fmt]; D = DECK["aarohi"]; B = AAROHI
    is_wa = fmt == "wa"
    seam = {"4x5": 0.60, "1x1": 0.54, "9x16": 0.58, "wa": 0.54}[fmt]
    ui_bot = int(H * 0.10) if fmt == "9x16" else 0
    plate_h = int(H * seam); m = int(W * 0.07)
    canvas = Image.new("RGBA", (W, H), A._hex_to_rgba(B["primary"]))
    A.paste(canvas, cover(plate, W, plate_h, *anchor), 0, 0)
    sh = Image.new("RGBA", (W, 40), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle([0, 0, W, 12], fill=(0, 0, 0, 60))
    A.paste(canvas, sh.filter(ImageFilter.GaussianBlur(10)), 0, plate_h - 24)
    if build < 0.15:
        return canvas
    A.paste(canvas, Image.new("RGBA", (W, H - plate_h), A._hex_to_rgba(B["primary"])), 0, plate_h)
    disp, txt, bold = ("dev_bold", "dev_regular", "dev_semibold") if hindi else ("didot", "hn", "hn_medium")
    hl = int(W * (0.19 if variant is None else 0.078)) if not is_wa else int(W * (0.21 if variant is None else 0.088))
    if fmt == "9x16":
        hl = int(hl * 1.35)
    hl = int(hl * shrink)
    if hindi:
        eyebrow, headline, code, legal = D["hindi"]["eyebrow"], D["hindi"]["headline"], D["hindi"]["code"], D["hindi"]["legal"]
    else:
        eyebrow = D["eyebrow"] if variant is None else D["hook_pill"]
        headline = D["headline"] if variant is None else variant
        code, legal = D["code"], D["legal"]
    pill = A.pill(eyebrow, bold if not hindi else "dev_semibold", int(W * 0.033), B["accent"], B["primary"])
    if build >= 0.30:
        A.paste(canvas, pill, m, plate_h - pill.height // 2)
    y = plate_h + pill.height // 2 + int(W * 0.045 * shrink)
    maxw = W - 2 * m - int(W * 0.05)          # never let a headline kiss the panel edge
    lines = [headline] if variant is None else wrap2(headline, disp, hl, maxw)
    while variant is not None and any(A.text_width(l, disp, hl) > maxw for l in lines) and hl > 30:
        hl -= 2; lines = wrap2(headline, disp, hl, maxw)
    if variant is None:
        while A.text_width(headline, disp, hl) > maxw:
            hl -= 4
    USED.add(headline)
    if build >= 0.45:
        for l in lines:
            g = A.text(l, disp, hl, B["cream"]); A.paste(canvas, g, m, y); y += int(hl * 1.08)
    else:
        y += int(hl * 1.08) * len(lines)
    y += int(W * 0.03 * shrink)
    if build >= 0.60:
        g = T(code, bold, int(W * 0.040), B["accent"]); A.paste(canvas, g, m, y); y += g.height + int(W * 0.035 * shrink)
    if cta and build >= 0.75:
        btn = A.button(cta, bold if not hindi else "dev_semibold", int(W * 0.034), B["accent"], B["primary"], min_w=int(W * 0.30))
        A.paste(canvas, btn, m, y); y += btn.height
    leg = T(legal, txt, max(18, int(W * 0.022)), B["cream"], alpha=165)
    mark = T(D["brand"], "didot", int(W * 0.040), B["cream"])
    ly = H - ui_bot - int(W * 0.06)
    ok = y + int(W * 0.03) <= ly - leg.height
    if build >= 0.85:
        A.paste(canvas, leg, m, ly - leg.height)
        A.paste(canvas, mark, W - m - mark.width, ly - mark.height)
    return canvas, ok


# --------------------------------------------------------------------------- KORA: poster register (type over picture)

def kora(base: Image.Image, fmt: str, hook: str, anchor=(0.45, 0.5), build: float = 1.0) -> Image.Image:
    """16:9: poster register, type in the wall's negative space. Square/vertical crops have no reliable empty wall, so the
    type sits on a solid oxblood panel below the picture — never over the garment."""
    W, H = FORMATS[fmt]; K = KORA
    if fmt == "16x9":   # editorial split: picture left 62 %, solid oxblood panel right; type only on the panel
        pw = int(W * 0.62); canvas = Image.new("RGBA", (W, H), A._hex_to_rgba(K["deep"]))
        A.paste(canvas, cover(base, pw, H, 0.30, 0.5), 0, 0)
        px = pw + int(W * 0.045); maxw = W - px - int(W * 0.045); size = int(W * 0.040)
        lines = wrap2(hook, "didot", size, maxw)
        while any(A.text_width(l, "didot", size) * 1.1 > maxw for l in lines) and size > 24:
            size -= 2; lines = wrap2(hook, "didot", size, maxw)
        USED.add(hook); glyphs = [tracked(l, "didot", size, K["ink"], 0.10) for l in lines]
        block = int(size * 0.7) + max(3, size // 12) + sum(int(size * 1.25) for _ in glyphs)
        y = (H - block) // 2 - int(H * 0.04)
        rule = Image.new("RGBA", (int(W * 0.05), max(3, size // 12)), A._hex_to_rgba(K["accent"]))
        A.paste(canvas, rule, px, y); y += rule.height + int(size * 0.7)
        for g in glyphs:
            A.paste(canvas, g, px, y); y += int(size * 1.25)
        USED.add(DECK["kora"]["brand"]); mark = tracked(DECK["kora"]["brand"], "hn_medium", int(W * 0.016), K["ink"], 0.28)
        A.paste(canvas, mark, W - int(W * 0.045) - mark.width, H - int(H * 0.08) - mark.height)
        return canvas
    seam = {"4x5": 0.64, "1x1": 0.60, "9x16": 0.62, "wa": 0.60}[fmt]; ph = int(H * seam)
    ui_bot = int(H * 0.10) if fmt == "9x16" else 0
    canvas = Image.new("RGBA", (W, H), A._hex_to_rgba(K["deep"]))
    A.paste(canvas, cover(base, W, ph, *anchor), 0, 0)
    m = int(W * 0.08); maxw = W - 2 * m - int(W * 0.05)
    size = int(W * (0.064 if fmt != "wa" else 0.07))
    lines = wrap2(hook, "didot", size, maxw)
    while any(A.text_width(l, "didot", size) * 1.1 > maxw for l in lines) and size > 24:
        size -= 2; lines = wrap2(hook, "didot", size, maxw)
    USED.add(hook); glyphs = [tracked(l, "didot", size, K["ink"], 0.10) for l in lines]
    y = ph + int(H * 0.05)
    rule = Image.new("RGBA", (int(W * 0.08), max(3, size // 12)), A._hex_to_rgba(K["accent"]))
    A.paste(canvas, rule, m, y); y += rule.height + int(size * 0.7)
    for g in glyphs:
        A.paste(canvas, g, m, y); y += int(size * 1.25)
    USED.add(DECK["kora"]["brand"]); mark = tracked(DECK["kora"]["brand"], "hn_medium", int(W * 0.024), K["ink"], 0.28)
    my = H - ui_bot - int(H * 0.06) - mark.height
    assert y + int(size * 0.4) <= my, f"kora {fmt}: headline runs into the wordmark"
    A.paste(canvas, mark, W - m - mark.width, my)
    return canvas


# --------------------------------------------------------------------------- DHABA 47: Hindi offer over the flat-lay

def dhaba(base: Image.Image, fmt: str = "4x5", anchor=(0.5, 0.5), build: float = 1.0) -> Image.Image:
    W, H = FORMATS[fmt]; Dd = DECK["dhaba"]; C = DHABA
    canvas = cover(base, W, H, *anchor).convert("RGBA")
    # soft dark gradient behind the copy so Devanagari stays legible on any tabletop
    grad = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(grad)
    for i in range(int(H * 0.55)):
        gd.line([(0, i), (W, i)], fill=(20, 12, 6, int(150 * (1 - i / (H * 0.55)))))
    canvas.alpha_composite(grad)
    m = int(W * 0.07); y = int(H * 0.07)
    if build >= 0.4:
        g = T(Dd["l1"], "dev_bold", int(W * 0.115), C["cream"]); A.paste(canvas, g, m, y); y += int(g.height * 1.25)
    if build >= 0.6:
        g = T(Dd["l2"], "dev_semibold", int(W * 0.062), C["accent"]); A.paste(canvas, g, m, y); y += int(g.height * 1.35)
    if build >= 0.75:
        g = T(Dd["l3"], "dev_medium", int(W * 0.046), C["cream"]); A.paste(canvas, g, m, y); y += int(g.height * 1.4)
        g = T(Dd["l4"], "dev_regular", int(W * 0.030), C["cream"], alpha=190); A.paste(canvas, g, m, y)
    if build >= 0.9:
        USED.add(Dd["brand"]); mark = tracked(Dd["brand"], "hn_medium", int(W * 0.026), C["cream"], 0.25)
        A.paste(canvas, mark, W - m - mark.width, H - int(H * 0.06) - mark.height)
    return canvas


# --------------------------------------------------------------------------- deck check

def deck_strings() -> set[str]:
    out = set()
    def walk(v):
        if isinstance(v, str): out.add(v)
        elif isinstance(v, dict): [walk(x) for x in v.values()]
        elif isinstance(v, list): [walk(x) for x in v]
    walk(DECK); return out


def deck_check(extra_allowed: set[str] = frozenset()) -> list[str]:
    off = sorted(s for s in USED if s not in deck_strings() and s not in extra_allowed)
    return off


if __name__ == "__main__":
    out = V3 / "gen/statics"; out.mkdir(parents=True, exist_ok=True)
    plate = Image.open(V3 / "gen/stills/a1-accepted.png").convert("RGBA")
    for fmt in ("4x5", "1x1", "9x16", "wa"):
        aarohi(plate, fmt, anchor=(0.62, 0.5)).convert("RGB").save(out / f"aarohi-master-{fmt}.png")
    for i, h in enumerate(DECK["aarohi"]["hooks"], 1):
        aarohi(plate, "4x5", variant=h, anchor=(0.62, 0.5)).convert("RGB").save(out / f"aarohi-hook-{i}.png")
    aarohi(plate, "4x5", hindi=True, anchor=(0.62, 0.5)).convert("RGB").save(out / "aarohi-hindi-4x5.png")
    print("off-deck:", deck_check())
