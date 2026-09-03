# Canon repair — tranche A verification report v1

**STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it; `coordination/CONTROL-STATE.md` governs.**

> **FINAL.** Every disposition marked "FIXED this session" landed in the same commit as this
> revision and was re-verified independently: `python3 canon/validation/validate_compiled_pack.py`
> passes all five check families (double-compile byte-identical), the invented line-crossing
> mechanism greps to zero hits, both packs carry the coverage-delta declaration, and the combined
> suites (test_compiled_packs, test_canon_context_validator, test_assign_markers,
> test_live24_coverage) run 92 tests OK. Quoted sizing figures in the adversary's evidence are the
> PRE-fix packs (the historical record of the review); the post-fix figures are 10 decisions / 32 sk
> objects (product_appearance) and 11 decisions / 69 sk objects (composition_and_attention) — the
> spec's §7 table carries them.

Two independent test agents ran after the seven executors: a **verifier** (every validator, every acceptance check, id-resolution and governance sweeps) and an **adversary** instructed to refute the compiled packs against committed corpus bytes. Verifier verdict: **pass_with_findings**. Adversary verdict: **fail** — its blocking and major findings were fixed in the same session (follow-up commit) by changing the compiler's decision definitions and re-rendering; dispositions below. The adversary failing the first render is the process working, not failing: every finding cites committed bytes.

## Verifier — checks

- **REP-01 live24 coverage validator** — `python3 canon/validation/validate_live24_coverage.py` → exit 0; ok:true with 7 checks — 24 sources/677 objects, double-build byte-identical, indian_indic_context = 5 CANON-014 sources, domain-system map resolves, 36-entry backfill closes graph 677/677 under simulated adoption, demand counts 30/18/6 and 39/54 recompute, PROPOSED headers present
- **REP-01 reachability recompute** — `python3 canon/validation/recompute_system_reachability.py` → exit 0; reached 641/677, 36 unreached across 6 sources — matches the backfill file and the brief's expectation
- **REP-02 cross-source ledger validator** — `python3 canon/validation/validate_cross_source_candidates.py` → exit 0; 'OK ... 53 candidate records, all rules hold'
- **REP-02 fixtures** — `python3 canon/validation/validate_cross_source_candidates.py canon/validation/fixtures/ontology-join/<fixture>.yaml (x4)` → positive_minimal exit 0; negative_bad_relation_enum exit 1 (E_RELATION_ENUM named), negative_hold_id_on_accepted_row exit 1, negative_agreement_on_companion_pair exit 1 — each fails with a named error as the brief requires
- **REP-03 domain vocabulary validator** — `python3 canon/validation/validate_domain_vocabulary.py` → exit 0; census recomputes 1335/331/197; 295 labels mapped, 1283/1335 mentions (96.1% >= 90%); 36-label review queue; m_short_form_feed_video reserved with 0 members
- **REP-04 marker assigner drift check** — `python3 canon/compilation/assign_markers.py --check` → exit 0; outputs reproduce byte-identically; base 59/337/281, flags 85/167/110/84/122, suffixes -our_reading 21 / -hedged 634 — all equal the brief's expected counts
- **REP-05 compiled pack validator** — `python3 canon/validation/validate_compiled_pack.py` → exit 0; PASS both packs (1934 and 2496 of 2500 terse tokens), trigger table 28 cells, double-compile byte-identical with committed packs, HOLD-id scan clean over 7 deliverables
- **REP-06 runtime section checker** — `python3 tests/check_rep06_runtime_sections.py` → FAILED initially (canon/context/confidence-marker-v0.yaml: 0 disposition rows — parallel-executor race); PASSES exit 0 after the mechanical fix below
- **REP-06 dossier section checker** — `python3 tests/check_rep06_dossier_sections.py` → exit 0; 18 runbook sections complete, both hashes verbatim, A1-A6 recompute commands executed with exit 0, spend sums to 8.372931 exactly, EVAL-038 required strings present, no frozen path modified
- **unittest over all cleanly-importing test modules** — `python3 -m unittest tests.test_live24_coverage tests.test_validate_cross_source_candidates tests.test_domain_vocabulary ` → Ran 195 tests ... OK (exit 0); post-fix re-run of the 4 new-artifact suites: Ran 71 tests ... OK. Excluded as pre-declared: tests/test_request_freeze_gates.py, tests/test_validate_source_artifact_schema.py, tests/test_value_gate_corrections.py (ModuleNotFoundError: pytest; pre-existing, frozen)
- **pre-existing canon validators** — `python3 canon/validation/validate_audit_gate_v02.py; python3 canon/validation/validate_canon003_integrated.py; python3 c` → all exit 0; canon_context example: 'PASS ... (3 questions, 5 guidance, 1 conflicts, 7 refs, 2491/14240 principle/total bytes)'
- **id-resolution sweep over every new yaml** — `python3 /tmp/claude-0/-home-user-media-intelligence/2c465bd1-ff55-5c80-af5d-aa1a0d9b4aaa/scratchpad/idcheck.py` → exit 0; every id in every strict-lane new yaml resolves in canon/knowledge/current; the 22 non-current ids in the REP-02 ledger all resolve under committed canon/candidates HOLD material (usable-flag rule enforced by its validator); negative-fixture ids exempt by design
- **STATUS: PROPOSED header sweep** — `python3 one-liner over git diff --name-only 159a3a1..HEAD (43 files)` → 43/43 tranche files carry the exact 'STATUS: PROPOSED' line in their header
- **change-scope check** — `git diff --name-only 159a3a1..HEAD | grep -vE '^(canon|tests)/'; git status --porcelain` → all 43 tranche-commit files are under canon/ or tests/; working tree contains only the verifier's one mechanical fix (canon/packs/COMPILED-PACK-CONTRACT-v0.1.md); no frozen dir touched
- **regeneration-vs-committed drift** — `python3 canon/planning/build_live24_coverage.py; python3 canon/compilation/compile_pilot_packs.py; git status --porcelai` → both generators exit 0 and produce zero git drift against committed outputs — determinism and committed-state consistency hold

## Verifier — findings and dispositions

### V1 · [major] REP-06 runtime checker broken by parallel-executor race: REP-04's canon/context/confidence-marker-v0.yaml had no disposition row

**Evidence.** tests/check_rep06_runtime_sections.py scans every file under canon/context/ for exactly one disposition row in canon/packs/COMPILED-PACK-CONTRACT-v0.1.md; REP-04 created canon/context/confidence-marker-v0.yaml after REP-06's table was written, so the checker exited 1 ('expected exactly 1 disposition row, found 0'). The contract already references the file as its marker decision table (line 51).

**Tester's proposed fix.** fixed: added one KEEP row to the section 9.1 table of canon/packs/COMPILED-PACK-CONTRACT-v0.1.md, explicitly noting it is a same-tranche REP-04 PROPOSED companion added post-hoc; checker now exits 0. This row edit needs a follow-up commit by the orchestrator (executor outputs were committed as da7da99 mid-verification).

**Disposition.** FIXED by the verifier (KEEP row added to the contract's disposition table); committed in the follow-up commit.

### V2 · [minor] Compiled packs embed cross-source tension prose whose ledger of record is candidates-lane material

**Evidence.** PACK-product_appearance-v0.yaml CF-08 (xj_0023) and PACK-composition_and_attention-v0.yaml CF-16 (xj_0022) carry tension nature/resolution_rule text and a ledger_file pointer to canon/candidates/ontology-join/cross-source-candidates-v0.yaml. Both tensions cite only accepted-corpus term ids (t_alt_c003_0021, t_lsm_c003_0008, t_hop_sa_0009, t_sam_c003_0018) and the pointer carries the disclaimer 'status: proposed; referenced about the tension, not consumed as admitted doctrine'; inclusion is mandated verbatim by the REP-05 brief ('Include tension T5 ... from REP-02 ledger').

**Tester's proposed fix.** no change made — brief-mandated and properly disclaimed; the Controller should adjudicate REP-02's ledger before or together with REP-05 pack adoption so packs never cite an unadopted ledger in production.

**Disposition.** NOT ACTIONED — Controller should adjudicate the REP-02 ledger before or together with REP-05 pack adoption.

### V3 · [minor] Terse pack rendering abbreviates ids into forms that do not resolve verbatim

**Evidence.** The token-budget terse block strips sk_/scs_ prefixes and the _c003 infix (compile_pilot_packs.py line ~713), yielding e.g. 't_alt_0021 vs t_lsm_0008' and 'lsm_0008' in PACK-product_appearance-v0.yaml line 701; the structured citation blocks in the same files carry the full resolving ids, and validate_compiled_pack.py's resolution check passes.

**Tester's proposed fix.** no change made — deliberate rendering economy; if the Controller wants terse text greppable back to corpus ids, a one-line legend of the abbreviation rule inside the terse header would close the gap without spending tokens per id.

**Disposition.** FIXED this session — abbreviation legend added to the terse header (adversary finding 6 covers the same defect).

### V4 · [minor] HOLD id sk_abcd_0014 appears in the REP-04 dating annex as a quarantined note

**Evidence.** canon/planning/PROPOSED-claim-dating-annex-v1.yaml line 915: 'Admission-context reference only, NOT consumable content: HOLD source google-abcd-video-ads (sk_abcd_0014, ...' — the REP-04 brief explicitly orders this note ('Note (do not consume): HOLD sk_abcd_0014 ...'); no compiled/production artifact carries it (REP-05's HOLD scan is clean).

**Tester's proposed fix.** no change needed — brief-mandated, correctly labeled non-consumable; recorded so the Controller sees the one HOLD-id mention outside the candidates lane.

**Disposition.** NOT ACTIONED — correctly-labelled non-consumable admission-context reference; recorded for Controller visibility.

### V5 · [minor] Executor outputs were committed pre-verification, so the verifier's fix is an uncommitted working-tree change

**Evidence.** git log shows da7da99 'canon: repair tranche A executor outputs (REP-01..REP-06, pre-verification)' landed during this verification pass; git status now shows ' M canon/packs/COMPILED-PACK-CONTRACT-v0.1.md' (the disposition-row fix) as the only modification.

**Tester's proposed fix.** orchestrator should commit the one-file fix; without it, tests/check_rep06_runtime_sections.py fails on a clean checkout of da7da99.

**Disposition.** RESOLVED — the verifier's fix and all post-verification fixes land in the follow-up commit.

### V6 · [minor] Three legacy pytest test files remain unrunnable in this environment

**Evidence.** tests/test_request_freeze_gates.py, tests/test_validate_source_artifact_schema.py, tests/test_value_gate_corrections.py each raise ModuleNotFoundError: No module named 'pytest' on import; they predate this tranche and are excluded per the verification instruction (also pre-declared in REP-04's open_issues).

**Tester's proposed fix.** out of scope for this stream (frozen/historical); a future Controller-authorised task could port them to unittest or add pytest to the environment.

**Disposition.** NOT ACTIONED — pre-existing environment defect (no pytest), out of this stream's scope.

## Adversary — checks

- **Guard closure recompute (adversarial, decision-level, symmetrised from source-knowledge.yaml)** — `python3 /tmp/claude-0/-home-user-media-intelligence/2c465bd1-ff55-5c80-af5d-aa1a0d9b4aaa/scratchpad/closure_check.py` → Pack-level closure holds (no partner missing from a pack, no stale waiver; all 9 waivers match real committed edges). The frozen sk_gos_c003_0012 trap is handled: 0007/0010/0013 all compiled into CA-D9. But 8 guard edges are satisfied only in a DIFFERENT decision of the same pack with no per-decision declaration: PA-D1 (sk_lsm_c003_0015 qualified_by 0017,0018 -> PA-D8), PA-D2 (0006 qualified_by 0007 -> PA-D3), PA-D3 (0014 qualified_by 0020 -> PA-D1/D2/D10), CA-D2 (sk_fre_c003_0019 depends_on 0010 -> CA-D6, 0020 -> CA-D1), CA-D6 (0010 depends_on 0019 -> CA-D2), CA-D7 (sk_gote_c003_0010 depends_on 0056 -> CA-D9).
- **Repo pack validator (structure, markers, digest, budgets, reproducibility)** — `python3 canon/validation/validate_compiled_pack.py` → PASS on all 5 check families (both packs, trigger table 28 cells, double-compile byte-identical, HOLD-id scan clean). Confirms the validator implements the spec's pack-level closure and cited-source origin rule — not the stricter decision-level closure of this review, and not the coverage-domain origin rule of confidence-marker-v0.yaml.
- **Marker scheme reference implementation** — `python3 canon/compilation/assign_markers.py --check` → check OK: outputs reproduce byte-identically; all expected counts hold (677 objects; MEASURED 59 / REASONED 337 / ASSERTED 281; flags and suffixes match). Hand recomputation of 15 decision-level markers (PA-D1,D3,D4,D5,D6,D7,D9; CA-D1,D2,D4,D5,D6,D8,D9,D10) from evidence fields + audit technology_contingency + dating annex agrees with the packs, including PA-D9's single-claim demotion REASONED->ASSERTED and every DATED/MEDIUM-UNTESTED attachment.
- **Committed compiled-pack test suite** — `python3 -m unittest tests.test_compiled_packs -v` → Ran 28 tests, OK (including test_gos_0012_regression_is_enforced, verbatim limit-line enforcement, tamper refusals, budget overflow refusal).
- **Required limit lines + B06 consumability walk** — `grep of pack_limits/terse text in both packs; read eval/experiments/EVAL-037/common/briefs/B06.txt against INJECTION-CON` → Devanagari line present verbatim in both packs (yaml pack_limits and terse text); LSM GAP-16 caveat present in product_appearance and consistent with canon/candidates/canon-014/INSPECTION-RUNBOOK.md line 136 (later chapters QUALIFY and in places REVERSE ch3). B06 walk findings reported below.

## Adversary — findings and dispositions

### A1 · [blocking] CF-10/CF-11 inject line-crossing doctrine that exists nowhere in committed bytes

**Evidence.** PACK-composition_and_attention-v0.yaml lines 723-725 render sk_gos_c003_0012 as 'jumping the line is invisible within any single MOVING shot'; CF-10 (lines 980-981) rules 'Cross the line in a moving shot freely'; CF-11 (lines 983-984) rules 'one travelling shot may cross and re-establish the line where it settles'. The committed claim (grammar-of-the-shot-ch4/source-knowledge.yaml, sk_gos_c003_0012) describes a STATIC far-side coverage setup: 'The resulting shot is perfectly good in itself: the mistake becomes apparent only once the shots are edited together' — nothing about camera movement. Exhaustive grep of both grammar sources finds no claim about a travelling shot crossing or re-establishing the line (only sk_gos_c003_0013's dancing-couple exception and subject-travel continuity at line 275). This is real-world film doctrine imported from priors into a pack whose premise is 'questions-with-defaults over accepted Canon only', and it is injected under 'PRE-ARBITRATED CONFLICTS (the rule already decides; do not re-arbitrate)' with implied grounding in 0012/0013 the bytes do not carry.

**Tester's proposed fix.** Rewrite CF-10/CF-11 resolution rules to what 0012+0013 support: a far-side setup is not itself an error and becomes one only at the cut; crossing across a cut requires a declared creative reason (0013). Delete 'moving shot freely' and 'travelling shot may cross and re-establish' or source them via a Controller-gated admission.

**Disposition.** FIXED this session (compiler rewrite + re-render) — see the follow-up commit.

### A2 · [major] CA-D8 states Rule-of-Six weights carried by objects the decision does not cite

**Evidence.** CA-D8 default (pack lines 643-648, terse 906-910): 'emotion 51 > story 23 > rhythm 10 > eye-trace 7 > planarity 5 > 3D space 4'. compiled_from carries only sk_murch_c003_0019 (no numbers), 0020 (51) and 0023 (7). The 23/10/5/4 figures live in sk_murch_c003_0021, 0022, 0024, 0025 (verified in murch-blink-p1-25/source-knowledge.yaml), none cited. Numbers are corpus-correct but unrecomputable from the decision's citation set, against the spec's own claim (COMPILED-DOCTRINE-SPEC §1) that everything mechanical is 'rendered by id from committed bytes'. Citing 0022 (a medium_transfer seed) would not even change the decision marker — CA-D8 already carries MEDIUM-UNTESTED.

**Tester's proposed fix.** Add sk_murch_c003_0021/0022/0024/0025 to CA-D8's compiled_from (guard recompute shows no new closure obligations beyond 0026, which 0025 contradicts — that pair would need a conflicts entry or waiver).

**Disposition.** FIXED this session — weight-bearing murch ids added to CA-D8 compiled_from with guard handling.

### A3 · [major] Every India-context contributor to these packs' domains is omitted, undeclared — the compiled defaults are the Western doctrine the accepted corpus already qualifies

**Evidence.** CANON-V1-LIVE24-COVERAGE.yaml lists dwyer-patel-cinema-india and jain-gods-in-the-bazaar as contributors to composition_and_attention (A01/A02) and product_appearance (A08), and samara-making-breaking-grid-ch1 to A02/A04/E02; the packs cite ZERO sk objects from all three (samara appears only as term t_sam_c003_0018 in T4; freeman, a listed product_appearance contributor, is also uncited there). Top-5 uncompiled by value, composition pack: sk_dpci_0020 (frontality/iconicity), sk_dpci_0010 (darshan two-way look), sk_jgb_0010 (frontal gaze overrides depicted action), sk_dpci_0090 (face-first poster attention order — direct CA-D1 input), sk_sam_c003_0068 (symmetry reads authoritative, asymmetry modern — directly qualifies CA-D5's symmetry rule). Top-5, product pack: sk_dpci_0040 (props as vocabulary for period/class/modernity — staging doctrine B06-class briefs need), sk_jgb_0130 (iconographic correctness as precondition), sk_jgb_0020 (saturation as public claim on attention), sk_jgb_0070 (novelty-within-sameness), sk_dpci_0070 (clothing as semiotic grammar). CA-D2's 'off-centre' default and CA-D1's attention order would be qualified or reversed by the frontality/darshan cluster for the product's target market; the omission is silent — no pack_limit or waiver names the dropped contributors, while the coverage file advertises independent_origin_count 9 (CA) and 6 (PA) for these very domains. Partially defensible (an uncompiled indian_indic_context pack exists in the trigger table, and grid claims could belong to typography_and_copy), but REP-01's own domain map assigns these sources to THESE packs' domains, and nothing declares the delta.

**Tester's proposed fix.** Either compile the frontality/darshan/samara-structure claims into CA-D1/D2/D5 (with the new conflicts they create), or add a pack_limit line per pack naming the coverage-listed contributors deliberately deferred and to which pack.

**Disposition.** FIXED this session — per-pack pack_limit line declares the omitted coverage-listed India contributors.

### A4 · [major] Cross-source tension pairings compiled into production injection text originate in the candidates lane

**Evidence.** PA CF-08 (lines 116-143) and CA CF-16 (lines 185-209) each carry ledger_record xj_0023/xj_0022 and ledger_file canon/candidates/ontology-join/cross-source-candidates-v0.yaml. The term ids and definition_in_origin_frame strings verify against ACCEPTED ontology-mappings.yaml (checked byte-for-byte), so no candidate text leaks — but the judgment that the pair IS a tension, and the authored resolution_rule ('Condition on artifact class...', 'The valuation turns on deliberateness...'), are REP-02 candidates-lane analysis compiled as binding do-not-re-arbitrate doctrine in a production artifact. The in-file defense ('referenced about the tension, not consumed as admitted doctrine') is strained: the terse injection instructs the model to obey the rule. Governance line at risk: 'HOLD material (canon/candidates/) must NEVER appear as content in a compiled/production artifact.'

**Tester's proposed fix.** Controller call: either adopt the CANON-00X cross-source layer first (making xj_0022/0023 accepted), or strip CF-08/CF-16 to the accepted-corpus facts (both terms exist; scope differs) without a candidates-derived resolution rule.

**Disposition.** FIXED this session — CF-08/CF-16 text rewritten to accepted-corpus derivation; xj pointers marked unadopted/informational.

### A5 · [minor] Closure is pack-granular; 8 guard edges are invisible at the decision level

**Evidence.** Spec §2 defines closure as 'cited in the same pack', and the validator enforces exactly that; my stricter decision-level recompute (closure_check.py output, listed in checks) finds 8 edges whose partner lives in a different decision with no per-decision pointer — e.g. PA-D1 compiles sk_lsm_c003_0015 while its qualifiers 0017/0018 sit in PA-D8; CA-D7 compiles sk_gote_c003_0010 whose depends_on 0056 sits in CA-D9. Whole-pack injection means the text is present, so a full-pack reader is safe; but any future per-decision consumption (or a model skimming one decision) loses the qualification, and nothing in the decision entry flags it.

**Tester's proposed fix.** Add cross-references in the affected decisions' defaults (cheap, e.g. 'qualified in PA-D8') or per-decision waiver entries; alternatively document pack-granularity as an explicit contract assumption in the spec.

**Disposition.** DOCUMENTED this session — spec declares closure as pack-granular with the 8 decision-level edges listed; full cross-references left to the Controller's REP-05 review.

### A6 · [minor] Two committed, conflicting definitions of SINGLE/MULTI-ORIGIN n

**Evidence.** canon/context/confidence-marker-v0.yaml (origin_count) and canon/compilation/marker-map-v0.yaml (decision_level_origin, lines 25-37) define decision origin as the coverage DOMAIN's independent_origin_count (A02=7); COMPILED-DOCTRINE-SPEC §4.4 and validate_compiled_pack.py (independent_origin_count over cited source ids, lines 209-243) compute it from the decision's CITED sources (CA-D2 = SINGLE-ORIGIN, though its domain would say 5-7). The packs' rule is the more honest one and the injected legend matches it, but the committed REP-04 scheme the spec claims to layer on says 'Read from CANON-V1-LIVE24-COVERAGE.yaml' and its legend says 'behind the decision's domain' — two artifacts on the same branch bind n to different functions.

**Tester's proposed fix.** Supersede confidence-marker-v0.yaml's origin_count section (live24-style superseding file) to the cited-sources rule, or have the spec explicitly declare the override.

**Disposition.** DOCUMENTED this session — spec declares the decision_level_origin override explicitly; superseding the REP-04 file is Controller-review material.

### A7 · [minor] Fidelity slips: five compiled statements strengthen, invert, or repurpose their cited claims

**Evidence.** (a) CA-D1/terse: 'eyes are the strongest attractor' — sk_fre_c003_0020 says 'more strongly than PROBABLY any other kind of subject'; hedge dropped. (b) CA-D4 default 'Yes when the scene offers one' — sk_fre_c003_0022 explicitly says 'There is no compulsion to use them'; the claim is a shutter-TIMING reflex for a subject passing behind an opening, repurposed as a use-frame-within-frame recommendation. (c) CA-D10/PA: 'describing the shot's contents aloud' — sk_gote_c003_0053's claim text says 'SILENTLY describe' (the error is inherited from the committed concept_label, but the claim bytes contradict the rendering). (d) CA-D10 makes the fast-cutting norm a bound to obey; sk_gote_c003_0052 records the source calling that norm 'alarming' — valence inverted without note. (e) CA-D1 'never issue two competing cues for one beat' widens sk_ms_c003_0019 (repeated focus racking between two planes, inside the reflection technique) into a universal prohibition — partially covered by the extraction's own 'applying beyond it', and the decision's ASSERTED-hedged marker is at least present.

**Tester's proposed fix.** Reword the four defaults/terse lines to the claims' actual strength ('probably', 'no compulsion — but when used, time it cleanly', 'silently describe', 'a prevailing norm the source itself calls alarming'); none changes pack structure or budgets materially (CA is at 2496/2500 tokens, so any growth needs offsetting cuts).

**Disposition.** FIXED this session — the five defaults/terse lines reworded to the claims' actual strength.

### A8 · [minor] PRE-ARBITRATED CONFLICTS carry the packs' strongest imperatives with no markers and an override ambiguity

**Evidence.** The terse conflicts section (e.g. PA CF-02 'Never both treatments on the same surface', CF-07 'Never apply one surface's rule to the other') is authored text rendered without any evidence marker, under the header 'the rule already decides; do not re-arbitrate', while the same injection tells the model every DEFAULT is overridable via DOCTRINE_DEVIATIONS. A resolution rule is bound to a decision_ref, so overriding the decision arguably covers it, but neither the injection contract §2 block nor the terse header says whether a brief clause may force through a conflict rule and how to record it — the one arbitration a weak model is told never to touch is also the only text with no evidence label.

**Tester's proposed fix.** One sentence in the system-prompt block: conflict rules inherit their decision_ref's marker and override path; a deviation on the decision id covers its conflict rules.

**Disposition.** FIXED this session — one-sentence marker/override inheritance rule added to the injection contract.

### A9 · [minor] B06 consumability: the packs answer the lighting/composition decisions well; five named holes remain for a Haiku-class model

**Evidence.** Walking eval/experiments/EVAL-037/common/briefs/B06.txt (Aster Meridian 38 watch, 4:5 hero) through the injection contract: PA-D1/D2/D3/D8 genuinely settle finish declaration, highlight placement, source size, and crystal speculars; PA-D9+limit is honest that packshot convention is absent. Remaining wrong-by-default: (1) watch-hand position — the 10:10 convention is nowhere in Canon and no limit names hands, so the model sets time arbitrarily; (2) the brushed SUNBURST dial is anisotropic — PA-D1's three-type contrast set forces 'diffuse/direct/glare' and a model declaring 'direct' will expect a mirror image of the source, not the radial two-sector glow that is the dial's selling feature; the surface-class chapters covering exactly this are the GAP-16 HOLD chapters; (3) fixed 4:5 collides with CA-D6's check ('justified by a named shape in the scene, not by the platform alone') — the correct v2 behavior is a DOCTRINE_DEVIATIONS entry citing the brief's aspect clause, but nothing tells a weak model a brief-fixed aspect is an override rather than something to rationalize, so it will fabricate a scene-shape justification; (4) staging/context ('avoid floating-product CGI') — no decision governs environment, prop, or on-wrist staging (sk_dpci_0040 would have; see omission finding); (5) colour register (deep blue dial + brown strap vs PA-D5's 'cold grounds separate WARM subjects') is ungoverned because colour_and_visual_register is uncompiled, and a pattern-matching model may put a cold ground behind a cold-blue product.

**Tester's proposed fix.** Add a pack_limit naming watch/anisotropic-surface absence (parallel to the PA-D9 packshot line); add one sentence to INJECTION-CONTRACT §3.1: a brief-fixed deliverable parameter that collides with a default IS an override and goes in DOCTRINE_DEVIATIONS.

**Disposition.** FIXED this session — product_appearance pack_limit names the watch/anisotropic absence; deliverable-parameter precedence sentence added to the injection contract.

### A10 · [minor] Marker generosity inherited from REP-04's rule: a taste claim renders as MEASURED

**Evidence.** sk_fre_c003_0021 ('extreme placement reads as perverse') carries [MEASURED-hedged|FIGURE-UNVERIFIED] in CA-D2's compiled_from because its evidence.characteristics includes controlled_comparison — yet the committed claim calls the source's own test 'weak but explicit'. The rule is followed exactly (this is a corpus-grading artifact, not a compiler bug), but 'MEASURED' on this claim is the scheme's ceiling case for overstatement; sample of one in 15 decisions checked, everything else recomputed honestly.

**Tester's proposed fix.** No pack change; note for the Controller's REP-04 review that evidence.characteristics 'controlled_comparison' is extractor-graded and MEASURED inherits its generosity.

**Disposition.** NOT ACTIONED — Controller-review material for REP-04: 'controlled_comparison' is extractor-graded and MEASURED inherits its generosity.

