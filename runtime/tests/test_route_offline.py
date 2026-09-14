"""ZERO SPEND, proved rather than asserted: `--plan` opens no socket.

The first test replaces `socket.socket` and every other way out of the process with a stub that
raises, and then plans every fixture. The second does the same in a FRESH interpreter, before any
router module is imported, so that even the import of the harness's pricing and surface modules
happens under the exploding stub. If any line of this package — or of the harness code it wraps —
tried to reach a provider, the test would fail rather than cost money.
"""
from __future__ import annotations

import http.client
import socket
import ssl
import subprocess
import sys
import tempfile
import textwrap
import unittest
import urllib.request
from pathlib import Path

import _bootstrap as B

STUB_SCRIPT = textwrap.dedent('''
    import http.client, socket, ssl, sys, urllib.request
    from pathlib import Path

    class NetworkAttempted(AssertionError):
        pass

    def boom(*a, **k):
        raise NetworkAttempted("planning tried to open a connection")

    class ExplodingSocket:
        def __init__(self, *a, **k):
            boom()

    socket.socket = ExplodingSocket
    socket.create_connection = boom
    socket.socketpair = boom
    socket.getaddrinfo = boom
    ssl.SSLContext.wrap_socket = boom
    http.client.HTTPConnection.__init__ = boom
    http.client.HTTPSConnection.__init__ = boom
    urllib.request.urlopen = boom

    root = Path(sys.argv[1])
    sys.path.insert(0, str(root))
    from decimal import Decimal
    from runtime.route.cli import build_router, _profile
    from runtime.route.spec import load_spec

    router, ev, _ = build_router(root)
    planned = 0
    for spec_path in sorted((root / "runtime" / "route" / "fixtures").glob("SPEC-*.yaml")):
        for profile_name in ("alpha_human_release", "alpha_wider_example", "dry"):
            d = router.plan(load_spec(spec_path), _profile(ev, profile_name),
                            already_committed_usd=Decimal("0"), customer_ref="acct-test")
            assert d["schema"] == "ROUTE-DECISION-v0"
            assert d["provenance"]["dispatched"] is False
            planned += 1
    print("PLANNED", planned)
''')


class NoSocketDuringPlanning(unittest.TestCase):
    def test_planning_in_this_process_opens_nothing(self):
        calls = []

        def boom(*a, **k):
            calls.append(a)
            raise AssertionError("planning tried to open a connection")

        class ExplodingSocket:
            def __init__(self, *a, **k):
                boom(*a, **k)

        patched = [(socket, "socket", ExplodingSocket), (socket, "create_connection", boom),
                   (socket, "socketpair", boom), (socket, "getaddrinfo", boom),
                   (ssl.SSLContext, "wrap_socket", boom),
                   (http.client.HTTPConnection, "__init__", boom),
                   (http.client.HTTPSConnection, "__init__", boom),
                   (urllib.request, "urlopen", boom)]
        originals = [(obj, name, getattr(obj, name)) for obj, name, _ in patched]
        for obj, name, stub in patched:
            setattr(obj, name, stub)
        try:
            for spec_path in (B.SPEC_STATIC_OVERLAY, B.SPEC_STATIC_IN_SCENE, B.SPEC_EDIT_PHOTO,
                              B.SPEC_MOTION):
                for profile_name in ("alpha_human_release", "alpha_wider_example", "dry"):
                    d = B.plan(spec_path, profile_name)
                    self.assertEqual(d["schema"], "ROUTE-DECISION-v0")
                    self.assertFalse(d["provenance"]["dispatched"])
                    self.assertEqual(d["provenance"]["network"], "none — planning opens no socket")
        finally:
            for obj, name, original in originals:
                setattr(obj, name, original)
        self.assertEqual(calls, [])

    def test_planning_in_a_fresh_interpreter_opens_nothing_even_while_importing(self):
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "plan_under_exploding_socket.py"
            script.write_text(STUB_SCRIPT, encoding="utf-8")
            proc = subprocess.run([sys.executable, str(script), str(B.ROOT)],
                                  capture_output=True, text=True, cwd=str(B.ROOT))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("PLANNED 12", proc.stdout)


class PlanIsCompleteOffline(unittest.TestCase):
    def test_every_fixture_produces_a_full_decision_under_the_alpha_profile(self):
        for spec_path in (B.SPEC_STATIC_OVERLAY, B.SPEC_STATIC_IN_SCENE, B.SPEC_EDIT_PHOTO,
                          B.SPEC_MOTION):
            d = B.plan(spec_path, "alpha_human_release")
            for key in ("decision_id", "spec_id", "decided_utc", "selection_basis",
                        "exclusions_applied", "manual_route_required", "cost_envelope",
                        "why_selected", "provenance"):
                self.assertIn(key, d)
            self.assertEqual(d["selection_basis"]["rule"],
                             "hard_requirements -> evidence_envelope -> cost -> fallback")

    def test_the_cli_renders_a_plan_without_touching_the_network(self):
        proc = subprocess.run([sys.executable, "-m", "runtime.route.cli", "--plan",
                               str(B.SPEC_MOTION), "--profile", "alpha_wider_example"],
                              capture_output=True, text=True, cwd=str(B.ROOT))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("PRIMARY   minimax-h3-max-i2v", proc.stdout)
        self.assertIn("EXCLUSIONS APPLIED", proc.stdout)


if __name__ == "__main__":
    unittest.main()
