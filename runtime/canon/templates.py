"""The template library — empirical memory for plans (CANON-SHAPE-v1 §4, last stage).

Controller ruling C-10, 14 Sep 2026: "Authorise USD-0 implementation of: Canon Injection v1;
template / empirical-memory integration. Do NOT compile the remaining eight packs unless a real
runtime failure later demands one." This module is the second of those two builds. It spends
nothing: no model, no provider, no network.

What it does, in plain English:

  * promote(spec, outcome_event) — when a PERSON has accepted a job's output, the plan that job was
    made from is kept as a template: the plan fields, the generation prompts, which Canon packs were
    injected behind it, and what route made it (a hint only). The customer's exact strings become
    numbered slots. Refuses unless the event says accepted, by a human. A dry-run event (nothing was
    drawn) can only make a dry-only template.
  * match(nr) — a later job whose Normalized Request has the SAME identity (kind, modality, operation,
    aspect, the exact strings with script and placement, motion, supplied-asset roles, market,
    language — see identity_fields) gets that template back. Exact comparison of one sha; no fuzzy
    matching, no search, no model. Newest wins if several match.
  * fill(template, job, nr) — the template's strings are replaced, by position, with THIS job's
    strings, and the result is handed to the compiler in the planner seam's shape with
    planner "template:<id>", so the repeat job needs no reasoning pass.

What it is not: a route decision (the router still decides from evidence and the policy profile;
route_hint is a hint), Registry evidence (it says nothing about model capability), or Lab data (the
store is runtime/store/templates, never eval/). Contract: runtime/contracts/TEMPLATE-v0.yaml.
"""
from __future__ import annotations

import copy
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .. import paths
from ..contract_schema import Contract
from ..errors import Refusal
from ..util import canonical_json, sha256_text
from .packs import RECEIPT_VOCABULARY

# Refusal codes of this module. They are string codes like every Refusal code; they live here
# rather than on runtime.errors.Refusal because that file is shared across lanes this round.
TEMPLATE_PROMOTION_REFUSED = "TEMPLATE_PROMOTION_REFUSED"
TEMPLATE_SLOT_MISMATCH = "TEMPLATE_SLOT_MISMATCH"
TEMPLATE_IMMUTABLE = "TEMPLATE_IMMUTABLE"
TEMPLATE_INVALID = "TEMPLATE_INVALID"

SCHEMA = "TEMPLATE-v0"
IDENTITY_VERSION = 1
STATUS_REUSABLE = "reusable"
STATUS_DRY_ONLY = "reusable_dry_only"
HUMAN = "human"
ACCEPTED = "accepted"

# The gate's HOLD-lane id shape (canon/gate/doctrine.py ID_TOKEN_RE), reused read-only.
_ID_TOKEN = re.compile(r"\b(?:sk|scs)_[a-z0-9_]+\b")
_TEMPLATE_ID_HEX = 16


# ---------------------------------------------------------------------------- identity
def identity_fields(nr) -> dict:
    """The NR facts that define "the same job shape", identity_version 1.

    IN: kind, modality, requested_operation, aspect, exact_text (sorted {content, script, placement}),
    motion ({seconds, from, audio} or None), supplied_asset_roles (sorted role names — presence and
    role, never bytes or asset ids), entity_roles (sorted), market, language.
    OUT: brief prose, deliverable count, job_id, customer_ref, asset hashes, policy profile, cost
    ceiling, retention, ambiguity markers, provenance fields.

    Exact-text CONTENT is in on purpose. A template's objective and prompts describe one customer's
    product, so for Alpha 1 "the same shape" means the same copy for the same product; a template
    is never stretched over a different customer's ad by shape alone. Changing this set is a new
    IDENTITY_VERSION, never a silent edit.

    `placement` comes from the NR text requirement when the v1 normaliser carries it (WAVE2 §1) and
    is None on a v0 NR; the value is recorded as found, never assumed.
    """
    strings = [
        {"content": t["content"], "script": t.get("script"), "placement": t.get("placement")}
        for t in (nr.text_requirements or [])
    ]
    motion = None
    if nr.temporal_structure:
        motion = {
            "seconds": nr.temporal_structure.get("seconds"),
            "from": nr.temporal_structure.get("from"),
            "audio": bool(nr.temporal_structure.get("audio", False)),
        }
    language = (nr.language_topology or {}).get("stated_language") if nr.language_topology else None
    return {
        "identity_version": IDENTITY_VERSION,
        "kind": nr.deliverable_set["kind"],
        "modality": nr.modality,
        "requested_operation": nr.requested_operation,
        "aspect": nr.deliverable_set["aspect"],
        "exact_text": sorted(strings, key=canonical_json),
        "motion": motion,
        "supplied_asset_roles": sorted(a["role"] for a in (nr.supplied_assets or [])),
        "entity_roles": sorted(e["role"] for e in (nr.entities or [])),
        "market": nr.market,
        "language": language,
    }


def normalized_identity(nr) -> str:
    return sha256_text(canonical_json(identity_fields(nr)))


# ---------------------------------------------------------------------------- the library
class TemplateLibrary:
    """JSON files under root, one per template, written once. No index: match() is an exact
    comparison over a directory listing, which is O(templates) and fine for an alpha; an index
    would be a second copy of the truth."""

    def __init__(self, root: str | Path | None = None, contract: Contract | None = None,
                 hold_ids: set | None = None):
        self.root = Path(root or paths.TEMPLATE_STORE)
        self.contract = contract or Contract.load(paths.TEMPLATE_CONTRACT)
        self._hold_ids = hold_ids

    # ------------------------------------------------------------------ promote
    def promote(self, spec: dict, outcome_event: dict, *, nr=None, job: dict | None = None,
                promoted_by: str = "runtime", created_utc: str | None = None) -> dict:
        """spec + accepted event -> template. The identity needs the Normalized Request: pass `nr`,
        or `job` (normalised here, deterministically). The spec alone cannot give it — it carries
        neither market/language nor the supplied assets' roles — and nothing is guessed."""
        self._check_acceptance(outcome_event)
        self._check_same_job(spec, outcome_event)
        if nr is None:
            if job is None:
                self._refuse("promotion needs the Normalized Request (nr=) or the job (job=) to compute the "
                             "template identity; the spec alone does not carry market, language or asset roles",
                             field="nr")
            if job.get("job_id") != spec.get("job_id"):
                self._refuse("the job passed is not the job this spec was compiled from",
                             job=job.get("job_id"), spec=spec.get("job_id"))
            from .normalize import normalize

            nr = normalize(job)
        dry_run = outcome_event.get("dry_run")
        if not isinstance(dry_run, bool):
            self._refuse("the outcome event does not say whether it was a dry run; a template is never "
                         "promoted on an assumed live acceptance", field="dry_run")
        status = STATUS_REUSABLE
        if dry_run:
            eligible = (outcome_event.get("template_candidate") or {}).get("eligible")
            if eligible is not True:
                self._refuse("a dry-run event promotes only when template_candidate.eligible is true; "
                             "nothing was drawn, so a dry acceptance alone proves nothing about the plan",
                             dry_run=True, eligible=eligible)
            # a dry event can only make a dry-only template: nobody accepted a real artifact
            status = STATUS_DRY_ONLY

        blueprint = self._blueprint(spec)
        slots = self._slots(spec)
        if [s["content"] for s in slots] != [t["content"] for t in (nr.text_requirements or [])]:
            self._refuse("the spec's exact strings and the Normalized Request's disagree; the template "
                         "would carry slots its identity does not describe", field="exact_text.strings")
        fields = identity_fields(nr)
        canon = self._canon(spec, outcome_event)
        route = outcome_event.get("route") or {}
        route_hint = {k: route.get(k) for k in ("route_key", "cell_key", "text_mechanism") if route.get(k)}

        content = {
            "schema": SCHEMA,
            "identity_version": IDENTITY_VERSION,
            "identity_fields": fields,
            "status": status,
            "accepted_event_id": outcome_event["event_id"],
            "source": {"job_id": spec["job_id"], "spec_id": spec["spec_id"]},
            "blueprint": blueprint,
            "slots": slots,
            "canon": canon,
            "route_hint": route_hint,
            "provenance": {
                "acceptance_authority": outcome_event["acceptance"]["authority"],
                "dry_run": dry_run,
                "promoted_by": promoted_by,
            },
        }
        content["normalized_identity"] = sha256_text(canonical_json(content["identity_fields"]))
        template_id = "tpl-" + sha256_text(canonical_json(content))[:_TEMPLATE_ID_HEX]
        template = {"template_id": template_id, "created_utc": created_utc or _utc_now(), **content}

        self._scan_for_forbidden_material(template)
        validated = self.contract.validate(template, code=TEMPLATE_INVALID)
        self._write(validated)
        return validated

    # ------------------------------------------------------------------ match
    def match(self, nr, *, dispatch_mode: str = "live") -> dict | None:
        """The single template whose normalized_identity equals this NR's. Exact; newest wins.
        A dry-only template is returned only under dispatch_mode "dry"."""
        wanted = normalized_identity(nr)
        allowed = {STATUS_REUSABLE} | ({STATUS_DRY_ONLY} if dispatch_mode == "dry" else set())
        candidates = [
            t for t in self._all()
            if t.get("normalized_identity") == wanted
            and t.get("identity_version") == IDENTITY_VERSION
            and t.get("status") in allowed
        ]
        if not candidates:
            return None
        candidates.sort(key=lambda t: (t["created_utc"], t["template_id"]))
        return candidates[-1]

    # ------------------------------------------------------------------ fill
    def fill(self, template: dict, job: dict, nr) -> dict:
        """The template's plan with every slot re-filled from THIS job's strings, by position.

        Returns the planner seam's RESPONSE_FIELDS plus generation_prompts, template_id and
        planner "template:<id>" (use response_fields() for the strict RESPONSE_FIELDS subset). The
        template's own strings never survive into the new job: if the counts differ the fill is
        refused, never partial."""
        slots = template["slots"]
        new = [t["content"] for t in (nr.text_requirements or [])]
        if len(new) != len(slots):
            raise Refusal(
                TEMPLATE_SLOT_MISMATCH,
                "the job carries a different number of exact strings than the template has slots; "
                "a template is filled completely or not at all",
                template_id=template["template_id"],
                slots=len(slots),
                job_strings=len(new),
            )
        old = [s["content"] for s in slots]
        blueprint = _refill(copy.deepcopy(template["blueprint"]), old, new)

        # nothing of the template's copy may remain (a slot equal to its replacement is fine)
        blob = canonical_json(blueprint)
        leftover = [o for o in old if o not in new and o in blob]
        if leftover:
            raise Refusal(
                TEMPLATE_SLOT_MISMATCH,
                "a template string survived the slot fill",
                template_id=template["template_id"],
                leftover=leftover,
            )
        return {
            "objective": blueprint["objective"],
            "hard_constraints": list(blueprint["hard_constraints"]),
            "acceptance_statements": list(blueprint["acceptance_statements"]),
            "composition": blueprint.get("composition"),
            "materials_and_light": blueprint.get("materials_and_light"),
            "resolution_class": blueprint.get("resolution_class"),
            "generation_prompts": blueprint["generation_prompts"],
            "template_id": template["template_id"],
            "planner": f"template:{template['template_id']}",
        }

    # ------------------------------------------------------------------ internals
    def _check_acceptance(self, event: dict) -> None:
        acceptance = event.get("acceptance") or {}
        decision = acceptance.get("decision")
        authority = acceptance.get("authority")
        if decision != ACCEPTED:
            self._refuse(f"promotion needs acceptance.decision == {ACCEPTED!r}; the event says {decision!r}",
                         decision=decision)
        if authority != HUMAN:
            self._refuse(f"promotion needs a {HUMAN} acceptance authority (C-8: every Alpha-1 output requires "
                         f"human approval); the event says {authority!r}", authority=authority)
        if not event.get("event_id"):
            self._refuse("the outcome event has no event_id to cite", field="event_id")

    def _check_same_job(self, spec: dict, event: dict) -> None:
        for key in ("job_id", "spec_id"):
            if key in event and event[key] != spec.get(key):
                self._refuse(f"the outcome event's {key} is not this spec's {key}",
                             event=event[key], spec=spec.get(key))

    def _blueprint(self, spec: dict) -> dict:
        prompts = ((spec.get("blueprint") or {}).get("generation_prompts") or {})
        # The prompt a repeat job needs is the one the mechanism DISPATCHES (lead integration, 14 Sep
        # 2026): under code-composed exact text (C-6c mechanism B) that is the textless plate and
        # `main` is legitimately absent; under a motion deliverable it is the motion prompt.
        mechanism = (spec.get("exact_text") or {}).get("text_mechanism")
        needed = ("textless_plate" if mechanism == "deterministic_text_composition"
                  else "motion" if (spec.get("deliverable") or {}).get("motion") and prompts.get("motion")
                  else "main")
        if not prompts.get(needed):
            self._refuse(f"the spec carries no blueprint.generation_prompts.{needed} (the prompt its text mechanism "
                         f"{mechanism!r} dispatches); a template without that prompt cannot serve a repeat job and "
                         "nothing is invented for it", field="blueprint.generation_prompts")
        out = {
            "objective": spec["objective"],
            "hard_constraints": list(spec.get("hard_constraints") or []),
            "acceptance_statements": list(spec.get("acceptance_contract") or []),
            "generation_prompts": {k: prompts[k] for k in ("main", "textless_plate", "motion") if prompts.get(k)},
        }
        if spec.get("composition"):
            out["composition"] = spec["composition"]
        if spec.get("materials_and_light"):
            out["materials_and_light"] = spec["materials_and_light"]
        if (spec.get("deliverable") or {}).get("resolution_class"):
            out["resolution_class"] = spec["deliverable"]["resolution_class"]
        return out

    @staticmethod
    def _slots(spec: dict) -> list:
        slots = []
        for index, item in enumerate((spec.get("exact_text") or {}).get("strings") or []):
            slot = {"id": item.get("id") or f"t{index + 1}", "content": item["content"]}
            if item.get("script"):
                slot["script"] = item["script"]
            if item.get("placement"):
                slot["placement"] = item["placement"]
            slots.append(slot)
        return slots

    def _canon(self, spec: dict, event: dict) -> dict:
        spec_canon = spec.get("canon") or {}
        rows = spec_canon.get("packs_selected") or []
        digest = (event.get("canon") or {}).get("corpus_digest")
        if not digest:
            self._refuse("the outcome event carries no canon.corpus_digest; the accepted-Canon fingerprint the "
                         "plan was written against is recorded, never guessed", field="canon.corpus_digest")
        prefix = spec_canon.get("prefix_sha256") or spec_canon.get("injected_context_sha256")
        if not prefix:
            self._refuse("the spec carries no Canon prefix fingerprint", field="canon.injected_context_sha256")
        out = {
            "packs_selected": [r["pack_id"] if isinstance(r, dict) else str(r) for r in rows],
            "packs_injected": [r["pack_id"] for r in rows if isinstance(r, dict) and r.get("compiled")],
            "corpus_digest": digest,
            "prefix_sha256": prefix,
        }
        if spec_canon.get("injection_version"):
            out["injection_version"] = spec_canon["injection_version"]
        return out

    def _scan_for_forbidden_material(self, template: dict) -> None:
        blob = canonical_json(template)
        words = [w for w in RECEIPT_VOCABULARY if w in blob]
        if words:
            self._refuse("the plan carries receipt vocabulary retired by CANON-SHAPE-v1 §5; a template never "
                         "carries it forward", words=words)
        hold = self.hold_ids()
        found = sorted(t for t in set(_ID_TOKEN.findall(blob)) if t in hold)
        if found:
            self._refuse("the plan names HOLD-lane Canon ids; fail closed", hold_ids=found)

    def hold_ids(self) -> set:
        if self._hold_ids is None:
            from canon.gate.doctrine import candidate_ids  # read-only reuse of the gate's listing

            self._hold_ids = candidate_ids()
        return self._hold_ids

    def _write(self, template: dict) -> None:
        os.makedirs(self.root, exist_ok=True)
        path = self.root / f"{template['template_id']}.json"
        if path.exists():
            raise Refusal(
                TEMPLATE_IMMUTABLE,
                "a template is written once; this id already exists and is not overwritten",
                template_id=template["template_id"],
                path=str(path),
            )
        with open(path, "x", encoding="utf-8") as fh:
            json.dump(template, fh, ensure_ascii=False, indent=2, sort_keys=True)

    def _all(self) -> list:
        if not self.root.exists():
            return []
        out = []
        for path in sorted(self.root.glob("*.json")):
            with open(path, "r", encoding="utf-8") as fh:
                out.append(json.load(fh))
        return out

    @staticmethod
    def _refuse(message: str, **context: Any) -> None:
        raise Refusal(TEMPLATE_PROMOTION_REFUSED, message, **context)


def response_fields(filled: dict) -> dict:
    """The strict planner_seam.RESPONSE_FIELDS subset of a filled plan (validate_response refuses
    unknown keys, so the consumer takes this and reads generation_prompts / planner separately)."""
    from ..spec.planner_seam import RESPONSE_FIELDS

    return {k: filled.get(k) for k in RESPONSE_FIELDS}


# ---------------------------------------------------------------------------- helpers
def _refill(value: Any, old: list, new: list) -> Any:
    """Replace every old string with the new one at the same position, in every string of the
    plan. Two phases through private-use-area placeholders (U+E000/U+E001 never occur in customer
    copy or plan prose) so a replacement never feeds a later one."""
    if isinstance(value, str):
        order = sorted(range(len(old)), key=lambda i: -len(old[i]))     # longest first
        for i in order:
            if old[i]:
                value = value.replace(old[i], f"\ue000{i}\ue001")
        for i in order:
            value = value.replace(f"\ue000{i}\ue001", new[i])
        return value
    if isinstance(value, list):
        return [_refill(v, old, new) for v in value]
    if isinstance(value, dict):
        return {k: _refill(v, old, new) for k, v in value.items()}
    return value


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
