#!/usr/bin/env python3
"""EVAL-037 — the three read-only Canon tools exposed in the FULL_CANON condition.

  canon_catalog   what sources exist, and in what epistemic state
  canon_search    find items across knowledge, concept systems, bindings, ontology and Q&A
  canon_read      read a whole artifact, a whole source, or one item by id

NO_CANON lanes never import this module. The runner refuses to load it unless the
lane's condition is FULL_CANON.

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
default is unbounded.
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
    "visual_evidence": ("visual_evidence", "evidence_id"),
}


class CanonStatusError(RuntimeError):
    """Raised when the corpus cannot establish a status. Fails closed."""


def _load(p):
    with open(p, "r", encoding="utf-8") as fh:
        return yaml.load(fh, Loader=_Loader)


class Canon:
    def __init__(self, repo_root, condition="FULL_CANON", cache_dir=None):
        if condition != "FULL_CANON":
            raise PermissionError(
                f"Canon tools are exposed only in FULL_CANON; got condition={condition!r}")
        self.root = pathlib.Path(repo_root).resolve()
        self.index_path = self.root / "canon/knowledge/CANON-CORPUS-INDEX.yaml"
        self.qa_dir = self.root / "canon/qa/canon-014"
        self.cache_dir = pathlib.Path(cache_dir) if cache_dir else None
        self._index = None
        self._sources = None
        self._artifacts = {}
        self._flat = None

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

    # -- tool 2: canon_search ----------------------------------------------
    def canon_search(self, query, kinds=None, source_status=None, include_qa=True,
                     limit=None, fields=None):
        """Substring/regex search across the corpus.

        limit is the CALLER's own choice. The harness imposes no aggregate top-K,
        no token budget and no retrieval-count budget. Default: unbounded.
        """
        if not query or not str(query).strip():
            raise ValueError("query must be a non-empty string")
        if source_status is not None and source_status not in (ACCEPTED, HOLD):
            raise ValueError(f"source_status must be {ACCEPTED!r} or {HOLD!r}")
        try:
            rx = re.compile(query, re.I)
        except re.error:
            rx = re.compile(re.escape(query), re.I)
        hits = []
        for entry in self._flatten():
            if kinds and entry["kind"] not in kinds:
                continue
            if source_status and entry["source_status"] != source_status:
                continue
            if not include_qa and entry["kind"] == "qa":
                continue
            hay = _haystack(entry["item"], fields)
            if rx.search(hay):
                hits.append(_assert_status(entry))
        hits.sort(key=lambda e: (e["source_dir"], e["kind"], str(e["item_id"])))
        total = len(hits)
        if limit is not None:
            if not isinstance(limit, int) or limit < 1:
                raise ValueError("limit must be a positive integer or None")
            hits = hits[:limit]
        return {"query": query,
                "total_matches": total,
                "returned": len(hits),
                "limit_applied": limit,
                "limit_source": "caller" if limit is not None else "none (unbounded)",
                "accepted_matches": sum(1 for h in hits if h["source_status"] == ACCEPTED),
                "hold_matches": sum(1 for h in hits if h["source_status"] == HOLD),
                "status_note": "Each result carries its own source_status. HOLD is not accepted.",
                "results": hits}

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


def _haystack(item, fields=None):
    if fields:
        return json.dumps({k: item.get(k) for k in fields}, default=str)
    return json.dumps(item, default=str)


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
     "description": ("Search the knowledge library. Returns every match by default; there is no "
                     "imposed result cap. Each result states its own source_status."),
     "input_schema": {"type": "object", "properties": {
         "query": {"type": "string", "description": "Substring or regular expression."},
         "kinds": {"type": "array", "items": {"type": "string", "enum": [
             "knowledge", "concept_system", "binding", "ontology_term",
             "ontology_concept", "qa", "visual_evidence"]}},
         "source_status": {"type": "string", "enum": [ACCEPTED, HOLD]},
         "include_qa": {"type": "boolean", "default": True},
         "limit": {"type": "integer", "minimum": 1,
                   "description": "Optional cap you choose. Omit for all matches."}},
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
