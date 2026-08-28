# Controller Brief — RES-007

**TASK:** RES-007
**STATUS:** completed

**HUMAN SUMMARY:** The project now has working software that can *record* a real customer
production job — every provider call (including the failed ones), every local ffmpeg-style
operation, every human review, every file of actual bytes, and every cost — in the exact
frozen v3 format the project's validators accept. Until now the v3 rulebook and its checkers
existed, but nothing could write a real journey into them; the first pilot would have had to
be reconstructed from chat afterwards, which is the failure mode the whole persistence
contract exists to prevent. I proved the writer works by building a fully synthetic
"branded video" journey (fictional provider, test currency, zero spend) whose true cost I
computed by hand first: the frozen cost engine independently recomputed the identical number
(42.00 test-currency units fully loaded). The main uncertainty is not in the writer but in
one inherited field of the old v2.1 attempt schema (`eval_item_id`, which assumes every
provider call serves a benchmark item — a pilot call serves a customer brief instead); this
is an observation for awareness, not a blocker, because the frozen validators accept
pilot-shaped records as-is. No contract was changed. PILOT-001 recording is now technically
unblocked from the persistence side.

**WHAT I DID:** Implemented `resources/pilot-writer/outcome_writer.py`, a small library that
builds a v3 archive step by step (job → outcome → set → unit → step → attempt/artifact →
acceptance) and refuses, at record time, the same mistakes the frozen validator would reject
later — e.g. attaching a provider attempt to local work, or hand-typing a file hash (hashes
and byte counts are always computed from the actual bytes). Then I wrote 19 tests
(`resources/pilot-writer/tests/test_pilot_journey.py`) that build a realistic synthetic
journey with genuinely binary artifact files, run the two frozen validators on the output as
subprocesses, exercise the failure paths, and re-run the pre-existing 18/18 lineage and
13/13 cost control suites to prove nothing regressed.

**OBSERVED:**
- All 19 new tests pass; the existing control suites still pass 18/18 and 13/13 (baseline
  verified on clean `main` before any change).
- The synthetic journey archive passes `validate_topology_v3.py` with all 11 gates green:
  1 job, 1 outcome, 2 sets, 4 units, 7 steps (3 provider / 2 local / 2 human), 5 attempts =
  5 trials, 5 artifacts, 2 failed attempts preserved individually with verbatim reasons.
- `recompute_cpao_v3.py` recomputed exactly the hand-calculated expectation: api_tool 26.50,
  local_compute 0.50, human_required 15.00, fully-loaded 42.00 XTS, 1 accepted outcome,
  9 distinct cost entries. One ledger entry shared by two local steps was counted once
  (the engine's no-double-counting rule, observed working). A 5.00 human_optional entry was
  visibly excluded from both views, as the contract requires.
- Binary handling: the five artifact files are deliberately not valid UTF-8 (embedded null
  bytes); tests independently recompute SHA-256 and byte length from the files on disk and
  they match the archive. The local artifacts' bytes really are their parents' bytes
  combined, so the recorded lineage is the lineage that produced the bytes.
- Ordered multi-parent lineage works: the concat artifact records shot-A-then-shot-B at
  positions 0/1, and the final composite records source+overlay at 0/1; the writer refuses
  duplicate or gapped positions.
- Failure paths: a refusal and a timeout persist as individual attempts with reasons and no
  artifact. Three committed negative controls behave as required — a mutable cost entry and
  a nothing-accepted journey are both *refused* by the frozen cost engine (refusing is the
  contract's correct behaviour), and an archive tampered after writing (fake attempt on a
  local step) is rejected by the frozen validator under gate G2.
- A repair journey (local `step_kind: repair` with `repair_of_step_id`) validates and
  recomputes correctly.
- Output is deterministic: rebuilding reproduces the archive byte-for-byte.

**INFERRED:** The accepted v3 topology and CpAO contracts can represent the planned
PILOT-001 journey shape cleanly — provider generation with retries/refusals, local
assembly, repair, human review, binary artifacts, ordered lineage, outcome-level acceptance
and immutable costs all fit without any contract change. I base this on the frozen
validators (not my own code) accepting every positive case and refusing every negative one.

**SURPRISES / BELIEF UPDATES:** None material. The contracts were implementable exactly as
written; no gate had to be argued with.

**FAILURES / BLOCKERS:** No task stop condition fired. One workspace incident, resolved:
several parallel pre-pilot worker sessions shared one working directory, and my commit (like
CANON-012's and CANON-013's) initially landed on the locally checked-out
`work/eval-035-video-route` branch. I recovered by re-parenting my commit onto clean `main`
in an isolated worktree and pushing that as `work/res-007-pilot-writer`; the pushed branch
contains exactly main + RES-007. I did not touch the shared local branch (a live EVAL-035
session owns that checkout) — it still carries stray local-only copies of the three
commits, which the EVAL-035 worker or Controller should drop before pushing it. The
incident affected git bookkeeping only; no other stream's files were modified.

**UNKNOWN / NOT VERIFIED:**
- The v2.1 attempt schema, which v3 inherits, lists `eval_item_id` ("the benchmark bank item
  this attempt was made for") as required. A pilot production call serves a customer brief,
  not a bank item. The frozen v3 validator does not mechanically require the field, so pilot
  records pass, and the writer stores any provider-identity fields verbatim — but strict
  v2.1-field-completeness for production (non-benchmark) attempts is undefined. Flagged for
  awareness; resolving it (e.g. a sanctioned sentinel for production jobs) would be a
  contract clarification only the Controller may make.
- The writer has not yet persisted a *real* journey (that is PILOT-001 itself, not
  authorised). Real provider payloads may carry fields the synthetic journey did not
  exercise; the writer accepts arbitrary verbatim attempt fields, so this is a low risk,
  not a verified fact.

**ASSUMPTIONS CHALLENGED:** none.

**LOCAL IMPLICATIONS:** Resources can now record the pilot as it happens instead of
reconstructing it afterwards. The committed synthetic journey doubles as a worked example of
correct v3 usage for whoever runs PILOT-001.

**CROSS-STREAM IMPLICATIONS:** CROSS_STREAM (propose only): EVAL-035's route substrate will
return real binary artifacts; its outputs can be persisted through this writer at the pilot
integration boundary. Measurement rows remain Eval-owned — the writer stores supplied
references verbatim and invents no semantics.

**ARCHITECTURAL IMPLICATIONS:** none — no schema mismatch was found, so no STOP was needed.

**DECISIONS NEEDED FROM CONTROLLER:**
- **HED-1 remains open, deliberately.** The writer records whichever human-cost class is
  supplied (`human_required` counts in fully-loaded CpAO; `human_optional` is recorded but
  excluded from both views). The synthetic journey shows both classes computing correctly;
  the class labels in synthetic data imply nothing about how real pilot review time should
  be classified. When you decide HED-1, the decision is representable without rewriting any
  journey (ledger entries are immutable; classification of new real entries follows your
  rule).
- Optional, low priority: whether production (non-benchmark) attempts need a sanctioned
  convention for the inherited `eval_item_id` field (see UNKNOWN above).

**EVIDENCE WORTH HUMAN INSPECTION:**
- `resources/pilot-writer/synthetic-journey/pilot-journey-synthetic.yaml` — read the steps
  section top to bottom: it is the story of a small production job (refusal, retry, timeout,
  retry, logo, concat, brand, review) told entirely in the frozen format. Notice the two
  failed attempts sitting as ordinary rows with verbatim reasons.
- `resources/pilot-writer/synthetic-journey/negative-controls/` — the three ways the system
  refuses to lie (mutable cost, accepting nothing, fake attempt on local work).

**FILES CREATED / MODIFIED:**
- `resources/pilot-writer/outcome_writer.py` (new — the writer)
- `resources/pilot-writer/tests/test_pilot_journey.py` (new — 19 tests)
- `resources/pilot-writer/synthetic-journey/` (new — committed archive, binary artifact
  bytes, recipes, README, repair journey, 3 negative controls)
- `resources/tasks/RES-007-CONTROLLER-BRIEF.md` (this brief)
No files outside `resources/` were touched. No frozen contract or validator was modified.

**RECOMMENDED NEXT STEP:** Review this alongside CANON-012 and EVAL-035 at the pilot gate.
If accepted, the pilot-side persistence question becomes "who calls the writer during
PILOT-001", which belongs to the pilot integration design, not to another Resources task.

**EPISTEMIC CHECK:** Facts above are observed from committed code, test output and the
frozen validators' own output; interpretations are confined to INFERRED; unknowns are
stated, not filled; numbers are explained (42.00 XTS is a synthetic test total proving the
engine reproduces a hand-computed figure, not a real cost); no unapproved decision is
presented as fact.

**CONFIRMATION:** No unapproved next strategic step was started. No provider was called, no
media generated, USD 0 spent. HED-1 was not decided. No topology/CpAO contract was changed.
