"""The real-clip path, exercised today on a locally encoded video.

No real footage exists yet, so these tests encode a video from constructed
frames with the same local ffmpeg the ingest uses, then ingest it back. That
proves the decode, normalisation, hashing, region-defaulting, shot-handling and
fail-closed behaviour work on an actual container - so the only thing still
missing when the 12 approved clips land is the clips.

Everything here runs on this machine. No account, no API, no spend.
"""
import json
import shutil
import subprocess

import pytest

import build_perturbation_pack as B
import ingest_clips as I
from clipseq import ClipError, ClipSequence, encode_png

pytestmark = pytest.mark.skipif(
    not (shutil.which("ffmpeg") and shutil.which("ffprobe")),
    reason="ffmpeg/ffprobe not installed on this machine")


def _encode_video(tmp_path, name="clip.mp4", seconds=7, fps=24, w=48, h=32):
    """Write a moving-block video locally. Zero spend, no network."""
    frames_dir = tmp_path / (name + ".frames")
    frames_dir.mkdir(parents=True, exist_ok=True)
    n = seconds * fps
    for i in range(n):
        f = bytearray(w * h * 3)
        x = (i * 2) % (w - 4)
        for yy in range(8, h - 8):
            for xx in range(x, x + 4):
                o = (yy * w + xx) * 3
                f[o], f[o + 1], f[o + 2] = 220, 60, 120
        (frames_dir / f"f-{i:05d}.png").write_bytes(encode_png(w, h, bytes(f)))
    out = tmp_path / name
    cmd = ["ffmpeg", "-y", "-nostdin", "-v", "error", "-framerate", str(fps),
           "-i", str(frames_dir / "f-%05d.png"), "-c:v", "libx264",
           "-preset", "ultrafast", "-crf", "0", "-pix_fmt", "yuv444p", str(out)]
    assert subprocess.run(cmd, capture_output=True, check=False).returncode == 0
    return out


def test_tool_versions_are_recorded():
    v = I.tool_versions()
    assert v["ffmpeg"] and v["ffprobe"], "the exact decoder must be recorded with the pack"


def test_ingest_produces_a_clipsequence_with_both_hashes(tmp_path):
    video = _encode_video(tmp_path)
    clip = I.ingest_file(video, "real-01", {}, target_fps=24)
    assert clip.fps == 24
    assert clip.n_frames == 7 * 24
    assert clip.duration_s == 7.0
    prov = clip.provenance
    assert len(prov["source_file_sha256"]) == 64, "the delivered file's own hash is recorded"
    assert clip.content_hash() != prov["source_file_sha256"], \
        "the file hash and the normalised-sequence hash are different facts"
    assert prov["ingest_decode_command"], "the exact decode command is recorded"
    assert prov["material_class"] == "supplied_real_clip"


def test_ingest_is_deterministic(tmp_path):
    video = _encode_video(tmp_path)
    a = I.ingest_file(video, "r", {}, target_fps=24)
    b = I.ingest_file(video, "r", {}, target_fps=24)
    assert a.content_hash() == b.content_hash()


def test_fps_normalisation_changes_the_sequence_identity(tmp_path):
    """Normalising to a different rate is a different material, and the hash says so."""
    video = _encode_video(tmp_path)
    a = I.ingest_file(video, "r", {}, target_fps=24)
    b = I.ingest_file(video, "r", {}, target_fps=12)
    assert a.content_hash() != b.content_hash()
    assert b.n_frames == a.n_frames // 2


def test_regions_default_to_geometry_and_say_so(tmp_path):
    clip = I.ingest_file(_encode_video(tmp_path), "r", {}, target_fps=24)
    assert clip.provenance["region_source"] == "geometric_default"
    assert set(clip.provenance["regions"]) == {"text", "product"}


def test_declared_regions_are_marked_declared(tmp_path):
    clip = I.ingest_file(_encode_video(tmp_path), "r",
                         {"regions": {"text": [1, 1, 10, 6], "product": [12, 8, 10, 8]}},
                         target_fps=24)
    assert clip.provenance["region_source"] == "declared"


def test_a_short_clip_is_refused(tmp_path):
    video = _encode_video(tmp_path, name="short.mp4", seconds=2)
    with pytest.raises(ClipError) as exc:
        I.ingest_file(video, "r", {}, target_fps=24)
    assert "below the declared minimum" in str(exc.value)


def test_a_long_clip_is_refused(tmp_path):
    video = _encode_video(tmp_path, name="long.mp4", seconds=25, w=24, h=16)
    with pytest.raises(ClipError):
        I.ingest_file(video, "r", {}, target_fps=24)


def test_a_missing_file_fails_closed(tmp_path):
    with pytest.raises(ClipError):
        I.ingest_file(tmp_path / "nope.mp4", "r", {})


def test_an_empty_file_fails_closed(tmp_path):
    p = tmp_path / "empty.mp4"
    p.write_bytes(b"")
    with pytest.raises(ClipError):
        I.ingest_file(p, "r", {})


def test_a_non_video_file_fails_closed(tmp_path):
    p = tmp_path / "junk.mp4"
    p.write_bytes(b"not a video at all" * 100)
    with pytest.raises(ClipError):
        I.ingest_file(p, "r", {})


def test_an_empty_ingest_config_is_a_failure(tmp_path):
    cfg = tmp_path / "clips.json"
    cfg.write_text(json.dumps({"clips": []}))
    with pytest.raises(ClipError):
        I.ingest_manifest(cfg, tmp_path / "out")


def test_cut_detection_finds_a_constructed_cut(tmp_path):
    """Deterministic, threshold-recorded, and only ever a proposal."""
    w, h, n = 32, 24, 24
    frames = []
    for i in range(n):
        col = (20, 20, 200) if i < n // 2 else (200, 30, 20)
        f = bytearray(bytes(col) * w * h)
        f[(i % 10) * 3] = 255
        frames.append(f)
    clip = ClipSequence("cut", w, h, 12, frames)
    shots = I.detect_cuts(clip)
    assert shots == [[0, 12], [12, 24]]


def test_single_shot_clip_reports_one_shot():
    w, h, n = 16, 12, 10
    frames = [bytearray(bytes((10, 10, 10)) * w * h) for _ in range(n)]
    for i, f in enumerate(frames):
        f[i * 3] = 200
    clip = ClipSequence("one", w, h, 12, frames)
    assert I.detect_cuts(clip) == [[0, n]]


def test_end_to_end_ingest_then_perturb(tmp_path):
    """The full path a real delivery will take: decode, then build a pack."""
    videos = [_encode_video(tmp_path, name=f"c{i}.mp4", seconds=6) for i in range(3)]
    clips = [I.ingest_file(v, f"real-{i:02d}", {}, target_fps=12)
             for i, v in enumerate(videos)]
    out = tmp_path / "pack"
    m = B.build(clips, out)
    assert m["is_approved_qualification_pack"] is True, \
        "a pack built purely from supplied clips is the real thing"
    assert m["material_classes"] == ["supplied_real_clip"]
    assert not any("CONSTRUCTED STAND-IN" in c for c in m["caveats"])
    ok, problems = B.verify(out)
    assert ok, problems
    # text_glyph_substitution is unavailable on footage we did not render
    assert "text_glyph_substitution" not in m["counts"]["by_perturbation_type"]
    assert any(s["perturbation_type"] == "text_glyph_substitution" for s in m["skipped"])
    # These constructed videos have a featureless default text box, so the text
    # mutation has nothing to alter. The build must record that rather than
    # invent a fixture, and must warn that the capability lost coverage.
    assert any(s["perturbation_type"] == "text_region_mutation"
               and "changed nothing" in s["reason"] for s in m["skipped"])
    assert any("text_logo_stability_in_clip" in w for w in m["coverage_warnings"])
