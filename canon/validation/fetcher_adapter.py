"""Adapter: the CANON-015 fetcher (canon/retrieval, PR #84) as a `--fetcher` for canon_done.py.

    python3 canon/validation/canon_done.py --fetcher canon.validation.fetcher_adapter:fetch

`fetch(nr, job)` returns the sk ids the fetcher would put in front of the model for this brief,
at the budget named by FETCH_BUDGET. Measurement only — nothing here is adopted.
"""
from __future__ import annotations

import dataclasses
from pathlib import Path

from canon.retrieval.budgets import DEFAULT_BUDGETS
from canon.retrieval.bundle import build_bundle
from canon.retrieval.corpus import AcceptedCanon

REPO = Path(__file__).resolve().parents[2]
# the widest bounded budget: ~30k chars ≈ 7.5k tokens (the fetcher's own default cap)
FETCH_BUDGET = dataclasses.replace(DEFAULT_BUDGETS)
_CORPUS = None


def _corpus():
    global _CORPUS
    if _CORPUS is None:
        _CORPUS = AcceptedCanon(REPO)
    return _CORPUS


def bundle_for(job: dict, budgets=FETCH_BUDGET) -> dict:
    text = job.get("brief", {}).get("text", "") or ""
    kind = job.get("deliverable_request", {}).get("kind", "")
    modality = job.get("deliverable_request", {}).get("modality", "")
    needs = [w for w in (kind.replace("_", " "), modality) if w]
    return build_bundle(text, _corpus(), budgets=budgets, declared_needs=needs)


def fetch(nr, job: dict):
    b = bundle_for(job)
    return [it.get("item_id") for it in b.get("items", []) if str(it.get("item_id", "")).startswith("sk_")]
