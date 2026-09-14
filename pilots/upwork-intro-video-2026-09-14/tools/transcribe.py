#!/usr/bin/env python3
"""Triage-tier transcript + delivery notes for a presenter take via Gemini (audio understanding on the Gemini API).
Not Registry evidence — a production check so the Creative Director can compare words against the frozen script.
usage: transcribe.py take.mp4 "expected line"
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from google import genai
from google.genai import types

take, expected = sys.argv[1], sys.argv[2]
wav = Path(tempfile.mkdtemp()) / "a.wav"
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", take, "-vn", "-ac", "1", "-ar", "16000", str(wav)], check=True)
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
prompt = (
    "Transcribe this audio verbatim, then evaluate the delivery. Return strict JSON with keys: "
    "transcript (string, exactly what is said, punctuation as heard), "
    "words_match_expected (true/false, ignoring punctuation and case), "
    "diff (short string describing any word differences vs expected, or 'none'), "
    "speech_end_s (number: seconds at which the last word ends), "
    "delivery (one sentence on pacing/naturalness/accent), "
    "defects (list of strings: doubled syllables, robotic cadence, cut-off words, other voices, music, noise; empty if none). "
    f"Expected line: {expected!r}"
)
resp = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=[types.Part.from_bytes(data=wav.read_bytes(), mime_type="audio/wav"), prompt],
    config=types.GenerateContentConfig(response_mime_type="application/json"),
)
print(resp.text)
