"""Provenance: hash-bound prompt/config, recoverable request, RES-007 production handoff."""
import hashlib
import json
import socket
from pathlib import Path

from conftest import (MP4_FIXTURE_BYTES, OPERATION_NAME, FakeGeminiTransport,
                      fixed_clock)
from video_route import (RES007_REQUIRED_FIELDS, GeminiVeoRoute,
                         res007_production_attempt)

PROMPT = "A festive premium 9:16 motion plate, warm light, no text"


def run_success(guard, tmp_path):
    route = GeminiVeoRoute(transport=FakeGeminiTransport(), guard=guard,
                           clock=fixed_clock())
    return route.generate(PROMPT, 8, "9:16", tmp_path)


# --------------------------------------------------------------- prompt/config binding
def test_prompt_hash_is_exact(guard, gemini_key, tmp_path):
    outcome = run_success(guard, tmp_path)
    assert outcome["attempt"]["prompt_hash"] == \
        hashlib.sha256(PROMPT.encode("utf-8")).hexdigest()


def test_config_hash_binds_the_recoverable_request_config(guard, gemini_key, tmp_path):
    outcome = run_success(guard, tmp_path)
    a = outcome["attempt"]
    config_path = Path(a["config_location"])
    assert config_path.exists()
    config_bytes = config_path.read_bytes()
    assert hashlib.sha256(config_bytes).hexdigest() == a["config_hash"]

    # The config is COMPLETE: the exact request could be reconstructed from it alone.
    config = json.loads(config_bytes.decode("utf-8"))
    assert config["model_id"] == "veo-3.1-fast-generate-preview"
    assert config["endpoint"].endswith(
        "models/veo-3.1-fast-generate-preview:predictLongRunning")
    assert config["request_body"]["instances"][0]["prompt"] == PROMPT
    assert config["request_body"]["parameters"] == {
        "aspectRatio": "9:16", "durationSeconds": 8, "resolution": "720p"}


def test_config_hash_changes_when_the_request_changes(guard, gemini_key, tmp_path):
    from conftest import RecordingGuard

    a = run_success(guard, tmp_path)["attempt"]
    b_dir = tmp_path / "b"
    route = GeminiVeoRoute(transport=FakeGeminiTransport(), guard=RecordingGuard(),
                           clock=fixed_clock())
    b = route.generate(PROMPT + " (variant)", 8, "9:16", b_dir)["attempt"]
    assert a["config_hash"] != b["config_hash"]
    assert a["prompt_hash"] != b["prompt_hash"]


def test_exact_provider_model_endpoint_preserved_on_the_attempt(guard, gemini_key,
                                                                tmp_path):
    a = run_success(guard, tmp_path)["attempt"]
    assert a["provider"] == "google"
    assert a["model_id"] == "veo-3.1-fast-generate-preview"
    assert a["model_version"] == "veo-3.1-fast-generate-preview"
    assert a["endpoint"] == ("https://generativelanguage.googleapis.com/v1beta/models/"
                             "veo-3.1-fast-generate-preview:predictLongRunning")
    assert a["workflow"] == "t2v"
    assert a["lane"] == "native_av"
    assert a["storage_class"] == "C_irreproducible_empirical"


# ------------------------------------------------------------- RES-007 handoff adapter
def test_production_attempt_satisfies_the_corrected_res007_field_set(guard, gemini_key,
                                                                     tmp_path):
    outcome = run_success(guard, tmp_path)
    handoff = res007_production_attempt(outcome)
    wf = handoff["writer_fields"]

    for field_name in RES007_REQUIRED_FIELDS:
        assert field_name in wf, f"missing required handoff field {field_name}"
    # G12-required inherited provenance is present AND non-null on a successful attempt
    for field_name in ("provider", "model_id", "model_version", "endpoint", "workflow",
                       "prompt_hash", "config_hash", "config_location", "requested_at"):
        assert wf[field_name], f"required inherited field {field_name} is empty"
    assert isinstance(wf["reference_asset_hashes"], list)      # list, empty if none
    assert wf["attempt_kind"] == "production"
    assert wf["status"] == "ok"
    assert wf["lane"] == "native_av"
    assert wf["completed_at"] is not None
    assert wf["error_detail"] is None                          # ok attempts carry none


def test_production_attempt_contains_no_fabricated_eval_item_id(guard, gemini_key,
                                                                tmp_path):
    """Per the RES-007 Controller correction: a production attempt serves a brief, not a
    benchmark item. The corrected writer REFUSES eval_item_id on production attempts, so
    the handoff must not even carry the key."""
    handoff = res007_production_attempt(run_success(guard, tmp_path))
    assert "eval_item_id" not in handoff["writer_fields"]
    assert "eval_item_id" not in handoff["provider_extras"]


def test_failed_attempt_handoff_carries_error_detail_and_null_completed_at(
        guard, gemini_key, tmp_path):
    """The corrected writer requires error_detail on non-ok status, and completed_at may
    be None only where the call genuinely never resolved — exactly the ambiguous case."""
    transport = FakeGeminiTransport(submit=socket.timeout("read timed out"))
    route = GeminiVeoRoute(transport=transport, guard=guard, clock=fixed_clock())
    outcome = route.generate(PROMPT, 8, "9:16", tmp_path)
    wf = res007_production_attempt(outcome)["writer_fields"]
    assert wf["status"] == "timeout"
    assert wf["error_detail"] and "read_timeout" in wf["error_detail"]
    assert wf["completed_at"] is None              # the call never resolved
    assert wf["requested_at"] is not None          # but it WAS dispatched
    for field_name in ("provider", "model_id", "model_version", "endpoint", "workflow",
                       "prompt_hash", "config_hash", "config_location"):
        assert wf[field_name], f"failed attempt still needs {field_name}"


def test_provider_extras_stay_out_of_writer_fields(guard, gemini_key, tmp_path):
    """The corrected writer refuses unknown fields; provider evidence rides separately."""
    handoff = res007_production_attempt(run_success(guard, tmp_path))
    wf, extras = handoff["writer_fields"], handoff["provider_extras"]
    for provider_key in ("operation_name", "artifact_uri", "status_checks",
                         "billing_state", "request_parameters"):
        assert provider_key in extras
        assert provider_key not in wf
    assert extras["operation_name"] == OPERATION_NAME


def test_handoff_is_json_serialisable_and_lossless(guard, gemini_key, tmp_path):
    outcome = run_success(guard, tmp_path)
    handoff = res007_production_attempt(outcome)
    loaded = json.loads(json.dumps(handoff, ensure_ascii=False, sort_keys=True))
    assert loaded["writer_fields"]["config_hash"] == outcome["attempt"]["config_hash"]
    assert loaded["provider_extras"]["artifact_uri"] == outcome["attempt"]["artifact_uri"]


def test_repeat_and_retry_fields_are_pinned_first_attempt_values(guard, gemini_key,
                                                                 tmp_path):
    wf = res007_production_attempt(run_success(guard, tmp_path))["writer_fields"]
    assert wf["repeat_index"] == 0
    assert wf["repeat_of_attempt_id"] is None
    assert wf["retry_of_attempt_id"] is None
    assert wf["retry_reason"] is None
