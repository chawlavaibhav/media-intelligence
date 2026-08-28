"""Every consequential failure mode: refusal, pre/post-dispatch, ambiguity, zero retries.

The invariant under test throughout: after the dispatch boundary, money is never released,
the attempt is always persisted, and NOTHING is ever dispatched a second time.
"""
import socket
from decimal import Decimal

import pytest

from conftest import OPERATION_NAME, VIDEO_URI, FakeGeminiTransport
from video_route import GeminiVeoRoute

SPENT = Decimal("0.80")     # every 8s trial settles at the reserved estimate


def run(transport, guard, tmp_path, **kw):
    route = GeminiVeoRoute(transport=transport, guard=guard, **kw)
    return route.generate("p", 8, "9:16", tmp_path), route


def _done(payload):
    return (200, {"name": OPERATION_NAME, "done": True, **payload})


# --------------------------------------------------------------------- operation failure
def test_operation_error_is_a_counted_failed_trial(guard, gemini_key, tmp_path):
    transport = FakeGeminiTransport(polls=[_done(
        {"error": {"code": 3, "status": "INVALID_ARGUMENT", "message": "bad request"}})])
    outcome, _ = run(transport, guard, tmp_path)
    a = outcome["attempt"]
    assert a["status"] == "error"
    assert a["error_class"] == "INVALID_ARGUMENT"
    assert a["outcome_resolved"] is True
    assert outcome["artifact"] is None
    assert len(transport.submit_calls) == 1        # the failure consumed its one trial
    assert guard.spent_usd == SPENT                # and it is not free


def test_safety_filtered_generation_is_a_refusal(guard, gemini_key, tmp_path):
    """Google documents safety blocking; the rai* fields are read only when present."""
    transport = FakeGeminiTransport(polls=[_done(
        {"response": {"generateVideoResponse": {
            "generatedSamples": [],
            "raiMediaFilteredCount": 1,
            "raiMediaFilteredReasons": ["blocked by safety filter"]}}})])
    outcome, _ = run(transport, guard, tmp_path)
    a = outcome["attempt"]
    assert a["status"] == "refusal"                # the provider understood and declined
    assert a["error_class"] == "safety_filtered"
    assert "safety filter" in a["raw_status_note"]
    assert a["outcome_resolved"] is True
    # Google documents blocked videos as not charged; the ledger still settles the
    # reserved estimate because an overstatement is correctable and a release is not.
    assert guard.spent_usd == SPENT


def test_done_with_no_samples_and_no_filter_fields_is_no_artifact(guard, gemini_key,
                                                                  tmp_path):
    transport = FakeGeminiTransport(polls=[_done(
        {"response": {"generateVideoResponse": {"generatedSamples": []}}})])
    outcome, _ = run(transport, guard, tmp_path)
    assert outcome["attempt"]["status"] == "error"
    assert outcome["attempt"]["error_class"] == "no_artifact_returned"
    assert guard.spent_usd == SPENT


def test_submit_http_error_is_counted_and_not_retried(guard, gemini_key, tmp_path):
    transport = FakeGeminiTransport(submit=(400, {"error": {
        "code": 400, "status": "INVALID_ARGUMENT", "message": "unsupported duration"}}))
    outcome, _ = run(transport, guard, tmp_path)
    assert outcome["attempt"]["status"] == "error"
    assert outcome["attempt"]["error_class"] == "INVALID_ARGUMENT"
    assert len(transport.submit_calls) == 1
    assert guard.spent_usd == SPENT                # it reached the provider; counted


# ------------------------------------------------------------------- ambiguous dispatch
def test_timeout_during_submit_is_ambiguous_and_conservative(guard, gemini_key, tmp_path):
    transport = FakeGeminiTransport(submit=socket.timeout("read timed out"))
    outcome, route = run(transport, guard, tmp_path)
    a = outcome["attempt"]
    assert a["status"] == "timeout"
    assert a["ambiguous_dispatch"] is True
    assert a["billing_state"] == "unknown_provisional"
    assert a["cost_basis"] == "conservative_reserved_estimate_billing_unknown"
    assert a["outcome_resolved"] is False
    assert guard.spent_usd == SPENT                # the money stays counted
    assert guard.released == 0                     # ambiguity NEVER releases headroom
    assert len(transport.submit_calls) == 1        # and is NEVER retried
    assert route.submits == 1


def test_connection_reset_during_submit_is_ambiguous(guard, gemini_key, tmp_path):
    transport = FakeGeminiTransport(submit=ConnectionResetError(54, "reset by peer"))
    outcome, _ = run(transport, guard, tmp_path)
    assert outcome["attempt"]["status"] == "error"
    assert outcome["attempt"]["error_class"] == "connection_reset"
    assert outcome["attempt"]["ambiguous_dispatch"] is True
    assert guard.spent_usd == SPENT


def test_malformed_submit_acknowledgement_is_ambiguous(guard, gemini_key, tmp_path):
    """200 with no operation name: the job may exist, but nothing can track it."""
    transport = FakeGeminiTransport(submit=(200, {"unexpected": "shape"}))
    outcome, _ = run(transport, guard, tmp_path)
    a = outcome["attempt"]
    assert a["status"] == "error"
    assert a["error_class"] == "malformed_response"
    assert a["ambiguous_dispatch"] is True
    assert a["outcome_resolved"] is False
    assert guard.spent_usd == SPENT


def test_undocumented_operation_shape_stops_conservatively(guard, gemini_key, tmp_path):
    transport = FakeGeminiTransport(polls=[(200, ["not", "an", "operation"])])
    outcome, _ = run(transport, guard, tmp_path)
    a = outcome["attempt"]
    assert a["error_class"] == "malformed_response"
    assert a["outcome_resolved"] is False
    assert len(transport.poll_calls) == 1          # stopped at the first breach; no loop
    assert guard.spent_usd == SPENT


# ------------------------------------------------------------ post-submit lifecycle loss
def test_poll_network_failure_never_resubmits(guard, gemini_key, tmp_path):
    transport = FakeGeminiTransport(polls=[TimeoutError("poll timed out")])
    outcome, route = run(transport, guard, tmp_path)
    a = outcome["attempt"]
    assert a["status"] == "timeout"
    assert a["error_class"] == "poll_read_timeout"
    assert a["operation_name"] == OPERATION_NAME     # the operation EXISTS; id preserved
    assert a["outcome_resolved"] is False            # it may complete and bill
    assert len(transport.submit_calls) == 1          # no re-submit, ever
    assert guard.spent_usd == SPENT


def test_poll_http_error_is_unresolved_not_retried(guard, gemini_key, tmp_path):
    transport = FakeGeminiTransport(polls=[(500, {"error": {"message": "backend"}})])
    outcome, _ = run(transport, guard, tmp_path)
    assert outcome["attempt"]["error_class"] == "poll_http_500"
    assert outcome["attempt"]["outcome_resolved"] is False
    assert len(transport.submit_calls) == 1
    assert guard.spent_usd == SPENT


def test_poll_budget_exhaustion_is_a_timeout_not_a_retry(guard, gemini_key, tmp_path):
    transport = FakeGeminiTransport(
        polls=[(200, {"name": OPERATION_NAME, "done": False})])
    outcome, route = run(transport, guard, tmp_path, max_status_checks=3)
    a = outcome["attempt"]
    assert a["status"] == "timeout"
    assert a["error_class"] == "poll_budget_exhausted"
    assert a["status_checks"] == 3
    assert a["outcome_resolved"] is False
    assert len(transport.submit_calls) == 1
    assert guard.spent_usd == SPENT


def test_artifact_download_failure_keeps_generation_billed_and_uri_recorded(
        guard, gemini_key, tmp_path):
    transport = FakeGeminiTransport(artifact=TimeoutError("download stalled"))
    outcome, _ = run(transport, guard, tmp_path)
    a = outcome["attempt"]
    assert a["status"] == "error"
    assert a["error_class"] == "artifact_download_failed"
    assert a["artifact_uri"] == VIDEO_URI            # recorded for a later authorised fetch
    assert outcome["artifact"] is None
    assert guard.spent_usd == SPENT                  # the generation happened; it is paid
    assert len(transport.bytes_calls) == 1           # one fetch, no auto re-fetch


def test_download_http_error_is_counted_once(guard, gemini_key, tmp_path):
    transport = FakeGeminiTransport(artifact=(404, b"", None))
    outcome, _ = run(transport, guard, tmp_path)
    assert outcome["attempt"]["error_class"] == "artifact_download_failed"
    assert len(transport.bytes_calls) == 1
    assert guard.spent_usd == SPENT


# ------------------------------------------------------------------------- zero retries
def test_zero_client_retries_even_when_a_second_call_would_succeed(guard, gemini_key,
                                                                   tmp_path):
    """A transport that would succeed on call two never GETS a call two."""

    class FlakyThenFine(FakeGeminiTransport):
        def post_json(self, url, headers, payload):
            if not self.submit_calls:
                self.submit_calls.append((url, dict(headers), payload))
                raise socket.timeout("first call times out")
            return super().post_json(url, headers, payload)

    transport = FlakyThenFine()
    outcome, route = run(transport, guard, tmp_path)
    assert len(transport.submit_calls) == 1
    assert route.submits == 1
    assert outcome["attempt"]["status"] == "timeout"
    assert outcome["attempt"]["retries"] == 0


def test_no_network_fixture_actually_bites():
    """Sanity: the autouse fixture makes a real connection attempt raise."""
    with pytest.raises(Exception, match="injected fake transport"):
        socket.create_connection(("example.com", 443), timeout=1)
