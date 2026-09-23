"""Cost: the quote the customer sees and the reasoning-cost report per worker (spec §9.4).

Reasoning budgets are TARGETS to measure, not promises: USD 0.30 per film job and USD 0.08 per image (amendment 1 §1:
one image recipe may produce a set of images — one per format — so an image job's reasoning is shared across its set). In simulated mode
every AI call records an ESTIMATED cost (product/ai.py: token estimate × the configured model's list price), so a
simulated job reports what its reasoning would have cost live, per worker, before any money is spent. Live jobs record
the actual settled cost per call in the ledger; the report shows both.
"""
from __future__ import annotations

import json
from decimal import Decimal

from product.dispatch import quote as provider_quote
from product.library import tokens

BUDGET = {"image": Decimal("0.08"), "video": Decimal("0.30")}          # image: per image in the set; video: per film
TARGETS = {"film": str(BUDGET["video"]), "image": str(BUDGET["image"])}
CLIP_LENGTHS = (4, 6, 8)
CARD_AND_SCHEMA_TOKENS = 1100      # the stable prefix of a small-taster / big-taster call (measured from the rulebook files)


def clip_len(use_s: float) -> int:
    for c in CLIP_LENGTHS:
        if use_s + 0.4 <= c:
            return c
    return 8


def expected_calls(recipe: dict, media: str, formats: list) -> list:
    """(worker, in_tokens) for the calls still to come after the recipe is approved."""
    out = []
    if media == "image":
        for _ in formats or ["1:1"]:
            out.append(("small_taster", CARD_AND_SCHEMA_TOKENS + 2 * 1300 + 400))
        out.append(("big_taster", CARD_AND_SCHEMA_TOKENS + len(formats or [1]) * 1300 + 1300 + 1500))
    else:
        out.append(("small_taster", CARD_AND_SCHEMA_TOKENS + 2 * 1300 + 400))                  # the master plate
        for s in recipe.get("shots", []):
            if s["route"] == "END-CARD":
                continue
            if s["starts_from"] != "previous_shot_end":
                out.append(("small_taster", CARD_AND_SCHEMA_TOKENS + 3 * 1300 + 400))          # the shot's first frame
            if s["route"] in ("FILM-B", "FILM-C"):
                out.append(("small_taster", CARD_AND_SCHEMA_TOKENS + 3 * 1300 + int(300 * clip_len(float(s["duration_s"]))) + 400))
        total = sum(float(s["duration_s"]) for s in recipe.get("shots", []))
        out.append(("big_taster", CARD_AND_SCHEMA_TOKENS + int(300 * total) + 2 * 1300 + 1500))
    out.append(("diary_writer", 6000))
    return out


def reasoning_report(k, job_id: str, recipe: dict | None = None, *, stage: str = "final") -> dict:
    """Per worker: calls made (estimated and, when live, actual cost) + calls still expected. Compared with the budget.
    stage "quote": before production — every call the recipe implies is still expected.
    stage "final": after production — only the calls made, plus the diary writer if it has not run yet."""
    job = k.store.job(job_id)
    media = job["media"]
    per = {}
    for c in k.store.llm_calls(job_id):
        w = c["worker"] or c["role"]
        e = per.setdefault(w, {"calls": 0, "estimated_usd": Decimal(0), "actual_usd": Decimal(0), "expected_calls": 0,
                               "expected_usd": Decimal(0), "model": k.s.models.get(w, "")})
        e["calls"] += 1
        e["estimated_usd"] += Decimal(c["est_cost_usd"] or 0)
    for a in k.store.attempts(job_id):
        if a["category"] == "reasoning" and a["settled_usd"]:
            call = k.store.q1("SELECT worker, role FROM llm_calls WHERE attempt_id=?", (a["id"],))
            if call:
                w = call["worker"] or call["role"]
                per.setdefault(w, {"calls": 0, "estimated_usd": Decimal(0), "actual_usd": Decimal(0), "expected_calls": 0,
                                   "expected_usd": Decimal(0), "model": k.s.models.get(w, "")})["actual_usd"] += Decimal(a["settled_usd"])
    if recipe is not None:
        formats = (k.store.artifact(job_id, "understanding") or {}).get("deliverable", {}).get("formats") or []
        todo = expected_calls(recipe, media, formats)
        if stage == "final":
            todo = [(w, t) for w, t in todo if w == "diary_writer" and "diary_writer" not in per]
        for w, tin in todo:
            e = per.setdefault(w, {"calls": 0, "estimated_usd": Decimal(0), "actual_usd": Decimal(0), "expected_calls": 0,
                                   "expected_usd": Decimal(0), "model": k.s.models.get(w, "")})
            e["expected_calls"] += 1
            e["expected_usd"] += k.workers.estimate(w, tin)[1]
    total = sum(e["estimated_usd"] + e["expected_usd"] for e in per.values())
    images = images_in_set(k, job_id) if media == "image" else None
    per_image = (total / images).quantize(Decimal("0.0001")) if images else None
    measured = per_image if media == "image" else total
    return {"media": media, "budget_usd": str(BUDGET[media]), "estimated_total_usd": str(total.quantize(Decimal("0.0001"))),
            "targets": dict(TARGETS), "images_in_set": images, "per_image_usd": str(per_image) if per_image is not None else None,
            "target_measured": "per image in the set" if media == "image" else "per film",
            "within_budget": measured <= BUDGET[media], "mode": k.s.reasoning_mode,
            "basis": "token estimates x the configured models' list prices (product/reasoning.py PRICES); "
                     "live jobs replace estimates with the ledger's settled cost",
            "per_worker": {w: {kk: (str(v.quantize(Decimal('0.000001'))) if isinstance(v, Decimal) else v) for kk, v in e.items()}
                           for w, e in sorted(per.items())}}


def images_in_set(k, job_id) -> int:
    """How many images one image recipe produces: one per requested format (amendment 1 §1)."""
    u = k.store.artifact(job_id, "understanding") or {}
    return max(1, len((u.get("deliverable") or {}).get("formats") or k.brief(job_id).get("formats") or ["1:1"]))


def quote(k, job_id: str, recipe: dict) -> dict:
    job = k.store.job(job_id)
    media = job["media"]
    u = k.store.artifact(job_id, "understanding")
    lines = []
    img = provider_quote("nano-banana-2")
    if media == "image":
        n = len(u["deliverable"].get("formats") or ["1:1"])
        lines.append(("pictures (one retry allowance each)", n * 2, img))
    else:
        reuse_master = any(str(x).startswith("shf_") for x in recipe.get("reuse_shelf_items", []))
        lines.append(("master plate (look of the film)", 0 if reuse_master else 2, img))
        for s in recipe.get("shots", []):
            if s["route"] == "END-CARD":
                continue
            if s["starts_from"] != "previous_shot_end":
                lines.append((f"shot {s['n']} first frame", 2, img))
            if s["route"] in ("FILM-B", "FILM-C"):
                c = clip_len(float(s["duration_s"]))
                lines.append((f"shot {s['n']} moving picture ({c}s, up to 2 takes)", 2, provider_quote("veo-3.1-fast-i2v", duration_s=c)))
        lines.append(("music bed", 2, provider_quote("lyria")))
    media_usd = sum(Decimal(n) * p for _, n, p in lines)
    rep = reasoning_report(k, job_id, recipe, stage="quote")
    reasoning = Decimal(rep["estimated_total_usd"])
    total = (media_usd + reasoning).quantize(Decimal("0.01"))
    return {"lines": [{"item": a, "units": n, "unit_usd": str(p), "usd": str((Decimal(n) * p).quantize(Decimal('0.01')))} for a, n, p in lines],
            "media_ceiling_usd": str(media_usd.quantize(Decimal("0.01"))),
            "reasoning_line_usd": str(reasoning.quantize(Decimal("0.01"))), "reasoning_budget_usd": rep["budget_usd"],
            "images_in_set": rep["images_in_set"],
            **({"reasoning_per_image_usd": str(Decimal(rep["per_image_usd"]).quantize(Decimal("0.001")))} if media == "image" else {}),
            "reasoning_targets": rep["targets"], "reasoning_within_target": rep["within_budget"],
            "reasoning_basis": rep["basis"], "recommended_budget_usd": str(max(total, Decimal("0.50"))),
            "basis": "unit prices x planned draws incl. one retry allowance per output; reasoning = per-worker estimate (spec 9.4)"}


def dump(obj) -> str:
    return json.dumps(obj, default=str)


__all__ = ["quote", "reasoning_report", "clip_len", "BUDGET", "tokens"]
