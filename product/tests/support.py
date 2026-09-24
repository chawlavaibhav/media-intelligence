"""Shared fixtures: a fresh data directory, an account, a customer, and a submit helper. USD 0, no network."""
from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from product import config
from product.service import Service
from product.store import Store
from product.worker import Worker
from runtime.loop.synthetic import make_png

FILM_BRIEF = ("A 20 second film for our travel backpack that shows how much it fits. Warm, a bit funny. "
              "End on our line. It must show the bag being zipped shut.")
IMAGE_BRIEF = "A festive Diwali poster for our 1 litre mustard oil tin; the tin must be the first thing you see; no people."


class Env:
    def __init__(self, **settings):
        self.dir = Path(tempfile.mkdtemp(prefix="mi-test-"))
        self.s = config.load(self.dir, provider_retry_after_s=0, **settings)
        self.store = Store(self.s.db_path)
        self.svc = Service(self.s, self.store)
        self.orch = self.svc.orch
        self.worker = Worker(self.s, self.store, self.orch)
        self.acct = self.store.create_account("Acme D2C", ceiling_usd="40")
        self.user = self.customer("buyer@acme.test", self.acct)

    def customer(self, email, acct):
        tok = self.svc.create_invite(email=email, role="customer", account_id=acct, by="test")
        self.svc.redeem_invite(tok, name="Buyer", password="correct horse battery")
        return self.store.user_by_email(email)

    def operator(self, email="ops@mi.test"):
        tok = self.svc.create_invite(email=email, role="operator", account_id=None, by="test")
        self.svc.redeem_invite(tok, name="Ops", password="correct horse battery")
        return self.store.user_by_email(email)

    def founder_session(self, email="founder@mi.test") -> str:
        """The one founder account, signed in: returns the session token (what the web app holds in its cookie)."""
        if not self.store.user_by_email(email):
            tok = self.svc.create_invite(email=email, role="founder", account_id=None, by="test")
            self.svc.redeem_invite(tok, name="Founder", password="correct horse battery")
        return self.svc.login(email, "correct horse battery")

    def founder(self, email="founder@mi.test"):
        from product.authority import founder_proof
        return founder_proof(self.store, self.founder_session(email))

    def session_of(self, email) -> str:
        return self.svc.login(email, "correct horse battery")

    def submit(self, media="video", text=None, budget="20", exact=("Pack less. Go further.",), user=None, **kw):
        return self.svc.submit(user or self.user, title=f"test {media}", media=media, text=text or (FILM_BRIEF if media == "video" else IMAGE_BRIEF),
                               formats=kw.pop("formats", ["9:16"] if media == "video" else ["1:1", "4:5"]), duration_s=kw.pop("duration_s", 20),
                               exact_strings=list(exact), product={"name": "Voyager 30L", "brand": "Acme", "category": "backpack",
                                                                   "description": "30 litre, navy, yellow lining"},
                               brand_colours=["#1f2a44"], max_budget_usd=budget, allow_preview_spend=True,
                               uploads=[{"role": "product", "filename": "bag.png", "data": make_png(64, 64, seed=2)},
                                        {"role": "logo", "filename": "logo.png", "data": make_png(32, 16, seed=5)}], **kw)

    def drain(self):
        return self.worker.drain()

    def state(self, jid):
        return self.store.job(jid)["state"]

    def front(self, jid):
        """v2 front of house: accept the pantry checker's alternatives → the plan card (no founder step: amendment 1 §3)."""
        self.drain()
        if self.state(jid) == "awaiting_customer_input":
            f = self.store.artifact(jid, "feasibility")
            self.orch.provide_input(jid, by=self.user["email"], accepted_alternatives=[
                {"instead_of": x["for_action"], "use": "the bag shown closed and zipped as a still"} for x in f["alternatives"]])
            self.drain()
        return self.state(jid)

    def produce(self, jid):
        """After approval: drain, approving the master plate and the taste (the customer) whenever production waits."""
        self.drain()
        while self.state(jid) in ("awaiting_master_approval", "awaiting_taste"):
            if self.state(jid) == "awaiting_master_approval":
                self.orch.approve_master(jid, by=self.user["email"])
            else:
                self.orch.approve_taste(jid, by=self.user["email"])      # the customer tastes the hardest shot
            self.drain()
        return self.state(jid)

    def waive_all(self, jid, why="DRY RUN — simulated media; nothing was verified"):
        """The founder, at the door, in a dry run: confirm the person-checks and waive what a simulation cannot verify."""
        from product import verify
        s = self.founder_session()
        g = self.store.artifact(jid, "gateway_report")
        for r in g["results"]:
            for b in r["blocking"]:
                if verify.attestable(b["check_id"]):
                    self.orch.confirm_check(jid, session=s, asset_id=r["asset_id"], check_id=b["check_id"],
                                            note="DRY RUN — test tone and pink noise only; no real look or listen was possible")
                else:
                    self.orch.waive_check(jid, session=s, asset_id=r["asset_id"], check_id=b["check_id"], reason=why)

    def release(self, jid):
        self.orch.release(jid, session=self.founder_session())

    def to_review(self, jid, budget="15"):
        """submitted → ready_for_review. Nobody waits for the founder (amendment 1 §3); only when a test switched the
        founder's hold on does the founder confirm/waive and release."""
        assert self.front(jid) == "awaiting_approval", self.state(jid)
        self.orch.approve(jid, by=self.user["email"], budget_usd=budget)
        self.produce(jid)
        if self.state(jid) == "operator_hold":
            self.waive_all(jid)
            self.release(jid)
        assert self.state(jid) == "ready_for_review", (self.state(jid), self.store.job(jid)["pause_reason"])
        return jid

    def close(self):
        shutil.rmtree(self.dir, ignore_errors=True)
