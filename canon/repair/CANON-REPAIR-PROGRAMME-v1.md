# Canon repair — programme v1

**STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it; `coordination/CONTROL-STATE.md` governs.**

Produced 31 Aug 2026 by the Canon repair diagnosis (six expert audits + one planner, read-only, USD 0). Every numeric claim carries its recompute path.

## Execution order rationale

REP-01 through REP-04 are mutually independent and run in parallel first: REP-01 (coverage/pack seeds) removes the one defect every expert ranked blocking — a compiler keyed off the committed map ships zero Indian-context knowledge; REP-02 (join ledger) and REP-04 (markers) produce the two inputs REP-05's packs must cite (tension records T4/T5; deterministic markers); REP-03 (domain vocabulary) is independent hygiene that future compilation and extraction consume. REP-05 then compiles the two pilot packs — the programme's centre of gravity — declared dependent on REP-01/02/04 because its acceptance checks recompute markers, cite tensions, and reference the refreshed map. REP-06 has no dependencies and runs in parallel from the start; it is sequenced last in the tranche only because its dossier should cite the tranche's landed artifact paths. The blocked tranche is ordered by what unblocks it: REP-07/REP-08 wait on materials and rulings (REP-08's two free re-fetches are the highest-leverage admissions and should go first when authorised); REP-09 waits only on Controller attestation plus a Writer session and should land before REP-10, because EVAL-038's evidentiary hygiene builds on the corrected record; REP-10 (the substitution experiment — the first time the north-star treatment is ever administered) needs REP-05's packs adopted and ~USD 1 approved; REP-11 (full compiler, 8 remaining packs) needs the PR disposition and the accepted tranche-A layers; REP-12 (acquisition) is independent of all of it and gated purely on Controller purchasing/elicitation decisions. The design principle throughout: everything that turns committed bytes into proposal-grade artifacts happens now at USD 0; everything needing materials, network, attestation, adoption, or spend is a named blocked task with its exact unblocking condition, so the Controller's week is a checklist, not a research project.

## Tranche A — executable now (offline, USD 0, PROPOSED artifacts on this branch)

## Tranche B — blocked, with exact unblock conditions

## Tasks

### REP-01 · Live-24 coverage layer: domain-map extension, regenerated coverage, domain->system map, orphan backfill, demand-weighted priorities

**Tranche:** A — executed this session · **Depends on:** — · **Gaps:** GAP-01, GAP-04, GAP-15, GAP-19, GAP-08

**Deliverable.** (1) Extended canon/planning/live19_domain_map.yaml with authored entries for the 5 Indian sources, header-annotated PROPOSED; (2) regenerated CANON-V1-LIVE19-COVERAGE.yaml/.md via canon/planning/build_live19_coverage.py; (3) canon/planning/domain-system-map-v0.yaml; (4) canon/planning/PROPOSED-orphan-backfill-v0.yaml; (5) canon/planning/PROPOSED-demand-weighted-pack-priority-v1.md incl. proposed gap-ledger amendments (G3a/G3b split, G12-G15, corrected G2 prose); (6) canon/validation/validate_live24_coverage.py

**Acceptance checks.** validate_live24_coverage.py exits 0 and asserts: regenerated summary accepted_sources==24 and total_objects==677; every dir under canon/knowledge/current with source-knowledge.yaml appears in >=1 pack's contributors; indian_indic_context contributors == the 5 named sources and pack_state != absent; build_live19_coverage.py run twice produces byte-identical output; domain-system map references only scs_ids that exist in committed source-concept-systems.yaml files and every pack's domains resolve to >=1 scs_id or an explicit residue entry; orphan-backfill file contains an entry for every sk_id the committed closure recompute (script included in repo under canon/validation/) reports unreached (expect 36; each entry cites the claim text justifying the edge); every proposed relation type is from the SPEC-03 intra-source enum; priority table's demand counts recompute from the three named files (30/18/6, video 39/54).


### REP-02 · Cross-source join candidate ledger v0 + SPEC-05 addendum proposal + join validator

**Tranche:** A — executed this session · **Depends on:** — · **Gaps:** GAP-03, GAP-20

**Deliverable.** canon/candidates/ontology-join/cross-source-candidates-v0.yaml (~32 records, status: proposed on every row); canon/PROPOSED-METHOD-CHANGE-CANON-00X-CROSS-SOURCE-LAYER.md; canon/validation/validate_cross_source_candidates.py + positive/negative fixtures

**Acceptance checks.** validate_cross_source_candidates.py exits 0 on the ledger and asserts: every referenced term/sk/cc id resolves in canon/knowledge/current (ids resolving only under canon/candidates/ are legal ONLY on rows with usable != accepted_only); every relation value is from the addendum's closed enum; every row has status: proposed, a confidence grade, and a usable flag; every independence claim string matches the verdict in the corresponding canon/audit/records/*.audit.yaml related_sources_in_corpus entry (validator recomputes the lookup); rows asserting agreement/equivalence have >=2 independent origins per those verdicts; exactly one adjudication row exists for each of the 6 duplicate term strings (darshan, eye_trace, jump_cut, no_authored_page, screen_direction, story); the 16 imported crossref rows are present with usable: involves_hold; negative fixtures (bad enum value, HOLD id on accepted_only row, agreement claim on companion_volume pair) each fail with a named error.


### REP-03 · Controlled domain vocabulary v1 (two-axis) + mechanical label mapping + review queue + validator

**Tranche:** A — executed this session · **Depends on:** — · **Gaps:** GAP-13

**Deliverable.** canon/ontology/PROPOSED-domain-vocabulary-v1.yaml (22 terms + label->term mapping + singleton review queue); canon/validation/validate_domain_vocabulary.py

**Acceptance checks.** validate_domain_vocabulary.py exits 0 and asserts: recomputed label census over canon/knowledge/current/*/source-knowledge.yaml matches the file's recorded totals (1335/331/197); every one of the 331 labels appears exactly once — in the mapping OR the review queue, never both, never neither; mapped mention coverage >=90% (recomputed, not trusted from the file); every mapping target is in the closed 22-term enum with at most one term per axis; m_short_form_feed_video has zero mapped labels and carries a rationale field; running the validator twice is deterministic; a negative fixture with a label mapped to two medium terms fails.


### REP-04 · Deterministic confidence-marker layer + technology-dating and medium-transfer annex

**Tranche:** A — executed this session · **Depends on:** — · **Gaps:** GAP-12

**Deliverable.** canon/context/confidence-marker-v0.yaml (decision table); canon/compilation/assign_markers.py (emits per-sk marker map for all 677 objects); canon/planning/PROPOSED-claim-dating-annex-v1.yaml; tests/fixtures; MARKER-SCHEME.md section inside the decision-table file

**Acceptance checks.** pytest fixtures pass and: assign_markers.py run twice emits byte-identical output; every one of 677 sk_ids receives exactly one base grade; recomputed counts equal 59/337/281 (base), 85/167/110/84/122 (flags) — the validator recomputes from committed yaml, failing on any drift; every annex tech-contingent row's sk_id appears in exactly the audit record claimed (validator re-walks canon/audit/records/); the 32-id list above is a subset of the annex; every medium_transfer_untested row cites its source dir and the claim substring that triggered it; a negative fixture (object with controlled_comparison mis-marked ASSERTED) fails; marker strings render as e.g. '[REASONED|CONTESTED|MULTI-ORIGIN(2)]' with legend <=120 tokens.


### REP-05 · Two compiled pilot packs (product_appearance, composition_and_attention) + compiled-pack validator + injection contract + NR->pack trigger table

**Tranche:** A — executed this session · **Depends on:** REP-01, REP-02, REP-04 · **Gaps:** GAP-02, GAP-04, GAP-05, GAP-11, GAP-14, GAP-16, GAP-09

**Deliverable.** canon/compilation/PACK-product_appearance-v0.yaml; canon/compilation/PACK-composition_and_attention-v0.yaml; canon/compilation/COMPILED-DOCTRINE-SPEC-v0.md; canon/compilation/compile_pilot_packs.py (fresh code; renders by id, fail-closed; NO code copied from commit 8115400); canon/validation/validate_compiled_pack.py (extends canon/validation/validate_canon_context.py checks); canon/compilation/INJECTION-CONTRACT-v0.md (package schema v2); canon/packs/pack-triggers-v0.yaml + totality check

**Acceptance checks.** validate_compiled_pack.py exits 0 on both packs and asserts, each check implemented mechanically: (1) every cited sk_/scs_ id resolves under canon/knowledge/current; zero ids resolving under canon/candidates (fail-closed on collision); every cited source has a complete Audit Gate record; (2) closure — for every cited sk_id, each direction-normalized guard partner (contradicts sym / qualified_by incl. reversed qualifies / trades_off_with sym / depends_on) is cited in the same pack, named in a conflicts entry with a resolution_rule, or listed in closure_waivers with reason; regression: any pack citing sk_gos_c003_0012 must also carry sk_gos_c003_0007, sk_gos_c003_0010, sk_gos_c003_0013; (3) every decision's confidence marker equals REP-04's assigner output for its cited ids (recomputed, fail on mismatch); PA-D9's marker string contains ASSERTED, DATED and SINGLE-ORIGIN; (4) terse rendering of each pack <=2,500 tokens at 4 chars/token; the largest legal pack combination in the trigger table <=45,000 tokens (uncached break-even envelope); (5) stamped corpus digest equals the digest recomputed from CANON-CORPUS-INDEX.yaml accepted entries; (6) trigger table covers all 28 cells; every referenced pack id is one of the 10 in the coverage map; the audio cell carries the coverage-gap notice; (7) compile run twice = byte-identical output; (8) both packs contain the Devanagari limit line and product_appearance contains the LSM-later-chapters caveat, verified by exact-string grep; (9) zero occurrences of any sk_abcd_/HOLD-prefixed id in any deliverable.


### REP-06 · Runtime disposition + Controller dossier (compiled-pack contract, inspection runbook, EVAL-037 evidence annotations + spend reconciliation, EVAL-038 design, G3b elicitation spec)

**Tranche:** A — executed this session · **Depends on:** — · **Gaps:** GAP-18, GAP-10, GAP-17, GAP-06, GAP-07, GAP-19, GAP-21, GAP-22, GAP-23

**Deliverable.** canon/packs/COMPILED-PACK-CONTRACT-v0.1.md; canon/candidates/canon-014/INSPECTION-RUNBOOK.md; canon/findings/PROPOSED-EVAL-037-EVIDENCE-ANNOTATIONS.md; canon/findings/PROPOSED-EVAL-038-SUBSTITUTION-DESIGN.md; canon/planning/PROPOSED-G3B-EXPERT-ELICITATION-SPEC.md; a grep-based section-completeness checker script

**Acceptance checks.** Section-completeness checker exits 0 and asserts: the disposition table names every file in 'git show 8115400 --stat' output (25 files) plus every file under canon/context/, each with exactly one of KEEP/SALVAGE/SUPERSEDE/FREEZE/RESTATE; the runbook has one section per HOLD dir under canon/candidates/canon-014/ (18, verified by directory listing) each containing a file-identity block, an inspection-or-replacement-copy verdict, and the four Audit Gate steps; the two committed hashes appear verbatim; the annotations doc contains six blocks each with a target path, a line anchor, and a runnable recompute command (checker executes each read-only command and requires exit 0); spend figures sum to 8.372931 exactly; the EVAL-038 doc contains the strings 'maximum cost', a named model list, 'strips KNOWLEDGE_AND_WEBSITE_USE', and 'failure-path'; no deliverable modifies any file under coordination/, eval/, or governance/ (git status check); every document header contains 'PROPOSED' and a Controller-decision statement.


### REP-07 · HOLD-corpus admission batch: visual inspections, null-visual ledgers, desai clean-copy diff, replacement-copy re-verification, sullivan completion

**Tranche:** B — blocked · **Depends on:** REP-06 · **Gaps:** GAP-10, GAP-16, GAP-21

**Deliverable.** Per-source visual-evidence-ledger.yaml + Audit Gate v0.2 records in canon/audit/records/ + validator passes, executed per the REP-06 runbook, in the priority order google-abcd/w3c (see REP-08), lsm-beyond, desai, berger, then the tail

**Blocked by.** Source materials live on the Controller's machine (~/Downloads/Books/) — supply per the shopping list in blocked_on_user; Controller rulings needed: ledger-from-extraction-inspection (unlocks partial ledgers for lsm/airey/freeman/connor at zero material cost), scope-extension admission convention, ries-vs-binet adjudication, platform/critique admission boundary; three sources need replacement copies purchased (airey English, freeman paginated, samara paginated); desai needs an independent clean HarperCollins copy

**Acceptance checks.** For each admitted source: validate_audit_gate_v02.py exits 0 including the new record; the ledger's file hash matches the hash-on-arrival log; no candidate dir gains a record while still under canon/candidates/ (the desai naming wrinkle is regularised on touch); admitted scope extensions carry explicit scoped-extension marking; after admission, REP-05's validator re-run confirms pack digests were recompiled if the accepted digest changed.


### REP-08 · Re-fetch and pin the two living artifacts (WCAG 2.2 + Google ABCD), then their light visual passes and admission

**Tranche:** B — blocked · **Depends on:** REP-06 · **Gaps:** GAP-08

**Deliverable.** Dated SHA-256-fingerprinted snapshots + screenshots of https://www.w3.org/TR/WCAG22/ (+ cited Understanding docs) and the 3 Google ABCD pages, committed alongside each candidate; diff report vs extracted claims (especially w3c's 39 exact numeric criteria); then ledger + v0.2 record per REP-07 mechanics

**Blocked by.** Governance: no network fetches without Controller authorisation (both routes are free and openly licensed); admission itself additionally requires the Controller's Audit Gate decision and the platform-contingency admission-boundary ruling for google-abcd

**Acceptance checks.** Committed snapshot files hash-match their recorded SHA-256; the diff report covers 100% of each candidate's extracted claims with per-claim match/changed/gone verdicts; living_artifact_not_fingerprinted no longer applies (fingerprint block present in PROVENANCE); admission then follows REP-07 acceptance checks; w3c's numeric values in any subsequently compiled typography pack byte-match the pinned snapshot.


### REP-09 · Evidence and governance repairs in coordination/ and eval/: judging evidence or downgrade, annotations A1-A6, spend reconciliation, value-gate disposition

**Tranche:** B — blocked · **Depends on:** REP-06 · **Gaps:** GAP-06, GAP-17, GAP-22

**Deliverable.** eval/experiments/EVAL-037/judging/ (four streams' verdicts, rankings, blinding statement, judge identities) OR a Controller downgrade record; the six annotations applied to CONCLUSION.md/PROJECT-MEMORY.md/CONTROL-STATE.md; a committed consolidated spend record; a value-gate adopt-or-retire decision; a one-line Sol-asymmetry note

**Blocked by.** (1) The judging material exists only with the Controller/user — only they can produce or attest it; (2) this programme's agents may never edit coordination/, eval/, governance/ — a Writer-Controller-authorised session must apply the drafts; (3) the EVAL-037 spend-authority statement is a Controller attestation

**Acceptance checks.** Every annotation appears at its stated anchor and its embedded recompute command still exits 0; spend rows sum correctly (8.372931; 1.60; 2.6397905+0.024); either judging/ exists with >=4 stream files + a blinding statement, or the downgrade record exists — never neither; CONTROL-STATE's value-gate row no longer reads bare 'Concluded' without the never-executed qualifier.


### REP-10 · EVAL-038: the substitution experiment — weak model + compiled accepted-only packs vs strong alone

**Tranche:** B — blocked · **Depends on:** REP-05, REP-06, REP-09 · **Gaps:** GAP-07, GAP-14, GAP-23

**Deliverable.** Executed lanes per canon/findings/PROPOSED-EVAL-038-SUBSTITUTION-DESIGN.md: Haiku+packs and Gemma+packs, 6 briefs x 3 reps, unconditional injection, schema-v2 consumption forcing; committed results + blinded judging with stripped packages; preceded by the USD-0 PILOT-001 retro-test of the compiled packs

**Blocked by.** (1) User spend approval (~USD 1.0 named maximum, per the 29-Aug reset requirement); (2) Controller adoption of the compiled packs and injection contract (REP-05 outputs are proposals); (3) writer authorisation for eval/

**Acceptance checks.** Every trial's result records injected token counts and completion status (no vacuous gate passes); recorded spend <= the named maximum; blinding commitment verifies against the revealed key; stripped packages contain zero case-insensitive 'canon' matches; endpoint table recomputable from committed verdict files; the retro-test analysis cites specific pack check-ids against specific rejection reasons.


### REP-11 · Full pack compiler + remaining 8 packs at live-24

**Tranche:** B — blocked · **Depends on:** REP-01, REP-02, REP-03, REP-04, REP-05, REP-06 · **Gaps:** GAP-02, GAP-04

**Deliverable.** canon/packs/compile_pack.py (salvaging 8115400 corpus.py loader + bundle projections per the adopted disposition), the 8 remaining compiled packs, trigger-table finalisation, break-even-calibrated budgets

**Blocked by.** Controller disposition adopting the COMPILED-PACK-CONTRACT (REP-06) and the amended CANON-CONTEXT spec as pack format; cross-branch salvage of 8115400 modules is an integration only a Controller-authorised task may perform; Controller acceptance of REP-01's live-24 map and REP-02's promoted joins; the committed break-even note (REP-09)

**Acceptance checks.** All 10 packs pass validate_compiled_pack.py; compile is deterministic; every pack's stamped digest equals the current accepted digest; the three thin packs contain their coverage-gap statements; no pack cites a HOLD id; the largest legal combination stays <=45K tokens (or the committed break-even figure once it lands).


### REP-12 · Knowledge-acquisition tranche: G1 Devanagari source, G3b operational-India elicitation execution, Molly Bang re-anchor

**Tranche:** B — blocked · **Depends on:** REP-06 · **Gaps:** GAP-09, GAP-19, GAP-20

**Deliverable.** Admitted Devanagari construction source (per chosen CANON-008 option); executed G3b elicitation artifact admitted under a variant gate; the floating/ground mechanism re-derived from an accepted source or Molly Bang admitted, restoring FINDINGS-11 E-01's anchor

**Blocked by.** CANON-008 Controller option choice (Dalvi thesis behind IIT Bombay auth — 4 options open in canon/findings/CANON-008-CONTROLLER-BRIEF.md); a human Indian-market expert + Controller-approved admission variant for elicited knowledge; source acquisition + gate passage for Bang; all are spend/acquisition decisions

**Acceptance checks.** Admitted artifacts pass validate_audit_gate_v02.py; elicited knowledge carries its variant-gate marking and elicitation date; the E-01 join in any updated findings cites only accepted ids; the Devanagari limit line is removed from packs only after the G1 source is admitted and a typography pack recompiled.


## Blocked on the Controller — the action list

1. SUPPLY SOURCE MATERIALS to the inspection environment (paths are your machine, per each PROVENANCE.md): (1) Contagious.epub — MD5 625aba06ceed728ba573dad60a52b3ed, 592,807 bytes (null-visual pass); (2) Read This If You Want to Take Great Photographs.epub (14/30 objects figure_not_inspected); (3) Discussing Design.pdf (Fig 5-3 p.120, 5-4 p.123 + rest of 25 figures); (4) The Photographer's Eye — BUY a paginated/authored-page copy (current calibre PDF has invented pages); (5) This Is Marketing.epub (null pass); (6) google-abcd — authorise re-fetch of the 3 official Google pages, pinned this time; (7) My Life in Advertising.pdf (scan-page pass); (8) Scientific Advertising.pdf pp.25-64; (9) Noise.epub (Figs 16, 18); (10) Light Science & Magic 5e.epub (76 remaining figures — list in the runbook); (11) Ogilvy on Advertising.epub (reproduced ads); (12) 22 Immutable Laws of Branding.pdf (null pass, pending your Ries-vs-Binet adjudication); (13) Making and Breaking the Grid — BUY a paginated copy (ch2: 205 figures, 0 inspected); (14) On Photography.epub (null pass); (15) Hey Whipple.epub — SHA-256 b0a2630f..., 144.6MB (45 figures + unread ch 10/13/14/17); (16) w3c-wcag22 — authorise free re-fetch + version pin; (17) Logo Design Love — BUY the English original (local copy is a Spanish machine translation that inverts the Tropicana outcome); (18) Mother Pious Lady — obtain an independent clean HarperCollins India copy for the tamper-bounding diff (NOT an inspection).

2. FIVE ADMISSION RULINGS (one memo each): (a) adjudicate ries-22-immutable-laws vs live binet-field; (b) rule whether a visual-evidence-ledger may be authored from an extraction run's own contemporaneous first-hand inspection record (unlocks partial ledgers for LSM/airey/freeman/connor at zero material cost); (c) set the admission boundary for platform-contingent (google-abcd) and critique-not-craft (sontag) material; (d) confirm the scope-extension admission convention (hopkins-ch8-21, LSM-beyond, ogilvy-beyond, samara-ch2, freeman-beyond enter as scoped extensions, never independent origins); (e) authorise the two zero-cost network re-fetches (W3C + Google).

3. RULE ON PR #83 / PR #84 DISPOSITION: adopt (or amend) the merge plan REP-06 drafts — PR83 object shape + validator as compiled-pack substrate; PR84 runtime not adopted, with corpus.py/projections/question-catalogue salvaged offline; this unblocks REP-11.

4. EVAL-037 ATTESTATIONS: produce or attest the four judging streams' verdicts/rankings/blinding procedure (or accept the downgrade annotation); state what authorised the recorded USD 8.372931 spend (or record its absence); approve the six corrective annotations for a Writer session to apply.

5. COMMIT THE BREAK-EVEN ARITHMETIC (~55K-token figure and its derivation) as a short decision-adjacent note; confirm the weak-model provider so the coefficients hold.

6. VALUE-GATE DISPOSITION: retire it into the pack-evaluation design, or dispatch a Canon-naive session to author generic-contexts-real/ so the oracle experiment can run.

7. CHOOSE A CANON-008 OPTION for the Devanagari source (Dalvi thesis behind IIT Bombay auth — 4 options in canon/findings/CANON-008-CONTROLLER-BRIEF.md).

8. AFTER TRANCHE A LANDS: review-and-accept the live-24 domain assignments (REP-01), the SPEC-05 addendum + the 2 immediately promotable joins darshan and eye_trace (REP-02), and the two pilot packs + injection contract (REP-05); then approve ~USD 1.0 for EVAL-038 (REP-10).
