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

src, prefix, names, standing, review = Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3].split(","), sys.argv[4], Path(sys.argv[5])
im = Image.open(src); rgba, keyable = key_out(im); alpha = rgba[:, :, 3] > 0
rows = runs(alpha, axis=1)
cells = []
for (y0, y1) in rows:
    for (x0, x1) in runs(alpha[y0:y1], axis=0):
        sub = alpha[y0:y1, x0:x1]; ys = np.where(sub.any(axis=1))[0]; xs = np.where(sub.any(axis=0))[0]
        cells.append((x0 + xs.min(), y0 + ys.min(), x0 + xs.max() + 1, y0 + ys.max() + 1))
rep = {"source": str(src.relative_to(JOB)), "size": list(im.size), "border_keyable": round(keyable, 4), "rows_found": len(rows), "cells_found": len(cells), "poses": []}
assets = JOB / "gen/assets"
for name, (x0, y0, x1, y1) in zip(names, cells):
    crop = rgba[y0:y1, x0:x1]
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
