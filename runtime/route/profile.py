"""The active policy profile, read as data and failing closed.

Every operating limit the router obeys is a value in a row of POLICY-PROFILES.yaml. There is no
default hidden in this file: asking for a limit the named row does not carry raises
`MissingLimit`, because "a limit that is not in the named profile is not a limit the runtime may
invent" (POLICY-PROFILES invariant).

`adopted` is separate from every limit and is checked separately: a profile with `adopted: false`
may plan, price and dry-run a job and may never spend. That invariant was added to the contract after
the first lane found that nothing stopped a paid run under a merely proposed profile.

`spend_authority` is separate from `adopted` (Controller rider, 14 Sep 2026: adopting the Alpha
policy is NOT spend authorisation). `may_spend()` is the one place both are read together, and it
says which of the two is missing. It does not validate the record itself; a Wave-2 lane wires the
check that the named record exists and is signed.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

import yaml

ALL_KINDS_SENTINEL = "__all__"


class ProfileError(RuntimeError):
    pass


class MissingLimit(ProfileError):
    """The named profile row does not carry a limit the router needs. Refuse, never default."""


class UnknownProfile(ProfileError):
    pass


@dataclass
class PolicyProfile:
    name: str
    row: dict
    path: Path

    def limit(self, key: str):
        if key not in self.row:
            raise MissingLimit(
                f"policy profile {self.name!r} in {self.path} carries no {key!r}. The runtime refuses "
                f"rather than inventing one (POLICY-PROFILES invariant: missing limit = refuse).")
        return self.row[key]

    # Named accessors, so a typo is an error rather than a silent None.
    @property
    def adopted(self) -> bool:
        return bool(self.limit("adopted"))

    @property
    def status(self) -> str:
        return str(self.limit("status"))

    @property
    def deliverable_kinds_allowed(self) -> list:
        return list(self.limit("deliverable_kinds_allowed"))

    @property
    def max_provider_draws(self) -> int:
        return int(self.limit("max_provider_draws_per_deliverable"))

    @property
    def repair_allowance(self) -> int:
        return int(self.limit("repair_allowance"))

    @property
    def auto_routable_evidence_status(self) -> list:
        return list(self.limit("auto_routable_evidence_status"))

    @property
    def on_non_auto_routable(self) -> str:
        return str(self.limit("on_non_auto_routable"))

    @property
    def fallback_required(self) -> bool:
        return bool(self.limit("fallback_required"))

    @property
    def default_job_cost_ceiling_usd(self) -> Decimal:
        return Decimal(str(self.limit("default_job_cost_ceiling_usd")))

    @property
    def acceptance_authority(self) -> str:
        return str(self.limit("acceptance_authority"))

    @property
    def autonomous_external_delivery(self) -> bool:
        return bool(self.limit("autonomous_external_delivery"))

    @property
    def spend_authority(self) -> dict:
        value = self.limit("spend_authority")
        if not isinstance(value, dict):
            raise MissingLimit(
                f"policy profile {self.name!r} in {self.path} carries spend_authority but not as a "
                f"{{status, record, note}} block; the runtime refuses rather than guessing its shape.")
        return dict(value)

    @property
    def exact_text_strategies_allowed(self) -> list:
        return list(self.limit("exact_text_strategies_allowed"))

    @property
    def motion_requires_accepted_still(self) -> bool:
        return bool(self.limit("motion_requires_accepted_still"))

    def may_spend(self) -> tuple[bool, str]:
        """(True, why) only when the profile is adopted AND spend_authority.status is "signed" AND a
        record path is named. Otherwise (False, exactly what is missing). The record path is not
        opened or validated here — that check is wired by the execution bridge (Wave 2)."""
        return may_spend(self.name, self.adopted, self.spend_authority)

    def allows_kind(self, kind: str) -> bool:
        allowed = self.deliverable_kinds_allowed
        return ALL_KINDS_SENTINEL in allowed or kind in allowed


def may_spend(name: str, adopted: bool, spend_authority: dict) -> tuple[bool, str]:
    """The adoption-plus-spend-authority test, shared by both profile readers.

    Adoption is a policy agreement; spend authority is money. Both are needed; neither implies the
    other. The reason text names the exact missing piece so a refusal can be read without the file.
    """
    missing = []
    if not adopted:
        missing.append("adopted is false (the Controller has not agreed this profile's limits)")
    status = spend_authority.get("status")
    record = spend_authority.get("record")
    if status != "signed":
        missing.append(f"spend_authority.status is {status!r}, not 'signed' (adoption is not spend authorisation)")
    if not isinstance(record, str) or not record.strip():
        missing.append("spend_authority.record names no signed spend authorisation record")
    if missing:
        return False, f"profile {name!r} may plan, price and dry-run only: " + "; ".join(missing)
    return True, (f"profile {name!r} is adopted and names spend authorisation record {record!r}; "
                  f"whether that record exists and is signed is checked by the execution bridge, not here")


def load_profile(name: str, profiles_path: Path | str) -> PolicyProfile:
    path = Path(profiles_path)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    for row in data.get("profiles") or []:
        if row.get("profile") == name:
            return PolicyProfile(name=name, row=row, path=path)
    known = [r.get("profile") for r in (data.get("profiles") or [])]
    raise UnknownProfile(f"no policy profile {name!r} in {path}; rows are {known!r}")
