# CANON-010 — request-coverage extension bank (C10-D)

**Task:** CANON-010 / C10-D · **Date:** 26 Aug 2026 · **Status: PROPOSED FOR CONTROLLER FREEZE**
**Machine-readable:** `REQUEST-COVERAGE-EXTENSION.jsonl` · **Source:** `request-coverage-extension-source.yaml`
**The original 30 briefs are byte-identical.** Verified by SHA-256 in `validate_request_freeze.py`.

---

## 1. Why this bank exists

CANON-009 measured the original 30 briefs against real request patterns and found an inversion: the
two operations most demonstrably present in real requests — **editing a supplied asset** and
**animating a supplied image** — had **zero** coverage, while exact text (28/30) and speech (12/30)
had no measured real-user frequency at all.

The Controller's disposition was to **keep the 30 byte-identical** as the frozen generation-core /
value-gate bank and authorise a **separate extension** covering at minimum edit, animate-from-supplied-image
and variant/campaign-set requests.

This is that extension. **Eleven items.**

## 2. Sized by coverage, not symmetry

The task says to add only as many items as coverage requires and not to force a symmetric count.
Eleven is what it took.

| Operation | Items | Why this many |
|---|---|---|
| **edit** | 4 | Three distinct preservation shapes — remove, background change with text survival, targeted text substitution — plus the multi-turn probe |
| **animate** | 2 | The camera/subject separation needs both directions: camera moves and subject does not (RX-05), subject moves and camera does not (RX-06) |
| **variants** | 2 | Two different acceptance bases: per-deliverable (RX-09) and set-level (RX-10). These have different economics |
| **restore** | 1 | Distinct acceptance semantics; one item establishes it |
| **extend** | 1 | One item covers the operation |
| **compose** | 1 | One item covers dual identity references plus a new relationship |

`generate` needs no items — the original 30 cover it 30 times over.

## 3. Language is earned, not balanced

**English 5, Hindi 2, Hinglish 4.** Deliberately asymmetric.

The task forbids duplicating prompts merely to balance languages, and the validator **fails the
build** if a non-English item carries no `language_dependency`, or if two items differ only by
language while covering the same operation and the same co-occurrences.

Every non-English item states what genuinely changes:

| Item | Language | What actually depends on it |
|---|---|---|
| **RX-02** | Hindi | Text **survival** under an edit. A damaged Devanagari matra produces a plausible-looking *wrong word*, not obvious garbage — Latin does not fail this way |
| **RX-03** | Hinglish | The substitution **switches script** mid-layout. The replacement has different metrics and must still fit |
| **RX-06** | Hindi | Text **stability under motion**. A conjunct that flickers between frames yields a different word frame-to-frame while each frame looks individually fine |
| **RX-08** | Hinglish | Separates **instruction language from on-screen-copy language** — the request is Hinglish, the headline is Devanagari |
| **RX-09** | Hinglish | **Language is the variation axis itself** — four languages, three non-Latin scripts, one fixed layout |
| **RX-11** | Hinglish | Relative-degree revisions (*"thoda zyada warm"*) and referring expressions (*"isme"*) carry the inheritance problem; a formal English rewrite would smooth away the very thing the probe exposes |

## 4. The items

| ID | Operation | Lang | What it probes | Wave 1 |
|---|---|---|---|---|
| RX-01 | edit | EN | Remove one element; everything else implicitly preserved | ✅ |
| RX-02 | edit | HI | Background change while Devanagari pack text survives intact | ✅ |
| RX-03 | edit | HG | Targeted text substitution inside a finished layout, across scripts | ✅ |
| RX-04 | restore | EN | Damage repair without inventing detail or modernising | ✅ |
| RX-05 | animate | EN | **Camera moves, subject must not** | ✅ |
| RX-06 | animate | HI | **Subject moves, camera must not** + text stable under motion | ✅ |
| RX-07 | extend | EN | Enlarge canvas without cropping named elements | ✅ |
| RX-08 | compose | HG | Two identity references, one new relationship | ✅ |
| RX-09 | variants | HG | 4 deliverables, language axis, **per-deliverable** acceptance | ✅ |
| RX-10 | variants | EN | 3 deliverables across modalities, **set-level** acceptance | ✅ |
| RX-11 | edit | HG | Multi-turn inheritance | ❌ **representation only** |

## 5. Three design points worth the Controller's attention

### 5.1 A supplied asset does not imply `edit`

**RX-08 is the item that makes this concrete.** The customer supplies two photographs — a model
portrait and a packshot — and asks for a new creative combining them. Both assets carry role
`identity_reference`, **not** `subject_of_operation`. Neither supplied image is being modified.

Compare RX-01, where the supplied photograph *is* the artefact being changed.

Assign roles by *"an asset was attached"* and these two requests become indistinguishable — with
opposite preservation semantics. That is why `subject_of_operation` is a new role rather than an
inference.

### 5.2 Acceptance basis is an economic fact, not a formality

RX-09 and RX-10 are both `variants`, and they cost differently to satisfy:

- **RX-09** — *"koi choose nahi karna"* — the customer will use all four, so **every one** must be
  acceptable. `per_deliverable`.
- **RX-10** — *"take it or leave it as a whole"* — one weak deliverable fails the set. `set_level`.

The product's primary metric is **Cost per Accepted Outcome**. Without this distinction we cannot
express, let alone price, the difference between four independent acceptances and one joint one.

### 5.3 Implicit preservation is recorded, never enumerated

An edit request names what should change; everything else is implicitly preserved. It is tempting to
expand that into an explicit `preserve` entry per element — and wrong, because those entries would be
recorded as things the customer said, and the customer said none of them.

Every item uses `preservation_default: implicit_everything_not_named`. Where an item *does* record an
explicit preserve intent (RX-02, RX-03, RX-04, RX-05, RX-08), the customer genuinely said so, and the
item carries an **`evidence_quote`** pointing at their exact words. The validator rejects a customer-provenance
claim without one.

> This check was strengthened mid-build. The first version matched English keywords against the
> request text, which **cannot work** when the intent target is described in English and the request
> is in Devanagari — it silently passed. A provenance check that quietly fails on non-Latin scripts
> is worse than none, so it now demands a verbatim quote instead.

## 6. What this bank is not

- **Not demand evidence.** Eleven authored probes covering a discovered space. Authoring them does
  not make them evidence about what customers ask for, and no frequency claim attaches to any item.
- **Not a replacement for the 30.** Separate, additive, and the 30 remain byte-identical.
- **Not a Wave-1 runnable set on its own.** Ten of eleven are runnable; RX-11 is representation-only
  and the validator fails the build if it is ever marked otherwise.
- **Not a workflow specification.** No item names a technique or a provider — the validator rejects
  both. Every item states *what the customer wants*, never *how to make it*.
