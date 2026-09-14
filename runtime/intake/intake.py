"""Intake: a raw customer request becomes a PRODUCTION-JOB-v1 object, or a refusal.

Order matters and is the whole point of the module:

  1. idempotency on job_id — a repeat submission returns the first job and does nothing else;
  2. the optional `_provenance` block is lifted off the request and kept BESIDE the job (it is not a
     contract field; see below);
  3. consent: any reference asset that depicts an identifiable person and carries no consent_ref is
     refused before anything else, whatever its declared role (PRODUCTION-JOB-v1 invariant);
  4. the named policy profile exists and carries every limit this lane will read;
  5. the object validates against the frozen contract;
  6. the requested kind is in that profile's allowed list and in the registry;
  7. the job's operation and modality agree with KIND-NR-BINDING's row for the kind — the binding
     stays the provenance source, the job may not contradict it;
  8. where the profile says motion_requires_accepted_still, a motion block must come from the
     accepted still and name the deliverable it depends on.

Nothing here dispatches, prices, or plans. Nothing here writes outside the job store.

THE `_provenance` BLOCK. A brief derived from a frozen Stage-A case (runtime/tools/
brief_from_stage_a_case.py) needs to say where it came from — which case, which blueprint, which
bytes — so the compiler can serve its reasoning pass from that blueprint instead of a recorded
fixture. PRODUCTION-JOB-v1 has no such field and frozen contracts are never edited in place, so the
block travels OUTSIDE the contract object: a top-level `_provenance` key on the brief JSON that
intake strips before validation and stores beside the job as job_provenance
(job_id -> {source_pool, case_id, blueprint_ref, blueprint_sha256, ...}). It is never part of the
job's fingerprint. This was the lane's design choice on 14 Sep 2026, recorded here and in
CHANGES-v0-to-v1.md.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .. import paths
from ..canon.normalize import KindBinding
from ..contract_schema import Contract
from ..errors import Refusal
from ..policy import PolicyProfiles
from ..registry import DeliverableKinds
from ..util import canonical_json, sha256_obj

PROVENANCE_KEY = "_provenance"
# The consent gate reads this answer and nothing else. PRODUCTION-JOB-v1: "Any reference asset with
# depicts_identifiable_person true and no consent_ref is refused at intake, before any spend,
# whatever its declared role."
DEPICTS_FIELD = "depicts_identifiable_person"
ACCEPTED_STILL = "accepted_still"  # PRODUCTION-JOB-v1 motion.from value the Alpha-1 ruling names


class JobStore:
    """Job records on disk. A runtime job never writes into the Lab's stores."""

    def __init__(self, root: str | Path | None = None):
        self.root = Path(root or paths.DEFAULT_STORE) / "jobs"

    def path_for(self, job_id: str) -> Path:
        safe = "".join(ch if (ch.isalnum() or ch in "-_.") else "_" for ch in job_id)
        return self.root / f"{safe}.json"

    def provenance_path_for(self, job_id: str) -> Path:
        return self.path_for(job_id).with_suffix(".provenance.json")

    def get(self, job_id: str) -> dict | None:
        path = self.path_for(job_id)
        if not path.exists():
            return None
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)

    def get_provenance(self, job_id: str) -> dict | None:
        path = self.provenance_path_for(job_id)
        if not path.exists():
            return None
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)

    def put(self, job: dict, provenance: dict | None = None) -> None:
        path = self.path_for(job["job_id"])
        if path.exists():
            raise Refusal(
                Refusal.JOB_IMMUTABLE,
                "the job object is immutable after creation",
                job_id=job["job_id"],
                path=str(path),
            )
        os.makedirs(path.parent, exist_ok=True)
        if provenance is not None:
            _write_atomic(self.provenance_path_for(job["job_id"]), canonical_json(provenance))
        _write_atomic(path, canonical_json(job))


def _write_atomic(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(text)
    os.replace(tmp, path)


@dataclass(frozen=True)
class IntakeResult:
    job: dict
    created: bool
    job_sha256: str
    provenance: dict | None = None

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
        binding: KindBinding | None = None,
    ):
        self.store = store or JobStore()
        self.profiles = profiles or PolicyProfiles()
        self.kinds = kinds or DeliverableKinds()
        self.contract = contract or Contract.load(paths.JOB_CONTRACT)
        self.binding = binding or KindBinding()

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
            return IntakeResult(
                job=existing, created=False, job_sha256=sha256_obj(existing),
                provenance=self.store.get_provenance(job_id),
            )

        candidate = json.loads(canonical_json(raw))
        provenance = self._lift_provenance(candidate)
        candidate.setdefault("received_utc", now or _utc_now())

        # (3) consent, read off the request as submitted, before any other work
        self._refuse_on_consent(candidate)

        # (4) the named profile exists and carries every limit this lane will read
        profile_name = candidate.get("policy_profile")
        if not isinstance(profile_name, str) or not profile_name.strip():
            raise Refusal(Refusal.MALFORMED_REQUEST, "policy_profile names the row that supplies every limit")
        profile = self.profiles.checked_profile(profile_name)
        self._apply_profile_defaults(candidate, profile)

        # (5) the frozen contract
        job = self.contract.validate(candidate)

        # (6) the requested kind is in that profile's allowed list, and in the registry
        self._refuse_on_kind(job, profile)
        # (7) the job's own operation/modality agree with the binding row for that kind
        self._refuse_on_binding_disagreement(job)
        # (8) the Alpha-1 motion ordering, where the profile asks for it
        self._refuse_on_motion_dependency(job, profile)

        self.store.put(job, provenance)
        return IntakeResult(job=job, created=True, job_sha256=sha256_obj(job), provenance=provenance)

    # ------------------------------------------------------------------ provenance sidecar
    @staticmethod
    def _lift_provenance(candidate: dict) -> dict | None:
        """Remove `_provenance` from the object that will be validated; return it for the sidecar."""
        if PROVENANCE_KEY not in candidate:
            return None
        block = candidate.pop(PROVENANCE_KEY)
        if not isinstance(block, dict) or not isinstance(block.get("source_pool"), str) or not block["source_pool"]:
            raise Refusal(
                Refusal.PROVENANCE_MALFORMED,
                f"{PROVENANCE_KEY} must be an object naming source_pool; it travels beside the job, "
                "never inside the contract object",
                got=type(block).__name__,
            )
        return block

    # ------------------------------------------------------------------ refusals
    @staticmethod
    def _refuse_on_consent(job: dict) -> None:
        assets = job.get("reference_assets") or []
        if not isinstance(assets, list):
            raise Refusal(Refusal.MALFORMED_REQUEST, "reference_assets must be a list", got=type(assets).__name__)
        for asset in assets:
            if not isinstance(asset, dict):
                raise Refusal(Refusal.MALFORMED_REQUEST, "each reference asset must be an object")
            # `is True` on purpose: a missing or non-boolean answer is not "no", it is a schema
            # violation the contract raises next. Nobody passes a person through by omission.
            if asset.get(DEPICTS_FIELD) is True and not asset.get("consent_ref"):
                raise Refusal(
                    Refusal.CONSENT_MISSING,
                    f"reference asset {asset.get('asset_id')!r} depicts an identifiable person "
                    f"({DEPICTS_FIELD}: true) and carries no consent_ref; refused at intake, before "
                    f"any spend, whatever its declared role (here {asset.get('role')!r})",
                    job_id=job.get("job_id"),
                    asset_id=asset.get("asset_id"),
                    role=asset.get("role"),
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

    def _refuse_on_binding_disagreement(self, job: dict) -> None:
        """PRODUCTION-JOB-v1 makes operation and modality job fields so the Canon lookup can read them
        off the job. The binding row for the kind remains the provenance source (R01/R05
        customer_stated through the kind the customer chose), so the two must agree; a job that says
        otherwise is contradicting its own deliverable kind and is refused with both values named."""
        request = job["deliverable_request"]
        row = self.binding.row(request["kind"])
        for job_field, binding_field in (("operation", "requested_operation"), ("modality", "modality")):
            stated, bound = request[job_field], row[binding_field]
            if stated != bound:
                raise Refusal(
                    Refusal.SCHEMA_VIOLATION,
                    f"deliverable_request.{job_field} is {stated!r} but KIND-NR-BINDING binds kind "
                    f"{request['kind']!r} to {bound!r}; the job may not contradict the binding row that "
                    f"is the provenance source for this value ({self.binding.path})",
                    job_id=job["job_id"],
                    field=f"deliverable_request.{job_field}",
                    stated=stated,
                    bound=bound,
                    kind=request["kind"],
                )

    def _refuse_on_motion_dependency(self, job: dict, profile) -> None:
        """POLICY-PROFILES motion_requires_accepted_still (C-7: motion "DERIVED ONLY FROM THE ACCEPTED
        STILL"): a motion block must have from == accepted_still and depends_on naming the still it
        follows. A job that IS the still and carries no motion block is not asked for a dependency."""
        motion = job["deliverable_request"].get("motion")
        if not motion or not profile.motion_requires_accepted_still:
            return
        problems = []
        if motion.get("from") != ACCEPTED_STILL:
            problems.append(f"motion.from is {motion.get('from')!r}, not {ACCEPTED_STILL!r}")
        depends_on = motion.get("depends_on")
        if not isinstance(depends_on, str) or not depends_on.strip():
            problems.append("motion.depends_on names no deliverable")
        elif (depends_on == job["job_id"]
              and self.binding.row(job["deliverable_request"]["kind"])["modality"] == "video"):
            # a motion-only job (the kind's own modality is video) cannot be its own accepted still
            problems.append(f"motion.depends_on {depends_on!r} is this motion job itself; it must name the still")
        if problems:
            raise Refusal(
                Refusal.MOTION_DEPENDENCY_MISSING,
                f"policy profile {profile.name!r} sets motion_requires_accepted_still: true, so a motion "
                "deliverable is admitted only with motion.from == accepted_still and motion.depends_on "
                "naming the accepted still it is derived from; " + "; ".join(problems)
                + (f". Basis: {profile.row.get('motion_requires_accepted_still_note').strip()}"
                   if isinstance(profile.row.get("motion_requires_accepted_still_note"), str) else ""),
                job_id=job["job_id"],
                profile=profile.name,
                motion=dict(motion),
            )

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
