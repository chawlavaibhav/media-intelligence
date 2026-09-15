#!/usr/bin/env python3
"""Nivaas Homes 15-s story v2: exterior clip (8 s, line 1) | cut | interior clip (7 s, line 2); the Ledge offer card slides up at 11.5 s.
Both clips 1080x1920 native (no crop); audio = the two native narrations joined at the cut, untouched otherwise."""
import subprocess, sys, yaml
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parent))
import compose_pf as PFc
V4 = Path(__file__).resolve().parent.parent; PF = yaml.safe_load((V4 / "plan/COPY-PF.yaml").read_text())["nivaas"]
EXT = V4 / "gen/portfolio/nivaas2-ext-motion-accepted.mp4"; INT = V4 / "gen/portfolio/nivaas2-int-motion-accepted.mp4"
OUT = Path(sys.argv[1]); OUT.parent.mkdir(parents=True, exist_ok=True)
Wv, Hv, FPS = 1080, 1920, 30; plate_h = int(Hv * 0.58); CUT, CARD_AT, TOTAL = 8.0, 11.5, 15.0


def reader(src, end):
    return subprocess.Popen(["ffmpeg", "-loglevel", "error", "-to", f"{end:.3f}", "-i", str(src), "-vf", f"fps={FPS},scale={Wv}:{Hv}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)


def ease(t): t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3


silent = OUT.with_suffix(".silent.mp4")
enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{Wv}x{Hv}", "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", str(silent)], stdin=subprocess.PIPE)
ra = reader(EXT, CUT); rb = reader(INT, TOTAL - CUT); last = None
for i in range(int(TOTAL * FPS)):
    t = i / FPS; r = ra if t < CUT else rb
    buf = r.stdout.read(Wv * Hv * 3); fr = Image.frombytes("RGB", (Wv, Hv), buf).convert("RGBA") if len(buf) == Wv * Hv * 3 else last; last = fr
    if t >= CARD_AT:
        k = ease((t - CARD_AT) / 0.6); b = 0.15 + 0.85 * ease((t - CARD_AT - 0.3) / 2.0)
        card = PFc.ledge(PFc.Cp.cover_at(fr, Wv, plate_h, 0.5, 0.45), "9x16", PF["brand"], PF["copy"], build=min(b, 1.0))
        f = Image.new("RGBA", (Wv, Hv), PFc.Cp.A._hex_to_rgba(PF["brand"]["primary"])); pan = card.crop((0, plate_h, Wv, Hv))
        if k < 1:
            ph_now = int(Hv - (Hv - plate_h) * k); f.alpha_composite(PFc.Cp.cover_at(fr, Wv, ph_now, 0.5, 0.45), (0, 0)); f.alpha_composite(pan, (0, ph_now))
        else:
            f.alpha_composite(card.crop((0, 0, Wv, plate_h)), (0, 0)); f.alpha_composite(pan, (0, plate_h))
        fr = f
    enc.stdin.write(fr.convert("RGB").tobytes())
enc.stdin.close(); enc.wait()
for r in (ra, rb):
    r.stdout.close(); r.kill()
fc = f"[0:a]atrim=0:{CUT},asetpts=PTS-STARTPTS[a0];[1:a]atrim=0:{TOTAL - CUT},asetpts=PTS-STARTPTS,afade=t=out:st={TOTAL - CUT - 1.0:.2f}:d=1.0[a1];[a0][a1]concat=n=2:v=0:a=1,loudnorm=I=-16:TP=-1.5:LRA=8[a]"
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(EXT), "-i", str(INT), "-i", str(silent), "-filter_complex", fc, "-map", "2:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{TOTAL:.3f}", "-movflags", "+faststart", str(OUT)], check=True)
silent.unlink(); print("wrote", OUT)
