# REP-07 — execution summary

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
`coordination/CONTROL-STATE.md` governs. Executed 2026-09-01 on branch
`work/rep-07-hold-inspections` per `INSPECTION-RUNBOOK.md`, under the Controller rulings
recorded in `REP-07-DECISION-NOTES.md` (DN-01..DN-05).

## What was executed

13 of the 18 HOLD candidates received their full inspection pass: hash-on-arrival, locator
sample where mandatory, the real figure/scan/null/re-fetch inspection, a
`visual-evidence-ledger.yaml`, and an Audit Gate v0.2 record authored IN THE CANDIDATE DIR
(never in `canon/audit/records/` — admission stays with the Controller). Every record passes
`validate_candidate_audit_record.py` (per-record rules identical to the adopted validator) and
the repo-wide `validate_audit_gate_v02.py` stays at 0 errors throughout. One commit per
ledger and one per record, in runbook priority order.

| # | Candidate | Pass | Headline result |
|---|---|---|---|
| 1 | google-abcd-video-ads | RE-FETCH-AND-PIN (DN-02) | 3 pages byte-pinned + screenshots; 26/26 claims match; figure discrepancy and table bindings stand exactly as recorded; figures illustrative only |
| 2 | w3c-wcag22-text-legibility | RE-FETCH-AND-PIN (DN-02) | Pinned the 12 Dec 2024 Recommendation + 7 Understanding docs; 39/39 objects verify incl. every numeric criterion; 53 figures enumerated, all image-backed figures + Figures 8-14 opened |
| 3 | light-science-magic-beyond-ch3 | INSPECT | 5-locator sample passes; 76 fresh figures opened + 53 extraction-time rows imported (DN-03); all 129 cited figures now inspected; no claim changed |
| 5 | berger-contagious | INSPECT (expected null) | Null did NOT hold: five in-body images incl. two prose-cited charts — all illustrative, no claim depends on any; brief-named MD5 matches |
| 6 | hopkins-scientific-advertising-ch8-21 | INSPECT (scan pass) | All 40 printed pp.25-64 opened (printed=PDF-8); zero figures, confirming source_evidence_never_printed; garbled folios are text-layer only |
| 7 | hopkins-my-life-in-advertising | INSPECT (scan pass) | Folio continuity mechanical over all 206 pp.; 66 pages opened; the p.134 "unrecoverable" OCR loss is legible in the page image — reclassified recovered |
| 8 | kahneman-sibony-sunstein-noise | INSPECT | All 19 numbered figures opened (not just 16/18); nine figure_not_inspected resolved; figure inventory corrected to 1-19 |
| 9 | godin-this-is-marketing | INSPECT (expected null) | Null did NOT hold: sixteen real figures — all semantically stated in prose; extraction unaffected; one documentation gap recorded and closed |
| 10 | sontag-on-photography | INSPECT (null) | Null held exactly: no photograph anywhere in the archive; ruling (c) left open, record asserts nothing about admissibility |
| 11 | sullivan-hey-whipple | INSPECT | Brief-named SHA-256 matches; 45/45 figures opened; chapters 10/13/14/17 read in full (bounding partial_extraction_recorded_as_whole); informant test resolved: cites_source, NOT shared_primary_informant |
| 13 | connor-irizarry-discussing-design | INSPECT | 25/25 figures opened fresh; printed=PDF-18 verified on the runbook's named locators; figures illustrative only |
| 14 | carroll-read-this-photographs | INSPECT | 30/30 lessons checked against opened photographs; 14 figure_not_inspected discharged; print-page filename mapping recovered the "unrecoverable" exercise and the focal-length table |
| 15 | ogilvy-beyond-ch2 | INSPECT | CENTRAL FINDING: the recorded "reproductions absent, 39 placeholders" loss is a text-dump artifact — the copy carries all reproductions inline (115 opened); announced_loss_placeholder reclassified recovered_in_this_copy |

## Not executed, and why

| Candidate | Reason |
|---|---|
| desai-mother-pious-lady (4) | CLEAN-COPY-DIFF requires an independent HarperCollins copy; none exists (DN-01). Existing ledger + parked v0.2-shaped assessment preserved untouched (naming regularisation deferred to its touch). |
| ries-22-immutable-laws-branding (12) | Controller ruled for Binet (DN-05): ries is retired; no pass runs. Candidate stays as source evidence; retirement paperwork is admission-time. |
| airey-logo-design-love (16) | REPLACEMENT-COPY (English original) not available (DN-01). |
| freeman-photographers-eye-beyond-parts1-3 (17) | REPLACEMENT-COPY (paginated) not available (DN-01). |
| samara-breaking-the-grid-ch2 (18) | REPLACEMENT-COPY (paginated) not available (DN-01). |

## Admission-time items the Controller should note

1. Ruling (c) (platform-contingent / critique-not-craft boundary) is still open; the
   google-abcd and sontag records state the facts and assert nothing about admissibility.
2. Ruling (d) is deferred (DN-04); the five scope-extension records carry lineage dependence
   facts only.
3. Cross-record symmetry: the candidate records for the three same-work extensions declare
   `shared_author` toward live records (light_science_and_magic_ch3,
   hopkins_scientific_advertising_ch1_7, ogilvy_on_advertising_ch2) which cannot declare back
   until a Writer-authorised session updates them at admission — the candidate validator
   reports these as INFO, not failures.
4. Two ledgers qualify existing audit bookkeeping (ogilvy-beyond's placeholder
   reclassification also bears on a note in the live ch-2 audit; noise's figure inventory
   correction) — recorded in ledgers only; no frozen file and no file outside the candidate
   dirs was edited.
5. After any admission that changes the accepted set, REP-05's compiled-pack validator must be
   re-run per the REP-07 acceptance checks (pack digests recompile if the accepted digest
   changes).
