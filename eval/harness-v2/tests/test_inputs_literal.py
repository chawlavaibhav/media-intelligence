"""inputs.py literal choices (2026-09-09): `literal:<value>` maps a recorded choice (the TTS speaker) through INPUTS.yaml."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _support import NoNetworkTestCase  # noqa: E402

import inputs as I  # noqa: E402


class LiteralInputTest(NoNetworkTestCase):
    def test_literal_ref_parses_and_loads_as_a_value_not_bytes(self):
        self.assertEqual(I.parse_ref("literal:aditya"), {"kind": "literal", "run_id": None, "artifact_id": "aditya", "suffix": None})
        with self.assertRaises(I.InputsError):
            I.parse_ref("literal:")
        with self.assertRaises(I.InputsError):
            I.parse_ref("literal:two words")
        p = I.write_inputs_file(self.tmp / "INPUTS.yaml", [{"case_id": "AUD-TTS-01", "arm": "*", "role": "choice:speaker_id_lowercase", "ref": "literal:aditya"}])
        f = I.InputsFile(p, runs_root=self.tmp)
        res = f.load(f.entries_for("AUD-TTS-01", "native")["choice:speaker_id_lowercase"])
        self.assertIsInstance(res, I.LiteralInput)
        self.assertEqual((res.value, res.summary()["kind"], res.summary()["bytes"]), ("aditya", "literal", None))

    def test_sarvam_rows_need_the_speaker_choice_and_get_it_as_voice(self):
        class E:  # the SurfaceEntry fields roles_needed reads
            adapter = "sarvam_tts"; workflow = "tts"; route_key = "sarvam-bulbul-v3"
        needed = I.roles_needed(E(), {"params": {"script": "x"}})
        self.assertEqual(needed, [("choice:speaker_id_lowercase", "voice")])
        built = I.build_inputs(E(), needed, {"choice:speaker_id_lowercase": I.LiteralInput("choice:speaker_id_lowercase", "literal:aditya", "aditya")})
        self.assertEqual(built, {"voice": "aditya"})

    def test_a_row_without_the_choice_line_stays_unresolved(self):
        class E:
            adapter = "sarvam_tts"; workflow = "tts"; route_key = "sarvam-bulbul-v3"
        p = I.write_inputs_file(self.tmp / "INPUTS.yaml", [])
        inputs, summaries, unresolved = I.InputResolver(I.InputsFile(p, runs_root=self.tmp)).for_row({"case_id": "AUD-TTS-01", "arm": "native", "params": {}}, E())
        self.assertEqual((inputs, summaries, unresolved), ({}, [], ["choice:speaker_id_lowercase"]))


if __name__ == "__main__":
    unittest.main()
