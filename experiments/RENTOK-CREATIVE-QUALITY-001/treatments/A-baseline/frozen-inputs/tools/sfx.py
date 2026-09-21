#!/usr/bin/env python3
"""sfx.py — the SFX stem, synthesised by code (Stage 4 A11) at the board's timestamps. No sampled sound anywhere.
Writes gen/sfx-stem.wav (48 kHz stereo, 30.0 s). Every cue is an original square/noise tone with an envelope; the
power-up arpeggio and the flag fanfare are short motifs written for this job (not any existing game's jingle).
"""
from __future__ import annotations

import json
import sys
import wave
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
JOB = HERE.parent
SR = 48000
DUR = 30.0


def env(n, a=0.005, d=0.08, s=0.0, r=0.05, hold=0.0):
    t = np.arange(n) / SR
    e = np.ones(n)
    at = int(a * SR); dt = int(d * SR); ht = int(hold * SR); rt = int(r * SR)
    e[:at] = np.linspace(0, 1, at) if at else 1
    e[at:at + dt] = np.linspace(1, s if s else 0.0001, dt)
    e[at + dt:at + dt + ht] = s
    tail = n - (at + dt + ht)
    if tail > 0:
        e[at + dt + ht:] = np.linspace(s if s else 0.0001, 0, tail)
    return e


def square(freq, dur, vol=0.3, duty=0.5, sweep=0.0):
    n = int(dur * SR); t = np.arange(n) / SR
    f = freq * (2 ** (sweep * t / max(dur, 1e-6)))
    ph = np.cumsum(f) / SR
    return vol * np.where((ph % 1.0) < duty, 1.0, -1.0)


def noise(dur, vol=0.3):
    rng = np.random.default_rng(7)
    return vol * rng.uniform(-1, 1, int(dur * SR))


def cue_jump():      s = square(300, 0.18, 0.28, 0.5, sweep=1.2); return s * env(len(s), d=0.15)
def cue_hit():       s = square(220, 0.22, 0.32, 0.25, sweep=-1.5) + noise(0.22, 0.18); return s * env(len(s), d=0.2)
def cue_trip():      s = square(180, 0.3, 0.28, 0.5, sweep=-1.0); return s * env(len(s), d=0.28)
def cue_key():       s = square(1600, 0.045, 0.22, 0.5); return s * env(len(s), a=0.002, d=0.04)
def cue_low():       s = square(70, 0.8, 0.28, 0.5, sweep=-0.5); return s * env(len(s), a=0.05, d=0.7)
def cue_pew():       s = square(900, 0.12, 0.26, 0.3, sweep=-2.0); return s * env(len(s), d=0.1)
def cue_burst():     s = noise(0.28, 0.3) + square(110, 0.28, 0.2, 0.5, sweep=-1.0); return s * env(len(s), d=0.26)
def cue_ding():      s = square(1320, 0.14, 0.2, 0.5) + square(1980, 0.14, 0.12, 0.5); return s * env(len(s), d=0.12)
def cue_tag():       s = square(660, 0.08, 0.22, 0.5) + square(990, 0.08, 0.18, 0.5); return s * env(len(s), d=0.07)
def cue_end():       s = square(196, 0.6, 0.25, 0.5) + square(392, 0.6, 0.12, 0.5); return s * env(len(s), a=0.01, d=0.55)


def motif(notes, step=0.09, vol=0.26):
    out = []
    for f in notes:
        s = square(f, step, vol, 0.5); out.append(s * env(len(s), d=step * 0.9))
    return np.concatenate(out)


def cue_powerup():   return motif([523.25, 659.25, 783.99, 1046.5, 1318.5], step=0.09)            # C E G C E, rising (original)
def cue_fanfare():   return motif([783.99, 783.99, 880.0, 1046.5, 1318.5, 1046.5], step=0.13, vol=0.28)  # G G A C E C (original)


def main():
    board = json.load(open(JOB / "board.json"))
    f = {x["n"]: x for x in board["frames"]}
    cues = []
    cues += [(0.6, cue_jump), (5.6, cue_jump), (26.2, cue_jump)]
    cues += [(3.3, cue_hit), (6.1, cue_hit), (8.6, cue_trip), (11.7, cue_hit), (14.1, cue_hit), (14.2, cue_low)]
    for i in range(17):
        cues.append((15.8 + i * (1.4 / 17), cue_key))
    cues += [(17.4, cue_powerup), (18.4, cue_pew)]
    for n in ["F9.1", "F9.2", "F9.3", "F9.4", "F9.5"]:
        t0 = f[n]["t0"]
        cues += [(t0 + 0.3, cue_pew), (t0 + 0.75, cue_tag if n == "F9.3" else cue_burst), (t0 + 1.1, cue_ding)]
    cues += [(26.6, cue_fanfare), (27.6, cue_end)]
    stem = np.zeros(int(DUR * SR))
    for t, fn in cues:
        s = fn(); i = int(t * SR); j = min(len(stem), i + len(s)); stem[i:j] += s[: j - i]
    stem = np.clip(stem, -1, 1)
    st = np.stack([stem, stem], axis=1)
    out = JOB / "gen/sfx-stem.wav"
    with wave.open(str(out), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
    print("wrote", out, "cues", len(cues))


if __name__ == "__main__":
    main()
