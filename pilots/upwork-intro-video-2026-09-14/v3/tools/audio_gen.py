#!/usr/bin/env python3
"""VO (Sarvam bulbul:v3, speaker aditya, en-IN) one call per paragraph of the frozen script, and the Lyria 2 bed."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import gen as G

V3 = G.V3
MUSIC_PROMPT = ("58-second instrumental advertising bed for a premium modern DTC creative studio. Confident, editorial, understated energy. "
                "Tight modern percussion, warm bass, restrained synth texture, subtle rise in the middle, stronger pulse for the delivery-speed section, "
                "elegant resolved ending. No vocals, no cinematic trailer booms, no cheesy corporate ukulele, no EDM drop. Leave clear spectral room for spoken voice.")

if __name__ == "__main__":
    what = sys.argv[1]
    if what == "vo":
        lines = [l.strip() for l in (V3 / "plan/VO-SCRIPT.txt").read_text().splitlines() if l.strip()]
        assert len(lines) == 8 and sum(l.count("Adwisely") for l in lines) == 1
        pace = float(sys.argv[2]) if len(sys.argv) > 2 else None
        for i, l in enumerate(lines, 1):
            G.sarvam(f"vo-{i:02d}" + (f"-p{pace}" if pace else ""), l, V3 / "gen/audio" / (f"vo-{i:02d}" + (f"-p{pace}" if pace else "") + ".wav"), "en-IN", "aditya", pace)
    elif what == "music":
        G.lyria(sys.argv[2] if len(sys.argv) > 2 else "music-r1", MUSIC_PROMPT, V3 / f"gen/audio/{sys.argv[2] if len(sys.argv) > 2 else 'music-r1'}.wav", negative="vocals, trailer booms, ukulele, EDM drop")
