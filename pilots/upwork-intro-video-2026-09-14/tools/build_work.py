#!/usr/bin/env python3
"""Render every non-presenter segment of the film from the deck, a plate and sealed library clips.

usage: build_work.py <plate.png> <out_dir>
Writes seg-*.mp4 plus segments.json (durations + sound-cue times) and the D3 deck check.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import adcomp as A  # noqa: E402
import film as F  # noqa: E402

REPO = Path(__file__).resolve().parents[3]
LIB = REPO / "eval/experiments/EVAL-040/runs"
GEN = Path(__file__).resolve().parents[1] / "gen"
CLIPS = {
    # phone1: new for this film (NB2 9:16 plate -> H3 Max i2v -> code-set text per frame); phone2/3: sealed EVAL-040 accepted artifacts
    "phone1": (GEN / "overlays/aarohi-motion.mp4", 0.2, "Aarohi text-in-motion, exact code-set type on an animated plate"),
    "phone2": (LIB / "topo3-video/artifacts/media/VID-TOPO3-01__minimax-h3-max-i2v__C_textless_plate_i2v_composite__r1.composite.mp4", 0.5, "Diwali sweets, code-set Devanagari composite (arm C, accepted)"),
    "phone3": (GEN / "overlays/juice-offer.mp4", 0.6, "juice hero macro (sealed Omni clip) + code-set offer pill"),
}


def main(plate_path: str, out_dir: str):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    plate = Image.open(plate_path).convert("RGBA")
    d = F.DECK
    en = d["aarohi_en"]
    copy_en = A.Copy("en", en["headline"], en["pill"], en["product"], en["price"], en["was"], en["code"], en["cta"], en["legal"])
    brand = A.Brand(wordmark=en["wordmark"])
    for s in [*en["headline"], en["pill"], en["product"], en["price"], en["was"], en["code"], en["cta"], en["legal"], en["wordmark"]]:
        F.USED_STRINGS.add(s)
    segs = {}
    n = F.seg_brief(plate, out / "seg-brief.mp4", 3.0); segs["brief"] = {"dur": n / F.FPS}
    n, snaps = F.seg_build(plate, copy_en, brand, out / "seg-build.mp4", 6.0); segs["build"] = {"dur": n / F.FPS, "snaps": snaps}
    n = F.seg_sizes(plate, copy_en, brand, out / "seg-sizes.mp4", 3.0); segs["sizes"] = {"dur": n / F.FPS, "snaps": [0.9]}
    n, flip = F.seg_hooks(plate, brand, out / "seg-hooks.mp4", 4.0); segs["hooks"] = {"dur": n / F.FPS, "snaps": [0.18 * j + 0.2 for j in range(6)], "flip": flip}
    n, fix = F.seg_check(plate, brand, out / "seg-check.mp4", 3.0); segs["check"] = {"dur": n / F.FPS, "tick": fix}
    sup = d["work_supers"]["video"]
    F.seg_phone(CLIPS["phone1"][0], out / "seg-phone1.mp4", CLIPS["phone1"][1], 3.2, sup); segs["phone1"] = {"dur": 3.2, "src": str(CLIPS["phone1"][0])}
    F.seg_phone(CLIPS["phone2"][0], out / "seg-phone2.mp4", CLIPS["phone2"][1], 3.0, sup); segs["phone2"] = {"dur": 3.0, "src": str(CLIPS["phone2"][0])}
    F.seg_phone(CLIPS["phone3"][0], out / "seg-phone3.mp4", CLIPS["phone3"][1], 3.0, None); segs["phone3"] = {"dur": 3.0, "src": str(CLIPS["phone3"][0])}
    n = F.seg_endcard(out / "seg-end.mp4", 5.5); segs["end"] = {"dur": n / F.FPS}
    # the insert at 0:02.5 — the finished ad as a still card (2.5 s) in a phone-less card frame
    ad = A.ledge(plate, copy_en, brand, "4x5")
    f = F.ground(); card = F.shadowed(F.fit_h(ad, int(F.H * 0.78))); A.paste(f, card, int(F.W * 0.70) - card.width // 2, (F.H - card.height) // 2)
    f.convert("RGB").save(out / "insert-ad.png")
    bad = F.d3_check()
    segs["_d3_off_deck_strings"] = bad
    (out / "segments.json").write_text(json.dumps(segs, indent=1, ensure_ascii=False))
    print(json.dumps({k: v.get("dur") for k, v in segs.items() if isinstance(v, dict)}, indent=0))
    print("D3 off-deck strings:", bad)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
