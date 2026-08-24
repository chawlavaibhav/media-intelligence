# Controller Brief — EVAL-003

**COMMUNICATION STANDARD:** `shared/COMMUNICATION-STANDARD.md` applies. Terms and numbers are
explained where they carry a decision.

**TASK:** EVAL-003 — Devanagari checker calibration pack readiness
**STATUS:** completed — awaiting Controller review

**Spend:** ₹0 API · 0 hours human specialist time · 0 external calls · 0 generations · 0 capability
results · 0 Registry entries · BSTD reserve untouched.

---

## What this task was for

Before we can ask "is this AI generator good at Hindi text?", we have to answer a prerequisite:
**can our checker read Devanagari at all?** If it cannot, its verdicts about generated Hindi are
worthless regardless of how careful everything downstream is.

EVAL-003 built the package that would answer that — and stopped before it costs anything.

---

## The seven questions you asked, answered

### 1 · What exactly will the Hindi reader see and do?

They open a browser page showing **54 cropped photographs of real Indian street signage**, one at a
time. For each, they type **exactly what they can see drawn** — letter for letter, mistakes included
— or mark it `cannot read` or `ambiguous`.

**They see no expected answer of any kind.** No dataset label, no AI output, no suggestion. This is
verified mechanically: the generated pack was scanned and **contains no Devanagari character
anywhere.**

That blinding is not ceremony. The pull toward the plausible word is exactly what made one AI checker
report six visibly misspelled signs as correct — and it acts on people too. A reader shown a target
and asked "does this match?" tends to see a match.

**About 1.5–2 hours.** Full instructions: `eval/calibration/devanagari-v0/HUMAN-REVIEW-GUIDE.md`.

### 2 · How many independent items do we actually have?

| Step | Count |
|---|---:|
| CVIT images with usable annotations | 551 |
| less byte-identical across the two datasets | −173 |
| less duplicate copies inside one dataset | −3 |
| **Eligible independent photographs** | **202** |
| **Selected for the pack** | **54** |

Independence is by file hash, not filename, and one region per photograph — so the same picture
cannot enter twice. Verified: 54 distinct hashes, zero overlap files leaked in.

**Note:** only ~12% of the 4,476 acquired images carry annotations at all. That follows from
Resources acquiring a partial slice of each archive. Not a problem — 202 is ample — but any later
plan assuming ~4,476 labelled images would be wrong eightfold.

### 3 · Why is the sample varied enough, and what does it still fail to represent?

**Varied:** spread across 12 buckets combining region size and scene clutter, 4–5 items each. Region
area spans **528 to 388,480 pixels** — a 735-fold range — and regions occupy 0.21% to 65.7% of their
frame, in photographs containing 1 to 98 separate words. These are genuinely degraded street
photographs, not clean renders — which the approved plan requires, because clean text does not
separate a strong reader from a weak one.

**What it fails to represent:**
- **Nukta: 1 item in 54** — and only 1 region in 1,629 across the eligible pool. A corpus property,
  not a detection bug; the check covers both the combining mark and precomposed forms.
- **Effectively single-source** — 53 of 54 from IndicSTR12 (see question 4).
- **Blur and contrast not measured** — deterministic in principle, but no image library exists in
  this environment. Recorded as `null` with a stated reason rather than guessed.
- **The buckets are proxies, not a validated difficulty scale.** Nobody has shown "small" means "hard".

### 4 · Is BSTD still genuinely untouched?

**Yes.** 25,252 files present, counted by directory traversal only. **None opened, read, decoded,
inspected or selected.** The builder writes that attestation on every run.

**And it matters more than expected.** Resources reported 173 overlapping files between the two CVIT
datasets. What that means in practice: those 173 are **98% of everything IIIT-ILST has labelled** —
only **3** labelled IIIT-ILST images are unique. **The CVIT lineage is effectively one dataset, so
BSTD is not the preferred cross-source check, it is the only one.**

Resources' warning is carried forward: do not treat BSTD's published train/test split as an
independence guarantee — two duplicate pairs cross it.

### 5 · Did per-item targets change any checker judgement?

**No, and it is proven rather than asserted.**

Both input modes normalise to one work list and call the *same* scoring function. The predicate is
identical; only where the target comes from differs.

**Evidence:** all **27 stored historical transcriptions** re-scored through **both** code paths and
compared against stored verdicts — **0 mismatches.** Wired into
`node eval/harness/run-fixture.mjs --selftest`, so a future change that breaks it fails loudly.

Malformed item files are rejected with named reasons rather than silently skipped — a skipped item
would quietly change what a calibration run measured. Five fixtures cover it.

### 6 · What exact human hours and API actions would the next task require?

| Stage | Human | API |
|---|---|---|
| Blind transcription | **1.5–2 h**, Hindi first-language reader | ₹0 |
| Freeze readings | 0 | ₹0 |
| Derive intact/broken targets | 0 | ₹0 |
| Confirm broken targets differ from what is visible | **20–30 min**, same reader | ₹0 |
| **Run candidate checkers** | 0 | **first API spend** |
| Score | 0 | ₹0 |
| **Total** | **≈ 2–2.5 hours** | per-call cost × volume |

**API cost cannot be quoted** — that needs a model roster, which EVAL-003 was explicitly barred from
selecting. Order of magnitude at our recorded ~₹0.90 per check: low tens of rupees for 54 images
across a small roster with repeats. An estimate from an old figure, not a quote.

**One unresolved prerequisite:** crop materialisation. The manifest carries crop boxes, not cropped
files. The only image tool available here is `sips`, whose offset semantics could not be verified
without pixel inspection — and a silent mis-crop would mean reader and checker judging the *wrong
region*, invisibly. The approved run must implement and verify this before stage 1.

### 7 · What could a clean V0 result let us say — and what could it not?

Assume ~30 usable items, ~15 deliberately altered. A false pass can only happen on an altered item,
so there are **~15 opportunities**, not 30.

**Could say:** *"passed our V0 qualification screen — zero false passes in 15 opportunities on real
photographed Devanagari."*

**Could not say:** *"this checker is accurate."* Zero in 15 is consistent with a true false-pass rate
of **up to ~18%**. A checker that genuinely misses one in ten has roughly a **1-in-5 chance** of
acing 15. Supporting a real "under 5%" claim needs 59 opportunities.

**And two limits specific to this material — see the finding below.**

---

## THE FINDING THAT MATTERS MOST

**Two expert annotation teams, given the same photographs, disagree about one time in three.**

The 173 overlapping files are the only place we have two independent expert readings of the *same
pixels*. Comparing them region by region (matched geometrically, so "annotated different words" is
excluded):

| | |
|---|---:|
| Same-region comparisons | 1,082 |
| **Identical transcription** | **725 (67.0%)** |
| **Different transcription** | **357 (33.0%)** |
| — spelling convention only | 64 (18% of disagreements) |
| — **actually different letters** | **293 (82% of disagreements)** |

Same sign, same box: IndicSTR12 reads `मार्केट`, IIIT-ILST reads `माकेट`. Also `सर्राफा`/`सरर्फि`,
`झेरोक्स`/`झारक्स`.

**Three consequences:**

1. **"Source labels are not ground truth" is now measured, not a policy position.**
2. **Our reader's transcription will also be one reading**, not truth. The record must say "as read
   by X on date Y".
3. **There is a ceiling.** Human-to-human agreement on this exact material is ~67%, or ~73% forgiving
   spelling conventions. **A checker cannot sensibly be held above the rate qualified humans achieve
   here.**

This does **not** contradict the approved calibration plan — that plan already says an instrument
threshold may never exceed measured inter-annotator agreement. **This supplies the number.**

**Caveat:** measured on the overlap set — images one lab chose to reuse — which may not be
representative. And whether any specific pair is a misreading or a legitimate alternative reading is
a Hindi judgement, deliberately not made.

---

## SURPRISES

- **The overlap is far more consequential than its headline number.** "173 shared files" sounds like
  a deduplication chore; it actually means one of our two development sources contributes 3 items.
- **The material is not what the note described.** Not cropped words but full scene photographs with
  up to 98 annotated regions each — which changes what "transcribe the text in this image" even means.
- **The disagreement rate.** I expected source labels to be imperfect. I did not expect a third.

## UNKNOWN / NOT VERIFIED

- Whether crops can be materialised correctly — unresolved by choice, flagged for the approved run.
- How many of the 54 survive the reader. The pool is oversized because this is unknown.
- Whether deterministic "broken" targets are genuinely broken — a string edit can accidentally
  produce a real word. Confirming needs Hindi judgement; deferred to a separate pass **after** the
  blind pass is frozen.
- Whether reading ability predicts judging *generated* text. It does not follow.
- Whether the 33% generalises beyond the overlap set.

## STOP CONDITIONS

**None fired.** Detail in findings §10. The one place native-Hindi judgement would have been required
— validating altered strings — was **deferred rather than invented**, as the task directs.

## DECISIONS NEEDED

1. **Approve the ~2–2.5 hours of Hindi first-language reader time**, and identify the reader. This is
   the only thing blocking stage 1.
2. **Approve a checker roster and API spend** for stage 5. Deliberately not selected here.
3. **Note the ceiling before results exist**, so a ~70%-agreement outcome is read as "consistent with
   human performance on this material", not as a failure.
4. **Accept the crop-materialisation prerequisite** as work belonging to the approved run.

## EVIDENCE WORTH INSPECTING

- `eval/calibration/devanagari-v0/README.md` §"Two findings that change how results must be read".
- `eval/calibration/devanagari-v0/annotator-disagreement.json` — the raw disagreement pairs.
- `eval/calibration/devanagari-v0/review-pack/index.html` — what the reader would actually see.

## FILES

New: `eval/calibration/devanagari-v0/` (builders, manifests, disagreement evidence, blinded review
pack, human-review guide, run plan), `eval/findings/EVAL-003-calibration-readiness-findings.md`,
this brief, per-item fixtures under `eval/harness/fixtures/per-item/`.
Modified: `eval/scripts/check-vlm.mjs` (per-item targets; judgement verified unchanged),
`eval/harness/run-fixture.mjs` (regression coverage), `eval/HANDOFF.md`.
Unchanged: every approved EVAL-001/002 artifact, all Resources material, all historical evidence.

## RECOMMENDED NEXT STEP

*A recommendation, not an action taken.*

Approve the reader time first — it is cheap, it is the gate on everything, and it produces the
reference without which no checker score means anything. Roster and API spend can follow.

## CONFIRMATION

No external model/API/network call. No human review time consumed. No generator run. No capability
result. No Registry entry. No battery, ladder, threshold, observation-unit or Registry change. BSTD
untouched. **EVAL-004 not started.**
