# Provenance record — Google, "ABCDs of effective video ads" (experimental lane 4)

**EXPERIMENTAL — NOT LIVE CANON.** Nothing in this directory is accepted Canon, and nothing here
may be described as accepted. This is exploratory, non-merge extraction work.

**source_id:** `google-abcd-video-ads` · **ID prefix:** `abcd` · **Retrieved:** 30 August 2026

## Source identity

Google's own published guidance on the "ABCDs of effective video ads" — Attention, Branding,
Connection, Direction — read across three Google-owned pages. This is a live web publication, not
a book: it has no edition, no ISBN and **no page numbers**, and it can change without notice.

| # | Page | URL | Page's own date | Byline |
|---|---|---|---|---|
| P1 | Google for Business resources, "ABCDs of effective video ads" | `https://business.google.com/us/resources/articles/abcds-of-effective-video-ads/` | May 2023 | none |
| P2 | Think with Google, "Understanding the ABCDs of effective creative on YouTube" | `https://business.google.com/us/think/future-of-marketing/youtube-video-ad-creative/` | April 2022, "2 min read" | Ariane Le Port, Global Creative Effectiveness Lead, Creative Works, Google |
| P3 | Google Ads Help, "About the ABCDs of effective video ads" | `https://support.google.com/google-ads/answer/14783551` | undated; page footer `©2026 Google` | none |

The task named P2 by its listing title, "YouTube ABCDs: Video ad best practices". That is the
page's `<title>`; its on-page headline is "Understanding the ABCDs of effective creative on
YouTube". Locators in this extraction use the on-page headline, because that is what a reader
checking the citation will see.

## Material available, and its span

All three pages in full, converted to text, at
`scratchpad/src/SRC-google-abcd.txt` — 4,816 lines, 31,262 bytes,
SHA-256 `df27a00fa974cf2369e8c4d5a6ef51f5a2b0b88c85d89947402beabeb35d85e4`.

The dump carries a great deal of navigation chrome, account/consent dialogue text, footer link
lists and language pickers. None of it was extracted. The substantive guidance is small: roughly
1,100 words across the three pages once the chrome is removed. **This is a thin source and the
extraction is sized to it.**

One page was re-fetched during extraction, with
`curl -sSL -A "Mozilla/5.0" https://support.google.com/google-ads/answer/14783551`, for one
reason: the text dump linearises P3's two HTML tables and destroys the cell-to-column binding. The
re-fetch was used to read the table markup and nothing else; the live page matched the dump
verbatim on every string checked. See "Table linearisation" below.

## Locator convention — no page numbers exist

Every `provenance` block sets `page_start: null` and `page_end: null`. The real locator is in
`section` and names the page plus the section heading, and for the objective matrix the table row:

- `Google Ads Help, "About the ABCDs of effective video ads", section "Core ABCDs", row "Attention"`
- `Google Ads Help, section "ABCDs by marketing objectives", table row "Awareness: Get noticed"`
- `Think with Google, "Understanding the ABCDs of effective creative on YouTube", section "B = Branding: Brand early, often, and richly"`
- `Google for Business resources, "ABCDs of effective video ads", section "A – Attention", sub-heading "Jump in"`

**No page number is invented anywhere in this lane.** Every section heading cited in
`qa-bank.yaml` was checked against the source dump; all resolve.

## Access basis

**Publisher-authorised, openly published, free.** No paywall, no authentication, no login. All
three pages are Google's own properties, served publicly.

**A Scribd reupload of a Google "ABCD reference guide" exists and was deliberately NOT used**, and
was not visited. It is a third-party reupload, and it is not the publisher's route. Where content
appeared to exist only on a non-Google host it was recorded as unavailable rather than sought:
specifically, P2 links to a downloadable "ABCDs Playbook" for the objective-driven variants, and
that playbook is **not part of this extraction**. Whatever detail it holds about the
objective-specific ABCDs is unavailable here, and nothing in this extraction should be read as
covering it. The four objective rows extracted come from P3's published table.

Nothing copyrighted is reproduced at length. Source terminology is quoted where the exact wording
carries the point — most often where two Google pages word the same thing differently.

## Overlap with live Canon

**None.** This source is independent of every source in `canon/knowledge/current/`.

The live corpus's newest source is 2013 and every moving-image source in it — *Grammar of the
Shot*, *Grammar of the Edit*, *Master Shots*, *In the Blink of an Eye*, *The Conversations*,
*Painting with Light*, *Light: Science & Magic* — is about film. Nothing in live Canon addresses
opening seconds of an ad, sound-off versus sound-on viewing, feed or platform placement, or
platform-specific ad products. There is no shared author, series, publisher or primary informant
with any live source.

There is a **structural** resemblance to `binet-field-effectiveness-in-context-ch1`, and it is a
resemblance of hazard rather than of content: both sources carry a declared commercial interest of
the publisher in the finding. That resemblance is why this record follows Binet's precedent of
stating the evidence base as the source describes it. **It is not a content overlap and no
cross-source relation is asserted anywhere in this lane** — cross-source promotion is forbidden
in this task, no `xs_` concept is created, and no relationship references another lane's
identifiers.

## Declared publisher interest — stated plainly

**The publisher sells advertising on the platform whose creative guidance this is, and whose
effectiveness the cited research validates.** Google publishes the ABCDs; Google sells YouTube ad
inventory; the research showing the ABCDs lift sales likelihood and brand contribution is
Google-commissioned and Google-reported. Advertisers persuaded by this guidance buy the
publisher's product.

The source itself discloses third-party involvement, and that involvement **moderates the interest
without removing it**:

- **Ipsos** is named as the research partner in the collaboration that produced the principles.
- **Nielsen** and **Kantar** are named as "two independent reviewers".
- The effectiveness study is credited to **Google/Kantar**.

Three limits on how much comfort that gives, all readable off the source:

1. The independent-reviewer language describes how the *framework* was arrived at (P2, opening
   paragraph). It is not offered as verification of the 30%/17% figures, which are separately
   sourced to a Google/Kantar study.
2. The source never says what the reviewers reviewed, or what they concluded.
3. The Google/Kantar study is **named but not published**: no method, no comparison baseline, no
   definition of either outcome measure, no dispersion, and no link.

This caution is carried in `caveats` on **every one of the 26 SourceKnowledge objects**, in the
`applicability.limits` of every operational binding, and in a dedicated governance binding
(`bnd_abcd_008`, consumer `evidence_interpretation`).

## Evidence base, as the source describes it

- **Framework derivation** (P2): "a collaboration with Ipsos, and the involvement of two
  independent reviewers, Nielsen and Kantar", pursuing what ads that drive results on YouTube have
  in common. What emerged is described as principles "demonstrated across video ads that worked
  effectively for brands" — selection on the outcome, as the source itself describes it, with no
  comparison against ads that did not work, no sample size, no market coverage and no selection
  rule.
- **Effectiveness study**: "The Short & the Long of ABCDs Effectiveness", Google/Kantar, Global,
  April 2021. **n = 11,000 ads is stated on P1 only.**
- **A third, separate citation**: P2 attributes to **NCSolutions** the proposition that creative —
  concept through execution — is the No. 1 driver of campaign effectiveness and ROI. No study
  name, date, sample or method is given for it.
- **Whether the two Google exercises are the same study is not stated.** The n=11,000 sample is
  attached to the Kantar effectiveness study, not to the Ipsos framework-derivation work, and the
  source never says the two are one exercise. This extraction does not merge them.

### The figure discrepancy, recorded and not resolved

The same finding is stated three ways on three Google pages:

| Page | Phrasing | Statistic implied | Citation detail given |
|---|---|---|---|
| P3 Google Ads Help | "Deliver **as much as** a 30% lift in short-term sales likelihood and a 17% lift in long-term brand contribution" | an upper bound | study, publisher, "Global", "Apr 2021"; **no n** |
| P2 Think with Google | "**On average**, the ABCDs deliver a 30% lift in short-term sales likelihood and a 17% lift in long-term brand contribution" | a central tendency | "Google/Kantar **Link AI**, Global, The Short and the Long of ABCDs Effectiveness, **2021**"; no month, **no n** |
| P1 resources article | "30% lift in short-term sales likelihood" / "17% lift in long-term brand contribution" as bare callouts, **no qualifier**, above a footer reading "Actual results will vary by advertiser" | unspecified | study, publisher, "Global", "Apr 2021", **"n=11,000 ads"** |

An upper bound and an average are different statistics. **Nothing on any page resolves which is
correct, and this extraction does not resolve it — it reports it.** It is recorded as caveats on
`sk_abcd_0003`, as the subject of governance binding `bnd_abcd_008`, and in three Q&A items
(`qa_abcd_0001`, `qa_abcd_0002`, `qa_abcd_0026`).

## Platform and time contingency

This is guidance about **one company's ad products, on one platform, under one set of playback
behaviours, at one time**. It is not a durable mechanism claim and the source does not present it
as one. Every SourceKnowledge object carries `historical_claim` in
`evidence.characteristics` and a platform-contingency caveat, and governance binding
`bnd_abcd_009` (consumer `rule_application`) constrains application outside YouTube video
advertising.

The sharpest instance is `sk_abcd_0014`. The source asserts that **"YouTube is almost entirely a
sound-on experience"** — a platform-behaviour claim about one platform at one time, made once, on
P2 only, with no measurement attached. It is **emphatically not** a general claim about short-form
video, and it points the opposite way from the sound-off default common on other feed surfaces. It
is extracted faithfully as a claim about YouTube, flagged as contingent, and **not generalised**.
Several guidelines on the other two pages depend on it without restating it, and those dependencies
are recorded as ours, not the source's.

## Representation and integrity

A plain-text conversion of three live HTML pages. No OCR, no scan, no figures. Every claim is
text-supported: `source_support: text` on every object, `inspected.figures: []` throughout, and no
object carries `visually_demonstrated`.

**Table linearisation is the one real representation loss, and it was repaired rather than
guessed.** P3 carries two tables. The text dump flattens both, and for the four-row objective
matrix that destroys which instruction belongs to which principle column. Two rows — awareness and
consideration — carry **two bullets in a single Connection cell**, so a reading-order reconstruction
sees five instructions for four columns and has no signal that anything is uncertain. This is the
same failure shape the live Canon's Binet record describes for charts: values survive, bindings do
not.

The page was therefore re-fetched and the table markup read directly. The resulting mapping is
recorded in `sk_abcd_0023`–`sk_abcd_0026`, and `scs_abcd_002` carries
`extraction_uncertainty: inferred_from_layout` with an explanation of how the mapping was
resolved. Every cell string used was afterwards verified verbatim against both the fetched table
and the dump.

No figure carries essential meaning that the text alone does not, so the caution name
`figure_semantic_binding_lost` does **not** apply to this source.

## Volatility

This is a live web page. It can change under this record. The retrieval date (30 August 2026), the
per-page dates, the dump's byte count and its SHA-256 are recorded above so that a later reader can
tell whether the source has moved. No claim here should be relied on without re-checking the pages.

## Counts

**26 SourceKnowledge objects · 2 SourceConceptSystems · 28 ontology terms · 32 relationships ·
4 concepts (2 source-specific, 2 canonical, 0 cross-source) · 9 operational bindings ·
26 Q&A items, 10 of them `requires_application: true` (38.5%).**

No `creative_ir` binding and no `production` binding is proposed. Nothing in this lane infers any
generative model capability, and no remedy term carries `executable_by: generative_respecification`.
