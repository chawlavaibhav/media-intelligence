# Stage forms — the five-stage questions as files a fresh session fills

Status: PROPOSED 2026-09-22 (Controller, on the founder's "go" for the forms workstream). Source of
the questions: `coordination/audits/AUDIT-2026-09-16-ARCHITECTURAL-AUDIT/QUESTION-TEMPLATE-v0.md`
(v0.1). Nothing here changes Canon, the Registry or any Controller decision.

## Why forms

On every accepted job so far the five-stage questions were asked from a session's memory and the
answers were written as prose. That worked when the session had the template in its context; a
fresh session gets a shorter table from the workflow and improvises the rest. The forms make the
questions a fixed list the kitchen carries, and make the answers readable by a checker, a customer
and a later measurement — without deciding any of the answers.

## The principle: judgement in, enforcement out

The founder's worry, verbatim: "too deterministic that we are making bad media but a better
enforced pipeline. the objective is quality and measurement." The forms are built to that line:

- **Every required field asks for a decision or its reason** (feeling, framing, impact, hero
  frame, cost-if-wrong, why this route). No field fixes a style, a palette, a camera, a joke.
- **The gate (`tools/check_stage.py`) checks presence and traceability only**: a field is there,
  a fact has a source, a claim id exists in the corpus, timings add up, spend is under the cap,
  the checker is not the author. It never scores an answer. A board of seven bland beats passes
  the gate; the customer's verdict and the acceptance statements catch it — and now the record
  shows exactly which decision was bland.
- **Canon is cited, never invented.** `canon` per beat may be empty. An id that is not in the
  accepted corpus or a compiled pack is refused. `retrieved_by: pack | fetcher | hand` records how
  a claim reached the author — the measurement the Canon workstream needs.
- **Measurement is built into Stages 1 and 5.** Stage 1 writes 3–6 acceptance statements
  decidable from the file. Stage 5 scores each one after the customer's verdict, maps every
  customer sentence to a failure id, and gives every failure an earliest stage and the form
  field that would have prevented it. Over jobs this tells us which questions earn their place
  (the template's own rule: a question is removed when three jobs answer it identically with no
  effect on a decision).

## The five forms

| Stage | File in the job | Schema | Gate refuses when |
|---|---|---|---|
| 1 Intent | `stages/01-intent.json` | `form-1-intent.schema.json` | a mandatory item has no verification method; a blocking ask has no answer; a flag is unresolved; fewer than 3 acceptance statements; no cap with a named human |
| 2 Structure | `stages/02-structure.json` | `form-2-structure.schema.json` | a format has no dated source; a fact has no source; a "have" asset has no hash; `sufficient_to_proceed` is false |
| 3 Creative | `stages/03-creative.json` | `form-3-creative.schema.json` | a beat lacks feeling / framing / impact / first_frame; the hero frame is not a beat; a mandatory item is on no beat; timings do not add up; an exact string has no source; a placement names an unknown string; a cited Canon id does not exist; the non-author review is by the author |
| 4 Selection | `stages/04-selection.json` | `form-4-selection.schema.json` | no risk order with a test; a route is `false`; a `manual_only` route has no micro-qualification; expected spend exceeds the Stage 1 cap; more than 4 references; generated text planned |
| 5 Verification | `stages/05-verification.json` | `form-5-verification.schema.json` | the checker is the producer or a form author; a DET check failed; a flag or not-run has no LJ cover; an LJ item is pending; a verdict is recorded without the customer's words; an acceptance statement is unscored; released without acceptance |

Run: `python3 .claude/skills/media-agency/tools/check_stage.py <job_dir> --through N`
(exit 0 = complete). The dispatch tool calls `require_stages_complete(job_dir, 4)` before the
first paid call. Prompts: `python3 .claude/skills/media-agency/tools/build_prompts.py <job_dir>`
writes `gen/prompts/bN-still.txt` and `bN-clip.txt` from the board — the same shape every time.

## The retro-fit (the anti-redo test)

The accepted Mokobara job (`AGY-2026-09-21-MOKOBARA-ODYSSEY-001`, v2 accepted "still some minor
issues but excellent. pass/") was replayed into the five forms: `examples/mokobara-odyssey-001/`.
Form 3 was generated from the job's real `board.json` and `copy-deck.json`; forms 1, 2, 4, 5 were
transcribed from `stages/01…05`, `CHECK-STAGE-5.md`, `HUMAN-VERDICT-V1.md` and `JOB.yaml`. All
five pass the gate; `test_forms.py` (21 tests) holds that and the refusals.

What the replay changed in the forms — fields the accepted job needed that a first draft lacked:

1. **`first_frame` per beat (Stage 3).** The board's `framing` describes the whole action; the
   still must describe the state at `t_in`. The accepted beat-4 still prompt said "right arm inside
   the bag up to the elbow" while the board said "arm to the shoulder, both arms, the paddle".
   That gap is checker failure D1 (the arms never went in past the forearm; i2v cannot be pushed
   past its first frame) — the one defect the customer named twice and that was never repaired.
   Now required for every film beat; the builder refuses a beat without it.
2. **`decision_ref` on every failure (Stage 5).** The checker's table had "earliest stage"; the
   form also asks *which field* would have prevented it. On Mokobara: D5 (paddle continuity) →
   the board had no line for where the paddle goes between beats 4 and 6; D6 (bag geometry) → the
   bag anchor did not forbid an open lid or a hanging pocket. Those are template-level lessons,
   recorded where they can be counted.
3. **`retrieved_by` on every Canon claim (Stage 3).** On Mokobara all 15 claim ids on the board
   were retrieved by hand (2 packs injected, 8 gaps). The field makes the Canon workstream's
   before/after measurable on real jobs.
4. **`reasons_mapped` (Stage 5).** The customer's five v1 sentences map to D6, D1, D5 and two
   "new" composition items (logo lockup, typography) that no gate and no LJ item covered — the
   next two candidate questions for the template.

Prompt builder check: the beat-4 still built from the form shares 81 % of its words with the
accepted hand-written prompt; the differences are ordering and the first-frame line above.

## What is deliberately not in the forms

- No style, palette, camera or humour rules. Those are the author's and Canon's.
- No scoring of answers. `non_author_review.claims_reopened` (line 3.13) is a person's list of
  questions answered with a claim instead of a frame; the gate only requires the review exists.
- No automatic promotion. A field that three jobs fill identically with no effect on a decision
  is a candidate for removal, argued in `/media-agency-sync`, decided by the Controller.

## Job-specific questions

The template's generated layer (one inverse-form question per mandatory item, distinctive asset
and board frame) lives in the prose stage file and in the board's `impact` / `first_frame`
lines; a generated question that informs no decision is deleted with a note. The forms do not
enumerate it because it is job-specific by definition.
