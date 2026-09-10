"""Test (n): SurfaceRegistry keys == route_catalogue keys; entries map to the roster."""
import hashlib
import unittest

import yaml

from _support import HV2, hv2_paths  # noqa: F401
import surfaces


def _committed(path_rel: str) -> dict:
    """The freeze package the registry must match: the WORKING TREE (the same files pricing.CostTable() and run_live's
    Pricing() read), so a package rebuild and its registry entries are checked together before they are committed.
    2026-09-09 (Wan 2 contender): until then this read HEAD, which made every package change fail here until committed;
    HEAD-vs-item-basis drift is run_live's own check (`freeze_matches_item_basis`)."""
    return yaml.safe_load((hv2_paths.REPO_ROOT / path_rel).read_text(encoding="utf-8"))


class SurfaceRegistryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import casebook as CB
        tc = _committed("eval/empirical-planning/STAGE-A-FREEZE-2026-09/TEST-CASES.yaml")
        ct = _committed("eval/empirical-planning/STAGE-A-FREEZE-2026-09/COST-TABLE.yaml")
        cls.catalogue = CB.resolve_catalogue(tc, ct)     # TEST-CASES carries a pointer to COST-TABLE since 0596aa2
        cls.reg = surfaces.REGISTRY

    def test_keys_equal_the_route_catalogue(self):
        self.assertEqual(self.reg.catalogue_keys(), set(self.catalogue), "registry keys (minus the extension routes) must equal route_catalogue keys exactly")
        self.assertEqual(len(self.reg.catalogue_keys()), 51)   # 47 frozen + the two ElevenLabs direct routes + the two Wan 2 contender routes (2026-09-09)
        # EXTENSION_ROUTES are registered but deliberately outside the freeze catalogue (no TEST-CASES / COST-TABLE row)
        self.assertEqual(set(surfaces.EXTENSION_ROUTES), self.reg.keys() - set(self.catalogue))
        self.assertEqual(len(self.reg), 51 + len(surfaces.EXTENSION_ROUTES))

    def test_every_entry_names_adapter_surface_and_schema(self):
        for e in self.reg:
            self.assertIn(e.adapter, ("fal_queue", "vertex_veo", "vertex_gemini_image", "vertex_omni", "gemini_api_image", "gemini_api_omni",
                                      "vertex_lyria", "sarvam_tts", "elevenlabs_direct", "none"), e.route_key)
            self.assertTrue(e.surface_model_id, e.route_key)
            self.assertTrue(e.params_schema, e.route_key)
            self.assertIn(e.shape_status, ("verified", "unverified", "not_built"), e.route_key)
            self.assertIn(e.billing_pool, ("cash", "credits", "sarvam_credits", "elevenlabs_credits"), e.route_key)

    def test_surface_and_pool_agree_with_the_catalogue(self):
        for key, cat in self.catalogue.items():
            e = self.reg.get(key)
            if key in surfaces.GEMINI_API_REPOINT_PENDING_PACKAGE:
                # a registry re-point the committed package has not been rebuilt for: the package records the pre-decision surface / pool
                # EXACTLY as the table says (empty since the 2026-09-10 rebuild; a rebuild that re-points a key must delete its row)
                self.assertEqual((cat["surface"], cat["billing_pool"]), surfaces.GEMINI_API_REPOINT_PENDING_PACKAGE[key], key)
                self.assertEqual((e.surface, e.billing_pool, e.key_name), ("gemini_api", "credits", surfaces.GEMINI_API_KEY_NAME), key)
                continue
            self.assertEqual(e.billing_pool, cat["billing_pool"], key)
            cat_surface = {"fal": "fal", "vertex": "vertex", "direct": "sarvam_direct", "bedrock": "bedrock",
                           "azure": "azure_foundry", "elevenlabs_direct": "elevenlabs_direct", "gemini_api": "gemini_api"}[cat["surface"]]
            if key == "chirp-3-hd-hi-in":
                cat_surface = "cloud_tts"
            self.assertEqual(e.surface, cat_surface, key)

    def test_roster_key_and_variant_agree_with_the_catalogue(self):
        for key, cat in self.catalogue.items():
            e = self.reg.get(key)
            rk = cat["roster_route_key"]
            if " / variant " in rk:
                roster_key, variant = rk.split(" / variant ")
            else:
                roster_key, variant = rk, None
            self.assertEqual(e.roster_key, roster_key, key)
            self.assertEqual(e.roster_variant, variant, key)

    def test_not_built_entries_refuse_by_construction(self):
        for key in ("sd3.5-large", "mai-image-2.6", "sora-2", "chirp-3-hd-hi-in", "azure-neural-tts-hi-in"):
            e = self.reg.get(key)
            self.assertEqual(e.adapter, "none")
            self.assertEqual(e.shape_status, "not_built")
        for key in ("mai-image-2.6", "sora-2", "azure-neural-tts-hi-in"):
            self.assertIn(surfaces.AZURE_PRECONDITION, self.reg.get(key).dispatch_preconditions)

    def test_no_key_value_anywhere_in_the_registry(self):
        blob = str(self.reg.as_dict())
        self.assertNotIn("BEGIN PRIVATE" + " KEY", blob)      # split so the Tester grep never hits this file
        for e in self.reg:
            self.assertIn(e.key_name, (surfaces.FAL_KEY_NAME, surfaces.SARVAM_KEY_NAME, surfaces.ELEVENLABS_KEY_NAME,
                                       surfaces.GCP_KEY_NAME, surfaces.GEMINI_API_KEY_NAME, "none (no adapter)"))

    def test_unknown_key_is_refused(self):
        with self.assertRaises(KeyError):
            self.reg.get("not-a-route")

    def test_extend_is_two_calls_in_one_trial(self):
        self.assertEqual(self.reg.get("veo-3.1-fast-extend").api_calls_per_trial, 2)
        self.assertEqual(sum(1 for e in self.reg if e.api_calls_per_trial != 1), 1)


PINS_ROOT = hv2_paths.REPO_ROOT / "eval/empirical-planning/price-pins-2026-09"


def verified_pin_index(tc: unittest.TestCase, name: str) -> dict:
    """Load <pins>/<name>/PIN-INDEX.yaml and prove every pin: the file exists, bytes and sha256 match, every evidence quote is a
    verbatim substring of the bytes, the fetch was a plain unauthenticated curl, and the pin kind is one this programme uses."""
    idx = yaml.safe_load((PINS_ROOT / name / "PIN-INDEX.yaml").read_text(encoding="utf-8"))
    tc.assertTrue(idx["pins"], name)
    for pin in idx["pins"]:
        f = hv2_paths.REPO_ROOT / pin["pin_file"]
        tc.assertTrue(f.exists(), pin["pin_file"])
        data = f.read_bytes()
        tc.assertEqual(len(data), pin["bytes"], pin["pin_file"])
        tc.assertEqual(hashlib.sha256(data).hexdigest(), pin["sha256"], pin["pin_file"])
        for q in [pin["evidence_quote"]] + (pin.get("additional_evidence_quotes") or []):
            tc.assertIn(q.encode("utf-8"), data, (pin["pin_file"], q))
        tc.assertTrue(pin["fetch_command"].startswith('curl -sL -A "Mozilla/5.0" '), pin["pin_file"])
        tc.assertIn(pin["pin_kind"], ("price", "page_only", "schema_page"), pin["pin_file"])
    return idx


class GeminiApiSurfaceTest(unittest.TestCase):
    """2026-09-09: the Gemini-named routes are re-pointed to the Gemini Developer API. The pins hash true, the exact price strings the
    registry quotes are in the pinned pricing bytes, and the schema index's evidence quotes are in the pinned doc / reference bytes."""
    ROUTES = ("nano-banana-2", "nano-banana-pro", "nano-banana-pro-edit", "gemini-omni-1.1-flash", "gemini-omni-1.1-flash-10s", "gemini-omni-1.1-flash-long")

    def test_pins_hash_true_and_cover_every_route(self):
        idx = verified_pin_index(self, "gemini-api")
        self.assertEqual((idx["surface"], idx["billing_pool"], idx["billing_note"]), ("gemini_api", "credits", surfaces.GEMINI_API_BILLING_NOTE))
        self.assertIn("GOOGLE_API_KEY", idx["key_name"])
        by_route = {}
        for p in idx["pins"]:
            by_route.setdefault(p["route_key"], set()).add(p["pin_kind"])
        self.assertEqual(set(by_route), set(self.ROUTES) - {"gemini-omni-1.1-flash-10s", "gemini-omni-1.1-flash-long"} | {"gemini-omni-1.1-flash-10s", "gemini-omni-1.1-flash-long"})
        for key in self.ROUTES:
            self.assertIn("schema_page", by_route[key], key)
        for key in ("nano-banana-2", "nano-banana-pro", "nano-banana-pro-edit", "gemini-omni-1.1-flash"):
            self.assertIn("price", by_route[key], key)
        # what the Gemini API exposes is recorded on the index, with the Omni answer (Interactions API, no generateContent video form)
        self.assertIn("Interactions API", idx["what_the_gemini_api_exposes"]["omni_video"])
        self.assertIn("generateContent", idx["what_the_gemini_api_exposes"]["image"])

    def test_registry_price_strings_are_the_pinned_pricing_bytes(self):
        pricing_pin = hv2_paths.REPO_ROOT / surfaces.GEMINI_API_PRICING_PIN
        data = pricing_pin.read_bytes()
        for model_id, quote in surfaces.GEMINI_API_PRICES.items():
            self.assertIn(quote.encode("utf-8"), data, (model_id, quote))
            self.assertIn(model_id.encode("utf-8"), data)
        for q in (b"5,792 tokens per second of 720p video", b"approximately $0.10 per second", b"Image input is set at 560 tokens", b"$0.0011 per image"):
            self.assertIn(q, data)
        idx = verified_pin_index(self, "gemini-api")
        price_rows = {p["route_key"]: p for p in idx["pins"] if p["pin_kind"] == "price"}
        self.assertEqual(price_rows["nano-banana-2"]["evidence_quote"], "$0.067 per 1K image")
        self.assertEqual(price_rows["nano-banana-pro"]["evidence_quote"], "$0.134 per 1K/2K image")
        self.assertEqual(price_rows["nano-banana-pro-edit"]["usd_per_input_image"], 0.0011)
        self.assertEqual(price_rows["gemini-omni-1.1-flash"]["evidence_quote"], "$17.50 (video)")
        self.assertEqual(price_rows["gemini-omni-1.1-flash"]["usd_per_second_720p_derived"], 0.10136)
        self.assertEqual(round(17.5 * 5792 / 1_000_000, 5), 0.10136)
        for key in self.ROUTES:
            e = surfaces.REGISTRY.get(key)
            self.assertEqual(e.price_pin_ref, surfaces.GEMINI_API_PRICING_PIN)
            self.assertIn(surfaces.GEMINI_API_PRICES[e.surface_model_id], e.notes, key)

    def test_schema_index_quotes_are_in_the_pinned_doc_bytes(self):
        idx = yaml.safe_load((hv2_paths.REPO_ROOT / surfaces.GEMINI_API_SCHEMA).read_text(encoding="utf-8"))
        sources = {s["id"]: s for s in idx["sources"]}
        for shape_id, shape in idx["shapes"].items():
            blobs = [(hv2_paths.REPO_ROOT / sources[s]["pin_file"]).read_bytes() for s in shape["sources"] if "pin_file" in sources[s]]
            self.assertTrue(blobs, shape_id)
            for q in shape["evidence_quotes"]:
                self.assertTrue(any(q.encode("utf-8") in b for b in blobs), (shape_id, q))
        for key in self.ROUTES:
            self.assertTrue(surfaces.REGISTRY.get(key).params_schema.startswith(surfaces.GEMINI_API_SCHEMA + "#"), key)
        self.assertEqual(set(idx["shapes"]), {"gemini_image", "omni_interactions"})


class RePinnedFalRoutesTest(unittest.TestCase):
    """2026-09-09 re-check of the two price-unpinned fal routes: every pin file hashes true and carries its evidence quotes;
    sync-lipsync-v3 carries the exact id's endpointBilling record (USD 8 per output minute); kling-v3-elements has no model,
    no schema and no price and stays unpinned/unverified."""
    PINS = PINS_ROOT

    def _index(self, name):
        return verified_pin_index(self, name)

    def test_sync_lipsync_v3_exact_id_price_is_in_both_page_fetches(self):
        idx = self._index("sync-lipsync-v3")
        price_pins = [p for p in idx["pins"] if p["pin_kind"] == "price"]
        self.assertEqual(len(price_pins), 2, "the 2026-09-09 page and the 2026-09-04 page both carry the record")
        record = b'endpointBilling\\":{\\"endpoint\\":\\"fal-ai/sync-lipsync/v3\\",\\"billing_unit\\":\\"minutes\\",\\"price\\":8'
        for p in price_pins:
            self.assertEqual(p["evidence_quote"].encode("utf-8"), record)
            self.assertEqual(p["url"], "https://fal.ai/models/fal-ai/sync-lipsync/v3")
        e = surfaces.REGISTRY.get("sync-lipsync-v3")
        self.assertEqual(e.price_pin_ref, "eval/empirical-planning/price-pins-2026-09/sync-lipsync-v3/fal-sync-lipsync-v3-2026-09-09.html")
        self.assertIn(record, (hv2_paths.REPO_ROOT / e.price_pin_ref).read_bytes())
        self.assertEqual(e.shape_status, "verified")
        self.assertIn("USD 8.00 per output minute", e.notes)
        # the JSON search result still has no price field on the exact id (the reason the route was unpinned) - only the page does
        js = [p for p in idx["pins"] if p["pin_file"].endswith("fal-api-models-sync-lipsync-v3.json")][0]
        self.assertEqual(js["pin_kind"], "page_only")
        self.assertNotIn(b"endpointBilling", (hv2_paths.REPO_ROOT / js["pin_file"]).read_bytes())

    def test_kling_v3_elements_has_no_model_no_schema_and_no_price(self):
        import json
        idx = self._index("kling-v3-elements")
        self.assertEqual({p["pin_kind"] for p in idx["pins"]}, {"page_only"}, "nothing in this directory is a price")
        by_status = {p["http_status"]: p for p in idx["pins"]}
        self.assertIn("404", by_status)
        search = [p for p in idx["pins"] if p["pin_file"].endswith("-search.json")][0]
        doc = json.loads((hv2_paths.REPO_ROOT / search["pin_file"]).read_bytes())
        ids = [m["id"] for m in doc["items"]]
        self.assertEqual(len(ids), doc["total"])
        self.assertNotIn("fal-ai/kling-video/v3/pro/elements", ids)
        e = surfaces.REGISTRY.get("kling-v3-elements")
        self.assertIsNone(e.price_pin_ref)
        self.assertEqual(e.shape_status, "unverified")
        self.assertNotIn("#", e.params_schema, "no pinned Input component exists for this id")
        self.assertIn("2026-09-09", e.notes)


if __name__ == "__main__":
    unittest.main()
