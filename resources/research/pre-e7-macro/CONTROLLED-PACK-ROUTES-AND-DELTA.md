# Controlled packs — routes and scope delta under the widened program

**Task:** R3-F of `resources/tasks/RES-003-CLOUD-EVIDENCE-PROGRAM.md`
**Date:** 26 Aug 2026 · **Status:** PROPOSED · **No acquisition. ₹0 / $0.**
**Register:** `REQUEST-AND-EVAL-SOURCE-ACCESS-REGISTER.yaml`

---

## Verdict first: the four-pack plan survives

**No fifth pack family is proposed.** The widened scope — composed multi-step outcomes, campaigns,
longer video — does not create a new *kind* of controlled material. It creates new **metadata and
grouping requirements on material the four packs were already going to acquire.**

That is the cheaper answer and it is also the right one: a fifth family would mean a fifth
acquisition, a fifth consent conversation and a fifth rights position, to obtain assets that the
existing families already have to produce.

| Pack | V1 target | Proposed change | New family? |
|---|---|---|:--:|
| Product references | ≥48 = 12 × ≥4 views | **unchanged count**; add cross-asset reuse metadata | no |
| Person references | ≥32 = 8 × ≥4 views | **unchanged count**; add cross-shot capture | no |
| AV / speaker | 36 clips = 24 + 12 | **unchanged count**; add duration + pronunciation coverage | no |
| Commercial creative | 80 = 60 active + 20 reserve | **unchanged count**; add campaign grouping + duration spread | no |

**One route changed, and it changed for the worse.** R3-A resolved the ABO licence contradiction to
**CC BY-NC 4.0** — the restrictive reading. ABO was the structurally ideal public product-reference
candidate (8,222 listings with 24- or 72-view turntable sequences). **Non-commercial use rules it out
for a commercial system.** It remains usable for internal non-commercial evaluator calibration only.

That does not weaken the V1 recommendation; it strengthens it. **Controlled first-party capture was
already the recommended route for every pack, and the best public alternative has now closed.**

---

## What the widened scope actually demands, pack by pack

### Product references — no more views, better recorded reuse

**No increase in count or view tiers.** R3-B found nothing that argues 12 products × 4 views is too
few for identity, colour or edit-preservation work.

**What changes:** composed outcomes reuse the same product across several shots of one video. To
measure `product_stability_in_clip` **across** an assembled sequence — not just within one clip —
Resources must record, at capture time, which reference view was supplied to which production step.

**Consumer need served:** `REQ-CAP-21 product_stability_in_clip` extended to the R3-D
`sequence_or_asset_set` level. **This is a metadata field on the R3-D topology, not more photographs.**

### Person references — no more identities, one capture-condition addition

**No increase from 8 identities × ≥4 views.**

**What changes:** the same person must appear across multiple shots of one outcome. The V1 pack
specifies ≥4 *controlled views* — lighting, angle, pose. For cross-shot work, capture should also
include **at least two distinct framings per identity** (e.g. close and mid), because identity drift
between a close-up and a wide shot is a different failure from drift within one framing.

**Cost of this addition: two extra frames per identity, 16 images total.** It is a capture-plan note,
not a scope increase.

**Unchanged and absolute:** no public-face scraping. R3-A reinforces this — TIP-I2V contains **1.7M+
user-uploaded image prompts** whose provenance is not stated and which may depict identifiable people.
It is the largest tempting shortcut in the register and it is **not** person-reference material.

### AV / speaker — the one place a genuine coverage argument exists

**No increase from 36 clips (24 single + 12 two-speaker).**

**Two coverage requirements the widened scope does create:**

1. **Duration.** R3-B measured it: **the longest clip we hold anywhere is 20.00 seconds, and there is
   nothing above 30 s in the corpus at all.** If outcomes are 20-second branded videos, a VO pack made
   entirely of 5-second utterances cannot support them. **Proposed: at least 6 of the 24
   single-speaker clips run ≥20 seconds continuous**, so lip-sync and drift can be measured over a
   real deliverable's length rather than a fragment.
2. **Pronunciation coverage.** Hinglish is a first-product requirement and code-switching is where
   speech systems fail. **Proposed: the Hinglish clips deliberately include brand names and
   English-loanword pronunciation**, because "reads the script correctly" and "says the brand name
   correctly" are different capabilities and only the second matters commercially.

**Still 36 clips.** These are composition constraints on clips already being recorded.

**Route position unchanged and confirmed:** no public AV corpus reviewed offers faces + verified
transcripts + turn boundaries + permissive terms. HiACC is audio-only and CC BY-NC. **Controlled
recording with consent remains the only route**, and it remains blocked on a human decision.

### Commercial creative — grouping metadata, and a duration spread

**No increase from 80 assets (60 active + 20 reserve).**

**Two additions, both metadata-or-selection rather than volume:**

1. **Campaign grouping.** R3-B found the corpus has **no field that could express "these assets belong
   to one campaign"**, and campaign/variant consistency is now in scope. **Proposed: acquire the 40
   video assets as ~10 campaign groups of related deliverables** rather than 40 unrelated ads. Same
   count, organised so variant-consistency questions are answerable at all.
2. **Duration spread.** **Proposed: the 40 video assets span 6 s / 15 s / 20–30 s**, matching real
   platform cuts. Acquiring 40 six-second ads would leave the longer-outcome question unanswerable.

**Reserve size: unchanged at 20.** Nothing in the widened scope argues for a larger reserve, and
enlarging it would shrink the active bank for no named consumer.

**Route unchanged:** first-party and permissioned creative is the recommendation. **Pitt Ads remains
behind an email-request gate** — a human permission decision, still not attempted, still the only
public candidate that addresses this pack.

---

## Summary of proposed deltas

| # | Delta | Volume change | Named consumer need |
|---|---|---|---|
| 1 | Record which product reference view fed which production step | **none** | `REQ-CAP-21` at sequence level |
| 2 | ≥2 distinct framings per person identity | +16 images | cross-shot `REQ-CAP-11` / `REQ-CAP-20` |
| 3 | ≥6 single-speaker clips ≥20 s continuous | **none** | lip-sync over deliverable-length audio |
| 4 | Hinglish clips include brand names / loanwords | **none** | `spoken_language_correctness` commercially |
| 5 | 40 video ads acquired as ~10 campaign groups | **none** | campaign/variant consistency |
| 6 | Video ads span 6 s / 15 s / 20–30 s | **none** | longer composed outcomes |

**Five of six deltas cost nothing in volume.** The single volume change is 16 images. Every row names
the consumer need it serves, as the task requires.

## What did not survive contact with the evidence

- **ABO as the product pack** — closed by CC BY-NC 4.0. Internal non-commercial calibration only.
- **Any public AV shortcut** — HiACC and comparable corpora are audio-only and non-commercial.
- **TIP-I2V's user images as person references** — not cleared, possibly identifiable people, and the
  publisher's own NSFW flagging indicates they expected problematic uploads.

## Unchanged blockers

All four packs remain blocked on the same thing: **a human decision** — consent for person capture,
permission for commercial creative, an email for Pitt Ads, a capture plan for products and AV. **None
was attempted.** Resources cannot obtain consent, accept terms, or send that email.

## Lineage consequence to carry into acquisition

From R3-C: any pack that later serves `evaluator_calibration` contaminates `final_holdout` for
anything sharing its lineage. **The 20-asset commercial reserve must be frozen at acquisition time,
before any evaluator or Canon work touches the 60 active assets.** Freezing is one-way, and a reserve
someone has already looked at is not a reserve.
