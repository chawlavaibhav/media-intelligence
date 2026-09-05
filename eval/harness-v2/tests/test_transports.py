"""Transports: construction opens nothing; the token source never leaks; fakes record."""
import os
import unittest
from types import SimpleNamespace

from _support import NoNetworkTestCase
import transports as T
from providers import PreDispatchRefusal


class TransportTest(NoNetworkTestCase):
    def test_construction_opens_no_socket(self):
        for cls in (T.FalQueueTransport, T.VertexTransport, T.SarvamTransport):
            t = cls()
            self.assertEqual(t.calls, 0)

    def test_live_call_would_hit_the_guard(self):
        """Proves the no-network guard is real: a live transport call raises NetworkAttempted here."""
        from _support import NetworkAttempted
        with self.assertRaises(NetworkAttempted):
            T.FalQueueTransport().get_json("https://queue.fal.run/never", {})

    def test_token_source_uses_a_throwaway_gcloud_config_and_returns_only_the_token(self):
        seen = []

        def runner(cmd, env=None, capture_output=None, text=None, timeout=None):
            seen.append((list(cmd), env.get("CLOUDSDK_CONFIG")))
            if cmd[1:3] == ["auth", "activate-service-account"]:
                return SimpleNamespace(returncode=0, stdout="", stderr="")
            return SimpleNamespace(returncode=0, stdout="FAKE-TOKEN-XYZ\n", stderr="")

        cred = self.tmp / "fake-sa.json"
        cred.write_text("{}")
        src = T.GcloudServiceAccountTokenSource(cred, runner=runner)
        tok = src.token()
        self.assertEqual(tok, "FAKE-TOKEN-XYZ")
        self.assertEqual(len(seen), 2)
        cfg = seen[0][1]
        self.assertTrue(cfg and cfg != os.environ.get("CLOUDSDK_CONFIG"))
        self.assertFalse(os.path.exists(cfg), "the throw-away CLOUDSDK_CONFIG must be deleted afterwards")
        self.assertIn("--key-file", seen[0][0])
        self.assertEqual(src.credential_file_name, str(cred))

    def test_token_source_refuses_missing_file_before_running_anything(self):
        calls = []
        src = T.GcloudServiceAccountTokenSource(self.tmp / "missing.json", runner=lambda *a, **k: calls.append(a))
        with self.assertRaises(PreDispatchRefusal):
            src.token()
        self.assertEqual(calls, [])

    def test_token_source_failure_text_carries_no_token(self):
        def runner(cmd, **k):
            return SimpleNamespace(returncode=1, stdout="SECRET-ish", stderr="boom")
        cred = self.tmp / "fake-sa.json"
        cred.write_text("{}")
        with self.assertRaises(PreDispatchRefusal) as cm:
            T.GcloudServiceAccountTokenSource(cred, runner=runner).token()
        self.assertNotIn("SECRET", str(cm.exception))

    def test_fake_transport_records_and_raises_scripted_failures(self):
        ft = T.FakeTransport(posts=[(200, {"a": 1}), TimeoutError("t")], gets=[(200, {"status": "COMPLETED"})],
                             downloads=[(200, b"\x00\x01", "video/mp4")])
        self.assertEqual(ft.post_json("u", {"h": 1}, b"{}"), (200, {"a": 1}))
        with self.assertRaises(TimeoutError):
            ft.post_json("u", {}, b"{}")
        self.assertEqual(ft.get_json("s", {}), (200, {"status": "COMPLETED"}))
        self.assertEqual(ft.get_bytes("d", {})[1], b"\x00\x01")
        self.assertEqual(ft.submits, 2)
        self.assertEqual([c["kind"] for c in ft.calls], ["post", "post", "get", "download"])


if __name__ == "__main__":
    unittest.main()
