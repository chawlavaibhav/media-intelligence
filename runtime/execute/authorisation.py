"""The signed runtime spend authorisation a LIVE dispatch would need. None exists on this branch.

Adopting a policy profile is not spend authorisation (Controller rider, 14 Sep 2026). A live dispatch
needs, in addition to `adopted: true`, a record named in the profile's `spend_authority.record` that
exists on disk and parses as a signed authorisation: `authorised: true`, a non-empty `approved_by`, an
`approved_at`, a `job_ceiling_usd`, the `profile` it was signed for, and the `routes_allowed`. Every
profile row today says `status: none, record: null`, so this module refuses; it is written so that the
refusal names exactly which of those things is missing rather than saying "no".

Reading the record opens a file, never a socket, and never a key.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from pathlib import Path

import yaml

REQUIRED_FIELDS = ("authorised", "approved_by", "approved_at", "job_ceiling_usd", "profile", "routes_allowed")


class AuthorisationRefused(RuntimeError):
    """No usable signed runtime spend authorisation. `reasons` says what is missing."""

    def __init__(self, reasons: list):
        self.reasons = list(reasons)
        super().__init__("; ".join(self.reasons))


@dataclass(frozen=True)
class RuntimeSpendAuthorisation:
    path: Path
    authorised: bool
    approved_by: str
    approved_at: str
    job_ceiling_usd: Decimal
    profile: str
    routes_allowed: tuple = field(default_factory=tuple)

    def as_dict(self) -> dict:
        return {"path": str(self.path), "authorised": self.authorised, "approved_by": self.approved_by,
                "approved_at": self.approved_at, "job_ceiling_usd": str(self.job_ceiling_usd),
                "profile": self.profile, "routes_allowed": list(self.routes_allowed)}


def load_authorisation(record: str | Path | None, root: Path | None = None) -> RuntimeSpendAuthorisation:
    """Parse the record the profile names. Raises AuthorisationRefused naming every defect found."""
    reasons: list[str] = []
    if not isinstance(record, str) or not record.strip():
        raise AuthorisationRefused(["spend_authority.record names no signed spend authorisation record"])
    path = Path(record)
    if not path.is_absolute() and root is not None:
        path = Path(root) / path
    if not path.exists():
        raise AuthorisationRefused([f"spend authorisation record {record!r} does not exist on disk"])
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:                       # noqa: BLE001 - reported, not raised bare
        raise AuthorisationRefused([f"spend authorisation record {record!r} is not readable YAML: {exc}"])
    if not isinstance(data, dict):
        raise AuthorisationRefused([f"spend authorisation record {record!r} is not a mapping"])
    for key in REQUIRED_FIELDS:
        if key not in data:
            reasons.append(f"record lacks {key!r}")
    if reasons:
        raise AuthorisationRefused(reasons)
    if data["authorised"] is not True:
        reasons.append(f"record says authorised: {data['authorised']!r}, not true")
    if not isinstance(data["approved_by"], str) or not data["approved_by"].strip():
        reasons.append("record names no approver (approved_by is empty)")
    if not str(data["approved_at"] or "").strip():
        reasons.append("record carries no approved_at")
    try:
        ceiling = Decimal(str(data["job_ceiling_usd"]))
    except (InvalidOperation, TypeError):
        ceiling = None
        reasons.append(f"record job_ceiling_usd {data['job_ceiling_usd']!r} is not a number")
    if not isinstance(data["routes_allowed"], list) or not data["routes_allowed"]:
        reasons.append("record allows no routes (routes_allowed is empty)")
    if reasons:
        raise AuthorisationRefused(reasons)
    return RuntimeSpendAuthorisation(path=path, authorised=True, approved_by=str(data["approved_by"]),
                                     approved_at=str(data["approved_at"]), job_ceiling_usd=ceiling,
                                     profile=str(data["profile"]),
                                     routes_allowed=tuple(str(r) for r in data["routes_allowed"]))


def check_live_authorisation(profile, root: Path | None, *, job_ceiling_usd: Decimal,
                             routes: list) -> RuntimeSpendAuthorisation:
    """Everything a live dispatch needs before a transport could even be considered.

    Order: the profile's own may_spend() (adopted + spend_authority signed + record named), then the
    record itself, then that the record was signed for THIS profile, covers THIS job's ceiling and
    names every route the manifest would call. The first failing layer is reported with its reason.
    """
    ok, why = profile.may_spend()
    if not ok:
        raise AuthorisationRefused([f"spend_authority: {why}"])
    auth = load_authorisation(profile.spend_authority.get("record"), root)
    reasons = []
    if auth.profile != profile.name:
        reasons.append(f"the record was signed for profile {auth.profile!r}, not {profile.name!r}")
    if Decimal(str(job_ceiling_usd)) > auth.job_ceiling_usd:
        reasons.append(f"the job ceiling {job_ceiling_usd} exceeds the authorised ceiling {auth.job_ceiling_usd}")
    missing = sorted({r for r in routes if r not in auth.routes_allowed})
    if missing:
        reasons.append(f"the record does not allow route(s) {missing}")
    if reasons:
        raise AuthorisationRefused(reasons)
    return auth
