"""The Alpha-1 policy profile as the Controller adopted it on 14 Sep 2026 (C-7, C-8, C-11).

Everything the rulings say is DATA in runtime/contracts/POLICY-PROFILES.yaml. These tests read
the rows back and check that the data says what the rulings say, that every profile carries every
limit the runtime will ask for (so a missing limit refuses at intake, not mid-job), and that
adopting the profile created no spend authority anywhere.

Two things these tests deliberately do NOT prove:
  * that the router or the compiler HONOUR exact_text_strategies_allowed and
    motion_requires_accepted_still — nothing in decision.py / compile.py reads them yet (Wave 2);
  * that a "no numeric literal" check over two modules is a proof that no limit is hard-coded
    anywhere. It is a proof about those two modules only, and about numbers only.
"""
from __future__ import annotations

import ast
import re
import unittest
from decimal import Decimal
from pathlib import Path

import _bootstrap as B
from runtime import paths
from runtime.policy import PolicyProfiles
from runtime.policy.profiles import PolicyProfile as IntakeProfile
from runtime.route.decision import ExecuteRefused
from runtime.route.profile import MissingLimit, load_profile
from runtime.util import load_yaml

ROOT = B.ROOT
PROFILES_PATH = Path(paths.POLICY_PROFILES)
REQUIRED_LIMITS_PATH = Path(paths.REQUIRED_LIMITS)
REPORT_A = ROOT / "coordination" / "audits" / "AUDIT-2026-09-10-REPORT-A.md"

C7_C8_RECORD = "coordination/decisions/CONTROLLER-ALPHA-1-PRODUCT-FAMILY-AND-RELEASE-POLICY-2026-09-14.md"

# The limits the 14-Sep rulings added. Every profile row must carry every one of them.
ALPHA_1_LIMITS = (
    "spend_authority",
    "exact_text_strategies_allowed",
    "motion_requires_accepted_still",
    "acceptance_authority",
    "autonomous_external_delivery",
    "human_approval_required_before_external_delivery",
)


def _doc() -> dict:
    return load_yaml(PROFILES_PATH) or {}


def _rows() -> dict:
    return {row["profile"]: row for row in _doc().get("profiles", [])}


def _alpha() -> dict:
    return _rows()["alpha_human_release"]


def _needs() -> dict:
    return load_yaml(REQUIRED_LIMITS_PATH) or {}


class AlphaProfileIsAdopted(unittest.TestCase):
    def test_the_alpha_profile_is_adopted_by_the_controller(self):
        row = _alpha()
        self.assertIs(row["adopted"], True)
        self.assertEqual(row["status"], "adopted_by_controller")
        self.assertIn(C7_C8_RECORD, row["adoption_basis"])
        self.assertIn("C-7", row["adoption_basis"])
        self.assertIn("C-8", row["adoption_basis"])

    def test_the_launch_eligible_correction_comment_is_kept(self):
        text = PROFILES_PATH.read_text(encoding="utf-8")
        self.assertIn("This row previously said `launch_eligible`", text)

    def test_the_limits_the_rulings_did_not_reopen_are_unchanged(self):
        row = _alpha()
        self.assertEqual(row["max_provider_draws_per_deliverable"], 2)
        self.assertEqual(row["repair_allowance"], 1)
        self.assertIs(row["fallback_required"], True)
        self.assertEqual(Decimal(str(row["default_job_cost_ceiling_usd"])), Decimal("5.00"))
        self.assertEqual(row["retention_days_default"], 30)
        self.assertEqual(row["surface_preference"]["rule"], "same_model_prefers_gcp")
        self.assertEqual(row["auto_routable_evidence_status"], ["clean_observed"])
        self.assertEqual(row["on_non_auto_routable"], "manual_route_required")


class SpendAuthorityIsSeparateFromAdoption(unittest.TestCase):
    """Controller rider, 14 Sep 2026: adopting the Alpha policy is NOT spend authorisation."""

    def test_no_profile_carries_spend_authority(self):
        for name, row in _rows().items():
            sa = row["spend_authority"]
            self.assertEqual(sa["status"], "none", name)
            self.assertIsNone(sa["record"], name)
            self.assertTrue(sa.get("note"), f"{name}: spend_authority.note must say why")

    def test_the_alpha_profile_names_the_rider(self):
        note = _alpha()["spend_authority"]["note"]
        self.assertIn("not spend authorisation", note)
        self.assertIn("none exists", note)

    def test_router_profile_may_spend_is_false_and_names_spend_authority(self):
        prof = B.profile("alpha_human_release")
        ok, reason = prof.may_spend()
        self.assertFalse(ok)
        self.assertIn("spend_authority", reason)
        self.assertIn("none", reason)

    def test_intake_profile_may_spend_is_false_and_names_spend_authority(self):
        prof = PolicyProfiles().profile("alpha_human_release")
        ok, reason = prof.may_spend()
        self.assertFalse(ok)
        self.assertIn("spend_authority", reason)

    def test_may_spend_names_adoption_when_that_is_what_is_missing(self):
        prof = B.profile("alpha_wider_example")
        ok, reason = prof.may_spend()
        self.assertFalse(ok)
        self.assertIn("adopted", reason)

    def test_may_spend_would_pass_only_with_adopted_and_a_signed_record(self):
        """The helper's positive branch, on an in-memory row. No such row exists on disk."""
        from runtime.route.profile import PolicyProfile as RouteProfile
        row = dict(_alpha())
        row["spend_authority"] = {"status": "signed", "record": "coordination/decisions/EXAMPLE.md", "note": "test"}
        ok, reason = RouteProfile(name="in_memory", row=row, path=PROFILES_PATH).may_spend()
        self.assertTrue(ok, reason)
        row["spend_authority"] = {"status": "signed", "record": None, "note": "test"}
        ok, reason = RouteProfile(name="in_memory", row=row, path=PROFILES_PATH).may_spend()
        self.assertFalse(ok)
        self.assertIn("record", reason)

    def test_spend_authority_accessor_refuses_when_absent(self):
        from runtime.route.profile import PolicyProfile as RouteProfile
        row = {k: v for k, v in _alpha().items() if k != "spend_authority"}
        with self.assertRaises(MissingLimit):
            _ = RouteProfile(name="in_memory", row=row, path=PROFILES_PATH).spend_authority
        with self.assertRaises(Exception):
            _ = IntakeProfile(name="in_memory", row=row, source=str(PROFILES_PATH)).spend_authority

    def test_execute_refuses_because_spend_authority_is_none(self):
        """CLOSED 14 Sep 2026 by lane F (execution bridge): Router.execute() checks spend_authority
        for a live-mode profile before it plans. alpha_human_release is adopted, dispatch_mode live,
        spend_authority none, so execute refuses and names the missing spend authorisation."""
        r = B.router()
        with self.assertRaises(ExecuteRefused) as ctx:
            r.execute(B.spec(B.SPEC_MOTION), B.profile("alpha_human_release"),
                      request_cost_ceiling_usd=Decimal("5.00"))
        self.assertIn("spend_authority", " ".join(ctx.exception.reasons))


class EveryProfileCarriesEveryRequiredLimit(unittest.TestCase):
    """Data completeness: a profile missing a limit refuses at intake, before any spend."""

    def test_the_new_limits_are_required_at_intake(self):
        required = _needs()["required_at_intake"]
        for name in ALPHA_1_LIMITS:
            self.assertIn(name, required)

    def test_every_required_at_intake_limit_is_on_every_profile(self):
        for name, row in _rows().items():
            for limit in _needs()["required_at_intake"]:
                self.assertIn(limit, row, f"profile {name!r} lacks required-at-intake limit {limit!r}")
                self.assertIsNotNone(row[limit], f"profile {name!r} has a null {limit!r}")

    def test_every_lane_declared_limit_is_on_every_profile(self):
        needs = _needs()
        for lane in ("read_by_router", "read_by_execution_bridge"):
            self.assertIn(lane, needs)
            self.assertTrue(needs[lane])
            for name, row in _rows().items():
                for limit in needs[lane]:
                    self.assertIn(limit, row, f"profile {name!r} lacks {limit!r} read by {lane}")

    def test_read_by_execution_bridge_names_spend_authority_first(self):
        self.assertEqual(_needs()["read_by_execution_bridge"][0], "spend_authority")

    def test_checked_profile_passes_for_every_row_in_the_contract(self):
        profiles = PolicyProfiles()
        for name in profiles.names():
            profiles.checked_profile(name)  # raises POLICY_LIMIT_MISSING on any gap


class C7ProductFamilyAsData(unittest.TestCase):
    def test_exact_text_strategies_exclude_generated_in_scene(self):
        allowed = _alpha()["exact_text_strategies_allowed"]
        self.assertEqual(allowed, ["code_set_on_textless_plate"])
        self.assertNotIn("generated_in_scene", allowed)
        self.assertEqual(B.profile("alpha_human_release").exact_text_strategies_allowed, allowed)
        self.assertEqual(PolicyProfiles().profile("alpha_human_release").exact_text_strategies_allowed, allowed)

    def test_the_allowed_kinds_are_exactly_the_c7_family(self):
        self.assertEqual(sorted(_alpha()["deliverable_kinds_allowed"]),
                         sorted(["static_ad", "short_motion_from_accepted_still", "static_ad_from_supplied_photo"]))

    def test_no_excluded_kind_is_allowed(self):
        row = _alpha()
        excluded = row["excluded_by_ruling"]
        self.assertTrue(excluded)
        registry = {k["kind"] for k in (load_yaml(paths.DELIVERABLE_KINDS) or {}).get("kinds", [])}
        for entry in excluded:
            self.assertIn("c7_phrase", entry, entry)
            self.assertTrue(entry["c7_phrase"])
            kind = entry.get("kind")
            if kind is not None:
                self.assertIn(kind, registry, f"excluded kind {kind!r} is not a registry kind")
                self.assertNotIn(kind, row["deliverable_kinds_allowed"])
            else:
                self.assertTrue(entry.get("note"), "an exclusion with no registry kind must say so")
        for kind in ("lipsync_to_supplied_audio", "two_speaker_dialogue", "spoken_voiceover", "multi_shot_story"):
            self.assertIn(kind, {e.get("kind") for e in excluded})

    def test_kinds_left_out_by_omission_are_recorded_and_not_allowed(self):
        row = _alpha()
        for kind in row["outside_alpha_1_by_omission"]:
            self.assertNotIn(kind, row["deliverable_kinds_allowed"])
        self.assertIn("text_in_motion", row["outside_alpha_1_by_omission"])

    def test_motion_derives_only_from_the_accepted_still(self):
        row = _alpha()
        self.assertIs(row["motion_requires_accepted_still"], True)
        self.assertIs(B.profile("alpha_human_release").motion_requires_accepted_still, True)
        self.assertIs(PolicyProfiles().profile("alpha_human_release").motion_requires_accepted_still, True)

    def test_speech_and_lipsync_are_off(self):
        row = _alpha()
        self.assertIs(row["native_speech_allowed"], False)
        self.assertIs(row["lipsync_allowed"], False)

    def test_supplied_photo_is_conditional_on_consent(self):
        cond = _alpha()["supplied_photo_conditions"]
        self.assertIs(cond["identifiable_person_requires_consent_ref"], True)
        self.assertIn("depicts_identifiable_person", cond["basis"])


class C8HumanRelease(unittest.TestCase):
    def test_every_output_requires_human_approval_and_nothing_is_delivered_autonomously(self):
        row = _alpha()
        self.assertEqual(row["acceptance_authority"], "human")
        self.assertIs(row["automated_judge_in_release_path"], False)
        self.assertIs(row["autonomous_external_delivery"], False)
        self.assertIs(row["human_approval_required_before_external_delivery"], True)
        self.assertIn("C-8", row["human_approval_basis"])

    def test_no_profile_delivers_autonomously(self):
        for name, row in _rows().items():
            self.assertIs(row["autonomous_external_delivery"], False, name)


class C11PublicReleaseGate(unittest.TestCase):
    @staticmethod
    def _report_conditions() -> list:
        """The twelve conditions as REPORT-A §7 T8 lists them, read mechanically: the numbered
        lines after 'Required conditions:' under the T8 heading, number and list punctuation
        stripped."""
        text = REPORT_A.read_text(encoding="utf-8")
        start = text.index("## T8 — Public beta gate")
        start = text.index("Required conditions:", start)
        out = []
        for line in text[start:].splitlines()[1:]:
            m = re.match(r"^\s*\d+\.\s+(.*?)[;.]?\s*$", line)
            if m:
                out.append(m.group(1))
            elif out:
                break
        return out

    def test_the_gate_is_adopted_and_carries_twelve_conditions(self):
        gate = _alpha()["public_release_gate"]
        self.assertIs(gate["adopted"], True)
        self.assertIn("C-11", gate["basis"])
        self.assertEqual(len(gate["conditions"]), 12)

    def test_the_conditions_equal_report_a_t8_verbatim(self):
        report = self._report_conditions()
        self.assertEqual(len(report), 12, report)
        self.assertEqual(_alpha()["public_release_gate"]["conditions"], report)

    def test_the_gate_says_none_is_met(self):
        note = _alpha()["public_release_gate"]["status_note"]
        self.assertIn("none of the twelve is met", note)
        self.assertIn("PRIVATE", note)


class NoLimitIsALiteralInTheAccessors(unittest.TestCase):
    """What this proves: the two modules that read profile rows contain no numeric literal other
    than 0 and 1 (checked over the syntax tree, so strings, comments and docstrings do not count).
    What it does not prove: that no limit is hidden as a string, or in some other module. The
    broader grep-style check lives in test_spec_compile."""

    def _numbers(self, path: Path) -> list:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        found = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) \
                    and not isinstance(node.value, bool) and node.value not in (0, 1):
                found.append((node.lineno, node.value))
        return found

    def test_profiles_py_has_no_numeric_literal_beyond_zero_and_one(self):
        self.assertEqual(self._numbers(Path(paths.RUNTIME) / "policy" / "profiles.py"), [])

    def test_route_profile_py_has_no_numeric_literal_beyond_zero_and_one(self):
        self.assertEqual(self._numbers(Path(paths.RUNTIME) / "route" / "profile.py"), [])


class DryProfileStillDry(unittest.TestCase):
    def test_dry_is_the_alpha_twin_is_adopted_and_has_no_spend_authority(self):
        """14 Sep 2026 (lane F): `dry` is the dry twin of alpha_human_release - the alpha's two draws,
        dispatch_mode dry, no spend authority. The zero-draw permissive row lives on as dry_permissive.
        The twin-equality test itself is runtime/tests/test_f_dry_twin.py."""
        row = _rows()["dry"]
        self.assertEqual(row["max_provider_draws_per_deliverable"], _alpha()["max_provider_draws_per_deliverable"])
        self.assertEqual(row["dispatch_mode"], "dry")
        self.assertIs(row["adopted"], True)
        self.assertEqual(row["spend_authority"]["status"], "none")
        prof = load_profile("dry", PROFILES_PATH)
        self.assertEqual(prof.max_provider_draws, 2)
        self.assertFalse(prof.may_spend()[0])
        permissive = _rows()["dry_permissive"]
        self.assertEqual(permissive["max_provider_draws_per_deliverable"], 0)
        self.assertEqual(permissive["dispatch_mode"], "dry")


class InvariantsSayWhatTheRulingsSay(unittest.TestCase):
    def test_the_invariants_separate_adoption_from_spend_authority(self):
        joined = " ".join(_doc()["invariants"])
        self.assertIn("NOT spend authority", joined)
        self.assertIn("spend_authority.status == signed", joined)
        self.assertIn("exact_text_strategies_allowed", joined)
        self.assertIn("never a silent downgrade", joined)


if __name__ == "__main__":
    unittest.main()
