#!/usr/bin/env python3
"""
Generate the native-validation sheets. **Preparation only — this does not consume human time.**

Three sheets, matching the three tasks in NATIVE-VALIDATION.md:

  1. word-validation-sheet.csv    is each base string a real, well-formed Hindi word?
  2. perceptibility-sheet.csv     can a person SEE the difference in each rendered pair?
  3. rendering-sanity-sheet.csv   does a sample of rendered images look like normal Hindi?

Sheet 1 needs no build and is committed. Sheets 2 and 3 reference rendered images, so they are
generated from a build directory with `--from-build`.

STABLE IDS
    Word ids are `w-<first 12 hex of sha256(NFC(word))>`. They do not move when the pool changes,
    so a response collected today still matches its word after the list is expanded — which is
    exactly what will happen when Resources supplies more lexical items.

NO SOURCE-IMAGE TASK
    Nobody is asked to look at a photograph and say what it says. That was the EVAL-004 task, and
    it is the one this design removed. Every question here is either lexical ("is this a word") or
    perceptual ("can you see a difference"), and **none of them establishes ground truth.**

No network, no model, no spend.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_items import load_base_strings  # noqa: E402
from devtext import RenderSpec, nfc, render  # noqa: E402

# Deterministic sample sizes. Small on purpose: this is difficulty tuning and tool checking, not
# a measurement, and the human budget is ~1.5 hours in total.
PERCEPTIBILITY_PAIRS = 25
RENDERING_SANITY_IMAGES = 20


def word_id(word: str) -> str:
    return "w-" + hashlib.sha256(nfc(word).encode("utf-8")).hexdigest()[:12]


def write_word_sheet(bases: list[dict], out: Path) -> int:
    rows = sorted(({"word_id": word_id(b["text"]), "word": b["text"],
                    "provenance": b["provenance"]} for b in bases),
                  key=lambda r: r["word_id"])
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["word_id", "word", "is_real_wellformed_hindi_word",
                    "reader_note", "provenance"])
        for r in rows:
            # Answer column left EMPTY. A pre-filled sheet is a leading question.
            w.writerow([r["word_id"], r["word"], "", "", r["provenance"]])
    return len(rows)


def write_perceptibility_sheet(items: list[dict], out: Path, build_dir: Path) -> int:
    """~25 mismatch pairs, spread deterministically across failure groups.

    Round-robin across groups so no group is over-represented, then take hard items first: those
    are the ones whose perceptibility actually matters, because a hard item nobody can see would
    be scoring a checker on an invisible difference.
    """
    mismatches = [i for i in items if i["expected_verdict"] == "mismatch"]
    by_group: dict[str, list[dict]] = {}
    for i in sorted(mismatches, key=lambda r: (not r.get("hard_opportunity"),
                                               r["failure_class"], r["item_id"])):
        by_group.setdefault(i["failure_group"], []).append(i)

    picked, cursor = [], {g: 0 for g in by_group}
    groups = sorted(by_group)
    while len(picked) < min(PERCEPTIBILITY_PAIRS, len(mismatches)):
        progressed = False
        for g in groups:
            if len(picked) >= PERCEPTIBILITY_PAIRS:
                break
            if cursor[g] < len(by_group[g]):
                picked.append(by_group[g][cursor[g]])
                cursor[g] += 1
                progressed = True
        if not progressed:
            break

    # Render the counterpart image: what the TARGET string looks like drawn. The reader compares
    # two pictures and is never asked to read either one.
    tdir = build_dir / "target-render"
    tdir.mkdir(parents=True, exist_ok=True)
    spec = RenderSpec(**{k: v for k, v in picked[0]["render_spec"].items()}) if picked else RenderSpec()
    for i in picked:
        render(i["target_string"], tdir / f"{i['item_id']}.png", spec)

    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["pair_id", "image_a", "image_b", "failure_group", "is_hard_opportunity",
                    "can_you_see_a_difference", "reader_note"])
        for i in picked:
            w.writerow([i["item_id"], i["image_file"], f"target-render/{i['item_id']}.png",
                        i["failure_group"], i.get("hard_opportunity", False), "", ""])
    return len(picked)


def write_rendering_sanity_sheet(items: list[dict], out: Path) -> int:
    clean = sorted({i["image_file"] for i in items if i["expected_verdict"] == "match"})
    step = max(1, len(clean) // RENDERING_SANITY_IMAGES)
    picked = clean[::step][:RENDERING_SANITY_IMAGES]
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["image", "looks_like_normal_hindi_text", "reader_note"])
        for p in picked:
            w.writerow([p, "", ""])
    return len(picked)


def main():
    here = Path(__file__).resolve().parent
    repo = here.parents[2]
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base-strings", type=Path, default=None)
    ap.add_argument("--eval003-manifest", type=Path,
                    default=repo / "eval/calibration/devanagari-v0/candidate-manifest.jsonl")
    ap.add_argument("--out-dir", type=Path, default=here / "native-validation")
    ap.add_argument("--from-build", type=Path, default=None,
                    help="a build directory; required for the perceptibility and sanity sheets")
    a = ap.parse_args()

    a.out_dir.mkdir(parents=True, exist_ok=True)
    bases = load_base_strings(a.base_strings, a.eval003_manifest)
    n = write_word_sheet(bases, a.out_dir / "word-validation-sheet.csv")
    print(f"word-validation-sheet.csv        {n} words, answers blank")

    if a.from_build:
        items = [json.loads(l) for l in
                 (a.from_build / "items.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        n2 = write_perceptibility_sheet(items, a.out_dir / "perceptibility-sheet.csv",
                                        a.from_build)
        n3 = write_rendering_sanity_sheet(items, a.out_dir / "rendering-sanity-sheet.csv")
        print(f"perceptibility-sheet.csv         {n2} pairs")
        print(f"rendering-sanity-sheet.csv       {n3} images")
    else:
        print("(perceptibility and rendering-sanity sheets need --from-build <build dir>)")
    print("\nPREPARED, NOT EXECUTED. No human has been asked anything; every answer column is blank.")


if __name__ == "__main__":
    main()
