#!/usr/bin/env python3
"""inspect_sheet.py — the consistency card for a 2x4 pose sheet (USD 0): keys the green out (Lane A cutout.key_out), splits the
grid by empty rows/columns, writes gen/assets/<prefix>_<pose>.png per cell in the prompt's order, a <prefix>_cutout.json
(cell boxes, sizes, standing_cell_h, keyability, red-book and key-ring pixel counts per cell), and a review strip that puts
the eight cells beside the accepted Lane A idle and the accepted C 'brace' for the identity look (same man, spectacles,
shirt, trousers, sandals; keys + red book; no lettering; keyable background; no Nintendo drift — judged by eye, recorded).
usage: inspect_sheet.py <sheet.png> <prefix> <pose1,...,pose8> <standing_pose_name> <review.png>"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parent))
from cutout import key_out
JOB = Path(__file__).resolve().parent.parent

def runs(mask, axis, min_frac=0.008):
    prof = mask.any(axis=axis); out = []; inrun = False
    for i, v in enumerate(prof):
        if v and not inrun: start = i; inrun = True
        elif not v and inrun: out.append((start, i)); inrun = False
    if inrun: out.append((start, len(prof)))
    merged = []
    for r in out:
        if merged and r[0] - merged[-1][1] < min_frac * len(prof): merged[-1] = (merged[-1][0], r[1])
        else: merged.append(r)
    return [r for r in merged if r[1] - r[0] > 0.03 * len(prof)]

def components(mask):
    """4-connected components of a boolean mask (BFS); returns list of (count, x0, y0, x1, y1, pixel-index-array)."""
    from collections import deque
    h, w = mask.shape; lab = np.full((h, w), -1, dtype=np.int32); comps = []
    for y in range(h):
        for x in range(w):
            if mask[y, x] and lab[y, x] < 0:
                cid = len(comps); q = deque([(y, x)]); lab[y, x] = cid; pts = []
                while q:
                    cy, cx = q.popleft(); pts.append((cy, cx))
                    for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                        if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and lab[ny, nx] < 0:
                            lab[ny, nx] = cid; q.append((ny, nx))
                ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
                comps.append({"n": len(pts), "x0": min(xs), "y0": min(ys), "x1": max(xs) + 1, "y1": max(ys) + 1, "pts": pts})
    return comps


def split_merged(alpha, cell, k):
    """A run that holds k figures whose columns overlap: label components, take the k largest as figures (left to right),
    attach every small component (loose book, knocked-off spectacles) to the figure whose bbox is nearest, return k masks."""
    x0, y0, x1, y1 = cell; sub = alpha[y0:y1, x0:x1]; comps = components(sub)
    big = sorted(sorted(comps, key=lambda c: -c["n"])[:k], key=lambda c: c["x0"])
    groups = [[c] for c in big]
    for c in comps:
        if c in big:
            continue
        def dist(b):
            dx = max(0, b["x0"] - c["x1"], c["x0"] - b["x1"]); dy = max(0, b["y0"] - c["y1"], c["y0"] - b["y1"]); return dx * dx + dy * dy
        groups[min(range(k), key=lambda i: dist(big[i]))].append(c)
    out = []
    for g in groups:
        m = np.zeros_like(sub)
        for c in g:
            for (py, px) in c["pts"]:
                m[py, px] = True
        ys = np.where(m.any(axis=1))[0]; xs = np.where(m.any(axis=0))[0]
        out.append((((x0, y0), m), (x0 + xs.min(), y0 + ys.min(), x0 + xs.max() + 1, y0 + ys.max() + 1)))
    return out


src, prefix, names, standing, review = Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3].split(","), sys.argv[4], Path(sys.argv[5])
im = Image.open(src); rgba, keyable = key_out(im); alpha = rgba[:, :, 3] > 0
rows = runs(alpha, axis=1)
cells = []; masks = []; per_row = len(names) // max(1, len(rows)); split_note = []
for (y0, y1) in rows:
    rr = runs(alpha[y0:y1], axis=0)
    row_cells = []
    for (x0, x1) in rr:
        sub = alpha[y0:y1, x0:x1]; ys = np.where(sub.any(axis=1))[0]; xs = np.where(sub.any(axis=0))[0]
        row_cells.append((x0 + xs.min(), y0 + ys.min(), x0 + xs.max() + 1, y0 + ys.max() + 1))
    if len(row_cells) < per_row:   # a merged run: split the widest by connected components
        missing = per_row - len(row_cells); widest = max(range(len(row_cells)), key=lambda i: row_cells[i][2] - row_cells[i][0])
        parts = split_merged(alpha, row_cells[widest], missing + 1); split_note.append({"merged_cell": list(map(int, row_cells[widest])), "into": missing + 1})
        new_cells = row_cells[:widest] + [b for m, b in parts] + row_cells[widest + 1:]
        new_masks = [None] * widest + [m for m, b in parts] + [None] * (len(row_cells) - widest - 1)
        row_cells, row_masks = new_cells, new_masks
    else:
        row_masks = [None] * len(row_cells)
    cells += row_cells; masks += row_masks
MERGED = {}


def mk_sheet(mk, box):
    """mk is a mask over the merged cell (stored with its origin); return the mask cropped to `box` in sheet coordinates."""
    (ox, oy), m = mk
    x0, y0, x1, y1 = box
    return m[y0 - oy:y1 - oy, x0 - ox:x1 - ox]


rep = {"source": str(src.relative_to(JOB)), "merged_cells_split": split_note, "size": list(im.size), "border_keyable": round(keyable, 4), "rows_found": len(rows), "cells_found": len(cells), "poses": []}
assets = JOB / "gen/assets"
for name, (x0, y0, x1, y1), mk in zip(names, cells, masks):
    crop = rgba[y0:y1, x0:x1].copy()
    if mk is not None:   # component-split cell: keep only this figure's pixels
        crop[:, :, 3] = np.where(mk_sheet(mk, (x0, y0, x1, y1)), crop[:, :, 3], 0)
    a = crop[:, :, 3] > 0; r, g, b = crop[:, :, 0].astype(int), crop[:, :, 1].astype(int), crop[:, :, 2].astype(int)
    red = int(((r > 150) & (g < 90) & (b < 90) & a).sum()); gold = int(((r > 150) & (g > 110) & (b < 90) & a).sum())
    out = assets / f"{prefix}_{name}.png"; Image.fromarray(crop, "RGBA").save(out)
    rep["poses"].append({"pose": name, "box": [int(x0), int(y0), int(x1), int(y1)], "w": int(x1 - x0), "h": int(y1 - y0), "red_book_px": red, "gold_keys_px": gold})
st = next((p for p in rep["poses"] if p["pose"] == standing), None)
rep["standing_cell_h"] = st["h"] if st else None; rep["standing_pose"] = standing
rep["status"] = "ok" if (len(cells) == len(names) and keyable >= 0.98) else f"CHECK: cells {len(cells)} vs {len(names)}, keyable {keyable:.3f}"
Path(assets / f"{prefix}_cutout.json").write_text(json.dumps(rep, indent=1))
# review strip: base idle + C brace + the eight cells, scaled to a common standing height
H = 360
ref = [("laneA idle", Image.open(assets / "owner_idle.png")), ("C brace", Image.open(assets / "c_brace.png"))]
tiles = [(n, Image.open(assets / f"{prefix}_{n}.png")) for n in names[:len(cells)]]
sc = {"laneA idle": H / 561, "C brace": H / 344}; s_new = H / (rep["standing_cell_h"] or H)
board = Image.new("RGB", (len(ref + tiles) * 300, H + 60), (40, 40, 40))
for i, (n, t) in enumerate(ref + tiles):
    f = sc.get(n, s_new); tt = t.convert("RGBA").resize((max(1, int(t.width * f)), max(1, int(t.height * f))), Image.NEAREST)
    board.paste(tt, (i * 300 + (300 - tt.width) // 2, H - tt.height + 20), tt)
import pixfont as PF
for i, (n, _) in enumerate(ref + tiles):
    lab = PF.render(n.upper().replace("_", " ")[:14], 2, fg=(255, 255, 255)); board.paste(lab, (i * 300 + 8, H + 30), lab)
board.save(review); print(json.dumps(rep, indent=1)); print("review:", review)
