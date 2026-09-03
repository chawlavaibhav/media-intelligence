# Controller — CANON-SHAPE-v1 Adopted as the Governing Consumption Shape — 2026-09-01

**Status:** APPROVED CONTROLLER DECISION.
**Role:** Writer Controller.
**Target:** `canon/CANON-SHAPE-v1.md`, on `claude/canon-context-guidance-ohi1i9` (PR #83).

## Authority — the Controller's words

Put to the Controller: the settled shape of Canon for now — what Canon is, what it is for, and how
it is consumed.

Controller answer, session `session_01MTzh8gGKkyN31UruDXHcZo`:

> **"Let's stick with that"**

## Decision

`canon/CANON-SHAPE-v1.md` is **adopted as the governing shape and consumption contract for Canon**.
Its own status header said it becomes governing when the Controller merges the branch carrying it.
This decision is that adoption, effective on the merge of PR #83.

What adoption means:

1. **The consumption architecture in §4 is the shape Canon work is built against**: normalized
   request → deterministic pack lookup → one blueprint from a reasoning model with packs injected
   unconditionally as a stable cached prefix → pre-dispatch gate in code → cheapest verified
   generation route → post-draw gate in code → redraw until the gate passes → human acceptance →
   accepted blueprints as templates. The consuming model never decides whether to consult Canon.

2. **The forced-consumption receipt schema is retired as a production mechanism** (§5). It
   supersedes that part of `canon/compilation/INJECTION-CONTRACT-v0.md`. Compliance is verified
   mechanically by the gate; the model writes the plan only. Everything else in the tranche-A
   artifacts remains PROPOSED and is not adopted here.

3. **The rules listed as surviving in §5 continue to bind**: accepted Canon only, fail-closed on
   HOLD; render by id, never paraphrase; guard closure; computed confidence markers; conflicts
   stated with a resolution rule or marked unresolved; mandatory limit lines; O(1) per-request cost
   in corpus size; and a validator PASS establishes structure over committed bytes — never
   relevance, quality, outcomes or adoption.

4. **The document deliberately carries no verdict on whether Canon works, and adoption adds none.**
   That judgment is reserved to the Controller under
   `CONTROLLER-EVAL-038-AUTHORISATION-AND-DISPOSITION-2026-09-01.md`. Adopting a shape is not
   accepting a result.

## Standing

`coordination/CONTROL-STATE.md` remains the primary current-state surface and governs what is
authorised. `canon/CANON-SHAPE-v1.md` governs the *shape* Canon consumption takes when work is
authorised. Where the shape document and an older Canon packaging proposal disagree, the shape
document wins; where it and a newer durable Controller decision disagree, the decision wins.

## Not authorised by this decision

This decision **authorises no work**. In particular it does not authorise:

- building the pre-dispatch or post-draw gate (the shape document's §7 item 1 — the next build,
  when the Controller directs it);
- injection v1, cache-pricing pinning, or runner changes;
- the template library / empirical memory layer;
- compiling any further packs;
- any spend, provider call, or media generation;
- any acceptance-rate measurement;
- Production IR or Planner implementation;
- promotion of any still-PROPOSED artifact beyond the receipt-schema retirement stated above.

The open work listed in `canon/CANON-SHAPE-v1.md` §7 is a queue, not an authorisation. Each item
needs its own Controller decision.
