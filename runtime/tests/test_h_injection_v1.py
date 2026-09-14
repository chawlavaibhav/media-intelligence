"""Canon Injection v1 (CANON-SHAPE-v1 §4-§5, Controller ruling C-10): a receipt-free, byte-stable,
cache-served prefix, with the v0 path left byte-for-byte intact behind a constructor switch."""
from __future__ import annotations

import hashlib
import math
import re
import unittest

from runtime import paths
from runtime.canon.normalize import normalize
from runtime.canon.packs import CanonCorpus, CACHE_BOUNDARY_MARKER
from runtime.tests import support
from runtime.util import read_text

# The v0 payload for the three fixture briefs, recorded on 14 Sep 2026 BEFORE this lane changed
# anything (all three select the same two compiled packs, so all three share one prefix).
V0_PAYLOAD_SHA256 = "0734d615e315d5700a7848a8c493789f4b9eb3b008b005d4e902c7dd01b73644"
RECEIPT_WORDS = ("FAILURE_PREVENTION", "DOCTRINE_DEVIATIONS")
_FENCE = re.compile(r"^```\n(.*?)^```", re.S | re.M)


def _hold_ids() -> set:
    # The gate's own way of enumerating the HOLD lane (canon/gate/doctrine.py), read-only.
    from canon.gate.doctrine import candidate_ids

    return candidate_ids()


class InjectionV1Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v1 = CanonCorpus()                         # v1 is the default
        cls.v0 = CanonCorpus(injection_version="v0")

    def lookup(self, corpus, name):
        return corpus.inject(normalize(support.submit(name)))

    # ------------------------------------------------------------ the block itself
    def test_v1_is_the_default_and_reads_the_runtime_owned_prefix_file(self):
        self.assertEqual(self.v1.injection_version, "v1")
        fenced = _FENCE.search(read_text(paths.INJECTION_PREFIX_V1)).group(1)
        self.assertEqual(self.v1.system_prompt_block, fenced)
        self.assertEqual(self.v1.system_prompt_block_v1, fenced)

    def test_the_v1_block_carries_no_receipt_instruction(self):
        for word in RECEIPT_WORDS:
            self.assertNotIn(word, self.v1.system_prompt_block)
            self.assertIn(word, self.v0.system_prompt_block)       # and v0 still does
        self.assertNotIn("pass or fix", self.v1.system_prompt_block)
        self.assertIn("verified mechanically", self.v1.system_prompt_block)

    def test_the_marker_legend_is_verbatim_from_v0(self):
        v0_legend = self.v0.system_prompt_block[self.v0.system_prompt_block.index("Marker legend."):]
        v1_legend = self.v1.system_prompt_block[self.v1.system_prompt_block.index("Marker legend."):]
        self.assertEqual(v0_legend, v1_legend)

    def test_the_v1_block_stays_within_the_trigger_tables_system_block_budget(self):
        budget = self.v1.triggers["system_prompt_block_tokens"]
        tokens = math.ceil(len(self.v1.system_prompt_block) / 4)
        self.assertLessEqual(tokens, budget)
        # and the figure the prefix file states is the figure the bytes give
        self.assertIn(f"{len(self.v1.system_prompt_block):,} chars = {tokens} tokens", read_text(paths.INJECTION_PREFIX_V1))

    # ------------------------------------------------------------ the lookup fields
    def test_lookup_records_the_v1_metadata(self):
        result = self.lookup(self.v1, "mustard-oil-tin")
        self.assertEqual(result.injection_version, "v1")
        self.assertFalse(result.receipts_required)
        self.assertEqual(result.cache_pricing, "not pinned")
        self.assertIn("CANON-SHAPE-v1", result.cache_pricing_note)
        self.assertEqual(result.cache_boundary_marker, CACHE_BOUNDARY_MARKER)
        # the marker documents the boundary; it is metadata and never enters the payload
        self.assertNotIn(CACHE_BOUNDARY_MARKER, result.payload)

    def test_prefix_sha_is_over_exactly_the_bytes_upstream_of_the_breakpoint(self):
        result = self.lookup(self.v1, "mustard-oil-tin")
        expected = "\n\n".join(
            [self.v1.system_prompt_block]
            + [self.v1.packs[p].terse_injection_text for p in result.injected_pack_ids]
        )
        self.assertEqual(result.payload, expected)
        self.assertEqual(result.prefix_sha256, hashlib.sha256(expected.encode("utf-8")).hexdigest())
        # PRODUCTION-SPEC's name for the same bytes: equal by construction in v1
        self.assertEqual(result.prefix_sha256, result.injected_context_sha256)

    def test_two_different_jobs_with_the_same_packs_share_one_byte_identical_prefix(self):
        a_job, b_job = support.submit("mustard-oil-tin"), support.submit("lipstick-packshot")
        a_nr, b_nr = normalize(a_job), normalize(b_job)
        self.assertNotEqual(a_nr.as_dict(), b_nr.as_dict())            # the volatile part differs
        a, b = self.v1.inject(a_nr), self.v1.inject(b_nr)
        self.assertEqual(a.injected_pack_ids, b.injected_pack_ids)
        self.assertEqual(a.prefix_sha256, b.prefix_sha256)
        self.assertEqual(a.payload, b.payload)
        for job in (a_job, b_job):
            self.assertNotIn(job["job_id"], a.payload)
            self.assertNotIn(job["brief"]["text"], a.payload)
            for item in job["exact_text_strings"]:
                self.assertNotIn(item["value"], a.payload)

    def test_the_order_of_injected_packs_is_the_trigger_tables_canonical_order(self):
        result = self.lookup(self.v1, "mustard-oil-tin")
        by_order = sorted(
            (s for s in result.selections if s.status == "compiled_accepted"), key=lambda s: s.order_index
        )
        self.assertEqual(tuple(s.pack_id for s in by_order), result.injected_pack_ids)
        positions = [result.payload.index(self.v1.packs[p].terse_injection_text) for p in result.injected_pack_ids]
        self.assertEqual(positions, sorted(positions))

    def test_receipt_words_that_survive_in_pack_text_are_reported_not_hidden(self):
        """OBSERVED 14 Sep 2026: the compiled packs' own terse text still carries the v0 receipt
        sentence. The runtime never rewrites pack bytes, so it says so instead."""
        result = self.lookup(self.v1, "mustard-oil-tin")
        carried = [p for p in result.injected_pack_ids
                   if any(w in self.v1.packs[p].terse_injection_text for w in RECEIPT_WORDS)]
        notices = " ".join(result.notices)
        if carried:
            for pack_id in carried:
                self.assertIn(pack_id, notices)
            self.assertIn("receipt", notices.lower())
        else:
            self.assertNotIn("receipt", notices.lower())
        self.assertFalse(result.receipts_required)

    # ------------------------------------------------------------ accepted-only and HOLD
    def test_a_pack_whose_digest_is_not_the_accepted_digest_is_a_gap_never_injected(self):
        for pack in self.v1.packs.values():
            if pack.corpus_digest != self.v1.accepted_digest:
                result = self.lookup(self.v1, "mustard-oil-tin")
                self.assertNotIn(pack.pack_id, result.injected_pack_ids)
        # and the accepted ones really do carry the accepted fingerprint
        result = self.lookup(self.v1, "mustard-oil-tin")
        for pack_id in result.injected_pack_ids:
            self.assertEqual(self.v1.packs[pack_id].corpus_digest, self.v1.accepted_digest)

    def test_no_hold_lane_id_reaches_any_prefix(self):
        hold = _hold_ids()
        self.assertTrue(hold, "the HOLD lane listing came back empty; the scan proves nothing")
        id_token = re.compile(r"\b(?:sk|scs)_[a-z0-9_]+\b")
        for name in ("mustard-oil-tin", "lipstick-packshot", "showroom-photo-edit"):
            payload = self.lookup(self.v1, name).payload
            found = sorted(t for t in set(id_token.findall(payload)) if t in hold)
            self.assertEqual(found, [])
            self.assertNotIn("canon/candidates/", payload)

    def test_the_token_bound_is_respected(self):
        for name in ("mustard-oil-tin", "lipstick-packshot", "showroom-photo-edit"):
            result = self.lookup(self.v1, name)
            self.assertLessEqual(result.tokens, self.v1.triggers["per_request_max_tokens"])
            self.assertEqual(result.tokens, math.ceil(len(result.payload) / 4))

    # ------------------------------------------------------------ v0 untouched
    def test_the_v0_path_is_byte_for_byte_what_it_was(self):
        result = self.lookup(self.v0, "mustard-oil-tin")
        self.assertEqual(result.injection_version, "v0")
        self.assertTrue(result.receipts_required)
        self.assertEqual(result.injected_context_sha256, V0_PAYLOAD_SHA256)
        fenced = _FENCE.search(read_text(paths.CANON_INJECTION_CONTRACT)).group(1)
        self.assertTrue(result.payload.startswith(fenced))
        self.assertNotEqual(result.prefix_sha256, self.lookup(self.v1, "mustard-oil-tin").prefix_sha256)

    def test_an_unknown_injection_version_is_refused_by_name(self):
        from runtime.errors import Refusal

        with self.assertRaises(Refusal) as caught:
            CanonCorpus(injection_version="v9")
        self.assertIn("v9", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
