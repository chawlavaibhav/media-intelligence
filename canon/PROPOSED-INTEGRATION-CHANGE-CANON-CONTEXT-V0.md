# Proposed integration change — CANON_CONTEXT packaging shape (v0.1)

**From:** Canon worker · **To:** Controller · **Date:** 31 Aug 2026
**Severity:** `CROSS_STREAM` — proposes a consumption boundary between Canon and production
reasoning. Not `ARCHITECTURAL`: it creates no IR, no planner, no runtime.
**Status:** proposal only. Nothing under `coordination/` was edited, no decision is claimed, and no
execution or spend is requested.

## OBSERVATION

`CONTROLLER-EVAL-037-CONCLUSION-2026-08-31.md` closed the Canon-value question and left the
retrieval/consumption question explicitly open, unauthorised, and deliberately unanswered.

The observation this proposal rests on is narrower than that open question, and does not require
reopening it: **EVAL-037 diagnosed a failure of the search/read interaction, but the failing step is
the hand-off, not the search.** Bounded objective-driven search already worked. What did not work
was everything after it — the model treated a ranked envelope as an answer and did not read.

A packaging shape can be specified without deciding how retrieval selects what to package.

## EVIDENCE

All from committed artifacts; recompute with
`python3 canon/validation/recount_eval037_retrieval.py`.

| Fact | Value | Source |
|---|---|---|
| Repair-lane completion | 2/18 complete, 16/18 failed execution | `runs/sonnet-full-canon-repair-001/result.json` |
| Canon calls in the 2 surviving transcripts | 3 searches, **0 reads** | run transcripts |
| Bytes returned by those 3 searches | 4,082,082 total; 2,641,642 largest | run transcripts |
| Admission mix of those results | 411 accepted, 962 HOLD, 441 QA | run transcripts |
| Lane context cost | 1,505,004 input tokens over 4 provider turns, USD 3.228778 | `result.json` |
| Controlled lane behaviour | 18/18 complete, 53 searches, **1 read** in the whole lane | `eval/experiments/EVAL-037/CONCLUSION.md` |
| Optional Canon uptake | Gemma FULL_CANON used Canon 0/18 | same |
| Hand-built context precedent | 12 oracle contexts, 3–4 entries, 2,571–3,655 bytes | `canon/experiments/v1/value-gate/oracle-contexts/` |

Two of these deserve emphasis because they point the same way. Across both the unbounded and the
controlled lanes, models searched and did not read — 0 reads from 3 searches in one, 1 read from 53
in the other. And the envelopes they were reading from were **majority non-admissible**: HOLD
material outnumbered accepted Canon roughly 2.3:1, because nothing enforced the admission boundary
at the point of consumption.

## PROPOSED CHANGE

Adopt **CANON_CONTEXT v0.1** (`canon/context/CANON-CONTEXT-SPEC-v0.1.md`) as the *shape* in which
Canon is handed to production reasoning: a bounded, per-request, already-read object with five
sections — production questions, key guidance (six mandatory fields each), conflicts, limits, and a
source trace — validated fail-closed by `canon/validation/validate_canon_context.py`.

Concretely, adoption would mean:

1. Canon is delivered as a finished object, not as a corpus plus a search tool.
2. The admission boundary (accepted sources, Audit Gate `complete`, no HOLD, no Q&A) is enforced
   **mechanically at the hand-off**, not by convention upstream.
3. Every principle is rendered verbatim from a committed id, inheriting the anti-drift rule already
   in `build_oracle_contexts.py`.
4. Uncertainty, conflicts and scope limits travel with the guidance rather than being dropped in
   packaging.

## EXISTING DECISIONS AFFECTED

| Decision | Effect |
|---|---|
| `CONTROLLER-EVAL-037-CONCLUSION-2026-08-31.md` | **None contradicted.** No lane rerun, no roster expansion, no new Canon/no-Canon experiment, no media generation. This proposes a shape, not a retrieval mechanism, and does not claim the open question is answered. |
| `CONTROLLER-CANON-014-INTEGRATION-2026-08-30.md` | **Reinforced.** Candidate/Q&A retrieval is not enabled in ordinary runtime; the validator now enforces that at the consumption boundary. |
| `CANON-004`/`CANON-005` Audit Gate | **Reinforced.** The gate already blocks unaudited material from downstream consumption; this makes a CANON_CONTEXT a checked instance of that rule. |
| Registry admission rules (`PROJECT-MEMORY.md` §4.2) | **Untouched.** Spec R9 states that a CANON_CONTEXT is never capability evidence and never a Registry input. |
| Frozen measurement contracts, CANON-010 request contract, Capability Contract v2 | **Untouched.** |

## EXPECTED BENEFIT

- Removes the two mechanical failure modes that cost EVAL-037 16 of 18 trials in one lane: context
  overflow, and non-consumption of optional Canon.
- Makes the admission boundary checkable rather than assumed, which the observed 2.3:1 HOLD ratio
  suggests it currently is not.
- Puts a declared, enforced ceiling on Canon's context cost — a CpAO input the programme currently
  cannot bound.
- Gives any future retrieval work a fixed output contract to be measured against, so retrieval
  designs become comparable rather than each being evaluated on its own terms.

## RISK

- **The budget numbers are weakly grounded.** They come from the oracle-context precedent and one
  worked example, not from accepted-outcome evidence. A budget that is too tight harms outcomes from
  the opposite direction to the unbounded envelope, and would do so less visibly.
- **Packaging cost moves upstream, it does not vanish.** Something must select and render the
  entries. This proposal does not say what, and a bad selector inside a tidy object is harder to
  notice than a bad search.
- **Verbatim rendering is an auditability choice with an unmeasured comprehension cost.** SPEC-03
  claims are written for extraction fidelity, not for a model reading them mid-production.
- **A schema can be satisfied without being useful.** A validator PASS says the object cites real
  audited Canon within budget and answers its own questions; it cannot say the guidance is right for
  the brief. Treating PASS as quality would be the same category error as treating a ranked envelope
  as an answer.

## FALSIFIER

The proposal is wrong if a model given a packaged CANON_CONTEXT performs no better than one given
the same Canon through the current search interface — that is, if the read/no-read gap was never
the binding constraint. The spec lists three further falsifiers in §6.

Testing any of them requires a Controller-authorised experiment. **None is requested here**, and
under `CONTROLLER-EVAL-037-CONCLUSION-2026-08-31.md` any such work would need to be justified by
accepted-outcome improvement, repeatability, latency/context cost or CpAO — not by the packaging
being more sophisticated than a search box.

## WHAT IS ASKED OF THE CONTROLLER

Nothing urgent, and nothing that unblocks other work. One of:

1. **Note and shelve** — the artifacts stay as a Canon-stream proposal until retrieval work is
   authorised; or
2. **Adopt the shape only** — CANON_CONTEXT v0.1 becomes the required output contract for any future
   Canon hand-off, leaving selection open; or
3. **Reject** — in which case the four files under `canon/context/` and the two validators should be
   removed rather than left to look authoritative.

The programme is in planning mode per the EVAL-037 disposition, so option 1 is the expected default.
