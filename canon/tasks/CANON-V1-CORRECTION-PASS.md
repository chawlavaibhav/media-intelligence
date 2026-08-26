# CANON-V1-CORRECTION-PASS

**Status:** AUTHORIZED correction pass on `work/canon-v1-overnight` only.  
**Purpose:** close the Controller review loop on C1–C4 before merge.  
**Spend:** ₹0. No new source ingestion, purchase, acquisition, value-gate model run, or human verdict is authorized.

## Zoom-out

Canon is the durable creative/production knowledge layer: what matters, what good looks like, what trade-offs exist, what failure modes to look for, and what capability a job requires. It does **not** choose current models/providers, create Capability Registry scores, or implement routing.

The overnight work is substantively accepted:
- C1 live-19 coverage rebaseline: retain;
- C2 30-brief commercial bank: retain as the shared end-to-end customer-intent bank;
- C4 source-gap portfolio: retain as research leads only;
- C3 value-gate package: **must be corrected before any real run**.

Do not redesign the entire Canon programme. This is a bounded correction pass.

## Controller decisions you must implement

### C-C1 — Correct independence language in C1

`build_live19_coverage.py` uses a greedy construction. A greedy maximal independent set is not, in general, guaranteed to be the mathematical maximum independent set.

Correct comments/docs that call it the "largest" or "maximum" set unless the exact graph is exhaustively proven. Describe it honestly as the greedy/maximal result used under the Audit Gate dependence rule.

For the current 19-source corpus, retain 17 only if the committed dependence graph still supports it after the correction. Do not change the number merely because wording changed.

Also make explicit in the C1 human-readable output that:
- source/object/audit counts and the dependence rule are mechanical evidence;
- **source→domain contribution assignments in `live19_domain_map.yaml` are authored Canon judgements that are mechanically validated for completeness/known source ids, not machine-discovered truths.**

### C-C2 — Keep the 30-brief bank unchanged unless a mechanical defect is found

The 30 commercial briefs are accepted as the shared customer-intent bank. Do not rewrite them for stylistic preference.

Preserve:
- 30 total;
- 10 scenario families ×3;
- 10 English / 10 Hindi-Devanagari / 10 Hinglish;
- authoritative intent hidden from planning arms;
- exact strings and planted contradictions;
- Eval later samples its 12 end-to-end production briefs from this bank rather than creating a competing bank.

Only fix a brief if a validator proves a structural defect. Record any such change explicitly.

### C-C3 — Invalidate the currently authored generic controls for the real experiment

Controller finding: the same Canon-reading worker authored the generic controls after seeing the Oracle Canon material. Even if done carefully, that is a contamination risk.

Therefore:
- mark the current `generic-contexts/` as **DRY-RUN / CONTAMINATED-FOR-REAL-GATE** and make the real run builder refuse to use them;
- do not "clean them up" or re-author them yourself from memory;
- create a frozen, self-contained `GENERIC-CONTROL-AUTHORING-PACKET.md` (and machine-readable input if helpful) that can be given to a **fresh isolated session with zero Canon/oracle access**.

The fresh control-authoring input may include only:
- the 12 customer briefs/allowed brief fields;
- the same planning procedure/output requirements;
- a generic instruction to produce strong professional craft guidance without named Canon sources, source ids, extracted Canon text or oracle contexts;
- the target length/tolerance requirements needed for matching.

It must not expose Canon/oracle contexts or accepted-source contents.

If your environment can launch a genuinely isolated child/context that cannot access the Canon/oracle files, you may use it. If not, stop at the authoring packet and mark `FRESH_CONTROL_SESSION_REQUIRED`. Do not pretend the current session can "unsee" Canon.

### C-C4 — Make blinding actually sealed

The currently committed `blinding-key.json` is not sealed from anyone who can read branch history. It must never be used for the real run.

Implement a new real-run workflow:
- invalidate the existing key as dry-run-only;
- generate a **fresh balanced 6/6 A/B mapping at real-run preparation time**, not from a committed deterministic seed;
- store the mapping outside reviewer-accessible committed files while reviews are open;
- commit/store only a cryptographic hash/commitment to the key in the frozen run manifest if needed for integrity;
- after all verdicts are frozen, the key may be revealed and archived for reproducibility.

The reviewer packet must not contain anything that reveals arm identity.

Add a negative control demonstrating that no committed real-run packet/manifests reveal the mapping before unblinding.

### C-C5 — Two independent reviewers, not one

Update verdict storage and scoring for **two independent reviewers per pair**.

Each reviewer independently judges all nine creative dimensions, overall preference and explicit intent preservation.

Controller combination rule:

> A coverage-probe pair counts as a **clear Canon win** only when **both reviewers independently satisfy the existing per-reviewer clear-win rule** for the Canon arm. Reviewer disagreement, `cannot_tell`, or one clear win plus one non-win does not count as a clear pair win; retain it diagnostically.

Do not average reviewer scores into a pseudo-continuous number.

The scorer must:
- require exactly two distinct reviewer ids for every scored pair;
- reject duplicates/missing reviewers;
- report reviewer disagreement explicitly;
- preserve each reviewer's raw judgement;
- keep explicit-intent preservation as a gate, not a tenth score.

### C-C6 — Separate coverage probes from gap probes in the value decision

The early-12 set is mechanically balanced as:
- **7 coverage probes**
- **5 gap probes**.

These answer different questions and must not vote in the same continuation count.

**Coverage probes** answer:
> Where the live Canon actually has relevant accepted knowledge, does explicit Canon improve planning beyond the independent generic control?

**Gap probes** answer:
> How far does existing general Canon knowledge transfer into a known hole, and what failure remains attributable to missing knowledge?

Controller gate for the **7 coverage probes only**, frozen before any real output exists:
- **5–7 / 7 unanimous clear Canon wins** + no intent-regression stop → `continue`;
- **4 / 7** → `mixed`;
- **0–3 / 7** → `stop`.

This is an engineering continuation gate, not a population estimate or confidence statement.

The 5 gap probes are reported separately as diagnostics. They **never vote to stop source acquisition merely because the necessary knowledge is absent**.

**Intent safety remains global:** if the Canon arm degrades/violates explicit customer intent on any pair where the generic arm preserves it, surface `intent_regression` prominently and block automatic continuation pending Controller diagnosis. Do not bury it in the gap/coverage split.

### C-C7 — Update the scorer/dry-runs for the corrected gate

Create synthetic fixtures proving at minimum:
- two reviewers required per pair;
- reviewer disagreement does not count as a clear win;
- 5/7 coverage unanimous wins → `continue`;
- 4/7 → `mixed`;
- ≤3/7 → `stop`;
- gap-probe wins/losses do not change the coverage continuation band;
- intent regression overrides automatic continuation;
- incomplete/missing verdicts fail closed;
- reviewer packet cannot reveal the fresh real-run mapping.

No real model outputs or human verdicts may be generated in this correction pass.

### C-C8 — C4 remains research-only

Do not ingest any candidate. Preserve the live Canon at 19.

If current official/public web access allows you to improve candidate identity/access evidence without crossing a login/purchase/access gate, you may update evidence labels. Otherwise keep routes `not_verified` rather than guessing.

Do not treat Dalvi/ABCD/Cayla/other candidates as approved merely because they are promising.

## Required verification

Freshly run where the environment permits:
- live-19 coverage builder/validator;
- 30-brief bank validator;
- corrected value-gate build/scorer synthetic suite;
- Audit Gate validator;
- existing Canon test suite.

No claim of PASS without fresh command evidence.

## Completion criteria

This correction pass is complete when:

1. C1 independence language is mathematically honest and authored-vs-mechanical evidence is explicit;
2. C2 remains a valid 30-brief shared bank;
3. current generic controls are impossible to use in a real gate;
4. a fresh-session generic-control authoring packet exists;
5. the old committed blinding key is invalidated for real use and a fresh sealed-key workflow exists;
6. scoring requires exactly two independent reviewers;
7. only 7 coverage probes vote on continuation using the frozen 5–7 / 4 / 0–3 rule;
8. 5 gap probes are diagnostic only;
9. intent regression remains a global safety stop;
10. dry-run/negative controls prove the corrected logic;
11. no source is ingested and no real value-gate output/verdict is produced;
12. a correction brief is written at `canon/findings/CANON-V1-CORRECTION-CONTROLLER-BRIEF.md` with tests, residual blocker `FRESH_CONTROL_SESSION_REQUIRED` if applicable, and exact changes.

Do not merge to `main`. Commit and push the correction pass on the existing Canon branch.