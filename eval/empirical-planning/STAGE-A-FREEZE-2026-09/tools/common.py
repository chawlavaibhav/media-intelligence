# Shared constructors for case records.
FAMILIES = ["COND-DELIVERY", "COND-LOAD", "COND-REFERENCE", "COND-INTERACTION", "COND-MOTION",
            "COND-CONSTRAINT", "COND-WORKFLOW", "COND-SEQUENCE", "COND-LANGUAGE", "COND-INPUT",
            "COND-PROVENANCE", "COND-OPERATION", "COND-SCALE"]

NOTICE = ("CANON COVERAGE GAP: no accepted Canon source covers audio production. Canon has no doctrine "
          "for this cell — no defaults, no checks. Proceed on the brief alone, state this gap in "
          "FAILURE_PREVENTION, and do not attribute audio decisions to Canon. Closing the gap requires "
          "new source ingestion only the Controller can authorise.")

LANG_TOPO = {
    "en": dict(language="en", script_system="latin", is_code_mixed=False),
    "hi": dict(language="hi", script_system="devanagari", is_code_mixed=False),
    "hg": dict(language="hi-en (Hinglish)", script_system="latin_with_devanagari", is_code_mixed=True),
}

def conds(case, *, delivery, load, reference=None, interaction=None, motion=None, constraint,
          workflow_modes, sequence=None, language, inp=None, operation, scale=None, ref_prov="none"):
    """Build all 13 families. Missing optional families are recorded as not_applicable."""
    lang = language
    return {
        "COND-DELIVERY": delivery,
        "COND-LOAD": load,
        "COND-REFERENCE": reference or dict(reference_type="none", reference_count=0, reference_view_diversity="not_applicable", reference_quality_class="not_applicable", decoy_present=False),
        "COND-INTERACTION": interaction or "not_applicable",
        "COND-MOTION": motion or "not_applicable",
        "COND-CONSTRAINT": constraint,
        "COND-WORKFLOW": dict(workflow_mode_per_route_arm=workflow_modes, who_chose_workflow_mode="benchmark_fixed",
                              seed_fields="SEED-POLICY.yaml (policy unset)"),
        "COND-SEQUENCE": sequence or dict(n_shots=1, shot_boundaries_declared=False, is_multi_shot=False, set_size=1, set_acceptance_basis="per_deliverable"),
        "COND-LANGUAGE": lang,
        "COND-INPUT": inp or dict(input_source_class="none", input_resolution="not_applicable", input_degradation_class="not_applicable"),
        "COND-PROVENANCE": dict(requested_operation=operation, workflow_mode="as COND-WORKFLOW.workflow_mode_per_route_arm", who_chose_workflow_mode="benchmark_fixed", reference_selection_provenance=ref_prov),
        "COND-OPERATION": operation,
        "COND-SCALE": scale or dict(deliverable_count=1, is_variant_set=False, set_acceptance_basis="per_deliverable"),
    }

def rt(key, arm, tranche, params, quantity, repeats=2, quantity_unit=None, exception=None, item_id=None, screen_status=None):
    d = dict(route_key=key, arm=arm, tranche=tranche, params=params, quantity=quantity, repeats=repeats)
    if screen_status: d["screen_status"] = screen_status
    if quantity_unit: d["quantity_unit"] = quantity_unit
    if exception: d["repeats_exception"] = exception
    if item_id: d["item_id"] = item_id
    return d

IMG_PARAMS = dict(aspect=None, resolution="~1 MP (1024-class)", audio="not_applicable", refs=0)
def imgp(aspect, refs=0, **kw):
    p = dict(IMG_PARAMS); p.update(aspect=aspect, refs=refs); p.update(kw); return p
def vidp(aspect="9:16", duration_s=6, resolution="720p", audio="on", refs=0, **kw):
    p = dict(aspect=aspect, duration_s=duration_s, resolution=resolution, audio=audio, refs=refs); p.update(kw); return p

def prov(**kw):
    """field -> provenance (string or dict with rationale for system_derived)."""
    return kw

def sd(rationale):
    return dict(value="system_derived", rationale=rationale)
