"""The library's statistics: exact binomial intervals and the significance test that gates failure notes."""
import unittest

from product.library import stats


class ExactBinomial(unittest.TestCase):
    def test_known_clopper_pearson_values(self):
        lo, hi = stats.interval(15, 16)                       # EQ-001: 15 of 16 hands-on-zip takes rejected
        self.assertAlmostEqual(lo, 0.698, places=2)
        self.assertAlmostEqual(hi, 0.998, places=2)
        lo, hi = stats.interval(0, 10)
        self.assertEqual(lo, 0.0)
        self.assertAlmostEqual(hi, 0.308, places=2)

    def test_significance_depends_on_the_sample_size(self):
        self.assertFalse(stats.recurs_significantly(3, 23))   # 3 of 23 jobs: not distinguishable from a one-off
        self.assertTrue(stats.recurs_significantly(4, 23))
        self.assertFalse(stats.recurs_significantly(1, 1))    # one job on record says nothing
        self.assertTrue(stats.recurs_significantly(3, 3))     # every job so far
        self.assertFalse(stats.recurs_significantly(1, 200))  # a one-off stays a one-off, however many jobs
        self.assertTrue(stats.recurs_significantly(4, 200))   # 4 of 200 is still clearly more than a one-off (1/200)

    def test_describe_reports_rate_and_interval(self):
        self.assertTrue(stats.describe(5, 23).startswith("seen on 5 of 23 jobs (22%, 95% CI"))


if __name__ == "__main__":
    unittest.main()


class EquipmentVerdictsFollowTheEvidence(unittest.TestCase):
    def setUp(self):
        import os, tempfile
        from product import library
        from product.store import Store
        self.st = Store(os.path.join(tempfile.mkdtemp(), "t.db"))
        self.eq = library.EquipmentSheet(self.st)

    def row(self, rid):
        return next(r for r in self.eq.rows() if r["id"] == rid)

    def test_seed_verdicts_are_computed_from_counts(self):
        self.assertEqual(self.row("EQ-001")["verdict"], "cannot")            # 15 of 16 failed: significant
        self.assertEqual(self.row("EQ-005")["declared_verdict"], "reliable")
        self.assertEqual(self.row("EQ-005")["verdict"], "risky")             # 1 accepted poster is not evidence
        self.assertEqual(self.row("EQ-010")["verdict"], "cannot")            # policy stays policy
        self.assertEqual(self.row("EQ-008")["verdict"], "reliable")          # deterministic code
        self.assertIn("0 of 1 attempts failed", self.row("EQ-005")["evidence"])

    def test_a_lesson_with_counts_adds_evidence_and_the_statistics_decide(self):
        self.eq.apply({"id": "EQ-005", "action_class": "product_still_from_clean_photo", "verdict": "reliable",
                       "successes": 19, "failures": 0}, by="lesson", source_lesson="L-1")
        r = self.row("EQ-005")
        self.assertEqual((r["successes"], r["failures"]), (20, 0))
        self.assertEqual(r["verdict"], "reliable")                           # 0 of 20 failed: upper bound 14% < 25%

    def test_a_lesson_without_counts_is_kept_labelled_and_never_stronger_than_risky(self):
        """Architect review 2026-09-25: one job's word is not evidence — a count-less 'cannot' is shown as risky."""
        self.eq.apply({"id": "EQ-003", "action_class": "lift_closed_product", "verdict": "cannot"}, by="lesson", source_lesson="L-2")
        r = self.row("EQ-003")
        self.assertEqual(r["verdict"], "risky")
        self.assertEqual(r["declared_verdict"], "cannot")
        self.assertIn("without counts", r["evidence"])
