#!/usr/bin/env python3
"""Canon retrieval evaluation (2026-09-25). US$0: local models only, no API calls.

Question: given a real customer brief, can a retriever surface the Canon claims a producer actually
cited by hand on that job (`canon/validation/HAND-RETRIEVED-CLAIMS.yaml`)?

Run (needs numpy, pyyaml, rank_bm25, sentence-transformers; models download from Hugging Face):
    python3 eval/retrieval-canon-2026-09-25/run_retrieval_eval.py

Inputs in this folder: brief-rentok.txt, brief-mokobara.txt (verbatim customer words from the job
branches), llm-queries.json and agentic-results.json (written by blind agents that saw only the brief
and the corpus), llm-rerank.json (optional, blind LLM re-rank of a candidate pool).
Output: results.json and a printed table.
"""
from __future__ import annotations

import glob
import json
import math
import re
from pathlib import Path

import numpy as np
import yaml
from rank_bm25 import BM25Okapi

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
KS = (5, 10, 20, 50, 100)
STOP = set("""a an the and or of to in on for with is are be as by it its that this from at not no into than their
his her they them which what when how why can may more most so if but do does did has have had was were will would
should could about over under also only such each any all one two there these those who whom our your you we i he she
him us me my own same other some very just then than too up down out off again further once here both few""".split())


def tok(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP and len(w) > 1]


# ── corpus ────────────────────────────────────────────────────────────────────────────────────────
def load_corpus():
    ids, plain, ctx, source_of = [], [], [], {}
    for f in sorted(glob.glob(str(REPO / "canon/knowledge/current/*/source-knowledge.yaml"))):
        src = Path(f).parent.name
        for c in yaml.safe_load(open(f, encoding="utf-8"))["source_knowledge"]:
            label = (c.get("concept_label") or "").replace("_", " ")
            claim = " ".join((c.get("claim") or "").split())
            terms = " ".join(c.get("source_terms") or [])
            scope = c.get("scope") or {}
            dom = " ".join(d.replace("_", " ") for d in (scope.get("domain_discussed_by_source") or []))
            cond = scope.get("conditions") or ""
            ids.append(c["sk_id"])
            source_of[c["sk_id"]] = src
            plain.append(claim)
            # "contextual" document: source + label + claim + domain + conditions + quoted source terms
            ctx.append(f"Source: {src.replace('-', ' ')}. Topic: {label}. {claim} Domain: {dom}. When: {cond}. {terms}")
    return ids, plain, ctx, source_of


def load_truth():
    y = yaml.safe_load(open(REPO / "canon/validation/HAND-RETRIEVED-CLAIMS.yaml"))
    jobs = {j: {c["id"] for c in (v.get("claims") or [])} for j, v in y["jobs"].items()}
    rentok_jobs = ["RENTOK-GAME-A-004", "RENTOK-GAME-B-005", "RENTOK-CREATIVE-QUALITY-001", "RENTOK-GAME-V2-006"]
    truth = {"rentok": set().union(*(jobs[j] for j in rentok_jobs)), "mokobara": jobs["MOKOBARA-ODYSSEY-007"]}
    return truth, jobs, rentok_jobs


# ── rankers ───────────────────────────────────────────────────────────────────────────────────────
def rrf(rankings: list[list[int]], k: int = 60) -> list[int]:
    score: dict[int, float] = {}
    for r in rankings:
        for pos, i in enumerate(r):
            score[i] = score.get(i, 0.0) + 1.0 / (k + pos + 1)
    return sorted(score, key=lambda i: -score[i])


class Dense:
    def __init__(self, name: str, docs: list[str]):
        from sentence_transformers import SentenceTransformer
        self.name = name
        self.m = SentenceTransformer(name, device="cpu")
        self.qp, dp = "", ""
        if "e5" in name:
            self.qp, dp = "query: ", "passage: "
        elif "bge" in name:
            self.qp = "Represent this sentence for searching relevant passages: "
        self.D = self.m.encode([dp + d for d in docs], batch_size=64, normalize_embeddings=True, show_progress_bar=False)

    def rank(self, q: str) -> list[int]:
        v = self.m.encode([self.qp + q], normalize_embeddings=True)[0]
        return list(np.argsort(-(self.D @ v)))


def recall_at(ranking: list[str], truth: set, k: int) -> float:
    return len(set(ranking[:k]) & truth) / len(truth) if truth else float("nan")


def main():
    ids, plain, ctx, source_of = load_corpus()
    truth, jobs, rentok_jobs = load_truth()
    n = len(ids)
    briefs = {b: (HERE / f"brief-{b}.txt").read_text() for b in ("rentok", "mokobara")}
    llmq = json.loads((HERE / "llm-queries.json").read_text()) if (HERE / "llm-queries.json").exists() else None
    agentic = json.loads((HERE / "agentic-results.json").read_text()) if (HERE / "agentic-results.json").exists() else None
    llm_rerank = json.loads((HERE / "llm-rerank.json").read_text()) if (HERE / "llm-rerank.json").exists() else None

    bm25_plain = BM25Okapi([tok(d) for d in plain])
    bm25_ctx = BM25Okapi([tok(d) for d in ctx])
    bm = lambda model, q: list(np.argsort(-model.get_scores(tok(q))))
    dense = {m: Dense(m, ctx) for m in ("BAAI/bge-small-en-v1.5", "BAAI/bge-base-en-v1.5", "intfloat/e5-base-v2")}
    dense_plain = Dense("BAAI/bge-base-en-v1.5", plain)
    from sentence_transformers import CrossEncoder
    ce = CrossEncoder("BAAI/bge-reranker-base", device="cpu", max_length=512)

    def ce_rerank(queries: list[str], pool: list[int], top: int = 100) -> list[int]:
        pool = pool[:top]
        best = np.full(len(pool), -1e9)
        for q in queries:
            s = ce.predict([(q, ctx[i]) for i in pool], batch_size=32, show_progress_bar=False)
            best = np.maximum(best, s)
        order = [pool[j] for j in np.argsort(-best)]
        return order + [i for i in range(n) if i not in set(order)]

    runs: dict[str, dict[str, list[str]]] = {}
    pools: dict[str, list[str]] = {}
    for b, q in briefs.items():
        R = {}
        R["bm25 (brief, claim text only)"] = bm(bm25_plain, q)
        R["bm25 (brief, contextual doc)"] = bm(bm25_ctx, q)
        R["dense bge-base (brief, claim text only)"] = dense_plain.rank(q)
        for m, d in dense.items():
            R[f"dense {m.split('/')[-1]} (brief)"] = d.rank(q)
        R["hybrid bm25+bge-base RRF (brief)"] = rrf([R["bm25 (brief, contextual doc)"], R["dense bge-base-en-v1.5 (brief)"]])
        R["hybrid + cross-encoder rerank (brief)"] = ce_rerank([q], R["hybrid bm25+bge-base RRF (brief)"])
        if llmq:
            qs = llmq[b]
            R["bm25 (LLM sub-queries, RRF)"] = rrf([bm(bm25_ctx, x) for x in qs])
            R["dense bge-base (LLM sub-queries, RRF)"] = rrf([dense["BAAI/bge-base-en-v1.5"].rank(x) for x in qs])
            hyb = rrf([bm(bm25_ctx, x) for x in qs] + [dense["BAAI/bge-base-en-v1.5"].rank(x) for x in qs])
            R["hybrid (LLM sub-queries, RRF)"] = hyb
            R["hybrid (LLM sub-queries) + cross-encoder rerank"] = ce_rerank(qs, hyb)
            R["hybrid (brief + LLM sub-queries) + cross-encoder rerank"] = ce_rerank(
                [q] + qs, rrf([hyb, R["hybrid bm25+bge-base RRF (brief)"]]))
            pools[b] = [ids[i] for i in R["hybrid (brief + LLM sub-queries) + cross-encoder rerank"][:80]]
        runs[b] = {k: [ids[i] for i in v] for k, v in R.items()}
        if agentic:
            runs[b]["agentic grep (blind LLM agent, 50 ids)"] = [x for x in agentic[b] if x in source_of]
        if llm_rerank and b in llm_rerank:
            runs[b]["LLM re-rank of the best pool (blind)"] = [x for x in llm_rerank[b] if x in source_of]

    # packs: the set of claim ids cited by all ten compiled packs (unranked; every brief selects all 10)
    pack_ids = set()
    for f in glob.glob(str(REPO / "canon/compilation/PACK-*.yaml")):
        pack_ids |= set(re.findall(r"\bsk_[a-z0-9]+(?:_[a-z0-9]+)*_[0-9]{3,4}\b", Path(f).read_text()))
    pack_ids &= set(ids)

    out = {"corpus_size": n, "truth_sizes": {b: len(t) for b, t in truth.items()},
           "packs_union_size": len(pack_ids),
           "packs_recall": {b: len(pack_ids & t) / len(t) for b, t in truth.items()},
           "random_expected_recall": {k: k / n for k in KS}, "methods": {}}
    for b in briefs:
        for name, r in runs[b].items():
            out["methods"].setdefault(name, {})[b] = {f"R@{k}": round(recall_at(r, truth[b], k), 3) for k in KS if k <= len(r)}
        # source-level recall at 20 for the best method is informative too
    out["per_job_rentok"] = {}
    best = "hybrid (brief + LLM sub-queries) + cross-encoder rerank" if llmq else "hybrid + cross-encoder rerank (brief)"
    for j in rentok_jobs:
        out["per_job_rentok"][j] = {f"R@{k}": round(recall_at(runs["rentok"][best], jobs[j], k), 3) for k in (20, 50)}
    out["truth_sources"] = {b: sorted({source_of[i] for i in t}) for b, t in truth.items()}
    (HERE / "results.json").write_text(json.dumps(out, indent=1))
    (HERE / "runs.json").write_text(json.dumps({b: {k: v[:100] for k, v in r.items()} for b, r in runs.items()}, indent=0))
    if pools:
        (HERE / "rerank-pool.json").write_text(json.dumps(pools, indent=1))

    print(f"corpus {n} claims; truth rentok={len(truth['rentok'])} mokobara={len(truth['mokobara'])}")
    print(f"packs: union {len(pack_ids)} ids ({len(pack_ids)/n:.0%} of corpus); recall rentok {out['packs_recall']['rentok']:.2f} mokobara {out['packs_recall']['mokobara']:.2f} (circular: packs were built to cover these ids)")
    print(f"random expected: " + " ".join(f"R@{k}={k/n:.3f}" for k in KS))
    hdr = "method".ljust(58) + "".join(f"{b[:3]}@{k}".rjust(8) for b in briefs for k in (10, 20, 50))
    print(hdr)
    for name, per in out["methods"].items():
        row = name.ljust(58)
        for b in briefs:
            for k in (10, 20, 50):
                v = per.get(b, {}).get(f"R@{k}")
                row += (f"{v:.2f}" if v is not None else "-").rjust(8)
        print(row)


if __name__ == "__main__":
    main()
