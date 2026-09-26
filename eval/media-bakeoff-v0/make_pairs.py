#!/usr/bin/env python3
"""Build blind judging pairs for the media bake-off.

    python3 make_pairs.py <run_dir>

Reads  <run_dir>/outputs.json : [{"brief_id","arm","file","kind":"image|video","status","cost_usd","seconds"}]
       (one entry per arm per brief = the single candidate that arm shows the judge; `file` relative to run_dir)
       ../BRIEFS.yaml
Writes <run_dir>/judge/                : the ONLY folder served to the judge
         media/<neutral name>          : every shown file under a hash name (stills re-encoded to PNG, so the file
                                         name and file type say nothing about the arm)
         pairs.json                    : what the viewer shows (no arm names anywhere)
         viewer.html                   : copied from this folder
       <run_dir>/mapping.json          : SEALED pair -> arms map, outside judge/ (do not open before verdicts are exported)
       <run_dir>/SKIPPED-PAIRS.txt     : comparisons that could not be built (an arm failed or has no file)

Judge with:  cd <run_dir>/judge && python3 -m http.server 8766 --bind 127.0.0.1   → http://127.0.0.1:8766/viewer.html
"""
from __future__ import annotations

import hashlib
import json
import random
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
# v1 design (TEST-FLOWS.md): A = LLM + media model, B = our pipeline, C = LLM + Canon + our pipeline.
COMPARISONS = [("B", "A"), ("C", "B"), ("C", "A"),
               ("A_MAI", "A")]   # side check: the same A prompt sent to MAI-Image-2.6 vs Nano Banana 2 (stills/edits only)
REPEAT_SHARE = 0.10


def neutral_copy(src: Path, media_dir: Path, kind: str) -> str:
    """Copy one shown file under a name derived from its content; stills become PNG so every still has one format."""
    digest = hashlib.sha256(src.read_bytes()).hexdigest()[:20]
    if kind == "image":
        dst = media_dir / f"{digest}.png"
        if not dst.exists():
            r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-frames:v", "1", "-map_metadata", "-1", str(dst)],
                               capture_output=True, text=True)
            if r.returncode != 0:
                raise RuntimeError(f"could not convert {src}: {r.stderr[-300:]}")
    else:
        dst = media_dir / f"{digest}.mp4"
        if not dst.exists():
            r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-map_metadata", "-1", "-c", "copy", str(dst)],
                               capture_output=True, text=True)
            if r.returncode != 0:
                shutil.copy(src, dst)
    return f"media/{dst.name}"


def main(run_dir: str) -> None:
    run = Path(run_dir)
    briefs = {b["id"]: b for b in yaml.safe_load((HERE / "BRIEFS.yaml").read_text())["exam"]}
    outs = json.loads((run / "outputs.json").read_text())
    by = {(o["brief_id"], o["arm"]): o for o in outs
          if o.get("status", "ok") == "ok" and o.get("file") and (run / o["file"]).exists()}
    judge = run / "judge"
    media_dir = judge / "media"
    media_dir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(int(hashlib.sha256(run.name.encode()).hexdigest(), 16) % 2**32)
    pairs, mapping, skipped, shown = [], {}, [], {}

    def shown_path(o):
        key = (o["brief_id"], o["arm"])
        if key not in shown:
            shown[key] = neutral_copy(run / o["file"], media_dir, o["kind"])
        return shown[key]

    for bid, b in briefs.items():
        for a, c in COMPARISONS:
            if (bid, a) not in by or (bid, c) not in by:
                if a != "A_MAI" or bid in ("E01", "E02", "E03", "E04", "E05"):
                    skipped.append(f"{bid} {a} vs {c}: missing " + ", ".join(x for x in (a, c) if (bid, x) not in by))
                continue
            left, right = (a, c) if rng.random() < 0.5 else (c, a)
            pid = f"p{len(pairs)+1:03d}"
            pairs.append({"pair_id": pid, "brief_id": bid, "brief": b.get("verbatim"), "answers": b.get("answers"),
                          "photos": len(b.get("assets") or []), "must_haves": [str(x) for x in b.get("must_haves") or []],
                          "deal_breakers": [str(x) for x in b.get("deal_breakers") or []],
                          "price_anchor_inr": b.get("price_anchor_inr"),
                          "left": shown_path(by[(bid, left)]), "right": shown_path(by[(bid, right)]),
                          "left_kind": by[(bid, left)]["kind"], "right_kind": by[(bid, right)]["kind"],
                          "kind": by[(bid, left)]["kind"]})
            mapping[pid] = {"left": left, "right": right, "comparison": f"{a} vs {c}", "brief_id": bid, "class": b["class"]}
    for p in rng.sample(pairs, max(1, int(len(pairs) * REPEAT_SHARE))) if pairs else []:
        pid = f"r{len(pairs)+1:03d}"
        m = mapping[p["pair_id"]]
        pairs.append({**p, "pair_id": pid, "left": p["right"], "right": p["left"],
                      "left_kind": p["right_kind"], "right_kind": p["left_kind"]})
        mapping[pid] = {**m, "left": m["right"], "right": m["left"], "repeat_of": p["pair_id"]}
    rng.shuffle(pairs)
    set_id = hashlib.sha256(json.dumps(pairs, sort_keys=True).encode()).hexdigest()[:12]
    for p in pairs:
        p["set"] = set_id            # the viewer keeps answers per pair set, so answers from another run never carry over
    (judge / "pairs.json").write_text(json.dumps(pairs, indent=1, ensure_ascii=False))
    shutil.copy(HERE / "viewer.html", judge / "viewer.html")
    (run / "mapping.json").write_text(json.dumps(mapping, indent=1))
    (run / "SKIPPED-PAIRS.txt").write_text("\n".join(skipped) + ("\n" if skipped else ""))
    print(f"{len(pairs)} pairs ({sum('repeat_of' in m for m in mapping.values())} swapped repeats), set {set_id}. "
          f"{len(skipped)} comparisons skipped" + (": " + "; ".join(skipped) if skipped else "") + ".\n"
          f"Judge with: cd {judge} && python3 -m http.server 8766 --bind 127.0.0.1  → open http://127.0.0.1:8766/viewer.html")


if __name__ == "__main__":
    main(sys.argv[1])
