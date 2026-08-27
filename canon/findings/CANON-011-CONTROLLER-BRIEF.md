# Controller Brief — CANON-011

**TASK:** CANON-011 — Marketplace-derived benchmark brief & prompt-ready bank
**STATUS:** completed
**AUTHORITY:** `coordination/decisions/CONTROLLER-MARKETPLACE-DERIVED-BRIEF-PREP-2026-08-27.md`
**SPEND:** USD 0 · **EXTERNAL CALLS:** 0 · **MODEL / EVALUATOR CALLS:** 0 · **REGISTRY ROWS:** 0

**Communication check:** I will explain technical ideas in plain English, including what they mean,
why they matter, and their practical consequence; use minimum sufficient wording without
sacrificing understandability; separate evidence from inference; and never invent facts. I have
read `shared/COMMUNICATION-STANDARD.md`.

---

## HUMAN SUMMARY

You asked for real customer jobs to test against, instead of jobs we made up. I turned eighteen
Upwork postings — real people paying real money for video — into benchmark cases, and kept a
record of exactly which parts of each one the buyer actually said and which parts we supplied to
make the test repeatable.

**The most useful thing they show is a gap in our own bank.** Our thirty authored briefs put
"these exact words must appear in the picture" into **28 of 30**. Across eighteen real paid jobs,
**one** asks for it. That does not mean our bank is wrong — it was built as a probe and never
claimed to be demand evidence — but it is the first time anyone paying for this work has told us
that the requirement we test hardest is not the one they buy. It is worth knowing before we spend
money benchmarking against it.

**Two other things surprised me.** First, real buyers almost never say what would make them reject
the work: **one of eighteen** states a rejection criterion. Our authored bank's defining strength
is that every brief carries acceptance criteria — real briefs mostly do not, which means a live
system will have to derive or ask for what our bank always hands it. Second, **the request format
we froze last week cannot hold four things these buyers actually said.** The sharpest one: when a
buyer supplies footage that must *appear* in the finished video, our format has no way to record
it. The only available workaround is to call it a "reference", and a reference is something a
system may legitimately depart from — so a hard requirement would silently become a soft one, and
an output that dropped the footage entirely could pass.

**On Hindi.** The honest answer is uncomfortable and worth stating plainly. Of 114 postings,
**exactly one buyer pays for an Indic language as part of producing a video** — Hindi and Urdu
narration for a safety film — and one more wants Hinglish content made. Both are among the only
two cases we cannot run, because we hold no audio material at all. Everything else Hindi on this
platform is voice-over, dubbing, translation or data work. That is a fact about Upwork, not about
India: the research says directly that Indian brands buying Hindi ad production are not on this
channel. I did **not** manufacture Hindi cases to fill the gap, and I rejected the one posting
that would have made it easy to — a $500 Hindi/Hinglish job whose deliverable is a *script*, not a
video.

**Nothing here is authorised, spent or frozen.** Sixteen of the eighteen cases can be run without
going back to the buyer, but **none of them can be scored**, because no evaluator in this project
has ever been qualified. Those are two different gates and the bank keeps them apart.

---

## WHAT I DID

Read the five governance documents, the task authority, all three marketplace source files, the
frozen Media Request Grammar and the Capability Contract, then worked one posting at a time: took
the buyer's stated facts as exact quotes, wrote a minimal customer brief from those facts only,
filled all eighteen request-grammar fields with a provenance label on each, and marked every field
the buyer did not address as `absent` rather than filling it. Where the benchmark had to supply
something for a case to be repeatable — a script, a product, an aspect ratio, a language — it is
labelled `experiment_supplied_fixture` and listed separately. I then wrote a validator with
fourteen gates and **broke the bank twenty-eight different ways to prove each gate actually fires**,
because this project has already paid for the lesson that a validator tested only on correct input
proves nothing.

---

## OBSERVED

All figures computed by `measure_coverage.py` into `coverage-measurement.json`.

- **114 postings recorded** in the research; **67** classified by it as addressable, **47** not.
  I recounted all three from the appendix table rather than trusting the prose; they agree.
- **18 cases built**, drawing on **19 source rows**. **16 runnable now**; 2 not.
- **Requested operations:** generate 14, edit 2, animate 1, variants 1.
- **Modality:** 18 of 18 video, 0 static.
- **Language:** only **2 of 18** buyers state a language, and both are the Indic cases. The English
  in the other twelve is a benchmark fixture, labelled as one.
- **Provenance labels across the bank:** 138 `absent`, 125 `customer_stated`, 63
  `customer_implied`, 62 `experiment_supplied_fixture`, 47 `system_derived`.
- **Exact text in the picture: 1 of 18.** In the authored 30-brief bank: **28 of 30**.
- **Buyer states a rejection criterion: 1 of 18.**
- **Text requirements (`R08`): `absent` in all 18.** **Acceptance intent (`R18`):
  `customer_stated` in all 18.**
- **Identity requirements in 13 of 18** cases; product identity 7, person/character 3, voice 5.
- **Deliverable sets larger than one in 10 of 18;** 3 need per-item acceptance *with* a set-level
  invariant.
- **Evaluator dependencies:** creative 15, visual 12, temporal 12, speech 11, deterministic 11,
  operational 6, OCR 1. **All unqualified.** 11 dependencies are hard-blocked for want of material.
- **Attemptable without a Production Planner:** 10 yes, 4 partial, 4 no.
- **Validators:** `validate_marketplace_bank.py` **PASS**, all 14 gates.
  `test_negative_fixtures.py` **PASS**, 28/28 negative controls rejected on the correct gate, and
  the unmodified bank still passes — so a validator that simply rejected everything could not have
  scored this.
- **Protected artifacts:** 57 files across the 30-brief bank, the coverage extension, Capability
  Contract v1 and v2, the 100-item Eval bank, the Registry and the marketplace sources are
  **byte-identical to `origin/main`**, verified by comparing git blob hashes.
- **Registry:** `eval/registry/registry-v1.jsonl` holds 6 comment lines and **0 rows**. Unchanged.

---

## INFERRED

- **The generate-heavy split is a sampling artefact, not a finding.** All eleven research queries
  were AI-video-creator queries, so postings framed as generation were selected for at search
  time. Same for 18-of-18 video and 0 static. I say this explicitly in the coverage report rather
  than letting the distribution read as demand evidence.
- **The exact-text observation is real but narrow.** It is direct evidence that a set of
  eighteen fully specified paid commercial video jobs mostly do not require exact text. It is
  **not** the missing frequency figure CANON-009 looked for and could not find anywhere, and I do
  not present it as one.
- **Character or product consistency across a series is the expensive requirement.** The research
  says so from the seller side; the cases say so from the buyer side — it is the primary
  acceptance condition in three cases and present in five, and it is also where our request format
  breaks.

---

## SURPRISES / BELIEF UPDATES

1. **Real briefs are much thinner than authored ones.** More than a third of all grammar slots
   across the bank record that the buyer said nothing. Our authored briefs always supply an
   objective, an audience and acceptance criteria. Real ones often supply a duration, a platform
   and a price, and nothing else. **A future session should not take this bank's `absent` count as
   sloppiness — it is the finding.**
2. **The frozen request grammar has four representational gaps**, each attested by a paying buyer
   rather than by a design review. See below.
3. **Four ordinary, cheaply-priced jobs are beyond us today** — ten 3-minute videos, 48 lecture
   videos, a 20-minute safety induction, and the 300-second end of a scripted batch. Not because
   they are hard creatively, but because they need a production plan and Production IR does not
   exist. That is the clearest price the project has yet paid for that absence.
4. **The one case with a real unit price is the best Stage-C candidate we have.** Knox Deco pays
   "$30–45 per approved video" with up to two revisions inside that price. That is Cost per
   Accepted Outcome, written by a buyer, against a rate we did not invent.

---

## FAILURES / BLOCKERS

- **Two cases could not be completed and are marked so.** MKT-015 needs verified Hindi and Urdu
  speech material we do not hold, and its 15–20 minute duration cannot be shortened without a
  scope decision that is yours. MKT-016 could only be made runnable by inventing the source
  material, the change, the length and the content — which would be authoring a brief and calling
  it marketplace evidence. It is kept in the bank with its generation brief marked *NOT
  SPECIFIABLE FROM THE SOURCE*, as a worked example of where the evidence stops.
- **No case can be scored.** Zero evaluator families are qualified project-wide.
- **The posting bodies were never captured**, only the researcher's summaries of them. Several
  fields labelled as fixtures here would become customer-stated if the original text were read
  again. This is recorded per case.

---

## UNKNOWN / NOT VERIFIED

- Whether the Knox Deco buyer (MKT-002) supplies source footage. It decides whether that job is
  `generate`, `edit` or `compose`, and it changes the acceptance contract materially. Recorded as
  an ambiguity marker, not resolved.
- What the Fiverr rupee-to-dollar rate actually is. The cleaned report says ₹100 = $1; the raw
  capture says ₹100 = $1.14 — a 14% gap on every Fiverr dollar figure. Recorded in
  `SOURCE-DISCREPANCIES.md`, not reconciled. Nothing in the bank depends on a Fiverr price.
- Three further cleaned-vs-raw Fiverr disagreements, all recorded, none load-bearing.

---

## ASSUMPTIONS CHALLENGED

None in `coordination/ASSUMPTIONS.md` is directly falsified. The exact-text observation weakens
the implicit working assumption that the authored bank's requirement mix resembles what customers
ask for — an assumption CANON-009 already flagged and which the Controller already answered by
freezing the 30 as a probe rather than a specification. This is the first buyer-side evidence for
the same point.

---

## LOCAL IMPLICATIONS

Canon now holds a second, independently-sourced request bank alongside the authored one, with
mechanically checked provenance on every field. It is a candidate Stage-C pool and a source of
compound-scenario material. It replaces nothing.

---

## CROSS-STREAM IMPLICATIONS — tagged **CROSS_STREAM**, proposed, not acted on

**To the request contract (CANON-010 / Controller).** Four representational gaps, recorded in the
bank as `grammar_gaps` with no field, role or value invented:

| ID | Gap | Cases | Consequence if left |
|---|---|---|---|
| GG-01 | No asset role for **supplied material that must appear in the output** of a `generate` request | 3 | The only workaround is to call it a reference, which converts a hard requirement into a soft one; an output that omitted the footage could pass. |
| GG-02 | No asset role for a **document supplying the content the deliverable must convey** | 5 | The most frequently attested buyer input in this sample has nowhere to live in the request record. |
| GG-03 | `acceptance_basis` cannot express **per-deliverable acceptance with a set-level invariant** | 3 | This is the requirement that separates routine pipeline work from expensive custom work. If the record cannot hold it, the benchmark cannot test it. |
| GG-04 | `deliverable_set` has cardinality but no **ongoing rate** | 3 | A rate is a different economic object from a total, and it is the shape worth selling into. |

**To Eval.** Two capabilities real buyers need that Capability Contract v2 does not measure:
**CO-01**, fidelity of a deliverable to a supplied source document — not the same as comparing
speech to an exact string, and it is one buyer's entire acceptance test; and **CO-02**, sustained
throughput as an acceptance condition. Also **CO-03**, that cross-asset identity, deliberately
handled as an observation *scope* rather than as its own capability, turns out to be the primary
acceptance condition in three cases; and **CO-04**, that three buyers state an aesthetic
*prohibition*, which the creative family has no way to score.

**To Resources.** The Indic finding sharpens the acquisition question: the only marketplace-attested
Indic media-production job needs verified Hindi and Urdu **speech** material, and the project holds
no audio of any kind. Several cases also need person and product reference packs **with
same-category decoys** — without decoys a qualification cannot detect a permissive judge at all.

---

## ARCHITECTURAL IMPLICATIONS

None acted on. GG-01 to GG-04 touch a frozen contract and are routed, not implemented — the Canon
charter's stop condition for "a source appears to require a field that does not exist" was hit
four times and observed four times.

---

## DECISIONS NEEDED FROM CONTROLLER

1. **Merge or reject the branch.** Not my decision and not proposed either way.
2. **Whether to act on GG-01 to GG-04.** Doing nothing is defensible — the sentinel label keeps the
   information visible. But GG-01 has a specific failure mode: if a supplied asset that must appear
   is recorded as a reference, an output that omits it can score as a pass.
3. **Whether MKT-015's stated 15–20 minute duration may be scoped down** for benchmark use.
   Shrinking a customer's stated request is a scope decision, so I left it blocked rather than
   quietly running a shorter version.
4. **Whether MKT-013 and MKT-015 belong in the bank at all.** Both come from postings the research
   classified as *not* addressable by an AI video pipeline, and I disagreed. Both disagreements are
   recorded on the cases. MKT-013 is the single cheapest thing in the bank to actually measure.

---

## EVIDENCE WORTH HUMAN INSPECTION

- **`derived/COVERAGE-REPORT.md` §4 and §10** — the exact-text and rejection-criteria numbers, and
  what they do and do not mean.
- **`derived/marketplace-brief-bank-v1.yaml`, case MKT-001, field `R15_delivery`** — the clearest
  example of the discipline. The buyer named the platform and nothing about format. A proposal
  draft elsewhere in the same research document offers a 9:16 cut — but that is the *researcher
  pitching*, not the buyer asking, so the aspect ratio is recorded as a fixture. It would have been
  very easy to record it as customer intent.
- **`derived/marketplace-brief-bank-v1.yaml`, case MKT-016** — the case the bank refuses to
  complete, and why.
- **`derived/validators/test_negative_fixtures.py`** — 28 ways the bank was broken to prove the
  checks are real.

---

## FILES CREATED / MODIFIED

Created, all under `canon/research/marketplace-demand-v1/derived/`:
`marketplace-brief-bank-v1.yaml`, `marketplace-prompt-ready-bank-v1.yaml`, `COVERAGE-REPORT.md`,
`SOURCE-DISCREPANCIES.md`, `README.md`, `coverage-measurement.json`, `measure_coverage.py`,
`build_prompt_ready_bank.py`, `validators/validate_marketplace_bank.py`,
`validators/test_negative_fixtures.py`.

Created: this brief, `canon/findings/CANON-011-CONTROLLER-BRIEF.md`.

**Modified: nothing.** No existing file in the repository was changed.

---

## RECOMMENDED NEXT STEP

If you want the cheapest useful thing from this: **MKT-013**. It is an edit inside a supplied video
whose "everything else unchanged" ground truth is held exactly, because the benchmark authors the
base video itself. Its evaluator family is deterministic geometry — the cheapest to qualify — and
`edit` is an operation the 30 authored briefs never exercise. It could be measured sooner than
anything else here, and it needs no money.

For the highest-value one: **MKT-002**, because it is the only case carrying a buyer's own
per-approved-unit price, which is what makes a real Cost per Accepted Outcome computable.

---

## EPISTEMIC CHECK

Every buyer fact in the bank is an exact quoted substring of a committed source file, checked
mechanically by gate G9. Every request field carries a provenance label from a closed vocabulary,
checked by G2. Interpretations are labelled `customer_implied` with a stated rationale, or
`system_derived`; benchmark additions are labelled `experiment_supplied_fixture` and cross-checked
against declared fixtures by G8. Unknowns are recorded as `absent` or as ambiguity markers and are
not filled. No evaluator is described as qualified anywhere, checked by G12. No decision is
presented as approved, no budget is proposed, and no number in the coverage report is a
market-share claim.

## CONFIRMATION

No unapproved next strategic step was started. No model, provider or evaluator call was made. No
Registry row was written. No existing repository file was modified. The branch is pushed and not
merged.
