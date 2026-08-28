"""Dispatch gating: transport, guard, key, budget ceiling, and PILOT-001 spend authority.

Each gate is tested by COUNTING CALLS on the fake transport. "Nothing was dispatched" is a
measurement here, not a claim. The spend-authority tests prove the Controller's corrected
requirement: a locally authored YAML file can never manufacture authority — only a
committed Controller decision carrying a valid machine_authorisation block, matched by the
local runtime file, opens a guard; and no such committed decision exists today.
"""
import textwrap
from decimal import Decimal
from pathlib import Path

import pytest

import pilot_authorisation as PA
from budget_guard import NotAuthorised
from providers import DispatchRefused, PreDispatchRefusal
from video_route import GeminiVeoRoute, generate_pilot_video


def test_no_transport_refuses_dispatch(guard, tmp_path):
    route = GeminiVeoRoute(guard=guard)          # transport defaults to None
    with pytest.raises(DispatchRefused, match="no transport"):
        route.generate("prompt", 8, "9:16", tmp_path)
    assert guard.reservations == []


def test_no_guard_refuses_dispatch(transport, tmp_path):
    route = GeminiVeoRoute(transport=transport)
    with pytest.raises(DispatchRefused, match="no budget guard"):
        route.generate("prompt", 8, "9:16", tmp_path)
    assert transport.submit_calls == []


def test_missing_key_is_provably_predispatch_and_releases_reservation(
        guard, transport, tmp_path):
    # conftest strips GEMINI_API_KEY; nothing sets it here.
    route = GeminiVeoRoute(transport=transport, guard=guard)
    with pytest.raises(PreDispatchRefusal, match="GEMINI_API_KEY"):
        route.generate("prompt", 8, "9:16", tmp_path)
    assert transport.submit_calls == []            # proven: zero network calls
    assert guard.reservations == [Decimal("0.80")]  # it WAS reserved first...
    assert guard.released == 1                     # ...and released on proven non-dispatch
    assert guard.spent_usd == Decimal("0")


def test_auth_header_shape_and_key_read_at_dispatch_only(guard, transport, gemini_key,
                                                         tmp_path):
    route = GeminiVeoRoute(transport=transport, guard=guard)
    route.generate("prompt", 8, "9:16", tmp_path)
    (url, headers, payload) = transport.submit_calls[0]
    assert headers == {"x-goog-api-key": gemini_key}   # documented Gemini API auth header
    # polls and the artifact download authenticate the same way
    assert all(h == {"x-goog-api-key": gemini_key}
               for (_, h) in transport.bytes_calls)


def test_key_never_enters_payload_or_persisted_records(guard, transport, gemini_key,
                                                       tmp_path):
    import json

    route = GeminiVeoRoute(transport=transport, guard=guard)
    outcome = route.generate("prompt", 8, "9:16", tmp_path)
    (_, _, payload) = transport.submit_calls[0]
    assert gemini_key.encode() not in payload
    assert gemini_key not in json.dumps(outcome["attempt"])
    assert gemini_key not in json.dumps(outcome["artifact"])
    # the persisted request-config file must not carry it either
    config = Path(outcome["attempt"]["config_location"]).read_text(encoding="utf-8")
    assert gemini_key not in config


def test_budget_ceiling_blocks_dispatch_before_send(transport, gemini_key, tmp_path):
    from conftest import RecordingGuard
    from budget_guard import BudgetExceeded

    tiny = RecordingGuard(ceiling="0.50")          # an 8s call needs 0.80
    route = GeminiVeoRoute(transport=transport, guard=tiny)
    with pytest.raises(BudgetExceeded):
        route.generate("prompt", 8, "9:16", tmp_path)
    assert transport.submit_calls == []            # refused BEFORE the send


def test_thin_pilot_interface_is_gated_the_same_way(transport, tmp_path):
    with pytest.raises(DispatchRefused):
        generate_pilot_video("p", 8, "9:16", tmp_path, guard=None, transport=transport)
    assert transport.submit_calls == []


# ================================================== PILOT-001 spend authority chain
LOCAL_OK = {
    "authorised": True,
    "tranche_id": "PILOT-001",
    "max_consumed_api_spend_usd": 5.00,
    "retries_authorised": 0,
    "approved_by": "test-fixture",
    "approved_at": "2026-08-28",
}

COMMITTED_BLOCK = textwrap.dedent("""\
    # Controller — synthetic test decision (test fixture, not real authority)

    ```yaml
    machine_authorisation:
      tranche_id: PILOT-001
      authorised: true
      max_consumed_api_spend_usd: 5.00
      retries_authorised: 0
      approved_by: test-controller
      approved_at: "2026-08-28"
    ```
    """)


def _write_local(tmp_path, decision_ref=None, **mutation):
    import yaml

    data = dict(LOCAL_OK)
    if decision_ref:
        data["decision_ref"] = decision_ref
    data.update(mutation)
    path = tmp_path / "auth.yaml"
    path.write_text(yaml.safe_dump(data), encoding="utf-8")
    return path


def test_current_committed_repository_state_cannot_open_a_paid_guard(tmp_path):
    """THE decisive test: even a perfectly-formed local file is refused today, because no
    committed Controller decision carries a machine_authorisation block for PILOT-001."""
    local = _write_local(tmp_path)
    with pytest.raises(NotAuthorised, match="no committed Controller decision"):
        PA.open_pilot_guard(local)                 # real DECISIONS_DIR, real repo state


def test_no_committed_decision_currently_carries_pilot_authority():
    authority, refusals = PA.find_committed_authority()
    assert authority is None
    assert any("has not been authorised" in r for r in refusals)


def test_default_paths_fail_closed_with_no_local_file():
    with pytest.raises(NotAuthorised, match="PILOT-001"):
        PA.open_pilot_guard()


def test_referencing_an_existing_but_non_authorising_decision_is_refused(tmp_path):
    """The first-pass hole, closed: pointing at a real committed decision that does NOT
    carry a machine_authorisation block manufactures nothing."""
    local = _write_local(
        tmp_path,
        decision_ref=("coordination/decisions/"
                      "CONTROLLER-REVISED-PROGRAM-AND-PREPILOT-TRANCHE-2026-08-28.md"))
    with pytest.raises(NotAuthorised, match="no machine_authorisation block"):
        PA.open_pilot_guard(local)


def test_valid_chain_opens_a_guard_only_when_committed_authority_exists(tmp_path):
    """The format works end-to-end — against a SYNTHETIC decisions dir, never the repo."""
    decisions = tmp_path / "decisions"
    decisions.mkdir()
    (decisions / "CONTROLLER-TEST-PILOT-SPEND.md").write_text(COMMITTED_BLOCK,
                                                              encoding="utf-8")
    local = _write_local(tmp_path,
                         decision_ref=str(decisions / "CONTROLLER-TEST-PILOT-SPEND.md"))
    g = PA.open_pilot_guard(local, decisions_dir=decisions)
    assert g.authorised_usd == Decimal("5")
    assert g.spent_usd == Decimal("0")


@pytest.mark.parametrize("mutation,expected", [
    ({"authorised": "true"}, "not the boolean true"),
    ({"tranche_id": "EMP-001"}, "expected 'PILOT-001'"),
    ({"max_consumed_api_spend_usd": 0}, "authorises nothing"),
    ({"max_consumed_api_spend_usd": 6.00}, "exceeds the committed authorised cap"),
    ({"retries_authorised": 1}, "exactly 0"),
    ({"approved_by": None}, "approved_by is missing"),
])
def test_local_file_defects_refused_even_with_committed_authority(tmp_path, mutation,
                                                                  expected):
    decisions = tmp_path / "decisions"
    decisions.mkdir()
    decision = decisions / "CONTROLLER-TEST-PILOT-SPEND.md"
    decision.write_text(COMMITTED_BLOCK, encoding="utf-8")
    local = _write_local(tmp_path, decision_ref=str(decision), **mutation)
    with pytest.raises(NotAuthorised) as exc:
        PA.open_pilot_guard(local, decisions_dir=decisions)
    assert expected in str(exc.value)


def _committed_decision_text(**overrides):
    fields = {"tranche_id": "PILOT-001", "authorised": "true",
              "max_consumed_api_spend_usd": "5.00", "retries_authorised": "0",
              "approved_by": "test-controller", "approved_at": '"2026-08-28"'}
    fields.update(overrides)
    lines = "\n".join(f"  {k}: {v}" for k, v in fields.items())
    return ("# Controller — synthetic test decision (test fixture, not real authority)\n\n"
            f"```yaml\nmachine_authorisation:\n{lines}\n```\n")


@pytest.mark.parametrize("overrides,expected", [
    ({}, None),                                                   # control: valid chain
    ({"authorised": '"true"'}, "not the boolean true"),
    ({"tranche_id": "EMP-001"}, "expected 'PILOT-001'"),
    ({"retries_authorised": "2"}, "authorises exactly 0"),
    ({"max_consumed_api_spend_usd": "0"}, "authorises nothing"),
    ({"approved_by": '""'}, "approved_by is missing"),
])
def test_committed_block_defects_refused(tmp_path, overrides, expected):
    decisions = tmp_path / "decisions"
    decisions.mkdir()
    decision = decisions / "CONTROLLER-TEST-PILOT-SPEND.md"
    decision.write_text(_committed_decision_text(**overrides), encoding="utf-8")
    local = _write_local(tmp_path, decision_ref=str(decision))
    if expected is None:
        assert PA.open_pilot_guard(local, decisions_dir=decisions)
    else:
        with pytest.raises(NotAuthorised) as exc:
            PA.open_pilot_guard(local, decisions_dir=decisions)
        assert expected in str(exc.value)


def test_two_committed_authorities_are_a_conflict_not_a_choice(tmp_path):
    decisions = tmp_path / "decisions"
    decisions.mkdir()
    (decisions / "CONTROLLER-A.md").write_text(COMMITTED_BLOCK, encoding="utf-8")
    (decisions / "CONTROLLER-B.md").write_text(COMMITTED_BLOCK, encoding="utf-8")
    local = _write_local(tmp_path, decision_ref=str(decisions / "CONTROLLER-A.md"))
    with pytest.raises(NotAuthorised, match="conflicting authority"):
        PA.open_pilot_guard(local, decisions_dir=decisions)


def test_local_decision_ref_must_name_an_actually_authorising_decision(tmp_path):
    """Naming an unrelated committed decision manufactures nothing, even while a valid
    authority exists elsewhere in the same directory."""
    decisions = tmp_path / "decisions"
    decisions.mkdir()
    (decisions / "CONTROLLER-TEST-PILOT-SPEND.md").write_text(COMMITTED_BLOCK,
                                                              encoding="utf-8")
    (decisions / "CONTROLLER-OTHER.md").write_text("# unrelated\n", encoding="utf-8")
    local = _write_local(tmp_path, decision_ref=str(decisions / "CONTROLLER-OTHER.md"))
    with pytest.raises(NotAuthorised, match="no machine_authorisation block"):
        PA.open_pilot_guard(local, decisions_dir=decisions)


def test_decision_ref_outside_the_decisions_dir_is_refused(tmp_path):
    decisions = tmp_path / "decisions"
    decisions.mkdir()
    elsewhere = tmp_path / "elsewhere.md"
    elsewhere.write_text(COMMITTED_BLOCK, encoding="utf-8")
    local = _write_local(tmp_path, decision_ref=str(elsewhere))
    with pytest.raises(NotAuthorised, match="is not under"):
        PA.open_pilot_guard(local, decisions_dir=decisions)
