# Family 3 — Structured visual VLM instruments

**Judges:** identity, attributes, anatomy, brand marks — perceptual questions with no deterministic oracle.
**Status: NOT QUALIFIED. Pack does not exist. Blocked on controlled reference material.**

**This family unblocks 6 capabilities — more than any other. It is the highest-value qualification in the programme.**

---

## The central difficulty

Every other family has, somewhere, a right answer we can compute. This one does
not. "Is this the same person?" has no pixel-level oracle. Identity similarity
is **not** exact equality, and any protocol that pretends otherwise will produce
a confident number that means nothing.

So this family's qualification is **two-sided** and requires human adjudication
to build its reference at all.

---

## Pack design — known-match, known-non-match, and the decoy

Built on the shared controlled reference packs (see `RESOURCE-REQUESTS.yaml`):
**≥48 product references** (12 products × ≥4 views) and **≥32 person references**
(8 identities × ≥4 views).

Three case types, and the third is the one that does the work:

| Case | Construction | Catches |
|---|---|---|
| **Known match** | Two views of the same entity | Over-strictness — an instrument that never says "same" |
| **Known non-match** | Two clearly different entities | Nothing much. This is the easy half. |
| **Same-category decoy** | Two *different* entities of the **same product category or similar person type** | **Permissiveness** — the failure that matters |

**Without the decoy, an instrument that answers "yes, that is a shampoo bottle"
scores as though it had verified identity.** The decoy is what separates
recognising a *category* from recognising an *individual*.

The same structure applies to preservation/edit cases: a source, an edit, and a
known out-of-region change that must be caught.

## Gate

Two-sided, because both error directions are real and they are not equally
dangerous:

- **False "same"** (says two different entities are the same) — the dangerous
  direction. Ships the wrong person or the wrong product with a passing grade.
  This carries the tighter bound.
- **False "different"** (says two views of one entity are different) — expensive
  in wasted regenerations, not dangerous.

⚠️ **No numeric thresholds are proposed here.** Setting a false-same rate before
seeing any data would encode a guess as a finding. The honest sequence is:
run the pack, plot the two error rates, **then** propose a gate with the
Controller. Compare the vision model against the human adjudication, not
against another vision model.

## Two accuracies, stored apart

- **Gate** — is this the same entity, yes or no? *Routing needs this.*
- **Diagnosis** — *what* differs: wardrobe, hair, label, proportion? *Repair needs this.*

An instrument may be trustworthy at the first and useless at the second. Never
report one number.

## Human adjudication is unavoidable here

Unlike families 1, 2 and 4, this pack's reference **cannot** be constructed
without people. Budget it explicitly and do not let it be discovered mid-run.

**Also unavoidable: `human_object_contact` and `logo_wordmark_fidelity` are
recorded in prior findings as `required_but_no_calibrated_instrument` and that
has not changed.** Template matching handles flat frontal marks and fails under
perspective and curvature — which is exactly where commercial work lives.

## Qualification inputs

| Need | State |
|---|---|
| Product references (≥48) | ❌ not held |
| Person references (≥32) | ❌ not held |
| Same-category decoys | ❌ not held — **must be requested explicitly**, they are not a by-product |
| Human adjudication time | ❌ not budgeted |
| Gate thresholds | ❌ deliberately not proposed before data |
| Frozen identity rubric | ✅ **exists** — V0 frozen, reuse unchanged |

**Reuse the frozen rubric, do not rewrite it.** It already encodes the essential
rule: each declared identity feature is judged on **two** questions — does it
match the reference, and is it consistent across the set — and **both must
hold**. A consistently-produced *wrong* person is a failure, not a pass.
It may not be edited during or after calibration; a case it cannot decide is
logged `not_reviewable` and raised as a V1.
