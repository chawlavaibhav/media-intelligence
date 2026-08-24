# Proposed Integration Change — CANON-001

**Filed by:** Canon · **Date:** 24 Aug 2026 · **Severity:** CROSS_STREAM
**Affects:** Eval / Capability Lab
**Status:** **APPROVED by Controller, 24 Aug 2026** (CANON-001 review, decision 5)
**Source evidence:** `canon/findings/CANON-001-current-schema-extraction-findings.md` §4;
`canon/knowledge/current/molly-bang/operational-bindings.yaml` → `bnd_mb_c001_0010`

Filed because the Runbook requires a worker tagging `CROSS_STREAM` to also file this file.
Canon proposes; it does not act on another stream.

## Controller decision — 24 Aug 2026

> Bang's visual minimal-pair candidates may be passed to Eval's deferred creative-evaluation list,
> clearly marked as source-asserted expected readings rather than validated human ground truth.

**Mandatory marking.** Any use of these four pairs must carry, alongside the pair itself:
`expected reading: source-asserted by Molly Bang; NOT validated human ground truth`.
The two isolation confounds recorded below travel with the pairs and must not be dropped.

Approval covers passing the candidates to Eval's **deferred** creative-evaluation list. It does not
place them in Capability Battery V0, does not create a benchmark dimension, and does not make the
expected readings evidence of anything about a model.

---

## OBSERVATION

Molly Bang builds four near-minimal pairs — two pictures differing in roughly one variable, each
with a stated expected viewer reading. That is the shape a benchmark item needs.

| Pair | Variable changed | Author's stated expected reading |
|---|---|---|
| p55 / p57 | same red triangle, upper vs lower half | upper reads freer and happier; lower reads heavier and more grounded |
| p63 / p65 | same burst, centred vs displaced | centred traps the eye; displaced releases it and reads as more dynamic |
| p70 / p71 | same black-on-white landform, pointed vs curved | pointed reads as threatening; curved reads as secure |
| p75 / p77 | same shape set, one colour vs two | one colour groups by shape; two colours group by colour |

## EVIDENCE

OBSERVED — all four pairs were inspected as rendered page images during CANON-001. Files exist at
`canon/sources/figures/`. The expected readings are quoted from the source text.

OBSERVED — two pairs are **not** strictly isolated, and this is recorded in the binding:
- p63/p65 also changes edge contact (the displaced version runs off the left edge) and introduces a
  second dark focus. Three variables move, not one.
- p75/p77 does not hold shape positions constant between the two sets.

NOT VERIFIED — the expected readings are the author's own judgements. No measured viewer response
exists for any of the four. They are candidate expected answers, not ground truth.

## PROPOSED CHANGE

Record these four pairs as **candidate items for the deferred creative-fitness register**, not for
Capability Battery V0.

EVAL-001's Controller clarification §2 places creative-judgement evaluation outside V0 and asks the
worker to document which creative dimensions are intentionally deferred, so that absence is not read
as irrelevance. This material belongs in that deferred list. Canon is not proposing it for V0 and is
not proposing any change to V0 scope.

Concretely: EVAL may cite `bnd_mb_c001_0010` when recording deferred creative dimensions, carrying
the two isolation confounds and the not-verified status with it.

## EXISTING DECISION AFFECTED

None reopened. Project Contract separation 5 (book knowledge ≠ empirical model capability) holds:
these pairs are stimulus material with a hypothesised answer, not a capability claim. Nothing here
asserts what any model can do.

## EXPECTED BENEFIT

Two of the four pairs are usable as-is for instrument calibration, because they have a known
expected answer that does not depend on a model's output — useful for asking whether an evaluator
can detect a difference a human reliably sees.

## RISK

The main risk is the expected readings hardening into ground truth through reuse. A pair with a
plausible stated answer is easy to treat as validated. If EVAL adopts any of these, the author's
judgement must stay labelled as an unvalidated hypothesis until human response data exists.

Secondary risk: the two confounded pairs could be used as controlled comparisons by a reader who
does not open the binding. The confounds are recorded in `bnd_mb_c001_0010.applicability.limits`.

## FALSIFIER

Show the pairs to human viewers. If responses do not follow the stated readings at better than
chance, the pairs are not usable as benchmark items and this proposal fails.

## WHAT CANON IS NOT CLAIMING

- Not claiming any current model can or cannot produce or judge these differences.
- Not proposing a new benchmark dimension. New benchmark dimensions are Controller-only.
- Not proposing a change to EVAL-001's approved scope.
