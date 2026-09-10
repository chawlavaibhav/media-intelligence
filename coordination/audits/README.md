# `coordination/audits/` — the 10 September 2026 audit set

Two auditors reviewed `main` at `dcfa6af` independently, on the same day, without seeing each
other's work. Both reports are kept whole. Nothing here decides anything: an audit reports, the
Controller rules.

| File | Who | What it is |
|---|---|---|
| `AUDIT-2026-09-10-REPORT-A.md` | Auditor A | Findings F-01…F-11 plus a full Controller programme, T0 to T8, from here to public rollout. Copied in verbatim from the auditor's own session; not edited. |
| `AUDIT-2026-09-10-REPORT-B.md` | Auditor B | Findings F-1…F-16, a verdict per audited section, the decision list, and a nine-step rollout plan. Every number re-computed locally. |
| `AUDIT-2026-09-10-EVIDENCE-RECOMPUTE.md` | Auditor B, executor pass | The literal re-computation of the elimination rules and the quarantine list. |
| `AUDIT-2026-09-10-SPEND-RECONCILIATION.md` | Auditor B, executor pass | One spend table per run, four columns, and what still cannot be known from the repository. |
| `tools/reconcile_spend.py` | — | Rebuilds the spend table from the sealed ledgers. Read-only, no network. |
| `tools/recompute_elimination.py` | — | Rebuilds the elimination arithmetic from the sealed attempts under the literal frozen rule. Read-only, no network. |

## Where the two auditors agree

These findings appear in both reports, reached separately. Treat them as settled facts.

| Fact | A | B |
|---|---|---|
| Video piece 1 consumed ≈ USD 10.364 against a USD 9.96 cap | F-05 | F-1 |
| The Wan 2 round consumed ≈ USD 11.84 against its final USD 11.53 cap | F-06 | F-1 |
| The published spend total does not reconcile with the ledgers (≈ USD 119.1 before the judge run, not USD 110.7) | F-09 | F-2 |
| ~~The vision judge recorded 206 calls against a 200-call authority~~ **— BOTH AUDITORS WERE WRONG, corrected 10 Sep 2026: `calls: 206` is a row count from an offline rebuild; only 190 of the 210 screened rows carry any evidence of a call, so at most 190 calls were sent against the 200 authorised. No breach.** | F-04 | F-4 |
| Smoke runs reused production trial identities, giving some routes an uncounted extra draw | F-03 | F-8 |
| E1/E2 were not applied exactly as frozen; some elimination numbers are product learning, not pre-registered results | F-02 | F-6 |
| The composite authorisation became durable evidence only after the calls it covers | F-07 | F-11 |
| `CONTROL-STATE` carries stale intermediate state | F-08 | F-5 (extended to `PROJECT-MEMORY.md`) |
| EVAL-040 proves nothing causal about Canon — there was no arm without Canon | §5 | F-16 |
| The deterministic Registry evidence is clean and is not affected by any of the above | §3 | Section C |

**A correction both auditors owe the record.** The judge "breach" above was reported independently by both
and is not real. Two auditors agreeing is not evidence; it means the same weak signal was read the same way
twice. The underlying defect was real — a live run kept no authoritative call counter, so a rebuilt report
printed a different number with no way to tell them apart — and that is what has been fixed.

## Where they differ, and why

1. **The package rebuild.** A recorded the package-basis invariant as PASS but could not run the
   rebuild. B ran it: every generated file rebuilds identically **except one provenance line** in
   `COST-TABLE.yaml`, which names the previous roster commit and says the working tree did not match
   HEAD. All prices are identical. (B, F-10.)
2. **Price pins.** A sampled ten routes. B checked all 42 pinned pages mechanically — file, byte
   count, fingerprint and the quoted price string inside the bytes — and found two of the judge's
   own quotes are not literal substrings, and that the "1,548 tokens per image" figure used in the
   judge's cost is not in the pinned bytes. (B, F-12.)
3. **Blindness.** Both note the sequence is sound. B adds the distinction that matters: the two
   image rounds carry a real salted commitment whose value B re-computed from the off-repo keys and
   confirmed, while every video and audio round has no commitment (`commitment_verified: false`) and
   the blind copies the Controller actually watched were never sealed. (B, F-7.)
4. **Re-dispatch of failed trials.** A treats the Wan 2 and Kling re-runs as a one-call/one-trial
   violation (F-01). B treated the same facts more narrowly and is re-computing them from the sealed
   attempts; the result is in `AUDIT-2026-09-10-EVIDENCE-RECOMPUTE.md`. Where the two readings differ
   the recompute report presents both, and the Controller rules.
5. **Local mechanical proof.** A could not execute from the Mac checkout. B did, at `dcfa6af`:
   326 tests `OK`; registry validator `PASS` at 575 rows; two runs' Registry rows rebuilt from sealed
   bytes and byte-identical (25 of 25); the routing map regenerated identically at 61 cells; the
   package rebuilt (see 1 above); **all 311 sealed media re-hashed exactly** against their record
   files with no post-sealing modification anywhere in git history; both blind commitments
   re-computed and matching; reveal keys confirmed outside the repository; network imports confined
   to `transports.py`; no key material in any sealed file.

## What was repaired on `work/audit-b-zero-spend-fixes`

Zero spend. Nothing under `eval/experiments/**` was modified and no `authorization*.local.yaml` was
touched. No Controller decision was taken by anyone: every open question went onto
`AUDIT-2026-09-10-CONTROLLER-DECISIONS.md` instead of being resolved.

**Test suite: 362 tests, `OK`** — the 326 that existed at `dcfa6af` plus 36 new ones. Verified twice,
once by the executor and once independently.

| Finding | What changed |
|---|---|
| F-1 — a cap was enforced per run, not per authorisation | `ledger.py` now pools every run that records the same signed authorisation and checks the ceiling, the tranche caps and the currency sub-caps against the combined total. A new run under a spent authorisation is refused before its folder exists. It fails closed: an unreadable sibling refuses rather than counting zero. Replaying the real ledgers, video piece 1's overrun is prevented outright. |
| F-4 — "no more than N calls" was unenforceable | `max_paid_calls` is now an optional authorisation field, enforced at reservation time across the same pooled runs. Absent means no limit, and the status output says so in words. No call constant exists in code. |
| F-4 (judge half) — a rebuilt report substituted its own call count | A live screening run now persists its own counters (sent, refused, what stopped it) into its results; a rebuild reports the live number or says plainly that it has none. |
| F-8 — smoke draws reused production trial identities | A liveness draw now carries its own identity that cannot collide with a candidate draw, the plan records its draw class, and the Registry builder, the evidence-map builder and the judging packet all refuse a liveness run as evidence. Duplicate trial ids in one plan are refused outright. |
| F-9 — the master price index silently carried superseded prices | A supersession note names the four re-pointed routes and the sub-index that now prices them, plus the fact that no paid call has ever run on that surface. No fetched bytes were touched. |
| F-5 — the state of record said the Registry was empty | Three annotated corrections in `PROJECT-MEMORY.md`; the spend figures, both cap crossings, the merged state of PR #93 and the untested Gemini surface corrected in `CONTROL-STATE.md`. Each correction is marked, not silently rewritten. |
| F-2 / F-3 — four different cost numbers were being reported as one | `tools/reconcile_spend.py` produces the per-run table with ledger-consumed, delivered, produced-nothing and a deliberately empty vendor-billed column. |
| F-6 — the elimination rule moved mid-run | `tools/recompute_elimination.py` recomputes it literally from the sealed attempts; the report shows every number that moves. Nothing was regenerated and no verdict was changed. |
| F-12 — pinned quotes were never re-checked mechanically | `tools/verify_price_pins.py` re-checks all 81 pins across every index: files, byte counts, fingerprints and quoted strings. All verify. |

**Discovered while repairing, not by either audit:** the signed authorisation files are amended **in
place**, so raising a cap changes the file's fingerprint and starts a fresh budget under the repaired
ledger. That is why the Wan 2 overrun is only half-caught. Whether an amendment should keep one budget
is decision **C-6a**; the one-line change is located and documented but deliberately not made.
