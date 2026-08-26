# Canon V1 — the 30-brief commercial bank (C2)

**Task:** CANON-V1 overnight program, work package C2 · **Date:** 26 Aug 2026
**Status:** complete and mechanically validated · **Owner:** Canon
**Zero planning outputs have been generated.** This is experiment input only.

---

## 1. What this is, and why Canon owns it

Thirty commercial intents a real Indian business might bring to the product. One stable bank, reused
across Canon's planning experiments (C5, C9, C10) and later **sampled by Eval** for the twelve
end-to-end production-workflow briefs in its own benchmark.

**Eval must not build a competing 30-brief bank.** That is not a territorial rule — it is what makes
the two streams' results comparable. If Canon measures planning quality on one set of briefs and Eval
measures production capability on another, no one can ever join the two.

## 2. The design rule that protects the experiment

Each brief is stored in two separate parts, and the separation is the whole point.

| Field | What it holds | Who sees it |
|---|---|---|
| `customer_brief` | What the customer actually said — incomplete, sometimes vague, sometimes self-contradictory | Both experiment arms |
| `authoritative_intent` | What must survive: exact strings, hard constraints, explicit intent, and the contradictions we planted | **Scoring only. Never shown to a planning arm.** |

**There is no finished Creative IR anywhere in this bank, deliberately.** No chosen hierarchy, no
selected proposition, no acceptance contract, no craft direction. Producing those from a messy brief
is precisely what Experiment A measures. Writing them here would answer the question the experiment
is asking, and the result would be worthless.

## 3. Structure and balance — all verified mechanically

| Dimension | Result |
|---|---|
| Briefs | **30** |
| Scenario families | **10 × exactly 3** |
| Language | **10 English-primary / 10 Hindi-Devanagari-primary / 10 Hinglish-mixed** |
| Media class | 12 static / 18 video |
| Video durations | all within the 6–20 second first-product scope |
| Distinct product categories | 20 |
| Objectives | 6 kinds — consideration 8, conversion 6, brand 6, awareness 4, offer 4, demonstration 2 |
| Specification quality | 13 clear / 9 underspecified / 8 contradictory |
| People | 11 with none, 12 with one, 7 with two |
| Planted contradictions | **15 across 8 briefs**, each with its correct handling recorded |

**Language is deliberately not confounded with scenario family.** Every family carries one brief of
each language condition. If the Canon arm wins the value gate, that win cannot be an artifact of
which families happened to be Hindi — a confound that would have been invisible afterwards and
impossible to fix without rebuilding the bank.

## 4. What the bank asks of the Canon — and one uncomfortable number

Each brief is tagged with the knowledge packs it requires. Cross-referenced against the C1 coverage
rebaseline:

| Pack required | Briefs needing it | Canon coverage (C1) |
|---|---|---|
| commercial_communication | 30 | covered, one critical domain limited |
| concept_and_distinctiveness | 30 | covered |
| critique_and_effectiveness | 30 | covered — strongest pack |
| colour_and_visual_register | 30 | covered |
| typography_and_copy | 28 | **critical hole — no Devanagari source** |
| **indian_indic_context** | **20** | **empty — zero contributing sources** |
| camera_and_spatial_grammar | 18 | covered |
| editing_pacing_and_short_form | 18 | **critical hole — no short-form source** |
| product_appearance | 13 | **critical — present but unbound** |
| composition_and_attention | 12 | covered |

**Two thirds of the bank needs a pack the Canon does not have at all.** That is not a flaw in the
bank — the briefs were written from the first-product scope, not from what the Canon happens to
hold. It is the clearest single statement of the Canon's distance from its own product, and it is
why C4 researches sources against gaps rather than by interest.

## 5. Capability families the bank will exercise

Tagged per brief against Eval's eight families, as **requirements only**. Canon states what a job
needs; it names no model, no provider and no measurement method.

`constraint_fidelity` 30 · `commercial_creative_fitness` 30 · `identity_and_references` 30 ·
`text_and_brand` 28 · `human_physical_realism` 19 · `temporal_continuity` 18 ·
`operational_workflow` 17 · `speech_audio` 12

Twelve briefs carry exact spoken scripts (voiceover, single speaker or two-speaker dialogue). The
two-speaker briefs record **turn boundaries explicitly**, because the three-stream plan says Eval's
AV work needs them and discovering that later would mean re-reading all thirty.

## 6. Devanagari strings are exact by design

Required copy is held as exact strings, including matras, conjuncts and nuktas. `तेज़` without its
nukta is a different word; `मिष्ठान` carries a conjunct that extraction and rendering both routinely
damage.

This is not pedantry. Eval's existing exactness battery exists because a generator can produce
something *subtly* wrong that a checker calls a match — shipping a defect with a passing grade. The
bank makes those cases available as commercial briefs rather than isolated test strings.

## 7. One brief carries a flag, not a fix

`BR-F07-HI` scripts a farmer saying an agricultural product doubled his crop. That is a strong
efficacy claim presented as personal testimony.

**It is recorded exactly as the customer said it**, because this bank records commercial intents —
it does not approve executions. If it is ever produced as real advertising, the claim needs
substantiation and the testimony needs to be genuine. The flag lives in the brief's authoritative
intent and is **excluded from value-gate scoring**, so it does not leak into reviewers' judgements
of planning quality. Flagged, not silently softened.

## 8. Files and verification

| File | What it is |
|---|---|
| `briefs-source.yaml` | Authored source. Edit here. |
| `briefs.jsonl` | Generated, one brief per line. The experiment input. |
| `build_brief_bank.py` | Validator and generator. **Fails closed** — nothing is written if any constraint breaks. |

`python3 canon/experiments/v1/brief-bank/build_brief_bank.py` — **run in this session, exit 0.**

It enforces, among other things: exactly 30 briefs; 10 families of 3; 10/10/10 languages; one of each
language per family; every `must_appear_exactly` string actually present in the customer brief it
belongs to; every brief marked contradictory actually planting one; every brief marked underspecified
naming what is underspecified; video durations inside 6–20 seconds; and no Creative IR vocabulary
leaking into a customer-facing brief.

**Not done:** no planning output, no Creative IR, no model call, no human judgement.
