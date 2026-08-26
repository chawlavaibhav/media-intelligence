#!/usr/bin/env python3
"""Validate the EVAL-007 research outputs. Fails closed.

Checks the things that would quietly invalidate the program:
  * all nine required deliverables exist;
  * the capability audit covers exactly the 36 frozen ids, none invented;
  * every audit classification comes from E7-C's vocabulary;
  * the workflow inventory admits ZERO endpoints and resolves ZERO rows;
  * no source register row claims first-party status without a URL;
  * no threshold or qualification is asserted anywhere in the research set.
"""
import pathlib, re, sys, yaml

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]

REQUIRED = ["BENCHMARK-LANDSCAPE.md", "benchmark-source-register.yaml",
            "CURRENT-WORKFLOW-INVENTORY-2026-08-26.yaml",
            "CAPABILITY-36-EXTERNAL-AUDIT.md", "CONDITION-EVIDENCE-MAP.yaml",
            "EVALUATOR-LANDSCAPE-AND-QUALIFICATION.md",
            "BENCHMARK-v2-PROPOSAL.md", "COST-FORECAST-PROVISIONAL.md",
            "EVAL-007-CONTROLLER-BRIEF.md"]

E7C_VOCAB = {"Externally supported, well scoped",
             "Supported — definition/unit needs refinement",
             "Likely a condition, not a capability",
             "Overlaps another capability",
             "Product-important, weakly evidenced externally",
             "Candidate missing capability"}

FROZEN_36 = [
 "object_count","attribute_binding","spatial_relationship","action_adherence",
 "delivery_format_compliance","exact_text_latin","exact_text_devanagari",
 "typography_legibility","logo_wordmark_fidelity","packaging_brand_colour_fidelity",
 "person_identity","product_identity","reference_conditioning","edit_preservation",
 "anatomy_hands","human_object_contact","human_human_interaction",
 "motion_action_quality","physics_material_appearance","person_stability_in_clip",
 "product_stability_in_clip","text_logo_stability_in_clip",
 "multi_shot_spatial_continuity","spoken_language_correctness",
 "single_speaker_lip_sync","two_speaker_turn_assignment_and_lip_sync",
 "emotional_prosodic_fit","audio_video_synchronisation","proposition_objective_fit",
 "hierarchy_product_as_hero","composition_brand_register",
 "hook_pacing_temporal_hierarchy","reliability_pass_at_k","cost_and_cpao",
 "latency_errors_refusals","reproducibility_repairability"]


def main():
    errors, warn = [], []

    missing = [f for f in REQUIRED if not (HERE / f).exists()]
    if missing:
        errors.append(f"missing deliverables: {missing}")

    # --- source register -----------------------------------------------------
    reg_p = HERE / "benchmark-source-register.yaml"
    reg = yaml.safe_load(reg_p.read_text()) if reg_p.exists() else None
    if not reg or not reg.get("sources"):
        errors.append("source register empty - an empty check is not a passing check")
    else:
        if len(reg["sources"]) != reg.get("sources_recorded"):
            errors.append("source register count disagrees with its own declaration")
        for s in reg["sources"]:
            if not s.get("url"):
                errors.append(f"{s.get('id')}: no URL - a source without a URL is not a source")
            if not s.get("accessed"):
                errors.append(f"{s.get('id')}: no accessed date")
            if not s.get("claim_basis"):
                errors.append(f"{s.get('id')}: no claim_basis - "
                              f"README claims and paper findings must be distinguishable")
        if not reg.get("known_gaps"):
            errors.append("source register declares no gaps; absence of gaps is not credible here")

    # --- capability audit ----------------------------------------------------
    aud_p = HERE / "CAPABILITY-36-EXTERNAL-AUDIT.md"
    if aud_p.exists():
        txt = aud_p.read_text()
        found = re.findall(r"^\*\*`([a-z0-9_]+)`\*\* — (.+)$", txt, re.M)
        ids = [f[0] for f in found]
        miss = [c for c in FROZEN_36 if c not in ids]
        extra = [c for c in ids if c not in FROZEN_36]
        if miss:
            errors.append(f"audit misses {len(miss)} frozen capability id(s): {miss[:5]}")
        if extra:
            errors.append(f"audit contains non-frozen id(s) - scope invention: {extra}")
        if len(ids) != 36:
            errors.append(f"audit covers {len(ids)} capabilities, expected 36")
        bad = sorted({c for _, c in found if c.strip() not in E7C_VOCAB})
        if bad:
            errors.append(f"classification(s) outside E7-C vocabulary: {bad}")

    # --- workflow inventory --------------------------------------------------
    inv_p = HERE / "CURRENT-WORKFLOW-INVENTORY-2026-08-26.yaml"
    if inv_p.exists():
        inv = yaml.safe_load(inv_p.read_text())
        if inv.get("endpoints_admitted") != 0:
            errors.append("inventory admits endpoints; no official evidence was obtained")
        if inv.get("rows_resolved") != 0:
            errors.append("inventory claims resolved rows without official evidence")
        if inv.get("api_calls_made") != 0:
            errors.append("inventory records API calls; none are permitted")
        for c in inv.get("candidates", []):
            if c.get("price") is not None or c.get("model_api_id") is not None:
                errors.append(f"{c.get('vendor')}: a price or model id is populated without "
                              f"official evidence")

    # --- conditions ----------------------------------------------------------
    cond_p = HERE / "CONDITION-EVIDENCE-MAP.yaml"
    if cond_p.exists():
        cond = yaml.safe_load(cond_p.read_text())
        if cond.get("empirically_measured_by_us") != 0:
            errors.append("condition map claims empirical measurement; none was made")
        if not cond.get("planner_decisions_not_conditions"):
            errors.append("condition map does not separate Planner decisions from conditions")
        for c in cond.get("conditions", []):
            if not c.get("evidence_strength"):
                errors.append(f"{c.get('id')}: no evidence_strength")

    # --- nothing may be declared qualified or approved ------------------------
    # Read the SENTENCE, not the substring. "No instrument is qualified" and
    # "an instrument must be qualified before it gates anything" both contain
    # the phrase while asserting the opposite of a qualification - a naive
    # substring match flags exactly the documents that are being careful.
    ASSERTIONS = ("is now qualified", "we have qualified", "has been qualified",
                  "is hereby qualified", "threshold is approved",
                  "thresholds are approved", "we approve ")
    NEGATORS = ("no ", "not ", "never", "must be", "cannot", "before it",
                "would be", "may not", "none ", "zero")
    for f in REQUIRED:
        fp = HERE / f
        if not fp.exists():
            continue
        for sent in re.split(r"(?<=[.!?])\s+", fp.read_text()):
            s = sent.lower()
            for phrase in ASSERTIONS:
                if phrase in s and not any(n in s for n in NEGATORS):
                    errors.append(f"{f}: asserts a qualification/approval - "
                                  f"'{sent.strip()[:90]}'")

    print(f"deliverables present     : {len(REQUIRED)-len(missing)}/{len(REQUIRED)}")
    if reg:
        print(f"sources registered       : {len(reg.get('sources', []))}")
    if aud_p.exists():
        print(f"capabilities audited     : {len(ids)}/36")
    if inv_p.exists():
        print(f"endpoints admitted       : {inv.get('endpoints_admitted')}")
    if cond_p.exists():
        print(f"conditions recorded      : {len(cond.get('conditions', []))}")
        print(f"planner decisions split  : {len(cond.get('planner_decisions_not_conditions', []))}")
    for w in warn:
        print("WARN ", w)
    if errors:
        print(f"\nFAIL - {len(errors)} error(s):")
        for e in errors:
            print("  -", e)
        return 1
    print("\nPASS - research outputs complete, scope unchanged, nothing over-claimed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
