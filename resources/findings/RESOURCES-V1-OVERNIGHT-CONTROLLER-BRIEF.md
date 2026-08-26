# Resources V1 overnight — Controller Brief

**Task:** `resources/tasks/RESOURCES-V1-OVERNIGHT-PROGRAM.md`, packages R1–R5 and the R8 schema/legacy tranche
**Date:** 26 Aug 2026 · **Branch:** `work/resources-v1-overnight` · **Not merged to `main`**
**Session:** cloud-browser, zero prior context, **no laptop access**
**Status:** all six packages complete · **0 new source-family acquisition · ₹0 / $0 spend**

> The runbook §12 named this file `resources/reports/RESOURCES-V1-OVERNIGHT-CONTROLLER-BRIEF.md`; the
> session instruction named `resources/findings/`. I followed the session instruction and left a
> pointer at the runbook path rather than maintaining two copies.

---

## 1. Read this first — what "done" means in each row

Per the cloud-session bootstrap §10, every claim below is one of five things:

| Label | Meaning |
|---|---|
| **VERIFIED TONIGHT** | I executed it in this session against committed data and it passed. |
| **PRIOR EVIDENCE** | A previously committed observation I cite with provenance and did **not** re-run. |
| **BLOCKED — NO RAW MEDIA** | Needs the git-ignored corpus, which is not in this session. |
| **BLOCKED — HUMAN DECISION** | Needs consent, permission or a gate only a person may cross. |
| **NOT ATTEMPTED** | Belongs to a later gated task. |

**The single most important caveat.** The 34,786-item / 5.70 GB corpus is **not in GitHub**. I opened
**zero media files**. Where the reports say "34,786 / 34,786 decode cleanly", that is **PRIOR
EVIDENCE** from `RES-001-integrity-report.md`. What I verified tonight is that all 34,786 manifest
records *carry* `validation_status: ok` — the **recorded** status, not a re-decode.

**One command re-verifies everything mechanical:** `bash resources/v1/validators/run_all.sh` —
executed tonight, **exit 0, ALL CHECKS PASSED**.

---

## 2. Status by package

| ID | Package | Status | Evidence |
|---|---|---|---|
| **R1** | Resource requirements matrix | **complete** | 48 rows; 36/36 capabilities, 6/6 evaluator families |
| **R2** | Corpus rebaseline + legacy reconciliation | **complete** | 46 pass / 0 fail / 1 warn; 10/10 legacy pools resolved |
| **R3** | Allocation, leakage, lineage, storage contract | **complete, validators executed** | 3 levels; negative control fails as designed |
| **R4** | Missing-pack supply routes | **complete (research only)** | 4 packs, 11 routes; 0 acquisition |
| **R5** | Existing-resource Eval views | **complete** | 9 views, 39,262 references, no media copied |
| **R8** | Empirical archive schema + legacy | **schema complete, proven at scale** | 1,000 artifacts, fan-out 6.00 |

---

## 3. The headline the Controller needs before approving any budget

**Of Eval's 36 capabilities, exactly ONE is served by material we already hold.**

| State | Capabilities |
|---|---:|
| `available` | **1** (Devanagari exact text) |
| `constructed_by_eval` — Eval builds it, Resources supplies nothing | 10 |
| `no_external_resource` — measured from the model's own telemetry | 5 |
| `partial` | 3 |
| **`missing`** | **17** |

**15 of 36 capabilities require no capability-specific external stimulus pack; some still inherit
evaluator-calibration dependencies.** That stops a third of the capability map from generating
acquisition work, which is a real result — but it is not a claim that those rows are independent of
Resources. Ten have their stimulus built by Eval yet may still need an instrument calibrated on
material Resources supplies (`REQ-CAP-04` `action_adherence` is the clearest case: no pack of its own,
no deterministic checker, and therefore blocked behind two evaluator families that are themselves
blocked). The other five need no media at all but are storage class **C** — measurable only if the
archive preserves every attempt with its cost reference and outcome.

*(Corrected under R-C1 of `RESOURCES-V1-CORRECTION-PASS.md`. The original wording, "need nothing from
Resources, ever", overstated the result. The underlying 36-row classification is unchanged.)*

**Three whole capability groups are at zero coverage:** speech/audio (5 of 5 missing), commercial and
creative fitness (4 of 4), identity and references (4 of 4).

**Three of six evaluator families cannot be qualified at all** — structured visual VLM, speech/AV, and
creative/commercial — each blocked on a pack that does not exist. Given the project's founding result
(a capability number without a qualified checker is not a measurement), **any capability depending on
those three families cannot produce a trustworthy number regardless of how much generation is paid
for.**

### Four acquisitions unblock almost everything

| Pack | Missing/blocked/partial rows it unblocks | Target |
|---|---:|---|
| `PACK-PRODUCT-REF` | **11** | ≥48 images = 12 products × ≥4 views |
| `PACK-PERSON-REF` | **8** | ≥32 images = 8 identities × ≥4 views |
| `PACK-AV-CLEAN` | **7** | 36 clips = 24 single + 12 two-speaker, with transcripts |
| `PACK-COMMERCIAL` | **7** | 80 assets; 60 active + 20 reserve |

**Four decisions, not seventeen.** That is the most actionable output of the night.

---

## 4. New findings from tonight

### 4.1 Deduplicating by file hash certifies a 100%-contaminated split — VERIFIED TONIGHT

Two dummy allocations, **identical membership**, different independence level:

| Allocation | Level | Result |
|---|---|---|
| `DUMMY-03` | **byte** | **PASS — no shared key** |
| `DUMMY-02` | **content** | **FAIL — 375 shared keys, 551/551 (100.0%) of the qualification set contaminated** |

Develop on the 3,925 CVIT crops, hold out the 551 CVIT scene photographs: a hash check calls it
clean, because almost every crop was cut *out of* a held-out photograph and shares no bytes with it.
`DUMMY-02` is retained permanently as a negative control.

### 4.2 A figure GOV-001 could not verify is now verified — VERIFIED TONIGHT

GOV-001 recorded "1,205 of IIIT-ILST's 1,214 crops derive from photographs shared with IndicSTR12" as
**unverifiable without the raw corpus**. It is now reproduced **exactly — 1,205 of 1,214 — from the
committed manifest alone, with no media file opened.** Crop filenames encode their parent photograph,
so the ancestry was recoverable from metadata all along.

**The consequence is larger than the fix.** Measured at content level, IIIT-ILST is **99.1%
non-independent** of IndicSTR12 (1,378 of its 1,390 items sit in 173 shared content groups). Measured
at byte level, the same overlap reads **12.4%**. Both numbers are correct; quoting only the second
makes a 99%-contaminated pool look like a 12% annoyance.

**And the whole CVIT pair — 4,476 items — resolves to just 376 content groups.** Anyone sizing a
Devanagari experiment off "4,476 images" is out by roughly twelvefold in independent units.

### 4.3 The legacy 64-image scored set is half-recoverable — VERIFIED TONIGHT

Recovered from `media-factory` git history: **all 64 human pass/fail judgements with notes**
(`scores.json`, `sha256 8d928dac…`) and a **129-line cost ledger totalling $35.28**. They reconcile
exactly with `FINDINGS-11`: 64 items, 10 failures, nano 7/32, seedream 3/32.

They survived because the spike's `.gitignore` whitelisted them against an `out/*` exclusion.
**The 64 images themselves were never committed** and are `metadata_only`. Practical consequence:
**the project cannot re-annotate those failures for all visible defects** — which the Eval master plan
R6 asks for — until someone with the original machine makes the bytes available.

That gitignore comment read *"expensive to make, wrong to store in git… regenerable from the scripts
here."* They were not regenerable. That is now written into the storage schema as the reason class C
exists.

### 4.4 The most plausible legacy person pack is not one — VERIFIED TONIGHT

`spike/guddu/` holds 19 committed images and looked like a ready-made identity set. **I opened them.**
They are AI-generated **illustrated story frames**, no identifiable person, no identity to reference.
`PACK-PERSON-REF` remains completely empty. Recorded because "19 images of a character" reads like
supply in a spreadsheet and is not.

**Genuine partial supply found instead:** three **first-party** brand marks (`aight_logo.png` and two
others) — the project's own demo brand, so zero trademark exposure. That moves
`logo_wordmark_fidelity` from `missing` to `partial`: **3 of ≥12 marks**, limited by resolution
(two are under 240 px wide), not by rights.

### 4.5 One committed figure does not reconcile — recorded, not fixed

The source registry and `resources/HANDOFF.md` say **351** BSTD images labelled as other languages
carry Devanagari text. The manifest holds **364** (19,773 hindi + 5,109 marathi + 364 other = 25,246,
which sums correctly). **Delta 13.**

Settling it needs the raw annotation files — **BLOCKED — NO RAW MEDIA**. Recorded as an open
discrepancy in both directions rather than silently corrected. Also new: **4 IIIT-ILST crops descend
from photograph `178`, which was never acquired**; their ancestry is flagged `unproven`, not
`independent`.

### 4.6 The AV gap is worse than "no audio" — VERIFIED TONIGHT (research)

Public **audio** corpora for Hindi/English/Hinglish exist. Our requirement is **audio-visual**: four
of five speech capabilities need to see a speaking face. Public AV material with faces *and* verified
transcripts *and* turn boundaries *and* a permissive licence *and* Hinglish essentially does not
exist — and anything with faces brings back the same consent and biometric exposure as the person
pack, plus voice, which is separately protected. Two candidates checked tonight report **CC BY-NC**,
which forbids commercial use.

### 4.7 Two GOV-001 "missing evidence" items are not lost — routed, not acted on

GOV-001 rows R1 and R2 flagged evidence absent from `main`. Both are **cloud-accessible on their
unmerged branches**: `CANON-001/002` findings and the `molly-bang` knowledge directory on
`origin/work/canon-003-a`; `READER-A-FREEZE.md` and `READER-ATTESTATION.md` on `origin/work/eval-004`.
Not lost, only unmerged. **Canon and Eval files — I did not touch them.**

---

## 5. Corpus fit summary — the 34,786 items

**VERIFIED TONIGHT:** every headline figure recomputed from the committed manifest matches exactly —
34,786 items, 34,586 distinct hashes, 200 duplicates (173 cross-source / 27 within), 5,702,337,356
bytes, 8 sources. All 8 per-source counts and byte totals match the registry. Both CVIT partitions are
**disjoint and exhaustive**.

**The item count flatters the corpus.** 32,306 images / 2,480 videos, of which **85.4% (29,722) is
photographed Devanagari scene text**. Total video runtime across all four video sources is about
**236 minutes**. It is one narrow capability repeated 30,000 times plus four thin video pools.

| Need | Served? |
|---|---|
| Devanagari **reading** | **Yes** — the one covered capability |
| Text/OCR evaluator family | **Yes** — the only sufficient instrument family |
| Temporal perturbation base clips | Partly — clips exist, cleanliness unscreened |
| Motion evaluator development | Partly — development only, not current-model qualification |
| Product / person / logo references | **No** (3 first-party marks recovered) |
| Speech / audio / AV | **No — zero audio** |
| Commercial creative | **No** — both public candidates blocked |
| Devanagari in *generated* output | **No — and no acquisition fixes it.** Only paid generation produces it. |

---

## 6. Legacy evidence reconciliation — 10 of 10 resolved

| Outcome | Pools |
|---|---:|
| `recovered` | **5** |
| `metadata_only` | **2** |
| `unavailable` | **1** |
| `unavailable_in_cloud_session` | **2** |

**Zero vague states remain.** Searched: all 6 branches and every reachable commit of
`chawlavaibhav/media-factory`, this repository's tree, and the GOV-001 branches. **No laptop was
searched** — none is reachable. 39 recovered artifacts are hashed in
`legacy-evidence/recovered-artifact-hashes.csv`. **No legacy media was copied into this repository.**

Two artifacts are `unavailable_in_cloud_session` for the *same* reason — `Fraunces.ttf` and the
EVAL-005 `build/` items — and it is one shape of defect: **a build that depends on an uncommitted
font cannot be reconstructed from GitHub alone.** The project knew this about EVAL-005; the legacy
spike has the identical hole.

---

## 7. Role, leakage, lineage and storage — verification

**Three independence levels**, because three different things destroy independence: byte identity,
content lineage (crops/re-encodes of shared parents), and source lineage (same lab or collection).

**Roles are allocations inside a named experiment**, not properties of files. Five roles;
`qualification` and `reserve` are protected. No media is duplicated on disk to express a second role.

**No role was assigned tonight, deliberately.** The obvious split (develop on CVIT, qualify on BSTD)
is written up as `DUMMY-01` and passes cleanly — but a role belongs to an experiment, and Eval has not
frozen its split. Every view carries `protected_role: unassigned_pending_eval_experiment_split`.

**Fail-closed, and negative-controlled.** The validators distinguish **exit 2 (could not check)** from
**exit 1 (found a problem)** — "I found no leak" and "I could not look" must never share an exit code.
Executed tonight: **6 broken inputs to the leakage validator** all exit 2 with no verdict;
**4 broken inputs to the matrix builder** all exit 2 and write nothing; **7 broken inputs to the
archive validator** behave correctly. I also found and fixed a vacuous check in my own suite — the
views-determinism step used `git diff` on untracked files, which passes without comparing anything;
it now compares content hashes, and tampering with a view correctly fails it.

**GOV-001 R3 is untouched.** `build_reports.py` still produces a degraded artifact and exits 0 when
the corpus is absent. Fixing it needs a Controller-assigned task, so I did not — but every new tool in
`resources/v1/` is built to the opposite standard. **I did not run `build_reports.py`**, precisely
because doing so in a corpus-less session is what destroys the committed integrity evidence.

**Storage classes:** A (reacquirable external) holds all 8 sources. **B (controlled/permissioned) is
empty — every pack in it is missing.** C (irreproducible empirical) is where all future paid output
must go.

---

## 8. Empirical archive — proven at the required scale

**VERIFIED TONIGHT** against a fully synthetic 1,000-artifact archive (fictional vendor and model
names, fixed timestamps; **no provider called, no money spent**):

| | |
|---|---:|
| Artifacts | **1,000** |
| Measurements | **5,796** |
| Refusals/errors retained | 34 |
| **Duplicate media copies** | **0** |
| **Mean measurements per scored artifact** | **6.00** |

**One generation, six measurements, stored once.** The ≥1,000 capacity requirement is demonstrated.

Four rules exist because omitting them loses evidence: a refusal is evidence (null output hash,
populated status — otherwise refusals vanish and reliability is overstated); never fabricate a hash or
a cost; frames of one clip are one trial; retention is not conditional on the result.

**Cost per Accepted Outcome is recomputable only if cost, acceptance, the retry chain and the output
bytes all survive together.** That is why the acceptance record is in a Resources schema — though
`decided_by` is never Resources.

**No byte budget was forecast, deliberately.** It needs per-endpoint duration and resolution from
Eval's E2 inventory, which does not exist. Guessing would encode a guess as a plan.

---

## 9. Supply routes — and the pattern in them

| Pack | Recommended | Reserve | Blocked / rejected |
|---|---|---|---|
| Product ≥48 | **Controlled first-party capture** | Google Scanned Objects (no brands, so no logo/colour use) | **ABO — licence contradiction found tonight** |
| Person ≥32 | **Consented internal capture** | Synthetic identities (stated external-validity cost) | Public face datasets — **reject** |
| AV 36 | **Controlled recording with consent** | Creator permission | Public AV corpora — none recommended |
| Commercial 80 | **First-party / permissioned** | — | **Pitt Ads — email gate, worth a decision**; AVA — reject |

**In all four packs the recommendation is controlled or permissioned first-party material,** because
all four need something public datasets structurally do not provide: **the same subject, under
conditions we control, with rights we can state.** A public dataset gives you pictures; these
capabilities need references.

**All four are blocked on the same thing: a human decision.** None was attempted.

**One live rights trap, found tonight.** Amazon Berkeley Objects is structurally near-ideal (8,222
listings with 24- or 72-view turntable sequences), but the AWS Open Data registry reports **CC BY-NC
4.0** while the dataset's own documentation is reported as **CC BY 4.0**. NC forbids commercial use.
**This is the same shape as the PVP trap** — where a search asserted MIT and that was the repository's
*code* licence. I did not resolve it and did not guess. Marked **blocked, not rejected**: if it
resolves to CC BY 4.0 it becomes the strongest public product route available.

**A limitation of this session:** the network egress proxy **blocks direct fetches of official
distribution pages** (confirmed — `people.cs.pitt.edu` returned `EGRESS_BLOCKED`). Search worked;
official-document retrieval did not. **Official rights verification cannot be completed from this
cloud session** and must happen where those pages are reachable. Every external rights claim is
labelled `checked_tonight` or `NOT VERIFIED tonight`, and no `NOT VERIFIED` claim may drive an
acquisition decision.

---

## 10. Cross-stream dependencies

**To Eval:**
1. Three of six evaluator families are unqualifiable until a pack exists. Budget spent on generation
   before that produces outputs no qualified instrument can score.
2. `REQ-CAP-04` `action_adherence` has no deterministic checker; its instrument depends on two blocked
   families. Flagged, not altered — the capability map is Eval's.
3. Roles await Eval's frozen experiment split. Views are ready and unassigned.
4. Of the 10 compound scenario families in E4's bank, **6 need a reference or AV pack that does not
   exist.** They can be designed now; they cannot be run.
5. `REQ-CAP-22` `text_logo_stability_in_clip` is the sharpest gap: the named commercial failure mode,
   with no material and no acquisition that fixes it.

**To Canon:** `REQ-CAN-03` (Experiment B) and `REQ-INS-06` point at **one** 60-asset bank. Two
acquisitions would double cost and make the results non-comparable.

**Unchanged and load-bearing:** rights are **internal research and evaluation only**. If any result is
published or shown to a customer, **the rights question must be reopened first.**

---

## 11. Files and commits

All under `resources/v1/` unless noted:

- **R1** — `RESOURCE-REQUIREMENTS.md`, `RESOURCE-REQUIREMENTS-MATRIX.csv`, `resource-requirements.yaml`
- **R2** — `EXISTING-CORPUS-FIT-GAP.md`, `legacy-evidence/LEGACY-EVIDENCE-RECONCILIATION.md`,
  `legacy-evidence/legacy-evidence-register.csv`, `legacy-evidence/recovered-artifact-hashes.csv`
- **R3** — `RESOURCE-ALLOCATION-SPEC.md`, `resource-allocation-schema.yaml`,
  `fixtures/allocations/DUMMY-01…03`
- **R4** — `MISSING-PACK-SUPPLY-ROUTES.md`
- **R5** — `views/` (9 `.jsonl` + `VIEWS.md`)
- **R8** — `EMPIRICAL-ARCHIVE.md`, `EMPIRICAL-ARTIFACT-MANIFEST-SCHEMA.yaml`,
  `fixtures/empirical-archive-dummy/`
- **Tooling** — `validators/` (6 files) + `run_all.sh`
- **This brief** — `resources/findings/RESOURCES-V1-OVERNIGHT-CONTROLLER-BRIEF.md`, with a pointer
  stub at the runbook's `resources/reports/` path
- **`resources/HANDOFF.md`** — pointed at tonight's work, and the stale "EVAL-003 correction awaiting
  PR review" line corrected to "merged as PR #5" (**GOV-001 R10**, a Resources-owned documentation
  defect and the only routed item I was able to close tonight)

**Nothing outside `resources/` was modified.** No other stream's files were touched. **Not merged to
`main`.**

---

## 11a. Delivery — pushed after a temporary permission block

**Resolved.** The branch is on the remote at `ff33bdf`.

For the record, because it affected how this brief was written: for most of the session both write
paths were refused — `git push` returned **exit 128 / 403** and the GitHub API returned **403
`Resource not accessible by integration`** — while reads worked normally. The Claude GitHub App
installation did not carry write permission on this repository. The operator granted it and the push
then succeeded on the first attempt, unchanged.

No workaround was attempted while it was blocked. The commit was preserved outside the container as a
git bundle and a patch, and the bundle was verified end-to-end: restored into a fresh clone, the full
validator suite passed there with exit 0. Those artifacts are now redundant.

---

## 12. Compliance statement

- **0** new source families acquired. **0** downloads. **0** logins, accounts, forms, terms
  acceptances or purchases. **₹0 / $0** spent.
- **0** media files opened from the raw corpus. **0** files copied from `media-factory`.
- **0** creative or human labels authored by Resources. **0** Canon truth decisions. **0** Eval metric
  or threshold decisions.
- **0** protected roles assigned. **0** holdouts constructed.
- **0** faces or voices collected. **0** emails sent.
- **0** files changed outside `resources/`. **Not merged to `main`.**
- **1** committed figure found not to reconcile, recorded rather than corrected.
- **1** vacuous check found in my own tooling, fixed and negative-controlled.

## 13. What I recommend the Controller decides first

1. **Approve or reject controlled first-party capture** for the product pack. It is the cheapest of
   the four, unblocks the most rows (11), and needs no external rights research at all.
2. **Decide the person pack's route** — consented capture or synthetic identities. It gates 8 rows and
   an entire evaluator family, and it is the one with real consent and biometric exposure.
3. **Yes or no on emailing the Pitt Ads group.** It is the only public candidate for the commercial
   bank and the only blocked source with a real argument for reopening.
4. **Have someone read ABO's actual licence file** where official pages are reachable. A single
   confirmation either opens or closes the strongest public product route.
5. **Decide whether GOV-001 R3** (`build_reports.py` exits 0 on a degraded report) **becomes a
   Resources task.** It is a real defect and I am not authorised to fix it.

**Do not authorise paid generation before at least one of decisions 1–3 lands.** Three of six
evaluator families cannot be qualified without those packs, and a capability number produced by an
unqualified instrument is not a measurement.
