"""DELIVERABLE-KINDS as an open registry.

Nothing in this package enumerates a kind. A kind the registry does not carry is a refusal
that names the registry, so adding a kind stays a row in a YAML file.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from . import paths
from .errors import Refusal
from .util import load_yaml


@dataclass(frozen=True)
class DeliverableKind:
    kind: str
    what: str
    capability_requirements: list
    row: dict


class DeliverableKinds:
    def __init__(self, path: str | Path | None = None):
        self.path = str(path or paths.DELIVERABLE_KINDS)
        doc = load_yaml(self.path) or {}
        self._rows = {row["kind"]: row for row in doc.get("kinds", [])}

    def names(self) -> list[str]:
        return sorted(self._rows)

    def get(self, kind: str) -> DeliverableKind:
        row = self._rows.get(kind)
        if row is None:
            raise Refusal(
                Refusal.KIND_NOT_IN_REGISTRY,
                f"deliverable kind {kind!r} has no row in the registry; adding one is a row, not a code change",
                kind=kind,
                registry=self.path,
                known=self.names(),
            )
        return DeliverableKind(
            kind=kind,
            what=row.get("what", ""),
            capability_requirements=list(row.get("capability_requirements", [])),
            row=row,
        )
