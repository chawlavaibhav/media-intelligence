# CANON-009 — 30-brief bank coverage audit (C9-D)

**Task:** CANON-009 / C9-D · **Date:** 26 Aug 2026
**Measurement:** `30-bank-grammar-measurement.json`, computed by `audit_30_bank.py`
**The bank was NOT edited.** This is a rebalance proposal only.

---

## 0. What is measured and what is judged

The bank's own distribution is **computed** from `briefs-source.yaml` — not eyeballed. What that
distribution *should* be is **judged**, because for most components no external frequency evidence
exists (see `SOURCE-LANDSCAPE.md` §6).

So: the numbers are facts about the bank. The four lists are argued positions.

## 1. Measured coverage against the proposed grammar

| Grammar component | In the 30-bank | External evidence |
|---|---|---|
| G01 generate from nothing | **30 / 30** (23 with a supplied reference) | Attested |
| **G01 edit a supplied asset** | **0 / 30** | **Strongest in the register — 82,976 real requests** |
| **G01 animate a supplied asset** | **0 / 30** | **1.70M+ real requests** |
| G02 static / video | 12 / 18 | Distinct populations attested |
| G03 people present | 19 / 30 (63%) | Strong — humans dominate two corpora |
| G03 product is hero | 13 / 30 | **No corpus reports product frequency** |
| G04 supplied reference | 30 / 30 (100%) | Attested |
| G06 identity continuity | 10 / 30 (33%) | Strong for editing; inferred for sequences |
| **G07 exact text** | **28 / 30 (93%)** | **No real-user frequency exists** |
| G09 duration specified | 18 / 30 | **No corpus records requested duration** |
| G10 speech | 12 / 30 (40%) | **No corpus covers speech at all** |
| **G12 output is a set** | **0 / 30** | Qualitative ("creative versioning") |
| **G12 multi-turn** | **0 / 30** | 95K real multi-turn sequences |
| G13 under/over-specification | 9 underspecified, 8 contradictory | PSR's creativity level is a coarse analogue |
| G14 objective present | **30 / 30** | **Absent from every public corpus** |

## 2. The four lists

### List 1 — well represented

| Component | Why it holds up |
|---|---|
| **Objective, audience, acceptance** | 30/30. **The bank's single greatest strength**, and the thing no public corpus has. Every prompt corpus is silent on why anyone wanted the image. Our bank is the only artefact in this analysis that knows. |
| **Human subjects** | 63% of briefs, against the best-attested subject finding in the register. |
| **Under- and over-specification** | 9 underspecified + 8 contradictory. PSR's creativity-level dimension shows real requests vary exactly this way, over 82,976 cases. Independent corroboration of a design choice we made for our own reasons. |
| **Supplied references** | 100%, with roles distinguished — and SPEC-01 distinguishes reference roles more finely than any corpus found. |
| **Language mixing** | 10/10/10 English / Devanagari / Hinglish. No external corpus covers this at all, but it is a hard first-product requirement and the bank is the only place it exists. |

### List 2 — present but underrepresented

| Component | Now | Why more |
|---|---|---|
| **Identity continuity** | 10 / 30 | Preservation is the best-evidenced requirement in the request space. Our coverage sits entirely inside *generated sequences*; the far larger real population is *preserving a supplied asset*. |
| **Motion typing** | 18 video briefs, motion mostly implicit | TIP-I2V shows users name specific motions, and camera / locomotion / micro-expression are three different production problems. Our briefs rarely separate them. |
| **Product as subject** | 13 / 30 hero | Not underrepresented against evidence — no evidence exists. Underrepresented against *our own product scope*, which is built for commercial product media. |

### List 3 — absent from the bank, supported by request evidence

**This list is the audit's main output.**

| Missing | Evidence | Consequence |
|---|---|---|
| **Edit an existing asset** | **PSR: 82,976 real requests, 2013–2025. RealEdit: 57K+. SEED part 2: 52K.** | The best-evidenced operation in the entire request space has **zero** representation. Everything we test assumes generation from nothing. |
| **Animate a supplied image** | **TIP-I2V: 1.70M+ real text+image requests.** | The most plausible production route for short commercial video — customer has a packshot, wants motion — is untested. |
| **Multi-turn refinement** | **SEED part 3: 95K sequences, up to 5 rounds.** | Real requests arrive as conversations. Every brief we hold is a single complete statement. This is a *format* limitation, not a content one. |
| **Variant sets / campaign families** | Qualitative: "creative versioning" recurs in practitioner reports. | A request yielding twelve variants has entirely different economics from one yielding a single asset — and *Cost per Accepted Outcome* is the product's primary metric. We cannot currently express it. |

### List 4 — present in the bank, weak or no external support

**Recorded honestly. None of these is necessarily wrong.**

| Present | Support | Verdict |
|---|---|---|
| **Exact text, 28/30 (93%)** | Benchmark family exists and cites advertising; **no real-user frequency anywhere** | **Keep, relabel.** Commercial creative genuinely carries copy, and Devanagari exactness is a real product risk Eval already targets. But 93% is a *scope assumption*, not an evidence-backed weighting, and we should stop implying otherwise. |
| **Speech, 12/30 (40%)** | **None. No corpus covers audio.** | **Keep, relabel as scope-derived.** Follows from the first-product scope; carries no external validation. |
| **Duration and beat structure** | **None. No corpus records requested duration.** | **Keep.** Product constraint, not a discovered pattern. |
| **Contradictory briefs, 8/30** | PSR creativity level is a loose analogue; nothing measures contradiction rates | **Keep.** Deliberately constructed as probes for a specific failure mode, and defensible as such. |

## 3. The shape of the problem, in one comparison

| | Best-evidenced operations | Heaviest bank coverage |
|---|---|---|
| Edit supplied asset | **82,976 + 57K + 52K real requests** | **0 briefs** |
| Animate supplied asset | **1.70M+ real requests** | **0 briefs** |
| Multi-turn | **95K sequences** | **0 briefs** |
| Exact text | **no frequency evidence** | **28 briefs** |
| Speech | **no evidence at all** | **12 briefs** |

**The two things the world most demonstrably asks for, we do not test. The two things we test most
heavily, the world has not been shown to ask for.**

That inversion is the finding. It is not a failure of the bank — the bank was built from the
first-product scope months before this research existed, and it does something no corpus does. But it
does mean the bank is a **narrow probe of a wide space**, and its narrowness was invisible until the
space was mapped.

## 4. Rebalance proposal — not an edit

**Nothing in `briefs-source.yaml` was changed.** Four options for the Controller, cheapest first.

### Option A — Relabel only (₹0, no new briefs)

Record in the bank README which components are **evidence-backed** and which are **scope-derived**.
Nothing moves; the claims get honest.

**This should happen regardless of the other options.** It costs nothing and removes an
over-claim that would otherwise propagate into Eval's benchmark design.

### Option B — Extend to a 40-brief bank (recommended)

Keep all 30 unchanged. Add ten, covering the List-3 absences:

- 4 × edit-a-supplied-asset (remove / replace / background change / restore-and-update)
- 3 × animate-a-supplied-image (product hero, person, packshot-to-motion)
- 2 × variant set (one creative, several markets or placements)
- 1 × multi-turn (a request arriving in three rounds)

**Why extend rather than rebalance:** the 30 are already the frozen input to a value-gate package,
and swapping briefs would invalidate the early-12 selection, the oracle contexts and the length
matching. Extension costs nothing already built.

**Note the caveat:** the ten new briefs would still be *authored*, not observed. Extension improves
*coverage of the discovered space*; it does not turn the bank into demand evidence. Nothing can.

### Option C — Rebalance the 30 in place

**Not recommended.** It would invalidate the value-gate package for no gain that Option B does not
deliver.

### Option D — Do nothing until the value gate runs

Defensible. The bank's purpose right now is testing whether explicit Canon improves planning, and it
can do that job while narrow. The risk is that Eval samples its twelve end-to-end production briefs
from a bank containing zero edit and zero animate requests, and the resulting capability map inherits
the blind spot.

**Recommendation: A now, B before Eval samples the bank.**

## 5. What this audit does not claim

- **It does not claim the bank is wrong.** It claims the bank is narrow, and names how.
- **It does not propose rebalancing toward corpus frequency.** Those corpora are recreational-dominant;
  importing their distribution would be a worse error than the current narrowness.
- **It does not treat the 30 briefs as evidence about demand.** They never were, and the runbook is
  explicit that they are probes.
- **It changed no file in the brief bank.**
