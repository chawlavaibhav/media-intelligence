#!/usr/bin/env python3
"""Chroma-key the magenta sheets and slice them into sprites. USD 0.
A1 (3x3 grid) -> 9 pose PNGs; A2_On (two panels) -> before/after PNGs. Key = distance from magenta in RGB with a soft edge;
1-px erosion of the matte removes fringe; the split is by column/row projection of the non-magenta mask (robust to a
divider line, which is dropped as a thin component)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
JOB = HERE.parent
OUT = JOB / "gen" / "sprites"


def key(im: Image.Image, tol: float = 90.0, soft: float = 40.0) -> Image.Image:
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    # magenta family: high R, low G, high B (the model used two magentas: #FF00FF-class and a lighter one)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    dist = np.sqrt((255 - r) ** 2 + (g) ** 2 + (255 - b) ** 2)
    # also treat "pinkish" (r>180, b>180, g<150) as background
    pink = (r > 170) & (b > 170) & (g < 150)
    alpha = np.clip((dist - tol) / soft, 0, 1)
    alpha[pink & (dist < tol + soft * 2)] = np.minimum(alpha[pink & (dist < tol + soft * 2)], 0.0)
    # erode 1 px
    m = alpha > 0.5
    er = m.copy()
    er[1:, :] &= m[:-1, :]; er[:-1, :] &= m[1:, :]; er[:, 1:] &= m[:, :-1]; er[:, :-1] &= m[:, 1:]
    alpha = alpha * er
    # despill: pull magenta out of edge pixels (reduce R and B where G is much lower)
    spill = np.clip(((r + b) / 2 - g) / 255.0 - 0.25, 0, 1) * (alpha < 0.999)
    a[..., 0] -= spill * 60; a[..., 2] -= spill * 60
    rgba = np.dstack([np.clip(a, 0, 255), alpha * 255]).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")


def components(alpha: np.ndarray, min_area: int = 400):
    """Bounding boxes of connected components of alpha>0.5 (4-connectivity), area >= min_area."""
    m = alpha > 128
    h, w = m.shape
    lab = np.zeros((h, w), np.int32); n = 0; boxes = []
    ys, xs = np.nonzero(m)
    for y0, x0 in zip(ys, xs):
        if lab[y0, x0]:
            continue
        n += 1; stack = [(y0, x0)]; lab[y0, x0] = n; area = 0; minx = maxx = x0; miny = maxy = y0
        while stack:
            y, x = stack.pop(); area += 1
            minx = min(minx, x); maxx = max(maxx, x); miny = min(miny, y); maxy = max(maxy, y)
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < h and 0 <= xx < w and m[yy, xx] and not lab[yy, xx]:
                    lab[yy, xx] = n; stack.append((yy, xx))
        if area >= min_area:
            boxes.append((minx, miny, maxx + 1, maxy + 1, area))
    return boxes


def merge_boxes(boxes, gap=30):
    """Merge boxes that overlap or sit within `gap` px (a sprite can key into several islands)."""
    boxes = [list(b[:4]) for b in boxes]
    changed = True
    while changed:
        changed = False
        out = []
        while boxes:
            b = boxes.pop()
            for i, o in enumerate(out):
                if not (b[2] + gap < o[0] or o[2] + gap < b[0] or b[3] + gap < o[1] or o[3] + gap < b[1]):
                    out[i] = [min(b[0], o[0]), min(b[1], o[1]), max(b[2], o[2]), max(b[3], o[3])]; changed = True; break
            else:
                out.append(b)
        boxes = out
    return boxes


def slice_grid(rgba: Image.Image, rows: int, cols: int, names: list[str], prefix: str) -> dict:
    """Split a sheet into a rows x cols grid by equal cells, then tighten each cell to its ink box."""
    OUT.mkdir(parents=True, exist_ok=True)
    W, H = rgba.size; cw, ch = W / cols, H / rows
    a = np.asarray(rgba)[..., 3]
    out = {}
    for r in range(rows):
        for c in range(cols):
            name = names[r * cols + c]
            x0, y0, x1, y1 = int(c * cw), int(r * ch), int((c + 1) * cw), int((r + 1) * ch)
            cell = a[y0:y1, x0:x1]
            ys, xs = np.nonzero(cell > 128)
            if len(xs) == 0:
                sys.exit(f"empty cell {name}")
            bx0, bx1, by0, by1 = x0 + xs.min(), x0 + xs.max() + 1, y0 + ys.min(), y0 + ys.max() + 1
            sp = rgba.crop((bx0, by0, bx1, by1)); p = OUT / f"{prefix}_{name}.png"; sp.save(p)
            out[name] = {"file": str(p.relative_to(JOB)), "box": [int(bx0), int(by0), int(bx1), int(by1)], "size": sp.size}
    return out


def slice_pair(rgba: Image.Image, prefix: str) -> dict:
    """Two panels: split at the widest empty column near the middle; drop thin divider lines."""
    OUT.mkdir(parents=True, exist_ok=True)
    a = np.asarray(rgba)[..., 3] > 128
    W = a.shape[1]
    col = a.sum(axis=0)
    mid = W // 2
    # search a split column in the middle 30 % with minimal ink; ignore a 1-6 px divider by allowing small ink
    lo, hi = int(W * 0.35), int(W * 0.65)
    cands = [(col[x], abs(x - mid), x) for x in range(lo, hi)]
    split = min(cands)[2]
    out = {}
    for name, (x0, x1) in (("before", (0, split)), ("after", (split, W))):
        sub = a[:, x0:x1]
        boxes = components(np.asarray(rgba)[:, x0:x1, 3], min_area=400)
        # drop divider-like components (very thin, tall)
        boxes = [b for b in boxes if not (b[2] - b[0] < 12 and b[3] - b[1] > 100)]
        if not boxes:
            sys.exit(f"no component in {prefix} {name}")
        m = merge_boxes(boxes, gap=60)
        m.sort(key=lambda b: -(b[2] - b[0]) * (b[3] - b[1]))
        # keep every merged box (a swarm of three is three boxes) but crop the union of all
        ux0, uy0 = min(b[0] for b in m), min(b[1] for b in m); ux1, uy1 = max(b[2] for b in m), max(b[3] for b in m)
        sp = rgba.crop((x0 + ux0, uy0, x0 + ux1, uy1)); p = OUT / f"{prefix}_{name}.png"; sp.save(p)
        out[name] = {"file": str(p.relative_to(JOB)), "box": [int(x0 + ux0), int(uy0), int(x0 + ux1), int(uy1)], "size": sp.size, "islands": len(m)}
    return out


if __name__ == "__main__":
    report = {}
    a1 = key(Image.open(JOB / "gen/stills/A1_character_sheet_v1.png"))
    a1.save(OUT.parent / "sprites" / "A1_keyed.png") if OUT.exists() else None
    names = ["run1", "run2", "run3", "run4", "jump", "hurt", "cornered", "powerA", "powerB"]
    report["A1"] = slice_grid(a1, 3, 3, names, "A1")
    for i in range(1, 6):
        rg = key(Image.open(JOB / f"gen/stills/A2_O{i}_v1.png"))
        report[f"O{i}"] = slice_pair(rg, f"O{i}")
    (JOB / "gen/sprites/SLICES.json").write_text(json.dumps(report, indent=1))
    for k, v in report.items():
        print(k, {n: d["size"] for n, d in v.items()})
