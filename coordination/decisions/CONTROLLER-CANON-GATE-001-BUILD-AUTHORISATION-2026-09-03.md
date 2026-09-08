# Controller — CANON-GATE-001 Build Authorisation — 2026-09-03

**Status:** TASK AUTHORISED.
**Role:** Writer Controller.
**Branch:** `work/canon-gate-001`.

## Authority

The Controller was asked whether to build the gate — the next build named in
`canon/CANON-SHAPE-v1.md` §7 item 1 — and answered:

> **"Go ahead."**

This is that authorisation. It opens one task. It renews no spend authority.

## What is authorised

**CANON-GATE-001 — build the compiled-doctrine gate as code.** Derive the pre-dispatch and
post-draw inspections from the committed check lines of the two compiled packs (PA-D1..PA-D10,
CA-D1..CA-D11), baked-text scan first. The gate is the third of the three places
`canon/CANON-SHAPE-v1.md` §4 allows Canon to touch the pipeline.

Boundary conditions, all binding:

1. **USD 0. Zero provider calls.** No model call, no generation, no paid OCR. Any text-detection
   capability is built as a pluggable interface with an offline detector; a paid detector may be
   *wired* but must not be *invoked*, and invoking one needs a separate spend authorisation.
2. **Render by id, never paraphrase.** Every check implemented must trace to a committed
   `check_id` in a compiled pack. A check with no committed source is invented doctrine and is
   forbidden.
3. **Never convert an unrun check into a pass.** A doctrine check line that cannot be mechanised
   must be reported as not mechanised, with its reason — never silently omitted and never counted
   as satisfied. Silent coverage gaps are the defect this rule exists to prevent.
4. **A gate PASS establishes structure, never quality.** It must say so in its own output, in the
   repo's existing idiom. The gate does not decide whether Canon works.
5. **Accepted Canon only, fail-closed on HOLD.** No HOLD id may reach the gate's rule set.
6. **No frozen or historical artifact is modified.** EVAL-038 evidence is read-only input.
7. **Stdlib only**, matching the repo's existing test convention (`python3 -m unittest`).

## How it is to be built — maker/checker, three separate roles

The Controller does not implement. Three agents, in sequence, each with its own context:

| Role | Does | Must not |
|---|---|---|
| **Planner** | Reads the doctrine and the repo, writes the implementation plan: which check lines mechanise, how, which do not and why, module layout, test strategy | Write implementation code or tests |
| **Maker** | Executes the approved plan under test-first discipline; reports what it built and what it could not | Change the plan's scope on its own authority; mark its own work verified |
| **Checker** | Independently verifies against the plan and the doctrine; runs the tests itself; adversarial review | Fix what it finds — it reports, the Controller routes |

The Controller reviews the plan before the maker starts, and the checker's verdict before anything
merges. **No agent may approve its own work.**

## Not authorised by this decision

- any spend, provider call, or media generation;
- injection v1, cache-pricing work, or runner changes;
- the template library / empirical memory layer;
- compiling any further pack;
- any acceptance-rate measurement;
- any conclusion about whether Canon works — that verdict remains reserved to the Controller
  (`CONTROLLER-EVAL-038-AUTHORISATION-AND-DISPOSITION-2026-09-01.md`);
- merge to `main` — that is a separate Controller act after the checker reports.
