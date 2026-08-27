# Project Contract

**Part of every session's default bootstrap — see `coordination/RUNBOOK.md` for the full order**
(`PROJECT-MEMORY.md` → `coordination/CONTROL-STATE.md` → this file →
`shared/COMMUNICATION-STANDARD.md` → `shared/CONTEXT-SUFFICIENCY-POLICY.md`).
Not autonomously rewritten by workers — proposals go through `PROPOSED-INTEGRATION-CHANGE-<ID>.md` in the proposing stream's folder.

## Communication and epistemic standard

`shared/COMMUNICATION-STANDARD.md` applies to every worker, every stream, the Controller, reports and chat.

Core rules:
- explain in plain English without removing technical substance;
- use the minimum wording needed to stay complete and correct;
- avoid wall-of-text responses when structure would make them easier to read;
- never invent facts, evidence, repository state, licences, costs, capabilities or decisions;
- keep observed/source-supported facts separate from inference, recommendation and unknowns.

A worker must acknowledge this standard once at the start of a new session or after the standard changes. If it cannot read the standard, it must stop rather than claim compliance.

## Product goal

An API-native media production intelligence layer: not a new foundation model, a system that sits
between a customer's intent and the ecosystem of image/video/audio tools, and continuously chooses
the cheapest reliable path to a commercially acceptable outcome. Primary metric, long-term: **Cost
per Accepted Outcome**, not cost per generation.

## High-level flow

```
CUSTOMER INPUT
    ↓
NORMALIZED REQUEST
    ↓
CREATIVE INTELLIGENCE + CANON
    ↓
CREATIVE IR
    ↓
PRODUCTION PLANNING / ROUTING  ←  CAPABILITY REGISTRY
    ↓
IMAGE / VIDEO / AUDIO TOOLS
    ↓
EVALUATION (technical + creative)
    ↓
REPAIR
    ↓
ACCEPTED MEDIA OUTCOME  →  EMPIRICAL MEMORY
```

## Three workstreams

**Canon** — durable creative and media expertise: what a good outcome must accomplish, what
techniques exist, how to plan without overriding customer intent, what to inspect to judge fitness
for an objective. Cookbook + culinary school + tasting expertise. **Does not** know which current
model is best, provider quirks, prices, or drift rates.

**Eval / Capability Lab** — what should be measured and how, and what current models/workflows can
actually do, measured empirically. Produces the Capability Registry. **Does not** invent creative
quality from first principles — Canon supplies the dimensions worth measuring.

**Resources** — independent media and data for testing ideas: dataset discovery, licensing,
sampling, manifests, integrity. **Does not** define Canon truth or pick examples because they
flatter a hypothesis. Keeps evaluation media separate from the knowledge being tested, to avoid
circular results (books teach hierarchy → pick hierarchy examples → Canon "wins").

## Core objects

**Normalized Request** — conservative record of what the customer said. Never overwritten.
**Creative IR** — what should exist: objective, audience, hierarchy, constraints, acceptance
contract. Model-independent.
**Production IR** — how today's tools should create and verify it. Does not exist yet.
**Capability Registry** — current, versioned, empirically measured model/workflow ability.
**Production Planner** — combines Creative IR requirements with the Registry to route a job.

## Major separations (do not reopen without an approved integration task)

1. Normalized Request ≠ Creative IR.
2. Creative IR ("what") ≠ Production IR ("how, today").
3. Source Knowledge ≠ current Operational/Product Bindings.
4. What a source teaches ≠ how current software uses it.
5. Book/source knowledge ≠ empirical model capability.
6. Capability Registry is empirical, never inferred from books.
7. Source terminology is preserved; the ontology maps, never silently rewrites.
8. Evidence and provenance stay explicit; no invented decimal confidence.
9. Public dataset labels are one source's observations, not our ground truth.
10. A worker's recommendation is not an approved decision.
11. Canon does not select current providers/models. Routing = requirements (Canon) + Registry (Eval).
12. Physical-production advice from books is not auto-translated into generative-model instructions.
13. Failure logging permits multiple defects per output.

## Authority

Controller (human, strategic): product direction, architecture, major experiments, accepting or
rejecting assumptions, scope changes, schema changes, milestones. **The Controller merges.**

Repository Governor (fifth, independent role — approved 25 Aug 2026): repository coherence, the
canonical `PROJECT-MEMORY.md`, per-task integrity review and periodic repository-health audits. It
does **not** own project strategy or any stream's methodology, and it may write only
`PROJECT-MEMORY.md`, `governance/**`, and status/supersession corrections in `coordination/**` when
an approved governance task includes that scope. It flags and routes domain-owned defects rather
than fixing them. Contract: `governance/GOVERNOR-CONTRACT.md`; approved design:
`docs/superpowers/specs/2026-08-25-repository-governor-project-memory-design.md`.

Workers (execution): research, ingest, implement, run *approved* experiments, script, collect,
analyse, report evidence, recommend. **Never** redefine the product, promote a recommendation to a
decision, expand scope on their own judgement, silently change cross-stream architecture, touch
another stream's ownership, or rerun a mutated experiment and report it as the original.

## Approval requirements

Architecture changes, curriculum approval, new benchmark dimensions, material budget changes, and
anything a CHARTER marks `DECISIONS REQUIRING CONTROLLER REVIEW` — human only.
