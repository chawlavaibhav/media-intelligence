#!/usr/bin/env python3
"""Validate a production-learning case directory (schema PRODUCTION-LEARNING-CASE-v0).

Checks, in order: the required files exist and parse as YAML; OUTCOME carries the accepted asset's identity
(sha256, path, commit) whenever final_outcome is accepted; REVISION-TRACE uses only the eleven root-cause
classes and covers every version OUTCOME lists; HUMAN-VERDICTS is labelled chat-only or file-backed and covers
the same versions; ROUTE-OBSERVATIONS rows are directional with routing_authority none and an integer n;
ACCEPTED-TEMPLATE pacing values all carry evidence_scope; PROMOTION-QUEUE has its four sections; the two
TTAO clocks in TIME-AND-COST are labelled by source; and — when --pilot-ref names a commit that exists locally —
every `path @ commit` pair in EVIDENCE-MAP.md resolves with `git cat-file -e`, and the films' sha256 match.

Exit 0 on PASS, 1 with the problems listed otherwise. No network, no media decoded.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

import yaml

REQUIRED_FILES = ("README.md", "OUTCOME.yaml", "REVISION-TRACE.yaml", "TIME-AND-COST.yaml",
                  "ROUTE-OBSERVATIONS.yaml", "SYSTEM-DEFECTS.yaml", "HUMAN-VERDICTS.yaml",
                  "ACCEPTED-TEMPLATE.yaml", "PROMOTION-QUEUE.yaml", "EVIDENCE-MAP.md")
ROOT_CAUSE_CLASSES = {"creative_direction", "model_generation", "model_audio", "routing", "compositor",
                      "deterministic_qa", "pacing_edit", "product_fidelity", "commercial_positioning",
                      "infrastructure", "orchestration"}
VERDICTS = {"accept", "specific_repair", "rebuild_direction", "reject"}
QUEUE_SECTIONS = ("promoted_now", "candidate_patterns", "directional_only", "not_promoted")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
EVIDENCE_ROW = re.compile(r"`([^`@]+?)`\s*@\s*`([0-9a-f]{7,40})`")
FILM_ROW = re.compile(r"`([^`@]+?\.mp4)`\s*@\s*`([0-9a-f]{7,40})`\s*\|\s*`([0-9a-f]{64})`")


def _load(case: Path, name: str, problems: list):
    path = case / name
    if not path.exists():
        problems.append(f"missing file: {name}")
        return None
    if name.endswith(".md"):
        return path.read_text(encoding="utf-8")
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        problems.append(f"{name}: not valid YAML ({exc})")
        return None


def _check_outcome(o: dict, problems: list) -> list:
    for key in ("case_id", "class", "final_outcome", "accepted_by", "not_evidence_for", "versions_produced",
                "two_conclusions"):
        if key not in o:
            problems.append(f"OUTCOME.yaml: missing key {key}")
    if o.get("final_outcome") == "accepted":
        fa = o.get("final_asset") or {}
        for key in ("path", "commit", "sha256"):
            if not fa.get(key):
                problems.append(f"OUTCOME.yaml: final_outcome accepted needs final_asset.{key}")
        if fa.get("sha256") and not SHA256.match(str(fa["sha256"])):
            problems.append("OUTCOME.yaml: final_asset.sha256 is not a 64-hex sha256")
        if not o.get("accepted_version"):
            problems.append("OUTCOME.yaml: accepted needs accepted_version")
    tc = o.get("two_conclusions") or {}
    if "final_quality" not in tc or "pipeline_efficiency_time_to_accepted_outcome" not in tc:
        problems.append("OUTCOME.yaml: two_conclusions must carry final_quality and pipeline_efficiency_time_to_accepted_outcome")
    return [v.get("version") for v in (o.get("versions_produced") or [])]


def _check_trace(t: dict, versions: list, problems: list):
    seen = []
    for v in t.get("versions") or []:
        name = v.get("version")
        seen.append(name)
        for key in ("input_source", "generation_status", "assembly_status", "human_verdict", "defects",
                    "repair_succeeded", "cost_usd", "elapsed"):
            if key not in v:
                problems.append(f"REVISION-TRACE.yaml {name}: missing {key}")
        if v.get("human_verdict") not in VERDICTS:
            problems.append(f"REVISION-TRACE.yaml {name}: human_verdict {v.get('human_verdict')!r} not in {sorted(VERDICTS)}")
        for d in v.get("defects") or []:
            rc = d.get("root_cause_class")
            if rc not in ROOT_CAUSE_CLASSES:
                problems.append(f"REVISION-TRACE.yaml {name}: root_cause_class {rc!r} not in the eleven classes")
        el = v.get("elapsed") or {}
        if "source" not in el:
            problems.append(f"REVISION-TRACE.yaml {name}: elapsed needs a source")
    if seen != versions:
        problems.append(f"REVISION-TRACE.yaml versions {seen} != OUTCOME versions {versions}")


def _check_verdicts(h: dict, versions: list, problems: list):
    if h.get("evidence_class") not in ("chat_only_human_evidence", "file_backed_human_evidence"):
        problems.append("HUMAN-VERDICTS.yaml: evidence_class must be chat_only_human_evidence or file_backed_human_evidence")
    seen = [v.get("version") for v in h.get("verdicts") or []]
    if seen != versions:
        problems.append(f"HUMAN-VERDICTS.yaml versions {seen} != OUTCOME versions {versions}")
    for v in h.get("verdicts") or []:
        if v.get("verdict") not in VERDICTS:
            problems.append(f"HUMAN-VERDICTS.yaml {v.get('version')}: verdict {v.get('verdict')!r} not in {sorted(VERDICTS)}")


def _check_routes(r: dict, problems: list):
    for o in r.get("observations") or []:
        oid = o.get("id", "?")
        if o.get("evidence_class") != "directional_production_observation":
            problems.append(f"ROUTE-OBSERVATIONS.yaml {oid}: evidence_class must be directional_production_observation")
        if o.get("routing_authority") != "none":
            problems.append(f"ROUTE-OBSERVATIONS.yaml {oid}: routing_authority must be none")
        if not isinstance(o.get("n"), int):
            problems.append(f"ROUTE-OBSERVATIONS.yaml {oid}: n must be an exact integer count")
        if not o.get("context"):
            problems.append(f"ROUTE-OBSERVATIONS.yaml {oid}: context (the exact job) is required")


def _check_defects(s: dict, problems: list):
    for d in s.get("defects") or []:
        if d.get("class") not in ("media_model_failure", "pipeline_failure", "infrastructure_transient"):
            problems.append(f"SYSTEM-DEFECTS.yaml {d.get('id')}: class must be media_model_failure | pipeline_failure | infrastructure_transient")
        if not d.get("root_cause"):
            problems.append(f"SYSTEM-DEFECTS.yaml {d.get('id')}: root_cause required")


def _check_template(t: dict, problems: list):
    if t.get("not_a_canon_rule") is not True:
        problems.append("ACCEPTED-TEMPLATE.yaml: not_a_canon_rule must be true")
    if len(t.get("structure") or []) < 1:
        problems.append("ACCEPTED-TEMPLATE.yaml: structure is empty")
    for p in t.get("observed_pacing") or []:
        if p.get("evidence_scope") != "this_accepted_template":
            problems.append(f"ACCEPTED-TEMPLATE.yaml pacing {p.get('rule')!r}: evidence_scope must be this_accepted_template")


def _check_queue(q: dict, problems: list):
    for sec in QUEUE_SECTIONS:
        if sec not in q:
            problems.append(f"PROMOTION-QUEUE.yaml: missing section {sec}")
    for item in q.get("promoted_now") or []:
        if not item.get("where"):
            problems.append(f"PROMOTION-QUEUE.yaml {item.get('id')}: promoted_now needs `where` (the code surface)")
    for item in q.get("candidate_patterns") or []:
        if not item.get("promotion_condition"):
            problems.append(f"PROMOTION-QUEUE.yaml {item.get('id')}: candidate needs promotion_condition")


def _check_time_cost(tc: dict, problems: list):
    t = tc.get("time") or {}
    mech = t.get("time_to_accepted_outcome_mechanical") or {}
    est = t.get("time_to_accepted_outcome_human_estimate") or {}
    if "source" not in mech:
        problems.append("TIME-AND-COST.yaml: time_to_accepted_outcome_mechanical needs source")
    if est.get("source") != "human_estimate" or est.get("confidence") != "approximate":
        problems.append("TIME-AND-COST.yaml: time_to_accepted_outcome_human_estimate must be source human_estimate, confidence approximate")
    if isinstance(est.get("value"), (int, float)):
        problems.append("TIME-AND-COST.yaml: the human estimate must stay a labelled approximate phrase, not a number")
    c = tc.get("cost") or {}
    for key in ("verified_pilot_provider_cost_usd", "total_known_provider_cost_usd", "cost_per_accepted_outcome"):
        if key not in c:
            problems.append(f"TIME-AND-COST.yaml: cost.{key} required")
    cp = c.get("cost_per_accepted_outcome") or {}
    if cp.get("numerator_complete") is False and not cp.get("missing_components"):
        problems.append("TIME-AND-COST.yaml: an incomplete CpAO numerator must list missing_components")
    pc = tc.get("product_conclusion") or {}
    if pc.get("final_quality") != "SUCCESS" or pc.get("pipeline_efficiency") != "UNDERPERFORMED":
        problems.append("TIME-AND-COST.yaml: product_conclusion must state final_quality and pipeline_efficiency separately")


def _ref_exists(root: Path, ref: str) -> bool:
    r = subprocess.run(["git", "rev-parse", "--verify", "--quiet", ref + "^{commit}"], cwd=root,
                       capture_output=True, text=True)
    return r.returncode == 0


def _check_evidence_map(text: str, root: Path, pilot_dir: str, problems: list, notes: list):
    pairs = sorted(set(EVIDENCE_ROW.findall(text)))
    if not pairs:
        problems.append("EVIDENCE-MAP.md: no `path` @ `commit` rows found")
        return
    for path, commit in pairs:
        if not _ref_exists(root, commit):
            notes.append(f"EVIDENCE-MAP.md: commit {commit} not present locally; {path} not verified")
            continue
        for one in [p.strip() for p in path.split(",")]:
            r = subprocess.run(["git", "cat-file", "-e", f"{commit}:{pilot_dir}/{one}"], cwd=root,
                               capture_output=True, text=True)
            if r.returncode != 0:
                problems.append(f"EVIDENCE-MAP.md: {one} @ {commit} does not resolve")
    for path, commit, sha in FILM_ROW.findall(text):
        if not _ref_exists(root, commit):
            continue
        r = subprocess.run(["git", "cat-file", "blob", f"{commit}:{pilot_dir}/{path}"], cwd=root,
                           capture_output=True)
        if r.returncode != 0:
            problems.append(f"EVIDENCE-MAP.md: film {path} @ {commit} unreadable")
            continue
        got = hashlib.sha256(r.stdout).hexdigest()
        if got != sha:
            problems.append(f"EVIDENCE-MAP.md: film {path} @ {commit} sha256 {got[:12]}… != recorded {sha[:12]}…")


def run(case: Path, pilot_ref: str | None = None, pilot_dir: str = "pilots/upwork-intro-video-2026-09-14",
        root: Path | None = None, notes: list | None = None) -> list:
    case = Path(case)
    root = root or _repo_root(case)
    problems: list = []
    notes = notes if notes is not None else []
    docs = {name: _load(case, name, problems) for name in REQUIRED_FILES}
    if any(docs[n] is None for n in REQUIRED_FILES):
        return problems
    versions = _check_outcome(docs["OUTCOME.yaml"], problems)
    _check_trace(docs["REVISION-TRACE.yaml"], versions, problems)
    _check_verdicts(docs["HUMAN-VERDICTS.yaml"], versions, problems)
    _check_routes(docs["ROUTE-OBSERVATIONS.yaml"], problems)
    _check_defects(docs["SYSTEM-DEFECTS.yaml"], problems)
    _check_template(docs["ACCEPTED-TEMPLATE.yaml"], problems)
    _check_queue(docs["PROMOTION-QUEUE.yaml"], problems)
    _check_time_cost(docs["TIME-AND-COST.yaml"], problems)
    if pilot_ref:
        if _ref_exists(root, pilot_ref):
            _check_evidence_map(docs["EVIDENCE-MAP.md"], root, pilot_dir, problems, notes)
        else:
            notes.append(f"pilot ref {pilot_ref} not present locally; evidence resolution skipped")
    return problems


def _repo_root(start: Path) -> Path:
    for p in [start.resolve()] + list(start.resolve().parents):
        if (p / ".git").exists():
            return p
    return Path.cwd()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", required=True)
    ap.add_argument("--pilot-ref", default=None)
    ap.add_argument("--pilot-dir", default="pilots/upwork-intro-video-2026-09-14")
    a = ap.parse_args()
    notes: list = []
    problems = run(Path(a.case), a.pilot_ref, a.pilot_dir, notes=notes)
    for n in notes:
        print("NOTE  " + n)
    for p in problems:
        print("FAIL  " + p)
    print(f"{'PASS' if not problems else 'FAIL'}  {a.case}: {len(problems)} problem(s), {len(notes)} note(s)")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
