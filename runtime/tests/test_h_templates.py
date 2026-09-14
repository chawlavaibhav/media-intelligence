"""The template library (CANON-SHAPE-v1 §4 last stage; Controller ruling C-10): accepted plans
kept as slot-filled assets so a repeat job needs no reasoning pass. Everything here is offline and
synthetic: the outcome events are minimal dicts in the WAVE2 OUTCOME-EVENT-v1 shape."""
from __future__ import annotations

import copy
import json
import re
import tempfile
import unittest
from pathlib import Path

from runtime import paths
from runtime.canon.normalize import normalize
from runtime.canon.packs import CanonCorpus
from runtime.canon.templates import (
    IDENTITY_VERSION,
    TemplateLibrary,
    normalized_identity,
    identity_fields,
    response_fields,
    TEMPLATE_IMMUTABLE,
    TEMPLATE_PROMOTION_REFUSED,
    TEMPLATE_SLOT_MISMATCH,
)
from runtime.contract_schema import Contract
from runtime.errors import Refusal
from runtime.spec.acceptance import StyleGuard
from runtime.tests import support

FIXED = "2026-09-14T10:00:00Z"
RECEIPT_WORDS = ("FAILURE_PREVENTION", "DOCTRINE_DEVIATIONS")
ID_TOKEN = re.compile(r"\b(?:sk|scs)_[a-z0-9_]+\b")


def v1_spec(name: str) -> tuple:
    """A compiled v0 spec lifted to the WAVE2 PRODUCTION-SPEC-v1 shape (the fields lane E adds)."""
    job = support.submit(name)
    spec = copy.deepcopy(support.compiler().compile(job, compiled_utc=FIXED).spec)
    spec["schema"] = "PRODUCTION-SPEC-v1"
    spec["policy_profile"] = job["policy_profile"]
    for item in spec["exact_text"]["strings"]:
        item["placement"] = "overlay"
    spec["exact_text"]["text_mechanism"] = "deterministic_text_composition"
    spec["canon"]["injection_version"] = "v1"
    strings = [t["content"] for t in spec["exact_text"]["strings"]]
    spec["blueprint"] = {
        "generation_prompts": {
            "main": (
                "A single one-litre mustard oil tin on a deep maroon ground lit by one low warm source "
                "from the lower left; matte clay diyas; no lettering of any kind in the picture; the "
                f"copy {', '.join(strings)} is set by code afterwards."
            ),
            "textless_plate": (
                "Textless plate: the same tin, ground and light with generous clear space in the upper "
                "zone and along the lower band where lettering will be set by code; no text anywhere."
            ),
            "motion": None,
        },
        "planner": "recorded_fixture",
        "source_ref": "runtime/fixtures/planner/mustard-oil-tin.response.json",
        "case_values": {},
        "production_parameters": {},
    }
    return job, spec


def event(spec: dict, *, decision="accepted", authority="human", dry_run=False, eligible=None,
          event_id="evt-0001", corpus_digest=None) -> dict:
    """A minimal OUTCOME-EVENT-v1 per WAVE2-INTERFACES §4; only the fields promotion reads."""
    out = {
        "schema": "OUTCOME-EVENT-v1",
        "event_id": event_id,
        "job_id": spec["job_id"],
        "spec_id": spec["spec_id"],
        "dry_run": dry_run,
        "route": {
            "route_key": "seedream-5-pro@fal",
            "cell_key": "static_ad|devanagari|overlay|code_set_on_textless_plate",
            "text_mechanism": "deterministic_text_composition",
        },
        "canon": {
            "packs_selected": [r["pack_id"] for r in spec["canon"]["packs_selected"]],
            "corpus_digest": corpus_digest or CanonCorpus().accepted_digest,
        },
        "acceptance": {"decision": decision, "authority": authority, "decided_utc": FIXED},
    }
    if eligible is not None:
        out["template_candidate"] = {"eligible": eligible, "reason": "synthetic"}
    return out


class IdentityTest(unittest.TestCase):
    def test_the_identity_covers_exactly_the_documented_field_set(self):
        nr = normalize(support.submit("mustard-oil-tin"))
        fields = identity_fields(nr)
        self.assertEqual(
            sorted(fields),
            sorted(["identity_version", "kind", "modality", "requested_operation", "aspect", "exact_text",
                    "motion", "supplied_asset_roles", "entity_roles", "market", "language"]),
        )
        self.assertEqual(fields["identity_version"], IDENTITY_VERSION)
        self.assertEqual(fields["kind"], "static_ad")
        self.assertEqual(fields["aspect"], "1:1")
        self.assertEqual(fields["supplied_asset_roles"], ["product"])
        self.assertIsNone(fields["motion"])
        # strings are in, sorted, with script and placement; bytes and ids of assets are out
        self.assertEqual([s["content"] for s in fields["exact_text"]], sorted(s["content"] for s in fields["exact_text"]))
        blob = json.dumps(fields, ensure_ascii=False)
        self.assertNotIn("ast_tin_front", blob)
        self.assertNotIn("9f2c1a55d0b3e47a", blob)
        self.assertNotIn("JOB-2026", blob)

    def test_the_same_job_shape_gives_the_same_identity_and_a_different_aspect_does_not(self):
        a = normalize(support.submit("mustard-oil-tin"))
        b = normalize(support.submit("mustard-oil-tin", job_id="JOB-OTHER-01", customer_ref="acct_9"))
        self.assertEqual(normalized_identity(a), normalized_identity(b))
        job = support.brief("mustard-oil-tin")
        job["deliverable_request"]["aspect"] = "9:16"
        c = normalize(support.submit("mustard-oil-tin", deliverable_request=job["deliverable_request"]))
        self.assertNotEqual(normalized_identity(a), normalized_identity(c))


class TemplateLibraryTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="runtime-templates-"))
        self.library = TemplateLibrary(root=self.root)
        self.job, self.spec = v1_spec("mustard-oil-tin")
        self.nr = normalize(self.job)

    # ------------------------------------------------------------ promotion
    def test_promote_refuses_a_rejected_event(self):
        with self.assertRaises(Refusal) as caught:
            self.library.promote(self.spec, event(self.spec, decision="rejected"), nr=self.nr, created_utc=FIXED)
        self.assertEqual(caught.exception.code, TEMPLATE_PROMOTION_REFUSED)
        self.assertIn("rejected", str(caught.exception))
        self.assertEqual(list(self.root.glob("*.json")), [])

    def test_promote_refuses_a_non_human_authority(self):
        with self.assertRaises(Refusal) as caught:
            self.library.promote(self.spec, event(self.spec, authority="automated_judge"), nr=self.nr, created_utc=FIXED)
        self.assertEqual(caught.exception.code, TEMPLATE_PROMOTION_REFUSED)
        self.assertIn("human", str(caught.exception))

    def test_promote_from_an_accepted_event_yields_a_template_that_validates(self):
        template = self.library.promote(self.spec, event(self.spec), nr=self.nr, created_utc=FIXED)
        Contract.load(paths.TEMPLATE_CONTRACT).validate(template)
        self.assertTrue(template["template_id"].startswith("tpl-"))
        self.assertEqual(template["status"], "reusable")
        self.assertEqual(template["identity_version"], IDENTITY_VERSION)
        self.assertEqual(template["normalized_identity"], normalized_identity(self.nr))
        self.assertEqual(template["accepted_event_id"], "evt-0001")
        self.assertEqual(template["blueprint"]["objective"], self.spec["objective"])
        self.assertEqual(template["blueprint"]["acceptance_statements"], self.spec["acceptance_contract"])
        self.assertEqual(template["blueprint"]["generation_prompts"]["main"], self.spec["blueprint"]["generation_prompts"]["main"])
        self.assertEqual(template["canon"]["prefix_sha256"], self.spec["canon"]["injected_context_sha256"])
        self.assertEqual(template["canon"]["injection_version"], "v1")
        self.assertEqual(sorted(template["canon"]["packs_injected"]), ["composition_and_attention", "product_appearance"])
        self.assertEqual(template["route_hint"]["text_mechanism"], "deterministic_text_composition")
        self.assertEqual([s["content"] for s in template["slots"]], [t["content"] for t in self.nr.text_requirements])
        # stored as JSON under root/<template_id>.json
        path = self.root / f"{template['template_id']}.json"
        self.assertTrue(path.exists())
        with open(path, encoding="utf-8") as fh:
            self.assertEqual(json.load(fh), template)

    def test_a_dry_event_makes_a_dry_only_template_and_needs_eligibility(self):
        with self.assertRaises(Refusal) as caught:
            self.library.promote(self.spec, event(self.spec, dry_run=True), nr=self.nr, created_utc=FIXED)
        self.assertEqual(caught.exception.code, TEMPLATE_PROMOTION_REFUSED)
        template = self.library.promote(self.spec, event(self.spec, dry_run=True, eligible=True), nr=self.nr, created_utc=FIXED)
        self.assertEqual(template["status"], "reusable_dry_only")
        self.assertTrue(template["provenance"]["dry_run"])
        # a dry-only template never serves a live job
        self.assertIsNone(self.library.match(self.nr))
        self.assertEqual(self.library.match(self.nr, dispatch_mode="dry")["template_id"], template["template_id"])

    def test_promote_refuses_an_event_for_a_different_spec(self):
        other = event(self.spec)
        other["spec_id"] = "spec-somethingelse"
        with self.assertRaises(Refusal) as caught:
            self.library.promote(self.spec, other, nr=self.nr, created_utc=FIXED)
        self.assertEqual(caught.exception.code, TEMPLATE_PROMOTION_REFUSED)

    def test_promote_refuses_a_spec_without_generation_prompts(self):
        spec = copy.deepcopy(self.spec)
        del spec["blueprint"]
        with self.assertRaises(Refusal) as caught:
            self.library.promote(spec, event(spec), nr=self.nr, created_utc=FIXED)
        self.assertEqual(caught.exception.code, TEMPLATE_PROMOTION_REFUSED)
        self.assertIn("generation_prompts", str(caught.exception))

    def test_promote_refuses_a_missing_corpus_digest_rather_than_inventing_one(self):
        ev = event(self.spec)
        del ev["canon"]["corpus_digest"]
        with self.assertRaises(Refusal) as caught:
            self.library.promote(self.spec, ev, nr=self.nr, created_utc=FIXED)
        self.assertEqual(caught.exception.code, TEMPLATE_PROMOTION_REFUSED)
        self.assertIn("corpus_digest", str(caught.exception))

    def test_the_store_is_immutable(self):
        first = self.library.promote(self.spec, event(self.spec), nr=self.nr, created_utc=FIXED)
        with self.assertRaises(Refusal) as caught:
            self.library.promote(self.spec, event(self.spec), nr=self.nr, created_utc="2026-09-15T10:00:00Z")
        self.assertEqual(caught.exception.code, TEMPLATE_IMMUTABLE)
        with open(self.root / f"{first['template_id']}.json", encoding="utf-8") as fh:
            self.assertEqual(json.load(fh)["created_utc"], FIXED)

    def test_a_template_never_contains_a_hold_id_or_receipt_vocabulary(self):
        from canon.gate.doctrine import candidate_ids

        template = self.library.promote(self.spec, event(self.spec), nr=self.nr, created_utc=FIXED)
        blob = json.dumps(template, ensure_ascii=False)
        for word in RECEIPT_WORDS:
            self.assertNotIn(word, blob)
        hold = candidate_ids()
        self.assertTrue(hold)
        self.assertEqual(sorted(t for t in set(ID_TOKEN.findall(blob)) if t in hold), [])
        # and a plan that smuggles either in is refused at promotion
        tainted = copy.deepcopy(self.spec)
        tainted["objective"] = tainted["objective"] + " Record overrides in DOCTRINE_DEVIATIONS."
        with self.assertRaises(Refusal) as caught:
            TemplateLibrary(root=Path(tempfile.mkdtemp())).promote(tainted, event(tainted), nr=self.nr, created_utc=FIXED)
        self.assertEqual(caught.exception.code, TEMPLATE_PROMOTION_REFUSED)
        tainted = copy.deepcopy(self.spec)
        tainted["objective"] = tainted["objective"] + " see " + sorted(hold)[0]
        with self.assertRaises(Refusal) as caught:
            TemplateLibrary(root=Path(tempfile.mkdtemp())).promote(tainted, event(tainted), nr=self.nr, created_utc=FIXED)
        self.assertEqual(caught.exception.code, TEMPLATE_PROMOTION_REFUSED)

    # ------------------------------------------------------------ match
    def test_match_returns_the_template_for_the_same_identity_and_none_for_another_aspect(self):
        self.assertIsNone(self.library.match(self.nr))
        template = self.library.promote(self.spec, event(self.spec), nr=self.nr, created_utc=FIXED)
        repeat = normalize(support.submit("mustard-oil-tin", job_id="JOB-2026-09-15-MUSTARD-02"))
        found = self.library.match(repeat)
        self.assertIsNotNone(found)
        self.assertEqual(found["template_id"], template["template_id"])
        request = dict(self.job["deliverable_request"], aspect="9:16")
        other = normalize(support.submit("mustard-oil-tin", deliverable_request=request))
        self.assertIsNone(self.library.match(other))

    def test_match_prefers_the_newest_when_several_share_an_identity(self):
        old = self.library.promote(self.spec, event(self.spec, event_id="evt-old"), nr=self.nr, created_utc="2026-09-13T10:00:00Z")
        new = self.library.promote(self.spec, event(self.spec, event_id="evt-new"), nr=self.nr, created_utc="2026-09-14T10:00:00Z")
        self.assertNotEqual(old["template_id"], new["template_id"])
        self.assertEqual(self.library.match(self.nr)["template_id"], new["template_id"])

    # ------------------------------------------------------------ fill
    def test_fill_replaces_every_string_and_marks_the_planner(self):
        template = self.library.promote(self.spec, event(self.spec), nr=self.nr, created_utc=FIXED)
        # the same shape, different copy: new price, new tagline, new shop name
        strings = [
            {"value": "असली कच्ची घाणी सरसों का तेल", "script": "devanagari", "may_reflow": False},
            {"value": "₹199 प्रति लीटर", "script": "devanagari", "may_reflow": False},
            {"value": "शर्मा ऑयल मिल्स", "script": "devanagari", "may_reflow": False},
        ]
        job = support.submit("mustard-oil-tin", job_id="JOB-2026-09-15-SHARMA-01", exact_text_strings=strings)
        nr = normalize(job)
        filled = self.library.fill(template, job, nr)
        self.assertEqual(filled["planner"], f"template:{template['template_id']}")
        blob = json.dumps(filled, ensure_ascii=False)
        for old in (s["content"] for s in template["slots"]):
            self.assertNotIn(old, blob)
        for new in (s["value"] for s in strings):
            self.assertIn(new, blob)
        # the fields the planner seam expects are all there, and only there once trimmed
        subset = response_fields(filled)
        from runtime.spec.planner_seam import validate_response

        validate_response(subset, source="template")
        self.assertIn("generation_prompts", filled)
        self.assertIn("₹199", filled["generation_prompts"]["main"])
        self.assertNotIn("₹185", filled["generation_prompts"]["main"])

    def test_fill_refuses_on_a_slot_count_mismatch(self):
        template = self.library.promote(self.spec, event(self.spec), nr=self.nr, created_utc=FIXED)
        strings = [{"value": "₹199 प्रति लीटर", "script": "devanagari", "may_reflow": False}]
        job = support.submit("mustard-oil-tin", exact_text_strings=strings)
        with self.assertRaises(Refusal) as caught:
            self.library.fill(template, job, normalize(job))
        self.assertEqual(caught.exception.code, TEMPLATE_SLOT_MISMATCH)

    def test_the_filled_plans_acceptance_statements_pass_the_style_guard(self):
        template = self.library.promote(self.spec, event(self.spec), nr=self.nr, created_utc=FIXED)
        strings = [
            {"value": "असली कच्ची घाणी सरसों का तेल", "script": "devanagari", "may_reflow": False},
            {"value": "₹199 प्रति लीटर", "script": "devanagari", "may_reflow": False},
            {"value": "शर्मा ऑयल मिल्स", "script": "devanagari", "may_reflow": False},
        ]
        job = support.submit("mustard-oil-tin", exact_text_strings=strings)
        nr = normalize(job)
        filled = self.library.fill(template, job, nr)
        guard = StyleGuard()
        guard.check(filled["acceptance_statements"], exempt_literals=[t["content"] for t in nr.text_requirements])
        guard.check_count(filled["acceptance_statements"])

    def test_the_default_store_is_under_runtime_store_never_eval(self):
        self.assertEqual(paths.TEMPLATE_STORE, paths.DEFAULT_STORE / "templates")
        self.assertNotIn("eval", paths.TEMPLATE_STORE.parts)
        self.assertEqual(TemplateLibrary().root, paths.TEMPLATE_STORE)


if __name__ == "__main__":
    unittest.main()
