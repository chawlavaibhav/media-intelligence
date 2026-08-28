# Governor Level-1 Review — EVAL-035 (pilot video-route substrate, third pass)

**Review mode:** Level 1 — task/PR integrity review (`governance/GOVERNOR-CONTRACT.md` §3a).
**Authorisation:** `coordination/decisions/CONTROLLER-EVAL-035-FINAL-ACCEPTANCE-2026-08-28.md`
("EVAL-035 is Controller-accepted and may proceed to a bounded Level-1 Repository Governor
review"), reflected in `coordination/CONTROL-STATE.md` Next gate item 1. This is **not** GOV-007;
GOV-007 remains unauthorised, and this file carries no GOV task number for that reason.
**Audited `main`:** `f734fa4f54a94ec948658b31632af84d62d0ea1f` — "controller: mark EVAL-035
accepted pending governor", 28 Aug 2026.
**Branch reviewed:** `work/eval-035-video-route` at
`a4fbf404bdc5ac54f1deebb6ebbfd8d832fa9253` — the exact Controller-accepted head, verified equal to
the SHA named in the final acceptance decision.
**Date:** 28 Aug 2026 · **Spend:** USD 0. No model, provider or paid API call; no generation.

**What this verdict is.** A Governor verdict speaks only to repository coherence: scope, authority
honesty, current-state consistency, historical integrity, and mechanically checkable paths, counts
and controls. A PASS here does **not** mean Veo is qualified, that Veo is the best model, that
PILOT-001 spend is authorised, or that the live Gemini provider path has been empirically proven —
all four remain explicitly false/unestablished, and the branch itself says so. This review does not
redesign the route, the spend system, the Resources writer or the pilot architecture.

---

# Verdict: PASS WITH NON-BLOCKING NOTES

No blocking repository-coherence defect found in scope. The worker-reported **103/103** test result
was **independently rerun in this review's environment and reproduced exactly** (fresh worktree at
the accepted head, isolated interpreter, zero network — the suite's own socket-blocking fixture was
also verified to bite). One Low documentation-only note recorded below — the same one the
Controller already routed. **EVAL-035 requires no correction before Controller merge.**

---

## A. Branch purity and ownership — clean

Mechanically verified from the complete diff `745f43c5..a4fbf404` (merge base with `main` is
`745f43c521d9ff1a611589e4ee8f826cf1213009`, exactly the `main` SHA the final acceptance names):

- **Three commits, all EVAL-035, same worker:** the first (fal) pass, the direct-Gemini
  correction pass, and the third RES-007-integration/persistent-spend pass. No unrelated commits.
- **16 files, every one added (`A`), every one under `eval/`:** 15 under `eval/pilot-substrate/`
  plus the task deliverable `eval/tasks/EVAL-035-CONTROLLER-BRIEF.md`. The Eval charter grants
  "everything under `eval/`".
- **Nothing outside `eval/` is touched** — path-scoped diff against `resources/`, `canon/`,
  `coordination/`, `governance/`, `verify/` returns empty. No Resources-owned file, no Canon file,
  no Controller decision modified.
- **No Registry row:** `eval/registry/registry-v1.jsonl` untouched by the branch; independently
  re-validated on current `main` (`validate_registry.py` → "PASS … registry empty", 0 data rows).
- **No paid/runtime artefact, no binary committed:** `git diff --numstat` shows zero binary
  entries; the only media bytes anywhere are the in-test synthetic `MP4_FIXTURE_BYTES` constant
  (deliberately invalid UTF-8, clearly labelled a fixture). A diff-wide scan for Google API key
  material (`AIza…`) returns zero.
- **The first-pass root-level `.gitignore` change is absent from the net diff** (Correction 4
  honoured). The only ignore handling is the task-local `eval/pilot-substrate/.gitignore`
  (ignoring the local runtime authorisation file), and runtime run state targets `eval/runs/`,
  which the root `.gitignore` already ignores (line 39).

## B. Route authority — agrees exactly with current Controller authority

Verified in the frozen route table (`video_route.py` `VIDEO_ROUTES`), the request builder, and the
tests — not just prose:

- Provider surface **direct Gemini Developer API** (`generativelanguage.googleapis.com/v1beta`,
  `:predictLongRunning`), credential **`GEMINI_API_KEY`** via the documented `x-goog-api-key`
  header, model **`veo-3.1-fast-generate-preview`** (also pinned as `model_version`), 720p pinned,
  9:16 supported and used in the pilot-shaped tests. Exactly one slot; an unknown slot raises with
  "adding one is a Controller decision".
- **fal execution code fully absent.** Repository-wide grep over the package's executable files
  finds no fal route, no `FAL_KEY`, no `X-Fal-*` header, no fal queue URL, no fallback/retry
  header logic. "fal" appears only twice, both prose history (the `video_route.py` docstring and
  the README's "superseded" paragraph) — permitted historical explanation.
- **No qualification claim.** The route table's own docstring, the README and the Controller Brief
  each state T1 plumbing only: "not model qualification, not a Registry row, not a claim Veo is
  the best production model."

## C. Actual merged RES-007 integration — verified in code and by execution

This was inspected directly in `eval/pilot-substrate/tests/test_res007_integration.py`, not taken
from the worker summary:

- The test module **imports the merged writer from the repository checkout by real path**:
  `REPO_ROOT / "resources" / "pilot-writer" / "outcome_writer.py"` via
  `importlib.util.spec_from_file_location`. There is no copied writer, no mock writer, no copied
  G12 schema, and no hand-maintained required-field list anywhere in the package
  (`test_provenance_res007.py` states this division explicitly). The `resources/` tree on the
  branch is byte-identical to current `main`'s (path-scoped diff empty), so the imported writer IS
  the merged one.
- It **invokes the merged validator as shipped**:
  `subprocess.run([sys.executable, resources/pre-execution-freeze/validators/validate_topology_v3.py, archive])`.
- **Successful-path proof** (`test_successful_route_outcome_flows_through_the_merged_writer_and_validator`):
  fake Gemini transport → EVAL route → **persistent** ledger reservation/settlement (via
  `open_pilot_runtime` on a synthetic authority chain) → `res007_cost_ledger_entry` → real
  `OutcomeWriter.add_ledger_entry` → real `record_attempt(step_id=…, **writer_fields)` → real
  `record_artifact` from the persisted bytes → `write_archive` → merged validator → **exit 0**.
  Asserted in the archive itself: attempt `cost_ref` == cost row `ledger_entry_id` == route
  outcome `cost_ref`; writer-recomputed artifact hash == route-persisted SHA-256; `immutable:
  true`; `cost_class: api_tool`.
- **`storage_class` is not passed to the writer.** `res007_production_attempt()` keeps it in
  `provider_extras`; `test_storage_class_kwarg_would_be_refused_by_the_merged_writer` proves the
  merged writer itself refuses it ("unknown field") — Resources owns the frozen storage class.
- **Failure/ambiguity proof** (`test_ambiguous_failed_outcome_…`): ambiguous submit timeout →
  persistent conservative settlement → immutable cost row (basis contains "conservative") → real
  failed attempt through the merged writer (`status: timeout`, non-empty `error_detail`,
  `completed_at: null` because genuinely unresolved, stable `cost_ref`) → no artifact (and a
  separate test proves the merged writer refuses attaching one to a failed attempt) → merged
  validator → exit 0.
- **Negative validator control** (`test_validator_negative_control_detects_a_gutted_attempt`): an
  archive whose attempt is stripped of `prompt_hash` makes the same subprocess invocation **exit
  1** — the green runs are not vacuous.

## D. Persistent PILOT-001 spend integrity — claimed invariants are actually present

Inspected in `pilot_spend_ledger.py` and its tests (Governor check only; no redesign):

- **Persistent identity:** `TRANCHE_ID = "PILOT-001"`; a durable `run.json` per run id carrying
  the ceiling, decision ref and `retries_authorised: 0`; `create()` refuses to overwrite an
  existing run; `open()` reconstructs history (an absent run record fails closed — "assuming zero
  is the one answer that can overspend").
- **Append-only:** record types exactly `reservation`/`spend`/`release`; sequence-numbered from 1;
  written with append + fsync; settlement adds a `spend` row referencing the reservation — no
  rewrite path exists in the module.
- **Reserve-before-dispatch:** the route calls `reserve()` before any send; the reservation is on
  disk before dispatch (`test_reservation_is_persisted_to_disk_before_any_dispatch`); pending
  reservations count against headroom, including from a second reader.
- **Settlement:** keeps the reservation's `cost_ref` (asserted row-by-row); after settlement the
  reservation no longer counts separately (`_totals` excludes settled reservations from pending).
- **Release:** only on the route's provably pre-dispatch paths (missing key before send); the
  ambiguous post-dispatch tests assert `released == 0` and headroom stays consumed.
- **Cross-process continuity:** proven with a **real second OS process**
  (`subprocess.run([sys.executable, "-c", …])`), not a second Python object — the fresh process
  sees committed 0.80 / pending as recorded, never zero. Independently rerun here: passes.
- **Corruption fails closed:** malformed JSONL line, sequence gap, in-process truncation/shrink,
  unknown record type, missing run record, and run-vs-authority ceiling drift each raise
  `LedgerCorrupt` — the task's explicit matrix is satisfied.

## E. Spend authority remains closed — mechanically verified against the real repository

- **No committed valid PILOT-001 authority exists.** Grep for `machine_authorisation` across
  `coordination/decisions/` on current `main` **and** on the branch: zero files. The suite's
  decisive tests (`test_current_committed_repository_state_cannot_open_a_paid_guard`,
  `test_current_repository_state_cannot_open_a_live_runtime`) run against the **real** decisions
  directory and pass — a perfectly-formed local YAML is refused and no run directory is created.
- **Both halves required:** a committed decision carrying a fenced `machine_authorisation` block
  (tranche `PILOT-001`, boolean `authorised: true`, positive cap, `retries_authorised: 0`,
  approval identity/date) AND a matching local runtime file. Local file alone: refused. Local file
  naming an existing **non-authorising** decision (the real pre-pilot tranche decision is used in
  the test): refused with "no machine_authorisation block". Local ceiling above the committed cap:
  refused ("may narrow an authority, never widen it"). Retries other than 0: refused on either
  side. Two valid committed authorities: refused as a conflict.
- **No real approving decision is created by this branch** (its diff adds nothing under
  `coordination/`); the synthetic authority chains live only in pytest `tmp_path` fixtures
  labelled "test fixture, not real authority".

## F. Cost-record coherence — complete and honestly labelled

`res007_cost_ledger_entry(...)` emits: `ledger_entry_id` (== the attempt's `cost_ref`), `amount`,
`currency: USD`, `cost_class: api_tool`, `recorded_at`, explicit `basis`, `immutable: true`. The
basis text never claims invoice truth: the success path is labelled
"provisional_published_rate … modelled estimate, not invoice evidence" (rate USD 0.10/generated
second, official pricing page, fetch date named), and ambiguous dispatch is labelled
"conservative_reserved_estimate_billing_unknown … not invoice evidence". The adapter **refuses**
an outcome with no durable `cost_ref` (in-memory guard) rather than emitting an anonymous row.
The integration test proves the attempt's `cost_ref` resolves to the Resources ledger row.

## G. One-call-one-trial semantics — mechanically verified

One `predictLongRunning` submit = one trial (`route.submits`, transport call counts). Ten polls
before completion still count as one trial; the download is one fetch with no auto re-fetch. There
is no retry code path (`retry_of_attempt_id` pinned `None`; `retries: 0`), and
`test_zero_client_retries_even_when_a_second_call_would_succeed` proves a transport that would
succeed on call two never gets one. Ambiguous submit/poll/download failures settle and stop —
never re-submit. Repair is explicitly out of scope ("a later authorised repair would be a NEW
attempt owned by PILOT-001, not by this module").

## H. Binary handling — clean

`artifact_store.py` accepts `bytes` only (`str` raises TypeError; empty payload refused); writes
with `write_bytes`; records SHA-256 and byte count over the exact bytes written; artifacts are
immutable (existing path refused); a declared-size mismatch is recorded, not hidden. The test
fixture is deliberately invalid UTF-8 and a test proves it cannot survive a text API. No generated
media bytes are committed anywhere as fake empirical evidence.

## I. API key handling — clean

`GEMINI_API_KEY` is read from the environment only inside `generate()` at dispatch time; a missing
key is a provably pre-dispatch refusal that releases the reservation. The key appears only in
request headers; `test_key_never_enters_payload_or_persisted_records` proves it is absent from the
payload, the attempt record, the artifact record and the persisted request-config file. The
autouse conftest fixture strips any real key from the test environment; fake tests use an
explicitly fake value. No credential is committed (diff scan clean).

## J. Branch freshness — merges cleanly; no material drift

The acceptance recorded `behind_by: 0` against then-current `main` (`745f43c5`). `main` has since
advanced by exactly two commits — the final-acceptance decision itself and the CONTROL-STATE
update marking EVAL-035 accepted-pending-Governor. Both touch only `coordination/`; neither
affects EVAL-035, the Resources writer, the validator, spend authority or route authority.
**Independently verified: the branch merges into current `main` `f734fa4` with zero conflicts**
(trial merge performed and aborted). No rebase is required.

## K. Historical honesty — the three passes are recorded, not rewritten

The correction loop is preserved in three places: the branch history itself keeps all three
commits (fal pass → direct-Gemini correction → third pass); the README and `video_route.py`
docstring state the first pass was fal and was superseded by Controller/user route policy; the
Controller Brief's human summary states plainly that the second pass's "78 green tests" hid a
hand-maintained field-list compatibility proof (with the `storage_class` defect) and an in-memory,
per-process spend guard, and that the third pass fixed both structurally. Nowhere does any
artifact claim EVAL-035 worked correctly from the beginning. The three Controller review decisions
recording the loop are untouched by the branch.

## L. Live-evidence boundary — explicit and consistent

The branch keeps fake-tested infrastructure clearly separate from live evidence, in the module
docstring ("UNTESTED AGAINST A LIVE PROVIDER … treat the real path as unproven"), the README
(execution-time re-verification required; the `-preview` identifier may be retired), and the
brief's UNKNOWN section (real dispatch, operation cadence, error vocabulary, blocked-video
response, served content type, actual billing — all unverified). Current truth remains: real
provider calls **0** · spend **USD 0** · generations **0** · live Gemini network path
**unverified** · actual provider billing **unverified** · Registry rows **0**.

---

## Independent test rerun — reproduced

Run in this review's environment from a fresh worktree at `a4fbf404` (isolated Python 3.12 via an
ephemeral environment; the package's own autouse fixture blocks sockets and strips the key):

- **Full committed EVAL-035 substrate suite: 103 passed, 0 failed** — reproducing the
  worker-reported 103/103 exactly, in under one second, with zero network and zero spend.
- The two decisive files were additionally rerun verbosely: `test_res007_integration.py`
  (5 tests — success chain, ambiguous-failure chain, writer-refuses-artifact-on-failure,
  negative validator control, storage_class refusal) and `test_pilot_spend_ledger.py` (18 tests —
  including both real-subprocess continuity proofs and the six fail-closed corruption cases):
  **23/23 passed**.
- Also independently rerun on current `main`: `eval/registry/validate_registry.py` → PASS,
  registry empty (0 data rows).

No test was skipped; nothing in the review relies on an unreproduced worker number.

---

## Non-blocking notes

**N1 (Low, documentation-only — already Controller-routed).** The `generate_pilot_video`
docstring ([`eval/pilot-substrate/video_route.py`](../../eval/pilot-substrate/video_route.py)
line 715) still says "see `pilot_authorisation.open_pilot_guard`", but no function of that name
exists any more; the live path is `pilot_spend_ledger.open_pilot_runtime` +
`pilot_authorisation.verify_authority`. Verified stale by grep: the name appears nowhere else in
the package and has no definition. Executable code and tests are unaffected (the docstring's
substantive claim — that committed state cannot open a paid path — remains true). Owner: Eval;
fix opportunistically on the next EVAL-035-touching task. Not a merge blocker, per the
Controller's explicit disposition.

**N2 (informational, no action).** The brief's `behind_by: 0` claim was true at acceptance time;
`main` has since gained the acceptance decision itself and the CONTROL-STATE update (both
coordination-only). Recorded here so a future reader does not mistake the drift for an unhonoured
rebase requirement; the clean trial merge above settles it.

---

## Completion summary

| Item | Result |
|---|---|
| Review mode | Level 1 (bounded task/PR integrity) |
| `main` SHA reviewed | `f734fa4f54a94ec948658b31632af84d62d0ea1f` |
| EVAL-035 branch SHA | `a4fbf404bdc5ac54f1deebb6ebbfd8d832fa9253` |
| Verdict | **PASS WITH NON-BLOCKING NOTES** |
| Blocking findings | none |
| Non-blocking notes | N1 stale docstring pointer (Low); N2 informational freshness note |
| Independent rerun | **103/103 reproduced** (full suite; 23/23 on the decisive files rerun verbosely) |
| Merged RES-007 successful-path integration | **PASS** — real merged writer + real merged validator, exit 0, cost/hash identity asserted |
| Merged RES-007 ambiguous/failure integration | **PASS** — real writer/validator accept the conservative failed journey; negative control exits 1 |
| Persistent cross-process spend | **PASS** — real second OS process sees prior committed/pending spend, never zero |
| Paid-authorisation status | **CLOSED** — no committed `machine_authorisation` block exists; dual-gate fails closed against the real repository |
| Live provider calls / spend / generations | 0 / USD 0 / 0 |
| fal execution code | **fully absent** (historical prose only) |
| Copied/mock Resources compatibility layer | **none remains** |
| Correction required before Controller merge | **No** |

The Controller merges; the Governor does not.
