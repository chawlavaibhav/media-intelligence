# Controller — REP-07 Admission Batch — 2026-09-01

**Status:** APPROVED CONTROLLER DECISION.
**Role:** Writer Controller.
**Target:** `claude/canon-context-guidance-ohi1i9` (PR #83), carrying the REP-07 inspection and
admission work.

This record promotes decision note **DN-06** from
`canon/candidates/canon-014/REP-07-DECISION-NOTES.md` into `coordination/decisions/`, where repo
convention places Controller rulings. The worker session that recorded DN-06 was blocked by its own
permission policy from writing here and noted that the Controller would promote it at merge. This is
that promotion. Nothing is added to the ruling; the authority below is the Controller's own words.

## Authority — the Controller's words

Put to the Controller: the 13 completed REP-07 inspection passes are independently re-verified
(repo-wide Audit Gate 0 errors; 13/13 candidate records 0 errors). Proceed to admission? And ruling
(c): how do `google-abcd-video-ads` (platform-contingent official guidance) and
`sontag-on-photography` (critique, not production technique) enter?

Controller answer, session `session_01MTzh8gGKkyN31UruDXHcZo`:

> **"I am good. Proceed. Continue from where you left off."**

and, on ruling (c):

> **"Admit both, marked"**

The related standing rulings this batch executes, also in the Controller's words:

- DN-05, ruling (a), on `ries-22-immutable-laws-branding` against the live
  `binet-field-effectiveness-in-context-ch1`: **"Rule for Binet — retire ries."**
- DN-04, ruling (d), the scope-extension admission convention, answered **"Defer."** on
  2026-08-31 and resolved here by DN-06 per the standing recommendation.

## Decision

1. **Admit the 13 inspected candidates** into accepted Canon. Their knowledge enters
   `canon/knowledge/current/`; their Audit Gate v0.2 records are promoted into
   `canon/audit/records/` with digests recomputed. The repo-wide validator stays at 0 errors
   throughout. Live accepted Canon moves **24 → 37 sources**.

2. **Ruling (c) — admitted with markers.** Both contested sources enter accepted Canon carrying
   explicit `admission_conditions` that downstream compilation must surface:

   | Source | Marker | What it means |
   |---|---|---|
   | `google-abcd-video-ads` | `platform_contingent` | platform-contingent, dated official guidance |
   | `sontag-on-photography` | `critique_context` | critique context — **never** production doctrine |

   The markers exist to keep compiled packs honest about what each source is.

3. **Ruling (d) — scoped extensions, not independent origins.** The same-work extensions
   `hopkins-ch8-21`, `lsm-beyond-ch3` and `ogilvy-beyond-ch2` enter as explicitly scoped extensions
   of their live counterparts and are never counted as independent origins. Two-sided lineage
   declarations are written on the live records at admission. This continues the CANON-006 rule
   that different bibliographic authorship does not prove independent origin.

4. **`ries-22-immutable-laws-branding` is retired** per DN-05. It is not admitted, no inspection
   pass runs, and it is never put to the Audit Gate. It is retained under
   `canon/candidates/canon-014/` as source evidence with its HOLD assessment.

5. **Post-admission rebuilds** required by the REP-07 acceptance checks are part of this decision:
   corpus index and fingerprints, the coverage layer extended with authored assignments for the 13
   sources, the marker map, and recompilation of the two pilot packs (LSM coverage caveat updated
   to accepted status).

## Resulting state (mechanically checkable)

| Fact | Value | Check |
|---|---|---|
| Live accepted Canon sources | **37** | `python3 canon/validation/validate_audit_gate_v02.py` → 37 records, 0 errors |
| Knowledge objects | **1,300** SourceKnowledge · 132 concept systems · 291 bindings | `canon/knowledge/CANON-CORPUS-INDEX.yaml` |
| HOLD | **5** — desai (clean-copy diff), airey / freeman-beyond / samara-ch2 (replacement copies), ries (retired here) | same index |
| Coverage with (c) markers | live-37 map, every accepted source packed, markers carried on every affected row | `python3 canon/validation/validate_live37_coverage.py` |

The CANON-003 method-test corpus stays **16 — fixed forever**. It is a historical instrument and must
never be confused with the live count.

## Not authorised by this decision

- spend of any kind;
- Capability Registry rows;
- Production IR or Planner work;
- any change to frozen historical artifacts;
- admission of `desai`, `airey`, `freeman-beyond` or `samara-ch2` (still blocked on source copies),
  or of `ries` (retired);
- adoption of the still-PROPOSED tranche-A artifacts beyond what admission mechanically requires.
