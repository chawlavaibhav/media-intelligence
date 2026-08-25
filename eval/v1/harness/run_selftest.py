#!/usr/bin/env python3
"""E5 verification: the six demonstrations the runbook requires, plus negative
controls on the harness itself.

Everything here uses dummy/synthetic fixtures. No network. No paid call.
No empirical Registry row is produced, and the harness refuses to produce one.

Run: python3 eval/v1/harness/run_selftest.py
"""
from __future__ import annotations
import json, pathlib, shutil, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from harness import Harness, Instrument, HarnessError
import adapters as A

ROOT = HERE.parents[2]
BANK = ROOT / "eval/v1/bank/master-bank-v1.jsonl"
results = []


def check(name, condition, detail=""):
    results.append((name, bool(condition), detail))
    print(f"  [{'PASS' if condition else 'FAIL'}] {name}"
          + (f"\n         {detail}" if detail else ""))
    return bool(condition)


def expect_raises(name, fn, must_contain=None):
    try:
        fn()
    except HarnessError as e:
        ok = (must_contain is None) or (must_contain.lower() in str(e).lower())
        return check(name, ok, f"raised: {str(e)[:120]}")
    except Exception as e:
        return check(name, False, f"wrong exception type {type(e).__name__}: {e}")
    return check(name, False, "NO exception raised - harness did not fail closed")


def load_bank():
    return [json.loads(l) for l in BANK.read_text().splitlines() if l.strip()]


def build_instruments(h):
    """Three narrow evaluators + one deterministic + one deliberately unqualified."""
    h.register_instrument(Instrument(
        "dummy-ocr", "0.0.1", {"prompt": "transcribe", "normalisation": "NFC"},
        qualification_status="screened_not_qualified",
        capabilities={"exact_text_latin", "exact_text_devanagari",
                      "text_logo_stability_in_clip"},
        cost_per_call=0.001,
        fn=A.make_evaluator("ocr", {"char_substitute", "text_mutates_mid_clip"})))
    h.register_instrument(Instrument(
        "dummy-vlm", "0.0.1", {"prompt": "structured-visual"},
        qualification_status="screened_not_qualified",
        capabilities={"person_identity", "product_identity", "anatomy_hands",
                      "physics_material_appearance", "logo_wordmark_fidelity",
                      "attribute_binding", "human_object_contact",
                      "typography_legibility", "hierarchy_product_as_hero",
                      "composition_brand_register", "proposition_objective_fit",
                      "reference_conditioning", "human_human_interaction",
                      "spatial_relationship", "object_count"},
        cost_per_call=0.010,
        fn=A.make_evaluator("vlm", {"extra_finger", "different_person", "shape_drift"})))
    h.register_instrument(Instrument(
        "dummy-temporal", "0.0.1", {"sample_rate_fps": 4},
        qualification_status="screened_not_qualified",
        capabilities={"person_stability_in_clip", "product_stability_in_clip",
                      "text_logo_stability_in_clip", "motion_action_quality",
                      "multi_shot_spatial_continuity", "action_adherence",
                      "hook_pacing_temporal_hierarchy"},
        observation_unit="sequence", cost_per_call=0.012,
        fn=A.make_evaluator("temporal", {"face_drift", "text_mutates_mid_clip"})))
    # Deterministic: a file probe needs no calibration, so it MAY write rows.
    h.register_instrument(Instrument(
        "file-probe", "1.0.0", {"checks": ["duration", "aspect", "resolution"]},
        qualification_status="deterministic",
        capabilities={"delivery_format_compliance"}, cost_per_call=0.0,
        fn=A.make_evaluator("probe", {"aspect_mismatch"})))
    return h


def main():
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="e5-"))
    bank = load_bank()
    by_id = {i["item_id"]: i for i in bank}
    # a video compound item with a large fan-out
    video_item = next(i for i in bank if i["class"] == "compound"
                      and i["modality"] == "video" and len(i["measurement_fanout"]) > 6)

    print("=" * 74)
    print("E5 HARNESS VERIFICATION — dummy/synthetic fixtures only, zero spend")
    print("=" * 74)

    # ---------------------------------------------------------------- DEMO 1
    print("\nDEMO 1 — one generated asset scored by several evaluators, no regeneration")
    h = build_instruments(Harness(tmp / "d1"))
    cfg = {"provider": "DUMMY", "model": "dummy-video-1", "version": "0.0.1",
           "endpoint": "text-to-video", "workflow": "single_call", "lane": "video",
           "seed_policy": "fixed", "seed": 42, "unit_price": 1.00,
           "inject_defects": ["face_drift", "text_mutates_mid_clip"]}
    prov = h.generate(video_item, cfg, A.dummy_generator)
    routing = {}
    for cap in video_item["measurement_fanout"]:
        for iid, instr in h.instruments.items():
            if cap in instr.capabilities:
                routing[cap] = iid
                break
    ms = h.fan_out(prov.asset_id, video_item, routing)
    instruments_used = {m.instrument_id for m in ms}
    check("one generation call only", len(h.attempts) == 1,
          f"attempts={len(h.attempts)}, assets={len(h.provenance)}")
    check(">=3 distinct evaluators scored the SAME asset",
          len(instruments_used) >= 3,
          f"{len(ms)} measurements from {len(instruments_used)} instruments "
          f"({', '.join(sorted(instruments_used))}) on 1 asset")
    check("all measurements point at that one asset",
          all(m.asset_id == prov.asset_id for m in ms))
    om = h.operational_metrics()
    check("still exactly one trial asset", om["trial_assets"] == 1,
          f"measurements_per_trial_asset = {om['measurements_per_trial_asset']}x")

    co = h.failure_cooccurrence()
    check("multiple defects recorded on one output",
          co["multi_defect_assets"] >= 1,
          f"co-occurrence: {list(co['co_occurrence'].keys())}")

    # ---------------------------------------------------------------- DEMO 2
    print("\nDEMO 2 — a retry creates a NEW attempt and never replaces the output")
    first_attempt, first_asset = prov.attempt_id, prov.asset_id
    first_hash = prov.output_sha256
    prov2 = h.generate(video_item, {**cfg, "inject_defects": []},
                       A.dummy_generator, retry_of=first_attempt,
                       retry_reason="reliability_repeat")
    check("new attempt id", prov2.attempt_id != first_attempt,
          f"{first_attempt} -> {prov2.attempt_id}")
    check("new asset id (original NOT overwritten)", prov2.asset_id != first_asset)
    check("original asset still on disk with its original hash",
          pathlib.Path(h.provenance[first_asset].output_path).exists()
          and h.provenance[first_asset].output_sha256 == first_hash)
    check("retry linkage recorded",
          prov2.retry_of_attempt_id == first_attempt
          and prov2.retry_reason == "reliability_repeat")
    check("each asset has exactly one provenance record",
          len(h.provenance) == len({p.asset_id for p in h.provenance.values()}))

    # ---------------------------------------------------------------- DEMO 3
    print("\nDEMO 3 — frames sampled from a clip keep the parent trial id")
    frames = h.derive_frames(first_asset, 4)
    check("4 child assets created", len(frames) == 4)
    check("every frame names its parent",
          all(f.parent_asset_id == first_asset for f in frames))
    check("every frame resolves to the parent TRIAL",
          all(h.trial_asset_id(f.asset_id) == first_asset for f in frames))
    om2 = h.operational_metrics()
    check("4 frames added 0 new trials", om2["trial_assets"] == 2,
          f"assets={len(h.provenance)} but trial_assets={om2['trial_assets']} "
          f"(2 generations, 4 derived frames). Frames from one clip are ONE trial.")
    check("frame extraction cost nothing",
          all(f.cost_generation == 0.0 for f in frames))

    # ---------------------------------------------------------------- DEMO 4
    print("\nDEMO 4 — the duplicate-regeneration guard fires")
    expect_raises("regenerating the same item+config is REFUSED",
                  lambda: h.generate(video_item, cfg, A.dummy_generator),
                  "duplicate generation refused")
    check("guard did not create a stray attempt", len(h.attempts) == 2,
          f"attempts still {len(h.attempts)}")
    n_before = len(h.measurements)
    extra = h.measure(first_asset, video_item["measurement_fanout"][0],
                      routing[video_item["measurement_fanout"][0]], video_item)
    check("but re-measuring the SAME asset is allowed and free",
          len(h.measurements) == n_before + 1 and len(h.attempts) == 2,
          "evaluating another capability needs no new generation - the point of fan-out")

    # ---------------------------------------------------------------- DEMO 5
    print("\nDEMO 5 — an unqualified instrument cannot write a Registry row")
    text_ms = [m for m in h.measurements if m.instrument_id == "dummy-vlm"
               and m.verdict in ("pass", "fail")]
    expect_raises("unqualified instrument REFUSED at the Registry boundary",
                  lambda: h.write_registry_row(
                      "person_identity", "dummy-vlm", text_ms,
                      {"resolution": "1080x1920"}, 2, 1),
                  "registry write refused")
    check("dummy-vlm is correctly marked not-writable",
          not h.instruments["dummy-vlm"].registry_writable,
          f"status={h.instruments['dummy-vlm'].qualification_status}")
    check("file-probe IS writable (deterministic needs no calibration)",
          h.instruments["file-probe"].registry_writable)
    probe_ms = [m for m in h.measurements if m.instrument_id == "file-probe"
                and m.verdict in ("pass", "fail")]
    if probe_ms:
        expect_raises("even a QUALIFIED instrument is refused on synthetic data",
                      lambda: h.write_registry_row(
                          "delivery_format_compliance", "file-probe", probe_ms,
                          {"aspect": "9:16"}, 1, 1),
                      "synthetic")
    expect_raises("empty measurement set is REFUSED",
                  lambda: h.write_registry_row(
                      "delivery_format_compliance", "file-probe", [],
                      {"aspect": "9:16"}, 1, 1),
                  "no measurements")
    check("registry still empty", len(h.registry_rows) == 0)

    # ------------------------------------------------- absence + negative ctl
    print("\nDEMO 5b — absence reasons and harness negative controls")
    h.register_instrument(Instrument(
        "na-eval", "0.0.1", {}, qualification_status="screened_not_qualified",
        capabilities={"object_count"}, fn=A.not_applicable_evaluator))
    h.register_instrument(Instrument(
        "bad-eval", "0.0.1", {}, qualification_status="screened_not_qualified",
        capabilities={"object_count"}, fn=A.badly_behaved_evaluator))
    h.register_instrument(Instrument(
        "bogus-eval", "0.0.1", {}, qualification_status="screened_not_qualified",
        capabilities={"object_count"}, fn=A.bogus_verdict_evaluator))
    img_item = next(i for i in bank if i["class"] == "compound"
                    and i["modality"] == "image" and "object_count" in i["measurement_fanout"])
    p_img = h.generate(img_item, {**cfg, "model": "dummy-image-1",
                                  "endpoint": "text-to-image", "lane": "image",
                                  "inject_defects": []}, A.dummy_generator)
    m_na = h.measure(p_img.asset_id, "object_count", "na-eval", img_item)
    check("'absent' carries a machine-readable reason",
          m_na.verdict == "absent" and m_na.absence_reason == "not_applicable",
          f"reason={m_na.absence_reason}")
    expect_raises("'absent' with NO reason is REFUSED",
                  lambda: h.measure(p_img.asset_id, "object_count", "bad-eval", img_item),
                  "needs a reason")
    expect_raises("verdict outside the vocabulary is REFUSED",
                  lambda: h.measure(p_img.asset_id, "object_count", "bogus-eval", img_item),
                  "unknown verdict")
    # Pick a capability dummy-vlm genuinely owns but which this item's fan-out
    # does NOT list, so the fan-out guard is the one under test.
    off_fanout = sorted(h.instruments["dummy-vlm"].capabilities
                        - set(img_item["measurement_fanout"]))
    check("found a capability owned by the instrument but outside the fan-out",
          bool(off_fanout), f"using '{off_fanout[0] if off_fanout else None}'")
    if off_fanout:
        expect_raises("scoring a capability outside the item's fan-out is REFUSED",
                      lambda: h.measure(p_img.asset_id, off_fanout[0],
                                        "dummy-vlm", img_item),
                      "not in item")
    expect_raises("using an instrument outside its judgement family is REFUSED",
                  lambda: h.measure(p_img.asset_id, "object_count", "dummy-ocr", img_item),
                  "not specified for capability")

    print("\nDEMO 5c — a refused generation yields 'absent/refused', not a fail")
    h2 = build_instruments(Harness(tmp / "d2"))
    pr = h2.generate(img_item, {**cfg, "lane": "image"}, A.refusing_generator)
    m_ref = h2.measure(pr.asset_id or "", "object_count", "dummy-vlm", img_item) \
        if pr.asset_id else None
    if m_ref is None:
        # refused attempts produce no asset; record the attempt-level fact instead
        om3 = h2.operational_metrics()
        check("refusal recorded as a refusal, not a failed capability",
              om3["refusals"] == 1 and om3["assets_produced"] == 0,
              f"refusals={om3['refusals']}, error_classes={om3['error_classes']}")

    # ---------------------------------------------------------------- DEMO 6
    print("\nDEMO 6 — the Registry schema validates and starts EMPTY")
    reg = ROOT / "eval/registry/registry-v1.jsonl"
    schema = ROOT / "eval/registry/SCHEMA-v1-draft.yaml"
    check("registry file exists", reg.exists())
    content = reg.read_text() if reg.exists() else "x"
    rows = [l for l in content.splitlines() if l.strip() and not l.startswith("#")]
    check("registry contains ZERO empirical rows", len(rows) == 0,
          f"{len(rows)} data rows")
    check("registry schema file exists", schema.exists())
    if schema.exists():
        import yaml
        s = yaml.safe_load(schema.read_text())
        check("schema parses and declares zero entries",
              s.get("empirical_entries") == 0,
              f"status={s.get('status')}")

    # ---------------------------------------------------------------- output
    outdir = ROOT / "eval/v1/harness/out-selftest"
    if outdir.exists():
        shutil.rmtree(outdir)
    h.dump(outdir)
    man = [json.loads(l) for l in (outdir / "artifact-manifest.jsonl").read_text().splitlines() if l.strip()]
    required = ["trial_asset_id", "attempt_id", "item_id", "provider", "model",
                "version", "endpoint", "workflow", "config_hash", "config_path",
                "input_hashes", "reference_hashes", "seed", "requested_at",
                "completed_at", "output_sha256", "cost_generation", "api_status",
                "error_class", "evaluator_result_refs"]
    missing = [f for f in required if any(f not in r for r in man)]
    print("\nSTORAGE HANDOFF")
    check("artifact manifest carries every required field", not missing,
          f"{len(man)} asset rows, {len(required)} required fields, missing={missing or 'none'}")
    om = h.operational_metrics()
    check("no routing score or weight was computed",
          om["routing_scores_computed"] == 0)
    check("generation and evaluator costs are separate lines",
          "cost_generation_total" in om and "cost_evaluator_total" in om,
          f"gen={om['cost_generation_total']} eval={om['cost_evaluator_total']}")

    print("\n" + "=" * 74)
    passed = sum(1 for _, ok, _ in results if ok)
    print(f"RESULT: {passed}/{len(results)} checks passed")
    print(f"Registry rows created: {len(h.registry_rows)}  (must be 0)")
    print(f"Paid API calls made:   0")
    print("=" * 74)
    shutil.rmtree(tmp, ignore_errors=True)
    return 0 if passed == len(results) and not h.registry_rows else 1


if __name__ == "__main__":
    sys.exit(main())
