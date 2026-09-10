"""PRODUCTION-JOB-v0 -> PRODUCTION-SPEC-v0. The heart of lane PC-03A.

A pure function of (job, Canon corpus, evidence map, policy profile) plus at most ONE reasoning
pass, and that pass sits behind a seam that runs from a fixture. Same inputs, same spec, byte for
byte — which is what makes the acceptance contract worth freezing.

Where the fields come from:

  deliverable, hard_constraints (the derived half)   the job
  exact_text.strategy / strategy_basis               ROUTING-EVIDENCE-MAP-v0, by rule
  canon.*                                            the trigger table + the compiled packs
  capability_requirements                            DELIVERABLE-KINDS.yaml + FACET-CAPABILITIES
  gate_requirements                                  the injected packs' own CHECK ids
  acceptance_contract                                job-derived statements + the reasoning pass,
                                                     every one through the style guard
  budget                                             the job's policy profile. Never a constant.
  objective, composition, materials_and_light        the reasoning pass
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

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
from .planner_seam import FixturePlanner, build_prompt


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
    ):
        self.profiles = profiles or PolicyProfiles()
        self.kinds = kinds or DeliverableKinds()
        self.corpus = corpus or CanonCorpus()
        self.evidence = evidence or EvidenceMap()
        self.binding = binding or KindBinding()
        self.planner = planner if planner is not None else FixturePlanner()
        self.guard = guard or StyleGuard(evidence=self.evidence)
        self.contract = contract or Contract.load(paths.SPEC_CONTRACT)
        self.facets = load_yaml(facet_capabilities_path or paths.FACET_CAPABILITIES) or {}

    # ------------------------------------------------------------------ compile
    def compile(self, job: dict, *, compiled_utc: str | None = None) -> CompiledSpec:
        profile = self.profiles.checked_profile(job["policy_profile"])
        kind_row = self.kinds.get(job["deliverable_request"]["kind"])

        nr = normalize(job, self.binding)
        canon = self.corpus.inject(nr)
        strategy = text_strategy_module.choose(nr, self.evidence)

        prompt = build_prompt(job, nr, canon, strategy)
        plan = self.planner.plan(prompt)

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
                **({"missing_domain": canon.missing_domain} if canon.missing_domain else {}),
            },
            "capability_requirements": self._capabilities(kind_row, nr),
            "gate_requirements": self._gate_requirements(canon, strategy, nr),
            "acceptance_contract": build_acceptance(job, nr, plan.get("acceptance_statements"), self.guard),
            "deterministic_checks": self._deterministic_checks(nr, strategy),
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

        # spec_id is a fingerprint of the spec's own content, so the same job compiles to the
        # same id on any machine, at any hour.
        spec["spec_id"] = "spec-" + sha256_text(
            canonical_json({k: v for k, v in sorted(spec.items()) if k != "compiled_utc"})
        )[:16]

        validated = self.contract.validate(spec)
        return CompiledSpec(
            spec=validated,
            canon_payload=canon.payload,
            normalized_request=nr.as_dict(),
            prompt_sha256=prompt.sha256,
            text_strategy=strategy,
        )

    # ------------------------------------------------------------------ field builders
    @staticmethod
    def _deliverable(job: dict, plan: dict) -> dict:
        request = job["deliverable_request"]
        out = {"kind": request["kind"], "aspect": request["aspect"]}
        if plan.get("resolution_class"):
            out["resolution_class"] = plan["resolution_class"]
        if request.get("motion"):
            out["motion"] = dict(request["motion"])
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

    def _capabilities(self, kind_row, nr) -> list:
        rows = []
        for capability in kind_row.capability_requirements:
            rows.append({"capability": capability, "mandatory": True})
        for row in self.facets.get("facets", []):
            if not nr.facets.get(row["facet"], False):
                continue
            for capability in row["capabilities"]:
                entry = {"capability": capability, "mandatory": bool(row.get("mandatory", True))}
                if row.get("level"):
                    entry["level"] = row["level"]
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

    @staticmethod
    def _gate_requirements(canon, strategy, nr) -> list:
        """The packs' own CHECK lines, by id, plus the limits those packs carry."""
        out = list(canon.check_ids)
        for limit in canon.pack_limits:
            out.append(f"pack limit: {limit}")
        if canon.canon_gap:
            out.append(
                "canon gap: no compiled pack answers "
                f"{canon.missing_domain}; the plan states this and attributes nothing to doctrine there"
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
