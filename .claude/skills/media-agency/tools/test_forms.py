#!/usr/bin/env python3
"""Tests for the stage-form gate and the prompt builder.

    python3 -m unittest .claude/skills/media-agency/tools/test_forms.py   (from the repo root)
"""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_prompts as bp  # noqa: E402
import check_stage as cs  # noqa: E402

EXAMPLE = HERE.parent / "forms" / "examples" / "mokobara-odyssey-001"
REPO = HERE.parents[3]


def load(n):
    return json.loads((EXAMPLE / "stages" / f"0{n}-{cs.STAGES[n]}.json").read_text(encoding="utf-8"))


class SchemaSubset(unittest.TestCase):
    def test_types_required_enum_min(self):
        sch = {"type": "object", "required": ["a"], "properties": {
            "a": {"type": "string", "minLength": 1}, "b": {"type": "integer", "minimum": 1},
            "c": {"type": "string", "enum": ["x"]}, "d": {"type": "array", "minItems": 1, "items": {"type": "number"}}}}
        self.assertEqual(cs.validate({"a": "ok", "b": 2, "c": "x", "d": [1.5]}, sch), [])
        probs = cs.validate({"a": " ", "b": 0, "c": "y", "d": []}, sch)
        self.assertEqual(len(probs), 4, probs)
        self.assertIn("$.a: empty", probs)

    def test_bool_is_not_a_number(self):
        self.assertTrue(cs.validate(True, {"type": "number"}))


class WorkedExample(unittest.TestCase):
    """The retro-fit: the accepted Mokobara job, replayed into the forms, passes the gate."""

    def test_all_five_stages_complete(self):
        res = cs.check_job(EXAMPLE, 5, REPO)
        for n, r in res.items():
            self.assertEqual(r["status"], "COMPLETE", f"stage {n}: {r['problems']}")

    def test_canon_ids_are_checked_against_the_corpus(self):
        ids = cs.known_canon_ids(REPO)
        self.assertIsNotNone(ids)
        self.assertGreater(len(ids), 1000)
        for c in load(3)["canon_consulted"]:
            self.assertIn(c["id"], ids)


class GateRefusals(unittest.TestCase):
    def setUp(self):
        self.ctx = {"authors": set(), "canon_ids": cs.known_canon_ids(REPO)}
        cs.cross_1(load(1), self.ctx)
        cs.cross_2(load(2), self.ctx)

    def problems3(self, f3):
        return cs.validate(f3, cs.load_schema(3)) + cs.cross_3(f3, self.ctx)

    def test_empty_impact_is_named(self):
        f3 = load(3); f3["board"]["beats"][2]["impact"] = ""
        self.assertTrue(any("beats[2].impact: empty" in p for p in self.problems3(f3)))

    def test_hero_frame_must_be_a_beat(self):
        f3 = load(3); f3["board"]["hero_frame"]["beat"] = 42
        self.assertTrue(any("hero_frame" in p for p in self.problems3(f3)))

    def test_invented_canon_id_is_refused(self):
        f3 = load(3); f3["board"]["beats"][0]["canon"].append("sk_made_up_0001")
        self.assertTrue(any("sk_made_up_0001" in p for p in self.problems3(f3)))

    def test_mandatory_item_off_the_board(self):
        f3 = load(3)
        for b in f3["board"]["beats"]:
            b["mandatory_ids"] = [m for m in b["mandatory_ids"] if m != "M5"]
        self.assertTrue(any("M5" in p for p in self.problems3(f3)))

    def test_timings_must_add_up(self):
        f3 = load(3); f3["board"]["beats"][3]["t_out"] = 19.0
        self.assertTrue(any("does not follow" in p for p in self.problems3(f3)))

    def test_string_without_source(self):
        f3 = load(3); f3["copy_deck"]["sources"].pop("tagline")
        self.assertTrue(any("sources['tagline']" in p for p in self.problems3(f3)))

    def test_first_frame_required_for_a_film_beat(self):
        f3 = load(3); f3["board"]["beats"][3].pop("first_frame")
        self.assertTrue(any("first_frame missing" in p for p in self.problems3(f3)))

    def test_blocking_ask_without_answer_blocks_stage_1(self):
        f1 = load(1); f1["asks"][0]["blocking"] = True
        self.assertTrue(any("blocking ask" in p for p in cs.cross_1(f1, {"authors": set()})))

    def test_spend_over_cap_blocks_stage_4(self):
        f4 = load(4); f4["expected_spend"]["total_usd"] = 99.0
        self.assertTrue(any("exceeds the Stage 1 cap" in p for p in cs.cross_4(f4, self.ctx)))

    def test_manual_only_route_needs_a_test(self):
        f4 = load(4); f4["risk_order"] = [f4["risk_order"][0]]
        self.assertTrue(any("manual_only" in p for p in cs.cross_4(f4, self.ctx)))

    def test_checker_may_not_be_the_author(self):
        f5 = load(5); f5["checker_session"] = "producer-2026-09-21"
        ctx = dict(self.ctx); ctx["acceptance_ids"] = {"A1", "A2", "A3", "A4", "A5"}
        self.assertTrue(any("not independent" in p for p in cs.cross_5(f5, ctx)))

    def test_det_fail_is_not_a_deliverable(self):
        f5 = load(5); f5["det"][0]["result"] = "fail"
        self.assertTrue(any("FAIL" in p for p in cs.cross_5(f5, self.ctx)))

    def test_accepted_verdict_requires_every_acceptance_statement_scored(self):
        f5 = load(5); f5["acceptance_scored"] = f5["acceptance_scored"][:2]
        ctx = dict(self.ctx); ctx["acceptance_ids"] = {"A1", "A2", "A3", "A4", "A5"}
        self.assertTrue(any("not scored" in p for p in cs.cross_5(f5, ctx)))

    def test_require_stages_complete_refuses_missing_forms(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "stages").mkdir()
            with self.assertRaises(SystemExit) as e:
                cs.require_stages_complete(d, 4)
            self.assertIn("REFUSED", str(e.exception))


class PromptBuilder(unittest.TestCase):
    def test_deterministic_and_from_form_fields(self):
        f3 = load(3)
        a, b = bp.build(f3), bp.build(copy.deepcopy(f3))
        self.assertEqual(a, b)
        beat4 = a[4]
        self.assertIn(f3["board"]["beats"][3]["first_frame"].rstrip(".").lower(), beat4["still"].lower())
        self.assertIn("The EXACT same bag as in the reference images", beat4["still"])
        self.assertIn(f3["board"]["beats"][3]["impact"][:40].lower(), beat4["motion"].lower())
        self.assertTrue(beat4["still"].endswith(bp.DEFAULT_NEGATIVE) or beat4["still"].endswith(f3["board"]["negative_line"]))
        self.assertNotIn(7, a)  # the code-composed end card has no prompt

    def test_board_change_changes_prompts(self):
        f3 = load(3); f3["board"]["identity_anchors"]["bag"] = "a bright red duffel"
        self.assertIn("a bright red duffel", bp.build(f3)[2]["still"])

    def test_copy_deck_string_in_a_beat_is_refused(self):
        f3 = load(3); f3["board"]["beats"][1]["framing"] += " with the words Room for the long way home. on the sand"
        with self.assertRaises(SystemExit):
            bp.build(f3)


if __name__ == "__main__":
    unittest.main()
