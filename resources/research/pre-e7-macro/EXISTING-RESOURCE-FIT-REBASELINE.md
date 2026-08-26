# Existing resource fit — rebaseline against the widened scope

**Task:** R3-B of `resources/tasks/RES-003-CLOUD-EVIDENCE-PROGRAM.md`
**Date:** 26 Aug 2026 · **Branch:** `work/res-003-evidence-topology`
**Method:** metadata/evidence rebaseline from committed artifacts only

---

## Evidence discipline

Three labels, used on every claim:

| Label | Meaning |
|---|---|
| **FRESH-CLOUD** | Recomputed in this session from the committed manifest/registry/matrix. |
| **PRIOR-COMMITTED** | A previously recorded observation, cited, **not** re-run. |
| **NOT-ESTABLISHED** | The committed metadata cannot answer it. |

**The raw 5.70 GB corpus is git-ignored and absent from this session. No media file was opened, no
byte re-hashed, no file re-decoded.** Where the reports say "34,786 / 34,786 decode cleanly", that is
**PRIOR-COMMITTED** from `resources/reports/RES-001-integrity-report.md`. What was re-confirmed
tonight is that all 34,786 manifest records *carry* `validation_status: ok` — the **recorded** status.

**FRESH-CLOUD baseline check:** `rebaseline_from_manifest.py` → **46 pass, 0 fail, 1 warn**. Every
headline figure still reconciles: 34,786 items, 34,586 distinct hashes, 200 duplicates (173
cross-source / 27 within), 5,702,337,356 bytes, 8 sources. The one warning is the unchanged
**BSTD 351-vs-364** documentation discrepancy, still open, still not silently corrected.

---

## What the corpus actually is, measured tonight

**FRESH-CLOUD.** Three numbers reframe the corpus for a scope that now includes composed video
outcomes and campaigns:

**1. Every video we hold is short, and most are very short.**

| Duration bucket | Items |
|---|---:|
| ≤ 3 s | 987 |
| 3–6 s | 288 |
| 6–10 s | 1,200 |
| 10–30 s | 5 |
| > 30 s | **0** |

**Total video runtime across the entire corpus: 236.1 minutes. The longest single clip is 20.00
seconds**, and there are five of those — the audio-stripped YouTube-UGC sample. VideoFeedback's 987
clips are *all exactly 3.00 s*.

**2. Half the corpus is smaller than a postage stamp.** **17,748 of 34,786 items (51.0%) are under
100 pixels wide.** These are the single-word Devanagari crops. The item count has always flattered
this corpus; measured by pixels it flatters it more.

**3. The metadata cannot answer the new questions.** The manifest carries
`bytes, codec, duration_s, extension, fps, height, width, media_type, sha256, source_id, source_split,
validation_status` and paths. It carries **no shot boundaries, no speaker labels, no audio-stream
flag, and no campaign or variant grouping**. Those are **NOT-ESTABLISHED** — not absent from the
media necessarily, but unanswerable from committed evidence, and not resolvable in cloud.

---

## Fit against the nine widened need areas

**PRIOR-COMMITTED** capability baseline, unchanged: of 36 capabilities, **1 available · 10
constructed_by_eval · 5 no_external_resource · 3 partial · 17 missing**. Instrument families:
**1 available · 1 constructed_by_eval · 1 partial · 3 blocked**.

| # | Need under widened scope | What exists | Verdict |
|---|---|---|---|
| 1 | **Exact / brand text** | 29,722 photographed Devanagari items with human transcriptions; frozen 96-item generated-defect battery | **Reading: covered.** Brand/logo: 3 first-party marks only. **Generated Devanagari: still zero.** |
| 2 | **Product identity / reference conditioning** | nothing | **Missing.** And the best public route just closed — ABO is CC BY-NC (R3-A). |
| 3 | **Person identity / reference conditioning** | nothing | **Missing.** TIP-I2V's user-uploaded images are *not* a substitute — not cleared, possibly identifiable people. |
| 4 | **Temporal / multi-shot consistency** | 2,480 clips, all ≤20 s | **Weak, and newly weaker.** Multi-shot structure is **NOT-ESTABLISHED**: no shot boundaries in metadata. A 3-second clip cannot exhibit multi-shot continuity at all. |
| 5 | **Speech / audio / AV** | nothing | **Empty category.** YouTube-UGC is audio-removed. Public audio corpora exist but are audio-only and mostly NC (R3-A). |
| 6 | **Creative / commercial judgement** | nothing | **Missing.** Pitt Ads remains behind a human email gate. |
| 7 | **Longer / composed video outcomes** | **longest clip 20 s; zero above 30 s** | **Structurally absent.** This is the widened scope's newest gap and no acquisition in the register fixes it. |
| 8 | **Campaign / variant consistency** | **NOT-ESTABLISHED** — no grouping field exists | **Absent.** Nothing in the corpus is organised as "same campaign, several assets". |
| 9 | **Evaluator qualification** | text/OCR family sufficient; CV geometry constructed by Eval | **1 of 6 families ready**, 3 blocked, 1 partial. Unchanged. |

## What the widened scope changes, and what it does not

**Does not change.** The V1 assessment stands in every particular: one capability covered, four
missing packs, three blocked evaluator families, zero audio, zero generated Devanagari. Nothing
tonight rehabilitates any of that, and nothing tonight makes it worse in a way the V1 record missed.

**Changes — two new gaps, both structural.**

**Duration.** The scope now includes composed multi-step video outcomes. Our entire video holding is
**≤ 20 seconds, and 90% of it is ≤ 10 seconds**. A pool of 3-second clips cannot serve as reference,
comparison or perturbation base for a 20-second branded sequence assembled from several shots. This
is not a shortfall to top up — the *shape* is wrong.

**Composition.** Campaign/variant consistency needs assets that are *related by production intent* —
same brand, same campaign, several deliverables. Nothing in the corpus is organised that way, and the
manifest has no field that could express it. **A new pack is not obviously the answer**: the natural
home is the commercial creative bank, if grouping metadata is required at acquisition time. That is
an R3-F question and it is answered there.

## What existing material can still legitimately do

Not everything is a gap. **PRIOR-COMMITTED** and unchanged:

- **BSTD** remains the only genuine cross-lineage Devanagari reserve — the one clean holdout the
  project owns.
- **KoNViD-1k** (1,200 clips, 160 min) remains the only real filmed video at any scale and the best
  candidate perturbation base we hold, with its recorded caveat that it was sampled for *degradation*
  variety rather than cleanliness.
- **VideoGen-RewardBench** — 24 clips × 12 named generators — remains the best material for asking
  whether an evaluator scores generator A differently from generator B on comparable content.
- **The frozen 96-item Devanagari battery** remains the project's only qualified-shaped instrument
  material.

## Lineage consequence from R3-A that lands here

**`src_imagerewarddb` — 2,584 items already in our corpus — shares a lineage with DiffusionDB**
(`lin_diffusiondb`). If DiffusionDB is later acquired for request discovery, it does **not** add an
independent lineage; it enlarges one we already hold. Anything treating ImageRewardDB as a holdout
against DiffusionDB-derived work would be contaminated, and no hash check would show it.

## Open items

- **BSTD 351 vs 364** — the documentation says 351 "other language" items, the manifest holds 364.
  Unresolvable without the raw annotations. Still open, still uncorrected.
- **Multi-shot structure, audio streams and campaign grouping** are **NOT-ESTABLISHED** from committed
  metadata. Answering them requires either the acquisition machine or new acquisition with richer
  metadata captured at ingest — which is the concrete recommendation in R3-F.
