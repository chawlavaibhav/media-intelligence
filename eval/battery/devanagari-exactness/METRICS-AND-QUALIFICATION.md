# Metrics and proposed qualification rule

**Status: PROPOSED, revised after Controller review. Nothing has been run; no checker is
qualified, ranked or entered anywhere. Every threshold below is a proposal, not an approved
standard.**

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

This section was wrong in the previous draft and is the most important correction in this review.

The earlier build allowed **up to four mismatch items from the same base word** and then quoted a
binomial zero-failure upper bound over the resulting item count. That is not a defensible bound.
Four deterministic perturbations of one word are not four independent chances to catch a checker
out: a model that reads `सुबह` toward the plausible word will do it for every perturbation of
`सुबह`. Counting them as separate trials makes the sample look larger than the evidence is.

### The rule now, and it is structural rather than a caveat

> **Every mismatch item sits on a distinct base word.**

So `hard items == distinct hard base words`, by construction, and the test suite asserts it
(`test_hard_opportunities_use_distinct_base_words`). The bound is computed from the opportunity
count, and since the two numbers are equal there is no gap between what is quoted and what is
defensible.

Class coverage was not sacrificed to achieve this. The allocation is solved deterministically —
a maximum bipartite matching between failure classes and base words, so scarce classes claim a
word before common ones can crowd them out — rather than by relaxing the independence rule. All
**20 failure classes across all 5 groups** remain represented at 53 base words.

### Both numbers are always reported

| | Value at the current 53-word pool |
|---|---:|
| Mismatch items | 53 |
| **Distinct mismatch base words** | **53** |
| Hard items (plausible ∧ `corrupt_image`) | 37 |
| **Distinct hard base-word opportunities** | **37** |

### The bound, and what it is a bound on

Zero false passes across **37 distinct hard opportunities** gives a one-sided 95% upper bound of
**7.8%**.

In plain English: a checker that never waved through a single hard item could still, on this kind
of material, be wrong up to roughly **8 times in 100** and we would not have seen it. That is a
ceiling on our ignorance, not a measurement of accuracy.

*(The previous draft quoted 8.2% at n=35. The corrected construction gives slightly more
opportunities, 37, and a slightly tighter bound, 7.8% — but the earlier figure was computed over
items that were partly correlated, so it was not comparable in the first place.)*

### ⚠ The epistemic limit, which must travel with the number

This is a **binomial upper bound over the opportunities this battery constructs**, conditional on
its word list, its perturbation operators and its font. The words are 53 lexical items reused from
one dataset lineage; the operators are a taxonomy we wrote. Neither is a probability sample of the
Hindi a generator will be asked to draw next year.

**So this is not an estimate of any checker's universal true error rate.** It bounds what *this
battery* could have failed to detect. It is legitimate to say "no false pass in 37 distinct
opportunities, 95% upper bound 7.8% on this material". It is not legitimate to say "the checker's
true error rate is ≤5%", with or without a larger battery.

### Per-class figures are not rates

At roughly 2.6 items per class, one miss moves a "rate" by 30–50 points. Per-class results are
**diagnostic signals** — *"this checker missed both conjunct items, look closer"* — never
measurements.

---

## What it would take to reach a ≤5% bound

Reaching a 95% upper bound of **5% or better with zero failures requires 59 distinct
opportunities.** Because every mismatch sits on its own base word and the hard direction takes 70%
of the mismatch stratum, that converts directly into a word-list requirement:

| Validated base words | Hard opportunities | 95% upper bound if zero false passes |
|---:|---:|---:|
| 53 *(today)* | 37 | 7.8% |
| 80 | 56 | 5.2% |
| **84** | **59** | **4.95%** |
| 85 | 59 | 4.95% |
| 90 | 63 | 4.6% |

**Recomputed after the corrected selection logic, the earlier "~85–90 words" recommendation
survives.** It was not carried over: 84 words is the arithmetic minimum, 85 is what the builder
derives (`ceil(59 / 0.7)`), and 90 buys a little margin against words being rejected during
validation. The figure is now backed by an opportunity count that is genuinely one-per-word.

**This is the single highest-value input to the battery**, and it is cheap: a word-list validation,
not another transcription exercise. See `NATIVE-VALIDATION.md`.

⚠ **The current repository cannot supply 84–90 words.** Merged repository-local material yields
**53** distinct Hindi lexical items — the EVAL-003 candidate manifest. The only other committed
Devanagari of any volume is the annotator-disagreement file, whose strings are *specifically the
contested ones* (and partly Marathi), so it is the worst possible source of validated words.
Closing the gap needs roughly **31–37 additional Hindi lexical items** from Resources. The precise
request is in `eval/tasks/EVAL-005-RESOURCES-REQUEST.md`.

---

## Proposed qualification rule

**Passing means "admitted for further evaluation at a stated bound" — never "accurate".**

### Rule 1 — false passes · **disqualifying**

> **Zero false passes on every mismatch item.**

There is one rule, not two, because the two strata are not independent: the hard stratum is a
subset of all mismatches, so "zero across all" already contains "zero on the hard subset".
Presenting them as separate statistical gates would double-count one piece of evidence. They are
distinguished by **what a failure in each one means**, and by **which one carries the bound**:

| Stratum | n | Role |
|---|---:|---|
| **Hard** — plausible corruption, `corrupt_image` | 37 | **The primary disqualifying subset, and the only one a bound is quoted on.** This is the production failure reproduced exactly: malformed text, plausible target, checker waves it through. One occurrence at this sample size means the checker autocorrects, and a checker that autocorrects cannot be a gate however good its other numbers are. |
| **Control** — `corrupt_target`, plus any visibly-broken cluster | 16 | An **additional coverage condition** on strictly easier material. A false pass here is not evidence about autocorrection; it means the checker is not comparing against the target at all. Also disqualifying, but for a different and more basic reason. |

The all-mismatch upper bound at n=53 is **5.5%**. It is reported as a **wider-coverage figure, not
as an independent result**: it includes the 37 hard opportunities, so it cannot be cited alongside
the 7.8% as though the two were separate evidence.

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
| **Qualification pass** — ≥3 full repeats, both shapes, per checker | a qualification at a stated bound, for **that** checker only |

A checker that completed only the screening pass is recorded as **"screened, not qualified"**. It
may not be described as passing, may not be entered in the Capability Registry, and may not be
cited as an instrument whose numbers are trusted.

**Thresholds are proposed, not approved.** 0.95, 10% and 5% are judgement calls with no empirical
backing in this repository. They need Controller approval before a run, and they should be revisited
once we have seen what real checkers do.

---

## Recorded with any result, without exception

> Passing this battery means the checker **did not autocorrect any of N distinct hard
> opportunities**, at a 95% upper bound of X% **on this battery's material**. It does **not** mean
> the checker is accurate, it is **not** an estimate of a universal error rate, and it says
> **nothing** about malformed generated glyphs, which this battery cannot produce.

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
