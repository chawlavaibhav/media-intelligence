"""A brief becomes a PRODUCTION-SPEC, with no human authoring step in between."""
from __future__ import annotations

import copy
import unittest

from runtime import paths
from runtime.contract_schema import Contract
from runtime.errors import Refusal
from runtime.policy import PolicyProfiles
from runtime.spec.compile import SpecCompiler
from runtime.spec.planner_seam import FixturePlanner, NoCallPlanner
from runtime.tests import support
from runtime.util import canonical_json

FIXED = "2026-09-10T12:00:00Z"
BRIEFS = ("mustard-oil-tin", "showroom-photo-edit", "lipstick-packshot")


class DeterminismTest(unittest.TestCase):
    def test_the_same_job_compiles_to_a_byte_identical_spec_twice(self):
        for name in BRIEFS:
            job = support.submit(name)
            first = SpecCompiler().compile(job, compiled_utc=FIXED).spec
            second = SpecCompiler().compile(job, compiled_utc=FIXED).spec
            self.assertEqual(canonical_json(first), canonical_json(second), name)

    def test_only_the_clock_differs_between_two_live_runs(self):
        job = support.submit("mustard-oil-tin")
        first = SpecCompiler().compile(job).spec
        second = SpecCompiler().compile(job).spec
        self.assertEqual(
            canonical_json({k: v for k, v in first.items() if k != "compiled_utc"}),
            canonical_json({k: v for k, v in second.items() if k != "compiled_utc"}),
        )

    def test_the_spec_id_is_a_fingerprint_of_the_spec_not_of_the_hour(self):
        job = support.submit("mustard-oil-tin")
        early = SpecCompiler().compile(job, compiled_utc="2026-09-10T01:00:00Z").spec
        late = SpecCompiler().compile(job, compiled_utc="2026-11-30T23:59:59Z").spec
        self.assertEqual(early["spec_id"], late["spec_id"])

    def test_a_different_job_gives_a_different_spec_id(self):
        ids = {SpecCompiler().compile(support.submit(n), compiled_utc=FIXED).spec["spec_id"] for n in BRIEFS}
        self.assertEqual(len(ids), len(BRIEFS))


class ContractCoverageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = Contract.load(paths.SPEC_CONTRACT)

    def test_every_required_field_of_the_contract_is_filled(self):
        required = sorted(n for n, f in self.contract.fields.items() if f.get("required") is True)
        for name in BRIEFS:
            spec = SpecCompiler().compile(support.submit(name), compiled_utc=FIXED).spec
            for field in required:
                self.assertIn(field, spec, f"{name} left {field} unfilled")
                self.assertNotIn(spec[field], (None, "", [], {}), f"{name}: {field} is empty")

    def test_the_spec_validates_against_the_frozen_contract(self):
        for name in BRIEFS:
            spec = SpecCompiler().compile(support.submit(name), compiled_utc=FIXED).spec
            self.contract.validate(spec)

    def test_capability_requirements_never_name_a_model_a_provider_or_a_route(self):
        from runtime.evidence import EvidenceMap

        brands = set(EvidenceMap().brand_tokens()) | set(EvidenceMap().route_keys())
        for name in BRIEFS:
            spec = SpecCompiler().compile(support.submit(name), compiled_utc=FIXED).spec
            for row in spec["capability_requirements"]:
                words = row["capability"].replace("-", "_").split("_")
                self.assertTrue(set(words).isdisjoint(brands), row)

    def test_the_job_fingerprint_is_carried_forward(self):
        job = support.submit("mustard-oil-tin")
        from runtime.util import sha256_obj

        spec = SpecCompiler().compile(job, compiled_utc=FIXED).spec
        self.assertEqual(spec["job_sha256"], sha256_obj(job))
        self.assertEqual(spec["job_id"], job["job_id"])


class BudgetTest(unittest.TestCase):
    def test_both_budget_numbers_come_from_the_policy_profile(self):
        job = support.submit("mustard-oil-tin")
        spec = SpecCompiler().compile(job, compiled_utc=FIXED).spec
        profile = PolicyProfiles().profile(job["policy_profile"])
        self.assertEqual(spec["budget"]["max_provider_draws"], profile.limit("max_provider_draws_per_deliverable"))
        self.assertEqual(spec["budget"]["repair_allowance"], profile.limit("repair_allowance"))

    def test_widening_the_profile_widens_the_spec_with_no_code_change(self):
        raw = copy.deepcopy(support.brief("mustard-oil-tin"))
        raw["policy_profile"] = "wide_and_generous"
        profiles = support.test_profiles()
        job = support.intake(profiles).submit(raw).job
        spec = SpecCompiler(profiles=profiles).compile(job, compiled_utc=FIXED).spec
        self.assertEqual(spec["budget"]["max_provider_draws"], 9)
        self.assertEqual(spec["budget"]["repair_allowance"], 4)

    def test_a_profile_missing_a_limit_refuses_at_compile_too(self):
        profiles = support.test_profiles()
        job = support.submit("mustard-oil-tin")
        job = dict(job, policy_profile="missing_a_limit")
        with self.assertRaises(Refusal) as caught:
            SpecCompiler(profiles=profiles).compile(job, compiled_utc=FIXED)
        self.assertEqual(caught.exception.code, Refusal.POLICY_LIMIT_MISSING)

    def test_no_operating_limit_is_a_constant_in_the_code_that_consumes_limits(self):
        """POLICY-PROFILES-v0 invariant: "No limit in this file is referenced by a constant
        anywhere in runtime code." Checked over the three modules that read limits."""
        import re
        from pathlib import Path

        from runtime.util import load_yaml

        numbers = set()
        for row in (load_yaml(paths.POLICY_PROFILES) or {}).get("profiles", []):
            for key, value in row.items():
                if key.startswith(("max_", "repair_", "default_job_", "retention_")) and isinstance(value, (int, float)):
                    if value in (0, 1):
                        continue  # 0 and 1 are not distinguishable from ordinary code
                    numbers.add(value)
        self.assertTrue(numbers)
        consumers = [
            Path(paths.RUNTIME) / "spec" / "compile.py",
            Path(paths.RUNTIME) / "intake" / "intake.py",
            Path(paths.RUNTIME) / "policy" / "profiles.py",
        ]
        for path in consumers:
            body = _code_only(path)
            for number in numbers:
                found = re.search(rf"(?<![\w.]){re.escape(str(number))}(?![\w.])", body)
                self.assertIsNone(found, f"{path.name} carries the limit value {number} as a literal")

    def test_every_limit_reaches_the_spec_through_the_profile_object(self):
        """Not a grep: the budget numbers are proven to come out of PolicyProfile.limit()."""
        from runtime.policy.profiles import PolicyProfile

        seen = []
        original = PolicyProfile.limit

        def spy(self, limit_name):
            value = original(self, limit_name)
            seen.append((limit_name, value))
            return value

        PolicyProfile.limit = spy
        try:
            spec = SpecCompiler().compile(support.submit("mustard-oil-tin"), compiled_utc=FIXED).spec
        finally:
            PolicyProfile.limit = original
        self.assertIn(("max_provider_draws_per_deliverable", spec["budget"]["max_provider_draws"]), seen)
        self.assertIn(("repair_allowance", spec["budget"]["repair_allowance"]), seen)


class SeamTest(unittest.TestCase):
    def test_the_lane_makes_no_model_call(self):
        job = support.submit("mustard-oil-tin")
        with self.assertRaises(Refusal) as caught:
            SpecCompiler(planner=NoCallPlanner()).compile(job, compiled_utc=FIXED)
        self.assertEqual(caught.exception.code, Refusal.NO_DISPATCH_ALLOWED)

    def test_an_unrecorded_prompt_refuses_and_writes_the_payload_out(self):
        import json
        import tempfile
        from pathlib import Path

        spill = Path(tempfile.mkdtemp(prefix="runtime-spill-"))
        empty = Path(tempfile.mkdtemp(prefix="runtime-fixtures-"))
        planner = FixturePlanner(fixture_dir=empty, spill_dir=spill)
        job = support.submit("mustard-oil-tin")
        with self.assertRaises(Refusal) as caught:
            SpecCompiler(planner=planner).compile(job, compiled_utc=FIXED)
        self.assertEqual(caught.exception.code, Refusal.PLANNER_FIXTURE_MISSING)
        written = list(spill.glob("*.prompt.json"))
        self.assertEqual(len(written), 1)
        payload = json.loads(written[0].read_text(encoding="utf-8"))
        self.assertIn("system", payload)
        self.assertIn("CANON_DOCTRINE", payload["system"])   # the cached prefix is Canon
        self.assertIn("शुद्ध कच्ची घाणी सरसों का तेल", payload["user"])

    def test_the_reasoning_pass_may_not_invent_fields_the_spec_cannot_hold(self):
        from runtime.spec.planner_seam import validate_response

        with self.assertRaises(Refusal) as caught:
            validate_response({"objective": "x", "hard_constraints": ["y"],
                               "acceptance_statements": ["ACCEPT only if z."], "route": "seedream-5-pro"})
        self.assertEqual(caught.exception.code, Refusal.PLANNER_RESPONSE_INVALID)

    def test_the_canon_prefix_carries_no_request_specific_bytes(self):
        """INJECTION-CONTRACT §2: nothing request-specific sits upstream of the cache breakpoint."""
        from runtime.spec.planner_seam import build_prompt
        from runtime.canon.normalize import normalize
        from runtime.canon.packs import CanonCorpus
        from runtime.spec import text_strategy

        corpus = CanonCorpus()
        systems = set()
        for name in ("mustard-oil-tin", "lipstick-packshot"):
            job = support.submit(name)
            nr = normalize(job)
            canon = corpus.inject(nr)
            prompt = build_prompt(job, nr, canon, text_strategy.choose(nr))
            self.assertNotIn(job["job_id"], prompt.system)
            self.assertNotIn(job["brief"]["text"], prompt.system)
            self.assertNotIn(job["exact_text_strings"][0]["value"], prompt.system)
            systems.add(prompt.system)
        # Two different requests, one identical prefix: the same packs were injected, so the
        # cached prefix is byte-identical and the volatile turn carries everything request-specific.
        self.assertEqual(len(systems), 1)
        prefix = systems.pop()
        self.assertTrue(prefix.startswith(corpus.system_prompt_block))
        for pack_id in ("composition_and_attention", "product_appearance"):
            self.assertIn(corpus.packs[pack_id].terse_injection_text, prefix)


class CliTest(unittest.TestCase):
    def test_one_command_prints_a_complete_spec_and_the_canon_payload(self):
        import io
        import contextlib

        from runtime import cli

        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = cli.main([str(paths.BRIEF_FIXTURES / "mustard-oil-tin.json"), "--at", FIXED, "--canon"])
        text = out.getvalue()
        self.assertEqual(code, 0)
        self.assertIn("PRODUCTION-SPEC-v0", text)
        self.assertIn("ACCEPTANCE CONTRACT", text)
        self.assertIn("EXACT CANON PAYLOAD", text)
        self.assertIn("CANON_DOCTRINE packs are compiled production decisions", text)

    def test_a_refusal_leaves_the_command_with_a_non_zero_exit(self):
        import io
        import contextlib
        import json
        import tempfile
        from pathlib import Path

        raw = copy.deepcopy(support.brief("mustard-oil-tin"))
        raw["policy_profile"] = "no_such_profile"
        path = Path(tempfile.mkdtemp()) / "bad.json"
        path.write_text(json.dumps(raw), encoding="utf-8")
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = cli_main(str(path))
        self.assertEqual(code, 2)
        self.assertIn("POLICY_PROFILE_UNKNOWN", err.getvalue())


def cli_main(path: str) -> int:
    from runtime import cli

    return cli.main([path])


if __name__ == "__main__":
    unittest.main()


def _code_only(path) -> str:
    """The file with comments and string literals removed — a number in prose is not a constant."""
    import io
    import tokenize

    kept = []
    with open(path, "rb") as fh:
        for token in tokenize.tokenize(fh.readline):
            if token.type in (tokenize.COMMENT, tokenize.STRING):
                continue
            kept.append(token.string)
    return " ".join(kept)
