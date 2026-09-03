# CANON-014 HOLD corpus — per-source inspection runbook

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

**What this is.** An executable protocol for the figure-level inspection / copy-verification passes
that the 18 HOLD candidates under `canon/candidates/canon-014/` need before any of them can be put
to the Audit Gate. It is a runbook ABOUT admission. It admits nothing, contains no HOLD knowledge
content, asserts no Controller decision, and spends USD 0. The source files live on the
Controller's machine (`~/Downloads/Books/` and the live web for two candidates); no inspection can
run in this repository's container. Compiled from the admission expert's shopping list
(REP-06 seed), each candidate's `PROVENANCE.md` / `EXTRACTION-NOTES.md` /
`audit-assessment-HOLD.yaml`, and `canon/audit/AUDIT-GATE-v0.2.md`. Gaps addressed: GAP-10, GAP-21.

**Corpus under management:** 18 HOLD directories, 839 `source_knowledge` objects
(recompute: `python3 -c` summing `len(source_knowledge)` over
`canon/candidates/canon-014/*/source-knowledge.yaml` — 50+54+30+55+17+55+29+26+70+48+50+60+70+49+45+22+70+39 = 839).

---

## Universal protocol (applies to every section below)

**Step zero — hash-on-arrival.** Before anything is opened: `sha256sum` (and `md5sum` where the
recorded hash is MD5) every supplied file, and record path, byte size and hash at the head of the
new `visual-evidence-ledger.yaml`. Where `PROVENANCE.md` records a hash of the original book file,
compare; a match proves the inspection is looking at the same copy the extraction read. The two
book-file hashes committed verbatim in the brief's identity set are:

- berger-contagious — MD5 `625aba06ceed728ba573dad60a52b3ed` (592,807 bytes)
- sullivan-hey-whipple — SHA-256
  `b0a2630f368fb62c25f7f08d2135267e3ebe1e4165be253ce1056c391ec2095d` (144,649,816 bytes)

Several other PROVENANCE files also record original-file hashes (airey PDF, carroll/godin/sontag/
kahneman EPUBs, ries/hopkins PDFs, freeman PDF, desai EPUB); GAP-21's "only 2/18 hashed" count
understates what is on disk — recount with
`grep -c 'SHA-256\|MD5\|sha256' canon/candidates/canon-014/*/PROVENANCE.md`. Hash-on-arrival is
step zero for all 18 regardless of what is recorded.

**Locator-verification sample.** Locators (printed-page offsets like connor's printed=PDF-18,
spine numbers, converter-invented pages) are copy-specific. Before trusting per-object
`figure_refs`, verify a sample of locators against the arrived copy whenever (a) the on-arrival
hash does not match a recorded original-file hash, or (b) no original-file hash is recorded at all
(connor-irizarry-discussing-design, ogilvy-beyond-ch2, light-science-magic-beyond-ch3 — path+size
only, samara original EPUB — size only, and the two web candidates). Sample rule: open 5 cited
figure/page locators spread across the extraction's range; all 5 must land on the described
content, else treat every locator in that source as unverified and re-derive before inspecting.

**Null-result ledger template.** The worked example of a completed null visual pass is
`canon/candidates/canon-014/desai-mother-pious-lady/visual-evidence-ledger.yaml`: full image
enumeration with byte sizes, size histogram separating decorative furniture from content-bearing
images, `visual_argument_role: no_visual_argument` recorded as a role, not a loss pattern, and a
`no_loss_detected` entry stating why nothing visual was lost. Prose-only EPUB candidates follow it.

**Admission steps (Audit Gate v0.2) — the same four steps close every section:**
(i) author `visual-evidence-ledger.yaml` from the real inspection (never from a prose summary);
(ii) fresh checkpoint;
(iii) v0.2 record with 5-file snapshot in `canon/audit/records/`;
(iv) validator pass — `python3 canon/validation/validate_audit_gate_v02.py`.
`evidence_insufficient` is a completed outcome that does NOT admit (desai proves this).

**Controller decisions this runbook depends on (none executable by any agent):**
(a) adjudicate ries-22-immutable-laws vs live binet-field-effectiveness-in-context-ch1;
(b) rule whether a ledger may be authored from an extraction run's own contemporaneous first-hand
figure inspection (unlocks partial ledgers for LSM-beyond 54 figs / airey 23 pp / freeman 16 pp /
connor 4 figs at zero material cost);
(c) set the admission boundary for platform-contingent guidance (google-abcd) and
critique-not-craft material (sontag);
(d) confirm the scope-extension admission convention (hopkins-ch8-21, LSM-beyond, ogilvy-beyond,
samara-ch2, freeman-beyond enter as explicitly scoped extensions, never as independent origins);
(e) authorize the network fetches for the W3C/Google re-pin.

**Verdict vocabulary:** `INSPECT` (open the listed figures/pages in the existing copy),
`REPLACEMENT-COPY` (a different copy is required before any pass),
`CLEAN-COPY-DIFF` (desai only: obtain an independent clean copy and diff),
`RE-FETCH-AND-PIN` (living web artifact: re-fetch, fingerprint, then inspect).

---

## 1. google-abcd-video-ads — priority 1

**Rank rationale:** the ONLY candidate touching G2 (short-form feed-native grammar — critical and
empty; "the entire video half of the first product") and G5 (feed hooks); 26 objects of
checklist-shaped platform guidance, ideal for questions-with-defaults doctrine; admission is a free
re-fetch. Condition: platform/time-contingency boundary explicit on every object (decision (c)).

**File identity (as recorded):** no local book file. Extraction read 3 official Google pages
(Ads Help / Google Business / Think with Google), retrieved 2026-08-30, URLs in `PROVENANCE.md`;
processed text `scratchpad/src/SRC-google-abcd.txt`, 31,262 bytes, SHA-256
`df27a00fa974cf2369e8c4d5a6ef51f5a2b0b88c85d89947402beabeb35d85e4`. No page bytes were pinned.

**Verdict:** RE-FETCH-AND-PIN — re-fetch the 3 pages under decision (e); record retrieval date,
byte-exact snapshots, SHA-256 per page, and screenshots; then diff against the 26 extracted
objects' claims.

**What to open:** every image/diagram on the 3 pages (ABCD framework illustrations); the light
visual pass runs over the pinned snapshots, not the live pages.

**Expected ledger shape:** fetch manifest (URL, date, SHA-256, screenshot ref per page) + per-figure
rows; `visual_argument_role` as found (likely illustrative-of-stated-propositions).

**Admission steps (Audit Gate v0.2):** (i) author `visual-evidence-ledger.yaml` from the real
inspection; (ii) fresh checkpoint; (iii) v0.2 record with 5-file snapshot in
`canon/audit/records/`; (iv) validator pass.

## 2. w3c-wcag22-text-legibility — priority 2

**Rank rationale:** exact numeric criteria (contrast ratios, resize %, spacing multipliers) are the
best possible weak-model doctrine — numbers replace judgement, directly serving capability
substitution; fills G8 thumbnail-scale legibility; the corpus's only standards document; openly
licensed, zero acquisition cost.

**File identity (as recorded):** no local book file. Canonical URL `https://www.w3.org/TR/WCAG22/`
plus cited Understanding documents; local source text `scratchpad/src/SRC-wcag22.txt` (3,055
lines); no byte fingerprint of the fetched pages recorded ("a criterion is only as good as the
version it came from" — `audit-assessment-HOLD.yaml`, `living_artifact_not_fingerprinted`).

**Verdict:** RE-FETCH-AND-PIN — re-fetch WCAG 2.2 + the cited Understanding docs under decision
(e) (W3C Document Licence, zero cost), record dated version + SHA-256 fingerprints, then inspect.

**What to open:** Understanding SC 1.4.11 Figure 41 and Figures 8–14. 48 figures are referenced in
total; 3 objects carry `figure_not_inspected` (incl. `sk_wcag_0034` in this candidate's
`source-knowledge.yaml`); the extraction's own assessment found figures illustrate stated
propositions, so the pass is small.

**Expected ledger shape:** version pin (dated W3C version + per-document SHA-256) + rows for the
inspected figures; numeric criteria re-verified verbatim against the pinned version.

**Admission steps (Audit Gate v0.2):** (i) author `visual-evidence-ledger.yaml` from the real
inspection; (ii) fresh checkpoint; (iii) v0.2 record with 5-file snapshot in
`canon/audit/records/`; (iv) validator pass.

## 3. light-science-magic-beyond-ch3 — priority 3

**Rank rationale:** fills the convention half of G4 product/packshot appearance (metal, glass,
liquids = scenario families 2 and 5) AND removes a live-corpus correctness risk: the later
chapters QUALIFY and in places REVERSE guidance in the live accepted `light-science-magic-ch3`
(`audit-assessment-HOLD.yaml` `source_specific_blockers[2]`, `EXTRACTION-NOTES.md` §4). Admit as
explicit scope extension (decision (d)). 54/129 cited figures already inspected first-hand during
extraction (decision (b) turns them into a partial ledger).

**File identity (as recorded):** `~/Downloads/Books/Light Science & Magic, 5th Edition.epub`,
9,692,005 bytes; NO original-file hash recorded (path+size only) — hash-on-arrival plus the
5-locator sample are mandatory before trusting figure refs. Processed text
`scratchpad/src/EPUB-Light_Science___Magic__5th_Editi.txt`, 468,886 bytes.

**Verdict:** INSPECT.

**What to open:** the 76 of 129 cited figures not opened during extraction, mostly diagrams:
4.1, 4.4–4.8, 5.7–5.8, 5.19–5.24, 6.1–6.6, 6.13–6.16, 6.18, 6.20–6.22, 6.25, 6.28, 6.30, 6.32,
7.3–7.4, 7.6–7.7, 9.13, 9.17, 9.19, plus the ch9 characteristic-curve graphs and ch10
mixed-colour diagrams. 54 figures were already opened first-hand (53 recorded in
`provenance.inspected.figures`; matched pairs verified; one over-claim caught — the 7.24/7.25 pair
producing the `sk_lsmx_0049` caveat) — see `EXTRACTION-NOTES.md` §3.

**Expected ledger shape:** full figure ledger; under decision (b) it may incorporate the 54
first-hand rows from the extraction's contemporaneous record, leaving 76 fresh rows.

**Admission steps (Audit Gate v0.2):** (i) author `visual-evidence-ledger.yaml` from the real
inspection; (ii) fresh checkpoint; (iii) v0.2 record with 5-file snapshot in
`canon/audit/records/`; (iv) validator pass.

## 4. desai-mother-pious-lady — priority 4

**Rank rationale:** `indian_indic_context` (C13), interpretive middle-class consumer
meaning-making (scooter, thali, matrimonial column — precisely B2C India); the only interpretive
consumer-culture candidate in the dock; its visual pass is already DONE.

**File identity (as recorded):**
`8d18d4df-Santosh_Desai__Mother_Pious_Lady__…_libgen.li.epub`, SHA-256
`b0a2fb33bde95c44018e5558c80129d74e4c9b13288be356c29c940fa2e2e305`, 532,237 bytes, 33 images.
The copy is redistributor-tampered: `dc:publisher` overwritten to GAPPAA.ORG, the string injected
at 11 enumerated positions including one unmarked sentence inside an authorial Introduction
paragraph (`audit-assessment-HOLD.yaml`, `audit_status_reason`).

**Verdict:** CLEAN-COPY-DIFF — NOT an inspection. Obtain an independent clean copy (HarperCollins
India), hash it on arrival, and diff against the extraction to bound redistributor tampering: the
11 enumerated GAPPAA.ORG injection sites are known; the risk being bounded is unmarked further
edits.

**What to open:** nothing figure-level. `visual-evidence-ledger.yaml` exists and is complete
(`pass: attempted_and_completed`, 33 images enumerated, `figures: 0`,
`visual_argument_role: no_visual_argument`) — it is the null-result template every prose-only
candidate below reuses. Desai also already carries a genuine v0.2-shaped assessment
(`audit_record_version: v0.2`, 5-file snapshot, `audit_status: evidence_insufficient`); it sits
outside `canon/audit/records/` and its naming should be regularized when touched.

**Expected ledger shape:** the existing ledger stands; the diff report (clean copy vs extraction
copy, per-injection-site disposition) is the new evidence artifact.

**Admission steps (Audit Gate v0.2):** (i) author `visual-evidence-ledger.yaml` from the real
inspection — here: append the clean-copy diff result to the completed ledger;
(ii) fresh checkpoint; (iii) v0.2 record with 5-file snapshot in `canon/audit/records/`;
(iv) validator pass.

## 5. berger-contagious — priority 5

**Rank rationale:** commercial_communication / B2C sharing mechanics (STEPPS); genuine independent
origin (nearest live neighbour heath-made-to-stick); 54 objects + 60-item QA bank; unusually good
evidence-origin hygiene (notes separate whose research each finding is); near-trivial null-visual
pass.

**File identity (as recorded):** `/Users/vaibhavchawla/Downloads/Books/Contagious_ Why Things
Catch On.epub`, 592,807 bytes, MD5 `625aba06ceed728ba573dad60a52b3ed` — one of the two brief-named
book-file hashes; on-arrival MD5 must match before the pass counts.

**Verdict:** INSPECT — expected null-visual pass (extraction found no figure refs).

**What to open:** unpack the EPUB, enumerate and measure every image, open everything large enough
to carry content, confirm no text points at any image.

**Expected ledger shape:** desai null-result template — image enumeration, size histogram,
`no_visual_argument` as role not loss, `no_loss_detected` entry.

**Admission steps (Audit Gate v0.2):** (i) author `visual-evidence-ledger.yaml` from the real
inspection; (ii) fresh checkpoint; (iii) v0.2 record with 5-file snapshot in
`canon/audit/records/`; (iv) validator pass.

## 6. hopkins-scientific-advertising-ch8-21 — priority 6

**Rank rationale:** cheap public-domain scope extension (decision (d)), commercial_communication
depth; scan-page pass only.

**File identity (as recorded):** `Scientific Advertising.pdf` (public-domain IA scan), SHA-256
`e081207466c2f8da334bf6bdeba8c454c17107e6ddfe90cbccc0d95e8531b6fc` (recomputed in the extraction
lane, matching the supplied fingerprint); printed pp.25–64 = ch8–21.

**Verdict:** INSPECT — scan-page pass over printed pp.25–64; no figure refs recorded.

**What to open:** the scan pages themselves (legibility/completeness of the scan), not figures.

**Expected ledger shape:** desai null-result template + scan-page completeness rows.

**Admission steps (Audit Gate v0.2):** (i) author `visual-evidence-ledger.yaml` from the real
inspection; (ii) fresh checkpoint; (iii) v0.2 record with 5-file snapshot in
`canon/audit/records/`; (iv) validator pass.

## 7. hopkins-my-life-in-advertising — priority 7

**Rank rationale:** same class as priority 6 (cheap public-domain pass, commercial_communication);
unranked in the seed's first-five — placed here by the same rationale, authored judgement marked
as such.

**File identity (as recorded):** `My Life in Advertising.pdf` (public-domain IA scan), SHA-256
`7842a0944d315a37fcf8a054f6141a16935ee3322bbc062afbfba8d6fac53e5f`; printed pp.1–206; processed
text `SRC-mylife.txt`, 288,156 bytes, 209 page markers.

**Verdict:** INSPECT — scan-page pass over printed pp.1–206; no figure refs recorded.

**What to open:** scan pages (legibility/completeness), not figures.

**Expected ledger shape:** desai null-result template + scan-page completeness rows.

**Admission steps (Audit Gate v0.2):** (i) author `visual-evidence-ledger.yaml` from the real
inspection; (ii) fresh checkpoint; (iii) v0.2 record with 5-file snapshot in
`canon/audit/records/`; (iv) validator pass.

## 8. kahneman-sibony-sunstein-noise — priority 8

**Rank rationale:** evaluation doctrine for the Eval side of the programme; only 2 named figures to
open.

**File identity (as recorded):** `/Users/vaibhavchawla/Downloads/Books/Noise_ A Flaw in Human
Judgment.epub`, 2,761,980 bytes, original SHA-256
`2fae4d85f000122401b780edbfcb27d1191308c3fc757af4b8cf7ef57386f7a6`; extracted text 850,276 bytes.

**Verdict:** INSPECT.

**What to open:** Figures 16 and 18, plus any figure in the judgement slice the extraction read.

**Expected ledger shape:** small figure ledger (2+ rows) over an otherwise prose book.

**Admission steps (Audit Gate v0.2):** (i) author `visual-evidence-ledger.yaml` from the real
inspection; (ii) fresh checkpoint; (iii) v0.2 record with 5-file snapshot in
`canon/audit/records/`; (iv) validator pass.

## 9. godin-this-is-marketing — priority 9

**Rank rationale:** cheap null-visual pass, lower doctrine yield than the top five.

**File identity (as recorded):** `This Is Marketing.epub`, 2,377,250 bytes, EPUB SHA-256
`c8f464e184f1903923462c5a0820f031d83d87f9ba9fb7f54ce67146e7303c1b`.

**Verdict:** INSPECT — expected null-visual pass.

**What to open:** full image enumeration per the desai template; confirm no text points at images.

**Expected ledger shape:** desai null-result template.

**Admission steps (Audit Gate v0.2):** (i) author `visual-evidence-ledger.yaml` from the real
inspection; (ii) fresh checkpoint; (iii) v0.2 record with 5-file snapshot in
`canon/audit/records/`; (iv) validator pass.

## 10. sontag-on-photography — priority 10

**Rank rationale:** cheap null-visual pass (verbal essays); admission additionally gated on the
critique-not-craft boundary ruling (decision (c)).

**File identity (as recorded):** `On Photography.epub`, 210,160 bytes, EPUB SHA-256
`edd6d37e3f765f5d2892a93c9f9069c0db4c0edf75a82a02b6fa15975298db57`.

**Verdict:** INSPECT — expected null-visual pass.

**What to open:** full image enumeration per the desai template.

**Expected ledger shape:** desai null-result template.

**Admission steps (Audit Gate v0.2):** (i) author `visual-evidence-ledger.yaml` from the real
inspection; (ii) fresh checkpoint; (iii) v0.2 record with 5-file snapshot in
`canon/audit/records/`; (iv) validator pass.

## 11. sullivan-hey-whipple — priority 11

**Rank rationale:** high value but the most expensive prose-heavy admission: 4 unread chapters, an
independence test, and 45 figures. Schedule after the cheap wins.

**File identity (as recorded):** `/Users/vaibhavchawla/Downloads/Books/Hey Whipple, Squeeze
This.epub`, 144,649,816 bytes, SHA-256
`b0a2630f368fb62c25f7f08d2135267e3ebe1e4165be253ce1056c391ec2095d` — the second brief-named
book-file hash; on-arrival hash must match.

**Verdict:** INSPECT.

**What to open:** the 45 distinct cited figures (33/70 objects name `figure_refs`); ALSO read
chapters 10, 13, 14 and 17 (never read — the extraction is partial but recorded as whole,
`partial_extraction_recorded_as_whole`); and run the `shared_primary_informant` test against
ogilvy-ch2 (an Ogilvy-published book is load-bearing across three chapters; under the Audit Gate
`independence_not_established` blocks promotion until resolved).

**Expected ledger shape:** full figure ledger (45 rows) + an extraction-scope statement naming the
read and unread chapters + the informant-test result.

**Admission steps (Audit Gate v0.2):** (i) author `visual-evidence-ledger.yaml` from the real
inspection; (ii) fresh checkpoint; (iii) v0.2 record with 5-file snapshot in
`canon/audit/records/`; (iv) validator pass.

## 12. ries-22-immutable-laws-branding — priority 12

**Rank rationale:** likely null-visual pass, but admission is blocked on Controller adjudication
against live binet-field-effectiveness-in-context-ch1 (opposed advice, deliberately unresolved —
decision (a)). Do not schedule the pass before the adjudication.

**File identity (as recorded):** `/Users/vaibhavchawla/Downloads/Books/The 22 Immutable Laws of
Branding.pdf`, 1,002,744 bytes, SHA-256
`9083461dc721ca4fff19b49aaf4d7ee76608162c2ee5a8ce741341761fc04ce2`, 257 PDF pages.

**Verdict:** INSPECT — likely null-visual pass (the edition adds "illustrations and text"; the pass
must confirm whether any illustration is load-bearing).

**What to open:** page-level scan for illustrations; open any found.

**Expected ledger shape:** desai null-result template, or small figure ledger if illustrations
prove load-bearing.

**Admission steps (Audit Gate v0.2):** (i) author `visual-evidence-ledger.yaml` from the real
inspection; (ii) fresh checkpoint; (iii) v0.2 record with 5-file snapshot in
`canon/audit/records/`; (iv) validator pass.

## 13. connor-irizarry-discussing-design — priority 13

**Rank rationale:** critique workflow (human_workflow consumer) — low weak-model runtime value;
figure pass is small.

**File identity (as recorded):** `/Users/vaibhavchawla/Downloads/Books/Discussing Design.pdf`,
205 PDF pages; NO hash recorded — hash-on-arrival plus the 5-locator sample are mandatory
(printed=PDF-18 offset is copy-specific).

**Verdict:** INSPECT.

**What to open:** Fig 5-3 (printed p.120) and Fig 5-4 (printed p.123), plus the rest of the 25
cited figures. Figures 2-1, 3-3, 3-5 and 3-6 were already rendered first-hand during extraction
(one changing `sk_disc_0024` in this candidate's `source-knowledge.yaml`) — decision (b) converts
those 4 into ledger rows.

**Expected ledger shape:** figure ledger over the 25 cited figures; 4 rows importable under
decision (b).

**Admission steps (Audit Gate v0.2):** (i) author `visual-evidence-ledger.yaml` from the real
inspection; (ii) fresh checkpoint; (iii) v0.2 record with 5-file snapshot in
`canon/audit/records/`; (iv) validator pass.

## 14. carroll-read-this-photographs — priority 14

**Rank rationale:** figure-heavy pass (every lesson is taught against one reproduced photograph);
moderate doctrine yield; whole book, images intact.

**File identity (as recorded):** `/Users/vaibhavchawla/Downloads/Books/Read This If You Want to
Take Great Photographs.epub`, 5,142,000 bytes, EPUB SHA-256
`c0a69021c14f2852c0235851ff7b45cf15676d25e6237144627f6e1936faa60a`.

**Verdict:** INSPECT.

**What to open:** the reproduced photograph behind each lesson; 14/30 objects carry
`figure_not_inspected`.

**Expected ledger shape:** per-lesson figure ledger (photograph identified, lesson-claim checked
against it).

**Admission steps (Audit Gate v0.2):** (i) author `visual-evidence-ledger.yaml` from the real
inspection; (ii) fresh checkpoint; (iii) v0.2 record with 5-file snapshot in
`canon/audit/records/`; (iv) validator pass.

## 15. ogilvy-beyond-ch2 — priority 15

**Rank rationale:** figure-heavy pass; scope extension of a live source (decision (d)); every
named-campaign claim currently rests on Sullivan-style say-so until the reproduced ads are opened.

**File identity (as recorded):** Controller-authorised read-only local copy of *Ogilvy on
Advertising* (EPUB); NO hash or size recorded — hash-on-arrival plus the 5-locator sample are
mandatory.

**Verdict:** INSPECT.

**What to open:** the reproduced advertisements across the print-craft / TV / direct-response /
research chapters.

**Expected ledger shape:** per-advertisement figure ledger tying each named-campaign claim to the
reproduction that carries it.

**Admission steps (Audit Gate v0.2):** (i) author `visual-evidence-ledger.yaml` from the real
inspection; (ii) fresh checkpoint; (iii) v0.2 record with 5-file snapshot in
`canon/audit/records/`; (iv) validator pass.

## 16. airey-logo-design-love — priority 16

**Rank rationale:** copy-replacement class — schedule last; nothing useful can run against the
current file.

**File identity (as recorded):** local PDF SHA-256
`bbd6e5e1292ebdb451b33b8abec80e7c2333bbe22538de4da790a0cebc7d5285`, 5,968,474 bytes, 217 PDF
pages. The copy is a degraded, unattributed Spanish machine translation: printed p.64 calls the
FAILED Tropicana redesign the successfully renamed identity (outcome inverted); all 45 ontology
terms `verbatim: false`; printed pp.99–100 missing.

**Verdict:** REPLACEMENT-COPY — the ENGLISH ORIGINAL of *Logo Design Love* is required. Do NOT
schedule a visual pass against the current file. 23 pages were already rendered first-hand with
`pdftoppm` during extraction (folios verified) — decision (b) preserves that as a partial record,
but admission still needs the English copy.

**What to open (on the replacement copy):** re-verify all 45 ontology terms verbatim; inspect the
logo/identity spreads printed pp.2–191; image pages 16/20/40/41/95/138/142/143; note the
pp.99–100 gap in the old copy.

**Expected ledger shape:** figure/spread ledger on the English copy + a term-verbatim re-check
table.

**Admission steps (Audit Gate v0.2):** (i) author `visual-evidence-ledger.yaml` from the real
inspection; (ii) fresh checkpoint; (iii) v0.2 record with 5-file snapshot in
`canon/audit/records/`; (iv) validator pass.

## 17. freeman-photographers-eye-beyond-parts1-3 — priority 17

**Rank rationale:** copy-replacement class — the calibre-converted PDF has converter-invented
pages and destroyed the designed spreads ("A different copy, not a better extraction, is what
fixes this" — `audit-assessment-HOLD.yaml`, `false_page_affordance`).

**File identity (as recorded):** converted PDF SHA-256
`a06d1dc36b12e5dddf4332cf8c7c97899dfc131a67bc76d7300065fdda527eaf`, 13,124,759 bytes.

**Verdict:** REPLACEMENT-COPY — an authored-page PDF or the physical book of *The Photographer's
Eye* is required. 16 converted-PDF pages were rendered first-hand during extraction (pp.83, 86,
92, …) — decision (b) preserves those rows; admission needs the paginated copy.

**What to open (on the replacement copy):** the designed spreads after converted-PDF p.70
(photograph + deconstruction + caption facing-page compositions); 29/55 objects carry
`figure_not_inspected`.

**Expected ledger shape:** spread-level ledger keyed to authored pages, not converter pages.

**Admission steps (Audit Gate v0.2):** (i) author `visual-evidence-ledger.yaml` from the real
inspection; (ii) fresh checkpoint; (iii) v0.2 record with 5-file snapshot in
`canon/audit/records/`; (iv) validator pass.

## 18. samara-breaking-the-grid-ch2 — priority 18

**Rank rationale:** copy-replacement class; the designed page IS the evidence
(`source_is_its_own_specimen` on the live counterpart) and the reflowable EPUB destroyed
page-as-argument.

**File identity (as recorded):** original `~/Downloads/Books/Making and Breaking the Grid_ A
Graphic Design Layout Workshop.epub`, 30,988,392 bytes (size only — no original hash; the recorded
SHA-256 `d52616e0eca30d5691a3c0acb0fef64281fedb6bfe489ca151d33f4d10def1fa` is of the processed
text). Hash-on-arrival plus the 5-locator sample are mandatory.

**Verdict:** REPLACEMENT-COPY — a PAGINATED copy (print or print-fidelity PDF) is required. Ch2
has 205 distinct figure references (counted in the EPUB's own `ch02.xhtml`), 0 inspected; 26/45
objects carry `figure_not_inspected`.

**What to open (on the replacement copy):** the ch2 case-study layouts as printed pages/spreads —
all 205 figure references resolve there.

**Expected ledger shape:** per-case-study spread ledger on the paginated copy.

**Admission steps (Audit Gate v0.2):** (i) author `visual-evidence-ledger.yaml` from the real
inspection; (ii) fresh checkpoint; (iii) v0.2 record with 5-file snapshot in
`canon/audit/records/`; (iv) validator pass.

---

## Recompute pointers

- 18 HOLD dirs: `ls -d canon/candidates/canon-014/*/ | wc -l` (18; two non-dir files sit beside
  them: `CROSS-SOURCE-RELATIONSHIPS.yaml`, `SOURCE-ACCESS-AND-STATUS.csv`).
- 839 objects: python sum over `source_knowledge` lengths, per the head of this file.
- 17 `candidate_hold_assessment` + 1 v0.2-shaped desai record:
  `grep -l 'assessment_kind: candidate_hold_assessment' canon/candidates/canon-014/*/audit-assessment-HOLD.yaml | wc -l`.
- Per-source figure lists: each candidate's `EXTRACTION-NOTES.md` (LSM §3 for the 54/129
  first-hand record; connor for the 4 rendered figures; w3c for the 48-figure assessment).
- Hash coverage: `grep -H 'MD5\|SHA-256\|sha256' canon/candidates/canon-014/*/PROVENANCE.md`.
