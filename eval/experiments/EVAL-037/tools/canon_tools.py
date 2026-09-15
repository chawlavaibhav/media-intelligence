#!/usr/bin/env python3
"""EVAL-037 — the three read-only Canon tools exposed in the FULL_CANON condition.

  canon_catalog   what sources exist, and in what epistemic state
  canon_search    deterministic tokenized BM25 ranked retrieval across SourceKnowledge,
                  concept systems, operational bindings, ontology, visual-evidence
                  items and Q&A. No embedding and no model call anywhere.
  canon_read      read a whole artifact, a whole source, or one item by id

NO_CANON lanes never import this module. The runner refuses to load it unless the
lane's condition is one of the Canon conditions: FULL_CANON, or CONTROLLED_CANON (the
supplemental objective-driven-retrieval treatment). Those two conditions get BYTE-
IDENTICAL tools, corpus, ranking and status semantics from this module — nothing here
is aware of which one is running. In particular CONTROLLED_CANON's retrieval allowance
is NOT implemented here: it is a behaviour asked of the model in the prompt, measured
after the fact, and never a cap inside the tool.

Hard invariants, enforced here and tested by validators/test_canon_tools.py:

  * every returned object carries source_status, verbatim-derived from the corpus index
    ('accepted' -> 'ACCEPTED', 'hold' -> 'HOLD')
  * HOLD is never represented, defaulted or relabelled as ACCEPTED
  * an object whose status cannot be established is DROPPED, never returned with a guess
  * Q&A objects additionally carry not_benchmark_ground_truth: true and
    independent_corroboration: false
  * read-only: this module opens no file for writing inside the canon tree

The harness imposes NO aggregate top-K, NO token budget and NO retrieval-count budget.
`limit` exists only so the tested model can bound its own result set if it chooses; the
default is unbounded — every scoring item is returned, ranked.

Ranking is BM25 (k1=1.2, b=0.75) over a deterministic tokenization, with ties broken
on (-score, source_dir, kind, item_id) so the same query always returns the same order
on the same corpus. Nothing here is stochastic and nothing calls a model.
"""
import hashlib
import json
import os
import pathlib
import re

import yaml

try:
    from yaml import CSafeLoader as _Loader
except ImportError:  # pragma: no cover
    from yaml import SafeLoader as _Loader

# Conditions permitted to construct the Canon tools. Same corpus, same tools, same
# ranking, same status semantics for every one of them.
CANON_CONDITIONS = ("FULL_CANON", "CONTROLLED_CANON")

ACCEPTED = "ACCEPTED"
HOLD = "HOLD"
_STATUS = {"accepted": ACCEPTED, "hold": HOLD}

ARTIFACTS = ["source-knowledge.yaml", "source-concept-systems.yaml",
             "operational-bindings.yaml", "ontology-mappings.yaml",
             "visual-evidence-ledger.yaml"]

# item list key -> (kind, id field)
_ITEM_LISTS = {
    "source_knowledge": ("knowledge", "sk_id"),
    "source_concept_systems": ("concept_system", "scs_id"),
    "operational_bindings": ("binding", "binding_id"),
    "terms": ("ontology_term", "term_id"),
    "concepts": ("ontology_concept", "concept_id"),
    "qa_items": ("qa", "qa_id"),
    # visual-evidence ledgers carry two item lists, both keyed on `ref`
    "demonstrations": ("visual_evidence", "ref"),
    "visual_only_observations": ("visual_evidence", "ref"),
}


class CanonStatusError(RuntimeError):
    """Raised when the corpus cannot establish a status. Fails closed."""


_TOKEN_RE = re.compile(r"[a-z0-9]+")

# BM25 constants, fixed at freeze. Standard defaults; not tuned against the corpus.
BM25_K1 = 1.2
BM25_B = 0.75

# Process-level cache of the flattened corpus and its BM25 index, keyed by repo root.
# Safe by construction: both are pure functions of immutable, read-only corpus bytes.
# NO trial state is involved, so sharing them across trials carries nothing between
# trials. Rebuilding per trial would only burn wall-clock.
_CORPUS_CACHE = {}


def tokenize(text):
    """Deterministic tokenizer: lowercase, split on non-alphanumerics, drop 1-char tokens.

    No stemming and no stopword list — both would be tuning decisions that quietly
    shape what the tested model can find.
    """
    return [t for t in _TOKEN_RE.findall(str(text).lower()) if len(t) > 1]


def _text_of(item):
    """Flatten every string leaf of an item into one searchable document."""
    out = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                out.append(str(k)); walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        elif o is not None and not isinstance(o, bool):
            out.append(str(o))

    walk(item)
    return " ".join(out)


def _load(p):
    with open(p, "r", encoding="utf-8") as fh:
        return yaml.load(fh, Loader=_Loader)


class Canon:
    def __init__(self, repo_root, condition="FULL_CANON", cache_dir=None):
        if condition not in CANON_CONDITIONS:
            raise PermissionError(
                f"Canon tools are exposed only in {'/'.join(CANON_CONDITIONS)}; "
                f"got condition={condition!r}")
        self.root = pathlib.Path(repo_root).resolve()
        self.index_path = self.root / "canon/knowledge/CANON-CORPUS-INDEX.yaml"
        self.qa_dir = self.root / "canon/qa/canon-014"
        self.cache_dir = pathlib.Path(cache_dir) if cache_dir else None
        self._index = None
        self._sources = None
        self._artifacts = _CORPUS_CACHE.setdefault(("artifacts", str(self.root)), {})
        self._titles = _CORPUS_CACHE.setdefault(("titles", str(self.root)), {})
        self._flat = None
        self._bm25 = None

    # -- corpus map ---------------------------------------------------------
    @property
    def index(self):
        if self._index is None:
            self._index = _load(self.index_path)
        return self._index

    @property
    def sources(self):
        """source_dir -> record, with source_status resolved. Unresolvable rows are dropped."""
        if self._sources is None:
            out = {}
            for s in self.index["sources"]:
                st = _STATUS.get(s.get("epistemic_status"))
                if st is None:
                    continue  # fail closed: no guessed status, no exposure
                rec = dict(s)
                rec["source_status"] = st
                rec["location"] = s["location"]
                out[s["source_dir"]] = rec
            self._sources = out
        return self._sources

    def _status_of(self, source_dir):
        rec = self.sources.get(source_dir)
        if rec is None:
            raise CanonStatusError(f"no status for source_dir={source_dir!r}")
        return rec["source_status"]

    def _qa_bank_path(self, source_dir):
        p = self.qa_dir / f"{source_dir}-qa-bank.yaml"
        return p if p.exists() else None

    def _title(self, source_dir):
        """Title only where the corpus states one. Never invented."""
        if source_dir in self._titles:
            return self._titles[source_dir]
        self._titles[source_dir] = t = self._title_uncached(source_dir)
        return t

    def _title_uncached(self, source_dir):
        qb = self._qa_bank_path(source_dir)
        if qb:
            items = (_load(qb) or {}).get("qa_items") or []
            if items and items[0].get("source_title"):
                return items[0]["source_title"]
        rec = self.sources.get(source_dir) or {}
        hold = self.root / rec.get("location", "") / "audit-assessment-HOLD.yaml"
        if hold.exists():
            return (_load(hold) or {}).get("title")
        return None

    # -- tool 1: canon_catalog ---------------------------------------------
    def canon_catalog(self, source_status=None, has_qa=None):
        """List the corpus. `source_status` optionally filters to ACCEPTED or HOLD."""
        if source_status is not None and source_status not in (ACCEPTED, HOLD):
            raise ValueError(f"source_status must be {ACCEPTED!r} or {HOLD!r}")
        rows = []
        for sd, rec in sorted(self.sources.items()):
            if source_status and rec["source_status"] != source_status:
                continue
            qb = self._qa_bank_path(sd)
            if has_qa is not None and bool(qb) != bool(has_qa):
                continue
            row = {
                "source_dir": sd,
                "source_id": rec.get("source_id"),
                "source_status": rec["source_status"],          # never omitted
                "title": self._title(sd),
                "location": rec["location"],
                "counts": {k: rec.get(k) for k in
                           ("source_knowledge", "concept_systems", "operational_bindings",
                            "ontology_terms", "ontology_concepts", "ontology_relationships")},
                "artifacts": [a for a in ARTIFACTS
                              if (self.root / rec["location"] / a).exists()],
                "qa_bank": str(qb.relative_to(self.root)) if qb else None,
                "visual_evidence": rec.get("visual_evidence"),
            }
            if rec["source_status"] == HOLD:
                row["hold_blocker"] = rec.get("candidate_blocker")
                row["caution"] = ("HOLD: unresolved evidence or representation blocker. "
                                  "Not accepted Canon. Treat cautiously.")
            else:
                row["audit"] = rec.get("audit")
            rows.append(_assert_status(row))
        return {"corpus": "canon-014 full status-aware corpus",
                "total": len(rows),
                "accepted": sum(1 for r in rows if r["source_status"] == ACCEPTED),
                "hold": sum(1 for r in rows if r["source_status"] == HOLD),
                "status_note": ("ACCEPTED passed the project's Audit Gate. HOLD did not and is "
                                "never equivalent to accepted. Q&A is not benchmark truth."),
                "sources": rows}

    # -- artifact loading ---------------------------------------------------
    def _artifact(self, source_dir, artifact):
        key = (source_dir, artifact)
        if key in self._artifacts:
            return self._artifacts[key]
        rec = self.sources.get(source_dir)
        if rec is None:
            raise CanonStatusError(f"unknown source_dir={source_dir!r}")
        if artifact == "qa-bank.yaml":
            p = self._qa_bank_path(source_dir)
        else:
            if artifact not in ARTIFACTS:
                raise ValueError(f"unknown artifact {artifact!r}")
            p = self.root / rec["location"] / artifact
            p = p if p.exists() else None
        data = _load(p) if p else None
        self._artifacts[key] = data
        return data

    def _items_of(self, source_dir, artifact):
        """Yield (kind, id, item) for every list-shaped item in an artifact."""
        data = self._artifact(source_dir, artifact)
        if not isinstance(data, dict):
            return
        for list_key, (kind, id_field) in _ITEM_LISTS.items():
            for item in (data.get(list_key) or []):
                if isinstance(item, dict):
                    yield kind, item.get(id_field), item

    def _flatten(self):
        """One pass over the whole corpus. Every item is stamped with its source_status."""
        if self._flat is not None:
            return self._flat
        ck = ("flat", str(self.root))
        if ck in _CORPUS_CACHE:
            self._flat = _CORPUS_CACHE[ck]
            return self._flat
        flat = []
        for sd, rec in sorted(self.sources.items()):
            try:
                status = self._status_of(sd)
            except CanonStatusError:
                continue  # fail closed
            arts = [a for a in ARTIFACTS if (self.root / rec["location"] / a).exists()]
            if self._qa_bank_path(sd):
                arts.append("qa-bank.yaml")
            for artifact in arts:
                for kind, iid, item in self._items_of(sd, artifact):
                    flat.append(_stamp(item, sd, rec.get("source_id"), status, kind, iid, artifact))
        self._flat = flat
        return flat

    # -- BM25 index ---------------------------------------------------------
    def _bm25_index(self):
        """Build the BM25 index once per process. Pure function of the corpus bytes."""
        if getattr(self, "_bm25", None) is not None:
            return self._bm25
        ck = ("bm25", str(self.root))
        if ck in _CORPUS_CACHE:
            self._bm25 = _CORPUS_CACHE[ck]
            return self._bm25
        import math
        docs, df = [], {}
        for entry in self._flatten():
            toks = tokenize(_text_of(entry["item"]))
            tf = {}
            for t in toks:
                tf[t] = tf.get(t, 0) + 1
            for t in tf:
                df[t] = df.get(t, 0) + 1
            docs.append({"entry": entry, "tf": tf, "len": len(toks)})
        n = len(docs)
        avgdl = (sum(d["len"] for d in docs) / n) if n else 0.0
        idf = {t: math.log(1.0 + (n - c + 0.5) / (c + 0.5)) for t, c in df.items()}
        self._bm25 = _CORPUS_CACHE[ck] = {"docs": docs, "idf": idf, "avgdl": avgdl,
                                          "n": n}
        return self._bm25

    # -- tool 2: canon_search ----------------------------------------------
    def canon_search(self, query, kinds=None, source_status=None, include_qa=True,
                     limit=None, min_score=0.0):
        """Deterministic BM25 ranked retrieval across the whole corpus.

        Every item kind is searched: SourceKnowledge, concept systems, operational
        bindings, ontology terms and concepts, visual-evidence items, and Q&A.

        `limit` is the CALLER's own choice. The harness imposes no aggregate top-K, no
        token budget and no retrieval-count budget. Default: every scoring item,
        ranked.
        """
        if not query or not str(query).strip():
            raise ValueError("query must be a non-empty string")
        if source_status is not None and source_status not in (ACCEPTED, HOLD):
            raise ValueError(f"source_status must be {ACCEPTED!r} or {HOLD!r}")
        q = tokenize(query)
        if not q:
            raise ValueError("query contained no searchable tokens")
        ix = self._bm25_index()
        idf, avgdl = ix["idf"], ix["avgdl"]

        scored = []
        for d in ix["docs"]:
            entry = d["entry"]
            if kinds and entry["kind"] not in kinds:
                continue
            if source_status and entry["source_status"] != source_status:
                continue
            if not include_qa and entry["kind"] == "qa":
                continue
            tf, dl = d["tf"], d["len"]
            score, matched = 0.0, []
            for t in q:
                f = tf.get(t)
                if not f:
                    continue
                matched.append(t)
                denom = f + BM25_K1 * (1 - BM25_B + BM25_B * (dl / avgdl if avgdl else 1))
                score += idf.get(t, 0.0) * (f * (BM25_K1 + 1)) / denom
            if score > min_score:
                scored.append((score, sorted(set(matched)), entry))

        scored.sort(key=lambda r: (-r[0], r[2]["source_dir"], r[2]["kind"],
                                   str(r[2]["item_id"])))
        total = len(scored)
        if limit is not None:
            if not isinstance(limit, int) or limit < 1:
                raise ValueError("limit must be a positive integer or None")
            scored = scored[:limit]

        results = []
        for rank, (score, matched, entry) in enumerate(scored, 1):
            r = dict(entry)
            r["rank"] = rank
            r["score"] = round(score, 6)
            r["matched_query_terms"] = matched
            results.append(_assert_status(r))

        return {"query": query,
                "query_tokens": q,
                "ranking": "BM25 k1=1.2 b=0.75, deterministic tokenization, no model call",
                "total_matches": total,
                "returned": len(results),
                "limit_applied": limit,
                "limit_source": "caller" if limit is not None else "none (unbounded)",
                "accepted_matches": sum(1 for r in results if r["source_status"] == ACCEPTED),
                "hold_matches": sum(1 for r in results if r["source_status"] == HOLD),
                "qa_matches": sum(1 for r in results if r["kind"] == "qa"),
                "status_note": "Each result carries its own source_status. HOLD is not accepted.",
                "results": results}

    # -- tool 3: canon_read -------------------------------------------------
    def canon_read(self, source_dir=None, artifact=None, item_id=None):
        """Read one artifact of one source, or one item by id, or a source overview."""
        if item_id:
            for entry in self._flatten():
                if str(entry["item_id"]) == str(item_id):
                    return _assert_status(entry)
            return {"item_id": item_id, "found": False,
                    "note": "No item with that id in the corpus."}
        if not source_dir:
            raise ValueError("canon_read needs source_dir or item_id")
        if source_dir not in self.sources:
            return {"source_dir": source_dir, "found": False,
                    "note": "Unknown source. Call canon_catalog for the list."}
        status = self._status_of(source_dir)
        rec = self.sources[source_dir]
        if artifact is None:
            avail = [a for a in ARTIFACTS if (self.root / rec["location"] / a).exists()]
            if self._qa_bank_path(source_dir):
                avail.append("qa-bank.yaml")
            return _assert_status({
                "source_dir": source_dir, "source_id": rec.get("source_id"),
                "source_status": status, "title": self._title(source_dir),
                "available_artifacts": avail, "counts": rec,
                "note": "Pass artifact= to read one."})
        items = [_stamp(it, source_dir, rec.get("source_id"), status, kind, iid, artifact)
                 for kind, iid, it in self._items_of(source_dir, artifact)]
        if not items and self._artifact(source_dir, artifact) is None:
            return {"source_dir": source_dir, "artifact": artifact, "found": False,
                    "source_status": status,
                    "note": "This source does not carry that artifact."}
        return {"source_dir": source_dir, "source_id": rec.get("source_id"),
                "artifact": artifact, "source_status": status,
                "item_count": len(items),
                "status_note": ("HOLD material is not accepted Canon."
                                if status == HOLD else "Passed the project's Audit Gate."),
                "items": [_assert_status(i) for i in items]}


# -- helpers ---------------------------------------------------------------
def _stamp(item, source_dir, source_id, status, kind, item_id, artifact):
    """Wrap a raw corpus item in an envelope that always states its status."""
    env = {"source_dir": source_dir, "source_id": source_id,
           "source_status": status, "kind": kind, "item_id": item_id,
           "artifact": artifact, "item": item}
    if kind == "qa":
        env["not_benchmark_ground_truth"] = True
        env["independent_corroboration"] = False
        env["representation_note"] = ("Q&A is an alternate grounded representation of the same "
                                      "source. It corroborates nothing on its own.")
    if status == HOLD:
        env["caution"] = ("HOLD: unresolved evidence or representation blocker. "
                          "Not accepted Canon.")
    return env


def _assert_status(obj):
    """Last line of defence. Nothing leaves without a real status."""
    st = obj.get("source_status")
    if st not in (ACCEPTED, HOLD):
        raise CanonStatusError(f"refusing to return an object without a valid source_status: {st!r}")
    return obj


# -- tool schemas exposed to the provider ----------------------------------
TOOL_SCHEMAS = [
    {"name": "canon_catalog",
     "description": ("List every source in the media-production knowledge library, with its "
                     "epistemic status (ACCEPTED or HOLD), counts and available artifacts."),
     "input_schema": {"type": "object", "properties": {
         "source_status": {"type": "string", "enum": [ACCEPTED, HOLD],
                           "description": "Optional filter."},
         "has_qa": {"type": "boolean", "description": "Optional: only sources with a Q&A bank."}},
         "required": []}},
    {"name": "canon_search",
     "description": ("Ranked lexical (BM25) search across the whole knowledge library: "
                     "source knowledge, concept systems, operational bindings, ontology "
                     "terms and concepts, visual-evidence items and Q&A. Returns every "
                     "scoring item by default, best first; there is no imposed result "
                     "cap. Each result states its own source_status."),
     "input_schema": {"type": "object", "properties": {
         "query": {"type": "string", "description": "Free-text query. Ranked by BM25."},
         "kinds": {"type": "array", "items": {"type": "string", "enum": [
             "knowledge", "concept_system", "binding", "ontology_term",
             "ontology_concept", "qa", "visual_evidence"]}},
         "source_status": {"type": "string", "enum": [ACCEPTED, HOLD]},
         "include_qa": {"type": "boolean", "default": True},
         "limit": {"type": "integer", "minimum": 1,
                   "description": "Optional cap you choose. Omit for all matches."},
         "min_score": {"type": "number",
                       "description": "Optional BM25 score floor. Default 0."}},
         "required": ["query"]}},
    {"name": "canon_read",
     "description": ("Read one source's artifact, one source's overview, or one item by id. "
                     "Artifacts: source-knowledge.yaml, source-concept-systems.yaml, "
                     "operational-bindings.yaml, ontology-mappings.yaml, "
                     "visual-evidence-ledger.yaml, qa-bank.yaml."),
     "input_schema": {"type": "object", "properties": {
         "source_dir": {"type": "string"},
         "artifact": {"type": "string"},
         "item_id": {"type": "string"}},
         "required": []}},
]

TOOL_NAMES = [t["name"] for t in TOOL_SCHEMAS]


def dispatch(canon, name, args):
    if name not in TOOL_NAMES:
        raise ValueError(f"tool {name!r} is not exposed in EVAL-037")
    return getattr(canon, name)(**(args or {}))
