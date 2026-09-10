"""Turning a PRODUCTION-SPEC's capability requirements into an executable ROUTE-DECISION.

THE SELECTION ORDER IS FIXED AND VISIBLE

        hard requirements  ->  evidence status  ->  price  ->  cost  ->  fallback

    Every candidate carries the stage it was dropped at, so the order can be read off the decision
    rather than taken on trust. Cost only ORDERS the routes that survived the earlier stages. It can
    never rescue a route and never overrules a hard requirement — a cheaper route that fails a
    mandatory capability, that the spec excludes, or whose evidence is awaiting a ruling, is gone
    before any number is compared.

WHAT COUNTS AS A CANDIDATE

    A route, never a model name. The router matches the spec's `capability_requirements` against the
    binding (capability -> evidence question + arms), and a candidate is a route with an acceptable
    cell in EVERY mandatory requirement that will be dispatched — because those requirements are
    satisfied by one provider call, so one route has to satisfy all of them.

    A requirement the runtime satisfies with its own code (`dispatches: false` in the binding —
    setting exact strings onto a picture) is gated separately: no route is selected for it and
    nothing is priced, but the CELL its strategy rests on still has to pass the evidence gate. A
    blocked cell blocks the strategy even when no provider is called, because the strategy's only
    evidence is that cell.

NO IMPLICIT RETRY

    The decision declares a fallback before dispatch, with named triggers, and a fallback is a
    DIFFERENT route for the same requirement. There is no code path anywhere in this package that
    tries the same route twice.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from . import attempt_id as identity
from .evidence import EvidenceBase, GateResult
from .price import PriceBook, Quote
from .profile import PolicyProfile
from .spec import Exclusion, Requirement, Spec

STAGES = ("hard_requirements", "evidence_envelope", "price", "cost", "fallback")


class RouterRefusal(RuntimeError):
    """The router will not produce a decision at all (a limit is missing, an input is unreadable)."""


class CostEnvelopeExceeded(RouterRefusal):
    """already_committed + this_decision_max would cross the job ceiling. Checked before dispatch."""


class ExecuteRefused(RuntimeError):
    """`--execute` was asked for and the preconditions for spending are not met."""

    def __init__(self, reasons: list):
        self.reasons = list(reasons)
        super().__init__("; ".join(self.reasons))


@dataclass
class Candidate:
    route_key: str
    cells: dict = field(default_factory=dict)          # capability -> Cell
    kept: bool = True
    dropped_at: str | None = None
    why: list = field(default_factory=list)
    quote: Quote | None = None

    def drop(self, stage: str, why: str) -> None:
        if self.kept:
            self.kept = False
            self.dropped_at = stage
        self.why.append(why)

    def as_dict(self, floor: int) -> dict:
        d = {"route_key": self.route_key,
             "evidence_cells": sorted(c.cell_key for c in self.cells.values()),
             "kept": self.kept,
             "dropped_at": self.dropped_at,
             "why": self.why}
        if self.quote is not None:
            d["price"] = {"priced": self.quote.priced,
                          "expected_cost_usd": (str(self.quote.expected_cost_usd)
                                                if self.quote.expected_cost_usd is not None else None),
                          "why": self.quote.reason}
        return d


def _utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _decision_id(spec: Spec, profile: PolicyProfile, decided_utc: str) -> str:
    seed = f"{spec.spec_id}|{spec.job_id}|{profile.name}|{decided_utc}".encode("utf-8")
    return "rd-" + hashlib.sha256(seed).hexdigest()[:16]


class Router:
    """Plans a route decision. Opens nothing, sends nothing, writes nothing outside the caller."""

    def __init__(self, evidence: EvidenceBase, prices: PriceBook,
                 identities: identity.Identities | None = None):
        self.ev = evidence
        self.prices = prices
        self.identities = identities or identity.load_identities()

    # ---------------------------------------------------------------- planning
    def plan(self, spec: Spec, profile: PolicyProfile, *,
             already_committed_usd: Decimal | str | int = 0,
             customer_ref: str = "unknown-customer",
             decided_utc: str | None = None) -> dict:
        decided_utc = decided_utc or _utc()
        did = _decision_id(spec, profile, decided_utc)
        already = Decimal(str(already_committed_usd))
        binding = self.ev.binding
        auto_statuses = profile.auto_routable_evidence_status
        manual_reasons: list = []
        unsupported: list = []
        exclusions_applied: list = []
        notes_applied: list = []

        # -- stage 0: things that are true of the whole job before any route is looked at ----------
        preflight = []
        unknown_statuses = self.ev.profile_statuses_not_in_vocabulary(auto_statuses)
        if unknown_statuses:
            real = [s for s in auto_statuses if s not in unknown_statuses]
            consequence = (
                f"this profile auto-routes NOTHING — not one of the {len(self.ev.cells)} cells — "
                f"until the Controller names statuses that exist"
                if not real else
                f"those names match no cell; the profile effectively auto-routes on {real!r} alone")
            preflight.append(
                f"policy profile {profile.name!r} lists {unknown_statuses!r} as auto-routable and the "
                f"taint register's vocabulary is {self.ev.status_vocabulary!r}. The register says in "
                f"writing that it carries no launch-eligibility status and never will, so {consequence}.")
            if not real:
                manual_reasons.append(
                    f"profile {profile.name!r} names only evidence statuses the register does not "
                    f"carry ({unknown_statuses!r}), so nothing can be auto-routed under it. This is a "
                    f"profile configuration to settle, not a ruling to wait for.")
        if not profile.allows_kind(spec.kind):
            manual_reasons.append(
                f"deliverable kind {spec.kind!r} is not in {profile.name}.deliverable_kinds_allowed "
                f"{profile.deliverable_kinds_allowed!r}")
        if spec.max_provider_draws != profile.max_provider_draws:
            preflight.append(
                f"the spec's budget.max_provider_draws ({spec.max_provider_draws}) differs from the "
                f"profile row ({profile.max_provider_draws}); the profile is the authority and the "
                f"router uses it")

        # -- requirements -> questions -------------------------------------------------------------
        dispatching: list[tuple[Requirement, dict]] = []
        self_composed: list[tuple[Requirement, dict]] = []
        for req in spec.requirements():
            resolved = binding.resolve(req.capability, req.level)
            if not resolved.get("found"):
                unsupported.append({"capability": req.capability, "level": req.level,
                                    "mandatory": req.mandatory, "reason": resolved["reason"]})
                if req.mandatory:
                    manual_reasons.append(f"requirement {req.capability!r} is unsupported: {resolved['reason']}")
                continue
            (dispatching if resolved["dispatches"] else self_composed).append((req, resolved))

        excl = {e.route_key: e for e in spec.exclusions()}

        # -- requirements the runtime satisfies itself (no provider call, evidence still gated) -----
        strategy_evidence = []
        for req, res in self_composed:
            cells = self.ev.cells_for(res["question"], res["arms"])
            notes_applied.extend(self.ev.notes_touching(cells))
            chosen, why = None, []
            for cell in cells:
                g = self.ev.gate(cell, auto_statuses)
                if cell.route_key in excl:
                    e = excl[cell.route_key]
                    exclusions_applied.append(self._exclusion_row(e, cell, "hard_requirements"))
                    why.append(f"{cell.cell_key}: excluded by the spec ({e.basis}). Its evidence, had "
                               f"the exclusion not applied: {g.reason}")
                    continue
                why.append(f"{cell.cell_key}: {g.reason}")
                if g.allowed and chosen is None:
                    chosen = cell
            row = {"capability": req.capability, "level": res.get("level"),
                   "question": res["question"], "arms": res.get("arms"),
                   "dispatches": False, "basis": res.get("basis"),
                   "cells_considered": [c.cell_key for c in cells], "why": why,
                   "cell_selected": chosen.cell_key if chosen else None,
                   "evidence_status": chosen.evidence_status if chosen else None,
                   "expected_cost_usd": "0.000000",
                   "price_pin_ref": None,
                   "price_note": "composed by the runtime; no provider call, so no price pin applies"}
            strategy_evidence.append(row)
            if chosen is None:
                blockers = sorted({c.blocking_ruling for c in cells if c.blocking_ruling} |
                                  {c.blocking_open_question for c in cells if c.blocking_open_question})
                unsupported.append({"capability": req.capability, "level": res.get("level"),
                                    "mandatory": req.mandatory, "question": res["question"],
                                    "cells_considered": [c.cell_key for c in cells],
                                    "blocking": blockers,
                                    "reason": "no cell backing this strategy passes the evidence gate"})
                if req.mandatory:
                    manual_reasons.append(
                        f"requirement {req.capability!r} (level {res.get('level')!r}) rests on "
                        f"{res['question']} cells {[c.cell_key for c in cells]!r} and none of them may be "
                        f"used today" + (f"; blocking: {blockers}" if blockers else ""))

        # -- candidate discovery over the dispatching requirements ---------------------------------
        candidates: dict[str, Candidate] = {}
        per_requirement = []
        mandatory_dispatch = [(r, res) for r, res in dispatching if r.mandatory]
        optional_dispatch = [(r, res) for r, res in dispatching if not r.mandatory]

        if mandatory_dispatch:
            found: dict[str, dict] = {}
            for req, res in mandatory_dispatch:
                cells = self.ev.cells_for(res["question"], res["arms"])
                notes_applied.extend(self.ev.notes_touching(cells))
                per_requirement.append({"capability": req.capability, "level": res.get("level"),
                                        "question": res["question"], "arms": res.get("arms"),
                                        "dispatches": True, "basis": res.get("basis"),
                                        "cells_considered": [c.cell_key for c in cells]})
                for c in cells:
                    found.setdefault(c.route_key, {}).setdefault(req.capability, c)
            for rk, cellmap in sorted(found.items()):
                cand = Candidate(route_key=rk, cells=dict(cellmap))
                missing = [r.capability for r, _ in mandatory_dispatch if r.capability not in cellmap]
                if missing:
                    cand.drop("hard_requirements",
                              f"answers {sorted(cellmap)} but has no evidence cell for the mandatory "
                              f"requirement(s) {missing!r}; one provider call has to satisfy all of them")
                candidates[rk] = cand

        # -- stage 1: hard requirements (exclusions) ------------------------------------------------
        for rk, cand in candidates.items():
            if rk in excl and cand.kept:
                e = excl[rk]
                for cell in cand.cells.values():
                    exclusions_applied.append(self._exclusion_row(e, cell, "hard_requirements"))
                cand.drop("hard_requirements",
                          f"the spec excludes this route: {e.reason} (basis {e.basis}). An excluded "
                          f"route may be neither primary nor fallback, whatever it costs.")

        # -- stage 2: the evidence gate -------------------------------------------------------------
        for cand in candidates.values():
            if not cand.kept:
                continue
            for capability, cell in sorted(cand.cells.items()):
                g: GateResult = self.ev.gate(cell, auto_statuses)
                if g.allowed:
                    cand.why.append(f"{capability}: {g.reason}")
                else:
                    cand.drop("evidence_envelope", f"{capability}: {g.reason}")

        # -- stage 3: price -------------------------------------------------------------------------
        facts = spec.billing_facts()
        for cand in candidates.values():
            if not cand.kept:
                continue
            cand.quote = self.prices.quote(cand.route_key, facts)
            if not cand.quote.priced:
                cand.drop("price", f"no live price: {cand.quote.reason}. A route with no live price "
                                   f"pin is never auto-selected.")

        # -- stage 4: cost (orders survivors only) --------------------------------------------------
        survivors = [c for c in candidates.values() if c.kept]
        survivors.sort(key=lambda c: (c.quote.expected_cost_usd, c.quote.unit_price, c.route_key))

        primary = survivors[0] if survivors else None
        fallback = next((c for c in survivors[1:] if c.route_key != primary.route_key), None) if primary else None

        if primary is None and mandatory_dispatch:
            blockers = sorted({b for c in candidates.values() for b in self._blockers(c)})
            profile_only = sorted(c.route_key for c in candidates.values()
                                  if c.dropped_at == "evidence_envelope" and self._profile_blocked(c))
            manual_reasons.append(
                "no route satisfies every mandatory dispatching requirement under this profile"
                + (f"; blocking rulings: {blockers}" if blockers else "")
                + (f"; blocked only by this profile's auto_routable_evidence_status, not by the "
                   f"register: {profile_only}" if profile_only else ""))
        if primary is not None and fallback is None and profile.fallback_required:
            manual_reasons.append(
                f"profile {profile.name!r} sets fallback_required: true and no second eligible route "
                f"exists for this requirement, so there is nothing to hand over to. A second attempt "
                f"at {primary.route_key!r} is not a fallback.")

        # -- optional requirements are reported, never used to drop a route -------------------------
        for req, res in optional_dispatch:
            cells = self.ev.cells_for(res["question"], res["arms"])
            per_requirement.append({"capability": req.capability, "level": res.get("level"),
                                    "question": res["question"], "mandatory": False,
                                    "dispatches": True, "basis": res.get("basis"),
                                    "cells_considered": [c.cell_key for c in cells],
                                    "note": "not mandatory; recorded, never used to drop a route"})

        # -- cost envelope, checked before dispatch --------------------------------------------------
        draws = profile.max_provider_draws
        worst_unit = max([q for q in [primary.quote.expected_cost_usd if primary else None,
                                      fallback.quote.expected_cost_usd if fallback else None]
                          if q is not None] or [Decimal("0")])
        this_max = (worst_unit * Decimal(draws)).quantize(Decimal("0.000001"))
        ceiling = spec.cost_ceiling_usd
        within = (already + this_max) <= ceiling
        if not within:
            manual_reasons.append(
                f"cost_envelope_exceeded: already_committed {already} + this_decision_max {this_max} "
                f"exceeds the job ceiling {ceiling}. Checked before dispatch, not after.")

        manual = bool(manual_reasons)
        decision = {
            "schema": "ROUTE-DECISION-v0",
            "decision_id": did,
            "spec_id": spec.spec_id,
            "decided_utc": decided_utc,
            "selection_basis": {
                "required_capabilities": [r.capability for r in spec.requirements()],
                "rule": binding.selection_order.get("rule"),
                "stages": binding.selection_order.get("stages"),
                "requirements_resolved": per_requirement,
                "self_composed_requirements": strategy_evidence,
                "candidates_considered": [c.as_dict(self.ev.settled_draw_floor)
                                          for c in sorted(candidates.values(), key=lambda x: x.route_key)],
                "preflight": preflight,
                "register_notes_applied": self._dedupe_notes(notes_applied),
                "keyed_on": "cell_key, never (route_key, arm) — see NOTE-ROUTE-KEY-COLLISION",
            },
            "primary": self._slot(primary, spec, profile, did, customer_ref) if primary else None,
            "fallback": self._fallback_slot(fallback, binding) if fallback else None,
            "exclusions_applied": exclusions_applied,
            "unsupported_requirements": unsupported,
            "manual_route_required": manual,
            "manual_route_reason": ("; ".join(manual_reasons) if manual else None),
            "cost_envelope": {
                "job_ceiling_usd": str(ceiling),
                "already_committed_usd": str(already),
                "this_decision_max_usd": str(this_max),
                "basis": f"worst-case unit cost {worst_unit} x max_provider_draws_per_deliverable "
                         f"{draws} from profile {profile.name!r}",
                "within_ceiling": within,
            },
            "why_selected": self._why(primary, fallback, spec, profile, manual_reasons, preflight),
            "provenance": self._provenance(spec, profile),
        }
        return decision

    # ---------------------------------------------------------------- helpers
    def _blockers(self, cand: Candidate) -> list:
        out = []
        for cell in cand.cells.values():
            if cell.blocking_ruling:
                out.append(cell.blocking_ruling)
            if cell.blocking_open_question:
                out.append(cell.blocking_open_question)
        return out

    def _profile_blocked(self, cand: Candidate) -> bool:
        """True when the register would have allowed every cell and only the profile refused."""
        cells = list(cand.cells.values())
        return bool(cells) and all(c.production_use_allowed is True
                                   and c.evidence_status != "awaiting_controller_ruling"
                                   for c in cells)

    def _exclusion_row(self, e: Exclusion, cell, stage: str) -> dict:
        return {"route_key": e.route_key, "reason": e.reason, "basis": e.basis,
                "would_have_supplied": cell.cell_key, "question": cell.question,
                "applied_at_stage": stage,
                "effect": "neither primary nor fallback"}

    def _dedupe_notes(self, notes: list) -> list:
        seen, out = set(), []
        for n in notes:
            if n["id"] in seen:
                continue
            seen.add(n["id"])
            out.append(n)
        return out

    def _slot(self, cand: Candidate, spec: Spec, profile: PolicyProfile, did: str,
              customer_ref: str) -> dict:
        q = cand.quote
        cell_any = next(iter(cand.cells.values()))
        return {
            "route_key": cand.route_key,
            "surface": q.surface,
            "surface_model_id": q.surface_model_id,
            "arm": cell_any.arm,
            "evidence_cells": sorted(c.cell_key for c in cand.cells.values()),
            "evidence_status": "+".join(sorted({c.evidence_status for c in cand.cells.values()})),
            "evidence_n": {cap: cell.evidence_n(self.ev.settled_draw_floor)
                           for cap, cell in sorted(cand.cells.items())},
            "price_pin_ref": q.price_pin_ref,
            "price_pin_indexes": q.pin_indexes,
            "price_pin_evidence_quote": q.pin_evidence_quote,
            "unit_price": str(q.unit_price),
            "unit": q.unit,
            "unit_price_note": q.unit_price_note,
            "quantity": str(q.quantity),
            "quantity_unit": q.quantity_unit,
            "quantity_rule": q.quantity_rule,
            "expected_cost_usd": str(q.expected_cost_usd),
            "billing_pool": q.billing_pool,
            "credential_name": q.credential_name,
            "adapter_family": q.adapter,
            "attempt_ids_if_dispatched": self.identities.plan_attempt_ids(
                customer_ref=customer_ref, job_id=spec.job_id, decision_id=did,
                route_key=cand.route_key, draws=profile.max_provider_draws),
        }

    def _fallback_slot(self, cand: Candidate, binding) -> dict:
        q = cand.quote
        return {
            "route_key": cand.route_key,
            "surface": q.surface,
            "evidence_cells": sorted(c.cell_key for c in cand.cells.values()),
            "evidence_status": "+".join(sorted({c.evidence_status for c in cand.cells.values()})),
            "expected_cost_usd": str(q.expected_cost_usd),
            "price_pin_ref": q.price_pin_ref,
            "billing_pool": q.billing_pool,
            "trigger": binding.fallback_triggers,
            "note": "a different route for the same requirement, declared before dispatch. Falling "
                    "through to it is a routing event, never a retry.",
        }

    def _why(self, primary, fallback, spec: Spec, profile: PolicyProfile,
             manual_reasons: list, preflight: list) -> str:
        bits = [f"Spec {spec.spec_id} asks for {spec.kind}."]
        if primary:
            q = primary.quote
            bits.append(
                f"Among the routes that satisfy every mandatory requirement, are not excluded by the "
                f"spec, pass the taint register and carry a live price pin, {primary.route_key} is the "
                f"cheapest at {q.expected_cost_usd} USD "
                f"({q.unit_price} {q.unit} x {q.quantity} {q.quantity_unit}, pool {q.billing_pool}, "
                f"priced from {q.price_pin_ref}).")
            bits.append("Cost decided the order, never the eligibility: every route dropped above was "
                        "dropped before any price was compared.")
        else:
            bits.append("No route survived to be priced.")
        if fallback:
            bits.append(f"{fallback.route_key} is declared as the fallback at "
                        f"{fallback.quote.expected_cost_usd} USD, before any dispatch.")
        else:
            bits.append("No fallback is declared.")
        if profile.acceptance_authority != "none":
            bits.append(f"Acceptance authority under {profile.name} is {profile.acceptance_authority}.")
        for p in preflight:
            bits.append(p)
        if manual_reasons:
            bits.append("This decision requires a person: " + "; ".join(manual_reasons))
        return " ".join(bits)

    def _provenance(self, spec: Spec, profile: PolicyProfile) -> dict:
        p = dict(self.prices.provenance)
        p.update({
            "routing_evidence_map_sha256": self.ev.map_sha256,
            "taint_register": str(self.ev.register_path.relative_to(self.ev.root)),
            "taint_register_sha256": self.ev.register_sha256,
            "binding": str(self.ev.binding_path.relative_to(self.ev.root)),
            "policy_profile": profile.name,
            "policy_profile_status": profile.status,
            "policy_profile_adopted": profile.adopted,
            "policy_profile_source": "supplied_alongside_spec (PRODUCTION-SPEC-v1 carries no profile name)",
            "spec": str(spec.path),
            "evidence_status_vocabulary": self.ev.status_vocabulary,
            "dispatched": False,
            "network": "none — planning opens no socket",
        })
        return p

    # ---------------------------------------------------------------- execution
    def execute(self, spec: Spec, profile: PolicyProfile, *,
                request_cost_ceiling_usd: Decimal | str | None = None,
                already_committed_usd: Decimal | str | int = 0,
                customer_ref: str = "unknown-customer") -> dict:
        """Refuses unless a request-level ceiling AND an adopted profile are both present.

        Nothing beyond those checks is wired: there is no provider client in this package. The
        refusal is deliberately the first thing that happens, before a decision is even planned, so
        that no code path exists in which a non-adopted profile reaches a dispatch.
        """
        reasons = []
        if request_cost_ceiling_usd is None:
            reasons.append(
                "no request-level cost ceiling was supplied. A dispatch is only permitted under a "
                "ceiling checked before the call, on the reserve-then-settle discipline the Lab "
                "ledger uses (PRODUCTION-JOB-v1.cost_ceiling_usd).")
        if not profile.adopted:
            reasons.append(
                f"policy profile {profile.name!r} is {profile.status!r} with adopted: false. A "
                f"non-adopted input may plan and price, never spend (POLICY-PROFILES invariant). "
                f"alpha_human_release ships adopted: false, so execute refuses under it today.")
        if reasons:
            raise ExecuteRefused(reasons)

        decision = self.plan(spec, profile, already_committed_usd=already_committed_usd,
                             customer_ref=customer_ref)
        if decision["manual_route_required"]:
            raise ExecuteRefused([f"the route decision requires a person: {decision['manual_route_reason']}"])
        if not decision["cost_envelope"]["within_ceiling"]:
            raise CostEnvelopeExceeded(decision["cost_envelope"])
        raise ExecuteRefused([
            "no provider client is wired in this lane. The decision is complete and dispatchable, and "
            "dispatch itself is deliberately absent: this branch plans, prices and refuses."])
