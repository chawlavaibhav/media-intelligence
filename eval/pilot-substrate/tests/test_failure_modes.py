"""Every consequential failure mode: refusal, pre/post-dispatch, ambiguity, zero retries.

The invariant under test throughout: after the dispatch boundary, money is never released,
the attempt is always persisted, and NOTHING is ever dispatched a second time.
"""
import socket
from decimal import Decimal

import pytest

from conftest import FakeQueueTransport
from video_route import PilotVideoRoute

SPENT = Decimal("2.40")     # every 6s trial settles at the reserved estimate


def run(transport, guard, tmp_path, **kw):
    route = PilotVideoRoute(transport=transport, guard=guard, **kw)
    return route.generate("p", 6, "16:9", tmp_path), route


# ------------------------------------------------------------------------------ refusals
def test_content_policy_refusal_on_submit(guard, fal_key, tmp_path):
    transport = FakeQueueTransport(submit=(422, {
        "detail": [{"loc": ["body", "prompt"], "msg": "flagged",
                    "type": "content_policy_violation"}]}))
    outcome, route = run(transport, guard, tmp_path)
    a = outcome["attempt"]
    assert a["api_status"] == "refusal"            # the provider understood and declined
    assert a["error_class"] == "moderation_block"
    assert a["outcome_resolved"] is True
    assert outcome["artifact"] is None
    assert len(transport.submit_calls) == 1        # the refusal consumed its one trial
    assert guard.spent_usd == SPENT                # and it is not free


def test_content_policy_refusal_surfaced_at_completion(guard, fal_key, tmp_path):
    transport = FakeQueueTransport(statuses=[
        (200, {"status": "IN_PROGRESS"}),
        (200, {"status": "COMPLETED", "error": {"message": "blocked"},
               "error_type": "content_policy_violation"}),
    ])
    outcome, _ = run(transport, guard, tmp_path)
    assert outcome["attempt"]["api_status"] == "refusal"
    assert outcome["attempt"]["error_class"] == "moderation_block"
    assert transport.result_calls == []            # no artifact to fetch after a refusal
    assert guard.spent_usd == SPENT


def test_submit_validation_error_is_an_error_not_a_refusal(guard, fal_key, tmp_path):
    transport = FakeQueueTransport(submit=(422, {
        "detail": [{"loc": ["body", "duration"], "msg": "bad", "type": "value_error"}]}))
    outcome, _ = run(transport, guard, tmp_path)
    assert outcome["attempt"]["api_status"] == "error"
    assert outcome["attempt"]["error_class"] == "value_error"
    assert guard.spent_usd == SPENT                # it reached the provider; counted


# ------------------------------------------------------------------- ambiguous dispatch
def test_timeout_during_submit_is_ambiguous_and_conservative(guard, fal_key, tmp_path):
    transport = FakeQueueTransport(submit=socket.timeout("read timed out"))
    outcome, route = run(transport, guard, tmp_path)
    a = outcome["attempt"]
    assert a["api_status"] == "timeout"
    assert a["ambiguous_dispatch"] is True
    assert a["billing_state"] == "unknown_provisional"
    assert a["cost_basis"] == "conservative_reserved_estimate_billing_unknown"
    assert a["outcome_resolved"] is False
    assert guard.spent_usd == SPENT                # the money stays counted
    assert guard.released == 0                     # ambiguity NEVER releases headroom
    assert len(transport.submit_calls) == 1        # and is NEVER retried
    assert route.submits == 1


def test_connection_reset_during_submit_is_ambiguous(guard, fal_key, tmp_path):
    transport = FakeQueueTransport(submit=ConnectionResetError(54, "reset by peer"))
    outcome, _ = run(transport, guard, tmp_path)
    assert outcome["attempt"]["api_status"] == "error"
    assert outcome["attempt"]["error_class"] == "connection_reset"
    assert outcome["attempt"]["ambiguous_dispatch"] is True
    assert guard.spent_usd == SPENT


def test_malformed_submit_response_is_ambiguous(guard, fal_key, tmp_path):
    """200 with no request_id: the job may exist, but nothing can track it."""
    transport = FakeQueueTransport(submit=(200, {"unexpected": "shape"}))
    outcome, _ = run(transport, guard, tmp_path)
    a = outcome["attempt"]
    assert a["api_status"] == "error"
    assert a["error_class"] == "malformed_response"
    assert a["ambiguous_dispatch"] is True
    assert a["outcome_resolved"] is False
    assert guard.spent_usd == SPENT


def test_undocumented_queue_status_stops_conservatively(guard, fal_key, tmp_path):
    transport = FakeQueueTransport(statuses=[(200, {"status": "EXPLODED"})])
    outcome, _ = run(transport, guard, tmp_path)
    a = outcome["attempt"]
    assert a["error_class"] == "malformed_response"
    assert a["outcome_resolved"] is False
    assert len(transport.status_calls) == 1        # stopped at the first breach; no loop
    assert guard.spent_usd == SPENT


# ------------------------------------------------------------ post-submit lifecycle loss
def test_poll_network_failure_never_resubmits(guard, fal_key, tmp_path):
    transport = FakeQueueTransport(statuses=[TimeoutError("poll timed out")])
    outcome, route = run(transport, guard, tmp_path)
    a = outcome["attempt"]
    assert a["api_status"] == "timeout"
    assert a["error_class"] == "poll_read_timeout"
    assert a["provider_request_id"] == "fal-q-0001"  # the job EXISTS; id preserved
    assert a["outcome_resolved"] is False            # it may complete and bill
    assert len(transport.submit_calls) == 1          # no re-submit, ever
    assert guard.spent_usd == SPENT


def test_poll_budget_exhaustion_is_a_timeout_not_a_retry(guard, fal_key, tmp_path):
    transport = FakeQueueTransport(statuses=[(200, {"status": "IN_PROGRESS"})])
    outcome, route = run(transport, guard, tmp_path, max_status_checks=3)
    a = outcome["attempt"]
    assert a["api_status"] == "timeout"
    assert a["error_class"] == "poll_budget_exhausted"
    assert a["status_checks"] == 3
    assert a["outcome_resolved"] is False
    assert len(transport.submit_calls) == 1
    assert guard.spent_usd == SPENT


def test_result_fetch_failure_after_completion_is_billable(guard, fal_key, tmp_path):
    transport = FakeQueueTransport(result=ConnectionResetError(54, "reset"))
    outcome, _ = run(transport, guard, tmp_path)
    a = outcome["attempt"]
    assert a["error_class"] == "result_fetch_connection_reset"
    assert a["ambiguous_dispatch"] is True
    assert guard.spent_usd == SPENT


def test_completed_result_with_no_artifact_url(guard, fal_key, tmp_path):
    transport = FakeQueueTransport(result=(200, {"video": {}}))
    outcome, _ = run(transport, guard, tmp_path)
    a = outcome["attempt"]
    assert a["api_status"] == "error"
    assert a["error_class"] == "no_artifact_returned"
    assert a["outcome_resolved"] is True
    assert guard.spent_usd == SPENT


def test_artifact_download_failure_keeps_generation_billed_and_url_recorded(
        guard, fal_key, tmp_path):
    transport = FakeQueueTransport(artifact=TimeoutError("download stalled"))
    outcome, _ = run(transport, guard, tmp_path)
    a = outcome["attempt"]
    assert a["api_status"] == "error"
    assert a["error_class"] == "artifact_download_failed"
    assert a["artifact_url"] == "https://v3.fal.media/files/fake/pilot-0001.mp4"
    assert outcome["artifact"] is None
    assert guard.spent_usd == SPENT                  # the generation happened; it is paid
    assert len(transport.bytes_calls) == 1           # one fetch, no auto re-fetch


# ------------------------------------------------------------------------- zero retries
def test_zero_automatic_retries_even_when_a_second_call_would_succeed(
        guard, fal_key, tmp_path):
    """A transport that would succeed on call two never GETS a call two."""

    class FlakyThenFine(FakeQueueTransport):
        def post_json(self, url, headers, payload):
            if not self.submit_calls:
                self.submit_calls.append((url, dict(headers), payload))
                raise socket.timeout("first call times out")
            return super().post_json(url, headers, payload)

    transport = FlakyThenFine()
    outcome, route = run(transport, guard, tmp_path)
    assert len(transport.submit_calls) == 1
    assert route.submits == 1
    assert outcome["attempt"]["api_status"] == "timeout"
    assert outcome["attempt"]["retries"] == 0
    assert outcome["attempt"]["platform_auto_retry_disabled"] is True


def test_http_500_on_submit_is_counted_and_not_retried(guard, fal_key, tmp_path):
    transport = FakeQueueTransport(submit=(500, {"error": {"type": "internal_server_error"}}))
    outcome, _ = run(transport, guard, tmp_path)
    assert outcome["attempt"]["api_status"] == "error"
    assert outcome["attempt"]["error_class"] == "internal_server_error"
    assert len(transport.submit_calls) == 1
    assert guard.spent_usd == SPENT                  # conservative even on 5xx


def test_no_network_fixture_actually_bites():
    """Sanity: the autouse fixture makes a real connection attempt raise."""
    with pytest.raises(Exception, match="injected fake transport"):
        socket.create_connection(("example.com", 443), timeout=1)
