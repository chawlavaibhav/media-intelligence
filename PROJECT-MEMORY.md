# Project Memory

**The canonical entry point for this project.** Read this first, every session, before anything else.

**Maintained by:** the Repository Governor (see `governance/GOVERNOR-CONTRACT.md`).
**Last Governor reset:** 25 Aug 2026, task GOV-001, against `main` at `00ea9b067229cd992b77b7d6e0958df35178b01b`.
**Last refresh:** 26 Aug 2026, task GOV-003, against `main` at `2cd29037c713e2fb9c77551ddc40ada7cc62f50b`
(`governance/reviews/GOV-003-MACRO-RESEARCH-INTEGRATION-REVIEW.md`). Task GOV-002 was assigned but
never executed and is superseded — `governance/status/2026-08-26-GOV-002-SUPERSEDED.md`.

## What this document is — and is not

This is a **map to the truth, not the truth itself.** It is a curated synthesis that tells you what
is currently the case and points you to the thing that actually establishes it.

**Where project truth comes from, in order:**

1. **Committed evidence and artifacts** establish factual state.
2. **Deterministic validators and reproducible calculations** establish mechanically checkable
   invariants.
3. **Explicit durable Controller decisions** establish project decisions.
4. **This document** is the canonical entry point to those three. It is **not** a competing source
   of truth and it establishes nothing on its own.

**If this document conflicts with the underlying evidence, the evidence wins and this document is
defective.** That is a governance defect to report, not a discrepancy to argue about.

The Repository Governor is **downstream of all three authorities above**. It maintains this map's
coherence, navigability and honesty about the evidence. **It does not manufacture or certify truth,
and it does not determine whether Canon, Eval or Resources work is scientifically or technically
correct** — that judgement belongs to the owning stream and the Controller.

**Provenance labels used below.** Each label says *what owns the fact*, not who vouched for it.
`[repo]` = established by a committed artifact, and memory was checked against it during GOV-001 —
the artifact is the authority, and it is named. `[decision]` = a durable Controller decision exists
in the repository at the path given. `[agent-reported]` = a worker reported it and it has not been
independently reproduced; it remains agent-reported until it is. `[external]` = external research
snapshot, not repository truth. `[unresolved]` = not established by anything.

---

## 1. What this project is

An **API-native media production intelligence layer**. It is not a new foundation model. It sits
between what a customer asks for and the ecosystem of image/video/audio generation tools, and
continuously chooses the cheapest reliable path to a commercially acceptable result.

The long-term primary metric is **Cost per Accepted Outcome** — what it costs to reach an output a
customer will actually use — not cost per generation. A model that is cheap per image but needs six
retries is not cheap.

Full statement: `coordination/PROJECT-CONTRACT.md`.

## 2. How the work is divided

Three domain streams produce evidence, plus two control roles.

| Role | Owns | Explicitly does not own |
|---|---|---|
| **Canon** | Durable creative/production knowledge: what a good outcome must achieve, what techniques exist, what to inspect to judge fitness. | Which model is best today, prices, provider quirks. |
| **Eval / Capability Lab** | What to measure and how, then measuring it empirically. Produces the Capability Registry. | Inventing creative quality from first principles — Canon supplies the dimensions. |
| **Resources** | Independent media/data for testing: discovery, licensing, sampling, manifests, integrity. | Defining Canon truth; choosing examples that flatter a hypothesis. |
| **Controller** (human) | Product direction, architecture, task authorization, accept/reject, merges. | — |
| **Repository Governor** | Repository coherence, this document, integrity review, audits. | Project strategy; domain methodology. |

Charters: `canon/CHARTER.md`, `eval/CHARTER.md`, `resources/CHARTER.md`.
Governor role: `governance/GOVERNOR-CONTRACT.md`, approved design in
`docs/superpowers/specs/2026-08-25-repository-governor-project-memory-design.md`.

## 3. Frozen decisions that constrain current work

These are not reopened without an approved integration task. Full list: `coordination/PROJECT-CONTRACT.md`
("Major separations"). The ones that most often trip up a new session:

1. **Creative IR ("what should exist") is separate from Production IR ("how today's tools make it").**
   Production IR **does not exist yet**. `[repo]`
2. **Book knowledge is never evidence about model capability.** The Capability Registry is empirical
   only. Its schema and validator exist (`eval/registry/`) and it holds **zero rows** — no model has
   ever been measured. `[repo]`
3. **Public dataset labels are one source's observations, not our ground truth.** `[decision]`
4. **A worker's recommendation is not an approved decision.** A recommendation becomes a decision
   only when the Controller records a disposition. In this repository a durable Controller decision
   may currently live in any of: a dedicated decision record (`canon/decisions/`, `eval/decisions/`),
   an approved task file or spec, a Controller Brief carrying an explicit Controller disposition, an
   approved proposal, or a frozen machine-readable decision artifact. **`coordination/DECISION-LOG.md`
   is the index for discovering them.** The form varies; what does not vary is that a Controller
   disposition must exist. Normalising these into dedicated decision records is a routed improvement,
   not a current requirement.
5. **Historical baselines are never rewritten to match current numbers.** Superseding is allowed;
   silent mutation is not.

## 4. Current state by stream

### First, the V1 architecture baseline — accepted 26 Aug, and the thing the macro reset re-examined

On the night of 25 Aug the three streams each produced a V1 design layer. The Controller reviewed
them, assigned correction passes, and **accepted and merged all three**. `[decision]`
(`coordination/decisions/CONTROLLER-V1-OVERNIGHT-INTEGRATION-2026-08-26.md`.)

You need to know these four artifacts exist, because everything since is described relative to them.
**All four are design and measurement scaffolding. None of them is empirical evidence about any
model.** `[repo]`

| Artifact | What it is | Where |
|---|---|---|
| **30 authored commercial briefs** | Hand-written customer briefs with objectives, audiences and acceptance criteria. A **designed probe bank**, never evidence of what customers actually ask for. | `canon/experiments/v1/brief-bank/` |
| **36-capability contract** | The list of things a commercial media output can be measured on — object count, exact text, person identity, lip sync, and so on — with the instrument and readiness recorded for each. | `eval/v1/capability-contract.yaml` |
| **100-item Eval bank** | Reusable test items designed so one generation can be measured many times ("generate once, measure many") rather than one generation per question. | `eval/v1/bank/` |
| **Persistence contract v2.1** | How an attempt, the artifact it produced, the measurements taken on it and its cost are stored so a cost figure can always be traced back to a real call. **One provider/API/transform call = one trial.** | `resources/v1/EMPIRICAL-ARTIFACT-MANIFEST-SCHEMA.yaml` |

Also accepted: **Creative IR v0.1** as the current experimental "what should exist" representation,
six evaluator families as a baseline, and the rules **repeat is not retry** and **failed and refused
attempts are kept individually, never collapsed into a counter**.

**Verified mechanically during GOV-003:** the bank holds exactly 30 briefs, the contract exactly 36
dimensions, the Eval bank exactly 100 items, and the Registry exactly 0 rows.

### Canon — 19 live accepted sources; historical CANON-003 baseline frozen at 16

Two numbers exist and must not be confused. `[repo]`

| Number | Value | Meaning |
|---|---|---|
| Historical CANON-003 / CANON-004 method-test corpus | **16** | Fixed forever. The frozen set the extraction batch closed on and the Audit Gate was tested against. |
| **Live accepted Canon** | **19** | What the Canon actually holds today. |

Verified mechanically by GOV-001: `canon/knowledge/current/` holds exactly 19 source directories,
`canon/audit/records/` holds exactly 19 audit records, and the two sets match one-for-one with no
orphans on either side. `canon/validation/validate_audit_gate_v02.py` reports 19 records and 0
errors. The historical instrument `canon/validation/validate_canon003_integrated.py` still reports
16 books / 505 source-knowledge objects / 54 concept systems / 417 ontology terms / 53 concepts /
111 bindings, 0 errors — unchanged, as intended.

**Admission method: Post-Extraction Audit Gate v0.2**, authoritative since CANON-005. `[decision]`
It asks five questions per source after extraction — representation integrity, evidence origin,
application fit, pairwise source lineage, technology contingency — and `evidence_insufficient` is a
legitimate completed outcome, not a failure. Normative text: `canon/audit/AUDIT-GATE-v0.2.md`.
Decision: `canon/decisions/CANON-004-ADOPT-AUDIT-GATE-2026-08-25.md`.

**The gate governs use, not storage.** An unaudited or stale-audited source stays in the repository
as evidence but may not be used for cross-source promotion, downstream product use, or
Canon-consumption/retrieval.

How the Canon got from 16 to 19:
- **CANON-006** admitted the two deferred reserve sources, *Master Shots* (Kenworthy) and
  *The Conversations* (Ondaatje). 16 → 18. It also added the lineage relation
  `shared_primary_informant`, because *The Conversations* is substantially Walter Murch speaking and
  the corpus already held Murch's own *In the Blink of an Eye* — different author, publisher and
  year, same intellectual origin. The relation is **pairwise and symmetric**, and incidental
  quotation of the same person does not qualify. `[repo]` `[decision]`
- **CANON-007** admitted *Effectiveness in Context* (Binet & Field). 18 → 19. It added the
  representation-loss category `figure_semantic_binding_lost`, for material where a chart's text and
  numbers survive extraction but which number belongs to which category does not. `[repo]`
- **CANON-008 STOPPED at its acquisition gate and ingested nothing.** The official D'source/IDC
  record for Girish Dalvi's *Conceptual Model for Devanagari Typefaces* publishes only a 3-page
  abstract; the full thesis sits behind IIT Bombay authentication, which was not attempted. **This
  is the gate working, not a failure.** Live Canon stays 19. `[repo]`
  Brief: `canon/findings/CANON-008-CONTROLLER-BRIEF.md`.

**The Canon still has no accepted Devanagari-structure source.** *Thinking with Type* remains
blocked on structural column interleaving and is not in the 19.

Stream detail: `canon/HANDOFF.md`. CANON-009 (returned, unmerged) added no source and changed nothing here — live Canon is still 19.

### Eval — a battery built and human-validated; no checker has ever been run

**Nothing in this stream currently licenses trusting any evaluator's numbers.** No checker qualified,
no model benchmarked, no Capability Registry entry, ₹0 API/generation spend. `[repo]`

**EVAL-005 is the live artifact: a Devanagari exactness battery.** It targets the failure that costs
money — we ask a generator for a specific string, it produces something *subtly* wrong, and the
checker says "matches", shipping a defect with a passing grade. Because the images are rendered from
strings we chose, each item's **match/mismatch label is known by construction**; no annotator decides
it. That removes human annotation from the *label*, **not humans from validation** — review was still
required, and performed, on whether each base word is valid Hindi, whether the rendered difference is
perceptible, and the exclusion decision that followed.

Two views exist and must not be confused: `[repo]`

| View | Contents | Status |
|---|---|---|
| Original build | 106 items — 53 match / 53 mismatch, 53 base words | **Historical.** What the reviewer actually saw. Unchanged. |
| **Validated view** | **96 items — 48 match / 48 mismatch, 48 base words, 33 hard opportunities, 20 failure classes** | **Authoritative for any checker run.** |

**Human validation is complete and the Controller chose PRUNE, DO NOT REBUILD.** `[decision]` One
Hindi-competent reviewer answered 98 of 98 questions; five of 53 base words were rejected, excluding
10 items which were **not replaced** — preserving the identity of items already reviewed rather than
opening a new validation surface. GOV-001 verified the frozen record mechanically, recomputing and
matching both SHA-256 hashes.

**One reader is not ground truth.** The record says so itself — "PROVENANCE, NOT GROUND TRUTH" — and
no threshold, rate or checker claim may be derived from it. The 8.68% figure attached to the
validated view is a sizing calculation under an independence assumption the battery explicitly does
**not** establish (`independence_status: NOT ESTABLISHED`); it is never a checker's error rate. The
qualification gate itself is deterministic — **zero false passes** — and needs no probability model.

**EVAL-004 was stopped by the Controller, not completed.** `[decision]` One 54-item Reader-A pass
exists and there is **no Reader B**, so no two-reader reference exists. Reader A is exploratory only;
no checker may be qualified or ranked from it, and it must not be resumed.
`eval/decisions/EVAL-004-STOP-2026-08-24.md`. **EVAL-003** remains closed and merged — a 54-item
Hindi-primary signage calibration pack, available if that screen is ever wanted.

**The founding result of the stream:** a capability number without its checker is not a measurement.
An early study gave 14 Hindi images to three checkers; one AI vision model returned **6 false
passes** — it looked at visibly misspelled signs and called them correct. That study is explicitly
preliminary. `eval/findings/FINDINGS-01-can-we-check.md`.

Stream detail: `eval/HANDOFF.md`. Current Eval work is EVAL-007 (returned, unmerged) and EVAL-008
(active) — see the macro-reset section below.

### Resources — corpus acquired and closed; RES-003 returned and is unmerged

**34,786 items / 5.70 GB across 8 acquired sources; 4 blocked.** `[repo]`
GOV-001 recomputed every headline figure directly from `resources/manifests/corpus-pilot-v0.jsonl`:
34,786 records, all `validation_status: ok`, 34,586 distinct SHA-256 hashes, 200 duplicates
(27 within a single source, 173 spanning two sources), 5,702,337,356 bytes. Every per-source count
matches the handoff table exactly.

**The most important Resources finding: two of the three Devanagari sources are not independent of
each other.** IndicSTR12 and IIIT-ILST are both CVIT / IIIT Hyderabad releases sharing 173
byte-identical files — 98.3% of IIIT-ILST's scene photographs. Treat them as **one source lineage**
for any holdout claim. **BSTD is the only genuine cross-lineage reserve and is held untouched.**

Two related traps recorded here, both real: hash-based deduplication cannot see content reuse
(1,205 of 1,214 IIIT-ILST crops derive from shared parent photographs while sharing no bytes), and
"media acquired" is not "usable annotated records" — 4,476 Devanagari images are 551 annotated
photographs plus 3,925 single-word crops, of which 3,924 resolve to a transcription.

**Rights posture: internal research and evaluation only.** If any result is ever published or shown
to a customer, the rights question must be reopened first.

Stream detail: `resources/HANDOFF.md`. RES-003's rebaseline reconfirmed every headline figure above from the committed manifest on 26 Aug, and GOV-003 reran it.

### The 26 August macro reset — why the plan changed, and where the three streams now stand

**What went wrong, in one sentence.** Before spending money on the first paid benchmark, the
Controller noticed that the 30 authored briefs and the 36-capability contract were starting to
*define* the product rather than *test* it — the benchmark was becoming the specification. `[decision]`

**The rule adopted instead:** research what customers actually request, independently research what
today's models can and cannot do, independently research what evidence and persistence the project
needs — and only then integrate the three and freeze the real empirical programme.

Three research programmes ran on that basis and **all three have returned.** Each spent ₹0, made no
model or evaluator call, and created no Registry entry. `[repo]`

| Programme | Branch | What it produced |
|---|---|---|
| **CANON-009** | `work/canon-009-request-space` | A map of real media-generation request patterns from 13 public sources, a proposed 14-part Media Request Grammar, and a measured audit of the 30-brief bank against it. |
| **EVAL-007** | `work/eval-007-capability-workflow` | An external audit of the 36 capabilities, an evaluator/qualification landscape, a four-layer benchmark v2 proposal, and a cost forecast that refuses to produce a total. |
| **RES-003** | `work/res-003-evidence-topology` | Dataset rights and independence research, a corpus rebaseline, a leakage/protected-set proposal, and a proposed whole-outcome persistence topology with a working cost-recomputation engine. |

**As of this refresh — `main` at `2cd29037`, 26 Aug 2026 — none of the three is merged.** `[repo]`
Their evidence therefore lives only on those branches. The Repository Governor reviewed all three
for repository coherence in GOV-003 and found them safe to merge on coherence grounds; **merging is
the Controller's act.** If they have since been merged, this paragraph is historical.

**The single most consequential finding, and it is a gap rather than a result.** CANON-009 measured
the 30-brief bank against the request patterns it found and got an inversion: `[repo]`

| | Best-evidenced in real requests | Briefs in our bank |
|---|---|---|
| Edit a supplied asset | 82,976 real requests in one corpus, plus two more | **0** |
| Animate a supplied image | 1.70M+ real requests | **0** |
| Multi-turn refinement | 95,000 sequences | **0** |
| Variant / campaign sets | qualitative reports only | **0** |
| Exact text in the image | **no real-user frequency figure exists anywhere** | **28 of 30** |
| Speech / voiceover | **no corpus covers audio at all** | **12 of 30** |

Read this correctly. It does **not** mean the bank is wrong, and it is **not** market-share
evidence — every corpus involved is a model-interface corpus shaped by who used that interface. It
means the bank is a **narrow probe of a wide space**, and the two operations the world most
demonstrably asks for are currently untested. The bank's own strength — every brief carries an
objective, an audience and acceptance criteria — is something **no public corpus has**.

These figures were reproduced mechanically during GOV-003 by rerunning Canon's own measurement
script against the committed bank.

### What the Controller adopted from the three programmes

Authoritative record: `coordination/decisions/CONTROLLER-MACRO-RESEARCH-INTEGRATION-2026-08-26.md`.
`[decision]` Summarised below; that file governs, and the worker branches remain **proposals** except
where it says otherwise.

**On what the customer asked for.**
- **The requested operation becomes an explicit field** on the Normalized Request — did the customer
  ask to generate, edit, animate, restore, extend, compose or produce variants. The exact machine
  vocabulary is not frozen yet.
- **It must stay separate from the production route.** If a customer says *"change the background of
  this photo"*, the requested operation is **edit**. Whether the Planner later does that by
  inpainting, image-to-image or segment-and-composite is a **production choice**, not customer
  intent. Collapsing the two destroys the ability to tell a misread request from a bad plan.
- **Output sets are first-class:** one deliverable, several variants, or a campaign set — and whether
  acceptance is per output or for the set. This changes the cost per accepted outcome directly.
- **Multi-turn requests are recognised but not solved.** No schema is frozen, and it must not block
  the first paid benchmark.
- **The 30 briefs stay byte-identical** as the frozen generation-core / value-gate bank. A separate
  **request-coverage extension** is authorised before end-to-end paid benchmarking, covering at
  minimum edit-a-supplied-asset, animate-a-supplied-image and variant/campaign-set requests.

**On what gets measured.** The 36 stay as the baseline; specification work is approved for a v2 that
splits 2D from depth relationships, separates spoken-word correctness from pronunciation, separates
reproducibility from repairability, broadens hand anatomy into human-anatomy integrity, makes
wardrobe invariants explicit within person identity, and adds four capabilities: camera/framing
fidelity, sequence and state continuity, technical visual integrity, and voice identity across
assets. **No target capability count is frozen.** Style-reference fidelity, cross-asset identity and
campaign-set consistency are deliberately *not* yet separate capabilities.

**One correction the Controller made to Eval's proposal, worth understanding.** Compound briefs get
prerequisite links, so a requirement that depends on a failed one is not scored as though it passed.
But a blocked requirement must **not** be recorded as ordinary "not applicable". If the product was
never rendered, the logo cannot be inspected — yet the customer still asked for the logo. A distinct
state (something like `blocked_by_prerequisite_failure`) will be specified: at diagnostic level it
means *not directly inspectable because something it depended on failed*; at outcome level the
requirement stays **unsatisfied**. Never a pass.

**On production conditions.** No single "complexity score". Every empirical result must carry the
conditions it was produced under — duration and delivery size, how much content was asked for,
reference type and quality, shot structure, motion and camera load, constraint load, language and
speaker topology, workflow mode, input quality, decision provenance and output-set structure.
Benchmark v2 has four separate layers — atomic probes, compound scenarios with prerequisites, sparse
condition sweeps, and end-to-end accepted outcomes. **No cartesian product is authorised**; 11
conditions at two levels each is already 2,048 combinations before a model is chosen.

**On evidence and cost.** The outcome topology direction is approved:
`job → outcome → sequence_or_asset_set → production_unit → production_step`. Artifacts may have
several parents in a defined order; local deterministic transforms may create artifacts **without
inventing a provider trial**; and **one call = one trial is unchanged**. Historical v2.1 records are
never backfilled with outcome context they never had.

**Fully-loaded Cost per Accepted Outcome is the primary business metric** — successful, failed and
refused calls, retries, paid transforms, evaluator calls, repairs, material local compute, required
human review time, and rejected revisions belonging to the same journey. Report API/tool-only cost
alongside it as a diagnostic. **Shared upstream costs are counted once**: RES-003 demonstrated that a
naive walk over a reused artifact overstates cost by 13.3% on its own worked example.

**On dataset independence.** `request_discovery` becomes its own evidence role, and request lineage
is tracked separately from media lineage. A discovery corpus and a benchmark drawn from the same
request pool **cannot** be presented as independent generalisation evidence — rephrasing prompts
does not erase ancestry, and a taxonomy derived from a source inherits that source's lineage.
Unknown lineage is **indeterminate**, not independent. The Controller chose to preserve
Arena-T2I-Hard for Eval methodology rather than make raw LMArena data load-bearing for discovery.

**On resource packs.** The existing four-pack architecture stands; **no fifth pack.** Expected
changes are metadata and grouping — reference-to-production-step lineage, more framing diversity for
person identity, longer continuous speech, commercial Hinglish and brand-name material, grouped
campaign examples, and both short and longer video durations. **Exact pack sizes are not frozen.**

### EVAL-008 — model selection first, sourcing second

A fourth lane is open: `eval/tasks/EVAL-008-CLOUD-MODEL-ACCESS-RESEARCH.md`, branch
`work/eval-008-model-access`. Its governing rule is that **which models to test is decided
independently of where credits happen to be available**; only then is sourcing checked, in the order
Frontier Clouds → fal → direct or other provider.

**Status from GitHub evidence, checked in GOV-003: assigned and active, with 0 of its 9 deliverables
produced.** The directory they must live in, `eval/model-access/2026-08-26/`, **does not exist on any
branch.** `[repo]` **No paid model roster is frozen anywhere in this repository.**

### Architecture objects — what does not exist yet

**Production IR, the Production Planner, routing, and any Canon-consumption / RAG / training
experiment are unapproved and not implemented.** The Capability Registry exists as a schema and an
empty file. `[repo]` Do not assume otherwise from a schema draft or a plan document; drafts exist,
implementations do not.

## 5. Current gate — research has run; paid execution is still blocked

**The GOV-001 audit freeze has been re-scoped twice and no longer reads as written.** `[decision]`
It was re-scoped on 25 Aug (`coordination/decisions/CONTROLLER-POST-AUDIT-UNBLOCK-2026-08-25.md` §6)
and again on 26 Aug when the Controller assigned four domain research tasks. **Any document still
saying "all new domain work is frozen" is stale** — including `coordination/WORKSTREAM-STATUS.md`,
which was flagged in GOV-003 and is the Controller's to refresh.

**`coordination/CONTROL-STATE.md` is authoritative for what is currently authorised.**

### What is authorised now

- **EVAL-008 only** — model selection, then sourcing. Research and documentation; no calls, no spend.

### What is blocked, and is not made authorised by any older file

**No paid empirical work may begin.** `[decision]` `[repo]`

- **0 qualified evaluators.** No checker or perceptual instrument has ever been qualified, so no
  automated judgement can currently gate anything.
- **0 empirical Registry entries.** No current model has ever been measured. Verified: the registry
  file holds 0 rows.
- **No paid benchmark budget is authorised.** Any earlier figure — the ₹600–2,100 checker roster,
  the ₹16,000 EVAL-006 cap, the historical 204 / 520 generation counts — is a **superseded
  calculation, not a budget.**
- **`EVAL-006` is PAUSED — DO NOT EXECUTE**, and its spend authority was explicitly withdrawn.
  (`coordination/decisions/CONTROLLER-PAUSE-EVAL-006-PENDING-MASTER-PLAN-2026-08-26.md`; the task
  file itself opens with the pause.) It must not be resumed or repurposed.
- **Historical E7 paid admission and E8 deep qualification remain blocked.**
- **No new controlled-pack acquisition is authorised.**
- **The Canon value gate remains unrun.**

**No worker may infer authorisation from an old task file.** If a task file and a current Controller
decision disagree, the decision wins and the task file is stale.

### What has to happen before any money is spent

From the Controller's integration decision, in the order it gives:

1. Governor coherence review of the three research branches, then merge of the accepted evidence —
   **the review is done (GOV-003); the merge is the Controller's.**
2. EVAL-008 returns a model roster and a sourcing map.
3. Formal specifications for the Normalized Request additions, Capability Contract v2, the condition
   contract and outcome topology v3.
4. The request-coverage brief extension is defined.
5. Evaluator qualification needs are mapped to the v2 capabilities.
6. Controlled-pack requirements are refrozen.
7. The model/workflow roster and access routes are fixed.
8. A fresh generation + evaluator + human-cost forecast is produced.
9. **The Controller explicitly approves the paid budget.**

## 6. Lessons already paid for — do not rediscover these

- **A validator that aborts a unit on a parse error under-reports, and the shortfall is invisible in
  its own output.** This hid 10 real errors until CANON-004 found them.
- **An audit record is only valid for the exact bytes it audited.** Any change to a source's
  machine-consumed artifacts fails its audit as stale. There is deliberately no refresh shortcut.
- **Different authorship is not independent origin.** Companion volumes and shared informants both
  defeat any independence check built on bibliographic metadata.
- **Bindability is not evidence quality.** The source with the most product bindings has the weakest
  support. Never rank sources by binding count.
- **Test tooling with deliberately broken inputs, not only correct ones.** Negative-control fixtures
  immediately exposed three real defects in the Eval harness, including a run that raised integrity
  errors and still exited successfully. **None was visible from reading the code.**
- **An empty check is not a passing check.** A suite with nothing in it must fail, not report
  success.
- **A statistical bound over correlated items is not a bound**, and de-correlating items does not
  make them independent. Count opportunities, not items — and say `independence_status: NOT
  ESTABLISHED` out loud.
- **Descriptions can be wrong for months while every integrity check passes.** Hash and decode checks
  prove files are intact; they prove nothing about whether the prose describes them.
- **Do not infer media rights from a code licence.** A repository's MIT licence says nothing about
  the dataset it ships.
- **A benchmark left unchecked starts defining the product.** The 30 briefs and 36 capabilities were
  built as tests and were quietly becoming the specification of what the product is for. Catching
  that cost one research cycle; not catching it would have cost the paid programme.
- **Scoring parts of a brief independently inflates the score exactly where the output is worst.**
  If the product was never rendered, its logo cannot be inspected — but scoring the logo as a pass
  makes the most complete failure return the highest number.
- **A prompt is not a brief.** Every large real-user corpus records what someone typed into a tool
  after deciding what they wanted. None records the objective, the audience or what would have been
  accepted. That gap is in the world, not just in our access to it.
- **Two datasets can share ancestry without sharing a single byte.** Two prompts drawn from the same
  arena pool are not independent, and every byte-level and content-level check reports them clean.

## 7. Known limitations and unresolved questions

- **The Canon has no accepted Devanagari-structure source.** `[repo]`
- **No checker is qualified; the project has taken no empirical capability measurement.** `[repo]`
- **The EVAL-005 battery is not reproducible from GitHub alone.** Its built items live under a
  git-ignored `build/` directory and the pinned font is a proprietary system asset that is not
  committed (provenance is recorded instead). The committed record fingerprints the build by SHA-256
  so a rebuild can be checked, but a fresh clone on a machine without that font cannot reconstruct
  it. `[repo]`
- **The Resources composition verifier cannot run from a fresh clone** — it reads the git-ignored raw
  corpus. `[repo]`
- **Whether the Devanagari transcriptions survive checking by a Hindi reader is untested.** `[unresolved]`
- **CANON-001 and CANON-002 outputs are not on `main`.** Their briefs, findings and two extracted
  knowledge directories exist only on unmerged branches, although `canon/tasks/CANON-003.md` cites
  them as evidence. Routed to Canon/Controller by GOV-001. `[repo]`
- **The EVAL-004 Reader-A freeze and attestation are not on `main`** — only on `work/eval-004`,
  although the merged stop decision refers to retaining that evidence. Routed to Eval/Controller. `[repo]`
- **How a Registry entry should lose confidence as it ages has deliberately not been decided.**
  Inventing a decay formula now would encode a guess as a finding. `[unresolved]`
- **Every external figure in the macro research is search-verified, not read.** All three cloud
  research sessions had outbound page fetching blocked; search worked, opening a page did not. Each
  worker recorded this. The Controller separately verified the load-bearing figures on primary
  surfaces before deciding. Any figure that would drive a spend decision must be re-verified.
  `[external]`
- **No provider price, endpoint, limit or model identity is established anywhere in this
  repository.** EVAL-007 probed 22 official provider domains and resolved **zero** rows; its cost
  forecast returns `null` for all nine price cells and refuses to produce a total. `[repo]`
- **`coordination/WORKSTREAM-STATUS.md` is stale** — it still describes a total audit freeze with no
  task open in any stream. Flagged in GOV-003 and routed to the Controller; it is outside the
  Governor's write scope. `[repo]`
- **`coordination/DECISION-LOG.md` indexes none of the six 26 Aug Controller decisions**, although
  this document calls it the index for discovering them. Read `coordination/decisions/` directly
  until it is refreshed. Routed to the Controller in GOV-003. `[repo]`
- **The real-world frequency of the requirements our bank tests most heavily is unknown.** No corpus
  reports how often users ask for exact text in an image, for a product rather than a person, for a
  particular duration, for speech at all, or in Hindi/Hinglish. Seven such questions are listed
  rather than estimated, because an estimate becomes a number someone later plans against.
  `[unresolved]`
- **One documentation discrepancy in the Resources corpus is open:** the manifest records 364 BSTD
  "other language" items where committed prose says 351. Resolving it needs raw annotation files no
  cloud session can reach. Deliberately not corrected in either direction. `[repo]`

## 8. External research — context, not authority

Some source-discovery and acquisition work was done outside GitHub. It is an **external research
snapshot** and never competes with repository truth. `[external]`

GOV-001 inspected two artifacts dated 24 Aug 2026 in the operator's local Downloads folder — a Canon
expansion report and a candidate-universe workbook. **Both are contradicted by the repository on
their central arithmetic:** they state live Canon is 16 and that *Master Shots* and *The
Conversations* are not accepted, but CANON-006 admitted both and live Canon is 19. Their 22-source
portfolio and projected total of 38 rest on that stale base and **must be recomputed before use**.
*Effectiveness in Context*, listed there as a candidate, has since been ingested as CANON-007. Two
further named artifacts were **not found and not inspected**; any claim resting on them is
unverified. `[unresolved]`

**Everything external in the 26 Aug macro research is search-verified, not read** — see §7. The
Controller performed a separate independent verification pass on the load-bearing figures before
deciding; that is recorded in the integration decision and is the Controller's evidence.

**One qualitative experiment is recorded for completeness and is not a benchmark.** A small informal
comparison of advertising concepts, one arm using Canon-derived principles and one not, was judged by
the operator to favour the Canon arm. It is anecdotal, ran outside the Eval system, and licenses no
capability claim and no Registry entry. `[external]`

## 9. Milestones

| Date | Milestone | Evidence |
|---|---|---|
| 23 Aug 2026 | SPEC-02's single-atom schema split into source knowledge / bindings / ontology; Canon scope restored after a category-error finding | `coordination/DECISION-LOG.md` |
| 24 Aug 2026 | Three workstreams started; RES-001/002 corpus acquired and closed | `resources/tasks/`, PR #2 |
| 24 Aug 2026 | CANON-003 extraction stopped at 16 accepted books, then integrated | `canon/decisions/CANON-003-STOP-AT-16-2026-08-24.md`, PR #4 |
| 24 Aug 2026 | EVAL-003 calibration pack merged; EVAL-004 stopped after Reader A | PR #3, `eval/decisions/EVAL-004-STOP-2026-08-24.md` |
| 25 Aug 2026 | Audit Gate v0.2 designed, adopted and made authoritative | `canon/decisions/CANON-004-ADOPT-AUDIT-GATE-2026-08-25.md`, PRs #6/#7 |
| 25 Aug 2026 | CANON-006/007 take live Canon 16 → 18 → 19 | PRs #9, #10 |
| 25 Aug 2026 | EVAL-005 human validation frozen; battery pruned to the 96-item view | PR #12 |
| 25 Aug 2026 | CANON-008 stopped at the acquisition gate | PR #13 |
| 25 Aug 2026 | Repository Governor approved; GOV-001 reset audit | PR #14, `governance/audits/2026-08-25-initial-repository-hygiene-audit.md` |
| 26 Aug 2026 | V1 architecture accepted and merged: 30-brief bank, 36-capability contract, 100-item Eval bank, persistence v2.1 | `coordination/decisions/CONTROLLER-V1-OVERNIGHT-INTEGRATION-2026-08-26.md`, PRs #17/#18/#19 |
| 26 Aug 2026 | EVAL-006 paused before execution; its spend authority withdrawn | `coordination/decisions/CONTROLLER-PAUSE-EVAL-006-PENDING-MASTER-PLAN-2026-08-26.md` |
| 26 Aug 2026 | Macro reset: paid benchmarking paused, three independent research programmes commissioned | `coordination/decisions/CONTROLLER-CLOUD-MACRO-RECALIBRATION-2026-08-26.md` |
| 26 Aug 2026 | CANON-009, EVAL-007 and RES-003 return; Controller issues the joint integration disposition | `coordination/decisions/CONTROLLER-MACRO-RESEARCH-INTEGRATION-2026-08-26.md` |
| 26 Aug 2026 | GOV-003 coherence review of the three research branches — PASS with non-blocking notes; branches unmerged at review | `governance/reviews/GOV-003-MACRO-RESEARCH-INTEGRATION-REVIEW.md` |

## 10. Authority map — which file proves what

| Question | Authoritative file |
|---|---|
| What is the product and what are the frozen separations? | `coordination/PROJECT-CONTRACT.md` |
| How must every worker communicate? | `shared/COMMUNICATION-STANDARD.md` |
| What is live in each stream right now? | `coordination/CONTROL-STATE.md`, then this document |
| Per-stream status and next gate | `coordination/WORKSTREAM-STATUS.md` — **STALE as of 26 Aug 2026.** It still describes a total audit freeze with no task open in any stream. Use `coordination/CONTROL-STATE.md` instead until the Controller refreshes it. |
| How do I start a session, approve a task, escalate? | `coordination/RUNBOOK.md` |
| When may a worker run unattended? | `shared/AUTONOMY-POLICY.md` |
| What has the Controller actually decided? | `coordination/decisions/` — read this directory directly; it holds the current records. `coordination/DECISION-LOG.md` is the index but **has not been updated since 25 Aug and lists none of the six 26 Aug decisions.** Decisions also live in approved tasks/specs, dispositioned Controller Briefs, approved proposals and frozen artifacts. |
| What is the current integration direction? | `coordination/decisions/CONTROLLER-MACRO-RESEARCH-INTEGRATION-2026-08-26.md` |
| What are the 36 capabilities, the 100-item bank, the 30 briefs and the persistence contract? | `eval/v1/capability-contract.yaml`, `eval/v1/bank/`, `canon/experiments/v1/brief-bank/`, `resources/v1/EMPIRICAL-ARTIFACT-MANIFEST-SCHEMA.yaml` |
| What is believed but untested? | `coordination/ASSUMPTIONS.md` |
| How is a Canon source admitted? | `canon/audit/AUDIT-GATE-v0.2.md` |
| Which Canon sources are live? | `canon/audit/records/` + `canon/knowledge/current/` (one record per directory) |
| What is the authoritative Eval battery? | `eval/battery/devanagari-exactness/human-validation/HUMAN-VALIDATION-RECORD.md` and `human-validation-v1.json` |
| What media do we hold? | `resources/manifests/corpus-pilot-v0.jsonl` and `source-registry-v0.csv` |
| What does the Governor do, and what may it write? | `governance/GOVERNOR-CONTRACT.md` |
| What did the first repository audit find? | `governance/audits/2026-08-25-initial-repository-hygiene-audit.md` |
| What did the Governor find in the macro-research branches? | `governance/reviews/GOV-003-MACRO-RESEARCH-INTEGRATION-REVIEW.md` |
| Which governance documents are superseded? | `governance/status/` |

**Every row above names the thing that owns the fact.** This document summarises them; it does not
outrank any of them. If a summary here and the file in the right-hand column disagree, the file is
right and this document needs fixing.

## 11. How to start a session

**Every role:** this document → `coordination/PROJECT-CONTRACT.md` → `shared/COMMUNICATION-STANDARD.md`.

Then:
- **Controller:** `coordination/CONTROL-STATE.md`, then the decision records it links.
- **Worker:** your stream `CHARTER.md` → your stream `HANDOFF.md` → your assigned task file → only
  the sources that task names. Do not replay full project history.
- **Governor:** `governance/GOVERNOR-CONTRACT.md` → current `main` → the task/PR under review →
  the most recent file in `governance/reviews/`.

**Before acting on any authorisation, check `coordination/CONTROL-STATE.md`.** Several task files in
this repository were written under plans that have since been superseded, and a task file is not an
authorisation.

**A session may persist for convenience, but no important project fact may depend on it.** If you
learn something that matters, it belongs in GitHub before the session ends.
