# Controller — ADOPT the ten compiled Canon packs — 2026-09-22

**Status:** APPROVED CONTROLLER DECISION (founder, 2026-09-22, in session).
**Authority — the founder's words, verbatim:**

> "adopt ten sheets"

(Context in the same session: "approve as drafted. go build the sheets"; earlier, "i would rather
have complete canon once then spending time and money again and again to fix it".)

**Follows:** `CONTROLLER-CANON-COMPLETION-2026-09-22.md` (which lifted C-10's compile prohibition
under a written definition of done) and completes it.
**Evidence:** `canon/validation/CANON-DONE-v0.md` (the definition and the test),
`canon/validation/canon_done.py` (A, B, D), `canon/validation/HAND-RETRIEVED-CLAIMS.yaml`
(87 claims from 23 sources, cited by producers on six recorded jobs),
`canon/compilation/authoring/CHECK-*.md` (one independent check per pack),
`canon/validation/blind-comparison-2026-09-22/` (condition C).

## What is adopted

All ten packs in `canon/compilation/PACK-*-v0.yaml` are ADOPTED as the production doctrine packs.
Their status lines change from PROPOSED to ADOPTED by way of `canon/compilation/ADOPTIONS.yaml`,
which the compiler reads. No pack content changes at adoption.

| Pack | Decisions | Cited objects | Seeds | Terse tokens | Independent check |
|---|---|---|---|---|---|
| camera_and_spatial_grammar | 8 | 58 | 25/25 | 2498 | PASS WITH EDITS (applied) |
| colour_and_visual_register | 10 | 61 | 23/23 | 2497 | PASS |
| commercial_communication | 10 | 58 | 41/41 | 2497 | PASS |
| composition_and_attention | 11 | 82 | 32/32 | 2286 | PASS WITH EDITS (applied) |
| concept_and_distinctiveness | 10 | 85 | 44/44 | 2499 | PASS WITH EDITS (applied) |
| critique_and_effectiveness | 10 | 74 | 63/63 | 2499 | PASS |
| editing_pacing_and_short_form | 10 | 45 | 29/29 | 2500 | PASS WITH EDITS (applied) |
| indian_indic_context | 6 | 27 | 5/5 | 2490 | PASS |
| product_appearance | 12 | 45 | 13/13 | 2500 | PASS WITH EDITS (applied) |
| typography_and_copy | 11 | 62 | 29/29 | 2499 | PASS WITH EDITS (applied) |

On every recorded brief the lookup now selects ten packs, injects ten, records **zero gaps**, and
delivers every claim its producer retrieved by hand (22/22 Mokobara, 32/32 RentOK A, 25/25 V2).

## The blind comparison (condition C), recorded

Nine boards, three briefs × three arms (ten packs / the hand-retrieved claim texts / brief only),
ids stripped, arms sealed, judged by a non-author whose verdict was committed before the mapping was
opened: **packs 8 · hand-retrieved claims 7 · brief only 3** (3/2/1 per job).

Read honestly: knowledge beats no knowledge on every brief; the packs are **not worse** than the
hand retrieval they replace, which is what §C tested; 8–7 over three briefs and one judge is **not**
evidence that packs are better. The judge, blind to arms, attributed the winning boards to form —
a `first_frame` that already contains the idea, one job per clip with stated timing, declared
deviations — "and none of them is knowledge". The stop rule (completion decision, ruling 7) does not
fire. Full limits in `canon/validation/blind-comparison-2026-09-22/RESULT.md`.

## Rulings

1. The ten packs are ADOPTED for production injection. `canon/packs/pack-triggers-v0.yaml` and
   `canon/CANON-SHAPE-v1.md` §2 are updated to say ten of ten compiled and adopted.
2. **What adoption does not establish** (carried from the validator's own words): relevance to any
   brief, doctrine quality, medium fit, or outcome improvement. A pack is a made decision a producer
   may deviate from with a recorded reason; it is not a result.
3. The declared gaps inside the packs stand as written and are the register of what Canon does not
   cover: 9:16 feeds and sound-off autoplay; grading; animated type and motion design; platform
   safe zones and recompression; Devanagari and non-Latin legibility; ASCI's rules; Indian price and
   offer display; national symbols; skin tone and colourism; packshot convention; product-only
   camera motivation; contrast over a moving ground; what changes for a single still.
4. Job-specific retrieval beyond the packs remains a logged model step; every claim a producer cites
   is recorded with `retrieved_by` in the Stage 3 form.
5. No new source is ingested. `canon_done.py` is the standing test: any later pack edit must keep
   A, B and D green.
6. Nothing here merges PR #103, #104 or #84, changes the Registry or routing, or authorises spend.

## Known notice carried into adoption

The lookup emits, as it did with two packs: *"receipt vocabulary retired by CANON-SHAPE-v1 §5 is
still carried by the canon-owned pack text of …"* — the packs' `feeds_sections` vocabulary
(`FAILURE_PREVENTION`, `DOCTRINE_DEVIATIONS`) predates §5's retirement of consumption receipts.
The runtime does not require receipts and the gate does not read them, so this is a wording debt in
canon-owned text, not a behaviour. It is adopted as-is and fixed when the pack format is next
revised.
