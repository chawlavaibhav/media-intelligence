# Controller — PILOT-001 Candidate 1 Technical Review — 2026-08-28

## Status
**TECHNICAL / EVIDENCE GATE PASSED. HUMAN H1-H6 GATE PENDING.**

Reviewed:
- branch `work/pilot-001-aight-execution`
- head `7ecc49e6efd9357c1e45cb708bf11e31cff319d7`
- base/current main `002beec2d8859d10a759a07aea92f8497e0f0b23`
- branch behind_by 0 / ahead_by 1.

## Real execution evidence

Accepted as real PILOT-001 product-learning evidence:
- direct Gemini Developer API;
- model `veo-3.1-fast-generate-preview`;
- one 8-second 9:16 720p provider generation;
- operation `models/veo-3.1-fast-generate-preview/operations/hog3ds7hhp43`;
- provider status resolved OK;
- 0 retries;
- one provider call only;
- provisional consumed API cost USD 0.80;
- stable cost_ref `pilot-cost-res-000001`;
- provider MP4 retained as class-C empirical bytes;
- deterministic Aight claims/endcard composition retained;
- final candidate retained at 12.000 s, 720x1280, 9:16, no audio;
- hard-check report 12/12 PASS;
- pre-acceptance RES-007 archive validates G1-G12;
- CpAO correctly remains undefined before an accepted outcome.

The one authorised repair remains unconsumed.

## Human gate

No customer-level acceptance is recorded yet. This is correct.

The next decision is the frozen H1-H6 human review:
- H1 modern and premium;
- H2 recognisably Indian-festive without named-festival dependence;
- H3 restrained / not gaudy;
- H4 primary takeaway = Aight is an outcome API;
- H5 prices are immediately legible and primary;
- H6 reviewer would put it in front of an Aight customer / publish it.

All six must pass for customer-level acceptance.

If any fail, the Controller decides whether the single repair is:
- local deterministic; or
- one second/final provider generation.

No worker may consume the repair before this human disposition.

## Deviations / corrections to route after human review

### D1 — credential preflight deviation
The runbook said `GEMINI_API_KEY` must already exist and otherwise STOP.
The worker reports the environment instead had the same Gemini Developer API credential available
as `GOOGLE_API_KEY` from the user's local key source and exported it as `GEMINI_API_KEY` for the
dispatch process.

This is a procedural deviation from the literal preflight. It does not currently invalidate the
evidence because:
- provider surface/model were unchanged;
- no alternative credential/provider was used;
- no key value is committed in the branch;
- the route still read `GEMINI_API_KEY` at dispatch;
- spend authority and attempt limits were respected.

Record it honestly; do not rewrite history to say the preflight matched exactly.

### D2 — machine-specific durable locations
Several committed attempt / transform / RES archive records contain the worker machine's absolute
`/Users/...` paths even though the durable artifacts are correctly committed under
`eval/pilot-001/evidence/`.

Before final task merge, normalise durable evidence locations to repo-relative or otherwise portable
references without changing artifact bytes, hashes, attempt identity, cost evidence or topology.
This is evidence-metadata hygiene, not the one creative repair.

## Integration posture

Do not merge the execution branch yet.

Sequence:
1. actual human H1-H6 review;
2. if needed, exactly one bounded repair;
3. record final accepted/rejected outcome through RES-007;
4. compute the available CpAO view if accepted;
5. correct D1/D2 documentation/portability without changing empirical bytes;
6. Controller final review;
7. Level-1 Governor review;
8. merge and close T1.

No T2 execution starts until T1's final disposition is durable.
