#!/usr/bin/env python3
"""Stage-form gate for /media-agency jobs.

    python3 .claude/skills/media-agency/tools/check_stage.py <job_dir> [--through N] [--json]

Reads `<job_dir>/stages/0N-<name>.json` for stages 1..N, validates each against
`forms/form-N-<name>.schema.json` (a JSON-Schema subset, stdlib only) and runs the
cross-form checks below. Prints COMPLETE or the list of missing / inconsistent fields
per stage. Exit 0 when every stage through N is complete, 2 otherwise.

What the gate checks: presence, traceability and consistency — a field is there, a
fact has a source, a claim id exists in the corpus, timings add up, the cap is not
exceeded, the checker is not the author. What the gate never checks: whether an
answer is good. Quality is the author's judgement and the customer's verdict; the
forms make both readable and measurable, they do not replace them.

`require_stages_complete(job_dir, through=4)` is the hook the dispatch tool calls
before the first paid call.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FORMS_DIR = HERE.parent / "forms"

STAGES = {
    1: "intent",
    2: "structure",
    3: "creative",
    4: "selection",
    5: "verification",
}


# --------------------------------------------------------------------------- schema subset
def _type_ok(value, typ):
    table = {
        "object": dict, "array": list, "string": str, "boolean": bool,
        "number": (int, float), "integer": int, "null": type(None),
    }
    if isinstance(typ, list):
        return any(_type_ok(value, t) for t in typ)
    py = table[typ]
    if typ in ("number", "integer") and isinstance(value, bool):
        return False
    return isinstance(value, py)


def validate(instance, schema, path="$", problems=None):
    """Validate `instance` against a JSON-Schema subset. Returns a list of problems."""
    problems = [] if problems is None else problems
    typ = schema.get("type")
    if typ and not _type_ok(instance, typ):
        problems.append(f"{path}: expected {typ}, got {type(instance).__name__}")
        return problems
    if "enum" in schema and instance not in schema["enum"]:
        problems.append(f"{path}: must be one of {schema['enum']}, got {instance!r}")
    if isinstance(instance, str):
        if "minLength" in schema and len(instance.strip()) < schema["minLength"]:
            problems.append(f"{path}: empty")
        if "pattern" in schema and not re.match(schema["pattern"], instance):
            problems.append(f"{path}: {instance!r} does not match {schema['pattern']}")
    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            problems.append(f"{path}: {instance} < minimum {schema['minimum']}")
        if "maximum" in schema and instance > schema["maximum"]:
            problems.append(f"{path}: {instance} > maximum {schema['maximum']}")
    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                problems.append(f"{path}.{key}: missing")
        if "minProperties" in schema and len(instance) < schema["minProperties"]:
            problems.append(f"{path}: needs at least {schema['minProperties']} entries")
        for key, sub in schema.get("properties", {}).items():
            if key in instance:
                validate(instance[key], sub, f"{path}.{key}", problems)
    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            problems.append(f"{path}: needs at least {schema['minItems']} items, has {len(instance)}")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            problems.append(f"{path}: at most {schema['maxItems']} items, has {len(instance)}")
        if "items" in schema:
            for i, item in enumerate(instance):
                validate(item, schema["items"], f"{path}[{i}]", problems)
    return problems


# --------------------------------------------------------------------------- corpus ids
_ID_CACHE: dict[str, set] = {}


def known_canon_ids(repo_root: Path | None) -> set | None:
    """Every `sk_id:` in canon/knowledge/current/** plus every compiled check id (XX-Dn).
    None when the corpus is not reachable (then ids are not checked)."""
    if repo_root is None:
        return None
    key = str(repo_root)
    if key in _ID_CACHE:
        return _ID_CACHE[key]
    ids: set = set()
    current = repo_root / "canon" / "knowledge" / "current"
    if not current.is_dir():
        return None
    sk = re.compile(r"^\s*(?:-\s*)?sk_id:\s*['\"]?([A-Za-z0-9_]+)", re.M)
    for f in current.rglob("source-knowledge.yaml"):
        try:
            ids.update(sk.findall(f.read_text(encoding="utf-8", errors="replace")))
        except OSError:
            pass
    comp = repo_root / "canon" / "compilation"
    chk = re.compile(r"\b([A-Z]{2}-D[0-9]{1,2})\b")
    if comp.is_dir():
        for f in comp.glob("PACK-*.yaml"):
            try:
                ids.update(chk.findall(f.read_text(encoding="utf-8", errors="replace")))
            except OSError:
                pass
    _ID_CACHE[key] = ids
    return ids


def find_repo_root(start: Path) -> Path | None:
    p = start.resolve()
    for cand in [p, *p.parents]:
        if (cand / "canon" / "knowledge").is_dir():
            return cand
    return None


# --------------------------------------------------------------------------- cross checks
def _ids(items, key="id"):
    return [it.get(key) for it in items if isinstance(it, dict)]


def cross_1(f1, ctx):
    p = []
    for a in f1.get("asks", []):
        if a.get("blocking") and not (a.get("answer") or "").strip():
            p.append(f"asks[{a.get('id')}]: blocking ask has no answer — nothing may be spent")
    for fl in f1.get("flags", []):
        if not fl.get("resolved") and not (fl.get("resolution") or "").strip():
            p.append(f"flags: '{fl.get('issue')}' unresolved — Stage 3 blocked (line 1.11)")
    if f1.get("deliverable", {}).get("type") == "film" and not f1.get("deliverable", {}).get("duration_s_band"):
        p.append("deliverable.duration_s_band: missing for a film")
    ctx["mandatory_ids"] = set(_ids(f1.get("mandatory", [])))
    ctx["acceptance_ids"] = set(_ids(f1.get("acceptance", [])))
    ctx["cap_usd"] = f1.get("cap", {}).get("usd")
    ctx["authors"].add(f1.get("author_session"))
    ctx["deliverable_type"] = f1.get("deliverable", {}).get("type")
    return p


def cross_2(f2, ctx):
    p = []
    for a in f2.get("assets", []):
        if a.get("status") == "have" and not (a.get("sha256") or "").strip():
            p.append(f"assets['{a.get('name')}']: status=have but no sha256 (line 2.5)")
    if f2.get("sufficient_to_proceed", {}).get("ok") is False:
        p.append(f"sufficient_to_proceed: blocked — {f2['sufficient_to_proceed'].get('blocking_dependency', 'no dependency named')}")
    ctx["authors"].add(f2.get("author_session"))
    ctx["claims"] = {c.get("text") for c in f2.get("permitted_claims", [])}
    return p


def cross_3(f3, ctx):
    p = []
    board = f3.get("board", {})
    beats = board.get("beats", [])
    ns = [b.get("n") for b in beats]
    if ns != sorted(ns) or len(set(ns)) != len(ns):
        p.append("board.beats: n must be unique and ascending")
    hero = board.get("hero_frame", {}).get("beat")
    if hero not in ns:
        p.append(f"board.hero_frame.beat={hero}: not a beat number (Gate 3 refuses to close without a numbered hero frame)")
    if board.get("kind") == "film":
        dur = board.get("duration_s")
        if dur is None:
            p.append("board.duration_s: missing for a film")
        prev_out = 0.0
        for b in beats:
            if "t_in" not in b or "t_out" not in b:
                p.append(f"board.beats[{b.get('n')}]: t_in/t_out missing for a film")
                continue
            if abs(b["t_in"] - prev_out) > 0.05:
                p.append(f"board.beats[{b.get('n')}]: t_in {b['t_in']} does not follow previous t_out {prev_out}")
            if b["t_out"] <= b["t_in"]:
                p.append(f"board.beats[{b.get('n')}]: t_out <= t_in")
            if b.get("clip_s", 0) > 0 and not (b.get("first_frame") or "").strip():
                p.append(f"board.beats[{b.get('n')}]: first_frame missing — the still must describe the state at t_in (Mokobara D1)")
            prev_out = b["t_out"]
        if dur is not None and beats and abs(prev_out - dur) > 0.1:
            p.append(f"board: beats end at {prev_out} s, duration_s is {dur}")
    covered = set()
    for b in beats:
        covered.update(b.get("mandatory_ids", []))
    missing = ctx.get("mandatory_ids", set()) - covered
    if missing:
        p.append(f"board: mandatory items not on any beat: {sorted(missing)} (line 3.7)")
    unknown = covered - ctx.get("mandatory_ids", set())
    if unknown and ctx.get("mandatory_ids"):
        p.append(f"board: beats cite unknown mandatory ids {sorted(unknown)}")
    deck = f3.get("copy_deck", {})
    strings, sources, placements = deck.get("strings", {}), deck.get("sources", {}), deck.get("placements", {})
    for sid in strings:
        if not (sources.get(sid) or "").strip():
            p.append(f"copy_deck.sources['{sid}']: every exact string needs a source (line 3.8 / 2.4)")
    for name, pl in placements.items():
        refs = pl.get("contents") or ([pl["string"]] if pl.get("string") else [])
        for r in refs:
            if r not in strings:
                p.append(f"copy_deck.placements['{name}']: references unknown string '{r}'")
        if board.get("kind") == "film" and ("t_in" not in pl or "t_out" not in pl):
            p.append(f"copy_deck.placements['{name}']: t_in/t_out missing")
    if f3.get("ask", {}).get("string_id") not in strings:
        p.append("ask.string_id: not in copy_deck.strings")
    review = f3.get("non_author_review", {})
    if review.get("by") and review.get("by") == f3.get("author_session"):
        p.append("non_author_review.by: is the author (line 3.13 requires a non-author)")
    ids = ctx.get("canon_ids")
    if ids is not None:
        cited = [c.get("id") for c in f3.get("canon_consulted", [])]
        for b in beats:
            cited.extend(b.get("canon", []))
        for c in cited:
            if c and c != "none" and c not in ids:
                p.append(f"canon id '{c}': not in the accepted corpus or a compiled pack — never invent one")
    ctx["authors"].add(f3.get("author_session"))
    ctx["beat_count"] = len(beats)
    return p


def cross_4(f4, ctx):
    p = []
    tests_named = " ".join(r.get("element", "") + " " + r["test"].get("what", "") for r in f4.get("risk_order", []) if isinstance(r.get("test"), dict))
    for r in f4.get("routes", []):
        if r.get("production_use_allowed") == "false":
            p.append(f"routes['{r.get('route_id')}']: production_use_allowed=false — not permitted")
        if r.get("production_use_allowed") == "manual_only" and r.get("route_id", "") not in tests_named:
            p.append(f"routes['{r.get('route_id')}']: manual_only cell with no micro-qualification test in risk_order (line 4.1)")
    cap = ctx.get("cap_usd")
    tot = f4.get("expected_spend", {}).get("total_usd")
    if cap is not None and tot is not None and tot > cap + 1e-9:
        p.append(f"expected_spend.total_usd {tot} exceeds the Stage 1 cap {cap} (line 4.9)")
    for ref in f4.get("references", []):
        if len(ref.get("refs", [])) > 4:
            p.append(f"references['{ref.get('for')}']: more than 4 references (line 4.7)")
    ctx["authors"].add(f4.get("author_session"))
    return p


def cross_5(f5, ctx):
    p = []
    authors = {a for a in ctx.get("authors", set()) if a}
    chk = f5.get("checker_session")
    if chk and (chk == f5.get("producer_session") or chk in authors):
        p.append("checker_session: is the producer or a form author — the check is not independent")
    lj_ids = set(_ids(f5.get("lj", [])))
    for d in f5.get("det", []):
        if d.get("result") == "fail":
            p.append(f"det['{d.get('id')}']: FAIL — a flagged file is not a deliverable")
        if d.get("result") in ("flag", "not_run") and d.get("covered_by_lj") not in lj_ids:
            p.append(f"det['{d.get('id')}']: {d.get('result')} with no LJ item covering it")
    for lj in f5.get("lj", []):
        if lj.get("judge") in (f5.get("producer_session"),):
            p.append(f"lj['{lj.get('id')}']: judged by the producer")
        if lj.get("result") == "pending":
            p.append(f"lj['{lj.get('id')}']: pending")
    att = f5.get("attempts", {})
    if att.get("all_reserved_before_settle") is False:
        p.append("attempts: not every attempt was reserved before settle")
    if att.get("usd_total") is not None and att.get("cap_usd") is not None and att["usd_total"] > att["cap_usd"] + 1e-9:
        p.append("attempts: spend exceeds cap")
    cv = f5.get("customer_verdict", {})
    if cv.get("outcome") in ("accepted", "rejected", "repair_requested"):
        if not (cv.get("verbatim") or "").strip():
            p.append("customer_verdict.verbatim: empty — record the customer's words unedited")
        scored = set(_ids(f5.get("acceptance_scored", [])))
        missing = ctx.get("acceptance_ids", set()) - scored
        if missing:
            p.append(f"acceptance_scored: Stage 1 statements not scored: {sorted(missing)}")
    if f5.get("release", {}).get("status") == "released" and cv.get("outcome") != "accepted":
        p.append("release: released without an accepted customer verdict (C-8)")
    return p


CROSS = {1: cross_1, 2: cross_2, 3: cross_3, 4: cross_4, 5: cross_5}


# --------------------------------------------------------------------------- driver
def load_schema(n: int) -> dict:
    return json.loads((FORMS_DIR / f"form-{n}-{STAGES[n]}.schema.json").read_text(encoding="utf-8"))


def form_path(job_dir: Path, n: int) -> Path:
    return job_dir / "stages" / f"0{n}-{STAGES[n]}.json"


def check_job(job_dir: Path, through: int = 5, repo_root: Path | None = None) -> dict:
    """Returns {stage: {"status": "COMPLETE"|"INCOMPLETE"|"MISSING", "problems": [...]}}."""
    ctx = {"authors": set(), "canon_ids": known_canon_ids(repo_root if repo_root else find_repo_root(job_dir))}
    out = {}
    for n in range(1, through + 1):
        path = form_path(job_dir, n)
        if not path.is_file():
            out[n] = {"status": "MISSING", "problems": [f"{path.name}: file not found"]}
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            out[n] = {"status": "INCOMPLETE", "problems": [f"{path.name}: invalid JSON — {e}"]}
            continue
        problems = validate(data, load_schema(n))
        problems += CROSS[n](data, ctx)
        out[n] = {"status": "COMPLETE" if not problems else "INCOMPLETE", "problems": problems}
    return out


def require_stages_complete(job_dir, through: int = 4) -> None:
    """Hook for the dispatch tool: refuse the first paid call unless stages 1..through are COMPLETE."""
    res = check_job(Path(job_dir), through)
    bad = {n: r for n, r in res.items() if r["status"] != "COMPLETE"}
    if bad:
        lines = [f"REFUSED: stage forms incomplete; nothing sent. Run check_stage.py {job_dir} --through {through}"]
        for n, r in bad.items():
            lines.append(f"  stage {n} {STAGES[n]}: {r['status']}")
            lines.extend(f"    - {x}" for x in r["problems"][:8])
        raise SystemExit("\n".join(lines))


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("job_dir")
    ap.add_argument("--through", type=int, default=5, choices=range(1, 6))
    ap.add_argument("--repo-root", default=None, help="repo root for canon id checks (default: walk up from job_dir)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    res = check_job(Path(a.job_dir), a.through, Path(a.repo_root) if a.repo_root else None)
    if a.json:
        print(json.dumps({str(k): v for k, v in res.items()}, indent=1))
    else:
        for n, r in res.items():
            print(f"stage {n} {STAGES[n]:<13} {r['status']}")
            for x in r["problems"]:
                print(f"    - {x}")
    return 0 if all(r["status"] == "COMPLETE" for r in res.values()) else 2


if __name__ == "__main__":
    sys.exit(main())
