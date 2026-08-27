"""Every injected defect must be real, located where the manifest says, and
reproducible. And a transformation that changes nothing must be refused."""
import pytest

import perturbations as P
from clipseq import ClipError, ClipSequence


def moving_clip(clip_id="m", n=24, w=16, h=12, fps=12, offset=0):
    """A block that moves one pixel per frame, so every frame differs."""
    frames = []
    for i in range(n):
        f = bytearray(w * h * 3)
        x = (i + offset) % (w - 2)
        for yy in range(2, h - 2):
            o = (yy * w + x) * 3
            f[o], f[o + 1], f[o + 2] = 200, 40 + offset, 90
        frames.append(f)
    return ClipSequence(clip_id, w, h, fps, frames,
                        {"regions": {"text": [1, 1, 8, 4], "product": [8, 6, 6, 4]},
                         "region_source": "declared",
                         "shots": [[0, n // 2], [n // 2, n]],
                         "text_string": "HELLO",
                         "material_class": "constructed_stand_in"})


ALL = [
    ("frame_freeze", lambda c: P.frame_freeze(c, 6, 4)),
    ("frame_duplication", lambda c: P.frame_duplication(c, 6, 3, 1)),
    ("frame_drop", lambda c: P.frame_drop(c, 8, 3)),
    ("frame_reversal", lambda c: P.frame_reversal(c, 4, 6)),
    ("segment_reordering", lambda c: P.segment_reordering(c, 14, 4, 2)),
    ("midclip_horizontal_flip", lambda c: P.midclip_horizontal_flip(c, 10, 16)),
    ("shot_horizontal_flip", lambda c: P.shot_horizontal_flip(c, 1, [(0, 12), (12, 24)])),
    ("identity_splice", lambda c: P.identity_splice(c, moving_clip("d", offset=5), 6, 4)),
    ("product_region_substitution",
     lambda c: P.product_region_substitution(c, [8, 6, 6, 4], 10, 24)),
    ("text_region_mutation", lambda c: P.text_region_mutation(c, [1, 1, 8, 4], 12, 24)),
    ("framing_discontinuity", lambda c: P.framing_discontinuity(c, 12, 24)),
    ("technical_corruption", lambda c: P.technical_corruption(c, 9, 14)),
]


@pytest.mark.parametrize("name,fn", ALL, ids=[n for n, _ in ALL])
def test_every_perturbation_actually_changes_the_pixels(name, fn):
    src = moving_clip()
    out, truth = fn(src)
    assert out.content_hash() != src.content_hash()
    assert truth["perturbation_type"] == name
    assert truth["defect_present"] is True
    assert truth["source_content_hash"] == src.content_hash()
    assert truth["output_content_hash"] == out.content_hash()


@pytest.mark.parametrize("name,fn", ALL, ids=[n for n, _ in ALL])
def test_truth_records_a_usable_interval(name, fn):
    out, truth = fn(moving_clip())
    a, b = truth["affected_output_frames"]
    assert 0 <= a < b <= out.n_frames, f"{name}: interval {a},{b} not inside the output clip"
    t0, t1 = truth["affected_output_time_s"]
    assert t1 > t0 >= 0
    assert truth["min_samples_inside_interval"] in (1, 2)
    assert truth["min_uniform_sample_fps_for_visibility"] > 0


@pytest.mark.parametrize("name,fn", ALL, ids=[n for n, _ in ALL])
def test_perturbations_are_deterministic(name, fn):
    a, ta = fn(moving_clip())
    b, tb = fn(moving_clip())
    assert a.content_hash() == b.content_hash()
    assert ta == tb


@pytest.mark.parametrize("name,fn", ALL, ids=[n for n, _ in ALL])
def test_every_perturbation_names_a_frozen_capability(name, fn):
    _, truth = fn(moving_clip())
    assert truth["targets_capabilities"], f"{name} claims no capability"
    frozen = {
        "action_adherence", "motion_action_quality", "person_stability_in_clip",
        "product_stability_in_clip", "text_logo_stability_in_clip",
        "multi_shot_spatial_continuity", "camera_framing_fidelity",
        "sequence_state_continuity", "technical_visual_integrity",
    }
    assert set(truth["targets_capabilities"]) <= frozen, \
        f"{name} names a capability outside the frozen temporal_video family"


def test_freeze_makes_the_named_frames_identical():
    out, truth = P.frame_freeze(moving_clip(), 6, 4)
    a, b = truth["affected_output_frames"]
    held = out.frames[a]
    assert all(out.frames[i] == held for i in range(a, b))
    assert out.frames[b] != held, "the stall must end where the manifest says it ends"


def test_duplication_lengthens_and_freeze_does_not():
    src = moving_clip()
    dup, _ = P.frame_duplication(src, 6, 3, 1)
    frz, _ = P.frame_freeze(src, 6, 4)
    assert dup.n_frames == src.n_frames + 3
    assert frz.n_frames == src.n_frames


def test_drop_shortens_by_exactly_the_dropped_run():
    src = moving_clip()
    out, truth = P.frame_drop(src, 8, 3)
    assert out.n_frames == src.n_frames - 3
    assert truth["affected_source_frames"] == [8, 11]


def test_reversal_run_is_the_source_run_backwards():
    src = moving_clip()
    out, _ = P.frame_reversal(src, 4, 6)
    assert out.frames[4:10] == list(reversed(src.frames[4:10]))


def test_flip_is_its_own_inverse():
    src = moving_clip()
    once, _ = P.midclip_horizontal_flip(src, 10, 16)
    twice, _ = P.midclip_horizontal_flip(once, 10, 16)
    assert twice.content_hash() == src.content_hash()


def test_region_perturbation_touches_only_its_region_and_only_from_frame_k():
    src = moving_clip()
    out, truth = P.product_region_substitution(src, [8, 6, 6, 4], 10, 24)
    assert out.frames[:10] == src.frames[:10], "frames before the injection must be untouched"
    x, y, w, h = truth["affected_region_xywh"]
    f_out, f_src = out.frames[12], src.frames[12]
    for yy in range(src.height):
        for xx in range(src.width):
            o = (yy * src.width + xx) * 3
            inside = x <= xx < x + w and y <= yy < y + h
            if not inside:
                assert f_out[o:o + 3] == f_src[o:o + 3], "pixels outside the region changed"


def test_segment_reordering_preserves_the_frame_multiset():
    src = moving_clip()
    out, _ = P.segment_reordering(src, 14, 4, 2)
    assert sorted(bytes(f) for f in out.frames) == sorted(bytes(f) for f in src.frames)
    assert out.frames != src.frames, "the order must actually differ"


def test_identity_splice_uses_the_donor_frames_and_records_the_donor_hash():
    src = moving_clip()
    donor = moving_clip("d", offset=5)
    out, truth = P.identity_splice(src, donor, 6, 4)
    assert out.frames[6:10] == donor.frames[0:4]
    assert truth["donor_content_hash"] == donor.content_hash()


def test_identity_splice_refuses_a_geometry_mismatch():
    with pytest.raises(ClipError):
        P.identity_splice(moving_clip(), moving_clip("d", w=8, h=6, offset=3), 6, 4)


def test_identity_splice_refuses_the_same_material_as_donor():
    src = moving_clip()
    with pytest.raises(ClipError):
        P.identity_splice(src, moving_clip("other-name"), 6, 4)


def test_null_perturbation_is_refused():
    with pytest.raises(P.NullPerturbationError):
        P.null_perturbation(moving_clip())


def test_a_freeze_on_an_already_still_run_is_refused():
    """The defect must be a defect. Freezing frames that were already identical
    changes nothing, so it is a no-op and must not enter a pack."""
    still = ClipSequence("s", 8, 6, 12, [bytearray(144) for _ in range(10)])
    with pytest.raises(P.NullPerturbationError):
        P.frame_freeze(still, 2, 4)


def test_text_glyph_substitution_refuses_an_unchanged_string():
    with pytest.raises(ClipError):
        P.text_glyph_substitution(moving_clip(), [1, 1, 8, 4], 12, 24,
                                  lambda *a: None, "SAME", "SAME")


def test_shot_flip_needs_more_than_one_shot():
    with pytest.raises(ClipError):
        P.shot_horizontal_flip(moving_clip(), 0, [(0, 24)])


@pytest.mark.parametrize("call", [
    lambda c: P.frame_freeze(c, 20, 20),
    lambda c: P.frame_drop(c, -1, 3),
    lambda c: P.frame_reversal(c, 0, 2),
    lambda c: P.product_region_substitution(c, [100, 100, 10, 10], 2, 5),
    lambda c: P.technical_corruption(c, 2, 5, severity=0),
])
def test_out_of_range_arguments_fail_closed(call):
    with pytest.raises(ClipError):
        call(moving_clip())


def test_motion_load_is_recorded_for_source_and_output():
    """The frozen contract makes motion load a REQUIRED condition, because a
    near-static clip scores perfectly on smoothness."""
    _, truth = P.frame_freeze(moving_clip(), 6, 4)
    assert truth["source_motion_load"] > 0
    assert truth["output_motion_load"] < truth["source_motion_load"], \
        "a stall must lower measured motion load"
