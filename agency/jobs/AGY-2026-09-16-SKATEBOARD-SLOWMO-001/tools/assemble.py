#!/usr/bin/env python3
"""Assembly for AGY-2026-09-16-SKATEBOARD-SLOWMO-001 — USD 0, ffmpeg only. No text in this job.

The accepted take (Gemini Omni i2v, 720x1280, 10 s) becomes the reel by code:
  A  0.00–CUT_S   normal speed — the walk and the bump
  B  CUT_S–END_S  the flight, slowed SLOW_X times by motion-interpolated frames (minterpolate), then a short hold
The tail after END_S (where the model put the cup back in her hand — a physics break) is NOT used.
Declared upscale 720p → 1080x1920 (lanczos). The generated audio track is dropped (the user chose music only).
Music: the Lyria bed at normal pitch through the bump, then a code "slow-down" — pitch drops and a low-pass closes —
starting at the MEASURED bump time (CUT_S), never at a planned time (case 003 lesson). Loudness normalised per stem,
limiter on the mix. Report written next to the output.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
JOB = HERE.parent
TAKE = JOB / "gen/clips/take-2-accepted.mp4"      # V2: the medium-framed take (user: 'more zoomed in')
MUSIC = JOB / "gen/music/bed-r1.wav"
FPS = 24
CUT_S = 4.90          # measured on the sampled frames of take-2: both hands have opened; cup, phone and keys are in the air
SEGMENTS = [(4.90, 6.60, 3), (6.60, 9.20, 1.5)]   # (from, to, slow factor): the flight at 3×, then the push-in on her face at 1.5×
END_S = 9.20          # after 9.2 s the objects are below the frame; unused
HOLD_S = 0.5
W, H = 1080, 1920


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"command failed: {' '.join(cmd[:8])}…\n{r.stderr[-1200:]}")
    return r


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    out = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else JOB / "gen/final/skateboard-slowmo-9x16.mp4"
    work = out.parent / "_work"; work.mkdir(parents=True, exist_ok=True)
    up = f"scale={W}:{H}:flags=lanczos"
    # A — normal speed
    run(["ffmpeg", "-v", "error", "-y", "-ss", "0", "-t", f"{CUT_S}", "-i", str(TAKE), "-an", "-vf", f"{up},fps={FPS},format=yuv420p",
         "-c:v", "libx264", "-preset", "medium", "-crf", "16", str(work / "A.mp4")])
    # B… — slow motion by interpolation per segment: interpolate to FPS*factor, stretch pts by the factor
    segs = [work / "A.mp4"]
    for i, (f0, f1, x) in enumerate(SEGMENTS):
        seg = work / f"B{i}.mp4"; last = i == len(SEGMENTS) - 1
        vf = f"{up},minterpolate=fps={int(FPS * x)}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,setpts={x}*PTS,fps={FPS}"
        if last:
            vf += f",tpad=stop_mode=clone:stop_duration={HOLD_S},fade=t=out:st={(f1 - f0) * x + HOLD_S - 0.5:.3f}:d=0.5"
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{f0}", "-t", f"{f1 - f0}", "-i", str(TAKE), "-an", "-vf", vf + ",format=yuv420p",
             "-c:v", "libx264", "-preset", "medium", "-crf", "16", str(seg)])
        segs.append(seg)
    (work / "concat.txt").write_text("".join(f"file '{p}'\n" for p in segs))
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(work / "concat.txt"), "-c", "copy", str(work / "video.mp4")])
    total = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(work / "video.mp4")]).stdout.strip())

    # music: normal until CUT_S, then the slow-down (pitch to 0.55×, low-pass closing, level dropping) — a code effect keyed to the measured bump
    slow_len = total - CUT_S
    af = (f"[0:a]atrim=0:{CUT_S:.3f},asetpts=PTS-STARTPTS,loudnorm=I=-16:TP=-2:LRA=9[m1];"
          f"[0:a]atrim={CUT_S:.3f}:{CUT_S + slow_len / 0.55 + 1:.3f},asetpts=PTS-STARTPTS,asetrate=48000*0.55,aresample=48000,"
          f"lowpass=f=900,atrim=0:{slow_len:.3f},loudnorm=I=-19:TP=-2:LRA=9,afade=t=out:st={slow_len - 1.5:.3f}:d=1.5[m2];"
          f"[m1][m2]concat=n=2:v=0:a=1,alimiter=limit=0.89:level=false[mix]")
    run(["ffmpeg", "-v", "error", "-y", "-i", str(MUSIC), "-filter_complex", af, "-map", "[mix]", "-t", f"{total:.3f}", "-ar", "48000", str(work / "mix.wav")])
    run(["ffmpeg", "-v", "error", "-y", "-i", str(work / "video.mp4"), "-i", str(work / "mix.wav"), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)])
    probe = json.loads(run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_name,width,height,r_frame_rate,duration", "-of", "json", str(out)]).stdout)["streams"]
    report = {"take": str(TAKE.relative_to(JOB)), "take_sha256": sha(TAKE), "cut_s": CUT_S, "segments": SEGMENTS, "hold_s": HOLD_S,
              "unused_tail": f"{END_S}–10.0 s of the take — not used", "upscale": "720x1280 → 1080x1920 lanczos (DECLARED)",
              "generated_audio": "dropped (user: music only)", "music": {"bed": str(MUSIC.relative_to(JOB)), "slow_down_at_s": CUT_S, "effect": "asetrate 0.55x + lowpass 900 Hz + level −3 LU, fade out"},
              "duration_s": round(total, 3), "probe": probe, "output": str(out.relative_to(JOB)), "sha256": sha(out)}
    out.with_suffix(".qa.json").write_text(json.dumps(report, indent=1))
    print(f"built {out.relative_to(JOB)}  {total:.2f} s  sha256 {report['sha256'][:16]}")


if __name__ == "__main__":
    main()
