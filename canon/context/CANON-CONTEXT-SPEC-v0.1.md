# CANON_CONTEXT — packaging spec and authoring guidance, v0.1

**Status: a Canon-stream proposal. No Controller decision adopts it.** It defines a *shape* for
Canon delivered into production reasoning; it authorises nothing, changes no frozen contract, and
does not answer the open retrieval question. `coordination/CONTROL-STATE.md` governs what is
actually active. Adoption would require a Controller decision — see
`canon/PROPOSED-INTEGRATION-CHANGE-CANON-CONTEXT-V0.md`.

**Owner:** Canon (`canon/CHARTER.md` — "testing consumption shapes" is Canon's).
**Scope:** how Canon is *packaged and handed over*. Not which Canon is retrieved, not by what
search algorithm, not which model consumes it.

---

## 1. Why this exists

`coordination/decisions/CONTROLLER-EVAL-037-CONCLUSION-2026-08-31.md` closed the Canon-value
question ("Canon helps") and left one open:

> What production retrieval / consumption mechanism gives a reasoning model the smallest, most
> relevant, highest-value Canon context for the customer's outcome?

EVAL-037 did not fail to answer that by accident. It established that the *interface* is the
problem, and the failures are specific enough to design against:

| Observed failure | Evidence |
|---|---|
| Optional Canon is simply not used | Gemma FULL_CANON used Canon **0/18** times (`eval/experiments/EVAL-037/CONCLUSION.md`) |
| Unbounded Canon destroys the run | Repaired Sonnet unbounded FULL_CANON completed **2/18**; 16/18 context-overflowed (`.../runs/sonnet-full-canon-repair-001/result.json`) |
| Search envelopes are enormous | The 2 surviving transcripts made **3 searches returning 4,082,082 bytes**, largest single search **2,641,642 bytes** |
| Ranked results are treated as sufficient | Those 3 searches produced **0 reads**. Sonnet CONTROLLED_CANON: 53 searches, 1 read in the whole lane |
| Envelopes are majority non-admissible | Those 3 searches returned **411 accepted, 962 HOLD, 441 QA** items — HOLD outnumbered accepted ~2.3:1 |
| Context cost is the binding constraint | The repair lane burned **1,505,004 input tokens over 4 provider turns**, USD 3.228778, for 2 usable trials |

Recompute the transcript figures from a fresh clone:

```sh
python3 canon/validation/recount_eval037_retrieval.py
```

The conclusion this spec draws: **stop shipping a corpus and a search box; ship a small, finished,
already-read object.** A model that never performs the follow-up read must be handed the read.

The size target is not invented. The hand-built oracle contexts in
`canon/experiments/v1/value-gate/oracle-contexts/` — Canon's own best-effort "ideal context" for a
brief — are **3–4 entries, 377–585 words, 2,571–3,655 bytes**. That is three orders of magnitude
below the search envelope above, and it is the envelope this spec budgets to.

## 2. What CANON_CONTEXT is

A **bounded, self-contained, per-request object**: everything the reasoning model gets from Canon
for one customer outcome, with nothing left to fetch. It replaces the search/read interaction at
the point of consumption; it does not replace retrieval, which decides what goes *into* it.

Five sections, in this order:

```yaml
production_questions:   # what this context is for — the outcome decisions it must inform
key_guidance:           # the answers, each with six mandatory fields
conflicts:              # where cited Canon disagrees, and the rule for proceeding
do_not_overgeneralize:  # the limits of what was just said
source_trace:           # what each claim is, where it came from, and its admission status
```

### 2.1 It is a projection, not new authoring

The six `key_guidance` fields are not a new authoring burden. They already exist in the frozen
SPEC-03 extraction and are copied across:

| CANON_CONTEXT field | SPEC-03 origin |
|---|---|
| `principle` | `claim` (verbatim), labelled by `concept_label` |
| `applicability` | `scope.domain_discussed_by_source` + `scope.conditions` |
| `concrete_implication` | `source_stated_remedies`, else `mechanism.text`, else `examples.positive` |
| `failure_mode` | `source_stated_problems`, else the `source_stated` `caveats` |
| `evidence` | `provenance` + `evidence.characteristics` |
| `uncertainty` | `evidence.source_uncertainty` + `evidence.extraction_uncertainty` + `caveats` |
| `conflicts` | `intra_source_relations` where relation ∈ {`contradicts`, `qualifies`, `qualified_by`} |
| `do_not_overgeneralize` | `scope.conditions` + `source_stated` caveats |
| `source_trace` | `sk_id` / `scs_id` + owning directory + Audit Gate status |

This matters for a reason beyond convenience: **a field that has to be written by hand can be
written better than the source.** `canon/experiments/v1/value-gate/build_oracle_contexts.py`
already names that failure mode — a worker paraphrasing a source into a stronger version silently
invalidates any comparison built on it. CANON_CONTEXT inherits that script's three rules:

1. render by id, never paraphrase by hand;
2. fail closed on an id that does not exist;
3. fail closed on a source whose Audit Gate record is not `complete`.

## 3. Authoring rules

### R1 — Bounded by construction, not by convention
Every context declares `budget` and the validator enforces it, in three dimensions:

| Dimension | Default | Where the number comes from |
|---|---|---|
| `max_guidance_entries` | 8 | twice the oracle precedent's 3–4 entries |
| `max_principle_bytes` | 4096 | the oracle contexts' own upper bound (3,655 bytes) rounded up — this is the dimension the precedent actually bounds |
| `max_serialized_bytes` | 16384 | the principle payload plus the six-field scaffolding, measured at ~5.7× on the worked example |

The two payloads are budgeted separately because they behave differently. The oracle precedent
bounds *claim text*: the worked example's five verbatim principles total **2,491 bytes**, squarely
inside the oracle range of 2,571–3,655. What the oracle contexts never carried is the rest of the
structure — applicability, implication, failure mode, uncertainty, conflicts, limits and trace —
and that is what takes the finished object to **14,240 bytes**. Budgeting the whole object against
the oracle number would have been a category error; a first draft of this spec made exactly that
mistake and the validator caught it.

Even so, 16 KiB is **~161× smaller than the smallest single unbounded search envelope observed in
EVAL-037** (2,641,642 bytes), and ~249× smaller than one trial's total.

A context that cannot fit is a retrieval failure to be reported, never a budget to be raised
silently.

*These numbers are calibrated against the oracle-context precedent and one worked example. There is
no accepted-outcome evidence behind them; treat them as a declared constraint to be tuned by later
authorised work, not as a finding.*

### R2 — Objective-driven: every entry earns its place against a question
`production_questions` is written **first**, from the request — not from what retrieval happened to
return. Each question names the outcome decision it informs. The validator enforces both
directions: no question without an answer, no guidance entry that answers no question. This is the
one EVAL-037 mechanism that worked — bounded objective-driven search completed 18/18 with zero
overflows — carried from the query side to the packaging side.

### R3 — Delivered read, not retrievable
No entry may depend on a follow-up fetch. If a claim needs its mechanism to be actionable, the
mechanism is in `concrete_implication`. Ranked-envelope-as-answer is the observed failure; a
context with dangling references reproduces it.

### R4 — Accepted Canon only
Every ref resolves to a live source under `canon/knowledge/current/` whose Audit Gate record is
`complete`. **HOLD/candidate material (`canon/candidates/`) and Q&A banks (`canon/qa/`) must not
appear** — including in `conflicts`, which is the tempting exception. Per
`CONTROLLER-CANON-014-INTEGRATION-2026-08-30.md`, candidate/Q&A retrieval is not enabled in
ordinary runtime; the EVAL-037 envelopes were majority-HOLD precisely because nothing enforced this
at the boundary.

### R5 — Verbatim principles
`principle` is the committed `claim` text, whitespace-normalized. `render_mode: verbatim_claim` is
the default and is mechanically checked against the extraction. `condensed` exists for the case a
claim genuinely does not fit, and requires `condensed_review: human` plus the digest of the source
field so drift is detectable.

### R6 — Uncertainty travels with the claim
`uncertainty` is mandatory and non-empty on every entry. Canon's records distinguish
`source_uncertainty` from `extraction_uncertainty`, and a large share of the visual corpus carries
`figure_not_inspected`. A production context that drops that distinction is asserting more than
Canon knows. `"none recorded"` is a legitimate value; an empty string is a defect.

### R7 — Conflicts are surfaced with a rule, never silently resolved
Where cited Canon disagrees, the conflict is stated and either given a `resolution_rule` (almost
always a scope rule — see the worked example) or marked `unresolved: true`. Deleting one side to
make the context tidy is manufacturing agreement, which
`canon/findings/CANON-014-CROSS-SOURCE-OBSERVATIONS.md` §3.2 flags as the mirror failure of
manufacturing disagreement.

### R8 — `do_not_overgeneralize` is mandatory and non-empty
This section exists because of the strongest negative result in EVAL-037's conclusion: Canon did
**not** win every brief. Sonnet NO_CANON led B03 and B04 outright. A context that presents its
guidance as unconditional overstates the programme's own evidence.

### R9 — The context establishes nothing
CANON_CONTEXT is book knowledge packaged for reasoning. It is never evidence about model
capability, never a Capability Registry input, and never a benchmark ground truth
(`PROJECT-MEMORY.md` §4.2). It is an input to a production decision, not a claim about the world we
have measured.

## 4. Files

| File | Role |
|---|---|
| `canon/context/CANON-CONTEXT-SPEC-v0.1.md` | this document |
| `canon/context/canon-context-schema-v0.1.yaml` | field-level schema |
| `canon/context/build_example_context.py` | renders the worked example from committed ids |
| `canon/context/examples/B06-watch-hero.canon-context.yaml` | the rendered worked example |
| `canon/validation/validate_canon_context.py` | deterministic validator, fail-closed |
| `canon/validation/recount_eval037_retrieval.py` | recomputes the §1 retrieval figures |
| `tests/test_canon_context_validator.py` | positive + negative fixtures |

Validate:

```sh
python3 canon/validation/validate_canon_context.py canon/context/examples/*.yaml
```

Exit status is the fact. A PASS is a linkage and admission check — it says the context cites real,
audited, accepted Canon within budget and answers its own questions. **It says nothing about
whether the guidance is right for the brief**, which no validator can check.

## 5. What this spec deliberately does not decide

- **How the entries are selected.** Ranking, embedding, keyword, or hand-selection — all produce
  the same object. That is the open question and it stays open.
- **Whether packaging beats search at improving outcomes.** Unmeasured. The EVAL-037 controlled
  lanes are suggestive about *executability*, not about accepted-outcome rate.
- **Where in the architecture it is built.** Between Normalized Request and Creative IR is the
  natural seam, but Production IR and the Planner do not exist and this spec does not create them.
- **The budget values.** See R1.

## 6. Falsifiers

This spec is wrong if any of these turn out to hold:

1. A model given a packaged CANON_CONTEXT performs no better than one given the same Canon through
   search — i.e. the read/no-read gap was never the binding problem.
2. The 8-entry / 8 KiB envelope routinely cannot hold what a real brief needs, so the budget is
   doing the harm the unbounded envelope did, from the other side.
3. `conflicts` and `do_not_overgeneralize` are consistently ignored by consuming models, making
   them cost without effect.
4. Verbatim rendering is materially worse than condensation for model comprehension — in which case
   R5 trades outcome quality for auditability and the trade needs restating.
