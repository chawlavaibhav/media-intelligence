"""Dispatch gating: transport, guard, key, budget ceiling, and PILOT-001 authorisation.

Each gate is tested by COUNTING CALLS on the fake transport. "Nothing was dispatched" is a
measurement here, not a claim.
"""
from decimal import Decimal

import pytest

import pilot_authorisation as PA
from budget_guard import NotAuthorised
from providers import DispatchRefused, PreDispatchRefusal
from video_route import PilotVideoRoute, generate_pilot_video


def test_no_transport_refuses_dispatch(guard, tmp_path):
    route = PilotVideoRoute(guard=guard)          # transport defaults to None
    with pytest.raises(DispatchRefused, match="no transport"):
        route.generate("prompt", 6, "16:9", tmp_path)
    assert guard.reservations == []


def test_no_guard_refuses_dispatch(transport, tmp_path):
    route = PilotVideoRoute(transport=transport)
    with pytest.raises(DispatchRefused, match="no budget guard"):
        route.generate("prompt", 6, "16:9", tmp_path)
    assert transport.submit_calls == []


def test_missing_key_is_provably_predispatch_and_releases_reservation(
        guard, transport, tmp_path):
    # conftest strips FAL_KEY; nothing sets it here.
    route = PilotVideoRoute(transport=transport, guard=guard)
    with pytest.raises(PreDispatchRefusal, match="FAL_KEY"):
        route.generate("prompt", 6, "16:9", tmp_path)
    assert transport.submit_calls == []            # proven: nothing was sent
    assert guard.reservations == [Decimal("2.40")]  # it WAS reserved first...
    assert guard.released == 1                     # ...and released on proven non-dispatch
    assert guard.spent_usd == Decimal("0")


def test_auth_shape_and_platform_retry_disabled(guard, transport, fal_key, tmp_path):
    """fal auth is `Authorization: Key ...`, and every submit disables fal's auto-retry."""
    route = PilotVideoRoute(transport=transport, guard=guard)
    route.generate("prompt", 6, "16:9", tmp_path)
    (url, headers, payload) = transport.submit_calls[0]
    assert headers["Authorization"] == f"Key {fal_key}"
    assert headers["X-Fal-No-Retry"] == "1"        # one submit may never fan out provider-side
    assert url == "https://queue.fal.run/fal-ai/veo3.1"


def test_key_never_enters_payload_or_persisted_records(guard, transport, fal_key, tmp_path):
    import json

    route = PilotVideoRoute(transport=transport, guard=guard)
    outcome = route.generate("prompt", 6, "16:9", tmp_path)
    (_, _, payload) = transport.submit_calls[0]
    assert fal_key.encode() not in payload
    assert fal_key not in json.dumps(outcome["attempt"])
    assert fal_key not in json.dumps(outcome["artifact"])


def test_budget_ceiling_blocks_dispatch_before_send(transport, fal_key, tmp_path):
    from conftest import RecordingGuard
    from budget_guard import BudgetExceeded

    tiny = RecordingGuard(ceiling="1.00")          # a 6s call needs 2.40
    route = PilotVideoRoute(transport=transport, guard=tiny)
    with pytest.raises(BudgetExceeded):
        route.generate("prompt", 6, "16:9", tmp_path)
    assert transport.submit_calls == []            # refused BEFORE the send


# ------------------------------------------------------- PILOT-001 authorisation gate
def test_pilot_guard_fails_closed_with_no_file(tmp_path):
    with pytest.raises(NotAuthorised, match="PILOT-001"):
        PA.open_pilot_guard(tmp_path / "does-not-exist.yaml")


def test_default_pilot_authorisation_path_is_refused_today():
    """The committed repository state must never permit pilot spend."""
    status = PA.load_pilot_authorisation()
    assert status["refusals"]                       # refused, with reasons


@pytest.mark.parametrize("mutation,expected", [
    ({"authorised": "true"}, "not the boolean true"),
    ({"tranche_id": "EMP-001"}, "expected 'PILOT-001'"),
    ({"max_consumed_api_spend_usd": 0}, "authorises nothing"),
    ({"max_consumed_api_spend_usd": "lots"}, "not a number"),
    ({"retries_authorised": 1}, "exactly 0"),
    ({"approved_by": None}, "approved_by is missing"),
    ({"decision_ref": None}, "decision_ref is missing"),
    ({"decision_ref": "eval/CHARTER.md"}, "not under coordination/decisions/"),
    ({"decision_ref": "coordination/decisions/DOES-NOT-EXIST.md"}, "does not exist"),
])
def test_pilot_authorisation_refuses_each_defect(tmp_path, mutation, expected):
    import yaml

    base = {
        "authorised": True,
        "tranche_id": "PILOT-001",
        "max_consumed_api_spend_usd": 5.00,
        "retries_authorised": 0,
        "approved_by": "test-fixture",
        "approved_at": "2026-08-28",
        "decision_ref": ("coordination/decisions/"
                         "CONTROLLER-REVISED-PROGRAM-AND-PREPILOT-TRANCHE-2026-08-28.md"),
    }
    base.update(mutation)
    path = tmp_path / "auth.yaml"
    path.write_text(yaml.safe_dump(base), encoding="utf-8")
    with pytest.raises(NotAuthorised) as exc:
        PA.open_pilot_guard(path)
    assert expected in str(exc.value)


def test_mechanically_valid_file_opens_a_decimal_guard(tmp_path):
    """The loader's mechanics work end-to-end. This is NOT spend authority: the runner at
    pilot time must still verify the referenced decision's content approves the cap."""
    import yaml

    path = tmp_path / "auth.yaml"
    path.write_text(yaml.safe_dump({
        "authorised": True, "tranche_id": "PILOT-001",
        "max_consumed_api_spend_usd": 5.00, "retries_authorised": 0,
        "approved_by": "test-fixture", "approved_at": "2026-08-28",
        "decision_ref": ("coordination/decisions/"
                         "CONTROLLER-REVISED-PROGRAM-AND-PREPILOT-TRANCHE-2026-08-28.md"),
    }), encoding="utf-8")
    g = PA.open_pilot_guard(path)
    assert g.authorised_usd == Decimal("5")
    assert g.spent_usd == Decimal("0")


def test_thin_pilot_interface_is_gated_the_same_way(transport, tmp_path):
    with pytest.raises(DispatchRefused):
        generate_pilot_video("p", 6, "16:9", tmp_path, guard=None, transport=transport)
    assert transport.submit_calls == []
