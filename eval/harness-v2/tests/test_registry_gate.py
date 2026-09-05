"""Test (l): the registry gate and BatteryHarness.

    - assert_registry_eligible refuses a capability outside EVALUATOR-PLAN.deterministic_capabilities,
      an instrument that is not deterministic / qualified, and a synthetic measurement;
    - BatteryHarness.write_registry_row IS Harness.write_registry_row (inherited, never overridden);
    - BatteryHarness.generate() stores bytes and measure() hands the instrument a PATH;
    - attach_uncertainty fills SCHEMA-v1 uncertainty with an exact Clopper-Pearson interval, computed over
      base items, independence NOT ESTABLISHED, is_reference_calculation_only true;
    - measurements_to_cell derives n_items / repeats / trials / passes / absence_reason.
This task writes no Registry row: every harness here lives in a temp dir and nothing under eval/registry/ is touched.
"""
import unittest

from _support import NoNetworkTestCase, hv2_paths
import battery_harness as BH
from instruments import registry_gate as RG
from instruments import imageio as IO
import harness as H
import models as M


def det_instrument(iid="probe", caps=("delivery_format_compliance",), status="deterministic", fn=None):
    return H.Instrument(iid, "1.0", {"t": 1}, qualification_status=status, capabilities=caps, observation_unit="artifact",
                        fn=fn or (lambda path, item, cap: {"verdict": "pass"}))


class RegistryGateTest(NoNetworkTestCase):
    def test_eligible_capabilities_are_exactly_the_eight(self):
        self.assertEqual(RG.deterministic_capabilities(), {"delivery_format_compliance", "edit_preservation", "packaging_brand_colour_fidelity",
                                                            "audio_video_synchronisation", "reliability_pass_at_k", "cost_and_cpao",
                                                            "latency_errors_refusals", "reproducibility"})

    def test_refusals(self):
        RG.assert_registry_eligible("delivery_format_compliance", det_instrument())
        with self.assertRaises(RG.RegistryGateRefused):
            RG.assert_registry_eligible("hierarchy_product_as_hero", det_instrument(caps=("hierarchy_product_as_hero",)))
        with self.assertRaises(RG.RegistryGateRefused):
            RG.assert_registry_eligible("delivery_format_compliance", det_instrument(status="provisional"))
        with self.assertRaises(RG.RegistryGateRefused):
            RG.assert_registry_eligible("delivery_format_compliance", det_instrument(status="screened_not_qualified"))
        with self.assertRaises(RG.RegistryGateRefused):
            RG.assert_registry_eligible("edit_preservation", det_instrument())        # instrument not specified for it
        m = M.Measurement("m1", "a", "a", "i", "delivery_format_compliance", "pass", instrument_id="probe", synthetic=True)
        with self.assertRaises(RG.RegistryGateRefused):
            RG.assert_measurements_real([m])

    def test_clopper_pearson_reference_values(self):
        lo, hi = RG.clopper_pearson(0, 10)
        self.assertEqual(lo, 0.0)
        self.assertAlmostEqual(hi, 0.3085, places=3)
        lo, hi = RG.clopper_pearson(10, 10)
        self.assertAlmostEqual(lo, 0.6915, places=3)
        self.assertEqual(hi, 1.0)
        lo, hi = RG.clopper_pearson(5, 10)
        self.assertAlmostEqual(lo, 0.1871, places=3)
        self.assertAlmostEqual(hi, 0.8129, places=3)
        with self.assertRaises(ValueError):
            RG.clopper_pearson(3, 0)

    def test_attach_uncertainty_shape(self):
        row = {"n_items": 10, "repeats_per_item": 2, "trials": 20, "passes": 7}
        u = RG.attach_uncertainty(row)["uncertainty"]
        self.assertEqual(u["status"], "computed")
        self.assertEqual(u["method"], "clopper_pearson_95")
        self.assertEqual(u["computed_over"], "base_items")
        self.assertEqual(u["n_used"], 10)
        self.assertEqual(u["independence_status"], "NOT ESTABLISHED")
        self.assertTrue(u["is_reference_calculation_only"])
        self.assertEqual(u["interval_level"], 0.95)
        self.assertTrue(0 <= u["interval_low"] <= u["interval_high"] <= 1)
        self.assertTrue(any("iid" in a or "independen" in a for a in u["assumptions"]))

    def test_measurements_to_cell(self):
        ms = [M.Measurement(f"m{i}", f"a{i}", f"a{i}", f"item{i % 3}", "delivery_format_compliance", v, absence_reason=ar, instrument_id="probe")
              for i, (v, ar) in enumerate([("pass", None), ("fail", None), ("pass", None), ("absent", "parse_failure"), ("pass", None), ("fail", None)])]
        cell = RG.measurements_to_cell(ms)
        self.assertEqual((cell["n_items"], cell["trials"], cell["passes"], cell["fails"], cell["absent"]), (3, 6, 3, 2, 1))
        self.assertEqual(cell["repeats_per_item"], 2)
        self.assertEqual(cell["absence_reasons"], {"parse_failure": 1})
        self.assertEqual(cell["absence_reason"], "parse_failure")
        self.assertIsNone(RG.measurements_to_cell(ms[:1])["absence_reason"])


class BatteryHarnessTest(NoNetworkTestCase):
    def test_write_registry_row_is_inherited_not_overridden(self):
        self.assertIs(BH.BatteryHarness.write_registry_row, H.Harness.write_registry_row)
        self.assertTrue(issubclass(BH.BatteryHarness, H.Harness))
        self.assertNotIn("write_registry_row", BH.BatteryHarness.__dict__)

    def test_generate_stores_bytes_and_measure_hands_a_path(self):
        hz = BH.BatteryHarness(self.tmp / "hz")
        png = IO.encode_png([b"\x01\x02\x03" * 4] * 4, 4, 4)
        seen = {}

        def fn(path, item, cap):
            seen["path"] = path
            seen["bytes"] = path.read_bytes()
            return {"verdict": "absent", "absence_reason": "other", "note": "criterion_not_frozen"}
        hz.register_instrument(det_instrument(fn=fn))
        item = {"item_id": "IMG-CORE-01", "measurement_fanout": ["delivery_format_compliance"]}
        prov = hz.generate(item, {"provider": "fal", "model": "m", "version": "v", "endpoint": "e", "workflow": "t2i", "lane": "image",
                                  "media_kind": "image", "currency": "USD"},
                           lambda it, cfg: {"api_status": "ok", "payload_bytes": png, "content_type": "image/png", "cost_generation": 0.05})
        self.assertTrue(prov.output_path.endswith(".png"))
        self.assertEqual(prov.output_bytes, len(png))
        m = hz.measure(prov.asset_id, "delivery_format_compliance", "probe", item, observation_unit="artifact")
        self.assertEqual(seen["bytes"], png)
        self.assertEqual(str(seen["path"]), prov.output_path)
        self.assertEqual(m.verdict, "absent")
        self.assertTrue(m.synthetic, "the frozen harness marks every measurement synthetic; a battery row is built through a separate real path")
        with self.assertRaises(TypeError):
            hz.generate({**item, "item_id": "x"}, {"lane": "image"}, lambda it, cfg: {"api_status": "ok", "payload": "text pretending to be media"})

    def test_registry_write_through_battery_harness_is_refused_for_ineligible_input(self):
        hz = BH.BatteryHarness(self.tmp / "hz")
        hz.register_instrument(det_instrument(status="provisional"))
        with self.assertRaises(H.HarnessError):
            hz.write_registry_row("delivery_format_compliance", "probe", [], {}, 1, 1)
        with self.assertRaises(RG.RegistryGateRefused):
            hz.registry_row_for("hierarchy_product_as_hero", "probe", [], {}, 1, 1)


if __name__ == "__main__":
    unittest.main()
