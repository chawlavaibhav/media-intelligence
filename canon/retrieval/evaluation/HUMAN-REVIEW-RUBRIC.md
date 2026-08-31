# Human review rubric — is the retrieved Canon actually the right Canon?

**Why this exists.** The offline evaluation measures size, purity, spread, redundancy and
reproducibility. It cannot measure whether the knowledge selected is the knowledge the job
needed. Nothing in this repository labels a Canon object as relevant to a brief, and
inventing such labels to produce a precision score would be manufacturing a ground truth —
exactly what `shared/COMMUNICATION-STANDARD.md` §5 forbids. So relevance is judged by a
person, on the record, or it is not claimed at all.

**Time required.** About 15 minutes per brief; about 90 minutes for all six.

**What to review.** Six committed bundles, one per EVAL-037 brief, exactly as a reasoning
model would receive them:

```
canon/retrieval/evaluation/bundles/B01-canon-context.json   RentOK vertical video ad
canon/retrieval/evaluation/bundles/B02-canon-context.json   aight festive poster
canon/retrieval/evaluation/bundles/B03-canon-context.json   mosambi sparkling drink image
canon/retrieval/evaluation/bundles/B04-canon-context.json   skincare UGC video
canon/retrieval/evaluation/bundles/B05-canon-context.json   café dialogue scene
canon/retrieval/evaluation/bundles/B06-canon-context.json   watch e-commerce hero image
```

The brief text is in `EVAL-SET-v0.1.yaml` under `briefs`. A readable view of any bundle:

```bash
python3 -m canon.retrieval.cli --request "<paste the brief text>"
```

---

## Part A — per item

For each item in the bundle, record one verdict and, where it is not `useful`, one line
saying why. **Do not score. Do not average.** These are categories, not a scale.

| Verdict | Meaning |
|---|---|
| `useful` | A person writing this production package would be better off having read it. |
| `true_but_not_for_this_job` | Sound knowledge, wrong job. The commonest expected failure — for example a film-editing claim retrieved for a still image. |
| `too_general` | Correct but so broad it changes nothing about this brief. |
| `misleading_as_presented` | **The serious one.** The item as packaged could lead a reader to a wrong decision — a hedged claim reading as a rule, an unreviewed proposal reading as settled, a caveat that has lost the fact that it was ours rather than the author's. |
| `cannot_judge` | You do not have the background to say. A legitimate answer; do not guess. |

A `misleading_as_presented` verdict is a defect in this package, not a preference. Note the
item id and what specifically misleads.

## Part B — per bundle

1. **Missing knowledge.** Name anything you expected and did not find. Then check whether
   it exists in accepted Canon at all: `python3 -m canon.retrieval.cli --request "<the
   missing topic>"`. A gap in the corpus and a gap in retrieval need different fixes and
   must not be recorded as the same finding.
2. **The questions.** Read `plan.questions`. Are these the right things to have asked about
   this brief? Is anything important missing from the catalogue, rather than merely absent
   from this plan?
3. **Domain fit.** Read `spread.source_stated_domains` — what the selected sources say they
   are about. Does the mix make sense for this medium? This is the known limitation the
   README names first, and your judgement here decides whether it needs fixing.
4. **Enough or too much.** Would you cut anything? Is anything so thin it should have been
   dropped rather than included?
5. **The one-call question.** Having read the bundle, would you have needed to go and read a
   full source object? The bundle claims 96% of items across the six briefs arrive whole
   and that a second call is normally unnecessary. Say whether that matches your experience.

## Part C — the comparison that matters most

Open one EVAL-037 trial for the same brief in
`EVAL-SET-v0.1.yaml → sonnet_controlled_trials`. Look at `returned_objects` for its three
searches: 24 objects, roughly half of them HOLD material the project has not admitted.

Then answer one question:

> **Would you rather hand a competent freelancer this bundle, or those 24 objects?**

If the answer is not clearly "this bundle", the design has not earned its place, whatever
the size numbers say.

---

## Recording a review

Write it to `canon/retrieval/evaluation/reviews/<brief-id>-<reviewer>-<date>.md`, with:

- reviewer, date, and the bundle's `corpus.corpus_fingerprint.combined_digest` (a review is
  only valid for the corpus it was done against);
- the Part A table: item id, kind, source, verdict, note;
- Part B answers;
- the Part C answer, with reasoning;
- an explicit **"the retriever should change how it..."** list, if any.

## How results may and may not be reported

**May:** "N of M items were judged useful by one reviewer on six briefs." Counts, with the
reviewer named and the sample size stated.

**May not:** a precision or recall figure, an accuracy percentage, a claim that retrieval
is production-ready, or any statement that Canon retrieval improves accepted outcomes. A
small single-reviewer judgement is directional evidence about the retriever. It is not a
benchmark, and outcome effect needs a controlled model experiment that CANON-015 neither
ran nor is authorised to run.
