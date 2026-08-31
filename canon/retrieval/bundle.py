"""Assemble one compact Canon context bundle — the thing the reasoning model reads.

This is the part EVAL-037 got structurally wrong rather than merely inefficiently. Its
interface was search -> inspect ranked envelopes -> read the interesting ones in full. The
Sonnet CONTROLLED_CANON lane ran 53 searches across 18 trials and made exactly **one**
detailed read. The Gemma controlled lane issued good, targeted production-question
searches and then usually did not follow through to a read either. Two different models,
the same behaviour: the ranked search envelope was treated as the knowledge.

So the fix is not a better ranking behind the same protocol. It is to stop depending on a
second tool call the model does not reliably make. A bundle carries the useful content
directly — the claim, its mechanism, its scope, its caveats and its uncertainty — and
reports `delivered_complete` per item so a reader can see whether anything was held back.
`detail_ref` stays available for the exceptional case; it is not the design's load path.

What must survive into the bundle, per issue #82 and the Audit Gate's reasoning:

  source · object id and kind · accepted status · claim type · evidence characteristics ·
  both uncertainty fields · caveats WITH their origin · binding review status

The last two are where a bundle would most easily lie. A caveat marked `source_stated` is
the author limiting their own claim; one marked `extractor_observed` is this project
noticing a weakness. Collapsing them into "notes" turns a hedged claim into a rule. And an
operational binding with `status: proposed` has not been reviewed by anyone — 141 of the
152 accepted bindings are in that state, so every binding in a bundle says so.

Nothing here paraphrases. Every content value is a verbatim slice of a committed corpus
field; the only transformation is truncation, and truncation is always marked.
"""
import json

from .budgets import CHARS_PER_TOKEN_ESTIMATE, DEFAULT_BUDGETS
from .corpus import (KIND_BINDING, KIND_CONCEPT_SYSTEM, KIND_KNOWLEDGE,
                     KIND_ONTOLOGY_CONCEPT, KIND_ONTOLOGY_TERM, KIND_QA,
                     KIND_VISUAL_EVIDENCE)
from .plan import build_plan, request_vocabulary
from .rank import TypedIndex, select

BUNDLE_VERSION = "canon-context-bundle-v0.1"
CONTRACT = "canon/retrieval/RETRIEVAL-CONTRACT-v0.1.md"

TRUNCATION_MARK = " …[truncated — full text via detail_ref]"

# Long prose fields, per kind, in the order they are shortened when an item is over its
# character allowance. Epistemic fields are never in this list and are never trimmed.
_TRIMMABLE = {
    KIND_KNOWLEDGE: ("source_words", "claim", "mechanism_text", "interpretation_basis"),
    KIND_CONCEPT_SYSTEM: ("description", "whole_system_claim"),
    KIND_BINDING: ("rationale", "applicability_limits", "applicability_when"),
    KIND_ONTOLOGY_TERM: ("definition_in_origin_frame",),
    KIND_ONTOLOGY_CONCEPT: ("definition", "basis"),
    KIND_VISUAL_EVIDENCE: ("what_the_visual_supports", "visible_difference", "observation"),
    KIND_QA: ("answer", "question"),
}

MIN_PROSE_CHARS = 200

STATUS_LEGEND = {
    "ACCEPTED": ("The source passed the project's Audit Gate: its extraction was checked "
                 "against the exact bytes it was taken from. It does not mean the claim "
                 "was independently tested."),
    "claim_type.explicit_source_claim": "The source says this in words.",
    "claim_type.source_interpretation": ("This is our reading of the source, not its own "
                                         "words. `interpretation_basis` says what it was "
                                         "read from."),
    "caveat_origin.source_stated": "The author limited their own claim this way.",
    "caveat_origin.extractor_observed": ("This project noticed a weakness in the support; "
                                         "the author did not state it."),
    "binding_status.proposed": ("Nobody has reviewed this suggested use. It is a proposal "
                                "about how our system could apply the knowledge, not part "
                                "of the source's claim."),
    "evidence_basis.extractor_inference": ("The step from the source's claim to this "
                                           "suggested use is our leap, not the source's."),
}


def _clean(value):
    """Drop empty values so the bundle spends its characters on content."""
    if isinstance(value, dict):
        out = {k: _clean(v) for k, v in value.items()}
        return {k: v for k, v in out.items() if v not in (None, {}, [], "")}
    if isinstance(value, list):
        out = [_clean(v) for v in value]
        return [v for v in out if v not in (None, {}, [], "")]
    if isinstance(value, str):
        return value.strip()
    return value


def _content_for(item):
    """The verbatim, kind-appropriate content a reader actually needs."""
    p = item.payload
    if item.kind == KIND_KNOWLEDGE:
        return {
            "concept_label": p.get("concept_label"),
            "claim": p.get("claim"),
            "source_words": p.get("source_terms"),
            "mechanism_text": (p.get("mechanism") or {}).get("text"),
            "mechanism_stated_by_source": (p.get("mechanism") or {}).get("stated_by_source"),
            "scope_domain": (p.get("scope") or {}).get("domain_discussed_by_source"),
            "scope_conditions": (p.get("scope") or {}).get("conditions"),
            "source_stated_problems": p.get("source_stated_problems"),
            "source_stated_remedies": p.get("source_stated_remedies"),
            "interpretation_basis": p.get("interpretation_basis"),
        }
    if item.kind == KIND_CONCEPT_SYSTEM:
        claim = p.get("whole_system_claim") or {}
        return {
            "label": p.get("label"),
            "system_type": p.get("system_type"),
            "description": p.get("description"),
            "whole_system_claim": claim.get("text"),
            "member_count": len(p.get("members") or []),
            "member_refs": [m.get("sk_ref") for m in (p.get("members") or [])],
            "tradeoffs": [{"between": t.get("between"), "nature": t.get("nature"),
                           "origin": t.get("origin")}
                          for t in (p.get("tradeoffs") or []) if isinstance(t, dict)],
            "source_warns_against_isolated_use": p.get("source_warns_against_isolated_use"),
        }
    if item.kind == KIND_BINDING:
        applicability = p.get("applicability") or {}
        return {
            "what_it_binds_to": {"target_type": p.get("target_type"),
                                 "target_path": p.get("target_path"),
                                 "role": p.get("role")},
            "rationale": p.get("rationale"),
            "applicability_when": applicability.get("when"),
            "applicability_limits": applicability.get("limits"),
            "observation_unit": p.get("observation_unit"),
            "derived_from_source_knowledge": p.get("source_knowledge_refs"),
        }
    if item.kind == KIND_ONTOLOGY_TERM:
        return {"term": p.get("term"), "term_kind": p.get("kind"),
                "definition_in_origin_frame": p.get("definition_in_origin_frame"),
                "is_the_source_own_word": p.get("verbatim"),
                "arising_from": p.get("arising_from")}
    if item.kind == KIND_ONTOLOGY_CONCEPT:
        return {"label": p.get("label"), "concept_kind": p.get("kind"),
                "definition": p.get("definition"), "basis": p.get("basis"),
                "purpose": p.get("purpose"), "children_terms": p.get("children_terms")}
    if item.kind == KIND_VISUAL_EVIDENCE:
        return {"visual_kind": p.get("kind_of_visual"),
                "visible_difference": p.get("visible_difference"),
                "what_is_visible": p.get("what_is_visible"),
                "observation": p.get("observation"),
                "what_the_visual_supports": p.get("what_the_visual_supports"),
                "why_it_matters": p.get("why_it_matters"),
                "requires_prose": p.get("requires_prose")}
    if item.kind == KIND_QA:
        return {"question": p.get("question"), "answer": p.get("answer"),
                "grounded_in": p.get("grounded_in")}
    return dict(p)


def _epistemics_for(item):
    """Everything that stops a bounded claim being read as a universal rule."""
    p = item.payload
    out = {"source_status": item.source_status}
    if item.kind == KIND_KNOWLEDGE:
        evidence = p.get("evidence") or {}
        out.update({
            "claim_type": p.get("claim_type"),
            "label_origin": p.get("label_origin"),
            "evidence_characteristics": evidence.get("characteristics"),
            "source_uncertainty": evidence.get("source_uncertainty"),
            "extraction_uncertainty": evidence.get("extraction_uncertainty"),
            "caveats": [{"text": c.get("text"), "origin": c.get("origin")}
                        for c in (p.get("caveats") or []) if isinstance(c, dict)],
        })
    elif item.kind == KIND_CONCEPT_SYSTEM:
        evidence = p.get("evidence") or {}
        claim = p.get("whole_system_claim") or {}
        out.update({
            "system_type_origin": p.get("system_type_origin"),
            "whole_system_claim_origin": claim.get("origin"),
            "whole_system_claim_interpretation_basis": claim.get("interpretation_basis"),
            "evidence_characteristics": evidence.get("characteristics"),
            "source_uncertainty": evidence.get("source_uncertainty"),
            "extraction_uncertainty": evidence.get("extraction_uncertainty"),
            "system_level_uncertainty": evidence.get("system_level_uncertainty"),
        })
    elif item.kind == KIND_BINDING:
        out.update({
            "binding_status": p.get("status"),
            "binding_status_reason": p.get("status_reason"),
            "evidence_basis": p.get("evidence_basis"),
            "empirical_refs": p.get("empirical_refs"),
            "review_note": ("This is a proposed use of the knowledge by this project. It "
                            "is not part of the source's claim."),
        })
    elif item.kind == KIND_ONTOLOGY_TERM:
        out.update({"term_origin": p.get("origin"), "origin_ref": p.get("origin_ref"),
                    "verbatim": p.get("verbatim")})
    elif item.kind == KIND_ONTOLOGY_CONCEPT:
        out.update({
            "concept_origin": p.get("origin"), "created_by": p.get("created_by"),
            "asserts_equivalence": p.get("asserts_equivalence"),
            "asserts_agreement_between_sources": p.get("asserts_agreement_between_sources"),
            "concept_status": p.get("status"),
        })
    elif item.kind == KIND_VISUAL_EVIDENCE:
        out.update({
            "legibility_status": p.get("status"), "strength": p.get("strength"),
            "lost_in_plain_text": p.get("lost_in_plain_text"),
            "colour_dependent": p.get("colour_dependent"),
            "promoted_to_source_claim": p.get("promoted_to_source_claim"),
        })
    elif item.kind == KIND_QA:
        out.update({"not_benchmark_ground_truth": True,
                    "independent_corroboration": False,
                    "review_note": ("A Q&A item is an alternate grounded representation of "
                                    "the same source. It corroborates nothing on its own.")})
    return out


def _provenance_for(item):
    p = item.payload
    if item.kind in (KIND_KNOWLEDGE, KIND_CONCEPT_SYSTEM):
        prov = p.get("provenance") or {}
        return {"chapter": prov.get("chapter"), "section": prov.get("section"),
                "page_start": prov.get("page_start"), "page_end": prov.get("page_end"),
                "locator": prov.get("locator"), "source_support": prov.get("source_support")}
    if item.kind == KIND_ONTOLOGY_TERM:
        return dict(p.get("source_ref") or {})
    if item.kind == KIND_VISUAL_EVIDENCE:
        return {"chapter": p.get("chapter"), "pdf_page": p.get("pdf_page")}
    if item.kind == KIND_BINDING:
        return {"target_schema": p.get("target_schema"),
                "target_schema_version": p.get("target_schema_version")}
    return {}


def _sizeof(obj):
    """Characters the bundle actually costs when delivered as JSON."""
    return len(json.dumps(obj, ensure_ascii=False, sort_keys=True))


def _render_item(item, candidate, ordinal, lineage_note, question_id):
    rendered = {
        "n": ordinal,
        "answers_question": question_id,
        "kind": item.kind,
        "item_id": item.item_id,
        "source": _clean({
            "source_dir": item.source_dir,
            "source_id": item.source_id,
            "title": item.source_title,
            "source_status": item.source_status,
            "lineage_note": lineage_note,
        }),
        "content": _clean(_content_for(item)),
        "epistemics": _clean(_epistemics_for(item)),
        "provenance": _clean(_provenance_for(item)),
        "relevance": {"kind_rank": candidate["kind_rank"], "score": candidate["score"],
                      "allocation": candidate["allocation"],
                      "matched_query_terms": candidate["matched_query_terms"],
                      "basis": ("BM25 rank within this object kind. It measures fit to the "
                                "retrieval question, and says nothing about how good or "
                                "how well-evidenced the knowledge is.")},
        "delivered_complete": True,
        "detail_ref": item.detail_ref,
    }
    return rendered


def _fit_item(rendered, kind, max_chars):
    """Shorten an over-long item by trimming prose only, never epistemics.

    Returns (rendered, trimmed_fields) or (None, reason) when even the minimum will not
    fit. Failing loudly is deliberate: a silently mangled claim is worse than a missing one.
    """
    trimmed = []
    for field in _TRIMMABLE.get(kind, ()):
        if _sizeof(rendered) <= max_chars:
            break
        value = rendered["content"].get(field)
        if isinstance(value, list) and len(value) > 1:
            # A list of verbatim source quotations. Keep the first and say how many were
            # held back, rather than cutting a quotation off mid-sentence.
            rendered["content"][field] = [value[0], f"…[{len(value) - 1} more held back]"]
            rendered["delivered_complete"] = False
            trimmed.append(field)
            continue
        if not isinstance(value, str) or len(value) <= MIN_PROSE_CHARS:
            continue
        overshoot = _sizeof(rendered) - max_chars
        keep = max(MIN_PROSE_CHARS, len(value) - overshoot - len(TRUNCATION_MARK))
        rendered["content"][field] = value[:keep].rstrip() + TRUNCATION_MARK
        rendered["delivered_complete"] = False
        trimmed.append(field)
    if _sizeof(rendered) > max_chars:
        return None, "exceeds_max_chars_per_item_even_after_trimming"
    return rendered, trimmed



# A lineage note is only known once the whole selection exists, but its cost has to be
# reserved while items are still being admitted. This is the fixed reserve; the real note
# is shorter, so the budget is never exceeded by adding one.
LINEAGE_NOTE_RESERVE = 260


def model_payload(bundle):
    """The bundle as the reasoning model receives it: diagnostics stripped.

    `_diagnostics` records every rejection and why, which is essential for reviewing the
    retriever and useless to the model. It is excluded from the size accounting, so
    `size.total_chars` is what the model is actually charged.
    """
    return {k: v for k, v in bundle.items() if not k.startswith("_")}


# The bundle's non-item sections grow a little once coverage, spread and size are filled
# in. Reserved rather than guessed at the end, so an item is never admitted on the
# strength of budget the scaffold will later claim.
_SCAFFOLD_GROWTH_RESERVE = 900


def _header(corpus, budgets, plan):
    """Everything in the bundle that does not depend on which items were selected."""
    return {
        "bundle_version": BUNDLE_VERSION,
        "contract": CONTRACT,
        "how_to_use": (
            "This is the Canon knowledge selected for this request. It is durable creative "
            "and production knowledge — what makes work good and what commonly goes wrong. "
            "It says nothing about which image or video model to use, what a provider "
            "charges, or whether a model can execute something reliably. Read each item "
            "with its `epistemics`: a claim the source hedged is not a rule, a caveat "
            "marked extractor_observed is this project's doubt rather than the author's, "
            "and a binding marked proposed has not been reviewed by anyone. Items are "
            "delivered in full unless `delivered_complete` is false; `detail_ref` fetches "
            "the untruncated object in the rare case you need it."),
        "status_legend": STATUS_LEGEND,
        "corpus": {
            "surface": ("accepted_only" if corpus.production_default
                        else "accepted_plus_diagnostic"),
            "production_default": corpus.production_default,
            "diagnostic_reason": corpus.diagnostic_reason,
            "root": "canon/knowledge/current",
            "accepted_sources_available": len(corpus.sources),
            "items_available": len(corpus.items),
            "corpus_fingerprint": corpus.fingerprint,
        },
        "budgets": budgets.as_dict(),
        "plan": plan.as_dict(),
    }


def build_bundle(request_text, corpus, *, budgets=DEFAULT_BUDGETS, question_ids=None,
                 declared_needs=(), typed_index=None, extra_terms=None):
    """One bounded retrieval operation: plan, rank, spread, package.

    Returns a plain dict. Same corpus fingerprint + same request + same budgets ->
    byte-identical output, which `tests/test_canon_retrieval.py` asserts.
    """
    index = typed_index or TypedIndex(corpus)
    terms = (tuple(extra_terms) if extra_terms is not None
             else request_vocabulary(f"{request_text} {' '.join(declared_needs)}",
                                     index.discriminative_terms()))
    plan = build_plan(request_text, budgets=budgets, question_ids=question_ids,
                      extra_terms=terms, declared_needs=declared_needs)

    header = _header(corpus, budgets, plan)
    # Everything except the items: measured exactly rather than guessed, so the character
    # budget is enforced against the real delivered payload.
    scaffold = dict(header)
    scaffold.update({"items": [], "coverage": {}, "spread": {}, "size": {}})
    available = budgets.max_total_chars - _sizeof(scaffold) - _SCAFFOLD_GROWTH_RESERVE
    if available < 1:
        raise ValueError(
            f"max_total_chars={budgets.max_total_chars} cannot hold the bundle header "
            f"({_sizeof(scaffold)} chars). Raise the budget.")

    spent = {"chars": 0}

    def admit(item, candidate, question_id):
        """Render, fit and cost an item before it is allowed to consume any budget."""
        rendered = _render_item(item, candidate, 0, None, question_id)
        rendered, outcome = _fit_item(rendered, item.kind, budgets.max_chars_per_item)
        if rendered is None:
            return False, None, outcome
        cost = _sizeof(rendered) + LINEAGE_NOTE_RESERVE
        if spent["chars"] + cost > available:
            return False, None, "max_total_chars_reached"
        spent["chars"] += cost
        return True, {"rendered": rendered, "trimmed_fields": outcome, "cost": cost}, ""

    state = select(plan, index, budgets, admit=admit)

    # Two selected sources inside one independence group are one origin, and their
    # agreement is not corroboration. Say so on both, now that the selection is known.
    group_members = {}
    for entry in state.selected:
        item = entry["item"]
        group_members.setdefault(item.lineage_group, set()).add(item.source_dir)

    items = []
    for entry in state.selected:
        item = entry["item"]
        rendered = entry["payload_rendered"]["rendered"]
        rendered["n"] = len(items) + 1
        peers = sorted(group_members.get(item.lineage_group, set()) - {item.source_dir})
        if peers:
            rendered["source"]["lineage_note"] = (
                "Not an independent origin from " + ", ".join(peers) +
                " — the Audit Gate records these as one origin, so agreement between "
                "them is not corroboration.")
        if entry["payload_rendered"]["trimmed_fields"]:
            rendered["trimmed_fields"] = entry["payload_rendered"]["trimmed_fields"]
        items.append(rendered)

    answered = {i["answers_question"] for i in items}
    kinds, groups, per_source, domains = {}, {}, {}, {}
    for entry, rendered in zip(state.selected, items):
        item = entry["item"]
        kinds[rendered["kind"]] = kinds.get(rendered["kind"], 0) + 1
        groups[item.lineage_group] = groups.get(item.lineage_group, 0) + 1
        per_source[item.source_dir] = per_source.get(item.source_dir, 0) + 1
        # The source's OWN statement of what it is about. Reported, never used to filter:
        # deciding that "film_editing" knowledge cannot serve a still image would be this
        # project's judgement, not the source's, and the corpus records no such mapping.
        for domain in ((item.payload.get("scope") or {}).get("domain_discussed_by_source")
                       or []):
            domains[str(domain)] = domains.get(str(domain), 0) + 1

    bundle = dict(header)
    bundle["items"] = items
    bundle["coverage"] = {
        "questions_planned": [q.qid for q in plan.questions],
        "questions_with_at_least_one_item": sorted(answered),
        "questions_with_no_item": [q.qid for q in plan.questions if q.qid not in answered],
    }
    bundle["spread"] = {
        "items": len(items),
        "distinct_sources": len(per_source),
        "sources": sorted(per_source),
        "distinct_lineage_groups": len(groups),
        "max_items_from_one_source": max(per_source.values(), default=0),
        "max_items_from_one_lineage_group": max(groups.values(), default=0),
        "items_by_kind": kinds,
        "source_stated_domains": dict(sorted(domains.items(), key=lambda kv: (-kv[1], kv[0]))),
        "domains_note": ("What the selected sources say THEY are about. Retrieval is "
                         "lexical, so a source written about one medium can answer a "
                         "question about another. Check this against the job."),
    }
    bundle["size"] = {
        "total_chars": 0,
        "estimated_tokens": 0,
        "chars_per_token_estimate": CHARS_PER_TOKEN_ESTIMATE,
        "budget_chars": budgets.max_total_chars,
        "items_delivered_complete": sum(1 for i in items if i["delivered_complete"]),
        "items_delivered_complete_share": (
            round(sum(1 for i in items if i["delivered_complete"]) / len(items), 3)
            if items else 0.0),
    }
    # `size` is inside the thing it measures, so writing the number changes the number.
    # Iterate to a fixed point: the digits only ever grow, so this settles in two or three
    # passes and `size.total_chars` is then exactly the delivered length.
    bundle["size"]["within_budget"] = True
    for _ in range(6):
        total = _sizeof(model_payload(bundle))
        if total == bundle["size"]["total_chars"]:
            break
        bundle["size"]["total_chars"] = total
        bundle["size"]["estimated_tokens"] = total // CHARS_PER_TOKEN_ESTIMATE
        bundle["size"]["within_budget"] = total <= budgets.max_total_chars
    else:  # pragma: no cover - defensive; the loop above converges
        raise RuntimeError("bundle size measurement did not converge")

    bundle["_diagnostics"] = {
        "note": ("Retriever diagnostics. Not part of the model-facing payload and not "
                 "counted in size.total_chars; strip with bundle.model_payload()."),
        "plan": plan.as_diagnostic_dict(),
        "selection_rejections": state.rejections,
        "excluded_sources": corpus.excluded_sources,
        "chars_reserved_for_items": available,
        "chars_committed_by_items": spent["chars"],
    }
    return bundle
