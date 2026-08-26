#!/usr/bin/env python3
"""E9-A — build Capability Contract v2 from V1 via an EXPLICIT transform.

WHY A TRANSFORM AND NOT A HAND-WRITTEN FILE. The mechanical gate says V1
capabilities may not disappear without explicit mapping. If v2 were hand-authored
that guarantee would rest on care. Here every v2 row is DERIVED from a declared
disposition on a V1 id, so a missing mapping is impossible by construction and
the validator can prove it.

V1 IS NOT MODIFIED. eval/v1/capability-contract.yaml is read only.
"""
import yaml, pathlib, collections, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
V1 = ROOT / "eval/v1/capability-contract.yaml"
OUT = ROOT / "eval/pre-execution-freeze/CAPABILITY-CONTRACT-v2.yaml"

# ---------------------------------------------------------------------------
# DISPOSITIONS. Every one of the 36 V1 ids must appear exactly once.
#   unchanged      carried into v2 with the same id and meaning
#   refined        same id, definition/condition tightened (no count change)
#   renamed        new id, same capability
#   split          becomes 2+ v2 ids
#   absorbed       folded into another capability + a condition
#   dormant        exists in v2 but cannot be measured until a mechanism exists
# ---------------------------------------------------------------------------
DISPOSITIONS = {
 # ---- Family A ----
 "object_count": ("unchanged", None, "Externally supported (GenEval, T2I-CompBench). No change."),
 "attribute_binding": ("unchanged", None, "Three of T2I-CompBench's six categories. No change."),
 "spatial_relationship": ("split", ["spatial_relationship_2d", "spatial_relationship_depth"],
   "T2I-CompBench evaluates 2D and 3D spatial relations SEPARATELY and with different judges. "
   "V1's own contract already stated depth ordering 'is NOT decidable from 2D boxes' - the split "
   "was documented and then not made. A 2D relation is deterministic given boxes; a depth "
   "relation is not. Different instrument, different qualification, different gate."),
 "action_adherence": ("unchanged", None, "VBench human_action; VBench-2.0 motion order. No change."),
 "delivery_format_compliance": ("refined", None,
   "Unchanged in meaning. Refined only to state its DUAL ROLE explicitly: the requested format is "
   "a CONDITION of every other measurement and simultaneously the subject of this capability."),
 # ---- Family B ----
 "exact_text_latin": ("unchanged", None, "Pack does not exist but the capability is well formed."),
 "exact_text_devanagari": ("unchanged", None,
   "96-item validated battery exists. Envelope limit preserved: it perturbs REAL characters and "
   "cannot produce malformed generated glyphs."),
 "typography_legibility": ("refined", None,
   "Controller-directed: legibility is now EXPLICITLY conditioned on delivery size. Previously the "
   "delivery size lived inside the prose definition, which made two legibility results silently "
   "incomparable. delivery_size becomes a REQUIRED condition."),
 "logo_wordmark_fidelity": ("unchanged", None,
   "No external benchmark found for mark fidelity under perspective/curvature. Remains "
   "required_but_no_calibrated_instrument."),
 "packaging_brand_colour_fidelity": ("refined", None,
   "Controller-directed: brand-colour tolerance is a DECLARED measurement condition and threshold, "
   "not generic categorical-colour evidence. External colour benchmarks test 'is it red', which is "
   "a different and easier judgement than matching a declared brand value within tolerance."),
 # ---- Family C ----
 "person_identity": ("split", ["person_identity", "wardrobe_invariant_fidelity"],
   "Controller-directed: declared wardrobe/clothing invariants must be VISIBLE rather than "
   "silently mixed with face identity. VBench-2.0 independently separates Human Identity from "
   "Human Clothes. The production consequence differs: a right face in wrong wardrobe is often "
   "repairable by re-prompting; a wrong face needs a different reference. One verdict cannot "
   "carry both."),
 "product_identity": ("unchanged", None,
   "DreamBench covers this directly. Cross-asset scope handled by observation unit, not a new id."),
 "reference_conditioning": ("refined", None,
   "STYLE-REFERENCE BOUNDARY RESOLVED HERE. Style reference is NOT a new capability: it is this "
   "capability measured with reference_type=style. The failure - 'the supplied reference did not "
   "control the output' - is identical in kind; only the reference type differs, and a condition "
   "represents that cleanly. Adding a capability would duplicate the mechanism."),
 "edit_preservation": ("unchanged", None, "Deterministic masked diff against our own input."),
 # ---- Family D ----
 "anatomy_hands": ("renamed", ["human_anatomy_integrity"],
   "Controller-directed rename/broaden. V1's own failure vocabulary already covered extra_limb, "
   "joint_inversion and facial_feature_misplaced - the NAME was narrower than the capability and "
   "invited under-testing of everything that is not a hand. Hand-specific diagnostics are "
   "PRESERVED as a required defect sub-vocabulary, not lost in the broadening."),
 "human_object_contact": ("unchanged", None, "No external benchmark; commercially central."),
 "human_human_interaction": ("unchanged", None, "VBench-2.0 Human Interaction."),
 "motion_action_quality": ("refined", None,
   "Refined to REQUIRE motion load as a recorded condition. VBench separates dynamic_degree from "
   "motion_smoothness because a near-static clip scores perfectly on smoothness - without motion "
   "load recorded, a model that produces almost no motion looks like one that produces excellent "
   "motion."),
 "physics_material_appearance": ("refined", None,
   "Scope deliberately bounded DOWNWARD. VBench-2.0's physics group (mechanics, thermotics) is a "
   "research frontier; this product needs commercial plausibility for 6-20s media, not physical "
   "correctness. Multi-view consistency is extracted into sequence_state_continuity instead."),
 # ---- Family E ----
 "person_stability_in_clip": ("unchanged", None, "VBench subject_consistency."),
 "product_stability_in_clip": ("unchanged", None, "Same, applied to objects."),
 "text_logo_stability_in_clip": ("unchanged", None,
   "Our own observed failure (Devanagari drifting within a clip) is stronger evidence than "
   "anything external here."),
 "multi_shot_spatial_continuity": ("refined", None,
   "Kept as SPATIAL continuity only, deliberately narrowed. Its V1 level-5 ladder example "
   "smuggled in product STATE continuity, which its name excludes. That case now belongs to the "
   "new sequence_state_continuity capability, so this id becomes honest rather than overloaded."),
 # ---- Family F ----
 "spoken_language_correctness": ("split", ["spoken_script_correctness", "pronunciation_intelligibility"],
   "Controller-directed. This is the founding Devanagari trap in a different medium: a robust ASR "
   "NORMALISES a mispronunciation into the correct word, exactly as the vision checker silently "
   "corrected a misspelling. Word correctness is machine-comparable; pronunciation acceptability "
   "needs a first-language listener. One instrument cannot answer both, so one capability must "
   "not claim to."),
 "single_speaker_lip_sync": ("unchanged", None,
   "Capability is right; the standard instrument (SyncNet LSE-C/LSE-D) is contested and must be "
   "qualified rather than adopted."),
 "two_speaker_turn_assignment_and_lip_sync": ("unchanged", None,
   "No external benchmark covers turn assignment across two visible speakers."),
 "emotional_prosodic_fit": ("refined", None,
   "Refined toward DISCRIMINATION - can the requested register be told apart and correctly "
   "identified. TTSDS shows prosody has measurable correlates, so this need not stay purely "
   "preference-shaped."),
 "audio_video_synchronisation": ("unchanged", None,
   "Distinct from lip-sync in the literature, matching our separation."),
 # ---- Family G ----
 "proposition_objective_fit": ("unchanged", None, "descriptive_only preserved."),
 "hierarchy_product_as_hero": ("unchanged", None, "descriptive_only preserved."),
 "composition_brand_register": ("unchanged", None, "descriptive_only preserved."),
 "hook_pacing_temporal_hierarchy": ("unchanged", None, "descriptive_only preserved."),
 # ---- Family H ----
 "reliability_pass_at_k": ("unchanged", None, "Counting rule unchanged: confidence on base items."),
 "cost_and_cpao": ("refined", None,
   "Refined to carry the Controller's TWO CpAO views: api_tool_cpao (diagnostic) and "
   "fully_loaded_cpao (primary business metric, including human review time in the operational "
   "path). V1 had a single cost view."),
 "latency_errors_refusals": ("unchanged", None, "Operational; ours to own."),
 "reproducibility_repairability": ("split", ["reproducibility", "repairability"],
   "Controller-directed. Repeat agreement is measurable now from repeats we already budget. "
   "REPAIR requires a repair loop that DOES NOT EXIST, and repair attempts are additional "
   "generations. V1 flagged the split in an envelope note; v2 makes it structural. repairability "
   "is DORMANT."),
}

# New capabilities. Each must justify why an existing capability + condition
# CANNOT represent the failure - that is the admission bar.
ADDITIONS = {
 "camera_framing_fidelity": dict(
   family="A_constraint_fidelity", unit="sequence", routing="hard_constraint",
   why_not_representable=(
     "action_adherence asks whether the SUBJECT did what was asked. A camera instruction is about "
     "the OBSERVER, not the subject: a push-in can be absent while the subject action is perfect, "
     "and no existing capability's verdict changes. No condition can express it either, because a "
     "condition records circumstances, not whether an instruction was honoured."),
   external="VBench-2.0 names Camera Motion as its own controllable dimension; providers expose "
            "camera/motion controls as first-class API parameters."),
 "sequence_state_continuity": dict(
   family="E_temporal_continuity", unit="shot_pair", routing="hard_constraint",
   why_not_representable=(
     "multi_shot_spatial_continuity covers geometry and screen direction. State continuity is "
     "ORDERED and causal - the box is open in shot 2 BECAUSE it was opened in shot 1 - and a "
     "spatially perfect pair can be state-inconsistent. V1 already asked its spatial capability to "
     "carry a state example at level 5, which is the clearest possible evidence that one id was "
     "doing two jobs."),
   external="VBench-2.0 Motion Order Understanding and Multi-View Consistency."),
 "technical_visual_integrity": dict(
   family="D_human_physical_realism", unit="sequence", routing="hard_constraint",
   why_not_representable=(
     "Flicker, transient corruption, warping and sudden softness are not identity drift (the "
     "subject is still the same person), not motion quality (the motion may be smooth) and not "
     "anatomy (the body is correct). Every existing capability can pass on an asset a customer "
     "would reject on sight. Nothing in V1's 36 has a home for it."),
   external="VBench dedicates temporal_flickering, motion_smoothness and imaging_quality to this "
            "space - 3 of its 16 dimensions."),
 "voice_identity_consistency": dict(
   family="F_speech_audio", unit="asset_set_over_time", routing="hard_constraint",
   why_not_representable=(
     "The audio analogue of person_identity, and genuinely absent. spoken_script_correctness "
     "checks WHAT was said; pronunciation_intelligibility checks HOW clearly; emotional_prosodic_fit "
     "checks register. None asks whether it is the SAME VOICE across a campaign - a brand voice "
     "that changes between assets is a commercial failure every one of those three would pass."),
   external="TTS evaluation measures speaker similarity via automatic speaker verification (ASV) "
            "as an instrument distinct from intelligibility (ASR-WER)."),
}

# Concepts deliberately NOT made capabilities.
NOT_CAPABILITIES = {
 "style_reference_fidelity": (
   "RESOLVED INTO reference_conditioning with reference_type=style. The failure is identical in "
   "kind - the supplied reference did not control the output - and only the reference type "
   "differs. A condition represents that cleanly, so the admission bar is not met."),
 "cross_asset_person_or_product_identity": (
   "RESOLVED BY OBSERVATION SCOPE. person_identity and product_identity already use "
   "asset_set_over_time. Cross-asset is a SCOPE of the same capability, not a different failure. "
   "Controller preferred extending existing identity capabilities and no distinct failure was "
   "found that scope cannot represent."),
 "campaign_variant_set_consistency": (
   "DEFERRED AS AN OUTCOME-LEVEL CONCEPT, not a capability. It is a property of a DELIVERABLE SET "
   "against an acceptance basis, which lives at outcome acceptance rather than per-asset "
   "measurement. Controller directed that its instrument and final boundary be frozen WITH the "
   "request-coverage extension. Recorded here so it is not mistaken for solved or forgotten; "
   "reconciliation point is CANON-010."),
}
print("transform spec loaded:", len(DISPOSITIONS), "dispositions,",
      len(ADDITIONS), "additions,", len(NOT_CAPABILITIES), "explicitly not capabilities")


# ---------------------------------------------------------------------------
def build():
    v1doc = yaml.safe_load(V1.read_text())
    v1 = {d["id"]: d for d in v1doc["dimensions"]}
    missing = [i for i in v1 if i not in DISPOSITIONS]
    extra = [i for i in DISPOSITIONS if i not in v1]
    if missing:
        raise SystemExit(f"BUILD ABORTED: {len(missing)} V1 id(s) have no disposition: {missing}")
    if extra:
        raise SystemExit(f"BUILD ABORTED: disposition for unknown id(s): {extra}")

    dims, mapping = [], []
    for cid, src in v1.items():
        kind, targets, rationale = DISPOSITIONS[cid]
        if kind in ("unchanged", "refined"):
            new_ids = [cid]
        elif kind in ("renamed", "split"):
            new_ids = targets
        else:
            raise SystemExit(f"unknown disposition kind {kind}")
        for n, nid in enumerate(new_ids):
            d = dict(src)
            d["id"] = nid
            d["v1_origin"] = cid
            d["v2_disposition"] = kind
            d["v2_rationale"] = rationale
            if kind == "split":
                d["split_sibling"] = [x for x in new_ids if x != nid]
            if nid == "repairability":
                d["status"] = "dormant"
                d["dormant_reason"] = (
                    "No repair loop exists. Repair attempts are additional generations that must "
                    "be budgeted explicitly, not smuggled in under generate-once. Measurable only "
                    "once a repair loop is built.")
            else:
                d["status"] = "active"
            dims.append(d)
        mapping.append({"v1_id": cid, "disposition": kind, "v2_ids": new_ids,
                        "rationale": rationale})

    for nid, meta in ADDITIONS.items():
        dims.append({
            "id": nid, "family": meta["family"], "observation_unit": meta["unit"],
            "routing_use": meta["routing"], "v1_origin": None,
            "v2_disposition": "added", "status": "active",
            "admission_justification": meta["why_not_representable"],
            "external_evidence": meta["external"],
            # inherited contract fields, marked as needing specification
            "instrument_readiness": "blocked_pending_qualification",
            "benchmark_material_readiness": "missing",
            "definition_status": "SPECIFIED_IN_V2_PROPOSAL_NOT_YET_FULLY_AUTHORED",
        })

    active = [d for d in dims if d["status"] == "active"]
    doc = {
        "contract_version": "v2-proposal",
        "date": "2026-08-26",
        "task": "EVAL-009 / E9-A",
        "status": "PROPOSED_FOR_CONTROLLER_FREEZE_NOT_IN_FORCE",
        "supersedes": None,
        "v1_source": "eval/v1/capability-contract.yaml (36 capabilities, UNMODIFIED)",
        "v1_preserved_verbatim": True,
        "counts": {
            "v1_capabilities": len(v1),
            "v2_capabilities_total": len(dims),
            "v2_active": len(active),
            "v2_dormant": len(dims) - len(active),
            "added": len(ADDITIONS),
            "from_splits": sum(len(m["v2_ids"]) - 1 for m in mapping if m["disposition"] == "split"),
            "renamed": sum(1 for m in mapping if m["disposition"] == "renamed"),
            "refined": sum(1 for m in mapping if m["disposition"] == "refined"),
            "unchanged": sum(1 for m in mapping if m["disposition"] == "unchanged"),
        },
        "no_target_count_was_aimed_at": (
            "The count is an OUTPUT of the Controller-approved dispositions, not an input. Nothing "
            "was added to reach a number and nothing was dropped to stay under one."),
        "admission_bar_for_new_capabilities": (
            "A new capability is admitted ONLY where existing capability + condition + observation "
            "scope cannot represent the failure cleanly. Three candidate concepts were REJECTED "
            "under this bar and are recorded in not_capabilities."),
        "not_capabilities": NOT_CAPABILITIES,
        "v1_to_v2_mapping": mapping,
        "dimensions": dims,
    }
    OUT.write_text(
        "# ===========================================================================\n"
        "# Capability Contract v2 - PROPOSAL (E9-A)\n"
        "# ===========================================================================\n"
        "# GENERATED from eval/v1/capability-contract.yaml by build_capability_v2.py.\n"
        "# V1 IS NOT MODIFIED. Every V1 id carries an explicit disposition, so a\n"
        "# capability cannot vanish silently - the build aborts if one lacks a mapping.\n"
        "# STATUS: PROPOSED FOR CONTROLLER FREEZE. NOT IN FORCE.\n"
        "# ===========================================================================\n\n"
        + yaml.safe_dump(doc, sort_keys=False, width=90, allow_unicode=True))
    return doc


if __name__ == "__main__":
    d = build()
    c = d["counts"]
    print(f"V1 {c['v1_capabilities']} -> V2 {c['v2_capabilities_total']} "
          f"({c['v2_active']} active, {c['v2_dormant']} dormant)")
    print(f"  unchanged {c['unchanged']} | refined {c['refined']} | renamed {c['renamed']} "
          f"| +{c['from_splits']} from splits | +{c['added']} added")
    print(f"  explicitly NOT capabilities: {len(d['not_capabilities'])}")
