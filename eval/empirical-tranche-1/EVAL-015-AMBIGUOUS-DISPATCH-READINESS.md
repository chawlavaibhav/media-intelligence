# EVAL-015 — EMP-001 ambiguous dispatch accounting readiness

**Verdict:** `READY_FOR_SPEND_APPROVAL`

**Branch:** `work/eval-015-emp-001-ambiguous-dispatch` · **not merged**
**External provider/model/evaluator calls made by EVAL-015: 0**
**External spend: USD 0 / INR 0**

Evidence: [`VERIFICATION-PRE-SPEND.md`](VERIFICATION-PRE-SPEND.md), copied from fresh runs.
Supersedes [`EVAL-014-BUDGET-HANDOFF-READINESS.md`](EVAL-014-BUDGET-HANDOFF-READINESS.md), whose
verdict the Controller correctly rejected on B11–B12.

---

## The defect, stated plainly

EVAL-014's `_dispatch` caught **every** transport exception and called `release()`. That assumed
an exception proves the provider never saw the request. It does not: a read timeout, a connection
reset, a remote disconnect, a TLS failure or an unparseable reply can all happen *after* the
provider received and billed the call.

Releasing there broke two things at once — the ledger could record USD 0 for a call that cost
money, weakening a user-approved hard ceiling; and the attempt vanished from the evidence instead
of persisting as a trial. The Controller was right to block on it.

## The correction

One asymmetric rule, applied to both provider paths:

> **Release only when it is PROVABLE nothing was sent. Otherwise keep the money counted and keep
> the trial.**

| Class | Examples | Reservation | Trial |
|---|---|---|---|
| `PreDispatchRefusal` | missing key; refused body construction; blindness violation | **released** | none — no call was made |
| `AmbiguousDispatch` | read/socket timeout; connection reset; remote disconnect; TLS failure; connection abort; malformed response after send | **kept, settled at the reserved estimate** | **one**, with full identity |

Ambiguous calls persist `api_status` timeout/error, an explicit `error_class`,
`billing_state: unknown_provisional`, `cost_basis:
conservative_reserved_estimate_billing_unknown`, a resolvable ledger `cost_ref`, provider/model or
route identity, `trial_id`/`attempt_id`, and `retries: 0` — then the run **stops**.

`provider_request_id` may legitimately be `null` when the provider never answered. Trial and cost
identity still exist, so the call is countable and reconcilable against an invoice later.

## Requirement B — evaluator path evidence

- missing key ⇒ **0 dispatches**, reservation freed, ledger at USD 0;
- refused body construction (model mismatch) and blindness violation ⇒ **0 dispatches**, no spend;
- each of six injected post-dispatch failures ⇒ exactly **1** dispatch, spend **kept**,
  `ambiguous_dispatch: true`, one trial persisted, **0** retries;
- malformed response after send ⇒ same conservative handling, `error_class: malformed_response`;
- reopening the run reports the same spend — the headroom cannot be reclaimed;
- the ledger row itself carries `billing_state: unknown_provisional`;
- the conservative charge equals the reserved estimate, verified exactly;
- an ambiguous call still cannot push the tranche past USD 10 — with the sub-cap exhausted the
  call is refused *before* dispatch, so nothing is sent;
- qualification **stops** on the first ambiguous dispatch: 1 call, 1 persisted trial, no Latin leg.

## Requirement C — fal generation path evidence

- missing `FAL_KEY` ⇒ **0 dispatches**, reservation freed;
- each injected ambiguous failure ⇒ Attempt **persisted** with timeout/error, explicit error class,
  resolvable ledger `cost_ref`, route/slot/provider-surface identity, `billing_state:
  unknown_provisional`, `retry_of_attempt_id: null`;
- spend **kept** and attributed to the `atex` stage;
- **no evaluator call** — there is no artifact to look at;
- **no retry**, and the run **stops**: a failure on call 3 of 16 ends the run at 3, so 13 further
  paid generations do not follow a call nobody can account for;
- the measurement is an **absence**, not a mismatch — a generation that may not have happened did
  not produce wrong text, and `text_specific_stop_eligible` stays **false** rather than reading
  0-of-0 as evidence of failure;
- the same stop applies when generation succeeded and the **evaluator** call is the ambiguous one;
  both trials are preserved with their own costs;
- Registry untouched; result still non-promotable.

## Requirement D — no regression

315 → **363** tests, all passing. EVAL-014's cumulative USD 10 / USD 6 controls, the full 2,304
fake-live qualification, the 16-generation fake-live A-TEXT, and the cross-process rehearsal all
still pass unchanged. Latin gate still closed. Registry still empty. 13/13 baselines identical.

## What this still does not establish

The fake readers are **perfect**, so `16/16 exact matches` is a property of the fake. The
empirical floor is unchanged: **0 qualified models, 0 qualified evaluators, 0 Registry rows.**

EVAL-015 makes the *failure* accounting of the live transports correct. It does not make their
*success* path observed — they have still never been run against a provider. The first authorised
call remains their first real test.

## Remaining non-code prerequisites

1. **Explicit user approval** — USD 10.00 total / USD 6.00 qualification sub-cap / retries 0 / no
   account pre-funding above the ceiling. *Blocking.*
2. **Runtime secrets** — `OPENAI_API_KEY`, `GOOGLE_API_KEY`, `FAL_KEY`, plus a funded fal surface.
   If a provider demands a minimum deposit above the approved ceiling, **stop and return**. *Blocking.*
3. **Exact version pins at execution** — already mechanically enforced; `--live` refuses without
   `--openai-version` and `--gemini-version`. *Blocking.*
4. **Latin human perceptibility review** — unfilled, not fabricated, and it gates the whole A-TEXT
   screen. *Zero-spend, outstanding.*
5. **Rebuild the gitignored image sets** before running (~30s, free).

None is a code change.

## Confirmation

- External provider/model/evaluator calls made by EVAL-015: **0**
- External spend: **USD 0 / INR 0**; no account funded, no terms accepted, no credit consumed
- No real API key used anywhere — every key is the literal `REHEARSAL-NOT-A-REAL-KEY`
- Capability Registry empirical rows: **0**, byte-identical throughout
- 13/13 protected baselines byte-identical; Devanagari battery read, never written
- USD 10 ceiling, USD 6 sub-cap, retries 0, candidates, prompts, thresholds, routes, A-TEXT items,
  repeats, Latin requirement and scientific architecture: **all unchanged**
- EVAL-012, EVAL-013 and EVAL-014 work preserved
- Branch pushed, **not merged**
