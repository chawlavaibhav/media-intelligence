#!/usr/bin/env python3
"""assemble_v2.py — mix + mux for the full 30 s. PROVENANCE: levels, two-pass loudnorm (I=-14, TP=-4 pre-encode), mux flags
(-use_editlist 0, +faststart+negative_cts_offsets) from Lane A tools/assemble.py @ 7dab37a; the bed PROCESSING generalises
Treatment C assemble_c.py @ 41d97c6 to the whole film, driven by the board's bed cues:
  bed_duck  (each of the first four hits): bed cut for the 0.1-s hit-stop, then 0.5 x until +0.5 s
  bed_cold  (the swarm hit 14.1): cut 0.1 s, then low-pass 800 Hz at 0.45 x until 17.3, then 0.06 x (near-silence) to the flash 17.6
  bed_level2 (17.6): the bed returns full-band ONE SEMITONE UP (asetrate x1.05946 + atempo 0.943874) — "level 2"; fade-out 29.3-30.0
usage: assemble_v2.py <video.mp4> <music.wav> <out.mp4>   (writes gen/audio-v2-raw.wav, gen/audio-v2-mix.wav, gen/audio-v2-mix.json)"""
import json, re, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; JOB = HERE.parent
def run(cmd): return subprocess.run(cmd, capture_output=True, text=True)
video, music, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
board = json.load(open(JOB / "board.json"))
sfx = JOB / "gen/sfx-v2-stem.wav"; mix = JOB / "gen/audio-v2-raw.wav"; norm = JOB / "gen/audio-v2-mix.wav"
FLASH = board["flash_t"]
ducks = sorted(e["t"] for f in board["frames"] for e in f["impact"] if e["primitive"] == "audio" and e["cue"] == "bed_duck")
cold = next(e["t"] for f in board["frames"] for e in f["impact"] if e["primitive"] == "audio" and e["cue"] == "bed_cold")
# volume expression over the first segment (0..FLASH): ducks, cold cut, low band level, near-silence
expr = "1"
for h in ducks:
    expr = f"if(between(t,{h},{h + 0.1}),0,if(between(t,{h + 0.1},{h + 0.5}),0.5,{expr}))"
expr = f"if(between(t,{cold},{cold + 0.1}),0,if(between(t,{cold + 0.1},{FLASH - 0.3}),0.45,if(between(t,{FLASH - 0.3},{FLASH}),0.06,{expr})))"
seg2 = 30.0 - FLASH
graph = ("[0:a]atrim=0:30,asetpts=PTS-STARTPTS,afade=t=in:d=0.15,volume=-7dB,asplit[b1][b2];"
         f"[b1]atrim=0:{FLASH},asetpts=PTS-STARTPTS,lowpass=f=800:enable='between(t,{cold + 0.1},{FLASH})',volume=eval=frame:volume='{expr}'[p1];"
         f"[b2]atrim={FLASH}:30,asetpts=PTS-STARTPTS,asetrate=48000*1.05946,aresample=48000,atempo=0.943874,afade=t=out:st={seg2 - 0.7:.3f}:d=0.7[p2];"
         "[p1][p2]concat=n=2:v=0:a=1[bed];[1:a]volume=-4dB[s];[bed][s]amix=inputs=2:duration=first:normalize=0[mix]")
r = run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(music), "-i", str(sfx), "-filter_complex", graph, "-map", "[mix]", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(mix)])
if r.returncode: sys.exit(r.stderr)
r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(mix), "-af", "loudnorm=I=-14:TP=-4:LRA=11:print_format=json", "-f", "null", "-"])
blob = r.stderr[r.stderr.rfind("{"):]; blob = blob[: blob.find("}") + 1]; m = json.loads(blob)
af = (f"loudnorm=I=-14:TP=-4:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
      f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true:print_format=json"
      ",alimiter=limit=0.5:attack=3:release=40:level=false,volume=1.5dB")   # v2: true limiter at -6 dBFS after loudnorm — the denser SFX peaked at -0.4 dBTP after AAC without it
r = run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mix), "-af", af, "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(norm)])
if r.returncode: sys.exit(r.stderr)
out.parent.mkdir(parents=True, exist_ok=True)
r = run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-i", str(norm), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-shortest",
         "-movflags", "+faststart+negative_cts_offsets", "-use_editlist", "0", str(out)])
if r.returncode: sys.exit(r.stderr)
r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(out), "-af", "ebur128=peak=true", "-f", "null", "-"])
summ = r.stderr[r.stderr.rfind("Integrated loudness:"):]
il = re.search(r"I:\s+(-?[\d.]+) LUFS", summ); tp = re.search(r"Peak:\s+(-?[\d.]+) dBFS", summ); lra = re.search(r"LRA:\s+([\d.]+) LU", summ)
rep = {"video": str(video), "music": str(music), "sfx": str(sfx), "out": str(out), "pass1": m, "bed_processing": graph, "ducks": ducks, "cold": cold, "flash": FLASH,
       "delivered": {"integrated_lufs": il.group(1) if il else None, "true_peak_dbtp": tp.group(1) if tp else None, "lra": lra.group(1) if lra else None},
       "levels": {"bed_db": -7, "sfx_db": -4, "loudnorm_tp_target": -4.0, "limiter": "alimiter -6 dBFS", "why": "Lane A: AAC overshoots true peak by ~2.3 dB on square-wave SFX; loudnorm TP -4 + a -6 dBFS limiter keeps the file <= -1 dBTP with I near -14"}}
json.dump(rep, open(JOB / "gen/audio-v2-mix.json", "w"), indent=1); print("delivered loudness:", rep["delivered"]); print("wrote", out)
