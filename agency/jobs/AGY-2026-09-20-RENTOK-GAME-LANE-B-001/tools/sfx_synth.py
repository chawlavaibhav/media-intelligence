#!/usr/bin/env python3
"""Ten synthesised game sound effects (numpy, 48 kHz mono float32). USD 0. Original waveforms — no samples, no borrowed
melodies (Stage 2 §2.5). Each effect is a few square/triangle/noise segments with an envelope."""
from __future__ import annotations

import numpy as np

SR = 48000


def env(n, a=0.005, d=0.05, s=0.6, r=0.05):
    t = np.arange(n) / SR; T = n / SR
    e = np.ones(n)
    ai, di, ri = int(a * SR), int(d * SR), int(r * SR)
    e[:ai] = np.linspace(0, 1, max(ai, 1))
    e[ai:ai + di] = np.linspace(1, s, max(di, 1))[: max(0, min(di, n - ai))]
    e[ai + di:n - ri] = s
    e[n - ri:] = np.linspace(s, 0, max(ri, 1))[-ri:] if ri > 0 else e[n - ri:]
    return e


def square(f, dur, duty=0.5, sweep=0.0):
    n = int(dur * SR); t = np.arange(n) / SR
    fi = f * (1 + sweep * t / dur)
    ph = np.cumsum(fi) / SR
    return np.where((ph % 1.0) < duty, 1.0, -1.0).astype(np.float32)


def tri(f, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    return (2 * np.abs(2 * ((t * f) % 1.0) - 1) - 1).astype(np.float32)


def noise(dur):
    return np.random.default_rng(7).uniform(-1, 1, int(dur * SR)).astype(np.float32)


def seq(parts):
    return np.concatenate([p for p in parts]).astype(np.float32)


def step():          # soft tick
    n = int(0.05 * SR); return (noise(0.05) * env(n, 0.001, 0.02, 0.2, 0.02) * 0.25)
def hurt():          # descending square blip
    s = square(520, 0.22, 0.25, sweep=-0.6); return s * env(len(s), 0.002, 0.05, 0.5, 0.08) * 0.6
def thud():          # low triangle + noise
    a = tri(90, 0.18) * env(int(0.18 * SR), 0.002, 0.08, 0.3, 0.06); b = noise(0.18) * env(int(0.18 * SR), 0.001, 0.03, 0.1, 0.05) * 0.3
    return (a + b) * 0.7
def rustle():
    n = int(0.3 * SR); return noise(0.3) * env(n, 0.01, 0.1, 0.4, 0.1) * (0.5 + 0.5 * np.sin(np.arange(n) / SR * 60)) * 0.35
def ringbuzz():      # old phone ring: 20 Hz amplitude-modulated 900 Hz square
    n = int(0.45 * SR); t = np.arange(n) / SR
    s = square(900, 0.45, 0.5) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 20 * t)))
    return s * env(n, 0.005, 0.05, 0.7, 0.05) * 0.4
def keyblip():
    s = square(1400, 0.04, 0.5); return s * env(len(s), 0.001, 0.01, 0.5, 0.02) * 0.35
def chime():         # rising three-note arpeggio, original intervals (major 2nd, 4th)
    return seq([square(f, 0.11, 0.5) * env(int(0.11 * SR), 0.002, 0.03, 0.6, 0.04) for f in (660, 740, 880)] + [square(1100, 0.3, 0.5) * env(int(0.3 * SR), 0.002, 0.1, 0.5, 0.15)]) * 0.5
def beam():          # rising sweep
    s = square(300, 0.25, 0.3, sweep=2.5); return s * env(len(s), 0.005, 0.05, 0.7, 0.08) * 0.45
def stamp():         # short bright hit + click
    a = square(1800, 0.06, 0.5) * env(int(0.06 * SR), 0.001, 0.02, 0.4, 0.03); b = tri(220, 0.12) * env(int(0.12 * SR), 0.001, 0.05, 0.3, 0.05)
    return seq([a * 0.5 + np.pad(b, (0, max(0, len(a) - len(b))))[:len(a)] * 0.5, b[len(a):] * 0.5])
def flagzip():
    s = square(1200, 0.5, 0.5, sweep=-0.7); return s * env(len(s), 0.005, 0.1, 0.6, 0.2) * 0.4
def fanfare():       # original four-note fanfare (not a known jingle): 523, 659, 784, 1047 with a held last note
    parts = [square(f, d, 0.5) * env(int(d * SR), 0.003, 0.04, 0.7, 0.05) for f, d in ((523, 0.14), (659, 0.14), (784, 0.14), (1047, 0.7))]
    return seq(parts) * 0.5
def heartbeat():
    return seq([tri(70, 0.09) * env(int(0.09 * SR), 0.002, 0.04, 0.4, 0.04), np.zeros(int(0.12 * SR), np.float32), tri(60, 0.09) * env(int(0.09 * SR), 0.002, 0.04, 0.4, 0.04)]) * 0.6


SFX = {"step": step, "hurt": hurt, "thud": thud, "rustle": rustle, "ringbuzz": ringbuzz, "keyblip": keyblip, "chime": chime,
       "beam": beam, "stamp": stamp, "flagzip": flagzip, "fanfare": fanfare, "heartbeat": heartbeat}

if __name__ == "__main__":
    import wave, sys
    from pathlib import Path
    out = Path(__file__).resolve().parent.parent / "gen" / "audio" / "sfx"; out.mkdir(parents=True, exist_ok=True)
    for k, fn in SFX.items():
        x = fn(); w = wave.open(str(out / f"{k}.wav"), "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
    print("sfx written:", sorted(SFX))
