# Metrics and proposed qualification rule

**Status: PROPOSED, revised after Controller review.**
**No checker/model/API qualification run and no human validation have occurred.** Only deterministic
local construction, rendering and test verification have been run. No checker is qualified, ranked or
entered anywhere. Every threshold below is a proposal, not an approved standard.

---

## The metric that decides everything

**False pass** — the checker says the image matches the target when the visible text differs.

This is the only failure that reaches a customer *with a passing grade attached*. A false fail
costs a regeneration. A false pass ships a broken asset and tells us it is fine. The two are not
symmetric and must never be averaged into one "accuracy" number.

We have watched this happen: one checker reported `सुबह की पहली चाय — exact match` for six frames
that visibly read `सुवह`. The battery exists to catch that before a checker is trusted, not after.

| Metric | Definition | Role |
|---|---|---|
| **False-pass rate** | false passes ÷ mismatch items | **primary** |
| False-fail rate | false fails ÷ match items | secondary; a checker that rejects correct text is also unusable |
| Refusal rate | refusals ÷ all items | reported separately, never counted as either verdict |
| Repeat consistency | identical verdict across repeats ÷ items | a gate must be stable per item, not merely on average |
| Transcription accuracy | exact + character edit distance (shape 1 only) | diagnosis for repair; never affects the gate |

### Always reported split by

- **direction** — `corrupt_image` (hard) vs `corrupt_target` (control);
- **plausibility** — plausible vs visibly-broken cluster;
- **failure group** — vowel signs, letters, conjuncts, dots/marks, र-forms;
- **checker shape** — transcribe (blind) vs verdict (target visible).

A single pooled number would let a checker that is blind to one whole aspect of the script — say,
every vowel-sign error — look fine because it handled the letter errors.

---

## The opportunity model — what may and may not be counted

This section was wrong in the first draft and was corrected twice. Both corrections matter, and the
second is subtler than the first.

### Correction 1 — one mismatch item per base word

The earlier build allowed **up to four mismatch items from the same base word** and then computed a
binomial zero-failure upper bound over the resulting item count. Four deterministic perturbations of
one word are plainly not four separate chances to catch a checker out: a model that reads `सुबह`
toward the plausible word will do it for every perturbation of `सुबह`. Counting them separately made
the sample look larger than the evidence was.

> **Every mismatch item now sits on a distinct base word.**

So `hard items == distinct hard base words`, by construction, and the test suite asserts it. Class
coverage was not sacrificed to achieve it: the allocation is solved deterministically — a maximum
bipartite matching between failure classes and base words, so scarce classes claim a word before
common ones can crowd them out. All **20 failure classes across all 5 groups** remain represented at
53 base words.

### Correction 2 — distinct words do not make the opportunities iid

Distinct base words remove the most obvious *within-word* correlation. **They do not establish
independent, identically distributed Bernoulli trials, and this battery does not claim they do.**

A checker's errors may remain correlated across words, across diacritics, across failure classes and
across lexical patterns — a model blind to anusvara is blind to it on every word carrying one. Our
53 words also come from a single dataset lineage. Nothing here demonstrates exchangeability, and
one-item-per-word does not create it.

Two consequences, and they are the shape of the whole section:

| | |
|---|---|
| **The qualification gate is deterministic** | *Zero false passes.* It needs no probability model at all, and it is what a checker is actually judged on. |
| **The Clopper-Pearson figure is a reference calculation** | It sizes the battery and states how little a clean sweep would prove. It is **not** an inference about a checker. |

The machine-readable fields carry the assumption in their names, so a value lifted out of
`build-summary.json` cannot be mistaken for a demonstrated bound:

```
iid_reference_upper_bound_if_zero_false_passes_95pct
iid_reference_upper_bound_all_mismatches_95pct
hard_opportunities_for_5pct_iid_reference
validated_base_words_planning_target_for_5pct_iid_reference
independence_status: "NOT ESTABLISHED. …"
```

### Both counts are always reported

| | Value at the current 53-word pool |
|---|---:|
| Mismatch items | 53 |
| **Distinct mismatch base words** | **53** |
| Hard items (plausible ∧ `corrupt_image`) | 37 |
| **Distinct hard base-word opportunities** | **37** |

### The reference calculation, stated correctly

> **Under an iid / exchangeable Bernoulli opportunity model, zero false passes in 37 hard
> opportunities corresponds to a one-sided 95% reference upper bound of ~7.8%.**

Every clause of that sentence is load-bearing:

- **"Under an iid model"** — EVAL-005 does **not** establish iid or exchangeability. The model is
  assumed for the calculation, not demonstrated by the battery.
- **"reference upper bound"** — a sizing figure, not a measurement and not an inference.
- **"~7.8%"** — this is **not** a universal checker error bound and **not** an estimate of any
  checker's real-world error rate.

What may honestly be said after a clean run: *"zero false passes across 37 distinct hard base-word
opportunities; under an iid Bernoulli reference model that corresponds to a 95% upper bound of
7.8%, which this battery does not establish as a real-world rate."*

What may **not** be said: *"the checker's error rate is below 7.8%."*

The all-mismatch figure at n=53 is **5.5%** under the same assumption. It is reported as wider
coverage, not as separate evidence: the 37 hard opportunities are inside it.

### Per-class figures are not rates

At roughly 2.6 items per class, one miss moves a "rate" by 30–50 points. Per-class results are
**diagnostic signals** — *"this checker missed both conjunct items, look closer"* — never
measurements.

---

## The battery-size planning target

Bringing the **reference calculation** below 5% needs **59 zero-failure opportunities**. Because
every mismatch sits on its own base word and the hard direction takes 70% of the mismatch stratum,
that converts directly into a word-list planning target:

| Validated base words | Hard opportunities | iid reference upper bound, zero false passes |
|---:|---:|---:|
| 53 *(today)* | 37 | 7.8% |
| 80 | 56 | 5.2% |
| **84** | **59** | **4.95%** |
| 85 | 59 | 4.95% |
| 90 | 63 | 4.6% |

**Recomputed after the corrected selection logic, the earlier "~85–90 words" recommendation
survives.** 84 is the arithmetic minimum, 85 is what the builder derives (`ceil(59 / 0.7)`), and 90
buys margin against words being rejected during validation.

⚠ **This is a planning target for the reference calculation, not proof of anything.** Reaching 84–90
words would make the iid reference figure fall below 5%. It would **not** demonstrate that a checker
errs on fewer than 5% of real cases, because the independence assumption behind that figure is still
not established and the words are still not a probability sample of future generated Hindi. More
words tighten a calculation; they do not supply an assumption.

### The pool cannot currently supply it

Merged repository-local material yields **53** distinct Hindi lexical items. Resources' merged
records establish that **3,924 single-word crops are transcription-resolvable** across IndicSTR12
and IIIT-ILST — but that is metadata about which labels *exist*; the raw lexical strings live in the
git-ignored Resources corpus, and how many *distinct* Hindi words they yield is unknown. Nor would
they be validated words: every candidate still has to pass the Hindi lexical validation.

The request is in `eval/tasks/EVAL-005-RESOURCES-REQUEST.md`, and its first step is a check of
existing local material rather than any new acquisition.

## Proposed qualification rule

**Passing means the checker satisfied the deterministic qualification gates below, on this
battery.** The associated iid reference calculation is reported separately, under its stated
modelling assumption, and is never part of what "passing" means. It certainly does not mean
"accurate".

### Rule 1 — false passes · **disqualifying**

> **Zero false passes on every mismatch item.**

There is one rule, not two, because the two strata are not independent: the hard stratum is a
subset of all mismatches, so "zero across all" already contains "zero on the hard subset".
Presenting them as separate statistical gates would double-count one piece of evidence. They are
distinguished by **what a failure in each one means**, and by **which one the iid reference figure is quoted on**:

| Stratum | n | Role |
|---|---:|---|
| **Hard** — plausible corruption, `corrupt_image` | 37 | **The primary disqualifying subset, and the only one a reference figure is quoted on.** This is the production failure reproduced exactly: malformed text, plausible target, checker waves it through. One occurrence at this sample size means the checker autocorrects, and a checker that autocorrects cannot be a gate however good its other numbers are. |
| **Control** — `corrupt_target`, plus any visibly-broken cluster | 16 | An **additional coverage condition** on strictly easier material. A false pass here is not evidence about autocorrection; it means the checker is not comparing against the target at all. Also disqualifying, but for a different and more basic reason. |

The all-mismatch reference figure at n=53 is **5.5%** under the same iid assumption. It is reported
as **wider coverage, not as a separate result**: it contains the 37 hard opportunities, so it cannot
be cited alongside the 7.8% as though the two were independent evidence.

### Rule 2 — usability

- **False-fail rate ≤ 10%** on the 53 clean match items — a checker that rejects correct text is
  unusable in a different way, and expensive in regenerations.
- **Refusal rate ≤ 5%**, reported separately and never folded into either verdict.

### Rule 3 — stability · **applies to every checker that receives a status**

- **Repeat consistency ≥ 0.95** across **≥ 3 full passes of the whole battery, in both shapes.**

This wording is deliberately stricter than the previous draft, which said repeats are run on "the
leading checker". That left open the reading that a checker could inherit a qualification from
someone else's stability. It cannot.

| Stage | What it may produce |
|---|---|
| **Screening pass** — one pass, any number of candidates | a ranking, a shortlist, a decision about which checkers are worth repeating. **No qualification status of any kind.** |
| **Qualification pass** — ≥3 full repeats, both shapes, per checker | a qualification on this battery's deterministic gates, for **that** checker only. The iid reference figure is reported alongside it, not as part of it |

A checker that completed only the screening pass is recorded as **"screened, not qualified"**. It
may not be described as passing, may not be entered in the Capability Registry, and may not be
cited as an instrument whose numbers are trusted.

**Thresholds are proposed, not approved.** 0.95, 10% and 5% are judgement calls with no empirical
backing in this repository. They need Controller approval before a run, and they should be revisited
once we have seen what real checkers do.

---

## Recorded with any result, without exception

> Passing this battery means the checker **did not autocorrect any of N distinct hard base-word
> opportunities** on this battery's material.
>
> Under an iid / exchangeable Bernoulli opportunity model — which **EVAL-005 does not establish** —
> that corresponds to a 95% reference upper bound of X%. That figure is a sizing calculation, not a
> measurement: it is **not** a universal checker error bound and **not** an estimate of the
> checker's real-world error rate. Errors may remain correlated across words, diacritics, failure
> classes and lexical patterns.
>
> It does **not** mean the checker is accurate, and it says **nothing** about malformed generated
> glyphs, which this battery cannot produce.

---

## What a failure tells us

A failure is more informative than a pass, and should not be treated as a dead end:

| Pattern | Reading |
|---|---|
| False passes concentrated in one group | the checker is blind to one feature of the script — actionable, possibly fixable by prompt |
| False passes only in `corrupt_image` | classic autocorrection: it reads toward the plausible word |
| False passes in both directions | it is not comparing against the target at all |
| High false-fail, low false-pass | over-strict; usable as a gate, expensive in regenerations |
| Shape 2 (target visible) much worse than shape 1 (blind) | a prompt-design finding, not a model verdict — showing the target invites the error |

---

## Cost of a first run

**Estimated, not quoted.** Based on ~₹0.90 per check recorded in FINDINGS-01, which is an old
figure and **must be re-verified against live pricing before any run**. No roster is selected here;
model choice is a Controller decision.

| Configuration | Calls | ≈ ₹ | ≈ $ |
|---|---:|---:|---:|
| 3 checkers × 106 items, screening pass | 318 | 286 | 3.25 |
| 3 checkers screened, 3 repeats on 1 qualifying checker | 636 | 572 | 6.50 |
| 5 checkers screened, 3 repeats on 2 qualifying checkers | 1,166 | 1,049 | 11.92 |

Running **both checker shapes** doubles these. The realistic first run is therefore of the order of
**₹600–2,100 / $7–24** — small enough that cost is not the binding constraint. Note this is higher
than the previous draft estimated, because repeats now attach to every checker that is given a
status rather than to one leader.

**Human validation of the base word list remains the real gate**, and it is measured in tens of
minutes. Per the project's cost discipline: the figures above exclude human time, which dominates
as usual.
