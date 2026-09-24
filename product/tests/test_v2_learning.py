"""P1 v2 phase 6 — the diary writer and the lessons it proposes, applied automatically by kind since amendment 1 §4.
Spec §11 tests 9, 10, 14 and the journey half of 13 (a second job reuses the customer's shelf). USD 0, real ffmpeg."""
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
            self.assertEqual(e.state(abandoned), "awaiting_customer_input")
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

    def test_a_more_careful_equipment_lesson_is_used_by_the_next_jobs_pantry_check_and_the_founder_can_undo_it(self):
        e = Env()
        try:
            orig = e.orch.sim.small_taster__ingredient_check

            def taster(b, media, **kw):
                out = orig(b, media, **kw)
                if kw.get("node_id") in ("frame_2", "shot_2"):
                    out.update(usable=False, notes="the laptop passes through the bag wall")
                return out
            e.orch.sim.small_taster__ingredient_check = taster
            first = fx.submit_backpack_film(e)
            self.assertEqual(e.orch.equipment.verdict("insert_object_into_container", "FILM-C")["verdict"], "risky")
            fx.film_to_hold(e, first)
            self.assertEqual(e.state(first), "ready_for_review")            # the shot became a still; the customer decides
            e.orch.abandon(first, e.user["email"], "the slide was the point of the film; closing")
            proposals = [r for r in e.orch.lessons.all(first) if r["target"] == "equipment_sheet"]
            ins = [r for r in proposals if json.loads(r["proposal_json"])["action_class"] == "insert_object_into_container"]
            self.assertTrue(ins, [json.loads(r["proposal_json"]) for r in proposals])
            self.assertEqual((ins[0]["kind"], ins[0]["status"]), ("careful", "applied"))          # more careful: applied at once
            second = fx.submit_backpack_film(e)
            e.drain()
            f = e.store.artifact(second, "feasibility")
            slide = next(a for a in f["actions_needed"] if "laptop" in a["action"])
            self.assertEqual(slide["best_verdict"], "cannot")
            row = next(v for v in f["route_verdicts"] if v["action_id"] == slide["id"] and v["route"] == "FILM-C")
            self.assertTrue(row["equipment_row"])
            self.assertTrue(any("laptop" in x["for_action"] for x in f["alternatives"]))
            e.orch.lessons.undo(ins[0]["id"], founder=e.founder(), note="The slide worked on the next brand; restore the old verdict.")
            third = fx.submit_backpack_film(e)
            e.drain()
            f = e.store.artifact(third, "feasibility")
            slide = next(a for a in f["actions_needed"] if "laptop" in a["action"])
            self.assertEqual(slide["best_verdict"], "risky")                  # undone: the previous verdict is back
        finally:
            e.close()

    def test_every_call_records_its_card_version_and_a_rulebook_lesson_bumps_it_for_the_next_job_under_watch(self):
        e = Env()
        try:
            first = fx.submit_backpack_film(e)
            e.drain()
            f = e.store.artifact(first, "feasibility")
            e.orch.provide_input(first, by=e.user["email"], accepted_alternatives=[
                {"instead_of": x["for_action"], "use": "the bag shown closed and zipped as a still"} for x in f["alternatives"]])
            e.orch.step(first)
            e.orch.step(first)
            u, f = e.store.artifact(first, "understanding"), e.store.artifact(first, "feasibility")
            e.orch.sim.chef__recipe = lambda b, media: fx.v1_recipe(u, f)
            e.orch.step(first)
            self.assertEqual(e.state(first), "awaiting_approval")            # the system's safe re-plan, for the customer
            e.orch.abandon(first, e.user["email"], "the chef kept planning hands on zips")
            for c in e.store.llm_calls(first):
                self.assertEqual(c["card_version"], 1, c["worker"])
            lesson = next(r for r in e.orch.lessons.all(first) if r["target"] == "rulebook_card")
            self.assertEqual((lesson["kind"], lesson["status"]), ("rulebook", "applied"))
            self.assertEqual(json.loads(lesson["watch_json"])["status"], "watching")      # the next 5 jobs are watched
            self.assertEqual(e.orch.rulebook.version("chef"), 2)
            hist = e.orch.rulebook.history("chef")
            self.assertEqual(hist[-1]["source_lesson"], lesson["id"])
            del e.orch.sim.chef__recipe
            second = fx.submit_backpack_film(e)
            fx.film_to_hold(e, second)
            chef_calls = [c for c in e.store.llm_calls(second) if c["worker"] == "chef"]
            self.assertTrue(chef_calls)
            self.assertTrue(all(c["card_version"] == 2 for c in chef_calls))
            self.assertEqual(e.store.artifact(second, "recipe")["rulebook_card_version"], 2)
            others = [c for c in e.store.llm_calls(second) if c["worker"] != "chef"]
            self.assertTrue(all(c["card_version"] == 1 for c in others))
        finally:
            e.close()


class SecondJobReusesTheShelf(unittest.TestCase):
    """Spec §11 test 13 (journey half) and checklist G4."""

    def test_the_second_film_for_the_same_customer_reuses_their_logo_character_and_master_plate_and_another_account_sees_none(self):
        e = Env()
        try:
            first = fx.submit_backpack_film(e)
            self.assertEqual(fx.film_to_hold(e, first), "ready_for_review")
            e.orch.accept(first, e.user["email"])
            proposed = e.orch.shelf.items(e.acct, status="proposed")
            self.assertTrue({"logo", "brand_colour", "product_photo", "character"} <= {r["kind"] for r in proposed})
            for r in proposed:
                e.orch.shelf.decide(e.acct, r["id"], approve=True, by=e.user["email"])
            approved = {r["kind"] for r in e.orch.shelf.approved(e.acct)}
            self.assertIn("master_plate", approved)                         # approved once, in the first job
            # second job: no logo, no colours supplied
            ups = [u for u in fx.photo_uploads() if u["role"] != "logo"]
            second = e.svc.submit(e.user, title="second reel", media="video", text=fx.BACKPACK_FILM_ORDER, formats=["9:16"], duration_s=30,
                                  exact_strings=fx.BACKPACK_EXACT, product=fx.BACKPACK_PRODUCT, brand_colours=[], max_budget_usd="15",
                                  allow_preview_spend=True, uploads=ups, references_note=fx.BACKPACK_NOTE)
            state = fx.film_to_hold(e, second)
            self.assertEqual(state, "ready_for_review")                     # no master-plate approval needed: it is on the shelf
            slip = e.store.artifact(second, "order_slip")
            self.assertTrue(slip["prefilled_from_shelf"])
            self.assertEqual(slip["brand_colours"], ["#101820"])
            used = {u["used_for"] for u in e.orch.shelf.uses(second)}
            self.assertTrue({"master_plate", "character", "logo", "brand_colour"} <= used, used)
            for node in ("master", "character"):
                self.assertEqual([a for a in e.store.attempts(second) if a["node_id"] == node], [], node)
                self.assertEqual(e.store.asset(e.store.node(second, node)["selected_asset_id"])["source"], "shelf")
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
