"""Q1 flat-colour geometry detector (stdlib only). THE METHOD IS FROZEN BY THE TASK (§4.3).

    decode PNG (imageio, fail closed) -> classify every pixel to the nearest of the five fixture colours
    if within T_rgb (Euclidean, sRGB 8-bit) else background (white and the grey shadow trap are
    background) -> 4-connected components -> count, bounding boxes (centres for left_of / right_of /
    above / below and the quadrant, areas for `larger`), shape by fill ratio (square ~ 1.0,
    circle ~ pi/4, bar by aspect). A corrupt PNG raises ProbeError.

Every number that shapes an answer is in CONFIG and covered by config_hash(); the same code at a
different T_rgb is a different instrument (FAMILY-2 gate: "detector confidence recorded").
"""
from __future__ import annotations

import hashlib
import json
import math

from instruments import imageio as IO

ProbeError = IO.ProbeError

CONFIG = {
    "detector": "hv2-q1-flat-colour-cc",
    "version": "0.1.0",
    "palette_srgb": {"red": [220, 40, 40], "blue": [40, 80, 220], "green": [40, 170, 70], "yellow": [240, 200, 50], "purple": [150, 60, 190]},
    "background_examples": {"white": [255, 255, 255], "grey_shadow_trap": [185, 185, 185]},
    "T_rgb": 30,                          # Euclidean distance in 8-bit sRGB; the "detector confidence" (pre-registered)
    "connectivity": 4,
    "min_component_area_px": 16,          # specks below this are ignored (none exist in the pack; declared anyway)
    "shape_rules": {"square_fill_min": 0.93, "circle_fill_min": 0.62, "circle_fill_max": 0.88, "bar_aspect_min": 1.8,
                    "square_aspect_max": 1.15, "circle_aspect_max": 1.15},
    "relation_rule": "dominant axis of the bounding-box centre offset: |dx| >= |dy| -> left_of / right_of, else above / below",
    "quadrant_rule": "bounding-box centre against the frame midlines (x < W/2 -> left, y < H/2 -> top)",
    "size_rule": "larger = the object with the larger pixel area; equal if areas are equal",
}


def config_hash() -> str:
    return hashlib.sha256(json.dumps(CONFIG, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _label_table() -> dict:
    return {name: tuple(rgb) for name, rgb in CONFIG["palette_srgb"].items()}


def classify_pixel(rgb: tuple, table: dict, t: int, cache: dict) -> str | None:
    if rgb in cache:
        return cache[rgb]
    best, bd = None, t * t + 1
    for name, ref in table.items():
        d = (rgb[0] - ref[0]) ** 2 + (rgb[1] - ref[1]) ** 2 + (rgb[2] - ref[2]) ** 2
        if d < bd:
            best, bd = name, d
    cache[rgb] = best if bd <= t * t else None
    return cache[rgb]


def detect(png_bytes: bytes) -> dict:
    img = IO.decode_png(png_bytes).to_rgb()          # ProbeError on anything unparseable
    w, h = img.width, img.height
    table = _label_table()
    t = int(CONFIG["T_rgb"])
    cache: dict = {}
    d = img.data
    labels = [None] * (w * h)
    for i in range(w * h):
        labels[i] = classify_pixel((d[3 * i], d[3 * i + 1], d[3 * i + 2]), table, t, cache)
    # 4-connected components over same-label pixels (iterative flood fill)
    comp = [-1] * (w * h)
    objects = []
    for start in range(w * h):
        if labels[start] is None or comp[start] != -1:
            continue
        cid = len(objects)
        lab = labels[start]
        stack = [start]
        comp[start] = cid
        area = 0
        x0 = y0 = 10 ** 9
        x1 = y1 = -1
        sx = sy = 0
        while stack:
            i = stack.pop()
            area += 1
            x, y = i % w, i // w
            sx += x
            sy += y
            x0, y0, x1, y1 = min(x0, x), min(y0, y), max(x1, x), max(y1, y)
            for j in ((i - 1) if x > 0 else -1, (i + 1) if x < w - 1 else -1, (i - w) if y > 0 else -1, (i + w) if y < h - 1 else -1):
                if j >= 0 and comp[j] == -1 and labels[j] == lab:
                    comp[j] = cid
                    stack.append(j)
        bw, bh = x1 - x0 + 1, y1 - y0 + 1
        objects.append({"colour": lab, "area": area, "x0": x0, "y0": y0, "x1": x1 + 1, "y1": y1 + 1, "bbox_w": bw, "bbox_h": bh,
                        "cx": (x0 + x1 + 1) / 2.0, "cy": (y0 + y1 + 1) / 2.0, "centroid_x": sx / area, "centroid_y": sy / area,
                        "fill_ratio": area / float(bw * bh), "aspect": max(bw, bh) / float(min(bw, bh))})
    objects = [o for o in objects if o["area"] >= CONFIG["min_component_area_px"]]
    for o in objects:
        o["shape"] = classify_shape(o)
    return {"width": w, "height": h, "object_count": len(objects), "objects": objects, "config_hash": config_hash()}


def classify_shape(o: dict) -> str:
    r = CONFIG["shape_rules"]
    if o["aspect"] >= r["bar_aspect_min"]:
        return "bar"
    if o["fill_ratio"] >= r["square_fill_min"] and o["aspect"] <= r["square_aspect_max"]:
        return "square"
    if r["circle_fill_min"] <= o["fill_ratio"] <= r["circle_fill_max"] and o["aspect"] <= r["circle_aspect_max"]:
        return "circle"
    return "unknown"


def find(result: dict, shape: str, colour: str) -> dict | None:
    hits = [o for o in result["objects"] if o["shape"] == shape and o["colour"] == colour]
    return hits[0] if len(hits) == 1 else None


def relation(result: dict, subject: tuple, obj: tuple) -> str | None:
    s, o = find(result, *subject), find(result, *obj)
    if s is None or o is None:
        return None
    dx, dy = o["cx"] - s["cx"], o["cy"] - s["cy"]
    if abs(dx) >= abs(dy):
        return "left_of" if dx > 0 else "right_of"
    return "above" if dy > 0 else "below"


def quadrant(o: dict, width: int, height: int) -> str:
    return ("top" if o["cy"] < height / 2.0 else "bottom") + "_" + ("left" if o["cx"] < width / 2.0 else "right")


def larger(result: dict, colour_a: str, colour_b: str) -> str | None:
    a = [o for o in result["objects"] if o["colour"] == colour_a]
    b = [o for o in result["objects"] if o["colour"] == colour_b]
    if len(a) != 1 or len(b) != 1:
        return None
    if a[0]["area"] > b[0]["area"]:
        return colour_a
    if b[0]["area"] > a[0]["area"]:
        return colour_b
    return "equal"
