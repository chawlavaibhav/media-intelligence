#!/usr/bin/env python3
"""Materialise the four frozen A-TEXT comparability items.

These four strings are FROZEN by Controller decision. They are not a sample, they are not tunable,
and they may not be swapped after seeing a result — that would be an experiment mutation reported
as the original run.

    ATEXT-01  शुभ दीपावली        Devanagari, festival greeting
    ATEXT-02  आज की डील          Devanagari, ordinary commercial phrase
    ATEXT-03  Aaj ki Deal        the same phrase in Hinglish/Latin
    ATEXT-04  SAVE 20% • ₹999    a commercial claim with a digit, a symbol and a rupee sign

Each prompt asks for a plain 1:1 poster whose ONLY textual content is the target: no logo, no
product or reference identity, no extra copy. That is deliberate. It isolates text rather than
pretending to measure creative quality, and it means a failure is attributable.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "atex-items-v1.jsonl"

PROMPT = (
    "A plain square poster on a flat, evenly lit background.\n"
    "The only textual content in the image is exactly this string, rendered clearly and "
    "legibly:\n"
    "{target}\n"
    "No logo. No brand mark. No product. No person. No other text of any kind — no captions, "
    "no taglines, no watermark, no additional text anywhere in the frame.\n"
    "Render the string exactly as given, character for character."
)

ITEMS = (
    ("ATEXT-01", "शुभ दीपावली", "devanagari"),
    ("ATEXT-02", "आज की डील", "devanagari"),
    ("ATEXT-03", "Aaj ki Deal", "latin_hinglish"),
    ("ATEXT-04", "SAVE 20% • ₹999", "latin_commercial_claim"),
)


def build_records() -> list[dict]:
    return [{
        "item_id": item_id,
        "operation": "generate",
        "target_string": target,
        "script": script,
        "prompt": PROMPT.format(target=target),
        "aspect_ratio": "1:1",
        "extra_text_forbidden": True,
        "reference_identity": None,
        "product_identity": None,
        "seed_policy": "unseeded",
        "seed": None,
        "repeats_per_slot": 2,
        "poolable_with_held_seed_evidence": False,
        "primary_measurement": "transcribe_then_code_exact_comparison",
        "verdict_is_diagnostic_only": True,
        "evidence_class": "partial_admission_screen_only",
    } for item_id, target, script in ITEMS]


def build(out_path: Path = OUT) -> dict:
    records = sorted(build_records(), key=lambda r: r["item_id"])
    payload = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records)
    out_path.write_text(payload, encoding="utf-8")
    return {"items": len(records), "path": str(out_path)}


if __name__ == "__main__":
    print(json.dumps(build(), ensure_ascii=False, indent=2))
