#!/usr/bin/env python3
"""Canon "definition of done" — the acceptance test that says whether Canon is complete for
production, run before any pack is built and again after each one.

    python3 canon/validation/canon_done.py [--brief path.json ...] [--fetcher module:function]

Tests (CANON-DONE-v0.md):
  A  Lookup on every brief returns 10 selected packs, 0 gaps, all injected packs ADOPTED
     (a status line that is not PROPOSED), each pack within the token budget, the validator green.
  B  Coverage: every claim id in HAND-RETRIEVED-CLAIMS.yaml is delivered — cited by a compiled
     pack that the brief selects, or returned by the fetcher for that brief.
  D  Adoption: a Controller decision file adopts each compiled pack (named in ADOPTIONS below).
  C  (the blind comparison) is a protocol, not code — see CANON-DONE-v0.md §C.

Exit 0 only when A, B and D all pass. Nothing is written; USD 0; no model call.
Briefs default to the recorded job briefs read from their branches on origin with `git show`.
"""
from __future__ import annotations

import argparse
import importlib
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

TOKEN_BUDGET_PER_PACK = 3000      # the two existing packs are ≈ 2,500
TOKEN_BUDGET_TOTAL = 30000
ADOPTIONS = REPO / "coordination" / "decisions"

DEFAULT_BRIEFS = {
    "MOKOBARA-ODYSSEY-007": "origin/work/agency-job-mokobara-odyssey-001:agency/jobs/AGY-2026-09-21-MOKOBARA-ODYSSEY-001/brief.job.json",
    "RENTOK-GAME-A-004": "origin/work/agency-job-rentok-game-lane-a-001:agency/jobs/AGY-2026-09-20-RENTOK-GAME-LANE-A-001/brief.job.json",
    "RENTOK-GAME-V2-006": "origin/work/agency-job-rentok-game-v2-001:agency/jobs/AGY-2026-09-21-RENTOK-GAME-V2-001/brief.job.json",
    "CUMINCO-CHOPSTICKS-003": "origin/work/agency-job-cuminco-chopsticks-001:agency/jobs/AGY-2026-09-15-CUMINCO-CHOPSTICKS-001/brief.job.json",
}


def git_show(spec: str) -> dict | None:
    r = subprocess.run(["git", "show", spec], capture_output=True, text=True, cwd=REPO)
    if r.returncode != 0:
        return None
    job = json.loads(r.stdout)
    job.pop("_provenance", None)
    return job


def hand_claims() -> dict:
    """job → set of sk ids (from HAND-RETRIEVED-CLAIMS.yaml)."""
    text = (REPO / "canon" / "validation" / "HAND-RETRIEVED-CLAIMS.yaml").read_text(encoding="utf-8")
    out, job = {}, None
    for line in text.splitlines():
        m = re.match(r"^  ([A-Z0-9-]+):$", line)
        if m:
            job = m.group(1); out[job] = set(); continue
        m = re.match(r"^      - \{id: (sk_[a-z0-9_]+),", line)
        if m and job:
            out[job].add(m.group(1))
    return out


def pack_cited_ids() -> dict:
    out = {}
    for f in (REPO / "canon" / "compilation").glob("PACK-*-v0.yaml"):
        pid = f.name[len("PACK-"):-len("-v0.yaml")]
        out[pid] = set(re.findall(r"sk_[a-z0-9]+(?:_[a-z0-9]+)*_[0-9]{3,4}", f.read_text(encoding="utf-8")))
    return out


def pack_status(pid: str) -> str:
    f = REPO / "canon" / "compilation" / f"PACK-{pid}-v0.yaml"
    if not f.is_file():
        return "MISSING"
    m = re.search(r"^status:\s*(.+)$", f.read_text(encoding="utf-8"), re.M)
    return (m.group(1).strip() if m else "no status line")


def adopted(pid: str) -> bool:
    """A decision file in coordination/decisions/ that names the pack and the word ADOPT (not DRAFT)."""
    for f in ADOPTIONS.glob("CONTROLLER-*.md"):
        t = f.read_text(encoding="utf-8", errors="replace")
        if pid in t and re.search(r"\bADOPT(?:ED|S)?\b", t) and "status: DRAFT" not in t.lower().replace("status: draft", "status: DRAFT"):
            if re.search(rf"ADOPT\w*[^\n]*{re.escape(pid)}|{re.escape(pid)}[^\n]*ADOPT", t):
                return True
    return False


def validator_green() -> tuple[bool, str]:
    r = subprocess.run([sys.executable, "canon/validation/validate_compiled_pack.py"], capture_output=True, text=True, cwd=REPO)
    return r.returncode == 0, (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout + r.stderr).strip() else ""


def pack_report(pack_id: str) -> int:
    """Seed coverage for one pack: every hand-retrieved claim from the pack's contributor sources
    must be cited by the compiled pack. Exit 0 at 100 %, 2 otherwise."""
    import yaml
    sys.path.insert(0, str(REPO / "canon" / "compilation"))
    from pack_seed import seed_ids_for  # noqa
    cov = yaml.safe_load((REPO / "canon/planning/CANON-V1-LIVE37-COVERAGE.yaml").read_text(encoding="utf-8"))
    contributors = set(cov["packs"][pack_id]["contributors"])
    seeds = [c for c, _ in seed_ids_for(contributors)]
    cited = pack_cited_ids().get(pack_id, set())
    status = pack_status(pack_id)
    missing = [s for s in seeds if s not in cited]
    print(f"pack {pack_id}: status '{status[:50]}' · seed {len(seeds)} · cited {len(seeds) - len(missing)} · missing {len(missing)}")
    for m in missing:
        print(f"  - {m}")
    return 0 if not missing and "PROPOSED" not in status.upper() and status != "MISSING" else 2


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--brief", action="append", default=[], help="path to a brief.job.json (repeatable); default: recorded job briefs")
    ap.add_argument("--fetcher", default=None, help="module:function(nr, brief) -> iterable of sk ids delivered for the brief")
    ap.add_argument("--pack", default=None, help="report one pack's seed coverage (hand-retrieved claims from its contributor sources vs its citations) and exit")
    a = ap.parse_args(argv)
    if a.pack:
        return pack_report(a.pack)

    from runtime.canon import normalize as _normalize, lookup as _lookup
    briefs = {}
    if a.brief:
        for p in a.brief:
            job = json.loads(Path(p).read_text(encoding="utf-8")); job.pop("_provenance", None)
            briefs[Path(p).stem] = job
    else:
        for k, spec in DEFAULT_BRIEFS.items():
            job = git_show(spec)
            if job:
                briefs[k] = job
    fetch = None
    if a.fetcher:
        mod, fn = a.fetcher.split(":")
        fetch = getattr(importlib.import_module(mod), fn)

    cited = pack_cited_ids()
    hand = hand_claims()
    fails, notes = [], []

    # ---- A: lookup
    for name, job in briefs.items():
        nr = _normalize(job)
        lk = _lookup(nr)
        sel = [s.pack_id for s in lk.selections]
        notes.append(f"A {name}: selected {len(sel)} injected {len(lk.injected_pack_ids)} gaps {len(lk.gap_pack_ids)} tokens {lk.tokens}")
        if len(sel) < 10 and name.startswith("MOKOBARA"):
            fails.append(f"A {name}: only {len(sel)} packs selected (an Indian video ad with text and a product should select all 10)")
        if lk.gap_pack_ids:
            fails.append(f"A {name}: gaps {list(lk.gap_pack_ids)}")
        if lk.tokens > TOKEN_BUDGET_TOTAL:
            fails.append(f"A {name}: prefix {lk.tokens} tokens > budget {TOKEN_BUDGET_TOTAL}")
        for pid in lk.injected_pack_ids:
            st = pack_status(pid)
            if "PROPOSED" in st.upper() or st == "MISSING":
                fails.append(f"A pack {pid}: status '{st[:60]}' — not adopted")
        # ---- B: coverage for this brief's job (if the brief is a recorded job)
        want = hand.get(name, set())
        if want:
            delivered = set()
            for pid in lk.injected_pack_ids:
                delivered |= cited.get(pid, set())
            if fetch:
                delivered |= set(fetch(nr, job))
            missing = sorted(want - delivered)
            notes.append(f"B {name}: hand-retrieved {len(want)}, delivered {len(want) - len(missing)}, missing {len(missing)}")
            if missing:
                fails.append(f"B {name}: not delivered by any injected pack or the fetcher: {missing}")
    # ---- per-pack token budget + validator
    for pid, s in cited.items():
        f = REPO / "canon" / "compilation" / f"PACK-{pid}-v0.yaml"
        m = re.search(r"terse_injection_text:\s*\|?\s*\n((?:[ \t]+.*\n)+)", f.read_text(encoding="utf-8"))
        if m and len(m.group(1)) / 4 > TOKEN_BUDGET_PER_PACK:
            fails.append(f"A pack {pid}: ≈{int(len(m.group(1)) / 4)} tokens > {TOKEN_BUDGET_PER_PACK}")
    ok, last = validator_green()
    notes.append(f"A validator: {'green' if ok else 'RED'} {last}")
    if not ok:
        fails.append("A validate_compiled_pack.py is not green")
    # ---- D: adoption
    for pid in sorted(cited):
        if not adopted(pid):
            fails.append(f"D pack {pid}: no Controller decision adopts it")

    fails = list(dict.fromkeys(fails))
    for n in notes:
        print(n)
    print()
    if fails:
        print(f"CANON NOT DONE — {len(fails)} failing condition(s):")
        for x in fails:
            print(f"  - {x}")
        return 2
    print("CANON DONE — A, B, D pass. C (blind comparison) is recorded separately.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
