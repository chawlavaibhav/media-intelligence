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

    def operator(self, email="founder@mi.test"):
        tok = self.svc.create_invite(email=email, role="operator", account_id=None, by="test")
        self.svc.redeem_invite(tok, name="Founder", password="correct horse battery")
        return self.store.user_by_email(email)

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

    def waive_all(self, jid, why="DRY RUN — simulated media; nothing was verified"):
        from product import verify
        g = self.store.artifact(jid, "gateway")
        for r in g["results"]:
            for b in r["blocking"]:
                if b["check_id"] in verify.NON_WAIVABLE:
                    verify.attest(self.store, jid, r["asset_id"], b["check_id"], by="operator:test",
                                  note="DRY RUN — test tone and pink noise only; no real listen was needed")
                else:
                    self.store.waive(jid, r["asset_id"], b["check_id"], "operator:test", why)

    def to_review(self, jid, budget="15"):
        """submitted → ready_for_review, with the operator waiving what a dry run cannot verify."""
        self.drain()
        assert self.state(jid) == "awaiting_approval", self.state(jid)
        self.orch.approve(jid, by=self.user["email"], budget_usd=budget)
        self.drain()
        assert self.state(jid) == "operator_hold", (self.state(jid), self.store.job(jid)["pause_reason"])
        self.waive_all(jid)
        self.orch.release_hold(jid, "operator:test")
        return jid

    def close(self):
        shutil.rmtree(self.dir, ignore_errors=True)
