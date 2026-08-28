"""THE PRIMARY ACCEPTANCE TESTS for EVAL-035: the actual production code calls the actual
production code.

No mock writer, no copied schema, no reimplemented gate, no hand-maintained field list.
These tests import the MERGED `resources/pilot-writer/outcome_writer.py` from current
main, feed it EVAL-035's cost and attempt handoffs verbatim, and run the MERGED v3
topology validator (subprocess, exactly as RES-007's own tests invoke it) over the
resulting archive. If the merged Resources interface or validator contract ever changes
incompatibly, these tests fail — that failure is their purpose; nothing here shields
them from interface drift.
"""
import importlib.util
import json
import socket
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

import pytest

import pilot_spend_ledger as SL
from conftest import (MP4_FIXTURE_BYTES, FakeGeminiTransport, fixed_clock,
                      make_pilot_authority)
from video_route import (GeminiVeoRoute, res007_cost_ledger_entry,
                         res007_production_attempt)

REPO_ROOT = Path(__file__).resolve().parents[3]
WRITER_PATH = REPO_ROOT / "resources" / "pilot-writer" / "outcome_writer.py"
VALIDATOR_PATH = (REPO_ROOT / "resources" / "pre-execution-freeze" / "validators"
                  / "validate_topology_v3.py")

# Import the MERGED writer module by its real path (the directory name is hyphenated, so
# a dotted import cannot address it — same resolution the repo uses elsewhere).
_spec = importlib.util.spec_from_file_location("res007_outcome_writer", WRITER_PATH)
outcome_writer = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(outcome_writer)
OutcomeWriter = outcome_writer.OutcomeWriter

T0 = "2026-08-28T09:00:00Z"


def run_validator(archive_path: Path) -> subprocess.CompletedProcess:
    """Run the MERGED v3 topology validator exactly as shipped. Exit 0 = valid."""
    return subprocess.run([sys.executable, str(VALIDATOR_PATH), str(archive_path)],
                          capture_output=True, text=True, timeout=120)


def pilot_route(tmp_path, transport):
    """A route wired to the PERSISTENT pilot ledger via a synthetic authority chain, so
    the settled attempt carries a durable, Resources-resolvable cost_ref."""
    local, decisions = make_pilot_authority(tmp_path, cap="5.00")
    budget = SL.open_pilot_runtime(tmp_path / "runs", "run-int-1",
                                   authorisation_path=local, decisions_dir=decisions)
    return GeminiVeoRoute(transport=transport, guard=budget, clock=fixed_clock()), budget


def minimal_journey(writer: OutcomeWriter):
    """The minimum real v3 objects a provider attempt hangs from."""
    writer.add_job("JOB-E35", T0, "BRIEF-E35-TEST", "req_lin_eval035_integration_test")
    writer.add_outcome("OUT-E35", "JOB-E35", "video_asset", T0)
    writer.add_set("SET-E35", "OUT-E35", "unordered", "multi_format_set")
    writer.add_unit("U-PLATE", "SET-E35", "shot")
    writer.add_provider_step("ST-GEN", "U-PLATE", "provider_generation", 0, T0)
    return "ST-GEN"


def test_successful_route_outcome_flows_through_the_merged_writer_and_validator(
        tmp_path, gemini_key):
    # 1-2. fake Gemini transport -> EVAL-035 route, spending against the persistent ledger
    route, budget = pilot_route(tmp_path, FakeGeminiTransport())
    outcome = route.generate("A festive premium 9:16 motion plate", 8, "9:16",
                             tmp_path / "out")
    assert outcome["attempt"]["status"] == "ok"

    # 3-4. the minimum real journey and the REAL cost ledger row, added FIRST
    writer = OutcomeWriter()
    step_id = minimal_journey(writer)
    writer.add_ledger_entry(**res007_cost_ledger_entry(outcome))

    # 5-6. the EVAL-035 handoff, fed verbatim into the MERGED record_attempt
    handoff = res007_production_attempt(outcome)
    writer.record_attempt(step_id=step_id, **handoff["writer_fields"])

    # 7. the actual binary artifact, recorded from its real bytes on disk
    writer.record_artifact("art-plate", step_id, "video",
                           path=outcome["artifact"]["output_location"],
                           attempt_id=outcome["attempt"]["attempt_id"])

    # 8-10. a valid archive, judged by the MERGED topology validator
    archive_path = tmp_path / "journey" / "archive.yaml"
    writer.write_archive(str(archive_path))
    result = run_validator(archive_path)
    assert result.returncode == 0, (
        f"merged v3 validator rejected the journey:\n{result.stdout}\n{result.stderr}")

    # The cost identity is one chain end to end: pilot ledger -> attempt -> Resources row.
    archive = writer.to_archive()
    [attempt_row] = archive["attempts"]
    [ledger_row] = archive["cost_ledger"]
    assert attempt_row["cost_ref"] == ledger_row["ledger_entry_id"] \
        == outcome["attempt"]["cost_ref"]
    assert ledger_row["immutable"] is True
    assert ledger_row["cost_class"] == "api_tool"
    assert "not invoice evidence" in ledger_row["basis"]
    # and the writer recomputed the artifact hash from the same bytes we persisted
    [artifact_row] = archive["artifacts"]
    assert artifact_row["output_hash"] == outcome["artifact"]["output_sha256"]
    assert artifact_row["output_bytes"] == len(MP4_FIXTURE_BYTES)
    assert budget.committed_usd() == Decimal("0.80")


def test_ambiguous_failed_outcome_flows_through_the_merged_writer_and_validator(
        tmp_path, gemini_key):
    # An ambiguous post-dispatch failure: the submit timed out after the send began.
    route, budget = pilot_route(tmp_path,
                                FakeGeminiTransport(submit=socket.timeout("read timeout")))
    outcome = route.generate("A festive premium 9:16 motion plate", 8, "9:16",
                             tmp_path / "out")
    a = outcome["attempt"]
    assert a["status"] == "timeout"
    assert a["completed_at"] is None            # genuinely unresolved, honestly recorded
    assert outcome["artifact"] is None

    writer = OutcomeWriter()
    step_id = minimal_journey(writer)
    # The conservative cost is still a REAL immutable row with the same cost identity.
    cost_kwargs = res007_cost_ledger_entry(outcome)
    assert "conservative" in cost_kwargs["basis"]
    writer.add_ledger_entry(**cost_kwargs)

    handoff = res007_production_attempt(outcome)
    wf = handoff["writer_fields"]
    assert wf["status"] == "timeout" and wf["error_detail"]     # preserved failure facts
    writer.record_attempt(step_id=step_id, **wf)
    # No artifact is attached to a failed attempt — the merged writer enforces this too.

    archive_path = tmp_path / "journey" / "archive-failed.yaml"
    writer.write_archive(str(archive_path))
    result = run_validator(archive_path)
    assert result.returncode == 0, (
        f"merged v3 validator rejected the failed journey:\n"
        f"{result.stdout}\n{result.stderr}")

    archive = writer.to_archive()
    [attempt_row] = archive["attempts"]
    assert attempt_row["status"] == "timeout"
    assert attempt_row["completed_at"] is None
    assert attempt_row["error_detail"]
    assert attempt_row["cost_ref"] == archive["cost_ledger"][0]["ledger_entry_id"]
    assert archive["artifacts"] == []
    assert budget.committed_usd() == Decimal("0.80")   # conservative: counted, not freed


def test_merged_writer_refuses_an_artifact_on_the_failed_attempt(tmp_path, gemini_key):
    """Defence in depth is the WRITER's, not ours: attaching bytes to a failed attempt is
    refused by the merged production code itself."""
    route, _ = pilot_route(tmp_path,
                           FakeGeminiTransport(submit=socket.timeout("read timeout")))
    outcome = route.generate("p", 8, "9:16", tmp_path / "out")

    writer = OutcomeWriter()
    step_id = minimal_journey(writer)
    writer.add_ledger_entry(**res007_cost_ledger_entry(outcome))
    writer.record_attempt(step_id=step_id,
                          **res007_production_attempt(outcome)["writer_fields"])
    with pytest.raises(outcome_writer.WriterError, match="produced no artifact"):
        writer.record_artifact("art-x", step_id, "video", data=MP4_FIXTURE_BYTES,
                               output_location="x.mp4",
                               attempt_id=outcome["attempt"]["attempt_id"])


def test_validator_negative_control_detects_a_gutted_attempt(tmp_path, gemini_key):
    """Prove the subprocess validator can FAIL: an archive whose attempt loses its
    prompt_hash must exit 1, not 0. Without this control a vacuously-green validator run
    (wrong path, wrong exit-code reading) would be indistinguishable from a pass."""
    import yaml

    route, _ = pilot_route(tmp_path, FakeGeminiTransport())
    outcome = route.generate("p", 8, "9:16", tmp_path / "out")
    writer = OutcomeWriter()
    step_id = minimal_journey(writer)
    writer.add_ledger_entry(**res007_cost_ledger_entry(outcome))
    writer.record_attempt(step_id=step_id,
                          **res007_production_attempt(outcome)["writer_fields"])
    writer.record_artifact("art-plate", step_id, "video",
                           path=outcome["artifact"]["output_location"],
                           attempt_id=outcome["attempt"]["attempt_id"])
    archive = writer.to_archive()
    del archive["attempts"][0]["prompt_hash"]          # gut the G12 provenance
    bad_path = tmp_path / "journey" / "archive-bad.yaml"
    bad_path.parent.mkdir(parents=True, exist_ok=True)
    bad_path.write_text(yaml.safe_dump(archive, sort_keys=False), encoding="utf-8")
    result = run_validator(bad_path)
    assert result.returncode == 1, (
        f"validator should have failed the gutted archive:\n{result.stdout}")


def test_storage_class_kwarg_would_be_refused_by_the_merged_writer(tmp_path, gemini_key):
    """The exact first-pass defect, proven against the real interface: the merged writer
    refuses storage_class as a caller argument, so the handoff must not carry it — and
    does not."""
    route, _ = pilot_route(tmp_path, FakeGeminiTransport())
    outcome = route.generate("p", 8, "9:16", tmp_path / "out")

    writer = OutcomeWriter()
    step_id = minimal_journey(writer)
    writer.add_ledger_entry(**res007_cost_ledger_entry(outcome))
    wf = dict(res007_production_attempt(outcome)["writer_fields"])
    assert "storage_class" not in wf
    with pytest.raises(outcome_writer.WriterError, match="unknown field"):
        writer.record_attempt(step_id=step_id, **{**wf, "storage_class": "anything"})
