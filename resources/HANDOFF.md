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

**LAST COMPLETED TASK:** `RES-001` (24 Aug 2026). Corpus pilot v0 acquired: 4,776 items / 4.58 GB
across 4 sources — KoNViD-1k (1,200 real videos), YouTube-UGC (5 real clips, explicit CC BY 4.0),
ImageRewardDB (2,584 generated images), VideoFeedback (987 generated videos). All validated, 0
defects, 0 duplicates. Five sources blocked — none for licence silence. See
`tasks/RES-001-CONTROLLER-BRIEF.md`.

**CURRENT TASK / QUEUE:** none. RES-001 complete; awaiting Controller review. Four open decisions
in the brief, the first being third-party personal data (crowdworker IPs) shipped inside
KoNViD-1k's subjective-scores file — flagged, not deleted.

**IMPORTANT OBSERVATIONS:**
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
