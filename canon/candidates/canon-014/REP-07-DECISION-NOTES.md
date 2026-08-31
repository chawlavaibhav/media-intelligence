# REP-07 — Controller decision notes

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
`coordination/CONTROL-STATE.md` governs. This file records Controller answers relayed to the
REP-07 executor session, verbatim or near-verbatim, so each ruling used by an inspection pass is
traceable. Rulings referenced: INSPECTION-RUNBOOK.md "Controller decisions this runbook depends
on" items (a)–(e).

---

## DN-01 · 2026-08-31 · Prior-work recovery check (not a ruling)

**Question put to the Controller:** does any completed REP-07 inspection work already exist
outside the visible GitHub branches (ledgers, v0.2 records, extraction-time renders/contact
sheets, pinned W3C/Google snapshots, replacement copies, or inspection transcripts)?

**Controller answer (recorded verbatim in substance):** No recoverable hidden REP-07 inspection
work exists for the remaining 17 sources. Specifically: (1) no visual-evidence-ledger.yaml, not
even draft/partial, for any candidate other than desai; (2) no HOLD-source Audit Gate v0.2
records with 5-file snapshots beyond the known desai parked assessment; (3) no surviving
extraction-time renders/contact sheets (LSM-beyond's 9 sheets / 54 figures; connor's 4 figures;
airey's 23 rendered pages; freeman's 16 rendered pages) — only the committed prose records
survive; (4) no pinned WCAG 2.2 or Google ABCD snapshots; (5) no replacement copies (English
Logo Design Love, paginated Photographer's Eye, paginated Making and Breaking the Grid, clean
HarperCollins Mother Pious Lady); (6) no unpushed branch, local-only commit, or session
transcript of REP-07 work. One adjacent asset: a copy of Discussing Design.pdf (17,219,889
bytes) in the Controller's persistent library, not hash-certified by the Controller at answer
time; the executor's local copy of the same byte size was hashed on arrival instead
(sha256 b731d78811ce7d167c7ef61618d0069e7a1ed02eed0f6fea8c73b7caf2e5687b).

**Consequence applied:** the executor's inventory is authoritative. Desai's existing ledger is
preserved untouched; every other pass starts from zero, except that extraction-time first-hand
records (LSM 54 figs, connor 4 figs, airey 23 pp, freeman 16 pp) may be imported as ledger rows
only if ruling (b) later permits.

---

## DN-02 · 2026-09-01 · Ruling (e) — network re-fetch authorisation

**Question put to the Controller:** authorise the two zero-cost network re-fetches —
`https://www.w3.org/TR/WCAG22/` (+ cited Understanding docs, W3C Document Licence) and the 3
official Google ABCD pages — so both living artifacts can be re-fetched, SHA-256-pinned,
screenshotted, and inspected against the extracted claims?

**Controller answer:** "Authorise both." Both fetches are authorised.

**Consequence applied:** RE-FETCH-AND-PIN passes for google-abcd-video-ads and
w3c-wcag22-text-legibility are scheduled. Fetches are limited to the URLs recorded in each
candidate's PROVENANCE.md (plus the cited Understanding documents for WCAG). No other network
access is authorised by this ruling.

---

## DN-03 · 2026-09-01 · Ruling (b) — ledger-from-extraction-inspection

**Question put to the Controller:** may a visual-evidence-ledger incorporate rows authored from an
extraction run's own contemporaneous first-hand figure-inspection record (LSM-beyond 54 figures,
connor 4 figures, airey 23 pages, freeman 16 pages), with each imported row marked as
extraction-time evidence?

**Controller answer:** "Yes, import marked rows." Extraction-time first-hand rows enter the
ledger explicitly marked as such; fresh inspection covers the rest.

**Consequence applied:** ledgers for lsm-beyond (54 rows) and connor (4 rows) import the
committed extraction-time record with an explicit `evidence_time: extraction_pass` (or
equivalent) marking on every imported row; airey's 23 pages and freeman's 16 pages are preserved
as partial records but their sources remain REPLACEMENT-COPY blocked regardless.

---

## DN-04 · 2026-09-01 · Ruling (d) — scope-extension admission convention

**Question put to the Controller:** confirm the scope-extension admission convention
(hopkins-ch8-21, lsm-beyond-ch3, ogilvy-beyond-ch2, samara-ch2, freeman-beyond-parts1-3 enter
only as explicitly scoped extensions of their live counterparts, never as independent origins)?

**Controller answer:** "Defer."

**Consequence applied:** inspection passes for those candidates still run; no admission language
asserting the convention is written into any record. Each affected record states the dependence
facts (shared authorship with the live counterpart, via lineage relations) — which v0.2 requires
anyway — but the scoped-extension admission marking waits for a later Controller memo.

---

## DN-05 · 2026-09-01 · Ruling (a) — ries-22-immutable-laws vs binet-field

**Question put to the Controller:** ries-22-immutable-laws gives advice opposed to the live
accepted binet-field-effectiveness-in-context-ch1 (deliberately unresolved; the runbook forbids
scheduling the ries pass before adjudication). How do you rule?

**Controller answer:** "Rule for Binet — retire ries." Binet & Field's evidence-based position
prevails; ries is not admitted and no pass runs.

**Consequence applied:** the ries-22-immutable-laws-branding inspection pass is NOT scheduled and
will not be. The candidate stays under `canon/candidates/canon-014/` as source evidence with its
HOLD assessment; it is never put to the Audit Gate. Formal retirement paperwork (disposition of
the candidate dir) is an admission-time/Writer task, not this executor's.

---

## Open rulings awaited (runbook items)

- (c) platform-contingent (google-abcd) / critique-not-craft (sontag) admission boundary —
  inspection passes may still run; admission language waits.
- (d) scope-extension admission convention — DEFERRED per DN-04; passes run, admission language
  waits.
