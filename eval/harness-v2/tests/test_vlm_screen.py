"""VLM screening (2026-09-09): GeminiApiTransport, instruments/vlm_screen.py, qualify_screen.py and the screened tier of evidence_map.py.

Proven here, with FakeTransport only (no socket, no key, no Gemini call):
    - the transport is a plain urllib POST to models/{model}:generateContent with `x-goog-api-key`; construction opens nothing;
      a live call hits the no-network guard; FakeTransport stands in through post_json alone;
    - the instrument is screened_not_qualified: registry_gate refuses it for every deterministic capability, registry_writable
      is False, and the prompt / model / criteria sha are inside config_hash;
    - canned JSON -> per-rule verdicts + an overall derived in code by the Controller's rule; a malformed answer is
      parse_failure; a 4xx / refusal / transport failure is absent; the key value never reaches a result or the body;
      a session with no call budget sends nothing; video sends 3 frames; audio is cannot_judge at USD 0;
    - Cohen's kappa on a known table; the qualification verdict stays screened_not_qualified while the criteria file is
      unfrozen and reports would_verdict;
    - the runner on a synthetic sealed run in a temp dir: --dry-run prints the plan and "price not pinned" and makes no call;
      a live run refuses without --auth, with screen_cap_usd 0, and without a pinned price; with a temp pin index and a
      FakeTransport it writes SCREEN-RESULTS.yaml + QUALIFICATION-REPORT.yaml and stops at the cap;
    - evidence_map fills the screened_not_qualified tier from SCREEN-RESULTS (n, agreement, config hash, status) and the
      status is `qualified` only under a binding QUALIFICATION-REPORT; registry stays False either way.
Nothing here writes under eval/experiments/ or eval/registry/.
"""
import json
import re
import shutil
import unittest
from pathlib import Path

import yaml

from _support import NoNetworkTestCase, NetworkAttempted, hv2_paths
import evidence_map as EM
import harness as H
import qualify_screen as QS
import store as S
import transports as T
from instruments import imageio as IO
from instruments import registry_gate as RG
from instruments import vlm_screen as VS

HAVE_FFMPEG = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))
CANARY = "FAKE-GOOGLE-KEY-CANARY-0123456789"
CONTRACT = ["ACCEPT only if the picture is a solid red square.",
            "REJECT if any lettering or pseudo-lettering appears.",
            "ACCEPT only if nothing is cut by the frame edge; REJECT if two elements overlap."]


def answer(verdicts, evidence="seen", usage=(300, 40)):
    rules = [{"rule_id": f"R{i}", "verdict": v, "evidence": f"{evidence} {i}"} for i, v in enumerate(verdicts, 1)]
    return (200, {"candidates": [{"content": {"parts": [{"text": json.dumps({"rules": rules})}]}, "finishReason": "STOP"}],
                  "usageMetadata": {"promptTokenCount": usage[0], "candidatesTokenCount": usage[1], "totalTokenCount": sum(usage)}})


def png_bytes(w=8, h=8, rgb=(255, 0, 0)):
    return IO.encode_png([bytes(rgb) * w for _ in range(h)], w, h)


def key_reader(name):
    assert name == VS.KEY_NAME
    return CANARY


class GeminiTransportTest(NoNetworkTestCase):
    def test_construction_opens_nothing_and_a_live_call_hits_the_guard(self):
        t = T.GeminiApiTransport()
        self.assertEqual((t.name, t.calls), ("gemini_api", 0))
        with self.assertRaises(NetworkAttempted):
            t.generate_content("gemini-3.1-flash", {"contents": []}, CANARY)

    def test_url_is_generate_content_on_the_developer_api(self):
        self.assertEqual(T.gemini_generate_content_url("gemini-3.1-flash"),
                         "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash:generateContent")
        for bad in ("", "models/x", "a:b", "a b"):
            with self.assertRaises(Exception):
                T.gemini_generate_content_url(bad)

    def test_fake_transport_stands_in_and_the_key_rides_only_in_the_header(self):
        ft = T.FakeTransport(posts=[answer(["pass", "pass", "pass"])])
        inst = VS.instrument(transport=ft, key_reader=key_reader, max_calls=1)
        p = self.tmp / "a.png"
        p.write_bytes(png_bytes())
        r = inst.fn(p, {"instrument_inputs": {"acceptance_contract": CONTRACT}}, "acceptance_contract_screen")
        self.assertEqual(r["verdict"], "pass")
        call = ft.calls[0]
        self.assertEqual(call["kind"], "post")
        self.assertTrue(call["url"].endswith("/models/gemini-3.1-flash:generateContent"))
        self.assertEqual(call["headers"], {"x-goog-api-key": CANARY})
        self.assertNotIn(CANARY.encode(), call["payload"])
        body = json.loads(call["payload"])
        self.assertEqual(body["generationConfig"]["temperature"], 0)
        self.assertEqual(body["generationConfig"]["responseMimeType"], "application/json")
        self.assertIn("responseSchema", body["generationConfig"])
        parts = body["contents"][0]["parts"]
        self.assertEqual(len(parts), 2)
        self.assertIn("R1 [accept_only]", parts[0]["text"])
        self.assertIn("R3 [mixed]", parts[0]["text"])
        self.assertEqual(parts[1]["inlineData"]["mimeType"], "image/png")

    def test_hygiene_new_modules_import_no_network_module(self):
        for mod in (VS, QS):
            src = Path(mod.__file__).read_text()
            for pat in ("url" + "lib", "http\\." + "client", "sock" + "et", "requ" + "ests"):
                self.assertIsNone(re.search(r"^\s*(import|from)\s+" + pat + r"\b", src, re.M), (mod.__name__, pat))


class InstrumentTest(NoNetworkTestCase):
    def setUp(self):
        super().setUp()
        self.png = self.tmp / "red.png"
        self.png.write_bytes(png_bytes())

    def run_one(self, posts, contract=CONTRACT, max_calls=1, **kw):
        ft = T.FakeTransport(posts=posts)
        inst = VS.instrument(transport=ft, key_reader=key_reader, max_calls=max_calls, **kw)
        return inst, ft, inst.fn(self.png, {"instrument_inputs": {"acceptance_contract": contract}}, "acceptance_contract_screen")

    def test_status_is_screened_not_qualified_and_the_gate_refuses_it(self):
        inst = VS.instrument(transport=T.FakeTransport())
        self.assertIsInstance(inst, H.Instrument)
        self.assertEqual(inst.qualification_status, "screened_not_qualified")
        self.assertFalse(inst.registry_writable)
        for cap in sorted(RG.deterministic_capabilities()):
            with self.subTest(capability=cap), self.assertRaises(RG.RegistryGateRefused):
                RG.assert_registry_eligible(cap, inst)
        with self.assertRaises(RG.RegistryGateRefused):
            RG.assert_registry_eligible("acceptance_contract_screen", inst)
        self.assertEqual(inst.config["qualification_status"], "screened_not_qualified")
        self.assertFalse(inst.config["criteria_frozen"], "SCREEN-QUALIFICATION-CRITERIA-v0.yaml is unfrozen")

    def test_config_hash_covers_prompt_model_and_criteria(self):
        base = VS.instrument(transport=T.FakeTransport())
        self.assertEqual(base.config["model"], "gemini-3.1-flash")
        self.assertIn(VS.PROMPT_TEMPLATE, base.config["prompt_template"])
        self.assertNotEqual(VS.instrument(transport=T.FakeTransport(), model="other-model").config_hash, base.config_hash)
        self.assertNotEqual(VS.instrument(transport=T.FakeTransport(), prompt_template=VS.PROMPT_TEMPLATE + "\nextra").config_hash, base.config_hash)
        alt = self.tmp / "crit.yaml"
        doc = yaml.safe_load(Path(VS.CRITERIA_PATH).read_text())
        doc["thresholds"]["cohens_kappa_min"] = 0.7
        alt.write_text(yaml.safe_dump(doc))
        self.assertNotEqual(VS.instrument(transport=T.FakeTransport(), criteria_path=alt).config_hash, base.config_hash)
        self.assertEqual(VS.instrument(transport=T.FakeTransport()).config_hash, base.config_hash)

    def test_contract_parsing_and_the_controllers_overall_rule(self):
        rules = VS.parse_contract(CONTRACT)
        self.assertEqual([r["rule_id"] for r in rules], ["R1", "R2", "R3"])
        self.assertEqual([r["kind"] for r in rules], ["accept_only", "reject", "mixed"])
        self.assertEqual(VS.derive_overall([{"verdict": "pass"}, {"verdict": "pass"}]), "accept")
        self.assertEqual(VS.derive_overall([{"verdict": "pass"}, {"verdict": "fail"}]), "reject")
        self.assertEqual(VS.derive_overall([{"verdict": "cannot_judge"}, {"verdict": "fail"}]), "reject", "a failing REJECT line rejects even with an unjudged line")
        self.assertEqual(VS.derive_overall([{"verdict": "pass"}, {"verdict": "cannot_judge"}]), "cannot_judge")
        self.assertEqual(VS.derive_overall([]), "cannot_judge")
        with self.assertRaises(VS.ScreenError):
            VS.parse_contract([])

    def test_canned_json_accept_reject_and_cannot_judge(self):
        _, _, r = self.run_one([answer(["pass", "pass", "pass"])])
        self.assertEqual((r["verdict"], r["overall"], r["absence_reason"]), ("pass", "accept", None))
        self.assertEqual([x["verdict"] for x in r["rules"]], ["pass"] * 3)
        self.assertEqual(r["rules"][1]["rule"], CONTRACT[1])
        self.assertEqual(r["measurement"]["usage"]["promptTokenCount"], 300)
        _, _, r = self.run_one([answer(["pass", "fail", "cannot_judge"])])
        self.assertEqual((r["verdict"], r["overall"]), ("fail", "reject"))
        self.assertEqual(len(r["defects"]), 1)
        self.assertTrue(r["defects"][0]["term"].startswith("R2 fail"))
        _, _, r = self.run_one([answer(["pass", "cannot_judge", "pass"])])
        self.assertEqual((r["verdict"], r["overall"], r["absence_reason"]), ("absent", "cannot_judge", "other"))

    def test_missing_rule_ids_are_cannot_judge_never_pass(self):
        rules = [{"rule_id": "R1", "verdict": "pass", "evidence": "x"}]
        posts = [(200, {"candidates": [{"content": {"parts": [{"text": json.dumps({"rules": rules})}]}, "finishReason": "STOP"}]})]
        _, _, r = self.run_one(posts)
        self.assertEqual(r["overall"], "cannot_judge")
        self.assertEqual([x["verdict"] for x in r["rules"]], ["pass", "cannot_judge", "cannot_judge"])

    def test_malformed_answers_are_parse_failure(self):
        bad = [
            (200, {"candidates": [{"content": {"parts": [{"text": "not json at all"}]}, "finishReason": "STOP"}]}),
            (200, {"candidates": [{"content": {"parts": [{"text": json.dumps({"nope": 1})}]}, "finishReason": "STOP"}]}),
            (200, {"candidates": [{"content": {"parts": [{"text": json.dumps({"rules": [{"rule_id": "R1", "verdict": "maybe", "evidence": ""}]})}]}, "finishReason": "STOP"}]}),
            (200, "a bare string"),
        ]
        for posts in bad:
            with self.subTest(answer=str(posts)[:60]):
                _, _, r = self.run_one([posts])
                self.assertEqual((r["verdict"], r["absence_reason"]), ("absent", "parse_failure"))
                self.assertNotIn("overall", r)

    def test_http_errors_refusals_and_transport_failures_are_absent_and_scrubbed(self):
        cases = [
            ((429, {"error": {"status": "RESOURCE_EXHAUSTED", "message": f"quota for {CANARY}"}}), "instrument_unavailable", "http 429"),
            ((400, {"error": {"status": "INVALID_ARGUMENT", "message": "bad request"}}), "other", "http 400"),
            ((403, {"error": {"status": "PERMISSION_DENIED", "message": "denied"}}), "instrument_unavailable", "http 403"),
            ((200, {"promptFeedback": {"blockReason": "SAFETY"}}), "other", "model refusal"),
            ((200, {"candidates": [{"content": {"parts": [{"text": ""}]}, "finishReason": "SAFETY"}]}), "other", "model refusal"),
            ((200, {"candidates": []}), "other", "model refusal"),
            (RuntimeError(f"socket said {CANARY}"), "instrument_unavailable", "transport failure"),
        ]
        for post, reason, prefix in cases:
            with self.subTest(case=prefix + " " + str(post)[:40]):
                _, ft, r = self.run_one([post])
                self.assertEqual((r["verdict"], r["absence_reason"]), ("absent", reason))
                self.assertTrue(r["note"].startswith(prefix), r["note"])
                self.assertNotIn(CANARY, json.dumps(r))
                self.assertEqual(ft.submits, 1, "0 retries")

    def test_no_call_budget_sends_nothing(self):
        inst, ft, r = self.run_one([answer(["pass"] * 3)], max_calls=0)
        self.assertEqual((r["verdict"], r["absence_reason"]), ("absent", "not_measured"))
        self.assertEqual(ft.calls, [])
        self.assertEqual(inst.session.calls, 0)

    def test_missing_key_is_unavailable_before_any_send(self):
        ft = T.FakeTransport(posts=[answer(["pass"] * 3)])
        inst = VS.instrument(transport=ft, max_calls=1)                    # default reader: env stripped, throw-away key file empty
        r = inst.fn(self.png, {"acceptance_contract": CONTRACT}, "x")
        self.assertEqual((r["verdict"], r["absence_reason"]), ("absent", "instrument_unavailable"))
        self.assertIn("GOOGLE_API_KEY", r["note"])
        self.assertEqual(ft.calls, [])
        self.write_fake_key("GOOGLE_API_KEY", CANARY)
        r = VS.instrument(transport=ft, max_calls=1).fn(self.png, {"acceptance_contract": CONTRACT}, "x")
        self.assertEqual(r["verdict"], "pass")
        self.assertEqual(ft.calls[0]["headers"]["x-goog-api-key"], CANARY)
        with self.assertRaises(Exception):
            VS.read_key_by_name("FAL_KEY")

    def test_no_contract_or_missing_file_fails_closed(self):
        inst = VS.instrument(transport=T.FakeTransport(posts=[answer(["pass"] * 3)]), key_reader=key_reader, max_calls=1)
        r = inst.fn(self.png, {"instrument_inputs": {}}, "x")
        self.assertEqual((r["verdict"], r["absence_reason"]), ("absent", "parse_failure"))
        r = inst.fn(self.tmp / "missing.png", {"acceptance_contract": CONTRACT}, "x")
        self.assertEqual((r["verdict"], r["absence_reason"]), ("absent", "parse_failure"))
        self.assertEqual(inst.session.calls, 0)

    def test_audio_is_cannot_judge_at_no_cost(self):
        wav = self.tmp / "a.wav"
        IO.write_wav(wav, [0] * 1600)
        inst, ft, _ = self.run_one([answer(["pass"] * 3)])
        r = inst.fn(wav, {"acceptance_contract": CONTRACT}, "x")
        self.assertEqual((r["verdict"], r["overall"], r["absence_reason"]), ("absent", "cannot_judge", "other"))
        self.assertEqual([x["verdict"] for x in r["rules"]], ["cannot_judge"] * 3)
        self.assertEqual(r["measurement"]["calls"], 0)
        self.assertEqual(ft.submits, 1, "only the image call from run_one; the audio made none")

    @unittest.skipUnless(HAVE_FFMPEG, "ffmpeg not installed")
    def test_video_sends_three_sampled_frames(self):
        mp4 = IO.make_test_video(self.tmp / "v.mp4", 64, 48, 1.0, 10)
        ft = T.FakeTransport(posts=[answer(["pass", "pass", "pass"])])
        inst = VS.instrument(transport=ft, key_reader=key_reader, max_calls=1, frame_max_side=32)
        r = inst.fn(mp4, {"acceptance_contract": CONTRACT}, "x")
        self.assertEqual(r["verdict"], "pass")
        frames = r["measurement"]["frames"]
        self.assertEqual(len(frames), 3)
        self.assertEqual(frames[0]["frame_index"], 0)
        self.assertGreater(frames[1]["frame_index"], frames[0]["frame_index"])
        self.assertGreater(frames[2]["frame_index"], frames[1]["frame_index"])
        self.assertLessEqual(max(frames[0]["width"], frames[0]["height"]), 32, "frames are downscaled to frame_max_side")
        self.assertEqual(frames[0]["source_width"], 64)
        parts = json.loads(ft.calls[0]["payload"])["contents"][0]["parts"]
        self.assertEqual(sum(1 for p in parts if "inlineData" in p), 3)
        self.assertIn("frames of one video clip", parts[0]["text"])


class StatisticsTest(NoNetworkTestCase):
    def test_cohens_kappa_on_a_known_table(self):
        pairs = [("accept", "accept")] * 20 + [("accept", "reject")] * 5 + [("reject", "accept")] * 10 + [("reject", "reject")] * 15
        s = QS.agreement_stats(pairs)
        self.assertEqual(s["n_compared"], 50)
        self.assertAlmostEqual(s["agreement_rate"], 0.7)
        self.assertAlmostEqual(s["cohens_kappa"], 0.4)                # po 0.70, pe 0.50
        self.assertAlmostEqual(s["false_accept_rate"], 0.4)           # 10 of 25 Controller rejects accepted by the screen
        self.assertAlmostEqual(s["false_reject_rate"], 0.2)
        self.assertEqual(s["confusion_controller_x_screen"], {"accept": {"accept": 20, "reject": 5}, "reject": {"accept": 10, "reject": 15}})
        self.assertEqual(QS.agreement_stats([("accept", "accept")] * 4 + [("reject", "reject")] * 4)["cohens_kappa"], 1.0)
        self.assertEqual(QS.agreement_stats([("accept", "accept")] * 4)["cohens_kappa"], 1.0, "all-accept both sides: pe 1, po 1")
        self.assertIsNone(QS.agreement_stats([])["cohens_kappa"])
        self.assertIsNone(QS.agreement_stats([("accept", "accept")])["false_accept_rate"])

    def test_qualification_stays_screened_not_qualified_while_unfrozen(self):
        crit = VS.load_criteria()
        good = QS.agreement_stats([("accept", "accept")] * 25 + [("reject", "reject")] * 24 + [("reject", "accept")])
        q = QS.qualification(good, {"coverage_fraction": 0.95}, crit)
        self.assertEqual(q["qualification_verdict"], "screened_not_qualified")
        self.assertEqual(q["would_verdict"], "qualified")
        self.assertFalse(q["criteria_frozen"])
        self.assertFalse(q["binding"])
        frozen = dict(crit, _frozen=True)
        self.assertEqual(QS.qualification(good, {"coverage_fraction": 0.95}, frozen)["qualification_verdict"], "qualified")
        bad = QS.agreement_stats([("accept", "accept")] * 20 + [("reject", "accept")] * 20 + [("reject", "reject")] * 10)
        self.assertEqual(QS.qualification(bad, {"coverage_fraction": 0.95}, frozen)["would_verdict"], "screened_not_qualified")
        small = QS.agreement_stats([("accept", "accept")] * 5 + [("reject", "reject")] * 5)
        self.assertEqual(QS.qualification(small, {"coverage_fraction": 1.0}, frozen)["would_verdict"], "insufficient_n")
        self.assertEqual(QS.qualification(good, {"coverage_fraction": 0.5}, frozen)["would_verdict"], "screened_not_qualified")


class SyntheticJudgedRun:
    """A sealed run in the temp dir: artifacts/media/<trial>.png + record + RESULTS.yaml, plus a two-case TEST-CASES.yaml."""

    def __init__(self, root: Path, run_id="syn-screen"):
        self.out = root / "runs" / run_id
        self.run_id = run_id
        self.store = S.SealedStore(self.out / "artifacts")
        self.trials = []

    def add(self, case_id, route, rep, verdict, note="", kind="png", arm="core"):
        tid = f"{case_id}__{route}__{arm}__r{rep}"
        seed = len(self.trials) + 1
        if kind == "png":
            self.store.seal(tid, png_bytes(8, 8, (seed * 30 % 256, 0, 0)), "image/png")
        elif kind == "wav":
            p = self.out / "artifacts" / "media" / f"{tid}.wav"
            p.parent.mkdir(parents=True, exist_ok=True)
            IO.write_wav(p, [0] * 800)
        self.trials.append({"trial_id": tid, "run_id": self.run_id, "case_id": case_id, "question": case_id.rsplit("-", 1)[0], "route_key": route, "arm": arm,
                            "repeat_index": rep, "dispatched": True, "status": "ok", "verdict": verdict, "verdict_basis": "blind_verdict", "note": note})
        return tid

    def commit(self):
        doc = {"run_id": self.run_id, "revealed_utc": "2026-09-09T10:00:00Z", "commitment_verified": True, "rules_ref": "rules.md", "trials": self.trials, "elimination": []}
        p = self.out / "RESULTS.yaml"
        p.write_text(yaml.safe_dump(doc, sort_keys=False))
        return p


def write_cases(path: Path):
    cases = [{"case_id": "SYN-A-01", "item_id": "SYN-A-01", "lane": "IMG", "acceptance_contract": CONTRACT},
             {"case_id": "SYN-A-02", "item_id": "SYN-A-02", "lane": "IMG", "acceptance_contract": CONTRACT[:2]},
             {"case_id": "SYN-S-01", "item_id": "SYN-S-01", "lane": "AUD", "acceptance_contract": ["ACCEPT only if one voice is heard."]}]
    path.write_text(yaml.safe_dump({"cases": cases}, allow_unicode=True))
    return path


def write_pin_index(path: Path, complete=True):
    entry = {"route_key": "gemini-api-judge", "pin_kind": "price", "url": "https://example.invalid/pricing", "fetched_utc": "2026-09-09T00:00:00Z", "sha256": "0" * 64}
    if complete:
        entry.update({"usd_per_1m_input_tokens": 0.30, "usd_per_1m_output_tokens": 2.50, "tokens_per_image": 258})
    path.write_text(yaml.safe_dump([entry]))
    return path


class RunnerTest(NoNetworkTestCase):
    def setUp(self):
        super().setUp()
        run = SyntheticJudgedRun(self.tmp)
        run.add("SYN-A-01", "alpha", 1, "accept")
        run.add("SYN-A-01", "alpha", 2, "reject", note="lettering appeared")
        run.add("SYN-A-02", "alpha", 1, "accept")
        run.add("SYN-A-02", "beta", 1, "reject", note="cut off")
        run.add("SYN-S-01", "voice", 1, "accept", kind="wav")
        self.results = run.commit()
        self.run = run
        self.cases = write_cases(self.tmp / "TEST-CASES.yaml")
        self.out = []

    def log(self, s):
        self.out.append(str(s))

    def base_args(self, *extra):
        return ["--results", str(self.results), "--test-cases", str(self.cases), "--runs-root", str(self.tmp / "runs"), *extra]

    def test_plan_resolves_artifacts_and_kinds(self):
        rows = QS.plan_trials([self.results], QS.load_cases(self.cases), self.tmp / "runs")
        self.assertEqual(len(rows), 5)
        self.assertEqual([r["calls"] for r in rows], [1, 1, 1, 1, 0])
        self.assertEqual(rows[4]["media_kind"], "audio")
        self.assertTrue(rows[4]["skip"].startswith("audio"))
        self.assertEqual(rows[0]["n_rules"], 3)
        self.assertTrue(Path(rows[0]["artifact"]).name.endswith(".png"))

    def test_dry_run_prints_the_plan_and_price_not_pinned_and_sends_nothing(self):
        exploding = T.FakeTransport()            # no scripted answers: any post would raise AssertionError
        # the repo now carries a real Gemini price pin (2026-09-09), so point at an absent index to exercise "price not pinned"
        rc = QS.main(self.base_args("--dry-run", "--pin-index", str(self.tmp / "NO-PIN-INDEX.yaml")), transport=exploding, key_reader=key_reader, log=self.log)
        self.assertEqual(rc, 0)
        text = "\n".join(self.out)
        self.assertIn("NOTHING IS SENT", text)
        self.assertIn("calls   4", text)
        self.assertIn("audio cannot_judge  1", text)
        self.assertIn("price not pinned", text)
        self.assertNotRegex(text, r"USD \d")
        self.assertEqual(exploding.calls, [])
        self.assertFalse((self.tmp / "runs" / "syn-screen" / "SCREEN-RESULTS.yaml").exists())

    def test_dry_run_prices_only_from_a_complete_pin(self):
        idx = write_pin_index(self.tmp / "PIN-INDEX.yaml", complete=True)
        QS.main(self.base_args("--dry-run", "--pin-index", str(idx)), transport=T.FakeTransport(), log=self.log)
        self.assertRegex("\n".join(self.out), r"cost estimate at the pinned price .*USD \d")
        self.out.clear()
        idx2 = write_pin_index(self.tmp / "PIN-INDEX-partial.yaml", complete=False)
        QS.main(self.base_args("--dry-run", "--pin-index", str(idx2)), transport=T.FakeTransport(), log=self.log)
        self.assertIn("price not pinned", "\n".join(self.out))

    def test_live_refuses_without_auth_with_zero_cap_and_without_a_pin(self):
        exploding = T.FakeTransport()
        rc = QS.main(self.base_args("--out", str(self.tmp / "R.yaml")), transport=exploding, key_reader=key_reader, log=self.log)
        self.assertEqual(rc, 2)
        self.assertIn("REFUSED", self.out[-1])
        self.assertIn("--auth", self.out[-1])
        zero = self.tmp / "auth0.yaml"
        zero.write_text(yaml.safe_dump({"screen_authorisation": {"screen_cap_usd": 0}}))
        rc = QS.main(self.base_args("--auth", str(zero), "--out", str(self.tmp / "R.yaml")), transport=exploding, key_reader=key_reader, log=self.log)
        self.assertEqual(rc, 2)
        self.assertIn("forbidden", self.out[-1])
        nocap = self.tmp / "auth-nocap.yaml"
        nocap.write_text(yaml.safe_dump({"screen_authorisation": {"approved_by": "x"}}))
        rc = QS.main(self.base_args("--auth", str(nocap), "--out", str(self.tmp / "R.yaml")), transport=exploding, key_reader=key_reader, log=self.log)
        self.assertEqual(rc, 2)
        cap = self.tmp / "auth.yaml"
        cap.write_text(yaml.safe_dump({"screen_authorisation": {"screen_cap_usd": 1.0}}))
        rc = QS.main(self.base_args("--auth", str(cap), "--out", str(self.tmp / "R.yaml"), "--pin-index", str(self.tmp / "NO-PIN-INDEX.yaml")), transport=exploding, key_reader=key_reader, log=self.log)
        self.assertEqual(rc, 2)
        self.assertIn("price not pinned", self.out[-1])
        self.assertEqual(exploding.calls, [])
        self.assertFalse((self.tmp / "R.yaml").exists())

    def test_live_with_fake_transport_writes_screen_results_and_report(self):
        idx = write_pin_index(self.tmp / "PIN-INDEX.yaml")
        auth = self.tmp / "auth.yaml"
        auth.write_text(yaml.safe_dump({"screen_authorisation": {"screen_cap_usd": 1.0, "approved_by": "test-fixture", "approved_at": "2026-09-09"}}))
        # trial order: A-01 r1 accept, A-01 r2 reject, A-02 r1 accept, A-02 beta reject; screen answers: agree, agree, DISAGREE (reject), agree
        ft = T.FakeTransport(posts=[answer(["pass", "pass", "pass"]), answer(["pass", "fail", "pass"]), answer(["fail", "pass"]), answer(["pass", "fail"])])
        report = self.tmp / "screening" / "QUALIFICATION-REPORT.yaml"
        rc = QS.main(self.base_args("--auth", str(auth), "--pin-index", str(idx), "--out", str(report), "--screen-out-dir", str(self.tmp / "screens")),
                     transport=ft, key_reader=key_reader, log=self.log)
        self.assertEqual(rc, 0, self.out)
        self.assertEqual(ft.submits, 4)
        self.assertTrue(all(c["headers"] == {"x-goog-api-key": CANARY} for c in ft.calls))
        sr_path = self.tmp / "screens" / "syn-screen" / "SCREEN-RESULTS.yaml"
        sr = yaml.safe_load(sr_path.read_text())
        self.assertEqual(sr["schema"], "SCREEN-RESULTS-v0")
        self.assertEqual(sr["run_id"], "syn-screen")
        self.assertIs(sr["registry"], False)
        self.assertEqual(sr["instrument"]["qualification_status"], "screened_not_qualified")
        self.assertEqual(len(sr["instrument"]["config_hash"]), 64)
        self.assertEqual([t["screen_overall"] for t in sr["trials"]], ["accept", "reject", "reject", "reject", "cannot_judge"])
        self.assertEqual([t["agree"] for t in sr["trials"]], [True, True, False, True, None])
        self.assertEqual(sr["trials"][1]["rules"][1]["verdict"], "fail")
        self.assertEqual(sr["trials"][4]["media_kind"], "audio")
        self.assertNotIn(CANARY, sr_path.read_text())
        rep = yaml.safe_load(report.read_text())
        self.assertEqual(rep["schema"], "QUALIFICATION-REPORT-v0")
        self.assertEqual(rep["agreement"]["n_compared"], 4)
        self.assertEqual(rep["agreement"]["agree"], 3)
        self.assertEqual(rep["agreement"]["false_accepts"], 0)
        self.assertEqual(rep["agreement"]["false_rejects"], 1)
        self.assertEqual(rep["coverage"]["audio_planned_cannot_judge"], 1)
        self.assertEqual(rep["coverage"]["coverage_fraction"], 1.0)
        self.assertEqual(set(rep["per_question"]), {"SYN-A"})
        self.assertEqual(set(rep["per_route"]), {"alpha", "beta"})
        self.assertEqual(rep["per_route"]["alpha"]["confusion_controller_x_screen"], {"accept": {"accept": 1, "reject": 1}, "reject": {"accept": 0, "reject": 1}})
        self.assertEqual(len(rep["disagreements"]), 1)
        self.assertEqual(rep["disagreements"][0]["trial_id"], "SYN-A-02__alpha__core__r1")
        self.assertEqual(rep["disagreements"][0]["screen_rules"][0]["rule_id"], "R1")
        self.assertEqual(rep["qualification"]["qualification_verdict"], "screened_not_qualified")
        self.assertEqual(rep["qualification"]["would_verdict"], "insufficient_n")
        self.assertFalse(rep["qualification"]["criteria_frozen"])
        self.assertEqual(rep["spend"]["calls"], 4)
        self.assertTrue(rep["spend"]["price_pinned"])
        self.assertEqual(rep["spend"]["prompt_tokens"], 1200)
        self.assertRegex(rep["spend"]["usd_at_pinned_price"], r"^0\.\d+$")
        self.assertEqual(rep["instrument"]["config_hash"], sr["instrument"]["config_hash"])
        self.assertNotIn(CANARY, report.read_text())

    def test_live_stops_before_the_call_that_would_cross_the_cap(self):
        idx = write_pin_index(self.tmp / "PIN-INDEX.yaml")
        auth = self.tmp / "auth.yaml"
        # one call is estimated at (258 + 1200) * 0.30 / 1e6 + 400 * 2.5 / 1e6 = 0.0014374 USD; a cap of 0.002 allows exactly one
        auth.write_text(yaml.safe_dump({"screen_authorisation": {"screen_cap_usd": 0.002}}))
        ft = T.FakeTransport(posts=[answer(["pass", "pass", "pass"])] * 4)
        rc = QS.main(self.base_args("--auth", str(auth), "--pin-index", str(idx), "--out", str(self.tmp / "R.yaml"), "--screen-out-dir", str(self.tmp / "s")),
                     transport=ft, key_reader=key_reader, log=self.log)
        self.assertEqual(rc, 0)
        self.assertEqual(ft.submits, 1)
        rep = yaml.safe_load((self.tmp / "R.yaml").read_text())
        self.assertIn("would cross screen_cap_usd", rep["spend"]["stopped"])
        self.assertEqual(rep["spend"]["calls"], 1)
        sr = yaml.safe_load((self.tmp / "s" / "syn-screen" / "SCREEN-RESULTS.yaml").read_text())
        self.assertEqual([t["screen_overall"] for t in sr["trials"]][:2], ["accept", None])
        self.assertEqual(sr["trials"][1]["absence_reason"], "not_measured")

    def test_screen_max_calls_is_a_hard_stop(self):
        idx = write_pin_index(self.tmp / "PIN-INDEX.yaml")
        auth = self.tmp / "auth.yaml"
        auth.write_text(yaml.safe_dump({"screen_authorisation": {"screen_cap_usd": 5, "screen_max_calls": 2}}))
        ft = T.FakeTransport(posts=[answer(["pass", "pass", "pass"])] * 4)
        rc = QS.main(self.base_args("--auth", str(auth), "--pin-index", str(idx), "--out", str(self.tmp / "R.yaml"), "--screen-out-dir", str(self.tmp / "s")),
                     transport=ft, key_reader=key_reader, log=self.log)
        self.assertEqual(rc, 0)
        self.assertEqual(ft.submits, 2)
        rep = yaml.safe_load((self.tmp / "R.yaml").read_text())
        self.assertEqual(rep["spend"]["calls"], 2)
        self.assertEqual(rep["spend"]["stopped_by"], "screen_max_calls")
        self.assertEqual(rep["spend"]["authorised_screen_max_calls"], 2)
        self.assertTrue(rep["spend"]["calls_at_or_above_authorised_limit"])
        self.assertIn("ATTENTION", rep["spend"]["calls_note"])

    # -------------------------------------------------------------- audit finding B (2026-09-10)
    def _live_screen(self, screen_dir="s", max_calls=None):
        idx = write_pin_index(self.tmp / "PIN-INDEX.yaml")
        auth = self.tmp / "auth.yaml"
        a = {"screen_cap_usd": 5.0}
        if max_calls is not None:
            a["screen_max_calls"] = max_calls
        auth.write_text(yaml.safe_dump({"screen_authorisation": a}))
        ft = T.FakeTransport(posts=[answer(["pass", "pass", "pass"])] * 4)
        rc = QS.main(self.base_args("--auth", str(auth), "--pin-index", str(idx), "--out", str(self.tmp / "R.yaml"),
                                    "--screen-out-dir", str(self.tmp / screen_dir)),
                     transport=ft, key_reader=key_reader, log=self.log)
        self.assertEqual(rc, 0, self.out)
        return ft, auth, idx

    def test_a_live_run_persists_its_own_call_counters(self):
        """The live loop's count of calls SENT is written into SCREEN-RESULTS, so nobody has to recompute it later."""
        ft, _, _ = self._live_screen()
        sr = yaml.safe_load((self.tmp / "s" / "syn-screen" / "SCREEN-RESULTS.yaml").read_text())
        c = sr[QS.COUNTERS_KEY]
        self.assertEqual(c["schema"], QS.COUNTERS_SCHEMA)
        self.assertEqual(c["source"], QS.BASIS_LIVE)
        self.assertEqual(c["screening_calls_sent"], 4)
        self.assertEqual(c["screening_calls_sent"], ft.submits, "the counter must equal the calls the transport saw")
        self.assertEqual(c["screening_calls_refused"], 0)
        self.assertIsNone(c["stopped"])
        self.assertIsNone(c["stopped_by"])
        self.assertEqual(len(sr["trials"]), 5, "5 rows for 4 calls: the audio row is cannot_judge with no call")
        self.assertEqual([t["call_sent"] for t in sr["trials"]], [True, True, True, True, False])

    def test_an_offline_rebuild_reports_the_live_count_not_a_row_count(self):
        """Finding B: the September rebuild recomputed `calls` by counting screened rows and printed 206 against a
        200 limit. With a live counter on disk the rebuild must report THAT number - here 4 calls, not 5 rows."""
        self._live_screen()
        rebuilt = self.tmp / "REBUILT.yaml"
        rc = QS.main(self.base_args("--auth", str(self.tmp / "auth.yaml"), "--pin-index", str(self.tmp / "PIN-INDEX.yaml"),
                                    "--out", str(rebuilt), "--report-from-screen-results",
                                    str(self.tmp / "s" / "*" / "SCREEN-RESULTS.yaml")),
                     transport=T.FakeTransport(), key_reader=key_reader, log=self.log)
        self.assertEqual(rc, 0, self.out)
        rep = yaml.safe_load(rebuilt.read_text())
        self.assertEqual(rep["mode"], "rebuilt_offline_from_screen_results")
        self.assertEqual(rep["spend"]["calls"], 4, "the LIVE count")
        self.assertEqual(rep["spend"]["calls_basis"], QS.BASIS_LIVE)
        self.assertEqual(rep["spend"]["screened_rows"], 5, "the row count is reported separately and never as `calls`")

    def test_a_rebuild_without_a_live_counter_says_so_instead_of_printing_a_number(self):
        """Exactly the September situation: SCREEN-RESULTS files written before counters existed."""
        self._live_screen()
        sr_path = self.tmp / "s" / "syn-screen" / "SCREEN-RESULTS.yaml"
        doc = yaml.safe_load(sr_path.read_text())
        doc.pop(QS.COUNTERS_KEY)
        sr_path.write_text(yaml.safe_dump(doc, sort_keys=False))
        rebuilt = self.tmp / "REBUILT2.yaml"
        rc = QS.main(self.base_args("--auth", str(self.tmp / "auth.yaml"), "--pin-index", str(self.tmp / "PIN-INDEX.yaml"),
                                    "--out", str(rebuilt), "--report-from-screen-results", str(sr_path)),
                     transport=T.FakeTransport(), key_reader=key_reader, log=self.log)
        self.assertEqual(rc, 0, self.out)
        rep = yaml.safe_load(rebuilt.read_text())
        self.assertIsNone(rep["spend"]["calls"], "no live counter: print no number at all")
        self.assertEqual(rep["spend"]["calls_basis"], QS.BASIS_MISSING)
        self.assertIn("NOT KNOWN", rep["spend"]["calls_note"])
        self.assertIsNone(rep["spend"]["calls_at_or_above_authorised_limit"])
        self.assertIn("NOT RECORDED", self.out[-1], "the CLI line must not print a number either")

    def test_the_rebuild_states_the_authorised_limit_and_keeps_the_verdict(self):
        self._live_screen(max_calls=4)
        rebuilt = self.tmp / "REBUILT3.yaml"
        rc = QS.main(self.base_args("--auth", str(self.tmp / "auth.yaml"), "--pin-index", str(self.tmp / "PIN-INDEX.yaml"),
                                    "--out", str(rebuilt), "--report-from-screen-results",
                                    str(self.tmp / "s" / "*" / "SCREEN-RESULTS.yaml")),
                     transport=T.FakeTransport(), key_reader=key_reader, log=self.log)
        self.assertEqual(rc, 0, self.out)
        rep = yaml.safe_load(rebuilt.read_text())
        self.assertEqual(rep["spend"]["authorised_screen_max_calls"], 4)
        self.assertTrue(rep["spend"]["calls_at_or_above_authorised_limit"], "4 calls sent against a limit of 4")
        self.assertIn("ATTENTION", rep["spend"]["calls_note"])
        self.assertEqual(rep["qualification"]["qualification_verdict"], "screened_not_qualified",
                         "the qualification verdict logic is untouched by this fix")


def screen_doc(run_id, trials, config_hash="h" * 64, model="gemini-3.1-flash"):
    return {"schema": "SCREEN-RESULTS-v0", "run_id": run_id, "results_ref": f"{run_id}/RESULTS.yaml", "screened_utc": "2026-09-09T12:00:00Z",
            "instrument": {"id": "vlm_screen", "version": "0.1.0", "model": model, "config_hash": config_hash, "qualification_status": "screened_not_qualified"},
            "criteria_sha256": "c" * 64, "registry": False, "trials": trials}


def st(trial_id, question, route, ctrl, scr, note="", arm="core", case_id=None):
    return {"trial_id": trial_id, "case_id": case_id or f"{question}-01", "question": question, "route_key": route, "arm": arm, "controller_verdict": ctrl,
            "controller_note": note, "screen_overall": scr, "agree": (ctrl == scr) if scr in ("accept", "reject") else None, "media_kind": "image", "rules": []}


class EvidenceMapScreenTierTest(NoNetworkTestCase):
    def results(self):
        trials = [{"trial_id": f"Q1-01__alpha__core__r{i}", "run_id": "syn", "case_id": "Q1-01", "question": "Q1", "route_key": "alpha", "arm": "core", "repeat_index": i,
                   "status": "ok", "verdict": v, "verdict_basis": "blind_verdict", "note": ""} for i, v in ((1, "accept"), (2, "reject"))]
        trials += [{"trial_id": "Q1-01__beta__core__r1", "run_id": "syn", "case_id": "Q1-01", "question": "Q1", "route_key": "beta", "arm": "core", "repeat_index": 1,
                    "status": "ok", "verdict": "accept", "verdict_basis": "blind_verdict", "note": ""}]
        return {"run_id": "syn", "revealed_utc": "2026-09-09", "commitment_verified": True, "rules_ref": "r.md", "trials": trials, "elimination": []}

    def screens(self):
        return [screen_doc("syn", [st("Q1-01__alpha__core__r1", "Q1", "alpha", "accept", "accept"),
                                   st("Q1-01__alpha__core__r2", "Q1", "alpha", "reject", "accept", note="lettering"),
                                   st("Q1-01__beta__core__r1", "Q1", "beta", "accept", "cannot_judge")])]

    def test_tier_is_filled_from_screen_results_and_stays_registry_false(self):
        m = EM.build_map([], self.results(), screen_results=self.screens())
        cells = m["questions"]["Q1"]["cells"]
        a = cells["alpha"]["screened_not_qualified"]
        self.assertEqual(a["tier"], "screened_not_qualified")
        self.assertIs(a["registry"], False)
        self.assertEqual(a["status"], "screened_not_qualified")
        self.assertEqual((a["n_screened"], a["n_compared"], a["agreements"], a["agreement_rate"]), (2, 2, 1, 0.5))
        self.assertEqual(a["false_accepts_vs_controller"], 1)
        self.assertEqual(a["instrument"]["config_hash"], ["h" * 64])
        self.assertEqual(a["instrument"]["model"], ["gemini-3.1-flash"])
        self.assertEqual(a["disagreements"], [{"trial_id": "Q1-01__alpha__core__r2", "controller_verdict": "reject", "screen_overall": "accept", "controller_note": "lettering"}])
        b = cells["beta"]["screened_not_qualified"]
        self.assertEqual((b["n_screened"], b["n_compared"], b["cannot_judge"]), (1, 0, 1))
        self.assertIsNone(b["agreement_rate"])
        self.assertEqual(m["sources"]["screen_config_hashes"], ["h" * 64])
        self.assertEqual(m["sources"]["qualified_config_hashes"], [])
        none = EM.build_map([], self.results())["questions"]["Q1"]["cells"]["alpha"]["screened_not_qualified"]
        self.assertEqual(none, {"tier": "screened_not_qualified", "registry": False, "status": "none_yet"})

    def test_status_is_qualified_only_under_a_binding_report_and_registry_stays_false(self):
        unfrozen = {"schema": "QUALIFICATION-REPORT-v0", "_path": "r1.yaml", "instrument": {"config_hash": "h" * 64},
                    "qualification": {"qualification_verdict": "screened_not_qualified", "would_verdict": "qualified", "criteria_frozen": False, "binding": False}}
        m = EM.build_map([], self.results(), screen_results=self.screens(), qualification_reports=[unfrozen])
        self.assertEqual(m["questions"]["Q1"]["cells"]["alpha"]["screened_not_qualified"]["status"], "screened_not_qualified")
        binding = {"schema": "QUALIFICATION-REPORT-v0", "_path": "r2.yaml", "instrument": {"config_hash": "h" * 64},
                   "qualification": {"qualification_verdict": "qualified", "would_verdict": "qualified", "criteria_frozen": True, "binding": True}}
        m = EM.build_map([], self.results(), screen_results=self.screens(), qualification_reports=[binding])
        a = m["questions"]["Q1"]["cells"]["alpha"]["screened_not_qualified"]
        self.assertEqual(a["status"], "qualified")
        self.assertEqual(a["instrument"]["qualification_report"], "r2.yaml")
        self.assertIs(a["registry"], False, "a qualified screen is still never a Registry input")
        self.assertEqual(m["sources"]["qualified_config_hashes"], ["h" * 64])
        other = dict(binding, instrument={"config_hash": "x" * 64})
        m = EM.build_map([], self.results(), screen_results=self.screens(), qualification_reports=[other])
        self.assertEqual(m["questions"]["Q1"]["cells"]["alpha"]["screened_not_qualified"]["status"], "screened_not_qualified", "a report for another config hash does not qualify this one")

    def test_cli_discovers_screen_results_beside_results(self):
        d = self.tmp / "syn"
        d.mkdir()
        (d / "RESULTS.yaml").write_text(yaml.safe_dump(self.results(), sort_keys=False))
        (d / "SCREEN-RESULTS.yaml").write_text(yaml.safe_dump(self.screens()[0], sort_keys=False))
        reg = self.tmp / "registry.jsonl"
        reg.write_text("# empty\n")
        out = self.tmp / "map.yaml"
        rc = EM.main(["--registry", str(reg), "--results", str(d / "RESULTS.yaml"), "--out", str(out)])
        self.assertEqual(rc, 0)
        m = yaml.safe_load(out.read_text())
        self.assertEqual(m["sources"]["screen_results"], [str(d / "SCREEN-RESULTS.yaml")])
        self.assertEqual(m["questions"]["Q1"]["cells"]["alpha"]["screened_not_qualified"]["n_compared"], 2)
        self.assertEqual(EM.sibling_screen_files(d / "RESULTS.yaml"), (d / "SCREEN-RESULTS.yaml", None))


if __name__ == "__main__":
    unittest.main()
