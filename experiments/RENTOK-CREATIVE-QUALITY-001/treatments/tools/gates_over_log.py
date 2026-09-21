#!/usr/bin/env python3
"""Run the runtime layout gates over a renderer layout log (C1 bounds in the safe box, C5 disjoint per frame, C6 exact copy),
as Lane A's qa_checks.py did. usage: gates_over_log.py <layout.jsonl> <copy-deck.json>"""
import json, sys
sys.path.insert(0, '/Users/vaibhavchawla/Vaibhav_Personal_Projects/media-intelligence-rentok-cq')
from runtime.compositor import gates
SAFE = (65, 288, 888, 1248); CANVAS = (0, 0, 1080, 1920)
deck = json.load(open(sys.argv[2]))["strings"]
rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
nbox = out = overl = mism = 0
for r in rows:
    regions = {}
    for b in r["boxes"]:
        nbox += 1
        box = b.get("backing_box") or b["box"]
        try: gates.check_text_bounds(box, canvas=CANVAS, container=SAFE, id_=b["id"])
        except Exception: out += 1
        regions[b["id"] + f"#{len(regions)}"] = box
        if b.get("kind") == "text" and not b["id"].endswith("_partial"):
            key = b["id"]
            if key in deck and b["text"] != deck[key]: mism += 1
    try: gates.check_disjoint(regions, critical=tuple(regions))
    except Exception: overl += 1
print(json.dumps({"frames": len(rows), "boxes": nbox, "C1_outside_safe": out, "C5_frames_with_overlap": overl, "C6_exact_copy_mismatches": mism}))
