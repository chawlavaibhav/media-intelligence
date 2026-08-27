# Controller Brief — RES-005

**TASK:** RES-005 — MAT-AV-MIN bounded acquisition (Stage-Q temporal perturbation base)
**STATUS:** completed — **12 of 12 frozen**, one cross-stream question needs your decision
**Branch:** `work/res-005-mat-av-min-acquisition` · **not merged**
**Spend:** **₹0 / USD 0.** No paid model call, no account, no login, no form, no terms acceptance,
no payment, no email.

---

## HUMAN SUMMARY

**What this is.** Twelve short video clips, acquired free and legally, that give the *temporal*
evaluator family something clean to break on purpose.

The trick that makes this cheap is worth stating plainly. To test whether a checker can spot a
video defect, you do not need labelled video. You take a clean clip, **inject a defect at a frame
you choose** — freeze a second of it, splice in a different face, alter a word of on-screen text —
and then see whether the checker finds it. Because you caused the defect, the right answer is known
exactly, and **no human has to label anything**. That is why the project's own planning documents
call this the cheapest large unblock available: **nine capabilities become measurable from twelve
clips and zero annotation hours**.

**The result.** All twelve are frozen and all twelve pass the cleanliness screen. Every perturbation
type in Eval's Family-4 table now has at least one base clip. Total cost was zero.

**The catch you need to decide on.** Two frozen documents in this repository define MAT-AV-MIN
differently, and I could not satisfy both. Details in **DECISIONS NEEDED**, and in full in
`resources/PROPOSED-INTEGRATION-CHANGE-RES-005-EVAL.md`. I proceeded on the reading your
instruction implied and recorded the conflict rather than papering over it.

---

## WHAT I DID

Selected twelve **distinct source works** whose licence can be read at a page a human can open,
retrieved each from the rights holder's own server where one exists, fingerprinted what actually
arrived, cut one 10-second clip from each, and then **measured** rather than assumed every property
the temporal plan needs. Where a measurement showed a clip unfit, I moved the sample window and
re-measured — never relaxed the requirement.

---

## OBSERVED

### The twelve clips

| Source family | Works | Licence | Retrieved from |
|---|---:|---|---|
| Blender Foundation open movies | 3 | CC BY 3.0 | `download.blender.org` — the creator's own server |
| NASA (HQ and JPL) | 5 | Public domain, US Government work | `images-assets.nasa.gov` — NASA's own asset server |
| Wikimedia Foundation productions | 2 | CC BY-SA 4.0 | uploaded by WMF's own staff accounts |
| Individual contributors' own work | 2 | CC BY 4.0, CC0 1.0 | licence read back live from the Commons API |

**No CC-BY-NC.** No YouTube ripping, no unclear reposts, no social-media downloads, no
request-corpus or user-uploaded identity footage. Blender's licence was confirmed on the creator's
own project sites (`peach.`, `durian.`, `mango.blender.org`), not inferred from a mirror.

All twelve clips: 10.0 seconds, H.264, audio present, 1280×534 to 3840×2160.

### Cleanliness — 12/12 PASS

A perturbation base must carry **no defect except the injected one**, so each clip was screened for
pre-existing freezes, black frames, interlacing and near-static content:

- pre-existing freeze runs: **0** across all twelve;
- black frames: **0**; interlacing: **0**;
- lowest movement measured: 0.36 (mean frame-to-frame brightness change, 0–255 scale).

### Coverage per perturbation type

| Perturbation from Eval's Family-4 table | Base clips available |
|---|---:|
| freeze N frames | 12 |
| reverse a frame run (direction) | 12 |
| shift audio by known ms | 11 |
| flip one shot (screen direction) | 6 |
| alter rendered text (text mutation) | 6 |
| substitute a product region | 5 |
| splice a rendered character (identity) | 4 |
| splice a **photographed** face (identity) | **3** |

Every type has a base. Two are thin — see UNKNOWN.

---

## INFERRED

The Stage-Q temporal lane is **materially unblocked at zero cost**, provided the Controller settles
which document defines MAT-AV-MIN. The remaining blocker is a definition, not a shortage of media.

---

## SURPRISES / BELIEF UPDATES

**1. A container can lie about its frame rate, and it would have silently ruined the pack.**
One source declared **600 frames per second** while actually carrying 30. Cutting at the declared
rate produced a clip in which **every frame was duplicated twenty times** — meaning the clip was
already nothing but freezes, in a pack whose main job is testing freeze detection. Injected and
pre-existing freezes would have been indistinguishable and the recall number would have been
meaningless. The pipeline now **counts frames inside the clip window** rather than trusting the
declared rate. The check found exactly one true anomaly and correctly left the other eleven alone.

**2. Measuring beat assuming, three times.** Three clips failed on first cut: a NASA press slate
that is a **static text card** (no movement at all, so not usable as video), a media reel window
carrying **eight** pre-existing freezes and a black frame, and a title card held long enough to
register as a freeze. All three were fixed by moving the sample window and re-measuring.

**3. A clip can pass every mechanical check and still be wrong.** MAVM-08's second window measured
perfectly clean — and frame inspection showed it holds only monochrome terrain, with none of the
hardware that entry exists to supply. Only looking caught it. A third window fixed it. **The
mechanical screen tests cleanliness; it does not test fitness for purpose.**

**4. One assumption I had to correct from the frames.** I expected `Wikimedia Foundation Funds
Strategy` to be a talking-head video with real people. It is animation. The tag was corrected from
the contact sheet rather than from the title, which is why the tags are recorded as inspected and
not declared.

---

## FAILURES / BLOCKERS

None outstanding. Two Commons files initially failed to download because already-encoded URLs were
being encoded a second time; fixed, and both retrieved.

---

## UNKNOWN / NOT VERIFIED

**1. Only 3 clips carry a photographed human face, and only 5 carry a manufactured product.**
Family-4 requires detection recall reported **per perturbation type, never as one average**. So
identity-swap recall on real faces will rest on 3 clips and product-swap on 5. That is enough to
run the qualification; it is **not** enough to call a per-type recall figure precise, and it must
not be averaged into a single headline accuracy number.

**2. Rendered characters are not photographed people.** Four clips carry animated or illustrated
figures. Whether an identity-preservation result on a rendered character transfers to a real face
is **an open question, not an assumption**. The tags record `real`, `rendered` and
`real_hand_no_face` separately so this cannot be silently merged.

**3. Twelve clips span only five source lineages** (Blender 3, NASA 5, WMF 2, two individuals 1
each). MAT-AV-MIN sets `disjointness_required: false` because perturbation truth is injected, so
this is not leakage — but a pooled false-positive rate over twelve clips is **less independent than
the count suggests**, and needs a per-lineage breakdown alongside it.

**4. On-screen text presence was screened with Tesseract**, which EVAL-022/023 already established
is unreliable as an exact-text judge. It is used here only to answer *"is there rendered text at
all"*, and every result was confirmed by looking at frames.

**5. Licences are verified as published, not legally reviewed.** Two clips are ShareAlike;
internal evaluation triggers no distribution obligation, but publishing a derived frame later would
carry CC BY-SA onward. One clip's file page carries a `trademarked` restriction on the marks shown.
Both recorded, neither waived.

---

## ASSUMPTIONS CHALLENGED

None. No entry in `coordination/ASSUMPTIONS.md` covers material acquisition.

---

## LOCAL IMPLICATIONS

Resources now holds a documented, reproducible, zero-cost temporal base. Media lives in
`resources/corpus/raw/mat-av-min/` (git-ignored, as repository policy requires); manifests,
provenance, lineage and the retrieval script are committed, so anyone can rebuild it byte-for-byte
from the committed spec.

---

## CROSS-STREAM IMPLICATIONS — `CROSS_STREAM`

Filed as `resources/PROPOSED-INTEGRATION-CHANGE-RES-005-EVAL.md`. Proposed, **not acted on**. No
file outside `resources/**` was modified.

---

## ARCHITECTURAL IMPLICATIONS

None.

---

## DECISIONS NEEDED FROM CONTROLLER

### 1. Which document defines MAT-AV-MIN? *(the one that matters)*

- **Eval's Family-4 spec** says the base needs only *"any rights-cleared clean footage with a
  person, a product and on-screen text"*. Under this reading, **RES-005 delivers it today, for ₹0.**
- **RES-004's stage map** says `MAT-AV-MIN: from_pack: PACK-AV-CLEAN` — controlled recordings with
  **written consent for likeness and voice**. Under this reading the temporal lane stays blocked
  behind a consent instrument that may need external legal review, and these twelve clips are not
  the base.

**Consequence.** One reading opens nine capabilities now at no cost; the other keeps them behind a
legal decision and roughly 73 person-hours of AV work — most of it transcription and turn-boundary
annotation that the temporal family **never reads**.

**My recommendation:** adopt the Eval reading for the temporal base only, and rename this set
(e.g. `MAT-TEMPORAL-BASE`) so it stops borrowing the AV pack's name. `PACK-AV-CLEAN`'s consent,
transcript, turn-boundary and language requirements stay **exactly as they are** for the five
speech capabilities — nothing here weakens them. This is a recommendation, not a decision taken.

### 2. Is 10 seconds the right clip length?

I chose 10 s as sampling mechanics. Re-cutting to any other length is free — the source files are
retained locally and the window is one line in the spec. If Eval wants a different length, say so
before perturbation code is written rather than after.

---

## EVIDENCE WORTH HUMAN INSPECTION

1. **`resources/corpus/raw/mat-av-min/contact-sheets/*.jpg`** — twelve frames per clip. This is how
   the person/product/text tags were set, and you can disagree with any of them by looking.
   `MAVM-06` and `MAVM-09` show the best on-screen text; `MAVM-03` is the only clip with a
   photographed face and a held object together.
2. **`MAT-AV-MIN-MANIFEST.csv`** — one row per clip with source URL, creator, exact licence,
   retrieval date, hashes, duration, resolution, fps, audio, tags and the exact transformation.
3. **`CANDIDATE-SPEC-v1.yaml`, entries MAVM-05/08/09** — the three window revisions, each recording
   the original window and the measured failure that caused the move.

---

## FILES CREATED / MODIFIED

Created — `resources/pre-execution-freeze/mat-av-min/`: `CANDIDATE-SPEC-v1.yaml`,
`acquisition-record.json`, `qualification-measurements.json`, `frame-inspection.json`,
`FRAME-INSPECTION-METHOD.md`, `MAT-AV-MIN-MANIFEST.csv`, `MAT-AV-MIN-MANIFEST.jsonl`,
`LINEAGE-MANIFEST.yaml`, `RES-005-CONTROLLER-BRIEF.md`.
Created — `resources/scripts/`: `acquire_mat_av_min.py`, `qualify_mat_av_min.py`,
`build_mat_av_min_manifest.py`.
Created — `resources/tasks/RES-005-MAT-AV-MIN-BOUNDED-ACQUISITION.md`,
`resources/PROPOSED-INTEGRATION-CHANGE-RES-005-EVAL.md`.
Modified — `resources/HANDOFF.md` (appended RES-005 section).
**No file outside `resources/**` was modified.**

---

## RECOMMENDED NEXT STEP

Settle decision 1. If the Eval reading governs, the next task is Eval's: **write the perturbation
injector** and run Family-4 qualification against these twelve clips. That needs no acquisition, no
human labels and no API spend, and it would produce this project's **first qualified evaluator
family** — against a current floor of zero. This is a recommendation, not work started.

---

## EPISTEMIC CHECK

Licences are quoted from pages named in the spec, not inferred. All numeric properties come from
`ffprobe`/`ffmpeg`/Tesseract output recorded in `qualification-measurements.json`. Content tags come
from recorded frame inspection and are marked as such; where inspection could not settle a
question, the value is not guessed. Interpretations sit under INFERRED, gaps under UNKNOWN, and the
naming/route proposal is marked as a recommendation.

## CONFIRMATION

No unapproved next strategic step was started. Speech/audio evaluator qualification was not begun.
The full 36-clip AV pack was not acquired. No paid model was run. The branch is pushed and **not
merged**.
