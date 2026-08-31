"""REP-04 validator: deterministic confidence markers + technology-dating annex.

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

Everything here recomputes from committed yaml and fails on any drift: the marker
rule is re-run over canon/knowledge/current/, the annex join is re-walked over
canon/audit/records/, and the committed outputs must equal the recomputation
byte-for-byte. Run: python3 -m unittest tests.test_assign_markers
"""
import unittest
from collections import Counter
from pathlib import Path

import yaml

from canon.compilation import assign_markers as am

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE = REPO_ROOT / "tests/fixtures/rep04-mismarked-controlled-comparison.yaml"

EXPECTED_BASE = {"MEASURED": 59, "REASONED": 337, "ASSERTED": 281}
EXPECTED_FLAGS = {
    "CONTESTED": 85,
    "QUALIFIED": 167,
    "DATED": 110,
    "CULTURE-BOUND": 84,
    "FIGURE-UNVERIFIED": 122,
}
EXPECTED_SUFFIXES = {"-our_reading": 21, "-hedged": 634}

# The brief's explicit 32-id technology-contingency list (30 technology_contingent
# + ogilvy's 2 uncertain). Must be a subset of the annex's technology_dating rows.
BRIEF_32_IDS = {
    "sk_alt_c003_0003", "sk_alt_c003_0004", "sk_alt_c003_0005", "sk_alt_c003_0006",
    "sk_alt_c003_0018",
    "sk_rbwl_0100", "sk_rbwl_0150", "sk_rbwl_0160",
    "sk_eic_0016", "sk_eic_0017", "sk_eic_0018", "sk_eic_0021", "sk_eic_0022",
    "sk_eic_0023", "sk_eic_0026",
    "sk_dpci_0110", "sk_dpci_0170", "sk_dpci_0180",
    "sk_hop_sa_0001", "sk_hop_sa_0006",
    "sk_jgb_0020", "sk_jgb_0050", "sk_jgb_0150",
    "sk_ppm_0010", "sk_ppm_0011", "sk_ppm_0031",
    "sk_nnn_0030", "sk_nnn_0040", "sk_nnn_0042", "sk_nnn_0051",
    "sk_ogl_c003_0013", "sk_ogl_c003_0019",
}

# The brief's medium_transfer_untested seed ids. Must be a subset of the annex rows.
SEED_IDS = {
    "sk_gote_c003_0009", "sk_gote_c003_0016", "sk_gote_c003_0028", "sk_gote_c003_0029",
    "sk_gote_c003_0053", "sk_murch_c003_0008", "sk_murch_c003_0022",
    "sk_ms_c003_0010", "sk_ms_c003_0013", "sk_ms_c003_0017", "sk_ms_c003_0019",
    "sk_hop_sa_0013", "sk_hop_sa_0031", "sk_hop_sa_0032", "sk_hop_sa_0033",
    "sk_hop_sa_0035", "sk_hea_mts_0011", "sk_hea_mts_0023",
}


class MarkerRuleTest(unittest.TestCase):
    """The marker rule recomputed from committed yaml — fails on any drift."""

    @classmethod
    def setUpClass(cls):
        cls.objs, cls.src_of = am.load_corpus()
        cls.markers = am.compute_markers(cls.objs)
        cls.scheme = yaml.safe_load(am.SCHEME_PATH.read_text())
        cls.committed_map = yaml.safe_load(am.MARKER_MAP_PATH.read_text())
        cls.annex = yaml.safe_load(am.ANNEX_PATH.read_text())

    def test_corpus_is_677_objects(self):
        self.assertEqual(len(self.objs), 677)

    def test_every_object_has_exactly_one_base_grade(self):
        entries = self.committed_map["markers"]
        self.assertEqual(sorted(entries), sorted(self.objs))
        for sk, e in entries.items():
            self.assertIn(e["base"], EXPECTED_BASE, sk)
            # base is a single grade, not a list — exactly one per object by shape
            self.assertIsInstance(e["base"], str, sk)

    def test_base_counts_recompute_to_expected(self):
        got = Counter(m["base"] for m in self.markers.values())
        self.assertEqual(dict(got), EXPECTED_BASE)

    def test_flag_counts_recompute_to_expected(self):
        got = Counter(f for m in self.markers.values() for f in m["flags"])
        self.assertEqual({k: got.get(k, 0) for k in EXPECTED_FLAGS}, EXPECTED_FLAGS)
        self.assertEqual(sum(got.values()), sum(EXPECTED_FLAGS.values()))

    def test_suffix_counts_recompute_to_expected(self):
        got = Counter(s for m in self.markers.values() for s in m["suffixes"])
        self.assertEqual(dict(got), EXPECTED_SUFFIXES)

    def test_scheme_expected_counts_match_recomputation(self):
        table = self.scheme["decision_table"]
        base = Counter(m["base"] for m in self.markers.values())
        for rule in table["base_grade"]["rules"]:
            self.assertEqual(base[rule["grade"]], rule["expected_count"], rule["grade"])
        flags = Counter(f for m in self.markers.values() for f in m["flags"])
        for rule in table["flags"]["rules"]:
            self.assertEqual(flags[rule["flag"]], rule["expected_count"], rule["flag"])
        suff = Counter(s for m in self.markers.values() for s in m["suffixes"])
        for rule in table["suffixes"]["rules"]:
            self.assertEqual(suff[rule["suffix"]], rule["expected_count"], rule["suffix"])

    def test_committed_marker_map_matches_rule_exactly(self):
        errors = am.check_entries(self.objs, self.committed_map["markers"])
        self.assertEqual(errors, [])

    def test_committed_distribution_block_matches(self):
        dist = self.committed_map["distribution"]
        self.assertEqual(dist["base"], EXPECTED_BASE)
        self.assertEqual(dist["flags"], EXPECTED_FLAGS)
        self.assertEqual(dist["suffixes"], EXPECTED_SUFFIXES)

    def test_no_hold_or_qa_material_in_marker_map(self):
        """Every marked id resolves in canon/knowledge/current/ — HOLD (canon/candidates/)
        and Q&A banks never appear."""
        for sk in self.committed_map["markers"]:
            self.assertIn(sk, self.objs, f"{sk} does not resolve in canon/knowledge/current")
            self.assertFalse(sk.startswith("sk_abcd"), sk)


class DeterminismTest(unittest.TestCase):
    def test_generation_is_byte_identical_and_matches_committed_files(self):
        first = am.generate()
        second = am.generate()
        for path in (am.MARKER_MAP_PATH, am.ANNEX_PATH):
            self.assertEqual(first[path], second[path], f"{path} not deterministic")
            self.assertEqual(
                path.read_text(), first[path],
                f"{path} committed bytes differ from recomputation (drift)",
            )


class RenderingTest(unittest.TestCase):
    def test_example_rendering(self):
        self.assertEqual(
            am.render_marker("REASONED", ["CONTESTED"], [], origin_count=2),
            "[REASONED|CONTESTED|MULTI-ORIGIN(2)]",
        )

    def test_single_origin_and_suffix_rendering(self):
        self.assertEqual(
            am.render_marker("ASSERTED", ["DATED"], ["-hedged"], origin_count=1),
            "[ASSERTED-hedged|DATED|SINGLE-ORIGIN]",
        )

    def test_origin_absent_on_claim_level_render(self):
        self.assertEqual(am.render_marker("MEASURED", ["QUALIFIED"], []), "[MEASURED|QUALIFIED]")

    def test_flag_order_is_fixed(self):
        self.assertEqual(
            am.render_marker("REASONED", ["FIGURE-UNVERIFIED", "CONTESTED"], []),
            "[REASONED|CONTESTED|FIGURE-UNVERIFIED]",
        )

    def test_legend_within_120_tokens(self):
        scheme = yaml.safe_load(am.SCHEME_PATH.read_text())
        legend = scheme["legend"]
        self.assertLessEqual(len(legend.split()), 120)


class NegativeFixtureTest(unittest.TestCase):
    def test_controlled_comparison_mismarked_asserted_is_refused(self):
        fx = yaml.safe_load(FIXTURE.read_text())
        errors = am.check_entries(fx["objects"], fx["claimed_markers"])
        self.assertTrue(errors, "expected the mis-marked fixture to be refused")
        joined = " | ".join(errors)
        self.assertIn("sk_fixture_neg_0001", joined)
        self.assertIn("MEASURED", joined)


class DatingAnnexTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.objs, cls.src_of = am.load_corpus()
        cls.annex = yaml.safe_load(am.ANNEX_PATH.read_text())
        # Re-walk canon/audit/records/ independently of the generator's join.
        cls.record_classes = {}  # record_rel -> {class -> set(sk_refs)}
        for f in sorted((REPO_ROOT / "canon/audit/records").glob("*.audit.yaml")):
            d = yaml.safe_load(f.read_text())
            tc = d.get("technology_contingency") or {}
            if not tc.get("applicable"):
                continue
            rel = str(f.relative_to(REPO_ROOT))
            by_class = {}
            for c in tc.get("classes") or []:
                by_class.setdefault(c["class"], set()).update(c.get("sk_refs") or [])
            cls.record_classes[rel] = by_class

    def test_nine_records_applicable(self):
        self.assertEqual(len(self.record_classes), 9)
        self.assertEqual(
            self.annex["technology_dating"]["records_applicable_true"],
            sorted(self.record_classes),
        )

    def test_every_tech_row_appears_in_exactly_the_audit_record_claimed(self):
        rows = self.annex["technology_dating"]["rows"]
        for r in rows:
            rec, cls_, sk = r["audit_record"], r["class"], r["sk_id"]
            self.assertIn(rec, self.record_classes, f"{sk}: unknown record {rec}")
            self.assertIn(
                sk, self.record_classes[rec].get(cls_, set()),
                f"{sk} not listed under class {cls_} in {rec}",
            )
            # ... and in NO other applicable record under that class
            for other, by_class in self.record_classes.items():
                if other != rec:
                    self.assertNotIn(
                        sk, by_class.get(cls_, set()),
                        f"{sk} class {cls_} also appears in {other}; row claims {rec}",
                    )
            self.assertEqual(r["source_dir"], self.src_of[sk], sk)

    def test_tech_rows_are_the_complete_join(self):
        want = {
            (sk, cls_, rec)
            for rec, by_class in self.record_classes.items()
            for cls_, refs in by_class.items()
            for sk in refs
        }
        got = {
            (r["sk_id"], r["class"], r["audit_record"])
            for r in self.annex["technology_dating"]["rows"]
        }
        self.assertEqual(got, want)

    def test_brief_32_id_list_is_subset_of_annex(self):
        annex_ids = {r["sk_id"] for r in self.annex["technology_dating"]["rows"]}
        self.assertTrue(BRIEF_32_IDS <= annex_ids, BRIEF_32_IDS - annex_ids)
        # and with the classes the brief assigns
        tc_ids = {
            r["sk_id"] for r in self.annex["technology_dating"]["rows"]
            if r["class"] == "technology_contingent"
        }
        unc_ids = {
            r["sk_id"] for r in self.annex["technology_dating"]["rows"]
            if r["class"] == "uncertain"
        }
        self.assertTrue((BRIEF_32_IDS - {"sk_ogl_c003_0013", "sk_ogl_c003_0019"}) <= tc_ids)
        self.assertTrue({"sk_ogl_c003_0013", "sk_ogl_c003_0019"} <= unc_ids)

    def test_technology_contingent_count_is_30(self):
        rows = self.annex["technology_dating"]["rows"]
        self.assertEqual(sum(1 for r in rows if r["class"] == "technology_contingent"), 30)


class MediumTransferTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.objs, cls.src_of = am.load_corpus()
        cls.annex = yaml.safe_load(am.ANNEX_PATH.read_text())
        cls.rows = cls.annex["medium_transfer_untested"]["rows"]

    def test_seed_ids_are_subset_of_rows(self):
        row_ids = {r["sk_id"] for r in self.rows}
        self.assertTrue(SEED_IDS <= row_ids, SEED_IDS - row_ids)

    def test_every_row_cites_source_dir_and_verbatim_trigger_substring(self):
        for r in self.rows:
            sk = r["sk_id"]
            self.assertIn(sk, self.objs, sk)
            self.assertEqual(r["source_dir"], self.src_of[sk], sk)
            obj = self.objs[sk]
            text = (obj.get("concept_label") or "") + " " + (obj.get("claim") or "")
            self.assertTrue(r["trigger_substring"], sk)
            self.assertIn(
                r["trigger_substring"], text,
                f"{sk}: trigger substring not verbatim in concept_label+claim",
            )

    def test_rows_are_the_complete_deterministic_sweep(self):
        scheme = yaml.safe_load(am.SCHEME_PATH.read_text())
        want = am.medium_transfer_rows(self.objs, self.src_of, scheme["medium_transfer_config"])
        self.assertEqual(self.rows, want)

    def test_rows_confined_to_swept_sources(self):
        cfg = yaml.safe_load(am.SCHEME_PATH.read_text())["medium_transfer_config"]
        allowed = set(cfg["swept_sources_editing"]) | set(cfg["swept_sources_commercial"])
        for r in self.rows:
            self.assertIn(r["source_dir"], allowed, r["sk_id"])


if __name__ == "__main__":
    unittest.main()
