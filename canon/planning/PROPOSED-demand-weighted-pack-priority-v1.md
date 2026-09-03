<!-- STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
     coordination/CONTROL-STATE.md governs. -->

# PROPOSED — Demand-weighted pack priority v1 (Canon repair / REP-01)

Joins the 54 recorded demand units against live-24 pack supply so pack compilation is ordered by
what buyers actually ask for, not by corpus mass. Nothing here amends
`canon/planning/CANON-V1-GAP-LEDGER.md` — that file is history and is not edited; §4 below
carries the amendments as PROPOSED text for a Controller-adopted next revision.

## 1 · The 54 demand units and how each number recomputes

| demand source | units | video | how the number is computed |
|---|---|---|---|
| `canon/experiments/v1/brief-bank/briefs.jsonl` | 30 | 18 | mechanical: line count; `media_class == "video"` |
| `canon/research/marketplace-demand-v1/derived/marketplace-brief-bank-v1.yaml` | 18 | 18 | mechanical: `len(cases)`; `normalized_request.R05_modality.value == "video"` |
| `eval/experiments/EVAL-037/common/briefs/*.txt` | 6 | 3 | mechanical: file count; a brief is video iff its text states a `duration` (B01 "Target duration: about 30 seconds", B04 "Target duration: about 25 seconds", B05 "Target final duration: about 40 seconds"; no static brief mentions one) |
| **total** | **54** | **39** | 39/54 = 72% of recorded demand is video |

Machine-readable block (parsed and recomputed by `canon/validation/validate_live24_coverage.py`):

```yaml
demand_counts:
  brief_bank_total: 30
  brief_bank_video: 18
  marketplace_total: 18
  marketplace_video: 18
  eval037_total: 6
  eval037_video: 3
  total: 54
  video_total: 39
```

**Per-pack demand attribution.** Three evidence grades, kept separate and never mixed silently:

- **Mechanical (brief bank):** `tags.knowledge_packs_required` counted over the 30 briefs.
- **Authored rule (marketplace):** the 18 cases carry no pack tags. All 18 are video ad
  deliverables (R05 mechanical, above), so each is attributed to the four packs a video ad
  cannot be planned or judged without: `editing_pacing_and_short_form`,
  `camera_and_spatial_grammar`, `commercial_communication`, `critique_and_effectiveness`.
  This is deliberately CONSERVATIVE — many cases plausibly also demand identity, typography or
  India-context packs, and are NOT counted there; marketplace demand below is an undercount for
  every other pack.
- **Authored per-brief (EVAL-037):** classification table in §5; a judgement call per brief,
  labelled as such.

## 2 · Demand × supply join (54 demand units × 10 packs)

Supply columns are read from the regenerated `canon/planning/CANON-V1-LIVE24-COVERAGE.yaml`
(pack_state, contributor_count, independent origins). `newest contributor year` is the maximum
publication year recorded in the contributors' `PROVENANCE.md` files; three sources record an
edition but no year (grammar-of-the-shot 2nd ed., light-science-magic 5th ed., ogilvy) and are
excluded from the maximum, marked `*` where they could raise it.

| pack | demand /54 | of which video-driven | pack_state (live24) | contributors | indep. origins | newest year | priority verdict |
|---|---|---|---|---|---|---|---|
| editing_pacing_and_short_form | **39** (18 bank + 18 mkt + 3 eval) | 39 | **critical_hole** (B11) | 4 | 3 | **2011** | **P1 — worst demand/supply inversion in the map.** 72% of demand lands on a pack whose newest source predates the feed era; B11 is empty and unfillable from the accepted library. |
| camera_and_spatial_grammar | **39** (18 + 18 + 3) | 39 | covered | 6 | 4 | 2011* | P2 — covered for film-era spatial grammar; same 2011 staleness rides every video brief. B05-class briefs are its acceptance test. |
| commercial_communication | **53** (30 + 18 + 5) | 39 | critical_limited (C09) | 9 | 9 | 2019 | P2 — deepest pack, but its hook domain is print-era by its own override; the highest-leverage moment of every video brief leans on it. |
| critique_and_effectiveness | **53** (30 + 18 + 5) | 39 | covered | 21 | 19 | 2019 | P3 — broadest supply; compile risk is degeneracy (21 contributors ≈ the corpus), needs the domain→system map to stay bounded. |
| typography_and_copy | **29** (28 + 0 + 1) | 10 | **critical_hole** (A14) | 5 | 5 | 2017 | **P1 — Devanagari/Indic (A14) empty while ~2/3 of bank briefs are Devanagari-primary or Hinglish**; unfixable without a Controller acquisition decision (G1/CANON-008). |
| indian_indic_context | **24** (20 + 0 + 4) | 13 | critical_limited (C13) | 5 | 5 | 2016 | P1 — no longer absent, but supply is 2002-2016 register/iconography priors, not the operational conventions demanded (see G3a/G3b below). Marketplace attribution excluded here, so 24 is an undercount. |
| colour_and_visual_register | **33** (30 + 0 + 3) | 18 | covered | 8 | 8 | 2017 | P3 — well supplied; India colour meaning is dated (jain 2007) and festival codes absent (G3b). |
| concept_and_distinctiveness | **33** (30 + 0 + 3) | 18 | covered | 13 | 12 | 2019 | P3 — well supplied, multi-origin. |
| composition_and_attention | **15** (12 + 0 + 3) | 3 | covered | 10 | 9 | 2017 | P4 — strongest supply relative to recorded demand. |
| product_appearance | **15** (13 + 0 + 2) | 3 | critical_limited (A13) | 6 | 6 | 2013* | P2 — modest demand count but a primary acceptance condition where it appears (packshot briefs); the block is translation (G4/G11), not sourcing. |

Headline row, stated once and recomputable: **editing_pacing_and_short_form is demanded by 39 of
54 units (72%), supplied by 4 contributors (3 independent origins) whose newest recorded
publication year is 2011, and its only critical short-form domain (B11) is empty.** The demand
distribution is the inverse of the supply distribution.

## 3 · What the join does NOT say

- Demand counts are not importance weights per brief: a pack demanded by 15 briefs as a primary
  acceptance condition can outrank one demanded by 30 as background (product_appearance's P2
  reflects this and is a judgement, labelled).
- The marketplace attribution rule undercounts every pack outside the four video packs; totals
  above are floors, not measurements, wherever the mkt column is 0.
- Nothing here authorises compilation, spend, or admission of HOLD sources; those are Controller
  gates (`coordination/CONTROL-STATE.md`).

## 4 · PROPOSED gap-ledger amendments (text for the next ledger revision; the committed ledger is not edited)

### 4.1 Split G3 into G3a and G3b

**G3a · Indian register & iconography — domain C13, pack `indian_indic_context` —
PARTIALLY COVERED.** Five accepted sources (bijapurkar 2007, dwyer-patel 2002, jain 2007,
pandey 2015, parameswaran 2016; 97 objects) now supply consumer-logic, register and iconography
priors: darshan and frontality (sk_dpci_0010, sk_dpci_0020, sk_jgb_0010), calendar-art colour
(sk_jgb_0020), audience purchase logic (sk_rbwl_0060, sk_rbwl_0070), vernacular register
(sk_nnn_0019, sk_nnn_0052). All five carry `technology_contingency applicable=true` in their
audit records — decade-dating is mandatory on every compiled claim. The ledger sentences "zero
contributors" and "every accepted source is Anglo-American" are false against the live-24 corpus
and must not be carried forward.

**G3b · Indian operational conventions — same domain — EMPTY, and not fixable by books.**
Festival codes by occasion, price framing conventions, current Hinglish/language-mixing norms,
current category conventions. None of the five sources holds these (they are 2002-2016 cultural
history), and the original ledger verdict — "expert + customer memory + empirical" — stands for
this half: fill via a structured expert-elicitation artifact admitted under a variant gate, plus
empirical memory from accepted/rejected outcomes. A compiled India pack must state explicitly
that these conventions DO NOT EXIST in Canon so a weak model does not improvise them.

### 4.2 Corrected G2 prose

Replace "The newest accepted source is 2013 and the domain postdates all nineteen" with:
**"The newest accepted MOVING-IMAGE source is 2011 (kenworthy-master-shots-ch8); the corpus's
post-2013 accepted sources — samara 2017, binet-field 2018, sutherland 2019, per their
PROVENANCE.md — are not moving-image sources, and the domain postdates all twenty-four."** The
original sentence was true of the live-19 corpus read loosely and is false as written against
live-24; the corrected sentence is sharper and survives corpus growth.

### 4.3 New demand-derived rows G12-G15 (from marketplace `capability_coverage_observations` CO-01..CO-04)

| ID | Gap | Evidence | State | Remedy class |
|---|---|---|---|---|
| **G12** | **Supplied-document content fidelity** — no pack or capability measures whether a deliverable faithfully conveys the CONTENT of a supplied source document | CO-01; MKT-004, MKT-018 — the buyer's entire acceptance test for a 48-video contract | absent | eval capability + empirical memory; not a book gap |
| **G13** | **Sustained throughput as an acceptance condition** — "75-100 a week without quality decay" is a stated buyer requirement at the largest-budget tier | CO-02; MKT-007 | absent | process/eval; not a book gap |
| **G14** | **Cross-asset identity persistence** — load-bearing in 5/18 marketplace cases, primary acceptance condition in 3 | CO-03; MKT-002/006/008/009/011 | scope-only (deliberate Controller decision, to be revisited with this evidence) | eval scope revisit + empirical memory |
| **G15** | **Anti-AI-look negative aesthetics** — buyers state PROHIBITIONS (avoid the AI-avatar look, do not look like stock AI); nothing measures avoidance of a named negative | CO-04; MKT-006, MKT-010 — "the reason a premium tier exists at all" | absent | eval capability + empirical memory; no book holds it |

These four rows exist because the committed ledger (26 Aug) predates the marketplace bank's
integration (CANON-011, 28 Aug) and reflects only the 30 synthetic briefs.

## 5 · EVAL-037 per-brief pack classification (authored)

| brief | media | packs demanded (authored judgement) |
|---|---|---|
| B01 RentOK 30s 9:16 | video | editing, camera, commercial, concept, critique, indian |
| B02 aight poster 4:5 | static | typography, colour, composition, commercial, critique, indian |
| B03 mosambi drink 4:5 | static | composition, colour, product_appearance, commercial, concept, indian |
| B04 skincare UGC 25s 9:16 | video | editing, camera, commercial, critique, indian |
| B05 café dialogue 40s 16:9 | video | camera, editing, concept, critique |
| B06 watch hero 4:5 | static | product_appearance, composition, colour, commercial, critique |

Column sums feeding §2: composition 3, typography 1, product_appearance 2, colour 3, camera 3,
editing 3, commercial 5, concept 3, indian 4, critique 5.

## 6 · Recompute commands

```
cd /home/user/media-intelligence
python3 -c "import json,collections; b=[json.loads(l) for l in open('canon/experiments/v1/brief-bank/briefs.jsonl')]; \
print(len(b), collections.Counter(x['media_class'] for x in b)); \
print(collections.Counter(p for x in b for p in x['tags']['knowledge_packs_required']))"
python3 -c "import yaml; d=yaml.safe_load(open('canon/research/marketplace-demand-v1/derived/marketplace-brief-bank-v1.yaml')); \
print(len(d['cases']), sum(1 for c in d['cases'] if c['normalized_request']['R05_modality']['value']=='video'))"
grep -il 'duration' eval/experiments/EVAL-037/common/briefs/*.txt | wc -l         # 3 of 6
python3 canon/validation/validate_live24_coverage.py                              # runs all checks
```
