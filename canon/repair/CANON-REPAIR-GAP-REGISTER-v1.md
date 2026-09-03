# Canon repair — gap register v1

**STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it; `coordination/CONTROL-STATE.md` governs.**

Produced 31 Aug 2026 by the Canon repair diagnosis (six expert audits + one planner, read-only, USD 0). Every numeric claim carries its recompute path.

## North star

Convert Canon from an inert, per-source corpus into compiled, unconditionally-injected, per-pack decision doctrine (questions-with-defaults with deterministic confidence markers and guard-partner closure) so that a weak LLM plus a cheap media model beats expensive models on Cost-per-Accepted-Outcome. Tranche A builds every offline artifact this requires from committed bytes at USD 0 — coverage/join/vocabulary/marker layers, two pilot packs, and the runtime disposition — as PROPOSED artifacts under canon/; Tranche B names exactly what only the Controller can unblock (source materials, admission rulings, network fetches, attestations, spend).

## Gaps

### GAP-01 · Pack/coverage map stale: covers 19 of 24 accepted sources; all 5 Indian sources (97 objects) in no pack; indian_indic_context falsely 'absent'

**Layer:** coverage · **Severity:** blocking · **Found by:** admission, join, shape, coverage (unanimous) · **Repaired by:** REP-01

**Evidence.** canon/planning/CANON-V1-LIVE19-COVERAGE.yaml summary accepted_sources:19, packs.indian_indic_context {contributors:[], pack_state:absent}; canon/knowledge/current/ has 24 dirs/677 objects incl. bijapurkar(18), dwyer-patel(19), jain(18), pandey(10), parameswaran(32); CANON-V1-GAP-LEDGER.md G3 still claims 'zero contributors'. Verified this planning session.

**Recompute.** `cd /home/user/media-intelligence && python3 -c "import yaml,glob,os; dirs=glob.glob('canon/knowledge/current/*/'); cov=yaml.safe_load(open('canon/planning/CANON-V1-LIVE19-COVERAGE.yaml')); inpack=set(s for p in cov['packs'].values() for s in p['contributors']); print(len(dirs), cov['summary']['accepted_sources'], [os.path.basename(d[:-1]) for d in dirs if os.path.basename(d[:-1]) not in inpack])"`


### GAP-02 · No compiled pack artifact or compiler exists; both runtime proposals (PR #83, PR #84) are per-request assemblers whose model-triggered surfaces are disqualified (Gemma FULL_CANON 0/18)

**Layer:** consumption · **Severity:** blocking · **Found by:** runtime, shape · **Repaired by:** REP-05 (pilots), REP-06 (disposition); REP-11 (full compiler, blocked)

**Evidence.** canon/context/CANON-CONTEXT-SPEC-v0.1.md sec 2 defines a per-request object; git show 8115400:canon/retrieval/plan.py builds per-request bundles from raw text with a model-invoked tool surface (tools.py); the 10 packs exist only as coverage accounting; find canon -name '*pack*' returns planning files only.

**Recompute.** `git show 8115400:canon/retrieval/plan.py | head -20; sed -n '49,55p' canon/context/CANON-CONTEXT-SPEC-v0.1.md; find canon -name '*compiled*' -o -name 'PACK-*'`


### GAP-03 · Join layer empty AND inexpressible: SPEC-05 has no cross-source contradiction/tension relation and no home file; 0 of 189 relationship rows cross a source boundary — yet ~32 candidate links are verified from committed bytes, 2 independence-cleared

**Layer:** join · **Severity:** blocking · **Found by:** join, runtime · **Repaired by:** REP-02 (ledger+addendum proposal); promotion blocked on Controller review

**Evidence.** grep -n contradict canon/knowledge/SPEC-05-knowledge-ontology.md finds none in the Layer-2 vocabulary (SPEC-03 intra-source only); 589 terms/67 concepts/189 rows, 0 boundary-crossing, 0 cross_source_concept; murch-blink-p1-25/ontology-mappings.yaml:469-479 records eye_trace candidate 'NOT acted on'; 6 identical term strings unadjudicated across 2 sources each.

**Recompute.** `python3 loop over canon/knowledge/current/*/ontology-mappings.yaml counting rows whose from/to source prefixes differ (=0) and lowercased term strings spanning >1 dir (=6); grep -n 'NOT acted' canon/knowledge/current/murch-blink-p1-25/ontology-mappings.yaml`


### GAP-04 · No object-level pack membership: domains map to whole sources only, so pack traversal pulls 20-83% of corpus (critique pack degenerates to 83%), defeating O(1) per-request cost

**Layer:** shape · **Severity:** blocking · **Found by:** join, shape · **Repaired by:** REP-01 (domain->system map) + REP-05 (per-decision id binding)

**Evidence.** grep -c 'sk_\|scs_' canon/planning/live19_domain_map.yaml = 0; per-pack contributor-object upper bounds over the real 677: composition 43%, critique_and_effectiveness 83%; samara has 79 objects of which ~8 are attention-relevant; the 78 concept systems are referenced by no planning artifact.

**Recompute.** `grep -c 'sk_\|scs_' canon/planning/live19_domain_map.yaml; python3: per pack in CANON-V1-LIVE19-COVERAGE.yaml sum contributor len(source_knowledge)/677`


### GAP-05 · Nothing consumes the frozen Normalized Request: no NR->pack trigger table; packs carry no modality/operation axis; PR #84's detect_media re-derives a weaker medium from raw text

**Layer:** consumption · **Severity:** blocking · **Found by:** runtime · **Repaired by:** REP-05 (trigger table)

**Evidence.** canon/experiments/pre-execution-freeze/MEDIA-REQUEST-GRAMMAR-v1.yaml provides requested_operation (7 values) and modality (4 values incl. audio/image_sequence) plus text_requirements/brand_requirements/language_topology; grep of both runtime artifacts for these field names = 0 hits; pack records carry only contributors/domains/pack_state.

**Recompute.** `python3 -c "import yaml; g=yaml.safe_load(open('canon/experiments/pre-execution-freeze/MEDIA-REQUEST-GRAMMAR-v1.yaml')); print([f['field'] for f in g['fields']])"; git show 8115400:canon/retrieval/questions.py | sed -n '44,60p'`


### GAP-06 · EVAL-037 'Canon helps' has zero committed evidence: no judging verdicts/rankings/blinding-key on any of 201 refs; treatment blindness structurally impossible (packages self-disclose in KNOWLEDGE_AND_WEBSITE_USE); signal is Sonnet-only under a 53.4%-HOLD diet

**Layer:** evidence · **Severity:** blocking · **Found by:** evidence · **Repaired by:** REP-06 (drafts annotations); REP-09 (blocked: Controller attestation)

**Evidence.** Exhaustive path search across fetched work/eval-037-* refs finds no judgment/blind/verdict files; E037SCC-sonnet-B01-R1.txt line 98 names Canon in the package; sonnet-controlled exposure ACC 198/HOLD 227 (53.4%). The retrieval-immaturity half of the conclusion IS recomputable; the helps half is a Controller judgment without committed bytes.

**Recompute.** `git fetch origin 'refs/heads/work/eval-037-*:refs/remotes/origin/work/eval-037-*'; for b in $(git for-each-ref --format='%(refname:short)' refs/remotes); do git ls-tree -r --name-only $b | grep -iE 'judgment|blind|verdict'; done; git show origin/work/eval-037-sonnet-controlled-canon:eval/experiments/EVAL-037/runs/sonnet-controlled-canon/result.json | python3 (sum accepted/hold items_returned)`


### GAP-07 · The north-star treatment was never administered: no weak model has ever consumed Canon at scale (Gemma FULL_CANON 0/18, Haiku 3/18 trials, gemma-required 18/18 rate-limit deaths, gemma-controlled 1/18 complete); no accepted-only treatment ever delivered to anyone

**Layer:** evidence · **Severity:** blocking · **Found by:** evidence · **Repaired by:** REP-06 (EVAL-038 design draft); REP-10 (blocked: spend approval)

**Evidence.** Committed lane result.json files on origin/work/eval-037-* branches; the winning lane was Sonnet on a HOLD-majority diet. The compiled-pack claim must be established fresh; EVAL-037 cannot be cited for it.

**Recompute.** `for l in gemma-full-canon haiku-full-canon gemma-required-canon gemma-controlled-canon; do git show origin/work/eval-037-$l:eval/experiments/EVAL-037/runs/$l/result.json | python3 -c "import json,sys; d=json.load(sys.stdin); ts=d['trials']; print(d['lane_id'], sum(1 for t in ts if t.get('canon_used')), len(ts))"; done`


### GAP-08 · Video demand-supply inversion: 72% of recorded demand (39/54 units; 18/18 real marketplace cases) is video; the only two video-facing packs are the only critical_holes; newest moving-image source is 2011; the only feed-native source (google-abcd, 26 objects, sole G2/G5 fill) is HOLD behind a mechanically-fixable fingerprint blocker

**Layer:** coverage · **Severity:** blocking · **Found by:** coverage, admission · **Repaired by:** REP-01 (demand weights); REP-08 (blocked: network auth + admission)

**Evidence.** briefs.jsonl 18/30 video, marketplace-brief-bank-v1.yaml 18/18 video, EVAL-037 3/6; editing_pacing_and_short_form pack_state critical_hole, contributors' years 2001-2011; google-abcd blockers living_artifact_not_fingerprinted + platform_contingent (annotation requirement, not disqualifier).

**Recompute.** `python3 -c "import json,collections; b=[json.loads(l) for l in open('canon/experiments/v1/brief-bank/briefs.jsonl')]; print(collections.Counter(x['media_class'] for x in b))"; python3 dump of CANON-CORPUS-INDEX.yaml candidate_blocker for google-abcd-video-ads`


### GAP-09 · G1 Devanagari/Indic typography genuinely empty; gates ~41% of demand (both non-runnable marketplace cases are Indic-language); nothing on HOLD fills it

**Layer:** coverage · **Severity:** blocking · **Found by:** coverage · **Repaired by:** blocked (CANON-008 decision); REP-05 must carry explicit 'Devanagari correctness criteria DO NOT EXIST in Canon — never generate glyphs, composite text deterministically' limit line

**Evidence.** CANON-V1-GAP-LEDGER.md G1; 20/30 briefs Devanagari-primary or Hinglish; MKT-015/016 runnable_now=false; CANON-008 stopped at acquisition gate (Dalvi thesis behind IIT Bombay auth, 4 open Controller options in canon/findings/CANON-008-CONTROLLER-BRIEF.md).

**Recompute.** `python3 -c "import json; b=[json.loads(l) for l in open('canon/experiments/v1/brief-bank/briefs.jsonl')]; print(sum(1 for x in b if x['language_condition']!='english_primary'))"`


### GAP-10 · HOLD corpus (18 sources, 839 objects) blocked on figure inspection that cannot run here — but the blocker is overstated: desai's visual pass already COMPLETED (real blocker = redistributor-tampered copy needing clean-copy diff); 4 candidates (LSM-beyond 54/129 figures, airey 23pp, freeman 16pp, connor 4 figs) have first-hand contemporaneous inspection records refused as ledger input; 3 need replacement copies, not inspection (airey Spanish MT, freeman calibre-destroyed, samara reflowed)

**Layer:** admission · **Severity:** blocking · **Found by:** admission · **Repaired by:** REP-06 (runbook); REP-07 (blocked: materials + rulings)

**Evidence.** canon/candidates/canon-014/desai-mother-pious-lady/visual-evidence-ledger.yaml (pass: attempted_and_completed, no_visual_argument) + genuine v0.2 record; light-science-magic-beyond-ch3/EXTRACTION-NOTES.md sec.3; the 17 other assessments assert 'no inspection has EVER run'. All 18 dirs pass SPEC-03/04/05 validation, 0 errors; accepted corpus 24/24 records validate, zero drift.

**Recompute.** `grep -l 'assessment_kind: candidate_hold_assessment' canon/candidates/canon-014/*/audit-assessment-HOLD.yaml | wc -l (=17); grep -n 'inspected' canon/candidates/canon-014/light-science-magic-beyond-ch3/EXTRACTION-NOTES.md; python3 canon/validation/validate_audit_gate_v02.py`


### GAP-11 · Guard-relation entanglement at corpus scale: 462/677 objects (68.2%) touched by contradicts/qualifies/qualified_by/trades_off_with/depends_on edges; direction stored inconsistently (qualifies 196 vs qualified_by 79); per-object delivery ships rules without exceptions (verified: sk_gos_c003_0012 delivered without sk_gos_c003_0007/0010 contradicts + 0013 qualified_by); PR #84's bundle drops intra_source_relations entirely

**Layer:** join · **Severity:** major · **Found by:** join, shape, runtime · **Repaired by:** REP-05 (compile-time closure invariant + validator)

**Evidence.** 1,280 intra-source relations verified this session (contradicts 65, qualified_by 79, qualifies 196, trades_off_with 23, depends_on 109); git show 8115400:canon/retrieval/bundle.py projects 10 fields, none relations. Fan-out mean 1.22 max 4 — closure is cheap. (Note: 225/677 is objects CARRYING an edge; 462/677 is touched incl. targets — the operative closure bound.)

**Recompute.** `python3 undirected-union loop over canon/knowledge/current/*/source-knowledge.yaml (verified this session: 1280 edges, 462 touched); git show 8115400:canon/retrieval/bundle.py | grep -c intra_source_relations`


### GAP-12 · No computable confidence marker; technology-contingency flags (30 ids + 2 uncertain across 9 audit records) invisible to anything reading source-knowledge.yaml; film->feed medium-transfer risk unmarked on all 146 editing-pack objects; claim-level cross-source consensus is uncomputable (0 joins) — only decision-level origin count is honest

**Layer:** shape · **Severity:** major · **Found by:** coverage, shape, runtime · **Repaired by:** REP-04

**Evidence.** Evidence profile 503/677 practitioner_assertion (74.3%), 25/677 controlled_comparison (3.7%), 1082/1408 caveats extractor_observed; the flags live only in canon/audit/records/*.audit.yaml technology_contingency blocks; all 4 editing sources applicable=false (silent on transfer); GAP-LEDGER G2 forbids assuming transfer either way.

**Recompute.** `python3 census of evidence.characteristics and caveats[].origin over canon/knowledge/current/*/source-knowledge.yaml; recursive hunt for class:technology_contingent sk_refs over canon/audit/records/*.audit.yaml (expect 9 applicable, 30 ids)`


### GAP-13 · Domain labels are free text: 331 unique labels, 197 singletons (59.5%) over 1,335 mentions in the accepted corpus; a 22-term two-axis vocabulary maps 90.4% mechanically

**Layer:** shape · **Severity:** major · **Found by:** coverage · **Repaired by:** REP-03

**Evidence.** Recomputed exactly: 1,335/331/197 accepted; 3,305/711/398 with HOLD; top labels film_editing 125, advertising 81, television_editing 60, editorial_design 59; reserved term m_short_form_feed_video has zero members — itself diagnostic.

**Recompute.** `python3 -c "import yaml,glob,collections; c=collections.Counter(); [c.update(dm for o in yaml.safe_load(open(f))['source_knowledge'] for dm in (o.get('scope') or {}).get('domain_discussed_by_source') or []) for f in glob.glob('canon/knowledge/current/*/source-knowledge.yaml')]; print(sum(c.values()), len(c), sum(1 for v in c.values() if v==1))"`


### GAP-14 · FINAL_PRODUCTION_PACKAGE schema forces no doctrine consumption — the exact trap EVAL-037 proved fatal (optional use = 0/18; bounded REQUIRED structure = 18/18)

**Layer:** consumption · **Severity:** major · **Found by:** shape · **Repaired by:** REP-05 (injection contract / schema v2)

**Evidence.** eval/experiments/EVAL-037/common/system-prompt.txt: 12 sections; KNOWLEDGE_AND_WEBSITE_USE is reporting-only ('none' satisfies it); FAILURE_PREVENTION is free-form, fillable from priors.

**Recompute.** `cat eval/experiments/EVAL-037/common/system-prompt.txt`


### GAP-15 · 36 objects (5.3%) unreachable from any concept system via member_of_system + relation closure, concentrated in the 5 newest sources (pandey 50% reachable, binet-field 57%); 20 fully isolated — system-seeded compilation silently drops the newest material

**Layer:** join · **Severity:** major · **Found by:** join · **Repaired by:** REP-01 (orphan backfill proposals)

**Evidence.** BFS from system member sk_refs over undirected intra-source edges reaches 641/677 (94.7%); unreached: pandey 5, binet-field 12, parameswaran 9, ondaatje 4, murch 5, dwyer 1; all 18 older sources 100%.

**Recompute.** `python3: load source-knowledge.yaml + source-concept-systems.yaml for all 24; adj from intra_source_relations sk_ targets + system members; BFS from member set; report unreached per source`


### GAP-16 · Live accepted source light-science-magic-ch3 is qualified and in places REVERSED by its own book's HOLD later chapters — consumers get guidance the source withdraws; direct correctness risk for the product_appearance pilot pack (metal/glass/liquid packshots)

**Layer:** evidence · **Severity:** major · **Found by:** admission · **Repaired by:** REP-05 (mandatory coverage caveat in the pack, without consuming HOLD content); full fix REP-07

**Evidence.** light-science-magic-beyond-ch3/audit-assessment-HOLD.yaml source_specific_blockers[2] qualifies_a_live_accepted_source; EXTRACTION-NOTES.md sec.4 details self-qualifications.

**Recompute.** `python3 -c "import yaml; print(yaml.safe_load(open('canon/candidates/canon-014/light-science-magic-beyond-ch3/audit-assessment-HOLD.yaml'))['source_specific_blockers'][2])"`


### GAP-17 · Governing prose overclaims and spend is unaccounted: CONCLUSION.md asserts uncommitted judgments and the artifact-driven search/read lesson; CONTROL-STATE spend table omits EVAL-037 (recorded USD 8.372931, true spend higher) and PILOT-001 (USD 1.60 provisional); no committed EVAL-037 spend authorisation; value gate listed 'Concluded' though never executed (0 model calls); Sol lanes (36 trials) never ran, unrecorded

**Layer:** process · **Severity:** major · **Found by:** evidence · **Repaired by:** REP-06 (drafts annotations A1-A6 + spend reconciliation + value-gate disposition options); REP-09 (blocked: writer authorisation for coordination/eval)

**Evidence.** Line-level comparisons in the evidence expert's report, all with recompute commands; canon/experiments/v1/value-gate/PROTOCOL.md 'NOT EXECUTED'; grep -rl EVAL-037 coordination/decisions/ finds only the conclusion.

**Recompute.** `sed -n '45p;53p;96,99p' eval/experiments/EVAL-037/CONCLUSION.md; per-lane cost summation over origin/work/eval-037-* result.json files; head -8 canon/experiments/v1/value-gate/PROTOCOL.md`


### GAP-18 · Two overlapping runtime proposals unreconciled on different branches (PR #83 canon/context, PR #84 at 8115400); repair tasks risk building on incompatible substrates; validator lacks the four compilation checks (closure, marker recompute, fingerprint staleness, trigger totality)

**Layer:** process · **Severity:** major · **Found by:** runtime · **Repaired by:** REP-05 (validator extension), REP-06 (disposition doc); adoption blocked on Controller

**Evidence.** Both contracts PROPOSED; they contradict on budgets (30K chars/12 items vs 16KiB/8 entries), keying (raw text vs NR), and tool surface; canon/validation/validate_canon_context.py (345 lines, sound core) greps 0 for fingerprint/contradicts; per-request bespoke bundles are cache-hostile (0% cache reads by construction; warm packs at 0.1x push Haiku break-even from ~47-67K to ~470-670K Canon tokens).

**Recompute.** `git show 8115400 --stat | tail -30; grep -c 'fingerprint\|contradicts' canon/validation/validate_canon_context.py; break-even algebra: 2B+10O=(B+C)+5O -> C=B+5O; cached C=10(B+5O)`


### GAP-19 · G3's operational half unfilled (the 5 accepted India sources are 2002-2016 cultural history — the MOST dated corpus slice, 13/30 tech-contingent flags are theirs — not festival codes/price framing/Hinglish norms); 4 buyer-proven demand classes absent from ledger and packs: doc-content fidelity, throughput, cross-asset identity persistence, anti-AI-look negative aesthetics; no source treats UGC/creator-credibility grammar

**Layer:** coverage · **Severity:** major · **Found by:** coverage · **Repaired by:** REP-01 (proposed G3a/G3b split + G12-G15 rows), REP-06 (G3b elicitation spec); execution REP-12 blocked

**Evidence.** marketplace-brief-bank-v1.yaml capability_coverage_observations CO-01..CO-04 + GG-01/02; gap ledger (26 Aug) predates the bank (28 Aug).

**Recompute.** `python3 -c "import yaml; d=yaml.safe_load(open('canon/research/marketplace-demand-v1/derived/marketplace-brief-bank-v1.yaml')); [print(o['id'],o['cases']) for o in d['capability_coverage_observations']['observations']]"`


### GAP-20 · 16 candidate-to-live cross-source relationships parked in a file nothing consumes; 4 more join findings live only as YAML comments (murch:469, ondaatje:355, pandey:1-3, parameswaran:1-12); the corpus's best empirical join (FINDINGS-11 E-01 floating-logo -> Bang mb_009) anchors to a superseded never-accepted source

**Layer:** join · **Severity:** minor · **Found by:** admission, join · **Repaired by:** REP-02 (transcribed into ledger; crossref rows usable:involves_hold; Bang anchor recorded as unanchored pending re-derivation or admission)

**Evidence.** canon/candidates/canon-014/CROSS-SOURCE-RELATIONSHIPS.yaml (16 rows, all pointing at live accepted terms); no bang/williams/lupton dir in canon/knowledge/current.

**Recompute.** `python3 -c "import yaml; print(len(yaml.safe_load(open('canon/candidates/canon-014/CROSS-SOURCE-RELATIONSHIPS.yaml'))['relationships']))"; ls canon/knowledge/current | grep -i 'bang\|williams\|lupton'`


### GAP-21 · Copy-identity and admission hygiene: only 2/18 candidates record byte hashes; sullivan is a partial extraction recorded as whole (ch 10/13/14/17 unread) with Ogilvy independence unresolved; 5 audit records carry branch names not SHAs in recorded_at_commit

**Layer:** admission · **Severity:** minor · **Found by:** admission · **Repaired by:** REP-06 (runbook hash-on-arrival + locator-sample steps); sullivan scheduling in REP-07; SHA backfill accepted-risk until next touch

**Evidence.** grep over canon/candidates/canon-014/*/PROVENANCE.md: MD5 only berger, SHA-256 only sullivan; sullivan blockers partial_extraction_recorded_as_whole + independence_not_established; recorded_at_commit tally 3x/2x branch names (informational-only per AUDIT-GATE-v0.2.md, harmless to validation).

**Recompute.** `grep -H 'MD5\|SHA-256\|sha256' canon/candidates/canon-014/*/PROVENANCE.md; grep -h recorded_at_commit canon/audit/records/*.audit.yaml | sort | uniq -c`


### GAP-22 · The ~55K-token break-even the sizing must clear exists only in session context, not committed; if the weak model is non-Anthropic the coefficients change

**Layer:** evidence · **Severity:** minor · **Found by:** shape, runtime · **Repaired by:** blocked (Controller commits arithmetic); REP-06 states the derivation C=B+5*O (uncached) / C=10(B+5*O) (cached) as proposal

**Evidence.** grep for break-even across *.md/*.yaml matches only unrelated resources/sources/src_ava.md; all pack budgets currently compare to an unrecomputable number.

**Recompute.** `grep -rln '55K\|break-even\|breakeven' --include='*.md' --include='*.yaml' . | grep -v .git`


### GAP-23 · PILOT-001's two human-rejected candidates + frozen acceptance contract are an unused, free, already-adjudicated retro-test fixture for compiled pack doctrine (the rejection sat exactly in the creative-direction layer packs target)

**Layer:** evidence · **Severity:** minor · **Found by:** evidence · **Repaired by:** REP-06 (retro-test protocol included in EVAL-038 design as USD-0 pre-check, runnable once REP-05 packs exist)

**Evidence.** eval/pilot-001/evidence/: 2 Veo attempts, USD 0.80 each provisional; attempt 2 passed 13/13 hard checks; both rejected H1 modern/premium + H6 publishable; deterministic text/logo layer passed both times.

**Recompute.** `python3 -c "import json; print(json.load(open('eval/pilot-001/evidence/records/provider-attempt-001-cost.json'))['amount'])"`


## Where expert reports disagreed, and the resolution

Seven conflicts, resolved: (1) Executability of coverage-map regeneration — the admission expert marked it blocked ('this session is read-only') while join/shape/coverage marked it executable; resolved: the read-only constraint bound the DIAGNOSTIC sessions, not the executor tranche, whose charter is precisely to write PROPOSED artifacts under canon/ on this branch — so it is REP-01, tranche A. (2) Claims payload ~88K (session briefing, real tokenizer) vs ~80K (two experts, bytes/4 over the verified 319,104 chars): tokenizer difference, same conclusion (full injection infeasible); the programme uses the recomputable 319,104-chars figure and bytes/4 consistently. (3) Guard entanglement 462/677 = 68.2% (join expert: objects TOUCHED incl. targets — verified this session) vs 225/677 = 33.2% (runtime expert: objects CARRYING an edge): both correct under their definitions; validators use the full undirected closure, so 462 is the operative bound and both numbers appear in GAP-11. (4) Pack-compiler executability — runtime expert: blocked on cross-branch salvage of 8115400 code; shape expert: pilot packs executable now; resolved by splitting: REP-05 compiles the two pilots from hand-verified id lists with fresh code (no 8115400 code copied), while the generalised compiler that salvages corpus.py is REP-11, blocked on the Controller's PR disposition. (5) The 17-vs-18 HOLD-blocker discrepancy: the admission expert's resolution accepted — desai's visual pass is complete; its blocker is a tampered copy, so it gets a clean-copy-diff path, not an inspection slot. (6) The evidence expert's finding that 'Canon helps' has no committed evidence versus the session's accepted EVAL-037 conclusion: not re-litigated — the conclusion stands as a Controller judgment; the gap is recorded as an evidentiary-status problem whose repair is attestation-or-annotation (REP-09), never reversal by an agent. (7) 'canon/sources/figures is empty' (session briefing) vs the admission expert's correction (21 legacy jpgs + 6 txt extracts): correction accepted; materially irrelevant — nothing there serves CANON-014 inspection.
