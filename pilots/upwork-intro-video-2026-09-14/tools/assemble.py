#!/usr/bin/env python3
"""Assemble the film: presenter takes (with J-cut insert and word-identical supers) + work segments + end card;
audio = native take audio at offsets + sealed Lyria bed (looped, ducked) + synthesised snaps/tick; loudnorm; export.

usage: assemble.py <out_dir>   (expects gen/segments, gen/p1-presenter-takes, gen/overlays)
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import film as F  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
GEN = HERE / "gen"
REPO = HERE.parents[1]
MUSIC = REPO / "eval/experiments/EVAL-040/runs/aud-music-lyria/artifacts/media/MUS-02__lyria__native__r1.wav"
D = F.DECK["supers"]


def sfx(path: Path, kind: str, sr: int = 48000):
    """Tiny synthesised sounds: 'snap' = 45 ms filtered noise burst; 'tone' = soft two-note; 'tick' = short sine blip."""
    if kind == "snap":
        n = int(0.045 * sr); t = np.arange(n) / sr
        x = np.random.default_rng(7).normal(0, 1, n) * np.exp(-t * 90)
        # crude band-pass by differencing + smoothing
        x = np.convolve(np.diff(x, prepend=0), np.ones(6) / 6, mode="same") * 0.6
    elif kind == "tone":
        n = int(0.35 * sr); t = np.arange(n) / sr
        x = (np.sin(2 * math.pi * 660 * t) * 0.5 + np.sin(2 * math.pi * 880 * t) * 0.35) * np.exp(-t * 9) * 0.35
    else:  # tick
        n = int(0.12 * sr); t = np.arange(n) / sr
        x = np.sin(2 * math.pi * 1320 * t) * np.exp(-t * 40) * 0.45
    x = np.clip(x, -1, 1)
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
        wf.writeframes((x * 32767).astype(np.int16).tobytes())


def main(out_dir: str):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    seg = GEN / "segments"; takes = GEN / "p1-presenter-takes"
    segs = json.loads((seg / "segments.json").read_text())
    t1 = json.loads((takes / "t1-times.json").read_text()); t2 = json.loads((takes / "t2-times.json").read_text()); t3 = json.loads((takes / "t3-times.json").read_text())

    # --- presenter takes with supers (cues from the transcript timings, ±0.15 s), T1 with the J-cut insert
    pad = 0.15
    c1 = [(max(0, t1[0]["start_s"]), t1[0]["end_s"] + pad, D["t1a"]),
          (t1[1]["start_s"] + 0.05, t1[1]["end_s"] + pad, D["t1b"]),
          (t1[2]["start_s"], t1[2]["end_s"] + 0.5, D["t1c"])]
    insert_until = t1[0]["end_s"]                       # the finished ad stays up while the first sentence is spoken
    d1 = F.burn_supers(takes / "t1-veo-r1.mp4", out / "t1.mp4", c1, insert=(str(seg / "insert-ad.png"), insert_until))
    c2 = [(t2[0]["start_s"], t2[0]["end_s"] + pad, D["t2a"]), (t2[1]["start_s"], t2[1]["end_s"] + 0.6, D["t2b"])]
    d2 = F.burn_supers(takes / "t2-veo-r1.mp4", out / "t2.mp4", c2, trim_s=min(8.0, t2[1]["end_s"] + 1.4))
    c3 = [(t3[0]["start_s"], t3[0]["end_s"] + pad, D["t3a"], D["t3a_qualifier"]), (t3[1]["start_s"], min(8.0, t3[1]["end_s"] + 0.3), D["t3b"])]
    d3 = F.burn_supers(takes / "t3-veo-r1.mp4", out / "t3.mp4", c3)

    # --- video order
    order = [("t1", out / "t1.mp4", d1), ("brief", seg / "seg-brief.mp4", segs["brief"]["dur"]), ("build", seg / "seg-build.mp4", segs["build"]["dur"]),
             ("sizes", seg / "seg-sizes.mp4", segs["sizes"]["dur"]), ("hooks", seg / "seg-hooks.mp4", segs["hooks"]["dur"]), ("check", seg / "seg-check.mp4", segs["check"]["dur"]),
             ("phone1", seg / "seg-phone1.mp4", segs["phone1"]["dur"]), ("phone2", seg / "seg-phone2.mp4", segs["phone2"]["dur"]), ("phone3", seg / "seg-phone3.mp4", segs["phone3"]["dur"]),
             ("t2", out / "t2.mp4", d2), ("t3", out / "t3.mp4", d3), ("end", seg / "seg-end.mp4", segs["end"]["dur"])]
    starts = {}; t = 0.0
    for name, path, dur in order:
        starts[name] = t; t += dur
    total = t
    # concat video streams (all 1920x1080 24 fps yuv420p) via the concat demuxer, video only
    lst = out / "concat.txt"
    lst.write_text("".join(f"file '{p.resolve()}'\n" for _, p, _ in order))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-an", "-c:v", "libx264", "-crf", "16", "-preset", "medium",
                    "-pix_fmt", "yuv420p", "-r", "24", str(out / "video.mp4")], check=True)

    # --- audio
    sfxd = out / "sfx"; sfxd.mkdir(exist_ok=True)
    for k in ("snap", "tone", "tick"):
        sfx(sfxd / f"{k}.wav", k)
    events = [(0.0, "snap", 0.35)]                                              # frame 1 has a sound (sk_abcd_0005)
    events += [(starts["build"] + s, "snap", 0.5) for s in segs["build"]["snaps"]]
    events += [(starts["sizes"] + s, "snap", 0.5) for s in segs["sizes"]["snaps"]]
    events += [(starts["hooks"] + s, "snap", 0.35) for s in segs["hooks"]["snaps"]]
    events += [(starts["hooks"] + segs["hooks"]["flip"], "tone", 0.6)]
    events += [(starts["check"] + segs["check"]["tick"], "tick", 0.7)]
    events += [(starts[p], "snap", 0.35) for p in ("phone1", "phone2", "phone3")]
    inputs = ["-i", str(out / "video.mp4"), "-i", str(out / "t1.mp4"), "-i", str(out / "t2.mp4"), "-i", str(out / "t3.mp4"), "-i", str(MUSIC)]
    for ev in events:
        inputs += ["-i", str(sfxd / f"{ev[1]}.wav")]
    n_sfx = len(events)
    fc = []
    # takes at their offsets (native audio), gentle per-take normalisation
    fc.append(f"[1:a]loudnorm=I=-18:TP=-2:LRA=9,adelay={int(starts['t1']*1000)}|{int(starts['t1']*1000)}[a1]")
    fc.append(f"[2:a]loudnorm=I=-18:TP=-2:LRA=9,adelay={int(starts['t2']*1000)}|{int(starts['t2']*1000)}[a2]")
    fc.append(f"[3:a]loudnorm=I=-18:TP=-2:LRA=9,adelay={int(starts['t3']*1000)}|{int(starts['t3']*1000)}[a3]")
    # music: loop the 32.8 s bed with a crossfade to cover the film, enter at the brief card, duck under T2/T3, out before the end
    m_in = starts["brief"]; m_end = total - 0.5
    duck_a, duck_b = starts["t2"], starts["end"]
    fc.append("[4:a]asplit[m0][m1];[m0][m1]acrossfade=d=3:c1=tri:c2=tri[mloop]")
    fc.append(f"[mloop]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,"
              f"volume='if(between(t,{duck_a:.2f},{duck_b:.2f}),0.28,1.0)':eval=frame,"
              f"afade=t=in:st={m_in:.2f}:d=1.5,afade=t=out:st={m_end-2.5:.2f}:d=2.0,"
              f"volume=0.16,adelay={int(m_in*1000)}|{int(m_in*1000)},atrim=0:{total:.3f}[mus]")
    labels = []
    for i, ev in enumerate(events):
        fc.append(f"[{5+i}:a]volume={ev[2]},adelay={int(ev[0]*1000)}|{int(ev[0]*1000)},aformat=channel_layouts=stereo[s{i}]")
        labels.append(f"[s{i}]")
    fc.append(f"[a1][a2][a3][mus]{''.join(labels)}amix=inputs={4+n_sfx}:normalize=0:duration=longest,"
              f"loudnorm=I=-16:TP=-1.5:LRA=11:linear=true,atrim=0:{total:.3f}[aout]")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "0:v", "-map", "[aout]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-t", f"{total:.3f}",
                    str(out / "upwork-intro-first-pass.mp4")], check=True)
    # two-pass loudness to the contract (D1: -16 LUFS ±1, TP <= -1 dBTP)
    mix = out / "mix.wav"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(out / "upwork-intro-first-pass.mp4"), "-vn", "-c:a", "pcm_s16le", str(mix)], check=True)
    meas = subprocess.run(["ffmpeg", "-i", str(mix), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    cur = float([l for l in meas.splitlines() if l.strip().startswith("I:")][-1].split()[1])
    gain = -16.0 - cur                                       # measured gain to the target, then a true-peak limiter at -1.2 dBTP
    ln = f"volume={gain:.2f}dB,alimiter=limit=0.87:attack=5:release=60:level=false"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(out / "video.mp4"), "-i", str(mix), "-af", ln, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-t", f"{total:.3f}",
                    str(out / "upwork-intro-first-pass.mp4")], check=True)
    (out / "timeline.json").write_text(json.dumps({"starts": starts, "total_s": total, "events": events}, indent=1))
    print(json.dumps({"total_s": round(total, 2), "starts": {k: round(v, 2) for k, v in starts.items()}}, indent=0))


if __name__ == "__main__":
    main(sys.argv[1])
