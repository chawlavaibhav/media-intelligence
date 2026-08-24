# Resources — Handoff

**PURPOSE:** Discover, licence-check, sample and validate independent media/data, keeping
evaluation media separate from the knowledge being tested.

**CURRENT STATE:** An external corpus **has** been acquired, across RES-001 and RES-002.

**CORPUS NOW — 34,786 items / 5.70 GB media across 8 acquired sources, 4 blocked.**

| source | what | items |
|---|---|---:|
| `src_bstd_devanagari` | Real Devanagari scene text + transcriptions | 25,246 |
| `src_indicstr12_devanagari` | Real Devanagari scene text + transcriptions | 3,086 |
| `src_iiit_ilst_devanagari` | Real Devanagari scene text + XML transcriptions | 1,390 |
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

**LAST COMPLETED TASK:** `RES-002` (24 Aug 2026), substantively Controller-approved with a
consistency cleanup completed. Two results. (a) **Devanagari gap closed** — 29,722 real photographed
Devanagari images with human transcriptions. (b) **Transient acquisition proved** —
VideoGen-RewardBench's 13.42 GB single archive sampled by HTTP range at 5.8% transfer, never staged
on disk; status moved from `too_large_for_pilot` to `partial_download`. Retained 1,170 MB of a
2,048 MB budget; free disk never below 14.5 GB. Also completed RES-001 finalization, including the
approved deletion of KoNViD crowdworker personal data. See `tasks/RES-002-CONTROLLER-BRIEF.md`.

**CURRENT TASK / QUEUE:** none. No RES task is open. RES-002 is closed pending final Controller
sign-off; RES-003 has not been assigned and must not be started without a Controller-created task
file.

**IMPORTANT OBSERVATIONS:**
- **Two of the three Devanagari sources are NOT independent of each other.** IndicSTR12 and IIIT-ILST
  are both CVIT / IIIT Hyderabad releases and share **173 byte-identical files** (12.4% of IIIT-ILST,
  5.6% of IndicSTR12). BSTD is genuinely independent of both. If a held-out Devanagari set is ever
  wanted, **BSTD is the clean choice** — holding out IIIT-ILST would leave ~1 in 8 of its images not
  actually unseen.
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

**PROPOSED CROSS-STREAM CHANGES:** `PROPOSED-INTEGRATION-CHANGE-RES-002-EVAL.md` filed 24 Aug 2026.

**NEXT APPROVED TASK:** none. Await a Controller-assigned task file.
