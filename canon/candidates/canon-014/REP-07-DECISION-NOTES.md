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

## DN-06 — Admission batch authorised; rulings (c) and (d) resolved — 2026-09-01

**Question put to the Controller:** the 13 completed inspection passes are independently
re-verified (repo-wide Audit Gate 0 errors; 13/13 candidate records 0 errors, PR #85).
Proceed to admission? And ruling (c): how do google-abcd-video-ads (platform-contingent
official guidance) and sontag-on-photography (critique, not production technique) enter?

**Controller answer (verbatim, session `session_01MTzh8gGKkyN31UruDXHcZo`):** "I am good.
Proceed. Continue from where you left off." — and, on ruling (c): **"Admit both, marked"** —
both enter accepted Canon carrying explicit markers: google-abcd as platform-contingent/dated
guidance, sontag as critique context, never production doctrine; markers must keep compiled
packs honest about what each is.

**Consequences applied:**
1. All 13 inspected candidates are admitted into `canon/knowledge/current/`, records promoted
   into `canon/audit/records/` with digests recomputed; the repo-wide validator stays at 0
   errors throughout.
2. Ruling (c): the google-abcd and sontag records carry explicit `admission_conditions`
   (platform_contingent / critique_context) that downstream compilation must surface.
3. Ruling (d), resolved per the standing recommendation: the same-work extensions
   (hopkins-ch8-21, lsm-beyond-ch3, ogilvy-beyond-ch2) enter as explicitly scoped extensions
   of their live sources, never as independent origins; two-sided lineage declarations are
   written on the live records at admission.
4. Ries retirement paperwork per DN-05: marked retired, retained as source evidence only.
5. Post-admission rebuilds per the REP-07 acceptance checks: corpus index/fingerprints,
   coverage layer extended with authored assignments for the 13 sources, marker map, and the
   compiled pilot packs recompiled (LSM coverage caveat updated to accepted status).

**Not authorised:** spend; Registry rows; Production IR/Planner; changes to frozen historical
artifacts; admission of desai/airey/freeman-beyond/samara-ch2 (still blocked) or ries
(retired); adoption of the still-PROPOSED tranche-A artifacts beyond what admission
mechanically requires.

**Note on recording location:** this ruling belongs in `coordination/decisions/` by repo
convention; this session's permission policy blocks workers from writing there, so it is
recorded here (the REP-07 rulings file) for the Controller to promote at merge.

---

## DN-07 · 2026-09-01 · EVAL-038 approved, EXTENDED TO MEDIA GENERATION — spend authority

**Context:** the Controller instructed a continuation session to pull
`claude/canon-context-guidance-ohi1i9` (PR #83), read this file through DN-06,
`canon/findings/PROPOSED-EVAL-038-SUBSTITUTION-DESIGN.md`,
`canon/compilation/INJECTION-CONTRACT-v0.md`, and the merged EVAL-035 / PILOT-001 generation
machinery and its spend conventions, then execute. This note records the approval verbatim
before any paid call, as instructed.

**Controller approval (verbatim):**

> I am the Controller. I approve EVAL-038 EXTENDED TO MEDIA GENERATION with a
> HARD max consumed API spend of USD 10.00 total, 0 retries, execution-time
> route/price verification before every paid call, keys from this machine.
> Record this approval verbatim as DN-07 in the REP-07 decision-notes file
> before any paid call. Media generation here is product learning — not
> Capability Registry evidence.

**Execution directives (verbatim):**

> Execute on a new branch off claude/canon-context-guidance-ohi1i9:
> 1. USD-0 retro-test from the EVAL-038 design (replay my two rejected
>    PILOT-001 candidates against the compiled packs).
> 2. Reasoning arms over ALL SIX EVAL-037 briefs — image and video both:
>    Haiku+packs x2 reps, unconditional injection per the injection contract;
>    then pin Gemma's official price (bytes+date, snapshot pattern — network
>    fetch authorised) and run Gemma+packs with remaining reasoning budget.
>    Baseline = the committed Sonnet NO_CANON packages; never re-run Sonnet.
> 3. Generation: for B06 (image) and B01 (video), execute BOTH the best
>    Haiku+packs package and the committed Sonnet NO_CANON package into real
>    media — 2 images + 2 videos — using the cheapest verified route.
> 4. Seal everything as committed bytes per the repo's sealed-evidence
>    conventions (EVAL-024 pattern), push, and hand me the blinded judging
>    protocol: I judge packages and media; models never judge themselves.
>
> Stop at the cap without exception; if video pricing makes step 3 exceed
> remaining budget, generate the image pair, report the exact video quote,
> and stop for my approval rather than guessing.

**Machine-readable authority (EVAL-038 extended):**

```yaml
machine_authorisation:
  tranche_id: EVAL-038-MEDIA-EXT
  authorised: true
  max_consumed_api_spend_usd: "10.00"
  retries_authorised: 0
  execution_time_route_price_verification: required_before_every_paid_call
  approved_by: "Vaibhav Chawla (Controller)"
  approved_at: "2026-09-01"
  scope:
    - haiku-plus-packs reasoning trials, 6 briefs x 2 reps, unconditional injection
    - gemma-plus-packs reasoning trials, contingent on a pinned official price snapshot
    - media generation for B06 (image pair) and B01 (video pair), best haiku+packs
      package vs committed sonnet NO_CANON package, cheapest verified route
  comparators_reused_usd0: committed Sonnet NO_CANON packages (never re-run)
  media_generation_role: product learning only — NOT Capability Registry evidence
  overrides:
    - EVAL-038 design 3-rep default -> 2 reps (Controller directive)
    - EVAL-038 design USD 1.00 reasoning ceiling -> subsumed under the USD 10.00 total cap
  stop_rule: hard stop at USD 10.00; if the video pair cannot fit remaining budget,
    generate the image pair, report the exact video quote, stop for approval
```

**Consequence applied:** DN-07 is recorded and committed before any paid call. All spend under
this authority is recorded per call as committed bytes; the PILOT-001 closure's "no further
PILOT-001 provider call" stands — media generation here runs under this NEW authority against
EVAL-037/EVAL-038 packages, not as a PILOT-001 attempt.

**Note on recording location:** as with DN-06, repo convention places rulings in
`coordination/decisions/`; the worker permission policy blocks writes there, so it is recorded
here for the Controller to promote at merge.

---

## Open rulings awaited (runbook items)

- ~~(c)~~ RESOLVED by DN-06.
- ~~(d)~~ RESOLVED by DN-06.
