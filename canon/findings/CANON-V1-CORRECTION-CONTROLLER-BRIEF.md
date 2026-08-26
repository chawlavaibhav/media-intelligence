# Canon V1 correction pass — Controller Brief

**Task:** `canon/tasks/CANON-V1-CORRECTION-PASS.md` (C-C1 to C-C8)
**Date:** 26 Aug 2026 · **Branch:** `work/canon-v1-overnight` · **Not merged to `main`**
**Spend: ₹0.** No ingestion, no purchase, no model run, no human verdict.
**Residual blocker: `FRESH_CONTROL_SESSION_REQUIRED`** — see §4.

---

## 1. All eight decisions implemented

| ID | Decision | Status |
|---|---|---|
| **C-C1** | Correct independence language; mark authored vs mechanical | **Done — and strengthened** |
| **C-C2** | Keep the 30-brief bank unless a defect is proven | **Done — no defect found, bank untouched** |
| **C-C3** | Invalidate the contaminated generic controls | **Done — blocker recorded** |
| **C-C4** | Make blinding actually sealed | **Done** |
| **C-C5** | Two independent reviewers | **Done** |
| **C-C6** | Coverage probes vote; gap probes diagnose | **Done** |
| **C-C7** | Update scorer and dry-runs | **Done — 26 negative controls** |
| **C-C8** | C4 stays research-only | **Done — re-checked, still blocked** |

## 2. The two things this pass found that were not in the task

Both were caught by the negative controls the task asked for, and neither was visible from reading
the code.

### 2.1 Overall blinding balance was the wrong invariant

The task asked for a fresh balanced 6/6 A/B mapping. That was implemented — and the position-bias
test **failed anyway**.

The reason: **only the 7 coverage probes vote on continuation.** A tidy 6/6 split across all 12 pairs
happened to show Canon first on **5 of those 7**. A reviewer with a pure order effect — one who
simply prefers whichever plan they read first — would have scored **5/7 and reached `continue`**
without reading a word.

Balance is now **stratified by probe role**, and because 7 is odd, the leftover pair is given to the
**control** arm rather than to Canon. Canon is now shown first on **3 of 7** coverage probes, and
pure position bias lands in `stop`.

> This is the second time this single check has caught a real bias — it previously found the Canon
> contexts running 22–37% longer than their controls. Both would have produced a Canon "win" that
> was an artifact of presentation.

### 2.2 A leakage check that fires on the word "context" is a check nobody reads

The first version of the control-packet leakage scanner flagged the word `context`, which it had
derived by splitting `binet-field-effectiveness-in-context-ch1` on hyphens. A check that fires on
ordinary English trains its operator to ignore it.

The scanner now excludes generic fragments and keeps distinctive identifiers — surnames, directory
names, `source_id`s, reference ids. **And the scanner itself is now tested**: a test asserts it still
detects `murch-blink-p1-25` and `ondaatje` while ignoring `context`. A check that never fails proves
nothing.

## 3. What changed, by decision

### C-C1 — independence is now proven, not asserted

The old comment called a greedy walk "the largest set". A greedy maximal independent set is not in
general the maximum one, so that wording asserted something unproven.

**The computation is now exhaustive.** `independent_origin_count()` enumerates every subset — the
graph is at most 19 nodes — returns a true maximum, and labels every result
`method: "exact_exhaustive"`. It also computes the greedy answer and **asserts greedy ≤ exact**.
Above 22 nodes it refuses to enumerate and returns `greedy_lower_bound`, so a larger future corpus
degrades into an honest under-report rather than a false claim.

**No number changed.** Corpus independent origins remain **17**; every per-domain and per-pack count
is identical. For this corpus the greedy answer happened to be optimal. The wording was wrong; the
figure was not, and it has not been adjusted to suit the correction.

**Authored vs mechanical is now explicit.** A new section in the C1 document, a machine-readable
`evidence_class` block in the YAML, and a rewritten header in `live19_domain_map.yaml` all state
plainly: source/object/audit counts and the dependence rule are **mechanical evidence**;
**source→domain contribution assignments are authored Canon judgements**, validated for completeness
and for naming only real accepted sources, but not machine-discovered truths. Whether another Canon
worker would assign the same contributors is **untested** — the same open question the handoff
already records about audit records.

### C-C2 — the bank is unchanged

The validator was re-run: **30 briefs, 10 families × 3, 10/10/10 by language, 12 static / 18 video,
15 planted contradictions across 8 briefs, exit 0.** No structural defect was found, so **nothing was
edited** — not a word, not for style. `git status` shows the brief-bank directory clean.

Also re-verified: `authoritative_intent` appears in **no** context file given to any planning arm.

### C-C3 — the contaminated controls cannot reach a real run

`generic-contexts/` is renamed **`generic-contexts-DRYRUN-CONTAMINATED/`**, each file carries a
banner explaining why, and the directory has a README. The dry-run builder writes there and
**re-stamps the banner on every write**, so a regeneration cannot quietly produce a file that looks
usable.

**Why they were not simply rewritten:** re-authoring in the same session fixes nothing. The worker
still cannot unsee the Canon. The task said not to, and it was right.

Created instead:

- **`GENERIC-CONTROL-AUTHORING-PACKET.md`** — what the fresh session must and must not have.
- **`control-authoring-input.json`** — self-contained: the 12 customer briefs, media class,
  duration, word targets, the planning procedure, the authoring rules. Nothing else.
- **`build_control_packet.py`** — assembles it and then scans the assembled bytes for every accepted
  source name, `source_id`, reference id, oracle line and `authoritative_intent`. **Fails closed.**

The packet's most important instruction is the one most likely to be disregarded: **write a strong
control.** A session told it is producing "the generic arm" may reasonably infer it should be the
lesser one. A weak control produces a meaningless Canon win, and that failure is invisible in the
results — they simply show Canon ahead.

### C-C4 — blinding is sealed for real

The committed key was derived from a committed seed and stored as plain JSON: anyone reading the
branch could recompute it. It is now stamped `DRY_RUN_ONLY_INVALIDATED_FOR_REAL_USE`, and the builder
**writes that stamp itself** so it cannot be regenerated clean.

`prepare_real_run.py`:

1. **fresh OS entropy** at preparation time — nothing committed determines the mapping;
2. writes the key **outside** the repository and **refuses** a path inside the working tree;
3. commits only **`sha256(salt ‖ canonical_mapping)`**, with the salt stored beside the key — so the
   commitment cannot be brute-forced over the 2¹² possible mappings;
4. `--verify-key` re-derives the commitment after reveal, proving the mapping was not altered
   mid-review;
5. **refuses to run at all** while `generic-contexts-real/` is absent.

**Negative control:** a test asserts no committed real-run artifact discloses the mapping, and that
the reviewer packet never names an arm.

### C-C5 — two independent reviewers

The verdict schema now holds one entry per (pair, reviewer) — 24 for 12 pairs. The scorer requires
**exactly two distinct reviewer ids** per pair and rejects duplicates and omissions.

A pair is a clear Canon win only when **both** reviewers independently satisfy the per-reviewer rule.
One clear win plus one non-win is **disagreement**, reported explicitly, not resolved by arithmetic.

**No averaging.** Averaging two preferences invents a precision neither reviewer expressed, and would
let a strong opinion and a shrug combine into a confident-looking half-win. Each reviewer's raw
judgement is preserved.

### C-C6 — only coverage probes vote

**7 coverage probes vote. 5 gap probes diagnose.** Frozen bands over the 7:

| Unanimous wins | Band |
|---|---|
| 5–7 | `continue` |
| 4 | `mixed` |
| 0–3 | `stop` |

Letting a gap probe vote to stop expansion would be perverse: it would use the **absence** of a
source as an argument against **acquiring** one. A gap probe losing is close to the expected result.

The scorer **refuses to rescale** these thresholds if the probe count ever differs, returning
`undefined_probe_count`. Adjusting a frozen threshold to fit a changed denominator is how a
predeclared gate quietly stops being predeclared.

**Intent safety stays global.** A Canon intent regression on **any** pair — coverage or gap —
surfaces as the headline and blocks automatic continuation.

### C-C7 — 26 negative controls, all passing

`tests/test_value_gate_corrections.py`. Every test corresponds to a way the gate could quietly give a
wrong answer.

| What it proves | Result |
|---|---|
| One reviewer, or the same reviewer twice, fails closed | ✅ exit 1 |
| Reviewer disagreement is not a clear win (5/7 → 4/7, `mixed`) | ✅ |
| Judgements are not averaged; each is preserved | ✅ |
| Coverage bands 5/7 → `continue`, 4/7 → `mixed`, 3/7 → `stop` | ✅ |
| **All 5 gap probes winning cannot rescue a 3/7 result** | ✅ still `stop` |
| **All 5 gap probes losing cannot sink a 5/7 result** | ✅ still `continue` |
| Intent regression on a **gap** probe overrides a 5/7 `continue` | ✅ `intent_regression` |
| Missing pair, missing dimension | ✅ exit 1 |
| No verdicts → refuses to infer | ✅ `NO_VERDICTS` |
| **Position bias alone cannot reach `continue`** | ✅ (found the §2.1 defect) |
| Blinding balanced within the voting stratum | ✅ |
| Real-run prep refuses contaminated controls | ✅ |
| Real-run prep refuses a key path inside the repo | ✅ |
| No committed real-run artifact reveals the mapping | ✅ |
| Reviewer packet never names an arm | ✅ |
| Control packet is free of Canon | ✅ |
| **The leakage checker itself actually fires** | ✅ |
| Synthetic input is never reported as a result | ✅ |
| No rate or confidence interval is ever emitted | ✅ |

### C-C8 — C4 remains research-only

Web access was **re-tested and is still blocked** — `support.google.com`, `thinkwithgoogle.com`,
`doi.org`, `w3.org` all returned `EGRESS_BLOCKED`; direct `curl` returned nothing.

**No route was upgraded from `not_verified`, and none was guessed.** A dated note now heads the
portfolio stating that `recommended` means "worth your attention", never "cleared to acquire".
Dalvi, ABCD, Cayla & Elson and the rest remain leads. **Nothing ingested. Live Canon remains 19.**

## 4. The residual blocker

### `FRESH_CONTROL_SESSION_REQUIRED`

**The real value gate cannot be run until an independent session authors the generic controls.**
`prepare_real_run.py` refuses to start, and that refusal is tested.

**Why it was not resolved here, stated plainly:** this session had already read the Canon. No
subagent it could launch would have helped — a subagent here shares the same filesystem and can read
`canon/knowledge/` directly, so it would reproduce the contamination with an extra step in between.
Claiming otherwise would have been the dishonest option, and the task explicitly warned against
pretending a session can unsee Canon.

**What unblocks it:** a session given `control-authoring-input.json` and no repository access, writing
12 files to `generic-contexts-real/`. That file is self-contained and proven Canon-free.

## 5. Verification — every command run fresh

| Check | Result |
|---|---|
| `validate_audit_gate_v02.py` | **19 records, 0 errors**, exit 0 |
| `validate_canon003_integrated.py` | **16 / 505 / 54 / 417 / 53 / 111, 0 errors — unchanged** |
| `build_live19_coverage.py` | exit 0 — 19 sources, **17 origins, `exact_exhaustive`**, 56 domains |
| `build_brief_bank.py` | exit 0 — 30 briefs, balance intact |
| `build_oracle_contexts.py` | exit 0 — 12 contexts |
| `build_run_manifest.py` | exit 0 — drift 14.5%, Canon-first 3/7 coverage |
| `build_control_packet.py` | **CLEAN**, `authoritative_intent_exposed: false` |
| `prepare_real_run.py` | **exit 1, REFUSED** — as designed |
| **`pytest tests/`** | **91 passed, 93 subtests** (65 pre-existing + 26 new) |

No PASS above is claimed without a command having been run in this session.

## 6. Not done

- **No source ingested.** Live Canon remains **19**.
- **No real value-gate output or human verdict.** 0 of 24. Every fixture is synthetic and labelled.
- **No brief rewritten.** C-C2 found no defect, so nothing was touched.
- **No spend, purchase, login, gated access or acquisition.**
- **No SPEC or Audit Gate change.** No new vocabulary, relation or version.
- **No historical artifact rewritten** — including the v0 coverage map.
- **No later task started.** C5–C10 remain gated.
- **Nothing modified outside `canon/` and `tests/`.**
- **No merge to `main`.**

---

### What I would put to you first

**The correction pass did not weaken the case for running the gate — it made the gate worth running.**
Twice now, a negative control has caught a bias that would have manufactured a Canon win: context
length, and then position within the voting stratum. Both were invisible in the code and would have
been invisible in the results.

One blocker stands between here and a real run, and it is not a technical one: **somebody has to
author twelve control contexts in a session that has never read the Canon.** Everything else is
ready.
