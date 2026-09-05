"""Adapter invariants (task §5 a-j). Fake transports only; no socket, no key, no queue submit."""
import json
import os
import unittest
from decimal import Decimal

from _support import MP4_FIXTURE, PNG_FIXTURE, WAV_FIXTURE, NoNetworkTestCase, fixed_clock
import casebook as CB
import pricing as PR
import store as S
import surfaces
import transports as T
from adapters import adapter_for
from adapters import base as B
from adapters import fal_queue
from budget_guard import BudgetExceeded
from providers import DispatchRefused, PreDispatchRefusal

BOOK = CB.CaseBook.from_git("HEAD")
CANARY = "CANARY-fal-key-value-9f3e2a1b7c6d"


def fal_ok(url="https://v3.fal.media/files/fake/out.png", extra=None):
    """A complete fal queue lifecycle: submit -> IN_QUEUE -> IN_PROGRESS -> COMPLETED -> result -> download."""
    result = {"images": [{"url": url, "content_type": "image/png"}]} if url.endswith(".png") else \
        {"video": {"url": url, "content_type": "video/mp4"}} if url.endswith(".mp4") else {"audio": {"url": url, "content_type": "audio/wav"}}
    if extra:
        result = extra
    return T.FakeTransport(
        posts=[(200, {"request_id": "req-1", "status_url": "https://queue.fal.run/x/requests/req-1/status",
                      "response_url": "https://queue.fal.run/x/requests/req-1", "status": "IN_QUEUE"})],
        gets=[(200, {"status": "IN_QUEUE"}), (200, {"status": "IN_PROGRESS"}), (200, {"status": "COMPLETED"}), (200, result)],
        downloads=[(200, PNG_FIXTURE if url.endswith(".png") else MP4_FIXTURE if url.endswith(".mp4") else WAV_FIXTURE,
                    "image/png" if url.endswith(".png") else "video/mp4" if url.endswith(".mp4") else "audio/wav")])


class AdapterBase(NoNetworkTestCase):
    def setUp(self):
        super().setUp()
        self.pricing = PR.Pricing()
        self.budget = self.make_ledger()
        self.store = S.SealedStore(self.tmp / "runs" / "run-test" / "artifacts")

    def make(self, route_key, transport=None, **kw):
        entry = surfaces.REGISTRY.get(route_key)
        kw.setdefault("token_source", T.FakeTokenSource())
        kw.setdefault("sleep", lambda s: None)
        kw.setdefault("clock", fixed_clock())
        return adapter_for(entry, pricing=self.pricing, transport=transport, budget=self.budget, store=self.store, **kw)

    def row(self, case_id, route_key, arm=None):
        return BOOK.row(case_id, route_key, arm)


# ============================================================ (a) construction opens nothing
class ConstructionTest(AdapterBase):
    def test_a_every_registry_key_constructs_without_socket_or_key(self):
        for entry in surfaces.REGISTRY:
            t = T.FakeTransport()
            ad = adapter_for(entry, pricing=self.pricing, transport=t)
            self.assertIsNotNone(ad, entry.route_key)
            self.assertEqual(len(t.calls), 0)
            self.assertEqual(ad.submits, 0)
        self.assertEqual(self.key_file.read_text(), "")            # no key was needed or read


# ============================================================ (b) keys never leak
class KeyLeakTest(AdapterBase):
    def _scan_tree(self, needle):
        hits = []
        for p in (self.tmp / "runs").rglob("*"):
            if p.is_file() and needle.encode() in p.read_bytes():
                hits.append(str(p))
        return hits

    def test_b_env_canary_never_reaches_disk_or_records(self):
        os.environ["FAL_KEY"] = CANARY
        t = fal_ok()
        ad = self.make("gpt-image-2", t)
        attempt = ad.dispatch(self.row("IMG-CORE-01", "gpt-image-2"))
        self.assertEqual(attempt["status"], "ok")
        self.assertEqual(t.calls[0]["headers"]["Authorization"], f"Key {CANARY}")   # the fake saw it, in memory only
        self.assertEqual(self._scan_tree(CANARY), [])
        self.assertNotIn(CANARY, json.dumps(attempt))
        self.assertEqual(attempt["headers_template"]["Authorization"], "Key <KEY:FAL_KEY>")
        self.assertEqual(attempt["key_name"], "FAL_KEY")

    def test_b_file_canary_by_name_from_a_fake_path(self):
        self.write_fake_key("FAL_KEY", CANARY)
        t = fal_ok()
        ad = self.make("gpt-image-2", t)
        ad.dispatch(self.row("IMG-CORE-01", "gpt-image-2"))
        self.assertEqual(t.calls[0]["headers"]["Authorization"], f"Key {CANARY}")
        self.assertEqual(self._scan_tree(CANARY), [])

    def test_b_exception_texts_never_carry_the_key(self):
        os.environ["FAL_KEY"] = CANARY
        t = T.FakeTransport(posts=[TimeoutError("read timed out")])
        ad = self.make("gpt-image-2", t)
        attempt = ad.dispatch(self.row("IMG-CORE-01", "gpt-image-2"))
        self.assertNotIn(CANARY, json.dumps(attempt))
        b = self.make_ledger(ceiling="0.01", caps=("0.01", "0.01"), run_id="tiny")
        ad2 = self.make("gpt-image-2", fal_ok())
        ad2.budget = b
        with self.assertRaises(BudgetExceeded) as cm:
            ad2.dispatch(self.row("IMG-CORE-01", "gpt-image-2"))
        self.assertNotIn(CANARY, str(cm.exception))

    def test_missing_key_releases_the_reservation_and_sends_nothing(self):
        t = fal_ok()
        ad = self.make("gpt-image-2", t)
        with self.assertRaises(PreDispatchRefusal) as cm:
            ad.dispatch(self.row("IMG-CORE-01", "gpt-image-2"))
        self.assertIn("FAL_KEY", str(cm.exception))
        self.assertEqual(len(t.calls), 0)
        self.assertEqual(self.budget.spent_usd(), Decimal("0"))
        self.assertEqual([r["type"] for r in self.budget.records()], ["reservation", "release"])


# ============================================================ (c) reservation precedes send
class OrderingTest(AdapterBase):
    def test_c_reservation_is_open_when_the_transport_is_called(self):
        os.environ["FAL_KEY"] = "fake"
        log = []
        t = fal_ok()
        t.on_call = lambda kind, url: log.append((kind, self.budget.pending_usd() > 0, self.store.request_path("IMG-CORE-01__gpt-image-2__core__r1").exists()))
        ad = self.make("gpt-image-2", t)
        ad.dispatch(self.row("IMG-CORE-01", "gpt-image-2"))
        self.assertTrue(log and log[0][0] == "post")
        self.assertTrue(all(open_res for _, open_res, _ in log), "a reservation must be open at every send")
        self.assertTrue(all(req for _, _, req in log), "request.json must exist before the first byte leaves")


# ============================================================ (d) price mismatch / (e) cap
class PriceAndCapTest(AdapterBase):
    def test_d_price_mismatch_refuses_with_zero_calls_and_no_open_reservation(self):
        os.environ["FAL_KEY"] = "fake"
        t = fal_ok()
        ad = self.make("gpt-image-2", t)
        row = {**self.row("IMG-CORE-01", "gpt-image-2"), "unit_price": 0.211}
        with self.assertRaises(PreDispatchRefusal):
            ad.dispatch(row)
        self.assertEqual(len(t.calls), 0)
        self.assertEqual(self.budget.records(), [])
        self.assertEqual(self.budget.pending_usd(), Decimal("0"))

    def test_e_cap_breach_raises_before_send(self):
        os.environ["FAL_KEY"] = "fake"
        self.budget = self.make_ledger(ceiling="0.05", caps=("0.05", "0.05"), run_id="tiny")
        t = fal_ok()
        ad = self.make("gpt-image-2", t)
        with self.assertRaises(BudgetExceeded):
            ad.dispatch(self.row("IMG-CORE-01", "gpt-image-2"))
        self.assertEqual(len(t.calls), 0)
        self.assertEqual(self.budget.records(), [])


# ============================================================ (f) failures: one trial, one settlement
class FailureModesTest(AdapterBase):
    def _run(self, transport, route_key="gpt-image-2", case="IMG-CORE-01", **kw):
        os.environ["FAL_KEY"] = "fake"
        ad = self.make(route_key, transport, **kw)
        attempt = ad.dispatch(self.row(case, route_key))
        return ad, attempt

    def _assert_one_trial(self, ad, attempt, transport, status, billing_state):
        self.assertEqual(ad.submits, 1)
        self.assertEqual(transport.submits, 1)
        self.assertEqual(attempt["status"], status)
        self.assertEqual(attempt["retries"], 0)
        self.assertTrue(attempt["error_class"])
        self.assertEqual(attempt["billing_state"], billing_state)
        rows = self.budget.records()
        self.assertEqual([r["type"] for r in rows], ["reservation", "spend"], "one reservation, one conservative settlement, no release")
        self.assertEqual(self.budget.spent_usd(), Decimal("0.053"))
        self.assertTrue(self.store.attempt_path(attempt["trial_id"]).exists())
        self.assertIsNone(attempt["artifact"])

    def test_f_transport_timeout_at_submit_is_ambiguous(self):
        t = T.FakeTransport(posts=[TimeoutError("read timed out")])
        ad, a = self._run(t)
        self._assert_one_trial(ad, a, t, "timeout", "unknown_provisional")
        self.assertTrue(a["ambiguous_dispatch"]); self.assertFalse(a["outcome_resolved"])

    def test_f_provider_error_resolves_but_still_settles(self):
        t = fal_ok(extra={"error": {"type": "internal_server_error", "message": "upstream"}})
        ad, a = self._run(t)
        self._assert_one_trial(ad, a, t, "error", "reported")

    def test_f_content_policy_is_a_refusal(self):
        t = fal_ok(extra={"detail": "content policy violation: blocked"})
        ad, a = self._run(t)
        self._assert_one_trial(ad, a, t, "refusal", "reported")
        self.assertEqual(a["error_class"], "moderation_block")

    def test_f_poll_exhaustion_never_resubmits(self):
        t = T.FakeTransport(posts=[(200, {"request_id": "r", "status_url": "s", "response_url": "p"})], gets=[(200, {"status": "IN_PROGRESS"})])
        sleeps = []
        ad, a = self._run(t, sleep=sleeps.append, max_status_checks=4)
        self._assert_one_trial(ad, a, t, "timeout", "unknown_provisional")
        self.assertEqual(a["error_class"], "poll_budget_exhausted")
        self.assertEqual(ad.status_checks, 4)
        self.assertEqual(len(sleeps), 3)
        self.assertEqual(sum(1 for c in t.calls if c["kind"] == "post"), 1)

    def test_f_poll_failure_after_submit_is_ambiguous(self):
        t = T.FakeTransport(posts=[(200, {"request_id": "r", "status_url": "s", "response_url": "p"})], gets=[ConnectionResetError(54, "reset")])
        ad, a = self._run(t)
        self._assert_one_trial(ad, a, t, "error", "unknown_provisional")
        self.assertTrue(a["error_class"].startswith("poll_"))

    def test_f_download_failure_keeps_the_trial_and_the_money(self):
        t = fal_ok()
        t.downloads = [TimeoutError("cdn")]
        ad, a = self._run(t)
        self._assert_one_trial(ad, a, t, "error", "reported")
        self.assertEqual(a["error_class"], "artifact_download_failed")

    def test_f_veo_operation_error_and_safety_filter(self):
        op = "projects/p/locations/us-central1/publishers/google/models/veo-3.1-fast-generate-001/operations/op-1"
        t = T.FakeTransport(posts=[(200, {"name": op}), (200, {"name": op, "done": True, "error": {"status": "INTERNAL", "message": "x"}})])
        ad = self.make("veo-3.1-fast", t)
        a = ad.dispatch(self.row("VID-T2V-01", "veo-3.1-fast"))
        self.assertEqual((a["status"], a["error_class"]), ("error", "INTERNAL"))
        self.assertEqual(ad.submits, 1)
        t2 = T.FakeTransport(posts=[(200, {"name": op}), (200, {"name": op, "done": True, "response": {"raiMediaFilteredCount": 1, "raiMediaFilteredReasons": ["x"]}})])
        ad2 = self.make("veo-3.1-fast", t2)
        a2 = ad2.dispatch({**self.row("VID-T2V-01", "veo-3.1-fast"), "repeat_index": 2})
        self.assertEqual((a2["status"], a2["error_class"]), ("refusal", "safety_filtered"))
        self.assertEqual(len(self.budget.records()), 4)      # two trials, two settlements


# ============================================================ (g) dry-run bytes == sent bytes
VEO_OP = "projects/p/locations/us-central1/publishers/google/models/m/operations/op-9"


def veo_ok():
    return T.FakeTransport(posts=[(200, {"name": VEO_OP}), (200, {"name": VEO_OP, "done": False}),
                                  (200, {"name": VEO_OP, "done": True, "response": {"raiMediaFilteredCount": 0, "videos": [{"bytesBase64Encoded": B.b64(MP4_FIXTURE), "mimeType": "video/mp4"}]}})])


class BodyEqualityTest(AdapterBase):
    ROUTES = [
        ("IMG-CORE-01", "gpt-image-2", {}, "fal"),
        ("VID-T2V-01", "kling-v3-pro-audio", {}, "fal-video"),
        ("VID-I2V-01", "kling-v3-pro-i2v", {"image_url": "https://example.test/plate.png"}, "fal-video"),
        ("VID-REF-01", "seedance-2.5-ref2v", {"image_urls": ["https://example.test/a.png", "https://example.test/b.png", "https://example.test/c.png"]}, "fal-video"),
        ("IMG-EDIT-01", "flux-2-pro-edit", {"image_urls": ["https://example.test/in.png"]}, "fal"),
        ("AUD-TTS-01", "elevenlabs-v3", {"voice": "Roger"}, "fal-audio"),
        ("AUD-LIP-01", "kling-lipsync-a2v", {"video_url": "https://example.test/plate.mp4", "audio_url": "https://example.test/drive.wav"}, "fal-video"),
        ("MUS-01", "elevenlabs-music", {}, "fal-audio"),
        ("VID-T2V-01", "veo-3.1-fast", {}, "veo"),
        ("IMG-CORE-01", "nano-banana-2", {}, "gemini"),
        ("VID-T2V-01", "gemini-omni-1.1-flash", {}, "omni"),
        ("MUS-01", "lyria", {}, "lyria"),
        ("AUD-TTS-01", "sarvam-bulbul-v3", {"voice": "rahul"}, "sarvam"),
    ]

    def _transport(self, kind):
        if kind == "fal":
            return fal_ok()
        if kind == "fal-video":
            return fal_ok("https://v3.fal.media/files/fake/out.mp4")
        if kind == "fal-audio":
            return fal_ok("https://v3.fal.media/files/fake/out.wav")
        if kind == "veo":
            return veo_ok()
        if kind == "gemini":
            return T.FakeTransport(posts=[(200, {"responseId": "r", "candidates": [{"finishReason": "STOP", "content": {"parts": [{"inlineData": {"mimeType": "image/png", "data": B.b64(PNG_FIXTURE)}}]}}]})])
        if kind == "omni":
            return T.FakeTransport(posts=[(200, {"id": "i", "status": "completed", "steps": [{"type": "model_output", "content": [{"type": "video", "data": B.b64(MP4_FIXTURE), "mime_type": "video/mp4"}]}]})])
        if kind == "lyria":
            return T.FakeTransport(posts=[(200, {"predictions": [{"audioContent": B.b64(WAV_FIXTURE), "mimeType": "audio/wav"}]})])
        if kind == "sarvam":
            return T.FakeTransport(posts=[(200, {"request_id": "s", "audios": [B.b64(WAV_FIXTURE)]})])
        raise AssertionError(kind)

    def test_g_dry_run_body_bytes_equal_sent_bytes_for_every_family(self):
        os.environ["FAL_KEY"] = "fake"
        os.environ["SARVAM_API_KEY"] = "fake"
        for case, route, inputs, kind in self.ROUTES:
            with self.subTest(route=route):
                t = self._transport(kind)
                ad = self.make(route, t)
                row = self.row(case, route)
                dry = ad.dry_run(row, inputs)
                self.assertTrue(dry["would_dispatch"], (route, dry["refusal_reason"]))
                attempt = ad.dispatch(row, inputs)
                self.assertEqual(attempt["status"], "ok", (route, attempt["error_class"], attempt["raw_status_note"]))
                sent = t.calls[0]["payload"]
                self.assertEqual(sent, S.canonical_json(dry["body"]), route)
                self.assertEqual(attempt["config_hash"], B.sha256_hex(sent))
                self.assertEqual(self.store.request_path(attempt["trial_id"]).read_bytes(), sent)
                self.assertIsNotNone(attempt["artifact"])
                self.assertTrue(self.store.verify({"relative_path": attempt["artifact"]["relative_path"], "bytes": attempt["artifact"]["bytes"], "sha256": attempt["artifact"]["sha256"]}))
                for k in ("provider", "surface", "surface_model_id", "model_version", "endpoint", "workflow", "lane", "case_id", "item_id", "route_key",
                          "arm", "repeat_index", "prompt_hash", "config_hash", "config_location", "seed", "seed_policy", "billing_pool", "currency",
                          "reserved_amount", "cost_ref", "key_name", "credential_file_name", "price_pin_ref", "unit_price", "quantity", "quantity_unit",
                          "requested_at", "completed_at", "status", "error_class", "raw_status_note", "billing_state", "ambiguous_dispatch",
                          "outcome_resolved", "lifecycle_counts", "retries", "one_call_one_trial"):
                    self.assertIn(k, attempt, (route, k))
                self.assertEqual(attempt["retries"], 0)
                self.assertTrue(attempt["one_call_one_trial"])
                self.assertEqual(attempt["seed_policy"], "unset")
                self.assertIsNone(attempt["seed"])

    def test_gpt_image_2_body_pins_quality_medium_and_one_image(self):
        body = self.make("gpt-image-2", fal_ok()).build_request(self.row("IMG-CORE-01", "gpt-image-2")).body
        self.assertEqual(body["quality"], "medium")
        self.assertEqual(body["num_images"], 1)
        self.assertEqual(body["image_size"], {"width": 816, "height": 1024})
        self.assertNotIn("seed", body)

    def test_veo_extend_is_two_calls_one_reservation(self):
        op2 = VEO_OP + "-2"
        t = T.FakeTransport(posts=[(200, {"name": VEO_OP}),
                                   (200, {"name": VEO_OP, "done": True, "response": {"videos": [{"bytesBase64Encoded": B.b64(MP4_FIXTURE), "mimeType": "video/mp4"}]}}),
                                   (200, {"name": op2}),
                                   (200, {"name": op2, "done": True, "response": {"videos": [{"bytesBase64Encoded": B.b64(MP4_FIXTURE + b"\x01"), "mimeType": "video/mp4"}]}})])
        ad = self.make("veo-3.1-fast-extend", t)
        row = self.row("VID-MS-01", "veo-3.1-fast-extend")
        dry = ad.dry_run(row)
        self.assertEqual(dry["api_calls_per_trial"], 2)
        self.assertEqual(dry["body"]["parameters"]["durationSeconds"], 8)
        self.assertEqual(len(dry["followups"]), 1)
        self.assertNotIn("durationSeconds", dry["followups"][0]["body"]["parameters"])
        a = ad.dispatch(row)
        self.assertEqual(a["status"], "ok")
        self.assertEqual(ad.submits, 2)
        self.assertEqual(a["lifecycle_counts"]["api_calls"], 2)
        posts = [c for c in t.calls if c["kind"] == "post" and ":predictLongRunning" in c["url"]]
        self.assertEqual(len(posts), 2)
        second = json.loads(posts[1]["payload"])
        self.assertEqual(second["instances"][0]["video"]["mimeType"], "video/mp4")
        self.assertEqual(second["instances"][0]["video"]["bytesBase64Encoded"], B.b64(MP4_FIXTURE))
        self.assertEqual([r["type"] for r in self.budget.records()], ["reservation", "spend"])
        self.assertEqual(self.budget.spent_usd(), Decimal("1.5"))
        self.assertEqual(len(self.store.manifest()), 2)          # final + call-1 intermediate sealed


# ============================================================ (h) refuse live, render dry
class RefuseLiveRenderDryTest(AdapterBase):
    def test_h_unpinned_conditional_unverified_and_azure_rows(self):
        os.environ["FAL_KEY"] = "fake"
        checks = [
            ("IMG-EDIT-01", "gpt-image-2-edit", None, "price_unpinned"),
            ("IMG-CORE-01", "sd3.5-large", None, "no adapter"),
            ("VID-REF-01", "kling-v3-elements", None, "unverified"),
            ("VID-T2V-01", "sora-2", None, "subscription"),
            ("VID-TOPO3-01", "veo-3.1-lite-i2v", None, "price_unpinned"),
            ("AUD-LIP-01", "sync-lipsync-v3", None, "price_unpinned"),
        ]
        for case, route, arm, needle in checks:
            with self.subTest(route=route):
                ad = self.make(route, fal_ok())
                row = self.row(case, route, arm)
                d = ad.dry_run(row)
                self.assertFalse(d["would_dispatch"])
                self.assertIn(needle, d["refusal_reason"])
                self.assertIsNotNone(d["url"])
                with self.assertRaises(DispatchRefused):
                    ad.dispatch(row)
                self.assertEqual(self.budget.records(), [])


# ============================================================ (i) parameter refusals
class ParameterRefusalTest(AdapterBase):
    def test_i_caller_parameters_are_refused(self):
        ad = self.make("gpt-image-2", fal_ok())
        row = self.row("IMG-CORE-01", "gpt-image-2")
        for bad in ({"num_images": 2}, {"seed": 7}, {"image_size": "square"}, {"unknown_param": 1}):
            with self.subTest(bad=bad):
                with self.assertRaises(PreDispatchRefusal):
                    ad.build_request(row, bad)

    def test_i_pinned_output_count_must_be_one(self):
        saved = dict(fal_queue.ROUTE_PINS["gpt-image-2"])
        try:
            fal_queue.ROUTE_PINS["gpt-image-2"]["num_images"] = 2
            with self.assertRaises(PreDispatchRefusal):
                self.make("gpt-image-2", fal_ok()).build_request(self.row("IMG-CORE-01", "gpt-image-2"))
            fal_queue.ROUTE_PINS["gpt-image-2"] = {**saved, "seed": 5}
            with self.assertRaises(PreDispatchRefusal) as cm:
                self.make("gpt-image-2", fal_ok()).build_request(self.row("IMG-CORE-01", "gpt-image-2"))
            self.assertIn("SEED-POLICY", str(cm.exception))
            fal_queue.ROUTE_PINS["gpt-image-2"] = {**saved, "not_in_schema": 1}
            with self.assertRaises(PreDispatchRefusal):
                self.make("gpt-image-2", fal_ok()).build_request(self.row("IMG-CORE-01", "gpt-image-2"))
        finally:
            fal_queue.ROUTE_PINS["gpt-image-2"] = saved

    def test_pending_inputs_render_in_dry_run_but_refuse_live(self):
        os.environ["FAL_KEY"] = "fake"
        ad = self.make("kling-v3-pro-i2v", fal_ok("https://x/out.mp4"))
        row = self.row("VID-I2V-01", "kling-v3-pro-i2v")
        d = ad.dry_run(row)
        self.assertEqual(d["body"]["start_image_url"], {"$pending_artifact": "VID-I2V-01:core:plate_accepted_draw"})
        self.assertTrue(d["would_dispatch"])                     # priced and shaped; the plate arrives after 1a acceptance
        with self.assertRaises(PreDispatchRefusal):
            ad.dispatch(row)
        self.assertEqual(self.budget.records(), [])


# ============================================================ (j) store
class StoreThroughAdapterTest(AdapterBase):
    def test_j_same_trial_twice_is_refused_and_nothing_is_overwritten(self):
        os.environ["FAL_KEY"] = "fake"
        ad = self.make("gpt-image-2", fal_ok())
        row = self.row("IMG-CORE-01", "gpt-image-2")
        a = ad.dispatch(row)
        before = self.store.request_path(a["trial_id"]).read_bytes()
        ad2 = self.make("gpt-image-2", fal_ok())
        with self.assertRaises(PreDispatchRefusal):
            ad2.dispatch(row)
        self.assertEqual(self.store.request_path(a["trial_id"]).read_bytes(), before)
        self.assertEqual([r["type"] for r in self.budget.records()], ["reservation", "spend", "reservation", "release"])

    def test_no_transport_or_ledger_refuses(self):
        entry = surfaces.REGISTRY.get("gpt-image-2")
        with self.assertRaises(DispatchRefused):
            adapter_for(entry, pricing=self.pricing).dispatch(self.row("IMG-CORE-01", "gpt-image-2"))
        with self.assertRaises(DispatchRefused):
            adapter_for(entry, pricing=self.pricing, transport=fal_ok()).dispatch(self.row("IMG-CORE-01", "gpt-image-2"))


if __name__ == "__main__":
    unittest.main()
