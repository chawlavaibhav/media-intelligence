"""job_id idempotency is real, not decorative.

PRODUCTION-JOB-v0: "Submitting the same job_id twice must return the existing job and must never
dispatch a second provider call. This is the single defence against a retry storm costing money
twice." So the second submission must return the first job AND DO NOTHING ELSE — which is what
the exploding collaborators below prove.
"""
from __future__ import annotations

import copy
import unittest

from runtime.errors import Refusal
from runtime.intake import Intake
from runtime.tests import support


class Explodes:
    """Any attribute access is a test failure."""

    def __init__(self, what: str):
        self.what = what

    def __getattr__(self, name):
        raise AssertionError(f"a repeat submission touched {self.what}.{name}")


class IdempotencyTest(unittest.TestCase):
    def test_second_submission_returns_the_first_job(self):
        store = support.fresh_store()
        raw = copy.deepcopy(support.brief("mustard-oil-tin"))

        first = Intake(store=store).submit(raw)
        self.assertTrue(first.created)

        second = Intake(store=store).submit(raw)
        self.assertFalse(second.created)
        self.assertEqual(first.job, second.job)
        self.assertEqual(first.job_sha256, second.job_sha256)

    def test_second_submission_does_nothing_else(self):
        store = support.fresh_store()
        raw = copy.deepcopy(support.brief("mustard-oil-tin"))
        Intake(store=store).submit(raw)

        blind = Intake(store=store, profiles=Explodes("profiles"), kinds=Explodes("kinds"),
                       contract=Explodes("contract"))
        result = blind.submit(raw)
        self.assertFalse(result.created)
        self.assertEqual(result.job["job_id"], raw["job_id"])

    def test_a_changed_body_under_the_same_job_id_returns_the_original(self):
        """The job object is immutable after creation. A correction is a new job."""
        store = support.fresh_store()
        raw = copy.deepcopy(support.brief("mustard-oil-tin"))
        original = Intake(store=store).submit(raw).job

        tampered = copy.deepcopy(raw)
        tampered["exact_text_strings"][1]["value"] = "₹186 प्रति लीटर"
        returned = Intake(store=store).submit(tampered)

        self.assertFalse(returned.created)
        self.assertEqual(returned.job["exact_text_strings"][1]["value"], "₹185 प्रति लीटर")
        self.assertEqual(returned.job, original)

    def test_a_job_record_is_never_overwritten(self):
        store = support.fresh_store()
        job = Intake(store=store).submit(copy.deepcopy(support.brief("mustard-oil-tin"))).job
        with self.assertRaises(Refusal) as caught:
            store.put(job)
        self.assertEqual(caught.exception.code, Refusal.JOB_IMMUTABLE)

    def test_the_job_store_is_nowhere_near_the_lab(self):
        store = support.fresh_store()
        Intake(store=store).submit(copy.deepcopy(support.brief("mustard-oil-tin")))
        self.assertNotIn("/eval/", str(store.root))


if __name__ == "__main__":
    unittest.main()
