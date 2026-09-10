"""The evidence side of a route decision: the taint register, the routing map, and the binding.

WHAT THIS MODULE IS ALLOWED TO KNOW

    Which cells exist, what each cell's evidence STATUS is, and how many draws sit behind it. It
    never reads a score (the map carries none and the runtime must not invent one), and it never
    reads the map's cost figures — those were measured on surfaces the roster has since re-pointed,
    so they are history, not prices. Prices come from `price.py`, through the roster.

THE GATE, IN THE ORDER IT IS APPLIED

    1. TAINT-REGISTER-v1 is the authority. A cell whose `evidence_status` is
       `awaiting_controller_ruling` is NEVER auto-routed, whatever any profile says — that is an
       invariant of ROUTE-DECISION-v0, not a policy choice. The decision names the blocking ruling.
    2. The register's own reading, `production_use_allowed`: `manual_only` and `false` both stop an
       automatic route.
    3. Only then the active policy profile: the status must be one the profile lists as
       auto-routable. The profile can be stricter than the register. It can never be looser.

    There is no launch-eligibility status anywhere in the register, and the register says in writing
    that there never will be. This module therefore reports, rather than hides, a profile that names
    a status the register's vocabulary does not contain: that profile auto-routes nothing.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path

import yaml

BINDING_FILENAME = "CAPABILITY-EVIDENCE-BINDING-v0.yaml"


class EvidenceError(RuntimeError):
    """An evidence input could not be read as the shape it declares."""


class FingerprintMismatch(EvidenceError):
    """The taint register was generated against a different routing map than the one on disk."""


def repo_root_from(here: Path) -> Path:
    """The checkout root: the directory holding runtime/ and eval/."""
    for parent in [here] + list(here.parents):
        if (parent / "runtime" / "contracts").is_dir() and (parent / "eval").is_dir():
            return parent
    raise EvidenceError(f"no checkout root above {here}")


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass(frozen=True)
class Cell:
    """One entry of the routing evidence map, carrying the register's verdict on it."""
    cell_key: str
    question: str
    route_key: str
    arm: str | None
    evidence_status: str
    production_use_allowed: object          # True | "manual_only" | False
    blocking_ruling: str | None
    blocking_open_question: str | None
    replacement_needed: bool
    register_reason: str
    accepts: int | None
    trials: int | None
    n_items: int | None
    blinding_commitment_verified: object

    def evidence_n(self, settled_draw_floor: int) -> dict:
        """Draws and items behind the cell, carried forward honestly. Two draws is two draws."""
        return {"accepts": self.accepts, "trials": self.trials, "items": self.n_items,
                "settled_draw_floor": settled_draw_floor,
                "note": "human blind acceptance, one judge; never a Registry row and never a score"}


@dataclass
class GateResult:
    allowed: bool
    stage: str
    reason: str
    blocking_ruling: str | None = None
    blocking_open_question: str | None = None


@dataclass
class Binding:
    """CAPABILITY-EVIDENCE-BINDING-v0, read from disk."""
    path: Path
    data: dict

    @property
    def sources(self) -> dict:
        return dict(self.data.get("sources") or {})

    @property
    def selection_order(self) -> dict:
        return dict(self.data.get("selection_order") or {})

    @property
    def fallback_triggers(self) -> list:
        return list((self.data.get("fallback_triggers") or {}).get("vocabulary") or [])

    def rows(self) -> list:
        return list(self.data.get("capabilities") or [])

    def resolve(self, capability: str, level: str | None) -> dict:
        """(question, arms, dispatches, basis) for a capability requirement, or a refusal dict."""
        for row in self.rows():
            if row.get("capability") != capability:
                continue
            if "levels" not in row:
                return {"found": True, "question": row["question"], "arms": row.get("arms"),
                        "dispatches": bool(row.get("dispatches")), "basis": row.get("basis"),
                        "level": None}
            for lv in row["levels"]:
                if lv.get("level") == level:
                    return {"found": True, "question": lv["question"], "arms": lv.get("arms"),
                            "dispatches": bool(lv.get("dispatches")), "basis": lv.get("basis"),
                            "level": level}
            declared = [lv.get("level") for lv in row["levels"]]
            return {"found": False, "reason":
                    f"capability {capability!r} is answered at a named level; the spec gave "
                    f"level={level!r} and the binding declares {declared!r}. The router does not "
                    f"choose a level on the spec's behalf."}
        return {"found": False, "reason":
                f"capability {capability!r} has no row in {BINDING_FILENAME}; it is not routed by "
                f"guesswork. Adding it is a row there, not a code change."}


class EvidenceBase:
    """The routing map and the taint register, read together and fingerprint-bound."""

    def __init__(self, root: Path | str | None = None, binding_path: Path | str | None = None):
        here = Path(__file__).resolve().parent
        self.root = Path(root) if root else repo_root_from(here)
        self.binding_path = Path(binding_path) if binding_path else here / BINDING_FILENAME
        raw = yaml.safe_load(self.binding_path.read_text(encoding="utf-8"))
        self.binding = Binding(self.binding_path, raw)

        src = self.binding.sources
        self.map_path = self.root / src["routing_evidence_map"]
        self.register_path = self.root / src["taint_register"]

        self.map = yaml.safe_load(self.map_path.read_text(encoding="utf-8"))
        self.register = yaml.safe_load(self.register_path.read_text(encoding="utf-8"))

        expected = (self.register.get("sources") or {}).get("routing_evidence_map_sha256")
        actual = sha256_of(self.map_path)
        if expected and expected != actual:
            raise FingerprintMismatch(
                f"TAINT-REGISTER-v1 was generated against routing map {expected[:12]}… but the map on "
                f"disk is {actual[:12]}…. The register is the authority on evidence status and it no "
                f"longer describes this map. Regenerate it; do not route.")
        self.map_sha256 = actual
        self.register_sha256 = sha256_of(self.register_path)

        self.status_vocabulary = list((self.register.get("evidence_status_vocabulary") or {}).keys())
        self.settled_draw_floor = int(((self.register.get("settled_draw_floor") or {}).get("value")) or 0)
        self.notes = list(self.register.get("notes") or [])
        self.open_questions = {q["id"]: q for q in (self.register.get("open_questions") or [])}
        self.cells: dict[str, Cell] = {}
        self._load_cells()

    # -- loading ---------------------------------------------------------------
    def _map_cell(self, question: str, cell_name: str) -> dict:
        return ((self.map.get("questions") or {}).get(question) or {}).get("cells", {}).get(cell_name) or {}

    def _load_cells(self) -> None:
        for entry in self.register.get("cells") or []:
            mc = self._map_cell(entry["question"], entry.get("map_cell_name") or "")
            human = mc.get("human_blind_acceptance") or {}
            cell = Cell(
                cell_key=entry["cell_key"],
                question=entry["question"],
                route_key=entry["route_key"],
                arm=entry.get("arm"),
                evidence_status=entry["evidence_status"],
                production_use_allowed=entry.get("production_use_allowed"),
                blocking_ruling=entry.get("blocking_ruling"),
                blocking_open_question=entry.get("blocking_open_question"),
                replacement_needed=bool(entry.get("replacement_needed")),
                register_reason=entry.get("reason") or "",
                accepts=human.get("accepts", entry.get("map_reported_accepts")),
                trials=human.get("trials", entry.get("map_reported_trials")),
                n_items=human.get("n_items"),
                blinding_commitment_verified=entry.get("blinding_commitment_verified"),
            )
            self.cells[cell.cell_key] = cell
        declared = self.register.get("cell_count")
        if declared is not None and int(declared) != len(self.cells):
            raise EvidenceError(f"register declares {declared} cells, read {len(self.cells)}")

    # -- queries ---------------------------------------------------------------
    def cells_for(self, question: str, arms: list | None) -> list[Cell]:
        out = [c for c in self.cells.values() if c.question == question]
        if arms:
            out = [c for c in out if c.arm in arms]
        return sorted(out, key=lambda c: c.cell_key)

    def notes_touching(self, cells: list[Cell]) -> list[dict]:
        keys = {c.cell_key for c in cells}
        questions = {c.question for c in cells}
        out = []
        for n in self.notes:
            named = set(n.get("cells") or [])
            if (named & keys) or (n.get("blocking_ruling") and any(q in (n.get("text") or "") for q in questions)):
                out.append({"id": n.get("id"), "blocking_ruling": n.get("blocking_ruling"),
                            "cells": sorted(named), "text": n.get("text")})
        return out

    def profile_statuses_not_in_vocabulary(self, statuses: list) -> list:
        return [s for s in statuses if s not in self.status_vocabulary]

    def gate(self, cell: Cell, auto_routable_statuses: list) -> GateResult:
        """The evidence gate, in the fixed order. The register first, the profile last."""
        if cell.evidence_status == "awaiting_controller_ruling":
            blocker = cell.blocking_ruling or cell.blocking_open_question
            what = "ruling" if cell.blocking_ruling else "open question"
            return GateResult(
                False, "evidence_envelope",
                f"{cell.cell_key} is awaiting_controller_ruling; {what} {blocker} decides this cell. "
                f"A cell awaiting a Controller ruling is never auto-routed (ROUTE-DECISION-v0 invariant). "
                f"Register reason: {cell.register_reason}",
                blocking_ruling=cell.blocking_ruling,
                blocking_open_question=cell.blocking_open_question)
        if cell.production_use_allowed is not True:
            return GateResult(
                False, "evidence_envelope",
                f"{cell.cell_key} is {cell.evidence_status} and the register records "
                f"production_use_allowed={cell.production_use_allowed!r}: {cell.register_reason}")
        if cell.evidence_status not in auto_routable_statuses:
            return GateResult(
                False, "evidence_envelope",
                f"{cell.cell_key} is {cell.evidence_status}; the active policy profile lists "
                f"{auto_routable_statuses!r} as auto-routable, so a person routes this one.")
        return GateResult(True, "evidence_envelope",
                          f"{cell.cell_key} is {cell.evidence_status} and the register allows "
                          f"production use; the profile lists that status as auto-routable.")
