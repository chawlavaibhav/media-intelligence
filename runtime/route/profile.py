"""The active policy profile, read as data and failing closed.

Every operating limit the router obeys is a value in a row of POLICY-PROFILES.yaml. There is no
default hidden in this file: asking for a limit the named row does not carry raises
`MissingLimit`, because "a limit that is not in the named profile is not a limit the runtime may
invent" (POLICY-PROFILES invariant).

`adopted` is separate from every limit and is checked separately: a profile with `adopted: false`
may plan, price and dry-run a job and may never spend. That invariant was added to the contract after
the first lane found that nothing stopped a paid run under a merely proposed profile.
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

    def allows_kind(self, kind: str) -> bool:
        allowed = self.deliverable_kinds_allowed
        return ALL_KINDS_SENTINEL in allowed or kind in allowed


def load_profile(name: str, profiles_path: Path | str) -> PolicyProfile:
    path = Path(profiles_path)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    for row in data.get("profiles") or []:
        if row.get("profile") == name:
            return PolicyProfile(name=name, row=row, path=path)
    known = [r.get("profile") for r in (data.get("profiles") or [])]
    raise UnknownProfile(f"no policy profile {name!r} in {path}; rows are {known!r}")
