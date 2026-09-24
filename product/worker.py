"""The production worker: claims runnable jobs under a lease, recovers anything a dead worker left
in flight, advances one step, repeats. Safe to run as several processes; safe to kill at any point.

    python3 -m product.worker            # loop forever
    python3 -m product.worker --once     # drain what is runnable now, then exit
"""
from __future__ import annotations

import argparse
import logging
import os
import secrets
import signal
import threading
import time

from product import config
from product.orchestrator import Orchestrator
from product.states import WORKER_STATES
from product.store import Store

log = logging.getLogger("mi.worker")


class Worker:
    def __init__(self, settings, store: Store, orch: Orchestrator | None = None):
        self.s, self.store = settings, store
        self.orch = orch or Orchestrator(settings, store)
        self.id = f"w-{os.getpid()}-{secrets.token_hex(3)}"
        self.stop = threading.Event()

    def run_once(self) -> bool:
        job = self.store.claim(WORKER_STATES, self.id, self.s.lease_seconds)
        if job is None:
            return False
        jid = job["id"]
        # Only the lease holder runs a step, and a step settles its own reservations before it returns. So a reservation
        # still open when a job is claimed was left by a step that died (killed process, expired lease, or an exception
        # that unwound it): settle those in-flight calls first — whichever way the previous worker went.
        if any(a["status"] == "reserved" for a in self.store.attempts(jid)):
            rec = self.orch.dispatch.recover(jid)
            if rec:
                self.store.event(jid, self.id, "recovered_in_flight", {"attempts": rec})
        done = threading.Event()
        hb = threading.Thread(target=self._heartbeat, args=(jid, done), daemon=True)
        hb.start()
        try:
            before = job["state"]
            after = self.orch.step(jid)
            log.info("job %s: %s -> %s", jid, before, after)
        finally:
            done.set()
            hb.join(timeout=5)
            self.store.release(jid, self.id)
        return True

    def _heartbeat(self, jid, done: threading.Event):
        while not done.wait(min(30, self.s.lease_seconds / 3)) and not self.stop.is_set():
            self.store.renew(jid, self.id, self.s.lease_seconds)

    def drain(self, max_steps: int = 500) -> int:
        n = 0
        while n < max_steps and self.run_once():
            n += 1
        return n

    def forever(self, idle_s: float = 2.0):
        signal.signal(signal.SIGTERM, lambda *_: self.stop.set())
        while not self.stop.is_set():
            try:
                if not self.run_once():
                    self.stop.wait(idle_s)
            except Exception:  # noqa: BLE001 — the loop must survive; the step already recorded the fault
                log.exception("worker loop error")
                self.stop.wait(idle_s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true")
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    s = config.load()
    w = Worker(s, Store(s.db_path))
    log.info("worker %s starting (providers=%s reasoning=%s data=%s)", w.id, s.provider_mode, s.reasoning_mode, s.data_dir)
    if a.once:
        w.drain()
    else:
        w.forever()


if __name__ == "__main__":
    main()
