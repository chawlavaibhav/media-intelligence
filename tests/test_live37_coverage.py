"""Tests for the REP-07 / DN-06 live-37 coverage layer.

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

Two layers, in the pattern of tests/test_live24_coverage.py: (1) the full validator runs end to
end and exits 0 — this is the acceptance check for the DN-06 consequence-5 rebuild and it
re-runs the generator twice, so it also proves determinism; (2) targeted checks that the
committed coverage artifact really carries the DN-06 rulings — the two ruling-(c) admission
markers visible wherever the marked sources appear, and the three ruling-(d) scoped extensions
never counted independent of their parents — plus the frozen-predecessor guarantee (the live24
AND live19 planning artifacts byte-identical to HEAD: supersede, never mutate).

Run: python3 -m unittest tests.test_live37_coverage
"""
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "canon/validation/validate_live37_coverage.py"
COVERAGE = REPO_ROOT / "canon/planning/CANON-V1-LIVE37-COVERAGE.yaml"
AUDIT_GATE = REPO_ROOT / "canon/validation/validate_audit_gate_v02.py"
RECORDS_DIR = REPO_ROOT / "canon/audit/records"

MARKED = {
    "google-abcd-video-ads": "platform_contingent",
    "sontag-on-photography": "critique_context",
}

SCOPED = {
    "hopkins-scientific-advertising-ch8-21": "hopkins-scientific-advertising-ch1-7",
    "light-science-magic-beyond-ch3": "light-science-magic-ch3",
    "ogilvy-beyond-ch2": "ogilvy-ch2-advertising-that-sells",
}


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Live37CoverageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proc = subprocess.run(
            [sys.executable, str(VALIDATOR)], capture_output=True, text=True,
            cwd=str(REPO_ROOT))
        cls.cov = yaml.safe_load(COVERAGE.read_text())

    def test_validator_exits_zero(self):
        self.assertEqual(
            self.proc.returncode, 0,
            f"validate_live37_coverage.py failed:\n{self.proc.stdout}\n{self.proc.stderr}")
        payload = json.loads(self.proc.stdout)
        self.assertTrue(payload["ok"])

    def test_coverage_yaml_facts(self):
        s = self.cov["summary"]
        self.assertEqual(s["accepted_sources"], 37)
        self.assertEqual(s["total_objects"], 1300)
        self.assertEqual(s["sources_contributing_to_no_domain"], [])
        iic = self.cov["packs"]["indian_indic_context"]
        self.assertEqual(len(iic["contributors"]), 5)
        # DN-06 changed none of its sources: it must keep the live24 state exactly.
        live24 = yaml.safe_load(
            (REPO_ROOT / "canon/planning/CANON-V1-LIVE24-COVERAGE.yaml").read_text())
        self.assertEqual(iic["contributors"],
                         live24["packs"]["indian_indic_context"]["contributors"])
        self.assertEqual(iic["pack_state"],
                         live24["packs"]["indian_indic_context"]["pack_state"])

    def test_every_source_packed(self):
        in_pack = {c for p in self.cov["packs"].values() for c in p["contributors"]}
        knowledge = REPO_ROOT / "canon/knowledge/current"
        accepted = {d.name for d in knowledge.iterdir()
                    if d.is_dir() and (d / "source-knowledge.yaml").exists()}
        self.assertEqual(accepted - in_pack, set(),
                         "accepted sources contributing to no pack")

    def test_ruling_c_markers_visible(self):
        """The two DN-06 ruling-(c) sources carry their markers in the summary and on every
        domain and pack row where they appear."""
        s = self.cov["summary"]["admission_markers"]
        self.assertEqual(s["platform_contingent"], ["google-abcd-video-ads"])
        self.assertEqual(s["critique_context"], ["sontag-on-photography"])
        appeared = {src: 0 for src in MARKED}
        for d in self.cov["domains"]:
            for src, cond in MARKED.items():
                if src in d["contributors"]:
                    appeared[src] += 1
                    self.assertEqual(d["contributor_markers"].get(src), cond,
                                     f"domain {d['id']} drops the {cond} marker for {src}")
        for name, p in self.cov["packs"].items():
            for src, cond in MARKED.items():
                if src in p["contributors"]:
                    self.assertEqual(p["contributor_markers"].get(src), cond,
                                     f"pack {name} drops the {cond} marker for {src}")
        for src, n in appeared.items():
            self.assertGreater(n, 0, f"marked source {src} contributes to no domain")

    def test_ruling_c_markers_match_audit_records(self):
        recs = [yaml.safe_load(p.read_text()) for p in sorted(RECORDS_DIR.glob("*.audit.yaml"))]
        by_sid = {r["source_id"]: r for r in recs if r.get("source_id")}
        for src, cond in MARKED.items():
            rec = by_sid.get(src)
            self.assertIsNotNone(rec, f"no audit record for {src}")
            conds = {c.get("condition") for c in (rec.get("admission_conditions") or [])}
            self.assertIn(cond, conds, f"{src} record lacks admission condition {cond}")

    def test_ruling_d_scoped_extensions_never_independent(self):
        """Each scoped extension is dependence-blocked against its parent by the committed
        lineage, and no domain or pack origin set holds both together."""
        self.assertEqual(self.cov["summary"]["scoped_extensions"], SCOPED)
        vmod = load(AUDIT_GATE, "audit_gate_t37")
        records = {p.name: yaml.safe_load(p.read_text())
                   for p in sorted(RECORDS_DIR.glob("*.audit.yaml"))}
        sid = {}
        for d in (REPO_ROOT / "canon/knowledge/current").iterdir():
            f = d / "source-knowledge.yaml"
            if d.is_dir() and f.exists():
                sid[d.name] = yaml.safe_load(f.read_text()).get("source_id")
        for ext, parent in SCOPED.items():
            ok, reason = vmod.independent_origins_ok(sid[ext], sid[parent], records)
            self.assertFalse(ok, f"{ext} not dependence-blocked against {parent}: {reason}")
        rows = list(self.cov["domains"]) + list(self.cov["packs"].values())
        for row in rows:
            chosen = set(row.get("independent_origin_set") or [])
            for ext, parent in SCOPED.items():
                self.assertFalse(
                    {sid[ext], sid[parent]} <= chosen,
                    f"{ext} counted independent of {parent} in "
                    f"{row.get('id') or 'a pack'}'s origin set")

    def test_b11_no_longer_floored_at_2011(self):
        b11 = next(d for d in self.cov["domains"] if d["id"] == "B11")
        self.assertIn("google-abcd-video-ads", b11["contributors"])
        self.assertNotEqual(b11["coverage_state"], "absent")
        self.assertNotIn("2011", b11["gap"])
        pack = self.cov["packs"]["editing_pacing_and_short_form"]
        self.assertIn("google-abcd-video-ads", pack["contributors"])

    def test_live24_and_live19_artifacts_untouched(self):
        """Frozen decision: supersede, never mutate. The live24 AND live19 planning artifacts
        must be byte-identical to HEAD, even after the live37 validator re-ran its builder."""
        diff = subprocess.run(
            ["git", "diff", "--name-only", "HEAD", "--",
             "canon/planning/live24_domain_map.yaml",
             "canon/planning/CANON-V1-LIVE24-COVERAGE.yaml",
             "canon/planning/CANON-V1-LIVE24-COVERAGE.md",
             "canon/planning/build_live24_coverage.py",
             "canon/validation/validate_live24_coverage.py",
             "canon/planning/live19_domain_map.yaml",
             "canon/planning/CANON-V1-LIVE19-COVERAGE.yaml",
             "canon/planning/CANON-V1-LIVE19-COVERAGE.md",
             "canon/planning/build_live19_coverage.py"],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        self.assertEqual(diff.stdout.strip(), "",
                         "frozen live24/live19 artifact modified: " + diff.stdout)


if __name__ == "__main__":
    unittest.main()
