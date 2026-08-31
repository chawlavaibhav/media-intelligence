# EVAL-037 — Controller Conclusion

**Date:** 2026-08-31  
**Status:** CONCLUDED FOR PROGRAMME DIRECTION  
**Media generation:** not part of this conclusion  
**Registry effect:** none

## Question

Does exposing a reasoning model to Canon improve the quality of an outcome-oriented media production package, and what did the experiment reveal about how Canon is currently consumed?

## Original design

EVAL-037 froze:

- 6 customer briefs;
- 4 reasoning models;
- 2 conditions (NO_CANON / FULL_CANON);
- 3 independent repetitions per brief;
- intended total: 144 reasoning trials.

The full 144-trial matrix did not complete symmetrically. Some lanes failed or were skipped, and supplemental controlled-retrieval treatments were added as separate evidence rather than retroactively replacing original lanes.

The conclusion below therefore does **not** claim a clean eight-cell average treatment effect over the original frozen matrix.

## Evidence actually available

Primary fully populated judging set:

- Haiku NO_CANON
- Haiku FULL_CANON
- Sonnet NO_CANON
- Sonnet CONTROLLED_CANON (supplemental)
- Gemma NO_CANON
- Gemma FULL_CANON

Each contributed three repetitions for each of the six briefs.

Supplemental diagnostic evidence also included:

- repaired Sonnet unbounded FULL_CANON survivors;
- Gemma mandatory-unbounded Canon;
- Gemma controlled mandatory Canon.

Judging was blind to model/treatment identity and was performed independently in four streams over the production packages only.

## Accepted programme conclusion

> **Canon helps, but the current retrieval / consumption system is not mature.**

This is accepted as a programme-direction conclusion, not as a universal quantified benchmark claim.

The blind judgments repeatedly placed Sonnet NO_CANON and Sonnet CONTROLLED_CANON at the top of the surviving field, with CONTROLLED_CANON leading or co-leading important briefs, especially RentOK (B01) and the watch hero (B06), while remaining competitive on the others.

Across the six briefs the leading treatment-level picture was:

| Brief | Current leading treatment-level signal |
|---|---|
| B01 RentOK video | Sonnet CONTROLLED_CANON |
| B02 aight image | Sonnet NO_CANON / CONTROLLED_CANON effectively tied |
| B03 mosambi image | Sonnet NO_CANON slight lead |
| B04 skincare video | Sonnet NO_CANON lead |
| B05 café video | Sonnet NO_CANON / CONTROLLED_CANON effectively tied |
| B06 watch image | Sonnet CONTROLLED_CANON |

This supports the bounded product thesis that relevant explicit Canon can improve production reasoning enough to win real brief-grounded comparisons.

It does **not** support the stronger claim that Canon always improves every task, model, or repetition.

## Retrieval / consumption findings

The retrieval mechanism is the unresolved part.

### Optional Canon can be under-used

- Gemma FULL_CANON used Canon 0/18 times.
- Haiku FULL_CANON used Canon only sparsely.

Simply exposing tools does not ensure useful Canon consumption.

### Unbounded Canon can be destructive

The repaired unbounded Sonnet FULL_CANON run completed only 2/18 trials; 16/18 context-overflowed.

The mandatory-unbounded Gemma treatment searched without an effective bound and exposed roughly 1.13M tokens from one search path against a much smaller provider quota, producing 18/18 technical failures.

This is not evidence against Canon knowledge. It is evidence against the current unbounded retrieval interface.

### Controlled retrieval is much more executable

The Sonnet CONTROLLED_CANON treatment completed 18/18 trials with zero context overflows.

Observed retrieval:
- 53 Canon searches;
- mean 2.94 searches/trial;
- median 3 searches/trial;
- only 1 Canon read in the whole lane.

The model saturated search but nearly ignored object reads.

### The current search/read interface is not the final product interface

Gemma controlled Canon produced targeted production-question searches but usually did not perform the required follow-up read.

Together, the Sonnet and Gemma controlled lanes show that:
- objective-driven bounded search is much healthier than free unbounded retrieval;
- the present search -> read interaction is not reliably consumed as intended;
- ranked search envelopes are often treated as sufficient;
- retrieval policy and information packaging need a separate product-design pass.

## What is now closed

For this tranche, stop asking:

> Does Canon have enough value to justify continuing?

Programme answer: **yes**.

Do not launch another broad model × Canon-value experiment merely to reconfirm that point.

## What remains open

The next Canon question is different:

> What production retrieval / consumption mechanism gives a reasoning model the smallest, most relevant, highest-value Canon context for the customer's outcome?

That question is deliberately **not** answered here.

No new retrieval experiment is authorised by this conclusion.

## Boundaries

This conclusion:

- does not populate the Capability Registry;
- does not establish current media-model capability;
- does not claim Canon retrieval is production-ready;
- does not claim a statistically balanced 8 × 3 result for every brief;
- does not merge HOLD material into accepted Canon;
- does not authorise media generation or spend;
- does not create Production IR or the Production Planner.

## Programme effect

T2B's central programme question is treated as answered enough for direction:

**Canon is worth carrying forward. Retrieval is not mature.**

The programme should now zoom back out to the outcome-oriented product path and decide the shortest route from today's evidence to a working end-to-end system that improves accepted outcomes and CpAO.
