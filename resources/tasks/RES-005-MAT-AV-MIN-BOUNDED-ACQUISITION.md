# RES-005 — MAT-AV-MIN bounded acquisition (Stage-Q temporal perturbation base)

**Stream:** Resources · **Assigned:** 28 Aug 2026 · **Branch:** `work/res-005-mat-av-min-acquisition`
**AUTONOMY MODE:** bounded — acquisition mechanics autonomous, every rights or scope
question is a STOP.
**Budget:** ₹0 / USD 0. No paid model call. No account, login, form, terms acceptance,
payment or email.

## Controller instruction this task records

The Controller directed a **bounded acquisition pass for MAT-AV-MIN only**: twelve clean
video clips sufficient to serve as the **Stage-Q temporal perturbation base**, and nothing
further.

Explicitly authorised source classes:

- official / creator-authorised;
- public domain where genuinely applicable;
- permissively licensed and acceptable under the current Resources rights contract;
- material already held by the repository, if it qualifies.

Explicitly excluded: YouTube ripping; pirated clips; unclear reposts; social-media
downloads without rights; request-corpus or user-uploaded identity footage; CC-BY-NC where
the existing contract prohibits commercial empirical use.

Explicitly out of scope: the full 36-clip AV pack; speech/audio evaluator qualification;
paid models.

## Why this is not "broad controlled-pack acquisition"

`coordination/CONTROL-STATE.md` still lists **broad controlled-pack acquisition** as not
authorised, and lists "any separately authorised temporal/governance lanes" as permitted in
parallel. This task is that separate authorisation: one named minimum subset, twelve clips,
one evaluator family, zero spend. It acquires no part of `PACK-PERSON-REF`,
`PACK-PRODUCT-REF` or `PACK-COMMERCIAL`, and no part of `PACK-AV-CLEAN` beyond the
perturbation base.

## Requirement being satisfied

`eval/pre-execution-integration/EVALUATOR-AND-MATERIAL-STAGE-MAP.yaml`:

- `MAT-AV-MIN` — minimum for Stage Q, feeding `MAT-PERT`;
- unblocks `temporal_video`, **9 capabilities**, via injected truth;
- `disjointness_required: false` — perturbation truth is injected, so speaker overlap
  creates no overfitting path;
- `human_labels_required: 0`.

`eval/v1/instruments/FAMILY-4-TEMPORAL-VIDEO.md` states what the base clips must contain:

> "any rights-cleared clean footage with a person, a product and on-screen text would
> serve, since we are testing the *instrument*, not a generator."

and the perturbation table requires, additionally, multi-shot material (horizontal flip of
one shot → screen-direction violation), directional motion (frame-run reversal) and audio
(known-millisecond shift → A/V offset).

## Deliverables

1. `resources/pre-execution-freeze/mat-av-min/CANDIDATE-SPEC-v1.yaml` — one entry per
   distinct source work, with the licence authority a human can open.
2. `resources/scripts/acquire_mat_av_min.py` — retrieval, fingerprinting, clip extraction.
3. `resources/scripts/qualify_mat_av_min.py` — measures the content tags and the
   cleanliness screens. Declares nothing.
4. `resources/pre-execution-freeze/mat-av-min/acquisition-record.json`
5. `resources/pre-execution-freeze/mat-av-min/qualification-measurements.json`
6. `resources/pre-execution-freeze/mat-av-min/MAT-AV-MIN-MANIFEST.csv` / `.jsonl`
7. `resources/pre-execution-freeze/mat-av-min/LINEAGE-MANIFEST.yaml`
8. `resources/pre-execution-freeze/mat-av-min/RES-005-CONTROLLER-BRIEF.md`

Media itself lands under `resources/corpus/raw/mat-av-min/`, which `.gitignore` already
excludes. Manifests, provenance and the retrieval script are committed; raw media is not.

## Stop conditions

Per `shared/AUTONOMY-POLICY.md`, plus specifically:

- any candidate needing a login, form, click-through, payment or API key → drop the
  candidate, record it blocked, continue (pre-approved blocked-candidate handling);
- any candidate whose licence cannot be read at an authority a human can open → drop;
- fewer than 12 clips satisfying rights **and** measured quality → **report the shortfall,
  do not weaken the requirement**.

## Explicit non-goals

Do not start speech/audio evaluator qualification. Do not acquire the remaining 24 clips,
the two-speaker set or the language balance. Do not author creative-quality labels. Do not
merge.
