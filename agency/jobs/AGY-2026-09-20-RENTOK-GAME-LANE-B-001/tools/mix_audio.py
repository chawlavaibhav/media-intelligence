#!/usr/bin/env python3
"""Audio assembly by code. USD 0. Music (Lyria, trimmed to 30 s with gain automation), three announcer lines at the measured
VO schedule (gate: check_vo_schedule), SFX on every contact event (CONTACT_EVENTS.json) — mixed in numpy at 48 kHz stereo,
then ffmpeg loudnorm (two-pass) to I=-14 LUFS / TP=-1 dBTP (Stage 2 §2.6 target), AAC-LC 48 kHz stereo 192 kbps, muxed
with the silent render into the final MP4 (faststart)."""
from __future__ import annotations

import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
JOB = HERE.parent
sys.path.insert(0, str(HERE))
import sfx_synth as S  # noqa: E402
from vo_schedule_gate import check_vo_schedule  # noqa: E402

SR = 48000
DUR = 30.0
TL = json.load(open(JOB / "gen/render/TIMELINE.json"))
EV = json.load(open(JOB / "gen/render/CONTACT_EVENTS.json"))
B = TL["beats"]


def load_mono(path: Path) -> np.ndarray:
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32).copy()


def load_stereo(path: Path) -> np.ndarray:
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32).reshape(-1, 2).copy()


def place(mix: np.ndarray, x: np.ndarray, t: float, gain: float = 1.0):
    i = int(t * SR); n = min(len(x), len(mix) - i)
    if n <= 0: return
    if x.ndim == 1:
        mix[i:i + n, 0] += x[:n] * gain; mix[i:i + n, 1] += x[:n] * gain
    else:
        mix[i:i + n] += x[:n] * gain


def main():
    N = int(DUR * SR)
    mix = np.zeros((N, 2), np.float32)
    # ── music: Lyria track, 30 s, fade out, gain automation (drop on the freeze, return after the install) ──
    mus = load_stereo(JOB / "gen/audio/A6_lyria_v1.wav")[:N]
    if len(mus) < N: mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))
    t = np.arange(N) / SR
    g = np.ones(N, np.float32) * 0.9
    f7, f9 = B["F7"][0], B["F9"][0] + 1.3
    v1_end = TL["vo_start"]["V1"] + 2.645
    g[(t >= f7) & (t < v1_end)] = 0.12                   # drops out on CONTINUE? (a low bed stays so the freeze is not dead air)
    g[(t >= v1_end) & (t < f9)] = 0.55                   # repair round 1, D-7: the bed comes back under the phone rise (no 0.6-s hole)
    g[t >= f9] = 1.0                                     # full and brighter at RENTOK MODE: ON
    # smooth the steps (50 ms)
    k = int(0.05 * SR); g = np.convolve(g, np.ones(k) / k, mode="same")
    # fade out over the last 0.6 s, silence in the last 0.2 s
    g[t > DUR - 0.8] *= np.clip((DUR - 0.2 - t[t > DUR - 0.8]) / 0.6, 0, 1)
    mix += mus * g[:, None]
    # ── VO (candidate A, Sarvam, one source): schedule from measured durations ──
    vo_lines = []
    for vid, start in TL["vo_start"].items():
        x = load_mono(JOB / f"gen/voice/A_sarvam_{vid}.wav")
        dur = len(x) / SR
        vo_lines.append({"id": vid, "start_s": start, "duration_s": round(dur, 3), "end_s": round(start + dur, 3)})
        place(mix, x, start, gain=1.6)
        # duck music under the line (-6 dB) with 80 ms ramps
        i0, i1 = int(start * SR), int((start + dur) * SR)
        r = int(0.08 * SR)
        duck = np.ones(N, np.float32); duck[i0:i1] = 0.5
        duck[max(0, i0 - r):i0] = np.linspace(1, 0.5, min(r, i0)); duck[i1:i1 + r] = np.linspace(0.5, 1, min(r, N - i1))
        mix -= mus * g[:, None] * (1 - duck)[:, None]
    gate = check_vo_schedule(vo_lines, film_end_s=DUR - 0.2, min_gap_s=0.1)
    # ── SFX ──
    sfx = {k: fn() for k, fn in S.SFX.items()}
    # steps during the runs
    for tt in np.arange(0.0, B["F7"][0], 0.2): place(mix, sfx["step"], tt, 0.5)
    for tt in np.arange(B["F10"][0], B["F15"][0], 0.2): place(mix, sfx["step"], tt, 0.5)
    for e in EV:
        if e["kind"] == "struggle_contact":
            snd = {"O1": "hurt", "O2": "thud", "O3": "hurt", "O4": "rustle", "O5": "ringbuzz"}[e["obstacle"]]
            place(mix, sfx[snd], e["t"], 0.9)
            if e["obstacle"] == "O5": place(mix, sfx["ringbuzz"], e["t"] + 0.4, 0.7)
        elif e["kind"] == "beam_hit_transform":
            place(mix, sfx["beam"], e["t"] - 0.25, 0.8); place(mix, sfx["stamp"], e["t"], 0.9)
            if e["obstacle"] == "O5": place(mix, sfx["stamp"], e["t"] + 0.12, 0.7); place(mix, sfx["stamp"], e["t"] + 0.24, 0.7)
        elif e["kind"] == "flag_capture":
            place(mix, sfx["flagzip"], e["t"], 0.8); place(mix, sfx["fanfare"], e["t"] + 0.4, 0.8)
    # freeze heartbeat, cheat-code typing, install chime
    for tt in np.arange(B["F7"][0] + 0.1, B["F8"][0], 0.7): place(mix, sfx["heartbeat"], tt, 0.7)
    n = len("INSTALL RENTOK")
    for i in range(n): place(mix, sfx["keyblip"], B["F8"][0] + 0.15 + i * (1.1 / n), 0.5)
    place(mix, sfx["beam"], B["F9"][0] + 0.2, 0.5)      # rising hum as the phone rises (fills the gap between V1 and V2)
    place(mix, sfx["chime"], B["F9"][0] + 0.9, 0.9)
    place(mix, sfx["chime"], B["F9"][0] + 1.3, 0.6)
    # ── write, normalise, mux ──
    out = JOB / "gen/audio"; out.mkdir(parents=True, exist_ok=True)
    raw = out / "mix_raw.wav"
    peak = float(np.abs(mix).max()); mix = mix / max(peak, 1.0) * 0.9
    with wave.open(str(raw), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes())
    # two-pass loudnorm
    r = subprocess.run(["ffmpeg", "-v", "info", "-i", str(raw), "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
    js = r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1]; m = json.loads(js)
    af = (f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
          f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true:print_format=summary")
    norm = out / "mix_norm.wav"
    # repair R2 (audio): loudnorm alone left TP at +0.6 dBTP (dynamic mode, +4.8 dB of gain needed); a true-peak limiter follows it
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-af", af + ",alimiter=limit=0.66:attack=3:release=40:level=false", "-ar", str(SR), str(norm)], check=True)
    final = JOB / "gen/final"; final.mkdir(parents=True, exist_ok=True)
    fp = final / "rentok-game-lane-b-9x16-30s.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(JOB / "gen/render/video_silent.mp4"), "-i", str(norm), "-map", "0:v:0", "-map", "1:a:0",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2", "-shortest", "-movflags", "+faststart", str(fp)], check=True)
    json.dump({"vo_lines": vo_lines, "vo_gate": gate, "loudnorm_pass1": m}, open(out / "MIX_REPORT.json", "w"), indent=1, default=str)
    print("vo gate:", gate); print("final:", fp)


if __name__ == "__main__":
    main()
