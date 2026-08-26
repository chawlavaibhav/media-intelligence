# RES-004 — Production Evidence & Persistence Readiness — Controller Brief

**Task:** `resources/tasks/RES-004-PRODUCTION-EVIDENCE-AND-PERSISTENCE-READINESS.md` (R4-A … R4-G)
**Date:** 26 Aug 2026 · **Branch:** `work/res-004-production-readiness` · **Not merged**
**Session:** cloud-only — no laptop, no raw corpus, no provider credentials
**Spend:** **₹0 / $0.** No acquisition, no paid call, no login, no terms acceptance, no email.

**Verify everything:** `bash resources/pre-execution-freeze/validators/run_all_res004.sh`
→ **exit 0, ALL RES-004 CHECKS PASSED.**

---

## 1. The question this task exists to answer

> **What must exist before the first paid attempt can be persisted without schema debt or evidence
> leakage?**

**Answer: the persistence layer is ready. Acquisition is not, and it is blocked on human decisions,
not on engineering.**

Under v2.1 the first paid composed run could have been recorded, but three things would have been
irrecoverable afterwards: the outcome it belonged to, whether local assembly steps were real trials,
and what the accepted outcome actually cost. v3 closes all three, and **31 executed controls over 30 fixtures** hold them closed.

---

## 2. Topology v3 — result

**Implemented and enforced.** `job → outcome → sequence_or_asset_set → production_unit →
production_step → attempt → artifact`, with 10 entities and **11 mechanical gates**.

| Control set | Result |
|---|---|
| Valid v3 archive (exercises every feature) | **passes all 11 gates** |
| 17 gate-violation fixtures | **each rejected by its own declared gate** |
| | **18/18 as declared** |

The positive fixture is one accepted 3-shot branded video: **7 provider calls → 7 trials**, one step
holding **two** attempts (an error and its retry), a **refusal that cost money and produced nothing**,
**4 of 9 artifacts produced by local or human steps with no attempt and no trial**, an **ordered**
3-parent concatenation and an **unordered** audio/video mix.

**Everything you asked to preserve is preserved and mechanically checked:**

| Invariant | Gate |
|---|---|
| one provider/API/transform call = one trial | **G1** |
| attempt / artifact separation | **G6** |
| failed and refused attempts persist individually with reasons | **G10** |
| historical v2.1 evidence untouched | **G9** |
| request lineage separate from media/byte lineage | **G11** |

**The gate that mattered most is G2.** v2.1 had nowhere to put an artifact produced by a local ffmpeg
operation, so the structural temptation was to **fake a provider attempt for local work**. That would
have been silently catastrophic: a fabricated attempt is a fabricated **trial**, and trials are the
denominator of reliability, `pass_at_k` and every per-trial cost view. A pipeline with three local
composition steps per outcome would have inflated its trial count ~3× with nothing in the data to
reveal it. G2 closes it from both directions — the step side and the artifact side.

**Ordered multi-parent lineage** requires positions to be **unique and contiguous from 0** where order
carries meaning. A duplicate makes order ambiguous; a gap makes it unknowable. Both are separate
fixtures. A single-element parents list is **exactly** a v2.1 `derived_from_artifact_id`, so legacy
archives need no rewriting.

## 3. CpAO — result

**Both required views implemented, 13/13 controls as declared.**

Worked example (the valid fixture, one accepted composed outcome):

| | |
|---|---:|
| `api_tool` — 7 calls incl. 1 error + 1 refusal, plus 2 evaluator calls | 50.00 |
| `local_compute` — overlay (**shared, counted once**) + concat + mix | 1.50 |
| `human_required` — review | 20.00 |
| **API/tool CpAO** (diagnostic) | **50.00** |
| **FULLY-LOADED CpAO** (primary business metric) | **71.50** |

**Human time is 28% of fully-loaded cost in this illustration.** A system optimised on API/tool CpAO
alone would happily trade 20.00 of human review for 5.00 of API spend and report an improvement.

**No double counting, by construction.** Cost attaches to the **step or attempt that incurred it**,
never to the edge that consumed it. Provenance is a **DAG**, so the engine sums the **set** of distinct
ledger entries exactly once. In the fixture the overlay entry is referenced by two steps and the logo
artifact consumed by two composites; a naive walk would report **71.75** instead of 71.50.

**Revision journeys and the scope boundary — two fixtures, identical but for one flag:**

| Fixture | Charged | Fully-loaded |
|---|---|---:|
| `revision-journey-included` | rejected v1 **+** accepted v2 | **30.00** |
| `scope-change-cuts-journey` | accepted v2 only | **15.00** |

Excluding revisions by default would systematically understate the cost of briefs needing a second
pass — exactly the briefs that matter commercially. The `scope_change_boundary` flag stops earlier work
being charged forward when the **customer** materially changed the brief.

**Ten refusal conditions**, each with an executed control. The engine **refuses to emit a number rather
than emit a wrong one**, because a wrong CpAO gets quoted. Notably: **no accepted outcome ⇒ CpAO is
UNDEFINED**, not zero — reporting zero would make the worst possible run look free. An **unclassified
cost** is also a refusal: it cannot be placed in either view.

## 4. Pack requirements — exact vs provisional

**Four packs. No fifth.** The validator enforces it and would reject a fifth without a named active
consumer.

| Pack | Consumers | Provisional quantity |
|---|---:|---|
| `PACK-PRODUCT-REF` | 7 | 12 products × 4 views = **48 images** |
| `PACK-PERSON-REF` | 5 | 8 identities × 4 views × 2 framings = **64 images** |
| `PACK-AV-CLEAN` | 7 | **36 clips** (24 single + 12 two-speaker) |
| `PACK-COMMERCIAL` | 6 | **80 assets** (60 active + 20 reserve), ~10 campaign groups |

**EXACT — will not move when EVAL-009 lands:** ≥4 product views · ≥4 person views **and** ≥2 framings ·
**≥6 AV clips at ≥20 s continuous** · 8/8/8 and 4/4/4 language balance · turn boundaries on all
two-speaker clips · 40/40 static-video and 60/20 active-reserve splits.

**PROVISIONAL — pending EVAL-009:** all four entity counts and the ~10 campaign groups.

**Deterministic sizing rule SR-1: N = ceil(C × V × R)** — capabilities consuming the pack × reference
variants needed × protected-role multiplier.

> **`R` is the single largest cost lever in the plan.** If EVAL-009 requires one pack to both calibrate
> and qualify an instrument, that pack roughly **doubles** (product → ~24 products / ~96 images; person
> → ~16 identities). **Halving a contaminated pack does not decontaminate it** — the split must be
> disjoint at identity/speaker/campaign level, not file level. Decide `R` deliberately rather than
> discover it mid-acquisition.

**No count claims statistical confidence.** These are coverage minima from named consumers, not power
calculations. The validator scans for confidence/significance language and fails on it — a check that
caught a phrase in my own first draft.

**The one evidence-driven exact requirement:** ≥6 AV clips at ≥20 s rests on a measurement, not a
preference. The **entire existing corpus tops out at 20.00 s and holds nothing above 30 s**; 90% of its
video is ≤10 s. A VO pack of 5-second utterances cannot support lip-sync over a real deliverable.

## 5. Rights and acquisition blockers

**All four packs are blocked on human decisions. None was attempted.**

| # | Gate | Owner | Blocks |
|---|---|---|---|
| 1 | **CC-BY-NC as commercial empirical material — currently NO** absent explicit disposition | Controller / legal | ABO, HiACC, VidProM, TIP-I2V |
| 2 | **Consent instrument** — likeness **and** voice, retention, withdrawal; may need counsel | Controller / legal | person + AV packs |
| 3 | **Verify load-bearing licences on the actual distribution page** | human with unrestricted network | any public route |
| 4 | **Pitt Ads: send the email or close the route** | Controller | commercial pack |
| 5 | **Confirm UGC reference images stay disallowed** | Controller | person pack |

**ABO is out for the product pack.** RES-003 resolved its licence contradiction to **CC BY-NC 4.0**
with a named licence file users must accept. It was structurally ideal — 8,222 listings with 24/72-view
turntable sequences — and non-commercial rules it out under your posture.

**UGC reference images: Resources classifies these DISALLOWED, not unresolved.** TIP-I2V ships **1.70M+
user-supplied image prompts** of unstated provenance — possibly third-party copyright, possibly
identifiable people — and the publisher's own NSFW flagging indicates they expected problematic
uploads. It is the largest tempting shortcut in the plan.

**Evidence caveat:** this session's egress proxy blocks official distribution pages, so every external
rights fact is `search_supported`, never officially verified. Gate 3 exists for that reason.

## 6. Human-effort budget inputs

**173 person-hours of acquisition effort** under provisional counts and `R = 1`, in hours not currency —
Resources does not know rates and a made-up rate would fabricate a financial fact.

| Pack | Hours | Dominant item |
|---|---:|---|
| Product | 24 | sourcing 12 products across ≥6 categories |
| Person | 31 | recruitment (10 h) + consent instrument (6 h, **may need counsel**) |
| **AV** | **73** | **transcription 18 h + turn annotation 9 h** |
| Commercial | 45 | rights-holder outreach (20 h, **confidence: unknown**) |

**AV is the largest item and it is annotation-bound.** Turn boundaries with speaker attribution are the
annotation almost no public source ships, and they are what `REQ-CAP-26` actually measures.

**Separately — operational human effort feeds fully-loaded CpAO**, not acquisition: ~0.5 h per composed
video acceptance review, ~0.15 h per static, ~0.25 h per adjudication while instrument families remain
unqualified, ~0.3 h per repair decision.

## 7. Unresolved Controller decisions

| # | Decision | Consequence |
|---|---|---|
| **1** | **Which human time is "required" in fully-loaded CpAO?** (`HED-1`) | Changes what the primary business metric *means*. Schema records every class either way. |
| **2** | **Protected-role multiplier `R`** | Roughly doubles two packs if `R = 2`. Biggest cost lever in the plan. |
| **3** | **CC-BY-NC disposition** | Gates four candidate sources. Legal judgement. |
| **4** | **Consent instrument approval** | Gates the two hardest packs; may need counsel. |
| **5** | **Adopt topology v3 as the forward contract** | Until adopted, whole-outcome CpAO is not computable. |
| **6** | **Pitt Ads: email or close** | Only public route to a commercial creative bank. |
| **7** | **Confirm UGC images disallowed** | Resources' position is disallowed; confirmation makes it binding. |
| **8** | **Final pack counts against Capability Contract v2** | EVAL-009 supplies `C` and `V`; you supply `R`. |

## 8. Deliverables and verification

All under `resources/pre-execution-freeze/`:

| File | Package |
|---|---|
| `OUTCOME-PRODUCTION-TOPOLOGY-v3.yaml` | R4-A |
| `V21-V3-COMPATIBILITY.md` | R4-B |
| `LINEAGE-CONTRACT-v3.md` | R4-C |
| `CPAO-CONTRACT-v3.md` | R4-D |
| `CONTROLLED-PACK-REQUIREMENTS-v2.yaml` + `.md` | R4-E |
| `RIGHTS-ACQUISITION-PLAN.md` · `HUMAN-EFFORT-BUDGET-INPUTS.yaml` | R4-F |
| `RES-004-CONTROLLER-BRIEF.md` | R4-G |
| `validators/` (3 validators + 3 runners) · `fixtures/` (30 fixtures) | R4-C/D/E |

| Suite | Result |
|---|---|
| v3 topology + lineage | **18/18 as declared** |
| Whole-outcome CpAO v3 | **13/13 as declared** |
| Controlled-pack requirements | **exit 0** |
| Inherited v2.1 contract | **exit 0 — historical evidence preserved** |
| Inherited RES-003 suite | **exit 0** |

**30 fixtures yielding 31 control results** (18 lineage + 13 CpAO), of which **3 fixtures are
deliberately positive**. A validator that rejects everything would pass every negative control and be
useless, so each suite carries at least one archive that must validate cleanly.

## 9. Compliance

- **0** acquisitions, downloads, logins, accounts, forms, terms acceptances, payments, emails. **₹0 / $0.**
- **0** paid or free provider/evaluator API calls. **0** media files opened from the raw corpus.
- **0** creative labels. **0** Eval thresholds. **0** provider/model selection.
- **0** historical v2.1 records mutated, migrated or backfilled. **0** trial acceptances promoted to customer acceptance.
- **0** fifth pack families. **0** counts claiming unearned statistical precision.
- **0** files changed outside `resources/`. **Not merged.**
