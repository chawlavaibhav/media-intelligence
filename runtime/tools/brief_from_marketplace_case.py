"""Derive a PRODUCTION-JOB-v1 request from a marketplace demand case. Deterministic; reads only.

    python3 -m runtime.tools.brief_from_marketplace_case MKT-001 [--out runtime/fixtures/alpha-briefs/mkt-001.json]

Reads canon/research/marketplace-demand-v1/derived/marketplace-brief-bank-v1.yaml (read-only): the
case's customer_brief and its Normalized Request with per-field provenance.

WHY THIS TOOL EXISTS. The marketplace cases are what real buyers ask for, and the first one
(MKT-001, Upwork UW-008) is a talking-head avatar plus AI product B-roll. No deliverable kind of that
shape exists in runtime/contracts/DELIVERABLE-KINDS.yaml, and the Alpha-1 ruling (C-7) excludes
talking heads by name. The honest job therefore names the kind the buyer asked for —
`talking_head_ad` — and intake refuses it precisely: KIND_NOT_IN_REGISTRY under a profile that
allows every kind (dry), KIND_NOT_IN_PROFILE under alpha_human_release. The tool does not bend the
buyer's request into a kind the runtime happens to have.

The mapping of buyer brief to kind name lives in this file's KIND_BY_CASE table, one row per case
this tool covers; a case with no row is refused, never guessed. Fields the bank marks
`experiment_supplied_fixture` (language, brand kit, script exactness) are NOT written into the job
as customer statements; the bank's own provenance vocabulary is carried under `_provenance`.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from .. import paths
from ..errors import Refusal
from ..util import canonical_json, load_yaml

SOURCE_POOL = "marketplace_case"

# case_id -> (kind name the buyer's brief describes, the basis in the buyer's words)
KIND_BY_CASE = {
    "MKT-001": ("talking_head_ad",
                "buyer: 'Talking-head AI avatar plus AI-generated product B-roll' (UW-008). No registry kind of "
                "this shape; C-7 excludes 'talking heads' (POLICY-PROFILES alpha_human_release.excluded_by_ruling)"),
}

FIXED = {
    "job_id_prefix": "alpha-dry-",
    "customer_ref_prefix": "acct-marketplace-",
    "policy_profile": "dry",
    "retention_policy_ref": "alpha-1-default",
    "submitted_by": "brief_from_marketplace_case",
    "asset_content_type": "image/jpeg",
    "asset_provenance": "generated_stand_in",
}


def load_case(case_id: str, bank_path: Path | None = None) -> tuple[dict, Path]:
    path = Path(bank_path or paths.MARKETPLACE_BRIEF_BANK)
    doc = load_yaml(path) or {}
    for row in doc.get("cases", []):
        if row.get("case_id") == case_id:
            return row, path
    raise Refusal(Refusal.PLANNER_FIXTURE_MISSING, f"no marketplace case {case_id!r}", bank=str(path))


def _value(nr: dict, field: str):
    block = nr.get(field) or {}
    return block.get("value") if isinstance(block, dict) else None


def _provenance_of(nr: dict, field: str):
    block = nr.get(field) or {}
    return block.get("provenance") if isinstance(block, dict) else None


def derive(case_id: str, *, profile: str | None = None, bank_path: Path | None = None) -> dict:
    if case_id not in KIND_BY_CASE:
        raise Refusal(
            Refusal.KIND_NOT_IN_REGISTRY,
            f"marketplace case {case_id!r} has no kind row in brief_from_marketplace_case.KIND_BY_CASE; "
            "the tool does not guess a kind",
            case_id=case_id,
        )
    kind, kind_basis = KIND_BY_CASE[case_id]
    case, bank = load_case(case_id, bank_path)
    nr = case.get("normalized_request") or {}

    operation = _value(nr, "R01_requested_operation")
    modality = _value(nr, "R05_modality")
    delivery = _value(nr, "R15_delivery") or {}
    aspects = delivery.get("aspect_ratios") or []
    if not (operation and modality and aspects):
        raise Refusal(Refusal.SCHEMA_VIOLATION, f"case {case_id!r} lacks operation, modality or aspect", case_id=case_id)

    entities = {e.get("entity_id"): e for e in (_value(nr, "R06_entities") or [])}
    assets = []
    for a in _value(nr, "R02_supplied_assets") or []:
        entity = entities.get(a.get("applies_to")) or {}
        assets.append({
            "asset_id": a["asset_id"],
            "role": "product" if entity.get("entity_type") == "product" else "other",
            "sha256": hashlib.sha256(f"{FIXED['asset_provenance']}:{case_id}:{a['asset_id']}".encode("utf-8")).hexdigest(),
            "content_type": FIXED["asset_content_type"],
            "provenance": FIXED["asset_provenance"],
            "depicts_identifiable_person": entity.get("entity_type") == "person",
        })

    deliverable = {
        "kind": kind,
        "operation": operation,
        "modality": modality,
        "aspect": str(aspects[0]),
        "count": int(((_value(nr, "R04_deliverable_set") or {}).get("cardinality")) or 1),
    }
    temporal = _value(nr, "R12_temporal_structure") or {}
    speakers = _value(nr, "R11_speaker_topology") or {}
    if modality == "video" and temporal.get("duration_seconds") is not None:
        deliverable["motion"] = {
            "seconds": temporal["duration_seconds"],
            # an identity reference is supplied and an avatar presents: the clip is made from a
            # reference, not from an accepted still and not from bare text
            "from": "reference",
            "audio": bool(speakers.get("visible_speakers") or speakers.get("offscreen_voices")),
        }

    job = {
        "job_id": f"{FIXED['job_id_prefix']}{case_id.lower()}",
        "customer_ref": f"{FIXED['customer_ref_prefix']}{str(case.get('source_marketplace') or 'unknown').lower()}",
        "submitted_by": FIXED["submitted_by"],
        "brief": {"text": " ".join(str(case.get("customer_brief") or "").split())},
        "deliverable_request": deliverable,
        "policy_profile": profile or FIXED["policy_profile"],
        "retention": {"policy_ref": FIXED["retention_policy_ref"]},
    }
    if assets:
        job["reference_assets"] = assets

    job["_provenance"] = {
        "source_pool": SOURCE_POOL,
        "case_id": case_id,
        "source_marketplace": case.get("source_marketplace"),
        "source_record_id": case.get("source_record_id"),
        "bank": str(bank.relative_to(paths.ROOT)) if bank.is_relative_to(paths.ROOT) else str(bank),
        "bank_sha256": hashlib.sha256(bank.read_bytes()).hexdigest(),
        "tool": "runtime/tools/brief_from_marketplace_case.py",
        "tool_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "kind_basis": kind_basis,
        "expected_intake_outcome": {
            "dry": "KIND_NOT_IN_REGISTRY (deliverable_kinds_allowed is __all__; the registry has no such kind)",
            "alpha_human_release": "KIND_NOT_IN_PROFILE (kind not in deliverable_kinds_allowed; C-7 'talking heads')",
        },
        "field_provenance_from_bank": {
            f: _provenance_of(nr, f) for f in ("R01_requested_operation", "R02_supplied_assets", "R05_modality",
                                                "R06_entities", "R10_language_topology", "R11_speaker_topology",
                                                "R12_temporal_structure", "R15_delivery")
        },
        "omitted_as_fixtures": ["brief.language (R10 is experiment_supplied_fixture)",
                                "brief.market (no market recorded; buyer is Ukraine-based)",
                                "exact_text_strings (R08 absent)"],
        "motion_from_basis": "tool reading: identity reference supplied + avatar presents -> from: reference; not a buyer statement",
        "tool_choices": dict(FIXED),
    }
    return job


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="runtime.tools.brief_from_marketplace_case", description=__doc__)
    parser.add_argument("case_id")
    parser.add_argument("--out", default=None)
    parser.add_argument("--profile", default=None)
    args = parser.parse_args(argv)
    try:
        job = derive(args.case_id, profile=args.profile)
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
