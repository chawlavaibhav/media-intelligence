"""Turn a customer request into a small, bounded, inspectable retrieval plan.

The plan is the stage EVAL-037 did not have. There, the model paraphrased the brief into
two or three free-text searches, differently on every repetition of the same brief. Here
the request selects production questions from a fixed catalogue by deterministic keyword
cue, so the same request always yields the same plan, and the plan is a readable object a
human can disagree with.

A caller who has better information may supply questions directly — `question_ids=` picks
catalogue entries, and `extra_terms=` adds request-specific vocabulary such as a product
material or a market. A model-formed plan is therefore allowed by the contract; what is
not allowed is an unbounded one. `Budgets.max_questions` caps the plan in every path.
"""
from .budgets import DEFAULT_BUDGETS
from .questions import (BY_ID, CATALOGUE, MEDIA_UNSPECIFIED, QUESTION_IDS, contains_cue,
                        detect_media, normalise)
from .corpus import tokenize


class PlanError(ValueError):
    """Raised when a caller asks for a question that does not exist."""


class PlannedQuestion:
    __slots__ = ("question", "score", "matched_cues", "selected_by", "request_terms")

    def __init__(self, question, score, matched_cues, selected_by, request_terms):
        self.question = question
        self.score = score
        self.matched_cues = matched_cues
        self.selected_by = selected_by
        self.request_terms = request_terms

    @property
    def qid(self):
        return self.question.qid

    def query_text(self):
        return self.question.query_text(self.request_terms)

    def as_dict(self):
        """What the reasoning model sees: the need, in plain English, and why it is here.

        The search vocabulary is deliberately NOT here. It is several hundred characters
        per question of retrieval machinery the model cannot act on, and the character
        budget is better spent on knowledge. It stays available for review in
        `as_diagnostic_dict`.
        """
        return {
            "question_id": self.qid,
            "plain_english": self.question.plain_english,
            "selected_by": self.selected_by,
            "matched_request_cues": list(self.matched_cues),
        }

    def as_diagnostic_dict(self):
        out = self.as_dict()
        out["cue_match_count"] = self.score
        out["search_vocabulary"] = (list(self.question.expansion_terms)
                                    + list(self.request_terms))
        return out


class RetrievalPlan:
    __slots__ = ("request_text", "media", "questions", "budgets", "extra_terms",
                 "declared_needs")

    def __init__(self, request_text, media, questions, budgets, extra_terms,
                 declared_needs):
        self.request_text = request_text
        self.media = media
        self.questions = questions
        self.budgets = budgets
        self.extra_terms = extra_terms
        self.declared_needs = declared_needs

    def as_dict(self):
        return {
            "detected_media": self.media,
            "question_count": len(self.questions),
            "max_questions": self.budgets.max_questions,
            "request_terms_used": list(self.extra_terms),
            "declared_needs_supplied": len(self.declared_needs),
            "questions": [q.as_dict() for q in self.questions],
            "boundary_note": ("Production questions ask what must be understood to specify "
                              "the work. They never ask which model or provider should make "
                              "it; that is capability routing and is out of Canon's scope."),
        }

    def as_diagnostic_dict(self):
        out = self.as_dict()
        out["questions"] = [q.as_diagnostic_dict() for q in self.questions]
        out["declared_needs"] = list(self.declared_needs)
        return out


def _cue_hits(question, normalised_text):
    return tuple(sorted({cue for cue in question.cue_terms
                         if contains_cue(normalised_text, cue)}))


def build_plan(request_text, *, budgets=DEFAULT_BUDGETS, question_ids=None,
               extra_terms=(), declared_needs=()):
    """Select at most `budgets.max_questions` production questions for this request.

    `declared_needs` are a caller's own statements of what it needs to know — the same
    thing the CONTROLLED_CANON lane wrote under its RESEARCH_NEEDS marker. They widen cue
    matching and are recorded in the plan, but they never bypass the question cap.
    """
    request_text = request_text or ""
    if not request_text.strip() and not question_ids:
        raise PlanError("build_plan needs a request text or explicit question_ids")

    declared_needs = tuple(str(n) for n in declared_needs if str(n).strip())
    cue_text = normalise(" ".join([request_text, *declared_needs]))
    media = detect_media(" ".join([request_text, *declared_needs]))
    request_terms = tuple(extra_terms)

    if question_ids is not None:
        unknown = [q for q in question_ids if q not in BY_ID]
        if unknown:
            raise PlanError(f"unknown question_ids {unknown}; valid ids are {list(QUESTION_IDS)}")
        chosen = [PlannedQuestion(BY_ID[qid], len(_cue_hits(BY_ID[qid], cue_text)),
                                  _cue_hits(BY_ID[qid], cue_text), "caller_specified",
                                  request_terms)
                  for qid in question_ids][:budgets.max_questions]
        return RetrievalPlan(request_text, media, chosen, budgets, request_terms,
                             declared_needs)

    eligible = [q for q in CATALOGUE if media in q.media or media == MEDIA_UNSPECIFIED]
    scored = []
    for question in eligible:
        cues = _cue_hits(question, cue_text)
        is_base = media in question.base_for
        scored.append(PlannedQuestion(
            question, len(cues), cues,
            "base_for_media" if is_base else "request_cue_match", request_terms))

    # Base questions for the detected media are always kept: a brief that never says the
    # word "composition" still needs composition knowledge. Everything else competes on
    # cue matches, with catalogue order as the deterministic tie-break.
    order = {qid: i for i, qid in enumerate(QUESTION_IDS)}
    base = [p for p in scored if p.selected_by == "base_for_media"]
    rest = [p for p in scored if p.selected_by != "base_for_media" and p.score > 0]
    base.sort(key=lambda p: order[p.qid])
    rest.sort(key=lambda p: (-p.score, order[p.qid]))

    chosen, seen = [], set()
    for planned in base + rest:
        if planned.qid in seen:
            continue
        seen.add(planned.qid)
        chosen.append(planned)
        if len(chosen) >= budgets.max_questions:
            break
    return RetrievalPlan(request_text, media, chosen, budgets, request_terms, declared_needs)


def request_vocabulary(request_text, discriminative_terms, limit=12):
    """The request's own discriminative words — the part worth adding to a search.

    Two kinds of word are dropped. A brief's proper nouns ("RentOK", "Aster Meridian")
    are absent from Canon and match nothing. Ordinary English ("the", "for", "with") is
    present in Canon everywhere and narrows nothing; it survived an earlier version of
    this function that only intersected with the corpus vocabulary, which is why the
    caller now passes `TypedIndex.discriminative_terms()` instead. Returned in
    first-appearance order, so the result is stable for a given request.
    """
    seen, out = set(), []
    for token in tokenize(request_text):
        if token in discriminative_terms and token not in seen:
            seen.add(token)
            out.append(token)
            if len(out) >= limit:
                break
    return tuple(out)
