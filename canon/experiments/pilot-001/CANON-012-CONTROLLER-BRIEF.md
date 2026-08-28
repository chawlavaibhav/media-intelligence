# Controller Brief — CANON-012 (corrected)

**TASK:** CANON-012 — Aight Normalized Request + Creative IR seed
**STATUS:** completed — correction pass applied per
`coordination/decisions/CONTROLLER-PREPILOT-RETURN-REVIEW-1-2026-08-28.md`
**BRANCH:** `work/canon-012-aight-ir-seed` · **Spend:** USD 0 · **Generations:** 0 · **Canon retrieved:** none

## CORRECTION PASS — what changed and what stands

The Controller reviewed the first pass and required four corrections. All four are applied in this
revision. **No schema, grammar or cross-stream file was modified in either pass.**

**What remains valid from the first pass (unchanged):**
- the Normalized Request instance itself — every field value, provenance assignment, the seven
  ambiguities (AMB-01…07), and the customer-vs-fixture separation;
- the Creative IR's semantic content — objective, audience, message, concept, hierarchy, brand
  constraints, three-beat shape, and the two-class acceptance contract (AC-01…AC-10);
- the missing-wordmark finding: the official aight wordmark/master still does not exist in this
  repository, AC-03 remains **blocked** (a recorded state, not a waiver), and this remains a real
  PILOT-001 input gate;
- frictions F1 (fixture provenance), F2 (NR↔IR provenance vocabulary mismatch), F3 (entity-type
  alignment), F5 (confidence conflict), F6, F7, F8 as findings.

**What was corrected:**
1. **Conformance claim.** The first pass said both schemas "held up well enough to be usable"
   without qualification. Corrected: the brief is **semantically representable**, but the Creative
   IR instance is **not strictly conformant to SPEC-01 as written** — SPEC-01 requires numeric
   `confidence: 0.0–1.0` on derived/system-decided fields, PROJECT-CONTRACT forbids invented
   decimal confidence, and the instance therefore carries `confidence: not_assigned`, a documented
   conformance deviation caused by that contract conflict (F5). No numeric confidence was
   fabricated to hide the seam. Stated in the IR file header, its `meta.spec_conformance`, and
   below.
2. **F4 narrowed.** The first pass overstated the gap ("exact price copy has no first-class IR
   slot"). Withdrawn. SPEC-01 **does** have first-class exact-copy machinery
   (`copy.headline/body/cta` with `exactness`, `script_system`) and explicitly permits price under
   `brand.mandatories[]`. The corrected, narrower finding is in OBSERVED below.
3. **False pilot-blinding claim removed.** The first pass claimed PILOT-001 human review must be
   blinded. That was wrong: current CONTROL-STATE requires acceptance criteria **frozen before
   generation** and an **explicit human inspection/acceptance record** — it does **not** require
   blinding. Blinded review belongs to the later architecture outcome experiment. Corrected in the
   IR acceptance-contract note; the freeze-before-generation requirement is kept at full strength.
4. **Instance workarounds are local.** `fixture: true`, `required_external_assets` and
   `confidence: not_assigned` are now explicitly described, in both YAML files and here, as
   **instance-level workarounds for this instance only** — not accepted schema extensions, not new
   frozen vocabulary, not precedent for future tasks. (The first pass's suggestion that future
   tasks reuse them is withdrawn.)

**Controller disposition recorded:** F1/F2/F3/F5 are retained as genuine architecture/spec seams
for later schema revision; the schemas are **not** to be revised before PILOT-001 merely to make
this first instance cleaner. Accordingly, the first pass's schema-decision requests (old items
2–6) are closed as "deferred by Controller decision" and no longer asked.

**HUMAN SUMMARY:**
The project's two core paper objects — the Normalized Request (a careful record of exactly what
the customer asked for, with nothing invented) and the Creative IR (a statement of what the
finished work should accomplish, before anyone chooses tools) — exist for the first time against a
real commercial brief: the Aight festive promo. The honest one-line verdict, corrected per
Controller review: **the brief could be fully represented semantically, and the resulting Creative
IR is usable, but it carries one documented conformance deviation from SPEC-01 as written** — the
confidence fields hold `not_assigned` because SPEC-01's numeric-confidence requirement conflicts
with the project's no-invented-confidence rule. That conflict is itself one of the task's genuine
findings. The most important practical finding is unchanged: **the official aight logo/wordmark
does not exist anywhere in this repository and was not supplied**, so the customer's own hard
constraint — "where the wordmark appears, it must remain exact" — is unverifiable until that asset
exists (PILOT-001 gate condition 1).

**WHAT I DID:**
First pass: treated the Controller-supplied brief as the customer voice of record; walked every
field of the frozen request grammar (R01–R18) against the brief text, assigning each value the
strictest provenance it can honestly carry, preserving every absence and recording seven
ambiguities rather than resolving them; produced the Creative IR under SPEC-01 with only the
minimum system decisions, all with empty `canon_refs`; wrote a two-class acceptance contract.
Correction pass: applied the four Controller-required corrections above to the two YAML instances
and this brief, re-validated YAML syntax and the byte-exactness of the two commercial strings.

## OBSERVED

*(directly seen in the brief text, the repository, or the frozen schemas)*

- **The brief was fully representable semantically; strict conformance was not achieved.** Every
  requirement, absence and ambiguity of the brief is recorded in
  `canon/experiments/pilot-001/aight-normalized-request.yaml` and
  `canon/experiments/pilot-001/aight-creative-ir.yaml`. The Creative IR instance deviates from
  SPEC-01 as written in one documented way: `confidence: not_assigned` where SPEC-01 requires a
  numeric 0.0–1.0 (see F5). The readiness scores are `not_computed`, which is **not** a deviation —
  SPEC-01 itself deliberately left that formula unfrozen.
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
- **Schema friction, eight items (F4 corrected; all unresolved by Controller decision):**
  - **F1 — no provenance value for "experiment-supplied fixture"** in either vocabulary (grammar:
    customer_stated/customer_implied/system_derived/absent; SPEC-01:
    user/derived/system_decided/brand_policy/customer_memory/default). The 12 s and 9:16 fixtures
    are marked `system_derived`/`system_decided` plus an instance-level `fixture: true`
    annotation — a workaround local to this instance, not new vocabulary. Without a first-class
    value, a future reader could mistake a fixture for a system judgment — or worse, for customer
    intent.
  - **F2 — the two objects use two different provenance vocabularies for the same concept** (the
    lists above), with no frozen mapping between them. Is `customer_implied` the same as
    `derived`? Is grammar `system_derived` SPEC-01's `system_decided` or its `derived`? Every
    future NR→IR instantiation will re-answer this ad hoc until a mapping is frozen.
  - **F3 — entity-type vocabularies disagree.** Grammar R06 includes `brand_mark` and
    `text_element`; SPEC-01 entities do not, even though R06 claims it "maps to Creative IR
    entities[] ... adds no new capability". The wordmark had to be re-homed under `brand.logo` and
    the price texts under `brand.mandatories`.
  - **F4 (corrected) — no clean generic representation for multiple independent exact text
    elements.** SPEC-01 **does** provide first-class exact-copy support (`copy.headline/body/cta`
    with `exactness` and `script_system`) and explicitly permits price under
    `brand.mandatories[]`, which is where this instance placed the two exact strings. The narrower
    real gap: the Creative IR has no clean, general way to represent **multiple independently
    required exact commercial strings / arbitrary exact text elements, each potentially carrying
    its own role and exactness semantics**, other than fitting them into headline/body/cta or
    brand mandatories. Two price strings fit `mandatories[]` acceptably; a brief with, say, five
    role-distinct exact strings would strain it. The earlier claim that exact price copy "has no
    first-class IR slot" is withdrawn as overstated.
  - **F5 — the confidence requirement conflicts with the no-invented-confidence rule, producing a
    conformance deviation.** SPEC-01 requires numeric confidence (0.0–1.0) on
    derived/system_decided fields; PROJECT-CONTRACT separation 8 forbids invented decimal
    confidence, and no calibration procedure exists. The instance records
    `confidence: not_assigned` throughout — an instance-level workaround that makes the object
    **not strictly conformant to SPEC-01 as written**. Fabricating numbers would have satisfied
    the letter of SPEC-01 by violating the contract; the deviation is documented instead.
  - **F6 — no home for conditional presence, stated style direction, or audience in the request
    grammar.** "Where the wordmark appears" (a constraint conditional on an unrequired presence)
    has no representation; the customer's stated creative direction and any stated audience would
    both land in R18 `acceptance_intent` by default, conflating direction with acceptance.
  - **F7 — no field for a required-but-missing asset.** Grammar R02 and SPEC-01 assets[] register
    only *supplied* assets. The pilot's most important missing input (the wordmark master) had to
    be recorded in an instance-level `required_external_assets` section — again a local
    workaround, not a schema extension.
  - **F8 — minor:** the text `script` vocabulary (latin/devanagari/mixed/other) does not address
    currency signs or numerals; "₹" (U+20B9) is neither Latin nor Devanagari. Classified `latin`
    with a note.
- **Acceptance contract:** 6 hard requirements (AC-01/02 exact price strings, verification mode
  hybrid; AC-03 conditional wordmark exactness, **blocked** for lack of ground truth; AC-04/05
  fixtures 12 s and 9:16, machine; AC-06 modality, machine) and 4 customer-stated subjective
  criteria (modern+premium, festive Indian context, not gaudy, outcome-API takeaway), all mode
  human, thresholds deliberately absent (Eval owns thresholds). **Pilot review posture
  (corrected):** criteria must be frozen before any generation and PILOT-001 requires an explicit
  human inspection/acceptance record; **blinding is not required for PILOT-001** — it belongs to
  the later architecture outcome experiment.

## INFERRED

*(interpretation of the observations above — labelled, not fact)*

- **The friction is mostly local, with one architectural seam.** F4 (as narrowed), F6, F7, F8 look
  like local vocabulary/slot gaps fixable inside Canon's own specs by ordinary Controller-approved
  revisions. F1, F2 and F3 sit on the Normalized-Request↔Creative-IR boundary itself — the
  project's separation #1 — so an inconsistent fix could quietly blur the line the architecture
  depends on. F5 is a documented conflict between SPEC-01 and the Project Contract. All are now
  explicitly deferred by Controller decision — recorded seams, not open work.
- **AC-01/02 verification honesty matters at pilot time.** Given the project's own evidence — no
  strict-exactness certifier exists, benchmark OCR carries a known error rate — an exact-text
  requirement can be *demanded* here but not *machine-certified* today. Mode `hybrid` was chosen
  so the pilot's human inspection is structurally expected rather than smuggled in.
- **The base Creative IR is deliberately thin, and that is a feature.** With no Canon, the concept
  amounts to careful common sense ("understated festive premium"). If a later Canon-armed instance
  cannot beat this, that is a real finding about Canon's product value.

## SURPRISES / BELIEF UPDATES

- The grammar survived a real brief better than expected — nothing was semantically
  unrepresentable; the failure modes found are *vocabulary misalignment between the two objects*
  and *one internal contract conflict* (F5), not missing expressive power.
- The sharpest gap was not creative at all: the conditional constraint pattern ("exact *if*
  present") appears in a real first brief and has no representation. Expect it to recur — brand
  marks are routinely conditional.
- Correction-pass update: one first-pass finding (F4) did not survive Controller scrutiny at its
  original strength and was narrowed; the next worker should not take the first-pass wording at
  face value anywhere it conflicts with this revision.

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

**LOCAL IMPLICATIONS:** the instance-level workarounds (`fixture: true`,
`required_external_assets`, `confidence: not_assigned`) are local to this instance only. Future
instantiation tasks take their conventions from Controller decisions at that time, not from this
instance — nothing here is precedent.

**CROSS-STREAM IMPLICATIONS:** none requiring another stream's files. One boundary note for Eval,
propose-only: AC-01/02 use verification mode `hybrid` explicitly because of Eval's own
strict-vs-benchmark text findings; when Production IR eventually selects instruments, that mode
choice should be revisited by Eval, not assumed. No `PROPOSED-INTEGRATION-CHANGE` file is needed —
no shared truth is being changed.

**ARCHITECTURAL IMPLICATIONS:** F1/F2/F3 (fixture provenance; NR↔IR provenance mapping;
entity-type alignment) and F5 (SPEC-01 vs Project Contract confidence conflict) sit on or across
object/contract boundaries — flagged, retained, and **explicitly deferred by
`CONTROLLER-PREPILOT-RETURN-REVIEW-1-2026-08-28.md`**: the schemas are not revised before
PILOT-001. No stop was triggered: recording friction is this task's deliverable, and no spec file
was modified in either pass.

## DECISIONS NEEDED FROM CONTROLLER

*(the first pass's schema-decision requests are closed — the Controller has already ruled that
F1/F2/F3/F5 are retained as seams and the schemas are not revised before PILOT-001)*

1. **Supply/approve the official Aight brand asset package** (wordmark master at minimum) — pilot
   gate condition 1. Without it AC-03 stays blocked and any on-screen wordmark is unverifiable.
2. **Resolve AMB-05 and AMB-06 at PILOT-001 brief freeze** (audio treatment; whether getaight.ai
   appears). The others (AMB-01 festival, AMB-04 audience, AMB-07 placement) have safe soft
   defaults recorded and can stay open.

**EVIDENCE WORTH HUMAN INSPECTION:**
- `aight-normalized-request.yaml` — R16 (who said what) and R17 (the seven ambiguities): two
  minutes of reading shows exactly how little the customer actually specified, which is the point
  of the object.
- `aight-creative-ir.yaml` — the conformance statement in the header and the acceptance contract:
  the contract is what the pilot's explicit human acceptance record will be built from; if any
  entry reads wrong, now is the cheap moment to say so.

**FILES CREATED / MODIFIED:**
- `canon/experiments/pilot-001/aight-normalized-request.yaml` (first pass; correction pass added
  workaround-locality notes)
- `canon/experiments/pilot-001/aight-creative-ir.yaml` (first pass; correction pass added the
  conformance statement, narrowed F4 wording, removed the blinding claim)
- `canon/experiments/pilot-001/CANON-012-CONTROLLER-BRIEF.md` (this revision)
No other file touched; no spec, grammar or cross-stream file modified in either pass.

**RECOMMENDED NEXT STEP:** bounded Level-1 Governor review of this branch (the Controller decision
makes CANON-012 eligible after these corrections); then, together with accepted EVAL-035 and
RES-007, freeze PILOT-001's brief, asset refs, acceptance criteria and explicit spend cap before
any generation.

**EPISTEMIC CHECK:** Facts above are source-supported (brief text, repository search, frozen
schema texts, the named Controller decision); interpretations are confined to INFERRED and to
labelled rationale fields; ambiguities and missing assets are recorded, not filled; fixtures are
nowhere presented as customer intent; the conformance deviation is stated rather than papered
over; no numeric confidence was fabricated; both text standards are named where exactness
verification is discussed; no unapproved decision is presented as fact.

**CONFIRMATION:** No unapproved next strategic step was started. No Canon was retrieved, no model
or provider named as a choice, no Production IR drafted, no generation attempted, USD 0 spent in
both passes.
