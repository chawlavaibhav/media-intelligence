"""Today's equipment (2026-09-25): what the machines the kitchen runs today can and cannot do, read from
equipment_today.yaml. Kept out of the cards so a card stays true when a machine changes; code that needs a machine's
limit (the longest clip) reads it here too, never a number of its own."""
from __future__ import annotations

import functools
from pathlib import Path

import yaml

HERE = Path(__file__).parent


@functools.lru_cache(maxsize=1)
def sheet() -> dict:
    return yaml.safe_load((HERE / "equipment_today.yaml").read_text())


def in_use() -> set:
    from product.providers import ROUTES
    return set(ROUTES)


def today(media: str | None = None) -> dict:
    """What the chef reads: only machines the kitchen actually runs, and for a picture only the picture machines."""
    run = in_use()
    kinds = {"image"} if media == "image" else {"video", "image", "audio"}
    machines = [{"machine": m["kind"], "facts": [f["says"] for f in m["facts"]]}
                for m in sheet()["machines"] if m["generator"] in run and m["kind"] in kinds]
    return {"as_of": sheet()["as_of"], "rule": sheet()["rule"], "machines": machines}


def fact(generator_kind: str, fact_id: str):
    run = in_use()
    for m in sheet()["machines"]:
        if m["kind"] == generator_kind and m["generator"] in run:
            for f in m["facts"]:
                if f["id"] == fact_id:
                    return f
    return None


def longest_clip_s() -> float:
    f = fact("video", "longest_clip_s")
    return float(f["value"]) if f and f.get("value") else 8.0
