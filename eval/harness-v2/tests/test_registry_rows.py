"""EVAL-041 part 1: registry_rows.py on a SYNTHETIC sealed run (built in the temp dir, never a committed one).

Proven here:
    - aggregation counts: n_items = distinct cases, never trials and never repeats; trials = n_items x 2 for artifact
      and trial cells; the reproducibility row counts one repeat PAIR per item;
    - a provider refusal is a trial (a fail) in the ledger rows, an item without an artifact is dropped from the format
      rows and named; a local network failure / pre-dispatch refusal is EXCLUDED from trials and listed;
    - a non-deterministic capability (exact_text_devanagari) is refused by the registry gate on every path;
    - the default (dry) mode writes nothing; --write appends rows that carry every field validate_registry.py requires
      of a row, synthetic: false, the criteria sha256, the plan sha256 and evidence_tier: deterministic, and a second
      --write of the same rows is refused (a row is written once);
    - RegistryHarness never overrides the writer.
Nothing here touches eval/registry/registry-v1.jsonl; the registry used is a temp copy of its comment header.
"""
import hashlib
import importlib.util
import json
import shutil
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

from _support import NoNetworkTestCase, hv2_paths
import battery_harness as BH
import casebook as CB
import registry_rows as RR
import store as S
from instruments import imageio as IO
from instruments import registry_gate as RG

HAVE_FFMPEG = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))
PROMPT = "A synthetic prompt for the registry tests."
PROMPT_SHA = hashlib.sha256(PROMPT.encode("utf-8")).hexdigest()
ROUTES = {
    "r-fal": {"surface": "fal", "provider": "fal", "model_id": "fake/route-a", "endpoint": "https://queue.fal.run/fake/route-a", "unit_price": "0.010"},
    "r-vx": {"surface": "vertex", "provider": "vertex", "model_id": "fake-image", "endpoint": "https://aiplatform.example/fake-image:generateContent", "unit_price": "0.020"},
}


def _png(w, h, seed):
    rows = [b"".join(bytes(px) for px in [((x * 7 + seed) % 256, (y * 5 + seed) % 256, (x + y + seed) % 256) for x in range(w)]) for y in range(h)]
    return IO.encode_png(rows, w, h)


def _case(case_id, aspect, language, size):
    return {"case_id": case_id, "item_id": case_id, "lane": "IMG", "blueprint_ref": "bp.md",
            "conditions": {"COND-DELIVERY": {"aspect_ratio": aspect, "resolution": f"{size[1]}p", "duration_s": "not_applicable", "fps": "not_applicable",
                                             "delivery_size_declared": True, "platform_target": "test"},
                           "COND-LOAD": {"n_people": 0, "scene_complexity_class": "minimal"},
                           "COND-REFERENCE": {"reference_type": "none"}, "COND-INPUT": {"input_source_class": "none"}, "COND-OPERATION": "generate",
                           "COND-LANGUAGE": {"language": language, "script_system": "latin"}, "COND-CONSTRAINT": {"exact_string_count": 0},
                           "COND-WORKFLOW": {"workflow_mode_per_route_arm": {"all core routes": "t2i"}}},
            "routes": [{"route_key": rk, "surface": ROUTES[rk]["surface"], "arm": "core", "repeats": 2, "billing_pool": "cash",
                        "params": {"aspect": aspect, "resolution": f"{min(size)}p", "audio": "not_applicable", "seed": "unset"}} for rk in ROUTES]}


def synthetic_book():
    tc = {"cases": [_case("SYN-A-01", "4:5", "en", (40, 50)), _case("SYN-A-02", "1:1", "en", (40, 40))]}
    md = "# bp\n\n## 6. generation_prompt\n\n```text\n" + PROMPT + "\n```\n"
    return CB.CaseBook(tc, lambda ref: md, {"kind": "synthetic", "test_cases_sha256": "synthetic"},
                       cost_table={"route_catalogue": {rk: {"unit_price": v["unit_price"]} for rk, v in ROUTES.items()}})


class SyntheticRun:
    """A sealed run directory in the schema run_live.py writes: PLAN.yaml + PLAN.sha256, artifacts/, trials/, ledger/."""

    def __init__(self, root: Path, run_id="syn-run"):
        self.out = root / run_id
        self.run_id = run_id
        self.store = S.SealedStore(self.out / "artifacts")
        self.trials, self.ledger, self.n = [], [], 0
        self.t0 = datetime(2026, 9, 8, 7, 0, tzinfo=timezone.utc)

    def _ts(self, offset_s):
        return (self.t0 + timedelta(seconds=offset_s)).isoformat().replace("+00:00", "Z")

    def add(self, case_id, route, rep, outcome="ok", size=(40, 50), seed=1, request_id="req-x", ambiguous=False):
        self.n += 1
        tid = f"{case_id}__{route}__core__r{rep}"
        r = ROUTES[route]
        plan = {"seq": self.n, "trial_id": tid, "case_id": case_id, "item_id": case_id, "route_key": route, "arm": "core", "repeat_index": rep,
                "tranche": "1a", "surface": r["surface"], "surface_model_id": r["model_id"], "endpoint": r["endpoint"], "billing_pool": "cash",
                "currency": "USD", "unit_price": r["unit_price"], "quantity": "1", "quantity_unit": "images", "price_pin_ref": f"pins/{route}.html",
                "seed_policy": "unset", "estimated_usd_equiv": r["unit_price"]}
        self.trials.append(plan)
        res = f"res-{self.n:06d}"
        base = {"attempt_id": tid, "trial_id": tid, "case_id": case_id, "item_id": case_id, "route_key": route, "arm": "core", "repeat_index": rep,
                "provider": r["provider"], "surface": r["surface"], "model_id": r["model_id"], "model_version": r["model_id"], "endpoint": r["endpoint"],
                "workflow": "t2i", "lane": "image", "seed_policy": "unset", "seed": None, "currency": "USD", "prompt_hash": PROMPT_SHA,
                "config_hash": hashlib.sha256(f"{case_id}|{route}".encode()).hexdigest(), "config_location": f"{tid}.request.json",
                "requested_at": self._ts(10 * self.n), "completed_at": self._ts(10 * self.n + 4 + rep), "reservation_id": res, "cost_ref": f"cost-{res}",
                "reserved_amount_usd_equiv": r["unit_price"], "billing_state": "reported", "synthetic": False, "retries": 0, "retry_of_attempt_id": None,
                "ambiguous_dispatch": ambiguous, "outcome_resolved": not ambiguous, "provider_request_id": request_id, "price_pin_ref": plan["price_pin_ref"]}
        self.ledger.append({"type": "reservation", "reservation_id": res, "cost_ref": f"cost-{res}", "amount_usd": r["unit_price"], "amount_usd_equiv": r["unit_price"],
                            "trial_id": tid, "attempt_id": tid})
        self.store.write_request(tid, b'{"prompt": "x"}')
        if outcome == "pre_dispatch":
            (self.out / "trials").mkdir(parents=True, exist_ok=True)
            (self.out / "trials" / f"{tid}.pre_dispatch_refusal.json").write_text(json.dumps({"reason": "DNS failure: nothing was sent", "sent": False}))
            self.ledger.append({"type": "release", "reservation_id": res, "reason": "dispatch did not occur"})
            return tid
        if outcome == "ok":
            rec = self.store.seal(tid, _png(size[0], size[1], seed), "image/png")
            attempt = {**base, "status": "ok", "error_class": None,
                       "artifact": {k: rec[k] for k in ("artifact_id", "relative_path", "bytes", "sha256", "content_type", "media_kind")}}
        elif outcome == "refusal":
            attempt = {**base, "status": "refusal", "error_class": "moderation_block", "artifact": None}
        elif outcome == "network_failure":
            attempt = {**base, "status": "error", "error_class": "network_failure", "artifact": None, "provider_request_id": None, "completed_at": None}
        else:
            raise ValueError(outcome)
        self.store.write_attempt(tid, attempt)
        self.ledger.append({"type": "spend", "reservation_id": res, "cost_ref": f"cost-{res}", "amount_usd": r["unit_price"], "amount_usd_equiv": r["unit_price"],
                            "trial_id": tid, "attempt_id": tid, "billing_state": "reported"})
        return tid

    def commit(self):
        header = {"plan": "EVAL-040-RUN-PLAN", "run_id": self.run_id, "mode": "lane", "commit": "0000000", "test_cases_sha256": "synthetic",
                  "counts": {"trials": len(self.trials), "excluded": 0}, "authorisation_sha256": "synthetic"}
        text = yaml.safe_dump({"header": header, "trials": self.trials, "excluded": []}, sort_keys=False)
        (self.out / "PLAN.yaml").write_text(text)
        sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
        (self.out / "PLAN.sha256").write_text(f"{sha}  PLAN.yaml\n")
        led = self.out / "ledger" / self.run_id
        led.mkdir(parents=True, exist_ok=True)
        (led / "spend-ledger.jsonl").write_text("".join(json.dumps(r) + "\n" for r in self.ledger))
        return f"{self.out}:{self.run_id}", sha


def standard_run(tmp: Path):
    """r-fal: 2 cases x 2 repeats, all ok.  r-vx: SYN-A-01 r1 REFUSED (a trial), r2 ok; SYN-A-02 r1 network failure (excluded), r2 ok."""
    run = SyntheticRun(tmp / "runs")
    run.add("SYN-A-01", "r-fal", 1, size=(40, 50), seed=1)
    run.add("SYN-A-02", "r-fal", 1, size=(40, 40), seed=2)
    run.add("SYN-A-01", "r-vx", 1, outcome="refusal")
    run.add("SYN-A-02", "r-vx", 1, outcome="network_failure")
    run.add("SYN-A-01", "r-fal", 2, size=(40, 50), seed=3)
    run.add("SYN-A-02", "r-fal", 2, size=(40, 40), seed=4)
    run.add("SYN-A-01", "r-vx", 2, size=(40, 50), seed=5)
    run.add("SYN-A-02", "r-vx", 2, size=(40, 40), seed=6)
    return run


@unittest.skipUnless(HAVE_FFMPEG, "ffmpeg/ffprobe genuinely absent on this machine")
class RegistryRowsTest(NoNetworkTestCase):
    def setUp(self):
        super().setUp()
        self.run = standard_run(self.tmp)
        self.spec, self.plan_sha = self.run.commit()
        self.book = synthetic_book()
        self.registry = self.tmp / "registry-v1.jsonl"
        header = [l for l in (hv2_paths.EVAL_ROOT / "registry" / "registry-v1.jsonl").read_text().splitlines() if l.startswith("#")]
        self.registry.write_text("\n".join(header) + "\n")

    def build(self, **kw):
        return RR.build_rows([self.spec], book=self.book, harness_root=self.tmp / "hz", **kw)

    def rows(self, result, cap, route):
        return [r for r in result["records"] if r["capability"] == cap and r["route_key"] == route]

    def test_aggregation_counts_over_a_clean_cell(self):
        res = self.build()
        for cap in ("delivery_format_compliance", "reliability_pass_at_k", "latency_errors_refusals", "cost_and_cpao"):
            with self.subTest(capability=cap):
                (row,) = self.rows(res, cap, "r-fal")
                self.assertEqual((row["n_items"], row["repeats_per_item"], row["trials"], row["passes"]), (2, 2, 4, 4))
                self.assertEqual(row["bank_item_ids"], ["SYN-A-01", "SYN-A-02"])
                self.assertEqual(row["uncertainty"]["status"], "computed")
                self.assertEqual(row["uncertainty"]["method"], "clopper_pearson_95")
                self.assertEqual(row["uncertainty"]["computed_over"], "base_items")
                self.assertEqual(row["uncertainty"]["n_used"], 2)
                self.assertEqual(row["uncertainty"]["independence_status"], "NOT ESTABLISHED")
                self.assertTrue(row["uncertainty"]["is_reference_calculation_only"])
                self.assertEqual(row["question"], "SYN-A")
                self.assertEqual(row["conditions"]["COND-LANGUAGE.language"], "en")
                self.assertEqual(row["conditions"]["declared_per_item"]["SYN-A-01"]["COND-DELIVERY.aspect_ratio"], "4:5")
                self.assertEqual(row["excluded_trials"], [])
        (rep,) = self.rows(res, "reproducibility", "r-fal")
        self.assertEqual((rep["n_items"], rep["repeats_per_item"], rep["trials"]), (2, 1, 2), "one repeat PAIR per item is one observation")
        self.assertEqual(rep["observation_unit"], "repeat_pair")
        self.assertEqual(rep["repeat_variance"]["n_pairs"], 2)
        self.assertEqual(rep["variance_uncertainty"]["not_computed_reason"], "descriptive_only_result")
        self.assertIsNotNone(rep["repeat_variance"]["dhash_hamming"]["max"])
        (cost,) = self.rows(res, "cost_and_cpao", "r-fal")
        self.assertEqual(cost["cpao"]["absence_reason"], "not_applicable")
        self.assertEqual(cost["cost"]["settled_total_usd_equiv_all_counted_trials"], "0.040000")
        (lat,) = self.rows(res, "latency_errors_refusals", "r-fal")
        self.assertEqual(lat["reliability"]["refusal_rate"], 0.0)
        self.assertEqual(lat["latency_s"]["n"], 4)
        self.assertGreaterEqual(lat["latency_s"]["p95"], lat["latency_s"]["p50"])
        (rel,) = self.rows(res, "reliability_pass_at_k", "r-fal")
        self.assertEqual(rel["pass_at_k"]["items_with_all_passes"], 2)

    def test_n_items_never_counts_repeats_or_trials(self):
        res = self.build()
        for row in res["records"]:
            with self.subTest(entry=row["entry_id"]):
                self.assertEqual(row["n_items"], len(row["bank_item_ids"]))
                self.assertEqual(row["trials"], row["n_items"] * row["repeats_per_item"])
                self.assertEqual(len({tv["item_id"] for tv in row["trial_verdicts"]}), row["n_items"])
                self.assertEqual(len(row["trial_verdicts"]), row["trials"])
                self.assertLessEqual(row["passes"], row["trials"])
                self.assertEqual(row["uncertainty"]["n_used"], row["n_items"])

    def test_refusal_is_a_trial_and_infrastructure_faults_are_excluded(self):
        res = self.build()
        (lat,) = self.rows(res, "latency_errors_refusals", "r-vx")
        # SYN-A-01: refusal + ok = 2 counted trials (1 fail, 1 pass). SYN-A-02: the network failure is excluded, so the item has only one counted trial and is dropped.
        self.assertEqual((lat["n_items"], lat["trials"], lat["passes"]), (1, 2, 1))
        self.assertEqual(lat["bank_item_ids"], ["SYN-A-01"])
        self.assertEqual(lat["reliability"]["status_counts"], {"refusal": 1, "ok": 2})
        self.assertEqual(lat["reliability"]["error_classes"], [{"class": "moderation_block", "n": 1}])
        self.assertAlmostEqual(lat["reliability"]["refusal_rate"], 1 / 3)
        self.assertEqual([x["item_id"] for x in lat["items_excluded"]], ["SYN-A-02"])
        self.assertEqual([(e["trial_id"], e["reason"].split(":")[0]) for e in lat["excluded_trials"]], [("SYN-A-02__r-vx__core__r1", "infrastructure_fault")])
        self.assertIn("moderation_block", json.dumps(lat["trial_verdicts"]))
        # format rows: no item of r-vx has two artifacts -> no row, and the reason names the refusal
        self.assertEqual(self.rows(res, "delivery_format_compliance", "r-vx"), [])
        unw = [u for u in res["unwritten"] if u["capability"] == "delivery_format_compliance" and "r-vx" in u["cell_id"]]
        self.assertEqual(len(unw), 1)
        self.assertEqual(unw[0]["absence_reason"], "refused")
        self.assertEqual(sorted(x["item_id"] for x in unw[0]["items_excluded"]), ["SYN-A-01", "SYN-A-02"])
        self.assertEqual(self.rows(res, "reproducibility", "r-vx"), [])

    def test_pre_dispatch_refusal_and_never_dispatched_are_excluded_not_trials(self):
        run = SyntheticRun(self.tmp / "runs2", "syn-2")
        run.add("SYN-A-01", "r-fal", 1, size=(40, 50), seed=1)
        run.add("SYN-A-01", "r-fal", 2, outcome="pre_dispatch")
        run.add("SYN-A-02", "r-fal", 1, size=(40, 40), seed=2)
        run.add("SYN-A-02", "r-fal", 2, size=(40, 40), seed=3)
        spec, _ = run.commit()
        res = RR.build_rows([spec], book=self.book, harness_root=self.tmp / "hz2")
        (lat,) = self.rows(res, "latency_errors_refusals", "r-fal")
        self.assertEqual((lat["n_items"], lat["trials"]), (1, 2))
        self.assertEqual(lat["bank_item_ids"], ["SYN-A-02"])
        self.assertEqual([e["reason"].split(":")[0] for e in lat["excluded_trials"]], ["pre_dispatch_refusal"])
        classified = {t["trial_id"]: t["status"] for t in res["runs"][0].trials}
        self.assertEqual(classified["SYN-A-01__r-fal__core__r2"], "excluded")

    def test_non_deterministic_capability_is_refused_on_every_path(self):
        res = self.build()
        cell = next(c for c in res["cells"].values() if c["route_key"] == "r-fal")
        insts = RR.frozen_instruments()
        with self.assertRaises(RG.RegistryGateRefused):
            RR.write_cell_rows(cell, insts, self.tmp / "hz-rogue", res["criteria_sha256"], capabilities=("exact_text_devanagari",))
        hz = RR.RegistryHarness(self.tmp / "hz-rogue2")
        for iid, inst in insts.items():
            hz.register_instrument(inst)
        with self.assertRaises(RG.RegistryGateRefused):
            hz.registry_row_for("exact_text_devanagari", "format_probe", [], {}, 1, 2)
        with self.assertRaises(RG.RegistryGateRefused):
            hz.write_registry_row("hierarchy_product_as_hero", "ledger_metrics", [], {}, 1, 2)
        self.assertEqual(set(RR.CAPABILITIES) - RG.deterministic_capabilities(), set(), "registry_rows measures only EVALUATOR-PLAN deterministic capabilities")

    def test_registry_harness_never_overrides_the_writer(self):
        self.assertTrue(issubclass(RR.RegistryHarness, BH.BatteryHarness))
        self.assertNotIn("write_registry_row", RR.RegistryHarness.__dict__)
        self.assertNotIn("registry_row_for", RR.RegistryHarness.__dict__)
        self.assertTrue(RR.RegistryHarness.write_registry_row is BH.BatteryHarness.write_registry_row)

    def test_frozen_instruments_refuse_an_unfrozen_criteria_file(self):
        d = yaml.safe_load(Path(hv2_paths.HERE / "instruments" / "PASS-CRITERIA-v0.yaml").read_text())
        d["criteria"]["format_probe"]["frozen"] = False
        p = self.tmp / "unfrozen.yaml"
        p.write_text(yaml.safe_dump(d, allow_unicode=True, sort_keys=False))
        with self.assertRaises(RR.RegistryRowsError):
            RR.frozen_instruments(p)

    def test_dry_mode_writes_nothing(self):
        before = self.registry.read_bytes()
        rc = RR.main(["--run", self.spec, "--registry", str(self.registry), "--harness-root", str(self.tmp / "hz-cli")], book=self.book)
        self.assertEqual(rc, 0)
        self.assertEqual(self.registry.read_bytes(), before)
        self.assertFalse((hv2_paths.EVAL_ROOT / "registry" / "registry-v1.jsonl").read_text().count("SYN-A"), "the committed registry is never touched by a test")

    def test_write_appends_rows_the_validator_accepts_and_never_twice(self):
        spec = importlib.util.spec_from_file_location("validate_registry", hv2_paths.EVAL_ROOT / "registry" / "validate_registry.py")
        V = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(V)
        dump = self.tmp / "records.jsonl"
        rc = RR.main(["--run", self.spec, "--registry", str(self.registry), "--harness-root", str(self.tmp / "hz-w"), "--write", "--json", str(dump)], book=self.book)
        self.assertEqual(rc, 0)
        lines = [l for l in self.registry.read_text().splitlines() if l.strip() and not l.startswith("#")]
        self.assertEqual(len(lines), 7, "5 capabilities on r-fal + 2 ledger capabilities on r-vx")
        crit_sha = hashlib.sha256((hv2_paths.HERE / "instruments" / "PASS-CRITERIA-v0.yaml").read_bytes()).hexdigest()
        ids = set()
        for l in lines:
            r = json.loads(l)
            for k in V.REQUIRED_ROW:
                self.assertIn(k, r, f"row {r.get('entry_id')} lacks {k}")
            for k in ("status", "method", "interval_low", "interval_high", "computed_over", "assumptions", "independence_status", "is_reference_calculation_only"):
                self.assertIn(k, r["uncertainty"])
            self.assertIs(r["synthetic"], False)
            self.assertEqual(r["criteria_sha256"], crit_sha)
            self.assertEqual(r["evidence_tier"], "deterministic")
            self.assertEqual(r["run_ids"], ["syn-run"])
            self.assertEqual(r["runs"][0]["plan_sha256"], self.plan_sha)
            self.assertEqual(r["instrument"]["calibration_status"], "deterministic")
            self.assertTrue(r["instrument"]["config_hash"])
            self.assertIn(r["capability"], RG.deterministic_capabilities())
            ids.add(r["entry_id"])
        self.assertEqual(len(ids), 7, "entry ids are unique across cells")
        self.assertEqual(len([l for l in dump.read_text().splitlines() if l.strip()]), 7)
        with self.assertRaises(RR.RegistryRowsError):
            RR.main(["--run", self.spec, "--registry", str(self.registry), "--harness-root", str(self.tmp / "hz-w2"), "--write"], book=self.book)
        self.assertEqual(len([l for l in self.registry.read_text().splitlines() if l.strip() and not l.startswith("#")]), 7)
        with self.assertRaises(RR.RegistryRowsError):
            RR.append_records(self.registry, [{"entry_id": "cap-x", "synthetic": True, "evidence_tier": "deterministic"}])
        with self.assertRaises(RR.RegistryRowsError):
            RR.append_records(self.registry, [{"entry_id": "cap-y", "synthetic": False, "evidence_tier": "human_blind_acceptance"}])

    def test_plan_tampering_is_refused(self):
        p = self.run.out / "PLAN.yaml"
        p.write_text(p.read_text().replace("r-fal", "r-tampered", 1))
        import run_live as RL
        with self.assertRaises(RL.PlanRefused):
            RR.Run.from_spec(self.spec)


if __name__ == "__main__":
    unittest.main()
