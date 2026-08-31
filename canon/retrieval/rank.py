"""Typed ranking: score inside a kind, allocate across kinds, then enforce spread.

EVAL-037 treated every Canon object as one interchangeable text blob and ranked them all
against each other with a single BM25 index. That is wrong in a way that is easy to miss.
An ontology term is a one-line definition of about 20 tokens; a SourceKnowledge object is a
claim with mechanism, scope and caveats running to 250 or more. BM25's length
normalisation shortens the gap but does not make the two scores mean the same thing, so a
mixed ranking quietly over-selects the shortest objects — the definitions — over the
claims that actually carry the knowledge.

Two changes follow.

**Score within a kind.** Each kind gets its own BM25 index, with its own document
frequencies and its own average length. A score is then only ever compared against other
scores of the same kind, which is the only comparison BM25 supports honestly.

**Allocate across kinds.** Because cross-kind scores are not comparable, the mix is decided
by an explicit, visible allocation rather than by a hidden weight:

  knowledge        the claim itself, with its mechanism, scope and caveats — the substance
  concept_system   the relations BETWEEN claims, which SPEC-03 says are destroyed if the
                   members are retrieved alone (centre-as-attractor and centre-avoidance
                   are a trade-off pair that is incoherent one at a time)
  binding          how this project could use the knowledge — but 141 of the 152 accepted
                   bindings still carry `status: proposed`, meaning nobody has reviewed
                   them, so one slot and always labelled
  visual_evidence  what the figure shows and the prose does not; raised for lighting and
                   material questions, where it is often the whole argument
  ontology_concept a navigational grouping that explicitly asserts no equivalence
  ontology_term    a definition, and usually a definition OF an already-selected claim —
                   `arising_from` says which, and a term whose parent claim is already in
                   the bundle is dropped as redundant

The allocation is a retrieval-role decision, not a quality judgement. Nothing here ranks
sources, and nothing uses binding count as a proxy for anything: `canon/HANDOFF.md` records
that the corpus's best-binding source has its weakest evidence.
"""
import math

from .corpus import (KIND_BINDING, KIND_CONCEPT_SYSTEM, KIND_KNOWLEDGE,
                     KIND_ONTOLOGY_CONCEPT, KIND_ONTOLOGY_TERM, KIND_VISUAL_EVIDENCE,
                     tokenize)

# Which operational bindings belong in a bundle whose job is to help specify a customer's
# media job. SPEC-04 defines five target types, and two of them are about this project's
# own machinery rather than about making the work:
#
#   governance  how the ontology admits, splits or refuses terms; how contradictions are
#               settled; how evidence characteristics are weighted   (50 of 152 accepted)
#   benchmark   how to generate a test case or a minimal pair for our own measurement
#                                                                     (13 of 152 accepted)
#
# Together that is 63 of the 152 accepted bindings — 41% of the binding surface — none of
# which tells a reasoning model anything about the customer's outcome. A flat search
# returns them anyway: EVAL-037 surfaced a Catmull binding about how to score an
# evaluator's feedback as an answer to "what goes wrong in a premium watch photograph".
# Excluding them is a scope filter, not a quality judgement, and it is configurable.
PRODUCTION_BINDING_TARGETS = frozenset({"creative_ir", "production", "evaluation"})

# Fixed at EVAL-037's values so a before/after comparison isolates the design change
# rather than a tuning change.
BM25_K1 = 1.2
BM25_B = 0.75

# The allocation, written as the order in which a question wants its slots filled. It is
# INTERLEAVED rather than grouped, and that is the whole point: the second-best claim from
# a source is worth less than the concept system that says how that source's claims relate
# to each other, so the mix survives a tight character budget instead of being crowded out
# by whichever kind happens to be listed first. Once the sequence is exhausted, remaining
# slots are backfilled by cycling the same kinds in first-appearance order.
DEFAULT_KIND_SEQUENCE = (KIND_KNOWLEDGE, KIND_CONCEPT_SYSTEM, KIND_KNOWLEDGE, KIND_BINDING,
                         KIND_KNOWLEDGE, KIND_VISUAL_EVIDENCE, KIND_ONTOLOGY_CONCEPT,
                         KIND_ONTOLOGY_TERM)

# Two items whose indexed text shares this proportion of its combined vocabulary are
# treated as saying the same thing, and the lower-ranked one is dropped. Jaccard over the
# token SET, so length differences do not by themselves create or hide a duplicate.
NEAR_DUPLICATE_JACCARD = 0.6


def is_production_relevant(item, binding_targets=PRODUCTION_BINDING_TARGETS):
    """False for bindings that address this project's own machinery rather than the work."""
    if item.kind != KIND_BINDING:
        return True
    return item.payload.get("target_type") in binding_targets


class KindIndex:
    """A BM25 index over one kind. Pure function of the corpus bytes; nothing stochastic."""

    __slots__ = ("kind", "docs", "idf", "avgdl", "n", "vocabulary")

    def __init__(self, kind, items):
        self.kind = kind
        docs, df = [], {}
        for item in items:
            tf = {}
            for token in item.tokens:
                tf[token] = tf.get(token, 0) + 1
            for token in tf:
                df[token] = df.get(token, 0) + 1
            docs.append((item, tf, len(item.tokens)))
        self.docs = docs
        self.n = len(docs)
        self.avgdl = (sum(d[2] for d in docs) / self.n) if self.n else 0.0
        self.idf = {t: math.log(1.0 + (self.n - c + 0.5) / (c + 0.5)) for t, c in df.items()}
        self.vocabulary = frozenset(df)

    def score(self, query_tokens, min_score=0.0):
        """Ranked (score, matched_terms, item) for this kind. Deterministic ordering."""
        out = []
        for item, tf, dl in self.docs:
            score, matched = 0.0, set()
            for token in query_tokens:
                freq = tf.get(token)
                if not freq:
                    continue
                matched.add(token)
                denom = freq + BM25_K1 * (
                    1 - BM25_B + BM25_B * (dl / self.avgdl if self.avgdl else 1))
                score += self.idf.get(token, 0.0) * (freq * (BM25_K1 + 1)) / denom
            if score > min_score:
                out.append((round(score, 6), tuple(sorted(matched)), item))
        out.sort(key=lambda row: (-row[0], row[2].source_dir, row[2].item_id))
        return out


class TypedIndex:
    """One BM25 index per kind, built once per corpus."""

    def __init__(self, corpus, binding_targets=PRODUCTION_BINDING_TARGETS):
        self.corpus = corpus
        self.binding_targets = frozenset(binding_targets)
        by_kind = {}
        self.out_of_scope_bindings = 0
        for item in corpus.items:
            if not is_production_relevant(item, self.binding_targets):
                self.out_of_scope_bindings += 1
                continue
            by_kind.setdefault(item.kind, []).append(item)
        self.indexes = {kind: KindIndex(kind, items) for kind, items in sorted(by_kind.items())}
        self.vocabulary = frozenset().union(
            *[ix.vocabulary for ix in self.indexes.values()]) if self.indexes else frozenset()
        # Corpus-wide document frequency, used to keep only the DISCRIMINATIVE words of a
        # customer request. Intersecting the request with the corpus vocabulary is not
        # enough: "the", "for" and "with" are all in the corpus vocabulary and carry no
        # signal, while "sapphire" and "condensation" do.
        df = {}
        for item in corpus.items:
            for token in set(item.tokens):
                df[token] = df.get(token, 0) + 1
        self.document_frequency = df
        self.document_count = len(corpus.items)

    def discriminative_terms(self, max_df_ratio=0.10):
        """Tokens rare enough to narrow a search rather than widen it.

        A token in more than `max_df_ratio` of accepted objects is treated as corpus
        background, not as a request signal. At 10% over 1,623 accepted objects the cut is
        162 documents, which removes ordinary English and keeps domain and product words.
        """
        ceiling = self.document_count * max_df_ratio
        return frozenset(t for t, c in self.document_frequency.items() if c <= ceiling)

    def slate(self, query_text, *, kind_sequence=None, max_candidates=60):
        """The ordered candidate list one question would like, best first.

        Ordering IS the allocation. Global spread limits are not applied here — a slate is
        a preference, and `select` decides what survives.
        """
        sequence = tuple(kind_sequence or DEFAULT_KIND_SEQUENCE)
        backfill_order, seen = [], set()
        for kind in sequence:
            if kind not in seen:
                seen.add(kind)
                backfill_order.append(kind)

        query_tokens = tokenize(query_text)
        ranked = {kind: (self.indexes[kind].score(query_tokens) if kind in self.indexes
                         else []) for kind in backfill_order}
        cursor = {kind: 0 for kind in backfill_order}
        slate = []

        def take(kind, allocation):
            i = cursor[kind]
            if i >= len(ranked[kind]):
                return False
            cursor[kind] = i + 1
            score, matched, item = ranked[kind][i]
            slate.append({"item": item, "score": score, "matched_query_terms": list(matched),
                          "kind_rank": i + 1, "allocation": allocation})
            return True

        for kind in sequence:
            if len(slate) >= max_candidates:
                break
            take(kind, "allocated")
        while len(slate) < max_candidates:
            progressed = False
            for kind in backfill_order:
                if len(slate) >= max_candidates:
                    break
                if take(kind, "backfill"):
                    progressed = True
            if not progressed:
                break
        return slate


def _jaccard(a, b):
    if not a or not b:
        return 0.0
    union = len(a | b)
    return (len(a & b) / union) if union else 0.0


class SelectionState:
    """Tracks every spread limit while candidates are accepted or rejected."""

    def __init__(self, budgets):
        self.budgets = budgets
        self.selected = []
        self.per_source = {}
        self.per_group = {}
        self.per_question = {}
        self.sources = []
        self.selected_ids = set()
        self.selected_sk_ids = set()
        self.token_sets = []
        self.rejections = []

    def _reject(self, candidate, question_id, reason, detail=None):
        self.rejections.append({
            "question_id": question_id, "item_id": candidate["item"].item_id,
            "kind": candidate["item"].kind, "source_dir": candidate["item"].source_dir,
            "reason": reason, "detail": detail})

    def offer(self, candidate, question_id, admit=None):
        """Try to accept one candidate. Returns True when it joins the selection.

        `admit(item, candidate, question_id)` is the caller's last veto, run only after every cheap
        constraint has passed. It returns (ok, payload, reason). A candidate vetoed here
        consumes NO budget — that ordering matters: an item rejected for size after it had
        already spent its source's allowance would silently starve the rest of the bundle.
        """
        item = candidate["item"]
        budgets = self.budgets
        if item.item_id in self.selected_ids:
            self._reject(candidate, question_id, "already_selected")
            return False
        if len(self.selected) >= budgets.max_items:
            self._reject(candidate, question_id, "max_items_reached")
            return False
        if self.per_question.get(question_id, 0) >= budgets.max_items_per_question:
            self._reject(candidate, question_id, "max_items_per_question_reached")
            return False
        if self.per_source.get(item.source_dir, 0) >= budgets.max_items_per_source:
            self._reject(candidate, question_id, "max_items_per_source_reached")
            return False
        if self.per_group.get(item.lineage_group, 0) >= budgets.max_items_per_lineage_group:
            self._reject(candidate, question_id, "max_items_per_lineage_group_reached",
                         item.lineage_group)
            return False
        if (item.source_dir not in self.per_source
                and len(self.sources) >= budgets.max_sources):
            self._reject(candidate, question_id, "max_sources_reached")
            return False

        # An ontology term is a definition of a claim. If the claim it arises from is
        # already in the bundle, the definition spends budget on something the reader
        # already has.
        if item.kind == KIND_ONTOLOGY_TERM:
            arising = {str(r) for r in (item.payload.get("arising_from") or [])}
            overlap = arising & self.selected_sk_ids
            if overlap:
                self._reject(candidate, question_id, "definition_of_already_selected_claim",
                             sorted(overlap))
                return False

        tokens = frozenset(item.tokens)
        for other_tokens, other in self.token_sets:
            similarity = _jaccard(tokens, other_tokens)
            if similarity >= NEAR_DUPLICATE_JACCARD:
                self._reject(candidate, question_id, "near_duplicate_of_selected",
                             {"item_id": other.item_id, "jaccard": round(similarity, 3)})
                return False

        payload = None
        if admit is not None:
            ok, payload, reason = admit(item, candidate, question_id)
            if not ok:
                self._reject(candidate, question_id, reason)
                return False

        entry = dict(candidate)
        entry["payload_rendered"] = payload
        entry["question_id"] = question_id
        entry["selection_rank"] = len(self.selected) + 1
        self.selected.append(entry)
        self.selected_ids.add(item.item_id)
        if item.kind == KIND_KNOWLEDGE:
            self.selected_sk_ids.add(item.item_id)
        if item.source_dir not in self.per_source:
            self.sources.append(item.source_dir)
        self.per_source[item.source_dir] = self.per_source.get(item.source_dir, 0) + 1
        self.per_group[item.lineage_group] = self.per_group.get(item.lineage_group, 0) + 1
        self.per_question[question_id] = self.per_question.get(question_id, 0) + 1
        self.token_sets.append((tokens, item))
        return True


def select(plan, typed_index, budgets, admit=None):
    """Fill the bundle by round-robin across questions, best-first inside each question.

    Round-robin matters: taking each question's first choice before any question's second
    means one question cannot spend the source or item budget the others need. It also
    makes truncation fair — if the character budget runs out, every question has already
    contributed its strongest item.
    """
    slates = []
    for planned in plan.questions:
        slate = typed_index.slate(
            planned.query_text(),
            kind_sequence=planned.question.kind_sequence,
            max_candidates=budgets.max_candidates_per_question)
        slates.append((planned.qid, slate, [0]))

    state = SelectionState(budgets)
    for _round in range(budgets.max_items_per_question):
        progressed = False
        for question_id, slate, cursor in slates:
            if len(state.selected) >= budgets.max_items:
                break
            if state.per_question.get(question_id, 0) >= budgets.max_items_per_question:
                continue
            while cursor[0] < len(slate):
                candidate = slate[cursor[0]]
                cursor[0] += 1
                if state.offer(candidate, question_id, admit=admit):
                    progressed = True
                    break
        if len(state.selected) >= budgets.max_items or not progressed:
            break
    return state
