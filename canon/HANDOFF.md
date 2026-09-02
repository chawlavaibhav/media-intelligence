# Canon — Handoff

**PURPOSE:** Build and maintain durable creative/media expertise, and make it consumable in the
production pipeline where it demonstrably matters. **Read `canon/CANON-SHAPE-v1.md` first** — it
is the settled shape of Canon for now (Controller-directed, 2026-09-01). This handoff is the map
to the current state; the shape document is the direction.

Previous handoff text (CANON-004…007 era) is preserved in git history; its durable facts are
carried below, its stale status lines are not.

---

## CURRENT STATE (2026-09-01, branch `claude/canon-context-guidance-ohi1i9`, PR #83)

**Live accepted Canon: 37 sources · 1,300 SourceKnowledge · 132 concept systems · 291 bindings.**
Grew 24 → 37 under Controller decision DN-06 (recorded in
`canon/candidates/canon-014/REP-07-DECISION-NOTES.md`; promotion to `coordination/decisions/` is a
Controller act at merge). Repo-wide Audit Gate: 37 records, 0 errors.

Two numbers that must never be confused:

| Number | Value |
|---|---|
| CANON-003 accepted books / method-test corpus | **16 — fixed forever** (`validate_canon003_integrated.py`, historical instrument) |
| Live accepted Canon | **37** (`validate_audit_gate_v02.py`) |

**HOLD (5):** desai (clean-copy diff pending), airey / freeman-beyond / samara-ch2 (replacement
copies pending), ries (retired, DN-05). `canon/knowledge/CANON-CORPUS-INDEX.yaml` is the derived
map of everything in either state; regenerate with `python3 canon/knowledge/build_corpus_index.py`.

**Derived layers, all PROPOSED, all validating green** (`canon/repair/CANON-REPAIR-PROGRAMME-v1.md`
is the task register they came from; `CANON-REPAIR-GAP-REGISTER-v1.md` the 23 gaps; the
verification report records the adversarial review that failed the first pack render and the fixes):

| Layer | Artifact | Validator |
|---|---|---|
| Coverage (live-37) | `canon/planning/live37_domain_map.yaml` + generated `CANON-V1-LIVE37-COVERAGE.*` | `validate_live37_coverage.py` |
| Join candidates | `canon/candidates/ontology-join/cross-source-candidates-v0.yaml` (60 records; SPEC-05 addendum in `canon/PROPOSED-METHOD-CHANGE-CANON-00X-CROSS-SOURCE-LAYER.md`) | `validate_cross_source_candidates.py` |
| Domain vocabulary | `canon/ontology/PROPOSED-domain-vocabulary-v1.yaml` | `validate_domain_vocabulary.py` |
| Confidence markers | `canon/context/confidence-marker-v0.yaml` + `canon/compilation/marker-map-v0.yaml` | `assign_markers.py --check` |
| Compiled packs (2/10) | `canon/compilation/PACK-*.yaml`, spec, compiler, injection contract v0 (receipt schema retired by the shape doc §5) | `validate_compiled_pack.py` |
| Pack contract / triggers | `canon/packs/COMPILED-PACK-CONTRACT-v0.1.md`, `pack-triggers-v0.yaml` | — |
| CANON_CONTEXT spec | `canon/context/` (the original packaging proposal; object shape + validator survive as the pack substrate) | `validate_canon_context.py` |

Superseded planning layers (live19, live24) are frozen history: byte-immutability enforced by
`tests/test_live37_coverage.py`; their corpus-dependent tests are skipped with the supersession reason.

## EVIDENCE STATE

- **EVAL-037** (closed): Canon helps a strong model; optional/unbounded retrieval is immature. Note
  for readers: the best lane read 53.5% HOLD material, and the "reads" statistic was an interface
  artifact — see `canon/findings/PROPOSED-EVAL-037-EVIDENCE-ANNOTATIONS.md`.
- **EVAL-038** (executed on the Controller's machine under DN-07, USD 2.26 of a 10.00 cap;
  `eval/experiments/EVAL-038/`): weak model + the two packs vs Sonnet alone, blind, extended to real
  media. Substitution **refuted 0/6**; the pack-guided image won the B06 media pair; the retro-test
  showed the doctrine forbids both human-rejected PILOT-001 candidates. Synthesis and proposed
  disposition: `canon/findings/PROPOSED-EVAL-038-CONCLUSION.md`. **The Controller has reserved the
  judgment of whether Canon works; no further conclusion is to be drawn by workers.**

## DURABLE METHOD FACTS (carried forward)

- **Audit Gate v0.2 is authoritative** (`canon/audit/AUDIT-GATE-v0.2.md`); one active record per
  source directory; the gate governs downstream *use*, not storage. One record version, fail-closed.
- **Different bibliographic authorship does not prove independent origin** (CANON-006):
  `shared_primary_informant` (Ondaatje↔Murch) and, now, `shared_author` scoped extensions
  (hopkins ch8-21, lsm-beyond, ogilvy-beyond — ruling (d)) are blocked from counting as independent
  convergence with their counterparts. Independent-origin counts are computed, never assumed.
- **Render by id, never paraphrase.** Every compiled statement traces to a committed id; the
  adversarial review caught invented doctrine once and the fix is in the compiler, not the packs.
- **A validator PASS establishes structure over committed bytes — never relevance, quality,
  outcomes, or adoption.**

## OPEN QUESTIONS

Whether the compiled-doctrine gate moves the accepted-outcome rate (Controller's measurement);
where the join layer's promotion threshold sits (SPEC-05 addendum pending); whether marker
generosity on extractor-graded `controlled_comparison` should be tightened (REP-04 review item).

## DEPENDENCIES

Merge of PR #83 (carries everything above). Controller promotion of DN-06/DN-07. Governor refresh
of `PROJECT-MEMORY.md` / `coordination/CONTROL-STATE.md`, which still describe the pre-EVAL-038
programme. Source copies for the 4 remaining HOLD candidates.

## PROPOSED CROSS-STREAM CHANGES

`canon/PROPOSED-INTEGRATION-CHANGE-CANON-CONTEXT-V0.md` (packaging shape — largely absorbed by the
shape doc); `canon/PROPOSED-METHOD-CHANGE-CANON-00X-CROSS-SOURCE-LAYER.md` (SPEC-05 addendum);
`canon/findings/PROPOSED-EVAL-037-EVIDENCE-ANNOTATIONS.md` (annotations to `eval/` and
`coordination/` prose — nothing there was edited).

## NEXT APPROVED TASK

None authorised by this handoff. The next build, when the Controller directs it, is the gate:
pre-dispatch and post-draw checks derived as code from PA-D1..D10 / CA-D1..D11
(`canon/CANON-SHAPE-v1.md` §7).
