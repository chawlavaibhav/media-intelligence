"""P1 v2 phase 1 — skeleton: rulebook data, form schemas, the flow table, founder-only authority, no third identical
retry. Spec §11 tests 3, 4 and 6 (the station-level halves of 3 and 4 are in test_v2_production.py). USD 0."""
import os
import subprocess
import sys
import unittest

from product import authority, flow, rulebook, verify
from product.config import REPO
from product.dispatch import Dispatcher, IdenticalRequestRefused
from product.store import utc_now
from product.tests.support import Env


class RulebookAndForms(unittest.TestCase):
    def test_every_worker_in_the_diagram_has_a_card_and_every_ai_worker_fills_exactly_one_form_per_call(self):
        cards = rulebook.seed_cards()
        self.assertEqual(len(rulebook.AI_WORKERS), 7)
        self.assertEqual(len(rulebook.CODE_WORKERS), 5)
        self.assertEqual(len(rulebook.PEOPLE), 2)
        for w in rulebook.AI_WORKERS + rulebook.CODE_WORKERS:
            self.assertIn(w, cards, w)
            c = cards[w]
            self.assertTrue(c["mission"] and c["kra"] and c["version"] == 1, w)
        for w in rulebook.AI_WORKERS:
            for f in cards[w]["forms"]:
                self.assertIn(f, rulebook.forms(), f"{w} writes {f}, which has no schema")
                self.assertIn(f, cards[w]["instructions"], f"{w} has no instructions for {f}")

    def test_all_forms_load_with_a_version_and_the_action_class_enum_is_resolved(self):
        fs = rulebook.forms()
        for name in ("order_slip", "understanding", "feasibility", "recipe", "recipe_check", "production_log",
                     "ingredient_check", "final_review", "change_request", "gateway_report", "lessons", "tray", "rulebook_card"):
            self.assertIn(name, fs)
            self.assertEqual(fs[name]["version"], 1)
        shot = fs["recipe"]["schema"]["properties"]["shots"]["items"]["properties"]
        self.assertIn("hands_work_mechanism", shot["action_class"]["enum"])
        self.assertEqual(set(rulebook.ai_schema("feasibility")["properties"]), {"product_truth", "actions_needed"})

    def test_a_card_change_is_a_new_version_with_a_reason_and_the_seed_is_untouched(self):
        e = Env()
        try:
            rb = rulebook.Rulebook(e.store)
            self.assertEqual(rb.version("chef"), 1)
            with self.assertRaises(ValueError):
                rb.change_card("chef", {"kra_add": "x"}, by="founder:f", reason="")
            v = rb.change_card("chef", {"kra_add": "Never plan hands on zips."}, by="founder:f", reason="lesson L-1 approved")
            self.assertEqual(v, 2)
            self.assertIn("Never plan hands on zips.", rb.card("chef")["kra"])
            self.assertEqual(rulebook.seed_cards()["chef"]["version"], 1)
            self.assertEqual([h["version"] for h in rb.history("chef")], [1, 2])
            text, ver = rb.card_text("chef", "recipe")
            self.assertEqual(ver, 2)
            self.assertTrue(text.startswith("RULEBOOK CARD — chef (version 2)"))
        finally:
            e.close()


class FlowTable(unittest.TestCase):
    def test_the_send_back_table_matches_spec_6_2(self):
        r = flow.RULES
        self.assertEqual(r["SB-RECIPE"]["limit"], 2)
        self.assertEqual(r["SB-RECIPE"]["then"], "paused_for_founder")
        self.assertEqual(r["SB-TASTER-RETRY"]["limit"], 2)
        self.assertEqual(r["SB-TASTER-REPLAN"]["limit"], 1)
        self.assertEqual(r["SB-BIG-FIX"]["limit"], 2)
        self.assertEqual(r["SB-BIG-FAIL"]["limit"], 1)
        for s in ("awaiting_customer_input", "awaiting_master_approval", "paused_for_founder", "feasibility", "abandoned"):
            self.assertIn(s, flow.STATES)

    def test_send_back_limits_are_counted_from_the_job_file(self):
        e = Env()
        try:
            jid = e.submit("image")
            self.assertEqual(flow.send_back(e.store, jid, "SB-RECIPE", why="a"), 1)
            self.assertEqual(flow.send_back(e.store, jid, "SB-RECIPE", why="b"), 2)
            with self.assertRaises(flow.LimitReached):
                flow.send_back(e.store, jid, "SB-RECIPE", why="c")
            self.assertEqual(flow.rounds_used(e.store, jid, "SB-RECIPE"), 2)
        finally:
            e.close()

    def test_a_pause_never_jumps_straight_to_the_customer(self):
        for p in flow.PAUSES + ("failed",):
            self.assertFalse(flow.can(p, "ready_for_review"), p)
            self.assertFalse(flow.can(p, "accepted"), p)


class OnlyTheFounderCanOverride(unittest.TestCase):
    """Spec §11 test 3 (store / door guard / CLI half) and test 4."""

    def setUp(self):
        self.e = Env()
        self.jid = self.e.submit("image")
        self.e.store.transition(self.jid, "submitted", "understanding", actor="system")
        self.e.store.transition(self.jid, "understanding", "paused_for_founder", actor="system", data={"reason": "test"},
                                resume_state="understanding", pause_reason="test")

    def tearDown(self):
        self.e.close()

    def refusals(self):
        return self.e.store.events(self.jid, ("override_refused",))

    def test_worker_script_operator_customer_and_builder_strings_are_refused_and_logged(self):
        e, jid = self.e, self.jid
        e.operator("ops@mi.test")
        ops_session = e.session_of("ops@mi.test")
        cust_session = e.session_of("buyer@acme.test")
        for caller in ("w-1234-abc", "operator:claude (builder, P1 validation)", "script", "admin-cli", None, 42,
                       ops_session, cust_session, "operator:vaibhav@getaight.ai"):
            with self.assertRaises(authority.NotFounder):
                authority.founder_proof(e.store, caller, job_id=jid, action="waive a check")
        self.assertEqual(len(self.refusals()), 9)
        # a hand-made proof object (right shape, no live founder session) is refused by the store itself
        fake = authority.FounderProof("usr_fake", "claude@builder", "0" * 64)
        with self.assertRaises(PermissionError):
            e.store.transition(jid, "paused_for_founder", "understanding", actor="operator:claude", founder=fake)
        with self.assertRaises(PermissionError):
            e.store.transition(jid, "paused_for_founder", "understanding", actor="w-1234")
        with self.assertRaises(PermissionError):
            e.store.add_override(jid, kind="check_waiver", target="x:y", founder=fake, reason="because I say so, builder")
        self.assertEqual(e.state(jid), "paused_for_founder")
        self.assertEqual(len(self.refusals()), 12)

    def test_a_waiver_written_by_anyone_but_the_founder_does_not_open_the_door(self):
        e, jid = self.e, self.jid
        aid = e.store.assets(jid, source="customer")[0]["id"]
        req = {"exact_copy_match": "EXACT_COPY_MATCH"}
        e.store.record_check(jid, aid, check_id="exact_copy_match", status="FAIL", blocking=True, runner="deterministic", detail="x")
        e.store.waive(jid, aid, "exact_copy_match", "operator:claude (builder)", "pushing it through for validation")
        g = verify.gateway(e.store, jid, aid, req)
        self.assertFalse(g["ready"])
        self.assertEqual(g["ignored_waivers"][0]["by"], "operator:claude (builder)")
        e.store.record_check(jid, aid, check_id="independent_review", status="PASS", blocking=True, runner="person:operator:claude",
                             detail="looks fine")
        g = verify.gateway(e.store, jid, aid, {**req, "independent_review": "QA"})
        self.assertIn("independent_review", [b["check_id"] for b in g["blocking"]])

    def test_the_admin_cli_has_no_override_command_and_no_environment_flag_bypasses_the_founder(self):
        from product import admin
        src = (REPO / "product" / "admin.py").read_text()
        for word in ("waive", "override", "release", "select-take", "select_take", "resume", "attest"):
            self.assertNotIn(f'add_parser("{word}', src)
        env = {**os.environ, "PYTHONPATH": str(REPO), "MI_DATA_DIR": str(self.e.dir)}
        r = subprocess.run([sys.executable, "-m", "product.admin", "override", "--job", self.jid], env=env, capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("invalid choice", r.stderr)
        self.assertNotIn("os.environ", (REPO / "product" / "authority.py").read_text())
        self.assertNotIn("import os", (REPO / "product" / "authority.py").read_text())
        for flag in ("MI_FOUNDER_OVERRIDE", "MI_ALLOW_OVERRIDE", "MI_REVIEWER_QUALIFIED", "MI_OPERATOR"):
            os.environ[flag] = "1"
        try:
            with self.assertRaises(authority.NotFounder):
                authority.founder_proof(self.e.store, "operator:claude", job_id=self.jid)
        finally:
            for flag in ("MI_FOUNDER_OVERRIDE", "MI_ALLOW_OVERRIDE", "MI_REVIEWER_QUALIFIED", "MI_OPERATOR"):
                os.environ.pop(flag, None)
        self.assertIsInstance(admin.main, type(lambda: 0))

    def test_there_is_exactly_one_founder(self):
        self.e.founder_session()
        from product.service import Invalid
        with self.assertRaises(Invalid):
            self.e.svc.create_invite(email="second@mi.test", role="founder", account_id=None, by="cli")

    def test_the_founder_can_override_with_a_reason_that_is_stored_and_shown_in_the_gateway_report(self):
        """Spec §11 test 4."""
        e, jid = self.e, self.jid
        f = e.founder()
        aid = e.store.assets(jid, source="customer")[0]["id"]
        req = {"exact_copy_match": "EXACT_COPY_MATCH"}
        e.store.record_check(jid, aid, check_id="exact_copy_match", status="FAIL", blocking=True, runner="deterministic", detail="x")
        with self.assertRaises(ValueError):
            verify.waive(e.store, jid, aid, "exact_copy_match", founder=f, reason="ok")        # a reason is required
        verify.waive(e.store, jid, aid, "exact_copy_match", founder=f,
                     reason="The customer supplied this line as an image; the copy check cannot read it.")
        g = verify.gateway(e.store, jid, aid, req)
        self.assertTrue(g["ready"])
        self.assertEqual(g["waived"][0]["waived_by"], "founder@mi.test")
        self.assertIn("cannot read it", g["waived"][0]["waiver_reason"])
        self.assertEqual(g["founder_overrides"][0]["by"], "founder@mi.test")
        self.assertIn("cannot read it", g["founder_overrides"][0]["reason"])
        e.store.transition(jid, "paused_for_founder", "understanding", actor="ignored", founder=f, data={"reason": "resume"})
        last = e.store.events(jid, ("state",))[-1]
        self.assertEqual(last["actor"], "founder:founder@mi.test")
        self.assertEqual(len(e.store.overrides(jid)), 1)


class NoThirdIdenticalRetry(unittest.TestCase):
    """Spec §11 test 6."""

    def test_the_same_request_to_the_same_generator_is_refused_the_third_time_and_nothing_is_reserved(self):
        e = Env()
        try:
            jid = e.submit("image")
            e.store.set_job(jid, budget_authorised_by="test", budget_authorised_at=utc_now())
            d = Dispatcher(e.s, e.store)
            guard = {"exact_strings": [], "forbidden_words": []}
            kw = dict(prompt="A navy backpack on a table. No text, no lettering.", aspect="1:1", refs=[], guard=guard)
            d.image(jid, "plate_1x1", **kw)
            d.image(jid, "plate_1x1", **kw)
            n = len(e.store.attempts(jid))
            with self.assertRaises(IdenticalRequestRefused):
                d.image(jid, "plate_1x1", **kw)
            self.assertEqual(len(e.store.attempts(jid)), n)                    # refused before any reservation
            self.assertTrue(e.store.events(jid, ("identical_request_refused",)))
            d.image(jid, "plate_1x1", **{**kw, "prompt": kw["prompt"] + " Warmer light."})   # a changed request is allowed
            self.assertEqual(len(e.store.attempts(jid)), n + 1)
        finally:
            e.close()

    def test_a_transient_outage_is_not_counted_as_an_answer(self):
        e = Env(fault_injection={"image": [503, 503]})
        try:
            jid = e.submit("image")
            e.store.set_job(jid, budget_authorised_by="test", budget_authorised_at=utc_now())
            d = Dispatcher(e.s, e.store)
            kw = dict(prompt="A navy backpack. No text, no lettering.", aspect="1:1", refs=[],
                      guard={"exact_strings": [], "forbidden_words": []})
            from product.dispatch import DispatchFailed
            for _ in range(2):
                with self.assertRaises(DispatchFailed):
                    d.image(jid, "p", **kw)
            d.image(jid, "p", **kw)
            d.image(jid, "p", **kw)
            with self.assertRaises(IdenticalRequestRefused):
                d.image(jid, "p", **kw)
            row = e.store.q1("SELECT sent FROM request_fingerprints WHERE job_id=?", (jid,))
            self.assertEqual(row["sent"], 2)
        finally:
            e.close()


if __name__ == "__main__":
    unittest.main()
