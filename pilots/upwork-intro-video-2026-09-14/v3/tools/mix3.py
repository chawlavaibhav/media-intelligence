#!/usr/bin/env python3
"""Audio for V3: VO paragraphs at beat anchors, Lyria bed looped with a crossfade (ducked under VO), restrained SFX
(soft shutter, UI tick, restrained whoosh) synthesised from primitives; loudnorm to -14 LUFS / <= -1 dBTP; mux with video.mp4.
usage: mix3.py <assembly_dir>"""
import json, math, subprocess, sys, wave
from pathlib import Path
import numpy as np

V3 = Path(__file__).resolve().parent.parent
GEN = V3 / "gen"
SR = 48000


def sfx(path: Path, kind: str):
    rng = np.random.default_rng(3)
    if kind == "shutter":   # soft shutter: two short filtered noise taps 40 ms apart
        n = int(0.16 * SR); t = np.arange(n) / SR; x = np.zeros(n)
        for off in (0.0, 0.045):
            i0 = int(off * SR); m = int(0.05 * SR); tt = np.arange(m) / SR
            burst = rng.normal(0, 1, m) * np.exp(-tt * 140); burst = np.convolve(burst, np.ones(9) / 9, mode="same")
            x[i0:i0 + m] += burst * 0.5
    elif kind == "tick":    # UI tick: short damped sine
        n = int(0.09 * SR); t = np.arange(n) / SR; x = np.sin(2 * math.pi * 1500 * t) * np.exp(-t * 60) * 0.35
    else:                   # restrained whoosh: band-limited noise with a slow swell and decay
        n = int(0.55 * SR); t = np.arange(n) / SR; env = np.sin(math.pi * t / 0.55) ** 2
        x = rng.normal(0, 1, n); x = np.convolve(x, np.ones(24) / 24, mode="same") - np.convolve(x, np.ones(200) / 200, mode="same"); x *= env * 0.55
    x = np.clip(x, -1, 1)
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes((x * 32767).astype(np.int16).tobytes())


def main(out_dir: str):
    out = Path(out_dir); tl = json.loads((out / "timeline.json").read_text()); S = tl["starts"]; total = tl["total_s"]
    takes = json.loads((V3 / "plan/VO-TAKES.json").read_text())
    vo_at = [S["s01-brief"] + 0.3, S["s03-freeze"] + 0.3, S["s07-master"] - 1.2, S["s08-stmo"] + 1.6, S["s12-exact"] - 0.4,
             S["s15-24h"] - 0.1, S["s17-intake"] + 0.3, S["s18-final"] + 0.2]
    sfxd = out / "sfx"; sfxd.mkdir(exist_ok=True)
    for k in ("shutter", "tick", "whoosh"):
        sfx(sfxd / f"{k}.wav", k)
    events = [(S["s03-freeze"] + 0.0, "shutter", 0.9)]
    events += [(S["s03-freeze"] + 1.25, "tick", 0.5)]
    events += [(S["s04-dirs"] + j * 0.75, "tick", 0.35) for j in range(4)]
    events += [(S["s05-sizes"] + 0.15 + j * 0.32, "tick", 0.45) for j in range(4)]
    events += [(S["s06-hooks"] + j * 0.37, "tick", 0.28) for j in range(6)]
    events += [(S["s06b-hindi"], "tick", 0.5), (S["s08-stmo"] + 0.5, "whoosh", 0.5), (S["s10a-b1"], "whoosh", 0.4), (S["s13-qa"] + 0.5, "tick", 0.6),
               (S["s15-24h"], "whoosh", 0.45), (S["s16-4h"], "tick", 0.5), (S["s17-intake"], "whoosh", 0.45)]
    inputs = ["-i", str(out / "video.mp4"), "-i", str(GEN / "audio/music-r4.wav")]
    for t in takes:
        inputs += ["-i", str(GEN / "audio" / t)]
    for ev in events:
        inputs += ["-i", str(sfxd / f"{ev[1]}.wav")]
    nv, ns = len(takes), len(events)
    fc = []
    vo_labels = []
    for i, at in enumerate(vo_at):
        fc.append(f"[{2 + i}:a]aresample={SR},aformat=channel_layouts=stereo,adelay={int(at * 1000)}|{int(at * 1000)}[v{i}]"); vo_labels.append(f"[v{i}]")
    fc.append(f"{''.join(vo_labels)}amix=inputs={nv}:normalize=0:duration=longest,loudnorm=I=-17:TP=-2:LRA=9,atrim=0:{total:.3f}[vo]")
    # music: loop the 32.8 s track with a 3 s crossfade (x3 covers 60 s), duck under VO with a sidechain, fade out at the end
    fc.append("[1:a]asplit=3[m0][m1][m2];[m0][m1]acrossfade=d=3:c1=tri:c2=tri[mm];[mm][m2]acrossfade=d=3:c1=tri:c2=tri[mloop]")
    fc.append(f"[mloop]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.8,afade=t=out:st={total - 2.2:.2f}:d=2.0,volume=0.30[musraw]")
    fc.append("[vo]asplit=2[vo1][vo2]")
    fc.append("[musraw][vo2]sidechaincompress=threshold=0.02:ratio=6:attack=40:release=500:makeup=1[mus]")
    labels = []
    for i, ev in enumerate(events):
        fc.append(f"[{2 + nv + i}:a]volume={ev[2]},aresample={SR},aformat=channel_layouts=stereo,adelay={int(ev[0] * 1000)}|{int(ev[0] * 1000)}[s{i}]"); labels.append(f"[s{i}]")
    fc.append(f"[vo1][mus]{''.join(labels)}amix=inputs={2 + ns}:normalize=0:duration=longest,atrim=0:{total:.3f}[aout]")
    mix = out / "mix.wav"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[aout]", "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s16le", str(mix)], check=True)
    meas = subprocess.run(["ffmpeg", "-i", str(mix), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    cur = float([l for l in meas.splitlines() if l.strip().startswith("I:")][-1].split()[1])
    gain = -14.0 - cur
    final = out / "upwork-intro-v3.mp4"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(out / "video.mp4"), "-i", str(mix), "-af", f"volume={gain:.2f}dB,alimiter=limit=0.82:attack=5:release=80:level=false",
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", str(SR), "-movflags", "+faststart", "-t", f"{total:.3f}", str(final)], check=True)
    meas = subprocess.run(["ffmpeg", "-i", str(final), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    I = [l for l in meas.splitlines() if l.strip().startswith("I:")][-1].strip(); P = [l for l in meas.splitlines() if "Peak:" in l][-1].strip()
    (out / "audio-report.json").write_text(json.dumps({"vo_at": vo_at, "events": events, "integrated": I, "true_peak": P, "gain_db": round(gain, 2)}, indent=1))
    print(final, I, P)


if __name__ == "__main__":
    main(sys.argv[1])
