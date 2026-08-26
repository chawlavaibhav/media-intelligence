# E7-E — Evaluator / instrument landscape and qualification proposal

**Task:** EVAL-007 · **Date:** 26 Aug 2026 · **Spend:** ₹0
**No checker or evaluator API was called. No instrument is declared qualified by this document.**

---

## The finding that should change how we buy instruments

**Two of the metrics we would most plausibly have adopted — because they are the field standard —
are contested or demonstrably weak.**

| Metric | Its standard use | What the literature says |
|---|---|---|
| **LSE-C / LSE-D** (SyncNet) | *The* default lip-sync metric | Of the three SyncNet metrics *"only LSE-O displays moderate effectiveness, casting doubt on their widespread application as quantitative lip-audio synchronization measures in the literature"* |
| **DINO / CLIP-I** | *The* default identity metric | A high DINO score *"may risk overfitting the identity-irrelevant information"* — it can reward a shared background and call it identity |

Had we adopted either on the grounds that everyone uses it, we would have gated production on an
instrument whose validity is disputed in its own field.

**This is the strongest external argument in the whole program for the rule we already hold:** an
instrument must be qualified *for our judgement, on our conditions* before it gates anything.
"Industry standard" is a reason to evaluate a metric, never a reason to trust it.

The identity finding also **independently corroborates ADD-01** (same-category decoys). A metric that
rewards contextual similarity is precisely what a decoy is designed to catch, and we asked for decoys
before finding this evidence.

---

## What "deterministic" actually means, family by family

The most useful thing this audit did was force a sharper line between *deterministic* and *merely
automated*. A detector is automated. It is not deterministic — it is a model with error modes.

| # | Family | Genuinely deterministic | Requires a learned judge | Human role that cannot be removed |
|---|---|---|---|---|
| 1 | Text / OCR | Normalisation + string comparison | **Transcription** | Target-string validity (first-language reader); perceptibility |
| 2 | Deterministic CV / geometry | File probing; masked pixel diff; box geometry *given boxes* | **Producing the boxes** | Adjudicating occlusion and depth |
| 3 | Structured visual VLM | Almost nothing | Essentially all of it | Building the reference at all |
| 4 | Temporal / video | Frame-freeze, injected-offset recovery, flow discontinuity | Semantic drift, plausibility | Borderline drift adjudication |
| 5 | Speech / audio / AV | A/V offset from located onsets; transcript comparison | ASR, ASV, onset location | **Pronunciation acceptability** |
| 6 | Creative / commercial | Structural correlates only (timings, areas) | Preference/issue detection | Fresh independent review |

**The recurring pattern is worth naming.** In almost every family, the *comparison* is deterministic
and the *perception* is not. Family 1 compares strings deterministically but must transcribe first.
Family 2 computes geometry deterministically but must detect first. Family 5 computes an offset
deterministically but must locate the onset first.

**So the uncertainty is nearly always in the front half of the instrument, not the back half.** That
is where qualification effort and false-pass risk both belong — and recording the split (the V0
Registry's `deterministic_component` field) stops a whole instrument being written off as unreliable
when only one stage is.

---

## Per-family assessment

### Family 1 — Text / OCR

- **Qualification material:** the frozen 96-item Devanagari battery **exists**; a Latin pack does not.
- **False-pass risk:** the founding one — the checker reads *toward* the plausible word and silently
  autocorrects. External work does not appear to test this at all, so our battery is ahead of the
  reachable public state of practice for this judgement.
- **Hard gate?** **Yes** — a deterministic zero-false-pass count needs no probability model.
- **Envelope limit:** the battery perturbs *real characters*. It cannot produce malformed generated
  glyphs, so a checker qualified on it is not qualified against that failure mode.

### Family 2 — Deterministic CV / geometry

- **External corroboration:** GenEval uses Mask2Former; T2I-CompBench uses UniDet. Detector-based
  judging of counts and positions is standard practice.
- **Qualification material:** our 100 synthetic known-answer fixtures **exist**, built with zero
  human labels.
- **False-pass risk:** the shadow trap (counting a shadow as an object) — already in our fixtures.
- **Hard gate?** **Yes for file probing and masked diff. For detector-based counting, only after
  qualification**, and separately per confidence setting: the same detector at two settings is two
  instruments.
- **Refinement from E7-C:** T2I-CompBench splits 2D from 3D spatial relations. 2D is decidable from
  boxes; depth is not. These should not share an instrument or a gate.

### Family 3 — Structured visual VLM

- **This is the family with the worst ratio of importance to readiness.** It unblocks the most
  capabilities and has the least deterministic content.
- **External economics, and they are sobering:** DreamBench++ upgraded from DINO/CLIP to an MLLM
  judge for better human alignment at roughly **20,000 judge API calls and >$400 per model
  evaluated**. *(Indicative — from a search summary, needs re-verification before it informs a
  budget.)*
- **False-pass risk:** permissiveness — recognising a *category* and reporting it as an *individual*.
- **Hard gate?** **Not on current evidence.** Two-sided error rates must be plotted against human
  adjudication first, and no threshold should be proposed before that data exists.

### Family 4 — Temporal / video

- **External corroboration:** VBench's 16 dimensions and VBench-2.0's 18 are almost entirely this
  family's territory.
- **Qualification material:** none held — but **truth can be injected**: a known freeze, a known
  identity swap at a known frame, a known horizontal flip. **Zero human labels required.**
- **False-pass risk:** a near-static clip scoring perfectly on smoothness. VBench separates
  `dynamic_degree` from `motion_smoothness` for exactly this reason and we should too.
- **Hard gate?** **Plausibly yes** for injected-perturbation recall, reported *per perturbation
  type* — never as one averaged number.

### Family 5 — Speech / audio / AV

- **The contested-metric family.** See the finding above.
- **External material exists and is rights-clear:** IndicVoices-R, 1,704 hours, 10,496 speakers,
  22 Indian languages, **CC-BY-4.0**, with per-speaker metadata. Directly relevant to this product's
  Hindi/Hinglish scope. **This is a cross-stream lead for Resources.**
- **Metric split confirmed externally:** intelligibility via ASR-WER, speaker similarity via ASV,
  prosody via pitch/rate — three different instruments, exactly as we assumed.
- **False-pass risk, and it is the founding trap in a new medium:** a robust ASR *normalises a
  mispronunciation into the correct word*, precisely as the vision checker silently corrected a
  misspelling. Word correctness and pronunciation acceptability cannot share an instrument.
- **Hard gate?** Deterministic half yes; pronunciation no — that needs listeners.

### Family 6 — Creative / commercial

- **External corroboration for our restraint:** HPSv2 states *"Comparison is only meaningful for
  images generated by the same prompt"* and that v2.0 and v2.1 scores *"can not be directly
  compared"*. A preference model is relative and version-fragile.
- **False-pass risk:** **false criticism** — flagging problems in flawless work. More insidious than
  missing them, because it looks diligent.
- **Hard gate?** **Never.** This confirms `descriptive_only` for all four family-G capabilities.
- **Do not adopt an aesthetic predictor as a proxy for brand register.** VBench's
  `aesthetic_quality` is a learned taste model trained on community preference; it would answer a
  different question confidently.

---

## Evaluator drift — now a design requirement, not maintenance

GenEval2 is explicitly positioned against benchmark drift (*"Addressing Benchmark Drift in
Text-to-Image Evaluation"*), and HPSv2 states outright that its own two versions are not comparable.

Three consequences for us:

1. **Instrument version and config hash must be pinned in every Registry row.** Already done — this
   is external corroboration, not new work.
2. **A qualification is a claim about a moment.** It needs an expiry trigger, not an indefinite pass.
3. **A learned judge drifts in a way a deterministic one does not.** Family 3 and 6 results need
   re-qualification on a cadence; families 1 and 2 largely do not.

---

## Proposed qualification sequencing

Ordered by **capabilities unblocked per unit of human time**, because human time — not API spend —
is the dominant cost in this programme.

| Order | Family | Human labels needed | Why here |
|---|---|---|---|
| 1 | **2 — deterministic CV** | **None** | Pack already built; truth by construction |
| 2 | **4 — temporal** | **None** | Truth by injected perturbation; unblocks the most per unit effort |
| 3 | **1 — text/OCR** | Already spent | Battery frozen and validated; needs a roster and budget |
| 4 | **3 — visual VLM** | Substantial | Highest unblock count but needs references **and** adjudication |
| 5 | **5 — speech/AV** | Substantial | Needs AV packs plus first-language listeners |
| 6 | **6 — creative** | Largest | Most expensive, and gates nothing hard |

**Families 2 and 4 together need no human labelling at all.** That remains the best available value
and is now externally corroborated: VBench's perturbation-style dimensions are precisely the ones
whose truth can be constructed.

---

## What this document does **not** do

No instrument is qualified. No threshold is proposed — every judgement threshold remains in the
threshold register with **zero approved**. No metric is adopted. Where external practice has a
standard (LSE-C, DINO), this document has argued *against* adopting it unexamined, not for it.
