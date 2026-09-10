# `runtime/` — the production path

This tree is the **product**. `eval/` is the laboratory. They are deliberately separate: a Capability
Lab run produces evidence, a runtime job produces a customer deliverable, and neither writes into the
other's records.

Four contracts are frozen here before any runtime worker starts, so that parallel workers agree on
the objects they hand each other:

| Contract | The question it answers |
|---|---|
| `PRODUCTION-JOB-v0.yaml` | What did the customer ask for, and under what limits? |
| `PRODUCTION-SPEC-v0.yaml` | What exactly must be made, and what must be true of it? |
| `ROUTE-DECISION-v0.yaml` | Which route will make it, why that one, at what price, and what happens if it fails? |
| `OUTCOME-EVENT-v0.yaml` | What actually happened, once, immutably. |

## Two rules that shaped every field below

**1. Nothing here encodes a product limitation.** Scope choices for the first alpha — one static ad,
one optional short motion version, two provider draws — appear as *values in a policy profile*, never
as constants in a schema or in code. A later profile that allows multi-scene work, audio, more draws
or a different deliverable is a configuration change, not a redesign. Where a schema field could have
been written as a fixed enum it is written as an open vocabulary with a named registry, so adding a
deliverable never requires editing a contract.

**2. Nothing here inherits the Lab's evidence weaknesses silently.** A route may be selected
automatically only if the evidence behind it is marked usable for production; otherwise the decision
says `manual_route_required` and a person chooses. The runtime reads an evidence *status*, never a
score, and never a cost figure it treats as a price without a live price pin.

## Status

`v0`, frozen at this commit as the base every runtime lane branches from. Changing a `v0` field is a
new version, never an edit in place — the same rule the Lab uses for its frozen packages.
