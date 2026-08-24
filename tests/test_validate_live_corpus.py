import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

from canon.validation import validate_audit_gate_v02 as audit
from canon.validation import validate_live_corpus as live

REPO_ROOT = Path(__file__).resolve().parents[1]


class LiveCorpusRegisterTests(unittest.TestCase):
    """The register is what lets a source be real, valid, and still not cleared for downstream use."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        # A miniature live corpus: one accepted source with an audit record, one held back.
        for name in ("accepted-book", "blocked-book"):
            src = REPO_ROOT / "canon" / "knowledge" / "current" / "vignelli-canon-intangibles"
            dst = self.root / "canon" / "knowledge" / "current" / name
            shutil.copytree(src, dst)
            self._rewrite_ids(dst, name)
        (self.root / audit.RECORDS_SUBPATH).mkdir(parents=True)
        self._write_register(
            {"dir": "accepted-book", "gate_status": "accepted"},
            {"dir": "blocked-book", "gate_status": "source_evidence_only",
             "blocked_reason": "a lineage relationship the vocabulary cannot state"},
        )
        self._write_audit("accepted-book")

    def tearDown(self):
        self._tmp.cleanup()

    def _rewrite_ids(self, book: Path, tag: str) -> None:
        """Give the copy its own ids so the collision check is exercised honestly."""
        short = "acc" if tag.startswith("accepted") else "blk"
        for path in book.glob("*.yaml"):
            text = path.read_text(encoding="utf-8").replace("_vig_", f"_{short}_")
            text = text.replace("vignelli_canon_part_one_intangibles", f"{short}_source")
            path.write_text(text, encoding="utf-8")

    def _write_register(self, *entries) -> None:
        path = self.root / live.REGISTER_PATH
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            yaml.safe_dump({"register_version": "v1", "historical_method_test_corpus": 16,
                            "sources": list(entries)}, sort_keys=False),
            encoding="utf-8",
        )

    def _write_audit(self, name: str) -> None:
        kd = f"canon/knowledge/current/{name}"
        snapshot = audit.compute_source_snapshot(self.root, kd)
        doc = {
            "audit_record_version": audit.AUDIT_RECORD_VERSION,
            "audit_id": f"aud_{name.replace('-', '_')}",
            "source_id": "acc_source" if name.startswith("accepted") else "blk_source",
            "knowledge_dir": kd,
            "audit_status": "complete",
            "source_snapshot": {k: snapshot[k] for k in ("algorithm", "files", "combined_digest")},
        }
        (self.root / audit.RECORDS_SUBPATH / f"{name}.audit.yaml").write_text(
            yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")

    def _errors(self):
        return live.validate_live_corpus(self.root)["errors"]

    def test_declared_corpus_validates_clean(self):
        report = live.validate_live_corpus(self.root)
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["accepted_count"], 1)
        self.assertEqual(report["source_evidence_only_count"], 1)
        self.assertEqual(report["sources_on_disk"], 2)

    def test_an_undeclared_source_on_disk_is_reported(self):
        shutil.copytree(
            self.root / "canon/knowledge/current/accepted-book",
            self.root / "canon/knowledge/current/smuggled-book",
        )
        self.assertTrue(any("undeclared source: smuggled-book" in e for e in self._errors()))

    def test_accepted_without_an_audit_record_is_reported(self):
        (self.root / audit.RECORDS_SUBPATH / "accepted-book.audit.yaml").unlink()
        errors = self._errors()
        self.assertTrue(
            any("declared accepted but has no active Audit Gate record" in e for e in errors), errors
        )

    def test_a_blocked_source_may_not_hold_an_audit_record(self):
        self._write_audit("blocked-book")
        errors = self._errors()
        self.assertTrue(
            any("declared source_evidence_only but carries an audit record" in e for e in errors),
            errors,
        )

    def test_a_blocked_source_must_say_why(self):
        self._write_register(
            {"dir": "accepted-book", "gate_status": "accepted"},
            {"dir": "blocked-book", "gate_status": "source_evidence_only"},
        )
        self.assertTrue(any("no blocked_reason" in e for e in self._errors()))

    def test_invalid_gate_status_is_reported(self):
        self._write_register(
            {"dir": "accepted-book", "gate_status": "probationary"},
            {"dir": "blocked-book", "gate_status": "source_evidence_only", "blocked_reason": "x"},
        )
        self.assertTrue(any("invalid gate_status" in e for e in self._errors()))

    def test_declared_but_absent_directory_is_reported(self):
        shutil.rmtree(self.root / "canon/knowledge/current/blocked-book")
        self.assertTrue(any("no such directory exists" in e for e in self._errors()))

    def test_id_collision_across_the_live_corpus_is_reported(self):
        # Make the blocked copy reuse the accepted copy's ids.
        for path in (self.root / "canon/knowledge/current/blocked-book").glob("*.yaml"):
            path.write_text(path.read_text(encoding="utf-8").replace("_blk_", "_acc_"), encoding="utf-8")
        self.assertTrue(any("id collision" in e for e in self._errors()))

    def test_a_blocked_source_must_still_be_mechanically_valid(self):
        path = self.root / "canon/knowledge/current/blocked-book/source-knowledge.yaml"
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        doc["source_knowledge"][0]["claim_type"] = "not_a_valid_claim_type"
        path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
        self.assertTrue(any("invalid or missing claim_type" in e for e in self._errors()))


class RealLiveCorpusTests(unittest.TestCase):
    """Assertions about the corpus this repository actually holds."""

    @classmethod
    def setUpClass(cls):
        cls.report = live.validate_live_corpus(REPO_ROOT)
        cls.register = yaml.safe_load(
            (REPO_ROOT / live.REGISTER_PATH).read_text(encoding="utf-8"))

    def test_live_corpus_validates_clean(self):
        self.assertEqual(self.report["errors"], [])

    def test_every_source_on_disk_is_declared(self):
        on_disk = {p.name for p in (REPO_ROOT / "canon/knowledge/current").iterdir() if p.is_dir()}
        declared = {e["dir"] for e in self.register["sources"]}
        self.assertEqual(on_disk, declared)

    def test_historical_method_test_corpus_is_fixed_at_sixteen(self):
        # CANON-003 accepted 16 and CANON-004 tested 16. Neither number may drift with the live corpus.
        self.assertEqual(self.register["historical_method_test_corpus"], 16)
        self.assertEqual(len(audit.validate_repository(REPO_ROOT)["records"]),
                         self.report["accepted_count"])

    def test_the_conversations_is_held_back_not_accepted(self):
        entry = next(e for e in self.register["sources"] if e["dir"] == "ondaatje-conversations-ch3")
        self.assertEqual(entry["gate_status"], "source_evidence_only")
        self.assertTrue(entry.get("blocked_reason", "").strip())
        self.assertNotIn("ondaatje-conversations-ch3", self.report["accepted"])

    def test_master_shots_is_accepted_with_an_audit_record(self):
        entry = next(e for e in self.register["sources"] if e["dir"] == "kenworthy-master-shots-ch8")
        self.assertEqual(entry["gate_status"], "accepted")
        self.assertTrue(
            (REPO_ROOT / audit.RECORDS_SUBPATH / "kenworthy-master-shots-ch8.audit.yaml").is_file())

    def test_no_lineage_relation_was_invented_for_the_murch_pair(self):
        # The blocked source holds no audit record, so no false relation could have been written.
        records = REPO_ROOT / audit.RECORDS_SUBPATH
        self.assertFalse((records / "ondaatje-conversations-ch3.audit.yaml").exists())
        for path in records.glob("*.audit.yaml"):
            doc = yaml.safe_load(path.read_text(encoding="utf-8"))
            for entry in (doc.get("lineage") or {}).get("related_sources_in_corpus") or []:
                self.assertIn(entry["relation"], audit.LINEAGE_RELATIONS)
                self.assertNotEqual(
                    entry.get("source_id"), "ondaatje_conversations_third_conversation",
                    "no accepted record may declare a relation to the blocked source while the "
                    "vocabulary cannot state it truthfully",
                )


if __name__ == "__main__":
    unittest.main()
