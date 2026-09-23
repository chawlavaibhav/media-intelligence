"""The orchestrator: code holds the state, LLMs are components.

Each worker state has one step function. A step reads its inputs from the store, writes its outputs
atomically, and ends in a compare-and-set transition, so a restarted worker re-runs at most the step it
was in — and the dispatcher's recovery makes sure a paid call in flight is resumed or recorded, never
silently repeated.

Stage map: 1 understand → (answers) → 2/3 direct (Canon + concept + board + independent pre-spend
review + quote + preview stills) → customer approval + budget → 4 plan (asset graph) → 5 produce
(graph, concurrent where dependencies allow; riskiest action qualified first) → check (deterministic +
independent review → gateway) → operator hold / customer review → targeted revision → accept → deliver.
"""
from __future__ import annotations

import json
import re
import shutil
import threading
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from decimal import Decimal
from pathlib import Path

from product import canon_access, compose, media, prompts, verify
from product.config import Settings, scrub
from product.dispatch import DispatchFailed, Dispatcher, GuardRefused, quote
from product.reasoning import ProviderUnavailable, Reasoner, ReasoningFailed
from product.store import BudgetExhausted, StaleState, Store, dec, money, utc_now

PREVIEW_ALLOWANCE_USD = Decimal("3.00")      # planning reasoning + preview stills, authorised at submission
MAX_INTERNAL_REPAIRS = 1
TRANSIENT_RETRIES = 3
CLIP_LENGTHS = (4, 6, 8)


class NeedsPerson(Exception):
    """Every draw of a node was rejected by an inspector that is not qualified to reject on its own: a person picks."""
    def __init__(self, node_id, candidates, why):
        super().__init__(f"{node_id}: a person picks a take from {candidates} (inspector: {why})")
        self.node_id, self.candidates, self.why = node_id, candidates, why


class NodeFailed(Exception):
    pass


def clip_len(use_s: float) -> int:
    for c in CLIP_LENGTHS:
        if use_s + 0.4 <= c:
            return c
    return 8


class Orchestrator:
    def __init__(self, settings: Settings, store: Store, *, providers=None, reasoner=None):
        self.s, self.store = settings, store
        self.dispatch = Dispatcher(settings, store, providers)
        self.llm = reasoner or Reasoner(settings, store)
        self._lock = threading.Lock()

    # ── helpers ────────────────────────────────────────────────────────────────────────────────
    def brief(self, job_id) -> dict:
        return self.store.original_brief(job_id)

    def job_dir(self, job_id) -> Path:
        d = self.s.media_dir / job_id
        d.mkdir(parents=True, exist_ok=True)
        return d

    def uploads(self, job_id, role=None):
        rows = self.store.assets(job_id, source="customer")
        return [r for r in rows if role is None or r["role"] == role]

    def _ref_images(self, job_id, limit=3):
        out = []
        for a in self.uploads(job_id, "product")[:limit]:
            if a["content_type"] in ("image/png", "image/jpeg", "image/webp") and a["bytes"] < 7_000_000:
                out.append((a["content_type"], Path(a["path"]).read_bytes()))
        return out

    def _brief_docs(self, job_id, limit=2):
        """PDF references the customer supplied (brief decks, storyboards) — read by the planning roles."""
        return [(a["content_type"], Path(a["path"]).read_bytes()) for a in self.uploads(job_id)
                if a["content_type"] == "application/pdf" and a["bytes"] < 20_000_000][:limit]

    def _logo(self, job_id):
        rows = self.uploads(job_id, "logo")
        return Path(rows[-1]["path"]) if rows else None

    def _pause(self, job_id, frm, to, reason, actor="system"):
        self.store.transition(job_id, frm, to, actor=actor, data={"reason": reason}, resume_state=frm, pause_reason=reason)

    # ── worker entry ───────────────────────────────────────────────────────────────────────────
    def step(self, job_id: str) -> str:
        job = self.store.job(job_id)
        state = job["state"]
        fn = {"submitted": self.understand, "understanding": self.understand, "directing": self.direct,
              "planning": self.plan, "producing": self.produce, "checking": self.check, "revising": self.revise,
              "paused_provider": self.resume_provider}.get(state)
        if fn is None:
            return state
        try:
            fn(job_id)
        except BudgetExhausted as e:
            self._pause(job_id, state, "paused_budget",
                        f"needs about USD {e.shortfall} more (USD {e.available} of USD {e.budget} left)")
        except ProviderUnavailable as e:
            self._pause(job_id, state, "paused_provider", f"a production service is unavailable: {scrub(str(e))[:200]}")
        except StaleState:
            pass                                  # someone else moved the job; nothing to do
        except (ReasoningFailed, NodeFailed, GuardRefused, media.MediaError) as e:
            self.store.event(job_id, "system", "step_failed", {"state": state, "error": scrub(str(e))[:800]})
            self._pause(job_id, state, "failed", scrub(str(e))[:300])
        except Exception as e:  # noqa: BLE001 — any unexpected fault is recorded, never swallowed silently
            self.store.event(job_id, "system", "step_crashed", {"state": state, "error": scrub(repr(e))[:800],
                                                                 "trace": scrub(traceback.format_exc())[-2000:]})
            try:
                self._pause(job_id, state, "failed", f"internal error: {scrub(repr(e))[:200]}")
            except StaleState:
                pass
        return self.store.job(job_id)["state"]

    def resume_provider(self, job_id):
        job = self.store.job(job_id)
        last = self.store.events(job_id, ("state",))[-1]
        if time.time() - _ts(last["utc"]) < getattr(self.s, "provider_retry_after_s", 60):
            return
        self.store.transition(job_id, "paused_provider", job["resume_state"], actor="system", data={"reason": "retrying after provider pause"},
                              pause_reason=None)

    # ── Stage 1: intent ────────────────────────────────────────────────────────────────────────
    def understand(self, job_id):
        job = self.store.job(job_id)
        if job["state"] == "submitted":
            self.store.transition(job_id, "submitted", "understanding", actor="system")
        brief = self.brief(job_id)
        answers = self.store.artifact(job_id, "answers") or {}
        ctx = {"BRIEF": _brief_for_model(brief), "ANSWERS": answers or "none yet",
               "SUPPLIED_ASSETS": [{"role": a["role"], "type": a["content_type"], "name": json.loads(a["meta_json"]).get("filename")}
                                   for a in self.uploads(job_id)]}
        with self.store.timed(job_id, "understanding"):
            intent = self.llm.call(job_id, "strategist", ctx, media=self._ref_images(job_id, 2) + self._brief_docs(job_id), max_tokens=8000)
        _enforce_intent(intent, brief)
        self.store.put_artifact(job_id, "intent", intent, "strategist")
        if not intent["supported"]:
            self.store.transition(job_id, "understanding", "refused", actor="system",
                                  data={"reason": intent.get("refusal_reason"), "alternative": intent.get("nearest_supported_alternative")},
                                  closed_at=utc_now(), outcome="refused")
            return
        if intent.get("questions") and not answers:
            self.store.transition(job_id, "understanding", "needs_answers", actor="system")
            self.store.timing_start(job_id, "customer_wait", "answers")
            return
        self.store.transition(job_id, "understanding", "directing", actor="system")

    def answer(self, job_id, answers: dict, by: str):
        self.store.put_artifact(job_id, "answers", answers, by)
        self._end_wait(job_id, "answers")
        self.store.transition(job_id, "needs_answers", "understanding", actor=by, data={"answered": sorted(answers)})

    def _end_wait(self, job_id, label):
        for t in self.store.timings(job_id):
            if t["phase"] == "customer_wait" and t["label"] == label and t["ended"] is None:
                self.store.timing_end(t["id"])

    # ── Stages 2–3: structure + creative ───────────────────────────────────────────────────────
    def direct(self, job_id):
        brief, intent = self.brief(job_id), self.store.artifact(job_id, "intent")
        media_kind = intent["deliverable"]["media"]
        packs = canon_access.practical_packs(
            media=media_kind, brief_text=brief.get("text", ""), market=intent.get("market", "IN"), language=intent.get("language", "en"),
            product={"category": intent["product"].get("category"), "brand": intent.get("brand")},
            exact_strings=brief.get("exact_strings", []), has_product_photo=bool(self.uploads(job_id, "product")))
        ctx = {"BRIEF": _brief_for_model(brief), "INTENT": _public(intent), "ANSWERS": self.store.artifact(job_id, "answers") or "none",
               "DOSSIER": {"brand": intent.get("brand"), "facts": intent["product"].get("facts", []),
                           "brand_colours": brief.get("brand_colours", []), "has_logo": bool(self._logo(job_id)),
                           "product_photos": len(self.uploads(job_id, "product"))}}
        prior = self.store.artifact(job_id, "concept_change")
        if prior:
            ctx["CUSTOMER_CHANGE_REQUEST"] = prior
        refs = self._ref_images(job_id, 3)
        with self.store.timed(job_id, "creative_planning"):
            d = self.llm.call(job_id, "creative_director", ctx, knowledge=packs["payload"], media=refs + self._brief_docs(job_id),
                              max_tokens=16000)
            retrieved = []
            if d.get("knowledge_requests"):
                with self.store.timed(job_id, "canon_consultation", "deep"):
                    retrieved = canon_access.deep_retrieve(d["knowledge_requests"][:4], limit=12)
                ctx["RETRIEVED_CLAIMS"] = retrieved
                ctx["NOTE"] = "Deeper knowledge you asked for is in RETRIEVED_CLAIMS. Finalise; knowledge_requests must now be empty."
                d = self.llm.call(job_id, "creative_director", ctx, knowledge=packs["payload"], media=refs + self._brief_docs(job_id),
                              max_tokens=16000)
            notes = _normalise_direction(d, intent, brief)
            review = self.llm.call(job_id, "direction_reviewer", {"BRIEF": _brief_for_model(brief), "INTENT": _public(intent),
                                                                   "DIRECTION": _public(d)}, media=refs, max_tokens=6000)
            if _blockers(review):
                ctx["INDEPENDENT_REVIEW"] = {"issues": review.get("issues"), "world_truth_blockers": truth_blockers(review)}
                ctx["NOTE"] = "An independent reviewer blocked this direction. Fix every blocker; keep what works."
                d = self.llm.call(job_id, "creative_director", ctx, knowledge=packs["payload"], media=refs + self._brief_docs(job_id),
                              max_tokens=16000)
                notes += _normalise_direction(d, intent, brief)
                review = self.llm.call(job_id, "direction_reviewer", {"BRIEF": _brief_for_model(brief), "INTENT": _public(intent),
                                                                       "DIRECTION": _public(d)}, media=refs, max_tokens=6000)
        trace = {"packs": packs["record"], "cited": d.get("canon_consulted", []), "deviations": d.get("deviations", []),
                 "deep_retrieved": [{"sk_id": c["sk_id"], "source_id": c["source_id"], "retrieved_by": "model_request"} for c in retrieved],
                 "knowledge_requests": d.get("knowledge_requests") or []}
        self.store.put_artifact(job_id, "canon_trace", trace, "system")
        d["_normalisation_notes"] = notes
        self.store.put_artifact(job_id, "direction", d, "creative_director")
        self.store.put_artifact(job_id, "direction_review", review, "direction_reviewer")
        still_blocked = _blockers(review)
        q = self.estimate(job_id, d, intent)
        self.store.put_artifact(job_id, "quote", q, "system")
        if not still_blocked:
            self._preview(job_id, d, intent)
        acct = self.store.account(self.store.job(job_id)["account_id"])
        cap = dec(brief.get("max_budget_usd") or 0)
        if still_blocked:
            # PRODUCT_AND_WORLD_TRUTH_BEFORE_SPEND: a direction the independent reviewer still blocks after the revision round
            # never reaches the customer's approve button; a person reads it and either redirects or overrides with a reason.
            why = "; ".join([i.get("issue", "") for i in review.get("issues", []) if i.get("severity") == "blocker"] + truth_blockers(review))
            self._pause(job_id, "directing", "paused_operator", f"independent review blocked the direction: {why[:600]}")
            return
        if acct["auto_approve"] and cap >= dec(q["recommended_budget_usd"]):
            self.approve(job_id, by="auto-approve (account setting)", budget_usd=cap)
            return
        self.store.transition(job_id, "directing", "awaiting_approval", actor="system")
        self.store.timing_start(job_id, "customer_wait", "approval")

    def estimate(self, job_id, d, intent) -> dict:
        media_kind = intent["deliverable"]["media"]
        lines = []
        if media_kind == "image":
            n = len(intent["deliverable"].get("formats") or ["1:1"])
            lines.append(("still images", n * 2, quote("nano-banana-2")))
        else:
            beats = [b for b in d["beats"] if b["first_frame"].strip().lower() != "end card"]
            lines.append(("character reference", 1 if (d.get("character") or {}).get("present") else 0, quote("nano-banana-2")))
            lines.append(("beat stills (with one re-draw allowance)", len(beats) * 2, quote("nano-banana-2")))
            for b in beats:
                c = clip_len(float(b["duration_s"]))
                lines.append((f"clip beat {b['n']} ({c}s, up to 2 takes)", 2, quote("veo-3.1-fast-i2v", duration_s=c)))
            lines.append(("music bed", 2, quote("lyria")))
        media_usd = sum(Decimal(n) * p for _, n, p in lines)
        reasoning_usd = Decimal("0") if self.s.reasoning_mode == "simulated" else Decimal("2.50")
        total = (media_usd + reasoning_usd).quantize(Decimal("0.01"))
        return {"lines": [{"item": a, "units": n, "unit_usd": str(p), "usd": str((Decimal(n) * p).quantize(Decimal('0.01')))} for a, n, p in lines],
                "media_ceiling_usd": str(media_usd.quantize(Decimal("0.01"))), "reasoning_allowance_usd": str(reasoning_usd),
                "recommended_budget_usd": str(total),
                "basis": "runtime PriceBook unit prices x planned draws incl. one re-draw/take allowance per asset; "
                         "reasoning allowance is an estimate until measured on live jobs"}

    def _preview(self, job_id, d, intent):
        """Preview stills the customer approves (they also become production assets when approved)."""
        guard = prompts.guard_for(intent, d, self.brief(job_id))
        refs = self._ref_images(job_id)
        media_kind = intent["deliverable"]["media"]
        aspect = (intent["deliverable"].get("formats") or ["9:16" if media_kind == "video" else "1:1"])[0]
        if media_kind == "video" and aspect not in ("9:16", "16:9"):
            aspect = "9:16"
        with self.store.timed(job_id, "asset_preparation", "preview"):
            if media_kind == "image":
                aid = self.dispatch.image(job_id, "preview", prompt=prompts.still_prompt(d, guard, aspect=aspect, with_product_ref=bool(refs),
                                                                                         with_character_ref=False),
                                          aspect=aspect, refs=refs, guard=guard, meta={"format": aspect, "preview": True})
            else:
                risky = _riskiest_beat(d)
                aid = self.dispatch.image(job_id, "preview", prompt=prompts.still_prompt(d, guard, beat=risky, aspect=aspect,
                                                                                         with_product_ref=bool(refs), with_character_ref=False),
                                          aspect=aspect, refs=refs[:2] if risky.get("product_present") else [], guard=guard,
                                          meta={"beat": risky["n"], "preview": True})
        self.store.set_asset(aid, role="preview")

    def approve(self, job_id, *, by: str, budget_usd, note: str = ""):
        job = self.store.job(job_id)
        review = self.store.artifact(job_id, "direction_review") or {}
        if _blockers(review) and not self.store.artifact(job_id, "direction_override"):
            raise PermissionError("the independent review blocked this direction; it cannot be approved until our team resolves it")
        acct = self.store.account(job["account_id"])
        budget = dec(budget_usd)
        if budget > dec(acct["ceiling_usd"]):
            raise PermissionError(f"USD {budget} is above the account ceiling USD {acct['ceiling_usd']}")
        committed = self.store.committed_usd(job_id)
        self._end_wait(job_id, "approval")
        self.store.transition(job_id, ("awaiting_approval", "directing"), "planning", actor=by,
                              data={"budget_usd": money(budget), "note": note, "direction_version": len(self.store.artifact_versions(job_id, "direction"))},
                              budget_usd=money(max(budget, committed)), budget_authorised_by=by, budget_authorised_at=utc_now(),
                              approved_at=utc_now())

    def select_take(self, job_id, *, asset_id: str, by: str, reason: str):
        """A person chose one of the inspected draws for a node that was waiting on a person; production resumes."""
        a = self.store.asset(asset_id)
        n = self.store.node(job_id, a["node_id"]) if a and a["job_id"] == job_id else None
        if n is None or n["status"] != "needs_person":
            raise ValueError("that take does not belong to a node waiting for a person")
        if len(reason.strip()) < 15:
            raise ValueError("say why this take is right (at least a sentence)")
        self.store.set_asset(asset_id, status="candidate")
        self._done(job_id, n["node_id"], asset_id)
        self.store.event(job_id, by, "take_selected_by_person", {"node": n["node_id"], "asset": asset_id, "reason": reason.strip()})
        if not [x for x in self.store.nodes(job_id) if x["status"] == "needs_person"] and self.store.job(job_id)["state"] == "paused_operator":
            self.store.transition(job_id, "paused_operator", "producing", actor=by, data={"take_selected": asset_id}, pause_reason=None)

    def override_direction(self, job_id, *, by: str, reason: str):
        """An operator read the blocked direction and releases it to the customer anyway — named and reasoned, never silent."""
        if len(reason.strip()) < 20:
            raise ValueError("an override needs a reason a colleague could audit (at least a sentence)")
        self.store.put_artifact(job_id, "direction_override", {"by": by, "reason": reason.strip(),
                                                               "blockers": truth_blockers(self.store.artifact(job_id, "direction_review") or {})}, by)
        if not self.store.assets(job_id, role="preview"):
            self._preview(job_id, self.store.artifact(job_id, "direction"), self.store.artifact(job_id, "intent"))
        self.store.transition(job_id, "paused_operator", "awaiting_approval", actor=by, data={"override": reason.strip()}, pause_reason=None)
        self.store.timing_start(job_id, "customer_wait", "approval")

    def request_direction_change(self, job_id, text: str, by: str):
        self.store.put_artifact(job_id, "concept_change", {"request": text, "by": by}, by)
        self._end_wait(job_id, "approval")
        self.store.transition(job_id, "awaiting_approval", "directing", actor=by, data={"change": text[:300]})

    # ── Stage 4: production selection → asset graph ────────────────────────────────────────────
    def plan(self, job_id):
        d, intent = self.store.artifact(job_id, "direction"), self.store.artifact(job_id, "intent")
        media_kind = intent["deliverable"]["media"]
        preview = [a for a in self.store.assets(job_id, role="preview")]
        with self.store.timed(job_id, "asset_preparation", "plan"):
            if media_kind == "image":
                for i, f in enumerate(intent["deliverable"].get("formats") or ["1:1"]):
                    reuse = next((a["id"] for a in preview if json.loads(a["meta_json"]).get("format") == f), None)
                    self.store.put_node(job_id, f"plate_{_fid(f)}", kind="plate", deps=[], spec={"aspect": f, "reuse": reuse})
                    self.store.put_node(job_id, f"ad_{_fid(f)}", kind="compose_still", deps=[f"plate_{_fid(f)}"], spec={"aspect": f})
            else:
                aspect = (intent["deliverable"].get("formats") or ["9:16"])[0]
                aspect = aspect if aspect in ("9:16", "16:9") else "9:16"
                beats = [b for b in d["beats"] if b["first_frame"].strip().lower() != "end card"]
                card = next((b for b in d["beats"] if b["first_frame"].strip().lower() == "end card"), {"duration_s": 3})
                risky = _riskiest_beat(d)
                char = (d.get("character") or {}).get("present")
                if char:
                    self.store.put_node(job_id, "character", kind="character", deps=[], spec={"aspect": aspect})
                for b in beats:
                    reuse = next((a["id"] for a in preview if json.loads(a["meta_json"]).get("beat") == b["n"]), None)
                    self.store.put_node(job_id, f"still_b{b['n']}", kind="still", deps=["character"] if char else [],
                                        spec={"beat": b["n"], "aspect": aspect, "reuse": reuse})
                    deps = [f"still_b{b['n']}"] + ([] if b["n"] == risky["n"] else [f"clip_b{risky['n']}"])
                    self.store.put_node(job_id, f"clip_b{b['n']}", kind="clip", deps=deps,
                                        spec={"beat": b["n"], "aspect": aspect, "qualify": b["n"] == risky["n"]})
                    if b.get("super_id"):
                        self.store.put_node(job_id, f"super_b{b['n']}", kind="super", deps=[f"clip_b{b['n']}"],
                                            spec={"beat": b["n"], "copy_id": b["super_id"], "aspect": aspect})
                self.store.put_node(job_id, "music", kind="music", deps=[], spec={})
                self.store.put_node(job_id, "end_card", kind="end_card", deps=[], spec={"aspect": aspect, "duration_s": card["duration_s"]})
                deps = [f"clip_b{b['n']}" for b in beats] + [f"super_b{b['n']}" for b in beats if b.get("super_id")] + ["music", "end_card"]
                self.store.put_node(job_id, "film", kind="assemble", deps=deps, spec={"aspect": aspect, "card_s": card["duration_s"]}, max_draws=1)
        self.store.event(job_id, "system", "plan", {"nodes": [n["node_id"] for n in self.store.nodes(job_id)]})
        self.store.transition(job_id, "planning", "producing", actor="system")

    # ── Stage 5: production (dependency-aware, concurrent) ─────────────────────────────────────
    def produce(self, job_id):
        for n in self.store.nodes(job_id):          # a node left running by a dead worker restarts cleanly
            if n["status"] == "running":
                self.store.set_node(job_id, n["node_id"], status="pending", note="restarted after interruption")
        ctx = self._ctx(job_id)
        with ThreadPoolExecutor(max_workers=max(1, self.s.worker_concurrency)) as pool:
            while True:
                nodes = {n["node_id"]: n for n in self.store.nodes(job_id)}
                if any(n["status"] == "failed" for n in nodes.values()):
                    bad = [k for k, n in nodes.items() if n["status"] == "failed"]
                    raise NodeFailed(f"production could not complete {bad}: " + "; ".join((nodes[k]["note"] or "")[:200] for k in bad))
                if all(n["status"] == "done" for n in nodes.values()):
                    break
                ready = [k for k, n in nodes.items() if n["status"] == "pending"
                         and all(nodes[d]["status"] == "done" for d in json.loads(n["deps_json"]) if d in nodes)]
                waiting = [k for k, n in nodes.items() if n["status"] == "needs_person"]
                if not ready and waiting:
                    self._pause(job_id, "producing", "paused_operator",
                                "a person picks a take for " + ", ".join(waiting) + " (the inspector rejected every draw and is not qualified to decide alone)")
                    return
                if not ready:
                    raise NodeFailed("no runnable node; states: " + json.dumps({k: n["status"] for k, n in nodes.items()}))
                futs = {pool.submit(self._run_node, job_id, k, ctx): k for k in ready if self.store.take_node(job_id, k)}
                errors = []
                for f in as_completed(futs):
                    try:
                        f.result()
                    except (BudgetExhausted, ProviderUnavailable) as e:
                        self.store.set_node(job_id, futs[f], status="pending", note=str(e)[:300])
                        errors.append(e)
                    except NeedsPerson as e:
                        self.store.set_node(job_id, futs[f], status="needs_person", note=json.dumps({"candidates": e.candidates, "why": e.why}))
                    except Exception as e:  # noqa: BLE001
                        self.store.set_node(job_id, futs[f], status="failed", note=scrub(str(e))[:500])
                if errors:
                    raise errors[0]
        film = self._final_assets(job_id)
        if not self.store.job(job_id)["first_cut_at"]:
            self.store.set_job(job_id, first_cut_at=utc_now())
        self.store.event(job_id, "system", "cut_ready", {"assets": film})
        self.store.transition(job_id, "producing", "checking", actor="system")

    def _ctx(self, job_id) -> dict:
        brief, intent, d = self.brief(job_id), self.store.artifact(job_id, "intent"), self.store.artifact(job_id, "direction")
        return {"brief": brief, "intent": intent, "d": d, "guard": prompts.guard_for(intent, d, brief), "refs": self._ref_images(job_id),
                "logo": self._logo(job_id), "beats": {b["n"]: b for b in d.get("beats", [])},
                "workdir": self.job_dir(job_id) / "work", "cut": self._cut(job_id)}

    def _cut(self, job_id) -> int:
        return 1 + len(self.store.artifact_versions(job_id, "revision_plan")) + len(self.store.artifact_versions(job_id, "internal_repair"))

    def exact_strings(self, job_id) -> list:
        """The customer's exact strings, with any change the customer later requested applied."""
        over = self.store.artifact(job_id, "copy_overrides") or {}
        return [over.get(s, s) for s in self.brief(job_id).get("exact_strings", [])]

    def _run_node(self, job_id, node_id, ctx):
        n = self.store.node(job_id, node_id)
        spec = json.loads(n["spec_json"])
        kind = n["kind"]
        ctx["workdir"].mkdir(parents=True, exist_ok=True)
        is_repair = bool(spec.get("revision_note"))
        if kind in ("plate", "still", "character"):
            return self._node_image(job_id, n, spec, ctx, is_repair)
        if kind == "clip":
            return self._node_clip(job_id, n, spec, ctx, is_repair)
        if kind == "music":
            aid = self._draw(job_id, n, lambda: self.dispatch.music(job_id, node_id, prompt=prompts.music_prompt(ctx["d"], ctx["guard"])[0],
                                                                    negative=prompts.music_prompt(ctx["d"], ctx["guard"])[1],
                                                                    guard=ctx["guard"], is_repair=is_repair))
            return self._done(job_id, node_id, aid)
        with self.store.timed(job_id, "composition", node_id):
            if kind == "compose_still":
                return self._node_compose_still(job_id, n, spec, ctx)
            if kind == "end_card":
                return self._node_end_card(job_id, n, spec, ctx)
            if kind == "super":
                return self._node_super(job_id, n, spec, ctx)
            if kind == "assemble":
                return self._node_assemble(job_id, n, spec, ctx)
        raise NodeFailed(f"unknown node kind {kind}")

    def _done(self, job_id, node_id, asset_id):
        if asset_id:
            self.store.set_asset(asset_id, status="selected")
        self.store.set_node(job_id, node_id, status="done", selected_asset_id=asset_id)

    def _draw(self, job_id, n, fn):
        """One paid draw. `max_draws` bounds quality draws (takes); transient provider failures do not use it up —
        they are retried up to TRANSIENT_RETRIES times in this run, then the job pauses as paused_provider."""
        node_id = n["node_id"]
        transient = 0
        while True:
            cur = self.store.node(job_id, node_id)
            if cur["draws"] >= cur["max_draws"]:
                raise NodeFailed(f"{node_id}: draw allowance ({cur['max_draws']}) used")
            self.store.set_node(job_id, node_id, draws=cur["draws"] + 1)
            try:
                return fn()
            except (BudgetExhausted, GuardRefused):
                self.store.set_node(job_id, node_id, draws=cur["draws"])      # nothing was sent: not a draw
                raise
            except DispatchFailed as e:
                self.store.event(job_id, "system", "provider_failure", {"node": node_id, "class": e.failure_class, "error": str(e)[:300]})
                if not e.retryable:
                    raise NodeFailed(f"{node_id}: {e}")
                self.store.set_node(job_id, node_id, draws=cur["draws"])      # an outage is not a bad draw
                transient += 1
                if transient >= TRANSIENT_RETRIES:
                    raise ProviderUnavailable(f"{node_id}: {e}")
                time.sleep(0 if self.s.provider_mode == "simulated" else 5 * transient)

    def _inspect(self, job_id, instruction: dict, media_items: list) -> dict:
        with self.store.timed(job_id, "independent_review", "inspection"):
            return self.llm.call(job_id, "inspector", {"INSTRUCTION": instruction,
                                                       "REFERENCE_NOTE": "The first image(s), when present, are the customer's product "
                                                                         "reference; the last item is the generated asset to inspect."},
                                 media=media_items, max_tokens=3000)

    def _node_image(self, job_id, n, spec, ctx, is_repair):
        node_id, d, guard, refs = n["node_id"], ctx["d"], ctx["guard"], ctx["refs"]
        if n["kind"] == "character":
            prompt, use_refs, aspect = prompts.character_prompt(d, guard, spec["aspect"]), [], spec["aspect"]
            instruction = {"asset": "character reference", "prompt": prompt}
        elif n["kind"] == "plate":
            aspect = spec["aspect"]
            prompt = prompts.still_prompt(d, guard, aspect=aspect, with_product_ref=bool(refs), with_character_ref=False)
            if spec.get("revision_note"):
                prompt = prompt.replace(prompts.NO_LETTERING, f"Change requested: {spec['revision_note']}. {prompts.NO_LETTERING}")
            use_refs = refs
            instruction = {"asset": "hero product picture (text is added later by code)", "prompt": prompt,
                           "must_show": [m["requirement"] for m in ctx["intent"].get("mandatory", []) if "text" not in m["requirement"].lower()],
                           "also_return": "product_box: the product's bounding box as fractions [x0,y0,x1,y1] in notes if visible"}
        else:
            beat = ctx["beats"][spec["beat"]]
            aspect = spec["aspect"]
            prompt = prompts.still_prompt(d, guard, beat=beat, aspect=aspect, with_product_ref=bool(refs) and beat.get("product_present"),
                                          with_character_ref=bool(self.store.node(job_id, "character")))
            if spec.get("revision_note"):
                prompt = prompt.replace(prompts.NO_LETTERING, f"Change requested: {spec['revision_note']}. {prompts.NO_LETTERING}")
            use_refs = (refs if beat.get("product_present") else [])[:2]
            ch = self.store.node(job_id, "character")
            if ch and ch["selected_asset_id"]:
                use_refs = use_refs + [("image/png", Path(self.store.asset(ch["selected_asset_id"])["path"]).read_bytes())]
            instruction = {"asset": f"first frame of beat {beat['n']}", "prompt": prompt, "first_frame": beat["first_frame"],
                           "product_present": beat.get("product_present"), "must_not": beat.get("must_not", [])}
        if spec.get("reuse") and not spec.get("revision_note") and self.store.asset(spec["reuse"]):
            aid = spec["reuse"]
            self.store.event(job_id, "system", "reuse", {"node": node_id, "asset": aid})
        else:
            aid = None
        while True:
            if aid is None:
                aid = self._draw(job_id, self.store.node(job_id, node_id),
                                 lambda: self.dispatch.image(job_id, node_id, prompt=prompt, aspect=aspect, refs=use_refs, guard=guard,
                                                             is_repair=is_repair, meta={"format": aspect, "beat": spec.get("beat")}))
            a = self.store.asset(aid)
            items = [(m, b) for m, b in (refs[:1] if n["kind"] != "character" else [])] + [(a["content_type"] or "image/png", Path(a["path"]).read_bytes())]
            verdict = self._inspect(job_id, instruction, items)
            meta = {**json.loads(a["meta_json"]), "inspection": _public(verdict), "product_box": _product_box(verdict)}
            self.store.set_asset(aid, meta_json=json.dumps(meta, default=str))
            ok = verdict.get("usable") and verdict.get("lettering_present") != "yes" and verdict.get("product_identity_ok") != "no"
            if ok:
                return self._done(job_id, node_id, aid)
            self.store.set_asset(aid, status="rejected")
            self.store.event(job_id, "system", "asset_rejected", {"node": node_id, "asset": aid, "why": verdict.get("notes", "")[:300]})
            cur = self.store.node(job_id, node_id)
            if cur["draws"] >= cur["max_draws"]:
                if not self.s.reviewer_qualified:
                    raise NeedsPerson(node_id, [x["id"] for x in self.store.assets(job_id, node_id=node_id) if x["status"] == "rejected"],
                                      verdict.get("notes", "")[:300])
                raise NodeFailed(f"{node_id}: no usable draw after {cur['draws']} (last: {verdict.get('notes', '')[:200]})")
            aid = None

    def _node_clip(self, job_id, n, spec, ctx, is_repair):
        node_id, d, guard = n["node_id"], ctx["d"], ctx["guard"]
        beat = ctx["beats"][spec["beat"]]
        still = self.store.asset(self.store.node(job_id, f"still_b{beat['n']}")["selected_asset_id"])
        use = float(beat["duration_s"])
        dur = clip_len(use)
        prompt = prompts.clip_prompt(d, guard, beat)
        if spec.get("revision_note"):
            prompt += f" Change requested: {spec['revision_note']}."
        negative = prompts.clip_negative(d, guard, beat, prompts.product_words(ctx["intent"]))
        instruction = {"asset": f"clip for beat {beat['n']} ({dur}s; {use}s will be used)", "action": beat["action"],
                       "end_state": beat["end_state"], "exit_action": beat.get("exit_action"), "must_not": beat.get("must_not", []),
                       "product_present": beat.get("product_present")}
        takes = []
        recovered = [x["id"] for x in self.store.assets(job_id, node_id=node_id, status="candidate")
                     if json.loads(x["meta_json"]).get("recovered")]
        while True:
            if recovered:              # a clip paid for before a crash and recovered by a resumed poll: use it, don't redraw
                aid = recovered.pop(0)
                self.store.event(job_id, "system", "recovered_take_used", {"node": node_id, "asset": aid})
            else:
                aid = None
            aid = aid or self._draw(job_id, self.store.node(job_id, node_id),
                             lambda: self.dispatch.video(job_id, node_id, prompt=prompt, image=(still["content_type"] or "image/png",
                                                                                                Path(still["path"]).read_bytes()),
                                                         duration_s=dur, aspect=spec["aspect"], negative=negative, guard=guard,
                                                         is_repair=is_repair, meta={"beat": beat["n"]}))
            a = self.store.asset(aid)
            det = self._clip_det(a, use)
            items = self._clip_media(a)
            verdict = self._inspect(job_id, instruction, items)
            seg = verdict.get("best_segment") or {}
            t_in = float(seg.get("in_s") or 0.0)
            if t_in + use > dur:
                t_in = max(0.0, dur - use)
            meta = {**json.loads(a["meta_json"]), "inspection": _public(verdict), "det": det, "in_s": t_in, "use_s": use}
            self.store.set_asset(aid, meta_json=json.dumps(meta, default=str))
            ok = (verdict.get("usable") and det["status"] != "FAIL" and verdict.get("required_action_occurred") not in ("no",)
                  and verdict.get("end_state_reached") != "no" and not verdict.get("prohibited_present"))
            takes.append((ok, aid, verdict, det))
            if ok:
                return self._done(job_id, node_id, aid)
            self.store.event(job_id, "system", "take_rejected", {"node": node_id, "asset": aid, "det": det["detail"],
                                                                 "why": verdict.get("notes", "")[:300]})
            cur = self.store.node(job_id, node_id)
            if cur["draws"] >= cur["max_draws"]:
                usable = [t for t in takes if t[2].get("usable") and t[3]["status"] != "FAIL"]
                if usable:                                  # TAKE_SELECTION_BEFORE_RETAKE: the best kept take, flagged
                    self.store.event(job_id, "system", "take_selected_with_flags", {"node": node_id, "asset": usable[0][1]})
                    return self._done(job_id, node_id, usable[0][1])
                if spec.get("qualify"):
                    raise NodeFailed(f"qualification failed on beat {beat['n']}: the route did not show the required action "
                                     f"({verdict.get('notes', '')[:200]}); a changed production method is needed")
                raise NodeFailed(f"{node_id}: no usable take after {cur['draws']} draws")

    def _clip_det(self, a, use) -> dict:
        if not media.have_ffmpeg():
            return {"check_id": "no_in_model_cut", "status": "NOT_VERIFIED", "detail": "ffmpeg not installed"}
        cuts = [t for t in media.scene_cuts(a["path"]) if 0.15 < t < use]
        return {"check_id": "no_in_model_cut", "status": "FAIL" if cuts else "PASS",
                "detail": f"in-model cut(s) at {cuts} inside the used {use}s" if cuts else f"no cut inside the used {use}s"}

    def _clip_media(self, a) -> list:
        if not media.have_ffmpeg():
            return []
        if self.s.reviewer_provider == "gemini":
            return [("video/mp4", Path(a["path"]).read_bytes())]
        d = probe_duration(a["path"])
        tmp = Path(a["path"]).with_suffix("")
        return [("image/png", media.frame_png(a["path"], d * k / 4 + 0.1, Path(f"{tmp}-f{k}.png")).read_bytes()) for k in range(4)]

    def _node_compose_still(self, job_id, n, spec, ctx):
        plate = self.store.asset(self.store.node(job_id, n["node_id"].replace("ad_", "plate_"))["selected_asset_id"])
        out = self.job_dir(job_id) / "out" / f"cut{ctx['cut']}-{_fid(spec['aspect'])}.png"
        if not media.have_ffmpeg():
            return self._placeholder_final(job_id, n, plate["path"], out, "image/png")
        pbox = json.loads(plate["meta_json"]).get("product_box")
        # Generated product colours drift (live 2026-09-23: navy 18 % darker than the real bag; the founder: "a little colour
        # off"). The product's dominant colours are matched to the customer's own photos, background untouched, and the
        # measured before/after distance is recorded on the delivered file.
        src_plate, colour_rows = Path(plate["path"]), []
        photos = [Path(u["path"]) for u in self.uploads(job_id, "product") if (u["content_type"] or "").startswith("image/")]
        if photos:
            matched = ctx["workdir"] / f"{Path(plate['path']).stem}-colour.png"
            cm = media.colour_match(src_plate, photos, matched)
            applied = {b: r for b, r in cm.items() if r.get("applied")}
            worst = max((r["distance_after"] for r in applied.values()), default=None)
            colour_rows.append({"check_id": "product_colour_match", "control": "PRODUCT_INTACT_AND_FAITHFUL",
                                "status": "PASS" if worst is not None and worst <= 8 else "FLAG", "blocking": False,
                                "detail": "; ".join(f"{b}: distance {r['distance_before']} -> {r['distance_after']} (reference {r['reference_rgb']})"
                                                    for b, r in applied.items()) or "no product colour band found on both",
                                "evidence": cm})
            src_plate = matched
        path, checks, layout = compose.still_ad(plate=src_plate, out=out, aspect=spec["aspect"], direction=ctx["d"],
                                                logo=ctx["logo"], workdir=ctx["workdir"], product_box_norm=pbox)
        checks = checks + colour_rows
        aid = self.store.add_asset(job_id, path=path, kind="image", source="composed", content_type="image/png", node_id=n["node_id"],
                                   role="deliverable", cut=ctx["cut"], meta={"format": spec["aspect"], "layout": layout, "plate": plate["id"]})
        verify.record_rows(self.store, job_id, aid, checks, runner="compositor_gates")
        return self._done(job_id, n["node_id"], aid)

    def _node_end_card(self, job_id, n, spec, ctx):
        size = media.FORMAT_PX[spec["aspect"]]
        out = ctx["workdir"] / f"endcard-cut{ctx['cut']}.png"
        if not media.have_ffmpeg():
            from runtime.loop.synthetic import make_png
            out.write_bytes(make_png(size[0] // 8, size[1] // 8, seed=7))
            aid = self.store.add_asset(job_id, path=out, kind="image", source="composed", content_type="image/png", node_id=n["node_id"], cut=ctx["cut"])
            return self._done(job_id, n["node_id"], aid)
        path, checks, layout = compose.end_card(out=out, size=size, direction=ctx["d"], logo=ctx["logo"], workdir=ctx["workdir"])
        aid = self.store.add_asset(job_id, path=path, kind="image", source="composed", content_type="image/png", node_id=n["node_id"],
                                   cut=ctx["cut"], meta={"layout": layout, "checks": checks})
        verify.record_rows(self.store, job_id, aid, checks, runner="compositor_gates")
        return self._done(job_id, n["node_id"], aid)

    def _node_super(self, job_id, n, spec, ctx):
        size = media.FORMAT_PX[spec["aspect"]]
        deck = {c["id"]: c["text"] for c in ctx["d"]["copy_deck"]}
        clip = self.store.asset(self.store.node(job_id, f"clip_b{spec['beat']}")["selected_asset_id"])
        cm = json.loads(clip["meta_json"])
        out = ctx["workdir"] / f"super-b{spec['beat']}-cut{ctx['cut']}.png"
        if not media.have_ffmpeg():
            from runtime.loop.synthetic import make_png
            out.write_bytes(make_png(8, 8, seed=3))
            aid = self.store.add_asset(job_id, path=out, kind="image", source="composed", content_type="image/png", node_id=n["node_id"], cut=ctx["cut"],
                                       meta={"checks": []})
            return self._done(job_id, n["node_id"], aid)
        path, checks = compose.super_overlay(out=out, size=size, text=deck.get(spec["copy_id"], ""), clip=Path(clip["path"]),
                                             clip_in=cm.get("in_s", 0.0), use=cm.get("use_s", 3.0), clip_size=size)
        aid = self.store.add_asset(job_id, path=path, kind="image", source="composed", content_type="image/png", node_id=n["node_id"],
                                   cut=ctx["cut"], meta={"checks": checks, "beat": spec["beat"], "rendered_text": [deck.get(spec["copy_id"], "")]})
        return self._done(job_id, n["node_id"], aid)

    def _node_assemble(self, job_id, n, spec, ctx):
        d = ctx["d"]
        beats = [b for b in d["beats"] if b["first_frame"].strip().lower() != "end card"]
        segs, t, supers, sources = [], 0.0, [], []
        for b in beats:
            clip = self.store.asset(self.store.node(job_id, f"clip_b{b['n']}")["selected_asset_id"])
            cm = json.loads(clip["meta_json"])
            segs.append({"clip": clip["path"], "in": cm.get("in_s", 0.0), "use": float(b["duration_s"]), "beat": b["n"], "asset": clip["id"]})
            sn = self.store.node(job_id, f"super_b{b['n']}")
            if sn:
                supers.append({"png": self.store.asset(sn["selected_asset_id"])["path"], "t_in": round(t + 0.2, 2),
                               "t_out": round(t + float(b["duration_s"]) - 0.1, 2), "beat": b["n"], "asset": sn["selected_asset_id"]})
            t += float(b["duration_s"])
        endcard = self.store.asset(self.store.node(job_id, "end_card")["selected_asset_id"])
        music = self.store.asset(self.store.node(job_id, "music")["selected_asset_id"])
        size = media.FORMAT_PX[spec["aspect"]]
        out = self.job_dir(job_id) / "out" / f"cut{ctx['cut']}-{_fid(spec['aspect'])}.mp4"
        if not media.have_ffmpeg():
            return self._placeholder_final(job_id, n, segs[0]["clip"], out, "video/mp4", extra={"segments": segs, "supers": supers})
        rep = media.assemble_film(segments=segs, endcard=Path(endcard["path"]), supers=supers, music=Path(music["path"]), out=out, size=size,
                                  card_s=float(spec["card_s"]), workdir=ctx["workdir"] / f"assemble-cut{ctx['cut']}")
        aid = self.store.add_asset(job_id, path=out, kind="video", source="composed", content_type="video/mp4", node_id=n["node_id"],
                                   role="deliverable", cut=ctx["cut"],
                                   meta={"segments": segs, "supers": supers, "assembly": rep, "end_card": endcard["id"], "music": music["id"]})
        # carry every component check onto the exact final file it contributed to
        rows = [dict(r, check_id="end_card:" + r["check_id"]) for r in json.loads(endcard["meta_json"]).get("checks", [])]
        for sp in supers:
            for r in json.loads(self.store.asset(sp["asset"])["meta_json"]).get("checks", []):
                rows.append(dict(r, check_id=f"super:b{sp['beat']}:{r['check_id']}"))
        cut_rows = [json.loads(self.store.asset(s["asset"])["meta_json"]).get("det", {}) for s in segs]
        worst = "FAIL" if any(r.get("status") == "FAIL" for r in cut_rows) else ("NOT_VERIFIED" if any(r.get("status") != "PASS" for r in cut_rows) else "PASS")
        rows.append({"check_id": "clips:no_in_model_cut", "control": "IN_MODEL_HARD_CUT", "status": worst,
                     "detail": "; ".join(f"b{s['beat']}: {r.get('detail')}" for s, r in zip(segs, cut_rows))})
        verify.record_rows(self.store, job_id, aid, rows, runner="compositor_gates+det")
        return self._done(job_id, n["node_id"], aid)

    def _placeholder_final(self, job_id, n, src, out, ctype, extra=None):
        """No media engine on this host: the final is a stand-in and every media check stays NOT_VERIFIED."""
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, out)
        with open(out, "ab") as fh:        # distinct bytes per cut, so versions are distinguishable
            fh.write(f"\n#cut-{n['node_id']}-{time.time()}".encode())
        aid = self.store.add_asset(job_id, path=out, kind="image" if ctype.startswith("image") else "video", source="composed",
                                   content_type=ctype, node_id=n["node_id"], role="deliverable", cut=self._cut(job_id),
                                   meta={"placeholder": True, "reason": "ffmpeg is not installed on this host", **(extra or {})})
        self.store.record_check(job_id, aid, check_id="media_engine", status="NOT_VERIFIED", blocking=True, runner="system",
                                detail="no media engine on this host: composition/assembly not performed; this file is a stand-in")
        return self._done(job_id, n["node_id"], aid)

    def _final_assets(self, job_id):
        return [n["selected_asset_id"] for n in self.store.nodes(job_id) if n["kind"] in ("compose_still", "assemble")]

    # ── check: deterministic + independent review → gateway ────────────────────────────────────
    def check(self, job_id):
        brief, intent, d = self.brief(job_id), self.store.artifact(job_id, "intent"), self.store.artifact(job_id, "direction")
        media_kind = intent["deliverable"]["media"]
        finals = self._final_assets(job_id)
        mandatory_ids = [m["id"] for m in intent.get("mandatory", [])]
        logo = self._logo(job_id)
        with self.store.timed(job_id, "deterministic_verification"):
            for aid in finals:
                a = self.store.asset(aid)
                meta = json.loads(a["meta_json"])
                rows = [verify.ledger_integrity(self.store, job_id),
                        verify.exact_copy_match(self.exact_strings(job_id), d, self._rendered_text(meta, media_kind)),
                        verify.not_previously_rejected(self.store, job_id, aid), verify.ad_structure(d, media_kind, bool(logo))]
                if media_kind == "video" and not meta.get("placeholder"):
                    srcs = []
                    for s in meta["segments"]:
                        try:
                            p = media.probe(s["clip"]); srcs.append([p["width"], p["height"]])
                        except media.MediaError:
                            pass
                    rep = meta["assembly"]
                    rows += verify.film_checks(Path(a["path"]), cuts=rep["cuts_s"], source_sizes=srcs,
                                               delivered=media.FORMAT_PX[json.loads(self.store.node(job_id, "film")["spec_json"])["aspect"]],
                                               planned_s=rep.get("duration_s"), card_in_s=rep.get("card_in_s"))
                if media_kind == "image" and not meta.get("placeholder"):
                    rows.append(verify.format_revalidated(self.store, aid, meta.get("format")))
                clips = [sg["asset"] for sg in meta.get("segments", [])]
                rows += verify.process_controls(self.store, job_id, media_kind, clip_asset_ids=clips)
                verify.record_rows(self.store, job_id, aid, rows, runner="deterministic")
        review_media = self._review_media(finals, media_kind)
        with self.store.timed(job_id, "independent_review", "final"):
            review = self.llm.call(job_id, "reviewer", {
                "BRIEF": _brief_for_model(brief), "INTENT": {"objective": intent["objective"], "audience": intent["audience"],
                                                             "audience_response": intent["audience_response"], "mandatory": intent["mandatory"],
                                                             "forbidden": intent["forbidden"]},
                "DIRECTION": {k: d.get(k) for k in ("proposition", "selected_concept", "audience_experience", "beats", "copy_deck", "composition")},
                "DETERMINISTIC_CHECKS": [{"check": r["check_id"], "status": r["status"]} for aid in finals for r in self.store.checks(aid)],
                "MEDIA_NOTE": ("The first image(s) are the customer's own product photos (reference, not the work); the rest is the "
                               "finished work. " if review_media.get("refs") else "") + review_media["note"]},
                media=review_media.get("refs", []) + review_media["items"], max_tokens=8000)
        review["_reviewed_sha256"] = review_media["shas"]
        self.store.put_artifact(job_id, "review", review, "reviewer")
        super_ids = [f"b{b['n']}" for b in d.get("beats", []) if b.get("super_id")]
        req = verify.required_checks(media_kind, mandatory_ids=mandatory_ids, has_copy=bool(d.get("copy_deck")), has_logo=bool(logo),
                                     super_ids=super_ids, has_character=bool((d.get("character") or {}).get("present")))
        results = []
        for aid in finals:
            verify.record_rows(self.store, job_id, aid, verify.review_rows(review, mandatory_ids=mandatory_ids, media_kind=media_kind,
                                                                           asset_sha256=self.store.asset(aid)["sha256"],
                                                                           qualified=self.s.reviewer_qualified),
                               runner=f"independent_review:{(review.get('_call') or {}).get('model')}")
            results.append(verify.gateway(self.store, job_id, aid, req))
        self.store.put_artifact(job_id, "gateway", {"results": results, "required": req}, "system")
        repairs = self.store.artifact_versions(job_id, "internal_repair")
        fixable = [x for x in review.get("defects", []) if x.get("severity") in ("blocker", "major") and x.get("beat")
                   and x.get("earliest_stage") in ("generation", "reference")]
        if fixable and len(repairs) < MAX_INTERNAL_REPAIRS and not review.get("_simulated"):
            targets = self._invalidate_beats(job_id, {int(x["beat"]): x["repair"] for x in fixable})
            self.store.put_artifact(job_id, "internal_repair", {"defects": fixable, "nodes": targets}, "system")
            self.store.transition(job_id, "checking", "producing", actor="system", data={"internal_repair": targets})
            return
        ready = all(r["ready"] for r in results)
        if ready and not self.s.hold_before_preview:
            self.store.transition(job_id, "checking", "ready_for_review", actor="system", presented_at=utc_now())
            self.store.timing_start(job_id, "customer_wait", "review")
        else:
            self.store.transition(job_id, "checking", "operator_hold", actor="system",
                                  data={"ready": ready, "blocking": [b["check_id"] for r in results for b in r["blocking"]][:40]})

    def _rendered_text(self, meta: dict, media_kind: str):
        """The strings drawn by code onto this final file (None when no render record exists)."""
        if meta.get("placeholder"):
            return None
        if media_kind == "image":
            return (meta.get("layout") or {}).get("rendered_text")
        card = json.loads(self.store.asset(meta["end_card"])["meta_json"]).get("layout", {}).get("rendered_text")
        if card is None:
            return None
        out = list(card)
        for sp in meta.get("supers", []):
            out += json.loads(self.store.asset(sp["asset"])["meta_json"]).get("rendered_text") or []
        return out

    def _review_media(self, finals, media_kind) -> dict:
        items, note, shas = [], "", []
        for aid in finals:
            a = self.store.asset(aid)
            if json.loads(a["meta_json"]).get("placeholder"):
                note += f"{aid}: stand-in file (no media engine on this host) — nothing to look at. "
                continue
            shas.append(a["sha256"])
            if media_kind == "image":
                items.append(("image/png", Path(a["path"]).read_bytes()))
                note += f"image {len(items)}: {json.loads(a['meta_json']).get('format')} at delivery size. "
            elif self.s.reviewer_provider == "gemini":
                small = Path(a["path"]).with_name(Path(a["path"]).stem + "-review.mp4")
                media.reencode_small(a["path"], small)
                items.append(("video/mp4", small.read_bytes()))
                note += "The attached MP4 is the complete assembled film with its sound (720p review copy). "
            else:
                sheet = media.contact_sheet(a["path"], Path(a["path"]).with_name("contact.png"))
                items.append(("image/png", sheet.read_bytes()))
                note += "Contact sheet at 2 fps; the audio could not be sent to this reviewer. "
        refs = []
        if finals:
            refs = list(self._ref_images(self.store.asset(finals[0])["job_id"], 4))   # every product photo: the open-pocket one was 3rd
        return {"items": items, "note": note or "no media", "shas": shas, "refs": refs}

    def _invalidate_beats(self, job_id, notes_by_beat: dict) -> list:
        changed = []
        for beat, note in notes_by_beat.items():
            node = self.store.node(job_id, f"clip_b{beat}")
            if not node:
                continue
            changed += self._reset(job_id, f"clip_b{beat}", note)
        return changed

    def _reset(self, job_id, node_id, note) -> list:
        """Mark a node and everything downstream of it pending; everything else is preserved."""
        nodes = {n["node_id"]: n for n in self.store.nodes(job_id)}
        todo, seen = [node_id], []
        while todo:
            k = todo.pop()
            if k in seen or k not in nodes:
                continue
            seen.append(k)
            todo += [m for m, n in nodes.items() if k in json.loads(n["deps_json"])]
        for k in seen:
            spec = json.loads(nodes[k]["spec_json"])
            if k == node_id:
                spec["revision_note"] = note
                spec.pop("reuse", None)
            self.store.set_node(job_id, k, status="pending", draws=0, spec_json=json.dumps(spec), note=f"reset by change to {node_id}")
        return seen

    # ── operator + customer decisions ──────────────────────────────────────────────────────────
    def release_hold(self, job_id, by: str):
        res = self.store.artifact(job_id, "gateway") or {"results": []}
        fresh = [verify.gateway(self.store, job_id, r["asset_id"], res.get("required", {})) for r in res["results"]]
        if not all(r["ready"] for r in fresh):
            raise PermissionError("the gateway still blocks: " + ", ".join(b["check_id"] for r in fresh for b in r["blocking"])
                                  + " — record a waiver with a reason for each, or fix them")
        self.store.put_artifact(job_id, "gateway", {"results": fresh, "required": res.get("required", {}), "released_by": by}, by)
        self.store.transition(job_id, "operator_hold", "ready_for_review", actor=by, presented_at=utc_now())
        self.store.timing_start(job_id, "customer_wait", "review")

    def accept(self, job_id, by: str):
        finals = self._final_assets(job_id)
        for aid in finals:
            g = verify.gateway(self.store, job_id, aid, (self.store.artifact(job_id, "gateway") or {}).get("required", {}))
            if not g["ready"]:
                raise PermissionError(f"{aid} is not presentable: {[b['check_id'] for b in g['blocking']]}")
            self.store.deliver(job_id, aid, by)
        self._end_wait(job_id, "review")
        self.store.transition(job_id, "ready_for_review", "accepted", actor=by, data={"delivered": finals},
                              closed_at=utc_now(), outcome="accepted")
        from product import learning
        learning.write_case(self.store, job_id)

    def reject(self, job_id, by: str, reason: str):
        for aid in self._final_assets(job_id):
            self.store.add_feedback(job_id, asset_id=aid, target=None, text=reason, kind="reject", by_user=by)
        self._end_wait(job_id, "review")
        self.store.transition(job_id, ("ready_for_review", "awaiting_approval", "needs_answers", "paused_budget", "failed"), "rejected",
                              actor=by, data={"reason": reason[:300]}, closed_at=utc_now(), outcome="rejected")
        from product import learning
        learning.write_case(self.store, job_id)

    def request_changes(self, job_id, by: str, items: list):
        """items: [{"target": "beat:3" | "copy:c1" | "music" | "whole" | None, "text": "..."}]"""
        finals = self._final_assets(job_id)
        for it in items:
            self.store.add_feedback(job_id, asset_id=finals[0] if finals else None, target=it.get("target"), text=it["text"],
                                    kind="revision", by_user=by)
        self._end_wait(job_id, "review")
        self.store.transition(job_id, "ready_for_review", "revising", actor=by, data={"items": len(items)})

    def revise(self, job_id):
        pending = [f for f in self.store.feedback(job_id) if f["kind"] == "revision" and not f["resolved_in_cut"]]
        d = self.store.artifact(job_id, "direction")
        intent = self.store.artifact(job_id, "intent")
        cut = self._cut(job_id) + 1
        plan = []
        with self.store.timed(job_id, "repair", "route"):
            for f in pending:
                r = self.llm.call(job_id, "revision_router", {"FEEDBACK": {"target": f["target"], "text": f["text"]},
                                                               "DIRECTION": {"beats": d.get("beats"), "copy_deck": d.get("copy_deck")},
                                                               "INTENT": {"mandatory": intent.get("mandatory")}}, max_tokens=4000)
                plan.append({"feedback_id": f["id"], **_public(r)})
        if any(p["class"] == "concept_change" for p in plan):
            self.store.put_artifact(job_id, "concept_change", {"request": [f["text"] for f in pending], "plan": plan}, "revision_router")
            self._mark_resolved(job_id, pending, cut)
            self.store.transition(job_id, "revising", "directing", actor="system", data={"reason": "concept change → new direction and quote"})
            return
        reset = []
        new_d = json.loads(json.dumps(d))
        overrides = dict(self.store.artifact(job_id, "copy_overrides") or {})
        for p in plan:
            for cc in p.get("copy_changes", []):
                for c in new_d["copy_deck"]:
                    if c["id"] == cc["id"]:
                        for orig in self.brief(job_id).get("exact_strings", []):
                            if overrides.get(orig, orig) == c["text"]:
                                overrides[orig] = cc["text"]
                        c["text"], c["source"] = cc["text"], "customer_exact"
                        reset += self._copy_nodes(job_id, c["id"])
            for t in p.get("targets", []):
                if t["kind"] == "copy":
                    reset += self._copy_nodes(job_id, t["ref"])
                elif t["kind"] == "music":
                    reset += self._reset(job_id, "music", t["change"])
                elif t["kind"] in ("beat", "still"):
                    ref = re.sub(r"\D", "", str(t["ref"]))
                    if self.store.node(job_id, f"still_b{ref}"):
                        reset += self._reset(job_id, f"still_b{ref}" if t["kind"] == "still" else f"clip_b{ref}", t["change"])
                    elif self.store.node(job_id, "plate_" + _fid((intent["deliverable"].get("formats") or ["1:1"])[0])):
                        for n in self.store.nodes(job_id):
                            if n["kind"] == "plate":
                                reset += self._reset(job_id, n["node_id"], t["change"])
                elif t["kind"] in ("edit", "composition"):
                    for n in self.store.nodes(job_id):
                        if n["kind"] in ("assemble", "compose_still"):
                            reset += self._reset(job_id, n["node_id"], t["change"])
        if new_d != d:
            self.store.put_artifact(job_id, "direction", new_d, "revision_router")
        if overrides:
            self.store.put_artifact(job_id, "copy_overrides", overrides, "customer")
        self.store.put_artifact(job_id, "revision_plan", {"cut": cut, "plan": plan, "reset_nodes": sorted(set(reset))}, "system")
        self._mark_resolved(job_id, pending, cut)
        if not reset:
            raise NodeFailed("the change request could not be mapped to any part of the production; an operator will review it")
        self.store.transition(job_id, "revising", "producing", actor="system", data={"reset": sorted(set(reset)), "cut": cut})

    def _copy_nodes(self, job_id, copy_id) -> list:
        out = []
        for n in self.store.nodes(job_id):
            spec = json.loads(n["spec_json"])
            if n["kind"] in ("compose_still", "end_card") or (n["kind"] == "super" and spec.get("copy_id") == copy_id):
                out += self._reset(job_id, n["node_id"], f"copy {copy_id} changed")
        return out

    def _mark_resolved(self, job_id, pending, cut):
        with self.store.tx() as c:
            for f in pending:
                c.execute("UPDATE feedback SET resolved_in_cut=? WHERE id=?", (cut, f["id"]))


# ── module helpers ─────────────────────────────────────────────────────────────────────────────
def _ts(utc: str) -> float:
    from datetime import datetime
    return datetime.strptime(utc, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=__import__("datetime").timezone.utc).timestamp()


def probe_duration(path) -> float:
    try:
        return media.probe(path)["duration_s"] or 4.0
    except media.MediaError:
        return 4.0


def _fid(fmt: str) -> str:
    return fmt.replace(":", "x")


def _public(d: dict) -> dict:
    return {k: v for k, v in d.items() if not k.startswith("_")}


truth_blockers = verify.truth_blockers


def _blockers(review) -> bool:
    return any(i.get("severity") == "blocker" for i in review.get("issues", [])) or bool(truth_blockers(review))


def _brief_for_model(brief: dict) -> dict:
    keep = ("text", "media", "formats", "duration_s", "exact_strings", "product", "brand_colours", "audience_hint", "market", "language",
            "references_note", "forbidden_words")
    return {k: brief[k] for k in keep if k in brief}


def _product_box(verdict: dict):
    m = re.search(r"\[\s*([01](?:\.\d+)?)\s*,\s*([01](?:\.\d+)?)\s*,\s*([01](?:\.\d+)?)\s*,\s*([01](?:\.\d+)?)\s*\]", verdict.get("notes", ""))
    return [float(x) for x in m.groups()] if m else None


def _riskiest_beat(d: dict) -> dict:
    beats = [b for b in d.get("beats", []) if b["first_frame"].strip().lower() != "end card"]
    if not beats:
        return {"n": 0, "product_present": True, "first_frame": "", "camera": ""}
    for r in d.get("risks", []):
        m = re.search(r"beat\s*(\d+)", r.get("where", ""), re.I)
        if m and int(m.group(1)) in {b["n"] for b in beats}:
            return next(b for b in beats if b["n"] == int(m.group(1)))
    return next((b for b in beats if b.get("product_present")), beats[0])


def _enforce_intent(intent: dict, brief: dict):
    """Deterministic floor under the model's reading: the customer's exact strings are always mandatory, and the
    media family is what the customer selected."""
    intent["deliverable"]["media"] = brief.get("media", intent["deliverable"]["media"])
    if brief.get("formats"):
        intent["deliverable"]["formats"] = brief["formats"]
    if brief.get("media") == "video" and brief.get("duration_s"):
        intent["deliverable"]["duration_s"] = float(brief["duration_s"])
    have = " ".join(m["requirement"] for m in intent.get("mandatory", []))
    for s in brief.get("exact_strings", []):
        if s and s not in have:
            intent["mandatory"].append({"id": f"M{len(intent['mandatory']) + 1}", "requirement": f'the exact text "{s}" appears, character for character',
                                        "source": "customer_stated", "observable_as": "rendered text equals the string"})


def _normalise_direction(d: dict, intent: dict, brief: dict) -> list:
    """Deterministic corrections, each recorded: exact strings present verbatim; beat lengths fit the clip grammar;
    total length equals the requested duration; an end card exists for films."""
    notes = []
    deck = d.setdefault("copy_deck", [])
    for s in brief.get("exact_strings", []):
        if s and s not in [c["text"] for c in deck]:
            deck.append({"id": f"c{len(deck) + 1}", "text": s, "role": "line", "source": "customer_exact"})
            notes.append(f"added the customer's exact string {s!r} to the copy deck (the director had omitted or altered it)")
    if intent["deliverable"]["media"] != "video":
        d["beats"] = []
        return notes
    beats = d.get("beats") or []
    if not any(b["first_frame"].strip().lower() == "end card" for b in beats):
        beats.append({"n": len(beats) + 1, "duration_s": 3.0, "purpose": "sign-off", "feeling": "resolved", "first_frame": "end card",
                      "action": "none", "end_state": "logo and line", "exit_action": None, "camera": "n/a", "product_present": False,
                      "product_state": "n/a", "continuity": [], "must_not": [], "super_id": None, "mandatory_ids": []})
        notes.append("added a 3 s end card beat")
    for b in beats:
        if b["first_frame"].strip().lower() != "end card" and float(b["duration_s"]) > 7.5:
            notes.append(f"beat {b['n']} shortened from {b['duration_s']}s to 7.5s (longest usable part of an 8 s clip)")
            b["duration_s"] = 7.5
        if float(b["duration_s"]) < 1.0:
            notes.append(f"beat {b['n']} lengthened to 1.0s")
            b["duration_s"] = 1.0
    target = float(intent["deliverable"].get("duration_s") or sum(float(b["duration_s"]) for b in beats))
    target = min(target, 30.0)
    total = sum(float(b["duration_s"]) for b in beats)
    if abs(total - target) > 0.25:
        body = [b for b in beats if b["first_frame"].strip().lower() != "end card"]
        card = sum(float(b["duration_s"]) for b in beats if b not in body)
        scale = (target - card) / max(0.1, sum(float(b["duration_s"]) for b in body))
        for b in body:
            b["duration_s"] = round(min(7.5, max(1.0, float(b["duration_s"]) * scale)), 2)
        notes.append(f"beat lengths scaled so the film runs {target:.1f}s (was {total:.1f}s)")
    for i, b in enumerate(beats, 1):
        b["n"] = i
    d["beats"] = beats
    return notes
