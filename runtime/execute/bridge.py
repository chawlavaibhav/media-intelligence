"""ExecutionBridge: from a ROUTE-DECISION to the attempts it allows, rendered but never sent.

WHAT build() DOES

    Takes the spec, the decision the router made for it, the policy profile, and the prompt. Refuses
    to build attempts (manifest.blocked) when the decision needs a person, has no primary, lacks a
    fallback the profile requires, or does not fit the cost envelope. Otherwise it mints one attempt per
    draw the profile allows for the primary slot and the same for the fallback slot, and renders each
    through the Lab harness's OWN adapter (`adapter.dry_run()` from eval/harness-v2): the same code
    that builds the bytes a live call would send, reading no key and opening no socket. If the harness
    refuses an attempt - the body shape is unverified, an input is unresolved, a precondition is not met
    - the attempt is kept with `would_dispatch: false` and the harness's own reason, never patched.

WHAT run() DOES

    dispatch_mode dry: every attempt becomes `dry_not_sent`, settled 0, reserved 0, no artifact.
    dispatch_mode live: refuses, in this order - the profile's may_spend() (adoption plus a signed
    spend authority), then the signed record itself (runtime/execute/authorisation.py), then, because
    no transport exists in this tranche, "live dispatch is not wired". Every refusal names what is
    missing. No code path here constructs a transport.

POOLS (UPWORK-INTRO-001, SD-11; Controller audit on PR #98, blocker 3)

    Spend authority is not provider liquidity. build() accepts a PoolLiquidity of explicit balance READINGS
    (runtime/execute/pools.py); every attempt is marked funded / not_funded / unknown / not_read against its
    billing pool, drawn down in reservation order. Two answers are kept apart on every attempt:
      would_dispatch_if_funded  the pool-agnostic answer — harness shape verified, price agrees, within ceiling;
      would_dispatch            the real answer — the above AND liquidity positively known and funded.
    An attempt its pool cannot fund is `blocked_by_pool`; an attempt whose pool is unknown or unread is not
    dispatchable either (`pool_liquidity_unknown` in refusal_reason) — fail closed. Nothing is assumed
    funded. The bridge reads no balance itself.

MONEY

    The job ceiling comes from the spec's budget (and, when a request ceiling is also given, the lower of
    the two). Attempts reserve in the order they are listed - primary draws, then fallback draws - and
    the running total may never cross the ceiling; an attempt that would is `blocked_by_ceiling` and
    stays on the manifest so the shortfall is visible. Nothing is trimmed silently.

LEAD'S DESIGN DECISION, stated here because it shapes this file: `dry` is the dry twin of
alpha_human_release (same limits, dispatch_mode dry), so a dry manifest is built with exactly the
draws, fallback rule and ceiling a paid run would use. Reservations under dry are 0 by definition.
"""
from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from runtime.route import attempt_id as identity
from runtime.route.decision import ExecuteRefused
from runtime.route.evidence import EvidenceBase
from runtime.route.price import PriceBook, harness
from runtime.route.profile import PolicyProfile
from runtime.route.spec import Spec

from . import manifest as M
from .authorisation import AuthorisationRefused, check_live_authorisation
from .pools import PoolLiquidity

GCP_SURFACES = ("vertex", "gemini_api")
ZERO = "0"


class ExecutionBridge:
    """Builds and (dry-)runs execution manifests. Constructing one opens nothing."""

    def __init__(self, root: Path | str | None = None, *, evidence: EvidenceBase | None = None,
                 prices: PriceBook | None = None, identities: identity.Identities | None = None):
        self.ev = evidence or EvidenceBase(root=root)
        self.root = self.ev.root
        src = self.ev.binding.sources
        self.prices = prices or PriceBook(root=self.root, roster_path=self.root / src["roster"],
                                          pin_root=self.root / src["price_pin_root"])
        self.identities = identities or identity.load_identities()
        self._h = harness(self.root)
        self._harness_pricing = None
        self._adapters: dict = {}

    # ------------------------------------------------------------------ harness wiring
    def _pricing(self):
        """The harness's own Pricing over the same roster the router priced from (bound to the
        COST-TABLE's priced-against sha, as the harness insists). Built once, lazily."""
        if self._harness_pricing is None:
            pricing_mod = self._h["pricing"]
            self._harness_pricing = pricing_mod.Pricing(self.prices.roster_path, registry=self._h["surface_registry"])
        return self._harness_pricing

    def _adapter(self, route_key: str):
        if route_key not in self._adapters:
            from adapters import adapter_for          # eval/harness-v2 is on sys.path via harness()
            entry = self._h["surface_registry"].get(route_key)
            self._adapters[route_key] = (entry, adapter_for(entry, pricing=self._pricing()))
        return self._adapters[route_key]

    # ------------------------------------------------------------------ build
    def build(self, spec: Spec, decision: dict, profile: PolicyProfile, *, prompt_text: str,
              inputs: dict | None = None, customer_ref: str,
              request_ceiling_usd: Decimal | str | None = None, built_utc: str | None = None,
              pools: PoolLiquidity | None = None) -> dict:
        mode = str(profile.limit("dispatch_mode"))
        if mode not in M.DISPATCH_MODES:
            raise ExecuteRefused([f"policy profile {profile.name!r} carries dispatch_mode {mode!r}; the bridge "
                                  f"knows {list(M.DISPATCH_MODES)} and refuses to guess"])
        if not isinstance(prompt_text, str) or not prompt_text.strip():
            raise ExecuteRefused(["a prompt is part of the request and none was supplied; the bridge never "
                                  "invents one (the lead's CLI supplies spec.blueprint.generation_prompts.main)"])
        built_utc = built_utc or M.utc_now()
        mid = M.manifest_id(spec.job_id, decision["decision_id"], profile.name, built_utc)
        base = {
            "schema": M.SCHEMA, "manifest_id": mid, "job_id": spec.job_id, "spec_id": spec.spec_id,
            "decision_id": decision["decision_id"], "policy_profile": profile.name, "dispatch_mode": mode,
            "customer_ref": customer_ref, "built_utc": built_utc,
        }

        # -- refusals to build attempts: the manifest exists, blocked, with no attempts ---------------
        block = None
        if decision.get("manual_route_required"):
            block = M.blocked(M.BLOCKED_MANUAL, f"the route decision requires a person: {decision.get('manual_route_reason')}")
        elif not decision.get("primary"):
            block = M.blocked(M.BLOCKED_NO_PRIMARY, "the decision names no primary route; nothing can be attempted")
        elif profile.fallback_required and not decision.get("fallback"):
            block = M.blocked(M.BLOCKED_NO_FALLBACK,
                              f"profile {profile.name!r} requires a declared fallback and the decision has none")
        elif not (decision.get("cost_envelope") or {}).get("within_ceiling", False):
            block = M.blocked(M.BLOCKED_CEILING, f"the decision's cost envelope is not within the job ceiling: "
                                                 f"{decision.get('cost_envelope')}")
        if block is not None:
            return {**base, "blocked": block, "attempts": [], "fallback_triggers": [], "self_composed": [],
                    "surface_preference": None, "ceiling": None,
                    "pool_liquidity": self._pool_block(pools, [], set()),
                    "provenance": self._provenance(spec, decision, profile)}

        # -- the ceiling every attempt is checked against ---------------------------------------------
        job_ceiling = spec.cost_ceiling_usd
        request_ceiling = Decimal(str(request_ceiling_usd)) if request_ceiling_usd is not None else None
        effective = min(job_ceiling, request_ceiling) if request_ceiling is not None else job_ceiling
        already = Decimal(str((decision.get("cost_envelope") or {}).get("already_committed_usd") or "0"))

        # -- attempts: primary draws, then fallback draws, in reservation order ---------------------
        draws = profile.max_provider_draws
        text_mechanism = self._attempt_text_mechanism(spec)
        attempts: list[dict] = []
        running = already
        blocked_by_ceiling = 0
        pools_seen: set = set()
        for slot_name in ("primary", "fallback"):
            slot = decision.get(slot_name)
            if not slot:
                continue
            for draw in range(1, draws + 1):
                att, running, hit = self._attempt(spec, decision, profile, slot_name, slot, draw, prompt_text,
                                                  inputs or {}, customer_ref, mode, text_mechanism,
                                                  effective, running, pools)
                blocked_by_ceiling += int(hit)
                pools_seen.add(str(slot.get("billing_pool")))
                attempts.append(att)

        self_composed = [
            {"capability": r["capability"], "cell": r.get("cell_selected"), "text_mechanism": r.get("text_mechanism"),
             "note": r.get("price_note") or "composed by the runtime; no provider call"}
            for r in (decision.get("selection_basis") or {}).get("self_composed_requirements") or []]

        return {
            **base,
            "blocked": None,
            "attempts": attempts,
            "fallback_triggers": list((decision.get("fallback") or {}).get("trigger") or []),
            "self_composed": self_composed,
            "surface_preference": self._surface_preference(profile, decision["primary"]),
            "ceiling": {"job_ceiling_usd": str(job_ceiling),
                        "request_ceiling_usd": (str(request_ceiling) if request_ceiling is not None else None),
                        "effective_ceiling_usd": str(effective),
                        "already_committed_usd": str(already),
                        "reserved_total_usd": str(running),
                        "attempts_blocked_by_ceiling": blocked_by_ceiling,
                        "rule": "attempts reserve in listed order; the running total never crosses the effective "
                                "ceiling; an attempt that would is blocked_by_ceiling and stays visible"},
            "pool_liquidity": self._pool_block(pools, attempts, pools_seen),
            "provenance": self._provenance(spec, decision, profile),
        }

    # ------------------------------------------------------------------ pool liquidity
    @staticmethod
    def _pool_block(pools: PoolLiquidity | None, attempts: list, pools_seen: set) -> dict:
        rule = ("spend authority is not provider liquidity: an attempt whose billing pool cannot fund it is "
                "blocked_by_pool; an attempt whose pool is unknown or unread is not dispatchable either "
                "(would_dispatch false, pool_liquidity_unknown); would_dispatch_if_funded keeps the pool-agnostic answer")
        unknown = sum(1 for a in attempts
                      if a.get("pool_liquidity", {}).get("funded") is None
                      and (a.get("would_dispatch_if_funded") or a.get("if_triggered_would_dispatch_if_funded")))
        if pools is None:
            return {"status": "not_read", "readings": {}, "pools_without_reading": sorted(pools_seen),
                    "attempts_blocked_by_pool": 0, "attempts_not_dispatchable_unknown_liquidity": unknown, "rule": rule,
                    "note": "no PoolLiquidity was supplied to build(); no attempt is dispatchable until a reading funds it"}
        readings = {p: pools.reading(p) for p in pools.pools}
        missing = sorted(p for p in pools_seen if p not in readings or readings[p]["balance_usd"] is None)
        if not missing:
            status = "read"
        elif len(missing) < len(pools_seen):
            status = "partial"
        else:
            status = "unknown"
        return {"status": status, "readings": readings, "pools_without_reading": missing,
                "attempts_blocked_by_pool": sum(1 for a in attempts if a.get("blocked_by_pool")),
                "attempts_not_dispatchable_unknown_liquidity": unknown, "rule": rule}

    def _attempt(self, spec, decision, profile, slot_name, slot, draw, prompt_text, inputs, customer_ref,
                 mode, text_mechanism, ceiling, running, pools: PoolLiquidity | None = None) -> tuple[dict, Decimal, bool]:
        route_key = slot["route_key"]
        aid = self.identities.mint(customer_ref=customer_ref, job_id=spec.job_id,
                                   decision_id=decision["decision_id"], route_key=route_key, draw_index=draw)
        case_row = self.case_row(spec, decision, slot, prompt_text, draw)
        entry, adapter = self._adapter(route_key)
        dry = adapter.dry_run(case_row, inputs)

        reasons: list[str] = []
        if dry.get("refusal_reason"):
            reasons.append(f"harness: {dry['refusal_reason']}")
        expected = Decimal(str(slot["expected_cost_usd"]))
        harness_usd = (dry.get("price") or {}).get("amount_usd_equiv")
        price_agrees = harness_usd is not None and Decimal(str(harness_usd)) == expected
        if harness_usd is not None and not price_agrees:
            reasons.append(f"price disagreement: the router quoted {expected} USD and the harness dry_run priced "
                           f"{harness_usd} USD from the same roster; refusing rather than picking one")

        # Validate before reserving (production-learning RENTOK-GAME-B-005, att-016 / T1): an attempt the
        # harness has already refused — an unresolved input, an unverified body shape, a failed
        # precondition — can never leave the machine, so it reserves neither ceiling nor pool. Lane B's
        # dispatcher wrote a ledger reservation and then found the input file missing; here the same
        # ordering fault let a refused draw consume the pool and block a later, sendable one.
        harness_refused = bool(dry.get("refusal_reason"))
        within = (running + expected) <= ceiling
        reserved_here = within and not harness_refused
        hit = (not within) and not harness_refused
        if reserved_here:
            running = running + expected
        elif harness_refused:
            reasons.append("not_reserved: refused by the harness before any reservation; ceiling and pool untouched")
        else:
            reasons.append(f"blocked_by_ceiling: reserved so far {running} + this attempt {expected} exceeds the "
                           f"effective ceiling {ceiling}; nothing is trimmed to fit")

        pool = str(slot.get("billing_pool"))
        if pools is None:
            liquidity = {"pool": pool, "status": "not_read", "funded": None, "reason": "no pool readings supplied"}
        else:
            funded, why = pools.reserve(pool, expected) if reserved_here else pools.can_fund(pool, expected)
            liquidity = {"pool": pool, "status": ("funded" if funded else "not_funded" if funded is False else "unknown"),
                         "funded": funded, "reason": why}
        blocked_by_pool = liquidity["funded"] is False
        if blocked_by_pool:
            reasons.append(f"blocked_by_pool: {liquidity['reason']}; spend authority is not provider liquidity")
        elif liquidity["funded"] is None:
            reasons.append(f"pool_liquidity_unknown: {liquidity['reason']}; an attempt is dispatchable only when its "
                           "pool is positively known to fund it (would_dispatch_if_funded records the pool-agnostic answer)")

        if_funded = bool(dry.get("would_dispatch")) and price_agrees and within
        harness_would = if_funded and liquidity["funded"] is True
        att = {
            "attempt_id": aid,
            "slot": slot_name,
            "draw_index": draw,
            "route_key": route_key,
            "surface": entry.surface,
            "adapter_family": entry.adapter,
            "surface_model_id": entry.surface_model_id,
            "arm": slot.get("arm"),
            "request": {
                "method": dry.get("method"),
                "url": dry.get("url"),
                "body_sha256": dry.get("body_sha256"),
                "body": (dry.get("body") if mode == "dry" else None),
                "rendered_by": "harness adapter dry_run",
                "shape_status": dry.get("shape_status"),
                "api_calls_per_trial": dry.get("api_calls_per_trial"),
                "followups": dry.get("followups") or [],
                "request_notes": list(dry.get("request_notes") or []),
                "credential_name": entry.key_name,          # a NAME; the bridge never reads a key
            },
            "price": {
                "unit_price": slot.get("unit_price"), "unit": slot.get("unit"),
                "quantity": slot.get("quantity"), "quantity_unit": slot.get("quantity_unit"),
                "expected_cost_usd": str(expected), "billing_pool": slot.get("billing_pool"),
                "price_pin_ref": slot.get("price_pin_ref"), "pin_indexes": list(slot.get("price_pin_indexes") or []),
                "harness_amount_usd_equiv": (str(harness_usd) if harness_usd is not None else None),
                "price_agrees_with_harness": price_agrees,
            },
            "evidence": {"cells": list(slot.get("evidence_cells") or []), "status": slot.get("evidence_status"),
                         "text_mechanism": text_mechanism},
            "would_dispatch": harness_would if slot_name == "primary" else False,
            "would_dispatch_if_funded": if_funded if slot_name == "primary" else False,
            "refusal_reason": ("; ".join(reasons) if reasons else None),
            "ceiling": {"job_ceiling_usd": str(ceiling),
                        "reserved_before_this_usd": str(running - expected if reserved_here else running),
                        "this_attempt_usd": str(expected), "within": within},
            "blocked_by_ceiling": hit,
            "pool_liquidity": liquidity,
            "blocked_by_pool": blocked_by_pool,
        }
        if slot_name == "fallback":
            att["conditional_on"] = list(slot.get("trigger") or [])
            att["if_triggered_would_dispatch"] = harness_would
            att["if_triggered_would_dispatch_if_funded"] = if_funded
            att["conditional_note"] = ("a fallback attempt is dispatched only if a named trigger fires on the "
                                       "primary; never alongside it and never as a retry of it")
        return att, running, hit

    # ------------------------------------------------------------------ the case row the harness reads
    @staticmethod
    def case_row(spec: Spec, decision: dict, slot: dict, prompt_text: str, draw_index: int) -> dict:
        """The row shape eval/harness-v2 adapters read (casebook.rows()), built from the spec and the
        decision - nothing is taken from the Lab's TEST-CASES. `audio` is the harness's on/off string,
        translated from the spec's boolean; every other field is copied."""
        deliverable = spec.deliverable
        motion = deliverable.get("motion") or {}
        params: dict = {"aspect": deliverable.get("aspect")}
        if motion.get("seconds") is not None:
            params["duration_s"] = motion["seconds"]
        if motion.get("audio") is not None:
            params["audio"] = "on" if motion["audio"] else "off"
        return {
            "case_id": spec.job_id, "item_id": spec.spec_id, "route_key": slot["route_key"],
            "arm": slot.get("arm"), "params": params, "prompt": prompt_text, "repeat_index": draw_index,
            "tranche": "alpha", "billing_pool": slot.get("billing_pool"),
            "quantity": slot.get("quantity"), "unit_price": slot.get("unit_price"),
            "price_status": "pinned", "route_status": "pinned",
            "conditional": False, "reference_assets": [],
            "decision_id": decision.get("decision_id"),
        }

    @staticmethod
    def _attempt_text_mechanism(spec: Spec) -> str | None:
        """What the DISPATCHED attempt does about exact text (C-6c): the spec's declared mechanism;
        not_applicable when the job has no exact text; None (unknown) when the spec carries text but
        does not say - reported, never inferred."""
        if spec.text_mechanism is not None:
            return spec.text_mechanism
        return None if spec.has_text_requirement() else "not_applicable"

    # ------------------------------------------------------------------ surface preference
    def _surface_preference(self, profile: PolicyProfile, primary: dict) -> dict:
        """profile.surface_preference (same_model_prefers_gcp), applied only where the roster actually
        offers the primary's model on both fal and a GCP surface. Never invents a surface."""
        pref = dict(profile.limit("surface_preference") or {})
        rule = pref.get("rule")
        entry = self._h["surface_registry"].get(primary["route_key"])
        offered = []
        roster = self.prices.roster                       # the harness's own reader; public record() only
        for variant, label in ((None, "route"), ("fallback", "fallback")):
            try:
                rec = roster.record(entry.roster_key, variant)
            except Exception:                              # noqa: BLE001 - no fallback record is not an error
                continue
            if rec.get("surface"):
                offered.append({"surface": rec["surface"], "route_status": rec.get("route_status"), "record": label})
        out = {"rule": rule, "basis": pref.get("basis"), "primary_surface": entry.surface,
               "roster_surfaces_for_model": offered, "applied": False, "reason": None}
        if rule != "same_model_prefers_gcp":
            out["reason"] = f"rule {rule!r} is not one the bridge implements; recorded, not applied"
            return out
        surfaces = {o["surface"] for o in offered}
        gcp = sorted(s for s in surfaces if s in GCP_SURFACES)
        if len(surfaces) <= 1:
            out["reason"] = "roster carries one surface per route_key; nothing to prefer between"
        elif "fal" in surfaces and gcp:
            if entry.surface in GCP_SURFACES:
                out["applied"] = True
                out["reason"] = f"the model is offered on fal and on {gcp}; the harness registry renders it on {entry.surface}"
            else:
                out["reason"] = (f"the roster offers this model on fal and on {gcp}, but the harness registry exposes "
                                 f"one surface per route_key ({entry.surface}); the bridge refuses to invent an adapter "
                                 f"for the other - this is a registry change to request, not a runtime guess")
        else:
            out["reason"] = (f"the roster offers this model on {sorted(surfaces)}; neither pair is fal + GCP, so the "
                             f"rule does not bite")
        return out

    # ------------------------------------------------------------------ provenance
    def _provenance(self, spec: Spec, decision: dict, profile: PolicyProfile) -> dict:
        ok, why = profile.may_spend()
        return {
            "spec_sha256": M.sha256_of(spec.data),
            "spec_path": str(spec.path),
            "decision_sha256": M.sha256_of(decision),
            "routing_evidence_map_sha256": self.ev.map_sha256,
            "taint_register_sha256": self.ev.register_sha256,
            "roster_sha256": self.prices.roster.sha256,
            "policy_profile": profile.name,
            "policy_profile_adopted": profile.adopted,
            "spend_authority_status": profile.spend_authority.get("status"),
            "may_spend": ok,
            "may_spend_reason": why,
            "harness_modules": list(self.prices.provenance.get("harness_modules") or []),
            "harness_providers_stubbed": self._h.get("providers_stubbed"),
            "dispatched": False,
            "network": "none",
        }

    # ------------------------------------------------------------------ run
    def run(self, manifest: dict, profile: PolicyProfile) -> dict:
        mode = manifest.get("dispatch_mode")
        prof_mode = str(profile.limit("dispatch_mode"))
        if mode != prof_mode:
            raise ExecuteRefused([f"the manifest was built for dispatch_mode {mode!r} and the profile handed to run() "
                                  f"says {prof_mode!r}; refusing to run one under the other"])
        if manifest.get("policy_profile") != profile.name:
            raise ExecuteRefused([f"the manifest was built under profile {manifest.get('policy_profile')!r}, not "
                                  f"{profile.name!r}"])
        if manifest.get("blocked"):
            return {"status": "refused", "manifest_id": manifest["manifest_id"], "dispatch_mode": mode,
                    "refusal": manifest["blocked"], "attempts": [], "dispatched": False, "network": "none"}
        if mode == "dry":
            return {
                "status": "dry_complete", "manifest_id": manifest["manifest_id"], "dispatch_mode": "dry",
                "attempts": [{"attempt_id": a["attempt_id"], "status": M.ATTEMPT_DRY_NOT_SENT,
                              "would_dispatch": a["would_dispatch"], "refusal_reason": a["refusal_reason"],
                              "artifact_sha256": None, "settled_usd": ZERO, "reserved_usd": ZERO}
                             for a in manifest["attempts"]],
                "settled_total_usd": ZERO, "reserved_total_usd": ZERO,
                "dispatched": False, "network": "none",
                "note": "dry mode: every attempt was rendered and priced through the harness adapter's dry_run(); "
                        "nothing was sent and nothing was reserved",
            }
        # live
        routes = sorted({a["route_key"] for a in manifest["attempts"]})
        ceiling = Decimal(str((manifest.get("ceiling") or {}).get("effective_ceiling_usd") or "0"))
        try:
            check_live_authorisation(profile, self.root, job_ceiling_usd=ceiling, routes=routes)
        except AuthorisationRefused as exc:
            raise ExecuteRefused(["live dispatch refused before any transport was considered: " + r
                                  for r in exc.reasons]) from None
        raise ExecuteRefused([
            "live dispatch is not wired in this tranche: the profile is adopted and its signed spend "
            "authorisation record parsed, and still nothing is sent, because no provider transport exists "
            "in runtime/execute and none will be constructed here. Plain statement, not a bug."])
