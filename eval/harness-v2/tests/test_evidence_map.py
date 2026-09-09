"""EVAL-041 part 1: evidence_map.py - the tiered ROUTING-EVIDENCE-MAP built from synthetic Registry rows and verdicts.

Proven here: every (question, route) cell carries all four tiers and each tier names itself; every human, screened
and historical tier is marked registry: false; the deterministic tier is registry: true only where rows exist; the
fallback is the next-best route by acceptance within the question; the Controller's routing rules are carried as
human-tier statements (registry: false); the CLI writes a YAML file that reloads to the same map.
Nothing here touches eval/capability-map/ or eval/registry/.
"""
import json
import unittest

import yaml

from _support import NoNetworkTestCase
import evidence_map as EM


def det_row(question, route, cap, n_items, trials, passes, basis="blueprint_main", **extra):
    r = {"entry_id": f"cap-{question}-{route}-{cap}-{basis}", "question": question, "route_key": route, "capability": cap, "prompt_basis": basis,
         "evidence_tier": "deterministic", "n_items": n_items, "trials": trials, "passes": passes, "bank_item_ids": [f"{question}-0{i}" for i in range(1, n_items + 1)],
         "surface": "fal", "tested_date": "2026-09-08T07:00:00Z", "synthetic": False,
         "cost": {"price_source": [f"pins/{route}.html"], "unit_price_pinned": ["0.05"], "billing_pool": ["cash"]}, "items_excluded": []}
    r.update(extra)
    return r


def synthetic_records():
    recs = []
    for route, ok, refusals, cost in (("alpha", 8, 0, "0.400000"), ("beta", 8, 1, "0.300000")):
        recs += [
            det_row("Q1", route, "delivery_format_compliance", 4, 8, ok),
            det_row("Q1", route, "reliability_pass_at_k", 4, 8, ok),
            det_row("Q1", route, "latency_errors_refusals", 4, 8, 8 - refusals,
                    reliability={"status_counts": {"ok": 8 - refusals, **({"refusal": refusals} if refusals else {})}, "refusal_rate": refusals / 8, "error_classes": []},
                    latency_s={"by_trial": {f"t{i}": 3.0 + i for i in range(8)}, "p50": 6.0, "p95": 10.0}),
            det_row("Q1", route, "cost_and_cpao", 4, 8, 8, cost={"price_source": [f"pins/{route}.html"], "unit_price_pinned": ["0.05"], "billing_pool": ["cash"],
                                                                 "settled_total_usd_equiv_all_counted_trials": cost, "n_settled": 8}),
            det_row("Q1", route, "reproducibility", 4, 4, 4, repeat_variance={"pairs": [{"dhash_hamming_max": 6 + i, "ssim_min": 0.8 - i / 100} for i in range(4)]}),
        ]
    # a composite (textless plate + code overlay) cell on route alpha under question Q2
    recs += [det_row("Q2", "alpha", "delivery_format_compliance", 2, 4, 4, basis="blueprint_textless_plate"),
             det_row("Q2", "alpha", "latency_errors_refusals", 2, 4, 4, basis="blueprint_textless_plate",
                     reliability={"status_counts": {"ok": 4}, "refusal_rate": 0.0, "error_classes": []}, latency_s={"by_trial": {"a": 2.0, "b": 3.0}})]
    return recs


def synthetic_results():
    trials = []
    for route, verdicts in (("alpha", "AAAAAAAR"), ("beta", "AAAARRRR"), ("gamma", "RRRRRRRR")):
        for i, v in enumerate(verdicts):
            trials.append({"trial_id": f"Q1-0{i % 4 + 1}__{route}__core__r{i // 4 + 1}", "run_id": "syn", "case_id": f"Q1-0{i % 4 + 1}", "question": "Q1",
                           "route_key": route, "arm": "core", "repeat_index": i // 4 + 1, "status": "ok", "verdict": "accept" if v == "A" else "reject",
                           "verdict_basis": "blind_verdict", "note": ("cut off" if v == "R" and i == 7 else "")})
    return {"run_id": "syn", "revealed_utc": "2026-09-08T13:20:16Z", "commitment_verified": True, "rules_ref": "rules.md", "trials": trials,
            "elimination": [{"question": "Q1", "route_key": "gamma", "n_planned": 8, "accepts": 0, "eliminated": True, "eliminated_by": ["E2"]}]}


def synthetic_composite():
    return {"run_id": "syn-composite", "arm": "C_composite (plate + overlay)", "judged_utc": "2026-09-09", "blind_as_to_arm": False,
            "per_case": {"Q2-01": {"accepted": 2, "trials": 2}, "Q2-02": {"accepted": 2, "trials": 2}}, "cost": {"per_accepted_usd": 0.03},
            "note": "product evidence", "trials": [{"trial_id": "x", "verdict": "accept", "note": "all accepted"}]}


class EvidenceMapTest(NoNetworkTestCase):
    def setUp(self):
        super().setUp()
        self.map = EM.build_map(synthetic_records(), synthetic_results(), synthetic_composite(), registry_path=None, results_paths=["r.yaml"], criteria_sha256="abc")

    def cells(self):
        return {(q, name): c for q, block in self.map["questions"].items() for name, c in block["cells"].items()}

    def test_every_cell_has_every_tier_and_each_tier_names_itself(self):
        cells = self.cells()
        self.assertEqual(set(cells), {("Q1", "alpha"), ("Q1", "beta"), ("Q1", "gamma"), ("Q2", "alpha+code_overlay")})
        self.assertEqual(self.map["cell_count"], 4)
        for key, c in cells.items():
            with self.subTest(cell=key):
                for tier in EM.TIERS:
                    self.assertIn(tier, c)
                    self.assertEqual(c[tier]["tier"], tier)
                    self.assertIn("registry", c[tier])
                self.assertIn("fallback", c)
                self.assertIn("price_pin_ref", c)
                self.assertIn("evidence_date", c)

    def test_no_human_screened_or_historical_cell_is_marked_registry(self):
        for key, c in self.cells().items():
            for tier in ("human_blind_acceptance", "screened_not_qualified", "historical_prior"):
                with self.subTest(cell=key, tier=tier):
                    self.assertIs(c[tier]["registry"], False)
            self.assertIs(c["fallback"]["registry"], False)
        for rule in self.map["routing_rules"]:
            self.assertIs(rule["registry"], False)
            self.assertEqual(rule["tier"], "human_blind_acceptance")
        self.assertEqual(len(self.map["routing_rules"]), 3)
        self.assertTrue(any("code-set" in r["rule"].lower() or "code-set" in r["rule"] for r in self.map["routing_rules"]))

    def test_deterministic_tier_is_registry_only_where_rows_exist(self):
        cells = self.cells()
        alpha = cells[("Q1", "alpha")]["deterministic"]
        self.assertIs(alpha["registry"], True)
        self.assertEqual(len(alpha["rows"]), 5)
        self.assertEqual(alpha["format_compliance"], {"passes": 8, "trials": 8, "n_items": 4, "items_excluded": []})
        self.assertEqual(alpha["refusal_rate"], 0.0)
        self.assertEqual(alpha["trial_cost_usd"]["per_trial_mean"], "0.050000")
        self.assertEqual(alpha["repeat_variance_unseeded"]["pairs"], 4)
        self.assertEqual(alpha["repeat_variance_unseeded"]["dhash_hamming_max"], 9)
        beta = cells[("Q1", "beta")]["deterministic"]
        self.assertAlmostEqual(beta["refusal_rate"], 1 / 8)
        gamma = cells[("Q1", "gamma")]["deterministic"]
        self.assertIs(gamma["registry"], False)
        self.assertEqual(gamma["status"], "no_rows")
        comp = cells[("Q2", "alpha+code_overlay")]
        self.assertIs(comp["deterministic"]["registry"], True)
        self.assertEqual(comp["human_blind_acceptance"]["accepts"], 4)
        self.assertIs(comp["human_blind_acceptance"]["blind_as_to_arm"], False)
        self.assertIn("plate", comp["arm_note"])

    def test_human_tier_carries_n_notes_and_elimination(self):
        h = self.cells()[("Q1", "beta")]["human_blind_acceptance"]
        self.assertEqual((h["accepts"], h["trials"], h["n_items"]), (4, 8, 4))
        self.assertEqual(h["controller_notes"], [{"trial_id": "Q1-04__beta__core__r2", "verdict": "reject", "note": "cut off"}])
        g = self.cells()[("Q1", "gamma")]["human_blind_acceptance"]
        self.assertTrue(g["elimination"]["eliminated"])

    def test_fallback_is_next_best_by_acceptance_within_the_question(self):
        cells = self.cells()
        self.assertEqual(cells[("Q1", "alpha")]["rank_in_question"], 1)
        self.assertEqual(cells[("Q1", "alpha")]["fallback"]["route"], "beta")
        self.assertEqual(cells[("Q1", "beta")]["fallback"]["route"], "gamma")
        self.assertEqual(cells[("Q1", "gamma")]["fallback"]["route"], "alpha", "the last-ranked falls back to the first")
        self.assertIsNone(cells[("Q2", "alpha+code_overlay")]["fallback"]["route"], "a single cell has nothing to fall back to")

    def test_cli_writes_a_yaml_that_reloads(self):
        reg = self.tmp / "reg.jsonl"
        reg.write_text("# header\n" + "".join(json.dumps(r) + "\n" for r in synthetic_records()))
        res = self.tmp / "RESULTS.yaml"
        res.write_text(yaml.safe_dump(synthetic_results()))
        comp = self.tmp / "RESULTS-composite.yaml"
        comp.write_text(yaml.safe_dump(synthetic_composite()))
        out = self.tmp / "map" / "MAP.yaml"
        self.assertEqual(EM.main(["--registry", str(reg), "--results", str(res), "--composite-results", str(comp), "--out", str(out)]), 0)
        m = yaml.safe_load(out.read_text())
        self.assertEqual(m["schema"], "ROUTING-EVIDENCE-MAP-v0")
        self.assertEqual(m["cell_count"], 4)
        self.assertEqual(m["sources"]["registry"], str(reg))
        self.assertTrue(m["sources"]["registry_sha256"])
        for q, block in m["questions"].items():
            for name, c in block["cells"].items():
                for tier in EM.TIERS:
                    self.assertEqual(c[tier]["tier"], tier)
                    if tier != "deterministic":
                        self.assertIs(c[tier]["registry"], False)


if __name__ == "__main__":
    unittest.main()
