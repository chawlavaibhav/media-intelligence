"""Kitchen v3 (founder-approved 2026-09-25): waiter -> chef -> customer -> head cook -> gatekeeper -> customer.

No pantry checker, no recipe checker, no forced stills; the chef writes every prompt in full and picks the tool per shot;
the head cook tastes every take on another company's model and repairs weak takes; kept stills are shown to the
customer; a voice-over is made when the customer asks for one. Simulated providers and workers only (USD 0)."""
import json
import unittest

from product import config, prompts, rulebook
from product.stations import head_cook
from product.tests.support import Env

VO_BRIEF = ("A 15 second film for our backpack for people over 50. Warm and real, one person, one moment. "
            "Add a Hindi voice-over.")


def states(e, jid):
    return [json.loads(x["data_json"]).get("to") for x in e.store.events(jid, ("state",))]


class TheLine(unittest.TestCase):
    def setUp(self):
        self.e = Env()

    def tearDown(self):
        self.e.close()

    def test_order_goes_waiter_to_chef_to_customer_with_no_pantry_and_no_recipe_checker(self):
        e = self.e
        jid = e.submit(duration_s=15)
        e.drain()
        self.assertEqual(e.state(jid), "awaiting_approval")
        path = states(e, jid)
        self.assertNotIn("feasibility", path)
        self.assertIn("directing", path)
        self.assertIsNone(e.store.artifact(jid, "feasibility"))
        self.assertIsNone(e.store.artifact(jid, "recipe_check"))
        r = e.store.artifact(jid, "recipe")
        self.assertEqual(r["form_version"], 3)
        self.assertTrue(r["story"] and r["identity_anchors"]["person"] and r["look"]["picture_prompt"])
        tools = [s["tool"] for s in r["shots"]]
        self.assertIn("video", tools)                          # the chef chose a moving moment; nothing forced it to a still
        self.assertEqual(tools[-1], "end_card")
        self.assertTrue(e.store.assets(jid, role="preview"))   # the customer sees the look of the film with the recipe

    def test_every_call_reads_the_kitchen_card_first(self):
        e = self.e
        text, _ = e.orch.rulebook.card_text("chef", "recipe")
        self.assertTrue(text.startswith("THE KITCHEN"))
        self.assertIn(rulebook.kitchen()["mission"], text)
        self.assertIn("WHAT THIS ROLE MEANS", text)
        self.assertIn("Canon", text)                           # the chef reads the books first (founder 2026-09-25)
        for w in rulebook.AI_WORKERS:
            self.assertIn(w, rulebook.seed_cards())
        for gone in ("pantry_checker", "recipe_checker", "small_taster", "big_taster"):
            self.assertNotIn(gone, rulebook.seed_cards())

    def test_a_newer_founder_seed_supersedes_a_stored_card_learned_on_an_older_seed(self):
        e = self.e
        seed = int(rulebook.seed_cards()["chef"]["version"])
        with e.store.tx() as c:
            c.execute("INSERT INTO rulebook_versions (worker, version, card_json, by, reason, source_lesson, created) VALUES (?,?,?,?,?,?,?)",
                      ("chef", seed - 1, json.dumps({**rulebook.seed_cards()["chef"], "version": seed - 1, "mission": "old"}),
                       "lesson", "an older learned card", None, "2026-09-20T00:00:00Z"))
        self.assertEqual(e.orch.rulebook.card("chef")["mission"], rulebook.seed_cards()["chef"]["mission"])

    def test_the_customer_approves_the_recipe_then_receives_the_dish_with_no_wait_in_between(self):
        e = self.e
        jid = e.submit(duration_s=15)
        e.drain()
        e.orch.approve(jid, by=e.user["email"], budget_usd="15")
        e.drain()
        path = states(e, jid)
        self.assertNotIn("awaiting_master_approval", path)
        self.assertNotIn("awaiting_taste", path)
        self.assertIn("checking", path)
        self.assertIn(e.state(jid), ("ready_for_review", "operator_hold", "needs_customer_decision"))
        shots = {n["node_id"]: n for n in e.store.nodes(jid)}
        self.assertTrue(any(n["kind"] == "photo" for n in shots.values()))     # the real product photo, by code
        stills = [json.loads(x["data_json"]) for x in e.store.events(jid, ("customer_update",))
                  if json.loads(x["data_json"]).get("asset")]
        self.assertTrue(stills)                                                   # kept stills posted to the customer
        final = e.store.artifact(jid, "final_review")
        self.assertEqual(final["written_by"]["worker"], "gatekeeper")

    def test_a_voice_over_is_cast_recorded_and_mixed_when_the_customer_asks(self):
        e = self.e
        jid = e.submit(duration_s=15, text=VO_BRIEF)
        e.drain()
        r = e.store.artifact(jid, "recipe")
        self.assertTrue(r["voice_over"]["wanted"])
        e.orch.approve(jid, by=e.user["email"], budget_usd="15")
        e.drain()
        v = e.store.node(jid, "voice")
        self.assertIsNotNone(v)
        self.assertEqual(v["status"], "done")
        cast = e.store.artifact(jid, "voice_cast")
        self.assertIn(cast["provider"], ("sarvam", "azure", "google", "elevenlabs"))
        self.assertTrue(any(a["route"] == "tts-sarvam" for a in e.store.attempts(jid)))

    def test_no_voice_is_made_when_none_was_asked_for(self):
        e = self.e
        jid = e.submit(duration_s=15)
        e.drain()
        e.orch.approve(jid, by=e.user["email"], budget_usd="15")
        e.drain()
        self.assertIsNone(e.store.node(jid, "voice"))


class TheHeadCookRepairs(unittest.TestCase):
    def test_a_weak_take_is_retaken_with_the_head_cooks_sharper_prompt_never_frozen(self):
        e = Env()
        try:
            jid = e.submit(duration_s=15)
            e.drain()
            e.orch.approve(jid, by=e.user["email"], budget_usd="15")
            calls = {"n": 0}
            real = e.orch.sim.head_cook__ingredient_check

            def first_frame_weak(b, media, **kw):
                v = real(b, media, **kw)
                if kw.get("node_id") == "frame_1" and calls["n"] == 0:
                    calls["n"] += 1
                    return {**v, "usable": False, "repair": "retake", "notes": "her face is turned away",
                            "better_prompt": "SHARPER: she faces the lamp, three-quarter to camera, a slow smile."}
                return v
            e.orch.sim.head_cook__ingredient_check = first_frame_weak
            e.drain()
            spec = json.loads(e.store.node(jid, "frame_1")["spec_json"])
            self.assertIn("SHARPER", spec.get("prompt_override", ""))
            self.assertEqual(spec.get("tool"), "video")                         # still a moving shot
            self.assertEqual(json.loads(e.store.node(jid, "shot_1")["spec_json"])["route"], "FILM-C")
            self.assertTrue(e.store.events(jid, ("head_cook_repair",)))
        finally:
            e.close()

    def test_use_photo_switches_the_shot_to_the_real_product_photo(self):
        e = Env()
        try:
            jid = e.submit(duration_s=15)
            e.drain()
            e.orch.approve(jid, by=e.user["email"], budget_usd="15")
            real = e.orch.sim.head_cook__ingredient_check
            seen = {"n": 0}

            def product_wrong(b, media, **kw):
                v = real(b, media, **kw)
                if kw.get("node_id") == "frame_3" and seen["n"] == 0:
                    seen["n"] += 1
                    return {**v, "usable": False, "repair": "use_photo", "notes": "the product is drawn wrong"}
                return v
            e.orch.sim.head_cook__ingredient_check = product_wrong
            e.drain()
            self.assertEqual(e.store.node(jid, "frame_3")["kind"], "photo")
            self.assertTrue(e.store.events(jid, ("switched_to_photo",)))
        finally:
            e.close()


class ChefAndTastersAreDifferentCompanies(unittest.TestCase):
    def test_default_models_are_independent_and_a_same_company_taster_is_refused(self):
        m = config.worker_models()
        config.check_independence(m)
        self.assertNotEqual(config.maker(m["chef"]), config.maker(m["head_cook"]))
        self.assertNotEqual(config.maker(m["chef"]), config.maker(m["gatekeeper"]))
        with self.assertRaises(ValueError):
            config.check_independence({**m, "head_cook": "azure_openai:gpt-5.6-luna"})


class ChefPromptsAreSentAsWritten(unittest.TestCase):
    def test_only_safety_lines_are_added_and_on_screen_words_never_reach_the_picture(self):
        g = prompts.guard_for({"brand": "Apple"}, {"copy_deck": [{"text": "Aaram Se Dekho"}, {"text": "iPhone Duo"}]},
                              {"exact_strings": ["iPhone Duo"]})
        p = prompts.chef_picture_prompt('Meera, 62, holds the iPhone Duo by the lamp. "Aaram Se Dekho" sits below her.', g,
                                        aspect="9:16", refs_note=prompts.REFS_NOTE)
        self.assertIn("Meera, 62, holds the product by the lamp.", p)
        self.assertNotIn("Aaram", p)
        self.assertTrue(p.endswith(prompts.NO_LETTERING))
        from product.dispatch import prompt_guard
        prompt_guard(p, **g)


if __name__ == "__main__":
    unittest.main()
