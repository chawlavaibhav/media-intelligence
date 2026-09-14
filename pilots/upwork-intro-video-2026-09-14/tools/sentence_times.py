#!/usr/bin/env python3
"""Sentence start/end times for a take (Gemini audio understanding, triage tier). usage: sentence_times.py take.mp4 'S1' 'S2' ..."""
import json, os, subprocess, sys, tempfile
from pathlib import Path
from google import genai
from google.genai import types
take, sents = sys.argv[1], sys.argv[2:]
wav = Path(tempfile.mkdtemp()) / "a.wav"
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", take, "-vn", "-ac", "1", "-ar", "16000", str(wav)], check=True)
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
prompt = ("For each of the following sentences, give the time in seconds (one decimal) at which its first word starts and "
          "its last word ends in this audio. Return strict JSON: a list of objects {sentence, start_s, end_s} in order. Sentences: "
          + json.dumps(sents))
resp = client.models.generate_content(model="gemini-3.6-flash",
    contents=[types.Part.from_bytes(data=wav.read_bytes(), mime_type="audio/wav"), prompt],
    config=types.GenerateContentConfig(response_mime_type="application/json"))
print(resp.text)
