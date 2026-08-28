"""Binary artifact handling: bytes stay bytes, hashes bind, text APIs are refused."""
import hashlib
import json

import pytest

import artifact_store as AS
from conftest import MP4_FIXTURE_BYTES, OPERATION_NAME, FakeGeminiTransport
from video_route import GeminiVeoRoute

IDENTITY = {"slot": "VID-PILOT-01", "provider": "google",
            "provider_surface": "gemini-developer-api",
            "model_id": "veo-3.1-fast-generate-preview",
            "model_version": "veo-3.1-fast-generate-preview",
            "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/"
                        "veo-3.1-fast-generate-preview:predictLongRunning",
            "workflow": "t2v", "lane": "native_av"}


def persist(tmp_path, data=MP4_FIXTURE_BYTES, **kw):
    args = dict(out_dir=tmp_path, attempt_id="att-x", trial_id="att-x", identity=IDENTITY,
                provider_request_id=OPERATION_NAME, content_type="video/mp4",
                declared_file_size=None,
                source_url="https://generativelanguage.googleapis.com/v1beta/files/f:download")
    args.update(kw)
    return AS.persist_video_bytes(data, **args)


def test_fixture_bytes_would_fail_any_text_path():
    """The fixture is invalid UTF-8 BY DESIGN: a text API cannot survive it silently."""
    with pytest.raises(UnicodeDecodeError):
        MP4_FIXTURE_BYTES.decode("utf-8")


def test_bytes_round_trip_with_exact_hash_and_count(tmp_path):
    record = persist(tmp_path)
    assert record["output_bytes"] == len(MP4_FIXTURE_BYTES)
    assert record["output_sha256"] == hashlib.sha256(MP4_FIXTURE_BYTES).hexdigest()
    assert record["media_kind"] == "video"
    on_disk = open(record["output_location"], "rb").read()
    assert on_disk == MP4_FIXTURE_BYTES                     # byte-identical, not "similar"
    assert AS.verify_artifact(record) is True


def test_str_payload_refused(tmp_path):
    with pytest.raises(TypeError, match="bytes, not str"):
        persist(tmp_path, data="this is text pretending to be a video")


def test_empty_payload_refused(tmp_path):
    with pytest.raises(AS.ArtifactIntegrityError, match="empty"):
        persist(tmp_path, data=b"")


def test_artifacts_are_immutable(tmp_path):
    persist(tmp_path)
    with pytest.raises(AS.ArtifactIntegrityError, match="immutable"):
        persist(tmp_path)                                    # same attempt_id, same path


@pytest.mark.parametrize("content_type,kind,ext", [
    ("video/mp4", "video", ".mp4"),
    ("video/webm", "video", ".webm"),
    ("video/x-unknown", "video", ".bin"),   # video/* but unmapped: kind kept, ext generic
    (None, "other", ".bin"),                # undeclared: conservative, never guessed
])
def test_media_kind_derived_from_served_content_type(tmp_path, content_type, kind, ext):
    record = persist(tmp_path, content_type=content_type)
    assert record["media_kind"] == kind
    assert record["output_location"].endswith(ext)


def test_declared_size_mismatch_is_recorded_not_hidden(tmp_path):
    record = persist(tmp_path, declared_file_size=999999)
    assert record["declared_size_matches"] is False
    assert record["output_bytes"] == len(MP4_FIXTURE_BYTES)  # actual bytes stay the truth


def test_lifecycle_persists_real_binary_end_to_end(guard, gemini_key, tmp_path):
    """Through the full route: the served bytes land on disk hash-bound to the attempt."""
    transport = FakeGeminiTransport()
    route = GeminiVeoRoute(transport=transport, guard=guard)
    outcome = route.generate("p", 8, "9:16", tmp_path)
    art = outcome["artifact"]
    assert art["output_sha256"] == hashlib.sha256(MP4_FIXTURE_BYTES).hexdigest()
    assert art["output_bytes"] == len(MP4_FIXTURE_BYTES)
    assert art["media_kind"] == "video"                      # from the served content type
    assert art["model_id"] == "veo-3.1-fast-generate-preview"
    assert art["provider_request_id"] == OPERATION_NAME
    assert art["attempt_id"] == outcome["attempt"]["attempt_id"]
    assert open(art["output_location"], "rb").read() == MP4_FIXTURE_BYTES


def test_artifact_provenance_survives_json_round_trip(guard, gemini_key, tmp_path):
    transport = FakeGeminiTransport()
    route = GeminiVeoRoute(transport=transport, guard=guard)
    outcome = route.generate("p", 8, "9:16", tmp_path)

    stored = tmp_path / "outcome.json"
    stored.write_text(json.dumps(
        {"attempt": outcome["attempt"], "artifact": outcome["artifact"]},
        ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    loaded = json.loads(stored.read_text(encoding="utf-8"))

    for rec in (loaded["attempt"], loaded["artifact"]):
        assert rec["model_id"] == "veo-3.1-fast-generate-preview"
        assert rec["model_version"] == "veo-3.1-fast-generate-preview"
        assert rec["provider"] == "google"
        assert rec["endpoint"].endswith(
            "models/veo-3.1-fast-generate-preview:predictLongRunning")
    assert loaded["artifact"]["output_sha256"] == \
        hashlib.sha256(MP4_FIXTURE_BYTES).hexdigest()
    assert AS.verify_artifact(loaded["artifact"]) is True    # the file still matches
