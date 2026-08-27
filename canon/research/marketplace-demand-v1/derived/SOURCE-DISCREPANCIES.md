# Source discrepancies — cleaned Fiverr report vs raw Fiverr capture

**Task:** CANON-011 · **Date:** 27 Aug 2026 · **Status:** recorded, not reconciled

The provenance README for this research says that if a cleaned report and the raw capture
disagree, the discrepancy must be recorded and not silently resolved. Four disagreements were
found. None of them is load-bearing for any case in the brief bank, because no Fiverr material
is used as customer intent anywhere — but they are recorded here so that anyone who later reaches
for a Fiverr number knows which ones are contested.

**Files compared**

- cleaned: `canon/research/marketplace-demand-v1/sources/fiverr-ai-video-demand-2026-08-26.md`
- raw: `canon/research/marketplace-demand-v1/sources/fiverr-raw-capture-2026-08-26.txt`

---

## D-1 · The rupee-to-dollar rate differs by 14%

**Cleaned report, header:**
> Fiverr's displayed conversion is almost exactly ₹100 = US$1 (₹501 = $5, ₹1,001 = $10, ₹5,001 = $50)

**Raw capture, header:**
> Fiverr rate ≈ ₹100 ≈ US$1.14, i.e. ₹1,001 ≈ $11, ₹4,501 ≈ $50

**What it means in practice.** Every dollar figure in the cleaned Fiverr price tables is derived
from one of these two rates, and they disagree by about 14%. A ₹9,001 package is either $90 or
about $103 depending on which is right. Neither file says where its rate came from.

**Not resolved.** Both are recorded. Nothing in this task depends on a Fiverr price, so no choice
was needed — but any future use of a Fiverr dollar figure should treat it as carrying a 14% band
rather than as a number.

---

## D-2 · One gig title and its AI/human classification are attributed to two different sellers

**Raw capture,** in the `"hindi video ad"` search listing:
> 10 /dsbohra — "I will create hindi and hinglish ai ugc video ads" — AI

**Cleaned report,** appendix row H5:
> I will create hindi ugc video ads for indian brands and startups | Sonu Bohra (dsbohra) | "UGC Creator" | ... | human creator, not AI

**And separately,** cleaned report row H2 gives the title the raw capture attached to `dsbohra` to a
different seller entirely:
> I will create hindi and hinglish ai ugc video ads | Anuranjan Toppo

**What it means in practice.** The raw capture and the cleaned report disagree about both what
seller `dsbohra` is selling and whether it is AI-generated or a human creator. This matters for
exactly one claim in the cleaned report — that there are **four** credible AI Hindi/Hinglish gigs
on Fiverr and that human Hindi creators are the ones with traction. If `dsbohra` is an AI gig, that
count is five and one more of them has a rating; if it is a human creator, the cleaned report is
right.

**Not resolved.** The count is not used anywhere in the brief bank. It is used in the coverage
report only as a directional statement — that the Fiverr Hindi AI supply is very thin — which
holds either way.

---

## D-3 · Two gig titles differ between the search listing and the gig page

**Raw capture,** `"ai ugc ad"` listing, item 9, with the capturer's own note:
> Haris Younus /harris_younus (title in listing: "I will create ai ugc ads, ai ugc video ads, and ai product ads")

**Cleaned report,** row G23, from the gig page:
> I will do ai ugc video ads, ai ugc ads, ai ugc, ugc testimonials, ai ugc reviews

The same pattern appears for `sahir1422`, where the raw capture marks its own listing title with a
question mark and the cleaned report gives a different one from the gig page.

**What it means in practice.** Probably not a real conflict — Fiverr shows shortened or
A/B-tested titles in search results — and the capturer flagged it themselves. Recorded because
title text is the evidence behind the cleaned report's section on keyword patterns, and that
section would be measuring the wrong strings if listing titles and gig titles are being mixed.

**Not resolved.** No case depends on it.

---

## D-4 · A seller's review count is present in one file and absent in the other

**Raw capture,** H2:
> No level badge (new seller), 4.0 seller rating, review count not displayed (≈0–1)

**Cleaned report,** §3 table:
> **0–1** (4.0 seller rating, no count)

These agree. The discrepancy is with the cleaned report's own coverage caveat, which lists this
seller among those it treats as 0–1 reviews while also stating the count was not capturable. That
is an internal softness rather than a conflict between the two files, and it is recorded only so
that "0–1 reviews" is read as an estimate, which is what both files actually say.

---

## What none of these change

No case in `marketplace-brief-bank-v1.yaml` uses a Fiverr price, a Fiverr review count, a Fiverr
seller title or a Fiverr AI/human classification as a customer requirement, an acceptance
condition or a fixture value. The five Fiverr conventions recorded in the bank
(`fiverr_convention_inputs`) are structural — the three-tier length ladder, the standard buyer
intake list, pronunciation guidance as an intake field, catalogue volume tiers, and the recorded
complaint about AI footage delivered where real footage was expected. Each is quoted verbatim from
the cleaned report and checked mechanically by the validator, and none of the four discrepancies
above touches any of them.
