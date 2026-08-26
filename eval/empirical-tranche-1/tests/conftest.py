"""Make the EMP-001 package modules importable from the tests.

The plan's illustrative snippet writes `from eval.empirical_tranche_1.budget_guard import ...`,
but the authoritative file structure in the same plan (and EVAL-012, and CONTROL-STATE) names the
directory `eval/empirical-tranche-1/`. A hyphen is not a legal Python identifier, so that dotted
import cannot address the frozen directory name. The directory name is authoritative; the import
form is not. This conftest resolves it exactly the way the Devanagari battery already does — the
package directory goes on sys.path and modules are imported by their own names.
"""
import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = PACKAGE_ROOT.parent.parent

for p in (str(PACKAGE_ROOT), str(PACKAGE_ROOT / "text_qualification"),
          str(PACKAGE_ROOT / "atex"), str(REPO_ROOT)):
    if p not in sys.path:
        sys.path.insert(0, p)
