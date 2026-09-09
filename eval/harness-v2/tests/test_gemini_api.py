"""The Gemini Developer API surface (2026-09-09, CONTROLLER-GEMINI-MODELS-VIA-GEMINI-KEY-2026-09-09): the Gemini-named routes run on
generativelanguage.googleapis.com with the key NAMED GOOGLE_API_KEY. Fake transports only; no socket, no key, no spend.

    dry-run body bytes == sent bytes (image t2i, image edit with inline references, Omni video);
    the key is read by NAME at dispatch, travels in the x-goog-api-key header of that one request and never reaches the URL,
    the body, the sealed request, the attempt record or an exception; a missing key refuses before any send and releases;
    a malformed reply, a safety block (image: promptFeedback / IMAGE_SAFETY; Omni: a failed interaction whose errors speak of
    safety) and a 429 after the submit are classified exactly as the Vertex variants classify them; the image body is the Vertex
    body byte for byte; the entry guard refuses any key name but GOOGLE_API_KEY and any host but generativelanguage.googleapis.com.
"""
import dataclasses
import json
import os
import unittest
from decimal import Decimal

from _support import MP4_FIXTURE, PNG_FIXTURE, NoNetworkTestCase, fixed_clock
import casebook as CB
import inputs as INP
import pricing as PR
import run_live as RL
import store as S
import surfaces
import transports as T
from adapters import adapter_for
from adapters import base as B
from adapters import gemini_api_image, gemini_api_omni, vertex_gemini_image, vertex_omni
from providers import PreDispatchRefusal

BOOK = CB.CaseBook.from_git("HEAD")
CANARY = "CANARY-google-api-key-value-7a1b2c3d4e5f"
IMAGE_ROUTES = ("nano-banana-2", "nano-banana-pro", "nano-banana-pro-edit")
OMNI_ROUTES = ("gemini-omni-1.1-flash", "gemini-omni-1.1-flash-10s", "gemini-omni-1.1-flash-long")


def image_ok(png=PNG_FIXTURE):
    return T.FakeTransport(posts=[(200, {"responseId": "resp-1", "modelVersion": "gemini-x", "candidates": [
        {"finishReason": "STOP", "content": {"parts": [{"inlineData": {"mimeType": "image/png", "data": B.b64(png)}}]}}]})])


def omni_ok(mp4=MP4_FIXTURE):
    return T.FakeTransport(posts=[(200, {"id": "v1_abc", "status": "completed", "model": "gemini-omni-1.1-flash", "object": "interaction",
                                          "steps": [{"type": "user_input", "content": [{"type": "text", "text": "..."}]},
                                                    {"type": "model_output", "content": [{"type": "video", "mime_type": "video/mp4", "data": B.b64(mp4)}]}],
                                          "usage": {"total_output_tokens": 34752}})])


class GeminiApiBase(NoNetworkTestCase):
    def setUp(self):
        super().setUp()
        self.pricing = PR.Pricing()
        self.budget = self.make_ledger()
        self.store = S.SealedStore(self.tmp / "runs" / "run-test" / "artifacts")

    def make(self, route_key, transport=None, entry=None, **kw):
        entry = entry or surfaces.REGISTRY.get(route_key)
        kw.setdefault("sleep", lambda s: None)
        kw.setdefault("clock", fixed_clock())
        return adapter_for(entry, pricing=self.pricing, transport=transport, budget=self.budget, store=self.store, **kw)

    def row(self, case_id, route_key, **over):
        return {**BOOK.row(case_id, route_key), **over}

    def _scan_tree(self, needle):
        return [str(p) for p in (self.tmp / "runs").rglob("*") if p.is_file() and needle.encode() in p.read_bytes()]


# ============================================================ registry: the six routes point at the Gemini API
class RegistryTest(unittest.TestCase):
    def test_six_routes_are_on_the_gemini_api_with_the_named_key_and_the_credits_pool(self):
        for key in IMAGE_ROUTES + OMNI_ROUTES:
            with self.subTest(route=key):
                e = surfaces.REGISTRY.get(key)
                self.assertEqual(e.surface, "gemini_api")
                self.assertEqual(e.adapter, "gemini_api_image" if key in IMAGE_ROUTES else "gemini_api_omni")
                self.assertEqual((e.key_name, e.credential_file_name), ("GOOGLE_API_KEY", surfaces.MI_KEYS_FILE))
                self.assertEqual((e.billing_pool, e.currency, e.shape_status), ("credits", "USD", "verified"))
                self.assertIn(surfaces.GEMINI_API_BILLING_NOTE, e.notes)
                self.assertEqual(e.price_pin_ref, surfaces.GEMINI_API_PRICING_PIN)
                self.assertTrue(e.endpoint.startswith("https://generativelanguage.googleapis.com/v1beta/"), e.endpoint)
                self.assertNotIn("?", e.endpoint)
                self.assertNotIn("preview", e.surface_model_id, "the Gemini API ids are the pricing-page ids, not the Vertex preview id")
                self.assertIn(e.surface_model_id, surfaces.GEMINI_API_PRICES)
                self.assertIn(surfaces.GEMINI_API_PRICES[e.surface_model_id], e.notes)
        self.assertEqual(surfaces.REGISTRY.get("nano-banana-2").surface_model_id, "gemini-3.1-flash-image")
        self.assertEqual(surfaces.REGISTRY.get("nano-banana-pro").surface_model_id, "gemini-3-pro-image")
        self.assertEqual(surfaces.REGISTRY.get("nano-banana-pro-edit").surface_model_id, "gemini-3-pro-image")
        self.assertEqual(surfaces.REGISTRY.get("nano-banana-pro-edit").workflow, "edit")
        for key in OMNI_ROUTES:
            self.assertEqual(surfaces.REGISTRY.get(key).surface_model_id, "gemini-omni-1.1-flash")
            self.assertEqual(surfaces.REGISTRY.get(key).endpoint, surfaces.GEMINI_API_INTERACTIONS)
        # the image endpoint is exactly the transport's generateContent URL for that model
        for key in IMAGE_ROUTES:
            e = surfaces.REGISTRY.get(key)
            self.assertEqual(e.endpoint, T.gemini_generate_content_url(e.surface_model_id))
        # no other route reads the Gemini key; no Gemini-named model is left on Vertex or fal
        others = [e for e in surfaces.REGISTRY if e.route_key not in IMAGE_ROUTES + OMNI_ROUTES]
        self.assertFalse([e.route_key for e in others if e.key_name == "GOOGLE_API_KEY" or e.surface == "gemini_api"])
        self.assertFalse([e.route_key for e in others if "gemini" in e.surface_model_id.lower()])
        self.assertEqual(set(surfaces.GEMINI_API_REPOINT_PENDING_PACKAGE), set(IMAGE_ROUTES + OMNI_ROUTES))

    def test_live_transport_factory_maps_the_surface_and_opens_nothing(self):
        for key in ("nano-banana-2", "gemini-omni-1.1-flash"):
            t = RL.live_transport_factory(surfaces.REGISTRY.get(key), {})
            self.assertIsInstance(t, T.GeminiApiTransport)
            self.assertEqual((t.name, t.calls), ("gemini_api", 0))

    def test_key_name_is_allowed_by_name_only(self):
        self.assertIn("GOOGLE_API_KEY", B.KEY_NAMES_ALLOWED)
        self.assertEqual(gemini_api_image.KEY_NAME, surfaces.GEMINI_API_KEY_NAME)


# ============================================================ bodies: dry-run bytes == sent bytes; the key in the header only
class BodyTest(GeminiApiBase):
    CASES = [
        ("IMG-CORE-01", "nano-banana-2", {}, "image"),
        ("IMG-CORE-01", "nano-banana-pro", {}, "image"),
        ("IMG-EDIT-01", "nano-banana-pro-edit", {"reference_images": [(PNG_FIXTURE, "image/png")]}, "image"),
        ("IMG-REF-01", "nano-banana-pro-edit", {"reference_images": [(PNG_FIXTURE, "image/png")] * 3}, "image"),
        ("VID-T2V-01", "gemini-omni-1.1-flash", {}, "omni"),
    ]

    def test_dry_run_body_bytes_equal_sent_bytes_and_the_key_is_in_the_header_only(self):
        os.environ["GOOGLE_API_KEY"] = CANARY
        for case, route, inputs, kind in self.CASES:
            with self.subTest(route=route, case=case):
                t = image_ok() if kind == "image" else omni_ok()
                ad = self.make(route, t)
                row = self.row(case, route)
                dry = ad.dry_run(row, inputs)
                self.assertTrue(dry["would_dispatch"], (route, dry["refusal_reason"]))
                self.assertEqual(dry["headers"], {"x-goog-api-key": "<KEY:GOOGLE_API_KEY>", "Content-Type": "application/json"})
                self.assertTrue(any("GCP credits via the Gemini API key" in n for n in dry["request_notes"]))
                attempt = ad.dispatch(row, inputs)
                self.assertEqual(attempt["status"], "ok", (route, attempt["error_class"], attempt["raw_status_note"]))
                sent = t.calls[0]
                self.assertEqual(sent["payload"], S.canonical_json(dry["body"]))
                self.assertEqual(sent["url"], surfaces.REGISTRY.get(route).endpoint)
                self.assertEqual(sent["headers"]["x-goog-api-key"], CANARY)      # the fake saw it, in memory only
                self.assertNotIn(CANARY, sent["url"])
                self.assertNotIn(CANARY.encode(), sent["payload"])
                self.assertEqual(self.store.request_path(attempt["trial_id"]).read_bytes(), sent["payload"])
                self.assertEqual(attempt["config_hash"], B.sha256_hex(sent["payload"]))
                self.assertEqual((attempt["provider"], attempt["surface"], attempt["key_name"], attempt["credential_file_name"], attempt["billing_pool"]),
                                 ("gemini_api", "gemini_api", "GOOGLE_API_KEY", "~/.mi-keys", "credits"))
                self.assertEqual(attempt["headers_template"]["x-goog-api-key"], "<KEY:GOOGLE_API_KEY>")
                self.assertEqual(attempt["lifecycle_counts"]["submits"], 1)
                self.assertTrue(attempt["one_call_one_trial"])
                self.assertIsNotNone(attempt["artifact"])
                self.assertNotIn(CANARY, json.dumps(attempt))
        self.assertEqual(self._scan_tree(CANARY), [])

    def test_image_body_is_the_pinned_generate_content_shape(self):
        ad = self.make("nano-banana-2")
        d = ad.dry_run(self.row("IMG-CORE-01", "nano-banana-2"))
        b = d["body"]
        self.assertEqual(set(b), {"contents", "generationConfig"})
        self.assertEqual(b["generationConfig"], {"responseModalities": ["IMAGE"], "candidateCount": 1, "imageConfig": {"aspectRatio": B.aspect(self.row("IMG-CORE-01", "nano-banana-2"))}})
        self.assertIn(b["generationConfig"]["imageConfig"]["aspectRatio"], vertex_gemini_image.ALLOWED_ASPECTS)
        self.assertEqual(b["contents"][0]["role"], "user")
        self.assertEqual([list(p) for p in b["contents"][0]["parts"]], [["text"]])
        self.assertEqual(d["url"], "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image:generateContent")
        # the edit row (no aspect in the row) carries the references inline and no imageConfig: the model follows the references
        ad2 = self.make("nano-banana-pro-edit")
        d2 = ad2.dry_run(self.row("IMG-EDIT-01", "nano-banana-pro-edit"), {"reference_images": [(PNG_FIXTURE, "image/png")]})
        self.assertTrue(d2["would_dispatch"], d2["refusal_reason"])
        self.assertEqual(d2["body"]["generationConfig"], {"responseModalities": ["IMAGE"], "candidateCount": 1})
        self.assertEqual(d2["body"]["contents"][0]["parts"][1], {"inlineData": {"mimeType": "image/png", "data": B.b64(PNG_FIXTURE)}})
        self.assertTrue(any("imageConfig.aspectRatio omitted" in n for n in d2["request_notes"]))

    def test_image_body_is_byte_identical_to_the_vertex_body(self):
        """The same model takes the same request on both surfaces; only the URL and the credential differ."""
        for case, route, inputs in [("IMG-CORE-01", "nano-banana-2", {}), ("IMG-REF-01", "nano-banana-pro-edit", {"reference_images": [(PNG_FIXTURE, "image/png")] * 3})]:
            e = surfaces.REGISTRY.get(route)
            vertex_entry = dataclasses.replace(e, adapter="vertex_gemini_image", surface="vertex",
                                               endpoint=f"{surfaces.VERTEX_GLOBAL}/{e.surface_model_id}:generateContent",
                                               key_name=surfaces.GCP_KEY_NAME, credential_file_name=" | ".join(surfaces.GCP_CREDENTIAL_CANDIDATES))
            g = self.make(route).build_request(self.row(case, route), inputs)
            v = self.make(route, entry=vertex_entry, token_source=T.FakeTokenSource()).build_request(self.row(case, route), inputs)
            self.assertIsInstance(self.make(route, entry=vertex_entry, token_source=T.FakeTokenSource()), vertex_gemini_image.VertexGeminiImageAdapter)
            self.assertEqual(g.body_bytes, v.body_bytes, route)
            self.assertEqual(v.headers["Authorization"], "Bearer <TOKEN:gcloud-service-account>")
            self.assertTrue(v.url.startswith("https://aiplatform.googleapis.com/"))

    def test_omni_body_is_the_pinned_interactions_shape(self):
        ad = self.make("gemini-omni-1.1-flash")
        d = ad.dry_run(self.row("VID-T2V-01", "gemini-omni-1.1-flash"))
        b = d["body"]
        self.assertEqual(set(b), gemini_api_omni.BODY_FIELDS)
        self.assertEqual(b["model"], "gemini-omni-1.1-flash")
        self.assertEqual(b["input"], [{"type": "text", "text": self.row("VID-T2V-01", "gemini-omni-1.1-flash")["prompt"]}])
        self.assertEqual(b["response_format"], {"type": "video", "aspect_ratio": "9:16", "resolution": "720p", "duration": "6s"})
        self.assertEqual(b["generation_config"], {"video_config": {"task": "text_to_video"}})
        self.assertEqual(d["url"], "https://generativelanguage.googleapis.com/v1beta/interactions")
        self.assertNotIn("delivery", b["response_format"], "inline bytes are the documented default; no uri delivery, no polling")
        self.assertNotIn("previous_interaction_id", b)
        self.assertNotIn("background", b)
        # the -long row renders the page maximum 10 s and says so (as on Vertex)
        d2 = self.make("gemini-omni-1.1-flash-long").dry_run(self.row("VID-MS-01", "gemini-omni-1.1-flash-long"))
        self.assertEqual(d2["body"]["response_format"]["duration"], "10s")
        self.assertTrue(any("page maximum 10s" in n for n in d2["request_notes"]))
        # the Vertex Omni adapter still renders its own (Vertex) form for the preview id
        e = surfaces.REGISTRY.get("gemini-omni-1.1-flash")
        vertex_entry = dataclasses.replace(e, adapter="vertex_omni", surface="vertex", surface_model_id="gemini-omni-1.1-flash-preview",
                                           endpoint=surfaces.VERTEX_INTERACTIONS, key_name=surfaces.GCP_KEY_NAME)
        vad = self.make("gemini-omni-1.1-flash", entry=vertex_entry, token_source=T.FakeTokenSource())
        self.assertIsInstance(vad, vertex_omni.VertexOmniAdapter)
        vb = vad.build_request(self.row("VID-T2V-01", "gemini-omni-1.1-flash")).body
        self.assertEqual(vb["response_format"], [{"type": "video", "aspect_ratio": "9:16", "resolution": "720p", "duration": "6s"}])
        self.assertEqual(vb["model"], "gemini-omni-1.1-flash-preview")

    def test_edit_route_needs_reference_images_and_refuses_while_pending(self):
        e = surfaces.REGISTRY.get("nano-banana-pro-edit")
        row = self.row("IMG-REF-01", "nano-banana-pro-edit")
        self.assertEqual(INP.roles_needed(e, row), [(f"reference_asset_{i}", "reference_images") for i in (1, 2, 3)])
        ad = self.make("nano-banana-pro-edit", image_ok())
        d = ad.dry_run(row)
        self.assertFalse(d["would_dispatch"])
        self.assertEqual(d["refusal_reason"], "input_unresolved:reference_asset_1,reference_asset_2,reference_asset_3")
        os.environ["GOOGLE_API_KEY"] = "fake"
        with self.assertRaises(PreDispatchRefusal):
            ad.dispatch(row)
        self.assertEqual(self.budget.records(), [])

    def test_caller_parameters_are_refused(self):
        ad = self.make("gemini-omni-1.1-flash")
        for bad in ({"seed": 7}, {"duration": "9s"}, {"num_videos": 2}, {"response_format": {}}):
            with self.assertRaises(PreDispatchRefusal):
                ad.build_request(self.row("VID-T2V-01", "gemini-omni-1.1-flash"), bad)
        with self.assertRaises(PreDispatchRefusal):
            self.make("nano-banana-2").build_request(self.row("IMG-CORE-01", "nano-banana-2"), {"candidateCount": 2})


# ============================================================ the key: by name, at dispatch, nowhere else
class KeyTest(GeminiApiBase):
    def test_file_key_by_name_from_a_fake_path_never_reaches_disk_records_or_exceptions(self):
        self.write_fake_key("GOOGLE_API_KEY", CANARY)
        t = image_ok()
        ad = self.make("nano-banana-2", t)
        attempt = ad.dispatch(self.row("IMG-CORE-01", "nano-banana-2"))
        self.assertEqual(attempt["status"], "ok")
        self.assertEqual(t.calls[0]["headers"]["x-goog-api-key"], CANARY)
        self.assertEqual(self._scan_tree(CANARY), [])
        self.assertNotIn(CANARY, json.dumps(attempt))
        t2 = T.FakeTransport(posts=[TimeoutError("read timed out")])
        a2 = self.make("gemini-omni-1.1-flash", t2).dispatch(self.row("VID-T2V-01", "gemini-omni-1.1-flash"))
        self.assertEqual((a2["status"], a2["ambiguous_dispatch"], a2["outcome_resolved"]), ("timeout", True, False))
        self.assertNotIn(CANARY, json.dumps(a2))
        self.assertEqual(self._scan_tree(CANARY), [])

    def test_missing_key_refuses_before_any_send_and_releases_the_reservation(self):
        t = omni_ok()
        ad = self.make("gemini-omni-1.1-flash", t)
        with self.assertRaises(PreDispatchRefusal) as cm:
            ad.dispatch(self.row("VID-T2V-01", "gemini-omni-1.1-flash"))
        self.assertIn("GOOGLE_API_KEY", str(cm.exception))
        self.assertEqual(len(t.calls), 0)
        self.assertEqual(self.budget.spent_usd(), Decimal("0"))
        self.assertEqual([r["type"] for r in self.budget.records()], ["reservation", "release"])

    def test_no_other_key_name_and_no_other_host_can_carry_the_gemini_key(self):
        e = surfaces.REGISTRY.get("nano-banana-2")
        row = self.row("IMG-CORE-01", "nano-banana-2")
        for bad in (dataclasses.replace(e, key_name="FAL_KEY"),
                    dataclasses.replace(e, endpoint="https://aiplatform.googleapis.com/v1beta/models/x:generateContent"),
                    dataclasses.replace(e, endpoint=e.endpoint + "?key=abc"),
                    dataclasses.replace(e, endpoint=e.endpoint.replace("https://", "http://"))):
            with self.assertRaises(PreDispatchRefusal):
                self.make("nano-banana-2", image_ok(), entry=bad).build_request(row)
        os.environ["GOOGLE_API_KEY"] = "fake"
        o = surfaces.REGISTRY.get("gemini-omni-1.1-flash")
        bad = dataclasses.replace(o, endpoint="https://example.test/v1beta/interactions")
        t = omni_ok()
        with self.assertRaises(PreDispatchRefusal):
            self.make("gemini-omni-1.1-flash", t, entry=bad).dispatch(self.row("VID-T2V-01", "gemini-omni-1.1-flash"))
        self.assertEqual(len(t.calls), 0)
        self.assertEqual(self.budget.records(), [], "the guard fires in build_request, before any reservation")


# ============================================================ outcomes: classified as the Vertex variants classify them
class OutcomeTest(GeminiApiBase):
    def setUp(self):
        super().setUp()
        os.environ["GOOGLE_API_KEY"] = "fake"

    def _one(self, route, case, transport, repeat=1):
        ad = self.make(route, transport)
        attempt = ad.dispatch(self.row(case, route, repeat_index=repeat))
        self.assertEqual(transport.submits, 1)
        self.assertEqual(attempt["lifecycle_counts"]["submits"], 1)
        return attempt

    def test_image_safety_blocks_are_refusals(self):
        blocked_prompt = T.FakeTransport(posts=[(200, {"responseId": "r1", "promptFeedback": {"blockReason": "PROHIBITED_CONTENT"}, "candidates": []})])
        a = self._one("nano-banana-2", "IMG-CORE-01", blocked_prompt)
        self.assertEqual((a["status"], a["error_class"], a["billing_state"], a["outcome_resolved"]), ("refusal", "moderation_block", "reported", True))
        self.assertIn("PROHIBITED_CONTENT", a["raw_status_note"])
        self.assertEqual(a["provider_request_id"], "r1")
        blocked_image = T.FakeTransport(posts=[(200, {"responseId": "r2", "candidates": [{"finishReason": "IMAGE_SAFETY", "content": {"parts": []}}]})])
        a2 = self._one("nano-banana-pro", "IMG-CORE-01", blocked_image)
        self.assertEqual((a2["status"], a2["error_class"], a2["raw_status_note"]), ("refusal", "moderation_block", "IMAGE_SAFETY"))
        self.assertIsNone(a2["artifact"])
        self.assertEqual([r["type"] for r in self.budget.records()], ["reservation", "spend", "reservation", "spend"], "a refusal is a settled trial: reserved, then recorded")

    def test_image_malformed_replies_are_resolved_errors(self):
        bad_b64 = T.FakeTransport(posts=[(200, {"responseId": "r3", "candidates": [{"finishReason": "STOP", "content": {"parts": [{"inlineData": {"mimeType": "image/png", "data": "!!not-base64!!"}}]}}]})])
        a = self._one("nano-banana-2", "IMG-CORE-01", bad_b64)
        self.assertEqual((a["status"], a["error_class"], a["outcome_resolved"], a["ambiguous_dispatch"]), ("error", "malformed_response", True, False))
        not_json = T.FakeTransport(posts=[(200, {"$unparseable_body": True, "$bytes": 12})])
        a2 = self._one("nano-banana-2", "IMG-CORE-01", not_json, repeat=2)
        self.assertEqual((a2["status"], a2["error_class"]), ("error", "malformed_response"))
        no_image = T.FakeTransport(posts=[(200, {"responseId": "r4", "candidates": [{"finishReason": "STOP", "content": {"parts": [{"text": "I cannot draw that"}]}}]})])
        a3 = self._one("nano-banana-pro", "IMG-CORE-01", no_image)
        self.assertEqual((a3["status"], a3["error_class"]), ("error", "no_artifact_returned"))
        for x in (a, a2, a3):
            self.assertEqual(x["billing_state"], "reported")

    def test_image_4xx_is_a_resolved_provider_error_named_by_status(self):
        t = T.FakeTransport(posts=[(400, {"error": {"code": 400, "message": "Invalid value at 'generation_config.image_config'", "status": "INVALID_ARGUMENT"}})])
        a = self._one("nano-banana-2", "IMG-CORE-01", t)
        self.assertEqual((a["status"], a["error_class"], a["ambiguous_dispatch"]), ("error", "INVALID_ARGUMENT", False))

    def test_omni_safety_block_failed_and_incomplete(self):
        blocked = T.FakeTransport(posts=[(200, {"id": "v1_b", "status": "failed", "errors": [{"code": "https://ai.google.dev/errors/blocked", "message": "The prompt was blocked by the content safety filter."}]})])
        a = self._one("gemini-omni-1.1-flash", "VID-T2V-01", blocked)
        self.assertEqual((a["status"], a["error_class"], a["outcome_resolved"], a["provider_request_id"]), ("refusal", "moderation_block", True, "v1_b"))
        self.assertIn("safety", a["raw_status_note"])
        failed = T.FakeTransport(posts=[(200, {"id": "v1_f", "status": "failed", "errors": [{"code": "internal", "message": "Internal error encountered."}]})])
        a2 = self._one("gemini-omni-1.1-flash", "VID-T2V-01", failed, repeat=2)
        self.assertEqual((a2["status"], a2["error_class"]), ("error", "interaction_failed"))
        incomplete = T.FakeTransport(posts=[(200, {"id": "v1_i", "status": "incomplete", "steps": []})])
        a3 = self._one("gemini-omni-1.1-flash-10s", "VID-MS-02", incomplete)
        self.assertEqual((a3["status"], a3["error_class"]), ("error", "interaction_incomplete"))
        uri_only = T.FakeTransport(posts=[(200, {"id": "v1_u", "status": "completed", "steps": [{"type": "model_output", "content": [{"type": "video", "mime_type": "video/mp4", "uri": "https://generativelanguage.googleapis.com/v1beta/files/x:download?alt=media"}]}]})])
        a4 = self._one("gemini-omni-1.1-flash-10s", "VID-MS-02", uri_only, repeat=2)
        self.assertEqual((a4["status"], a4["error_class"]), ("error", "artifact_not_inline"))
        for x in (a, a2, a3, a4):
            self.assertEqual((x["billing_state"], x["ambiguous_dispatch"]), ("reported", False))

    def test_omni_malformed_replies(self):
        bad_b64 = T.FakeTransport(posts=[(200, {"id": "v1_m", "status": "completed", "steps": [{"type": "model_output", "content": [{"type": "video", "mime_type": "video/mp4", "data": "%%%"}]}]})])
        a = self._one("gemini-omni-1.1-flash", "VID-T2V-01", bad_b64)
        self.assertEqual((a["status"], a["error_class"]), ("error", "malformed_response"))
        not_json = T.FakeTransport(posts=[(200, {"$unparseable_body": True, "$bytes": 5})])
        a2 = self._one("gemini-omni-1.1-flash", "VID-T2V-01", not_json, repeat=2)
        self.assertEqual((a2["status"], a2["error_class"]), ("error", "malformed_response"))
        empty = T.FakeTransport(posts=[(200, {"id": "v1_e", "status": "completed", "steps": [{"type": "thought", "content": []}]})])
        a3 = self._one("gemini-omni-1.1-flash-10s", "VID-MS-02", empty)
        self.assertEqual((a3["status"], a3["error_class"]), ("error", "no_artifact_returned"))

    def test_429_and_5xx_after_the_submit_are_ambiguous_and_never_resubmitted(self):
        for code in (429, 503):
            with self.subTest(code=code):
                t = T.FakeTransport(posts=[(code, {"error": {"code": code, "message": "try later", "status": "RESOURCE_EXHAUSTED"}})])
                a = self._one("gemini-omni-1.1-flash", "VID-T2V-01", t, repeat=1 if code == 429 else 2)
                self.assertEqual((a["status"], a["error_class"], a["ambiguous_dispatch"], a["outcome_resolved"], a["billing_state"]),
                                 ("error", f"http_{code}", True, False, "unknown_provisional"))
                self.assertEqual(a["retries"], 0)


if __name__ == "__main__":
    unittest.main()
