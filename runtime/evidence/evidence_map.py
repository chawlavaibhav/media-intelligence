"""Reading ROUTING-EVIDENCE-MAP-v0 as evidence, not as a leaderboard.

The map carries no score and the runtime must not invent one. What this module extracts is:

  * the routing rules, split into clauses and classified by the lexicon in
    RULE-INTERPRETATION-v0.yaml (prohibit / default / prefer);
  * for a prohibiting clause, the ROUTES it names — matched against the map's own route keys,
    so a rule that starts naming a different route needs no code change;
  * for any route, the map CELLS that back it, so a decision can cite where it came from.

Nothing in here calls anything. It is a YAML file and a regex.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .. import paths
from ..util import load_yaml

_CLAUSE = re.compile(r"[;.]\s+|\s+—\s+")
_NONWORD = re.compile(r"[^a-z0-9]+")


@dataclass(frozen=True)
class Clause:
    text: str
    directive: str            # prohibit | default | prefer | none
    strategies: tuple         # strategy ids this clause is about
    routes: tuple             # route keys this clause names


@dataclass(frozen=True)
class Rule:
    id: str
    scope: str
    text: str
    evidence: str
    tier: str
    registry: bool
    source: str
    clauses: tuple
    facets: tuple             # the facets its scope and text are conditional on

    def directive_for(self, strategy: str) -> str:
        rank = {"prohibit": 0, "default": 1, "prefer": 2, "none": 3}
        best = "none"
        for clause in self.clauses:
            if strategy in clause.strategies and rank[clause.directive] < rank[best]:
                best = clause.directive
        return best

    def routes_for(self, strategy: str, directive: str) -> tuple:
        out = []
        for clause in self.clauses:
            if clause.directive == directive and strategy in clause.strategies:
                out.extend(clause.routes)
        return tuple(sorted(set(out)))


class EvidenceMap:
    def __init__(self, map_path: str | Path | None = None, lexicon_path: str | Path | None = None):
        self.map_path = str(map_path or paths.EVIDENCE_MAP)
        self.lexicon_path = str(lexicon_path or paths.RULE_INTERPRETATION)
        self.doc = load_yaml(self.map_path) or {}
        self.lex = load_yaml(self.lexicon_path) or {}
        self.questions = self.doc.get("questions", {}) or {}
        self._route_keys = self._collect_route_keys()
        self.rules = tuple(self._read_rule(r) for r in self.doc.get("routing_rules", []))

    # ------------------------------------------------------------------ routes and cells
    def _collect_route_keys(self) -> dict:
        """route_key -> [(question, cell_key, arm)], straight out of the map."""
        out: dict[str, list] = {}
        for question, body in self.questions.items():
            for cell_key, cell in (body.get("cells") or {}).items():
                route = cell.get("route_key") or cell_key.split("+")[0]
                out.setdefault(route, []).append((question, cell_key, cell.get("arm")))
        return out

    def route_keys(self) -> list:
        return sorted(self._route_keys)

    def cells_for_route(self, route_key: str) -> list:
        return sorted(f"{q}/{c}" for q, c, _ in self._route_keys.get(route_key, []))

    def cells_for_strategy(self, strategy: str, modality: str) -> list:
        """Every map cell whose ARM names this strategy, within the modality's questions."""
        arm_phrases = [p.lower() for p in ((self.lex.get("strategies") or {}).get(strategy) or {}).get("arm_phrases", [])]
        if not arm_phrases:
            return []
        prefixes = [p for p, m in (self.lex.get("question_prefix_modality") or {}).items() if m == modality]
        out = []
        for question, body in self.questions.items():
            if not any(question.startswith(p) for p in prefixes):
                continue
            for cell_key, cell in (body.get("cells") or {}).items():
                arm = str(cell.get("arm") or cell_key)
                if any(phrase in arm.lower() for phrase in arm_phrases):
                    out.append(f"{question}/{cell_key}")
        return sorted(out)

    def brand_tokens(self) -> list:
        """Identity words in the map's route keys — the model names an acceptance statement
        may never contain. Derived from the map, so a new provider is guarded the day it lands."""
        stop = {s.lower() for s in self.lex.get("route_token_stoplist", [])}
        tokens = set()
        for route in self._route_keys:
            for part in route.split("-"):
                part = part.lower()
                if not part or part in stop:
                    continue
                if any(ch.isdigit() for ch in part):
                    continue
                if len(part) < 3:
                    continue
                tokens.add(part)
        return sorted(tokens)

    # ------------------------------------------------------------------ rules
    def _read_rule(self, row: dict) -> Rule:
        text = str(row.get("rule", ""))
        scope = str(row.get("scope", ""))
        clauses = tuple(self._read_clause(c) for c in _split(text))
        facets = tuple(sorted(self._facets_of(scope + " || " + text)))
        return Rule(
            id=row.get("id", ""),
            scope=scope,
            text=text,
            evidence=str(row.get("evidence", "")),
            tier=str(row.get("tier", "")),
            registry=bool(row.get("registry", False)),
            source=str(row.get("source", "")),
            clauses=clauses,
            facets=facets,
        )

    def _read_clause(self, text: str) -> Clause:
        low = text.lower()
        directive = "none"
        for kind in self.lex.get("directive_rank", []):
            markers = (self.lex.get("directives") or {}).get(kind, [])
            if any(marker.lower() in low for marker in markers):
                directive = kind
                break
        strategies = tuple(
            sorted(
                sid
                for sid, body in (self.lex.get("strategies") or {}).items()
                if any(phrase.lower() in low for phrase in body.get("rule_phrases", []))
            )
        )
        if directive == "none" and strategies:
            # a clause that names a strategy and forbids nothing is a recommendation
            directive = "prefer"
        return Clause(text=text, directive=directive, strategies=strategies, routes=tuple(self._routes_in(text)))

    def _routes_in(self, text: str) -> list:
        """Route keys named in prose. 'Seedream 5 Pro' -> 'seedream-5-pro' by normalising both
        sides to a bare alphanumeric run; the map's own key list is the vocabulary."""
        flat = _NONWORD.sub("", text.lower())
        found = []
        for route in self._route_keys:
            if _NONWORD.sub("", route.lower()) in flat:
                found.append(route)
        # keep the longest match per family: 'flux-2-pro-edit' contains 'flux-2-pro'
        out = [r for r in found if not any(r != o and _NONWORD.sub("", r.lower()) in _NONWORD.sub("", o.lower()) for o in found)]
        return sorted(out)

    def _facets_of(self, text: str) -> set:
        low = text.lower()
        return {
            facet
            for facet, body in (self.lex.get("facets") or {}).items()
            if any(phrase.lower() in low for phrase in body.get("phrases", []))
        }

    def rule(self, rule_id: str) -> Rule | None:
        for rule in self.rules:
            if rule.id == rule_id:
                return rule
        return None

    def strategy_ids(self) -> list:
        return sorted((self.lex.get("strategies") or {}))

    def strategy_row(self, strategy: str) -> dict:
        return dict(((self.lex.get("strategies") or {}).get(strategy) or {}))

    def lettering_facets(self) -> set:
        return set(self.lex.get("lettering_facets", []))

    def facet_names(self) -> list:
        return sorted((self.lex.get("facets") or {}))


def _split(text: str) -> list:
    return [part.strip() for part in _CLAUSE.split(text) if part.strip()]
