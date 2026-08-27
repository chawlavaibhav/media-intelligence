# Deletion log — RES-005

The Resources charter makes **transient acquisition the default**: retain the bounded useful
subset, hashes, the source URLs and the retrieval script; do not retain bulk source material that
stays reliably reacquirable from its official source. Every deletion is logged.

## Deleted 28 Aug 2026

| What | Size | Why | Recoverable by |
|---|---:|---|---|
| `resources/corpus/raw/mat-av-min/originals/` — the 12 full source works as retrieved | **3.8 GB** | Bulk source material. Each file's SHA-256, byte count, direct URL and retrieval date are recorded in `MAT-AV-MIN-MANIFEST.csv` and `acquisition-record.json` **before** deletion. | `python3 resources/scripts/acquire_mat_av_min.py` — re-downloads from the same official servers and re-cuts identically from the committed spec. |
| `contact-sheets/.frames/` — per-frame PNGs extracted for the OCR text screen | **264 MB** | Rebuildable intermediate of the measurement pass. The measurements themselves are committed in `qualification-measurements.json`. | `python3 resources/scripts/qualify_mat_av_min.py` |
| scratch ingest output — per-frame PNGs from the EVAL-026 ingest check | 941 MB | Rebuildable intermediate of a verification run; never evidence. | rerun the command in `INGEST-VERIFICATION.md` |

**Hashes were recorded before deletion, not after, and none was invented.** A hash of a file no
longer held would be fabricated evidence; every hash here was computed from bytes actually on disk.

## Retained

| What | Size | Why |
|---|---:|---|
| `clips/` — the 12 frozen 10-second clips | 159 MB | The deliverable. |
| `contact-sheets/*.jpg` — 12 frames per clip | 1.3 MB | The evidence behind every person / product / on-screen-text tag. A reviewer must be able to disagree by looking. |

Both are git-ignored under the existing `resources/corpus/raw/` rule. Manifests, provenance,
lineage and the retrieval script are committed.
