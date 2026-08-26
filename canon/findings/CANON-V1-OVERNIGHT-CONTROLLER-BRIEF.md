# Canon V1 overnight — Controller Brief

**Task:** `canon/tasks/CANON-V1-OVERNIGHT-PROGRAM.md`, packages C1–C4
**Date:** 26 Aug 2026 · **Branch:** `work/canon-v1-overnight` · **Not merged to `main`**
**Session:** fresh cloud session, zero prior context, no laptop access assumed or used
**Spend: ₹0.** No paid API call, no purchase, no acquisition, no ingestion.

---

## 1. Work packages attempted and completed

| Package | Scope | Status |
|---|---|---|
| **C1** — live-19 coverage rebaseline | 19 sources × 56 domains × 10 packs | **Complete, mechanically verified** |
| **C2** — 30-brief bank + oracle contexts | 30 briefs, early-12 subset, 12 oracle contexts | **Complete, mechanically verified** |
| **C3** — value-gate execution package | prompts, matched controls, blinding, scorer, dry run | **Complete as a package. Not executed** |
| **C4** — gap-closing source portfolio | ≤14 candidates, research only | **Complete, with a verification limit recorded** |

All four ran to completion. **No stop condition fired.** Two constraints were hit and worked around
without expanding scope; both are in §7.

## 2. Quantified deliverables and verification

**A code runner was available** (Python 3.11 + PyYAML), so validators genuinely ran here. Everything
below marked "verified" was executed in this session.

| Deliverable | Quantity | Verification |
|---|---|---|
| Coverage rebaseline | 19/19 sources, 56/56 domains, 10/10 packs | `build_live19_coverage.py` exit 0 |
| Gap ledger | 11 gaps in 4 tiers | derived from the above |
| Brief bank | 30 briefs, exact balance | `build_brief_bank.py` exit 0, fails closed |
| Early-gate subset | 12 briefs | `build_oracle_contexts.py` exit 0 |
| Oracle contexts | 12 files, 6,170 words, 35 Canon refs, 15 sources | rendered from committed extraction **by id** |
| Generic contexts | 12 matched controls | max length drift **14.5%** under a 15% cap |
| Value-gate package | prompts, 2 schemas, 3 manifests, 2 scripts, 5 fixtures | `build_run_manifest.py` exit 0 |
| Source portfolio | 12 candidates (cap 14) | research only |
| **Files added** | **52 files, 11,192 lines**, 4 commits | one commit per package |

**Independent checks that nothing existing was disturbed:**

| Check | Result |
|---|---|
| Audit Gate validator | **19 records, 0 errors**, exit 0 |
| Historical 16-source instrument | **16 books / 505 / 54 / 417 / 53 / 111, 0 errors — byte-identical to `main`** |
| Existing test suite | **65 tests, 93 subtests, all passing** |
| Files modified outside `canon/` | **none** |

## 3. Current live-19 coverage headline

**19 accepted sources are 17 independent intellectual origins.** Two pairs each collapse to one:
*Grammar of the Shot*/*Grammar of the Edit* (companion volumes) and *In the Blink of an Eye*/*The
Conversations* (Walter Murch in both). Computed by calling the committed `independent_origins_ok()`,
never by counting authors.

**The live-19 totals have never been published before: 580 source-knowledge objects, 63 concept
systems, 470 ontology terms, 127 bindings.** The repository held only the frozen 16-source figures.

| Coverage state | Domains |
|---|---|
| `present_multi_origin` | 49 |
| `absent` | 5 |
| `present_but_application_unbound` | 1 |
| `representation_or_evidence_limited` | 1 |

**Three critical domains are empty:** Devanagari/Indic typography, short-form/feed-native grammar,
Indian market & cultural context. **Two more are present but unusable as-is:** product/packshot
photography (all bindings are physical-production candidates) and hooks/openings (all of it assumes a
reader who has already stopped on a page).

### The finding that matters most

**The old v0 coverage map rated the library we own, not the Canon we have — and three of its "strong"
ratings rest on titles that are not accepted knowledge.**

| Domain | v0 rated it strong on | Status |
|---|---|---|
| Hierarchy / attention | Picture This, Non-Designer's, Thinking with Type | **none accepted** |
| Critique process & language | Discussing Design | **not accepted** |
| Judgement quality & bias | Noise, Thinking Fast and Slow, Superforecasting | **none accepted** |

All three are still multi-origin — **on completely different evidence.** The old ratings were right
by accident. Planning on them meant planning on knowledge the Canon does not hold.

Going the other way, four domains are **materially better** than v0 recorded, trade-off reasoning
most importantly: five accepted sources carry explicit trade-off machinery. **The raw material for
cross-source synthesis is present and the synthesis has never been done.**

## 4. 30-brief bank balance

Exactly as the runbook specifies, enforced by a validator that fails closed:

- **10 scenario families × 3 briefs = 30**
- **10 English-primary / 10 Hindi-Devanagari-primary / 10 Hinglish-mixed**
- 12 static / 18 video, every video inside the 6–20 second scope
- 20 product categories, 6 objectives, 13 clear / 9 underspecified / 8 contradictory
- **15 planted contradictions across 8 briefs**, each with its correct handling recorded

**One design choice worth your attention:** every family carries one brief of each language, so
**language is not confounded with scenario family.** If Canon wins the value gate, that win cannot be
an artifact of which families happened to be Hindi — a confound that would have been invisible
afterwards and unfixable without rebuilding the bank.

**And one uncomfortable number.** Cross-referencing C2 against C1:

> **20 of the 30 briefs require the `indian_indic_context` pack. That pack has zero contributing
> sources.** 28 of 30 require `typography_and_copy`, which has no Devanagari source. 18 require
> `editing_pacing_and_short_form`, which has no short-form source.

The briefs were written from the first-product scope, not from what the Canon happens to hold. This
is the clearest single statement of the Canon's distance from its own product.

## 5. Value-gate package readiness

**Ready to run. Not run.** 0 of 24 outputs generated, 0 model calls, 0 human verdicts.

**The package caught two real biases in itself before freezing, and both would have been invisible in
the results:**

1. **The Canon arm was 22–37% longer than its control in ten of twelve pairs.** More context produces
   longer plans and reviewers reward that. The control was strengthened until maximum drift was
   **14.5%**, under a cap the builder enforces by refusing to build.
2. **An unconstrained shuffle put Canon in presentation position A for 9 of 12 pairs.** Assignment is
   now balanced **6/6**. The dry run proves the fix: a synthetic reviewer who always picks whatever is
   shown first scores exactly **6/12** — a tie, in the `stop` band — instead of a Canon win.

**Explicit intent preservation is implemented as a gate, not a tenth score.** A Canon intent
regression where the generic arm preserved intent **overrides the win count**. Verified firing: a
fixture with 12/12 Canon wins and two violations returns `intent_regression`, not `continue`.

**The scorer cannot manufacture a result.** No defaults, no imputation, no "unknown means tie". With
no verdicts it reports `NO_VERDICTS`; with incomplete ones it exits 1 and names what is missing.

**Not verified, and you should know it:** the prompt has never been run against a model, and no human
has ever seen the reviewer packet. Whether the prompt elicits usable plans, and whether reviewers can
apply ten dimensions consistently, are both **unknown**.

## 6. Source portfolio and blocks

**12 candidates against a cap of 14.** Nothing acquired, purchased, downloaded or logged into.

| Recommended | Closes |
|---|---|
| **Dalvi, *Anatomy of Devanagari Typefaces*** (Design Thoughts, 2009) | G1 — **this is CANON-008 Option 2 and needs no IIT Bombay credential** |
| **Google/YouTube ABCD framework** | G2, G5 — short-form and hooks |
| **Cayla & Elson, *Indian Consumer Kaun Hai?*** (J. Macromarketing 2012) | G3 — the empty pack 20 briefs need |
| ***Light: Science & Magic*, chapters beyond ch3** | G4 — extends an already-accepted source |
| **Binet & Field, *The Long and the Short of It*** | effectiveness depth |
| **W3C WCAG 2.2 contrast criteria** | G8 — and gives Eval a numeric criterion the Canon has never had |

**If only three are approved: Dalvi, ABCD, Cayla & Elson** — one per empty critical domain.

### Blocks and honest gaps

- **No access route was verified.** Outbound web fetching is blocked in this session (§7). Every
  route is `not_verified_in_cloud_session`. **No candidate is cleared for acquisition.**
- **Two slots left deliberately empty** — second packshot source and motion design — because no
  identity could be established without inventing a citation.
- **Meta and TikTok slots are `identity_unresolved`.** Searching for official platform guidance
  returned overwhelmingly agency blogs repeating unsourced statistics. **None was admitted.**
- **Two gaps get no source at all, and this is the finding:** cross-source synthesis (G10) and
  physical-to-generative translation (G11) are C7/C8 work. **If the Canon's problem is unsynthesised
  knowledge rather than missing knowledge, buying twelve books makes it worse.** C5 is what
  distinguishes the two cases.

### Lineage traps declared up front, not discovered later

- Dalvi's paper is **`derivative_of`** the blocked CANON-008 thesis.
- *The Long and the Short of It* is **`shared_author` and `same_series`** with an accepted source. It
  deepens one origin; **it adds none.**
- Extending *Light: Science & Magic* raises a real schema question — the Audit Gate binds a record to
  **exact bytes**, so extending in place would invalidate the existing record. **Flagged, not decided.**

## 7. Assumptions and decisions made locally

Where several valid choices existed inside the task, I took the most conservative reversible one.

1. **The v0 map's summary contradicts its own tables.** It claims 52 domains; it has **56**. Also 22
   critical vs 27, 10 weak vs 12, 5 absent vs 4. I **accounted for all 56** (a superset of the
   runbook's "52/52") and **did not edit the v0 map** — historical baselines are not rewritten.
2. **Coverage state is computed, not authored**, except two overrides that carry stated reasons.
3. **Oracle contexts are rendered from committed text by id**, never paraphrased, so the Canon arm
   cannot be accidentally strengthened by a worker writing a better version of what a source said.
4. **Selection at concept-system level by default** — retrieving one member of Murch's Rule of Six
   and dropping the rest would test retrieval damage, not Canon value.
5. **`BR-F07-HI` carries an unsubstantiated efficacy claim** ("doubled my crop"). Recorded **as the
   customer said it**, because the bank records intents and does not approve executions. Flagged for
   you, **excluded from scoring** so it cannot leak into reviewers' judgements.
6. **The venv is not self-ignoring** on Python 3.11, contrary to `canon/HANDOFF.md`. I removed it
   rather than edit root `.gitignore`, which is outside Canon's ownership. Recreate with
   `python3 -m venv .venv && .venv/bin/pip install pyyaml pytest`, run with
   `PYTHONPATH=$PWD .venv/bin/pytest tests/ -q`.

### Two environment constraints, recorded not worked around

- **Outbound web fetching is blocked.** Search works; opening any page returns `EGRESS_BLOCKED`, and
  direct `curl` to any host fails. This limits C4 to search-result evidence. **A missing terminal is
  not an architecture stop and neither is this** — but it does mean no access route was confirmed.
- **GitHub write access is denied.** `git push` returns **403 — "Claude doesn't have GitHub access to
  chawlavaibhav/media-intelligence for your organization"**, and the GitHub API returns
  `403 Resource not accessible by integration`. **See §9 — the work is committed but cannot reach
  GitHub from here.**

## 8. Cross-stream dependencies for Eval and Resources

**Canon owes Eval:**

- The **30-brief bank is ready for sampling.** Eval's later 12 end-to-end workflow briefs should be
  drawn from it. Each brief is tagged with likely capability families as **requirements only** — no
  model, no provider, no measurement method named.
- **Twelve briefs carry exact spoken scripts**; the two-speaker briefs record **turn boundaries
  explicitly**, because the shared plan says Eval's AV work needs them.
- **One Canon finding Eval should see before designing evaluators.** C1 domain E02: *Grammar of the
  Shot* establishes **"defects with no within-frame signature"** — failures that are invisible in any
  single frame and exist only across a pair of shots. **An evaluator that scores frames one at a time
  cannot detect them by construction.** This is a Canon-side observation about measurement design,
  routed rather than acted on, because instrument design is Eval's.
- **Failure vocabulary is the Canon's most harvestable unused asset** — ten of nineteen sources name
  craft failures with named ontology terms. Never consolidated. Available if Eval wants it.

**Canon owes Resources:** nothing tonight. The C9/C10 experiments will need the shared 60 active
commercial assets; no separate Canon pool should be acquired.

**Canon needs from the Controller:** approval of any source identity before ingestion, and a decision
on the CANON-008 slot in light of C4 candidate D1.

## 9. Files and commits

Four commits on `work/canon-v1-overnight`, one per package:

| Commit | Package |
|---|---|
| `f243d91` | C1 — coverage rebaseline, gap ledger, generator |
| `e31d2d4` | C2 — brief bank, early-12, oracle contexts |
| `5c69bd2` | C3 — value-gate package, dry run |
| `124a578` | C4 — source portfolio |

Key paths: `canon/planning/CANON-V1-LIVE19-COVERAGE.{md,yaml}`, `CANON-V1-GAP-LEDGER.md`,
`CANON-V1-SOURCE-PORTFOLIO.md`; `canon/experiments/v1/brief-bank/`;
`canon/experiments/v1/value-gate/`.

> ### ⚠ The branch could not be pushed
>
> Both `git push` and the GitHub API return 403. **These four commits exist only in this session's
> container**, which is reclaimed after inactivity. A git bundle and a patch file have been sent to
> you separately so the work is recoverable.
>
> To restore write access: an org admin installs the Claude GitHub App at
> `github.com/apps/claude/installations/select_target`, or you reconnect GitHub from claude.ai
> settings. To restore the work from the bundle:
> `git fetch canon-v1.bundle 'refs/heads/*:refs/heads/*'` — or apply the `.patch` with `git am`.

## 10. Explicitly NOT executed

- **No source ingested.** No source directory created. **Live Canon remains 19.**
- **No value-gate execution.** 0 of 24 planning outputs, 0 LLM experiment calls.
- **No human judgement invented.** No verdict exists; the scorer cannot produce one.
- **No acquisition, purchase, login, account creation, click-through acceptance, gated access or DRM
  interaction.** No unofficial mirror, rip or torrent sought or used. ₹0 spent.
- **No SPEC-01/03/04/05 or Audit Gate change.** No new vocabulary, no new relation, no new version.
- **No extraction, audit record, or historical artifact modified** — including the v0 coverage map,
  whose defect is recorded rather than fixed.
- **No Production IR, Planner or routing work. No RAG or retrieval built.** C8 deliberately tests
  consumption forms before any retrieval infrastructure exists.
- **No other stream's files touched.** Nothing outside `canon/` modified.
- **C5–C10 not started.** They are gated on your review of this package.
- **No merge to `main`.**

---

### The one thing to decide first

**Run the value gate before approving any source.** The Canon has 49 multi-origin domains and no
synthesis across any of them. If C5 comes back `mixed` or `stop`, the problem is that the Canon is
unsynthesised, and twelve more books would make an unsynthesised corpus larger rather than better.
The gate costs 24 planning outputs and one reviewer's time. **Source expansion costs money and
cannot be undone.**
