"""Case rows for the battery: TEST-CASES.yaml routes[] x repeats, each with its blueprint prompt.

The freeze package is read either from paths (working tree) or from a git revision
(`CaseBook.from_git("HEAD")`), because another role may be editing the working tree while this
harness runs; the manifest records which revision and sha256 it used.

ROUTE CATALOGUE. Since the EVAL-039A Auditor fixes (commit 0596aa2) `TEST-CASES.yaml ->
route_catalogue` is a pointer string ("see COST-TABLE.yaml -> route_catalogue"); the one record
per route_key lives in `COST-TABLE.yaml`. `CaseBook` therefore reads the catalogue from the
COST-TABLE at the same source (path or git revision) and records both sha256s.

REPEATS. A route row with `repeats: 0` (screen_status recorded_not_screened, README OQ-19) is
listed but contributes no call: `rows()` expands it to zero rows, `route_rows()` still lists it.
"""
from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path
from typing import Callable

import yaml

import hv2_paths

FREEZE_REL = "eval/empirical-planning/STAGE-A-FREEZE-2026-09"
_PROMPT_RE = re.compile(r"## 6\. generation_prompt[^\n]*\n\s*```text\n(.*?)\n```", re.S)


def extract_prompt(blueprint_md: str) -> str:
    m = _PROMPT_RE.search(blueprint_md)
    if not m:
        raise ValueError("blueprint has no '## 6. generation_prompt' ```text block")
    return m.group(1)


def git_show(rev: str, rel_path: str, repo_root: Path = hv2_paths.REPO_ROOT) -> bytes:
    return subprocess.run(["git", "show", f"{rev}:{rel_path}"], cwd=repo_root, capture_output=True, check=True).stdout


def git_sha(rev: str, repo_root: Path = hv2_paths.REPO_ROOT) -> str:
    return subprocess.run(["git", "rev-parse", rev], cwd=repo_root, capture_output=True, text=True, check=True).stdout.strip()


def resolve_catalogue(test_cases: dict, cost_table: dict | None) -> dict:
    """The route catalogue: inline in TEST-CASES if it is a mapping, else COST-TABLE's."""
    rc = test_cases.get("route_catalogue")
    if isinstance(rc, dict):
        return rc
    if cost_table is None or not isinstance(cost_table.get("route_catalogue"), dict):
        raise ValueError("TEST-CASES.yaml carries a route_catalogue pointer and no COST-TABLE.yaml was supplied")
    return cost_table["route_catalogue"]


class CaseBook:
    def __init__(self, test_cases: dict, blueprint_loader: Callable[[str], str], source: dict,
                 cost_table: dict | None = None):
        self.data = test_cases
        self.catalogue = resolve_catalogue(test_cases, cost_table)
        self.cases = test_cases["cases"]
        self._bp = blueprint_loader
        self.source = source
        self._prompts: dict[str, str] = {}

    # -- constructors ----------------------------------------------------------------------
    @classmethod
    def from_paths(cls, test_cases_path: Path | str = hv2_paths.TEST_CASES, freeze_dir: Path | str = hv2_paths.FREEZE,
                   cost_table_path: Path | str | None = None) -> "CaseBook":
        raw = Path(test_cases_path).read_bytes()
        freeze_dir = Path(freeze_dir)
        ct_path = Path(cost_table_path) if cost_table_path else freeze_dir / "COST-TABLE.yaml"
        ct_raw = ct_path.read_bytes() if ct_path.exists() else None

        def loader(ref: str) -> str:
            return (freeze_dir / ref).read_text(encoding="utf-8")
        return cls(yaml.safe_load(raw.decode("utf-8")), loader,
                   {"kind": "working_tree", "test_cases_path": str(test_cases_path),
                    "test_cases_sha256": hashlib.sha256(raw).hexdigest(),
                    "cost_table_path": str(ct_path) if ct_raw is not None else None,
                    "cost_table_sha256": hashlib.sha256(ct_raw).hexdigest() if ct_raw is not None else None},
                   cost_table=(yaml.safe_load(ct_raw.decode("utf-8")) if ct_raw is not None else None))

    @classmethod
    def from_git(cls, rev: str = "HEAD", repo_root: Path = hv2_paths.REPO_ROOT) -> "CaseBook":
        raw = git_show(rev, f"{FREEZE_REL}/TEST-CASES.yaml", repo_root)
        ct_raw = git_show(rev, f"{FREEZE_REL}/COST-TABLE.yaml", repo_root)

        def loader(ref: str) -> str:
            return git_show(rev, f"{FREEZE_REL}/{ref}", repo_root).decode("utf-8")
        return cls(yaml.safe_load(raw.decode("utf-8")), loader,
                   {"kind": "git", "rev": rev, "commit": git_sha(rev, repo_root),
                    "test_cases_path": f"{FREEZE_REL}/TEST-CASES.yaml", "test_cases_sha256": hashlib.sha256(raw).hexdigest(),
                    "cost_table_path": f"{FREEZE_REL}/COST-TABLE.yaml", "cost_table_sha256": hashlib.sha256(ct_raw).hexdigest()},
                   cost_table=yaml.safe_load(ct_raw.decode("utf-8")))

    # -- access -----------------------------------------------------------------------------
    def case(self, case_id: str) -> dict:
        for c in self.cases:
            if c["case_id"] == case_id:
                return c
        raise KeyError(case_id)

    def prompt_for(self, case_id: str) -> str:
        if case_id not in self._prompts:
            c = self.case(case_id)
            md = self._bp(c["blueprint_ref"])
            digest = hashlib.sha256(md.encode("utf-8")).hexdigest()
            if c.get("blueprint_sha256") and digest != c["blueprint_sha256"]:
                raise ValueError(f"{case_id}: blueprint sha256 {digest[:12]} != TEST-CASES {c['blueprint_sha256'][:12]}")
            self._prompts[case_id] = extract_prompt(md)
        return self._prompts[case_id]

    def route_rows(self, case_id: str | None = None) -> list[dict]:
        """One row per (case, route row) - before repeats are expanded."""
        out = []
        for c in self.cases:
            if case_id and c["case_id"] != case_id:
                continue
            for r in c["routes"]:
                cat = self.catalogue[r["route_key"]]
                out.append({
                    "case_id": c["case_id"], "item_id": r.get("item_id") or c["item_id"], "lane": c.get("lane"),
                    "route_key": r["route_key"], "route_id": r.get("route_id"), "surface": r.get("surface"),
                    "billing_pool": r.get("billing_pool"), "route_status": r.get("route_status"),
                    "arm": r.get("arm"), "params": dict(r.get("params") or {}),
                    "repeats": (1 if r.get("repeats") is None else int(r["repeats"])),   # 0 stays 0 (recorded_not_screened)
                    "screen_status": r.get("screen_status") or "screened",
                    "tranche": r.get("tranche"), "quantity": r.get("quantity"), "quantity_unit": r.get("quantity_unit"),
                    "price_status": r.get("price_status"), "unit_price": cat.get("unit_price"),
                    "conditional": bool(r.get("conditional")), "conditional_note": r.get("conditional"),
                    "conditions": c.get("conditions") or {}, "language": ((c.get("conditions") or {}).get("COND-LANGUAGE") or {}).get("language"),
                    "blueprint_ref": c.get("blueprint_ref"), "blueprint_sha256": c.get("blueprint_sha256"),
                    "reference_assets": c.get("reference_assets") or [],
                })
        return out

    def rows(self, case_id: str | None = None, with_prompt: bool = True) -> list[dict]:
        """One row per (case, route row, repeat_index 1..repeats)."""
        out = []
        for base in self.route_rows(case_id):
            prompt = self.prompt_for(base["case_id"]) if with_prompt else None
            for i in range(1, base["repeats"] + 1):
                out.append({**base, "repeat_index": i, "prompt": prompt})
        return out

    def row(self, case_id: str, route_key: str, arm: str | None = None, repeat_index: int = 1) -> dict:
        for r in self.rows(case_id):
            if r["route_key"] == route_key and (arm is None or r["arm"] == arm) and r["repeat_index"] == repeat_index:
                return r
        raise KeyError((case_id, route_key, arm, repeat_index))
