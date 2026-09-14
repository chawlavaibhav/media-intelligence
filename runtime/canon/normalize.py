"""Job -> Normalized Request (CANON-010 grammar), with no model in the loop.

CANON-SHAPE-v1 §4 puts the pack lookup between the Normalized Request and the reasoning pass.
So the NR has to be computable from the job alone: if a model produced it, the "deterministic
table lookup, never a model choice" property would be gone.

Every kind-specific value comes from runtime/canon/KIND-NR-BINDING-v0.yaml. No kind is named
in this file.
"""
from __future__ import annotations

import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .. import paths
from ..errors import Refusal
from ..util import load_yaml

LATIN = "LATIN"


@dataclass(frozen=True)
class NormalizedRequest:
    requested_operation: str            # R01
    supplied_assets: list               # R02
    deliverable_set: dict               # R04
    modality: str                       # R05
    entities: list                      # R06
    text_requirements: list             # R08
    language_topology: dict | None      # R10
    temporal_structure: dict | None     # R12
    delivery: dict                      # R15
    specification_provenance: dict      # R16
    ambiguity_markers: list             # R17
    acceptance_intent: dict | None      # R18
    market: str | None = None
    facets: dict = field(default_factory=dict)

    def as_dict(self) -> dict:
        return {
            "R01_requested_operation": self.requested_operation,
            "R02_supplied_assets": self.supplied_assets,
            "R04_deliverable_set": self.deliverable_set,
            "R05_modality": self.modality,
            "R06_entities": self.entities,
            "R08_text_requirements": self.text_requirements,
            "R10_language_topology": self.language_topology,
            "R12_temporal_structure": self.temporal_structure,
            "R15_delivery": self.delivery,
            "R16_specification_provenance": self.specification_provenance,
            "R17_ambiguity_markers": self.ambiguity_markers,
            "R18_acceptance_intent": self.acceptance_intent,
            "market": self.market,
        }


class KindBinding:
    def __init__(self, path: str | Path | None = None):
        self.path = str(path or paths.KIND_NR_BINDING)
        doc = load_yaml(self.path) or {}
        self._rows = {row["kind"]: row for row in doc.get("kinds", [])}
        self.product_entity_roles = list(doc.get("product_entity_roles", []))
        self.identity_roles = list(doc.get("identity_roles", []))
        self.supplied_asset_roles = list(doc.get("supplied_asset_roles", []))
        self.ambiguity_rules = list(doc.get("ambiguity_markers", []))

    def row(self, kind: str) -> dict:
        row = self._rows.get(kind)
        if row is None:
            raise Refusal(
                Refusal.NR_BINDING_MISSING,
                f"deliverable kind {kind!r} has no Normalized-Request binding; the Canon lookup "
                "cannot be computed without one. Adding it is a row, not a code change",
                kind=kind,
                binding=self.path,
                known=sorted(self._rows),
            )
        return row


def script_of(text: str) -> str:
    """The dominant Unicode script name of a string, from the characters themselves."""
    counts: dict[str, int] = {}
    for ch in text:
        if not ch.isalpha():
            continue
        try:
            name = unicodedata.name(ch)
        except ValueError:
            continue
        script = name.split(" ")[0]
        counts[script] = counts.get(script, 0) + 1
    if not counts:
        return "UNSPECIFIED"
    return max(sorted(counts), key=lambda k: counts[k])


def normalize(job: dict, binding: KindBinding | None = None) -> NormalizedRequest:
    binding = binding or KindBinding()
    request = job["deliverable_request"]
    row = binding.row(request["kind"])

    assets = list(job.get("reference_assets") or [])
    supplied = [
        {"asset_id": a["asset_id"], "role": a["role"], "provenance": a["provenance"], "sha256": a["sha256"]}
        for a in assets
        if a.get("role") in binding.supplied_asset_roles
    ]

    entities = [
        {"role": a["role"], "asset_id": a["asset_id"], "identity_bound": a["role"] in binding.identity_roles}
        for a in assets
        if a.get("role") in binding.product_entity_roles
    ]
    product_entity_present = bool(entities) or bool(row.get("product_entity_implied"))

    strings = list(job.get("exact_text_strings") or [])
    text_requirements = []
    for index, item in enumerate(strings):
        declared = item.get("script")
        text_requirements.append(
            {
                "id": f"t{index + 1}",
                "content": item["value"],
                "script": declared or script_of(item["value"]).lower(),
                "script_detected": script_of(item["value"]),
                "may_reflow": bool(item.get("may_reflow", False)),
                "exactness": "contractual" if not item.get("may_reflow", False) else "reflowable",
            }
        )

    brief = job.get("brief") or {}
    language = brief.get("language")
    market = brief.get("market")
    language_topology = None
    if language or any(t["script_detected"] not in (LATIN, "UNSPECIFIED") for t in text_requirements):
        language_topology = {
            "stated_language": language,
            "scripts": sorted({t["script_detected"] for t in text_requirements if t["script_detected"] != "UNSPECIFIED"}),
        }

    motion = request.get("motion") or None
    temporal_structure = None
    if motion:
        temporal_structure = {
            "seconds": motion.get("seconds"),
            "from": motion.get("from"),
            "audio": bool(motion.get("audio", False)),
        }

    facets = {
        "exact_text_present": bool(text_requirements),
        "exactness_contractual": any(t["exactness"] == "contractual" for t in text_requirements),
        "script_beyond_latin": any(t["script_detected"] not in (LATIN, "UNSPECIFIED") for t in text_requirements),
        "scripts": sorted({t["script_detected"].lower() for t in text_requirements if t["script_detected"] != "UNSPECIFIED"}),
        "text_in_scene": _text_in_scene(),
        "motion_requested": bool(motion),
        "text_must_move": bool(motion) and bool(text_requirements),
        "product_entity_present": product_entity_present,
        "supplied_asset_present": bool(supplied),
        # in the binding's own order of consequence, not alphabetical: the thing whose identity
        # the customer is most likely to be judged on comes first
        "identity_bound_roles": [r for r in binding.identity_roles
                                if any(a.get("role") == r for a in assets)],
        "market": market,
    }

    markers = []
    provenance_modality = row["modality_provenance"]
    for rule in binding.ambiguity_rules:
        if _marker_fires(rule["marker"], facets, brief, row["modality"]):
            markers.append({"marker": rule["marker"], "note": rule.get("note", "")})
            if rule.get("sets_modality_provenance"):
                provenance_modality = rule["sets_modality_provenance"]

    return NormalizedRequest(
        requested_operation=row["requested_operation"],
        supplied_assets=supplied,
        deliverable_set={"kind": request["kind"], "count": request.get("count", 1), "aspect": request["aspect"]},
        modality=row["modality"],
        entities=entities,
        text_requirements=text_requirements,
        language_topology=language_topology,
        temporal_structure=temporal_structure,
        delivery={"aspect": request["aspect"], "motion": temporal_structure},
        specification_provenance={
            "requested_operation": row["operation_provenance"],
            "modality": provenance_modality,
            "source": "PRODUCTION-JOB-v0 + runtime/canon/KIND-NR-BINDING-v0.yaml",
        },
        ambiguity_markers=markers,
        acceptance_intent={"advertising": True} if row.get("advertising_acceptance_intent") else None,
        market=market,
        facets=facets,
    )


def _text_in_scene() -> bool:
    """Does the type have to sit INSIDE the scene — printed on a pack, a sign, a surface —
    rather than sit over it?

    PRODUCTION-JOB-v0 carries no field that says so (see the report on this lane). Absent a
    customer statement the runtime never assumes it: an unstated in-scene requirement would
    push a contractual price line onto generated text, which is the expensive way to be wrong.
    A v1 `exact_text_strings[].placement: overlay | in_scene` closes this with a row, and this
    function reads it; nothing else in the lane changes.
    """
    return False


def _marker_fires(marker: str, facets: dict, brief: dict, modality: str) -> bool:
    """The conditions named in KIND-NR-BINDING-v0.ambiguity_markers, as facts about the job."""
    if marker == "motion_requested_on_a_still_modality":
        return facets["motion_requested"] and modality != "video"
    if marker == "exact_text_script_without_stated_language":
        return facets["script_beyond_latin"] and not brief.get("language")
    return False
