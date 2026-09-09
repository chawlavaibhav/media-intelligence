"""Arm-aware prompts: the composite arm (C_composite*) of an exact-text case dispatches the blueprint's textless plate
prompt; every other arm dispatches the main prompt, byte-identical across routes. Image Round 1 (2026-09-08) had
dispatched arm C with the main prompt, so the composite arm was never tested — this pins the fix."""
import unittest

from _support import NoNetworkTestCase, hv2_paths  # noqa: F401
import casebook as CB


class ArmAwarePromptTest(NoNetworkTestCase):
    @classmethod
    def setUpClass(cls):
        cls.book = CB.CaseBook.from_git("HEAD")

    def test_composite_arm_gets_the_textless_plate_prompt(self):
        for case_id in ("IMG-TEXT-01", "IMG-TEXT-02"):
            rows = self.book.rows(case_id)
            arms = {r["arm"] for r in rows}
            comp = [r for r in rows if r["arm"].startswith(CB.COMPOSITE_ARM_PREFIX)]
            others = [r for r in rows if not r["arm"].startswith(CB.COMPOSITE_ARM_PREFIX)]
            self.assertTrue(comp and others, (case_id, arms))
            main_prompts = {r["prompt"] for r in others}
            self.assertEqual(len(main_prompts), 1, f"{case_id}: arms A/B must share one byte-identical prompt")
            plate = {r["prompt"] for r in comp}
            self.assertEqual(len(plate), 1)
            plate = plate.pop()
            self.assertNotEqual(plate, main_prompts.pop())
            low = plate.lower()
            self.assertIn("no text", low)
            self.assertNotIn('"', plate, f"{case_id}: the textless plate prompt must carry no quoted strings to render")

    def test_extract_prompt_refuses_a_composite_arm_without_a_plate_block(self):
        md = "## 6. generation_prompt (x)\n\n```text\nhello\n```\n"
        self.assertEqual(CB.extract_prompt(md), "hello")
        with self.assertRaises(ValueError):
            CB.extract_prompt(md, arm="C_composite_textless_base")

    def test_non_text_cases_are_unchanged(self):
        rows = self.book.rows("IMG-CORE-01")
        self.assertEqual(len({r["prompt"] for r in rows}), 1)


if __name__ == "__main__":
    unittest.main()
