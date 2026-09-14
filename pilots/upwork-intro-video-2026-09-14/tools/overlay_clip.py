#!/usr/bin/env python3
"""Code-set text onto generated clips (RR-6 mechanism: the model never writes a word).

modes:
  aarohi  <in.mp4> <out.mp4>   text-in-motion: pill + two-line headline rise into the empty wall; product/price/wordmark below
  juice   <in.mp4> <out.mp4>   a gold offer pill + one cream line on the dark slate
Frames are decoded by ffmpeg, composed with Pillow using hb-view glyphs from the deck, re-encoded (silent).
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import adcomp as A  # noqa: E402
import film as F  # noqa: E402

DECK = F.DECK
FPS = 24


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip().split(",")
    return int(out[0]), int(out[1]), float(out[2])


def run(mode, src, dst):
    W, H, dur = probe(src)
    n = int(dur * FPS)
    dec = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", src, "-vf", f"fps={FPS}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-an", "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
    brand = A.Brand()
    po = DECK["phone_overlays"]
    if mode == "aarohi":
        hl = int(W * 0.105)
        pill = A.pill(po["aarohi_motion_pill"], "hn_medium", int(hl * 0.42), brand.accent, brand.primary)
        lines = [A.text(l, "didot", hl, brand.primary) for l in po["aarohi_motion_line"]]
        sub = A.text(f'{DECK["aarohi_en"]["product"]}  {DECK["aarohi_en"]["price"]}', "hn_medium", int(hl * 0.36), brand.primary)
        mark = A.text(DECK["aarohi_en"]["wordmark"], "didot", int(hl * 0.42), brand.primary)
        for s in [po["aarohi_motion_pill"], *po["aarohi_motion_line"], DECK["aarohi_en"]["wordmark"]]:
            F.USED_STRINGS.add(s)
        m = int(W * 0.08)
        y_pill, y1 = int(H * 0.10), int(H * 0.10) + pill.height + int(hl * 0.45)
        y2 = y1 + int(hl * 1.12)
        y_sub = int(H * 0.86)
    else:
        pill = A.pill(po["juice_pill"], "hn_medium", int(W * 0.05), "#E8A33D", "#1A1A1A")
        sub = A.text(po["juice_sub"], "hn", int(W * 0.045), "#F5F1EA")
        F.USED_STRINGS.update([po["juice_pill"], po["juice_sub"]])
        m = int(W * 0.08)
    for i in range(n):
        buf = dec.stdout.read(W * H * 3)
        if len(buf) < W * H * 3:
            break
        f = Image.frombytes("RGB", (W, H), buf).convert("RGBA")
        t = i / FPS
        def fade(im, a, dy=0, x=0, y=0):
            if a <= 0:
                return
            im2 = im.copy(); im2.putalpha(im2.getchannel("A").point(lambda v: int(v * a)))
            A.paste(f, im2, x, y + int((1 - a) * dy))
        if mode == "aarohi":
            fade(pill, F.ease((t - 0.4) / 0.6), 30, m, y_pill)
            fade(lines[0], F.ease((t - 0.9) / 0.7), 40, m, y1)
            fade(lines[1], F.ease((t - 1.3) / 0.7), 40, m, y2)
            fade(sub, F.ease((t - 2.2) / 0.6), 20, m, y_sub)
            fade(mark, F.ease((t - 2.2) / 0.6), 20, W - m - mark.width, y_sub + (sub.height - mark.height) // 2)
        else:
            fade(pill, F.ease((t - 0.5) / 0.6), 30, m, int(H * 0.88) - pill.height)
        enc.stdin.write(f.convert("RGB").tobytes())
    enc.stdin.close(); enc.wait()
    dec.stdout.close(); dec.kill(); dec.wait()
    print("wrote", dst, n, "frames")


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], sys.argv[3])
