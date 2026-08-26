#!/usr/bin/env python3
"""Validate eval/v1/capability-contract.yaml against the frozen Controller scope.

Fails closed. An empty check is not a passing check: if zero dimensions are
loaded, that is an error, not a success (Eval HANDOFF lesson).

Run:  python3 eval/v1/validate_capability_contract.py
"""
import sys, yaml, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "eval/v1/capability-contract.yaml"

# The 36 ids frozen by eval/tasks/EVAL-V1-OVERNIGHT-PROGRAM.md section 1.
# Transcribed from the runbook. Eval may refine definitions, never this list.
FROZEN_36 = [
    # A constraint fidelity (5)
    "object_count", "attribute_binding", "spatial_relationship",
    "action_adherence", "delivery_format_compliance",
    # B text & brand (5)
    "exact_text_latin", "exact_text_devanagari", "typography_legibility",
    "logo_wordmark_fidelity", "packaging_brand_colour_fidelity",
    # C identity & references (4)
    "person_identity", "product_identity", "reference_conditioning",
    "edit_preservation",
    # D human & physical realism (5)
    "anatomy_hands", "human_object_contact", "human_human_interaction",
    "motion_action_quality", "physics_material_appearance",
    # E temporal / continuity (4)
    "person_stability_in_clip", "product_stability_in_clip",
    "text_logo_stability_in_clip", "multi_shot_spatial_continuity",
    # F speech / audio (5)
    "spoken_language_correctness", "single_speaker_lip_sync",
    "two_speaker_turn_assignment_and_lip_sync", "emotional_prosodic_fit",
    "audio_video_synchronisation",
    # G commercial / creative (4)
    "proposition_objective_fit", "hierarchy_product_as_hero",
    "composition_brand_register", "hook_pacing_temporal_hierarchy",
    # H operational (4)
    "reliability_pass_at_k", "cost_and_cpao", "latency_errors_refusals",
    "reproducibility_repairability",
]

MANDATORY = [
    "id", "family", "name_plain", "definition", "inside", "outside",
    "modalities", "observation_unit", "observation_span_detail",
    "atomic_probe", "compound_reuse", "difficulty_ladder",
    "instrument_family", "human_verifier", "benchmark_material_readiness",
    "result_form", "failure_vocabulary", "registry_conditions",
    "routing_use", "instrument_readiness", "readiness_note",
]
# Mandatory as KEYS but may be null.
MANDATORY_NULLABLE = ["secondary_instrument", "production_envelope_note"]

# Canon's vocabulary, adopted unchanged. SPEC-04-operational-bindings.md:105
CANON_UNITS = {"frame", "shot", "shot_pair", "sequence", "whole_asset",
               "asset_set_over_time"}
# --- E-C1: two INDEPENDENT readiness axes, never one conflated scalar ------
# Can the mechanism be trusted?
INSTRUMENT_READINESS = {"deterministic_ready", "qualified", "provisional",
                        "blocked_pending_qualification", "unmeasurable"}
# Do we hold the material to exercise it under the intended conditions?
BENCHMARK_MATERIAL_READINESS = {"available", "constructed_by_eval", "partial",
                                "missing", "no_external_stimulus_required"}
RESULT_FORMS = {"exact_pass_fail", "structured_categorical",
                "pairwise_preference", "human_hybrid_score",
                "operational_metric"}
ROUTING = {"hard_constraint", "descriptive_only"}
INSTRUMENT_FAMILIES = {1, 2, 3, 4, 5, 6, "operational"}
MODALITIES = {"image", "video", "native_av", "lipsync", "tts", "editing"}


def main():
    errors, warnings = [], []
    doc = yaml.safe_load(CONTRACT.read_text())
    dims = doc.get("dimensions") or []

    # An empty check is not a passing check.
    if not dims:
        print("FAIL: contract contains zero dimensions.")
        return 1

    ids = [d.get("id") for d in dims]

    # --- scope integrity: exactly the frozen 36, no additions, no removals ---
    missing = [i for i in FROZEN_36 if i not in ids]
    extra = [i for i in ids if i not in FROZEN_36]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if missing:
        errors.append(f"missing frozen capability ids: {missing}")
    if extra:
        errors.append(f"capability ids NOT in the frozen 36 (scope change): {extra}")
    if dupes:
        errors.append(f"duplicate capability ids: {dupes}")
    if len(dims) != 36:
        errors.append(f"expected 36 dimensions, found {len(dims)}")

    # --- per-dimension field integrity ---
    for d in dims:
        did = d.get("id", "<no id>")
        for f in MANDATORY:
            if f not in d:
                errors.append(f"{did}: missing mandatory field '{f}'")
            elif d[f] in (None, "", [], {}):
                errors.append(f"{did}: mandatory field '{f}' is empty")
        for f in MANDATORY_NULLABLE:
            if f not in d:
                errors.append(f"{did}: missing mandatory (nullable) key '{f}'")

        if d.get("observation_unit") not in CANON_UNITS:
            errors.append(
                f"{did}: observation_unit '{d.get('observation_unit')}' is not in "
                f"Canon's SPEC-04 vocabulary {sorted(CANON_UNITS)}")
        if d.get("instrument_readiness") not in INSTRUMENT_READINESS:
            errors.append(f"{did}: bad instrument_readiness "
                          f"'{d.get('instrument_readiness')}'")
        if d.get("benchmark_material_readiness") not in BENCHMARK_MATERIAL_READINESS:
            errors.append(f"{did}: bad benchmark_material_readiness "
                          f"'{d.get('benchmark_material_readiness')}'")
        if d.get("result_form") not in RESULT_FORMS:
            errors.append(f"{did}: bad result_form '{d.get('result_form')}'")
        if d.get("routing_use") not in ROUTING:
            errors.append(f"{did}: bad routing_use '{d.get('routing_use')}'")
        if d.get("instrument_family") not in INSTRUMENT_FAMILIES:
            errors.append(f"{did}: bad instrument_family '{d.get('instrument_family')}'")
        for m in d.get("modalities") or []:
            if m not in MODALITIES:
                errors.append(f"{did}: unknown modality '{m}'")

        ladder = d.get("difficulty_ladder") or []
        if not 3 <= len(ladder) <= 5:
            errors.append(f"{did}: difficulty ladder has {len(ladder)} levels, need 3-5")
        for i, lvl in enumerate(ladder, 1):
            if lvl.get("level") != i:
                errors.append(f"{did}: ladder level {i} out of order (got {lvl.get('level')})")
            if not lvl.get("observable"):
                errors.append(f"{did}: ladder level {i} has no observable change")

        # Every dimension must reach a measurement path or an explicit state.
        if d.get("instrument_readiness") == "unmeasurable" and \
                len(str(d.get("readiness_note", ""))) < 40:
            errors.append(f"{did}: unmeasurable requires a substantive readiness_note")

        # E-C1: nothing may claim a qualification that does not exist. No
        # instrument family holds a qualification record, so `qualified` and
        # `provisional` are reserved and must not appear.
        if d.get("instrument_readiness") in ("qualified", "provisional"):
            errors.append(
                f"{did}: instrument_readiness '{d.get('instrument_readiness')}' "
                f"claims a qualification record that does not exist. Zero "
                f"instrument families are qualified.")

        # E-C1: a model-based instrument is never `deterministic_ready`. A
        # detector or a VLM is a model, not a deterministic oracle.
        if d.get("instrument_readiness") == "deterministic_ready" and \
                d.get("instrument_family") in (1, 3, 4, 5, 6):
            errors.append(
                f"{did}: instrument_family {d.get('instrument_family')} is a "
                f"model-based evaluator and cannot be deterministic_ready.")

        # E-C1: the axes are INDEPENDENT. Material state must never be inferred
        # from instrument state, so no combination is forbidden - but a
        # deterministic mechanism with absent material MUST say so, because that
        # is precisely the case the old single scalar could not express.
        if d.get("instrument_readiness") == "deterministic_ready" and \
                d.get("benchmark_material_readiness") in ("missing", "partial") and \
                not d.get("production_envelope_note"):
            errors.append(
                f"{did}: deterministic mechanism with "
                f"'{d.get('benchmark_material_readiness')}' material requires a "
                f"production_envelope_note saying so.")

        # Family G is descriptive only, by contract.
        if str(d.get("family", "")).startswith("G_") and d.get("routing_use") != "descriptive_only":
            errors.append(f"{did}: family G must be descriptive_only")

        # Operational dimensions must not require their own generations.
        if d.get("instrument_family") == "operational" and \
                "None of its own" not in str(d.get("atomic_probe", "")):
            warnings.append(f"{did}: operational dimension should derive from existing trials")

    print(f"dimensions loaded            : {len(dims)}")
    print(f"frozen scope ids matched     : {len(FROZEN_36) - len(missing)}/36")
    print(f"mandatory fields per dim     : {len(MANDATORY) + len(MANDATORY_NULLABLE)}")
    import collections as _c
    ir = _c.Counter(d.get("instrument_readiness") for d in dims)
    mr = _c.Counter(d.get("benchmark_material_readiness") for d in dims)
    # sort by str(): a dimension missing the field yields None, and the summary
    # must still PRINT so the collected errors are visible. Crashing here would
    # hide the very errors this validator exists to report.
    print("instrument_readiness         : "
          + ", ".join(f"{k}={v}" for k, v in sorted(ir.items(), key=lambda kv: str(kv[0]))))
    print("benchmark_material_readiness : "
          + ", ".join(f"{k}={v}" for k, v in sorted(mr.items(), key=lambda kv: str(kv[0]))))
    print(f"both-axes-ready (measurable) : "
          f"{sum(1 for d in dims if d.get('instrument_readiness') in ('deterministic_ready','qualified') and d.get('benchmark_material_readiness') in ('available','constructed_by_eval','no_external_stimulus_required'))}")
    print(f"production_envelope_notes    : {sum(1 for d in dims if d.get('production_envelope_note'))}")
    print(f"hard_constraint / descriptive: "
          f"{sum(1 for d in dims if d.get('routing_use')=='hard_constraint')} / "
          f"{sum(1 for d in dims if d.get('routing_use')=='descriptive_only')}")
    for w in warnings:
        print(f"WARN  {w}")
    if errors:
        print(f"\nFAIL — {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("\nPASS — 36/36 dimensions, no missing mandatory field, scope unchanged.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
