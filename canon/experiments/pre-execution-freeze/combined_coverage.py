#!/usr/bin/env python3
"""CANON-010 / C10-E — measure the original 30 + extension against Media Request Grammar v1.

STRUCTURAL COVERAGE ONLY. This reports which request operations and feature co-occurrences the
combined bank exercises. It reports NO frequency and NO market share, because neither bank is
demand evidence — the 30 are authored probes and the 11 are authored probes.

Run: python3 canon/experiments/pre-execution-freeze/combined_coverage.py
"""
from __future__ import annotations

import collections
import json
import pathlib
import sys

import yaml

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
GRAMMAR = HERE / "MEDIA-REQUEST-GRAMMAR-v1.yaml"
EXT = HERE / "REQUEST-COVERAGE-EXTENSION.jsonl"
BANK = ROOT / "canon/experiments/v1/brief-bank/briefs-source.yaml"
OUT = HERE / "combined-coverage-measurement.json"


def classify_30(b: dict) -> dict:
    """Classify an original brief against the grammar. All 30 are generate requests.

    CANON-009 established this by measurement: no brief in the 30 asks to modify or animate a
    supplied artefact. Assets appear as references informing a NEW artefact, which is `generate`.
    """
    ai = b.get("authoritative_intent") or {}
    return {
        "id": b["brief_id"],
        "requested_operation": "generate",
        "media_class": b["media_class"],
        "language": b["language_condition"],
        "cardinality": 1,
        "acceptance_basis": "per_deliverable",
        "has_supplied_asset_as_subject": False,
        "has_reference": bool(b.get("brand_assets")),
        "has_exact_text": b["copy_requirement"] == "exact_strings_required",
        "has_speech": bool(ai.get("voiceover_script_exact") or ai.get("spoken_script_exact")
                           or ai.get("dialogue_exact")),
        "has_camera_motion": False,
        "has_subject_motion": b["media_class"] == "video",
        "motion_separated": False,
        "has_objective": True,
        "has_ambiguity_marker": b["specification_quality"] in ("underspecified", "contradictory"),
        "runnable_wave1": True,
        "source": "original_30",
    }


def classify_ext(r: dict) -> dict:
    mi = r.get("mutation_intents") or {}
    motion = r.get("motion_intent") or {}
    return {
        "id": r["item_id"],
        "requested_operation": r["requested_operation"],
        "media_class": r["media_class"],
        "language": r["language"],
        "cardinality": r["deliverable_set"]["cardinality"],
        "acceptance_basis": r["deliverable_set"]["acceptance_basis"],
        "has_supplied_asset_as_subject": any(
            a.get("role") == "subject_of_operation" for a in r.get("supplied_inputs", [])),
        "has_reference": any(a.get("role", "").endswith("_reference") or a.get("role") == "brand_asset"
                             for a in r.get("supplied_inputs", [])),
        "has_exact_text": any('"' in c for c in r["constraints"].get("hard", [])),
        "has_speech": False,
        "has_camera_motion": bool(motion.get("camera_motion")),
        "has_subject_motion": bool(motion.get("subject_motion")),
        "motion_separated": bool(motion.get("camera_motion")) and "subject_motion" in motion,
        "has_objective": True,
        "has_ambiguity_marker": False,
        "runnable_wave1": r["runnable_wave1"],
        "source": "extension",
    }


def main() -> int:
    grammar = yaml.safe_load(GRAMMAR.read_text())
    all_ops = set(grammar["vocabularies"]["requested_operation"]["values"])
    rows = [classify_30(b) for b in yaml.safe_load(BANK.read_text())["briefs"]]
    rows += [classify_ext(json.loads(l)) for l in EXT.read_text().splitlines()]

    covered_ops = {r["requested_operation"] for r in rows}
    ext_cooc = collections.Counter()
    for l in EXT.read_text().splitlines():
        for c in json.loads(l).get("covers_cooccurrence", []):
            ext_cooc[c] += 1

    def n(pred):
        return sum(1 for r in rows if pred(r))

    result = {
        "task": "CANON-010 / C10-E",
        "note": "Structural coverage only. No frequency or market-share claim is made or implied.",
        "totals": {"original_30": 30, "extension": len(rows) - 30, "combined": len(rows),
                   "runnable_wave1": n(lambda r: r["runnable_wave1"]),
                   "representation_only": n(lambda r: not r["runnable_wave1"])},
        "operations": {
            "in_grammar": sorted(all_ops),
            "covered": sorted(covered_ops),
            "not_covered": sorted(all_ops - covered_ops),
            "by_operation": dict(collections.Counter(r["requested_operation"] for r in rows)),
            "by_operation_original_30": dict(collections.Counter(
                r["requested_operation"] for r in rows if r["source"] == "original_30")),
            "by_operation_extension": dict(collections.Counter(
                r["requested_operation"] for r in rows if r["source"] == "extension")),
        },
        "features": {
            "supplied_asset_as_subject": {"combined": n(lambda r: r["has_supplied_asset_as_subject"]),
                                          "original_30": 0},
            "reference_supplied": {"combined": n(lambda r: r["has_reference"])},
            "exact_text": {"combined": n(lambda r: r["has_exact_text"])},
            "speech": {"combined": n(lambda r: r["has_speech"]),
                       "extension": 0,
                       "note": "speech remains original-30 only; no corpus evidence exists for it"},
            "camera_motion_declared": {"combined": n(lambda r: r["has_camera_motion"]),
                                       "original_30": 0},
            "camera_and_subject_motion_separated": {"combined": n(lambda r: r["motion_separated"]),
                                                    "original_30": 0},
            "cardinality_gt_1": {"combined": n(lambda r: r["cardinality"] > 1), "original_30": 0},
            "set_level_acceptance": {"combined": n(lambda r: r["acceptance_basis"] == "set_level"),
                                     "original_30": 0},
            "ambiguity_markers": {"combined": n(lambda r: r["has_ambiguity_marker"]),
                                  "extension": 0},
            "objective_present": {"combined": n(lambda r: r["has_objective"]), "share": 1.0},
        },
        "extension_cooccurrences": dict(ext_cooc),
        "languages": {
            "combined": dict(collections.Counter(r["language"] for r in rows)),
        },
        "per_item": rows,
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("per_item",)},
                     indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
