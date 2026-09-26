#!/usr/bin/env python3
"""Build blind judging pairs for the media bake-off.

    python3 make_pairs.py <run_dir>

Reads  <run_dir>/outputs.json : [{"brief_id","arm","file","kind":"image|video","status","cost_usd","seconds"}]
       (one entry per arm per brief = the single candidate that arm shows the judge; `file` relative to run_dir)
       ../BRIEFS.yaml
Writes <run_dir>/judge/                : the ONLY folder served to the judge
         media/<random name>           : every shown file, re-encoded to one format per kind (films: 1080-wide H.264 +
                                         48 kHz stereo AAC, 24 fps; stills: PNG, long edge 1350 px, square pixels),
                                         metadata stripped, all with one fixed file time, written in shuffled order
         pairs.json                    : what the viewer shows (random pair ids; no arm names, no order that means anything)
         viewer.html                   : copied from this folder
       <run_dir>/mapping.json          : SEALED: pair -> arms, the random seed, and media name -> source file.
                                         Outside judge/. Do not open before verdicts are exported.
       <run_dir>/SKIPPED-PAIRS.txt     : comparisons that could not be built (an arm failed or has no file)

Blindness (final check, 26 Sep): the seed and the media names are random and live only in mapping.json, so neither
the public run name, make_pairs.py nor MANIFEST.sha256 can rebuild the pairing.

Judge with:  cd <run_dir>/judge && python3 -m http.server 8766 --bind 127.0.0.1   → http://127.0.0.1:8766/viewer.html
"""
from __future__ import annotations

import json
import os
import random
import secrets
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
FIXED_TIME = 1790000000          # one file time for every served file (2026-09-21), so Last-Modified says nothing


def probe_wh(src: Path) -> tuple[int, int]:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                        "-of", "csv=p=0", str(src)], capture_output=True, text=True)
    w, h = (int(x) for x in r.stdout.strip().split(",")[:2])
    return w, h


def encode(src: Path, dst: Path, kind: str) -> None:
    if kind == "image":
        vf = "scale='if(gte(iw,ih),1350,-2)':'if(gte(iw,ih),-2,1350)',setsar=1"
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(src), "-frames:v", "1", "-vf", vf, "-map_metadata", "-1", str(dst)]
    else:
        w, h = probe_wh(src)
        W, H = (1080, 1920) if h >= w else (1920, 1080)
        vf = f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,fps=24,setsar=1,format=yuv420p"
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", vf, "-c:v", "libx264", "-crf", "20", "-preset", "medium",
               "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "160k", "-map_metadata", "-1", "-map_chapters", "-1",
               "-fflags", "+bitexact", "-flags:v", "+bitexact", "-flags:a", "+bitexact", "-movflags", "+faststart", str(dst)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"could not encode {src}: {r.stderr[-300:]}")
    os.utime(dst, (FIXED_TIME, FIXED_TIME))


def main(run_dir: str) -> None:
    run = Path(run_dir)
    briefs = {b["id"]: b for b in yaml.safe_load((HERE / "BRIEFS.yaml").read_text())["exam"]}
    outs = json.loads((run / "outputs.json").read_text())
    by = {(o["brief_id"], o["arm"]): o for o in outs
          if o.get("status", "ok") == "ok" and o.get("file") and (run / o["file"]).exists()}
    judge = run / "judge"
    if judge.exists():
        shutil.rmtree(judge)                       # never mix files from an earlier build
    media_dir = judge / "media"
    media_dir.mkdir(parents=True)
    seed = secrets.randbits(64)
    rng = random.Random(seed)

    # every shown file gets a random name; files are written in shuffled order
    shown_keys = sorted(by)
    rng.shuffle(shown_keys)
    names = {}
    for key in shown_keys:
        o = by[key]
        ext = ".png" if o["kind"] == "image" else ".mp4"
        name = f"{secrets.token_hex(10)}{ext}"
        encode(run / o["file"], media_dir / name, o["kind"])
        names[key] = f"media/{name}"

    pairs, mapping, skipped = [], {}, []
    for bid, b in briefs.items():
        for a, c in COMPARISONS:
            if (bid, a) not in by or (bid, c) not in by:
                if a != "A_MAI" or bid in ("E01", "E02", "E03", "E04", "E05"):
                    skipped.append(f"{bid} {a} vs {c}: missing " + ", ".join(x for x in (a, c) if (bid, x) not in by))
                continue
            left, right = (a, c) if rng.random() < 0.5 else (c, a)
            pairs.append({"brief_id": bid, "brief": b.get("verbatim"), "answers": b.get("answers"),
                          "photos": len(b.get("assets") or []), "must_haves": [str(x) for x in b.get("must_haves") or []],
                          "deal_breakers": [str(x) for x in b.get("deal_breakers") or []],
                          "price_anchor_inr": b.get("price_anchor_inr"),
                          "left": names[(bid, left)], "right": names[(bid, right)],
                          "left_kind": by[(bid, left)]["kind"], "right_kind": by[(bid, right)]["kind"],
                          "kind": by[(bid, left)]["kind"],
                          "_m": {"left": left, "right": right, "comparison": f"{a} vs {c}", "brief_id": bid, "class": b["class"]}})
    for p in (rng.sample(pairs, max(1, int(len(pairs) * REPEAT_SHARE))) if pairs else []):
        m = p["_m"]
        pairs.append({**p, "left": p["right"], "right": p["left"], "left_kind": p["right_kind"], "right_kind": p["left_kind"],
                      "_m": {**m, "left": m["right"], "right": m["left"], "repeat_of": id(p)}, "_orig": id(p)})
    rng.shuffle(pairs)
    ids = {}
    for p in pairs:
        pid = secrets.token_hex(4)
        ids[id(p)] = pid
        p["pair_id"] = pid
    for p in pairs:
        m = p.pop("_m")
        if "repeat_of" in m:
            m["repeat_of"] = ids[m["repeat_of"]]
        p.pop("_orig", None)
        mapping[p["pair_id"]] = m
    set_id = secrets.token_hex(6)
    for p in pairs:
        p["set"] = set_id            # the viewer keeps answers per pair set, so answers from another build never carry over
    (judge / "pairs.json").write_text(json.dumps(pairs, indent=1, ensure_ascii=False))
    shutil.copy(HERE / "viewer.html", judge / "viewer.html")
    for f in (judge / "pairs.json", judge / "viewer.html", media_dir, judge):
        os.utime(f, (FIXED_TIME, FIXED_TIME))
    (run / "mapping.json").write_text(json.dumps(
        {**mapping, "_seed": seed, "_set": set_id,
         "_media": {v: {"brief_id": k[0], "arm": k[1], "source": by[k]["file"]} for k, v in names.items()}}, indent=1))
    (run / "SKIPPED-PAIRS.txt").write_text("\n".join(skipped) + ("\n" if skipped else ""))
    print(f"{len(pairs)} pairs ({sum('repeat_of' in m for m in mapping.values())} swapped repeats), set {set_id}. "
          f"{len(skipped)} comparisons skipped" + (": " + "; ".join(skipped) if skipped else "") + ".\n"
          f"Judge with: cd {judge} && python3 -m http.server 8766 --bind 127.0.0.1  → open http://127.0.0.1:8766/viewer.html")


if __name__ == "__main__":
    main(sys.argv[1])
