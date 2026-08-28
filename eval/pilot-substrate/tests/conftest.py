"""Test plumbing for the EVAL-035 pilot video-route substrate.

Two jobs:

1. Make the hyphenated package directories importable (the same resolution the EMP-001
   tests use — the directory name is authoritative, the dotted import form is not).
2. Make it STRUCTURALLY impossible for any test to reach a network: an autouse fixture
   replaces socket connection primitives with ones that raise. "No network call occurs
   during normal tests" is enforced here as a measurement, not asserted as a promise.
   The fixture also strips FAL_KEY from the environment so a developer machine that holds
   a real key can never leak it into a test run.
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
    monkeypatch.delenv("FAL_KEY", raising=False)


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


class FakeQueueTransport:
    """Deterministic provider-shaped queue lifecycle. Counts everything, opens nothing.

    Each scripted step is either a (status_code, body) tuple or an Exception instance to
    raise — which is exactly where a real socket failure would surface.
    """

    def __init__(self, submit=None, statuses=None, result=None, artifact=None):
        self.submit = submit if submit is not None else (
            200, {"request_id": "fal-q-0001",
                  "status_url": "https://queue.fal.run/fal-ai/veo3.1/requests/fal-q-0001/status",
                  "response_url": "https://queue.fal.run/fal-ai/veo3.1/requests/fal-q-0001",
                  "queue_position": 0})
        self.statuses = statuses if statuses is not None else [
            (200, {"status": "IN_QUEUE", "request_id": "fal-q-0001", "queue_position": 0}),
            (200, {"status": "IN_PROGRESS", "request_id": "fal-q-0001", "logs": []}),
            (200, {"status": "COMPLETED", "request_id": "fal-q-0001", "logs": [],
                   "metrics": {"inference_time": 41.0}}),
        ]
        self.result = result if result is not None else (
            200, {"video": {"url": "https://v3.fal.media/files/fake/pilot-0001.mp4",
                            "content_type": "video/mp4",
                            "file_name": "pilot-0001.mp4",
                            "file_size": len(MP4_FIXTURE_BYTES)}})
        self.artifact = artifact if artifact is not None else (200, MP4_FIXTURE_BYTES)
        self.submit_calls: list[tuple] = []
        self.status_calls: list[str] = []
        self.result_calls: list[str] = []
        self.bytes_calls: list[str] = []

    @staticmethod
    def _play(step):
        if isinstance(step, BaseException):
            raise step
        return step

    def post_json(self, url, headers, payload):
        self.submit_calls.append((url, dict(headers), payload))
        return self._play(self.submit)

    def get_json(self, url, headers):
        if url.endswith("/status"):
            self.status_calls.append(url)
            i = min(len(self.status_calls) - 1, len(self.statuses) - 1)
            return self._play(self.statuses[i])
        self.result_calls.append(url)
        return self._play(self.result)

    def get_bytes(self, url, headers):
        self.bytes_calls.append(url)
        return self._play(self.artifact)


# Binary fixture: an MP4-shaped header followed by bytes that are INVALID UTF-8 — 0xFF/0xFE
# never begin a UTF-8 sequence, and 0x80 without a lead byte is malformed. Any code path
# that treats this payload as text raises immediately instead of quietly mangling it.
MP4_FIXTURE_BYTES = (b"\x00\x00\x00\x18ftypmp42\x00\x00\x00\x00mp42isom"
                     + b"\xff\xfe\x80\x81\xc0\x00" * 100)


@pytest.fixture
def transport():
    return FakeQueueTransport()


@pytest.fixture
def fal_key(monkeypatch):
    monkeypatch.setenv("FAL_KEY", "test-key-not-a-real-credential")
    return "test-key-not-a-real-credential"
