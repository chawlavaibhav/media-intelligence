"""The `dry` profile is the DRY TWIN of alpha_human_release, and the data says so (lane F, 14 Sep 2026).

What is being protected: a dry run is only evidence about the alpha if it takes the SAME decisions the
alpha would take. So `dry` must carry alpha_human_release's limits verbatim and differ only in the
fields that name the profile itself and in dispatch_mode. These tests read the two rows back and
assert they agree on every other key, so an edit to one row without the other fails here rather than
producing a dry run that quietly routes differently from the paid run it stands in for.

The exclusion set is spelled out below and nowhere else. Anything not in it must be identical.
"""
from __future__ import annotations

import unittest
from pathlib import Path

import _bootstrap as B
from runtime import paths
from runtime.policy import PolicyProfiles
from runtime.util import load_yaml

PROFILES_PATH = Path(paths.POLICY_PROFILES)
REQUIRED_LIMITS_PATH = Path(paths.REQUIRED_LIMITS)

# The ONLY keys on which the twin may differ from alpha_human_release. Everything else is a limit and
# must be byte-for-byte the same value. human_approval_basis and public_release_gate are deliberately
# NOT in this set: the twin carries the same C-8 basis and the same twelve-condition gate as data.
TWIN_MAY_DIFFER = frozenset({"profile", "purpose", "status", "adoption_basis", "dispatch_mode",
                             "spend_authority", "note"})


def _rows() -> dict:
    return {row["profile"]: row for row in (load_yaml(PROFILES_PATH) or {}).get("profiles", [])}


class DryIsTheTwinOfAlpha(unittest.TestCase):
    def test_every_key_outside_the_exclusion_set_is_identical(self):
        rows = _rows()
        alpha, dry = rows["alpha_human_release"], rows["dry"]
        self.assertEqual(set(alpha) - TWIN_MAY_DIFFER, set(dry) - TWIN_MAY_DIFFER,
                         "the twin and the alpha row do not carry the same set of limit keys")
        for key in sorted(set(alpha) - TWIN_MAY_DIFFER):
            self.assertEqual(alpha[key], dry[key], f"dry.{key} has drifted from alpha_human_release.{key}")

    def test_the_twin_differs_only_where_it_must(self):
        rows = _rows()
        alpha, dry = rows["alpha_human_release"], rows["dry"]
        differing = {k for k in set(alpha) | set(dry) if alpha.get(k) != dry.get(k)}
        self.assertLessEqual(differing, TWIN_MAY_DIFFER, f"unexpected differences: {sorted(differing - TWIN_MAY_DIFFER)}")
        # and the fields that must differ, do
        self.assertEqual(alpha["dispatch_mode"], "live")
        self.assertEqual(dry["dispatch_mode"], "dry")
        self.assertIs(dry["adopted"], True)
        self.assertEqual(dry["status"], "active")
        self.assertIn("dry twin of alpha_human_release", dry["adoption_basis"])

    def test_the_twin_carries_the_alpha_numbers_not_the_old_permissive_ones(self):
        dry = _rows()["dry"]
        self.assertEqual(dry["max_provider_draws_per_deliverable"], 2)
        self.assertEqual(dry["repair_allowance"], 1)
        self.assertEqual(dry["auto_routable_evidence_status"], ["clean_observed"])
        self.assertEqual(dry["on_non_auto_routable"], "manual_route_required")
        self.assertEqual(dry["acceptance_authority"], "human")
        self.assertIs(dry["fallback_required"], True)
        self.assertEqual(str(dry["default_job_cost_ceiling_usd"]), "5.0")
        self.assertEqual(dry["exact_text_strategies_allowed"], ["code_set_on_textless_plate"])

    def test_the_twin_has_no_spend_authority_and_says_why(self):
        sa = _rows()["dry"]["spend_authority"]
        self.assertEqual(sa["status"], "none")
        self.assertIsNone(sa["record"])
        self.assertIn("nothing is sent", sa["note"])
        self.assertIn("reservations are 0", sa["note"])
        self.assertFalse(B.profile("dry").may_spend()[0])

    def test_both_profile_readers_read_the_same_dry_row(self):
        route_side = B.profile("dry")
        intake_side = PolicyProfiles().profile("dry")
        self.assertEqual(route_side.max_provider_draws, intake_side.limit("max_provider_draws_per_deliverable"))
        self.assertEqual(route_side.limit("dispatch_mode"), intake_side.limit("dispatch_mode"))
        self.assertEqual(route_side.limit("dispatch_mode"), "dry")


class DryPermissiveKeepsTheOldRow(unittest.TestCase):
    def test_the_old_permissive_row_survives_under_its_new_name(self):
        row = _rows()["dry_permissive"]
        self.assertEqual(row["max_provider_draws_per_deliverable"], 0)
        self.assertEqual(row["repair_allowance"], 0)
        self.assertEqual(row["deliverable_kinds_allowed"], ["__all__"])
        self.assertEqual(row["acceptance_authority"], "none")
        self.assertEqual(row["on_non_auto_routable"], "annotate_and_continue")
        self.assertEqual(row["dispatch_mode"], "dry")
        self.assertIn("never a battery profile", row["purpose"])
        self.assertEqual(row["spend_authority"]["status"], "none")


class DispatchModeIsARequiredLimit(unittest.TestCase):
    def test_every_profile_row_names_a_dispatch_mode_from_the_two_word_vocabulary(self):
        for name, row in _rows().items():
            self.assertIn("dispatch_mode", row, name)
            self.assertIn(row["dispatch_mode"], ("dry", "live"), name)

    def test_only_the_dry_rows_are_dry(self):
        rows = _rows()
        self.assertEqual(sorted(k for k, r in rows.items() if r["dispatch_mode"] == "dry"), ["dry", "dry_permissive"])
        self.assertEqual(sorted(k for k, r in rows.items() if r["dispatch_mode"] == "live"),
                         ["alpha_human_release", "alpha_wider_example"])

    def test_required_limits_lists_dispatch_mode_for_intake_and_the_bridge(self):
        needs = load_yaml(REQUIRED_LIMITS_PATH) or {}
        self.assertIn("dispatch_mode", needs["required_at_intake"])
        self.assertIn("dispatch_mode", needs["read_by_execution_bridge"])
        self.assertEqual(needs["read_by_execution_bridge"][0], "spend_authority")
        self.assertEqual(needs["read_by_execution_bridge"][1], "dispatch_mode")

    def test_intake_checks_dispatch_mode_before_anything_runs(self):
        profiles = PolicyProfiles()
        for name in profiles.names():
            profiles.checked_profile(name)     # raises POLICY_LIMIT_MISSING on any gap, dispatch_mode included


if __name__ == "__main__":
    unittest.main()
