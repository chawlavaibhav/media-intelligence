"""ZERO SPEND for the execution bridge, proved: build()+run() under `dry` opens no socket.

Same discipline as runtime/tests/test_route_offline.py, one layer further along the pipeline. A FRESH
interpreter replaces socket, ssl, http.client and urllib with stubs that raise, BEFORE any runtime or
harness module is imported, then plans, builds and dry-runs every fixture spec under the `dry` profile -
through the harness adapters' dry_run(). If any line in this package, or in the harness code it wraps,
tried to reach a provider or read a key file over the network, this test fails instead of costing money.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

import _bootstrap as B

STUB_SCRIPT = textwrap.dedent('''
    import http.client, socket, ssl, sys, urllib.request
    from pathlib import Path

    class NetworkAttempted(AssertionError):
        pass

    def boom(*a, **k):
        raise NetworkAttempted("the execution bridge tried to open a connection")

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
    from runtime.execute.bridge import ExecutionBridge

    router, ev, _ = build_router(root)
    bridge = ExecutionBridge(evidence=ev, prices=router.prices, identities=router.identities)
    prof = _profile(ev, "dry")
    built = blocked = attempts = 0
    prompt = "A textless plate for the fixture job; calm light; no lettering anywhere in the picture at all."
    for spec_path in sorted((root / "runtime" / "route" / "fixtures").glob("SPEC-*.yaml")):
        spec = load_spec(spec_path)
        d = router.plan(spec, prof, already_committed_usd=Decimal("0"), customer_ref="acct-test")
        m = bridge.build(spec, d, prof, prompt_text=prompt, customer_ref="acct-test")
        assert m["schema"] == "EXECUTION-MANIFEST-v0"
        assert m["provenance"]["dispatched"] is False and m["provenance"]["network"] == "none"
        res = bridge.run(m, prof)
        assert res["dispatched"] is False and res["network"] == "none"
        if m["blocked"]:
            assert res["status"] == "refused" and res["attempts"] == []
            blocked += 1
        else:
            assert res["status"] == "dry_complete"
            assert all(a["status"] == "dry_not_sent" and a["settled_usd"] == "0" and a["reserved_usd"] == "0"
                       for a in res["attempts"])
            attempts += len(res["attempts"])
        built += 1
    print("BUILT", built, "BLOCKED", blocked, "ATTEMPTS", attempts)
''')


class NoSocketDuringBuildAndDryRun(unittest.TestCase):
    def test_every_fixture_builds_and_dry_runs_under_an_exploding_socket_in_a_fresh_interpreter(self):
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "bridge_under_exploding_socket.py"
            script.write_text(STUB_SCRIPT, encoding="utf-8")
            proc = subprocess.run([sys.executable, str(script), str(B.ROOT)],
                                  capture_output=True, text=True, cwd=str(B.ROOT))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            # four fixtures; the supplied-photo edit is blocked (manual_route_required: no fallback route);
            # the other three render 2 primary + 2 fallback attempts each
            self.assertIn("BUILT 4 BLOCKED 1 ATTEMPTS 12", proc.stdout)


if __name__ == "__main__":
    unittest.main()
