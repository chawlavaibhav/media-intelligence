"""Controlled taste tests: every pair differs in exactly ONE factor, so a pick says something about that factor.

Rounds 1–2 compared whole layouts that differed in several ways at once (position, alignment, font, colour, balance)
and credited the win to the template's name — the founder rightly called them bad tests. Here each factor has a base and
a variant; everything else (picture, copy, brand, other template properties) is held fixed.

  python -m product.typeset.experiment build --out DIR       # renders pairs for the brands in BRANDS + taste page
  python -m product.typeset.experiment read  --out DIR --results results.json   # per-factor verdicts
"""
from __future__ import annotations

import argparse
import itertools
import json
import random
from pathlib import Path

from product.typeset import checks as C
from product.typeset import engine as E

# Each factor: (question it answers, level A (name, template, system, overrides), level B (...)).
# Base look: text under the product, centred, sans (modern_clean). Logo top-left in every variant so it never confounds.
LOGO_TL = {"corners": {"logo": "tl"}}
FACTORS = {
    "alignment": ("Centred text or left-aligned text?",
                  ("centred", "bottom_center", "modern_clean", LOGO_TL),
                  ("left-aligned", "bottom_center", "modern_clean", {**LOGO_TL, "block": {"align": "left"}})),
    "text_position": ("Text under the product or above it?",
                      ("text below", "bottom_center", "modern_clean", LOGO_TL),
                      ("text above", "bottom_center", "modern_clean",
                       {**LOGO_TL, "block": {"box": [0.08, 0.13, 0.92, 0.34], "valign": "top"}, "plate": "fit_below",
                        "corners": {"logo": "bl"}})),
    "colour_band": ("Text on the plain background or on a band of brand colour?",
                    ("no band", "bottom_center", "modern_clean", LOGO_TL),
                    ("brand-colour band", "panel_bottom", "modern_clean",
                     {**LOGO_TL, "block": {"align": "center", "box": [0.07, 0.75, 0.93, 0.95]}})),
    "typeface": ("Sans-serif headline or serif headline?",
                 ("sans", "bottom_center", "modern_clean", LOGO_TL),
                 ("serif", "bottom_center", "warm_serif", LOGO_TL)),
    "headline_size": ("Modest headline or big headline?",
                      ("modest", "bottom_center", "modern_clean", {**LOGO_TL, "headline": {"max_size": 0.055, "min_size": 0.052}}),
                      ("big", "bottom_center", "modern_clean",
                       {**LOGO_TL, "headline": {"max_size": 0.10, "min_size": 0.085, "max_lines": 2},
                        "block": {"box": [0.06, 0.64, 0.94, 0.95]}})),
    "symmetry": ("Product centred (symmetric) or product off-centre?",
                 ("product centred", "bottom_center", "modern_clean", LOGO_TL),
                 ("product off-centre", "bottom_center", "modern_clean", {**LOGO_TL, "product_shift": 0.12})),
}

EV = Path.home() / "Vaibhav_Personal_Projects"
BRANDS = [
    {"name": "Mokobara", "fmt": "4:5",
     "plate": EV / "mi-p1-evidence/livebeta/media/job_20260923_6720871c/gen/plate_4x5__att-0018.png",
     "product_box": [0.13, 0.18, 0.86, 0.86],
     "logo_glob": EV / "mi-p1-evidence/livebeta/media/job_20260923_6720871c/uploads",
     "copy": [{"id": "C01", "text": "Room for the long way home.", "role": "headline"},
              {"id": "C02", "text": "mokobara.com", "role": "small"}],
     "kit": {"primary": "#101820", "ink": "#101820", "background": "#F4F1EA"}},
    {"name": "Cumin Co.", "fmt": "4:5",
     "plate": EV / "media-intelligence-agency-exp/agency/jobs/AGY-2026-09-20-CUMIN-EXP-B-FIVESTAGE-001/source/images/Slide_01.jpg",
     "product_box": None, "logo_glob": None,
     "copy": [{"id": "C01", "text": "Pinch. Lift. Eat.", "role": "headline"}, {"id": "C02", "text": "Cumin Co.", "role": "small"}],
     "kit": {"primary": "#3E4A3D", "ink": "#23261F", "background": "#F3EFE7"}},
]


def _kit(b: dict) -> E.BrandKit:
    logo = next(Path(b["logo_glob"]).glob("*logo*"), None) if b["logo_glob"] else None
    return E.BrandKit(name=b["name"], logo=logo, **b["kit"])


def build(out: Path, seed: int = 3) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    pairs, problems = [], []
    for b in BRANDS:
        kit = _kit(b)
        pb = b["product_box"] or E.detect_product_box(b["plate"])
        for fid, (question, A, B) in FACTORS.items():
            files = []
            for lvl, tid, sid, ov in (A, B):
                L = E.layout(template_id=tid, fmt=b["fmt"], system_id=sid, kit=kit, copy=b["copy"], plate=b["plate"],
                             product_box_norm=pb, overrides=ov)
                rows = C.run(L)
                bad = [r["check_id"] for r in C.blocking_failures(rows) if not (fid == "symmetry" and r["check_id"] == "product_clear")]
                if bad:
                    problems.append({"brand": b["name"], "factor": fid, "level": lvl, "blocking": bad})
                name = f"{b['name'].replace(' ', '').replace('.', '').lower()}-{fid}-{lvl.replace(' ', '_').replace('-', '_')}.png"
                L["image"].save(out / name)
                files.append(name)
            pairs.append({"brand": b["name"], "factor": fid, "question": question, "a": files[0], "b": files[1],
                          "a_level": A[0], "b_level": B[0]})
    random.Random(seed).shuffle(pairs)
    (out / "pairs.json").write_text(json.dumps(pairs, indent=1))
    from product.typeset import taste
    page = taste.page_pairs(out, [(p["a"], p["b"]) for p in pairs], title="Round 3 — one difference per pair")
    return {"pairs": len(pairs), "page": str(page), "problems": problems}


def read(out: Path, results: list) -> dict:
    pairs = json.loads((out / "pairs.json").read_text())
    by_files = {frozenset((p["a"], p["b"])): p for p in pairs}
    verdict = {}
    for r in results:
        p = by_files[frozenset((r["winner"], r["loser"]))]
        lvl = p["a_level"] if r["winner"] == p["a"] else p["b_level"]
        verdict.setdefault(p["factor"], {"question": p["question"], "picks": {}})["picks"][p["brand"]] = lvl
    for f, v in verdict.items():
        levels = set(v["picks"].values())
        v["consistent_across_brands"] = len(levels) == 1 and len(v["picks"]) > 1
    return verdict


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["build", "read"])
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--results", type=Path)
    a = ap.parse_args()
    if a.cmd == "build":
        print(json.dumps(build(a.out), indent=1))
    else:
        print(json.dumps(read(a.out, json.loads(a.results.read_text())), indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
