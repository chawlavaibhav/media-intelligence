"""The long-running-operation lifecycle: submit -> poll -> result -> download, as ONE trial."""
from decimal import Decimal

from conftest import MP4_FIXTURE_BYTES, OPERATION_NAME, VIDEO_URI, fixed_clock
from video_route import GeminiVeoRoute, generate_pilot_video


def test_full_async_lifecycle_success(guard, transport, gemini_key, tmp_path):
    sleeps = []
    route = GeminiVeoRoute(transport=transport, guard=guard, sleep=sleeps.append,
                           clock=fixed_clock(), poll_interval_s=10.0)
    outcome = route.generate("A festive premium motion plate", 8, "9:16", tmp_path)
    attempt, artifact = outcome["attempt"], outcome["artifact"]

    # exactly one generation trial, three lifecycle polls, one download
    assert route.submits == 1
    assert len(transport.submit_calls) == 1
    assert len(transport.poll_calls) == 3
    assert len(transport.bytes_calls) == 1
    assert sleeps == [10.0, 10.0]              # paced between polls, injected, no real wait

    assert attempt["status"] == "ok"
    assert attempt["error_class"] is None
    assert attempt["operation_name"] == OPERATION_NAME
    assert attempt["artifact_uri"] == VIDEO_URI
    assert attempt["trial_id"] == attempt["attempt_id"]      # one call = one trial
    assert attempt["status_checks"] == 3
    assert attempt["retries"] == 0
    assert attempt["retry_of_attempt_id"] is None
    assert attempt["billing_state"] == "reported"
    assert attempt["outcome_resolved"] is True
    assert attempt["requested_at"] < attempt["completed_at"]  # both stamped, ordered

    assert artifact is not None
    assert artifact["output_bytes"] == len(MP4_FIXTURE_BYTES)
    assert guard.spent_usd == Decimal("0.80")   # settled exactly once at the estimate
    assert guard.records == [Decimal("0.80")]


def test_polling_is_never_a_new_generation(guard, gemini_key, tmp_path):
    """Ten polls before completion still count as ONE generation trial."""
    from conftest import FakeGeminiTransport

    polls = [(200, {"name": OPERATION_NAME, "done": False})] * 9 \
        + [(200, {"name": OPERATION_NAME, "done": True,
                  "response": {"generateVideoResponse": {
                      "generatedSamples": [{"video": {"uri": VIDEO_URI}}]}}})]
    transport = FakeGeminiTransport(polls=polls)
    route = GeminiVeoRoute(transport=transport, guard=guard, max_status_checks=20)
    outcome = route.generate("p", 8, "9:16", tmp_path)

    assert len(transport.submit_calls) == 1     # the trial
    assert len(transport.poll_calls) == 10      # lifecycle steps of the SAME trial
    assert route.submits == 1
    assert outcome["attempt"]["status_checks"] == 10
    assert outcome["attempt"]["status"] == "ok"
    assert guard.records == [Decimal("0.80")]   # one trial, one settlement


def test_thin_interface_runs_the_same_single_trial(guard, transport, gemini_key, tmp_path):
    outcome = generate_pilot_video("p", 4, "16:9", tmp_path, guard=guard,
                                   transport=transport)
    assert outcome["attempt"]["status"] == "ok"
    assert outcome["attempt"]["request_parameters"]["durationSeconds"] == 4
    assert outcome["attempt"]["request_parameters"]["aspectRatio"] == "16:9"
    assert guard.spent_usd == Decimal("0.40")   # 4s at the per-second published rate


def test_call_context_travels_to_the_attempt_record(guard, transport, gemini_key,
                                                    tmp_path):
    outcome = generate_pilot_video(
        "p", 8, "9:16", tmp_path, guard=guard, transport=transport,
        call_context={"attempt_id": "pilot-aight-001"})
    assert outcome["attempt"]["attempt_id"] == "pilot-aight-001"
    assert outcome["attempt"]["trial_id"] == "pilot-aight-001"
    assert outcome["artifact"]["attempt_id"] == "pilot-aight-001"
