"""Run the committed dry Alpha battery and persist its evidence outside every sealed tree.

    python3 -m runtime.alpha.battery [--manifest runtime/battery/DRY-ALPHA-BATTERY-2026-09-14.yaml]
                                     [--out runtime/battery/results/2026-09-14] [--store DIR]

Sequential, one store, fixed timestamp from the manifest, so a run is reproducible and a motion
job can find the accepted still it depends on. Writes per-run SUMMARY.json plus the objects that
carry provenance (spec, route decision, execution manifest, gate report, loop record, outcome
event, template) and one SUMMARY.yaml over the battery. No socket is opened at any point.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

import yaml

from .. import paths
from .run import AlphaRunner

KEEP = ("SUMMARY.json", "02-spec.json", "04-route-decision.json", "05-execution-manifest.json",
        "08-gate-pre.json", "09-loop.json", "10-outcome-event.json", "10-outcome-event.unwritten.json",
        "11-template.json")


def _prepare_brief(entry: dict, tmp: Path) -> Path:
    src = Path(paths.ROOT) / entry["brief"]
    raw = json.loads(src.read_text(encoding="utf-8"))
    if entry.get("strip_provenance"):
        raw.pop("_provenance", None)
    for key, value in (entry.get("overrides") or {}).items():
        raw[key] = value
    out = tmp / f"{entry['id']}.json"
    out.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def run_battery(manifest_path: Path, out_dir: Path, store_root: Path) -> dict:
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    runner = AlphaRunner()
    tmp = Path(tempfile.mkdtemp(prefix="alpha-battery-briefs-"))
    rows = []
    for entry in manifest["runs"]:
        brief = _prepare_brief(entry, tmp)
        result = runner.run(brief, store_root=store_root, human_verdict=entry.get("human_verdict"),
                            post_draw=entry.get("post_draw") or "clean", at=manifest.get("at"),
                            consent_ref=entry.get("consent_ref"))
        dest = out_dir / entry["id"]
        os.makedirs(dest, exist_ok=True)
        for name in KEEP:
            src = Path(result.run_dir) / name
            if src.exists():
                shutil.copy(src, dest / name)
        for name in os.listdir(result.run_dir):
            if name.startswith("refusal-"):
                shutil.copy(Path(result.run_dir) / name, dest / name)
        route = result.objects.get("decision") or {}
        loop = result.objects.get("loop")
        spec = result.objects.get("spec") or {}
        rows.append({
            "id": entry["id"], "brief": entry["brief"], "job_id": result.job_id, "profile": result.profile,
            "exercises": entry.get("exercises"), "expect": entry.get("expect"),
            "observed": {
                "final_state": result.final_state,
                "refusal": result.refusal,
                "stages": [{"stage": s.stage, "status": s.status, "summary": s.summary} for s in result.stages],
                "route": {
                    "primary": (route.get("primary") or {}).get("route_key"),
                    "primary_surface": (route.get("primary") or {}).get("surface"),
                    "primary_evidence": (route.get("primary") or {}).get("evidence_status"),
                    "fallback": (route.get("fallback") or {}).get("route_key"),
                    "manual_route_required": route.get("manual_route_required"),
                    "manual_route_reason": route.get("manual_route_reason"),
                    "exclusions_applied": [{"route_key": e["route_key"], "effect": e.get("effect")} for e in route.get("exclusions_applied") or []],
                    "text_composed_from_cell": next((r.get("cell_selected") for r in (route.get("selection_basis") or {}).get("self_composed_requirements") or []), None),
                    "cost_envelope": route.get("cost_envelope"),
                } if route else None,
                "spec": {"spec_id": spec.get("spec_id"), "kind": (spec.get("deliverable") or {}).get("kind"),
                         "text_strategy": (spec.get("exact_text") or {}).get("strategy"),
                         "text_mechanism": (spec.get("exact_text") or {}).get("text_mechanism"),
                         "planner": (spec.get("blueprint") or {}).get("planner"),
                         "packs_injected": [p["pack_id"] for p in (spec.get("canon") or {}).get("packs_selected") or [] if p.get("compiled")],
                         "missing_domains": (spec.get("canon") or {}).get("missing_domains")} if spec else None,
                "gate_pre": {"verdict": loop.pre["verdict"], "blocking_failures": loop.pre["blocking_failures"]} if loop else None,
                "manifest": {
                    "attempts_rendered": len((result.objects.get("manifest") or {}).get("attempts") or []),
                    "primary_would_dispatch": [a["would_dispatch"] for a in (result.objects.get("manifest") or {}).get("attempts") or [] if a.get("slot") == "primary"],
                    "primary_would_dispatch_if_funded": [a.get("would_dispatch_if_funded") for a in (result.objects.get("manifest") or {}).get("attempts") or [] if a.get("slot") == "primary"],
                    "fallback_executable_if_triggered": [a.get("if_triggered_would_dispatch") for a in (result.objects.get("manifest") or {}).get("attempts") or [] if a.get("slot") == "fallback"],
                    "fallback_executable_if_triggered_if_funded": [a.get("if_triggered_would_dispatch_if_funded") for a in (result.objects.get("manifest") or {}).get("attempts") or [] if a.get("slot") == "fallback"],
                    "pool_liquidity_status": ((result.objects.get("manifest") or {}).get("pool_liquidity") or {}).get("status"),
                    "harness_refusals": sorted({a["refusal_reason"] for a in (result.objects.get("manifest") or {}).get("attempts") or [] if a.get("refusal_reason")}),
                } if result.objects.get("manifest") else None,
                "attempts": len(loop.attempts) if loop else None,
                "repairs": len(loop.repairs) if loop else None,
                "acceptance": loop.acceptance_state if loop else None,
                "event_id": (result.objects.get("event") or {}).get("event_id"),
                "template_id": (result.objects.get("template") or {}).get("template_id"),
            },
        })
    summary = {"schema": "DRY-ALPHA-BATTERY-RESULTS-v0", "manifest": str(manifest_path.relative_to(paths.ROOT)) if str(manifest_path).startswith(str(paths.ROOT)) else str(manifest_path),
               "at": manifest.get("at"), "profile": manifest.get("profile"), "runs": rows,
               "totals": {
                   "runs": len(rows),
                   "reached_intended_end_state_or_precise_refusal": sum(1 for r in rows if r["observed"]["final_state"] != "not_started"),
                   "crashes": sum(1 for r in rows if (r["observed"]["refusal"] or {}).get("code") in ("KeyError", "TypeError", "AttributeError", "ValueError", "AssertionError")),
                   "network": "none (no socket is ever opened; see runtime/tests/test_alpha_cli.py)",
                   "spend_usd": "0",
               }}
    os.makedirs(out_dir, exist_ok=True)
    (out_dir / "SUMMARY.yaml").write_text(yaml.safe_dump(summary, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8")
    return summary


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="runtime.alpha.battery", description=__doc__)
    ap.add_argument("--manifest", default=str(Path(paths.ROOT) / "runtime" / "battery" / "DRY-ALPHA-BATTERY-2026-09-14.yaml"))
    ap.add_argument("--out", default=str(Path(paths.ROOT) / "runtime" / "battery" / "results" / "2026-09-14"))
    ap.add_argument("--store", default=None)
    args = ap.parse_args(argv)
    store = Path(args.store or tempfile.mkdtemp(prefix="alpha-battery-store-"))
    summary = run_battery(Path(args.manifest), Path(args.out), store)
    for r in summary["runs"]:
        o = r["observed"]
        print(f"{r['id']:<50} {o['final_state']:<28} {(o['refusal'] or {}).get('code') or '-'}")
    print(f"\n{summary['totals']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
