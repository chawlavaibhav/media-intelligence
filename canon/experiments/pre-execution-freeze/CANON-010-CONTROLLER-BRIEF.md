# CANON-010 — Controller Brief

**Task:** `canon/tasks/CANON-010-REQUEST-CONTRACT-AND-COVERAGE-FREEZE.md` (C10-A → C10-E)
**Date:** 26 Aug 2026 · **Branch:** `work/canon-010-request-freeze` · **Not merged**
**Spend: ₹0.** No paid call, no source ingestion, no model or provider selection, no Production IR.
**Stop conditions triggered: none.**

---

## 1. Status — all five work packages complete

| Package | Deliverable | Status |
|---|---|---|
| C10-A Media Request Grammar v1 | `MEDIA-REQUEST-GRAMMAR-v1.yaml` | Complete — 18 fields, 9 cross-field rules, 5 vocabularies |
| C10-B Normalized Request delta | `NORMALIZED-REQUEST-DELTA.md` §1–3 | Complete — 6 additions, all upstream of Creative IR |
| C10-C Multi-turn boundary | `NORMALIZED-REQUEST-DELTA.md` §4 | Complete — 3 constraints, no schema designed |
| C10-D Extension bank | `REQUEST-COVERAGE-EXTENSION.{jsonl,md}` | Complete — 11 items, 10 runnable |
| C10-E Combined coverage | `COMBINED-COVERAGE-REPORT.md` | Complete — 7/7 operations covered |
| Mechanical gates | `validate_request_freeze.py` | **PASSED**, all 7 gates, each proven to fire |

## 2. Major proposed freeze decisions

### D1 · `requested_operation` — seven values, customer intent only

**Proposed vocabulary:** `generate` · `edit` · `animate` · `restore` · `extend` · `compose` ·
`variants`. Placed on the **Normalized Request**, not Creative IR, because it is something the
customer *said*.

**Provenance is restricted to `user` or `derived` — never `system_decided`.** If the system decided
what operation the customer wanted, the system misread the request. There is no legitimate case.

**Production routes are forbidden values and the validator rejects them:** `inpaint`, `outpaint`,
`img2img`, `text2img`, `controlnet`, `lora`, `upscale`, `segment_and_composite`. Every one is a
technique. A customer asks to remove a person from a photo; inpainting is one way to do it.

**The rule that makes this worth freezing:**

> **A supplied asset does not imply `edit`.**
>
> *"Change the background of this photo"* → **edit**, the artefact is being altered.
> *"Here's our product shot — make a Diwali creative"* → **generate**, the photo is a reference.
>
> Both arrive with an image attached. They have **opposite preservation semantics.**

### D2 · `deliverable_set` — cardinality and acceptance basis

`cardinality`, `variation_axis`, `acceptance_basis` (`per_deliverable` / `set_level` /
`best_n_of_m`). Default when unstated: 1, none, per-deliverable, provenance `derived`.

**This is an economic field, not a formality.** The primary metric is Cost per Accepted Outcome, and
four independent acceptances is a different object from one joint acceptance. Extension items RX-09
and RX-10 are both `variants` and differ only in this — *"koi choose nahi karna"* (all four must be
good) versus *"take it or leave it as a whole"*.

Distinct from `delivery.aspect_ratios[]`, which is one artefact delivered several ways.

### D3 · `motion_intent` — camera and subject motion never merged

Two sub-objects, permanently separate. CANON-009's evidence: users ask for **"zoom"** (camera),
**"walk"** (locomotion), **"blink"** (micro-expression) — three production problems, three failure
modes. Extension items RX-05 and RX-06 exercise both directions.

One asymmetry: camera motion may be `system_decided` (silence delegates it); subject motion may not
(silence usually means no motion was requested).

### D4 · `subject_of_operation` — one new asset role

SPEC-01's existing roles all describe a reference that *informs* a new artefact. An edit or animate
request supplies the artefact the operation acts **on**. SPEC-01's own comment warns that conflating
asset meanings is the failure to avoid; this is such a case.

### D5 · `specification_provenance` — required, with evidence

Records `customer_specified` / `customer_omitted` / `derived`. **A field is `customer_specified` only
if the customer said it**, and any preserve-intent claiming customer provenance must carry an
`evidence_quote` present verbatim in the request text.

Assigning customer provenance to a system decision is how a bad plan later gets scored as a misread
request — it corrupts the one distinction the two-object architecture exists to protect.

### D6 · Extension bank of 11 — sized by coverage, asymmetric by language

Eleven items: edit 4, animate 2, variants 2, restore 1, extend 1, compose 1. English 5, Hindi 2,
Hinglish 4. **Every non-English item states a real language dependency** and the validator rejects a
translated duplicate.

**Result: 7 of 7 operations covered. Before the extension, 1 of 7.**

### D7 · The original 30 stay byte-identical

SHA-256 verified on both bank files; 30 briefs present. Gate G1 fails the build on any change.

## 3. Unresolved — Controller decisions required

| # | Decision | Notes |
|---|---|---|
| **U1** | **Freeze the seven-value `requested_operation` vocabulary** | Proposed with an extension rule: a new value requires that a request be unrepresentable by an existing value *plus* `mutation_intent` — not merely that a new technique exists |
| **U2** | **Does `restore` stay distinct, or fold into `edit`?** | Proposed **distinct**, on acceptance grounds: an edit is judged against the change requested; a restoration is judged against a plausible original nobody has. RX-04 makes it concrete |
| **U3** | **Multi-turn request history** | **Architecture decision, deliberately not made.** See §4 |
| **U4** | **Accept the 11-item extension, or adjust scope** | Two known non-additions are deliberate: speech (no corpus evidence) and ambiguity markers (would confound operation failures) |
| **U5** | **Is `best_n_of_m` needed in Wave 1?** | Vocabulary exists; no item uses it. RX-09/RX-10 cover the two bases that change cost most |
| **U6** | **Where does `deliverable_set` finally live?** | Proposed on the Normalized Request. CANON-009 flagged the placement as a genuine architecture question and it is still open |

### Cross-stream dependency

**EVAL-009 needs D1 and D3 before freezing its condition contract.** The Controller decision requires
requested operation and workflow mode to stay distinct in every empirical row. If EVAL-009 freezes a
condition contract with one field covering both, the distinction is lost at measurement time and no
amount of downstream care recovers it.

## 4. Multi-turn — flagged, not designed

**95,000 real multi-turn sequences** of up to five rounds exist in the evidence. The Controller
deferred it and it is **not designed here.**

The reason it must not be improvised:

> Round three of a conversation is not a new request. **It inherits everything unstated from rounds
> one and two.** Modelling each round as an independent Normalized Request loses the inheritance;
> modelling it as a mutation breaks the "preserved forever, never overwritten" rule.

Extension item **RX-11** carries this concretely: *"thoda zyada warm"* — more warm than **what**? Than
the round-1 output, which is not the supplied asset. Neither round is interpretable against the
original input alone.

The Canon charter's mandatory stop conditions cover exactly this: a request appearing to require an
IR field that does not exist is an **ARCHITECTURE** matter — stop, do not add the field yourself.

**Three constraints proposed instead** (the whole of C10-C — not a design, just keeping the door
open): the Normalized Request stays append-only and addressable; nothing assumes a request is
complete at first receipt; `specification_provenance` can later record inherited provenance.

**RX-11 is `representation_only` and gate G5 fails the build if it is ever marked runnable.**

## 5. Verification — every command run fresh

| Check | Result |
|---|---|
| `validate_request_freeze.py` | **PASSED** — all 7 gates, exit 0 |
| Gate negative controls (`tests/test_request_freeze_gates.py`) | **7/7 gates proven to fire**, exit 0 |
| Original 30-bank byte-identity | **PASS** — SHA-256 on both files, 30 briefs |
| `combined_coverage.py` | exit 0 — 41 items, 7/7 operations |
| Grammar fields with provenance + operation rules | 18/18 |
| Workflow or provider tokens anywhere in the bank | **none** |

**Two defects were caught during the build and both are worth recording**, because both would have
passed silently:

1. **The provenance check could not work across scripts.** The first version matched English
   keywords from an intent target against the request text — which never matches when the request is
   in Devanagari. It passed RX-02 and RX-04 *by failing to look*. Replaced with a mandatory verbatim
   `evidence_quote`. A provenance check that quietly fails on non-Latin scripts is worse than none.
2. **Prose in RX-02 named a production technique** while describing the customer's requirement. Gate
   G3 caught it. Minor in itself, and exactly the collapse this package exists to prevent.

## 6. Boundaries honoured

- **Original 30 briefs byte-identical** — SHA-256 verified, gate-enforced.
- **No market-share claim anywhere.** Structural coverage only. The 30:11 ratio is build-order, not
  prevalence, and both banks are authored probes.
- **Requested operation is customer intent, never workflow mode** — forbidden-value list plus a
  token scan across every item.
- **No model or provider selected** — provider tokens rejected by the validator.
- **No Production IR designed.**
- **No Canon source ingested.** Live Canon remains 19.
- **No Eval thresholds.** `acceptance_intent` carries what the customer asked to be true, never a
  metric or a score — *"the label must be readable"* is Canon's; *"OCR accuracy ≥ 0.98"* is Eval's.
- **No paid calls, ₹0 spend. Not merged.**

## 7. Stop conditions — checked, none triggered

| Condition | Assessment |
|---|---|
| Requires changing the fundamental Creative IR separation | **No.** All six additions sit in the Normalized Request and strengthen the separation |
| A field is inherently a Production IR / provider decision | **No.** Production routes are forbidden and mechanically rejected |
| External evidence needed to claim market prevalence | **No** — no prevalence claim is made. Every field is justified by structural recurrence or stated first-product scope, labelled differently |

Multi-turn was **flagged rather than decided**, which is the charter-correct handling of an
architecture question, not a stop.

---

### What to decide first

**U1 — freeze the `requested_operation` vocabulary.** EVAL-009 is building its condition contract in
parallel and needs the operation/workflow-mode distinction settled before it freezes. Everything else
here can wait; that one is on the critical path, and if the two collapse into one field at
measurement time, the distinction cannot be recovered afterwards.
