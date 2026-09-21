#!/usr/bin/env python3
"""assemble.py — the film from the board: trim each beat clip to use_s, upscale 720x1280 -> 1080x1920, hard cuts between beats,
0.6-s crossfade into the code end card, the wordmark super 5.0-7.5 s, native Veo ambience + the Lyria bed (from 7.5 s),
two-pass loudnorm I=-14 TP=-4 + alimiter (RentOK v2 assemble_v2.py @ ffefe44b; PROVENANCE.md), mux with no edit lists + faststart.
usage: assemble.py [--music gen/music/bed.wav] [--out gen/final/mokobara-odyssey-9x16-30s.mp4] [--clip b4=gen/clips/b4-take2.mp4 ...]"""
import argparse, json, re, subprocess, sys
from pathlib import Path
JOB = Path(__file__).resolve().parent.parent
ap = argparse.ArgumentParser(); ap.add_argument("--music", default=None); ap.add_argument("--out", default="gen/final/mokobara-odyssey-9x16-30s.mp4")
ap.add_argument("--clip", action="append", default=[], help="beat=path override"); a = ap.parse_args()
board = json.load(open(JOB / "board.json")); beats = [b for b in board["beats"] if b["clip_s"] > 0]
over = dict(c.split("=", 1) for c in a.clip)
clips = [JOB / over.get(f"b{b['n']}", f"gen/clips/b{b['n']}.mp4") for b in beats]
XF = 0.6; card_s = 2.0 + XF; total_v = sum(b["use_s"] for b in beats)      # 28.0
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit(r.stderr[-2000:])
    return r
inputs = []
for c in clips: inputs += ["-i", str(c)]
inputs += ["-loop", "1", "-t", f"{card_s}", "-i", str(JOB / "gen/overlays/endcard.png"), "-loop", "1", "-t", "3", "-i", str(JOB / "gen/overlays/super.png")]
n = len(clips); iec, isup = n, n + 1
f = []
for i, b in enumerate(beats):
    f.append(f"[{i}:v]trim=0:{b['use_s']},setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1,fps=24,format=yuv420p[v{i}]")
    f.append(f"[{i}:a]atrim=0:{b['use_s']},asetpts=PTS-STARTPTS,aresample=48000,afade=t=in:d=0.04,afade=t=out:st={b['use_s'] - 0.06:.3f}:d=0.06[a{i}]")
f.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,settb=AVTB[vcat]")
f.append("".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[acat]")
f.append(f"[{iec}:v]scale=1080:1920,setsar=1,fps=24,format=yuv420p,settb=AVTB[ec]")
f.append(f"[vcat][ec]xfade=transition=fade:duration={XF}:offset={total_v - XF}[vx]")
sup = json.load(open(JOB / "copy-deck.json"))["placements"]["wordmark_super"]; t0, t1 = sup["t_in"], sup["t_out"]
f.append(f"[{isup}:v]format=rgba,fade=t=in:st=0:d=0.3:alpha=1,fade=t=out:st={t1 - t0 - 0.3:.2f}:d=0.3:alpha=1,setpts=PTS+{t0}/TB[sp]")
f.append(f"[vx][sp]overlay=0:0:eof_action=pass:enable='between(t,{t0},{t1})'[vout]")
if a.music:
    inputs += ["-i", a.music]; im = n + 2
    f.append(f"[{im}:a]aresample=48000,atrim=0:{30 - 7.5},asetpts=PTS-STARTPTS,afade=t=in:d=2.0,afade=t=out:st={30 - 7.5 - 1.8:.2f}:d=1.8,adelay=7500|7500,volume=-9dB[bed]")
    f.append("[acat]apad=whole_dur=30,volume=-4dB[amb];[amb][bed]amix=inputs=2:duration=first:normalize=0[amix]")
else:
    f.append("[acat]apad=whole_dur=30,volume=-4dB[amix]")
raw = JOB / "gen/audio-raw.wav"; norm = JOB / "gen/audio-mix.wav"; vid = JOB / "gen/video-only.mp4"
run(["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-filter_complex", ";".join(f), "-map", "[vout]", "-map", "[amix]", "-t", "30",
     "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", "24", "-c:a", "pcm_s16le", str(JOB / "gen/assembled-raw.mov")])
run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(JOB / "gen/assembled-raw.mov"), "-map", "0:a", "-c:a", "pcm_s16le", str(raw)])
run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(JOB / "gen/assembled-raw.mov"), "-map", "0:v", "-c:v", "copy", str(vid)])
r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(raw), "-af", "loudnorm=I=-14:TP=-4:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
blob = r.stderr[r.stderr.rfind("{"):]; blob = blob[: blob.find("}") + 1]; m = json.loads(blob)
af = (f"loudnorm=I=-14:TP=-4:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
      f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true:print_format=json,alimiter=limit=0.5:attack=3:release=40:level=false,volume=1.5dB")
run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-af", af, "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(norm)])
out = JOB / a.out; out.parent.mkdir(parents=True, exist_ok=True)
run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(vid), "-i", str(norm), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
     "-shortest", "-movflags", "+faststart+negative_cts_offsets", "-use_editlist", "0", str(out)])
r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(out), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
summ = r.stderr[r.stderr.rfind("Integrated loudness:"):]
il = re.search(r"I:\s+(-?[\d.]+) LUFS", summ); tp = re.search(r"Peak:\s+(-?[\d.]+) dBFS", summ)
rep = {"out": str(out), "clips": [str(c) for c in clips], "music": a.music, "beats": [(b["n"], b["use_s"]) for b in beats], "xfade_s": XF, "pass1": m,
       "delivered": {"integrated_lufs": il.group(1) if il else None, "true_peak_dbtp": tp.group(1) if tp else None}}
json.dump(rep, open(JOB / "gen/assemble-report.json", "w"), indent=1); print("delivered loudness:", rep["delivered"]); print("wrote", out)
