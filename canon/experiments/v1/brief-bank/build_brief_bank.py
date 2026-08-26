#!/usr/bin/env python3
"""CANON-V1 / C2 — validate the 30-brief bank and emit briefs.jsonl.

WHY A VALIDATOR AND NOT A CHECKLIST. The runbook fixes exact balance counts — 10/10/10 by language,
10 families of 3, a 12-brief early-gate subset with six simultaneous constraints. Those are easy to
believe and hard to keep true by hand once briefs are edited. This fails closed: any violation is a
non-zero exit and nothing is written.

It also enforces the one rule that protects the experiment: `customer_brief` must not contain a
finished Creative IR. Producing that from the brief is what Experiment A measures.

Run: python3 canon/experiments/v1/brief-bank/build_brief_bank.py
"""
from __future__ import annotations

import collections
import json
import pathlib
import sys

import yaml

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SRC = HERE / "briefs-source.yaml"
OUT = HERE / "briefs.jsonl"
GATE = ROOT / "canon/experiments/v1/value-gate/early-12-manifest.json"

FAMILIES = [
    "typography_led_offer_static", "product_packshot_static", "person_product_static",
    "reference_based_campaign", "product_hero_video_vo", "actor_product_video_no_dialogue",
    "one_visible_speaker", "two_person_dialogue", "product_handoff_action", "multi_shot_branded_ad",
]
LANGS = ["english_primary", "hindi_devanagari_primary", "hinglish_mixed"]
PACKS = [
    "composition_and_attention", "typography_and_copy", "product_appearance",
    "colour_and_visual_register", "camera_and_spatial_grammar", "editing_pacing_and_short_form",
    "commercial_communication", "concept_and_distinctiveness", "indian_indic_context",
    "critique_and_effectiveness",
]
CAP_FAMILIES = [
    "constraint_fidelity", "text_and_brand", "identity_and_references", "human_physical_realism",
    "temporal_continuity", "speech_audio", "commercial_creative_fitness", "operational_workflow",
]
# Phrases that would mean a finished Creative IR leaked into the customer-facing brief.
IR_LEAK_MARKERS = [
    "creative ir", "acceptance contract", "rank-1", "hierarchy:", "normalized request",
]


def packs_for(b: dict) -> list[str]:
    """Which Canon knowledge packs a brief requires. Derived, not hand-typed per brief."""
    p = {"commercial_communication", "concept_and_distinctiveness", "critique_and_effectiveness"}
    if b["media_class"] == "static":
        p.add("composition_and_attention")
    else:
        p |= {"editing_pacing_and_short_form", "camera_and_spatial_grammar"}
    if b["copy_requirement"] == "exact_strings_required":
        p.add("typography_and_copy")
    if b["product_prominence"] == "hero":
        p.add("product_appearance")
    if b.get("brand_assets"):
        p.add("colour_and_visual_register")
    if b["language_condition"] in ("hindi_devanagari_primary", "hinglish_mixed"):
        p |= {"indian_indic_context", "typography_and_copy"}
    return sorted(p)


def caps_for(b: dict) -> list[str]:
    """Eval capability families a brief is likely to exercise. Canon states requirements only —
    this names no model, no provider and no measurement method."""
    c = {"constraint_fidelity", "commercial_creative_fitness"}
    if b["copy_requirement"] == "exact_strings_required":
        c.add("text_and_brand")
    if b.get("brand_assets"):
        c.add("identity_and_references")
    if b["people_count"] > 0:
        c |= {"human_physical_realism", "identity_and_references"}
    if b["media_class"] == "video":
        c.add("temporal_continuity")
    if b.get("authoritative_intent", {}).get("voiceover_script_exact") \
       or b.get("authoritative_intent", {}).get("spoken_script_exact") \
       or b.get("authoritative_intent", {}).get("dialogue_exact"):
        c.add("speech_audio")
    if b.get("specification_quality") in ("underspecified", "contradictory"):
        c.add("operational_workflow")
    return sorted(c)


def main() -> int:
    doc = yaml.safe_load(SRC.read_text())
    briefs = doc["briefs"]
    errors: list[str] = []

    if len(briefs) != 30:
        errors.append(f"expected 30 briefs, found {len(briefs)}")

    by_family = collections.Counter(b["scenario_family"] for b in briefs)
    for f in FAMILIES:
        if by_family.get(f) != 3:
            errors.append(f"family {f} has {by_family.get(f, 0)} briefs, expected exactly 3")
    for f in by_family:
        if f not in FAMILIES:
            errors.append(f"unknown scenario family {f!r}")

    by_lang = collections.Counter(b["language_condition"] for b in briefs)
    for l in LANGS:
        if by_lang.get(l) != 10:
            errors.append(f"language {l} has {by_lang.get(l, 0)} briefs, expected exactly 10")

    # Language must not be confounded with family: one of each language per family.
    for f in FAMILIES:
        ls = sorted(b["language_condition"] for b in briefs if b["scenario_family"] == f)
        if ls != sorted(LANGS):
            errors.append(f"family {f} language spread is {ls}, expected one of each")

    ids = [b["brief_id"] for b in briefs]
    for i, n in collections.Counter(ids).items():
        if n > 1:
            errors.append(f"duplicate brief_id {i}")

    for b in briefs:
        bid = b["brief_id"]
        ai = b.get("authoritative_intent") or {}
        if not b.get("customer_brief", "").strip():
            errors.append(f"{bid}: empty customer_brief")
        if not ai:
            errors.append(f"{bid}: missing authoritative_intent")
        low = b.get("customer_brief", "").lower()
        for marker in IR_LEAK_MARKERS:
            if marker in low:
                errors.append(f"{bid}: customer_brief contains Creative IR language {marker!r}")
        if b.get("specification_quality") == "contradictory" and not ai.get("contradictions_planted"):
            errors.append(f"{bid}: marked contradictory but plants no contradiction")
        if b.get("specification_quality") == "clear" and ai.get("contradictions_planted"):
            errors.append(f"{bid}: marked clear but plants a contradiction")
        if b.get("specification_quality") == "underspecified" and not ai.get("underspecified_aspects"):
            errors.append(f"{bid}: marked underspecified but names no underspecified aspect")
        # Every exact string demanded must actually appear in what the customer wrote.
        for s in ai.get("must_appear_exactly", []):
            if s not in b["customer_brief"]:
                errors.append(f"{bid}: required exact string {s!r} is not present in customer_brief")
        if b["media_class"] == "video" and not b.get("duration_seconds"):
            errors.append(f"{bid}: video brief has no duration")
        if b["media_class"] == "video" and not (6 <= b.get("duration_seconds", 0) <= 20):
            errors.append(f"{bid}: duration {b.get('duration_seconds')}s is outside the 6-20s scope")

    # Required variety across the bank.
    for field, minimum in (("objective", 5), ("product_category", 10)):
        n = len({b[field] for b in briefs})
        if n < minimum:
            errors.append(f"only {n} distinct {field} values across the bank, expected >= {minimum}")
    spec = collections.Counter(b["specification_quality"] for b in briefs)
    for k in ("clear", "underspecified", "contradictory"):
        if spec.get(k, 0) < 5:
            errors.append(f"only {spec.get(k, 0)} {k} briefs, expected >= 5")
    if not any(b["copy_requirement"] == "minimal_copy" for b in briefs):
        errors.append("no minimal-copy brief in the bank")
    people = collections.Counter(b["people_count"] for b in briefs)
    for n in (0, 1, 2):
        if people.get(n, 0) < 4:
            errors.append(f"only {people.get(n, 0)} briefs with {n} people, expected >= 4")

    if errors:
        print(json.dumps({"error_count": len(errors), "errors": errors}, indent=2))
        return 1

    rows = []
    for b in briefs:
        rows.append({
            "brief_id": b["brief_id"],
            "scenario_family": b["scenario_family"],
            "media_class": b["media_class"],
            "language_condition": b["language_condition"],
            "duration_seconds": b.get("duration_seconds"),
            "business": b["business"],
            "tags": {
                "objective": b["objective"],
                "product_category": b["product_category"],
                "product_prominence": b["product_prominence"],
                "people_count": b["people_count"],
                "brand_assets": b.get("brand_assets", []),
                "copy_requirement": b["copy_requirement"],
                "specification_quality": b["specification_quality"],
                "knowledge_packs_required": packs_for(b),
                "capability_families_likely": caps_for(b),
            },
            # What the customer said. Deliberately incomplete. This is the experiment input.
            "customer_brief": " ".join(b["customer_brief"].split()),
            # Scoring only. Never shown to a planning arm.
            "authoritative_intent": b["authoritative_intent"],
        })

    OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))

    summary = {
        "briefs": len(rows),
        "families": dict(by_family),
        "languages": dict(by_lang),
        "media_class": dict(collections.Counter(r["media_class"] for r in rows)),
        "objectives": dict(collections.Counter(r["tags"]["objective"] for r in rows)),
        "specification_quality": dict(spec),
        "people_count": dict(people),
        "distinct_product_categories": len({r["tags"]["product_category"] for r in rows}),
        "briefs_with_planted_contradictions": sum(
            1 for r in rows if r["authoritative_intent"].get("contradictions_planted")),
        "total_planted_contradictions": sum(
            len(r["authoritative_intent"].get("contradictions_planted") or []) for r in rows),
        "pack_demand": dict(collections.Counter(
            p for r in rows for p in r["tags"]["knowledge_packs_required"])),
        "capability_demand": dict(collections.Counter(
            c for r in rows for c in r["tags"]["capability_families_likely"])),
        "output": str(OUT.relative_to(ROOT)),
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
