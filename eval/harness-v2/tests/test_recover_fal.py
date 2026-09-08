"""recover_fal: a submitted-and-billed fal job whose poll was misread is fetched by request id — no re-submit,
no new charge, original attempt untouched, recovered attempt preferred by every reader."""
import json
import unittest

from _support import NoNetworkTestCase, hv2_paths  # noqa: F401
import transports as T
import store as S
import recover_fal as RF
import run_live as RL
from test_adapters import PNG_FIXTURE  # shared fixture bytes


class RecoverFalTest(NoNetworkTestCase):
    RID = "01a07fd0-3ec8-7733-8fe0-ce17d812e5c2"
    TID = "IMG-CORE-01__gpt-image-2__core__r1"

    def _run_dir(self):
        out = self.tmp / "runs" / "img-x"
        store = S.SealedStore(out / RL.ARTIFACTS_DIR)
        store.write_request(self.TID, b'{"prompt": "x"}')
        attempt = {"trial_id": self.TID, "case_id": "IMG-CORE-01", "route_key": "gpt-image-2", "arm": "core", "repeat_index": 1,
                   "status": "error", "error_class": "poll_http_202", "outcome_resolved": False, "ambiguous_dispatch": True,
                   "billing_state": "unknown_provisional", "provider_request_id": None,
                   "raw_status_note": f"status poll answered 202 for {self.RID}; final outcome unknown",
                   "endpoint": "https://queue.fal.run/openai/gpt-image-2", "lifecycle_counts": {"submits": 1, "status_checks": 1},
                   "artifact": None, "seed_policy": "unset"}
        store.write_attempt(self.TID, attempt)
        (out / "PLAN.yaml").write_text("header: {}\ntrials: []\n")
        return out, store, attempt

    def test_candidates_need_a_poll_error_and_a_request_id(self):
        out, store, _ = self._run_dir()
        c = RF.candidates(store)
        self.assertEqual([t for t, _ in c], [self.TID])
        self.assertEqual(RF.request_id_of(c[0][1]), self.RID)

    def test_recovery_fetches_seals_and_never_resubmits(self):
        out, store, original = self._run_dir()
        t = T.FakeTransport(gets=[(202, {"status": "IN_PROGRESS"}), (200, {"status": "COMPLETED"}),
                                  (200, {"images": [{"url": "https://v3.fal.media/files/fake/out.png", "content_type": "image/png"}]})],
                            downloads=[(200, PNG_FIXTURE, "image/png")])
        res = RF.recover_one(self.TID, original, store, t, {"Authorization": "Key CANARY"}, sleep=lambda s: None)
        self.assertTrue(res["recovered"], res)
        self.assertEqual(res["status_checks"], 2)
        self.assertEqual(t.submits, 0, "a recovery never submits")
        self.assertEqual([c["kind"] for c in t.calls], ["get", "get", "get", "download"])
        # the original attempt is byte-for-byte untouched; the recovered one sits beside it and is preferred
        self.assertEqual(json.loads(store.attempt_path(self.TID).read_text())["status"], "error")
        rec = store.load_attempt(self.TID)
        self.assertEqual(rec["status"], "ok")
        self.assertEqual(rec["provider_request_id"], self.RID)
        self.assertFalse(rec["recovery"]["resubmitted"])
        self.assertEqual(rec["lifecycle_counts"]["submits"], 1)
        self.assertTrue(store.verify(rec["artifact"] | {"trial_id": self.TID}) or (store.root / rec["artifact"]["relative_path"]).exists())
        # the key never lands in any persisted file
        for p in out.rglob("*"):
            if p.is_file():
                self.assertNotIn(b"CANARY", p.read_bytes(), str(p))
        # a second recovery of the same trial is not a candidate any more
        self.assertEqual(RF.candidates(store), [])

    def test_not_completed_is_reported_not_forced(self):
        out, store, original = self._run_dir()
        t = T.FakeTransport(gets=[(202, {"status": "IN_PROGRESS"})] * 3 + [(500, {"detail": "boom"})])
        res = RF.recover_one(self.TID, original, store, t, {"Authorization": "Key K"}, sleep=lambda s: None)
        self.assertFalse(res["recovered"])
        self.assertIsNone(store.load_attempt(self.TID).get("artifact"))
        self.assertFalse(store.recovered_attempt_path(self.TID).exists())

    def test_recovered_attempt_needs_an_original(self):
        store = S.SealedStore(self.tmp / "s")
        with self.assertRaises(S.ArtifactIntegrityError):
            store.write_recovered_attempt("nope", {"status": "ok"})


if __name__ == "__main__":
    unittest.main()
