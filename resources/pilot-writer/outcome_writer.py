#!/usr/bin/env python3
"""RES-007: minimal v3 outcome writer.

Builds a topology-v3 archive (job -> outcome -> set -> unit -> step -> attempt/artifact ->
acceptance) in memory and writes it as YAML, so a real PILOT-001 production journey can be
PERSISTED rather than reconstructed from chat or logs afterwards.

AUTHORITY. This writer IMPLEMENTS the accepted contracts; it decides nothing:
  * schema:      resources/pre-execution-freeze/OUTCOME-PRODUCTION-TOPOLOGY-v3.yaml
  * cost rules:  resources/pre-execution-freeze/CPAO-CONTRACT-v3.md
  * lineage:     resources/pre-execution-freeze/LINEAGE-CONTRACT-v3.md
  * acceptance authority over produced records:
                 validators/validate_topology_v3.py and validators/recompute_cpao_v3.py

The validators remain the acceptance authority. The writer's own guards exist only to fail FAST
at record time on mistakes the validator would reject later (a local step carrying a provider
attempt, an ambiguous parent order, a hand-typed hash). Guards mirror the gates; they never
extend or weaken them.

WHAT THE WRITER REFUSES BY CONSTRUCTION
  * attempts on local_deterministic / human steps (gate G2) - there was no call, so no trial;
  * artifacts from local/human steps claiming an attempt or trial (G2/G6);
  * hand-supplied output_hash / output_bytes - artifact identity is always COMPUTED from the
    actual bytes, so it cannot be invented;
  * duplicate ids, unresolvable references (G3/G6), ambiguous ordered-parent positions (G5);
  * mutating a ledger entry after it is recorded - cost references are immutable here in code,
    matching `immutable: true` in the data;
  * (correction 2026-08-28, gate G12) provider attempts with incomplete inherited v2.1 call
    provenance - provider, model_id, model_version, endpoint, workflow, prompt_hash,
    config_hash, config_location, reference_asset_hashes, requested_at, completed_at are
    mechanically required named parameters, not an open field bag. eval_item_id is required
    for attempt_kind benchmark_eval and refused for production attempts (the
    Controller-approved conditional override in OUTCOME-PRODUCTION-TOPOLOGY-v3.yaml,
    authority CONTROLLER-PREPILOT-RETURN-REVIEW-1-2026-08-28.md).

WHAT THE WRITER DELIBERATELY DOES NOT DECIDE
  * HED-1 (which human time belongs in fully-loaded CpAO): the writer records whichever
    cost_class the caller supplies (`human_required` or `human_optional`); the classification
    of real pilot human time is a Controller decision, representable later without rewriting
    the journey (the ledger keeps `human_optional` rows; the engine excludes them from both
    views until reclassified by a NEW entry - never by editing an old one);
  * acceptance: `record_outcome_acceptance` stores who decided; Resources never decides
    (validator gate G7 rejects `decided_by: resources*`).

The writer does not call providers, generate media, or spend money. RES-007 budget: USD 0.
"""

import hashlib
import os
import re
from datetime import datetime

import yaml

# Frozen machine vocabularies, verbatim from the v3 topology / v2.1 schema.
VALID_ATTEMPT_STATUS = {"ok", "error", "refusal", "timeout", "cancelled"}
NON_OK_STATUS = VALID_ATTEMPT_STATUS - {"ok"}
VALID_LANE = {"image", "general_video", "native_av", "lipsync", "tts"}
VALID_EXECUTION_MODE = {"provider_call", "local_deterministic", "human"}
VALID_STEP_KIND = {"provider_generation", "transform", "composition", "edit",
                   "assembly", "repair", "human_review"}
VALID_ORDERING = {"ordered", "unordered"}
VALID_SET_KIND = {"video_sequence", "campaign_set", "variant_set", "multi_format_set"}
VALID_UNIT_KIND = {"shot", "layer", "end_card", "audio", "static", "caption",
                   "grade", "overlay", "other"}
VALID_OUTCOME_KIND = {"static_asset", "video_asset", "av_asset", "asset_set",
                      "campaign_variant"}
VALID_MEDIA_KIND = {"image", "video", "audio", "audio_video", "text", "other"}
VALID_PARENT_ROLE = {"source", "overlay", "audio", "mask", "reference",
                     "grade_source", "other"}
# Roles where sequence carries meaning - positions required, unique, contiguous from 0.
# Must match ORDERED_ROLES in validate_topology_v3.py.
ORDER_BEARING_ROLES = {"source", "overlay", "grade_source"}
VALID_COST_CLASS = {"api_tool", "local_compute", "human_required", "human_optional"}
VALID_ATTEMPT_KIND = {"production", "benchmark_eval"}
# Inherited v2.1 call provenance every v3 attempt must carry, non-null (gate G12).
ATTEMPT_REQUIRED_NON_NULL = ("provider", "model_id", "model_version", "endpoint",
                             "workflow", "prompt_hash", "config_hash",
                             "config_location", "requested_at")
# v2.1 optional attempt fields the writer will pass through verbatim. Anything else is
# refused - an unconstrained field bag is how required provenance went unenforced.
ATTEMPT_OPTIONAL_FIELDS = {"seed", "settings", "latency_ms"}
_UNSET = object()
# SHA-256 as the project records it (hashlib hexdigest): 64 lowercase hex characters.
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
# ISO-8601 UTC as the project records it: 2026-02-01T09:10:00Z (or explicit +00:00).
ISO_UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,6})?(Z|\+00:00)$")


def _is_iso_utc(v):
    if not isinstance(v, str) or not ISO_UTC_RE.match(v):
        return False
    try:
        datetime.fromisoformat(v.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False
VALID_TRANSFORM_OPERATION = {"concat", "overlay", "mix", "crop", "grade",
                             "encode", "resize", "other"}
STORAGE_CLASS = "C_irreproducible_empirical"
# Media-lineage namespaces that must NEVER appear as a request lineage id (gate G11).
MEDIA_LINEAGE_PREFIXES = ("lin_cvit", "lin_bhashini", "lin_diffusiondb", "lin_konstanz",
                          "lin_tigerlab", "lin_kwaivgi", "lin_google", "lin_abo",
                          "content::", "sha256:")


class WriterError(ValueError):
    """A record the accepted v3 contract forbids. Raised at record time, before any file is
    written, so a bad journey is refused instead of persisted."""


class OutcomeWriter:
    """Builds one v3 archive for one (or more) production journeys."""

    def __init__(self):
        self._jobs = []
        self._outcomes = []
        self._sets = []
        self._units = []
        self._steps = []
        self._attempts = []
        self._artifacts = []
        self._recipes = []
        self._measurements = []
        self._acceptances = []
        self._ledger = []
        self._ids = {}          # id -> namespace, for duplicate/reference checks
        self._trial_ids = set()

    # ---- id bookkeeping ------------------------------------------------------------

    def _register(self, namespace, id_):
        if not id_ or not isinstance(id_, str):
            raise WriterError(f"{namespace}: id must be a non-empty string, got {id_!r}")
        if id_ in self._ids:
            raise WriterError(f"{namespace} id {id_!r} already used as a "
                              f"{self._ids[id_]} id; ids are never reused")
        self._ids[id_] = namespace

    def _require(self, namespace, id_, why):
        if self._ids.get(id_) != namespace:
            raise WriterError(f"{why}: {namespace} {id_!r} does not exist; "
                              f"a reference must resolve at record time")

    @staticmethod
    def _require_vocab(value, vocab, field):
        if value not in vocab:
            raise WriterError(f"{field} {value!r} not in the frozen vocabulary "
                              f"{sorted(vocab)}")

    # ---- job / outcome / set / unit ------------------------------------------------

    def add_job(self, job_id, received_at, brief_ref, request_lineage_id,
                customer_ref=None):
        self._register("job", job_id)
        if not request_lineage_id:
            raise WriterError(f"job {job_id}: request_lineage_id is required; unknown "
                              f"request lineage is INDETERMINATE and must be recorded as "
                              f"such, never omitted")
        if any(str(request_lineage_id).startswith(p) for p in MEDIA_LINEAGE_PREFIXES):
            raise WriterError(f"job {job_id}: request_lineage_id {request_lineage_id!r} "
                              f"is a MEDIA lineage id; a brief's provenance and a "
                              f"photograph's provenance must never share a namespace (G11)")
        row = {"job_id": job_id, "received_at": received_at, "brief_ref": brief_ref,
               "request_lineage_id": request_lineage_id}
        if customer_ref is not None:
            row["customer_ref"] = customer_ref
        self._jobs.append(row)
        return job_id

    def add_outcome(self, outcome_id, job_id, outcome_kind, created_at,
                    supersedes_outcome_id=None, scope_change_boundary=None,
                    variant_group_id=None, reproducibility_status=None):
        self._register("outcome", outcome_id)
        self._require("job", job_id, f"outcome {outcome_id}")
        self._require_vocab(outcome_kind, VALID_OUTCOME_KIND, "outcome_kind")
        row = {"outcome_id": outcome_id, "job_id": job_id, "outcome_kind": outcome_kind,
               "created_at": created_at,
               # Null until set_final_artifact; may stay null ONLY while unaccepted.
               "final_artifact_id": None}
        if supersedes_outcome_id is not None:
            self._require("outcome", supersedes_outcome_id, f"outcome {outcome_id}")
            row["supersedes_outcome_id"] = supersedes_outcome_id
        if scope_change_boundary is not None:
            row["scope_change_boundary"] = bool(scope_change_boundary)
        if variant_group_id is not None:
            row["variant_group_id"] = variant_group_id
        if reproducibility_status is not None:
            self._require_vocab(reproducibility_status,
                                {"full", "partial", "not_reproducible"},
                                "reproducibility_status")
            row["reproducibility_status"] = reproducibility_status
        self._outcomes.append(row)
        return outcome_id

    def add_set(self, set_id, outcome_id, ordering, set_kind):
        self._register("set", set_id)
        self._require("outcome", outcome_id, f"set {set_id}")
        self._require_vocab(ordering, VALID_ORDERING, "ordering")
        self._require_vocab(set_kind, VALID_SET_KIND, "set_kind")
        self._sets.append({"set_id": set_id, "outcome_id": outcome_id,
                           "ordering": ordering, "set_kind": set_kind})
        return set_id

    def add_unit(self, unit_id, set_id, unit_kind, position=None,
                 unit_acceptance_ref=None):
        self._register("unit", unit_id)
        self._require("set", set_id, f"unit {unit_id}")
        self._require_vocab(unit_kind, VALID_UNIT_KIND, "unit_kind")
        parent = next(s for s in self._sets if s["set_id"] == set_id)
        if parent["ordering"] == "ordered":
            if position is None:
                raise WriterError(f"unit {unit_id}: parent set {set_id} is ordered, so a "
                                  f"unique position is REQUIRED (G5)")
            taken = [u.get("position") for u in self._units if u["set_id"] == set_id]
            if position in taken:
                raise WriterError(f"unit {unit_id}: position {position} already used in "
                                  f"ordered set {set_id}; the order would be ambiguous (G5)")
        elif position is not None:
            raise WriterError(f"unit {unit_id}: parent set {set_id} is unordered, so a "
                              f"position is FORBIDDEN - nobody may infer meaning from "
                              f"file order (G5)")
        row = {"unit_id": unit_id, "set_id": set_id, "unit_kind": unit_kind}
        if position is not None:
            row["position"] = position
        if unit_acceptance_ref is not None:
            # DIAGNOSTIC only. Never customer acceptance; never a CpAO numerator.
            row["unit_acceptance_ref"] = unit_acceptance_ref
        self._units.append(row)
        return unit_id

    # ---- steps ---------------------------------------------------------------------

    def _add_step(self, step_id, unit_id, step_kind, step_index, executed_at,
                  execution_mode, cost_ref=None, repair_of_step_id=None, **extra):
        self._register("step", step_id)
        self._require("unit", unit_id, f"step {step_id}")
        self._require_vocab(step_kind, VALID_STEP_KIND, "step_kind")
        self._require_vocab(execution_mode, VALID_EXECUTION_MODE, "execution_mode")
        row = {"step_id": step_id, "unit_id": unit_id, "step_kind": step_kind,
               "step_index": step_index, "executed_at": executed_at,
               "execution_mode": execution_mode, **extra}
        if cost_ref is not None:
            self._require("ledger", cost_ref, f"step {step_id} cost_ref")
            row["cost_ref"] = cost_ref
        if repair_of_step_id is not None:
            self._require("step", repair_of_step_id, f"step {step_id}")
            row["repair_of_step_id"] = repair_of_step_id
        self._steps.append(row)
        return step_id

    def add_provider_step(self, step_id, unit_id, step_kind, step_index, executed_at,
                          cost_ref=None, repair_of_step_id=None):
        """A step that calls a provider. Attempts are attached with record_attempt;
        the archive is invalid until it has at least one (G2)."""
        return self._add_step(step_id, unit_id, step_kind, step_index, executed_at,
                              "provider_call", cost_ref=cost_ref,
                              repair_of_step_id=repair_of_step_id, attempt_ids=[])

    def add_local_step(self, step_id, unit_id, step_kind, step_index, executed_at,
                       transform_ref, cost_ref=None, repair_of_step_id=None):
        """Local deterministic work (ffmpeg concat, overlay, grade...). Creates real
        bytes, costs no provider money, and MUST NOT manufacture an attempt (G2)."""
        self._require("recipe", transform_ref, f"step {step_id} transform_ref")
        return self._add_step(step_id, unit_id, step_kind, step_index, executed_at,
                              "local_deterministic", cost_ref=cost_ref,
                              repair_of_step_id=repair_of_step_id, attempt_ids=[],
                              transform_ref=transform_ref)

    def add_human_step(self, step_id, unit_id, step_kind, step_index, executed_at,
                       operator_ref, cost_ref=None, repair_of_step_id=None):
        """Human work (typically human_review). operator_ref is a ROLE reference, never
        PII. cost_ref may point at a human_required OR human_optional ledger entry -
        which real human time counts in fully-loaded CpAO is HED-1, a Controller
        decision this writer does not make."""
        if not operator_ref:
            raise WriterError(f"step {step_id}: human step requires operator_ref")
        return self._add_step(step_id, unit_id, step_kind, step_index, executed_at,
                              "human", cost_ref=cost_ref,
                              repair_of_step_id=repair_of_step_id, attempt_ids=[],
                              operator_ref=operator_ref)

    def add_transform_recipe(self, transform_ref, tool, tool_version, operation,
                             params, params_location):
        """Reconstructible provenance for a local step. params_hash is COMPUTED from the
        exact parameter string - never hand-typed, so it cannot be fabricated (G8)."""
        self._register("recipe", transform_ref)
        self._require_vocab(operation, VALID_TRANSFORM_OPERATION, "operation")
        if not tool_version:
            raise WriterError(f"recipe {transform_ref}: tool_version is required; "
                              f"deterministic in principle is not reproducible without "
                              f"the exact version (G8)")
        if params is None or params == "":
            raise WriterError(f"recipe {transform_ref}: params were not captured. Do not "
                              f"fabricate a params_hash - record the step unreproducible "
                              f"and let the outcome carry reproducibility_status: partial")
        params_hash = hashlib.sha256(
            params.encode("utf-8") if isinstance(params, str) else params).hexdigest()
        self._recipes.append({"transform_ref": transform_ref, "tool": tool,
                              "tool_version": tool_version, "operation": operation,
                              "params_hash": params_hash,
                              "params_location": params_location})
        return transform_ref

    # ---- attempts ------------------------------------------------------------------

    def record_attempt(self, attempt_id, step_id, status, lane, cost_ref, *,
                       provider, model_id, model_version, endpoint, workflow,
                       prompt_hash, config_hash, config_location,
                       reference_asset_hashes, requested_at, completed_at=_UNSET,
                       attempt_kind="production", eval_item_id=None,
                       trial_id=None, repeat_index=0, repeat_of_attempt_id=None,
                       retry_of_attempt_id=None, retry_reason=None, error_detail=None,
                       **optional_fields):
        """One provider/API call = one attempt = one trial - written when the call is
        MADE, kept whether it succeeded, errored, was refused, timed out or was
        cancelled. A failed call stays an individual row with its verbatim reason;
        aggregate counters never substitute (G1/G10).

        CORRECTED under CONTROLLER-PREPILOT-RETURN-REVIEW-1-2026-08-28: the full
        inherited v2.1 call provenance is now MECHANICALLY REQUIRED, not an
        unconstrained field bag. Nullable-by-contract values keep their v2.1 meaning:
        completed_at may be None only in the sense 'the call never completed' (the
        argument must still be passed explicitly); repeat_of/retry_of are None on a
        first attempt; reference_asset_hashes is a list, empty if none - never None.

        attempt_kind declares which eval_item_id rule applies (gate G12):
        'production' (default) - eval_item_id must NOT be supplied; the request context
        is already linked via step -> unit -> set -> outcome -> job -> brief_ref.
        'benchmark_eval' - eval_item_id is required exactly as v2.1 specifies.
        Only v2.1's optional fields (seed, settings, latency_ms) may be passed as
        extras; unknown fields are refused."""
        self._register("attempt", attempt_id)
        self._require_vocab(attempt_kind, VALID_ATTEMPT_KIND, "attempt_kind")
        prov = {"provider": provider, "model_id": model_id,
                "model_version": model_version, "endpoint": endpoint,
                "workflow": workflow, "prompt_hash": prompt_hash,
                "config_hash": config_hash, "config_location": config_location,
                "requested_at": requested_at}
        for field, value in prov.items():
            if value in (None, ""):
                raise WriterError(f"attempt {attempt_id}: required inherited field "
                                  f"{field!r} is missing or empty. v3 inherits the "
                                  f"v2.1 attempt contract; an attempt without its call "
                                  f"identity is not verifiable evidence (G12)")
        for hash_field, value in (("prompt_hash", prompt_hash),
                                  ("config_hash", config_hash)):
            if not (isinstance(value, str) and SHA256_RE.match(value)):
                raise WriterError(f"attempt {attempt_id}: {hash_field} must be a valid "
                                  f"SHA-256 - 64 lowercase hex characters (hashlib "
                                  f"hexdigest); a placeholder pseudo-hash is not a hash")
        if not isinstance(reference_asset_hashes, list):
            raise WriterError(f"attempt {attempt_id}: reference_asset_hashes must be a "
                              f"list (empty list if none), got "
                              f"{type(reference_asset_hashes).__name__}")
        for h in reference_asset_hashes:
            if not (isinstance(h, str) and SHA256_RE.match(h)):
                raise WriterError(f"attempt {attempt_id}: reference_asset_hashes member "
                                  f"{str(h)[:20]!r} is not a valid SHA-256")
        if not isinstance(repeat_index, int) or isinstance(repeat_index, bool) \
                or repeat_index < 0:
            raise WriterError(f"attempt {attempt_id}: repeat_index {repeat_index!r} must "
                              f"be an integer >= 0 (booleans, strings, negatives and "
                              f"null are refused)")
        if not _is_iso_utc(requested_at):
            raise WriterError(f"attempt {attempt_id}: requested_at "
                              f"{str(requested_at)[:30]!r} is not a valid ISO-8601 UTC "
                              f"timestamp (e.g. 2026-08-28T09:00:00Z)")
        if completed_at is not _UNSET and completed_at is not None \
                and not _is_iso_utc(completed_at):
            raise WriterError(f"attempt {attempt_id}: completed_at "
                              f"{str(completed_at)[:30]!r} is neither null (call never "
                              f"completed) nor a valid ISO-8601 UTC timestamp")
        if completed_at is _UNSET:
            raise WriterError(f"attempt {attempt_id}: completed_at must be passed "
                              f"explicitly - a timestamp, or None only where the call "
                              f"genuinely never completed. Omitting it would silently "
                              f"record 'never completed'.")
        if attempt_kind == "production" and eval_item_id is not None:
            raise WriterError(f"attempt {attempt_id}: production-job attempt with "
                              f"eval_item_id {eval_item_id!r}. A production attempt "
                              f"serves a brief, not a benchmark item; a fabricated "
                              f"benchmark link is invented provenance (G12)")
        if attempt_kind == "benchmark_eval" and not eval_item_id:
            raise WriterError(f"attempt {attempt_id}: benchmark/eval attempt requires "
                              f"eval_item_id exactly as v2.1 specifies (G12)")
        unknown = set(optional_fields) - ATTEMPT_OPTIONAL_FIELDS
        if unknown:
            raise WriterError(f"attempt {attempt_id}: unknown field(s) {sorted(unknown)}. "
                              f"Only v2.1 optional fields {sorted(ATTEMPT_OPTIONAL_FIELDS)} "
                              f"may be passed as extras; required provenance has named "
                              f"parameters so it cannot be silently omitted")
        step = self._step(step_id)
        if step["execution_mode"] != "provider_call":
            raise WriterError(
                f"attempt {attempt_id}: step {step_id} is "
                f"{step['execution_mode']}, and a local or human step MUST NOT "
                f"manufacture a provider attempt - it would create a trial that never "
                f"happened and corrupt every per-trial count (G2)")
        self._require_vocab(status, VALID_ATTEMPT_STATUS, "status")
        self._require_vocab(lane, VALID_LANE, "lane")
        trial_id = trial_id or attempt_id          # trial_id == attempt_id is acceptable
        if trial_id in self._trial_ids:
            raise WriterError(f"attempt {attempt_id}: trial_id {trial_id!r} already "
                              f"used. ONE CALL = ONE TRIAL - a repeat or retry is a NEW "
                              f"trial linked backward (G1)")
        self._trial_ids.add(trial_id)
        if status in NON_OK_STATUS and not error_detail:
            raise WriterError(f"attempt {attempt_id}: status {status!r} with no "
                              f"error_detail; a failure with no recorded reason is a "
                              f"row, not preserved evidence (G10)")
        if retry_of_attempt_id is not None:
            self._require("attempt", retry_of_attempt_id, f"attempt {attempt_id}")
            if not retry_reason:
                raise WriterError(f"attempt {attempt_id}: retry_of_attempt_id set "
                                  f"without retry_reason; repeat and retry are "
                                  f"different concepts and must stay distinguishable")
        if repeat_of_attempt_id is not None:
            self._require("attempt", repeat_of_attempt_id, f"attempt {attempt_id}")
        self._require("ledger", cost_ref, f"attempt {attempt_id} cost_ref")
        row = {"attempt_id": attempt_id, "trial_id": trial_id, "step_id": step_id,
               "attempt_kind": attempt_kind, "status": status, "lane": lane,
               "cost_ref": cost_ref, **prov,
               "reference_asset_hashes": reference_asset_hashes,
               "completed_at": completed_at,
               "repeat_index": repeat_index,
               "repeat_of_attempt_id": repeat_of_attempt_id,
               "retry_of_attempt_id": retry_of_attempt_id,
               "error_detail": error_detail,
               "storage_class": STORAGE_CLASS}
        if attempt_kind == "benchmark_eval":
            row["eval_item_id"] = eval_item_id
        if retry_reason is not None:
            row["retry_reason"] = retry_reason
        row.update(optional_fields)
        self._attempts.append(row)
        step["attempt_ids"].append(attempt_id)
        return attempt_id

    def _step(self, step_id):
        self._require("step", step_id, "step lookup")
        return next(s for s in self._steps if s["step_id"] == step_id)

    def _attempt(self, attempt_id):
        self._require("attempt", attempt_id, "attempt lookup")
        return next(a for a in self._attempts if a["attempt_id"] == attempt_id)

    # ---- artifacts -----------------------------------------------------------------

    def record_artifact(self, artifact_id, producing_step_id, media_kind,
                        data=None, path=None, output_location=None,
                        attempt_id=None, parents=None):
        """Persist an artifact record from ACTUAL BYTES - `data` (bytes) or `path` (a
        file on disk; production media is not assumed to be UTF-8 text). SHA-256 and
        byte length are computed here, never accepted from the caller, so identity
        cannot be invented.

        attempt_id is REQUIRED for provider_call steps and FORBIDDEN otherwise: an
        artifact from a local or human step genuinely has no attempt and no trial
        (G2/G6). parents is an ordered multi-parent lineage list of
        (parent_artifact_id, role, position) - position required and contiguous from 0
        for order-bearing roles (source/overlay/grade_source), None where order carries
        no meaning (G5)."""
        self._register("artifact", artifact_id)
        step = self._step(producing_step_id)
        self._require_vocab(media_kind, VALID_MEDIA_KIND, "media_kind")
        if (data is None) == (path is None):
            raise WriterError(f"artifact {artifact_id}: pass exactly one of data= or "
                              f"path=; an artifact IS its bytes and its hash is never "
                              f"hand-typed")
        if path is not None:
            with open(path, "rb") as f:
                data = f.read()
            output_location = output_location or path
        if not isinstance(data, bytes) or len(data) == 0:
            raise WriterError(f"artifact {artifact_id}: bytes required, got "
                              f"{type(data).__name__} of length "
                              f"{len(data) if hasattr(data, '__len__') else '?'}")
        if not output_location:
            raise WriterError(f"artifact {artifact_id}: output_location is required - "
                              f"where the bytes are retained")

        if step["execution_mode"] == "provider_call":
            if attempt_id is None:
                raise WriterError(f"artifact {artifact_id}: produced by provider_call "
                                  f"step {producing_step_id} but claims no attempt (G6)")
            att = self._attempt(attempt_id)
            if att["step_id"] != producing_step_id:
                raise WriterError(f"artifact {artifact_id}: attempt {attempt_id} "
                                  f"belongs to step {att['step_id']}, not "
                                  f"{producing_step_id}")
            if att["status"] != "ok":
                raise WriterError(f"artifact {artifact_id}: attempt {attempt_id} has "
                                  f"status {att['status']!r}; a failed, refused or "
                                  f"timed-out call produced no artifact and must not "
                                  f"be given one")
            trial_id = att["trial_id"]
        else:
            if attempt_id is not None:
                raise WriterError(f"artifact {artifact_id}: produced by a "
                                  f"{step['execution_mode']} step but claims attempt "
                                  f"{attempt_id!r}. A local or human step produces no "
                                  f"trial (G2)")
            trial_id = None

        parent_rows, seen, ordered_positions = [], set(), []
        for parent_artifact_id, role, position in (parents or []):
            self._require("artifact", parent_artifact_id,
                          f"artifact {artifact_id} parent")
            self._require_vocab(role, VALID_PARENT_ROLE, "parent role")
            if parent_artifact_id in seen:
                raise WriterError(f"artifact {artifact_id}: parent "
                                  f"{parent_artifact_id!r} listed more than once (G5)")
            seen.add(parent_artifact_id)
            if role in ORDER_BEARING_ROLES:
                if position is None:
                    raise WriterError(f"artifact {artifact_id}: parent "
                                      f"{parent_artifact_id!r} has order-bearing role "
                                      f"{role!r} but no position; the composition "
                                      f"order would be unknowable (G5)")
                ordered_positions.append(position)
            elif position is not None:
                raise WriterError(f"artifact {artifact_id}: parent "
                                  f"{parent_artifact_id!r} role {role!r} carries no "
                                  f"order, so position must be None (G5)")
            parent_rows.append({"parent_artifact_id": parent_artifact_id,
                                "role": role, "position": position})
        if ordered_positions and sorted(ordered_positions) != list(range(len(ordered_positions))):
            raise WriterError(f"artifact {artifact_id}: ordered parent positions "
                              f"{sorted(ordered_positions)} are not unique and "
                              f"contiguous from 0; the intended order is ambiguous (G5)")

        self._artifacts.append({
            "artifact_id": artifact_id, "producing_step_id": producing_step_id,
            "attempt_id": attempt_id, "trial_id": trial_id,
            "output_hash": hashlib.sha256(data).hexdigest(),
            "output_bytes": len(data), "output_location": output_location,
            "media_kind": media_kind, "storage_class": STORAGE_CLASS,
            "parents": parent_rows})
        return artifact_id

    # ---- measurements (Eval-owned semantics; stored verbatim) ----------------------

    def record_measurement(self, measurement_id, artifact_id, capability_id,
                           observation_unit, result=None, absence_reason=None,
                           evaluator_cost_ref=None):
        """Stores an already-supplied measurement reference verbatim. Resources never
        invents measurement semantics; capability_id is stored exactly as Eval defines
        it. Exactly one of result / absence_reason must be non-null."""
        self._register("measurement", measurement_id)
        self._require("artifact", artifact_id, f"measurement {measurement_id}")
        if (result is None) == (absence_reason is None):
            raise WriterError(f"measurement {measurement_id}: exactly one of result "
                              f"and absence_reason must be non-null")
        art = next(a for a in self._artifacts if a["artifact_id"] == artifact_id)
        if evaluator_cost_ref is not None:
            self._require("ledger", evaluator_cost_ref,
                          f"measurement {measurement_id} evaluator_cost_ref")
        self._measurements.append({
            "measurement_id": measurement_id, "artifact_id": artifact_id,
            "trial_id": art["trial_id"], "capability_id": capability_id,
            "observation_unit": observation_unit, "result": result,
            "absence_reason": absence_reason,
            "evaluator_cost_ref": evaluator_cost_ref})
        return measurement_id

    # ---- cost ledger ----------------------------------------------------------------

    def add_ledger_entry(self, ledger_entry_id, amount, currency, cost_class,
                         recorded_at, basis, unit="call", synthetic=None,
                         immutable=True):
        """One immutable cost row. Attempts/steps/measurements REFERENCE it by id -
        never an inline number. Once recorded here it cannot be edited or removed:
        there is deliberately no update/delete method for the ledger.

        cost_class must be one of api_tool | local_compute | human_required |
        human_optional (an unclassified cost cannot be placed in either CpAO view).
        `immutable` is data the CpAO engine checks - recording immutable=False is
        representable (and the engine will refuse to count it), because a writer that
        silently rewrote it to True would be inventing evidence."""
        self._register("ledger", ledger_entry_id)
        self._require_vocab(cost_class, VALID_COST_CLASS, "cost_class")
        if amount is None:
            raise WriterError(f"ledger {ledger_entry_id}: amount is required; a missing "
                              f"cost is not a zero cost")
        if not currency:
            raise WriterError(f"ledger {ledger_entry_id}: currency is required")
        row = {"ledger_entry_id": ledger_entry_id, "amount": amount,
               "currency": currency, "unit": unit, "recorded_at": recorded_at,
               "basis": basis, "immutable": immutable, "cost_class": cost_class}
        if synthetic is not None:
            row["synthetic"] = synthetic
        self._ledger.append(row)
        return ledger_entry_id

    # ---- acceptance ----------------------------------------------------------------

    def set_final_artifact(self, outcome_id, artifact_id):
        self._require("outcome", outcome_id, "set_final_artifact")
        self._require("artifact", artifact_id, "set_final_artifact")
        o = next(o for o in self._outcomes if o["outcome_id"] == outcome_id)
        o["final_artifact_id"] = artifact_id

    def record_outcome_acceptance(self, acceptance_id, outcome_id, accepted,
                                  decided_by, decided_at, brief_ref,
                                  rejection_reasons=None, revision_of_outcome_id=None):
        """CUSTOMER-level acceptance - the only level at which it exists, and the CpAO
        denominator. decided_by is the customer or a human acting for them, NEVER
        Resources. Unit-level 'this shot is usable' is diagnostic unit_acceptance and
        must never be recorded here."""
        self._register("acceptance", acceptance_id)
        self._require("outcome", outcome_id, f"acceptance {acceptance_id}")
        if str(decided_by or "").lower().startswith("resources"):
            raise WriterError(f"acceptance {acceptance_id}: decided_by must never be "
                              f"Resources (G7)")
        o = next(o for o in self._outcomes if o["outcome_id"] == outcome_id)
        if accepted and not o.get("final_artifact_id"):
            raise WriterError(f"acceptance {acceptance_id}: outcome {outcome_id} has "
                              f"no final_artifact_id - you cannot accept nothing (G7)")
        row = {"acceptance_id": acceptance_id, "outcome_id": outcome_id,
               "accepted": bool(accepted), "decided_by": decided_by,
               "decided_at": decided_at, "brief_ref": brief_ref}
        if rejection_reasons is not None:
            row["rejection_reasons"] = rejection_reasons
        if revision_of_outcome_id is not None:
            self._require("outcome", revision_of_outcome_id,
                          f"acceptance {acceptance_id}")
            row["revision_of_outcome_id"] = revision_of_outcome_id
        self._acceptances.append(row)
        return acceptance_id

    # ---- output --------------------------------------------------------------------

    def to_archive(self, expected_cpao=None):
        """The archive as a plain dict, in the exact shape the frozen validators read."""
        for s in self._steps:
            if s["execution_mode"] == "provider_call" and not s["attempt_ids"]:
                raise WriterError(f"step {s['step_id']}: provider_call step with no "
                                  f"attempts; a call that was never made is not a step "
                                  f"that happened (G2)")
        archive = {
            "schema_era": "v3",
            "jobs": self._jobs, "outcomes": self._outcomes, "sets": self._sets,
            "units": self._units, "steps": self._steps, "attempts": self._attempts,
            "transform_recipes": self._recipes, "artifacts": self._artifacts,
            "measurements": self._measurements,
            "outcome_acceptance": self._acceptances,
            "cost_ledger": self._ledger,
        }
        if expected_cpao is not None:
            # An independently hand-computed expectation the engine must reproduce.
            archive["expected_cpao"] = expected_cpao
        return archive

    def write_archive(self, path, expected_cpao=None):
        archive = self.to_archive(expected_cpao=expected_cpao)
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w") as f:
            yaml.safe_dump(archive, f, sort_keys=False, default_flow_style=False,
                           allow_unicode=True)
        return path
