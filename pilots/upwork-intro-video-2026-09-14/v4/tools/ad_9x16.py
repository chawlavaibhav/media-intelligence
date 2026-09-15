#!/usr/bin/env python3
"""Rebuild the 9:16 Aarohi offer-in-motion clip with the V4 composer (fit loop, edge margin, SHOP NOW). USD 0."""
import subprocess, sys
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parent))
import compose_v4 as Cp
from compose_v4 import A
V4 = Path(__file__).resolve().parent.parent; G3 = V4.parent / "v3" / "gen"; FPS = 30
Wv, Hv = 1080, 1920; plate_h = int(Hv * 0.58)
A2 = Image.open(G3 / "stills/a2-accepted.png").convert("RGBA")
seq = [("a2-accepted.mp4", (0.5, 0.45), 4.0), ("a1-accepted.mp4", (0.62, 0.5), 4.0), ("a3-accepted.mp4", (0.5, 0.5), 3.5)]
out = Path(sys.argv[1]); out.parent.mkdir(parents=True, exist_ok=True)
p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{Wv}x{Hv}", "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
full = Cp.aarohi(A2, "9x16", anchor=(0.5, 0.45), cta="SHOP NOW"); panel_full = full.crop((0, plate_h - 60, Wv, Hv))
def ease(t): t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3
tglob = 0.0; prev = None
for src, anc, d in seq:
    ax, ay = anc
    vf = f"fps={FPS},scale={Wv}:{plate_h}:force_original_aspect_ratio=increase,crop={Wv}:{plate_h}:(iw-{Wv})*{ax}:(ih-{plate_h})*{ay}"
    dec = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", str(G3 / "video" / src), "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    last = None
    for i in range(int(d * FPS)):
        buf = dec.stdout.read(Wv * plate_h * 3)
        fr = Image.frombytes("RGB", (Wv, plate_h), buf).convert("RGBA") if len(buf) == Wv * plate_h * 3 else last
        last = fr
        if i < 10 and prev is not None:
            fr = Image.blend(prev, fr, ease(i / 10))
        f = Image.new("RGBA", (Wv, Hv), A._hex_to_rgba(Cp.AAROHI["primary"])); f.alpha_composite(fr, (0, 0))
        b = ease((tglob - 0.4) / 1.0)
        card = Cp.aarohi(A2, "9x16", build=0.15 + 0.85 * b, anchor=(0.5, 0.45), cta="SHOP NOW") if b < 1 else full
        f.alpha_composite(card.crop((0, plate_h - 60, Wv, Hv)), (0, plate_h - 60))
        p.stdin.write(f.convert("RGB").tobytes()); tglob += 1 / FPS
    prev = last; dec.stdout.close(); dec.kill(); dec.wait()
p.stdin.close(); p.wait(); print("wrote", out)
