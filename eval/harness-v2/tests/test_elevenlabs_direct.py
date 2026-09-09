"""ElevenLabs DIRECT adapter (plan credits, pool elevenlabs_credits, cap elevenlabs_cap_credits).

Fake transports only: no socket, no key, no call to api.elevenlabs.io. The key name is read from a throw-away file
(never ~/.mi-keys) and its canary value must never reach a body, a record, the ledger or an exception text.
"""
import hashlib
import json
import os
import re
import unittest
from decimal import Decimal
from pathlib import Path

import yaml

from _support import NoNetworkTestCase, fixed_clock, hv2_paths
import casebook as CB
import ledger as L
import pricing as PR
import run_live as RL
import store as S
import surfaces
import transports as T
from adapters import adapter_for
from adapters import base as B
from adapters import elevenlabs_direct as EL
from budget_guard import BudgetExceeded
from providers import DispatchRefused, PreDispatchRefusal

BOOK = CB.CaseBook.from_git("HEAD")
CANARY = "CANARY-elevenlabs-key-value-0a1b2c3d4e5f"
VOICE = "JBFqnCBsd6RMkjVDRZzb"
# Binary fixture: an ID3-tagged mp3 frame header followed by invalid UTF-8, so any text path fails loudly.
MP3_FIXTURE = b"ID3\x04\x00\x00\x00\x00\x00\x00" + b"\xff\xfb\x90\x00" + b"\xff\xfe\x80\x81" * 64
TTS_URL = f"{surfaces.ELEVENLABS_TTS}/{VOICE}?output_format=mp3_44100_128"
MUSIC_URL = f"{surfaces.ELEVENLABS_MUSIC}?output_format=mp3_44100_128"


def tts_row(**over):
    """The freeze's AUD-TTS-01 row re-pointed at the direct route (there is no catalogue row for an extension route)."""
    row = BOOK.row("AUD-TTS-01", "elevenlabs-v3")
    return {**row, "route_key": "elevenlabs-v3-direct", "surface": "direct", "billing_pool": "elevenlabs_credits",
            "unit_price": 0, "quantity": 30, "quantity_unit": "chars", **over}


def music_row(**over):
    row = BOOK.row("MUS-01", "elevenlabs-music")
    return {**row, "route_key": "elevenlabs-music-direct", "surface": "direct", "billing_pool": "elevenlabs_credits",
            "unit_price": 0, "quantity": 30, "quantity_unit": "seconds", **over}


def ok_transport(headers=None):
    return T.FakeTransport(posts=[(200, MP3_FIXTURE, "audio/mpeg", headers if headers is not None else {"request-id": "req-abc"})])


class ElevenLabsBase(NoNetworkTestCase):
    def setUp(self):
        super().setUp()
        self.pricing = PR.Pricing()
        self.budget = self.make_ledger(elevenlabs_cap_credits="5000")
        self.store = S.SealedStore(self.tmp / "runs" / "run-test" / "artifacts")

    def make(self, route_key, transport=None, budget=None, **kw):
        entry = surfaces.REGISTRY.get(route_key)
        kw.setdefault("sleep", lambda s: None)
        kw.setdefault("clock", fixed_clock())
        return adapter_for(entry, pricing=self.pricing, transport=transport, budget=budget or self.budget, store=self.store, **kw)


# ============================================================================ registry + pins
class RegistryTest(NoNetworkTestCase):
    def test_two_extension_routes_are_registered_outside_the_catalogue(self):
        self.assertEqual(surfaces.EXTENSION_ROUTES, ("elevenlabs-v3-direct", "elevenlabs-music-direct"))
        tts, music = (surfaces.REGISTRY.get(k) for k in surfaces.EXTENSION_ROUTES)
        for e in (tts, music):
            self.assertEqual(e.adapter, "elevenlabs_direct")
            self.assertEqual(e.surface, "elevenlabs_direct")
            self.assertEqual(e.billing_pool, "elevenlabs_credits")
            self.assertEqual(e.currency, "USD")
            self.assertEqual(e.key_name, "ELEVENLABS_API_KEY")
            self.assertEqual(e.shape_status, "verified")
            self.assertEqual(e.media_kind, "audio")
            self.assertTrue(e.endpoint.startswith("https://api.elevenlabs.io/v1/"), e.endpoint)
            self.assertNotIn(e.route_key, surfaces.REGISTRY.catalogue_keys())
        self.assertEqual((tts.workflow, tts.lane, tts.surface_model_id), ("tts", "tts", "eleven_v3"))
        self.assertEqual((music.workflow, music.lane, music.surface_model_id), ("music", "music", "music_v1"))
        self.assertEqual(tts.endpoint, "https://api.elevenlabs.io/v1/text-to-speech")
        self.assertEqual(music.endpoint, "https://api.elevenlabs.io/v1/music")

    def test_pinned_schema_and_price_pages_exist_and_hash_true(self):
        root = hv2_paths.REPO_ROOT
        idx = yaml.safe_load((root / "eval/empirical-planning/price-pins-2026-09/elevenlabs-direct/PIN-INDEX.yaml").read_text())
        by_file = {}
        for pin in idx["pins"]:
            f = root / pin["pin_file"]
            self.assertTrue(f.exists(), pin["pin_file"])
            data = f.read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), pin["sha256"], pin["pin_file"])
            self.assertEqual(len(data), pin["bytes"], pin["pin_file"])
            for q in [pin["evidence_quote"]] + (pin.get("additional_evidence_quotes") or []):
                self.assertIn(q.encode("utf-8"), data, (pin["pin_file"], q))
            by_file[pin["pin_file"]] = pin
        # the pricing numbers the harness relies on are exact substrings of the pinned pricing page
        pricing = (root / surfaces.ELEVENLABS_PRICING_PIN).read_bytes()
        self.assertIn(b"Text to Speech 1 credit per character", pricing)
        self.assertIn(b"Eleven Music 900 credits per minute", pricing)
        schema = yaml.safe_load((hv2_paths.SCHEMAS / "elevenlabs" / "SCHEMA-INDEX.yaml").read_text())
        self.assertEqual(set(schema["shapes"]), {"elevenlabs_tts", "elevenlabs_music"})
        for page in schema["pages"]:
            raw = root / page["raw_file"]
            self.assertEqual(hashlib.sha256(raw.read_bytes()).hexdigest(), page["raw_sha256"], page["id"])
            if page.get("stored_file"):
                self.assertTrue((root / page["stored_file"]).exists(), page["stored_file"])
        self.assertEqual(schema["shapes"]["elevenlabs_tts"]["model_id"], EL.TTS_MODEL_ID)
        self.assertEqual(schema["shapes"]["elevenlabs_music"]["model_id"], EL.MUSIC_MODEL_ID)
        self.assertEqual(set(schema["shapes"]["elevenlabs_tts"]["body_fields_pinned"]), EL.TTS_BODY_FIELDS)
        self.assertEqual(set(schema["shapes"]["elevenlabs_music"]["body_fields_pinned"]), EL.MUSIC_BODY_FIELDS)
        for e in (surfaces.REGISTRY.get(k) for k in surfaces.EXTENSION_ROUTES):
            self.assertTrue((root / e.price_pin_ref).exists(), e.price_pin_ref)
            self.assertTrue((root / e.params_schema.split("#")[0]).exists(), e.params_schema)

    def test_hygiene_adapter_imports_no_network_module(self):
        src = Path(EL.__file__).read_text()
        for mod in ("url" + "lib", "http\\." + "client", "sock" + "et", "requ" + "ests", "subpro" + "cess"):
            self.assertIsNone(re.search(r"^\s*(import|from)\s+" + mod + r"\b", src, re.M), mod)

    def test_live_transport_factory_maps_the_surface_and_opens_nothing(self):
        t = RL.live_transport_factory(surfaces.REGISTRY.get("elevenlabs-v3-direct"), {})
        self.assertIsInstance(t, T.ElevenLabsTransport)
        self.assertEqual(t.calls, 0)
        self.assertTrue(callable(getattr(t, "post_bytes", None)))


# ============================================================================ build + dry run
class BuildTest(ElevenLabsBase):
    def test_construction_reads_no_key_and_dry_run_needs_none(self):
        self.assertFalse(os.environ.get("ELEVENLABS_API_KEY"))
        self.assertEqual(self.key_file.read_text(), "")
        for k in surfaces.EXTENSION_ROUTES:
            adapter_for(surfaces.REGISTRY.get(k), pricing=self.pricing)   # no transport, no ledger, no store, no key
        d = self.make("elevenlabs-music-direct").dry_run(music_row())
        self.assertTrue(d["would_dispatch"], d["refusal_reason"])

    def test_tts_body_url_and_price_come_from_the_pinned_pages(self):
        d = self.make("elevenlabs-v3-direct").dry_run(tts_row(), {"voice": VOICE})
        self.assertTrue(d["would_dispatch"], d["refusal_reason"])
        self.assertEqual(d["url"], TTS_URL)
        self.assertEqual(d["body"], {"text": tts_row()["params"]["script"], "model_id": "eleven_v3"})
        self.assertEqual(d["headers"]["xi-api-key"], "<KEY:ELEVENLABS_API_KEY>")
        p = d["price"]
        self.assertEqual((p["unit_price"], p["currency"], p["unit"]), ("0", "USD", "plan_credits"))
        self.assertEqual((p["quantity"], p["quantity_unit"]), ("30", "chars"))
        self.assertEqual((p["amount_native"], p["amount_usd_equiv"]), ("30", "0"))     # 30 characters = 30 credits, 0 USD cash
        self.assertEqual(p["pin_ref"], surfaces.ELEVENLABS_PRICING_PIN)
        self.assertIn("1_credit_per_character", p["quantity_rule"])

    def test_tts_without_a_voice_is_input_unresolved_not_a_guess(self):
        d = self.make("elevenlabs-v3-direct").dry_run(tts_row())
        self.assertFalse(d["would_dispatch"])
        self.assertIn("input_unresolved:voice", d["refusal_reason"])
        with self.assertRaises(PreDispatchRefusal):
            self.make("elevenlabs-v3-direct").build_request(tts_row(), {"voice": "../admin?x=1"})   # not a plain id

    def test_music_body_and_credits(self):
        d = self.make("elevenlabs-music-direct").dry_run(music_row())
        self.assertTrue(d["would_dispatch"], d["refusal_reason"])
        self.assertEqual(d["url"], MUSIC_URL)
        self.assertEqual(d["body"], {"prompt": music_row()["prompt"], "music_length_ms": 30000, "model_id": "music_v1"})
        p = d["price"]
        self.assertEqual((p["quantity"], p["quantity_unit"]), ("30", "seconds"))
        self.assertEqual((p["amount_native"], p["amount_usd_equiv"], p["unit_price"]), ("900", "0", "0"))   # 30 s -> 1 minute x 900 credits
        # 61 s rounds UP to two minutes = 1800 credits (proration is not stated on the pinned page)
        row = music_row(params={**music_row()["params"], "duration_s": 61}, quantity=61)
        self.assertEqual(self.pricing.evaluate("elevenlabs-music-direct", row).amount_native, Decimal(1800))

    def test_pinned_limits_and_foreign_fields_are_refused(self):
        ad = self.make("elevenlabs-v3-direct")
        with self.assertRaises(PreDispatchRefusal):
            ad.build_request(tts_row(params={"script": "x" * 5001}), {"voice": VOICE})
        with self.assertRaises(PreDispatchRefusal):
            ad.build_request(tts_row(), {"voice": VOICE, "seed": 7})                     # caller parameters never reach the body
        m = self.make("elevenlabs-music-direct")
        with self.assertRaises(PreDispatchRefusal):
            m.build_request(music_row(params={"duration_s": 2}))                         # below the pinned 3000 ms
        with self.assertRaises(PreDispatchRefusal):
            m.build_request(music_row(params={"duration_s": 601}))                       # above the pinned 600000 ms
        with self.assertRaises(PreDispatchRefusal):
            m.build_request(music_row(params={}))                                        # no duration -> no billable quantity
        # a case row that carries a cash unit price for a credit pool is a mismatch, not silently priced
        d = ad.dry_run(tts_row(unit_price=0.1), {"voice": VOICE})
        self.assertFalse(d["would_dispatch"])
        self.assertIn("price_mismatch", d["refusal_reason"])


# ============================================================================ dispatch outcomes
class DispatchTest(ElevenLabsBase):
    def test_success_tts_seals_mp3_and_records_credits_at_zero_cash(self):
        os.environ["ELEVENLABS_API_KEY"] = "fake-not-a-real-key"
        t = ok_transport()
        ad = self.make("elevenlabs-v3-direct", t)
        dry = ad.dry_run(tts_row(), {"voice": VOICE})
        a = ad.dispatch(tts_row(), {"voice": VOICE})
        self.assertEqual(a["status"], "ok", (a["error_class"], a["raw_status_note"]))
        self.assertEqual(t.submits, 1)
        self.assertEqual(t.calls[0]["url"], TTS_URL)
        self.assertEqual(t.calls[0]["payload"], S.canonical_json(dry["body"]))         # the dry-run bytes ARE the sent bytes
        self.assertEqual(a["provider_request_id"], "req-abc")
        self.assertEqual(a["artifact"]["content_type"], "audio/mpeg")
        self.assertEqual(a["artifact"]["media_kind"], "audio")
        self.assertTrue(a["artifact"]["relative_path"].endswith(".mp3"))
        self.assertEqual((a["billing_pool"], a["currency"], a["reserved_amount"], a["reserved_amount_usd_equiv"]),
                         ("elevenlabs_credits", "USD", "30", "0"))
        self.assertEqual((a["quantity"], a["quantity_unit"], a["unit_price"]), ("30", "chars", "0"))
        self.assertEqual((a["billing_state"], a["retries"], a["one_call_one_trial"]), ("reported", 0, True))
        pools = self.budget.totals_by_pool()
        self.assertEqual(pools["elevenlabs_credits"]["native"], Decimal(30))
        self.assertEqual(pools["elevenlabs_credits"]["usd_equiv"], Decimal(0))
        self.assertEqual(self.budget.spent_usd(), Decimal(0))

    def test_success_music_uses_the_song_id_header(self):
        os.environ["ELEVENLABS_API_KEY"] = "fake-not-a-real-key"
        t = ok_transport({"song-id": "song-42"})
        a = self.make("elevenlabs-music-direct", t).dispatch(music_row())
        self.assertEqual(a["status"], "ok", (a["error_class"], a["raw_status_note"]))
        self.assertEqual(a["provider_request_id"], "song-42")
        self.assertEqual(t.calls[0]["url"], MUSIC_URL)
        self.assertEqual(json.loads(t.calls[0]["payload"])["music_length_ms"], 30000)
        self.assertEqual(self.budget.totals_by_pool()["elevenlabs_credits"]["native"], Decimal(900))

    def test_4xx_refusal_and_errors_are_classified_like_sarvam(self):
        os.environ["ELEVENLABS_API_KEY"] = "fake-not-a-real-key"
        cases = [
            (400, b'{"detail":{"status":"content_moderation","message":"text blocked by policy"}}', "refusal", "moderation_block", False),
            (401, b'{"detail":{"status":"quota_exceeded","message":"not enough credits"}}', "error", "http_401", False),
            (422, b'{"detail":[{"loc":["body","text"],"msg":"field required"}]}', "error", "http_422", False),
            (429, b'{"detail":{"status":"too_many_concurrent_requests","message":"slow down"}}', "error", "http_429", True),
            (502, b"<html>bad gateway</html>", "error", "http_502", True),
        ]
        for i, (code, body, status, err, ambiguous) in enumerate(cases, start=1):
            with self.subTest(code=code):
                t = T.FakeTransport(posts=[(code, body, "application/json", {"request-id": f"r{code}"})])
                a = self.make("elevenlabs-v3-direct", t).dispatch(tts_row(repeat_index=i), {"voice": VOICE})
                self.assertEqual((a["status"], a["error_class"], a["ambiguous_dispatch"]), (status, err, ambiguous))
                self.assertEqual(a["billing_state"], "unknown_provisional" if ambiguous else "reported")
                self.assertEqual(a["provider_request_id"], f"r{code}")
                self.assertEqual(a["lifecycle_counts"]["submits"], 1)
                self.assertIsNone(a["artifact"])
        note = a["raw_status_note"]
        self.assertIn("502", note)

    def test_malformed_200_responses(self):
        os.environ["ELEVENLABS_API_KEY"] = "fake-not-a-real-key"
        cases = [
            ((200, b'{"detail":"unexpected json"}', "application/json", {}), "malformed_response"),
            ((200, b"", "audio/mpeg", {}), "no_artifact_returned"),
            ((200, b"<html>login</html>", "text/html", {}), "malformed_response"),
            ((200, b"not audio at all", None, {}), "malformed_response"),
            ((200, {"audios": ["not-the-elevenlabs-shape"]}), "malformed_response"),          # a JSON-shaped answer to a bytes POST
        ]
        for i, (scripted, err) in enumerate(cases, start=1):
            with self.subTest(case=i):
                t = T.FakeTransport(posts=[scripted])
                a = self.make("elevenlabs-v3-direct", t).dispatch(tts_row(repeat_index=i), {"voice": VOICE})
                self.assertEqual((a["status"], a["error_class"]), ("error", err), a["raw_status_note"])
                self.assertIsNone(a["artifact"])
                self.assertEqual(a["lifecycle_counts"]["submits"], 1)

    def test_transport_failure_after_send_is_ambiguous_and_never_retried(self):
        os.environ["ELEVENLABS_API_KEY"] = "fake-not-a-real-key"
        t = T.FakeTransport(posts=[TimeoutError("timed out")])
        a = self.make("elevenlabs-v3-direct", t).dispatch(tts_row(), {"voice": VOICE})
        self.assertTrue(a["ambiguous_dispatch"])
        self.assertFalse(a["outcome_resolved"])
        self.assertEqual(t.submits, 1)

    def test_no_transport_or_ledger_refuses(self):
        with self.assertRaises(DispatchRefused):
            self.make("elevenlabs-v3-direct", None).dispatch(tts_row(), {"voice": VOICE})


# ============================================================================ the key never leaks
class KeyLeakTest(ElevenLabsBase):
    def _walk_text(self):
        out = []
        for p in self.tmp.rglob("*"):
            if p.is_file():
                out.append(p.read_bytes())
        return b"".join(out)

    def test_key_is_read_by_name_from_the_file_and_never_written_anywhere(self):
        self.write_fake_key("ELEVENLABS_API_KEY", CANARY)                 # a throw-away file, never ~/.mi-keys
        t = ok_transport()
        ad = self.make("elevenlabs-v3-direct", t)
        a = ad.dispatch(tts_row(), {"voice": VOICE})
        self.assertEqual(a["status"], "ok")
        self.assertEqual(t.calls[0]["headers"]["xi-api-key"], CANARY)      # the transport got the value, in memory only
        self.assertNotIn(CANARY, json.dumps(a))
        self.assertEqual(a["key_name"], "ELEVENLABS_API_KEY")
        self.assertEqual(a["credential_file_name"], "~/.mi-keys")
        self.assertNotIn(CANARY, t.calls[0]["payload"].decode("utf-8"))
        on_disk = self._walk_text().replace(f"export ELEVENLABS_API_KEY={CANARY}".encode(), b"")   # only the fake key file itself
        self.assertNotIn(CANARY.encode(), on_disk)
        self.assertNotIn(CANARY, json.dumps(self.budget.records()))

    def test_exception_texts_and_notes_are_scrubbed(self):
        self.write_fake_key("ELEVENLABS_API_KEY", CANARY)
        t = T.FakeTransport(posts=[RuntimeError(f"connection reset while sending xi-api-key {CANARY}")])
        a = self.make("elevenlabs-v3-direct", t).dispatch(tts_row(), {"voice": VOICE})
        self.assertNotIn(CANARY, json.dumps(a))
        self.assertIn("<REDACTED>", a["raw_status_note"])
        self.assertNotIn(CANARY.encode(), self._walk_text().replace(f"export ELEVENLABS_API_KEY={CANARY}".encode(), b""))

    def test_missing_key_refuses_by_name_releases_the_reservation_and_sends_nothing(self):
        t = ok_transport()
        with self.assertRaises(PreDispatchRefusal) as cm:
            self.make("elevenlabs-v3-direct", t).dispatch(tts_row(), {"voice": VOICE})
        self.assertIn("ELEVENLABS_API_KEY", str(cm.exception))
        self.assertEqual(t.submits, 0)
        types = [r["type"] for r in self.budget.records()]
        self.assertEqual(types, ["reservation", "release"])

    def test_unknown_key_names_stay_unreadable(self):
        with self.assertRaises(PreDispatchRefusal):
            B.KeyLoader().read("ELEVENLABS_SECRET")


# ============================================================================ ledger: pool + cap
class CreditCapTest(ElevenLabsBase):
    def test_cap_missing_from_the_file_means_zero_and_forbids_dispatch(self):
        budget = self.make_ledger(run_id="run-nocap")                       # the 13-field record: no elevenlabs_cap_credits
        self.assertEqual(budget.run.elevenlabs_cap_credits, Decimal(0))
        self.assertEqual(budget.run.record["elevenlabs_cap_credits"], "0")
        os.environ["ELEVENLABS_API_KEY"] = "fake-not-a-real-key"
        t = ok_transport()
        with self.assertRaises(BudgetExceeded) as cm:
            self.make("elevenlabs-v3-direct", t, budget=budget).dispatch(tts_row(), {"voice": VOICE})
        self.assertIn("elevenlabs_cap_credits", str(cm.exception))
        self.assertEqual(t.submits, 0)                                        # refused BEFORE the send
        self.assertEqual(budget.records(), [])                                # nothing was even reserved
        self.assertFalse(list(self.store.manifest()))

    def test_cap_is_enforced_over_native_credits_across_both_workflows(self):
        budget = self.make_ledger(run_id="run-cap", elevenlabs_cap_credits="920")
        os.environ["ELEVENLABS_API_KEY"] = "fake-not-a-real-key"
        a = self.make("elevenlabs-v3-direct", ok_transport(), budget=budget).dispatch(tts_row(), {"voice": VOICE})
        self.assertEqual(a["status"], "ok")                                   # 30 credits
        t = ok_transport({"song-id": "s"})
        with self.assertRaises(BudgetExceeded):                               # 30 + 900 > 920
            self.make("elevenlabs-music-direct", t, budget=budget).dispatch(music_row())
        self.assertEqual(t.submits, 0)
        self.assertEqual(budget.credits_native_live(), Decimal(30))
        self.assertEqual(budget.spent_usd(), Decimal(0))                      # the USD ceiling never moved

    def test_zero_cash_rows_and_the_usd_caps_stay_symmetrical(self):
        b = self.make_ledger(run_id="run-sym", ceiling="1.00", caps=("0.50", "0.50"), elevenlabs_cap_credits="100")
        t = b.tranche("1b")
        t.reserve(Decimal("0"), billing_pool="elevenlabs_credits", currency="USD", amount_native=Decimal(60), amount_usd_equiv=Decimal("0"))
        t.record(Decimal("0"), billing_pool="elevenlabs_credits", currency="USD", amount_native=Decimal(60), amount_usd_equiv=Decimal("0"))
        self.assertEqual(b.totals_by_pool()["elevenlabs_credits"], {"native": Decimal(60), "usd_equiv": Decimal(0), "currency": "USD"})
        with self.assertRaises(BudgetExceeded):                               # 60 + 50 > 100 credits
            t.reserve(Decimal("0"), billing_pool="elevenlabs_credits", currency="USD", amount_native=Decimal(50), amount_usd_equiv=Decimal("0"))
        with self.assertRaises(ValueError):                                   # a cash amount on the credits pool hides money
            t.reserve(Decimal("0.05"), billing_pool="elevenlabs_credits", currency="USD", amount_native=Decimal(5), amount_usd_equiv=Decimal("0.05"))
        with self.assertRaises(ValueError):                                   # INR on the credits pool disagrees
            t.reserve(Decimal("0"), billing_pool="elevenlabs_credits", currency="INR", amount_native=Decimal(5), amount_usd_equiv=Decimal("0"))
        self.assertEqual(b.remaining_usd(), Decimal("1.00"))

    def test_authorisation_loader_keeps_the_signed_13_fields_and_reads_the_optional_cap(self):
        self.assertEqual(len(L.AUTH_FIELDS), 13)
        self.assertNotIn("elevenlabs_cap_credits", L.AUTH_FIELDS)
        self.assertEqual(L.OPTIONAL_AUTH_FIELDS, ("elevenlabs_cap_credits",))
        plain = L.load_battery_authorisation(self.write_auth(name="plain.yaml"))
        self.assertEqual(plain.refusals, ())
        self.assertEqual(plain.elevenlabs_cap_credits, Decimal(0))
        with_cap = L.load_battery_authorisation(self.write_auth(name="cap.yaml", elevenlabs_cap_credits=1500))
        self.assertEqual(with_cap.refusals, ())
        self.assertEqual(with_cap.elevenlabs_cap_credits, Decimal(1500))
        for bad in ("-1", "12.5", "lots"):
            with self.subTest(bad=bad):
                auth = L.load_battery_authorisation(self.write_auth(name=f"bad-{bad}.yaml", elevenlabs_cap_credits=bad))
                self.assertTrue(any("elevenlabs_cap_credits" in r for r in auth.refusals), auth.refusals)
        st = L.authorisation_status(self.write_auth(name="st.yaml", elevenlabs_cap_credits=7))
        self.assertEqual(st["elevenlabs_cap_credits"], "7")
        # the committed example still carries exactly the 13 signed fields (the optional one is a comment there)
        ex = yaml.safe_load(L.AUTH_EXAMPLE_PATH.read_text())["machine_authorisation"]
        self.assertEqual(tuple(ex), L.AUTH_FIELDS)


if __name__ == "__main__":
    unittest.main()
