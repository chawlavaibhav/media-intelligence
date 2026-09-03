# PROPOSED — EVAL-038 substitution design: weak model + compiled packs vs strong model alone

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

**What this is.** A design, and only a design, for the experiment the north star actually needs
and that no lane has ever run (GAP-07): a WEAK model consuming accepted-only compiled Canon packs,
compared against a STRONG model alone. This document authorises nothing, dispatches nothing, and
spends USD 0. Running it requires (1) compiled packs that exist and pass the USD-0 pre-checks
below, (2) explicit user spend approval naming exact model, call count and maximum cost, per the
29-Aug reset decision (`coordination/decisions/CONTROLLER-PROGRAMME-RESET-MEDIA-FACTORY-PRIORS-2026-08-29.md`),
and (3) a Controller decision adopting this design. Gaps addressed: GAP-07, GAP-06 (judging
repair), GAP-23 (retro-test pre-check), GAP-22 (economics dependency).

**Why EVAL-037 cannot be cited instead:** the only lane that consumed Canon at scale was Sonnet
CONTROLLED_CANON — a strong model on a 53.4%-HOLD diet with judging never committed. The
weak+Canon cell of the matrix is empty (Gemma FULL_CANON 0/18 trials used Canon, Haiku FULL_CANON
3/18), and no lane anywhere ever received an accepted-only treatment. Recompute: the A2/A3
commands in `canon/findings/PROPOSED-EVAL-037-EVIDENCE-ANNOTATIONS.md`.

---

## 1. Question and endpoints

**Question.** Does a weak LLM with per-pack compiled doctrine injected unconditionally produce
creative packages that match or beat a strong LLM working alone, on the same six briefs?

**Primary endpoint:** pairwise weak+pack vs strong-alone win/tie/loss per brief (18 pairings per
weak model: 6 briefs × 3 reps against the matching brief's strong-alone package).

**Secondary endpoint:** weak+pack vs weak-alone win/tie/loss (isolates the pack effect from the
model).

**Decision rule (proposal):** the substitution thesis is supported on a brief if weak+pack wins or
ties strong-alone under unanimous two-reviewer judgment; the programme-level read requires
supported-on ≥ 3 of 6 briefs. Anything less is a real negative result and is committed as one.

## 2. Treatment arms (new, paid)

Model list (named exactly; EVAL-037 ids, `eval/experiments/EVAL-037/experiment.yaml:99-124`):

- `claude-haiku-4-5-20251001` (Haiku) + compiled packs — 6 briefs × 3 reps = 18 trials.
- `gemma-4-31b-it` (Gemma) + compiled packs — 18 trials, CONDITIONAL: dispatch only if a unit
  price is established before freeze (it never was for EVAL-037) AND the pre-check in §5.4 shows
  the injected payload fits Gemma's 16,000-token input quota. If either fails, Gemma is dropped
  and the run is Haiku-only; the drop is recorded in the run record, not silently.

**Treatment mechanics:** the accepted-only compiled pack(s) selected by the brief's trigger row
are injected unconditionally into the system prompt — no retrieval tool, no model decision, no
optional consumption. Injection payload per trial is recorded byte-exact (see §6). Pack content
comes from `canon/knowledge/current/**` only; any HOLD or Q&A byte in an injected pack is a
protocol violation that voids the trial.

## 3. Comparator arms (REUSED, USD 0)

No new strong-model calls. The comparators already exist as committed packages:

- strong-alone: 18 sonnet-no-canon packages on `origin/work/eval-037-sonnet-no-canon`
  (`eval/experiments/EVAL-037/runs/sonnet-no-canon/packages/`);
- weak-alone: 18 haiku-no-canon packages and the gemma-no-canon packages on their
  `origin/work/eval-037-*` branches.

Same six briefs (B01–B06), so pairings are brief-matched. The reuse is legitimate only because
the no-canon conditions are treatment-free; the run record must state the reuse and the freeze
commit of each reused package set.

## 4. Judging

1. **Strip before blinding:** the judging pipeline strips KNOWLEDGE_AND_WEBSITE_USE and any other
   treatment-revealing section (any Canon-citing text) from every package before blinding —
   EVAL-037 packages self-disclose their treatment in that section, which made treatment-blindness
   structurally impossible (GAP-06). The stripped variants are committed alongside the originals.
2. **Blinding:** the corrected value-gate pattern
   (`canon/experiments/v1/value-gate/prepare_real_run.py`): OS-entropy blinding key generated and
   held OFF-repo; a salted SHA-256 commitment of the key IS committed before judging begins;
   key revealed and committed only after all verdicts are in.
3. **Reviewers:** two independent reviewers, neither being the session that built the packs;
   verdicts count only on unanimity, disagreements recorded as disagreements.
4. **Everything committed:** verdicts, rankings, reviewer-identity/independence statements, the
   commitment, and the revealed key — the EVAL-037 judging hole (no artifact on any ref) must not
   recur. `score_value_gate.py` machinery is reused where it fits.

## 5. USD-0 pre-checks — ALL must pass before any spend request is even made

**5.1 PILOT-001 retro-test (GAP-23).** Retro-test the compiled pack doctrine against the
programme's only human-adjudicated end-to-end failure. PILOT-001's two candidates were rejected by
the human acceptance authority on H1 (modern/premium FAIL) and H6 (publishable FAIL), with the
failure attributed to the prompt's creative direction, not the pipeline
(`coordination/decisions/CONTROLLER-PILOT-001-CANDIDATE-2-REJECTION-AND-T1-CLOSURE-2026-08-28.md`;
evidence at `eval/pilot-001/evidence/`). The check: read the relevant compiled pack(s) (B-video /
brand / premium-look doctrine) against the two rejected candidates and the frozen acceptance
contract, and answer in writing, item by item: **would the doctrine have forbidden the exact
choices the human rejected** (single-scene flat prompt, non-premium look)? Zero model calls, zero
spend. If the doctrine is silent on what the human rejected, the packs are not ready and EVAL-038
must not be dispatched — the retro-test result is committed either way as a findings artifact.

**5.2 Coverage-map freshness.** The 10-pack coverage map currently covers 19 of 24 accepted
sources; all 5 Indian sources are missing and `indian_indic_context` falsely shows zero
contributors (recompute:
`grep -c 'bijapurkar\|dwyer\|jain\|pandey\|parameswaran' canon/planning/CANON-V1-LIVE19-COVERAGE.yaml` = 0).
Packs compiled off the stale map silently omit every Indian-market accepted source — fatal for
B2C India briefs. The map must be regenerated over all 24 sources before pack compilation.

**5.3 Pack validation.** Every injected pack passes the pack validator(s) named by the compiled
pack contract (`canon/packs/COMPILED-PACK-CONTRACT-v0.1.md`, PROPOSED) and a mechanical
accepted-only purity check (every item id resolves under `canon/knowledge/current/`).

**5.4 Payload dry-run.** For each brief × model: serialize the exact injection payload (packs +
brief + non-reusable remainder), count tokens, and verify it fits the model's input quota with
headroom. EVAL-037's gemma-required lane died 18/18 on a 1.13M-token payload against a
16,000-token quota; that failure class must be excluded on paper before any call.

**5.5 Judging-pipeline dry-run.** Run the strip + blind + commit pipeline end-to-end on two
already-committed EVAL-037 packages (USD 0) and verify the stripped variants leak no treatment
marker (mechanical grep for 'Canon', 'KNOWLEDGE_AND_WEBSITE_USE', pack ids).

## 6. Failure-path evidence retention (mandatory)

Every trial — including every failed trial — records: the exact injected payload (or its SHA-256
plus committed bytes), token usage up to the failing turn, status and failure class, and cost.
EVAL-037's 16 overflow trials retained nothing ("What they retrieved is still not retained") and
their spend is permanently UNKNOWN; a trial in EVAL-038 whose failure-path evidence is missing is
a protocol violation. Survivor trials are never pooled with complete-lane packages in judging.

## 7. Spend

**Named maximum cost: USD 1.00** for the full paid tranche (both weak-model lanes, 36 trials),
per the ~USD 1.0 ceiling in the 29-Aug reset requirement's format. Basis: EVAL-037 Haiku lanes
empirically cost USD 0.331358–0.400029 for 18 trials each (recompute: A5 command in
`canon/findings/PROPOSED-EVAL-037-EVIDENCE-ANNOTATIONS.md`); comparators are reused at USD 0;
judging is human. If Gemma is dropped (§2), the maximum for the Haiku-only run is USD 0.50.
Dispatch requires a committed user spend approval naming: models `claude-haiku-4-5-20251001`
(and conditionally `gemma-4-31b-it`), call count 36 (or 18), maximum cost USD 1.00 (or 0.50).
Hard stop at the maximum; no retries beyond it; all spend recorded per lane as committed bytes.
This document requests nothing; it only fixes the numbers any request must name.

## 8. Value-gate disposition (proposal for a Controller decision)

The never-executed oracle-context value gate (`canon/experiments/v1/value-gate/`, 0 model calls,
blocker FRESH_CONTROL_SESSION_REQUIRED standing) asks exactly the compiled-pack question: if
hand-picked, perfectly relevant Canon does not beat generic craft advice, no retrieval or
compilation system will either. Two clean dispositions exist; this design needs the Controller to
pick one, and works under either:

- **(a) Retire and transfer (recommended by this proposal):** formally retire the value gate,
  transferring its question, its anti-lying safeguards (independent control authorship, length
  parity, two-reviewer unanimity, coverage-vs-gap probe split) and its blinding design into
  EVAL-038, whose oracle analogue is the compiled pack itself. The 12 hand-built oracle contexts
  and `oracle-selection.yaml` inclusion reasons remain the closest existing ancestor of per-pack
  doctrine selection and are consulted (not injected) during pack compilation review.
- **(b) Execute first:** authorise the one missing input — a Canon-naive session authoring
  `generic-contexts-real/` via `GENERIC-CONTROL-AUTHORING-PACKET.md` — and run the oracle
  experiment before EVAL-038, treating its result as the best-case ceiling the packs must
  approach.

Either way, the CONTROL-STATE row folding the value gate into "Concluded" needs the A6 annotation
(see the annotations document); "retired with question transferred" and "concluded" are different
states and only a Controller decision can set either.

## 9. What this design does NOT do

No pack compilation (REP-06A's contract and its successors), no edits under `eval/`,
`coordination/` or `governance/`, no model or provider call, no network fetch, no admission of any
HOLD source, no claim that EVAL-037's "Canon helps" transfers to this setting. Every number above
is either committed bytes (lane costs, quota, trial counts) or explicitly marked as a proposal
(decision rule, ceiling, disposition).
