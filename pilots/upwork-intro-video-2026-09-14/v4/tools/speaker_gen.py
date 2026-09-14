import sys; sys.path.insert(0, 'tools'); import gen4 as G
from pathlib import Path
txt = Path('plan/SPEAKER-PROMPTS-V4.md').read_text()
tmpl = txt.split('## Native-speech clip')[1].split('LINE (Omni')[0].split('\n', 1)[1].strip().replace('\n', ' ')
FULL = "Everyone can make AI ads now. So the bar went up. You need more creative, faster — and it can't suck."
SHORT = "Everyone can make AI ads now. So the bar went up. You need more creative, faster."
still = G.V3 / "gen/speaker/still-accepted.png"
which = sys.argv[1]
if which == "omni":
    G.omni_i2v("v4-speaker-omni-r1", tmpl.replace("{LINE}", FULL), still, G.V3 / "gen/speaker/omni-r1.mp4", 10, "720p")
else:
    G.veo_i2v("v4-speaker-veo-r3", tmpl.replace("{LINE}", SHORT), still, G.V3 / "gen/speaker/veo-r3.mp4", 8, "1080p", True)
