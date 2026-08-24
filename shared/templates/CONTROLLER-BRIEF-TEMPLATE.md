# Controller Brief — <TASK ID>

**TASK:** <ID>
**STATUS:** completed | blocked | needs_controller_review

**HUMAN SUMMARY:** Explain the most important result in plain English. State what it means, why it matters, what changed because of it, the main uncertainty, and any decision needed. Define unfamiliar technical terms on first use. Translate consequential numbers into practical meaning. Do not assume the reader remembers internal labels from earlier work.

**WHAT I DID:** 2–4 sentences, explaining the method rather than only naming files/tools.

**OBSERVED:** directly seen / measured / source-supported. No interpretation here. If a technical measurement matters, add one sentence explaining what it means in practice.

**INFERRED:** interpretation based on the observations above. Never merged with OBSERVED. Explain the reasoning connecting the evidence to the interpretation.

**SURPRISES / BELIEF UPDATES:** what did not behave as expected, what became more or less plausible, why that matters, and what the next worker should not take at face value.

**FAILURES / BLOCKERS:** explain the actual consequence, not only the error/status label.

**UNKNOWN / NOT VERIFIED:** material gaps that remain. Do not fill them with guesses. State why the gap matters if it affects a decision.

**ASSUMPTIONS CHALLENGED:** reference coordination/ASSUMPTIONS.md entry numbers and briefly explain what changed.

**LOCAL IMPLICATIONS:** this stream only; explain the practical consequence.

**CROSS-STREAM IMPLICATIONS:** tag as CROSS_STREAM — propose, do not act. Explain which other stream is affected and how.

**ARCHITECTURAL IMPLICATIONS:** tag as ARCHITECTURAL — this should have already triggered a STOP. Explain what part of the system design is affected.

**DECISIONS NEEDED FROM CONTROLLER:** state the exact decision, why it matters, and the consequence of the main options.

**EVIDENCE WORTH HUMAN INSPECTION:** at most the few artifacts/examples that materially affect direction; say what the human should notice in each. `none` if genuinely none.

**FILES CREATED / MODIFIED:**

**RECOMMENDED NEXT STEP:** a recommendation, not a next action taken. Explain why this is the next useful step.

**EPISTEMIC CHECK:** Confirm that facts are source-supported/observed, interpretations are labeled, unknowns are not invented, no unexplained technical shorthand carries the main meaning, and no unapproved decision is presented as fact.

**CONFIRMATION:** No unapproved next strategic step was started.

---
Follow `shared/COMMUNICATION-STANDARD.md`. Aim for ~500–1000 words only when that much is necessary; shorter is preferred only when the explanation remains complete and understandable. Detailed evidence stays in the stream's findings/experiments/runs folder and is referenced by path rather than pasted in full.
