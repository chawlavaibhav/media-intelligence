"""Drop-in entry points for the production pipeline, with the same return shape as product/compose.py
(`(out_path, check_rows, layout_meta)`), so the P1 v2 build can switch its sign painter to this engine behind a flag.

Check rows use the v1 shape: {check_id, control, status, detail, evidence}; blocking typography failures are FAIL rows
the presentation gateway already refuses on.
"""
from __future__ import annotations

from pathlib import Path

from product.typeset import engine as E
from product.typeset import picker

CONTROL = {"exact_copy": "EXACT_TEXT_RENDERED", "contrast": "CONTRAST_GATE", "safe_area": "TEXT_BOUNDS_GATE",
           "product_clear": "HERO_VISIBLE", "no_collisions": "ELEMENT_DISJOINTNESS"}


def _rows(checks: list) -> list:
    return [{"check_id": f"type:{r['check_id']}", "control": CONTROL.get(r["check_id"], "TYPOGRAPHY"), "status": r["status"],
             "detail": r["detail"], "evidence": {"blocking": r["blocking"]}} for r in checks]


def _pick(kit, fmt, kind, copy, plate, product_box_norm):
    cands = picker.candidates(kit=kit, fmt=fmt, kind=kind, copy=copy, plate=plate, product_box_norm=product_box_norm)
    best = next((c for c in cands if c["layout"] is not None), None)
    if best is None:
        raise E.TypesetError("no template could fit this copy: " + "; ".join(c["error"] or "" for c in cands[:3]))
    return best, cands


def _meta(best, cands) -> dict:
    L = best["layout"]
    return {"engine": "typeset", "template": best["template"], "system": best["system"], "score": best["score"],
            "canvas": list(L["canvas"]), "boxes": {(e.id or e.role): list(e.box) for e in L["elements"]},
            "rendered_text": [" ".join(e.lines) for e in L["elements"] if e.kind == "text"],
            "fonts": {e.role: {"family": e.family, "weight": e.weight, "size": e.size} for e in L["elements"] if e.kind == "text"},
            "alternatives": [{"template": c["template"], "system": c["system"], "score": c["score"]} for c in cands[:6]]}


def still_ad(*, plate: Path, out: Path, aspect: str, direction: dict, kit: E.BrandKit, product_box_norm: list | None):
    copy = E.roles_from_copy_deck(direction.get("copy_deck", []))
    best, cands = _pick(kit, aspect, "poster", copy, plate, product_box_norm)
    best["layout"]["image"].save(out)
    return out, _rows(best["checks"]), _meta(best, cands)


def end_card(*, out: Path, aspect: str, direction: dict, kit: E.BrandKit):
    deck = direction.get("copy_deck", [])
    ids = (direction.get("end_card") or {}).get("copy_ids")
    if ids:
        deck = [c for i in ids for c in deck if c["id"] == i]
    copy = E.roles_from_copy_deck(deck)
    best, cands = _pick(kit, aspect, "endcard", copy, None, None)
    best["layout"]["image"].save(out)
    return out, _rows(best["checks"]), _meta(best, cands)
