"""Deterministic tests for CANON-015 Canon retrieval.

Two kinds of test live here and they are deliberately not mixed up.

Tests over the REAL accepted corpus assert the properties that must hold for the corpus we
actually ship: an accepted-only surface, hard budgets, preserved epistemics, reproducible
output. They are anchored to the committed corpus fingerprint, so if accepted Canon
changes, the anchor test fails first and says so rather than a dozen downstream tests
failing mysteriously.

Tests over a SYNTHETIC corpus assert the failure behaviour — an unresolvable status, a
missing index, a source present on disk but absent from the index, one source trying to
saturate a bundle. Those states must not be created in the real corpus to be tested.

Nothing here calls a model or a provider, and nothing writes inside `canon/`.
"""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

from canon.retrieval import budgets as budgets_mod
from canon.retrieval import questions as questions_mod
from canon.retrieval.budgets import Budgets, BudgetError, COMPACT_BUDGETS, DEFAULT_BUDGETS
from canon.retrieval.bundle import build_bundle, model_payload
from canon.retrieval.corpus import (ACCEPTED, HOLD, AcceptedCanon, CanonStatusError,
                                    CorpusError, KIND_BINDING, KIND_KNOWLEDGE,
                                    KIND_ONTOLOGY_TERM)
from canon.retrieval.plan import PlanError, build_plan
from canon.retrieval.rank import PRODUCTION_BINDING_TARGETS, TypedIndex
from canon.retrieval.tools import CanonContextTools

REPO_ROOT = Path(__file__).resolve().parents[1]

# The committed accepted-Canon fingerprint. Every "same corpus -> same bundle" claim in
# this package is relative to these exact bytes.
ACCEPTED_FINGERPRINT = "a9cee40fb433adc08ac98ba7c87e1ead790f60aa71d184327cc5e97f59ed7eb9"

WATCH_BRIEF = (
    "Create one premium 4:5 e-commerce hero image for a mechanical watch: 38 mm brushed "
    "stainless-steel case, deep blue sunburst dial, domed sapphire crystal, dark brown "
    "leather strap. Communicate craftsmanship, dial detail and material quality. Product "
    "geometry must not be altered. Avoid generic floating-product CGI.")
CAFE_BRIEF = (
    "Create a short cinematic scene between two people at a cafe table. One has "
    "discovered the other concealed something. The dialogue is tense but restrained. The "
    "viewer must always understand where each person is. Use exactly six shots. Avoid "
    "elaborate camera movement. About 40 seconds, 16:9.")
FESTIVE_BRIEF = (
    "One premium promotional poster for our media-generation API for Indian businesses "
    "during the festive season. Image generation at Rs 9 and video generation at Rs 99. "
    "Typography and information hierarchy must do most of the work. It must not look like "
    "a discount retail flyer. 4:5 poster.")

_CORPUS = None
_INDEX = None


def real_corpus():
    """Load the accepted corpus once for the whole module: 24 sources, 120 files."""
    global _CORPUS, _INDEX
    if _CORPUS is None:
        _CORPUS = AcceptedCanon(REPO_ROOT)
        _INDEX = TypedIndex(_CORPUS)
    return _CORPUS, _INDEX


# ── synthetic corpus ────────────────────────────────────────────────────────────────
def _knowledge_item(sk_id, source_id, claim, label):
    return {
        "sk_id": sk_id, "source_id": source_id,
        "source_terms": [f"verbatim words for {label}"],
        "concept_label": label, "label_origin": "extractor_assigned",
        "claim": claim, "claim_type": "explicit_source_claim",
        "interpretation_basis": None,
        "mechanism": {"stated_by_source": False, "text": None},
        "scope": {"domain_discussed_by_source": ["test_domain"],
                  "conditions": "any test composition"},
        "caveats": [{"text": "the source hedges this", "origin": "source_stated"},
                    {"text": "we noticed the sample was small", "origin": "extractor_observed"}],
        "source_stated_problems": ["the eye gets stuck"],
        "source_stated_remedies": ["move the emphasis"],
        "examples": {"positive": []},
        "evidence": {"characteristics": ["explicitly_stated", "argued"],
                     "source_uncertainty": "source_hedges",
                     "extraction_uncertainty": "figure_not_inspected"},
        "provenance": {"chapter": "I", "section": None, "page_start": 1, "page_end": 2,
                       "locator": "chapter I", "figure_refs": [],
                       "source_support": "text", "inspected": {"text": True, "figures": []}},
    }


def write_synthetic_corpus(root, *, sources, unknown_status_source=None,
                           orphan_directory=None):
    """Write a minimal but structurally real corpus. Returns the repo root."""
    root = Path(root)
    index_sources = []
    for spec in sources:
        location = (f"canon/knowledge/current/{spec['dir']}" if spec["status"] == "accepted"
                    else f"canon/candidates/canon-014/{spec['dir']}")
        directory = root / location
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "source-knowledge.yaml").write_text(yaml.safe_dump(
            {"source_id": spec["source_id"],
             "source_knowledge": [_knowledge_item(f"sk_{spec['dir']}_{i:04d}",
                                                  spec["source_id"], claim, label)
                                  for i, (claim, label) in enumerate(spec["items"])]},
            sort_keys=False), encoding="utf-8")
        index_sources.append({
            "source_dir": spec["dir"], "epistemic_status": spec["status"],
            "location": location, "source_id": spec["source_id"],
            "source_knowledge": len(spec["items"]), "concept_systems": 0,
            "operational_bindings": 0, "ontology_terms": 0, "ontology_concepts": 0,
            "ontology_relationships": 0,
            "visual_evidence": {"ledger": False}, "audit": None,
            "candidate_blocker": None, "qa": {"bank": None, "qa_items": 0},
        })
    if unknown_status_source:
        location = f"canon/knowledge/current/{unknown_status_source}"
        (root / location).mkdir(parents=True, exist_ok=True)
        (root / location / "source-knowledge.yaml").write_text(
            yaml.safe_dump({"source_id": unknown_status_source, "source_knowledge": [
                _knowledge_item("sk_unknown_0001", unknown_status_source,
                                "a claim about composition and hierarchy", "unknown_thing")]},
                sort_keys=False), encoding="utf-8")
        index_sources.append({
            "source_dir": unknown_status_source, "epistemic_status": "provisional",
            "location": location, "source_id": unknown_status_source})
    if orphan_directory:
        orphan = root / "canon/knowledge/current" / orphan_directory
        orphan.mkdir(parents=True, exist_ok=True)
        (orphan / "source-knowledge.yaml").write_text(
            yaml.safe_dump({"source_id": orphan_directory, "source_knowledge": [
                _knowledge_item("sk_orphan_0001", orphan_directory,
                                "a composition claim nobody admitted", "orphan_thing")]},
                sort_keys=False), encoding="utf-8")

    index_path = root / "canon/knowledge/CANON-CORPUS-INDEX.yaml"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(yaml.safe_dump(
        {"index_version": "test", "sources": index_sources}, sort_keys=False),
        encoding="utf-8")
    return root


COMPOSITION_CLAIMS = [
    ("The centre of the frame is the strongest point of attraction and holds the eye, so "
     "a composition places its focal point deliberately rather than by default.",
     "centre_as_strongest_attractor"),
    ("Visual hierarchy decides what the viewer notices first; scale and contrast are the "
     "instruments that set it, and emphasis without contrast is not emphasis.",
     "hierarchy_is_set_by_scale_and_contrast"),
    ("Negative space around a subject is part of the composition and controls how much "
     "attention the subject commands within the frame.",
     "negative_space_controls_attention"),
    ("Balance in a frame is the distribution of visual weight; an unbalanced frame moves "
     "the eye toward the heavier side whether or not that was intended.",
     "balance_is_distribution_of_weight"),
]


class BudgetTests(unittest.TestCase):
    def test_every_field_must_be_a_positive_integer(self):
        for field in ("max_items", "max_total_chars", "max_sources", "max_questions"):
            with self.subTest(field=field):
                with self.assertRaises(BudgetError):
                    Budgets(**{field: None})
                with self.assertRaises(BudgetError):
                    Budgets(**{field: 0})
                with self.assertRaises(BudgetError):
                    Budgets(**{field: -1})

    def test_booleans_are_not_integers_here(self):
        with self.assertRaises(BudgetError):
            Budgets(max_items=True)

    def test_incoherent_budgets_are_refused(self):
        with self.assertRaises(BudgetError):
            Budgets(max_items=3, max_items_per_question=4)
        with self.assertRaises(BudgetError):
            Budgets(max_total_chars=1_000, max_chars_per_item=2_000)

    def test_no_preset_is_unbounded(self):
        for name, preset in budgets_mod.PRESETS.items():
            with self.subTest(preset=name):
                for field, value in preset.as_dict().items():
                    self.assertIsInstance(value, int, field)
                    self.assertGreaterEqual(value, 1, field)


class CorpusSurfaceTests(unittest.TestCase):
    def test_corpus_fingerprint_matches_the_committed_index(self):
        corpus, _ = real_corpus()
        index = yaml.safe_load(
            (REPO_ROOT / "canon/knowledge/CANON-CORPUS-INDEX.yaml").read_text())
        committed = index["fingerprints"]["accepted_canon"]
        self.assertEqual(corpus.fingerprint["combined_digest"], committed["combined_digest"])
        self.assertEqual(corpus.fingerprint["combined_digest"], ACCEPTED_FINGERPRINT)
        self.assertEqual(corpus.fingerprint["file_count"], committed["file_count"])

    def test_default_surface_is_accepted_only(self):
        corpus, _ = real_corpus()
        self.assertTrue(corpus.production_default)
        self.assertIsNone(corpus.diagnostic_reason)
        self.assertEqual(len(corpus.sources), 24)
        for item in corpus.items:
            self.assertEqual(item.source_status, ACCEPTED, item.item_id)

    def test_no_hold_source_directory_is_reachable(self):
        corpus, _ = real_corpus()
        hold_dirs = {s["source_dir"] for s in yaml.safe_load(
            (REPO_ROOT / "canon/knowledge/CANON-CORPUS-INDEX.yaml").read_text())["sources"]
            if s["epistemic_status"] == "hold"}
        self.assertTrue(hold_dirs)
        self.assertFalse(hold_dirs & set(corpus.sources))

    def test_qa_is_not_in_the_production_surface(self):
        corpus, _ = real_corpus()
        self.assertNotIn("qa", corpus.counts_by_kind())

    def test_hold_and_qa_require_a_stated_diagnostic_reason(self):
        with self.assertRaises(CanonStatusError):
            AcceptedCanon(REPO_ROOT, include_hold=True)
        with self.assertRaises(CanonStatusError):
            AcceptedCanon(REPO_ROOT, include_qa=True, diagnostic_reason="   ")

    def test_lineage_groups_follow_the_audit_gate(self):
        corpus, _ = real_corpus()
        shot = corpus.sources["grammar-of-the-shot-ch4"]["source_id"]
        edit = corpus.sources["grammar-of-the-edit-ch3-5"]["source_id"]
        murch = corpus.sources["murch-blink-p1-25"]["source_id"]
        ondaatje = corpus.sources["ondaatje-conversations-ch3"]["source_id"]
        albers = corpus.sources["albers-interaction-of-color"]["source_id"]
        self.assertEqual(corpus.lineage_group_of(shot), corpus.lineage_group_of(edit))
        self.assertEqual(corpus.lineage_group_of(murch), corpus.lineage_group_of(ondaatje))
        self.assertNotEqual(corpus.lineage_group_of(albers), corpus.lineage_group_of(shot))


class FailClosedTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def test_missing_index_raises(self):
        with self.assertRaises(CorpusError):
            AcceptedCanon(self.tmp)

    def test_unresolvable_status_is_excluded_and_reported(self):
        write_synthetic_corpus(
            self.tmp,
            sources=[{"dir": "good", "source_id": "good_src", "status": "accepted",
                      "items": COMPOSITION_CLAIMS}],
            unknown_status_source="murky")
        corpus = AcceptedCanon(self.tmp)
        self.assertNotIn("murky", corpus.sources)
        reasons = {e["source_dir"]: e["reason"] for e in corpus.excluded_sources}
        self.assertEqual(reasons["murky"], "status_not_established")
        self.assertTrue(all(item.source_dir == "good" for item in corpus.items))

    def test_directory_on_disk_but_absent_from_the_index_is_excluded(self):
        write_synthetic_corpus(
            self.tmp,
            sources=[{"dir": "good", "source_id": "good_src", "status": "accepted",
                      "items": COMPOSITION_CLAIMS}],
            orphan_directory="never_admitted")
        corpus = AcceptedCanon(self.tmp)
        self.assertNotIn("never_admitted", corpus.sources)
        reasons = {e["source_dir"]: e["reason"] for e in corpus.excluded_sources}
        self.assertEqual(reasons["never_admitted"],
                         "present_on_disk_but_not_in_corpus_index")

    def test_an_item_cannot_be_built_without_a_real_status(self):
        from canon.retrieval.corpus import CanonItem
        with self.assertRaises(CanonStatusError):
            CanonItem(source_dir="d", source_id="s", source_title=None,
                      source_status="PROBABLY_FINE", kind=KIND_KNOWLEDGE, item_id="x",
                      artifact="source-knowledge.yaml", lineage_group="s",
                      index_text="text", payload={})


class PlanTests(unittest.TestCase):
    def test_media_detection_uses_word_boundaries(self):
        # "dialogue" contains "dial"; an earlier substring rule fired the lighting
        # question on it. This is the regression guard.
        plan = build_plan(CAFE_BRIEF)
        self.assertEqual(plan.media, "video")
        self.assertNotIn("lighting_material", [q.qid for q in plan.questions])

    def test_plan_never_exceeds_the_question_budget(self):
        budgets = Budgets(max_questions=2, max_items_per_question=2, max_items=4)
        plan = build_plan(FESTIVE_BRIEF, budgets=budgets)
        self.assertLessEqual(len(plan.questions), 2)

    def test_base_questions_survive_a_brief_that_never_names_them(self):
        plan = build_plan(WATCH_BRIEF)
        self.assertIn("composition_hierarchy", [q.qid for q in plan.questions])
        self.assertIn("failure_prevention", [q.qid for q in plan.questions])

    def test_unknown_question_id_is_refused(self):
        with self.assertRaises(PlanError):
            build_plan(WATCH_BRIEF, question_ids=["not_a_question"])

    def test_empty_request_without_explicit_questions_is_refused(self):
        with self.assertRaises(PlanError):
            build_plan("   ")

    def test_catalogue_never_asks_a_capability_routing_question(self):
        """Canon says what must be understood, never which model or provider to use."""
        # Capability-routing vocabulary: who makes it, on what, at what service cost.
        # "price"/"pricing" are NOT here — a price printed in a poster is a legibility
        # question and the festive-poster brief turns on it. What must never appear is a
        # model, a provider, or a service-level property of one.
        forbidden = ("model", "provider", "api", "gpt", "gemini", "veo", "imagen",
                     "midjourney", "latency", "quota", "endpoint", "checkpoint",
                     "diffusion", "throughput", "inference", "gpu")
        for question in questions_mod.CATALOGUE:
            haystack = " ".join((question.qid, question.plain_english,
                                 *question.cue_terms, *question.expansion_terms)).lower()
            for word in forbidden:
                with self.subTest(question=question.qid, word=word):
                    self.assertNotIn(f" {word} ", f" {haystack} ")


class BundleBudgetTests(unittest.TestCase):
    def setUp(self):
        self.corpus, self.index = real_corpus()

    def _bundle(self, brief=WATCH_BRIEF, budgets=DEFAULT_BUDGETS):
        return build_bundle(brief, self.corpus, budgets=budgets, typed_index=self.index)

    def test_every_hard_budget_is_respected(self):
        for name, budgets in (("default", DEFAULT_BUDGETS), ("compact", COMPACT_BUDGETS)):
            for brief in (WATCH_BRIEF, CAFE_BRIEF, FESTIVE_BRIEF):
                with self.subTest(preset=name, brief=brief[:20]):
                    bundle = self._bundle(brief, budgets)
                    spread = bundle["spread"]
                    self.assertLessEqual(spread["items"], budgets.max_items)
                    self.assertLessEqual(spread["distinct_sources"], budgets.max_sources)
                    self.assertLessEqual(spread["max_items_from_one_source"],
                                         budgets.max_items_per_source)
                    self.assertLessEqual(spread["max_items_from_one_lineage_group"],
                                         budgets.max_items_per_lineage_group)
                    self.assertLessEqual(len(bundle["plan"]["questions"]),
                                         budgets.max_questions)
                    self.assertLessEqual(bundle["size"]["total_chars"],
                                         budgets.max_total_chars)
                    self.assertTrue(bundle["size"]["within_budget"])

    def test_measured_size_is_the_model_facing_payload(self):
        bundle = self._bundle()
        measured = len(json.dumps(model_payload(bundle), ensure_ascii=False, sort_keys=True))
        self.assertEqual(measured, bundle["size"]["total_chars"])
        self.assertNotIn("_diagnostics", model_payload(bundle))

    def test_no_item_exceeds_its_own_character_allowance(self):
        bundle = self._bundle()
        for item in bundle["items"]:
            with self.subTest(item=item["item_id"]):
                self.assertLessEqual(
                    len(json.dumps(item, ensure_ascii=False, sort_keys=True)),
                    DEFAULT_BUDGETS.max_chars_per_item + 400)  # lineage-note headroom

    def test_per_question_cap_holds(self):
        bundle = self._bundle()
        counts = {}
        for item in bundle["items"]:
            counts[item["answers_question"]] = counts.get(item["answers_question"], 0) + 1
        for question, count in counts.items():
            self.assertLessEqual(count, DEFAULT_BUDGETS.max_items_per_question, question)

    def test_a_tiny_budget_still_produces_a_valid_bounded_bundle(self):
        tiny = Budgets(max_items=2, max_total_chars=9_000, max_chars_per_item=2_500,
                       max_sources=2, max_items_per_source=1,
                       max_items_per_lineage_group=1, max_questions=1,
                       max_items_per_question=1, max_candidates_per_question=20)
        bundle = self._bundle(budgets=tiny)
        self.assertLessEqual(bundle["spread"]["items"], 2)
        self.assertLessEqual(bundle["size"]["total_chars"], 9_000)

    def test_a_budget_too_small_for_the_header_fails_loudly(self):
        cramped = Budgets(max_items=1, max_total_chars=1_200, max_chars_per_item=1_000,
                          max_sources=1, max_items_per_source=1,
                          max_items_per_lineage_group=1, max_questions=1,
                          max_items_per_question=1, max_candidates_per_question=5)
        with self.assertRaises(ValueError):
            self._bundle(budgets=cramped)


class BundleContentTests(unittest.TestCase):
    def setUp(self):
        self.corpus, self.index = real_corpus()
        self.bundle = build_bundle(WATCH_BRIEF, self.corpus, typed_index=self.index)

    def test_every_item_states_an_accepted_status(self):
        self.assertTrue(self.bundle["items"])
        for item in self.bundle["items"]:
            self.assertEqual(item["epistemics"]["source_status"], ACCEPTED)
            self.assertEqual(item["source"]["source_status"], ACCEPTED)
        self.assertTrue(self.bundle["corpus"]["production_default"])
        self.assertEqual(self.bundle["corpus"]["surface"], "accepted_only")

    def test_knowledge_items_keep_claim_type_evidence_and_both_uncertainties(self):
        seen = 0
        for brief in (WATCH_BRIEF, CAFE_BRIEF, FESTIVE_BRIEF):
            bundle = build_bundle(brief, self.corpus, typed_index=self.index)
            for item in bundle["items"]:
                if item["kind"] != KIND_KNOWLEDGE:
                    continue
                seen += 1
                epistemics = item["epistemics"]
                self.assertIn("claim_type", epistemics, item["item_id"])
                self.assertTrue(epistemics.get("evidence_characteristics"), item["item_id"])
                self.assertIn("source_uncertainty", epistemics, item["item_id"])
                self.assertIn("extraction_uncertainty", epistemics, item["item_id"])
        self.assertGreater(seen, 0)

    def test_caveats_keep_the_origin_that_says_whose_doubt_it_is(self):
        found = False
        for brief in (WATCH_BRIEF, CAFE_BRIEF, FESTIVE_BRIEF):
            bundle = build_bundle(brief, self.corpus, typed_index=self.index)
            for item in bundle["items"]:
                for caveat in item["epistemics"].get("caveats", []):
                    found = True
                    self.assertIn(caveat.get("origin"),
                                  ("source_stated", "extractor_observed"), caveat)
        self.assertTrue(found, "no caveats appeared in any bundle; the guard is untested")

    def test_bindings_always_disclose_that_they_are_unreviewed_proposals(self):
        found = False
        for brief in (WATCH_BRIEF, CAFE_BRIEF, FESTIVE_BRIEF):
            bundle = build_bundle(brief, self.corpus, typed_index=self.index)
            for item in bundle["items"]:
                if item["kind"] != KIND_BINDING:
                    continue
                found = True
                self.assertIn(item["epistemics"]["binding_status"],
                              ("proposed", "production_candidate", "accepted"))
                self.assertIn("evidence_basis", item["epistemics"])
                self.assertIn("review_note", item["epistemics"])
        self.assertTrue(found, "no bindings appeared in any bundle; the guard is untested")

    def test_governance_and_benchmark_bindings_stay_out_of_a_production_bundle(self):
        self.assertEqual(self.index.out_of_scope_bindings, 63)
        for brief in (WATCH_BRIEF, CAFE_BRIEF, FESTIVE_BRIEF):
            bundle = build_bundle(brief, self.corpus, typed_index=self.index)
            for item in bundle["items"]:
                if item["kind"] != KIND_BINDING:
                    continue
                self.assertIn(item["content"]["what_it_binds_to"]["target_type"],
                              PRODUCTION_BINDING_TARGETS)

    def test_every_item_can_be_traced_back_to_its_source(self):
        for item in self.bundle["items"]:
            self.assertTrue(item["source"]["source_dir"])
            self.assertTrue(item["item_id"])
            self.assertTrue(item["kind"])
            self.assertEqual(item["detail_ref"]["item_id"], item["item_id"])

    def test_relevance_is_labelled_as_relevance_not_as_quality(self):
        for item in self.bundle["items"]:
            self.assertIn("says nothing about how good", item["relevance"]["basis"])

    def test_items_are_delivered_whole_or_marked_incomplete(self):
        for item in self.bundle["items"]:
            if item["delivered_complete"]:
                self.assertNotIn("trimmed_fields", item)
            else:
                self.assertTrue(item["trimmed_fields"])

    def test_trimming_never_touches_epistemics(self):
        """Force trimming with a small per-item allowance and check what survives."""
        # Search downward for an allowance that actually forces a trim rather than an
        # outright rejection, so the guard is exercised rather than vacuously passed.
        trimmed, bundle = [], None
        for allowance in (2_600, 2_400, 2_200, 2_000, 1_800):
            squeezed = Budgets(max_items=8, max_total_chars=26_000,
                               max_chars_per_item=allowance, max_sources=8,
                               max_items_per_source=2, max_items_per_lineage_group=2,
                               max_questions=4, max_items_per_question=2,
                               max_candidates_per_question=60)
            bundle = build_bundle(WATCH_BRIEF, self.corpus, budgets=squeezed,
                                  typed_index=self.index)
            trimmed = [i for i in bundle["items"] if not i["delivered_complete"]]
            if trimmed:
                break
        self.assertTrue(trimmed, "no allowance in the sweep forced a trim")
        for item in trimmed:
            if item["kind"] != KIND_KNOWLEDGE:
                continue
            self.assertIn("source_uncertainty", item["epistemics"])
            self.assertIn("extraction_uncertainty", item["epistemics"])
            self.assertTrue(item["epistemics"].get("evidence_characteristics"))

    def test_coverage_reports_which_questions_got_nothing(self):
        coverage = self.bundle["coverage"]
        planned = set(coverage["questions_planned"])
        answered = set(coverage["questions_with_at_least_one_item"])
        self.assertEqual(planned - answered, set(coverage["questions_with_no_item"]))
        self.assertTrue(answered)


class DiversityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def test_one_source_cannot_saturate_the_bundle(self):
        """A corpus of one dominant source plus one small one, with a per-source cap of 1."""
        write_synthetic_corpus(self.tmp, sources=[
            {"dir": "dominant", "source_id": "dominant_src", "status": "accepted",
             "items": COMPOSITION_CLAIMS},
            {"dir": "quiet", "source_id": "quiet_src", "status": "accepted",
             "items": COMPOSITION_CLAIMS[:2]},
        ])
        corpus = AcceptedCanon(self.tmp)
        budgets = Budgets(max_items=6, max_total_chars=30_000, max_chars_per_item=4_200,
                          max_sources=4, max_items_per_source=1,
                          max_items_per_lineage_group=1, max_questions=2,
                          max_items_per_question=3, max_candidates_per_question=20)
        bundle = build_bundle("a poster about composition and hierarchy", corpus,
                              budgets=budgets)
        self.assertLessEqual(bundle["spread"]["max_items_from_one_source"], 1)
        self.assertLessEqual(bundle["spread"]["items"], 2)

    def test_near_duplicates_are_dropped(self):
        identical = ("An identical claim repeated verbatim in two different books about "
                     "visual hierarchy, scale, contrast, emphasis and attention in a frame.")
        write_synthetic_corpus(self.tmp, sources=[
            {"dir": "first", "source_id": "first_src", "status": "accepted",
             "items": [(identical, "same_claim")]},
            {"dir": "second", "source_id": "second_src", "status": "accepted",
             "items": [(identical, "same_claim")]},
        ])
        corpus = AcceptedCanon(self.tmp)
        bundle = build_bundle("visual hierarchy scale contrast emphasis attention", corpus)
        self.assertEqual(bundle["spread"]["items"], 1)
        reasons = {r["reason"] for r in bundle["_diagnostics"]["selection_rejections"]}
        self.assertIn("near_duplicate_of_selected", reasons)

    def test_dependent_sources_share_one_lineage_budget(self):
        corpus, index = real_corpus()
        budgets = Budgets(max_items=8, max_total_chars=30_000, max_chars_per_item=4_200,
                          max_sources=8, max_items_per_source=4,
                          max_items_per_lineage_group=2, max_questions=2,
                          max_items_per_question=4, max_candidates_per_question=60)
        bundle = build_bundle(CAFE_BRIEF, corpus, budgets=budgets, typed_index=index)
        self.assertLessEqual(bundle["spread"]["max_items_from_one_lineage_group"], 2)

    def test_a_definition_of_an_already_selected_claim_is_not_repeated(self):
        corpus, index = real_corpus()
        bundle = build_bundle(CAFE_BRIEF, corpus, typed_index=index)
        selected_sk = {i["item_id"] for i in bundle["items"] if i["kind"] == KIND_KNOWLEDGE}
        for item in bundle["items"]:
            if item["kind"] != KIND_ONTOLOGY_TERM:
                continue
            arising = set(item["content"].get("arising_from") or [])
            self.assertFalse(arising & selected_sk, item["item_id"])

    def test_dependent_sources_selected_together_carry_a_lineage_warning(self):
        corpus, index = real_corpus()
        budgets = Budgets(max_items=12, max_total_chars=30_000, max_chars_per_item=4_200,
                          max_sources=8, max_items_per_source=2,
                          max_items_per_lineage_group=4, max_questions=2,
                          max_items_per_question=5, max_candidates_per_question=60)
        bundle = build_bundle(CAFE_BRIEF, corpus, budgets=budgets, typed_index=index)
        groups = {}
        for item in bundle["items"]:
            source_id = corpus.sources[item["source"]["source_dir"]]["source_id"]
            groups.setdefault(corpus.lineage_group_of(source_id), set()).add(
                item["source"]["source_dir"])
        shared = {g for g, members in groups.items() if len(members) > 1}
        if not shared:
            self.skipTest("no dependent pair co-selected for this brief")
        for item in bundle["items"]:
            source_id = corpus.sources[item["source"]["source_dir"]]["source_id"]
            if corpus.lineage_group_of(source_id) in shared:
                self.assertIn("Not an independent origin",
                              item["source"].get("lineage_note", ""))


class DeterminismTests(unittest.TestCase):
    def test_same_request_and_config_give_a_byte_identical_bundle(self):
        corpus, index = real_corpus()
        first = build_bundle(WATCH_BRIEF, corpus, typed_index=index)
        second = build_bundle(WATCH_BRIEF, corpus, typed_index=index)
        self.assertEqual(json.dumps(model_payload(first), sort_keys=True),
                         json.dumps(model_payload(second), sort_keys=True))

    def test_a_freshly_loaded_corpus_gives_the_same_bundle(self):
        corpus, index = real_corpus()
        first = build_bundle(CAFE_BRIEF, corpus, typed_index=index)
        fresh = AcceptedCanon(REPO_ROOT)
        second = build_bundle(CAFE_BRIEF, fresh, typed_index=TypedIndex(fresh))
        self.assertEqual(json.dumps(model_payload(first), sort_keys=True),
                         json.dumps(model_payload(second), sort_keys=True))

    def test_item_order_is_stable_and_numbered_from_one(self):
        corpus, index = real_corpus()
        bundle = build_bundle(WATCH_BRIEF, corpus, typed_index=index)
        self.assertEqual([i["n"] for i in bundle["items"]],
                         list(range(1, len(bundle["items"]) + 1)))

    def test_ranking_ties_break_deterministically(self):
        corpus, index = real_corpus()
        ranked = index.indexes[KIND_KNOWLEDGE].score(["composition", "hierarchy"])
        keys = [(-score, item.source_dir, item.item_id) for score, _, item in ranked]
        self.assertEqual(keys, sorted(keys))


class ToolSurfaceTests(unittest.TestCase):
    def setUp(self):
        corpus, index = real_corpus()
        self.tools = CanonContextTools(corpus=corpus)
        self.tools.index = index

    def test_canon_context_returns_no_diagnostics(self):
        payload = self.tools.canon_context(WATCH_BRIEF)
        self.assertNotIn("_diagnostics", payload)
        self.assertTrue(payload["items"])

    def test_size_preset_is_honoured_and_validated(self):
        compact = self.tools.canon_context(WATCH_BRIEF, size="compact")
        self.assertLessEqual(compact["size"]["total_chars"], COMPACT_BUDGETS.max_total_chars)
        with self.assertRaises(ValueError):
            self.tools.canon_context(WATCH_BRIEF, size="unbounded")

    def test_declared_needs_are_accepted_without_widening_the_budget(self):
        payload = self.tools.canon_context(
            WATCH_BRIEF,
            knowledge_needs=["How to light brushed steel without blowing the highlights",
                             "How to keep dial detail legible at product-page size"])
        self.assertLessEqual(payload["spread"]["items"], DEFAULT_BUDGETS.max_items)
        self.assertEqual(payload["plan"]["declared_needs_supplied"], 2)

    def test_canon_detail_finds_an_accepted_item_and_refuses_anything_else(self):
        payload = self.tools.canon_context(WATCH_BRIEF)
        item_id = payload["items"][0]["item_id"]
        detail = self.tools.canon_detail(item_id)
        self.assertEqual(detail["item_id"], item_id)
        self.assertEqual(detail["source"]["source_status"], ACCEPTED)
        missing = self.tools.canon_detail("sk_not_a_real_id")
        self.assertFalse(missing["found"])

    def test_there_is_no_free_text_search_tool(self):
        from canon.retrieval.tools import TOOL_NAMES
        self.assertEqual(sorted(TOOL_NAMES), ["canon_context", "canon_detail"])
        with self.assertRaises(ValueError):
            self.tools.dispatch("canon_search", {"query": "anything"})


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
