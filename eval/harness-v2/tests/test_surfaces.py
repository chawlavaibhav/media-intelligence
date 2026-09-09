"""Test (n): SurfaceRegistry keys == route_catalogue keys; entries map to the roster."""
import hashlib
import subprocess
import unittest

import yaml

from _support import HV2, hv2_paths  # noqa: F401
import surfaces


def _committed(path_rel: str) -> dict:
    """The freeze package at the committed HEAD (the working tree may be mid-edit by another role)."""
    raw = subprocess.run(["git", "show", f"HEAD:{path_rel}"], cwd=hv2_paths.REPO_ROOT,
                         capture_output=True, check=True).stdout
    return yaml.safe_load(raw.decode("utf-8"))


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
        self.assertEqual(len(self.reg.catalogue_keys()), 49)   # 47 frozen + the two ElevenLabs direct routes (2026-09-09)
        # EXTENSION_ROUTES are registered but deliberately outside the freeze catalogue (no TEST-CASES / COST-TABLE row)
        self.assertEqual(set(surfaces.EXTENSION_ROUTES), self.reg.keys() - set(self.catalogue))
        self.assertEqual(len(self.reg), 49 + len(surfaces.EXTENSION_ROUTES))

    def test_every_entry_names_adapter_surface_and_schema(self):
        for e in self.reg:
            self.assertIn(e.adapter, ("fal_queue", "vertex_veo", "vertex_gemini_image", "vertex_omni",
                                      "vertex_lyria", "sarvam_tts", "elevenlabs_direct", "none"), e.route_key)
            self.assertTrue(e.surface_model_id, e.route_key)
            self.assertTrue(e.params_schema, e.route_key)
            self.assertIn(e.shape_status, ("verified", "unverified", "not_built"), e.route_key)
            self.assertIn(e.billing_pool, ("cash", "credits", "sarvam_credits", "elevenlabs_credits"), e.route_key)

    def test_surface_and_pool_agree_with_the_catalogue(self):
        for key, cat in self.catalogue.items():
            e = self.reg.get(key)
            self.assertEqual(e.billing_pool, cat["billing_pool"], key)
            cat_surface = {"fal": "fal", "vertex": "vertex", "direct": "sarvam_direct", "bedrock": "bedrock",
                           "azure": "azure_foundry", "elevenlabs_direct": "elevenlabs_direct"}[cat["surface"]]
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
                                       surfaces.GCP_KEY_NAME, "none (no adapter)"))

    def test_unknown_key_is_refused(self):
        with self.assertRaises(KeyError):
            self.reg.get("not-a-route")

    def test_extend_is_two_calls_in_one_trial(self):
        self.assertEqual(self.reg.get("veo-3.1-fast-extend").api_calls_per_trial, 2)
        self.assertEqual(sum(1 for e in self.reg if e.api_calls_per_trial != 1), 1)


class RePinnedFalRoutesTest(unittest.TestCase):
    """2026-09-09 re-check of the two price-unpinned fal routes: every pin file hashes true and carries its evidence quotes;
    sync-lipsync-v3 carries the exact id's endpointBilling record (USD 8 per output minute); kling-v3-elements has no model,
    no schema and no price and stays unpinned/unverified."""
    PINS = hv2_paths.REPO_ROOT / "eval/empirical-planning/price-pins-2026-09"

    def _index(self, name):
        idx = yaml.safe_load((self.PINS / name / "PIN-INDEX.yaml").read_text(encoding="utf-8"))
        self.assertTrue(idx["pins"], name)
        for pin in idx["pins"]:
            f = hv2_paths.REPO_ROOT / pin["pin_file"]
            self.assertTrue(f.exists(), pin["pin_file"])
            data = f.read_bytes()
            self.assertEqual(len(data), pin["bytes"], pin["pin_file"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), pin["sha256"], pin["pin_file"])
            for q in [pin["evidence_quote"]] + (pin.get("additional_evidence_quotes") or []):
                self.assertIn(q.encode("utf-8"), data, (pin["pin_file"], q))
            self.assertTrue(pin["fetch_command"].startswith('curl -sL -A "Mozilla/5.0" '), pin["pin_file"])
            self.assertIn(pin["pin_kind"], ("price", "page_only", "schema_page"), pin["pin_file"])
        return idx

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
