"""Result model, verdict and renderers for the gate (CANON-GATE-001 plan §C, Ruling 2).

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

Statuses: PASS (the tested clause holds), FAIL (it does not), NOT_MECHANISED (code cannot
test the line; reason mandatory), NOT_APPLICABLE (pack not selected or modality excludes the
check), NOT_RUN (mechanisable but an input is missing), ERROR (input unparsable — fails closed).

Verdict (Ruling 2): FAIL iff any row with blocking=True is FAIL, or any row is ERROR. A
non-blocking FAIL is printed as `FAIL (non-blocking)` and counted on the final line; it is
never folded into a pass count. A partial PASS always prints its clause in brackets.
"""
from __future__ import annotations

import enum
from dataclasses import dataclass, field

FAMILIES = ("doctrine", "limit", "dispatch", "infra")
GATES = ("pre_dispatch", "post_draw")
COVERAGES = ("full", "partial", "none")
GATE_LABEL = {"pre_dispatch": "pre-dispatch", "post_draw": "post-draw"}


class Status(enum.Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    NOT_MECHANISED = "NOT-MECHANISED"
    NOT_APPLICABLE = "NOT-APPLICABLE"
    NOT_RUN = "NOT-RUN"
    ERROR = "ERROR"


@dataclass(frozen=True)
class CheckResult:
    check_id: str
    family: str            # doctrine | limit | dispatch | infra
    gate: str              # pre_dispatch | post_draw
    status: Status
    coverage: str          # full | partial | none
    clause: str            # the literal clause tested (partial checks print it)
    source_text: str       # the committed pack `check` / limit line, verbatim
    detail: str            # reason (mandatory when not PASS) or evidence summary
    evidence: tuple = ()
    blocking: bool = False  # Ruling 2: only LIMIT-TEXT, DISPATCH-*, CA-D2 clause 2 block

    def __post_init__(self):
        if self.family not in FAMILIES:
            raise ValueError(f"{self.check_id}: unknown family {self.family!r}")
        if self.gate not in GATES:
            raise ValueError(f"{self.check_id}: unknown gate {self.gate!r}")
        if self.coverage not in COVERAGES:
            raise ValueError(f"{self.check_id}: unknown coverage {self.coverage!r}")
        if self.status is not Status.PASS and not self.detail.strip():
            raise ValueError(f"{self.check_id}: a {self.status.name} row needs a reason")
        if self.family == "doctrine" and not self.source_text.strip():
            raise ValueError(f"{self.check_id}: a doctrine row needs its source_text")

    @property
    def failing(self) -> bool:
        """Turns the verdict: any ERROR, or a FAIL on a blocking row."""
        return self.status is Status.ERROR or (self.status is Status.FAIL and self.blocking)

    def status_label(self) -> str:
        if self.status is Status.FAIL and not self.blocking:
            return "FAIL (non-blocking)"
        return self.status.value

    def rendered_detail(self) -> str:
        if self.status is Status.NOT_MECHANISED:
            return f"{self.detail} — not counted as satisfied"
        if self.status in (Status.PASS, Status.FAIL) and self.coverage == "partial" and self.clause:
            return f'[partial: "{self.clause}"] {self.detail}'.rstrip()
        return self.detail


@dataclass
class Report:
    gate: str
    inputs: dict                 # path -> sha256, subject first
    packs_selected: list
    results: list
    label: str = ""              # header subject, e.g. "package X.txt (sha256 …)"
    notes: list = field(default_factory=list)

    def __post_init__(self):
        if self.gate not in GATES:
            raise ValueError(f"unknown gate {self.gate!r}")
        seen = set()
        for r in self.results:
            if r.check_id in seen:
                raise ValueError(f"duplicate row for {r.check_id}")
            seen.add(r.check_id)

    # ── verdict ─────────────────────────────────────────────────────────
    def verdict(self) -> str:
        return "FAIL" if any(r.failing for r in self.results) else "PASS"

    def rows(self, *families) -> list:
        return [r for r in self.results if r.family in families]

    # ── text rendering (mirrors validate_compiled_pack.py's PASS/FAIL idiom) ──
    def render_text(self) -> str:
        lines = [f"CANON GATE v0 — {GATE_LABEL[self.gate]} — {self.label} — packs: "
                 f"{', '.join(self.packs_selected) or 'none'}"]
        for r in self.rows("limit", "doctrine"):
            lines.append(self._row(r))
        for heading in ("dispatch", "infra"):
            block = self.rows(heading)
            if block:
                lines.append(heading)
                lines.extend(self._row(r) for r in block)
        lines.extend(self.notes)
        lines.append(self.final_line())
        return "\n".join(lines)

    @staticmethod
    def _row(r: CheckResult) -> str:
        label = r.status_label()
        return f"{label}{' ' * max(1, 16 - len(label))}{r.check_id:<16}{r.rendered_detail()}"

    def final_line(self) -> str:
        S = Status
        doctrine = self.rows("doctrine")
        n_pass = sum(1 for r in self.results if r.status is S.PASS)
        nb = sum(1 for r in self.results if r.status is S.FAIL and not r.blocking)
        nb_text = f"{nb} non-blocking FAIL{'s' if nb != 1 else ''} on record"
        m = sum(1 for r in doctrine if r.status is S.NOT_MECHANISED)
        k = sum(1 for r in doctrine if r.status is S.NOT_APPLICABLE)
        j = sum(1 for r in doctrine if r.status is S.NOT_RUN)
        if self.verdict() == "PASS":
            return (f"GATE PASS: {n_pass} mechanised checks hold over the submitted bytes "
                    f"({nb_text}); {m} doctrine check lines NOT mechanised, {k} not applicable, "
                    f"{j} not run — none counted as satisfied. This establishes structure over "
                    "the prompt/artifact bytes — not doctrine satisfaction, quality, outcomes, "
                    "or adoption.")
        failing = sum(1 for r in self.results if r.failing)
        ran = [r for r in doctrine if r.status in (S.PASS, S.FAIL)]
        partial = sum(1 for r in ran if r.coverage == "partial")
        cov = "all partial" if partial == len(ran) else f"{partial} partial"
        return (f"GATE FAIL ({failing} failing checks; {nb_text}). {len(ran)} checks mechanised "
                f"({cov}) over {len(doctrine)} doctrine check lines; {m + k + j} lines NOT "
                "mechanised, not applicable or not run — never counted as satisfied.")

    # ── JSON ────────────────────────────────────────────────────────────
    def to_json(self) -> dict:
        return {
            "gate": self.gate,
            "verdict": self.verdict(),
            "label": self.label,
            "inputs": dict(self.inputs),
            "packs_selected": list(self.packs_selected),
            "results": [{
                "check_id": r.check_id, "family": r.family, "gate": r.gate,
                "status": r.status.name, "coverage": r.coverage, "clause": r.clause,
                "source_text": r.source_text, "detail": r.detail,
                "evidence": list(r.evidence), "blocking": r.blocking,
            } for r in self.results],
            "notes": list(self.notes),
            "report_text": self.render_text(),
        }
