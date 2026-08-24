# EVAL-004 — Hindi human-reference construction

**Status:** Controller-authorized · 24 Aug 2026  
**Predecessor:** EVAL-003 readiness, merged to `main`  
**Human-time budget:** approximately **3.5–4.5 hours total across two readers**  
**API/model/generator spend:** **not authorized**  
**Purpose:** construct and freeze a two-reader human reference for the existing 54-item Hindi-primary Devanagari calibration pack, then prepare validated altered targets. Stop before any checker/model run.

## Controller decision

Human reference construction is authorized. The approved EVAL-003 pack, matching logic, crop pipeline, blinding design, and reader protocol are frozen for this task.

This task authorizes only:

1. two independent blind Hindi-competent reader passes;
2. freezing and mechanically comparing those passes;
3. using exact reader agreement as the strict V0 reference set;
4. excluding disagreements / `cannot_read` items from the strict gate rather than spending extra human time adjudicating them in V0;
5. deterministic intact/broken target derivation only after the reference is frozen;
6. a short altered-target validity check by either reader after freezing.

It does **not** authorize any checker API/model call, generator run, Capability Registry entry, EVAL-005 work, BSTD use, Marathi stress subset, or change to the calibration methodology.

## Authoritative inputs

Read and follow without redesign:

- `eval/calibration/devanagari-v0/CALIBRATION-RUN-PLAN-V0.md`
- `eval/calibration/devanagari-v0/HUMAN-REVIEW-GUIDE.md`
- `eval/calibration/devanagari-v0/README.md`
- `eval/calibration/devanagari-v0/candidate-manifest.jsonl`
- `eval/calibration/devanagari-v0/review-pack/`

Committed pack configuration remains:

`--overlap-policy admit-once --language-filter hindi --target-n 54`

Expected pack identity: **173 eligible Hindi photographs → 54 selected → 54 distinct photograph hashes**.

## Reader requirements

Use exactly **two distinct human readers**, called `reader_a` and `reader_b` in project records. Do not commit names or other personal details.

Each reader must:

- be competent reading Hindi in Devanagari;
- work independently;
- see only the blinded crop + item ID during Stage 1;
- not see source transcriptions, expected answers, checker/model output, or the other reader's responses before both passes are frozen;
- transcribe what is visibly drawn rather than silently correcting spelling;
- use `cannot_read` / `ambiguous` rather than guessing.

The Controller/operator must confirm privately that `reader_a` and `reader_b` are distinct humans and satisfy the competence requirement before starting. The repository records only this attestation, not identity.

## Stage 0 — preflight before consuming human time

Before either reader begins:

1. regenerate / verify the committed V0 pack using the exact README command;
2. verify `selection-summary.json` still reports 173 eligible Hindi / 54 selected Hindi;
3. verify 54 manifest records and 54 distinct photograph hashes;
4. run `python3 build-candidate-pool.py --self-test` and require PASS;
5. run `python3 materialise-crops.py --self-test` and require PASS;
6. materialise crops and verify reviewer/checker crop-hash identity 54/54;
7. run `python3 build-review-pack.py --verify-blind` and require a clean blind-pack result;
8. verify no source transcription is exposed in the reader interface.

If any preflight check fails, **STOP before human work** and return to Controller. Do not improvise.

## Stage 1 — two independent blind passes

Each reader completes all 54 items independently according to `HUMAN-REVIEW-GUIDE.md`.

Keep the two exports separate. During collection they must not be compared, normalized, corrected, reconciled, or shown to the other reader.

Recommended run evidence paths after each pass is complete:

- `eval/calibration/devanagari-v0/human-reference-v0/reader-a.csv`
- `eval/calibration/devanagari-v0/human-reference-v0/reader-b.csv`

Before committing human responses, ensure files contain only item IDs, transcriptions, status and task-relevant notes; no reader names or personal details.

## Stage 2 — freeze and compare

After **both** passes are complete:

1. freeze both response files before comparison;
2. compute and record SHA-256 for each frozen reader file;
3. compare by item ID mechanically;
4. classify each item as:
   - `exact_agreement`;
   - `reader_disagreement`;
   - `cannot_read_or_ambiguous`;
5. **do not edit either reader file after comparison**;
6. do not normalize spelling or Unicode merely to manufacture agreement unless the already-approved protocol explicitly defines such normalization. V0 strict reference is character-for-character agreement.

For V0:

- `exact_agreement` → eligible strict reference;
- any reader disagreement → excluded from strict gate and reported;
- either `cannot_read` → excluded and reported;
- ambiguous items → excluded from strict gate unless both exact transcriptions and statuses satisfy the existing protocol unambiguously; default to exclusion rather than invention.

**No adjudication human time is authorized in EVAL-004.** If disagreement/rejection leaves fewer than ~20 usable strict-reference items, STOP and return to Controller rather than proceeding to altered targets.

## Stage 3 — reference artifact

Produce a machine-readable reference artifact that contains, per item:

- item ID;
- frozen agreed transcription where applicable;
- reference state (`exact_agreement`, `reader_disagreement`, `cannot_read_or_ambiguous`);
- reader-file hashes / run identifiers sufficient to trace provenance;
- no dataset transcription promoted as truth.

Also report:

- total 54 reviewed by each reader;
- exact-agreement count and rate;
- disagreement count;
- `cannot_read` / ambiguous count;
- final strict-reference count.

Do **not** call this human accuracy or human ceiling. It is agreement/reference-construction evidence for this pack only.

## Stage 4 — deterministic intact/broken targets

Only after the Stage-2 reference is frozen may intact/broken targets be created, using the frozen EVAL-003 run plan rules and no newly invented linguistic rule.

Target assignment must be deterministic and recorded. Only exact-agreement strict-reference items may enter this stage.

If the repository does not yet contain executable deterministic target-derivation tooling that implements the already-approved rules, do **not** hand-author targets ad hoc. Record that implementation gap and STOP after producing the frozen human reference. A separate bounded implementation task can be opened without rerunning the readers.

## Stage 5 — short altered-target human validity check

If deterministic altered targets are successfully produced, either `reader_a` or `reader_b` may perform the short validity check described in the run plan **after the reference is frozen**.

The question is only whether the proposed altered string is visibly different from the frozen agreed reference and image.

- record which reader checked each altered item;
- doubt → drop/reclassify the altered item;
- never alter the frozen reference to fit a target;
- estimated human budget: 20–30 minutes total.

## Stop conditions

Stop and return to Controller if any of the following occurs:

- preflight crop / matching / blinding verification fails;
- the two readers are not genuinely independent;
- reader competence requirement cannot be satisfied;
- fewer than ~20 exact-agreement usable items survive;
- many crops are unreadable or clearly malformed;
- deterministic altered-target tooling required by Stage 4 does not exist or would require inventing new methodology;
- Stage 5 finds many altered targets do not genuinely differ from the visible reading;
- any API/model/checker run would be required to continue.

## Deliverables

At minimum, after Stage 1–3:

- two frozen reader response files (no personal identities);
- their hashes;
- machine-readable agreement/reference artifact;
- short EVAL-004 findings report with counts and exclusions;
- updated `eval/HANDOFF.md` / Controller brief as appropriate.

If Stage 4–5 can be executed strictly under existing frozen rules, also deliver:

- deterministic run-target manifest;
- altered-target validity-check record.

## Completion gate

EVAL-004 completes when the human reference has been frozen and reported, and—only if already-supported deterministic tooling exists—the altered target set has been human-validity checked.

Then **STOP**. Do not run a checker/model. The next Controller decision is checker roster + API/model spend, which must be separately authorized.