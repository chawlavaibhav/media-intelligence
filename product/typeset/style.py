"""Style features (descriptors, NOT rules).

2026-09-23: the founder rejected turning taste picks into rules ("it is variable, you can't make it a rule"). Features are
used only to DESCRIBE layouts — to build a varied shortlist (picker.shortlist) and to analyse picks. `data/style.yaml`
records what round 3 showed, as history; `score()` below is not used by the picker.

Original notes:

A layout is described by a handful of design features a person actually judges (where the text sits, alignment, a
colour band, serif or sans, headline scale, whether the product sits off-centre). The founder's controlled picks
(experiment.py) set a preference per feature — globally when both brands agreed, per brand when they split. The
picker then scores any layout, from any template, by how many preferences it meets. Unlike template-name weights this
carries to new templates and new brands.
"""
from __future__ import annotations

import yaml

from product.typeset import engine as E

STYLE = E.DATA / "style.yaml"
POINTS = 8.0          # score per met (+) or missed (−) preference


def features(L: dict) -> dict:
    W, H = L["canvas"]
    texts = [e for e in L["elements"] if e.kind == "text"]
    head = next((e for e in texts if e.role in ("headline", "offer")), texts[0] if texts else None)
    f = {}
    if head is not None:
        f["alignment"] = "centred" if head.align == "center" else "left-aligned"
        serif = E._family(head.family, None).get("class") == "serif" if not head.family.startswith("brand_") else None
        if serif is not None:
            f["typeface"] = "serif" if serif else "sans"
        f["headline_size"] = "big" if head.size / W >= 0.075 else "modest"
        pb = L.get("product_box")
        if pb:
            f["text_position"] = "text above" if (head.box[1] + head.box[3]) / 2 < (pb[1] + pb[3]) / 2 else "text below"
    f["colour_band"] = "brand-colour band" if L.get("panel") else "no band"
    pb = L.get("product_box")
    if pb:
        f["symmetry"] = "product off-centre" if abs((pb[0] + pb[2]) / 2 - W / 2) > W * 0.06 else "product centred"
    return f


def profile() -> dict:
    return yaml.safe_load(STYLE.read_text()) if STYLE.exists() else {"global": {}, "brands": {}}


def preferences(brand: str = "") -> dict:
    p = profile()
    out = {k: v["prefer"] for k, v in (p.get("global") or {}).items()}
    out.update({k: v["prefer"] for k, v in ((p.get("brands") or {}).get(brand) or {}).items()})
    return out


def score(L: dict, brand: str = "") -> float:
    prefs, feats = preferences(brand), features(L)
    return sum(POINTS if feats.get(k) == v else -POINTS for k, v in prefs.items() if k in feats)


def learn_from_experiment(verdict: dict, source: str) -> dict:
    """Round-3-style verdicts → style.yaml: agreed factors become global, split ones become per-brand."""
    p = profile()
    p.setdefault("global", {})
    p.setdefault("brands", {})
    for factor, v in verdict.items():
        picks = v["picks"]
        if v.get("consistent_across_brands"):
            p["global"][factor] = {"prefer": next(iter(picks.values())), "evidence": f"{source}: {sorted(picks)} agreed"}
            for b in picks:
                (p["brands"].get(b) or {}).pop(factor, None)
        else:
            for b, lvl in picks.items():
                p["brands"].setdefault(b, {})[factor] = {"prefer": lvl, "evidence": f"{source}: 1 controlled pick"}
    STYLE.write_text(yaml.safe_dump(p, sort_keys=True, allow_unicode=True))
    return p
