# Controlled-pack requirements v2 — what must exist, and what is still provisional

**Task:** R4-E · **Date:** 26 Aug 2026 · **Machine-readable:** `CONTROLLED-PACK-REQUIREMENTS-v2.yaml`
**Validator:** `validators/check_pack_requirements.py` — **executed, exit 0**
**Controller basis:** integration decision §4.4 — four packs retained; **exact sizes not reauthorised**,
to be frozen against Capability Contract v2

---

## Four packs. No fifth.

The widened scope — composed multi-step outcomes, campaigns, longer video — creates **metadata,
grouping and composition requirements on material the four families were already going to acquire**.
It does not create a new *kind* of controlled material, so no fifth family is proposed. The validator
enforces this and would fail a fifth without a named active consumer.

| Pack | Named consumers | Provisional quantity |
|---|---:|---|
| `PACK-PRODUCT-REF` | 7 | 12 products × 4 views = **48 images** |
| `PACK-PERSON-REF` | 5 | 8 identities × 4 views × 2 framings = **64 images** |
| `PACK-AV-CLEAN` | 7 | **36 clips** (24 single + 12 two-speaker) |
| `PACK-COMMERCIAL` | 6 | **80 assets** (60 active + 20 reserve), ~10 campaign groups |

Every pack names the capability rows that consume it. A pack with no active consumer is speculative
and the validator rejects it.

## Exact vs provisional — and why the distinction is honest

**The Controller did not reauthorise pack sizes**; they will be frozen against Capability Contract v2.
So this document separates what follows from the architecture from what waits on EVAL-009.

**EXACT — these do not move when EVAL-009 lands:**

- product: **≥4 controlled views** per product — identity needs angles, colour needs a flat reference,
  logo-on-surface needs curvature;
- person: **≥4 views AND ≥2 framings** — drift between a close-up and a wide shot is a *different*
  failure from drift within one framing;
- AV: **≥6 single-speaker clips ≥20 s continuous**;
- AV: **8/8/8 and 4/4/4** language balance; **turn boundaries** on all two-speaker clips;
- commercial: **40 static / 40 video** and **60 active / 20 reserve**.

**PROVISIONAL — pending EVAL-009:** the entity counts (12 products, 8 identities, 36 clips, 80 assets)
and the ~10 campaign groups.

**No count claims statistical confidence.** These are coverage minima derived from named consumers,
not power calculations. The validator scans the whole document for confidence/significance language
and fails on it — a check that caught a phrase in my own first draft.

## The sizing rule

> **N = ceil( C × V × R )**
> **C** = distinct Capability Contract v2 rows consuming this pack and needing a controlled reference
> **V** = minimum distinct reference variants each needs to separate a real match from a plausible confusion
> **R** = protected-role multiplier: **1** for one role in one experiment, **2** if the same pack must
> supply both a calibration pool and a **disjoint** qualification pool

**`R` is the largest cost sensitivity in the entire acquisition plan.** If EVAL-009 requires one pack
to both calibrate and qualify an instrument, that pack roughly **doubles** — product goes to ~24
products / ~96 images, person to ~16 identities.

**Halving a contaminated pack does not decontaminate it.** The split must be disjoint at the
*lineage* level — product identity, person identity, speaker, campaign — not at file level. Two
photographs of one person are not two independent items.

**The Controller should decide `R` deliberately rather than discover it during acquisition.**

## The one evidence-driven requirement worth singling out

**≥6 AV clips at ≥20 seconds continuous** is marked EXACT because it rests on a measurement, not a
preference. The **entire existing corpus tops out at 20.00 seconds and holds nothing above 30 s**
(fresh recompute, RES-003 R3-B; 90% of video is ≤10 s and VideoFeedback's 987 clips are all exactly
3.00 s). If outcomes are 20-second branded videos, a VO pack of 5-second utterances cannot support
lip-sync or drift measurement over a real deliverable's length. The *shape* would be wrong, not just
the quantity.

## Reuse instead of a fifth pack

**The AV pack supplies its own perturbation base** — ≥12 of its clean clips — rather than acquiring a
separate temporal pack. A perturbation base needs clips whose only defect is the one introduced, and a
controlled recording satisfies that better than KoNViD-1k, which was sampled for degradation variety.

**Resources must enforce the consequence:** those reused clips **share content lineage** with their AV
originals and cannot be an independent holdout for any speech measurement that also uses the original.

## Protected roles, and the one-way freeze

Every pack declares calibration, qualification and holdout roles, with disjointness required at the
**lineage** level named per pack.

**The 20-asset commercial reserve is frozen at acquisition time**, before any evaluator or Canon work
touches the 60 active assets. Freezing is one-way: a reserve someone has already looked at is not a
reserve.

## Boundaries Resources holds

- **No creative labels.** Eval may later designate a ≥15-asset known-clean subset for false-criticism
  calibration; **Resources supplies candidates, rights and provenance and must not author that label** —
  "clean" is a creative-quality judgement.
- **No public-face scraping, absolute.** User-uploaded reference images from request corpora are **not
  assumed cleared** and must not be used as person references.
- **No thresholds.** Resources supplies clips and known offsets; tolerances are Eval's.
