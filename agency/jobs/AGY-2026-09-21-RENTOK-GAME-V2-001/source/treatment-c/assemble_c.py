#!/usr/bin/env python3
"""assemble_c.py — Treatment C mix + mux for the 14.0–20.8 s window.
PROVENANCE: levels, two-pass loudnorm (I=-14, TP=-4 pre-encode) and the mux flags are Lane A tools/assemble.py @ 7dab37a;
the bed PROCESSING is new (05 §2b audio progression): bed cut for the 0.1-s hit-stop, low-passed (800 Hz) and -7 dB from
the hit to the flash, near-silent (-24 dB) 0.3 s before the flash, then full-band and one semitone up ("level 2").
usage: assemble_c.py <video.mp4> <music.wav> <out.mp4>"""
import json, re, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; JOB = HERE.parent
def run(cmd): return subprocess.run(cmd, capture_output=True, text=True)
video, music, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
sfx = JOB / "gen/sfx-c-stem.wav"; mix = JOB / "gen/audio-c-raw.wav"; norm = JOB / "gen/audio-c-mix.wav"
FLASH = 3.6   # 17.6 - 14.0
graph = ("[0:a]atrim=14:20.8333,asetpts=PTS-STARTPTS,volume=-7dB,asplit[b1][b2];"
         f"[b1]atrim=0:{FLASH},asetpts=PTS-STARTPTS,lowpass=f=800:enable='between(t,0.2,{FLASH})',"
         f"volume=eval=frame:volume='if(lt(t,0.1),1,if(lt(t,0.2),0,if(lt(t,3.3),0.45,0.06)))'[p1];"
         f"[b2]atrim={FLASH},asetpts=PTS-STARTPTS,asetrate=48000*1.05946,aresample=48000,atempo=0.943874[p2];"
         "[p1][p2]concat=n=2:v=0:a=1[bed];[1:a]volume=-4dB[s];[bed][s]amix=inputs=2:duration=first:normalize=0[mix]")
r = run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(music), "-i", str(sfx), "-filter_complex", graph, "-map", "[mix]", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(mix)])
if r.returncode: sys.exit(r.stderr)
r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(mix), "-af", "loudnorm=I=-14:TP=-4:LRA=11:print_format=json", "-f", "null", "-"])
blob = r.stderr[r.stderr.rfind("{"):]; blob = blob[: blob.find("}") + 1]; m = json.loads(blob)
af = (f"loudnorm=I=-14:TP=-4:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
      f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true:print_format=json")
r = run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mix), "-af", af, "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(norm)])
if r.returncode: sys.exit(r.stderr)
r = run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-i", str(norm), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart+negative_cts_offsets", "-use_editlist", "0", str(out)])
if r.returncode: sys.exit(r.stderr)
r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(out), "-af", "ebur128=peak=true", "-f", "null", "-"])
summ = r.stderr[r.stderr.rfind("Integrated loudness:"):]
il = re.search(r"I:\s+(-?[\d.]+) LUFS", summ); tp = re.search(r"Peak:\s+(-?[\d.]+) dBFS", summ)
rep = {"video": str(video), "music": str(music), "sfx": str(sfx), "out": str(out), "pass1": m, "delivered": {"integrated_lufs": il.group(1) if il else None, "true_peak_dbtp": tp.group(1) if tp else None}, "bed_processing": graph}
json.dump(rep, open(JOB / "gen/audio-c-mix.json", "w"), indent=1); print("delivered loudness:", rep["delivered"]); print("wrote", out)
