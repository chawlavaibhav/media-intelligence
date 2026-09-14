"""Intake refuses, by name, before anything else happens."""
from __future__ import annotations

import copy
import unittest

from runtime.errors import Refusal
from runtime.policy import PolicyProfiles
from runtime.tests import support


class ConsentTest(unittest.TestCase):
    def test_person_reference_without_consent_is_refused(self):
        raw = copy.deepcopy(support.brief("lipstick-packshot"))
        raw["reference_assets"].append(
            {
                "asset_id": "ast_founder_portrait",
                "role": "person",
                "sha256": "aa" * 32,
                "content_type": "image/jpeg",
                "provenance": "customer_supplied",
            }
        )
        with self.assertRaises(Refusal) as caught:
            support.intake().submit(raw)
        self.assertEqual(caught.exception.code, Refusal.CONSENT_MISSING)
        self.assertEqual(caught.exception.context["asset_id"], "ast_founder_portrait")

    def test_person_reference_with_consent_is_accepted(self):
        raw = copy.deepcopy(support.brief("lipstick-packshot"))
        raw["reference_assets"].append(
            {
                "asset_id": "ast_founder_portrait",
                "role": "person",
                "sha256": "aa" * 32,
                "content_type": "image/jpeg",
                "provenance": "customer_supplied",
                "consent_ref": "CONSENT-2026-09-01-RANGEEN-04",
            }
        )
        job = support.intake().submit(raw).job
        self.assertEqual(len(job["reference_assets"]), 3)

    def test_consent_is_checked_before_the_profile(self):
        """Order matters: a consent failure must not wait behind a policy lookup."""
        raw = copy.deepcopy(support.brief("lipstick-packshot"))
        raw["policy_profile"] = "no_such_profile"
        raw["reference_assets"].append(
            {
                "asset_id": "ast_face",
                "role": "person",
                "sha256": "bb" * 32,
                "content_type": "image/jpeg",
                "provenance": "customer_supplied",
            }
        )
        with self.assertRaises(Refusal) as caught:
            support.intake().submit(raw)
        self.assertEqual(caught.exception.code, Refusal.CONSENT_MISSING)


class PolicyTest(unittest.TestCase):
    def test_profile_missing_a_limit_is_refused(self):
        raw = copy.deepcopy(support.brief("mustard-oil-tin"))
        raw["policy_profile"] = "missing_a_limit"
        with self.assertRaises(Refusal) as caught:
            support.intake(support.test_profiles()).submit(raw)
        self.assertEqual(caught.exception.code, Refusal.POLICY_LIMIT_MISSING)
        self.assertEqual(caught.exception.context["limit"], "repair_allowance")

    def test_unknown_profile_is_refused(self):
        raw = copy.deepcopy(support.brief("mustard-oil-tin"))
        raw["policy_profile"] = "no_such_profile"
        with self.assertRaises(Refusal) as caught:
            support.intake().submit(raw)
        self.assertEqual(caught.exception.code, Refusal.POLICY_PROFILE_UNKNOWN)

    def test_kind_not_in_profile_is_refused(self):
        raw = copy.deepcopy(support.brief("mustard-oil-tin"))
        raw["policy_profile"] = "narrow_kinds"
        with self.assertRaises(Refusal) as caught:
            support.intake(support.test_profiles()).submit(raw)
        self.assertEqual(caught.exception.code, Refusal.KIND_NOT_IN_PROFILE)
        self.assertEqual(caught.exception.context["kind"], "static_ad")

    def test_widening_the_profile_is_a_row_edit(self):
        """The same job the narrow profile refuses is accepted by a wider row. No code changed."""
        raw = copy.deepcopy(support.brief("mustard-oil-tin"))
        raw["policy_profile"] = "wide_and_generous"
        job = support.intake(support.test_profiles()).submit(raw).job
        self.assertEqual(job["deliverable_request"]["kind"], "static_ad")

    def test_omitted_job_field_is_filled_from_the_profile_not_from_code(self):
        raw = copy.deepcopy(support.brief("lipstick-packshot"))  # carries no cost_ceiling_usd
        self.assertNotIn("cost_ceiling_usd", raw)
        job = support.intake().submit(raw).job
        profile = PolicyProfiles().profile("dry")
        self.assertEqual(float(job["cost_ceiling_usd"]), float(profile.limit("default_job_cost_ceiling_usd")))
        self.assertEqual(job["retention"]["delete_after_days"], profile.limit("retention_days_default"))


class SchemaTest(unittest.TestCase):
    def test_undeclared_field_is_refused(self):
        raw = copy.deepcopy(support.brief("mustard-oil-tin"))
        raw["rush_it"] = True
        with self.assertRaises(Refusal) as caught:
            support.intake().submit(raw)
        self.assertEqual(caught.exception.code, Refusal.SCHEMA_VIOLATION)

    def test_missing_required_field_is_refused(self):
        raw = copy.deepcopy(support.brief("mustard-oil-tin"))
        del raw["customer_ref"]
        with self.assertRaises(Refusal) as caught:
            support.intake().submit(raw)
        self.assertEqual(caught.exception.code, Refusal.SCHEMA_VIOLATION)

    def test_kind_outside_the_registry_is_refused(self):
        raw = copy.deepcopy(support.brief("mustard-oil-tin"))
        raw["policy_profile"] = "wide_and_generous"
        raw["deliverable_request"]["kind"] = "holographic_shop_sign"
        with self.assertRaises(Refusal) as caught:
            support.intake(support.test_profiles()).submit(raw)
        self.assertEqual(caught.exception.code, Refusal.KIND_NOT_IN_REGISTRY)


if __name__ == "__main__":
    unittest.main()
