"""One command: a customer brief in, a PRODUCTION-SPEC-v1 plus the exact Canon payload out.

    python3 -m runtime.cli runtime/fixtures/briefs/mustard-oil-tin.json
    python3 -m runtime.cli runtime/fixtures/alpha-briefs/img-text-02.json --store /tmp/jobs

Nothing between those two things is typed by a person. The command makes no network call: the
one reasoning pass runs from recorded material (a recorded fixture, or the frozen Stage-A blueprint
a `_provenance` block names) and a prompt with no recorded answer refuses and writes the payload out
rather than calling anything.

With `--store <dir>` the job is kept under <dir>/jobs/ and the spec is written as YAML to
<dir>/specs/<job_id>.spec.yaml — the file runtime/route/spec.py's load_spec() reads. `--out` names
another path for that YAML. This is the spec-only entry; the lead wires the full one-command run
(runtime/alpha/) after the lanes land.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

import yaml

from . import paths
from .errors import Refusal
from .intake import Intake, JobStore
from .spec.compile import SpecCompiler


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="runtime.cli", description=__doc__)
    parser.add_argument("brief", help="path to a customer request (JSON)")
    parser.add_argument("--store", default=None, help="job store root (default: a throwaway directory)")
    parser.add_argument("--out", default=None, help="write the spec YAML here (default: <store>/specs/<job_id>.spec.yaml)")
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
        compiled = SpecCompiler().compile(result.job, compiled_utc=args.at, provenance=result.provenance)
    except Refusal as refusal:
        print(f"REFUSED  {refusal}", file=sys.stderr)
        return 2

    spec_path = write_spec(compiled.spec, Path(args.out) if args.out else Path(store_root) / "specs" / f"{_safe(result.job_id)}.spec.yaml")

    if args.json:
        print(json.dumps(compiled.spec, ensure_ascii=False, indent=2))
    else:
        print(render(compiled, result))
        print(f"\nspec written    {spec_path}")
    if args.canon:
        print("\n" + "=" * 78 + "\nEXACT CANON PAYLOAD (sha256 "
              + compiled.spec["canon"]["injected_context_sha256"] + ")\n" + "=" * 78)
        print(compiled.canon_payload)
    if args.prompt_sha:
        print(f"\nreasoning-pass prompt sha256: {compiled.prompt_sha256}")
    return 0


def write_spec(spec: dict, path: Path) -> Path:
    """The spec as YAML, the shape runtime.route.spec.load_spec() reads. Written atomically."""
    os.makedirs(path.parent, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(yaml.safe_dump(spec, sort_keys=True, allow_unicode=True, width=120), encoding="utf-8")
    os.replace(tmp, path)
    return path


def _safe(job_id: str) -> str:
    return "".join(ch if (ch.isalnum() or ch in "-_.") else "_" for ch in job_id)


def render(compiled, intake_result) -> str:
    spec = compiled.spec
    lines = []
    add = lines.append
    add(f"{spec['schema']}  {spec['spec_id']}")
    add(f"  job            {spec['job_id']}  (new job: {intake_result.created})")
    add(f"  job_sha256     {spec['job_sha256']}")
    add(f"  compiled_utc   {spec['compiled_utc']}")
    add(f"  policy_profile {spec['policy_profile']}")
    if intake_result.provenance:
        prov = intake_result.provenance
        add(f"  provenance     {prov.get('source_pool')} {prov.get('case_id') or ''}".rstrip())
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
    add(f"  mechanism      {spec['exact_text']['text_mechanism']}")
    add(f"  basis          {spec['exact_text']['strategy_basis']}")
    for item in spec["exact_text"]["strings"]:
        add(f"  {item['id']:<14} {item['content']}   [{item['script']}, {item['exactness']}, {item['placement']}]")
    add("")
    add("ROUTE EXCLUSIONS (the one place a spec may name a route, in order to forbid it)")
    if not spec["route_exclusions"]:
        add("  none: no in-scope rule names a route to exclude")
    for row in spec["route_exclusions"]:
        add(f"  - {row['route_key']:<18} scope={row['scope']:<20} {row['basis']}")
    add("")
    canon = spec["canon"]
    add("CANON (deterministic pack lookup)")
    for row in canon["packs_selected"]:
        mark = "injected " if row["compiled"] else "gap      "
        add(f"  {mark} {row['pack_id']:<30} {row['trigger']}")
    add(f"  injected_context_sha256  {canon['injected_context_sha256']}")
    add(f"  canon_gap                {canon['canon_gap']}")
    if canon.get("missing_domains"):
        add(f"  missing_domains          {', '.join(canon['missing_domains'])}")
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
    bp = spec["blueprint"]
    add("BLUEPRINT (the reasoning pass, from recorded material only)")
    add(f"  planner        {bp['planner']}")
    add(f"  source_ref     {bp['source_ref']}")
    for slot, prompt in bp["generation_prompts"].items():
        shown = (prompt[:96] + "…") if prompt and len(prompt) > 96 else (prompt or "—")
        add(f"  prompt.{slot:<14} {shown}")
    add("")
    budget = spec["budget"]
    add("BUDGET (every number read from the job's policy profile)")
    add(f"  cost_ceiling_usd    {budget['cost_ceiling_usd']}")
    add(f"  max_provider_draws  {budget['max_provider_draws']}")
    add(f"  repair_allowance    {budget['repair_allowance']}")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
