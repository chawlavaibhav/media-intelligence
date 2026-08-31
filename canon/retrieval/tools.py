"""The tool surface a reasoning model sees: one bounded operation, plus a rare escape hatch.

EVAL-037 exposed three tools — `canon_catalog`, `canon_search`, `canon_read` — and left the
model to compose them. Recomputed from the committed transcripts, the Sonnet
CONTROLLED_CANON lane spent 53 searches and 424 results (1,205,392 bytes, a mean of 66,966
per trial) doing that composition, and 53.5% of what came back was HOLD material the model
then had to discount for itself.

`canon_context` replaces the composition step. One call takes the customer's request and
returns the bounded, accepted-only, evidence-preserving bundle. `canon_detail` remains for
the exceptional case where a trimmed item needs its full text, and the bundle says per item
whether that is even necessary (`delivered_complete`).

There is no `canon_search` here. Reintroducing free-text search over the whole corpus would
reintroduce the failure this package exists to fix.
"""
from .budgets import Budgets, PRESETS
from .bundle import build_bundle, model_payload
from .corpus import ARTIFACTS, AcceptedCanon
from .questions import CATALOGUE, QUESTION_IDS
from .rank import TypedIndex

TOOL_SCHEMAS = [
    {
        "name": "canon_context",
        "description": (
            "Get the media-production knowledge relevant to a customer request, as one "
            "compact bundle. Covers composition, lighting and material, product "
            "legibility, advertising message structure, shot and edit grammar, "
            "persuasion, brand handling, culturally specific communication and common "
            "failures. Only accepted knowledge is returned — material still under review "
            "is never included. Each item arrives with its claim, the source's own scope "
            "and caveats, and how well the source supports it, so you can tell a hedged "
            "observation from a rule. It tells you nothing about which image or video "
            "model to use, what a provider costs, or what a model can reliably execute."),
        "input_schema": {
            "type": "object",
            "properties": {
                "request": {
                    "type": "string",
                    "description": "The customer's request or brief, in their own words."},
                "knowledge_needs": {
                    "type": "array", "items": {"type": "string"},
                    "description": ("Optional. Your own statements of what you need to "
                                    "know for this job, one per entry. They sharpen the "
                                    "selection; they do not enlarge it.")},
                "questions": {
                    "type": "array", "items": {"type": "string", "enum": list(QUESTION_IDS)},
                    "description": ("Optional. Ask for specific production questions "
                                    "instead of letting the request select them.")},
                "size": {
                    "type": "string", "enum": sorted(PRESETS),
                    "description": ("Optional. 'default' returns up to 12 items in about "
                                    "30,000 characters; 'compact' up to 8 in about 15,000. "
                                    "Both are hard limits.")},
            },
            "required": ["request"],
        },
    },
    {
        "name": "canon_detail",
        "description": (
            "Read one Canon object in full. Only needed when a bundle item reports "
            "delivered_complete: false. Pass the item's detail_ref."),
        "input_schema": {
            "type": "object",
            "properties": {
                "source_dir": {"type": "string"},
                "artifact": {"type": "string", "enum": list(ARTIFACTS)},
                "item_id": {"type": "string"},
            },
            "required": ["item_id"],
        },
    },
]

TOOL_NAMES = [schema["name"] for schema in TOOL_SCHEMAS]


class CanonContextTools:
    """Bind the tools to one loaded corpus. Build once; reuse across requests."""

    def __init__(self, repo_root=".", corpus=None, budgets=None):
        self.corpus = corpus or AcceptedCanon(repo_root)
        self.index = TypedIndex(self.corpus)
        self.default_budgets = budgets or PRESETS["default"]

    def canon_context(self, request, knowledge_needs=None, questions=None, size=None):
        budgets = self.default_budgets
        if size is not None:
            if size not in PRESETS:
                raise ValueError(f"size must be one of {sorted(PRESETS)}; got {size!r}")
            budgets = PRESETS[size]
        bundle = build_bundle(request, self.corpus, budgets=budgets,
                              question_ids=questions,
                              declared_needs=tuple(knowledge_needs or ()),
                              typed_index=self.index)
        return model_payload(bundle)

    def canon_detail(self, item_id, source_dir=None, artifact=None):
        """The full stored object, with its status and epistemics, or a not-found note."""
        from .bundle import _clean, _content_for, _epistemics_for, _provenance_for
        for item in self.corpus.items:
            if item.item_id != str(item_id):
                continue
            if source_dir and item.source_dir != source_dir:
                continue
            if artifact and item.artifact != artifact:
                continue
            return {
                "kind": item.kind, "item_id": item.item_id,
                "source": {"source_dir": item.source_dir, "source_id": item.source_id,
                           "title": item.source_title,
                           "source_status": item.source_status},
                "content": _clean(_content_for(item)),
                "epistemics": _clean(_epistemics_for(item)),
                "provenance": _clean(_provenance_for(item)),
                "delivered_complete": True,
            }
        return {"item_id": item_id, "found": False,
                "note": ("No accepted Canon object with that id. Held material is not "
                         "reachable through this tool.")}

    def dispatch(self, name, arguments):
        if name not in TOOL_NAMES:
            raise ValueError(f"tool {name!r} is not part of the Canon retrieval surface")
        return getattr(self, name)(**(arguments or {}))


def budgets_from_dict(values):
    """Build a Budgets from a plain mapping, rejecting anything unbounded."""
    return Budgets(**values)


QUESTION_CATALOGUE = [q.as_dict() for q in CATALOGUE]
