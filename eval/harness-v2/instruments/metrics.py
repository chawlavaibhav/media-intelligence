"""Pure-stdlib image metrics shared by the instruments: MAE, SSIM (Wang 2004 form), dHash.

    mae_rgb(a, b, outside)   mean |a - b| per channel over the pixels where outside[i] is True
    ssim_grey(a, b, outside) 8x8 non-overlapping windows (stride 8), K1 0.01, K2 0.03, L 255, mean over
                             windows whose pixels all lie outside the mask (outside=None -> every window)
    dhash(img)               9x8 greyscale difference hash, 64-bit int; hamming() between two
"""
from __future__ import annotations

import math

from . import imageio as IO

K1, K2, L = 0.01, 0.03, 255.0
C1, C2 = (K1 * L) ** 2, (K2 * L) ** 2
WIN = 8


def mae_rgb(a: IO.Image, b: IO.Image, outside: list | None = None) -> dict:
    if (a.width, a.height) != (b.width, b.height):
        raise ValueError("images differ in size; resize first")
    a3, b3 = a.to_rgb().data, b.to_rgb().data
    n = a.width * a.height
    sums = [0, 0, 0]
    count = 0
    for i in range(n):
        if outside is not None and not outside[i]:
            continue
        count += 1
        j = 3 * i
        sums[0] += abs(a3[j] - b3[j])
        sums[1] += abs(a3[j + 1] - b3[j + 1])
        sums[2] += abs(a3[j + 2] - b3[j + 2])
    if count == 0:
        return {"per_channel": None, "mean": None, "pixels": 0}
    per = [s / count for s in sums]
    return {"per_channel": per, "mean": sum(per) / 3.0, "pixels": count}


def ssim_grey(a: IO.Image, b: IO.Image, outside: list | None = None) -> dict:
    if (a.width, a.height) != (b.width, b.height):
        raise ValueError("images differ in size; resize first")
    ga, gb = a.to_grey().data, b.to_grey().data
    w, h = a.width, a.height
    vals = []
    for wy in range(0, h - WIN + 1, WIN):
        for wx in range(0, w - WIN + 1, WIN):
            idx = [(wy + y) * w + wx + x for y in range(WIN) for x in range(WIN)]
            if outside is not None and not all(outside[i] for i in idx):
                continue
            xs = [ga[i] for i in idx]
            ys = [gb[i] for i in idx]
            n = float(len(idx))
            mx, my = sum(xs) / n, sum(ys) / n
            vx = sum((v - mx) ** 2 for v in xs) / (n - 1)
            vy = sum((v - my) ** 2 for v in ys) / (n - 1)
            cov = sum((xs[i] - mx) * (ys[i] - my) for i in range(len(idx))) / (n - 1)
            vals.append(((2 * mx * my + C1) * (2 * cov + C2)) / ((mx * mx + my * my + C1) * (vx + vy + C2)))
    if not vals:
        return {"ssim": None, "windows": 0}
    return {"ssim": sum(vals) / len(vals), "windows": len(vals)}


def dhash(img: IO.Image) -> int:
    small = IO.resize_nearest(img.to_grey(), 9, 8)
    bits = 0
    d = small.data
    for y in range(8):
        for x in range(8):
            left, right = d[y * 9 + x], d[y * 9 + x + 1]
            bits = (bits << 1) | (1 if left < right else 0)
    return bits


def hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def percentile_nearest_rank(values: list, p: float) -> float | None:
    if not values:
        return None
    s = sorted(values)
    k = max(1, min(len(s), math.ceil(p * len(s))))
    return float(s[k - 1])
