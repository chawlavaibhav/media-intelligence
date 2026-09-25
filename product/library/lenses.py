"""Lenses and recent dishes (kitchen card v4 / chef v9, 2026-09-25: the directors' review).

Code keeps only memory here, never taste: it OFFERS the chef three ways of seeing for this order (fit for the medium,
not used in the last three dishes, at least one far from what the category usually gets) and shows the chef what the
kitchen recently served so habits are visible. The chef writes one direction through each lens and chooses on the idea.
"""
from __future__ import annotations

import functools
import json
import random
import re
from pathlib import Path

import yaml

HERE = Path(__file__).parent


@functools.lru_cache(maxsize=1)
def roster() -> dict:
    return yaml.safe_load((HERE / "lenses.yaml").read_text())


def lens(lens_id: str) -> dict | None:
    return next((x for x in roster()["lenses"] if x["id"] == lens_id), None)


def plain(lens_id: str | None) -> str:
    """The lens in plain words for the customer — never a director's name."""
    x = lens(lens_id or "")
    return f"{x['name']}: {x['way_of_seeing']}" if x else ""


def recent_dishes(store, exclude_job: str, n: int = 8) -> list:
    """What this kitchen served most recently (latest recipe of each other job), newest first."""
    rows = store.q("SELECT a.job_id, a.data_json FROM artifacts a JOIN (SELECT job_id, MAX(version) v FROM artifacts "
                   "WHERE kind='recipe' GROUP BY job_id) m ON a.job_id=m.job_id AND a.version=m.v "
                   "WHERE a.kind='recipe' AND a.job_id != ? ORDER BY a.id DESC LIMIT ?", (exclude_job, n))
    out = []
    for r in rows:
        d = json.loads(r["data_json"])
        anchors, sound = d.get("identity_anchors") or {}, d.get("sound") or {}
        out.append({"lens": d.get("lens") or None, "idea": (d.get("selected_concept") or "")[:200],
                    "shape": (d.get("shape") or "")[:200], "people": (anchors.get("person") or "")[:180],
                    "setting": (anchors.get("world") or "")[:160], "grade": (anchors.get("grade") or "")[:140],
                    "music": (sound.get("music_prompt") or "")[:180], "remember": (d.get("remember") or "")[:120],
                    "shots": " → ".join(s.get("tool", "?") for s in d.get("shots") or []) or "a picture"})
    return out


def _words(text: str) -> set:
    return set(re.findall(r"[a-z]{4,}", (text or "").lower()))


def offer(job_id: str, media: str, category_text: str, recent: list) -> list:
    """Three lenses for this order: fit the medium; none used in the last three dishes (unless too few remain); at least
    one whose strengths share nothing with the category's words (far from what the category usually gets)."""
    kind = "film" if media == "video" else "picture"
    eligible = [x for x in roster()["lenses"] if x["for"] in ("both", kind)]
    used = [d.get("lens") for d in recent[:3] if d.get("lens")]
    pool = [x for x in eligible if x["id"] not in used]
    if len(pool) < 3:
        pool = eligible
    rng = random.Random(job_id)
    cat = _words(category_text)
    far = [x for x in pool if not (cat & _words(x["good_at"]))]
    picks = [rng.choice(far)] if far else []
    rest = [x for x in pool if x not in picks]
    rng.shuffle(rest)
    picks += rest[: 3 - len(picks)]
    rng.shuffle(picks)
    return [{kk: x[kk] for kk in ("id", "name", "way_of_seeing", "good_at", "risks")} for x in picks]
