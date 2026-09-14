"""Bind a recorded reasoning-pass response to the prompt it answers.

    python3 -m runtime.tools.bind_planner_fixture <brief.json> <response.json>

The prompt is built offline from the brief, its sha256 computed, and the pair written into
runtime/fixtures/planner/INDEX.yaml. Nothing is called. This exists so that changing the prompt's
wording is a re-bind, not a re-authoring of every fixture.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import yaml

from .. import paths
from ..canon.normalize import normalize
from ..canon.packs import CanonCorpus
from ..intake import Intake, JobStore
from ..spec import text_strategy as text_strategy_module
from ..spec.planner_seam import build_prompt


def prompt_sha_for(brief_path: str) -> str:
    with open(brief_path, "r", encoding="utf-8") as fh:
        raw = json.load(fh)
    intake = Intake(store=JobStore(tempfile.mkdtemp(prefix="runtime-bind-")))
    job = intake.submit(raw).job
    nr = normalize(job)
    canon = CanonCorpus().inject(nr)
    strategy = text_strategy_module.choose(nr)
    return build_prompt(job, nr, canon, strategy).sha256


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 2:
        print(__doc__)
        return 1
    brief_path, response_path = argv
    sha = prompt_sha_for(brief_path)
    index_path = Path(paths.PLANNER_FIXTURES) / "INDEX.yaml"
    index = yaml.safe_load(index_path.read_text(encoding="utf-8")) if index_path.exists() else None
    index = index or {"schema": "PLANNER-FIXTURE-INDEX-v0", "responses": {}}
    index.setdefault("responses", {})
    name = Path(response_path).name
    index["responses"][sha] = name
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(yaml.safe_dump(index, sort_keys=True, allow_unicode=True), encoding="utf-8")
    print(f"bound {name} -> {sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
