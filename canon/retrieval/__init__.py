"""CANON-015 — bounded, accepted-only Canon retrieval and context packaging.

Read `canon/retrieval/README.md` for the design and
`canon/retrieval/RETRIEVAL-CONTRACT-v0.1.md` for the guarantees this package makes.

Everything here is read-only over the Canon tree. No module in this package opens a file
for writing anywhere under `canon/`, and none makes a model or provider call.
"""
from .budgets import COMPACT_BUDGETS, DEFAULT_BUDGETS, PRESETS, BudgetError, Budgets
from .bundle import BUNDLE_VERSION, build_bundle, model_payload
from .corpus import ACCEPTED, HOLD, AcceptedCanon, CanonStatusError, CorpusError
from .plan import PlanError, build_plan
from .questions import CATALOGUE, QUESTION_IDS
from .rank import TypedIndex

__all__ = [
    "ACCEPTED", "HOLD", "AcceptedCanon", "BUNDLE_VERSION", "BudgetError", "Budgets",
    "CATALOGUE", "COMPACT_BUDGETS", "CanonStatusError", "CorpusError", "DEFAULT_BUDGETS",
    "PRESETS", "PlanError", "QUESTION_IDS", "TypedIndex", "build_bundle", "build_plan",
    "model_payload",
]
