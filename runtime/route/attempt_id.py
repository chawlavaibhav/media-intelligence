"""Minting the identity a customer provider attempt would carry.

This lane dispatches nothing, so no attempt id is ever sent anywhere. The ids are minted and printed
on the plan anyway, because the identity rule is only worth anything if it exists BEFORE the first
call: the taint register's `smoke_shared_identity` problem — thirteen cells where a Lab smoke attempt
and a Lab core attempt answer to the same name — happened because nobody minted the identity first.

The namespace and the foreign patterns are data (ROUTE-IDENTITY-v0.yaml). A minted id must match the
customer template and must match none of the reserved patterns, or it is refused rather than sent.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

IDENTITY_FILENAME = "ROUTE-IDENTITY-v0.yaml"


class IdentityCollision(RuntimeError):
    """A minted id could be read as a Lab, smoke or liveness identity. Never send it."""


@dataclass
class Identities:
    data: dict
    path: Path

    @property
    def prefix(self) -> str:
        return str(self.data["customer_namespace"]["prefix"])

    def mint(self, *, customer_ref: str, job_id: str, decision_id: str, route_key: str,
             draw_index: int) -> str:
        ns = self.data["customer_namespace"]
        attempt = ns["template"].format(prefix=self.prefix, customer_ref=customer_ref, job_id=job_id,
                                        decision_id=decision_id, route_key=route_key,
                                        draw_index=draw_index)
        if not re.match(ns["must_match"], attempt):
            raise IdentityCollision(f"minted id {attempt!r} does not match the customer namespace "
                                    f"{ns['must_match']!r}")
        for foreign in self.data.get("reserved_foreign_identities") or []:
            pattern, how = foreign["pattern"], foreign.get("match", "regex")
            hit = (pattern in attempt) if how == "contains" else bool(re.search(pattern, attempt))
            if hit:
                raise IdentityCollision(
                    f"minted id {attempt!r} collides with reserved identity {foreign['id']!r} "
                    f"({foreign.get('source')}). A customer attempt may never share a name with a Lab, "
                    f"smoke or liveness attempt.")
        return attempt

    def plan_attempt_ids(self, *, customer_ref: str, job_id: str, decision_id: str, route_key: str,
                         draws: int) -> list:
        return [self.mint(customer_ref=customer_ref, job_id=job_id, decision_id=decision_id,
                          route_key=route_key, draw_index=i + 1) for i in range(max(int(draws), 0))]


def load_identities(path: Path | str | None = None) -> Identities:
    p = Path(path) if path else Path(__file__).resolve().parent / IDENTITY_FILENAME
    return Identities(data=yaml.safe_load(p.read_text(encoding="utf-8")), path=p)
