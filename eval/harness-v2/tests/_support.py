"""Test plumbing for eval/harness-v2 (stdlib unittest).

Two jobs, copied in spirit from eval/pilot-substrate/tests/conftest.py:

1. Put eval/harness-v2 on sys.path so modules import by their own names.
2. Make it STRUCTURALLY impossible for a test to reach a network or a real key:
   `NoNetworkTestCase.setUp` replaces socket connection primitives and urllib.request.urlopen
   with functions that raise, strips every provider key name from the environment, and points
   the adapters' key loader at a throw-away file. A test that wants a key value writes a canary
   into that file - never the real ~/.mi-keys.
"""
from __future__ import annotations

import os
import socket
import sys
import tempfile
import unittest
import urllib.request
from decimal import Decimal
from pathlib import Path

HV2 = Path(__file__).resolve().parents[1]
if str(HV2) not in sys.path:
    sys.path.insert(0, str(HV2))

import hv2_paths  # noqa: E402,F401

KEY_NAMES = ("FAL_KEY", "SARVAM_API_KEY", "GOOGLE_API_KEY", "GEMINI_API_KEY", "ANTHROPIC_API_KEY",
             "GOOGLE_CLOUD_VISION_API_KEY")


class NetworkAttempted(RuntimeError):
    """A test tried to open a real socket. That is a test failure by definition."""


def _explode(*args, **kwargs):
    raise NetworkAttempted("a test attempted a real network connection; every dispatch must go "
                           "through an injected fake transport")


class NoNetworkTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self._saved = {
            "connect": socket.socket.connect, "create_connection": socket.create_connection,
            "urlopen": urllib.request.urlopen, "env": {k: os.environ.get(k) for k in KEY_NAMES},
        }
        socket.socket.connect = _explode
        socket.create_connection = _explode
        urllib.request.urlopen = _explode
        for k in KEY_NAMES:
            os.environ.pop(k, None)
        self.tmp = Path(tempfile.mkdtemp(prefix="hv2-test-"))
        self.key_file = self.tmp / "fake-keys"          # a throw-away key file, never ~/.mi-keys
        self.key_file.write_text("")
        import adapters.base as B
        self._saved_key_file = B.DEFAULT_KEY_FILE
        B.DEFAULT_KEY_FILE = self.key_file

    def tearDown(self):
        socket.socket.connect = self._saved["connect"]
        socket.create_connection = self._saved["create_connection"]
        urllib.request.urlopen = self._saved["urlopen"]
        for k, v in self._saved["env"].items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        import adapters.base as B
        B.DEFAULT_KEY_FILE = self._saved_key_file
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)
        super().tearDown()

    # -- helpers ---------------------------------------------------------------------------
    def write_fake_key(self, name: str, value: str) -> None:
        with self.key_file.open("a") as fh:
            fh.write(f"export {name}={value}\n")

    def write_auth(self, ceiling="200.00", caps=("85.00", "115.00"), inr_cap="5.00", name="auth.yaml", **overrides):
        """A TEST-ONLY authorisation file in the signed record's machine_authorisation shape."""
        import hashlib
        fields = {
            "tranche_id": "EVAL-040-TRANCHE-1", "authorised": True, "item_basis_commit": "0596aa2",
            "price_basis_roster_sha256": hashlib.sha256(Path(hv2_paths.ROSTER).read_bytes()).hexdigest(),
            "max_consumed_usd_equivalent": ceiling, "cap_1a_usd": caps[0], "cap_1b_usd": caps[1], "sarvam_cap_inr": inr_cap,
            "retries_authorised": 0, "execution_time_route_price_verification": "required_before_every_paid_call",
            "images_before_video": True, "approved_by": "test-fixture", "approved_at": "2026-09-05T00:00:00Z",
        }
        fields.update(overrides)
        import yaml
        auth_path = self.tmp / name
        auth_path.write_text(yaml.safe_dump({"machine_authorisation": fields}, sort_keys=False))
        return auth_path

    def make_ledger(self, ceiling="200.00", caps=("85.00", "115.00"), run_id="run-test", inr_cap="5.00"):
        import ledger as L
        auth_path = self.write_auth(ceiling, caps, inr_cap)
        auth = L.load_battery_authorisation(auth_path)
        run = L.BatteryRun.create(self.tmp / "runs", run_id, auth, mode="fake_live")
        return L.BatteryBudget(run)


def fixed_clock():
    state = {"t": 0}

    def tick():
        state["t"] += 1
        return f"2026-09-05T00:00:{state['t']:02d}Z"
    return tick


# Binary fixtures: invalid UTF-8 on purpose so any text path fails loudly.
MP4_FIXTURE = b"\x00\x00\x00\x18ftypmp42\x00\x00\x00\x00mp42isom" + b"\xff\xfe\x80\x81\xc0\x00" * 100
PNG_FIXTURE = b"\x89PNG\r\n\x1a\n" + b"\xff\xfe\x80\x81" * 64
WAV_FIXTURE = b"RIFF\x24\x00\x00\x00WAVEfmt " + b"\xff\xfe\x80\x81" * 32
D = Decimal
