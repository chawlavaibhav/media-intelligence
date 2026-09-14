import base64, json, sys, urllib.request, os
from pathlib import Path
wav=Path(sys.argv[1]).read_bytes(); expected=sys.argv[2]
prompt=("You are judging a spoken line for a commercial film. Transcribe verbatim, then evaluate. Return strict JSON with keys: transcript; "
 "words_match_expected (true/false ignoring punctuation/case; contractions and dashes fine); diff; pause_after_bar_went_up (true/false: is there an audible pause after 'So the bar went up'?); "
 "pace_wpm_estimate (number); accent (short: e.g. 'Indian English', 'American', 'British', 'mixed'); "
 "naturalness_1_to_10 (10 = indistinguishable from a real calm professional speaking, 1 = robotic TTS); "
 "sounds_read_not_spoken (true/false); too_fast_for_confidence (true/false); defects (list: robotic cadence, synthetic timbre, clipped words, doubled syllables, wrong stress, mispronunciation, background noise, music, other voice; empty if none); "
 f"one_sentence_verdict. Expected line: {expected!r}")
body={"contents":[{"role":"user","parts":[{"inlineData":{"mimeType":"audio/wav","data":base64.b64encode(wav).decode()}},{"text":prompt}]}],"generationConfig":{"responseMimeType":"application/json","temperature":0}}
req=urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent",data=json.dumps(body).encode(),headers={"x-goog-api-key":os.environ["GOOGLE_API_KEY"],"Content-Type":"application/json"})
with urllib.request.urlopen(req,timeout=120) as r: rep=json.load(r)
print(rep["candidates"][0]["content"]["parts"][0]["text"])
