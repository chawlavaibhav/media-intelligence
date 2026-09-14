"""Derive a PRODUCTION-JOB-v1 request from a frozen Stage-A case. Deterministic; reads only.

    python3 -m runtime.tools.brief_from_stage_a_case IMG-TEXT-02 [--out runtime/fixtures/alpha-briefs/img-text-02.json]
        [--consent-ref CONSENT-...] [--depends-on alpha-dry-img-core-01] [--profile dry]

WHAT IT READS (never writes): eval/empirical-planning/STAGE-A-FREEZE-2026-09/TEST-CASES.yaml — the
case's customer_request, nr, reference_assets, blueprint_ref — and the blueprint file's bytes for
its sha256. The join from case family to deliverable kind is runtime/tools/STAGE-A-CASE-KIND-MAP-v0.yaml.

WHAT IT DOES NOT DO: infer. Every value is either the customer's own words (brief.text verbatim),
a field of the frozen Normalized Request (strings, scripts, exactness, entities, duration, aspect),
a row of the kind map, or a fixed tool choice recorded under `_provenance`. Where a real customer
would have had to say something the case does not (does the copy sit on a pack? is there consent
for the person in the photograph?), the tool takes the SAFE default and records that it did:
placement `overlay` with `_provenance.placement_default: true`; no consent_ref unless
`--consent-ref` is given, so the consent gate fires exactly as it would for a real submission.

THE `_provenance` BLOCK is not a contract field. Intake strips it and stores it beside the job
(runtime/intake/intake.py); the compiler reads it to serve the reasoning pass from the case's frozen
blueprint (runtime/spec/blueprint_planner.py). It carries: source_pool stage_a_case, case_id,
blueprint_ref, blueprint_sha256, test_cases_sha256, tool_sha256, and the tool's own choices.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from .. import paths
from ..canon.normalize import KindBinding
from ..errors import Refusal
from ..util import canonical_json, load_yaml

KIND_MAP = Path(__file__).with_name("STAGE-A-CASE-KIND-MAP-v0.yaml")
SOURCE_POOL = "stage_a_case"
_PARENTHETICAL = re.compile(r"\s*\([^)]*\)")


class DerivationError(Refusal):
    """The case cannot be turned into a job without inventing something. Named, never guessed."""


def _sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_case(case_id: str, freeze_root: Path | None = None) -> tuple[dict, dict, Path]:
    root = Path(freeze_root or paths.STAGE_A_FREEZE)
    test_cases = root / "TEST-CASES.yaml"
    doc = load_yaml(test_cases) or {}
    for row in doc.get("cases", []):
        if row.get("case_id") == case_id:
            return doc, row, test_cases
    raise DerivationError(Refusal.PLANNER_FIXTURE_MISSING, f"no Stage-A case {case_id!r}", test_cases=str(test_cases))


def family_of(case_id: str) -> str:
    return case_id.rsplit("-", 1)[0]


def derive(case_id: str, *, consent_ref: str | None = None, depends_on: str | None = None,
           profile: str | None = None, freeze_root: Path | None = None) -> dict:
    kind_map = load_yaml(KIND_MAP) or {}
    fixed = kind_map["fixed"]
    doc, case, test_cases_path = load_case(case_id, freeze_root)
    root = Path(freeze_root or paths.STAGE_A_FREEZE)

    family = family_of(case_id)
    kind = (kind_map.get("family_kind") or {}).get(family)
    if not kind:
        raise DerivationError(
            Refusal.KIND_NOT_IN_REGISTRY,
            f"Stage-A case family {family!r} has no deliverable-kind row in {KIND_MAP.name}; the tool does "
            "not guess a kind. Marketplace cases are handled by brief_from_marketplace_case.py",
            case_id=case_id, family=family, map=str(KIND_MAP),
        )
    binding_row = KindBinding().row(kind)

    request = case.get("customer_request") or {}
    nr = case.get("nr") or {}
    entities = {e.get("entity_id"): e for e in (nr.get("entities") or [])}
    person_entities = [e for e in entities.values() if e.get("entity_type") == "person"]

    # ---- exact text strings, from the frozen NR
    strings = []
    for t in nr.get("text_requirements") or []:
        strings.append({
            "value": t["content"],
            "script": t.get("script") or "other",
            "may_reflow": t.get("exactness") != "exact",
            "placement": fixed["placement_default"],
        })

    # ---- reference assets, from the frozen NR's supplied assets
    assets, depicts_basis = [], {}
    for a in nr.get("supplied_assets") or []:
        role, basis = _asset_role(a, entities, kind_map)
        depicts, why = _depicts(a, entities, person_entities)
        depicts_basis[a["asset_id"]] = why
        asset = {
            "asset_id": a["asset_id"],
            "role": role,
            "sha256": hashlib.sha256(f"{fixed['asset_provenance']}:{case_id}:{a['asset_id']}".encode("utf-8")).hexdigest(),
            "content_type": fixed["asset_content_type"],
            "provenance": fixed["asset_provenance"],
            "depicts_identifiable_person": depicts,
        }
        if consent_ref and depicts:
            asset["consent_ref"] = consent_ref
        assets.append(asset)

    # ---- deliverable
    aspects = (nr.get("delivery") or {}).get("aspect_ratios") or []
    if not aspects:
        raise DerivationError(Refusal.SCHEMA_VIOLATION, f"case {case_id!r} names no aspect ratio", case_id=case_id)
    aspect = _PARENTHETICAL.sub("", str(aspects[0])).strip()
    aspect = (kind_map.get("aspect_aliases") or {}).get(aspect, aspect)

    deliverable = {
        "kind": kind,
        "operation": binding_row["requested_operation"],
        "modality": binding_row["modality"],
        "aspect": aspect,
        "count": int(((nr.get("deliverable_set") or {}).get("cardinality")) or 1),
    }
    subject = _subject(nr, entities)
    if subject:
        deliverable["subject"] = subject
    if binding_row["modality"] == "video":
        temporal = nr.get("temporal_structure") or {}
        seconds = temporal.get("duration_seconds")
        if seconds is None:
            raise DerivationError(Refusal.SCHEMA_VIOLATION, f"video case {case_id!r} states no duration_seconds", case_id=case_id)
        spoken = str(((nr.get("language_topology") or {}).get("spoken")) or "none")
        motion = {"seconds": seconds, "from": "accepted_still", "audio": spoken != "none"}
        if depends_on:
            motion["depends_on"] = depends_on
        deliverable["motion"] = motion

    blueprint_ref = case.get("blueprint_ref")
    blueprint_path = root / blueprint_ref if blueprint_ref else None
    if not blueprint_path or not blueprint_path.is_file():
        raise DerivationError(Refusal.PLANNER_FIXTURE_MISSING, f"case {case_id!r} names no blueprint on disk", case_id=case_id)

    brief = {"text": request["text"], "market": fixed["market"]}
    if request.get("language"):
        brief["language"] = request["language"]

    job = {
        "job_id": f"{fixed['job_id_prefix']}{case_id.lower()}",
        "customer_ref": f"{fixed['customer_ref_prefix']}{str(case.get('lane') or family).lower()}",
        "submitted_by": fixed["submitted_by"],
        "brief": brief,
        "deliverable_request": deliverable,
        "policy_profile": profile or fixed["policy_profile"],
        "retention": {"policy_ref": fixed["retention_policy_ref"]},   # delete_after_days: profile default via intake
    }
    if strings:
        job["exact_text_strings"] = strings
    if assets:
        job["reference_assets"] = assets

    job["_provenance"] = {
        "source_pool": SOURCE_POOL,
        "case_id": case_id,
        "case_family": family,
        "freeze_package": doc.get("package"),
        "freeze_base": doc.get("base"),
        "blueprint_ref": blueprint_ref,
        "blueprint_sha256": _sha_file(blueprint_path),
        "test_cases_sha256": _sha_file(test_cases_path),
        "tool": "runtime/tools/brief_from_stage_a_case.py",
        "tool_sha256": _sha_file(Path(__file__)),
        "kind_map_sha256": _sha_file(KIND_MAP),
        "kind_basis": f"{KIND_MAP.name}: family {family} -> {kind}; operation/modality from KIND-NR-BINDING row",
        "case_nr_operation": nr.get("requested_operation"),
        "case_nr_modality": nr.get("modality"),
        "binding_agrees_with_case_nr": (nr.get("requested_operation") == binding_row["requested_operation"]
                                        and nr.get("modality") == binding_row["modality"]),
        "placement_default": bool(strings),
        "depicts_basis": depicts_basis,
        "consent_ref_added": bool(consent_ref),
        "depends_on_added": bool(depends_on),
        "motion_from_basis": ("accepted_still is the PRODUCTION-JOB-v1 default; the customer's request "
                              "names the still it follows" if "motion" in deliverable else None),
        "tool_choices": {k: v for k, v in fixed.items()},
    }
    return job


def _asset_role(asset: dict, entities: dict, kind_map: dict) -> tuple[str, str]:
    roles = kind_map.get("asset_role") or {}
    mapped = roles.get(asset.get("role"))
    if mapped == "by_entity_type":
        entity = entities.get(asset.get("applies_to")) or {}
        role = (kind_map.get("entity_type_role") or {}).get(entity.get("entity_type"), "other")
        return role, f"identity_reference applies_to {asset.get('applies_to')!r} ({entity.get('entity_type')})"
    if mapped:
        return mapped, f"{asset.get('role')} -> {mapped}"
    raise DerivationError(
        Refusal.SCHEMA_VIOLATION,
        f"supplied asset {asset.get('asset_id')!r} has Stage-A role {asset.get('role')!r} with no row in {KIND_MAP.name}",
        asset_id=asset.get("asset_id"), role=asset.get("role"),
    )


def _depicts(asset: dict, entities: dict, person_entities: list) -> tuple[bool, str]:
    """True iff the case's own entities say a person is in this asset: an identity reference whose
    entity is a person, or the photograph being operated on when the NR names any person entity
    (including one to be REMOVED — it is in the supplied picture)."""
    target = entities.get(asset.get("applies_to")) or {}
    if target.get("entity_type") == "person":
        return True, f"applies_to {asset.get('applies_to')!r} is a person entity"
    if asset.get("role") == "subject_of_operation" and person_entities:
        names = ", ".join(e.get("entity_id", "?") for e in person_entities)
        return True, f"subject_of_operation and the NR names person entities: {names}"
    return False, "no person entity applies to this asset"


def _subject(nr: dict, entities: dict) -> dict | None:
    """PRODUCTION-JOB-v1 subject: what the picture is OF, from the frozen NR's entities."""
    if nr.get("product_or_packshot_present"):
        for e in entities.values():
            if e.get("entity_type") == "product":
                return {"entity": "product", "entity_id": e.get("entity_id"),
                        "identity_invariants": list(e.get("identity_invariants") or [])}
    for e in entities.values():
        if e.get("entity_type") == "person" and e.get("role") == "hero":
            return {"entity": "person", "entity_id": e.get("entity_id"),
                    "identity_invariants": list(e.get("identity_invariants") or [])}
    return None


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="runtime.tools.brief_from_stage_a_case", description=__doc__)
    parser.add_argument("case_id")
    parser.add_argument("--out", default=None)
    parser.add_argument("--consent-ref", default=None, help="add this consent_ref to every asset that depicts a person")
    parser.add_argument("--depends-on", default=None, help="motion.depends_on: the job id of the accepted still")
    parser.add_argument("--profile", default=None, help="policy profile (default: the map's fixed value, dry)")
    args = parser.parse_args(argv)
    try:
        job = derive(args.case_id, consent_ref=args.consent_ref, depends_on=args.depends_on, profile=args.profile)
    except Refusal as refusal:
        print(f"REFUSED  {refusal}", file=sys.stderr)
        return 2
    text = json.dumps(json.loads(canonical_json(job)), ensure_ascii=False, indent=2) + "\n"
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
