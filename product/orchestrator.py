"""The flow controller ("the kitchen", v3 — founder-approved 2026-09-25): code holds the state and the memory; each role
does its job from its card.

    state                      role
    submitted / understanding  stations/waiter.py      (the waiter: Understanding; questions only when they change the dish)
    directing                  stations/chef.py        (the chef: librarian tray incl. the Canon → the Recipe, written in full)
    awaiting_approval          the customer            (the recipe, the price and the look of the film: go ahead or change)
    planning / producing       stations/head_cook.py   (the head cook: cooks, tastes every take on another company's model,
                                                        repairs; posts kept stills to the customer's page)
    checking                   stations/tasters.py     (the gatekeeper: the finished dish against the order)
    revising                   stations/changes.py     (the customer's changes to a finished dish)
    closed jobs                stations/diary.py       (the memory keeper: lessons, applied automatically, undoable)

The pantry checker and the recipe checker are retired (a job found in `feasibility` is handed straight to the chef). The
founder is never inside a running job; a step error retries twice by itself, then the customer chooses try again / stop.

Every step reads its inputs from the store, writes its outputs, and ends in a compare-and-set transition, so a restarted
worker re-runs at most the step it was in. Customer decisions are methods taking the customer's email; founder decisions
take the founder's SESSION TOKEN and are refused for anyone else (authority.py).
"""
from __future__ import annotations

import json
import time
import traceback
from decimal import Decimal
from pathlib import Path

from product import authority, flow, library, media, rulebook, verify
from product.ai import Workers
from product.config import Settings, scrub
from product.dispatch import Dispatcher, GuardRefused
from product.lessons import LessonQueue
from product.library.librarian import Librarian
from product.reasoning import ProviderUnavailable, Reasoner, ReasoningFailed
from product.shelf import Shelf
from product.stations.simulated import SimulatedWorkers
from product.store import BudgetExhausted, StaleState, Store, dec, money, utc_now

PREVIEW_ALLOWANCE_USD = Decimal("3.00")      # planning reasoning + the sample picture, authorised at submission
STEP_RETRIES = 2                             # automatic retries of a step that errored, then the customer (2026-09-24)


class NodeFailed(Exception):
    pass


class Orchestrator:
    def __init__(self, settings: Settings, store: Store, *, providers=None, reasoner=None, simulated=None):
        self.s, self.store = settings, store
        self.dispatch = Dispatcher(settings, store, providers)
        self.llm = reasoner or Reasoner(settings, store)
        self.rulebook = rulebook.Rulebook(store)
        self.sim = simulated or SimulatedWorkers()
        self.workers = Workers(settings, store, self.llm, self.rulebook, self.sim)
        self.shelf = Shelf(store, settings.data_dir)
        self.equipment = library.EquipmentSheet(store)
        self.failures = library.FailureDiary(store)
        self.recipes = library.RecipeLibrary(store)
        self.librarian = Librarian(store, self.equipment, self.failures, self.recipes, self.shelf)
        self.lessons = LessonQueue(store, rulebook=self.rulebook, equipment=self.equipment, recipes=self.recipes,
                                   failures=self.failures, shelf=self.shelf)

    # ── the job file ────────────────────────────────────────────────────────────────────────────────────
    def brief(self, job_id) -> dict:
        return self.store.original_brief(job_id)

    def exact_words(self, job_id) -> str:
        """The customer's brief exactly as submitted: stored once (fingerprinted), never edited, sent to every AI worker."""
        return self.brief(job_id)["text"]

    def job_dir(self, job_id) -> Path:
        d = self.s.media_dir / job_id
        d.mkdir(parents=True, exist_ok=True)
        return d

    def uploads(self, job_id, role=None):
        rows = self.store.assets(job_id, source="customer")
        return [r for r in rows if role is None or r["role"] == role]

    def photos(self, job_id) -> list:
        """The customer's photos in order slip order (product and reference images; the logo is separate)."""
        return [a for a in self.uploads(job_id) if a["role"] in ("product", "reference")
                and a["content_type"] in ("image/png", "image/jpeg", "image/webp")]

    def photo_media(self, job_id, limit=6) -> list:
        return [(a["content_type"], Path(a["path"]).read_bytes()) for a in self.photos(job_id)[:limit] if a["bytes"] < 7_000_000]

    def logo(self, job_id):
        rows = self.uploads(job_id, "logo")
        if rows:
            return Path(rows[-1]["path"])
        job = self.store.job(job_id)
        for it in self.shelf.approved(job["account_id"], "logo"):
            if it["path"]:
                self.shelf.record_use(job_id, job["account_id"], it["id"], "logo")
                return Path(it["path"])
        return None

    def order_slip(self, job_id) -> dict:
        """The Order slip form (spec §4.1). Written once, and again (a new version) only when the customer adds photos."""
        brief = self.brief(job_id)
        job = self.store.job(job_id)
        photos = [{"photo": i + 1, "asset_id": a["id"], "customer_label": json.loads(a["meta_json"]).get("label"),
                   "filename": json.loads(a["meta_json"]).get("filename") or ""} for i, a in enumerate(self.photos(job_id))]
        cur = self.store.artifact(job_id, "order_slip")
        if cur and [p["asset_id"] for p in cur["photos"]] == [p["asset_id"] for p in photos]:
            return cur
        colours = list(brief.get("brand_colours") or [])
        prefilled = []
        if not colours:
            for it in self.shelf.approved(job["account_id"], "brand_colour"):
                colours.append(json.loads(it["data_json"]).get("hex"))
                self.shelf.record_use(job_id, job["account_id"], it["id"], "brand_colour")
                prefilled.append(it["id"])
        slip = {"customer_exact_words": brief["text"], "media": brief["media"], "formats": brief.get("formats") or [],
                "duration_s": brief.get("duration_s"), "exact_strings": brief.get("exact_strings") or [], "product": brief.get("product") or {},
                "brand_colours": [c for c in colours if c], "photos": photos, "max_budget_usd": str(brief.get("max_budget_usd") or "0"),
                "forbidden_words": brief.get("forbidden_words") or [], "references_note": brief.get("references_note") or "",
                "prefilled_from_shelf": prefilled}
        self.put_form(job_id, "order_slip", slip, by="customer", stamp=False)
        return slip

    def put_form(self, job_id, name: str, body: dict, *, by: str | None = None, stamp: bool = True) -> int:
        errs = rulebook.validate(name, body)
        if errs:
            raise ReasoningFailed(f"{name} form failed its schema: {errs[:5]}")
        if stamp and "form_version" not in body:
            body.update({"job_id": job_id, "form": name, "form_version": rulebook.form(name)["version"],
                         "written_by": {"worker": by or rulebook.form(name)["written_by"], "model": "code"},
                         "rulebook_card_version": self.rulebook.version(by) if by in rulebook.seed_cards() else None,
                         "created_utc": utc_now()})
        return self.store.put_artifact(job_id, name, body, by or (body.get("written_by") or {}).get("worker") or rulebook.form(name)["written_by"])

    def pause(self, job_id, frm, to, reason, actor="system"):
        self.store.transition(job_id, frm, to, actor=actor, data={"reason": reason}, resume_state=frm, pause_reason=reason[:600])

    # ── worker entry ───────────────────────────────────────────────────────────────────────────────────
    STEPS = {"submitted": ("waiter", "understand"), "understanding": ("waiter", "understand"), "feasibility": ("waiter", "hand_to_chef"),
             "directing": ("chef", "direct"), "planning": ("head_cook", "plan"), "producing": ("head_cook", "produce"),
             "checking": ("tasters", "check_cut"), "revising": ("changes", "revise")}

    def step(self, job_id: str) -> str:
        import importlib
        state = self.store.job(job_id)["state"]
        if state == "paused_provider":
            fn = self.resume_provider
        elif state in self.STEPS:
            mod, name = self.STEPS[state]
            fn = getattr(importlib.import_module(f"product.stations.{mod}"), name)
        else:
            return state
        try:
            self._step(fn, job_id, state)
        except BudgetExhausted as e:
            self.pause(job_id, state, "paused_budget", f"needs about USD {e.shortfall} more (USD {e.available} of USD {e.budget} left)")
        except ProviderUnavailable as e:
            self.pause(job_id, state, "paused_provider", f"a production service is unavailable: {scrub(str(e))[:200]}")
        except flow.LimitReached as e:
            self._limit_reached(job_id, state, e)
        except StaleState:
            pass
        except (ReasoningFailed, NodeFailed, GuardRefused, media.MediaError) as e:
            self.store.event(job_id, "system", "step_failed", {"state": state, "error": scrub(str(e))[:800]})
            self._step_error(job_id, state, scrub(str(e))[:300])
        except Exception as e:  # noqa: BLE001 — any unexpected fault is recorded, never swallowed silently
            self.store.event(job_id, "system", "step_crashed", {"state": state, "error": scrub(repr(e))[:800],
                                                                 "trace": scrub(traceback.format_exc())[-2000:]})
            self._step_error(job_id, state, f"internal error: {scrub(repr(e))[:200]}")
        now = self.store.job(job_id)["state"]
        if now != state:                    # it's the customer's turn: tell them (page always; email when configured)
            from product import customer
            customer.notify_turn(self, job_id, now)
        return now

    def _step(self, fn, job_id, state):
        fn(job_id) if state == "paused_provider" else fn(self, job_id)

    def _retries(self, job_id, state) -> int:
        """Automatic retries of `state` since the job last changed state (a customer's "try again" starts afresh)."""
        n = 0
        for e in reversed(self.store.events(job_id, ("state", "step_retry"))):
            if e["kind"] == "state":
                break
            n += json.loads(e["data_json"]).get("state") == state
        return n

    def _step_error(self, job_id, state, error: str):
        """Beta rules 2026-09-24: a step that errored is retried by the system (at most STEP_RETRIES times, each an event);
        then the customer decides: try again (the same step, fresh retries) or stop (closed; nothing more is spent)."""
        try:
            if self.store.job(job_id)["state"] != state:
                return                                         # the step moved the job on before it failed: nothing to retry
            n = self._retries(job_id, state)
            if n < STEP_RETRIES:
                self.store.event(job_id, "system", "step_retry", {"state": state, "retry": n + 1, "error": error[:300]})
                return                                         # the job stays in `state`: the next worker claim re-runs it
            resume = self.store.job(job_id)["resume_state"] if state == "paused_provider" else state
            self.store.transition(job_id, state, "needs_retry_decision", actor="system",
                                  data={"reason": error, "retries": n}, resume_state=resume,
                                  pause_reason="Something went wrong on our side and our automatic retries did not fix it. "
                                               "You can ask us to try again, or stop here (nothing more is spent).")
            self.store.timing_start(job_id, "customer_wait", "retry")
        except StaleState:
            pass

    def _limit_reached(self, job_id, state, e):
        """A send-back limit that no station handled: a step error — retried, then the customer's try again / stop."""
        self.store.event(job_id, "system", "step_failed", {"state": state, "error": str(e)[:800]})
        self._step_error(job_id, state, str(e)[:300])

    def resume_provider(self, job_id):
        job = self.store.job(job_id)
        last = self.store.events(job_id, ("state",))[-1]
        if time.time() - _ts(last["utc"]) < getattr(self.s, "provider_retry_after_s", 60):
            return
        self.store.transition(job_id, "paused_provider", job["resume_state"], actor="system", data={"reason": "retrying after provider pause"},
                              pause_reason=None)

    def _end_wait(self, job_id, label):
        for t in self.store.timings(job_id):
            if t["phase"] == "customer_wait" and t["label"] == label and t["ended"] is None:
                self.store.timing_end(t["id"])

    # ── customer decisions ─────────────────────────────────────────────────────────────────────────────
    def answer(self, job_id, answers: dict, by: str):
        self.store.put_artifact(job_id, "answers", answers, by)
        self._end_wait(job_id, "answers")
        self.store.transition(job_id, "needs_answers", "understanding", actor=by, data={"answered": sorted(answers)})

    def provide_input(self, job_id, *, by: str, accepted_alternatives: list = (), facts: list = (), note: str = ""):
        """The customer answers the pantry checker: photos (uploaded through the service), facts, accepted alternatives."""
        prev = self.store.artifact(job_id, "customer_input") or {}
        data = {"accepted_alternatives": list(prev.get("accepted_alternatives", [])) + list(accepted_alternatives),
                "facts": list(prev.get("facts", [])) + [f for f in facts if f], "note": note[:1000], "by": by}
        self.store.put_artifact(job_id, "customer_input", data, by)
        self._end_wait(job_id, "customer_input")
        self.store.transition(job_id, "awaiting_customer_input", "understanding", actor=by, data={"customer_input": True})

    def approve(self, job_id, *, by: str, budget_usd, note: str = "", accept_objections: bool = False):
        from product.stations import chef
        return chef.approve(self, job_id, by=by, budget_usd=budget_usd, note=note, accept_objections=accept_objections)

    def request_plan_change(self, job_id, text: str, by: str):
        self.store.put_artifact(job_id, "plan_change", {"request": text, "by": by}, by)
        self._end_wait(job_id, "approval")
        self.store.transition(job_id, "awaiting_approval", "directing", actor=by, data={"change": text[:300]})

    request_direction_change = request_plan_change

    def approve_master(self, job_id, *, by: str, founder_session: str | None = None):
        from product.stations import head_cook
        return head_cook.approve_master(self, job_id, by=by, founder_session=founder_session)

    def approve_taste(self, job_id, *, by: str):
        from product.stations import head_cook
        return head_cook.approve_taste(self, job_id, by=by)

    def change_taste(self, job_id, *, by: str, text: str):
        from product.stations import head_cook
        return head_cook.change_taste(self, job_id, by=by, text=text)

    def request_changes(self, job_id, by: str, items: list):
        from product.stations import changes
        return changes.request(self, job_id, by, items)

    def decide(self, job_id, *, by: str, choice: str, note: str = "", budget_usd=None):
        """A measured check failed and the automatic repairs are used up: the customer stops or pays for a rework. After a
        step error the same customer decision is try again / stop (after_error)."""
        if self.store.job(job_id)["state"] == "needs_retry_decision":
            return self.after_error(job_id, by=by, choice=choice, note=note)
        from product.stations import tasters
        return tasters.decide(self, job_id, by=by, choice=choice, note=note, budget_usd=budget_usd)

    def after_error(self, job_id, *, by: str, choice: str, note: str = ""):
        """The customer's answer to needs_retry_decision (beta rules 2026-09-24): "try_again" resumes the step that errored
        (with fresh automatic retries); "stop" closes the job — nothing more is spent on production."""
        job = self.store.job(job_id)
        if job["state"] != "needs_retry_decision":
            raise ValueError("there is nothing waiting for you to try again")
        if choice not in ("try_again", "stop"):
            raise ValueError(f"choose try_again or stop, not {choice!r}")
        self._end_wait(job_id, "retry")
        if choice == "try_again":
            self.store.event(job_id, by, "customer_retry", {"state": job["resume_state"]})
            self.store.transition(job_id, "needs_retry_decision", job["resume_state"], actor=by, data={"try_again": True},
                                  pause_reason=None)
            return
        from product.stations import diary
        self.store.transition(job_id, "needs_retry_decision", "abandoned", actor=by,
                              data={"reason": note[:300] or "the customer stopped after an error on our side"},
                              closed_at=utc_now(), outcome="abandoned")
        diary.write(self, job_id)

    def accept(self, job_id, by: str):
        from product.stations import tasters
        return tasters.accept(self, job_id, by)

    def reject(self, job_id, by: str, reason: str):
        from product.stations import diary
        for aid in self.final_assets(job_id):
            self.store.add_feedback(job_id, asset_id=aid, target=None, text=reason, kind="reject", by_user=by)
        self._end_wait(job_id, "review")
        self.store.transition(job_id, ("ready_for_review", "awaiting_approval", "needs_answers", "paused_budget"), "rejected",
                              actor=by, data={"reason": reason[:300]}, closed_at=utc_now(), outcome="rejected")
        diary.write(self, job_id)

    def abandon(self, job_id, by: str, reason: str, founder_session: str | None = None):
        """The customer walks away (or the founder closes a job). Every closed job still produces lessons (spec §7.5)."""
        from product.stations import diary
        job = self.store.job(job_id)
        proof = authority.founder_proof(self.store, founder_session, job_id=job_id, action="close the job") if founder_session else None
        self._end_wait(job_id, "review")
        self.store.transition(job_id, job["state"], "abandoned", actor=by, founder=proof, data={"reason": reason[:300]},
                              closed_at=utc_now(), outcome="abandoned")
        diary.write(self, job_id)

    # ── founder decisions (a signed-in founder session; anyone else is refused and logged) ─────────────
    def founder(self, session, job_id, action):
        return authority.founder_proof(self.store, session, job_id=job_id, action=action)

    def founder_resume(self, job_id, *, session, to: str | None = None, reason: str):
        proof = self.founder(session, job_id, "resume the job")
        job = self.store.job(job_id)
        reason = authority.check_reason(reason)
        target = to or job["resume_state"]
        self.store.add_override(job_id, kind="resume", target=f"{job['state']}->{target}", founder=proof, reason=reason)
        self.store.transition(job_id, job["state"], target, actor=proof.actor, founder=proof, data={"reason": reason}, pause_reason=None)

    def override_final_review(self, job_id, *, session, reason: str):
        from product.stations import tasters
        return tasters.founder_override(self, job_id, self.founder(session, job_id, "override the gatekeeper"), reason)

    def waive_check(self, job_id, *, session, asset_id: str, check_id: str, reason: str):
        proof = self.founder(session, job_id, f"waive {check_id}")
        verify.waive(self.store, job_id, asset_id, check_id, founder=proof, reason=reason)

    def confirm_check(self, job_id, *, session, asset_id: str, check_id: str, note: str, outcome: str = "PASS"):
        proof = self.founder(session, job_id, f"confirm {check_id}")
        verify.attest(self.store, job_id, asset_id, check_id, founder=proof, note=note, outcome=outcome)

    def release(self, job_id, *, session):
        from product.stations import tasters
        return tasters.release(self, job_id, self.founder(session, job_id, "release the cut to the customer"))

    release_hold = release

    # ── shared helpers used by stations and pages ───────────────────────────────────────────────────────
    def final_assets(self, job_id):
        return [n["selected_asset_id"] for n in self.store.nodes(job_id) if n["kind"] in ("compose_still", "assemble") and n["selected_asset_id"]]

    _final_assets = final_assets

    def exact_strings(self, job_id) -> list:
        """The customer's exact strings, with any change the customer later requested applied."""
        from product.stations.tasters import exact_strings
        return exact_strings(self, job_id)

    def qualified(self, judge: str, model: str | None = None) -> bool:
        """Only a founder-recorded live qualification run, for the exact model now configured — or `model`, the one that
        actually judged (an image job's final check runs on gatekeeper_image) (reviewer 2026-09-24). No setting, env flag
        or admin command makes a judge qualified."""
        return self.store.qualification(judge, model or self.s.models.get(judge)) is not None


def _ts(utc: str) -> float:
    from datetime import datetime, timezone
    return datetime.strptime(utc, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc).timestamp()


def money_str(v) -> str:
    return money(dec(v))
