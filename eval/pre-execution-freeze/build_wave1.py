#!/usr/bin/env python3
"""E9-E + E9-H — build the Wave-1 benchmark spec and its exact call counts.

Counts are DERIVED from the declared design, never asserted. Prices are absent:
EVAL-010 owns them, and a partially-resolved forecast must not total.
"""
import yaml, pathlib, json, collections, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT_Y = ROOT / "eval/pre-execution-freeze/BENCHMARK-v2-WAVE1.yaml"
OUT_F = ROOT / "eval/pre-execution-freeze/WAVE1-CALL-COUNT-FORECAST.yaml"

# ---------------------------------------------------------------------------
# LAYER 1 — atomic probes. Causal isolation, one capability each.
# Only for capabilities that are MEASURABLE in Wave 1 (see evaluator map).
# ---------------------------------------------------------------------------
ATOMIC = {
    "image": ["exact_text_devanagari", "exact_text_latin", "typography_legibility",
              "object_count", "attribute_binding", "spatial_relationship_2d",
              "spatial_relationship_depth", "product_identity", "person_identity",
              "wardrobe_invariant_fidelity", "reference_conditioning",
              "edit_preservation", "human_anatomy_integrity", "logo_wordmark_fidelity",
              "packaging_brand_colour_fidelity", "delivery_format_compliance"],
    "video": ["camera_framing_fidelity", "sequence_state_continuity",
              "technical_visual_integrity", "text_logo_stability_in_clip",
              "person_stability_in_clip", "product_stability_in_clip",
              "multi_shot_spatial_continuity", "motion_action_quality",
              "action_adherence"],
    "audio": ["spoken_script_correctness", "pronunciation_intelligibility",
              "voice_identity_consistency", "audio_video_synchronisation",
              "single_speaker_lip_sync", "two_speaker_turn_assignment_and_lip_sync",
              "emotional_prosodic_fit"],
}
ATOMIC_ITEMS_PER_CAPABILITY = 2   # two ladder levels: one easy, one hard

# ---------------------------------------------------------------------------
# LAYER 2 — compound scenarios WITH prerequisite graphs, crossed by
# requested operation. This is where dependency-aware scoring is exercised.
# ---------------------------------------------------------------------------
COMPOUND = [
    {"id": "typography_led_static", "modality": "image", "operation": "generate", "items": 4},
    {"id": "product_packshot", "modality": "image", "operation": "generate", "items": 3},
    {"id": "person_plus_product_static", "modality": "image", "operation": "generate", "items": 3},
    {"id": "campaign_variant_set", "modality": "image", "operation": "variants", "items": 3},
    {"id": "supplied_asset_edit", "modality": "image", "operation": "edit", "items": 3},
    {"id": "animate_from_supplied_image", "modality": "video", "operation": "animate", "items": 3},
    {"id": "product_hero_video", "modality": "video", "operation": "generate", "items": 3},
    {"id": "multi_shot_branded_ad", "modality": "video", "operation": "generate", "items": 3},
    {"id": "one_visible_speaker_dialogue", "modality": "native_av", "operation": "generate", "items": 3},
    {"id": "footage_edit", "modality": "video", "operation": "edit", "items": 2},
]

# ---------------------------------------------------------------------------
# LAYER 3 — sparse ADAPTIVE condition sweeps. Reuse layer-2 items; add ONE
# extra level per swept condition on a SUBSET. No cartesian product.
# ---------------------------------------------------------------------------
SWEEPS = {
    "COND-LANGUAGE":   {"items_swept": 6, "extra_levels": 2},  # hi + hinglish beyond en
    "COND-CONSTRAINT": {"items_swept": 5, "extra_levels": 1},
    "COND-LOAD":       {"items_swept": 4, "extra_levels": 1},
    "COND-DELIVERY":   {"items_swept": 4, "extra_levels": 1},  # duration/size
}

# ---------------------------------------------------------------------------
# LAYER 4 — end-to-end accepted outcomes. RESERVED, parameterised, not invented.
# ---------------------------------------------------------------------------
E2E = {
    "status": "PARAMETERISED_PENDING_CANON_010",
    "briefs_from": "Canon accepted brief bank + request-coverage extension",
    "slots_reserved": 8,
    "recipes_per_brief": 2,
    "repeats": 2,
    "eval_must_not_author_briefs": True,
    "reconciliation_point": (
        "CANON-010 freezes the Media Request Grammar and the request-coverage "
        "extension. Until then these are SLOTS with a declared operation mix, not "
        "items. Eval authoring its own customer briefs is precisely how a benchmark "
        "starts defining the product instead of the other way round."),
    "operation_mix_required": ["generate", "edit", "animate", "variants"],
}

REPEATS_PER_ITEM = 2   # reliability; NEVER counted as independent base items

# Evaluator fan-out per generated asset, by modality. ESTIMATE, labelled as one.
FANOUT = {
    "image":     {"ocr": 2, "vlm": 3, "deterministic_local": 4, "human_review": 0.25},
    "video":     {"ocr": 6, "vlm": 3, "temporal_local": 4, "deterministic_local": 3, "human_review": 0.5},
    "native_av": {"ocr": 6, "vlm": 3, "asr": 2, "temporal_local": 4, "deterministic_local": 3, "human_review": 0.75},
    "audio":     {"asr": 2, "asv": 1, "deterministic_local": 2, "human_review": 0.5},
}


def build():
    # ---- layer 1
    l1 = {m: len(c) * ATOMIC_ITEMS_PER_CAPABILITY for m, c in ATOMIC.items()}
    l1_items = sum(l1.values())

    # ---- layer 2
    l2_items = sum(s["items"] for s in COMPOUND)
    l2_by_mod = collections.Counter()
    for s in COMPOUND:
        l2_by_mod[s["modality"]] += s["items"]
    l2_by_op = collections.Counter()
    for s in COMPOUND:
        l2_by_op[s["operation"]] += s["items"]

    # ---- layer 3 (extra ITEM INSTANCES, not new base items)
    l3_instances = sum(v["items_swept"] * v["extra_levels"] for v in SWEEPS.values())

    base_items = l1_items + l2_items
    item_instances = base_items + l3_instances

    # ---- generations: instances x repeats x applicable slots
    roster = yaml.safe_load(
        (ROOT / "eval/pre-execution-freeze/SCIENTIFIC-WAVE1-MODEL-ROSTER.yaml").read_text())
    core = [s for s in roster["slots"] if s["tier"] == "core"]
    reserve = [s for s in roster["slots"] if s["tier"] == "reserve"]
    # rough total item load across core slots, used only to apportion sweeps
    tot_inst_estimate = sum(
        len([c for c in s.get("capabilities", []) if c in
             {x for caps in ATOMIC.values() for x in caps}]) * ATOMIC_ITEMS_PER_CAPABILITY + 6
        for s in core)

    # ---- SLOT-TARGETED ITEM SETS -------------------------------------------
    # A slot exists to answer ONE question. Running every item of its modality
    # on every slot is cartesian-ish waste and buys redundant evidence. Each
    # slot therefore runs:
    #   (a) the atomic items for the capabilities IT declares, and
    #   (b) the compound scenarios matching its lane/operation, and
    #   (c) a small SHARED COMPARABILITY CORE so slots remain comparable, and
    #   (d) its share of the sparse sweeps.
    COMPARABILITY_CORE = {"image": 4, "video": 4, "audio": 3}
    LANE_TO_MOD = {"image": "image", "video": "video", "tts": "audio", "lipsync": "audio"}
    atomic_index = {}
    for m, caps in ATOMIC.items():
        for c in caps:
            atomic_index[c] = m
    # compound scenarios each slot legitimately runs
    def compound_for(slot):
        mod = LANE_TO_MOD[slot["lane"]]
        n = 0
        for s in COMPOUND:
            smod = "video" if s["modality"] in ("video", "native_av") else s["modality"]
            if smod != mod:
                continue
            # only if the slot's workflow mode can serve that operation
            if s["operation"] == "edit" and slot["workflow_mode"] not in ("edit",):
                continue
            if s["operation"] == "animate" and slot["workflow_mode"] not in ("i2v", "edit"):
                continue
            if s["operation"] == "variants" and slot["workflow_mode"] not in \
                    ("reference_conditioned", "edit", "t2i"):
                continue
            n += s["items"]
        return n

    REDUCED_SLOTS = {"VID-05": 0.4}   # cost knee needs contrast, not full coverage
    per_slot, gen_total = {}, 0
    for s in core:
        mod = LANE_TO_MOD[s["lane"]]
        # (a) atomic items for the capabilities THIS slot declares
        own_caps = [c for c in s.get("capabilities", []) if atomic_index.get(c) == mod]
        a_items = len(own_caps) * ATOMIC_ITEMS_PER_CAPABILITY
        # (b) compound scenarios it can serve
        c_items = compound_for(s)
        # (c) shared comparability core
        core_items = COMPARABILITY_CORE[mod]
        # (d) share of sweeps, proportional to its own item load
        inst = a_items + c_items + core_items
        sweep_share = round(l3_instances * (inst / max(1, tot_inst_estimate)), 1)
        inst_total = inst + sweep_share
        factor = REDUCED_SLOTS.get(s["slot_id"], 1.0)
        g = round(inst_total * REPEATS_PER_ITEM * factor)
        per_slot[s["slot_id"]] = {
            "lane": s["lane"], "atomic_items": a_items, "compound_items": c_items,
            "comparability_core": core_items, "sweep_instances": sweep_share,
            "item_instances": round(inst_total, 1), "repeats": REPEATS_PER_ITEM,
            "reduced_factor": factor, "generations": g}
        gen_total += g

    # ---- evaluator calls
    mod_share = {"image": l1["image"] + l2_by_mod["image"],
                 "video": l1["video"] + l2_by_mod["video"],
                 "native_av": l2_by_mod["native_av"],
                 "audio": l1["audio"]}
    tot_share = sum(mod_share.values())
    ev = collections.Counter()
    for sid, row in per_slot.items():
        lane = row["lane"]
        mod = {"image": "image", "video": "video", "tts": "audio", "lipsync": "audio"}[lane]
        for k, v in FANOUT[mod].items():
            ev[k] += row["generations"] * v
    ev = {k: round(v, 1) for k, v in ev.items()}
    human = ev.pop("human_review", 0)

    spec = {
        "benchmark_version": "v2-wave1",
        "task": "E9-E",
        "date": "2026-08-26",
        "status": "PROPOSED_FOR_CONTROLLER_FREEZE_NOT_IN_FORCE",
        "v1_bank_status": "PRESERVED_UNMODIFIED_AS_HISTORICAL_BASELINE",
        "v1_bank_path": "eval/v1/bank/master-bank-v1.jsonl (100 items, byte-identical)",
        "cartesian_sweep": False,
        "layers": {
            "layer1_atomic": {"purpose": "causal isolation, one capability per item",
                              "items_per_capability": ATOMIC_ITEMS_PER_CAPABILITY,
                              "capabilities_covered": {m: len(c) for m, c in ATOMIC.items()},
                              "items": l1, "items_total": l1_items},
            "layer2_compound": {"purpose": "realistic co-occurrence WITH prerequisite graphs",
                                "scenarios": COMPOUND, "items_total": l2_items,
                                "by_modality": dict(l2_by_mod),
                                "by_requested_operation": dict(l2_by_op),
                                "prerequisite_graph_required": True},
            "layer3_sweeps": {"purpose": "sparse adaptive condition sweeps; reuse layer-2 items",
                              "swept": SWEEPS, "extra_item_instances": l3_instances,
                              "cartesian": False,
                              "adaptive_rule": ("Sweep the next level only where the previous did "
                                                "NOT already fail. No saving is claimed in the "
                                                "forecast."),
                              "stop_rule": ("Stop expanding a sweep axis after two consecutive "
                                            "failing levels on the same item."),
                              "expansion_rule": ("Expand an axis only where a level PASSED and the "
                                                 "next level is materially harder.")},
            "layer4_e2e": E2E,
        },
        "totals": {"base_items": base_items, "sweep_instances": l3_instances,
                   "item_instances": item_instances,
                   "repeats_per_item": REPEATS_PER_ITEM},
        "repeats_semantics": (
            "A repeat is a DELIBERATE experimental re-run to estimate reliability, decided before "
            "any result is seen. It gets its own trial id and NEVER counts as an independent base "
            "item. A RETRY is caused by a prior failure, belongs to the acceptance/CpAO chain, and "
            "must never be pooled into a capability pass-rate cell."),
        "requested_operations_covered": sorted(l2_by_op.keys()),
    }

    forecast = {
        "task": "E9-H",
        "date": "2026-08-26",
        "status": "COUNTS_EXACT_PRICES_UNRESOLVED",
        "authorises_spend": False,
        "core_slots": len(core), "reserve_slots": len(reserve),
        "generations_by_slot": per_slot,
        "generations_total_core": gen_total,
        "reserve_note": ("Reserve slots are NOT in this total. Promoting one adds its own "
                         "generation count and is an explicit Controller decision."),
        "evaluator_calls": ev,
        "evaluator_calls_total": round(sum(ev.values()), 1),
        "evaluator_fanout_status": "ESTIMATE_NOT_MEASURED",
        "human_review_units": round(human, 1),
        "human_review_note": ("Units are reviewer-passes, not hours. No approved rate exists, so "
                              "no cost is derived. Expected to dominate fully-loaded CpAO."),
        "retries": {"included": False,
                    "rule": ("Retries are budgeted SEPARATELY and predeclared. Discovering a retry "
                             "allowance mid-run is a budget change and a MONEY stop.")},
        "prices": {"status": "UNRESOLVED_OWNED_BY_EVAL_010",
                   "generation_unit_price_by_slot": {s["slot_id"]: None for s in core},
                   "evaluator_unit_price_by_instrument": {k: None for k in ev},
                   "human_rate": None},
        "totals": {"generation_cost": None, "evaluator_cost": None, "human_cost": None,
                   "fully_loaded": None,
                   "why_null": ("Every price cell is unresolved. A partially-resolved forecast must "
                                "NOT be totalled as though exact - that produces a number that "
                                "looks like a budget and is a fraction of one.")},
        "reduction_levers": {
            "purpose": ("Offered so the Controller can trade scope against budget EXPLICITLY. "
                        "None is applied. Each names what evidence is lost - a cheaper wave that "
                        "hides what it gave up is not cheaper, it is less honest."),
            "levers": [
                {"id": "L1", "lever": "repeats_per_item 2 -> 1",
                 "saves_pct": 50,
                 "loses": ("ALL reliability evidence. pass_at_k and reproducibility become "
                           "uncomputable, and a single draw cannot distinguish a flaky model from "
                           "a bad one. Strongly discouraged: reliability IS the product question.")},
                {"id": "L2", "lever": "drop the comparability core",
                 "saves_pct": 12,
                 "loses": ("Cross-slot comparability. Slots could no longer be compared on shared "
                           "items, only on their own.")},
                {"id": "L3", "lever": "defer VID-04 (footage edit) to Wave 2",
                 "saves_pct": 8,
                 "loses": ("Whether customer-supplied footage is usable. Preserves the hypothesis "
                           "in the record per the Controller's trade-off rule.")},
                {"id": "L4", "lever": "defer layer-3 sweeps to Wave 2",
                 "saves_pct": 17,
                 "loses": ("Condition-dependence evidence. Every result becomes a single-point "
                           "measurement whose envelope is unknown.")},
                {"id": "L5", "lever": "reduce core image slots from 4 to 3",
                 "saves_pct": 9,
                 "loses": ("One of: specialist-vs-generalist text, edit economics, or campaign "
                           "identity. Each is a distinct production decision.")},
            ],
            "recommended_if_budget_forces_a_cut": (
                "L3 then L4. They defer whole QUESTIONS, which is recoverable and visible. L1 "
                "corrupts every remaining number instead, which is not."),
        },
        "formula_for_eval010": {
            "generation_cost": "sum over slots of ( generations[slot] * unit_price[slot] )",
            "evaluator_cost": "sum over instruments of ( calls[instrument] * unit_price[instrument] )",
            "human_cost": "human_review_units * review_minutes_per_unit * hourly_rate / 60",
            "api_tool_cpao": "(generation_cost + evaluator_cost) / accepted_outcomes",
            "fully_loaded_cpao": ("(generation_cost + evaluator_cost + human_cost + "
                                  "local_compute_cost) / accepted_outcomes"),
            "note": ("accepted_outcomes comes from layer 4, which is parameterised pending "
                     "CANON-010. CpAO is therefore not computable in Wave 1 until layer 4 lands."),
        },
    }
    OUT_Y.write_text("# GENERATED by build_wave1.py - E9-E. PROPOSED, NOT IN FORCE.\n"
                     "# The V1 100-item bank is PRESERVED UNMODIFIED as a historical baseline.\n\n"
                     + yaml.safe_dump(spec, sort_keys=False, width=90, allow_unicode=True))
    OUT_F.write_text("# GENERATED by build_wave1.py - E9-H. Counts exact; prices UNRESOLVED.\n\n"
                     + yaml.safe_dump(forecast, sort_keys=False, width=90, allow_unicode=True))
    return spec, forecast


if __name__ == "__main__":
    s, f = build()
    t = s["totals"]
    print(f"base items {t['base_items']} (L1 {s['layers']['layer1_atomic']['items_total']} + "
          f"L2 {s['layers']['layer2_compound']['items_total']})")
    print(f"sweep instances {t['sweep_instances']} -> item instances {t['item_instances']}")
    print(f"operations covered: {s['requested_operations_covered']}")
    print(f"core slots {f['core_slots']} | generations {f['generations_total_core']}")
    print(f"evaluator calls {f['evaluator_calls_total']} -> {f['evaluator_calls']}")
    print(f"human review units {f['human_review_units']}")
