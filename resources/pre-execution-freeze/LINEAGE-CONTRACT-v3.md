# Lineage contract v3

**Task:** R4-C · **Date:** 26 Aug 2026 · **Validator:** `validators/validate_topology_v3.py`
**Controls:** `validators/run_lineage_controls.sh` — originally **executed, 18/18 as declared**;
after the 2026-08-28 G12 correction (below) the suite grew to 28, and after the same-day
Review-2 extension it is **41 controls** (2 positives, 39 negatives) — **executed, 41/41 as
declared**. G12 negative controls also declare the exact invariant they must trip
(`# EXPECT-SUBSTRING:`), and the runner verifies the failure names that invariant — a control
cannot pass by accidentally breaking an unrelated field.

**Correction 2026-08-28 (RES-007 correction pass):** RES-007 stopped on a contract defect —
v3 inherits the v2.1 attempt contract, but the validator never mechanically checked the
inherited required fields, so an archive could pass while violating the written inheritance.
The Controller approved one narrow conditional override plus enforcement
(`coordination/decisions/CONTROLLER-PREPILOT-RETURN-REVIEW-1-2026-08-28.md`): `eval_item_id`
stays required for benchmark/eval attempts exactly as v2.1 wrote it, is not required and must
not be fabricated on v3 production-job attempts (their request context is the chain
attempt → step → unit → set → outcome → job → `brief_ref`), and **every other inherited
required attempt field stays required** — now enforced by gate **G12** below. Every v3
attempt declares `attempt_kind: production | benchmark_eval` so the rule is fail-closed
checkable. Historical v2.1 archives are unchanged and never reinterpreted.

**Review-2 extension (same day,
`coordination/decisions/CONTROLLER-RES-007-CORRECTION-REVIEW-2-2026-08-28.md`):** G12 also
checks the mechanically explicit v2.1 value constraints, not just field presence — `lane`
from the frozen vocabulary; `storage_class` exactly `C_irreproducible_empirical`;
`repeat_index` a 0-based integer (booleans, strings, negatives refused); `prompt_hash`,
`config_hash` and every `reference_asset_hashes` member a genuine SHA-256 (64 lowercase hex
characters, the project's hashlib-hexdigest convention; empty reference list stays valid);
non-null `repeat_of_attempt_id`/`retry_of_attempt_id` resolving to real attempts in the same
archive; `requested_at` and non-null `completed_at` valid ISO-8601 UTC (null `completed_at`
stays valid for a call that never completed). Deliberately outside mechanical validation:
whether a provider/model/endpoint actually exists, URL semantics, and any repeat/retry
*policy* beyond structural provenance.

---

## Two lineage namespaces that must never merge

| Namespace | Answers | Levels | Carried by |
|---|---|---|---|
| **Media lineage** | where a *piece of media* came from | byte · content · source | `lineage_keys.py` |
| **Request lineage** | where a *brief/request* came from | request population | `job.request_lineage_id` |

**A brief's provenance and a photograph's provenance are different facts.** Merging the namespaces
makes both unusable for independence reasoning: you could no longer ask "is this benchmark
independent of the request data we learned from?" separately from "is this holdout image independent
of the training pool?"

**Gate G11** fails any job whose `request_lineage_id` is populated with a media lineage id. Unknown
request lineage is **INDETERMINATE, never independent** — the accepted R-C4 rule, carried forward.

**Controller constraint recorded in the schema:** Arena-T2I-Hard is preserved for Eval
methodology/benchmark use, and raw LMArena prompt data is **not** a load-bearing request-discovery
source for the integrated request grammar. The constraint travels with the contract so it cannot be
lost between documents.

## The twelve gates

Each is enforced by the validator and has at least one negative-control fixture that must fail for
**its own declared gate** — a fixture failing for the wrong reason does not count as passing.

| Gate | Rule | Why it matters | Controls |
|---|---|---|---|
| **G1** | one provider call = one trial | If two calls shared a trial, every per-trial count would depend on filing habits | `nc-G1` |
| **G2** | local/human steps carry **no** provider attempts | **The core v3 gate.** See below. | `nc-G2a`, `nc-G2b` |
| **G3** | no unknown parent/unit/set/step reference | A dangling edge makes provenance unwalkable | `nc-G3` |
| **G4** | artifact parent graph is acyclic | A cycle means an artifact is its own ancestor; walks and cost sums never terminate | `nc-G4` |
| **G5** | ordering unambiguous | Shot order is meaning: A-then-B ≠ B-then-A | `nc-G5a…d` |
| **G6** | no artifact claims a trial that never existed | A trial invented after the fact | `nc-G6` |
| **G7** | accepted outcome has a final artifact **in its own provenance** | You cannot accept nothing, and the cost must describe what was delivered | `nc-G7a`, `nc-G7b` |
| **G8** | local steps carry a complete transform recipe | Deterministic in principle ≠ reproducible without the tool version | `nc-G8a`, `nc-G8b` |
| **G9** | no historical backfill of v3 context | Inventing provenance is the failure this contract exists to prevent | `nc-G9` |
| **G10** | failed/refused attempts persist individually with a reason | A failure with no reason is a row, not evidence | `nc-G10` |
| **G11** | request lineage ≠ media lineage | See above | `nc-G11` |
| **G12** | v3 attempts carry full inherited v2.1 call provenance; `eval_item_id` required iff `benchmark_eval`, forbidden on `production` | Without call identity an attempt is not verifiable evidence; a benchmark id on a production attempt is fabricated provenance (added 2026-08-28, see correction note) | `nc-G12a…i`, positive `v3-valid-benchmark-attempt` |

## G2: why it is the gate that mattered most

v2.1 had **nowhere to put an artifact produced by a local operation**. An ffmpeg concat produces real
bytes, costs no provider money, and is part of the outcome — but every artifact in v2.1 needed an
attempt. The structural temptation was therefore to **fake a provider attempt for local work**.

That would have been silently catastrophic. A fabricated attempt is a fabricated **trial**, and trials
are the denominator of reliability, `pass_at_k`, and every per-trial cost view. A pipeline with three
local composition steps per outcome would have inflated its trial count by roughly 3× and depressed
its apparent failure rate accordingly — with nothing in the data to reveal it.

v3 closes it from both directions:

- **G2a** — a `local_deterministic` or `human` step carrying `attempt_ids` is rejected;
- **G2b** — an artifact produced by such a step claiming an `attempt_id` or `trial_id` is rejected.

The positive fixture demonstrates the intended shape: **4 of its 9 artifacts come from local or human
steps and carry no attempt and no trial at all**, while the archive still reports exactly **7 trials
for 7 provider calls**.

## Ordered multi-parent lineage

Parents are a **list**, each `{parent_artifact_id, role, position}`.

- `position` is **required** where order carries meaning (`source`, `overlay`, `grade_source`) and must
  be **unique and contiguous from 0**. A duplicate makes order ambiguous; a gap makes it unknowable —
  was something dropped, or mis-numbered?
- `position` is **null** where order is meaningless (a simultaneous audio mix).
- The graph must be a **DAG**.

The positive fixture carries both shapes: an ordered 3-parent concatenation (positions 0/1/2) and an
unordered audio/video mix (positions null).

**Backward compatible:** a single-element list with `role: source, position: null` is exactly a v2.1
`derived_from_artifact_id`.

## Shared intermediates

One artifact may be consumed by many. The positive fixture generates a logo **once** and composites it
into two shots. This is normal and correct — and it is why cost attribution uses **set semantics over
distinct ledger entries** rather than graph traversal. See `CPAO-CONTRACT-v3.md`.

## Fail-closed behaviour

| Exit | Meaning |
|:--:|---|
| **0** | validated |
| **1** | gate violation found |
| **2** | **could not check** — missing, empty or unparseable input, or a partial archive |

"I found no problem" and "I could not look" never share an exit code. An archive missing any required
section is exit 2, not a pass.
