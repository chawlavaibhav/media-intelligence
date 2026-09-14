#!/usr/bin/env python3
"""Triage transcript check of the chosen VO takes via the Gemini API (credits; not evidence, a production check)."""
import base64, json, sys, urllib.request, os
from pathlib import Path
V3 = Path(__file__).resolve().parent.parent
lines = [l.strip() for l in (V3 / "plan/VO-SCRIPT.txt").read_text().splitlines() if l.strip()]
CHOSEN = json.loads((V3 / "plan/VO-TAKES.json").read_text())
key = os.environ["GOOGLE_API_KEY"]
for i, take in enumerate(CHOSEN, 1):
    wav = (V3 / "gen/audio" / take).read_bytes()
    prompt = ("Transcribe this audio verbatim, then evaluate the delivery. Return strict JSON with keys: transcript, words_match_expected (true/false ignoring punctuation/case; "
              "spelled-out numbers vs digits count as a match), diff (short, or 'none'), delivery (one sentence: pace, naturalness, accent), defects (list: doubled syllables, "
              f"robotic cadence, cut-off words, mispronunciation, other voices, noise; empty if none). Expected line: {lines[i-1]!r}")
    body = {"contents": [{"role": "user", "parts": [{"inlineData": {"mimeType": "audio/wav", "data": base64.b64encode(wav).decode()}}, {"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json"}}
    req = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent", data=json.dumps(body).encode(),
                                 headers={"x-goog-api-key": key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        rep = json.load(r)
    txt = rep["candidates"][0]["content"]["parts"][0]["text"]
    print(take, txt.replace("\n", " ")[:600])
