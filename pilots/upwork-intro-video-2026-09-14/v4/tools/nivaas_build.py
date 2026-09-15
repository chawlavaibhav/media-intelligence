#!/usr/bin/env python3
"""Nivaas Homes 15-s story: exterior (0-8.35 s) | straight cut over the extend-morph | interior (9.0-15 s); from 11.0 s the frame becomes
the Ledge offer card (interior as the moving plate, copy composed by code). Audio = the native narration, untouched."""
import subprocess, sys, yaml
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parent))
import compose_pf as PFc
V4 = Path(__file__).resolve().parent.parent; PF = yaml.safe_load((V4 / "plan/COPY-PF.yaml").read_text())["nivaas"]
SRC = V4 / "gen/portfolio/nivaas-story-r1.mp4"; OUT = Path(sys.argv[1]); OUT.parent.mkdir(parents=True, exist_ok=True)
Wv, Hv, FPS = 1080, 1920, 30; plate_h = int(Hv * 0.58); CUT_A, CUT_B, CARD_AT, TOTAL = 8.0, 9.1, 11.0, 15.0


def reader(start, end):
    vf = f"fps={FPS},scale={Wv}:{Hv}"
    return subprocess.Popen(["ffmpeg", "-loglevel", "error", "-ss", f"{start:.3f}", "-to", f"{end:.3f}", "-i", str(SRC), "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)


def ease(t): t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3


silent = OUT.with_suffix(".silent.mp4")
enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{Wv}x{Hv}", "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", str(silent)], stdin=subprocess.PIPE)
n = int(TOTAL * FPS); ra = reader(0, CUT_A); rb = reader(CUT_B, 15.04); last = None; t_card = 0.0
for i in range(n):
    t = i / FPS; r = ra if t < CUT_A else rb
    buf = r.stdout.read(Wv * Hv * 3); fr = Image.frombytes("RGB", (Wv, Hv), buf).convert("RGBA") if len(buf) == Wv * Hv * 3 else last; last = fr
    if t >= CARD_AT:
        k = ease((t - CARD_AT) / 0.6)
        b = 0.15 + 0.85 * ease((t - CARD_AT - 0.3) / 2.0)
        # the plate: the moving interior, cover-fitted into the plate region; the panel rises from below
        plate = PFc.Cp.cover_at(fr, Wv, plate_h, 0.5, 0.45)
        card = PFc.ledge(plate, "9x16", PF["brand"], PF["copy"], build=min(b, 1.0))
        # the picture shrinks into the plate region and the solid panel slides up from below — no translucent overlay at any point
        f = Image.new("RGBA", (Wv, Hv), PFc.Cp.A._hex_to_rgba(PF["brand"]["primary"]))
        top = card.crop((0, 0, Wv, plate_h)); pan = card.crop((0, plate_h, Wv, Hv))
        if k < 1:
            ph_now = int(Hv - (Hv - plate_h) * k); f.alpha_composite(PFc.Cp.cover_at(fr, Wv, ph_now, 0.5, 0.45), (0, 0)); f.alpha_composite(pan, (0, ph_now))
        else:
            f.alpha_composite(top, (0, 0)); f.alpha_composite(pan, (0, plate_h))
        fr = f
    enc.stdin.write(fr.convert("RGB").tobytes())
enc.stdin.close(); enc.wait(); ra.stdout.close(); ra.kill(); rb.stdout.close(); rb.kill()
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(silent), "-i", str(SRC), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-af", f"afade=t=out:st={TOTAL - 1.0:.2f}:d=1.0", "-t", f"{TOTAL:.3f}", "-movflags", "+faststart", str(OUT)], check=True)
silent.unlink(); print("wrote", OUT)
