"""The pack build must be reproducible, complete, honest about what it skipped,
and must abort rather than ship a fixture whose truth is not knowable."""
import json

import pytest

import build_dummy_clips
import build_perturbation_pack as B
from clipseq import ClipError, ClipSequence


def tiny_clips(n_clips=4, n=12, w=40, h=28, fps=12):
    """Miniature stand-ins carrying the same declared structure as the real
    stand-in clips - a moving subject, a product box, a text box, and a cut in
    the last clip - but small enough that a full build takes a second.

    They exercise the machinery. Like every constructed clip in this package
    they qualify nothing.
    """
    out = []
    for k in range(n_clips):
        frames = []
        for i in range(n):
            f = bytearray(w * h * 3)
            for yy in range(6, h - 6):
                x = (i + k) % (w - 3)
                o = (yy * w + x) * 3
                f[o], f[o + 1], f[o + 2] = 200, 30 + 10 * k, 90
            for yy in range(2, 8):                       # product box pixels
                for xx in range(24, 34):
                    o = (yy * w + xx) * 3
                    f[o], f[o + 1], f[o + 2] = 60, 200, 160
            build_dummy_clips.render_text(f, w, (2, h - 12, 34, 10), "AB%d" % k)
            frames.append(f)
        shots = ([[0, n // 2], [n // 2, n]] if k == n_clips - 1 else [[0, n]])
        out.append(ClipSequence(
            f"tiny-{k:02d}", w, h, fps, frames,
            {"material_class": "constructed_stand_in",
             "regions": {"text": [2, h - 12, 34, 10], "product": [24, 2, 10, 6]},
             "region_source": "declared", "shots": shots,
             "text_string": "AB%d" % k}))
    return out


@pytest.fixture(scope="module")
def small_pack(tmp_path_factory):
    clips = tiny_clips()
    out = tmp_path_factory.mktemp("pack")
    manifest = B.build(clips, out)
    return manifest, out, clips


def test_build_produces_fixtures_controls_and_a_manifest(small_pack):
    m, out, _ = small_pack
    assert (out / "MANIFEST.json").is_file()
    assert m["counts"]["base_clips"] == 4
    assert m["counts"]["perturbed_fixtures"] > 0
    assert m["counts"]["clean_controls"] == 4
    assert m["counts"]["corrupt_controls"] >= 5


def test_every_fixture_carries_its_source_hash_config_and_interval(small_pack):
    m, _, _ = small_pack
    for f in m["fixtures"]:
        assert f["source_content_hash"]
        assert f["output_content_hash"]
        assert f["independent_opportunity_id"]
        if f["kind"] == "perturbed":
            assert f["params"], "a transformation with no recorded config is not reproducible"
            a, b = f["affected_output_frames"]
            assert 0 <= a < b <= f["output_n_frames"]
            assert f["defect_present"] is True


def test_clean_controls_are_byte_identical_to_their_source(small_pack):
    m, _, _ = small_pack
    base = {b["clip_id"]: b["content_hash"] for b in m["base_clips"]}
    for f in m["fixtures"]:
        if f["kind"] == "clean_control":
            assert f["output_content_hash"] == base[f["source_clip_id"]]
            assert f["defect_present"] is False


def test_no_perturbed_fixture_equals_its_source(small_pack):
    m, _, _ = small_pack
    for f in m["fixtures"]:
        if f["kind"] == "perturbed":
            assert f["output_content_hash"] != f["source_content_hash"]


def test_all_fixture_output_hashes_are_distinct(small_pack):
    m, _, _ = small_pack
    hashes = [f["output_content_hash"] for f in m["fixtures"]]
    assert len(set(hashes)) == len(hashes), "two fixtures with identical pixels are one fixture"


def test_verify_passes_on_a_fresh_build(small_pack):
    _, out, _ = small_pack
    ok, problems = B.verify(out)
    assert ok, problems


def test_rebuild_is_hash_identical(small_pack):
    _, out, clips = small_pack
    same, diffs = B.rebuild_is_identical(clips, out)
    assert same, diffs


def test_verify_catches_a_tampered_fixture(tmp_path):
    clips = tiny_clips(2)
    out = tmp_path / "p"
    m = B.build(clips, out)
    victim = next(f for f in m["fixtures"] if f["kind"] == "perturbed")
    (out / victim["path"] / "frame-00001.png").write_bytes(b"broken")
    ok, problems = B.verify(out)
    assert not ok and any(victim["fixture_id"] in p for p in problems)


def test_verify_fails_on_an_empty_manifest(tmp_path):
    (tmp_path / "MANIFEST.json").write_text(json.dumps({"fixtures": []}))
    ok, problems = B.verify(tmp_path)
    assert not ok
    assert any("empty check" in p for p in problems)


def test_verify_fails_when_the_transformation_code_changed(tmp_path):
    clips = tiny_clips(2)
    out = tmp_path / "p"
    B.build(clips, out)
    m = json.loads((out / "MANIFEST.json").read_text())
    m["configuration_hash"] = "0" * 64
    (out / "MANIFEST.json").write_text(json.dumps(m))
    ok, problems = B.verify(out)
    assert not ok
    assert any("configuration_hash" in p for p in problems)


def test_every_corrupt_control_refuses_to_load(small_pack):
    m, out, _ = small_pack
    controls = [c for c in m["controls"] if c["kind"] == "corrupt_control"]
    assert controls
    for c in controls:
        assert c["fail_closed"] is True
        with pytest.raises(ClipError):
            ClipSequence.read(out / "controls" / c["control_id"])


def test_builder_control_records_the_refused_no_op(small_pack):
    m, _, _ = small_pack
    nc = next(c for c in m["controls"] if c["control_id"] == "nc-null-perturbation")
    assert nc["observed"] == "NullPerturbationError"


def test_build_refuses_an_empty_clip_set(tmp_path):
    with pytest.raises(ClipError):
        B.build([], tmp_path / "empty")


def test_skips_are_recorded_with_reasons(small_pack):
    m, _, _ = small_pack
    for s in m["skipped"]:
        assert s["reason"] and s["perturbation_type"]


def test_standin_material_is_never_labelled_an_approved_pack(small_pack):
    m, _, _ = small_pack
    assert m["is_approved_qualification_pack"] is False
    assert m["material_classes"] == ["constructed_stand_in"]
    assert any("CONSTRUCTED STAND-IN" in c for c in m["caveats"])


def test_pack_declares_zero_calls_and_zero_spend(small_pack):
    m, _, _ = small_pack
    assert m["external_calls"] == 0
    assert m["model_or_evaluator_calls"] == 0
    assert m["human_labels_used"] == 0
    assert m["spend_usd"] == 0.0


def test_config_hash_changes_when_a_transformation_file_changes(monkeypatch, tmp_path):
    before = B.config_hash()
    fake = tmp_path / "perturbations.py"
    fake.write_text("# changed\n")
    monkeypatch.setattr(B, "HERE", tmp_path)
    for name in B.CONFIG_SOURCES:
        (tmp_path / name).write_text("# changed\n")
    assert B.config_hash() != before
