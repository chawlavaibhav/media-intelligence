"""Read-only import paths for the frozen packages harness-v2 builds on.

harness-v2 never edits `eval/empirical-tranche-1/`, `eval/pilot-substrate/` or
`eval/v1/harness/` (all three are byte-frozen by
`eval/empirical-tranche-1/protected-baselines.sha256`). It imports from them by
putting their directories on `sys.path`, exactly as `eval/pilot-substrate/video_route.py`
already does, and subclasses what it needs. Importing this module has no side effect
other than the path insertions; it opens no network connection, reads no key, and writes nothing.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent            # eval/harness-v2
EVAL_ROOT = HERE.parent                            # eval
REPO_ROOT = EVAL_ROOT.parent
EMP001 = EVAL_ROOT / "empirical-tranche-1"
PILOT = EVAL_ROOT / "pilot-substrate"
V1_HARNESS = EVAL_ROOT / "v1" / "harness"
FREEZE = EVAL_ROOT / "empirical-planning" / "STAGE-A-FREEZE-2026-09"
ROSTER = EVAL_ROOT / "empirical-planning" / "ROSTER-REFRESH-2026-09.yaml"
TEST_CASES = FREEZE / "TEST-CASES.yaml"
COST_TABLE = FREEZE / "COST-TABLE.yaml"
SEED_POLICY = FREEZE / "SEED-POLICY.yaml"
EVALUATOR_PLAN = FREEZE / "EVALUATOR-PLAN.yaml"
SCHEMAS = HERE / "schemas"
RUN_ROOT = EVAL_ROOT / "runs" / "harness-v2"      # gitignored runtime state (eval/runs/)

# Insert in REVERSE priority so that HERE ends up first: harness-v2's own `adapters/`
# package must shadow the frozen `eval/v1/harness/adapters.py` module of the same name.
for _p in (str(V1_HARNESS), str(PILOT), str(EMP001), str(HERE)):
    if _p in sys.path:
        sys.path.remove(_p)
    sys.path.insert(0, _p)
