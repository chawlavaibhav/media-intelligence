"""Policy profiles: every operating limit the runtime obeys, read as data.

No limit is a constant in this package. A limit the named profile does not carry is a
refusal, never a silently-applied default.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .. import paths
from ..errors import Refusal
from ..util import load_yaml

_MISSING = object()


@dataclass(frozen=True)
class PolicyProfile:
    name: str
    row: dict
    source: str

    def limit(self, limit_name: str) -> Any:
        """Read a limit. Absent (or null) is a refusal, by name."""
        value = self.row.get(limit_name, _MISSING)
        if value is _MISSING or value is None:
            raise Refusal(
                Refusal.POLICY_LIMIT_MISSING,
                f"policy profile {self.name!r} does not carry the limit {limit_name!r}; "
                "the runtime may not invent one",
                profile=self.name,
                limit=limit_name,
                source=self.source,
            )
        return value

    def has(self, limit_name: str) -> bool:
        return self.row.get(limit_name) is not None


class PolicyProfiles:
    """The rows of POLICY-PROFILES-v0, plus this lane's declared limit needs."""

    def __init__(self, profiles_path: str | Path | None = None, required_limits_path: str | Path | None = None):
        self.profiles_path = str(profiles_path or paths.POLICY_PROFILES)
        self.required_limits_path = str(required_limits_path or paths.REQUIRED_LIMITS)
        doc = load_yaml(self.profiles_path) or {}
        self._rows = {row["profile"]: row for row in doc.get("profiles", [])}
        self._needs = load_yaml(self.required_limits_path) or {}

    @property
    def required_at_intake(self) -> list[str]:
        return list(self._needs.get("required_at_intake", []))

    @property
    def allow_all_token(self) -> str:
        token = self._needs.get("allow_all_token")
        if not token:
            raise Refusal(
                Refusal.POLICY_LIMIT_MISSING,
                "REQUIRED-LIMITS-v0 does not declare allow_all_token",
                source=self.required_limits_path,
            )
        return token

    def job_field_default_limit(self, job_field: str) -> str | None:
        return (self._needs.get("job_field_defaults") or {}).get(job_field)

    def names(self) -> list[str]:
        return sorted(self._rows)

    def profile(self, name: str) -> PolicyProfile:
        row = self._rows.get(name)
        if row is None:
            raise Refusal(
                Refusal.POLICY_PROFILE_UNKNOWN,
                f"no policy profile named {name!r}",
                profile=name,
                known=self.names(),
                source=self.profiles_path,
            )
        return PolicyProfile(name=name, row=row, source=self.profiles_path)

    def checked_profile(self, name: str) -> PolicyProfile:
        """The profile, with every limit this lane will need proven present first."""
        profile = self.profile(name)
        for limit_name in self.required_at_intake:
            profile.limit(limit_name)  # raises POLICY_LIMIT_MISSING
        return profile
