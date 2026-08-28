# Controller — CANON-012 Correction Acceptance — 2026-08-28

## Status
**CONTROLLER ACCEPTED. GOVERNOR REVIEW PENDING.**

Reviewed:
- current main: `7de9b839cefca521d335a8f67d518193061387e2`
- branch: `work/canon-012-aight-ir-seed`
- correction commit: `1ad0b7dd68954b2b6abaaa77db0b523f09321948`

## Disposition

The correction pass satisfies
`coordination/decisions/CONTROLLER-PREPILOT-RETURN-REVIEW-1-2026-08-28.md`.

Accepted corrections:
1. Creative IR conformance is now stated honestly: semantically usable, but not strictly conformant to SPEC-01 because `confidence: not_assigned` is used instead of fabricated numeric confidence.
2. F4 is narrowed correctly: exact-copy support exists; the remaining gap is a generic representation for multiple independently required exact text elements with their own roles/exactness semantics.
3. The false PILOT-001 blinding requirement is removed. Freeze-before-generation and explicit human acceptance remain.
4. Instance-local workarounds are explicitly not schema precedent.

No frozen schema, grammar, cross-stream contract, provider choice or Production IR was modified.

The later direct-Gemini/T1 route decision does not invalidate this task because CANON-012 remains model-independent.

## Remaining pilot input gate

The official Aight wordmark/master remains missing from the repository and must be supplied before the branded PILOT-001 recipe can be frozen.

AMB-05 (audio treatment) and AMB-06 (whether getaight.ai/CTA appears) remain brief-freeze decisions, not CANON-012 blockers.

## Merge gate

CANON-012 is **Controller-accepted** and eligible for the required bounded **Level-1 Repository Governor review**.

Do not merge until that review returns PASS or PASS WITH NON-BLOCKING NOTES and the Controller accepts the review.
