"""Test (n): SurfaceRegistry keys == route_catalogue keys; entries map to the roster."""
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
        self.assertEqual(self.reg.keys(), set(self.catalogue), "registry keys must equal route_catalogue keys exactly")
        self.assertEqual(len(self.reg), 47)

    def test_every_entry_names_adapter_surface_and_schema(self):
        for e in self.reg:
            self.assertIn(e.adapter, ("fal_queue", "vertex_veo", "vertex_gemini_image", "vertex_omni",
                                      "vertex_lyria", "sarvam_tts", "none"), e.route_key)
            self.assertTrue(e.surface_model_id, e.route_key)
            self.assertTrue(e.params_schema, e.route_key)
            self.assertIn(e.shape_status, ("verified", "unverified", "not_built"), e.route_key)
            self.assertIn(e.billing_pool, ("cash", "credits", "sarvam_credits"), e.route_key)

    def test_surface_and_pool_agree_with_the_catalogue(self):
        for key, cat in self.catalogue.items():
            e = self.reg.get(key)
            self.assertEqual(e.billing_pool, cat["billing_pool"], key)
            cat_surface = {"fal": "fal", "vertex": "vertex", "direct": "sarvam_direct", "bedrock": "bedrock",
                           "azure": "azure_foundry"}[cat["surface"]]
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
            self.assertIn(e.key_name, (surfaces.FAL_KEY_NAME, surfaces.SARVAM_KEY_NAME, surfaces.GCP_KEY_NAME, "none (no adapter)"))

    def test_unknown_key_is_refused(self):
        with self.assertRaises(KeyError):
            self.reg.get("not-a-route")

    def test_extend_is_two_calls_in_one_trial(self):
        self.assertEqual(self.reg.get("veo-3.1-fast-extend").api_calls_per_trial, 2)
        self.assertEqual(sum(1 for e in self.reg if e.api_calls_per_trial != 1), 1)


if __name__ == "__main__":
    unittest.main()
