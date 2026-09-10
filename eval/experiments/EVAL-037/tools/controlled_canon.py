#!/usr/bin/env python3
"""EVAL-037 — CONTROLLED_CANON retrieval governor.

The treatment: Canon research is mandatory, objective-driven and MECHANICALLY BOUNDED.
The tested model still chooses the production question, the search wording, which
returned objects to read, and what knowledge to apply. The harness controls only HOW
MUCH evidence is exposed.

    <= 3 canon_search per trial
    <= 6 results returned by each search      (clamped here, never trusted to the model)
    <= 2 canon_read per research question     (a research question = one canon_search)
    <= 4 canon_read per trial
    => at most 18 search-result items exposed per trial

This module is a WRAPPER. It does not touch canon_tools.py: Canon contents, the BM25
ranking, the tie-break order and the ACCEPTED/HOLD/Q&A status semantics are exactly what
the frozen corpus and the frozen tool produce. The governor only:

  * forces `limit` to at most MAX_RESULTS_PER_SEARCH before the search runs, so an
    oversized payload is never built rather than being built and truncated;
  * refuses a call that would exceed an allowance, returning a structured, Canon-free
    refusal the model can act on instead of an error.

It NEVER chooses a query, names a source, ranks anything, or reads an object on the
model's behalf. Exceeding an allowance is prevented, not punished: a refusal carries no
Canon content and no source_status, so it can never be mistaken for retrieved knowledge.

`canon_catalog` is unchanged and uncounted — it is a table of contents, not evidence.
"""

MAX_SEARCHES = 3
MAX_RESULTS_PER_SEARCH = 6
MAX_READS_PER_QUESTION = 2
MAX_READS_TOTAL = 4


class ControlledCanon:
    """One governor per trial. Fresh state per trial; nothing crosses a trial boundary."""

    def __init__(self, canon):
        self.canon = canon
        self.searches_used = 0
        self.reads_total = 0
        self.reads_since_search = 0
        self.blocked_searches = 0
        self.blocked_reads = 0
        self.results_exposed = 0
        self.exposed_item_ids = []          # what the model was actually shown
        self.ledger = []                    # governor decision per call, for the evidence

    # -- refusals ---------------------------------------------------------
    def _refusal(self, tool, reason, **extra):
        """A Canon-free, structured refusal. Carries no source_status by construction."""
        out = {
            "canon_research_allowance": "exhausted",
            "tool": tool,
            "blocked_by_harness": True,
            "reason": reason,
            "searches_used": self.searches_used,
            "searches_allowed": MAX_SEARCHES,
            "objects_read": self.reads_total,
            "objects_allowed": MAX_READS_TOTAL,
            "instruction": ("Research is complete. Produce the final production package "
                            "now using what you have already retrieved."),
        }
        out.update(extra)
        return out

    # -- governed dispatch -------------------------------------------------
    def dispatch(self, name, args):
        import canon_tools as CT
        args = dict(args or {})

        if name == "canon_catalog":
            # Uncounted and unbounded: a table of contents, not retrieved evidence.
            self.ledger.append({"tool": name, "decision": "allowed", "counted": False})
            return CT.dispatch(self.canon, name, args)

        if name == "canon_search":
            if self.searches_used >= MAX_SEARCHES:
                self.blocked_searches += 1
                self.ledger.append({"tool": name, "decision": "blocked",
                                    "reason": "search allowance exhausted",
                                    "requested_query": args.get("query")})
                return self._refusal(name, f"All {MAX_SEARCHES} Canon searches are used.")

            # The harness owns the result count. The model owns the query.
            requested = args.get("limit")
            clamped = MAX_RESULTS_PER_SEARCH
            if isinstance(requested, int) and 1 <= requested < MAX_RESULTS_PER_SEARCH:
                clamped = requested          # a SMALLER self-imposed bound is honoured
            args["limit"] = clamped

            out = CT.dispatch(self.canon, name, args)
            self.searches_used += 1
            self.reads_since_search = 0      # a new search opens a new research question
            n = len(out.get("results") or [])
            self.results_exposed += n
            self.exposed_item_ids += [str(r.get("item_id")) for r in (out.get("results") or [])]
            out["harness_result_limit"] = MAX_RESULTS_PER_SEARCH
            out["harness_limit_applied"] = clamped
            out["limit_source"] = ("caller (below the harness cap)"
                                   if clamped != MAX_RESULTS_PER_SEARCH else "harness")
            out["searches_remaining"] = MAX_SEARCHES - self.searches_used
            out["objects_you_may_read_next"] = min(
                MAX_READS_PER_QUESTION, MAX_READS_TOTAL - self.reads_total)
            self.ledger.append({"tool": name, "decision": "allowed",
                                "query": args.get("query"),
                                "requested_limit": requested, "applied_limit": clamped,
                                "results_returned": n})
            return out

        if name == "canon_read":
            if self.reads_total >= MAX_READS_TOTAL:
                self.blocked_reads += 1
                self.ledger.append({"tool": name, "decision": "blocked",
                                    "reason": "total read allowance exhausted",
                                    "requested": args})
                return self._refusal(name, f"All {MAX_READS_TOTAL} Canon reads are used.")
            if self.reads_since_search >= MAX_READS_PER_QUESTION:
                self.blocked_reads += 1
                self.ledger.append({"tool": name, "decision": "blocked",
                                    "reason": "per-question read allowance exhausted",
                                    "requested": args})
                return self._refusal(
                    name,
                    f"{MAX_READS_PER_QUESTION} objects already read for this research "
                    f"question. Search again for a different production question, or "
                    f"produce the package.",
                    reads_for_this_question=self.reads_since_search)

            out = CT.dispatch(self.canon, name, args)
            self.reads_total += 1
            self.reads_since_search += 1
            target = str(args.get("item_id") or args.get("source_dir"))
            self.ledger.append({"tool": name, "decision": "allowed", "target": target,
                                "was_in_exposed_results": target in self.exposed_item_ids,
                                "reads_total": self.reads_total})
            return out

        raise ValueError(f"tool {name!r} is not exposed in EVAL-037")

    # -- evidence ----------------------------------------------------------
    def summary(self):
        return {
            "treatment": "CONTROLLED_CANON",
            "max_searches": MAX_SEARCHES,
            "max_results_per_search": MAX_RESULTS_PER_SEARCH,
            "max_reads_per_question": MAX_READS_PER_QUESTION,
            "max_reads_total": MAX_READS_TOTAL,
            "max_items_exposable": MAX_SEARCHES * MAX_RESULTS_PER_SEARCH,
            "searches_used": self.searches_used,
            "reads_used": self.reads_total,
            "results_exposed": self.results_exposed,
            "blocked_searches": self.blocked_searches,
            "blocked_reads": self.blocked_reads,
            "governor_ledger": self.ledger,
        }
