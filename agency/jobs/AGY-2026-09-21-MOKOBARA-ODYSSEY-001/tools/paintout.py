#!/usr/bin/env python3
"""paintout.py — deterministic paint-over of a small in-model lettering mark on a still (job rule: no in-model lettering /
wordmark). Fills the box by per-column vertical interpolation between the rows just above and below, blurs the box edge,
writes <out> and <out>.edit.json (sha256 in and out, the box, the reason). usage: paintout.py in.png out.png x0 y0 x1 y1 "why"
"""
import sys, json, hashlib, datetime
from PIL import Image, ImageFilter
import numpy as np
src, dst = sys.argv[1], sys.argv[2]; x0, y0, x1, y1 = map(int, sys.argv[3:7]); why = sys.argv[7]
im = Image.open(src).convert('RGB'); a = np.asarray(im).astype(float)
top = a[y0 - 3:y0, x0:x1].mean(0); bot = a[y1:y1 + 3, x0:x1].mean(0)
for k, y in enumerate(range(y0, y1)):
    t = (k + 1) / (y1 - y0 + 1); a[y, x0:x1] = top * (1 - t) + bot * t
out = Image.fromarray(a.clip(0, 255).astype('uint8'))
reg = out.crop((x0 - 4, y0 - 4, x1 + 4, y1 + 4)).filter(ImageFilter.GaussianBlur(0.7)); out.paste(reg, (x0 - 4, y0 - 4))
out.save(dst)
h = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
json.dump({"utc": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'), "source": src, "source_sha256": h(src), "out": dst, "out_sha256": h(dst),
           "box": [x0, y0, x1, y1], "method": "per-column vertical interpolation between the 3 rows above and below; 0.7 px blur on the box edge; nothing else touched",
           "why": why}, open(dst + ".edit.json", "w"), indent=1)
print("wrote", dst, h(dst))
