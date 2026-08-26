# Canon V1 early value gate — frozen protocol (C3)

**Task:** CANON-V1 overnight program, work package C3 · **Date:** 26 Aug 2026
**Status: PACKAGE ONLY. NOT EXECUTED.** 0 of 24 planning outputs generated. 0 model calls made.
0 human verdicts exist.
**Corrected 26 Aug 2026** under `canon/tasks/CANON-V1-CORRECTION-PASS.md` (C-C3 to C-C7).
**The real gate cannot be run yet — see §0.**

---

## 0. What the correction pass changed, and the one blocker that remains

Four things about the first version would have produced a result that could not be interpreted.

| Was | Now |
|---|---|
| Controls authored by the same session that had read the Canon | Those controls are **quarantined and unusable in a real run**. Replacements must come from a fresh session with no Canon access, via `GENERIC-CONTROL-AUTHORING-PACKET.md`. |
| Blinding key derived from a committed seed and committed as plain JSON | Fresh OS entropy at preparation time, key stored **outside** the repository, only a salted SHA-256 commitment committed |
| One reviewer | **Two independent reviewers**, combined by unanimity, never averaged |
| All 12 pairs voted on continuation | **Only the 7 coverage probes vote.** The 5 gap probes are diagnostics |

**Blocker: `FRESH_CONTROL_SESSION_REQUIRED`.** `prepare_real_run.py` refuses to start until
`generic-contexts-real/` exists. Until an independent session authors those controls, the real gate
cannot run. That refusal is deliberate and is covered by a test.

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

**Position bias.** Reviewers favour whichever plan they read first, so the A/B assignment is
**balanced, not randomised per pair** — and balanced **within each probe stratum**, which is a
stronger condition than it first appears.

> This check earned its place twice.
>
> First, an unconstrained shuffle put Canon in position A for **9 of 12** pairs.
>
> Then, after fixing that to a tidy 6/6 overall, the negative control **failed again** — and the
> reason is the interesting part. Only the 7 coverage probes vote on continuation, and the 6/6 split
> happened to show Canon first on **5 of those 7**. A reviewer with a pure position effect would have
> scored 5/7 and reached `continue` without reading a word. **Overall balance was the wrong
> invariant.** Balance now applies inside each stratum, and because 7 is odd, any leftover pair is
> given to the *control* arm rather than to Canon. Canon is now shown first on 3 of 7 coverage
> probes, and pure position bias lands in `stop`.
>
> Neither of these was visible by reading the code. Both were found by asking what a lazy reviewer
> would score.

**Control contamination.** The most serious of the four, because no amount of care inside one session
fixes it. See §0 and the authoring packet.

## 4. Review dimensions

Nine creative dimensions, each judged as a preference between the two blinded plans:

concept quality · hierarchy reasoning · proposition clarity · objective fit · audience fit ·
visual/temporal strategy · trade-off awareness · contradiction handling · appropriate specificity

**A "clear Canon win" requires all three of:** a majority of the nine dimensions (≥5), more than the
other arm, and the reviewer's overall preference. One dimension is not a win.

### Two independent reviewers, combined by unanimity (C-C5)

Every pair is judged by **exactly two distinct reviewers**, independently. A pair counts as a clear
Canon win only when **both** satisfy the per-reviewer rule above.

One clear win plus one non-win is **not** a win. Neither is `cannot_tell`. Those are **disagreement**,
and disagreement is reported explicitly rather than resolved by arithmetic.

**Reviewer judgements are never averaged.** Averaging two people's preferences into a number invents a
precision neither of them expressed, and it would let a strong opinion and a shrug combine into a
confident-looking half-win. The scorer keeps each reviewer's raw judgement and rejects any pair that
does not carry two distinct reviewer ids.

### Coverage probes vote; gap probes diagnose (C-C6)

The early-12 splits **7 coverage probes / 5 gap probes**, and they answer different questions.

| | Question |
|---|---|
| **Coverage probe** | Where the live Canon actually holds relevant accepted knowledge, does explicit Canon beat an independent generic control? |
| **Gap probe** | How far does general Canon knowledge carry into a known hole, and what failure remains attributable to missing knowledge? |

**Only the 7 coverage probes vote on continuation.** Letting a gap probe vote to stop expansion would
be perverse: it would use the *absence* of a source as an argument against *acquiring* one. A gap
probe losing is close to the expected result — that is what a gap is.

Gap probes are reported separately, and two tests hold the line: gap wins cannot rescue a failing
band, and gap losses cannot sink a passing one.

### Explicit intent preservation is a gate, not a tenth score — and it is global

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

**Over the 7 coverage probes only:**

| Unanimous Canon wins | Band | Decision |
|---|---|---|
| **5–7 of 7** | `continue` | Canon expansion may proceed to Controller review |
| **4 of 7** | `mixed` | Diagnose before any source expansion |
| **0–3 of 7** | `stop` | Stop expansion; diagnose Canon noise, redundancy or over-prescription first |
| any Canon intent regression on **any** pair | `intent_regression` | **Overrides the band.** Blocks automatic continuation pending Controller diagnosis |

The 5 gap probes are reported as diagnostics and never move the band.

**This is an engineering continuation gate, not a population claim.** Seven briefs support a decision
about whether to keep going. They support no rate, no confidence interval and no statement about
briefs outside this set — and independence across briefs is not established. The scorer emits no such
number, deliberately, and says so in its own output.

The scorer refuses to rescale these thresholds if the probe count ever differs; it returns
`undefined_probe_count` instead. Adjusting a frozen threshold to fit a changed denominator is how a
predeclared gate quietly stops being predeclared.

**Changing these thresholds after seeing results is experiment mutation** and voids the run.

## 6. What must not happen

- **No agent may produce a verdict.** Reviews are human. `score_value_gate.py` contains no verdicts,
  no defaults and no imputation. A missing verdict is an error, never a tie.
- **The contaminated controls may never be used in a real run.** Enforced by refusal, not by
  convention.
- The blinding key is generated at preparation time from OS entropy, stored outside the repository,
  and revealed only after every verdict is frozen. `--verify-key` then proves the revealed key
  matches the commitment frozen beforehand, so a mapping altered mid-review is detectable.
- `authoritative_intent` is never shown to a planning arm. A run that exposes it is void.
- The prompt is hashed in the run manifest; editing it after generation is detectable.

## 7. Files

| File | Role |
|---|---|
| `prompts/planning-prompt.md` | Frozen prompt, identical across arms |
| `oracle-contexts/*.md` | 12 Canon contexts, rendered from committed extraction by id |
| `generic-contexts-DRYRUN-CONTAMINATED/` | **Invalidated controls.** Dry-run fixtures only |
| `generic-contexts-real/` | **Does not exist yet.** Independent controls go here |
| `GENERIC-CONTROL-AUTHORING-PACKET.md` | Instructions for the fresh authoring session |
| `control-authoring-input.json` | Self-contained input, proven free of Canon |
| `build_control_packet.py` | Builds that input and fails closed on leakage |
| `prepare_real_run.py` | Real-run preparation: refuses contaminated controls, sealed key |
| `generic-source.yaml` | Authored source of the contaminated controls |
| `output-schema.json` | One planning output |
| `verdict-schema.json` | One human verdict |
| `build_run_manifest.py` | Length match, balanced blinding, prompt hash, reviewer packet |
| `run-manifest.json`, `blinding-key.json`, `reviewer-packet-template.json` | Generated |
| `score_value_gate.py` | Aggregation from human verdicts |
| `dry-run/` | Synthetic fixtures — **not evidence** |

## 8. Verification performed

All executed here; a code runner with Python 3.11 and PyYAML was available.

| Check | Result |
|---|---|
| `build_oracle_contexts.py` | exit 0 — 12 contexts, 35 Canon refs, 15 audited sources |
| `build_run_manifest.py` | exit 0 — max length drift **14.5%**, blinding **6/6** |
| Scorer, no verdicts file | `NO_VERDICTS` — refuses to infer a result |
| **`tests/test_value_gate_corrections.py`** | **26 negative controls, all passing** |
| Coverage bands 5/7, 4/7, 3/7 | `continue` / `mixed` / `stop` respectively |
| Gap probes winning on a 3/7 coverage result | still `stop` — gaps cannot rescue |
| Gap probes losing on a 5/7 coverage result | still `continue` — gaps cannot sink |
| One reviewer, or the same reviewer twice | `INCOMPLETE`, **exit 1** |
| Reviewer disagreement on a winning pair | not counted; drops 5/7 to 4/7, `mixed` |
| Intent regression on a **gap** probe with 5/7 coverage | `intent_regression` — global, overrides |
| Missing pair / missing dimension | `INCOMPLETE`, **exit 1** |
| Position bias, both reviewers always pick first | does **not** reach `continue` |
| Real-run preparation with no independent controls | **REFUSED** |
| Real-run preparation writing the key inside the repo | **REFUSED** |
| Committed real-run artifacts disclosing the mapping | none — asserted by test |
| Control-authoring packet containing Canon | none — asserted by test, and the leakage check is itself tested to fire |

**What has NOT been verified:** nothing was generated, so the prompt has never been run against a
model, and no reviewer has ever seen the packet. The pipeline is verified on synthetic labels only.
Whether the prompt elicits usable plans, and whether reviewers can apply these dimensions
consistently, are both **unknown** and are the first things the morning gate should consider.
