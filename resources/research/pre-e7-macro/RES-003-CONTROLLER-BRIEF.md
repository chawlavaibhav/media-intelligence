# RES-003 — Cloud Evidence, Independence & Outcome-Persistence — Controller Brief

**Task:** `resources/tasks/RES-003-CLOUD-EVIDENCE-PROGRAM.md` (R3-A … R3-F, executed as one program)
**Date:** 26 Aug 2026 · **Branch:** `work/res-003-evidence-topology` · **Not merged**
**Session:** cloud-only — no laptop, no raw corpus, no provider credentials, no prior chat context
**Spend:** **₹0 / $0.** No acquisition, no API call, no login, no terms acceptance, no email sent.

**Verify everything mechanical:** `bash resources/research/pre-e7-macro/validators/run_all_res003.sh`
→ **exit 0, ALL RES-003 CHECKS PASSED.**

---

## 1. Evidence labels used throughout

| Label | Meaning |
|---|---|
| **OBSERVED** | Computed in this session from committed repository data. |
| **PREVIOUSLY-COMMITTED** | A prior recorded result, cited, **not** re-run. |
| **SOURCE-SUPPORTED** | From external documentation via search. **Official pages were egress-blocked**, so nothing external is officially verified. |
| **INFERRED** | Reasoned from the above; labelled wherever it appears. |
| **PROPOSED** | A design recommendation. **Not an approved decision.** |
| **UNKNOWN** | Not established. |

**The binding constraint on this whole program:** `huggingface.co`, `arxiv.org`,
`poloclub.github.io` and `vidprom.github.io` all returned `EGRESS_BLOCKED` on direct fetch. Search
worked. **Therefore every external rights fact is SOURCE-SUPPORTED, never officially verified**, and
the register's validator fails if any field claims otherwise. No row may drive an acquisition
decision until a human reads the actual licence file on the actual distribution page.

---

## 2. Headline: what evidence we can actually get, independently

**The asymmetry is the finding.**

> **Request evidence is cheap, abundant and legally clean. Controlled evidence is none of those, and
> no amount of searching changes it.**

**SOURCE-SUPPORTED.** Millions of real user prompts are publicly available:

| Source | Prompts | Licence | Commercial use | Verdict |
|---|---|---|---|---|
| **LMArena open data** | full text | **CC-BY-4.0** | **permitted** | **best-positioned source** |
| **DiffusionDB** | full text | **CC0 1.0** | permitted | usable; stale images, hobbyist skew |
| **VidProM** | full text | CC BY-NC 4.0 | **non-commercial only** | discovery only, NC unresolved |
| **TIP-I2V** | text + user images | CC BY-NC 4.0 | **non-commercial only** | text only; **images not cleared** |

**Canon does not have to invent a request taxonomy from synthetic briefs** — which is exactly the
failure the macro reset exists to correct.

**But the controlled material the capability work needs is not obtainable from any public source
reviewed.** The product-pack front-runner just closed, the commercial-creative candidate is behind a
human permission gate, and no public AV pack has faces + verified transcripts + turn boundaries +
permissive terms.

---

## 3. Rights and leakage risks, in priority order

### 3.1 The circularity that would invalidate a generalisation claim — OBSERVED

**Arena-T2I-Hard's 310 benchmark prompts are sampled from the same public arena pool that LMArena's
open data exposes.** SOURCE-SUPPORTED, from its own methodology: prompts drawn from a public T2I arena
leaderboard, Jan–Mar 2026, with its own disjoint 10k/1k split from that pool.

**If Canon learns its request grammar from arena prompts and Eval benchmarks on Arena-T2I-Hard, the
benchmark is a descendant of the discovery set and "generalisation" means nothing.** Registered as one
lineage (`lin_lmarena`).

**The cost, stated plainly: adopting LMArena for discovery spends Arena-T2I-Hard as a holdout.** That
is a real loss and the Controller should take it knowingly.

**A second, quieter instance — OBSERVED:** `src_imagerewarddb`, **already in our corpus (2,584
items)**, draws its images from DiffusionDB. Acquiring DiffusionDB would **not** add an independent
lineage; it would enlarge one we already hold. No hash check would show this.

### 3.2 Non-commercial terms on two request corpora — SOURCE-SUPPORTED

VidProM and TIP-I2V are CC BY-NC 4.0. **Our product is commercial.** Learning a taxonomy from NC data
and shipping a commercial system informed by it are different acts, and **where the line sits is a
human legal judgement.** Flagged, not resolved.

### 3.3 TIP-I2V's user-uploaded images — UNKNOWN provenance

Every record includes a **user-supplied image prompt**. Provenance not stated: possibly third-party
copyright, possibly identifiable people. The publisher records an NSFW flag for images, indicating
they expected problematic uploads. **Text prompts usable for discovery; the images are not cleared and
must never be treated as person-reference material.**

### 3.4 The prompt-text basis for DiffusionDB — SOURCE-SUPPORTED, with a caveat

Images are CC0 and that is clean. The **prompts** are user-written text, and the basis for treating
them as free is the **Discord server's terms of service** (users "forfeit all intellectual property
rights claims… including forfeiture of any/all copyright claim(s)"). That is a third-party
platform-terms argument, not a per-author grant. Recorded as the publisher's position, not restated as
settled.

### 3.5 A code licence is not a dataset licence — the trap, again

T2I-CompBench is reported as **MIT** — which is the **repository's code licence**. The register carries
an explicit caution not to record it as an "MIT-licensed dataset". **The project has already been
caught by this exact substitution once, with PVP.** The exposure here is low (mostly prompt text); the
discipline is the point.

---

## 4. Does the existing corpus still make sense? Mostly yes — with two new structural gaps

**OBSERVED, fresh recompute:** 46 pass / 0 fail / 1 warn. Every headline figure reconciles — 34,786
items, 34,586 distinct hashes, 200 duplicates, 5,702,337,356 bytes, 8 sources. **No media file was
opened.** "34,786/34,786 decode cleanly" remains **PREVIOUSLY-COMMITTED**.

**Three OBSERVED measurements reframe the corpus for the widened scope:**

1. **Every video we hold is short.** Total runtime 236.1 minutes; **longest single clip 20.00
   seconds; nothing above 30 s at all.** 90% is ≤10 s. VideoFeedback's 987 clips are *all exactly
   3.00 s*.
2. **Half the corpus is tiny.** **17,748 of 34,786 items (51.0%) are under 100 pixels wide** — the
   single-word Devanagari crops.
3. **The metadata cannot answer the new questions.** No shot boundaries, no speaker labels, no
   audio-stream flag, no campaign grouping. **UNKNOWN**, and not resolvable in cloud.

**Unchanged (PREVIOUSLY-COMMITTED):** 1 of 36 capabilities available, 17 missing; 1 of 6 evaluator
families ready, 3 blocked; zero audio; zero generated Devanagari.

**Two new gaps the widened scope creates, both structural:**

- **Duration.** A pool of 3-second clips cannot serve a 20-second composed branded outcome. The
  *shape* is wrong, not just the quantity.
- **Composition.** Nothing in the corpus is organised as "same campaign, several deliverables", and
  no field could express it.

---

## 5. Does the four-pack plan survive? Yes — six deltas, five of them free

**PROPOSED. No fifth pack family.** The widened scope creates **metadata and grouping requirements on
material the four packs were already going to acquire**, not a new kind of material.

| # | Delta | Volume change | Named consumer need |
|---|---|---|---|
| 1 | Record which product reference fed which production step | **none** | `REQ-CAP-21` at sequence level |
| 2 | ≥2 distinct framings per person identity | **+16 images** | cross-shot `REQ-CAP-11` / `REQ-CAP-20` |
| 3 | ≥6 single-speaker clips ≥20 s continuous | **none** | lip-sync over deliverable-length audio |
| 4 | Hinglish clips include brand names / loanwords | **none** | commercial `spoken_language_correctness` |
| 5 | 40 video ads acquired as ~10 campaign groups | **none** | campaign/variant consistency |
| 6 | Video ads span 6 s / 15 s / 20–30 s | **none** | longer composed outcomes |

**One route closed. SOURCE-SUPPORTED:** **ABO resolves to CC BY-NC 4.0.** The V1 pass recorded a
contradiction (AWS registry said NC, dataset docs reportedly said BY) and correctly marked it *blocked
pending human verification rather than guessing*. **It resolves to the restrictive reading**, with a
named `LICENSE-CC-BY-NC-4.0.txt` users must accept. ABO was structurally ideal — 8,222 listings with
24- or 72-view turntable sequences — and **non-commercial rules it out for a commercial system.**

This strengthens the V1 recommendation: **controlled first-party capture is the route**, and the best
public alternative has now closed.

---

## 6. What outcome-level persistence must change

**PROPOSED. `resources/v1/EMPIRICAL-ARTIFACT-MANIFEST-SCHEMA.yaml` v2.1 REMAINS AUTHORITATIVE** and is
not modified by this program.

**The problem:** v2.1 models `attempt → artifact → measurement` + acceptance. A real outcome is a
20-second video assembled from several generated shots, a VO, an overlay and a grade — some steps paid
provider calls, some **local ffmpeg operations that cost no money and still create artifacts** — with
a final asset that has **several parents in a specific order**. v2.1 cannot express any of it, so
**whole-outcome CpAO is not computable today.**

**Proposed topology:**
`job → outcome → sequence_or_asset_set → production_unit → production_step → attempt → artifact`

**Four changes that matter:**

1. **Multi-parent artifact lineage with ordered parents.** Concatenating shot A then B is a different
   film from B then A. A single-element parents list is exactly equivalent to today's
   `derived_from_artifact_id`, so **legacy archives keep working and are never back-filled** — they
   are marked `legacy_v2_1_no_outcome_context` rather than given invented provenance.
2. **Local deterministic steps create artifacts without provider attempts**, carrying a
   `transform_recipe` (tool, **version**, params hash + recoverable location). They create **no
   trial** — one call = one trial is untouched, because there was no call.
3. **Outcome acceptance is distinct from unit acceptance.** **This is the most dangerous confusion the
   topology introduces:** eight accepted shots inside one rejected film are eight diagnostic passes and
   **zero accepted outcomes**. Conflating them would inflate acceptance by roughly the component count
   and make CpAO look an order of magnitude better than it is. Different entities, different owners.
4. **Every v2.1 invariant preserved** — failed/refused attempts persist individually, repeat ≠ retry,
   measurements Eval-owned, costs reference immutable ledger entries.

### Whole-outcome CpAO — implemented and proven, not just specified

**OBSERVED: 9/9 controls behaved as declared.**

**The double-counting problem is real and quantified.** Provenance is a **DAG, not a tree**: one logo
composited into two shots is visited twice by a recursive walk.

| | Total |
|---|---:|
| **Correct distinct-entry recomputation** | **45.25 XTS** |
| Naive tree walk double-counting the shared logo | 51.25 XTS |
| **Overstatement** | **+13.3%** |

**The fix is structural:** cost attaches to the step or attempt that **incurred** it, never to the edge
that **consumed** it. The engine sums the *set* of distinct ledger entries exactly once.

**Failed, refused and retried attempts are all in the total** — they are what the outcome actually
cost. **Eight refusal conditions** each have an executed negative control: unresolvable cost ref,
mutable ledger entry, **no accepted outcome (CpAO is undefined, not zero)**, mixed currency, delivered
artifact outside its own provenance, local transform with no recipe, provider call with no attempt,
ledger entry with no amount.

**A note on honesty:** the engine's first run disagreed with my hand-computed fixture. **The engine was
right and my arithmetic was wrong** — I had collapsed three evaluator entries into one. The fixture was
corrected; the total never changed. Recorded rather than quietly fixed.

---

## 7. Protected sets and leakage — PROPOSED

**Five roles**, extending the accepted V1 model with one new role that changes the picture:

`request_discovery` (**new**) · `benchmark_construction` · `evaluator_calibration` ·
`active_benchmark` · `final_holdout` (protected)

**`request_discovery` sits upstream of the benchmark's existence, so its contamination reach is the
widest in the system.**

**A fourth independence level: `request_lineage`.** The existing byte / content / source-lineage levels
reason about media. **Prompts share no bytes, no parent photograph and no lab** — two prompts from the
same arena pool in the same quarter are non-independent for taxonomy purposes and **every existing
level reports them clean.**

**Six anti-circularity rules**, of which three are the operative ones:
- **discovery contaminates its whole lineage** (blocks the arena circularity directly);
- **a rephrase is a descendant, not a new item** — testing on rephrases of the discovery set is the
  specific failure being prevented;
- **a derived taxonomy carries its parent's lineage** — authorship does not launder ancestry.

**Unknown request lineage is INDETERMINATE, never independent** — the accepted R-C4 rule, unchanged.

---

## 8. What the Controller must decide at integration

| # | Decision | Why it cannot wait |
|---|---|---|
| **1** | **Is CC BY-NC data usable for taxonomy discovery in a commercial product?** | Gates VidProM and TIP-I2V. A legal judgement, not a worker's. |
| **2** | **Accept the arena lineage constraint?** | Costs Eval the option of Arena-T2I-Hard as a clean holdout. Decide before either stream builds on arena data. |
| **3** | **How strictly does "a derived taxonomy carries its lineage" apply?** | Determines whether the project can ever claim a generalisation result. Resources recommends the **strict** reading because it is checkable. |
| **4** | **Is human review time counted in CpAO?** | Changes what the metric means. The schema records it either way. |
| **5** | **Does a rejected revision's cost count toward the accepted one?** | Excluding revisions systematically understates the cost of hard briefs. |
| **6** | **Adopt the outcome topology as v3?** | Until then whole-outcome CpAO is not computable. |
| **7** | **Pitt Ads: send the email or close the route.** | Unchanged from V1; still the only public path to a commercial creative bank. |
| **8** | **Verify the four load-bearing licences officially** | LMArena, DiffusionDB, ABO, and whichever benchmark Eval adopts. One afternoon with unrestricted network. |

---

## 9. Deliverables and verification

All under `resources/research/pre-e7-macro/`:

| File | Package |
|---|---|
| `REQUEST-AND-EVAL-SOURCE-ACCESS-REGISTER.yaml` (13 sources, 11 lineages) | R3-A |
| `SOURCE-ACCESS-RIGHTS-REPORT.md` | R3-A |
| `EXISTING-RESOURCE-FIT-REBASELINE.md` | R3-B |
| `PROTECTED-SETS-AND-LEAKAGE-PROPOSAL.md` | R3-C |
| `OUTCOME-PRODUCTION-TOPOLOGY-PROPOSAL.yaml` | R3-D |
| `OUTCOME-CPAO-RECOMPUTATION.md` | R3-E |
| `CONTROLLED-PACK-ROUTES-AND-DELTA.md` | R3-F |
| `RES-003-CONTROLLER-BRIEF.md` | this |
| `validators/` (4 tools) + `fixtures/cpao/` (9 fixtures) | R3-A/E |

| Suite | Result |
|---|---|
| Source register completeness + lineage integrity | **pass** |
| Corpus rebaseline from committed metadata | **46 pass / 0 fail / 1 warn** |
| CpAO known answer + 8 required refusals | **9/9 as declared** |
| Inherited V1/V2.1 contract (nothing regressed) | **exit 0** |

**The 1 warning is the unchanged BSTD 351-vs-364 documentation discrepancy** — still open, still not
silently corrected in either direction.

## 10. Compliance

- **0** acquisitions, downloads, logins, accounts, forms, terms acceptances, purchases, emails.
- **₹0 / $0** spent. **0** generation or evaluator API calls.
- **0** media files opened from the raw corpus; **0** laptop paths assumed.
- **0** creative-quality labels. **0** Eval thresholds or metric decisions. **0** Canon truth decisions.
- **0** files edited outside `resources/`. **0** authoritative schemas rewritten — v2.1 stands.
- **0** protected roles assigned; roles belong to a named experiment and none exists.
- **0** recommendations promoted to decisions.
- **Not merged to `main`.**
