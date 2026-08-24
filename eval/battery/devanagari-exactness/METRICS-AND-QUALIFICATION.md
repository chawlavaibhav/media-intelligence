# Metrics and proposed qualification rule

**Status: PROPOSED. Nothing has been run; no checker is qualified, ranked or entered anywhere.**

---

## The metric that decides everything

**False pass** — the checker says the image matches the target when the visible text differs.

This is the only failure that reaches a customer *with a passing grade attached*. A false fail
costs a regeneration. A false pass ships a broken asset and tells us it is fine. The two are not
symmetric and must never be averaged into one "accuracy" number.

We have watched this happen: one checker reported `सुबह की पहली चाय — exact match` for six frames
that visibly read `सुवह`. The battery exists to catch that before it is trusted, not after.

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
- **checker shape** — transcribe vs verdict.

A single pooled number would let a checker that is blind to one whole aspect of the script — say,
every vowel-sign error — look fine because it handled the letter errors.

---

## What the current battery can and cannot support

With **53 mismatch items**, observing zero false passes gives a 95% upper bound of **5.5%** on the
true rate. But the headline is not the number that matters:

| Stratum | n | 95% upper bound if zero false passes |
|---|---:|---:|
| All mismatches | 53 | **5.5%** |
| **Hard stratum** (plausible + `corrupt_image`) | **35** | **8.2%** |
| Per failure class | ~2.6 mean | **not estimable at all** |

**Per-class rates must not be reported as rates.** With two or three items in a class, a single
miss moves the "rate" by 30–50 points. Per-class results are **diagnostic signals** — "this checker
missed both conjunct items, look closer" — never measurements.

### The concrete ask this produces

The hard stratum is the one that matters, and at n=35 its bound is weak. Reaching **≤5% on the hard
stratum** requires **59 hard items**, which at the current 70% direction split and 15% implausible
cap means roughly **85–90 validated base words** instead of 53.

That is the single highest-value input to this battery, and it is cheap: see
`NATIVE-VALIDATION.md`. It is a word-list validation, not another transcription exercise.

---

## Proposed qualification rule

Three gates. All three must pass. **Passing means "admitted for further evaluation at a stated
bound" — never "accurate".**

### Gate 1 — false passes on the hard stratum · **disqualifying**
**Zero false passes on plausible `corrupt_image` mismatches.**

No tolerance. This is the production failure reproduced exactly: malformed text, plausible target,
and the checker waved it through. One occurrence at this sample size means the checker does
autocorrect, and a checker that autocorrects cannot be a gate no matter how good its other numbers.

### Gate 2 — overall false-pass bound
**Zero false passes across all mismatch items**, reported with its 95% upper bound (5.5% at n=53).

### Gate 3 — usability
- **False-fail rate ≤ 10%** on clean controls — a checker that rejects correct text is unusable in
  a different way.
- **Repeat consistency ≥ 0.95** on the leading checker across ≥3 passes.
- **Refusal rate ≤ 5%**, reported separately.

### Recorded with any result, without exception

> Passing this battery means the checker **did not autocorrect any of N constructed mismatches**
> at a 95% upper bound of X%. It does **not** mean the checker is accurate, and it says **nothing**
> about malformed generated glyphs, which this battery cannot produce.

---

## What a failure tells us

A failure is more informative than a pass, and should not be treated as a dead end:

| Pattern | Reading |
|---|---|
| False passes concentrated in one group | the checker is blind to one feature of the script — actionable, possibly fixable by prompt |
| False passes only in `corrupt_image` | classic autocorrection: it reads toward the plausible word |
| False passes in both directions | it is not comparing against the target at all |
| High false-fail, low false-pass | over-strict; usable as a gate, expensive in regenerations |
| Shape 2 much worse than shape 1 | a prompt-design finding, not a model verdict — showing the target invites the error |

---

## Cost of a first run

**Estimated, not quoted.** Based on ~₹0.90 per check recorded in FINDINGS-01, which is an old
figure and **must be re-verified against live pricing before any run**. No roster is selected here;
model choice is a Controller decision.

| Configuration | Calls | ≈ ₹ | ≈ $ |
|---|---:|---:|---:|
| 3 checkers × 106 items, 1 pass | 318 | 286 | 3.25 |
| 3 checkers, 3 repeats on the leader | 530 | 477 | 5.42 |
| 5 checkers, 3 repeats on the leader | 742 | 668 | 7.59 |

Running **both checker shapes** doubles these. The realistic first run is therefore of the order of
**₹500–1,500 / $6–17** — small enough that cost is not the binding constraint. **Human validation
of the base word list is the real gate**, and it is measured in tens of minutes.

Also recorded, per the project's cost discipline: the evaluation cost above excludes the human
time, which dominates as usual.
