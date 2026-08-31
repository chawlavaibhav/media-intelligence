"""REP-06 (dossier half) section-completeness checker.

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

Grep-based checks over the four dossier deliverables:

  1. canon/candidates/canon-014/INSPECTION-RUNBOOK.md has one section per HOLD
     directory under canon/candidates/canon-014/ (must be exactly 18, verified by
     directory listing), each containing a file-identity block, exactly one
     inspection-or-replacement-copy verdict, and the four Audit Gate v0.2
     admission steps (i)-(iv); the two committed book-file hashes (berger MD5,
     sullivan SHA-256) appear verbatim.
  2. canon/findings/PROPOSED-EVAL-037-EVIDENCE-ANNOTATIONS.md contains six blocks
     A1-A6, each with a target path, a line anchor, and a runnable read-only
     recompute command; every recompute command is executed and must exit 0; the
     six itemised EVAL-037 lane spend figures sum to 8.372931 exactly.
  3. canon/findings/PROPOSED-EVAL-038-SUBSTITUTION-DESIGN.md contains the strings
     'maximum cost', a named model list, 'strips KNOWLEDGE_AND_WEBSITE_USE' and
     'failure-path'.
  4. Every dossier document header carries PROPOSED, the Controller-decision
     statement, and the CONTROL-STATE governance pointer
     (canon/planning/PROPOSED-G3B-EXPERT-ELICITATION-SPEC.md included).
  5. Nothing under coordination/, eval/, governance/, shared/, history/, verify/
     is modified in the working tree (git status check).

Run either way; exit status is the fact:

    python3 tests/check_rep06_dossier_sections.py
    python3 -m unittest tests.check_rep06_dossier_sections
"""
import re
import subprocess
import unittest
from decimal import Decimal
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = REPO_ROOT / "canon/candidates/canon-014"
RUNBOOK = CANDIDATES / "INSPECTION-RUNBOOK.md"
ANNOTATIONS = REPO_ROOT / "canon/findings/PROPOSED-EVAL-037-EVIDENCE-ANNOTATIONS.md"
EVAL038 = REPO_ROOT / "canon/findings/PROPOSED-EVAL-038-SUBSTITUTION-DESIGN.md"
G3B = REPO_ROOT / "canon/planning/PROPOSED-G3B-EXPERT-ELICITATION-SPEC.md"

VERDICT_TOKENS = ("INSPECT", "REPLACEMENT-COPY", "CLEAN-COPY-DIFF", "RE-FETCH-AND-PIN")
ADMISSION_STEPS = (
    "(i) author `visual-evidence-ledger.yaml` from the real",
    "(ii) fresh checkpoint",
    "(iii) v0.2 record with 5-file snapshot in",
    "(iv) validator pass",
)
HASH_BERGER_MD5 = "625aba06ceed728ba573dad60a52b3ed"
HASH_SULLIVAN_SHA256 = "b0a2630f368fb62c25f7f08d2135267e3ebe1e4165be253ce1056c391ec2095d"
SPEND_TOTAL = Decimal("8.372931")
FROZEN_DIRS = ("coordination/", "eval/", "governance/", "shared/", "history/", "verify/")
HEADER_NEEDLES = ("PROPOSED", "no Controller decision adopts it",
                  "coordination/CONTROL-STATE.md governs")
EVAL038_NEEDLES = ("maximum cost", "strips KNOWLEDGE_AND_WEBSITE_USE", "failure-path",
                   # the named model list
                   "claude-haiku-4-5-20251001", "gemma-4-31b-it")


def hold_dirs() -> list[str]:
    return sorted(p.name for p in CANDIDATES.iterdir() if p.is_dir())


def sections(text: str) -> list[tuple[str, str]]:
    """(heading, body) pairs for every '## ' heading."""
    out, heading, body = [], None, []
    for line in text.splitlines():
        if line.startswith("## "):
            if heading is not None:
                out.append((heading, "\n".join(body)))
            heading, body = line, []
        elif heading is not None:
            body.append(line)
    if heading is not None:
        out.append((heading, "\n".join(body)))
    return out


def check_runbook(problems: list[str]) -> None:
    if not RUNBOOK.is_file():
        problems.append(f"missing runbook: {RUNBOOK}")
        return
    text = RUNBOOK.read_text(encoding="utf-8")

    dirs = hold_dirs()
    if len(dirs) != 18:
        problems.append(f"expected 18 HOLD dirs under {CANDIDATES}, found {len(dirs)}")

    per_dir = {}
    for heading, body in sections(text):
        for d in dirs:
            if d in heading:
                per_dir.setdefault(d, []).append((heading, body))

    for d in dirs:
        got = per_dir.get(d, [])
        if len(got) != 1:
            problems.append(f"runbook: expected exactly 1 section for {d}, found {len(got)}")
            continue
        heading, body = got[0]
        if "File identity" not in body:
            problems.append(f"runbook {d}: no file-identity block")
        verdict_lines = [ln for ln in body.splitlines() if ln.startswith("**Verdict:**")]
        if len(verdict_lines) != 1:
            problems.append(f"runbook {d}: expected exactly 1 verdict line, "
                            f"found {len(verdict_lines)}")
        elif not any(t in verdict_lines[0] for t in VERDICT_TOKENS):
            problems.append(f"runbook {d}: verdict line carries no verdict token: "
                            f"{verdict_lines[0]}")
        for step in ADMISSION_STEPS:
            if step not in body:
                problems.append(f"runbook {d}: missing admission step {step!r}")
        if "canon/audit/records/" not in body:
            problems.append(f"runbook {d}: admission steps do not name canon/audit/records/")

    for h in (HASH_BERGER_MD5, HASH_SULLIVAN_SHA256):
        if h not in text:
            problems.append(f"runbook lacks committed hash {h}")


def annotation_blocks(text: str) -> dict[str, str]:
    out = {}
    matches = list(re.finditer(r"^### (A[1-6]) ", text, re.M))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else text.find("\n## ", m.end())
        out[m.group(1)] = text[m.start():end if end != -1 else len(text)]
    return out


def check_annotations(problems: list[str]) -> None:
    if not ANNOTATIONS.is_file():
        problems.append(f"missing annotations doc: {ANNOTATIONS}")
        return
    text = ANNOTATIONS.read_text(encoding="utf-8")

    blocks = annotation_blocks(text)
    if sorted(blocks) != [f"A{i}" for i in range(1, 7)]:
        problems.append(f"annotations: expected blocks A1..A6, found {sorted(blocks)}")

    for name, block in sorted(blocks.items()):
        target = re.search(r"\*\*Target:\*\* `([^`]+):(\d+)`", block)
        if not target:
            problems.append(f"annotations {name}: no `path:line` target anchor")
        elif not (REPO_ROOT / target.group(1)).is_file():
            problems.append(f"annotations {name}: target path {target.group(1)} not on disk")
        cmd = re.search(r"\*\*RECOMPUTE:\*\*\s*\n+```bash\n(.*?)```", block, re.S)
        if not cmd:
            problems.append(f"annotations {name}: no fenced RECOMPUTE command")
            continue
        run = subprocess.run(["bash", "-c", cmd.group(1)], cwd=REPO_ROOT,
                             capture_output=True, text=True)
        if run.returncode != 0:
            problems.append(f"annotations {name}: recompute exited {run.returncode}: "
                            f"{(run.stderr or run.stdout).strip()[:300]}")

    figures = re.findall(r"^\| EVAL-037 [^|*]+\| ([0-9]+\.[0-9]+) \|", text, re.M)
    if len(figures) != 6:
        problems.append(f"annotations: expected 6 itemised EVAL-037 lane figures, "
                        f"found {len(figures)}: {figures}")
    else:
        total = sum(Decimal(f) for f in figures)
        if total != SPEND_TOTAL:
            problems.append(f"annotations: lane figures sum to {total}, not {SPEND_TOTAL}")
    if str(SPEND_TOTAL) not in text:
        problems.append(f"annotations: total {SPEND_TOTAL} not stated verbatim")


def check_eval038(problems: list[str]) -> None:
    if not EVAL038.is_file():
        problems.append(f"missing EVAL-038 design doc: {EVAL038}")
        return
    text = EVAL038.read_text(encoding="utf-8")
    for needle in EVAL038_NEEDLES:
        if needle not in text:
            problems.append(f"EVAL-038 doc lacks required string {needle!r}")


def check_headers(problems: list[str]) -> None:
    for doc in (RUNBOOK, ANNOTATIONS, EVAL038, G3B):
        if not doc.is_file():
            problems.append(f"missing document: {doc}")
            continue
        header = "\n".join(doc.read_text(encoding="utf-8").splitlines()[:8])
        for needle in HEADER_NEEDLES:
            if needle not in header:
                problems.append(f"{doc.name}: header lacks {needle!r}")


def check_frozen(problems: list[str]) -> None:
    status = subprocess.run(["git", "status", "--porcelain"], cwd=REPO_ROOT,
                            check=True, capture_output=True, text=True).stdout
    for line in status.splitlines():
        touched = line[3:].strip().strip('"')
        if touched.startswith(FROZEN_DIRS):
            problems.append(f"frozen path modified: {line.strip()}")


def check() -> list[str]:
    problems: list[str] = []
    check_runbook(problems)
    check_annotations(problems)
    check_eval038(problems)
    check_headers(problems)
    check_frozen(problems)
    return problems


class Rep06DossierSectionsTest(unittest.TestCase):
    def test_dossier_half_is_complete(self):
        problems = check()
        self.assertEqual(problems, [], "\n".join(problems))


if __name__ == "__main__":
    issues = check()
    for issue in issues:
        print(f"FAIL: {issue}")
    if not issues:
        print("PASS: REP-06 dossier-half section-completeness checks all hold "
              "(18 runbook sections each with identity block, verdict and the four "
              "Audit Gate steps; both committed hashes verbatim; A1-A6 anchored and "
              "recomputed with exit 0; EVAL-037 lane spend sums to 8.372931 exactly; "
              "EVAL-038 required strings present; PROPOSED headers on all four docs; "
              "no frozen path modified)")
    raise SystemExit(1 if issues else 0)
