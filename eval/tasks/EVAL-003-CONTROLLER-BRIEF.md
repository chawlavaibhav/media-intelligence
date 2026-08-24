# Controller Brief — EVAL-003

**COMMUNICATION STANDARD:** `shared/COMMUNICATION-STANDARD.md` applies. Terms and numbers are
explained where they carry a decision.

**TASK:** EVAL-003 — Devanagari checker calibration pack readiness
**STATUS:** completed — **correction pass applied 24 Aug 2026**, awaiting Controller review.
Ten corrections; two were substantive overclaims of mine. See *Correction pass* below and
findings §11.

**Spend:** ₹0 API · 0 hours human specialist time · 0 external calls · 0 generations · 0 capability
results · 0 Registry entries · BSTD reserve untouched.

---

## FINALIZATION PASS — 24 Aug 2026

All seven finalization items complete. **No blocker remains.**

### Branch sync
`origin/main` merged into `work/eval` with an ordinary merge commit — **no rebase, squash or history
rewrite**. Controller files accepted as authoritative; returned Eval work preserved. Branch is now
current with `main`.

### Adversarial matching regression — added, and it passes
The one-to-one matcher is lifted out of `main()` into testable functions, and
`build-candidate-pool.py --self-test` runs a fabricated case the real corpus does **not** contain:
**two A-regions both above threshold against, and both preferring, the same B-region.**

```
PASS  two A-regions contend for one B-region: superseded matches both  (got 2)
PASS  ...corrected rule uses that B-region at most once  (got 1)
PASS  ...and the contested-partner counter sees it
PASS  the closer of two contenders is the one matched
PASS  matches never exceed min(len(A), len(B))
PASS  no B-region reused / no A-region reused
PASS  pairs below threshold are not matched
PASS  identical inputs match fully
PASS  repeated calls are identical
```

The real-corpus observation is **no longer used as evidence of correctness**, and the `0 of 1,778`
figure is now computed in committed code (`count_contested_partners`) and written to
`annotator-disagreement.json` under `contested_partner_audit`, with an explicit note that zero
contested partners is a property of this corpus and **not** evidence the superseded rule was sound.

### Hindi-primary V0 pack — built, no shortfall

| | |
|---|---:|
| Eligible Hindi-labelled photographs | **173** |
| **Selected** | **54** |
| Distinct SHA-256 among the 54 | **54** |
| Eligible language mix | `{hindi: 173}` |
| Selected language mix | `{hindi: 54}` |

Configuration: `--overlap-policy admit-once --language-filter hindi --target-n 54`.

Each photograph appears **once**, attributed deterministically to one source record; the two dataset
names are not treated as independent evidence. A shortfall guard exits non-zero rather than
substituting another language — it did not fire. Source transcriptions remain provenance metadata,
hidden from readers and checkers.

**Why admit-once was necessary:** all 173 Hindi-labelled records are shared photographs. Under
`exclude` there is no Hindi at all.

Arithmetic, in records:
`551 − 173 (overlap policy 'admit-once') − 3 (same-source dupes) − 202 (language filter 'hindi') = 173`.

### Reviewer qualification and human time

**Two independent Hindi-competent readers.** Every item is Hindi-labelled, so Hindi competence is the
requirement; the guide states explicitly that reading Hindi does not automatically qualify someone
for Marathi.

| Stage | Human |
|---|---|
| Blind transcription, reader A | 1.5–2 h |
| Blind transcription, reader B | 1.5–2 h |
| Freeze, compare, count agreement | 0 |
| Adjudicate disagreements *(optional)* | 0–30 min |
| Confirm altered targets | 20–30 min |
| **Total** | **≈ 3.5–4.5 h across two readers** |

### Stage-4 rule corrected without a third reader
The impossible rule is withdrawn. **Either of the two readers may perform the altered-target check**,
because by that stage the reference is **frozen** and the check has no power to edit or replace it —
it only asks whether a proposed altered string is visibly different from the agreed reference. Doubt
drops the item rather than adjusting the reference, and the checker's identity is recorded. **No
third reader, no extra budget.**

### Stale contradictions removed
Swept and corrected: crops-not-materialised prose in the findings; the one-reader protocol; the
impossible stage-4 rule in three places; "the pool contains no Hindi" as a current-state claim; and
wording implying a Hindi reader is automatically competent for Marathi. Historical trace is kept in
clearly marked correction sections; no obsolete instruction remains followable.

### Resources proposal completed
`eval/PROPOSED-INTEGRATION-CHANGE-EVAL-003-RESOURCES.md` now carries all three points:
1. full-scene / multiple-region correction;
2. **375 IndicSTR12 + 176 IIIT-ILST = 551 locally paired image+annotation records** against 4,476
   acquired images, with a request to distinguish media acquired from locally usable pairs;
3. **173 of the 176 locally paired IIIT-ILST records** are byte-identical to an IndicSTR12 file —
   98.3% of that subset, leaving 3 unique — stated explicitly as a **different denominator** from
   Resources' 12.4% full-source figure, **consistent rather than contradictory**.

No Resources file was edited; no rights or reacquisition change is sought.

### Verification outputs

| Check | Result |
|---|---|
| Builder determinism, Hindi-primary config | byte-identical ✓ |
| 54 items = 54 distinct hashes | ✓ |
| Selected language composition | **54 Hindi** ✓ |
| Adversarial one-to-one regression | 10/10 PASS ✓ |
| Crop geometry self-test | 8/8 PASS ✓ |
| Crop/hash identity, reviewer vs checker | 54/54, 0 mismatches ✓ |
| Blind-pack scan | no Devanagari in pack ✓ |
| 27 historical checker cases | 27 re-scored, **0 judgement mismatches** ✓ |
| Malformed per-item inputs + harness suites | selftest, positive, negative all pass ✓ |
| Absolute machine paths in committed evidence | none ✓ |
| BSTD reserve | 25,252 files, never opened ✓ |
| Human / API / model / generator work | none ✓ |

**Remaining blocker: none.** What EVAL-003 cannot do for itself is spend — two readers' time and a
checker roster with API budget remain Controller decisions.

---

## What this task was for

Before we can ask "is this AI generator good at Hindi text?", we have to answer a prerequisite:
**can our checker read Devanagari at all?** If it cannot, its verdicts about generated Hindi are
worthless regardless of how careful everything downstream is.

EVAL-003 built the package that would answer that — and stopped before it costs anything.

---

## CORRECTION PASS — what changed

| # | Correction | Where |
|---|---|---|
| 1 | "independent expert teams" / "human-to-human ceiling" **withdrawn**; supported conclusion retained | findings §2, README, run plan |
| 2 | Region matching redone **strictly one-to-one**; old and new both reported (identical: 725/1082; 0 of 1,778 contested) | findings §2.1 |
| 3 | "convention only" → `matches_after_selected_diacritic_removal`, marks named | findings §2.2 |
| 4 | Candidate arithmetic restated in **records**: 551 − 346 − 3 = 202 | findings §5 |
| 5 | Language composition measured: **0 Hindi** under the then-current policy; options proposed. **Resolved in the finalization pass — see below** | `PROPOSED-V0-COMPOSITION.md` |
| 6 | Human protocol → **two independent readers**; ≈ 3.5–4.5 h | run plan, review guide |
| 7 | Crop materialisation **solved and verified**; found a real `sips` defect | `materialise-crops.py` |
| 8 | Machine-specific `/Users/...` paths removed from generated metadata | `selection-summary.json` |
| 9 | Cross-stream correction **filed, not applied** | `eval/PROPOSED-INTEGRATION-CHANGE-EVAL-003-RESOURCES.md` |
| 10 | All regressions re-run and passing | *Confirmation* below |

**A defect this pass introduced and caught.** Restructuring the builder silently deleted the manifest
and report writes, leaving stale pre-correction files on disk while the script still reported
success. Found by checking generated files for the new field names instead of trusting the run's exit
code. Restored and re-verified. Recorded because "reports success, writes nothing" is exactly the
class of failure our harness guards against elsewhere.

---

## The seven questions you asked, answered

### 1 · What exactly will the readers see and do?

**Two readers, independently.** Each opens a browser page showing **54 cropped photographs of real
Indian street signage**, one at a time, and types **exactly what they can see drawn** — letter for
letter, mistakes included — or marks it `cannot read` or `ambiguous`. Neither sees the other's
answers.

**The single-reader design is withdrawn.** It would have made one person's transcription the answer
key: if they misread an item, every checker that read it *correctly* would have been scored wrong,
and nothing in the process would have revealed it. Now exact agreement between the two becomes
reference material; disagreements are excluded from the hard gate or adjudicated, and reported
either way. **Neither reader alone becomes ground truth.**

They see the **same crop files the checker will receive** — byte-identical, verified by hash.

**They see no expected answer of any kind.** No dataset label, no AI output, no suggestion. This is
verified mechanically: the generated pack was scanned and **contains no Devanagari character
anywhere.**

That blinding is not ceremony. The pull toward the plausible word is exactly what made one AI checker
report six visibly misspelled signs as correct — and it acts on people too. A reader shown a target
and asked "does this match?" tends to see a match.

**About 1.5–2 hours per reader; ≈ 3.5–4.5 hours total** including a short adjudication and the later
altered-string check — which, per the corrected protocol, **must not be done by the reader who
established that item's original reading.** Full instructions:
`eval/calibration/devanagari-v0/HUMAN-REVIEW-GUIDE.md`.

### 2 · How many independent items do we actually have?

| Step | Records |
|---|---:|
| Labelled source records | 551 |
| less records removed because **both copies** of each of the 173 shared hashes go | **−346** |
| less same-source duplicate records | −3 |
| **Eligible unique photographs** | **202** |
| **Selected for the pack** | **54** |

**Arithmetic corrected:** 173 shared *hashes* remove **346 records**, since each shared photograph is
a record in both datasets. My earlier "551 − 173 − 3" was wrong even though it reached the right
total.

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
- **Hindi: 0 items in 54.** The single largest gap, measured in this correction pass — see the
  composition section below. As built, this calibrates script-general Devanagari reading only.
- **Nukta: 1 item in 54** — and only 1 region in 1,629 across the eligible pool. A corpus property,
  not a detection bug; the check covers both the combining mark and precomposed forms.
- **Effectively single-source** — 53 of 54 from IndicSTR12 (see question 4), and all Marathi.
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
| Blind transcription, **reader A** | **1.5–2 h** | ₹0 |
| Blind transcription, **reader B** (independent) | **1.5–2 h** | ₹0 |
| Freeze both, compare, count agreement | 0 | ₹0 |
| Adjudicate disagreements *(optional)* | 0–30 min | ₹0 |
| Derive intact/broken targets | 0 | ₹0 |
| Confirm altered targets differ — **either reader**; the reference is frozen and cannot be edited | 20–30 min | ₹0 |
| **Run candidate checkers** | 0 | **first API spend** |
| Score | 0 | ₹0 |
| **Total** | **≈ 3.5–4.5 hours across two readers** | per-call cost × volume |

**API cost cannot be quoted** — that needs a model roster, which EVAL-003 was explicitly barred from
selecting. Order of magnitude at our recorded ~₹0.90 per check: low tens of rupees for 54 images
across a small roster with repeats. An estimate from an old figure, not a quote.

**Crop materialisation is now solved** — and solving it caught a real defect.

Crops are materialised once, and **the reviewer and the checker read the same files**, verified by
hash across all 54 items. That replaces "two computations agree" with "it is the same file".

Geometry is proven rather than assumed: a self-test writes a synthetic image in which every pixel
encodes its own coordinates, crops known rectangles, and decodes the result with a dependency-free
PNG reader written for the purpose. **That test found that `sips --cropOffset 0 0` is silently
treated as "no offset" and returns a CENTRE crop** — so any region at the exact image origin would
have been wrong, and nothing downstream would have revealed it. A verified flip-crop-flip workaround
handles that case, and the script refuses to materialise anything if the self-test fails.

### 7 · What could a clean V0 result let us say — and what could it not?

Assume ~30 usable items, ~15 deliberately altered. A false pass can only happen on an altered item,
so there are **~15 opportunities**, not 30.

**Could say:** *"passed our V0 qualification screen — zero false passes in 15 opportunities on real
photographed Devanagari."*

**Could not say:** *"this checker is accurate."* Zero in 15 is consistent with a true false-pass rate
of **up to ~18%**. A checker that genuinely misses one in ten has roughly a **1-in-5 chance** of
acing 15. Supporting a real "under 5%" claim needs 59 opportunities.

**Scope of the claim, after the Hindi-primary rebuild:** the pack is **54 Hindi-labelled
photographs**, so a clean result speaks to **reading Hindi from photographed signage**. It does
**not** automatically transfer to Marathi or to Devanagari-language use generally — the Marathi
stress subset is deferred, not rejected.

**And no threshold may be derived from the 67% cross-dataset figure.** That correction stands.

---

## THE CORRECTION THAT MATTERS MOST

**I overstated the central finding, and you were right to stop it.**

I reported that "two independent expert annotation teams disagree one time in three" and turned 67%
into a **human-performance ceiling** that should bound any evaluator threshold.

**Nothing in the repository supports either claim.** What we have is two dataset releases from the
*same* lab (CVIT / IIIT Hyderabad), each with manual annotations, and **no provenance** about who
made them, whether the annotators were independent, or whether the later release re-annotated or
simply inherited from the earlier one. Two releases from one lineage are not a controlled
inter-annotator study, and I presented them as one.

**Withdrawn:** "independent expert teams", "human-to-human agreement", and the ceiling framing.
**No threshold may be derived from 67% or 73%.**

**What survives, and it is still the useful part:**

> **Source annotations are demonstrably unsafe to promote directly to project ground truth.** Two
> releases from one lineage assign different transcriptions to the same pixels often enough
> (357 of 1,082 matched regions) that adopting either arbitrarily would embed unexamined error.

That is precisely why the protocol establishes its own reference — and now does so with **two**
readers rather than one.

### The matching audit you asked for

You were right that the geometry did not enforce one-to-one correspondence. Implemented strictly
one-to-one: pairs sorted by descending IoU, each region on either side matched at most once,
threshold 0.5 stated explicitly.

**The corrected figures are identical: 725/1082 either way.** The reason is measurable — **0 of
1,778** regions were within threshold of more than one partner, because the two releases' boxes are
near-identical rather than merely overlapping. **The flaw was real; its effect on this corpus was
nil.** Both results are reported side by side so nothing is silently overwritten.

### The "convention only" label, removed

Renamed to `matches_after_selected_diacritic_removal`, with the four marks named (U+094D, U+093C,
U+0902, U+0901). 64 of 357 match after removal. That is a mechanical Unicode result and **is not**
evidence they are equivalent readings.

---

## THE PROBLEM YOU SUSPECTED, MEASURED: the pool has no Hindi in it

**53 Marathi, 1 unlabelled, 0 Hindi.**

**Why:** **all 173 Hindi-labelled records sit inside the excluded overlap.** The smaller dataset's
Devanagari folder *is* the larger dataset's Hindi folder, so "exclude everything that appears in
both" removes every Hindi photograph. Deduplication and Hindi coverage are in structural conflict in
this corpus.

**Why it matters — script-general vs Hindi-specific.** Marathi is written in Devanagari, so Marathi
signage tests **script** reading fine. But the defect we are hunting is a **language-prior** failure:
a vision model reads toward the plausible *word*, which is exactly how one checker passed six
misspelled Hindi signs. A model's Hindi prior is generally stronger than its Marathi prior, so a
Marathi-only pool may **under-detect the very failure we care about** — while our production failure
is Hindi and the checker prompt says "Devanagari (Hindi) text".

*(That the priors differ is a reasonable expectation, not something measured here.)*

**Options, with measured numbers, in `PROPOSED-V0-COMPOSITION.md`:**

| Option | Pool | Composition |
|---|---|---|
| **A** — current default, exclude all overlaps | 202 eligible | 53 Marathi, **0 Hindi** |
| **B** — admit each shared photograph **once** | 375 eligible | **19 Hindi, 35 Marathi** |
| **C** — B, partitioned: Hindi core + Marathi stress subset | 375 eligible | Controller sets the split |

Option B keeps one photograph to one item — verified: 54 items, 54 distinct hashes. It is implemented
behind `--overlap-policy admit-once`; **the default is unchanged and nothing was switched.**

**I recommend C, built on B** — but it is your call, and no new data is needed either way.

## SURPRISES

- **I over-claimed on the central finding and did not catch it myself.** The project's standing rule
  is that external labels are one source's observations — I had the discipline available, and still
  described two releases from one lab as independent expert teams, then built a threshold argument
  on top of it. Review caught it; I did not.
- **The overlap is far more consequential than its headline number.** "173 shared files" sounds like
  a deduplication chore. It actually means one development source contributes 3 items, **and** that
  excluding overlaps removes 100% of the Hindi.
- **The crop self-test earned its keep immediately** by finding that `sips --cropOffset 0 0` silently
  centre-crops. Without it, any region at the image origin would have been wrong invisibly.
- **The matching flaw had zero effect on this data.** Worth fixing regardless — that was luck, not
  design, and a different corpus could easily have differed.

## UNKNOWN / NOT VERIFIED

- **Whether a model's Hindi prior really is stronger than its Marathi prior.** That expectation is
  the argument for fixing the composition, and it is a reasonable expectation, **not** something this
  project has measured.
- **Who produced the source annotations, and whether independently.** The absence of this provenance
  is precisely why the "expert teams" claim was withdrawn.
- Whether two readers will agree often enough to leave a usable gate. Unmeasured until run.
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

1. **Decide the language composition** — Option A (script-general only, 0 Hindi), B (19 Hindi /
   35 Marathi), or C (B, partitioned with a Marathi stress subset). **This is the most consequential
   decision**, because it determines whether a clean result can say anything about Hindi at all.
   I recommend C. No new data is needed for any option.
2. **Approve ≈ 3.5–4.5 hours across two Devanagari-capable readers**, and identify them. Roughly
   double the single-reader estimate; the reason is in the correction above.
3. **Approve a checker roster and API spend** for stage 5. Deliberately not selected here.
4. **Note before results exist** that the first result is a qualification screen bounded at ~18%,
   **and** that no threshold may be derived from the 67% cross-dataset figure.
5. **Action or reject the cross-stream correction** to the Resources source record (item 9).

## EVIDENCE WORTH INSPECTING

- `eval/calibration/devanagari-v0/PROPOSED-V0-COMPOSITION.md` — the 0-Hindi problem and the three
  options. **The decision that matters most.**
- `eval/findings/EVAL-003-calibration-readiness-findings.md` §2 — the withdrawn overclaim in full,
  with the original wording preserved above the correction.
- `eval/calibration/devanagari-v0/annotator-disagreement.json` — raw pairs, plus the corrected and
  superseded matching results side by side.

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
result. No Registry entry. No battery, ladder, threshold, observation-unit or Registry change. No
Resources file edited. No new data acquired. BSTD untouched — 25,252 files, none opened. The
**27/27 historical checker-judgement regression still passes**, along with the harness positive,
negative and selftest suites.
**Human calibration not started. EVAL-004 not started.**
