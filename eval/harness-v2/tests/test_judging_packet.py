"""judging_packet.py: blind packet build, leak scan, commitment, reveal, E1/E2. Fakes only (a run produced by the
runner with fake transports); the reveal key is written to a temp dir that is outside the repo."""
import hashlib
import json
import os
import re
import struct
import unittest
import zlib
from pathlib import Path

import yaml

from _support import NoNetworkTestCase, hv2_paths
import judging_packet as JP
import run_live as RL
import store as S
import surfaces
from test_run_live import CANARY, FakeFactory, RunnerBase, png_bytes


def png_with_text(keyword: str, text: str) -> bytes:
    """A valid PNG with one tEXt chunk inserted after IHDR."""
    base = png_bytes(rgb=(1, 2, 3))
    payload = keyword.encode("latin-1") + b"\x00" + text.encode("latin-1")
    chunk = struct.pack(">I", len(payload)) + b"tEXt" + payload + struct.pack(">I", zlib.crc32(b"tEXt" + payload) & 0xFFFFFFFF)
    ihdr_end = 8 + 4 + 4 + 13 + 4
    return base[:ihdr_end] + chunk + base[ihdr_end:]


class PacketBase(RunnerBase):
    def setUp(self):
        super().setUp()
        self.key_dir = self.tmp / "keys-outside-repo"
        self.assertNotIn(hv2_paths.REPO_ROOT, self.key_dir.resolve().parents)

    def make_run(self, routes=("gpt-image-2", "nano-banana-2"), outcome_for=None):
        self.plan(routes=routes)
        self.factory = FakeFactory(outcome_for=outcome_for)
        summary = self.runner().execute()
        self.assertEqual(summary["status"], "completed")
        return summary


class BuildTest(PacketBase):
    def test_packet_carries_only_blind_id_case_and_contract(self):
        self.make_run()
        res = JP.build(self.out, "run-x", key_dir=self.key_dir)
        jd = self.out / "judging"
        files = sorted(p.name for p in jd.iterdir())
        self.assertEqual(res["n_artifacts"], 4)
        self.assertEqual(len([f for f in files if f.endswith(".png")]), 4)
        self.assertTrue(all(re.fullmatch(r"J\d{2}\.png", f) for f in files if f.endswith(".png")), files)
        self.assertIn("JUDGING-SHEET.md", files)
        self.assertIn("REVEAL-COMMITMENT.txt", files)
        self.assertIn("VERDICTS.template.yaml", files)
        sheet = (jd / "JUDGING-SHEET.md").read_text()
        self.assertIn("IMG-CORE-01", sheet)
        self.assertIn("ACCEPT only if exactly one bottle is in frame", sheet)
        # the key is NOT under out; the commitment is
        self.assertFalse(list(self.out.rglob("REVEAL-*.json")))
        key = json.loads((self.key_dir / "REVEAL-run-x.json").read_text())
        self.assertEqual(set(key["mapping"]), {f[:-4] for f in files if f.endswith(".png")})
        self.assertEqual({v["route_key"] for v in key["mapping"].values()}, {"gpt-image-2", "nano-banana-2"})
        # bytes are evidence: every packet file equals its sealed artifact byte for byte
        store = S.SealedStore(self.out / "artifacts")
        by_trial = {m["trial_id"]: m for m in store.manifest()}
        for bid, v in key["mapping"].items():
            self.assertEqual(hashlib.sha256((jd / f"{bid}.png").read_bytes()).hexdigest(), by_trial[v["trial_id"]]["sha256"])

    def test_packet_leaks_no_route_identity(self):
        self.make_run()
        JP.build(self.out, "run-x", key_dir=self.key_dir)
        plan = yaml.safe_load((self.out / "PLAN.yaml").read_text())
        needles = set()
        for t in plan["trials"]:
            e = surfaces.REGISTRY.get(t["route_key"])
            needles |= {t["route_key"], t["trial_id"], e.surface, e.surface_model_id, e.adapter, t["billing_pool"],
                        str(t["estimated_usd_equiv"]), f"r{t['repeat_index']}", "repeat_index"}
            if "_" in t["arm"]:
                needles.add(t["arm"])          # the text-case arms name the route tier; "core" is the case family, not an identity
        needles |= {"fal", "vertex", "gemini", "openai", "repeat", "surface", "route", "price", "usd", "arm"}
        for p in (self.out / "judging").iterdir():
            raw = p.read_bytes().decode("utf-8", errors="ignore")
            for n in needles:
                pat = r"(?<![A-Za-z0-9_])" + re.escape(n) + r"(?![A-Za-z0-9_])"
                self.assertIsNone(re.search(pat, raw, re.I), f"{p.name} leaks {n!r}")

    def test_blind_ids_are_a_random_permutation_not_plan_order(self):
        self.make_run()
        JP.build(self.out, "run-x", key_dir=self.key_dir, seed="seed-A")
        a = json.loads((self.key_dir / "REVEAL-run-x.json").read_text())["mapping"]
        out2 = self.tmp / "runs" / "run-y"
        self.plan(out=out2, run_id="run-y")
        RL.LiveRunner(out2, "run-y", auth_path=self.auth, transport_factory=FakeFactory(), adapter_kwargs=self.adapter_kwargs,
                      gate_script=self.gate_script).execute()
        JP.build(out2, "run-y", key_dir=self.key_dir, seed="seed-B")
        b = json.loads((self.key_dir / "REVEAL-run-y.json").read_text())["mapping"]
        order_a = [a[k]["trial_id"].replace("run", "") for k in sorted(a)]
        order_b = [b[k]["trial_id"].replace("run", "") for k in sorted(b)]
        self.assertNotEqual(order_a, order_b, "two seeds give two permutations")
        plan_order = [t["trial_id"] for t in yaml.safe_load((self.out / "PLAN.yaml").read_text())["trials"]]
        self.assertTrue(order_a != plan_order or order_b != plan_order)

    def test_key_dir_inside_the_repo_is_refused(self):
        self.make_run()
        with self.assertRaises(JP.PacketRefused):
            JP.build(self.out, "run-x", key_dir=hv2_paths.REPO_ROOT / "eval" / "runs" / "keys")
        self.assertFalse((self.out / "judging").exists())

    def test_build_refuses_to_overwrite_a_packet(self):
        self.make_run()
        JP.build(self.out, "run-x", key_dir=self.key_dir)
        with self.assertRaises(JP.PacketRefused):
            JP.build(self.out, "run-x", key_dir=self.key_dir)

    def test_metadata_guard_notes_a_text_chunk_without_altering_bytes(self):
        tagged = png_with_text("Software", "made with gemini-3-pro-image")
        flags = JP.scan_metadata(tagged, ".png", ["gemini-3-pro-image"])
        self.assertTrue(any("tEXt" in f for f in flags), flags)
        self.assertTrue(any("gemini-3-pro-image" in f for f in flags), flags)
        self.assertEqual(JP.scan_metadata(png_bytes(), ".png", ["gemini-3-pro-image"]), [])
        # end to end: a run whose vertex artifacts carry the chunk -> note recorded OUTSIDE judging/, bytes untouched
        import test_run_live as TRL
        saved = TRL.vertex_transport

        def tagged_vertex(png, outcome="ok"):
            return saved(tagged, outcome)
        TRL.vertex_transport = tagged_vertex
        try:
            self.make_run()
        finally:
            TRL.vertex_transport = saved
        res = JP.build(self.out, "run-x", key_dir=self.key_dir)
        notes = json.loads((self.out / "judging-build" / "METADATA-NOTES.json").read_text())
        flagged = [t for t, v in notes.items() if v]
        self.assertEqual(len(flagged), 2)
        self.assertTrue(all("nano-banana" in t for t in flagged))
        self.assertEqual(res["metadata_flagged"], 2)
        for bid, v in json.loads((self.key_dir / "REVEAL-run-x.json").read_text())["mapping"].items():
            if "nano-banana" in v["trial_id"]:
                self.assertEqual(hashlib.sha256((self.out / "judging" / f"{bid}.png").read_bytes()).hexdigest(), hashlib.sha256(tagged).hexdigest())
        sheet = (self.out / "judging" / "JUDGING-SHEET.md").read_text()
        self.assertNotIn("gemini", sheet.lower())


class RevealTest(PacketBase):
    def _verdicts(self, mapping, fn):
        v = {bid: {"verdict": fn(bid, m), "note": "test"} for bid, m in mapping.items()}
        (self.out / "judging" / "VERDICTS.yaml").write_text(yaml.safe_dump({"verdicts": v}))
        return v

    def test_reveal_refuses_on_commitment_mismatch(self):
        self.make_run()
        JP.build(self.out, "run-x", key_dir=self.key_dir)
        kp = self.key_dir / "REVEAL-run-x.json"
        key = json.loads(kp.read_text())
        self._verdicts(key["mapping"], lambda b, m: "accept")
        ids = sorted(key["mapping"])
        key["mapping"][ids[0]], key["mapping"][ids[1]] = key["mapping"][ids[1]], key["mapping"][ids[0]]
        kp.write_text(json.dumps(key))
        with self.assertRaises(JP.PacketRefused):
            JP.reveal(self.out, "run-x", key_dir=self.key_dir)
        self.assertFalse((self.out / "RESULTS.yaml").exists())

    def test_reveal_refuses_incomplete_verdicts(self):
        self.make_run()
        JP.build(self.out, "run-x", key_dir=self.key_dir)
        key = json.loads((self.key_dir / "REVEAL-run-x.json").read_text())
        v = self._verdicts(key["mapping"], lambda b, m: "accept")
        v.pop(sorted(v)[0])
        (self.out / "judging" / "VERDICTS.yaml").write_text(yaml.safe_dump({"verdicts": v}))
        with self.assertRaises(JP.PacketRefused):
            JP.reveal(self.out, "run-x", key_dir=self.key_dir)

    def test_reveal_merges_verdicts_per_case_route_repeat(self):
        self.make_run(outcome_for=lambda t: "refusal" if t["seq"] == 1 else "ok")   # gpt-image-2 r1 refused -> no artifact
        JP.build(self.out, "run-x", key_dir=self.key_dir)
        key = json.loads((self.key_dir / "REVEAL-run-x.json").read_text())
        self.assertEqual(len(key["mapping"]), 3)
        self._verdicts(key["mapping"], lambda b, m: "accept" if "nano-banana" in m["trial_id"] else "reject")
        res = JP.reveal(self.out, "run-x", key_dir=self.key_dir)
        results = yaml.safe_load((self.out / "RESULTS.yaml").read_text())
        rows = {(r["case_id"], r["route_key"], r["repeat_index"]): r for r in results["trials"]}
        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[("IMG-CORE-01", "gpt-image-2", 1)]["verdict"], "reject")
        self.assertEqual(rows[("IMG-CORE-01", "gpt-image-2", 1)]["verdict_basis"], "no_artifact:refusal")
        self.assertEqual(rows[("IMG-CORE-01", "gpt-image-2", 2)]["verdict"], "reject")
        self.assertEqual(rows[("IMG-CORE-01", "nano-banana-2", 1)]["verdict"], "accept")
        self.assertTrue(rows[("IMG-CORE-01", "nano-banana-2", 1)]["blind_id"].startswith("J"))
        self.assertEqual(results["commitment_verified"], True)
        table = {(r["route_key"], r["question"]): r for r in results["elimination"]}
        self.assertEqual(table[("gpt-image-2", "IMG-CORE")]["n_planned"], 2)
        self.assertEqual(table[("gpt-image-2", "IMG-CORE")]["refusals_or_errors"], 1)
        self.assertEqual(table[("nano-banana-2", "IMG-CORE")]["accepts"], 2)
        self.assertIn("route_key", res["table_text"])


class EliminationRulesTest(NoNetworkTestCase):
    def _trials(self, route, n, accepts, refusals, question="IMG-CORE", not_dispatched=0):
        out = []
        for i in range(n):
            if i < refusals:
                out.append({"route_key": route, "question": question, "arm": "core", "status": "refusal", "verdict": "reject", "dispatched": True})
            elif i < refusals + accepts:
                out.append({"route_key": route, "question": question, "arm": "core", "status": "ok", "verdict": "accept", "dispatched": True})
            elif i < n - not_dispatched:
                out.append({"route_key": route, "question": question, "arm": "core", "status": "ok", "verdict": "reject", "dispatched": True})
            else:
                out.append({"route_key": route, "question": question, "arm": "core", "status": None, "verdict": "reject", "dispatched": False})
        return out

    def test_thresholds_are_the_frozen_proportions(self):
        # (n, E1 minimum refusals to eliminate, E2 maximum accepts to eliminate) from ELIMINATION-RULES.md
        for n, e1, e2 in ((8, 3, 2), (4, 2, 1), (6, 3, 1), (2, 1, 0)):
            self.assertEqual(JP.e1_threshold(n), e1, n)
            self.assertEqual(JP.e2_threshold(n), e2, n)

    def test_e1_and_e2_on_a_constructed_verdict_set(self):
        trials = (self._trials("a", 8, accepts=5, refusals=0) +            # survives
                  self._trials("b", 8, accepts=2, refusals=0) +            # E2: <= 2 of 8
                  self._trials("c", 8, accepts=5, refusals=3) +            # E1: >= 3 of 8 (accepts do not save it)
                  self._trials("d", 8, accepts=3, refusals=2) +            # survives: 2 refusals, 3 accepts
                  self._trials("e", 4, accepts=2, refusals=1, question="IMG-TEXT") +   # survives on the 4-trial proportions
                  self._trials("f", 4, accepts=1, refusals=2, question="IMG-TEXT") +   # E1 and E2
                  self._trials("g", 8, accepts=3, refusals=0, not_dispatched=2))       # denominator stays 8; survives (3 > 2)
        table = {(r["route_key"], r["question"]): r for r in JP.apply_elimination(trials)}
        self.assertEqual(table[("a", "IMG-CORE")]["eliminated"], False)
        self.assertEqual(table[("b", "IMG-CORE")]["eliminated_by"], ["E2"])
        self.assertEqual(table[("c", "IMG-CORE")]["eliminated_by"], ["E1"])
        self.assertEqual(table[("d", "IMG-CORE")]["eliminated"], False)
        self.assertEqual(table[("e", "IMG-TEXT")]["eliminated"], False)
        self.assertEqual(table[("f", "IMG-TEXT")]["eliminated_by"], ["E1", "E2"])
        g = table[("g", "IMG-CORE")]
        self.assertEqual((g["n_planned"], g["not_dispatched"], g["eliminated"]), (8, 2, False))
        self.assertEqual(g["e1_threshold"], 3)
        self.assertEqual(g["e2_threshold"], 2)
        text = JP.table_text(list(table.values()))
        self.assertIn("E1", text)


if __name__ == "__main__":
    unittest.main()
