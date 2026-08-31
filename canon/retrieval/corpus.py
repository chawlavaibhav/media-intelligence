"""Read-only accepted-Canon corpus: load it once, type it, and never guess a status.

Scope is deliberately narrower than EVAL-037's `canon_tools.py`. That module searched the
whole status-aware corpus — accepted knowledge, HOLD candidates and the Q&A banks — in one
surface, and left it to the caller to notice which was which. Here the production surface
is `canon/knowledge/current/**` only, exactly as
`coordination/decisions/CONTROLLER-CANON-014-INTEGRATION-2026-08-30.md` requires. HOLD and
Q&A can be loaded, but only by asking for them explicitly and by naming a diagnostic
reason, and a bundle built that way is stamped `production_default: false`.

Three things this module does that the EVAL-037 loader did not:

1. **Separates index text from presented text.** `canon_tools._text_of` flattened every
   string leaf of an item — dictionary KEYS included — into one searchable document, so a
   query for "product hero composition" could score on the literal words `provenance`,
   `source_support` or `explicitly_stated`. Here each kind declares which fields carry
   content and which are metadata. Metadata is preserved on the way out and excluded from
   the index.

2. **Keeps the epistemic fields structurally.** Every item carries its claim type,
   evidence characteristics, both uncertainty fields, its caveats WITH their origin
   (source-stated or extractor-observed), and — for operational bindings — the fact that
   141 of the 152 accepted bindings still carry `status: proposed`, meaning nobody has
   reviewed them. A bundle that drops that turns a cautious source claim into a rule.

3. **Records lineage groups.** The Audit Gate records which sources are NOT independent of
   each other. `grammar-of-the-shot` and `grammar-of-the-edit` are companion volumes by the
   same authors; `murch-blink` and `ondaatje-conversations` are the same practitioner
   speaking under two author names. Two members of one group agreeing is one origin
   agreeing with itself, so the ranker shares one budget between them.

Nothing here scores, rates or ranks a source. Audit Gate v0.2's anti-score rule governs
audit records rather than this module, but its reasoning applies: the only ordering this
package produces is query relevance, which is a statement about the query and not about
the knowledge.
"""
import hashlib
import pathlib
import re

import yaml

try:
    from yaml import CSafeLoader as _Loader
except ImportError:  # pragma: no cover - CSafeLoader is present on this machine
    from yaml import SafeLoader as _Loader

from canon.validation.validate_audit_gate_v02 import DEPENDENT_RELATIONS

ACCEPTED = "ACCEPTED"
HOLD = "HOLD"
_STATUS = {"accepted": ACCEPTED, "hold": HOLD}

INDEX_PATH = "canon/knowledge/CANON-CORPUS-INDEX.yaml"
AUDIT_RECORDS_DIR = "canon/audit/records"
QA_DIR = "canon/qa/canon-014"

KIND_KNOWLEDGE = "knowledge"
KIND_CONCEPT_SYSTEM = "concept_system"
KIND_BINDING = "binding"
KIND_ONTOLOGY_TERM = "ontology_term"
KIND_ONTOLOGY_CONCEPT = "ontology_concept"
KIND_VISUAL_EVIDENCE = "visual_evidence"
KIND_QA = "qa"

ALL_KINDS = (KIND_KNOWLEDGE, KIND_CONCEPT_SYSTEM, KIND_BINDING,
             KIND_ONTOLOGY_TERM, KIND_ONTOLOGY_CONCEPT, KIND_VISUAL_EVIDENCE)


class CanonStatusError(RuntimeError):
    """Raised when a source's accepted/HOLD status cannot be established. Fails closed."""


class CorpusError(RuntimeError):
    """Raised when the corpus index itself is missing or unreadable."""


_TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text):
    """Lowercase, split on non-alphanumerics, drop one-character tokens.

    Identical to EVAL-037's tokenizer on purpose: no stemming and no stopword list, so a
    before/after comparison measures what changed in retrieval rather than in tokenizing.
    """
    return [t for t in _TOKEN_RE.findall(str(text).lower()) if len(t) > 1]


def _load_yaml(path):
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.load(fh, Loader=_Loader)


def _texts(*values):
    """Flatten content values into indexable strings. Dict KEYS are never indexed."""
    out = []

    def walk(v):
        if isinstance(v, dict):
            for inner in v.values():
                walk(inner)
        elif isinstance(v, (list, tuple)):
            for inner in v:
                walk(inner)
        elif isinstance(v, str):
            out.append(v)
        elif isinstance(v, (int, float)) and not isinstance(v, bool):
            out.append(str(v))

    for value in values:
        walk(value)
    return out


def _get(item, *path, default=None):
    cur = item
    for key in path:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(key)
    return default if cur is None else cur


class CanonItem:
    """One retrievable Canon object, typed, with its status and epistemics attached."""

    __slots__ = ("source_dir", "source_id", "source_title", "source_status", "kind",
                 "item_id", "artifact", "lineage_group", "index_text", "payload",
                 "_tokens")

    def __init__(self, *, source_dir, source_id, source_title, source_status, kind,
                 item_id, artifact, lineage_group, index_text, payload):
        if source_status not in (ACCEPTED, HOLD):
            raise CanonStatusError(
                f"refusing to build an item without a real source_status: {source_status!r}")
        self.source_dir = source_dir
        self.source_id = source_id
        self.source_title = source_title
        self.source_status = source_status
        self.kind = kind
        self.item_id = item_id
        self.artifact = artifact
        self.lineage_group = lineage_group
        self.index_text = index_text
        self.payload = payload
        self._tokens = None

    @property
    def tokens(self):
        if self._tokens is None:
            self._tokens = tokenize(self.index_text)
        return self._tokens

    @property
    def detail_ref(self):
        """How a caller would fetch this object in full, if it ever needed to."""
        return {"source_dir": self.source_dir, "artifact": self.artifact,
                "item_id": self.item_id}

    def __repr__(self):  # pragma: no cover - debugging aid
        return f"<CanonItem {self.kind} {self.item_id} {self.source_dir}>"


# ── per-kind field mapping ──────────────────────────────────────────────────────────
# Each builder returns (index_text_parts, payload). `payload` is assembled from verbatim
# field values; nothing is paraphrased, summarised or rewritten anywhere in this package.

def _build_knowledge(item):
    payload = {
        "concept_label": item.get("concept_label"),
        "label_origin": item.get("label_origin"),
        "source_terms": item.get("source_terms") or [],
        "claim": item.get("claim"),
        "claim_type": item.get("claim_type"),
        "interpretation_basis": item.get("interpretation_basis"),
        "mechanism": item.get("mechanism") or {},
        "scope": item.get("scope") or {},
        "caveats": item.get("caveats") or [],
        "source_stated_problems": item.get("source_stated_problems") or [],
        "source_stated_remedies": item.get("source_stated_remedies") or [],
        "evidence": item.get("evidence") or {},
        "provenance": item.get("provenance") or {},
    }
    parts = _texts(
        item.get("concept_label"), item.get("source_terms"), item.get("claim"),
        _get(item, "mechanism", "text"), _get(item, "scope", "domain_discussed_by_source"),
        _get(item, "scope", "conditions"),
        [c.get("text") for c in (item.get("caveats") or []) if isinstance(c, dict)],
        item.get("source_stated_problems"), item.get("source_stated_remedies"),
        [e.get("description") for kindlist in (item.get("examples") or {}).values()
         if isinstance(kindlist, list) for e in kindlist if isinstance(e, dict)],
        item.get("interpretation_basis"),
    )
    return parts, payload


def _build_concept_system(item):
    payload = {
        "label": item.get("label"),
        "system_type": item.get("system_type"),
        "system_type_origin": item.get("system_type_origin"),
        "description": item.get("description"),
        "whole_system_claim": item.get("whole_system_claim") or {},
        "members": [{"sk_ref": m.get("sk_ref"), "role_in_system": m.get("role_in_system"),
                     "membership_origin": m.get("membership_origin")}
                    for m in (item.get("members") or []) if isinstance(m, dict)],
        "tradeoffs": _get(item, "internal_structure", "tradeoffs", default=[]),
        "conflicts": _get(item, "internal_structure", "conflicts", default=[]),
        "source_warns_against_isolated_use": item.get("source_warns_against_isolated_use"),
        "evidence": item.get("evidence") or {},
        "provenance": item.get("provenance") or {},
    }
    parts = _texts(
        item.get("label"), item.get("description"), item.get("system_type"),
        _get(item, "whole_system_claim", "text"),
        _get(item, "whole_system_claim", "interpretation_basis"),
        [t.get("nature") for t in _get(item, "internal_structure", "tradeoffs", default=[])
         if isinstance(t, dict)],
        [d.get("nature") for d in _get(item, "internal_structure", "dependencies", default=[])
         if isinstance(d, dict)],
        [m.get("role_in_system") for m in (item.get("members") or []) if isinstance(m, dict)],
    )
    return parts, payload


def _build_binding(item):
    payload = {
        "target_type": item.get("target_type"),
        "target_path": item.get("target_path"),
        "target_schema": item.get("target_schema"),
        "target_schema_version": item.get("target_schema_version"),
        "role": item.get("role") or [],
        "rationale": item.get("rationale"),
        "applicability": item.get("applicability") or {},
        "evidence_basis": item.get("evidence_basis"),
        "empirical_refs": item.get("empirical_refs") or [],
        "observation_unit": item.get("observation_unit"),
        "status": item.get("status"),
        "status_reason": item.get("status_reason"),
        "source_knowledge_refs": item.get("source_knowledge_refs") or [],
        "source_system_refs": item.get("source_system_refs") or [],
    }
    parts = _texts(
        item.get("rationale"), _get(item, "applicability", "when"),
        _get(item, "applicability", "limits"), item.get("target_path"),
        item.get("target_type"), item.get("role"),
    )
    return parts, payload


def _build_ontology_term(item):
    payload = {
        "term": item.get("term"),
        "kind": item.get("kind"),
        "origin": item.get("origin"),
        "origin_ref": item.get("origin_ref"),
        "verbatim": item.get("verbatim"),
        "definition_in_origin_frame": item.get("definition_in_origin_frame"),
        "arising_from": item.get("arising_from") or [],
        "source_ref": item.get("source_ref") or {},
    }
    parts = _texts(item.get("term"), item.get("definition_in_origin_frame"), item.get("kind"))
    return parts, payload


def _build_ontology_concept(item):
    payload = {
        "label": item.get("label"),
        "kind": item.get("kind"),
        "origin": item.get("origin"),
        "origin_ref": item.get("origin_ref"),
        "definition": item.get("definition"),
        "purpose": item.get("purpose"),
        "basis": item.get("basis"),
        "created_by": item.get("created_by"),
        # Load-bearing: a canonical_concept groups terms for retrieval and asserts
        # nothing about them being the same thing.
        "asserts_equivalence": item.get("asserts_equivalence"),
        "asserts_agreement_between_sources": item.get("asserts_agreement_between_sources"),
        "children_terms": item.get("children_terms") or [],
        "independent_origins": item.get("independent_origins") or [],
        "status": item.get("status"),
    }
    parts = _texts(item.get("label"), item.get("definition"), item.get("basis"),
                   item.get("kind"))
    return parts, payload


def _build_visual_evidence(item):
    payload = {
        "kind_of_visual": item.get("kind"),
        "status": item.get("status"),
        "strength": item.get("strength"),
        "visible_difference": item.get("visible_difference"),
        "what_is_visible": item.get("what_is_visible"),
        "observation": item.get("observation"),
        "what_the_visual_supports": item.get("what_the_visual_supports"),
        "why_it_matters": item.get("why_it_matters"),
        "requires_prose": item.get("requires_prose"),
        "lost_in_plain_text": item.get("lost_in_plain_text"),
        "colour_dependent": item.get("colour_dependent"),
        "promoted_to_source_claim": item.get("promoted_to_source_claim"),
        "chapter": item.get("chapter"),
        "pdf_page": item.get("pdf_page"),
    }
    parts = _texts(item.get("visible_difference"), item.get("what_the_visual_supports"),
                   item.get("observation"), item.get("why_it_matters"),
                   item.get("what_is_visible"), item.get("requires_prose"),
                   item.get("kind"))
    return parts, payload


def _build_qa(item):
    payload = {
        "question": item.get("question"),
        "answer": item.get("answer"),
        "grounded_in": item.get("grounded_in") or item.get("sk_refs") or [],
        "not_benchmark_ground_truth": True,
        "independent_corroboration": False,
    }
    parts = _texts(item.get("question"), item.get("answer"))
    return parts, payload


# artifact -> list of (yaml list key, kind, id field, builder)
_ARTIFACT_ITEMS = {
    "source-knowledge.yaml": [
        ("source_knowledge", KIND_KNOWLEDGE, "sk_id", _build_knowledge)],
    "source-concept-systems.yaml": [
        ("source_concept_systems", KIND_CONCEPT_SYSTEM, "scs_id", _build_concept_system)],
    "operational-bindings.yaml": [
        ("operational_bindings", KIND_BINDING, "binding_id", _build_binding)],
    "ontology-mappings.yaml": [
        ("terms", KIND_ONTOLOGY_TERM, "term_id", _build_ontology_term),
        ("concepts", KIND_ONTOLOGY_CONCEPT, "concept_id", _build_ontology_concept)],
    "visual-evidence-ledger.yaml": [
        ("demonstrations", KIND_VISUAL_EVIDENCE, "ref", _build_visual_evidence),
        ("visual_only_observations", KIND_VISUAL_EVIDENCE, "ref", _build_visual_evidence)],
    "qa-bank.yaml": [("qa_items", KIND_QA, "qa_id", _build_qa)],
}

ARTIFACTS = [a for a in _ARTIFACT_ITEMS if a != "qa-bank.yaml"]


class AcceptedCanon:
    """The accepted-Canon retrieval surface.

    `include_hold` and `include_qa` exist for development diagnostics and both require a
    non-empty `diagnostic_reason`. Anything loaded that way marks the corpus
    `production_default = False`, and that flag travels onto every bundle built from it.
    """

    def __init__(self, repo_root=".", *, include_hold=False, include_qa=False,
                 diagnostic_reason=None):
        if (include_hold or include_qa) and not (diagnostic_reason or "").strip():
            raise CanonStatusError(
                "include_hold/include_qa are diagnostic-only and require diagnostic_reason. "
                "The production default is accepted Canon under canon/knowledge/current/**.")
        self.root = pathlib.Path(repo_root).resolve()
        self.include_hold = bool(include_hold)
        self.include_qa = bool(include_qa)
        self.diagnostic_reason = diagnostic_reason if (include_hold or include_qa) else None
        self.production_default = not (include_hold or include_qa)

        index_path = self.root / INDEX_PATH
        if not index_path.exists():
            raise CorpusError(f"corpus index not found at {index_path}")
        self._index = _load_yaml(index_path)
        if not isinstance(self._index, dict) or not self._index.get("sources"):
            raise CorpusError(f"corpus index at {index_path} carries no sources")

        self.excluded_sources = []
        self.sources = self._resolve_sources()
        self._audit = self._load_audit_records()
        self.lineage_groups = self._build_lineage_groups()
        self.items = self._flatten()
        self.fingerprint = self._fingerprint()

    # -- sources ------------------------------------------------------------
    def _resolve_sources(self):
        wanted = {ACCEPTED} | ({HOLD} if self.include_hold else set())
        out = {}
        for record in self._index["sources"]:
            source_dir = record.get("source_dir")
            status = _STATUS.get(record.get("epistemic_status"))
            if status is None:
                # Fail closed. A source whose status the index cannot state is not
                # exposed at all, and the exclusion is reported rather than silent.
                self.excluded_sources.append(
                    {"source_dir": source_dir, "reason": "status_not_established",
                     "epistemic_status": record.get("epistemic_status")})
                continue
            if status not in wanted:
                continue
            location = record.get("location")
            if not location or not (self.root / location).is_dir():
                self.excluded_sources.append(
                    {"source_dir": source_dir, "reason": "location_missing",
                     "location": location})
                continue
            rec = dict(record)
            rec["source_status"] = status
            out[source_dir] = rec

        # A directory sitting in the accepted tree that the index does not name is also
        # excluded. Presence on disk is not admission; only the index plus an Audit Gate
        # record makes a source accepted.
        current = self.root / "canon/knowledge/current"
        if current.is_dir():
            for child in sorted(p for p in current.iterdir() if p.is_dir()):
                if child.name not in out and not any(
                        e["source_dir"] == child.name for e in self.excluded_sources):
                    self.excluded_sources.append(
                        {"source_dir": child.name,
                         "reason": "present_on_disk_but_not_in_corpus_index"})
        return out

    def _load_audit_records(self):
        out = {}
        records_dir = self.root / AUDIT_RECORDS_DIR
        if not records_dir.is_dir():
            return out
        for path in sorted(records_dir.glob("*.audit.yaml")):
            record = _load_yaml(path)
            if isinstance(record, dict) and record.get("source_id"):
                out[record["source_id"]] = record
        return out

    def _build_lineage_groups(self):
        """Connected components over the Audit Gate's dependence-creating relations.

        `DEPENDENT_RELATIONS` is imported from the Audit Gate validator rather than
        restated, so this package can never drift from the promotion rule it borrows.
        A group id is the alphabetically first source_id in the component, which keeps
        it stable across runs.
        """
        parent = {sid: sid for sid in self._audit}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                lo, hi = sorted((ra, rb))
                parent[hi] = lo

        for source_id, record in self._audit.items():
            lineage = record.get("lineage") if isinstance(record.get("lineage"), dict) else {}
            for entry in lineage.get("related_sources_in_corpus") or []:
                if not isinstance(entry, dict):
                    continue
                other = entry.get("source_id")
                if entry.get("relation") in DEPENDENT_RELATIONS and other in parent:
                    union(source_id, other)
        return {sid: find(sid) for sid in parent}

    def lineage_group_of(self, source_id):
        """The independence group a source belongs to; itself when it stands alone."""
        return self.lineage_groups.get(source_id, source_id)

    # -- titles -------------------------------------------------------------
    def _title(self, source_dir, record):
        """A human-readable title only where the corpus states one. Never invented."""
        audit = self._audit.get(record.get("source_id")) or {}
        lineage = audit.get("lineage") if isinstance(audit.get("lineage"), dict) else {}
        authors = lineage.get("authors")
        qa_bank = self.root / QA_DIR / f"{source_dir}-qa-bank.yaml"
        title = None
        if qa_bank.exists():
            items = (_load_yaml(qa_bank) or {}).get("qa_items") or []
            if items and isinstance(items[0], dict):
                title = items[0].get("source_title")
        if not title:
            hold_assessment = self.root / record["location"] / "audit-assessment-HOLD.yaml"
            if hold_assessment.exists():
                title = (_load_yaml(hold_assessment) or {}).get("title")
        if title and authors:
            return f"{title} ({', '.join(authors)})"
        if title:
            return title
        if authors:
            return f"{source_dir} ({', '.join(authors)})"
        return None

    # -- flatten ------------------------------------------------------------
    def _flatten(self):
        items = []
        for source_dir, record in sorted(self.sources.items()):
            status = record["source_status"]
            source_id = record.get("source_id")
            title = self._title(source_dir, record)
            group = self.lineage_group_of(source_id)
            artifacts = list(ARTIFACTS)
            if self.include_qa:
                artifacts.append("qa-bank.yaml")
            for artifact in artifacts:
                if artifact == "qa-bank.yaml":
                    path = self.root / QA_DIR / f"{source_dir}-qa-bank.yaml"
                else:
                    path = self.root / record["location"] / artifact
                if not path.exists():
                    continue
                data = _load_yaml(path)
                if not isinstance(data, dict):
                    continue
                for list_key, kind, id_field, builder in _ARTIFACT_ITEMS[artifact]:
                    for raw in data.get(list_key) or []:
                        if not isinstance(raw, dict):
                            continue
                        item_id = raw.get(id_field)
                        if not item_id:
                            continue
                        parts, payload = builder(raw)
                        index_text = " ".join(p for p in parts if p)
                        if not index_text.strip():
                            continue
                        items.append(CanonItem(
                            source_dir=source_dir, source_id=source_id,
                            source_title=title, source_status=status, kind=kind,
                            item_id=str(item_id), artifact=artifact,
                            lineage_group=group, index_text=index_text, payload=payload))
        return items

    # -- fingerprint --------------------------------------------------------
    def _fingerprint(self):
        """sha256 over the exact bytes retrieval can see, same algorithm as the index.

        For the production default this reproduces
        `fingerprints.accepted_canon.combined_digest` in CANON-CORPUS-INDEX.yaml, which is
        what makes "same corpus, same request, same config -> same bundle" checkable
        rather than asserted.
        """
        paths = []
        for source_dir, record in sorted(self.sources.items()):
            for artifact in ARTIFACTS:
                path = self.root / record["location"] / artifact
                if path.exists():
                    paths.append(f"{record['location']}/{artifact}")
            if self.include_qa:
                qa_bank = self.root / QA_DIR / f"{source_dir}-qa-bank.yaml"
                if qa_bank.exists():
                    paths.append(f"{QA_DIR}/{source_dir}-qa-bank.yaml")
        rows = []
        for rel in sorted(paths):
            digest = hashlib.sha256((self.root / rel).read_bytes()).hexdigest()
            rows.append(f"{rel}:{digest}\n")
        return {"algorithm": "sha256-of-sorted-path-and-content",
                "file_count": len(rows),
                "combined_digest": hashlib.sha256("".join(rows).encode()).hexdigest()}

    # -- reporting ----------------------------------------------------------
    def counts_by_kind(self):
        out = {}
        for item in self.items:
            out[item.kind] = out.get(item.kind, 0) + 1
        return out

    def summary(self):
        return {
            "surface": ("accepted_only" if self.production_default
                        else "accepted_plus_diagnostic"),
            "production_default": self.production_default,
            "diagnostic_reason": self.diagnostic_reason,
            "roots": {"accepted": "canon/knowledge/current"},
            "sources": len(self.sources),
            "items": len(self.items),
            "items_by_kind": self.counts_by_kind(),
            "lineage_groups": len({self.lineage_group_of(r.get("source_id"))
                                   for r in self.sources.values()}),
            "excluded_sources": self.excluded_sources,
            "corpus_fingerprint": self.fingerprint,
        }
