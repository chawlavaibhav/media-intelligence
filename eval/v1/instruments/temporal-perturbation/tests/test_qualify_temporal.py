"""The scoring harness must be unable to flatter an instrument.

It must: refuse an incomplete run, refuse a run with no sample rate, report
recall per perturbation type rather than as one average, count clips rather than
frames as opportunities, and never emit `qualified`.
"""
import copy
import json

import pytest

import qualify_temporal as Q
from test_pack_build import tiny_clips
import build_perturbation_pack as B


@pytest.fixture(scope="module")
def manifest(tmp_path_factory):
    return B.build(tiny_clips(), tmp_path_factory.mktemp("qpack"))


INSTRUMENT = {"instrument_id": "test-instrument", "instrument_version": "v0",
              "configuration_hash": "abc", "calls": 0}


def test_perfect_selftest_finds_every_injected_defect(manifest):
    rec = Q.score(manifest, Q.synthetic_detections(manifest, "perfect"), INSTRUMENT)
    assert rec["gate"]["false_passes"] == 0
    assert rec["gate"]["false_fails"] == 0
    for v in rec["recall_by_perturbation_type"].values():
        assert v["recall_over_fixtures"] == 1.0


def test_a_blind_spot_is_visible_per_type_not_hidden_in_an_average(manifest):
    rec = Q.score(manifest, Q.synthetic_detections(manifest, "blind_to_text"), INSTRUMENT)
    text_types = [t for t in rec["recall_by_perturbation_type"]
                  if t.startswith("text_")]
    assert text_types
    for t in text_types:
        assert rec["recall_by_perturbation_type"][t]["recall_over_fixtures"] == 0.0
    others = [v["recall_over_fixtures"] for t, v in rec["recall_by_perturbation_type"].items()
              if not t.startswith("text_")]
    assert all(v == 1.0 for v in others)
    assert "never_report_a_single_average" in rec


def test_false_alarms_on_clean_controls_are_counted(manifest):
    rec = Q.score(manifest, Q.synthetic_detections(manifest, "alarmist"), INSTRUMENT)
    assert rec["gate"]["false_fails"] == rec["gate"]["clean_controls"] > 0
    assert rec["gate"]["clean_control_false_positive_rate"] == 1.0


def test_an_incomplete_run_is_unmeasurable_not_a_score(manifest):
    rec = Q.score(manifest, Q.synthetic_detections(manifest, "incomplete"), INSTRUMENT)
    assert rec["status"] == "unmeasurable"
    assert rec["incomplete_run"]["missing_count"] > 0
    assert "not a miss and not a pass" in rec["status_reason"]


def test_missing_sample_rate_invalidates_the_run(manifest):
    dets = copy.deepcopy(Q.synthetic_detections(manifest, "perfect"))
    dets[3]["sampled_frames"] = None
    rec = Q.score(manifest, dets, INSTRUMENT)
    assert rec["status"] == "unmeasurable"
    assert rec["incomplete_run"]["records_without_sample_rate"]


def test_empty_detections_are_a_failure_not_a_pass(manifest):
    with pytest.raises(Q.ScoringError):
        Q.score(manifest, [], INSTRUMENT)


def test_empty_manifest_is_a_failure(manifest):
    with pytest.raises(Q.ScoringError):
        Q.score({"fixtures": []}, [{"fixture_id": "x"}], INSTRUMENT)


def test_duplicate_detection_records_are_refused(manifest):
    dets = Q.synthetic_detections(manifest, "perfect")
    with pytest.raises(Q.ScoringError):
        Q.score(manifest, dets + [dets[0]], INSTRUMENT)


def test_unknown_fixture_ids_invalidate_the_run(manifest):
    dets = Q.synthetic_detections(manifest, "perfect")
    dets.append({"fixture_id": "not-in-this-pack", "defect_detected": True,
                 "sampled_frames": 10})
    rec = Q.score(manifest, dets, INSTRUMENT)
    assert rec["status"] == "unmeasurable"
    assert rec["incomplete_run"]["unknown_fixture_ids"] == ["not-in-this-pack"]


def test_opportunities_are_clips_not_fixtures(manifest):
    rec = Q.score(manifest, Q.synthetic_detections(manifest, "perfect"), INSTRUMENT)
    assert rec["gate"]["n_opportunities"] == manifest["counts"]["base_clips"]
    assert rec["gate"]["n_perturbed_fixtures"] > rec["gate"]["n_opportunities"]
    assert "ONE trial" in rec["gate"]["opportunity_definition"]


def test_standin_material_can_never_be_scored_as_qualified(manifest):
    for profile in ("perfect", "blind_to_text", "alarmist"):
        rec = Q.score(manifest, Q.synthetic_detections(manifest, profile), INSTRUMENT,
                      repeats=5, threshold_ref="pretend-approval")
        assert rec["status"] == "unmeasurable"
        assert rec["registry_use_permitted"] is False


def test_real_material_without_a_pass_mark_stops_short_of_qualified(manifest):
    """Even on approved material, with repeats done, this file cannot promote."""
    m = copy.deepcopy(manifest)
    m["is_approved_qualification_pack"] = True
    m["material_classes"] = ["supplied_real_clip"]
    rec = Q.score(m, Q.synthetic_detections(m, "perfect"), INSTRUMENT, repeats=3)
    assert rec["status"] == "provisional"
    assert rec["registry_use_permitted"] is False
    assert rec["gate"]["gate_verdict"] == "undetermined"
    assert "no Controller-approved" in rec["status_reason"]


def test_one_pass_is_screening_never_a_status(manifest):
    m = copy.deepcopy(manifest)
    m["is_approved_qualification_pack"] = True
    m["material_classes"] = ["supplied_real_clip"]
    rec = Q.score(m, Q.synthetic_detections(m, "perfect"), INSTRUMENT, repeats=1)
    assert rec["status"] == "screened_not_qualified"


def test_status_is_always_one_of_the_frozen_values(manifest):
    rec = Q.score(manifest, Q.synthetic_detections(manifest, "perfect"), INSTRUMENT)
    assert rec["status"] in Q.ALLOWED_STATUS


def test_localisation_is_measured_against_the_injected_interval(manifest):
    dets = copy.deepcopy(Q.synthetic_detections(manifest, "perfect"))
    for d in dets:
        if d["reported_frames"]:
            d["reported_frames"] = [0, 1]           # detected, but pointing elsewhere
    rec = Q.score(manifest, dets, INSTRUMENT)
    assert rec["localisation"]["n_with_reported_interval"] > 0
    assert max(rec["localisation"]["gap_frames_distribution"]) > 0
    assert "No tolerance is applied" in rec["localisation"]["note"]


def test_refusals_are_counted_separately_not_folded_into_recall(manifest):
    dets = copy.deepcopy(Q.synthetic_detections(manifest, "perfect"))
    dets[0] = {"fixture_id": dets[0]["fixture_id"], "refused": True}
    rec = Q.score(manifest, dets, INSTRUMENT)
    assert rec["gate"]["refusals"] == 1


def test_reference_bound_always_carries_its_independence_warning(manifest):
    rec = Q.score(manifest, Q.synthetic_detections(manifest, "blind_to_text"), INSTRUMENT)
    ref = rec["reference_calculation"]
    assert ref["independence_status"] == "NOT ESTABLISHED"
    assert ref["computed_over"] == "independent clips, not fixtures"
    assert 0.0 <= ref["iid_reference_upper_bound_95pct"] <= 1.0


def test_clopper_pearson_behaves_at_the_edges():
    assert Q.clopper_pearson_upper(0, 0) is None
    assert Q.clopper_pearson_upper(5, 5) == 1.0
    assert 0.2 < Q.clopper_pearson_upper(0, 12) < 0.3


def test_diagnosis_is_stored_apart_from_the_gate(manifest):
    dets = copy.deepcopy(Q.synthetic_detections(manifest, "perfect"))
    for d in dets:
        if d["reported_type"]:
            d["reported_type"] = "wrong_label"
    rec = Q.score(manifest, dets, INSTRUMENT)
    assert rec["gate"]["false_passes"] == 0, "the gate is still perfect"
    assert rec["diagnosis"]["wrong_class"] > 0, "the diagnosis is not"


def test_blindness_check_flags_the_manifest_itself(tmp_path, manifest):
    mp = tmp_path / "MANIFEST.json"
    mp.write_text(json.dumps(manifest))
    res = Q.check_blindness([mp], mp)
    assert res["result"] == "leak_detected"


def test_blindness_check_fails_closed_on_a_missing_path(tmp_path):
    res = Q.check_blindness([tmp_path / "nope"], tmp_path / "MANIFEST.json")
    assert res["result"] == "leak_detected"


def test_blindness_check_passes_on_frames_only(tmp_path, manifest):
    frames_dir = tmp_path / "frames"
    frames_dir.mkdir()
    (frames_dir / "frame-00000.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    res = Q.check_blindness([frames_dir], tmp_path / "MANIFEST.json")
    assert res["result"] == "clean"


def test_conditions_record_resolution_fps_and_motion_load_range(manifest):
    """A qualification is only valid inside the conditions it was measured under,
    so those conditions have to actually be in the record."""
    rec = Q.score(manifest, Q.synthetic_detections(manifest, "perfect"), INSTRUMENT)
    cond = rec["conditions"]
    assert cond["resolution"] and all("x" in r for r in cond["resolution"])
    assert cond["fps"] and all(isinstance(f, int) for f in cond["fps"])
    assert cond["clip_duration_s"]
    lo, hi = cond["source_motion_load_range"]
    assert lo is not None and hi is not None and hi >= lo
    assert cond["sampled_frames_values_observed"]
    assert "at or above" in cond["sample_rate_rule"]
