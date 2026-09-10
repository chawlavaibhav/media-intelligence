"""The deterministic pack lookup of CANON-SHAPE-v1 section 4."""
from __future__ import annotations

import unittest

from runtime.canon.normalize import normalize
from runtime.canon.packs import CanonCorpus
from runtime.tests import support


class PackLookupTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.corpus = CanonCorpus()

    def lookup(self, name: str):
        job = support.submit(name)
        return self.corpus.inject(normalize(job))

    def test_the_same_request_selects_the_same_packs_and_the_same_bytes(self):
        first = self.lookup("mustard-oil-tin")
        second = self.lookup("mustard-oil-tin")
        self.assertEqual([s.pack_id for s in first.selections], [s.pack_id for s in second.selections])
        self.assertEqual([s.trigger for s in first.selections], [s.trigger for s in second.selections])
        self.assertEqual(first.injected_context_sha256, second.injected_context_sha256)
        self.assertEqual(first.payload, second.payload)

    def test_the_fingerprint_is_over_the_exact_injected_bytes(self):
        import hashlib

        result = self.lookup("mustard-oil-tin")
        self.assertEqual(
            result.injected_context_sha256,
            hashlib.sha256(result.payload.encode("utf-8")).hexdigest(),
        )

    def test_only_accepted_compiled_packs_are_injected(self):
        result = self.lookup("mustard-oil-tin")
        self.assertEqual(sorted(result.injected_pack_ids), ["composition_and_attention", "product_appearance"])
        for pack_id in result.injected_pack_ids:
            pack = self.corpus.packs[pack_id]
            self.assertTrue(pack.accepted)
            self.assertEqual(pack.corpus_digest, self.corpus.accepted_digest)
            self.assertIn(pack.terse_injection_text, result.payload)

    def test_the_invariant_system_block_leads_the_payload(self):
        result = self.lookup("mustard-oil-tin")
        self.assertTrue(result.payload.startswith(self.corpus.system_prompt_block))

    def test_a_trigger_with_no_compiled_pack_sets_canon_gap_and_the_job_continues(self):
        result = self.lookup("mustard-oil-tin")
        fired = {s.pack_id for s in result.selections}
        self.assertIn("typography_and_copy", fired)          # text_requirements_nonempty fired
        self.assertNotIn("typography_and_copy", result.injected_pack_ids)  # nothing compiled for it
        self.assertTrue(result.canon_gap)
        self.assertIn("typography_and_copy", result.missing_domain)
        # and the job still compiles all the way to a spec
        spec = support.compiler().compile(support.submit("mustard-oil-tin"), compiled_utc="2026-09-10T12:00:00Z").spec
        self.assertTrue(spec["canon"]["canon_gap"])
        self.assertIn("typography_and_copy", spec["canon"]["missing_domain"])

    def test_a_gap_never_names_a_compilation_programme(self):
        result = self.lookup("mustard-oil-tin")
        self.assertNotIn("compil", (result.missing_domain or "").lower())

    def test_no_hold_material_can_reach_the_payload(self):
        result = self.lookup("mustard-oil-tin")
        self.assertNotIn("canon/candidates/", result.payload)
        self.assertNotIn("canon/qa/", result.payload)

    def test_an_uncertain_modality_injects_the_bounded_union_never_a_guess(self):
        result = self.lookup("lipstick-packshot")  # a still deliverable that also wants motion
        triggers = {s.pack_id: s.trigger for s in result.selections}
        self.assertIn("uncertainty_rule", triggers["composition_and_attention"])
        for pack_id in ("camera_and_spatial_grammar", "editing_pacing_and_short_form"):
            self.assertIn(pack_id, triggers)  # the video base set is present too
        self.assertLessEqual(result.tokens, self.corpus.triggers["per_request_max_tokens"])

    def test_the_selection_is_a_table_lookup_not_a_judgement(self):
        """Every selected pack cites the trigger row that put it there."""
        result = self.lookup("showroom-photo-edit")
        for selection in result.selections:
            self.assertTrue(selection.trigger)
            self.assertIn(selection.pack_id, self.corpus.triggers["pack_ids_closed_set"])


if __name__ == "__main__":
    unittest.main()
