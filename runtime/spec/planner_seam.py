"""The one reasoning-model call in the spec lane, behind a seam that runs from a fixture.

CANON-SHAPE-v1 §4: packs are injected UNCONDITIONALLY as a stable, byte-identical, cache-served
prefix, and the model writes ONE production plan. No compliance receipts: the gate verifies
mechanically, so the plan is all the model is asked for.

Everything in this module is offline.

  * `PlannerPrompt` builds the exact payload a reasoning model would receive — system block +
    injected pack bytes as the cached prefix, then the volatile Normalized Request as the first
    user turn, exactly as INJECTION-CONTRACT-v0 §2 places them. Nothing request-specific sits
    upstream of the cache breakpoint.
  * `FixturePlanner` answers from a recorded response, keyed by the sha256 of that payload. A
    prompt with no recorded answer is a refusal that writes the payload out and names the key, so
    the call can be made later, deliberately, by someone who meant to spend money.
  * `NoCallPlanner` refuses everything. It exists so a test can prove the lane never dispatches.
  * `BlueprintPlanner` (runtime/spec/blueprint_planner.py) answers a Stage-A-derived brief from its
    frozen blueprint, parsed deterministically. Same protocol.

THE PROTOCOL (14 Sep 2026): `plan(prompt: PlannerPrompt, *, job: dict, nr) -> dict`. The compiler
chooses the planner by the job's provenance (stage_a_case -> BlueprintPlanner; otherwise the
FixturePlanner it was built with), after first offering the job to an injected `template_planner`
callable (lane H's TemplateLibrary.fill) which returns None when it has no template for the job.

A response carries RESPONSE_FIELDS. The five BLUEPRINT_FIELDS are optional: they let a plan say
which planner produced it, from which source bytes, with which generation prompts, so the spec's
`blueprint` block (WAVE2-INTERFACES §1) is filled from the plan rather than guessed.

There is no live client here on purpose. This lane spends nothing.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

from .. import paths
from ..errors import Refusal
from ..util import canonical_json, load_yaml, sha256_text

RESPONSE_FIELDS = {
    "objective": str,
    "hard_constraints": list,
    "acceptance_statements": list,
    "composition": dict,
    "materials_and_light": dict,
    "resolution_class": (str, type(None)),
    # optional, blueprint-shaped (WAVE2-INTERFACES §1 spec["blueprint"])
    "planner": (str, type(None)),
    "source_ref": (str, type(None)),
    "generation_prompts": (dict, type(None)),
    "case_values": (dict, type(None)),
    "production_parameters": (dict, type(None)),
}
BLUEPRINT_FIELDS = ("planner", "source_ref", "generation_prompts", "case_values", "production_parameters")
PLANNER_RECORDED_FIXTURE = "recorded_fixture"
PLANNER_STAGE_A_BLUEPRINT = "stage_a_blueprint_fixture"


@dataclass(frozen=True)
class PlannerPrompt:
    system: str
    user: str

    @property
    def payload(self) -> dict:
        return {"system": self.system, "user": self.user}

    @property
    def sha256(self) -> str:
        return sha256_text(canonical_json(self.payload))


def build_prompt(job: dict, nr, canon, text_strategy) -> PlannerPrompt:
    """The cached prefix is Canon; the volatile turn is this request. Byte-stable by construction."""
    system = canon.payload
    request = {
        "task": (
            "Write ONE production plan for this request. Answer only with the JSON object described "
            "under output_schema. Every hard_constraint must quote the customer's own words. Every "
            "acceptance_statement must be decidable by a first-language judge looking only at the "
            "finished artifact, must open with 'ACCEPT only if ' or 'REJECT if ', and must never "
            "name a route, a model, an arm, a cost or a rule id."
        ),
        "brief_verbatim": job["brief"]["text"],
        "normalized_request": nr.as_dict(),
        "exact_text_strategy": {
            "strategy": text_strategy.strategy,
            "means": "the strings are set by code, or drawn by the maker, as the strategy says",
        },
        "deliverable": job["deliverable_request"],
        "output_schema": {
            "objective": "one sentence: what the customer is trying to achieve",
            "hard_constraints": ["customer statements that are non-negotiable, each grounded in the brief"],
            "acceptance_statements": ["3 to 6 'ACCEPT only if ...' / 'REJECT if ...' statements"],
            "composition": {"attention_order": "...", "placement_zone": "...", "edge_treatment": "..."},
            "materials_and_light": {"surface_finish_per_key_object": "...", "implied_light_source": "..."},
            "resolution_class": "a delivery class, or null",
        },
    }
    return PlannerPrompt(system=system, user=canonical_json(request))


class NoCallPlanner:
    """Refuses. The lane's proof that nothing here reaches a provider."""

    def plan(self, prompt: PlannerPrompt, *, job: dict | None = None, nr=None) -> dict:
        raise Refusal(
            Refusal.NO_DISPATCH_ALLOWED,
            "this lane makes no model call; run the seam from a fixture",
            prompt_sha256=prompt.sha256,
        )


class FixturePlanner:
    """A recorded reasoning pass. Same prompt bytes in, same plan out, forever."""

    def __init__(self, fixture_dir: str | Path | None = None, spill_dir: str | Path | None = None):
        self.dir = Path(fixture_dir or paths.PLANNER_FIXTURES)
        self.spill_dir = Path(spill_dir) if spill_dir else self.dir / "unanswered"
        self.index = (load_yaml(self.dir / "INDEX.yaml") if (self.dir / "INDEX.yaml").exists() else {}) or {}

    def plan(self, prompt: PlannerPrompt, *, job: dict | None = None, nr=None) -> dict:
        key = prompt.sha256
        name = (self.index.get("responses") or {}).get(key)
        if not name:
            spill = self._spill(prompt)
            raise Refusal(
                Refusal.PLANNER_FIXTURE_MISSING,
                "no recorded reasoning pass for this prompt; the lane will not call a model. "
                f"the exact payload was written to {spill}",
                prompt_sha256=key,
                index=str(self.dir / "INDEX.yaml"),
            )
        path = self.dir / name
        with open(path, "r", encoding="utf-8") as fh:
            response = json.load(fh)
        plan = validate_response(response, source=str(path))
        # a recorded pass says so; the spec's blueprint block reads these two
        plan["planner"] = plan.get("planner") or PLANNER_RECORDED_FIXTURE
        plan["source_ref"] = plan.get("source_ref") or f"{_rel(path)} sha256:{sha256_text(_read(path))}"
        return plan

    def _spill(self, prompt: PlannerPrompt) -> str:
        os.makedirs(self.spill_dir, exist_ok=True)
        path = self.spill_dir / f"{prompt.sha256}.prompt.json"
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(prompt.payload, fh, ensure_ascii=False, indent=2)
        return str(path)


def _rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(paths.ROOT))
    except ValueError:
        return str(path)


def _read(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def validate_response(response, source: str = "") -> dict:
    if not isinstance(response, dict):
        raise Refusal(Refusal.PLANNER_RESPONSE_INVALID, "the reasoning pass must return an object", source=source)
    out = {}
    for field, kind in RESPONSE_FIELDS.items():
        value = response.get(field)
        if field in ("objective", "hard_constraints", "acceptance_statements") and value in (None, "", []):
            raise Refusal(
                Refusal.PLANNER_RESPONSE_INVALID,
                f"the reasoning pass returned no {field}",
                source=source,
            )
        if value is not None and not isinstance(value, kind):
            raise Refusal(
                Refusal.PLANNER_RESPONSE_INVALID,
                f"{field} must be {kind}",
                got=type(value).__name__,
                source=source,
            )
        out[field] = value
    unknown = sorted(set(response) - set(RESPONSE_FIELDS))
    if unknown:
        raise Refusal(
            Refusal.PLANNER_RESPONSE_INVALID,
            "the reasoning pass returned fields the spec has nowhere to put",
            unknown=unknown,
            source=source,
        )
    return out
