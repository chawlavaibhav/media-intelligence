#!/usr/bin/env python3
"""V4 audio: the speaker's native audio (0–7.75 s, untouched, no time-stretch), the accepted V3 Lyria bed re-edited
(enters under the last word, one loop with a crossfade, sidechain-ducked under speech), three restrained ticks; two-pass
loudness to -14 LUFS with a true-peak limiter. usage: mix4.py <assembly_dir>"""
import json, math, subprocess, sys, wave
from pathlib import Path
import numpy as np

V4 = Path(__file__).resolve().parent.parent; V3G = V4.parent / "v3" / "gen"; SR = 48000


def tick(path: Path, kind: str):
    if kind == "tick":
        n = int(0.09 * SR); t = np.arange(n) / SR; x = np.sin(2 * math.pi * 1400 * t) * np.exp(-t * 55) * 0.3
    else:  # soft air for the handoff
        rng = np.random.default_rng(5); n = int(0.5 * SR); t = np.arange(n) / SR; env = np.sin(math.pi * t / 0.5) ** 2
        x = rng.normal(0, 1, n); x = np.convolve(x, np.ones(30) / 30, mode="same") - np.convolve(x, np.ones(240) / 240, mode="same"); x *= env * 0.4
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())


def main(out_dir):
    out = Path(out_dir); tl = json.loads((out / "timeline.json").read_text()); S = tl["starts"]; total = tl["total_s"]
    spk = V4 / "gen/speaker/speaker-accepted.mp4"; music = V3G / "audio/music-r4.wav"
    sfx = out / "sfx"; sfx.mkdir(exist_ok=True); tick(sfx / "tick.wav", "tick"); tick(sfx / "air.wav", "air")
    ev = [(S["b2-handoff"], "air", 0.35), (S["b4-proof2"] + 1.5, "tick", 0.4), (S["b4-proof2"] + 3.1, "tick", 0.4), (S["b4-proof2"] + 4.7, "tick", 0.4),
          (S["b8-speed"], "tick", 0.3), (S["b8-speed"] + 2.6, "tick", 0.3)]
    m_in = 7.0
    inputs = ["-i", str(out / "video.mp4"), "-i", str(spk), "-i", str(music)] + sum([["-i", str(sfx / f"{k}.wav")] for _, k, _ in ev], [])
    fc = [f"[1:a]atrim=0:7.75,asetpts=PTS-STARTPTS,aresample={SR},aformat=channel_layouts=stereo,loudnorm=I=-15:TP=-2:LRA=6,apad=whole_dur={total:.3f}[spk]",
          "[2:a]asplit=2[m0][m1];[m0][m1]acrossfade=d=3:c1=tri:c2=tri[mloop]",
          f"[mloop]atrim=0:{total - m_in:.3f},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=2.5,afade=t=out:st={total - m_in - 2.5:.2f}:d=2.4,acompressor=threshold=0.16:ratio=4:attack=8:release=220:makeup=1.6,volume=0.55,adelay={int(m_in * 1000)}|{int(m_in * 1000)},apad=whole_dur={total:.3f}[musraw]",
          "[spk]asplit=2[spk1][spk2]", "[musraw][spk2]sidechaincompress=threshold=0.03:ratio=5:attack=30:release=600:makeup=1[mus]"]
    labels = []
    for i, (t, k, v) in enumerate(ev):
        fc.append(f"[{3 + i}:a]volume={v},aresample={SR},aformat=channel_layouts=stereo,adelay={int(t * 1000)}|{int(t * 1000)}[s{i}]"); labels.append(f"[s{i}]")
    fc.append(f"[spk1][mus]{''.join(labels)}amix=inputs={2 + len(ev)}:normalize=0:duration=longest,atrim=0:{total:.3f}[aout]")
    mix = out / "mix.wav"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[aout]", "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s16le", str(mix)], check=True)
    mix2 = out / "mix-comp.wav"   # gentle glue compression first, then measure, then one clean gain + true-peak limiter
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(mix), "-af", "acompressor=threshold=0.16:ratio=2.5:attack=15:release=250:makeup=1", "-c:a", "pcm_s16le", str(mix2)], check=True)
    mix = mix2
    meas = subprocess.run(["ffmpeg", "-i", str(mix), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    cur = float([l for l in meas.splitlines() if l.strip().startswith("I:")][-1].split()[1]); gain = -14.0 - cur
    final = out / "upwork-intro-v4.mp4"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(out / "video.mp4"), "-i", str(mix), "-af", f"volume={gain:.2f}dB,alimiter=limit=0.76:attack=4:release=120:level=false",
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", str(SR), "-movflags", "+faststart", "-t", f"{total:.3f}", str(final)], check=True)
    meas = subprocess.run(["ffmpeg", "-i", str(final), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    I = [l for l in meas.splitlines() if l.strip().startswith("I:")][-1].strip(); P = [l for l in meas.splitlines() if "Peak:" in l][-1].strip(); LRA = [l for l in meas.splitlines() if l.strip().startswith("LRA:")][-1].strip()
    (out / "audio-measure.json").write_text(json.dumps({"integrated": I, "true_peak": P, "lra": LRA, "gain_db": round(gain, 2), "music_in_s": m_in, "events": ev}, indent=1))
    print(final, I, P, LRA)


if __name__ == "__main__":
    main(sys.argv[1])
