# Marketplace Demand v1 — Source Provenance

**Added:** 27 Aug 2026  
**Origin:** user-supplied research conducted 26 Aug 2026  
**Use:** internal research / benchmark-brief preparation

## Source files

1. `sources/upwork-ai-video-demand-2026-08-26.md`
   - logged-in, read-only Upwork job-market research;
   - 11 search queries;
   - 114 unique job postings recorded;
   - 4 detail pages opened;
   - no proposals/messages/account mutations.

2. `sources/fiverr-ai-video-demand-2026-08-26.md`
   - logged-in, read-only Fiverr demand/competition sweep;
   - 10 listing/category pages;
   - 42 gig pages;
   - no purchases/messages/account mutations.

3. `sources/fiverr-raw-capture-2026-08-26.txt`
   - raw capture notes underlying the Fiverr sweep;
   - retained as provenance, not treated as more authoritative than the cleaned report.

## Evidence hierarchy for derived work

For marketplace-derived benchmark preparation:

1. exact individual buyer-job facts in the Upwork report/capture;
2. cleaned Upwork report interpretations;
3. cleaned Fiverr report for seller/package/input conventions;
4. Fiverr raw capture notes as supporting provenance.

If a cleaned report and raw capture disagree, record the discrepancy. Do not silently choose one.

## Interpretation boundary

- Upwork buyer jobs may be used as **customer-intent source briefs**.
- Fiverr seller gigs are **not customer briefs**. They may inform commercial packaging, typical
  buyer inputs, delivery formats, and market conventions, but must not be rewritten as though a
  customer requested those fields.
- Estimates of market size/volume are research estimates from the supplied sweep, not universal
  market-share facts.
- Derived benchmark cases must preserve source lineage and distinguish:
  - customer stated;
  - customer implied;
  - experiment-supplied fixture;
  - system-derived / benchmark decision.

Do not publish or redistribute marketplace content without a separate rights review.
