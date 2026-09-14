"""Reading a PRODUCTION-SPEC-v1 — the router's input, and the only thing it may match on.

The router reads a spec that another lane compiled. It validates the fields it is about to rely on
and fails loudly when one is missing, in the same spirit as the contract's own invariant ("a spec
compiles from a job with no human authoring step in between; if it cannot, it fails loudly").

It matches on `capability_requirements` and nothing else. It reads `route_exclusions` to forbid, and
that is the single, contract-declared exception to the rule that a spec never names a route.

ONE THING THE SPEC DOES NOT CARRY. PRODUCTION-SPEC-v1 copies the two budget numbers out of the
policy profile but not the profile's NAME, and every other limit the router needs — which evidence
statuses may auto-route, whether a fallback is required — lives only in the profile row. So the
profile has to be handed to the router alongside the spec. That is recorded on the decision as
`policy_profile_source: supplied_alongside_spec`, and it is reported upward rather than patched here:
this lane does not edit frozen contracts.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

import yaml

REQUIRED_TOP = ("spec_id", "job_id", "deliverable", "capability_requirements", "budget",
                "acceptance_contract", "gate_requirements", "deterministic_checks", "hard_constraints")


class SpecError(RuntimeError):
    pass


@dataclass(frozen=True)
class Requirement:
    capability: str
    level: str | None
    mandatory: bool


@dataclass(frozen=True)
class Exclusion:
    route_key: str
    reason: str
    basis: str


@dataclass
class Spec:
    path: Path
    data: dict

    def __post_init__(self):
        if self.data.get("schema") not in ("PRODUCTION-SPEC-v1",):
            raise SpecError(f"{self.path}: schema {self.data.get('schema')!r}; this router builds "
                            f"against PRODUCTION-SPEC-v1")
        missing = [k for k in REQUIRED_TOP if k not in self.data]
        if missing:
            raise SpecError(f"{self.path}: missing required field(s) {missing!r}")
        for k in ("cost_ceiling_usd", "max_provider_draws", "repair_allowance"):
            if k not in (self.data.get("budget") or {}):
                raise SpecError(f"{self.path}: budget.{k} is required and is read from the policy "
                                f"profile, never from code")

    # -- accessors -------------------------------------------------------------
    @property
    def spec_id(self) -> str:
        return str(self.data["spec_id"])

    @property
    def job_id(self) -> str:
        return str(self.data["job_id"])

    @property
    def objective(self) -> str:
        return str(self.data.get("objective") or "")

    @property
    def kind(self) -> str:
        return str(self.data["deliverable"]["kind"])

    @property
    def deliverable(self) -> dict:
        return dict(self.data["deliverable"])

    @property
    def hard_constraints(self) -> list:
        return list(self.data.get("hard_constraints") or [])

    @property
    def exact_text(self) -> dict:
        return dict(self.data.get("exact_text") or {})

    @property
    def cost_ceiling_usd(self) -> Decimal:
        return Decimal(str(self.data["budget"]["cost_ceiling_usd"]))

    @property
    def max_provider_draws(self) -> int:
        return int(self.data["budget"]["max_provider_draws"])

    @property
    def repair_allowance(self) -> int:
        return int(self.data["budget"]["repair_allowance"])

    def requirements(self) -> list[Requirement]:
        out = []
        for r in self.data["capability_requirements"]:
            if "capability" not in r:
                raise SpecError(f"{self.path}: a capability_requirement carries no capability")
            out.append(Requirement(capability=str(r["capability"]),
                                   level=(r.get("level") if r.get("level") is not None else None),
                                   mandatory=bool(r.get("mandatory", True))))
        return out

    def exclusions(self) -> list[Exclusion]:
        out = []
        for e in self.data.get("route_exclusions") or []:
            out.append(Exclusion(route_key=str(e["route_key"]), reason=str(e.get("reason") or ""),
                                 basis=str(e.get("basis") or "")))
        return out

    def billing_facts(self) -> dict:
        """The quantity facts one provider call is billed on, taken only from the spec.

        `duration_s` is the motion length the deliverable asks for. Nothing else is synthesised: a
        unit whose quantity is not answerable from the spec makes the route unpriceable, and an
        unpriceable route is never auto-selected.
        """
        params: dict = {}
        motion = (self.deliverable.get("motion") or {})
        if motion.get("seconds") is not None:
            params["duration_s"] = motion["seconds"]
        return {"params": params}


def load_spec(path: Path | str) -> Spec:
    p = Path(path)
    return Spec(path=p, data=yaml.safe_load(p.read_text(encoding="utf-8")))
