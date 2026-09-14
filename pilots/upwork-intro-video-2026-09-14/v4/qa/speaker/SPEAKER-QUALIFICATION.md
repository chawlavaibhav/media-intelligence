# Speaker micro-qualification (§8–§9) — 2026-09-14

Anchor still: Nano Banana 2, r1 rejected (blurred handwriting-like sheets on the wall — strict no-environmental-text), r2 accepted.

| Candidate | Route | Line | Result | Transcript | Pause | wpm | Accent | Naturalness (triage) | Hard defects | Scores F/E/V/A/D/Q | Total | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A `omni-r1` | Gemini Omni 1.1 Flash, Vertex, i2v 10 s 720p, USD 1.014 | full | media ok | **not verbatim** ("You need *make* more creative") | yes 0.88 s | 108 | Indian English | 6 — "synthetic timbre, robotic cadence" | script error; voice < 8 | 8/9/6/8/7/7 | 45 | **FAIL** |
| B `veo-r1`, `veo-r2` | Veo 3.1 Fast, Vertex, i2v 8 s 1080p audio | short | **provider error 14 UNAVAILABLE ×2** | — | — | — | — | — | infrastructure | — | — | no result |
| B `veo-r3` (Addendum 1) | same | short (8-s hard limit; §6 permitted form) | media ok | verbatim | yes 0.76 s | 99 | Indian English | 9 — no defects | none | 9/9/9/9/9/8 | **53** | **PASS** |
| C Wan 3.0 Prime | fal | — | not callable (fal USD 0.26 < 1.12) | | | | | | | | | not run |

Selected: **`veo-r3`** → `gen/speaker/speaker-accepted.mp4`; bubble frame `gen/speaker/speaker-bubble-frame.png` (t = 7.7 s).
Evidence: `qa/speaker/*-contact-1s.jpg`, `veo-r3-contact-05s.jpg`, `*-transcript.json`, audio `gen/speaker/*.wav`.
Voice naturalness is scored by the triage transcript model and my frame/waveform reading; the Controller's ear is the
release authority (§9 "listen to the whole line"). Speech span 0.46–7.40 s; clip used 0–7.75 s (the last 0.25 s has a
downward glance and is not shown).
