"""Choosing the exact-text strategy BY RULE, from the evidence map.

PRODUCTION-SPEC-v0 requires `exact_text.strategy` and `exact_text.strategy_basis`, and says the
strategy "is chosen by rule from the evidence, and the rule is named in strategy_basis so it can
be audited later". This module is that rule, and it holds no evidence of its own:

  * the rules come from eval/capability-map/ROUTING-EVIDENCE-MAP-v0.yaml at call time;
  * which words in a rule mean what comes from runtime/evidence/RULE-INTERPRETATION-v0.yaml;
  * which routes a prohibition names comes from the map's own route keys.

RR-1, RR-2, RR-3 and RR-6 are not written down here. When they change — and they will — this
file does not change.

The procedure:
  1. work out which facets are true of this request (contractual exactness, script, in-scene,
     must-move);
  2. a rule is in scope only when EVERY facet its scope and text are conditional on is true;
  3. prohibitions first: a strategy any in-scope rule forbids is out, and the routes an in-scope
     rule forbids are carried forward for the routing lane;
  4. among what survives, the rule marked DEFAULT wins, then the more specific rule;
  5. a strategy with no surviving route to execute it is a refusal, not a guess.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from ..errors import Refusal
from ..evidence import EvidenceMap

_RANK = {"prohibit": 0, "default": 1, "prefer": 2, "none": 3}


@dataclass(frozen=True)
class TextStrategy:
    strategy: str
    strategy_basis: str
    rule_id: str
    map_cells: tuple
    prohibited_routes: tuple
    prohibitions: tuple
    considered: tuple
    facets_active: tuple


def choose(nr, evidence: EvidenceMap | None = None) -> TextStrategy:
    evidence = evidence or EvidenceMap()
    active = _active_facets(nr, evidence)

    if not nr.text_requirements:
        return TextStrategy(
            strategy="no_exact_text",
            strategy_basis=(
                "no rule consulted: the job names no character-exact string, so nothing about "
                "lettering is contractual (PRODUCTION-JOB-v0.exact_text_strings empty)"
            ),
            rule_id="",
            map_cells=(),
            prohibited_routes=(),
            prohibitions=(),
            considered=(),
            facets_active=tuple(sorted(f for f, on in active.items() if on)),
        )

    in_scope = [r for r in evidence.rules if r.facets and all(active.get(f, False) for f in r.facets)]
    if not in_scope:
        raise Refusal(
            Refusal.TEXT_STRATEGY_UNDECIDABLE,
            "the job names character-exact strings but no routing rule is in scope for them; "
            "the runtime does not choose a text strategy without evidence",
            facets=sorted(f for f, on in active.items() if on),
            map=evidence.map_path,
        )

    forbidden_strategies: dict[str, str] = {}
    prohibitions: list[dict] = []
    candidates: list[tuple] = []

    for rule in in_scope:
        for clause in rule.clauses:
            if clause.directive == "prohibit":
                for sid in clause.strategies:
                    forbidden_strategies.setdefault(sid, rule.id)
                if clause.routes:
                    prohibitions.append(
                        {
                            "rule_id": rule.id,
                            "routes": list(clause.routes),
                            "because": clause.text,
                            "lettering_prohibition": bool(rule.facets) and set(rule.facets) <= evidence.lettering_facets(),
                        }
                    )
            elif clause.strategies and clause.directive in ("default", "prefer"):
                for sid in clause.strategies:
                    candidates.append((sid, rule, clause.directive))

    surviving = [c for c in candidates if c[0] not in forbidden_strategies]
    if not surviving:
        raise Refusal(
            Refusal.TEXT_STRATEGY_UNDECIDABLE,
            "every exact-text strategy the in-scope rules name is forbidden by another in-scope rule",
            forbidden=forbidden_strategies,
            considered=sorted({c[0] for c in candidates}),
        )

    # the most specific rule first (it was written about exactly this request), then the
    # rule marked DEFAULT over one that merely prefers, then rule order for stability
    surviving.sort(key=lambda c: (-len(c[1].facets), _RANK[c[2]], _rule_order(c[1].id)))
    strategy, rule, directive = surviving[0]

    drawn_by = evidence.strategy_row(strategy).get("lettering_drawn_by")
    biting = [
        p for p in prohibitions
        if not (drawn_by == "code" and p["lettering_prohibition"])
    ]
    prohibited_routes = tuple(sorted({r for p in biting for r in p["routes"]}))

    cells = [c for c in evidence.cells_for_strategy(strategy, nr.modality)]
    surviving_cells = tuple(c for c in cells if _cell_route(c, evidence) not in prohibited_routes)
    if cells and not surviving_cells:
        raise Refusal(
            Refusal.TEXT_STRATEGY_UNDECIDABLE,
            f"strategy {strategy!r} has no route left that may execute it once the in-scope "
            "prohibitions are applied",
            strategy=strategy,
            prohibited_routes=list(prohibited_routes),
            cells=cells,
        )

    basis = (
        f"{rule.id} [{directive}] — {rule.scope}; map cells: "
        + (", ".join(surviving_cells) if surviving_cells else "none recorded for this modality")
    )
    if prohibited_routes:
        basis += "; routes excluded by " + ", ".join(
            f"{p['rule_id']} ({'/'.join(p['routes'])})" for p in biting
        )
    if strategy in forbidden_strategies:  # unreachable, kept as an explicit invariant
        raise Refusal(Refusal.TEXT_STRATEGY_UNDECIDABLE, "chose a forbidden strategy", strategy=strategy)

    return TextStrategy(
        strategy=strategy,
        strategy_basis=basis,
        rule_id=rule.id,
        map_cells=surviving_cells,
        prohibited_routes=prohibited_routes,
        prohibitions=tuple(
            (p["rule_id"], tuple(p["routes"]), p["lettering_prohibition"]) for p in prohibitions
        ),
        considered=tuple(sorted({(c[0], c[1].id) for c in candidates})),
        facets_active=tuple(sorted(f for f, on in active.items() if on)),
    )


def _cell_route(cell: str, evidence: EvidenceMap) -> str:
    body = cell.split("/", 1)[1]
    question = cell.split("/", 1)[0]
    cells = (evidence.questions.get(question) or {}).get("cells") or {}
    return (cells.get(body) or {}).get("route_key") or body.split("+")[0]


def _active_facets(nr, evidence: EvidenceMap) -> dict:
    """A facet is true of a request or it is not. Nothing here is a judgement call."""
    facets = nr.facets
    scripts = {s.lower() for s in facets.get("scripts", [])}
    active = {}
    for name in evidence.facet_names():
        if name.startswith("script_"):
            active[name] = name.split("script_", 1)[1] in scripts
        else:
            active[name] = bool(facets.get(name, False))
    return active


def _rule_order(rule_id: str) -> tuple:
    digits = "".join(ch for ch in rule_id if ch.isdigit())
    return (int(digits) if digits else 10**6, rule_id)
