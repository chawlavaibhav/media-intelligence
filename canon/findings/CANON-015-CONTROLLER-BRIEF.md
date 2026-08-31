# Controller Brief — CANON-015

**TASK:** CANON-015 — Retrieval / consumption maturity (issue #82)
**STATUS:** completed — needs_controller_review
**SPEND:** USD 0. No model call, no provider call, no media generated, no book ingested,
no HOLD candidate admitted, no Audit Gate change, no EVAL-037 artifact modified.

---

## HUMAN SUMMARY

EVAL-037 concluded that Canon helps but that the way we hand it to a reasoning model is not
mature. CANON-015 built the replacement and measured it against what EVAL-037 actually did.
Nothing here is authorised to be switched on; this is a proposal with evidence attached.

**The most important thing I found was not the size problem.** Reading the committed
EVAL-037 transcripts object by object shows that in the best-performing lane —
Sonnet under a controlled retrieval allowance, the only lane that completed all 18 trials —
**53.5% of the Canon the model received was HOLD material**: knowledge the project has
deliberately *not* admitted. A further 22.2% were Q&A items, which the corpus itself labels
"not benchmark ground truth, not independent corroboration". Only **42.2%** was accepted,
non-Q&A Canon. On the watch brief, the first search of one trial returned **8 held items out
of 8**, and zero accepted ones.

Nothing was mislabelled — every object stated its own status correctly, exactly as the
CANON-014 integration decision required. The ranking simply put held material first, because
Q&A items are short and question-shaped and the lexical ranker rewards that. **This means the
Controller's conclusion "Canon helps" was reached on evidence where the model was reading
mostly non-accepted knowledge.** That does not overturn the conclusion — the lane won or
co-led on two of six briefs — but it changes what the conclusion is about. It is closer to
"the wider knowledge corpus helps" than "accepted Canon helps", and those are different
claims.

**What was built.** A retrieval layer that reads accepted Canon only, asks a small set of
explicit production questions instead of paraphrasing the brief, ranks within each object
kind rather than pooling them, caps how much any one book or any one *origin* can
contribute, and returns a single bundle containing the knowledge itself rather than a
ranked list of pointers.

**What it measures, on the same six real briefs, at USD 0:** one retrieval operation instead
of three; **27,862 characters instead of 66,966 bytes (−58.4%)**; **100% accepted-status
purity instead of 46.5%**; every planned production question answered; 96% of items
delivered whole, so a second tool call is normally unnecessary.

**What it does not show.** Nothing here says the retrieved knowledge is the *right*
knowledge. Nothing in the repository labels a Canon object relevant to a brief, and I did
not invent such labels. Relevance needs a person; a rubric and six ready-to-read bundles are
committed for that. Outcome effect — accepted-outcome rate, Cost per Accepted Outcome —
needs a controlled model experiment, which I did not run and am not authorised to run.

**The decision needed** is whether this interface is strong enough to justify that small
controlled experiment.

---

## WHAT I DID

Read the durable authority in the order issue #82 specified, then read the four frozen
EVAL-037 branches read-only and recomputed retrieval behaviour from the committed
transcripts rather than trusting the summary figures. Implemented a read-only retrieval and
context-building package under `canon/retrieval/` with hard budgets, an accepted-only
default, a production-question planner, per-kind ranking with an explicit cross-kind
allocation, diversity limits driven by the Audit Gate's own lineage records, and an
evidence-preserving bundle format. Wrote 50 deterministic tests and an offline evaluation
that compares three columns: what EVAL-037's model actually received, the same queries
replayed through EVAL-037's unmodified tool module as a control, and the new retriever.

---

## OBSERVED

All figures recomputed from committed bytes; none quoted from a summary.

**EVAL-037, Sonnet CONTROLLED_CANON lane, 18 trials** (`work/eval-037-sonnet-controlled-canon`):

- 53 searches, 1 read, **424 objects, 1,205,392 bytes** — a mean of **66,966 bytes per trial**.
- Status split of those 424 objects: accepted non-Q&A **179 (42.2%)**, accepted Q&A 18
  (4.2%), HOLD non-Q&A 133 (31.4%), HOLD Q&A 94 (22.2%). **HOLD total: 227 (53.5%).**
- A single search returned a mean of **4.5 of its 8 results from one source**; worst case
  8 of 8.
- 13 objects were returned twice within the same trial.
- Accepted share by brief: B05 café dialogue **88%**, B02 poster 57%, B03 drink 47%, B06
  watch 33%, B04 skincare 28%, B01 RentOK **26%**.

**Unbounded lanes, quoted not re-run:** `sonnet-full-canon-repair-001` completed 2 of 18
(16 execution failures); `gemma-required-canon` failed 18 of 18 technically.

**Corpus, verified on `main` at `5b95da1`:** the accepted-Canon fingerprint recomputes to
`a9cee40f…7eb9` over 120 files, identical to `CANON-CORPUS-INDEX.yaml`. 24 accepted sources,
1,623 retrievable objects: 677 SourceKnowledge, 78 concept systems, 152 operational
bindings, 589 ontology terms, 67 ontology concepts, 60 visual-evidence items.

**Composition facts that shaped the design:**

- **141 of the 152** accepted operational bindings carry `status: proposed` — nobody has
  reviewed them.
- **63 of the 152** bind to `governance` (50) or `benchmark` (13) targets: SPEC-04 defines
  these as being about this project's own ontology and test-case machinery, not about making
  the customer's work. That is **41% of the binding surface**. EVAL-037 surfaced one of them
  — a Catmull binding about how to score an evaluator's feedback — as an answer to "what
  goes wrong in a premium watch photograph".
- Exactly **two pairs** of accepted sources are recorded as not independent of each other:
  the two *Grammar of the...* companion volumes, and Murch's own book with the Ondaatje
  conversations in which he is the speaker.
- A rendered SourceKnowledge object costs a median 2,046 characters (p90 2,940, max 5,682).

**CANON-015 measured on the same six briefs** (`canon/retrieval/evaluation/RESULTS-v0.1.md`):

| Measure | observed EVAL-037 | replayed EVAL-037 | CANON-015 |
|---|---|---|---|
| Retrieval operations per job | 3.0 | 3.0 | **1** |
| Context handed to the model | 66,966 bytes | 66,708 bytes | **27,862 chars (−58.4%)** |
| Accepted-status purity | 46.5% | 46.5% | **100%** |
| Distinct sources | 8.9 | — | 6.7 (6.5 independent origins) |
| Redundancy (mean pairwise overlap) | not recoverable | 0.153 | **0.117** |
| Production questions answered | not asked | not asked | **100%** |
| Items delivered whole | n/a | n/a | **96%** |

The `compact` preset gives a mean of 13,722 characters. The replay control agrees with the
observed lane to within 0.4% on bytes, so the difference is the interface, not corpus drift.

**Tests:** 50 tests, 164 subtests, pass in ~11 seconds with no network. They cover budget
enforcement, accepted-only default, status and uncertainty preservation, stable ordering,
per-source and per-lineage saturation, near-duplicate suppression, byte-identical
reproducibility across separate corpus loads, and fail-closed behaviour on unknown status, a
missing index, and a directory present on disk but absent from the index.

---

## INFERRED

**The consumption problem was mis-stated, and the correction matters.** The widely repeated
finding is that the lane made 53 searches and only 1 read, so models treat ranked envelopes
as sufficient. Reading `canon_tools.py` shows why they did: `canon_search` already returned
each result's **complete stored object**. A follow-up read was usually redundant *by
construction*. The models were not skipping a step they needed. On the evidence, the real
defects are cost, status purity, redundancy and framing — not a missing tool call. I have
built for those, and issue #82's premise that "a second read call cannot be relied on"
happens to lead to the right design for a different reason than the one stated.

**Cross-kind ranking was quietly biased.** EVAL-037 pooled all object kinds into one BM25
index and flattened every string leaf, dictionary keys included, into the searchable text.
An ontology term is roughly 20 tokens and a SourceKnowledge object roughly 250, so a single
pool over-selects the shortest objects, and indexing keys lets a query score on the words
`provenance` or `explicitly_stated`. Scoring within a kind and allocating across kinds by an
explicit visible order removes both. **This is reasoning about the mechanism, not a measured
relevance gain** — I have no relevance ground truth and did not invent one.

**The accepted corpus is thin exactly where the accepted share was lowest.** The briefs whose
EVAL-037 searches drew mostly HOLD material — Indian market context (B01, 26%), creator-style
performance video (B04, 28%), premium product photography (B06, 33%) — are the same domains
`coordination/ASSUMPTIONS.md` §14 already names as the library's real weakness. This is
independent corroboration of that entry from a different direction. It also explains
CANON-015's own weakest result: B04 draws only 4 distinct sources against a cap of 8, which is
a corpus fact rather than a retriever fault.

---

## SURPRISES / BELIEF UPDATES

1. **The best lane was reading mostly non-accepted knowledge.** I expected the accepted/HOLD
   split to be a detail. It is 53.5% HOLD, and it reframes what EVAL-037's positive result is
   evidence *for*. The next worker should not read "Canon helps" as "accepted Canon helps".
2. **"Only 1 read" is weak evidence of a consumption failure.** See INFERRED. Do not take
   that number at face value without reading `canon_tools._stamp`, which puts the whole raw
   item into every search result.
3. **41% of the binding surface is not about making media at all.** I expected bindings to be
   the most directly useful kind. Half of them are about our own ontology and benchmarks.
4. **A substring bug survived into a working prototype.** Cue matching on substrings fired
   the lighting question on the word "dia**log**ue". It is fixed and regression-tested, and it
   is a reminder that a deterministic rule is only as good as its boundaries.

---

## FAILURES / BLOCKERS

None blocking. Three things I chose not to do, each with its consequence:

- **No media-domain filter.** A film-editing claim can be retrieved for a still-image brief,
  and on B06 one ranks first for the composition question. Filtering would need a mapping
  from a source's stated domain to a delivery medium, which does not exist in the corpus;
  inventing one would be this project's judgement presented as the source's. Instead the
  bundle reports every selected source's own stated domain so the mismatch is visible. This is
  the top candidate for the next iteration.
- **No relevance number.** Deliberate. See UNKNOWN.
- **No change to `canon/knowledge/current/**`, the Audit Gate, any SPEC, or any EVAL-037
  artifact.** The task forbade it and nothing made it necessary.

---

## UNKNOWN / NOT VERIFIED

- **Whether the retrieved knowledge is the right knowledge.** Unmeasured. No relevance labels
  exist and I did not create any. `canon/retrieval/evaluation/HUMAN-REVIEW-RUBRIC.md` plus
  the six bundles in `evaluation/bundles/` is about 90 minutes of human work and would settle
  it directionally.
- **Whether any of this changes an accepted outcome or Cost per Accepted Outcome.** Requires
  a controlled model experiment. Not run, not authorised.
- **Whether the defaults are the right defaults.** 12 items and 30,000 characters are set
  against measured EVAL-037 behaviour, not against any evidence about what a model uses well.
- **Whether a compiled checklist would do the same job.** See ASSUMPTIONS CHALLENGED.
- **Six briefs.** Real, and used by EVAL-037, but six.

---

## ASSUMPTIONS CHALLENGED

**§7 — "Runtime RAG is the best way to consume Canon" (hypothesis, never examined).** Its
review trigger reads: *"Before any vector database is built. No retrieval infrastructure
should be built until this is tested."* I built no vector database and no embedding model —
this is deterministic lexical retrieval over committed YAML — so I read the trigger as not
fired, and issue #82 authorised the work explicitly. But the entry's falsifier is still
untested and is now **cheap**: compile the same accepted knowledge into a fixed checklist per
production question and compare it against a bundle, offline, at USD 0. I recommend it below.
I have not marked the entry as challenged; that is the Controller's call.

**§14 — "The library is representative enough to bootstrap the Canon".** Strengthened in the
direction the entry already leans. See INFERRED.

---

## LOCAL IMPLICATIONS

Canon now has a retrieval layer with a written contract, a fingerprint anchor and a test
suite, replacing an experiment-only tool module. `canon/knowledge/current/**` is untouched,
so every Audit Gate record remains valid for the exact bytes it audited.

---

## CROSS-STREAM IMPLICATIONS

**CROSS_STREAM (Eval).** The accepted/HOLD split above qualifies what EVAL-037's positive
result is evidence for. I propose the EVAL-037 conclusion record gains one sentence of
scope — *the lane's Canon exposure was 53.5% HOLD material* — rather than any change to its
finding. I have not edited `eval/`; that is a Controller decision and, if taken, a proposed
integration change.

**CROSS_STREAM (Eval).** Any future Canon experiment should record its accepted/HOLD
exposure per trial as a first-class number. EVAL-037 recorded byte counts and item counts but
not the status composition of what the model saw; recovering it required re-parsing the
transcripts.

---

## ARCHITECTURAL IMPLICATIONS

None that required a stop. No SPEC meaning changed, no frozen contract reopened, no
Production IR or Planner created, no Capability Registry row, no provider or model named.
The scope boundary between Canon knowledge and capability routing is now enforced by a test
rather than by convention.

---

## DECISIONS NEEDED FROM CONTROLLER

1. **Is accepted-only the right production default?** CANON-015 assumes yes, following the
   CANON-014 integration decision. The cost is visible: on the Indian-market and
   creator-video briefs, most of what EVAL-037's model found useful-looking was held
   material, and an accepted-only retriever cannot reach it. The alternative is not "expose
   HOLD" but "decide whether those held sources should be audited toward admission".
2. **Does the EVAL-037 conclusion record need the one-sentence scope note?** The finding
   stands either way; what changes is what a future reader thinks it established.
3. **Should the human relevance review happen before any model experiment?** ~90 minutes,
   USD 0, and it is the only thing that can tell us whether the selection is any good.
4. **Is a small controlled model-level retrieval test now warranted?** I recommend deferring
   this until decision 3 is done. I am not authorised to self-authorise it and have not.

---

## EVIDENCE WORTH HUMAN INSPECTION

1. `canon/retrieval/evaluation/bundles/B06-canon-context.json` — one complete bundle as a
   model would receive it. Notice that each item carries its caveats **with the origin that
   says whose doubt it is**, and that the one binding says it is an unreviewed proposal.
2. `canon/retrieval/evaluation/EVAL-SET-v0.1.yaml`, trial `E037SCC-sonnet-B06-R1`, first
   search — 8 returned objects, all HOLD. This is the single clearest picture of the problem.
3. `canon/retrieval/evaluation/RESULTS-v0.1.md`, the per-brief table — notice the accepted
   share before the change ranges from 26% to 88% depending on the brief.

---

## FILES CREATED / MODIFIED

**Created — `canon/retrieval/`:** `README.md`, `RETRIEVAL-CONTRACT-v0.1.md`, `__init__.py`,
`budgets.py`, `corpus.py`, `questions.py`, `plan.py`, `rank.py`, `bundle.py`, `tools.py`,
`cli.py`.

**Created — `canon/retrieval/evaluation/`:** `build_eval_set.py`, `EVAL-SET-v0.1.yaml`,
`run_offline_eval.py`, `results-v0.1.json`, `RESULTS-v0.1.md`, `HUMAN-REVIEW-RUBRIC.md`,
`bundles/B01…B06-canon-context.json`.

**Created — elsewhere:** `tests/test_canon_retrieval.py`, this brief.

**Modified:** nothing. No existing file in the repository was changed.

---

## RECOMMENDED NEXT STEP

**Run the human relevance review first — 90 minutes, USD 0, no new code.** Everything else
depends on its answer. If items come back mostly `useful`, the interface has earned a small
controlled model test. If they come back mostly `true_but_not_for_this_job`, the next work is
the medium-fit problem, not a model experiment, and a model experiment run first would have
wasted the money.

**Then, and still at USD 0, test assumption §7's falsifier.** Compile the same accepted
knowledge into a fixed per-question checklist and compare it against a retrieved bundle on
the same six briefs. If the checklist matches, retrieval is unnecessary complexity, and that
is far cheaper to learn now than after a paid experiment.

Only after both would I recommend a controlled model-level test, and its primary measure
should be production-package quality and accepted-outcome potential, not retrieval
sophistication.

---

## EPISTEMIC CHECK

Every number in OBSERVED was recomputed from committed bytes and can be reproduced by the
two commands in `RESULTS-v0.1.md`. Interpretations are confined to INFERRED and SURPRISES and
are labelled. The mechanism argument for per-kind ranking is explicitly marked as reasoning
rather than a measured gain. No relevance, precision, recall or outcome number appears
anywhere, because none can be computed without a ground truth this project does not have.
Technical terms are explained where the meaning depends on them; "HOLD", "accepted",
"binding", "lineage group" and "production question" are each defined at first use in the
README and the contract. No unapproved decision is presented as fact: the retrieval contract
is marked PROPOSED and the four Controller decisions above are stated as open.

## CONFIRMATION

No unapproved next strategic step was started. No model or provider was called, no media was
generated, no money was spent, no source was ingested, no HOLD candidate was admitted, the
Audit Gate was not altered, no EVAL-037 artifact or branch was modified, no Capability
Registry row was created, and no Production IR or Planner work was begun. The pull request
is opened as a draft and is not merged.
