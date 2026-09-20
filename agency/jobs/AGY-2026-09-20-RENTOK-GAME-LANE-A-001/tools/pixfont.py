#!/usr/bin/env python3
"""pixfont.py — an original 5x7 bitmap capitals font defined in code, for every exact string in this job.

Why a code font: (1) no download and no licence question (the glyphs below are written for this job);
(2) rendering is byte-exact by construction — each character maps to one glyph, so the exact-copy check is a
string comparison on the copy deck plus a glyph-coverage check; (3) nearest-neighbour scaling gives the
arcade look the brief asks for at any size. Latin capitals, digits, and the punctuation the copy deck uses.
Devanagari is NOT covered (this job's copy is English; a Hindi string would go through hb-view + Pillow).

Run `python3 pixfont.py audition <out.png>` to render the longest copy-deck lines at final scale inside the
Stage-2 safe box (USD 0). `python3 pixfont.py coverage <copy-deck.json>` lists any character with no glyph.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

W, H = 5, 7  # glyph cell (columns x rows); 1 column of spacing added between glyphs

_G = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "J": ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "10001", "11001", "10101", "10011", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11111", "00010", "00100", "00010", "00001", "10001", "01110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    ".": ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    ",": ["00000", "00000", "00000", "00000", "01100", "00100", "01000"],
    "!": ["00100", "00100", "00100", "00100", "00100", "00000", "00100"],
    "?": ["01110", "10001", "00001", "00010", "00100", "00000", "00100"],
    "-": ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    "&": ["01100", "10010", "10100", "01000", "10101", "10010", "01101"],
    "/": ["00001", "00010", "00010", "00100", "01000", "01000", "10000"],
    ":": ["00000", "01100", "01100", "00000", "01100", "01100", "00000"],
    "'": ["00100", "00100", "01000", "00000", "00000", "00000", "00000"],
    "+": ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
    "✓": ["00000", "00001", "00011", "10110", "11100", "01000", "00000"],
    "▮": ["11111", "11111", "11111", "11111", "11111", "11111", "11111"],
    "▯": ["11111", "10001", "10001", "10001", "10001", "10001", "11111"],
    "♥": ["01010", "11111", "11111", "11111", "01110", "00100", "00000"],
    "♡": ["01010", "10101", "10001", "10001", "01010", "00100", "00000"],
    "₹": ["11111", "00100", "11111", "01000", "00100", "00010", "00001"],
}


def glyph(ch: str):
    return _G.get(ch.upper())


def missing(text: str) -> list[str]:
    return sorted({c for c in text if glyph(c) is None})


def measure(text: str, scale: int) -> tuple[int, int]:
    n = len(text)
    return (n * W + (n - 1)) * scale, H * scale


def render(text: str, scale: int, fg=(255, 255, 255), bg=None, pad: int = 0) -> Image.Image:
    """Nearest-neighbour bitmap render. Raises on a character with no glyph (fail closed, never a blank)."""
    miss = missing(text)
    if miss:
        raise ValueError(f"no glyph for {miss!r} in {text!r}")
    w, h = measure(text, scale)
    im = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), bg or (0, 0, 0, 0))
    px = im.load()
    x0 = pad
    for ch in text:
        rows = glyph(ch)
        for r, row in enumerate(rows):
            for c, bit in enumerate(row):
                if bit == "1":
                    for dy in range(scale):
                        for dx in range(scale):
                            px[x0 + c * scale + dx, pad + r * scale + dy] = (*fg, 255)
        x0 += (W + 1) * scale
    return im


def draw_text(canvas: Image.Image, xy, text: str, scale: int, fg=(255, 255, 255), shadow=None) -> tuple[int, int, int, int]:
    """Paste text at xy; optional 1-scale drop shadow. Returns the ink box (x0,y0,x1,y1) on the canvas."""
    x, y = xy
    if shadow is not None:
        canvas.alpha_composite(render(text, scale, fg=shadow), (x + scale, y + scale))
    im = render(text, scale, fg=fg)
    canvas.alpha_composite(im, (x, y))
    return (x, y, x + im.width, y + im.height)


SAFE = (65, 288, 888, 1248)  # Stage 2.2 intersection at 1080x1920


def audition(out: Path) -> None:
    """Render the longest copy-deck lines at the planned scales inside the safe box, over a mid-grey ground."""
    cv = Image.new("RGBA", (1080, 1920), (70, 90, 120, 255))
    d = ImageDraw.Draw(cv)
    d.rectangle(SAFE, outline=(255, 0, 0, 255), width=3)
    y = SAFE[1] + 12
    lines = [
        ("HUD scale 6", "PG OWNER ▮▮▮▯▯  LEVEL 1", 6, (255, 255, 255)),
        ("obstacle label scale 7", "TENANT VERIFICATION", 7, (255, 241, 0)),
        ("obstacle label scale 7", "LEFT WITHOUT PAYING", 7, (255, 241, 0)),
        ("cheat code line scale 10", "INSTALL", 10, (3, 255, 241)),
        ("cheat code line scale 10", "RENTOK APP", 10, (3, 255, 241)),
        ("checklist chip scale 6", "✓ DUES TRACKED LIVE", 6, (48, 181, 2)),
        ("checklist chip scale 6", "✓ COMPLAINT TICKETS", 6, (48, 181, 2)),
        ("CTA line scale 10", "INSTALL", 10, (255, 255, 255)),
        ("CTA line scale 10", "RENTOK APP", 10, (255, 255, 255)),
        ("URL scale 7", "RENTOK.COM", 7, (255, 255, 255)),
    ]
    for label, text, sc, fg in lines:
        w, h = measure(text, sc)
        x = SAFE[0] + (SAFE[2] - SAFE[0] - w) // 2
        box = draw_text(cv, (x, y), text, sc, fg=fg, shadow=(0, 0, 0))
        inside = box[0] >= SAFE[0] and box[2] <= SAFE[2] and box[1] >= SAFE[1] and box[3] <= SAFE[3]
        print(f"{label:24s} {text!r:26s} ink {w}x{h}px  fits_safe={inside}")
        y += h + 46
    cv.convert("RGB").save(out)
    print("wrote", out)


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "audition":
        audition(Path(sys.argv[2]))
    elif len(sys.argv) >= 3 and sys.argv[1] == "coverage":
        deck = json.load(open(sys.argv[2]))
        bad = {}
        for k, v in deck.get("strings", {}).items():
            m = missing(v) if isinstance(v, str) else []
            if m:
                bad[k] = m
        print("missing glyphs:", bad or "none")
        sys.exit(1 if bad else 0)
    else:
        print(__doc__)
