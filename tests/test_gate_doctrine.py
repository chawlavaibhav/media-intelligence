"""Gate registry and result model (CANON-GATE-001, plan §B doctrine.py / findings.py, §C, §F).

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

The registry renders the 21 check lines by id from the two committed packs; nothing in
canon/gate/ carries doctrine text of its own. Negative tests mutate a copy of a pack in a
tempdir and assert the loader refuses it. Run: python3 -m unittest tests.test_gate_doctrine
"""
import re
import tempfile
import unittest
from pathlib import Path

import yaml

from canon.gate import doctrine, findings
from canon.validation import validate_compiled_pack as vcp

REPO_ROOT = Path(__file__).resolve().parents[1]
PA = REPO_ROOT / "canon/compilation/PACK-product_appearance-v0.yaml"
CA = REPO_ROOT / "canon/compilation/PACK-composition_and_attention-v0.yaml"
GATE_DIR = REPO_ROOT / "canon/gate"

ALL_IDS = [f"PA-D{i}-check" for i in range(1, 11)] + [f"CA-D{i}-check" for i in range(1, 12)]


def row(check_id, status, *, family="doctrine", blocking=False, detail="", coverage="partial",
        clause="c", source_text="src"):
    return findings.CheckResult(
        check_id=check_id, family=family, gate="pre_dispatch", status=status,
        coverage=coverage, clause=clause, source_text=source_text, detail=detail,
        evidence=(), blocking=blocking)


class RegistryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reg = doctrine.load_registry()
        cls.pa = yaml.safe_load(PA.read_text())
        cls.ca = yaml.safe_load(CA.read_text())

    # ── render by id ────────────────────────────────────────────────────
    def test_registry_has_exactly_the_21_committed_ids_in_pack_order(self):
        self.assertEqual(list(self.reg.checks), ALL_IDS)

    def test_every_check_text_equals_the_pack_check_string(self):
        for pack in (self.pa, self.ca):
            for d in pack["decisions"]:
                line = self.reg.checks[d["check_id"]]
                self.assertEqual(line.text, d["check"])
                self.assertEqual(line.question, d["question"])
                self.assertEqual(line.decision_id, d["decision_id"])
                self.assertEqual(line.pack_id, pack["pack_id"])
                self.assertEqual(list(line.feeds_sections), d["feeds_sections"])

    def test_limit_text_is_the_verbatim_devanagari_line_from_both_packs(self):
        self.assertEqual(self.reg.limit_text, vcp.DEVANAGARI_LIMIT)
        for pack in (self.pa, self.ca):
            self.assertIn(self.reg.limit_text, pack["pack_limits"])

    def test_pack_info_carries_path_sha_and_modalities(self):
        info = self.reg.packs["product_appearance"]
        self.assertEqual(info.path, PA)
        self.assertEqual(len(info.sha256), 64)
        self.assertEqual(list(info.modalities), ["static_image", "video", "image_sequence"])

    # ── applicability (mirrors canon/packs/pack-triggers-v0.yaml) ───────
    def test_select_packs_mirrors_the_trigger_table(self):
        self.assertEqual(self.reg.select_packs("static_image", False), ["composition_and_attention"])
        self.assertEqual(self.reg.select_packs("static_image", True),
                         ["composition_and_attention", "product_appearance"])
        self.assertEqual(self.reg.select_packs("video", True),
                         ["composition_and_attention", "product_appearance"])
        self.assertEqual(self.reg.select_packs("image_sequence", False),
                         ["composition_and_attention"])
        self.assertEqual(self.reg.select_packs("audio", True), [])

    def test_unknown_modality_is_refused(self):
        with self.assertRaises(doctrine.RegistryError):
            self.reg.select_packs("hologram", False)

    def test_video_only_and_cut_checks_per_modality(self):
        for cid in ("CA-D7-check", "CA-D8-check", "CA-D9-check"):
            self.assertTrue(self.reg.applicable(cid, "video"))
            self.assertTrue(self.reg.applicable(cid, "image_sequence"))
            self.assertFalse(self.reg.applicable(cid, "static_image"))
        for cid in ("CA-D10-check", "CA-D11-check"):
            self.assertTrue(self.reg.applicable(cid, "video"))
            self.assertFalse(self.reg.applicable(cid, "image_sequence"))
            self.assertFalse(self.reg.applicable(cid, "static_image"))
        for cid in ("PA-D1-check", "CA-D1-check", "CA-D6-check"):
            for m in ("static_image", "video", "image_sequence"):
                self.assertTrue(self.reg.applicable(cid, m))
        self.assertFalse(self.reg.applicable("PA-D1-check", "audio"))

    def test_modality_scope_reason_quotes_the_check_line(self):
        reason = self.reg.applicability_reason("CA-D10-check", "static_image")
        self.assertIn("video", reason)
        self.assertIn(self.reg.checks["CA-D10-check"].question, reason)

    # ── fail closed on a tampered or HOLD-carrying pack ─────────────────
    def load_mutated(self, mutate):
        pa = yaml.safe_load(PA.read_text())
        ca = yaml.safe_load(CA.read_text())
        mutate(pa, ca)
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / PA.name
            c = Path(tmp) / CA.name
            p.write_text(yaml.safe_dump(pa, sort_keys=True, allow_unicode=True))
            c.write_text(yaml.safe_dump(ca, sort_keys=True, allow_unicode=True))
            return doctrine.load_registry(pack_paths=[p, c])

    def test_round_tripped_packs_still_load(self):
        reg = self.load_mutated(lambda pa, ca: None)
        self.assertEqual(list(reg.checks), ALL_IDS)

    def test_renamed_check_id_is_refused(self):
        def mutate(pa, ca):
            pa["decisions"][0]["check_id"] = "PA-D1-chk"
        with self.assertRaisesRegex(doctrine.RegistryError, "check_id"):
            self.load_mutated(mutate)

    def test_wrong_decision_count_is_refused(self):
        def mutate(pa, ca):
            del ca["decisions"][-1]
        with self.assertRaisesRegex(doctrine.RegistryError, "decision"):
            self.load_mutated(mutate)

    def test_hold_lane_id_in_a_pack_is_refused(self):
        # scs_logo_001 lives under canon/candidates/ (airey-logo-design-love, HOLD) —
        # the same lane tests/test_compiled_packs.py uses for its refusal fixture.
        def mutate(pa, ca):
            pa["decisions"][0]["limits"] = ["see scs_logo_001"]
        with self.assertRaisesRegex(doctrine.RegistryError, "scs_logo_001"):
            self.load_mutated(mutate)

    def test_missing_devanagari_limit_line_is_refused(self):
        def mutate(pa, ca):
            ca["pack_limits"] = [l for l in ca["pack_limits"] if "Devanagari" not in l]
        with self.assertRaisesRegex(doctrine.RegistryError, "Devanagari"):
            self.load_mutated(mutate)

    def test_id_regex_is_the_validators(self):
        src = (REPO_ROOT / "canon/validation/validate_compiled_pack.py").read_text()
        self.assertIn(doctrine.ID_TOKEN_RE.pattern, src)

    def test_no_id_shaped_token_under_gate_resolves_outside_accepted_canon(self):
        env = vcp.load_environment()
        for path in sorted(GATE_DIR.glob("*.py")):
            for token in sorted(set(re.findall(r"\b(?:sk|scs)_[a-z0-9_]*\d\b", path.read_text()))):
                self.assertNotIn(token, env["candidate_ids"], f"{path.name}: {token} is HOLD")
                self.assertIn(token, env["owner"], f"{path.name}: {token} does not resolve")


class FindingsTest(unittest.TestCase):
    def report(self, rows, gate="pre_dispatch"):
        return findings.Report(gate=gate, inputs={"x.txt": "0" * 64},
                               packs_selected=["composition_and_attention"], results=rows,
                               label="package x.txt (sha256 000000000000)")

    def test_statuses(self):
        self.assertEqual({s.name for s in findings.Status},
                         {"PASS", "FAIL", "NOT_MECHANISED", "NOT_APPLICABLE", "NOT_RUN", "ERROR"})

    def test_verdict_is_fail_only_on_blocking_fail_or_any_error(self):
        S = findings.Status
        self.assertEqual(self.report([row("A", S.PASS)]).verdict(), "PASS")
        self.assertEqual(self.report([row("A", S.FAIL, detail="d")]).verdict(), "PASS")
        self.assertEqual(self.report([row("A", S.FAIL, detail="d", blocking=True)]).verdict(), "FAIL")
        self.assertEqual(self.report([row("A", S.ERROR, detail="d")]).verdict(), "FAIL")
        self.assertEqual(self.report([row("A", S.NOT_RUN, detail="d"),
                                      row("B", S.NOT_MECHANISED, detail="d"),
                                      row("C", S.NOT_APPLICABLE, detail="d")]).verdict(), "PASS")

    def test_every_non_pass_row_needs_a_reason(self):
        for status in (findings.Status.FAIL, findings.Status.NOT_MECHANISED,
                       findings.Status.NOT_APPLICABLE, findings.Status.NOT_RUN,
                       findings.Status.ERROR):
            with self.assertRaisesRegex(ValueError, "reason"):
                self.report([row("A", status, detail="")])

    def test_duplicate_ids_are_refused(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.report([row("A", findings.Status.PASS), row("A", findings.Status.PASS)])

    def test_doctrine_rows_need_source_text(self):
        with self.assertRaisesRegex(ValueError, "source_text"):
            self.report([row("A", findings.Status.PASS, source_text="")])

    def test_render_pass_line_idiom_and_non_blocking_count(self):
        S = findings.Status
        text = self.report([
            row("PA-D1-check", S.PASS, clause="Every key object has exactly one declared finish"),
            row("CA-D5-check", S.FAIL, detail="no balance declaration"),
            row("PA-D2-check", S.NOT_MECHANISED, detail="needs pixels"),
            row("CA-D7-check", S.NOT_APPLICABLE, detail="video decision"),
            row("PA-D10-check", S.NOT_RUN, detail="no DOCTRINE_DEVIATIONS section"),
        ]).render_text()
        lines = text.splitlines()
        self.assertTrue(lines[0].startswith("CANON GATE v0 — pre-dispatch — package x.txt (sha256 "))
        self.assertIn("packs: composition_and_attention", lines[0])
        self.assertIn('PASS            PA-D1-check     [partial: "Every key object has exactly one '
                      'declared finish"]', text)
        self.assertIn("FAIL (non-blocking)", text)
        self.assertIn("NOT-MECHANISED  PA-D2-check     needs pixels — not counted as satisfied", text)
        self.assertIn("NOT-APPLICABLE  CA-D7-check     video decision", text)
        self.assertIn("NOT-RUN         PA-D10-check    no DOCTRINE_DEVIATIONS section", text)
        self.assertEqual(
            lines[-1],
            "GATE PASS: 1 mechanised checks hold over the submitted bytes (1 non-blocking FAIL on "
            "record); 1 doctrine check lines NOT mechanised, 1 not applicable, 1 not run — none "
            "counted as satisfied. This establishes structure over the prompt/artifact bytes — "
            "not doctrine satisfaction, quality, outcomes, or adoption.")
        self.assertNotIn("doctrine satisfied", text)

    def test_render_fail_line_idiom(self):
        S = findings.Status
        text = self.report([
            row("LIMIT-TEXT", S.FAIL, family="limit", blocking=True, detail="prompt 1 requests text",
                coverage="full", clause=""),
            row("CA-D1-check", S.PASS, clause="Name the 1st/2nd/3rd read"),
            row("CA-D5-check", S.FAIL, detail="no balance declaration"),
            row("PA-D2-check", S.NOT_MECHANISED, detail="needs pixels"),
            row("DISPATCH-ASPECT", S.PASS, family="dispatch", blocking=True, coverage="full",
                clause=""),
        ]).render_text()
        lines = text.splitlines()
        self.assertTrue(lines[1].startswith("FAIL            LIMIT-TEXT      prompt 1 requests text"))
        self.assertIn("dispatch", lines)   # the DISPATCH family prints under its own heading
        # a check id longer than the 16-column field still gets a separator
        long_id = self.report([row("DISPATCH-SHOT-SUM", S.PASS, family="dispatch",
                                   coverage="full", clause="", detail="11 shots")]).render_text()
        self.assertIn("PASS            DISPATCH-SHOT-SUM 11 shots", long_id)
        self.assertEqual(
            lines[-1],
            "GATE FAIL (1 failing checks; 1 non-blocking FAIL on record). 2 checks mechanised "
            "(all partial) over 3 doctrine check lines; 1 lines NOT mechanised, not applicable "
            "or not run — never counted as satisfied.")

    def test_error_row_renders_and_fails(self):
        rep = self.report([row("LIMIT-TEXT", findings.Status.ERROR, family="limit",
                               detail="no prompts", coverage="full", clause="")])
        self.assertEqual(rep.verdict(), "FAIL")
        self.assertIn("ERROR           LIMIT-TEXT      no prompts", rep.render_text())

    def test_json_round_trips_every_row(self):
        S = findings.Status
        rep = self.report([row("A", S.PASS), row("B", S.FAIL, detail="d", blocking=True)])
        js = rep.to_json()
        self.assertEqual(js["gate"], "pre_dispatch")
        self.assertEqual(js["verdict"], "FAIL")
        self.assertEqual(js["inputs"], {"x.txt": "0" * 64})
        self.assertEqual([r["check_id"] for r in js["results"]], ["A", "B"])
        self.assertEqual(js["results"][1]["status"], "FAIL")
        self.assertTrue(js["results"][1]["blocking"])
        self.assertEqual(js["results"][0]["evidence"], [])
        self.assertEqual(js["report_text"], rep.render_text())


if __name__ == "__main__":
    unittest.main()
