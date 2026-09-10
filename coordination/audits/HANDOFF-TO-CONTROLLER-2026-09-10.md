# Handoff to the Controller — 10 September 2026

**Read this file first. It is the only entry point.** Everything below it is evidence.

Written by the second auditor after: a full independent audit of `main` at `dcfa6af`, nine zero-spend
repairs, and the first two lanes of the production runtime. A parallel auditor produced its own report,
which is kept here whole and reconciled against this one.

**Nothing in any of this decided anything.** Fifteen rulings are waiting, all of them free.

---

## 1. Where the work is

Four branches. None is merged. None was pushed by the auditor.

| Branch | Head | What it carries |
|---|---|---|
| `work/audit-b-zero-spend-fixes` | `850003f` | Both audit reports, the cross-audit reconciliation, the decision sheet, four re-runnable audit tools, the taint register, and nine mechanical repairs. 362 tests OK. |
| `work/runtime-v0-contracts` | `81bbdd4` | The four frozen production contracts, v0 and v1, plus the record of thirteen defects found by using them. |
| `work/runtime-v0-spec-canon` | `e278331` | Lane PC-03A: customer brief → Production Specification, with deterministic Canon lookup. 85 tests OK. |
| `work/runtime-v0-router` | `46efdd5` | Lane PC-03B: the evidence-aware router. 41 tests OK. |

Merge order, if they are merged: audit branch first (the taint register and the repaired ledger are
inputs to everything else), then contracts, then the two lanes.

---

## 2. Read in this order

**Five minutes** — `AUDIT-2026-09-10-CONTROLLER-DECISIONS.md`. Fifteen rulings on one page, each with
its options and its consequence. This is the only file that asks you for anything.

**Thirty minutes** — add `README.md` in this directory (what the two audits agree on, where they
differ, and what was repaired), then `AUDIT-2026-09-10-REPORT-B.md` Parts 1 to 3.

**Everything** — `AUDIT-2026-09-10-REPORT-A.md` (the parallel auditor, including its T0–T8 programme),
`AUDIT-2026-09-10-EVIDENCE-RECOMPUTE.md`, `AUDIT-2026-09-10-SPEND-RECONCILIATION.md`, and
`runtime/contracts/CHANGES-v0-to-v1.md`.

---

## 3. What is true

Verified by re-computation, not by reading a summary:

- **All 311 sealed media files re-hash exactly**, on disk, in the real checkout. Nothing sealed has
  been modified since it was sealed, anywhere in git history.
- **575 Registry rows, validator passes**, every row deterministic and carrying the frozen criteria
  fingerprint. Two runs' rows were rebuilt from the sealed bytes and came out byte-identical.
- **The routing map regenerates identically** — 61 cells — from the Registry and the verdicts. It was
  not hand-edited.
- **All 81 price pins verify**: files, byte counts, fingerprints, and the quoted price present in the
  bytes.
- **Both image-round blind commitments re-compute correctly** from the off-repo keys.
- **Every per-route number** in the summaries and the audit index is true: 10/12, 8/8, 5/7, 6/6, 4/4,
  0/5, 11/16 — all of it checks out.
- **362 tests pass** after the repairs (326 before).

## 4. What was corrected

- **The spend total was wrong.** Not USD 110.7. The ledgers say **USD 119.085** consumed, plus **USD
  3.156** for the judge run = **USD 122.241** counted against caps. Of the ledgered amount, **USD
  108.971 produced an artifact and USD 10.115 produced nothing**. Vendor-billed is unknown and is not
  in this repository.
- **Two caps were crossed** at the level you sign them: video piece 1 (10.364 against 9.96) and the
  Wan 2 round (11.840 against 11.53). The mechanism that let it happen is repaired.
- **Both auditors were wrong about the judge.** `calls: 206` is a row count from an offline rebuild.
  At most 190 calls were sent against 200 authorised. **No breach.** Two auditors agreeing was not
  corroboration — it was the same weak signal read twice.
- **`PROJECT-MEMORY.md` said the Registry was empty.** Corrected; it still predates the whole two-day
  run and needs a Governor refresh.

## 5. The four rulings that unblock the most

Fifteen are waiting. These four move the most:

1. **C-4 and C-6b** — how duplicated and re-sent draws count. Between them they hold **13 of the 21
   blocked evidence cells**, including five of the six base-image routes. Nothing is wrong with that
   evidence; it is held by paperwork, and ruling costs nothing.
2. **C-6c** — the exact-text cell collision. It blocks the code-set-text mechanism, which is the
   cheapest exact-text path the project has and the core of the first production wedge.
3. **C-6b again** — it alone decides whether RR-16 survives. If a failed draw stays a failure, "Wan
   2.2 A14B is the cheap Wan tier for image-to-video" cannot stand.
4. **C-2** — read the four provider statements once. Until then the project has an upper bound on its
   costs, not its costs, and every price quoted later rests on that number.

## 6. Where the product actually stands

**16 of 61 evidence cells can be routed automatically today.** A six-second motion job from an
accepted still routes end to end with a declared fallback. A static ad with an exact price line, and
an edit of a customer photograph, both select a sensible route but fall back to manual — **not because
the route is bad, but because there is no second usable route**, and a profile that requires a
fallback refuses to proceed without one.

That is the single most useful sentence in this handoff: **the first alpha needs a second usable route
far more than it needs a better first one.** C-4 and C-6b supply most of them for free.

Still missing, unchanged by any of this work: no intake for a customer, no repair loop, no measured
cost per accepted outcome, and nothing commercial — no terms, no output-rights position, no provider
resale review, no refund policy.

## 7. Verify any of it yourself

From a clean checkout of the audit branch:

```
cd eval/harness-v2 && python3 -m unittest discover -s tests -p 'test_*.py'   # 362 OK
python3 eval/registry/validate_registry.py                                   # PASS, 575 rows
python3 coordination/audits/tools/reconcile_spend.py                         # the four-column spend table
python3 coordination/audits/tools/recompute_elimination.py                   # the literal elimination arithmetic
python3 coordination/audits/tools/verify_price_pins.py                       # 81 pins
python3 coordination/audits/tools/build_taint_register.py --check            # register vs map fingerprint
```

## 8. What I would not do next

Both auditors independently reached the same list: do not re-run Stage A, do not compile the other
eight Canon packs, do not chase a better automatic judge yet, do not widen every two-draw cell for
neatness, and do not build a general planner before the first vertical slice is finished.

Thirteen contract defects were found in two rounds of building. **Not one was found by reading a
contract.** Every one was found by building something that had to use it.
