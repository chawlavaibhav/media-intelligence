"""Provider-pool liquidity and transient-error classification (UPWORK-INTRO-001 SD-09, SD-10, SD-11).

Spend authority is not provider liquidity: the pilot's INR 2,000 cap was 6x the fal cash balance, video
slots were dropped and a fallback was structurally dead. And a Veo gRPC 14 UNAVAILABLE was written to
the ledger as `failed_or_filtered` — a label that cannot tell an outage from a bad draw.
"""
from __future__ import annotations

import unittest
from decimal import Decimal

import _bootstrap as B
from runtime.execute import provider_errors
from runtime.execute.bridge import ExecutionBridge
from runtime.execute.pools import PoolLiquidity

PROMPT = ("A centred gift box of Indian mithai on a warm, softly lit Diwali table; textless plate with a calm "
          "lower third kept clear; no lettering anywhere.")


def _build(spec_path, pools=None):
    ev = B.evidence_base()
    pb = B.price_book(ev)
    r = B.router(ev, pb)
    bridge = ExecutionBridge(evidence=ev, prices=pb, identities=r.identities)
    spec = B.spec(spec_path)
    prof = B.profile("dry", ev)
    decision = r.plan(spec, prof, customer_ref="acct-test")
    return bridge.build(spec, decision, prof, prompt_text=PROMPT, customer_ref="acct-test", pools=pools)


class Liquidity(unittest.TestCase):
    def test_can_fund_answers_yes_no_or_unknown(self):
        pools = PoolLiquidity.from_readings([
            {"pool": "cash", "balance_usd": "0.2589", "read_utc": "2026-09-14T13:35:00Z", "source": "rest.alpha.fal.ai/billing/user_balance"}])
        ok, why = pools.can_fund("cash", Decimal("0.03"))
        self.assertTrue(ok)
        ok, why = pools.can_fund("cash", Decimal("1.12"))
        self.assertFalse(ok)
        self.assertIn("0.2589", why)
        ok, why = pools.can_fund("gcp_credits", Decimal("0.96"))
        self.assertIsNone(ok)
        self.assertIn("no reading", why)

    def test_a_reading_needs_a_source_and_a_time(self):
        with self.assertRaises(ValueError):
            PoolLiquidity.from_readings([{"pool": "cash", "balance_usd": "1"}])

    def test_reservations_draw_the_pool_down_in_order(self):
        pools = PoolLiquidity.from_readings([
            {"pool": "cash", "balance_usd": "0.05", "read_utc": "2026-09-14T13:35:00Z", "source": "test"}])
        self.assertTrue(pools.reserve("cash", Decimal("0.03"))[0])
        ok, why = pools.reserve("cash", Decimal("0.03"))
        self.assertFalse(ok)
        self.assertIn("0.02", why)


class BridgeWithPools(unittest.TestCase):
    def test_authorised_budget_but_insufficient_pool_cannot_dispatch(self):
        pools = PoolLiquidity.from_readings([
            {"pool": "cash", "balance_usd": "0.04", "read_utc": "2026-09-14T13:35:00Z", "source": "test"}])
        m = _build(B.SPEC_STATIC_OVERLAY, pools=pools)
        self.assertIsNone(m["blocked"])                                  # the ceiling permits all four attempts
        self.assertTrue(m["ceiling"]["attempts_blocked_by_ceiling"] == 0)
        a1, a2 = m["attempts"][0], m["attempts"][1]
        self.assertTrue(a1["would_dispatch"])                           # 0.03 of 0.04
        self.assertTrue(a1["pool_liquidity"]["funded"])
        self.assertFalse(a2["would_dispatch"])                          # 0.03 more than the 0.01 left
        self.assertTrue(a2["blocked_by_pool"])
        self.assertIn("blocked_by_pool", a2["refusal_reason"])
        self.assertIn("cash", a2["refusal_reason"])
        self.assertTrue(a1["would_dispatch_if_funded"])
        self.assertEqual(m["pool_liquidity"]["status"], "read")
        self.assertEqual(m["pool_liquidity"]["attempts_blocked_by_pool"], 3)   # primary 2 + both fallbacks
        self.assertEqual(m["pool_liquidity"]["attempts_not_dispatchable_unknown_liquidity"], 0)
        self.assertIn("spend authority", m["pool_liquidity"]["rule"])

    def test_unknown_pool_cannot_dispatch_but_the_hypothetical_is_kept(self):
        # Controller audit on PR #98, blocker 3: spend authority must not imply a route is usable. A pool
        # whose balance is not readable leaves would_dispatch False; the pool-agnostic answer (harness
        # shape + price + ceiling) lives in would_dispatch_if_funded so dry planning still shows it.
        pools = PoolLiquidity.from_readings([
            {"pool": "cash", "balance_usd": None, "read_utc": "2026-09-14T13:35:00Z", "source": "console only"}])
        m = _build(B.SPEC_STATIC_OVERLAY, pools=pools)
        a1 = m["attempts"][0]
        self.assertTrue(a1["would_dispatch_if_funded"])
        self.assertFalse(a1["would_dispatch"])
        self.assertIsNone(a1["pool_liquidity"]["funded"])
        self.assertEqual(a1["pool_liquidity"]["status"], "unknown")
        self.assertIn("pool_liquidity_unknown", a1["refusal_reason"])
        self.assertEqual(m["pool_liquidity"]["status"], "unknown")
        self.assertEqual(m["pool_liquidity"]["attempts_blocked_by_pool"], 0)
        self.assertEqual(m["pool_liquidity"]["attempts_not_dispatchable_unknown_liquidity"], 4)

    def test_no_pool_reading_at_all_cannot_dispatch(self):
        m = _build(B.SPEC_STATIC_OVERLAY)
        self.assertEqual(m["pool_liquidity"]["status"], "not_read")
        for a in m["attempts"]:
            self.assertFalse(a["would_dispatch"], a["attempt_id"])
            self.assertEqual(a["pool_liquidity"]["status"], "not_read")
        self.assertTrue(m["attempts"][0]["would_dispatch_if_funded"])
        self.assertIn("pool_liquidity_unknown", m["attempts"][0]["refusal_reason"])
        self.assertEqual(m["pool_liquidity"]["attempts_not_dispatchable_unknown_liquidity"], 4)

    def test_a_reading_for_another_pool_does_not_fund_this_one(self):
        pools = PoolLiquidity.from_readings([
            {"pool": "gcp_credits", "balance_usd": "50", "read_utc": "2026-09-14T13:35:00Z", "source": "test"}])
        m = _build(B.SPEC_STATIC_OVERLAY, pools=pools)
        self.assertFalse(m["attempts"][0]["would_dispatch"])
        self.assertEqual(m["attempts"][0]["pool_liquidity"]["status"], "unknown")
        self.assertIn("cash", m["pool_liquidity"]["pools_without_reading"])

    def test_funded_fallback_is_executable_if_triggered_only_when_funded(self):
        pools = PoolLiquidity.from_readings([
            {"pool": "cash", "balance_usd": "10", "read_utc": "2026-09-14T13:35:00Z", "source": "test"}])
        m = _build(B.SPEC_STATIC_OVERLAY, pools=pools)
        fb = [a for a in m["attempts"] if a["slot"] == "fallback"]
        self.assertTrue(all(a["if_triggered_would_dispatch"] for a in fb))
        self.assertTrue(all(a["if_triggered_would_dispatch_if_funded"] for a in fb))
        m2 = _build(B.SPEC_STATIC_OVERLAY)
        fb2 = [a for a in m2["attempts"] if a["slot"] == "fallback"]
        self.assertFalse(any(a["if_triggered_would_dispatch"] for a in fb2))
        self.assertTrue(all(a["if_triggered_would_dispatch_if_funded"] for a in fb2))


class Classification(unittest.TestCase):
    def test_grpc_unavailable_is_infrastructure_transient(self):
        c = provider_errors.classify(grpc_code=14, message="UNAVAILABLE")
        self.assertEqual(c["failure_class"], provider_errors.INFRASTRUCTURE_TRANSIENT)
        self.assertFalse(c["counts_against_route_quality"])
        self.assertTrue(c["retry_eligible"])
        self.assertNotEqual(c["failure_class"], provider_errors.MODEL_QUALITY_FAILURE)

    def test_http_5xx_and_429_and_timeouts_are_transient(self):
        for kw in ({"http_status": 503}, {"http_status": 500}, {"http_status": 502}, {"http_status": 504},
                   {"http_status": 429}, {"timed_out": True}):
            self.assertEqual(provider_errors.classify(**kw)["failure_class"], provider_errors.INFRASTRUCTURE_TRANSIENT, kw)

    def test_content_filter_is_a_provider_refusal_not_transient(self):
        c = provider_errors.classify(http_status=400, message="Request blocked by content filter (SAFETY)")
        self.assertEqual(c["failure_class"], provider_errors.PROVIDER_REFUSAL)
        self.assertFalse(c["retry_eligible"])
        self.assertFalse(c["counts_against_route_quality"])

    def test_nothing_is_ever_classified_as_model_quality_here(self):
        for kw in ({"http_status": 418}, {"message": "weird"}, {}, {"http_status": 200, "message": "empty body"}):
            c = provider_errors.classify(**kw)
            self.assertEqual(c["failure_class"], provider_errors.UNCLASSIFIED, kw)
            self.assertNotEqual(c["failure_class"], provider_errors.MODEL_QUALITY_FAILURE)

    def test_a_failure_record_carries_the_class_and_keeps_provider_error_status(self):
        c = provider_errors.classify(grpc_code=14, message="UNAVAILABLE")
        rec = provider_errors.failure_record({"attempt_id": "att-1", "route_key": "veo-3.1-fast-i2v"}, c,
                                             reserved_usd="0.96")
        self.assertEqual(rec["status"], "provider_error")          # OUTCOME-EVENT-v1 vocabulary, untouched
        self.assertEqual(rec["failure_class"], provider_errors.INFRASTRUCTURE_TRANSIENT)
        self.assertEqual(rec["billing_state"], "unknown_provisional")
        self.assertEqual(rec["reserved_usd"], "0.96")
        self.assertFalse(rec["counts_against_route_quality"])


if __name__ == "__main__":
    unittest.main()
