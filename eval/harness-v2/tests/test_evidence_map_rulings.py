"""Audit close-out, 14 September 2026: the routing map computes every human-acceptance number under the FROZEN
elimination rule, applied literally, through the audit's recompute tool - one implementation of the arithmetic.

Rulings applied (Controller, 14 Sep 2026; record: coordination/decisions/CONTROLLER-AUDIT-CLOSEOUT-EVIDENCE-RULINGS-2026-09-14.md):
    C-3   literal denominators; infrastructure / request failures count where the frozen rule says they count
    C-4   a Stage-A cell touched by duplicated identities, smoke-as-extra-draw or contrary exclusions is descriptive only
          until recomputed - so every cell is recomputed here
    C-6b  STRICT: a failed draw stays a failure; later undeclared re-sends are descriptive product evidence, never counted
    C-6c  exact-text mechanisms are DIFFERENT routes: the model drawing text vs code composing text on a textless plate
    C-6d  elimination is per (route, question), exactly as frozen E4

Two kinds of test:
  * SEALED-FILE tests build the map from the committed sealed run directories (read-only) and assert the numbers the
    Controller's rulings produce: the thirteen groups named in AUDIT-2026-09-10-EVIDENCE-RECOMPUTE.md section 2 move
    exactly as that report's strict column says, and EVERY OTHER cell keeps the accepts / trials the map showed before.
  * SYNTHETIC tests exercise the wiring on made-up RESULTS documents (results-only mode), where the recompute tool
    sees no run directory.
Nothing here writes under eval/capability-map/, eval/registry/ or eval/experiments/.
"""
import unittest

import yaml

from _support import NoNetworkTestCase, hv2_paths
import evidence_map as EM

RUNS_DIR = hv2_paths.EVAL_ROOT / "experiments" / "EVAL-040" / "runs"
REGISTRY = hv2_paths.EVAL_ROOT / "registry" / "registry-v1.jsonl"
RESULT_RUNS = ["img-r1", "half2", "topo3-video", "topo3-nb-video", "vid-knee", "vid-ms", "vid-i2v", "vid-ref", "aud-tts-sarvam",
               "aud-tts-eleven", "aud-music-lyria", "aud-lip", "vid-2spk", "vid-t2v", "vid-wan2"]
COMPOSITE_RUN = "img-r1-composite"

# What the committed map showed at e57bb36 (before the rulings) for every cell: (accepts, trials, eliminated).
# Read from eval/capability-map/ROUTING-EVIDENCE-MAP-v0.yaml at that commit; a literal table so the test does not
# depend on the file it is about to change.
BEFORE = {
    ("AUD-LIP", "kling-lipsync-a2v+chain"): (0, 6, True),
    ("AUD-TTS", "elevenlabs-v3-direct+native"): (4, 6, False),
    ("AUD-TTS", "sarvam-bulbul-v3+native"): (6, 6, False),
    ("IMG-COMP", "flux-2-pro-edit"): (1, 2, False),
    ("IMG-COMP", "nano-banana-pro-edit"): (1, 2, False),
    ("IMG-COMP", "seedream-5-pro-edit"): (2, 2, False),
    ("IMG-CORE", "flux-2-pro"): (5, 8, False),
    ("IMG-CORE", "gpt-image-2"): (7, 8, False),
    ("IMG-CORE", "nano-banana-2"): (7, 8, False),
    ("IMG-CORE", "nano-banana-pro"): (4, 8, False),
    ("IMG-CORE", "qwen-image-3"): (7, 8, False),
    ("IMG-CORE", "seedream-5-pro"): (6, 8, False),
    ("IMG-EDIT", "flux-2-pro-edit"): (3, 4, False),
    ("IMG-EDIT", "nano-banana-pro-edit"): (1, 4, True),
    ("IMG-EDIT", "seedream-5-pro-edit"): (2, 4, False),
    ("IMG-EXT", "flux-2-pro-edit"): (0, 2, True),
    ("IMG-EXT", "nano-banana-pro-edit"): (0, 2, True),
    ("IMG-EXT", "seedream-5-pro-edit"): (2, 2, False),
    ("IMG-REF", "flux-2-pro-edit"): (0, 4, True),
    ("IMG-REF", "nano-banana-pro-edit"): (1, 4, True),
    ("IMG-REF", "seedream-5-pro-edit"): (4, 4, False),
    ("IMG-TEXT", "flux-2-pro+C_composite_textless_base"): (1, 4, True),
    ("IMG-TEXT", "flux-2-pro+code_overlay"): (4, 4, None),
    ("IMG-TEXT", "gpt-image-2+A_cheap_generated"): (4, 4, False),
    ("IMG-TEXT", "nano-banana-2+A_cheap_generated"): (4, 4, False),
    ("IMG-TEXT", "nano-banana-pro+B_premium_generated"): (4, 4, False),
    ("IMG-TEXT", "qwen-image-3+A_cheap_generated"): (2, 4, False),
    ("IMG-TEXT", "recraft-v4+B_premium_generated"): (2, 4, False),
    ("IMG-TEXT", "seedream-5-pro+B_premium_generated"): (2, 4, False),
    ("MUS", "lyria+native"): (4, 4, False),
    ("VID-2SPK", "gemini-omni-1.1-flash+A_native"): (2, 2, False),
    ("VID-2SPK", "kling-v3-pro-audio+A_native"): (0, 2, True),
    ("VID-2SPK", "veo-3.1-fast+A_native"): (2, 2, False),
    ("VID-2SPK", "wan-2.2-a14b+A_native"): (0, 2, True),
    ("VID-2SPK", "wan-3.0-prime+A_native"): (2, 2, False),
    ("VID-I2V", "kling-v3-pro-i2v"): (8, 8, False),
    ("VID-I2V", "minimax-h3-max-i2v"): (7, 8, False),
    ("VID-I2V", "veo-3.1-fast-i2v"): (5, 8, False),
    ("VID-I2V", "wan-2.2-a14b-i2v"): (7, 14, False),
    ("VID-I2V", "wan-3.0-prime-i2v"): (8, 8, False),
    ("VID-KNEE", "minimax-h3-max-480p+knee_cheap"): (0, 2, True),
    ("VID-KNEE", "veo-3.1-full+knee_premium"): (1, 2, False),
    ("VID-KNEE", "veo-3.1-lite+knee_cheap"): (0, 2, True),
    ("VID-MS", "gemini-omni-1.1-flash-10s"): (2, 2, False),
    ("VID-MS", "kling-v3-pro-10s"): (2, 2, False),
    ("VID-MS", "kling-v3-pro-15s"): (2, 2, False),
    ("VID-MS", "veo-3.1-fast-extend+chain"): (2, 2, False),
    ("VID-REF", "veo-3.1-fast-ref2v+native"): (2, 4, False),
    ("VID-T2V", "gemini-omni-1.1-flash"): (8, 8, False),
    ("VID-T2V", "kling-v3-pro-audio"): (2, 8, False),
    ("VID-T2V", "minimax-h3-max"): (5, 8, False),
    ("VID-T2V", "veo-3.1-fast"): (4, 8, False),
    ("VID-T2V", "wan-2.2-a14b"): (4, 6, False),
    ("VID-T2V", "wan-3.0-prime"): (4, 8, False),
    ("VID-TOPO3", "kling-v3-pro+B_premium_native_t2v"): (0, 2, True),
    ("VID-TOPO3", "minimax-h3-max-i2v+A2_nb_still_to_cheap_i2v"): (2, 2, False),
    ("VID-TOPO3", "minimax-h3-max-i2v+A_cheap_still_to_cheap_i2v"): (0, 2, True),
    ("VID-TOPO3", "minimax-h3-max-i2v+C_textless_plate_i2v_composite"): (2, 2, False),
    ("VID-TOPO3", "nano-banana-2+A2_nb_plate_9x16"): (1, 2, False),
    ("VID-TOPO3", "veo-3.1-full+B_premium_native_t2v"): (0, 2, True),
    ("VID-TOPO3", "wan-3.0-prime-i2v+A_cheap_still_to_cheap_i2v"): (0, 2, True),
}

# The thirteen groups of AUDIT-2026-09-10-EVIDENCE-RECOMPUTE.md section 2 (fourteen map cells), strict column:
# (accepts, trials, refusals_or_errors, eliminated, eliminated_by)
AFTER = {
    ("VID-T2V", "kling-v3-pro-audio"): (2, 8, 2, True, ["E2"]),
    ("VID-I2V", "wan-2.2-a14b-i2v"): (2, 8, 6, True, ["E1", "E2"]),
    ("IMG-TEXT", "flux-2-pro+C_composite_textless_base"): (1, 4, 0, True, ["E2"]),
    ("IMG-TEXT", "flux-2-pro+code_overlay"): (4, 4, 0, False, []),
    ("VID-2SPK", "kling-v3-pro-audio+A_native"): (0, 2, 2, True, ["E1", "E2"]),
    ("AUD-LIP", "kling-lipsync-a2v+chain"): (0, 6, 1, True, ["E2"]),
    ("IMG-CORE", "flux-2-pro"): (4, 8, 1, False, []),
    ("IMG-CORE", "gpt-image-2"): (6, 8, 2, False, []),
    ("IMG-CORE", "qwen-image-3"): (6, 8, 1, False, []),
    ("IMG-CORE", "seedream-5-pro"): (6, 8, 1, False, []),
    ("VID-T2V", "minimax-h3-max"): (5, 8, 1, False, []),
    ("VID-T2V", "wan-3.0-prime"): (4, 8, 1, False, []),
    ("AUD-TTS", "elevenlabs-v3-direct+native"): (4, 6, 0, False, []),
    ("VID-REF", "veo-3.1-fast-ref2v+native"): (2, 4, 0, False, []),
}


def _load(p):
    return yaml.safe_load(p.read_text(encoding="utf-8"))


class SealedFilesMapTest(NoNetworkTestCase):
    """Built once from the sealed run directories; every test reads the same map."""
    _map = None

    @classmethod
    def build(cls):
        if cls._map is None:
            records = EM.load_registry(REGISTRY)
            results = [_load(RUNS_DIR / r / "RESULTS.yaml") for r in RESULT_RUNS]
            comp = _load(RUNS_DIR / COMPOSITE_RUN / "RESULTS.yaml")
            frozen = EM.FrozenRule.from_runs_dir(str(RUNS_DIR))
            cls._map = EM.build_map(records, results, comp, registry_path=str(REGISTRY),
                                    results_paths=[str(RUNS_DIR / r / "RESULTS.yaml") for r in RESULT_RUNS], frozen=frozen)
        return cls._map

    def setUp(self):
        super().setUp()
        self.map = self.build()
        self.cells = {(q, n): c for q, b in self.map["questions"].items() for n, c in b["cells"].items()}

    def test_cell_count_and_keys_are_unchanged(self):
        self.assertEqual(self.map["cell_count"], 61)
        self.assertEqual(set(self.cells), set(BEFORE), "cell KEYS are stable so consumers keep their references")

    def test_the_thirteen_named_groups_move_exactly_as_the_strict_column_says(self):
        for key, (acc, n, ref, elim, by) in AFTER.items():
            h = self.cells[key]["human_blind_acceptance"]
            with self.subTest(cell=key):
                self.assertEqual((h["accepts"], h["trials"], h["refusals_or_errors"], h["eliminated"], h["eliminated_by"]), (acc, n, ref, elim, by))
                self.assertEqual(h["rule_basis"], EM.RULE_BASIS)

    def test_every_other_cell_keeps_the_numbers_the_map_already_showed(self):
        for key, (acc, n, elim) in BEFORE.items():
            if key in AFTER:
                continue
            h = self.cells[key]["human_blind_acceptance"]
            with self.subTest(cell=key):
                self.assertEqual((h["accepts"], h["trials"], bool(h["eliminated"])), (acc, n, bool(elim)))

    def test_recorded_in_results_file_is_carried_for_transparency(self):
        h = self.cells[("VID-I2V", "wan-2.2-a14b-i2v")]["human_blind_acceptance"]
        self.assertEqual((h["recorded_in_results_file"]["accepts"], h["recorded_in_results_file"]["trials"], h["recorded_in_results_file"]["eliminated"]), (7, 8, False))
        h = self.cells[("VID-T2V", "kling-v3-pro-audio")]["human_blind_acceptance"]
        self.assertEqual((h["recorded_in_results_file"]["accepts"], h["recorded_in_results_file"]["trials"], h["recorded_in_results_file"]["eliminated"]), (2, 6, False))
        h = self.cells[("AUD-TTS", "elevenlabs-v3-direct+native")]["human_blind_acceptance"]
        self.assertEqual((h["recorded_in_results_file"]["accepts"], h["recorded_in_results_file"]["trials"], h["recorded_in_results_file"]["eliminated"]), (4, 6, True))
        self.assertTrue(h["recorded_in_results_file"]["per_case_scope"])
        h = self.cells[("IMG-TEXT", "flux-2-pro+code_overlay")]["human_blind_acceptance"]
        self.assertEqual((h["recorded_in_results_file"]["accepts"], h["recorded_in_results_file"]["trials"], h["recorded_in_results_file"]["eliminated"]), (4, 4, None))

    def test_wan2_i2v_resends_are_descriptive_and_never_double_counted(self):
        h = self.cells[("VID-I2V", "wan-2.2-a14b-i2v")]["human_blind_acceptance"]
        self.assertEqual(sum(v["trials"] for v in h["per_item"].values()), 8, "8 planned, never 14")
        self.assertEqual(sum(v["refusals_or_errors"] for v in h["per_item"].values()), 6)
        d = h["descriptive_resends"]
        self.assertEqual((d["accepts"], d["trials"]), (5, 6))
        self.assertEqual(len(d["attempts"]), 6)
        self.assertTrue(all(a["run_id"] == "vid-wan2-i2v" for a in d["attempts"]))
        self.assertIn("not counted", d["label"])
        self.assertEqual(h["smoke_draws_excluded"], ["VID-I2V-01__wan-2.2-a14b-i2v__core__r1"])
        k = self.cells[("VID-2SPK", "kling-v3-pro-audio+A_native")]["human_blind_acceptance"]
        self.assertEqual((k["descriptive_resends"]["accepts"], k["descriptive_resends"]["trials"]), (0, 2))
        self.assertEqual(k["smoke_draws_excluded"], ["VID-2SPK-01__kling-v3-pro-audio__A_native__r1"])
        f = self.cells[("IMG-CORE", "flux-2-pro")]["human_blind_acceptance"]
        self.assertEqual((f["descriptive_resends"]["accepts"], f["descriptive_resends"]["trials"]), (1, 1), "a declared redo is a re-send too under C-6b strict")
        self.assertNotIn("descriptive_resends", self.cells[("VID-T2V", "gemini-omni-1.1-flash")]["human_blind_acceptance"])

    def test_c6c_rekeys_the_two_exact_text_mechanisms(self):
        comp = self.cells[("IMG-TEXT", "flux-2-pro+code_overlay")]
        self.assertEqual((comp["route_key"], comp["arm"], comp["text_mechanism"]), ("flux-2-pro+code_overlay", "C_composite_textless_base", "deterministic_text_composition"))
        self.assertIn("The model did NOT render the accepted exact copy", comp["arm_note"])
        self.assertEqual(comp["registry_route_key"], "flux-2-pro")
        bare = self.cells[("IMG-TEXT", "flux-2-pro+C_composite_textless_base")]
        self.assertEqual((bare["route_key"], bare["arm"], bare["text_mechanism"]), ("flux-2-pro", "C_composite_textless_base", "model_draws_text"))
        self.assertEqual(bare["arm_note"], "the provider's own plate output judged against the exact-text contract in img-r1: 1/4, eliminated E2")
        self.assertEqual(bare["human_blind_acceptance"].get("ambiguous", 0), 0, "no contested verdicts once the identities differ")
        for (q, n), c in self.cells.items():
            with self.subTest(cell=(q, n)):
                if q == "IMG-TEXT":
                    self.assertEqual(c["text_mechanism"], "deterministic_text_composition" if n == "flux-2-pro+code_overlay" else "model_draws_text")
                elif (q, n) == ("VID-TOPO3", "minimax-h3-max-i2v+C_textless_plate_i2v_composite"):
                    self.assertEqual(c["text_mechanism"], "deterministic_text_composition")
                else:
                    self.assertEqual(c["text_mechanism"], "not_applicable")
        pairs = {}
        for (q, n), c in self.cells.items():
            pairs.setdefault((q, c["route_key"], c["arm"]), []).append(n)
        self.assertTrue(all(len(v) == 1 for v in pairs.values()), f"no two cells share (question, route_key, arm): {pairs}")

    def test_eliminated_cells_are_never_a_fallback_target(self):
        for (q, n), c in self.cells.items():
            h = c["human_blind_acceptance"]
            with self.subTest(cell=(q, n)):
                if h["eliminated"]:
                    self.assertIsNone(c["fallback"]["route"])
                else:
                    fb = c["fallback"]["route"]
                    if fb is not None:
                        self.assertFalse(self.cells[(q, fb)]["human_blind_acceptance"]["eliminated"])
        vid_i2v = self.map["questions"]["VID-I2V"]["cells"]
        self.assertEqual(vid_i2v["wan-2.2-a14b-i2v"]["rank_in_question"], 5)
        self.assertEqual(vid_i2v["veo-3.1-fast-i2v"]["fallback"]["route"], "kling-v3-pro-i2v", "the last survivor falls back to the first survivor")
        self.assertEqual(self.map["questions"]["VID-T2V"]["cells"]["kling-v3-pro-audio"]["rank_in_question"], 6)
        self.assertEqual(self.map["questions"]["IMG-TEXT"]["cells"]["flux-2-pro+C_composite_textless_base"]["rank_in_question"], 8)

    def test_routing_rules_carry_the_rulings(self):
        rules = {r["id"]: r for r in self.map["routing_rules"]}
        self.assertEqual(rules["RR-1"]["rulings_applied"], ["C-6c"])
        self.assertEqual(rules["RR-1"]["mechanism"], "deterministic_text_composition")
        self.assertIn("The image model did not render the accepted copy", rules["RR-1"]["evidence"])
        self.assertIn("IMG-TEXT/flux-2-pro+code_overlay", rules["RR-1"]["evidence"])
        self.assertEqual(rules["RR-16"]["status"], "withdrawn_as_stage_a_i2v_routing_truth (C-6b)")
        self.assertEqual(rules["RR-16"]["rulings_applied"], ["C-3", "C-6b"])
        self.assertIn("ELIMINATED from image-to-video", rules["RR-16"]["rule"])
        self.assertIn("descriptive product evidence only", rules["RR-16"]["evidence"])
        self.assertIn("caveat", rules["RR-16"])
        self.assertEqual(rules["RR-15"]["rulings_applied"], ["C-3"])
        self.assertIn("kling-v3-pro-audio 2/8", rules["RR-15"]["evidence"])
        self.assertIn("minimax-h3-max 5/8 (one fal 403 refusal counted)", rules["RR-15"]["evidence"])
        self.assertIn("wan-3.0-prime 4/8 (one fal 403 refusal counted)", rules["RR-15"]["evidence"])
        self.assertIn("COUNTED as failures under C-3", rules["RR-15"]["caveat"])
        for rid in ("RR-11", "RR-12"):
            self.assertEqual(rules[rid]["rulings_applied"], ["C-6d"])
            self.assertIn("per-question elimination", rules[rid]["note"])
        self.assertEqual(set(self.map["sources"]["human_acceptance_basis"]) >= {"mode", "recompute_tool", "recompute_tool_sha256", "rule_basis", "rulings_record"}, True)
        self.assertEqual(self.map["sources"]["human_acceptance_basis"]["mode"], "sealed_run_directories")


class ResultsOnlyWiringTest(NoNetworkTestCase):
    """The same arithmetic over RESULTS documents alone (no run directory): re-sends, smoke, refusals, elimination."""

    def rows(self, run, route, verdicts, question="Q1", arm="core", case_stride=4, status=None):
        out = []
        for i, v in enumerate(verdicts):
            case = f"{question}-0{i % case_stride + 1}"
            out.append({"trial_id": f"{case}__{route}__{arm}__r{i // case_stride + 1}", "run_id": run, "case_id": case, "question": question,
                        "route_key": route, "arm": arm, "repeat_index": i // case_stride + 1,
                        "status": "error" if v == "E" else "ok", "error_class": "http_422" if v == "E" else None,
                        "verdict": {"A": "accept", "R": "reject"}.get(v), "verdict_basis": "blind_verdict" if v in "AR" else "fault", "note": ""})
        return out

    def test_a_failed_draw_stays_a_failure_and_its_resend_is_descriptive(self):
        first = self.rows("one", "rho", "EEAAEEAA")            # 4 errors, 4 accepts
        resend = [dict(r, run_id="two", status="ok", error_class=None, verdict="accept", verdict_basis="blind_verdict") for r in first if r["status"] == "error"]
        doc = {"run_id": "one + two", "trials": first + resend, "elimination": [{"question": "Q1", "route_key": "rho", "n_planned": 8, "accepts": 8, "eliminated": False, "eliminated_by": []}]}
        m = EM.build_map([], doc)
        h = m["questions"]["Q1"]["cells"]["rho"]["human_blind_acceptance"]
        self.assertEqual((h["accepts"], h["trials"], h["refusals_or_errors"], h["eliminated"], h["eliminated_by"]), (4, 8, 4, True, ["E1"]))
        self.assertEqual((h["descriptive_resends"]["accepts"], h["descriptive_resends"]["trials"]), (4, 4))
        self.assertEqual(h["recorded_in_results_file"], {"accepts": 8, "trials": 8, "eliminated": False, "eliminated_by": [], "per_case_scope": False, "files": []})
        self.assertIn("results-only", h["rule_basis"])
        self.assertEqual(sum(v["trials"] for v in h["per_item"].values()), 8)

    def test_elimination_is_computed_not_read(self):
        doc = {"run_id": "syn", "trials": self.rows("syn", "sigma", "AARRRRRR"),
               "elimination": [{"question": "Q1", "route_key": "sigma", "n_planned": 8, "accepts": 2, "eliminated": False, "eliminated_by": []}]}
        h = EM.build_map([], doc)["questions"]["Q1"]["cells"]["sigma"]["human_blind_acceptance"]
        self.assertEqual((h["accepts"], h["trials"], h["eliminated"], h["eliminated_by"]), (2, 8, True, ["E2"]), "2 of 8 is ON the E2 line whatever the file recorded")
        self.assertIs(h["recorded_in_results_file"]["eliminated"], False)

    def test_composite_layout_rows_are_a_distinct_route_identity(self):
        bare = self.rows("img", "phi", "RRRA", question="IMG-TEXT", arm="C_composite_textless_base", case_stride=2)
        comp_rows = [{"trial_id": r["trial_id"], "case_id": r["case_id"], "arm": r["arm"], "layout": "composite-v2", "verdict": "accept", "note": "all accepted"} for r in bare]
        comp = {"run_id": "img-composite", "arm": "C_composite_textless_base (plate + code overlay, layout composite-v2)", "judged_utc": "2026-09-09", "blind_as_to_arm": False,
                "per_case": {"IMG-TEXT-01": {"accepted": 2, "trials": 2}, "IMG-TEXT-02": {"accepted": 2, "trials": 2}}, "trials": comp_rows, "cost": {"per_accepted_usd": 0.03}}
        recs = [{"entry_id": "cap-plate", "question": "IMG-TEXT", "route_key": "phi", "arm": "C_composite_textless_base", "capability": "latency_errors_refusals",
                 "prompt_basis": "blueprint_textless_plate", "evidence_tier": "deterministic", "n_items": 2, "trials": 4, "passes": 4, "bank_item_ids": ["IMG-TEXT-01", "IMG-TEXT-02"],
                 "reliability": {"status_counts": {"ok": 4}}, "latency_s": {"by_trial": {"a": 1.0}}, "cost": {}, "items_excluded": []}]
        m = EM.build_map(recs, {"run_id": "img", "trials": bare, "elimination": []}, comp)
        cells = m["questions"]["IMG-TEXT"]["cells"]
        self.assertEqual(set(cells), {"phi+C_composite_textless_base", "phi+code_overlay"})
        a, b = cells["phi+C_composite_textless_base"]["human_blind_acceptance"], cells["phi+code_overlay"]["human_blind_acceptance"]
        self.assertEqual((a["accepts"], a["trials"], a["eliminated"], a.get("ambiguous", 0)), (1, 4, True, 0))
        self.assertEqual((b["accepts"], b["trials"], b["eliminated"]), (4, 4, False))
        self.assertEqual(cells["phi+code_overlay"]["route_key"], "phi+code_overlay")
        self.assertEqual(cells["phi+code_overlay"]["text_mechanism"], "deterministic_text_composition")
        self.assertEqual(cells["phi+C_composite_textless_base"]["text_mechanism"], "model_draws_text")
        self.assertIsNone(cells["phi+C_composite_textless_base"]["fallback"]["route"], "an eliminated route is never a fallback")
        self.assertEqual(cells["phi+code_overlay"]["rank_in_question"], 1)

    def test_recompute_tool_classifies_the_composite_dispatch_as_a_distinct_mechanism(self):
        rc = EM.load_recompute()
        runs = rc.load_runs(str(hv2_paths.REPO_ROOT), str(RUNS_DIR))
        occ = rc.build_occurrences(runs)
        kinds = [r["kind"] for r in occ["IMG-TEXT-01__flux-2-pro__C_composite_textless_base__r1"]]
        self.assertEqual(kinds, ["core", "distinct_mechanism (C-6c)"])
        groups = rc.build_groups(runs, occ, rc.judged_verdicts(runs))
        self.assertIn(("IMG-TEXT", "flux-2-pro+code_overlay", "C_composite_textless_base"), groups)
        self.assertIn(("IMG-TEXT", "flux-2-pro", "C_composite_textless_base"), groups)
        for key in (("IMG-TEXT", "flux-2-pro+code_overlay", "C_composite_textless_base"), ("IMG-TEXT", "flux-2-pro", "C_composite_textless_base")):
            self.assertFalse(any(t["conflict"] for t in groups[key].values()))
            self.assertEqual(rc.planned_denominator(runs, key), 4)
        n = rc.cell_numbers(runs, groups, occ, ("VID-I2V", "wan-2.2-a14b-i2v", "core"))
        self.assertEqual((n["n_planned"], n["accepts"], n["refusals_or_errors"], n["eliminated_by"]), (8, 2, 6, ["E1", "E2"]))


if __name__ == "__main__":
    unittest.main()
