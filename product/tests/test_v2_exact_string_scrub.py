"""P1 v2 — production failed instantly (live 2026-09-24): "exact copy string 'iPhone Duo' appears in a generation prompt".
guard_for() scrubbed the brand from generator prompts but not the customer's exact strings, while the dispatcher refuses
any prompt that contains one — so a recipe naming the product in its anchor, master plate or shot state could never
produce. The guard itself is unchanged: exact text is still code-set. USD 0, no network."""
import unittest

from product import prompts
from product.dispatch import GuardRefused, prompt_guard


def _recipe():
    return {"product_anchor": "The iPhone Duo, a slim graphite foldable phone with a twin-lens camera bar.",
            "visual_language": {"look": "calm premium", "light": "soft window light", "palette": ["graphite", "warm white"],
                                "camera": "slow, steady"},
            "master_plate": {"description": "A pale oak desk by a window; the iPhone Duo lies folded at the centre.",
                             "product_state": "the iPhone Duo folded shut"},
            "character": {"present": False},
            "copy_deck": [{"id": "c1", "text": "Two screens. One pocket."}]}


def _shot():
    return {"n": 1, "first_frame": "The desk by the window, the phone at the centre.", "product_present": True,
            "product_state": "the iPhone Duo unfolded, inner display lit", "camera": "slow push-in",
            "continuity": ["same desk"], "must_not": ["a second iPhone Duo"], "action": "none", "end_state": "held"}


class ExactStringsAreScrubbedFromGeneratorPrompts(unittest.TestCase):
    def setUp(self):
        self.guard = prompts.guard_for({"brand": "Acme"}, _recipe(),
                                       {"exact_strings": ["iPhone Duo", "Pack less. Go further."], "forbidden_words": []})

    def _passes(self, prompt):
        prompt_guard(prompt, exact_strings=self.guard["exact_strings"], forbidden_words=self.guard["forbidden_words"])

    def test_a_recipe_naming_the_product_builds_master_and_shot_prompts_that_pass_the_guard(self):
        master = prompts.master_plate_prompt(_recipe(), self.guard, aspect="9:16", with_product_ref=True)
        shot = prompts.shot_frame_prompt(_recipe(), self.guard, _shot(), aspect="9:16", has_previous=False)
        for p in (master, shot):
            self.assertNotIn("iphone duo", p.lower())
            self._passes(p)                                       # no GuardRefused
        self.assertIn("slim graphite foldable phone", master)     # the rest of the product description survives
        self.assertIn("unfolded, inner display lit", shot)

    def test_an_exact_string_ending_in_punctuation_is_scrubbed_too(self):
        r = _recipe()
        r["master_plate"]["description"] += " A card reads Pack less. Go further. on the desk."
        self._passes(prompts.master_plate_prompt(r, self.guard, aspect="9:16", with_product_ref=True))

    def test_the_guard_still_refuses_a_prompt_with_the_exact_string_injected_directly(self):
        with self.assertRaises(GuardRefused):
            self._passes(f"A phone on a desk; the iPhone Duo is visible. {prompts.NO_LETTERING}")
        with self.assertRaises(GuardRefused):
            prompt_guard(f"A phone labelled iPhone Duo on a desk. {prompts.NO_LETTERING}",
                         exact_strings=["iPhone Duo"], forbidden_words=[])


if __name__ == "__main__":
    unittest.main()
