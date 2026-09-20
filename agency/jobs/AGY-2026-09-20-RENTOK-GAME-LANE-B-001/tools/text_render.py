#!/usr/bin/env python3
"""Exact text by code (mechanism B, RR-1) for AGY-2026-09-20-RENTOK-GAME-LANE-B-001. USD 0, local only.

hb-view shapes each copy-deck string (font FILE + face INDEX, --unicodes, transparent ground) — the invocation is the
reference kit's `render()` (tools/reference-kit/overlay_text_video.py), which is the renderer behind RR-1 (4/4). Pillow
places the glyph raster on an opaque plate with a tokenised inset (READABILITY_MARGIN candidate). Every placed string is
checked by the runtime gates: check_text_bounds (canvas + the Meta safe box), check_contrast (against the opaque backing),
check_geometry (one DesignTokens source). Two-line wraps keep the cap height (STACK_LEVEL_FIT candidate); nothing shrinks.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO))
from runtime.compositor.gates import check_contrast, check_text_bounds, check_geometry, check_disjoint, card_geometry, LayoutRefused  # noqa: E402
from runtime.compositor.tokens import DesignTokens  # noqa: E402

W, H = 1080, 1920
SAFE = (65, 269, 1015, 1248)            # Meta 14 % top / 35 % bottom / 6 % sides on 1080x1920 (Stage 2 §2.2)
TOKENS = DesignTokens(card_radius=18, card_border_px=4, card_shadow=(0, 0, 0), safe_x=65, safe_y=269,
                      spacing=(12, 24, 48, 96), min_gap_px=12, source="tools/text_render.py TOKENS")
FONTS = {
    "bold": ("/System/Library/Fonts/HelveticaNeue.ttc", 1),
    "cond-bold": ("/System/Library/Fonts/HelveticaNeue.ttc", 4),
    "medium": ("/System/Library/Fonts/HelveticaNeue.ttc", 10),
}
INSET = TOKENS.spacing[1]               # 24 px visual inset from the plate edge
_cache: dict = {}


def unicodes(text: str) -> str:
    return ",".join(f"U+{ord(c):04X}" for c in text)


def glyphs(text: str, face: str = "cond-bold", size: int = 60, colour: str = "FFFFFF") -> Image.Image:
    """hb-view -> RGBA glyph raster (transparent ground). Cached per (text, face, size, colour)."""
    key = (text, face, size, colour)
    if key in _cache:
        return _cache[key]
    file, idx = FONTS[face]
    out = HERE.parent / "gen" / "text" / f"{abs(hash(key)) & 0xFFFFFFFF:08x}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["hb-view", file, f"--face-index={idx}", f"--unicodes={unicodes(text)}", f"--font-size={size}",
                        "--margin=4", "--background=00000000", f"--foreground={colour.upper()}FF", "-O", "png", "-o", str(out)],
                       capture_output=True, text=True)
    if r.returncode != 0 or not out.exists():
        sys.exit(f"hb-view failed for {text!r}: {r.stderr[:200]}")
    im = Image.open(out).convert("RGBA")
    # crop to the ink box so the measured bounds are the ink, not the margin
    bbox = im.getchannel("A").getbbox()
    im = im.crop(bbox) if bbox else im
    _cache[key] = im
    return im


def plate(lines: list[str], *, face="cond-bold", size=60, colour="FFFFFF", backing="101528", alpha=235,
          border="FFFFFF", radius=None, inset=INSET, line_gap=None, id_="text", role=None) -> tuple[Image.Image, dict]:
    """An opaque plate carrying one or two centred lines. Returns (RGBA image, gate report). The plate is opaque enough
    that contrast is measured against the backing colour (alpha >= 235 ~ 92 %: the gate treats < 1.0 as NOT opaque, so
    the ratio is measured with backing_alpha=1.0 only when alpha == 255; otherwise we sample the composited pixels)."""
    radius = TOKENS.card_radius if radius is None else radius
    gap = line_gap if line_gap is not None else size // 4
    gl = [glyphs(t, face, size, colour) for t in lines]
    tw = max(g.width for g in gl); th = sum(g.height for g in gl) + gap * (len(gl) - 1)
    pw, ph = tw + 2 * inset, th + 2 * inset
    im = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    bg = tuple(int(backing[i:i + 2], 16) for i in (0, 2, 4)) + (alpha,)
    d.rounded_rectangle([0, 0, pw - 1, ph - 1], radius=radius, fill=bg,
                        outline=tuple(int(border[i:i + 2], 16) for i in (0, 2, 4)) + (alpha,), width=TOKENS.card_border_px)
    y = inset
    boxes = []
    for g in gl:
        x = (pw - g.width) // 2
        im.alpha_composite(g, (x, y))
        boxes.append((x, y, x + g.width, y + g.height))
        y += g.height + gap
    role = role or ("display" if size >= TOKENS.display_threshold_px else "body")
    # contrast against the backing (opaque at alpha 255; else the worst composited pixel behind the ink)
    if alpha >= 255:
        c = check_contrast("#" + colour, [], role=role, backing_hex="#" + backing, backing_alpha=1.0, tokens=TOKENS, id_=id_)
    else:
        # sample luminance of the backing blended over black and over white (the two extremes any world pixel can be)
        from runtime.compositor.gates import relative_luminance
        a = alpha / 255.0
        samples = []
        for under in (0, 255):
            blended = tuple(int(round(a * ch + (1 - a) * under)) for ch in bg[:3])
            samples.append(relative_luminance("#%02X%02X%02X" % blended))
        c = check_contrast("#" + colour, samples, role=role, tokens=TOKENS, id_=id_)
    geo = check_geometry([card_geometry(TOKENS, id_=id_)], TOKENS)
    return im, {"id": id_, "lines": lines, "size": size, "plate": (pw, ph), "ink_boxes": boxes, "contrast": c, "geometry": geo["status"]}


def check_placement(box: tuple, id_: str) -> dict:
    """Bounds gate: the ink/plate box must be inside the canvas AND the Meta safe box."""
    return check_text_bounds(box, canvas=(0, 0, W, H), container=SAFE, tokens=TOKENS, id_=id_)


def wordmark(height: int) -> Image.Image:
    src = HERE.parent / "source" / "brand" / "rentok-new-logo.webp"
    im = Image.open(src).convert("RGBA")
    w = int(im.width * height / im.height)
    return im.resize((w, height), Image.LANCZOS)


if __name__ == "__main__":
    im, rep = plate(["LEFT WITHOUT", "PAYING"], size=60)
    print(rep)
    im2, rep2 = plate(["CHEAT CODE:", "INSTALL RENTOK"], size=72, backing="0239FF", alpha=255, border="03FFF1")
    print(rep2)
    print(check_placement((100, 700, 100 + im.width, 700 + im.height), "demo"))
