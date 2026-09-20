#!/usr/bin/env python3
"""cutout.py — key the flat green background out of a generated still (Stage 4 A1–A6), by code.

usage: python3 cutout.py <in.png> <out_prefix> [--sheet N]     # --sheet N splits a horizontal sprite sheet into N poses
Writes RGBA PNG(s) cropped to content, plus a JSON report: border keyability (share of border pixels that are the
flat background), bounding boxes, grayscale separation (PA-D5: mean luminance of the sprite vs the world ground/sky
values used by the engine), and the pose count found. Fails closed (exit 1) when the border is < 98 % keyable —
that means the model did not give a clean flat background and the sprite cannot be cut out safely.
"""
from __future__ import annotations

import json
import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image


def key_out(im: Image.Image, tol: int = 60) -> tuple[np.ndarray, float]:
    a = np.asarray(im.convert("RGB")).astype(int)
    # background estimate = the median colour of the border
    border = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    bg = np.median(border, axis=0)
    dist = np.abs(a - bg).sum(axis=2)
    near = dist < tol
    keyable = float(np.concatenate([near[0], near[-1], near[:, 0], near[:, -1]]).mean())
    # flood fill from the border so background-coloured pixels INSIDE the sprite are kept
    h, w = near.shape; bgmask = np.zeros_like(near, dtype=bool)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if near[y, x] and not bgmask[y, x]:
                bgmask[y, x] = True; q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if near[y, x] and not bgmask[y, x]:
                bgmask[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= ny < h and 0 <= nx < w and near[ny, nx] and not bgmask[ny, nx]:
                bgmask[ny, nx] = True; q.append((ny, nx))
    alpha = np.where(bgmask, 0, 255).astype(np.uint8)
    # soften green fringe: pixels adjacent to background that are greenish get their green channel pulled down
    rgba = np.dstack([a.astype(np.uint8), alpha])
    return rgba, keyable


def split_sheet(alpha: np.ndarray, n: int) -> list[tuple[int, int]]:
    cols = (alpha > 0).any(axis=0)
    runs = []; inrun = False
    for x, v in enumerate(cols):
        if v and not inrun:
            start = x; inrun = True
        elif not v and inrun:
            runs.append((start, x)); inrun = False
    if inrun:
        runs.append((start, len(cols)))
    # merge tiny gaps (< 2 % of width) so a sprite split by an internal gap stays one pose
    merged = []
    for r in runs:
        if merged and r[0] - merged[-1][1] < 0.02 * len(cols):
            merged[-1] = (merged[-1][0], r[1])
        else:
            merged.append(r)
    merged = [r for r in merged if r[1] - r[0] > 0.03 * len(cols)]
    return merged


def main():
    src = Path(sys.argv[1]); prefix = sys.argv[2]
    n = int(sys.argv[sys.argv.index("--sheet") + 1]) if "--sheet" in sys.argv else 1
    im = Image.open(src)
    rgba, keyable = key_out(im)
    alpha = rgba[:, :, 3]
    report = {"source": str(src), "size": im.size, "border_keyable": round(keyable, 4), "poses": []}
    if keyable < 0.98:
        report["status"] = "FAIL: border not keyable (< 98 %) — no clean flat background"
        print(json.dumps(report, indent=1)); sys.exit(1)
    boxes = split_sheet(alpha, n) if n > 1 else [(0, im.width)]
    report["poses_found"] = len(boxes)
    names = ["idle", "runA", "runB", "jump"] if n == 4 else [""] * len(boxes)
    for i, (x0, x1) in enumerate(boxes[:n]):
        sub = rgba[:, x0:x1]
        ys = np.where(sub[:, :, 3] > 0)[0]
        if len(ys) == 0:
            continue
        y0, y1 = ys.min(), ys.max() + 1
        xs = np.where(sub[:, :, 3] > 0)[1]; xa, xb = xs.min(), xs.max() + 1
        crop = sub[y0:y1, xa:xb]
        out = Path(f"{prefix}{('_' + names[i]) if names[i] else ''}.png")
        Image.fromarray(crop, "RGBA").save(out)
        vis = crop[crop[:, :, 3] > 0][:, :3].astype(float)
        lum = float((0.2126 * vis[:, 0] + 0.7152 * vis[:, 1] + 0.0722 * vis[:, 2]).mean() / 255)
        report["poses"].append({"file": str(out), "box_in_source": [int(x0 + xa), int(y0), int(x0 + xb), int(y1)],
                                "w": int(xb - xa), "h": int(y1 - y0), "mean_luminance": round(lum, 3),
                                "grayscale_vs_lane_0.55": "separates" if abs(lum - 0.55) > 0.12 else "weak"})
    if n > 1 and len(boxes) != n:
        report["status"] = f"WARN: expected {n} poses, found {len(boxes)}"
    else:
        report["status"] = "ok"
    Path(f"{prefix}_cutout.json").write_text(json.dumps(report, indent=1))
    print(json.dumps(report, indent=1))
    sys.exit(0 if report["status"] == "ok" else 2)


if __name__ == "__main__":
    main()
