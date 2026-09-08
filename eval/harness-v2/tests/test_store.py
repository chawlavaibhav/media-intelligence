"""Test (j): the sealed store refuses an existing path and records sha256 over the exact bytes."""
import hashlib
import json
import unittest

from _support import MP4_FIXTURE, PNG_FIXTURE, NoNetworkTestCase
import store as S


class StoreTest(NoNetworkTestCase):
    def test_request_written_before_dispatch_and_hash_bound(self):
        st = S.SealedStore(self.tmp / "run")
        body = S.canonical_json({"prompt": "x", "num_images": 1})
        path, h = st.write_request("T-1", body)
        self.assertEqual(path.read_bytes(), body)
        self.assertEqual(h, hashlib.sha256(body).hexdigest())
        with self.assertRaises(S.ArtifactIntegrityError):
            st.write_request("T-1", body)

    def test_seal_bytes_with_record_and_manifest(self):
        st = S.SealedStore(self.tmp / "run")
        rec = st.seal("T-1", MP4_FIXTURE, "video/mp4", {"request_id": "r"})
        self.assertEqual(rec["sha256"], hashlib.sha256(MP4_FIXTURE).hexdigest())
        self.assertEqual(rec["bytes"], len(MP4_FIXTURE))
        self.assertEqual(rec["media_kind"], "video")
        self.assertTrue(rec["relative_path"].endswith(".mp4"))
        self.assertTrue(st.verify(rec))
        self.assertEqual(json.loads(st.record_path("T-1").read_text())["sha256"], rec["sha256"])
        self.assertEqual(len(st.manifest()), 1)
        with self.assertRaises(S.ArtifactIntegrityError):
            st.seal("T-1", MP4_FIXTURE, "video/mp4")
        self.assertEqual(len(st.manifest()), 1)

    def test_refusals(self):
        st = S.SealedStore(self.tmp / "run")
        with self.assertRaises(TypeError):
            st.seal("T-2", "text pretending to be media", "image/png")
        with self.assertRaises(S.ArtifactIntegrityError):
            st.seal("T-2", b"", "image/png")

    def test_image_and_unknown_types(self):
        st = S.SealedStore(self.tmp / "run")
        self.assertTrue(st.seal("T-3", PNG_FIXTURE, "image/png")["relative_path"].endswith(".png"))
        r = st.seal("T-4", PNG_FIXTURE, None)
        self.assertTrue(r["relative_path"].endswith(".bin"))
        self.assertEqual(r["media_kind"], "other")

    def test_canonical_json_is_stable_and_unicode_safe(self):
        a = S.canonical_json({"b": 1, "a": "शुभ"})
        b = S.canonical_json({"a": "शुभ", "b": 1})
        self.assertEqual(a, b)
        self.assertIn("शुभ".encode("utf-8"), a)


if __name__ == "__main__":
    unittest.main()
