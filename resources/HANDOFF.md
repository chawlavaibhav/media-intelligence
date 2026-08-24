# Resources — Handoff

**PURPOSE:** Discover, licence-check, sample and validate independent media/data, keeping
evaluation media separate from the knowledge being tested.

**CURRENT STATE:** No external dataset has been downloaded yet. A research plan exists at
`corpus/CORPUS-SOURCING-PLAN.md`; all previously listed licences remain unverified until checked at
official sources. Two small internal pools exist: `corpus/finding-01-samples/` and a larger
64-image human-scored set that remains in the `media-factory` repo.

**CURRENT APPROVED DECISIONS:** External labels are source observations, not Canon/Eval ground
truth. Evaluation media must stay independent of the knowledge under test. Rights must be separated
into code licence, dataset/annotation licence, underlying-media rights, access terms and
redistribution status.

**LAST COMPLETED TASK:** none — this stream has not executed yet.

**CURRENT TASK / QUEUE:** `tasks/RES-001.md` — bounded corpus acquisition pilot. Target 10–15 GB,
hard stop at 20 GB, no paid APIs, prioritize at least three distinct usable source/domain families
if legitimately accessible. Raw media must remain out of git; manifests/reports/scripts belong in
the repo.

**IMPORTANT OBSERVATIONS:**
- Do not infer media rights from a code licence.
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
