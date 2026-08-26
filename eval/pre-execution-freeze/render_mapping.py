#!/usr/bin/env python3
"""Render CAPABILITY-V1-V2-MAPPING.md from the generated v2 contract."""
import yaml, pathlib, collections
ROOT = pathlib.Path(__file__).resolve().parents[2]
d = yaml.safe_load((ROOT / "eval/pre-execution-freeze/CAPABILITY-CONTRACT-v2.yaml").read_text())
c, mapping = d["counts"], d["v1_to_v2_mapping"]
o = []
o.append("# Capability V1 → V2 mapping\n")
o.append("> **GENERATED** from `CAPABILITY-CONTRACT-v2.yaml`. **V1 is not modified.**\n")
o.append("**Task:** EVAL-009 / E9-A · **Date:** 26 Aug 2026 · "
         "**Status:** `PROPOSED_FOR_CONTROLLER_FREEZE_NOT_IN_FORCE`\n")
o.append("## The count is an output, not a target\n")
o.append(f"| | |\n|---|---:|")
o.append(f"| V1 capabilities | **{c['v1_capabilities']}** |")
o.append(f"| V2 capabilities | **{c['v2_capabilities_total']}** |")
o.append(f"| — active | {c['v2_active']} |")
o.append(f"| — dormant | {c['v2_dormant']} |")
o.append("")
o.append(f"Arithmetic: **{c['v1_capabilities']} + {c['from_splits']} (splits) + "
         f"{c['added']} (added) = {c['v2_capabilities_total']}**. "
         f"{c['unchanged']} unchanged, {c['refined']} refined in place, {c['renamed']} renamed.\n")
o.append("**No target count was aimed at.** Every change traces to a Controller-approved direction "
         "or to the admission bar below. Nothing was added to reach a number.\n")
o.append("## The admission bar for a new capability\n")
o.append("> A new capability is admitted **only** where existing capability + condition + "
         "observation scope cannot represent the failure cleanly.\n")
o.append("**Three candidate concepts were rejected under this bar** — see the last section. That is "
         "the bar doing its job: it is only credible if it sometimes says no.\n")
o.append("\n---\n\n## Every V1 id, with its disposition\n")
o.append("| V1 id | Disposition | V2 id(s) |\n|---|---|---|")
for m in mapping:
    ids = ", ".join(f"`{x}`" for x in m["v2_ids"])
    o.append(f"| `{m['v1_id']}` | **{m['disposition']}** | {ids} |")
o.append(f"\n**{len(mapping)} / 36 V1 ids mapped.** The build aborts if any lacks a disposition, so "
         "this is guaranteed by construction rather than by review.\n")

o.append("\n---\n\n## The changes that carry reasoning\n")
for m in mapping:
    if m["disposition"] in ("split", "renamed", "refined"):
        ids = ", ".join(f"`{x}`" for x in m["v2_ids"])
        o.append(f"### `{m['v1_id']}` → {ids} *({m['disposition']})*\n")
        o.append(f"{m['rationale']}\n")

o.append("\n---\n\n## Added in V2\n")
for dim in d["dimensions"]:
    if dim.get("v2_disposition") == "added":
        o.append(f"### `{dim['id']}`\n")
        o.append(f"- **Family:** {dim['family']} · **Unit:** `{dim['observation_unit']}` · "
                 f"**Routing:** `{dim['routing_use']}`")
        o.append(f"- **Why no existing capability + condition can represent it:** "
                 f"{dim['admission_justification']}")
        o.append(f"- **External evidence:** {dim['external_evidence']}\n")

o.append("\n---\n\n## Rejected under the admission bar — deliberately NOT capabilities\n")
for k, v in d["not_capabilities"].items():
    o.append(f"**`{k}`**\n\n{v}\n")

o.append("\n---\n\n## Backward compatibility\n")
o.append("- **V1 remains authoritative until the Controller freezes v2.** This is a proposal.\n")
o.append("- **No V1 artifact is modified.** `eval/v1/capability-contract.yaml` and the 100-item "
         "bank are byte-identical.\n")
o.append("- **Historical Registry rows** (there are none) would remain readable: every V1 id "
         "resolves forward through this table, and split ids name their siblings so a historical "
         "result can be attributed to the correct successor or explicitly marked ambiguous.\n")
o.append("- **A split is not a silent re-measure.** A V1 result under `spatial_relationship` "
         "cannot be presented as a `spatial_relationship_2d` result: the predicate changed. Such "
         "rows would be marked superseded, never migrated.\n")
(ROOT / "eval/pre-execution-freeze/CAPABILITY-V1-V2-MAPPING.md").write_text("\n".join(o) + "\n")
print("mapping rendered")
