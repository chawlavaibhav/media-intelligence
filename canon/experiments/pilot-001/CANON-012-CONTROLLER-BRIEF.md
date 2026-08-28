# Controller Brief — CANON-012

**TASK:** CANON-012 — Aight Normalized Request + Creative IR seed
**STATUS:** completed
**BRANCH:** `work/canon-012-aight-ir-seed` · **Spend:** USD 0 · **Generations:** 0 · **Canon retrieved:** none

**HUMAN SUMMARY:**
The project's two core paper objects — the Normalized Request (a careful record of exactly what the
customer asked for, with nothing invented) and the Creative IR (a statement of what the finished
work should accomplish, before anyone chooses tools) — now exist for the first time against a real
commercial brief: the Aight festive promo. Both schemas held up well enough to be usable, which is
the headline. The task's second purpose was to find where they creak, and it did: eight points of
schema friction were found, none of which blocked the instantiation, but several need a Controller
decision before the pilot or before the next instance is written. The single most important
practical finding is not schema at all: **the official aight logo/wordmark does not exist anywhere
in this repository and was not supplied.** The customer's own hard constraint — "where the wordmark
appears, it must remain exact" — is unverifiable until that asset exists. This is already pilot
gate condition 1 in `CONTROL-STATE.md`; this task confirms it empirically.

**WHAT I DID:**
Treated the Controller-supplied brief in the task file as the customer voice of record. Walked
every field of the frozen request grammar (R01–R18) against the brief text, assigning each value
the strictest provenance it can honestly carry, preserving every absence and recording seven
ambiguities rather than resolving them. Then produced the Creative IR under SPEC-01, making only
the minimum system decisions a "what should exist" object needs (objective class, audience,
concept, a three-beat shape), each labelled `decide` with a rationale and an empty `canon_refs` —
no Canon file was read for creative content, so this instance is a fair base arm for later
Canon-vs-no-Canon experiments. Finally wrote a two-class acceptance contract and this brief.

## OBSERVED

*(directly seen in the brief text, the repository, or the frozen schemas)*

- **Both instances were representable.** No field of the brief was impossible to record; the
  deliverables exist at `canon/experiments/pilot-001/aight-normalized-request.yaml` and
  `canon/experiments/pilot-001/aight-creative-ir.yaml`.
- **Customer-stated facts are few and sharp:** create (generate) · a video · two exact strings
  ("Image ₹9", "Video ₹99") · wordmark exact *where it appears* · modern + premium + Indian
  festive + not gaudy · positioned as an outcome API · "short". Everything else in the brief is
  absent, implied, or an experiment fixture — the grammar's provenance discipline made that
  separation clean to record.
- **No Aight brand asset exists in this repository** (searched 2026-08-28; the only file naming
  Aight is the task itself). Nothing was supplied with the brief. Recorded as a required external
  asset (role `brand_asset`), status MISSING — not invented.
- **Seven ambiguities recorded** (AMB-01…07 in the Normalized Request): festival unnamed; wordmark
  presence/placement only conditionally constrained; no wordmark ground truth (and "logo/wordmark"
  vs the plain string "aight" undetermined); audience unstated; audio entirely unaddressed;
  URL/CTA unstated; price-claim placement/prominence unstated.
- **Schema friction, eight items:**
  - **F1 — no provenance value for "experiment-supplied fixture"** in either vocabulary (grammar:
    customer_stated/customer_implied/system_derived/absent; SPEC-01:
    user/derived/system_decided/brand_policy/customer_memory/default). The 12 s and 9:16 fixtures
    are marked `system_derived`/`system_decided` plus an instance-level `fixture: true` annotation.
    Without a first-class value, a future reader could mistake a fixture for a system judgment —
    or worse, for customer intent.
  - **F2 — the two objects use two different provenance vocabularies for the same concept** (the
    lists above), with no frozen mapping between them. Is `customer_implied` the same as
    `derived`? Is grammar `system_derived` SPEC-01's `system_decided` or its `derived`? Every
    future NR→IR instantiation will re-answer this ad hoc until a mapping is frozen.
  - **F3 — entity-type vocabularies disagree.** Grammar R06 includes `brand_mark` and
    `text_element`; SPEC-01 entities do not, even though R06 claims it "maps to Creative IR
    entities[] ... adds no new capability". The wordmark had to be re-homed under `brand.logo` and
    the price texts under `brand.mandatories`.
  - **F4 — exact price copy has no first-class IR slot.** SPEC-01's copy block offers only
    headline/body/cta; the brand section's `mandatories[]` names "price" in a comment but defines
    no exactness/script machinery. The instance placed the two exact strings in
    `brand.mandatories` with full annotations.
  - **F5 — confidence cannot be honestly filled.** SPEC-01 requires numeric confidence (0.0–1.0)
    on derived/system_decided fields; PROJECT-CONTRACT separation 8 forbids invented decimal
    confidence, and no calibration procedure exists. The instance records
    `confidence: not_assigned` throughout. The same applies to the readiness scores, whose formula
    SPEC-01 deliberately left unfrozen — both are `not_computed`.
  - **F6 — no home for conditional presence, stated style direction, or audience in the request
    grammar.** "Where the wordmark appears" (a constraint conditional on an unrequired presence)
    has no representation; the customer's stated creative direction and any stated audience would
    both land in R18 `acceptance_intent` by default, conflating direction with acceptance.
  - **F7 — no field for a required-but-missing asset.** Grammar R02 and SPEC-01 assets[] register
    only *supplied* assets. The pilot's most important missing input (the wordmark master) had to
    be recorded in an instance-level `required_external_assets` section.
  - **F8 — minor:** the text `script` vocabulary (latin/devanagari/mixed/other) does not address
    currency signs or numerals; "₹" (U+20B9) is neither Latin nor Devanagari. Classified `latin`
    with a note.
- **Acceptance contract:** 6 hard requirements (AC-01/02 exact price strings, verification mode
  hybrid; AC-03 conditional wordmark exactness, **blocked** for lack of ground truth; AC-04/05
  fixtures 12 s and 9:16, machine; AC-06 modality, machine) and 4 customer-stated subjective
  criteria (modern+premium, festive Indian context, not gaudy, outcome-API takeaway), all mode
  human, thresholds deliberately absent (Eval owns thresholds).

## INFERRED

*(interpretation of the observations above — labelled, not fact)*

- **The friction is mostly local, with one architectural seam.** F4, F6, F7, F8 look like local
  vocabulary/slot gaps fixable inside Canon's own specs by ordinary Controller-approved revisions.
  F1, F2 and F3 sit on the Normalized-Request↔Creative-IR boundary itself — the project's
  separation #1 — so an inconsistent fix could quietly blur the line the architecture depends on.
  I tag F1/F2/F3 **ARCHITECTURAL-adjacent** (they need a deliberate cross-object decision, though
  they required no stop: the task explicitly makes recording friction the deliverable), and the
  rest **LOCAL**.
- **AC-01/02 verification honesty matters at pilot time.** Given the project's own evidence — no
  strict-exactness certifier exists, benchmark OCR carries a known error rate — an exact-text
  requirement can be *demanded* here but not *machine-certified* today. Mode `hybrid` was chosen
  so the pilot's human inspection is structurally expected rather than smuggled in.
- **The base Creative IR is deliberately thin, and that is a feature.** With no Canon, the concept
  amounts to careful common sense ("understated festive premium"). If a later Canon-armed instance
  cannot beat this, that is a real finding about Canon's product value.

## SURPRISES / BELIEF UPDATES

- The grammar survived a real brief better than expected — nothing was unrepresentable; the
  failure mode found is *vocabulary misalignment between the two objects*, not missing expressive
  power in either one.
- The sharpest gap was not creative at all: the conditional constraint pattern ("exact *if*
  present") appears in a real first brief and has no representation. Expect it to recur — brand
  marks are routinely conditional.

## FAILURES / BLOCKERS

None for this task. AC-03 (wordmark exactness) is **blocked inside the deliverable** — recorded as
a state, not a waiver — because the ground-truth asset is missing. That blocks part of PILOT-001,
not CANON-012.

## UNKNOWN / NOT VERIFIED

- Whether Aight (the real business) endorses this brief's exact wording — the Controller-supplied
  brief is treated as the customer voice of record by task instruction.
- Whether the two price claims are commercially current — customer-asserted; taken as
  authoritative content, not verified fact.
- Everything under AMB-01…07 remains genuinely open; none was resolved by guessing.

**ASSUMPTIONS CHALLENGED:** none of the entries in `coordination/ASSUMPTIONS.md` was contradicted
by this work; no entry speaks to NR/IR instantiation mechanics.

**LOCAL IMPLICATIONS:** the next Canon instantiation task should reuse the instance-level
conventions introduced here (`fixture: true`, `required_external_assets`, `confidence:
not_assigned`) until the Controller rules on F1–F7 — or explicitly discard them. They are
conventions, not schema.

**CROSS-STREAM IMPLICATIONS:** none requiring another stream's files. One boundary note for Eval,
propose-only: AC-01/02 use verification mode `hybrid` explicitly because of Eval's own
strict-vs-benchmark text findings; when Production IR eventually selects instruments, that mode
choice should be revisited by Eval, not assumed. No `PROPOSED-INTEGRATION-CHANGE` file is needed —
no shared truth is being changed.

**ARCHITECTURAL IMPLICATIONS:** F1/F2/F3 (fixture provenance; NR↔IR provenance mapping;
entity-type alignment) sit on the object boundary — flagged for Controller decision, no change
made. No stop was triggered: CANON-012's own text defines recording schema friction as the
deliverable, and no spec file was modified.

## DECISIONS NEEDED FROM CONTROLLER (RECOMMENDED dispositions attached)

1. **Supply/approve the official Aight brand asset package** (wordmark master at minimum) — pilot
   gate condition 1. Without it AC-03 stays blocked and any on-screen wordmark is unverifiable.
   *Recommended: obtain from the real Aight brand workspace before freezing PILOT-001.*
2. **F1 — fixture provenance.** Add an `experiment_supplied_fixture` provenance value (or bless
   the `fixture: true` annotation) in both vocabularies. *Recommended: add the value; the
   annotation is a workaround.*
3. **F2 — freeze an NR↔IR provenance mapping table** (e.g. customer_stated→user,
   customer_implied→derived, system_derived→system_decided). *Recommended: a one-page mapping
   appended to the grammar via an approved revision, not per-instance judgment.*
4. **F3 — entity-type alignment:** either add brand_mark/text_element to SPEC-01 entities or amend
   R06's mapping note to name their real homes (brand.logo, copy/brand.mandatories).
   *Recommended: the latter — re-homing worked cleanly in practice.*
5. **F4/F6/F7 — local schema gaps** (price-copy slot with exactness; conditional presence; stated
   style/audience homes in the NR; required-but-missing assets). *Recommended: batch into one
   small Controller-approved spec revision after CANON-013 and the pilot surface any further
   friction — one revision, not four.*
6. **F5 — confidence policy:** rule whether `not_assigned` is the standing convention until a
   calibration procedure exists. *Recommended: yes.*
7. **Resolve AMB-05 and AMB-06 before freezing the PILOT-001 brief** (audio treatment; whether
   getaight.ai appears). The others (AMB-01 festival, AMB-04 audience, AMB-07 placement) have safe
   soft defaults recorded and can stay open. *Recommended: one-line Controller answers at brief
   freeze.*

**EVIDENCE WORTH HUMAN INSPECTION:**
- `aight-normalized-request.yaml` — R16 (who said what) and R17 (the seven ambiguities): two
  minutes of reading shows exactly how little the customer actually specified, which is the point
  of the object.
- `aight-creative-ir.yaml` — the acceptance contract: this is what the pilot's human review will
  be scored against; if any entry reads wrong, now is the cheap moment to say so.

**FILES CREATED / MODIFIED:**
- `canon/experiments/pilot-001/aight-normalized-request.yaml` (new)
- `canon/experiments/pilot-001/aight-creative-ir.yaml` (new)
- `canon/experiments/pilot-001/CANON-012-CONTROLLER-BRIEF.md` (new)
No other file touched; no spec, grammar or cross-stream file modified.

**RECOMMENDED NEXT STEP:** Controller review of this brief alongside EVAL-035 and RES-007 per the
pilot gate; decide items 1–7 above (item 1 and item 7's two ambiguities are the only ones the
pilot actually waits on); then freeze the PILOT-001 brief, asset refs and acceptance criteria
before any generation.

**EPISTEMIC CHECK:** Facts above are source-supported (brief text, repository search, frozen
schema texts); interpretations are confined to INFERRED and to labelled rationale fields;
ambiguities and missing assets are recorded, not filled; fixtures are nowhere presented as
customer intent; both text standards are named where exactness verification is discussed; no
unapproved decision is presented as fact.

**CONFIRMATION:** No unapproved next strategic step was started. No Canon was retrieved, no model
or provider named as a choice, no Production IR drafted, no generation attempted, USD 0 spent.
