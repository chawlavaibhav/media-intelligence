# EVAL-014 — EMP-001 budget continuity and paid-handoff readiness

> **SUPERSEDED — 27 Aug 2026.** The Controller rejected this `READY_FOR_SPEND_APPROVAL` verdict in
> `coordination/decisions/CONTROLLER-EVAL-014-REVIEW-2026-08-27.md` on B11–B12: an ambiguous
> transport exception could release its reservation, manufacturing spend headroom and erasing an
> attempted call. The work below stands and was preserved. Current verdict:
> [`EVAL-015-AMBIGUOUS-DISPATCH-READINESS.md`](EVAL-015-AMBIGUOUS-DISPATCH-READINESS.md).


**Verdict:** `READY_FOR_SPEND_APPROVAL`

**Branch:** `work/eval-014-emp-001-budget-continuity` · **not merged**
**External provider/model/evaluator calls made by EVAL-014: 0**
**External spend: USD 0 / INR 0**

Evidence: [`VERIFICATION-PRE-SPEND.md`](VERIFICATION-PRE-SPEND.md), copied from fresh runs.
Supersedes [`EVAL-013-LIVE-PATH-READINESS.md`](EVAL-013-LIVE-PATH-READINESS.md), whose verdict the
Controller correctly rejected on B6–B10.

---

## The five blockers, closed

| | Blocker | Correction | Fresh proof |
|---|---|---|---|
| **B6** | tranche spend not cumulative across processes | durable ledger keyed by RUN id, reconstructed from disk on every read | process A spent USD 0.9763200 and exited; process B reconstructed exactly that, not USD 10 |
| **B7** | USD 6 evaluator sub-cap not mechanically enforced | stage caps enforced in one place, independent of the authorisation file | qualification refused at 6.00 with tranche headroom still available |
| **B8** | A-TEXT paid CLI unconditionally refused | fingerprint-bound handoff; `--live` and `--fake-live` share one code path | 16 generations + 16 evaluator dispatches from a persisted qualification, in a separate process |
| **B9** | evaluator calls lacked durable trial/cost identity | deterministic trial id + ledger-resolvable cost_ref per dispatch | 2,304 dispatches → 2,304 unique trial ids and 2,304 resolvable cost refs |
| **B10** | A-TEXT blind check not target-aware | `blind_check_target` evaluator-side only | leak controls on a Devanagari item *and* a Latin one |

## Requirement A — persistent cumulative budget

All six required controls pass, and each is paired with the failure it prevents:

1. process A spends USD 5.75 and closes; process B sees USD 4.25 headroom, not USD 10;
2. qualification is refused at its USD 6 sub-cap while the tranche still has room;
3. A-TEXT is refused when qualification + A-TEXT would break USD 10;
4. deleting **and replacing** the authorisation file does not erase prior spend — permission and
   history are different facts, and spend is keyed to the run;
5. an outstanding reservation blocks a second writer, so two processes cannot be told the same
   headroom is free; a released reservation returns it;
6. a corrupt line, missing amount, **sequence gap**, unknown record type, shrunken file or missing
   run record all fail closed rather than returning a best guess.

Corrections are additive with an explicit type and reason. A negative correction is refused
outright — subtracting from recorded spend is how a ceiling quietly acquires headroom nobody
approved.

## Requirement B — durable one-call-one-trial evidence

Every live evaluator dispatch carries `trial_id`, `attempt_id`, `cost_ref`, provider, model alias,
resolved version, script, item, shape, pass index, provider request id, API status / refusal /
error, `retries: 0` and `evidence_mode`.

The trial id is **deterministic** — run, provider, exact resolved version, script, item, shape,
pass — rather than a counter, so a resumed process gives the same call the same id and a duplicate
is visible as a duplicate rather than looking like a new trial.

Proved at frozen full scale: 2,304 dispatches → 2,304 unique trial ids, 2,304 cost refs, all
resolving to rows in the persistent ledger.

## Requirement C — real qualification → A-TEXT handoff

`run_atex.py --live` is executable when given genuine inputs. It refuses when:

- no qualification exists for this run, or it belongs to a different run;
- its declared mode does not match A-TEXT's — a rehearsal may not open a paid stage, and a paid
  stage may not be scored against rehearsal evidence;
- the evidence is marked synthetic;
- **the fingerprint does not match** — the claim is bound by SHA-256 to the call records behind
  it, so widening `qualified_scope` by hand changes the fingerprint and the handoff refuses;
- no candidate is qualified for **every** script the four frozen items need;
- the Latin human perceptibility gate is unresolved;
- the tranche has no headroom left.

The rebuilt judge binds to the exact provider, alias and resolved version that qualified, opens the
provider-correct transport, spends on the same persistent tranche budget, and instantiates only the
two frozen fal routes. Generation and evaluator calls carry separate ledger cost refs.

### One consequence worth stating plainly

ATEXT-03 and ATEXT-04 are Latin. A-TEXT therefore needs a judge qualified on **both** scripts, so
**the unresolved Latin perceptibility review gates the entire A-TEXT screen, not half of it.** The
rehearsal demonstrates this: step 6 runs A-TEXT against the committed unfilled sheet and is
refused, before step 7 shows the far side of the gate with a clearly-labelled temporary fixture.

## Requirement E — cross-process rehearsal

`rehearse_cross_process.py` spawns real interpreters. Measured across the boundary:

```
qualification USD 0.9763200  +  A-TEXT USD 0.9142480  =  USD 1.8905680 of 10.00
2,336 spend records; all cost refs and trial ids unique
retries 0 · 16 generations (8+8) · Registry rows 0 · evidence non-promotable
```

## What none of this establishes

The fake readers are **perfect**. A perfect reader is not a real one, and `16/16 exact matches` is
a property of the fake. The empirical floor is unchanged: **0 qualified models, 0 qualified
evaluators, 0 Registry rows**, and no accepted evidence that Canon improves model outcomes.

The live transports have **never been run against a provider**. Their URLs, headers and bodies are
asserted against documented contracts, not observed responses. The first authorised call is also
their first test, and it should be budgeted as such.

## Remaining non-code prerequisites

1. **Explicit user approval** — USD 10.00 total / approximately ₹954, qualification sub-cap USD
   6.00, retries 0, no account pre-funding above the ceiling. *Blocking.*
2. **Runtime secrets** — `OPENAI_API_KEY`, `GOOGLE_API_KEY`, `FAL_KEY`, plus a funded fal surface.
   If any provider demands a minimum deposit above the approved ceiling, **stop and return**. *Blocking.*
3. **Exact version pins at execution** — `--live` refuses without `--openai-version` and
   `--gemini-version`; a judge refuses to exist without a resolved version. *Blocking.*
4. **Latin human perceptibility review** — still unfilled, still not fabricated, and it gates the
   whole A-TEXT screen. The mechanical half is done: all 48 mismatches differ after NFC *and* in
   decoded pixels. That proves a difference is on the page; it does not prove a person would
   notice it. *Zero-spend, outstanding.*
5. **Rebuild the gitignored image sets** before running (~30s, free).

None of these is a code change.

## Confirmation

- External provider/model/evaluator calls made by EVAL-014: **0**
- External spend: **USD 0 / INR 0**; no account funded, no terms accepted, no API credit consumed
- No real API key was used; the rehearsal uses the literal string `REHEARSAL-NOT-A-REAL-KEY`
- Capability Registry empirical rows: **0**, byte-identical throughout
- 13/13 protected baselines byte-identical; Devanagari battery read, never written
- Frozen scope, roster, thresholds, prompts, routes, repeat counts, four A-TEXT strings, USD 10
  ceiling, USD 6 sub-cap, 0 retries and the 16-generation cap: **all unchanged**
- EVAL-012 and EVAL-013 work preserved; runtime spend state is gitignored and uncommitted
- Branch pushed, **not merged**

## Would approval + secrets + version pins now start EMP-001 with no further code change?

**Yes for qualification, and yes for A-TEXT once the Latin review is complete.**

Qualification runs end to end with no code change. A-TEXT then consumes the persisted
qualification, rebuilds the same pinned judge and runs the frozen routes — again with no code
change — but it will correctly refuse until the Latin perceptibility review is filled in by a
person, because two of the four frozen items are Latin.

The honest caveat is unchanged from EVAL-013: no code change is *known* to be needed for the live
transports, but whether one *turns out* to be needed is what the first authorised call will reveal.
