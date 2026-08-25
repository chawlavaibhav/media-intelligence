# Canon V1 early value gate — frozen protocol (C3)

**Task:** CANON-V1 overnight program, work package C3 · **Date:** 26 Aug 2026
**Status: PACKAGE ONLY. NOT EXECUTED.** 0 of 24 planning outputs generated. 0 model calls made.
0 human verdicts exist. **Do not run this before the morning integration gate.**

---

## 1. The question

**Does explicit, correctly selected Canon improve planning beyond the same procedure plus a generic
craft context?**

Not "is the Canon good". Not "does the Canon contain true things". The Canon could be entirely
correct and still add nothing a competent general model does not already produce — in which case
buying fourteen more books would be the wrong move. This gate is what tells the difference, and it
is why the runbook puts it **before** source expansion.

## 2. The two arms

| | Context supplied |
|---|---|
| **Generic** | brief + planning procedure + a general craft checklist |
| **Oracle Canon** | brief + the same procedure + hand-selected relevant accepted Canon |

Everything else is identical: same prompt, same section list, same output format, same model, same
settings, same batch.

**"Oracle" means the Canon material was chosen by hand, not retrieved.** This deliberately tests the
best case. If hand-picked, perfectly relevant Canon does not beat generic craft advice, then no
retrieval system built on top of it will either — and building retrieval first would have been
expensive wasted work. If it does win, retrieval quality becomes the next question (C8).

## 3. Three ways this experiment could lie to us, and what stops each

**A weak control.** If the generic arm were vague filler, the Canon would win and the win would mean
nothing. The generic contexts here are deliberately strong: real, usable professional craft advice.
What they lack is not quality — it is *origin, system structure and stated exceptions*. The Canon arm
gets the advice **with** where it came from, how the source organised it, and when the source says
its own rule should be broken.

**Extra words.** More context tends to produce longer, more detailed plans, which reviewers reward.
`build_run_manifest.py` refuses to build if any generic context differs from its paired oracle by
more than **15%**.

> This check earned its place immediately. On first run the oracle contexts were **22–37% longer**
> in ten of twelve pairs. Left alone, the Canon arm would have gone in with a systematic advantage
> that no reviewer could have seen. The generic contexts were extended until the maximum drift was
> **14.5%**.

**Position bias.** Reviewers favour whichever plan they read first. The A/B assignment is therefore
**balanced, not randomised per pair**: exactly 6 pairs present each arm first.

> This also earned its place. An unconstrained shuffle on the fixed seed put Canon in position A for
> **9 of 12** pairs. The dry run confirms the fix: a synthetic reviewer who always picks whatever is
> shown first now scores exactly **6/12** — a tie, in the `stop` band — rather than a Canon win.

## 4. Review dimensions

Nine creative dimensions, each judged as a preference between the two blinded plans:

concept quality · hierarchy reasoning · proposition clarity · objective fit · audience fit ·
visual/temporal strategy · trade-off awareness · contradiction handling · appropriate specificity

**A "clear Canon win" requires all three of:** a majority of the nine dimensions (≥5), more than the
other arm, and the reviewer's overall preference. One dimension is not a win.

### Explicit intent preservation is a gate, not a tenth score

Judged **per plan**, separately, and **never averaged into creative quality**. The question is: did
the plan keep every requirement the client actually stated, including copy that must appear exactly?

Violation kinds: `exact_string_altered`, `requirement_dropped`, `constraint_broken`, `fact_invented`,
`contradiction_resolved_silently`.

**If Canon degrades or violates intent on any pair where the generic arm preserved it, that overrides
the win count entirely.** A Canon that produces beautiful plans while quietly overwriting what the
customer asked for is not an improvement — it is a more articulate failure. The scorer implements
this override, and the dry run confirms it fires: a fixture with 12/12 Canon wins and two intent
violations returns `intent_regression`, not `continue`.

## 5. Predeclared gate — frozen before any output exists

| Result | Band | Decision |
|---|---|---|
| ≥9/12 clear Canon wins, no meaningful intent regression | `continue` | Canon expansion may proceed to Controller review |
| 7–8/12 | `mixed` | Diagnose before any source expansion |
| ≤6/12 | `stop` | Stop expansion; diagnose Canon noise, redundancy or over-prescription first |
| any Canon intent regression where generic preserved | `intent_regression` | Overrides the count |

**This is an engineering continuation gate, not a population claim.** Twelve briefs support a
decision about whether to keep going. They support no rate, no confidence interval and no statement
about briefs outside this set — and independence across briefs is not established. The scorer emits
no such number, deliberately, and says so in its own output.

**Changing these thresholds after seeing results is experiment mutation** and voids the run.

## 6. What must not happen

- **No agent may produce a verdict.** Reviews are human. `score_value_gate.py` contains no verdicts,
  no defaults and no imputation. A missing verdict is an error, never a tie.
- The blinding key is sealed until every verdict is recorded.
- `authoritative_intent` is never shown to a planning arm. A run that exposes it is void.
- The prompt is hashed in the run manifest; editing it after generation is detectable.

## 7. Files

| File | Role |
|---|---|
| `prompts/planning-prompt.md` | Frozen prompt, identical across arms |
| `oracle-contexts/*.md` | 12 Canon contexts, rendered from committed extraction by id |
| `generic-contexts/*.md` | 12 matched control contexts |
| `generic-source.yaml` | Authored control source |
| `output-schema.json` | One planning output |
| `verdict-schema.json` | One human verdict |
| `build_run_manifest.py` | Length match, balanced blinding, prompt hash, reviewer packet |
| `run-manifest.json`, `blinding-key.json`, `reviewer-packet-template.json` | Generated |
| `score_value_gate.py` | Aggregation from human verdicts |
| `dry-run/` | Synthetic fixtures — **not evidence** |

## 8. Verification performed in this session

All executed here; a code runner with Python 3.11 and PyYAML was available.

| Check | Result |
|---|---|
| `build_oracle_contexts.py` | exit 0 — 12 contexts, 35 Canon refs, 15 audited sources |
| `build_run_manifest.py` | exit 0 — max length drift **14.5%**, blinding **6/6** |
| Scorer, no verdicts file | `NO_VERDICTS` — refuses to infer a result |
| Scorer, always-picks-A fixture | **6/12, band `stop`** — position bias yields a tie, as intended |
| Scorer, always-picks-B fixture | **6/12, band `stop`** — symmetric, as intended |
| Scorer, mixed fixture | 0/12, band `stop` |
| Scorer, intent-regression fixture | 12/12 wins but band **`intent_regression`** — override fires |
| Scorer, incomplete fixture | `INCOMPLETE`, **exit 1** — missing verdicts named, not defaulted |

**What has NOT been verified:** nothing was generated, so the prompt has never been run against a
model, and no reviewer has ever seen the packet. The pipeline is verified on synthetic labels only.
Whether the prompt elicits usable plans, and whether reviewers can apply these dimensions
consistently, are both **unknown** and are the first things the morning gate should consider.
