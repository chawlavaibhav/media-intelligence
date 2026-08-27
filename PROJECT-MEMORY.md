# Project Memory

**The canonical entry point for this project.** Read this first, every session, before anything else.

**Maintained by:** the Repository Governor (see `governance/GOVERNOR-CONTRACT.md`).
**Last Governor reset:** 25 Aug 2026, task GOV-001, against `main` at `00ea9b067229cd992b77b7d6e0958df35178b01b`.
**Last refresh:** **28 Aug 2026, task GOV-005**, resynced against `main` at
`8990a7afe3d31038bc01dae531e771df12e49870` after the Controller's disposition
(`coordination/decisions/CONTROLLER-GOV-005-REVIEW-AND-CORRECTIONS-2026-08-28.md`).
The review itself is `governance/reviews/GOV-005-POST-EMP-001-COHERENCE-REVIEW.md`; its §§1–9 are a
historical audit of `0e24d6a` and its §10 is the current-state update.
Previous refresh: 26 Aug 2026, GOV-004, at `74d6b0d`
(`governance/reviews/GOV-004-FINAL-PRE-EXECUTION-REVIEW.md`). Task GOV-002 was assigned but
never executed and is superseded — `governance/status/2026-08-26-GOV-002-SUPERSEDED.md`.

> **If you read nothing else, read this.** The project has **spent real money and run its first
> paid experiment.** Five different systems were tested on whether they can tell that the text drawn
> in an image is exactly the text that was asked for. **All five failed the same way** — they
> silently repaired misspelled words instead of reading what was actually there. The project
> therefore still has **zero qualified evaluators, zero measured models and zero Registry rows** —
> but that is now a *tested* zero, not an untested one. Roughly **USD 1.30** of the approved USD 10
> ceiling has been consumed.
>
> **And then the Controller changed what that failure means.** As of 28 Aug 2026, exact text is
> **no longer a gate on the rest of the programme**. Certifying text as perfect and *benchmarking*
> which model handles text better are now separate jobs with separate standards. Unrelated image,
> video and audio work may proceed. **EVAL-028's two-human architecture is cancelled and must not
> run**; **EVAL-029** is the live text-evaluator lane. Full detail in §4 under "EMP-001"; current
> authorisation lives in `coordination/CONTROL-STATE.md`.

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
`[repo]` = established by a committed artifact, and memory was checked against it during a Governor
review — the artifact is the authority, and it is named. `[decision]` = a durable Controller decision exists
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

Stream detail: `canon/HANDOFF.md`. CANON-009 and CANON-010 are merged; neither added a source, so
live Canon is still 19.

**New on 27 Aug: the first record of what real buyers actually ask for.** `[external]` Three
user-supplied research files were committed under `canon/research/marketplace-demand-v1/sources/` —
a read-only Upwork job-market sweep (11 search queries, 114 unique job postings, 4 detail pages), a
read-only Fiverr demand and competition sweep (10 listing pages, 42 gig pages), and the raw capture
notes behind the Fiverr sweep. Provenance and boundaries: `canon/research/marketplace-demand-v1/README.md`.

**This matters because of the gap CANON-009 measured** — the 30 authored briefs test almost none of
what real requests most demonstrably ask for. This is the first material in the repository that
records real demand rather than authored probes.

**Three boundaries that must not be blurred**, all stated by the source README itself:

- **Upwork buyer jobs may be used as customer-intent source briefs. Fiverr seller gigs may not** — a
  seller's package description is not a customer's request.
- Volume and market-size figures in the sweep are **research estimates from one capture**, not
  market-share facts.
- This is **external research**, not repository-derived evidence, and it carries an explicit
  no-redistribution-without-rights-review boundary.

**It is not a Canon source.** It sits in `canon/research/`, not `canon/knowledge/current/`, has not
been through the Audit Gate, and does not change the count of 19. `[repo]`

**CANON-011 is the open lane** that turns this research into a benchmark brief and prompt bank at
zero spend. **No derived output is committed** as of `8990a7a`, and no branch has been pushed.
Governing authority: `coordination/decisions/CONTROLLER-MARKETPLACE-DERIVED-BRIEF-PREP-2026-08-27.md`
and `canon/tasks/CANON-011-MARKETPLACE-DERIVED-BRIEF-BANK.md`.

### Eval — the battery has now been run against five checkers, and all five failed

**Nothing in this stream currently licenses trusting any evaluator's numbers.** No checker is
qualified, no model has been benchmarked, and the Capability Registry holds zero rows —
mechanically verified in GOV-005. `[repo]`

**What changed on 27 Aug 2026, and it is the most important change in the project so far.** The
₹0-spend statement that stood here through GOV-004 is **no longer true**. The user approved a
bounded USD 10 tranche, the machinery ran, and five distinct exact-text checkers were measured
against the frozen Devanagari battery. All five were disqualified. **Roughly USD 1.30 has been
consumed.** `[decision]` Full history below under "EMP-001 — the first paid tranche".

The historical EVAL-003/004/005 material below is unchanged and remains the foundation the paid
runs were measured on.

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

Stream detail: `eval/HANDOFF.md`. **Warning: that handoff is stale.** It still states "₹0 API/model"
and "No checker/model/API call has occurred", which the spend authorisation and eight subsequent
decision records contradict. Routed to Eval as GOV-005 finding F-2; until it is refreshed, use
`coordination/CONTROL-STATE.md` and this document for spend and qualification state. `[repo]`

### Resources — corpus acquired and closed; RES-003 and RES-004 both merged

**34,786 items / 5.70 GB across 8 acquired sources; 4 blocked.** `[repo]`
Recomputed directly from `resources/manifests/corpus-pilot-v0.jsonl` at GOV-001 and again at GOV-005:
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

Stream detail: `resources/HANDOFF.md`. RES-003's rebaseline reconfirmed every headline figure above
from the committed manifest on 26 Aug; GOV-003, GOV-004 and GOV-005 each re-derived them. **Nothing
in Resources has changed since GOV-004** — no acquisition is authorised and none has occurred.

### The 26 August macro reset — why the plan changed, and where the three streams now stand

**What went wrong, in one sentence.** Before spending money on the first paid benchmark, the
Controller noticed that the 30 authored briefs and the 36-capability contract were starting to
*define* the product rather than *test* it — the benchmark was becoming the specification. `[decision]`

**The rule adopted instead:** research what customers actually request, independently research what
today's models can and cannot do, independently research what evidence and persistence the project
needs — and only then integrate the three and freeze the real empirical programme.

Three research programmes ran on that basis. All three returned, and **all three are now merged into
`main`.** Each spent ₹0, made no model or evaluator call, and created no Registry entry. `[repo]`

| Programme | Branch | What it produced |
|---|---|---|
| **CANON-009** | `work/canon-009-request-space` | A map of real media-generation request patterns from 13 public sources, a proposed 14-part Media Request Grammar, and a measured audit of the 30-brief bank against it. |
| **EVAL-007** | `work/eval-007-capability-workflow` | An external audit of the 36 capabilities, an evaluator/qualification landscape, a four-layer benchmark v2 proposal, and a cost forecast that refuses to produce a total. |
| **RES-003** | `work/res-003-evidence-topology` | Dataset rights and independence research, a corpus rebaseline, a leakage/protected-set proposal, and a proposed whole-outcome persistence topology with a working cost-recomputation engine. |

GOV-003 reviewed all three for repository coherence and found them safe to merge; the Controller
merged them into `main` on 26 Aug. `[repo]` **Their evidence is now on `main`** — the branches are
history.

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
`[decision]` That file governs.

**Compressed at GOV-005.** These were *directions* for specification work, and the specification
work is done — every direction below was turned into a frozen contract in the pre-execution freeze
two sections down, which is where the binding detail now lives. Kept here are the distinctions that
still trip people up.

- **The requested operation is an explicit field on the Normalized Request**, and it must stay
  separate from the production route. "Change the background of this photo" is an **edit**; whether
  the Planner does that by inpainting or img2img is a production choice. Collapsing the two destroys
  the ability to tell a misread request from a bad plan.
- **Output sets are first-class** — one deliverable, several variants, or a campaign set — and
  whether acceptance is per output or for the whole set changes cost per accepted outcome directly.
- **Multi-turn requests are recognised but not solved**, and must not block a paid benchmark.
- **The 30 briefs stay byte-identical** as the frozen generation-core bank; a separate
  request-coverage extension covers what they never exercised.
- **A requirement blocked by a failed prerequisite is never a pass and never "not applicable".** If
  the product was never rendered, its logo cannot be inspected — but the customer still asked for
  the logo, so at outcome level it stays **unsatisfied**. Scoring it as "not applicable" makes the
  most complete failure return the highest number.
- **Every empirical result carries the conditions it was produced under**, and there is **no single
  complexity score**. No cartesian product is authorised: 11 conditions at two levels is already
  2,048 combinations before a model is chosen.
- **Fully-loaded Cost per Accepted Outcome is the primary business metric** — failed and refused
  calls, retries, evaluator calls, repairs, required human review time and rejected revisions in the
  same journey all count. API-only cost is a diagnostic reported alongside it. **Shared upstream
  costs count once**: RES-003 showed a naive walk over a reused artifact overstates cost by 13.3% on
  its own worked example.
- **A discovery corpus and a benchmark drawn from the same request pool are not independent
  evidence.** Rephrasing prompts does not erase ancestry; a taxonomy inherits its source's lineage;
  unknown lineage is **indeterminate**, not independent.
- **Four controlled resource packs, no fifth.** Expected changes are metadata and grouping, not new
  pack families.

### EVAL-008 — model selection first, sourcing second · superseded as supply evidence

A fourth lane ran alongside the macro research: `eval/tasks/EVAL-008-CLOUD-MODEL-ACCESS-RESEARCH.md`.
Its rule is that **which models to test is decided independently of where credits happen to be
available**; only then is sourcing checked (Frontier Clouds → fal → direct). Credits may optimise what
execution costs; they must never shape what the project chooses to learn about. The ordering was
honoured provably in git — the roster was committed before any route content existed — and verified
in GOV-003.

All nine deliverables exist under `eval/model-access/2026-08-26/` on branch
`claude/eval-008-cloud-model-access-i3fl86`, unmerged, draft PR #21. `[repo]`

**Read it as a candidate universe, not as supply truth.** EVAL-010 has since checked its rows against
providers' own material and **rejected eight of its claims**, including an unverified ~99%
Hindi/Bengali accuracy figure and a silent fal family/version substitution. **Where the two disagree,
EVAL-010 governs.** Nothing in EVAL-008 is authorised: no model is selected, admitted, qualified or
budgeted, and the "FROZEN for this task" heading on its roster means only "committed before sourcing
began".

### The final pre-execution freeze — four packages, now merged and in force

After the macro reset was integrated, the Controller ran one more ₹0 tranche: turn the adopted
*directions* into contracts precise enough to price. Four programmes returned, GOV-004 reviewed them
for coherence, and **the Controller merged all four into `main` on 26 Aug 2026**. `[decision]`
(`coordination/decisions/CONTROLLER-PRE-EXECUTION-CLOSURE-2026-08-26.md`.) Their contents are on
`main`; the branches are history.

| Package | Merged from | What it froze |
|---|---|---|
| **CANON-010** | `work/canon-010-request-freeze` @ `3cf2979` | The request contract: the seven-value operation vocabulary, the Normalized Request delta, and an 11-item coverage extension |
| **EVAL-011** (corrects EVAL-009) | `work/eval-011-pre-execution-integration` @ `e300999` | Capability Contract v2, the condition contract, dependency scoring, the scientific roster and the staged execution plan |
| **RES-004** | `work/res-004-production-readiness` @ `2dc4796` | Outcome topology v3, the CpAO v3 accounting contract and the four controlled-pack requirements |
| **EVAL-010** | `work/eval-010-route-verification` @ `8a8fc09` | Verified model identities, routes and prices — deliberately **partial** |

> **A trap for a fresh session.** Several of these artifacts still carry
> `status: PROPOSED_FOR_CONTROLLER_FREEZE_NOT_IN_FORCE` in their own header — including
> `eval/pre-execution-freeze/CAPABILITY-CONTRACT-v2.yaml`. **That status field is stale, not
> authoritative.** It was correct before the merge and the generator that emits it has not been
> rerun. `coordination/CONTROL-STATE.md` lists these contracts among the project's frozen
> foundations, and it governs. Routed to Eval as GOV-005 finding F-6. `[repo]`

**`work/eval-009-measurement-freeze` is historical.** EVAL-009 shipped with an internal contradiction
— its own contract declared 13 condition families while parts of the package still said 12, making a
derived figure 4,096 instead of 8,192. The Controller ordered one bounded correction rather than
another research round, and **EVAL-011 is the corrected live proposal.** No family was removed to
recover the old number; the count was the error.

**Everything below is a proposal until the Controller merges and freezes it.** Each artifact says so
in its own status field.

### What the pre-execution packages actually contract

Authoritative record: `coordination/decisions/CONTROLLER-PRE-EXECUTION-INTEGRATION-2026-08-26.md`.
`[decision]` Every number below was re-derived from the committed artifacts during GOV-004. `[repo]`

**The request contract.** Seven customer-intent operations —
`generate · edit · animate · restore · extend · compose · variants` — recorded on the Normalized
Request, upstream of Creative IR. **A supplied asset does not imply `edit`**, and `restore` stays
distinct from `edit` because it is judged against a plausible original nobody has rather than against
a requested change. Production-route values (`inpaint`, `img2img`, `controlnet`, …) are **forbidden**
as operation values and a validator rejects them, which is how requested operation is kept from
collapsing into workflow mode. The original **30 briefs stay byte-identical**; an **11-item
extension** covers the operations they never exercised. Both banks are authored probes — **neither is
demand evidence**, and no file in the package carries a prevalence claim. Multi-turn stays
representation-only.

**The measurement contract.** Capability Contract **v2 = 44 = 43 active + 1 dormant**, the dormant
one being `repairability`, which stays asleep until a repair loop exists. It comes from V1's 36 by
four splits, one rename and four additions; **V1's 36-capability contract and 100-item bank stay
byte-identical historical baselines.** The 43 active capabilities partition exactly across the seven
evaluator families. Conditions are **13 families** — a naive two-level product would be **8,192**
cells, which is why sweeps are sparse and no cartesian product is authorised, and why there is no
single "complexity score". A requirement blocked by a failed prerequisite gets its own state,
`blocked_by_prerequisite_failure`: not directly inspectable, but **still unsatisfied at outcome
acceptance — never a pass, never "not applicable"**. Seeded and unseeded repeat groups measure
different quantities and **may not be pooled**.

**The scientific roster: 12 core question slots + 2 reserve.** These are questions, not provider
commitments. Sourcing may swap an equivalent implementation into a slot but **may not delete a
question for access convenience** — and none was: 0 slots deleted, 0 sibling substitutions.

**The staged execution model**, which is the part that decides what a first bill could look like:

| Stage | What it does | Model generations |
|---|---|---:|
| **Q** | Qualify the instruments before spending on models | **0** |
| **A** | Admission and discrimination screen across the 12 core slots | **90** |
| **B** | Deeper capability and sparse-envelope work, survivors only | **≤ 404** |
| **C** | End-to-end customer outcomes and real CpAO | 32 outcome **attempts** |

`90 + 404 = 494`, the **full Layers-1–3 design ceiling**. Stage C's 32 attempts are a separate layer
and are *not* added to it; its generation count is deliberately left unset because it depends on a
production recipe the Planner would choose, and the Planner does not exist.

**Layers 1–3 may not report customer-outcome CpAO** — there are no accepted customer outcomes there,
so the denominator does not exist. They report trial cost, reliability, latency, errors and refusals.
The premium-versus-fast cost-knee verdict is a **Stage C** output only.

**The evidence contract.** Outcome topology v3 is
`job → outcome → sequence_or_asset_set → production_unit → production_step → attempt → artifact`.
Artifacts may have several ordered parents; deterministic local steps create artifacts **without
inventing a provider attempt**; **one provider/API/transform call = one trial** is unchanged; historical
v2.1 records are never backfilled. **Fully-loaded whole-outcome CpAO is the primary business metric**
and API/tool CpAO is diagnostic. Rejected revisions in the same journey count; a material customer
scope change cuts the journey; shared upstream costs count once. **One-time R&D, benchmark design,
pack acquisition and evaluator qualification are not per-customer production cost.** Four controlled
packs, **no fifth**, with consent required before any person or voice material is captured and
CC-BY-NC still unauthorised for commercial empirical use.

**The supply picture is deliberately partial.** Of 26 candidate rows, **2 are execution-ready** —
meaning identity, route, billing unit *and* current price are all verified — and 19 more have verified
identity and route but **no verified price**. That is an evidence gap caused by blocked provider
pages, **not** a finding that only two models are usable. `Frontier Clouds` remains unidentified, so
cash outlay after credits cannot be computed at all.

### EMP-001 — the first paid tranche, and what it actually found

**This is the section that changed most since GOV-004. Read it before assuming anything about spend
or evaluators.**

#### What EMP-001 is

A deliberately small first experiment, designed so that a bad outcome costs almost nothing. It asks
one question before it asks any other: **can any available system reliably tell whether the text
drawn inside an image is exactly the text that was requested?** Until something can, no image-quality
number the project produces means anything, because there is nothing trustworthy to judge with.

The shape, frozen and unchanged: qualify a text judge on Devanagari first; run Latin only for
candidates that survive; and only if a judge qualifies for every script needed, generate **16 images
maximum** (4 strings × 2 repeats × 2 routes) as a partial admission screen called A-TEXT.

The measurement is deliberately crude and unarguable: **the judge transcribes what it sees without
being told the answer, and code checks exact character equality.** A judge that "passes" a
deliberately misspelled word has done the one thing that costs money in production.

#### The spend approval — this is real, and it is on record

The user explicitly approved **USD 10 total consumed API spend**, with a **USD 6 text-judge
qualification sub-cap**, **zero retries**, and **no account pre-funding above the ceiling**.
`[decision]` `coordination/decisions/CONTROLLER-EMP-001-SPEND-AUTHORISATION-2026-08-27.md`.

**Any document in this repository still saying paid execution is unauthorised or has not happened is
stale.** GOV-005 found and routed the remaining instances.

#### The qualification history — five configurations, five failures *against the strict standard*

**The standard these were judged against matters, and it changed afterwards.** Every result below
was scored under **strict exactness certification**: mismatch false passes must be **zero**. That is
the right bar for certifying customer-facing text and it is the bar all five failed. Since 28 Aug
2026 a second, looser standard also exists for a different job — see "Exact text stops being a
gate" below. **The results here are unchanged and were not rewritten** under the new standard.

Every row is a **Controller decision on record carrying worker-reported measurement**. `[decision]`
`[agent-reported]` None of it was independently reproduced by the Governor, for the reason in the
box below.

| # | Candidate configuration | Devanagari primary result | Disposition |
|---|---|---|---|
| 1 | Anthropic `claude-haiku-4-5-20251001` | 576 calls; 43 false passes; 118 false fails; match false-fail rate 0.4097; consistency 0.9271 | Disqualified (contract-v1 pooled gate) |
| 2 | Google `gemini-3.5-flash-lite`, first attempt | stopped at 17 calls on HTTP 429 | **Not a verdict** — ambiguous post-dispatch failure; preserved, not retried |
| 3 | Anthropic `claude-sonnet-5`, corrected | 576 calls; 29 false passes; 6 false fails; false-fail rate 0.0208; consistency 0.9843 | Triggered the contract-v1 calibration review |
| 4 | Anthropic `claude-sonnet-5` under contract v2 | 288 blind transcribe calls; **20 false passes / 7 unique items**; false-fail rate 0.0278; consistency 0.9792 | **Disqualified** |
| 5 | Google `gemini-3.5-flash-lite` under contract v2, 7s pacing | 288/288 primary; **18 false passes / 7 unique**; false-fail rate 0.1111; consistency 0.9375 | **Disqualified** |
| 6 | Google `gemini-3.5-flash-lite` repeat, no pacing | 576/576, zero errors, zero 429s; **16 false passes / 8 unique**; consistency 0.9167 | **Disqualified** — second complete screen; the pacing rule was withdrawn |
| 7 | Google Cloud Vision `TEXT_DETECTION`, no language hints | 288/288; **18 false passes / 6 unique**; false-fail rate 0.0208; consistency **1.0**; zero infrastructure failures | **Disqualified** — best operational stability tested, still fails the safety gate |
| 8 | Tesseract 5.5.3 `hin+eng`, all six lexical dictionaries off (USD 0) | 288/288; **3 false passes / 1 unique**; false-fail rate **0.6667**; consistency 1.0 | **Disqualified** |
| 9 | Tesseract `hin` script-routed leg (USD 0) | 3 false passes / 1 unique; false-fail rate 0.6042; consistency 1.0 | **Disqualified** |
| 10 | Tesseract `eng` script-routed leg (USD 0) | 12 false passes / 4 unique; false-fail rate 0.5000; consistency 1.0 | **Disqualified** |

**Contract v1 versus contract v2, since the table depends on it.** Under v1 the gate pooled two
question shapes: blind transcription and a target-aware yes/no verdict. EVAL-020 corrected this so
that **only the blind transcription decides qualification** and the target-aware verdict is a
diagnostic. That is why rows 3 and 4 are the same model with different numbers — the instrument was
corrected between them, not the model.

#### The finding that is worth more than the money it cost

**Modern text recognisers repair broken words on purpose, and that is exactly the wrong behaviour
here.** `[decision]`

Both technology families failed the same way. Vision-language models and purpose-built OCR alike use
language and dictionary knowledge to guess what a word *should* be. Shown a deliberately corrupted
Hindi word, they returned the correct word. Sonnet, Gemini and Cloud Vision even failed on
overlapping items, and Cloud Vision repeated every one of its six false-pass items in all three
repeats — this is stable behaviour, not noise.

Turning that knowledge off proved the mechanism and produced the trade-off:

- Tesseract with all six dictionaries disabled cut false passes from ~18 to **3**;
- but its false-fail rate rose to **0.67** — it started rejecting perfectly correct text;
- routing by script removed wrong-script mistakes but **did not reduce false passes**.

So a floor remains after the dictionaries are gone: Devanagari glyph confusion, and Latin
homoglyph confusion (`O`/`0`, `5`/`S`, `Z`/`2`).

**The Controller did not relax the zero-false-pass standard for any of these runs.** That is what
makes the evidence worth having — a bar that moves when candidates fail measures nothing. The bar
was later kept intact *and set aside for a different purpose*, which is not the same as relaxing
it; see below.

**Tesseract configuration search is CLOSED.** No further page-segmentation, engine-mode, language or
preprocessing sweeps are authorised without a new mechanism-level rationale.
`coordination/decisions/CONTROLLER-EVAL-025-DISPOSITION-HUMAN-CONFIRMED-TEXT-GATE-2026-08-27.md`.

**A naive machine ensemble is not an escape either.** At least one residual Tesseract false-pass
item also appears among the false passes of the stronger candidates, so "pass only if two engines
agree" cannot be assumed to reach zero false passes. Any ensemble must qualify empirically; none is
authorised.

#### Spend consumed

| | |
|---|---|
| Cumulative paid qualification spend | **USD 1.3037905** `[decision]` |
| Qualification sub-cap | USD 6.00 |
| Total EMP-001 ceiling | USD 10.00 |
| Image generations run | **0** — fal spend USD 0 |
| Retries authorised, and used | 0 |

> **How solid are these numbers? Read this before quoting them.** `eval/runs/` is git-ignored. **No
> per-trial record, spend ledger or qualification result from any live run is committed to `main`.**
> Every figure above exists only as prose inside a Controller decision record. Nobody reading GitHub
> can recompute a false-pass rate, re-derive the cumulative spend, or re-analyse the false-pass
> items. That is GOV-005 finding **F-1**, routed to Eval and the Controller and **unresolved**. It
> is the one place where the project's own rule — that a fresh session reconstructs state from
> GitHub *by reading the evidence* — is currently not satisfied.

#### Exact text stops being a gate — the 28 August course correction

**This is the most consequential decision since the spend approval, and it is easy to misread.**
`[decision]` `coordination/decisions/CONTROLLER-EXACT-TEXT-NONBLOCKING-BENCHMARK-THRESHOLD-2026-08-28.md`

**The problem it solved.** The programme had reached a state where nothing could be measured about
any model until an exact-Hindi-text checker reached zero false passes — a bar nothing tested could
clear. One imperfect capability was holding the entire benchmark hostage.

**The insight.** Two different jobs had been treated as one:

| Job | Question it answers | Standard | Status |
|---|---|---|---|
| **Strict exactness certification** | "Can I promise the customer this text is exactly right?" | zero mismatch false passes | **Nothing has ever passed.** All five results above stand. |
| **Benchmark-grade text OCR** | "Which generation route handles text better?" | a known, bounded error rate | New contract `benchmark_text_ocr_v1` |

Comparing two models does not need a perfect judge — it needs a judge whose error you can measure
and report alongside the result.

**`benchmark_text_ocr_v1` thresholds:** mismatch false-pass ≤ **0.15**; match false-fail ≤ **0.10**;
repeat consistency ≥ **0.95**; empty/refusal/infrastructure failure ≤ **0.05**; 3 repeats; blind
transcription only; retries 0; **no human review in the contract**.

**`benchmark_qualified` and `strict_exactness_qualified` are different statuses and must stay
visibly different.** Any metric scored by a benchmark-grade evaluator carries that evaluator's
measured error rate and contract id. Benchmark-grade OCR **must never be presented as a guaranteed
exactness certifier**.

**What this does to Cloud Vision, stated carefully because it looks contradictory.** Its Devanagari
numbers did not change: false-pass 0.125, false-fail 0.0208, repeat consistency 1.0, zero empty
transcriptions, zero infrastructure failures. Under the **strict** screen it **fails** — 0.125 is
not zero. Under the **benchmark** contract those same numbers **pass** — 0.125 ≤ 0.15. Both
statements are true, because they answer different questions.

**Four rules that follow, and a fresh session gets these wrong most often:** `[decision]`

1. **EVAL-028 is cancelled and must not run.** `eval/status/EVAL-028-SUPERSEDED-2026-08-28.md`.
2. **No mandatory human-in-the-loop step exists in the production API architecture.** The
   two-independent-blind-reader composite was a proposal, and it was withdrawn.
3. **Exact-text imperfection blocks nothing else.** A Stage-A slot may proceed as soon as the
   instruments *that measurement* needs are ready. Temporal/video evaluator work, deterministic
   instruments, marketplace-derived Stage-C brief preparation and A-TEXT generation all run
   independently.
4. **The strict results are preserved as valid research**, reclassified as
   `strict_exactness_certification`, and must not be rewritten to look like passes.

**If a customer ever needs near-zero text risk**, that is a production-recipe problem — compositing
text deterministically rather than asking a generative model to paint it, or a separate stricter
verifier — not a prerequisite for learning which media models are useful.

#### Where the exact-text line goes next — EVAL-029

**EVAL-029 is the live lane.** `eval/tasks/EVAL-029-BENCHMARK-GRADE-TEXT-OCR.md`. `[decision]`

1. Build the separate `benchmark_text_ocr_v1` contract without mutating any historical strict
   contract or result.
2. **Recompute** — not rerun — the existing Cloud Vision Devanagari evidence against it, mechanically
   from stored observations. If recomputation disagrees with the accepted numbers, stop and return
   to the Controller before any paid call.
3. If Devanagari passes, run the **one missing Latin screen**: Cloud Vision `TEXT_DETECTION`, no
   language hints, 96 items × 3 repeats = **288 calls**, retries 0, conservative reservation
   **USD 0.432**, on the existing persistent ledger. No Devanagari rerun; no Gemini, Anthropic,
   Tesseract or fal calls.
4. If both scripts pass, Cloud Vision is **benchmark-qualified** for model comparison — and still
   **not** strict-exactness qualified.
5. If EVAL-024's sealed artifacts exist, score those exact images with no humans and no
   regeneration. If they do not, prepare the handoff and stop.
6. **Registry text rows stay blocked** pending Controller review of the A-TEXT result.

> **A dependency worth checking before spending.** Step 2 requires the stored per-trial Cloud Vision
> observations, which — per **F-1** — are **not on `main`**. Whether they are reachable in the
> worker's local run root is not verifiable from the repository. If they are not, EVAL-029's first
> step cannot be performed as written. GOV-005 §10.5, routed to Eval and the Controller.

### Numbers in this repository that are NOT approved budgets

Worth stating flatly, because they are the ones most likely to be mistaken for authorisations. `[decision]`

- **494 generations · 5,515 evaluator calls · 188 human review units** — the Layers-1–3 *design
  ceiling* and its forecast, not a tranche.
- **173 person-hours** of pack acquisition — a full provisional plan under one sizing assumption,
  explicitly **not** a prerequisite to the first paid model call.
- **Provisional controlled-pack entity totals** — labelled provisional, with the sizing rule and its
  assumption attached.
- **Every price in the repository** — 0 of the 4 stages is price-complete, and no missing price has
  been guessed.

### Architecture objects — what does not exist yet

**Production IR, the Production Planner, routing, and any Canon-consumption / RAG / training
experiment are unapproved and not implemented.** The Capability Registry exists as a schema and an
empty file. `[repo]` Do not assume otherwise from a schema draft or a plan document; drafts exist,
implementations do not.

## 5. Current gate — paid execution is live, bounded, and mid-experiment

**`coordination/CONTROL-STATE.md` is authoritative for what is currently authorised.** This section
is the map to it, refreshed on 28 Aug 2026 against `main` at `0e24d6a`.

**The GOV-001 audit freeze has been re-scoped repeatedly and no longer reads as written.** `[decision]`
Any document still saying "all new domain work is frozen", or that no paid call is authorised, is
stale. GOV-005 corrected the instances it owns and routed the rest.

### What is authorised and running now

Three lanes are open in parallel. `[decision]`

| Lane | What it does | Spend |
|---|---|---|
| **EVAL-029** | Benchmark-grade text OCR: build `benchmark_text_ocr_v1`, recompute the existing Cloud Vision Devanagari evidence against it, then run the one missing Latin screen if it passes. | ≤ **USD 0.432**, inside the existing EMP-001 ceilings |
| **EVAL-024** | Generate and **seal** the 16 frozen A-TEXT images. **Scoring them is not part of this task.** Currently behind a cleanup gate — see below. | Bounded by the existing USD 10 EMP-001 ceiling; **USD 0 spent so far** |
| **CANON-011** | Turn the Upwork/Fiverr marketplace research into a provenance-preserving benchmark brief and prompt bank. | USD 0 |

> **EVAL-028 is CANCELLED and must not be executed.** `eval/status/EVAL-028-SUPERSEDED-2026-08-28.md`.
> Its two-independent-blind-human composite was withdrawn on 28 Aug 2026, and **no mandatory
> human-in-the-loop step exists in the production API architecture.** If you find a document
> describing EVAL-028 as the next direction, it predates the course correction. EVAL-029 replaced it.

**EVAL-024 reverses the original ordering deliberately.** EMP-001 originally required a qualified
judge before spending on generation, so a failed qualification would save the generation money. The
Controller overrode that so the images exist while the judge problem is worked on. The images may
not be interpreted, scored or promoted until a qualified evaluator and an accepted handoff exist.

**EVAL-024 returned with zero live spend, and is not cleared to dispatch.** `[decision]`
`coordination/decisions/CONTROLLER-EVAL-024-READINESS-CLEANUP-AND-LIVE-2026-08-28.md`

`FAL_KEY` was unavailable. The runner correctly classified that as a **pre-dispatch** failure —
meaning no provider call was made, so no reservation was consumed and **no money was spent**. That is
the accounting rule working as designed, not a failure.

The design is accepted in principle. Before any live dispatch, four cleanup items apply:

1. **sync the branch to current `main`** — it predates the exact-text course correction and EVAL-029;
2. **restore `preflight-result.json` and `perceptibility-mechanical.json` byte-for-byte from `main`** —
   the branch rewrote both incidentally and neither is an EVAL-024 output;
3. **stop writing non-PNG bytes to `.png` paths** — determine media type from the returned bytes,
   preserve and hash the raw bytes, never transcode to make an extension convenient;
4. **restore the pinned Tesseract traineddata** so the full suite is green again — this is
   environment restoration, not a reopening of the Tesseract research line.

If `FAL_KEY` is available after cleanup, the 16 generations may run from that exact pushed and tested
head, on the existing ledger. If it is still unavailable, the worker stops pre-dispatch and returns.
**Committing the 16 sealed image bytes to the repository is accepted as a bounded EMP-001 exception**
and must not be generalised into storing future generated media in Git.

**Lane state on the remote, checked against `8990a7a`:** `[repo]`

- EVAL-024 — `origin/work/eval-024-parallel-atext-generation-only` @ `e4e4d39`, behind current
  `main`. Orchestrator and tests only. **No generation result and no image is committed.**
- CANON-011 — local branch only, nothing pushed, no derived output committed.
- EVAL-029 — task file merged; no worker branch yet.

**Which authority governs each lane** — settled by the Controller on 28 Aug 2026, closing GOV-005
finding F-4. `[decision]`
`coordination/decisions/CONTROLLER-GOV-005-REVIEW-AND-CORRECTIONS-2026-08-28.md`

| Lane | Governing | Historical, preserved, **not** governing |
|---|---|---|
| **EVAL-024** | `coordination/decisions/CONTROLLER-EVAL-024-READINESS-CLEANUP-AND-LIVE-2026-08-28.md` → `.../CONTROLLER-PARALLEL-ATEXT-GENERATION-ONLY-2026-08-27.md` → `eval/tasks/EVAL-024-PARALLEL-ATEXT-GENERATION-ONLY.md` | `.../CONTROLLER-EMP-001-PARALLEL-ATEXT-GENERATION-ONLY-2026-08-27.md`; `eval/tasks/EVAL-024-ATEXT-GENERATION-ONLY.md` |
| **CANON-011** | `coordination/decisions/CONTROLLER-MARKETPLACE-DERIVED-BRIEF-PREP-2026-08-27.md` → `canon/tasks/CANON-011-MARKETPLACE-DERIVED-BRIEF-BANK.md` → `canon/research/marketplace-demand-v1/README.md` | `.../CONTROLLER-MARKETPLACE-DERIVED-BRIEF-PROMPT-PREP-2026-08-27.md`; `canon/tasks/CANON-011-MARKETPLACE-DERIVED-BRIEF-PROMPT-BANK.md` |

The duplicates are kept as history and are **not instructions**. The later pair won because it binds
the committed marketplace-source provenance and keeps a brief separate from a prompt-ready envelope.


### The current empirical floor — what is still zero, and what no longer is

**Still zero, and mechanically verified where it can be:** `[repo]`

- **0 qualified models or workflows.**
- **0 qualified subjective or perceptual evaluator families.**
- **0 exact-text evaluators qualified under the strict zero-false-pass standard** — five
  configurations tested, five disqualified. **0 benchmark-qualified as well, so far**: Cloud Vision
  meets the new benchmark-grade thresholds on Devanagari, but its Latin screen has not been run, so
  no candidate holds `benchmark_qualified` status yet.
- **0 rows in the Capability Registry.** Verified: the file holds zero data rows and the validator
  passes.
- **0 A-TEXT image generations.**
- **0 accepted evidence that Canon improves model outcomes.**
- **0 customer-outcome CpAO observations.** Those are Stage C only, and Stage C is not authorised.
- **No Production IR and no Planner exists.**

**No longer zero:** `[decision]`

- Paid execution **has been authorised** and **has happened**.
- **USD 1.3037905** of consumed API spend, against a USD 10 ceiling.
- Roughly **2,500 live evaluator calls** across the screens above, plus about 1,150 zero-cost local
  Tesseract executions.
- **Five instrument configurations scientifically disqualified**, with a mechanism finding attached.

**Read the difference correctly.** "Zero qualified evaluators" meant *untested* at GOV-004. It now
means *tested and failed against the strict standard*, which is a far stronger and more useful
statement — and it is why the Controller separated certification from benchmarking rather than
queueing another candidate.

### What is still blocked, and is not made authorised by any older file

`[decision]` `coordination/CONTROL-STATE.md`, "Still blocked / not authorised".

- **Mandatory human-in-the-loop exact-text review as part of the production API architecture.**
  Withdrawn on 28 Aug 2026 and not to be reintroduced without a new decision.
- **Treating benchmark-grade OCR as a perfect exactness certifier.** It is a confidence signal with
  a measured error rate, and must never be described as a guarantee.
- **Registry population from text metrics** until the benchmark-grade handoff is reviewed.
- **Further Tesseract or OCR configuration sweeps** without a new mechanism-level rationale.
  General-purpose multimodal LLMs remain frozen as the strict exact-text judge family.
- **Broad Stage-B and Stage-C execution** without their own instrument readiness.
- **Broad controlled-pack acquisition.**
- **Production IR / Planner implementation** before sufficient empirical capability evidence exists.
- **`EVAL-006` remains PAUSED — DO NOT EXECUTE**, spend authority explicitly withdrawn. It must not
  be resumed or repurposed.
- **Historical E7 paid admission and E8 deep qualification remain blocked.**
- **The Canon value gate remains unrun.**

**No worker may infer authorisation from an old task file.** If a task file and a current Controller
decision disagree, the decision wins and the task file is stale.

### What still has to happen before the programme can scale

1. **Benchmark-qualify one text evaluator — EVAL-029.** No longer a gate on everything else, but
   still the thing that decides whether A-TEXT can be scored at all. It needs the Cloud Vision Latin
   screen and, before that, the stored Devanagari observations F-1 says are missing from `main`.
2. **Seal the completed EMP-001 evidence into GitHub — GOV-005 F-1.** The Controller has accepted
   this must be fixed. It gets more expensive with every run, and EVAL-029's first step already
   depends on it.
3. **Get EVAL-024 through its cleanup gate**, so 16 sealed images exist for a benchmark-qualified
   evaluator to score.
4. **Resolve the prices.** 0 of 4 stages is price-complete, and `Frontier Clouds` must be identified
   before cash outlay after credits can be computed at all.
5. **Controller decides HED-1** — which human review time counts as required in fully-loaded CpAO.
   Less urgent than it was, now that no mandatory human step sits in the production architecture.
6. **The Controller explicitly approves any tranche beyond EMP-001.** The USD 10 approval covers
   EMP-001 only.

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
- **A count declared in one place and derived in another will drift.** EVAL-009 declared 13 condition
  families in its schema while prose elsewhere still said 12, and the derived cell figure silently
  became 4,096 instead of 8,192. **The cheap wrong fix — delete a family to recover the old number —
  was explicitly refused.** Derive counts from the structure, and gate on the derivation.
- **A complete design is not a sensible first bill.** The instinct to authorise the whole 494-generation
  design at once had to be replaced with stages, and scope was reduced by deferring whole questions
  rather than by halving repeats, because halving repeats destroys the reliability evidence that
  justified running at all.

**Added after the first paid tranche, 27–28 Aug 2026:**

- **Accuracy is not literalness, and for a checker they are opposite virtues.** Every recogniser
  tested — two vision-language models and two OCR engines — used language knowledge to repair
  corrupted words. That makes them *better* at reading ordinary text and *useless* as a judge of
  whether the exact requested text was drawn. A checker must be optimised for literal glyph
  fidelity under adversarial misspelling, which is not what any general recogniser is sold on.
- **Turning off the language priors moves the failure, it does not remove it.** Disabling all six
  Tesseract dictionaries cut false passes from ~18 to 3, and pushed the false-fail rate to 0.67. A
  residual floor remains: Devanagari glyph confusion, Latin homoglyph confusion. Cheap literalness
  buys expensive rejection of correct work.
- **Cycling through more candidates in the same family is not evidence-gathering.** Once two
  independent models failed by the same mechanism, the Controller froze the family rather than
  trying a third. The next move was an architecture change, not another candidate.
- **A repeated failure across three repeats is behaviour; a single one is noise.** Cloud Vision
  false-passed all six of its items in 3/3 repeats. That is what made a 288-call screen decisive
  rather than suggestive.
- **Do not relax the gate when the gate is what is producing the finding.** Every candidate failed
  the zero-false-pass rule. Loosening it would have manufactured a qualified evaluator and destroyed
  the one result the tranche actually bought.
- **A "correction" between two runs of the same model makes their numbers incomparable.** Sonnet was
  measured twice with different results because the *instrument* changed between them (contract v1
  pooled two question shapes; v2 scores only the blind one). Always say which contract a number was
  produced under.
- **Money spent buys a mechanism, or it buys nothing.** USD 1.30 produced no qualified evaluator and
  is still the best-value spend in the project, because it replaced "we have not tested a checker"
  with "we know why checkers fail here."
- **Check what a standard is *for* before letting it block everything.** A zero-false-pass bar is
  right for promising a customer their text is exact, and wrong as a precondition for finding out
  which model draws text better. Holding one imperfect capability's certification standard over the
  whole programme froze work that had nothing to do with it. The fix was to name the two jobs
  separately and give each its own threshold — **not** to lower the bar. Both standards still exist,
  and a result must always say which one it was measured against.

## 7. Known limitations and unresolved questions

- **The Canon has no accepted Devanagari-structure source.** `[repo]`
- **No checker is qualified.** Five exact-text configurations have now been measured and all five
  were disqualified; the project has still taken **no empirical capability measurement of any
  generation model**. `[repo]` `[decision]`
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
- **Provider prices remain largely unestablished in the repository.** EVAL-007 probed 22 official
  provider domains and resolved **zero** rows; its cost forecast returns `null` for all nine price
  cells and refuses to produce a total. `[repo]` **The exception is the EMP-001 execution set** —
  the fal image routes, Anthropic, Gemini and Cloud Vision prices used in the tranche were verified
  by the Controller on 27 Aug 2026 and are recorded in
  `coordination/decisions/CONTROLLER-EMP-001-PRE-SPEND-VERIFICATION-2026-08-27.md`. That is a
  verification of four routes, not of the supply table. `[decision]`
- **No evaluator has been qualified, so no capability number can be trusted yet.**
  `instruments_qualified: 0`. This is **no longer a gate on the whole programme** — since 28 Aug
  2026 a capability may proceed as soon as the instruments *that measurement* needs are ready. For
  text specifically, **EVAL-029** is the current attempt, at benchmark-grade rather than strict
  thresholds. `[repo]` `[decision]`
- **No provider price is complete for any stage** — 0 of 4 — and `Frontier Clouds` is still an
  unidentified service, so the cash cost of any tranche after credits is genuinely unknown rather
  than merely unstated. `[unresolved]`
- **Two scientific slots have no confirmed model.** `IMG-04` and `AUD-03` were kept unresolved rather
  than filled with a sibling version, and both are marked `do_not_substitute`. `[repo]`
- **The Devanagari battery cannot be rebuilt from a fresh clone.** Its built items are git-ignored and
  the pinned font is an uncommitted proprietary asset; the committed record fingerprints it by
  SHA-256 so a rebuild can be checked. This is a rebuild risk on one of the two instruments that
  could be qualified today. `[repo]`
- **The real-world frequency of the requirements our bank tests most heavily is unknown.** No corpus
  reports how often users ask for exact text in an image, for a product rather than a person, for a
  particular duration, for speech at all, or in Hindi/Hinglish. Seven such questions are listed
  rather than estimated, because an estimate becomes a number someone later plans against.
  `[unresolved]`
- **One documentation discrepancy in the Resources corpus is open:** the manifest records 364 BSTD
  "other language" items where committed prose says 351. Resolving it needs raw annotation files no
  cloud session can reach. Deliberately not corrected in either direction. `[repo]`

**New or changed at GOV-005, 28 Aug 2026:**

- **The live EMP-001 evidence is not in the repository.** `eval/runs/` is git-ignored, and no
  per-trial record, spend ledger or qualification result from any paid run is committed. Every
  qualification figure and the cumulative spend exist only as prose inside Controller decision
  records, so none of them can be recomputed, re-checked or re-analysed from GitHub. **The Controller
  accepted this as High and ruled that completed evidence must be sealed immutably into GitHub after
  a bounded screen finishes** — the live mutable ledger stays local, and no keys, secrets or
  rights-restricted provider artifacts are ever committed. A bounded Eval correction opens once
  active Eval work is safely isolated. GOV-005 **F-1**, still **unresolved**. `[unresolved]`
- **EVAL-029's first step depends on those missing observations.** It must recompute the Cloud
  Vision Devanagari result mechanically from stored per-trial records, which are not on `main`.
  Whether they exist in a worker's local run root cannot be verified from the repository. GOV-005
  §10.5. `[unresolved]`
- ~~EVAL-024 and CANON-011 duplicate authorities~~ — **RESOLVED** on 28 Aug 2026 by
  `coordination/decisions/CONTROLLER-GOV-005-REVIEW-AND-CORRECTIONS-2026-08-28.md`. The governing
  chains are in §5; the duplicates are preserved as history and are not instructions. `[decision]`
- **`eval/HANDOFF.md` contradicts the spend record**, stating ₹0 API spend and that no model or API
  call has occurred. Stream-owned, routed as GOV-005 finding **F-2**; do not treat it as current for
  spend or qualification state. `[repo]`
- **Several merged v2 contracts still declare themselves `NOT IN FORCE`** in their own status
  fields, because the generators that emit that string have not been rerun since the merge. GOV-005
  finding **F-6**. `coordination/CONTROL-STATE.md` governs. `[repo]`
- **`coordination/DECISION-LOG.md` is a curated historical and navigation index, not an exhaustive
  record of decisions after 26 Aug 2026** — settled by Controller decision, not a defect to fix.
  Current authorisation comes from `coordination/CONTROL-STATE.md`; detailed decisions are
  discovered by listing `coordination/decisions/` directly. No manual transcription is required, and
  a mechanical index may replace it later. GOV-005 **F-5**, closed as re-scoped. `[decision]`
- **No evaluator can currently certify exact text, and none is expected to.** Strict zero-false-pass
  certification remains unmet by everything tested, and the programme no longer waits on it. If a
  customer ever needs near-zero text risk, that is a production-recipe problem — deterministic text
  compositing, or a separate stricter verifier — not a benchmark prerequisite. `[decision]`
- **HED-1 — which human review time counts as required cost in fully-loaded CpAO — is still
  undecided.** Less urgent since no mandatory human step sits in the production architecture, but
  still open. `[unresolved]`

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

**The 26 Aug Upwork/Fiverr marketplace research is external too**, but unlike the artifacts above it
**is committed** — under `canon/research/marketplace-demand-v1/`, with a provenance README stating
its origin, its evidence hierarchy and its interpretation boundary. It is the first material in the
repository describing real buyer demand rather than authored probes. It is **not** a Canon source,
has not been through the Audit Gate, and its volume figures are one capture's research estimates,
never market-share facts. `[external]`

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
| 26 Aug 2026 | EVAL-008 returns a 26-row proposed model roster with sourcing; nothing authorised | `eval/model-access/2026-08-26/` (unmerged, draft PR #21) |
| 26 Aug 2026 | GOV-003 coherence review of the three research branches — PASS with non-blocking notes | `governance/reviews/GOV-003-MACRO-RESEARCH-INTEGRATION-REVIEW.md` |
| 26 Aug 2026 | CANON-009, EVAL-007, RES-003 and the GOV-003 review merged to `main` | commits `4815bcf`, `b71624e`, `fed0db6`, `cf105b1` |
| 26 Aug 2026 | Final pre-execution freeze tranche returns: CANON-010, EVAL-009, RES-004, EVAL-010 | `coordination/decisions/CONTROLLER-FINAL-PRE-EXECUTION-FREEZE-2026-08-26.md` |
| 26 Aug 2026 | Controller integrates the tranche and orders one bounded Eval correction; EVAL-011 delivers it | `coordination/decisions/CONTROLLER-PRE-EXECUTION-INTEGRATION-2026-08-26.md` |
| 26 Aug 2026 | GOV-004 final pre-execution coherence review — PASS with non-blocking notes; four packages unmerged at review | `governance/reviews/GOV-004-FINAL-PRE-EXECUTION-REVIEW.md` |
| 26 Aug 2026 | Pre-execution freeze closed; CANON-010, RES-004, EVAL-010 and corrected EVAL-011 merged into `main`; the v2 contracts become frozen foundations | `coordination/decisions/CONTROLLER-PRE-EXECUTION-CLOSURE-2026-08-26.md` |
| 26–27 Aug 2026 | EMP-001 execution machinery built and corrected across EVAL-012 → EVAL-016: persistent spend ledger, mechanical caps, ambiguous-dispatch accounting, fingerprint-bound handoff | `coordination/decisions/CONTROLLER-EVAL-01{2,3,4,5,6}-REVIEW-*.md` |
| 27 Aug 2026 | Latin human perceptibility review completed — 96/96 usable, 48/48 mismatch visible, 0 rejected | `coordination/decisions/CONTROLLER-EMP-001-LATIN-HUMAN-REVIEW-2026-08-27.md` |
| **27 Aug 2026** | **The user approves EMP-001: USD 10 total, USD 6 qualification sub-cap, 0 retries. The project's first paid execution authority.** | `coordination/decisions/CONTROLLER-EMP-001-SPEND-AUTHORISATION-2026-08-27.md` |
| 27 Aug 2026 | First live run: Haiku 4.5 disqualified on a complete Devanagari screen; Gemini stops at 17 calls on a 429 | `coordination/decisions/CONTROLLER-EMP-001-GEMINI-CONTINUATION-2026-08-27.md` |
| 27 Aug 2026 | Qualification contract corrected to v2 — blind transcription decides, target-aware verdict becomes diagnostic | `coordination/decisions/CONTROLLER-EVAL-020-PRIMARY-SHAPE-QUALIFICATION-2026-08-27.md` |
| 27 Aug 2026 | Sonnet 5 disqualified under contract v2; general-purpose multimodal LLMs frozen as the exact-text judge family after Gemini fails the same way | `coordination/decisions/CONTROLLER-EVAL-021-SONNET-DISPOSITION-GEMINI-READINESS-2026-08-27.md`, `.../CONTROLLER-EVAL-022-OCR-FAMILY-PIVOT-2026-08-27.md` |
| 27 Aug 2026 | EVAL-022 integrated: Gemini disqualified again on a clean unpaced screen; Cloud Vision TEXT_DETECTION disqualified despite perfect repeat consistency | PR #45, merge `afe866c`; `coordination/decisions/CONTROLLER-EVAL-022-LIVE-RESULTS-AND-EVAL-023-2026-08-27.md` |
| 27 Aug 2026 | User-supplied Upwork/Fiverr marketplace demand research committed; CANON-011 opened to derive real-demand briefs at USD 0 | `canon/research/marketplace-demand-v1/README.md` |
| 27 Aug 2026 | EVAL-023 integrated: Tesseract with dictionaries disabled cuts false passes to 3 but rejects 67% of valid text — the literalness/accuracy trade-off is demonstrated, not hypothesised | PR #46, merge `0ecbf5f`; `coordination/decisions/CONTROLLER-EVAL-023-DISPOSITION-AND-SCRIPT-ROUTED-OCR-2026-08-27.md` |
| 27 Aug 2026 | A-TEXT generation is decoupled from evaluator qualification: EVAL-024 may generate and seal the 16 images but may not score them | `coordination/decisions/CONTROLLER-PARALLEL-ATEXT-GENERATION-ONLY-2026-08-27.md` |
| 27 Aug 2026 | EVAL-025 integrated; script routing removes wrong-script errors but not false passes. **Tesseract line closed.** Next direction *as decided that day*: a fail-closed human-confirmed composite, prepared by EVAL-028 — **superseded the following day, see below** | PR #47, merge `711aa8c`; `coordination/decisions/CONTROLLER-EVAL-025-DISPOSITION-HUMAN-CONFIRMED-TEXT-GATE-2026-08-27.md` |
| 28 Aug 2026 | GOV-005 post-EMP-001 coherence review and project-memory refresh — PASS with non-blocking notes; the missing live-evidence problem (F-1) routed | `governance/reviews/GOV-005-POST-EMP-001-COHERENCE-REVIEW.md` |
| **28 Aug 2026** | **Course correction: exact text becomes a non-blocking measured capability.** Strict zero-false-pass certification is preserved as research but stops gating the programme; a separate `benchmark_text_ocr_v1` contract is created; **EVAL-028 and its two-human architecture are cancelled**; EVAL-029 opens | `coordination/decisions/CONTROLLER-EXACT-TEXT-NONBLOCKING-BENCHMARK-THRESHOLD-2026-08-28.md`, `eval/status/EVAL-028-SUPERSEDED-2026-08-28.md`, `eval/tasks/EVAL-029-BENCHMARK-GRADE-TEXT-OCR.md` |
| 28 Aug 2026 | EVAL-024 returns with **zero live spend** — `FAL_KEY` unavailable, correctly treated as pre-dispatch. Design accepted in principle behind a cleanup/sync gate | `coordination/decisions/CONTROLLER-EVAL-024-READINESS-CLEANUP-AND-LIVE-2026-08-28.md` |
| 28 Aug 2026 | Controller reviews GOV-005: findings accepted, F-1 accepted as High and must be fixed, F-4 resolved with named authority chains, F-5 re-scoped, F-9/F-10 closed; Governor branch must resync to current `main` | `coordination/decisions/CONTROLLER-GOV-005-REVIEW-AND-CORRECTIONS-2026-08-28.md` |

## 10. Authority map — which file proves what

| Question | Authoritative file |
|---|---|
| What is the product and what are the frozen separations? | `coordination/PROJECT-CONTRACT.md` |
| How must every worker communicate? | `shared/COMMUNICATION-STANDARD.md` |
| What is live in each stream right now? | `coordination/CONTROL-STATE.md`, then this document |
| Per-stream status and next gate | `coordination/WORKSTREAM-STATUS.md` — refreshed by GOV-005; `CONTROL-STATE.md` still governs where the two differ |
| How do I start a session, approve a task, escalate? | `coordination/RUNBOOK.md` |
| When may a worker run unattended? | `shared/AUTONOMY-POLICY.md` |
| What has the Controller actually decided? | **List `coordination/decisions/` directly — those records are the authority**, together with stream-owned decision records that Controller state references. `coordination/DECISION-LOG.md` is a **curated historical and navigation index, not an exhaustive post-26-Aug source**, by Controller decision. Current authorisation comes from `coordination/CONTROL-STATE.md`. |
| What is currently authorised, blocked and running? | `coordination/CONTROL-STATE.md` — **this is the single most important file for a new session after this one** |
| **What is the current exact-text posture?** | `coordination/decisions/CONTROLLER-EXACT-TEXT-NONBLOCKING-BENCHMARK-THRESHOLD-2026-08-28.md` — **this supersedes the human-confirmed-gate direction** |
| Is EVAL-028 running? | **No — cancelled.** `eval/status/EVAL-028-SUPERSEDED-2026-08-28.md` |
| What is the active text-evaluator lane? | `eval/tasks/EVAL-029-BENCHMARK-GRADE-TEXT-OCR.md` |
| What is EVAL-024's current state? | `coordination/decisions/CONTROLLER-EVAL-024-READINESS-CLEANUP-AND-LIVE-2026-08-28.md` — returned at USD 0, cleanup gate before live |
| How did the exact-text line reach that point? | The EVAL-022 / EVAL-023 / EVAL-025 dispositions under `coordination/decisions/` — **historical research, still valid, no longer the current direction** |
| What paid spend was approved, and by whom? | `coordination/decisions/CONTROLLER-EMP-001-SPEND-AUTHORISATION-2026-08-27.md` |
| What did the first paid tranche measure? | The Controller decision records under `coordination/decisions/` — **not** a committed evidence artifact. See §7, GOV-005 finding F-1. |
| What was the pre-execution integration direction? | `coordination/decisions/CONTROLLER-PRE-EXECUTION-INTEGRATION-2026-08-26.md`, closed by `.../CONTROLLER-PRE-EXECUTION-CLOSURE-2026-08-26.md` |
| What are the v2 contracts — request, capability, condition, topology, CpAO? | `canon/experiments/pre-execution-freeze/`, `eval/pre-execution-freeze/`, `eval/pre-execution-integration/`, `resources/pre-execution-freeze/` — **all merged into `main` and in force**. Several still say `NOT IN FORCE` in their own status fields; that wording is stale and `CONTROL-STATE.md` governs. |
| What did EMP-001 actually cost? | **USD 1.3037905** consumed, against a USD 10 ceiling — recorded in the Controller decisions, not in a committed ledger. |
| What would a *full* tranche cost? | **Still not answerable.** 0 of 4 stages is price-complete and `Frontier Clouds` is unidentified. |
| What are the 36 capabilities, the 100-item bank, the 30 briefs and the persistence contract? | `eval/v1/capability-contract.yaml`, `eval/v1/bank/`, `canon/experiments/v1/brief-bank/`, `resources/v1/EMPIRICAL-ARTIFACT-MANIFEST-SCHEMA.yaml` |
| What is believed but untested? | `coordination/ASSUMPTIONS.md` |
| How is a Canon source admitted? | `canon/audit/AUDIT-GATE-v0.2.md` |
| Which Canon sources are live? | `canon/audit/records/` + `canon/knowledge/current/` (one record per directory) |
| What is the authoritative Eval battery? | `eval/battery/devanagari-exactness/human-validation/HUMAN-VALIDATION-RECORD.md` and `human-validation-v1.json` |
| What is the Latin exact-text pack and its human review? | `eval/empirical-tranche-1/text_qualification/latin-pack-v1.jsonl` (+ `.sha256`) and `perceptibility-mechanical.json` |
| Where does real customer demand evidence live? | `canon/research/marketplace-demand-v1/` — external research with a stated interpretation boundary, **not** a Canon source |
| What media do we hold? | `resources/manifests/corpus-pilot-v0.jsonl` and `source-registry-v0.csv` |
| What does the Governor do, and what may it write? | `governance/GOVERNOR-CONTRACT.md` |
| What did the first repository audit find? | `governance/audits/2026-08-25-initial-repository-hygiene-audit.md` |
| What did the Governor find in the macro-research branches? | `governance/reviews/GOV-003-MACRO-RESEARCH-INTEGRATION-REVIEW.md` |
| What did the Governor find in the pre-execution packages? | `governance/reviews/GOV-004-FINAL-PRE-EXECUTION-REVIEW.md` |
| What did the Governor find after the first paid tranche? | `governance/reviews/GOV-005-POST-EMP-001-COHERENCE-REVIEW.md` — §§1–9 audit `0e24d6a`; **§10 is the current-state update and governs** |
| How did the Controller dispose of the GOV-005 findings? | `coordination/decisions/CONTROLLER-GOV-005-REVIEW-AND-CORRECTIONS-2026-08-28.md` |
| Which governance documents are superseded? | `governance/status/` |

**Every row above names the thing that owns the fact.** This document summarises them; it does not
outrank any of them. If a summary here and the file in the right-hand column disagree, the file is
right and this document needs fixing.

## 11. How to start a session

**Every role:** this document → `coordination/PROJECT-CONTRACT.md` → `shared/COMMUNICATION-STANDARD.md`.

Then:
- **Controller:** `coordination/CONTROL-STATE.md`, then the decision records it links. **List
  `coordination/decisions/` directly** to discover decisions — `DECISION-LOG.md` is a curated
  historical and navigation index by design, not an exhaustive post-26-Aug source.
- **Worker:** your stream `CHARTER.md` → your stream `HANDOFF.md` → your assigned task file → only
  the sources that task names. Do not replay full project history. **Eval workers: your handoff is
  stale on spend and qualification state** (GOV-005 F-2) — take those from `CONTROL-STATE.md`.
- **Governor:** `governance/GOVERNOR-CONTRACT.md` → current `main` → the task/PR under review →
  the most recent file in `governance/reviews/`.

**Four traps specific to right now**, each worth thirty seconds to avoid:

1. **Do not conclude that paid execution is unauthorised** because a task file, handoff or plan says
   so. Several still do. The spend authorisation is real and recorded; `CONTROL-STATE.md` governs.
2. **Do not start EVAL-028 or design anything around a mandatory human reviewer.** EVAL-028 is
   cancelled and no human-in-the-loop step belongs in the production API architecture. Several
   documents written on 27 Aug still describe that direction; they predate the 28 Aug course
   correction.
3. **Do not read a strict zero-false-pass failure as "unusable".** Cloud Vision fails strict
   certification and meets the benchmark-grade thresholds on Devanagari. Always say which standard a
   text result was measured against.
4. **Do not conclude that a v2 contract is only a proposal** because its own status field says
   `NOT IN FORCE`. Those fields were not regenerated after the merge.

**Before acting on any authorisation, check `coordination/CONTROL-STATE.md`.** Several task files in
this repository were written under plans that have since been superseded, and a task file is not an
authorisation.

**A session may persist for convenience, but no important project fact may depend on it.** If you
learn something that matters, it belongs in GitHub before the session ends.
