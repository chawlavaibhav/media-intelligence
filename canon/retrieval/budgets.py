"""Hard budgets for a Canon context bundle. There is deliberately no unbounded mode.

EVAL-037 left retrieval open on purpose: no aggregate top-K, no token budget, no
retrieval-count budget. That produced the two failures the Controller recorded — a
repaired Sonnet lane that context-overflowed on 16 of 18 trials, and a Gemma lane that
exposed roughly 1.13M tokens from one search path and failed 18/18. So every field here
is required and every field is checked at construction. A `None` is a rejected value,
not "no limit".

The defaults are set against measured EVAL-037 behaviour rather than taste. Recomputed
from the committed transcripts of the Sonnet CONTROLLED_CANON lane
(`work/eval-037-sonnet-controlled-canon`), that lane exposed 53 searches and 424 results
across 18 trials, totalling 1,205,392 bytes — a mean of **66,966 bytes per trial**. The
default `max_total_chars` of 30,000 is under half of that, delivered in one operation
instead of three. `COMPACT` halves it again for callers with a tighter context.

The point is to leave headroom, not to find the largest survivable bundle. Both presets
are bounded; there is no third, unbounded one.

Characters, not tokens, are the enforced unit. A character count is exact and needs no
tokenizer; `estimated_tokens` divides by `CHARS_PER_TOKEN_ESTIMATE` and is reported as an
estimate everywhere it appears. It is never the thing being enforced.
"""
from dataclasses import dataclass, asdict

# A rough English-prose ratio, used only to translate a character budget into a number a
# reader can compare against a context window. Not a tokenizer and not a guarantee.
CHARS_PER_TOKEN_ESTIMATE = 4


class BudgetError(ValueError):
    """Raised when a budget is missing, unbounded, or not a positive integer."""


@dataclass(frozen=True)
class Budgets:
    """Every bound the retriever enforces. All are required and all are finite."""

    # -- size of the delivered bundle --------------------------------------
    max_items: int = 12
    max_total_chars: int = 30_000
    # A rendered SourceKnowledge object costs a median of about 2,050 characters and a
    # 90th percentile of about 2,940 (measured over all 677 accepted objects); a concept
    # system runs larger. 4,200 admits almost everything whole. Anything larger is trimmed
    # in its prose only — never in its caveats or uncertainty — and says which fields.
    max_chars_per_item: int = 4_200

    # -- spread of the delivered bundle ------------------------------------
    max_sources: int = 8
    max_items_per_source: int = 3
    # A lineage group is a set of sources the Audit Gate says are NOT independent of
    # each other (companion volumes, the same practitioner speaking in two books). Two
    # such sources agreeing is one origin agreeing with itself, so they share one cap.
    max_items_per_lineage_group: int = 4

    # -- shape of the retrieval plan ---------------------------------------
    max_questions: int = 4
    max_items_per_question: int = 5
    # Candidates each question's ranker may consider before diversity trimming. Bounds
    # work, not output; it never widens what the model sees.
    max_candidates_per_question: int = 60

    def __post_init__(self):
        for field_name, value in asdict(self).items():
            if not isinstance(value, int) or isinstance(value, bool):
                raise BudgetError(
                    f"{field_name} must be a positive integer; got {value!r}. "
                    "There is no unbounded setting."
                )
            if value < 1:
                raise BudgetError(f"{field_name} must be >= 1; got {value}")
        if self.max_items_per_question > self.max_items:
            raise BudgetError(
                f"max_items_per_question ({self.max_items_per_question}) exceeds "
                f"max_items ({self.max_items})")
        if self.max_chars_per_item > self.max_total_chars:
            raise BudgetError(
                f"max_chars_per_item ({self.max_chars_per_item}) exceeds "
                f"max_total_chars ({self.max_total_chars})")

    @property
    def estimated_max_tokens(self) -> int:
        """Character budget expressed as an approximate token count. An estimate."""
        return self.max_total_chars // CHARS_PER_TOKEN_ESTIMATE

    def as_dict(self) -> dict:
        return asdict(self)


DEFAULT_BUDGETS = Budgets()

# For callers with a tighter context window. Still bounded on every axis.
COMPACT_BUDGETS = Budgets(
    max_items=8, max_total_chars=15_000, max_chars_per_item=2_600,
    max_sources=6, max_items_per_source=2, max_items_per_lineage_group=3,
    max_questions=3, max_items_per_question=3, max_candidates_per_question=60)

PRESETS = {"default": DEFAULT_BUDGETS, "compact": COMPACT_BUDGETS}
