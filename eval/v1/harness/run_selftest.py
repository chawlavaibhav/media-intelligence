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
           "endpoint": "text-to-video", "workflow": "single_call",
           "lane": "general_video", "media_kind": "video",
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
    print("\nDEMO 2 — an experimental REPEAT creates a new attempt, never a replacement")
    first_attempt, first_asset = prov.attempt_id, prov.asset_id
    first_hash = prov.output_sha256
    prov2 = h.generate(video_item, {**cfg, "inject_defects": []},
                       A.dummy_generator, repeat_of=first_attempt, repeat_index=1)
    check("new attempt id", prov2.attempt_id != first_attempt,
          f"{first_attempt} -> {prov2.attempt_id}")
    check("new asset id (original NOT overwritten)", prov2.asset_id != first_asset)
    check("original asset still on disk with its original hash",
          pathlib.Path(h.provenance[first_asset].output_path).exists()
          and h.provenance[first_asset].output_sha256 == first_hash)
    check("repeat linkage recorded as a REPEAT",
          prov2.repeat_of_attempt_id == first_attempt and prov2.repeat_index == 1
          and prov2.is_experimental_repeat())
    check("a repeat is NOT a retry", not prov2.is_production_retry()
          and prov2.retry_of_attempt_id is None)
    check("each asset has exactly one provenance record",
          len(h.provenance) == len({p.asset_id for p in h.provenance.values()}))

    # ---------------------------------------------------------------- E-C4
    print("\nDEMO 2b — E-C4: repeat and retry are structurally separate")
    hR = build_instruments(Harness(tmp / "d_ec4"))
    base = hR.generate(video_item, cfg, A.dummy_generator)
    rep = hR.generate(video_item, cfg, A.dummy_generator,
                      repeat_of=base.attempt_id, repeat_index=1)
    ret = hR.generate(video_item, cfg, A.dummy_generator,
                      retry_of=base.attempt_id, retry_reason="rejected_by_reviewer")
    om4 = hR.operational_metrics()
    check("a repeat is counted as a repeat, NOT a retry",
          om4["experimental_repeats"] == 1 and rep.is_experimental_repeat()
          and not rep.is_production_retry(),
          f"experimental_repeats={om4['experimental_repeats']}")
    check("a retry is counted as a retry, NOT a repeat",
          om4["production_retries"] == 1 and ret.is_production_retry()
          and not ret.is_experimental_repeat(),
          f"production_retries={om4['production_retries']}")
    check("the two counters are reported separately and never summed",
          "experimental_repeats" in om4 and "production_retries" in om4
          and "retries" not in om4)
    check("EI-C2: a repeat gets its OWN trial id, never the original's",
          rep.trial_id != base.trial_id and rep.trial_id == rep.attempt_id)
    check("EI-C2: a retry gets its OWN trial id, never the original's",
          ret.trial_id != base.trial_id and ret.trial_id == ret.attempt_id)
    check("the CpAO retry chain contains the retry and EXCLUDES the repeat",
          hR.retry_chain(ret.attempt_id) == [base.attempt_id, ret.attempt_id]
          and rep.attempt_id not in hR.retry_chain(ret.attempt_id),
          f"chain={hR.retry_chain(ret.attempt_id)}")
    check("retry-attempt cost and repeat cost are separate, accurately named lines",
          "cost_of_retry_attempts" in om4 and "cost_of_experimental_repeats" in om4,
          f"retry_attempts={om4['cost_of_retry_attempts']} "
          f"repeats={om4['cost_of_experimental_repeats']}")
    check("a COMPLETE chain cost includes the originator, unlike the retry-only line",
          hR.accepted_chain_cost(ret.attempt_id) > om4["cost_of_retry_attempts"],
          f"complete chain={hR.accepted_chain_cost(ret.attempt_id)} vs "
          f"retry-only={om4['cost_of_retry_attempts']} - the old key summed "
          f"only retries and could never have been a chain cost")
    expect_raises("an attempt that is BOTH repeat and retry is REFUSED",
                  lambda: hR.generate(video_item, cfg, A.dummy_generator,
                                      repeat_of=base.attempt_id, repeat_index=2,
                                      retry_of=base.attempt_id,
                                      retry_reason="x"),
                  "cannot be both")
    expect_raises("a retry with no reason is REFUSED",
                  lambda: hR.generate(video_item, cfg, A.dummy_generator,
                                      retry_of=base.attempt_id),
                  "requires retry_reason")
    expect_raises("a repeat with repeat_index 0 is REFUSED",
                  lambda: hR.generate(video_item, cfg, A.dummy_generator,
                                      repeat_of=base.attempt_id, repeat_index=0),
                  "repeat_index >= 1")

    # ---------------------------------------------------------------- DEMO 3
    print("\nDEMO 3 — frames sampled from a clip keep the parent trial id")
    frames = h.derive_frames(first_asset, 4)
    check("4 child assets created", len(frames) == 4)
    check("every frame names its parent",
          all(f.parent_asset_id == first_asset for f in frames))
    check("every frame inherits the parent's TRIAL id (EI-C2)",
          all(f.trial_id == h.provenance[first_asset].trial_id for f in frames))
    check("every frame inherits the parent's ATTEMPT id",
          all(f.attempt_id == h.provenance[first_asset].attempt_id for f in frames))
    om2 = h.operational_metrics()
    check("4 frames added 0 new trials", om2["trials"] == 2,
          f"assets={len(h.provenance)} but trials={om2['trials']} "
          f"(2 calls, 4 derived frames). The trial is the CALL.")
    check("trial_id == attempt_id, one-to-one by construction (EI-C2)",
          all(a.trial_id == a.attempt_id for a in h.attempts.values())
          and len({a.trial_id for a in h.attempts.values()}) == len(h.attempts))
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

    # ---------------------------------------------------------------- E-C6
    print("\nDEMO 5d — E-C6: there is NO synthetic promotion bypass")
    import inspect as _insp
    sig = _insp.signature(Harness.write_registry_row)
    bad = [p for p in sig.parameters
           if "synthetic" in p.lower() or "allow" in p.lower()
           or "force" in p.lower() or "override" in p.lower()]
    check("write_registry_row exposes NO override parameter", not bad,
          f"parameters: {list(sig.parameters)[1:]}")
    src = pathlib.Path(HERE / "harness.py").read_text()
    check("no allow_synthetic anywhere in the harness source",
          "allow_synthetic" not in src)
    # Prove it by attacking it: every call shape must still refuse.
    refused = 0
    for kwargs in ({}, {"repeats_per_item": 1}):
        try:
            h.write_registry_row("delivery_format_compliance", "file-probe",
                                 probe_ms, {"aspect": "9:16"}, 1,
                                 kwargs.get("repeats_per_item", 1))
        except HarnessError:
            refused += 1
        except TypeError:
            refused += 1
    check("no call shape promotes synthetic measurements", refused == 2,
          f"{refused}/2 call shapes refused")
    check("registry STILL empty after bypass attempts", len(h.registry_rows) == 0)

    # ---------------------------------------------------------------- E-C5
    print("\nDEMO 5e — E-C5: a Registry row must be ONE coherent cell")
    hM = build_instruments(Harness(tmp / "d_ec5"))
    # Build two genuinely different cells, then try to pool them.
    cfgA = {**cfg, "model": "model-A", "version": "1.0", "inject_defects": []}
    cfgB = {**cfg, "model": "model-B", "version": "2.0", "inject_defects": []}
    pA = hM.generate(video_item, cfgA, A.dummy_generator)
    pB = hM.generate(video_item, cfgB, A.dummy_generator)
    capX = next(c for c in video_item["measurement_fanout"]
                if c in hM.instruments["dummy-temporal"].capabilities)
    capY = next(c for c in video_item["measurement_fanout"]
                if c in hM.instruments["dummy-ocr"].capabilities and c != capX)
    mA = hM.measure(pA.asset_id, capX, "dummy-temporal", video_item)
    mB = hM.measure(pB.asset_id, capX, "dummy-temporal", video_item)
    mY = hM.measure(pA.asset_id, capY, "dummy-ocr", video_item)
    # make the instrument writable so the refusal proves the CELL check, not
    # the qualification check
    hM.instruments["dummy-temporal"].qualification_status = "deterministic"
    hM.instruments["dummy-ocr"].qualification_status = "deterministic"
    for m in hM.measurements:
        m.synthetic = False          # isolate the homogeneity gate

    expect_raises("mixing TWO MODELS in one cell is REFUSED",
                  lambda: hM.write_registry_row(capX, "dummy-temporal",
                                                [mA, mB], {}, 1, 1),
                  "mixed cell")
    expect_raises("mixing TWO CAPABILITIES in one cell is REFUSED",
                  lambda: hM.write_registry_row(capX, "dummy-temporal",
                                                [mA, mY], {}, 1, 1),
                  "mixed cell")
    expect_raises("mixing TWO INSTRUMENTS in one cell is REFUSED",
                  lambda: hM.write_registry_row(capX, "dummy-temporal",
                                                [mA, mY], {}, 1, 1),
                  "mixed cell")
    expect_raises("a capability that is not the requested one is REFUSED",
                  lambda: hM.write_registry_row(capY, "dummy-temporal",
                                                [mA], {}, 1, 1),
                  "requested capability")
    expect_raises("an instrument that is not the requested one is REFUSED",
                  lambda: hM.write_registry_row(capX, "dummy-ocr",
                                                [mA], {}, 1, 1),
                  "requested instrument")
    expect_raises("a declared condition contradicting the trials is REFUSED",
                  lambda: hM.write_registry_row(capX, "dummy-temporal", [mA],
                                                {"model": "model-Z"}, 1, 1),
                  "contradicts the trials")
    expect_raises("an over-declared repeats_per_item is not trusted",
                  lambda: hM.write_registry_row(capX, "dummy-temporal", [mA],
                                                {}, 1, 0),
                  "repeats_per_item must be")
    # a production retry may not be pooled into a capability pass-rate cell
    pRet = hM.generate(video_item, cfgA, A.dummy_generator,
                       retry_of=pA.attempt_id, retry_reason="rejected")
    mRet = hM.measure(pRet.asset_id, capX, "dummy-temporal", video_item)
    mRet.synthetic = False
    # Isolate the gate under test: mA was measured BEFORE the instrument status
    # was flipped, so without this the HOMOGENEITY gate fires first and the
    # retry gate is never reached. Normalise everything except the retry-ness.
    for m in (mA, mRet):
        m.instrument_qualification_status = "deterministic"
    expect_raises("pooling a production RETRY into a pass-rate cell is REFUSED",
                  lambda: hM.write_registry_row(capX, "dummy-temporal",
                                                [mA, mRet], {}, 1, 2),
                  "production RETRIES")
    check("no Registry row was created by any mixed-cell attempt",
          len(hM.registry_rows) == 0)

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
                                  "endpoint": "text-to-image", "lane": "image", "media_kind": "image",
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

    print("\nDEMO 5c — EI-C5: a provider failure lives on the ATTEMPT, not a measurement")
    h2 = build_instruments(Harness(tmp / "d2"))
    pr = h2.generate(img_item, {**cfg, "lane": "image", "media_kind": "image",
                                "unit_price": 0.40}, A.refusing_generator)
    om3 = h2.operational_metrics()
    check("refusal recorded as a refusal, not a failed capability",
          om3["refusals"] == 1 and om3["assets_produced"] == 0,
          f"refusals={om3['refusals']}, error_classes={om3['error_classes']}")
    check("canonical persistent status is 'refusal', not 'refused'",
          pr.api_status == "refusal")
    check("a refused attempt still has a trial id and a cost_ref",
          bool(pr.trial_id) and bool(pr.cost_ref) and pr.cost_ref in h2.cost_ledger)
    expect_raises("measuring a failed attempt is REFUSED (no double-counting)",
                  lambda: h2.measure(pr.asset_id or "x", "object_count",
                                     "dummy-vlm", img_item),
                  "unknown asset")

    # ---------------------------------------------------------------- EI-C6
    print("\nDEMO 5f — EI-C6: cost is summed over ATTEMPTS, not over artifacts")
    hC = build_instruments(Harness(tmp / "d_ec6"))
    hC.generate(img_item, {**cfg, "lane": "image", "media_kind": "image",
                           "unit_price": 1.00, "inject_defects": []},
                A.dummy_generator)
    hC.generate(img_item, {**cfg, "lane": "image", "media_kind": "image",
                           "unit_price": 0.75}, A.refusing_generator, force=True)
    hC.generate(img_item, {**cfg, "lane": "image", "media_kind": "image",
                           "unit_price": 0.50}, A.erroring_generator, force=True)
    omC = hC.operational_metrics()
    check("a refused attempt with non-zero cost SURVIVES the total",
          abs(omC["cost_generation_total"] - 2.25) < 1e-9,
          f"total={omC['cost_generation_total']} (1.00 ok + 0.75 refusal + "
          f"0.50 error). Summing produced artifacts only would give 1.00.")
    check("the dropped portion is surfaced explicitly",
          abs(omC["cost_of_failed_or_refused_attempts"] - 1.25) < 1e-9,
          f"failed/refused cost={omC['cost_of_failed_or_refused_attempts']}")
    check("every attempt has a resolvable cost_ref",
          all(a.cost_ref in hC.cost_ledger for a in hC.attempts.values()),
          f"{len(hC.cost_ledger)} ledger lines")
    check("the misleading cost_in_retry_chains key is GONE",
          "cost_in_retry_chains" not in omC
          and "cost_of_retry_attempts" in omC)
    check("no complete CpAO chain cost is claimed without an acceptance",
          omC["complete_retry_chain_cost"] is None
          and omC["cpao_computable"] is False,
          f"status={omC['complete_retry_chain_cost_status']}")

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

    # --------------------------------------------------------------- EI-C7
    print("\nDEMO 6b — EI-C7: repeat structure is DERIVED from provenance")
    hB = build_instruments(Harness(tmp / "d_ec7"))
    bcfg = {**cfg, "lane": "general_video", "media_kind": "video",
            "inject_defects": [], "unit_price": 1.0}
    vid_items = [i for i in bank if i["class"] == "compound"
                 and i["modality"] == "video"]
    capZ = next(c for c in vid_items[0]["measurement_fanout"]
                if c in hB.instruments["dummy-temporal"].capabilities)
    hB.instruments["dummy-temporal"].qualification_status = "deterministic"

    def cell(items, repeats, extra_retry=False, dup_trial=False, short_item=None):
        """Build a cell from real provenance and return its measurements."""
        ms = []
        for it in items:
            n = repeats if (short_item is None or it["item_id"] != short_item) else repeats - 1
            base_att = None
            for k in range(n):
                if k == 0:
                    pr = hB.generate(it, bcfg, A.dummy_generator, force=True)
                    base_att = pr.attempt_id
                else:
                    pr = hB.generate(it, bcfg, A.dummy_generator,
                                     repeat_of=base_att, repeat_index=k)
                m = hB.measure(pr.asset_id, capZ, "dummy-temporal", it)
                m.synthetic = False
                ms.append(m)
                if dup_trial and k == 0:
                    m2 = hB.measure(pr.asset_id, capZ, "dummy-temporal", it)
                    m2.synthetic = False
                    ms.append(m2)
            if extra_retry:
                pr = hB.generate(it, bcfg, A.dummy_generator,
                                 retry_of=base_att, retry_reason="rejected")
                m = hB.measure(pr.asset_id, capZ, "dummy-temporal", it)
                m.synthetic = False
                ms.append(m)
        return ms

    good = cell(vid_items[:2], 2)
    check("a BALANCED cell is built from real provenance (2 items x 2 repeats)",
          len(good) == 4 and len({hB.trial_id_of(m.asset_id) for m in good}) == 4,
          f"{len(good)} measurements over "
          f"{len({hB.trial_id_of(m.asset_id) for m in good})} distinct trials")

    expect_raises("EI-C7: declaring 2 repeats while only 1 was observed is REFUSED",
                  lambda: hB.write_registry_row(capZ, "dummy-temporal",
                                                cell([vid_items[2]], 1), {}, 1, 2),
                  "do not contribute that many")
    expect_raises("EI-C7: two measurements of ONE trial is REFUSED",
                  lambda: hB.write_registry_row(
                      capZ, "dummy-temporal",
                      cell([vid_items[3]], 2, dup_trial=True), {}, 1, 2),
                  "more than one scoreable measurement")
    expect_raises("EI-C7: one item with fewer repeats than another is REFUSED",
                  lambda: hB.write_registry_row(
                      capZ, "dummy-temporal",
                      cell(vid_items[4:6], 2, short_item=vid_items[4]["item_id"]),
                      {}, 2, 2),
                  "observed trial structure")
    expect_raises("EI-C7: a retry masquerading inside the repeat cell is REFUSED",
                  lambda: hB.write_registry_row(
                      capZ, "dummy-temporal",
                      cell([vid_items[6]], 2, extra_retry=True), {}, 1, 2),
                  "production RETRIES")
    # The balance invariant is a belt-and-braces guard: if every item
    # contributes exactly repeats_per_item trials and no trial is double-counted,
    # trials == n_items * repeats_per_item follows. It is asserted here as a
    # guard rather than pretending it is independently reachable - a mis-shaped
    # cell is refused by whichever gate sees it first, and both refuse.
    expect_raises("EI-C7: a mis-shaped cell (3 trials over 2 items) is REFUSED",
                  lambda: hB.write_registry_row(capZ, "dummy-temporal",
                                                good[:3], {}, 2, 2),
                  "REGISTRY WRITE REFUSED")
    check("the balance invariant trials == n_items x repeats is enforced in code",
          "unbalanced cell" in pathlib.Path(HERE / "harness.py").read_text())
    check("no Registry row was created by any EI-C7 attempt",
          len(hB.registry_rows) == 0)

    # ---------------------------------------------------------------- E-C7
    print("\nDEMO 7 — E-C7: canonical Resources storage handoff")
    outdir = ROOT / "eval/v1/harness/out-selftest"
    if outdir.exists():
        shutil.rmtree(outdir)
    # include a refused attempt so we can prove it survives with no artifact
    h.generate(img_item, {**cfg, "lane": "image", "media_kind": "image", "model": "dummy-image-1",
                          "endpoint": "text-to-image"},
               A.refusing_generator, force=True)
    h.generate(img_item, {**cfg, "lane": "image", "media_kind": "image", "model": "dummy-image-2",
                          "endpoint": "text-to-image"},
               A.erroring_generator, force=True)
    summary = h.emit_storage_handoff(outdir)
    h.dump(outdir)

    for name in ("attempts", "artifacts", "measurements", "acceptances"):
        check(f"canonical record file emitted: {name}.jsonl",
              (outdir / f"{name}.jsonl").exists())
    check("no competing Eval-specific persistent manifest is emitted",
          not (outdir / "artifact-manifest.jsonl").exists(),
          "the old single manifest is gone; Resources owns the persistent model")

    attempts = [json.loads(l) for l in (outdir / "attempts.jsonl").read_text().splitlines() if l.strip()]
    artifacts = [json.loads(l) for l in (outdir / "artifacts.jsonl").read_text().splitlines() if l.strip()]
    meas = [json.loads(l) for l in (outdir / "measurements.jsonl").read_text().splitlines() if l.strip()]
    accept = [l for l in (outdir / "acceptances.jsonl").read_text().splitlines() if l.strip()]

    # criterion 7: every failed/refused call survives as its own attempt record
    failed = [a for a in attempts if a["status"] != "ok"]
    art_by_attempt = {}
    for r in artifacts:
        if not r.get("derived_from_artifact_id"):
            art_by_attempt.setdefault(r["attempt_id"], []).append(r)
    check("every failed/refused call survives as an ATTEMPT record",
          len(failed) >= 2
          and all(not art_by_attempt.get(a["attempt_id"]) for a in failed)
          and all(a["error_detail"] for a in failed),
          f"{len(failed)} non-ok attempts, none with a direct artifact, all "
          f"carrying error_detail; statuses={sorted({a['status'] for a in failed})}")
    check("attempts without an artifact are NOT dropped from the handoff",
          summary["attempts_without_artifact"] >= 2,
          f"attempts_without_artifact={summary['attempts_without_artifact']}")

    A_REQ = ["attempt_id", "eval_item_id", "provider", "model_id", "model_version",
             "endpoint", "workflow", "lane", "config_hash", "config_location",
             "reference_asset_hashes", "requested_at", "completed_at",
             "status", "error_detail", "repeat_index", "repeat_of_attempt_id",
             "retry_of_attempt_id", "retry_reason", "cost_ref", "storage_class",
             "prompt_hash", "trial_id"]
    F_REQ = ["artifact_id", "attempt_id", "trial_id", "output_hash",
             "output_bytes", "output_location", "media_kind", "storage_class",
             "derived_from_artifact_id", "derivation_type", "derivation_params"]
    M_REQ = ["measurement_id", "artifact_id", "trial_id", "capability_id",
             "instrument_ref", "instrument_version", "instrument_config_hash",
             "instrument_qualification_ref", "observation_unit", "measured_at",
             "result", "absence_reason", "defects"]
    for label, rows, req in (("attempt", attempts, A_REQ),
                             ("artifact", artifacts, F_REQ),
                             ("measurement", meas, M_REQ)):
        missing = [f for f in req if any(f not in r for r in rows)]
        check(f"{label} records carry every contract field", not missing,
              f"{len(rows)} rows, {len(req)} required, missing={missing or 'none'}")

    CANON = {"frame", "shot", "shot_pair", "sequence", "whole_asset",
             "asset_set_over_time"}
    bad_units = sorted({m["observation_unit"] for m in meas} - CANON)
    check("observation units are the CANONICAL vocabulary only", not bad_units,
          f"used: {summary['observation_unit_vocabulary']}")

    check("derived artifacts point to a parent and add no trial",
          summary["derived_artifacts"] > 0
          and summary["trials"] < len(artifacts),
          f"{len(artifacts)} artifacts, {summary['derived_artifacts']} derived, "
          f"{summary['trials']} trials")
    check("acceptance is EMPTY - Eval does not decide it",
          accept == [] and summary["acceptance_decided_by_eval"] is False)

    # The handoff must be REPRODUCIBLE. An absolute working path makes an
    # otherwise deterministic emission differ on every run and is meaningless
    # to Resources when archiving. This regressed once when emit_artifacts()
    # replaced the earlier manifest, so it is pinned here.
    abs_paths = [a["artifact_id"] for a in artifacts
                 if a["output_location"] and
                 (a["output_location"].startswith("/") or ":\\" in a["output_location"])]
    check("artifact locations are RELATIVE, not machine-specific", not abs_paths,
          f"{len(artifacts)} artifacts, absolute paths: {abs_paths or 'none'}")
    _first = h.emit_artifacts()
    _second = h.emit_artifacts()
    check("the handoff emission is deterministic across calls", _first == _second)

    om = h.operational_metrics()
    check("no routing score or weight was computed",
          om["routing_scores_computed"] == 0)
    check("generation and evaluator costs are separate lines",
          "cost_generation_total" in om and "cost_evaluator_total" in om,
          f"gen={om['cost_generation_total']} eval={om['cost_evaluator_total']}")

    print("\n" + "=" * 74)
    passed = sum(1 for _, ok, _ in results if ok)
    print(f"RESULT: {passed}/{len(results)} checks passed")
    print(f"Registry rows created: {len(h.registry_rows) + len(hM.registry_rows)}  (must be 0)")
    print(f"Paid API calls made:   0")
    print("=" * 74)
    shutil.rmtree(tmp, ignore_errors=True)
    return 0 if (passed == len(results) and not h.registry_rows
                 and not hM.registry_rows) else 1


if __name__ == "__main__":
    sys.exit(main())
