# ABORTED EXECUTION 001 — gemma-no-canon

**This is not the lane result. The lane result is `runs/gemma-no-canon/`.**

This directory holds the retained outputs of a first execution of this lane that was
killed part-way through by the *execution harness's* 10-minute command timeout, after
roughly 12 of 18 trials. It is preserved, not deleted, because EVAL-037 requires that
every output produced by a real provider call be retained.

What this abort was **not**:

- not a provider failure of any class, transient or deterministic;
- not a per-trial retry, and not licensed by the retry policy;
- not a creative-quality judgement — no output here was read, scored or compared, and
  nothing here was selected for or against.

Because the process was killed before it wrote `attempt-ledger.json` or `result.json`,
this run has no ledger, no result, no usage totals and no validated trial set. It
cannot be reported as a lane result and is not offered as one.

Recovery was a clean re-execution of all 18 trials from the top, under the identical
frozen runner, lane config and substrate — committed before the first call and
unchanged since. There is no best-of-N selection between this directory and the lane
result: the complete run is used in whole, and this partial one is used not at all.
