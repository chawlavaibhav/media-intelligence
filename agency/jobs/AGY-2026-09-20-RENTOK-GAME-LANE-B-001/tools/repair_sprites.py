#!/usr/bin/env python3
"""Repair round 1 (USD 0): (a) composite a code-drawn red rent register on the three character cells the model drew without it
(jump, hurt, cornered) so every pose carries every identifier — checker defect D-4; (b) replace the green tick on the drifting
ghost's price tag (O3 after-state) with a neutral cyan "tracked" ring marker so nothing reads as "paid" — checker note.
Writes new sprite files (…_reg.png / O3_after_tracked.png); the originals stay as evidence."""
from __future__ import annotations
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

JOB = Path(__file__).resolve().parent.parent
SP = JOB / "gen/sprites"


def register(w: int, h: int) -> Image.Image:
    """A red cloth-bound register seen edge-on-ish, matching the run cells' one (about 64x52 px at sheet scale)."""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=4, fill=(178, 34, 34, 255), outline=(40, 20, 20, 255), width=3)
    d.rectangle([w - 12, 4, w - 5, h - 5], fill=(235, 225, 200, 255))          # page edge
    d.line([(6, 6), (6, h - 7)], fill=(120, 20, 20, 255), width=3)             # spine
    return im


# placements (sprite-relative fractions of width/height; register box size as fraction of sprite width), chosen by eye
# against the run cells, where the register sits under the left arm at x 0.17-0.45 w, y 0.40-0.57 h
PLACE = {"jump": (0.03, 0.42, 0.30, 0.19), "hurt": (0.30, 0.44, 0.28, 0.18), "cornered": (0.04, 0.46, 0.30, 0.18)}
for name, (fx, fy, fw, fh) in PLACE.items():
    im = Image.open(SP / f"A1_{name}.png").convert("RGBA")
    W, H = im.size
    reg = register(int(W * fw), int(H * fh))
    base = Image.new("RGBA", im.size, (0, 0, 0, 0))
    base.alpha_composite(reg, (int(W * fx), int(H * fy)))
    base.alpha_composite(im)                                                     # the body stays in front of the book (as in the run cells)
    # the book must also show in front where the body is transparent, which alpha_composite handles; add the book's outer edge on top
    base.save(SP / f"A1_{name}_reg.png")
    print(name, "register composited at", (int(W * fx), int(H * fy)), reg.size)

# O3 after: green tick -> cyan ring marker
im = Image.open(SP / "O3_after.png").convert("RGBA"); a = np.asarray(im).copy()
r, g, b, al = [a[..., i].astype(int) for i in range(4)]
grn = (al > 128) & (g > 150) & (r < 120) & (b < 120)
ys, xs = np.nonzero(grn); x0, y0, x1, y1 = xs.min() - 6, ys.min() - 6, xs.max() + 6, ys.max() + 6
# fill the tick area with the tag's paper colour (sample just outside the tick), then draw the ring
paper = tuple(int(v) for v in a[y0 - 4, (x0 + x1) // 2][:3])
out = Image.fromarray(a); d = ImageDraw.Draw(out)
d.rectangle([x0, y0, x1, y1], fill=paper + (255,))
cx, cy, rr = (x0 + x1) // 2, (y0 + y1) // 2, min(x1 - x0, y1 - y0) // 2 - 2
d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=(3, 200, 190, 255), width=6)
d.ellipse([cx - rr // 3, cy - rr // 3, cx + rr // 3, cy + rr // 3], fill=(2, 57, 255, 255))
out.save(SP / "O3_after_tracked.png"); print("O3 tick replaced at", (x0, y0, x1, y1), "paper", paper)
