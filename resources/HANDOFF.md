# Resources — Handoff

**PURPOSE:** Discover, licence-check, sample and validate independent media/data, keeping
evaluation media separate from the knowledge being tested.

**CURRENT STATE:** An external corpus **has** been acquired, across RES-001 and RES-002.

**CORPUS NOW — 34,786 items / 5.70 GB media across 8 acquired sources, 4 blocked.**

| source | what | items |
|---|---|---:|
| `src_bstd_devanagari` | Real Devanagari scene text + transcriptions | 25,246 |
| `src_indicstr12_devanagari` | 375 scene photos (1–98 regions each) + 2,711 word crops = 3,086 | 3,086 |
| `src_iiit_ilst_devanagari` | 176 scene photos (1–64 regions each) + 1,214 word crops = 1,390 | 1,390 |
| `src_imagerewarddb` | Generated images, expert dimensional preference | 2,584 |
| `src_konvid1k` | Real natural video, quality MOS | 1,200 |
| `src_videofeedback` | Generated video, 5-aspect human scores | 987 |
| `src_videogen_rewardbench` | Generated video, 12 generators, pairwise preference | 288 |
| `src_youtube_ugc` | Real UGC video, explicit CC BY 4.0 | 5 |

All decode-validated, 0 defects. **34,586 distinct files — 200 duplicate hashes (27 within a single
source, 173 spanning two sources).** Blocked: `src_pvp`, `src_pitt_ads`, `src_lsvq` (access gates),
`src_ava` (explicit terms prohibition). **None blocked for licence silence.**

**Live figures are generated, not typed.** `resources/reports/RES-001-integrity-report.md` and
`RES-001-bias-and-coverage-report.md` are produced by `resources/scripts/build_reports.py` from the
manifest and registry. Coverage claims in those reports are derived from the domains actually
present, so they cannot go stale the way hand-written prose did. Rerun the script rather than
editing them.

**KNOWN GAPS** (derived — see the coverage table in the bias/coverage report):
- **Devanagari in *generated* output.** We now hold real photographed Devanagari, which tests whether
  a judge can *read* the script. We hold none of our actual failure mode: a generator *rendering*
  Devanagari wrongly, including text that drifts within a single video clip. Producing it needs
  generation spend and is outside current Resources tasks.
- No comparison material against real professional or commercial creative (Pitt Ads gated, AVA
  prohibited by site terms).
- No real photography aesthetics material. No audio — the YouTube-UGC clips are audio-removed.

**Two small internal pools also exist:** `corpus/finding-01-samples/`, and a 64-image human-scored
set that remains in the `media-factory` repo.

**CURRENT APPROVED DECISIONS:** External labels are source observations, never Canon/Eval ground
truth. Evaluation media stays independent of the knowledge under test. Rights are recorded as six
separate facts (code licence, dataset/annotation licence, underlying-media rights, redistribution,
access terms, explicit commercial-use terms). Licence silence is not a block for public, ungated,
internal-only acquisition; access gates and explicit terms still are. **Transient acquisition is the
default for large reliably-reacquirable public archives** (Charter, approved 24 Aug 2026).

**LAST COMPLETED WORK:** Resources–Eval **storage integration pass** (26 Aug 2026) on branch
`work/resources-v1-overnight`. Tightened the one canonical persistence contract to v2.1 so Eval's
emitted JSONL can validate against it exactly: one call = one trial; frozen lane and attempt-status
machine vocabularies; a canonical measurement-absence set that excludes provider failures and
`instrument_unqualified`; and cost as a reference to an immutable ledger entry rather than an inline
number. **Cross-branch gate status: `BLOCKED_WAITING_FOR_EVAL_INTERFACE`** — at
`origin/work/eval-v1-overnight@adac747` the attempts, artifacts, measurements and acceptances files
all validate, and the only remaining defect class is four missing cost-ledger fields (`unit`,
`recorded_at`, `basis`, `immutable`). Re-check with
`bash resources/v1/validators/validate_eval_archive.sh`. Brief:
`resources/findings/RESOURCES-EVAL-STORAGE-INTEGRATION-CONTROLLER-BRIEF.md`; exact delta:
`resources/v1/EVAL-ARCHIVE-INTERFACE-DELTA.md`. **0 acquisition, ₹0 spend, no Eval file edited, not
merged.**

**PRIOR WORK:** Resources V1 **correction pass** (26 Aug 2026) on branch
`work/resources-v1-overnight`, closing the Controller's five review findings on the overnight work:
the 15/36 wording made precise; one canonical attempt/artifact/measurement/acceptance storage
contract with the canonical observation vocabulary and repeats separated from retries; ~34 MB of
deterministic generated artifacts removed from Git and rebuilt by validation instead; unknown source
lineage now returns INDETERMINATE rather than being certified independent; and the accepted Eval
refinements folded into the existing four packs with no new acquisition family. **0 acquisition, ₹0
spend, not merged.** Brief: `resources/findings/RESOURCES-V1-CORRECTION-CONTROLLER-BRIEF.md`.
Eval-facing contract: `resources/v1/EVAL-STORAGE-HANDOFF.md`.

**PRIOR WORK:** Resources V1 overnight programme (26 Aug 2026) on branch
`work/resources-v1-overnight` — R1-R5 plus the R8 schema/legacy tranche, executed from a cloud
session with no access to the raw corpus. Outputs live under `resources/v1/`; the Controller Brief is
`resources/findings/RESOURCES-V1-OVERNIGHT-CONTROLLER-BRIEF.md`. **0 acquisition, ₹0 spend, not
merged.** Re-verify everything mechanical with `bash resources/v1/validators/run_all.sh`.
Headline: of Eval's 36 capabilities only **1** is served by material we already hold; 17 are
`missing`, and four packs (product, person, AV, commercial) unblock nearly all of them.

**PRIOR COMPLETED WORK:** EVAL-003 correction pass (25 Aug 2026) on branch
`work/resources-eval003-correction`. Eval found that a Resources description did not match the files
acquired; the correction is applied, independently reverified, and **merged as PR #5**. **Descriptions
only — nothing reacquired, no hash recomputed, no integrity or rights conclusion changed.** See
`reports/RES-CORRECTION-01-indicstr12-composition.md` and
`PROPOSED-INTEGRATION-CHANGE-RES-003-EVAL.md`.

**PRIOR TASK:** `RES-002` (24 Aug 2026), substantively Controller-approved with a
consistency cleanup completed. Two results. (a) **Devanagari gap closed** — 29,722 real photographed
Devanagari images with human transcriptions. (b) **Transient acquisition proved** —
VideoGen-RewardBench's 13.42 GB single archive sampled by HTTP range at 5.8% transfer, never staged
on disk; status moved from `too_large_for_pilot` to `partial_download`. Retained 1,170 MB of a
2,048 MB budget; free disk never below 14.5 GB. Also completed RES-001 finalization, including the
approved deletion of KoNViD crowdworker personal data. See `tasks/RES-002-CONTROLLER-BRIEF.md`.

**CURRENT TASK / QUEUE:** none open. RES-001/002 are closed and merged, and the EVAL-003
correction **merged as PR #5** (this line previously said "awaiting PR review" — corrected 26 Aug
2026; GOV-001 R10). The Resources V1 overnight branch is complete and awaits Controller review.

**DELIBERATE POSTURE — do not accumulate speculatively.** Resources does **not** hunt for more
Devanagari datasets, books or any other material on spec. Wait for the new Eval battery to produce a
**concrete resource requirement** — openly licensed Devanagari fonts, a particular script-phenomenon
corpus, a cross-lineage reserve, controlled generated-text failure material — and source against
that. A specific request gets a better answer than a larger pile.

**IMPORTANT OBSERVATIONS:**
- **Media categories must partition, and are now asserted to.** Each Devanagari source's media splits
  into exactly two mutually exclusive categories that sum to the acquired total:
  IndicSTR12 **375 scene + 2,711 crops = 3,086**; IIIT-ILST **176 scene + 1,214 crops = 1,390**.
  Annotation files are **not media** and are counted separately.
- **"Media acquired" is not "usable annotated records".** Of 4,476 Devanagari images, only **551** are
  photographs with their own annotation file; the other **3,925** are single-word crops. Always say
  which count is meant — reading one as the other oversizes a task roughly eightfold.
- **The crops are not unlabelled, and there are two routes.** (a) Each source ships a dedicated
  crop-level label file — `word_image_gt.txt` for IndicSTR12 (100% coverage), `WordImagesList.txt` for
  IIIT-ILST (94.7%). (b) The crop filename encodes parent + coordinates, matching one line of the
  parent scene annotation (100% / 99.7%). Union: **3,924 of 3,925 crops** resolve; exactly **1** does
  not and is named in the verifier output. So the usable pool is **3,924 single-word items** or **551
  multi-region photographs**, depending on the task.
- **A description can be wrong for months while every integrity check passes.** Our validation proves
  files decode and hash correctly — it proves nothing about whether our prose describes them. Eval
  caught this one.
- **Counting by filename pattern without filtering to media extensions is a real trap.** Both CVIT
  sources store their crop-level ground-truth file *inside* the crop directory, so a name-pattern
  detector counted three annotation `.txt` files as images. That is exactly why the first correction's
  categories summed to more media than existed. **Check the partition, not just the counts** — see
  `scripts/verify_devanagari_composition.py`, which now asserts disjointness and exhaustiveness rather
  than only comparing each number to an expected value.
- **Hash-based deduplication cannot see content reuse.** No crop is byte-identical across the two
  CVIT sources, yet **1,205 of IIIT-ILST's 1,214 crops (99.3%) come from photographs shared with
  IndicSTR12**. Different tooling, different bytes, same content. No fingerprint check will warn you.
- **Two of the three Devanagari sources are NOT independent of each other.** IndicSTR12 and IIIT-ILST
  are both CVIT / IIIT Hyderabad releases and share **173 byte-identical files** (12.4% of IIIT-ILST,
  5.6% of IndicSTR12). BSTD is genuinely independent of both. If a held-out Devanagari set is ever
  wanted, **BSTD is the clean choice.** Two valid denominators, both true: **173 of 1,390 acquired
  images (12.4%)** overall, and **173 of 176 scene photographs (98.3%)** — the latter being
  specifically the overlap rate among photographs carrying their own annotation, where only **3**
  IIIT-ILST scene photographs are unique. Crop images are **also scoreable**, so this is not a claim
  that only 551 items are usable; crop-level independence is compromised separately, because 1,205 of
  1,214 IIIT-ILST crops come from parent photographs shared with IndicSTR12. Both routes point the
  same way: treat the two CVIT releases as **one source lineage** for holdout purposes.
- **BSTD's own train/test splits are not perfectly disjoint** — 2 duplicate pairs span them.
- **A dataset's language label is not its script label.** Marathi is written in Devanagari; filtering
  BSTD by `language == hindi` would have missed 5,109 Marathi images plus 351 more labelled as other
  languages that still carry Devanagari text. Filter on the script in the transcription.
- **"Too large" may be a method limit, not a source property.** Reading the index of a 13.42 GB
  archive cost 0.5 MB over 4 range requests. Always test for a real HTTP 206 before declaring a
  source too big — a host that ignores Range replies 200 with the whole file.
- **Never fabricate a hash for an archive that was never downloaded.** Record remote metadata and
  per-member hashes instead.
- **Three byte figures exist and differ legitimately:** manifest media bytes, whole-folder bytes
  (media + retained annotations), and `du` disk-block usage. Sources made of many tiny files carry
  real block overhead — BSTD 23.3%, KoNViD-1k ~0.1%. Always say which figure is being quoted.
- Do not infer media rights from a code licence. A web search asserted the PVP *dataset* was MIT;
  that was the repository *code* licence. The trap appears unprompted.
- Prefer creator/official/lab distribution; no unofficial mirrors, torrents, piracy or arbitrary
  scraping.
- Do not construct a final holdout, new creative labels, or Canon-derived strata.

**OPEN QUESTIONS:** whether the Devanagari transcriptions survive checking by a human Hindi reader
(Resources deliberately did not do this); whether the remaining blocked sources are worth a human
completing their access forms; which gaps require proprietary collection rather than public sourcing.

**DEPENDENCIES:** none blocking Resources. Downstream, Eval depends on this corpus:
`PROPOSED-INTEGRATION-CHANGE-RES-002-EVAL.md` tells Eval what is available and what it does and does
not test. Rights are **internal research and evaluation only** — if Eval's results are ever to be
published or shown to a customer, the rights question must be reopened first.

**PROPOSED CROSS-STREAM CHANGES:** `PROPOSED-INTEGRATION-CHANGE-RES-002-EVAL.md` (24 Aug 2026) and
`PROPOSED-INTEGRATION-CHANGE-RES-003-EVAL.md` (25 Aug 2026 — confirms Eval's correction, flags that
crops carry recoverable transcriptions, and warns that hash dedup cannot see the crop-level content
reuse). The latter also proposes a replacement Resources row for
`coordination/WORKSTREAM-STATUS.md`, which is not Resources' file to edit.

**NEXT APPROVED TASK:** none. Await a Controller-assigned task file, or a concrete Eval requirement
to source against. Do not begin broad source discovery.
