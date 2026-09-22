# Build note — PACK editing_pacing_and_short_form (EP)

Built 2026-09-22 against `canon/compilation/authoring/BUILDER-BRIEF.md`. USD 0; no model call.
Applicability: `video`, `image_sequence` (every decision is about ordered shots in time; the
image_sequence limit line says which decisions additionally need a timeline and an audio track).

## 1. Decisions (10)

- **EP-D1** How does the film open? — mid-action / close-up / bold imagery; reach the heart faster; hook then sustain; opening music must not set an expectation the film fails to meet.
- **EP-D2** What must every cut carry, and what lets us leave the shot? — new information in the shot cut to; a motivating movement or sound in the shot cut from; when a cut is the right transition; the edit is the order and rate of release of information.
- **EP-D3** When candidate cuts compete, which wins? — Murch's six ranked criteria, emotion first; aim for all six; sacrifice bottom-up only when forced.
- **EP-D4** How long does each shot hold? — describe-aloud duration for any shot that must be read; felt beat for beat-driven cuts; the sub-three-second norm is not a rule; over-frequent changes read as a pointing guide.
- **EP-D5** How do movement and screen direction hold across cuts? — screen direction, action line, crossing the line, side-of-frame continuity, the inserted bridging shot.
- **EP-D6** Move the camera, hold it, or cut — and how is attention moved? — every move and every hold has a reason; move attention inside a shot (camouflaged move, static-wide blocking, pre-established colour); never rack focus back and forth.
- **EP-D7** Cut, dissolve or fade — which, and what does it say? — cut as default; dissolve register and duration; fade as boundary; audio up before picture fades in.
- **EP-D8** What does sound do that picture cannot, and how does music enter? — sound creates reality faster; sound bridge; score channels an emotion already created; source music takes a different route; withdrawn voice makes sound read as speech.
- **EP-D9** Where and how does the brand appear across the film? — from the start and throughout; early/often/richly; asset variety; core-then-tailor; full-funnel finish on product.
- **EP-D10** How is the ask made, and how are audio and on-screen channels paired? — clear CTA tied to one objective; see-and-say pairings for CTA and brand; supers and audio reinforce, never compete; pairings rest on sound-on (YouTube only); full-funnel CTAs throughout.

## 2. Seed coverage — 29 of 29

| Seed | Decision |
|---|---|
| sk_abcd_0006, sk_abcd_0007 | EP-D1 |
| sk_abcd_0010, sk_abcd_0011, sk_abcd_0013 | EP-D9 |
| sk_abcd_0026 | EP-D9, EP-D10 |
| sk_abcd_0012, sk_abcd_0019, sk_abcd_0020, sk_abcd_0021 | EP-D10 |
| sk_gote_c003_0004, sk_gote_c003_0006 | EP-D2 |
| sk_gote_c003_0017 | EP-D5 |
| sk_gote_c003_0031, sk_gote_c003_0037 | EP-D7 |
| sk_gote_c003_0048 | EP-D8 |
| sk_gote_c003_0052, sk_gote_c003_0053 | EP-D4 |
| sk_ms_c003_0002, sk_ms_c003_0016, sk_ms_c003_0017, sk_ms_c003_0019 | EP-D6 |
| sk_murch_c003_0013 | EP-D2 |
| sk_murch_c003_0019, sk_murch_c003_0020, sk_murch_c003_0027 | EP-D3 |
| sk_conv_c003_0007, sk_conv_c003_0019 | EP-D8 |
| sk_conv_c003_0023 | EP-D1 |

Non-seed ids added (16, all read in full): sk_abcd_0005, 0008, 0014, 0022; sk_gote_c003_0007, 0009, 0018, 0027, 0028, 0054, 0055; sk_ms_c003_0010; sk_murch_c003_0031; sk_conv_c003_0009, 0024. Total 45 sk objects; all five contributors compiled; no coverage-delta line needed.

## 3. Closure holes and resolution

By **cite**:
- sk_abcd_0011 ↔ 0026 (both seeds, EP-D9).
- sk_abcd_0012 / 0021 / 0008 depend on sk_abcd_0014 → 0014 cited (EP-D10); 0014's qualifies-partners 0008, 0012, 0021 all cited.
- sk_abcd_0013 / 0020 depend on sk_abcd_0022 → 0022 cited (EP-D9).
- sk_gote_c003_0004 ↔ 0006 (both seeds, EP-D2).
- sk_gote_c003_0017 depends on 0054 → cited (EP-D5).
- sk_gote_c003_0031 depends on 0028 → cited (EP-D7).
- sk_gote_c003_0052 ↔ 0053 (both seeds, EP-D4) — also pre-arbitrated as CF-01.
- sk_conv_c003_0007 qualified_by 0009 → cited (EP-D8).
- sk_murch_c003_0027 qualified_by 0031 → cited (EP-D3; it bounds when the sacrifice rule applies, which changes the default).

By **conflict** (resolution rules are scope rules drawn from the claims' own stated conditions):
- CF-01 gote_0053 vs gote_0052 (qualified_by): 0053's stated scope is the informational/establishing shot; 0052's own words give quick cuts a place in action sequences but not love scenes.
- CF-02 ms_0017 vs ms_0010 (contradicts, stored on 0017): the static-wide technique for continuous two-person movement versus the chapter's camouflaged-move default; both cited.
- CF-03 murch_0018 vs murch_0033 (contradicts): cut frequency versus in-shot misdirection; 0033 not compiled, named so the boundary is visible.

By **waiver** (14; each states what the decision consumes and why the partner does not change it):
- sk_abcd_0022 qualifies sk_abcd_0001 (set membership vs the two-stage rule).
- sk_ms_c003_0019 qualifies sk_ms_c003_0008 and 0014 (limit consumed; combination advice and reflection technique not compiled).
- sk_ms_c003_0016 trades_off_with sk_ms_c003_0014 (the trade-off is a lens choice; EP-D6 does not decide lens; 0014 not compiled).
- sk_ms_c003_0010 qualified_by sk_ms_c003_0001 and 0004 (meta-claims about the recipes' status; neither changes the default).
- sk_ms_c003_0002 qualified_by sk_ms_c003_0018 (the invisibility test is the other face of the motivation rule; dropped from the text for the terse budget after being cited in an earlier draft).
- sk_gote_c003_0018 qualified_by sk_gote_c003_0008 (sound level does not change side-of-frame continuity; dropped from EP-D8 for the terse budget after being cited in an earlier draft).
- sk_murch_c003_0019 qualified_by sk_murch_c003_0011 (film-relative bad-bit criterion; does not reorder the six — the narrative-film scope is carried as the EP-D3 limit line).
- sk_murch_c003_0019 qualified_by sk_murch_c003_0028, 0029, 0032 and sk_murch_c003_0027 qualified_by 0030 (justification, hedged weights, underlying preoccupation, top-three binding — none reorders the list; all four were cited in an earlier draft and removed to fit the budget, see §6).
- sk_conv_c003_0009 qualified_by sk_conv_c003_0011 (overuse bound does not change which route a cue takes).

Note on the compiler's closure semantics: a stored `qualifies` is reversed onto its target only, so the three `qualifies` waivers (abcd_0022, ms_0019 x2) are not required by the compiler; they are kept because the seed packet lists those partners and the judgement should be on record.

## 4. Limit lines and why

- EP-D3: Murch's list is scoped 'for me' and to narrative film — the source's own caveat; a product film is not narrative film.
- EP-D10: audio pairings assume sound-on, stated for YouTube only (sk_abcd_0014's own scope) — a sound-off feed has no doctrine here.
- Pack: no contributor treats 9:16 feed frames or sound-off autoplay (all four craft sources predate feed video; ABCD is YouTube-only) — transfer untested. Shape follows CA-D6.
- Pack: no target duration anywhere — 'early', 'faster', 'the start', 'often' unquantified (caveats on sk_abcd_0005, 0006, 0010, 0011).
- Pack: B12 motion design / animated type has no contributor; B09 dialogue presentation is thin (two claims).
- Pack: image_sequence — transition durations and sound decisions need a timeline and audio track.
- Devanagari line added by the compiler.

## 5. Deliberately not compiled

- ABCD Connection principle (sk_abcd_0015–0018) and the per-objective weighting rows (0023–0025): commercial-communication territory, not editing.
- Grammar of the Edit's six-element checklist (0003), edit-type taxonomy (0039–0046), wipe (0033–0036), 30-degree / jump-cut rules (0012, 0013), split edit (0022), reaction shots (0051), self-sufficient shot (0050): each brings guard partners that would cost terse budget the seeds needed; the pack states the cut/motivation/information core and the transition meanings the seeds asked for.
- Murch's editing-room discipline (0034–0039) and history/why-cuts-work (0004–0010): not producer decisions for a brief.
- Kenworthy techniques 8.1–8.5 (0011–0015): the chapter's worked moves; EP-D6 carries the governing rule and the three techniques the seeds named.
- Ondaatje: structural-repair cases (0001–0006), music timing (0008, 0010), character/lens claims (0012–0018, 0020–0022, 0025–0027).

## 6. Terse budget

2,497 of 2,500 tokens. The first full draft rendered at 3,193 tokens; it fit by tightening prose, not by dropping seeds. Four non-seed Murch qualifiers (0028, 0029, 0030, 0032), ms_0018 and gote_0008 were cited in early drafts and moved to waivers to fit — their content is recorded above and each waiver says why the default stands without it. No seed was dropped.

## 7. Red flags

None of the four named in the brief. No seed lacked an honest question; no waived partner changes a default; the pack fits with all seeds; the two in-source contradictions (CF-02, CF-03) each have a condition that separates them.

## 8. Session tokens

Roughly 200k tokens for this build (seed packet read in sections, 32 non-seed claims fetched by id, six compile iterations).
