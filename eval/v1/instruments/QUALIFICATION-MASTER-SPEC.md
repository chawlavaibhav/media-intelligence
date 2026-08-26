# E3 — Evaluator qualification: master specification

**Task:** E3 · **Date:** 26 Aug 2026 · **Branch:** `work/eval-v1-overnight`
**Status: SPECIFICATION ONLY. NO INSTRUMENT IS QUALIFIED BY THIS DOCUMENT.**
**0 checker calls · 0 model calls · ₹0 spend**

---

## Why this document exists

An **instrument** (we also say *checker* or *evaluator*) is whatever decides
whether a generated asset passed — a text-recognition system, a geometry
calculation, a vision model, a listening test, a human reviewer.

**A capability number without its instrument is not a weak measurement. It is
not a measurement at all.** This is the founding result of the Eval stream and
it was paid for with real evidence: fourteen images of Hindi text were given to
three checkers. One vision model returned fourteen correct verdicts. Another
returned **six false passes** — it looked at visibly misspelled signs and called
them correct. Same images. Same question. Opposite answers.

A **false pass** is the error that costs money, because the defect ships *with a
passing grade attached*. Nobody looks again at work the checker approved.

So before any instrument's output may be written into the Capability Registry,
that instrument must have passed a qualification protocol for the specific
judgement it is being asked to make.

**Today, zero of six families are qualified.** That is not a gap in this
document — it is the current true state of the project, and this document is
what makes closing it possible.

---

## The general rule

> A model or workflow score may name an instrument **only when that exact
> instrument configuration holds a qualification record for the relevant
> judgement family and the relevant conditions.**

Three words in that sentence do real work:

- **exact configuration** — a version change, a prompt change or a threshold
  change makes a different instrument. It must be re-qualified.
- **relevant judgement family** — qualifying at reading Hindi says nothing about
  detecting broken hands. Families do not lend each other credibility.
- **relevant conditions** — qualification on clean studio renders does not
  transfer to degraded real-world material.

And its consequence:

> **`required_but_no_calibrated_instrument` is a valid Registry state.**

This matters more than it looks. It means "this property genuinely matters and
we currently *cannot* measure it." Without that state, a dimension with no
instrument silently vanishes from the battery and, six months later, reads as
*"we decided this didn't matter."* Two of our dimensions are in that state today
by prior finding — brand-mark fidelity and human-object contact — and eighteen
more join them because no family is qualified yet.

---

## Six rules that apply to every family

### 1 · Do not port one family's thresholds to another for tidiness

A zero-false-pass gate is right for exact text, where there is a correct answer
and a wrong answer. It is meaningless for "does this ad convey its
proposition", where there is no correct answer at all. Uniformity across
families would be a presentation choice masquerading as rigour. Each family
below carries its own gate, with its own justification.

### 2 · Gate accuracy and diagnosis accuracy are two numbers, stored apart

- **Gate** accuracy — does it correctly say pass or fail? *Routing needs this.*
- **Diagnosis** accuracy — does it correctly say **what** broke? *Repair needs this.*

The same prior finding that recorded a checker at fourteen-out-of-fourteen on
**verdicts** also records it catching one misspelling and **silently correcting
another**. Its gate was perfect; its diagnosis was incomplete. Never cite a bare
"14/14" as general accuracy.

### 3 · Screening rank is not qualification

| Stage | What it may produce |
|---|---|
| **Screening** — one pass, any number of candidates | A ranking or shortlist. **No status of any kind.** |
| **Qualification** — ≥3 full repeats, all shapes, per checker | A qualification for **that** checker on **that** battery |

A checker that only completed screening is recorded **"screened, not
qualified"**. It may not be described as passing, may not enter the Registry,
and may not be cited as an instrument whose numbers are trusted. **Stability is
a property of the instrument and is never inherited** from whichever candidate
happened to lead the screen.

### 4 · The gate is deterministic; any probability figure is a sizing calculation

Where a family has a right answer, its gate is a **count**, not a rate: zero
false passes. That needs no probability model and no independence assumption.

Any Clopper-Pearson or binomial figure quoted alongside it is a **reference
calculation for sizing the battery**, must be named as such in its own field
(`iid_reference_upper_bound_…`), and must carry
`independence_status: NOT ESTABLISHED`.

**It is never a checker's real-world error rate.** Two separate lessons sit
behind that, and the project got each wrong in turn:

- A bound computed over **correlated items** is not a bound. Four perturbations
  of one word are one opportunity, not four. *Count opportunities, not items.*
- **De-correlating items does not make them independent.** One item per word
  removes obvious within-word correlation; it does not create independent,
  identically distributed trials. A checker blind to a particular nasal mark is
  blind to it on every word carrying one.

And a third, easily confused with the second: **execution isolation is not
statistical independence.** Running items so no response can see another
prevents *context leakage*. It says nothing about whether the checker's errors
are correlated across those items.

### 5 · Blindness is verified mechanically, and *before* the run

Where an instrument must not see the answer, the payload is checked by code
before any call is made — an allow-list that **fails closed**, plus a sweep for
any character from the forbidden script.

**A leak cannot be detected afterwards from the responses.** By then the
experiment is simply gone. Both prior packs did this and both must continue to.

### 6 · Test the instrument with deliberately broken inputs

Negative-control fixtures immediately exposed three real defects in our own
harness — including a run that raised integrity errors and still exited
successfully, and a negative check that passed on "some error was raised
somewhere" and so would have passed even when one fixture was silently accepted.

**None was visible from reading the code.** Every family's qualification pack
below therefore includes deliberately-broken cases, and **an empty check must
fail, not report success.**

---

## What a qualification record must contain

Schema: [`qualification-result-schema.yaml`](qualification-result-schema.yaml).
Dummy examples: [`dummy-qualification-records.yaml`](dummy-qualification-records.yaml)
— clearly synthetic, and about instruments, never about generators.

Every record carries: instrument id **and version**; exact configuration hash
(prompt, thresholds, parameters); the judgement family; the conditions
qualified under; the pack and its version; gate results **and** diagnosis
results separately; repeat count and repeat consistency; refusal rate; and a
final status from exactly:

`qualified` · `provisional` · `screened_not_qualified` · `disqualified` · `unmeasurable`

`unmeasurable` means the protocol could not be run at all — the material or the
human reference does not exist. It is an honest outcome, not a failure.

---

## The six families, and what stands between each and qualification

| # | Family | Judges | Material we hold | Gate type |
|---|---|---|---|---|
| 1 | [Text / OCR](FAMILY-1-TEXT-OCR.md) | Is the rendered string exactly right? | **96-item Devanagari battery, frozen** | Zero false passes |
| 2 | [Deterministic CV / geometry](FAMILY-2-DETERMINISTIC-CV.md) | Counts, positions, file properties | **100 synthetic fixtures, built tonight** | Exact agreement |
| 3 | [Structured visual VLM](FAMILY-3-VISUAL-VLM.md) | Identity, anatomy, attributes, marks | None | Two-sided, human-adjudicated |
| 4 | [Temporal / video](FAMILY-4-TEMPORAL-VIDEO.md) | Drift, continuity, motion over time | None | Known-perturbation recall |
| 5 | [Speech / audio / AV](FAMILY-5-SPEECH-AUDIO.md) | Words, sync, turns, delivery | None | Split: deterministic + human |
| 6 | [Creative / commercial](FAMILY-6-CREATIVE-COMMERCIAL.md) | Does the ad work? | None | Agreement + false-criticism |

**Family 1 is the only family with a finished, human-validated qualification
pack.** Family 2's pack was constructed in this session. Families 3–6 are
specified but blocked on material that does not exist yet — see
[`RESOURCE-REQUESTS.yaml`](RESOURCE-REQUESTS.yaml).

---

## The cheapest ordering of the work

From the E1 dependency matrix, qualifying **one** family unblocks every
capability in its row at once:

| Qualify this family | Capabilities unblocked |
|---|---:|
| Structured visual VLM | **6** |
| Temporal / video | **5** |
| Speech / audio / AV | **2** |
| Text / OCR | **1** (but it is the product's headline risk, and its pack already exists) |

Two of these need **no new human labelling at all**, because their truth can be
constructed: family 2 by generating fixtures with known geometry, and family 4
by injecting known perturbations — a known freeze, a known identity swap, a
known horizontal flip — into clean clips. That is the same trick that made the
Devanagari battery cheap, and it is the reason those two should go first among
the unbuilt packs.
