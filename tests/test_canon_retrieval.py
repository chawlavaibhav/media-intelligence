"""SALVAGE-OFFLINE remnant of the CANON-015 retrieval test module.

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

SUPERSESSION NOTE (per canon/packs/COMPILED-PACK-CONTRACT-v0.1.md §9, in the pattern of
tests/test_live24_coverage.py): the CANON-015 per-request retrieval runtime
(canon/retrieval/plan.py, rank.py, tools.py — commit 8115400) is disposed SUPERSEDE by the
compiled-pack layer and its modules are not present in this tree, so the per-request runtime
tests retired with them. The contract's disposition row for this file is SALVAGE-OFFLINE:
exactly one check survives — the capability-routing boundary test
(`test_catalogue_never_asks_a_capability_routing_question`), run verbatim against the pack
question skeletons that replaced the retrieval question catalogue. Canon says what must be
understood, never which model or provider to use.

Run: python3 -m unittest tests.test_canon_retrieval
"""
import unittest
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKS = (
    REPO_ROOT / "canon/compilation/PACK-product_appearance-v0.yaml",
    REPO_ROOT / "canon/compilation/PACK-composition_and_attention-v0.yaml",
)


class CapabilityRoutingBoundaryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packs = [yaml.safe_load(p.read_text()) for p in PACKS]

    def test_catalogue_never_asks_a_capability_routing_question(self):
        """Canon says what must be understood, never which model or provider to use."""
        # Capability-routing vocabulary: who makes it, on what, at what service cost.
        # "price"/"pricing" are NOT here — a price printed in a poster is a legibility
        # question and the festive-poster brief turns on it. What must never appear is a
        # model, a provider, or a service-level property of one.
        forbidden = ("model", "provider", "api", "gpt", "gemini", "veo", "imagen",
                     "midjourney", "latency", "quota", "endpoint", "checkpoint",
                     "diffusion", "throughput", "inference", "gpu")
        for pack in self.packs:
            for decision in pack["decisions"]:
                haystack = " ".join((decision["decision_id"], decision["question"],
                                     decision["default"], decision["check"])).lower()
                for word in forbidden:
                    with self.subTest(decision=decision["decision_id"], word=word):
                        self.assertNotIn(f" {word} ", f" {haystack} ")

    def test_every_decision_carries_a_question_skeleton(self):
        """The salvaged boundary check is only meaningful if the skeletons exist: every
        compiled decision must carry a non-empty question, default and check."""
        for pack in self.packs:
            self.assertTrue(pack["decisions"], pack["pack_id"])
            for decision in pack["decisions"]:
                for field in ("question", "default", "check"):
                    self.assertTrue(str(decision[field]).strip(),
                                    f"{decision['decision_id']}.{field}")


if __name__ == "__main__":
    unittest.main()
