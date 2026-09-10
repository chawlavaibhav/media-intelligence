"""Audit finding B (2026-09-10): the vision-judge report's call count must be the LIVE count or no count at all.

QUALIFICATION-REPORT-2026-09-09.yaml records `calls: 206` against an authorised screen_max_calls of 200 with
`stopped: null`. The live loop counts calls SENT; the offline rebuild recomputed a different number by counting
screened rows - and a row is not a call (an audio row is decided cannot_judge without any call). From the report
alone nobody could tell whether the limit had been breached.

Proven here (no socket, no key, no Gemini call):
    - a live screening run persists its own counters (calls sent, calls refused, which limit stopped it);
    - a rebuild that has those counters reports the LIVE number, never a row count;
    - a rebuild with no counters prints NO call number and says so in words;
    - the report always states the authorised limit and flags plainly when the count is at or above it;
    - the committed September SCREEN-RESULTS files hold 210 rows of which only 190 carry evidence of a call, so 206 was
      a row count, not a call count.
"""
import unittest
from decimal import Decimal
from pathlib import Path

import yaml

from _support import hv2_paths
import qualify_screen as QS

RUNS = hv2_paths.EVAL_ROOT / "experiments" / "EVAL-040" / "runs"
AUTH_200 = {"present": True, "screen_cap_usd": Decimal("5.0"), "screen_max_calls": 200}
AUTH_NONE = {"present": False}


def counters(sent, refused=0, stopped=None, stopped_by=None, auth=AUTH_200, this_file=None):
    return QS.call_counters(sent, refused, stopped, stopped_by, auth, this_file=this_file)


class CallCountersTest(unittest.TestCase):
    def test_a_live_run_records_what_it_sent(self):
        c = counters(190, refused=4, stopped="stopped: ...", stopped_by="screen_max_calls", this_file=12)
        self.assertEqual(c["schema"], QS.COUNTERS_SCHEMA)
        self.assertEqual(c["source"], QS.BASIS_LIVE)
        self.assertEqual(c["screening_calls_sent"], 190)
        self.assertEqual(c["screening_calls_refused"], 4)
        self.assertEqual(c["calls_sent_for_trials_in_this_file"], 12)
        self.assertEqual(c["screen_max_calls"], 200)
        self.assertEqual(c["stopped_by"], "screen_max_calls")

    def test_counters_are_read_back_off_the_screen_results_documents(self):
        docs = [{QS.COUNTERS_KEY: counters(190, refused=2)}, {QS.COUNTERS_KEY: counters(190, refused=4)}]
        live = QS.live_call_counters(docs)
        self.assertEqual(live["calls"], 190)
        self.assertEqual(live["refused"], 4)
        self.assertEqual(live["basis"], QS.BASIS_LIVE)

    def test_no_counter_means_no_number(self):
        live = QS.live_call_counters([{"run_id": "img-r1", "trials": [{"screen_overall": "accept"}] * 76}])
        self.assertIsNone(live["calls"], "a rebuild must not invent a count from the rows")
        self.assertEqual(live["basis"], QS.BASIS_MISSING)

    def test_counters_that_disagree_are_not_reported_as_fact(self):
        live = QS.live_call_counters([{QS.COUNTERS_KEY: counters(190)}, {QS.COUNTERS_KEY: counters(206)}])
        self.assertIsNone(live["calls"])
        self.assertIn("conflicting", live["basis"])


class CallsSectionTest(unittest.TestCase):
    def test_it_states_the_authorised_limit(self):
        sec = QS.calls_section(190, QS.BASIS_LIVE, AUTH_200, None, None)
        self.assertEqual(sec["calls"], 190)
        self.assertEqual(sec["authorised_screen_max_calls"], 200)
        self.assertFalse(sec["calls_at_or_above_authorised_limit"])
        self.assertIn("within the authorised", sec["calls_note"])

    def test_it_flags_a_count_at_or_above_the_limit(self):
        for n in (200, 206):
            sec = QS.calls_section(n, QS.BASIS_LIVE, AUTH_200, None, None)
            self.assertTrue(sec["calls_at_or_above_authorised_limit"], n)
            self.assertIn("ATTENTION", sec["calls_note"])
            self.assertIn("200", sec["calls_note"])
        self.assertIn("no stop was recorded", QS.calls_section(206, QS.BASIS_LIVE, AUTH_200, None, None)["calls_note"],
                      "206 calls against a 200 limit with stopped: null is exactly what the report had to explain")

    def test_an_unknown_count_prints_no_number_and_says_so_in_words(self):
        sec = QS.calls_section(None, QS.BASIS_MISSING, AUTH_200, None, None)
        self.assertIsNone(sec["calls"])
        self.assertIsNone(sec["calls_at_or_above_authorised_limit"])
        self.assertIn("NOT KNOWN", sec["calls_note"])
        self.assertIn("a row is not a call", sec["calls_note"])
        self.assertEqual(sec["calls_basis"], QS.BASIS_MISSING)

    def test_no_authorised_limit_is_said_plainly(self):
        sec = QS.calls_section(12, QS.BASIS_LIVE, AUTH_NONE, None, None)
        self.assertIsNone(sec["authorised_screen_max_calls"])
        self.assertIsNone(sec["calls_at_or_above_authorised_limit"])
        self.assertIn("no screen_max_calls was authorised", sec["calls_note"])


class CommittedScreenResultsTest(unittest.TestCase):
    """Read-only: what the sealed September SCREEN-RESULTS files actually contain."""

    def _docs(self):
        return [yaml.safe_load(p.read_text(encoding="utf-8")) for p in sorted(RUNS.glob("*/SCREEN-RESULTS.yaml"))]

    def test_the_row_count_is_not_the_call_count(self):
        docs = self._docs()
        if not docs:
            self.skipTest("sealed SCREEN-RESULTS files not present")
        rows = [t for d in docs for t in (d.get("trials") or [])]
        old_formula = sum(1 for t in rows if t.get("screen_overall") is not None or t.get("http_status"))
        audio = sum(1 for t in rows if (t.get("artifact") or {}).get("media_kind") == "audio" or t.get("media_kind") == "audio")
        with_evidence_of_a_call = sum(1 for t in rows if t.get("http_status") or (t.get("usage") or {}))
        self.assertEqual(len(rows), 210, "total screened rows across the 14 committed SCREEN-RESULTS files")
        self.assertEqual(old_formula, 206, "the number the offline rebuild printed as `calls`")
        self.assertEqual(audio, 16, "audio rows are planned cannot_judge and never make a call")
        self.assertEqual(old_formula - audio, with_evidence_of_a_call,
                         "206 minus the 16 audio rows is exactly the rows that carry usage or an http status")
        self.assertLessEqual(with_evidence_of_a_call, 200, "the authorised screen_max_calls was never actually crossed")

    def test_the_sealed_files_carry_no_live_counter_so_a_rebuild_must_say_so(self):
        docs = self._docs()
        if not docs:
            self.skipTest("sealed SCREEN-RESULTS files not present")
        self.assertEqual(QS.live_call_counters(docs)["basis"], QS.BASIS_MISSING)


if __name__ == "__main__":
    unittest.main()
