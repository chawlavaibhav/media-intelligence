"""The acceptance contract: 3-6 statements, frozen before the first draw.

Two jobs in here.

`StyleGuard` is the build-time guard the Stage-A freeze runs over its own contracts, moved onto
the production path: a statement that names a route, a model, an arm, a cost or a rule id is a
build failure, not a warning. The model-name half of the vocabulary is derived from the routing
evidence map's route keys, so a provider added to the map is guarded that day.

`build` assembles the contract: the statements the job itself forces (the customer's exact
strings must read exactly; a supplied identity must survive) come first and are not the
reasoning pass's to decide; the reasoning pass adds what it saw in the brief; everything is
guarded; and the count is held inside the declared range or the compile fails loudly.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .. import paths
from ..errors import Refusal
from ..evidence import EvidenceMap
from ..util import load_yaml

_MASK = "█"


@dataclass(frozen=True)
class Violation:
    statement: str
    reason: str
    token: str


class StyleGuard:
    def __init__(self, style_path: str | Path | None = None, evidence: EvidenceMap | None = None):
        self.style = load_yaml(style_path or paths.ACCEPTANCE_STYLE) or {}
        self.evidence = evidence or EvidenceMap()
        self.openings = tuple(self.style.get("required_openings", []))
        self.min = self.style["count"]["min"]
        self.max = self.style["count"]["max"]
        self._patterns = [
            (row["name"], re.compile(row["pattern"], re.I))
            for row in self.style.get("banned_patterns", [])
        ]
        self._brand = (
            re.compile(r"\b(" + "|".join(re.escape(t) for t in self.evidence.brand_tokens()) + r")\b", re.I)
            if self.style.get("derive_model_name_tokens_from_evidence_map")
            else None
        )

    def inspect(self, statement: str, exempt_literals=()) -> Violation | None:
        if not isinstance(statement, str) or not statement.strip():
            return Violation(str(statement), "empty statement", "")
        if not statement.startswith(self.openings):
            return Violation(statement, f"a statement must open with one of {list(self.openings)}", statement[:24])
        # the customer's own copy is the artifact's content, never leakage: mask it before scanning
        scanned = statement
        for literal in sorted(exempt_literals, key=len, reverse=True):
            if literal:
                scanned = scanned.replace(literal, _MASK * min(len(literal), 8))
        for name, pattern in self._patterns:
            found = pattern.search(scanned)
            if found:
                return Violation(statement, f"banned by {name}", found.group(0))
        if self._brand:
            found = self._brand.search(scanned)
            if found:
                return Violation(statement, "names a model or provider from the routing evidence map", found.group(0))
        return None

    def check(self, statements, exempt_literals=()) -> None:
        for statement in statements:
            violation = self.inspect(statement, exempt_literals)
            if violation:
                raise Refusal(
                    Refusal.ACCEPTANCE_STYLE_VIOLATION,
                    f"acceptance statement rejected: {violation.reason}",
                    statement=violation.statement,
                    token=violation.token,
                )

    def check_count(self, statements) -> None:
        if not (self.min <= len(statements) <= self.max):
            raise Refusal(
                Refusal.ACCEPTANCE_COUNT_OUT_OF_RANGE,
                f"an acceptance contract carries {self.min} to {self.max} statements",
                got=len(statements),
                statements=list(statements),
            )


def derived_statements(job: dict, nr, style: dict) -> list:
    """The statements the JOB forces. No deliverable kind is named anywhere in here; each row
    fires on a fact about the job, so a new kind inherits them without a code change."""
    strings = [t["content"] for t in nr.text_requirements]
    identity_roles = list(nr.facets.get("identity_bound_roles") or [])
    conditions = {
        "exact_text_present": bool(strings),
        "identity_reference_present": bool(identity_roles),
        "supplied_asset_edit": bool(nr.facets.get("supplied_asset_present")) and nr.requested_operation != "generate",
    }
    out = []
    for row in style.get("derived_statements", []):
        if not conditions.get(row["when"], False):
            continue
        template = " ".join(row["template"].split())
        text = template.format(
            strings=_quote_list(strings),
            role=identity_roles[0] if identity_roles else "subject",
        )
        out.append(text)
    return out


def build(job: dict, nr, planner_statements, guard: StyleGuard) -> list:
    """Derived first, then what the reasoning pass saw, guarded, deduped, held in range."""
    exempt = [t["content"] for t in nr.text_requirements]
    derived = derived_statements(job, nr, guard.style)
    extra = [" ".join(str(s).split()) for s in (planner_statements or [])]

    guard.check(derived, exempt)
    guard.check(extra, exempt)  # a bad statement fails the compile; it is never silently dropped

    statements, seen = [], set()
    for statement in derived + extra:
        if statement in seen:
            continue
        seen.add(statement)
        statements.append(statement)
        if len(statements) == guard.max:
            break
    guard.check_count(statements)
    return statements


def _quote_list(strings) -> str:
    quoted = [f'"{s}"' for s in strings]
    if not quoted:
        return ""
    if len(quoted) == 1:
        return quoted[0]
    return ", ".join(quoted[:-1]) + " and " + quoted[-1]
