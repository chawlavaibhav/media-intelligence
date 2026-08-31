# Canon Retrieval Contract v0.1

**Status:** PROPOSED — implemented and tested, not accepted as the production retrieval design.
Only a Controller decision can accept it (`coordination/decisions/`).
**Task:** CANON-015 (issue #82).
**Applies to:** `canon/retrieval/**` and the `canon_context` / `canon_detail` tool surface.
**Supersedes:** nothing. EVAL-037's `canon_tools.py` stays exactly as it is, as experiment evidence.

This document states what a caller may rely on. Where the code and this document disagree,
the code is defective and should be repaired to match — except where this document is
wrong, in which case say so rather than quietly changing the code.

---

## 1. What retrieval is for

One sentence: **give a reasoning model the smallest set of accepted Canon knowledge that
actually bears on this customer's outcome, with enough of its epistemic context attached
that the model cannot mistake a hedged observation for a rule.**

"Canon" here means the project's durable creative and production knowledge — what makes
work good, what commonly goes wrong, what to inspect. It is extracted from books and
reports under `canon/knowledge/current/`.

## 2. Scope boundary — what retrieval must never do

Canon answers *what must be understood to specify the work*. It never answers *who or what
should make it*. A retrieval bundle therefore contains no statement about:

- which image, video or audio model to use;
- what a provider charges, or how fast or reliable it is;
- whether a model can execute a described technique.

That is capability routing. It belongs to the Eval / Capability Lab stream and the
Capability Registry, which is deliberately empty
(`coordination/decisions/CONTROLLER-EVAL-030-INTEGRATION-AND-REGISTRY-DISPOSITION-2026-08-28.md`).
`tests/test_canon_retrieval.py::PlanTests::test_catalogue_never_asks_a_capability_routing_question`
enforces this on the question catalogue.

## 3. Guarantees

### G1 — Accepted-only by default
The production surface is `canon/knowledge/current/**`: 24 accepted sources, 120 files.
Every returned object carries `source_status: ACCEPTED`. HOLD candidate material under
`canon/candidates/canon-014/` and the Q&A banks under `canon/qa/canon-014/` are **not
reachable** through the default surface.

They can be loaded for development diagnostics, but only by passing `include_hold` /
`include_qa` **together with a non-empty `diagnostic_reason`**; a corpus loaded that way
sets `production_default: false`, and that flag is stamped on every bundle built from it.
There is no path that returns HOLD material as accepted.

### G2 — Nothing is unbounded
Every budget is a required, positive integer. `None` is rejected at construction, not
treated as "no limit". The enforced bounds are: total items, total characters, characters
per item, sources, items per source, items per lineage group, questions, items per
question, and candidates considered per question.

Two presets ship, `default` and `compact`. Both are bounded. There is no third.

### G3 — The size reported is the size delivered
`size.total_chars` is the exact length of the JSON the model receives
(`bundle.model_payload()`), measured to a fixed point because the field is inside the
object it measures. `estimated_tokens` divides by 4 and is labelled an estimate wherever it
appears; it is never the quantity enforced.

Retriever diagnostics live under `_diagnostics`, are excluded from that count, and are
stripped by `model_payload()`.

### G4 — Status and uncertainty survive
Every item carries its source, object id, object kind, and accepted status. Beyond that,
by kind:

| Kind | What must survive |
|---|---|
| SourceKnowledge | `claim_type`, `interpretation_basis` where the claim is our reading, evidence characteristics, `source_uncertainty`, `extraction_uncertainty`, and every caveat **with its `origin`** |
| SourceConceptSystem | whether the system type, the whole-system claim and its members are the source's or ours; system-level uncertainty |
| OperationalBinding | `status` (141 of 152 accepted bindings are `proposed`, meaning unreviewed), `status_reason`, `evidence_basis`, applicability limits, and a note saying it is our proposal rather than the source's claim |
| Ontology term | origin, `verbatim`, the definition in its origin's frame |
| Ontology concept | `asserts_equivalence` / `asserts_agreement_between_sources` — a canonical concept groups terms for retrieval and claims nothing about them being the same |
| Visual evidence | legibility status, `lost_in_plain_text`, `colour_dependent`, `promoted_to_source_claim` |

A caveat's `origin` is the load-bearing one. `source_stated` means the author limited their
own claim. `extractor_observed` means this project noticed a weakness the author did not
state. Collapsing the two turns a hedged claim into a rule, which is precisely what
issue #82 forbids.

### G5 — Nothing is paraphrased
Every content value is a verbatim slice of a committed corpus field. The only
transformation is truncation, which is applied to prose fields only — never to caveats,
evidence characteristics or uncertainty — and is always marked, by
`delivered_complete: false`, a `trimmed_fields` list, and a visible marker in the text.

### G6 — Retrieval ranking is not a quality judgement
The only ordering produced is fit to the retrieval question. `relevance.basis` says so on
every item. No source, claim or binding is scored, rated or ranked for credibility.
Binding count is never used as a proxy for anything: `canon/HANDOFF.md` records that the
corpus's best-binding source has its weakest evidence.

This mirrors the reasoning behind Audit Gate v0.2's anti-score rule, which governs audit
records rather than this package.

### G7 — Determinism
Given the same corpus fingerprint, the same request text, and the same budgets, the bundle
is byte-identical. No model call, no embedding, no randomness, no wall-clock or filesystem
ordering dependence. Ties break on `(-score, source_dir, item_id)`.

The corpus fingerprint uses the same algorithm as `CANON-CORPUS-INDEX.yaml` and, for the
production surface, recomputes to the committed `fingerprints.accepted_canon.combined_digest`.

### G8 — Fail closed
- A source whose epistemic status the index cannot state is **excluded**, and the exclusion
  is reported in `excluded_sources` with a reason.
- A directory present in the accepted tree but absent from the index is excluded the same
  way. Presence on disk is not admission.
- A missing or empty corpus index raises `CorpusError` rather than returning an empty
  corpus that looks like a working one.
- An item cannot be constructed at all without a real status.

### G9 — Read-only
No module in `canon/retrieval/` opens a file for writing anywhere under `canon/`. The
evaluation writes only inside `canon/retrieval/evaluation/`.

## 4. The consumption contract

**One operation is the design.** `canon_context` returns the useful content directly. The
model is not expected to make a second call, and the bundle reports per item whether one
would even help (`delivered_complete`). `canon_detail` exists for the exceptional case.

**There is no free-text search tool.** Reintroducing unbounded search over the whole corpus
would reintroduce the failure this package exists to fix.

**The plan is visible.** The bundle names the production questions it asked and why each
was selected, so a human can disagree with the plan rather than only with the results.

**Coverage is stated, including its gaps.** `coverage.questions_with_no_item` names any
question the corpus could not answer. Silence about a gap is worse than the gap.

## 5. What this contract does NOT promise

- **Not relevance.** Nothing in the repository labels a Canon object relevant to a brief.
  The retriever finds lexical fit to a question; whether that fit is useful is unmeasured.
  See `evaluation/HUMAN-REVIEW-RUBRIC.md`.
- **Not medium fit.** Retrieval is lexical, so a source about film editing can answer a
  question asked about a still image. The bundle reports each source's own stated domain
  under `spread.source_stated_domains` so the mismatch is visible, but it does not filter
  on it — deciding that film-editing knowledge cannot serve a still image would be this
  project's judgement, and the corpus records no such mapping.
- **Not outcome improvement.** No claim is made that this raises accepted-outcome rate or
  lowers Cost per Accepted Outcome. That needs a controlled model experiment, which
  CANON-015 is not authorised to run and does not run.
- **Not production readiness.** Deterministic tests passing is not the same as being right.

## 6. Versioning

`bundle_version: canon-context-bundle-v0.1`. A change that removes a field, changes the
meaning of a field, or weakens any guarantee above requires a new contract version and a
Controller decision. Adding an optional field does not.
