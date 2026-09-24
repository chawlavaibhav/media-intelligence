"""P1 v2 phase 6 — the diary writer and the lessons it proposes, applied automatically by kind since amendment 1 §4.
Spec §11 tests 9, 10, 14 and the journey half of 13 (a second job reuses the customer's shelf). USD 0, real ffmpeg.

Kitchen v3 (2026-09-25): the pantry checker is retired, so the equipment sheet reaches the next job through the chef's
tray (memory for awareness), and the rulebook lesson no longer comes from recipe-checker send-backs (retired) — the
diary writer proposes it directly. No test retired."""
import json
import unittest

from product import library, rulebook
from product.tests import fixtures_v2 as fx
from product.tests.support import Env

IMAGE_ORDER = "A calm launch poster for our navy travel backpack; the bag must be the first thing you see; no people."


def image_to_review(e, jid):
    e.drain()
    e.orch.approve(jid, by=e.user["email"], budget_usd="15")
    e.drain()
    assert e.state(jid) == "ready_for_review", e.state(jid)


def queue_snapshot(e):
    return (library.EquipmentSheet(e.store).rows(), rulebook.Rulebook(e.store).version("chef"), e.store.q("SELECT COUNT(*) n FROM recipe_library")[0]["n"])


class DiaryOnEveryOutcome(unittest.TestCase):
    """Spec §11 test 9."""

    def test_accepted_rejected_and_abandoned_jobs_each_produce_lessons_applied_by_kind_without_the_founder(self):
        e = Env()
        try:
            before = queue_snapshot(e)
            accepted = e.submit("image", text=IMAGE_ORDER)
            image_to_review(e, accepted)
            e.orch.accept(accepted, e.user["email"])
            rejected = e.submit("image", text=IMAGE_ORDER)
            image_to_review(e, rejected)
            e.orch.reject(rejected, e.user["email"], "too dark, the bag looks black")
            abandoned = fx.submit_backpack_film(e)
            e.drain()
            self.assertEqual(e.state(abandoned), "awaiting_approval")         # the customer walks away from the recipe
            e.orch.abandon(abandoned, e.user["email"], "we changed our minds about the reel")
            for jid, outcome in ((accepted, "accepted"), (rejected, "rejected"), (abandoned, "abandoned")):
                les = e.store.artifact(jid, "lessons")
                self.assertIsNotNone(les, outcome)
                self.assertEqual(les["outcome"], outcome)
                self.assertEqual(les["written_by"]["worker"], "diary_writer")
                self.assertTrue(all(w["worker"] for w in les["per_worker"]))
                self.assertTrue(e.store.events(jid, ("lessons_proposed",)))
            self.assertIn("too dark", e.store.artifact(rejected, "lessons")["what_the_customer_said"])
            rows = e.orch.lessons.all()
            self.assertTrue(rows)
            self.assertTrue(all(r["status"] in ("applied", "founder_only", "waiting_support") for r in rows), [r["status"] for r in rows])
            self.assertEqual(e.orch.lessons.waiting(), [r for r in e.orch.lessons.waiting() if r["kind"] == "founder_only"])
            recipes = [r for r in rows if r["target"] == "recipe_library"]
            self.assertEqual({r["status"] for r in recipes}, {"applied"})               # every recipe kept with its outcome
            self.assertEqual(queue_snapshot(e)[2], before[2] + len(recipes))
            for r in recipes:                                                           # logged with job, evidence, before/after
                self.assertTrue(json.loads(r["evidence_json"]))
                self.assertIn("after", json.loads(r["applied_json"]))
                self.assertTrue(e.store.events(r["job_id"], ("lesson_applied",)))
            cost = e.store.q("SELECT est_cost_usd FROM llm_calls WHERE worker='diary_writer'")
            self.assertEqual(len(cost), 3)
        finally:
            e.close()


class ApprovedLessonsChangeTheNextJob(unittest.TestCase):
    """Spec §11 test 10 (equipment sheet) and test 14 (rulebook)."""

    def test_a_more_careful_equipment_lesson_reaches_the_next_jobs_chef_and_the_founder_can_undo_it(self):
        e = Env()
        try:
            orig = e.orch.sim.head_cook__ingredient_check

            def taster(b, media, **kw):
                out = orig(b, media, **kw)
                if kw.get("node_id") == "shot_1":
                    out.update(usable=False, notes="the hand passes through the bag wall")
                return out
            e.orch.sim.head_cook__ingredient_check = taster
            first = fx.submit_backpack_film(e)
            fx.film_to_hold(e, first)
            self.assertEqual(e.state(first), "ready_for_review")            # the best take kept, flagged; the customer decides
            cls = next(s for s in e.store.artifact(first, "recipe")["shots"] if s["n"] == 1)["action_class"]
            before = e.orch.equipment.verdict(cls, "FILM-C")["verdict"]
            self.assertNotEqual(before, "cannot")
            self.assertFalse([r for r in e.orch.equipment.rows() if r["action_class"] == cls and r.get("basis") == "lesson"])
            e.orch.abandon(first, e.user["email"], "the moment was the point of the film; closing")
            proposals = [r for r in e.orch.lessons.all(first) if r["target"] == "equipment_sheet"]
            ins = [r for r in proposals if json.loads(r["proposal_json"])["action_class"] == cls]
            self.assertTrue(ins, [json.loads(r["proposal_json"]) for r in proposals])
            self.assertEqual((ins[0]["kind"], ins[0]["status"]), ("careful", "applied"))          # more careful: applied at once
            # the row now says cannot; without counts it is shown as risky until counts prove it (founder 2026-09-24)
            rows = [r["id"] for r in e.orch.equipment.rows() if r["action_class"] == cls and "FILM-C" in r["routes"]
                    and r["declared_verdict"] == "cannot" and r.get("basis") == "lesson"]
            self.assertTrue(rows)
            second = fx.submit_backpack_film(e)
            e.drain()
            tray = {i["id"] for i in e.store.artifact(second, "tray:chef")["items"] if i["section"] == "equipment_sheet"}
            self.assertTrue(set(rows) & tray, (rows, tray))                # the next chef is aware of it
            e.orch.lessons.undo(ins[0]["id"], founder=e.founder(), note="The moment worked on the next brand; restore the old verdict.")
            self.assertEqual(e.orch.equipment.verdict(cls, "FILM-C")["verdict"], before)           # undone: the previous verdict is back
            self.assertFalse([r for r in e.orch.equipment.rows() if r["action_class"] == cls and r["declared_verdict"] == "cannot"
                              and r.get("basis") == "lesson"])
        finally:
            e.close()

    def test_every_call_records_its_card_version_and_a_rulebook_lesson_bumps_it_for_the_next_job_under_watch(self):
        e = Env()
        try:
            orig = e.orch.sim.diary_writer__lessons

            def diary(b, media):
                out = orig(b, media)
                out["per_worker"].append({"worker": "chef", "what_went_right": "", "what_went_wrong": "the customer walked away",
                                          "evidence_refs": ["the customer's words"],
                                          "proposed_change": {"target": "rulebook_card", "why": "the customer closed the job at the recipe",
                                                              "diff": {"worker": "chef", "changes": {"kra_add": "Read the customer's "
                                                                       "must-haves back in the story's first line."}}}})
                return out
            e.orch.sim.diary_writer__lessons = diary
            first = fx.submit_backpack_film(e)
            e.drain()
            self.assertEqual(e.state(first), "awaiting_approval")
            e.orch.abandon(first, e.user["email"], "the chef missed the zip")
            for c in e.store.llm_calls(first):
                self.assertEqual(c["card_version"], int(rulebook.seed_cards()[c["worker"]]["version"]), c["worker"])
            lesson = next(r for r in e.orch.lessons.all(first) if r["target"] == "rulebook_card")
            self.assertEqual((lesson["kind"], lesson["status"]), ("rulebook", "applied"))
            self.assertEqual(json.loads(lesson["watch_json"])["status"], "watching")      # the next 5 jobs are watched
            self.assertEqual(e.orch.rulebook.version("chef"), int(rulebook.seed_cards()["chef"]["version"]) + 1)
            hist = e.orch.rulebook.history("chef")
            self.assertEqual(hist[-1]["source_lesson"], lesson["id"])
            e.orch.sim.diary_writer__lessons = orig
            second = fx.submit_backpack_film(e)
            fx.film_to_hold(e, second)
            chef_calls = [c for c in e.store.llm_calls(second) if c["worker"] == "chef"]
            self.assertTrue(chef_calls)
            self.assertTrue(all(c["card_version"] == int(rulebook.seed_cards()["chef"]["version"]) + 1 for c in chef_calls))
            self.assertEqual(e.store.artifact(second, "recipe")["rulebook_card_version"], int(rulebook.seed_cards()["chef"]["version"]) + 1)
            others = [c for c in e.store.llm_calls(second) if c["worker"] != "chef"]
            self.assertTrue(all(c["card_version"] == int(rulebook.seed_cards()[c["worker"]]["version"]) for c in others))
        finally:
            e.close()


class SecondJobReusesTheShelf(unittest.TestCase):
    """Spec §11 test 13 (journey half) and checklist G4."""

    def test_the_second_film_for_the_same_customer_reuses_their_logo_and_colours_and_another_account_sees_none(self):
        # kitchen v3: there is no separate character picture (the chef's identity anchors carry the person in every
        # prompt), and the chef writes each film's look afresh (the v3 recipe has no reuse_shelf_items), so the second
        # job reuses the logo and colours; the look of the film is on the shelf, shown to the chef
        e = Env()
        try:
            first = fx.submit_backpack_film(e)
            self.assertEqual(fx.film_to_hold(e, first), "ready_for_review")
            e.orch.accept(first, e.user["email"])
            proposed = e.orch.shelf.items(e.acct, status="proposed")
            self.assertTrue({"logo", "brand_colour", "product_photo", "master_plate"} <= {r["kind"] for r in proposed})
            for r in proposed:
                e.orch.shelf.decide(e.acct, r["id"], approve=True, by=e.user["email"])
            approved = {r["kind"] for r in e.orch.shelf.approved(e.acct)}
            self.assertIn("master_plate", approved)                         # approved once, after the first job
            # second job: no logo, no colours supplied
            ups = [u for u in fx.photo_uploads() if u["role"] != "logo"]
            second = e.svc.submit(e.user, title="second reel", media="video", text=fx.BACKPACK_FILM_ORDER, formats=["9:16"], duration_s=30,
                                  exact_strings=fx.BACKPACK_EXACT, product=fx.BACKPACK_PRODUCT, brand_colours=[], max_budget_usd="15",
                                  allow_preview_spend=True, uploads=ups, references_note=fx.BACKPACK_NOTE)
            state = fx.film_to_hold(e, second)
            self.assertEqual(state, "ready_for_review")
            slip = e.store.artifact(second, "order_slip")
            self.assertTrue(slip["prefilled_from_shelf"])
            self.assertEqual(slip["brand_colours"], ["#101820"])
            used = {u["used_for"] for u in e.orch.shelf.uses(second)}
            self.assertTrue({"logo", "brand_colour"} <= used, used)
            self.assertTrue(e.orch.shelf.summary(e.acct)["master_plates"])  # the look is on the shelf for the chef to see
            # another account: nothing of this shelf reaches its waiter or its chef
            other = e.store.create_account("Rival Co", ceiling_usd="20")
            spy = e.customer("spy@rival.test", other)
            third = e.svc.submit(spy, title="rival", media="image", text=IMAGE_ORDER, formats=["1:1"], duration_s=None,
                                 exact_strings=[], product={"name": "Bag"}, brand_colours=[], max_budget_usd="10", allow_preview_spend=True,
                                 uploads=[u for u in fx.photo_uploads()[:1]])
            e.drain()
            self.assertEqual(e.store.artifact(third, "order_slip")["prefilled_from_shelf"], [])
            self.assertEqual(e.orch.shelf.uses(third), [])
            tray = e.store.artifact(third, "tray:chef")
            self.assertFalse([i for i in tray["items"] if i["section"] == "customer_shelf"])
        finally:
            e.close()


if __name__ == "__main__":
    unittest.main()
