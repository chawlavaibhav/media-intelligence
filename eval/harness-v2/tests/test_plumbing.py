"""EVAL-041 part 2 plumbing: the input resolver, fixture mode, the roster-price option, the per-frame video composite
and the video smoke path. Fake transports only; no socket, no key, no queue submit; hb-view is never needed (a stub
glyph renderer is injected). ffmpeg/ffprobe are LOCAL tools and are used for the tiny test clip.
"""
import base64
import hashlib
import json
import os
import unittest
from decimal import Decimal
from pathlib import Path

import yaml

from _support import NoNetworkTestCase, fixed_clock, hv2_paths
import casebook as CB
import composite as CP
import fixtures as FX
import inputs as INP
import run_live as RL
import store as S
import surfaces
import transports as T
from instruments import imageio as IO
from providers import PreDispatchRefusal

STAND_IN_SPEC = hv2_paths.EVAL_ROOT / "experiments" / "EVAL-040" / "fixtures" / "STAND-IN-SPEC.yaml"
CANARY = "CANARY-fal-key-value-5e4d3c2b1a09"


def png_bytes(w: int = 24, h: int = 32, rgb=(200, 120, 40)) -> bytes:
    return IO.encode_png([bytes(rgb) * w for _ in range(h)], w, h, 3)


def stub_render(text, font, size_pt, colour_hex, scratch):
    """An opaque 8 x 4 block in the requested colour: what hb-view would give, without hb-view."""
    r, g, b = (int(colour_hex[i:i + 2], 16) for i in (0, 2, 4))
    w, h = 8, 4
    return IO.Image(w, h, 4, bytes([r, g, b, 255]) * (w * h))


def fal_image_transport(png: bytes) -> T.FakeTransport:
    return T.FakeTransport(
        posts=[(200, {"request_id": "req-1", "status_url": "https://queue.fal.run/x/requests/req-1/status",
                      "response_url": "https://queue.fal.run/x/requests/req-1", "status": "IN_QUEUE"})],
        gets=[(200, {"status": "COMPLETED"}), (200, {"images": [{"url": "https://v3.fal.media/files/fake/out.png", "content_type": "image/png"}]})],
        downloads=[(200, png, "image/png")])


def fal_video_transport(mp4: bytes) -> T.FakeTransport:
    return T.FakeTransport(
        posts=[(200, {"request_id": "req-v", "status_url": "https://queue.fal.run/x/requests/req-v/status",
                      "response_url": "https://queue.fal.run/x/requests/req-v", "status": "IN_QUEUE"})],
        gets=[(202, {"status": "IN_PROGRESS"}), (200, {"status": "COMPLETED"}), (200, {"video": {"url": "https://v3.fal.media/files/fake/out.mp4", "content_type": "video/mp4"}})],
        downloads=[(200, mp4, "video/mp4")])


def vertex_image_transport(png: bytes) -> T.FakeTransport:
    return T.FakeTransport(posts=[(200, {"responseId": "resp-1", "candidates": [{"finishReason": "STOP", "content": {"parts": [
        {"inlineData": {"mimeType": "image/png", "data": base64.b64encode(png).decode("ascii")}}]}}]})])


def veo_video_transport(mp4: bytes) -> T.FakeTransport:
    op = "projects/p/locations/us-central1/publishers/google/models/m/operations/op-1"
    return T.FakeTransport(posts=[(200, {"name": op}), (200, {"name": op, "done": False}),
                                  (200, {"name": op, "done": True, "response": {"raiMediaFilteredCount": 0,
                                                                                "videos": [{"bytesBase64Encoded": base64.b64encode(mp4).decode("ascii"), "mimeType": "video/mp4"}]}})])


class Factory:
    """transport_factory(entry, trial): per surface / media kind; records every transport and every payload."""

    def __init__(self, png=None, mp4=None):
        self.png = png or png_bytes()
        self.mp4 = mp4
        self.transports = []

    def __call__(self, entry, trial):
        if entry.surface == "fal":
            t = fal_video_transport(self.mp4) if entry.media_kind == "video" else fal_image_transport(self.png)
        elif entry.adapter == "vertex_veo":
            t = veo_video_transport(self.mp4)
        else:
            t = vertex_image_transport(self.png)
        self.transports.append(t)
        return t

    @property
    def submits(self):
        return sum(t.submits for t in self.transports)

    def payloads(self):
        return [c["payload"] for t in self.transports for c in t.calls if c["kind"] == "post" and c["payload"]]


class PlumbingBase(NoNetworkTestCase):
    def setUp(self):
        super().setUp()
        os.environ["FAL_KEY"] = CANARY
        os.environ["GOOGLE_API_KEY"] = "FAKE-GOOGLE-API-KEY-NOT-A-CREDENTIAL"   # the Gemini routes read this name (2026-09-09)
        self.runs = self.tmp / "runs"
        self.auth = self.write_auth()
        self.adapter_kwargs = {"token_source": T.FakeTokenSource(), "sleep": lambda s: None, "clock": fixed_clock()}
        self.gate = self.tmp / "no-gate.py"

    # -- fake sealed stores -----------------------------------------------------------------
    def seal_fixture(self, run_id, fixture_id, data, *, is_decoy=False, for_case="IMG-EDIT-01", role="supplied_subject", synthetic=True, ct="image/png"):
        store = S.SealedStore(self.runs / run_id / "artifacts")
        art = store.seal(FX.trial_id_for(fixture_id, "nano-banana-2"), data, ct, {"constructed_synthetic": True})
        rec = {"fixture_id": fixture_id, "for_case": for_case, "role": role, "is_decoy": is_decoy, "constructed_synthetic": synthetic,
               "relative_path": art["relative_path"], "sha256": art["sha256"], "bytes": art["bytes"], "content_type": ct, "prompt": "p"}
        p = FX.fixture_record_path(self.runs / run_id, fixture_id)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(rec))
        return art

    def seal_trial(self, run_id, trial_id, data, ct="image/png", suffix=""):
        store = S.SealedStore(self.runs / run_id / "artifacts")
        return store.seal(trial_id, data, ct, {}, suffix=suffix)

    def inputs_file(self, lines, name="INPUTS.yaml"):
        return INP.write_inputs_file(self.tmp / name, lines, runs_root=self.runs)

    def runner(self, out, run_id, factory, auth=None):
        return RL.LiveRunner(out, run_id, auth_path=auth or self.auth, transport_factory=factory, adapter_kwargs=self.adapter_kwargs, gate_script=self.gate)


# ============================================================================ resolver
class ResolverTest(PlumbingBase):
    def test_fal_edit_gets_a_data_uri_of_the_sealed_bytes_and_the_plan_records_the_sha(self):
        png = png_bytes()
        self.seal_fixture("fx", "showroom_sofa_01", png)
        f = INP.InputsFile(self.inputs_file([{"case_id": "IMG-EDIT-01", "arm": "edit", "role": "reference_asset_1", "ref": "fixture:fx:showroom_sofa_01"}]))
        book = CB.CaseBook.from_git("HEAD")
        row = book.row("IMG-EDIT-01", "flux-2-pro-edit")
        inputs, resolved, unresolved = INP.InputResolver(f).for_row(row, surfaces.REGISTRY.get("flux-2-pro-edit"))
        self.assertEqual(unresolved, [])
        self.assertEqual(list(inputs), ["image_urls"])
        uri = inputs["image_urls"][0]
        self.assertTrue(uri.startswith("data:image/png;base64,"))
        self.assertEqual(base64.b64decode(uri.split(",", 1)[1]), png)
        self.assertEqual(resolved[0]["sha256"], hashlib.sha256(png).hexdigest())
        self.assertTrue(resolved[0]["constructed_synthetic"])
        self.assertNotIn("data", resolved[0], "the plan summary never carries bytes")
        # the SAME builder renders the body with the data URI, so the sha commits to the input bytes
        from adapters import adapter_for
        import pricing as PR
        ad = adapter_for(surfaces.REGISTRY.get("flux-2-pro-edit"), pricing=PR.Pricing())
        d = ad.dry_run(row, inputs)
        self.assertTrue(d["would_dispatch"], d["refusal_reason"])
        self.assertEqual(d["body"]["image_urls"], [uri])

    def test_vertex_shapes_bytes_for_veo_i2v_and_reference_images_for_gemini_edit(self):
        png = png_bytes()
        self.seal_trial("prev", "IMG-CORE-01__gpt-image-2__core__r1", png)
        f = INP.InputsFile(self.inputs_file([{"case_id": "VID-I2V-01", "role": "plate_accepted_draw", "ref": "prev:IMG-CORE-01__gpt-image-2__core__r1"}]))
        book = CB.CaseBook.from_git("HEAD")
        row = book.row("VID-I2V-01", "veo-3.1-fast-i2v")
        inputs, resolved, unresolved = INP.InputResolver(f).for_row(row, surfaces.REGISTRY.get("veo-3.1-fast-i2v"))
        self.assertEqual((inputs["image_bytes"], inputs["image_mime"], unresolved), (png, "image/png", []))
        self.assertEqual(resolved[0]["kind"], "trial")
        from adapters import adapter_for
        import pricing as PR
        d = adapter_for(surfaces.REGISTRY.get("veo-3.1-fast-i2v"), pricing=PR.Pricing()).dry_run(row, inputs)
        self.assertEqual(d["body"]["instances"][0]["image"], {"bytesBase64Encoded": base64.b64encode(png).decode("ascii"), "mimeType": "image/png"})
        # a Gemini image edit takes (bytes, mime) reference images
        entry = surfaces.REGISTRY.get("nano-banana-pro")
        fake_row = {**book.row("IMG-EDIT-01", "nano-banana-pro-edit"), "route_key": "nano-banana-pro"}
        needed = INP.roles_needed(entry, fake_row)
        self.assertEqual(needed, [("reference_asset_1", "reference_images")])
        built = INP.build_inputs(entry, needed, {"reference_asset_1": f.load(f.entries[0])})
        self.assertEqual(built["reference_images"], [(png, "image/png")])

    def test_unmapped_role_stays_pending_and_the_row_refuses(self):
        f = INP.InputsFile(self.inputs_file([]))
        book = CB.CaseBook.from_git("HEAD")
        row = book.row("IMG-COMP-01", "seedream-5-pro-edit")
        inputs, resolved, unresolved = INP.InputResolver(f).for_row(row, surfaces.REGISTRY.get("seedream-5-pro-edit"))
        self.assertEqual((inputs, resolved, unresolved), ({}, [], ["reference_asset_1", "reference_asset_2"]))
        from adapters import adapter_for
        import pricing as PR
        d = adapter_for(surfaces.REGISTRY.get("seedream-5-pro-edit"), pricing=PR.Pricing()).dry_run(row, inputs)
        self.assertFalse(d["would_dispatch"])
        self.assertIn("input_unresolved:reference_asset_1,reference_asset_2", d["refusal_reason"])

    def test_sha_verification_refuses_altered_bytes_and_a_wrong_pin(self):
        png = png_bytes()
        art = self.seal_fixture("fx", "tin_front", png)
        f = INP.InputsFile(self.inputs_file([{"case_id": "IMG-REF-01", "role": "reference_asset_1", "ref": "fixture:fx:tin_front", "sha256": "0" * 64}]))
        with self.assertRaises(INP.InputsError) as cm:
            f.load(f.entries[0])
        self.assertIn("INPUTS pins sha256", str(cm.exception))
        media = self.runs / "fx" / "artifacts" / art["relative_path"]
        media.write_bytes(png_bytes(rgb=(1, 2, 3)))                 # altered on disk after sealing
        f2 = INP.InputsFile(self.inputs_file([{"case_id": "IMG-REF-01", "role": "reference_asset_1", "ref": "fixture:fx:tin_front"}], name="I2.yaml"))
        with self.assertRaises(INP.InputsError) as cm:
            f2.load(f2.entries[0])
        self.assertIn("altered", str(cm.exception))

    def test_decoys_are_never_sent(self):
        self.seal_fixture("fx", "model_portrait", png_bytes(), for_case="IMG-COMP-01", role="identity_person")
        self.seal_fixture("fx", "model_portrait_decoy_1", png_bytes(rgb=(9, 9, 9)), is_decoy=True, for_case="IMG-COMP-01", role="decoy")
        self.seal_fixture("fx", "shade_ruby_pack", png_bytes(rgb=(150, 0, 20)), for_case="IMG-COMP-01", role="identity_product")
        f = INP.InputsFile(self.inputs_file([
            {"case_id": "IMG-COMP-01", "role": "reference_asset_1", "ref": "fixture:fx:model_portrait_decoy_1"},
            {"case_id": "IMG-COMP-01", "role": "reference_asset_2", "ref": "fixture:fx:shade_ruby_pack"}]))
        book = CB.CaseBook.from_git("HEAD")
        row = book.row("IMG-COMP-01", "flux-2-pro-edit")
        with self.assertRaises(INP.InputsError) as cm:
            INP.InputResolver(f).for_row(row, surfaces.REGISTRY.get("flux-2-pro-edit"))
        self.assertIn("DECOY", str(cm.exception))
        # the rule reaches the plan: a decoy in INPUTS refuses the whole plan, nothing is written
        out = self.tmp / "p-decoy"
        with self.assertRaises(RL.PlanRefused):
            RL.build_plan(out, "p-decoy", cases=["IMG-COMP-01"], routes=["flux-2-pro-edit"], tranche="1a", auth_path=self.auth, inputs_path=f.path)
        self.assertFalse((out / "PLAN.yaml").exists())

    def test_multi_reference_order_identity_views_first_in_role_order(self):
        views = {"tin_front": png_bytes(rgb=(1, 1, 1)), "tin_side": png_bytes(rgb=(2, 2, 2)), "tin_top": png_bytes(rgb=(3, 3, 3))}
        for k, v in views.items():
            self.seal_fixture("fx", k, v, for_case="IMG-REF-01", role="identity_product")
        # mapped in a scrambled order on purpose: the ROLE index decides, not the file order
        f = INP.InputsFile(self.inputs_file([
            {"case_id": "IMG-REF-01", "role": "reference_asset_3", "ref": "fixture:fx:tin_top"},
            {"case_id": "IMG-REF-01", "role": "reference_asset_1", "ref": "fixture:fx:tin_front"},
            {"case_id": "IMG-REF-01", "role": "reference_asset_2", "ref": "fixture:fx:tin_side"}]))
        book = CB.CaseBook.from_git("HEAD")
        row = book.row("IMG-REF-01", "nano-banana-pro-edit")
        inputs, resolved, unresolved = INP.InputResolver(f).for_row(row, surfaces.REGISTRY.get("nano-banana-pro-edit"))
        # 2026-09-09: nano-banana-pro-edit runs on the Gemini API (inline reference bytes), no longer on fal (data URIs)
        self.assertEqual([b for b, _ in inputs["reference_images"]], [views["tin_front"], views["tin_side"], views["tin_top"]])
        self.assertEqual({m for _, m in inputs["reference_images"]}, {"image/png"})
        self.assertEqual([r["role"] for r in resolved], ["reference_asset_1", "reference_asset_2", "reference_asset_3"])
        # IMG-COMP-01: the portrait first, then the packshot
        self.seal_fixture("fx", "model_portrait", png_bytes(rgb=(4, 4, 4)), for_case="IMG-COMP-01", role="identity_person")
        self.seal_fixture("fx", "shade_ruby_pack", png_bytes(rgb=(5, 5, 5)), for_case="IMG-COMP-01", role="identity_product")
        f2 = INP.InputsFile(self.inputs_file([
            {"case_id": "IMG-COMP-01", "role": "reference_asset_1", "ref": "fixture:fx:model_portrait"},
            {"case_id": "IMG-COMP-01", "role": "reference_asset_2", "ref": "fixture:fx:shade_ruby_pack"}], name="I2.yaml"))
        inputs, resolved, _ = INP.InputResolver(f2).for_row(book.row("IMG-COMP-01", "seedream-5-pro-edit"), surfaces.REGISTRY.get("seedream-5-pro-edit"))
        self.assertEqual([r["fixture_role"] for r in resolved], ["identity_person", "identity_product"])
        self.assertEqual(len(inputs["image_urls"]), 2)

    def test_arm_specific_line_beats_wildcard_and_refs_parse(self):
        f = INP.InputsFile(self.inputs_file([
            {"case_id": "VID-TOPO3-01", "arm": "*", "role": "plate_accepted_draw", "ref": "plates:X"},
            {"case_id": "VID-TOPO3-01", "arm": "C_textless_plate_i2v_composite", "role": "plate_accepted_draw", "ref": "plates:Y:composite"}]))
        self.assertEqual(f.entries_for("VID-TOPO3-01", "A_cheap_still_to_cheap_i2v")["plate_accepted_draw"]["ref"], "plates:X")
        self.assertEqual(f.entries_for("VID-TOPO3-01", "C_textless_plate_i2v_composite")["plate_accepted_draw"]["ref"], "plates:Y:composite")
        self.assertEqual(INP.parse_ref("plates:Y:composite"), {"kind": "trial", "run_id": "plates", "artifact_id": "Y", "suffix": "composite"})
        for bad in ("", "fixture:only", "a:b:c:d"):
            with self.assertRaises(INP.InputsError):
                INP.parse_ref(bad)


# ============================================================================ plan + execute with inputs
class PlanWithInputsTest(PlumbingBase):
    def _half_two_inputs(self):
        self.seal_fixture("fx", "showroom_sofa_01", png_bytes(rgb=(60, 60, 60)))
        return self.inputs_file([{"case_id": "IMG-EDIT-01", "role": "reference_asset_1", "ref": "fixture:fx:showroom_sofa_01"}])

    def test_plan_commits_to_the_input_bytes_and_execute_sends_the_data_uri(self):
        ipath = self._half_two_inputs()
        out = self.tmp / "h2"
        plan = RL.build_plan(out, "h2", cases=["IMG-EDIT-01"], routes=["flux-2-pro-edit", "nano-banana-pro-edit"], tranche="1a", auth_path=self.auth, inputs_path=ipath)
        self.assertEqual(len(plan["trials"]), 4)
        self.assertEqual(plan["header"]["inputs_file"]["sha256"], hashlib.sha256(ipath.read_bytes()).hexdigest())
        t = plan["trials"][0]
        self.assertEqual(t["inputs"][0]["role"], "reference_asset_1")
        self.assertTrue(t["constructed_synthetic_inputs"])
        self.assertNotIn("base64", (out / "PLAN.yaml").read_text(), "the plan carries sha256s, never bytes")
        # a different input -> a different body sha
        self.seal_fixture("fx2", "showroom_sofa_01", png_bytes(rgb=(61, 61, 61)))
        ipath2 = self.inputs_file([{"case_id": "IMG-EDIT-01", "role": "reference_asset_1", "ref": "fixture:fx2:showroom_sofa_01"}], name="I2.yaml")
        plan2 = RL.build_plan(self.tmp / "h2b", "h2b", cases=["IMG-EDIT-01"], routes=["flux-2-pro-edit"], tranche="1a", auth_path=self.auth, inputs_path=ipath2)
        self.assertNotEqual(plan2["trials"][0]["body_sha256"], t["body_sha256"])
        factory = Factory()
        summary = self.runner(out, "h2", factory).execute()
        self.assertEqual((summary["status"], summary["dispatched"]), ("completed", 4))
        sent = json.loads(factory.payloads()[0])
        self.assertTrue(sent["image_urls"][0].startswith("data:image/png;base64,"))
        self.assertEqual(hashlib.sha256(base64.b64decode(sent["image_urls"][0].split(",", 1)[1])).hexdigest(), t["inputs"][0]["sha256"])
        for p in out.rglob("*"):
            if p.is_file():
                self.assertNotIn(CANARY.encode(), p.read_bytes(), str(p))

    def test_execute_refuses_a_changed_inputs_file(self):
        ipath = self._half_two_inputs()
        out = self.tmp / "h3"
        RL.build_plan(out, "h3", cases=["IMG-EDIT-01"], routes=["flux-2-pro-edit"], tranche="1a", auth_path=self.auth, inputs_path=ipath)
        ipath.write_text(ipath.read_text() + "# touched\n")
        factory = Factory()
        with self.assertRaises(RL.PlanRefused):
            self.runner(out, "h3", factory).execute()
        self.assertEqual(factory.submits, 0)

    def test_execute_refuses_a_swapped_input(self):
        ipath = self._half_two_inputs()
        out = self.tmp / "h4"
        RL.build_plan(out, "h4", cases=["IMG-EDIT-01"], routes=["flux-2-pro-edit"], tranche="1a", auth_path=self.auth, inputs_path=ipath)
        # swap the fixture behind the same id: new bytes + a matching record (an attacker with disk access, or a re-run over the same id)
        rec_path = FX.fixture_record_path(self.runs / "fx", "showroom_sofa_01")
        rec = json.loads(rec_path.read_text())
        new = png_bytes(rgb=(99, 99, 99))
        (self.runs / "fx" / "artifacts" / rec["relative_path"]).write_bytes(new)
        rec.update(sha256=hashlib.sha256(new).hexdigest(), bytes=len(new))
        rec_path.write_text(json.dumps(rec))
        factory = Factory()
        summary = self.runner(out, "h4", factory).execute()
        self.assertEqual(factory.submits, 0, "nothing was sent")
        self.assertEqual(summary["dispatched"], 0)
        refusals = list((out / "trials").glob("*.pre_dispatch_refusal.json"))
        self.assertEqual(len(refusals), 2)
        self.assertIn("swapped", json.loads(refusals[0].read_text())["reason"])
        rows = [json.loads(l) for l in (out / "ledger" / "h4" / "spend-ledger.jsonl").read_text().splitlines()] if (out / "ledger" / "h4" / "spend-ledger.jsonl").exists() else []
        self.assertEqual([r["type"] for r in rows if r["type"] == "spend"], [])

    def test_plan_without_inputs_excludes_input_rows_with_the_role_named(self):
        with self.assertRaises(RL.PlanRefused) as cm:
            RL.build_plan(self.tmp / "h5", "h5", cases=["IMG-EDIT-01"], routes=["flux-2-pro-edit"], tranche="1a", auth_path=self.auth)
        self.assertIn("input_unresolved:reference_asset_1", str(cm.exception))


# ============================================================================ price mismatch option
class RosterPriceTest(PlumbingBase):
    def _comp_inputs(self):
        self.seal_fixture("fx", "model_portrait", png_bytes(rgb=(4, 4, 4)), for_case="IMG-COMP-01", role="identity_person")
        self.seal_fixture("fx", "shade_ruby_pack", png_bytes(rgb=(5, 5, 5)), for_case="IMG-COMP-01", role="identity_product")
        return self.inputs_file([{"case_id": "IMG-COMP-01", "role": "reference_asset_1", "ref": "fixture:fx:model_portrait"},
                                 {"case_id": "IMG-COMP-01", "role": "reference_asset_2", "ref": "fixture:fx:shade_ruby_pack"}])

    def test_mismatch_row_refuses_explicitly_with_both_prices_and_dispatches_at_the_roster_price_on_request(self):
        ipath = self._comp_inputs()
        with self.assertRaises(RL.PlanRefused) as cm:
            RL.build_plan(self.tmp / "r1", "r1", cases=["IMG-COMP-01"], routes=["flux-2-pro-edit"], tranche="1a", auth_path=self.auth, inputs_path=ipath)
        msg = str(cm.exception)
        self.assertIn("price_mismatch", msg)
        self.assertIn("cost_table 0.045 vs roster 0.060", msg)
        self.assertIn("--accept-roster-price", msg)
        out = self.tmp / "r2"
        plan = RL.build_plan(out, "r2", cases=["IMG-COMP-01"], routes=None, tranche="1a", auth_path=self.auth,
                             inputs_path=ipath, accept_roster_price=True)
        flux = [t for t in plan["trials"] if t["route_key"] == "flux-2-pro-edit"]
        seed = [t for t in plan["trials"] if t["route_key"] != "flux-2-pro-edit"]
        self.assertEqual(len(flux), 2)
        self.assertEqual(len(plan["trials"]), 6, "flux at the roster price + nano-banana-pro-edit + seedream, two repeats each")
        self.assertEqual({t["price_basis"] for t in flux}, {"roster_over_cost_table"})
        self.assertEqual({t["price_basis"] for t in seed}, {"cost_table"})
        self.assertEqual((flux[0]["unit_price"], flux[0]["cost_table_unit_price"], flux[0]["roster_implied_usd"]), ("0.060", "0.045", "0.060"))
        self.assertEqual(Decimal(flux[0]["estimated_usd_equiv"]), Decimal("0.06"))
        self.assertEqual(plan["header"]["accept_roster_price"], True)
        self.assertEqual(sorted(plan["header"]["roster_price_trials"]), sorted(t["trial_id"] for t in flux))
        gpt = [e for e in plan["excluded"] if e["route_key"] == "gpt-image-2-edit"]
        self.assertTrue(gpt and all("price_unpinned" in e["reason"] for e in gpt), "the token-metered edit stays excluded")
        factory = Factory()
        summary = self.runner(out, "r2", factory).execute()
        self.assertEqual((summary["status"], summary["dispatched"]), ("completed", 6))
        rows = [json.loads(l) for l in (out / "ledger" / "r2" / "spend-ledger.jsonl").read_text().splitlines()]
        flux_spend = [Decimal(str(r["amount_usd"])) for r in rows if r["type"] == "spend" and r.get("route_key") == "flux-2-pro-edit"]
        self.assertEqual(flux_spend, [Decimal("0.06"), Decimal("0.06")], "the ledger charges the roster price, the higher one")

    def test_the_option_never_touches_a_single_reference_row(self):
        self.seal_fixture("fx", "showroom_sofa_01", png_bytes())
        ipath = self.inputs_file([{"case_id": "IMG-EDIT-01", "role": "reference_asset_1", "ref": "fixture:fx:showroom_sofa_01"}])
        plan = RL.build_plan(self.tmp / "r3", "r3", cases=["IMG-EDIT-01"], routes=["flux-2-pro-edit"], tranche="1a", auth_path=self.auth,
                             inputs_path=ipath, accept_roster_price=True)
        self.assertEqual({t["price_basis"] for t in plan["trials"]}, {"cost_table"})
        self.assertEqual(plan["trials"][0]["unit_price"], "0.045")


# ============================================================================ fixtures mode
SMALL_SPEC = """
package: test
generation_route: nano-banana-2
derivation_route: nano-banana-pro-edit
assets:
  - id: sofa
    for: IMG-EDIT-01
    role: supplied_subject
    kind: generate
    prompt: a sofa
    aspect: "4:3"
    record_srgb_of: the sofa fabric
    decoys:
      - {id: sofa_decoy_1, prompt: another sofa}
  - id: tin_front
    for: IMG-REF-01
    role: identity_product
    kind: generate_then_overlay
    prompt: a blank tin
    aspect: "1:1"
    overlay:
      - {text: "सरसों तेल", script: devanagari, size_pt: 44, colour: "B3000C", anchor: center, y_frac: 0.42}
    exact_strings_by_code: true
    derived_views:
      - {id: tin_side, edit_prompt: same tin from the side}
counts: {nominal_usd: 0.35}
"""


class FixturesModeTest(PlumbingBase):
    def setUp(self):
        super().setUp()
        self.spec = self.tmp / "SPEC.yaml"
        self.spec.write_text(SMALL_SPEC)
        self.out = self.tmp / "runs" / "fx"

    def fx_runner(self, factory, auth=None):
        return FX.FixtureRunner(self.out, "fx", auth or self.auth, factory, self.adapter_kwargs, render_text=stub_render)

    def test_dry_plan_orders_generate_overlay_derive_and_prices_from_the_roster(self):
        plan = FX.build_fixture_plan(self.out, "fx", self.spec, self.auth)
        kinds = [(s["kind"], s["fixture_id"]) for s in plan["steps"]]
        self.assertEqual(kinds, [("generate", "sofa"), ("generate", "sofa_decoy_1"), ("generate", "tin_front__raw"), ("overlay", "tin_front"), ("derive", "tin_side")])
        # the derivation route (nano-banana-pro-edit) prices at the roster's Gemini API line, 0.134 per 1K/2K output image (re-pointed 2026-09-10; was fal 0.15)
        self.assertEqual(Decimal(plan["header"]["estimated_total_usd_equiv"]), Decimal("0.067") * 3 + Decimal("0.134"))
        gen, ov, der = plan["steps"][0], plan["steps"][3], plan["steps"][4]
        self.assertTrue(gen["body_sha256"] and gen["template_body_sha256"] is None)
        self.assertTrue(der["template_body_sha256"] and der["body_sha256"] is None)
        self.assertEqual(der["parent_fixture_id"], "tin_front")
        self.assertEqual(ov["parent_fixture_id"], "tin_front__raw")
        self.assertTrue(plan["steps"][1]["is_decoy"] and plan["steps"][1]["decoy_of"] == "sofa")
        self.assertTrue((self.out / "FIXTURE-PLAN.yaml").exists() and (self.out / "FIXTURE-PLAN.sha256").exists())
        with self.assertRaises(FX.FixturePlanRefused):
            FX.build_fixture_plan(self.out, "fx", self.spec, self.auth)
        self.assertNotIn(CANARY, (self.out / "FIXTURE-PLAN.yaml").read_text())

    def test_execute_generates_overlays_derives_with_the_parent_and_seals_fixture_records(self):
        FX.build_fixture_plan(self.out, "fx", self.spec, self.auth)
        factory = Factory(png=png_bytes(rgb=(200, 200, 40)))
        summary = self.fx_runner(factory).execute()
        self.assertEqual((summary["status"], summary["dispatched"], summary["overlaid"], summary["errors"]), ("completed", 4, 1, []))
        self.assertEqual(factory.submits, 4)
        recs = {fid: json.loads(FX.fixture_record_path(self.out, fid).read_text()) for fid in ("sofa", "sofa_decoy_1", "tin_front__raw", "tin_front", "tin_side")}
        for r in recs.values():
            self.assertTrue(r["constructed_synthetic"] and r["never_a_customer_photo"])
            self.assertTrue((self.out / "artifacts" / r["relative_path"]).exists())
            self.assertEqual(hashlib.sha256((self.out / "artifacts" / r["relative_path"]).read_bytes()).hexdigest(), r["sha256"])
        self.assertEqual((recs["sofa"]["for_case"], recs["sofa"]["role"], recs["sofa"]["prompt"]), ("IMG-EDIT-01", "supplied_subject", "a sofa"))
        self.assertTrue(recs["sofa_decoy_1"]["is_decoy"])
        self.assertEqual(recs["sofa"]["record_srgb_of"], "the sofa fabric")
        self.assertEqual(recs["sofa"]["central_srgb"]["mean_srgb"], [200, 200, 40])
        # the overlay changed the picture (its sha differs from the raw draw) and recorded the placed string
        self.assertNotEqual(recs["tin_front"]["sha256"], recs["tin_front__raw"]["sha256"])
        self.assertEqual(recs["tin_front"]["parent_sha256"], recs["tin_front__raw"]["sha256"])
        self.assertEqual(recs["tin_front"]["overlay"]["strings"][0]["text"], "सरसों तेल")
        self.assertTrue(recs["tin_front"]["overlay"]["exact_strings_by_code"])
        # the derive call carried the OVERLAID parent inline (2026-09-09: the derivation route nano-banana-pro-edit runs on the Gemini API,
        # reference bytes as inlineData, no longer a fal data URI), and the record names the parent's sha
        derive_payload = json.loads([p for p in factory.payloads() if b"inlineData" in p][0])
        sent = base64.b64decode([part for part in derive_payload["contents"][0]["parts"] if "inlineData" in part][0]["inlineData"]["data"])
        self.assertEqual(hashlib.sha256(sent).hexdigest(), recs["tin_front"]["sha256"])
        self.assertEqual(recs["tin_side"]["parent_sha256"], recs["tin_front"]["sha256"])
        self.assertEqual(recs["tin_side"]["parent_fixture_id"], "tin_front")
        # ledger: reservation + spend per PAID step, nothing for the overlay
        rows = [json.loads(l) for l in (self.out / "ledger" / "fx" / "spend-ledger.jsonl").read_text().splitlines()]
        self.assertEqual([r["type"] for r in rows], ["reservation", "spend"] * 4)
        self.assertEqual(sum(Decimal(str(r["amount_usd"])) for r in rows if r["type"] == "spend"), Decimal("0.067") * 3 + Decimal("0.134"))
        # the resolver accepts the sealed fixtures for the battery (and still refuses the decoy)
        f = INP.InputsFile(self.inputs_file([{"case_id": "IMG-REF-01", "role": "reference_asset_1", "ref": "fixture:fx:tin_front"},
                                             {"case_id": "IMG-REF-01", "role": "reference_asset_2", "ref": "fixture:fx:tin_side"},
                                             {"case_id": "IMG-REF-01", "role": "reference_asset_3", "ref": "fixture:fx:sofa_decoy_1"}]))
        self.assertEqual(f.load(f.entries[0]).sha256, recs["tin_front"]["sha256"])
        with self.assertRaises(INP.InputsError):
            f.load(f.entries[2])
        for p in self.out.rglob("*"):
            if p.is_file():
                self.assertNotIn(CANARY.encode(), p.read_bytes(), str(p))

    def test_resumable_and_derive_waits_for_its_parent(self):
        FX.build_fixture_plan(self.out, "fx", self.spec, self.auth)
        factory = Factory()
        first = self.fx_runner(factory).execute(max_dispatches=2)
        self.assertEqual((first["status"], first["dispatched"]), ("paused_max_dispatches", 2))
        second = self.fx_runner(factory).execute()
        self.assertEqual((second["status"], second["skipped"], second["dispatched"], second["overlaid"]), ("completed", 2, 2, 1))
        self.assertEqual(factory.submits, 4)
        third = self.fx_runner(factory).execute()
        self.assertEqual((third["skipped"], third["dispatched"]), (5, 0))

    def test_cap_stops_before_anything_is_sent(self):
        FX.build_fixture_plan(self.out, "fx", self.spec, self.auth)
        auth = self.write_auth(ceiling="0.10", caps=("0.10", "0.00"), name="tiny.yaml")
        factory = Factory()
        summary = self.fx_runner(factory, auth=auth).execute()
        self.assertEqual((summary["status"], summary["dispatched"], factory.submits), ("stopped_cap_reached", 1, 1))
        rows = [json.loads(l) for l in (self.out / "ledger" / "fx" / "spend-ledger.jsonl").read_text().splitlines()]
        self.assertEqual([r["type"] for r in rows], ["reservation", "spend"])

    def test_execute_refuses_a_changed_plan_and_needs_authorisation(self):
        FX.build_fixture_plan(self.out, "fx", self.spec, self.auth)
        p = self.out / "FIXTURE-PLAN.yaml"
        p.write_text(p.read_text().replace("a sofa", "a chair"))
        factory = Factory()
        with self.assertRaises(FX.FixturePlanRefused):
            self.fx_runner(factory).execute()
        self.assertEqual(factory.submits, 0)
        from budget_guard import NotAuthorised
        with self.assertRaises(NotAuthorised):
            FX.build_fixture_plan(self.tmp / "fx-none", "fx-none", self.spec, self.tmp / "absent.yaml")

    def test_real_stand_in_spec_dry_plan_is_within_the_sizing(self):
        plan = FX.build_fixture_plan(self.tmp / "real-dry", "real-dry", STAND_IN_SPEC, self.auth)
        c = plan["header"]["counts"]
        # the spec's own sum line (1+1+1+1+2+1+2+1+2+1+2) is 15 generations (7 assets + 8 decoys), not the 13 it wrote; the
        # derivation route prices at the roster's pinned Gemini API number (0.134 since the 2026-09-10 re-point; the fal 0.15 it
        # carried before made this 1.605) -> USD 1.541, inside the "<= 1.6" sizing and well inside the half-two cap (7.34).
        self.assertEqual((c["generate"], c["decoys"], c["overlay"], c["derive"]), (15, 8, 3, 4))
        total = Decimal(plan["header"]["estimated_total_usd_equiv"])
        self.assertEqual(total, Decimal("0.067") * 15 + Decimal("0.134") * 4)
        self.assertEqual(total, Decimal("1.541"))
        self.assertLessEqual(total, Decimal("7.34"))
        for s in plan["steps"]:
            if s["kind"] == "derive":
                self.assertIn(s["parent_fixture_id"], ("tin_front", "host_ref_1"))
        self.assertEqual([s["fixture_id"] for s in plan["steps"] if s["kind"] == "overlay"], ["masala_pack_raw", "backwaters_banner_16x9", "tin_front"])


# ============================================================================ video composite
class VideoCompositeTest(PlumbingBase):
    def _clip(self, name="plate.mp4", seconds=1.0, fps=10, with_audio=False):
        return IO.make_test_video(self.tmp / name, width=64, height=48, seconds=seconds, fps=fps, with_audio=with_audio)

    def test_every_frame_is_overlaid_and_the_fps_is_kept(self):
        clip = self._clip()
        spec = {"strings": [{"id": "t1", "text": "X", "script": "latin", "size_pt": 10, "colour": "FF0000", "anchor": "center", "y_frac": 0.5}]}
        fonts = {"latin": {"file": "unused-by-the-stub", "face_index": 0}}
        out, placed, info = CP.composite_video(clip, spec, fonts, self.tmp, self.tmp / "out.mp4", render_text=stub_render)
        self.assertEqual(info["frames"], 10)
        self.assertEqual(info["source_fps"], "10/1")
        probe = IO.ffprobe(out)
        self.assertEqual((probe["width"], probe["height"], probe["fps"], probe["has_audio"]), (64, 48, 10.0, False))
        self.assertAlmostEqual(probe["duration_s"], 1.0, delta=0.15)
        x0, y0, w, h = placed[0]["box"]
        for frame in IO.decode_video_frames(out, ("first", "middle", "last")):
            px = frame.data[((y0 + h // 2) * 64 + x0 + w // 2) * 3:][:3]
            self.assertGreater(px[0], 150, "red glyph present")
            self.assertLess(px[1], 90)
            self.assertLess(px[2], 90)

    def test_audio_stream_is_carried_over(self):
        clip = self._clip("plate-a.mp4", with_audio=True)
        spec = {"strings": [{"id": "t1", "text": "X", "script": "latin", "size_pt": 10, "colour": "00FF00", "anchor": "left", "x_frac": 0.1, "y_frac": 0.2}]}
        out, _, info = CP.composite_video(clip, spec, {"latin": {"file": "x"}}, self.tmp, self.tmp / "out-a.mp4", render_text=stub_render)
        self.assertTrue(info["audio_copied"])
        self.assertTrue(IO.ffprobe(out)["has_audio"])

    def test_run_video_seals_the_composite_under_the_clip_trial_with_suffix(self):
        out = self.tmp / "vrun"
        tid = "VID-TOPO3-01__minimax-h3-max-i2v__C_textless_plate_i2v_composite__r1"
        plan = {"header": {"plan": "EVAL-040-RUN-PLAN", "run_id": "vrun", "mode": "lane"},
                "trials": [{"seq": 1, "trial_id": tid, "case_id": "VID-TOPO3-01", "route_key": "minimax-h3-max-i2v", "arm": "C_textless_plate_i2v_composite", "repeat_index": 1},
                           {"seq": 2, "trial_id": "VID-TOPO3-01__veo-3.1-full__B_premium_native_t2v__r1", "case_id": "VID-TOPO3-01", "route_key": "veo-3.1-full",
                            "arm": "B_premium_native_t2v", "repeat_index": 1}], "excluded": []}
        out.mkdir(parents=True)
        (out / "PLAN.yaml").write_text(yaml.safe_dump(plan, sort_keys=False))
        (out / "PLAN.sha256").write_text(hashlib.sha256((out / "PLAN.yaml").read_bytes()).hexdigest() + "  PLAN.yaml\n")
        store = S.SealedStore(out / "artifacts")
        clip = self._clip("c.mp4")
        art = store.seal(tid, clip.read_bytes(), "video/mp4", {})
        store.write_attempt(tid, {"trial_id": tid, "status": "ok", "artifact": {k: art[k] for k in ("artifact_id", "relative_path", "bytes", "sha256", "content_type", "media_kind")}})
        font = self.tmp / "font.bin"
        font.write_bytes(b"not a font; the stub renderer never opens it")
        spec = self.tmp / "VSPEC.yaml"
        spec.write_text(yaml.safe_dump({"fonts": {"devanagari": {"file": str(font), "face_index": 0}},
                                        "cases": {"VID-TOPO3-01": {"strings": [{"id": "t3", "text": "श्री", "script": "devanagari", "size_pt": 12, "colour": "F5E9D3", "anchor": "center", "y_frac": 0.8}]}}}))
        rec = CP.run(out, "vrun", spec, video=True, render_text=stub_render)
        self.assertEqual(rec["mode"], "video")
        done = [c for c in rec["composites"] if "composite_sha256" in c]
        self.assertEqual([c["trial_id"] for c in done], [tid], "only the composite arm's clip; arm B is not a plate")
        self.assertEqual(done[0]["video"]["frames"], 10)
        sealed = out / "artifacts" / "media" / f"{tid}.composite.mp4"
        self.assertTrue(sealed.exists())
        self.assertEqual(IO.ffprobe(sealed)["fps"], 10.0)
        self.assertTrue((out / "COMPOSITE-RECORD-video.json").exists())
        self.assertEqual(rec["usd_spent"], 0)


# ============================================================================ video smoke path
class VideoSmokeTest(PlumbingBase):
    def setUp(self):
        super().setUp()
        self.mp4 = IO.make_test_video(self.tmp / "gen.mp4", width=72, height=128, seconds=1.0, fps=24, with_audio=False).read_bytes()

    def test_smoke_on_h3_max_i2v_dispatches_once_with_the_plate_and_runs_the_video_instruments(self):
        plate = png_bytes(w=72, h=128, rgb=(90, 10, 10))
        self.seal_trial("plates", "VID-TOPO3-01__qwen-image-3__A_plate_9x16__r1", plate)
        ipath = self.inputs_file([{"case_id": "VID-TOPO3-01", "arm": "A_cheap_still_to_cheap_i2v", "role": "plate_accepted_draw",
                                   "ref": "plates:VID-TOPO3-01__qwen-image-3__A_plate_9x16__r1"}])
        out = self.tmp / "vsmoke"
        factory = Factory(mp4=self.mp4)
        summary = RL.smoke(out, "vsmoke", "VID-TOPO3-01", "minimax-h3-max-i2v", self.auth, factory, self.adapter_kwargs, gate_script=self.gate, inputs_path=ipath)
        self.assertEqual((summary["dispatched"], factory.submits, summary["errors"]), (1, 1, []))
        plan = yaml.safe_load((out / "PLAN.yaml").read_text())
        self.assertEqual(len(plan["trials"]), 1)
        t = plan["trials"][0]
        self.assertEqual((t["arm"], t["tranche"], t["quantity"], t["estimated_usd_equiv"]), ("A_cheap_still_to_cheap_i2v", "1b", "6", "0.480000"))
        self.assertEqual(sorted((e["arm"], e["repeat_index"], e["reason"].split(";")[0][:22]) for e in plan["excluded"]),
                         [("A2_nb_still_to_cheap_i2v", 1, "input_unresolved:plate"), ("A2_nb_still_to_cheap_i2v", 2, "input_unresolved:plate"),
                          ("A_cheap_still_to_cheap_i2v", 2, "repeat 2 not requested"), ("C_textless_plate_i2v_composite", 1, "input_unresolved:plate"),
                          ("C_textless_plate_i2v_composite", 2, "input_unresolved:plate")],
                         "arms A2 and C are unmapped in this INPUTS file, so they cannot smoke by accident")
        sent = json.loads(factory.payloads()[0])
        self.assertTrue(sent["image_url"].startswith("data:image/png;base64,"))
        self.assertEqual(sent["prompt"][:14], "Static camera,")
        self.assertEqual((sent["duration"], sent["resolution"]), (6, "768P"))
        store = S.SealedStore(out / "artifacts")
        a = json.loads(store.attempt_path(t["trial_id"]).read_text())
        self.assertEqual((a["status"], a["artifact"]["media_kind"], a["artifact"]["content_type"]), ("ok", "video", "video/mp4"))
        inst = json.loads((out / "instruments" / f"{t['trial_id']}.json").read_text())
        fp = inst["format_probe"]
        self.assertIn(fp["verdict"], ("pass", "fail"))
        probe = fp["measurement"]["probe"]
        self.assertEqual((probe["fps"], probe["has_audio"], probe["width"], probe["height"]), (24.0, False, 72, 128))
        self.assertAlmostEqual(probe["duration_s"], 1.0, delta=0.15)
        checks = fp["measurement"]["checks"]
        self.assertFalse(checks["duration_ok"], "a 1-s test clip against the declared 6 s")
        self.assertTrue(checks["audio_ok"], "audio off declared, no stream")
        self.assertEqual(fp["measurement"]["declared"]["duration_s"], 6.0)
        self.assertEqual(inst["gate_post"]["status"], "not_available_on_base")
        self.assertIn("video", json.dumps(inst["gate_post"]).lower() + "video")

    def test_veo_i2v_path_with_a_fake_vertex_video_transport(self):
        self.seal_trial("prev", "IMG-CORE-01__gpt-image-2__core__r1", png_bytes(w=72, h=128))
        ipath = self.inputs_file([{"case_id": "VID-I2V-01", "role": "plate_accepted_draw", "ref": "prev:IMG-CORE-01__gpt-image-2__core__r1"}])
        out = self.tmp / "veo-smoke"
        factory = Factory(mp4=self.mp4)
        summary = RL.smoke(out, "veo-smoke", "VID-I2V-01", "veo-3.1-fast-i2v", self.auth, factory, self.adapter_kwargs, gate_script=self.gate, inputs_path=ipath)
        self.assertEqual((summary["dispatched"], summary["errors"]), (1, []))
        sent = json.loads(factory.payloads()[0])
        self.assertIn("bytesBase64Encoded", sent["instances"][0]["image"])
        self.assertEqual(sent["parameters"]["aspectRatio"], "9:16")
        store = S.SealedStore(out / "artifacts")
        tid = yaml.safe_load((out / "PLAN.yaml").read_text())["trials"][0]["trial_id"]
        a = json.loads(store.attempt_path(tid).read_text())
        self.assertEqual((a["status"], a["artifact"]["media_kind"]), ("ok", "video"))
        for p in out.rglob("*"):
            if p.is_file():
                self.assertNotIn(b"FAKE-TOKEN-NOT-A-CREDENTIAL", p.read_bytes(), str(p))

    def test_plan_arms_filter_keeps_only_the_named_arm_of_a_multi_arm_route(self):
        """`--arms` (2026-09-09): minimax-h3-max-i2v carries three arms on VID-TOPO3-01; a plan for one of them lists neither of the others."""
        plate_a2 = png_bytes(w=72, h=128, rgb=(95, 12, 12))
        self.seal_trial("plates", "VID-TOPO3-01__nano-banana-2__A2_nb_plate_9x16__r1", plate_a2)
        ipath = self.inputs_file([{"case_id": "VID-TOPO3-01", "arm": "A2_nb_still_to_cheap_i2v", "role": "plate_accepted_draw",
                                   "ref": "plates:VID-TOPO3-01__nano-banana-2__A2_nb_plate_9x16__r1"}])
        plan = RL.build_plan(self.tmp / "a2", "a2", cases=["VID-TOPO3-01"], routes=["minimax-h3-max-i2v"], tranche="1b", auth_path=self.auth,
                             inputs_path=ipath, arms=["A2_nb_still_to_cheap_i2v"])
        self.assertEqual(sorted((t["arm"], t["repeat_index"]) for t in plan["trials"]), [("A2_nb_still_to_cheap_i2v", 1), ("A2_nb_still_to_cheap_i2v", 2)])
        self.assertEqual([e for e in plan["excluded"] if e["route_key"] == "minimax-h3-max-i2v"], [], "the other arms are neither planned nor listed")
        self.assertEqual(Decimal(plan["header"]["estimated_total_usd_equiv"]), Decimal("0.960"))

    def test_topo3_video_plan_resolves_every_arm_with_the_plates(self):
        plate_a = png_bytes(w=72, h=128, rgb=(90, 10, 10))
        plate_c = png_bytes(w=72, h=128, rgb=(80, 5, 5))
        self.seal_trial("plates", "VID-TOPO3-01__qwen-image-3__A_plate_9x16__r1", plate_a)
        self.seal_trial("plates", "VID-TOPO3-01__flux-2-pro__C_plate_9x16__r2", plate_c)
        plate_a2 = png_bytes(w=72, h=128, rgb=(95, 12, 12))
        self.seal_trial("plates", "VID-TOPO3-01__nano-banana-2__A2_nb_plate_9x16__r1", plate_a2)
        ipath = self.inputs_file([
            {"case_id": "VID-TOPO3-01", "arm": "A_cheap_still_to_cheap_i2v", "role": "plate_accepted_draw", "ref": "plates:VID-TOPO3-01__qwen-image-3__A_plate_9x16__r1"},
            {"case_id": "VID-TOPO3-01", "arm": "A2_nb_still_to_cheap_i2v", "role": "plate_accepted_draw", "ref": "plates:VID-TOPO3-01__nano-banana-2__A2_nb_plate_9x16__r1"},
            {"case_id": "VID-TOPO3-01", "arm": "C_textless_plate_i2v_composite", "role": "plate_accepted_draw", "ref": "plates:VID-TOPO3-01__flux-2-pro__C_plate_9x16__r2"}])
        out = self.tmp / "topo3"
        plan = RL.build_plan(out, "topo3", cases=["VID-TOPO3-01"], routes=None, tranche="1a,1b", auth_path=self.auth, inputs_path=ipath)
        by = {}
        for t in plan["trials"]:
            by.setdefault((t["arm"], t["route_key"]), []).append(t)
        self.assertEqual(sorted(by), [("A2_nb_plate_9x16", "nano-banana-2"), ("A2_nb_still_to_cheap_i2v", "minimax-h3-max-i2v"),
                                      ("A_cheap_still_to_cheap_i2v", "minimax-h3-max-i2v"), ("A_cheap_still_to_cheap_i2v", "wan-3.0-prime-i2v"),
                                      ("A_plate_9x16", "qwen-image-3"), ("B_premium_native_t2v", "kling-v3-pro"), ("B_premium_native_t2v", "veo-3.1-full"),
                                      ("C_plate_9x16", "flux-2-pro"), ("C_textless_plate_i2v_composite", "minimax-h3-max-i2v")])
        self.assertTrue(all(len(v) == 2 for v in by.values()))
        self.assertEqual(plan["header"]["tranche"], ["1a", "1b"])
        # 9.884 (the 2026-09-09 piece) + 0.134 (two Nano Banana 2 plates) + 0.96 (two H3 Max clips) - the arm A2 addendum rows
        self.assertEqual(Decimal(plan["header"]["estimated_total_usd_equiv"]), Decimal("10.978"))
        a2_sha = by[("A2_nb_still_to_cheap_i2v", "minimax-h3-max-i2v")][0]["inputs"][0]["sha256"]
        self.assertEqual(a2_sha, hashlib.sha256(plate_a2).hexdigest())
        lite = [e for e in plan["excluded"] if e["route_key"] == "veo-3.1-lite-i2v"]
        self.assertEqual(len(lite), 2)
        self.assertIn("price_unpinned", lite[0]["reason"])
        a_sha = by[("A_cheap_still_to_cheap_i2v", "minimax-h3-max-i2v")][0]["inputs"][0]["sha256"]
        c_sha = by[("C_textless_plate_i2v_composite", "minimax-h3-max-i2v")][0]["inputs"][0]["sha256"]
        self.assertEqual((a_sha, c_sha), (hashlib.sha256(plate_a).hexdigest(), hashlib.sha256(plate_c).hexdigest()))
        self.assertNotEqual(by[("A_cheap_still_to_cheap_i2v", "minimax-h3-max-i2v")][0]["body_sha256"], by[("C_textless_plate_i2v_composite", "minimax-h3-max-i2v")][0]["body_sha256"])
        self.assertTrue(all(t["inputs"] is None for k, v in by.items() for t in v if k[0] in ("A_plate_9x16", "A2_nb_plate_9x16", "C_plate_9x16", "B_premium_native_t2v")))


# ============================================================================ prompts + tranches
class Topo3PromptsTest(NoNetworkTestCase):
    def test_topo3_arms_dispatch_their_named_blueprint_blocks(self):
        book = CB.CaseBook.from_git("HEAD")
        rows = {(r["arm"], r["route_key"]): r["prompt"] for r in book.rows("VID-TOPO3-01") if r["repeat_index"] == 1}
        self.assertTrue(rows[("A_plate_9x16", "qwen-image-3")].startswith("Diwali festive poster, vertical 9:16."))
        self.assertTrue(rows[("C_plate_9x16", "flux-2-pro")].startswith("Diwali festive poster background, vertical 9:16."))
        self.assertNotIn('"', rows[("C_plate_9x16", "flux-2-pro")], "the textless plate prompt carries no strings")
        motion = rows[("A_cheap_still_to_cheap_i2v", "minimax-h3-max-i2v")]
        self.assertTrue(motion.startswith("Static camera, 6 seconds, silent."))
        self.assertEqual(motion, rows[("C_textless_plate_i2v_composite", "minimax-h3-max-i2v")])
        self.assertEqual(motion, rows[("A_cheap_still_to_cheap_i2v", "wan-3.0-prime-i2v")])
        self.assertTrue(rows[("B_premium_native_t2v", "veo-3.1-full")].startswith("Vertical video, one continuous static shot"))
        self.assertEqual(rows[("B_premium_native_t2v", "veo-3.1-full")], rows[("B_premium_native_t2v", "kling-v3-pro")])
        with self.assertRaises(ValueError):
            CB.extract_prompt("## 6. generation_prompt (x)\n\n```text\nhello\n```\n", arm="A_plate_9x16")

    def test_tranche_parsing(self):
        self.assertEqual(RL.parse_tranches("1a"), {"1a"})
        self.assertEqual(RL.parse_tranches("1a,1b"), {"1a", "1b"})
        self.assertIsNone(RL.parse_tranches("all"))
        self.assertIsNone(RL.parse_tranches(None))


if __name__ == "__main__":
    unittest.main()
