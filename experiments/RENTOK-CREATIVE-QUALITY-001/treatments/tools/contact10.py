#!/usr/bin/env python3
"""10-fps contact sheet of a clip (labels = 14.0 + j*0.1 s by default). usage: contact10.py <clip> <out.png> [t0]"""
import sys, glob, math, subprocess, tempfile, shutil
from PIL import Image, ImageDraw
clip, out = sys.argv[1], sys.argv[2]; t0 = float(sys.argv[3]) if len(sys.argv) > 3 else 14.0
d = tempfile.mkdtemp()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", clip, "-vf", "fps=10,scale=144:-1", f"{d}/f%03d.png"], check=True)
fs = sorted(glob.glob(f"{d}/f*.png")); cols = 10; tw, th = 144, 256; rows = math.ceil(len(fs) / cols)
sheet = Image.new("RGB", (cols * tw, rows * (th + 16)), (20, 20, 24)); dr = ImageDraw.Draw(sheet)
for j, f in enumerate(fs):
    im = Image.open(f); x = (j % cols) * tw; y = (j // cols) * (th + 16); sheet.paste(im, (x, y)); dr.text((x + 3, y + th + 2), f"{t0 + j * 0.1:05.2f}s", fill=(255, 255, 255))
sheet.save(out); shutil.rmtree(d); print(len(fs), out)
