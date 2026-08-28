"""Test plumbing for the EVAL-035 pilot video-route substrate (direct Gemini/Veo).

Two jobs:

1. Make the hyphenated package directories importable (the same resolution the EMP-001
   tests use — the directory name is authoritative, the dotted import form is not).
2. Make it STRUCTURALLY impossible for any test to reach a network: an autouse fixture
   replaces socket connection primitives with ones that raise. "No network call occurs
   during normal tests" is enforced here as a measurement, not asserted as a promise.
   The fixture also strips GEMINI_API_KEY from the environment so a developer machine
   that holds a real key can never leak it into a test run.
"""
from __future__ import annotations

import socket
import sys
from decimal import Decimal
from pathlib import Path

import pytest

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
EMP001 = PACKAGE_ROOT.parent / "empirical-tranche-1"
for p in (str(PACKAGE_ROOT), str(EMP001)):
    if p not in sys.path:
        sys.path.insert(0, p)

from budget_guard import BudgetGuard  # noqa: E402

OPERATION_NAME = ("models/veo-3.1-fast-generate-preview/operations/fake-op-0001")
VIDEO_URI = ("https://generativelanguage.googleapis.com/v1beta/files/fake-file-0001:download"
             "?alt=media")


class NetworkAttempted(RuntimeError):
    """A test tried to open a real socket. That is a test failure by definition."""


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    def explode(*args, **kwargs):
        raise NetworkAttempted(
            "a test attempted a real network connection; every dispatch in this package "
            "must go through an injected fake transport")

    monkeypatch.setattr(socket.socket, "connect", explode)
    monkeypatch.setattr(socket, "create_connection", explode)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)


class RecordingGuard(BudgetGuard):
    """EMP-001's real Decimal guard, plus counters so tests can see what happened to it."""

    def __init__(self, ceiling: str = "10.00"):
        super().__init__(authorised_usd=Decimal(ceiling))
        self.released = 0
        self.reservations: list[Decimal] = []
        self.records: list[Decimal] = []

    def reserve(self, estimated_usd: Decimal) -> None:
        super().reserve(estimated_usd)
        self.reservations.append(estimated_usd)

    def record(self, actual_usd: Decimal) -> None:
        super().record(actual_usd)
        self.records.append(actual_usd)

    def release(self) -> None:
        self.released += 1


@pytest.fixture
def guard():
    return RecordingGuard()


class FakeGeminiTransport:
    """Deterministic provider-shaped long-running-operation lifecycle. Opens nothing.

    Each scripted step is either a return value or an Exception instance to raise — which
    is exactly where a real socket failure would surface.

      submit    (status_code, body) for POST :predictLongRunning
      polls     list of (status_code, operation_json) for GET <operation name>
      artifact  (status_code, bytes, content_type) for GET <video uri>
    """

    def __init__(self, submit=None, polls=None, artifact=None):
        self.submit = submit if submit is not None else (200, {"name": OPERATION_NAME})
        self.polls = polls if polls is not None else [
            (200, {"name": OPERATION_NAME, "done": False}),
            (200, {"name": OPERATION_NAME, "done": False,
                   "metadata": {"state": "PROCESSING"}}),
            (200, {"name": OPERATION_NAME, "done": True,
                   "response": {"generateVideoResponse": {
                       "generatedSamples": [{"video": {"uri": VIDEO_URI}}]}}}),
        ]
        self.artifact = artifact if artifact is not None else (
            200, MP4_FIXTURE_BYTES, "video/mp4")
        self.submit_calls: list[tuple] = []
        self.poll_calls: list[str] = []
        self.bytes_calls: list[tuple] = []

    @staticmethod
    def _play(step):
        if isinstance(step, BaseException):
            raise step
        return step

    def post_json(self, url, headers, payload):
        self.submit_calls.append((url, dict(headers), payload))
        return self._play(self.submit)

    def get_json(self, url, headers):
        self.poll_calls.append(url)
        i = min(len(self.poll_calls) - 1, len(self.polls) - 1)
        return self._play(self.polls[i])

    def get_bytes(self, url, headers):
        self.bytes_calls.append((url, dict(headers)))
        return self._play(self.artifact)


# Binary fixture: an MP4-shaped header followed by bytes that are INVALID UTF-8 — 0xFF/0xFE
# never begin a UTF-8 sequence, and 0x80 without a lead byte is malformed. Any code path
# that treats this payload as text raises immediately instead of quietly mangling it.
MP4_FIXTURE_BYTES = (b"\x00\x00\x00\x18ftypmp42\x00\x00\x00\x00mp42isom"
                     + b"\xff\xfe\x80\x81\xc0\x00" * 100)


@pytest.fixture
def transport():
    return FakeGeminiTransport()


@pytest.fixture
def gemini_key(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key-not-a-real-credential")
    return "test-key-not-a-real-credential"


def make_pilot_authority(tmp_path, cap: str = "5.00"):
    """A complete SYNTHETIC authority chain in tmp_path: a decisions dir holding one
    Controller-format decision with a valid machine_authorisation block, plus a matching
    local runtime file. Test fixture only — never the repository's decisions directory,
    which (correctly) authorises nothing today."""
    import yaml

    decisions = tmp_path / "decisions"
    decisions.mkdir(exist_ok=True)
    decision = decisions / "CONTROLLER-TEST-PILOT-SPEND.md"
    decision.write_text(
        "# Controller — synthetic test decision (test fixture, not real authority)\n\n"
        "```yaml\n"
        "machine_authorisation:\n"
        "  tranche_id: PILOT-001\n"
        "  authorised: true\n"
        f"  max_consumed_api_spend_usd: {cap}\n"
        "  retries_authorised: 0\n"
        "  approved_by: test-controller\n"
        "  approved_at: \"2026-08-28\"\n"
        "```\n", encoding="utf-8")
    local = tmp_path / "authorization.pilot.local.yaml"
    local.write_text(yaml.safe_dump({
        "authorised": True, "tranche_id": "PILOT-001",
        "max_consumed_api_spend_usd": float(cap), "retries_authorised": 0,
        "approved_by": "test-fixture", "approved_at": "2026-08-28",
        "decision_ref": str(decision)}), encoding="utf-8")
    return local, decisions


def fixed_clock():
    """Deterministic injected clock: monotonic fake ISO timestamps."""
    state = {"t": 0}

    def tick():
        state["t"] += 1
        return f"2026-08-28T00:00:{state['t']:02d}Z"

    return tick
