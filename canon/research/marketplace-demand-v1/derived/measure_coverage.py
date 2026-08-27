#!/usr/bin/env python3
"""CANON-011 - compute the coverage figures for COVERAGE-REPORT.md.

Every number in the coverage report comes from here, and from the two committed banks
plus the existing authored bank it is compared against. Nothing is counted by hand.

Writes coverage-measurement.json next to the banks.

    python3 canon/research/marketplace-demand-v1/derived/measure_coverage.py
"""
import collections
import json
import pathlib
import re
import sys

import yaml

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BANK = HERE / "marketplace-brief-bank-v1.yaml"
OUT = HERE / "coverage-measurement.json"
AUTHORED_30 = ROOT / "canon/experiments/v1/brief-bank/briefs.jsonl"
EXTENSION_11 = ROOT / "canon/experiments/pre-execution-freeze/REQUEST-COVERAGE-EXTENSION.jsonl"
UPWORK = ROOT / "canon/research/marketplace-demand-v1/sources/upwork-ai-video-demand-2026-08-26.md"

GRAMMAR_FIELDS = [f"R{i:02d}" for i in range(1, 19)]


def count_appendix_rows():
    """Recount the Upwork appendix directly rather than trusting the prose total."""
    lines = UPWORK.read_text().splitlines()
    start = next(i for i, l in enumerate(lines)
                 if l.startswith("| # | Title | Budget | Proposals | Client spend / location"))
    rows = []
    for l in lines[start:]:
        m = re.match(r"^\|\s*(\d+)\s*\|([^|]*)\|", l)
        if m:
            rows.append((int(m.group(1)), m.group(2).strip()))
    bold = [r for r in rows if r[1].startswith("**")]
    return {
        "appendix_rows": len(rows),
        "bold_titles_source_classified_addressable": len(bold),
        "non_bold_source_classified_not_addressable": len(rows) - len(bold),
    }


def main():
    bank = yaml.safe_load(BANK.read_text())
    cases = bank["cases"]

    ops = collections.Counter(
        c["normalized_request"]["R01_requested_operation"]["value"] for c in cases
    )
    modality = collections.Counter(
        c["normalized_request"]["R05_modality"].get("value") for c in cases
    )

    def spoken(c):
        v = c["normalized_request"]["R10_language_topology"].get("value")
        if not isinstance(v, dict):
            return None
        s = v.get("spoken")
        return tuple(s) if isinstance(s, list) else s

    langs = collections.Counter(spoken(c) for c in cases)
    lang_prov = collections.Counter(
        c["normalized_request"]["R10_language_topology"]["provenance"] for c in cases
    )

    prov_totals = collections.Counter()
    prov_by_field = collections.defaultdict(collections.Counter)
    for c in cases:
        for f, entry in c["normalized_request"].items():
            p = entry.get("provenance")
            prov_totals[p] += 1
            prov_by_field[f[:3]][p] += 1
            for _, sp in (entry.get("sub_field_provenance") or {}).items():
                prov_totals[sp] += 1

    def has_asset_role(c, role):
        v = c["normalized_request"]["R02_supplied_assets"].get("value") or []
        return any(isinstance(a, dict) and a.get("role") == role for a in v)

    def caps(c):
        return set(c["capability_mappings"].get("atomic") or [])

    identity_caps = {"person_identity", "product_identity", "voice_identity_consistency",
                     "wardrobe_invariant_fidelity"}
    text_caps = {"exact_text_latin", "exact_text_devanagari"}

    fam = collections.Counter()
    for c in cases:
        for d in c["evaluator_dependencies"]:
            fam[d["family"]] += 1

    stage_c = collections.Counter(c["stage_fit"]["stage_c_end_to_end"] for c in cases)
    stage_a = collections.Counter(c["stage_fit"]["stage_a_atomic"] for c in cases)
    stage_b = collections.Counter(c["stage_fit"]["stage_b_compound"] for c in cases)

    # --- comparison against the two existing authored banks ------------------------
    authored = [json.loads(l) for l in AUTHORED_30.read_text().splitlines() if l.strip()]
    extension = [json.loads(l) for l in EXTENSION_11.read_text().splitlines() if l.strip()]
    authored_ops = {"generate": len(authored)}
    ext_ops = collections.Counter(r.get("requested_operation") for r in extension)
    authored_exact_text = sum(
        1 for r in authored if r["tags"].get("copy_requirement") == "exact_strings_required"
    )

    result = {
        "task": "CANON-011",
        "computed_by": "canon/research/marketplace-demand-v1/derived/measure_coverage.py",
        "source_records": count_appendix_rows(),
        "cases_total": len(cases),
        "runnable_now_true": sum(1 for c in cases if c["runnable_now"]),
        "runnable_now_false": sum(1 for c in cases if not c["runnable_now"]),
        "attemptable_without_a_planner": collections.Counter(
            str(c["execution_feasibility"]["attemptable_without_a_planner"]) for c in cases
        ),
        "requested_operation_distribution": dict(ops),
        "modality_distribution": dict(modality),
        "spoken_language_distribution": {str(k): v for k, v in langs.items()},
        "language_topology_provenance": dict(lang_prov),
        "provenance_label_totals": dict(prov_totals),
        "provenance_by_grammar_field": {k: dict(v) for k, v in sorted(prov_by_field.items())},
        "supplied_asset_coverage": {
            "cases_with_any_supplied_asset_recorded": sum(
                1 for c in cases
                if c["normalized_request"]["R02_supplied_assets"].get("value")
            ),
            "cases_where_asset_is_customer_stated": sum(
                1 for c in cases
                if c["normalized_request"]["R02_supplied_assets"]["provenance"] == "customer_stated"
            ),
            "cases_where_asset_is_experiment_fixture": sum(
                1 for c in cases
                if c["normalized_request"]["R02_supplied_assets"]["provenance"] == "experiment_supplied_fixture"
            ),
            "cases_with_subject_of_operation": sum(
                1 for c in cases if has_asset_role(c, "subject_of_operation")
            ),
            "cases_with_role_unrepresentable_in_grammar": sum(
                1 for c in cases if has_asset_role(c, "unresolved_not_in_grammar_v1")
            ),
        },
        "product_identity_coverage": sum(1 for c in cases if "product_identity" in caps(c)),
        "person_or_character_identity_coverage": sum(
            1 for c in cases if "person_identity" in caps(c)
        ),
        "voice_identity_coverage": sum(
            1 for c in cases if "voice_identity_consistency" in caps(c)
        ),
        "any_identity_coverage": sum(1 for c in cases if caps(c) & identity_caps),
        "exact_text_coverage": sum(1 for c in cases if caps(c) & text_caps),
        "set_level_acceptance_coverage": {
            "cases_with_cardinality_gt_1": sum(
                1 for c in cases
                if isinstance((c["normalized_request"]["R04_deliverable_set"].get("value") or {}).get("cardinality"), int)
                and c["normalized_request"]["R04_deliverable_set"]["value"]["cardinality"] > 1
            ),
            "cases_with_set_level_invariant": sum(
                1 for c in cases
                if (c["normalized_request"]["R04_deliverable_set"].get("value") or {}).get("set_level_invariant")
            ),
            "acceptance_basis_values": dict(collections.Counter(
                c["acceptance_contract"].get("acceptance_basis") for c in cases
            )),
        },
        "speech_coverage": sum(
            1 for c in cases
            if (c["normalized_request"]["R11_speaker_topology"].get("value"))
        ),
        "evaluator_family_dependency_counts": dict(fam),
        "evaluator_families_qualified": 0,
        "hard_blocked_dependencies": sum(
            1 for c in cases for d in c["evaluator_dependencies"] if d.get("hard_blocker")
        ),
        "stage_fit": {
            "stage_c_end_to_end": dict(stage_c),
            "stage_b_compound": dict(stage_b),
            "stage_a_atomic": dict(stage_a),
        },
        "ambiguity_markers_total": sum(
            len(c["normalized_request"]["R17_ambiguity_markers"].get("value") or [])
            for c in cases
        ),
        "cases_with_stated_rejection_criteria": sum(
            1 for c in cases
            if (c["normalized_request"]["R18_acceptance_intent"].get("value") or {}).get("stated_rejection_criteria")
        ),
        "grammar_gaps": [g["id"] for g in bank["grammar_gaps"]["gaps"]],
        "capability_coverage_observations": [
            o["id"] for o in bank["capability_coverage_observations"]["observations"]
        ],
        "comparison_with_existing_banks": {
            "authored_30_count": len(authored),
            "authored_30_operations": authored_ops,
            "authored_30_exact_text_briefs": authored_exact_text,
            "authored_30_language_conditions": dict(collections.Counter(
                r["language_condition"] for r in authored
            )),
            "extension_11_count": len(extension),
            "extension_11_operations": dict(ext_ops),
            "marketplace_18_operations": dict(ops),
        },
        "fixtures_declared": sum(len(c.get("fixture_requirements") or []) for c in cases),
        "fixtures_blocking_runnability": sum(
            1 for c in cases for f in (c.get("fixture_requirements") or [])
            if f.get("blocks_runnable")
        ),
    }

    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
