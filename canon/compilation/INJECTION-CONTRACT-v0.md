# INJECTION-CONTRACT v0 — how compiled doctrine reaches a weak model, and what forces its use

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

**Task:** REP-05. **Addresses:** GAP-02 (consumption not forced by schema), GAP-14.
**Companions:** `canon/compilation/COMPILED-DOCTRINE-SPEC-v0.md` (pack shape),
`canon/packs/pack-triggers-v0.yaml` (NR → pack selection),
`canon/packs/COMPILED-PACK-CONTRACT-v0.1.md` (runtime contract this instantiates).
**Consumption target:** the 12 sections of `eval/experiments/EVAL-037/common/system-prompt.txt`.

## 1. Why the contract is shaped this way (established, not conjectured)

- Optional, model-triggered Canon use measured **0/18** on Gemma (EVAL-037 FULL_CANON;
  `eval/experiments/EVAL-037/CONCLUSION.md`; recompute
  `python3 canon/validation/recount_eval037_retrieval.py`). Nothing here is optional.
- Bounded REQUIRED structure completed **18/18** in the same experiment. Everything here is a
  required field with a bounded answer.
- A weak model cannot arbitrate two competing claims. Every contested pair is pre-arbitrated by
  the compiler into ONE scoped if/then rule with a `resolution_rule`
  (`canon/context/CANON-CONTEXT-SPEC-v0.1.md` R7); the model never sees an open contradiction
  without the rule that already decides it.
- Nothing is retrievable at runtime (EVAL-037: 53 searches, 1 read). The pack text is the
  delivered read (R3), injected unconditionally per the trigger table — O(1) in corpus size.

## 2. System-prompt block (~340 tokens; the invariant prefix)

Injected once, before any pack text, verbatim:

```
CANON_DOCTRINE packs are compiled production decisions from an audited corpus. Each
DEFAULT is a decision already made: accept it, or override it — legal only when a specific
brief clause forces it — record it in DOCTRINE_DEVIATIONS with that clause. Never
re-arbitrate a PRE-ARBITRATED CONFLICT: the stated rule decides. A conflict rule inherits
the confidence marker and override path of its decision_ref: a DOCTRINE_DEVIATIONS entry
on that decision id covers its conflict rules. Answer every CHECK by
decision id in FAILURE_PREVENTION as pass or fix: <what changed>.

Marker legend. MEASURED = the source compares or measures. REASONED = a mechanism is given.
ASSERTED = stated without either. CONTESTED = contradicted within its source. QUALIFIED =
narrowed by an in-source exception. DATED = tied to its era's technology. CULTURE-BOUND = tied
to its culture. FIGURE-UNVERIFIED = cites an uninspected figure. MEDIUM-UNTESTED = transfer to
short feed video untested — assume it neither way. -hedged = extractor-added caveat.
-our_reading = our interpretation, not the source's words. SINGLE-ORIGIN / MULTI-ORIGIN(n) =
independent sources behind the decision, never claim-level agreement. Markers label evidence
character, never rank sources. A weak marker is a reason for care, not silence: follow the
default unless a brief clause forces otherwise.
```

Size: the fenced block is 1,354 chars = 339 tokens at the repo's 4-chars/token estimate
(recompute: extract the fenced block, `ceil(len/4)`); the trigger table budgets it at
`system_prompt_block_tokens: 340`, and `canon/validation/validate_compiled_pack.py` verifies
the block stays within that figure.

Placement (COMPILED-PACK-CONTRACT §4): system prompt carries this block, then the selected
packs' `terse_injection_text` in canonical order (universal → modality-base → conditional),
then the cache breakpoint; the volatile NR follows as the first user-turn content. Nothing
request-specific sits upstream of the breakpoint.

## 3. FINAL_PRODUCTION_PACKAGE schema v2

v1 is the 12-section list in `eval/experiments/EVAL-037/common/system-prompt.txt` (DELIVERABLE
… KNOWLEDGE_AND_WEBSITE_USE). v1's failure: no field forces doctrine consumption —
KNOWLEDGE_AND_WEBSITE_USE is a reporting field satisfiable with "none", and FAILURE_PREVENTION
is free-form, so a weak model fills it from priors (GAP-02). v2 keeps all 12 sections and
changes three things:

### 3.1 New required section: DOCTRINE_DEVIATIONS

Placed after FAILURE_PREVENTION. One line per overridden default:
`<decision-id>: overridden because <verbatim brief clause>`. The literal value `none` is valid
**only** when every injected default was accepted. An override with no brief clause, or a
deviation that appears in the package body but not here, is a package defect. A deliverable
parameter fixed by the brief (aspect ratio, duration, placement, format) is itself a forcing
brief clause and takes precedence over any pack default it collides with: record the
collision here as an override citing the brief's parameter clause — never fabricate a
scene-based justification for a brief-fixed parameter.

### 3.2 FAILURE_PREVENTION becomes per-check-id

One line per injected check id (`PA-D1-check` … `CA-D11-check`, for the packs the trigger
table selected): `<check-id>: pass` or `<check-id>: fix: <what was changed to make it pass>`.
A missing check id is a package defect. Free-form additions remain allowed after the check-id
lines; they no longer substitute for them.

### 3.3 VISUAL_SYSTEM gains typed required subfields

The doctrine's questions map onto them; a weak model edits a slot, it does not compose from
principle:

| Subfield | Filled from | Content |
|---|---|---|
| `attention_order` | CA-D1 | 1st / 2nd / 3rd read, each with its single dominant cue |
| `surface_finish_per_key_object` | PA-D1 | object → matte/diffuse, glossy/direct, or glare |
| `implied_light_source` | PA-D2, PA-D4 | the one nameable fictional source and its direction |
| `placement_zone` | CA-D2, PA-D5 | subject zone + the stated reason (never a ratio) |

When a pack feeding a subfield was not injected (e.g. no product entity → no
`product_appearance`), the subfield takes the literal `not_governed_by_injected_doctrine`
rather than being omitted — absence must be distinguishable from neglect.

### 3.4 Section → pack map (v2, unchanged sections abbreviated)

OBJECTIVE_INTERPRETATION ← commercial_communication; CORE_CREATIVE_IDEA ←
concept_and_distinctiveness + commercial_communication; MESSAGE_AND_INFORMATION_HIERARCHY ←
commercial_communication + composition_and_attention + typography_and_copy; VISUAL_SYSTEM ←
composition_and_attention + colour_and_visual_register + typography_and_copy +
product_appearance; PRODUCTION_RECIPE ← product_appearance + camera_and_spatial_grammar;
GENERATION_PROMPTS ← projections of VISUAL_SYSTEM + PRODUCTION_RECIPE decisions;
DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS ← typography_and_copy + indian_indic_context (A14
absent → the standing Devanagari rule, carried verbatim in every pilot pack's limits);
AUDIO_AND_EDIT ← editing_pacing_and_short_form + camera_and_spatial_grammar;
FAILURE_PREVENTION ← every injected pack's check ids + critique_and_effectiveness;
KNOWLEDGE_AND_WEBSITE_USE ← the injected packs' cited ids; DELIVERABLE and
HARD_CONSTRAINT_CHECK ← the brief alone.

## 4. What this contract does not claim

No claim that forced consumption improves accepted-outcome rate — that is an unexecuted,
Controller-gated experiment (EVAL-038-shaped; no paid execution is authorised). No claim that
the ~300-token block or the v2 fields are calibrated: they are declared constraints with
stated rationale, tunable only by authorised later work. This document adopts nothing and
admits nothing; `coordination/CONTROL-STATE.md` governs.
