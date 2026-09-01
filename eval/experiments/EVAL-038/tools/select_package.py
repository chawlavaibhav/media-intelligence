#!/usr/bin/env python3
"""EVAL-038 — mechanical package selection for media generation (USD 0).

Picks which repetition of a lane's packages goes to media generation for a brief.
The rule is STRUCTURAL, not creative — models never judge themselves and this
session does not judge creative quality either (the Controller does, blind):

- v2 packages (haiku-packs): defects = missing required sections (the 12 v1 sections
  + DOCTRINE_DEVIATIONS), missing injected check-id lines in FAILURE_PREVENTION,
  missing typed VISUAL_SYSTEM subfields.
- v1 packages (sonnet-no-canon): defects = missing v1 sections.

Fewest defects wins; ties break to the LOWEST repetition number (deterministic,
committed before any package was read). Output: the chosen file plus the full
defect table, for the run record.
"""
import argparse
import pathlib
import re
import sys

import yaml

E38 = pathlib.Path(__file__).resolve().parents[1]

V1_SECTIONS = [
    "DELIVERABLE", "OBJECTIVE_INTERPRETATION", "CORE_CREATIVE_IDEA",
    "MESSAGE_AND_INFORMATION_HIERARCHY", "VISUAL_SYSTEM", "PRODUCTION_RECIPE",
    "GENERATION_PROMPTS", "DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS",
    "AUDIO_AND_EDIT", "FAILURE_PREVENTION", "HARD_CONSTRAINT_CHECK",
    "KNOWLEDGE_AND_WEBSITE_USE",
]
V2_SUBFIELDS = ["attention_order", "surface_finish_per_key_object",
                "implied_light_source", "placement_zone"]
PACK_CHECKS = {"composition_and_attention": [f"CA-D{i}" for i in range(1, 12)],
               "product_appearance": [f"PA-D{i}" for i in range(1, 11)]}

def defects(text, schema, injected_packs):
    out = []
    for s in V1_SECTIONS:
        if not re.search(rf"^(?:#{{1,4}}\s+)?(?:\*\*)?{s}(?:\*\*)?:?\s*$", text, re.M):
            out.append(f"missing section {s}")
    if schema == "v2":
        if not re.search(r"^(?:#{1,4}\s+)?(?:\*\*)?DOCTRINE_DEVIATIONS(?:\*\*)?:?\s*$",
                         text, re.M):
            out.append("missing section DOCTRINE_DEVIATIONS")
        for f in V2_SUBFIELDS:
            if f not in text:
                out.append(f"missing VISUAL_SYSTEM subfield {f}")
        for pack in injected_packs:
            for cid in PACK_CHECKS.get(pack, []):
                if not re.search(rf"{cid}\b", text):
                    out.append(f"missing check id {cid}")
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brief", required=True)
    ap.add_argument("--schema", choices=["v1", "v2"], required=True)
    ap.add_argument("files", nargs="+")
    args = ap.parse_args()
    manifest = yaml.safe_load((E38 / "payloads/PAYLOAD-MANIFEST.yaml").read_text())
    injected = manifest["briefs"][args.brief]["packs_injected_compiled_only"]
    scored = []
    for f in sorted(args.files):
        text = pathlib.Path(f).read_text()
        d = defects(text, args.schema, injected)
        scored.append((len(d), f, d))
        print(f"{f}: {len(d)} defects" + ("" if not d else " -> " + "; ".join(d)))
    scored.sort(key=lambda t: (t[0], t[1]))  # fewest defects, then lowest rep (R1<R2)
    print(f"SELECTED: {scored[0][1]}")

if __name__ == "__main__":
    main()
