#!/usr/bin/env python3
"""prompts.py — the seven generation prompts as data (Stage 4 A1–A7), written to the gate's rule:
no text-surface word without an illegibility/deferral term in the same sentence, an explicit no-lettering clause,
no Nintendo name, no copy-deck string. `python3 prompts.py write` writes gen/prompts/*.txt and gen/prompts/PACKAGE.md
(the minimal package the pre-dispatch gate reads); `python3 prompts.py gate` runs canon/gate/run_gate.py pre on each.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
JOB = HERE.parent
REPO = JOB.parents[2]
OUT = JOB / "gen/prompts"

STYLE = ("Flat 16-bit pixel-art game sprite, crisp square pixels, matte colours with no gloss, every shape closed by a "
         "2-pixel dark outline, daylight from the upper left with one hard pixel shadow, on a solid uniform bright green "
         "background (#00FF00) with nothing else in frame. No text, no lettering, no numbers, no logos, no watermark anywhere. "
         "Original design, not based on any existing video game character.")

PROMPTS = {
    "A1_owner_sheet": (
        "A sprite sheet of ONE character in four poses side by side, evenly spaced, same size and same design in every pose: "
        "(1) standing idle, (2) running with the left leg forward, (3) running with the right leg forward, (4) jumping with knees up. "
        "The character: an ordinary Indian man of about forty, slightly stocky, short black hair, rectangular spectacles, a blue-and-white "
        "checked half-sleeve shirt, dark trousers, brown sandals; a big bunch of keys on a ring hangs from his belt; he carries a thick "
        "red bound account book under one arm, its cover blank. Full body, facing right, feet on the bottom edge. " + STYLE),
    "A2_obst_wall": (
        "A single game obstacle: a tall wall built from stacked blank white paper sheets and blank folders, slightly leaning, with a faceless "
        "grey human silhouette peeking out from behind it and a large bold question-mark symbol floating above. The sheets are blank with no writing. " + STYLE),
    "A3_obst_sack": (
        "A single game obstacle: a heavy brown cloth money sack tied at the neck, wrapped in a thick grey chain with a big padlock in front, "
        "a mean squinting face on the sack, mid-hop with a small pixel shadow beneath. No symbols or writing on the sack. " + STYLE),
    "A4_obst_tenant": (
        "A single game character: a young man in a hoodie and jeans sprinting to the right in a running pose, dragging a rolling suitcase behind "
        "him with one hand and clutching a bulging cloth coin bag to his chest with the other, looking back over his shoulder. Full body, feet on the bottom edge. " + STYLE),
    "A5_obst_tower": (
        "A single game obstacle: a precarious toppling tower of thick bound account books, loose blank paper sheets and a chunky pocket calculator "
        "with a blank display, stacked crookedly and about to fall to the left; a few sheets fluttering. All pages blank, no writing. " + STYLE),
    "A6_obst_swarm": (
        "A single game obstacle: a swarm of five angry red speech-bubble shapes with cartoon frowning eyes, each bubble empty except one bold "
        "exclamation-mark symbol, flying in a loose cluster with small motion lines. No letters or words inside the bubbles. " + STYLE),
    "A7_plate": (
        "A vertical 9:16 pixel-art background for a side-scrolling game, Indian city lane: a tall cream-and-terracotta paying-guest building "
        "with many stacked floors of small windows and balconies filling the upper two thirds, black water tanks and a TV antenna on the roof, "
        "a lower cream building beside it, a pale blue sky with two simple clouds. The bottom fifth is an empty flat packed-earth lane in "
        "muted ochre with a low stone kerb, no ground pattern. All building faces and walls are plain and blank — no shop fronts, no boards, "
        "no hoardings, no writing of any kind. Flat 16-bit pixel art, crisp square pixels, matte colours, 2-pixel dark outlines, daylight from "
        "the upper left. No text, no lettering, no numbers, no logos, no watermark anywhere. Original design, not based on any existing video game."),
}
ASPECT = {"A1_owner_sheet": "21:9", "A7_plate": "9:16"}   # everything else 1:1 (Gemini image aspect enum has no 4:1; 21:9 is the widest)


def write():
    OUT.mkdir(parents=True, exist_ok=True)
    for k, v in PROMPTS.items():
        (OUT / f"{k}.txt").write_text(v + "\n")
    pkg = ["## DELIVERABLE", "", "Textless pixel-art sprites and one 9:16 background plate for a code-rendered 30 s vertical game film "
           "(1080x1920). Every string is composited by code in post; no generated text anywhere.", "",
           "## VISUAL_SYSTEM", "", "Finish: matte flat pixel art, no gloss. Light: one source, daylight upper-left, hard pixel shadows. "
           "Separation: 2-px dark outlines on every sprite. Key level: bright daytime. Attention: 1st read the moving sprite entering from the right, 2nd read its label, 3rd read the HUD change. Balance: deliberately restless during the run, balanced on the end card.", "",
           "## GENERATION_PROMPTS", ""]
    for k, v in PROMPTS.items():
        pkg += [f"### {k} (aspect {ASPECT.get(k, '1:1')})", "", v, ""]
    pkg += ["## DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS", "", "All copy (HUD, obstacle labels, cheat code, chips, CTA, URL) and the "
            "RentOk wordmark are composited by code onto the rendered frames; the ground, flag, phone item, projectiles and effects are drawn by code.", ""]
    (OUT / "PACKAGE.md").write_text("\n".join(pkg))
    print("wrote", len(PROMPTS), "prompts +", OUT / "PACKAGE.md")


def gate():
    write()
    bad = 0
    for k in PROMPTS:
        r = subprocess.run([sys.executable, str(REPO / "canon/gate/run_gate.py"), "pre", "--package", str(OUT / "PACKAGE.md"),
                            "--prompt-file", str(OUT / f"{k}.txt"), "--modality", "static_image", "--json", str(OUT / f"{k}.gate.json")],
                           capture_output=True, text=True, cwd=str(REPO))
        lines = [l for l in r.stdout.splitlines() if "FAIL" in l or "BLOCK" in l or "verdict" in l.lower() or "LIMIT" in l]
        status = "ok" if r.returncode == 0 else f"exit {r.returncode}"
        print(f"== {k}: {status}")
        for l in lines[:8]:
            print("   ", l[:160])
        if r.returncode != 0:
            bad += 1
    print("gate failures:", bad)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    {"write": write, "gate": gate}[sys.argv[1] if len(sys.argv) > 1 else "write"]()
