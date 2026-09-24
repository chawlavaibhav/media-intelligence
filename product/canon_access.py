"""Canon for the creative director: practical packs by rule, deep claims on request.

Practical knowledge: the ten ADOPTED compiled packs, selected and injected by the runtime's own
lookup (`runtime.canon.packs.lookup`) from a Normalized Request built from the customer's job —
deterministic given the job (CANON-SHAPE-v1 §4).

Deep knowledge: per CONTROLLER-CANON-COMPLETION-2026-09-22 ruling 4, job-specific retrieval beyond
the packs is a bounded, logged model step. The director names what it needs (claim ids it saw cited
in a pack, or plain-language questions); this module returns at most `limit` accepted source claims,
and every id returned is recorded with `retrieved_by`. The keyword ranking here has NOT been
measured with the canon_done coverage test; its hits are logged so that measurement can be run.
"""
from __future__ import annotations

import functools
import math
import re
from collections import Counter
from pathlib import Path

import yaml

from product.config import REPO
from runtime.canon.normalize import normalize
from runtime.canon.packs import lookup

KNOWLEDGE = REPO / "canon" / "knowledge" / "current"
_WORD = re.compile(r"[a-z][a-z0-9']+")
_STOP = set("the a an of and or to in on for with is are be as by it its that this from at not no into than "
            "their his her they them which what when how why can may more most".split())


def _job_for_lookup(media: str, brief_text: str, market: str, language: str, product: dict, exact_strings: list,
                    has_product_photo: bool) -> dict:
    """A PRODUCTION-JOB-v1-shaped record for the runtime's Normalized-Request binding."""
    kind = "multi_shot_story" if media == "video" else (
        "static_ad_from_supplied_photo" if has_product_photo else "static_ad")
    return {
        "brief": {"text": brief_text or "", "language": language or "en", "market": market or "IN"},
        "exact_text_strings": [{"value": s, "script": "latin" if s.isascii() else "other", "may_reflow": False}
                               for s in exact_strings if s],
        "reference_assets": [{"asset_id": "product_photo", "role": "product", "sha256": "0" * 64,
                              "provenance": "customer_supplied"}] if has_product_photo else [],
        "deliverable_request": {"kind": kind, "operation": "generate",
                                "modality": "video" if media == "video" else "static_image", "aspect": "9:16" if media == "video" else "1:1",
                                "subject": {"entity": "product", "category": product.get("category") or "product",
                                            "brand": product.get("brand") or ""}},
    }


def practical_packs(**kw) -> dict:
    """Returns the injected pack payload and the lookup record (pack ids, prefix sha, tokens, gaps)."""
    nr = normalize(_job_for_lookup(**kw))
    lk = lookup(nr)
    return {
        "payload": lk.payload,
        "record": {"packs_selected": [s["pack_id"] for s in lk.packs_selected()],
                   "packs_injected": list(lk.injected_pack_ids), "canon_gap": lk.canon_gap,
                   "missing_domain": list(lk.missing_domain or []), "tokens": lk.tokens,
                   "prefix_sha256": lk.prefix_sha256, "check_ids": list(lk.check_ids or [])[:400],
                   "notices": list(lk.notices or [])},
    }


@functools.lru_cache(maxsize=1)
def _claims() -> dict:
    out = {}
    for f in sorted(KNOWLEDGE.glob("*/source-knowledge.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        for c in d.get("source_knowledge") or []:
            if not isinstance(c, dict) or not c.get("sk_id"):
                continue
            text = " ".join([c.get("claim") or "", " ".join(c.get("source_terms") or []),
                             (c.get("concept_label") or "").replace("_", " "),
                             " ".join((c.get("scope") or {}).get("domain_discussed_by_source") or []).replace("_", " ")])
            out[c["sk_id"]] = {"sk_id": c["sk_id"], "source_id": c.get("source_id") or f.parent.name,
                               "claim": c.get("claim") or "", "terms": (c.get("source_terms") or [])[:3],
                               "conditions": (c.get("scope") or {}).get("conditions"),
                               "caveats": [cv.get("text") for cv in (c.get("caveats") or []) if isinstance(cv, dict)][:2],
                               "_tokens": Counter(w for w in _WORD.findall(text.lower()) if w not in _STOP)}
    return out


@functools.lru_cache(maxsize=1)
def _idf() -> dict:
    claims = _claims()
    df = Counter()
    for c in claims.values():
        df.update(set(c["_tokens"]))
    n = len(claims) or 1
    return {w: math.log(1 + n / (1 + d)) for w, d in df.items()}


def claim_count() -> int:
    return len(_claims())


def deep_retrieve(requests: list, limit: int = 12) -> list:
    """requests: claim ids ('sk_...') and/or questions. Returns <= limit public claim records."""
    claims, idf = _claims(), _idf()
    picked: list = []
    for r in requests:
        r = str(r).strip()
        if r in claims and r not in picked:
            picked.append(r)
    questions = [r for r in requests if str(r).strip() not in claims]
    for qtext in questions:
        qt = [w for w in _WORD.findall(str(qtext).lower()) if w not in _STOP]
        if not qt:
            continue
        scored = []
        for sk, c in claims.items():
            tf = c["_tokens"]
            s = sum(idf.get(w, 0) * (tf[w] / (tf[w] + 1.2)) for w in qt if w in tf)
            if s > 0:
                scored.append((s, sk))
        per_q = max(2, limit // max(1, len(questions)))
        for _, sk in sorted(scored, reverse=True)[:per_q]:
            if sk not in picked:
                picked.append(sk)
    return [{k: v for k, v in claims[sk].items() if not k.startswith("_")} for sk in picked[:limit]]
