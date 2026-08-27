#!/usr/bin/env python3
"""CANON-011 - build the prompt-ready bank from the brief bank.

The prompt-ready bank is a DERIVED VIEW, not a second source of truth. It is generated
from marketplace-brief-bank-v1.yaml so the two cannot drift apart, and
validate_marketplace_bank.py re-checks that every envelope still matches its case.

Run from the repository root, with PyYAML available:

    python3 canon/research/marketplace-demand-v1/derived/build_prompt_ready_bank.py

PyYAML is not installed system-wide on this machine. Create a local virtual environment
with pyyaml first; the repository handoffs already record this.
"""
import hashlib
import pathlib
import sys

import yaml

HERE = pathlib.Path(__file__).resolve().parent
BANK = HERE / "marketplace-brief-bank-v1.yaml"
OUT = HERE / "marketplace-prompt-ready-bank-v1.yaml"

HEADER = """\
# ===========================================================================
# CANON-011 - Marketplace-derived prompt-ready envelope bank v1
# ===========================================================================
# STATUS: PROPOSED WORKER OUTPUT. NOT FROZEN. GENERATED FILE - DO NOT HAND-EDIT.
#
# GENERATED from marketplace-brief-bank-v1.yaml by build_prompt_ready_bank.py.
# Edit the brief bank and regenerate. validate_marketplace_bank.py fails if this
# file and the brief bank disagree.
#
# WHAT AN ENVELOPE IS. A structured, model-neutral statement of what must be made,
# ready for a later adapter to turn into a real provider prompt. It is NOT a prompt.
# It names no model, no vendor and no production technique, and it never will - that
# translation belongs to a Production IR the project has not built.
#
# WHAT TO DO WITH IT. Read it with its case in the brief bank. The envelope says what
# must be true of the output; the case says which parts of that the customer asked for
# and which parts the benchmark supplied. Using an envelope without its case loses the
# provenance, and the provenance is the point.
#
# FIELDS ENDING `_provenance` mark where a value that looks like a customer requirement
# actually came from. Where an envelope value is a benchmark fixture, the field says so.
# ===========================================================================

"""


def main() -> int:
    if not BANK.exists():
        print(f"FAIL: {BANK} not found", file=sys.stderr)
        return 1
    raw = BANK.read_text()
    bank = yaml.safe_load(raw)

    doc = {
        "meta": {
            "bank_id": "marketplace_prompt_ready_bank",
            "version": "v1",
            "status": "PROPOSED_WORKER_OUTPUT_NOT_FROZEN",
            "task": "CANON-011",
            "generated_from": "canon/research/marketplace-demand-v1/derived/marketplace-brief-bank-v1.yaml",
            "generated_by": "canon/research/marketplace-demand-v1/derived/build_prompt_ready_bank.py",
            "source_bank_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
            "route_neutral": True,
            "model_specific_adapters_exist": False,
            "model_specific_adapters_note": (
                "Every envelope carries model_specific_fields: null. That is deliberate and it is "
                "the boundary of this task. Turning an envelope into a provider prompt requires a "
                "Production IR and a Capability Registry with rows in it; the project has neither."
            ),
            "envelope_count": len(bank["cases"]),
        },
        "envelopes": [
            {
                "case_id": c["case_id"],
                "source_marketplace": c["source_marketplace"],
                "source_record_id": c["source_record_id"],
                "runnable_now": c["runnable_now"],
                "stage_fit": c["stage_fit"],
                "envelope": c["prompt_ready_envelope"],
            }
            for c in bank["cases"]
        ],
    }

    body = yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100)
    OUT.write_text(HEADER + body)
    print(f"wrote {OUT.relative_to(HERE.parents[3])} with {len(doc['envelopes'])} envelopes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
