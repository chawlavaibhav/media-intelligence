"""Render several candidate layouts, drop the ones with blocking defects, rank the rest.

Ranking = craft score (from the checks and measurements) + the founder's learned taste (data/taste.yaml, written by
taste.py) + an optional judge (a vision model shown the survivors). Rendering is local and costs nothing; the judge is
the only paid step and is off unless a callable is passed in.
"""
from __future__ import annotations

from pathlib import Path

import yaml

from product.typeset import checks as C
from product.typeset import engine as E

TASTE = E.DATA / "taste.yaml"


def taste_weights() -> dict:
    if TASTE.exists():
        return yaml.safe_load(TASTE.read_text()) or {}
    return {}


def score(L: dict, rows: list, taste: dict) -> float:
    if C.blocking_failures(rows):
        return -1000.0 - len(C.blocking_failures(rows))
    W, H = L["canvas"]
    s = 50.0
    s -= 6.0 * sum(1 for r in rows if r["status"] == "FLAG")
    head = next((e for e in L["elements"] if e.role == "headline"), None)
    if head:
        s += 20.0 * min(1.0, head.size / (W * 0.08))          # a confident headline, up to ~8 % of width
    pb = L.get("product_box")
    if pb:
        s += 25.0 * min(1.0, ((pb[2] - pb[0]) * (pb[3] - pb[1]) / (W * H)) / 0.35)   # a big product
    # Contrast is a pass/fail check, not a score: extra contrast beyond "readable" earned up to +10 here and pushed the
    # white-on-navy panel layouts to the top; the founder rejected them in 7 of 8 pairs (taste round 1, 2026-09-23).
    # the founder's taste: patterns that held across brands (global) + what this brand's rounds showed (brand)
    s += float(taste.get("templates", {}).get(L["template"], 0.0))
    s += float(taste.get("systems", {}).get(L["system"], 0.0))
    brand = taste.get("brands", {}).get(L.get("brand") or "", {})
    s += float(brand.get("templates", {}).get(L["template"], 0.0))
    s += float(brand.get("systems", {}).get(L["system"], 0.0))
    return round(s, 2)


def candidates(*, kit: E.BrandKit, fmt: str, kind: str, copy: list, plate: Path | None = None,
               product_box_norm: list | None = None, templates: list | None = None, systems: list | None = None,
               judge=None) -> list:
    """All (template × type system) layouts for this format, scored and sorted best first.
    Each item: {template, system, fmt, score, checks, layout (or None), error}."""
    T = E.templates_registry()["templates"]
    tids = templates or kit.preferred_templates or [t for t, v in T.items() if v["kind"] == kind and fmt in v["formats"]]
    sids = systems or ([kit.system] if kit.system else E.systems_for(kit.moods, 3))
    taste = taste_weights()
    out = []
    for tid in tids:
        if fmt not in T[tid]["formats"] or T[tid]["kind"] != kind:
            continue
        slots = set(T[tid].get("block", {}).get("order", [])) | set(T[tid].get("corners", {}))
        roles = {c["role"] for c in copy}
        if ("offer" in slots) != ("offer" in roles):
            continue          # an offer layout needs an offer line; any other layout would drop the offer
        for sid in sids:
            try:
                L = E.layout(template_id=tid, fmt=fmt, system_id=sid, kit=kit, copy=copy, plate=plate,
                             product_box_norm=product_box_norm)
            except E.TypesetError as exc:
                out.append({"template": tid, "system": sid, "fmt": fmt, "score": -2000.0, "checks": [], "layout": None,
                            "error": str(exc)})
                continue
            L["brand"] = kit.name
            rows = C.run(L)
            out.append({"template": tid, "system": sid, "fmt": fmt, "score": score(L, rows, taste), "checks": rows,
                        "layout": L, "error": None})
    out.sort(key=lambda c: -c["score"])
    if judge is not None:
        good = [c for c in out if c["score"] > -1000]
        order = judge(good)                     # a list of indices into `good`, best first
        out = [good[i] for i in order] + [c for c in out if c not in good]
    return out


JUDGE_PROMPT = """You are an art director at a premium advertising agency. You are shown {n} finished layouts of the same ad
(same picture, same exact words), numbered 1..{n}. The brief: {brief}. Rank them best first for this brand and audience,
judging typography only: hierarchy (is the headline clearly the boss), type choice (does the face suit the brand and the
mood), spacing and alignment, balance with the product, and how it reads at phone size. Return JSON:
{{"ranking": [numbers best first], "why_best": "one sentence", "worst_problem": "one sentence"}}."""
