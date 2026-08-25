# Allocation, leakage, lineage and storage contract

**Task:** R3 of `resources/tasks/RESOURCES-V1-OVERNIGHT-PROGRAM.md`
**Date:** 26 Aug 2026 · **Branch:** `work/resources-v1-overnight` · **Status:** design frozen, validators executed
**Machine-readable:** `resource-allocation-schema.yaml` · **Enforced by:** `validators/check_allocation_leakage.py`

---

## The finding this contract is built on

**On this corpus, deduplicating by file hash certifies a split that is 100% contaminated.**

That is not a hypothetical. I ran it tonight, twice, on the same two sets of files:

| Dummy allocation | Membership | Level required | Result |
|---|---|---|---|
| `DUMMY-03` | develop on 3,925 CVIT crops, qualify on 551 CVIT scene photographs | **byte** | **PASS — no shared key** |
| `DUMMY-02` | **identical membership** | **content** | **FAIL — 375 shared keys, 551/551 (100.0%) of the qualification set contaminated** |

Same files. Same split. One check says clean; the other says every single qualification item is a
photograph the instrument already trained on, because almost every crop was cut out of one of those
photographs. The crops share **no bytes** with their parents — different tooling, different pixels —
so no hash comparison can ever see it.

`DUMMY-02` is retained permanently as a **negative control**. If it ever passes, the content-lineage
check has silently broken.

## Three levels, because three different things destroy independence

| Level | Catches | Measured on this corpus (cloud-verified tonight) |
|---|---|---|
| **byte** | The same file appearing twice | 173 hashes shared between the two CVIT sources — all 173 are scene photographs |
| **content** | Different bytes, same underlying content | **173 content groups span the two CVIT sources and contain 2,633 items — 1,378 of IIIT-ILST's 1,390 (99.1%)** |
| **source lineage** | Different content, shared collection/lab ancestry | IndicSTR12 + IIIT-ILST are one lineage; BSTD is the only independent Devanagari lineage |

Look at the two overlap figures for IIIT-ILST side by side: **12.4% at byte level, 99.1% at content
level.** Both are correct measurements of different things, and quoting only the first would make a
99%-contaminated pool look like a 12% annoyance.

**How the content key works.** A crop's filename encodes its parent photograph. The content key is
built from the **parent's byte hash**, so a crop, its parent, and the *other source's copy of that
same parent* all collapse into one group. That is what makes the 1,205 derived crops visible.

**Verification worth noting:** GOV-001 recorded the "1,205 of 1,214 crops derive from shared parents"
figure as one it **could not verify**, because the raw corpus was unavailable. It is now
independently reproduced — **1,205 of 1,214, exactly** — from the committed manifest alone, with no
media file opened. The ancestry was recoverable from filenames all along.

**A whole-corpus consequence.** The two CVIT sources contain 4,476 items which resolve to just
**376 content groups**. Anyone sizing a Devanagari experiment off "4,476 images" is off by roughly
twelvefold in independent units.

## Roles are allocations, not properties

A role is a role **inside a named experiment at a named version**. The same photograph can be
development material in one experiment and reserve in another. Five roles:

| Role | What it means | Protected? |
|---|---|---|
| `development` | Free to inspect while building | no |
| `calibration` | Sets an instrument's operating point | no |
| `qualification` | Decides whether the instrument may be trusted; must be unseen at calibration | **yes** |
| `reserve` | Held untouched so a later question can be asked cleanly | **yes** |
| `regression` | Retained because a specific failure happened on it | no |

Rules that follow: one role per item per experiment version; **no media is duplicated on disk to
express a second role**; a frozen allocation is superseded, never edited (historical baselines are
not rewritten); and a reserve anyone has inspected is no longer a reserve — freezing it is one-way.

`regression` deserves a note: regression items are **contaminated by construction**. Somebody already
studied them closely, which is why they exist. That is fine for their purpose and disqualifying for
every other.

## Why no role is assigned tonight

The obvious split — develop on CVIT, qualify on BSTD — is written up as `DUMMY-01` and passes cleanly
at source-lineage level. **It is still not assigned.** A role belongs to an experiment, and Eval has
not frozen its experiment split. Assigning now would either be overwritten or, worse, quietly treated
as binding. Every view therefore carries
`protected_role: unassigned_pending_eval_experiment_split`.

What is delivered instead is the machinery that makes assigning it later **safe**.

## Fail-closed behaviour, and why exit 2 is not exit 1

The validator distinguishes three outcomes, deliberately:

- **exit 0** — checked, no collision found
- **exit 1** — checked, leak found (a DATA INTEGRITY stop under `shared/AUTONOMY-POLICY.md`)
- **exit 2** — **could not check**

"I found no leak" and "I could not look" must never produce the same exit code. **Executed tonight**,
six broken inputs all produced exit 2 and no verdict: missing file, empty file, missing
`independence_level`, reference to a view that does not exist, reference to an item id absent from
the manifest, and no arguments at all. An empty role aborts rather than passing vacuously.

Two smaller honesty rules the validator follows:

- **Duplicates are reported, never removed.** Deleting them improves the number and destroys the
  finding. `DUMMY-01` reports 176 redundant copies in its calibration role and 19 in qualification;
  the run still passes, because reporting is the correct handling.
- **Unresolved ancestry is `unproven`, not `clean`.** Four IIIT-ILST crops descend from photograph
  `178`, which was never acquired. They are flagged on every content-level run rather than assumed
  independent.

**What the validator cannot do:** it cannot prove independence. It can only fail on a collision it
knows how to look for. Absence of a detected collision is not proof, and the tool prints exactly that
on every clean run.

## Storage classes

### A — reacquirable external

Public datasets that stay reliably reacquirable. Retain the selected members, per-item hashes, the
complete remote member list, the selection rule, the official URL, the remote size and the retrieval
script — enough to reproduce the selection exactly. Do not retain the full archive; log every
deletion.

**Hash rule, unchanged and non-negotiable:** fingerprint an archive *before* deleting it; if range
access meant it was never downloaded, record **no** full-archive hash. A hash of a file we never held
is fabricated evidence. All 8 acquired sources are class A.

### B — controlled / permissioned

Controlled references and commercial material. Retain durable originals **plus** the permission,
provenance, capture-condition and consent records. These are not reacquirable on demand: **losing
the consent record makes the media unusable even if the media survives.**

**This class is currently empty.** Every pack in it is missing.

### C — irreproducible empirical model output

Our own paid generations, processed derivatives and production failures. **Never treat as
reacquirable.** Providers drift, versions retire, identical inputs stop producing identical outputs.
Delete it and every measurement derived from it becomes unverifiable.

**The project has already lost material this way.** The legacy spike's `.gitignore` said generated
media was *"expensive to make, wrong to store in git… regenerable from the scripts here."* It was not
regenerable. The 64 judgements survived because someone whitelisted `scores.json`; the 64 images did
not. That is the whole argument for class C, and it is written into the schema next to the rule.

## Boundaries

Resources stores evidence and enforces independence. It does not decide what an experiment's
independence requirement should be, does not label failures, and does not assign roles until an
experiment names them. A detected leak is escalated, **not** quietly re-split — re-splitting after
seeing a result is experiment mutation, which is never worker-autonomous.
