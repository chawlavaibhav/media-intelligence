"""One command: a customer brief in, a PRODUCTION-SPEC plus the exact Canon payload out.

    python3 -m runtime.cli runtime/fixtures/briefs/mustard-oil-tin.json

Nothing between those two things is typed by a person. The command makes no network call: the
one reasoning pass runs from a recorded fixture, and a prompt with no fixture refuses and writes
the payload out rather than calling anything.
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

from . import paths
from .canon.packs import CanonCorpus
from .errors import Refusal
from .intake import Intake, JobStore
from .spec.compile import SpecCompiler
from .util import canonical_json, sha256_text


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="runtime.cli", description=__doc__)
    parser.add_argument("brief", help="path to a customer request (JSON)")
    parser.add_argument("--store", default=None, help="job store root (default: a throwaway directory)")
    parser.add_argument("--at", default=None, help="compiled_utc, for a reproducible run")
    parser.add_argument("--json", action="store_true", help="print the spec as JSON only")
    parser.add_argument("--canon", action="store_true", help="also print the exact injected Canon payload")
    parser.add_argument("--prompt-sha", action="store_true", help="print the reasoning-pass prompt fingerprint")
    args = parser.parse_args(argv)

    with open(args.brief, "r", encoding="utf-8") as fh:
        raw = json.load(fh)

    store_root = args.store or tempfile.mkdtemp(prefix="runtime-jobs-")
    try:
        intake = Intake(store=JobStore(store_root))
        result = intake.submit(raw)
        compiled = SpecCompiler().compile(result.job, compiled_utc=args.at)
    except Refusal as refusal:
        print(f"REFUSED  {refusal}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(compiled.spec, ensure_ascii=False, indent=2))
    else:
        print(render(compiled, result))
    if args.canon:
        print("\n" + "=" * 78 + "\nEXACT CANON PAYLOAD (sha256 "
              + compiled.spec["canon"]["injected_context_sha256"] + ")\n" + "=" * 78)
        print(compiled.canon_payload)
    if args.prompt_sha:
        print(f"\nreasoning-pass prompt sha256: {compiled.prompt_sha256}")
    return 0


def render(compiled, intake_result) -> str:
    spec = compiled.spec
    lines = []
    add = lines.append
    add(f"PRODUCTION-SPEC-v0  {spec['spec_id']}")
    add(f"  job            {spec['job_id']}  (new job: {intake_result.created})")
    add(f"  job_sha256     {spec['job_sha256']}")
    add(f"  compiled_utc   {spec['compiled_utc']}")
    add("")
    add(f"OBJECTIVE\n  {spec['objective']}")
    add("")
    deliverable = spec["deliverable"]
    add("DELIVERABLE")
    for key, value in deliverable.items():
        add(f"  {key:<16} {value}")
    add("")
    add("HARD CONSTRAINTS")
    for item in spec["hard_constraints"]:
        add(f"  - {item}")
    add("")
    add("EXACT TEXT")
    add(f"  strategy       {spec['exact_text']['strategy']}")
    add(f"  basis          {spec['exact_text']['strategy_basis']}")
    for item in spec["exact_text"]["strings"]:
        add(f"  {item['id']:<14} {item['content']}   [{item['script']}, {item['exactness']}]")
    add("")
    canon = spec["canon"]
    add("CANON (deterministic pack lookup)")
    for row in canon["packs_selected"]:
        mark = "injected " if row["compiled"] else "gap      "
        add(f"  {mark} {row['pack_id']:<30} {row['trigger']}")
    add(f"  injected_context_sha256  {canon['injected_context_sha256']}")
    add(f"  canon_gap                {canon['canon_gap']}")
    if canon.get("missing_domain"):
        add(f"  missing_domain           {canon['missing_domain']}")
    add("")
    add("CAPABILITY REQUIREMENTS (never a model name)")
    for row in spec["capability_requirements"]:
        level = f" [{row['level']}]" if row.get("level") else ""
        add(f"  - {row['capability']}{level}  mandatory={row['mandatory']}")
    if spec.get("identity_requirements"):
        add("")
        add("IDENTITY")
        add(f"  preserve      {', '.join(spec['identity_requirements']['preserve'])}")
        add(f"  decoy_check   {spec['identity_requirements']['decoy_check']}")
    for section in ("composition", "materials_and_light"):
        if spec.get(section):
            add("")
            add(section.upper())
            for key, value in spec[section].items():
                add(f"  {key:<28} {value}")
    add("")
    add("GATE REQUIREMENTS (pre-dispatch and post-draw, run by code)")
    for item in spec["gate_requirements"]:
        add(f"  - {item}")
    add("")
    add("ACCEPTANCE CONTRACT (frozen before the first draw; what the approver reads)")
    for item in spec["acceptance_contract"]:
        add(f"  - {item}")
    add("")
    add("DETERMINISTIC CHECKS (code, never shown to the approver)")
    for item in spec["deterministic_checks"]:
        add(f"  - {item}")
    add("")
    budget = spec["budget"]
    add("BUDGET (every number read from the job's policy profile)")
    add(f"  cost_ceiling_usd    {budget['cost_ceiling_usd']}")
    add(f"  max_provider_draws  {budget['max_provider_draws']}")
    add(f"  repair_allowance    {budget['repair_allowance']}")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
