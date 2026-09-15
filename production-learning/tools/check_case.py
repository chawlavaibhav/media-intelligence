#!/usr/bin/env python3
"""Validate a production-learning case directory (schema PRODUCTION-LEARNING-CASE-v0).

The validator checks the STRUCTURE and HONESTY of a case — never the outcome of any particular job. A case
may be accepted, rejected or abandoned; it may have met, beaten or underperformed a baseline; it may or may
not have produced a reusable template; its evidence may live under any directory on any ref. What is fixed:

- OUTCOME names the outcome (accepted | rejected | abandoned). An accepted outcome needs the accepted asset's
  identity (path, commit, 64-hex sha256) and accepted_version; a rejected/abandoned one needs a reason instead.
  `two_conclusions` (quality, efficiency) are two labelled keys whose VALUES are the case's to state.
- An accepted case declares `template_status` (reusable_candidate | job_specific | none). ACCEPTED-TEMPLATE.yaml
  is required only for reusable_candidate; when present it is validated (not_a_canon_rule, non-empty structure,
  scoped pacing). A case with the file and no declaration is read as reusable_candidate (the UPWORK-INTRO-001 shape).
- REVISION-TRACE uses only the eleven root-cause classes and covers every version OUTCOME lists; HUMAN-VERDICTS is
  labelled chat-only or file-backed and covers the same versions; ROUTE-OBSERVATIONS rows are directional with
  routing_authority none and an integer n; PROMOTION-QUEUE has its four sections.
- TIME-AND-COST: one mechanical clock (`time_to_accepted_outcome_mechanical` or `time_to_outcome_mechanical`)
  with a `source`, or `value: null` + `reason`; a human estimate is optional and, if present, labelled and
  non-numeric; `cost.total_known_provider_cost_usd` is a number or `{value: null, reason}`; `cost_per_accepted_outcome`
  is required for accepted cases (an incomplete numerator lists missing_components) and may be absent or
  `{value: null, reason}` otherwise; `counts` carries paid_generation_attempts and human_review_cycles;
  `product_conclusion` states final_quality and pipeline_efficiency as two separate non-empty values.
- Evidence resolution. With no source ref at all the structural checks run and resolution is skipped with a NOTE.
  A source ref that is SUPPLIED (--source-ref, or the --pilot-ref alias) must resolve locally — otherwise FAIL,
  because a case whose raw evidence cannot be inspected is not validated. When it resolves: every `path` @ `commit`
  row in EVIDENCE-MAP.md resolves under --source-dir with `git cat-file -e`, and every `path` @ `commit` | `sha256`
  row's blob hashes to that sha256.
- Accepted-asset byte verification. For final_outcome accepted, once a source ref is supplied, OUTCOME.final_asset
  is read as a git blob at final_asset.commit — the path may be repo-root or relative to the source dir — and its
  sha256 must equal final_asset.sha256 (a well-formed but false hash FAILS), and EVIDENCE-MAP.md must carry a hashed
  row for that same normalised path and commit with the same sha256. --pilot-ref / --pilot-dir remain
  backwards-compatible aliases (the pilot directory is the default only for them).

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
                  "PROMOTION-QUEUE.yaml", "EVIDENCE-MAP.md")
TEMPLATE_FILE = "ACCEPTED-TEMPLATE.yaml"
OUTCOMES = ("accepted", "rejected", "abandoned")
TEMPLATE_STATUSES = ("reusable_candidate", "job_specific", "none")
ROOT_CAUSE_CLASSES = {"creative_direction", "model_generation", "model_audio", "routing", "compositor",
                      "deterministic_qa", "pacing_edit", "product_fidelity", "commercial_positioning",
                      "infrastructure", "orchestration"}
VERDICTS = {"accept", "specific_repair", "rebuild_direction", "reject"}
QUEUE_SECTIONS = ("promoted_now", "candidate_patterns", "directional_only", "not_promoted")
MECHANICAL_CLOCKS = ("time_to_accepted_outcome_mechanical", "time_to_outcome_mechanical")
LEGACY_PILOT_DIR = "pilots/upwork-intro-video-2026-09-14"
SHA256 = re.compile(r"^[0-9a-f]{64}$")
EVIDENCE_ROW = re.compile(r"`([^`@]+?)`\s*@\s*`([0-9a-f]{7,40})`")
HASHED_ROW = re.compile(r"`([^`@]+?)`\s*@\s*`([0-9a-f]{7,40})`\s*\|\s*`([0-9a-f]{64})`")


def _load(case: Path, name: str, problems: list, required: bool = True):
    path = case / name
    if not path.exists():
        if required:
            problems.append(f"missing file: {name}")
        return None
    if name.endswith(".md"):
        return path.read_text(encoding="utf-8")
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        problems.append(f"{name}: not valid YAML ({exc})")
        return None


def _nonempty(value) -> bool:
    return value is not None and str(value).strip() != ""


def _null_with_reason(value) -> bool:
    """`{value: null, reason: <why>}` — the honest shape for a figure that could not be established."""
    return isinstance(value, dict) and value.get("value") is None and _nonempty(value.get("reason"))


# ── OUTCOME ─────────────────────────────────────────────────────────────────

def _check_outcome(o: dict, has_template_file: bool, problems: list) -> tuple:
    for key in ("case_id", "class", "final_outcome", "not_evidence_for", "versions_produced", "two_conclusions"):
        if key not in o:
            problems.append(f"OUTCOME.yaml: missing key {key}")
    outcome = o.get("final_outcome")
    if outcome not in OUTCOMES:
        problems.append(f"OUTCOME.yaml: final_outcome {outcome!r} must be one of {OUTCOMES}")
    if outcome == "accepted":
        fa = o.get("final_asset") or {}
        for key in ("path", "commit", "sha256"):
            if not fa.get(key):
                problems.append(f"OUTCOME.yaml: final_outcome accepted needs final_asset.{key}")
        if fa.get("sha256") and not SHA256.match(str(fa["sha256"])):
            problems.append("OUTCOME.yaml: final_asset.sha256 is not a 64-hex sha256")
        if not o.get("accepted_version"):
            problems.append("OUTCOME.yaml: accepted needs accepted_version")
        if not _nonempty(o.get("accepted_by")):
            problems.append("OUTCOME.yaml: accepted needs accepted_by (the person)")
    elif outcome in ("rejected", "abandoned"):
        if not _nonempty(o.get("final_outcome_reason")):
            problems.append(f"OUTCOME.yaml: final_outcome {outcome} needs final_outcome_reason")
    tc = o.get("two_conclusions") or {}
    for key in ("final_quality", "pipeline_efficiency_time_to_accepted_outcome"):
        if not _nonempty(tc.get(key)):
            problems.append(f"OUTCOME.yaml: two_conclusions.{key} must be stated (its value is the case's own)")
    # template status: declared, or implied by the presence of the file (the pilot's shape)
    ts = o.get("template_status")
    if ts is None and has_template_file:
        ts = "reusable_candidate"
    if ts is None:
        if outcome == "accepted":
            problems.append("OUTCOME.yaml: an accepted case must declare template_status "
                            f"({' | '.join(TEMPLATE_STATUSES)}) or ship {TEMPLATE_FILE}")
        else:
            ts = "none"
    elif ts not in TEMPLATE_STATUSES:
        problems.append(f"OUTCOME.yaml: template_status {ts!r} must be one of {TEMPLATE_STATUSES}")
    if ts == "reusable_candidate" and not has_template_file:
        problems.append(f"OUTCOME.yaml: template_status reusable_candidate but {TEMPLATE_FILE} is absent")
    versions = [v.get("version") for v in (o.get("versions_produced") or [])]
    return versions, ts


# ── REVISION-TRACE / HUMAN-VERDICTS ─────────────────────────────────────────

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


# ── ROUTE-OBSERVATIONS / SYSTEM-DEFECTS / ACCEPTED-TEMPLATE / PROMOTION-QUEUE ──

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
        problems.append(f"{TEMPLATE_FILE}: not_a_canon_rule must be true")
    if len(t.get("structure") or []) < 1:
        problems.append(f"{TEMPLATE_FILE}: structure is empty")
    for p in t.get("observed_pacing") or []:
        if p.get("evidence_scope") != "this_accepted_template":
            problems.append(f"{TEMPLATE_FILE} pacing {p.get('rule')!r}: evidence_scope must be this_accepted_template")


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


# ── TIME-AND-COST ───────────────────────────────────────────────────────────

def _check_time_cost(tc: dict, outcome: str, problems: list):
    t = tc.get("time") or {}
    clocks = [k for k in MECHANICAL_CLOCKS if k in t]
    if not clocks:
        problems.append(f"TIME-AND-COST.yaml: time needs one mechanical clock ({' | '.join(MECHANICAL_CLOCKS)})")
    for k in clocks:
        mech = t.get(k) or {}
        if mech.get("value") is None and "value" in mech:
            if not _nonempty(mech.get("reason")):
                problems.append(f"TIME-AND-COST.yaml: {k} is null and must say why (reason)")
        elif "source" not in mech:
            problems.append(f"TIME-AND-COST.yaml: {k} needs source")
    est = t.get("time_to_accepted_outcome_human_estimate") or t.get("time_to_outcome_human_estimate")
    if est is not None:
        if est.get("source") != "human_estimate" or est.get("confidence") != "approximate":
            problems.append("TIME-AND-COST.yaml: a human time estimate must be labelled source human_estimate, confidence approximate")
        if isinstance(est.get("value"), (int, float)):
            problems.append("TIME-AND-COST.yaml: the human estimate must stay a labelled approximate phrase, not a number")
    c = tc.get("cost") or {}
    total = c.get("total_known_provider_cost_usd", "ABSENT")
    if total == "ABSENT":
        problems.append("TIME-AND-COST.yaml: cost.total_known_provider_cost_usd required (a number, or {value: null, reason})")
    elif isinstance(total, dict):
        if total.get("value") is None and not _nonempty(total.get("reason")):
            problems.append("TIME-AND-COST.yaml: cost.total_known_provider_cost_usd is null and must say why (reason)")
    elif not isinstance(total, (int, float)) and not (isinstance(total, str) and re.fullmatch(r"\d+(\.\d+)?", total)):
        problems.append("TIME-AND-COST.yaml: cost.total_known_provider_cost_usd must be a number or {value: null, reason}")
    cp = c.get("cost_per_accepted_outcome")
    if outcome == "accepted":
        if not isinstance(cp, dict):
            problems.append("TIME-AND-COST.yaml: an accepted case needs cost.cost_per_accepted_outcome")
        elif cp.get("numerator_complete") is False and not cp.get("missing_components"):
            problems.append("TIME-AND-COST.yaml: an incomplete CpAO numerator must list missing_components")
    elif cp is not None and not _null_with_reason(cp) and "value" in cp and cp.get("value") is None:
        problems.append("TIME-AND-COST.yaml: cost_per_accepted_outcome is null and must say why (reason)")
    counts = tc.get("counts") or {}
    for key in ("paid_generation_attempts", "human_review_cycles"):
        if not isinstance(counts.get(key), int):
            problems.append(f"TIME-AND-COST.yaml: counts.{key} must be an integer")
    pc = tc.get("product_conclusion") or {}
    for key in ("final_quality", "pipeline_efficiency"):
        if not _nonempty(pc.get(key)):
            problems.append(f"TIME-AND-COST.yaml: product_conclusion.{key} must be stated separately (its value is the case's own)")


# ── EVIDENCE-MAP ────────────────────────────────────────────────────────────

def _ref_exists(root: Path, ref: str) -> bool:
    r = subprocess.run(["git", "rev-parse", "--verify", "--quiet", ref + "^{commit}"], cwd=root,
                       capture_output=True, text=True)
    return r.returncode == 0


def _full_sha(root: Path, ref: str) -> str | None:
    r = subprocess.run(["git", "rev-parse", "--verify", "--quiet", ref + "^{commit}"], cwd=root,
                       capture_output=True, text=True)
    return r.stdout.strip() or None


def _blob(root: Path, commit: str, path: str) -> bytes | None:
    r = subprocess.run(["git", "cat-file", "blob", f"{commit}:{path}"], cwd=root, capture_output=True)
    return r.stdout if r.returncode == 0 else None


def _normalise(path: str, source_dir: str | None) -> str:
    """The evidence-relative form of a path: strip the source dir prefix when the path carries it."""
    path = path.strip().lstrip("./")
    if source_dir:
        prefix = source_dir.strip("/") + "/"
        if path.startswith(prefix):
            return path[len(prefix):]
    return path


def _check_final_asset_bytes(o: dict, text: str, root: Path, source_dir: str | None, problems: list, notes: list):
    """Byte-verify OUTCOME.final_asset: the blob at final_asset.commit hashes to final_asset.sha256, and
    EVIDENCE-MAP.md carries a hashed row for the same normalised path, commit and sha256."""
    fa = o.get("final_asset") or {}
    path, commit, sha = str(fa.get("path") or ""), str(fa.get("commit") or ""), str(fa.get("sha256") or "")
    if not (path and commit and sha):
        return                                                    # already reported by _check_outcome
    full = _full_sha(root, commit)
    if not full:
        problems.append(f"OUTCOME.yaml: final_asset.commit {commit} does not resolve locally; the accepted asset cannot be byte-verified")
        return
    rel = _normalise(path, source_dir)
    candidates = [path.strip().lstrip("./")]
    if source_dir:
        candidates.append(f"{source_dir.strip('/')}/{rel}")
    data = None
    for cand in dict.fromkeys(candidates):
        data = _blob(root, full, cand)
        if data is not None:
            break
    if data is None:
        problems.append(f"OUTCOME.yaml: final_asset.path {path} is not a blob at {commit} (tried {', '.join(dict.fromkeys(candidates))})")
        return
    got = hashlib.sha256(data).hexdigest()
    if got != sha:
        problems.append(f"OUTCOME.yaml: final_asset sha256 {got[:12]}… (blob at {commit}) != recorded {sha[:12]}…")
        return
    matched = False
    for row_path, row_commit, row_sha in HASHED_ROW.findall(text):
        row_full = _full_sha(root, row_commit)
        if _normalise(row_path, source_dir) == rel and row_full == full:
            matched = True
            if row_sha != sha:
                problems.append(f"EVIDENCE-MAP.md: hashed row for final_asset {rel} @ {commit} records {row_sha[:12]}… != OUTCOME {sha[:12]}…")
    if not matched:
        problems.append(f"EVIDENCE-MAP.md: no hashed row (`path` @ `commit` | `sha256`) for final_asset {rel} @ {commit}")
        return
    notes.append(f"final_asset byte-verified: {rel} @ {commit} sha256 {sha[:12]}… matches the blob and EVIDENCE-MAP.md")


def _check_evidence_map(text: str, root: Path, source_dir: str, problems: list, notes: list):
    pairs = sorted(set(EVIDENCE_ROW.findall(text)))
    if not pairs:
        problems.append("EVIDENCE-MAP.md: no `path` @ `commit` rows found")
        return
    prefix = f"{source_dir.rstrip('/')}/" if source_dir else ""
    for path, commit in pairs:
        if not _ref_exists(root, commit):
            notes.append(f"EVIDENCE-MAP.md: commit {commit} not present locally; {path} not verified")
            continue
        for one in [p.strip() for p in path.split(",")]:
            r = subprocess.run(["git", "cat-file", "-e", f"{commit}:{prefix}{one}"], cwd=root,
                               capture_output=True, text=True)
            if r.returncode != 0:
                problems.append(f"EVIDENCE-MAP.md: {one} @ {commit} does not resolve under {source_dir or '<repo root>'}")
    for path, commit, sha in HASHED_ROW.findall(text):
        if not _ref_exists(root, commit):
            continue
        r = subprocess.run(["git", "cat-file", "blob", f"{commit}:{prefix}{path}"], cwd=root, capture_output=True)
        if r.returncode != 0:
            problems.append(f"EVIDENCE-MAP.md: {path} @ {commit} unreadable")
            continue
        got = hashlib.sha256(r.stdout).hexdigest()
        if got != sha:
            problems.append(f"EVIDENCE-MAP.md: {path} @ {commit} sha256 {got[:12]}… != recorded {sha[:12]}…")


# ── driver ──────────────────────────────────────────────────────────────────

def run(case: Path, source_ref: str | None = None, source_dir: str | None = None, *,
        pilot_ref: str | None = None, pilot_dir: str | None = None,
        root: Path | None = None, notes: list | None = None) -> list:
    """Validate one case. `source_ref` / `source_dir` locate the raw evidence (any branch, any directory);
    `pilot_ref` / `pilot_dir` are the backwards-compatible aliases whose directory defaults to the pilot's.
    With no ref at all the structural checks still run and evidence resolution is skipped with a note; a ref that
    is supplied but does not resolve is a FAIL (fail closed)."""
    case = Path(case)
    root = root or _repo_root(case)
    problems: list = []
    notes = notes if notes is not None else []
    if pilot_ref and not source_ref:
        source_ref, source_dir = pilot_ref, (pilot_dir or source_dir or LEGACY_PILOT_DIR)
    docs = {name: _load(case, name, problems) for name in REQUIRED_FILES}
    template = _load(case, TEMPLATE_FILE, problems, required=False)
    if any(docs[n] is None for n in REQUIRED_FILES):
        return problems
    outcome_doc = docs["OUTCOME.yaml"]
    if source_dir is None and isinstance(outcome_doc, dict):
        source_dir = ((outcome_doc.get("evidence_source") or {}).get("dir")) or None
    versions, _template_status = _check_outcome(outcome_doc, template is not None, problems)
    _check_trace(docs["REVISION-TRACE.yaml"], versions, problems)
    _check_verdicts(docs["HUMAN-VERDICTS.yaml"], versions, problems)
    _check_routes(docs["ROUTE-OBSERVATIONS.yaml"], problems)
    _check_defects(docs["SYSTEM-DEFECTS.yaml"], problems)
    if template is not None:
        _check_template(template, problems)
    _check_queue(docs["PROMOTION-QUEUE.yaml"], problems)
    _check_time_cost(docs["TIME-AND-COST.yaml"], outcome_doc.get("final_outcome"), problems)
    accepted = outcome_doc.get("final_outcome") == "accepted"
    if source_ref:
        if not _ref_exists(root, source_ref):
            problems.append(f"source ref {source_ref} was supplied but does not resolve locally; the raw evidence "
                            "cannot be inspected, so this case is NOT validated (fetch the ref, or omit --source-ref "
                            "for a structural-only check)")
        elif source_dir is None:
            problems.append("evidence source directory unknown: pass --source-dir or declare OUTCOME.yaml evidence_source.dir")
        else:
            _check_evidence_map(docs["EVIDENCE-MAP.md"], root, source_dir, problems, notes)
            if accepted:
                _check_final_asset_bytes(outcome_doc, docs["EVIDENCE-MAP.md"], root, source_dir, problems, notes)
    else:
        notes.append("no --source-ref given; evidence resolution skipped (structural checks only)")
        if accepted:
            notes.append("final_asset not byte-verified (no source ref); the sha256 is checked for form only")
    return problems


def _repo_root(start: Path) -> Path:
    for p in [start.resolve()] + list(start.resolve().parents):
        if (p / ".git").exists():
            return p
    return Path.cwd()


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate a production-learning case (structure and honesty, not outcome).")
    ap.add_argument("--case", required=True)
    ap.add_argument("--source-ref", default=None, help="git ref/commit where the raw job evidence lives")
    ap.add_argument("--source-dir", default=None, help="directory of the raw evidence at that ref (e.g. pilots/<name> or <jobs-dir>/<id>); "
                                                        "defaults to OUTCOME.yaml evidence_source.dir")
    ap.add_argument("--pilot-ref", default=None, help="alias of --source-ref (legacy)")
    ap.add_argument("--pilot-dir", default=None, help=f"alias of --source-dir (legacy; defaults to {LEGACY_PILOT_DIR} with --pilot-ref)")
    a = ap.parse_args()
    notes: list = []
    problems = run(Path(a.case), a.source_ref, a.source_dir, pilot_ref=a.pilot_ref, pilot_dir=a.pilot_dir, notes=notes)
    for n in notes:
        print("NOTE  " + n)
    for p in problems:
        print("FAIL  " + p)
    print(f"{'PASS' if not problems else 'FAIL'}  {a.case}: {len(problems)} problem(s), {len(notes)} note(s)")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
