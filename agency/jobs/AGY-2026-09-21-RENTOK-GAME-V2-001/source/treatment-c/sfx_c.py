#!/usr/bin/env python3
"""sfx_c.py — Treatment C SFX stem for the 14.0–20.8 s window (times are window-relative: t - 14.0).
PROVENANCE: cue synthesis copied from Lane A tools/sfx.py @ 7dab37a (square/noise + envelope); the new cues
(thump, riser, whoosh, bass drop, impact) are written here for the direction in 05 §2b. Writes gen/sfx-c-stem.wav (48 kHz stereo)."""
import sys, wave
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent; JOB = HERE.parent
sys.path.insert(0, str(HERE))
SR = 48000; DUR = 6.8333; T0 = 14.0

def env(n, a=0.005, d=0.08, s=0.0, r=0.05, hold=0.0):
    e = np.ones(n); at = int(a * SR); dt = int(d * SR); ht = int(hold * SR)
    if at: e[:at] = np.linspace(0, 1, at)
    e[at:at + dt] = np.linspace(1, s if s else 0.0001, dt)
    e[at + dt:at + dt + ht] = s
    tail = n - (at + dt + ht)
    if tail > 0: e[at + dt + ht:] = np.linspace(s if s else 0.0001, 0, tail)
    return e
def square(freq, dur, vol=0.3, duty=0.5, sweep=0.0):
    n = int(dur * SR); t = np.arange(n) / SR; f = freq * (2 ** (sweep * t / max(dur, 1e-6))); ph = np.cumsum(f) / SR
    return vol * np.where((ph % 1.0) < duty, 1.0, -1.0)
def sine(freq, dur, vol=0.3, sweep=0.0):
    n = int(dur * SR); t = np.arange(n) / SR; f = freq * (2 ** (sweep * t / max(dur, 1e-6))); return vol * np.sin(2 * np.pi * np.cumsum(f) / SR)
def noise(dur, vol=0.3, seed=7):
    return vol * np.random.default_rng(seed).uniform(-1, 1, int(dur * SR))
def lowpass(x, fc):
    a = 1 - np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); acc = 0.0
    for i in range(len(x)): acc += a * (x[i] - acc); y[i] = acc
    return y
# Lane A cues (verbatim)
def cue_hit():   s = square(220, 0.22, 0.32, 0.25, sweep=-1.5) + noise(0.22, 0.18); return s * env(len(s), d=0.2)
def cue_key():   s = square(1600, 0.045, 0.22, 0.5); return s * env(len(s), a=0.002, d=0.04)
def cue_low():   s = square(70, 0.8, 0.28, 0.5, sweep=-0.5); return s * env(len(s), a=0.05, d=0.7)
def cue_pew():   s = square(900, 0.12, 0.26, 0.3, sweep=-2.0) + square(200, 0.12, 0.12, 0.5, sweep=-1.0); return s * env(len(s), d=0.1)   # + a 200-Hz body (05 §2b beat 7)
def cue_burst(): s = noise(0.28, 0.3) + square(110, 0.28, 0.2, 0.5, sweep=-1.0); return s * env(len(s), d=0.26)
def cue_ding():  s = square(1320, 0.14, 0.2, 0.5) + square(1980, 0.14, 0.12, 0.5); return s * env(len(s), d=0.12)
def motif(notes, step=0.09, vol=0.26):
    out = []
    for f in notes: s = square(f, step, vol, 0.5); out.append(s * env(len(s), d=step * 0.9))
    return np.concatenate(out)
def cue_powerup(): return motif([523.25, 659.25, 783.99, 1046.5, 1318.5], step=0.09)
# C cues
def cue_thump():   s = sine(60, 0.3, 0.6, sweep=-0.6); return s * env(len(s), a=0.003, d=0.28)
def cue_riser():   s = lowpass(noise(0.22, 0.5, 3), 400) * 4; return s * np.linspace(0.05, 1.0, len(s)) ** 2
def cue_whoosh():  s = lowpass(noise(0.3, 0.5, 11), 2500) * 2 - lowpass(noise(0.3, 0.5, 11), 300) * 2; return s * env(len(s), a=0.01, d=0.28)
def cue_bassdrop(): s = sine(110, 0.5, 0.5, sweep=-1.5); return s * env(len(s), a=0.002, d=0.45)
def cue_impact():  s = noise(0.12, 0.5, 5) + sine(160, 0.12, 0.5, sweep=-1.0); return s * env(len(s), a=0.001, d=0.11)
def cue_sparks():  s = square(2400, 0.06, 0.12, 0.5, sweep=1.0); return s * env(len(s), d=0.05)

def main():
    cues = [(14.0, cue_riser), (14.1, cue_thump), (14.1, cue_hit), (14.2, cue_low)]
    cues += [(15.8 + i * (1.4 / 17), cue_key) for i in range(17)]
    cues += [(17.6, cue_impact), (17.6, cue_bassdrop), (17.62, cue_powerup)]
    cues += [(17.7 + i * 0.07, cue_sparks) for i in range(6)]
    cues += [(18.4, cue_pew), (19.9, cue_pew), (20.35, cue_burst), (20.35, cue_thump), (20.36, cue_whoosh), (20.7, cue_ding)]
    stem = np.zeros(int(DUR * SR))
    for t, fn in cues:
        s = fn(); i = int((t - T0) * SR); j = min(len(stem), i + len(s))
        if i < len(stem): stem[i:j] += s[: j - i]
    stem = np.clip(stem, -1, 1); st = np.stack([stem, stem], axis=1)
    out = JOB / "gen/sfx-c-stem.wav"
    with wave.open(str(out), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
    print("wrote", out, "cues", len(cues))
if __name__ == "__main__": main()
