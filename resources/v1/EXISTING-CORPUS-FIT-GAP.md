# Existing corpus — fit and gap against the V1 requirements

**Task:** R2 of `resources/tasks/RESOURCES-V1-OVERNIGHT-PROGRAM.md`
**Date:** 26 Aug 2026 · **Branch:** `work/resources-v1-overnight`
**Verifier:** `validators/rebaseline_from_manifest.py` — executed in this cloud session, **46 pass, 0 fail, 1 warn**

---

## Read this first: what "verified tonight" means here

The raw corpus is **not in GitHub**. `.gitignore` excludes `resources/corpus/raw/`, so the 5.70 GB of
media lives only on the acquisition machine. What *is* committed, and what I therefore could check,
is the **manifest** (`corpus-pilot-v0.jsonl`, 34,786 records, 21 MB) and the **source registry**
(12 candidate records).

So three kinds of statement appear below and are labelled every time:

| Label | Meaning |
|---|---|
| **cloud-verified** | I recomputed it tonight from the committed manifest or registry. |
| **previously committed** | A prior result I cite with provenance and did **not** re-run. |
| **unavailable in cloud** | Needs raw bytes; not checkable here. |

The most important instance: **"34,786 / 34,786 decode cleanly" is previously committed**, from
`resources/reports/RES-001-integrity-report.md`. Tonight I confirmed that all 34,786 manifest records
*carry* `validation_status: ok` — that is the **recorded status**, not a re-decode. No media file was
opened in this session.

## The baseline reconciles

**cloud-verified.** Every headline figure recomputed from the manifest matches its committed value
exactly:

| Figure | Recomputed | Committed |
|---|---:|---:|
| Items | 34,786 | 34,786 |
| Distinct SHA-256 | 34,586 | 34,586 |
| Duplicate hashes | 200 | 200 |
| — cross-source | 173 | 173 |
| — within-source | 27 | 27 |
| Media bytes | 5,702,337,356 | 5,702,337,356 |
| Sources | 8 | 8 |

All 8 per-source item counts and all 8 per-source byte totals also match the registry exactly, and
both CVIT media-category partitions are **disjoint and exhaustive** (375 + 2,711 = 3,086;
176 + 1,214 = 1,390). That is checked as a partition, not as two lookups — the distinction that
caught the earlier count error.

**One discrepancy found, not reconciled.** The source registry and `resources/HANDOFF.md` both say
**351** BSTD images labelled as other languages carry Devanagari text. The manifest holds **364**
items outside the `hindi/` and `marathi/` folders (19,773 + 5,109 + 364 = 25,246, which sums
correctly). Delta 13. Deciding which is right requires the raw annotation files, which are
**unavailable in cloud**. Recorded as an open discrepancy for the acquisition machine to settle;
**not silently corrected in either direction.**

## The corpus in one honest sentence

We hold a large, well-documented pile of photographed Devanagari signage, a modest amount of
generated-image and generated-video preference material, some real video that was collected to study
compression artefacts, and **no audio, no commercial creative, no controlled references, and no
generated Devanagari at all**.

**cloud-verified composition:** 32,306 images / 2,480 videos. **85.4% of all items (29,722) are
photographed Devanagari scene text.** Total video runtime across all four video sources is
approximately **236 minutes** — KoNViD-1k 160.0 min (1,200 clips ≈ 8 s each), VideoFeedback 49.4 min
(987 clips, exactly 3.00 s each), VideoGen-RewardBench 25.1 min (288 clips, 3.75–6.12 s),
YouTube-UGC 1.7 min (5 clips ≈ 20 s).

The item count flatters the corpus badly. 34,786 sounds like a lot; it is one narrow capability
repeated 30,000 times plus four thin video pools.

---

## Source-by-source fit

### `src_bstd_devanagari` — 25,246 items, 201.4 MB · the genuine reserve

**Composition (cloud-verified):** hindi 19,773 · marathi 5,109 · 10 other language folders 364.
19 within-source duplicate hashes, of which **2 span the distributor's own train/test split**.

**Valid V1 uses:** `REQ-CAP-07` Devanagari *reading* calibration; the **cross-lineage holdout** for any
Devanagari independence claim. This is the only Devanagari source independent of the other two.

**Invalid / misleading uses:** it does not test whether a generator *renders* Devanagari — only
whether a judge can *read* it. Do **not** filter it by `language == hindi`: that would drop 5,109
Marathi images, which are written in Devanagari. Filter on the script in the transcription.
Do **not** treat the distributor's train/test split as a usable holdout boundary — 2 duplicate pairs
already cross it.

**Label provenance:** human transcriptions from the Bhashini/IIT-Jodhpur annotation effort. These are
**that group's observations**, not project ground truth, until Eval validates them. Whether they
survive checking by a Hindi reader is still untested — Resources deliberately did not do it.

**Rights:** images stated `cc-by-sa-4.0` by the repository; **annotation licence not stated**.
Internal research and evaluation only.

**Reacquisition:** creator-published Google Drive link; archive fingerprinted before deletion
(`sha256 159fb044…`), transient acquisition, selection = union of language label and Devanagari
codepoint presence.

### `src_indicstr12_devanagari` + `src_iiit_ilst_devanagari` — 4,476 items · ONE lineage

**Treat these as a single source for every independence purpose.** Two independent routes say so, and
both were cloud-verified tonight:

1. **Byte identity.** 173 hashes are shared. **All 173 shared IIIT-ILST items are scene photographs
   and none is a crop** — that is 173 of its 176 scene photographs, **98.3%**. Only 3 IIIT-ILST scene
   photographs are unique. Stated the other way round, the same 173 files are 5.6% of IndicSTR12.
   Both denominators are true; quoting one without the other misleads.
2. **Content reuse that no hash can see (previously committed).** 1,205 of IIIT-ILST's 1,214 crops
   (99.3%) derive from photographs shared with IndicSTR12. **No crop is byte-identical across the two
   sources** — different tooling, different bytes, same depicted regions. A clean deduplication report
   would say these sources are 99% distinct and would be wrong about what matters.

**This is the single most important structural fact in the corpus,** and it is why the storage
contract separates byte identity from content lineage from source lineage as three different checks.

**Valid V1 uses:** Devanagari reading development/calibration — **as one pool, allocated to one role.**
**Invalid uses:** using one to hold out against the other. Any independence claim built on the two
being separate datasets is false.

**Usable-record counts (previously committed).** Of 4,476 Devanagari images across the pair: **551**
are photographs with their own annotation file, **3,925** are single-word crops, of which **3,924**
resolve to a transcription by at least one of two routes; **exactly 1** resolves by neither. Say which
count is meant — reading one as the other mis-sizes a task roughly eightfold.

**Rights:** both `not_stated / not_verified`, photographs of real signage, no rights statement on the
CVIT project pages. Internal evaluation only; **treat as not permitted** for anything else.

### `src_imagerewarddb` — 2,584 items, 1,125.6 MB

**Valid:** developing an image-preference evaluator; the only source separating alignment, fidelity
and harmlessness as distinct dimensions — the closest public analogue to our technical-vs-creative split.
**Invalid:** as evidence about *current* models. These are **DiffusionDB-era Stable Diffusion** images.
Generator era is a hard limitation, not a caveat to wave through.
**Labels:** expert pairwise comparisons — the publisher's observations. **Rights:** apache-2.0 asserted
by the publisher over images collected from DiffusionDB; not independently verified.
**Selection integrity:** the distributor's own complete validation split was taken whole, so **no
selection judgement of ours entered the corpus**. That is worth preserving.

### `src_konvid1k` — 1,200 clips, 2,412.9 MB · 160.0 min

**Valid:** real filmed video for technical-quality evaluator development; the largest real-video pool;
candidate base clips for deterministic temporal perturbation.
**Invalid:** as creative-quality material. The population was **sampled for degradation variety** —
compression, blur, camera shake — not creative merit. For perturbation calibration you want clips
whose *only* defect is the one you introduced, so Eval must screen base-clip cleanliness first;
**I cannot screen it in this cloud session.**
**Labels:** crowdsourced subjective quality MOS. **Rights:** `not_stated`; sourced from YFCC100M,
described as Creative Commons but the distributed metadata carries **no per-video licence field**.
`flickr_id` is retained, so a future rights review could resolve per-video status if a use beyond
internal evaluation is ever proposed.
**Privacy:** the distributor shipped crowdworker IP addresses, worker IDs and city/region/country.
**Deleted 24 Aug 2026 under explicit Controller approval**, no redacted copy kept. Aggregate MOS and
technical attributes retained and contain no personal data.

### `src_videofeedback` — 987 clips, 181.6 MB · 49.4 min (all exactly 3.00 s)

**Valid:** generated-video multi-aspect score development, particularly temporal consistency — the
axis behind the cross-frame observation-unit problem.
**Invalid:** as current-generator evidence. **The dataset card names neither its source models nor
which items are its real-world augmentation portion.** You cannot attribute a behaviour to a generator
you cannot name.
**Recorded anomaly (previously committed):** the card claims 37.6k pairs / 8.81 GB; the media repo's
main revision exposes 987 mp4 files totalling 0.18 GB. **The discrepancy is unexplained and was
recorded as observed rather than reconciled.** Correct handling.

### `src_videogen_rewardbench` — 288 clips, 782.6 MB · 25.1 min

**cloud-verified:** exactly **24 clips from each of 12 named generators** — Cog5B, Easyanimatev4,
OpenSora1.2, gen3, kling, kling1.5, luma, luma1.6, minimax, qingying, tongyi, vidu. Equal
representation by construction, not first-N, which would have over-represented whichever generator
sorts first.
**Valid:** the best material we hold for *cross-generator* evaluator behaviour — does an evaluator
score generator A differently from generator B on comparable content?
**Invalid:** as a current-model benchmark; these are the generators as they were, not as they are.
**Acquisition:** the proof that "too large" was a method limit. 13.42 GB single archive, sampled by
HTTP range at **5.8% transfer**, never staged on disk. **No full-archive hash is recorded, correctly**
— the archive was never downloaded, so any hash would be fabricated.

### `src_youtube_ugc` — 5 clips, 855.1 MB · 1.7 min

**The best-documented rights position in the corpus and the smallest sample.** Explicit CC BY 4.0 with
per-item attribution, read directly from the bucket's LICENSE and ATTRIBUTION files.
**Valid:** proof of the acquisition path and the rights posture; a handful of real UGC clips.
**Invalid:** as a population — it is 5 clips. And **the clips are audio-removed**, so they contribute
nothing to the empty audio category.

---

## Blocked sources — do not reopen without a better reason than "unresolved"

| Source | Status | Blocker | Should it be reopened? |
|---|---|---|---|
| `src_pvp` | `blocked_access` | Login + terms acceptance (gate is automatic but still a gate) | **No.** Persuasion ratings serve no V1 requirement row. |
| `src_pitt_ads` | `blocked_access` | Email request to the research group — a human permission decision | **Worth a Controller decision.** It is the only public candidate that addresses `PACK-COMMERCIAL`, and its annotation zips are separately downloadable if metadata-only use is ever wanted. |
| `src_lsvq` | `blocked_access` | Download form | **No.** More real-video quality material duplicates KoNViD-1k's role. |
| `src_ava` | `blocked_license` | Site terms explicitly prohibit robots, reproduction and aggregation; photographers' copyright expressly reserved | **No, and not close.** This is an explicit prohibition, the one category policy treats as a hard limit. |

**Not one of the four is blocked for licence silence.** Three are access gates and one is an explicit
terms prohibition — exactly the categories current policy still treats as hard limits, and none of
them is waivable by a worker.

---

## Fit against the requirements matrix

| Requirement group | Served by existing corpus? |
|---|---|
| `exact_text_devanagari` (reading) | **Yes** — the one genuinely covered capability. |
| Text/OCR evaluator family | **Yes** — the only sufficient instrument family today. |
| Temporal evaluator perturbation bases | **Partly** — clips exist; cleanliness unscreened. |
| Motion/action evaluator development | **Partly** — usable for development, not for current-model qualification. |
| Product / person / logo references | **No.** Nothing. (3 first-party logo marks recovered from legacy — see the reconciliation.) |
| Speech / audio / AV | **No.** Zero audio in the corpus. |
| Commercial creative | **No.** Both public candidates blocked. |
| Generated Devanagari | **No** — and no acquisition fixes it. Only paid generation produces it. |

## Allocation: why nothing is assigned a role tonight

The corpus splits cleanly enough that it is tempting to declare BSTD the qualification holdout and
the CVIT pair the development pool. **I have not done that, deliberately.** A role is an allocation
inside a *named experiment*, and Eval has not yet frozen its experiment split. Assigning roles now
would either be overwritten or, worse, quietly treated as binding.

What R3 does instead is make the allocation **safe to perform later**: the role model, the three
leakage checks and a validator that fails closed when a protected reserve shares a lineage with a
development pool. Every view manifest built in R5 therefore carries
`protected_role: unassigned_pending_eval_experiment_split`.
