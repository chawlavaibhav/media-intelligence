# Rights, acquisition routes and gates

**Task:** R4-F · **Date:** 26 Aug 2026 · **Branch:** `work/res-004-production-readiness`
**NO ACQUISITION OCCURRED. No download, login, account, form, terms acceptance, payment or email. ₹0 / $0.**

---

## The binding rule from the Controller

> **CC-BY-NC material is not authorised as commercial-project empirical material without explicit
> Controller/legal disposition.**
> Published aggregate findings may be **cited** as external research evidence with their source and
> limitations — **that is not the same as ingesting the dataset.**
> **Verify load-bearing licences on the actual distribution page before acquisition.**
> **User-uploaded reference images from request datasets are not assumed cleared.**

Everything below is arranged around those four sentences.

## Evidence caveat carried forward

RES-003 recorded that this session's egress proxy blocks the official distribution pages
(`huggingface.co`, `arxiv.org`, project sites). **That constraint still applies.** Every external
rights fact below is `search_supported`, never officially verified, and **no route may be exercised
until a human reads the actual licence file on the actual page.**

---

## Material class 1 — Product references

| | |
|---|---|
| **Preferred route** | **Controlled first-party capture.** Photograph 12 products the project or operator owns, ≥4 controlled views each. |
| **Rights basis to establish** | First-party ownership. No third-party licence, no consent question. |
| **UGC status** | Not applicable — no user-generated material involved. |
| **Leakage implications** | Controlled capture forms its **own source lineage**, independent by construction and incapable of appearing in any public training corpus we later test against. |
| **Human effort** | **24 person-hours** (sourcing 8, rig setup 4, capture 6, colour/condition records 3, manifest 3). |

**Why not the public alternative.** ABO was structurally near-ideal — 8,222 listings with 24- or
72-view turntable sequences — and RES-003 resolved its licence contradiction to **CC BY-NC 4.0**, with
a named `LICENSE-CC-BY-NC-4.0.txt` users must accept. **Non-commercial rules it out** for a commercial
system under the Controller rule above. It remains available for internal non-commercial evaluator
calibration only, if the Controller ever separates those uses.

**Google Scanned Objects** is CC BY 4.0 with no NC problem and genuinely controlled multi-view — but
they are **generic household objects with no wordmark and no brand colour spec**, so they cannot serve
`logo_wordmark_fidelity` or `packaging_brand_colour_fidelity` at all.

## Material class 2 — Person references

| | |
|---|---|
| **Preferred route** | **Consented internal capture.** 8 identities, ≥4 views × ≥2 framings, written consent. |
| **Rights basis to establish** | Specific written consent naming internal model-evaluation use, retention period and withdrawal process. Facial images are **biometric data** in several regimes. |
| **UGC status** | **DISALLOWED.** See below. |
| **Leakage implications** | Disjointness must hold at **identity** level, not file level. Two photographs of one person are not two independent items. |
| **Human effort** | **31 person-hours**, of which **6 for the consent instrument** — and that row **may require external legal review**, which Resources cannot estimate. |
| **Blocker** | **ACCESS/LEGAL — a human consent decision.** Resources cannot obtain consent and did not try. |

**User-generated images are disallowed, explicitly.** TIP-I2V ships **1.70M+ user-supplied image
prompts** whose provenance is unstated: possibly third-party copyright, possibly identifiable people.
The publisher records an NSFW flag for images, which indicates they expected problematic uploads. Per
the Controller rule, these are **not assumed cleared**, and Resources classifies them **DISALLOWED as
person-reference material** — not "unresolved". It is the largest tempting shortcut in the whole plan.

**Fallback if consent proves impractical:** purpose-created synthetic identity references. No real
person, so no consent and no biometric exposure — at a **stated cost in external validity** (whether
identity-preservation results on synthetic references transfer to real people is an open question, not
an assumption), and with a constraint that references must not come from the generator family under
test. **Eval decides whether that trade is acceptable; Resources only records it.**

## Material class 3 — AV / speaker

| | |
|---|---|
| **Preferred route** | **Controlled recording with consent.** 36 clips, three language conditions. |
| **Rights basis to establish** | **Two separate permissions: likeness AND voice.** Voice is separately protected in several regimes; recording them as one fact loses information. |
| **UGC status** | Not applicable to the preferred route. |
| **Leakage implications** | Disjointness at **speaker** level. Clips reused as the perturbation base **share content lineage** with their originals and cannot be an independent holdout for a measurement that also uses the original. |
| **Human effort** | **73 person-hours — the largest item in the plan.** Transcription (18 h) and turn-boundary annotation (9 h) alone are 27 h. |
| **Blocker** | **ACCESS/LEGAL — consent for likeness and voice.** |

**No public route substitutes.** Public corpora reviewed are audio-only (four of five speech
capabilities need a visible speaking face), and the closest Hinglish candidate, **HiACC, is
CC BY-NC 4.0** — barred by the Controller rule. Nothing public reviewed offers faces + verified
transcripts + turn boundaries + permissive terms together.

## Material class 4 — Commercial / campaign creative

| | |
|---|---|
| **Preferred route** | **First-party and permissioned creative**, including operator client work where clients permit it, acquired as ~10 campaign groups. |
| **Rights basis to establish** | Written permission per asset or campaign. **Ad creative is dense third-party IP** — brand marks, licensed music, talent likeness and stock imagery are often *separately* licensed inside one asset. |
| **UGC status** | Not applicable. |
| **Leakage implications** | Disjointness at **campaign** level. The **20-asset reserve is frozen at acquisition time**, before any evaluator or Canon work touches the 60 active assets. One-way. |
| **Human effort** | **45 person-hours**, dominated by rights-holder outreach (**20 h, confidence: unknown**). |
| **Blocker** | Permission conversations — human decisions. |

**Pitt Ads remains behind an email-request gate**, confirmed from the official readme text: *"To obtain
the dataset for research purposes, please email us."* It is a human permission decision, **not
attempted**, and still the only public candidate addressing this pack. Its research-purpose framing
may not cover commercial-product evaluation, and it is US-weighted, so it does not serve the ≥50%
Indian-market target.

---

## The pattern, and what it costs

**In all four classes the preferred route is controlled or permissioned first-party material.** That is
not a stylistic preference: all four capabilities need **the same subject, under conditions we control,
with rights we can state**. Public datasets give you pictures; these capabilities need *references*.

**All four are blocked on the same thing: a human decision** — consent, permission, an email, a capture
plan. None was attempted.

## Rights gates, in the order they must clear

| # | Gate | Owner | Blocks |
|---|---|---|---|
| 1 | **Is CC-BY-NC usable as commercial-project empirical material?** Currently **NO** absent explicit disposition. | Controller / legal | ABO, HiACC, VidProM, TIP-I2V |
| 2 | **Consent instrument for person + AV capture** — likeness and voice, retention, withdrawal. May need counsel. | Controller / legal | person and AV packs |
| 3 | **Verify load-bearing licences on the actual distribution page.** | a human with unrestricted network | any public route |
| 4 | **Pitt Ads: send the email or close the route.** | Controller | commercial pack |
| 5 | **Confirm UGC reference images stay disallowed.** Resources' position: **disallowed**, not unresolved. | Controller | person pack |

## What Resources did not do

No dataset was downloaded. No account was created. No form, click-through or terms acceptance
occurred. No email was sent. No payment was made. No consent was sought. **₹0 / $0 spent.**
