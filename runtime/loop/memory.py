"""Empirical memory: assemble one OUTCOME-EVENT-v1 and write it once.

`assemble(...)` turns the loop's pieces (spec, manifest, gate outcomes, attempts, repairs, the
acceptance state machine) into the event dict; `OutcomeStore.write(event)` validates it against
runtime/contracts/OUTCOME-EVENT-v1.yaml and writes runtime/store/outcomes/<event_id>.json.

REFUSALS (each tested in test_g_memory.py):
- OUTCOME_IMMUTABLE            the event id already exists on disk; a correction is a new event
- OUTCOME_EVENT_ID_MISMATCH    event_id is not the sha of the content it claims to fingerprint
- OUTCOME_AUTHORITY_MISMATCH   acceptance.authority differs from the profile row's acceptance_authority
- OUTCOME_ACCEPTED_WITHOUT_HUMAN  decision accepted but no person recorded it (or a judge did)
- SCHEMA_VIOLATION             any contract violation, from runtime.contract_schema

DRY. Every event this tranche writes carries dry_run: true and says so; see the contract header.
"""
from __future__ import annotations

import json
import re
from decimal import Decimal
from pathlib import Path

from runtime import paths
from runtime.contract_schema import Contract
from runtime.errors import Refusal
from runtime.loop import package, refusals
from runtime.loop.acceptance import AUTOMATED_PREFIXES
from runtime.route.profile import load_profile
from runtime.util import canonical_json, sha256_obj, sha256_text

CONTRACT_PATH = paths.CONTRACTS / "OUTCOME-EVENT-v1.yaml"
DRY_NOTE = ("dry_run: nothing was sent to any provider; the artifact the post-draw gate saw was "
            "synthetic or absent. This event is empirical memory of the CHAIN, never of a real outcome.")
# spec.deterministic_checks name -> the gate row that mechanises it (post-draw)
DETERMINISTIC_TO_GATE_ROW = {
    "format_probe": "INFRA-CONTAINER",
    "baked_text_scan": "LIMIT-TEXT",
    "aspect_check": "DISPATCH-ASPECT",
    "duration_probe": "DISPATCH-DURATION",
    "audio_track_probe": "INFRA-VIDEO-TRACK",
    "dimensions_check": "DISPATCH-DIMENSIONS",
}


def contract() -> Contract:
    return Contract.load(CONTRACT_PATH)


def event_id_for(event: dict) -> str:
    body = {k: v for k, v in event.items() if k not in ("event_id", "written_utc")}
    return "oe-" + sha256_obj(body)


def _need(obj: dict, path: str, what: str):
    cur = obj
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur or cur[part] is None:
            raise Refusal(refusals.MANIFEST_FIELD_MISSING,
                          f"the {what} carries no {path!r}; the event cannot be assembled without it",
                          field=path)
        cur = cur[part]
    return cur


_HEX64 = re.compile(r"^[0-9a-f]{64}$")


def _fingerprint(value, what: str) -> str:
    """A sha256 as the contract means it: 64 hex characters. The committed route fixtures write an
    unquoted run of zeros that YAML reads as the integer 0; a fingerprint that is not 64 hex
    characters is refused here rather than stored as '0'."""
    text = str(value) if value is not None else ""
    if not _HEX64.match(text):
        raise Refusal(refusals.FINGERPRINT_INVALID,
                      f"{what} is not a sha256 (64 hex characters); the event stores fingerprints, "
                      f"not placeholders", field=what, got=text[:16])
    return text


def deterministic_checks(spec: dict, post_rows: list) -> list:
    by_id = {r["check_id"]: r for r in post_rows}
    out = []
    for name in spec.get("deterministic_checks") or []:
        row_id = DETERMINISTIC_TO_GATE_ROW.get(str(name))
        row = by_id.get(row_id) if row_id else None
        out.append({"check": str(name), "gate_row": row_id,
                    "status": row["status"] if row else "not_mechanised_in_this_tranche",
                    "detail": row["detail"] if row else "no gate row maps to this check"})
    return out


def assemble(spec: dict, manifest: dict, profile, *, package_text: str, pre: dict, attempts: list,
             repairs: list, acceptance, blueprint: dict, dry_run: bool, canon_lookup: dict | None = None,
             post_by_attempt: list | None = None) -> dict:
    """The event dict, without event_id/written_utc (finalize() adds them)."""
    primary = next((a for a in manifest.get("attempts") or [] if a.get("slot") == "primary"),
                   (manifest.get("attempts") or [None])[0])
    if primary is None:
        raise Refusal(refusals.MANIFEST_FIELD_MISSING, "the manifest carries no attempt", field="attempts")
    ev = primary.get("evidence") or {}
    cells = [str(c) for c in (ev.get("cells") or [])]
    acc = acceptance.to_event()
    last_post = attempts[-1]["_post"] if attempts else None
    post_rows = list(last_post["rows"]) if last_post else []
    blocking = list(dict.fromkeys(list(pre.get("blocking_failures") or [])
                                  + (list(last_post.get("blocking_failures") or []) if last_post else [])))
    settled = sum(Decimal(str(a.get("settled_usd", "0"))) for a in attempts)
    by_pool: dict = {}
    for a in attempts:
        by_pool[a["billing_pool"]] = format(Decimal(str(by_pool.get(a["billing_pool"], "0")))
                                           + Decimal(str(a.get("settled_usd", "0"))), "f")
    accepted = acc["decision"] == "accepted"
    if accepted:
        tc = {"eligible": True,
              "reason": ("accepted by a human under authority "
                         f"{acc['authority']}" + ("; dry_run true — eligibility of the CHAIN only: the template "
                                                  "library must not promote a dry event as a real outcome"
                                                  if dry_run else ""))}
    else:
        tc = {"eligible": False, "reason": f"acceptance decision {acc['decision']!r}; only an accepted outcome is eligible"}
    canon_spec = spec.get("canon") or {}
    canon = {
        "packs_selected": [str(r.get("pack_id") if isinstance(r, dict) else r)
                           for r in canon_spec.get("packs_selected") or []],
        "canon_gap": bool(canon_spec.get("canon_gap", False)),
        "missing_domains": [str(d) for d in canon_spec.get("missing_domains") or []],
    }
    if canon_lookup:
        for key in ("corpus_digest", "injection_prefix_sha256"):
            if canon_lookup.get(key):
                canon[key] = str(canon_lookup[key])
    event = {
        "job_id": str(spec["job_id"]),
        "spec_id": str(spec["spec_id"]),
        "policy_profile": str(getattr(profile, "name", None) or spec.get("policy_profile")),
        "dry_run": bool(dry_run),
        "fingerprints": {
            "job_sha256": _fingerprint(spec.get("job_sha256"), "spec.job_sha256"),
            "spec_sha256": sha256_obj(spec),
            "canon_injected_context_sha256": _fingerprint(
                (spec.get("canon") or {}).get("injected_context_sha256"), "spec.canon.injected_context_sha256"),
            "acceptance_contract_sha256": sha256_obj(list(spec.get("acceptance_contract") or [])),
            "decision_sha256": _fingerprint(_need(manifest, "provenance.decision_sha256", "manifest"),
                                            "manifest.provenance.decision_sha256"),
            "manifest_sha256": sha256_obj(manifest),
            "package_sha256": sha256_text(package_text),
        },
        "route": {
            "route_key": str(_need(primary, "route_key", "manifest attempt")),
            "cell_key": cells[0] if cells else str(_need(primary, "route_key", "manifest attempt")),
            "cells": cells,
            "text_mechanism": str(ev.get("text_mechanism") or package.text_mechanism(spec)),
            "surface": str(_need(primary, "surface", "manifest attempt")),
            "surface_model_id": str(_need(primary, "surface_model_id", "manifest attempt")),
            "evidence_status": str(_need(primary, "evidence.status", "manifest attempt")),
            "price_pin_ref": str(_need(primary, "price.price_pin_ref", "manifest attempt")),
        },
        "blueprint": {
            "planner": str(blueprint.get("planner") or "not stated by the plan"),
            "source_ref": str(blueprint.get("source_ref") or "not stated by the plan"),
            "template_id": blueprint.get("template_id"),
        },
        "canon": canon,
        "attempts": [{k: v for k, v in a.items() if not k.startswith("_")} for a in attempts],
        "gate": {"pre_dispatch": list(pre["rows"]), "post_draw": post_rows, "blocking_failures": blocking,
                 "post_draw_by_attempt": list(post_by_attempt or [])},
        "deterministic_checks": deterministic_checks(spec, post_rows),
        "repairs": list(repairs),
        "acceptance": acc,
        "cost": {"provider_usd_total": format(settled, "f"), "by_pool": by_pool, "draws": len(attempts),
                 "draws_per_accepted_outcome": len(attempts) if accepted else None,
                 "vendor_billed_usd": None},
        "template_candidate": tc,
    }
    if acceptance.delivered:
        event["delivered"] = dict(acceptance.delivered)
    return event


def finalize(event: dict, written_utc: str) -> dict:
    """Stamp event_id and written_utc, validate, return the contract-normalised copy."""
    body = {k: v for k, v in event.items() if k not in ("event_id", "written_utc")}
    # Normalise FIRST (the contract reader drops absent/None keys and formats money), then
    # fingerprint the normalised content: the id must be the sha of the bytes on disk.
    body = contract().validate(dict(body, event_id="oe-pending", written_utc=str(written_utc)))
    body["event_id"] = event_id_for(body)
    return contract().validate(body)


class OutcomeStore:
    def __init__(self, root: str | Path, profiles_path: str | Path | None = None):
        self.root = Path(root)
        self.dir = self.root / "outcomes"
        self.profiles_path = Path(profiles_path or paths.POLICY_PROFILES)

    def path_for(self, event_id: str) -> Path:
        return self.dir / f"{event_id}.json"

    def _check(self, event: dict) -> dict:
        event = contract().validate(event)
        expected = event_id_for(event)
        if event["event_id"] != expected:
            raise Refusal(refusals.OUTCOME_EVENT_ID_MISMATCH,
                          "event_id is not the sha of the event content; the event was altered after "
                          "it was fingerprinted", got=event["event_id"], expected=expected)
        profile = load_profile(event["policy_profile"], self.profiles_path)
        authority = str(profile.limit("acceptance_authority"))
        acc = event["acceptance"]
        if acc["authority"] != authority:
            raise Refusal(refusals.OUTCOME_AUTHORITY_MISMATCH,
                          f"acceptance.authority {acc['authority']!r} is not the profile row's "
                          f"acceptance_authority {authority!r}", profile=event["policy_profile"])
        if acc["decision"] == "accepted":
            by = acc.get("decided_by")
            if not isinstance(by, str) or not by.strip() or by.lower().startswith(AUTOMATED_PREFIXES) \
                    or not acc.get("transcript_sha256"):
                raise Refusal(refusals.OUTCOME_ACCEPTED_WITHOUT_HUMAN,
                              "acceptance.decision is accepted but no human approval is recorded "
                              "(decided_by must name a person; a judge or model is not one)",
                              decided_by=by)
        return event

    def write(self, event: dict) -> Path:
        event = self._check(event)
        path = self.path_for(event["event_id"])
        if path.exists():
            raise Refusal(refusals.OUTCOME_IMMUTABLE,
                          "an outcome event with this id is already written; events are immutable — a "
                          "correction is a new event that supersedes this one", path=str(path))
        self.dir.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(event, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                       encoding="utf-8")
        tmp.replace(path)
        return path

    def read(self, event_id: str) -> dict:
        return json.loads(self.path_for(event_id).read_text(encoding="utf-8"))

    def canonical(self, event: dict) -> str:
        return canonical_json(event)
