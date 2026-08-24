# Evaluation Corpus Plan

**Date:** 23 Aug 2026 · **Nothing downloaded. Nothing licensed. Research record only.**

We hold too little media to run Experiment B properly: 64 scored generations, 14 Finding 01
samples, some spike video. All ours, all from two models, all one brand.

**⚠ Verification required before any use.** Everything below is recorded from prior knowledge with
a cutoff of May 2026. **Sizes, URLs and especially licences must be checked against the source
before anything is downloaded.** Where a licence is marked *unverified*, assume nothing.

---

## The standing rule

> **Existing dataset labels are not ground truth for our Canon.**

An aesthetic score, a preference vote, a "prompt adherence" label — each was collected against
somebody else's rubric, for somebody else's question. None answers *is this good for this
commercial objective?*

**The media is the asset. The labels are a convenience.** Where a dimension matters to us, we
create our own blind human annotations against our own rubric. External labels are useful for
sampling, for stratifying, and for checking whether our judges are wildly out of line with a large
population — nothing more.

---

## A · Real advertising

**Pitt Ads Dataset** (Hussain et al., CVPR 2017)
~64k image ads, ~3.5k video ads. Annotated for topic, sentiment, rhetoric (the "what should I do,
and why" action-reason structure), symbolism, and free-form Q/A.
*Why us:* the only large corpus of **real commercial creative with intent annotations**. Directly
relevant to proposition clarity, objective fit and persuasion — the Experiment A dimensions we
otherwise cannot test against real work.
*Tests:* proposition clarity, objective fit, hook, symbolism, product prominence.
*Licence:* research use, **unverified**. Media are scraped ads — third-party copyright almost
certainly applies. **Internal research only; assume no commercial reuse.**

**Persuasion Strategies in Advertisements** (Singla et al., AAAI 2022)
~3k ad images annotated with named persuasion strategies. Built on Pitt Ads.
*Why us:* the closest public thing to a persuasion taxonomy with labelled examples — a direct check
on whether Canon-informed evaluation identifies strategy correctly.
*Licence:* research, **unverified**.

---

## B · AI-generated images with human preference

**Pick-a-Pic** (Kirstain et al., 2023) — ~500k+ pairwise human preferences over generated images,
with prompts. *Why us:* pairwise is our judging format. Large enough to sample stratified subsets.
*Licence:* open, **unverified**.

**HPD v2** (Wu et al., 2023) — ~798k pairwise comparisons across ~433k images, multiple generators.
*Why us:* generator diversity, so evaluator behaviour can be tested across model styles rather than
just ours.
*Licence:* research, **unverified**.

**ImageRewardDB** (Xu et al., 2023) — ~137k expert comparisons with separate ratings for alignment,
fidelity and harmlessness. *Why us:* **separated dimensions**, closest public analogue to our split
between technical fidelity and creative fitness.

**AVA** (Murray et al., 2012) — ~255k photographs with aesthetic ratings from a photo-contest
community. Not AI-generated. *Why us:* aesthetic judgement on real photography, useful for
calibrating whether our judges track a large human population at all.
*Caveat:* contest aesthetics are not commercial effectiveness. Ogilvy's whole opening argument.

---

## C · Prompt adherence and composition

**T2I-CompBench** — ~6k prompts across attribute binding, spatial relations, numeracy and complex
composition, with evaluation protocols. *Why us:* maps almost directly onto Capability Lab
dimensions — count, relations, placement. **Capability Lab material more than Canon material.**

**GenEval** — object-focused: counting, position, colour attribution, verified by object detection.
*Why us:* deterministic instruments for the technical side of evaluation, where a VLM should not
be trusted.

**TIFA / question-generation faithfulness** — generates questions from the prompt and checks the
image answers them. *Why us:* a methodology worth borrowing for acceptance-contract checking.

---

## D · Text rendering in images

**MARIO-Eval** (TextDiffuser, 2023) — text rendering benchmark, Latin script.
**AnyText / AnyWord-3M** — multilingual text rendering, includes Chinese and English.
*Why us:* exact text is a hard constraint and our worst observed failure area.
**⚠ Critical unknown: whether either covers Devanagari.** Finding 01 suggests not — it found no
usable public tooling for Devanagari verification, and classical OCR failed completely.

**If no public Devanagari rendering benchmark exists, we must build one.** It would be small,
cheap, and genuinely proprietary — and it is the single highest-value gap in this document.

---

## E · Video

**VBench** — ~16 dimensions including subject consistency, background consistency, temporal
flickering, motion smoothness, dynamic degree, aesthetic and imaging quality, with human preference
annotations per dimension.
*Why us:* **the closest existing thing to our observation-unit problem.** Subject consistency and
temporal flickering are cross-frame properties, which is exactly what Finding 11 showed a
frame-level evaluator cannot see. Adopt the methodology, not the scores.

**EvalCrafter** — objective metrics plus human alignment across generation, quality and adherence.
**T2VQA-DB** — text-to-video quality with mean opinion scores.
**VideoScore / VideoFeedback** — multi-aspect human-annotated video quality.

*Why us:* video evaluation is where we are weakest and where our product lives.
*Licences:* research, **all unverified**.

---

## What no public dataset gives us

| Gap | Why it matters | Path |
|---|---|---|
| **Devanagari / Indic text rendering** | Our worst observed failure; no public benchmark found | **Build it.** Small, cheap, proprietary. |
| **Indian commercial creative with intent labels** | Our market; Pitt Ads is Anglo-American | Build from customer work + expert annotation |
| **Short-form feed-native assets with performance data** | Our format; hook windows, sound-off | Platform data + customer outcomes |
| **Commercial outcome linked to creative** | Assumption 13 — never examined | Customer campaign data, long horizon |
| **Brand-constraint violations** | Logo exactness, mandatories — nobody labels these | Build from our own runs |

Four of five must be built. That is consistent with the whole thesis: the transferable knowledge is
public, and **the proprietary asset is the data about our own market and our own failures.**

---

## Recommended sequence

1. **Verify before anything else.** Licence, access terms, whether media may be redistributed, and
   whether use is research-only. Do not download on the strength of this document.
2. **Start with Pitt Ads.** Real commercial creative with intent annotations is the one thing we
   cannot substitute, and Experiment A's dimensions need it.
3. **Check the Devanagari question.** One afternoon; determines whether we build a benchmark.
4. **Adopt VBench's dimensional method** for video evaluation design, without adopting its scores.
5. **Sample small and annotate ourselves.** 50–100 assets, blind, against our rubric, beats 10,000
   with someone else's labels.
6. **Keep external and internal labels in separate stores.** Never merge; an external label is a
   different origin under SPEC-05 and should be related, not absorbed.
