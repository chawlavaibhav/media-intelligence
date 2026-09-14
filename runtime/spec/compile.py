"""PRODUCTION-JOB-v1 -> PRODUCTION-SPEC-v1. The heart of lane PC-03A, bridged to v1 by lane E.

A pure function of (job, Canon corpus, evidence map, policy profile) plus at most ONE reasoning
pass, and that pass sits behind a seam that never calls a model. Same inputs, same spec, byte for
byte — which is what makes the acceptance contract worth freezing.

Where the fields come from:

  deliverable, hard_constraints (the derived half)   the job
  exact_text.strategy / strategy_basis               ROUTING-EVIDENCE-MAP-v0, by rule
  exact_text.text_mechanism                          the strategy row's lettering_drawn_by, mapped by
                                                     FACET-CAPABILITIES (C-6c vocabulary)
  route_exclusions                                   the in-scope prohibitions the rule found, each
                                                     with a scope
  canon.*                                            the trigger table + the compiled packs
  capability_requirements                            DELIVERABLE-KINDS.yaml + FACET-CAPABILITIES
  gate_requirements                                  the injected packs' own CHECK ids
  acceptance_contract                                job-derived statements + the reasoning pass,
                                                     every one through the style guard
  policy_profile, budget                             the job's policy profile. Never a constant.
  objective, composition, materials_and_light,
  blueprint                                          the reasoning pass (a recorded fixture, a frozen
                                                     Stage-A blueprint, or lane H's template)

THE PROFILE LIMITS THIS MODULE ENFORCES (14 Sep 2026). `exact_text_strategies_allowed`: a strategy
the rule chose that the profile does not list is a refusal by name, carrying the profile's own
note as the basis — never a silent downgrade (POLICY-PROFILES invariant). `motion_requires_
accepted_still` is enforced at intake (runtime/intake/intake.py), before anything is compiled.

THE THREE KEYS BEYOND THE v1 CONTRACT. The router (runtime/route/spec.py) refuses a spec without
`schema: PRODUCTION-SPEC-v1`, and WAVE2-INTERFACES §1 requires `blueprint` and
`exact_text.text_mechanism`; the frozen v1 contract declares none of the three. Frozen contracts are
never edited in place and the router accepts only the v1 schema name, so a v2 file would not
connect the lanes either. The compiler validates the contract-declared part against v1 exactly as
before and then attaches the three interface keys (`INTERFACE_KEYS`, `EXACT_TEXT_INTERFACE_KEYS`);
`contract_view()` gives the contract-declared view back. Recorded in CHANGES-v0-to-v1.md as a v1
defect for the next contract version to close.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable

from .. import paths
from ..canon.normalize import KindBinding, normalize
from ..canon.packs import CanonCorpus
from ..contract_schema import Contract
from ..errors import Refusal
from ..evidence import EvidenceMap
from ..policy import PolicyProfiles
from ..registry import DeliverableKinds
from ..util import canonical_json, load_yaml, sha256_obj, sha256_text
from . import text_strategy as text_strategy_module
from .acceptance import StyleGuard, build as build_acceptance
from .blueprint_planner import BlueprintPlanner, STAGE_A_POOL
from .planner_seam import FixturePlanner, build_prompt

SPEC_SCHEMA = "PRODUCTION-SPEC-v1"
# Keys the spec carries beyond the frozen v1 contract's declared fields (see the module docstring).
INTERFACE_KEYS = ("schema", "blueprint", "waived_capabilities")
EXACT_TEXT_INTERFACE_KEYS = ("text_mechanism",)
# Prohibition scopes, PRODUCTION-SPEC-v1.route_exclusions[].scope (open vocabulary; today's values).
SCOPE_GENERATED_TEXT_ONLY = "generated_text_only"
SCOPE_WHOLE_ROUTE = "whole_route"
# The strategy the rule returns when the job names no exact string; no profile list bites on it
# (POLICY-PROFILES invariant: "the list governs a spec that carries exact-text strings").
NO_EXACT_TEXT = "no_exact_text"
# FACET-CAPABILITIES marker: a facet row whose level is this word takes the chosen strategy as its level.
LEVEL_IS_STRATEGY = "exact_text_strategy"


@dataclass(frozen=True)
class CompiledSpec:
    spec: dict
    canon_payload: str
    normalized_request: dict
    prompt_sha256: str
    text_strategy: object

    @property
    def spec_id(self) -> str:
        return self.spec["spec_id"]


def contract_view(spec: dict) -> dict:
    """The spec with the interface-only keys removed: exactly what PRODUCTION-SPEC-v1 declares."""
    out = {k: v for k, v in spec.items() if k not in INTERFACE_KEYS}
    if isinstance(out.get("exact_text"), dict):
        out["exact_text"] = {k: v for k, v in out["exact_text"].items() if k not in EXACT_TEXT_INTERFACE_KEYS}
    return out


def text_mechanism_for(lettering_drawn_by: str, facets_table: dict | None = None) -> str:
    """lettering_drawn_by (the lexicon row) -> C-6c mechanism name, from FACET-CAPABILITIES rows."""
    table = (facets_table if facets_table is not None else load_yaml(paths.FACET_CAPABILITIES) or {})
    rows = table.get("text_mechanism_by_lettering_drawn_by") or {}
    mechanism = rows.get(lettering_drawn_by)
    if not mechanism:
        raise Refusal(
            Refusal.TEXT_STRATEGY_UNDECIDABLE,
            f"no text_mechanism row for lettering_drawn_by {lettering_drawn_by!r}; the compiler does not "
            "invent a mechanism name (C-6c: the two mechanisms are different route identities)",
            lettering_drawn_by=lettering_drawn_by,
            table=str(paths.FACET_CAPABILITIES),
        )
    return str(mechanism)


class SpecCompiler:
    def __init__(
        self,
        profiles: PolicyProfiles | None = None,
        kinds: DeliverableKinds | None = None,
        corpus: CanonCorpus | None = None,
        evidence: EvidenceMap | None = None,
        binding: KindBinding | None = None,
        planner=None,
        guard: StyleGuard | None = None,
        contract: Contract | None = None,
        facet_capabilities_path=None,
        template_planner: Callable | None = None,
        freeze_root=None,
    ):
        self.profiles = profiles or PolicyProfiles()
        self.kinds = kinds or DeliverableKinds()
        self.corpus = corpus or CanonCorpus()
        self.evidence = evidence or EvidenceMap()
        self.binding = binding or KindBinding()
        self.planner = planner if planner is not None else FixturePlanner()
        # Lane H's hook: a callable with the planner protocol that returns None when it holds no
        # template for this job. Tried FIRST when provided; this module only defines the seam.
        self.template_planner = template_planner
        self.freeze_root = freeze_root
        self.guard = guard or StyleGuard(evidence=self.evidence)
        self.contract = contract or Contract.load(paths.SPEC_CONTRACT)
        self.facets = load_yaml(facet_capabilities_path or paths.FACET_CAPABILITIES) or {}

    # ------------------------------------------------------------------ compile
    def compile(self, job: dict, *, compiled_utc: str | None = None, provenance: dict | None = None) -> CompiledSpec:
        profile = self.profiles.checked_profile(job["policy_profile"])
        kind_row = self.kinds.get(job["deliverable_request"]["kind"])

        nr = normalize(job, self.binding)
        canon = self.corpus.inject(nr)
        strategy = text_strategy_module.choose(nr, self.evidence)
        self._refuse_on_strategy_outside_profile(strategy, profile, job)
        drawn_by = self.evidence.strategy_row(strategy.strategy).get("lettering_drawn_by") or "none"

        prompt = build_prompt(job, nr, canon, strategy)
        plan = self._plan(prompt, job, nr, provenance)

        job_sha = sha256_obj(job)
        spec = {
            "job_id": job["job_id"],
            "job_sha256": job_sha,
            "compiled_utc": compiled_utc or _utc_now(),
            "objective": plan["objective"],
            "deliverable": self._deliverable(job, plan),
            "hard_constraints": self._hard_constraints(job, nr, plan),
            "exact_text": {
                "strings": [dict(t) for t in nr.text_requirements],
                "strategy": strategy.strategy,
                "strategy_basis": strategy.strategy_basis,
            },
            "canon": {
                "packs_selected": canon.packs_selected(),
                "injected_context_sha256": canon.injected_context_sha256,
                "canon_gap": canon.canon_gap,
                # v1: a LIST of the doctrines no compiled pack answers (v0's single string lost which)
                "missing_domains": sorted(canon.gap_pack_ids),
            },
            "capability_requirements": self._capabilities(kind_row, nr, strategy),
            "route_exclusions": self._route_exclusions(strategy, drawn_by, nr),
            "gate_requirements": self._gate_requirements(canon, strategy, nr),
            "acceptance_contract": build_acceptance(job, nr, plan.get("acceptance_statements"), self.guard),
            "deterministic_checks": self._deterministic_checks(nr, strategy),
            "policy_profile": profile.name,
            "budget": {
                "cost_ceiling_usd": job["cost_ceiling_usd"],
                "max_provider_draws": profile.limit("max_provider_draws_per_deliverable"),
                "repair_allowance": profile.limit("repair_allowance"),
            },
        }
        identity = self._identity(nr)
        if identity:
            spec["identity_requirements"] = identity
        if plan.get("composition"):
            spec["composition"] = plan["composition"]
        if plan.get("materials_and_light"):
            spec["materials_and_light"] = plan["materials_and_light"]

        # the interface keys beyond the frozen v1 contract (module docstring)
        extension = {
            "schema": SPEC_SCHEMA,
            "blueprint": self._blueprint(plan),
            "waived_capabilities": list(self._waived),
            "text_mechanism": text_mechanism_for(drawn_by, self.facets),
        }
        # spec_id is a fingerprint of the spec's own content (interface keys included), so the same
        # job compiles to the same id on any machine, at any hour.
        fingerprinted = dict(spec, schema=extension["schema"], blueprint=extension["blueprint"],
                             exact_text=dict(spec["exact_text"], text_mechanism=extension["text_mechanism"]))
        spec["spec_id"] = "spec-" + sha256_text(
            canonical_json({k: v for k, v in sorted(fingerprinted.items()) if k != "compiled_utc"})
        )[:16]

        validated = self.contract.validate(spec)          # the contract-declared part, against v1
        validated["schema"] = extension["schema"]
        validated["exact_text"]["text_mechanism"] = extension["text_mechanism"]
        validated["blueprint"] = extension["blueprint"]
        return CompiledSpec(
            spec=validated,
            canon_payload=canon.payload,
            normalized_request=nr.as_dict(),
            prompt_sha256=prompt.sha256,
            text_strategy=strategy,
        )

    # ------------------------------------------------------------------ the reasoning pass
    def _plan(self, prompt, job: dict, nr, provenance: dict | None) -> dict:
        if self.template_planner is not None:
            plan = self.template_planner(prompt, job=job, nr=nr)
            if plan is not None:
                plan.setdefault("planner", "template:unnamed")
                return plan
        if provenance and provenance.get("source_pool") == STAGE_A_POOL:
            planner = BlueprintPlanner(self.freeze_root, provenance=provenance)
            return planner.plan(prompt, job=job, nr=nr)
        return self.planner.plan(prompt, job=job, nr=nr)

    @staticmethod
    def _blueprint(plan: dict) -> dict:
        """WAVE2-INTERFACES §1 spec["blueprint"], filled from the plan. A recorded fixture that carries
        no generation prompt yields an empty main prompt and says so through `planner`; nothing is
        invented to fill the gap."""
        prompts = dict(plan.get("generation_prompts") or {})
        return {
            "generation_prompts": {
                "main": str(prompts.get("main") or ""),
                "textless_plate": prompts.get("textless_plate") or None,
                "motion": prompts.get("motion") or None,
            },
            "planner": str(plan.get("planner") or "recorded_fixture"),
            "source_ref": str(plan.get("source_ref") or ""),
            "case_values": dict(plan.get("case_values") or {}),
            "production_parameters": dict(plan.get("production_parameters") or {}),
        }

    # ------------------------------------------------------------------ profile limit
    @staticmethod
    def _refuse_on_strategy_outside_profile(strategy, profile, job: dict) -> None:
        """POLICY-PROFILES exact_text_strategies_allowed, read through the profile object. A spec with no
        exact text names no strategy to check. Otherwise a strategy outside the list refuses by name,
        with the profile's own note as the basis (C-7 for alpha_human_release) — never a downgrade."""
        if strategy.strategy == NO_EXACT_TEXT:
            return
        allowed = profile.exact_text_strategies_allowed
        if strategy.strategy in allowed:
            return
        note = profile.row.get("exact_text_strategies_note")
        basis = " ".join(str(note).split()) if isinstance(note, str) and note.strip() else (
            f"policy profile {profile.name!r} lists exact_text_strategies_allowed {allowed!r} and carries "
            "no exact_text_strategies_note"
        )
        raise Refusal(
            Refusal.TEXT_STRATEGY_NOT_ALLOWED_BY_PROFILE,
            f"the evidence rule chose exact-text strategy {strategy.strategy!r} ({strategy.rule_id}) but "
            f"policy profile {profile.name!r} allows only {allowed!r}; refused by name, not downgraded. "
            f"Ruling basis: {basis}",
            job_id=job["job_id"],
            strategy=strategy.strategy,
            rule_id=strategy.rule_id,
            allowed=list(allowed),
            profile=profile.name,
            basis=basis,
        )

    # ------------------------------------------------------------------ field builders
    @staticmethod
    def _deliverable(job: dict, plan: dict) -> dict:
        request = job["deliverable_request"]
        out = {"kind": request["kind"], "aspect": request["aspect"]}
        if plan.get("resolution_class"):
            out["resolution_class"] = plan["resolution_class"]
        if request.get("motion"):
            out["motion"] = dict(request["motion"])   # carries v1 motion.depends_on when present
        return out

    @staticmethod
    def _hard_constraints(job: dict, nr, plan: dict) -> list:
        """Derived first — these are facts of the job and are not the reasoning pass's to soften."""
        derived = []
        for item in nr.text_requirements:
            if item["exactness"] == "contractual":
                derived.append(
                    f'the string {item["content"]!r} appears character-exact and is not re-flowed, '
                    "re-spelled or re-typeset"
                )
        derived.append(f'the deliverable is {job["deliverable_request"]["aspect"]}')
        count = job["deliverable_request"].get("count", 1)
        if count and count != 1:
            derived.append(f"{count} distinct deliverables are produced")
        if job["deliverable_request"].get("motion"):
            motion = job["deliverable_request"]["motion"]
            derived.append(f'the moving version runs {motion["seconds"]} seconds')
            if not motion.get("audio", False):
                derived.append("the moving version carries no audio track")
        stated = [" ".join(str(c).split()) for c in (plan.get("hard_constraints") or [])]
        out, seen = [], set()
        for item in derived + stated:
            if item in seen:
                continue
            seen.add(item)
            out.append(item)
        return out

    def _capabilities(self, kind_row, nr, strategy) -> list:
        rows = []
        conditions = self.facets.get("kind_capability_conditions") or {}
        self._waived = []
        for capability in kind_row.capability_requirements:
            facet = conditions.get(capability)
            if facet and not nr.facets.get(facet, False):
                # the kind demands it unconditionally; the fact it exists for is absent -> waived, on record
                self._waived.append({"capability": capability, "waived_because_facet_false": facet,
                                     "basis": "FACET-CAPABILITIES-v0 kind_capability_conditions"})
                continue
            rows.append({"capability": capability, "mandatory": True})
        for row in self.facets.get("facets", []):
            if not nr.facets.get(row["facet"], False):
                continue
            if row.get("modalities") and nr.modality not in row["modalities"]:
                continue
            for capability in row["capabilities"]:
                entry = {"capability": capability, "mandatory": bool(row.get("mandatory", True))}
                if row.get("level"):
                    # the marker row: the level IS the strategy the rule chose (see the YAML note)
                    entry["level"] = strategy.strategy if row["level"] == LEVEL_IS_STRATEGY else row["level"]
                rows.append(entry)
        if nr.temporal_structure:
            source = nr.temporal_structure.get("from") or "accepted_still"
            for capability in (self.facets.get("motion_from") or {}).get(source, []):
                rows.append({"capability": capability, "mandatory": True})
            if nr.temporal_structure.get("audio"):
                rows.append({"capability": "native_audio", "mandatory": True})
        merged: dict[str, dict] = {}
        for row in rows:
            key = row["capability"]
            if key in merged:
                merged[key]["mandatory"] = merged[key]["mandatory"] or row["mandatory"]
                if row.get("level"):
                    merged[key]["level"] = row["level"]
            else:
                merged[key] = dict(row)
        return [merged[k] for k in sorted(merged)]

    def _route_exclusions(self, strategy, drawn_by: str, nr) -> list:
        """Every in-scope prohibition that names routes, as PRODUCTION-SPEC-v1.route_exclusions rows.

        scope is `generated_text_only` when the prohibition is a LETTERING prohibition (its facets are
        all lettering facets: it forbids the route from DRAWING the text) and `whole_route` otherwise.
        The rows are written whatever the strategy: under code-set text the lettering rows still
        travel, so the router can see that the same route remains usable as a textless PLATE (RR-1)
        while forbidden from drawing the copy (RR-3). basis names the rule and the map cells for the
        route within this modality, so the row can be audited without re-deriving it."""
        rows = []
        for prohibition in strategy.prohibition_rows:
            scope = SCOPE_GENERATED_TEXT_ONLY if prohibition["lettering_prohibition"] else SCOPE_WHOLE_ROUTE
            for route in prohibition["routes"]:
                cells = self._cells_in_modality(route, nr.modality)
                rows.append({
                    "route_key": route,
                    "reason": " ".join(str(prohibition["because"]).split()),
                    "basis": f"{prohibition['rule_id']}; map cells: "
                             + (", ".join(cells) if cells else "none recorded for this modality"),
                    "scope": scope,
                })
        rows.sort(key=lambda r: (r["route_key"], r["basis"], r["scope"]))
        return rows

    def _cells_in_modality(self, route: str, modality: str) -> list:
        prefixes = [p for p, m in (self.evidence.lex.get("question_prefix_modality") or {}).items() if m == modality]
        return [c for c in self.evidence.cells_for_route(route) if any(c.startswith(p) for p in prefixes)]

    @staticmethod
    def _gate_requirements(canon, strategy, nr) -> list:
        """The packs' own CHECK lines, by id, plus the limits those packs carry."""
        out = list(canon.check_ids)
        for limit in canon.pack_limits:
            out.append(f"pack limit: {limit}")
        if canon.canon_gap:
            out.append(
                "canon gap: no compiled pack answers "
                f"{', '.join(sorted(canon.gap_pack_ids))}; the plan states this and attributes nothing to doctrine there"
            )
        return out

    def _deterministic_checks(self, nr, strategy) -> list:
        conditions = {
            "always": True,
            "exact_text_present": bool(nr.text_requirements),
            "not_exact_text_present": not nr.text_requirements,
            "motion_requested": bool(nr.temporal_structure),
            "lettering_set_by_code": self.evidence.strategy_row(strategy.strategy).get("lettering_drawn_by") == "code",
            "lettering_drawn_by_maker": self.evidence.strategy_row(strategy.strategy).get("lettering_drawn_by") == "maker",
        }
        return [
            row["check"]
            for row in self.facets.get("deterministic_checks", [])
            if conditions.get(row["when"], False)
        ]

    def _identity(self, nr) -> dict | None:
        roles = list(nr.facets.get("identity_bound_roles") or [])
        if not roles:
            return None
        return {"preserve": sorted(roles), "decoy_check": True}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
