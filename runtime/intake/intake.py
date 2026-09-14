"""Intake: a raw customer request becomes a PRODUCTION-JOB-v0 object, or a refusal.

Order matters and is the whole point of the module:

  1. idempotency on job_id — a repeat submission returns the first job and does nothing else;
  2. the object validates against the frozen contract;
  3. consent: a `person` reference asset without a consent_ref is refused before anything else;
  4. the named policy profile exists and carries every limit this lane will read;
  5. the requested kind is in that profile's allowed list.

Nothing here dispatches, prices, or plans. Nothing here writes outside the job store.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .. import paths
from ..contract_schema import Contract
from ..errors import Refusal
from ..policy import PolicyProfiles
from ..registry import DeliverableKinds
from ..util import canonical_json, sha256_obj

CONSENT_REQUIRED_ROLE = "person"  # the role word PRODUCTION-JOB-v0 names in its consent invariant


class JobStore:
    """Job records on disk. A runtime job never writes into the Lab's stores."""

    def __init__(self, root: str | Path | None = None):
        self.root = Path(root or paths.DEFAULT_STORE) / "jobs"

    def path_for(self, job_id: str) -> Path:
        safe = "".join(ch if (ch.isalnum() or ch in "-_.") else "_" for ch in job_id)
        return self.root / f"{safe}.json"

    def get(self, job_id: str) -> dict | None:
        path = self.path_for(job_id)
        if not path.exists():
            return None
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)

    def put(self, job: dict) -> None:
        path = self.path_for(job["job_id"])
        if path.exists():
            raise Refusal(
                Refusal.JOB_IMMUTABLE,
                "the job object is immutable after creation",
                job_id=job["job_id"],
                path=str(path),
            )
        os.makedirs(path.parent, exist_ok=True)
        tmp = path.with_suffix(".json.tmp")
        with open(tmp, "w", encoding="utf-8") as fh:
            fh.write(canonical_json(job))
        os.replace(tmp, path)


@dataclass(frozen=True)
class IntakeResult:
    job: dict
    created: bool
    job_sha256: str

    @property
    def job_id(self) -> str:
        return self.job["job_id"]


class Intake:
    def __init__(
        self,
        store: JobStore | None = None,
        profiles: PolicyProfiles | None = None,
        kinds: DeliverableKinds | None = None,
        contract: Contract | None = None,
    ):
        self.store = store or JobStore()
        self.profiles = profiles or PolicyProfiles()
        self.kinds = kinds or DeliverableKinds()
        self.contract = contract or Contract.load(paths.JOB_CONTRACT)

    # ------------------------------------------------------------------ submit
    def submit(self, raw: dict, *, now: str | None = None) -> IntakeResult:
        if not isinstance(raw, dict):
            raise Refusal(Refusal.MALFORMED_REQUEST, "a request must be an object", got=type(raw).__name__)
        job_id = raw.get("job_id")
        if not isinstance(job_id, str) or not job_id.strip():
            raise Refusal(Refusal.MALFORMED_REQUEST, "job_id is the idempotency key and must be a non-empty string")

        existing = self.store.get(job_id)
        if existing is not None:
            # Idempotency is not a nicety: it is the single defence against a retry storm
            # costing money twice. Nothing below this line runs on a repeat submission.
            return IntakeResult(job=existing, created=False, job_sha256=sha256_obj(existing))

        candidate = json.loads(canonical_json(raw))
        candidate.setdefault("received_utc", now or _utc_now())

        # (3) consent, read off the request as submitted, before any other work
        self._refuse_on_consent(candidate)

        # (4) the named profile exists and carries every limit this lane will read
        profile_name = candidate.get("policy_profile")
        if not isinstance(profile_name, str) or not profile_name.strip():
            raise Refusal(Refusal.MALFORMED_REQUEST, "policy_profile names the row that supplies every limit")
        profile = self.profiles.checked_profile(profile_name)
        self._apply_profile_defaults(candidate, profile)

        job = self.contract.validate(candidate)

        # (5) the requested kind is in that profile's allowed list, and in the registry
        self._refuse_on_kind(job, profile)

        self.store.put(job)
        return IntakeResult(job=job, created=True, job_sha256=sha256_obj(job))

    # ------------------------------------------------------------------ refusals
    @staticmethod
    def _refuse_on_consent(job: dict) -> None:
        assets = job.get("reference_assets") or []
        if not isinstance(assets, list):
            raise Refusal(Refusal.MALFORMED_REQUEST, "reference_assets must be a list", got=type(assets).__name__)
        for asset in assets:
            if not isinstance(asset, dict):
                raise Refusal(Refusal.MALFORMED_REQUEST, "each reference asset must be an object")
            if asset.get("role") == CONSENT_REQUIRED_ROLE and not asset.get("consent_ref"):
                raise Refusal(
                    Refusal.CONSENT_MISSING,
                    f"reference asset {asset.get('asset_id')!r} has role {CONSENT_REQUIRED_ROLE!r} "
                    "and no consent_ref; refused at intake, before any spend",
                    job_id=job.get("job_id"),
                    asset_id=asset.get("asset_id"),
                )

    def _refuse_on_kind(self, job: dict, profile) -> None:
        kind = job["deliverable_request"]["kind"]
        allowed = profile.limit("deliverable_kinds_allowed")
        if self.profiles.allow_all_token not in allowed and kind not in allowed:
            raise Refusal(
                Refusal.KIND_NOT_IN_PROFILE,
                f"deliverable kind {kind!r} is not in the allowed list of policy profile {profile.name!r}; "
                "widening the profile is a row edit, never a code change",
                job_id=job["job_id"],
                kind=kind,
                profile=profile.name,
                allowed=list(allowed),
            )
        self.kinds.get(kind)  # the kind must also have a registry row

    # ------------------------------------------------------------------ profile-sourced values
    def _apply_profile_defaults(self, job: dict, profile) -> None:
        """Fill an omitted job field from the profile. The value still comes from the
        profile row, so a profile without it refuses rather than a default hiding in code."""
        for job_field in ("cost_ceiling_usd", "retention.delete_after_days"):
            limit_name = self.profiles.job_field_default_limit(job_field)
            if not limit_name:
                continue
            if _get_path(job, job_field) is None:
                _set_path(job, job_field, profile.limit(limit_name))


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _get_path(obj: dict, dotted: str) -> Any:
    cur: Any = obj
    for part in dotted.split("."):
        if not isinstance(cur, dict):
            return None
        cur = cur.get(part)
    return cur


def _set_path(obj: dict, dotted: str, value: Any) -> None:
    parts = dotted.split(".")
    cur = obj
    for part in parts[:-1]:
        cur = cur.setdefault(part, {})
    cur[parts[-1]] = value
