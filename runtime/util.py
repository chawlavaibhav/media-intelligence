"""Canonical serialisation and fingerprints. Determinism lives here."""
from __future__ import annotations

import functools
import hashlib
import json
import math
from decimal import Decimal
from pathlib import Path
from typing import Any

import yaml


@functools.lru_cache(maxsize=64)
def load_yaml(path: str | Path) -> Any:
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def read_text(path: str | Path) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def canonical_json(obj: Any) -> str:
    """One serialisation, one byte string, for every fingerprint in this lane."""
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=_default)


def _default(obj: Any) -> Any:
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError(f"not canonically serialisable: {type(obj).__name__}")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_obj(obj: Any) -> str:
    return sha256_text(canonical_json(obj))


def token_estimate(text: str) -> int:
    """The repo's estimator: tokens = ceil(chars / 4) (pack-triggers-v0.yaml)."""
    return math.ceil(len(text) / 4)


def dedupe(items):
    seen = set()
    out = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out
