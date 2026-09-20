#!/usr/bin/env python3
"""assemble.py — mix + mux (Stage 4 A12): Lyria bed trimmed to 30.0 s, SFX stem, two-pass loudnorm to −14 LUFS / −1 dBTP,
AAC-LC 48 kHz 192 kbps stereo, muxed with the code-rendered video (stream copy, moov first).

usage: python3 assemble.py <video.mp4> <music.wav> <out.mp4>
Prints the measured loudness of the delivered file (ffmpeg ebur128) and writes gen/audio-mix.json.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
JOB = HERE.parent


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def main():
    video, music, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    sfx = JOB / "gen/sfx-stem.wav"
    mix = JOB / "gen/audio-mix-raw.wav"
    # 1. bed trimmed with fades, −7 dB; sfx −4 dB; sum
    graph = ("[0:a]atrim=0:30,asetpts=PTS-STARTPTS,afade=t=in:d=0.15,afade=t=out:st=29.3:d=0.7,volume=-7dB[m];"
             "[1:a]volume=-4dB[s];[m][s]amix=inputs=2:duration=first:normalize=0[mix]")
    r = run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(music), "-i", str(sfx), "-filter_complex", graph, "-map", "[mix]",
             "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(mix)])
    if r.returncode:
        sys.exit(r.stderr)
    # 2. loudnorm pass 1 (measure)
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(mix), "-af", "loudnorm=I=-14:TP=-4:LRA=11:print_format=json", "-f", "null", "-"])
    blob = r.stderr[r.stderr.rfind("{"):]; blob = blob[: blob.find("}") + 1]
    m = json.loads(blob)
    # 3. pass 2 (linear, measured values)
    norm = JOB / "gen/audio-mix.wav"
    af = (f"loudnorm=I=-14:TP=-4:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
          f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true:print_format=json")
    r = run(["ffmpeg", "-y", "-loglevel", "info", "-i", str(mix), "-af", af, "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(norm)])
    if r.returncode:
        sys.exit(r.stderr)
    # 4. mux
    out.parent.mkdir(parents=True, exist_ok=True)
    r = run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-i", str(norm), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
             "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-shortest", "-movflags", "+faststart", str(out)])
    if r.returncode:
        sys.exit(r.stderr)
    # 5. measure the delivered file
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(out), "-af", "ebur128=peak=true", "-f", "null", "-"])
    summ = r.stderr[r.stderr.rfind("Integrated loudness:"):]   # the summary block, not the running lines
    il = re.search(r"I:\s+(-?[\d.]+) LUFS", summ); tp = re.search(r"Peak:\s+(-?[\d.]+) dBFS", summ); lra = re.search(r"LRA:\s+([\d.]+) LU", summ)
    rep = {"video": str(video), "music": str(music), "sfx": str(sfx), "out": str(out), "pass1": m,
           "delivered": {"integrated_lufs": il.group(1) if il else None, "true_peak_dbtp": tp.group(1) if tp else None, "lra": lra.group(1) if lra else None},
           "levels": {"bed_db": -7, "sfx_db": -4, "bed_fade_out_s": 0.7, "loudnorm_tp_target": -4.0, "why": "AAC encoding overshoots true peak by ~2.3 dB on square-wave SFX (measured -0.3 dBTP from a -2.6 dBTP wav); target -4 keeps the delivered file <= -1"}}
    json.dump(rep, open(JOB / "gen/audio-mix.json", "w"), indent=1)
    print("delivered loudness:", rep["delivered"]); print("wrote", out)


if __name__ == "__main__":
    main()
