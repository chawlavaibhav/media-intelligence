# Canon Experiment V0 — design only, not to be run

**Date:** 23 Aug 2026 · **Blocked on:** Coverage Map and Curriculum review, then Canon V0 build.

Two separate experiments. Neither is "books versus no books." Both test **latent model knowledge
versus explicit, retrieved, structured knowledge** — the same reasoning model throughout.

Technical exactness checks (text match, logo, count, aspect ratio) are a **separate instrument**
and appear in neither experiment's judging.

---

# Experiment A — Creative planning

**Question:** does explicit Canon context improve the Creative Spec that the same reasoning model
produces?

## Arms

| Arm | Receives |
|---|---|
| **A** | brief only, free-form output — the commercial baseline |
| **B** | brief + Creative IR schema + a **generic craft checklist** |
| **C** | brief + same schema + **retrieved Canon relevant to this brief** |

**B versus C is the experiment.** A is context for how far the whole procedure moves things, and
is not a clean comparison — A produces prose, B and C produce a filled schema.

**B and C must be matched on length, formatting and instruction style.** If C wins only because it
received more text, the result is worthless. B's checklist is written to the same word count as
C's average retrieval, from generic craft vocabulary with no source-derived content.

## Input design — two axes

**Axis 1 — task variety.** 30 underlying briefs across three challenge families chosen to separate:
product prominence (Canon should help most), typography-heavy including Devanagari (a known
weakness with a proven checker from Finding 01), emotional/lifestyle concept (latent knowledge
strongest, Canon likely helps least). Ten each — three deep beats six thin.

**Axis 2 — how the request arrives.** Five phrasings of each underlying intent: novice one-liner,
marketer brief, expert production prompt, messy/Hinglish, over-specified with a contradiction.

**150 specs per arm, text only.** No image generation in Experiment A at all.

## Judging dimensions

Concept quality · hierarchy reasoning · proposition clarity · objective fit · audience fit ·
visual strategy · trade-off awareness · internal contradictions · specificity without unnecessary
prescription · **preservation of explicit user intent**.

That last one is a **safety dimension, not a quality dimension.** A Canon that improves the other
nine while overriding what the customer actually asked for has failed. Scored separately and
reported separately.

## Protocol

- **Blind and randomised.** Arm labels stripped, sides shuffled per pair.
- **Human judges first, machines second.** Finding 01 established that a confident wrong checker
  is worse than none, on a task far easier than this. No machine judge is trusted until agreement
  with human verdicts is measured **on this task**.
- **Pairwise, not absolute scoring.** "Which better satisfies the brief, and why" beats "8.3/10".
- **Reason recorded against the dimension list**, so we learn *where* Canon helped.
- **Tie rule fixed in advance.** Ties are recorded as ties, never split.
- **Invariance metrics** from SPEC-01: explicit intent preservation, explicit intent mutation,
  incorrect autonomous decision. All text-only.

## Pre-registered interpretation

| Result | Reading |
|---|---|
| C materially beats B | Explicit knowledge adds beyond latent. Continue the curriculum. |
| C ≈ B | The **structure** did the work, not the knowledge. Stop processing books; invest in schema and Empirical Memory. |
| C loses to B | Retrieval is noisy, knowledge over-prescriptive, or atoms lack context. Debug. If it survives debugging, the thesis is weakened **for this task**. |
| B materially beats A | The procedure itself is valuable **even if the Canon is not**. A real and separately shippable finding. |
| C wins but intent preservation drops | **Failure.** A Canon that overrides customers is not shippable at any quality level. |

Numbers: at 30 briefs, 27/40-style thresholds are roughly p≈0.02 and meaningful; 21/40 is a coin
flip. Report wins, losses and ties separately.

**Cost: LLM calls only.** No generation spend.

---

# Experiment B — Creative evaluation

**Question:** does explicit Canon context improve the same evaluator's assessment of a finished asset?

Run second. It reuses Experiment A's judge calibration.

## Arms

Same evaluator model, given the asset plus its brief plus relevant constraints:

| Arm | Receives |
|---|---|
| **B** | asset + brief + generic critique instructions |
| **C** | asset + brief + retrieved Canon relevant to this brief's dimensions |

## Material

**No new generation initially.** We already hold: 64 human-scored generations in
`spike/out/scores.json` with pass/fail and a written reason; the Finding 01 samples; existing
video from the spike. Plus an external pool once [EVAL-CORPUS-PLAN](EVAL-CORPUS-PLAN.md) is
reviewed.

**Existing labels are not ground truth for creative fitness.** `scores.json` records one defect
per asset — Finding 11 found an image with two where only one was written down. Ground truth for
this experiment is **fresh blind human annotation against our own rubric**.

## Measures

- **Important issues found** — against the blind human annotation
- **Important issues missed**
- **False or irrelevant criticisms** — the failure mode a knowledge-loaded evaluator is most prone
  to: inventing violations of principles it has just read
- **Diagnosis quality** — does it name a cause, not just a symptom
- **Explanation quality** — would a customer understand it
- **Observation unit appropriateness** — did it look at the right thing? Finding 11's strongest
  result: *Grammar of the Shot* says continuity breaks are invisible frame-by-frame, and the Wan
  clip's drifting misspelling was exactly that. **Does a Canon-informed evaluator ask for the shot
  pair?**
- **Usefulness of the proposed creative correction**

## Pre-registered interpretation

| Result | Reading |
|---|---|
| C finds more real issues, false criticisms flat | Canon improves evaluation. Strongest available result. |
| C finds more real issues, false criticisms also up | Ambiguous. Compute net value; a noisy evaluator may be worse than a quiet one. |
| C ≈ B | Latent knowledge was already sufficient for critique. |
| C's false criticisms rise sharply | Canon is being pattern-matched onto assets. Retrieval is too loose. |
| C asks for the right observation unit where B does not | **Independently valuable even if issue counts tie** — it means Canon shapes the instrument. |

---

## What neither experiment tests

Routing. Cost per accepted outcome. Whether an open model can substitute. Whether the Canon helps
on long-form or non-advertising media. Whether Canon-derived requirements plus a Capability
Registry improve model selection — that needs the Registry, which does not exist.

## Sequence

```
Canon V0 built  →  human judge calibration  →  Experiment A (text only)
                                                    ↓
                                     read result, then Experiment B
```

Do not start until the Coverage Map and Curriculum are reviewed.
