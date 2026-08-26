# Frozen planning prompt — Canon V1 early value gate

**FROZEN 26 Aug 2026. Identical for both arms.** The only difference between the Generic arm and the
Oracle Canon arm is the text substituted into `{{CONTEXT_BLOCK}}`. Nothing else varies — not the
instructions, not the ordering, not the output format, not the wording.

Changing this file after any output has been generated is experiment mutation and invalidates the
run. If it must change, the run restarts.

---

```
You are planning a commercial media production for a client. You will be given the client's brief
and a block of craft guidance. Produce a production plan.

Work only from what the brief actually says. Where the brief is unclear, incomplete or
self-contradictory, say so explicitly rather than resolving it silently. Do not invent facts about
the client, the product or the audience.

CLIENT BRIEF
------------
{{CUSTOMER_BRIEF}}

CRAFT GUIDANCE
--------------
{{CONTEXT_BLOCK}}

PRODUCE A PLAN WITH THESE SECTIONS
----------------------------------
1. OBJECTIVE — what this piece has to achieve, and for whom.
2. CORE PROPOSITION — the single thing the audience should take away.
3. HIERARCHY — what must be noticed first, second and third, and why in that order.
4. EXPLICIT CLIENT REQUIREMENTS — every requirement the client actually stated, listed exactly,
   including any copy that must appear verbatim. Do not paraphrase these.
5. CONFLICTS AND GAPS — anything in the brief that contradicts itself, is missing, or cannot be
   satisfied as stated. For each, say what you propose and why, or what you would need to know.
6. VISUAL OR TEMPORAL STRATEGY — how the piece is constructed. For video, the shot progression.
7. TRADE-OFFS — where two things you would want cannot both be had, which you chose and what it
   costs.
8. WHAT TO INSPECT — how someone would judge whether a finished version of this succeeded.

Be specific. A plan that would apply equally to any other brief is not a plan.
```

---

## Substitution rules

| Placeholder | Generic arm | Oracle Canon arm |
|---|---|---|
| `{{CUSTOMER_BRIEF}}` | the brief's `customer_brief` field, identical in both arms | identical |
| `{{CONTEXT_BLOCK}}` | `generic-contexts/<brief_id>.md` | `oracle-contexts/<brief_id>.md` |

**`authoritative_intent` is never substituted into either arm.** It is scoring material. A run that
exposes it to a planning arm is void.

## Why the section list is identical for both arms

The experiment asks whether Canon improves planning *given the same procedure*. If the Canon arm were
also given a better output structure, a win could not be attributed to the Canon. The structure is
therefore held constant and only the knowledge varies.

## Model and execution

Deliberately unspecified here, and **not executed tonight**. Whatever is used must be:

- the same model, version and settings for both arms;
- run with both arms of a brief in the same session batch, so provider-side drift cannot fall
  unevenly on one arm;
- recorded per output — model, version, settings, timestamp — in the run record.
