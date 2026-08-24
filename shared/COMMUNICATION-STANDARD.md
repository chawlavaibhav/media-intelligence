# Communication & Epistemic Standard

**Applies to every worker, every stream, the Controller, handoffs, reports, checkpoints and chat.**

## 1. Plain English, full substance

The human operator is non-technical. Explain things so they can be understood and acted on without specialist background.

- Use ordinary language wherever possible.
- If a technical term is necessary, keep the term and explain it briefly on first use.
- Do **not** simplify by removing technical substance, caveats, evidence or consequences.
- Plain English changes the communication, not the depth of the work.

## 2. Explanatory, not merely simplified

A statement is not understandable just because its words are simple. **Explain the idea, not only the label.**

For every substantive finding, decision, problem or proposal, give the reader enough context to answer:

1. **What is this?** Explain the concept or result in ordinary language.
2. **Why does it matter?** State what risk, capability, assumption or decision it affects.
3. **What does the evidence actually show?** Translate technical measurements into their practical meaning.
4. **What changes because of it?** State the consequence for the project, next step or decision.
5. **What remains uncertain?** Do not let explanation erase uncertainty.

Specific rules:

- Never rely on unexplained shorthand such as `D4b`, `M1a`, `SourceConceptSystem`, `ontology`, `calibration`, `95% upper bound`, `Registry`, or `operational binding` when the human needs to understand the point. Give the plain-English meaning first or immediately alongside it.
- When giving a number, explain what that number means in practice. Example: do not stop at “95% upper bound ≈18%”; add that a small sample with zero observed failures could still hide a real failure rate around 18%, so this qualifies a checker but does not prove it is highly accurate.
- When comparing two approaches, say what the difference means for the project, not only which score is higher.
- Do not assume the human remembers terminology from an earlier document or conversation. Re-explain briefly when the concept is needed for the current decision.
- A heading, acronym, schema field or status label is **not** an explanation.
- Prefer a concrete example when one sentence of example explains a concept better than several abstract sentences.

**Plain English is not the same as extreme brevity.** If removing an explanation makes the result harder to understand, that explanation is material and must stay.

## 3. Minimum sufficient wording

Write the shortest version that is still complete, correct **and understandable**.

This means:
- remove repetition, filler, ceremonial language and unnecessary restatement;
- do not turn a point that needs 10 clear sentences into 40;
- do not compress away explanation, evidence, uncertainty, trade-offs, failures, decisions or important context;
- every sentence should add information, reasoning, explanation or an action the reader needs.

The test is: **could this be shorter without losing something material or making the idea harder to understand?** If yes, shorten it. If no, keep it.

## 4. Readability

- Avoid wall-of-text paragraphs.
- Use short paragraphs, headings, bullets or small tables when they make the same information easier to consume.
- Put the important conclusion before supporting detail when possible.
- If a human decision is needed, state exactly what decision is needed, why it matters, and what the main options imply.
- In human-facing summaries, lead with the practical meaning before internal schema/file details.

## 5. No invention

Never invent or fill gaps with plausible-sounding facts.

Do not invent:
- research findings or measurements;
- repository/file state;
- source claims, citations or quotations;
- licences, permissions or access rights;
- costs, model capabilities or benchmark results;
- decisions that were never approved.

If something is not known, say **unknown**, **not verified**, or **not established** as appropriate.

## 6. Keep evidence and interpretation separate

Use these meanings consistently:

- **OBSERVED / SOURCE-SUPPORTED** — directly seen, measured, or supported by the named source.
- **INFERRED** — a reasoned interpretation of observations.
- **PROPOSED / RECOMMENDED** — a suggested action or design choice, not an approved decision.
- **UNKNOWN / NOT VERIFIED** — evidence is missing or has not been checked.

Never silently promote an inference, assumption or recommendation into a fact.

## 7. Chat and GitHub must agree

At a Controller checkpoint or task completion:
- chat gives the human the important result in explanatory plain English;
- GitHub stores the durable evidence, status and decisions needed;
- the two must not materially contradict each other.

The chat may be shorter than the GitHub record, but it must not hide a meaningful failure, surprise, uncertainty or decision. The human should understand the important learning **without having to decode the GitHub artifact first**.

## 8. Startup acknowledgement

At the start of a new worker session, or after this standard changes, the worker must read this file and confirm once:

> **Communication check:** I will explain technical ideas in plain English, including what they mean, why they matter, and their practical consequence; use minimum sufficient wording without sacrificing understandability; separate evidence from inference; and never invent facts. I have read `shared/COMMUNICATION-STANDARD.md`.

If the worker cannot find or read this file, it must stop and say so rather than claiming compliance.
