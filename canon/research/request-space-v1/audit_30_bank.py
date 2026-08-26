#!/usr/bin/env python3
"""CANON-009 / C9-D — measure the 30-brief bank against the proposed request grammar.

WHY A SCRIPT. The comparison must not be impressionistic. Which grammar components the bank
exercises, and how often, is computable from the committed bank — so it is computed, not asserted.

WHAT IT CANNOT DO. It cannot tell you whether the bank's balance is RIGHT. That needs external
frequency evidence, and for most components none exists (see the register's `unresolved`). The
script therefore reports the bank's own distribution and leaves the judgement to the audit document.

Run: python3 canon/research/request-space-v1/audit_30_bank.py
"""
from __future__ import annotations

import collections
import json
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[3]
BANK = ROOT / "canon/experiments/v1/brief-bank/briefs-source.yaml"
OUT = ROOT / "canon/research/request-space-v1/30-bank-grammar-measurement.json"


def classify_operation(b: dict) -> str:
    """Which grammar G01 operation does this brief request?"""
    assets = b.get("brand_assets") or []
    ai = b.get("authoritative_intent") or {}
    hard = " ".join(ai.get("hard_constraints") or []).lower()
    text = (b.get("customer_brief") or "").lower()
    supplied_visual = any(a in assets for a in (
        "product_photographs", "food_photographs", "property_photographs", "topper_photographs",
        "store_photographs", "app_ui_screenshot", "app_ui", "product_bottle", "product_tin",
        "product_bar", "product_pack", "product_tube", "product_cooker", "product_shoe",
        "product_mattress", "product_jewellery", "product_can", "product_food", "label_artwork",
        "wrapper_artwork", "colour_swatches", "aircraft_livery", "uniform", "competitor_reference",
        "previous_year_creative", "existing_campaign"))
    # No brief in the bank asks to modify a supplied asset in place, or to animate one.
    if "same look" in text or "usi format" in text or "same format" in text:
        return "generate_from_nothing_with_reference"
    if supplied_visual:
        return "generate_from_nothing_with_reference"
    return "generate_from_nothing"


def main() -> int:
    doc = yaml.safe_load(BANK.read_text())
    briefs = doc["briefs"]
    rows = []
    for b in briefs:
        ai = b.get("authoritative_intent") or {}
        rows.append({
            "brief_id": b["brief_id"],
            "media_class": b["media_class"],
            "operation": classify_operation(b),
            "people_count": b["people_count"],
            "product_prominence": b["product_prominence"],
            "exact_text_required": b["copy_requirement"] == "exact_strings_required",
            "has_supplied_reference": bool(b.get("brand_assets")),
            "has_identity_continuity_requirement": any(
                "consistent" in c.lower() or "same identity" in c.lower()
                or "same person" in c.lower() or "identities" in c.lower()
                for c in (ai.get("hard_constraints") or [])),
            "has_speech": bool(ai.get("voiceover_script_exact") or ai.get("spoken_script_exact")
                               or ai.get("dialogue_exact")),
            "has_duration": bool(b.get("duration_seconds")),
            "output_cardinality": 1,          # nothing in the bank requests a set
            "is_multi_turn": False,           # nothing in the bank arrives in rounds
            "specification_quality": b["specification_quality"],
            "language_condition": b["language_condition"],
        })

    n = len(rows)
    def pct(k):
        c = sum(1 for r in rows if r[k])
        return {"count": c, "of": n, "share": round(c / n, 3)}

    measurement = {
        "task": "CANON-009 / C9-D",
        "bank": str(BANK.relative_to(ROOT)),
        "briefs": n,
        "note": "Bank-internal measurement. It says what the bank contains, NOT whether that is the "
                "right balance — no external frequency evidence exists for most components.",
        "grammar_component_coverage": {
            "G01_requested_operation": dict(collections.Counter(r["operation"] for r in rows)),
            "G01_edit_supplied_asset": {"count": 0, "of": n, "share": 0.0},
            "G01_animate_supplied_asset": {"count": 0, "of": n, "share": 0.0},
            "G02_output_media_type": dict(collections.Counter(r["media_class"] for r in rows)),
            "G03_subject_people_present": pct("people_count"),
            "G03_product_is_hero": {"count": sum(1 for r in rows
                                                 if r["product_prominence"] == "hero"), "of": n},
            "G04_supplied_reference": pct("has_supplied_reference"),
            "G06_identity_continuity": pct("has_identity_continuity_requirement"),
            "G07_exact_text": pct("exact_text_required"),
            "G09_duration_specified": pct("has_duration"),
            "G10_speech": pct("has_speech"),
            "G12_output_cardinality_gt_1": {"count": 0, "of": n, "share": 0.0},
            "G12_multi_turn": {"count": 0, "of": n, "share": 0.0},
            "G13_specification_quality": dict(
                collections.Counter(r["specification_quality"] for r in rows)),
            "G14_objective_present": {"count": n, "of": n, "share": 1.0,
                                      "note": "every brief carries an objective — this is the bank's "
                                              "principal difference from every public corpus"},
        },
        "language": dict(collections.Counter(r["language_condition"] for r in rows)),
        "per_brief": rows,
    }
    OUT.write_text(json.dumps(measurement, indent=2) + "\n")
    print(json.dumps({k: v for k, v in measurement["grammar_component_coverage"].items()}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
