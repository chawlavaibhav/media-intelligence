# Resources — Handoff

**PURPOSE:** Discover, licence-check, sample and validate independent media/data, keeping
evaluation media separate from the knowledge being tested.

**CURRENT STATE:** An external corpus **has** been acquired. RES-001 retained 4,776 items / 4.58 GB
across four sources: KoNViD-1k (1,200 real videos), YouTube-UGC (5 real clips, explicit CC BY 4.0),
ImageRewardDB (2,584 generated images), VideoFeedback (987 generated videos). All decode-validated;
4,771 unique fingerprints (5 byte-identical duplicate pairs inside ImageRewardDB, retained and
reported). Five candidate sources are blocked — none for licence silence. Rights were verified at
official sources; `corpus/CORPUS-SOURCING-PLAN.md` remains unverified research context, not evidence.

**KNOWN GAP:** the corpus contains **no known Devanagari/Indic material**, so it does not unblock
Eval's Hindi-text checker. RES-002 Work Package A exists to close this.

Two small internal pools also exist: `corpus/finding-01-samples/` and a 64-image human-scored set
that remains in the `media-factory` repo.

**CURRENT APPROVED DECISIONS:** External labels are source observations, not Canon/Eval ground
truth. Evaluation media must stay independent of the knowledge under test. Rights must be separated
into code licence, dataset/annotation licence, underlying-media rights, access terms and
redistribution status.

**LAST COMPLETED TASK:** `RES-002` (24 Aug 2026). Two results. (a) **Devanagari gap closed** —
29,722 real photographed Devanagari images with human transcriptions from three independent
collections (BSTD 25,246 / IndicSTR12 3,086 / IIIT-ILST 1,390). (b) **Transient acquisition proved**
— VideoGen-RewardBench's 13.42 GB single archive was sampled by HTTP range at 5.8% transfer, never
staged on disk; its status changed from `too_large_for_pilot` to `partial_download`. Retained
1,170 MB of a 2,048 MB budget; free disk never below 14.5 GB. Also completed RES-001 finalization
including the approved deletion of KoNViD crowdworker personal data. See
`tasks/RES-002-CONTROLLER-BRIEF.md`.

**CORPUS NOW:** 34,786 items / 5.70 GB across 8 acquired sources; 4 blocked (2 access gates, 1
explicit terms prohibition, 1 gated). 4,771 unique fingerprints — 5 duplicate hashes inside
ImageRewardDB, retained and reported.

**CURRENT TASK / QUEUE:** none. RES-002 complete, awaiting Controller review. Three open decisions
in the brief; the first is whether Google Drive's large-file "virus scan warning" interstitial counts
as an access gate — I judged it does not (no credential, no agreement, any anonymous visitor can
proceed), which is why BSTD was acquired. If the Controller disagrees, BSTD must be marked
`blocked_access` and removed.

**IMPORTANT OBSERVATIONS:**
- **A dataset's language label is not its script label.** Marathi is written in Devanagari; in BSTD,
  filtering by `language == hindi` would have missed 5,109 Marathi images plus 351 more labelled as
  other languages that still carry Devanagari text. Filter on the script in the transcription.
- **"Too large" may be a method limit, not a source property.** A zip keeps its index at the end, and
  hosts answering HTTP 206 allow member-level fetching. Reading the index of a 13.42 GB archive cost
  0.5 MB. Always test for range support before declaring a source too big.
- Do not infer media rights from a code licence. A web search asserted the PVP *dataset* was MIT;
  that was the repository *code* licence. The trap is real and appears unprompted.
- Licence silence is not a block for public, ungated, internal-only use (clarification 6) — but
  record rights as `not_stated`/`not_verified` and never present such material as cleared.
- Access gates and explicit terms still block absolutely. Every remaining blocked source is blocked
  for one of those, not for silence.
- Prefer creator/official/lab distributions; no unofficial mirrors, torrents, piracy or arbitrary
  scraping.
- Access/login/payment/licence ambiguity is a STOP, not a puzzle to work around.
- Do not create a final holdout, new creative labels, or Canon-derived strata in RES-001.

**OPEN QUESTIONS:** actual licence/access status of candidate sources; what mixture is legitimately
acquirable inside the budget; which gaps will require later proprietary collection.

**DEPENDENCIES:** none to start source verification/acquisition. EVAL-001 may later refine which
corpus properties are most valuable, but RES-001 is deliberately broad enough to proceed now.

**PROPOSED CROSS-STREAM CHANGES:** none filed yet.

**NEXT APPROVED TASK:** `RES-001` only. After acquisition/validation and Controller Brief, stop; do
not construct the benchmark or start evaluation.
