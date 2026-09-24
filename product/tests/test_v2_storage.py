"""P1 v2 phase 2 — storage: write-once job files, the customer shelf, the library sections, the lesson queue.
Spec §11 tests 8 and 13 (storage halves; the journey halves are in test_v2_journeys.py). USD 0."""
import json
import unittest
from pathlib import Path

from product import library, rulebook
from product.lessons import LessonQueue
from product.shelf import Shelf, ShelfAccessDenied
from product.store import WriteOnceViolation
from product.tests.support import Env
from runtime.loop.synthetic import make_png


class WriteOnceFiles(unittest.TestCase):
    def test_a_path_that_holds_a_registered_file_can_never_be_registered_again_and_new_paths_are_versioned(self):
        e = Env()
        try:
            jid = e.submit("image")
            out = e.s.media_dir / jid / "out"
            p1 = e.store.new_output_path(out, "ad_1x1", "png")
            p1.write_bytes(make_png(8, 8, seed=1))
            a1 = e.store.add_asset(jid, path=p1, kind="image", source="composed", content_type="image/png", role="deliverable")
            p2 = e.store.new_output_path(out, "ad_1x1", "png")
            self.assertNotEqual(p1, p2)
            self.assertTrue(p2.name.endswith("-v2.png"))
            with self.assertRaises(WriteOnceViolation):
                e.store.add_asset(jid, path=p1, kind="image", source="composed", content_type="image/png", role="deliverable")
            p2.write_bytes(make_png(8, 8, seed=2))
            e.store.add_asset(jid, path=p2, kind="image", source="composed", content_type="image/png", role="deliverable")
            self.assertEqual(e.store.asset(a1)["sha256"], __import__("hashlib").sha256(p1.read_bytes()).hexdigest())
        finally:
            e.close()


class CustomerShelf(unittest.TestCase):
    def setUp(self):
        self.e = Env()
        self.shelf = Shelf(self.e.store, self.e.s.data_dir)
        self.other = self.e.store.create_account("Rival Co", ceiling_usd="10")

    def tearDown(self):
        self.e.close()

    def test_items_are_proposed_approved_once_and_new_versions_keep_the_old(self):
        s, acct = self.shelf, self.e.acct
        logo = self.e.dir / "logo.png"
        logo.write_bytes(make_png(16, 8, seed=5))
        i1 = s.propose(acct, kind="logo", key="primary", data={"filename": "logo.png"}, file=logo, source_job_id="job_x")
        self.assertEqual(s.summary(acct)["logos"], [])                         # not usable until the customer approves
        s.decide(acct, i1, approve=True, by="buyer@acme.test")
        with self.assertRaises(ValueError):
            s.decide(acct, i1, approve=True, by="buyer@acme.test")          # once
        self.assertEqual(s.summary(acct)["logos"][0]["version"], 1)
        logo.write_bytes(make_png(16, 8, seed=6))
        i2 = s.propose(acct, kind="logo", key="primary", data={"filename": "logo-2025.png"}, file=logo)
        s.decide(acct, i2, approve=True, by="buyer@acme.test")
        self.assertEqual(s.summary(acct)["logos"][0]["version"], 2)
        versions = [r["version"] for r in s.items(acct, kind="logo")]
        self.assertEqual(versions, [1, 2])                                   # the old version is kept
        self.assertTrue(Path(s.item(acct, i1)["path"]).exists())

    def test_another_account_can_never_read_or_decide_this_shelf(self):
        s, acct = self.shelf, self.e.acct
        i1 = s.propose(acct, kind="character", key="hands", data={"description": "medium-brown hands, off-white cuffs"})
        s.decide(acct, i1, approve=True, by="buyer@acme.test")
        self.assertEqual(s.items(self.other), [])
        self.assertEqual(s.summary(self.other)["characters"], [])
        with self.assertRaises(ShelfAccessDenied):
            s.item(self.other, i1)
        with self.assertRaises(ShelfAccessDenied):
            s.decide(self.other, i1, approve=False, by="spy@rival.test")
        with self.assertRaises(ShelfAccessDenied):
            s.record_use("job_y", self.other, i1, "character")


class BrandFontsFromTheShelf(unittest.TestCase):
    """Spec §5 sign painter: the brand's type from the customer shelf — and still never a font that lacks a glyph."""

    def test_an_approved_brand_font_is_used_first_but_only_when_it_covers_every_character(self):
        from product import media
        bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if not Path(bold).exists():
            self.skipTest("DejaVu fonts are not installed on this host")
        e = Env()
        try:
            shelf = Shelf(e.store, e.s.data_dir)
            sid = shelf.propose(e.acct, kind="brand_font", key="Brand Sans", data={"name": "Brand Sans"}, file=Path(bold))
            shelf.decide(e.acct, sid, approve=True, by="buyer@acme.test")
            jid = e.submit("image")
            from product.stations.assembly import brand_fonts
            fonts = brand_fonts(e.orch, jid)
            self.assertEqual(len(fonts), 1)
            self.assertIn("brand_font", {u["used_for"] for u in shelf.uses(jid)})
            tok = media.BRAND_FONTS.set(tuple(fonts))
            try:
                self.assertEqual(media.font("regular", "Room for the long way home."), fonts[0])
                self.assertNotEqual(media.font("regular", "₹185 प्रति लीटर"), fonts[0])     # no Devanagari in it: not used
            finally:
                media.BRAND_FONTS.reset(tok)
        finally:
            e.close()


class Library(unittest.TestCase):
    def test_the_equipment_sheet_says_veo_cannot_do_hands_working_zips_with_its_evidence(self):
        e = Env()
        try:
            eq = library.EquipmentSheet(e.store)
            v = eq.verdict("hands_work_mechanism", "FILM-C")
            self.assertEqual((v["verdict"], v["row"]), ("cannot", "EQ-001"))
            row = next(r for r in eq.rows() if r["id"] == "EQ-001")
            self.assertIn("EV-0923-FILM", row["evidence_refs"])
            self.assertEqual(row["sample_count"], 16)
            self.assertEqual(eq.verdict("lift_closed_product", "FILM-C")["verdict"], "risky")
            self.assertEqual(eq.verdict("camera_move_static_product", "FILM-A")["verdict"], "reliable")
            self.assertEqual(eq.verdict("person_performance", "FILM-C")["verdict"], "risky")      # unknown = risky
            self.assertEqual(eq.verdict("hands_work_mechanism", "FILM-A")["verdict"], "cannot")  # a still cannot act
        finally:
            e.close()

    def test_code_holds_an_action_to_the_most_restrictive_class_its_words_match(self):
        self.assertEqual(library.floor_class("The hands pull the paired zippers outward along the curved flap edge", "simple_hand_gesture"),
                         "hands_work_mechanism")
        self.assertEqual(library.floor_class("Both hands lower the folded clothes into the yellow bucket", None),
                         "insert_object_into_container")
        self.assertEqual(library.floor_class("The camera slowly circles the closed bag", "camera_move_static_product"),
                         "camera_move_static_product")
        self.assertEqual(library.floor_class("The hand places the laptop into the bag and lifts it by the handle", None),
                         "multi_step_manipulation")

    def test_the_failure_diary_holds_the_atlas_and_the_23_september_failures_with_labels(self):
        e = Env()
        try:
            rows = library.FailureDiary(e.store).all(None)
            ids = {r["id"] for r in rows}
            self.assertIn("FD-0923-01", ids)
            self.assertGreaterEqual(len([r for r in rows if r["id"].startswith("ATLAS-")]), 225)
            fd = next(r for r in rows if r["id"] == "FD-0923-01")
            self.assertIn("hands_work_mechanism", fd["action_classes"])
        finally:
            e.close()

    def test_cookbook_pages_are_single_decisions_not_whole_packs(self):
        pages, rec = library.cookbook_pages("video", "a film for a backpack", "IN", "en", {"category": "backpack"}, ["x"], True)
        self.assertGreater(len(pages), 40)
        self.assertTrue(all(len(p["text"]) < 6000 for p in pages))
        self.assertTrue(rec["packs_injected"])


class LessonQueueApplies(unittest.TestCase):
    def test_lessons_are_applied_by_kind_and_a_money_lesson_waits_for_the_founder(self):
        """Amendment 1 §4 (storage half; the behaviour tests are in test_v2_amendment1.py)."""
        e = Env()
        try:
            st = e.store
            q = LessonQueue(st, rulebook=rulebook.Rulebook(st), equipment=library.EquipmentSheet(st), recipes=library.RecipeLibrary(st),
                            failures=library.FailureDiary(st), shelf=Shelf(st, e.s.data_dir))
            jid = e.submit("video")
            form = {"outcome": "rejected", "what_the_customer_said": "robotic", "per_worker": [
                {"worker": "pantry_checker", "what_went_right": "-", "what_went_wrong": "lift floated", "evidence_refs": ["att-0012"],
                 "proposed_change": {"target": "equipment_sheet", "why": "floated in both takes",
                                     "diff": {"id": "EQ-003", "action_class": "lift_closed_product", "verdict": "cannot", "sample_count": 4}}},
                {"worker": "chef", "what_went_right": "-", "what_went_wrong": "-", "evidence_refs": [],
                 "proposed_change": {"target": "rulebook_card", "why": "repeat",
                                     "diff": {"worker": "chef", "changes": {"kra_add": "Spend up to the budget cap without asking."}}}},
                {"worker": "waiter", "what_went_right": "ok", "what_went_wrong": "", "evidence_refs": [], "proposed_change": None}]}
            ids = q.enqueue(jid, form)
            self.assertEqual(len(ids), 2)
            eq = library.EquipmentSheet(st)
            self.assertEqual(eq.verdict("lift_closed_product", "FILM-C")["verdict"], "cannot")      # careful: applied at once
            self.assertEqual(json.loads(q.lesson(ids[0])["applied_json"])["version"], 2)
            self.assertEqual(q.lesson(ids[1])["status"], "founder_only")                          # money: never automatic
            self.assertEqual(rulebook.Rulebook(st).version("chef"), int(rulebook.seed_cards()["chef"]["version"]))
            with self.assertRaises(PermissionError):
                q.decide(ids[1], founder="operator:claude", decision="approve", note="looks right to me, applying")
            q.decide(ids[1], founder=e.founder(), decision="reject", note="Budget rules are mine; never in a card.")
            self.assertEqual(rulebook.Rulebook(st).version("chef"), int(rulebook.seed_cards()["chef"]["version"]))
            self.assertEqual(q.waiting(), [])
        finally:
            e.close()


if __name__ == "__main__":
    unittest.main()
