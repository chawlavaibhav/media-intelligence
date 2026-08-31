"""Positive and negative fixtures for the compiled-pack validator (REP-05).

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

Each negative test mutates a committed artifact in one way and asserts the validator refuses
it — every rule in canon/compilation/COMPILED-DOCTRINE-SPEC-v0.md is mechanically enforced,
not merely written down. Run: python3 -m unittest tests.test_compiled_packs
"""
import tempfile
import unittest
from pathlib import Path

import yaml

from canon.validation import validate_compiled_pack as vcp

REPO_ROOT = Path(__file__).resolve().parents[1]
PA = REPO_ROOT / "canon/compilation/PACK-product_appearance-v0.yaml"
CA = REPO_ROOT / "canon/compilation/PACK-composition_and_attention-v0.yaml"
TRIGGERS = REPO_ROOT / "canon/packs/pack-triggers-v0.yaml"


class CompiledPackValidatorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.env = vcp.load_environment()
        errors = []
        cls.digest = vcp.recompute_corpus_digest(errors)
        assert not errors, errors
        cls.pa = yaml.safe_load(PA.read_text())
        cls.ca = yaml.safe_load(CA.read_text())

    # ── helpers ─────────────────────────────────────────────────────────
    def check_pack(self, doc) -> list:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "PACK-product_appearance-v0.yaml"
            path.write_text(yaml.safe_dump(doc, sort_keys=True, allow_unicode=True))
            return vcp.validate_pack(path, self.env, self.digest)

    def check_triggers(self, doc) -> list:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "pack-triggers-v0.yaml"
            path.write_text(yaml.safe_dump(doc, sort_keys=True, allow_unicode=True))
            return vcp.validate_triggers(path, self.env)

    def mutate(self, doc):
        return yaml.safe_load(yaml.safe_dump(doc))

    def assertRefused(self, errors, needle):
        self.assertTrue(errors, "expected the validator to refuse this artifact")
        self.assertIn(needle, " | ".join(errors))

    # ── the committed artifacts ─────────────────────────────────────────
    def test_committed_packs_pass(self):
        self.assertEqual(vcp.validate_pack(PA, self.env, self.digest), [])
        self.assertEqual(vcp.validate_pack(CA, self.env, self.digest), [])

    def test_committed_trigger_table_passes(self):
        self.assertEqual(vcp.validate_triggers(TRIGGERS, self.env), [])

    def test_round_tripped_pack_still_passes(self):
        self.assertEqual(self.check_pack(self.mutate(self.pa)), [])

    def test_full_validator_main_exits_zero(self):
        self.assertEqual(vcp.main([]), 0)

    # ── check 7: determinism ────────────────────────────────────────────
    def test_double_compile_is_byte_identical_with_committed(self):
        self.assertEqual(vcp.validate_reproducibility(), [])

    # ── check 1: accepted corpus only, audit-complete, no HOLD ──────────
    def test_unknown_id_is_refused(self):
        doc = self.mutate(self.pa)
        doc["decisions"][0]["compiled_from"][0]["ref"] = "sk_does_not_exist_0001"
        self.assertRefused(self.check_pack(doc), "does not resolve")

    def test_hold_lane_id_is_refused(self):
        doc = self.mutate(self.pa)
        doc["decisions"][0]["compiled_from"].append({
            "ref": "sk_abcd_0001", "kind": "source_knowledge",
            "source_dir": "google-abcd-video-ads", "concept_label": "x", "marker": None})
        self.assertRefused(self.check_pack(doc), "sk_abcd_")

    def test_wrong_source_dir_is_refused(self):
        doc = self.mutate(self.pa)
        doc["decisions"][0]["compiled_from"][0]["source_dir"] = "murch-blink-p1-25"
        self.assertRefused(self.check_pack(doc), "corpus owner is")

    # ── check 2: guard closure and the gos_0012 regression ──────────────
    def test_dropping_a_contradiction_partner_breaks_closure(self):
        doc = self.mutate(self.ca)
        for d in doc["decisions"]:
            d["compiled_from"] = [r for r in d["compiled_from"]
                                  if r["ref"] != "sk_murch_c003_0033"]
        # also strip the conflicts entry that names it, so nothing covers the partner
        doc["conflicts"] = [c for c in doc["conflicts"]
                            if "sk_murch_c003_0033" not in (c.get("between") or [])]
        self.assertRefused(self.check_pack(doc), "closure hole")

    def test_gos_0012_regression_is_enforced(self):
        doc = self.mutate(self.ca)
        for d in doc["decisions"]:
            d["compiled_from"] = [r for r in d["compiled_from"]
                                  if r["ref"] != "sk_gos_c003_0013"]
        self.assertRefused(self.check_pack(doc), "regression")

    def test_conflict_without_resolution_rule_is_refused(self):
        doc = self.mutate(self.pa)
        doc["conflicts"][0]["resolution_rule"] = ""
        self.assertRefused(self.check_pack(doc), "no resolution_rule")

    def test_waiver_without_reason_is_refused(self):
        doc = self.mutate(self.pa)
        doc["closure_waivers"][0]["reason"] = ""
        self.assertRefused(self.check_pack(doc), "no reason stated")

    # ── check 3: markers recompute from the REP-04 assigner ─────────────
    def test_tampered_marker_is_refused(self):
        doc = self.mutate(self.pa)
        doc["decisions"][0]["confidence_marker"] = "[MEASURED|MULTI-ORIGIN(9)]"
        self.assertRefused(self.check_pack(doc), "recomputed")

    def test_pa_d9_marker_tokens_are_enforced(self):
        doc = self.mutate(self.pa)
        for d in doc["decisions"]:
            if d["decision_id"] == "PA-D9":
                d["confidence_marker"] = d["confidence_marker"].replace("DATED|", "")
        errors = self.check_pack(doc)
        self.assertRefused(errors, "lacks DATED")
        # the tamper also breaks recomputation, which must be reported too
        self.assertRefused(errors, "recomputed")

    def test_committed_pa_d9_marker_carries_the_three_tokens(self):
        d9 = next(d for d in self.pa["decisions"] if d["decision_id"] == "PA-D9")
        for needle in ("ASSERTED", "DATED", "SINGLE-ORIGIN"):
            self.assertIn(needle, d9["confidence_marker"])

    # ── check 4: budgets ────────────────────────────────────────────────
    def test_oversize_terse_rendering_is_refused(self):
        doc = self.mutate(self.pa)
        doc["terse_injection_text"] += "x" * 10001
        errors = self.check_pack(doc)
        self.assertRefused(errors, "terse rendering")

    def test_tampered_terse_count_is_refused(self):
        doc = self.mutate(self.pa)
        doc["counts"]["terse_tokens"] -= 1
        self.assertRefused(self.check_pack(doc),
                           "size reported must equal size delivered")

    def test_trigger_budget_overflow_is_refused(self):
        doc = self.mutate(yaml.safe_load(TRIGGERS.read_text()))
        doc["token_budgets"]["colour_and_visual_register"] = 40000
        self.assertRefused(self.check_triggers(doc), "largest legal combination")

    # ── check 5: corpus digest stamp ────────────────────────────────────
    def test_stale_corpus_digest_is_refused(self):
        doc = self.mutate(self.pa)
        doc["corpus_digest"] = "0" * 64
        self.assertRefused(self.check_pack(doc), "stale stamp")

    # ── check 6: trigger-table totality ─────────────────────────────────
    def test_missing_cell_is_refused(self):
        doc = self.mutate(yaml.safe_load(TRIGGERS.read_text()))
        doc["cells"] = doc["cells"][:-1]
        self.assertRefused(self.check_triggers(doc), "missing cell")

    def test_audio_cell_without_notice_is_refused(self):
        doc = self.mutate(yaml.safe_load(TRIGGERS.read_text()))
        for c in doc["cells"]:
            if c["modality"] == "audio" and c["requested_operation"] == "generate":
                del c["coverage_gap_notice"]
        self.assertRefused(self.check_triggers(doc), "coverage-gap notice")

    def test_pack_id_outside_closed_set_is_refused(self):
        doc = self.mutate(yaml.safe_load(TRIGGERS.read_text()))
        doc["universal_packs"].append("pack_that_does_not_exist")
        self.assertRefused(self.check_triggers(doc), "closed set")

    # ── check 8: verbatim limit lines ───────────────────────────────────
    def test_removing_devanagari_line_is_refused(self):
        for committed in (self.pa, self.ca):
            doc = self.mutate(committed)
            doc["pack_limits"] = [l for l in doc["pack_limits"]
                                  if "Devanagari" not in l]
            self.assertRefused(self.check_pack(doc), "Devanagari")

    def test_removing_lsm_caveat_is_refused(self):
        doc = self.mutate(self.pa)
        doc["pack_limits"] = [l for l in doc["pack_limits"] if "GAP-16" not in l]
        self.assertRefused(self.check_pack(doc), "LSM later-chapters")

    def test_paraphrasing_devanagari_line_is_refused(self):
        doc = self.mutate(self.pa)
        doc["pack_limits"] = [
            l.replace("never generate Devanagari glyphs", "avoid Devanagari glyphs")
            for l in doc["pack_limits"]]
        self.assertRefused(self.check_pack(doc), "Devanagari")

    # ── check 9: deliverable-wide HOLD scan ─────────────────────────────
    def test_committed_deliverables_carry_no_hold_ids(self):
        self.assertEqual(vcp.validate_no_hold_ids(self.env), [])

    # ── decision-shape sanity over the committed packs ──────────────────
    def test_every_decision_lists_ids_marker_question_default_check(self):
        for pack in (self.pa, self.ca):
            for d in pack["decisions"]:
                self.assertTrue(d["compiled_from"], d["decision_id"])
                self.assertTrue(d["confidence_marker"].startswith("["), d["decision_id"])
                for field in ("question", "default", "check"):
                    self.assertTrue(str(d[field]).strip(), d["decision_id"])

    def test_pilot_union_is_21_decisions_101_sk_objects(self):
        # 97 at first compile; +4 after the adversary-mandated CA-D8 Rule-of-Six
        # weight citations (sk_murch_c003_0021/0022/0024/0025).
        cited = set()
        n = 0
        for pack in (self.pa, self.ca):
            n += len(pack["decisions"])
            for d in pack["decisions"]:
                cited.update(r["ref"] for r in d["compiled_from"]
                             if r["kind"] == "source_knowledge")
        self.assertEqual(n, 21)
        self.assertEqual(len(cited), 101)


if __name__ == "__main__":
    unittest.main()
