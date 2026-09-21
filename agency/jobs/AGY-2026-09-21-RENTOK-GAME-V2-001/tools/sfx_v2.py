#!/usr/bin/env python3
"""sfx_v2.py — the SFX stem for the full 30 s, synthesised by code at the BOARD-v2 audio cues (impact[].primitive == 'audio').
PROVENANCE: cue synthesis from Lane A tools/sfx.py @ 7dab37a and Treatment C sfx_c.py @ 41d97c6 (thump, riser, whoosh, bass drop,
impact, sparks; pew with the 200-Hz body); the new cues here (hop, steps, coins, creak, crash, papers, buzz, pops, confetti,
land, tick) are written for this board. Bed-processing cues (bed_duck, bed_cold, bed_level2) are handled by assemble_v2.py.
Writes gen/sfx-v2-stem.wav (48 kHz stereo, 30.0 s)."""
import json, sys, wave
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent; JOB = HERE.parent
SR = 48000; DUR = 30.0

def env(n, a=0.005, d=0.08, s=0.0, r=0.05, hold=0.0):
    e = np.ones(n); at = int(a * SR); dt = int(d * SR); ht = int(hold * SR)
    if at: e[:at] = np.linspace(0, 1, at)
    e[at:at + dt] = np.linspace(1, s if s else 0.0001, min(dt, max(0, n - at)))
    e[at + dt:at + dt + ht] = s
    tail = n - (at + dt + ht)
    if tail > 0: e[at + dt + ht:] = np.linspace(s if s else 0.0001, 0, tail)
    return e
def square(freq, dur, vol=0.3, duty=0.5, sweep=0.0):
    n = int(dur * SR); t = np.arange(n) / SR; f = freq * (2 ** (sweep * t / max(dur, 1e-6))); ph = np.cumsum(f) / SR
    return vol * np.where((ph % 1.0) < duty, 1.0, -1.0)
def sine(freq, dur, vol=0.3, sweep=0.0):
    n = int(dur * SR); t = np.arange(n) / SR; f = freq * (2 ** (sweep * t / max(dur, 1e-6))); return vol * np.sin(2 * np.pi * np.cumsum(f) / SR)
def noise(dur, vol=0.3, seed=7): return vol * np.random.default_rng(seed).uniform(-1, 1, int(dur * SR))
def lowpass(x, fc):
    a = 1 - np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); acc = 0.0
    for i in range(len(x)): acc += a * (x[i] - acc); y[i] = acc
    return y
def seq(parts):
    """place (offset_s, signal) parts into one buffer"""
    n = max(int(o * SR) + len(s) for o, s in parts); out = np.zeros(n)
    for o, s in parts: i = int(o * SR); out[i:i + len(s)] += s
    return out
# Lane A cues
def cue_jump():   s = square(300, 0.18, 0.28, 0.5, sweep=1.2); return s * env(len(s), d=0.15)
def cue_hit():    s = square(220, 0.22, 0.32, 0.25, sweep=-1.5) + noise(0.22, 0.18); return s * env(len(s), d=0.2)
def cue_trip():   s = square(180, 0.3, 0.28, 0.5, sweep=-1.0); return s * env(len(s), d=0.28)
def cue_key():    s = square(1600, 0.045, 0.22, 0.5); return s * env(len(s), a=0.002, d=0.04)
def cue_low():    s = square(70, 0.8, 0.28, 0.5, sweep=-0.5); return s * env(len(s), a=0.05, d=0.7)
def cue_pew():    s = square(900, 0.12, 0.26, 0.3, sweep=-2.0) + square(200, 0.12, 0.12, 0.5, sweep=-1.0); return s * env(len(s), d=0.1)
def cue_burst():  s = noise(0.28, 0.3) + square(110, 0.28, 0.2, 0.5, sweep=-1.0); return s * env(len(s), d=0.26)
def cue_ding():   s = square(1320, 0.14, 0.2, 0.5) + square(1980, 0.14, 0.12, 0.5); return s * env(len(s), d=0.12)
def cue_tag():    s = square(660, 0.08, 0.22, 0.5) + square(990, 0.08, 0.18, 0.5); return s * env(len(s), d=0.07)
def cue_end():    s = square(196, 0.6, 0.25, 0.5) + square(392, 0.6, 0.12, 0.5); return s * env(len(s), a=0.01, d=0.55)
def motif(notes, step=0.09, vol=0.26):
    out = []
    for f in notes: s = square(f, step, vol, 0.5); out.append(s * env(len(s), d=step * 0.9))
    return np.concatenate(out)
def cue_powerup(): return motif([523.25, 659.25, 783.99, 1046.5, 1318.5], step=0.09)
def cue_fanfare(): return motif([783.99, 783.99, 880.0, 1046.5, 1318.5, 1046.5], step=0.13, vol=0.28)
# Treatment C cues
def cue_thump():    s = sine(60, 0.3, 0.6, sweep=-0.6); return s * env(len(s), a=0.003, d=0.28)
def cue_riser():    s = lowpass(noise(0.22, 0.5, 3), 400) * 4; return s * np.linspace(0.05, 1.0, len(s)) ** 2
def cue_whoosh():   s = lowpass(noise(0.3, 0.5, 11), 2500) * 2 - lowpass(noise(0.3, 0.5, 11), 300) * 2; return s * env(len(s), a=0.01, d=0.28)
def cue_bassdrop(): s = sine(110, 0.5, 0.5, sweep=-1.5); return s * env(len(s), a=0.002, d=0.45)
def cue_impact():   s = noise(0.12, 0.5, 5) + sine(160, 0.12, 0.5, sweep=-1.0); return s * env(len(s), a=0.001, d=0.11)
def cue_sparks():   s = square(2400, 0.06, 0.12, 0.5, sweep=1.0); return s * env(len(s), d=0.05)
# v2 cues
def cue_land():     s = square(150, 0.08, 0.2, 0.5, sweep=-0.5) + noise(0.08, 0.1, 9); return s * env(len(s), d=0.07)
def cue_hop():      s = square(120, 0.1, 0.24, 0.5, sweep=-0.8) + (noise(0.1, 0.35, 13) - lowpass(noise(0.1, 0.35, 13), 1500)); return s * env(len(s), d=0.09)
def cue_step():     s = square(140, 0.05, 0.16, 0.5, sweep=-0.6); return s * env(len(s), d=0.045)
def cue_steps():    return seq([(i * 0.2, cue_step()) for i in range(8)])
def cue_coins():    return seq([(i * 0.06, square(f, 0.07, 0.16, 0.5) * env(int(0.07 * SR), d=0.06)) for i, f in enumerate((1760, 2093, 2637))])
def cue_creak():
    n = int(0.45 * SR); t = np.arange(n) / SR; f = 95 * (1 + 0.04 * np.sin(2 * np.pi * 9 * t)) * (2 ** (0.3 * t / 0.45)); s = 0.22 * np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)); return s * env(n, a=0.05, d=0.4)
def cue_crash():    s = lowpass(noise(0.35, 0.7, 17), 900) * 1.5 + square(80, 0.35, 0.25, 0.5, sweep=-1.2); return s * env(len(s), a=0.002, d=0.33)
def cue_papers():   s = lowpass(noise(0.45, 0.4, 21), 3000) - lowpass(noise(0.45, 0.4, 21), 800); return s * (0.5 + 0.5 * np.sin(2 * np.pi * 14 * np.arange(len(s)) / SR)) * env(len(s), a=0.02, d=0.4)
def cue_buzz():
    n = int(2.8 * SR); t = np.arange(n) / SR; s = square(90, 2.8, 0.12, 0.2) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 8 * t))); return s * env(n, a=0.3, d=0.2, s=1.0, hold=2.0)
def cue_pop():      s = square(880, 0.06, 0.2, 0.5, sweep=-1.0); return s * env(len(s), d=0.05)
def cue_pops():     return seq([(i * 0.05, cue_pop()) for i in range(5)])
def cue_confetti(): return seq([(i * 0.03, square(2400 + 300 * (i % 4), 0.03, 0.08, 0.5) * env(int(0.03 * SR), d=0.025)) for i in range(20)])
def cue_tick():     s = square(2200, 0.03, 0.14, 0.5); return s * env(len(s), a=0.001, d=0.025)
def cue_keys():     return seq([(i * (1.4 / 17), cue_key()) for i in range(17)])
def cue_refill():   return seq([(i * 0.08, cue_tick()) for i in range(5)])

CUES = {"jump": [cue_jump], "land": [cue_land], "riser": [cue_riser], "thump+hit": [cue_thump, cue_hit], "hop": [cue_hop], "steps": [cue_steps],
        "whoosh": [cue_whoosh], "trip": [cue_trip], "coins": [cue_coins], "creak": [cue_creak], "crash+thump": [cue_crash, cue_thump], "papers": [cue_papers],
        "buzz": [cue_buzz], "low": [cue_low], "keys": [cue_keys], "impact+bassdrop": [cue_impact, cue_bassdrop], "powerup": [cue_powerup],
        "sparks": [lambda: seq([(i * 0.07, cue_sparks()) for i in range(6)])], "pew": [cue_pew], "tag": [cue_tag], "burst+coins": [cue_burst, cue_coins],
        "pops": [cue_pops], "burst+thump+whoosh": [cue_burst, cue_thump, cue_whoosh], "burst+papers": [cue_burst, cue_papers], "ding": [cue_ding],
        "fanfare": [cue_fanfare], "confetti": [cue_confetti], "end": [cue_end]}
BED_CUES = {"bed_duck", "bed_cold", "bed_level2"}

def main():
    board = json.load(open(JOB / "board.json"))
    cues = []
    for f in board["frames"]:
        for e in f["impact"]:
            if e["primitive"] == "audio":
                if e["cue"] in BED_CUES: continue
                if e["cue"] not in CUES: sys.exit(f"unknown audio cue {e['cue']!r} at {e['t']}")
                for fn in CUES[e["cue"]]: cues.append((e["t"], fn))
            if e["primitive"] == "hud_refill": cues.append((e["t"], cue_refill))
    stem = np.zeros(int(DUR * SR))
    for t, fn in cues:
        s = fn(); i = int(t * SR); j = min(len(stem), i + len(s))
        if i < len(stem): stem[i:j] += s[: j - i]
    stem = np.clip(stem, -1, 1); st = np.stack([stem, stem], axis=1)
    out = JOB / "gen/sfx-v2-stem.wav"
    with wave.open(str(out), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
    print("wrote", out, "cues", len(cues), "from the board")
if __name__ == "__main__": main()
