#!/usr/bin/env python3
"""EVAL-037 — the CONTROLLED_CANON retrieval treatment: measurement, not enforcement.

This module OBSERVES what the tested model actually retrieved and states whether that
stayed inside the treatment's allowance. It does not cap, truncate, block or repair
anything.

That distinction is the whole point of the supplemental run. The allowance below is an
EXPERIMENTAL TREATMENT — a behaviour asked of the model in the prompt — not a technical
context-window guard. If the model exceeds it, the honest result is a trial marked
`failed_controlled_retrieval`, not a quietly clamped tool call that would make the
treatment look obeyed when it was not.

  <= 3  canon_search calls per trial
  <= 8  results returned per canon_search   (the model must pass `limit`; the tool's
        default is unbounded and returns every scoring item)
  <= 24 search results exposed in total
  <= 6  canon_read objects per trial

`canon_catalog` is discouraged in the prompt but carries no numeric allowance, so it is
counted and reported, never scored.
"""

TREATMENT_ID = "CONTROLLED_CANON"

LIMITS = {
    "max_canon_search_calls": 3,
    "max_results_per_search": 8,
    "max_search_results_total": 24,
    "max_canon_read_objects": 6,
}

VIOLATION_STATUS = "failed_controlled_retrieval"

# The model is asked to declare its knowledge needs under this marker before its first
# retrieval call. Absence is recorded as an observation; it is not itself a violation,
# because the allowance the treatment defines is numeric.
NEEDS_MARKER = "RESEARCH_NEEDS"


def declared_needs(intermediate_text):
    """Pull the model's own stated knowledge needs out of its pre-tool assistant text.

    Returns (needs, raw_block). `needs` is the list of lines the model wrote under the
    marker. Nothing is inferred: if the model never wrote the block, this returns
    ([], None) and the evidence says so.
    """
    blocks = [n.get("text", "") for n in (intermediate_text or [])
              if NEEDS_MARKER in (n.get("text") or "")]
    if not blocks:
        return [], None
    raw = blocks[0]
    tail = raw.split(NEEDS_MARKER, 1)[1].lstrip(":").strip()
    needs, seen_any = [], False
    for line in tail.splitlines():
        t = line.strip()
        if not t:
            if seen_any:
                break          # the list ends at the first blank line after it starts
            continue
        if t.startswith(("#", "```")):
            continue
        seen_any = True
        needs.append(t.lstrip("-*• ").strip())
    return needs, raw


def assess(tool_calls, intermediate_text=None):
    """Measure one trial's Canon retrieval against the treatment allowance.

    `tool_calls` are the runner's tool-call records for the whole trial, every attempt
    included — a format repair is part of the same trial and its retrieval counts too.
    """
    canon = [tc for tc in (tool_calls or []) if tc.get("tool_family") == "canon"]
    searches = [tc for tc in canon if tc.get("name") == "canon_search"]
    reads = [tc for tc in canon if tc.get("name") == "canon_read"]
    catalogs = [tc for tc in canon if tc.get("name") == "canon_catalog"]

    per_search = []
    for tc in searches:
        args = tc.get("arguments") or {}
        per_search.append({
            "turn_index": tc.get("turn_index"),
            "query": args.get("query"),
            "limit_requested": args.get("limit"),
            "kinds": args.get("kinds"),
            "source_status": args.get("source_status"),
            "include_qa": args.get("include_qa"),
            "results_returned": tc.get("result_item_count", 0),
            "result_bytes": tc.get("result_bytes"),
        })

    read_objects = []
    for tc in reads:
        args = tc.get("arguments") or {}
        read_objects.append({
            "turn_index": tc.get("turn_index"),
            "item_id": args.get("item_id"),
            "source_dir": args.get("source_dir"),
            "artifact": args.get("artifact"),
            "items_returned": tc.get("result_item_count", 0),
            "result_bytes": tc.get("result_bytes"),
        })

    total_results = sum(s["results_returned"] for s in per_search)
    needs, needs_raw = declared_needs(intermediate_text)

    v = []
    if len(searches) > LIMITS["max_canon_search_calls"]:
        v.append(f"canon_search calls {len(searches)} > {LIMITS['max_canon_search_calls']}")
    over = [s for s in per_search if s["results_returned"] > LIMITS["max_results_per_search"]]
    for s in over:
        v.append(f"canon_search returned {s['results_returned']} results "
                 f"> {LIMITS['max_results_per_search']} (limit_requested="
                 f"{s['limit_requested']!r}, query={str(s['query'])[:60]!r})")
    if total_results > LIMITS["max_search_results_total"]:
        v.append(f"search results exposed {total_results} "
                 f"> {LIMITS['max_search_results_total']}")
    if len(reads) > LIMITS["max_canon_read_objects"]:
        v.append(f"canon_read objects {len(reads)} > {LIMITS['max_canon_read_objects']}")

    return {
        "treatment": TREATMENT_ID,
        "limits": dict(LIMITS),
        "enforced_by_harness": False,
        "enforcement_note": ("Observation only. The allowance is an experimental "
                             "treatment, not a technical guard; the harness never "
                             "clamped, blocked or repaired a call."),
        "declared_knowledge_needs": needs,
        "declared_knowledge_needs_count": len(needs),
        "declared_knowledge_needs_raw": needs_raw,
        "canon_search_calls": len(searches),
        "canon_read_calls": len(reads),
        "canon_catalog_calls": len(catalogs),
        "searches": per_search,
        "search_results_total": total_results,
        "canon_read_objects": read_objects,
        "canon_read_items_returned_total": sum(r["items_returned"] for r in read_objects),
        "violations": v,
        "compliant": not v,
    }
