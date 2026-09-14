# INJECTION-PREFIX v1 — the receipt-free system block (runtime-owned)

STATUS: runtime data, built under Controller ruling C-10 (14 Sep 2026): "Authorise USD-0
implementation of: Canon Injection v1; template / empirical-memory integration."
Shape authority: `canon/CANON-SHAPE-v1.md` §4–§5 (adopted 2026-09-01). The v0 block it replaces
lives in `canon/compilation/INJECTION-CONTRACT-v0.md` §2 and is NOT edited; `CanonCorpus(
injection_version="v0")` still reads it byte-for-byte.

The fenced block below is what `runtime/canon/packs.py` injects once, before any pack text, as
the first bytes of the cache-served prefix. The runtime reads the FIRST fenced block in this
file and nothing else; keep it first.

```
CANON_DOCTRINE packs are compiled production decisions from an audited corpus. Each
DEFAULT is a decision already made: accept it, or override it — legal only when a specific
brief clause forces it. Never re-arbitrate a PRE-ARBITRATED CONFLICT: the stated rule
decides. A conflict rule inherits the confidence marker and override path of its
decision_ref. Write the plan only: every CHECK is verified mechanically by a code gate after
the plan is written, so no compliance receipt, deviation list or pass/fix line is asked for.

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

## Size

The fenced block is **1,311 chars = 328 tokens** at the repo's estimate (tokens = ceil(chars / 4);
recompute: extract the fenced block, `ceil(len/4)`). The trigger table
(`canon/packs/pack-triggers-v0.yaml`) budgets the system block at `system_prompt_block_tokens: 340`;
v1 is 12 tokens under it, and `runtime/tests/test_h_injection_v1.py` holds it there. The v0 block
was 1,354 chars = 339 tokens.

## What changed against v0 §2, sentence by sentence

CANON-SHAPE-v1 §5 retires the forced-consumption receipt schema: "The gate verifies mechanically;
the model writes the plan only." Every instruction that told the model to write proof back is gone.

Removed (receipt / forced-consumption instructions):

1. From the DEFAULT sentence, the clause "— record it in DOCTRINE_DEVIATIONS with that clause".
   The override rule itself survives: an override is legal only when a specific brief clause
   forces it. What is gone is the demand to write it down in a receipt field.
2. From the conflict-rule sentence, the clause ": a DOCTRINE_DEVIATIONS entry on that decision id
   covers its conflict rules". The inheritance rule (a conflict rule takes its decision's marker and
   override path) survives.
3. The whole sentence "Answer every CHECK by decision id in FAILURE_PREVENTION as pass or fix:
   <what changed>." — the per-check receipt line.

Added (one sentence, the mechanical-verification statement):

- "Write the plan only: every CHECK is verified mechanically by a code gate after the plan is
  written, so no compliance receipt, deviation list or pass/fix line is asked for."

Kept verbatim: the opening sentence, the "never re-arbitrate a PRE-ARBITRATED CONFLICT" rule, and
the entire marker legend (a test compares it character-for-character against the v0 legend).

## What this block cannot fix on its own (OBSERVED, 14 Sep 2026)

The two compiled packs' `terse_injection_text` (canon-owned, byte-stable, validated by
`canon/validation/validate_compiled_pack.py`) still open with the v0 receipt sentence ("override it
in DOCTRINE_DEVIATIONS … Answer every CHECK in FAILURE_PREVENTION as pass or fix") and PA-D10 /
CA-D9 / CF-06 name DOCTRINE_DEVIATIONS in their own text. The runtime does not rewrite pack bytes
(render by id, never paraphrase — CANON-SHAPE-v1 §5), so those words still reach the prefix through
the packs. The lookup records this as a notice (`CanonLookup.notices`) naming the packs, and
`receipts_required` is `False` regardless: the gate does not read receipts and nothing downstream
asks for them. Removing the words for good is a pack recompilation, which is canon-owned and not
authorised by C-10 ("Do NOT compile the remaining eight packs" — and recompiling the two is a
Canon-stream decision, not a runtime one).

## Cache boundary

Nothing request-specific sits upstream of the cache breakpoint (COMPILED-PACK-CONTRACT-v0.1 §4).
The prefix is: this block, then (audio only) the trigger table's coverage-gap notice, then the
selected accepted packs' terse text in canonical order, joined with a blank line. The Normalized
Request follows as the first user-turn content. `CanonLookup.cache_boundary_marker` names the
boundary as metadata; the marker string is never injected. Cache-read pricing is **not pinned**
(CANON-SHAPE-v1 §6, "cache-read pricing, to be pinned"); no cost claim rests on it.
