#!/usr/bin/env python3
"""Build blind judging pairs for the media bake-off.

    python3 make_pairs.py <run_dir>

Reads  <run_dir>/outputs.json : [{"brief_id","arm","file","kind":"image|video","cost_usd","seconds"}]
       (one entry per arm per brief = the single candidate that arm shows the judge; `file` relative to run_dir)
       ../BRIEFS.yaml
Writes <run_dir>/pairs.json   : what the viewer shows (no arm names)
       <run_dir>/mapping.json : SEALED pair -> arms map (do not open before verdicts are exported)
"""
from __future__ import annotations

import hashlib
import json
import random
import sys
from pathlib import Path

import yaml

COMPARISONS = [("P", "B0"), ("P", "B1"), ("P+Canon", "P"), ("P+Canon", "B1")]
REPEAT_SHARE = 0.10


def main(run_dir: str) -> None:
    run = Path(run_dir)
    briefs = {b["id"]: b for b in yaml.safe_load((Path(__file__).parent / "BRIEFS.yaml").read_text())["exam"]}
    outs = json.loads((run / "outputs.json").read_text())
    by = {(o["brief_id"], o["arm"]): o for o in outs}
    rng = random.Random(int(hashlib.sha256(run.name.encode()).hexdigest(), 16) % 2**32)
    pairs, mapping = [], {}
    for bid, b in briefs.items():
        for a, c in COMPARISONS:
            if (bid, a) not in by or (bid, c) not in by:
                continue
            left, right = (a, c) if rng.random() < 0.5 else (c, a)
            pid = f"p{len(pairs)+1:03d}"
            pairs.append({"pair_id": pid, "brief_id": bid, "brief": b.get("verbatim"), "price_anchor_inr": b.get("price_anchor_inr"),
                          "left": by[(bid, left)]["file"], "right": by[(bid, right)]["file"], "kind": by[(bid, left)]["kind"]})
            mapping[pid] = {"left": left, "right": right, "comparison": f"{a} vs {c}", "brief_id": bid, "class": b["class"]}
    for p in rng.sample(pairs, max(1, int(len(pairs) * REPEAT_SHARE))):
        pid = f"r{len(pairs)+1:03d}"
        m = mapping[p["pair_id"]]
        pairs.append({**p, "pair_id": pid, "left": p["right"], "right": p["left"]})
        mapping[pid] = {**m, "left": m["right"], "right": m["left"], "repeat_of": p["pair_id"]}
    rng.shuffle(pairs)
    (run / "pairs.json").write_text(json.dumps(pairs, indent=1))
    (run / "mapping.json").write_text(json.dumps(mapping, indent=1))
    print(f"{len(pairs)} pairs ({sum('repeat_of' in m for m in mapping.values())} swapped repeats). "
          f"Judge with: cd {run} && python3 -m http.server 8765  → open http://localhost:8765/viewer.html")


if __name__ == "__main__":
    main(sys.argv[1])
