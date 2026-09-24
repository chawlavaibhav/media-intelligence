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
