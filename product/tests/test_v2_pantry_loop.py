"""P1 v2 — the pantry loop (reproduced 2026-09-24 on a live-mode iPhone Duo 15-s 9:16 film, no voice, official photos):
the job bounced between `understanding` and `awaiting_customer_input` forever because
  1. the code floor read "unfolded" in a still, and "dialogue" in "without ... dialogue", as `cannot` actions; and
  2. an accepted alternative only stuck when the pantry model repeated its action word for word, which it never does.
USD 0, no network."""
import unittest

from product import library
from product.tests import fixtures_v2 as fx
from product.tests.support import Env


def provider_attempts(e, jid):
    return [a for a in e.store.attempts(jid) if a["category"] == "provider"]


class TheFloorReadsStillsAndNegationsAsNoAction(unittest.TestCase):
    def test_the_three_iphone_duo_sentences_are_not_cannot_actions(self):
        self.assertEqual(library.floor_class("Show a still of the phone unfolded with the inner display visible", None),
                         "product_state_still")
        self.assertEqual(library.floor_class("Cut editorially between the folded and unfolded still states", None),
                         "product_state_still")
        self.assertEqual(library.floor_class("Use music and natural sound without spoken words or dialogue", None), "none")
        self.assertEqual(library.floor_class("Use music and natural sound without spoken words or dialogue", "camera_move_static_product"),
                         "camera_move_static_product")

    def test_real_actions_are_held_to_the_same_class_as_before(self):
        self.assertEqual(library.floor_class("A hand unfolds the phone", None), "hands_work_mechanism")
        self.assertEqual(library.floor_class("Hands unzip the bag", None), "hands_work_mechanism")
        self.assertEqual(library.floor_class("The woman speaks to camera", None), "speech_or_lipsync")
        self.assertEqual(library.floor_class("She sings", None), "speech_or_lipsync")
        self.assertEqual(library.floor_class("A hand unfolds the phone", "product_state_still"), "hands_work_mechanism")

    def test_a_still_or_a_negation_elsewhere_does_not_excuse_a_real_action(self):
        self.assertEqual(library.floor_class("Hands unzip the bag, then a still of it open", None), "hands_work_mechanism")
        self.assertEqual(library.floor_class("Hands unzip the bag and a still of it open", None), "hands_work_mechanism")
        self.assertEqual(library.floor_class("A still hand unfolds the phone", None), "hands_work_mechanism")   # adjective, not a picture
        self.assertEqual(library.floor_class("No music, and she sings", None), "speech_or_lipsync")
        self.assertEqual(library.floor_class("No music and she sings", None), "speech_or_lipsync")
        self.assertEqual(library.floor_class("Not only does she sing, she dances", None), "speech_or_lipsync")
        self.assertEqual(library.floor_class("She never stops talking", None), "speech_or_lipsync")


def _rewording_pantry(e):
    """The pantry model as it behaves live: the same needs, reworded every round, and the accepted alternative's `use`
    never echoed back verbatim."""
    rounds = {"n": 0}

    def pantry(b, media):
        rounds["n"] += 1
        n = rounds["n"]
        verbs = ["A hand unfolds the phone to reveal the inner display", "The hand opens the phone out along its hinge",
                 "Fingers unfold the handset flat", "Both hands unfold the device"]
        return {"product_truth": [], "actions_needed": [
            {"id": "A1", "action": "The camera glides slowly around the closed phone", "action_class": "camera_move_static_product",
             "required_by_customer": False},
            {"id": "A2", "action": verbs[(n - 1) % len(verbs)], "action_class": "simple_hand_gesture", "required_by_customer": True},
            {"id": "A3", "action": "Use music and natural sound without spoken words or dialogue", "action_class": "none",
             "required_by_customer": True},
            {"id": "A4", "action": "Show a still of the phone unfolded with the inner display visible", "action_class": "product_state_still",
             "required_by_customer": True}]}
    e.orch.sim.pantry_checker__feasibility = pantry
    return rounds


class AnAcceptedAlternativeSticksAcrossRounds(unittest.TestCase):
    def test_the_customer_accepts_once_and_the_job_reaches_directing_although_the_pantry_rewords_its_actions(self):
        e = Env()
        try:
            rounds = _rewording_pantry(e)
            jid = fx.submit_backpack_film(e)
            e.drain()
            self.assertEqual(e.state(jid), "awaiting_customer_input")
            f = e.store.artifact(jid, "feasibility")
            self.assertEqual(f["verdict"], "cannot_make")
            self.assertEqual([x["action_class"] for x in f["alternatives"]], ["hands_work_mechanism"])   # only the real unfold
            e.orch.provide_input(jid, by=e.user["email"], accepted_alternatives=[
                {"instead_of": x["for_action"], "use": "the phone shown unfolded as a still"} for x in f["alternatives"]])
            e.orch.step(jid)              # waiter folds the answer in
            e.orch.step(jid)              # pantry re-checks — with reworded actions
            self.assertEqual(rounds["n"], 2)
            self.assertEqual(e.state(jid), "directing")
            f2 = e.store.artifact(jid, "feasibility")
            self.assertIn(f2["verdict"], ("go", "go_with_limits"))
            a2 = next(a for a in f2["actions_needed"] if a["id"] == "A2")
            self.assertEqual((a2["action"], a2["action_class"], a2["alternative_by"]),
                             ("the phone shown unfolded as a still", "product_state_still", "customer_accepted"))
            self.assertEqual(a2["instead_of"], "The hand opens the phone out along its hinge")
            self.assertFalse([a for a in f2["actions_needed"] if a["best_verdict"] == "cannot"])
            self.assertEqual(provider_attempts(e, jid), [])
        finally:
            e.close()

    def test_an_alternative_accepted_through_the_waiters_reworded_copy_still_sticks_by_its_class(self):
        e = Env()
        try:
            _rewording_pantry(e)
            jid = fx.submit_backpack_film(e)
            e.drain()
            f = e.store.artifact(jid, "feasibility")
            alts = [{"instead_of": x["for_action"], "use": x["alternative"], "action_class": x["action_class"]} for x in f["alternatives"]]
            e.orch.provide_input(jid, by=e.user["email"], accepted_alternatives=alts)
            real = e.orch.sim.waiter__understanding

            def waiter(b, media):                     # the waiter model paraphrases the accepted alternative
                u = real(b, media)
                u["accepted_alternatives"] = [{"instead_of": "opening the phone", "use": "a picture of it open"}]
                return u
            e.orch.sim.waiter__understanding = waiter
            e.orch.step(jid)
            e.orch.step(jid)
            self.assertEqual(e.state(jid), "directing")
        finally:
            e.close()


class TheSameAskIsNeverSentTwice(unittest.TestCase):
    def test_a_customer_who_answers_without_ticking_the_alternative_is_not_asked_again(self):
        e = Env()
        try:
            _rewording_pantry(e)
            jid = fx.submit_backpack_film(e)
            e.drain()
            self.assertEqual(e.state(jid), "awaiting_customer_input")
            e.orch.provide_input(jid, by=e.user["email"], facts=["it is the new Duo"], note="go ahead")   # no alternative ticked
            e.orch.step(jid)
            e.orch.step(jid)
            self.assertEqual(e.state(jid), "directing")
            f2 = e.store.artifact(jid, "feasibility")
            self.assertEqual(f2["ask_customer"], [])
            a2 = next(a for a in f2["actions_needed"] if a["id"] == "A2")
            self.assertEqual((a2["action_class"], a2["alternative_by"]), ("product_state_still", "system_applied_after_asking_once"))
            self.assertTrue(f2["loop_guard"])
            self.assertTrue(e.store.events(jid, ("pantry_loop_guard",)))
            self.assertEqual(provider_attempts(e, jid), [])
        finally:
            e.close()

    def test_a_part_already_requested_once_becomes_a_limit_not_a_second_request(self):
        e = Env()
        try:
            photos = [fx.BACKPACK_PHOTOS[0]]
            text = ("A 15-second film for our backpack. The camera circles the bag, then shows the front pocket open "
                    "with the bright yellow lining. It must show the front pocket open. Calm and premium.")
            jid = fx.submit_backpack_film(e, text=text, photos=photos, note="")
            e.drain()
            self.assertEqual(e.state(jid), "awaiting_customer_input")
            first = e.store.artifact(jid, "feasibility")
            self.assertEqual(first["verdict"], "need_input")
            e.orch.provide_input(jid, by=e.user["email"], note="we don't have that photo")
            e.orch.step(jid)
            e.orch.step(jid)
            f2 = e.store.artifact(jid, "feasibility")
            self.assertFalse(set(f2["ask_customer"]) & set(first["ask_customer"]))
            self.assertTrue(f2["limits"])
            self.assertEqual(f2["verdict"], "go_with_limits")
            self.assertEqual(e.state(jid), "directing")
        finally:
            e.close()


if __name__ == "__main__":
    unittest.main()
