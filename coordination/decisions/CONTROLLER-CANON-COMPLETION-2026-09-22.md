# Controller — Amend C-10: complete Canon under a written definition of done — 2026-09-22

**Status:** APPROVED CONTROLLER DECISION (founder, 2026-09-22, in session; quoted verbatim below).
**Role:** drafted by the Controller session on branch `work/canon-done-2026-09-22`; no pack is
compiled, no Canon file is changed by this draft.
**Amends:** C-10 in `CONTROLLER-CAPABILITY-LAB-STOP-WIDENING-AND-CANON-INJECTION-V1-2026-09-14.md`
("Do NOT compile the remaining eight packs unless a real runtime failure later demands one").
**Related:** `canon/validation/CANON-DONE-v0.md` (the definition of done and the test);
`canon/validation/HAND-RETRIEVED-CLAIMS.yaml` (87 claims producers retrieved by hand on six jobs);
`coordination/assessments/P1-PRODUCTIZATION-2026-09-22/` (the P1 assessment, §C).

## What is being decided — in plain English

C-10 froze eight of ten knowledge packs until "a real runtime failure" demanded one. Six
production jobs have run since; none through the runtime, so the trigger could never fire — and
on every one of them the producer read the eight frozen shelves by hand (87 distinct claims from
23 sources). A machine-run P1 would not do that reading. The founder's instruction on 22 Sep:
complete Canon once, properly, rather than fix it job by job. This decision replaces the C-10
trigger with a written definition of done and authorises the eight packs to be built under it.

## Authority — the founder's words (to be quoted verbatim on approval)

> "approve as drafted. go build the sheets"

Context of the instruction, from the session of 22 Sep 2026: "go for it. i dont mind the time it
takes, i mind the tokens you spend to do it and quality of work" and "i would rather have complete
canon once then spending time and money again and again to fix it".

## Rulings

1. **C-10's compile prohibition is lifted for all eight packs**, replaced by
   `canon/validation/CANON-DONE-v0.md`: a pack is done only when `canon_done.py` conditions A
   (10 injected, 0 gaps, adopted, within budget, validator green), B (every hand-retrieved claim
   from its sources is cited) and D (an adoption decision) pass, and C (the blind comparison) is
   recorded before adoption.
2. **Build order** (P1 dependence first): commercial_communication, editing_pacing_and_short_form,
   typography_and_copy, camera_and_spatial_grammar, colour_and_visual_register,
   concept_and_distinctiveness, indian_indic_context, critique_and_effectiveness. Two builders in
   parallel, one independent checker per pack, in the cloud (not the 8 GB Mac).
3. **The two existing packs** (composition_and_attention, product_appearance) are extended to
   their seed lists (32 and 13 hand-retrieved claims; 15 and 4 cited today) and adopted under the
   same test. Their PROPOSED headers are replaced by an adoption line citing this decision.
4. **The CANON-015 fetcher (PR #84) is not adopted.** Measured on the 37-source corpus it
   delivers 0 of 22 hand-retrieved claims on Mokobara and 1–2 of 25–32 on RentOK at every
   budget and query tried (`CANON-DONE-v0.md`). Job-specific retrieval in the product is a
   bounded, logged model step (every cited id recorded with `retrieved_by` in the Stage 3 form),
   measured by the same coverage test before it is trusted. CANON-SHAPE-v1 §4's "the model never
   chooses what to read" is amended accordingly for that one step.
5. **No new sources are ingested** under this decision; the 37 accepted sources are the corpus.
   The audio gap and the animation/game gap remain recorded in the trigger table.
6. **Spend:** USD 0 in media. Builder and checker sessions are the only cost; each pack's
   session tokens are recorded in the pack's build note.
7. **Stop rule:** if the blind comparison (C) shows the hand-retrieved claim texts beating the
   compiled packs on all three briefs, compilation stops at the packs already built, the result
   is recorded, and the model retrieval step becomes the primary mechanism — no further packs
   without a new decision.

## What this decision does not do

It does not merge PR #103, #104 or #84; it does not change the Registry, routing or any accepted
job record; it does not authorise paid generation.
