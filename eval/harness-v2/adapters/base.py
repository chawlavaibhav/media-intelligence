"""The adapter contract every route family implements. Read this before any concrete adapter.

ONE BUILDER, TWO USES

    `build_request(case_row, inputs)` is the single function that produces the request body.
    `dry_run()` renders it and prices it without sending; `dispatch()` reserves money against it,
    writes it to disk, then sends exactly those bytes. There is no second rendering path that
    could drift from the first, and a test proves the dry-run bytes equal the bytes the fake
    transport received.

INVARIANTS (task §2.1; each has a test)

    construction opens no network connection and reads no key; the credential is resolved at dispatch only,
    by NAME, and never enters a body, log, record or exception text; every output-count
    parameter is pinned to 1 and a caller value != 1 is refused; a parameter absent from the
    pinned schema is refused (the body is built from the schema, never from the caller's dict);
    `seed` is sent only when SEED-POLICY says `held` (today: never); 0 retries - one dispatch is
    one submit, polls / result / download are lifecycle steps of that trial, the poll loop is
    bounded by `max_status_checks` with an injected sleep and can never resubmit; the
    reservation is written through ledger.py BEFORE the first byte leaves; a pre-dispatch failure
    releases it, everything after the send settles conservatively (AmbiguousDispatch semantics
    imported from EMP-001); every attempt is persisted; artifacts are committed bytes.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any

import yaml

import hv2_paths
from providers import (AmbiguousDispatch, DispatchRefused, PreDispatchRefusal,  # noqa: F401
                       classify_transport_failure)
from budget_guard import BudgetExceeded  # noqa: F401
import store as S

# Looked up at call time so a test can point it at a throw-away file. Never the real file in tests.
DEFAULT_KEY_FILE = Path("~/.mi-keys").expanduser()
KEY_NAMES_ALLOWED = ("FAL_KEY", "SARVAM_API_KEY")
OUTPUT_COUNT_PARAMS = ("num_images", "num_videos", "num_samples", "num_outputs", "sampleCount",
                       "sample_count", "candidateCount", "n")
SEED_PARAMS = ("seed",)
PENDING_KEYS = ("$pending_artifact", "$pending_choice", "$pending_bytes", "$shape")
INPUT_ROLES_ALLOWED = ("image_url", "image_urls", "video_url", "audio_url", "voice", "image_bytes",
                       "image_mime", "reference_images", "language_code")
STORAGE_CLASS = "C_irreproducible_empirical"
GCP_CREDENTIAL_CANDIDATES = ("~/.mi-battery-keys/gcp-mi-battery-sa.json", "~/.aight-litellm-keys/vertex-sa.json")


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# --------------------------------------------------------------------------------- keys
class KeyLoader:
    """Reads a provider key by NAME from the environment or a `export NAME=value` file.

    Only the names in KEY_NAMES_ALLOWED are readable. The value is returned to the caller and
    to nobody else: it is never logged, never persisted, never put in an exception.
    """

    def __init__(self, path: Path | str | None = None):
        self.path = Path(path).expanduser() if path else None

    def read(self, name: str) -> str:
        if name not in KEY_NAMES_ALLOWED:
            raise PreDispatchRefusal(f"key name {name!r} is not one this harness may read; nothing was sent")
        value = os.environ.get(name)
        if value:
            return value
        path = self.path or DEFAULT_KEY_FILE
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                m = re.match(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)=(.*)$", line)
                if m and m.group(1) == name:
                    v = m.group(2).strip().strip('"').strip("'")
                    if v:
                        return v
        raise PreDispatchRefusal(
            f"{name} is not set in the environment or in {path.name}. Keys are read by name at "
            f"dispatch time and are never committed, logged or persisted. Nothing was sent.")


def resolve_gcp_credential_file() -> str:
    """MD-C3 default: the mi-battery file if MD-9 created it, else the aight-litellm file. NAME only."""
    for cand in GCP_CREDENTIAL_CANDIDATES:
        if Path(cand).expanduser().exists():
            return cand
    return GCP_CREDENTIAL_CANDIDATES[-1]


# ------------------------------------------------------------------------------- request
@dataclass
class Request:
    method: str
    url: str
    headers: dict                      # template: credentials appear ONLY as "<KEY:NAME>" / "<TOKEN:...>"
    body: dict
    followups: list = field(default_factory=list)   # extra API calls inside the SAME trial (extend)
    notes: list = field(default_factory=list)
    rendered_chars: int | None = None               # AF-9: characters actually in the body's text (character-metered routes)

    @property
    def body_bytes(self) -> bytes:
        return S.canonical_json(self.body)

    @property
    def body_sha256(self) -> str:
        return sha256_hex(self.body_bytes)

    def has_pending(self) -> bool:
        return _has_pending(self.body) or any(_has_pending(f.get("body")) for f in self.followups)


def _has_pending(obj: Any) -> bool:
    if isinstance(obj, dict):
        if any(k in PENDING_KEYS for k in obj):
            return True
        return any(_has_pending(v) for v in obj.values())
    if isinstance(obj, list):
        return any(_has_pending(v) for v in obj)
    return False


def pending_artifact(case_row: dict, role: str) -> dict:
    return {"$pending_artifact": f"{case_row.get('case_id')}:{case_row.get('arm')}:{role}"}


def pending_choice(what: str) -> dict:
    return {"$pending_choice": what}


# ------------------------------------------------------------------------------- outcome
@dataclass
class Outcome:
    status: str                         # ok | error | refusal | timeout
    error_class: str | None = None
    note: str = ""
    ambiguous: bool = False
    outcome_resolved: bool = True
    media: bytes | None = None
    content_type: str | None = None
    provider_request_id: str | None = None
    provider_meta: dict = field(default_factory=dict)
    intermediates: list = field(default_factory=list)    # [(suffix, bytes, content_type)]
    lifecycle_counts: dict = field(default_factory=dict)


# ------------------------------------------------------------------------- seed policy
_SEED_POLICY_CACHE: dict = {}


def seed_policy_for(route_key: str, path: Path | str = hv2_paths.SEED_POLICY) -> dict:
    p = str(path)
    if p not in _SEED_POLICY_CACHE:
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
        _SEED_POLICY_CACHE[p] = {
            "default": data.get("default_policy", "unset"),
            "routes": {r["route_key"]: r for r in (data.get("routes") or []) if isinstance(r, dict)},
        }
    pol = _SEED_POLICY_CACHE[p]
    r = pol["routes"].get(route_key) or {}
    return {"seed_policy": r.get("seed_policy", pol["default"]), "seed_value": r.get("seed_value")}


# ------------------------------------------------------------------------------- base
class RouteAdapter:
    family = "base"

    # AF-10: 180 checks x 5 s = 15 minutes of polling; a completed job is never abandoned before that.
    DEFAULT_MAX_STATUS_CHECKS = 180
    DEFAULT_POLL_INTERVAL_S = 5.0

    def __init__(self, entry, *, pricing, transport=None, budget=None, store=None, key_loader=None,
                 token_source=None, sleep=None, clock=None, max_status_checks: int = DEFAULT_MAX_STATUS_CHECKS,
                 poll_interval_s: float = DEFAULT_POLL_INTERVAL_S, seed_policy_path: Path | str = hv2_paths.SEED_POLICY,
                 allow_default_token_source: bool = False):
        if entry.adapter != self.family:
            raise ValueError(f"{type(self).__name__} cannot serve route {entry.route_key!r} (adapter {entry.adapter!r})")
        self.entry = entry
        self.pricing = pricing
        self.transport = transport
        self.budget = budget
        self.store = store
        self.key_loader = key_loader or KeyLoader()
        self.token_source = token_source
        self.sleep = sleep
        self.clock = clock
        self.max_status_checks = max_status_checks
        self.poll_interval_s = poll_interval_s
        self.seed_policy_path = seed_policy_path
        # AF-8: the gcloud token source is built from resolve_gcp_credential_file() ONLY when the live runner says so;
        # tests never set this flag, so no test can start a token exchange.
        self.allow_default_token_source = allow_default_token_source
        self.submits = 0            # instance totals (diagnostics); the persisted counts are PER DISPATCH (AF-5)
        self.status_checks = 0
        self._counts: dict = {}     # the current dispatch's lifecycle counts

    # -- to be implemented per family ---------------------------------------------------------
    def build_request(self, case_row: dict, inputs: dict | None = None) -> Request:
        raise NotImplementedError

    def _lifecycle(self, request: Request, headers: dict, attempt: dict) -> Outcome:
        raise NotImplementedError

    def _credential(self) -> str:
        raise NotImplementedError

    def _auth_headers(self, credential: str) -> dict:
        raise NotImplementedError

    def _default_token_source(self):
        """MD-C3 / AF-8: the gcloud token source over the resolved credential file NAME, at dispatch only."""
        if not self.allow_default_token_source:
            raise PreDispatchRefusal("no token source injected and the default gcloud token source is not allowed here "
                                     "(allow_default_token_source is set only by the live runner); nothing was sent")
        import transports as T
        return T.GcloudServiceAccountTokenSource(resolve_gcp_credential_file())

    # -- shared guards -------------------------------------------------------------------------
    def _now(self) -> str:
        return self.clock() if self.clock else now_utc()

    def _check_inputs(self, inputs: dict | None) -> dict:
        inputs = dict(inputs or {})
        unknown = sorted(k for k in inputs if k not in INPUT_ROLES_ALLOWED)
        if unknown:
            raise PreDispatchRefusal(
                f"caller passed {unknown} - the request body is built from the pinned schema, never from "
                f"the caller's dict, so a provider parameter (seed, output count, size, anything) cannot "
                f"reach the provider merely by being passed in. Nothing was sent.")
        return inputs

    def _guard_body(self, body: dict, allowed: set[str] | None, route_key: str) -> None:
        for k in OUTPUT_COUNT_PARAMS:
            if k in body and body[k] != 1:
                raise PreDispatchRefusal(f"{k}={body[k]!r}: output count is pinned to 1 (one call = one trial)")
        pol = seed_policy_for(route_key, self.seed_policy_path)
        for k in SEED_PARAMS:
            if k in body and pol["seed_policy"] != "held":
                raise PreDispatchRefusal(f"a seed is present but SEED-POLICY says {pol['seed_policy']!r} for {route_key}")
        if allowed is not None:
            unknown = sorted(k for k in body if k not in allowed)
            if unknown:
                raise PreDispatchRefusal(f"fields {unknown} are absent from the pinned schema for {route_key}; refusing to send a guessed field")

    # -- dry run ------------------------------------------------------------------------------
    def dry_run(self, case_row: dict, inputs: dict | None = None) -> dict:
        entry = self.entry
        try:
            req = self.build_request(case_row, inputs)
            build_error = None
        except (PreDispatchRefusal, ValueError) as exc:
            req, build_error = None, f"{type(exc).__name__}: {exc}"
        pc = self.pricing.evaluate(entry.route_key, case_row, rendered_chars=(req.rendered_chars if req else None))
        reasons = []
        if build_error:
            reasons.append(build_error)
        if entry.adapter == "none":
            reasons.append("no adapter built tonight (needs_controller_enablement)")
        if entry.shape_status != "verified":
            reasons.append(f"shape_status {entry.shape_status}")
        if case_row.get("conditional"):
            reasons.append("conditional row (listed, not in the cap)")
        for pre in entry.dispatch_preconditions:
            reasons.append(f"precondition not satisfiable tonight: {pre}")
        if not pc.ok:
            reasons.append(pc.refusal_reason)
        return {
            "method": req.method if req else None, "url": req.url if req else entry.endpoint,
            "headers": req.headers if req else None, "body": req.body if req else None,
            "body_sha256": req.body_sha256 if req else None,
            "api_calls_per_trial": entry.api_calls_per_trial,
            "followups": [{"url": f.get("url"), "body": f.get("body"), "note": f.get("note")} for f in (req.followups if req else [])],
            "shape_status": entry.shape_status, "price": pc.as_dict(),
            "would_dispatch": not reasons,
            "refusal_reason": ("; ".join(reasons) if reasons else None),
            "request_notes": list(req.notes) if req else [],
        }

    # -- dispatch -----------------------------------------------------------------------------
    def dispatch(self, case_row: dict, inputs: dict | None = None, call_context: dict | None = None) -> dict:
        entry = self.entry
        if self.transport is None:
            raise DispatchRefused("no transport injected. This adapter cannot reach a provider, which is the correct state until EVAL-040 is authorised.")
        if self.budget is None:
            raise DispatchRefused("no battery ledger. A paid call must be reserved against an authorised ceiling before it is dispatched.")
        if self.store is None:
            raise DispatchRefused("no sealed store. The request must be written to disk before it is sent.")
        if entry.adapter == "none":
            raise PreDispatchRefusal(f"{entry.route_key}: no adapter is built for surface {entry.surface} (needs_controller_enablement); nothing was sent")
        if entry.shape_status != "verified":
            raise PreDispatchRefusal(f"{entry.route_key}: request shape is {entry.shape_status}; live dispatch refuses an unverified body; nothing was sent")
        for pre in entry.dispatch_preconditions:
            raise PreDispatchRefusal(f"{entry.route_key}: dispatch precondition not satisfiable tonight ({pre}); nothing was sent")
        if case_row.get("conditional"):
            raise PreDispatchRefusal(f"{entry.route_key}: conditional row is outside the cap; nothing was sent")

        request = self.build_request(case_row, inputs)         # refuses bad params BEFORE any money moves
        if request.has_pending():
            raise PreDispatchRefusal("request body carries a pending input placeholder; a live dispatch needs concrete inputs; nothing was sent")
        pc = self.pricing.check(entry.route_key, case_row, rendered_chars=request.rendered_chars)   # refuses drift BEFORE anything is reserved
        tranche = case_row.get("tranche")
        stage = self.budget.tranche(tranche)
        call_context = dict(call_context or {})
        trial_id = call_context.get("trial_id") or make_trial_id(case_row)
        ctx = {
            "trial_id": trial_id, "attempt_id": trial_id, "case_id": case_row.get("case_id"),
            "item_id": case_row.get("item_id"), "route_key": entry.route_key, "arm": case_row.get("arm"),
            "repeat_index": case_row.get("repeat_index", 1),
            "billing_pool": entry.billing_pool, "currency": pc.currency,
            "amount_native": pc.amount_native, "amount_usd_equiv": pc.amount_usd_equiv, "fx_rate": pc.fx_rate,
            "unit_price": pc.unit_price, "quantity": pc.quantity, "quantity_unit": pc.quantity_unit,
            "price_pin_ref": pc.pin_ref,
        }
        reservation_id = stage.reserve(pc.amount_usd_equiv, **ctx)     # BudgetExceeded raises HERE, nothing sent

        # ---- AF-3: from here on, EVERY outcome persists an attempt and settles the reservation. Only a refusal
        # raised by our own code before any send (PreDispatchRefusal / a sealed-store clash) may release it.
        self._counts = {}
        secrets: list[str] = []
        attempt = self._base_attempt(case_row, request, pc, ctx, trial_id, None, None, reservation_id)
        outcome = None
        try:
            req_path, config_hash = self.store.write_request(trial_id, request.body_bytes)
            attempt["config_hash"], attempt["config_location"] = config_hash, str(req_path)
            credential = self._credential()
            secrets.append(credential)
            headers = self._auth_headers(credential)
            secrets += [v for v in headers.values() if isinstance(v, str)]
            del credential
            attempt["credential_file_name"] = self._credential_file_name()
            attempt["requested_at"] = self._now()
            # ---- THE DISPATCH BOUNDARY: everything below may have reached the provider ----------
            outcome = self._lifecycle(request, headers, attempt)
        except (PreDispatchRefusal, S.ArtifactIntegrityError) as exc:
            if not self._counts.get("submits"):                     # PROVEN nothing was sent
                stage.release()
                if isinstance(exc, S.ArtifactIntegrityError):
                    raise PreDispatchRefusal(f"trial {trial_id} already has a sealed request; a repeat is a new trial id, never a re-run: {exc}") from exc
                raise
            outcome = self._harness_exception(exc)
        except Exception as exc:                                     # noqa: BLE001 - AF-3: never escapes, never releases
            outcome = self._harness_exception(exc)
        if attempt["completed_at"] is None and outcome.outcome_resolved:
            attempt["completed_at"] = self._now()
        billing_state = "unknown_provisional" if (outcome.ambiguous or not outcome.outcome_resolved) else "reported"
        cost_ref = stage.record(pc.amount_usd_equiv, billing_state=billing_state, **ctx)
        artifact = None
        try:
            if outcome.media:
                artifact = self.store.seal(trial_id, outcome.media, outcome.content_type, outcome.provider_meta)
            for suffix, data, ct in outcome.intermediates:
                self.store.seal(trial_id, data, ct, outcome.provider_meta, suffix=suffix)
        except Exception as exc:                                     # noqa: BLE001 - a sealing failure is recorded, never lost
            outcome.note = f"{outcome.note} | artifact sealing failed: {type(exc).__name__}: {exc}"
            outcome.error_class = outcome.error_class or "artifact_seal_failed"
            outcome.status = "error" if outcome.status == "ok" else outcome.status
        attempt.update({
            "status": outcome.status, "error_class": outcome.error_class,
            "raw_status_note": (outcome.note or "")[:300],
            "billing_state": billing_state,
            "cost_basis": ("conservative_reserved_estimate_billing_unknown" if billing_state == "unknown_provisional"
                           else "provisional_pinned_rate"),
            "cost_ref": cost_ref, "ambiguous_dispatch": bool(outcome.ambiguous),
            "outcome_resolved": bool(outcome.outcome_resolved),
            "provider_request_id": outcome.provider_request_id,
            "lifecycle_counts": {**outcome.lifecycle_counts, "submits": self._counts.get("submits", 0), "status_checks": self._counts.get("status_checks", 0)},
            "artifact": ({k: artifact[k] for k in ("artifact_id", "relative_path", "bytes", "sha256", "content_type", "media_kind")}
                         if artifact else None),
        })
        attempt = scrub(attempt, secrets)
        self.store.write_attempt(trial_id, attempt)
        return attempt

    @staticmethod
    def _harness_exception(exc: BaseException) -> "Outcome":
        return Outcome("error", "harness_exception", f"{type(exc).__name__}: {exc}", ambiguous=True, outcome_resolved=False)

    def _base_attempt(self, case_row, request, pc, ctx, trial_id, config_hash, req_path, reservation_id) -> dict:
        e = self.entry
        prompt = extract_prompt(request.body)
        pol = seed_policy_for(e.route_key, self.seed_policy_path)
        return {
            "provider": e.surface, "surface": e.surface, "surface_model_id": e.surface_model_id,
            "model_id": e.surface_model_id, "model_version": e.surface_model_id, "endpoint": request.url,
            "workflow": e.workflow, "lane": e.lane, "case_id": ctx["case_id"], "item_id": ctx["item_id"],
            "route_key": e.route_key, "arm": ctx["arm"], "repeat_index": ctx["repeat_index"],
            "trial_id": trial_id, "attempt_id": trial_id,
            "prompt_hash": sha256_hex(prompt.encode("utf-8")) if prompt else None,
            "config_hash": config_hash, "config_location": (str(req_path) if req_path else None),
            "headers_template": request.headers, "api_calls_per_trial": e.api_calls_per_trial,
            "seed": None, "seed_policy": pol["seed_policy"],
            "billing_pool": e.billing_pool, "currency": pc.currency,
            "reserved_amount": str(pc.amount_native), "reserved_amount_usd_equiv": str(pc.amount_usd_equiv),
            "fx_rate": str(pc.fx_rate), "reservation_id": reservation_id, "cost_ref": None,
            "key_name": e.key_name, "credential_file_name": self._credential_file_name(),
            "price_pin_ref": pc.pin_ref, "unit_price": str(pc.unit_price), "quantity": str(pc.quantity),
            "quantity_unit": pc.quantity_unit, "quantity_rule": pc.quantity_rule,
            "requested_at": None, "completed_at": None, "status": None, "error_class": None,
            "raw_status_note": "", "billing_state": None, "ambiguous_dispatch": False,
            "outcome_resolved": False, "lifecycle_counts": {}, "provider_request_id": None,
            "retries": 0, "retry_of_attempt_id": None, "one_call_one_trial": True,
            "storage_class": STORAGE_CLASS, "synthetic": False,
        }

    def _credential_file_name(self) -> str:
        return self.entry.credential_file_name

    # -- lifecycle helpers ---------------------------------------------------------------------
    def _submit(self, url: str, headers: dict, payload: bytes, attempt: dict, counts: dict):
        """Exactly one submit per call. Returns (status, reply) or an ambiguous Outcome."""
        self.submits += 1
        self._counts["submits"] = self._counts.get("submits", 0) + 1
        counts["api_calls"] = counts.get("api_calls", 0) + 1
        try:
            return self.transport.post_json(url, headers, payload)
        except Exception as exc:                     # noqa: BLE001 - every post-send failure is ambiguous
            api_status, error_class = classify_transport_failure(exc)
            return Outcome(api_status, error_class,
                           f"{type(exc).__name__} after dispatch to {url}: {exc}",
                           ambiguous=True, outcome_resolved=False, lifecycle_counts=counts)

    def _poll(self, check, attempt: dict, counts: dict, what: str):
        """Bounded status polling with injected sleep. Returns the terminal reply or an Outcome."""
        for _ in range(self.max_status_checks):
            if counts.get("status_checks") and self.sleep:
                self.sleep(self.poll_interval_s)
            self.status_checks += 1
            self._counts["status_checks"] = self._counts.get("status_checks", 0) + 1
            counts["status_checks"] = counts.get("status_checks", 0) + 1
            try:
                done, reply = check()
            except Exception as exc:                 # noqa: BLE001
                api_status, error_class = classify_transport_failure(exc)
                return Outcome(api_status, f"poll_{error_class}",
                               f"{what} poll failed after the submit succeeded; the job may still complete and bill: {exc}",
                               ambiguous=True, outcome_resolved=False, lifecycle_counts=counts)
            if isinstance(reply, Outcome):
                return reply
            if done:
                return reply
        return Outcome("timeout", "poll_budget_exhausted",
                       f"{what} not done after {self.max_status_checks} status checks; it may still complete and bill. No re-submit.",
                       ambiguous=True, outcome_resolved=False, lifecycle_counts=counts)

    def _download(self, url: str, headers: dict, counts: dict):
        try:
            code, data, ct = self.transport.get_bytes(url, headers)
        except Exception as exc:                     # noqa: BLE001
            return Outcome("error", "artifact_download_failed",
                           f"generation completed (billable) but the artifact download failed: {exc}. The URL is recorded for a separately authorised fetch, never an automatic one.",
                           ambiguous=False, outcome_resolved=True, lifecycle_counts=counts,
                           provider_meta={"artifact_url": url})
        counts["downloads"] = counts.get("downloads", 0) + 1
        if code != 200 or not isinstance(data, (bytes, bytearray)) or not data:
            return Outcome("error", "artifact_download_failed", f"artifact URL answered {code} with {'no' if not data else 'non-byte'} content",
                           ambiguous=False, outcome_resolved=True, lifecycle_counts=counts, provider_meta={"artifact_url": url})
        return bytes(data), ct


def http_status_outcome(status: int, reply, counts: dict, refusal: bool = False, note: str = "") -> Outcome:
    """AF-6: a non-200 reply after the submit. 429, 5xx and a 2xx other than 200 mean the request was RECEIVED and
    may still complete and bill -> ambiguous / unresolved. A 4xx validation answer is a resolved provider error."""
    ambiguous = status == 429 or status >= 500 or (200 < status < 300)
    if refusal:
        return Outcome("refusal", "moderation_block", note[:300], ambiguous=False, outcome_resolved=True, lifecycle_counts=counts)
    return Outcome("error", f"http_{status}", note[:300], ambiguous=ambiguous, outcome_resolved=not ambiguous, lifecycle_counts=counts)


def error_of(reply) -> dict:
    """A provider `error` field may be a dict, a string or missing; never assume a dict (AF-3 probe A)."""
    err = reply.get("error") if isinstance(reply, dict) else None
    if isinstance(err, dict):
        return err
    return {"message": str(err)} if err else {}


def scrub(obj, secrets: list):
    """Replace every credential value (>= 8 chars) with <REDACTED> in every string of a record. Never logs the value."""
    keys = [k for k in secrets if isinstance(k, str) and len(k) >= 8]
    if not keys:
        return obj
    if isinstance(obj, str):
        for k in keys:
            if k in obj:
                obj = obj.replace(k, "<REDACTED>")
        return obj
    if isinstance(obj, dict):
        return {k: scrub(v, secrets) for k, v in obj.items()}
    if isinstance(obj, list):
        return [scrub(v, secrets) for v in obj]
    return obj


def make_trial_id(case_row: dict) -> str:
    return S.safe_id(f"{case_row.get('case_id')}__{case_row.get('route_key')}__{case_row.get('arm')}__r{case_row.get('repeat_index', 1)}")


def extract_prompt(body: dict) -> str | None:
    for k in ("prompt", "text"):
        if isinstance(body.get(k), str):
            return body[k]
    inst = body.get("instances")
    if isinstance(inst, list) and inst and isinstance(inst[0], dict) and isinstance(inst[0].get("prompt"), str):
        return inst[0]["prompt"]
    for c in body.get("contents") or []:
        for p in c.get("parts") or []:
            if isinstance(p, dict) and isinstance(p.get("text"), str):
                return p["text"]
    for part in body.get("input") or []:
        if isinstance(part, dict) and part.get("type") == "text":
            return part.get("text")
    return None


def b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def audio_flag(case_row: dict) -> bool | None:
    a = str((case_row.get("params") or {}).get("audio", "")).strip().lower()
    if a.startswith("on"):
        return True
    if a.startswith("off"):
        return False
    return None


def duration_s(case_row: dict) -> int | None:
    d = (case_row.get("params") or {}).get("duration_s")
    if isinstance(d, bool):
        return None
    if isinstance(d, (int, float)):
        return int(d)
    if isinstance(d, str) and d.strip().isdigit():
        return int(d.strip())
    return None


def aspect(case_row: dict) -> str | None:
    a = (case_row.get("params") or {}).get("aspect")
    if isinstance(a, str) and re.fullmatch(r"\d+:\d+", a.strip()):
        return a.strip()
    return None


def load_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


class NullAdapter(RouteAdapter):
    """`adapter: none` routes (Bedrock / Azure / Cloud TTS): render a dry-run row, refuse dispatch."""
    family = "none"

    def build_request(self, case_row: dict, inputs: dict | None = None) -> Request:
        self._check_inputs(inputs)
        e = self.entry
        return Request("POST", e.endpoint, {"Authorization": "<no adapter built tonight>"},
                       {"$shape": "not_built", "$reason": e.notes or "needs_controller_enablement"},
                       notes=["no adapter: priced as a conditional line only"])

    def _credential(self) -> str:
        raise PreDispatchRefusal(f"{self.entry.route_key}: no adapter is built for surface {self.entry.surface}; nothing was sent")

    def _auth_headers(self, credential: str) -> dict:
        return {}

    def _lifecycle(self, request: Request, headers: dict, attempt: dict) -> Outcome:
        raise PreDispatchRefusal("unreachable: NullAdapter.dispatch refuses before any lifecycle")
