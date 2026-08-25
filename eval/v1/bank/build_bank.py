#!/usr/bin/env python3
"""E4 — build the 100-base-item reusable benchmark bank.

THE POINT OF THIS FILE
----------------------
"Generate once, measure every scientifically valid capability from that same
output." A compound item is one generation that legitimately feeds many
measurements. The bank exists so that later paid waves never regenerate an
asset merely because a second evaluator wants to inspect it.

The measurement fan-out is DERIVED from eval/v1/capability-contract.yaml, not
hand-written here. A compound item in scenario family F can score capability C
if and only if C's contract entry lists F in `compound_reuse` (or lists ALL).
That makes the fan-out auditable and stops it drifting from the contract.

Repeats are NEVER base items. Reuse never turns one asset into two trials.

Usage:
  python3 eval/v1/bank/build_bank.py --build
  python3 eval/v1/bank/build_bank.py --validate
"""
import argparse, csv, json, pathlib, sys, yaml, collections

ROOT = pathlib.Path(__file__).resolve().parents[3]
CONTRACT = ROOT / "eval/v1/capability-contract.yaml"
OUT = ROOT / "eval/v1/bank"

# ---------------------------------------------------------------- frozen spec
# Runbook section 6: 40 atomic + 60 compound = 100 distinct base items.
ATOMIC_TOTAL, COMPOUND_TOTAL = 40, 60

# Runbook's atomic family counts. "Use exactly these unless E1 proves a
# material invalidity and the Controller Brief records it." No invalidity found.
ATOMIC_GROUPS = {
    "exact_text": {
        "count": 10,
        "allocation": {"exact_text_latin": 5, "exact_text_devanagari": 5},
    },
    "count_attribute_spatial": {
        "count": 6,
        "allocation": {"object_count": 2, "attribute_binding": 2,
                       "spatial_relationship": 2},
    },
    "identity_reference_preservation": {
        "count": 6,
        "allocation": {"person_identity": 2, "product_identity": 2,
                       "reference_conditioning": 1, "edit_preservation": 1},
    },
    "anatomy_human_object": {
        "count": 6,
        "allocation": {"anatomy_hands": 3, "human_object_contact": 2,
                       "human_human_interaction": 1},
    },
    "motion_camera_physics": {
        "count": 6,
        "allocation": {"motion_action_quality": 2, "action_adherence": 2,
                       "physics_material_appearance": 2},
    },
    "speech_lipsync_speaker": {
        "count": 6,
        "allocation": {"spoken_language_correctness": 2,
                       "single_speaker_lip_sync": 2,
                       "two_speaker_turn_assignment_and_lip_sync": 1,
                       "audio_video_synchronisation": 1},
    },
}

# Runbook section 6: 10 scenario families x 6 benchmark items.
# These ids match `compound_reuse` in the capability contract exactly.
SCENARIOS = [
    ("typography_led_image", "Typography-led commercial image",
     "image", "A headline-driven static creative where the words carry the message."),
    ("product_packshot", "Product packshot",
     "image", "A single product presented cleanly, as a catalogue or hero shot."),
    ("person_plus_product_static", "Person + product static ad",
     "image", "A model holding, using or presented with the product."),
    ("reference_campaign_edit", "Reference-based campaign edit",
     "editing", "An existing asset edited to a new brief while preserving what must not change."),
    ("product_hero_video", "Product-hero video, external VO or no speech",
     "video", "A 6-20 second product video with no visible speaker."),
    ("actor_plus_product_vo", "Actor + product, external VO, no visible dialogue",
     "video", "A person appears with the product; the voice is added, not spoken on camera."),
    ("one_visible_speaker", "One visible speaker",
     "native_av", "A single person speaking to camera."),
    ("two_person_dialogue", "Two-person dialogue",
     "native_av", "Two visible speakers exchanging turns."),
    ("product_handoff_action", "Product handoff / action sequence",
     "video", "A physical action involving the product, often between two people."),
    ("multi_shot_branded_ad", "Multi-shot branded ad, 6-20 seconds",
     "video", "Several shots cut together into a complete branded ad."),
]

# Difficulty tiers across the 6 items in each scenario family. Deliberately
# weighted toward the middle: level 1 proves the scenario runs at all, level 5
# is where commercial work actually lives.
COMPOUND_TIERS = [1, 2, 3, 3, 4, 5]

# Capabilities designated CRITICAL for the first product. The >=10 coverage
# target applies to these. Chosen because each is a hard routing constraint AND
# a recorded or commercially load-bearing failure mode.
CRITICAL = [
    "exact_text_devanagari", "exact_text_latin", "logo_wordmark_fidelity",
    "person_identity", "product_identity", "reference_conditioning",
    "object_count", "attribute_binding", "spatial_relationship",
    "anatomy_hands", "human_object_contact",
    "person_stability_in_clip", "product_stability_in_clip",
    "text_logo_stability_in_clip", "multi_shot_spatial_continuity",
    "spoken_language_correctness", "single_speaker_lip_sync",
    "two_speaker_turn_assignment_and_lip_sync", "audio_video_synchronisation",
    "delivery_format_compliance",
]


def load_contract():
    doc = yaml.safe_load(CONTRACT.read_text())
    return {d["id"]: d for d in doc["dimensions"]}


def fanout_for_scenario(dims, scenario_id, modality):
    """Capabilities a compound asset in this scenario can VALIDLY score.

    Two gates, both required:
      1. the contract lists this scenario in compound_reuse (or ALL), and
      2. the capability applies to this asset's modality.
    Gate 2 matters: a still image cannot evidence a temporal capability, and
    letting it would be a design defect dressed up as a cheaper test.
    """
    out = []
    for cid, d in dims.items():
        reuse = d.get("compound_reuse") or []
        if reuse != ["ALL"] and scenario_id not in reuse:
            continue
        if d["instrument_family"] != "operational" and modality not in d["modalities"]:
            continue
        out.append(cid)
    return sorted(out)


def build():
    dims = load_contract()
    items = []

    # ------------------------------------------------------------ atomic 40
    n = 0
    for gname, g in ATOMIC_GROUPS.items():
        assert sum(g["allocation"].values()) == g["count"], gname
        for cap, k in g["allocation"].items():
            d = dims[cap]
            ladder = d["difficulty_ladder"]
            modality = d["modalities"][0]
            for j in range(k):
                # Spread items across the ladder rather than clustering at 1.
                lvl = min(len(ladder), 1 + round(j * (len(ladder) - 1) / max(1, k - 1))) if k > 1 else 2
                # Atomic items isolate ONE capability, but still free-ride the
                # zero-cost operational and delivery checks on the same asset.
                free = [c for c, dd in dims.items()
                        if (dd.get("compound_reuse") == ["ALL"] and c != cap)]
                free = [c for c in free
                        if dims[c]["instrument_family"] == "operational"
                        or modality in dims[c]["modalities"]]
                items.append({
                    "item_id": f"atomic-{n:03d}",
                    "class": "atomic",
                    "atomic_group": gname,
                    "primary_capability": cap,
                    "difficulty_level": lvl,
                    "difficulty_observable": ladder[lvl - 1]["observable"],
                    "modality": modality,
                    "observation_unit": d["observation_unit"],
                    "purpose": "causal isolation of a single capability",
                    "measurement_fanout": sorted([cap] + free),
                    "fanout_primary": cap,
                    "fanout_free_riders": sorted(free),
                    "resource_requirement": d["resource_requirement"],
                    "prompt_spec": (
                        f"Isolated probe for {cap} at level {lvl}: "
                        f"{ladder[lvl-1]['observable']}. Plain background, no "
                        f"distractor content, nothing else under test."),
                    "repeats_are_not_base_items": True,
                })
                n += 1

    # ---------------------------------------------------------- compound 60
    m = 0
    for sid, label, modality, blurb in SCENARIOS:
        fan = fanout_for_scenario(dims, sid, modality)
        for tier in COMPOUND_TIERS:
            per_cap = {}
            for c in fan:
                L = len(dims[c]["difficulty_ladder"])
                per_cap[c] = min(tier, L)
            items.append({
                "item_id": f"compound-{m:03d}",
                "class": "compound",
                "scenario_family": sid,
                "scenario_label": label,
                "scenario_description": blurb,
                "difficulty_tier": tier,
                "modality": modality,
                "measurement_fanout": fan,
                "fanout_size": len(fan),
                "fanout_difficulty_by_capability": per_cap,
                "purpose": "one generation scored on every valid capability",
                "regeneration_rule": (
                    "NEVER regenerate this asset because another listed "
                    "capability is being evaluated. One asset, one trial, "
                    "many measurements."),
                "prompt_spec": (
                    f"{label} at tier {tier}. {blurb} Conditions are declared "
                    f"per capability in fanout_difficulty_by_capability."),
                "repeats_are_not_base_items": True,
            })
            m += 1

    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "master-bank-v1.jsonl").open("w") as fh:
        for it in items:
            fh.write(json.dumps(it, sort_keys=True) + "\n")

    # ------------------------------------------------------- fan-out CSV
    with (OUT / "MEASUREMENT-FANOUT.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["item_id", "class", "group_or_scenario", "modality",
                    "difficulty", "fanout_size", "capability", "capability_level"])
        for it in items:
            grp = it.get("atomic_group") or it.get("scenario_family")
            diff = it.get("difficulty_level") or it.get("difficulty_tier")
            lv = it.get("fanout_difficulty_by_capability", {})
            for c in it["measurement_fanout"]:
                w.writerow([it["item_id"], it["class"], grp, it["modality"],
                            diff, len(it["measurement_fanout"]), c,
                            lv.get(c, diff)])
    return items, dims


def coverage(items, dims):
    cov = collections.Counter()
    for it in items:
        for c in it["measurement_fanout"]:
            cov[c] += 1
    return cov


def validate(verbose=True):
    dims = load_contract()
    p = OUT / "master-bank-v1.jsonl"
    if not p.exists():
        print("FAIL: bank not built")
        return 1
    items = [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
    errors = []

    if not items:
        print("FAIL: bank is empty - an empty check is not a passing check")
        return 1

    atomic = [i for i in items if i["class"] == "atomic"]
    compound = [i for i in items if i["class"] == "compound"]
    if len(items) != 100:
        errors.append(f"expected 100 base items, found {len(items)}")
    if len(atomic) != ATOMIC_TOTAL:
        errors.append(f"expected {ATOMIC_TOTAL} atomic, found {len(atomic)}")
    if len(compound) != COMPOUND_TOTAL:
        errors.append(f"expected {COMPOUND_TOTAL} compound, found {len(compound)}")

    ids = [i["item_id"] for i in items]
    if len(set(ids)) != len(ids):
        errors.append("duplicate item ids")

    # atomic group counts must match the frozen allocation
    got = collections.Counter(i["atomic_group"] for i in atomic)
    for g, spec in ATOMIC_GROUPS.items():
        if got[g] != spec["count"]:
            errors.append(f"atomic group {g}: expected {spec['count']}, got {got[g]}")

    # scenario families: exactly 10 x 6
    sc = collections.Counter(i["scenario_family"] for i in compound)
    if len(sc) != 10:
        errors.append(f"expected 10 scenario families, found {len(sc)}")
    for s, c in sc.items():
        if c != 6:
            errors.append(f"scenario {s}: expected 6 items, got {c}")

    # every compound item must declare a fan-out, and it must be VALID
    for it in compound:
        if not it["measurement_fanout"]:
            errors.append(f"{it['item_id']}: empty measurement fanout")
        for c in it["measurement_fanout"]:
            d = dims.get(c)
            if d is None:
                errors.append(f"{it['item_id']}: unknown capability {c}")
                continue
            reuse = d["compound_reuse"]
            if reuse != ["ALL"] and it["scenario_family"] not in reuse:
                errors.append(f"{it['item_id']}: {c} not valid for scenario "
                              f"{it['scenario_family']} per contract")
            if d["instrument_family"] != "operational" and \
                    it["modality"] not in d["modalities"]:
                errors.append(f"{it['item_id']}: {c} not applicable to modality "
                              f"{it['modality']}")

    cov = coverage(items, dims)
    under = {c: cov.get(c, 0) for c in CRITICAL if cov.get(c, 0) < 10}

    if verbose:
        print(f"base items            : {len(items)} "
              f"({len(atomic)} atomic + {len(compound)} compound)")
        print(f"scenario families     : {len(sc)} x 6")
        print(f"capabilities covered  : {len(cov)}/36")
        print(f"total measurements    : {sum(cov.values())}")
        print(f"measurement multiplier: {sum(cov.values())/len(items):.1f}x "
              f"(measurements per generated asset)")
        print(f"critical caps >=10    : {len(CRITICAL)-len(under)}/{len(CRITICAL)}")
        if under:
            print("  under-covered criticals (denominator recorded, not padded):")
            for c, v in sorted(under.items(), key=lambda kv: kv[1]):
                print(f"    {c}: {v}")
        uncovered = [c for c in dims if cov.get(c, 0) == 0]
        if uncovered:
            print(f"  capabilities with 0 opportunities: {uncovered}")

    if errors:
        print(f"\nFAIL - {len(errors)} error(s):")
        for e in errors[:20]:
            print("  -", e)
        return 1
    print("\nPASS - bank structure valid, every fan-out entry authorised by the contract.")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--validate", action="store_true")
    a = ap.parse_args()
    if a.build:
        its, dims = build()
        print(f"built {len(its)} base items")
    sys.exit(validate())
