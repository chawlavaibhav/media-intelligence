# Eval V1 overnight — Controller Brief

**Task:** E1–E5 of `eval/tasks/EVAL-V1-OVERNIGHT-PROGRAM.md`
**Date:** 26 Aug 2026 · **Branch:** `work/eval-v1-overnight` · **Not merged to `main`.**
**Session:** fresh cloud session, no laptop access, no prior chat context.

> ## ₹0 spent · 0 paid API calls · 0 generations · 0 empirical Registry entries · 0 instruments qualified
>
> Nothing in this tranche measured a model. Nothing qualified a checker. That
> was the instruction, and it held.

---

## 1 · What actually happened, in one paragraph

I built the **measurement architecture** that the later paid waves will run
inside: a definition of all 36 capabilities precise enough that nobody can
quietly redefine one later; a 100-item benchmark bank where **one generated
asset is scored on average 12.7 times** instead of being regenerated per metric;
qualification specifications for all six evaluator families; and a working,
**executed** harness that enforces the rules in code rather than trusting
discipline. One package — the model pricing inventory — hit a genuine
environment blocker and is delivered as complete machinery with the price cells
empty.

**The single most useful number for your decision:** of the 36 capabilities,
**only 6 can be measured and trusted today**, and all 6 are operational or
deterministic — none of them tells you anything about fidelity or creative
quality. **20 are blocked on qualifying an instrument. 10 are blocked on test
material we do not hold.**

---

## 2 · Status of E1–E5

| | Package | Status | Runtime-verified here? |
|---|---|---|---|
| **E1** | Capability & measurement contract | ✅ **Complete** — 36/36 | ✅ yes |
| **E2** | Model/API/access/pricing inventory | ⚠️ **Partially blocked** — architecture and call counts complete, prices unobtainable | ✅ machinery verified |
| **E3** | Six evaluator qualification specs | ✅ **Complete** — plus one pack actually built | ✅ pack verified |
| **E4** | 100-item benchmark bank | ✅ **Complete** | ✅ yes |
| **E5** | Generate-once harness + empty Registry | ✅ **Complete and executed** | ✅ 38/38 checks |

**Cloud runner note:** the bootstrap allowed for having no code runner. This
session **did** have one (Python 3.11.15, Node 22.22.2), so E5 is
`implementation_written_AND_executed_in_cloud` — not merely written. Every
"PASS" below was produced by a command run in this session, and the full output
is committed.

---

## 3 · The 36-capability contract (E1)

Each capability now carries 22 mandatory fields: what it means, what it
**excludes** (so two capabilities cannot quietly overlap), the minimum
observation unit, an atomic probe, which compound scenarios may reuse one asset
to score it, a 3–5 step difficulty ladder written as **observable changes** not
adjectives, its instrument family, resource need, result form, the conditions
that must be held fixed for two measurements to be comparable, and whether it
may ever act as a hard routing constraint.

### The honest state of measurability

| | Count | Meaning in plain terms |
|---|---:|---|
| **Measurable now** | **6** | Could be measured and believed today |
| Blocked — no qualified instrument | **20** | We could run it; we could not trust the answer |
| Blocked — material missing | **10** | We do not hold what the test needs |

The 6 measurable today are `delivery_format_compliance`, `edit_preservation`,
`audio_video_synchronisation`, `reliability_pass_at_k`, `cost_and_cpao` and
`latency_errors_refusals`. **Every one is operational or deterministic.** We can
currently measure how fast, how often it breaks, what it costs, and whether the
file is the right shape — and essentially nothing about whether the output is
any good.

I tightened this definition deliberately mid-task. An earlier pass called 11
capabilities "measurable now" by counting anything with an implementable
instrument. But **a detector or a vision model is a model, not a deterministic
oracle**, and calling its output measurable-now would repeat exactly the error
this project already paid for — attaching false confidence to an unqualified
checker. The stricter count is the true one.

### Two rules the contract makes structural

**The observation unit is load-bearing.** A misspelling that *changes* partway
through a clip does not exist in any single frame. Pick the wrong unit and the
defect is undetectable, not merely under-measured. The vocabulary is Canon's
(`SPEC-04`), adopted unchanged.

**One generation is one trial.** Twelve evaluators scoring one asset are twelve
measurements of *one* trial. Frames sampled from a clip add none. Confidence is
computed on independent base items only.

**Verified:** `validate_capability_contract.py` → 36/36, no missing mandatory
field, ids exactly matching your frozen list. `test_validator_negative_controls.py`
→ **12/12** deliberately broken contracts rejected, including an empty contract,
a dropped capability, an added out-of-scope capability, a non-Canon observation
unit, and a family-G capability promoted to a hard routing gate.

---

## 4 · Model roster and access (E2) — **the one blocked package**

**0 endpoints admitted. This is the package that needs you.**

### What blocked it

E2's own rule is that **official provider documentation only** establishes model
identity, availability and price. This session's network policy blocks it:

| Check | Result |
|---|---|
| Official provider domains probed | **22** |
| Reachable | **1** (`cloud.google.com`) |
| Yielding an extractable pricing table | **0** |
| Web search available | Yes — but returned reseller blogs and cost calculators |

Those secondary sources are exactly the category the rule permits as *leads* and
forbids as *evidence*.

### Why I did not just write the prices from memory

This is the part worth your attention. I could have produced a confident-looking
table of model ids and prices. I did not, and the reason is demonstrable rather
than a principle: a search result indicated that legacy `veo-3.0` endpoints were
**shut down on 30 June 2026** — *after* my training cutoff. In this market,
remembered prices and even remembered *model identities* go stale faster than
that gap. A remembered price inside a document that gates a real budget decision
is invented evidence, however plausible it reads.

Candidate models are therefore recorded as vendor **families**, marked
`evidential_weight: none`. Not exact ids — an exact id from memory would look
like verified identity.

### What is complete regardless

- The five-lane architecture and caps (max 19 endpoints), each lane mapped to
  the capabilities it can evidence.
- The per-endpoint admission schema, including **version-pinning mechanism or
  its absence** — an endpoint that cannot be pinned makes every measurement
  against it provisional, because the model can change underneath a Registry row
  with no signal to us.
- **Access visibility:** `user_laptop_credentials: not_visible_to_cloud_session`,
  `cloud_session_configured_access: no_or_unknown`, zero media-provider
  credentials present. Presence booleans only — no secret value was read,
  printed or committed. AWS and GitHub tokens *are* present in this container
  and were deliberately **not used**: they are harness infrastructure, not an
  approved project media account.

### How to finish it — under an hour

Fill `eval/v1/prices-TEMPLATE.yaml` from official pricing pages, then run
`python3 eval/v1/cost_forecast.py --prices <file>`. Totals appear immediately.
**It is a lookup task, not a design task** — everything around it is built and
self-tested.

---

## 5 · Call counts and cost forecast

**Verified by independent computation against your stated hard maxima.**

| Wave | Outputs | Matches runbook max |
|---|---:|:--:|
| E7 admission screen | **204** | ✅ |
| E8 deep qualification | **520** | ✅ |

Retries are **excluded** and must be predeclared — discovering a retry allowance
mid-run is a budget change, not an adjustment.

### The number that will surprise you

| Wave | Generations | VLM | OCR | ASR | Local |
|---|---:|---:|---:|---:|---:|
| Admission | 204 | 492 | 696 | 24 | 792 |
| Deep qualification | 520 | 1,320 | 1,744 | 48 | 2,016 |

**Evaluator calls exceed generations roughly 8 to 1** (~8,000 total). That is
the generate-once rule *working*, not an overrun — one asset inspected by many
evaluators is the whole point. But it means **evaluator cost cannot be folded
into generation cost**, and the forecast keeps them on separate lines. At the
roughly one rupee per vision check recorded in our own prior findings,
evaluation can exceed a third of the true cost of observing a cheap generation.

The calculator **fails closed**: an unresolved price yields `null`, never `0`,
and it **refuses to total a partially-resolved forecast** rather than quietly
under-reporting a budget. Both behaviours are covered by its self-test, which
passes.

**Human verification is a separate top-level line and is expected to dominate.**
Our original cost model omitted it entirely. Any ratio quoted before we have
measured it is an illustrative scenario, not a finding.

---

## 6 · The six evaluator families (E3)

**Qualified: 0 of 6.** That is not a gap in the work — it is the current true
state of the project, and these specs are what make closing it possible.

| # | Family | Material we hold | Unblocks |
|---|---|---|---:|
| 1 | Text / OCR | ✅ **96-item Devanagari battery, frozen and human-validated** | 1 |
| 2 | Deterministic CV / geometry | ✅ **100-fixture pack — built tonight** | 6 |
| 3 | Structured visual VLM | ❌ nothing | **6** |
| 4 | Temporal / video | ❌ nothing | **5** |
| 5 | Speech / audio / AV | ❌ nothing | 2 |
| 6 | Creative / commercial | ❌ nothing | 4 |

### Built and verified tonight: the family-2 pack

**100 scoreable synthetic fixtures + 2 negative controls**, ground truth
constructed by code — **zero human labels, zero spend**. Deterministic from a
seed, so the same repository state always produces byte-identical fixtures.
102/102 distinct file hashes, 101/101 distinct pixel fingerprints, all decode
correctly through the project's existing `pngraster`, and the corrupt fixture
**correctly fails closed** rather than reporting "0 objects found".

It deliberately includes the recorded shadow trap (grey object-shaped
distractors that must not be counted) and attribute-swap cases where both
colours and both shapes appear in *every* fixture, so an instrument that merely
detects "red and blue and square and circle" scores at chance.

**A defect I found and fixed:** the first build produced only **65 distinct
images across 101 fixtures** because my parameter cycling repeated. A pack of N
that is really M is a *correlated* pack — the same error as treating frames from
one clip as independent tests. The generator now refuses to emit any
pixel-identical pair, and the verifier enforces distinctness as an invariant.

### The cheapest ordering of the work

Qualifying **one** family unblocks every capability in its row at once. Two
families need **no human labelling at all**, because their truth can be
constructed: family 2 (done) and family 4 (inject a known freeze, a known
identity swap, a known flip into a clean clip). **Those two should go first.**

---

## 7 · The benchmark bank (E4)

**100 base items = 40 atomic + 60 compound (10 scenario families × 6 tiers).**

> ### 1,266 valid measurements from 100 generated assets — a **12.7× multiplier**

Scoring the same coverage one-metric-per-generation would need **1,266
generations instead of 100**. At any plausible price that is the difference
between a fundable programme and an unfundable one. It is also why evaluator
calls outnumber generations 8:1 — intended economics, not waste.

The fan-out is **derived from the capability contract**, not hand-written: a
compound item may score a capability only if the contract lists that scenario as
valid reuse **and** the capability applies to that modality. A still image can
never claim a temporal measurement.

**Coverage:** all 36 capabilities exercised. **19 of 20 critical capabilities**
reach the ≥10 opportunity target.

**The one that does not, and what I did about it.**
`two_speaker_turn_assignment_and_lip_sync` reaches **7**, not 10, because only
one scenario family has two visible speakers exchanging turns. I did **not** pad
it by adding two-speaker items to scenarios without on-camera dialogue — that
would manufacture opportunities that cannot exhibit the failure, inflating the
denominator while measuring nothing. The exact denominator and reason are
recorded, as your runbook requires.

**A design question for you:** `multi_shot_branded_ad` is defined as modality
`video`, so it is excluded from dialogue capabilities. If a multi-shot branded ad
should carry on-camera dialogue, its modality should be `native_av` — which
would take that capability to 13 and change nothing else. I left it alone
because it alters the frozen compound-60 design, which is your call.

**Verified:** structure valid, every fan-out entry contract-authorised; **9/9**
negative controls rejected, including a still image claiming a temporal
measurement.

---

## 8 · Harness verification (E5) — **executed, not just written**

**38/38 checks pass.** Full output committed at
`eval/v1/harness/VERIFICATION-LOG.md`. Reproduce with one command.

| Demonstration | Result |
|---|---|
| One video scored by several evaluators, no regeneration | **4 instruments, 12 measurements, 1 generation — 12.0×** |
| Retry creates a new attempt, never replaces | ✅ original asset intact with original hash |
| Frames keep the parent trial id | ✅ 6 assets, **2 trial assets** — 4 frames added 0 trials |
| Duplicate-regeneration guard fires | ✅ refused; re-measuring the same asset stays free |
| Unqualified instrument cannot write a Registry row | ✅ refused |
| Empty Registry schema validates | ✅ 0 rows |

The harness **fails closed** on every violation, because a prior defect in this
project was *a run that raised integrity errors and still exited successfully*.
It also refuses: synthetic measurements even from a *qualified* instrument; an
empty measurement set; an `absent` verdict with no machine-readable reason; a
verdict outside the vocabulary; scoring a capability outside the item's fan-out;
and using an instrument outside its qualified judgement family.

**Absence is five distinct reasons**, not one — so "could not be measured" can
never read as "passed". That distinction matters to routing: unmeasured risk is
not absent risk.

*Two defects surfaced during verification were in my **test assertions**, not
the harness — an expected-substring mismatch, and a case that tripped an earlier
guard before reaching the one under test. Both corrected so the intended guard
is genuinely exercised.*

---

## 9 · Cross-stream requests (Resources)

`eval/v1/instruments/RESOURCE-REQUESTS.yaml` — **proposed, not approved. No
Resources file was edited and no acquisition is authorised.** Most requests
match the shared V1 contract. Five are **additions**:

| | Addition | Severity | Why it matters |
|---|---|---|---|
| **ADD-01** | **Same-category decoys** for person and product reference packs | **CRITICAL** | The shared contract specifies matches only. **Without decoys the identity qualification cannot detect permissiveness** — an instrument answering "yes, that is a shampoo bottle" would score as though it had verified an individual product. |
| ADD-02 | ≥12 clean base clips for temporal perturbation | HIGH | Unblocks 6 capabilities at **zero human-labelling cost**. Need not be generated; any clean rights-cleared footage serves, because we are qualifying the instrument, not scoring a generator. |
| ADD-03 | Declared brand colour reference **values** | MEDIUM | A photograph is not a colour reference. Without values, colour fidelity is descriptive only. |
| ADD-04 | Brand marks on **curved and angled** surfaces | MEDIUM | Flat marks qualify only the easy case; commercial work is the hard case. |
| ADD-05 | ≥15 **known-clean** commercial assets | MEDIUM | Required to measure **false criticism** — an instrument that flags problems in flawless work is as useless as one that misses them, and more insidious because it looks diligent. |

Also restated (already in the shared contract, but the field most easily dropped
in delivery): **turn boundaries** for the two-speaker clips. They are what make a
wrong speaker assignment machine-detectable.

Unchanged and still optional: asking Resources to check **existing** material for
~36–42 more Hindi words. It would tighten a sizing figure from 8.68% to below
5%. It blocks nothing — the deterministic zero-false-pass gate is unaffected.

---

## 10 · Evidence classification — what you can and cannot rely on

### ✅ Verified in this cloud session (commands run, output committed)
- Capability contract: 36/36, scope unchanged; 12/12 negative controls rejected.
- Cost calculator self-test, including refusal to total a partial forecast.
- Call counts 204 / 520 independently computed and matched to your maxima.
- CV fixture pack: 102 fixtures, distinctness, determinism, decode, fail-closed.
- Bank: 100 items, contract-authorised fan-out; 9/9 negative controls rejected.
- Harness: 38/38 checks.
- Both frozen EVAL-005 human-validation response hashes recomputed and matched.

### 📐 Designed but not runtime-verified (no runtime exists to verify against)
- The six family qualification protocols and their gates.
- Registry schema v1 — proposed, not in force.
- The evaluator per-asset fan-out counts, flagged `ESTIMATE_NOT_MEASURED`.
- Every proposed threshold. **0.95 repeat consistency, ≤10% false fail, ≤5%
  refusal, and all colour/sync/legibility tolerances are judgement calls with no
  empirical backing.** They need your approval before a run, and changing one
  after seeing results is an experiment-mutation stop.

### 📋 Previously committed evidence, cited but not re-run
- The 96-item validated battery and its human validation (record verified by
  hash; the validation itself was not repeated).
- The founding checker study — 6 false passes on 14 images, and **explicitly
  preliminary**: 14 images from only 4 independent sources, right answers never
  confirmed by a first-language reader, each image checked once.
- EVAL-004's stop; Reader A remains exploratory only.
- The CVIT/IIIT-ILST shared lineage and ~33% cross-release label disagreement.

### 🚫 Blocked by this environment
- **E2 official pricing and model identity** — the only genuine blocker.
- Byte-level inspection of the raw Resources corpus (git-ignored, laptop-only).
  Nothing in E1–E5 depended on it.

### ⏭️ Deliberately not attempted — later gated work
E6 instrument qualification, E7 admission screen, E8 deep qualification, E9
production benchmark, E10 maintenance. All require approval, budget and material
that does not exist. **EVAL-006 remains paused and was not executed, resumed or
reinterpreted.**

---

## 11 · Files and commits

Branch `work/eval-v1-overnight`, **5 commits, not merged**. 143 files, ~12,000
insertions (102 are fixture PNGs).

| Commit | Package |
|---|---|
| `7ab5cde` | E1 capability and measurement contract |
| `2b32908` | E2 inventory — architecture complete, prices blocked |
| `f432e6d` | E3 six family specs + CV pack built |
| `5bbf496` | E4 100-item bank — 12.7× multiplier |
| `498eab0` | E5 harness + empty Registry, executed |

**Isolation verified:** every change is confined to the new `eval/v1/` and
`eval/registry/` directories. **No prior Eval evidence was modified** —
`eval/battery/`, `eval/harness/`, `eval/calibration/`, `eval/findings/`,
`eval/decisions/` and `eval/tasks/` are untouched. **No Canon, Resources,
coordination, governance or shared file was edited.**

---

## 12 · What I recommend you decide

These are **recommendations, not decisions**.

1. **Fill in the prices** (≈1 hour, needs only ordinary web access). It is the
   only thing standing between you and a real budget number.
2. **Approve the two zero-human-cost qualifications first** — family 2 (pack
   already built) and family 4 (needs only clean clips). Together they unblock
   **11 capabilities** without a single human label or a rupee of API spend.
   This is by far the best value available right now.
3. **Add same-category decoys (ADD-01)** to the Resources contract before those
   packs are collected. Retrofitting them later means recollecting.
4. **Rule on the proposed thresholds** — or explicitly defer them. They cannot
   be inferred from anything we hold, and a run that adopts them silently would
   bake a guess into every result.
5. **Answer the `multi_shot_branded_ad` modality question** — a one-line
   decision that changes a coverage denominator.

**Nothing above authorises spend, and no instrument may be described as
qualified on the basis of this tranche.**
