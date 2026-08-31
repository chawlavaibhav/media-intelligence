"""REP-06 (runtime half) section-completeness checker.

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

Grep-based checks over canon/packs/COMPILED-PACK-CONTRACT-v0.1.md:

  1. The runtime disposition table names every file in the commit-8115400 tree diff
     (must be exactly 25 files, matching `git show 8115400 --stat`) plus every file
     under canon/context/, each in exactly one table row carrying exactly one
     disposition token from {KEEP, SALVAGE, SUPERSEDE, FREEZE, RESTATE}.
  2. The contract header carries PROPOSED status, a Controller-decision statement,
     and the CONTROL-STATE governance pointer.
  3. The contract states the required runtime content: break-even arithmetic
     (uncached and cached variants), the ~45K per-request cold-case ceiling, the
     UNCOMMITTED/Anthropic-priced marker, the cache-shaping requirements, the
     union fallback for uncertain classification, and the audio coverage-gap rule.
  4. Nothing under coordination/, eval/, governance/, shared/, history/, verify/
     is modified in the working tree (git status check).

Run either way; exit status is the fact:

    python3 tests/check_rep06_runtime_sections.py
    python3 -m unittest tests.check_rep06_runtime_sections
"""
import re
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT = REPO_ROOT / "canon/packs/COMPILED-PACK-CONTRACT-v0.1.md"
COMMIT = "8115400"
TOKENS = ("KEEP", "SALVAGE", "SUPERSEDE", "FREEZE", "RESTATE")
FROZEN_DIRS = ("coordination/", "eval/", "governance/", "shared/", "history/", "verify/")

REQUIRED_STRINGS = [
    "PROPOSED",
    "no Controller decision adopts it",
    "coordination/CONTROL-STATE.md governs",
    "C = B + 5*O",            # uncached break-even
    "C = 10*(B + 5*O)",       # cached variant
    "47K",                    # uncached range low end at O=9-13K, B~2K
    "670K",                   # cached range high end
    "45K",                    # per-request cold-case ceiling
    "UNCOMMITTED",            # session arithmetic, pending Controller note
    "Anthropic",              # pricing basis; recompute for other providers
    "cache breakpoint",       # packs before volatile NR
    "byte-stable",            # serialization requirement
    "universal packs first",  # canonical pack order
    "union",                  # uncertain-classification fallback
    "coverage-gap notice",    # audio cell rule
    "system prompt",          # injection placement
    "trigger",                # NR->pack trigger rule
]


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=REPO_ROOT, check=True,
        capture_output=True, text=True).stdout


def files_at_8115400() -> list[str]:
    out = git("diff-tree", "--no-commit-id", "--name-only", "-r", COMMIT)
    return [line for line in out.splitlines() if line.strip()]


def files_under_canon_context() -> list[str]:
    root = REPO_ROOT / "canon/context"
    return sorted(str(p.relative_to(REPO_ROOT)) for p in root.rglob("*") if p.is_file())


def disposition_rows(text: str, path: str) -> list[str]:
    """Table rows whose first cell is exactly `path` (backtick-quoted)."""
    pattern = re.compile(r"^\|\s*`" + re.escape(path) + r"`\s*\|")
    return [line for line in text.splitlines() if pattern.search(line)]


def token_count(line: str) -> int:
    return sum(len(re.findall(r"\b" + t + r"\b", line)) for t in TOKENS)


def check() -> list[str]:
    problems: list[str] = []
    if not CONTRACT.is_file():
        return [f"missing contract: {CONTRACT}"]
    text = CONTRACT.read_text(encoding="utf-8")

    header = "\n".join(text.splitlines()[:12])
    for needle in ("PROPOSED", "no Controller decision adopts it",
                   "coordination/CONTROL-STATE.md governs"):
        if needle not in header:
            problems.append(f"contract header lacks {needle!r}")

    for needle in REQUIRED_STRINGS:
        if needle not in text:
            problems.append(f"contract lacks required string {needle!r}")

    listed = files_at_8115400()
    if len(listed) != 25:
        problems.append(f"expected 25 files at {COMMIT}, git names {len(listed)}")
    ctx = files_under_canon_context()
    if not ctx:
        problems.append("no files found under canon/context/")

    for path in listed + ctx:
        rows = disposition_rows(text, path)
        if len(rows) != 1:
            problems.append(f"{path}: expected exactly 1 disposition row, found {len(rows)}")
            continue
        n = token_count(rows[0])
        if n != 1:
            problems.append(f"{path}: expected exactly 1 disposition token, found {n}: {rows[0]}")

    status = git("status", "--porcelain")
    for line in status.splitlines():
        touched = line[3:].strip().strip('"')
        if touched.startswith(FROZEN_DIRS):
            problems.append(f"frozen path modified: {line.strip()}")

    return problems


class Rep06RuntimeSectionsTest(unittest.TestCase):
    def test_runtime_half_is_complete(self):
        problems = check()
        self.assertEqual(problems, [], "\n".join(problems))


if __name__ == "__main__":
    issues = check()
    for issue in issues:
        print(f"FAIL: {issue}")
    if not issues:
        print("PASS: REP-06 runtime-half section-completeness checks all hold "
              "(25 files at 8115400 + canon/context files each carry exactly one "
              "disposition; contract header and required content present; no frozen "
              "path modified)")
    raise SystemExit(1 if issues else 0)
