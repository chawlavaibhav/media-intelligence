"""The async queue lifecycle: submit -> poll -> result -> download, as ONE trial."""
from decimal import Decimal

from conftest import MP4_FIXTURE_BYTES
from video_route import PilotVideoRoute, generate_pilot_video


def test_full_async_lifecycle_success(guard, transport, fal_key, tmp_path):
    sleeps = []
    route = PilotVideoRoute(transport=transport, guard=guard, sleep=sleeps.append,
                            poll_interval_s=10.0)
    outcome = route.generate("A short commercial clip", 6, "16:9", tmp_path)
    attempt, artifact = outcome["attempt"], outcome["artifact"]

    # exactly one generation trial, three lifecycle polls, one result fetch, one download
    assert route.submits == 1
    assert len(transport.submit_calls) == 1
    assert len(transport.status_calls) == 3
    assert len(transport.result_calls) == 1
    assert len(transport.bytes_calls) == 1
    assert sleeps == [10.0, 10.0]              # paced between polls, injected, no real wait

    assert attempt["api_status"] == "ok"
    assert attempt["error_class"] is None
    assert attempt["provider_request_id"] == "fal-q-0001"
    assert attempt["trial_id"] == attempt["attempt_id"]      # one call = one trial
    assert attempt["status_checks"] == 3
    assert attempt["retries"] == 0
    assert attempt["retry_of_attempt_id"] is None
    assert attempt["billing_state"] == "reported"
    assert attempt["outcome_resolved"] is True

    assert artifact is not None
    assert artifact["output_bytes"] == len(MP4_FIXTURE_BYTES)
    assert guard.spent_usd == Decimal("2.40")   # settled exactly once at the estimate
    assert guard.records == [Decimal("2.40")]


def test_polling_is_never_a_new_generation(guard, fal_key, tmp_path):
    """Ten polls before completion still count as ONE generation trial."""
    from conftest import FakeQueueTransport

    statuses = [(200, {"status": "IN_QUEUE"})] * 4 \
        + [(200, {"status": "IN_PROGRESS"})] * 5 \
        + [(200, {"status": "COMPLETED"})]
    transport = FakeQueueTransport(statuses=statuses)
    route = PilotVideoRoute(transport=transport, guard=guard, max_status_checks=20)
    outcome = route.generate("p", 6, "16:9", tmp_path)

    assert len(transport.submit_calls) == 1     # the trial
    assert len(transport.status_calls) == 10    # lifecycle steps of the SAME trial
    assert route.submits == 1
    assert outcome["attempt"]["status_checks"] == 10
    assert outcome["attempt"]["api_status"] == "ok"
    assert guard.records == [Decimal("2.40")]   # one trial, one settlement


def test_thin_interface_runs_the_same_single_trial(guard, transport, fal_key, tmp_path):
    outcome = generate_pilot_video("p", 8, "9:16", tmp_path, guard=guard,
                                   transport=transport)
    assert outcome["attempt"]["api_status"] == "ok"
    assert outcome["attempt"]["request_parameters"]["duration"] == "8s"
    assert outcome["attempt"]["request_parameters"]["aspect_ratio"] == "9:16"
    assert guard.spent_usd == Decimal("3.20")   # 8s at the per-second planning rate


def test_call_context_travels_to_the_attempt_record(guard, transport, fal_key, tmp_path):
    outcome = generate_pilot_video(
        "p", 6, "16:9", tmp_path, guard=guard, transport=transport,
        call_context={"attempt_id": "pilot-aight-001"})
    assert outcome["attempt"]["attempt_id"] == "pilot-aight-001"
    assert outcome["attempt"]["trial_id"] == "pilot-aight-001"
    assert outcome["artifact"]["attempt_id"] == "pilot-aight-001"
