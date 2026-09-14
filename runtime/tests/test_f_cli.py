"""`--manifest` and `--execute` on the route CLI (lane F). Subprocess, offline, USD 0."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import _bootstrap as B

PROMPT = "A textless Diwali plate for the sweet shop with a calm lower third; no lettering anywhere in the frame."


def _cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-m", "runtime.route.cli", *args],
                          capture_output=True, text=True, cwd=str(B.ROOT))


class ManifestCommand(unittest.TestCase):
    def test_without_a_prompt_the_cli_refuses_and_says_so(self):
        proc = _cli("--manifest", str(B.SPEC_STATIC_OVERLAY), "--profile", "dry")
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn("MANIFEST REFUSED", proc.stdout)
        self.assertIn("never invents a prompt", proc.stdout)

    def test_with_a_prompt_file_it_prints_a_manifest_and_json_parses(self):
        with tempfile.TemporaryDirectory() as tmp:
            pf = Path(tmp) / "prompt.txt"
            pf.write_text(PROMPT, encoding="utf-8")
            proc = _cli("--manifest", str(B.SPEC_STATIC_OVERLAY), "--profile", "dry", "--prompt-file", str(pf))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("EXECUTION-MANIFEST", proc.stdout)
            self.assertIn("flux-2-pro on fal", proc.stdout)
            proc = _cli("--manifest", str(B.SPEC_STATIC_OVERLAY), "--profile", "dry", "--prompt-file", str(pf), "--json")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            m = json.loads(proc.stdout)
            self.assertEqual(m["schema"], "EXECUTION-MANIFEST-v0")
            self.assertEqual(len(m["attempts"]), 4)
            self.assertEqual(m["attempts"][0]["request"]["body"]["prompt"], PROMPT)

    def test_prompt_from_spec_reads_lane_e_s_field_when_present(self):
        """The fixtures carry no blueprint yet (lane E lands it); a copy with the field is enough to prove
        the plumbing, and without the field the CLI refuses rather than inventing."""
        import yaml
        with tempfile.TemporaryDirectory() as tmp:
            data = yaml.safe_load(B.SPEC_STATIC_OVERLAY.read_text(encoding="utf-8"))
            data["blueprint"] = {"generation_prompts": {"main": PROMPT, "textless_plate": None, "motion": None},
                                 "planner": "recorded_fixture", "source_ref": "test", "case_values": {},
                                 "production_parameters": {}}
            sp = Path(tmp) / "SPEC-with-blueprint.yaml"
            sp.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
            proc = _cli("--manifest", str(sp), "--profile", "dry", "--prompt-from-spec", "--json")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(json.loads(proc.stdout)["attempts"][0]["request"]["body"]["prompt"], PROMPT)
        proc = _cli("--manifest", str(B.SPEC_STATIC_OVERLAY), "--profile", "dry", "--prompt-from-spec")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("MANIFEST REFUSED", proc.stdout)

    def test_a_blocked_manifest_prints_blocked_and_no_attempts(self):
        with tempfile.TemporaryDirectory() as tmp:
            pf = Path(tmp) / "prompt.txt"
            pf.write_text(PROMPT, encoding="utf-8")
            proc = _cli("--manifest", str(B.SPEC_EDIT_PHOTO), "--profile", "dry", "--prompt-file", str(pf), "--json")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            m = json.loads(proc.stdout)
            self.assertEqual(m["blocked"]["reason_code"], "manual_route_required")
            self.assertEqual(m["attempts"], [])


class ExecuteCommand(unittest.TestCase):
    def test_execute_under_the_live_alpha_profile_refuses_on_spend_authority(self):
        proc = _cli("--execute", str(B.SPEC_STATIC_OVERLAY), "--profile", "alpha_human_release",
                    "--request-ceiling-usd", "5")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("EXECUTE REFUSED", proc.stdout)
        self.assertIn("spend_authority", proc.stdout)

    def test_execute_under_dry_prints_a_dry_complete_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            pf = Path(tmp) / "prompt.txt"
            pf.write_text(PROMPT, encoding="utf-8")
            proc = _cli("--execute", str(B.SPEC_STATIC_OVERLAY), "--profile", "dry",
                        "--request-ceiling-usd", "5", "--prompt-file", str(pf))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("RUN  status dry_complete", proc.stdout)
            self.assertIn("dry_not_sent", proc.stdout)
            self.assertIn("network none", proc.stdout)


if __name__ == "__main__":
    unittest.main()
